<?php
// Streak reminder sender. Run by cron every 15 minutes:
//   /usr/bin/php /home/u401386392/domains/holybiblewords.com/public_html/lib/cron-reminders.php
// Command line only (lib/ is also blocked from the web by .htaccess).
if (PHP_SAPI !== 'cli') { http_response_code(404); exit; }
require __DIR__ . '/push.php';
$r = send_due_reminders();
echo date('c'), " sent={$r['sent']} removed={$r['removed']}\n";
