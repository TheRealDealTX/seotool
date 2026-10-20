<?php
/**
 * Housekeeping: purge expired weather alerts, old rate-limit/nonce files, and stale locks.
 * Suggested schedule: daily.   php cron/maintenance.php
 */
declare(strict_types=1);
require __DIR__ . '/_cli.php';
require_once MPA_ROOT . '/includes/form.php';

$removed = cleanup_ratelimit_dir();
out('cron', "Removed $removed old rate-limit/nonce file(s)");

$alertsFile = data_path('cache/wx-alerts.json');
$a = read_json_file($alertsFile, null);
if ($a && isset($a['data']) && is_array($a['data'])) {
    $before = count($a['data']);
    $a['data'] = array_values(array_filter($a['data'], fn($x) => empty($x['expires']) || strtotime($x['expires']) > time()));
    write_json_file($alertsFile, $a);
    out('cron', 'Expired alerts removed: ' . ($before - count($a['data'])));
}
foreach (glob(data_path('cache') . '/*.lock') ?: [] as $lock) {
    if (filemtime($lock) < time() - 300) {
        @unlink($lock);
    }
}
foreach (glob(data_path('cache') . '/*.tmp') ?: [] as $t) {
    @unlink($t);
}
exit(0);
