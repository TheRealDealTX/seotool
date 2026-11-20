<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
$ms = rows('SELECT m.*, l.title FROM messages m LEFT JOIN listings l ON l.id = m.listing_id ORDER BY m.id DESC LIMIT 200');
ob_start(); ?>
<div class="table-scroll"><table class="tbl"><tr><th>When</th><th>Type</th><th>Listing</th><th>From</th><th>Message</th><th>Relayed</th></tr>
<?php foreach ($ms as $m): ?>
<tr><td class="small"><?= e($m['created_at']) ?></td><td><?= e($m['kind']) ?></td><td><?= $m['listing_id'] ? '<a href="/admin/listing/' . (int)$m['listing_id'] . '/">' . e($m['title'] ?? '#' . $m['listing_id']) . '</a>' : '—' ?></td>
<td class="small"><?= e($m['sender_name']) ?><br><?= e($m['sender_email']) ?><br><span class="muted"><?= e($m['ip']) ?></span></td><td class="small msg-cell"><?= nl2br(e($m['body'])) ?></td><td><?= $m['relayed'] ? '✔' : ($m['kind'] === 'contact' ? '—' : '✖') ?></td></tr>
<?php endforeach; ?></table></div>
<?php if (!$ms): ?><p class="muted">No messages yet.</p><?php endif; ?>
<?php
admin_page('Messages', ob_get_clean());
