<?php
/**
 * Shared layout for every page.
 *
 *   require __DIR__ . '/../inc/layout.php';
 *   page_start([...]);  ...page HTML...  page_end();
 *
 * page_start() keys:
 *   title        <title>, 30-60 chars, unique
 *   description  meta description, 70-160 chars, unique
 *   path         canonical path, e.g. '/monetization/'
 *   type         'website' (default) or 'article'
 *   image        absolute or root-relative OG image (default: /assets/img/og-default.png)
 *   published / modified   ISO dates for articles
 *   schema       array of extra JSON-LD nodes (added to the page @graph)
 *   noindex      true to keep the page out of search
 *   body_class   extra class on <body>
 *   extra_css    array of extra stylesheet URLs (page-group CSS, e.g. /assets/css/tools.css)
 *   extra_js     array of extra script URLs, loaded deferred AFTER site.js (so window.MI exists)
 */
require_once __DIR__ . '/config.php';
require_once __DIR__ . '/icons.php';

const GA_ID = ''; // Google Analytics 4 measurement ID, e.g. 'G-XXXXXXX'. Empty = no tag.

$GLOBALS['__page'] = [];

function abs_url(string $path): string
{
    return preg_match('#^https?://#', $path) ? $path : SITE_URL . $path;
}

function org_schema(): array
{
    return [
        '@type' => 'Organization',
        '@id'   => SITE_URL . '/#org',
        'name'  => SITE_NAME,
        'url'   => SITE_URL . '/',
        'logo'  => ['@type' => 'ImageObject', 'url' => SITE_URL . '/assets/img/logo-512.png', 'width' => 512, 'height' => 512],
        'email' => SITE_EMAIL,
        'telephone' => '+1-' . SITE_PHONE,
        'slogan' => SITE_TAG,
        'address' => [
            '@type' => 'PostalAddress',
            'streetAddress' => SITE_STREET,
            'addressLocality' => SITE_CITY,
            'addressRegion' => SITE_REGION,
            'postalCode' => SITE_ZIP,
            'addressCountry' => 'US',
        ],
        'contactPoint' => [
            '@type' => 'ContactPoint',
            'contactType' => 'customer support',
            'email' => SITE_EMAIL,
            'telephone' => '+1-' . SITE_PHONE,
        ],
    ];
}

function page_start(array $p): void
{
    $p += ['type' => 'website', 'image' => '/assets/img/og-default.png', 'schema' => [], 'noindex' => false, 'body_class' => '', 'extra_css' => [], 'extra_js' => []];
    $GLOBALS['__page'] = $p;
    $canonical = abs_url($p['path']);
    $image = abs_url($p['image']);

    $graph = [
        org_schema(),
        [
            '@type' => 'WebSite',
            '@id' => SITE_URL . '/#website',
            'url' => SITE_URL . '/',
            'name' => SITE_NAME,
            'description' => 'Influencer monetization guides, free creator tools and web design for influencers.',
            'publisher' => ['@id' => SITE_URL . '/#org'],
            'inLanguage' => 'en-US',
        ],
        [
            '@type' => 'WebPage',
            '@id' => $canonical . '#webpage',
            'url' => $canonical,
            'name' => $p['title'],
            'description' => $p['description'],
            'isPartOf' => ['@id' => SITE_URL . '/#website'],
            'primaryImageOfPage' => ['@type' => 'ImageObject', 'url' => $image],
            'inLanguage' => 'en-US',
        ],
    ];
    foreach ($p['schema'] as $node) {
        $graph[] = $node;
    }
    $ld = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    ?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($p['title']) ?></title>
<meta name="description" content="<?= e($p['description']) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php if ($p['noindex']): ?><meta name="robots" content="noindex, follow">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<?php endif; ?>
<meta name="theme-color" content="#070a1c">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= $p['type'] === 'article' ? 'article' : 'website' ?>">
<meta property="og:title" content="<?= e($p['title']) ?>">
<meta property="og:description" content="<?= e($p['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<?php if ($p['type'] === 'article'): ?>
<meta property="article:published_time" content="<?= e($p['published']) ?>">
<meta property="article:modified_time" content="<?= e($p['modified'] ?? $p['published']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($p['title']) ?>">
<meta name="twitter:description" content="<?= e($p['description']) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800;900&family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_VER ?>">
<?php foreach ($p['extra_css'] as $css): ?><link rel="stylesheet" href="<?= e($css) ?>?v=<?= ASSET_VER ?>">
<?php endforeach; ?>
<link rel="alternate" type="application/rss+xml" title="<?= e(SITE_NAME) ?> Blog" href="/feed/">
<script type="application/ld+json"><?= $ld ?></script>
<?php if (GA_ID !== ''): ?>
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= e(GA_ID) ?>"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','<?= e(GA_ID) ?>');</script>
<?php endif; ?>
</head>
<body class="<?= e(trim($p['body_class'])) ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="scroll-progress" aria-hidden="true"></div>
<div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>
<div class="cursor-glow" aria-hidden="true"></div>
<header class="site-header" id="top">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <img src="/assets/img/logo-mark.webp" width="44" height="44" alt="<?= e(SITE_NAME) ?> logo">
      <span class="brand-word"><b>Monetizing</b> Influencers</span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach (site_nav() as $label => [$url, $kids]):
        $active = $url !== '/' && str_starts_with($p['path'], $url) ? ' is-active' : ''; ?>
        <li class="<?= $kids ? 'has-sub' : '' ?><?= $active ?>">
          <a href="<?= e($url) ?>"><?= e($label) ?><?php if ($kids): ?><?= icon('chevron', 'ico caret') ?><?php endif; ?></a>
<?php if ($kids): ?>
          <ul class="sub">
<?php foreach ($kids as $kl => $ku): ?>
            <li><a href="<?= e($ku) ?>"><?= e($kl) ?></a></li>
<?php endforeach; ?>
          </ul>
<?php endif; ?>
        </li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn-glow nav-cta" href="/get-started/"><?= icon('rocket') ?> Get Started</a>
    </nav>
    <button class="nav-toggle" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><?= icon('menu') ?></button>
  </div>
</header>
<main id="main">
<?php
}

/** Interior page hero with breadcrumbs (and BreadcrumbList JSON-LD). */
function page_hero(string $eyebrow, string $h1Html, string $leadHtml, array $crumbs = [], string $extraHtml = ''): void
{
    $items = [['Home', '/']];
    foreach ($crumbs as $c) {
        $items[] = $c;
    }
    $ld = ['@context' => 'https://schema.org', '@type' => 'BreadcrumbList', 'itemListElement' => []];
    foreach ($items as $i => [$name, $url]) {
        $ld['itemListElement'][] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'item' => abs_url($url)];
    }
    ?>
<section class="page-hero">
  <div class="hero-grid-bg" aria-hidden="true"></div>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><ol>
<?php foreach ($items as $i => [$name, $url]): ?>
      <li><?php if ($i < count($items) - 1): ?><a href="<?= e($url) ?>"><?= e($name) ?></a><?php else: ?><span aria-current="page"><?= e($name) ?></span><?php endif; ?></li>
<?php endforeach; ?>
    </ol></nav>
    <p class="eyebrow reveal"><?= icon('sparkles') ?> <?= e($eyebrow) ?></p>
    <h1 class="reveal"><?= $h1Html ?></h1>
    <p class="lead reveal"><?= $leadHtml ?></p>
    <?= $extraHtml ?>
  </div>
  <script type="application/ld+json"><?= json_encode($ld, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
</section>
<?php
}

/** FAQ accordion + FAQPage JSON-LD. $faqs = [[question, answerHtml], ...] */
function faq_block(array $faqs, string $heading = 'Frequently asked questions'): void
{
    $ld = ['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => []];
    foreach ($faqs as [$q, $a]) {
        $ld['mainEntity'][] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($a)]];
    }
    ?>
<section class="section faq" id="faq">
  <div class="wrap narrow">
    <h2 class="section-title reveal"><?= e($heading) ?></h2>
    <div class="accordion">
<?php foreach ($faqs as [$q, $a]): ?>
      <details class="reveal"><summary><?= e($q) ?><?= icon('chevron', 'ico caret') ?></summary><div class="answer"><?= $a ?></div></details>
<?php endforeach; ?>
    </div>
  </div>
  <script type="application/ld+json"><?= json_encode($ld, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>
</section>
<?php
}

/** Call-to-action band. */
function cta_band(string $title = 'Ready to get paid more from your audience?', string $text = 'Tell us about your channel and we will map out the income streams that fit your niche, platform and audience size.', string $btn = 'Get Started Free', string $href = '/get-started/'): void
{
    ?>
<section class="section">
  <div class="wrap">
    <div class="cta-band reveal">
      <div class="cta-orbs" aria-hidden="true"><i></i><i></i><i></i></div>
      <h2><?= e($title) ?></h2>
      <p><?= e($text) ?></p>
      <a class="btn btn-light btn-lg magnetic" href="<?= e($href) ?>"><?= e($btn) ?> <?= icon('arrow') ?></a>
    </div>
  </div>
</section>
<?php
}

/** Grid of blog post cards. */
function post_cards(int $limit = 3, string $exclude = ''): void
{
    $n = 0;
    echo '<div class="card-grid cols-3">';
    foreach (site_posts() as [$url, $title, $cat, $date, $excerpt]) {
        if ($url === $exclude) {
            continue;
        }
        if (++$n > $limit) {
            break;
        }
        echo '<article class="card post-card tilt reveal"><a href="' . e($url) . '">'
            . '<span class="chip">' . e($cat) . '</span>'
            . '<h3>' . e($title) . '</h3><p>' . e($excerpt) . '</p>'
            . '<span class="more">Read the guide ' . icon('arrow') . '</span></a></article>';
    }
    echo '</div>';
}

/** Flash message after a form round-trip (?sent=ok|err). */
function form_flash(string $form): string
{
    $sent = $_GET['sent'] ?? '';
    $which = $_GET['form'] ?? '';
    if ($which !== $form || $sent === '') {
        return '';
    }
    return $sent === 'ok'
        ? '<p class="flash ok" role="status">' . icon('check') . ' Thanks! Your message is in. We reply within 1-2 business days.</p>'
        : '<p class="flash err" role="alert">Something went wrong sending that. Please check the required fields, or email ' . e(SITE_EMAIL) . '.</p>';
}

/** Hidden anti-spam fields shared by every form. */
function form_guard(string $form, string $return): string
{
    return '<input type="hidden" name="form" value="' . e($form) . '">'
        . '<input type="hidden" name="return" value="' . e($return) . '">'
        . '<input type="hidden" name="ts" value="' . time() . '">'
        . '<div class="hp" aria-hidden="true"><label>Leave this empty<input type="text" name="website_url" tabindex="-1" autocomplete="off"></label></div>';
}

function page_end(): void
{
    ?>
</main>
<footer class="site-footer">
  <div class="footer-marquee" aria-hidden="true"><div class="marquee-track">
    <?php for ($i = 0; $i < 2; $i++): ?><span>Brand Deals</span><span>Affiliate Income</span><span>Sponsored Posts</span><span>UGC</span><span>Merch Drops</span><span>Ad Revenue</span><span>Memberships</span><span>Digital Products</span><span>White Label</span><?php endfor; ?>
  </div></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="brand" href="/"><img src="/assets/img/logo-mark.webp" width="44" height="44" alt="" loading="lazy"><span class="brand-word"><b>Monetizing</b> Influencers</span></a>
      <p><?= e(SITE_NAME) ?> helps creators turn followers into income with brand deals, smarter pricing, free tools and websites built to earn.</p>
      <ul class="contact-list">
        <li><?= icon('mail') ?> <a href="mailto:<?= e(SITE_EMAIL) ?>"><?= e(SITE_EMAIL) ?></a></li>
        <li><?= icon('phone') ?> <a href="tel:<?= e(SITE_PHONE_HREF) ?>"><?= e(SITE_PHONE) ?></a></li>
        <li><?= icon('pin') ?> <?= e(SITE_STREET . ', ' . SITE_CITY . ', ' . SITE_REGION . ' ' . SITE_ZIP) ?>, USA</li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Platforms</h2>
      <ul>
        <li><a href="/social-platforms/youtube/">YouTube</a></li>
        <li><a href="/social-platforms/tiktok/">TikTok</a></li>
        <li><a href="/social-platforms/instagram/">Instagram</a></li>
        <li><a href="/social-platforms/facebook/">Facebook</a></li>
        <li><a href="/social-platforms/pinterest/">Pinterest</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Monetization</h2>
      <ul>
        <li><a href="/monetization/#brand-outreach">Brand Outreach</a></li>
        <li><a href="/monetization/#partnership-deals">Partnership Deals</a></li>
        <li><a href="/monetization/#ad-placements">Ad Placements</a></li>
        <li><a href="/monetization/#white-labeling">White Labeling</a></li>
        <li><a href="/monetization/#short-content">Short Content</a></li>
        <li><a href="/website-design/">Web Design for Influencers</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Free Tools</h2>
      <ul>
        <li><a href="/tools/influencer-earnings-calculator/">Earnings Calculator</a></li>
        <li><a href="/tools/engagement-rate-calculator/">Engagement Rate</a></li>
        <li><a href="/tools/influencer-email-generator/">Email Generator</a></li>
        <li><a href="/tools/media-kit-builder/">Media Kit Builder</a></li>
        <li><a href="/tools/income-stream-simulator/">Income Simulator</a></li>
        <li><a href="/tools/monetization-readiness-quiz/">Readiness Quiz</a></li>
      </ul>
    </div>
    <div>
      <h2 class="footer-h">Get the creator money memo</h2>
      <p class="small">One email a month: new rate data, pitch templates and tools. No spam.</p>
      <?= form_flash('newsletter') ?>
      <form class="newsletter js-form" action="/api/form.php" method="post">
        <?= form_guard('newsletter', $GLOBALS['__page']['path'] ?? '/') ?>
        <label class="sr-only" for="nl-email">Email</label>
        <input id="nl-email" type="email" name="email" placeholder="you@email.com" required>
        <button class="btn btn-glow" type="submit">Subscribe</button>
      </form>
      <ul class="legal-links">
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/write-for-us/">Write For Us</a></li>
        <li><a href="/privacy-policy/">Privacy</a></li>
        <li><a href="/terms/">Terms</a></li>
        <li><a href="/sitemap/">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; <?= date('Y') ?> <?= e(SITE_NAME) ?>. All rights reserved.</p>
    <p>Designed &amp; developed by JWeb.</p>
  </div>
</footer>
<button class="to-top" aria-label="Back to top"><?= icon('arrow') ?></button>
<script src="/assets/js/site.js?v=<?= ASSET_VER ?>" defer></script>
<?php foreach ($GLOBALS['__page']['extra_js'] ?? [] as $js): ?><script src="<?= e($js) ?>?v=<?= ASSET_VER ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}
