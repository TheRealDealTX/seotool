<?php
defined('ERE') or exit;

/**
 * $m keys: title (full <title>), description, path (canonical path), type (website|article),
 * image (abs url), schema (array of nodes), robots, crumbs ([[name,url],...]), body_class,
 * published, modified, scripts (array of asset paths)
 */
function page_head(array $m): void
{
    $c = cfg();
    $canonical = abs_url($m['path'] ?? '/');
    $image = $m['image'] ?? abs_url('/assets/img/og-default.jpg');
    $robots = $m['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1';
    $nodes = array_merge([schema_org(), schema_website()], $m['schema'] ?? []);
    if (!empty($m['crumbs'])) {
        $nodes[] = schema_breadcrumbs($m['crumbs']);
    }
    $nav = [
        ['/blog/', 'Blog'],
        ['/category/buying/', 'Buying'],
        ['/category/selling/', 'Selling'],
        ['/category/investing/', 'Investing'],
        ['/category/insurance-claims/', 'Claims'],
        ['/tools/', 'Free Tools'],
        ['/recommended-products/', 'Gear'],
    ];
    $current = $m['path'] ?? '/';
    ?><!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($m['title']) ?></title>
<meta name="description" content="<?= e($m['description']) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($m['type'] ?? 'website') ?>">
<meta property="og:site_name" content="<?= e($c['name']) ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $m['title']) ?>">
<meta property="og:description" content="<?= e($m['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<?php if (!empty($m['published'])): ?>
<meta property="article:published_time" content="<?= e(date('c', strtotime($m['published']))) ?>">
<meta property="article:modified_time" content="<?= e(date('c', strtotime($m['modified'] ?? $m['published']))) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($m['og_title'] ?? $m['title']) ?>">
<meta name="twitter:description" content="<?= e($m['description']) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<meta name="theme-color" content="#0f2a44">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="<?= e($c['name']) ?>" href="<?= e(abs_url('/feed.xml')) ?>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="<?= asset('css/site.css') ?>">
<?= json_ld($nodes) ?>

</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/" aria-label="<?= e($c['name']) ?> home">
      <span class="brand__mark" aria-hidden="true">540</span>
      <span class="brand__text"><strong>Exit Real Estate</strong><span>540</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><?= icon('menu') ?><span class="sr-only">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
<?php foreach ($nav as [$href, $label]): $active = $current === $href || ($href !== '/' && str_starts_with($current, $href) && $href !== '/blog/'); ?>
        <li><a href="<?= $href ?>"<?= $active ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
    </nav>
  </div>
</header>
<main id="main">
<?php
}

function breadcrumbs(array $crumbs): void
{
    echo '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => [$name, $url]) {
        echo $i === $last
            ? '<li aria-current="page">' . e($name) . '</li>'
            : '<li><a href="' . e($url) . '">' . e($name) . '</a></li>';
    }
    echo '</ol></nav>';
}

function page_foot(array $m = []): void
{
    $c = cfg();
    ?>
</main>
<section class="newsletter">
  <div class="wrap newsletter__inner">
    <div>
      <h2>Make your next move with confidence</h2>
      <p>Run the numbers before you buy, sell, refinance or file a claim. Every calculator is free, private and runs right in your browser.</p>
    </div>
    <a class="btn btn--light" href="/tools/">Browse free tools <?= icon('arrow') ?></a>
  </div>
</section>
<footer class="site-footer">
  <div class="wrap site-footer__grid">
    <div>
      <a class="brand brand--light" href="/"><span class="brand__mark" aria-hidden="true">540</span><span class="brand__text"><strong>Exit Real Estate</strong><span>540</span></span></a>
      <p class="site-footer__about"><?= e($c['description']) ?></p>
    </div>
    <div>
      <h2>Topics</h2>
      <ul>
<?php foreach ($c['categories'] as $slug => $cat): ?>
        <li><a href="/category/<?= $slug ?>/"><?= e($cat['name']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2>Popular tools</h2>
      <ul>
<?php foreach (['mortgage-calculator', 'home-affordability-calculator', 'closing-cost-calculator', 'rental-property-calculator', 'texas-property-tax-calculator', 'insurance-claim-depreciation-calculator'] as $t): ?>
        <li><a href="<?= tools()[$t]['url'] ?>"><?= e(tools()[$t]['name']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2>Site</h2>
      <ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/write-for-us/">Write for Us</a></li>
        <li><a href="/recommended-products/">Recommended Gear</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms/">Terms of Use</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap site-footer__legal">
    <p>&copy; <?= date('Y') ?> <?= e($c['name']) ?>. Educational content only - not legal, tax, insurance or financial advice. Calculator results are estimates.</p>
    <p>As an Amazon Associate we earn from qualifying purchases. <a href="/affiliate-disclosure/">Learn more</a>.</p>
  </div>
</footer>
<script src="<?= asset('js/site.js') ?>" defer></script>
<?php foreach ($m['scripts'] ?? [] as $s): ?>
<script src="<?= asset($s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}

function post_card(array $p, bool $featured = false): string
{
    $cat = category($p['category']);
    return '<article class="card' . ($featured ? ' card--featured' : '') . ' cat-' . e($p['category']) . '">'
        . (has_photo($p['slug'])
            ? '<a class="card__art card__art--photo" href="' . e($p['url']) . '" tabindex="-1" aria-hidden="true">' . picture($p['slug'], $featured ? '(max-width: 620px) 100vw, 480px' : '(max-width: 620px) 100vw, (max-width: 960px) 50vw, 380px', '', false, '') . '</a>'
            : '<a class="card__art" href="' . e($p['url']) . '" tabindex="-1" aria-hidden="true">' . icon($cat['icon']) . '</a>')
        . '<div class="card__body">'
        . '<a class="card__cat" href="' . e($cat['url']) . '">' . e($cat['name']) . '</a>'
        . '<h3 class="card__title"><a href="' . e($p['url']) . '">' . e($p['title']) . '</a></h3>'
        . '<p class="card__excerpt">' . e($p['excerpt']) . '</p>'
        . '<p class="card__meta"><time datetime="' . e($p['date']) . '">' . e(fmt_date($p['date'])) . '</time> &middot; ' . (int) $p['read_minutes'] . ' min read</p>'
        . '</div></article>';
}
