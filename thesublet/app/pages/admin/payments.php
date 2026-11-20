<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
$ps = rows('SELECT p.*, l.title FROM payments p LEFT JOIN listings l ON l.id = p.listing_id ORDER BY p.id DESC LIMIT 300');
ob_start(); ?>
<div class="table-scroll"><table class="tbl"><tr><th>#</th><th>Created</th><th>Listing</th><th>Kind</th><th>Email</th><th>Amount</th><th>Promo</th><th>Status</th><th>Stripe session</th></tr>
<?php foreach ($ps as $p): ?>
<tr><td><?= (int)$p['id'] ?></td><td class="small"><?= e($p['created_at']) ?></td><td><?= $p['listing_id'] ? '<a href="/admin/listing/' . (int)$p['listing_id'] . '/">' . e($p['title'] ?? '#' . $p['listing_id']) . '</a>' : '' ?></td>
<td><?= e($p['kind']) ?></td><td class="small"><?= e($p['email']) ?></td><td>$<?= number_format($p['amount_cents'] / 100, 2) ?></td><td class="small"><?= e($p['promo']) ?></td>
<td><span class="status status-<?= $p['status'] === 'complete' ? 'active' : 'pending' ?>"><?= e($p['status']) ?></span></td><td class="small mono"><?= e(substr($p['stripe_session_id'], 0, 24)) ?>…</td></tr>
<?php endforeach; ?></table></div>
<?php if (!$ps): ?><p class="muted">No payments yet.</p><?php endif; ?>
<?php
admin_page('Payments', ob_get_clean());
