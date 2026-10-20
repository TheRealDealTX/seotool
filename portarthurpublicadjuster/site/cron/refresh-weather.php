<?php
/**
 * Refresh the live weather caches (current conditions, 7-day forecast, alerts, NHC tropics).
 * Suggested schedule: every 15 minutes.   php cron/refresh-weather.php
 */
declare(strict_types=1);
require __DIR__ . '/_cli.php';
define('MPA_FORCE_REFRESH', true);
require_once MPA_ROOT . '/includes/tropics.php';

$ok = 0;
foreach (['current' => 'weather_current', 'forecast' => 'weather_forecast', 'alerts' => 'weather_alerts'] as $name => $fn) {
    $r = $fn(true);
    if ($r && empty($r['stale'])) {
        $ok++;
        $count = $name === 'alerts' ? ' (' . count($r['data']) . ' active)' : '';
        out('cron', "weather $name refreshed$count");
    } else {
        out('cron', "weather $name refresh FAILED" . ($r ? ' (keeping cached copy from ' . date('Y-m-d H:i', (int) $r['fetched']) . ')' : ' (no cached copy)'));
    }
}
$t = tropics_current(true);
out('cron', $t && empty($t['stale']) ? 'tropics refreshed (' . count($t['data']) . ' active storm(s))' : 'tropics refresh FAILED');
exit($ok === 3 ? 0 : 1);
