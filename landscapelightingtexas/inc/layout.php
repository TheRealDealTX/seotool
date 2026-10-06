<?php
// Page shell: <head>, header, page hero, article wrapper, footer and JSON-LD.
defined('LLT') or die(http_response_code(404));

function e($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8', false); }
function abs_url(string $path): string { return SITE_ORIGIN . $path; }
function img_url(?string $key, int $w = 1600): string {
    return $key ? "/assets/img/{$key}-{$w}.webp" : '/assets/img/og-image.jpg';
}
function fmt_date(string $ymd): string { return date('F j, Y', strtotime($ymd)); }

/** Shared JSON-LD nodes: the business, the website. */
function base_schema(): array {
    global $AREAS;
    $served = [['@type' => 'State', 'name' => 'Texas']];
    foreach ($AREAS as $a) foreach ($a[2] as $c) $served[] = ['@type' => 'City', 'name' => "$c, TX"];
    return [
        [
            '@type' => ['LocalBusiness', 'HomeAndConstructionBusiness'],
            '@id' => SITE_ORIGIN . '/#business',
            'name' => SITE_NAME,
            'url' => SITE_ORIGIN . '/',
            'logo' => SITE_ORIGIN . '/assets/img/logo.webp',
            'image' => SITE_ORIGIN . '/assets/img/architectural-uplighting-1600.webp',
            'description' => 'Landscape Lighting Texas designs, installs and maintains custom low-voltage LED landscape and outdoor lighting for homes and businesses across Texas.',
            'telephone' => '+1-281-704-7210',
            'email' => EMAIL,
            'priceRange' => '$$$',
            'address' => ['@type' => 'PostalAddress', 'addressRegion' => 'TX', 'addressCountry' => 'US'],
            'areaServed' => $served,
            'openingHoursSpecification' => [[
                '@type' => 'OpeningHoursSpecification',
                'dayOfWeek' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                'opens' => '08:00', 'closes' => '18:00',
            ]],
            'aggregateRating' => ['@type' => 'AggregateRating', 'ratingValue' => '4.9', 'bestRating' => '5', 'reviewCount' => '6'],
            'knowsAbout' => ['Landscape lighting', 'Architectural uplighting', 'Tree lighting', 'Pathway lighting', 'Low-voltage LED lighting', 'Smart outdoor lighting'],
        ],
        [
            '@type' => 'WebSite', '@id' => SITE_ORIGIN . '/#website',
            'url' => SITE_ORIGIN . '/', 'name' => SITE_NAME,
            'publisher' => ['@id' => SITE_ORIGIN . '/#business'], 'inLanguage' => 'en-US',
        ],
    ];
}

function breadcrumb_trail(array $P): array {
    global $PAGES;
    $trail = [['Home', '/']];
    $path = $P['path'];
    if ($path === '/') return $trail;
    if ($P['type'] === 'post') {
        $trail[] = ['Blog', '/blog/'];
    } elseif ($path === '/category/general/') {
        $trail[] = ['Blog', '/blog/'];
    } else {
        $parts = array_values(array_filter(explode('/', $path)));
        $acc = '/';
        for ($i = 0; $i < count($parts) - 1; $i++) {
            $acc .= $parts[$i] . '/';
            if (isset($PAGES[$acc])) $trail[] = [short_name($PAGES[$acc]), $acc];
        }
    }
    $trail[] = [short_name($P), $path];
    return $trail;
}

function short_name(array $P): string {
    $map = ['/services/' => 'Services', '/areas/' => 'Service Areas', '/tools/' => 'Tools', '/blog/' => 'Blog',
            '/about-us/' => 'About Us', '/quote/' => 'Free Quote', '/gallery/' => 'Gallery', '/faq/' => 'FAQ'];
    return $map[$P['path']] ?? $P['h1'];
}

function page_schema(array $P): array {
    $url = abs_url($P['path']);
    $graph = base_schema();
    $graph[] = [
        '@type' => 'WebPage',
        '@id' => $url . '#webpage', 'url' => $url, 'name' => $P['title'],
        'description' => $P['description'], 'isPartOf' => ['@id' => SITE_ORIGIN . '/#website'],
        'about' => ['@id' => SITE_ORIGIN . '/#business'], 'inLanguage' => 'en-US',
        'primaryImageOfPage' => abs_url(img_url($P['image'])),
        'dateModified' => $P['modified'],
    ];
    $trail = breadcrumb_trail($P);
    if (count($trail) > 1) {
        $items = [];
        foreach ($trail as $i => [$name, $href]) {
            $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($href)];
        }
        $graph[] = ['@type' => 'BreadcrumbList', '@id' => $url . '#breadcrumb', 'itemListElement' => $items];
    }
    if ($P['type'] === 'post') {
        $graph[] = [
            '@type' => 'BlogPosting', '@id' => $url . '#article', 'headline' => $P['h1'],
            'description' => $P['description'], 'image' => abs_url(img_url($P['image'])),
            'datePublished' => $P['date'], 'dateModified' => $P['modified'],
            'author' => ['@type' => 'Organization', 'name' => SITE_NAME . ' Design Team', 'url' => SITE_ORIGIN . '/about-us/'],
            'publisher' => ['@id' => SITE_ORIGIN . '/#business'],
            'mainEntityOfPage' => ['@id' => $url . '#webpage'],
            'articleSection' => 'General', 'wordCount' => $P['_words'] ?? null,
        ];
    }
    if ($P['type'] === 'service') {
        $graph[] = [
            '@type' => 'Service', '@id' => $url . '#service', 'name' => $P['h1'],
            'serviceType' => $P['h1'], 'description' => $P['description'],
            'provider' => ['@id' => SITE_ORIGIN . '/#business'],
            'areaServed' => ['@type' => 'State', 'name' => 'Texas'], 'url' => $url,
        ];
    }
    if ($P['type'] === 'area') {
        $graph[] = [
            '@type' => 'Service', '@id' => $url . '#service', 'name' => $P['h1'],
            'serviceType' => 'Landscape lighting design and installation',
            'provider' => ['@id' => SITE_ORIGIN . '/#business'],
            'areaServed' => array_map(fn($c) => ['@type' => 'City', 'name' => "$c, TX"], $P['_cities'] ?? []),
        ];
    }
    if ($P['type'] === 'tool') {
        $graph[] = [
            '@type' => 'WebApplication', '@id' => $url . '#app', 'name' => $P['h1'], 'url' => $url,
            'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any (web browser)',
            'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
            'provider' => ['@id' => SITE_ORIGIN . '/#business'],
        ];
    }
    if (!empty($GLOBALS['FAQ_SCHEMA'])) {
        $faq = ['@type' => 'FAQPage', '@id' => $url . '#faq', 'mainEntity' => []];
        foreach ($GLOBALS['FAQ_SCHEMA'] as [$q, $a]) {
            $faq['mainEntity'][] = ['@type' => 'Question', 'name' => $q,
                'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(preg_replace('/\s+/', ' ', strip_tags($a)))]];
        }
        $graph[] = $faq;
    }
    if (!empty($P['schema'])) foreach ($P['schema'] as $node) $graph[] = $node;
    return ['@context' => 'https://schema.org', '@graph' => array_values(array_filter($graph))];
}

/** Adds id="" to every <h2> in an article body and returns [body, toc]. */
function add_heading_ids(string $html): array {
    $toc = []; $seen = [];
    $html = preg_replace_callback('#<h2([^>]*)>(.*?)</h2>#s', function ($m) use (&$toc, &$seen) {
        $text = trim(strip_tags($m[2]));
        if (preg_match('/id="([^"]+)"/', $m[1], $idm)) { $id = $idm[1]; }
        else {
            $id = trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($text)), '-');
            $base = $id; $n = 2;
            while (isset($seen[$id])) $id = $base . '-' . $n++;
            $m[1] .= ' id="' . $id . '"';
        }
        $seen[$id] = 1;
        $toc[] = [$id, $text];
        return '<h2' . $m[1] . '>' . $m[2] . '</h2>';
    }, $html);
    return [$html, $toc];
}

function render_page(array $P): void {
    global $PAGES;
    $GLOBALS['FAQ_SCHEMA'] = [];
    ob_start();
    include __DIR__ . '/../' . $P['file'];
    $body = ob_get_clean();

    $words = str_word_count(strip_tags($body));
    $P['_words'] = $words;
    header('Content-Type: text/html; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');

    render_head($P);
    render_header($P);
    echo '<main id="main">';
    if ($P['type'] === 'home') {
        echo $body;
    } elseif ($P['type'] === 'post') {
        render_post($P, $body, $words);
    } else {
        if (empty($P['no_hero'])) render_hero($P);
        echo $body;
    }
    echo '</main>';
    render_footer($P);
}

function render_head(array $P): void {
    $canonical = abs_url($P['path']);
    $og = abs_url(img_url($P['image']));
    $schema = json_encode(page_schema($P), JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG);
    $v = ASSET_VER;
    ?><!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title><?= e($P['title']) ?></title>
<meta name="description" content="<?= e($P['description']) ?>">
<?php if (!empty($P['noindex'])): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta name="theme-color" content="#070b18">
<meta property="og:type" content="<?= $P['type'] === 'post' ? 'article' : 'website' ?>">
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:title" content="<?= e($P['title']) ?>">
<meta property="og:description" content="<?= e($P['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($og) ?>">
<meta property="og:locale" content="en_US">
<?php if ($P['type'] === 'post'): ?>
<meta property="article:published_time" content="<?= e($P['date']) ?>">
<meta property="article:modified_time" content="<?= e($P['modified']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($P['title']) ?>">
<meta name="twitter:description" content="<?= e($P['description']) ?>">
<meta name="twitter:image" content="<?= e($og) ?>">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="<?= SITE_NAME ?> Blog" href="<?= SITE_ORIGIN ?>/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= $v ?>">
<?php if (!empty($P['preload'])): ?><link rel="preload" as="image" href="<?= e($P['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<script type="application/ld+json"><?= $schema ?></script>
</head>
<?php
}

function nav_children(string $key): array {
    global $SERVICES, $AREAS, $TOOLS;
    if ($key === 'services') return array_map(fn($s, $v) => [$v[0], "/services/$s/", $v[1]], array_keys($SERVICES), $SERVICES);
    if ($key === 'areas')    return array_map(fn($s, $v) => [$v[0], "/areas/$s/", $v[1]], array_keys($AREAS), $AREAS);
    if ($key === 'tools')    return array_map(fn($s, $v) => [$v[0], $s, $v[1]], array_keys($TOOLS), $TOOLS);
    return [];
}

function render_header(array $P): void {
    global $NAV;
    $cur = $P['path'];
    $home = $P['type'] === 'home';
    ?>
<body class="<?= $home ? 'is-home' : 'is-inner' ?> type-<?= e($P['type']) ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"><span></span></div>
<div class="cursor-glow" aria-hidden="true"></div>
<header class="site-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="<?= SITE_NAME ?> home">
      <img src="/assets/img/logo.webp" alt="<?= SITE_NAME ?>" width="623" height="112">
    </a>
    <nav class="main-nav" aria-label="Main" data-nav>
      <ul>
      <?php foreach ($NAV as $item):
          $active = $cur === $item['href'] || ($item['href'] !== '/' && str_starts_with($cur, $item['href'])); ?>
        <li class="<?= !empty($item['children']) ? 'has-menu' : '' ?><?= $active ? ' is-active' : '' ?>">
          <a href="<?= $item['href'] ?>"><?= e($item['label']) ?></a>
          <?php if (!empty($item['children'])): ?>
          <button class="submenu-toggle" aria-expanded="false" aria-label="Show <?= e($item['label']) ?> menu"><svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M6 9l6 6 6-6" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>
          <div class="mega">
            <div class="mega-grid">
            <?php foreach (nav_children($item['children']) as [$label, $href, $blurb]): ?>
              <a href="<?= e($href) ?>" class="mega-link"><strong><?= e($label) ?></strong><span><?= e($blurb) ?></span></a>
            <?php endforeach; ?>
            </div>
            <a class="mega-all" href="<?= $item['href'] ?>">View all <?= e(strtolower($item['label'])) ?> →</a>
          </div>
          <?php endif; ?>
        </li>
      <?php endforeach; ?>
      </ul>
      <div class="nav-mobile-cta">
        <a class="btn btn-gold" href="/quote/">Get a Free Quote</a>
        <a class="btn btn-ghost" href="<?= PHONE_HREF ?>"><?= PHONE ?></a>
      </div>
    </nav>
    <div class="header-cta">
      <a class="header-phone" href="<?= PHONE_HREF ?>"><?= icon('phone') ?><span><?= PHONE ?></span></a>
      <a class="btn btn-gold btn-sm magnetic" href="/quote/">Free Quote</a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false" data-nav-toggle><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<?php
}

function render_hero(array $P): void {
    $img = $P['hero_image'] ?? $P['image'];
    $legal = $P['type'] === 'legal';
    ?>
<section class="page-hero<?= $img && !$legal ? ' has-image' : ' no-image' ?>">
  <?php if ($img && !$legal): ?>
  <div class="page-hero-bg" data-parallax="0.25"><img src="<?= img_url($img) ?>" alt="" width="1536" height="1024" fetchpriority="high"></div>
  <?php endif; ?>
  <div class="page-hero-glow" aria-hidden="true"></div>
  <div class="container page-hero-inner">
    <?php render_breadcrumbs($P); ?>
    <?php if (!empty($P['eyebrow'])): ?><p class="eyebrow reveal"><?= e($P['eyebrow']) ?></p><?php endif; ?>
    <h1 class="page-title reveal" data-split><?= e($P['h1']) ?></h1>
    <?php if (!empty($P['lead'])): ?><p class="lead reveal"><?= $P['lead'] ?></p><?php endif; ?>
    <?php if (empty($P['hero_no_cta']) && !$legal): ?>
    <div class="hero-actions reveal">
      <a class="btn btn-gold magnetic" href="/quote/">Get a Free Quote</a>
      <a class="btn btn-ghost" href="<?= PHONE_HREF ?>"><?= icon('phone') ?> <?= PHONE ?></a>
    </div>
    <?php endif; ?>
    <?php if ($legal): ?><p class="hero-meta">Last updated: <?= fmt_date($P['modified']) ?></p><?php endif; ?>
  </div>
</section>
<?php
}

function render_breadcrumbs(array $P): void {
    $trail = breadcrumb_trail($P);
    if (count($trail) < 2) return;
    echo '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>';
    foreach ($trail as $i => [$name, $href]) {
        $last = $i === count($trail) - 1;
        echo $last ? '<li aria-current="page">' . e($name) . '</li>' : '<li><a href="' . e($href) . '">' . e($name) . '</a></li>';
    }
    echo '</ol></nav>';
}

function render_post(array $P, string $body, int $words): void {
    [$body, $toc] = add_heading_ids($body);
    $mins = max(1, (int)round($words / 225));
    ?>
<article class="post">
  <header class="post-hero">
    <div class="post-hero-bg" data-parallax="0.2"><img src="<?= img_url($P['image']) ?>" alt="" width="1536" height="1024" fetchpriority="high"></div>
    <div class="container post-hero-inner">
      <?php render_breadcrumbs($P); ?>
      <a class="chip reveal" href="/category/general/">General</a>
      <h1 class="post-title reveal" data-split><?= e($P['h1']) ?></h1>
      <p class="post-meta reveal">
        <span><?= icon('calendar') ?> <time datetime="<?= e($P['date']) ?>"><?= fmt_date($P['date']) ?></time></span>
        <?php if ($P['modified'] !== $P['date']): ?><span>Updated <time datetime="<?= e($P['modified']) ?>"><?= fmt_date($P['modified']) ?></time></span><?php endif; ?>
        <span><?= icon('clock') ?> <?= $mins ?> min read</span>
        <span>By the <?= SITE_NAME ?> design team</span>
      </p>
    </div>
  </header>
  <div class="container post-layout">
    <aside class="post-aside">
      <?php if (count($toc) > 2): ?>
      <nav class="toc" aria-label="On this page" data-toc>
        <p class="toc-title">On this page</p>
        <ol><?php foreach ($toc as [$id, $text]): ?><li><a href="#<?= e($id) ?>"><?= e($text) ?></a></li><?php endforeach; ?></ol>
      </nav>
      <?php endif; ?>
      <div class="aside-cta">
        <p class="aside-cta-title">See it on your home</p>
        <p>Free dusk consultation anywhere in Texas.</p>
        <a class="btn btn-gold btn-sm" href="/quote/">Get a Free Quote</a>
      </div>
    </aside>
    <div class="prose post-body"><?= $body ?></div>
  </div>
  <div class="container post-foot">
    <div class="author-box reveal">
      <img src="/assets/img/icon-192.png" alt="" width="64" height="64" loading="lazy">
      <div><p class="author-name">Written by the <?= SITE_NAME ?> design team</p>
      <p>Our lighting designers have planned and aimed more than 1,400 outdoor lighting systems across Texas. <a href="/about-us/">More about us</a>.</p></div>
    </div>
  </div>
</article>
<?php
    related_posts($P['path']);
    cta_band();
}

function render_footer(array $P): void {
    global $SERVICES, $AREAS, $TOOLS;
    $v = ASSET_VER;
    ?>
<footer class="site-footer">
  <div class="footer-glow" aria-hidden="true"></div>
  <div class="container footer-top">
    <div class="footer-brand">
      <a href="/" class="brand"><img src="/assets/img/logo.webp" alt="<?= SITE_NAME ?>" width="623" height="112" loading="lazy"></a>
      <p><?= SITE_NAME ?> designs, installs and maintains custom low-voltage LED outdoor lighting for homes and businesses across the Lone Star State.</p>
      <ul class="footer-contact">
        <li><?= icon('phone') ?><a href="<?= PHONE_HREF ?>"><?= PHONE ?></a></li>
        <li><?= icon('mail') ?><a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a></li>
        <li><?= icon('clock') ?><span><?= HOURS ?></span></li>
        <li><?= icon('pin') ?><span>Serving all of Texas</span></li>
      </ul>
    </div>
    <div class="footer-col">
      <p class="footer-title">Services</p>
      <ul><?php foreach ($SERVICES as $slug => $s): ?><li><a href="/services/<?= $slug ?>/"><?= e($s[0]) ?></a></li><?php endforeach; ?></ul>
    </div>
    <div class="footer-col">
      <p class="footer-title">Service Areas</p>
      <ul><?php foreach ($AREAS as $slug => $a): ?><li><a href="/areas/<?= $slug ?>/"><?= e($a[0]) ?></a></li><?php endforeach; ?>
      <li><a href="/areas/">All Texas areas</a></li></ul>
    </div>
    <div class="footer-col">
      <p class="footer-title">Tools</p>
      <ul><?php foreach ($TOOLS as $href => $t): ?><li><a href="<?= $href ?>"><?= e($t[0]) ?></a></li><?php endforeach; ?></ul>
    </div>
    <div class="footer-col">
      <p class="footer-title">Company</p>
      <ul>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="/gallery/">Gallery</a></li>
        <li><a href="/faq/">FAQ</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/quote/">Get a Free Quote</a></li>
      </ul>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>© <?= date('Y') ?> <?= SITE_NAME ?> · All rights reserved.</p>
    <ul><li><a href="/privacy-policy/">Privacy Policy</a></li><li><a href="/terms-of-service/">Terms of Service</a></li><li><a href="/sitemap/">Sitemap</a></li></ul>
  </div>
</footer>
<a class="mobile-call" href="<?= PHONE_HREF ?>" aria-label="Call <?= SITE_NAME ?>"><?= icon('phone') ?></a>
<script src="/assets/js/site.js?v=<?= $v ?>" defer></script>
<?php if (!empty($P['tools_js'])): ?><script src="/assets/js/tools.js?v=<?= $v ?>" defer></script><?php endif; ?>
</body>
</html>
<?php
}
