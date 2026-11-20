<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
$c = fn($sql, $p = []) => (int)val($sql, $p);
$stats = [
    'Pending review' => [$c("SELECT COUNT(*) FROM listings WHERE status = 'pending'"), '/admin/listings/?status=pending'],
    'Live listings' => [$c("SELECT COUNT(*) FROM listings WHERE status = 'active'"), '/admin/listings/?status=active'],
    'Verified (paid) live' => [$c("SELECT COUNT(*) FROM listings WHERE status = 'active' AND tier = 'paid'"), '/admin/listings/?tier=paid'],
    'Awaiting payment' => [$c("SELECT COUNT(*) FROM listings WHERE status = 'pending_payment'"), '/admin/listings/?status=pending_payment'],
    'Owners' => [$c('SELECT COUNT(*) FROM owners'), '/admin/owners/'],
    'Open reports' => [$c('SELECT COUNT(*) FROM reports WHERE resolved = 0'), '/admin/reports/'],
    'Messages (7 days)' => [$c('SELECT COUNT(*) FROM messages WHERE created_at > ?', [gmdate('Y-m-d H:i:s', time() - 7 * 86400)]), '/admin/messages/'],
    'Revenue (all time)' => ['$' . number_format($c("SELECT COALESCE(SUM(amount_cents),0) FROM payments WHERE status = 'complete'") / 100, 2), '/admin/payments/'],
];
$h = '<div class="stat-grid">';
foreach ($stats as $label => [$n, $url]) $h .= '<a class="stat" href="' . e($url) . '"><strong>' . e($n) . '</strong><span>' . e($label) . '</span></a>';
$h .= '</div>';
$checks = [
    'SMTP password set' => (string)cfg('smtp.pass') !== '',
    'Stripe secret key' => stripe_secret() !== '',
    'Stripe webhook secret' => stripe_webhook_secret() !== '',
    'GTM container ID' => setting('gtm_id') !== null,
    'Cron last run' => (int)setting('last_cron', 0) > time() - 7200,
];
$h .= '<h2>Setup checklist</h2><ul class="checks">';
foreach ($checks as $l => $ok) $h .= '<li class="' . ($ok ? 'ok' : 'no') . '">' . ($ok ? '✔' : '✖') . ' ' . e($l) . '</li>';
$h .= '</ul>';
$fails = rows("SELECT * FROM email_log WHERE status = 'failed' ORDER BY id DESC LIMIT 5");
if ($fails) {
    $h .= '<h2>Recent email failures</h2><table class="tbl"><tr><th>When</th><th>To</th><th>Subject</th><th>Error</th></tr>';
    foreach ($fails as $f) $h .= '<tr><td>' . e($f['created_at']) . '</td><td>' . e($f['to_addr']) . '</td><td>' . e($f['subject']) . '</td><td class="small">' . e($f['error']) . '</td></tr>';
    $h .= '</table>';
}
admin_page('Dashboard', $h);
