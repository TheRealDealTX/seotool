<div class="auth-card card">
  <h1>Reset your password</h1>
  <?php if ($sent): ?>
    <div class="alert alert-success">If an account exists for that email, we've sent a reset link. Check your inbox (and spam folder).</div>
    <p class="auth-alt"><a href="/login">Back to log in</a></p>
  <?php else: ?>
  <p class="muted">Enter your account email and we'll send you a link to choose a new password.</p>
  <form method="post" class="form">
    <?= csrf_field() ?>
    <label>Email<input type="email" name="email" required autofocus></label>
    <button class="btn btn-primary btn-block" type="submit">Send reset link</button>
  </form>
  <p class="auth-alt"><a href="/login">Back to log in</a></p>
  <?php endif; ?>
</div>
