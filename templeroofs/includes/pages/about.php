<?php
defined('TR_ROOT') || exit;
$c = page_content('about');
$crumbs = [['About', '/about/']];
layout_start([
    'title'       => $c['seo_title'] ?? 'About Temple Roofers',
    'description' => $c['meta_description'] ?? '',
    'path'        => '/about/',
    'crumbs'      => $crumbs,
    'image'       => 'roofer-installing-shingles',
    'preload_image' => 'roofer-installing-shingles',
]);
page_hero(['h1' => $c['h1'] ?? 'About Temple Roofers', 'lead' => $c['hero_lead'] ?? '', 'image' => 'roofer-installing-shingles', 'alt' => 'Roofer installing asphalt shingles on a residential roof', 'crumbs' => $crumbs, 'eyebrow' => 'Roofing contractor · Temple, Texas']);
?>
<div class="container content-layout">
  <article class="prose">
    <?= render_body($c['body'] ?? '', 'See how we work — book a free inspection') ?>
  </article>
  <aside class="sidebar">
    <div class="sidebar__sticky">
      <div class="side-card side-card--navy">
        <p class="side-card__title">Talk to Temple Roofers</p>
        <p>Questions about your roof, a storm or an estimate? Call us or request a free inspection online.</p>
        <a class="btn btn--gold btn--block" href="/free-roof-inspection/">Free Roof Inspection</a>
        <a class="btn btn--outline-light btn--block" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <?= e(cfg('phone_display')) ?></a>
      </div>
      <div class="side-card">
        <p class="side-card__title">Explore</p>
        <ul class="side-links">
          <li><a href="/services/"><?= icon('wrench') ?> Roofing services</a></li>
          <li><a href="/service-areas/"><?= icon('map-pin') ?> Service areas</a></li>
          <li><a href="/tools/"><?= icon('calculator') ?> Free roofing tools</a></li>
          <li><a href="/weather/"><?= icon('cloud-sun') ?> Temple weather</a></li>
          <li><a href="/blog/"><?= icon('book') ?> Roofing blog</a></li>
        </ul>
      </div>
    </div>
  </aside>
</div>
<?php final_cta('Ready When You Are: Schedule a Free Roof Inspection', '', '/about/'); ?>
<?php layout_end();
