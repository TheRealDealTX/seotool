<?php
/** @var string $content  @var array $page */
$title = seo_title($page['title'] ?? SITE_NAME);
$desc = seo_desc($page['desc'] ?? '');
$path = $page['path'] ?? '/';
$robots = $page['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1';
$ogImage = canonical($page['og_image'] ?? '/assets/img/og-default.jpg');
$schema = $page['schema'] ?? [];
$navTopics = ['lamb', 'brining', 'baking', 'canning', 'goats', 'chickens-eggs', 'homestead', 'crafts'];
?><!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<?php if (is_production_host()): ?>
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-JB48YFCMM7"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-JB48YFCMM7');
</script>
<?php endif ?>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<link rel="canonical" href="<?= e(canonical($path)) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:type" content="<?= e($page['og_type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($title) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e(canonical($path)) ?>">
<meta property="og:image" content="<?= e($ogImage) ?>">
<?php if (!empty($page['og_image_w'])): ?><meta property="og:image:width" content="<?= (int)$page['og_image_w'] ?>">
<meta property="og:image:height" content="<?= (int)$page['og_image_h'] ?>">
<?php else: ?><meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<?php endif ?>
<meta property="og:image:alt" content="<?= e($page['og_image_alt'] ?? $title) ?>">
<?php foreach ($page['article'] ?? [] as $prop => $val): ?><meta property="article:<?= e($prop) ?>" content="<?= e($val) ?>">
<?php endforeach ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($title) ?>">
<meta name="twitter:description" content="<?= e($desc) ?>">
<meta name="twitter:image" content="<?= e($ogImage) ?>">
<meta name="theme-color" content="#1C352D">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/assets/img/favicon-96x96.png" type="image/png" sizes="96x96">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="application/rss+xml" title="<?= e(SITE_NAME) ?> Feed" href="/feed/">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&family=Fraunces:opsz,wght,SOFT@9..144,400..800,50..100&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="<?= asset('css/site.css') ?>">
<?php if (!empty($page['preload'])): ?><link rel="preload" as="image" href="<?= e($page['preload']) ?>" fetchpriority="high"><?php endif ?>
<?= json_ld(['@context' => 'https://schema.org', '@graph' => array_merge([
    org_schema(),
    ['@type' => 'WebSite', '@id' => SITE_ORIGIN . '/#website', 'url' => SITE_ORIGIN . '/', 'name' => SITE_NAME, 'publisher' => ['@id' => SITE_ORIGIN . '/#organization'],
     'potentialAction' => ['@type' => 'SearchAction', 'target' => SITE_ORIGIN . '/?s={search_term_string}', 'query-input' => 'required name=search_term_string']],
], $schema)]) ?>
</head>
<body class="<?= e($page['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header" data-header>
  <div class="wrap site-header__inner">
    <a class="brand" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <img src="/assets/img/purely-wholesome-farm-logo.webp" alt="<?= e(SITE_NAME) ?>" width="600" height="81">
      <span class="brand__farm">Farm</span>
    </a>
    <nav class="nav" aria-label="Main" data-nav>
      <ul class="nav__list">
        <li class="nav__item nav__item--mega">
          <button class="nav__link" aria-expanded="false" data-mega-toggle>Recipes &amp; Guides <?= icon('chevron') ?></button>
          <div class="mega" data-mega>
            <div class="mega__grid">
              <?php foreach ($navTopics as $t): [$label, $blurb] = TOPICS[$t]; ?>
                <a class="mega__item" href="/topics/<?= $t ?>/"><span class="mega__dot mega__dot--<?= $t ?>"></span><strong><?= e($label) ?></strong><small><?= e($blurb) ?></small></a>
              <?php endforeach ?>
            </div>
            <a class="mega__all" href="/blog/">Browse the whole journal <?= icon('arrow') ?></a>
          </div>
        </li>
        <li class="nav__item"><a class="nav__link" href="/tools/">Farm Tools <span class="nav__badge">9</span></a></li>
        <li class="nav__item"><a class="nav__link" href="/blog/">Journal</a></li>
        <li class="nav__item"><a class="nav__link" href="/about-us/">About</a></li>
        <li class="nav__item"><a class="nav__link" href="/contact-us/">Contact</a></li>
      </ul>
    </nav>
    <div class="site-header__actions">
      <button class="icon-btn" data-search-open aria-label="Search (press /)"><?= icon('search') ?><kbd>/</kbd></button>
      <button class="icon-btn icon-btn--menu" data-menu aria-label="Open menu" aria-expanded="false" aria-controls="drawer"><span class="burger" aria-hidden="true"><i></i><i></i><i></i></span></button>
    </div>
  </div>
</header>

<div class="drawer" id="drawer" data-drawer hidden>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <button type="button" class="drawer__search" data-search-open><?= icon('search') ?><span>Search recipes, guides &amp; tools</span></button>
    <nav class="drawer__links" aria-label="Mobile">
      <a href="/blog/"><span><?= icon('book') ?></span>The Farm Journal<?= icon('arrow') ?></a>
      <a href="/tools/"><span><?= icon('tool') ?></span>Farm Tools <em>9 free</em><?= icon('arrow') ?></a>
      <a href="/about-us/"><span><?= icon('sprout') ?></span>About Us<?= icon('arrow') ?></a>
      <a href="/contact-us/"><span><?= icon('mail') ?></span>Contact<?= icon('arrow') ?></a>
    </nav>
    <p class="drawer__label">Browse by topic</p>
    <div class="drawer__topics">
      <?php foreach ($navTopics as $t): ?>
        <a href="/topics/<?= $t ?>/"><span class="mega__dot mega__dot--<?= $t ?>"></span><?= e(TOPICS[$t][0]) ?></a>
      <?php endforeach ?>
    </div>
    <a class="drawer__cta" href="/tools/brine-calculator/">
      <span class="drawer__cta-icon"><?= icon('flask') ?></span>
      <span><strong>Try the Brine Calculator</strong><small>Exact salt for any salt brand, in seconds</small></span>
      <?= icon('arrow') ?>
    </a>
    <p class="drawer__foot hand">Grow better, live simpler.</p>
  </div>
</div>

<main id="main"><?= $content ?></main>

<footer class="site-footer">
  <svg class="site-footer__wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 40c160 40 320 50 480 30S800 0 960 10s320 60 480 40V90H0Z" fill="currentColor"/></svg>
  <div class="wrap site-footer__grid">
    <div class="site-footer__brand">
      <img src="/assets/img/purely-wholesome-farm-logo.webp" alt="<?= e(SITE_NAME) ?>" width="600" height="81" loading="lazy">
      <p>Purely Wholesome Farm is a farm kitchen and homestead journal: tested recipes, honest livestock know-how and free tools that make country living a little simpler.</p>
      <p class="hand">Grow better, live simpler.</p>
    </div>
    <div>
      <h2>Explore</h2>
      <ul>
        <?php foreach (array_slice($navTopics, 0, 6) as $t): ?><li><a href="/topics/<?= $t ?>/"><?= e(TOPICS[$t][0]) ?></a></li><?php endforeach ?>
      </ul>
    </div>
    <div>
      <h2>Farm Tools</h2>
      <ul>
        <?php foreach (array_slice(tools(), 0, 6, true) as $slug => $t): ?><li><a href="/tools/<?= $slug ?>/"><?= e($t['name']) ?></a></li><?php endforeach ?>
      </ul>
    </div>
    <div>
      <h2>The Farm</h2>
      <ul>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="/editorial-policy/">Editorial Policy</a></li>
        <li><a href="/contact-us/">Contact</a></li>
        <li><a href="/blog/">All Articles</a></li>
        <li><a href="/privacy-policy/">Privacy Policy</a></li>
        <li><a href="/terms-of-use/">Terms of Use</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap site-footer__bottom">
    <p>© <?= date('Y') ?> Purely Wholesome Farm. All rights reserved.</p>
    <p>Information on this site is for general education. For animal health concerns, consult your veterinarian.</p>
  </div>
</footer>

<div class="search" data-search-overlay hidden>
  <div class="search__backdrop" data-search-close></div>
  <div class="search__panel" role="dialog" aria-modal="true" aria-label="Search">
    <form class="search__form" action="/" method="get" role="search">
      <?= icon('search') ?>
      <input type="search" name="s" placeholder="Search recipes, guides and tools…" autocomplete="off" data-search-input aria-label="Search">
      <button type="button" class="icon-btn" data-search-close aria-label="Close search"><?= icon('close') ?></button>
    </form>
    <div class="search__results" data-search-results>
      <p class="search__hint">Try <button type="button" data-q="brine">brine</button> <button type="button" data-q="lamb chops">lamb chops</button> <button type="button" data-q="pumpkin pie">pumpkin pie</button> <button type="button" data-q="goat">goat</button> <button type="button" data-q="eggs">eggs</button></p>
    </div>
  </div>
</div>

<script src="<?= asset('js/site.js') ?>" defer></script>
<script src="<?= asset('js/tools.js') ?>" defer></script>
</body>
</html>
