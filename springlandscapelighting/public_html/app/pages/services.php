<?php defined('SLT') || exit;
add_schema(['@type' => 'ItemList', 'name' => 'Landscape lighting services', 'itemListElement' => array_values(array_map(fn($k, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url('/services/' . $k . '/'), 'name' => SERVICES[$k]['name']], array_keys(SERVICES), range(0, count(SERVICES) - 1)))]);
page_hero(['title' => 'Landscape Lighting Services', 'eyebrow' => 'Spring Landscape Lighting', 'sub' => 'Design, installation, repair and upgrades for every part of your property, from the facade to the farthest oak.', 'cta' => true, 'crumbs' => [['Home', '/'], ['Services', null]]]);
?>
<section class="sec" style="padding-top:40px">
  <div class="wrap">
    <div class="grid-3"><?php $i = 0; foreach (SERVICES as $k => $s) echo service_card($k, $s, $i++); ?></div>
  </div>
</section>
<section class="sec sec--forest">
  <div class="wrap split">
    <div class="prose">
      <h2>Layered lighting, one cohesive plan</h2>
      <p class="lead">The most beautiful properties are not lit by one technique. They combine several, each doing a specific job.</p>
      <p><strong>Architectural lighting</strong> gives the home its shape after dark. <strong>Path and driveway lighting</strong> makes arrival safe and gracious. <strong>Tree and garden lighting</strong> adds height and depth. <strong>Patio and pool lighting</strong> turns outdoor rooms into evening rooms. <strong>Smart controls</strong> tie it together, and <strong>repairs and upgrades</strong> keep it performing.</p>
      <p>Spring Landscape Lighting designs these layers together, even if you install them in phases, so every addition fits the whole. See how layers combine in our <a href="/tools/lighting-visualizer/">interactive visualizer</a>.</p>
    </div>
    <div data-reveal="right"><?php tool_embed('lighting-visualizer', false); ?></div>
  </div>
</section>
<section class="sec"><div class="wrap"><?php section_head('How it works', 'Our six-step process'); process_strip(); ?></div></section>
<?php cta_band(); ?>
