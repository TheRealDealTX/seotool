<?php
defined('SCC') || exit;
$groups = [
    ['essentials', 'Start here', 'book', ['pillar', 'compare'], 'The core guides every solar camera buyer should read first.'],
    ['guides', 'Power, sun & performance', 'sun', ['guides'], 'Sunlight, batteries, winter, night vision, Wi‑Fi and the questions owners ask most.'],
    ['use-cases', 'Use cases', 'map', ['use-cases'], 'Farms, rural land, RVs, cabins, campsites and job sites.'],
    ['how-to', 'Setup & troubleshooting', 'tool', ['how-to', 'troubleshooting'], 'Mount without drilling, reset, and fix a camera that stops charging.'],
    ['reviews', 'Buying guides', 'star', ['reviews'], 'Category buying guides with honest, research-based picks.'],
];
$all = articles();
$list = [];
page_head([
    'title' => 'Solar Camera Guides: Every Solar Security Camera Guide',
    'description' => 'All Solar CCTV Camera guides in one place: solar panel angle, battery life, winter and night performance, Wi‑Fi vs 4G, installation and use cases.',
    'path' => '/solar-camera-guides/',
    'schema' => [
        breadcrumb_schema([['Home', '/'], ['Guides', '/solar-camera-guides/']]),
        ['@type' => 'CollectionPage', 'name' => 'Solar Camera Guides', 'url' => abs_url('/solar-camera-guides/'), 'isPartOf' => ['@id' => SITE_ORIGIN . '/#website'],
         'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_values(array_map(function ($p, $i) use ($all) { return ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($p), 'name' => $all[$p]['h1']]; }, array_keys($all), array_keys(array_keys($all))))]],
    ],
]);
?>
<section class="page-hero">
  <div class="hero-sky" aria-hidden="true"><span class="hero-sun"></span></div>
  <div class="wrap" style="position:relative">
    <?= breadcrumbs_html([['Home', '/'], ['Guides', '/solar-camera-guides/']]) ?>
    <h1>Solar camera guides</h1>
    <p class="lede">Everything we know about solar security cameras, organised by the question you are trying to answer. Each guide is research-based, kept up to date, and linked to a calculator where numbers matter.</p>
    <div class="filter-bar">
<?php foreach ($groups as [$id, $name]): ?>
      <a href="#<?= $id ?>"><?= e($name) ?></a>
<?php endforeach; ?>
      <a href="/tools/">Calculators</a>
    </div>
  </div>
</section>
<div class="wrap">
<?php foreach ($groups as [$id, $name, $ic, $secs, $blurb]):
    $items = array_filter($all, fn($a) => in_array($a['section'], $secs, true));
    if (!$items) continue; ?>
  <section class="hub-section" id="<?= $id ?>">
    <h2><?= icon($ic, 26) ?> <?= e($name) ?></h2>
    <p class="muted"><?= e($blurb) ?></p>
    <div class="card-grid">
<?php foreach ($items as $a) echo article_card($a); ?>
    </div>
  </section>
<?php endforeach; ?>
</div>
<div style="height:60px"></div>
<?php require_once ROOT . '/inc/article.php'; cta_band(); page_foot();
