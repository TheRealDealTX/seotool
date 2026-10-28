<?php $GLOBALS['scripts'][] = 'tools.js'; ?>
<section class="hero hero--home">
  <div class="wrap">
    <div>
      <p class="eyebrow">Cowboy Tiny Homes · Texas Built</p>
      <h1>Tiny Home Builders in Texas for <em>Custom Tiny Homes, ADUs &amp; Park Models</em></h1>
      <p class="lead">Cowboy Tiny Homes designs and builds small homes that live big — backyard casitas, tiny homes on wheels, park model cabins and custom tiny houses on a foundation. Every Cowboy Tiny Homes project starts with a real plan for your land, your budget and the codes where you build.</p>
      <ul class="hero-points">
        <li>Design &amp; build under one roof</li>
        <li>IRC and local-code compliant plans</li>
        <li>Floor plans, elevations &amp; 3D renderings</li>
        <li>San Antonio, Austin, Dallas, Fort Worth &amp; Houston</li>
      </ul>
      <div class="btn-row">
        <a class="btn btn--gold" href="/contact-us/">Get a Free Design Consult</a>
        <a class="btn btn--ghost" href="<?= PHONE_HREF ?>">Call <?= PHONE ?></a>
      </div>
    </div>
    <div class="hero-card">
      <h2>Request Your Free Quote</h2>
      <p>Tell us what you want to build. A Cowboy Tiny Homes designer will get back to you with next steps.</p>
      <form class="form" method="post" action="/contact-us/">
        <input type="hidden" name="form" value="quick">
        <input type="hidden" name="ts" value="<?= time() ?>">
        <div class="hp" aria-hidden="true"><label for="q-website">Website</label><input id="q-website" type="text" name="website" tabindex="-1" autocomplete="off"></div>
        <div><label for="q-name">Name</label><input id="q-name" type="text" name="first_name" autocomplete="name" required></div>
        <div><label for="q-phone">Phone</label><input id="q-phone" type="tel" name="phone" autocomplete="tel" required></div>
        <div class="full"><label for="q-email">Email</label><input id="q-email" type="email" name="email" autocomplete="email" required></div>
        <div><label for="q-city">City</label>
          <select id="q-city" name="city" required>
            <option value="">Select city</option>
<?php foreach (SERVICE_CITIES as $c): ?>
            <option><?= $c ?></option>
<?php endforeach; ?>
            <option>Other Texas city</option>
          </select></div>
        <div><label for="q-type">Project</label>
          <select id="q-type" name="project_type" required>
            <option value="">Select project</option>
            <option>Custom tiny home</option>
            <option>ADU / casita</option>
            <option>Tiny home on wheels</option>
            <option>Park model home</option>
            <option>Design / plans only</option>
            <option>Home remodel</option>
          </select></div>
        <div class="full"><button class="btn btn--ink" type="submit" style="width:100%">Get My Free Quote</button></div>
        <p class="form-note full">No spam, no obligation. We only use your details to reply.</p>
      </form>
    </div>
  </div>
</section>

<section class="section--tight section--alt">
  <div class="wrap stats">
    <div class="stat"><b>5</b><span>Home types: custom, ADU, THOW, park model &amp; remodel</span></div>
    <div class="stat"><b>8-part</b><span>Design package, from feasibility study to 3D renderings</span></div>
    <div class="stat"><b>IRC</b><span>Plans drawn to International Residential Code standards</span></div>
    <div class="stat"><b>Statewide</b><span>Serving homeowners across Texas</span></div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div>
      <p class="eyebrow" style="color:var(--gold-dark)">Why Texans Choose Us</p>
      <h2>The Tiny Home Builder Texas Homeowners Call When It Has to Be Done Right</h2>
      <p>Most people searching for tiny home builders in Texas find two kinds of companies: factories that sell a handful of fixed models, and general contractors who have never built anything under 1,000 square feet. Cowboy Tiny Homes sits in between. We are small house specialists, and we design every home around the person who will live in it.</p>
      <p>That matters because small spaces are unforgiving. A misplaced door or a staircase two inches too steep is something you feel every day in 300 square feet. The Cowboy Tiny Homes team plans storage, light, airflow and circulation first, then wraps it in the look you want — modern farmhouse, Hill Country limestone, Texas ranch, or clean contemporary.</p>
      <p>Just as important, we plan for the rules. Whether your build is regulated as a permanent dwelling under the International Residential Code, as an accessory dwelling unit under city zoning, or as a recreational vehicle, Cowboy Tiny Homes draws the plans so the inspector, the lender and the insurance company can all say yes.</p>
      <a class="btn btn--outline" href="/our-process/">See How We Work</a>
    </div>
    <div class="img-frame">
      <img src="/assets/img/Custom-Tiny-Homes.webp" alt="Modern cabin-style tiny home lit up at dusk" width="640" height="427" loading="lazy">
      <span class="img-badge">★ Designed &amp; built in Texas</span>
    </div>
  </div>
</section>

<section class="section section--alt" id="homes">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">What We Build</p>
      <h2>Tiny Homes, ADUs &amp; Small Houses Built for Texas</h2>
      <p class="section-intro">From a 200-square-foot tiny house on wheels to a 1,500-square-foot custom small home, Cowboy Tiny Homes handles the design and the build.</p>
    </div>
    <div class="grid-3">
      <article class="card service-card">
        <img src="/assets/img/Custom-Tiny-Homes.webp" alt="Custom tiny home on a permanent foundation" width="640" height="427" loading="lazy">
        <div class="card-body"><h3>Custom Tiny Homes</h3><p>Tiny, small and right-sized single-family homes on a permanent foundation, designed to IRC code and local zoning.</p><a class="card-more" href="/custom-tiny-homes-texas/">Custom tiny homes in Texas →</a></div>
      </article>
      <article class="card service-card">
        <img src="/assets/img/Accessory-Dwelling-Units.webp" alt="Farmhouse-style home with a covered front porch" width="640" height="427" loading="lazy">
        <div class="card-body"><h3>ADUs, Casitas &amp; Granny Flats</h3><p>Backyard homes, guest houses, mother-in-law suites and pool houses that add space, family flexibility or rental income.</p><a class="card-more" href="/adu-builders-texas/">ADU builders in Texas →</a></div>
      </article>
      <article class="card service-card">
        <img src="/assets/img/Tiny-Homes-On-Wheels.webp" alt="Tiny home on wheels on a triple-axle trailer" width="640" height="427" loading="lazy">
        <div class="card-body"><h3>Tiny Homes on Wheels</h3><p>Bumper-pull and gooseneck tiny houses built to move — ideal for RV parks, ranch land and rural property outside city limits.</p><a class="card-more" href="/tiny-homes-on-wheels-texas/">Tiny homes on wheels →</a></div>
      </article>
      <article class="card service-card">
        <img src="/assets/img/Park-Model-Homes.webp" alt="Park model home with a covered front porch" width="640" height="427" loading="lazy">
        <div class="card-body"><h3>Park Model Homes</h3><p>Cabin-style homes around 399 square feet with full kitchens, porches and lofts, perfect for RV parks and hunting or lake land.</p><a class="card-more" href="/park-model-homes-texas/">Park model homes →</a></div>
      </article>
      <article class="card service-card">
        <img src="/assets/img/Cowboy-Tiny-Homes-Home-BG.webp" alt="Blueprint drawing of a small house elevation" width="640" height="452" loading="lazy">
        <div class="card-body"><h3>Tiny House Design Services</h3><p>Already have a builder? Get permit-ready floor plans, elevations, site and electrical plans plus 3D renderings.</p><a class="card-more" href="/tiny-house-design-services/">Design services →</a></div>
      </article>
      <article class="card service-card">
        <img src="/assets/img/Home-Remodel.webp" alt="Remodeled modern kitchen with island" width="640" height="427" loading="lazy">
        <div class="card-body"><h3>Home Remodel Design</h3><p>Kitchens, baths, living areas and bedrooms re-planned with the same space-smart thinking we bring to tiny homes.</p><a class="card-more" href="/home-remodel-design-texas/">Remodel design →</a></div>
      </article>
    </div>
  </div>
</section>

<section class="section section--ink">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Every Design Includes</p>
      <h2>The Cowboy Tiny Homes Design Package</h2>
      <p class="section-intro">Every Cowboy Tiny Homes project comes with a complete set of drawings, so you know exactly what you are getting before a single board is cut.</p>
    </div>
    <div class="grid-4">
      <div class="card"><div class="icon">⌕</div><h3>Feasibility Study</h3><p>Zoning, setbacks, utilities and access checked for your lot before design starts.</p></div>
      <div class="card"><div class="icon">▦</div><h3>Floor Plans</h3><p>Dimensioned layouts with storage, furniture and circulation worked out.</p></div>
      <div class="card"><div class="icon">⌂</div><h3>Exterior Elevations</h3><p>Every side of the home drawn with materials, windows and heights.</p></div>
      <div class="card"><div class="icon">△</div><h3>Roof Plan</h3><p>Pitch, drainage and overhangs designed for Texas sun, hail and storms.</p></div>
      <div class="card"><div class="icon">⌖</div><h3>Site Plan Creation</h3><p>Placement, setbacks, driveways and utility runs mapped on your property.</p></div>
      <div class="card"><div class="icon">ϟ</div><h3>Electrical Layout</h3><p>Outlets, lighting, panel and HVAC planned for how you will actually live.</p></div>
      <div class="card"><div class="icon">◐</div><h3>Interior &amp; Exterior Renderings</h3><p>Photo-style images of finishes and colors so there are no surprises.</p></div>
      <div class="card"><div class="icon">◇</div><h3>3D Perspective Renderings</h3><p>Walk through your home in 3D before you commit to construction.</p></div>
    </div>
  </div>
</section>

<section class="section" id="estimate">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" style="color:var(--gold-dark)">Free Planning Tool</p>
      <h2>What Will Your Tiny Home Cost in Texas?</h2>
      <p class="section-intro">Get a ballpark in ten seconds. Pick a home type, slide to your size and choose a finish level.</p>
    </div>
    <div class="tool" data-tool="mini-estimate">
      <div class="tool-panel">
        <div class="field">
          <label>Home type</label>
          <div class="chips">
            <label class="chip"><input type="radio" name="type" value="thow" checked><span>Tiny home on wheels</span></label>
            <label class="chip"><input type="radio" name="type" value="park"><span>Park model</span></label>
            <label class="chip"><input type="radio" name="type" value="adu"><span>ADU / casita</span></label>
            <label class="chip"><input type="radio" name="type" value="custom"><span>Custom home</span></label>
          </div>
        </div>
        <div class="field">
          <div class="range-head"><label for="mini-size">Size</label><output for="mini-size"></output></div>
          <input id="mini-size" type="range" name="size" min="120" max="400" step="10" value="260" data-fmt="sqft">
        </div>
        <div class="field">
          <label>Finish level</label>
          <div class="chips">
            <label class="chip"><input type="radio" name="finish" value="basic"><span>Basic</span></label>
            <label class="chip"><input type="radio" name="finish" value="standard" checked><span>Standard</span></label>
            <label class="chip"><input type="radio" name="finish" value="premium"><span>Premium</span></label>
          </div>
        </div>
        <p class="tool-note">Want land prep, utilities, solar, septic and financing in the math? Open the full <a href="/tools/tiny-home-cost-calculator/">tiny home cost calculator</a>.</p>
      </div>
      <div class="result-panel" aria-live="polite">
        <h3>Estimated build cost</h3>
        <div class="result-big" data-out="range">—</div>
        <p class="result-sub" data-out="note"></p>
        <a class="btn btn--gold" data-out="link" href="/tools/tiny-home-cost-calculator/">Refine My Estimate</a>
        <a class="btn btn--ghost" href="/contact-us/">Get an Exact Quote</a>
        <p class="disclaimer">Planning ranges for builder-built homes in Texas in 2026. Your quote depends on design, site and materials.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">How It Works</p>
      <h2>From First Call to Front Porch in Five Steps</h2>
    </div>
    <ol class="steps">
      <li><h3>Free consultation</h3><p>Tell us about your land, budget, timeline and how you want to live.</p></li>
      <li><h3>Feasibility &amp; budget</h3><p>We check zoning, setbacks, utilities and access, then set a realistic budget.</p></li>
      <li><h3>Design &amp; renderings</h3><p>Floor plans, elevations and 3D renderings, revised until it feels like home.</p></li>
      <li><h3>Permits &amp; build</h3><p>Permit-ready drawings, then construction with regular progress updates.</p></li>
      <li><h3>Move in</h3><p>Final walkthrough, inspections signed off and keys in your hand.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div class="gallery-2">
      <img src="/assets/img/3.webp" alt="Living room of the Gonzales Modern Living small house plan" width="500" height="333" loading="lazy">
      <img src="/assets/img/4.webp" alt="Kitchen and stairs in the Gonzales Modern Living plan" width="500" height="333" loading="lazy">
    </div>
    <div>
      <p class="eyebrow" style="color:var(--gold-dark)">Featured Design</p>
      <h2>Gonzales Modern Living</h2>
      <div class="spec-row"><span class="spec">2 bedrooms</span><span class="spec">1.5 baths</span><span class="spec">2 floors</span><span class="spec">Home office</span></div>
      <p>A cozy contemporary small house with wood-textured floors, warm earth tones, a two-seat mini bar in the kitchen, a ground-floor powder room and both bedrooms plus a study upstairs. It is a favorite Cowboy Tiny Homes plan for couples and small families who want quality over square footage.</p>
      <div class="btn-row"><a class="btn btn--ink" href="/gonzales-modern-living/">View the Plan</a><a class="btn btn--outline" href="/home-designs/">All House Designs</a></div>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Interactive Tools</p>
      <h2>Plan Your Tiny Home Before You Call</h2>
      <p class="section-intro">Free tools from Cowboy Tiny Homes to help you size, price and pay for your project.</p>
    </div>
    <div class="cards cards--links">
      <a class="card card--link" href="/tools/which-tiny-home-is-right-for-me/"><span class="card-kicker">Quiz</span><strong>Which Tiny Home Is Right for Me?</strong><span>Six questions match you with a THOW, park model, ADU or custom home.</span><span class="card-more">Take the quiz →</span></a>
      <a class="card card--link" href="/tools/tiny-house-size-planner/"><span class="card-kicker">Planner</span><strong>Tiny House Size Planner</strong><span>Add the rooms you need and see the square footage and home types that fit.</span><span class="card-more">Plan my space →</span></a>
      <a class="card card--link" href="/tools/adu-rental-income-calculator/"><span class="card-kicker">Calculator</span><strong>ADU Rental Income Calculator</strong><span>See cash flow, ROI and payback for a backyard casita rental.</span><span class="card-more">Run the numbers →</span></a>
      <a class="card card--link" href="/tools/tiny-home-loan-calculator/"><span class="card-kicker">Calculator</span><strong>Tiny Home Loan Calculator</strong><span>Compare monthly payments for RV loans, personal loans, HELOCs and mortgages.</span><span class="card-more">Estimate payments →</span></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid-2">
    <div>
      <p class="eyebrow" style="color:var(--gold-dark)">Service Areas</p>
      <h2>Building Tiny Homes Across Texas</h2>
      <p>Cowboy Tiny Homes builds throughout Texas, from the San Antonio area and Hill Country to Austin, Dallas–Fort Worth and Houston. Rules for tiny houses change from one city to the next — Austin's HOME code changes, Houston's deed restrictions, San Antonio's ADU standards and the special-exception process in parts of Dallas all shape what you can build. We know what to ask before you buy land or pour a slab.</p>
      <ul class="checklist checklist--2">
<?php foreach (SERVICE_CITIES as $slug => $city): ?>
        <li><a href="/tiny-home-builders-<?= $slug ?>/">Tiny home builders <?= $city ?></a></li>
<?php endforeach; ?>
        <li><a href="/service-areas/">Rural Texas &amp; Hill Country</a></li>
      </ul>
    </div>
    <div class="card">
      <h3>Not sure your land allows a tiny home?</h3>
      <p>Read our plain-English guide to <a href="/guides/tiny-house-laws-texas/">tiny house laws in Texas</a>, covering building permits, zoning, IRC Appendix Q, RV rules and HOA restrictions — then use the interactive permit checklist before you call your city.</p>
      <p>Or skip the homework: the feasibility study in every Cowboy Tiny Homes design package answers it for your exact address.</p>
      <a class="btn btn--ink" href="/guides/tiny-house-laws-texas/">Read the Texas Laws Guide</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" style="color:var(--gold-dark)">From the Blog</p>
      <h2>Latest Tiny Home Ideas &amp; Advice</h2>
      <p class="section-intro">Fresh design ideas and practical tips from the Cowboy Tiny Homes blog.</p>
    </div>
    <?php post_cards(3); ?>
    <p style="text-align:center;margin-top:30px"><a class="btn btn--outline" href="/blog/">Visit the Blog</a></p>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Guides</p>
      <h2>Tiny Home Guides for Texas Buyers</h2>
    </div>
    <div class="cards cards--links">
      <a class="card card--link" href="/guides/cost-to-build-a-tiny-house-in-texas/"><span class="card-kicker">Costs</span><strong>How Much Does It Cost to Build a Tiny House in Texas?</strong><span>Real cost ranges by home type, with a line-by-line budget.</span><span class="card-more">Read the guide →</span></a>
      <a class="card card--link" href="/guides/adu-vs-park-model-vs-tiny-house-on-wheels/"><span class="card-kicker">Compare</span><strong>ADU vs Park Model vs Tiny House on Wheels</strong><span>Cost, permits, financing, mobility and resale side by side.</span><span class="card-more">Compare options →</span></a>
      <a class="card card--link" href="/guides/how-to-choose-a-tiny-home-builder-in-texas/"><span class="card-kicker">Hiring</span><strong>How to Choose the Best Tiny Home Builder in Texas</strong><span>Certifications, contracts, red flags and 15 questions to ask.</span><span class="card-more">Read the guide →</span></a>
    </div>
  </div>
</section>

<?php faq_section([
    ['Do tiny home builders in Texas need a permit to build my home?',
     '<p>Usually, yes. A tiny house on a permanent foundation is treated like any other house and needs a building permit from your city or, outside city limits, must meet any county and HOA requirements. A tiny home on wheels is often treated as an RV instead. Cowboy Tiny Homes checks the rules for your address during the feasibility study. See our <a href="/guides/tiny-house-laws-texas/">Texas tiny house laws guide</a>.</p>'],
    ['How much does a tiny home cost in Texas?',
     '<p>Most builder-built tiny homes on wheels land between about $45,000 and $120,000, park models between about $40,000 and $105,000, and backyard ADUs on a foundation between about $60,000 and $250,000 or more depending on size and finishes. Land, utilities and site work are extra. Try our <a href="/tools/tiny-home-cost-calculator/">tiny home cost calculator</a> for your own numbers.</p>'],
    ['Do I need to own land before I contact Cowboy Tiny Homes?',
     '<p>No. Many clients call us while they are still shopping for land, and we can help you evaluate a lot before you buy. You can also place a tiny home on family property, in a tiny house community or in an RV park, depending on the home type.</p>'],
    ['Can you build a tiny house on wheels and a foundation home?',
     '<p>Yes. Cowboy Tiny Homes builds tiny homes on bumper-pull and gooseneck trailers, park model homes, and permanent homes and ADUs on foundations. We will recommend the right type for your land, budget and plans.</p>'],
    ['Can I use a tiny house as a permanent residence in Texas?',
     '<p>Yes, as long as it meets local building and zoning codes for a permanent dwelling. Foundation-built tiny homes and ADUs designed to the International Residential Code are the most straightforward path to full-time living.</p>'],
    ['Do you only sell plans, or do you build too?',
     '<p>Both. You can hire Cowboy Tiny Homes for full design and build, or just for <a href="/tiny-house-design-services/">tiny house design services</a> and permit-ready drawings to hand to your own builder.</p>'],
], 'Tiny Home Builder FAQs', 'Quick answers from the Cowboy Tiny Homes team. More in our full <a href="/faqs/">tiny home FAQ</a>.'); ?>

<?php cta_band('Let’s Build Your Texas Tiny Home', 'Big ideas, built small. Call Cowboy Tiny Homes at ' . PHONE . ' or send us your project details for a free design consultation.'); ?>
