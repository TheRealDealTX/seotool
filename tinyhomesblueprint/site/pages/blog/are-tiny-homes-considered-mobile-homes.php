<?php
page_start([
    'breadcrumbs' => [['Home', '/'], ['Blog', '/blog/'], [$ROUTE['nav'], null]],
]);
?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow"><?= e($ROUTE['cat']) ?></p>
    <h1>Are Tiny Homes Considered Mobile Homes? RV vs HUD vs House</h1>
    <p class="lead">How tiny houses on wheels, park model RVs, HUD-code manufactured homes, modular homes and foundation tiny homes are classified, why the label matters for zoning, financing and taxes, and how to find out what yours is.</p>
    <?php guide_byline(); ?>
    <ul class="hero-facts">
      <li>Classification follows how it is built and certified</li>
      <li>Wheels usually mean RV, not mobile home</li>
      <li>Local rules have the final word</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="wrap article-layout">
    <div class="prose" style="min-width:0">
      <p><strong>Are tiny homes considered mobile homes?</strong> Usually not. A tiny house on wheels is typically classified as an RV or park model RV, while "mobile home" today generally means a HUD-code manufactured home. A tiny home on a permanent foundation is normally treated as a house under the residential building code. The exact label depends on how the home is built, certified and placed, and on local rules.</p>
      <p>The confusion is understandable: all of these homes can be small, factory-built and transportable. But the category a home falls into decides where it can legally go, how it can be financed and insured, and how it is taxed. Here is how the categories break down.</p>

      <div class="callout wood">
        <strong>General information, not legal advice</strong>
        <p>Tiny Homes Blueprint designs house plans; we are not attorneys or code officials. Definitions vary by state and locality and change over time. Confirm how your home will be classified with your local planning and building departments, your state's motor vehicle or housing agency, and your lender or insurer.</p>
      </div>

      <div class="key-takeaways">
        <h2>Key takeaways</h2>
        <ul>
          <li>Most tiny houses on wheels are built and certified as RVs (NFPA 1192) or park model RVs (ANSI A119.5), not as mobile homes.</li>
          <li>"Mobile home" is the everyday term for what federal law calls a manufactured home, built to the HUD code on a permanent chassis.</li>
          <li>Tiny homes on foundations follow the residential building code, and possibly IRC Appendix AQ where it has been adopted.</li>
          <li>Modular homes are factory-built but meet the same state or local codes as site-built houses.</li>
          <li>The label affects zoning, financing, insurance, taxes and resale, so settle it before you buy or build.</li>
        </ul>
      </div>

      <nav class="toc" aria-label="On this page"><strong>On this page</strong><ol>
        <li><a href="#categories">The five categories at a glance</a></li>
        <li><a href="#rv">Is a tiny house an RV?</a></li>
        <li><a href="#hud">What counts as a mobile home</a></li>
        <li><a href="#vs">Tiny house vs mobile home</a></li>
        <li><a href="#foundation">Foundation and modular tiny homes</a></li>
        <li><a href="#why">Why the classification matters</a></li>
        <li><a href="#check">How to find out how yours is classified</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ol></nav>

      <h2 id="categories">The five categories at a glance</h2>
      <p>In the US, small dwellings generally fall into one of five buckets. The standard a home is built to is usually what determines its category.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Category</th><th>Typically built to</th><th>Usually treated as</th><th>Typical tiny home example</th></tr></thead>
        <tbody>
          <tr><td>Recreational vehicle (RV)</td><td>NFPA 1192</td><td>Vehicle; titled and registered</td><td>Certified tiny house on wheels</td></tr>
          <tr><td>Park model RV</td><td>ANSI A119.5</td><td>RV for seasonal or extended stays in parks</td><td>Wider THOW-style home, up to 400 sq ft set up</td></tr>
          <tr><td>Manufactured ("mobile") home</td><td>Federal HUD code</td><td>Manufactured housing; can sometimes become real property</td><td>Small single-section factory home</td></tr>
          <tr><td>Modular home</td><td>State or local building codes</td><td>Real property once set on a foundation</td><td>Factory-built tiny cottage or ADU</td></tr>
          <tr><td>Site-built house</td><td>Residential code (IRC), possibly Appendix AQ</td><td>Real property</td><td>Foundation tiny home, cabin or ADU</td></tr>
        </tbody>
      </table></div>
      <p>A sixth, informal group causes the most trouble: uncertified, self-built tiny houses on wheels. They may be registered as a trailer, but they often fit no category cleanly, which can make them hard to place, insure and finance.</p>

      <figure class="diagram">
        <svg viewBox="0 0 640 330" role="img" aria-label="Classification tree. A tiny home either has a chassis or wheels, or sits on a permanent foundation. With wheels: RV built to NFPA 1192, park model RV built to ANSI A119.5, or manufactured home built to the HUD code on a permanent chassis. On a foundation: modular home built to state codes, or site-built home under the IRC and Appendix AQ where adopted. Only the HUD-code manufactured home is what most people mean by mobile home.">
          <defs><marker id="ar2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#e8f2f2"/></marker></defs>
          <g fill="none" stroke="#e8f2f2" stroke-width="1.5">
            <path d="M320 56v14"/><path d="M320 70H180v16" marker-end="url(#ar2)"/><path d="M320 70h200v16" marker-end="url(#ar2)"/>
            <path d="M180 124v16"/><path d="M80 140h200"/>
            <path d="M80 140v24" marker-end="url(#ar2)"/><path d="M180 140v24" marker-end="url(#ar2)"/><path d="M280 140v24" marker-end="url(#ar2)"/>
            <path d="M520 124v16"/><path d="M460 140h120"/>
            <path d="M460 140v24" marker-end="url(#ar2)"/><path d="M580 140v24" marker-end="url(#ar2)"/>
          </g>
          <g fill="none" stroke="#e8f2f2" stroke-width="2">
            <rect x="230" y="20" width="180" height="36" rx="6"/>
            <rect x="80" y="88" width="200" height="36" rx="6"/><rect x="420" y="88" width="200" height="36" rx="6"/>
            <rect x="34" y="166" width="92" height="64" rx="6"/><rect x="134" y="166" width="92" height="64" rx="6"/>
            <rect x="414" y="166" width="92" height="64" rx="6"/><rect x="534" y="166" width="92" height="64" rx="6"/>
          </g>
          <rect x="234" y="166" width="92" height="64" rx="6" fill="none" stroke="#f2c58d" stroke-width="2.5"/>
          <g fill="#cfe3e3" font-family="Inter,sans-serif" font-size="12" text-anchor="middle">
            <text x="320" y="42" font-weight="600">TINY HOME</text>
            <text x="180" y="110" fill="#f2c58d" font-weight="600">WHEELS OR CHASSIS</text>
            <text x="520" y="110" fill="#f2c58d" font-weight="600">PERMANENT FOUNDATION</text>
            <text x="80" y="188" font-weight="600">RV</text><text x="80" y="206" font-size="11">NFPA 1192</text>
            <text x="180" y="188" font-weight="600">Park model</text><text x="180" y="206" font-size="11">ANSI A119.5</text>
            <text x="280" y="188" font-weight="600">Manufactured</text><text x="280" y="206" font-size="11">HUD code</text><text x="280" y="221" font-size="11">on chassis</text>
            <text x="460" y="188" font-weight="600">Modular</text><text x="460" y="206" font-size="11">State codes</text>
            <text x="580" y="188" font-weight="600">Site-built</text><text x="580" y="206" font-size="11">IRC / App. AQ</text>
            <text x="280" y="256" fill="#f2c58d">What most people</text><text x="280" y="272" fill="#f2c58d">call a mobile home</text>
            <text x="130" y="300">Usually titled like a vehicle</text>
            <text x="520" y="300">Usually treated as real property</text>
          </g>
        </svg>
        <figcaption>How small homes are typically classified. Only the HUD-code manufactured home matches the modern legal meaning of "mobile home."</figcaption>
      </figure>

      <h2 id="rv">Is a tiny house an RV?</h2>
      <p>A tiny house on wheels often is, if it is built and certified that way. Many professional builders construct THOWs to <strong>NFPA 1192</strong>, the standard for recreational vehicles, and participate in an industry certification program so they can label the home as compliant. Larger units may be built to <strong>ANSI A119.5</strong>, the park model RV standard, which covers RVs up to 400 sq ft in the set-up position that are designed for longer stays at a site. Some park models are wider than a typical travel trailer, which can mean special permits to move them.</p>
      <p>The RV label solves one problem and creates another. It usually means the home does not need a residential building permit, but RVs are generally intended as temporary or seasonal living quarters, and many jurisdictions restrict living in one full time outside an RV park or campground. Where your RV-certified tiny house can be lived in is a zoning question, covered in our <a href="/blog/tiny-house-zoning-laws/">tiny house zoning laws guide</a> and in <a href="/blog/where-to-put-a-tiny-house/">where to put a tiny house</a>.</p>
      <p>Designing for the road also means designing for its limits: about 8.5 ft wide and 13.5 ft tall in most states, plus trailer weight. See the <a href="/blog/tiny-house-trailer-size-guide/">tiny house trailer size guide</a> and <a href="/blog/how-much-do-tiny-homes-weigh/">how much tiny homes weigh</a>.</p>

      <h2 id="hud">What counts as a mobile home</h2>
      <p>In everyday speech, "mobile home" means a factory-built home on a steel chassis. Legally, homes built since the federal manufactured housing standards took effect in 1976 are called <strong>manufactured homes</strong>, and they are built to the HUD code (the Manufactured Home Construction and Safety Standards). "Mobile home" is often used specifically for older units built before that code applied.</p>
      <p>The federal definition of a manufactured home is broadly a structure built on a permanent chassis, designed to be used as a dwelling with or without a permanent foundation, and meeting minimum size thresholds when transported or set up (in general terms, at least 8 ft wide or 40 ft long in traveling mode, or at least 320 sq ft once erected). Many tiny houses fall below those thresholds or are built to a different standard entirely, which is one reason most tiny homes are not HUD-code homes. Some small manufactured homes do exist, though, and a few tiny home builders work within the HUD code.</p>

      <h2 id="vs">Tiny house vs mobile home: the practical differences</h2>
      <p>Beyond the legal labels, a tiny house vs mobile home comparison usually comes down to a few points:</p>
      <ul>
        <li><strong>Size:</strong> tiny houses are commonly under 400 sq ft; manufactured homes are usually much larger, with single-section homes often several hundred to over 1,000 sq ft.</li>
        <li><strong>Mobility:</strong> a THOW is designed to be towed on a standard trailer within road limits; a manufactured home is typically moved once, by a professional hauler, to a site where it stays.</li>
        <li><strong>Construction:</strong> THOWs are often built with residential-style materials on a trailer; manufactured homes follow HUD's federal standards in a factory.</li>
        <li><strong>Placement:</strong> manufactured homes may be allowed in manufactured home parks and in districts that permit them; tiny houses on wheels often follow RV rules instead. Some parks accept only HUD-code homes, so ask before you assume.</li>
      </ul>

      <h2 id="foundation">Foundation and modular tiny homes</h2>
      <p>Put a tiny home on a permanent foundation and it generally becomes a house in the eyes of the law. A site-built tiny home is permitted and inspected under the residential building code your jurisdiction has adopted, typically a version of the International Residential Code. The IRC's tiny house appendix, <strong>Appendix AQ</strong> (Appendix Q in the 2018 edition), relaxes some rules for homes of 400 sq ft or less, but only where it has been adopted.</p>
      <p>A <strong>modular</strong> tiny home is built in sections in a factory, like a manufactured home, but to the state or local building code rather than the HUD code. Once set on a foundation, it is normally treated the same as a site-built house. Foundation tiny homes still have to meet zoning rules, including any minimum dwelling size, which is why many are built as ADUs. If that is your path, see <a href="/blog/can-i-put-a-tiny-home-in-my-backyard/">can I put a tiny home in my backyard?</a> and our <a href="/adu-plans/">ADU plans</a>.</p>

      <h2 id="why">Why the classification matters</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Issue</th><th>RV or park model</th><th>Manufactured home</th><th>Foundation or modular home</th></tr></thead>
        <tbody>
          <tr><td>Where it can go</td><td>RV parks, communities, lots that allow RV living</td><td>Manufactured home parks and districts that allow them</td><td>Residential lots that meet zoning</td></tr>
          <tr><td>Financing</td><td>Often RV or personal loans</td><td>Chattel loans, or mortgages when titled as real property</td><td>Mortgages and construction loans are more available</td></tr>
          <tr><td>Taxes</td><td>Often registration or personal property tax</td><td>Varies by state and titling</td><td>Real property tax</td></tr>
          <tr><td>Value over time</td><td>Tends to depreciate</td><td>Varies; land ownership helps</td><td>Can track the local housing market</td></tr>
        </tbody>
      </table></div>
      <p>These are general patterns; state law and lender policy vary. For loan options in more detail, see <a href="/blog/how-to-finance-a-tiny-home/">how to finance a tiny home</a>.</p>

      <h2 id="check">How to find out how your tiny home is classified</h2>
      <ol>
        <li><strong>Look for a label.</strong> RV and park model homes from certified builders usually carry a compliance seal; HUD-code homes carry a HUD certification label and a data plate.</li>
        <li><strong>Check the paperwork.</strong> A vehicle title and VIN point to an RV or trailer; a deed points to real property.</li>
        <li><strong>Ask the builder</strong> exactly which standard the home is built to, and get it in writing.</li>
        <li><strong>Call your planning office</strong> and ask how they would treat the home on your specific parcel.</li>
      </ol>
      <p>Buying rather than building? Our guide on <a href="/blog/how-to-buy-a-tiny-house/">how to buy a tiny house</a> covers what to ask a seller about certification. At Tiny Homes Blueprint, we draw both trailer and foundation plans, and the right choice often depends on which classification works where you plan to live.</p>
      <?php plan_grid(['plan-12-2419', 'plan-12-2422', 'plan-12-2431', 'plan-12-2439'], false); ?>

      <?php faq_block([
          ['Is a tiny house on wheels a mobile home?', '<p>Usually not. Most tiny houses on wheels are built and certified as RVs (NFPA 1192) or park model RVs (ANSI A119.5). A mobile home, legally a manufactured home, is built to the federal HUD code on a permanent chassis. Local rules can still treat them differently, so check with your planning office.</p>'],
          ['Can I put a tiny house in a mobile home park?', '<p>Sometimes. Some manufactured home parks accept RV-certified tiny houses, but others accept only HUD-code homes. Ask the park for its written rules and confirm that local zoning allows your home type there.</p>'],
          ['Is a park model RV considered a mobile home?', '<p>Generally no. A park model RV is built to the ANSI A119.5 recreational vehicle standard and is limited to 400 sq ft in the set-up position. It is usually treated as an RV, although local rules on where it can be placed vary.</p>'],
          ['Do tiny homes depreciate like mobile homes?', '<p>Tiny houses on wheels tend to lose value over time much like RVs. A tiny home on a permanent foundation on land you own is more likely to follow the local housing market, largely because of the land. See <a href="/blog/are-tiny-homes-worth-it/">are tiny homes worth it?</a></p>'],
          ['Can a tiny house on wheels become a permanent house?', '<p>Possibly, but it is rarely as simple as removing the wheels. To be treated as a permanent dwelling, the home generally has to meet the building code and zoning for that use, which can require inspections, modifications or engineering. Ask your building department before you plan on it.</p>'],
      ]); ?>
      <p class="muted"><small>This article is general information, not legal advice. Classification rules vary by state and locality and change over time.</small></p>
    </div>
    <aside class="article-aside">
      <div class="aside-box aside-cta"><h3>Wheels or foundation?</h3><p>Tell Tiny Homes Blueprint where you plan to live and we can point you to plans that fit the rules there.</p><a class="btn btn-light btn-sm" href="/contact/">Ask about your project</a></div>
      <div class="aside-box"><h3>Related posts</h3><ul>
        <li><a href="/blog/tiny-house-zoning-laws/">Tiny house zoning laws</a></li>
        <li><a href="/blog/what-is-a-tiny-house/">What is a tiny house?</a></li>
        <li><a href="/blog/how-to-finance-a-tiny-home/">How to finance a tiny home</a></li>
        <li><a href="/blog/tiny-house-trailer-size-guide/">Trailer size guide</a></li>
      </ul></div>
      <div class="aside-box"><h3>Free tools</h3><ul>
        <li><a href="/tools/tiny-house-trailer-weight-calculator/">Trailer weight calculator</a></li>
        <li><a href="/tools/tiny-house-style-quiz/">Tiny house style quiz</a></li>
        <li><a href="/tools/tiny-house-cost-calculator/">Cost calculator</a></li>
      </ul></div>
    </aside>
  </div>
</section>

<section class="section section-alt"><div class="wrap">
  <h2>Keep reading</h2>
  <?php route_cards('post', $PATH, 3); ?>
</div></section>

<?php cta_band('Pick a plan that fits your legal path', 'Tiny Homes Blueprint designs tiny houses on wheels, cabins, cottages and ADUs, and can adapt a plan to the rules where you build.'); ?>
<?php page_end(); ?>
