<?php
/** @var array $page */
$current = $page['path'] ?? '/';
$bodyClass = 'type-' . ($page['_type'] ?? 'page') . ' tpl-' . ($page['template'] ?? 'default');
?>
<body class="<?= e($bodyClass) ?>">
<a class="skip-link" href="#main">Skip to content</a>
<div class="topbar">
  <div class="container topbar-inner">
    <p class="topbar-note"><?= icon('shield', 'icon icon-sm') ?> Licensed Texas Public Adjusting Firm &middot; TDI License #<?= e(cfg('license')) ?></p>
    <p class="topbar-links">
      <a href="mailto:<?= e(cfg('public_email')) ?>"><?= icon('mail', 'icon icon-sm') ?> <?= e(cfg('public_email')) ?></a>
      <a href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_display')) ?></a>
    </p>
  </div>
</div>
<header class="site-header" id="site-header">
  <div class="container header-inner">
    <a class="brand" href="/" aria-label="McAllen Public Adjuster home">
      <img src="/assets/img/logo-mark.svg" alt="" width="44" height="44">
      <span class="brand-text"><span class="brand-name">McAllen</span><span class="brand-sub">Public Adjuster</span></span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="Primary">
      <ul class="nav-list">
        <?php foreach (primary_nav() as $item):
            [$label, $href] = $item;
            $children = $item[2] ?? [];
            $active = ($href === '/' ? $current === '/' : strpos($current, $href) === 0);
            if ($children) {
                foreach ($children as $c) { if ($c[1] === $current) { $active = true; } }
            }
        ?>
        <li class="nav-item<?= $children ? ' has-sub' : '' ?><?= $active ? ' is-active' : '' ?>">
          <a href="<?= e($href) ?>"<?= $current === $href ? ' aria-current="page"' : '' ?>><?= e($label) ?></a>
          <?php if ($children): ?>
          <button class="sub-toggle" type="button" aria-expanded="false" aria-label="Show <?= e($label) ?> menu"><svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
          <ul class="sub-menu<?= count($children) > 9 ? ' sub-menu-wide' : '' ?>">
            <?php foreach ($children as [$cl, $ch]): ?>
            <li><a href="<?= e($ch) ?>"<?= $current === $ch ? ' aria-current="page"' : '' ?>><?= e($cl) ?></a></li>
            <?php endforeach; ?>
          </ul>
          <?php endif; ?>
        </li>
        <?php endforeach; ?>
      </ul>
      <div class="nav-mobile-cta">
        <a class="btn btn-gold btn-block" href="/free-claim-review/">Get a Free Claim Review</a>
        <a class="btn btn-outline-light btn-block" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> Call <?= e(cfg('phone_short')) ?></a>
      </div>
    </nav>
    <div class="header-actions">
      <a class="header-phone" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon') ?><span><small>Call now</small><?= e(cfg('phone_short')) ?></span></a>
      <a class="btn btn-gold btn-sm header-cta" href="/free-claim-review/">Free Claim Review</a>
      <button class="nav-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="Open menu">
        <span class="nav-toggle-bars" aria-hidden="true"><span></span><span></span><span></span></span>
      </button>
    </div>
  </div>
</header>
<main id="main" tabindex="-1">
