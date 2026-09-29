<?php
declare(strict_types=1);

namespace RT;

/**
 * Location logic: Texas checks, venue time zones, regions and geocoding.
 *
 * Regions are assigned by nearest anchor city (an approximation of the
 * familiar Texas travel regions). An admin can override any venue's region.
 */
final class Geo
{
    /** region slug => [name, [[lat,lng], …anchor cities]] */
    public const REGIONS = [
        'panhandle-plains' => ['Panhandle & Plains', [[35.222, -101.831], [33.578, -101.855], [34.433, -100.204], [36.058, -102.513], [32.449, -99.733], [33.914, -98.493], [32.251, -101.479], [31.464, -100.437], [32.717, -100.918]]],
        'west-texas'       => ['West Texas & Big Bend', [[31.762, -106.485], [31.997, -102.078], [31.846, -102.368], [31.423, -103.493], [30.358, -103.661], [30.894, -102.879], [31.894, -102.325]]],
        'north-texas'      => ['North Texas & Prairies', [[32.777, -96.797], [32.755, -97.331], [33.215, -97.133], [32.767, -96.599], [32.220, -98.202], [31.549, -97.147], [33.234, -97.586], [32.759, -97.797], [32.347, -97.387], [32.387, -96.848], [30.628, -96.334], [31.117, -97.728], [33.297, -96.989]]],
        'east-texas'       => ['East Texas Piney Woods', [[32.351, -95.301], [32.500, -94.740], [31.338, -94.729], [31.604, -94.655], [30.723, -95.551], [31.318, -95.456], [32.158, -94.337], [32.548, -94.947], [33.157, -94.968], [31.961, -95.270], [33.425, -94.048], [32.204, -95.855]]],
        'gulf-coast'       => ['Gulf Coast', [[29.760, -95.370], [29.691, -95.209], [29.582, -95.761], [29.166, -95.432], [30.080, -94.126], [29.301, -94.798], [27.801, -97.396], [28.805, -97.003], [29.311, -96.103], [30.097, -96.078], [29.949, -96.257], [28.982, -95.969]]],
        'hill-country'     => ['Hill Country & Central Texas', [[30.267, -97.743], [29.883, -97.941], [29.703, -98.124], [30.047, -99.140], [30.275, -98.872], [29.726, -99.074], [30.751, -98.676], [30.671, -97.923], [31.709, -98.991], [31.834, -99.426], [30.508, -97.679]]],
        'south-texas'      => ['South Texas & Rio Grande Valley', [[29.424, -98.494], [27.506, -99.507], [26.203, -98.230], [26.151, -97.991], [25.901, -97.497], [26.190, -97.696], [29.362, -100.897], [29.209, -99.786], [29.569, -97.964], [28.668, -97.388], [27.515, -97.856], [27.752, -98.069]]],
    ];

    /** Counties that officially observe Mountain Time. */
    private const MOUNTAIN_COUNTIES = ['el paso county', 'hudspeth county'];

    public static function isTexasState(?string $state): ?bool
    {
        $s = strtolower(trim((string) $state));
        if ($s === '') {
            return null;
        }
        return in_array($s, ['tx', 'texas', 'tex', 'tx.'], true);
    }

    /** Texas ZIPs: 75000–79999 and 885xx (El Paso). */
    public static function isTexasZip(?string $zip): bool
    {
        return (bool) preg_match('/^(7[5-9]\d{3}|885\d{2})(-\d{4})?$/', trim((string) $zip));
    }

    /** Rough bounding box; a point inside it is only a hint, not proof. */
    public static function inTexasBox(?float $lat, ?float $lng): bool
    {
        return $lat !== null && $lng !== null && $lat >= 25.8 && $lat <= 36.51 && $lng >= -106.65 && $lng <= -93.5;
    }

    /**
     * Decide whether a venue is physically in Texas.
     * @return string 'yes' | 'no' | 'unknown'
     */
    public static function texasVerdict(array $venue): string
    {
        $state = self::isTexasState($venue['state'] ?? null);
        if ($state === true) {
            return 'yes';
        }
        if ($state === false) {
            return 'no';
        }
        $country = strtolower(trim((string) ($venue['country'] ?? '')));
        if ($country !== '' && !in_array($country, ['us', 'usa', 'united states', 'united states of america'], true)) {
            return 'no';
        }
        if (!empty($venue['postal_code'])) {
            return self::isTexasZip($venue['postal_code']) ? 'yes' : 'no';
        }
        return 'unknown';
    }

    /** ZIP codes in El Paso and Hudspeth counties (Mountain Time). */
    private const MOUNTAIN_ZIPS = ['79821', '79835', '79836', '79837', '79838', '79839', '79847', '79849', '79851', '79853'];

    public static function timezoneFor(?string $county, ?float $lng, ?string $zip = null): string
    {
        $z = substr(trim((string) $zip), 0, 5);
        if ($z !== '' && (str_starts_with($z, '799') || str_starts_with($z, '885') || in_array($z, self::MOUNTAIN_ZIPS, true))) {
            return 'America/Denver';
        }
        $c = strtolower(trim((string) $county));
        if ($c !== '') {
            if (!str_ends_with($c, ' county')) {
                $c .= ' county';
            }
            return in_array($c, self::MOUNTAIN_COUNTIES, true) ? 'America/Denver' : 'America/Chicago';
        }
        // No county: only far-west longitudes (El Paso/Hudspeth area) are Mountain.
        return ($lng !== null && $lng < -104.95) ? 'America/Denver' : 'America/Chicago';
    }

    public static function regionSlugFor(?float $lat, ?float $lng): ?string
    {
        if ($lat === null || $lng === null) {
            return null;
        }
        $best = null; $bestD = INF;
        foreach (self::REGIONS as $slug => [, $anchors]) {
            foreach ($anchors as [$alat, $alng]) {
                $d = self::km($lat, $lng, $alat, $alng);
                if ($d < $bestD) {
                    $bestD = $d; $best = $slug;
                }
            }
        }
        return $best;
    }

    public static function regionIdFor(?float $lat, ?float $lng): ?int
    {
        $slug = self::regionSlugFor($lat, $lng);
        if ($slug === null) {
            return null;
        }
        $id = Db::val('SELECT id FROM regions WHERE slug = ?', [$slug]);
        return $id === null ? null : (int) $id;
    }

    public static function km(float $a1, float $o1, float $a2, float $o2): float
    {
        $r = 6371.0;
        $dLat = deg2rad($a2 - $a1); $dLng = deg2rad($o2 - $o1);
        $h = sin($dLat / 2) ** 2 + cos(deg2rad($a1)) * cos(deg2rad($a2)) * sin($dLng / 2) ** 2;
        return 2 * $r * asin(min(1.0, sqrt($h)));
    }

    /**
     * Geocode with OpenStreetMap Nominatim (cached; max 1 request/second).
     * Returns null when disabled, over budget, or nothing found.
     * @return array{lat:float,lng:float,county:?string,state:?string,postal_code:?string,city:?string,precision:string}|null
     */
    /** Max network lookups per process (null = config import.max_geocodes_per_run). */
    public static ?int $budget = null;

    public static function geocode(string $query, bool $cityLevel = false): ?array
    {
        static $lastCall = 0.0;
        static $calls = 0;
        $query = trim($query);
        if ($query === '' || !cfg('geocoder.enabled', true)) {
            return null;
        }
        $hash = hash('sha256', strtolower($query) . ($cityLevel ? '|city' : ''));
        $cached = Db::one('SELECT result FROM geocode_cache WHERE query_hash = ?', [$hash]);
        if ($cached !== null) {
            return $cached['result'] ? json_decode($cached['result'], true) : null;
        }
        if ($calls >= (self::$budget ?? (int) cfg('import.max_geocodes_per_run', 40))) {
            return null;
        }
        $wait = 1.1 - (microtime(true) - $lastCall);
        if ($wait > 0) {
            usleep((int) ($wait * 1_000_000));
        }
        $calls++;
        $url = cfg('geocoder.endpoint', 'https://nominatim.openstreetmap.org/search') . '?' . http_build_query([
            'q' => $query, 'format' => 'jsonv2', 'addressdetails' => 1, 'limit' => 1, 'countrycodes' => 'us',
        ]);
        $r = Http::once($url, ['timeout' => 20, 'headers' => ['Accept: application/json', 'Accept-Language: en']]);
        $lastCall = microtime(true);
        if ($r['error'] !== '' || $r['status'] !== 200) {
            return null;   // transient: do not cache failures
        }
        $data = json_decode($r['body'], true);
        $out = null;
        if (is_array($data) && isset($data[0]['lat'])) {
            $a = $data[0]['address'] ?? [];
            $state = $a['state'] ?? null;
            $out = [
                'lat' => (float) $data[0]['lat'], 'lng' => (float) $data[0]['lon'],
                'county' => $a['county'] ?? null,
                'state' => $state === 'Texas' ? 'TX' : $state,
                'postal_code' => $a['postcode'] ?? null,
                'city' => $a['city'] ?? $a['town'] ?? $a['village'] ?? $a['hamlet'] ?? null,
                'precision' => $cityLevel ? 'city' : ((int) ($data[0]['place_rank'] ?? 0) >= 26 ? 'address' : 'city'),
            ];
        }
        Db::q('INSERT INTO geocode_cache (query_hash, query, result, created_at) VALUES (?,?,?,?)
               ON DUPLICATE KEY UPDATE result = VALUES(result), created_at = VALUES(created_at)',
            [$hash, mb_substr($query, 0, 500), $out ? json_encode($out) : null, now_utc()]);
        return $out;
    }

    /**
     * Geocode venues that still have no coordinates (e.g. after the per-run
     * budget was exhausted). Skips venues edited by an admin.
     * @return int number of venues located
     */
    public static function backfillVenues(int $limit = 40): int
    {
        $n = 0;
        foreach (Db::all("SELECT * FROM venues WHERE location_precision = 'none' AND city IS NOT NULL AND manually_edited = 0 LIMIT " . max(1, $limit)) as $v) {
            $geo = null;
            if ($v['name']) {
                $geo = self::geocode(implode(', ', array_filter([$v['name'], $v['address'], $v['city'], 'TX', $v['postal_code']])));
            }
            $city = false;
            if (!$geo || ($geo['state'] ?? '') !== 'TX') {
                $geo = self::geocode($v['city'] . ', TX', true);
                $city = true;
            }
            if (!$geo || ($geo['state'] ?? '') !== 'TX') {
                continue;
            }
            Db::update('venues', [
                'lat' => $geo['lat'], 'lng' => $geo['lng'], 'location_precision' => $city ? 'city' : $geo['precision'],
                'county' => $v['county'] ?: $geo['county'],
                'timezone' => self::timezoneFor($v['county'] ?: $geo['county'], $geo['lng'], $v['postal_code']),
                'region_id' => $v['region_id'] ?: self::regionIdFor($geo['lat'], $geo['lng']),
                'updated_at' => now_utc(),
            ], 'id = :id', ['id' => $v['id']]);
            Db::q('UPDATE events SET timezone = ? WHERE venue_id = ?', [self::timezoneFor($v['county'] ?: $geo['county'], $geo['lng'], $v['postal_code']), $v['id']]);
            $n++;
        }
        return $n;
    }
}
