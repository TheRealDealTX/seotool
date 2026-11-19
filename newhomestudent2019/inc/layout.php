<?php defined('NHS') || exit;

/**
 * Output a full page.
 * $m keys: title (full <title>), description, path (canonical path), body (HTML),
 *          schema (array of JSON-LD nodes), image (path), type (website|article),
 *          noindex (bool), published, modified, status (HTTP code)
 */
function render_page(array $m): never {
    $m += ['schema' => [], 'image' => '/assets/img/og-default.jpg', 'type' => 'website', 'noindex' => false, 'status' => 200];
    http_response_code($m['status']);
    header('Content-Type: text/html; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    $canonical = url($m['path']);
    $img = url($m['image']);
    $schema = array_merge([org_schema(), [
        '@type' => 'WebSite', '@id' => url('/#website'), 'url' => url('/'), 'name' => SITE['name'],
        'publisher' => ['@id' => url('/#organization')],
    ]], $m['schema']);
    $current = $m['path'];
    ?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','<?= e(SITE['gtm_id']) ?>');</script>
<script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date());</script>
<!-- End Google Tag Manager -->
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($m['title']) ?></title>
<meta name="description" content="<?= e($m['description']) ?>">
<?php if ($m['noindex']): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta property="og:site_name" content="<?= e(SITE['name']) ?>">
<meta property="og:type" content="<?= e($m['type']) ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $m['title']) ?>">
<meta property="og:description" content="<?= e($m['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($img) ?>">
<?php if (!empty($m['published'])): ?><meta property="article:published_time" content="<?= e($m['published']) ?>">
<meta property="article:modified_time" content="<?= e($m['modified'] ?? $m['published']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#1d4e89">
<link rel="alternate" type="application/rss+xml" title="<?= e(SITE['name']) ?> feed" href="/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="<?= asset('css/site.css') ?>">
<?= json_ld($schema) ?>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=<?= e(SITE['gtm_id']) ?>" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span>Free owner-builder training: <a href="/free-training/">the 6 keys to building your own home &rarr;</a></span>
  <a class="topbar-phone" href="tel:<?= e(SITE['phone_href']) ?>"><?= icon('phone') ?> <?= e(SITE['phone']) ?></a>
</div></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= e(SITE['name']) ?> home">
      <span class="brand-mark" aria-hidden="true"><?= icon('house') ?></span>
      <span class="brand-text"><strong>New Home</strong> Investing Knowledge</span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
      <?php foreach (NAV as [$label, $href]): ?>
        <li><a href="<?= e($href) ?>"<?= str_starts_with($current, $href) && $href !== '/' ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
      <?php endforeach; ?>
      </ul>
      <a class="btn btn-small" href="/free-training/">Get the free course</a>
    </nav>
  </div>
</header>
<main id="main">
<?= $m['body'] ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand brand-footer" href="/"><span class="brand-mark" aria-hidden="true"><?= icon('house') ?></span><span class="brand-text"><strong>New Home</strong> Investing Knowledge</span></a>
      <p><?= e(SITE['tagline']) ?>. We teach owner-builders, future homeowners and new investors how to plan, build and protect a home they love.</p>
      <p class="footer-contact"><a href="tel:<?= e(SITE['phone_href']) ?>"><?= icon('phone') ?> <?= e(SITE['phone']) ?></a><br><a href="mailto:<?= e(SITE['email']) ?>"><?= icon('mail') ?> <?= e(SITE['email']) ?></a></p>
    </div>
    <div>
      <h2>Learn</h2>
      <ul>
        <li><a href="/build-a-home-yourself/">Build a home yourself</a></li>
        <li><a href="/free-training/">Free owner-builder training</a></li>
        <li><a href="/how-to-be-your-own-general-contractor/">Be your own general contractor</a></li>
        <li><a href="/new-home-construction-timeline/">Construction timeline</a></li>
        <li><a href="/how-much-does-it-cost-to-build-a-house-in-texas/">Cost to build in Texas</a></li>
      </ul>
    </div>
    <div>
      <h2>Topics</h2>
      <ul>
        <?php foreach (CATEGORIES as $slug => $c): ?><li><a href="/category/<?= e($slug) ?>/"><?= e($c['name']) ?></a></li><?php endforeach; ?>
        <li><a href="/our-products/">Recommended tools &amp; books</a></li>
      </ul>
    </div>
    <div>
      <h2>Company</h2>
      <ul>
        <li><a href="/about-us/">About us</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/write-for-us/">Write for us</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
        <li><a href="/terms-of-use/">Terms of use</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-legal">
    <p>As an Amazon Associate we earn from qualifying purchases. Some links on this site are affiliate links, which means we may earn a commission at no extra cost to you. Content is for general education only and is not legal, financial, engineering or insurance advice — always confirm requirements with your local building department and licensed professionals.</p>
    <p>&copy; <?= date('Y') ?> <?= e(SITE['name']) ?>. All rights reserved.</p>
  </div>
</footer>
<script src="<?= asset('js/site.js') ?>" defer></script>
</body>
</html>
<?php
    exit;
}

function page_hero(string $h1, string $lead = '', array $crumbs = [], string $extra = ''): string {
    $bc = '';
    if ($crumbs) {
        $bc = '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>';
        $last = count($crumbs) - 1;
        foreach ($crumbs as $i => [$name, $path]) {
            $bc .= $i === $last ? '<li aria-current="page">' . e($name) . '</li>' : '<li><a href="' . e($path) . '">' . e($name) . '</a></li>';
        }
        $bc .= '</ol></nav>';
    }
    return '<section class="page-hero"><div class="wrap">' . $bc . '<h1>' . e($h1) . '</h1>'
        . ($lead !== '' ? '<p class="lead">' . $lead . '</p>' : '') . $extra . '</div></section>';
}

function cta_band(): string {
    return '<section class="cta-band"><div class="wrap cta-inner">'
        . '<div><h2>Thinking about building your own home?</h2>'
        . '<p>Get our free owner-builder mini-course: six short lessons on how to design, budget and manage your build without overpaying a general contractor.</p></div>'
        . '<a class="btn btn-light" href="/free-training/">Start the free training ' . icon('arrow') . '</a>'
        . '</div></section>';
}
