<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
if (is_post()) {
    admin_guard_post();
    $r = row('SELECT * FROM reports WHERE id = ?', [(int)post('id')]);
    if ($r) {
        if (post('do') === 'takedown') admin_listing_action((int)$r['listing_id'], 'expire', '');
        update('reports', ['resolved' => 1], 'id = ?', [(int)$r['id']]);
    }
    flash('Report resolved.');
    redirect('/admin/reports/');
}
$show = get('all') === '1' ? '1=1' : 'r.resolved = 0';
$rs = rows("SELECT r.*, l.title, l.status FROM reports r LEFT JOIN listings l ON l.id = r.listing_id WHERE $show ORDER BY r.id DESC LIMIT 200");
ob_start(); ?>
<p><a href="?all=1">Show resolved too</a></p>
<div class="table-scroll"><table class="tbl"><tr><th>When</th><th>Listing</th><th>Reason</th><th>Details</th><th>Reporter</th><th></th></tr>
<?php foreach ($rs as $r): ?>
<tr><td class="small"><?= e($r['created_at']) ?></td><td><a href="/admin/listing/<?= (int)$r['listing_id'] ?>/"><?= e($r['title'] ?? '#' . $r['listing_id']) ?></a><br><span class="small"><?= e(listing_status_label($r['status'] ?? '')) ?></span></td>
<td><?= e($r['reason']) ?></td><td class="small msg-cell"><?= nl2br(e($r['details'])) ?></td><td class="small"><?= e($r['reporter_email']) ?><br><?= e($r['ip']) ?></td>
<td><?php if (!$r['resolved']): ?><form method="post" class="inline"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$r['id'] ?>"><button class="btn btn-sm btn-danger" name="do" value="takedown">Take down</button> <button class="btn btn-sm btn-ghost" name="do" value="dismiss">Dismiss</button></form><?php else: ?>resolved<?php endif; ?></td></tr>
<?php endforeach; ?></table></div>
<?php if (!$rs): ?><p class="muted">No open reports. 🎉</p><?php endif; ?>
<?php
admin_page('Reports', ob_get_clean());
