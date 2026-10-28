<?php
/**
 * Shared layout and components. Every page does:
 *
 *   require $_SERVER['DOCUMENT_ROOT'] . '/includes/layout.php';
 *   page_start([...meta...]);
 *   ...page HTML...
 *   page_end();
 */

require_once __DIR__ . '/config.php';
require_once __DIR__ . '/icons.php';

/** HTML-escape. */
function e($s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES | ENT_HTML5, 'UTF-8');
}

/** Absolute URL for a site path. */
function abs_url(string $path): string
{
    return BIZ['origin'] . $path;
}

/** Version string for cache-busting local assets. */
function asset(string $path): string
{
    $file = AR_ROOT . $path;
    $v = is_file($file) ? substr(md5((string) filemtime($file)), 0, 8) : '1';
    return $path . '?v=' . $v;
}

/** Phone link. */
function phone_link(string $class = '', string $label = ''): string
{
    $label = $label ?: BIZ['phone_display'];
    return '<a class="' . e($class) . '" href="tel:' . BIZ['phone_href'] . '">' . e($label) . '</a>';
}

/** Current request path, normalised. */
function current_path(): string
{
    $p = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
    return $p === false ? '/' : $p;
}

$GLOBALS['AR_SCHEMA'] = [];

/** Queue a JSON-LD node to be printed in the page <head>/footer graph. */
function add_schema(array $node): void
{
    $GLOBALS['AR_SCHEMA'][] = $node;
}

/** The sitewide business node. */
function business_schema(): array
{
    $areas = [['@type' => 'City', 'name' => 'Austin', 'containedInPlace' => ['@type' => 'State', 'name' => 'Texas']]];
    foreach (AREAS as $a) {
        if (($a['kind'] ?? '') === 'neighborhood') {
            continue;
        }
        $areas[] = ['@type' => 'City', 'name' => $a['name'] . ', TX'];
    }
    $offers = [];
    foreach (SERVICES as $slug => $s) {
        $offers[] = [
            '@type' => 'Offer',
            'itemOffered' => ['@type' => 'Service', 'name' => $s['h1'], 'url' => abs_url('/services/' . $slug . '/')],
        ];
    }
    return [
        '@type' => ['RoofingContractor', 'LocalBusiness'],
        '@id' => abs_url('/#business'),
        'name' => BIZ['name'],
        'url' => abs_url('/'),
        'logo' => abs_url(BIZ['logo']),
        'image' => abs_url(BIZ['og_image']),
        'telephone' => BIZ['phone_href'],
        'email' => BIZ['email'],
        'priceRange' => '$$',
        'description' => 'Austin Roofing is an Austin, TX roofing company providing roof repair, roof replacement, storm and hail damage restoration, commercial and multi-family roofing across Central Texas, with free inspections and free quotes.',
        'address' => [
            '@type' => 'PostalAddress',
            'addressLocality' => 'Austin',
            'addressRegion' => 'TX',
            'addressCountry' => 'US',
        ],
        'geo' => ['@type' => 'GeoCoordinates', 'latitude' => BIZ['latitude'], 'longitude' => BIZ['longitude']],
        'openingHoursSpecification' => [[
            '@type' => 'OpeningHoursSpecification',
            'dayOfWeek' => ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'opens' => '00:00', 'closes' => '23:59',
        ]],
        'areaServed' => $areas,
        'hasOfferCatalog' => ['@type' => 'OfferCatalog', 'name' => 'Austin Roofing Services', 'itemListElement' => $offers],
    ];
}

/**
 * Open the document.
 *
 * Keys: title, description, path (canonical), image, crumbs ([[name, path], ...]),
 * noindex, body_class, type ('website'|'article'), article (BlogPosting extras),
 * service (Service name), hero (bool, transparent header over hero)
 */
function page_start(array $p): void
{
    $path = $p['path'] ?? current_path();
    $canonical = abs_url($path);
    $title = $p['title'];
    $desc = $p['description'];
    $image = abs_url($p['image'] ?? BIZ['og_image']);
    $type = $p['type'] ?? 'website';
    $GLOBALS['AR_PAGE'] = $p + ['path' => $path];

    // Structured data -------------------------------------------------------
    add_schema(business_schema());
    add_schema([
        '@type' => 'WebSite', '@id' => abs_url('/#website'), 'url' => abs_url('/'),
        'name' => BIZ['name'], 'publisher' => ['@id' => abs_url('/#business')], 'inLanguage' => 'en-US',
    ]);
    $webpage = [
        '@type' => 'WebPage', '@id' => $canonical . '#webpage', 'url' => $canonical, 'name' => $title,
        'description' => $desc, 'isPartOf' => ['@id' => abs_url('/#website')],
        'about' => ['@id' => abs_url('/#business')], 'inLanguage' => 'en-US',
        'primaryImageOfPage' => ['@type' => 'ImageObject', 'url' => $image],
    ];
    if (!empty($p['crumbs'])) {
        $items = [['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => abs_url('/')]];
        $i = 2;
        foreach ($p['crumbs'] as $c) {
            $items[] = ['@type' => 'ListItem', 'position' => $i++, 'name' => $c[0], 'item' => abs_url($c[1])];
        }
        add_schema(['@type' => 'BreadcrumbList', '@id' => $canonical . '#breadcrumb', 'itemListElement' => $items]);
        $webpage['breadcrumb'] = ['@id' => $canonical . '#breadcrumb'];
    }
    add_schema($webpage);
    if (!empty($p['service'])) {
        add_schema([
            '@type' => 'Service', '@id' => $canonical . '#service', 'name' => $p['service'],
            'serviceType' => $p['service_type'] ?? $p['service'], 'url' => $canonical, 'description' => $desc,
            'provider' => ['@id' => abs_url('/#business')],
            'areaServed' => ['@type' => 'City', 'name' => $p['area'] ?? 'Austin, TX'],
        ]);
    }
    if (!empty($p['article'])) {
        $a = $p['article'];
        add_schema([
            '@type' => 'BlogPosting', '@id' => $canonical . '#article', 'headline' => $a['headline'],
            'description' => $desc, 'image' => $image, 'datePublished' => $a['published'],
            'dateModified' => $a['modified'], 'mainEntityOfPage' => ['@id' => $canonical . '#webpage'],
            'author' => ['@type' => 'Organization', 'name' => BIZ['name'], 'url' => abs_url('/about-us/')],
            'publisher' => ['@id' => abs_url('/#business')], 'inLanguage' => 'en-US',
        ]);
    }

    $robots = !empty($p['noindex']) ? 'noindex, follow' : 'index, follow, max-image-preview:large, max-snippet:-1';
    $bodyClass = trim(($p['body_class'] ?? '') . (!empty($p['hero_home']) ? ' has-home-hero' : ''));
    ?>
<!doctype html>
<html lang="en-US">
<head>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-G6C3B8SGY7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-G6C3B8SGY7');
</script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<meta name="robots" content="<?= $robots ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= $type === 'article' ? 'article' : 'website' ?>">
<meta property="og:site_name" content="<?= e(BIZ['name']) ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<?php if (!empty($p['article'])): ?>
<meta property="article:published_time" content="<?= e($p['article']['published']) ?>">
<meta property="article:modified_time" content="<?= e($p['article']['modified']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<meta name="theme-color" content="#E62727">
<link rel="icon" href="/wp-content/uploads/2025/11/cropped-Austin-Roofing-Icon-32x32.webp" sizes="32x32">
<link rel="icon" href="/wp-content/uploads/2025/11/cropped-Austin-Roofing-Icon-192x192.webp" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/site.css') ?>">
<?php if (!empty($p['preload'])): ?>
<link rel="preload" as="image" href="<?= e($p['preload']) ?>">
<?php endif; ?>
</head>
<body class="<?= e($bodyClass) ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="scroll-roof" aria-hidden="true"><span></span></div>
<div class="topbar">
  <div class="container topbar__inner">
    <span class="topbar__note"><?= icon('alert') ?> 24/7 emergency roof service · Free inspections &amp; quotes</span>
    <a class="topbar__phone" href="tel:<?= BIZ['phone_href'] ?>"><?= icon('phone') ?> <?= e(BIZ['phone_display']) ?></a>
  </div>
</div>
<header class="site-header" id="top">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Austin Roofing home">
      <img src="<?= BIZ['logo_small'] ?>" srcset="<?= BIZ['logo_small'] ?> 300w, /wp-content/uploads/2025/11/Austin-Roofing-Logo-768x375.webp 768w" sizes="140px" width="140" height="68" alt="Austin Roofing logo">
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span><span class="sr-only">Menu</span></button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <ul>
      <?php foreach (NAV as $item):
          $active = ($item[1] === '/' ? $path === '/' : str_starts_with($path, $item[1])) ? ' aria-current="page"' : '';
          $mega = $item[2] ?? null; ?>
        <li class="<?= $mega ? 'has-mega' : '' ?>">
          <a href="<?= $item[1] ?>"<?= $active ?>><?= e($item[0]) ?></a>
          <?php if ($mega === 'services'): ?>
          <div class="mega">
            <?php foreach (SERVICE_GROUPS as $g => $gname): ?>
            <div class="mega__col"><p class="mega__title"><?= e($gname) ?></p><ul>
              <?php foreach (SERVICES as $slug => $s): if ($s['group'] !== $g) continue; ?>
              <li><a href="/services/<?= $slug ?>/"><?= icon($s['icon']) ?><?= e($s['name']) ?></a></li>
              <?php endforeach; ?>
            </ul></div>
            <?php endforeach; ?>
          </div>
          <?php elseif ($mega === 'areas'): ?>
          <div class="mega mega--narrow"><div class="mega__col"><ul class="mega__grid">
            <?php foreach (AREAS as $slug => $a): ?>
            <li><a href="/service-areas/<?= $slug ?>/"><?= icon('pin') ?><?= e($a['name']) ?></a></li>
            <?php endforeach; ?>
          </ul></div></div>
          <?php elseif ($mega === 'tools'): ?>
          <div class="mega mega--narrow"><div class="mega__col"><ul>
            <?php foreach (TOOLS as $slug => $t): ?>
            <li><a href="/roofing-tools/<?= $slug ?>/"><?= icon($t['icon']) ?><?= e($t['name']) ?></a></li>
            <?php endforeach; ?>
          </ul></div></div>
          <?php endif; ?>
        </li>
      <?php endforeach; ?>
      </ul>
      <a class="btn btn--red site-nav__cta" href="/contact-us/">Get a FREE Quote</a>
    </nav>
  </div>
</header>
<main id="main">
<?php
}

/** Close the document. */
function page_end(): void
{
    ?>
</main>
<footer class="site-footer">
  <div class="footer-roofline" aria-hidden="true"></div>
  <div class="container site-footer__grid">
    <div class="site-footer__brand">
      <a href="/" class="footer-logo"><img src="<?= BIZ['logo_small'] ?>" width="170" height="83" alt="Austin Roofing logo" loading="lazy"></a>
      <p>Austin Roofing is a Central Texas roofing company for homes, commercial buildings and multi-family properties — repairs, replacements, storm damage and free inspections.</p>
      <p class="site-footer__phone"><?= icon('phone') ?> <?= phone_link() ?></p>
      <p><?= icon('mail') ?> <a href="mailto:<?= BIZ['email'] ?>"><?= BIZ['email'] ?></a></p>
      <p class="badge-247"><?= icon('clock') ?> 24/7 Emergency Services</p>
    </div>
    <div>
      <p class="site-footer__title">Company</p>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="/services/">Services</a></li>
        <li><a href="/service-areas/">Service Areas</a></li>
        <li><a href="/roofing-tools/">Roofing Tools</a></li>
        <li><a href="/faqs/">FAQs</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/contact-us/">Contact Us</a></li>
      </ul>
    </div>
    <div>
      <p class="site-footer__title">Services Offered</p>
      <ul>
        <?php foreach (SERVICES as $slug => $s): ?>
        <li><a href="/services/<?= $slug ?>/"><?= e($s['name']) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <div>
      <p class="site-footer__title">Service Areas</p>
      <ul>
        <li><a href="/">Austin, TX</a></li>
        <?php foreach (AREAS as $slug => $a): ?>
        <li><a href="/service-areas/<?= $slug ?>/"><?= e($a['name']) ?><?= ($a['kind'] ?? '') === 'neighborhood' ? '' : ', TX' ?></a></li>
        <?php endforeach; ?>
        <li class="muted">And other surrounding areas of Austin, TX</li>
      </ul>
    </div>
  </div>
  <div class="site-footer__bottom">
    <div class="container site-footer__bottom-inner">
      <p>© Copyright <?= date('Y') ?> Austin Roofing. All Rights Reserved.</p>
      <p><a href="/sitemap/">Sitemap</a> · <a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-of-service/">Terms of Service</a></p>
    </div>
  </div>
</footer>
<div class="mobile-cta">
  <a href="tel:<?= BIZ['phone_href'] ?>" class="mobile-cta__call"><?= icon('phone') ?> Call Now</a>
  <a href="/contact-us/" class="mobile-cta__quote"><?= icon('clipboard') ?> Free Quote</a>
</div>
<script type="application/ld+json"><?= json_encode(['@context' => 'https://schema.org', '@graph' => $GLOBALS['AR_SCHEMA']], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
<script src="<?= asset('/assets/js/site.js') ?>" defer></script>
<script src="<?= asset('/assets/js/tools.js') ?>" defer></script>
</body>
</html>
<?php
}

/** Breadcrumb trail (visible). */
function breadcrumbs(array $crumbs): string
{
    $h = '<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => $c) {
        $h .= $i === $last
            ? '<li aria-current="page">' . e($c[0]) . '</li>'
            : '<li><a href="' . e($c[1]) . '">' . e($c[0]) . '</a></li>';
    }
    return $h . '</ol></nav>';
}

/**
 * Interior page hero with rain canvas over the roof photo.
 * $opts: crumbs, eyebrow, lead, image, cta (bool), meta (html below lead)
 */
function page_hero(string $h1, array $opts = []): void
{
    $img = $opts['image'] ?? '/wp-content/uploads/2025/12/Austin-Roofing-BG-1.webp';
    ?>
<section class="page-hero" style="--hero-img:url('<?= e($img) ?>')">
  <canvas class="weather" data-weather="<?= e($opts['weather'] ?? 'rain') ?>" aria-hidden="true"></canvas>
  <div class="container page-hero__inner">
    <?php if (!empty($opts['crumbs'])) echo breadcrumbs($opts['crumbs']); ?>
    <?php if (!empty($opts['eyebrow'])): ?><p class="eyebrow"><?= e($opts['eyebrow']) ?></p><?php endif; ?>
    <h1><?= e($h1) ?></h1>
    <?php if (!empty($opts['lead'])): ?><p class="page-hero__lead"><?= $opts['lead'] ?></p><?php endif; ?>
    <?php if (!empty($opts['meta'])): ?><div class="page-hero__meta"><?= $opts['meta'] ?></div><?php endif; ?>
    <?php if ($opts['cta'] ?? true): ?>
    <div class="btn-row">
      <a class="btn btn--red" href="/contact-us/"><?= icon('clipboard') ?> Get a FREE Quote</a>
      <a class="btn btn--ghost" href="tel:<?= BIZ['phone_href'] ?>"><?= icon('phone') ?> <?= e(BIZ['phone_short']) ?></a>
    </div>
    <?php endif; ?>
  </div>
  <div class="roof-divider" aria-hidden="true"></div>
</section>
<?php
}

/** Big call-to-action band. */
function cta_band(string $heading = 'Get Your Free Austin Roof Inspection Today', string $text = ''): void
{
    $text = $text ?: 'Storm damage, a stubborn leak or a roof that is simply getting old — Austin Roofing will inspect it, photograph what we find and give you a free, no-pressure quote.';
    ?>
<section class="cta-band">
  <canvas class="weather" data-weather="rain" aria-hidden="true"></canvas>
  <div class="container cta-band__inner">
    <div>
      <h2><?= e($heading) ?></h2>
      <p><?= e($text) ?></p>
    </div>
    <div class="cta-band__actions">
      <a class="btn btn--green btn--lg" href="/contact-us/"><?= icon('clipboard') ?> Schedule a Free Quote</a>
      <a class="btn btn--ghost btn--lg" href="tel:<?= BIZ['phone_href'] ?>"><?= icon('phone') ?> <?= e(BIZ['phone_display']) ?></a>
    </div>
  </div>
</section>
<?php
}

/**
 * FAQ accordion + FAQPage schema.
 * $faqs: [[question, answer_html], ...]
 */
function faq_block(array $faqs, string $heading = 'Frequently Asked Questions', string $id = 'faq'): void
{
    $entities = [];
    echo '<section class="faq" id="' . e($id) . '"><h2>' . e($heading) . '</h2><div class="faq__list">';
    foreach ($faqs as $i => [$q, $a]) {
        echo '<details class="faq__item"' . ($i === 0 ? ' open' : '') . '><summary>' . e($q) . '</summary><div class="faq__a">' . $a . '</div></details>';
        $entities[] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => trim(strip_tags($a))]];
    }
    echo '</div></section>';
    add_schema(['@type' => 'FAQPage', '@id' => abs_url($GLOBALS['AR_PAGE']['path']) . '#faq', 'mainEntity' => $entities]);
}

/** Mount point for an interactive tool (see assets/js/tools.js). */
function tool(string $key, string $heading = ''): void
{
    echo '<div class="tool" data-tool="' . e($key) . '"' . ($heading ? ' data-heading="' . e($heading) . '"' : '') . '><noscript><p>This calculator needs JavaScript. Call ' . e(BIZ['phone_display']) . ' and we will run the numbers with you.</p></noscript></div>';
}

/** A boxed tool embed linking to the full tool page. */
function tool_embed(string $slug): void
{
    $t = TOOLS[$slug];
    echo '<aside class="tool-embed"><p class="eyebrow">' . icon($t['icon']) . ' Free interactive tool</p>';
    tool($t['tool'], $t['name']);
    echo '<p class="tool-embed__more"><a href="/roofing-tools/' . $slug . '/">Open the full ' . e($t['name']) . ' →</a></p></aside>';
}

/** Grid of service cards. $slugs = null for all. */
function service_cards(?array $slugs = null, string $class = ''): void
{
    $slugs = $slugs ?? array_keys(SERVICES);
    echo '<div class="cards cards--services ' . e($class) . '">';
    foreach ($slugs as $slug) {
        $s = SERVICES[$slug];
        echo '<a class="card card--service reveal" href="/services/' . $slug . '/"><span class="card__icon">' . icon($s['icon']) . '</span><h3>' . e($s['h1']) . '</h3><p>' . e($s['blurb']) . '</p><span class="card__more">Learn more →</span></a>';
    }
    echo '</div>';
}

/** Grid of area links. */
function area_cards(?array $slugs = null): void
{
    $slugs = $slugs ?? array_keys(AREAS);
    echo '<div class="area-grid">';
    foreach ($slugs as $slug) {
        $a = AREAS[$slug];
        echo '<a class="area-chip reveal" href="/service-areas/' . $slug . '/">' . icon('pin') . '<span><strong>' . e($a['name']) . '</strong><small>' . e($a['county']) . '</small></span></a>';
    }
    echo '</div>';
}

/** Grid of tool cards. */
function tool_cards(?array $slugs = null): void
{
    $slugs = $slugs ?? array_keys(TOOLS);
    echo '<div class="cards cards--tools">';
    foreach ($slugs as $slug) {
        $t = TOOLS[$slug];
        echo '<a class="card card--tool reveal" href="/roofing-tools/' . $slug . '/"><span class="card__icon">' . icon($t['icon']) . '</span><h3>' . e($t['name']) . '</h3><p>' . e($t['blurb']) . '</p><span class="card__more">Try it free →</span></a>';
    }
    echo '</div>';
}

/** Blog post cards, newest first. */
function post_cards(int $limit = 3, array $exclude = []): void
{
    $posts = POSTS;
    uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
    echo '<div class="cards cards--posts">';
    $n = 0;
    foreach ($posts as $slug => $p) {
        if (in_array($slug, $exclude, true)) {
            continue;
        }
        if ($n++ >= $limit) {
            break;
        }
        echo '<article class="card card--post reveal"><a href="/blog/' . $slug . '/" class="card--post__img"><img src="' . e($p['thumb']) . '" alt="' . e($p['h1']) . '" width="768" height="511" loading="lazy"></a><div class="card--post__body"><p class="card__date">' . date('F j, Y', strtotime($p['date'])) . '</p><h3><a href="/blog/' . $slug . '/">' . e($p['h1']) . '</a></h3><p>' . e($p['excerpt']) . '</p><a class="card__more" href="/blog/' . $slug . '/">Read article →</a></div></article>';
    }
    echo '</div>';
}

/** Estimate form. $compact = sidebar version. */
function quote_form(bool $compact = false, string $source = ''): void
{
    $source = $source ?: current_path();
    $t = time();
    $sig = hash_hmac('sha256', (string) $t, form_secret());
    ?>
<form class="quote-form<?= $compact ? ' quote-form--compact' : '' ?>" method="post" action="/submit.php">
  <input type="hidden" name="source" value="<?= e($source) ?>">
  <input type="hidden" name="ts" value="<?= $t ?>">
  <input type="hidden" name="sig" value="<?= $sig ?>">
  <div class="hp" aria-hidden="true"><label>Leave blank <input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
  <div class="quote-form__grid">
    <label>Name<input type="text" name="name" required autocomplete="name"></label>
    <label>Phone<input type="tel" name="phone" required autocomplete="tel"></label>
    <label>Email<input type="email" name="email" autocomplete="email"></label>
    <?php if (!$compact): ?>
    <label>Property address or ZIP<input type="text" name="address" autocomplete="street-address"></label>
    <?php endif; ?>
    <label class="span-2">What do you need?
      <select name="service">
        <option value="">Choose a service…</option>
        <?php foreach (SERVICES as $s): ?><option><?= e($s['name']) ?></option><?php endforeach; ?>
        <option>Something else</option>
      </select>
    </label>
    <label class="span-2">Message<textarea name="message" rows="<?= $compact ? 3 : 5 ?>" placeholder="Tell us about the roof — leaks, storm date, roof age…"></textarea></label>
  </div>
  <button class="btn btn--red btn--block" type="submit"><?= icon('clipboard') ?> Request My Free Quote</button>
  <p class="quote-form__note">Free inspection · No obligation · We reply fast, 24/7 for emergencies</p>
</form>
<?php
}

/** Secret used to sign form timestamps (per-install; falls back to a file hash). */
function form_secret(): string
{
    $f = AR_ROOT . '/includes/.form-secret';
    if (is_readable($f)) {
        return trim((string) file_get_contents($f));
    }
    return hash('sha256', __FILE__ . BIZ['email']);
}

/** Sidebar used on service, area and blog pages. */
function sidebar(array $opts = []): void
{
    ?>
<aside class="sidebar">
  <div class="sidebar__box sidebar__box--quote">
    <p class="sidebar__title">Free Roofing Estimate</p>
    <p class="sidebar__phone"><?= icon('phone') ?> <?= phone_link() ?></p>
    <?php quote_form(true); ?>
  </div>
  <?php if (!empty($opts['links'])): ?>
  <div class="sidebar__box">
    <p class="sidebar__title"><?= e($opts['links_title'] ?? 'Related Services') ?></p>
    <ul class="sidebar__links">
      <?php foreach ($opts['links'] as [$label, $href]): ?>
      <li><a href="<?= e($href) ?>"><?= e($label) ?></a></li>
      <?php endforeach; ?>
    </ul>
  </div>
  <?php endif; ?>
  <div class="sidebar__box sidebar__box--tools">
    <p class="sidebar__title">Roofing Calculators</p>
    <ul class="sidebar__links">
      <?php foreach (TOOLS as $slug => $t): ?>
      <li><a href="/roofing-tools/<?= $slug ?>/"><?= icon($t['icon']) ?> <?= e($t['name']) ?></a></li>
      <?php endforeach; ?>
    </ul>
  </div>
</aside>
<?php
}

/** Links to related service pages as [label, href] pairs for the sidebar. */
function service_links(array $slugs): array
{
    return array_map(fn($s) => [SERVICES[$s]['h1'], '/services/' . $s . '/'], $slugs);
}

/**
 * Standard service page. Content file supplies $content (HTML string) etc.
 * Keys: slug, title, description, lead, body (html), faqs, related (slugs), tool (slug)
 */
function render_service(array $c): void
{
    $slug = $c['slug'];
    $s = SERVICES[$slug];
    $path = '/services/' . $slug . '/';
    $crumbs = [['Services', '/services/'], [$s['name'], $path]];
    page_start([
        'title' => $c['title'], 'description' => $c['description'], 'path' => $path,
        'crumbs' => $crumbs, 'service' => $s['h1'], 'service_type' => $s['name'],
        'image' => $c['image'] ?? null, 'body_class' => 'page-service',
    ]);
    page_hero($s['h1'], ['crumbs' => $crumbs, 'eyebrow' => $c['eyebrow'] ?? 'Austin Roofing Services', 'lead' => $c['lead'], 'weather' => $c['weather'] ?? 'rain']);
    ?>
<div class="container layout-sidebar">
  <article class="prose">
    <?= $c['body'] ?>
    <?php if (!empty($c['tool'])) tool_embed($c['tool']); ?>
    <?php if (!empty($c['faqs'])) faq_block($c['faqs'], $c['faq_heading'] ?? $s['name'] . ' FAQs'); ?>
  </article>
  <?php sidebar(['links' => service_links($c['related'] ?? []), 'links_title' => 'Related Services']); ?>
</div>
<section class="section section--cream">
  <div class="container">
    <h2 class="section-title">More Austin Roofing Services</h2>
    <?php service_cards(array_slice(array_values(array_diff(array_keys(SERVICES), [$slug])), 0, 6)); ?>
  </div>
</section>
<?php
    cta_band();
    page_end();
}

/**
 * Standard area page.
 * Keys: slug, title, description, lead, body, faqs, services (slugs)
 */
function render_area(array $c): void
{
    $slug = $c['slug'];
    $a = AREAS[$slug];
    $path = '/service-areas/' . $slug . '/';
    $crumbs = [['Service Areas', '/service-areas/'], [$a['name'], $path]];
    $place = $a['name'] . (($a['kind'] ?? '') === 'neighborhood' ? ', Austin, TX' : ', TX');
    page_start([
        'title' => $c['title'], 'description' => $c['description'], 'path' => $path,
        'crumbs' => $crumbs, 'service' => $a['h1'], 'service_type' => 'Roofing contractor', 'area' => $place,
        'body_class' => 'page-area',
    ]);
    page_hero($a['h1'], ['crumbs' => $crumbs, 'eyebrow' => 'Serving ' . $place, 'lead' => $c['lead']]);
    ?>
<div class="container layout-sidebar">
  <article class="prose">
    <?= $c['body'] ?>
    <h2>Roofing Services in <?= e($a['name']) ?></h2>
    <?php service_cards($c['services'] ?? ['roof-repair', 'roof-replacement', 'hail-damage-repair', 'roof-inspection'], 'cards--compact'); ?>
    <?php if (!empty($c['faqs'])) faq_block($c['faqs'], $a['name'] . ' Roofing FAQs'); ?>
  </article>
  <?php sidebar(['links' => array_map(fn($s, $x) => [$x['name'], '/service-areas/' . $s . '/'], array_keys(AREAS), AREAS), 'links_title' => 'Other Areas We Serve']); ?>
</div>
<?php
    cta_band('Need a Roofer in ' . $a['name'] . '?');
    page_end();
}

/**
 * Standard blog post.
 * Keys: slug, body (html), faqs, toc (bool, default true)
 */
function render_post(array $c): void
{
    $slug = $c['slug'];
    $p = POSTS[$slug];
    $path = '/blog/' . $slug . '/';
    $crumbs = [['Blog', '/blog/'], [$p['h1'], $path]];
    page_start([
        'title' => mb_strlen($p['title']) <= 48 ? $p['title'] . ' | Austin Roofing' : $p['title'], 'description' => $p['desc'], 'path' => $path,
        'crumbs' => $crumbs, 'type' => 'article', 'image' => $p['img'], 'body_class' => 'page-post',
        'article' => ['headline' => $p['h1'], 'published' => $p['date'] . 'T08:00:00-06:00', 'modified' => $p['modified'] . 'T08:00:00-05:00'],
    ]);
    $meta = '<span>' . icon('calendar') . ' Updated ' . date('F j, Y', strtotime($p['modified'])) . '</span><span>' . icon('user') . ' Austin Roofing Team</span>';
    page_hero($p['h1'], ['crumbs' => $crumbs, 'eyebrow' => 'Austin Roofing Blog', 'lead' => e($p['excerpt']), 'meta' => $meta, 'cta' => false, 'weather' => 'rain']);
    ?>
<div class="container layout-sidebar">
  <article class="prose prose--post">
    <figure class="post-figure"><img src="<?= e($p['img']) ?>" alt="<?= e($p['h1']) ?>" width="1200" height="800" fetchpriority="high"></figure>
    <?php if ($c['toc'] ?? true): ?><nav class="toc" aria-label="In this article"><p class="toc__title">In this article</p><ol data-toc></ol></nav><?php endif; ?>
    <?= $c['body'] ?>
    <?php if (!empty($p['tool'])) tool_embed($p['tool']); ?>
    <?php if (!empty($c['faqs'])) faq_block($c['faqs'], 'FAQs', 'h-faqs'); ?>
    <div class="author-box">
      <img src="<?= BIZ['icon'] ?>" width="64" height="64" alt="Austin Roofing icon" loading="lazy">
      <div><p><strong>Written by the Austin Roofing team.</strong> We inspect, repair and replace roofs across Austin and Central Texas every week, and we write these guides to answer the questions homeowners ask us on the roof. Questions about your own roof? Call <?= phone_link() ?> for a free inspection.</p></div>
    </div>
  </article>
  <?php sidebar(['links' => $c['related'] ?? service_links(['roof-replacement', 'roof-repair', 'hail-damage-repair', 'roof-inspection']), 'links_title' => 'Austin Roofing Services']); ?>
</div>
<section class="section section--cream">
  <div class="container">
    <h2 class="section-title">More Roofing Guides</h2>
    <?php post_cards(3, [$slug]); ?>
  </div>
</section>
<?php
    cta_band();
    page_end();
}

/**
 * Standard tool page.
 * Keys: slug, title, description, lead, intro (html), body (html), faqs
 */
function render_tool(array $c): void
{
    $slug = $c['slug'];
    $t = TOOLS[$slug];
    $path = '/roofing-tools/' . $slug . '/';
    $crumbs = [['Roofing Tools', '/roofing-tools/'], [$t['name'], $path]];
    add_schema([
        '@type' => 'WebApplication', 'name' => $t['name'], 'url' => abs_url($path),
        'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any',
        'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
        'provider' => ['@id' => abs_url('/#business')],
    ]);
    page_start(['title' => $c['title'], 'description' => $c['description'], 'path' => $path, 'crumbs' => $crumbs, 'body_class' => 'page-tool']);
    page_hero($t['name'], ['crumbs' => $crumbs, 'eyebrow' => 'Free Austin Roofing Tool', 'lead' => $c['lead'], 'cta' => false, 'weather' => $c['weather'] ?? 'rain']);
    ?>
<div class="container">
  <div class="tool-stage">
    <?php if (!empty($c['intro'])): ?><div class="tool-stage__intro"><?= $c['intro'] ?></div><?php endif; ?>
    <?php tool($t['tool']); ?>
  </div>
</div>
<div class="container layout-sidebar">
  <article class="prose">
    <?= $c['body'] ?>
    <?php if (!empty($c['faqs'])) faq_block($c['faqs']); ?>
  </article>
  <?php sidebar(['links' => service_links($c['related'] ?? ['roof-replacement', 'roof-repair', 'roof-inspection']), 'links_title' => 'Related Services']); ?>
</div>
<section class="section section--cream">
  <div class="container">
    <h2 class="section-title">More Free Roofing Tools</h2>
    <?php tool_cards(array_values(array_diff(array_keys(TOOLS), [$slug]))); ?>
  </div>
</section>
<?php
    cta_band();
    page_end();
}
