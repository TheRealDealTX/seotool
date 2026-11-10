<div class="auth-card card">
  <h1>Choose a new password</h1>
  <?php if (!$valid): ?>
    <div class="alert alert-error">This reset link is invalid or has expired.</div>
    <p class="auth-alt"><a href="/forgot">Request a new link</a></p>
  <?php else: ?>
  <?php if ($error): ?><div class="alert alert-error"><?= e($error) ?></div><?php endif; ?>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <input type="hidden" name="token" value="<?= e($token) ?>">
    <label>New password<input type="password" name="password" required minlength="8" autocomplete="new-password" autofocus></label>
    <button class="btn btn-primary btn-block" type="submit">Save password</button>
  </form>
  <?php endif; ?>
</div>
