<?php
defined('HA_ROOT') || exit;
$cur = strtok($_SERVER['REQUEST_URI'] ?? '/admin/', '?');
$nav = [
    ['/admin/', 'Dashboard', '▦'],
    ['/admin/listings/', 'Listings', '🏢'],
    ['/admin/listings/new/', 'Add a listing', '＋'],
    ['/admin/leads/', 'Leads', '✉'],
    ['/admin/import/', 'Import from Rise', '⇩'],
];
if (($user['role'] ?? '') === 'admin') {
    $nav[] = ['/admin/users/', 'Users', '👥'];
    $nav[] = ['/admin/integrations/', 'Integrations', '🔗'];
}
$nav[] = ['/admin/account/', 'My account', '⚙'];
$active = function ($href) use ($cur) {
    if ($href === '/admin/') return $cur === '/admin/';
    if ($href === '/admin/listings/') return str_starts_with($cur, '/admin/listings/') && $cur !== '/admin/listings/new/';
    return str_starts_with($cur, $href);
};
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title><?= e($title ?? 'Admin') ?> · Houston Apartments Admin</title>
<link rel="icon" href="/assets/img/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<link rel="stylesheet" href="<?= asset('css/admin.css') ?>">
</head>
<body data-csrf="<?= e($csrf) ?>">
<aside class="side" id="side">
  <a class="side-brand" href="/admin/"><?php $logoClass = 'logo-light'; require HA_APP . '/views/partials/logo.php'; ?><small>Admin</small></a>
  <nav>
    <?php foreach ($nav as [$href, $label, $ico]): ?>
      <a href="<?= $href ?>"<?= $active($href) ? ' class="on"' : '' ?>><span class="ni"><?= $ico ?></span><?= e($label) ?><?php if ($href === '/admin/leads/' && $newLeads): ?><b class="nb"><?= $newLeads ?></b><?php endif ?></a>
    <?php endforeach ?>
  </nav>
  <div class="side-foot">
    <a href="/" target="_blank" rel="noopener">View website ↗</a>
    <a href="/admin/logout/">Log out</a>
    <small>Signed in as <?= e($user['name'] ?: $user['email']) ?></small>
  </div>
</aside>
<div class="main">
  <header class="top">
    <button class="menu-btn" type="button" onclick="document.body.classList.toggle('nav-open')" aria-label="Menu">☰</button>
    <h1><?= e($title ?? '') ?></h1>
    <div class="top-actions"><?= $actions ?? '' ?></div>
  </header>
  <?php if ($flash): ?><div class="flash <?= e($flash[0]) ?>"><?= e($flash[1]) ?></div><?php endif ?>
  <div class="content"><?= $content ?></div>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="<?= asset('js/admin.js') ?>" defer></script>
</body>
</html>
