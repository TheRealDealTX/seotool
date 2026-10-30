<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Blog', '/blog/'], [$ROUTE['nav'], null]],
]);
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow"><?= e($ROUTE['cat']) ?></p>
    <h1>What Is a Tiny House? Definition, Size and Types</h1>
    <p class="lead">What counts as tiny, how a tiny home differs from a small house, the main types you will see, and what the building code actually says about homes under 400 square feet.</p>
    <?php guide_byline(); ?>
    <ul class="hero-facts">
      <li>Usually 400 sq ft or less</li>
      <li>On wheels or on a foundation</li>
      <li>A complete home, not a shed</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose" style="min-width:0">
      <p><strong>What is a tiny house?</strong> A tiny house is a small, fully functional home, usually 400 square feet or less, with its own kitchen, bathroom and sleeping area. It can be built on a trailer as a tiny house on wheels or on a permanent foundation. Homes from roughly 400 to 1,000 square feet are usually called small houses instead.</p>
      <p>That is the short version. The longer answer matters if you are planning to build or buy one, because the label "tiny house" means different things to a zoning officer, a building inspector, an insurer and a lender. This guide sorts out the definitions so you know which rules will apply to the home you have in mind.</p>

      <div class="key-takeaways">
        <h2>Key takeaways</h2>
        <ul>
          <li>A tiny house is a complete dwelling, typically 400 sq ft or less, not counting a sleeping loft.</li>
          <li>The 400 sq ft figure comes from the model building code's tiny house appendix (IRC Appendix Q, later AQ), which applies only where it has been adopted.</li>
          <li>Homes between about 400 and 1,000 sq ft are generally called small houses, cottages or cabins.</li>
          <li>The biggest practical split is wheels vs foundation: wheels usually means RV rules, a foundation usually means house rules.</li>
          <li>There is no single national legal definition, so local zoning decides where a tiny home can go.</li>
        </ul>
      </div>

      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#considered">What is considered a tiny house?</a></li>
        <li><a href="#small-house">Tiny home vs small house</a></li>
        <li><a href="#types">What are tiny homes? The main types</a></li>
        <li><a href="#code">What the building code says</a></li>
        <li><a href="#legal">Is a tiny house legal?</a></li>
        <li><a href="#right-for-you">Is a tiny house right for you?</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="considered">What is considered a tiny house?</h2>
      <p>Three things make a building a tiny house rather than a shed, a camper or a cabin with no plumbing.</p>
      <ul class="check-list">
        <li><strong>Size:</strong> generally 400 sq ft of floor area or less, with lofts often counted separately. Most tiny houses on wheels fall between about 150 and 350 sq ft once a loft is included.</li>
        <li><strong>Full-time function:</strong> a kitchen (even a compact one), a bathroom with a toilet and shower, a place to sleep and a place to sit. If you could not live in it year-round, it is closer to a shed or a cabin.</li>
        <li><strong>Permanent construction:</strong> framed, insulated, wired and plumbed like a house, whether it sits on a trailer or a foundation. That is what separates a tiny house on wheels from a typical travel trailer.</li>
      </ul>
      <p>So what is considered a tiny home in everyday use? Mostly the same thing. "Tiny house" and "tiny home" are used interchangeably, and neither has a strict legal meaning outside the specific codes and ordinances that define them. If you want to know how the square footage breaks down, our post on <a href="/blog/how-big-is-a-tiny-home/">how big a tiny home is</a> goes through typical sizes by trailer length and foundation type.</p>

      <figure class="diagram">
        <svg viewBox="0 0 600 230" role="img" aria-label="Size spectrum for homes. Under 200 square feet is informally called micro, 200 to 400 square feet is tiny, 400 to 1,000 square feet is a small house, and over 1,000 square feet is a standard home. The 400 square foot mark is the limit in IRC Appendix AQ, excluding lofts.">
          <g fill="none" stroke="#e8f2f2" stroke-width="2">
            <rect x="40" y="80" width="130" height="50"/>
            <rect x="300" y="80" width="130" height="50"/>
            <rect x="430" y="80" width="130" height="50"/>
          </g>
          <rect x="170" y="80" width="130" height="50" fill="rgba(242,197,141,.12)" stroke="#f2c58d" stroke-width="2"/>
          <g stroke="#e8f2f2" stroke-width="1.5">
            <path d="M40 130v10M170 130v10M300 130v10M430 130v10M560 130v10"/>
          </g>
          <path d="M300 40v40" stroke="#f2c58d" stroke-width="1.5" stroke-dasharray="4 4"/>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">
            <text x="300" y="32" fill="#f2c58d" font-weight="600">IRC Appendix AQ limit: 400 sq ft (lofts excluded)</text>
            <text x="105" y="110" font-weight="600">MICRO</text>
            <text x="235" y="110" fill="#f2c58d" font-weight="600">TINY</text>
            <text x="365" y="110" font-weight="600">SMALL HOUSE</text>
            <text x="495" y="110" font-weight="600">STANDARD</text>
            <text x="40" y="158">0</text>
            <text x="170" y="158">200</text>
            <text x="300" y="158">400</text>
            <text x="430" y="158">1,000</text>
            <text x="560" y="158" text-anchor="end">sq ft</text>
            <text x="105" y="190">Containers, studios</text>
            <text x="235" y="190">Most THOWs, cabins</text>
            <text x="365" y="190">Cottages, ADUs</text>
            <text x="495" y="190">Typical houses</text>
            <text x="300" y="218" font-size="11">Scale is not linear. Labels other than the 400 sq ft code mark are informal.</text>
          </g>
        </svg>
        <figcaption>Where tiny houses sit on the size spectrum. Only the 400 sq ft line comes from a code; the other labels are common usage.</figcaption>
      </figure>

      <h2 id="small-house">What is a tiny home vs a small house?</h2>
      <p>The line between tiny and small is fuzzy, but most people in the industry draw it around 400 sq ft, partly because that is where the building code's tiny house appendix stops. Above that, homes start to feel like conventional houses with normal stairs, separate bedrooms and full-size appliances.</p>
      <div class="table-wrap"><table>
        <thead><tr><th></th><th>Tiny house</th><th>Small house</th><th>Standard house</th></tr></thead>
        <tbody>
          <tr><td>Typical size</td><td>Up to 400 sq ft, plus loft</td><td>About 400 to 1,000 sq ft</td><td>Over 1,000 sq ft</td></tr>
          <tr><td>Common base</td><td>Trailer or foundation</td><td>Foundation</td><td>Foundation</td></tr>
          <tr><td>Bedrooms</td><td>Loft or one small room</td><td>One to three</td><td>Two or more</td></tr>
          <tr><td>Stairs</td><td>Ladder, ship's ladder or compact stair</td><td>Standard stair if two levels</td><td>Standard stair</td></tr>
          <tr><td>Usual legal path</td><td>RV, park model, ADU or small primary home</td><td>Primary home or ADU</td><td>Primary home</td></tr>
        </tbody>
      </table></div>
      <h3>What is considered a small house?</h3>
      <p>A small house is usually a permanent home of roughly 400 to 1,000 sq ft. It is big enough for one to three bedrooms and a conventional kitchen, and small enough to cost noticeably less to build, heat and maintain than a typical new home. Many minimum dwelling size rules in zoning ordinances fall in this range, which is one reason small houses are often easier to permit as a primary home than true tiny houses.</p>
      <h3>What are small houses called?</h3>
      <p>Small houses go by a lot of names, usually describing their style or use rather than their size: cottages, cabins, bungalows, casitas, carriage houses, granny flats, in-law suites and backyard cottages. Planners call a second home on a residential lot an accessory dwelling unit, or ADU. Very small homes are sometimes called micro homes, and factory-built units under 400 sq ft are often sold as park model RVs.</p>

      <h2 id="types">What are tiny homes? The main types</h2>
      <p>Tiny homes come in a handful of recognizable forms. The type you choose affects cost, legal path and how easy the home is to move or finance.</p>
      <ul>
        <li><strong>Tiny house on wheels (THOW):</strong> built on a trailer and limited by road rules, usually 8.5 ft wide and 13.5 ft tall in most states. Usually treated as an RV. See our <a href="/tiny-house-on-wheels-plans/">tiny house on wheels plans</a>.</li>
        <li><strong>Foundation tiny home:</strong> a small cabin or cottage on piers, a crawlspace or a slab, permitted like a house. Our <a href="/small-cabin-plans/">small cabin plans</a> start around 250 sq ft.</li>
        <li><strong>Shipping container home:</strong> one or more steel containers converted into living space. A single 20 ft container gives about 160 sq ft; see <a href="/shipping-container-home-plans/">container home plans</a>.</li>
        <li><strong>A-frame:</strong> a steep triangular roof that doubles as the walls, with a loft tucked into the peak. See <a href="/a-frame-house-plans/">A-frame house plans</a>.</li>
        <li><strong>Shed conversion:</strong> a prebuilt or site-built shed finished as a living space. It must meet dwelling standards to be lived in legally; see <a href="/shed-to-tiny-house/">shed to tiny house</a>.</li>
        <li><strong>Backyard ADU:</strong> a tiny or small home behind an existing house, used for family, guests or rental income. See <a href="/adu-plans/">ADU plans</a>.</li>
      </ul>
      <p>Here is one real example of four of those types from the Tiny Homes Blueprint catalog, each under 300 sq ft:</p>
      <?php plan_grid(['plan-12-2419', 'plan-12-2426', 'plan-12-2425', 'plan-12-2433'], false); ?>

      <h2 id="code">What the building code says about tiny houses</h2>
      <p>The 2018 International Residential Code added <strong>Appendix Q, "Tiny Houses,"</strong> renumbered <strong>Appendix AQ</strong> in the 2021 edition. It applies to dwellings of 400 sq ft or less, excluding lofts, and relaxes a few rules that make very small homes hard to build under the standard code, mainly ceiling heights in lofts and the types of stairs and ladders allowed to reach them.</p>
      <p>This is the closest thing to an official definition of a tiny house in the US, but it has limits. An appendix only applies where a state or city has adopted it, adoption varies, and it covers homes on foundations rather than trailers. A tiny house on wheels is normally built to recreational vehicle standards instead, or not certified at all if it is self-built. Our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning laws</a> guide explains Appendix AQ and the RV standards in more detail.</p>

      <div class="callout">
        <strong>Why the definition matters</strong>
        <p>The same 250 sq ft home can be an RV, a park model, an ADU or a primary dwelling depending on how it is built and where it is placed. Decide which category you are aiming for before you pick a plan, because that choice drives the structure, the certification and the permits. Rules vary by location, so check with your local planning office early.</p>
      </div>

      <h2 id="legal">Is a tiny house legal?</h2>
      <p>Often yes, but where and how is set locally. In practice most tiny homes are legal in one of four ways: as a permitted home on a foundation where zoning has no high minimum size, as an ADU behind a main house, as an RV or park model in an RV park or tiny home community, or on private land where the county allows RV-style living. Questions about classification come up a lot with wheeled homes; see <a href="/blog/are-tiny-homes-considered-mobile-homes/">are tiny homes considered mobile homes?</a> for how they compare with manufactured housing. For placement options, read <a href="/blog/where-to-put-a-tiny-house/">where to put a tiny house</a>.</p>

      <h2 id="right-for-you">Is a tiny house right for you?</h2>
      <p>A tiny house trades space for lower costs, less upkeep and, with wheels, some mobility. The trade-offs are real: limited storage, little room for guests, loft ladders that get harder with age, and a legal path that takes more research than buying a conventional home. Many people find the sweet spot is a home slightly above "tiny," in the 400 to 700 sq ft range, which still feels compact but fits a real bedroom.</p>
      <p>If you are weighing it up, these posts go deeper:</p>
      <ul>
        <li><strong>Cost:</strong> <a href="/blog/how-much-does-a-tiny-house-cost/">how much a tiny house costs</a>, with typical DIY and builder price ranges per square foot.</li>
        <li><strong>Value:</strong> <a href="/blog/are-tiny-homes-worth-it/">are tiny homes worth it?</a></li>
        <li><strong>Background:</strong> <a href="/blog/tiny-house-movement/">the tiny house movement</a> and why it grew.</li>
        <li><strong>Next steps:</strong> <a href="/blog/how-to-build-a-tiny-house/">how to build a tiny house</a> or <a href="/blog/how-to-buy-a-tiny-house/">how to buy one</a>.</li>
      </ul>
      <p>When you are ready to look at real layouts, browse all <a href="/tiny-house-plans/">tiny house plans</a> or take the <a href="/tools/tiny-house-style-quiz/">style quiz</a> to see which type fits your land and budget.</p>

      <?php faq_block([
          ['What is the difference between a tiny house and a tiny home?', '<p>None in everyday use. Both terms describe a small, complete dwelling, usually 400 sq ft or less. Some people use "tiny home" for foundation builds and "tiny house" for homes on wheels, but there is no official distinction.</p>'],
          ['How many square feet is a tiny house?', '<p>Usually 400 sq ft or less, not counting a loft. That limit comes from IRC Appendix AQ (Appendix Q in the 2018 code). Most tiny houses on wheels are between about 150 and 350 sq ft including the loft.</p>'],
          ['Is a tiny house considered a real house?', '<p>A tiny house on a permanent foundation that is permitted under the residential building code is generally treated as a house. A tiny house on wheels is usually classified as an RV or trailer, which affects where it can be lived in, how it is financed and how it is insured.</p>'],
          ['What is the smallest a tiny house can be?', '<p>There is no single minimum, but the building code sets room-level limits. Recent IRC editions require habitable rooms other than kitchens to be at least 70 sq ft, and zoning may set a higher minimum for a whole dwelling. Very small units, around 100 to 150 sq ft, exist but are hard to live in full-time.</p>'],
          ['Is a shed a tiny house?', '<p>Not until it is built or finished to dwelling standards, with insulation, a bathroom, a kitchen, safe wiring and an emergency escape opening, and permitted for living in where required. Many places exempt small sheds from permits only when they are not lived in.</p>'],
      ]); ?>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Ready to see real plans?</h3><p>Tiny Homes Blueprint sells build-ready plans from 160 sq ft containers to 860 sq ft small houses, each with full specs.</p><a class="btn btn-light btn-sm" href="/tiny-house-plans/">Browse plans</a></div>
      <div class="aside-box"><h3>Related posts</h3><ul>
        <li><a href="/blog/how-big-is-a-tiny-home/">How big is a tiny home?</a></li>
        <li><a href="/blog/where-to-put-a-tiny-house/">Where to put a tiny house</a></li>
        <li><a href="/blog/tiny-house-movement/">The tiny house movement</a></li>
        <li><a href="/blog/tiny-house-zoning-laws/">Tiny house zoning laws</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-style-quiz/">Tiny house style quiz</a></li>
        <li><a href="/tools/how-big-should-my-tiny-house-be/">Size calculator</a></li>
        <li><a href="/tools/tiny-house-cost-calculator/">Cost calculator</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Keep reading</h2>
  <?php route_cards('post', $PATH, 3); ?>
</div></section>

<?php cta_band('Know what kind of tiny house you want?', 'Browse build-ready plans from Tiny Homes Blueprint for tiny houses on wheels, cabins, containers, A-frames and ADUs.'); ?>
<?php page_end(); ?>
