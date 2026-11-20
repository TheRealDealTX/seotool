<?php defined('WCA') || exit;
$siteName = cfg('site_name');
$title = $meta['title'] ?? $siteName;
$desc = $meta['description'] ?? '';
$canonical = isset($meta['canonical']) ? url($meta['canonical']) : null;
$img = url($meta['image'] ?? '/assets/img/og-default.webp');
$admin = str_contains($meta['body_class'] ?? '', 'admin');
$user = current_user();
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<?php if ($desc): ?><meta name="description" content="<?= e($desc) ?>"><?php endif; ?>
<?php if ($canonical): ?><link rel="canonical" href="<?= e($canonical) ?>"><?php endif; ?>
<meta name="robots" content="<?= e($meta['robots'] ?? 'index, follow, max-image-preview:large') ?>">
<meta property="og:site_name" content="<?= e($siteName) ?>">
<meta property="og:type" content="<?= e($meta['og_type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($title) ?>">
<?php if ($desc): ?><meta property="og:description" content="<?= e($desc) ?>"><?php endif; ?>
<?php if ($canonical): ?><meta property="og:url" content="<?= e($canonical) ?>"><?php endif; ?>
<meta property="og:image" content="<?= e($img) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f4c5c">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="<?= asset('css/style.css') ?>">
<?php if (!empty($meta['leaflet'])): ?>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<?php endif; ?>
<?php foreach ($meta['schema'] ?? [] as $s): ?>
<script type="application/ld+json"><?= json_encode($s, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
<?php endforeach; ?>
</head>
<body class="<?= e($meta['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="<?= e($siteName) ?> home">
      <img src="/assets/img/logo.svg" alt="" width="36" height="36">
      <span><strong>West Carrollton</strong> Apartments</span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav id="nav" class="nav" aria-label="Main">
      <?php if ($admin && is_admin()): ?>
        <a href="/admin/">Dashboard</a><a href="/admin/listings/">Listings</a><a href="/admin/users/">Owners</a><a href="/admin/payments/">Payments</a><a href="/admin/messages/">Messages</a><a href="/admin/settings/">Settings</a><a href="/" target="_blank">View site ↗</a><a href="/admin/logout/">Log out</a>
      <?php else: ?>
      <div class="dropdown">
        <a href="/apartments/">Apartments</a>
        <button type="button" class="sub-toggle" aria-expanded="false" aria-label="Show apartment categories">▾</button>
        <div class="dropdown-menu">
          <a href="/apartments/">All apartments</a>
          <a href="/apartments/pet-friendly/">Pet-friendly</a>
          <a href="/apartments/under-1000/">Under $1,000</a>
          <a href="/apartments/1-bedroom/">1 bedroom</a>
          <a href="/apartments/2-bedroom/">2 bedroom</a>
          <a href="/apartments/3-bedroom/">3 bedroom</a>
          <a href="/apartments/townhomes/">Townhomes</a>
          <a href="/apartments/senior/">Senior / 55+</a>
          <a href="/apartments/income-based/">Income-based</a>
        </div>
      </div>
      <a href="/tools/">Renter Tools</a>
      <a href="/west-carrollton-living-guide/">Living Guide</a>
      <a href="/blog/">Blog</a>
      <a href="/compare/" class="fav-link" title="Saved & compare">♥<span class="fav-label"> Saved &amp; compare</span> <span class="fav-count" hidden>0</span></a>
      <?php if ($user): ?><a href="/account/">My Account</a><?php else: ?><a href="/account/login/">Owner Login</a><?php endif; ?>
      <a class="btn btn-sm" href="/list-your-property/">List Your Property</a>
      <?php endif; ?>
    </nav>
  </div>
</header>

<main id="main">
<?php if (!empty($meta['breadcrumbs'])): ?>
<nav class="wrap breadcrumbs" aria-label="Breadcrumb"><ol>
<?php foreach ($meta['breadcrumbs'] as [$n, $p]): ?>
  <li><?php if ($p): ?><a href="<?= e($p) ?>"><?= e($n) ?></a><?php else: ?><span aria-current="page"><?= e($n) ?></span><?php endif; ?></li>
<?php endforeach; ?>
</ol></nav>
<?php endif; ?>
<?php $fl = flashes(); if ($fl): ?>
<div class="wrap flashes"><?php foreach ($fl as [$t, $m]): ?><div class="alert alert-<?= e($t) ?>"><?= e($m) ?></div><?php endforeach; ?></div>
<?php endif; ?>
<?= $content ?>
</main>

<?php if (!$admin): ?>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="logo logo-light" href="/"><img src="/assets/img/logo.svg" alt="" width="32" height="32"><span><strong>West Carrollton</strong> Apartments</span></a>
      <p>An independent directory of apartment, townhome and senior communities in West Carrollton, Ohio 45449 and the surrounding Dayton area.</p>
      <p><a href="mailto:info@westcarrolltonapartments.com">info@westcarrolltonapartments.com</a></p>
    </div>
    <div>
      <h3>Find an apartment</h3>
      <a href="/apartments/">All apartments</a>
      <a href="/apartments/pet-friendly/">Pet-friendly apartments</a>
      <a href="/apartments/under-1000/">Apartments under $1,000</a>
      <a href="/apartments/2-bedroom/">2-bedroom apartments</a>
      <a href="/apartments/townhomes/">Townhomes for rent</a>
      <a href="/apartments/senior/">Senior apartments</a>
    </div>
    <div>
      <h3>Renter tools</h3>
      <a href="/tools/rent-affordability-calculator/">Rent affordability calculator</a>
      <a href="/tools/apartment-match-quiz/">Apartment match quiz</a>
      <a href="/tools/roommate-rent-splitter/">Roommate rent splitter</a>
      <a href="/tools/moving-cost-estimator/">Moving cost estimator</a>
      <a href="/tools/room-planner/">Room layout planner</a>
      <a href="/west-carrollton-living-guide/">West Carrollton living guide</a>
    </div>
    <div>
      <h3>Owners &amp; managers</h3>
      <a href="/list-your-property/">List your property</a>
      <a href="/apartments/">Claim your listing</a>
      <a href="/account/login/">Owner login</a>
      <h3 class="mt">Company</h3>
      <a href="/about/">About</a>
      <a href="/contact/">Contact</a>
      <a href="/blog/">Blog</a>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; <?= date('Y') ?> West Carrollton Apartments. Listing information is gathered from public sources and owners and may change; confirm details with the property. Photos marked "representative" are stock images.</p>
    <p class="small">As an Amazon Associate we earn from qualifying purchases. <a href="/affiliate-disclosure/">Affiliate disclosure</a> · <a href="/privacy-policy/">Privacy</a> · <a href="/terms-of-use/">Terms</a></p>
  </div>
</footer>
<?php endif; ?>
<?php if (!empty($meta['leaflet'])): ?><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script><?php endif; ?>
<script src="<?= asset('js/app.js') ?>" defer></script>
<?php if (!empty($meta['tools_js'])): ?><script src="<?= asset('js/tools.js') ?>" defer></script><?php endif; ?>
</body>
</html>
