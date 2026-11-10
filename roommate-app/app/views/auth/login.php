<div class="auth-card card">
  <h1>Welcome back</h1>
  <p class="muted">Log in to see your matches and messages.</p>
  <?php if ($error): ?><div class="alert alert-error"><?= e($error) ?></div><?php endif; ?>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <label>Email or username<input type="text" name="email" value="<?= e(old('email')) ?>" required autocomplete="username" autofocus></label>
    <label>Password<input type="password" name="password" required autocomplete="current-password"></label>
    <button class="btn btn-primary btn-block" type="submit">Log in</button>
  </form>
  <p class="auth-alt"><a href="/forgot">Forgot your password?</a></p>
  <p class="auth-alt">New here? <a href="/register">Create a free account</a></p>
</div>
