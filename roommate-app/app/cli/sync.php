<?php
// Daily cron: php app/cli/sync.php  — imports/updates all listings from riseapartments.com
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
$_SERVER['REQUEST_METHOD'] = 'GET';
$_SERVER['HTTP_HOST'] = 'cli';
set_time_limit(0);
require dirname(__DIR__) . '/bootstrap.php';
migrate();
$page = 1; $added = $updated = 0;
do {
    $r = sync_rise_page($page);
    $added += $r['added']; $updated += $r['updated'];
    $page++;
} while ($page <= $r['total_pages']);
q('INSERT INTO settings (k, v) VALUES (?, ?) ON DUPLICATE KEY UPDATE v = VALUES(v)', ['last_sync', date('c') . " (cron: +$added new, $updated updated)"]);
echo "added=$added updated=$updated\n";
