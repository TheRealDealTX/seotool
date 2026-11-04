<?php
/** Shared document shell: <head>, header/nav, footer. */
defined('SCC') || (http_response_code(404) && exit);

function org_schema(): array
{
    return [
        '@type' => 'Organization',
        '@id' => SITE_ORIGIN . '/#organization',
        'name' => SITE_NAME,
        'alternateName' => 'SolarCCTVCamera.com',
        'url' => SITE_ORIGIN . '/',
        'email' => SITE_EMAIL,
        'logo' => ['@type' => 'ImageObject', 'url' => abs_url('/icon-512.png'), 'width' => 512, 'height' => 512],
        'description' => 'Solar CCTV Camera publishes independent, research-based guides, calculators and buying advice for solar-powered security cameras.',
    ];
}

function website_schema(): array
{
    return [
        '@type' => 'WebSite',
        '@id' => SITE_ORIGIN . '/#website',
        'name' => SITE_NAME,
        'url' => SITE_ORIGIN . '/',
        'publisher' => ['@id' => SITE_ORIGIN . '/#organization'],
        'inLanguage' => 'en-US',
    ];
}

function breadcrumb_schema(array $crumbs): array
{
    $items = [];
    foreach (array_values($crumbs) as $i => [$name, $url]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($url)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function nav_items(): array
{
    return [
        ['Best Cameras', '/best-solar-security-cameras/', null],
        ['Guides', '/solar-camera-guides/', [
            ['How Solar Cameras Work', '/how-solar-cameras-work/', 'sun'],
            ['Installation Guide', '/solar-camera-installation/', 'tool'],
            ['Best Panel Angle', '/guides/solar-camera-panel-angle/', 'angle'],
            ['Do They Work at Night?', '/guides/do-solar-cameras-work-at-night/', 'moon'],
            ['Solar vs Wired', '/compare/solar-vs-wired/', 'plug'],
            ['4G SIM Card Cameras', '/reviews/solar-cctv-camera-with-sim-card/', 'signal'],
            ['All guides →', '/solar-camera-guides/', 'book'],
        ]],
        ['Tools', '/tools/', [
            ['Panel Angle Calculator', '/tools/solar-panel-angle-calculator/', 'angle'],
            ['Battery & Solar Calculator', '/tools/solar-camera-battery-calculator/', 'battery'],
            ['CCTV Camera Planner', '/tools/cctv-camera-planner/', 'map'],
            ['Solar Site Check', '/tools/solar-camera-site-check/', 'compass'],
            ['4G Data & Storage', '/tools/4g-data-and-storage-calculator/', 'sd'],
            ['Coverage Calculator', '/tools/camera-coverage-calculator/', 'eye'],
            ['Solar vs Wired Cost', '/tools/solar-vs-wired-cost-calculator/', 'dollar'],
        ]],
        ['Use Cases', '/solar-camera-guides/#use-cases', [
            ['Farms & Ranches', '/use-cases/solar-cameras-for-farms/', 'barn'],
            ['Rural Property', '/use-cases/solar-cameras-rural-property/', 'tree'],
            ['RVs & Campers', '/use-cases/solar-cameras-for-rvs/', 'rv'],
            ['Construction Sites', '/use-cases/solar-cameras-for-construction-sites/', 'building'],
            ['Gates & Driveways', '/guides/solar-gate-camera/', 'gate'],
            ['Remote Cabins', '/guides/remote-cabin-solar-camera/', 'home'],
        ]],
        ['About', '/about-us/', null],
    ];
}

/**
 * @param array $m title, description, path, image, type, schema (graph nodes),
 *                 noindex, body_class, scripts (array of asset paths), published, updated
 */
function page_head(array $m): void
{
    $title = $m['title'];
    $desc = $m['description'] ?? '';
    $path = $m['path'] ?? '/';
    $canonical = abs_url($path);
    $image = $m['image'] ?? img_url('og-default');
    $type = $m['type'] ?? 'website';
    $graph = array_merge([org_schema(), website_schema()], $m['schema'] ?? []);
    $bodyClass = $m['body_class'] ?? '';
    ?>
<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php if (!empty($m['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<?php endif; ?>
<meta name="theme-color" content="#0b1324">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:type" content="<?= e($type) ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<?php if (!empty($m['published'])): ?><meta property="article:published_time" content="<?= e($m['published']) ?>T08:00:00+00:00">
<meta property="article:modified_time" content="<?= e($m['updated'] ?? $m['published']) ?>T08:00:00+00:00">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($m['og_title'] ?? $title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap">
<link rel="stylesheet" href="<?= asset('css/site.css') ?>">
<?php if (!empty($m['preload_image'])): ?><link rel="preload" as="image" href="<?= e($m['preload_image']) ?>">
<?php endif; ?>
<?= json_ld(['@context' => 'https://schema.org', '@graph' => $graph]) ?>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA_ID ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '<?= GA_ID ?>');
  gtag('config', '<?= GA_LEGACY_ID ?>');
</script>
</head>
<body class="<?= e($bodyClass) ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="charge-bar" aria-hidden="true"><span></span></div>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <span class="brand-mark"><?= icon('sun', 22) ?></span>
      <span class="brand-text">Solar<b>CCTV</b>Camera</span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><?= icon('menu', 24) ?></button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
<?php foreach (nav_items() as [$label, $href, $children]):
        $active = ($path === $href || ($children && in_array($path, array_column($children, 1), true))) ? ' is-active' : ''; ?>
        <li class="<?= $children ? 'has-sub' : '' ?><?= $active ?>">
          <a href="<?= e($href) ?>"<?= $children ? ' aria-haspopup="true"' : '' ?>><?= e($label) ?></a>
<?php if ($children): ?>
          <button class="sub-toggle" aria-label="Show <?= e($label) ?> menu" aria-expanded="false"><svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8"/></svg></button>
          <ul class="sub">
<?php foreach ($children as [$cl, $ch, $ci]): ?>
            <li><a href="<?= e($ch) ?>"><?= icon($ci, 18) ?><span><?= e($cl) ?></span></a></li>
<?php endforeach; ?>
          </ul>
<?php endif; ?>
        </li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-sun nav-cta" href="/tools/"><?= icon('calc', 18) ?> Free Tools</a>
    </nav>
  </div>
</header>
<main id="main">
<?php
}

function page_foot(array $scripts = []): void
{
    $year = date('Y');
    ?>
</main>
<footer class="site-footer">
  <div class="footer-horizon" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="brand" href="/"><span class="brand-mark"><?= icon('sun', 22) ?></span><span class="brand-text">Solar<b>CCTV</b>Camera</span></a>
      <p>Solar CCTV Camera is an independent resource for anyone choosing, installing or troubleshooting a solar-powered security camera. Research-based guides and free calculators, no paid placements.</p>
      <p class="footer-mail"><?= icon('mail', 18) ?> <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a></p>
    </div>
    <div>
      <h2>Start here</h2>
      <ul>
        <li><a href="/best-solar-security-cameras/">Best Solar Security Cameras</a></li>
        <li><a href="/how-solar-cameras-work/">How Solar Cameras Work</a></li>
        <li><a href="/solar-camera-installation/">Solar Camera Installation</a></li>
        <li><a href="/compare/solar-vs-wired/">Solar vs Wired Cameras</a></li>
        <li><a href="/solar-camera-guides/">All Guides</a></li>
      </ul>
    </div>
    <div>
      <h2>Free tools</h2>
      <ul>
<?php foreach (tools_meta() as $t): ?>
        <li><a href="<?= e($t['path']) ?>"><?= e($t['short']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2>Company</h2>
      <ul>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
        <li><a href="/sitemap/">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>© <?= $year ?> Solar CCTV Camera · SolarCCTVCamera.com</p>
    <p class="muted">As an Amazon Associate we earn from qualifying purchases. This never changes what we recommend.</p>
  </div>
</footer>
<script src="<?= asset('js/site.js') ?>" defer></script>
<?php foreach ($scripts as $s): ?>
<script src="<?= asset($s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}

function breadcrumbs_html(array $crumbs): string
{
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $n = count($crumbs);
    foreach (array_values($crumbs) as $i => [$name, $url]) {
        $h .= $i === $n - 1 ? '<li aria-current="page">' . e($name) . '</li>' : '<li><a href="' . e($url) . '">' . e($name) . '</a></li>';
    }
    return $h . '</ol></nav>';
}

/** Card for listing an article. */
function article_card(array $a, bool $showImg = true): string
{
    $sec = SECTIONS[$a['section']][0] ?? '';
    $img = $showImg && !empty($a['image']) ? '<div class="card-img">' . img($a['image'], $a['image_alt'] ?? $a['h1'], ['sizes' => '(max-width: 700px) 100vw, 360px']) . '</div>' : '';
    return '<article class="card reveal">' . $img . '<div class="card-body"><span class="tag">' . e($a['kicker'] ?? $sec) . '</span><h3><a href="' . e($a['path']) . '">' . e($a['card_title'] ?? $a['h1']) . '</a></h3><p>' . e($a['card_text'] ?? $a['description']) . '</p></div></article>';
}

function tool_card(array $t): string
{
    return '<a class="tool-card reveal" href="' . e($t['path']) . '"><span class="tool-ic">' . icon($t['icon'], 26) . '</span><span class="tool-txt"><strong>' . e($t['name']) . '</strong><span>' . e($t['blurb']) . '</span></span><span class="tool-go">' . icon('arrow', 18) . '</span></a>';
}
