<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/** @var array $page */
$current = $page['path'];
$isCurrent = fn (string $p) => $current === $p ? ' aria-current="page"' : '';
$inSection = fn (string $p) => str_starts_with($current, $p) && $current !== $p ? ' class="is-section"' : '';
$links = [
    '/about/'                   => 'About',
    '/service-area/'            => 'Service Area',
    '/roofing-project-planner/' => 'Project Planner',
    '/blog/'                    => 'Blog',
    '/faqs/'                    => 'FAQs',
    '/contact/'                 => 'Contact',
];
?>
<header class="site-header" data-header>
  <div class="container header-inner">
    <a class="brand" href="/"<?= $current === '/' ? ' aria-current="page"' : '' ?>>
      <?php partial('logo'); ?>
      <span class="brand-text"><span class="brand-name">Friendswood Roofers</span><span class="brand-tag">Friendswood, TX</span></span>
    </a>

    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" data-nav-toggle>
      <span class="nav-toggle-open"><?= icon('menu') ?><span class="sr-only">Open menu</span></span>
      <span class="nav-toggle-close"><?= icon('close') ?><span class="sr-only">Close menu</span></span>
      <span class="nav-toggle-label" aria-hidden="true">Menu</span>
    </button>

    <nav class="site-nav" id="site-nav" aria-label="Main" data-nav>
      <ul class="nav-list">
        <li class="nav-item has-sub" data-submenu>
          <a href="/services/"<?= $isCurrent('/services/') ?><?= $inSection('/services/') ?>>Services</a>
          <button class="sub-toggle" type="button" aria-expanded="false" aria-controls="services-menu" data-submenu-toggle>
            <?= icon('chevron', 'icon icon-sm') ?><span class="sr-only">Show service pages</span>
          </button>
          <ul class="sub-menu" id="services-menu">
            <li><a href="/services/"<?= $isCurrent('/services/') ?>>All roofing services</a></li>
            <?php foreach (services() as $slug => $s): ?>
            <li><a href="/services/<?= e($slug) ?>/"<?= $isCurrent('/services/' . $slug . '/') ?>><?= e($s['name']) ?></a></li>
            <?php endforeach; ?>
          </ul>
        </li>
        <?php foreach ($links as $href => $label): ?>
        <li class="nav-item"><a href="<?= e($href) ?>"<?= $isCurrent($href) ?><?= $inSection($href) ?>><?= e($label) ?></a></li>
        <?php endforeach; ?>
      </ul>
      <div class="nav-actions">
        <a class="btn btn-ghost btn-call" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span class="btn-call-full"><span class="sr-only">Call </span><?= e(phone_display()) ?></span><span class="btn-call-short">Call Now <span class="sr-only"><?= e(phone_display()) ?></span></span></a>
        <a class="btn btn-accent" href="/contact/#estimate-form">Request an Estimate</a>
      </div>
    </nav>
  </div>
</header>
