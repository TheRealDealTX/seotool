<?php
$title = 'Texas Insurance Appraiser Service Areas | 288 Cities Served';
$desc  = 'Find a local insurance appraiser in your Texas city. TX Insurance Appraiser serves 288 cities, from Houston and Dallas to El Paso and the RGV.';
$C = cities();
$byRegion = [];
foreach ($C as $c) {
    $byRegion[$c['region']][] = $c;
}
$order = ['Houston & Upper Gulf Coast', 'Dallas–Fort Worth Metroplex', 'Central Texas', 'San Antonio & Hill Country', 'Coastal Bend & South Texas', 'Rio Grande Valley', 'Golden Triangle (Southeast Texas)', 'East Texas', 'North Texas & Red River', 'West Texas & Permian Basin', 'Panhandle & South Plains', 'El Paso & Far West Texas'];
$featured = ['houston', 'dallas', 'austin', 'san-antonio', 'fort-worth', 'el-paso', 'arlington', 'corpus-christi'];
ob_start(); ?>
<section class="hero hero-sm">
  <div class="hero-bg" style="background-image:url(/assets/img/site/Texas-Map.webp)"></div>
  <div class="orb orb-1"></div>
  <div class="wrap hero-in">
    <div>
      <span class="eyebrow anim">Service areas</span>
      <h1 class="anim">Insurance Appraisers Serving All of Texas</h1>
      <p class="lead anim">From hubs in Austin, Waco, Dallas and Houston, TX Insurance Appraiser covers <?= count($C) ?> Texas cities across 12 regions. Find your local insurance appraiser below.</p>
      <div class="search-box anim" style="margin:24px 0 0;max-width:520px">
        <?= icon('search', 20) ?><input type="search" placeholder="Search your city (e.g. Katy, Plano, Lubbock)…" aria-label="Search cities" data-cityfilter>
      </div>
    </div>
  </div>
</section>
<section class="section-sm">
  <div class="wrap">
    <div class="featured-cities">
      <?php foreach ($featured as $i => $s): $c = $C[$s]; ?>
      <a class="fc reveal d<?= $i % 4 + 1 ?>" href="<?= city_url($s) ?>"><img src="<?= city_image($c) ?>" alt="<?= e($c['name']) ?>, Texas" width="800" height="420" loading="lazy"><span><small><?= e($c['county']) ?> County</small><?= e($c['name']) ?> Insurance Appraiser</span></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section" style="padding-top:20px">
  <div class="wrap">
    <?php foreach ($order as $r): if (empty($byRegion[$r])) continue;
        $list = $byRegion[$r]; usort($list, fn($a, $b) => strcmp($a['name'], $b['name'])); ?>
    <div class="region reveal">
      <h2><?= icon('map', 26) ?> <?= e($r) ?> <small><?= count($list) ?> cities</small></h2>
      <ul class="city-grid">
        <?php foreach ($list as $c): ?><li><a href="<?= city_url($c['slug']) ?>"><?= icon('pin', 16) ?> <?= e($c['name']) ?></a></li><?php endforeach; ?>
      </ul>
    </div>
    <?php endforeach; ?>
    <p class="center" style="color:var(--ink-2)">Don’t see your city? We serve all of Texas — <a href="/contact-us/">contact us</a> and we’ll confirm coverage.</p>
  </div>
</section>
<?= cta_band('Need an insurance appraiser near you?', 'Call or send your carrier estimate — TX Insurance Appraiser reviews claims anywhere in Texas at no cost.') ?>
<?php
$content = (string) ob_get_clean();
$items = [];
$i = 0;
foreach ($C as $c) {
    $items[] = ['@type' => 'ListItem', 'position' => ++$i, 'name' => $c['name'] . ' Insurance Appraiser', 'url' => abs_url(city_url($c['slug']))];
}
render_page([
    'title' => $title, 'description' => $desc, 'path' => '/areas/',
    'crumbs' => [['Home', '/'], ['Areas', '/areas/']],
    'schema' => [schema_webpage('CollectionPage', $title, $desc, '/areas/'), ['@type' => 'ItemList', 'itemListElement' => $items]],
], $content);
