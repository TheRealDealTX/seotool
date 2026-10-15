<?php
// Address -> evacuation zone (+ nearest Escambia shelters).
// Geocoding: U.S. Census Bureau geocoder. Zones: Escambia County and
// Santa Rosa County public GIS layers.
require __DIR__ . '/_lib.php';
ph_rate_limit('zone', 20, 60);

$address = trim((string) ($_GET['address'] ?? ''));
if (strlen($address) < 5 || strlen($address) > 200) {
    ph_json(['error' => 'Please enter a full street address.'], 400);
}
if (!preg_match('/\b(FL|Florida)\b/i', $address)) {
    $address .= ', FL';
}

$geo = ph_cached_fetch('https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?' . http_build_query([
    'address' => $address,
    'benchmark' => 'Public_AR_Current',
    'vintage' => 'Current_Current',
    'layers' => 'Counties',
    'format' => 'json',
]), 86400);
$match = $geo ? (json_decode($geo, true)['result']['addressMatches'][0] ?? null) : null;
if (!$match) {
    ph_json(['error' => "We couldn't find that address."]);
}
$lon = (float) $match['coordinates']['x'];
$lat = (float) $match['coordinates']['y'];
$county = $match['geographies']['Counties'][0]['NAME'] ?? '';
$out = ['matched' => $match['matchedAddress'], 'lat' => $lat, 'lon' => $lon, 'county' => $county,
        'zone' => null, 'zone_info' => null, 'supported' => false, 'shelters' => []];

function zone_query(string $layer, float $lon, float $lat, string $field, int $buffer = 0): array
{
    $q = [
        'geometry' => "$lon,$lat", 'geometryType' => 'esriGeometryPoint', 'inSR' => 4326,
        'spatialRel' => 'esriSpatialRelIntersects', 'outFields' => '*', 'returnGeometry' => 'false', 'f' => 'json',
    ];
    if ($buffer) {
        $q['distance'] = $buffer;
        $q['units'] = 'esriSRUnit_Meter';
    }
    $body = ph_cached_fetch($layer . '/query?' . http_build_query($q), 86400 * 7);
    $rows = [];
    foreach (($body ? (json_decode($body, true)['features'] ?? []) : []) as $f) {
        $rows[] = $f['attributes'];
    }
    usort($rows, fn($a, $b) => strcmp((string) $a[$field], (string) $b[$field]));   // A (most vulnerable) first
    return $rows;
}

function miles(float $a, float $b, float $c, float $d): float
{
    $r = 3958.8;
    $dl = deg2rad($c - $a);
    $dn = deg2rad($d - $b);
    $x = sin($dl / 2) ** 2 + cos(deg2rad($a)) * cos(deg2rad($c)) * sin($dn / 2) ** 2;
    return 2 * $r * asin(sqrt($x));
}

if (stripos($county, 'Escambia') === 0) {
    $out['supported'] = true;
    $rows = zone_query('https://gismaps.myescambia.com/arcgis/rest/services/Escambia_County/MapServer/15', $lon, $lat, 'EVAC_ZONE');
    $out['zone'] = $rows[0]['EVAC_ZONE'] ?? null;
    $sh = ph_cached_fetch('https://gismaps.myescambia.com/arcgis/rest/services/Escambia_County/MapServer/12/query?' . http_build_query([
        'where' => '1=1', 'outFields' => 'SHELTERNAM,SHELTERTYP,SHELTERLOC,ADDRESS,CITYSTZIP,X,Y', 'returnGeometry' => 'false', 'f' => 'json',
    ]), 86400);
    $list = [];
    foreach (($sh ? (json_decode($sh, true)['features'] ?? []) : []) as $f) {
        $a = $f['attributes'];
        $list[] = [
            'name' => ucwords(strtolower($a['SHELTERNAM'])),
            'type' => str_ireplace(['(ehpa)', 'Bldg '], ['(EHPA)', 'Building '], ucwords(strtolower(trim($a['SHELTERTYP'] . ' - ' . $a['SHELTERLOC'], ' -')))),
            'address' => ucwords(strtolower($a['ADDRESS'])) . ', ' . preg_replace('/\bFl\b/', 'FL', ucwords(strtolower($a['CITYSTZIP']))),
            'miles' => round(miles($lat, $lon, (float) $a['Y'], (float) $a['X']), 1),
        ];
    }
    usort($list, fn($a, $b) => $a['miles'] <=> $b['miles']);
    $out['shelters'] = array_slice($list, 0, 4);
} elseif (stripos($county, 'Santa Rosa') === 0) {
    $out['supported'] = true;
    $layer = 'https://cloud.santarosa.fl.gov/arcgis/rest/services/Hosted/OpenData_EvacuationZones/FeatureServer/0';
    $rows = zone_query($layer, $lon, $lat, 'evac');
    if (!$rows) {
        $rows = zone_query($layer, $lon, $lat, 'evac', 40);   // tolerate tiny gaps between zone polygons
    }
    $out['zone'] = $rows[0]['evac'] ?? null;
    $out['zone_info'] = $rows[0]['evacinfo'] ?? null;
}
ph_json($out);
