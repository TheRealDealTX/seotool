<?php
$path = '/tools/';
$crumbs = [['Home', '/'], ['Design Tools', $path]];
$items = [];
$i = 1;
foreach (TOOLS as $s => $t) {
    $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => url('/tools/' . $s . '/'), 'name' => $t['name']];
}
page_head([
    'title' => 'Free Interior Design Tools & Calculators',
    'description' => 'Free interior design tools from Luxury Apartment Design: style quiz, color palette generator, rug size, art hanging, paint, lighting and curtain calculators.',
    'path' => $path,
    'schema' => [
        ['@type' => 'CollectionPage', '@id' => url($path), 'name' => 'Free Interior Design Tools', 'isPartOf' => ['@id' => url('/#website')]],
        ['@type' => 'ItemList', 'itemListElement' => $items],
        schema_breadcrumbs($crumbs),
    ],
]);
?>
<section class="page-hero">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow">Free · No sign-up · Works on your phone</p>
    <h1>Free Interior Design Tools &amp; Calculators</h1>
    <p class="page-hero__lead">Designers rely on a handful of measurements and rules of thumb. These tools do the math for you, so you can buy the right rug, hang art at the right height and order the right amount of paint the first time.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3 tools-grid">
      <?php foreach (array_keys(TOOLS) as $t) echo tool_card($t); ?>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container container--narrow prose">
    <h2>How to use these tools together</h2>
    <p>Start with the <a href="/tools/interior-design-style-quiz/">Interior Design Style Quiz</a> to name the look you are drawn to, then build a color scheme in the <a href="/tools/room-color-palette-generator/">Room Color Palette Generator</a>. Sketch your furniture in the <a href="/tools/room-layout-planner/">Room Layout Planner</a> before you buy anything, and use the <a href="/tools/rug-size-calculator/">Rug Size Calculator</a> and <a href="/tools/curtain-size-calculator/">Curtain Size Calculator</a> to size the two items people most often get wrong.</p>
    <p>When it is time to shop, the <a href="/tools/decorating-budget-planner/">Decorating Budget Planner</a> splits your budget the way designers do, and the <a href="/tools/paint-calculator/">Paint Calculator</a>, <a href="/tools/room-lighting-calculator/">Room Lighting Calculator</a> and <a href="/tools/art-hanging-calculator/">Art Hanging Calculator</a> cover the finishing details. For the thinking behind it all, read our guide to <a href="/luxury-apartment-interior-design/">luxury apartment interior design</a>.</p>
  </div>
</section>
<?= newsletter_block() ?>
<?php page_foot(); ?>
