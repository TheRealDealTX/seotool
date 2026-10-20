<?php
/** Homepage. Keyword "Port Arthur Public Adjuster" is used naturally across sections (14+ times). */
require_once MPA_ROOT . '/includes/weather.php';
require_once MPA_ROOT . '/includes/storms.php';
require_once MPA_ROOT . '/includes/tropics.php';
$cur = weather_current();
$fc = weather_forecast();
$al = weather_alerts();
$tr = tropics_current();
$season = hurricane_season();
$atl = array_values(array_filter($tr['data'] ?? [], fn($s) => $s['basin'] === 'al'));
$stats = storm_stats();
$recentEvents = array_slice(weather_events_data()['events'] ?? [], 0, 3);
$posts = array_slice(all_content('posts'), 0, 6);
$alertCount = is_array($al['data'] ?? null) ? count($al['data']) : 0;
$areas = ['Port Arthur', 'Beaumont', 'Nederland', 'Groves', 'Port Neches', 'Sabine Pass', 'Pleasure Island', 'Port Acres', 'Orange', 'Bridge City', 'Vidor', 'Hamshire', 'Fannett', 'China', 'Nome', 'Bevil Oaks'];
$wave = '<svg class="wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 46c120 26 240 38 360 30S600 30 720 22s240 6 360 22 240 26 360 14v32H0Z" fill="%s" opacity=".55"/><path d="M0 60c140 18 260 22 380 12S620 40 740 38s250 12 370 22 220 12 330 4v26H0Z" fill="%s"/></svg>';
?>
<section class="hero" aria-labelledby="hero-h">
  <div class="hero-bg" aria-hidden="true" data-parallax>
    <?= img('/assets/img/photos/adjuster-and-homeowner-roof-tarp.webp', '', ['eager' => true, 'sizes' => '100vw']) ?>
  </div>
  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="container hero-inner">
    <div>
      <p class="eyebrow eyebrow-gold hero-anim">Licensed Texas public adjusting &middot; TDI License #<?= e(cfg('license')) ?></p>
      <h1 id="hero-h" class="hero-anim" style="--d:80ms">Port Arthur Public Adjuster <span class="accent">Hurricane, Windstorm &amp; Property Claim Help for Southeast Texas</span></h1>
      <p class="hero-text hero-anim" style="--d:160ms">Hurricane damage, a TWIA windstorm claim, flooding, fire, or a denied insurance claim? Port Arthur Public Adjuster works for policyholders&mdash;never insurance companies&mdash;to document the full loss, review the insurer's estimate, and guide you through every step of the claim.</p>
      <div class="hero-actions hero-anim" style="--d:240ms">
        <a class="btn btn-gold btn-lg" href="#free-claim-review">Get a Free Claim Review</a>
        <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> Call <?= e(cfg('phone_short')) ?></a>
      </div>
      <ul class="hero-badges hero-anim" style="--d:320ms">
        <li><?= icon('shield', 'icon') ?> We represent the insured only</li>
        <li><?= icon('hurricane', 'icon') ?> Hurricane &amp; TWIA claims</li>
        <li><?= icon('map', 'icon') ?> Port Arthur &amp; Jefferson County</li>
      </ul>
      <a class="hero-live hero-anim" style="--d:400ms" href="/hurricane-tracker/">
        <span class="pulse-dot" aria-hidden="true"></span>
        <span><strong>Live tropics:</strong>
        <?php if ($tr === null): ?>Open the hurricane tracker
        <?php elseif ($atl): ?><?= count($atl) ?> active Atlantic system<?= count($atl) > 1 ? 's' : '' ?> &middot; closest <?= e($atl[0]['name']) ?>, <?= number_format($atl[0]['miles']) ?> mi away
        <?php else: ?>No active Atlantic storms<?= $season['in'] ? ' &middot; ' . (int) $season['days_left'] . ' days left in hurricane season' : '' ?>
        <?php endif; ?></span>
        <?= icon('arrow', 'icon icon-sm') ?>
      </a>
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

<div class="ticker" aria-label="Communities we serve">
  <div class="ticker-track">
    <?php for ($i = 0; $i < 2; $i++): foreach ($areas as $a): ?>
    <span class="ticker-item"<?= $i ? ' aria-hidden="true"' : '' ?>><?= icon('map', 'icon icon-sm') ?> <?= e($a) ?>, TX</span>
    <?php endforeach; endfor; ?>
  </div>
</div>

<section class="section section-dots" aria-labelledby="why-h">
  <div class="container split">
    <div class="split-media reveal-left">
      <?= img('/assets/img/photos/public-adjuster-roof-inspection-tarp.webp', 'Port Arthur Public Adjuster inspecting storm damage on a Southeast Texas roof', ['sizes' => '(max-width: 900px) 100vw, 560px']) ?>
      <div class="media-badge">Working for policyholders<small>Not insurance companies</small></div>
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Why choose us</p>
      <h2 id="why-h">Why Choose Port Arthur Public Adjuster?</h2>
      <p>After a hurricane or major loss, your insurance company sends its own adjusters, estimators, and sometimes engineers. Their job is to evaluate the claim for the insurer. A licensed public adjuster is the only claim professional who works for <em>you</em>&mdash;the policyholder.</p>
      <p>Port Arthur Public Adjuster helps homeowners, landlords, and business owners in Jefferson County understand their policies, document the full scope of damage, and present a clear, well-supported claim&mdash;whether it is with a standard carrier, TWIA, or a flood insurer.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> <span><strong>Policy review</strong> &mdash; coverages, deductibles, exclusions, and deadlines explained in plain English.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Thorough documentation</strong> &mdash; photos, measurements, moisture readings, and line-item estimates of visible and hidden damage.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Estimate review</strong> &mdash; we compare the insurer's estimate with what repairs actually require.</span></li>
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
      <h2 id="services-h">Insurance Claim Services in Port Arthur</h2>
      <p>From hurricane and windstorm losses to flood, fire, water, and commercial claims, our Port Arthur public adjusters handle residential and commercial property insurance claims across Jefferson County and the Golden Triangle.</p>
    </div>
    <?php component('services-grid', ['limit' => 8]); ?>
    <p class="center" style="margin-top:30px"><a class="btn btn-ghost" href="/services/">View all <?= count(service_cards()) ?> claim services</a></p>
  </div>
</section>

<section class="section" aria-labelledby="policies-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Coastal coverage, explained</p>
      <h2 id="policies-h">One Hurricane, Up to Three Insurance Claims</h2>
      <p>Jefferson County is a TWIA first-tier coastal county. Many Port Arthur homes carry a homeowners policy that excludes wind, a separate TWIA windstorm policy, and a flood policy. Each has its own adjuster, deductible, and rules.</p>
    </div>
    <div class="card-grid card-grid-3">
      <div class="feature reveal"><div class="feature-icon"><?= icon('home', 'icon') ?></div><h3>Homeowners or commercial policy</h3><p>Fire, theft, plumbing leaks, and&mdash;if wind is not excluded&mdash;wind and hail. Check the wind/hail or named-storm deductible on your declarations page.</p><p style="margin-top:12px"><a href="/services/residential-property-claims/">Residential claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:80ms"><div class="feature-icon"><?= icon('wind', 'icon') ?></div><h3>TWIA windstorm policy</h3><p>Wind and hail damage when your regular policy excludes it. Repairs, including re-roofs, need TDI windstorm inspection (WPI-8) to keep TWIA eligibility.</p><p style="margin-top:12px"><a href="/services/twia-windstorm-claims/">TWIA windstorm claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:160ms"><div class="feature-icon"><?= icon('water', 'icon') ?></div><h3>Flood policy (NFIP or private)</h3><p>Rising water and storm surge, which homeowners and TWIA policies exclude. Proof-of-loss deadlines are strict, so start documenting right away.</p><p style="margin-top:12px"><a href="/services/flood-damage-claims/">Flood damage claims &rarr;</a></p></div>
    </div>
    <p class="center" style="margin-top:28px">When wind and water damage overlap, insurers may disagree about which policy pays. A Port Arthur Public Adjuster documents the cause of each part of the loss so every applicable policy is considered. <a href="/wind-vs-flood-damage-port-arthur-insurance/">Read our wind vs. flood guide</a>.</p>
  </div>
</section>

<section class="section section-alt" id="free-claim-review" aria-labelledby="fcr-h">
  <div class="container split split-form">
    <div class="reveal-left">
      <p class="eyebrow">Free Claim Review</p>
      <h2 id="fcr-h">Request Your Free Claim Review</h2>
      <p class="lead">Whether you haven't filed yet, your claim was denied, or the insurer's offer won't cover repairs, a Port Arthur Public Adjuster can review your situation at no cost.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> Review of your policies, the insurer's estimate, and any denial letter</li>
        <li><?= icon('check', 'icon') ?> Plain-English explanation of options and next steps</li>
        <li><?= icon('check', 'icon') ?> Upload photos or documents securely (optional)</li>
        <li><?= icon('check', 'icon') ?> No obligation to hire us</li>
      </ul>
      <p>Prefer to talk? Call <a href="<?= e(tel_link()) ?>"><strong><?= e(cfg('phone_display')) ?></strong></a> or email <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a>.</p>
    </div>
    <div class="form-card glass-card reveal-right">
      <p class="form-card-title h3" style="font-family:var(--font-head);font-weight:700;color:var(--navy);font-size:1.35rem">Tell us about your claim</p>
      <?php component('claim-form', ['context' => 'Homepage form']); ?>
    </div>
  </div>
</section>

<section class="section section-navy" aria-labelledby="storm-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow eyebrow-gold">Local weather risks</p>
      <h2 id="storm-h">Storm Damage in Port Arthur and Jefferson County</h2>
      <p>The upper Texas coast sees hurricanes, storm surge, extreme rainfall, tornadoes, damaging thunderstorm winds, and hail. Here is what the official NOAA record shows for Jefferson County.</p>
    </div>
    <div class="stats">
      <div class="stat reveal"><span class="stat-num" data-count="<?= (int) $stats['wind'] ?>">0</span><span class="stat-label">thunderstorm wind reports since <?= (int) $stats['first_year'] ?></span></div>
      <div class="stat reveal" style="--d:80ms"><span class="stat-num" data-count="<?= (int) $stats['tornado'] ?>">0</span><span class="stat-label">tornado reports</span></div>
      <div class="stat reveal" style="--d:160ms"><span class="stat-num" data-count="<?= (int) $stats['flood'] ?>">0</span><span class="stat-label">flood and flash flood reports</span></div>
      <div class="stat reveal" style="--d:240ms"><span class="stat-num" data-count="<?= (int) $stats['hail'] ?>">0</span><span class="stat-label">hail reports (<?= (int) $stats['hail_175'] ?> golf-ball size or larger)</span></div>
    </div>
    <p class="stat-source center" style="margin-top:14px">Source: <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA NCEI Storm Events Database</a>, Jefferson County, TX. Counts are individual reports, not storm days.</p>
    <div class="card-grid card-grid-3" style="margin-top:40px">
      <div class="tool-card reveal"><span class="tool-card-icon"><?= icon('hurricane', 'icon') ?></span><span class="tool-card-title">Rita (2005) &amp; Ike (2008)</span><span class="tool-card-text">Rita's winds damaged homes across Southeast Texas. NOAA records a 14&ndash;15 foot storm surge at Sabine Pass during Ike, the highest water level ever recorded there.</span></div>
      <div class="tool-card reveal" style="--d:80ms"><span class="tool-card-icon"><?= icon('water', 'icon') ?></span><span class="tool-card-title">Harvey (2017) &amp; Imelda (2019)</span><span class="tool-card-text">NWS Lake Charles reports Harvey totals over 40 inches across the county, 60.58 inches near Nederland, and more than 64,000 Jefferson County homes flooded.</span></div>
      <div class="tool-card reveal" style="--d:160ms"><span class="tool-card-icon"><?= icon('wind', 'icon') ?></span><span class="tool-card-title">Laura &amp; Delta (2020)</span><span class="tool-card-text">Two hurricanes six weeks apart. During Delta, NOAA logged hurricane-force sustained winds at Sabine Pass and gusts near 90 mph at Jack Brooks Regional Airport.</span></div>
    </div>
    <p class="center" style="margin-top:30px"><a class="btn btn-gold" href="/storm-history/">Explore Port Arthur storm history</a> <a class="btn btn-outline-light" href="/storm-lookup/">Look up storms near you</a></p>
  </div>
</section>

<section class="section section-alt" aria-labelledby="wx-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0">Live weather</p><h2 id="wx-h" class="mb-0">Port Arthur Weather Right Now</h2></div>
      <div><a class="btn btn-ghost btn-sm" href="/weather/">Forecast, radar &amp; alerts</a> <a class="btn btn-navy btn-sm" href="/hurricane-tracker/"><?= icon('hurricane', 'icon icon-sm') ?> Hurricane tracker</a></div>
    </div>
    <?php if ($alertCount): ?>
    <div class="notice notice-error"><strong><?= icon('alert', 'icon icon-sm') ?> <?= $alertCount ?> active National Weather Service alert<?= $alertCount > 1 ? 's' : '' ?> for Port Arthur:</strong> <?= e(implode(', ', array_unique(array_column($al['data'], 'event')))) ?>. <a href="/weather/">See details</a>.</div>
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
      <div><p class="eyebrow mb-0">Recent weather events</p><h2 id="events-h" class="mb-0">Latest Storm Reports in Jefferson County</h2></div>
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
      <p>Every claim is different, but the path is consistent and transparent. When you hire Port Arthur Public Adjuster, we stay involved from the first conversation until the claim is resolved.</p>
      <p>Texas requires public adjusters to use a written, TDI-compliant contract that states <strong>&ldquo;We represent the insured only,&rdquo;</strong> gives you 72 hours to cancel, and caps compensation at 10% of the settlement.</p>
      <a class="btn btn-gold" href="/free-claim-review/">Start with a Free Claim Review</a>
    </div>
    <ol class="timeline">
      <li><div class="timeline-card"><h3>Initial consultation</h3><p>We review what happened and explain your options&mdash;free.</p></div></li>
      <li><div class="timeline-card"><h3>Property inspection</h3><p>A detailed assessment of damage, including areas that are easy to miss.</p></div></li>
      <li><div class="timeline-card"><h3>Policy analysis</h3><p>We identify applicable coverages, limits, deductibles, and exclusions across every policy.</p></div></li>
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
      <h2 id="tools-h">Insurance Claim Tools &amp; Weather Apps</h2>
      <p>Free tools built for Golden Triangle property owners. They run in your browser and use official National Hurricane Center, National Weather Service, and NOAA data.</p>
    </div>
    <?php component('tools-grid'); ?>
  </div>
</section>

<section class="section" aria-labelledby="codes-h">
  <div class="container split">
    <div class="reveal-left">
      <p class="eyebrow">Local building codes</p>
      <h2 id="codes-h">Port Arthur Building Codes and Your Repairs</h2>
      <p>The City of Port Arthur's Building Inspections Division operates under the <strong>2021 International Residential Code and International Building Code</strong>, the 2021 plumbing and mechanical codes, and the <strong>2020 National Electrical Code</strong>. In Jefferson County, repairs on TWIA-insured buildings also need <strong>TDI windstorm inspection</strong>.</p>
      <p>Code-required work can raise repair costs. Whether your insurer pays for it depends on your policy, often through <em>ordinance or law</em> coverage. A Port Arthur Public Adjuster checks whether code items belong in your claim.</p>
      <a class="btn btn-navy" href="/local-building-codes/">Port Arthur building code guide</a>
    </div>
    <div class="reveal-right">
      <div class="table-wrap"><table class="code-table">
        <thead><tr><th scope="col">Topic</th><th scope="col">What to know</th></tr></thead>
        <tbody>
          <tr><td>Codes</td><td>2021 IRC / IBC / IPC / IMC; 2020 NEC</td></tr>
          <tr><td>Permits</td><td>Re-roofing and most structural repairs need a city permit; permit techs (409) 983-8261</td></tr>
          <tr><td>Windstorm</td><td>TDI inspection and WPI-8 certificate for TWIA eligibility, including re-roofs</td></tr>
          <tr><td>Insurance</td><td>Code upgrades may be covered by ordinance or law coverage, up to its limit</td></tr>
        </tbody></table></div>
      <p class="small muted">Verified October 20, 2026 from City of Port Arthur and Texas Department of Insurance sources. Confirm requirements before starting work.</p>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="who-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Who we help</p>
      <h2 id="who-h">Residential and Commercial Policyholders</h2>
      <p>Port Arthur Public Adjuster works with property owners of every kind across the Golden Triangle.</p>
    </div>
    <div class="card-grid card-grid-3">
      <div class="feature reveal"><div class="feature-icon"><?= icon('home', 'icon') ?></div><h3>Homeowners</h3><p>Hurricane and wind damage, roof claims, flooding, water leaks and burst pipes, mold, fire and smoke, and contents claims.</p><p style="margin-top:12px"><a href="/services/residential-property-claims/">Residential claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:80ms"><div class="feature-icon"><?= icon('building', 'icon') ?></div><h3>Business owners</h3><p>Retail, office, warehouse, marine, and industrial-area properties&mdash;including business income, equipment, and inventory losses.</p><p style="margin-top:12px"><a href="/services/commercial-property-claims/">Commercial claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:160ms"><div class="feature-icon"><?= icon('layers', 'icon') ?></div><h3>Landlords, HOAs &amp; multifamily</h3><p>Apartment complexes, condominium and HOA properties, and rental homes with owner and tenant coverage questions.</p><p style="margin-top:12px"><a href="/services/">All services &rarr;</a></p></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="joseph-h">
  <div class="container split">
    <div class="reveal-left" style="text-align:center">
      <img src="/assets/img/joseph-dittman.webp" alt="Joseph Dittman, licensed Texas public adjuster" width="320" height="320" loading="lazy" decoding="async" style="border-radius:50%;border:6px solid var(--gold);box-shadow:var(--shadow-lg),var(--glow);margin:0 auto;width:min(320px,80%);height:auto">
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Meet the author</p>
      <h2 id="joseph-h">About Joseph Dittman, Licensed Public Adjuster</h2>
      <p>Joseph Dittman is a licensed Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness. His background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience.</p>
      <p>He writes and reviews the guides on this site, covering residential, commercial, storm, wind, water, fire, hurricane, and catastrophe losses, so Port Arthur Public Adjuster readers get practical information grounded in Texas claim experience.</p>
      <a class="btn btn-navy" href="/author/joseph-dittman/">Read Joseph's profile</a>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="blog-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0">Insurance claim guides</p><h2 id="blog-h" class="mb-0">Latest From the Port Arthur Public Adjuster Blog</h2></div>
      <a class="btn btn-ghost btn-sm" href="/blog/">View all articles</a>
    </div>
    <div class="card-grid card-grid-posts"><?php foreach ($posts as $post) component('post-card', ['post' => $post]); ?></div>
  </div>
</section>

<section class="section" aria-labelledby="faq-heading-home">
  <div class="container narrow">
    <?php component('faq', ['faqs' => $page['faqs'] ?? [], 'heading' => 'Port Arthur Public Adjuster FAQs', 'id' => 'home']); ?>
    <p class="center" style="margin-top:22px"><a class="btn btn-ghost btn-sm" href="/faq/">More questions answered</a></p>
  </div>
</section>

<section class="section section-navy" aria-labelledby="final-h">
  <div class="container narrow center reveal">
    <p class="eyebrow eyebrow-gold">Free Claim Review</p>
    <h2 id="final-h">Talk With a Port Arthur Public Adjuster Today</h2>
    <p>Insurance policies have deadlines, and evidence fades after a storm. If your property in Port Arthur, Beaumont, Nederland, Groves, Port Neches, Sabine Pass, or anywhere in Jefferson County was damaged, start with a free, no-obligation review.</p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn btn-gold btn-lg" href="/free-claim-review/">Get a Free Claim Review</a>
      <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_display')) ?></a>
    </div>
    <p class="small" style="margin-top:18px;color:#a3b8b3">Email: <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a> &middot; Serving <?= e(cfg('service_area')) ?>.</p>
  </div>
</section>
