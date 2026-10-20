<?php
/** Homepage. The keyword "San Antonio Public Adjuster" is used naturally across sections. */
require_once MPA_ROOT . '/includes/weather.php';
require_once MPA_ROOT . '/includes/storms.php';
$cur = weather_current();
$fc = weather_forecast();
$al = weather_alerts();
$stats = storm_stats();
$recentEvents = array_slice(weather_events_data()['events'] ?? [], 0, 3);
$posts = array_slice(all_content('posts'), 0, 6);
$alertCount = is_array($al['data'] ?? null) ? count($al['data']) : 0;
$ticker = [
    ['hail', 'Hail damage claims'], ['wind', 'Wind & downburst damage'], ['droplets', 'Flash flood losses'],
    ['thermo', 'Freeze & burst pipes'], ['fire', 'Fire & smoke damage'], ['x-doc', 'Denied claims reviewed'],
    ['dollar', 'Underpaid claims'], ['layers', 'Claim supplements'], ['scale', 'Insurance appraisal'], ['building', 'Commercial property'],
];
?>
<section class="hero" aria-labelledby="hero-h">
  <div class="hero-bg" aria-hidden="true" data-parallax>
    <?= img('/wp-content/uploads/2026/03/Property-Damage-Adjuster.webp', '', ['eager' => true, 'sizes' => '100vw']) ?>
  </div>
  <div class="hero-orbs" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="hero-grain" aria-hidden="true"></div>
  <div class="container hero-inner">
    <div>
      <p class="hero-pill hero-anim"><b>TDI #<?= e(cfg('license')) ?></b> Licensed Texas public adjusting &middot; Bexar County</p>
      <h1 id="hero-h" class="hero-anim" style="--d:80ms">San Antonio Public Adjuster <span class="accent text-gradient">Your Advocate After Hail, Wind, Flood, Freeze &amp; Fire Damage</span></h1>
      <p class="hero-text hero-anim" style="--d:160ms">Your insurance company has its own adjusters. San Antonio Public Adjuster works only for you, the policyholder: we read your policy, document every part of the damage, review the insurer&rsquo;s estimate line by line, and handle the back-and-forth until your claim is resolved.</p>
      <div class="hero-actions hero-anim" style="--d:240ms">
        <a class="btn btn-gold btn-lg btn-pulse" href="#free-claim-review">Get a Free Claim Review</a>
        <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> Call <?= e(cfg('phone_short')) ?></a>
      </div>
      <ul class="hero-badges hero-anim" style="--d:320ms">
        <li><?= icon('shield', 'icon') ?> We represent the insured only</li>
        <li><?= icon('home', 'icon') ?> Homes, businesses &amp; HOAs</li>
        <li><?= icon('map', 'icon') ?> San Antonio &amp; Bexar County</li>
      </ul>
    </div>
    <div class="hero-card hero-anim" style="--d:300ms" data-tilt>
      <h2>Free Claim Review</h2>
      <p>Tell us what happened. A licensed public adjuster will review your situation and explain your options. No cost, no obligation.</p>
      <?php component('claim-form', ['context' => 'Homepage hero', 'compact' => true]); ?>
    </div>
  </div>
  <div class="hero-scroll" aria-hidden="true"></div>
</section>

<div class="ticker" aria-hidden="true">
  <div class="ticker-track">
    <?php for ($r = 0; $r < 2; $r++): foreach ($ticker as [$ic, $label]): ?>
    <span class="ticker-item"><?= icon($ic, 'icon icon-sm') ?> <?= e($label) ?></span>
    <?php endforeach; endfor; ?>
  </div>
</div>

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
      <?= img('/wp-content/uploads/2026/04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-Xactimate-Insights-3.webp', 'Public adjuster reviewing hail damage findings on a tablet with a San Antonio homeowner', ['sizes' => '(max-width: 900px) 100vw, 560px']) ?>
      <div class="media-badge">Working for policyholders<small>Not insurance companies</small></div>
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Why choose us</p>
      <h2 id="why-h">Why Choose San Antonio Public Adjuster?</h2>
      <p>After a loss, your insurer sends its own adjuster, and sometimes an engineer or estimator. Their job is to evaluate the claim for the insurance company. A licensed public adjuster is the only claim professional who works for <em>you</em>.</p>
      <p>San Antonio Public Adjuster helps homeowners and business owners across Bexar County understand their coverage, document the full scope of damage, and present a clear, well-supported claim, so decisions are based on complete information instead of a rushed first inspection.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> <span><strong>Policy review</strong> &mdash; coverages, deductibles, exclusions, and deadlines explained in plain English.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Thorough documentation</strong> &mdash; photos, measurements, and Xactimate line-item estimates of visible and hidden damage.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Estimate review</strong> &mdash; we compare the insurer&rsquo;s estimate with what repairs actually require in San Antonio.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Communication handled</strong> &mdash; we work with the insurer&rsquo;s adjuster through settlement.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Honest guidance</strong> &mdash; if we don&rsquo;t think we can help, we&rsquo;ll tell you.</span></li>
      </ul>
      <a class="btn btn-navy" href="/about-us/">About our approach</a>
    </div>
  </div>
</section>

<section class="section section-gray" aria-labelledby="compare-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Know who works for whom</p>
      <h2 id="compare-h">Insurance Company Adjuster vs. a San Antonio Public Adjuster</h2>
      <p>Both may walk your roof and write an estimate. The difference is who they answer to.</p>
    </div>
    <div class="compare">
      <div class="compare-col reveal-left">
        <h3><?= icon('building', 'icon') ?> Insurance company adjuster</h3>
        <ul>
          <li><?= icon('arrow', 'icon icon-sm') ?> Hired and paid by the insurance company</li>
          <li><?= icon('arrow', 'icon icon-sm') ?> Often juggling many claims after a big storm</li>
          <li><?= icon('arrow', 'icon icon-sm') ?> Writes the scope the insurer reviews and pays from</li>
          <li><?= icon('arrow', 'icon icon-sm') ?> Interprets the policy on the insurer&rsquo;s behalf</li>
        </ul>
      </div>
      <div class="compare-col compare-us reveal-right">
        <h3><?= icon('shield', 'icon') ?> Your public adjuster</h3>
        <ul>
          <li><?= icon('check', 'icon icon-sm') ?> Hired by you; Texas contracts state &ldquo;We represent the insured only&rdquo;</li>
          <li><?= icon('check', 'icon icon-sm') ?> Focused on your property, your policy, and your claim file</li>
          <li><?= icon('check', 'icon icon-sm') ?> Documents hidden and secondary damage that is easy to miss</li>
          <li><?= icon('check', 'icon icon-sm') ?> Negotiates scope and pricing directly with the carrier</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="services-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Our services</p>
      <h2 id="services-h">Insurance Claim Services in San Antonio</h2>
      <p>From hail-damaged roofs in Helotes to flooded businesses near the San Antonio River, San Antonio Public Adjuster handles residential and commercial property insurance claims throughout Bexar County.</p>
    </div>
    <?php component('services-grid', ['limit' => 8]); ?>
    <p class="center" style="margin-top:30px"><a class="btn btn-ghost" href="/services/">View all <?= count(service_cards()) ?> claim services</a></p>
  </div>
</section>

<section class="section" id="free-claim-review" aria-labelledby="fcr-h">
  <div class="container split split-form">
    <div class="reveal-left">
      <p class="eyebrow">Free Claim Review</p>
      <h2 id="fcr-h">Request Your Free Claim Review</h2>
      <p class="lead">Haven&rsquo;t filed yet? Claim denied? Offer won&rsquo;t cover the repairs? A San Antonio Public Adjuster can review your situation at no cost and tell you honestly whether we can help.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> Review of your policy, the insurer&rsquo;s estimate, and any denial letter</li>
        <li><?= icon('check', 'icon') ?> Plain-English explanation of options and next steps</li>
        <li><?= icon('check', 'icon') ?> Upload photos or documents securely (optional)</li>
        <li><?= icon('check', 'icon') ?> No obligation to hire us</li>
      </ul>
      <p>Prefer to talk? Call <a href="<?= e(tel_link()) ?>"><strong><?= e(cfg('phone_display')) ?></strong></a> or email <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a>.</p>
      <div class="direct-card">
        <img src="/assets/img/joseph-dittman.webp" alt="Joseph Dittman, licensed Texas public adjuster" width="64" height="64" loading="lazy" decoding="async">
        <p><strong>Want to reach the adjuster directly?</strong><br>Email Joseph Dittman: <a href="mailto:<?= e(cfg('author_email')) ?>"><?= e(cfg('author_email')) ?></a></p>
      </div>
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
      <h2 id="storm-h">Storm Damage in San Antonio and Bexar County</h2>
      <p>San Antonio sits where Hill Country storms meet Gulf moisture: large hail, damaging downbursts, flash flooding along the Balcones Escarpment, and the occasional hard freeze. Here is what the official NOAA record shows, and why a San Antonio Public Adjuster pays close attention to storm dates.</p>
    </div>
    <div class="stats">
      <div class="stat reveal"><span class="stat-num" data-count="<?= (int) $stats['hail'] ?>">0</span><span class="stat-label">hail reports in Bexar County since <?= (int) ($stats['hail_first'] ?? $stats['first_year']) ?></span></div>
      <div class="stat reveal" style="--d:80ms"><span class="stat-num" data-count="<?= (int) $stats['hail_175'] ?>">0</span><span class="stat-label">reports of golf-ball-size (1.75&quot;) hail or larger</span></div>
      <div class="stat reveal" style="--d:160ms"><span class="stat-num" data-count="<?= (int) $stats['flood'] ?>">0</span><span class="stat-label">flood and flash-flood reports</span></div>
      <div class="stat reveal" style="--d:240ms"><span class="stat-num" data-count="<?= e((string) $stats['max_hail']) ?>" data-suffix="&quot;">0</span><span class="stat-label">largest hail reported (<?= e(date('M Y', strtotime($stats['max_hail_ev']['date'] ?? 'now'))) ?>, <?= e($stats['max_hail_ev']['loc'] ?? 'San Antonio') ?>)</span></div>
    </div>
    <p class="stat-source center" style="margin-top:14px">Source: <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA NCEI Storm Events Database</a>, Bexar County, TX. Counts are individual reports, not storm days.</p>
    <div class="card-grid card-grid-3" style="margin-top:40px">
      <div class="tool-card reveal"><span class="tool-card-icon"><?= icon('hail', 'icon') ?></span><span class="tool-card-title">Hail season peaks March&ndash;May</span><span class="tool-card-text">April is the busiest hail month in Bexar County. The April 12, 2016 storm dropped hail up to 4.5&quot; across northwest San Antonio; on May 3, 2021, 5.5&quot; hail fell near China Grove.</span></div>
      <div class="tool-card reveal" style="--d:80ms"><span class="tool-card-icon"><?= icon('droplets', 'icon') ?></span><span class="tool-card-title">Flash Flood Alley</span><span class="tool-card-text">Heavy rain over the Balcones Escarpment makes Bexar County one of the most flash-flood-prone areas in the country. Flood needs its own policy, separate from homeowners coverage.</span></div>
      <div class="tool-card reveal" style="--d:160ms"><span class="tool-card-icon"><?= icon('thermo', 'icon') ?></span><span class="tool-card-title">Freezes &amp; ice storms</span><span class="tool-card-text">Winter Storm Uri (February 2021) brought wind chills near &minus;5&deg;F and widespread burst pipes. Ice storms followed in 2022, 2025, and January 2026.</span></div>
    </div>
    <p class="center" style="margin-top:30px"><a class="btn btn-gold" href="/storm-history/">Explore San Antonio storm history</a> <a class="btn btn-outline-light" href="/storm-lookup/">Look up storms near you</a></p>
  </div>
</section>

<section class="section section-alt" aria-labelledby="wx-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0"><span class="live-dot" aria-hidden="true"></span> Live weather</p><h2 id="wx-h" class="mb-0">San Antonio Weather Right Now</h2></div>
      <a class="btn btn-ghost btn-sm" href="/weather/">Full forecast &amp; alerts</a>
    </div>
    <?php if ($alertCount): ?>
    <div class="notice notice-error"><strong><?= icon('alert', 'icon icon-sm') ?> <?= $alertCount ?> active National Weather Service alert<?= $alertCount > 1 ? 's' : '' ?> for San Antonio:</strong> <?= e(implode(', ', array_unique(array_column($al['data'], 'event')))) ?>. <a href="/weather/">See details</a>.</div>
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
      <div><p class="eyebrow mb-0">Recent weather events</p><h2 id="events-h" class="mb-0">Latest Storm Reports in Bexar County</h2></div>
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
      <p>Every claim is different, but the path with San Antonio Public Adjuster is consistent and transparent. We stay involved from the first conversation until the claim is resolved.</p>
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
      <h2 id="tools-h">Insurance Claim Tools &amp; Live Weather</h2>
      <p>Free tools from San Antonio Public Adjuster that run in your browser and use official NOAA and National Weather Service data: estimate a settlement, organize your documentation, and check which storms hit your neighborhood.</p>
    </div>
    <?php component('tools-grid'); ?>
  </div>
</section>

<section class="section" aria-labelledby="codes-h">
  <div class="container split">
    <div class="reveal-left">
      <p class="eyebrow">Local building codes</p>
      <h2 id="codes-h">San Antonio Building Codes and Your Repairs</h2>
      <p>Roof replacements and many structural repairs inside San Antonio city limits require permits and inspections through the City of San Antonio <strong>Development Services Department</strong>. Suburban cities such as Alamo Heights, Leon Valley, and Schertz run their own permit offices.</p>
      <p>Code-required work can raise repair costs. Whether your insurer pays for it depends on your policy, usually through <em>ordinance or law</em> coverage, which often has its own limit. Code requirements alone don&rsquo;t create coverage.</p>
      <a class="btn btn-navy" href="/local-building-codes/">San Antonio building code guide</a>
    </div>
    <div class="reveal-right">
      <div class="table-wrap"><table class="code-table">
        <thead><tr><th scope="col">Topic</th><th scope="col">What to know</th></tr></thead>
        <tbody>
          <tr><td>Permits</td><td>City of San Antonio Development Services (inside city limits)</td></tr>
          <tr><td>Suburbs</td><td>Each incorporated city has its own building office</td></tr>
          <tr><td>Inspections</td><td>Scheduled through the permitting office after work begins</td></tr>
          <tr><td>Insurance</td><td>Code upgrades may be covered by ordinance or law coverage, up to its limit</td></tr>
        </tbody></table></div>
      <p class="small muted">Confirm current requirements with the permitting office before starting work.</p>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="who-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Who we help</p>
      <h2 id="who-h">Residential and Commercial Policyholders</h2>
      <p>San Antonio Public Adjuster represents homeowners, landlords, and businesses from the Medical Center to Stone Oak, and across the surrounding cities.</p>
    </div>
    <div class="bento">
      <div class="bento-card bento-wide reveal"><div class="feature-icon"><?= icon('home', 'icon') ?></div><h3>Homeowners</h3><p>Roof and hail damage, wind and storm damage, water leaks and burst pipes, fire and smoke, and contents claims for single-family homes&mdash;from 1920s bungalows in historic districts to newer subdivisions on the North Side.</p><p style="margin-top:12px"><a href="/services/residential-property-claims/">Residential claims &rarr;</a></p></div>
      <div class="bento-card bento-dark reveal" style="--d:80ms"><div class="bento-num text-gradient">10%</div><h3>Fee cap by Texas law</h3><p>Fees are disclosed in a written contract before any work begins.</p></div>
      <div class="bento-card reveal" style="--d:120ms"><div class="feature-icon"><?= icon('building', 'icon') ?></div><h3>Business owners</h3><p>Retail, office, warehouse, and industrial properties, including business income, equipment, and inventory.</p><p style="margin-top:12px"><a href="/services/commercial-property-claims/">Commercial claims &rarr;</a></p></div>
      <div class="bento-card reveal" style="--d:160ms"><div class="feature-icon"><?= icon('layers', 'icon') ?></div><h3>Landlords, HOAs &amp; multifamily</h3><p>Apartment complexes, condominium and HOA properties, and rental homes.</p><p style="margin-top:12px"><a href="/services/">All services &rarr;</a></p></div>
      <div class="bento-card bento-dark reveal" style="--d:200ms"><div class="bento-num text-gradient">72 hrs</div><h3>To cancel your contract</h3><p>Texas gives you 72 hours after signing to rescind a public adjuster contract.</p></div>
    </div>
    <div class="chip-list chip-list-center">
      <?php foreach (service_area_links() as [$l, $h]): ?><a class="chip" href="<?= e($h) ?>"><?= e($l) ?></a><?php endforeach; ?>
      <a class="chip" href="/service-areas/">All areas &rarr;</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="joseph-h">
  <div class="container split">
    <div class="reveal-left" style="text-align:center">
      <img src="/assets/img/joseph-dittman.webp" alt="Joseph Dittman, licensed Texas public adjuster" width="320" height="320" loading="lazy" decoding="async" style="border-radius:50%;border:6px solid var(--gold);box-shadow:var(--shadow-lg);margin:0 auto;width:min(320px,80%);height:auto">
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Meet your public adjuster</p>
      <h2 id="joseph-h">Joseph Dittman, Licensed Texas Public Adjuster</h2>
      <p>Joseph Dittman is a Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness. His background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience.</p>
      <p>He writes and reviews the guides on this site, covering residential, commercial, storm, hail, wind, water, fire, and catastrophe losses, so San Antonio Public Adjuster readers get practical information grounded in Texas claim experience.</p>
      <p><?= icon('mail', 'icon icon-sm') ?> Contact Joseph directly: <a href="mailto:<?= e(cfg('author_email')) ?>"><strong><?= e(cfg('author_email')) ?></strong></a></p>
      <a class="btn btn-navy" href="/author/joseph-dittman/">Read Joseph&rsquo;s profile</a>
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
    <?php component('faq', ['faqs' => $page['faqs'] ?? [], 'heading' => 'San Antonio Public Adjuster FAQs', 'id' => 'home']); ?>
    <p class="center" style="margin-top:24px"><a class="btn btn-ghost" href="/faq/">More questions answered</a></p>
  </div>
</section>

<section class="section section-navy" aria-labelledby="final-h">
  <div class="container narrow center reveal">
    <p class="eyebrow eyebrow-gold">Free Claim Review</p>
    <h2 id="final-h">Talk With a San Antonio Public Adjuster Today</h2>
    <p>Insurance policies have deadlines, and evidence fades after a storm. If your property in San Antonio, Helotes, Leon Valley, Converse, Schertz, or anywhere in Bexar County was damaged, start with a free, no-obligation review from San Antonio Public Adjuster.</p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn btn-gold btn-lg" href="/free-claim-review/">Get a Free Claim Review</a>
      <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_display')) ?></a>
    </div>
    <p class="small" style="margin-top:18px;color:#c9c6b8">Email: <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a> &middot; Joseph Dittman direct: <a href="mailto:<?= e(cfg('author_email')) ?>"><?= e(cfg('author_email')) ?></a></p>
  </div>
</section>
