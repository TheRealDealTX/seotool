<?php
/** Homepage. Keyword "McAllen Public Adjuster" is used naturally across sections. */
require_once MPA_ROOT . '/includes/weather.php';
require_once MPA_ROOT . '/includes/storms.php';
$cur = weather_current();
$fc = weather_forecast();
$al = weather_alerts();
$stats = storm_stats();
$recentEvents = array_slice(weather_events_data()['events'] ?? [], 0, 3);
$posts = array_slice(all_content('posts'), 0, 6);
$alertCount = is_array($al['data'] ?? null) ? count($al['data']) : 0;
?>
<section class="hero" aria-labelledby="hero-h">
  <div class="hero-bg" aria-hidden="true" data-parallax>
    <?= img('/wp-content/uploads/2026/04/Public-Adjuster-vs.-Insurance-Adjuster-for-Hail-Claims-4.webp', '', ['eager' => true, 'sizes' => '100vw']) ?>
  </div>
  <div class="container hero-inner">
    <div>
      <p class="eyebrow eyebrow-gold hero-anim">Licensed Texas public adjusting &middot; TDI License #<?= e(cfg('license')) ?></p>
      <h1 id="hero-h" class="hero-anim" style="--d:80ms">McAllen Public Adjuster <span class="accent">Helping Property Owners Navigate Insurance Claims</span></h1>
      <p class="hero-text hero-anim" style="--d:160ms">Dealing with hail damage, storm damage, fire damage, water damage, or a denied insurance claim? McAllen Public Adjuster helps homeowners and business owners document property losses, review insurance estimates, and understand their claim options.</p>
      <div class="hero-actions hero-anim" style="--d:240ms">
        <a class="btn btn-gold btn-lg" href="#free-claim-review">Get a Free Claim Review</a>
        <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> Call <?= e(cfg('phone_short')) ?></a>
      </div>
      <ul class="hero-badges hero-anim" style="--d:320ms">
        <li><?= icon('shield', 'icon') ?> We represent the policyholder only</li>
        <li><?= icon('home', 'icon') ?> Residential &amp; commercial claims</li>
        <li><?= icon('map', 'icon') ?> McAllen &amp; Hidalgo County</li>
      </ul>
    </div>
    <div class="hero-card hero-anim" style="--d:300ms">
      <h2>Free Claim Review</h2>
      <p>Tell us what happened. A licensed public adjuster will review your situation and explain your options. No cost, no obligation.</p>
      <?php component('claim-form', ['context' => 'Homepage hero', 'compact' => true]); ?>
    </div>
  </div>
  <div class="hero-scroll" aria-hidden="true"></div>
</section>

<section class="trust-strip" aria-label="Credentials">
  <div class="container trust-grid">
    <div class="trust-item reveal"><?= icon('shield', 'icon') ?><div><strong>TDI License #<?= e(cfg('license')) ?></strong><span>Texas Department of Insurance</span></div></div>
    <div class="trust-item reveal" style="--d:80ms"><?= icon('building', 'icon') ?><div><strong><?= e(cfg('company')) ?></strong><span>Licensed public adjusting firm</span></div></div>
    <div class="trust-item reveal" style="--d:160ms"><?= icon('scale', 'icon') ?><div><strong>Policyholder advocates</strong><span>We never work for insurers</span></div></div>
    <div class="trust-item reveal" style="--d:240ms"><?= icon('doc', 'icon') ?><div><strong>Transparent fees</strong><span>Written contract; capped at 10% by Texas law</span></div></div>
  </div>
</section>

<section class="section" aria-labelledby="why-h">
  <div class="container split">
    <div class="split-media reveal-left">
      <?= img('/wp-content/uploads/2026/04/Roof-Hail-Damage-Insurance-Claim-McAllen-3.webp', 'Public adjuster documenting hail damage on a McAllen home roof', ['sizes' => '(max-width: 900px) 100vw, 560px']) ?>
      <div class="media-badge">Working for policyholders<small>Not insurance companies</small></div>
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Why choose us</p>
      <h2 id="why-h">Why Choose McAllen Public Adjuster?</h2>
      <p>After a loss, your insurance company has its own adjusters, estimators, and engineers. Their job is to evaluate the claim for the insurer. A licensed public adjuster is the only claim professional who works for <em>you</em>&mdash;the policyholder.</p>
      <p>McAllen Public Adjuster helps Rio Grande Valley property owners understand their policy, document the full scope of damage, and present a clear, well-supported claim.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> <span><strong>Policy review</strong> &mdash; coverages, deductibles, exclusions, and deadlines explained in plain English.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Thorough documentation</strong> &mdash; photos, measurements, and line-item estimates of visible and hidden damage.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Estimate review</strong> &mdash; we compare the insurer's estimate with what the repairs actually require.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Communication handled</strong> &mdash; we work with the insurer's adjuster through settlement.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Honest guidance</strong> &mdash; if we don't think we can help, we'll tell you.</span></li>
      </ul>
      <a class="btn btn-navy" href="/about-us/">About our approach</a>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="services-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Our services</p>
      <h2 id="services-h">Insurance Claim Services in McAllen</h2>
      <p>From hail-damaged roofs to fire, water, and commercial losses, our McAllen public adjusters handle residential and commercial property insurance claims across Hidalgo County.</p>
    </div>
    <?php component('services-grid', ['limit' => 8]); ?>
    <p class="center" style="margin-top:30px"><a class="btn btn-ghost" href="/services/">View all 16 claim services</a></p>
  </div>
</section>

<section class="section" id="free-claim-review" aria-labelledby="fcr-h">
  <div class="container split split-form">
    <div class="reveal-left">
      <p class="eyebrow">Free Claim Review</p>
      <h2 id="fcr-h">Request Your Free Claim Review</h2>
      <p class="lead">Whether you haven't filed yet, your claim was denied, or the insurer's offer won't cover repairs, a McAllen Public Adjuster can review your situation at no cost.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> Review of your policy, the insurer's estimate, and any denial letter</li>
        <li><?= icon('check', 'icon') ?> Plain-English explanation of options and next steps</li>
        <li><?= icon('check', 'icon') ?> Upload photos or documents securely (optional)</li>
        <li><?= icon('check', 'icon') ?> No obligation to hire us</li>
      </ul>
      <p>Prefer to talk? Call <a href="<?= e(tel_link()) ?>"><strong><?= e(cfg('phone_display')) ?></strong></a> or email <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a>.</p>
    </div>
    <div class="form-card reveal-right">
      <p class="form-card-title h3" style="font-family:var(--font-head);font-weight:700;color:var(--navy);font-size:1.35rem">Tell us about your claim</p>
      <?php component('claim-form', ['context' => 'Homepage form']); ?>
    </div>
  </div>
</section>

<section class="section section-navy" aria-labelledby="storm-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow eyebrow-gold">Local weather risks</p>
      <h2 id="storm-h">Storm Damage in McAllen and the Rio Grande Valley</h2>
      <p>Hidalgo County sees large hail, damaging straight-line winds, tropical systems, flash flooding, and the occasional hard freeze. Here is what the official NOAA record shows.</p>
    </div>
    <div class="stats">
      <div class="stat reveal"><span class="stat-num" data-count="<?= (int) $stats['hail'] ?>">0</span><span class="stat-label">hail reports in Hidalgo County since <?= (int) ($stats['hail_first'] ?? $stats['first_year']) ?></span></div>
      <div class="stat reveal" style="--d:80ms"><span class="stat-num" data-count="<?= (int) $stats['hail_175'] ?>">0</span><span class="stat-label">reports of golf-ball-size (1.75&quot;) hail or larger</span></div>
      <div class="stat reveal" style="--d:160ms"><span class="stat-num" data-count="<?= (int) $stats['wind'] ?>">0</span><span class="stat-label">thunderstorm wind reports</span></div>
      <div class="stat reveal" style="--d:240ms"><span class="stat-num" data-count="<?= e((string) $stats['max_hail']) ?>" data-suffix="&quot;">0</span><span class="stat-label">largest hail reported (<?= e(date('M Y', strtotime($stats['max_hail_ev']['date'] ?? 'now'))) ?>, <?= e($stats['max_hail_ev']['loc'] ?? 'McAllen') ?>)</span></div>
    </div>
    <p class="stat-source center" style="margin-top:14px">Source: <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA NCEI Storm Events Database</a>, Hidalgo County, TX. Counts are individual reports, not storm days.</p>
    <div class="card-grid card-grid-3" style="margin-top:40px">
      <div class="tool-card reveal"><span class="tool-card-icon"><?= icon('hail', 'icon') ?></span><span class="tool-card-title">Hail season peaks April&ndash;May</span><span class="tool-card-text">Most Hidalgo County hail reports fall in April and May. Recent damaging events include April 21, 2023 and May 8, 2025 in north McAllen.</span></div>
      <div class="tool-card reveal" style="--d:80ms"><span class="tool-card-icon"><?= icon('wind', 'icon') ?></span><span class="tool-card-title">Damaging straight-line winds</span><span class="tool-card-text">NWS surveys after the April 28, 2023 storm found shingles stripped and roofs damaged across McAllen, Mission, Pharr, and Edinburg.</span></div>
      <div class="tool-card reveal" style="--d:160ms"><span class="tool-card-icon"><?= icon('hurricane', 'icon') ?></span><span class="tool-card-title">Tropical systems &amp; flooding</span><span class="tool-card-text">Hurricane Dolly (2008) and Hurricane Hanna (2020) brought wind damage and heavy flooding to the Valley. Flood needs separate coverage.</span></div>
    </div>
    <p class="center" style="margin-top:30px"><a class="btn btn-gold" href="/storm-history/">Explore McAllen storm history</a> <a class="btn btn-outline-light" href="/storm-lookup/">Look up storms near you</a></p>
  </div>
</section>

<section class="section section-alt" aria-labelledby="wx-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0">Live weather</p><h2 id="wx-h" class="mb-0">McAllen Weather Right Now</h2></div>
      <a class="btn btn-ghost btn-sm" href="/weather/">Full forecast &amp; alerts</a>
    </div>
    <?php if ($alertCount): ?>
    <div class="notice notice-error"><strong><?= icon('alert', 'icon icon-sm') ?> <?= $alertCount ?> active National Weather Service alert<?= $alertCount > 1 ? 's' : '' ?> for McAllen:</strong> <?= e(implode(', ', array_unique(array_column($al['data'], 'event')))) ?>. <a href="/weather/">See details</a>.</div>
    <?php endif; ?>
    <div class="wx-grid">
      <?php component('weather-now', ['cur' => $cur, 'mini' => true]); ?>
      <div>
        <h3>7-day forecast</h3>
        <?php component('weather-forecast', ['fc' => $fc]); ?>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="events-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0">Recent weather events</p><h2 id="events-h" class="mb-0">Latest Storm Reports in Hidalgo County</h2></div>
      <a class="btn btn-ghost btn-sm" href="/weather-events/">All weather events</a>
    </div>
    <?php if ($recentEvents): ?>
    <div class="event-list"><?php foreach ($recentEvents as $ev) component('event-card', ['ev' => $ev]); ?></div>
    <?php else: ?>
    <p class="muted">No recent storm reports are on file. New National Weather Service reports appear here automatically.</p>
    <?php endif; ?>
    <p class="small muted" style="margin-top:14px">Preliminary National Weather Service Local Storm Reports. A nearby report does not prove damage at a specific property.</p>
    <?php component('cta-storm'); ?>
  </div>
</section>

<section class="section section-gray" aria-labelledby="process-h">
  <div class="container split" style="align-items:start">
    <div class="reveal-left">
      <p class="eyebrow">How it works</p>
      <h2 id="process-h">How the Claims Process Works</h2>
      <p>Every claim is different, but the path is consistent and transparent. We stay involved from the first conversation until the claim is resolved.</p>
      <p>Texas requires public adjusters to use a written, TDI-compliant contract that states <strong>&ldquo;We represent the insured only,&rdquo;</strong> gives you 72 hours to cancel, and caps compensation at 10% of the settlement.</p>
      <a class="btn btn-gold" href="/free-claim-review/">Start with a Free Claim Review</a>
    </div>
    <ol class="timeline">
      <li><div class="timeline-card"><h3>Initial consultation</h3><p>We review what happened and explain your options&mdash;free.</p></div></li>
      <li><div class="timeline-card"><h3>Property inspection</h3><p>A detailed assessment of damage, including areas that are easy to miss.</p></div></li>
      <li><div class="timeline-card"><h3>Policy analysis</h3><p>We identify applicable coverages, limits, deductibles, and exclusions.</p></div></li>
      <li><div class="timeline-card"><h3>Claim preparation</h3><p>Photos, measurements, and a line-item estimate that documents the loss.</p></div></li>
      <li><div class="timeline-card"><h3>Negotiation</h3><p>We communicate directly with the insurance company on your behalf.</p></div></li>
      <li><div class="timeline-card"><h3>Resolution</h3><p>Support through settlement, supplements, and final claim closure.</p></div></li>
    </ol>
  </div>
</section>

<section class="section section-navy" aria-labelledby="tools-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow eyebrow-gold">Free resources</p>
      <h2 id="tools-h">Insurance Claim Tools</h2>
      <p>Practical, free tools built for Rio Grande Valley property owners. They run in your browser and use official NOAA and National Weather Service data.</p>
    </div>
    <?php component('tools-grid'); ?>
  </div>
</section>

<section class="section" aria-labelledby="codes-h">
  <div class="container split">
    <div class="reveal-left">
      <p class="eyebrow">Local building codes</p>
      <h2 id="codes-h">McAllen Building Codes and Your Repairs</h2>
      <p>The City of McAllen adopted the <strong>2024 International Code Council (ICC) codes</strong>&mdash;including the International Residential Code and International Building Code&mdash;effective <strong>January 1, 2026</strong>. Roof replacements and many repairs require permits and inspections through the city's Building Permits &amp; Inspections department.</p>
      <p>Code-required work can raise repair costs. Whether your insurer pays for it depends on your policy, often through <em>ordinance or law</em> coverage. Code requirements alone don't create coverage.</p>
      <a class="btn btn-navy" href="/local-building-codes/">McAllen building code guide</a>
    </div>
    <div class="reveal-right">
      <div class="table-wrap"><table class="code-table">
        <thead><tr><th scope="col">Topic</th><th scope="col">What to know</th></tr></thead>
        <tbody>
          <tr><td>Codes</td><td>2024 IRC / IBC / IEBC / IECC; 2023 NEC (effective Jan 1, 2026)</td></tr>
          <tr><td>Permits</td><td>Re-roofing and most structural repairs need a city permit</td></tr>
          <tr><td>Inspections</td><td>Requested through the city; re-inspections carry a fee</td></tr>
          <tr><td>Insurance</td><td>Code upgrades may be covered by ordinance or law coverage, up to its limit</td></tr>
        </tbody></table></div>
      <p class="small muted">Verified October 3, 2026 from City of McAllen sources. Confirm requirements with the city before starting work.</p>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="who-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Who we help</p>
      <h2 id="who-h">Residential and Commercial Policyholders</h2>
    </div>
    <div class="card-grid card-grid-3">
      <div class="feature reveal"><div class="feature-icon"><?= icon('home', 'icon') ?></div><h3>Homeowners</h3><p>Roof and hail damage, wind and storm damage, water leaks and burst pipes, fire and smoke, and contents claims for single-family homes.</p><p style="margin-top:12px"><a href="/services/residential-property-claims/">Residential claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:80ms"><div class="feature-icon"><?= icon('building', 'icon') ?></div><h3>Business owners</h3><p>Retail, office, warehouse, and industrial properties&mdash;including business income, equipment, and inventory losses.</p><p style="margin-top:12px"><a href="/services/commercial-property-claims/">Commercial claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:160ms"><div class="feature-icon"><?= icon('layers', 'icon') ?></div><h3>Landlords, HOAs &amp; multifamily</h3><p>Apartment complexes, condominium and HOA properties, and rental homes with owner and tenant coverage questions.</p><p style="margin-top:12px"><a href="/services/">All services &rarr;</a></p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="joseph-h">
  <div class="container split">
    <div class="reveal-left" style="text-align:center">
      <img src="/assets/img/joseph-dittman.webp" alt="Joseph Dittman, Texas public adjuster" width="320" height="320" loading="lazy" decoding="async" style="border-radius:50%;border:6px solid var(--gold);box-shadow:var(--shadow-lg);margin:0 auto;width:min(320px,80%);height:auto">
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Meet the author</p>
      <h2 id="joseph-h">About Joseph Dittman</h2>
      <p>Joseph Dittman is a Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness. His background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience.</p>
      <p>He writes and reviews the guides on this site, covering residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses, so McAllen Public Adjuster readers get practical information grounded in Texas claim experience.</p>
      <a class="btn btn-navy" href="/author/joseph-dittman/">Read Joseph's profile</a>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="blog-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0">Insurance claim guides</p><h2 id="blog-h" class="mb-0">Latest Blog Articles</h2></div>
      <a class="btn btn-ghost btn-sm" href="/blog/">View all articles</a>
    </div>
    <div class="card-grid card-grid-posts"><?php foreach ($posts as $post) component('post-card', ['post' => $post]); ?></div>
  </div>
</section>

<section class="section" aria-labelledby="faq-heading-home">
  <div class="container narrow">
    <?php component('faq', ['faqs' => $page['faqs'] ?? [], 'heading' => 'McAllen Public Adjuster FAQs', 'id' => 'home']); ?>
  </div>
</section>

<section class="section section-navy" aria-labelledby="final-h">
  <div class="container narrow center reveal">
    <p class="eyebrow eyebrow-gold">Free Claim Review</p>
    <h2 id="final-h">Talk With a McAllen Public Adjuster Today</h2>
    <p>Insurance policies have deadlines, and evidence fades after a storm. If your property in McAllen, Mission, Edinburg, Pharr, or anywhere in Hidalgo County was damaged, start with a free, no-obligation review.</p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn btn-gold btn-lg" href="/free-claim-review/">Get a Free Claim Review</a>
      <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_display')) ?></a>
    </div>
    <p class="small" style="margin-top:18px;color:#9fb2c4">Email: <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a> &middot; Serving McAllen, Hidalgo County, and surrounding Rio Grande Valley communities.</p>
  </div>
</section>
