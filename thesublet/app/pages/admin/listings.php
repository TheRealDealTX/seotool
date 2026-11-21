<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
if (is_post()) {
    admin_guard_post();
    $ids = array_map('intval', (array)($_POST['ids'] ?? []));
    $do = post('bulk');
    foreach ($ids as $id) admin_listing_action($id, $do, '');
    flash(count($ids) . ' listing(s) updated.');
    redirect($_SERVER['REQUEST_URI']);
}
$w = ['1=1']; $p = [];
$status = get('status'); $tier = get('tier'); $qq = get('q'); $src = get('source');
if (in_array($src, ['host', 'directory'], true)) { $w[] = 'source = ?'; $p[] = $src; }
if ($status !== '') { $w[] = 'status = ?'; $p[] = $status; }
if ($tier !== '') { $w[] = 'tier = ?'; $p[] = $tier; }
if ($qq !== '') { $w[] = '(title LIKE ? OR contact_email LIKE ? OR city LIKE ? OR CAST(id AS CHAR) = ?)'; array_push($p, "%$qq%", "%$qq%", "%$qq%", $qq); }
$where = implode(' AND ', $w);
$pg = paginate((int)val("SELECT COUNT(*) FROM listings WHERE $where", $p), 50, (int)get('page', '1'));
$ls = rows("SELECT * FROM listings WHERE $where ORDER BY CASE WHEN status = 'pending' THEN 0 ELSE 1 END, id DESC LIMIT 50 OFFSET " . $pg['offset'], $p);
$statuses = ['', 'pending', 'pending_payment', 'active', 'rented', 'unavailable', 'expired', 'rejected'];
ob_start(); ?>
<form class="admin-filter" method="get">
  <input type="search" name="q" value="<?= e($qq) ?>" placeholder="Search title, email, city, #id">
  <select name="status"><?php foreach ($statuses as $s): ?><option value="<?= e($s) ?>"<?= $s === $status ? ' selected' : '' ?>><?= $s ? e(listing_status_label($s)) : 'Any status' ?></option><?php endforeach; ?></select>
  <select name="tier"><option value="">Any tier</option><option value="free"<?= $tier === 'free' ? ' selected' : '' ?>>Free</option><option value="paid"<?= $tier === 'paid' ? ' selected' : '' ?>>Paid</option></select>
  <select name="source"><option value="">Any source</option><option value="host"<?= $src === 'host' ? ' selected' : '' ?>>Host-posted</option><option value="directory"<?= $src === 'directory' ? ' selected' : '' ?>>Directory (claimable)</option></select>
  <button class="btn btn-sm">Filter</button>
</form>
<p class="muted"><?= (int)$pg['total'] ?> listing(s)</p>
<form method="post"><?= csrf_field() ?>
<div class="table-scroll"><table class="tbl">
<tr><th><input type="checkbox" data-checkall></th><th>#</th><th>Title</th><th>Location</th><th>Rent</th><th>Tier</th><th>Status</th><th>Contact</th><th>Created</th><th></th></tr>
<?php foreach ($ls as $l): ?>
<tr>
  <td><input type="checkbox" name="ids[]" value="<?= (int)$l['id'] ?>"></td>
  <td><?= (int)$l['id'] ?></td>
  <td><a href="/admin/listing/<?= (int)$l['id'] ?>/"><?= e($l['title']) ?></a></td>
  <td><?= e($l['city'] . ', ' . $l['state']) ?></td>
  <td><?= money($l['rent']) ?></td>
  <td><?= $l['tier'] === 'paid' ? '✔ paid' : 'free' ?></td>
  <td><span class="status status-<?= e($l['status']) ?>"><?= e(listing_status_label($l['status'])) ?></span></td>
  <td class="small"><?= e($l['contact_email']) ?></td>
  <td class="small"><?= e(substr($l['created_at'], 0, 10)) ?></td>
  <td><a class="small" href="<?= e(listing_url($l)) ?>" target="_blank">view</a></td>
</tr>
<?php endforeach; ?>
</table></div>
<p>With selected: <select name="bulk"><option value="approve">Approve &amp; publish</option><option value="reject">Reject</option><option value="expire">Expire</option><option value="delete">Delete</option></select> <button class="btn btn-sm" data-confirm="Apply to selected listings?">Apply</button></p>
</form>
<?php if ($pg['pages'] > 1): ?><nav class="pager"><?php for ($i = 1; $i <= $pg['pages']; $i++): ?><a href="?<?= e(http_build_query(['status' => $status, 'tier' => $tier, 'q' => $qq, 'source' => $src, 'page' => $i])) ?>"<?= $i === $pg['page'] ? ' class="is-on"' : '' ?>><?= $i ?></a><?php endfor; ?></nav><?php endif; ?>
<?php
admin_page($status === 'pending' ? 'Review queue' : 'Listings', ob_get_clean());
