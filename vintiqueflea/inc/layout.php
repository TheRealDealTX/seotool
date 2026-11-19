<?php
defined('INC') || exit;
/** Shared helpers, page head/header/footer. */

function e(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function abs_url(string $path): string
{
    return SITE_URL . $path;
}

/** ASIN for a product: explicit 'asin', else the researched match in inc/asins.php. */
function product_asin(array $p): ?string
{
    if (!empty($p['asin'])) {
        return $p['asin'];
    }
    $k = 'q:' . strtolower(trim($p['q'] ?? $p['name']));
    return defined('PRODUCT_ASINS') ? (PRODUCT_ASINS[$k] ?? null) : null;
}

function amazon_url(array $p): string
{
    if (function_exists('amazon_item') && ($hit = amazon_item($p))) {
        return $hit['url'];
    }
    if ($asin = product_asin($p)) {
        $p['asin'] = $asin;
    }
    if (!empty($p['asin'])) {
        return 'https://www.amazon.com/dp/' . rawurlencode($p['asin']) . '/?tag=' . AMAZON_TAG;
    }
    return 'https://www.amazon.com/s?k=' . rawurlencode($p['q']) . '&tag=' . AMAZON_TAG;
}

function amazon_link(array $p, string $label, string $class = ''): string
{
    return '<a class="' . e($class) . '" href="' . e(amazon_url($p)) . '" target="_blank" rel="sponsored nofollow noopener">' . $label . '</a>';
}

/** Responsive <img> for a self-hosted photo. */
function photo(string $name, string $alt, string $class = '', bool $eager = false, string $sizes = '(max-width: 800px) 100vw, 800px'): string
{
    if (!isset(PHOTOS[$name])) {
        return '';
    }
    [$w, $h] = PHOTOS[$name];
    $b = '/assets/img/photos/' . rawurlencode($name);
    return '<img class="' . e($class) . '" src="' . $b . '-1600.webp" srcset="' . $b . '-800.webp 800w, ' . $b . '-1600.webp ' . $w . 'w" sizes="' . e($sizes) . '" width="' . $w . '" height="' . $h . '" alt="' . e($alt) . '"'
        . ($eager ? ' fetchpriority="high"' : ' loading="lazy"') . ' decoding="async">';
}

function photo_url(string $name): string
{
    return isset(PHOTOS[$name]) ? SITE_URL . '/assets/img/photos/' . rawurlencode($name) . '-1600.webp' : SITE_URL . '/assets/img/og-image.png';
}

function product_card(array $p): string
{
    $tier = $p['tier'] ?? '';
    $icon = $p['icon'] ?? '🛍️';
    $tierLabel = ['$' => 'Under $50', '$$' => '$50–$250', '$$$' => '$250+'][$tier] ?? '';
    $hit = function_exists('amazon_item') ? amazon_item($p) : null;
    if ($hit) {
        $p['img'] = $hit['img'];
    }
    $h = '<article class="product' . ($hit ? ' product--amazon' : '') . '">';
    $h .= !empty($p['img'])
        ? amazon_link($p, '<img src="' . e($p['img']) . '" alt="' . e($hit['title'] ?? $p['name']) . '" loading="lazy" decoding="async"' . ($hit ? ' width="' . (int) $hit['w'] . '" height="' . (int) $hit['h'] . '"' : '') . '>', 'product__art product__art--img')
        : '<div class="product__art' . (!empty($p['bg']) && isset(PHOTOS[$p['bg']]) ? ' product__art--photo" style="background-image:url(/assets/img/photos/' . rawurlencode($p['bg']) . '-800.webp)' : '') . '" aria-hidden="true"><span class="product__icon">' . $icon . '</span></div>';
    $h .= '<div class="product__body"><h3 class="product__name">' . e($p['name']) . '</h3>';
    $h .= '<p class="product__note">' . e($p['note'] ?? '') . '</p>';
    $h .= '<div class="product__foot">';
    if ($tierLabel) {
        $h .= '<span class="product__tier" title="Typical price range">' . e($tierLabel) . '</span>';
    }
    $h .= amazon_link($p, 'See on Amazon <span aria-hidden="true">→</span>', 'btn btn--small btn--primary');
    $h .= '</div></div></article>';
    return $h;
}

function product_grid(array $products, ?string $bg = null): string
{
    if ($bg !== null) {
        $products = array_map(fn($p) => $p + ['bg' => $bg], $products);
    }
    return '<div class="product-grid">' . implode('', array_map('product_card', $products)) . '</div>';
}

function disclosure(): string
{
    return '<p class="disclosure"><strong>Affiliate disclosure:</strong> As an Amazon Associate, Vintique Flea earns from qualifying purchases. Prices and availability are set by Amazon and may change. <a href="/affiliate-disclosure/">Learn more</a>.</p>';
}

function breadcrumbs(array $items): string
{
    // $items: [[label, path], ...] — last item is the current page
    $all = array_merge([['Home', '/']], $items);
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $ld = [];
    foreach ($all as $i => [$label, $path]) {
        $last = $i === count($all) - 1;
        $h .= '<li>' . ($last ? '<span aria-current="page">' . e($label) . '</span>' : '<a href="' . e($path) . '">' . e($label) . '</a>') . '</li>';
        $ld[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => abs_url($path)];
    }
    $h .= '</ol></nav>';
    $GLOBALS['__schema'][] = ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => $ld];
    return $h;
}

function add_schema(array $s): void
{
    $GLOBALS['__schema'][] = $s + ['@context' => 'https://schema.org'];
}

function org_schema(): array
{
    $sameAs = array_values(SOCIAL);
    $o = [
        '@context' => 'https://schema.org',
        '@type' => 'Organization',
        '@id' => SITE_URL . '/#org',
        'name' => SITE_NAME,
        'url' => SITE_URL . '/',
        'logo' => SITE_URL . '/assets/img/logo.png',
        'description' => 'Curated indoor marketplace of mid-century modern, vintage clothing, architectural salvage and industrial, rustic home decor, local food trucks and more at Silver Street Studios in Houston.',
        'address' => venue_address(),
    ];
    if ($sameAs) {
        $o['sameAs'] = $sameAs;
    }
    return $o;
}

function venue_address(): array
{
    return [
        '@type' => 'PostalAddress',
        'streetAddress' => VENUE['street'],
        'addressLocality' => VENUE['city'],
        'addressRegion' => VENUE['region'],
        'postalCode' => VENUE['postal'],
        'addressCountry' => VENUE['country'],
    ];
}

function nav_items(): array
{
    return [
        ['/shop/', 'Shop'],
        ['/events/', 'Events'],
        ['/food-trucks/', 'Food Trucks'],
        ['/play/', 'Play'],
        ['/guides/', 'Guides'],
        ['/about/', 'About'],
        ['/contact/', 'Contact'],
    ];
}

/**
 * Print <head> + site header. $m keys: title, description, path, robots, type, css[], js[], body_class
 */
function page_start(array $m): void
{
    $path = $m['path'] ?? '/';
    $canonical = abs_url($path);
    $title = $m['title'] ?? SITE_NAME;
    $desc = $m['description'] ?? '';
    $robots = $m['robots'] ?? 'index, follow, max-image-preview:large';
    $GLOBALS['__page'] = $m;
    $current = '/' . explode('/', trim($path, '/'))[0] . '/';
    ?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:type" content="<?= e($m['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e(isset($m['image']) ? photo_url($m['image']) : SITE_URL . '/assets/img/og-image.png') ?>">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#c2552d">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Work+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_V ?>">
<?php foreach ($m['css'] ?? [] as $css): ?>
<link rel="stylesheet" href="<?= e($css) ?>?v=<?= ASSET_V ?>">
<?php endforeach; ?>
<script src="/assets/js/site.js?v=<?= ASSET_V ?>" defer></script>
<?php foreach ($m['js'] ?? [] as $js): ?>
<script src="<?= e($js) ?>?v=<?= ASSET_V ?>" defer></script>
<?php endforeach; ?>
</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brand" href="/" aria-label="Vintique Flea home">
      <span class="brand__mark" aria-hidden="true"><?= logo_svg() ?></span>
      <span class="brand__text">Vintique <em>Flea</em></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span class="sr-only">Menu</span><span class="nav-toggle__bars" aria-hidden="true"></span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
<?php foreach (nav_items() as [$href, $label]): ?>
        <li><a href="<?= $href ?>"<?= $current === $href ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn--small btn--primary site-nav__cta" href="/vendors/">Become a Vendor</a>
    </nav>
  </div>
</header>
<main id="main">
<?php
}

function page_end(): void
{
    $schemas = array_merge([org_schema(), [
        '@context' => 'https://schema.org',
        '@type' => 'WebSite',
        '@id' => SITE_URL . '/#website',
        'name' => SITE_NAME,
        'url' => SITE_URL . '/',
        'publisher' => ['@id' => SITE_URL . '/#org'],
    ]], $GLOBALS['__schema'] ?? []);
    $year = date('Y');
    ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-about">
      <a class="brand brand--light" href="/"><span class="brand__mark" aria-hidden="true"><?= logo_svg() ?></span><span class="brand__text">Vintique <em>Flea</em></span></a>
      <p>Houston's curated indoor marketplace of interesting things: mid-century modern, vintage clothing, architectural salvage and industrial, rustic home decor, local food trucks and more. From the founders of Rice Village Flea.</p>
      <address><?= e(VENUE['name']) ?><br><?= e(VENUE['street']) ?>, <?= e(VENUE['city']) ?>, <?= e(VENUE['region']) ?> <?= e(VENUE['postal']) ?></address>
    </div>
    <div>
      <h2 class="footer-h">Shop</h2>
      <ul class="footer-links">
<?php foreach (SHOP as $slug => $c): ?>
        <li><a href="/shop/<?= $slug ?>/"><?= e($c['name']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Visit</h2>
      <ul class="footer-links">
        <li><a href="/events/">Market Dates</a></li>
<?php foreach (EDITIONS as $slug => $ed): ?>
        <li><a href="/events/<?= $slug ?>/"><?= e($ed['name']) ?></a></li>
<?php endforeach; ?>
        <li><a href="/food-trucks/">Food Trucks</a></li>
        <li><a href="/vendors/">Become a Vendor</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Explore</h2>
      <ul class="footer-links">
        <li><a href="/play/">Games &amp; Tools</a></li>
        <li><a href="/guides/">Guides</a></li>
        <li><a href="/about/">About Us</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/photo-credits/">Photo Credits</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>© <?= $year ?> Vintique Flea. All rights reserved.</p>
    <p>As an Amazon Associate, Vintique Flea earns from qualifying purchases.</p>
  </div>
</footer>
<?php foreach ($schemas as $s): ?>
<script type="application/ld+json"><?= json_encode($s, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
<?php endforeach; ?>
</body>
</html>
<?php
}

function logo_svg(): string
{
    // Starburst + "VF" monogram
    return '<svg viewBox="0 0 48 48" width="40" height="40" role="img" aria-hidden="true"><g transform="translate(24 24)"><g fill="#d9a21b">'
        . implode('', array_map(fn($a) => '<rect x="-1.5" y="-23" width="3" height="10" rx="1.5" transform="rotate(' . $a . ')"/>', range(0, 330, 30)))
        . '</g><circle r="13" fill="#c2552d"/><text y="5" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="13" fill="#fffaf1">VF</text></g></svg>';
}

function app_secret(): string
{
    static $k = null;
    if ($k === null) {
        $f = DATA_DIR . '/secret.php';           // a PHP file, so it can never be read over the web
        if (!is_file($f)) {
            @file_put_contents($f, "<?php return '" . bin2hex(random_bytes(32)) . "';\n", LOCK_EX);
        }
        $k = is_file($f) ? (string) (include $f) : '';
        if ($k === '') {
            $k = hash('sha256', __FILE__ . php_uname());
        }
    }
    return $k;
}

/** Stateless CSRF token: timestamp + HMAC. Valid for 48h, no session needed. */
function csrf_token(): string
{
    $t = (string) time();
    return $t . '.' . hash_hmac('sha256', $t, app_secret());
}

function csrf_valid(?string $tok): bool
{
    if (!$tok || !str_contains($tok, '.')) {
        return false;
    }
    [$t, $sig] = explode('.', $tok, 2);
    if (!ctype_digit($t) || (time() - (int) $t) > 172800 || (time() - (int) $t) < 2) {
        return false; // expired, or submitted faster than a human could
    }
    return hash_equals(hash_hmac('sha256', $t, app_secret()), $sig);
}

function newsletter_form(string $source = 'site'): string
{
    $t = e(csrf_token());
    return '<form class="newsletter" method="post" action="/subscribe/">'
        . '<input type="hidden" name="csrf" value="' . $t . '"><input type="hidden" name="source" value="' . e($source) . '">'
        . '<div class="hp" aria-hidden="true"><label>Leave blank<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>'
        . '<label class="sr-only" for="nl-email-' . e($source) . '">Email address</label>'
        . '<input id="nl-email-' . e($source) . '" type="email" name="email" required placeholder="you@example.com" autocomplete="email">'
        . '<button class="btn btn--primary" type="submit">Get market dates</button></form>';
}

function faq_block(array $faq): string
{
    if (!$faq) {
        return '';
    }
    $h = '<section class="faq"><h2>Frequently asked questions</h2>';
    $ld = [];
    foreach ($faq as $f) {
        $h .= '<details><summary>' . e($f['q']) . '</summary><p>' . e($f['a']) . '</p></details>';
        $ld[] = ['@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']]];
    }
    add_schema(['@type' => 'FAQPage', 'mainEntity' => $ld]);
    return $h . '</section>';
}

function load_guides(): array
{
    static $g = null;
    if ($g === null) {
        $g = [];
        foreach (glob(__DIR__ . '/guides/*.php') ?: [] as $f) {
            $g[basename($f, '.php')] = require $f;
        }
        uasort($g, fn($a, $b) => strcmp($a['h1'], $b['h1']));
    }
    return $g;
}
