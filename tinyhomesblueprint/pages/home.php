<?php
$featured = ['plan-12-2418', 'plan-12-2420', 'plan-12-2423', 'plan-12-2428', 'plan-12-2429', 'plan-12-2435', 'plan-12-2437', 'plan-12-2440'];
page_start([
    'schema' => [[
        '@context' => 'https://schema.org', '@type' => 'ItemList', 'name' => 'Tiny house plans from ' . SITE_NAME,
        'itemListElement' => array_values(array_map(fn($slug, $i) => [
            '@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url("/plans/$slug/"),
        ], $featured, array_keys($featured))),
    ]],
]);
?>
<section class="hero bp">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow">Tiny Homes Blueprint &middot; Plans, tools &amp; guides</p>
      <h1>Tiny House Plans &amp; Blueprints <em>Built for Real Life</em></h1>
      <p class="lead">Tiny Homes Blueprint gives you build-ready tiny house plans with full dimensions, framing details and CAD files, plus free calculators that show what your tiny home will cost, weigh and need before you buy a single board.</p>
      <div class="hero-actions">
        <a class="btn btn-wood" href="/tiny-house-plans/">Browse tiny house plans <?= icon('arrow') ?></a>
        <a class="btn btn-ghost" href="/tools/tiny-house-cost-calculator/">Estimate my build cost</a>
      </div>
      <ul class="hero-proof">
        <li><?= icon('file') ?> PDF, CAD &amp; image files</li>
        <li><?= icon('ruler') ?> 2x6 framing details</li>
        <li><?= icon('phone') ?> Real people at <?= SITE_PHONE ?></li>
      </ul>
    </div>
    <div class="hero-art">
      <svg viewBox="0 0 440 300" role="img" aria-labelledby="fp-title">
        <title id="fp-title">Floor plan sketch of a 20 by 38 foot tiny house from Tiny Homes Blueprint</title>
        <g fill="none" stroke="#e8f2f2" stroke-width="2.5">
          <rect x="30" y="40" width="380" height="200"/>
          <path d="M150 40v120M150 190v50M270 40v80M270 150v90M330 120v120M270 120h140M30 160h70M130 160h20"/>
        </g>
        <g fill="none" stroke="#f2c58d" stroke-width="1.5" stroke-dasharray="5 4">
          <rect x="30" y="240" width="120" height="40"/>
        </g>
        <g stroke="#9fe0dc" stroke-width="1" fill="none">
          <path d="M30 20h380M30 14v12M410 14v12M430 40v200M424 40h12M424 240h12"/>
          <path d="M100 160a30 30 0 0 1 30 -30" />
          <path d="M150 160a30 30 0 0 0 30 30" />
        </g>
        <g fill="#cfe3e3" font-family="Inter, sans-serif" font-size="12" text-anchor="middle">
          <text x="220" y="15">38'-0"</text>
          <text x="436" y="144" transform="rotate(90 436 144)">20'-0"</text>
          <text x="90" y="100">LIVING</text>
          <text x="210" y="95">KITCHEN</text>
          <text x="210" y="215">FLEX / OFFICE</text>
          <text x="340" y="85">BEDROOM</text>
          <text x="300" y="185">BATH</text>
          <text x="370" y="185">BEDROOM 2</text>
          <text x="90" y="205">ENTRY</text>
          <text x="90" y="265" fill="#f2c58d">COVERED PORCH</text>
        </g>
      </svg>
      <img class="photo" src="/assets/img/tiny-home-interior.webp" width="640" height="426" alt="Bright tiny home interior with open shelving and a compact kitchen">
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><b><?= count($PLANS) ?> plans</b><span>From <?= min(array_column($PLANS, 'sqft')) ?> to <?= max(array_column($PLANS, 'sqft')) ?> sq ft in the Tiny Homes Blueprint catalog</span></div>
      <div class="stat"><b>3 file types</b><span>PDF, CAD and image files in every plan set</span></div>
      <div class="stat"><b>6 free tools</b><span>Cost, layout, size, weight, solar and style quiz</span></div>
      <div class="stat"><b>1 business day</b><span>Typical reply time on plan questions</span></div>
    </div>
  </div>
</section>

<section class="section section-alt" id="plans">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Featured tiny house plans</p>
      <h2>Tiny home blueprints you can build from</h2>
      <p class="lead">Every plan from Tiny Homes Blueprint is drawn to be permit-ready, with exterior elevations, a dimensioned floor plan, roof and wall framing notes, and the CAD file your builder or engineer needs to make local changes.</p>
    </div>
    <?php plan_grid($featured); ?>
    <p class="mt-2"><a class="btn btn-outline" href="/tiny-house-plans/">See all <?= count($PLANS) ?> tiny house floor plans <?= icon('arrow') ?></a></p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Shop by style</p>
      <h2>Find the tiny house design that fits your land and life</h2>
      <p class="lead">A tiny house on wheels solves a different problem than a backyard ADU or an A-frame cabin. Tiny Homes Blueprint breaks down each style with sizes, costs, layout ideas and the trade-offs nobody puts in the brochure.</p>
    </div>
    <?php route_cards('style'); ?>
  </div>
</section>

<section class="section bp" id="quick-estimate">
  <div class="wrap two-col">
    <div>
      <p class="eyebrow">Free tool preview</p>
      <h2>What will your tiny house cost?</h2>
      <p>Move the sliders for a quick ballpark. For a line-by-line estimate covering foundation, utilities, land prep and DIY versus builder labor, open the full Tiny Homes Blueprint cost calculator.</p>
      <p><a class="btn btn-light" href="/tools/tiny-house-cost-calculator/">Open the full cost calculator</a></p>
    </div>
    <div class="panel result-panel" id="mini-calc">
      <div class="field">
        <label for="mc-size" style="color:#fff">Size: <span class="range-out" style="color:#f2c58d" id="mc-size-out">300</span> sq ft</label>
        <input type="range" id="mc-size" min="120" max="800" step="10" value="300">
      </div>
      <div class="field">
        <span class="label" style="color:#fff">Finish level</span>
        <div class="seg" role="radiogroup" aria-label="Finish level">
          <label><input type="radio" name="mc-finish" value="0" checked><span>Basic</span></label>
          <label><input type="radio" name="mc-finish" value="1"><span>Mid-range</span></label>
          <label><input type="radio" name="mc-finish" value="2"><span>High-end</span></label>
        </div>
      </div>
      <div class="field">
        <span class="label" style="color:#fff">Who builds it?</span>
        <div class="seg" role="radiogroup" aria-label="Builder">
          <label><input type="radio" name="mc-labor" value="diy" checked><span>DIY</span></label>
          <label><input type="radio" name="mc-labor" value="pro"><span>Hire a builder</span></label>
        </div>
      </div>
      <p class="result-sub">Estimated build cost</p>
      <p class="result-big" id="mc-out" aria-live="polite">$45,000 - $66,000</p>
      <p class="result-sub">Structure and finishes only. Land, permits and utility hookups are extra.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Free planning tools</p>
      <h2>Plan smarter with Tiny Homes Blueprint calculators</h2>
      <p class="lead">Most tiny house projects stall on the same questions: how big, how heavy, how much and how to power it. These free tools answer them in minutes, with no email sign-up.</p>
    </div>
    <?php route_cards('tool'); ?>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap two-col">
    <div>
      <img class="rounded" src="/assets/img/plan-12-2418.webp" width="800" height="430" alt="Rustic tiny house with covered porch, stone base and vertical siding - Plan 12-2418" loading="lazy">
    </div>
    <div>
      <p class="eyebrow">Why Tiny Homes Blueprint</p>
      <h2>Small-home plans drawn by people who sweat the details</h2>
      <p>In a 300-square-foot house, a 6-inch mistake is the difference between a fridge that fits and one that does not. That is why Tiny Homes Blueprint plans are drawn around real fixtures, real clearances and real framing lumber, not just pretty renderings.</p>
      <ul class="check-list">
        <li><strong>Build-ready detail.</strong> Dimensioned floor plans, elevations, roof pitch and wall framing specs.</li>
        <li><strong>CAD files included.</strong> Your builder or local engineer can adapt the plan to your lot and code.</li>
        <li><strong>Flexible layouts.</strong> Flex rooms, flippable porches and loft options that grow with you.</li>
        <li><strong>Honest guidance.</strong> Our guides cover zoning, costs and trailer limits plainly, including the downsides.</li>
      </ul>
      <p><a href="/about/">More about Tiny Homes Blueprint</a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">How it works</p>
      <h2>From idea to permit set in four steps</h2>
    </div>
    <ol class="steps">
      <li><h3>Size it</h3><p>Use the <a href="/tools/how-big-should-my-tiny-house-be/">size calculator</a> and <a href="/tools/tiny-house-style-quiz/">style quiz</a> to narrow down what you need.</p></li>
      <li><h3>Budget it</h3><p>Run the <a href="/tools/tiny-house-cost-calculator/">cost calculator</a> and check your <a href="/blog/tiny-house-zoning-laws/">local zoning</a> before you commit.</p></li>
      <li><h3>Pick a plan</h3><p>Choose a Tiny Homes Blueprint plan, or ask us about changes. Order online inquiry or by phone.</p></li>
      <li><h3>Build it</h3><p>Hand your builder the PDF and CAD set, pull permits and follow our <a href="/blog/how-to-build-a-tiny-house/">step-by-step build guide</a>.</p></li>
    </ol>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap two-col top">
    <div>
      <p class="eyebrow">Inside the plan set</p>
      <h2>What comes with a Tiny Homes Blueprint plan</h2>
      <p>Free tiny house plans usually stop at a floor sketch. A complete Tiny Homes Blueprint set gives your builder, lender and permit office what they actually ask for.</p>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Included</th><th>Why it matters</th></tr></thead>
          <tbody>
            <tr><td>Dimensioned floor plan</td><td>Exact room sizes, door swings and window locations</td></tr>
            <tr><td>Exterior elevations</td><td>Siding, roof pitch and overall height for zoning review</td></tr>
            <tr><td>Roof &amp; wall framing specs</td><td>Truss roof framing and 2x6 walls for strength and insulation depth</td></tr>
            <tr><td>PDF file</td><td>Print-ready sheets for the job site and the permit counter</td></tr>
            <tr><td>CAD file</td><td>Editable drawings for local engineering or custom changes</td></tr>
            <tr><td>Image files</td><td>Renderings to share with lenders, family or your HOA</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    <div>
      <p class="eyebrow">Tiny house guides</p>
      <h2>Learn before you build</h2>
      <p>The Tiny Homes Blueprint guides answer the questions buyers ask us most, with real numbers.</p>
      <div class="card-grid" style="grid-template-columns:1fr">
      <?php foreach (['/blog/how-much-does-a-tiny-house-cost/', '/blog/tiny-house-zoning-laws/', '/blog/how-to-build-a-tiny-house/', '/blog/tiny-house-layout-ideas/'] as $g): ?>
        <a class="link-card" href="<?= $g ?>"><strong><?= e($ROUTES[$g]['nav']) ?></strong><span><?= e($ROUTES[$g]['description']) ?></span></a>
      <?php endforeach; ?>
      </div>
      <p class="mt-2"><a href="/blog/">All tiny house guides <?= icon('arrow') ?></a></p>
    </div>
  </div>
</section>

<section class="section">
  <div class="narrow">
    <?php faq_block([
        ['What is included in a Tiny Homes Blueprint tiny house plan?', '<p>Each Tiny Homes Blueprint plan set includes a dimensioned floor plan, exterior elevations, roof and wall framing specifications, and the drawings as PDF, CAD and image files. The CAD file lets a local designer or engineer adapt the plan to your site and building code.</p>'],
        ['How much does it cost to build a tiny house from plans?', '<p>Most owner-builders spend roughly $150 to $330 per square foot depending on finish level, and hiring a builder for the whole job typically runs $250 to $500 per square foot. A 300 sq ft tiny house therefore lands somewhere between about $45,000 and $150,000 before land and utility hookups. Try our <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a> for an estimate based on your choices.</p>'],
        ['Can I build a tiny house plan on a foundation instead of a trailer?', '<p>Yes. Foundation tiny homes are treated like any other small house and often have an easier path through zoning than a tiny house on wheels. Our <a href="/tiny-cottage-plans/">cottage</a>, <a href="/small-cabin-plans/">cabin</a> and <a href="/adu-plans/">ADU plans</a> are designed for permanent foundations.</p>'],
        ['Are tiny houses legal where I live?', '<p>It depends on your county and city. Many places now allow small homes through ADU rules or the IRC tiny house appendix, while others set minimum house sizes. Read our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a> for the questions to ask your planning office.</p>'],
        ['Can Tiny Homes Blueprint modify a plan for me?', '<p>Yes. Call ' . SITE_PHONE . ' or use the <a href="/contact/">contact form</a> with the plan number and what you want to change, such as flipping the layout, adding a loft or changing the foundation. Tiny Homes Blueprint will reply with options and pricing.</p>'],
        ['How do I order a plan?', '<p>Open any plan page and use the order form, or call ' . SITE_PHONE . '. We confirm the plan, your intended use and the file formats you need, then send a secure payment link and deliver the files by email.</p>'],
    ]); ?>
  </div>
</section>

<?php cta_band('Start your tiny home with Tiny Homes Blueprint', 'Pick a plan, ask about changes or tell us about your lot. Tiny Homes Blueprint answers every message within one business day.'); ?>

<script>
(function () {
  var size = document.getElementById('mc-size'), out = document.getElementById('mc-out'), so = document.getElementById('mc-size-out');
  if (!size) return;
  // $/sq ft ranges by finish level: [DIY low, DIY high, builder low, builder high]
  var rates = [[150, 220, 250, 330], [190, 260, 300, 400], [240, 330, 380, 500]];
  function calc() {
    var f = +document.querySelector('input[name=mc-finish]:checked').value;
    var pro = document.querySelector('input[name=mc-labor]:checked').value === 'pro';
    var s = +size.value, r = rates[f], lo = s * r[pro ? 2 : 0], hi = s * r[pro ? 3 : 1];
    var round = function (n) { return Math.round(n / 1000) * 1000; };
    so.textContent = s;
    out.textContent = THB.usd(round(lo)) + ' - ' + THB.usd(round(hi));
  }
  document.getElementById('mini-calc').addEventListener('input', calc);
  window.addEventListener('DOMContentLoaded', calc);
})();
</script>
<?php page_end(); ?>
