<?php
/**
 * Refresh the live weather caches (current conditions, hourly + 7-day forecast, alerts,
 * NOAA tides for each station, and National Hurricane Center storms).
 * Suggested schedule: every 15 minutes.   php cron/refresh-weather.php
 */
declare(strict_types=1);
require __DIR__ . '/_cli.php';
define('CCPA_FORCE_REFRESH', true);

$ok = 0;
$jobs = ['current' => 'weather_current', 'forecast' => 'weather_forecast', 'hourly' => 'weather_hourly', 'alerts' => 'weather_alerts', 'tropics' => 'tropics_data'];
foreach (tide_stations() as $id => $label) {
    $jobs['tides ' . $id] = fn() => tides_data((string) $id, true);
}
foreach ($jobs as $name => $fn) {
    $r = $fn(true);
    if ($r && empty($r['stale'])) {
        $ok++;
        $count = $name === 'alerts' ? ' (' . count($r['data']) . ' active)' : '';
        out('cron', "weather $name refreshed$count");
    } else {
        out('cron', "weather $name refresh FAILED" . ($r ? ' (keeping cached copy from ' . date('Y-m-d H:i', (int) $r['fetched']) . ')' : ' (no cached copy)'));
    }
}
exit($ok === count($jobs) ? 0 : 1);
