<?php
defined('GAP') || exit;
/** @var array $CFG @var array $CAT @var string $content */
$meta = $meta ?? [];
$title = isset($meta['title']) ? $meta['title'] . ' | ' . $CFG['name'] : $CFG['name'] . ' — ' . $CFG['tagline'];
$desc = $meta['desc'] ?? '';
$canon = isset($meta['canonical']) ? abs_url($meta['canonical']) : null;
$noindex = !$CFG['live'] || !empty($meta['noindex']);
$ld = [
    '@context' => 'https://schema.org',
    '@graph' => array_values(array_filter(array_merge([
        ['@type' => 'Organization', '@id' => abs_url('/#org'), 'name' => $CFG['name'], 'url' => abs_url('/'), 'logo' => abs_url('/static/images/logo.png')],
        ['@type' => 'WebSite', '@id' => abs_url('/#site'), 'name' => $CFG['name'], 'url' => abs_url('/'), 'publisher' => ['@id' => abs_url('/#org')],
         'potentialAction' => ['@type' => 'SearchAction', 'target' => abs_url('/search/?q={search_term_string}'), 'query-input' => 'required name=search_term_string']],
    ], $meta['jsonld'] ?? []))),
];
$depts = array_filter(array_map(fn($p) => $CAT['categories'][$p] ?? null, $CFG['departments']));
?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($title) ?></title>
<?php if ($desc): ?><meta name="description" content="<?= e($desc) ?>">
<?php endif; ?>
<?php if ($noindex): ?><meta name="robots" content="noindex, nofollow">
<?php endif; ?>
<?php if ($canon): ?><link rel="canonical" href="<?= e($canon) ?>">
<?php endif; ?>
<meta property="og:site_name" content="<?= e($CFG['name']) ?>">
<meta property="og:title" content="<?= e($meta['title'] ?? $CFG['name']) ?>">
<?php if ($desc): ?><meta property="og:description" content="<?= e($desc) ?>">
<?php endif; ?>
<meta property="og:type" content="<?= e($meta['og_type'] ?? 'website') ?>">
<?php if ($canon): ?><meta property="og:url" content="<?= e($canon) ?>">
<?php endif; ?>
<meta property="og:image" content="<?= e(abs_url('/static/images/og.png')) ?>">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#12261b">
<link rel="icon" href="/assets/img/logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/static/images/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;800;900&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v=<?= ASSET_V ?>">
<script type="application/ld+json"><?= json_encode($ld, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
</head>
<body class="<?= e($meta['body_class'] ?? '') ?>">
<a class="skip" href="#main">Skip to content</a>
<div class="rope-progress" aria-hidden="true"><span class="rope-line"></span><span class="rope-climber"></span></div>

<div class="topbar"><div class="wrap">
  <p><span class="dot"></span> Independent arborist gear picks · Typical prices shown, checked at the retailer</p>
  <p class="topbar-links"><a href="/tools/">Free gear tools</a><a href="/guides/">Buying guides</a></p>
</div></div>

<header class="site-header" id="top">
  <div class="wrap header-row">
    <button class="nav-toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mainnav"><span></span><span></span><span></span></button>
    <a class="logo" href="/" aria-label="<?= e($CFG['name']) ?> home">
      <img src="/assets/img/logo.svg" alt="" width="40" height="40">
      <span class="logo-text"><b>Gap</b> Arborist Supply</span>
    </a>
    <form class="search" action="/search/" method="get" role="search">
      <label class="sr" for="q">Search gear</label>
      <input id="q" name="q" type="search" placeholder="Search saws, saddles, rope, spurs…" autocomplete="off" data-livesearch>
      <button type="submit" aria-label="Search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></button>
      <div class="suggest" hidden></div>
    </form>
    <div class="header-icons">
      <a href="/cart/#saved" class="icon-btn" aria-label="Saved gear"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8 3.2 4 7 4c2.1 0 3.6 1.2 5 3 1.4-1.8 2.9-3 5-3 3.8 0 6.1 4 4.6 7.7C19.5 16.4 12 21 12 21z"/></svg><span class="badge" data-saved-count hidden>0</span></a>
      <a href="/cart/" class="icon-btn cart-btn" aria-label="Cart"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg><span class="badge" data-cart-count hidden>0</span></a>
    </div>
  </div>
  <nav class="mainnav" id="mainnav" aria-label="Departments">
    <div class="wrap">
      <ul class="dept-list">
<?php foreach ($depts as $d): ?>
        <li class="dept"><a href="<?= e($d['path']) ?>"><?= e($d['name']) ?></a>
<?php if ($d['children']): ?>
          <div class="mega"><div class="mega-inner">
            <div class="mega-cols">
<?php foreach (array_slice($d['children'], 0, 12) as $cp): $ch = $CAT['categories'][$cp]; ?>
              <a href="<?= e($cp) ?>"><img src="<?= kind_img($ch['kind']) ?>" alt="" width="36" height="36" loading="lazy"><span><?= e($ch['name']) ?></span></a>
<?php endforeach; ?>
            </div>
            <a class="mega-all" href="<?= e($d['path']) ?>">Shop all <?= e($d['name']) ?> →</a>
          </div></div>
<?php endif; ?>
        </li>
<?php endforeach; ?>
        <li class="dept dept-alt"><a href="/brands/">Brands</a></li>
        <li class="dept dept-alt"><a href="/tools/">Tools</a></li>
      </ul>
    </div>
  </nav>
</header>

<main id="main">
<?= $content ?>
</main>

<footer class="site-footer">
  <div class="canopy" aria-hidden="true"></div>
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <a class="logo" href="/"><img src="/assets/img/logo.svg" alt="" width="44" height="44"><span class="logo-text"><b>Gap</b> Arborist Supply</span></a>
      <p>Climbing, rigging, cutting and safety gear for tree care pros and serious homeowners, with straight-talking buying guides and free tools for the job.</p>
      <p class="disclosure-note">Some links on this site are affiliate links. If you buy through them we may earn a commission at no cost to you. <a href="/affiliate-disclosure/">How that works</a>.</p>
    </div>
    <div>
      <h2>Shop</h2>
      <ul><?php foreach ($depts as $d): ?><li><a href="<?= e($d['path']) ?>"><?= e($d['name']) ?></a></li><?php endforeach; ?><li><a href="/shop-all/">All gear</a></li></ul>
    </div>
    <div>
      <h2>Tools</h2>
      <ul><?php foreach (TOOLS as $slug => $t): ?><li><a href="/tools/<?= $slug ?>/"><?= e($t[0]) ?></a></li><?php endforeach; ?></ul>
      <h2>Guides</h2>
      <ul><?php foreach (array_slice($CAT['guides'], 0, 4) as $g): ?><li><a href="<?= e($g['path']) ?>"><?= e($g['h1']) ?></a></li><?php endforeach; ?></ul>
    </div>
    <div>
      <h2>Company</h2>
      <ul>
        <li><a href="/about/">About</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/brands/">Brands</a></li>
        <li><a href="/affiliate-disclosure/">Affiliate disclosure</a></li>
        <li><a href="/privacy-policy/">Privacy policy</a></li>
        <li><a href="/terms-of-use/">Terms of use</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-base">
    <p>© <?= date('Y') ?> <?= e($CFG['name']) ?>. Gear for working at height carries real risk: get trained, follow the manufacturer's instructions and ANSI Z133.</p>
    <a href="#top" class="to-top">Back to top ↑</a>
  </div>
</footer>

<div class="compare-bar" hidden>
  <div class="wrap"><div class="compare-items"></div><button class="btn btn-sm" type="button" data-compare-open>Compare</button><button class="btn btn-sm btn-ghost" type="button" data-compare-clear>Clear</button></div>
</div>
<dialog class="compare-dialog"><form method="dialog"><button class="dialog-x" aria-label="Close">×</button></form><div class="compare-table"></div></dialog>
<div class="toast" role="status" aria-live="polite"></div>

<script src="/assets/js/site.js?v=<?= ASSET_V ?>" defer></script>
<?php foreach ($meta['scripts'] ?? [] as $s): ?><script src="<?= e($s) ?>?v=<?= ASSET_V ?>" defer></script>
<?php endforeach; ?>
</body>
</html>
