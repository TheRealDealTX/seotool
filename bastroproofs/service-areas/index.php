<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$crumbs = [['Home', '/'], ['Service Areas', '/service-areas/']];
page_start([
    'title'       => 'Roofing Service Areas | Bastrop County Roofers | Bastrop Roofing',
    'description' => 'Bastrop Roofing serves Bastrop, Elgin, Smithville, Cedar Creek, Paige, McDade and Red Rock, TX with roof repair, replacement, metal roofing and storm repair.',
    'path'        => '/service-areas/',
    'schema'      => [breadcrumb_schema($crumbs)],
]);
page_hero('Bastrop County coverage', 'Roofing Service Areas Across Bastrop County', 'Based in Bastrop, our crews serve every town and rural road in the county, from Elgin in the north to Smithville in the south.', $crumbs, 'LOCAL-ROOFING-IN-BASTROP-TEXAS.webp');
?>
<section class="section">
  <div class="container">
    <div class="area-grid">
      <a class="area-card area-card-main reveal" href="/">
        <span class="area-pin"><?= icon('pin') ?></span>
        <h2>Bastrop, TX 78602</h2>
        <p>Our home base. Roofing for Tahitian Village, Hunters Crossing, Pine Forest, ColoVista, Piney Ridge, downtown and every Bastrop neighborhood.</p>
        <span class="card-link">Bastrop roofing <?= icon('arrow') ?></span>
      </a>
<?php foreach ($AREAS as $slug => $a): ?>
      <a class="area-card reveal" href="/service-areas/<?= $slug ?>/">
        <span class="area-pin"><?= icon('pin') ?></span>
        <h2>Roofing <?= e($a['name']) ?>, TX</h2>
        <p><?= e($a['lead']) ?></p>
        <small><?= e($a['distance']) ?></small>
        <span class="card-link">View <?= e($a['name']) ?> roofing <?= icon('arrow') ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section-tint">
  <div class="container narrow prose">
    <h2>Don't See Your Town?</h2>
    <p>Bastrop Roofing also works in the unincorporated communities and rural areas between these towns, including Rockne, Wyldwood, Camp Swift, Rosanky and the Lake Bastrop area. If you are within Bastrop County or just across the line, <a href="/contact/">contact us</a> or call <a href="tel:+15122977580">(512) 297-7580</a> and we will let you know right away.</p>
  </div>
</section>
<?php cta_band(); page_end();
