<?php
// Shared layout + helpers used by every page template.
//
// A page template under pages/ just echoes the content of <main>. It can:
//   hero([...])               page hero with H1 and breadcrumbs
//   faq_section($items, $h)   FAQ accordion; also feeds FAQPage JSON-LD
//   cta_band()                standard "start your project" band
//   related($paths, $h)       card links to other pages in the route table
//   $GLOBALS['schema'][]      extra JSON-LD nodes for this page
//   $GLOBALS['scripts'][]     extra JS files under /assets/js/
// The router renders the page into a buffer first, so templates can set
// these before the <head> is printed.

$GLOBALS['schema']  = [];
$GLOBALS['faqs']    = [];
$GLOBALS['scripts'] = [];

function e(?string $s): string
{
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function abs_url(string $path): string
{
    return SITE_URL . $path;
}

function img_url(string $file): string
{
    return '/assets/img/' . $file;
}

function page_meta(string $path): ?array
{
    return PAGES[$path] ?? null;
}

// Breadcrumb trail for a path: [[label, path], ...] starting at Home.
function trail(string $path): array
{
    $out = [];
    $p = $path;
    while ($p !== null && isset(PAGES[$p])) {
        array_unshift($out, [PAGES[$p]['crumb'], $p]);
        $p = PAGES[$p]['parent'] ?? ($p === '/' ? null : '/');
    }
    return $out;
}

function hero(array $h): void
{
    $path = $GLOBALS['path'];
    $img  = $h['image'] ?? null;
    $style = $img ? ' style="--hero-img:url(\'' . e(img_url($img)) . '\')"' : '';
    echo '<section class="hero hero--page' . ($img ? ' hero--img' : '') . '"' . $style . '><div class="wrap">';
    $t = trail($path);
    if (count($t) > 1) {
        echo '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
        foreach ($t as $i => [$label, $p]) {
            echo $i === count($t) - 1
                ? '<li aria-current="page">' . e($label) . '</li>'
                : '<li><a href="' . e($p) . '">' . e($label) . '</a></li>';
        }
        echo '</ol></nav>';
    }
    if (!empty($h['eyebrow'])) echo '<p class="eyebrow">' . e($h['eyebrow']) . '</p>';
    echo '<h1>' . $h['h1'] . '</h1>';
    if (!empty($h['lead'])) echo '<p class="lead">' . $h['lead'] . '</p>';
    if (!empty($h['meta'])) echo '<p class="hero-meta">' . $h['meta'] . '</p>';
    if (($h['cta'] ?? true) !== false) {
        echo '<div class="btn-row"><a class="btn btn--gold" href="/contact-us/">Get a Free Design Consult</a>'
           . '<a class="btn btn--ghost" href="' . PHONE_HREF . '">Call ' . PHONE . '</a></div>';
    }
    echo '</div></section>';
}

// $items: [[question, answer_html], ...]
function faq_section(array $items, string $heading = 'Frequently Asked Questions', string $intro = ''): void
{
    echo '<section class="section faq" id="faq"><div class="wrap wrap--narrow"><h2>' . e($heading) . '</h2>';
    if ($intro) echo '<p class="section-intro">' . $intro . '</p>';
    foreach ($items as [$q, $a]) {
        $GLOBALS['faqs'][] = [$q, $a];
        echo '<details class="faq-item"><summary>' . e($q) . '</summary><div class="faq-a">' . $a . '</div></details>';
    }
    echo '</div></section>';
}

function cta_band(string $title = 'Ready to Build Your Tiny Home in Texas?', string $text = ''): void
{
    $text = $text ?: 'Tell Cowboy Tiny Homes about your land, budget and must-haves. We will map out what you can build, what it will cost and how long it will take — free, with no obligation.';
    echo '<section class="cta-band"><div class="wrap"><div><h2>' . e($title) . '</h2><p>' . e($text) . '</p></div>'
       . '<div class="btn-row"><a class="btn btn--gold" href="/contact-us/">Start My Project</a>'
       . '<a class="btn btn--ghost" href="' . PHONE_HREF . '">' . PHONE . '</a></div></div></section>';
}

// Card links to other routed pages. $paths: list of paths, or [path => blurb].
function related(array $paths, string $heading = 'Keep Exploring'): void
{
    echo '<section class="section section--alt"><div class="wrap"><h2>' . e($heading) . '</h2><div class="cards cards--links">';
    foreach ($paths as $k => $v) {
        [$p, $blurb] = is_int($k) ? [$v, PAGES[$v]['desc'] ?? ''] : [$k, $v];
        $m = PAGES[$p] ?? null;
        if (!$m) continue;
        echo '<a class="card card--link" href="' . e($p) . '"><span class="card-kicker">' . e(kicker($m['type'])) . '</span>'
           . '<strong>' . e($m['crumb']) . '</strong><span>' . e($blurb) . '</span><span class="card-more">Read more →</span></a>';
    }
    echo '</div></div></section>';
}

function kicker(string $type): string
{
    return ['service' => 'Home Build', 'area' => 'Service Area', 'guide' => 'Guide', 'post' => 'Blog', 'tool' => 'Free Tool',
            'hub' => 'Explore', 'page' => 'Cowboy Tiny Homes', 'home' => 'Home', 'legal' => 'Info'][$type] ?? 'Explore';
}

// ---------------------------------------------------------------------------
// JSON-LD

function org_node(): array
{
    return [
        '@type' => ['HomeAndConstructionBusiness', 'GeneralContractor'],
        '@id'   => SITE_URL . '/#business',
        'name'  => SITE_NAME,
        'url'   => SITE_URL . '/',
        'telephone' => '+1-' . PHONE,
        'email' => EMAIL,
        'logo'  => ['@type' => 'ImageObject', 'url' => abs_url(img_url('Cowboy-Tiny-Homes-Org-Logo.webp')), 'width' => 500, 'height' => 500],
        'image' => abs_url(img_url('og-cowboy-tiny-homes.jpg')),
        'description' => 'Cowboy Tiny Homes is a Texas tiny home builder and designer offering custom tiny homes, accessory dwelling units, casitas, park model homes, tiny homes on wheels and home remodel design.',
        'priceRange' => '$$',
        'slogan' => 'Big Ideas, Built Small.',
        'areaServed' => array_merge(
            [['@type' => 'State', 'name' => 'Texas']],
            array_map(fn($c) => ['@type' => 'City', 'name' => $c . ', TX'], array_values(SERVICE_CITIES))
        ),
        'knowsAbout' => ['Tiny homes', 'Accessory dwelling units', 'Casitas', 'Park model homes', 'Tiny homes on wheels', 'Home remodel design', 'International Residential Code'],
        'contactPoint' => ['@type' => 'ContactPoint', 'telephone' => '+1-' . PHONE, 'email' => EMAIL, 'contactType' => 'sales', 'areaServed' => 'US-TX', 'availableLanguage' => 'English'],
    ];
}

function build_schema(string $path, array $m): array
{
    $url = abs_url($path);
    $graph = [org_node(), [
        '@type' => 'WebSite', '@id' => SITE_URL . '/#website', 'url' => SITE_URL . '/', 'name' => SITE_NAME,
        'publisher' => ['@id' => SITE_URL . '/#business'], 'inLanguage' => 'en-US',
    ]];
    $webpage = [
        '@type' => $path === '/faqs/' ? ['WebPage', 'FAQPage'] : 'WebPage',
        '@id' => $url . '#webpage', 'url' => $url, 'name' => $m['title'], 'description' => $m['desc'],
        'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#business'],
        'primaryImageOfPage' => abs_url(img_url($m['image'])), 'inLanguage' => 'en-US',
        'dateModified' => $m['updated'] ?? '2026-10-28',
    ];
    $t = trail($path);
    if (count($t) > 1) {
        $webpage['breadcrumb'] = ['@id' => $url . '#breadcrumb'];
        $graph[] = ['@type' => 'BreadcrumbList', '@id' => $url . '#breadcrumb', 'itemListElement' => array_map(
            fn($i, $c) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $c[0], 'item' => abs_url($c[1])],
            array_keys($t), $t
        )];
    }
    if ($GLOBALS['faqs']) {
        $faq = ['mainEntity' => array_map(fn($f) => [
            '@type' => 'Question', 'name' => $f[0],
            'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(preg_replace('/\s+/', ' ', strip_tags($f[1])))],
        ], $GLOBALS['faqs'])];
        if ($path === '/faqs/') {
            $webpage += $faq;
        } else {
            $graph[] = ['@type' => 'FAQPage', '@id' => $url . '#faq', 'isPartOf' => ['@id' => $url . '#webpage']] + $faq;
        }
    }
    $graph[] = $webpage;
    switch ($m['type']) {
        case 'service':
        case 'area':
            $graph[] = [
                '@type' => 'Service', '@id' => $url . '#service',
                'name' => $m['crumb'] . ($m['type'] === 'area' ? ' Tiny Home Builders' : ''),
                'serviceType' => $m['crumb'], 'description' => $m['desc'], 'url' => $url,
                'provider' => ['@id' => SITE_URL . '/#business'],
                'areaServed' => isset($m['city'])
                    ? ['@type' => 'City', 'name' => $m['city'] . ', TX']
                    : ['@type' => 'State', 'name' => 'Texas'],
                'image' => abs_url(img_url($m['image'])),
            ];
            break;
        case 'guide':
        case 'post':
            $graph[] = [
                '@type' => $m['type'] === 'post' ? 'BlogPosting' : 'Article', '@id' => $url . '#article', 'headline' => $m['title'], 'description' => $m['desc'],
                'image' => abs_url(img_url($m['image'])), 'datePublished' => $m['published'] ?? '2026-10-28',
                'dateModified' => $m['updated'] ?? ($m['published'] ?? '2026-10-28'),
                'author' => ['@type' => 'Organization', 'name' => SITE_NAME, 'url' => SITE_URL . '/'],
                'publisher' => ['@id' => SITE_URL . '/#business'], 'mainEntityOfPage' => ['@id' => $url . '#webpage'],
            ];
            break;
        case 'tool':
            $graph[] = [
                '@type' => 'WebApplication', '@id' => $url . '#app', 'name' => $m['crumb'], 'url' => $url,
                'description' => $m['desc'], 'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any',
                'browserRequirements' => 'Requires JavaScript',
                'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
                'provider' => ['@id' => SITE_URL . '/#business'],
            ];
            break;
    }
    foreach ($GLOBALS['schema'] as $node) $graph[] = $node;
    return ['@context' => 'https://schema.org', '@graph' => $graph];
}

// ---------------------------------------------------------------------------
// Page shell

function render_page(string $path, array $m, string $content, int $status = 200): void
{
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    $canonical = abs_url($path);
    $og = abs_url(img_url($m['image'] ?? 'og-cowboy-tiny-homes.jpg'));
    $robots = $status === 200 ? 'index, follow, max-image-preview:large' : 'noindex, follow';
    $schema = $status === 200 ? build_schema($path, $m) : null;
    ?><!DOCTYPE html>
<html lang="en-US">
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
<title><?= e($m['title']) ?></title>
<meta name="description" content="<?= e($m['desc']) ?>">
<meta name="robots" content="<?= $robots ?>">
<?php if ($status === 200): ?><link rel="canonical" href="<?= e($canonical) ?>">
<?php endif; ?>
<meta property="og:type" content="<?= in_array($m['type'], ['guide', 'post'], true) ? 'article' : 'website' ?>">
<?php if ($m['type'] === 'post'): ?><meta property="article:published_time" content="<?= e($m['published']) ?>">
<link rel="alternate" type="application/rss+xml" title="<?= SITE_NAME ?> Blog" href="/blog/feed.xml">
<?php endif; ?>
<meta property="og:site_name" content="<?= SITE_NAME ?>">
<meta property="og:title" content="<?= e($m['title']) ?>">
<meta property="og:description" content="<?= e($m['desc']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($og) ?>">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($m['title']) ?>">
<meta name="twitter:description" content="<?= e($m['desc']) ?>">
<meta name="twitter:image" content="<?= e($og) ?>">
<meta name="theme-color" content="#282a39">
<meta name="geo.region" content="US-TX">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="96x96" href="/favicon-96x96.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Montserrat:wght@600;700;800&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_VER ?>">
<?php if ($schema): ?><script type="application/ld+json"><?= json_encode($schema, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
<?php endif; ?>
</head>
<body class="type-<?= e($m['type']) ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span>★ Texas tiny home builders — custom homes, ADUs, park models &amp; tiny homes on wheels</span>
  <span class="topbar-links"><a href="<?= PHONE_HREF ?>"><?= PHONE ?></a><a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a></span>
</div></div>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= SITE_NAME ?> home">
      <img src="/assets/img/Cowboy-Tiny-Homes-Logo.webp" alt="<?= SITE_NAME ?> logo" width="512" height="330">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as [$label, $href, $children]):
        $active = ($href === $path || ($children && in_array($path, array_column($children, 1), true))) ? ' is-active' : ''; ?>
        <li class="<?= $children ? 'has-sub' : '' ?><?= $active ?>">
          <a href="<?= e($href) ?>"><?= e($label) ?></a>
<?php if ($children): ?>
          <button class="sub-toggle" aria-label="Show <?= e($label) ?> menu" aria-expanded="false"></button>
          <ul class="sub">
<?php foreach ($children as [$cl, $ch]): ?>
            <li><a href="<?= e($ch) ?>"><?= e($cl) ?></a></li>
<?php endforeach; ?>
          </ul>
<?php endif; ?>
        </li>
<?php endforeach; ?>
        <li class="nav-cta"><a class="btn btn--gold btn--sm" href="/contact-us/">Free Consult</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main">
<?= $content ?>
</main>
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="/assets/img/Cowboy-Tiny-Homes-Footer-Image.webp" alt="<?= SITE_NAME ?>" width="500" height="167" loading="lazy">
      <p><?= SITE_NAME ?> designs and builds custom tiny homes, ADUs, casitas, park model homes and tiny homes on wheels for homeowners across Texas.</p>
      <p class="footer-contact"><a href="<?= PHONE_HREF ?>"><?= PHONE ?></a><br><a href="mailto:<?= EMAIL ?>"><?= EMAIL ?></a></p>
    </div>
    <div>
      <h2>Home Builds</h2>
      <ul>
        <li><a href="/custom-tiny-homes-texas/">Custom Tiny Homes</a></li>
        <li><a href="/adu-builders-texas/">ADUs &amp; Casitas</a></li>
        <li><a href="/tiny-homes-on-wheels-texas/">Tiny Homes on Wheels</a></li>
        <li><a href="/park-model-homes-texas/">Park Model Homes</a></li>
        <li><a href="/tiny-house-design-services/">Design Services</a></li>
        <li><a href="/home-remodel-design-texas/">Home Remodel Design</a></li>
        <li><a href="/home-designs/">House Designs</a></li>
      </ul>
    </div>
    <div>
      <h2>Service Areas</h2>
      <ul>
<?php foreach (SERVICE_CITIES as $slug => $city): ?>
        <li><a href="/tiny-home-builders-<?= $slug ?>/">Tiny Home Builders <?= $city ?></a></li>
<?php endforeach; ?>
        <li><a href="/service-areas/">All Texas Service Areas</a></li>
      </ul>
    </div>
    <div>
      <h2>Plan &amp; Learn</h2>
      <ul>
        <li><a href="/tools/tiny-home-cost-calculator/">Cost Calculator</a></li>
        <li><a href="/tools/which-tiny-home-is-right-for-me/">Tiny Home Quiz</a></li>
        <li><a href="/guides/tiny-house-laws-texas/">Texas Tiny House Laws</a></li>
        <li><a href="/guides/cost-to-build-a-tiny-house-in-texas/">Tiny House Costs</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/our-process/">Our Process</a></li>
        <li><a href="/faqs/">FAQs</a></li>
        <li><a href="/write-for-us/">Write for Us</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <span>© <?= date('Y') ?> <?= SITE_NAME ?>. All rights reserved.</span>
    <span><a href="/privacy-policy/">Privacy Policy</a> · <a href="/contact-us/">Contact Us</a> · <a href="/sitemap.xml">Sitemap</a></span>
  </div>
</footer>
<a class="mobile-call" href="<?= PHONE_HREF ?>">Call <?= PHONE ?></a>
<script src="/assets/js/site.js?v=<?= ASSET_VER ?>" defer></script>
<?php foreach (array_unique($GLOBALS['scripts']) as $js): ?>
<script src="/assets/js/<?= e($js) ?>?v=<?= ASSET_VER ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}

// ---------------------------------------------------------------------------
// Blog helpers

/** Posts from the route table, newest first: [path => meta]. */
function blog_posts(): array
{
    $posts = array_filter(PAGES, function ($m) { return $m['type'] === 'post'; });
    uasort($posts, function ($a, $b) { return strcmp($b['published'], $a['published']); });
    return $posts;
}

function nice_date(string $ymd): string
{
    return date('F j, Y', strtotime($ymd));
}

// Hero for a blog post: title, dek, byline + date + read time, then the featured image.
function post_hero(string $h1, string $lead): void
{
    $m = $GLOBALS['page'];
    hero([
        'eyebrow' => $m['category'],
        'h1' => $h1,
        'lead' => $lead,
        'meta' => 'By the ' . SITE_NAME . ' team · <time datetime="' . e($m['published']) . '">' . nice_date($m['published']) . '</time> · ' . (int)$m['read'] . ' min read',
        'cta' => false,
    ]);
    echo '<div class="wrap post-feature"><img src="' . e(img_url($m['image'])) . '" alt="' . e($m['crumb']) . ' — featured image" width="1200" height="675" fetchpriority="high"></div>';
}

// Sidebar for posts: CTA + recent posts.
function post_sidebar(): void
{
    $self = $GLOBALS['path'];
    echo '<aside class="sidebar"><div class="side-box side-box--cta"><h3>Planning a Tiny Home?</h3>'
       . '<p>Get a free design consultation with ' . SITE_NAME . '.</p>'
       . '<a class="btn btn--gold" href="/contact-us/">Free Consult</a><a class="btn btn--ghost" href="' . PHONE_HREF . '">' . PHONE . '</a></div>'
       . '<div class="side-box"><h3>More From the Blog</h3><ul>';
    foreach (blog_posts() as $p => $m) {
        if ($p !== $self) echo '<li><a href="' . e($p) . '">' . e($m['crumb']) . '</a></li>';
    }
    echo '</ul></div><div class="side-box"><h3>Free Tools</h3><ul>'
       . '<li><a href="/tools/tiny-home-cost-calculator/">Tiny home cost calculator</a></li>'
       . '<li><a href="/tools/which-tiny-home-is-right-for-me/">Which tiny home fits me?</a></li>'
       . '<li><a href="/tools/tiny-house-size-planner/">Tiny house size planner</a></li></ul></div></aside>';
}

// Card grid of posts (blog index, homepage).
function post_cards(int $limit = 0): void
{
    $i = 0;
    echo '<div class="grid-3 post-grid">';
    foreach (blog_posts() as $p => $m) {
        if ($limit && $i++ >= $limit) break;
        echo '<article class="card service-card post-card"><a href="' . e($p) . '" tabindex="-1" aria-hidden="true"><img src="' . e(img_url($m['image'])) . '" alt="' . e($m['crumb']) . ' — Cowboy Tiny Homes blog" width="1200" height="675" loading="lazy" style="aspect-ratio:16/9"></a>'
           . '<div class="card-body"><span class="card-kicker">' . e($m['category']) . ' · <time datetime="' . e($m['published']) . '">' . nice_date($m['published']) . '</time></span>'
           . '<h3><a href="' . e($p) . '">' . e($m['title']) . '</a></h3><p>' . e($m['desc']) . '</p>'
           . '<a class="card-more" href="' . e($p) . '">Read article →</a></div></article>';
    }
    echo '</div>';
}
