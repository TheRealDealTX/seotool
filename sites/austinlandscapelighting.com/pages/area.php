<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$a = area($slug);
[$body, $toc] = with_heading_ids($a['body']);
$crumbs = [['Home', '/'], ['Service Areas', '/service-areas/'], [$a['city'] . ', TX', $a['path']]];
$popular = [];
foreach ($a['popular'] ?? [] as $p) {
    if ($ps = service($p)) {
        $popular[] = [$ps['name'] . ' in ' . $a['city'], $ps['path']];
    }
}
$nearby = [];
foreach (areas() as $o) {
    if ($o['slug'] !== $slug) {
        $nearby[] = $o;
    }
}
$page = [
    'title' => $a['title'],
    'description' => $a['description'],
    'path' => $a['path'],
    'image' => $a['image'],
    'active' => '/service-areas/',
    'schema' => [
        schema_webpage(['title' => $a['title'], 'description' => $a['description'], 'path' => $a['path'], 'image' => $a['image']]),
        schema_breadcrumb($crumbs),
        ['@type' => 'Service', 'name' => 'Landscape lighting in ' . $a['city'] . ', TX', 'serviceType' => 'Landscape lighting design and installation', 'provider' => ['@id' => url('/#organization')], 'areaServed' => ['@type' => 'City', 'name' => $a['city'], 'containedInPlace' => ['@type' => 'AdministrativeArea', 'name' => $a['county']]], 'url' => url($a['path'])],
        ['@type' => 'Place', 'name' => $a['city'] . ', TX', 'geo' => ['@type' => 'GeoCoordinates', 'latitude' => $a['lat'], 'longitude' => $a['lng']]],
        schema_faq($a['faqs']),
    ],
];
ob_start();
echo sub_hero(['eyebrow' => $a['eyebrow'], 'h1' => e($a['h1']), 'intro' => e($a['intro']), 'image' => $a['image'], 'image_alt' => $a['image_alt'], 'crumbs' => $crumbs]);
?>
<section class="section">
  <div class="container layout">
    <article class="prose" data-reveal>
      <dl class="local-facts">
        <div><dt>County</dt><dd><?= e($a['county']) ?></dd></div>
        <div><dt>From central Austin</dt><dd><?= e($a['drive']) ?></dd></div>
        <div><dt>ZIP codes</dt><dd><?= e(implode(', ', $a['zips'])) ?></dd></div>
      </dl>
      <?= $body ?>
      <h2 id="neighborhoods"><?= e($a['city']) ?> neighborhoods we light</h2>
      <ul class="pill-list" style="margin-bottom:1.6em"><?php foreach ($a['neighborhoods'] as $n) echo '<li>' . e($n) . '</li>'; ?></ul>
      <p>Landmarks nearby: <?= e(implode(', ', $a['landmarks'])) ?>.</p>
      <h2 id="popular-services">Popular services in <?= e($a['city']) ?></h2>
      <div class="grid grid--3" style="margin-bottom:2em">
        <?php foreach ($a['popular'] ?? [] as $i => $p) { if ($ps = service($p)) echo service_card($ps, $i); } ?>
      </div>
      <h2 id="faq">Landscape lighting in <?= e($a['city']) ?>: FAQ</h2>
      <?= faq_list($a['faqs'], 'area-faq') ?>
    </article>
    <?= sidebar(['toc' => $toc, 'links' => $popular, 'links_title' => 'Services in ' . $a['city']]) ?>
  </div>
</section>
<section class="section section--alt section--tight">
  <div class="container">
    <?= section_head('Nearby', 'Austin Landscape Lighting also serves', '', 'left') ?>
    <div class="pill-list"><?php foreach ($nearby as $n) echo area_chip($n); ?></div>
  </div>
</section>
<?= contact_section('Serving ' . $a['city'], 'Light up your ' . $a['city'] . ' home') ?>
<?php
render_page($page, ob_get_clean());
