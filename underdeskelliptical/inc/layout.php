<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// Page shell: <head>, header, footer. Every route calls page_start() then page_end().

function page_start(array $m): void
{
    $title = $m['title'];
    $desc = $m['description'] ?? SITE_TAGLINE;
    $canon = SITE_URL . ($m['path'] ?? CURRENT_PATH);
    $img = abs_url($m['image'] ?? DEFAULT_IMAGE);
    $graph = array_merge([schema_org(), schema_website()], $m['schema'] ?? []);
    $ld = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
    $css = '/assets/css/site.css?v=' . @filemtime(ROOT . '/assets/css/site.css');
    ?>
<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<?php if (!empty($m['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<?php endif; ?>
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($m['og_type'] ?? 'website') ?>">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:image" content="<?= e($img) ?>">
<?php if (!empty($m['published'])): ?>
<meta property="article:published_time" content="<?= e($m['published']) ?>T08:00:00+00:00">
<meta property="article:modified_time" content="<?= e($m['updated'] ?? $m['published']) ?>T08:00:00+00:00">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/wp-content/uploads/2026/04/cropped-Under-Desk-Elliptical-Site-Icon-32x32.webp" sizes="32x32">
<link rel="icon" href="<?= e(SITE_ICON) ?>" sizes="192x192">
<link rel="apple-touch-icon" href="/wp-content/uploads/2026/04/cropped-Under-Desk-Elliptical-Site-Icon-180x180.webp">
<?php if (!empty($m['preload'])): ?><link rel="preload" as="image" href="<?= e($m['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="<?= e($css) ?>">
<script type="application/ld+json"><?= $ld ?></script>
</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">Free tools: <a href="/tools/which-under-desk-elliptical-quiz/">Find your under desk elliptical in 60 seconds</a> &middot; <a href="/tools/under-desk-elliptical-calorie-calculator/">Calorie calculator</a></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="<?= e(SITE_NAME) ?> home"><img src="<?= e(SITE_LOGO) ?>" alt="<?= e(SITE_NAME) ?>" width="1026" height="150"></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as [$label, $href]): ?>
        <li><a href="<?= e($href) ?>"<?= CURRENT_PATH === $href ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
      <form class="nav-search" action="/" method="get" role="search"><label class="sr" for="q">Search</label><input id="q" type="search" name="s" placeholder="Search guides…"></form>
    </nav>
  </div>
</header>
<main id="main">
<?php
}

function page_end(): void
{
    $js = '/assets/js/site.js?v=' . @filemtime(ROOT . '/assets/js/site.js');
    ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="logo" href="/"><img src="/wp-content/uploads/2026/04/Under-Desk-Elliptical-Logo-Alt.webp" alt="<?= e(SITE_NAME) ?>" width="1026" height="150" loading="lazy"></a>
      <p><?= e(SITE_NAME) ?> helps desk workers, remote employees and seniors choose the right under desk elliptical, use it well and stay active all day.</p>
      <p class="small">As an Amazon Associate, <?= e(SITE_NAME) ?> earns from qualifying purchases. <a href="/affiliate-disclosure/">Affiliate disclosure</a>.</p>
    </div>
    <div>
      <h2>Top Guides</h2>
      <ul>
        <li><a href="/what-is-the-best-under-desk-elliptical/">Best Under Desk Elliptical</a></li>
        <li><a href="/best-under-desk-elliptical-for-seniors/">Best for Seniors</a></li>
        <li><a href="/quietest-under-desk-elliptical/">Quietest Models</a></li>
        <li><a href="/best-motorized-under-desk-elliptical/">Best Motorized</a></li>
        <li><a href="/what-muscles-does-an-under-desk-elliptical-work/">Muscles Worked</a></li>
        <li><a href="/under-desk-elliptical-vs-walking-pad/">Elliptical vs Walking Pad</a></li>
      </ul>
    </div>
    <div>
      <h2>Free Tools</h2>
      <ul>
<?php foreach (TOOLS as $slug => $t): ?>
        <li><a href="/tools/<?= e($slug) ?>/"><?= e($t['short']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2><?= e(SITE_NAME) ?></h2>
      <ul>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/blog/">All Guides</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
        <li><a href="/sitemap/">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; <?= date('Y') ?> <?= e(SITE_NAME) ?>. Information on this site is for general education and is not medical advice. Talk to your doctor before starting a new exercise program.</p>
  </div>
</footer>
<script src="<?= e($js) ?>" defer></script>
</body>
</html>
<?php
}
