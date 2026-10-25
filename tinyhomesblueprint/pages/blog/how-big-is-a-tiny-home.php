<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Blog', '/blog/'], [$ROUTE['nav'], null]],
]);
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow"><?= e($ROUTE['cat']) ?></p>
    <h1>How Big Is a Tiny Home? Typical Sizes and Square Footage</h1>
    <p class="lead">Real square footage for tiny houses on wheels and on foundations, where the 400 sq ft code limit comes from, and how much space one or two people actually need day to day.</p>
    <?php guide_byline(); ?>
    <ul class="hero-facts">
      <li>Most are 100 to 400 sq ft</li>
      <li>On wheels: 8.5 ft wide max</li>
      <li>Code appendix: 400 sq ft, lofts excluded</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose" style="min-width:0">
      <p><strong>How big is a tiny home?</strong> Most tiny homes are 100 to 400 square feet. A tiny house on wheels is usually 8 to 8.5 feet wide and 16 to 32 feet long, giving about 130 to 270 sq ft on the main floor plus a loft. Foundation tiny homes typically run 200 to 400 sq ft, the code appendix limit.</p>
      <p>Those ranges hide a lot of variation. A 20 ft trailer and a 16 x 24 ft cabin are both "tiny," but they live very differently. Below we break the numbers down by type, explain which square footage counts and which does not, and show real plans at each size so you can picture what the numbers mean.</p>

      <div class="key-takeaways">
        <h2>Key takeaways</h2>
        <ul>
          <li>Tiny homes are generally 400 sq ft or less, not counting lofts; homes above that are usually called small houses.</li>
          <li>On wheels, width is capped at about 8.5 ft by road rules in most states, so length sets the floor area.</li>
          <li>Each foot of trailer length adds about 8.5 sq ft of main floor; a loft can add roughly 30 to 70 percent more usable space.</li>
          <li>Foundation tiny homes have no road limits, so they are usually wider and easier to lay out.</li>
          <li>The right size depends on how many people live there, whether you work from home and how much you store.</li>
        </ul>
      </div>

      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#how-big">How big are tiny homes by type?</a></li>
        <li><a href="#wheels">Tiny houses on wheels: size by trailer length</a></li>
        <li><a href="#foundation">Foundation tiny homes</a></li>
        <li><a href="#considered">What square footage is considered a tiny home?</a></li>
        <li><a href="#need">How many square feet do you need?</a></li>
        <li><a href="#plans">Real plans at each size</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="how-big">How big are tiny homes by type?</h2>
      <p>The base you build on sets most of the size limits. Here is how the common types compare, using exterior footprint for floor area, the same way most plan sets measure it.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Type</th><th>Typical footprint</th><th>Typical size</th><th>What limits it</th></tr></thead>
        <tbody>
          <tr><td>Tiny house on wheels</td><td>8.5 ft wide, 16 to 32 ft long</td><td>About 130 to 270 sq ft, plus loft</td><td>Road width and height, trailer weight rating</td></tr>
          <tr><td>Gooseneck THOW</td><td>8.5 ft wide, often 30 ft or longer</td><td>About 250 to 350 sq ft</td><td>Tow vehicle and weight</td></tr>
          <tr><td>Shipping container home</td><td>8 ft wide, 20 or 40 ft long</td><td>160 or 320 sq ft per container</td><td>Container dimensions</td></tr>
          <tr><td>Park model RV</td><td>Varies</td><td>Up to 400 sq ft set up</td><td>ANSI A119.5 standard</td></tr>
          <tr><td>Foundation tiny home</td><td>12 x 16 to 20 x 20 ft</td><td>About 190 to 400 sq ft</td><td>Code appendix, zoning, budget</td></tr>
          <tr><td>Small house (for comparison)</td><td>16 x 32 to 24 x 36 ft</td><td>About 400 to 1,000 sq ft</td><td>Zoning, lot size, budget</td></tr>
        </tbody>
      </table></div>

      <h2 id="wheels">Tiny houses on wheels: size by trailer length</h2>
      <p>A tiny house on wheels has to stay within road limits to tow without special permits: in most states that means 8.5 ft wide and 13.5 ft tall, measured to the highest point. With the width fixed, length is the main variable, and the math is simple: trailer length times 8.5 ft gives the main-floor footprint.</p>
      <figure class="diagram">
        <svg viewBox="0 0 600 420" role="img" aria-label="Scaled comparison of tiny house on wheels footprints, all 8.5 feet wide. 16 feet long gives 136 square feet, 20 feet gives 170, 24 feet gives 204, 28 feet gives 238 and 32 feet gives 272 square feet of main floor, before any loft.">
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12">
            <text x="20" y="28" font-weight="600">MAIN-FLOOR FOOTPRINT BY TRAILER LENGTH (8.5 FT WIDE)</text>
          </g>
          <g fill="none" stroke="#e8f2f2" stroke-width="2">
            <rect x="80" y="50" width="112" height="60"/>
            <rect x="80" y="122" width="140" height="60"/>
            <rect x="80" y="194" width="168" height="60"/>
            <rect x="80" y="266" width="196" height="60"/>
            <rect x="80" y="338" width="224" height="60"/>
          </g>
          <g fill="none" stroke="#f2c58d" stroke-width="1.5" stroke-dasharray="4 4">
            <rect x="80" y="122" width="56" height="60"/>
            <rect x="80" y="194" width="56" height="60"/>
            <rect x="192" y="194" width="56" height="60"/>
          </g>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12">
            <text x="20" y="84" font-weight="600">16 ft</text>
            <text x="20" y="156" font-weight="600">20 ft</text>
            <text x="20" y="228" font-weight="600">24 ft</text>
            <text x="20" y="300" font-weight="600">28 ft</text>
            <text x="20" y="372" font-weight="600">32 ft</text>
            <text x="210" y="84">136 sq ft</text>
            <text x="238" y="156">170 sq ft</text>
            <text x="266" y="228">204 sq ft</text>
            <text x="294" y="300">238 sq ft</text>
            <text x="322" y="372">272 sq ft</text>
            <text x="238" y="172" fill="#f2c58d" font-size="11">e.g. The Wren: +68 sq ft loft</text>
            <text x="266" y="244" fill="#f2c58d" font-size="11">e.g. The Finch: +136 sq ft in two lofts</text>
            <text x="294" y="316" font-size="11">e.g. The Kestrel: main-floor bedroom</text>
          </g>
        </svg>
        <figcaption>Drawn to scale. Dashed areas show where lofts typically sit above the main floor. Square footage is exterior footprint; interior width is roughly 7 to 7.5 ft after walls.</figcaption>
      </figure>
      <p>Lofts are where tiny houses on wheels gain most of their space. A sleeping loft over one end of a 20 ft trailer can add 60 to 70 sq ft; lofts at both ends of a 24 ft trailer can add well over 100. The trade-off is headroom: with a 13.5 ft height limit, a loft often has only 3 to 4 ft of clear height, enough to sit up in bed but not to stand.</p>
      <p>Longer is not automatically better. Every extra foot adds weight and makes the house harder to tow and park. A 28 to 32 ft THOW usually needs a heavy-duty truck, and some RV parks and communities limit length. Our <a href="/blog/tiny-house-trailer-size-guide/">tiny house trailer size guide</a> covers lengths, axle ratings and GVWR, and <a href="/blog/how-much-do-tiny-homes-weigh/">how much tiny homes weigh</a> explains why weight climbs so fast.</p>

      <h2 id="foundation">Foundation tiny homes</h2>
      <p>Without road limits, a foundation tiny home can be as wide as you like, which makes a big difference to how the space feels. A 12 ft wide cabin fits a real sofa facing a wall of windows; an 8.5 ft wide trailer usually cannot. Common foundation footprints include 12 x 16, 12 x 20, 16 x 20 and 16 x 24 ft, landing between about 190 and 400 sq ft before any loft.</p>
      <p>Foundation homes also escape the height limit, so a loft can have more headroom, and a steeper roof (as on an A-frame) creates a loft with real standing room at the center. If you want to go above 400 sq ft, you are into small-house territory, where cottages and ADUs of 480 to 700 sq ft are common.</p>

      <h2 id="considered">What square footage is considered a tiny home?</h2>
      <p>The most widely cited line is <strong>400 sq ft, not counting lofts</strong>. That number comes from the International Residential Code: Appendix Q, "Tiny Houses," in the 2018 edition, renumbered Appendix AQ in 2021, applies to dwellings of 400 sq ft or less excluding lofts. It is a building code appendix, so it applies only where your state or city has adopted it, and adoption varies.</p>
      <p>So what size defines a tiny home in practice? Three different numbers can matter for the same house:</p>
      <ul class="check-list">
        <li><strong>The code definition:</strong> 400 sq ft or less excluding lofts, where Appendix AQ is adopted.</li>
        <li><strong>The zoning minimum:</strong> some districts require a primary dwelling to be several hundred square feet or more, which can rule out a tiny home as a main residence even if it meets the building code.</li>
        <li><strong>The ADU maximum:</strong> backyard units often have a size cap, so a tiny home can be the easiest unit to approve.</li>
      </ul>
      <p>Rules vary by location, so check with your local planning office. Our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning laws</a> guide explains minimum dwelling sizes in more depth.</p>

      <h2 id="need">How many square feet in a tiny home do you actually need?</h2>
      <p>There is no correct number, but there are useful thresholds. These are based on what reliably fits in real floor plans, not on a formula.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Size</th><th>What usually fits</th><th>Best for</th></tr></thead>
        <tbody>
          <tr><td>Under 200 sq ft</td><td>Studio with a compact kitchen, shower bath and loft or fold-down bed</td><td>One person, a guest unit or office</td></tr>
          <tr><td>200 to 300 sq ft</td><td>Full galley kitchen, separate bath, sofa, sleeping loft or small main-floor bedroom</td><td>One person full-time, or a couple with few belongings</td></tr>
          <tr><td>300 to 400 sq ft</td><td>Room for a dining table or desk, closet storage, two sleeping areas</td><td>A couple full-time, or one person working from home</td></tr>
          <tr><td>400 to 700 sq ft</td><td>A real bedroom with a door, full-size appliances, laundry</td><td>Couples who want separation, small families</td></tr>
        </tbody>
      </table></div>
      <p>Two questions move the number more than anything else: does anyone work from home, and are lofts an option for everyone in the household? A dedicated workspace typically needs 20 to 40 sq ft, and a main-floor bedroom 70 sq ft or more, the minimum for a habitable room in recent editions of the residential code. For a personalized estimate, try the <a href="/tools/how-big-should-my-tiny-house-be/">tiny house size calculator</a>, which works through your household, work and storage needs.</p>

      <div class="callout">
        <strong>Size drives cost, but not evenly</strong>
        <p>Kitchens and bathrooms cost the same whether the house is 200 or 400 sq ft, so smaller homes cost more per square foot. Typical estimates run about $150 to $330 per sq ft for DIY builds and $250 to $500 per sq ft from a builder, depending on finish. For the full breakdown, see <a href="/blog/how-much-does-a-tiny-house-cost/">how much a tiny house costs</a>.</p>
      </div>

      <h2 id="plans">Real tiny home plans at each size</h2>
      <p>To make the numbers concrete, here are four plans from the Tiny Homes Blueprint catalog that span the tiny range, from a 20 ft trailer with a loft to a 384 sq ft cabin:</p>
      <?php plan_grid(['plan-12-2419', 'plan-12-2421', 'plan-12-2420', 'plan-12-2431'], false); ?>
      <p>The Wren and the Kestrel are both listed at 238 sq ft, but they get there differently: the Wren pairs a 20 ft main floor with a sleeping loft, while the Kestrel puts all 238 sq ft on one level on a 28 ft trailer for a main-floor bedroom with no ladder. That is a good example of why total square footage alone does not tell you how a home will live. To sketch your own arrangement, use the <a href="/tools/tiny-house-layout-planner/">layout planner</a>, and when you are ready to plan the details, read <a href="/blog/how-to-design-a-tiny-home/">how to design a tiny home</a>.</p>

      <?php faq_block([
          ['How big is the average tiny house?', '<p>Most tiny houses fall between about 150 and 400 sq ft. Tiny houses on wheels cluster in the 150 to 350 sq ft range including lofts, while foundation tiny homes are often closer to 300 to 400 sq ft because they are not limited by road width.</p>'],
          ['What is the maximum size of a tiny home?', '<p>Under IRC Appendix AQ, a tiny house is 400 sq ft or less, excluding lofts, where that appendix is adopted. A tiny house on wheels is effectively limited by road rules of about 8.5 ft wide and 13.5 ft tall in most states, plus trailer weight ratings.</p>'],
          ['Do lofts count toward tiny house square footage?', '<p>Not under Appendix AQ, which measures the 400 sq ft limit excluding lofts. Plan sets and listings often quote total square footage including lofts, so check which figure you are looking at when comparing homes.</p>'],
          ['How wide is a tiny house on wheels?', '<p>Usually 8 to 8.5 ft wide on the outside, because 8.5 ft is the maximum width most states allow without an oversize permit. After walls, the interior is typically about 7 to 7.5 ft wide.</p>'],
          ['Is 500 sq ft a tiny house?', '<p>Technically it is above the 400 sq ft tiny house definition, so it is usually called a small house, cottage or ADU. In everyday conversation people still call homes of 500 to 600 sq ft tiny, and they are small by any normal standard.</p>'],
      ]); ?>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Not sure what size to build?</h3><p>Tell Tiny Homes Blueprint how many people will live there and where it will go, and we can point you to a plan that fits.</p><a class="btn btn-light btn-sm" href="/contact/">Ask about your project</a></div>
      <div class="aside-box"><h3>Related posts</h3><ul>
        <li><a href="/blog/what-is-a-tiny-house/">What is a tiny house?</a></li>
        <li><a href="/blog/how-much-do-tiny-homes-weigh/">How much do tiny homes weigh?</a></li>
        <li><a href="/blog/tiny-house-trailer-size-guide/">Trailer size guide</a></li>
        <li><a href="/blog/how-many-tiny-homes-can-fit-on-an-acre/">How many tiny homes fit on an acre?</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/how-big-should-my-tiny-house-be/">Size calculator</a></li>
        <li><a href="/tools/tiny-house-layout-planner/">Layout planner</a></li>
        <li><a href="/tools/tiny-house-trailer-weight-calculator/">Trailer weight calculator</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Keep reading</h2>
  <?php route_cards('post', $PATH, 3); ?>
</div></section>

<?php cta_band('Found the right size? Find the plan', 'Browse tiny house plans from 160 to 400 sq ft and beyond, with full dimensions, loft details and specs for every design.'); ?>
<?php page_end(); ?>
