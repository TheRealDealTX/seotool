<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', '/tiny-house-plans/'], ['Tiny House on Wheels', null]],
]);
$plans = plans_for_style('tiny-house-on-wheels-plans');
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Tiny house style guide</p>
    <h1>Tiny House on Wheels Plans</h1>
    <p class="lead">Tiny house on wheels plans are designed from the road up: a legal width, a legal height and a trailer that can carry the weight. This guide covers the road limits every mobile tiny home has to meet, trailer sizes and weights, layouts that balance on the axles, typical costs, and how Tiny Homes Blueprint approaches a THOW design.</p>
    <ul class="hero-facts">
      <li>Max width: 8.5 ft without a permit</li>
      <li>Max height: 13.5 ft in most states</li>
      <li>Common lengths: 16&ndash;32 ft</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose">
      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#plans">Request a custom THOW plan</a></li>
        <li><a href="#limits">Road limits for a mobile tiny home</a></li>
        <li><a href="#sizes">Trailer sizes and weights</a></li>
        <li><a href="#layout">Layouts that work on wheels</a></li>
        <li><a href="#cost">Costs</a></li>
        <li><a href="#build">Building light and road-ready</a></li>
        <li><a href="#legal">Where you can park it</a></li>
        <li><a href="#pros-cons">Pros and cons</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="plans">Request a custom tiny house on wheels plan</h2>
      <p>Tiny Homes Blueprint does not currently list a stock tiny house on wheels plan. A THOW plan has to be drawn around a specific trailer (its length, deck style, axle position and rated capacity), so we design them to order. Tell us the trailer you have or plan to buy, who will live in the home and how often you will move it, and we will quote a custom plan.</p>
    </div>
  </div>
  <div class="wrap"><?php plan_grid($plans); ?></div>
  <div class="wrap article-layout mt-2">
    <div class="prose">
      <h2 id="limits">Road limits that shape every mobile tiny home</h2>
      <p>The three numbers below decide what a tiny house on wheels can be. Go over them and you need an oversize permit (and often a pilot car) every time you move.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Limit</th><th>Typical legal maximum</th><th>What it means for the plan</th></tr></thead>
        <tbody>
          <tr><td>Width</td><td>8.5 ft (102 in.)</td><td>Interior is about 7'6"&ndash;7'10" after walls; eaves and trim count toward the width</td></tr>
          <tr><td>Height</td><td>13.5 ft in most states (13 ft in some, 14 ft in a few)</td><td>Measured from the road, so the trailer deck eats about 2 ft before the house starts</td></tr>
          <tr><td>Length</td><td>Varies by state; trailers to about 40 ft, combined truck + trailer often around 65 ft</td><td>Most homes stay at 32 ft or less to tow and park easily</td></tr>
          <tr><td>Weight</td><td>Trailer GVWR and tow vehicle ratings</td><td>The real limit for most builds; see below</td></tr>
        </tbody>
      </table></div>
      <p>Height and length rules vary by state and change over time, so check the DMV or department of transportation rules for every state you plan to tow through. Our <a href="/blog/tiny-house-trailer-size-guide/">tiny house trailer size guide</a> covers deck types, lengths and ratings in more detail.</p>

      <h2 id="sizes">Trailer sizes and weights</h2>
      <p>Weight is where most mobile tiny home plans get into trouble. A finished THOW typically weighs roughly 400 to 550 lb per foot of trailer length once furnished, and it is easy to creep past the trailer&rsquo;s gross vehicle weight rating (GVWR) with stone counters, tile and a full water tank. These are typical estimates for a finished, furnished home:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Trailer length</th><th class="num">Main floor sq ft</th><th class="num">Typical finished weight</th><th>Common trailer setup</th></tr></thead>
        <tbody>
          <tr><td>16 ft</td><td class="num">~128</td><td class="num">6,000 &ndash; 8,000 lb</td><td>Tandem axle, ~10,000 lb GVWR</td></tr>
          <tr><td>20 ft</td><td class="num">~160</td><td class="num">8,000 &ndash; 11,000 lb</td><td>Tandem 7,000 lb axles, 14,000 lb GVWR</td></tr>
          <tr><td>24 ft</td><td class="num">~192</td><td class="num">10,000 &ndash; 13,000 lb</td><td>Tandem or triple axle</td></tr>
          <tr><td>28 ft</td><td class="num">~224</td><td class="num">12,000 &ndash; 15,000 lb</td><td>Triple axle, often gooseneck</td></tr>
          <tr><td>32 ft</td><td class="num">~256</td><td class="num">14,000 &ndash; 18,000 lb</td><td>Triple axle gooseneck</td></tr>
        </tbody>
      </table></div>
      <p>Remember the GVWR includes the trailer itself, which often weighs 2,500 to 4,000 lb. Before you finalize materials, estimate the build with the <a href="/tools/tiny-house-trailer-weight-calculator/">tiny house trailer weight calculator</a> and leave at least 10% headroom under the GVWR. Towing a 10,000 lb-plus home usually takes a 3/4-ton or 1-ton truck, and some states have special license requirements for heavy combinations.</p>

      <h2 id="layout">Layouts that work on wheels</h2>

      <figure class="diagram">
        <svg viewBox="0 0 420 185" role="img" aria-label="Floor plan of a 24 foot by 8.5 foot tiny house on wheels with living area under a loft at the tongue end, kitchen over the axles and bath under a rear loft">
          <g fill="none" stroke="#e8f2f2" stroke-width="2.5"><rect x="60" y="30" width="336" height="119"/><path d="M300 30v119"/></g>
          <g fill="none" stroke="#f2c58d" stroke-dasharray="5 4" stroke-width="1.5"><path d="M60 50 20 89.5 60 129"/><rect x="226" y="30" width="64" height="10"/><rect x="226" y="139" width="64" height="10"/></g>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">
            <text x="228" y="20" font-size="10">24 ft x 8.5 ft</text>
            <text x="115" y="95">LIVING</text><text x="115" y="111" font-size="10">loft above</text>
            <text x="235" y="95">KITCHEN</text>
            <text x="348" y="90">BATH</text><text x="348" y="106" font-size="10">loft above</text>
            <text x="40" y="170" font-size="10" fill="#f2c58d">TONGUE</text><text x="258" y="170" font-size="10" fill="#f2c58d">axles / wheel wells</text>
          </g>
        </svg>
        <figcaption>A 24 ft THOW: kitchen over the axles carries the heaviest fixed weight, with a bath under the rear loft and living space under a second loft at the tongue end.</figcaption>
      </figure>

      <ul class="check-list">
        <li><strong>Balance the weight on the axles.</strong> Put the heaviest items (kitchen, water heater, fridge, tanks) over or just ahead of the axles. Aim for about 10&ndash;15% of total weight on the tongue; too little causes sway, too much overloads the truck.</li>
        <li><strong>Plan around the wheel wells.</strong> On a bumper-pull trailer, fenders intrude into the floor. Hide them under the kitchen cabinets, a bench or a closet rather than in the middle of the living room.</li>
        <li><strong>Choose loft vs single level early.</strong> With 13.5 ft total height, a loft gives about 3 to 3.5 ft of headroom above a 6'4" to 6'8" ceiling below. For a single-level home, put the bed in a gooseneck or on a raised platform with storage under it. Read more on <a href="/tiny-house-plans-with-loft/">tiny house plans with a loft</a>.</li>
        <li><strong>Use storage stairs, not just a ladder.</strong> Stairs with drawers take about 10 to 12 sq ft but are far safer and double as the closet.</li>
        <li><strong>Make the bath a wet bath or a compact 3-piece.</strong> A 30 x 30 in. shower, a compact toilet and a small vanity fit in about 5 x 7 ft.</li>
      </ul>
      <p>Lay out your trailer to scale with the <a href="/tools/tiny-house-layout-planner/">tiny house layout planner</a> and borrow ideas from <a href="/blog/tiny-house-layout-ideas/">tiny house layout ideas</a>.</p>

      <h2 id="cost">How much does a tiny house on wheels cost?</h2>
      <p>THOW costs per square foot look high because lofts usually are not counted and the trailer, tie-down hardware and lightweight materials add cost. A purpose-built tiny house trailer typically runs $6,000 to $15,000 on its own. As typical industry estimates for a 200 sq ft main floor:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Finish level</th><th class="num">Owner-built / sq ft</th><th class="num">Builder / sq ft</th><th class="num">200 sq ft (builder, excl. trailer)</th></tr></thead>
        <tbody>
          <tr><td>Basic</td><td class="num">$150 &ndash; $220</td><td class="num">$250 &ndash; $330</td><td class="num">$50k &ndash; $66k</td></tr>
          <tr><td>Mid-range</td><td class="num">$190 &ndash; $260</td><td class="num">$300 &ndash; $400</td><td class="num">$60k &ndash; $80k</td></tr>
          <tr><td>High-end</td><td class="num">$240 &ndash; $330</td><td class="num">$380 &ndash; $500</td><td class="num">$76k &ndash; $100k</td></tr>
        </tbody>
      </table></div>
      <p>Certified builders with RV certification, warranty and delivery often price at or above the top of these ranges, and off-grid systems add more. Estimate your own build with the <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a>, size solar with the <a href="/tools/off-grid-solar-calculator/">off-grid solar calculator</a> and see every line item in <a href="/blog/how-much-does-a-tiny-house-cost/">how much a tiny house costs</a>.</p>

      <h2 id="build">Building light and road-ready</h2>
      <ul>
        <li><strong>Framing:</strong> 2x4 walls at 16 in. on center, or steel or SIPs, keep weight down. Sheathe with structural panels and use hurricane ties and construction adhesive; a THOW sees forces like a small earthquake on every trip.</li>
        <li><strong>Attach the house to the trailer:</strong> bolt the floor framing or sill to the trailer frame at regular intervals with plate washers, per your trailer maker&rsquo;s guidance.</li>
        <li><strong>Materials:</strong> metal roofing, lightweight siding (fiber cement is heavy), pine or plywood interiors and butcher-block or laminate counters save hundreds of pounds.</li>
        <li><strong>Insulation:</strong> closed-cell spray foam adds rigidity and high R-value per inch, which matters in thin walls.</li>
        <li><strong>Utilities:</strong> plan RV-style 30 or 50 amp shore power, a fresh-water inlet and a sewer outlet, or tanks for off-grid use.</li>
      </ul>
      <p>For a full build sequence, see <a href="/blog/how-to-build-a-tiny-house/">how to build a tiny house</a>.</p>

      <h2 id="legal">Where you can park a tiny house on wheels</h2>
      <p>Most jurisdictions treat a tiny house on wheels as a recreational vehicle rather than a dwelling, which can limit full-time living to RV parks, campgrounds or properties where local rules specifically allow it. A growing number of cities permit THOWs as backyard units, often requiring RV certification, skirting and utility hookups. Check our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a> and your local planning office before you buy land or a trailer. If you want a small home that is a legal dwelling from day one, a foundation-built <a href="/adu-plans/">ADU</a> or <a href="/small-cabin-plans/">small cabin</a> may be simpler.</p>

      <h2 id="pros-cons">Pros and cons of tiny house on wheels plans</h2>
      <div class="pros-cons">
        <div class="pros"><h3>Pros</h3><ul><li>Movable: take your home to a new job or lot</li><li>Often avoids property tax on a building</li><li>Lower total cost than most foundation homes</li><li>Can be built in a garage or shop</li></ul></div>
        <div class="cons"><h3>Cons</h3><ul><li>Width, height and weight limits are strict</li><li>Legal parking for full-time living can be hard to find</li><li>Financing is usually an RV or personal loan</li><li>Lofts are low; storage is tight</li></ul></div>
      </div>

      <?php faq_block([
          ['How wide can a tiny house on wheels be?', '<p>8.5 ft (102 in.) is the standard legal width on US roads without an oversize permit. That includes eaves, trim and anything else sticking out, so most plans use exterior widths of about 8 ft 4 in. to 8 ft 6 in.</p>'],
          ['How tall can a tiny house on wheels be?', '<p>13.5 ft from the road is the limit in most states, but some use 13 ft and a few allow 14 ft. Check every state you will tow through. Because the trailer deck is about 2 ft high, the house itself is usually around 11 to 11.5 ft tall.</p>'],
          ['How much does a 24 ft tiny house on wheels weigh?', '<p>A finished, furnished 24 ft THOW typically weighs about 10,000 to 13,000 lb including the trailer. Material choices make a big difference; use our <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a> to estimate yours.</p>'],
          ['What truck do I need to tow a tiny house?', '<p>Most finished tiny houses need a 3/4-ton or 1-ton pickup with a towing capacity comfortably above the loaded weight. Check the truck&rsquo;s towing and combined weight ratings, not just the hitch rating.</p>'],
          ['Can I live full time in a tiny house on wheels?', '<p>It depends on local zoning. Many places classify THOWs as RVs and restrict full-time living, while others allow them in RV parks or as backyard units. See our <a href="/blog/tiny-house-zoning-laws/">zoning guide</a> for how to check.</p>'],
      ]); ?>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Designing a THOW?</h3><p>Tiny Homes Blueprint can draw a custom plan around your trailer, weight budget and road limits.</p><a class="btn btn-light btn-sm" href="/contact/">Request a quote</a></div>
      <div class="aside-box"><h3>Related styles</h3><ul>
        <li><a href="/tiny-house-plans-with-loft/">Plans with a loft</a></li><li><a href="/shipping-container-home-plans/">Shipping container homes</a></li><li><a href="/a-frame-house-plans/">A-frame house plans</a></li><li><a href="/shed-to-tiny-house/">Shed to tiny house</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-trailer-weight-calculator/">Trailer weight calculator</a></li><li><a href="/tools/tiny-house-cost-calculator/">Cost calculator</a></li><li><a href="/tools/off-grid-solar-calculator/">Off-grid solar calculator</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Explore more tiny house styles</h2>
  <?php route_cards('style', '/tiny-house-on-wheels-plans/', 4); ?>
</div></section>

<?php cta_band('Plan a tiny house on wheels that stays road-legal'); ?>
<?php page_end(); ?>
