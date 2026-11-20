<?php defined('APP') || exit;

require_admin();
require __DIR__ . '/_layout.php';
if (is_post()) {
    admin_guard_post();
    $id = (int)post('id');
    switch (post('do')) {
        case 'suspend': update('owners', ['status' => 'suspended'], 'id = ?', [$id]); q("UPDATE listings SET status = 'unavailable' WHERE owner_id = ? AND status = 'active'", [$id]); break;
        case 'activate': update('owners', ['status' => 'active'], 'id = ?', [$id]); break;
        case 'link':
            $o = row('SELECT * FROM owners WHERE id = ?', [$id]);
            if ($o) { send_mail($o['email'], 'Your sign-in link for The Sublet', view('emails/login', ['link' => magic_link_create($id)])); }
            break;
    }
    flash('Updated.');
    redirect('/admin/owners/');
}
$qq = get('q');
$os = $qq !== '' ? rows('SELECT * FROM owners WHERE email LIKE ? OR name LIKE ? ORDER BY id DESC LIMIT 200', ["%$qq%", "%$qq%"]) : rows('SELECT * FROM owners ORDER BY id DESC LIMIT 200');
$counts = [];
foreach (rows('SELECT owner_id, COUNT(*) n FROM listings WHERE owner_id IS NOT NULL GROUP BY owner_id') as $r) $counts[(int)$r['owner_id']] = (int)$r['n'];
ob_start(); ?>
<form class="admin-filter" method="get"><input type="search" name="q" value="<?= e($qq) ?>" placeholder="Search name or email"><button class="btn btn-sm">Search</button></form>
<div class="table-scroll"><table class="tbl"><tr><th>#</th><th>Name</th><th>Email</th><th>Verified</th><th>Listings</th><th>Status</th><th>Last login</th><th></th></tr>
<?php foreach ($os as $o): ?>
<tr><td><?= (int)$o['id'] ?></td><td><?= e($o['name']) ?></td><td><?= e($o['email']) ?></td><td><?= $o['email_verified_at'] ? '✔' : '—' ?></td>
<td><a href="/admin/listings/?q=<?= e(rawurlencode($o['email'])) ?>"><?= $counts[(int)$o['id']] ?? 0 ?></a></td><td><?= e($o['status']) ?></td><td class="small"><?= e($o['last_login_at'] ?? '') ?></td>
<td><form method="post" class="inline"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$o['id'] ?>">
<button class="btn btn-sm btn-ghost" name="do" value="link">Email sign-in link</button>
<?= $o['status'] === 'active' ? '<button class="btn btn-sm btn-danger" name="do" value="suspend" data-confirm="Suspend this owner and hide their listings?">Suspend</button>' : '<button class="btn btn-sm" name="do" value="activate">Re-activate</button>' ?></form></td></tr>
<?php endforeach; ?></table></div>
<?php
admin_page('Owners', ob_get_clean());
