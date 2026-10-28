<?php
hero([
    'eyebrow' => 'House Designs',
    'h1' => 'Tiny House Plans &amp; Designs for Texas',
    'lead' => 'Explore the home types Cowboy Tiny Homes designs — from tiny homes on wheels and park models to backyard ADUs and small single-family homes — and our featured Gonzales Modern Living plan. Every design can be customized to your land and lifestyle.',
    'image' => '3.webp',
]);

// Design categories carried over from the old site's taxonomy. Sizes are typical ranges.
$designs = [
    ['filter' => 'single dwelling', 'img' => '3.webp', 'w' => 500, 'h' => 333, 'title' => 'Gonzales Modern Living', 'tag' => 'Featured plan',
     'specs' => ['2 bed', '1.5 bath', '2 floors', 'Office'], 'text' => 'A cozy contemporary two-story small house with a mini bar kitchen, ground-floor powder room and upstairs study.',
     'href' => '/gonzales-modern-living/', 'cta' => 'View the plan'],
    ['filter' => 'single', 'img' => 'Custom-Tiny-Homes.webp', 'w' => 640, 'h' => 427, 'title' => 'Single-Family Residential', 'tag' => 'Category',
     'specs' => ['400–1,800 sq ft', 'Foundation', 'IRC code'], 'text' => 'Tiny, small and right-sized homes on a permanent foundation for full-time living, designed to IRC and local zoning.',
     'href' => '/custom-tiny-homes-texas/', 'cta' => 'Custom tiny homes'],
    ['filter' => 'dwelling', 'img' => 'Accessory-Dwelling-Units.webp', 'w' => 640, 'h' => 427, 'title' => 'Dwelling Units (ADUs)', 'tag' => 'Category',
     'specs' => ['300–1,200 sq ft', 'Backyard', 'Rental-ready'], 'text' => 'Casitas, granny flats, guest houses and mother-in-law suites with their own kitchen, bath and entry.',
     'href' => '/adu-builders-texas/', 'cta' => 'ADU builders'],
    ['filter' => 'accessory', 'img' => 'Cowboy-Tiny-Homes-Site-Image.webp', 'w' => 1200, 'h' => 675, 'title' => 'Accessory Structures', 'tag' => 'Category',
     'specs' => ['Studios', 'Pool houses', 'Offices'], 'text' => 'Backyard offices, art studios, pool houses and workshops — permanent structures that add space without a full kitchen.',
     'href' => '/adu-builders-texas/', 'cta' => 'Backyard structures'],
    ['filter' => 'park', 'img' => 'Park-Model-Homes.webp', 'w' => 640, 'h' => 427, 'title' => 'Park Models', 'tag' => 'Category',
     'specs' => ['~399 sq ft', 'Porch', 'Loft option'], 'text' => 'Cabin-style homes sized around 399 square feet for RV parks, ranches and rural land outside city limits.',
     'href' => '/park-model-homes-texas/', 'cta' => 'Park model homes'],
    ['filter' => 'thow', 'img' => 'Tiny-Homes-On-Wheels.webp', 'w' => 640, 'h' => 427, 'title' => 'Tiny House on Wheels', 'tag' => 'Category',
     'specs' => ['120–400 sq ft', 'Bumper pull', 'Gooseneck'], 'text' => 'Mobile tiny homes on bumper-pull or gooseneck trailers with lofts, full kitchens and off-grid options.',
     'href' => '/tiny-homes-on-wheels-texas/', 'cta' => 'Tiny homes on wheels'],
    ['filter' => 'misc', 'img' => 'Home-Remodel.webp', 'w' => 640, 'h' => 427, 'title' => 'Miscellaneous &amp; Remodels', 'tag' => 'Category',
     'specs' => ['Kitchens', 'Baths', 'Additions'], 'text' => 'Remodel designs, additions and one-off projects that do not fit a box — if it is small and smart, we can draw it.',
     'href' => '/home-remodel-design-texas/', 'cta' => 'Remodel design'],
];
$filters = ['all' => 'All designs', 'single' => 'Single-family', 'dwelling' => 'ADUs', 'accessory' => 'Accessory structures', 'park' => 'Park models', 'thow' => 'On wheels', 'misc' => 'Remodels &amp; misc'];
?>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Browse Designs by Type</h2>
      <p class="section-intro">Filter by the kind of home you are planning. Not sure which type fits? Take the <a href="/tools/which-tiny-home-is-right-for-me/">60-second tiny home quiz</a>.</p>
    </div>
    <div class="filter-bar" role="group" aria-label="Filter designs">
<?php foreach ($filters as $k => $label): ?>
      <button type="button" class="filter-btn<?= $k === 'all' ? ' is-active' : '' ?>" data-design-filter="<?= $k ?>"><?= $label ?></button>
<?php endforeach; ?>
    </div>
    <div class="grid-3">
<?php foreach ($designs as $d): ?>
      <article class="card service-card design-card" data-design="<?= $d['filter'] ?>">
        <img src="/assets/img/<?= $d['img'] ?>" alt="<?= strip_tags($d['title']) ?> — Cowboy Tiny Homes design" width="<?= $d['w'] ?>" height="<?= $d['h'] ?>" loading="lazy" style="aspect-ratio:3/2;object-fit:cover">
        <div class="card-body">
          <span class="card-kicker"><?= $d['tag'] ?></span>
          <h3><?= $d['title'] ?></h3>
          <div class="spec-row"><?php foreach ($d['specs'] as $s) echo '<span class="spec">' . e($s) . '</span>'; ?></div>
          <p><?= $d['text'] ?></p>
          <a class="card-more" href="<?= $d['href'] ?>"><?= $d['cta'] ?> →</a>
        </div>
      </article>
<?php endforeach; ?>
    </div>
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
      <p>Every Cowboy Tiny Homes design package includes floor plans, exterior elevations, a roof plan, site plan, electrical layout and interior, exterior and 3D renderings. Learn more about our <a href="/tiny-house-design-services/">tiny house design services</a>.</p>
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
<?php
faq_section([
    ['Can I modify one of your tiny house plans?', '<p>Yes. Every plan is a starting point. We adjust size, layout, windows, roof style and finishes to match your property, code requirements and budget.</p>'],
    ['Do your house plans meet Texas building codes?', '<p>Foundation homes and ADUs are drawn to the International Residential Code and the local amendments where you build. Tiny homes on wheels and park models follow the standards that apply to those home types. Final approval always rests with your local building official.</p>'],
    ['Can I buy plans and use my own builder?', '<p>Yes. Our <a href="/tiny-house-design-services/">design services</a> produce drawings you can hand to any qualified builder or use for an owner-builder project.</p>'],
    ['How much does a tiny house plan cost?', '<p>Design fees depend on the size and complexity of the home and how much customization you need. Featured plans like the Gonzales Modern Living start at $1,000; fully custom design is quoted after a free consultation.</p>'],
]);
cta_band('Found a Design You Love?', 'Let Cowboy Tiny Homes tailor it to your land, budget and the codes where you build. Free design consultation.');
