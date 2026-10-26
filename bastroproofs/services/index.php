<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$crumbs = [['Home', '/'], ['Services', '/services/']];
$items = [];
foreach ($SERVICES as $slug => $s) {
    $items[] = ['@type' => 'ListItem', 'position' => count($items) + 1, 'name' => $s['name'], 'url' => abs_url("/services/$slug/")];
}
page_start([
    'title'       => 'Roofing Services Bastrop TX | Repair, Metal & More | Bastrop Roofing',
    'description' => 'All roofing services from Bastrop Roofing: roof repair, replacement, metal and shingle roofing, inspections, storm, hail and commercial roofing in Bastrop, TX.',
    'path'        => '/services/',
    'schema'      => [breadcrumb_schema($crumbs), ['@type' => 'ItemList', 'name' => 'Bastrop Roofing services', 'itemListElement' => $items]],
]);
page_hero('Bastrop Roofing Services', 'Roofing Services in Bastrop, TX', 'Residential and commercial roofing for Bastrop and Bastrop County — repairs, replacements, metal roofing, inspections and storm response from one local team.', $crumbs, 'Roof-Replacement.webp');
?>
<section class="section">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">What we do</span>
      <h2 class="section-title">Every Roofing Service Under One Local Roof</h2>
      <p class="section-copy">Not sure which service you need? Start with a <a href="/services/roof-inspection-bastrop-tx/">free roof inspection</a> or take the <a href="/roofing-tools/repair-or-replace-quiz/">repair-or-replace quiz</a>.</p>
    </div>
    <div class="card-grid"><?php service_cards(); ?></div>
  </div>
</section>
<section class="section section-tint">
  <div class="container split">
    <div class="split-media reveal"><img src="<?= img('Repair-Maintenance.webp') ?>" alt="Bastrop Roofing technician repairing roof flashing" width="1200" height="655" loading="lazy"></div>
    <div class="split-copy reveal">
      <span class="eyebrow">Residential &amp; commercial</span>
      <h2 class="section-title small">One Bastrop Roofer for Homes, Shops and Businesses</h2>
      <p>Bastrop Roofing works on subdivision homes, historic houses near downtown, rural properties with barns and workshops, and commercial buildings along SH 71 and SH 21. Whatever the roof — architectural shingles, standing seam metal, R-panel or low-slope TPO — we inspect it, explain it and price it clearly.</p>
      <a class="btn btn-dark" href="/contact/">Request a Free Estimate <?= icon('arrow') ?></a>
    </div>
  </div>
</section>
<?php cta_band(); page_end();
