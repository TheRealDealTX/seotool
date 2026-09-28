<?php
// Shared layout: <head>, header, banners, footer, popup, lead form, icons.

function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

function phone_link($class = '', $label = null) {
    return '<a class="' . e($class) . '" href="tel:' . PHONE_TEL . '">' . ($label ?? e(PHONE)) . '</a>';
}

function icon($name, $size = 24) {
    $p = [
        'phone'  => '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
        'wind'   => '<path d="M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/>',
        'fire'   => '<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.4 1.3 1.4 2.3 2.5 2.8z"/>',
        'water'  => '<path d="M12 2.7s-6 6.6-6 11.3a6 6 0 0 0 12 0c0-4.7-6-11.3-6-11.3z"/>',
        'shield' => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
        'file'   => '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5z"/><path d="M14 2v6h6"/><path d="M16 13H8M16 17H8M10 9H8"/>',
        'scale'  => '<path d="m16 16 3-8 3 8c-.9.7-1.9 1-3 1s-2.1-.3-3-1z"/><path d="m2 16 3-8 3 8c-.9.7-1.9 1-3 1s-2.1-.3-3-1z"/><path d="M7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
        'home'   => '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
        'check'  => '<path d="M20 6 9 17l-5-5"/>',
        'x'      => '<path d="M18 6 6 18M6 6l12 12"/>',
        'clock'  => '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        'search' => '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        'dollar' => '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
        'alert'  => '<path d="m21.7 18-8-14a2 2 0 0 0-3.5 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3z"/><path d="M12 9v4M12 17h.01"/>',
        'hurricane' => '<path d="M12 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/><path d="M13 5.1C9.3 4.4 5.6 6.8 5 10.5c-.3 1.9.2 3.8 1.4 5.3"/><path d="M11 18.9c3.7.7 7.4-1.7 8-5.4.3-1.9-.2-3.8-1.4-5.3"/><path d="M7 4c1.6-1 3.6-1.3 6-1M17 20c-1.6 1-3.6 1.3-6 1"/>',
        'building' => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
        'calc'   => '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M8 6h8M16 14v4M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M8 18h.01M12 18h.01"/>',
        'user'   => '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
        'arrow'  => '<path d="M5 12h14M12 5l7 7-7 7"/>',
        'star'   => '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8-6.2-3.2-6.2 3.2L7 14.2 2 9.3l6.9-1z"/>',
    ][$name] ?? '';
    return '<svg class="ico" width="' . $size . '" height="' . $size . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' . $p . '</svg>';
}

function logo_svg() {
    return '<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1f8fc4"/><stop offset="1" stop-color="#0b2540"/></linearGradient></defs>'
        . '<path d="M24 3 42 9v14c0 11-8 19-18 22C14 42 6 34 6 23V9z" fill="url(#lg)"/>'
        . '<path d="M13 26c3-3 6-3 9 0s6 3 9 0 4-2 5-1" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
        . '<path d="M13 32c3-3 6-3 9 0s6 3 9 0 4-2 5-1" stroke="#f97316" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
        . '<path d="m16 19 8-7 8 7" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';
}

function business_schema() {
    return [
        '@type' => ['LocalBusiness', 'ProfessionalService'],
        '@id' => SITE_URL . '/#business',
        'name' => SITE_NAME,
        'url' => SITE_URL . '/',
        'telephone' => PHONE_TEL,
        'email' => LEAD_EMAIL,
        'image' => SITE_URL . '/assets/img/og.png',
        'logo' => SITE_URL . '/assets/img/logo.svg',
        'description' => 'Licensed Texas public adjuster for Galveston County homeowners and businesses: TWIA windstorm, hurricane, fire, flood and denied or underpaid property insurance claims.',
        'legalName' => FIRM,
        'identifier' => ['@type' => 'PropertyValue', 'name' => 'Texas Department of Insurance license', 'value' => LICENSE_NO],
        'address' => ['@type' => 'PostalAddress', 'streetAddress' => STREET, 'addressLocality' => ADDR_CITY, 'addressRegion' => REGION, 'postalCode' => ZIP, 'addressCountry' => 'US'],
        'openingHours' => 'Mo-Fr 09:00-18:00',
        'sameAs' => [SISTER_SITE],
        'geo' => ['@type' => 'GeoCoordinates', 'latitude' => GEO_LAT, 'longitude' => GEO_LNG],
        'areaServed' => array_map(fn($a) => ['@type' => 'Place', 'name' => "$a, TX"], AREAS),
        'founder' => ['@type' => 'Person', 'name' => AUTHOR, 'jobTitle' => AUTHOR_ROLE, 'image' => SITE_URL . AUTHOR_PHOTO],
        'priceRange' => 'Contingency fee — no recovery, no fee',
    ];
}

/**
 * $m keys: title, description, path, h1 (unused here), schema (array of extra nodes), og_type, noindex
 */
function render_page(array $m, string $body) {
    $path = $m['path'] ?? '/';
    $canon = SITE_URL . $path;
    $graph = array_merge([business_schema(), [
        '@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'url' => SITE_URL . '/', 'name' => SITE_NAME,
        'publisher' => ['@id' => SITE_URL . '/#business'],
    ]], $m['schema'] ?? []);
    if ($path !== '/') {
        $graph[] = ['@type' => 'BreadcrumbList', 'itemListElement' => [
            ['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => SITE_URL . '/'],
            ['@type' => 'ListItem', 'position' => 2, 'name' => $m['crumb'] ?? $m['title'], 'item' => $canon],
        ]];
    }
    $ld = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
    header('Content-Type: text/html; charset=utf-8');
    ?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($m['title']) ?></title>
<meta name="description" content="<?= e($m['description']) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<?php if (!empty($m['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php endif ?>
<meta property="og:type" content="<?= e($m['og_type'] ?? 'website') ?>">
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:title" content="<?= e($m['title']) ?>">
<meta property="og:description" content="<?= e($m['description']) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:image" content="<?= SITE_URL ?>/assets/img/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b2540">
<link rel="icon" href="/assets/img/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= @filemtime(ROOT . '/assets/css/site.css') ?>">
<script type="application/ld+json"><?= $ld ?></script>
</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">
  <div class="wrap topbar-in">
    <span><?= icon('alert', 16) ?> Storm, fire or TWIA claim denied or underpaid? <strong>Call for an expert consultation</strong></span>
    <?= phone_link('topbar-phone', icon('phone', 16) . ' ' . PHONE) ?>
  </div>
</div>
<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="/" aria-label="<?= SITE_NAME ?> home"><?= logo_svg() ?><span><strong>Galveston</strong> Public Adjuster<small>TWIA · Hurricane · Fire · Flood</small></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Menu"><span></span><span></span><span></span></button>
    <nav id="nav" class="nav" aria-label="Main">
      <?php foreach (NAV as $href => $label): ?><a href="<?= $href ?>"<?= $href === $path || ($href === '/blog/' && str_starts_with($path, '/blog/')) ? ' aria-current="page"' : '' ?>><?= e($label) ?></a><?php endforeach ?>
      <?= phone_link('btn btn-cta nav-call', icon('phone', 18) . ' Call Now') ?>
    </nav>
  </div>
</header>
<main id="main">
<?= $body ?>
</main>
<?= cta_band() ?>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="brand brand-light" href="/"><?= logo_svg() ?><span><strong>Galveston</strong> Public Adjuster<small>TWIA · Hurricane · Fire · Flood</small></span></a>
      <p>Licensed Texas public adjusting for Galveston Island and all of Galveston County. We represent policyholders — never insurance companies.</p>
      <p class="foot-phone"><?= phone_link('', icon('phone', 18) . ' ' . PHONE) ?></p>
      <p><a href="mailto:<?= LEAD_EMAIL ?>"><?= LEAD_EMAIL ?></a></p>
      <p class="small"><?= FIRM ?> · TX License #<?= LICENSE_NO ?><br><?= STREET ?>, <?= ADDR_CITY ?>, TX <?= ZIP ?><br>Office hours: <?= HOURS ?></p>
    </div>
    <div>
      <h3>Claims We Handle</h3>
      <ul>
        <li><a href="/twia-claims-expert/">TWIA Windstorm Claims</a></li>
        <li><a href="/galveston-fire-claims/">Galveston Fire &amp; Smoke Claims</a></li>
        <li><a href="/#claims">Hurricane &amp; Wind Damage</a></li>
        <li><a href="/#claims">Flood &amp; Water Damage</a></li>
        <li><a href="/#claims">Denied &amp; Underpaid Claims</a></li>
        <li><a href="/#claims">Commercial Property Claims</a></li>
      </ul>
    </div>
    <div>
      <h3>Resources</h3>
      <ul>
        <li><a href="/calculators/">Shingle Wind &amp; Claim Calculators</a></li>
        <li><a href="/texas-windstorm-rules/">Texas Windstorm Rules</a></li>
        <li><a href="/galveston-local-code/">Galveston Local Code</a></li>
        <li><a href="/galveston-storm-history/">Galveston Storm History</a></li>
        <li><a href="/weather-events/">Weather Events (70+ mph)</a></li>
        <li><a href="/blog/">Claim Guides &amp; Blog</a></li>
      </ul>
    </div>
    <div>
      <h3>Service Area</h3>
      <p class="areas"><?= e(implode(' · ', AREAS)) ?></p>
      <a class="btn btn-cta" href="/contact/">Free Claim Review <?= icon('arrow', 18) ?></a>
    </div>
  </div>
  <div class="wrap footer-legal">
    <p>© <?= date('Y') ?> <?= SITE_NAME ?>, a service of <?= FIRM ?>, Texas public adjuster license #<?= LICENSE_NO ?>, <?= STREET ?>, <?= ADDR_CITY ?>, TX <?= ZIP ?>. Public adjusters are licensed by the Texas Department of Insurance. We are not a law firm and do not provide legal advice. Information on this site is general and educational; always read your own policy. <a href="/privacy-policy/">Privacy Policy</a> · <a href="/contact/">Contact</a></p>
  </div>
</footer>
<div class="callbar"><?= phone_link('callbar-btn', icon('phone', 20) . ' Call ' . PHONE) ?><a class="callbar-btn alt" href="/contact/">Free Review</a></div>
<div class="modal" id="lead-modal" role="dialog" aria-modal="true" aria-labelledby="modal-title" hidden>
  <div class="modal-card">
    <button class="modal-x" type="button" aria-label="Close" data-close><?= icon('x', 22) ?></button>
    <div class="modal-head">
      <span class="pill"><?= icon('shield', 16) ?> Free · No obligation</span>
      <h2 id="modal-title">Is your insurance company paying what your claim is worth?</h2>
      <p>Talk to a Galveston public adjuster today. Call for an expert consultation: <?= phone_link('strong-link') ?></p>
    </div>
    <?= lead_form('popup', true) ?>
    <p class="small muted center" style="margin:-14px 0 18px"><?= FIRM ?> · TX License #<?= LICENSE_NO ?></p>
  </div>
</div>
<script src="/assets/js/site.js?v=<?= @filemtime(ROOT . '/assets/js/site.js') ?>" defer></script>
</body>
</html>
<?php
}

function lead_form($source = 'page', $compact = false) {
    static $n = 0; $n++;
    $id = 'f' . $n;
    ob_start(); ?>
<form class="lead-form<?= $compact ? ' compact' : '' ?>" method="post" action="/api/lead.php" data-lead>
  <input type="hidden" name="source" value="<?= e($source) ?>">
  <input type="hidden" name="page" value="">
  <div class="hp" aria-hidden="true"><label>Leave blank<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <div class="grid2">
    <label for="<?= $id ?>n">Name<input id="<?= $id ?>n" name="name" required autocomplete="name"></label>
    <label for="<?= $id ?>p">Phone<input id="<?= $id ?>p" name="phone" type="tel" required autocomplete="tel"></label>
  </div>
  <?php if (!$compact): ?>
  <div class="grid2">
    <label for="<?= $id ?>e">Email<input id="<?= $id ?>e" name="email" type="email" autocomplete="email"></label>
    <label for="<?= $id ?>a">Property address / city<input id="<?= $id ?>a" name="address" autocomplete="street-address"></label>
  </div>
  <?php endif ?>
  <div class="grid2">
    <label for="<?= $id ?>t">Claim type
      <select id="<?= $id ?>t" name="claim_type">
        <option>TWIA / windstorm</option><option>Hurricane damage</option><option>Fire or smoke</option>
        <option>Flood or water</option><option>Roof / hail</option><option>Denied or underpaid claim</option>
        <option>Commercial property</option><option>Other</option>
      </select></label>
    <label for="<?= $id ?>s">Claim status
      <select id="<?= $id ?>s" name="status">
        <option>Haven't filed yet</option><option>Filed — waiting</option><option>Offer seems too low</option>
        <option>Claim denied</option><option>Need to reopen / supplement</option>
      </select></label>
  </div>
  <?php if (!$compact): ?>
  <label for="<?= $id ?>m">What happened?<textarea id="<?= $id ?>m" name="message" rows="3" placeholder="Date of loss, insurance carrier, what's damaged…"></textarea></label>
  <?php endif ?>
  <button class="btn btn-cta btn-block" type="submit"><?= icon('shield', 18) ?> Get My Free Claim Review</button>
  <p class="form-note">Prefer to talk? <?= phone_link('', PHONE) ?> — no fee unless we recover.</p>
  <p class="form-status" role="status" aria-live="polite"></p>
</form>
<?php return ob_get_clean();
}

function cta_band() {
    return '<section class="cta-band"><div class="wrap cta-band-in">'
        . '<div><h2>Don\'t settle for the first offer.</h2><p>Every claim is reviewed personally by ' . AUTHOR . ', licensed Texas public adjuster. Call for an expert consultation.</p></div>'
        . '<div class="cta-band-actions">' . phone_link('btn btn-cta btn-lg', icon('phone', 20) . ' ' . PHONE) . '<a class="btn btn-ghost btn-lg" href="/contact/">Request a Free Review</a></div>'
        . '</div></section>';
}

function banner($text, $sub = '') {
    return '<aside class="banner"><div class="banner-in">' . icon('phone', 28)
        . '<div><strong>' . $text . '</strong>' . ($sub ? '<span>' . $sub . '</span>' : '') . '</div>'
        . phone_link('btn btn-cta', 'Call ' . PHONE) . '</div></aside>';
}

function page_hero($eyebrow, $h1, $lede, $art = '') {
    return '<section class="hero hero-sub"><div class="wrap hero-grid"><div class="hero-copy">'
        . '<span class="eyebrow">' . $eyebrow . '</span><h1>' . $h1 . '</h1><p class="lede">' . $lede . '</p>'
        . '<div class="hero-actions">' . phone_link('btn btn-cta btn-lg', icon('phone', 20) . ' ' . PHONE) . '<a class="btn btn-ghost btn-lg" href="/contact/">Free Claim Review</a></div>'
        . '</div>' . ($art ? '<div class="hero-art">' . $art . '</div>' : '') . '</div>' . wave_divider() . '</section>';
}

function wave_divider() {
    return '<svg class="wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40c120 30 240 30 360 0s240-30 360 0 240 30 360 0 240-30 360 0v40H0z" fill="currentColor"/></svg>';
}

function faq_block(array $faqs, &$schema) {
    $schema[] = ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => [
        '@type' => 'Question', 'name' => $f[0], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f[1])],
    ], $faqs)];
    $h = '<div class="faq">';
    foreach ($faqs as $f) $h .= '<details><summary>' . e($f[0]) . '</summary><div>' . $f[1] . '</div></details>';
    return $h . '</div>';
}

function post_card($p, $i = 0) {
    $cats = ['TWIA & Windstorm' => ['wind', 0], 'Fire & Smoke' => ['fire', 1], 'Flood & Water' => ['water', 2], 'Denied & Underpaid' => ['alert', 3], 'Claim Process' => ['file', 4]];
    [$ico, $c] = $cats[$p['category']] ?? ['file', 4];
    $url = '/blog/' . e($p['slug']) . '/';
    return '<article class="card post-card reveal"><a class="thumb c' . $c . '" href="' . $url . '" aria-hidden="true" tabindex="-1">' . icon($ico, 56) . '</a>'
        . '<div class="body"><div class="post-meta"><span class="tag">' . e($p['category']) . '</span><span>' . fmt_date($p['date']) . '</span><span>' . (int)$p['read_minutes'] . ' min read</span></div>'
        . '<h3><a href="' . $url . '">' . e($p['title']) . '</a></h3><p>' . e($p['description']) . '</p>'
        . '<a class="more" href="' . $url . '" style="margin-top:auto">Read the guide ' . icon('arrow', 16) . '</a></div></article>';
}
