<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$crumbs = [['Home', '/'], ['Roof Tools', '/roofing-tools/']];
page_start([
    'title'       => 'Free Roofing Calculators & Tools | Bastrop Roofing',
    'description' => 'Free roofing tools from Bastrop Roofing: roof cost calculator, metal vs. shingle calculator, pitch and area calculator, repair-or-replace quiz and storm checklist.',
    'path'        => '/roofing-tools/',
    'schema'      => [breadcrumb_schema($crumbs)],
]);
page_hero('Free interactive tools', 'Free Roofing Calculators & Tools', 'Plan your project before anyone climbs a ladder. Estimate costs, compare materials, measure your roof and check for storm damage — all free.', $crumbs);
?>
<section class="section">
  <div class="container">
    <div class="tool-grid tool-grid-lg"><?php tool_cards(); ?></div>
  </div>
</section>
<section class="section section-tint">
  <div class="container">
    <div class="section-head center reveal"><span class="eyebrow">Try it now</span><h2 class="section-title small">Bastrop Roof Replacement Cost Calculator</h2></div>
    <?php include dirname(__DIR__) . '/includes/tools/roof-replacement-cost-calculator.php'; ?>
  </div>
</section>
<section class="section">
  <div class="container narrow prose">
    <h2>Built for Bastrop Roofs</h2>
    <p>These tools use planning numbers typical for Central Texas: installed costs for shingle and metal roofing, common pitches on Bastrop homes, and the storm signs we see most after hail and wind in Bastrop County. They are a starting point. For an exact measurement and price, a <a href="/">Bastrop roofer</a> from our team will inspect your roof for free.</p>
  </div>
</section>
<?php cta_band(); page_end();
