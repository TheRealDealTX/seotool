<?php
$styleRoutes = array_filter($ROUTES, fn($r) => $r['type'] === 'style');
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', null]],
    'schema' => [[
        '@context' => 'https://schema.org', '@type' => 'CollectionPage', 'name' => 'Tiny House Floor Plans',
        'url' => abs_url('/tiny-house-plans/'),
        'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_values(array_map(
            fn($slug, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url("/plans/$slug/")],
            array_keys($PLANS), array_keys(array_keys($PLANS))))],
    ]],
]);
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Tiny house plans</p>
    <h1>Tiny House Floor Plans</h1>
    <p class="lead">Browse build-ready tiny house floor plans from Tiny Homes Blueprint. Every plan lists its square footage, footprint, roof and wall framing, and ships as PDF, CAD and image files so your builder can price it and your permit office can review it.</p>
    <ul class="hero-facts"><li>PDF + CAD + image files</li><li>Modifications available</li><li>Order online or by phone: <?= SITE_PHONE ?></li></ul>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <form class="filters" data-target="#catalog-grid" data-empty="#catalog-empty" aria-label="Filter plans">
      <label>Style
        <select name="style">
          <option value="">All styles</option>
          <?php foreach ($styleRoutes as $p => $r): ?><option value="<?= e(trim($p, '/')) ?>"><?= e($r['nav']) ?></option><?php endforeach; ?>
        </select>
      </label>
      <label>Bedrooms
        <select name="beds"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option></select>
      </label>
      <label>Floors
        <select name="floors"><option value="">Any</option><option value="1">1 floor</option><option value="2">2 floors</option></select>
      </label>
      <label>Sort
        <select name="sort"><option value="">Featured</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option><option value="sqft-asc">Size: small to large</option></select>
      </label>
      <span class="filter-count" aria-live="polite"></span>
    </form>
    <div id="catalog-grid"><?php plan_grid(); ?></div>
    <div id="catalog-empty" class="callout wood" hidden><strong>No ready-made plan matches those filters yet.</strong><p>Tiny Homes Blueprint can modify an existing plan or draw a custom one. <a href="/contact/">Tell us what you need</a> or call <?= SITE_PHONE ?>.</p></div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>Browse tiny house plans by style</h2><p class="lead">Each style guide covers sizes, costs, layout ideas and the plans that fit that style.</p></div>
    <?php route_cards('style'); ?>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose">
      <h2>How to choose a tiny house floor plan</h2>
      <p>The right tiny house floor plan starts with how you will use the house, not with the prettiest rendering. Work through these five questions before you buy any plan, from Tiny Homes Blueprint or anyone else.</p>
      <h3>1. Wheels or foundation?</h3>
      <p>A <a href="/tiny-house-on-wheels-plans/">tiny house on wheels</a> is limited to about 8.5 ft wide and 13.5 ft tall for road travel, which usually means 150 to 300 sq ft and a sleeping loft. A foundation home can be any width your lot and zoning allow, so 400 to 800 sq ft with a main-floor bedroom becomes realistic. Our <a href="/blog/tiny-house-zoning-laws/">zoning guide</a> explains how each is treated legally.</p>
      <h3>2. How many people, and how often?</h3>
      <p>A weekend cabin for two can live happily in 300 sq ft. A family living full-time needs real bedrooms, a laundry spot and storage. The <a href="/tools/how-big-should-my-tiny-house-be/">tiny house size calculator</a> turns your household into a square-footage range.</p>
      <h3>3. Loft or single level?</h3>
      <p>Lofts double sleeping space without adding footprint, but they mean ladders or stairs and limited headroom. If knees, kids or aging in place matter, choose a single-level plan like <a href="/plans/plan-12-2417/">Plan 12-2417</a>. See <a href="/tiny-house-plans-with-loft/">tiny house plans with a loft</a> for the trade-offs.</p>
      <h3>4. Where does the plumbing go?</h3>
      <p>Good tiny house floor plans stack the kitchen, bathroom and laundry along one "wet wall." It shortens pipe runs, cuts cost and makes winterizing easier.</p>
      <h3>5. What will it cost to build?</h3>
      <p>Plans are typically around 1% of a tiny house budget; materials and labor are the rest. Run the plan's square footage through the <a href="/tools/tiny-house-cost-calculator/">cost calculator</a> before you commit.</p>
      <h2>What is in a Tiny Homes Blueprint plan set</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Sheet or file</th><th>What it shows</th></tr></thead>
        <tbody>
          <tr><td>Floor plan</td><td>Room dimensions, walls, doors, windows, fixtures</td></tr>
          <tr><td>Exterior elevations</td><td>All four sides, finishes, overall height</td></tr>
          <tr><td>Roof &amp; framing notes</td><td>Roof pitch, truss framing, 2x6 exterior walls</td></tr>
          <tr><td>PDF</td><td>Print-ready drawings for builders and permit review</td></tr>
          <tr><td>CAD</td><td>Editable source drawings for local changes</td></tr>
          <tr><td>Images</td><td>Renderings for planning, lenders and HOA approval</td></tr>
        </tbody>
      </table></div>
      <p>Your local building department may require a stamped structural or energy review for your site. The CAD file makes that review faster and cheaper for a local engineer.</p>
      <?php faq_block([
          ['What size are your tiny house floor plans?', '<p>Our current plans are 700 sq ft on a 20 x 38 ft footprint, in single-level 2-bedroom and two-story 3-bedroom versions. Tiny Homes Blueprint can modify either plan to a smaller footprint on request.</p>'],
          ['Can you change a tiny house plan for me?', '<p>Yes. Common requests include flipping the layout, moving the porch, adding a loft, changing the foundation type or shrinking the footprint. <a href="/contact/">Send us the plan number and your changes</a> for a quote.</p>'],
          ['Are the plans permit-ready?', '<p>The plans include the drawings building departments usually ask for. Because codes, snow and wind loads, and energy rules vary by location, your jurisdiction may require a local engineer or designer to review or stamp them.</p>'],
          ['How are plans delivered?', '<p>After your order is confirmed, the PDF, CAD and image files are delivered digitally by email.</p>'],
          ['Do you offer free tiny house plans?', '<p>We focus on complete plan sets, but our <a href="/blog/free-tiny-house-plans/">guide to free tiny house plans</a> explains what free plans include and when they are good enough.</p>'],
      ]); ?>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Order by phone</h3><p>Questions about a plan? Talk to Tiny Homes Blueprint directly.</p><a class="btn btn-light btn-sm" href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> <?= SITE_PHONE ?></a></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-cost-calculator/">Tiny house cost calculator</a></li>
        <li><a href="/tools/tiny-house-layout-planner/">Layout planner</a></li>
        <li><a href="/tools/tiny-house-style-quiz/">Tiny house style quiz</a></li>
      </ul></div>
    </aside>
  </div>
</section>
<?php cta_band('Don\'t see the right plan?', 'Tiny Homes Blueprint modifies existing plans and designs custom tiny homes. Tell us your lot, budget and must-haves.', 'Request a custom plan', '/contact/'); ?>
<?php page_end(); ?>
