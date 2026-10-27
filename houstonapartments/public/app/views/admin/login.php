<?php defined('HA_ROOT') || exit; ?><!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Sign in · Houston Apartments Admin</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="<?= asset('css/admin.css') ?>"></head>
<body class="login-body">
<form class="login-card" method="post">
  <div class="login-logo"><?php require HA_APP . '/views/partials/logo.php'; ?></div>
  <h1>Admin sign in</h1>
  <?php if ($error): ?><p class="flash err"><?= e($error) ?></p><?php endif ?>
  <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
  <label>Email<input name="email" type="email" required autofocus autocomplete="username"></label>
  <label>Password<input name="password" type="password" required autocomplete="current-password"></label>
  <button class="btn primary big" type="submit">Sign in</button>
  <p class="muted">Forgot your password? Ask an admin to reset it on the Users page.</p>
</form>
</body></html>
