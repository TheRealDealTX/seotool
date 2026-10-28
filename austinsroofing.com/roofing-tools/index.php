<?php
require dirname(__DIR__) . '/includes/layout.php';
$crumbs = [['Roofing Tools', '/roofing-tools/']];
page_start([
    'title' => 'Free Roofing Calculators & Tools | Austin Roofing',
    'description' => 'Free roofing calculators: roof replacement cost, roofing squares and shingle bundles, roof pitch, roof lifespan, hail damage checker and a repair-or-replace quiz.',
    'path' => '/roofing-tools/', 'crumbs' => $crumbs, 'body_class' => 'page-tools',
]);
page_hero('Free Roofing Calculators & Tools', [
    'crumbs' => $crumbs, 'eyebrow' => 'Built by Austin roofers', 'cta' => false,
    'lead' => 'Estimate a new roof’s cost, measure squares and bundles, find your roof pitch, check hail damage and see how much life your roof has left — free, instant and private.',
]);
?>
<section class="section section--tight">
  <div class="container">
    <?php tool_cards(); ?>
  </div>
</section>
<section class="section section--cream">
  <div class="container tools-teaser">
    <div class="prose">
      <h2>Try It: Roof Replacement Cost Calculator</h2>
      <p>Slide in your home size, choose a pitch and material, and see a planning range for an Austin-area roof in seconds. Every tool on this page runs in your browser — nothing you type is sent anywhere.</p>
      <p>When you are ready for real numbers, Austin Roofing will measure your roof and give you an exact, free written quote.</p>
      <a class="btn btn--red" href="/contact-us/">Get an exact free quote</a>
    </div>
    <?php tool('cost'); ?>
  </div>
</section>
<?php cta_band(); page_end();
