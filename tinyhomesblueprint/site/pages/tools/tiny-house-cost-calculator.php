<?php
$app = [
    '@context' => 'https://schema.org', '@type' => 'WebApplication',
    'name' => 'Tiny House Cost Calculator', 'url' => abs_url($PATH),
    'description' => $ROUTE['description'],
    'applicationCategory' => 'UtilitiesApplication', 'operatingSystem' => 'Any',
    'browserRequirements' => 'Requires JavaScript',
    'offers' => ['@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'],
    'publisher' => ['@id' => SITE_URL . '/#org'],
];
page_start([
    'breadcrumbs' => [['Home', '/'], ['Free Tools', '/tools/'], [$ROUTE['nav'], null]],
    'styles' => ['/assets/css/tools.css'],
    'schema' => [$app],
]);
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Free tool</p>
    <h1>Tiny House Cost Calculator</h1>
    <p class="lead">How much does a tiny house cost? Set the size, build type, finish level and who does the work, and this calculator gives you a low-to-high budget with a line-by-line breakdown, from framing and roofing to the trailer, utilities and permits.</p>
    <ul class="hero-facts">
      <li>12+ cost line items</li>
      <li>DIY, partial or builder labor</li>
      <li>Copy or print your estimate</li>
    </ul>
  </div>
</section>

<section class="section tool-sec">
  <div class="wrap">
    <form class="tool-shell" id="cc" novalidate>
      <div class="panel">
        <h2>Describe your build</h2>
        <p class="panel-intro">Every change updates the estimate instantly.</p>

        <div class="field">
          <label for="cc-size">Floor area: <span class="range-out" id="cc-size-out">250</span> sq ft</label>
          <input type="range" id="cc-size" name="size" min="100" max="1000" step="10" value="250" aria-describedby="cc-size-hint">
          <div class="range-ends" aria-hidden="true"><span>100</span><span>1,000 sq ft</span></div>
          <small id="cc-size-hint">Heated main-floor area. Lofts are added separately below.</small>
        </div>

        <div class="field">
          <span class="label" id="cc-type-l">Build type</span>
          <div class="seg" role="radiogroup" aria-labelledby="cc-type-l">
            <label><input type="radio" name="type" value="thow" checked><span>On wheels (THOW)</span></label>
            <label><input type="radio" name="type" value="foundation"><span>On a foundation</span></label>
            <label><input type="radio" name="type" value="shell"><span>Shell only</span></label>
          </div>
        </div>

        <div class="field" id="cc-base-field">
          <span class="label" id="cc-base-l">What it sits on</span>
          <div class="seg" role="radiogroup" aria-labelledby="cc-base-l">
            <label data-base="trailer"><input type="radio" name="base" value="trailer" checked><span>Trailer</span></label>
            <label data-base="piers"><input type="radio" name="base" value="piers"><span>Piers / piles</span></label>
            <label data-base="slab"><input type="radio" name="base" value="slab"><span>Concrete slab</span></label>
          </div>
        </div>

        <div class="field">
          <span class="label" id="cc-finish-l">Finish level</span>
          <div class="seg" role="radiogroup" aria-labelledby="cc-finish-l">
            <label><input type="radio" name="finish" value="0"><span>Basic</span></label>
            <label><input type="radio" name="finish" value="1" checked><span>Mid-range</span></label>
            <label><input type="radio" name="finish" value="2"><span>High-end</span></label>
          </div>
        </div>

        <div class="field">
          <span class="label" id="cc-labor-l">Who builds it?</span>
          <div class="seg" role="radiogroup" aria-labelledby="cc-labor-l">
            <label><input type="radio" name="labor" value="diy" checked><span>DIY</span></label>
            <label><input type="radio" name="labor" value="partial"><span>DIY + hired trades</span></label>
            <label><input type="radio" name="labor" value="builder"><span>Builder</span></label>
          </div>
        </div>

        <div class="field">
          <span class="label" id="cc-util-l">Utilities</span>
          <div class="seg" role="radiogroup" aria-labelledby="cc-util-l">
            <label><input type="radio" name="util" value="grid" checked><span>Grid hookup</span></label>
            <label><input type="radio" name="util" value="solar"><span>Off-grid solar</span></label>
            <label><input type="radio" name="util" value="none"><span>None / later</span></label>
          </div>
        </div>

        <p class="group-title">Extras</p>
        <div class="checks">
          <label class="check"><input type="checkbox" name="loft" checked><span>Sleeping loft<small>Framing, decking, ladder or stairs</small></span></label>
          <label class="check"><input type="checkbox" name="appliances" checked><span>Appliance package<small>Fridge, range, hood, water heater</small></span></label>
          <label class="check"><input type="checkbox" name="permits" checked><span>Plans &amp; permits<small>Plan set, permits or certification</small></span></label>
          <label class="check"><input type="checkbox" name="delivery"><span id="cc-deliv-txt">Delivery &amp; site prep<small>Transport, leveling, access</small></span></label>
        </div>

        <div class="field mt-2">
          <span class="label" id="cc-toilet-l">Toilet</span>
          <div class="seg" role="radiogroup" aria-labelledby="cc-toilet-l">
            <label><input type="radio" name="toilet" value="compost" checked><span>Composting</span></label>
            <label><input type="radio" name="toilet" value="flush"><span>Flush</span></label>
          </div>
        </div>

        <div class="field">
          <label for="cc-land">Land purchase (optional)</label>
          <div class="input-prefix"><span>$</span><input type="number" id="cc-land" name="land" min="0" step="1000" value="0" inputmode="numeric"></div>
          <small>Leave at 0 if you already own land or will rent a spot.</small>
        </div>
      </div>

      <div class="panel result-panel" id="cc-result">
        <p class="result-label">Estimated total cost</p>
        <div aria-live="polite" aria-atomic="true">
          <p class="result-big" id="cc-total">$60,000 - $84,000</p>
          <p class="result-sub" id="cc-sub">250 sq ft tiny house on wheels, mid-range finishes, DIY</p>
        </div>
        <div class="mini-stats">
          <div><b id="cc-psf">$240 - $336</b><span>per sq ft, before land</span></div>
          <div><b id="cc-mid">$72,000</b><span>midpoint budget</span></div>
        </div>
        <ul class="result-rows" id="cc-rows"></ul>
        <ul class="flag-list" id="cc-flags"></ul>
        <div class="result-actions">
          <button type="button" class="btn btn-light btn-sm" id="cc-copy">Copy estimate</button>
          <button type="button" class="btn btn-ghost btn-sm" id="cc-print">Print estimate</button>
        </div>
        <p class="copy-status" id="cc-copy-status" role="status"></p>
        <p class="result-note">Planning estimate in 2026 US dollars. Local labor, material prices and code requirements can move real costs well outside this range.</p>
      </div>
    </form>

    <div class="panel bk-panel" id="cc-breakdown">
      <h2>Line-item breakdown</h2>
      <p class="panel-intro">Where the money goes for the build you described. Bars show each item's share of the total.</p>
      <div class="table-wrap mt-0">
        <table class="bk-table">
          <thead><tr><th scope="col">Item</th><th scope="col" class="num">Low</th><th scope="col" class="num">High</th><th scope="col" class="bar-col">Share</th></tr></thead>
          <tbody id="cc-table"></tbody>
          <tfoot><tr><td>Total</td><td class="num" id="cc-tlo">-</td><td class="num" id="cc-thi">-</td><td class="bar-col"></td></tr></tfoot>
        </table>
      </div>
    </div>
  </div>
</section>

<section class="section tool-prose">
  <div class="narrow prose">
    <h2>How much does a tiny house cost?</h2>
    <p>Most finished tiny houses cost between about <strong>$40,000 and $150,000</strong>, and the spread comes down to three decisions: how big the house is, who does the labor and how nice the finishes are. A 200 sq ft tiny house on wheels built by its owner with basic finishes comes in around $50,000 to $78,000 all in, while a 400 sq ft builder-made home with high-end finishes on a foundation can pass $200,000 before land. This calculator from Tiny Homes Blueprint turns those decisions into a budget you can actually plan around.</p>

    <h2>How the calculator works</h2>
    <p>The core of the estimate is a cost per square foot for the structure and finishes, picked from your labor and finish choices. It is multiplied by your floor area and split into nine trade line items. Costs that do not scale neatly with size, like the trailer, foundation, utilities and permits, are added as separate items so you can see their effect on the total cost to build a tiny house.</p>
    <div class="table-wrap"><table>
      <caption class="sr">Cost per square foot used for structure and finishes</caption>
      <thead><tr><th>Finish level</th><th class="num">DIY</th><th class="num">DIY + hired trades</th><th class="num">Builder</th></tr></thead>
      <tbody>
        <tr><td>Basic</td><td class="num">$150 &ndash; $220</td><td class="num">$200 &ndash; $275</td><td class="num">$250 &ndash; $330</td></tr>
        <tr><td>Mid-range</td><td class="num">$190 &ndash; $260</td><td class="num">$245 &ndash; $330</td><td class="num">$300 &ndash; $400</td></tr>
        <tr><td>High-end</td><td class="num">$240 &ndash; $330</td><td class="num">$310 &ndash; $415</td><td class="num">$380 &ndash; $500</td></tr>
      </tbody>
    </table></div>
    <p>The &ldquo;DIY + hired trades&rdquo; column sits halfway between doing everything yourself and hiring a builder, which is how most owner-builders work: you frame and finish, and licensed electricians and plumbers handle the systems.</p>

    <h3>Fixed and size-based add-ons</h3>
    <div class="table-wrap"><table>
      <thead><tr><th>Item</th><th class="num">Range used</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Tiny house trailer</td><td class="num">$6,000 &ndash; $12,000</td><td>Scales with trailer length (about 16 to 32+ ft)</td></tr>
        <tr><td>Pier or helical pile foundation</td><td class="num">$4,000 &ndash; $10,000</td><td>Lower for small footprints and easy sites</td></tr>
        <tr><td>Slab foundation</td><td class="num">$8,000 &ndash; $20,000</td><td>Includes forming, gravel base and concrete</td></tr>
        <tr><td>Grid hookup</td><td class="num">$3,000 &ndash; $15,000</td><td>Power, water and sewer connections; distance drives cost</td></tr>
        <tr><td>Off-grid solar</td><td class="num">$8,000 &ndash; $30,000</td><td>Panels, batteries and inverter, installed</td></tr>
        <tr><td>Shell only</td><td class="num">45% &ndash; 55%</td><td>Share of the full finished cost at the same labor level</td></tr>
        <tr><td>Sleeping loft</td><td class="num">+10%</td><td>Of structure cost, for framing, decking and access</td></tr>
      </tbody>
    </table></div>

    <h3>Example budgets from the calculator</h3>
    <p>Here is what the calculator returns for five common builds, so you can see how the choices stack up. Each includes the loft, appliances, permits and delivery settings that suit that build, but no land.</p>
    <div class="table-wrap"><table>
      <thead><tr><th>Build</th><th class="num">Estimated total</th><th class="num">Per sq ft</th></tr></thead>
      <tbody>
        <tr><td>200 sq ft on wheels, basic finishes, DIY, grid hookup</td><td class="num">$49,000 &ndash; $78,000</td><td class="num">$243 &ndash; $392</td></tr>
        <tr><td>250 sq ft on wheels, mid-range, DIY + trades, off-grid solar</td><td class="num">$94,000 &ndash; $142,000</td><td class="num">$377 &ndash; $569</td></tr>
        <tr><td>300 sq ft builder-made shell on a trailer, with loft</td><td class="num">$55,000 &ndash; $85,000</td><td class="num">$182 &ndash; $282</td></tr>
        <tr><td>400 sq ft on piers, mid-range, builder, grid hookup</td><td class="num">$140,000 &ndash; $209,000</td><td class="num">$351 &ndash; $522</td></tr>
        <tr><td>700 sq ft on a slab, mid-range, DIY + trades, grid hookup</td><td class="num">$200,000 &ndash; $292,000</td><td class="num">$285 &ndash; $417</td></tr>
      </tbody>
    </table></div>
    <p>Notice that cost per square foot falls as the house gets bigger. The trailer or foundation, utility hookups and permits cost much the same for a small house as a larger one, so they weigh more heavily on a small build.</p>

    <h2>How to use your estimate</h2>
    <ol>
      <li><strong>Plan around the high number.</strong> Tiny house builds run over budget far more often than under. If the high end of your range is not affordable, change an input now rather than mid-build.</li>
      <li><strong>Add a contingency.</strong> Set aside another 10&ndash;15% for price changes, mistakes and the things you decide to upgrade once you see them in place.</li>
      <li><strong>Get real quotes for the big items.</strong> The trailer or foundation, windows and the electrical and plumbing work are the lines most worth pricing locally once you have a plan.</li>
      <li><strong>Check the rules first.</strong> Zoning decides whether you can live in the house at all. Read our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a> before buying land or a trailer.</li>
    </ol>

    <h2>Ways to lower the cost to build a tiny house</h2>
    <ul class="check-list">
      <li><strong>Build smaller.</strong> Each square foot you cut saves $150 to $500. The <a href="/tools/how-big-should-my-tiny-house-be/">tiny house size calculator</a> helps you find the smallest size that still fits your household.</li>
      <li><strong>Keep plumbing on one wall.</strong> A shared wet wall for the kitchen and bath shortens pipe runs and plumber time. Try arrangements in the <a href="/tools/tiny-house-layout-planner/">layout planner</a>.</li>
      <li><strong>Start from a complete plan.</strong> Buying a full plan set costs far less than redesigning on site. Compare options in <a href="/blog/free-tiny-house-plans/">free vs paid tiny house plans</a> and <a href="/blog/tiny-house-kits-vs-plans/">kits vs plans</a>.</li>
      <li><strong>Buy a shell and finish it yourself.</strong> A dried-in shell gets the hardest, riskiest work done by a pro while you keep the finish labor.</li>
      <li><strong>Size solar honestly.</strong> Off-grid power is one of the most variable lines. Use the <a href="/tools/off-grid-solar-calculator/">off-grid solar calculator</a> to size panels and batteries for your actual appliances.</li>
    </ul>
    <div class="callout wood">
      <strong>Building on wheels?</strong>
      <p>Weight matters as much as cost. Every upgrade adds pounds, so run your choices through the <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a> and read the <a href="/blog/tiny-house-trailer-size-guide/">trailer size guide</a> before you order a trailer.</p>
    </div>
    <p>For the full story behind these numbers, including hidden costs like insurance, storage during the build and tool purchases, read <a href="/blog/how-much-does-a-tiny-house-cost/">how much a tiny house costs in 2026</a>. When you are ready to build, Tiny Homes Blueprint offers <a href="/tiny-house-plans/">build-ready tiny house plans</a> with the dimensioned drawings a builder needs to quote accurately.</p>

    <?php faq_block([
        ['How much does a tiny house cost on average?', '<p>Most finished tiny houses cost roughly $40,000 to $150,000. Owner-built homes with basic finishes sit at the low end, around $150 to $220 per sq ft, while builder-made homes with high-end finishes can reach $380 to $500 per sq ft before land and utilities.</p>'],
        ['Is it cheaper to build a tiny house yourself?', '<p>Usually, yes. Doing the work yourself typically saves 30&ndash;40% compared with hiring a builder, because labor is a large share of the cost. You still pay for licensed trades where your jurisdiction requires them, and the build takes much longer.</p>'],
        ['How much does a tiny house trailer cost?', '<p>A purpose-built tiny house trailer typically costs about $6,000 to $12,000 depending on length, axle rating and options like drop axles or flush decks. Longer and heavier trailers sit at the top of that range.</p>'],
        ['What does a tiny house shell cost?', '<p>A dried-in shell with framing, sheathing, roofing, windows and doors usually runs about 45&ndash;55% of the cost of the finished house. You then add insulation, systems and interior finishes yourself.</p>'],
        ['Does the estimate include land?', '<p>Only if you enter a land price. Land costs vary from a few thousand dollars for rural acreage to six figures in cities, so it is kept separate from the cost per square foot.</p>'],
        ['How accurate is this tiny house cost calculator?', '<p>It is a planning estimate built on typical 2026 US price ranges, not a quote. Use it to compare options and set a budget, then get local quotes for your plan. Remote sites, high-cost regions and custom features can push real costs above the range.</p>'],
    ]); ?>

    <h2>Related tools and guides</h2>
    <ul class="related-links">
      <li><a href="/tools/tiny-house-layout-planner/"><?= icon('layout') ?> Layout planner</a></li>
      <li><a href="/tools/how-big-should-my-tiny-house-be/"><?= icon('size') ?> Size calculator</a></li>
      <li><a href="/tools/off-grid-solar-calculator/"><?= icon('solar') ?> Off-grid solar calculator</a></li>
      <li><a href="/tools/tiny-house-trailer-weight-calculator/"><?= icon('weight') ?> Trailer weight calculator</a></li>
      <li><a href="/tiny-house-on-wheels-plans/"><?= icon('wheels') ?> Tiny house on wheels plans</a></li>
      <li><a href="/small-cabin-plans/"><?= icon('cabin') ?> Small cabin plans</a></li>
      <li><a href="/adu-plans/"><?= icon('adu') ?> ADU plans</a></li>
      <li><a href="/blog/how-to-build-a-tiny-house/"><?= icon('book') ?> How to build a tiny house</a></li>
    </ul>
  </div>
</section>

<?php cta_band('Price your build from a real plan', 'A complete plan set lets builders and suppliers quote accurately. Browse Tiny Homes Blueprint plans or ask us about a modification.'); ?>
<?php page_end(['scripts' => ['/assets/js/tools/cost-calculator.js']]); ?>
