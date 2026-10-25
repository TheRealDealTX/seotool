<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', '/tiny-house-plans/'], ['Shipping Container Homes', null]],
]);
$plans = plans_for_style('shipping-container-home-plans');
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Tiny house style guide</p>
    <h1>Shipping Container Home Plans</h1>
    <p class="lead">Shipping container home plans start with a fixed box: 8 ft wide, 20 or 40 ft long, made of steel that was never meant to have windows cut into it. Here is how 20ft and 40ft container layouts actually work, what a container home costs, how to insulate and permit one, and when Tiny Homes Blueprint would steer you toward a framed build instead.</p>
    <ul class="hero-facts">
      <li>Box sizes: 20 ft and 40 ft, 8 ft wide</li>
      <li>Inside one 40ft box: ~300 sq ft</li>
      <li>Best for: modular, off-grid, quick shells</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose">
      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#plans">Container home plans to buy</a></li>
        <li><a href="#sizes">Container sizes and real interior space</a></li>
        <li><a href="#layouts">20ft vs 40ft container home layouts</a></li>
        <li><a href="#cost">Container home costs</a></li>
        <li><a href="#insulation">Insulation, condensation and structure</a></li>
        <li><a href="#permits">Permits and foundations</a></li>
        <li><a href="#pros-cons">Pros and cons</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="plans">Shipping container home plans to buy</h2>
      <p>Three container plans are ready to order: a single 20 ft studio, a single 40 ft one-bedroom and a double 40 ft two-bedroom home. Any plan that cuts large openings in container walls needs steel reinforcement specified by an engineer for your site, and your building department may also want to see the containers' structural condition.</p>
    </div>
  </div>
  <div class="wrap"><?php plan_grid($plans); ?></div>
  <div class="wrap article-layout mt-2">
    <div class="prose">
      <h2 id="sizes">Container sizes and real interior space</h2>
      <p>Every container home plan is a negotiation with the box. The outside dimensions are fixed by shipping standards; the inside shrinks as soon as you add insulation and finishes. Always plan with <strong>high-cube</strong> containers if you intend to live in one: the extra foot of height is the difference between a 7 ft ceiling and a cramped one.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Container</th><th>Outside (L x W x H)</th><th class="num">Raw inside sq ft</th><th class="num">After insulation*</th></tr></thead>
        <tbody>
          <tr><td>20 ft standard</td><td>20' x 8' x 8'6"</td><td class="num">~148</td><td class="num">~135</td></tr>
          <tr><td>20 ft high cube</td><td>20' x 8' x 9'6"</td><td class="num">~148</td><td class="num">~135</td></tr>
          <tr><td>40 ft standard</td><td>40' x 8' x 8'6"</td><td class="num">~302</td><td class="num">~280</td></tr>
          <tr><td>40 ft high cube</td><td>40' x 8' x 9'6"</td><td class="num">~302</td><td class="num">~280</td></tr>
        </tbody>
      </table></div>
      <p class="muted">*Assumes about 3 in. of interior wall insulation and finish on each long side, which takes the inside width from about 7'8" to about 7'2".</p>
      <p>A 7 ft wide room is workable for a galley kitchen or a hallway-style bath, but tight for a living room with a sofa facing a TV. That is why many container home plans combine boxes side by side and remove most of the shared walls, giving a 15 to 16 ft wide room. If you are still deciding how much space you need, the <a href="/tools/how-big-should-my-tiny-house-be/">tiny house size calculator</a> gives a square-footage target to plan toward.</p>

      <h2 id="layouts">20ft vs 40ft container home layouts</h2>
      <p>The 20ft container is a studio. It fits a compact kitchen, a wet bath at one end and a bed or daybed at the other, which makes it a good guest suite, office or backyard rental. The 40ft container is the workhorse of container home plans: it holds a separate bedroom, a center bath and a kitchen-living area, which is enough for one or two people full time.</p>

      <figure class="diagram">
        <svg viewBox="0 0 400 235" role="img" aria-label="Floor plans of a 20 foot container studio with bath, kitchen and bed, and a 40 foot container home with bedroom, bath, kitchen and living room and a slider opening">
          <g fill="none" stroke="#e8f2f2" stroke-width="2.5"><rect x="20" y="20" width="180" height="72"/><path d="M65 20v72"/><rect x="20" y="132" width="360" height="72"/><path d="M119 132v72M173 132v72"/></g>
          <g fill="none" stroke="#f2c58d" stroke-dasharray="5 4" stroke-width="3"><path d="M280 132h70"/><path d="M110 20h50"/></g>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">
            <text x="42" y="60">BATH</text><text x="102" y="60">KITCHEN</text><text x="170" y="60">BED</text>
            <text x="110" y="113" font-size="10">20 FT HIGH CUBE &middot; ~135 sq ft usable</text>
            <text x="69" y="172">BEDROOM</text><text x="146" y="172">BATH</text><text x="218" y="172">KITCHEN</text><text x="321" y="172">LIVING</text>
            <text x="315" y="126" font-size="10" fill="#f2c58d">slider opening</text>
            <text x="200" y="226" font-size="10">40 FT HIGH CUBE &middot; ~280 sq ft usable</text>
          </g>
        </svg>
        <figcaption>Typical 20ft and 40ft container layouts. Dashed segments mark openings cut into the side wall; each one needs a steel frame around it.</figcaption>
      </figure>

      <p>Layout tips that save money and headaches:</p>
      <ul class="check-list">
        <li><strong>Put the bath and kitchen back to back.</strong> In a 40ft box, a center bath next to the kitchen keeps all plumbing in one 10 to 12 ft zone.</li>
        <li><strong>Cut fewer, bigger openings.</strong> Each opening means cutting corrugated steel and welding in a frame. Two well-placed sliders often beat six small windows on cost and light.</li>
        <li><strong>Keep openings away from the corners.</strong> The corner posts and end frames carry the load; the long side walls are cut far more easily.</li>
        <li><strong>Combine boxes for width.</strong> Two 40ft containers side by side give about 640 sq ft outside and a 15 ft wide great room, but the cut shared wall must be reinforced with steel beams and posts.</li>
        <li><strong>Add a roof deck or pergola, not a heavy roof garden.</strong> Container roofs are thin and not designed for standing water or soil loads.</li>
      </ul>
      <p>Sketch your own arrangement to scale with the <a href="/tools/tiny-house-layout-planner/">tiny house layout planner</a>, and see more space-saving patterns in <a href="/blog/tiny-house-layout-ideas/">tiny house layout ideas</a>.</p>

      <h2 id="cost">How much do container homes cost?</h2>
      <p>A used one-trip 40ft high-cube container typically costs a few thousand dollars delivered, but the box is a small part of the budget. Cutting, welding, insulation, plumbing, electrical and finishes cost about the same as in any small home, and you add crane and delivery costs. As a typical industry estimate, a finished container home lands close to the same per-square-foot range as other tiny homes: roughly $150&ndash;$260 per sq ft owner-built and $250&ndash;$400 per sq ft with a builder at basic to mid-range finishes, with high-end builds reaching $500 per sq ft.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Configuration</th><th class="num">Outside sq ft</th><th class="num">Owner-built</th><th class="num">Builder</th></tr></thead>
        <tbody>
          <tr><td>One 20ft container</td><td class="num">160</td><td class="num">$24k &ndash; $42k</td><td class="num">$40k &ndash; $64k</td></tr>
          <tr><td>One 40ft container</td><td class="num">320</td><td class="num">$48k &ndash; $83k</td><td class="num">$80k &ndash; $128k</td></tr>
          <tr><td>Two 40ft side by side</td><td class="num">640</td><td class="num">$96k &ndash; $166k</td><td class="num">$160k &ndash; $256k</td></tr>
          <tr><td>Three 40ft containers</td><td class="num">960</td><td class="num">$144k &ndash; $250k</td><td class="num">$240k &ndash; $384k</td></tr>
        </tbody>
      </table></div>
      <p>These ranges cover basic to mid-range finishes and exclude land, foundation site work, well, septic and utility hookups. Run your own numbers with the <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a>, and if the build is off-grid, size panels and batteries with the <a href="/tools/off-grid-solar-calculator/">off-grid solar calculator</a>. Our full <a href="/blog/how-much-does-a-tiny-house-cost/">tiny house cost breakdown</a> covers the hidden line items.</p>

      <h2 id="insulation">Insulation, condensation and structure</h2>
      <p>Steel is a superb conductor of heat. An uninsulated container is an oven in summer and drips with condensation in winter, so insulation is the most important part of any container home plan.</p>
      <ul>
        <li><strong>Closed-cell spray foam</strong> (2 to 3 in., roughly R-13 to R-20) is the most common choice because it bonds to the steel and acts as a vapor barrier, stopping condensation at the metal.</li>
        <li><strong>Exterior insulation</strong> with rigid foam and new siding keeps the full interior width and protects the steel, but hides the container look.</li>
        <li><strong>A separate pitched roof</strong> over the boxes adds insulation space, sheds rain and snow and shades the steel. It is the single best upgrade in hot or snowy climates.</li>
        <li><strong>Check the floor.</strong> Original container floors are often hardwood plywood treated with pesticides for international shipping. Remove it or seal it under a new subfloor.</li>
        <li><strong>Engineering:</strong> once you cut large openings or remove walls, the box loses strength. A structural engineer should size the steel frames, headers and posts.</li>
      </ul>

      <h2 id="permits">Permits and foundations for container homes</h2>
      <p>Container homes are increasingly accepted, but rules vary widely. The 2021 International Building Code added a section on intermodal shipping containers, and some jurisdictions now reference it; others review container homes case by case or treat them like any site-built house. Ask your building department early whether they want engineered drawings, and read our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a> for minimum dwelling sizes and where small homes are allowed.</p>
      <p>Containers are designed to sit on their four corner castings, which makes foundations simple: <strong>concrete piers</strong> at each corner (plus mid-span piers on 40ft boxes) are the most common, <strong>strip footings</strong> suit multi-box builds, and a <strong>slab</strong> works on flat, dry sites. Weld or bolt the castings to embedded steel plates to resist wind uplift.</p>

      <h2 id="pros-cons">Pros and cons of container home plans</h2>
      <div class="pros-cons">
        <div class="pros"><h3>Pros</h3><ul><li>Strong steel shell arrives ready to set on piers</li><li>Fast to weather-tight once on site</li><li>Modular: add boxes later as needs grow</li><li>Industrial look suits rentals and studios</li></ul></div>
        <div class="cons"><h3>Cons</h3><ul><li>Only about 7 ft wide inside after insulation</li><li>Cutting and welding add cost and need engineering</li><li>Condensation risk if insulation is done poorly</li><li>Some counties and lenders are still wary of them</li></ul></div>
      </div>
      <p>If the narrow width is a deal-breaker, compare with a framed <a href="/small-cabin-plans/">small cabin plan</a> or a <a href="/tiny-house-on-wheels-plans/">tiny house on wheels</a>, which faces similar width limits but weighs far less.</p>

      <?php faq_block([
          ['How much does a 40ft shipping container home cost?', '<p>As a typical industry estimate, a finished 40ft container home (about 320 sq ft outside) costs roughly $48,000 to $83,000 owner-built and $80,000 to $128,000 with a builder at basic to mid-range finishes, before land, foundation and utilities.</p>'],
          ['Is a 20ft or 40ft container better for a home?', '<p>A 40ft container is better for full-time living because it fits a separate bedroom, bath and kitchen. A 20ft container works as a studio, office or guest suite, or as an add-on module to a larger build.</p>'],
          ['Are container homes cheaper than traditional builds?', '<p>Usually not by as much as people expect. The steel box is inexpensive, but cutting, reinforcing, insulating and finishing cost about the same per square foot as a framed tiny home. The main savings are speed and a strong shell.</p>'],
          ['How do you stop condensation in a container home?', '<p>Insulate with closed-cell spray foam or exterior rigid foam so warm, moist indoor air never touches cold steel, ventilate the bath and kitchen to the outside, and consider a separate pitched roof to shade the box.</p>'],
          ['Do container homes need a permit?', '<p>Yes, if anyone will live in it, it needs a building permit in most of the US. Many building departments ask for engineered drawings because openings and removed walls change how the container carries load.</p>'],
      ]); ?>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Planning a container home?</h3><p>Tiny Homes Blueprint can draw a custom container layout for one box or several.</p><a class="btn btn-light btn-sm" href="/contact/">Request a quote</a></div>
      <div class="aside-box"><h3>Related styles</h3><ul>
        <li><a href="/tiny-house-on-wheels-plans/">Tiny house on wheels</a></li><li><a href="/adu-plans/">ADU plans</a></li><li><a href="/shed-to-tiny-house/">Shed to tiny house</a></li><li><a href="/small-cabin-plans/">Small cabin plans</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-cost-calculator/">Cost calculator</a></li><li><a href="/tools/off-grid-solar-calculator/">Off-grid solar calculator</a></li><li><a href="/tools/tiny-house-layout-planner/">Layout planner</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Explore more tiny house styles</h2>
  <?php route_cards('style', '/shipping-container-home-plans/', 4); ?>
</div></section>

<?php cta_band('Plan your container home the right way'); ?>
<?php page_end(); ?>
