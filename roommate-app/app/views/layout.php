<?php
$me = current_user();
$site = setting('site_name', 'Rise Roommates');
$counts = $me ? unread_counts((int)$me['id']) : ['messages' => 0, 'notifications' => 0, 'requests' => 0];
$path = parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH);
$active = fn($p) => ($path === $p || str_starts_with($path, $p . '/')) ? ' class="active"' : '';
$announcement = setting('announcement', '');
$badge = fn($n) => $n > 0 ? '<span class="badge">' . ($n > 99 ? '99+' : $n) . '</span>' : '<span class="badge" hidden></span>';
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title><?= e(isset($title) ? $title . ' · ' . $site : $site . ' — ' . setting('tagline', '')) ?></title>
<meta name="description" content="<?= e($description ?? 'Find a compatible roommate at the apartment you love. Match with renters interested in the same property, add friends and message them.') ?>">
<meta name="theme-color" content="#1d4463">
<meta name="csrf" content="<?= e(csrf_token()) ?>">
<link rel="icon" href="/assets/icon.svg?v=<?= @filemtime(APP_ROOT . '/assets/icon.svg') ?>" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/icon-192.png?v=<?= @filemtime(APP_ROOT . '/assets/icon-192.png') ?>">
<link rel="stylesheet" href="/assets/app.css?v=<?= @filemtime(APP_ROOT . '/assets/app.css') ?>">
<?php if (!empty($noindex) || $me): ?><meta name="robots" content="noindex"><?php endif; ?>
</head>
<body class="<?= $me ? 'authed' : 'guest' ?> <?= e($bodyClass ?? '') ?>">
<header class="topbar">
  <div class="topbar-inner">
    <a class="brand" href="<?= $me ? '/home' : '/' ?>">
      <img src="/assets/icon.svg?v=<?= @filemtime(APP_ROOT . '/assets/icon.svg') ?>" alt="" width="40" height="40"><span class="brand-text"><span><?= e($site) ?></span><small>by Rise Apartments</small></span>
    </a>
    <?php if ($me): ?>
    <nav class="mainnav" aria-label="Main">
      <a href="/home"<?= $active('/home') ?>><?= icon('home') ?><span>Feed</span></a>
      <a href="/discover"<?= $active('/discover') ?>><?= icon('search') ?><span>Discover</span></a>
      <a href="/properties"<?= $active('/properties') ?>><?= icon('building') ?><span>Properties</span></a>
      <a href="/friends"<?= $active('/friends') ?>><?= icon('users') ?><span>Friends</span><?= $badge($counts['requests']) ?></a>
      <a href="/messages"<?= $active('/messages') ?> data-count="messages"><?= icon('chat') ?><span>Messages</span><?= $badge($counts['messages']) ?></a>
    </nav>
    <div class="topbar-right">
      <a class="iconbtn" href="/notifications" data-count="notifications" aria-label="Notifications"><?= icon('bell') ?><?= $badge($counts['notifications']) ?></a>
      <details class="menu">
        <summary aria-label="Account menu"><?= avatar($me, 'sm') ?></summary>
        <div class="menu-pop">
          <div class="menu-head"><strong><?= e($me['name']) ?></strong><small>@<?= e($me['username']) ?></small></div>
          <a href="/u/<?= e($me['username']) ?>"><?= icon('user') ?> My profile</a>
          <a href="/profile/edit"><?= icon('edit') ?> Edit profile</a>
          <a href="/settings"><?= icon('gear') ?> Settings</a>
          <?php if ($me['role'] === 'admin'): ?><a href="/admin"><?= icon('shield') ?> Admin panel</a><?php endif; ?>
          <a href="/safety"><?= icon('info') ?> Safety tips</a>
          <form method="post" action="/logout"><?= csrf_field() ?><button type="submit"><?= icon('logout') ?> Log out</button></form>
        </div>
      </details>
    </div>
    <?php else: ?>
    <div class="topbar-right">
      <a class="btn btn-ghost" href="/login">Log in</a>
      <a class="btn btn-primary" href="/register">Join free</a>
    </div>
    <?php endif; ?>
  </div>
</header>
<?php if ($announcement): ?><div class="announcement"><?= linkify($announcement) ?></div><?php endif; ?>
<?php $flashes = take_flashes(); if ($flashes): ?>
<div class="flashes"><?php foreach ($flashes as [$t, $m]): ?><div class="flash flash-<?= e($t) ?>" role="status"><?= e($m) ?><button type="button" class="flash-x" aria-label="Dismiss">×</button></div><?php endforeach; ?></div>
<?php endif; ?>
<main class="main <?= e($mainClass ?? '') ?>">
<?= $content ?>
</main>
<?php if ($me): ?>
<nav class="tabbar" aria-label="Main">
  <a href="/home"<?= $active('/home') ?>><?= icon('home') ?><span>Feed</span></a>
  <a href="/discover"<?= $active('/discover') ?>><?= icon('search') ?><span>Discover</span></a>
  <a href="/properties"<?= $active('/properties') ?>><?= icon('building') ?><span>Places</span></a>
  <a href="/friends"<?= $active('/friends') ?>><?= icon('users') ?><span>Friends</span><?= $badge($counts['requests']) ?></a>
  <a href="/messages"<?= $active('/messages') ?> data-count="messages"><?= icon('chat') ?><span>Chats</span><?= $badge($counts['messages']) ?></a>
</nav>
<?php else: ?>
<footer class="footer">
  <div class="footer-inner">
    <div><strong><?= e($site) ?></strong><br><small>A roommate community by <a href="https://riseapartments.com">Rise Apartments</a>.</small></div>
    <nav><a href="/safety">Safety</a><a href="/terms">Terms</a><a href="/privacy">Privacy</a><a href="/login">Log in</a></nav>
  </div>
</footer>
<?php endif; ?>
<script src="/assets/app.js?v=<?= @filemtime(APP_ROOT . '/assets/app.js') ?>" defer></script>
</body>
</html>
