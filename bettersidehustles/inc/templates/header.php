<?php
/** @var array $meta title, description, url, image?, type?, noindex?, schema?, published?, modified?, bodyClass? */
$canonical = abs_url($meta['url']);
$ogImage = abs_url($meta['image'] ?? SITE_IMAGE);
$graph = array_merge([schema_org(), schema_website()], $meta['schema'] ?? []);
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($meta['title']) ?></title>
<meta name="description" content="<?= e($meta['description']) ?>">
<?php if (!empty($meta['noindex'])): ?>
<meta name="robots" content="noindex, follow">
<?php else: ?>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:type" content="<?= e($meta['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($meta['og_title'] ?? $meta['title']) ?>">
<meta property="og:description" content="<?= e($meta['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($ogImage) ?>">
<?php if (!empty($meta['published'])): ?>
<meta property="article:published_time" content="<?= e($meta['published']) ?>T08:00:00+00:00">
<meta property="article:modified_time" content="<?= e($meta['modified'] ?? $meta['published']) ?>T08:00:00+00:00">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($meta['og_title'] ?? $meta['title']) ?>">
<meta name="twitter:description" content="<?= e($meta['description']) ?>">
<meta name="twitter:image" content="<?= e($ogImage) ?>">
<meta name="theme-color" content="#0097B2">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="<?= e(SITE_NAME) ?>" href="<?= SITE_URL ?>/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<?= json_ld($graph) ?>

</head>
<body class="<?= e($meta['bodyClass'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <img src="<?= SITE_LOGO ?>" alt="<?= e(SITE_NAME) ?> logo" width="170" height="56">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as [$label, $href, $menu]): ?>
<?php if ($menu === 'platforms'): ?>
        <li class="has-menu"><button type="button" class="menu-btn" aria-expanded="false"><?= e($label) ?><?= icon('chev') ?></button>
          <div class="mega">
            <div class="mega-col">
              <span class="mega-title">Platform guides</span>
<?php foreach (PLATFORMS as $slug => [$name, $logo, $blurb]): ?>
              <a href="/<?= $slug ?>/"><img src="<?= e($logo) ?>" alt="" width="28" height="28" loading="lazy"><span><b><?= e($name) ?></b><small><?= e($blurb) ?></small></span></a>
<?php endforeach; ?>
            </div>
            <div class="mega-col">
              <span class="mega-title">Popular guides</span>
              <a href="/side-hustles-you-can-start-with-just-your-smartphone/"><?= icon('phone') ?><span><b>Phone side hustles</b><small>20 legit ways to earn from your phone</small></span></a>
              <a href="/digital-marketing-side-hustle/"><?= icon('chart') ?><span><b>Digital marketing</b><small>Start a marketing side hustle</small></span></a>
              <a href="/blog/?cat=city-guides"><?= icon('pin') ?><span><b>Side hustles by city</b><small>70+ local city guides</small></span></a>
              <a href="/tools/side-hustle-quiz/"><?= icon('target') ?><span><b>Find your match</b><small>Take the 60-second quiz</small></span></a>
            </div>
          </div>
        </li>
<?php else: ?>
        <li><a href="<?= e($href) ?>"><?= e($label) ?></a></li>
<?php endif; ?>
<?php endforeach; ?>
      </ul>
    </nav>
    <a class="btn btn-sm btn-green header-cta" href="/tools/side-hustle-quiz/"><?= icon('target') ?>Take the Quiz</a>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><?= icon('menu') ?></button>
  </div>
</header>
<main id="main">
