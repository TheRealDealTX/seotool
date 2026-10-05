<?php
// Shared helpers and the page layout.

const APP = __DIR__;

function cfg($key = null) {
    static $c;
    $c ??= require APP . '/config.php';
    return $key === null ? $c : ($c[$key] ?? null);
}

function data($name) {
    static $cache = [];
    return $cache[$name] ??= json_decode(file_get_contents(APP . "/data/$name.json"), true);
}

function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function abs_url($path) { return rtrim(cfg('origin'), '/') . $path; }

function listings() { return data('listings'); }
function bases() { return data('bases'); }
function posts() { return data('posts'); }

function listing($slug) {
    foreach (listings() as $l) if ($l['slug'] === $slug) return $l;
    return null;
}
function base($slug) {
    foreach (bases() as $b) if ($b['slug'] === $slug) return $b;
    return null;
}
function post($slug) {
    foreach (posts() as $p) if ($p['slug'] === $slug) return $p;
    return null;
}
function listings_for_base($slug) {
    return array_values(array_filter(listings(), fn($l) => $l['base'] === $slug));
}
function newest_listings($n = 6) {
    $l = listings();
    usort($l, fn($a, $b) => strcmp($b['date'], $a['date']));
    return array_slice($l, 0, $n);
}

function fmt_num($n) {
    if ($n === null) return '';
    return (floor($n) == $n) ? number_format($n) : rtrim(rtrim(number_format($n, 1), '0'), '.');
}
function price_label($l) { return $l['price'] ? '$' . number_format($l['price']) . '/mo' : 'BAH-based rent'; }
function fmt_date($d) { return date('F j, Y', strtotime($d)); }
function listing_image($l) {
    return $l['images'][0] ?? ['src' => cfg('og_image'), 'alt' => $l['title']];
}
function city_state($l) {
    $parts = array_map('trim', explode(',', $l['address']));
    return count($parts) >= 3 ? $parts[count($parts) - 2] . ', ' . preg_replace('/\s*\d{5}.*/', '', end($parts)) : $l['address'];
}

// Lucide-style inline icons (stroke icons, 24x24 viewBox).
function icon($name, $cls = '') {
    static $p = [
        'bed' => '<path d="M2 4v16"/><path d="M2 8h18a2 2 0 0 1 2 2v10"/><path d="M2 17h20"/><path d="M6 8v9"/>',
        'bath' => '<path d="M9 6 6.5 3.5a1.5 1.5 0 0 0-1-.5C4.68 3 4 3.68 4 4.5V17a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/><line x1="10" x2="8" y1="5" y2="7"/><line x1="2" x2="22" y1="12" y2="12"/><line x1="7" x2="7" y1="19" y2="21"/><line x1="17" x2="17" y1="19" y2="21"/>',
        'ruler' => '<path d="M21.3 15.3a2.4 2.4 0 0 1 0 3.4l-2.6 2.6a2.4 2.4 0 0 1-3.4 0L2.7 8.7a2.41 2.41 0 0 1 0-3.4l2.6-2.6a2.41 2.41 0 0 1 3.4 0Z"/><path d="m14.5 12.5 2-2"/><path d="m11.5 9.5 2-2"/><path d="m8.5 6.5 2-2"/><path d="m17.5 15.5 2-2"/>',
        'pin' => '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
        'phone' => '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
        'globe' => '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
        'heart' => '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
        'search' => '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
        'map' => '<polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/><line x1="9" x2="9" y1="3" y2="18"/><line x1="15" x2="15" y1="6" y2="21"/>',
        'grid' => '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>',
        'sun' => '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
        'moon' => '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
        'menu' => '<line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/>',
        'x' => '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
        'arrow' => '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
        'check' => '<path d="M20 6 9 17l-5-5"/>',
        'shield' => '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
        'home' => '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
        'calc' => '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8" x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path d="M16 10h.01"/><path d="M12 10h.01"/><path d="M8 10h.01"/><path d="M12 14h.01"/><path d="M8 14h.01"/><path d="M12 18h.01"/><path d="M8 18h.01"/>',
        'calendar' => '<rect width="18" height="18" x="3" y="4" rx="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/>',
        'paw' => '<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z"/>',
        'users' => '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
        'school' => '<path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
        'bolt' => '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
        'clock' => '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
        'mail' => '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
        'share' => '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/>',
        'building' => '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
        'star' => '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>',
        'image' => '<rect width="18" height="18" x="3" y="3" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.09-3.09a2 2 0 0 0-2.82 0L6 21"/>',
        'list' => '<line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/>',
    ];
    $c = $cls ? " class=\"icon $cls\"" : ' class="icon"';
    return "<svg$c viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\">" . ($p[$name] ?? '') . '</svg>';
}

// ---------------------------------------------------------------- layout

function layout_start(array $page) {
    $c = cfg();
    $title = $page['title'] ?? $c['name'];
    $full = $page['full_title'] ?? ($title . ' | ' . $c['name']);
    $desc = $page['description'] ?? $c['tagline'];
    $canonical = abs_url($page['path'] ?? '/');
    $og = abs_url($page['image'] ?? $c['og_image']);
    $type = $page['og_type'] ?? 'website';
    $robots = $page['robots'] ?? 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1';
    $current = $page['nav'] ?? ($page['path'] ?? '/');
    $schema = json_encode(array_merge([
        '@context' => 'https://schema.org',
    ], ['@graph' => array_merge([site_schema()], $page['schema'] ?? [])]), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    ?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($full) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($type) ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:site_name" content="<?= e($c['name']) ?>">
<meta property="og:image" content="<?= e($og) ?>">
<meta name="twitter:card" content="summary_large_image">
<?= $page['head_extra'] ?? '' ?>
<meta name="theme-color" content="#0b1f3a">
<link rel="icon" href="<?= e(str_replace('.webp', '-32x32.webp', $c['icon'])) ?>" sizes="32x32">
<link rel="icon" href="<?= e(str_replace('.webp', '-192x192.webp', $c['icon'])) ?>" sizes="192x192">
<link rel="apple-touch-icon" href="<?= e(str_replace('.webp', '-180x180.webp', $c['icon'])) ?>">
<link rel="alternate" type="application/rss+xml" title="<?= e($c['name']) ?> Feed" href="/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= asset_ver('css/site.css') ?>">
<?php if (!empty($page['leaflet'])): ?>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<?php endif; ?>
<script>try{var t=localStorage.getItem('mhr-theme');if(t)document.documentElement.dataset.theme=t}catch(e){}</script>
<script defer src="/assets/js/site.js?v=<?= asset_ver('js/site.js') ?>"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= e($c['ga_ids'][0]) ?>"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());<?php foreach ($c['ga_ids'] as $id) echo "gtag('config','" . e($id) . "');"; ?></script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=<?= e($c['adsense']) ?>" crossorigin="anonymous"></script>
<script type="application/ld+json"><?= $schema ?></script>
</head>
<body class="<?= e($page['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<?php if (!empty($page['progress'])): ?><div class="progress" aria-hidden="true"><span></span></div><?php endif; ?>
<header class="site-header" data-header>
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= e($c['name']) ?> home">
      <img class="logo-dark-bg" src="/assets/img/logo-light.webp" alt="<?= e($c['name']) ?>" width="150" height="70">
      <img class="logo-light-bg" src="/assets/img/logo.webp" alt="<?= e($c['name']) ?>" width="150" height="70">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <?php foreach ($c['nav'] as $href => $label):
        $active = ($href === '/' ? $current === '/' : str_starts_with($current, $href)); ?>
        <a href="<?= e($href) ?>"<?= $active ? ' aria-current="page"' : '' ?>><?= e($label) ?></a>
      <?php endforeach; ?>
      <a class="btn btn-sm btn-accent nav-cta" href="/submit-property/">Submit Property</a>
    </nav>
    <div class="header-tools">
      <a class="icon-btn saved-link" href="/properties/?saved=1" aria-label="Saved listings" title="Saved listings"><?= icon('heart') ?><span class="badge" data-saved-count hidden>0</span></a>
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle dark mode"><?= icon('moon', 'i-moon') ?><?= icon('sun', 'i-sun') ?></button>
      <button class="icon-btn menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" data-menu aria-label="Menu"><?= icon('menu', 'i-open') ?><?= icon('x', 'i-close') ?></button>
    </div>
  </div>
</header>
<main id="main">
<?php
}

function asset_ver($rel) {
    $f = dirname(APP) . '/assets/' . $rel;
    return is_file($f) ? substr(md5_file($f), 0, 8) : '1';
}

function layout_end() {
    $c = cfg();
    ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="/assets/img/logo-light.webp" alt="<?= e($c['name']) ?>" width="150" height="70" loading="lazy">
      <p><?= e($c['tagline']) ?>. A directory of on-base and military-friendly rental housing for service members and their families.</p>
      <div class="social">
        <?php foreach ($c['social'] as $n => $u): ?><a href="<?= e($u) ?>" target="_blank" rel="noopener"><?= e($n) ?></a><?php endforeach; ?>
      </div>
    </div>
    <div>
      <h3>Military Bases</h3>
      <ul><?php foreach (bases() as $b): ?><li><a href="/bases/<?= e($b['slug']) ?>/"><?= e($b['name']) ?></a></li><?php endforeach; ?></ul>
    </div>
    <div>
      <h3>Recently Listed</h3>
      <ul><?php foreach (newest_listings(5) as $l): ?><li><a href="/properties/<?= e($l['slug']) ?>/"><?= e($l['title']) ?></a></li><?php endforeach; ?></ul>
    </div>
    <div>
      <h3>Site</h3>
      <ul>
        <li><a href="/properties/">All Listings</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/submit-property/">Submit a Property</a></li>
        <li><a href="/contact-us/">Contact Us</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
      </ul>
      <p class="footer-contact"><a href="<?= e($c['phone_href']) ?>"><?= icon('phone') ?> <?= e($c['phone']) ?></a><br><a href="mailto:<?= e($c['email']) ?>"><?= icon('mail') ?> <?= e($c['email']) ?></a></p>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>Copyright &copy; <?= date('Y') ?> <?= e($c['name']) ?>. All rights reserved.</p>
    <p class="muted">Not affiliated with the Department of Defense or any military housing company. Verify availability, eligibility and rent with each community. As an Amazon Associate we earn from qualifying purchases.</p>
  </div>
</footer>
<div class="toast" role="status" aria-live="polite" data-toast></div>
</body>
</html>
<?php
}

function site_schema() {
    $c = cfg();
    return [
        '@type' => 'Organization', '@id' => abs_url('/#organization'), 'name' => $c['name'], 'url' => abs_url('/'),
        'logo' => abs_url($c['logo']), 'email' => $c['email'], 'telephone' => $c['phone'],
        'sameAs' => array_values($c['social']),
    ];
}

function breadcrumbs(array $items) {
    // $items: [[label, path|null], ...]
    $html = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $schema = [];
    foreach ($items as $i => [$label, $path]) {
        $html .= '<li>' . ($path ? '<a href="' . e($path) . '">' . e($label) . '</a>' : '<span aria-current="page">' . e($label) . '</span>') . '</li>';
        $schema[] = array_filter(['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => $path ? abs_url($path) : null]);
    }
    return [$html . '</ol></nav>', ['@type' => 'BreadcrumbList', 'itemListElement' => $schema]];
}

function listing_card($l, $extra_class = '') {
    $b = base($l['base']);
    $img = listing_image($l);
    $data = [
        'slug' => $l['slug'], 'base' => $l['base'], 'beds' => $l['beds'] ?? 0, 'baths' => $l['baths'] ?? 0,
        'sqft' => $l['sqft'] ?? 0, 'date' => $l['date'], 'branch' => strtolower($b['branch'] ?? ''),
        'q' => strtolower($l['title'] . ' ' . $l['address'] . ' ' . ($b['name'] ?? '') . ' ' . ($l['operator'] ?? '') . ' ' . implode(' ', $l['amenities'])),
        'pets' => !empty($l['pets']) ? 1 : 0,
    ];
    $attrs = '';
    foreach ($data as $k => $v) $attrs .= ' data-' . $k . '="' . e($v) . '"';
    ob_start(); ?>
<article class="card listing-card <?= e($extra_class) ?>"<?= $attrs ?>>
  <a class="card-media" href="/properties/<?= e($l['slug']) ?>/" tabindex="-1" aria-hidden="true">
    <img src="<?= e($img['src']) ?>" alt="" loading="lazy" width="600" height="400">
    <span class="chip chip-dark"><?= e($b['short'] ?? '') ?></span>
    <?php if (!empty($l['featured'])): ?><span class="chip chip-accent chip-right"><?= icon('star') ?> Featured</span><?php endif; ?>
  </a>
  <button class="fav-btn" type="button" data-fav="<?= e($l['slug']) ?>" aria-pressed="false" aria-label="Save <?= e($l['title']) ?>"><?= icon('heart') ?></button>
  <div class="card-body">
    <p class="card-price"><?= e(price_label($l)) ?></p>
    <h3 class="card-title"><a href="/properties/<?= e($l['slug']) ?>/"><?= e($l['title']) ?></a></h3>
    <p class="card-addr"><?= icon('pin') ?> <?= e($l['address']) ?></p>
    <ul class="facts">
      <?php if ($l['beds']): ?><li><?= icon('bed') ?> <?= e($l['beds_range'] ?: fmt_num($l['beds'])) ?> bd</li><?php endif; ?>
      <?php if ($l['baths']): ?><li><?= icon('bath') ?> <?= e($l['baths_range'] ?? '' ?: fmt_num($l['baths'])) ?> ba</li><?php endif; ?>
      <?php if ($l['sqft'] || $l['sqft_range']): ?><li><?= icon('ruler') ?> <?= e($l['sqft_range'] ?: fmt_num($l['sqft'])) ?> sq ft</li><?php endif; ?>
    </ul>
  </div>
</article>
<?php
    return ob_get_clean();
}

function post_card($p) {
    ob_start(); ?>
<article class="card post-card">
  <a class="card-media" href="/<?= e($p['slug']) ?>/" tabindex="-1" aria-hidden="true">
    <img src="<?= e($p['image']['src'] ?? cfg('og_image')) ?>" alt="" loading="lazy" width="600" height="400">
  </a>
  <div class="card-body">
    <p class="card-meta"><?= e(fmt_date($p['date'])) ?> &middot; <?= e(reading_time($p['slug'])) ?> min read</p>
    <h3 class="card-title"><a href="/<?= e($p['slug']) ?>/"><?= e($p['title']) ?></a></h3>
    <p class="card-excerpt"><?= e(mb_strimwidth($p['excerpt'], 0, 150, '…')) ?></p>
  </div>
</article>
<?php
    return ob_get_clean();
}

function post_html($slug) {
    $f = APP . "/data/posts/$slug.html";
    return is_file($f) ? file_get_contents($f) : '';
}
function reading_time($slug) {
    return max(1, (int)round(str_word_count(strip_tags(post_html($slug))) / 225));
}

function not_found() {
    http_response_code(404);
    require APP . '/views/404.php';
    exit;
}

function redirect($to, $code = 301) {
    header('Location: ' . $to, true, $code);
    exit;
}

function csrf_token() {
    if (session_status() !== PHP_SESSION_ACTIVE) session_start();
    return $_SESSION['csrf'] ??= bin2hex(random_bytes(16));
}

require APP . '/views/partials.php';
