<?php defined('BO') || exit;
// Page chrome: <head>, header, CTA band and footer.

/**
 * $m keys: title, desc, path, image (absolute path), type, schema (array of
 * graph nodes), body_class, robots, preload (image path for LCP).
 */
function page_head(array $m) {
    global $NAV, $POSTS;
    $title  = $m['title'];
    $canon  = SITE_URL . $m['path'];
    $image  = SITE_URL . ($m['image'] ?? img_url('Better-Outdoors-Site-Image.webp'));
    $graph  = array_merge([org_schema(), [
        '@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'url' => SITE_URL . '/', 'name' => SITE_NAME,
        'publisher' => ['@id' => SITE_URL . '/#organization'],
        'potentialAction' => ['@type' => 'SearchAction', 'target' => SITE_URL . '/blog/?q={search_term_string}', 'query-input' => 'required name=search_term_string'],
    ]], $m['schema'] ?? []);
    // Search index for the header search overlay.
    $index = [];
    foreach ($POSTS as $slug => $p) $index[] = ['t' => $p['h1'], 'u' => '/' . $slug . '/', 'k' => $p['kw'] . ' ' . $p['cat']];
    global $TOOLS;
    foreach ($TOOLS as $slug => $t) $index[] = ['t' => $t['h1'], 'u' => '/tools/' . $slug . '/', 'k' => 'tool calculator ' . $t['short']];
    ?>
<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($m['desc']) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<meta name="robots" content="<?= e($m['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1') ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($m['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($m['desc']) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:image" content="<?= e($image) ?>">
<?php if (!empty($m['published'])): ?>
<meta property="article:published_time" content="<?= e($m['published']) ?>T08:00:00+00:00">
<meta property="article:modified_time" content="<?= e($m['modified']) ?>T08:00:00+00:00">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#061E29">
<link rel="icon" href="<?= img_url('cropped-Better-Outdoors-Site-Icon-32x32.webp') ?>" sizes="32x32">
<link rel="icon" href="<?= img_url('cropped-Better-Outdoors-Site-Icon-192x192.webp') ?>" sizes="192x192">
<link rel="apple-touch-icon" href="<?= img_url('cropped-Better-Outdoors-Site-Icon-180x180.webp') ?>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@500;700;800&family=Roboto:ital,wght@0,400;0,500;0,700;1,400&display=swap">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_VER ?>">
<?php if (!empty($m['preload'])): ?>
<link rel="preload" as="image" href="<?= e($m['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<?= json_ld(['@context' => 'https://schema.org', '@graph' => $graph]) ?>

</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span class="progress-shaft"></span><span class="progress-tip"></span></div>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="Better Outdoors home">
      <img src="<?= img_url('Better-Outdoors-Logo.webp') ?>" alt="Better Outdoors logo" width="200" height="49">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach ($NAV as [$label, $href]): $cur = $href === $m['path'] || ($href !== '/' && str_starts_with($m['path'], $href)); ?>
        <li><a href="<?= e($href) ?>"<?= $cur ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
    </nav>
    <div class="header-actions">
      <button class="icon-btn" id="search-open" aria-label="Search the site"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i></button>
      <button class="icon-btn nav-toggle" id="nav-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="main-nav"><i class="fa-solid fa-bars" aria-hidden="true"></i></button>
    </div>
  </div>
</header>
<div class="search-overlay" id="search-overlay" hidden>
  <div class="search-box" role="dialog" aria-modal="true" aria-label="Search Better Outdoors">
    <div class="search-field"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i><input type="search" id="search-input" placeholder="Search bows, guides and tools…" autocomplete="off"><button class="icon-btn" id="search-close" aria-label="Close search"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button></div>
    <ul class="search-results" id="search-results"></ul>
  </div>
</div>
<script>window.BO_INDEX=<?= json_encode($index, JSON_UNESCAPED_SLASHES | JSON_HEX_TAG) ?>;</script>
<main id="main">
<?php
}

function page_foot($cta = true) {
    global $TOOLS;
    ?>
</main>
<?php if ($cta): ?>
<section class="cta-band">
  <canvas class="cta-canvas" aria-hidden="true"></canvas>
  <div class="wrap cta-inner reveal">
    <h2>Start Planning Your Next Outdoor Adventure</h2>
    <p>Browse our bow reviews, learn from real-world tuning advice, and head into the field with confidence.</p>
    <div class="btn-row">
      <a class="btn btn-orange" href="/blog/">Explore the Latest Articles</a>
      <a class="btn btn-ghost" href="/category/tips/">Discover Outdoor Tips</a>
      <a class="btn btn-ghost" href="/contact-us/">Contact Us</a>
    </div>
  </div>
</section>
<?php endif; ?>
<footer class="site-footer">
  <div class="footer-ridge" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="<?= img_url('Better-Outdoors-Logo-White.webp') ?>" alt="Better Outdoors logo" width="220" height="54" loading="lazy">
      <p>Better Outdoors provides free archery guides, bow reviews, interactive tools and honest gear recommendations to help you plan smarter hunts and enjoy every adventure.</p>
    </div>
    <div>
      <h4>Quick Links</h4>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="/category/tips/">Tips</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/contact-us/">Contact Us</a></li>
      </ul>
    </div>
    <div>
      <h4>Free Tools</h4>
      <ul>
<?php foreach ($TOOLS as $slug => $t): ?>
        <li><a href="/tools/<?= e($slug) ?>/"><?= e($t['h1']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h4>Learn More</h4>
      <ul>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
        <li><a href="/privacy-policy/#affiliate-disclosure">Affiliate Disclosure</a></li>
        <li><a href="/sitemap.xml">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; <?= date('Y') ?> Better Outdoors. All Rights Reserved.</p>
    <p class="small">As an Amazon Associate, Better Outdoors earns from qualifying purchases.</p>
  </div>
  <a class="to-top" href="#top" aria-label="Back to top"><i class="fa-solid fa-arrow-up" aria-hidden="true"></i></a>
</footer>
<script src="/assets/js/site.js?v=<?= ASSET_VER ?>" defer></script>
</body>
</html>
<?php
}
