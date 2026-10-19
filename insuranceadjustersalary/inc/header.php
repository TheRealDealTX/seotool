<?php
/**
 * Shared <head> + site header.
 * Expects $page = [
 *   'title' => '<title>', 'description' => '...', 'path' => '/canonical/path/',
 *   'image' => 'file.webp' (optional, og image), 'schema' => [ ...JSON-LD nodes ] (optional),
 *   'body_class' => '' (optional), 'type' => 'website'|'article'
 * ]
 */
$page += ['image' => 'hero-roof-inspection.webp', 'schema' => [], 'body_class' => '', 'type' => 'website', 'preload' => null];
$canonical = base_url() . $page['path'];
$ogImage   = base_url() . '/assets/img/' . $page['image'];

$graph = array_merge([
    [
        '@type' => 'Organization',
        '@id'   => base_url() . '/#org',
        'name'  => SITE_NAME,
        'url'   => base_url() . '/',
        'logo'  => base_url() . '/icon-192.png',
    ],
    [
        '@type' => 'WebSite',
        '@id'   => base_url() . '/#website',
        'name'  => SITE_NAME,
        'url'   => base_url() . '/',
        'publisher' => ['@id' => base_url() . '/#org'],
    ],
], $page['schema']);

$current = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($page['title']) ?></title>
<meta name="description" content="<?= e($page['description']) ?>">
<?php if (is_temporary_host()): ?>
<meta name="robots" content="noindex, nofollow">
<?php else: ?>
<meta name="robots" content="index, follow, max-image-preview:large">
<?php endif; ?>
<link rel="canonical" href="<?= e($canonical) ?>">
<meta property="og:type" content="<?= e($page['type']) ?>">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:title" content="<?= e($page['title']) ?>">
<meta property="og:description" content="<?= e($page['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($ogImage) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#121212">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
<?php if ($page['preload']): ?>
<link rel="preload" as="image" href="/assets/img/<?= e($page['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<link rel="stylesheet" href="<?= asset('css/style.css') ?>">
<script type="application/ld+json"><?= json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
</head>
<body class="<?= e($page['body_class']) ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span></span></div>
<header class="site-header" id="top">
  <div class="promo-bar">
    <div class="container promo-inner">
      <span><?= icon('bolt', 14) ?> <span class="promo-long">Get your Texas adjuster license this week &mdash;</span> <a href="<?= COURSE_URL ?>" target="_blank" rel="sponsored noopener">Get Certified</a></span>
      <?= promo_line('promo-code') ?>
    </div>
  </div>
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <span class="brand-mark"><?= icon('shield', 22) ?></span>
      <span class="brand-text">Insurance Adjuster <em>Salary</em></span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach (nav_items() as $label => $href):
    $active = ($href !== '/#salary-guide' && str_starts_with($current, rtrim($href, '/') . '/')) ? ' aria-current="page"' : ''; ?>
        <li><a href="<?= e($href) ?>"<?= $active ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-gold btn-sm nav-cta" href="<?= COURSE_URL ?>" target="_blank" rel="sponsored noopener">Get Certified <span class="nav-code">joe20 = 20% off</span></a>
    </nav>
    <button class="nav-toggle" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="main">
