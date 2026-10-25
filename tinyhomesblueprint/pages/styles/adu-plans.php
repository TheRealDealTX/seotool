<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', '/tiny-house-plans/'], ['ADU Plans', null]],
]);
$plans = plans_for_style('adu-plans');
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">Tiny house style guide</p>
    <h1>ADU Plans</h1>
    <p class="lead">ADU plans for backyard cottages, granny flats and rental units have to do two jobs: be a great small home and pass a city&rsquo;s accessory dwelling rules. This guide covers typical size limits, setbacks, costs and rental return, the layouts that get through permit review, and the ADU plans Tiny Homes Blueprint has ready to build.</p>
    <ul class="hero-facts">
      <li>Typical size cap: 600&ndash;1,200 sq ft</li>
      <li>Common setbacks: 4&ndash;10 ft side and rear</li>
      <li>Uses: rental, family, home office</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose">
      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#plans">ADU plans to buy</a></li>
        <li><a href="#types">Types of ADUs</a></li>
        <li><a href="#rules">Size limits, setbacks and height</a></li>
        <li><a href="#sizes">Backyard cottage plan sizes</a></li>
        <li><a href="#layout">Layouts that pass permit review</a></li>
        <li><a href="#cost">ADU costs</a></li>
        <li><a href="#rental">Rental return</a></li>
        <li><a href="#pros-cons">Pros and cons</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="plans">ADU plans to buy</h2>
      <p>Both plans below are 700 sq ft on a 20 x 38 ft footprint with 2x6 walls, a 9 ft ceiling and a flex room with a retractable wall. Plan 12-2417 is a single-level two-bedroom with no stairs, a good fit for aging parents or a long-term rental. Plan 12-2418 is a two-floor three-bedroom with a covered porch for families or higher rent. Before buying, confirm your city allows a 700 sq ft detached unit and that a 20 x 38 ft footprint fits inside your lot&rsquo;s setbacks.</p>
    </div>
  </div>
  <div class="wrap"><?php plan_grid($plans); ?></div>
  <div class="wrap article-layout mt-2">
    <div class="prose">
      <h2 id="types">Types of ADUs</h2>
      <ul>
        <li><strong>Detached ADU (backyard cottage):</strong> a separate small house behind or beside the main home. The most private option and the best for rental value, but usually the most expensive.</li>
        <li><strong>Attached ADU:</strong> an addition that shares a wall with the main house, with its own entrance. Saves on foundation and utility runs.</li>
        <li><strong>Garage conversion:</strong> turns an existing garage into a granny flat. Often the cheapest route, but watch for slab moisture, low ceilings and lost parking.</li>
        <li><strong>Junior ADU:</strong> a small unit (often capped around 500 sq ft) carved out of the existing house, sometimes sharing a bathroom.</li>
      </ul>
      <p>Converting an existing outbuilding is another path; see our <a href="/shed-to-tiny-house/">shed to tiny house conversion</a> guide.</p>

      <h2 id="rules">ADU size limits, setbacks and height</h2>
      <p>Every city writes its own ADU code, and many states have passed laws that override local limits. Treat the figures below as common ranges and confirm the current rules with your planning department before you buy granny flat plans or hire a designer.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Rule</th><th>Common range</th><th>Notes</th></tr></thead>
        <tbody>
          <tr><td>Maximum size</td><td>600&ndash;1,200 sq ft, or a % of the main house</td><td>Some cities cap at 50% of the main home&rsquo;s floor area</td></tr>
          <tr><td>Side and rear setbacks</td><td>4&ndash;10 ft</td><td>California, for example, generally allows 4 ft for ADUs under state law</td></tr>
          <tr><td>Height (detached)</td><td>16&ndash;25 ft</td><td>16 ft single-story is common; two stories often need more setback</td></tr>
          <tr><td>Parking</td><td>0&ndash;1 space</td><td>Often waived near transit or for conversions</td></tr>
          <tr><td>Owner occupancy</td><td>Varies</td><td>Some cities require the owner to live on site</td></tr>
          <tr><td>Short-term rental</td><td>Often restricted</td><td>Many cities ban rentals under 30 days</td></tr>
        </tbody>
      </table></div>

      <figure class="diagram">
        <svg viewBox="0 0 400 200" role="img" aria-label="Site plan of a 50 by 120 foot lot with the main house near the street, a 20 by 30 foot detached ADU in the rear corner, and dashed setback lines">
          <g fill="none" stroke="#e8f2f2" stroke-width="2.5"><rect x="80" y="50" width="120" height="90"/><rect x="305" y="65" width="60" height="90"/><path d="M305 110h60"/></g>
          <g fill="none" stroke="#e8f2f2" stroke-width="1"><rect x="20" y="20" width="360" height="150"/></g>
          <g fill="none" stroke="#f2c58d" stroke-dasharray="5 4" stroke-width="1.5"><path d="M80 20v150M365 20v150M220 155h160"/></g>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">
            <text x="140" y="100">MAIN HOUSE</text>
            <text x="335" y="92">ADU</text><text x="335" y="135" font-size="10">600 sq ft</text>
            <text x="252" y="98" font-size="10">backyard</text>
            <text x="50" y="95" font-size="10" fill="#f2c58d">front</text><text x="50" y="108" font-size="10" fill="#f2c58d">setback</text>
            <text x="60" y="188" font-size="10">STREET SIDE</text>
            <text x="320" y="188" font-size="10" fill="#f2c58d">5 ft side + rear setbacks</text>
          </g>
        </svg>
        <figcaption>A 50 x 120 ft lot with a 20 x 30 ft detached ADU tucked into the rear corner at 5 ft setbacks (dashed). Check your city&rsquo;s required separation between buildings and fire access path to the ADU door.</figcaption>
      </figure>

      <p>Our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning guide</a> explains how to look up your zoning district and what to ask the planning office.</p>

      <h2 id="sizes">Backyard cottage plan sizes</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Unit type</th><th class="num">Typical sq ft</th><th>Example footprint</th><th>Best for</th></tr></thead>
        <tbody>
          <tr><td>Studio</td><td class="num">300&ndash;450</td><td>16 x 24</td><td>Home office, single renter, guest suite</td></tr>
          <tr><td>One bedroom</td><td class="num">450&ndash;650</td><td>20 x 30</td><td>Aging parent, couple, steady rental</td></tr>
          <tr><td>Two bedroom</td><td class="num">650&ndash;900</td><td>20 x 38</td><td>Small family, roommates, higher rent</td></tr>
          <tr><td>Three bedroom</td><td class="num">700&ndash;1,200</td><td>20 x 38, two floors</td><td>Families, multigenerational living</td></tr>
        </tbody>
      </table></div>
      <p>Bigger is not always better. Each extra square foot raises cost and may push you past a size cap, a fee threshold or a setback limit. Use the <a href="/tools/how-big-should-my-tiny-house-be/">tiny house size calculator</a> to find the smallest unit that works. A <a href="/tiny-cottage-plans/">tiny cottage plan</a> or <a href="/small-cabin-plans/">small cabin plan</a> can also make a good backyard cottage if it fits your city&rsquo;s rules.</p>

      <h2 id="layout">ADU layouts that pass permit review</h2>
      <ul class="check-list">
        <li><strong>Entry facing a path, not the neighbor.</strong> Many codes and fire departments want a clear, lit path from the street to the ADU door. Orient the entry toward your side yard or driveway.</li>
        <li><strong>Windows placed for privacy.</strong> Near a property line, use high clerestory windows on the neighbor side and big glass toward your own yard. Some cities limit windows within a few feet of the lot line.</li>
        <li><strong>Single level where you can.</strong> A one-story unit avoids stricter height and setback rules, and works for aging in place: 36 in. doors, a curbless shower and no steps make a granny flat usable for decades.</li>
        <li><strong>Separate utilities planned early.</strong> Decide on a shared or separate electric meter, sewer lateral and water line before the design is final; trenching across a finished yard is expensive.</li>
        <li><strong>Laundry and storage inside the unit.</strong> Tenants and family members value a stacked washer and dryer and a real closet more than an extra few square feet of living room.</li>
      </ul>
      <p>Sketch a layout on the <a href="/tools/tiny-house-layout-planner/">tiny house layout planner</a> or browse <a href="/blog/tiny-house-layout-ideas/">tiny house layout ideas</a>.</p>

      <h2 id="cost">How much does it cost to build an ADU?</h2>
      <p>Most detached ADUs are built by contractors because of permit and utility complexity. These are typical industry estimates for the building itself:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Finish level</th><th class="num">Owner-built / sq ft</th><th class="num">Builder / sq ft</th><th class="num">700 sq ft (builder)</th></tr></thead>
        <tbody>
          <tr><td>Basic</td><td class="num">$150 &ndash; $220</td><td class="num">$250 &ndash; $330</td><td class="num">$175k &ndash; $231k</td></tr>
          <tr><td>Mid-range</td><td class="num">$190 &ndash; $260</td><td class="num">$300 &ndash; $400</td><td class="num">$210k &ndash; $280k</td></tr>
          <tr><td>High-end</td><td class="num">$240 &ndash; $330</td><td class="num">$380 &ndash; $500</td><td class="num">$266k &ndash; $350k</td></tr>
        </tbody>
      </table></div>
      <p>On top of construction, budget for permit and plan-review fees, possible impact or utility connection fees (some states waive these for smaller ADUs), surveys, and utility trenching, which commonly add $10,000 to $50,000 or more depending on the city and how far the ADU sits from existing lines. Estimate your project with the <a href="/tools/tiny-house-cost-calculator/">tiny house cost calculator</a> and see the full <a href="/blog/how-much-does-a-tiny-house-cost/">tiny house cost breakdown</a>.</p>

      <h2 id="rental">ADU rental return: a worked example</h2>
      <p>Whether an ADU pays off depends almost entirely on local rents and your all-in cost. Here is an illustrative example (not a forecast) for a $220,000 all-in backyard cottage, assuming about 30% of rent goes to vacancy, maintenance, insurance, property tax increases and management:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Monthly rent</th><th class="num">Gross per year</th><th class="num">Net per year</th><th class="num">Net yield</th><th class="num">Simple payback</th></tr></thead>
        <tbody>
          <tr><td>$1,200</td><td class="num">$14,400</td><td class="num">$10,080</td><td class="num">4.6%</td><td class="num">~22 years</td></tr>
          <tr><td>$1,800</td><td class="num">$21,600</td><td class="num">$15,120</td><td class="num">6.9%</td><td class="num">~15 years</td></tr>
          <tr><td>$2,500</td><td class="num">$30,000</td><td class="num">$21,000</td><td class="num">9.5%</td><td class="num">~10.5 years</td></tr>
        </tbody>
      </table></div>
      <p>Look up comparable one- and two-bedroom rents in your neighborhood, then rerun the numbers with your own cost. Financing costs, tax treatment and any added home value are not included, so talk to a lender or tax advisor before you commit. Many owners also value an ADU for family use (housing parents or adult children) as much as for income.</p>

      <h2 id="pros-cons">Pros and cons of ADU plans</h2>
      <div class="pros-cons">
        <div class="pros"><h3>Pros</h3><ul><li>Rental income or housing for family on land you own</li><li>Many states have eased ADU rules and fees</li><li>Uses existing lot, utilities and street access</li><li>Can add resale value to the property</li></ul></div>
        <div class="cons"><h3>Cons</h3><ul><li>Permit fees and utility trenching add up</li><li>Setbacks and size caps constrain the design</li><li>Construction disrupts your yard for months</li><li>Owner-occupancy or rental rules may apply</li></ul></div>
      </div>

      <?php faq_block([
          ['How big can an ADU be?', '<p>It depends on your city and state. Common caps are 600 to 1,200 sq ft for a detached ADU, sometimes limited to a percentage of the main house. California, for example, sets statewide minimums that cities must allow. Check your local ADU ordinance for current numbers.</p>'],
          ['How much does it cost to build a backyard ADU?', '<p>As a typical industry estimate, a builder-built ADU runs about $250 to $500 per sq ft depending on finishes, so roughly $175,000 to $350,000 for 700 sq ft, plus permit fees and utility connections that often add $10,000 to $50,000 or more.</p>'],
          ['What is the difference between an ADU and a granny flat?', '<p>&ldquo;Granny flat&rdquo; is an informal name for an ADU, usually one built for a family member. Legally they are the same thing: a secondary dwelling with its own kitchen, bath and entrance on a single-family lot.</p>'],
          ['Can I put a tiny house in my backyard as an ADU?', '<p>Often, yes, if it is on a permanent foundation and meets the ADU and building code. Some cities also allow a <a href="/tiny-house-on-wheels-plans/">tiny house on wheels</a> as a backyard unit, usually with extra conditions.</p>'],
          ['Are Tiny Homes Blueprint plans permit-ready for ADUs?', '<p>Our plans give you a full design to start from, but every city has its own submission rules and some require local engineering or energy calculations. <a href="/contact/">Contact us</a> about modifications to fit your lot or local requirements.</p>'],
      ]); ?>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Need an ADU plan to fit your lot?</h3><p>Tiny Homes Blueprint can flip, resize or modify a plan to fit your setbacks and size cap.</p><a class="btn btn-light btn-sm" href="/contact/">Ask about your lot</a></div>
      <div class="aside-box"><h3>Related styles</h3><ul>
        <li><a href="/tiny-cottage-plans/">Tiny cottage plans</a></li><li><a href="/small-cabin-plans/">Small cabin plans</a></li><li><a href="/shed-to-tiny-house/">Shed to tiny house</a></li><li><a href="/small-farmhouse-plans/">Small farmhouse plans</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-cost-calculator/">Cost calculator</a></li><li><a href="/tools/how-big-should-my-tiny-house-be/">Size calculator</a></li><li><a href="/tools/tiny-house-layout-planner/">Layout planner</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Explore more tiny house styles</h2>
  <?php route_cards('style', '/adu-plans/', 4); ?>
</div></section>

<?php cta_band('Add a backyard ADU with a proven plan'); ?>
<?php page_end(); ?>
