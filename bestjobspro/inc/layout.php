<?php
// Shared layout: <head>, header, footer, icons and schema helpers.

function e($s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function url(string $path): string
{
    return SITE_URL . $path;
}

function asset(string $path): string
{
    return $path . '?v=' . ASSET_VER;
}

const ICONS = [
    'phone'    => '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
    'mail'     => '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    'pin'      => '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    'clock'    => '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    'menu'     => '<path d="M4 6h16M4 12h16M4 18h16"/>',
    'x'        => '<path d="M18 6 6 18M6 6l12 12"/>',
    'arrow'    => '<path d="M5 12h14M12 5l7 7-7 7"/>',
    'check'    => '<path d="M20 6 9 17l-5-5"/>',
    'briefcase'=> '<rect width="20" height="14" x="2" y="7" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    'users'    => '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    'search'   => '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    'shield'   => '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    'flask'    => '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3M7 15h10"/>',
    'clipboard'=> '<rect width="8" height="4" x="8" y="2" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    'link'     => '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    'star'     => '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
    'wallet'   => '<path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/>',
    'compass'  => '<circle cx="12" cy="12" r="10"/><path d="m16.24 7.76-2.12 6.36-6.36 2.12 2.12-6.36 6.36-2.12z"/>',
    'scan'     => '<path d="M3 7V5a2 2 0 0 1 2-2h2M17 3h2a2 2 0 0 1 2 2v2M21 17v2a2 2 0 0 1-2 2h-2M7 21H5a2 2 0 0 1-2-2v-2M7 8h8M7 12h10M7 16h6"/>',
    'receipt'  => '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8M12 17.5v-11"/>',
    'gauge'    => '<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',
    'chart'    => '<path d="M3 3v18h18M18 17V9M13 17V5M8 17v-3"/>',
    'calendar' => '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'zap'      => '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    'file'     => '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M10 9H8M16 13H8M16 17H8"/>',
    'building' => '<rect width="16" height="20" x="4" y="2" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
    'truck'    => '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2M15 18H9M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
    'wrench'   => '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    'headset'  => '<path d="M3 14h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-7a9 9 0 0 1 18 0v7a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3"/>',
    'package'  => '<path d="m7.5 4.27 9 5.15M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/>',
    'target'   => '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    'trending' => '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    'dollar'   => '<circle cx="12" cy="12" r="10"/><path d="M16 8h-6a2 2 0 1 0 0 4h4a2 2 0 1 1 0 4H8M12 18V6"/>',
    'usercheck'=> '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/>',
    'layers'   => '<path d="M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65M22 12.65l-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    'send'     => '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    'upload'   => '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5M12 3v12"/>',
    'book'     => '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2zM22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    'hardhat'  => '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2z"/><path d="M10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5M4 15v-3a6 6 0 0 1 6-6M14 6a6 6 0 0 1 6 6v3"/>',
    'heart'    => '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    'repeat'   => '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14M7 22l-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
];

function icon(string $name, string $class = 'ico'): string
{
    $paths = ICONS[$name] ?? ICONS['check'];
    return '<svg class="' . e($class) . '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $paths . '</svg>';
}

function json_ld(array $data): string
{
    return '<script type="application/ld+json">' . json_encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) . '</script>' . "\n";
}

function org_schema(): array
{
    return [
        '@type'       => 'EmploymentAgency',
        '@id'         => SITE_URL . '/#organization',
        'name'        => SITE_NAME,
        'alternateName' => ['BestJobsPro', 'Best Jobs Pro Staffing'],
        'url'         => SITE_URL . '/',
        'logo'        => url('/assets/img/site/Best-Jobs-Pro-Organization-Logo.webp'),
        'image'       => url('/assets/img/site/Best-Jobs-Pro-Site-Image.webp'),
        'description' => 'Best Jobs Pro is a Texas staffing agency and recruiter connecting job seekers with office, warehouse, skilled-trade, driving and customer-service jobs, with no fees for applicants.',
        'telephone'   => SITE_TEL,
        'email'       => SITE_EMAIL,
        'foundingDate'=> SITE_FOUNDED,
        'priceRange'  => 'Free for job seekers',
        'address'     => [
            '@type'           => 'PostalAddress',
            'streetAddress'   => SITE_STREET,
            'addressLocality' => SITE_CITY,
            'addressRegion'   => SITE_REGION,
            'postalCode'      => SITE_ZIP,
            'addressCountry'  => 'US',
        ],
        'areaServed'  => ['@type' => 'State', 'name' => 'Texas'],
        'openingHoursSpecification' => [
            '@type'     => 'OpeningHoursSpecification',
            'dayOfWeek' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'opens'     => '00:00',
            'closes'    => '23:59',
        ],
        'hasMap'      => SITE_MAP,
    ];
}

function breadcrumb_schema(array $crumbs): array
{
    $items = [];
    foreach ($crumbs as $i => [$name, $path]) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => url($path)];
    }
    return ['@type' => 'BreadcrumbList', 'itemListElement' => $items];
}

function faq_schema(array $faqs): array
{
    return [
        '@type'      => 'FAQPage',
        'mainEntity' => array_map(fn($f) => [
            '@type'          => 'Question',
            'name'           => $f['q'],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']],
        ], $faqs),
    ];
}

/**
 * Print everything from <!doctype> to the opening of <main>.
 * $m keys: title (full <title>), description, path, image, type, schema (list of nodes),
 * crumbs (list of [name, path]; Home is prepended), robots, body_class.
 */
function page_start(array $m): void
{
    $path   = $m['path'] ?? '/';
    $canon  = url($path);
    $image  = url($m['image'] ?? '/assets/img/site/Best-Jobs-Pro-Site-Image.webp');
    $robots = $m['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1';
    $crumbs = $m['crumbs'] ?? [];

    $graph = [
        org_schema(),
        [
            '@type'     => 'WebSite',
            '@id'       => SITE_URL . '/#website',
            'url'       => SITE_URL . '/',
            'name'      => SITE_NAME,
            'publisher' => ['@id' => SITE_URL . '/#organization'],
            'inLanguage'=> 'en-US',
        ],
    ];
    if ($crumbs) {
        $graph[] = breadcrumb_schema(array_merge([['Home', '/']], $crumbs));
    }
    foreach ($m['schema'] ?? [] as $node) {
        $graph[] = $node;
    }
    ?>
<!doctype html>
<html lang="en-US">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA_ID ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '<?= GA_ID ?>');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($m['title']) ?></title>
<meta name="description" content="<?= e($m['description']) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= e($m['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($m['og_title'] ?? $m['title']) ?>">
<meta property="og:description" content="<?= e($m['description']) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<meta name="twitter:card" content="summary_large_image">
<?php if (!empty($m['published'])): ?>
<meta property="article:published_time" content="<?= e($m['published']) ?>T08:00:00-05:00">
<meta property="article:modified_time" content="<?= e($m['updated'] ?? $m['published']) ?>T08:00:00-05:00">
<?php endif; ?>
<meta name="theme-color" content="#FF5757">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" href="/favicon-32x32.png" sizes="32x32">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/png" href="/web-app-manifest-192x192.png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat+Alternates:wght@600;700&family=Montserrat:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<?php if (!empty($m['preload'])): ?>
<link rel="preload" as="image" href="<?= e($m['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<?= json_ld(['@context' => 'https://schema.org', '@graph' => $graph]) ?>
</head>
<body class="<?= e($m['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">
  <div class="wrap topbar__in">
    <span><?= icon('clock') ?> 24/7 Around-the-Clock Service</span>
    <span class="topbar__fees"><?= icon('shield') ?> No employment or processing fees</span>
    <a href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> <?= SITE_PHONE ?></a>
    <a class="topbar__mail" href="mailto:<?= SITE_EMAIL ?>"><?= icon('mail') ?> <?= SITE_EMAIL ?></a>
  </div>
</div>
<header class="site-header" id="top">
  <div class="wrap site-header__in">
    <a class="brand" href="/" aria-label="Best Jobs Pro home">
      <img src="/assets/img/site/Best-Jobs-Pro-Logo.webp" alt="Best Jobs Pro logo" width="500" height="426">
      <span class="brand__text">Best Jobs Pro<small>Texas Staffing &amp; Recruiting</small></span>
    </a>
    <nav class="nav" id="site-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as [$href, $label]):
        $active = $href === $path || ($href !== '/' && str_starts_with($path, $href)); ?>
        <li><a href="<?= e($href) ?>"<?= $active ? ' aria-current="page"' : '' ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn--sm nav__cta" href="/applications/">Apply Now <?= icon('arrow') ?></a>
    </nav>
    <button class="nav-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><?= icon('menu', 'ico i-open') ?><?= icon('x', 'ico i-close') ?></button>
  </div>
</header>
<main id="main">
<?php
}

function breadcrumbs(array $crumbs): string
{
    $out = '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => [$name, $path]) {
        $out .= $i === $last
            ? '<li aria-current="page">' . e($name) . '</li>'
            : '<li><a href="' . e($path) . '">' . e($name) . '</a></li>';
    }
    return $out . '</ol></nav>';
}

/** Inner-page hero banner with the brand arcs and breadcrumbs. */
function page_hero(string $h1, string $intro, array $crumbs, string $bg = '', string $eyebrow = ''): void
{
    ?>
<section class="page-hero"<?= $bg ? ' style="--hero-img:url(\'' . e($bg) . '\')"' : '' ?>>
  <canvas class="net-canvas" aria-hidden="true"></canvas>
  <div class="arcs" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap page-hero__in">
    <?= breadcrumbs($crumbs) ?>
<?php if ($eyebrow): ?>    <p class="eyebrow"><?= e($eyebrow) ?></p>
<?php endif; ?>
    <h1><?= $h1 ?></h1>
    <p class="page-hero__intro"><?= $intro ?></p>
  </div>
</section>
<?php
}

function cta_band(string $title = 'Ready for your next move?', string $text = ''): string
{
    $text = $text ?: 'Whether you are looking for work or looking for people, the Best Jobs Pro team answers the phone 24/7, and job seekers never pay a fee.';
    return '<section class="cta-band"><div class="arcs" aria-hidden="true"><span></span><span></span></div><div class="wrap cta-band__in reveal">'
        . '<div><h2>' . e($title) . '</h2><p>' . e($text) . '</p></div>'
        . '<div class="cta-band__btns"><a class="btn btn--light" href="/applications/">' . icon('file') . ' Apply for a Job</a>'
        . '<a class="btn btn--ghost-light" href="tel:' . SITE_TEL . '">' . icon('phone') . ' ' . SITE_PHONE . '</a></div>'
        . '</div></section>';
}

function faq_block(array $faqs, string $title = 'Frequently asked questions', string $id = 'faq'): string
{
    $out = '<section class="faq" id="' . e($id) . '"><h2>' . e($title) . '</h2><div class="faq__list">';
    foreach ($faqs as $f) {
        $out .= '<details class="faq__item"><summary>' . e($f['q']) . '</summary><div class="faq__a"><p>' . e($f['a']) . '</p></div></details>';
    }
    return $out . '</div></section>';
}

function page_end(array $scripts = []): void
{
    $year = date('Y');
    ?>
</main>
<footer class="site-footer">
  <div class="arcs arcs--footer" aria-hidden="true"><span></span><span></span></div>
  <div class="wrap site-footer__grid">
    <div class="site-footer__about">
      <a class="brand brand--footer" href="/"><img src="/assets/img/site/Best-Jobs-Pro-Logo.webp" alt="Best Jobs Pro logo" width="500" height="426" loading="lazy"></a>
      <p>Best Jobs Pro is a Texas staffing agency and recruiter that matches job seekers with employers who value them. No employment or processing fees, ever.</p>
      <a class="btn btn--sm" href="/applications/">Submit Your Application <?= icon('arrow') ?></a>
    </div>
    <div>
      <h2 class="site-footer__h">Company</h2>
      <ul>
        <li><a href="/about/">About Best Jobs Pro</a></li>
        <li><a href="/our-services/">Staffing Services</a></li>
        <li><a href="/blog/">Career Blog</a></li>
        <li><a href="/contact-us/">Contact Us</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
      </ul>
    </div>
    <div>
      <h2 class="site-footer__h">Job Seekers &amp; Employers</h2>
      <ul>
        <li><a href="/job-postings/">Job Postings</a></li>
        <li><a href="/applications/">Apply Online</a></li>
        <li><a href="/employers/">Hire Talent</a></li>
        <li><a href="/career-tools/">Career Tools</a></li>
        <li><a href="/career-tools/job-match-quiz/">Job Match Quiz</a></li>
      </ul>
    </div>
    <div>
      <h2 class="site-footer__h">Get in Touch</h2>
      <ul class="site-footer__contact">
        <li><a href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> <?= SITE_PHONE ?></a></li>
        <li><a href="mailto:<?= SITE_EMAIL ?>"><?= icon('mail') ?> <?= SITE_EMAIL ?></a></li>
        <li><a href="<?= SITE_MAP ?>" target="_blank" rel="noopener"><?= icon('pin') ?> <?= SITE_STREET ?><br><?= SITE_CITY ?>, <?= SITE_REGION ?> <?= SITE_ZIP ?>, USA</a></li>
        <li><span><?= icon('clock') ?> Phones answered 24/7</span></li>
      </ul>
    </div>
  </div>
  <div class="wrap site-footer__bar">
    <p>&copy; <?= $year ?> Best Jobs Pro &bull; All Rights Reserved.</p>
    <a href="#top" class="to-top"><?= icon('arrow') ?> Back to top</a>
  </div>
</footer>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
<?php foreach ($scripts as $s): ?>
<script src="<?= asset($s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}
