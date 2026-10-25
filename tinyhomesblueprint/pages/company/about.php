<?php page_start(['breadcrumbs' => [['Home', '/'], ['About', null]],
    'schema' => [['@context' => 'https://schema.org', '@type' => 'AboutPage', 'name' => 'About ' . SITE_NAME, 'url' => abs_url('/about/')]]]); ?>
<section class="page-hero bp">
  <div class="wrap">
    <p class="eyebrow">About us</p>
    <h1>About Tiny Homes Blueprint</h1>
    <p class="lead">Tiny Homes Blueprint designs build-ready tiny house plans and publishes free tools and guides for anyone who wants a smaller, simpler, more affordable home.</p>
  </div>
</section>
<section class="section">
  <div class="wrap two-col top">
    <div class="prose">
      <h2>Why we exist</h2>
      <p>Most people who dream about a tiny home get stuck long before they pick up a hammer. Will the county allow it? What will it really cost? Will a family of three fit? Is a trailer or a foundation the better call? Tiny Homes Blueprint was started to answer those questions honestly and then hand you a set of plans you can actually build from.</p>
      <p>We believe a small house should not feel like a compromise. Good tiny house design is about proportion, light, storage and flow, and getting those right takes careful drawing, not just a smaller version of a big house.</p>
      <h2>What we do</h2>
      <ul class="check-list">
        <li><strong>Tiny house plans.</strong> Complete plan sets with dimensioned floor plans, elevations, framing specs and PDF, CAD and image files. <a href="/tiny-house-plans/">Browse the plans</a>.</li>
        <li><strong>Plan modifications.</strong> Flip a layout, add a loft, change the porch or foundation. <a href="/contact/">Request a quote</a>.</li>
        <li><strong>Free planning tools.</strong> A <a href="/tools/tiny-house-cost-calculator/">cost calculator</a>, <a href="/tools/tiny-house-layout-planner/">layout planner</a>, <a href="/tools/how-big-should-my-tiny-house-be/">size calculator</a>, <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a>, <a href="/tools/off-grid-solar-calculator/">solar calculator</a> and <a href="/tools/tiny-house-style-quiz/">style quiz</a>.</li>
        <li><strong>Practical guides.</strong> Plain-English articles on <a href="/blog/how-much-does-a-tiny-house-cost/">costs</a>, <a href="/blog/how-to-build-a-tiny-house/">building</a>, <a href="/blog/tiny-house-zoning-laws/">zoning</a> and <a href="/blog/tiny-house-layout-ideas/">layouts</a>.</li>
      </ul>
    </div>
    <div>
      <img class="rounded" src="/assets/img/tiny-home-interior.webp" width="640" height="426" alt="Inside a compact tiny home kitchen and dining area" loading="lazy">
      <div class="panel mt-2">
        <h2>How we design</h2>
        <ul class="check-list">
          <li>Real fixture and appliance dimensions on every drawing</li>
          <li>2x6 exterior walls for deeper insulation</li>
          <li>Wet walls stacked to keep plumbing simple</li>
          <li>Flexible rooms that adapt as life changes</li>
          <li>Simple roof lines that are affordable to frame</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><h2>Our editorial standards</h2>
    <p class="lead">Every guide on Tiny Homes Blueprint is written to help you make a decision, not to sell you something you do not need.</p></div>
    <div class="feature-grid">
      <div class="feature"><span class="link-ico"><?= icon('book') ?></span><h3>Specific numbers</h3><p>We give cost ranges, dimensions and weights, and explain the assumptions behind them.</p></div>
      <div class="feature"><span class="link-ico"><?= icon('shield') ?></span><h3>Honest trade-offs</h3><p>Every style guide includes the downsides, because tiny living is not right for everyone.</p></div>
      <div class="feature"><span class="link-ico"><?= icon('check') ?></span><h3>Kept current</h3><p>Costs and code references are reviewed and updated as materials prices and codes change.</p></div>
      <div class="feature"><span class="link-ico"><?= icon('leaf') ?></span><h3>Check locally</h3><p>Zoning and building codes vary. We always point you to your local office for the final word.</p></div>
    </div>
  </div>
</section>
<section class="section"><div class="narrow center">
  <h2>Talk to Tiny Homes Blueprint</h2>
  <p>Call <a href="tel:<?= SITE_TEL ?>"><?= SITE_PHONE ?></a> or email <a href="mailto:<?= SITE_EMAIL ?>"><?= SITE_EMAIL ?></a>. Want to contribute an article? See <a href="/write-for-us/">Write for Us</a>.</p>
</div></section>
<?php cta_band(); ?>
<?php page_end(); ?>
