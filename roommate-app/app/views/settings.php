<div class="narrow">
  <h1>Settings</h1>
  <section class="card form-section">
    <h2>Privacy &amp; notifications</h2>
    <form method="post" class="form"><?= csrf_field() ?><input type="hidden" name="action" value="privacy">
      <label class="switch"><input type="checkbox" name="profile_visible" value="1"<?= $u['profile_visible'] ? ' checked' : '' ?>><span></span> Show my profile in Discover and to non-friends</label>
      <label class="switch"><input type="checkbox" name="email_notifications" value="1"<?= $u['email_notifications'] ? ' checked' : '' ?>><span></span> Email me about important account activity</label>
      <button class="btn btn-primary btn-sm" type="submit">Save</button>
    </form>
  </section>
  <section class="card form-section">
    <h2>Email address</h2>
    <form method="post" class="form"><?= csrf_field() ?><input type="hidden" name="action" value="email">
      <label>Email<input type="email" name="email" value="<?= e($u['email']) ?>" required></label>
      <label>Current password<input type="password" name="password" required autocomplete="current-password"></label>
      <button class="btn btn-primary btn-sm" type="submit">Update email</button>
    </form>
  </section>
  <section class="card form-section">
    <h2>Change password</h2>
    <form method="post" class="form"><?= csrf_field() ?><input type="hidden" name="action" value="password">
      <label>Current password<input type="password" name="current" required autocomplete="current-password"></label>
      <label>New password<input type="password" name="new" required minlength="8" autocomplete="new-password"></label>
      <button class="btn btn-primary btn-sm" type="submit">Change password</button>
    </form>
  </section>
  <section class="card form-section">
    <h2>Blocked members</h2>
    <?php if (!$blocked): ?><p class="muted small">You haven't blocked anyone.</p><?php endif; ?>
    <ul class="people-list">
      <?php foreach ($blocked as $b): ?>
      <li><?= avatar($b, 'sm') ?><span class="grow"><?= e($b['name']) ?> <small class="muted">@<?= e($b['username']) ?></small></span>
        <div class="pl-actions"><form method="post" action="/unblock/<?= (int)$b['id'] ?>"><?= csrf_field() ?><button class="btn btn-outline btn-sm" type="submit">Unblock</button></form></div></li>
      <?php endforeach; ?>
    </ul>
  </section>
  <section class="card form-section danger-zone">
    <h2>Delete account</h2>
    <p class="muted small">This permanently deletes your profile, posts, comments, friends and messages. It can't be undone.</p>
    <form method="post" class="form" data-confirm="Permanently delete your account?"><?= csrf_field() ?><input type="hidden" name="action" value="delete">
      <label>Confirm with your password<input type="password" name="password" required autocomplete="current-password"></label>
      <button class="btn btn-danger btn-sm" type="submit">Delete my account</button>
    </form>
  </section>
</div>
