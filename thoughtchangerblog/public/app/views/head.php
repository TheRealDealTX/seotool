<?php
/** @var array $meta title, description, canonical(path), type, image, robots, schema[], preload, bodyClass, published, modified */
$canonical = SITE_URL . ($meta['canonical'] ?? '/');
$image = SITE_URL . ($meta['image'] ?? '/wp-content/uploads/2026/01/Thought-Changer-Site-Image.webp');
$graph = array_merge([
    ['@type' => 'Organization', '@id' => SITE_URL . '/#organization', 'name' => SITE_NAME, 'url' => SITE_URL . '/',
     'email' => SITE_EMAIL,
     'logo' => ['@type' => 'ImageObject', 'url' => SITE_URL . LOGO, 'width' => 756, 'height' => 114]],
    ['@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'url' => SITE_URL . '/', 'name' => SITE_NAME,
     'description' => SITE_TAGLINE, 'publisher' => ['@id' => SITE_URL . '/#organization'], 'inLanguage' => 'en-US',
     'potentialAction' => ['@type' => 'SearchAction', 'target' => ['@type' => 'EntryPoint', 'urlTemplate' => SITE_URL . '/?s={search_term_string}'], 'query-input' => 'required name=search_term_string']],
], $meta['schema'] ?? []);
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($meta['title']) ?></title>
<?php if (!empty($meta['description'])): ?><meta name="description" content="<?= e($meta['description']) ?>">
<?php endif; ?>
<meta name="robots" content="<?= IS_STAGING ? 'noindex, nofollow' : e($meta['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1') ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php if (!empty($meta['prev'])): ?><link rel="prev" href="<?= e(SITE_URL . $meta['prev']) ?>">
<?php endif; if (!empty($meta['next'])): ?><link rel="next" href="<?= e(SITE_URL . $meta['next']) ?>">
<?php endif; ?>
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($meta['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($meta['title']) ?>">
<?php if (!empty($meta['description'])): ?><meta property="og:description" content="<?= e($meta['description']) ?>">
<?php endif; ?>
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<?php if (!empty($meta['published'])): ?><meta property="article:published_time" content="<?= e($meta['published']) ?>">
<meta property="article:modified_time" content="<?= e($meta['modified'] ?? $meta['published']) ?>">
<?php endif; ?>
<meta property="og:image" content="<?= e($image) ?>">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/wp-content/uploads/2026/01/cropped-Thought-Changer-Site-Icon-32x32.webp" sizes="32x32">
<link rel="icon" href="/wp-content/uploads/2026/01/cropped-Thought-Changer-Site-Icon-192x192.webp" sizes="192x192">
<link rel="apple-touch-icon" href="/wp-content/uploads/2026/01/cropped-Thought-Changer-Site-Icon-180x180.webp">
<meta name="theme-color" content="#00B3D1">
<link rel="alternate" type="application/rss+xml" title="<?= SITE_NAME ?> &raquo; Feed" href="<?= SITE_URL ?>/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,400;0,500;0,700;0,800;1,400&family=Roboto+Slab:wght@400;600&family=Rochester&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_VER ?>">
<?php if (!empty($meta['preload'])): ?><link rel="preload" as="image" href="<?= e($meta['preload']) ?>"<?php if (!empty($meta['preload_srcset'])): ?> imagesrcset="<?= e($meta['preload_srcset']) ?>" imagesizes="(max-width: 1100px) 100vw, 760px"<?php endif; ?> fetchpriority="high">
<?php endif; ?>
<script type="application/ld+json"><?= json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA_ID ?>"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','<?= GA_ID ?>');</script>
<script>document.documentElement.classList.add('js');</script>
</head>
<body class="<?= e($meta['bodyClass'] ?? '') ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header" id="top">
  <div class="header-bar">
    <a class="brand" href="/" aria-label="Thought Changer home"><img src="<?= LOGO ?>" width="756" height="114" alt="Thought Changer Logo"></a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <?php $cur = $meta['canonical'] ?? '/';
      foreach (['/' => 'Home', '/about-us/' => 'About Us', '/quotes/' => 'Quotes', '/mindset/' => 'Mindset', '/blog/' => 'Blog', '/recommended-reads/' => 'Bookshelf', '/contact-us/' => 'Contact Us'] as $href => $label): ?>
        <a href="<?= $href ?>"<?= $cur === $href ? ' aria-current="page"' : '' ?>><?= $label ?></a>
      <?php endforeach; ?>
    </nav>
    <form class="hsearch js-suggest" role="search" action="/" method="get" autocomplete="off">
      <label class="sr-only" for="hs">Search articles</label>
      <input id="hs" type="search" name="s" placeholder="Search articles…" value="<?= e($_GET['s'] ?? '') ?>" aria-autocomplete="list" aria-controls="hs-list" aria-expanded="false">
      <button type="submit" aria-label="Submit search"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M10 2a8 8 0 0 1 6.32 12.9l5.39 5.4-1.41 1.4-5.4-5.39A8 8 0 1 1 10 2Zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12Z"/></svg></button>
      <div class="suggest" id="hs-list" role="listbox" hidden></div>
    </form>
    <button class="search-toggle" type="button" aria-label="Search" aria-expanded="false"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M10 2a8 8 0 0 1 6.32 12.9l5.39 5.4-1.41 1.4-5.4-5.39A8 8 0 1 1 10 2Zm0 2a6 6 0 1 0 0 12 6 6 0 0 0 0-12Z"/></svg></button>
    <button class="nav-toggle" aria-controls="main-nav" aria-expanded="false" aria-label="Menu"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="main">
