<?php
// House plan catalog: every plan in inc/plans.php with a category filter, plus the home
// types Cowboy Tiny Homes designs and builds. /home-designs/#adu (etc.) opens a filter.
global $PLANS;
hero([
    'eyebrow' => 'Texas House Plans',
    'h1' => 'Tiny House Plans &amp; Designs for Texas',
    'lead' => 'Buy a complete plan set for a small Texas home, ADU, casita, park model, tiny home on wheels or backyard studio — drawn for Texas heat, clay soils and codes, with a 3D model and a cost estimate for your part of the state. Or have Cowboy Tiny Homes build it.',
    'image' => '3.webp',
]);
$GLOBALS['schema'][] = [
    '@type' => 'ItemList', '@id' => abs_url('/home-designs/') . '#plans', 'name' => 'Cowboy Tiny Homes Texas house plans',
    'itemListElement' => array_map(fn($slug, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($PLANS[$slug]['url']), 'name' => $PLANS[$slug]['name']],
        array_keys($PLANS), array_keys(array_keys($PLANS))),
];
$prices = array_column($PLANS, 'price');
// Home types Cowboy Tiny Homes designs and builds (the old site's design categories).
$designs = [
    ['img' => 'Custom-Tiny-Homes.webp', 'title' => 'Single-Family Residential', 'specs' => ['400–1,800 sq ft', 'Foundation', 'IRC code'],
     'text' => 'Tiny, small and right-sized homes on a permanent foundation for full-time living, designed to IRC and local zoning.', 'href' => '/custom-tiny-homes-texas/', 'cta' => 'Custom tiny homes'],
    ['img' => 'Accessory-Dwelling-Units.webp', 'title' => 'Dwelling Units (ADUs)', 'specs' => ['300–1,200 sq ft', 'Backyard', 'Rental-ready'],
     'text' => 'Casitas, granny flats, guest houses and mother-in-law suites with their own kitchen, bath and entry.', 'href' => '/adu-builders-texas/', 'cta' => 'ADU builders'],
    ['img' => 'Park-Model-Homes.webp', 'title' => 'Park Models', 'specs' => ['~399 sq ft', 'Porch', 'Loft option'],
     'text' => 'Cabin-style homes sized around 399 square feet for RV parks, ranches and rural land outside city limits.', 'href' => '/park-model-homes-texas/', 'cta' => 'Park model homes'],
    ['img' => 'Tiny-Homes-On-Wheels.webp', 'title' => 'Tiny House on Wheels', 'specs' => ['120–400 sq ft', 'Bumper pull', 'Gooseneck'],
     'text' => 'Mobile tiny homes on bumper-pull or gooseneck trailers with lofts, full kitchens and off-grid options.', 'href' => '/tiny-homes-on-wheels-texas/', 'cta' => 'Tiny homes on wheels'],
    ['img' => 'Cowboy-Tiny-Homes-Site-Image.webp', 'title' => 'Accessory Structures', 'specs' => ['Studios', 'Pool houses', 'Offices'],
     'text' => 'Backyard offices, art studios, pool houses and workshops — permanent structures that add space without a full kitchen.', 'href' => '/adu-builders-texas/', 'cta' => 'Backyard structures'],
    ['img' => 'Home-Remodel.webp', 'title' => 'Miscellaneous &amp; Remodels', 'specs' => ['Kitchens', 'Baths', 'Additions'],
     'text' => 'Remodel designs, additions and one-off projects that do not fit a box — if it is small and smart, we can draw it.', 'href' => '/home-remodel-design-texas/', 'cta' => 'Remodel design'],
];
?>
<section class="section" id="plans">
  <div class="wrap">
    <div class="section-head">
      <h2>Browse <?= count($PLANS) ?> Texas House Plans</h2>
      <p class="section-intro">Every plan comes as a complete set: a 24 x 36 construction drawing set with Texas code and climate notes, CAD file, electrical and plumbing plans, materials list, cost estimate and 3D model, from <?= money(min($prices)) ?> to <?= money(max($prices)) ?>. Not sure which type fits? Take the <a href="/tools/which-tiny-home-is-right-for-me/">60-second tiny home quiz</a>.</p>
    </div>
    <div class="filter-bar" role="group" aria-label="Filter plans">
      <button type="button" class="filter-btn is-active" data-design-filter="all">All plans</button>
<?php foreach (PLAN_CATEGORIES as $k => $label): ?>
      <button type="button" class="filter-btn" data-design-filter="<?= $k ?>"><?= e($label) ?> (<?= count(array_filter($PLANS, fn($p) => $p['category'] === $k)) ?>)</button>
<?php endforeach; ?>
    </div>
    <?php plan_grid(array_keys($PLANS)); ?>
  </div>
</section>

<section class="section section--ink build-band">
  <div class="wrap grid-2">
    <div>
      <p class="eyebrow">Buy the plan, or have us build it</p>
      <h2>Plans from a Texas builder</h2>
      <p>These plans come from the team that builds them. Buy a set and use your own builder, or hire Cowboy Tiny Homes to adapt it to your lot and build it. <?= e(PLAN_CREDIT) ?></p>
      <div class="btn-row"><a class="btn btn--gold" href="/contact-us/">Get a Free Build Quote</a><a class="btn btn--ghost" href="<?= PHONE_HREF ?>">Call <?= PHONE ?></a></div>
    </div>
    <ul class="texas-notes texas-notes--dark">
      <li><strong>Cooling-first</strong><span>Radiant-barrier roofs, low-SHGC windows, deep porches, ceiling fans and right-sized heat pumps.</span></li>
      <li><strong>Clay-soil slabs</strong><span>Stiffened slabs with grade beams, finalized from your geotechnical report.</span></li>
      <li><strong>Texas codes</strong><span>IRC notes for cities, ANSI A119.5 for park models and TxDMV limits for tiny homes on wheels.</span></li>
      <li><strong>Regional costs</strong><span>Estimates for San Antonio, Austin, Dallas, Fort Worth, Houston and rural Texas.</span></li>
    </ul>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap content-grid">
    <article class="prose">
      <h2>How Our Tiny House Plans Work</h2>
      <p>A good tiny house plan is more than a pretty floor plan. It has to fit your lot, satisfy the code that governs your home type, survive Texas heat and storms, and make every square foot earn its keep. That is why Cowboy Tiny Homes treats each plan as a starting point rather than a finished product. We take a design you like, then adjust the footprint, room sizes, window placement, roof and finishes to match your land, budget and the way you live.</p>
      <h3>Choosing a starting size</h3>
      <p>Most people underestimate how much storage and circulation a home needs, and overestimate how much room furniture really takes. As a rough guide:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Size</th><th>Typical layout</th><th>Best fit</th></tr></thead>
        <tbody>
          <tr><td>150–300 sq ft</td><td>Studio or one sleeping loft, compact kitchen, full bath</td><td>Tiny home on wheels, weekend cabin, backyard office</td></tr>
          <tr><td>300–400 sq ft</td><td>One bedroom or loft, full kitchen, living area, porch</td><td>Park model, studio ADU, IRC Appendix Q tiny house</td></tr>
          <tr><td>400–800 sq ft</td><td>One or two bedrooms, full kitchen, laundry</td><td>ADU / casita, rental unit, downsizers</td></tr>
          <tr><td>800–1,500 sq ft</td><td>Two or three bedrooms, office, two baths</td><td>Small single-family home, small families</td></tr>
        </tbody>
      </table></div>
      <p>Try the <a href="/tools/tiny-house-size-planner/">tiny house size planner</a> to add the rooms you want and see the square footage you will actually need.</p>
      <h3>Customizing a design</h3>
      <ul class="checklist">
        <li>Flip or stretch the floor plan to fit your lot and views</li>
        <li>Swap a sleeping loft for a main-floor bedroom (great for aging in place)</li>
        <li>Choose a Texas style: modern farmhouse, Hill Country stone and metal, ranch or contemporary</li>
        <li>Add porches, shade and deep overhangs for summer comfort</li>
        <li>Plan for off-grid power, rainwater or a septic system on rural land</li>
      </ul>
      <p>Every catalog plan includes the full construction drawing set, a CAD file, electrical and plumbing plans, a materials list, a Texas cost estimate and a 3D model. Custom design packages add a site plan and interior renderings. Learn more about our <a href="/tiny-house-design-services/">tiny house design services</a>.</p>
      <h3>Planning documents, reviewed for your site</h3>
      <p>Our plan sets are planning and permit-development drawings. Texas cities review homes under the IRC with their own amendments, many counties have no residential code, park models are certified to ANSI A119.5 and tiny homes on wheels follow TxDMV trailer rules. Whatever you build, have the set reviewed — and sealed where your city, lender or insurer requires — by a Texas-licensed engineer or architect. Read the <a href="/guides/tiny-house-laws-texas/">Texas tiny house laws guide</a> before you buy land.</p>
    </article>
    <aside class="sidebar">
      <div class="side-box side-box--cta">
        <h3>Want a Custom Plan?</h3>
        <p>Tell us your must-haves and we will sketch a layout that fits your land.</p>
        <a class="btn btn--gold" href="/contact-us/">Start My Design</a>
      </div>
      <div class="side-box">
        <h3>Plan &amp; Price It</h3>
        <ul>
          <li><a href="/tools/tiny-home-cost-calculator/">Tiny home cost calculator</a></li>
          <li><a href="/tools/tiny-house-size-planner/">Tiny house size planner</a></li>
          <li><a href="/guides/adu-vs-park-model-vs-tiny-house-on-wheels/">ADU vs park model vs THOW</a></li>
        </ul>
      </div>
    </aside>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Home Types We Design &amp; Build</h2>
      <p class="section-intro">Every plan above can be customized, and we design one-off homes and remodels too.</p></div>
    <div class="grid-3">
<?php foreach ($designs as $d): ?>
      <article class="card service-card design-card">
        <img src="/assets/img/<?= $d['img'] ?>" alt="<?= strip_tags($d['title']) ?> — Cowboy Tiny Homes design" width="640" height="427" loading="lazy" style="aspect-ratio:3/2;object-fit:cover">
        <div class="card-body">
          <h3><?= $d['title'] ?></h3>
          <div class="spec-row"><?php foreach ($d['specs'] as $sp) echo '<span class="spec">' . e($sp) . '</span>'; ?></div>
          <p><?= $d['text'] ?></p>
          <a class="card-more" href="<?= $d['href'] ?>"><?= $d['cta'] ?> →</a>
        </div>
      </article>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php
faq_section([
    ['How much does a house plan cost?', '<p>Catalog plans run from ' . money(min($prices)) . ' for a backyard studio to ' . money(max($prices)) . ' for a 1,728 sq ft barndominium-style home. Each price buys the complete plan set and a license to build one home. Fully custom design is quoted after a free consultation.</p>'],
    ['What is in a plan set?', '<p>A 24 x 36 in. construction drawing set (cover with Texas code and load notes, floor plans, elevations, section, slab or trailer plan, roof framing, electrical with panel schedule, plumbing with fixture schedule, materials list and cost estimate), a DXF CAD file, CSV materials and cost spreadsheets, a 3D model and PNG images, delivered as an instant download.</p>'],
    ['Will you build the plan for me?', '<p>Yes — that is what we do. ' . e(PLAN_CREDIT) . ' <a href="/contact-us/">Ask for a build quote</a>.</p>'],
    ['Do your house plans meet Texas building codes?', '<p>Foundation homes and ADUs are drawn to the 2021 International Residential Code, which Texas cities adopt with their own amendments; many county areas have no residential code. Park models are RVs built to ANSI A119.5, and tiny homes on wheels follow TxDMV trailer rules. The plans are planning documents: final approval rests with your building official, and many jurisdictions require a Texas-licensed engineer\'s or architect\'s seal. See the <a href="/guides/tiny-house-laws-texas/">Texas tiny house laws guide</a>.</p>'],
    ['Do the plans work on the Gulf Coast?', '<p>With an engineer\'s upgrade. The plans assume 115 mph inland design wind. Houston and coastal sites need higher-wind engineering, protected or impact-rated windows and, inside the TDI catastrophe area, Texas Department of Insurance windstorm certification.</p>'],
    ['Can I modify one of your plans?', '<p>Yes. Every plan is a starting point. We adjust size, layout, windows, roof style and finishes to match your property, code requirements and budget.</p>'],
    ['Can I buy plans and use my own builder?', '<p>Yes. The plan set is made to hand to any qualified Texas builder or to use for an owner-builder project, and the materials list goes straight to a lumberyard for pricing.</p>'],
    ['I lost my download link. How do I get it again?', '<p>Use <a href="/order/lookup/">Find my plan download</a> with the email address you used at checkout, and we will email fresh links.</p>'],
]);
cta_band('Found a Design You Love?', 'Let Cowboy Tiny Homes tailor it to your land, budget and the codes where you build — or build it for you. Free design consultation.');
