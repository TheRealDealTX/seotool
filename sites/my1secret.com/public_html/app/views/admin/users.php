<?php defined('M1S') || exit; ?>
<h1>Users</h1>
<?= view('admin/_nav') ?>
<form method="get" class="search-big"><input type="search" name="q" value="<?= e($qText) ?>" placeholder="Search username or email" aria-label="Search users"><button class="btn btn-accent">Search</button></form>
<table class="table"><thead><tr><th>User</th><th>Email</th><th>Karma</th><th>Joined</th><th>Role</th><th>Status</th></tr></thead><tbody>
<?php foreach ($users as $u): ?>
  <tr>
    <td><a href="<?= e(user_url($u)) ?>"><?= e($u['username']) ?></a></td>
    <td class="small"><?= e((string)$u['email']) ?></td>
    <td><?= (int)$u['karma'] ?></td>
    <td class="small"><?= e(substr($u['created_at'], 0, 10)) ?></td>
    <td><?php if (is_admin()): ?>
      <form method="post" action="/admin/users/" class="inline"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$u['id'] ?>"><input type="hidden" name="action" value="role"><input type="hidden" name="q" value="<?= e($qText) ?>">
        <select name="role" aria-label="Role" data-autosubmit><?php foreach (['member', 'mod', 'admin'] as $r): ?><option<?= $u['role'] === $r ? ' selected' : '' ?>><?= $r ?></option><?php endforeach; ?></select></form>
      <?php else: ?><?= e($u['role']) ?><?php endif; ?></td>
    <td>
      <form method="post" action="/admin/users/" class="inline"<?= $u['banned'] ? '' : ' data-confirm="Ban ' . e($u['username']) . '?"' ?>><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$u['id'] ?>"><input type="hidden" name="q" value="<?= e($qText) ?>">
        <?php if ($u['banned']): ?><input type="hidden" name="action" value="unban"><button class="btn btn-ghost btn-sm">Unban</button>
        <?php else: ?><input type="hidden" name="action" value="ban"><label class="small"><input type="checkbox" name="purge" value="1"> remove content</label> <button class="btn btn-ghost btn-sm danger">Ban</button><?php endif; ?>
      </form>
    </td>
  </tr>
<?php endforeach; ?>
</tbody></table>

<h2 class="block">Guest contributors</h2>
<p class="muted">People who posted with a name and email instead of an account. Banning an email removes everything it posted and blocks it from posting again.</p>
<table class="table"><thead><tr><th>Name</th><th>Email</th><th>Contributions</th><th>Confirmed</th><th></th></tr></thead><tbody>
<?php foreach ($guests as $g): ?>
  <tr><td><?= e($g['name']) ?></td><td class="small"><?= e($g['email']) ?></td><td><?= (int)$g['posts'] ?></td><td class="small"><?= $g['verified_at'] ? e(substr($g['verified_at'], 0, 10)) : 'no' ?></td>
  <td><form method="post" action="/admin/users/" class="inline"<?= $g['banned'] ? '' : ' data-confirm="Ban ' . e($g['email']) . ' and remove their posts?"' ?>><?= csrf_field() ?><input type="hidden" name="email" value="<?= e($g['email']) ?>"><input type="hidden" name="action" value="<?= $g['banned'] ? 'guest_unban' : 'guest_ban' ?>"><button class="btn btn-ghost btn-sm<?= $g['banned'] ? '' : ' danger' ?>"><?= $g['banned'] ? 'Unban' : 'Ban' ?></button></form></td></tr>
<?php endforeach; ?>
<?php if (!$guests): ?><tr><td colspan="5" class="muted">No guest contributors yet.</td></tr><?php endif; ?>
</tbody></table>
