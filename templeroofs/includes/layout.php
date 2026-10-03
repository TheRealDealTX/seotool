<?php
/**
 * Page shell: <head>, header/navigation, footer, sticky mobile bar.
 *
 * $page keys: title, description, path, crumbs (list of [label, path]),
 * schema (list of JSON-LD nodes), image (OG image key), og_type, noindex,
 * body_class, scripts (list of asset paths), status (HTTP status).
 */
defined('TR_ROOT') || exit;

function page_title(array $page): string
{
    $t = $page['title'] ?? cfg('site_name');
    $brand = ' | ' . cfg('site_name');
    if (!empty($page['raw_title']) || str_contains($t, cfg('site_name')) || mb_strlen($t . $brand) > 65) {
        return $t;
    }
    return $t . $brand;
}

function layout_start(array $page): void
{
    http_response_code($page['status'] ?? 200);
    header('Content-Type: text/html; charset=utf-8');
    header('Cache-Control: no-cache');
    header("Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; font-src 'self'; frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'");
    $GLOBALS['TR_PAGE'] = $page;
    ob_start();

    $title = page_title($page);
    $desc = $page['description'] ?? '';
    $canonical = abs_url($page['path'] ?? '/');
    $ogImage = !empty($page['image'])
        ? abs_url('/assets/images/' . $page['image'] . '-1600.webp')
        : abs_url('/assets/images/og-image.jpg');
    $crumbs = $page['crumbs'] ?? [];
    $schema = array_merge([schema_business(), schema_website()], $page['schema'] ?? []);
    if ($crumbs) {
        $schema[] = schema_breadcrumbs($crumbs);
    }
    ?>
<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<?php if (!empty($page['noindex'])): ?>
<meta name="robots" content="noindex, follow">
<?php else: ?>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta name="theme-color" content="#0B1F3A">
<meta property="og:site_name" content="<?= e(cfg('site_name')) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($page['og_type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($ogImage) ?>">
<?php if (!empty($page['published_time'])): ?>
<meta property="article:published_time" content="<?= e($page['published_time']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($ogImage) ?>">
<link rel="preload" href="/assets/fonts/montserrat-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<?php if (!empty($page['preload_image'])): ?>
<link rel="preload" as="image" type="image/webp" imagesrcset="/assets/images/<?= e($page['preload_image']) ?>-800.webp 800w, /assets/images/<?= e($page['preload_image']) ?>-1600.webp 1600w" imagesizes="100vw" fetchpriority="high">
<?php endif; ?>
<link rel="stylesheet" href="<?= e(asset('css/site.css')) ?>">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Temple Roofers Blog" href="<?= e(abs_url('/blog/feed/')) ?>">
<?= schema_graph($schema) ?>

</head>
<body class="<?= e($page['body_class'] ?? '') ?>">
<a class="skip-link" href="#main">Skip to main content</a>
<?php site_header(); ?>
<main id="main" tabindex="-1">
<?php
}

function layout_end(array $page = []): void
{
    $page += $GLOBALS['TR_PAGE'] ?? [];
    ?>
</main>
<?php site_footer(); ?>
<?php icon_sprite(); ?>
<script src="<?= e(asset('js/site.js')) ?>" defer></script>
<?php foreach ($page['scripts'] ?? [] as $s): ?>
<script src="<?= e(asset($s)) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
    echo guard_links((string) ob_get_clean());
}

function logo_svg(): string
{
    return '<svg class="logo__mark" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
        . '<rect width="48" height="48" rx="11" fill="#0B1F3A"/>'
        . '<path d="M8 26 24 12l16 14" fill="none" stroke="#D4A843" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        . '<path d="M14 24v12h20V24" fill="none" stroke="#F2DFB0" stroke-width="3" stroke-linejoin="round"/>'
        . '<path d="M21 36v-7h6v7" fill="none" stroke="#F2DFB0" stroke-width="3" stroke-linejoin="round"/>'
        . '<path d="M31 15v-4h4v8" fill="none" stroke="#D4A843" stroke-width="3" stroke-linejoin="round"/>'
        . '</svg>';
}

function site_header(): void
{
    $services = services();
    $areas = areas();
    $tools = catalog('tools');
    ?>
<div class="topbar">
  <div class="container topbar__inner">
    <p class="topbar__msg"><?= icon('shield') ?> <strong>Free roof inspections in Temple, TX</strong><span class="topbar__dash"> — no cost, no obligation</span></p>
    <a class="topbar__phone" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <?= e(cfg('phone_intl')) ?></a>
  </div>
</div>
<header class="site-header" data-header>
  <div class="container site-header__inner">
    <a class="logo" href="/">
      <?= logo_svg() ?>
      <span class="logo__text"><span class="logo__name">Temple Roofers</span><span class="logo__tag">Temple, Texas</span></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul class="nav__list">
        <li class="nav__item has-drop">
          <a class="nav__link" href="/services/">Services</a>
          <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="drop-services" aria-label="Show services menu"><?= icon('chevron-down') ?></button>
          <div class="drop drop--mega" id="drop-services">
            <ul class="drop__grid">
              <?php foreach ($services as $s): ?>
              <li><a href="<?= e($s['url']) ?>"><?= icon($s['icon'] ?? 'home') ?><span><?= e($s['name']) ?></span></a></li>
              <?php endforeach; ?>
            </ul>
            <div class="drop__foot">
              <a href="/services/">All roofing services <?= icon('arrow-right') ?></a>
              <a class="drop__cta" href="/free-roof-inspection/">Book a free roof inspection</a>
            </div>
          </div>
        </li>
        <li class="nav__item has-drop">
          <a class="nav__link" href="/service-areas/">Service Areas</a>
          <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="drop-areas" aria-label="Show service areas menu"><?= icon('chevron-down') ?></button>
          <div class="drop" id="drop-areas">
            <ul>
              <?php foreach ($areas as $a): ?>
              <li><a href="<?= e($a['url']) ?>"><?= icon('map-pin') ?><span><?= e($a['city']) ?>, TX</span></a></li>
              <?php endforeach; ?>
              <li><a href="/service-areas/"><?= icon('arrow-right') ?><span>All service areas</span></a></li>
            </ul>
          </div>
        </li>
        <li class="nav__item has-drop">
          <a class="nav__link" href="/tools/">Roofing Tools</a>
          <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="drop-tools" aria-label="Show roofing tools menu"><?= icon('chevron-down') ?></button>
          <div class="drop" id="drop-tools">
            <ul>
              <?php foreach ($tools as $slug => $t): ?>
              <li><a href="/tools/<?= e($slug) ?>/"><?= icon($t['icon']) ?><span><?= e($t['short']) ?></span></a></li>
              <?php endforeach; ?>
              <li><a href="/weather/"><?= icon('cloud-sun') ?><span>Temple Weather</span></a></li>
            </ul>
          </div>
        </li>
        <li class="nav__item"><a class="nav__link" href="/weather/">Weather</a></li>
        <li class="nav__item"><a class="nav__link" href="/blog/">Blog</a></li>
        <li class="nav__item"><a class="nav__link" href="/about/">About</a></li>
        <li class="nav__item"><a class="nav__link" href="/contact/">Contact</a></li>
      </ul>
      <div class="nav__mobile-cta">
        <a class="btn btn--gold btn--block" href="/free-roof-inspection/">Get My Free Roof Inspection</a>
        <a class="btn btn--outline-light btn--block" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> Call <?= e(cfg('phone_display')) ?></a>
      </div>
    </nav>
    <div class="header-actions">
      <a class="header-phone" href="<?= e(tel_href()) ?>"><?= icon('phone') ?><span><?= e(cfg('phone_display')) ?></span><span class="sr-only header-phone__sr">Call Temple Roofers</span></a>
      <a class="btn btn--gold btn--sm header-cta" href="/free-roof-inspection/">Free Inspection</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav" data-menu-btn>
        <span class="menu-btn__bars" aria-hidden="true"></span><span class="sr-only">Menu</span>
      </button>
    </div>
  </div>
</header>
<?php
}

function site_footer(): void
{
    $services = services();
    $areas = areas();
    ?>
<footer class="site-footer">
  <div class="container footer__grid">
    <div class="footer__brand">
      <a class="logo logo--light" href="/">
        <?= logo_svg() ?>
        <span class="logo__text"><span class="logo__name">Temple Roofers</span><span class="logo__tag">Temple, Texas</span></span>
      </a>
      <p>Roof repair, replacement, storm damage and free roof inspections for homes and businesses in Temple and nearby Bell County communities.</p>
      <a class="footer__phone" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <?= e(cfg('phone_intl')) ?></a>
      <a class="btn btn--gold btn--sm" href="/free-roof-inspection/">Schedule a Free Inspection</a>
    </div>
    <div class="footer__col">
      <h2 class="footer__title">Roofing Services</h2>
      <ul>
        <?php foreach (array_slice($services, 0, 8) as $s): ?>
        <li><a href="<?= e($s['url']) ?>"><?= e($s['name']) ?></a></li>
        <?php endforeach; ?>
        <li><a href="/services/">All services</a></li>
      </ul>
    </div>
    <div class="footer__col">
      <h2 class="footer__title">Service Areas</h2>
      <ul>
        <?php foreach ($areas as $a): ?>
        <li><a href="<?= e($a['url']) ?>"><?= e($a['city']) ?>, TX</a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <div class="footer__col">
      <h2 class="footer__title">Resources</h2>
      <ul>
        <li><a href="/free-roof-inspection/">Free Roof Inspection</a></li>
        <li><a href="/tools/">Free Roofing Tools</a></li>
        <?php foreach (catalog('tools') as $slug => $t): ?>
        <li><a href="/tools/<?= e($slug) ?>/"><?= e($t['short']) ?></a></li>
        <?php endforeach; ?>
        <li><a href="/weather/">Temple Weather</a></li>
        <li><a href="/blog/">Roofing Blog</a></li>
      </ul>
    </div>
    <div class="footer__col">
      <h2 class="footer__title">Company</h2>
      <ul>
        <li><a href="/about/">About Temple Roofers</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
        <li><a href="/sitemap/">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="footer__bottom">
    <div class="container footer__bottom-inner">
      <p>&copy; <?= e(tr_now()->format('Y')) ?> Temple Roofers · Temple, Texas · <a href="<?= e(tel_href()) ?>"><?= e(cfg('phone_display')) ?></a></p>
      <p class="footer__note">Photos on this site are licensed stock images used for illustration. Weather data: Open-Meteo &amp; National Weather Service.</p>
    </div>
  </div>
</footer>
<div class="mobile-bar" aria-label="Quick contact">
  <a class="mobile-bar__call" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> Call Now</a>
  <a class="mobile-bar__cta" href="/free-roof-inspection/"><?= icon('clipboard-check') ?> Free Inspection</a>
</div>
<?php
}
