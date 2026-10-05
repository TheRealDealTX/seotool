<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Tools', '/tools/']];
$items = array_map(fn($t) => [$t['name'], $t['path']], array_values(tools()));
$page = [
    'title' => 'Free Landscape Lighting Calculators & Planning Tools',
    'description' => 'Eight free tools from Austin Landscape Lighting: fixture calculator, cost estimator, LED savings, transformer sizing, color temperature, visualizer and more.',
    'path' => '/tools/',
    'active' => '/tools/',
    'image' => 'landscape-lighting-design-tool-1',
    'tools_js' => true,
    'schema' => [schema_webpage(['title' => 'Tools', 'description' => 'Free landscape lighting planning tools.', 'path' => '/tools/'], 'CollectionPage'), schema_breadcrumb($crumbs), schema_itemlist($items, 'Austin Landscape Lighting tools')],
];
ob_start();
echo sub_hero(['eyebrow' => 'Free tools', 'h1' => 'Landscape Lighting Calculators and Planning Tools', 'intro' => 'Plan like a designer before you call one. Austin Landscape Lighting built these tools from the rules of thumb we use on real projects. Every figure is a planning estimate; your free on-site design is exact.', 'image' => 'landscape-lighting-design-tool-1', 'image_alt' => 'Landscape lighting design tool sketch for an Austin home', 'crumbs' => $crumbs]);
?>
<section class="section">
  <div class="container">
    <div class="grid grid--4"><?php foreach (array_values(tools()) as $i => $t) echo tool_card($t, $i); ?></div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <?= section_head('Try one now', 'Lighting visualizer', 'Switch techniques on and off and watch the fixture count and planning range update.') ?>
    <div data-reveal="scale"><?= tool_markup('lighting-visualizer') ?></div>
  </div>
</section>
<?= cta_band('Turn the numbers into a design', 'Bring your tool results to a free dusk consultation. Austin Landscape Lighting turns them into a fixture-by-fixture plan and a written estimate.') ?>
<?php
render_page($page, ob_get_clean());
