<?php defined('WCA') || exit; ?>
<div class="wrap narrow section">
  <div class="card auth-card">
    <h1 class="h2">Admin sign in</h1>
    <?php if ($error): ?><div class="alert alert-error"><?= e($error) ?></div><?php endif; ?>
    <form method="post" class="form">
      <?= csrf_field() ?>
      <label>Username<input name="username" required autocomplete="username" autofocus></label>
      <label>Password<input type="password" name="password" required autocomplete="current-password"></label>
      <button class="btn btn-block" type="submit">Sign in</button>
    </form>
  </div>
</div>
