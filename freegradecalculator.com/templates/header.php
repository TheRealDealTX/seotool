<?php
$P = $GLOBALS['__page'];
$title = $P['title'] ?? SITE_NAME;
$desc  = $P['description'] ?? '';
$canon = abs_url($P['path'] ?? '/');
$og    = SITE_URL . '/assets/img/photos/' . ($P['image'] ?? 'graduation-caps-sky') . '.webp';
$graph = array_merge([
    ['@type' => 'Organization', '@id' => SITE_URL . '/#org', 'name' => SITE_NAME, 'url' => SITE_URL . '/', 'logo' => SITE_URL . '/assets/img/logo.png', 'email' => SITE_EMAIL],
    ['@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'name' => SITE_NAME, 'url' => SITE_URL . '/', 'publisher' => ['@id' => SITE_URL . '/#org']],
], $P['schema'] ?? []);
$path = $P['path'] ?? '/';
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<?php if (!empty($P['noindex'])): ?><meta name="robots" content="noindex, follow"><?php else: ?><meta name="robots" content="index, follow, max-image-preview:large"><?php endif; ?>
<meta property="og:type" content="<?= isset($P['article']) ? 'article' : 'website' ?>">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:image" content="<?= e($og) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#6d5dfc">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="<?= asset('css/app.css') ?>">
<script>try{var t=localStorage.getItem('fgc-theme');if(t)document.documentElement.dataset.theme=t;}catch(e){}</script>
<?= json_ld(['@context' => 'https://schema.org', '@graph' => $graph]) ?>
</head>
<body class="<?= e($P['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span></span></div>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 40 40"><defs><linearGradient id="bm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7c6cff"/><stop offset="1" stop-color="#22d3ee"/></linearGradient></defs><rect width="40" height="40" rx="11" fill="url(#bm)"/><text x="20" y="27" text-anchor="middle" font-family="Space Grotesk,Arial" font-weight="700" font-size="18" fill="#fff">A+</text></svg></span>
      <span class="brand-name">Free<b>Grade</b>Calculator</span>
    </a>
    <nav class="main-nav" aria-label="Main">
      <?php foreach (nav_items() as [$label, $href]): ?>
        <a href="<?= e($href) ?>"<?= ($href === $path) ? ' aria-current="page"' : '' ?>><?= e($label) ?></a>
      <?php endforeach; ?>
    </nav>
    <div class="header-actions">
      <button class="icon-btn search-open" type="button" aria-label="Search tools (Ctrl+K)"><?= icon('search') ?><kbd>⌘K</kbd></button>
      <button class="icon-btn theme-toggle" type="button" aria-label="Toggle dark mode"><?= icon('moon', 'ic i-moon') ?><?= icon('sun', 'ic i-sun') ?></button>
      <button class="icon-btn menu-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><?= icon('menu') ?></button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu" hidden>
  <div class="mobile-menu-panel">
    <div class="mm-head"><strong>Menu</strong><button class="icon-btn menu-close" type="button" aria-label="Close menu"><?= icon('x') ?></button></div>
    <?php foreach (tool_categories() as $ck => [$cname, $cdesc, $cic]): ?>
      <details class="mm-group"><summary><?= icon($cic) ?> <?= e($cname) ?></summary>
        <div class="mm-links"><?php foreach (tools() as $s => $t) if ($t[1] === $ck): ?><a href="/<?= e($s) ?>"><?= e($t[0]) ?></a><?php endif; ?></div>
      </details>
    <?php endforeach; ?>
    <div class="mm-foot"><a href="/blog">Blog</a><a href="/study-supplies">Study Supplies</a><a href="/about-us">About</a><a href="/contact">Contact</a></div>
  </div>
</div>
<main id="main">
