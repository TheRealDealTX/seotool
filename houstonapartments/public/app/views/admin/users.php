<?php
defined('HA_ROOT') || exit;
$title = 'Users';
?>
<div class="grid-2">
  <section class="card table-card">
    <table class="table">
      <thead><tr><th>Name</th><th>Email</th><th>Role</th><th>Last sign-in</th><th></th></tr></thead>
      <tbody>
      <?php foreach ($rows as $u): ?>
        <tr>
          <td><?= e($u['name']) ?></td><td><?= e($u['email']) ?></td><td><?= $u['role'] === 'admin' ? 'Admin' : 'Editor' ?></td>
          <td><small><?= $u['last_login'] ? e(date('M j, Y', strtotime($u['last_login']))) : 'Never' ?></small></td>
          <td class="nowrap">
            <details class="inline-menu"><summary class="btn small">Reset password</summary>
              <form method="post" action="/admin/users/<?= $u['id'] ?>/password/"><input type="hidden" name="_csrf" value="<?= e($csrf) ?>"><input name="password" type="text" minlength="10" placeholder="New password (10+ chars)" required><button class="btn small primary">Save</button></form>
            </details>
            <?php if ((int) $u['id'] !== (int) $user['id']): ?>
            <form method="post" action="/admin/users/<?= $u['id'] ?>/delete/" class="inline" onsubmit="return confirm('Remove <?= e($u['email']) ?>?')"><input type="hidden" name="_csrf" value="<?= e($csrf) ?>"><button class="btn small danger">Remove</button></form>
            <?php endif ?>
          </td>
        </tr>
      <?php endforeach ?>
      </tbody>
    </table>
  </section>
  <form class="card" method="post">
    <h2>Add a team member</h2>
    <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
    <label class="block">Name<input name="name" required></label>
    <label class="block">Email<input name="email" type="email" required></label>
    <label class="block">Password <small>(at least 10 characters – share it privately)</small><input name="password" type="text" minlength="10" required></label>
    <label class="block">Role<select name="role"><option value="editor">Editor – listings &amp; leads</option><option value="admin">Admin – also manages users</option></select></label>
    <button class="btn primary" type="submit">Add user</button>
  </form>
</div>
