<?php
// Evacuation zone lookup for Okaloosa and Walton counties.
//   /api/zone.php?address=...   address -> zone (+ nearest shelter sites)
//   /api/zone.php?shelters=1    Okaloosa County shelter sites with GIS status
// Geocoding: U.S. Census Bureau geocoder.
// Okaloosa zones + shelters: the county's hosted Emergency_Layers service
//   (the same layers its official "Evacuations" zone-search app reads).
// Walton zones: Walton County's published EvacuationZones layer (county
//   storm-surge zones from the 2010 Statewide Regional Evacuation Study); the
//   response tells the visitor to confirm with Walton County EM.
require __DIR__ . '/_lib.php';
dh_rate_limit('zone', 20, 60);

const OKA_ZONES = 'https://services7.arcgis.com/lOFQguHNarTIBTRU/arcgis/rest/services/Emergency_Layers/FeatureServer/0';
const OKA_SHELTERS = 'https://services7.arcgis.com/lOFQguHNarTIBTRU/arcgis/rest/services/Emergency_Layers/FeatureServer/109';
const WAL_ZONES = 'https://services1.arcgis.com/TaXHPwWfIMuzJ7Ov/ArcGIS/rest/services/EvacuationZones/FeatureServer/0';

// Walton County's primary shelter (Walton County All Hazards Preparedness Guide).
const WAL_SHELTER = ['name' => 'Freeport High School', 'address' => '12615 US-331 Bus, Freeport, FL 32439',
                     'lat' => 30.5448, 'lon' => -86.1178, 'status' => ''];

function miles(float $a, float $b, float $c, float $d): float
{
    $dl = deg2rad($c - $a);
    $dn = deg2rad($d - $b);
    $x = sin($dl / 2) ** 2 + cos(deg2rad($a)) * cos(deg2rad($c)) * sin($dn / 2) ** 2;
    return 7917.6 * asin(sqrt($x));
}

/** Attributes of the polygons containing (or, with $buffer metres, near) a point. */
function zones_at(string $layer, float $lon, float $lat, string $fields, int $buffer = 0): array
{
    $q = ['geometry' => "$lon,$lat", 'geometryType' => 'esriGeometryPoint', 'inSR' => 4326,
          'spatialRel' => 'esriSpatialRelIntersects', 'outFields' => $fields, 'returnGeometry' => 'false', 'f' => 'json'];
    if ($buffer) {
        $q['distance'] = $buffer;
        $q['units'] = 'esriSRUnit_Meter';
    }
    $body = dh_cached_fetch($layer . '/query?' . http_build_query($q), 86400);
    $rows = [];
    foreach (($body ? (json_decode($body, true)['features'] ?? []) : []) as $f) {
        $rows[] = $f['attributes'];
    }
    return $rows;
}

function okaloosa_shelters(): array
{
    $body = dh_cached_fetch(OKA_SHELTERS . '/query?' . http_build_query([
        'where' => '1=1', 'outFields' => 'FACILITY_NAME,SITE_ADDR,ZIP_CITY,STATUS', 'returnGeometry' => 'true', 'outSR' => 4326, 'f' => 'json',
    ]), 900);
    $out = [];
    foreach (($body ? (json_decode($body, true)['features'] ?? []) : []) as $f) {
        $a = $f['attributes'];
        $addr = ucwords(strtolower(trim((string) $a['SITE_ADDR'])));
        $addr = preg_replace_callback('/\b(Nw|Ne|Sw|Se|Fl|E|W)\b/', fn($m) => strtoupper($m[1]), $addr);
        $city = ucwords(strtolower(trim((string) ($a['ZIP_CITY'] ?? ''))));
        if ($city !== '' && ($p = strripos($addr, ' ' . $city . ' FL')) !== false) {
            $addr = substr($addr, 0, $p) . ', ' . $city . substr($addr, $p + strlen($city) + 1);
        }
        $addr = preg_replace('/ FL (\d{5})$/', ', FL $1', $addr);
        $out[] = [
            'name' => ucwords(strtolower((string) $a['FACILITY_NAME'])),
            'address' => $addr,
            'status' => trim((string) ($a['STATUS'] ?? '')),
            'lat' => (float) ($f['geometry']['y'] ?? 0),
            'lon' => (float) ($f['geometry']['x'] ?? 0),
        ];
    }
    foreach ($out as &$s) {
        $s['name'] = str_replace(['Nwfsc', 'Special Needs Shelter'], ['NWFSC', '(special needs)'], $s['name']);
    }
    usort($out, fn($a, $b) => strcmp($a['name'], $b['name']));
    return $out;
}

if (!empty($_GET['shelters'])) {
    $list = array_map(fn($s) => array_diff_key($s, ['lat' => 1, 'lon' => 1]), okaloosa_shelters());
    dh_json(['shelters' => $list, 'source' => OKA_SHELTERS], $list ? 200 : 502, 300);
}

$address = trim((string) ($_GET['address'] ?? ''));
if (strlen($address) < 6 || strlen($address) > 200) {
    dh_json(['error' => 'Please enter a full street address.'], 400);
}
if (!preg_match('/\b(FL|Florida)\b/i', $address)) {
    $address .= ', FL';
}
$geo = dh_cached_fetch('https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?' . http_build_query([
    'address' => $address, 'benchmark' => 'Public_AR_Current', 'vintage' => 'Current_Current', 'layers' => 'Counties', 'format' => 'json',
]), 86400);
$match = $geo ? (json_decode($geo, true)['result']['addressMatches'][0] ?? null) : null;
if (!$match) {
    dh_json(['error' => "That address could not be matched."]);
}
$lon = (float) $match['coordinates']['x'];
$lat = (float) $match['coordinates']['y'];
$county = $match['geographies']['Counties'][0]['NAME'] ?? '';
$out = ['matched' => $match['matchedAddress'], 'county' => $county, 'zone' => null, 'zone_info' => null,
        'conflict' => null, 'supported' => false, 'source_note' => null, 'shelters' => []];

if (stripos($county, 'Okaloosa') === 0) {
    $out['supported'] = true;
    $fields = 'EVAC_ZONE,EvacDesc,EvacDefinition';
    $rows = zones_at(OKA_ZONES, $lon, $lat, $fields) ?: zones_at(OKA_ZONES, $lon, $lat, $fields, 40);
    $letters = [];
    foreach ($rows as $r) {
        $z = strtoupper(trim((string) ($r['EVAC_ZONE'] ?? '')));
        if ($z !== '') {
            $letters[] = $z;
        }
        // Some polygons carry a different letter in their description; keep both.
        if (preg_match('/^ZONE ([A-E])$/', strtoupper(trim((string) ($r['EvacDesc'] ?? ''))), $m)) {
            $letters[] = $m[1];
        }
        if (in_array($z, ['G', 'H'], true)) {
            $out['zone_info'] = ucfirst(strtolower((string) ($r['EvacDefinition'] ?? '')));
        }
    }
    $surge = array_values(array_unique(array_filter($letters, fn($l) => preg_match('/^[A-E]$/', $l))));
    sort($surge);                                  // A = most exposed
    if ($surge) {
        $out['zone'] = $surge[0];
        if (count($surge) > 1) {
            $out['conflict'] = array_map(fn($l) => "Zone $l", $surge);
        }
    } elseif (array_intersect($letters, ['G', 'H'])) {
        $out['zone'] = in_array('G', $letters, true) ? 'G' : 'H';
    }
    $out['source_note'] = 'Zone from Okaloosa County Public Safety GIS (2020 storm-surge modeling).';
    foreach (okaloosa_shelters() as $s) {
        $s['miles'] = round(miles($lat, $lon, $s['lat'], $s['lon']), 1);
        unset($s['lat'], $s['lon']);
        $out['shelters'][] = $s;
    }
    usort($out['shelters'], fn($a, $b) => $a['miles'] <=> $b['miles']);
    $out['shelters'] = array_slice($out['shelters'], 0, 4);
} elseif (stripos($county, 'Walton') === 0) {
    $out['supported'] = true;
    $rows = zones_at(WAL_ZONES, $lon, $lat, 'EVAC_ZONE') ?: zones_at(WAL_ZONES, $lon, $lat, 'EVAC_ZONE', 40);
    $letters = array_values(array_unique(array_filter(array_map(fn($r) => strtoupper(trim((string) ($r['EVAC_ZONE'] ?? ''))), $rows),
        fn($l) => preg_match('/^[A-E]$/', $l))));
    sort($letters);
    $out['zone'] = $letters[0] ?? null;
    $out['source_note'] = "Zone from Walton County's published storm-surge evacuation-zone layer. Walton County EM can revise zones, so confirm yours at waltoncountyem.org or 850-892-8065.";
    $s = WAL_SHELTER;
    $s['miles'] = round(miles($lat, $lon, $s['lat'], $s['lon']), 1);
    unset($s['lat'], $s['lon']);
    $out['shelters'] = [$s];
}
dh_json($out);
