<?php
defined('TR_ROOT') || exit;
$crumbs = [['Service Areas', '/service-areas/']];
$areas = areas();
layout_start([
    'title'       => 'Roofing Service Areas Near Temple, TX',
    'description' => 'Temple Roofers serves Temple, Belton, Troy, Salado, Harker Heights, Nolanville and nearby Bell County communities. Free roof inspections.',
    'path'        => '/service-areas/',
    'crumbs'      => $crumbs,
    'image'       => 'central-texas-neighborhood',
    'preload_image' => 'central-texas-neighborhood',
]);
page_hero(['h1' => 'Roofing Service Areas Around Temple, TX', 'lead' => 'Based in Temple and serving the surrounding Bell County communities with roof repairs, replacements, storm damage help and free inspections.', 'image' => 'central-texas-neighborhood', 'alt' => 'Residential street with single-family homes on a sunny day', 'crumbs' => $crumbs, 'eyebrow' => 'Where we work']);
$temple = $areas['temple-tx'] ?? null;
?>
<section class="section">
  <div class="container split split--top">
    <div class="split__copy reveal">
      <p class="eyebrow">Home base</p>
      <h2 class="section-title">Temple First, Then the Communities Around It</h2>
      <p>Temple is where we are based and where most of our roofing work happens. Because we are close by, scheduling a free inspection is straightforward, and after a storm we can usually get eyes on Temple roofs quickly.</p>
      <p>We also serve the towns along I-35 and US-190 that share the same Central Texas weather: lake communities exposed to open-water wind, historic homes with older flashing details, newer subdivisions with builder-grade roofs and rural properties with metal barns and shops. Each page below covers what matters for roofs in that community.</p>
      <?php if ($temple): ?><a class="btn btn--navy" href="<?= e($temple['url']) ?>">Roofing in Temple, TX</a><?php endif; ?>
    </div>
    <div class="area-grid area-grid--wide">
      <?php foreach ($areas as $a): ?><?= area_card($a) ?><?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <?= section_head('Community guides', 'Roofing Notes for Each Community', 'A quick look at what we keep in mind when inspecting roofs in each town we serve.') ?>
    <div class="card-grid card-grid--3">
      <?php foreach ($areas as $a): ?>
      <article class="card card--area reveal">
        <a class="card__media" href="<?= e($a['url']) ?>" tabindex="-1" aria-hidden="true"><?= img($a['image'], '', ['sizes' => '(max-width: 640px) 100vw, 33vw', 'decorative' => true]) ?></a>
        <div class="card__body">
          <h3 class="card__title"><a href="<?= e($a['url']) ?>"><?= e($a['city']) ?>, TX</a></h3>
          <p class="card__meta"><?= icon('map-pin') ?> <?= e($a['distance_note']) ?></p>
          <p><?= e($a['card_summary']) ?></p>
          <a class="card__link" href="<?= e($a['url']) ?>">Roofing in <?= e($a['city']) ?> <?= icon('arrow-right') ?></a>
        </div>
      </article>
      <?php endforeach; ?>
    </div>
    <p class="center-note reveal">Don't see your town? If you are near Temple, call <a href="<?= e(tel_href()) ?>"><?= e(cfg('phone_display')) ?></a> and ask — we will tell you honestly whether we can help.</p>
  </div>
</section>
<?php final_cta('Book a Free Roof Inspection Near Temple', '', '/service-areas/'); ?>
<?php layout_end();
