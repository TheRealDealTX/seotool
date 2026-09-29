<?php
/**
 * Event import — run by cron or by hand.
 *
 *   php app/bin/import.php                    run all enabled automatic sources now
 *   php app/bin/import.php --cron             weekly job: only proceeds on Monday 07:00 America/Chicago
 *   php app/bin/import.php --daily            daily 7-day check: only at the configured Chicago hour
 *   php app/bin/import.php --source=slug      one source (any adapter)
 *   php app/bin/import.php --source=manual-csv --file=/path/events.csv
 *
 * Hostinger cron runs in the server clock (UTC). Because Chicago moves between
 * UTC-6 (CST) and UTC-5 (CDT), schedule BOTH 12:00 and 13:00 UTC on Mondays:
 *     0 12,13 * * 1   /usr/bin/php /home/<user>/domains/rodeotexas.org/app/bin/import.php --cron
 * The script itself checks the local Chicago time, so exactly one of the two
 * runs does the work, all year, with no edits at DST changes.
 *
 * Exit codes: 0 success/skipped, 1 failed, 2 partial, 3 another run in progress.
 */
declare(strict_types=1);

require_once dirname(__DIR__) . '/bootstrap.php';

use RT\Db;
use RT\Importer;

if (PHP_SAPI !== 'cli') {
    exit("CLI only\n");
}
@set_time_limit(0);
ini_set('memory_limit', '512M');

$opts = getopt('', ['cron', 'daily', 'source:', 'file:', 'force', 'quiet']);
if (isset($opts['quiet'])) {
    putenv('RT_QUIET=1');
}
$chicago = new DateTimeImmutable('now', new DateTimeZone('America/Chicago'));

if (isset($opts['cron']) || isset($opts['daily'])) {
    $daily = isset($opts['daily']);
    if ($daily && !cfg('import.daily_enabled', false)) {
        app_log('cron', 'daily check disabled in config; nothing to do');
        exit(0);
    }
    $wantHour = (int) cfg($daily ? 'import.daily_hour_local' : 'import.weekly_hour_local', $daily ? 6 : 7);
    $wantDay = (int) cfg('import.weekly_weekday', 1);
    $hourOk = (int) $chicago->format('G') === $wantHour;
    $dayOk = $daily || (int) $chicago->format('N') === $wantDay;
    if (!isset($opts['force']) && (!$hourOk || !$dayOk)) {
        app_log('cron', sprintf('%s trigger at %s Chicago — not the scheduled hour, skipped', $daily ? 'daily' : 'weekly', $chicago->format('D H:i T')));
        exit(0);
    }
    // Guard against a second trigger within the same local hour/day (e.g. duplicate cron lines).
    $mode = $daily ? 'daily' : 'weekly';
    $recent = Db::val("SELECT id FROM import_runs WHERE trigger_type = 'cron' AND mode = ? AND status IN ('success','partial','running') AND started_at > ?",
        [$mode, gmdate('Y-m-d H:i:s', time() - ($daily ? 20 : 6 * 24) * 3600)]);
    if ($recent && !isset($opts['force'])) {
        app_log('cron', "{$mode} import already ran recently (run #{$recent}); skipped");
        exit(0);
    }
    $r = Importer::run('cron', $mode, null, null, 'cron');
} else {
    $ids = null;
    $mode = 'weekly';
    if (!empty($opts['source'])) {
        $id = Db::val('SELECT id FROM sources WHERE slug = ?', [$opts['source']]);
        if (!$id) {
            fwrite(STDERR, "Unknown source: {$opts['source']}\n");
            exit(1);
        }
        $ids = [(int) $id];
        $mode = 'single';
    }
    $file = $opts['file'] ?? null;
    if ($file !== null && !is_file($file)) {
        fwrite(STDERR, "File not found: {$file}\n");
        exit(1);
    }
    $r = Importer::run('cli', $mode, $ids, $file, get_current_user() ?: 'cli');
}

echo "Run #{$r['run_id']}: {$r['status']} — {$r['message']}\n";
app_log('cron', "run #{$r['run_id']} {$r['status']}: {$r['message']}");
exit(['success' => 0, 'failed' => 1, 'partial' => 2, 'locked' => 3][$r['status']] ?? 1);
