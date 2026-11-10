<div class="page-head"><h1>Members <small class="muted"><?= number_format($total) ?></small></h1>
<div class="btn-row">
  <?php if ($demoCount): ?><form method="post" data-confirm="Delete all <?= $demoCount ?> demo accounts and their posts?"><?= csrf_field() ?><input type="hidden" name="bulk" value="delete_demo"><button class="btn btn-outline btn-sm danger">Delete <?= $demoCount ?> demo accounts</button></form><?php endif; ?>
  <a class="btn btn-outline btn-sm" href="?<?= e(http_build_query(array_merge($_GET, ['export' => 'csv']))) ?>">Export CSV</a></div></div>
<form class="card filters" method="get">
  <div class="filters-grid">
    <label>Search<input type="search" name="q" value="<?= e($s) ?>" placeholder="Name, email, username, city"></label>
    <label>Role<select name="role"><option value="">All</option><option value="user"<?= $role === 'user' ? ' selected' : '' ?>>Members</option><option value="admin"<?= $role === 'admin' ? ' selected' : '' ?>>Admins</option><option value="demo"<?= $role === 'demo' ? ' selected' : '' ?>>Demo accounts</option></select></label>
    <label>Status<select name="status"><option value="">All</option><option value="active"<?= $status === 'active' ? ' selected' : '' ?>>Active</option><option value="suspended"<?= $status === 'suspended' ? ' selected' : '' ?>>Suspended</option></select></label>
  </div>
  <div class="filters-foot"><span class="spacer"></span><button class="btn btn-primary btn-sm">Filter</button></div>
</form>
<form method="post" class="card table-card">
  <?= csrf_field() ?>
  <div class="table-tools">
    <select name="bulk" class="select-sm"><option value="">Bulk action…</option><option value="verify">Mark verified</option><option value="suspend">Suspend</option><option value="activate">Reactivate</option></select>
    <button class="btn btn-outline btn-sm" type="submit">Apply</button>
  </div>
  <div class="table-wrap"><table class="table">
    <thead><tr><th><input type="checkbox" class="js-check-all"></th><th>Member</th><th>Email</th><th>City</th><th>Status</th><th>Reports</th><th>Joined</th><th>Last seen</th></tr></thead>
    <tbody>
    <?php foreach ($users as $u): ?>
    <tr>
      <td><input type="checkbox" name="ids[]" value="<?= (int)$u['id'] ?>"></td>
      <td><a class="cell-user" href="/admin/users/<?= (int)$u['id'] ?>"><?= avatar($u, 'xs') ?> <span><?= e($u['name']) ?> <small class="muted">@<?= e($u['username']) ?></small></span></a>
        <?php if ($u['is_demo']): ?><span class="tag tag-warn">Demo</span><?php endif; ?><?php if ($u['role'] === 'admin'): ?><span class="tag tag-feature">Admin</span><?php endif; ?><?php if ($u['is_verified']): ?><span class="tag tag-ok">Verified</span><?php endif; ?></td>
      <td class="small"><?= e($u['email']) ?></td>
      <td class="small"><?= e($u['city']) ?></td>
      <td><span class="tag <?= $u['status'] === 'active' ? 'tag-ok' : 'tag-danger' ?>"><?= e($u['status']) ?></span></td>
      <td class="num"><?= (int)$u['report_count'] ?: '' ?></td>
      <td class="small muted"><?= e(date('M j, Y', strtotime($u['created_at']))) ?></td>
      <td class="small muted"><?= $u['last_seen'] ? e(time_ago($u['last_seen'])) : '—' ?></td>
    </tr>
    <?php endforeach; ?>
    </tbody>
  </table></div>
</form>
<?php partial('partials/pager', ['page' => $page, 'pages' => $pages]); ?>
