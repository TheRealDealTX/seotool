<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Blog', '/blog/'], [$ROUTE['nav'], null]],
]);
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow"><?= e($ROUTE['cat']) ?></p>
    <h1>How Much Does It Cost to Move a Tiny Home?</h1>
    <p class="lead">Per-mile towing rates, minimum charges, oversize permits, setup and utility hookups, and what it really takes to tow a tiny house yourself.</p>
    <?php guide_byline(); ?>
    <ul class="hero-facts">
      <li>Towing: roughly $1 to $5 per mile</li>
      <li>Oversize loads add permits and escorts</li>
      <li>Budget for setup at the new site</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose" style="min-width:0">
      <p><strong>How much does it cost to move a tiny home?</strong> Professional towing for a tiny house on wheels typically runs roughly $1 to $5 per mile, often with a minimum charge for short trips. Oversize permits, escort vehicles, setup and utility reconnection come on top, so a short local move might cost a few hundred dollars while a cross-country move can run into the thousands.</p>
      <p>Tiny house transport cost depends on distance, the size and weight of the house, whether it fits within legal road limits, and how much work the new site needs. Below we break down each piece, show what typical distances cost, and cover the real requirements for moving a tiny house yourself.</p>

      <div class="key-takeaways">
        <h2>Key takeaways</h2>
        <ul>
          <li>Per-mile towing is the biggest line item on long moves; minimum charges dominate short ones.</li>
          <li>A house within about 8.5 ft wide and 13.5 ft tall is legal-size in most states; beyond that, expect oversize permits and possibly escorts.</li>
          <li>Setup, leveling and reconnecting water, power and sewer are separate costs that are easy to forget.</li>
          <li>DIY towing needs a truck and hitch rated above the home's loaded weight, plus working trailer brakes.</li>
          <li>Foundation tiny homes cost far more to move, because they need house movers or a crane.</li>
        </ul>
      </div>

      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#breakdown">Cost breakdown</a></li>
        <li><a href="#distance">Towing cost by distance</a></li>
        <li><a href="#oversize">Oversize permits and escorts</a></li>
        <li><a href="#setup">Setup and utility reconnection</a></li>
        <li><a href="#diy">Moving a tiny house yourself</a></li>
        <li><a href="#save">How to save on the move</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="breakdown">Tiny house transport cost breakdown</h2>
      <p>Most moves are built from the same handful of items. The figures below are typical estimates for a tiny house on wheels; quotes vary by region, season, mover and route, so get several written quotes.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Cost item</th><th>Typical estimate</th><th>When it applies</th></tr></thead>
        <tbody>
          <tr><td>Professional towing</td><td>Roughly $1 to $5 per mile</td><td>Every hired move; heavier and larger homes sit at the higher end</td></tr>
          <tr><td>Minimum or flat fee</td><td>Varies by mover</td><td>Short moves, where per-mile pricing alone would be very low</td></tr>
          <tr><td>Oversize permits</td><td>Varies by state and load</td><td>Homes over legal width, height, length or weight limits; one permit per state crossed</td></tr>
          <tr><td>Escort or pilot vehicles</td><td>Often billed per mile or per day</td><td>Wider loads, as required by each state</td></tr>
          <tr><td>Pre-move prep</td><td>DIY time to a service call</td><td>Tire, brake, bearing and light checks; securing contents</td></tr>
          <tr><td>Setup and leveling</td><td>Often a few hundred dollars and up</td><td>Every move; more if site work or a pad is needed</td></tr>
          <tr><td>Utility reconnection</td><td>Varies with site and trades needed</td><td>Water, sewer or septic, power and propane at the new site</td></tr>
          <tr><td>Transit insurance</td><td>Varies</td><td>Check the mover's coverage and your own policy</td></tr>
        </tbody>
      </table></div>

      <h2 id="distance">Towing cost by distance</h2>
      <p>Using the typical $1 to $5 per mile range, here is what the towing portion alone looks like for common move lengths. Movers may also charge for their return trip or deadhead miles, so ask how the mileage is counted.</p>

      <figure class="diagram">
        <svg viewBox="0 0 600 300" role="img" aria-label="Range bar chart of towing cost by distance at 1 to 5 dollars per mile: 50 miles, 50 to 250 dollars; 100 miles, 100 to 500 dollars; 250 miles, 250 to 1,250 dollars; 500 miles, 500 to 2,500 dollars; 1,000 miles, 1,000 to 5,000 dollars. Minimums, permits and setup are extra.">
          <g stroke="#e8f2f2" stroke-width="1" opacity="0.25">
            <path d="M202 40v200M294 40v200M386 40v200M478 40v200M570 40v200"/>
          </g>
          <path d="M110 40v200h460" fill="none" stroke="#e8f2f2" stroke-width="1.5"/>
          <g fill="#f2c58d">
            <rect x="114.6" y="56" width="18.4" height="12" rx="2"/>
            <rect x="119.2" y="96" width="36.8" height="12" rx="2"/>
            <rect x="133" y="136" width="92" height="12" rx="2"/>
            <rect x="156" y="176" width="184" height="12" rx="2"/>
            <rect x="202" y="216" width="368" height="12" rx="2"/>
          </g>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12">
            <text x="110" y="24" font-weight="600">TOWING ONLY, AT $1 TO $5 PER MILE</text>
            <g text-anchor="end"><text x="100" y="66">50 mi</text><text x="100" y="106">100 mi</text><text x="100" y="146">250 mi</text><text x="100" y="186">500 mi</text><text x="100" y="226">1,000 mi</text></g>
            <text x="140" y="66">$50 to $250</text>
            <text x="164" y="106">$100 to $500</text>
            <text x="133" y="131">$250 to $1,250</text>
            <text x="156" y="171">$500 to $2,500</text>
            <text x="202" y="211">$1,000 to $5,000</text>
            <g text-anchor="middle"><text x="110" y="258">$0</text><text x="202" y="258">$1k</text><text x="294" y="258">$2k</text><text x="386" y="258">$3k</text><text x="478" y="258">$4k</text><text x="570" y="258">$5k</text></g>
            <text x="110" y="288" fill="#f2c58d">Add minimum charges, permits, escorts and setup on top.</text>
          </g>
        </svg>
        <figcaption>Illustrative ranges based on a typical $1 to $5 per mile estimate. Real quotes depend on the mover, the house and the route.</figcaption>
      </figure>

      <p>Where a house falls in that range usually comes down to its size and weight, the type of hitch, how remote the pickup and delivery sites are, and whether the route involves mountains, tolls or oversize restrictions. A 20 ft home with a bumper-pull hitch generally costs less to tow than a 32 ft gooseneck. To understand what you are asking a mover to pull, see <a href="/blog/how-much-do-tiny-homes-weigh/">how much tiny homes weigh</a>. How the home is classified also matters to movers and insurers; our guide on <a href="/blog/are-tiny-homes-considered-mobile-homes/">whether tiny homes are considered mobile homes</a> explains the RV, HUD and site-built categories.</p>

      <h2 id="oversize">Oversize permits and escorts</h2>
      <p>In most states, a towed load up to 8.5 ft wide and 13.5 ft tall can travel without a special permit, subject to length and weight limits that vary by state. Go past those limits and the house becomes an oversize load. That typically means a permit from every state on the route, travel restricted to certain days and hours, specific routes, signage and flags, and, for wider loads, one or more escort vehicles. Each of those adds cost and planning time.</p>
      <p>This is why most tiny houses on wheels are designed to stay within road limits from the start. The <a href="/blog/tiny-house-trailer-size-guide/">tiny house trailer size guide</a> explains the width, height, length and weight numbers in detail, and every Tiny Homes Blueprint <a href="/tiny-house-on-wheels-plans/">tiny house on wheels plan</a> is drawn 8.5 ft wide and 13 ft 6 in. tall to fit them.</p>

      <div class="callout wood">
        <strong>Rules vary by state</strong>
        <p>Size, weight, permit and escort rules are set by each state and can change. Check with the transportation department in every state you will cross, or use an experienced mover who handles permits. This article is general information, not legal advice.</p>
      </div>

      <h2 id="setup">Setup, leveling and utility reconnection</h2>
      <p>Moving a tiny house does not end at the curb. At the new site, expect to:</p>
      <ul class="check-list">
        <li>Prepare a level, well-drained parking pad (gravel or concrete) that can support the weight</li>
        <li>Position the house, then level it and stabilize it with jacks or piers</li>
        <li>Reinstall skirting, steps or a deck, and any tie-downs local rules require</li>
        <li>Reconnect water, sewer or septic, power and propane, often with a licensed electrician or plumber</li>
        <li>Inspect for anything that shifted in transit: doors, windows, cabinets and plumbing joints</li>
      </ul>
      <p>Before you go, confirm the new spot is legal and has the hookups you need. Our guide on <a href="/blog/where-to-put-a-tiny-house/">where to put a tiny house</a> covers the options, and <a href="/blog/tiny-house-zoning-laws/">tiny house zoning laws</a> explains the rules. If the house sits on a permanent foundation, the job is very different: it may require a structural house mover, a crane and new foundation work, which costs far more than towing a THOW.</p>

      <h2 id="diy">Moving a tiny house yourself</h2>
      <p>Towing your own tiny house can save the mover's fee, but only if you have the right equipment and experience. Many tiny houses on wheels weigh as much as a large travel trailer or more. At minimum you need:</p>
      <ul>
        <li><strong>A properly rated truck.</strong> Its towing capacity and combined weight rating must exceed the loaded weight of the house, with margin. Many builds call for a heavy-duty pickup.</li>
        <li><strong>The right hitch.</strong> A bumper-pull or gooseneck hitch rated for the load, with safety chains and a breakaway system.</li>
        <li><strong>Working trailer brakes and a brake controller.</strong> Inspect tires, wheel bearings, brakes and lights before every move.</li>
        <li><strong>Licensing and insurance.</strong> Some heavy combinations require a different class of driver's license in some states, and your insurance should cover the house while it is being towed.</li>
      </ul>
      <p>Use the <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a> to estimate your home's loaded weight and check it against the trailer's rating before you hook up. If you have never towed a heavy trailer, hiring a professional for the first move is usually the safer choice.</p>

      <h2 id="save">How to save on the move</h2>
      <ul>
        <li><strong>Stay legal-size.</strong> Designing within width and height limits avoids permits and escorts.</li>
        <li><strong>Pack light.</strong> Remove heavy contents and ship them separately to reduce weight and risk.</li>
        <li><strong>Be flexible on dates.</strong> Some movers charge less if they can combine your trip with another run.</li>
        <li><strong>Prep the site first.</strong> Have the pad and hookups ready so the crew is not waiting on site work.</li>
        <li><strong>Compare written quotes.</strong> Confirm what is included: mileage basis, minimums, permits, escorts, setup and insurance.</li>
      </ul>
      <p>These Tiny Homes Blueprint plans are designed as tiny houses on wheels within typical road limits:</p>
      <?php plan_grid(['plan-12-2419', 'plan-12-2420', 'plan-12-2422'], false); ?>
      <p>For the cost of the house itself, rather than the move, see <a href="/blog/how-much-does-a-tiny-house-cost/">how much a tiny house costs</a>.</p>

      <?php faq_block([
          ['How much does it cost to tow a tiny house per mile?', '<p>As a typical estimate, professional tiny house towing runs roughly $1 to $5 per mile, often with a minimum charge. Larger, heavier and oversize homes, remote locations and difficult routes tend to cost more.</p>'],
          ['Do I need a permit to move a tiny house?', '<p>Usually not if the house is within legal road limits, which in most states means about 8.5 ft wide and 13.5 ft tall plus state length and weight limits. Homes that exceed those limits typically need oversize permits from each state on the route, and sometimes escort vehicles.</p>'],
          ['Can I move a tiny house with a regular pickup truck?', '<p>Only if the truck, hitch and brakes are rated for the home\'s loaded weight with margin. Many tiny houses on wheels need a heavy-duty pickup. Estimate the weight with a trailer weight calculator and check your truck\'s towing and combined weight ratings.</p>'],
          ['How much does it cost to move a tiny house on a foundation?', '<p>Much more than towing a tiny house on wheels. It typically involves a structural house mover or crane, a transport trailer, permits and a new foundation at the destination. Get a site visit and written quote from a licensed mover.</p>'],
          ['How long does it take to move a tiny house?', '<p>Local moves can happen in a day once the site is ready. Long-distance moves depend on the distance, permit restrictions on travel days and hours, and weather. Allow extra time for permits, setup and utility reconnection.</p>'],
      ]); ?>
      <p class="muted"><small>Costs are typical estimates and vary by mover, region and route. Transport rules vary by state; confirm before you move.</small></p>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Building a house that moves?</h3><p>Tiny Homes Blueprint tiny house on wheels plans are drawn to typical road limits.</p><a class="btn btn-light btn-sm" href="/tiny-house-on-wheels-plans/">See THOW plans</a></div>
      <div class="aside-box"><h3>Related posts</h3><ul>
        <li><a href="/blog/tiny-house-trailer-size-guide/">Tiny house trailer size guide</a></li>
        <li><a href="/blog/how-much-do-tiny-homes-weigh/">How much do tiny homes weigh?</a></li>
        <li><a href="/blog/where-to-put-a-tiny-house/">Where to put a tiny house</a></li>
        <li><a href="/blog/how-much-does-a-tiny-house-cost/">How much does a tiny house cost?</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-trailer-weight-calculator/">Trailer weight calculator</a></li>
        <li><a href="/tools/tiny-house-cost-calculator/">Cost calculator</a></li>
        <li><a href="/tools/off-grid-solar-calculator/">Off-grid solar calculator</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Keep reading</h2>
  <?php route_cards('post', $PATH, 3); ?>
</div></section>

<?php cta_band('Design a tiny house that is easy to move', 'Tiny Homes Blueprint THOW plans are drawn to typical road limits, so your home can travel without oversize headaches.'); ?>
<?php page_end(); ?>
