<?php
// Shared layout: <head>, header, footer, lead forms, schema. Every page starts with
//   require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';  (or a relative path)
//   page_start([...]);  ...page HTML...  page_end();

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/posts.php';

function e($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function abs_url(string $path): string { return preg_match('#^https?://#', $path) ? $path : SITE_URL . $path; }
function tel_link(string $cls = '', string $label = ''): string {
    return '<a class="' . e($cls) . '" href="tel:' . PHONE_E164 . '">' . ($label !== '' ? $label : 'Call ' . PHONE_DISPLAY) . '</a>';
}
function asset(string $path): string {
    $f = dirname(__DIR__) . $path;
    return $path . (is_file($f) ? '?v=' . filemtime($f) : '');
}

/** Schema nodes shared by every page. */
function base_schema(): array {
    return [
        [
            '@type' => ['ProfessionalService', 'LocalBusiness'],
            '@id' => SITE_URL . '/#business',
            'name' => SITE_NAME,
            'legalName' => LEGAL_NAME,
            'alternateName' => ['Houston Public Adjusting', 'Houston Public Insurance Adjusters'],
            'description' => 'Houston Public Adjusters are licensed Texas public insurance adjusters who represent homeowners and business owners — not insurance companies — on hurricane, wind, hail, flood, water and fire damage claims across Greater Houston.',
            'url' => SITE_URL . '/',
            'telephone' => PHONE_E164,
            'email' => EMAIL,
            'image' => SITE_URL . '/assets/img/houston-public-adjusters-og.jpg',
            'logo' => SITE_URL . '/assets/img/houston-public-adjusters-logo.png',
            'priceRange' => 'No upfront fees — contingency based',
            'address' => ['@type' => 'PostalAddress', 'addressLocality' => 'Houston', 'addressRegion' => 'TX', 'addressCountry' => 'US'],
            'geo' => ['@type' => 'GeoCoordinates', 'latitude' => GEO_LAT, 'longitude' => GEO_LNG],
            'areaServed' => array_map(fn($a) => ['@type' => 'City', 'name' => $a[0] . ', TX'], AREAS),
            'openingHoursSpecification' => [[
                '@type' => 'OpeningHoursSpecification',
                'dayOfWeek' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opens' => '09:00', 'closes' => '18:00',
            ]],
            'hasCredential' => [
                '@type' => 'EducationalOccupationalCredential',
                'credentialCategory' => 'license',
                'name' => 'Texas Public Adjuster License #' . LICENSE_NO,
                'recognizedBy' => ['@type' => 'GovernmentOrganization', 'name' => 'Texas Department of Insurance'],
            ],
            'founder' => ['@id' => SITE_URL . '/#joseph-dittman'],
            'knowsAbout' => ['Hurricane damage insurance claims', 'Hail damage claims', 'Wind damage claims', 'Water damage claims', 'Fire and smoke damage claims', 'Commercial property claims', 'Denied and underpaid insurance claims', 'Xactimate estimating'],
        ],
        person_schema(),
        [
            '@type' => 'WebSite',
            '@id' => SITE_URL . '/#website',
            'url' => SITE_URL . '/',
            'name' => SITE_NAME,
            'publisher' => ['@id' => SITE_URL . '/#business'],
            'inLanguage' => 'en-US',
        ],
    ];
}

function person_schema(): array {
    return [
        '@type' => 'Person',
        '@id' => SITE_URL . '/#joseph-dittman',
        'name' => AUTHOR['name'],
        'jobTitle' => AUTHOR['title'],
        'url' => SITE_URL . AUTHOR['url'],
        'image' => SITE_URL . AUTHOR['photo'],
        'description' => AUTHOR['short'],
        'worksFor' => ['@id' => SITE_URL . '/#business'],
        'hasCredential' => [
            '@type' => 'EducationalOccupationalCredential',
            'credentialCategory' => 'license',
            'name' => 'Texas Public Adjuster (Rise Public Adjusting LLC, license #' . LICENSE_NO . ')',
            'recognizedBy' => ['@type' => 'GovernmentOrganization', 'name' => 'Texas Department of Insurance'],
        ],
        'knowsAbout' => ['Public adjusting', 'Property insurance claims', 'Texas insurance law', 'Xactimate', 'Matterport 3D documentation'],
        'sameAs' => AUTHOR['sameAs'],
    ];
}

function breadcrumb_schema(array $crumbs): array {
    $items = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function faq_schema(array $faqs): array {
    return ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => [
        '@type' => 'Question', 'name' => $f[0],
        'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f[1])],
    ], $faqs)];
}

/** Render <details> FAQ list. */
function faq_html(array $faqs): string {
    $h = '<div class="faq">';
    foreach ($faqs as [$q, $a]) $h .= '<details><summary>' . e($q) . '</summary><div class="faq-a"><p>' . $a . '</p></div></details>';
    return $h . '</div>';
}

function breadcrumbs_html(array $crumbs): string {
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => [$name, $path]) {
        $h .= $i === $last ? '<li aria-current="page">' . e($name) . '</li>' : '<li><a href="' . e($path) . '">' . e($name) . '</a></li>';
    }
    return $h . '</ol></nav>';
}

/**
 * Opens the page. Keys: title, desc, path, image, type (website|article), schema (extra nodes),
 * crumbs ([[name, path], ...]), noindex, body_class, published, modified, hero (html string, optional).
 */
function page_start(array $p): void {
    global $PAGE;
    $PAGE = $p;
    $canonical = SITE_URL . $p['path'];
    $image = abs_url($p['image'] ?? '/assets/img/houston-public-adjusters-og.jpg');
    $graph = base_schema();
    $graph[] = [
        '@type' => 'WebPage', '@id' => $canonical . '#webpage', 'url' => $canonical,
        'name' => $p['title'], 'description' => $p['desc'], 'isPartOf' => ['@id' => SITE_URL . '/#website'],
        'about' => ['@id' => SITE_URL . '/#business'], 'inLanguage' => 'en-US',
    ];
    if (!empty($p['crumbs'])) $graph[] = breadcrumb_schema($p['crumbs']);
    foreach ($p['schema'] ?? [] as $node) $graph[] = $node;
    $ld = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
    ?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($p['title']) ?></title>
<meta name="description" content="<?= e($p['desc']) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php if (!empty($p['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<?php endif; ?>
<meta name="geo.region" content="US-TX"><meta name="geo.placename" content="Houston">
<meta name="geo.position" content="<?= GEO_LAT ?>;<?= GEO_LNG ?>"><meta name="ICBM" content="<?= GEO_LAT ?>, <?= GEO_LNG ?>">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:type" content="<?= e($p['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($p['title']) ?>">
<meta property="og:description" content="<?= e($p['desc']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<?php if (!empty($p['published'])): ?><meta property="article:published_time" content="<?= e($p['published']) ?>">
<meta property="article:modified_time" content="<?= e($p['modified'] ?? $p['published']) ?>">
<meta property="article:author" content="<?= e(SITE_URL . AUTHOR['url']) ?>">
<meta name="author" content="<?= e(AUTHOR['name']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($p['title']) ?>">
<meta name="twitter:description" content="<?= e($p['desc']) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<meta name="theme-color" content="#13202d">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<script type="application/ld+json"><?= $ld ?></script>
</head>
<body class="<?= e($p['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">
  <div class="wrap topbar-in">
    <span><strong>Free claim review</strong> &middot; No upfront fees &middot; TDI license #<?= LICENSE_NO ?></span>
    <span class="topbar-links"><a href="tel:<?= PHONE_E164 ?>">Call <?= PHONE_DISPLAY ?></a><a href="sms:<?= PHONE_E164 ?>">Text <?= PHONE_DISPLAY ?></a></span>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-in">
    <a class="logo" href="/" aria-label="<?= SITE_NAME ?> home">
      <span class="logo-mark" aria-hidden="true">H</span>
      <span class="logo-text"><strong>Houston</strong><em>Public Adjusters</em></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as [$label, $href]):
        $cur = $href === '/' ? $p['path'] === '/' : str_starts_with($p['path'], $href); ?>
        <li><a href="<?= $href ?>"<?= $cur ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-accent nav-cta" href="tel:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a>
    </nav>
  </div>
</header>
<div id="alert-strip" class="alert-strip" hidden></div>
<main id="main">
<?php
    if (!empty($p['hero'])) echo $p['hero'];
}

/** Compact interior hero with breadcrumbs. */
function page_hero(string $h1, string $lede, array $crumbs, string $eyebrow = ''): string {
    return '<section class="page-hero"><div class="wrap">' . breadcrumbs_html($crumbs)
        . ($eyebrow ? '<p class="eyebrow">' . e($eyebrow) . '</p>' : '')
        . '<h1>' . $h1 . '</h1><p class="lede">' . $lede . '</p>'
        . '<div class="hero-actions"><a class="btn btn-accent" href="tel:' . PHONE_E164 . '">Call ' . PHONE_DISPLAY . '</a>'
        . '<a class="btn btn-ghost-light" href="sms:' . PHONE_E164 . '">Text Us</a>'
        . '<button class="btn btn-ghost-light" type="button" data-open-lead>Free Claim Review</button></div>'
        . '</div></section>';
}

/** Lead form. $id must be unique per page. */
function lead_form(string $id, string $heading = 'Request a Free Claim Review', string $sub = '', bool $compact = false): string {
    ob_start(); ?>
<form class="lead-form<?= $compact ? ' compact' : '' ?>" id="<?= e($id) ?>" action="/submit-lead.php" method="post" novalidate>
  <?php if ($heading): ?><h3><?= e($heading) ?></h3><?php endif; ?>
  <?php if ($sub): ?><p class="form-sub"><?= $sub ?></p><?php endif; ?>
  <div class="field-row">
    <label>Full name<input name="name" autocomplete="name" required maxlength="100"></label>
    <label>Phone<input name="phone" type="tel" autocomplete="tel" required maxlength="30"></label>
  </div>
  <div class="field-row">
    <label>Email<input name="email" type="email" autocomplete="email" required maxlength="120"></label>
    <label>Property ZIP<input name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="10"></label>
  </div>
  <?php if (!$compact): ?>
  <div class="field-row">
    <label>Type of damage
      <select name="damage">
        <option value="">Select one</option>
        <option>Hurricane / wind</option><option>Hail / roof</option><option>Flood / water</option>
        <option>Fire / smoke</option><option>Burst pipe / plumbing</option><option>Freeze</option>
        <option>Theft / vandalism</option><option>Commercial property</option><option>Other</option>
      </select>
    </label>
    <label>Claim status
      <select name="status">
        <option value="">Select one</option>
        <option>Haven't filed yet</option><option>Filed, waiting on insurer</option><option>Underpaid / low offer</option>
        <option>Denied</option><option>Delayed / stalled</option><option>Settled — may reopen</option>
      </select>
    </label>
  </div>
  <label>What happened?<textarea name="message" rows="3" maxlength="3000" placeholder="Date of loss, what was damaged, what your insurer has said so far"></textarea></label>
  <?php endif; ?>
  <label class="hp" aria-hidden="true">Leave blank<input name="website" tabindex="-1" autocomplete="off"></label>
  <input type="hidden" name="ts" value="<?= time() ?>">
  <input type="hidden" name="source" value="">
  <label class="consent"><input type="checkbox" name="consent" value="yes" required> I agree to be contacted by call, text or email about my claim. Msg &amp; data rates may apply. Reply STOP to opt out.</label>
  <button class="btn btn-accent btn-block" type="submit">Get My Free Claim Review</button>
  <p class="form-status" role="status" aria-live="polite"></p>
  <p class="form-note">Prefer to talk? Call or text <a href="tel:<?= PHONE_E164 ?>"><?= PHONE_DISPLAY ?></a>.</p>
</form>
<?php
    return ob_get_clean();
}

function author_box(): string {
    return '<aside class="author-box"><img src="' . AUTHOR['photo'] . '" alt="' . AUTHOR['name'] . ', ' . AUTHOR['title'] . '" width="96" height="96" loading="lazy">'
        . '<div><p class="author-kicker">Written by</p><p class="author-name"><a href="' . AUTHOR['url'] . '" rel="author">' . AUTHOR['name'] . '</a> &middot; ' . AUTHOR['title'] . '</p>'
        . '<p>' . e(AUTHOR['short']) . '</p>'
        . '<p class="author-links"><a href="' . AUTHOR['url'] . '">Full bio</a> &middot; <a href="tel:' . PHONE_E164 . '">Call Joseph: ' . PHONE_DISPLAY . '</a></p></div></aside>';
}

function cta_band(): string {
    return '<section class="cta-band"><div class="wrap cta-in"><div><h2>Property damage? The clock is already ticking.</h2>'
        . '<p>Start with a free consultation from Houston Public Adjusters and protect your claim before mistakes cost you money.</p></div>'
        . '<div class="cta-actions"><a class="btn btn-accent" href="tel:' . PHONE_E164 . '">Call ' . PHONE_DISPLAY . '</a>'
        . '<a class="btn btn-ghost-light" href="sms:' . PHONE_E164 . '">Text ' . PHONE_DISPLAY . '</a></div></div></section>';
}

/** Card grid of blog posts. */
function post_cards(array $slugs): string {
    $h = '<div class="card-grid">';
    foreach ($slugs as $s) {
        $p = POSTS[$s];
        $h .= '<article class="card post-card"><a class="card-img" href="/' . $s . '/"><img src="' . e($p['thumb']) . '" alt="' . e($p['h1']) . '" width="300" height="200" loading="lazy"></a>'
            . '<div class="card-body"><p class="meta">' . date('M j, Y', strtotime($p['published'])) . ' &middot; ' . AUTHOR['name'] . '</p>'
            . '<h3><a href="/' . $s . '/">' . e($p['h1']) . '</a></h3><p>' . e($p['excerpt']) . '</p></div></article>';
    }
    return $h . '</div>';
}

function page_end(bool $cta = true): void {
    global $PAGE;
    if ($cta) echo cta_band();
    $year = date('Y');
    ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="logo logo-light" href="/"><span class="logo-mark" aria-hidden="true">H</span><span class="logo-text"><strong>Houston</strong><em>Public Adjusters</em></span></a>
      <p>Houston Public Adjusters help homeowners and businesses across Greater Houston navigate insurance claims after property damage. Our licensed public adjusters work on your behalf to document losses, challenge low settlements and pursue the full compensation your policy allows.</p>
      <p class="license"><?= LEGAL_NAME ?> &middot; Texas Public Adjuster License #<?= LICENSE_NO ?></p>
    </div>
    <div>
      <h2 class="footer-h">Get Help</h2>
      <ul class="footer-list">
        <li><a href="tel:<?= PHONE_E164 ?>">Call: <?= PHONE_DISPLAY ?></a></li>
        <li><a href="sms:<?= PHONE_E164 ?>">Text: <?= PHONE_DISPLAY ?></a></li>
        <li><a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a></li>
        <li><?= HOURS_TEXT ?></li>
        <li>Serving Houston and surrounding areas</li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Explore</h2>
      <ul class="footer-list">
        <li><a href="/services/">Claim Services</a></li>
        <li><a href="/service-areas/">Service Areas</a></li>
        <li><a href="/tools/">Claim Calculators</a></li>
        <li><a href="/houston-weather/">Live Houston Weather</a></li>
        <li><a href="/houston-storm-history/">Houston Storm History</a></li>
        <li><a href="/hurricane-preparedness-checklist/">Hurricane Checklist</a></li>
        <li><a href="/insurance-claim-glossary/">Claim Glossary</a></li>
        <li><a href="/faq/">FAQ</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Company</h2>
      <ul class="footer-list">
        <li><a href="/">Home</a></li>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="<?= AUTHOR['url'] ?>">Joseph Dittman</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>&copy; <?= $year ?> <?= SITE_NAME ?>. All rights reserved. Houston Public Adjusters is operated by <?= LEGAL_NAME ?>. We are public adjusters, not attorneys, and nothing on this site is legal advice.</p>
  </div>
</footer>
<div class="mobile-bar"><a href="tel:<?= PHONE_E164 ?>">Call</a><a href="sms:<?= PHONE_E164 ?>">Text</a><button type="button" data-open-lead>Free Review</button></div>
<?php if (empty($PAGE['no_popup'])): ?>
<div class="lead-modal" id="lead-modal" role="dialog" aria-modal="true" aria-labelledby="lead-modal-title" hidden>
  <div class="lead-modal-box">
    <button class="lead-close" type="button" aria-label="Close">&times;</button>
    <div class="lead-modal-head">
      <img src="<?= AUTHOR['photo'] ?>" alt="" width="64" height="64">
      <div><p class="eyebrow">Free, no-obligation claim review</p>
      <h2 id="lead-modal-title">Was your claim denied, delayed or underpaid?</h2></div>
    </div>
    <p>Tell us what happened and a licensed Houston public adjuster will call you back. No upfront fees &mdash; we only get paid if we recover for you.</p>
    <?= lead_form('lead-popup', '', '', true) ?>
  </div>
</div>
<?php endif; ?>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
<?php foreach ($PAGE['scripts'] ?? [] as $s): ?><script src="<?= asset($s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}
