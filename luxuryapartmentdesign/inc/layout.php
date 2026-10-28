<?php
// Shared <head>, header and footer.
//
// $page keys: title, description, path, image (absolute or stem), type
// (website|article), robots, schema (array of nodes), published, updated,
// scripts (extra js files under assets/js/), body_class.

function page_head(array $page): void
{
    $canonical = url($page['path']);
    $image = $page['image'] ?? 'japandi-rug';
    $image = str_starts_with($image, 'http') ? $image : url(img_url($image));
    $robots = $page['robots'] ?? 'index, follow, max-image-preview:large, max-snippet:-1';
    $GLOBALS['page_scripts'] = $page['scripts'] ?? [];
    ?>
<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($page['title']) ?></title>
<meta name="description" content="<?= e($page['description']) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<meta name="robots" content="<?= e($robots) ?>">
<meta property="og:locale" content="en_US">
<meta property="og:site_name" content="<?= e(SITE_NAME) ?>">
<meta property="og:type" content="<?= e($page['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($page['title']) ?>">
<meta property="og:description" content="<?= e($page['description']) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<?php if (!empty($page['published'])): ?>
<meta property="article:published_time" content="<?= e($page['published']) ?>T08:00:00+00:00">
<meta property="article:modified_time" content="<?= e($page['updated'] ?? $page['published']) ?>T08:00:00+00:00">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="<?= e($page['title']) ?>">
<meta name="twitter:description" content="<?= e($page['description']) ?>">
<meta name="twitter:image" content="<?= e($image) ?>">
<meta name="theme-color" content="#1c1a17">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Jost:wght@400;500;600&display=swap">
<link rel="stylesheet" href="<?= asset('css/style.css') ?>">
<?php if (!empty($page['preload'])): ?>
<link rel="preload" as="image" href="<?= e($page['preload']) ?>" fetchpriority="high">
<?php endif; ?>
<link rel="alternate" type="application/rss+xml" title="<?= e(SITE_NAME) ?>" href="<?= url('/rss.xml') ?>">
<?= schema_graph($page['schema'] ?? []) ?>

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=<?= GA4_ID ?>"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', '<?= GA4_ID ?>');
  gtag('config', '<?= GA_TAG ?>');
</script>
</head>
<body class="<?= e($page['body_class'] ?? '') ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="progress" aria-hidden="true"><span></span></div>
<header class="site-header">
  <div class="container site-header__inner">
    <a class="logo" href="/" aria-label="<?= e(SITE_NAME) ?> home">
      <img src="/assets/img/logo.webp" alt="<?= e(SITE_NAME) ?>" width="188" height="60">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      <ul>
<?php foreach (NAV as [$label, $href]):
        $active = str_starts_with($page['path'], $href) && $href !== '/' ? ' aria-current="page"' : ''; ?>
        <li><a href="<?= e($href) ?>"<?= $active ?>><?= e($label) ?></a></li>
<?php endforeach; ?>
      </ul>
    </nav>
    <div class="site-header__actions">
      <button class="icon-btn" type="button" data-search-open aria-label="Search"><?= icon('search') ?></button>
      <a class="btn btn--small btn--gold header-cta" href="/tools/interior-design-style-quiz/">Style Quiz</a>
      <button class="icon-btn nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Menu"><?= icon('menu') ?></button>
    </div>
  </div>
</header>
<div class="search-overlay" hidden>
  <div class="search-overlay__panel" role="dialog" aria-modal="true" aria-label="Search the site">
    <form action="/search/" method="get" class="search-overlay__form">
      <?= icon('search') ?>
      <label class="sr-only" for="site-search">Search articles and tools</label>
      <input id="site-search" type="search" name="q" placeholder="Search guides and tools…" autocomplete="off">
      <button type="button" class="icon-btn" data-search-close aria-label="Close search"><?= icon('close') ?></button>
    </form>
    <ul class="search-overlay__results" aria-live="polite"></ul>
  </div>
</div>
<main id="main">
<?php
}

function page_foot(array $page = []): void
{
    $year = date('Y');
    ?>
</main>
<footer class="site-footer">
  <div class="container site-footer__grid">
    <div class="site-footer__brand">
      <img src="/assets/img/logo.webp" alt="<?= e(SITE_NAME) ?>" width="188" height="60" loading="lazy">
      <p><?= e(SITE_NAME) ?> publishes practical, measurement-driven guides and free design tools that help apartment dwellers and renters create a home that feels high-end.</p>
    </div>
    <div>
      <h2 class="site-footer__title">Topics</h2>
      <ul>
<?php foreach (CATEGORIES as $slug => $c): ?>
        <li><a href="/category/<?= $slug ?>/"><?= e($c['name']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
    <div>
      <h2 class="site-footer__title">Free Design Tools</h2>
      <ul>
<?php foreach (array_slice(TOOLS, 0, 6, true) as $slug => $t): ?>
        <li><a href="/tools/<?= $slug ?>/"><?= e($t['name']) ?></a></li>
<?php endforeach; ?>
        <li><a href="/tools/">All tools</a></li>
      </ul>
    </div>
    <div>
      <h2 class="site-footer__title"><?= e(SITE_NAME) ?></h2>
      <ul>
        <li><a href="/about-us/">About Us</a></li>
        <li><a href="/editorial-policy/">Editorial Policy</a></li>
        <li><a href="/blogs/">All Articles</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/sitemap/">Sitemap</a></li>
      </ul>
    </div>
  </div>
  <div class="container site-footer__bottom">
    <p>&copy; <?= $year ?> <?= e(SITE_NAME) ?>. All rights reserved.</p>
    <p><a href="/privacy-policy/">Privacy Policy</a> · <a href="/terms-of-use/">Terms of Use</a></p>
  </div>
</footer>
<button class="to-top" type="button" aria-label="Back to top">&uarr;</button>
<script src="<?= asset('js/main.js') ?>" defer></script>
<?php foreach ($page['scripts'] ?? $GLOBALS['page_scripts'] ?? [] as $s): ?>
<script src="<?= asset('js/' . $s) ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
<?php
}
