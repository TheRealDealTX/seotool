<a class="backlink" href="/admin/users"><?= icon('back') ?> Members</a>
<div class="page-head">
  <div class="cell-user big"><?= avatar($u, 'lg') ?><div><h1><?= e($u['name']) ?></h1><p class="muted">@<?= e($u['username']) ?> · joined <?= e(date('M j, Y', strtotime($u['created_at']))) ?> · last seen <?= $u['last_seen'] ? e(time_ago($u['last_seen'])) : 'never' ?></p></div></div>
  <a class="btn btn-outline btn-sm" href="/u/<?= e($u['username']) ?>">View public profile</a>
</div>
<div class="stat-grid small-stats">
  <div class="stat card"><span>Status</span><strong class="<?= $u['status'] === 'active' ? 'ok' : 'danger' ?>"><?= e(ucfirst($u['status'])) ?></strong></div>
  <div class="stat card"><span>Friends</span><strong><?= $info['friends'] ?></strong></div>
  <div class="stat card"><span>Posts</span><strong><?= $info['posts'] ?></strong></div>
  <div class="stat card"><span>Messages sent</span><strong><?= $info['messages'] ?></strong></div>
  <div class="stat card"><span>Blocked by</span><strong><?= $info['blocked_by'] ?></strong></div>
</div>
<div class="layout-2 even">
  <section class="card form-section">
    <h2>Account</h2>
    <form method="post" class="form"><?= csrf_field() ?><input type="hidden" name="action" value="save">
      <label>Name<input type="text" name="name" value="<?= e($u['name']) ?>" required></label>
      <label>Email<input type="email" name="email" value="<?= e($u['email']) ?>" required></label>
      <label>Username<input type="text" name="username" value="<?= e($u['username']) ?>" required></label>
      <label>City<input type="text" name="city" value="<?= e($u['city']) ?>"></label>
      <label>Role<select name="role"><option value="user"<?= $u['role'] === 'user' ? ' selected' : '' ?>>Member</option><option value="admin"<?= $u['role'] === 'admin' ? ' selected' : '' ?>>Administrator</option></select></label>
      <label class="check"><input type="checkbox" name="is_verified" value="1"<?= $u['is_verified'] ? ' checked' : '' ?>> Verified member (shows a check badge)</label>
      <button class="btn btn-primary btn-sm">Save changes</button>
    </form>
  </section>
  <div>
    <section class="card form-section">
      <h2>Moderation</h2>
      <div class="btn-row">
      <?php if ($u['status'] === 'active'): ?>
        <form method="post" data-confirm="Suspend this member? They will be logged out and hidden."><?= csrf_field() ?><input type="hidden" name="action" value="suspend"><button class="btn btn-outline btn-sm"><?= icon('ban') ?> Suspend</button></form>
      <?php else: ?>
        <form method="post"><?= csrf_field() ?><input type="hidden" name="action" value="activate"><button class="btn btn-primary btn-sm">Reactivate</button></form>
      <?php endif; ?>
        <form method="post" data-confirm="Permanently delete this member and all their content?"><?= csrf_field() ?><input type="hidden" name="action" value="delete"><button class="btn btn-danger btn-sm"><?= icon('trash') ?> Delete</button></form>
      </div>
      <form method="post" class="form" style="margin-top:16px"><?= csrf_field() ?><input type="hidden" name="action" value="password">
        <label>Set a new password<input type="text" name="new_password" minlength="8" autocomplete="off" placeholder="At least 8 characters"></label>
        <button class="btn btn-outline btn-sm">Set password</button>
      </form>
    </section>
    <section class="card">
      <h3 class="card-title">Preferred properties</h3>
      <?php if (!$props): ?><p class="muted small">None.</p><?php endif; ?>
      <ul class="side-list"><?php foreach ($props as $p): ?><li><a href="/properties/<?= e($p['slug']) ?>"><?= icon('building') ?><?= e($p['name']) ?></a></li><?php endforeach; ?></ul>
    </section>
    <section class="card">
      <h3 class="card-title">Reports about this member</h3>
      <?php if (!$reports): ?><p class="muted small">No reports.</p><?php endif; ?>
      <ul class="report-mini"><?php foreach ($reports as $r): ?><li><span class="tag"><?= e($r['status']) ?></span> <?= e($r['reason']) ?> <small class="muted">— @<?= e($r['reporter'] ?? 'deleted') ?>, <?= e(time_ago($r['created_at'])) ?></small></li><?php endforeach; ?></ul>
    </section>
  </div>
</div>
