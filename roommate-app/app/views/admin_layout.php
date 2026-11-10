<?php
$me = current_user();
$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
$on = fn($p, $exact = false) => ($exact ? $path === $p : ($path === $p || str_starts_with($path, $p . '/'))) ? ' class="active"' : '';
$openReports = (int)val("SELECT COUNT(*) FROM reports WHERE status = 'open'");
$pendingProps = (int)val("SELECT COUNT(*) FROM properties WHERE status = 'pending'");
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e(($title ?? 'Admin') . ' · ' . setting('site_name') . ' Admin') ?></title>
<meta name="robots" content="noindex">
<meta name="csrf" content="<?= e(csrf_token()) ?>">
<link rel="icon" href="/assets/icon.svg?v=<?= @filemtime(APP_ROOT . '/assets/icon.svg') ?>" type="image/svg+xml">
<link rel="stylesheet" href="/assets/app.css?v=<?= @filemtime(APP_ROOT . '/assets/app.css') ?>">
</head>
<body class="admin">
<div class="admin-shell">
  <aside class="admin-nav">
    <a class="brand" href="/admin"><img src="/assets/icon.svg?v=<?= @filemtime(APP_ROOT . '/assets/icon.svg') ?>" alt="" width="28" height="28"><span>Admin</span></a>
    <nav>
      <a href="/admin"<?= $on('/admin', true) ?>><?= icon('chart') ?> Dashboard</a>
      <a href="/admin/users"<?= $on('/admin/users') ?>><?= icon('users') ?> Members</a>
      <a href="/admin/properties"<?= $on('/admin/properties') ?>><?= icon('building') ?> Properties<?php if ($pendingProps): ?><span class="badge"><?= $pendingProps ?></span><?php endif; ?></a>
      <a href="/admin/reports"<?= $on('/admin/reports') ?>><?= icon('flag') ?> Reports<?php if ($openReports): ?><span class="badge"><?= $openReports ?></span><?php endif; ?></a>
      <a href="/admin/posts"<?= $on('/admin/posts') ?>><?= icon('comment') ?> Posts</a>
      <a href="/admin/sync"<?= $on('/admin/sync') ?>><?= icon('link') ?> Sync listings</a>
      <a href="/admin/settings"<?= $on('/admin/settings') ?>><?= icon('gear') ?> Settings</a>
      <a href="/admin/audit"<?= $on('/admin/audit') ?>><?= icon('shield') ?> Audit log</a>
    </nav>
    <div class="admin-nav-foot">
      <a href="/home"><?= icon('back') ?> Back to app</a>
      <small class="muted">Signed in as @<?= e($me['username']) ?></small>
    </div>
  </aside>
  <main class="admin-main">
    <?php foreach (take_flashes() as [$t, $m]): ?><div class="flash flash-<?= e($t) ?>" role="status"><?= e($m) ?><button type="button" class="flash-x" aria-label="Dismiss">×</button></div><?php endforeach; ?>
    <?= $content ?>
  </main>
</div>
<script src="/assets/app.js?v=<?= @filemtime(APP_ROOT . '/assets/app.js') ?>" defer></script>
</body>
</html>
