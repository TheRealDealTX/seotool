<?php
$items = [];
$n = 0;
foreach ($ROUTES as $p => $r) {
    if ($r['type'] !== 'tool') continue;
    $items[] = ['@type' => 'ListItem', 'position' => ++$n, 'name' => $r['nav'], 'url' => abs_url($p)];
}
page_start([
    'breadcrumbs' => [['Home', '/'], ['Free Tools', null]],
    'styles' => ['/assets/css/tools.css'],
    'schema' => [[
        '@context' => 'https://schema.org', '@type' => 'CollectionPage',
        'name' => 'Free Tiny House Planning Tools & Calculators', 'url' => abs_url($PATH),
        'description' => $ROUTE['description'],
        'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $items],
    ]],
]);
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Free planning tools</p>
    <h1>Free Tiny House Planning Tools &amp; Calculators</h1>
    <p class="lead">Six free tools from Tiny Homes Blueprint that answer the big questions before you buy a plan, a trailer or a single stud: what it will cost, how big it should be, how the layout fits, how much it weighs, how to power it and which style suits you.</p>
    <ul class="hero-facts">
      <li>No sign-up or email</li>
      <li>Works on phone and desktop</li>
      <li>Instant results</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>All tiny house tools</h2>
      <p class="lead">Every tool gives you a result the moment you open it, then updates as you change your inputs.</p>
    </div>
    <?php route_cards('tool'); ?>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Where to start</p>
      <h2>Which tool should you use first?</h2>
      <p class="lead">The tools work best in roughly this order, because each answer feeds the next one.</p>
    </div>
    <ol class="steps">
      <li><h3>Find your style</h3><p>Not sure what kind of tiny house you want? The <a href="/tools/tiny-house-style-quiz/">style quiz</a> matches your land, budget and lifestyle to a style in eight questions.</p></li>
      <li><h3>Pick your size</h3><p>The <a href="/tools/how-big-should-my-tiny-house-be/">size calculator</a> turns your household and habits into a square footage range and footprint.</p></li>
      <li><h3>Sketch the layout</h3><p>Drag real-size furniture onto your footprint in the <a href="/tools/tiny-house-layout-planner/">layout planner</a> to check that everything fits.</p></li>
      <li><h3>Set a budget</h3><p>The <a href="/tools/tiny-house-cost-calculator/">cost calculator</a> prices your size, finishes and labor line by line.</p></li>
      <li><h3>Check weight and power</h3><p>Building on wheels? Run the <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a>. Going off-grid? Size it with the <a href="/tools/off-grid-solar-calculator/">solar calculator</a>.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="narrow prose">
    <h2>Pick a tool by the question you are asking</h2>
    <div class="table-wrap"><table class="tool-matrix">
      <thead><tr><th>Your question</th><th>Use this tool</th><th>What you get</th></tr></thead>
      <tbody>
        <tr><td>How much does a tiny house cost?</td><td><a href="/tools/tiny-house-cost-calculator/">Tiny house cost calculator</a></td><td>Low-high total, cost per sq ft and a line-item breakdown</td></tr>
        <tr><td>How big should my tiny house be?</td><td><a href="/tools/how-big-should-my-tiny-house-be/">Size calculator</a></td><td>Square footage range, zone breakdown, footprint suggestion</td></tr>
        <tr><td>Will my furniture fit?</td><td><a href="/tools/tiny-house-layout-planner/">Layout planner</a></td><td>A scaled floor plan sketch you can save as a PNG</td></tr>
        <tr><td>How much will it weigh on a trailer?</td><td><a href="/tools/tiny-house-trailer-weight-calculator/">Trailer weight calculator</a></td><td>Estimated weight, GVWR margin and tow guidance</td></tr>
        <tr><td>How much solar do I need?</td><td><a href="/tools/off-grid-solar-calculator/">Off-grid solar calculator</a></td><td>Daily energy use, panels, battery bank, inverter and budget</td></tr>
        <tr><td>Which style suits me?</td><td><a href="/tools/tiny-house-style-quiz/">Style quiz</a></td><td>Your top style plus two runner-ups, with links to plans</td></tr>
      </tbody>
    </table></div>
    <p>All the tools share the same assumptions, so the numbers agree with each other. The cost calculator uses the same per-square-foot figures you will find in our <a href="/blog/how-much-does-a-tiny-house-cost/">tiny house cost guide</a>, and the size calculator compares your result with the 700 sq ft <a href="/tiny-house-plans/">tiny house plans</a> Tiny Homes Blueprint sells. They are planning tools, not quotes or engineering: once you know what you want, a complete plan set and local quotes turn the estimate into a real project.</p>

    <?php faq_block([
        ['Are these tiny house tools really free?', '<p>Yes. All six tools are free to use with no account, email or payment. They run in your browser, and the layout planner saves your sketch only on your own device.</p>'],
        ['How accurate are the tiny house calculators?', '<p>They use typical 2026 US costs, material weights and space standards, so they are good for comparing options and setting a budget. Real costs and weights vary with your region, materials and design, so confirm with local quotes and a scale ticket before you commit.</p>'],
        ['Which tool should I use first?', '<p>If you are just starting, take the <a href="/tools/tiny-house-style-quiz/">style quiz</a>, then use the <a href="/tools/how-big-should-my-tiny-house-be/">size calculator</a>. With a style and size in hand, the cost calculator and layout planner give you much more useful results.</p>'],
        ['Can you turn my results into a plan?', '<p>Yes. Share your size, layout sketch and budget through the <a href="/contact/">contact page</a>, and Tiny Homes Blueprint can suggest one of our plans, quote a modification or discuss a custom design.</p>'],
    ]); ?>
  </div>
</section>

<?php cta_band('Ready to turn numbers into a plan?', 'Browse build-ready tiny house plans, or call us to talk through your results.'); ?>
<?php page_end(); ?>
