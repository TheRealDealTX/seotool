<?php
defined('ERE') or exit;
$crumbs = [['Home', '/'], ['Free Tools', '/tools/']];
$groups = [];
foreach (tools() as $slug => $t) $groups[$t['group']][] = $slug;
page_head([
    'title' => 'Free Real Estate Calculators & Tools for Texas | Exit Real Estate 540',
    'description' => '12 free real estate calculators: Texas mortgage, affordability, closing costs, property tax, rent vs buy, rental ROI, refinance, seller net and insurance claim depreciation.',
    'path' => '/tools/',
    'crumbs' => $crumbs,
    'schema' => [[
        '@type' => 'CollectionPage', 'url' => abs_url('/tools/'), 'name' => 'Free Real Estate Calculators',
        'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_map(fn($t, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($t['url']), 'name' => $t['name']], array_values(tools()), array_keys(array_values(tools())))],
    ]],
]);
?>
<section class="page-head">
  <div class="wrap">
    <?php breadcrumbs($crumbs); ?>
    <h1>Free Real Estate Calculators</h1>
    <p class="lead">Run the numbers before you make a move. Every tool is free, needs no sign-up, and runs privately in your browser - nothing you type is sent to us.</p>
  </div>
</section>
<?php foreach ($groups as $g => $slugs): ?>
<section class="section section--compact">
  <div class="wrap">
    <h2 class="group-title"><?= e($g) ?></h2>
    <div class="tool-grid">
<?php foreach ($slugs as $s) echo tool_card($s); ?>
    </div>
  </div>
</section>
<?php endforeach;
page_foot();
