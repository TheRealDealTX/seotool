<?php
// Page shell: <head>, header, footer. Every page goes through render_page().
defined('PGF') || exit;

function breadcrumbs_html(array $crumbs): string
{
    $out = '<nav class="crumbs" aria-label="Breadcrumb"><ol>';
    $last = count($crumbs) - 1;
    foreach ($crumbs as $i => [$name, $path]) {
        $out .= $i === $last
            ? '<li aria-current="page">' . e($name) . '</li>'
            : '<li><a href="' . e($path) . '">' . e($name) . '</a></li>';
    }
    return $out . '</ol></nav>';
}

function render_page(array $page, string $main): void
{
    $path   = $page['path'];
    $canon  = SITE_URL . $path;
    $title  = $page['title'];
    $desc   = $page['desc'];
    $image  = abs_url($page['image'] ?? IMG['og']);
    $type   = $page['type'] ?? 'website';
    $graph  = array_merge([schema_org(), schema_website()], $page['schema'] ?? []);
    if (!empty($page['crumbs'])) {
        $graph[] = schema_breadcrumbs($page['crumbs']);
    }
    $ld = json_encode(['@context' => 'https://schema.org', '@graph' => $graph], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
    $bodyClass = $page['body_class'] ?? '';
    header('Content-Type: text/html; charset=utf-8');
    ?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canon) ?>">
<meta name="robots" content="<?= empty($page['noindex']) ? 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1' : 'noindex, follow' ?>">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="<?= $type === 'article' ? 'article' : 'website' ?>">
<meta property="og:title" content="<?= e($page['og_title'] ?? $title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canon) ?>">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<?php if ($type === 'article'): ?>
<meta property="article:published_time" content="<?= e(iso_date($page['published'])) ?>">
<meta property="article:modified_time" content="<?= e(iso_date($page['modified'])) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($page['og_title'] ?? $title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<meta name="theme-color" content="#3B2A1E">
<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="shortcut icon" href="/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<meta name="apple-mobile-web-app-title" content="Pure Goat Farms">
<meta name="application-name" content="Pure Goat Farms">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="Pure Goat Farms &raquo; Feed" href="<?= SITE_URL ?>/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700;9..144,800&family=Libre+Franklin:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap">
<link rel="stylesheet" href="<?= asset('/assets/css/style.css') ?>">
<?php if (!empty($page['preload'])): ?>
<link rel="preload" as="image" href="<?= e($page['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<script type="application/ld+json"><?= $ld ?></script>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA_ID ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '<?= GA_ID ?>');
</script>
</head>
<body class="<?= e($bodyClass) ?>">
<a class="skip-link" href="#content">Skip to content</a>
<?php if ($type === 'article'): ?><div class="read-progress" aria-hidden="true"><span></span></div><?php endif; ?>
<header class="site-header" id="top">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Pure Goat Farms home">
      <img src="<?= IMG['logo'] ?>" alt="Pure Goat Farms" width="600" height="117">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach (nav_items() as [$label, $href, $children]):
        $active = $href === '/' ? $path === '/' : str_starts_with($path, $href);
        if ($label === 'Blog' && (str_starts_with($path, '/category/') || ($type === 'article'))) { $active = true; } ?>
        <li class="<?= $children ? 'has-sub' : '' ?><?= $active ? ' is-active' : '' ?>">
          <a href="<?= e($href) ?>"<?= $active ? ' aria-current="page"' : '' ?>><?= e($label) ?></a>
<?php if ($children): ?>
          <button class="sub-toggle" type="button" aria-expanded="false" aria-label="Open <?= e($label) ?> menu"><?= icon('chev') ?></button>
          <ul class="sub">
<?php foreach ($children as [$cl, $ch]): ?>
            <li><a href="<?= e($ch) ?>"><?= e($cl) ?></a></li>
<?php endforeach; ?>
          </ul>
<?php endif; ?>
        </li>
<?php endforeach; ?>
      </ul>
      <a class="btn btn--sm btn--rust nav-cta" href="/contact/">Contact</a>
    </nav>
    <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu"><?= icon('menu', 'ico ico-open') ?><?= icon('close', 'ico ico-close') ?></button>
  </div>
</header>
<main id="content">
<?= $main ?>
</main>
<section class="cta-band">
  <div class="container cta-band__inner reveal">
    <div>
      <p class="eyebrow eyebrow--light">Field notes</p>
      <h2>Get one field note a month.</h2>
      <p>Seasonal reminders — breeding windows, hoof trims, pasture rotation — sent when you actually need them.</p>
    </div>
    <div class="cta-band__actions">
      <a class="btn btn--gold" href="/contact/">Ask Us A Question</a>
      <a class="btn btn--ghost-light" href="/blog/">Start Reading</a>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="container site-footer__grid">
    <div class="site-footer__brand">
      <a href="/"><img src="<?= IMG['logo_wh'] ?>" alt="Pure Goat Farms" width="600" height="117" loading="lazy"></a>
      <p>Practical, field-tested guidance on raising, milking, and caring for goats — written from a working farm, not a stock-photo library.</p>
      <a class="footer-mail" href="mailto:<?= SITE_EMAIL ?>"><?= icon('mail') ?> <?= SITE_EMAIL ?></a>
    </div>
    <div>
      <h4>Quick Links</h4>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about/">About Us</a></li>
        <li><a href="/blog/">Blog</a></li>
        <li><a href="/start-here/">Start Here</a></li>
        <li><a href="/faq/">Goat FAQ</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
    </div>
    <div>
      <h4>Categories</h4>
      <ul>
<?php foreach (['farm-life', 'goat-breeds', 'health-care', 'milking-dairy'] as $c): ?>
        <li><a href="/category/<?= $c ?>/"><?= e(CATEGORIES[$c]['name']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h4>Free Tools</h4>
      <ul>
<?php foreach (array_slice(TOOLS, 0, 5, true) as $slug => $t): ?>
        <li><a href="/tools/<?= $slug ?>/"><?= e($t['name']) ?></a></li>
<?php endforeach; ?>
        <li><a href="/tools/">All tools &rarr;</a></li>
      </ul>
    </div>
    <div class="site-footer__news" id="newsletter">
      <h4>Newsletter</h4>
      <p>One email a month. Real farm notes, no fluff.</p>
      <form class="news-form" action="/subscribe/" method="post">
        <label class="sr-only" for="news-email">Email address</label>
        <input id="news-email" type="email" name="email" placeholder="Email address" required autocomplete="email">
        <input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <input type="hidden" name="ts" value="<?= time() ?>">
        <button class="btn btn--gold" type="submit">Subscribe</button>
      </form>
    </div>
  </div>
  <div class="container site-footer__bottom">
    <p>&copy; <?= date('Y') ?> Pure Goat Farms. All rights reserved.</p>
    <ul>
      <li><a href="/privacy-policy/">Privacy Policy</a></li>
      <li><a href="/terms-of-use/">Terms of Use</a></li>
      <li><a href="/affiliate-disclosure/">Affiliate Disclosure</a></li>
      <li><a href="/sitemap/">Sitemap</a></li>
    </ul>
  </div>
  <p class="pgf-aff-footer">As an Amazon Associate, Pure Goat Farms earns from qualifying purchases.</p>
</footer>
<button class="to-top" type="button" aria-label="Back to top"><?= icon('up') ?></button>
<script src="<?= asset('/assets/js/main.js') ?>" defer></script>
<?php if (!empty($page['tools_js'])): ?>
<script src="<?= asset('/assets/js/tools.js') ?>" defer></script>
<?php endif; ?>
</body>
</html>
<?php
}
