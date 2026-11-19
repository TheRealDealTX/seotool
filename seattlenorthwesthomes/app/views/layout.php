<?php defined('SNW') || (http_response_code(404) && exit);
$m = $meta + ['title' => cfg('name'), 'description' => cfg('tagline'), 'canonical' => '/', 'image' => '/assets/img/brand/og-default.jpg', 'type' => 'website', 'noindex' => false, 'schema' => []];
$m['title'] = meta_title($m['title']);
$m['description'] = meta_desc($m['description']);
$current = '/' . trim(parse_url($_SERVER['REQUEST_URI'] ?? '/', PHP_URL_PATH), '/') . '/';
$nav = [
    '/homes-for-sale/' => 'Homes for Sale',
    '/neighborhoods/' => 'Neighborhoods',
    '/buy-a-home-in-seattle/' => 'Buy',
    '/sell-your-home-seattle/' => 'Sell',
    '/blog/' => 'Blog',
    '/about-seattle-northwest-homes/' => 'About',
];
$isActive = fn($href) => $href === '/' ? $current === '/' : str_starts_with($current, $href);
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<?php if (cfg('gtm_id')): ?>
<script async src="https://www.googletagmanager.com/gtm.js?id=<?= e(cfg('gtm_id')) ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
</script>
<?php endif ?>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($m['title']) ?></title>
<meta name="description" content="<?= e($m['description']) ?>">
<link rel="canonical" href="<?= e(abs_url($m['canonical'])) ?>">
<?php if ($m['noindex']): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<?php endif ?>
<?php if (!empty($m['prev'])): ?><link rel="prev" href="<?= e(abs_url($m['prev'])) ?>">
<?php endif ?><?php if (!empty($m['next'])): ?><link rel="next" href="<?= e(abs_url($m['next'])) ?>">
<?php endif ?>
<meta property="og:site_name" content="<?= e(cfg('name')) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($m['type'] === 'product' ? 'website' : $m['type']) ?>">
<meta property="og:title" content="<?= e($m['title']) ?>">
<meta property="og:description" content="<?= e($m['description']) ?>">
<meta property="og:url" content="<?= e(abs_url($m['canonical'])) ?>">
<meta property="og:image" content="<?= e(abs_url($m['image'])) ?>">
<?php if (!empty($m['published'])): ?><meta property="article:published_time" content="<?= e($m['published']) ?>T09:00:00-08:00">
<meta property="article:modified_time" content="<?= e($m['modified']) ?>T09:00:00-08:00">
<?php endif ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($m['title']) ?>">
<meta name="twitter:description" content="<?= e($m['description']) ?>">
<meta name="twitter:image" content="<?= e(abs_url($m['image'])) ?>">
<meta name="theme-color" content="#0d2433">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="<?= e(cfg('name')) ?> Blog" href="/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600;700&display=swap">
<?php if (!empty($m['preload'])): ?><link rel="preload" as="image" href="<?= e($m['preload']) ?>" fetchpriority="high">
<?php endif ?>
<link rel="stylesheet" href="<?= asset('css/site.css') ?>">
<script type="application/ld+json"><?= schema_json($m['schema']) ?></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= e(cfg('name')) ?> home">
      <img src="/assets/img/brand/logo-light.webp" alt="<?= e(cfg('name')) ?>" width="190" height="72">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
<?php foreach ($nav as $href => $label): ?>
        <li><a href="<?= $href ?>"<?= $isActive($href) ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
<?php endforeach ?>
      </ul>
      <a class="btn btn-accent nav-cta" href="/contact-seattle-real-estate-agents/">Contact Us</a>
    </nav>
  </div>
</header>
<main id="main">
<?= $content ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="/assets/img/brand/logo-light.webp" alt="<?= e(cfg('name')) ?>" width="190" height="72" loading="lazy">
      <p>Local real estate guidance for buyers and sellers across Seattle's neighborhoods.</p>
      <p><a href="mailto:<?= e(cfg('email')) ?>"><?= e(cfg('email')) ?></a><?php if (cfg('phone')): ?><br><a href="tel:<?= e(preg_replace('/\D/', '', cfg('phone'))) ?>"><?= e(cfg('phone')) ?></a><?php endif ?></p>
    </div>
    <div>
      <h2 class="footer-h">Explore</h2>
      <ul>
        <li><a href="/homes-for-sale/">Seattle Homes for Sale</a></li>
        <li><a href="/neighborhoods/">Neighborhood Guide</a></li>
        <li><a href="/buy-a-home-in-seattle/">Buy a Home</a></li>
        <li><a href="/sell-your-home-seattle/">Sell Your Home</a></li>
        <li><a href="/blog/">Real Estate Blog</a></li>
        <li><a href="/contact-seattle-real-estate-agents/">Contact Us</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Neighborhoods</h2>
      <ul class="cols-2">
<?php foreach (array_slice(neighborhoods(), 0, 10, true) as $s => $h): ?>
        <li><a href="/neighborhoods/<?= $s ?>/"><?= e($h['name']) ?></a></li>
<?php endforeach ?>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Stay Updated</h2>
      <p>New listings and Seattle market notes, straight to your inbox.</p>
      <form class="newsletter" method="post" action="/submit/">
        <?= form_guard('newsletter') ?>
        <label class="sr" for="nl-email">Email address</label>
        <input id="nl-email" type="email" name="email" placeholder="you@example.com" required>
        <button class="btn btn-accent" type="submit">Subscribe</button>
      </form>
    </div>
  </div>
  <div class="wrap footer-legal">
    <p>&copy; <?= date('Y') ?> <?= e(cfg('name')) ?><?= cfg('brokerage') ? ' · ' . e(cfg('brokerage')) : '' ?>. All rights reserved.
      <a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-of-use/">Terms of Use</a> · <a href="/sitemap.xml">Sitemap</a></p>
    <p class="eho"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2 1 9h2v12h18V9h2L12 2zm5 17H7v-8h10v8zm-8-6h6v1.5H9V13zm0 3h6v1.5H9V16z"/></svg> Equal Housing Opportunity. We are committed to compliance with all federal, state and local fair housing laws.</p>
  </div>
</footer>
<script src="<?= asset('js/site.js') ?>" defer></script>
</body>
</html>
