<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', '/tiny-house-plans/'], ['A-Frame House Plans', null]],
]);
$plans = plans_for_style('a-frame-house-plans');
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Tiny house style guide</p>
    <h1>A-Frame House Plans</h1>
    <p class="lead">A-frame house plans turn one steep roof into walls, weather shell and a dramatic vaulted ceiling. This guide covers A-frame sizes, real usable floor area, roof pitch, loft layouts, what an A-frame cabin costs to build in 2026 and the trade-offs designers at Tiny Homes Blueprint weigh before recommending one.</p>
    <ul class="hero-facts">
      <li>Typical size: 250&ndash;1,000 sq ft</li>
      <li>Roof pitch: 12:12 to 24:12 (45&deg;&ndash;63&deg;)</li>
      <li>Best for: snowy sites, cabins, getaways</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose">
      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#plans">Request a custom A-frame plan</a></li>
        <li><a href="#what">What makes a good A-frame plan</a></li>
        <li><a href="#usable">Usable floor area and headroom</a></li>
        <li><a href="#sizes">A-frame sizes and layouts</a></li>
        <li><a href="#cost">A-frame cabin costs</a></li>
        <li><a href="#structure">Structure and foundations</a></li>
        <li><a href="#pros-cons">Pros and cons</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="plans">Request a custom A-frame plan</h2>
      <p>Tiny Homes Blueprint does not list a stock A-frame plan in the catalog right now. A-frames are very sensitive to site conditions (snow load, wind exposure, the view you are framing), so we design them to order. Send us your lot, the footprint you have in mind and how many people need to sleep in it, and we will quote a custom A-frame cabin plan or suggest a stock plan that can be adapted.</p>
    </div>
  </div>
  <div class="wrap"><?php plan_grid($plans); ?></div>
  <div class="wrap article-layout mt-2">
    <div class="prose">
      <h2 id="what">What makes a good A-frame house plan</h2>
      <p>The appeal of an A-frame is obvious from the road: a tall triangle of glass facing a lake or a ridgeline. The plans that work well to live in get the less glamorous details right too.</p>
      <ul class="check-list">
        <li><strong>A pitch matched to the climate.</strong> A 60&deg; roof (roughly 21:12) sheds snow on its own and gives a tall loft. A 45&deg; (12:12) roof is cheaper and easier to roof but wastes less space at the floor and sheds snow more slowly.</li>
        <li><strong>Kitchen and bath in the tall middle.</strong> Upper cabinets, a shower head and a standing cook need 7 ft or more of headroom, so the wet core belongs near the center line, not against the sloped walls.</li>
        <li><strong>Storage along the low edges.</strong> The first 3 to 4 ft inside each sloped wall is too low to stand in. Good A-frame cabin plans line that strip with built-in benches, drawers, beds and bookcases instead of pretending it is floor.</li>
        <li><strong>A dormer or shed bump-out where you need it.</strong> One dormer over the bathroom or loft stair buys a lot of headroom for a modest cost and breaks up the roof.</li>
        <li><strong>Gable-end glazing with an overhang.</strong> A big glass gable faces the view, but plan an overhang or deck roof so summer sun does not cook the loft.</li>
      </ul>

      <h2 id="usable">Usable floor area and headroom in an A-frame</h2>
      <p>This is where most people get surprised. The footprint of an A-frame is not the same as its livable area. On a 60&deg; frame, the roof only reaches 5 ft of height about 3 ft in from the edge and 7 ft of height about 4 ft in. On a 45&deg; frame, 5 ft of headroom is a full 5 ft in from each side. Many building codes only count floor area with at least 5 ft of ceiling height toward habitable space, so check your local code before comparing plans by square footage.</p>

      <figure class="diagram">
        <svg viewBox="0 0 380 250" role="img" aria-label="Floor plan of a 24 by 32 foot A-frame cabin showing kitchen, bath, great room, front deck and the 5 foot headroom lines along both sloped walls">
          <g fill="none" stroke="#e8f2f2" stroke-width="2.5"><rect x="20" y="30" width="256" height="192"/><path d="M100 30v192M20 126h80"/></g>
          <g fill="none" stroke="#f2c58d" stroke-dasharray="5 4" stroke-width="1.5"><rect x="276" y="62" width="80" height="128"/><path d="M20 54h256M20 198h256"/></g>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">
            <text x="60" y="82">KITCHEN</text><text x="60" y="178">BATH</text>
            <text x="188" y="122">GREAT ROOM</text><text x="188" y="138" font-size="10">vaulted, loft over rear half</text>
            <text x="188" y="47" font-size="10" fill="#f2c58d">5 ft headroom line</text><text x="188" y="215" font-size="10" fill="#f2c58d">5 ft headroom line</text>
            <text x="316" y="130" fill="#f2c58d">DECK</text>
          </g>
        </svg>
        <figcaption>A 24 x 32 ft A-frame (768 sq ft footprint). The dashed lines mark where the sloped roof drops below 5 ft; the strip outside them is storage and built-ins, not walking space.</figcaption>
      </figure>

      <p>As a rule of thumb, plan on 70&ndash;80% of a 60&deg; A-frame's footprint being comfortable standing room, and 55&ndash;65% on a shallower 45&deg; frame. The loft adds back what the edges take away: on a 24 ft wide, 60&deg; frame with the loft floor at 9 ft, the loft is about 13 ft wide at floor level and roughly 10 ft wide at sitting height.</p>

      <h2 id="sizes">A-frame sizes and layouts</h2>
      <p>A-frame tiny house plans scale in a predictable way: the width sets the height and loft size, and the length sets how many rooms you get on the main floor.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Footprint</th><th class="num">Footprint sq ft</th><th>Peak height (60&deg;)</th><th>Typical layout</th></tr></thead>
        <tbody>
          <tr><td>14 x 20</td><td class="num">280</td><td>~12 ft</td><td>Studio cabin, sleeping nook, no loft</td></tr>
          <tr><td>20 x 24</td><td class="num">480</td><td>~17 ft</td><td>Great room, bath, small sleeping loft</td></tr>
          <tr><td>24 x 32</td><td class="num">768</td><td>~21 ft</td><td>Great room, bath, bedroom, full loft</td></tr>
          <tr><td>28 x 36</td><td class="num">1,008</td><td>~24 ft</td><td>Two bedrooms, loft office, laundry</td></tr>
        </tbody>
      </table></div>
      <p>Below about 20 ft wide, a loft becomes a crawl space, so the smallest A-frame tiny house plans are usually single-volume studios. At 24 ft wide the style really starts to work: a full-height great room, a bath and a bedroom on the main floor and a real loft above. If you are torn between this and a conventional roof, a <a href="/small-cabin-plans/">small cabin plan</a> gives more usable floor for the same footprint, while <a href="/tiny-house-plans-with-loft/">tiny house plans with a loft</a> explain stair and headroom rules in more depth. You can sketch both on a grid with the <a href="/tools/tiny-house-layout-planner/">tiny house layout planner</a>.</p>

      <h2 id="cost">How much does an A-frame cabin cost to build?</h2>
      <p>Per square foot, A-frames land in the same range as other small homes, but the numbers hide two things. First, you pay for a lot of roof: on a steep frame the roof is the wall, so roofing, underlayment and insulation cover far more area than on a box. Second, the big triangle of glass on the gable end is often the single most expensive line item. These are typical industry estimates for a finished, insulated A-frame with plumbing and electrical:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Finish level</th><th class="num">Owner-built / sq ft</th><th class="num">Builder / sq ft</th><th class="num">480 sq ft example (builder)</th></tr></thead>
        <tbody>
          <tr><td>Basic</td><td class="num">$150 &ndash; $220</td><td class="num">$250 &ndash; $330</td><td class="num">$120k &ndash; $158k</td></tr>
          <tr><td>Mid-range</td><td class="num">$190 &ndash; $260</td><td class="num">$300 &ndash; $400</td><td class="num">$144k &ndash; $192k</td></tr>
          <tr><td>High-end</td><td class="num">$240 &ndash; $330</td><td class="num">$380 &ndash; $500</td><td class="num">$182k &ndash; $240k</td></tr>
        </tbody>
      </table></div>
      <p>A 480 sq ft owner-built A-frame at a basic finish works out to roughly $72,000&ndash;$106,000 before land, well, septic and power. A-frame kits can lower the shell cost, but read our comparison of <a href="/blog/tiny-house-kits-vs-plans/">tiny house kits vs plans</a> first, because kits rarely include foundation, insulation or finishes. For your own size and finish level, run the <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a>, and see the full line-item breakdown in <a href="/blog/how-much-does-a-tiny-house-cost/">how much a tiny house costs</a>.</p>

      <h2 id="structure">Structure, insulation and foundations</h2>
      <p>Most modern A-frames are built one of two ways. <strong>Site-framed rafter pairs</strong> (2x10 or 2x12 at 16 or 24 in. on center) tied by the loft floor joists, which act as collar ties, are the most common and the friendliest for owner-builders. <strong>Glulam or timber frames</strong> at 4 to 8 ft spacing with structural insulated panels (SIPs) between them go up fast and look beautiful inside, but cost more and need a crane.</p>
      <ul>
        <li><strong>Insulation:</strong> because the roof is the wall, roof-level insulation is everything. Aim for R-38 to R-49 in cold climates. Deep rafters with closed-cell spray foam, or SIPs with a vented over-roof, avoid condensation problems in the steep slope.</li>
        <li><strong>Roofing:</strong> standing-seam metal is the usual choice: it sheds snow, lasts 40+ years and is easier to install on a steep pitch than shingles.</li>
        <li><strong>Foundation:</strong> piers or helical piles suit sloped, wooded lots; a slab or crawlspace suits flat sites. The frame pushes outward at the base, so the sill and floor framing must be designed to resist that thrust.</li>
        <li><strong>Engineering:</strong> snow and wind loads drive rafter size and spacing. Expect your building department to want stamped calculations for any A-frame in heavy-snow country.</li>
      </ul>
      <p>An A-frame on a permanent foundation is a house under the building code, so check minimum dwelling size and setbacks in our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a> before buying land.</p>

      <h2 id="pros-cons">Pros and cons of A-frame house plans</h2>
      <div class="pros-cons">
        <div class="pros"><h3>Pros</h3><ul><li>Sheds snow and heavy rain extremely well</li><li>Simple, repetitive framing suits owner-builders</li><li>Tall vaulted interior feels larger than its footprint</li><li>Iconic look that photographs well for short-term rentals</li></ul></div>
        <div class="cons"><h3>Cons</h3><ul><li>Sloped walls cost 20&ndash;40% of floor area in headroom</li><li>Furniture and cabinets are harder to place</li><li>Large gable glazing is expensive and can overheat</li><li>Hard to add on to later without breaking the shape</li></ul></div>
      </div>

      <?php faq_block([
          ['How much does it cost to build a small A-frame house?', '<p>As a typical industry estimate, a finished 400 to 500 sq ft A-frame runs about $150 to $260 per sq ft owner-built and $250 to $400 per sq ft with a builder at basic to mid-range finishes. That is roughly $60,000 to $130,000 owner-built and $100,000 to $200,000 with a builder, before land and utilities.</p>'],
          ['What is the best roof pitch for an A-frame cabin?', '<p>For snowy climates, around 60&deg; (about 21:12) is the classic choice because snow slides off and the loft is tall. In mild climates a 45&deg; (12:12) roof is cheaper and wastes less floor at the edges, but gives a lower loft.</p>'],
          ['Are A-frame houses cheaper to build?', '<p>The framing is simple, but they are not automatically cheaper per usable square foot. You pay for a large roof area and often a big glass gable, and you lose some floor to low headroom. A conventional <a href="/small-cabin-plans/">small cabin</a> usually delivers more usable space for the same budget.</p>'],
          ['Can an A-frame have a loft?', '<p>Yes, and most do once the frame is about 20 ft wide or more. The loft floor joists double as collar ties. On a 24 ft wide, 60&deg; frame, a loft is roughly 13 ft wide at floor level. Check your local code for loft stair or ladder rules.</p>'],
          ['Do I need an engineer for A-frame plans?', '<p>In heavy-snow or high-wind areas, most building departments will ask for engineered rafter or frame calculations. Even where it is not required, it is worth having an engineer confirm the base connections resist outward thrust.</p>'],
      ]); ?>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Planning an A-frame?</h3><p>Tiny Homes Blueprint can design a custom A-frame cabin plan around your site, snow load and view.</p><a class="btn btn-light btn-sm" href="/contact/">Request a quote</a></div>
      <div class="aside-box"><h3>Related styles</h3><ul>
        <li><a href="/small-cabin-plans/">Small cabin plans</a></li><li><a href="/tiny-house-plans-with-loft/">Plans with a loft</a></li><li><a href="/tiny-cottage-plans/">Tiny cottage plans</a></li><li><a href="/shipping-container-home-plans/">Shipping container homes</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-cost-calculator/">Cost calculator</a></li><li><a href="/tools/tiny-house-layout-planner/">Layout planner</a></li><li><a href="/tools/tiny-house-style-quiz/">Tiny house style quiz</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Explore more tiny house styles</h2>
  <?php route_cards('style', '/a-frame-house-plans/', 4); ?>
</div></section>

<?php cta_band('Design your A-frame cabin with us'); ?>
<?php page_end(); ?>
