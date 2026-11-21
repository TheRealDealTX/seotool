<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
if (is_post()) {
    admin_guard_post();
    $c = row('SELECT * FROM claims WHERE id = ?', [(int)post('id')]);
    if ($c) {
        if (post('do') === 'approve') {
            approve_claim($c, false);
            flash('Claim approved — the owner has been emailed a sign-in link.');
        } elseif (post('do') === 'reject') {
            update('claims', ['status' => 'rejected', 'decided_at' => now()], 'id = ?', [(int)$c['id']]);
            $l = listing_get((int)$c['listing_id']);
            if ($l) send_mail($c['email'], 'About your claim on The Sublet', '<p>Hi ' . e($c['name']) . ',</p><p>We couldn’t verify your claim for <strong>' . e($l['title']) . '</strong>.' . (post('reason') ? ' Reason: ' . e(post('reason')) : '') . '</p><p>Reply to this email with proof of your connection to the property (for example, from an email address at the property’s website domain) and we’ll take another look.</p>');
            flash('Claim rejected.');
        }
    }
    redirect('/admin/claims/');
}
$show = get('all') === '1' ? '1=1' : "c.status IN ('pending','pending_payment')";
$cs = rows("SELECT c.*, l.title, l.website, l.city, l.state FROM claims c LEFT JOIN listings l ON l.id = c.listing_id WHERE $show ORDER BY c.id DESC LIMIT 200");
ob_start(); ?>
<p><a href="?all=1">Show decided claims too</a></p>
<div class="table-scroll"><table class="tbl"><tr><th>When</th><th>Listing</th><th>Claimant</th><th>Role / note</th><th>Check</th><th>Status</th><th></th></tr>
<?php foreach ($cs as $c): ?>
<tr>
  <td class="small"><?= e($c['created_at']) ?></td>
  <td><a href="/admin/listing/<?= (int)$c['listing_id'] ?>/"><?= e($c['title'] ?? '#' . $c['listing_id']) ?></a><br><span class="small muted"><?= e(($c['city'] ?? '') . ', ' . ($c['state'] ?? '')) ?> · <?= e(preg_replace('#^https?://(www\.)?([^/]+).*$#', '$2', (string)$c['website'])) ?></span></td>
  <td class="small"><?= e($c['name']) ?><br><?= e($c['email']) ?><br><?= e($c['phone']) ?></td>
  <td class="small msg-cell"><?= e($c['role']) ?><br><?= nl2br(e((string)$c['message'])) ?></td>
  <td><?= $c['domain_match'] ? '<span class="status status-active">✔ email matches website</span>' : '<span class="status">no domain match</span>' ?></td>
  <td><span class="status status-<?= $c['status'] === 'approved' ? 'active' : ($c['status'] === 'rejected' ? 'rejected' : 'pending') ?>"><?= e($c['status']) ?></span></td>
  <td><?php if (in_array($c['status'], ['pending', 'pending_payment'], true)): ?>
    <form method="post" class="inline"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$c['id'] ?>">
      <button class="btn btn-sm" name="do" value="approve" data-confirm="Approve this claim and give the claimant control of the listing?">Approve</button>
      <input name="reason" placeholder="Reason (optional)" style="width:140px">
      <button class="btn btn-sm btn-ghost" name="do" value="reject">Reject</button>
    </form><?php endif; ?></td>
</tr>
<?php endforeach; ?></table></div>
<?php if (!$cs): ?><p class="muted">No pending claims.</p><?php endif; ?>
<?php
admin_page('Claims', ob_get_clean());
