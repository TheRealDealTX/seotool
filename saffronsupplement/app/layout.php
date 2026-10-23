<?php
// Shared page shell: <head>, header, breadcrumbs, footer, JSON-LD, sitemap.
defined('SS_APP') || exit;

const NAV = [
    ['Best Supplements', '/best-saffron-supplements/'],
    ['Benefits', '/saffron-benefits/', [
        ['Mood & Depression', '/saffron-for-depression-and-mood/'],
        ['Sleep', '/saffron-for-sleep/'],
        ['Eye Health', '/saffron-for-eye-health/'],
        ['Weight & Appetite', '/saffron-for-weight-loss/'],
        ['PMS', '/saffron-for-pms/'],
    ]],
    ['Guides', '/guides/', [
        ['Dosage', '/saffron-dosage/'],
        ['Side Effects', '/saffron-side-effects/'],
        ['How to Choose', '/how-to-choose-a-saffron-supplement/'],
        ['affron vs Satiereal', '/affron-vs-satiereal/'],
    ]],
    ['Free Tools', '/tools/', [
        ['Dosage Calculator', '/tools/saffron-dosage-calculator/'],
        ['Supplement Quiz', '/tools/saffron-supplement-quiz/'],
        ['Cost-Per-Dose', '/tools/cost-per-dose-calculator/'],
        ['Safety Checker', '/tools/saffron-safety-checker/'],
        ['Mood & Sleep Tracker', '/tools/saffron-mood-sleep-tracker/'],
    ]],
    ['Blog', '/blog/'],
    ['FAQ', '/faq/'],
];

function logo_svg($size = 36) {
    return '<svg class="logo-mark" width="' . $size . '" height="' . $size . '" viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
        . '<path d="M32 58c0-10 0-18 0-26" stroke="#3f7d4e" stroke-width="3" stroke-linecap="round" fill="none"/>'
        . '<path d="M32 36C20 34 13 24 14 10c9 3 16 11 18 26z" fill="#7b4fa6"/>'
        . '<path d="M32 36c12-2 19-12 18-26-9 3-16 11-18 26z" fill="#7b4fa6"/>'
        . '<path d="M32 38C25 28 25 15 32 4c7 11 7 24 0 34z" fill="#9b6cc8"/>'
        . '<path d="M32 34l-7-20M32 34l0-22M32 34l7-20" stroke="#e8461f" stroke-width="2.6" stroke-linecap="round"/>'
        . '<circle cx="25" cy="14" r="2.4" fill="#f2a516"/><circle cx="32" cy="11" r="2.4" fill="#f2a516"/><circle cx="39" cy="14" r="2.4" fill="#f2a516"/>'
        . '</svg>';
}

/** Hero for interior pages (H1 comes from the route). */
function page_hero($route, $lede = '', $kicker = '') {
    $h = '<header class="phero"><div class="wrap">' . breadcrumbs_html() . ($kicker ? '<p class="kicker">' . e($kicker) . '</p>' : '')
        . '<h1>' . e($route['h1']) . '</h1>' . ($lede ? '<p class="lede">' . $lede . '</p>' : '');
    if (in_array($route['type'], ['article', 'review'], true)) {
        $h .= '<p class="byline"><span>By the ' . SITE_NAME . ' Editorial Team</span><span>' . (isset($route['date']) ? 'Published' : 'Updated') . ' <time datetime="' . route_date($route) . '">' . human_date(route_date($route)) . '</time></span><span>' . a('/about/#process', 'How we research') . '</span></p>';
    }
    return $h . '</div></header>';
}

function breadcrumbs() {
    $path = $GLOBALS['ss_path'];
    $route = $GLOBALS['ss_route'];
    if ($path === '/' || $path === '/404') return [];
    $crumbs = [['Home', '/']];
    if (!empty($route['parent'])) {
        $crumbs[] = [SECTION_NAMES[$route['parent']] ?? ROUTES[$route['parent']]['h1'], $route['parent']];
    }
    $crumbs[] = [$route['h1'], $path];
    return $crumbs;
}

function breadcrumbs_html() {
    $c = breadcrumbs();
    if (!$c) return '';
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    foreach ($c as $i => [$label, $href]) {
        $h .= $i === count($c) - 1 ? '<li aria-current="page">' . e($label) . '</li>' : '<li><a href="' . e($href) . '">' . e($label) . '</a></li>';
    }
    return $h . '</ol></nav>';
}

function render_page($path, array $route) {
    $GLOBALS['ss_path'] = $path;
    $GLOBALS['ss_route'] = $route;
    $GLOBALS['faq'] = [];
    $GLOBALS['extra_head'] = '';

    ob_start();
    require __DIR__ . '/pages/' . $route['file'] . '.php';
    $body = ob_get_clean();

    $canonical = SITE_ORIGIN . ($path === '/404' ? '/' : $path);
    header('Content-Type: text/html; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    ?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA_ID ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '<?= GA_ID ?>');
</script>
<title><?= e($route['title']) ?></title>
<meta name="description" content="<?= e($route['desc']) ?>">
<?php if (!empty($route['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta property="og:type" content="<?= $route['type'] === 'article' || $route['type'] === 'review' ? 'article' : 'website' ?>">
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:title" content="<?= e($route['title']) ?>">
<meta property="og:description" content="<?= e($route['desc']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:image" content="<?= SITE_ORIGIN ?>/assets/img/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="<?= SITE_NAME ?>: research-backed saffron benefits, dosage and reviews">
<?php if ($route['type'] === 'article' || $route['type'] === 'review'): ?><meta property="article:published_time" content="<?= route_date($route) ?>T00:00:00+00:00">
<meta property="article:modified_time" content="<?= route_date($route) ?>T00:00:00+00:00">
<?php endif; ?><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($route['title']) ?>">
<meta name="twitter:description" content="<?= e($route['desc']) ?>">
<meta name="twitter:image" content="<?= SITE_ORIGIN ?>/assets/img/og-image.png">
<meta name="author" content="<?= SITE_NAME ?>">
<meta name="format-detection" content="telephone=no">
<meta name="theme-color" content="#5b2a86">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="<?= SITE_NAME ?>" href="<?= SITE_ORIGIN ?>/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/assets/css/style.css?v=<?= filemtime(dirname(__DIR__) . '/assets/css/style.css') ?>">
<script type="application/ld+json"><?= json_ld($path, $route) ?></script>
<?= $GLOBALS['extra_head'] ?>
</head>
<body class="page-<?= e($route['file']) ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">Independent, research-based saffron reviews &middot; <a href="/tools/">Try our free saffron tools</a></div></div>
<header class="site-header">
  <div class="wrap hdr">
    <a class="brand" href="/" aria-label="<?= SITE_NAME ?> home"><?= logo_svg() ?><span><?= SITE_NAME ?></span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="site-nav" class="nav" aria-label="Main">
      <ul>
<?php foreach (NAV as $item):
        $active = $path === $item[1] || (isset($item[2]) && in_array($path, array_column($item[2], 1), true)); ?>
        <li class="<?= isset($item[2]) ? 'has-sub' : '' ?><?= $active ? ' active' : '' ?>"><a href="<?= e($item[1]) ?>"><?= e($item[0]) ?></a>
<?php if (isset($item[2])): ?>          <ul class="sub"><?php foreach ($item[2] as [$l, $h]): ?><li><a href="<?= e($h) ?>"><?= e($l) ?></a></li><?php endforeach; ?></ul>
<?php endif; ?>        </li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-nav" href="/tools/saffron-supplement-quiz/">Find My Supplement</a>
    </nav>
  </div>
</header>
<main id="main">
<?= $body ?>
</main>
<footer class="site-footer">
  <div class="wrap fgrid">
    <div class="fcol fabout">
      <a class="brand brand-f" href="/"><?= logo_svg(32) ?><span><?= SITE_NAME ?></span></a>
      <p><?= SITE_NAME ?> is an independent guide to saffron extract: what the research says, how to dose it safely, and which products are worth buying.</p>
      <p class="small">As an Amazon Associate, <?= SITE_NAME ?> earns from qualifying purchases.</p>
    </div>
    <div class="fcol"><h2>Benefits</h2><ul>
      <li><a href="/saffron-benefits/">All Benefits</a></li><li><a href="/saffron-for-depression-and-mood/">Mood &amp; Depression</a></li><li><a href="/saffron-for-sleep/">Sleep</a></li><li><a href="/saffron-for-eye-health/">Eye Health</a></li><li><a href="/saffron-for-weight-loss/">Weight &amp; Appetite</a></li><li><a href="/saffron-for-pms/">PMS</a></li></ul></div>
    <div class="fcol"><h2>Guides &amp; Reviews</h2><ul>
      <li><a href="/best-saffron-supplements/">Best Saffron Supplements</a></li><li><a href="/saffron-dosage/">Dosage Guide</a></li><li><a href="/saffron-side-effects/">Side Effects</a></li><li><a href="/how-to-choose-a-saffron-supplement/">How to Choose</a></li><li><a href="/affron-vs-satiereal/">affron vs Satiereal</a></li><li><a href="/blog/">Blog</a></li><li><a href="/faq/">FAQ</a></li></ul></div>
    <div class="fcol"><h2>Free Tools</h2><ul>
      <li><a href="/tools/saffron-dosage-calculator/">Dosage Calculator</a></li><li><a href="/tools/saffron-supplement-quiz/">Supplement Quiz</a></li><li><a href="/tools/cost-per-dose-calculator/">Cost-Per-Dose</a></li><li><a href="/tools/saffron-safety-checker/">Safety Checker</a></li><li><a href="/tools/saffron-mood-sleep-tracker/">Mood &amp; Sleep Tracker</a></li></ul></div>
    <div class="fcol"><h2>Company</h2><ul>
      <li><a href="/about/">About Us</a></li><li><a href="/contact/">Contact</a></li><li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li><li><a href="/medical-disclaimer/">Medical Disclaimer</a></li><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms/">Terms of Use</a></li><li><a href="/sitemap/">Sitemap</a></li></ul></div>
  </div>
  <div class="wrap fbottom">
    <p>&copy; <?= SITE_YEAR ?> <?= SITE_NAME ?>. All rights reserved.</p>
    <p class="small">These statements have not been evaluated by the Food and Drug Administration. Products mentioned are not intended to diagnose, treat, cure or prevent any disease. Content is for education only; consult a qualified healthcare professional before taking any supplement.</p>
  </div>
</footer>
<script src="/assets/js/app.js?v=<?= filemtime(dirname(__DIR__) . '/assets/js/app.js') ?>" defer></script>
</body>
</html>
<?php
}

function json_ld($path, array $route) {
    $org = ['@type' => 'Organization', '@id' => SITE_ORIGIN . '/#org', 'name' => SITE_NAME, 'url' => SITE_ORIGIN . '/',
            'logo' => SITE_ORIGIN . '/assets/img/logo-512.png', 'email' => SITE_EMAIL];
    $graph = [$org, ['@type' => 'WebSite', '@id' => SITE_ORIGIN . '/#website', 'name' => SITE_NAME, 'url' => SITE_ORIGIN . '/',
                     'publisher' => ['@id' => SITE_ORIGIN . '/#org'], 'inLanguage' => 'en-US']];
    $url = SITE_ORIGIN . $path;
    if ($path === '/404') return json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);

    $page = ['@type' => 'WebPage', '@id' => $url . '#webpage', 'url' => $url, 'name' => $route['title'], 'description' => $route['desc'],
             'isPartOf' => ['@id' => SITE_ORIGIN . '/#website'], 'dateModified' => route_date($route), 'inLanguage' => 'en-US'];
    if ($route['type'] === 'article' || $route['type'] === 'review') {
        $page['@type'] = ['WebPage', 'MedicalWebPage'];
        $graph[] = ['@type' => 'Article', '@id' => $url . '#article', 'headline' => $route['h1'], 'description' => $route['desc'],
                    'mainEntityOfPage' => ['@id' => $url . '#webpage'], 'datePublished' => route_date($route), 'dateModified' => route_date($route),
                    'author' => ['@type' => 'Organization', 'name' => SITE_NAME . ' Editorial Team', 'url' => SITE_ORIGIN . '/about/'],
                    'publisher' => ['@id' => SITE_ORIGIN . '/#org'], 'image' => SITE_ORIGIN . '/assets/img/og-image.png'];
    }
    if ($route['type'] === 'tool') {
        $graph[] = ['@type' => 'WebApplication', 'name' => $route['h1'], 'url' => $url, 'applicationCategory' => 'HealthApplication',
                    'operatingSystem' => 'Any (web browser)', 'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
                    'publisher' => ['@id' => SITE_ORIGIN . '/#org']];
    }
    if ($route['type'] === 'review') {
        $items = [];
        $i = 1;
        foreach (PRODUCTS as $id => $p) {
            $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => $url . '#' . $id, 'name' => $p['name']];
        }
        $graph[] = ['@type' => 'ItemList', 'name' => $route['h1'], 'itemListElement' => $items];
    }
    $graph[] = $page;
    if ($c = breadcrumbs()) {
        $list = [];
        foreach ($c as $i => [$label, $href]) $list[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $label, 'item' => SITE_ORIGIN . $href];
        $graph[] = ['@type' => 'BreadcrumbList', 'itemListElement' => $list];
    }
    if (!empty($GLOBALS['faq'])) {
        $q = [];
        foreach ($GLOBALS['faq'] as [$question, $answer]) {
            $q[] = ['@type' => 'Question', 'name' => $question,
                    'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(preg_replace('/\s+/', ' ', strip_tags($answer)))]];
        }
        $graph[] = ['@type' => 'FAQPage', 'mainEntity' => $q];
    }
    return json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
}

function render_sitemap() {
    header('Content-Type: application/xml; charset=utf-8');
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach (ROUTES as $p => $r) {
        $prio = $p === '/' ? '1.0' : (in_array($r['type'], ['review', 'tool'], true) || $p === '/best-saffron-supplements/' ? '0.9' : (str_starts_with($r['file'], 'legal') ? '0.3' : '0.8'));
        echo '  <url><loc>' . SITE_ORIGIN . $p . '</loc><lastmod>' . route_date($r) . '</lastmod><priority>' . $prio . "</priority></url>\n";
    }
    echo "</urlset>\n";
}

function render_feed() {
    header('Content-Type: application/rss+xml; charset=utf-8');
    $date = date(DATE_RSS, strtotime(UPDATED . ' 12:00:00 UTC'));
    echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n"
        . '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
        . '<title>' . SITE_NAME . '</title><link>' . SITE_ORIGIN . '/</link>'
        . '<description>Research-backed saffron supplement benefits, dosage, safety and reviews.</description>'
        . '<language>en-us</language><lastBuildDate>' . $date . '</lastBuildDate>'
        . '<atom:link href="' . SITE_ORIGIN . '/feed.xml" rel="self" type="application/rss+xml"/>' . "\n";
    $items = array_filter(ROUTES, fn($r) => in_array($r['type'], ['article', 'review'], true));
    uasort($items, fn($a, $b) => strcmp(route_date($b), route_date($a)));
    foreach ($items as $p => $r) {
        echo '<item><title>' . e($r['h1']) . '</title><link>' . SITE_ORIGIN . $p . '</link><guid>' . SITE_ORIGIN . $p . '</guid>'
            . '<pubDate>' . date(DATE_RSS, strtotime(route_date($r) . ' 12:00:00 UTC')) . '</pubDate><description>' . e($r['desc']) . "</description></item>\n";
    }
    echo "</channel></rss>\n";
}
