<?php
/**
 * One cron entry that runs everything on a sensible cadence.
 * Hostinger: Advanced → Cron Jobs → "Custom" → every 15 minutes:
 *   /usr/bin/php /home/USERNAME/domains/mcallenpublicadjuster.com/public_html/cron/run-all.php
 */
declare(strict_types=1);
if (PHP_SAPI !== 'cli') {
    http_response_code(403);
    exit;
}
$php = PHP_BINARY ?: 'php';
$dir = __DIR__;
$min = (int) date('i');
$hour = (int) date('G');
$jobs = ['refresh-weather.php'];                                  // every run (15 min)
if ($min < 15) $jobs[] = 'update-weather-events.php';             // hourly
if ($hour === 3 && $min < 15) $jobs[] = 'maintenance.php';        // daily 3 AM
if ($hour === 4 && $min < 15 && date('N') === '1') $jobs[] = 'update-storm-history.php'; // Mondays 4 AM
$code = 0;
if (!function_exists('passthru')) {
    fwrite(STDERR, "passthru() is disabled on this server. Add each script as its own cron job instead (see INSTALL guide).\n");
    exit(1);
}
foreach ($jobs as $job) {
    passthru(escapeshellarg($php) . ' ' . escapeshellarg("$dir/$job"), $rc);
    $code = max($code, $rc);
}
exit($code);
