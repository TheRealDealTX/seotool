<?php defined('WCA') || exit; ?>
<div class="wrap section-tight admin-page">
  <h1 class="h2">Owner accounts</h1>
  <form method="post" class="admin-filter card"><?= csrf_field() ?><input type="hidden" name="action" value="create">
    <input name="name" placeholder="Name" required><input type="email" name="email" placeholder="Email" required><button class="btn btn-sm">Create owner account (sends verification)</button>
  </form>
  <div class="table-scroll"><table class="table">
    <thead><tr><th>Name</th><th>Email</th><th>Verified</th><th>Listings</th><th>Created</th><th></th></tr></thead>
    <tbody><?php foreach ($users as $u): ?><tr>
      <td><?= e($u['name']) ?></td><td><?= e($u['email']) ?></td><td><?= $u['verified_at'] ? '✓ ' . e(time_ago($u['verified_at'])) : 'No' ?></td><td><?= (int)$u['listings'] ?></td><td><?= e(time_ago($u['created_at'])) ?></td>
      <td class="row-actions"><?php if (!$u['verified_at']): ?>
        <form method="post"><?= csrf_field() ?><input type="hidden" name="id" value="<?= (int)$u['id'] ?>"><button class="btn btn-ghost btn-sm" name="action" value="resend">Resend link</button><button class="btn btn-ghost btn-sm" name="action" value="verify">Mark verified</button></form>
      <?php endif; ?></td>
    </tr><?php endforeach; ?></tbody>
  </table></div>
</div>
