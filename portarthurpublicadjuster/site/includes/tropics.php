<?php
/**
 * Live tropical data from the National Hurricane Center (nhc.noaa.gov/CurrentStorms.json).
 * Cached in data/cache/tropics.json; refreshed by cron/refresh-weather.php or on page view.
 */

declare(strict_types=1);

require_once __DIR__ . '/weather.php';

/** Great-circle distance in statute miles. */
function miles_between(float $lat1, float $lon1, float $lat2, float $lon2): float
{
    $r = 3958.8;
    $dLat = deg2rad($lat2 - $lat1);
    $dLon = deg2rad($lon2 - $lon1);
    $a = sin($dLat / 2) ** 2 + cos(deg2rad($lat1)) * cos(deg2rad($lat2)) * sin($dLon / 2) ** 2;
    return 2 * $r * asin(min(1, sqrt($a)));
}

/** Initial compass bearing from point 1 to point 2, as a 16-point label. */
function bearing_label(float $lat1, float $lon1, float $lat2, float $lon2): string
{
    $y = sin(deg2rad($lon2 - $lon1)) * cos(deg2rad($lat2));
    $x = cos(deg2rad($lat1)) * sin(deg2rad($lat2)) - sin(deg2rad($lat1)) * cos(deg2rad($lat2)) * cos(deg2rad($lon2 - $lon1));
    return deg_to_compass(fmod(rad2deg(atan2($y, $x)) + 360, 360));
}

function storm_class_label(string $c): string
{
    return [
        'HU' => 'Hurricane', 'TS' => 'Tropical Storm', 'TD' => 'Tropical Depression', 'STS' => 'Subtropical Storm',
        'SD' => 'Subtropical Depression', 'PTC' => 'Potential Tropical Cyclone', 'PC' => 'Post-tropical Cyclone',
        'TY' => 'Typhoon', 'MH' => 'Major Hurricane',
    ][$c] ?? $c;
}

/** Saffir-Simpson category from sustained wind in knots (0 = below hurricane strength). */
function saffir_simpson(int $kt): int
{
    foreach ([[137, 5], [113, 4], [96, 3], [83, 2], [64, 1]] as [$min, $cat]) {
        if ($kt >= $min) {
            return $cat;
        }
    }
    return 0;
}

/** Active storms (all basins) with distance from Port Arthur. */
function tropics_current(bool $allowRefresh = true): ?array
{
    return cached_fetch('tropics', (int) cfg('cache_ttl_tropics', 900), function () {
        $j = http_get_json((string) cfg('nhc_feed'), 10);
        if (!$j || !array_key_exists('activeStorms', $j)) {
            return null;
        }
        $storms = [];
        foreach ($j['activeStorms'] ?? [] as $s) {
            $lat = (float) ($s['latitudeNumeric'] ?? 0);
            $lon = (float) ($s['longitudeNumeric'] ?? 0);
            $kt = (int) ($s['intensity'] ?? 0);
            $storms[] = [
                'id'        => (string) ($s['id'] ?? ''),
                'basin'     => strtolower(substr((string) ($s['id'] ?? ''), 0, 2)),
                'name'      => (string) ($s['name'] ?? ''),
                'class'     => (string) ($s['classification'] ?? ''),
                'label'     => storm_class_label((string) ($s['classification'] ?? '')),
                'wind_kt'   => $kt,
                'wind_mph'  => (int) round($kt * 1.15078),
                'category'  => saffir_simpson($kt),
                'pressure'  => (int) ($s['pressure'] ?? 0),
                'lat'       => $lat,
                'lon'       => $lon,
                'move_dir'  => (int) ($s['movementDir'] ?? 0),
                'move_mph'  => (int) round((float) ($s['movementSpeed'] ?? 0) * 1.15078),
                'updated'   => (string) ($s['lastUpdate'] ?? ''),
                'miles'     => (int) round(miles_between((float) cfg('lat'), (float) cfg('lon'), $lat, $lon)),
                'bearing'   => bearing_label((float) cfg('lat'), (float) cfg('lon'), $lat, $lon),
                'advisory'  => (string) ($s['publicAdvisory']['url'] ?? ''),
                'graphics'  => (string) ($s['forecastGraphics']['url'] ?? ''),
                'discussion'=> (string) ($s['forecastDiscussion']['url'] ?? ''),
                'adv_num'   => (string) ($s['publicAdvisory']['advNum'] ?? ''),
            ];
        }
        // Atlantic first (it is the basin that affects Port Arthur), then closest.
        usort($storms, fn($a, $b) => [$a['basin'] !== 'al', $a['miles']] <=> [$b['basin'] !== 'al', $b['miles']]);
        return $storms;
    }, $allowRefresh);
}

/** Hurricane season status for a timestamp: in season, days until start, etc. */
function hurricane_season(?int $now = null): array
{
    $now = $now ?? time();
    $y = (int) date('Y', $now);
    $start = strtotime("$y-06-01 00:00:00");
    $end = strtotime("$y-11-30 23:59:59");
    if ($now < $start) {
        return ['in' => false, 'days' => (int) ceil(($start - $now) / 86400), 'next' => $start, 'year' => $y];
    }
    if ($now <= $end) {
        return ['in' => true, 'days_left' => (int) ceil(($end - $now) / 86400), 'end' => $end, 'year' => $y,
                'pct' => round(100 * ($now - $start) / ($end - $start))];
    }
    $next = strtotime(($y + 1) . '-06-01 00:00:00');
    return ['in' => false, 'days' => (int) ceil(($next - $now) / 86400), 'next' => $next, 'year' => $y + 1];
}
