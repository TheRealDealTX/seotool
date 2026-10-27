<?php
defined('HA_ROOT') || exit;
$title = $meta['title'] ?? SITE['name'];
$desc = $meta['description'] ?? '';
$canonical = isset($meta['canonical']) ? site_url($meta['canonical']) : null;
$image = !empty($meta['image']) ? site_url($meta['image']) : site_url('/assets/img/og-default.png');
$noindex = !config('indexable') || !empty($meta['noindex']);
$needsMap = in_array($meta['body_class'] ?? '', ['home', 'search-page', 'property-page'], true) || !empty($meta['map']);
$current = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$schemas = $meta['schema'] ?? [];
if (isset($schemas['@context'])) {
    $schemas = [$schemas];
}
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-5MLTL4JE4N"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-5MLTL4JE4N');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title><?= e($title) ?></title>
<?php if ($desc): ?><meta name="description" content="<?= e($desc) ?>"><?php endif ?>
<?php if ($canonical): ?><link rel="canonical" href="<?= e($canonical) ?>"><?php endif ?>
<?php if ($noindex): ?><meta name="robots" content="noindex, nofollow"><?php endif ?>
<meta property="og:type" content="<?= e($meta['type'] ?? 'website') ?>">
<meta property="og:site_name" content="Houston Apartments">
<meta property="og:title" content="<?= e($title) ?>">
<?php if ($desc): ?><meta property="og:description" content="<?= e($desc) ?>"><?php endif ?>
<?php if ($canonical): ?><meta property="og:url" content="<?= e($canonical) ?>"><?php endif ?>
<meta property="og:image" content="<?= e($image) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f766e">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Houston Apartments">
<meta name="application-name" content="Houston Apartments">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<?php if ($needsMap): ?>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin="">
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" crossorigin="">
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" crossorigin="">
<?php endif ?>
<link rel="stylesheet" href="<?= asset('css/site.css') ?>">
<?php foreach ($schemas as $schema): ?>
<script type="application/ld+json"><?= json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
<?php endforeach ?>
</head>
<body class="<?= e($meta['body_class'] ?? 'inner') ?><?= !empty($meta['full']) ? ' full' : '' ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="Houston Apartments home"><?php require HA_APP . '/views/partials/logo.php'; ?></a>
    <nav class="main-nav" aria-label="Main">
      <?php foreach (NAV as [$href, $label]): ?>
        <a href="<?= e($href) ?>"<?= str_starts_with($current, $href) ? ' aria-current="page"' : '' ?>><?= e($label) ?></a>
      <?php endforeach ?>
    </nav>
    <div class="header-cta">
      <a class="phone-link" href="tel:<?= SITE['phone_raw'] ?>"><span class="ico ico-phone" aria-hidden="true"></span><span><?= SITE['phone'] ?></span></a>
      <button class="btn btn-grad btn-sm" type="button" data-lead>Free apartment search</button>
      <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" hidden>
  <nav aria-label="Mobile">
    <?php foreach (NAV as [$href, $label]): ?><a href="<?= e($href) ?>"><?= e($label) ?></a><?php endforeach ?>
    <a href="/houston-apartments-frequently-asked-questions/">FAQs</a>
    <a href="/contact-houston-apartments/">Contact Us</a>
    <a class="btn btn-grad" href="tel:<?= SITE['phone_raw'] ?>">Call <?= SITE['phone'] ?></a>
    <a class="btn btn-outline" href="mailto:<?= SITE['email'] ?>">Email <?= SITE['email'] ?></a>
  </nav>
</div>

<main id="main">
<?= $content ?>
</main>

<?php if (empty($meta['full'])): ?>
<section class="cta-band reveal">
  <div class="wrap cta-band-inner">
    <div>
      <h2>Let a Houston Apartments locator do the searching.</h2>
      <p>Free for renters. Tell us your budget, move-in date and must-haves – we’ll send a short list and book the tours. Lease through us and get up to $<?= SITE['cashback'] ?> back.</p>
    </div>
    <div class="cta-band-actions">
      <button class="btn btn-light btn-lg magnetic" type="button" data-lead>Start my free search</button>
      <a class="btn btn-ghost-light btn-lg" href="tel:<?= SITE['phone_raw'] ?>">Call <?= SITE['phone'] ?></a>
    </div>
  </div>
</section>

<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <?php $logoClass = 'logo-light'; require HA_APP . '/views/partials/logo.php'; ?>
      <p>Houston Apartments is a free apartment locating service run by <?= e(SITE['legal']) ?>. Licensed Texas real estate professionals helping renters across Greater Houston since <?= SITE['founded'] ?>.</p>
      <p class="footer-contact"><a href="tel:<?= SITE['phone_raw'] ?>"><?= SITE['phone'] ?></a><br><a href="mailto:<?= SITE['email'] ?>"><?= SITE['email'] ?></a></p>
    </div>
    <div>
      <h3>Popular areas</h3>
      <ul>
        <?php foreach (array_slice(AREAS, 0, 9, true) as $slug => $a): ?>
          <li><a href="/<?= $slug ?>/"><?= e($a['name']) ?> Apartments</a></li>
        <?php endforeach ?>
      </ul>
    </div>
    <div>
      <h3>Suburbs</h3>
      <ul>
        <?php foreach (array_slice(AREAS, 9, null, true) as $slug => $a): ?>
          <li><a href="/<?= $slug ?>/"><?= e($a['name']) ?> Apartments</a></li>
        <?php endforeach ?>
      </ul>
    </div>
    <div>
      <h3>Resources</h3>
      <ul>
        <li><a href="/apartments/">Map search</a></li>
        <li><a href="/houston-apartment-tools/">Free renter tools</a></li>
        <li><a href="/about-houston-apartments/">About Houston Apartments</a></li>
        <li><a href="/houston-apartments-process/">Our process</a></li>
        <li><a href="/houston-apartments-blog/">Houston Apartments blog</a></li>
        <li><a href="/houston-apartments-frequently-asked-questions/">FAQs</a></li>
        <li><a href="/contact-houston-apartments/">Contact</a></li>
        <li><a href="/wp-content/uploads/2024/09/TREC-Information-About-Brokerage-Services.pdf" target="_blank" rel="noopener">TREC Information About Brokerage Services</a></li>
        <li><a href="/wp-content/uploads/2024/09/TREC-Consumer-Protection-Notice.pdf" target="_blank" rel="noopener">TREC Consumer Protection Notice</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>© <?= date('Y') ?> Houston Apartments. All rights reserved. Prices and availability are subject to change; confirm details with the property.</p>
    <button type="button" class="to-top" data-to-top aria-label="Back to top">↑</button>
  </div>
</footer>
<?php endif ?>

<div class="modal" id="lead-modal" hidden role="dialog" aria-modal="true" aria-labelledby="lead-title">
  <div class="modal-backdrop"></div>
  <div class="modal-card">
    <button class="modal-x" type="button" data-close aria-label="Close">×</button>
    <div class="modal-head">
      <span class="pill pill-grad">Free · No obligation</span>
      <h2 id="lead-title">Find my Houston apartment</h2>
      <p class="lead-for" hidden></p>
      <p>A local locator will text you matching options within one business day. Lease through us and get up to $<?= SITE['cashback'] ?> back.</p>
    </div>
    <form class="lead-form" novalidate>
      <input type="hidden" name="property_id" value="">
      <input type="hidden" name="page" value="">
      <label class="hp">Website <input name="website" tabindex="-1" autocomplete="off"></label>
      <div class="grid2">
        <label>Name<input name="name" required autocomplete="name"></label>
        <label><span>Phone <small>(US numbers only)</small></span><input name="phone" type="tel" autocomplete="tel-national" inputmode="numeric" required placeholder="+1 (___) ___-____" data-us-phone><span class="field-err" hidden></span></label>
      </div>
      <label>Email<input name="email" type="email" autocomplete="email" required></label>
      <div class="grid3">
        <label>Move-in<select name="move_in"><option value="">Any time</option><option>ASAP</option><option>Within 30 days</option><option>1–2 months</option><option>2+ months</option></select></label>
        <label>Bedrooms<select name="beds"><option value="">Any</option><option>Studio</option><option>1</option><option>2</option><option>3+</option></select></label>
        <label>Budget<select name="budget"><option value="">Any</option><option>Under $1,200</option><option>$1,200–$1,600</option><option>$1,600–$2,200</option><option>$2,200+</option></select></label>
      </div>
      <label>Anything else?<textarea name="message" rows="2" placeholder="Pets, neighborhoods, commute, must-have amenities…"></textarea></label>
      <button class="btn btn-grad btn-block btn-lg" type="submit">Send my request</button>
      <p class="form-note">By submitting you agree to be contacted about apartments. We never sell your information.</p>
      <p class="form-msg" role="status" aria-live="polite"></p>
    </form>
  </div>
</div>

<?php if ($needsMap): ?>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js" crossorigin=""></script>
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js" crossorigin=""></script>
<script src="https://unpkg.com/@maplibre/maplibre-gl-leaflet@0.0.22/leaflet-maplibre-gl.js" crossorigin=""></script>
<script>window.HA_MAP = <?= json_encode(['style' => config('map_style'), 'attr' => config('map_attr')], JSON_UNESCAPED_SLASHES) ?>;</script>
<?php endif ?>
<script src="<?= asset('js/site.js') ?>" defer></script>
<?php if ($needsMap): ?><script src="<?= asset('js/map.js') ?>" defer></script><?php endif ?>
<?php foreach ($meta['scripts'] ?? [] as $js): ?><script src="<?= asset($js) ?>" defer></script><?php endforeach ?>
</body>
</html>
