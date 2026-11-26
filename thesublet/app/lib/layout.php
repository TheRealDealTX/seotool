<?php defined('APP') || exit;

const ASSET_V = '4';

function logo_svg(): string
{
    return '<svg class="logo-mark" viewBox="0 0 40 40" width="34" height="34" aria-hidden="true" focusable="false">'
        . '<rect width="40" height="40" rx="10" fill="#2f6f4f"/>'
        . '<path d="M9 21 L20 11 L31 21" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>'
        . '<rect x="13" y="20" width="14" height="11" rx="1.5" fill="#fff"/>'
        . '<rect x="18" y="24" width="4" height="7" fill="#e46f4c"/></svg>';
}

/**
 * Render a full page.
 * $p: title, description, canonical (path), robots, body, schema (array of objects), og_image, og_type, h_extra (head html), scripts (array of urls), private (bool)
 */
function page(array $p): void
{
    header('Content-Type: text/html; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('X-Frame-Options: SAMEORIGIN');
    $title = $p['title'] ?? 'The Sublet';
    if (mb_strlen($title) > 60) $title = seo_title(preg_replace('/ \| The Sublet$/u', '', $title));
    $desc = seo_desc((string)($p['description'] ?? ''));
    $canonical = isset($p['canonical']) ? base_url($p['canonical']) : null;
    $robots = $p['robots'] ?? 'index, follow, max-image-preview:large';
    $og = $p['og_image'] ?? base_url('/assets/img/og-default.png');
    $gtm = preg_match('/^GTM-[A-Z0-9]+$/', (string)setting('gtm_id', '')) ? setting('gtm_id') : '';
    $gsc = (string)setting('gsc_meta', '');
    $schemas = $p['schema'] ?? [];
    $schemas[] = schema_org();
    ?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php if ($gtm): ?>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','<?= e($gtm) ?>');</script>
<?php endif; ?>
<title><?= e($title) ?></title>
<?php if ($desc): ?><meta name="description" content="<?= e($desc) ?>"><?php endif; ?>
<meta name="robots" content="<?= e($robots) ?>">
<?php if ($canonical): ?><link rel="canonical" href="<?= e($canonical) ?>"><?php endif; ?>
<?php if ($gsc): ?><meta name="google-site-verification" content="<?= e($gsc) ?>"><?php endif; ?>
<meta property="og:site_name" content="The Sublet">
<meta property="og:type" content="<?= e($p['og_type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($p['og_title'] ?? $title) ?>">
<?php if ($desc): ?><meta property="og:description" content="<?= e($desc) ?>"><?php endif; ?>
<?php if ($canonical): ?><meta property="og:url" content="<?= e($canonical) ?>"><?php endif; ?>
<meta property="og:image" content="<?= e($og) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2f6f4f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_V ?>">
<?= $p['h_extra'] ?? '' ?>
<?php foreach ($schemas as $s): ?>
<script type="application/ld+json"><?= json_encode($s, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
<?php endforeach; ?>
</head>
<body class="<?= e($p['body_class'] ?? '') ?>">
<?php if ($gtm): ?><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=<?= e($gtm) ?>" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript><?php endif; ?>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="logo" href="/" aria-label="The Sublet home"><?= logo_svg() ?><span class="logo-text">The<b>Sublet</b></span></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="nav-toggle-bars" aria-hidden="true"></span><span class="sr">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <a href="/sublets/">Find a sublet</a>
      <a href="/hosts/">For hosts</a>
      <a href="/tools/">Tools</a>
      <a href="/blog/">Guides</a>
      <a href="/favorites/" class="nav-fav">♡ Saved <span class="fav-count" hidden></span></a>
      <a href="/account/">Host login</a>
      <a class="btn btn-sm nav-cta" href="/post-a-sublet/">List your place</a>
    </nav>
  </div>
</header>
<main id="main">
<?= $p['body'] ?? '' ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <a class="logo logo-footer" href="/"><?= logo_svg() ?><span class="logo-text">The<b>Sublet</b></span></a>
      <p class="muted small">Furnished sublets and short-term rentals across the US, from one month to twelve. Built for summer sublets, travel nurses, interns, students and anyone relocating.</p>
    </div>
    <div>
      <h2 class="f-h">Renters</h2>
      <a href="/sublets/">Browse sublets</a><a href="/favorites/">Saved listings</a><a href="/compare/">Compare</a><a href="/safety/">Scam-awareness tips</a><a href="/tools/city-quiz/">City match quiz</a>
    </div>
    <div>
      <h2 class="f-h">Hosts</h2>
      <a href="/hosts/">Why host with us</a><a href="/post-a-sublet/">List your place</a><a href="/pricing/">Free vs. verified</a><a href="/account/">Host dashboard</a><a href="/blog/how-to-write-a-sublet-listing-that-rents/">Listing tips</a><a href="/blog/short-term-rental-laws-what-hosts-should-know/">Rental laws</a>
    </div>
    <div>
      <h2 class="f-h">The Sublet</h2>
      <a href="/about/">About</a><a href="/contact/">Contact</a><a href="/fair-housing/">Fair housing</a><a href="/terms/">Terms</a><a href="/privacy/">Privacy</a><a href="/credits/">Photo credits</a>
    </div>
  </div>
  <div class="wrap footer-legal small muted">
    <p><strong>Fair housing:</strong> The Sublet supports the federal Fair Housing Act. Listings may not discriminate based on race, color, religion, sex, disability, familial status or national origin, or other characteristics protected by state or local law. <strong>Hosts</strong> are responsible for following their lease and local short-term-rental, registration and tax rules.</p>
    <p>As an Amazon Associate, The Sublet earns from qualifying purchases. © <?= date('Y') ?> The Sublet · thesublet.com</p>
  </div>
</footer>
<script src="/assets/js/site.js?v=<?= ASSET_V ?>" defer></script>
<?php foreach ($p['scripts'] ?? [] as $s): ?>
<script src="<?= e($s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}

function breadcrumbs_html(array $crumbs): string
{
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $n = count($crumbs);
    foreach ($crumbs as $i => [$label, $url]) {
        $h .= '<li>' . ($i < $n - 1 ? '<a href="' . e($url) . '">' . e($label) . '</a>' : '<span aria-current="page">' . e($label) . '</span>') . '</li>';
    }
    return $h . '</ol></nav>';
}

function faq_html(array $faqs, string $heading = 'Frequently asked questions'): string
{
    if (!$faqs) return '';
    $h = '<section class="faq"><h2>' . e($heading) . '</h2>';
    foreach ($faqs as $f) {
        $h .= '<details><summary>' . e(html_entity_decode($f['q'], ENT_QUOTES, 'UTF-8')) . '</summary><div>' . (str_contains($f['a'], '<') ? $f['a'] : '<p>' . $f['a'] . '</p>') . '</div></details>';
    }
    return $h . '</section>';
}

/** Error list for forms */
function form_errors(array $err): string
{
    if (!$err) return '';
    $h = '<div class="flash flash-err" role="alert"><strong>Please fix the following:</strong><ul>';
    foreach ($err as $m) $h .= '<li>' . e($m) . '</li>';
    return $h . '</ul></div>';
}

/** Royalty-free photo manifest (app/content/photos/*.php). */
function photos(): array
{
    static $all = null;
    if ($all !== null) return $all;
    $all = [];
    foreach (glob(APPDIR . '/content/photos/*.php') ?: [] as $f) {
        $d = require $f;
        if (is_array($d)) $all += $d;
    }
    return $all;
}

function photo(string $key): ?array
{
    $p = photos()[$key] ?? null;
    if (!$p || !is_file(ROOT . $p['file'])) return null;
    return $p;
}

function photo_img(string $key, string $class = '', bool $lazy = true, ?string $alt = null): string
{
    $p = photo($key);
    if (!$p) return '';
    return '<img src="' . e($p['file']) . '" alt="' . e($alt ?? $p['alt']) . '" width="' . (int)$p['w'] . '" height="' . (int)$p['h'] . '"'
        . ($class ? ' class="' . e($class) . '"' : '') . ($lazy ? ' loading="lazy" decoding="async"' : ' fetchpriority="high"') . '>';
}

function photo_url(string $key, string $fallback = ''): string
{
    $p = photo($key);
    return $p ? $p['file'] : $fallback;
}
