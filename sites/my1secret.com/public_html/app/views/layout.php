<?php
defined('M1S') || exit;
/** @var string $content @var array $meta */
$me = current_user();
$title = full_title($meta['title'] ?? null);
$desc = $meta['description'] ?? M1S_DEFAULT_DESC;
$canonical = $meta['canonical'] ?? current_canonical();
$robots = $meta['robots'] ?? null;
if (!cfg('allow_indexing', true)) {
    $robots = 'noindex, nofollow';
}
$image = $meta['image'] ?? abs_url('/assets/img/og-default.png');
$flashes = take_flashes();
$path = strtok($_SERVER['REQUEST_URI'] ?? '/', '?');
$section = str_starts_with($path, '/blog') || str_starts_with($path, '/author') ? 'blog' : (str_starts_with($path, '/forum') || $path === '/submit/' ? 'forum' : '');
$openReports = $me && is_mod($me) ? (int)val('SELECT COUNT(*) FROM reports WHERE resolved_at IS NULL') : 0;
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<?php if (cfg('gtm_id', 'GTM-TGKSZ6DG') && !str_starts_with($path, '/admin')): $gtm = cfg('gtm_id', 'GTM-TGKSZ6DG'); ?>
<!-- Google Tag Manager -->
<script nonce="<?= e(csp_nonce()) ?>">
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  dataLayer.push({'gtm.start': new Date().getTime(), event: 'gtm.js'});
</script>
<script async nonce="<?= e(csp_nonce()) ?>" src="https://www.googletagmanager.com/gtm.js?id=<?= e($gtm) ?>"></script>
<!-- End Google Tag Manager -->
<?php endif; ?>

<title><?= e($title) ?></title>
<meta name="description" content="<?= e($desc) ?>">
<link rel="canonical" href="<?= e($canonical) ?>">
<?php if ($robots): ?><meta name="robots" content="<?= e($robots) ?>">
<?php else: ?><meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<?php endif; ?>
<meta property="og:site_name" content="<?= e(cfg('site_name')) ?>">
<meta property="og:type" content="<?= e($meta['type'] ?? 'website') ?>">
<meta property="og:title" content="<?= e($meta['title'] ?? cfg('site_name')) ?>">
<meta property="og:description" content="<?= e($desc) ?>">
<meta property="og:url" content="<?= e($canonical) ?>">
<meta property="og:image" content="<?= e($image) ?>">
<meta property="og:locale" content="en_US">
<?php if (!empty($meta['published'])): ?><meta property="article:published_time" content="<?= e($meta['published']) ?>">
<meta property="article:modified_time" content="<?= e($meta['modified']) ?>">
<?php endif; ?>
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0f2233">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest?v=2">
<link rel="alternate" type="application/rss+xml" title="<?= e(cfg('site_name')) ?> blog" href="/feed/">
<link rel="stylesheet" href="<?= e(asset('assets/css/app.css')) ?>">
<script src="<?= e(asset('assets/js/app.js')) ?>" defer></script>
<?php if (!empty($meta['jsonld'])): ?><?= jsonld_tag($meta['jsonld']) ?>
<?php endif; ?>
</head>
<body class="<?= e($meta['body_class'] ?? '') ?>">
<?php if (!empty($gtm)): ?><noscript><iframe src="https://www.googletagmanager.com/ns.html?id=<?= e($gtm) ?>" height="0" width="0" style="display:none;visibility:hidden" title="Google Tag Manager"></iframe></noscript><?php endif; ?>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/" aria-label="My 1 Secret home">
      <img src="/assets/img/my1secret-logo.webp" alt="My 1 Secret" width="184" height="60">
    </a>
    <nav class="main-nav" aria-label="Main">
      <a href="/blog/"<?= $section === 'blog' ? ' aria-current="page"' : '' ?>>Blog</a>
      <a href="/forum/"<?= $section === 'forum' ? ' aria-current="page"' : '' ?>>Forum</a>
      <a href="/shop/"<?= str_starts_with($path, '/shop') ? ' aria-current="page"' : '' ?>>Shop</a>
      <details class="dropdown">
        <summary>Topics</summary>
        <div class="dropdown-menu">
          <?php foreach (topics() as $t): ?><a href="<?= e(topic_url($t)) ?>"><?= e($t['name']) ?></a><?php endforeach; ?>
        </div>
      </details>
    </nav>
    <form class="search" action="/search/" method="get" role="search">
      <label class="sr-only" for="site-q">Search My 1 Secret</label>
      <input id="site-q" type="search" name="q" placeholder="Search guides & posts" value="<?= e($_GET['q'] ?? '') ?>" maxlength="100">
    </form>
    <div class="header-actions">
      <?php if ($me): ?>
        <a class="btn btn-accent btn-sm" href="/submit/">+ Post</a>
        <details class="dropdown user-menu">
          <summary><span class="avatar" style="--h:<?= crc32($me['username']) % 360 ?>"><?= e(strtoupper(substr($me['username'], 0, 1))) ?></span><span class="sr-only">Account menu</span><?php if ($openReports): ?><span class="dot" title="Open reports"></span><?php endif; ?></summary>
          <div class="dropdown-menu dropdown-right">
            <span class="menu-label">u/<?= e($me['username']) ?> · <?= number_format((int)$me['karma']) ?> karma</span>
            <a href="<?= e(user_url($me)) ?>">My profile</a>
            <a href="/settings/">Settings</a>
            <?php if (is_mod($me)): ?><a href="/admin/">Admin<?= $openReports ? ' (' . $openReports . ' reports)' : '' ?></a><?php endif; ?>
            <form method="post" action="/logout/"><?= csrf_field() ?><button type="submit" class="linklike">Log out</button></form>
          </div>
        </details>
      <?php else: ?>
        <a class="btn btn-accent btn-sm hide-sm" href="/submit/">+ Post</a>
        <a class="btn btn-ghost-light btn-sm" href="/login/?next=<?= e(rawurlencode($_SERVER['REQUEST_URI'] ?? '/')) ?>">Log in</a>
        <a class="btn btn-accent btn-sm" href="/register/">Join</a>
      <?php endif; ?>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mobile-nav"><span class="sr-only">Menu</span><span></span></button>
    </div>
  </div>
  <nav id="mobile-nav" class="mobile-nav" aria-label="Mobile" hidden>
    <a href="/blog/">Blog</a><a href="/forum/">Forum</a><a href="/shop/">Shop</a>
    <?php foreach (topics() as $t): ?><a href="<?= e(topic_url($t)) ?>"><?= e($t['name']) ?></a><?php endforeach; ?>
    <form action="/search/" method="get"><input type="search" name="q" placeholder="Search" aria-label="Search"></form>
  </nav>
</header>

<main id="main" class="wrap main">
<?php if (!empty($meta['breadcrumbs'])): ?>
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><?php foreach ($meta['breadcrumbs'] as [$n, $u]): ?> <span aria-hidden="true">›</span> <?= $u ? '<a href="' . e($u) . '">' . e($n) . '</a>' : '<span>' . e($n) . '</span>' ?><?php endforeach; ?></nav>
<?php endif; ?>
<?php foreach ($flashes as [$type, $msg]): ?>
  <div class="flash flash-<?= e($type) ?>" role="status"><?= e($msg) ?></div>
<?php endforeach; ?>
<?= $content ?>
</main>

<footer class="site-footer">
  <div class="wrap footer-grid">
    <div>
      <img src="/assets/img/my1secret-logo.webp" alt="My 1 Secret" width="147" height="48" loading="lazy">
      <p><?= e(M1S_TAGLINE) ?>. Read the guides, then ask the community.</p>
    </div>
    <div>
      <h2>Blog topics</h2>
      <?php foreach (topics() as $t): ?><a href="<?= e(topic_url($t)) ?>"><?= e($t['name']) ?></a><?php endforeach; ?>
    </div>
    <div>
      <h2>Communities</h2>
      <?php foreach (communities() as $c): ?><a href="<?= e(community_url($c)) ?>"><?= e($c['name']) ?></a><?php endforeach; ?>
    </div>
    <div>
      <h2>My 1 Secret</h2>
      <a href="/about/">About</a><a href="/community-guidelines/">Community guidelines</a><a href="/contact/">Contact</a>
      <a href="/shop/">Renter essentials shop</a><a href="/privacy-policy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="/feed/">RSS feed</a>
    </div>
  </div>
  <p class="wrap fineprint">© <?= gmdate('Y') ?> My 1 Secret. Community posts are the opinions of their authors and are not professional advice. <?= e(amazon_disclosure()) ?></p>
</footer>
</body>
</html>
