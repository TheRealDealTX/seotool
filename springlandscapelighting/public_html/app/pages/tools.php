<?php defined('SLT') || exit;
add_schema(['@type' => 'ItemList', 'name' => 'Free landscape lighting tools', 'itemListElement' => array_values(array_map(fn($k, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url('/tools/' . $k . '/'), 'name' => TOOLS[$k]['name']], array_keys(TOOLS), range(0, count(TOOLS) - 1)))]);
page_hero(['title' => 'Free Landscape Lighting Tools', 'eyebrow' => 'Plan like a designer', 'sub' => 'Seven free calculators and interactive tools from Spring Landscape Lighting to help you plan, budget and troubleshoot outdoor lighting.', 'crumbs' => [['Home', '/'], ['Tools', null]]]);
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap">
    <div data-reveal="zoom" style="margin-bottom:40px"><?php tool_embed('lighting-visualizer', false); ?></div>
    <div class="grid-3"><?php $i = 0; foreach (TOOLS as $k => $t) { if ($k === 'lighting-visualizer') continue; echo tool_card($k, $t, $i++); } ?></div>
  </div>
</section>
<section class="sec sec--forest">
  <div class="wrap split">
    <div class="prose">
      <h2>Estimates are a starting point</h2>
      <p class="lead">Our tools use the same rules of thumb designers start with: fixture spacing, the 80% transformer rule, wire resistance and real sunset data for Spring, Texas.</p>
      <p>A real lighting plan responds to things a calculator cannot see: your home's materials, the exact shape of your trees, where you sit on the patio, and what your neighbors see. That is why Spring Landscape Lighting finishes every installation with a nighttime adjustment.</p>
      <div class="btn-row"><a class="btn btn--glow" href="/quote/">Get a professional plan</a></div>
    </div>
    <div data-reveal="right"><?php tool_embed('energy-cost-calculator', false); ?></div>
  </div>
</section>
<?php cta_band(); ?>
