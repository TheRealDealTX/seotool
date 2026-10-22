<?php
/**
 * Homepage. The main keyword "Corpus Christi Public Adjuster" appears naturally
 * throughout the visible copy (hero, section headings, body text, FAQs, final CTA).
 */
require_once CCPA_ROOT . '/includes/weather.php';
require_once CCPA_ROOT . '/includes/storms.php';
$cur = weather_current();
$fc = weather_forecast();
$al = weather_alerts();
$stats = storm_stats(cfg('county_name'));
$recentEvents = array_slice(weather_events_data()['events'] ?? [], 0, 3);
$posts = array_slice(all_content('posts'), 0, 6);
$alertCount = is_array($al['data'] ?? null) ? count($al['data']) : 0;
$curTemp = $cur['data']['temp_f'] ?? null;
$marquee = [
    ['hurricane', 'Hurricane claims'], ['shield', 'TWIA windstorm claims'], ['wind', 'Wind damage'], ['hail', 'Hail damage'],
    ['droplets', 'Flood & storm surge'], ['water', 'Burst pipes & leaks'], ['fire', 'Fire & smoke'], ['building', 'Commercial property'],
    ['x-doc', 'Denied claims'], ['dollar', 'Underpaid claims'], ['layers', 'Supplements'], ['scale', 'Appraisal'],
];
?>
<section class="hero" aria-labelledby="hero-h">
  <div class="hero-bg" aria-hidden="true" data-parallax>
    <?= img('/wp-content/uploads/2026/04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-3.webp', '', ['eager' => true, 'sizes' => '100vw']) ?>
  </div>
  <?php component('aurora'); ?>
  <div class="grid-overlay" aria-hidden="true"></div>
  <div class="container hero-inner">
    <div>
      <p class="eyebrow eyebrow-gold hero-anim">Licensed Texas public adjusting &middot; TDI License #<?= e(cfg('license')) ?></p>
      <h1 id="hero-h" data-words>Corpus Christi Public Adjuster <span class="accent">for hurricane, windstorm, hail, flood, and fire claims on the Coastal Bend</span></h1>
      <p class="hero-text hero-anim" style="--d:420ms">When a storm, fire, or leak damages your home or business, the insurance company already has its adjusters working on the claim. Corpus Christi Public Adjuster works for you: we read the policy, document every item of damage, and present a claim that reflects what the repairs actually cost.</p>
      <div class="hero-actions hero-anim" style="--d:520ms">
        <a class="btn btn-gold btn-lg" href="#free-claim-review">Get a Free Claim Review</a>
        <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> Call <?= e(cfg('phone_short')) ?></a>
      </div>
      <ul class="hero-badges hero-anim" style="--d:600ms">
        <li><?= icon('shield', 'icon') ?> We represent the policyholder only</li>
        <li><?= icon('home', 'icon') ?> Homes, rentals &amp; businesses</li>
        <li><?= icon('map', 'icon') ?> Nueces, San Patricio, Aransas &amp; Kleberg</li>
      </ul>
      <a class="hero-live hero-anim" style="--d:700ms" href="/weather/">
        <b><?= $curTemp !== null ? e(fmt_num($curTemp)) . '&deg;' : icon('thermo', 'icon icon-sm') ?></b>
        <span><?= $alertCount ? e($alertCount . ' active weather alert' . ($alertCount > 1 ? 's' : '') . ' for Corpus Christi') : 'Live Corpus Christi weather, radar &amp; tides' ?> &rarr;</span>
      </a>
    </div>
    <div class="hero-card hero-anim" style="--d:300ms">
      <span class="hero-card-badge">Free &middot; No obligation</span>
      <h2>Free Claim Review</h2>
      <p>Tell us what happened. A licensed public adjuster will review your situation and explain your options&mdash;at no cost.</p>
      <?php component('claim-form', ['context' => 'Homepage hero', 'compact' => true]); ?>
    </div>
  </div>
  <div class="hero-scroll" aria-hidden="true"></div>
  <?php component('waves'); ?>
</section>

<section class="trust-strip" aria-label="Credentials">
  <div class="container"><div class="trust-grid">
    <div class="trust-item reveal"><?= icon('shield', 'icon') ?><div><strong>TDI License #<?= e(cfg('license')) ?></strong><span>Texas Department of Insurance</span></div></div>
    <div class="trust-item reveal" style="--d:80ms"><?= icon('building', 'icon') ?><div><strong><?= e(cfg('company')) ?></strong><span>Licensed public adjusting firm</span></div></div>
    <div class="trust-item reveal" style="--d:160ms"><?= icon('scale', 'icon') ?><div><strong>Policyholder advocates</strong><span>We never work for insurers</span></div></div>
    <div class="trust-item reveal" style="--d:240ms"><?= icon('doc', 'icon') ?><div><strong>Transparent fees</strong><span>Written contract; capped at 10% by Texas law</span></div></div>
  </div></div>
</section>

<section class="section" aria-labelledby="why-h">
  <div class="container split">
    <div class="split-media reveal-left">
      <?= img('/wp-content/uploads/2026/04/Hail-Damage-Claim-Supplements-What-Carriers-Miss-in-Their-Scope-2.webp', 'Corpus Christi public adjuster reviewing storm damage with homeowners outside a coastal home', ['sizes' => '(max-width: 900px) 100vw, 560px']) ?>
      <div class="media-badge">Working for policyholders<small>Not insurance companies</small></div>
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Why choose us</p>
      <h2 id="why-h">Why Choose <span class="text-gradient-dark">Corpus Christi Public Adjuster</span>?</h2>
      <p>After a loss, your insurer sends its own adjuster, estimator, and sometimes an engineer. Their job is to evaluate the claim for the insurance company. A licensed public adjuster is the only claim professional who works for <em>you</em>&mdash;the policyholder.</p>
      <p>On the coast, claims are rarely simple. Many Corpus Christi homes carry three separate policies&mdash;homeowners, TWIA windstorm, and flood&mdash;and each one points to the others when damage is mixed. Corpus Christi Public Adjuster sorts out which coverage applies, documents the full scope of damage, and keeps the claim moving.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> <span><strong>Policy review</strong> &mdash; coverages, named-storm deductibles, exclusions, and deadlines explained in plain English.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Thorough documentation</strong> &mdash; photos, measurements, and line-item estimates of visible and hidden damage.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Estimate review</strong> &mdash; we compare the insurer's estimate with what Coastal Bend repairs actually require.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Communication handled</strong> &mdash; we work with the carrier's adjuster through settlement.</span></li>
        <li><?= icon('check', 'icon') ?> <span><strong>Honest guidance</strong> &mdash; if we don't think we can help, we'll tell you.</span></li>
      </ul>
      <a class="btn btn-navy" href="/about-us/">About our approach</a>
    </div>
  </div>
</section>

<div class="marquee" aria-label="Claim types we handle">
  <div class="marquee-track">
    <?php for ($r = 0; $r < 2; $r++): foreach ($marquee as [$ic, $label]): ?>
    <span class="marquee-item"<?= $r ? ' aria-hidden="true"' : '' ?>><?= icon($ic, 'icon') ?> <?= e($label) ?></span>
    <?php endforeach; endfor; ?>
  </div>
</div>

<section class="section section-alt" aria-labelledby="services-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Our services</p>
      <h2 id="services-h">Insurance Claim Services From Corpus Christi Public Adjuster</h2>
      <p>From hurricane and TWIA windstorm claims to hail-damaged roofs, flooded first floors, fire, and commercial losses, Corpus Christi Public Adjuster handles residential and commercial property insurance claims across Nueces County and the Coastal Bend.</p>
    </div>
    <?php component('services-grid', ['limit' => 8]); ?>
    <p class="center" style="margin-top:30px"><a class="btn btn-ghost" href="/services/">View all <?= count(service_cards()) ?> claim services</a></p>
  </div>
</section>

<section class="section" aria-labelledby="policy-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">Coastal coverage, explained</p>
      <h2 id="policy-h">Which Policy Pays for Your Damage?</h2>
      <p>On the Texas coast, the cause of damage decides which policy responds. Pick a type of damage to see where a claim usually starts. Every policy is different, so a Corpus Christi Public Adjuster always confirms with your declarations page and endorsements.</p>
    </div>
    <div class="policy-picker reveal" data-policy-picker>
      <div class="policy-tabs" role="tablist" aria-label="Type of damage">
        <button role="tab" type="button" aria-selected="true" data-key="wind"><?= icon('wind', 'icon') ?> Hurricane wind</button>
        <button role="tab" type="button" aria-selected="false" data-key="surge"><?= icon('droplets', 'icon') ?> Storm surge / flood</button>
        <button role="tab" type="button" aria-selected="false" data-key="hail"><?= icon('hail', 'icon') ?> Hail</button>
        <button role="tab" type="button" aria-selected="false" data-key="pipe"><?= icon('water', 'icon') ?> Burst pipe / leak</button>
        <button role="tab" type="button" aria-selected="false" data-key="fire"><?= icon('fire', 'icon') ?> Fire &amp; smoke</button>
      </div>
      <div class="policy-panels">
        <div class="policy-panel" role="tabpanel" data-panel="wind">
          <div class="policy-cards">
            <div class="policy-card is-primary"><span>Usually responds</span><strong>TWIA windstorm policy</strong><p>For most properties in the TWIA catastrophe area (Nueces, San Patricio, Aransas, Kleberg), wind damage is covered by TWIA, not the homeowners policy.</p></div>
            <div class="policy-card"><span>Sometimes</span><strong>Homeowners policy</strong><p>If your homeowners policy does not exclude wind and hail, it may respond instead. Check for a windstorm exclusion endorsement.</p></div>
            <div class="policy-card is-muted"><span>Watch for</span><strong>Named-storm deductible</strong><p>A percentage deductible often applies to hurricane wind. Try our <a href="/hurricane-deductible-calculator/">deductible calculator</a>.</p></div>
          </div>
        </div>
        <div class="policy-panel" role="tabpanel" data-panel="surge" hidden>
          <div class="policy-cards">
            <div class="policy-card is-primary"><span>Usually responds</span><strong>Flood policy (NFIP or private)</strong><p>Rising water and storm surge are flood. Homeowners and TWIA policies generally exclude flood.</p></div>
            <div class="policy-card"><span>Often disputed</span><strong>Wind vs. water</strong><p>When wind and surge hit the same building, insurers may argue over which caused what. Documentation matters.</p></div>
            <div class="policy-card is-muted"><span>Watch for</span><strong>30-day waiting period</strong><p>New NFIP policies usually take 30 days to start&mdash;buy before hurricane season, not during it.</p></div>
          </div>
        </div>
        <div class="policy-panel" role="tabpanel" data-panel="hail" hidden>
          <div class="policy-cards">
            <div class="policy-card is-primary"><span>Usually responds</span><strong>TWIA or homeowners</strong><p>TWIA covers wind <em>and hail</em> in the catastrophe area; otherwise your homeowners or commercial policy usually does.</p></div>
            <div class="policy-card"><span>Common dispute</span><strong>Wear vs. hail</strong><p>Carriers often blame granule loss on age. Dated photos and NOAA records help tie damage to a storm.</p></div>
            <div class="policy-card is-muted"><span>Watch for</span><strong>Cosmetic exclusions</strong><p>Some roof endorsements exclude dents that don't affect function, especially on metal roofs.</p></div>
          </div>
        </div>
        <div class="policy-panel" role="tabpanel" data-panel="pipe" hidden>
          <div class="policy-cards">
            <div class="policy-card is-primary"><span>Usually responds</span><strong>Homeowners / commercial policy</strong><p>Sudden and accidental water discharge (a burst supply line, a failed water heater) is a common covered loss.</p></div>
            <div class="policy-card"><span>Common dispute</span><strong>"Long-term leak"</strong><p>Insurers may deny repeated seepage or deterioration. Prompt reporting and moisture mapping help.</p></div>
            <div class="policy-card is-muted"><span>Watch for</span><strong>Mold limits</strong><p>Many policies cap mold remediation. Dry-out quickly and keep the receipts.</p></div>
          </div>
        </div>
        <div class="policy-panel" role="tabpanel" data-panel="fire" hidden>
          <div class="policy-cards">
            <div class="policy-card is-primary"><span>Usually responds</span><strong>Homeowners / commercial policy</strong><p>Fire and smoke are named perils on nearly every property policy, including contents and living expenses.</p></div>
            <div class="policy-card"><span>Often missed</span><strong>Smoke &amp; soot migration</strong><p>Smoke travels through HVAC and wall cavities far beyond the burned room.</p></div>
            <div class="policy-card is-muted"><span>Watch for</span><strong>Contents inventory</strong><p>Room-by-room inventories take time; additional living expense helps while you're displaced.</p></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt" id="free-claim-review" aria-labelledby="fcr-h">
  <div class="container split split-form">
    <div class="reveal-left">
      <p class="eyebrow">Free Claim Review</p>
      <h2 id="fcr-h">Request Your Free Claim Review</h2>
      <p class="lead">Whether you haven't filed yet, your claim was denied, or the insurer's offer won't cover repairs, a Corpus Christi Public Adjuster can review your situation at no cost.</p>
      <ul class="check-list">
        <li><?= icon('check', 'icon') ?> Review of your policy, the insurer's estimate, and any denial letter</li>
        <li><?= icon('check', 'icon') ?> Plain-English explanation of options and next steps</li>
        <li><?= icon('check', 'icon') ?> Upload photos or documents securely (optional)</li>
        <li><?= icon('check', 'icon') ?> No obligation to hire us</li>
      </ul>
      <p>Prefer to talk? Call or text <a href="<?= e(tel_link()) ?>"><strong><?= e(cfg('phone_display')) ?></strong></a> or email <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a>.</p>
      <div class="contact-direct">
        <img src="/assets/img/joseph-dittman.webp" alt="" width="58" height="58" loading="lazy">
        <div><strong>Want to reach Joseph Dittman directly?</strong>Email <a href="mailto:<?= e(cfg('author_email')) ?>"><?= e(cfg('author_email')) ?></a></div>
      </div>
    </div>
    <div class="form-card reveal-right">
      <p class="form-card-title h3" style="font-family:var(--font-head);font-weight:700;color:var(--navy);font-size:1.35rem">Tell us about your claim</p>
      <?php component('claim-form', ['context' => 'Homepage form']); ?>
    </div>
  </div>
</section>

<section class="section section-navy" aria-labelledby="storm-h">
  <div class="grid-overlay" aria-hidden="true"></div>
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow eyebrow-gold">Local weather risks</p>
      <h2 id="storm-h">Hurricanes, Hail, and Wind on the Coastal Bend</h2>
      <p>Nueces County sees tropical storms and hurricanes, storm surge on the bays and barrier islands, damaging thunderstorm winds, spring hail, flash flooding, and the occasional hard freeze. Here is what the official NOAA record shows.</p>
    </div>
    <div class="stats">
      <div class="stat reveal"><span class="stat-num" data-count="<?= (int) $stats['wind'] ?>">0</span><span class="stat-label">thunderstorm wind reports in Nueces County since <?= (int) $stats['first_year'] ?></span></div>
      <div class="stat reveal" style="--d:80ms"><span class="stat-num" data-count="<?= (int) $stats['hail'] ?>">0</span><span class="stat-label">hail reports, peaking in April and May</span></div>
      <div class="stat reveal" style="--d:160ms"><span class="stat-num" data-count="<?= (int) $stats['max_wind'] ?>" data-suffix=" mph">0</span><span class="stat-label">strongest estimated gust on record (<?= e(date('M Y', strtotime($stats['max_wind_ev']['date'] ?? 'now'))) ?>, <?= e($stats['max_wind_ev']['loc'] ?? 'Nueces County') ?>)</span></div>
      <div class="stat reveal" style="--d:240ms"><span class="stat-num" data-count="<?= (int) $stats['flood'] ?>">0</span><span class="stat-label">flood and flash flood reports</span></div>
    </div>
    <p class="stat-source center" style="margin-top:14px">Source: <a href="https://www.ncdc.noaa.gov/stormevents/" target="_blank" rel="noopener">NOAA NCEI Storm Events Database</a>, Nueces County, TX (county and NWS zone entries). Counts are individual reports, not storm days.</p>
    <div class="card-grid card-grid-3" style="margin-top:40px">
      <div class="tool-card reveal"><span class="tool-card-icon"><?= icon('hurricane', 'icon') ?></span><span class="tool-card-title">Hurricane Harvey (2017) &amp; Hanna (2020)</span><span class="tool-card-text">Harvey brought widespread major damage to Port Aransas, Rockport, and the bay communities; Hanna's surge damaged Bob Hall Pier and piers along the Corpus Christi waterfront.</span></div>
      <div class="tool-card reveal" style="--d:80ms"><span class="tool-card-icon"><?= icon('wind', 'icon') ?></span><span class="tool-card-title">May 8, 2025 windstorm</span><span class="tool-card-text">NWS surveys estimated 105&ndash;115 mph gusts around Petronila, Driscoll, and Agua Dulce, snapping power poles and stripping roofs in western Nueces County.</span></div>
      <div class="tool-card reveal" style="--d:160ms"><span class="tool-card-icon"><?= icon('droplets', 'icon') ?></span><span class="tool-card-title">Surge, tides &amp; flash floods</span><span class="tool-card-text">Tropical Storm Harold (2023) pushed tides over 3 feet above MHHW on the islands. Flood damage needs a separate flood policy.</span></div>
    </div>
    <p class="center" style="margin-top:30px"><a class="btn btn-gold" href="/storm-history/">Explore Coastal Bend storm history</a> <a class="btn btn-outline-light" href="/storm-lookup/">Look up storms near you</a></p>
  </div>
</section>

<section class="section section-alt" aria-labelledby="wx-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0">Live weather</p><h2 id="wx-h" class="mb-0">Corpus Christi Weather Right Now</h2></div>
      <a class="btn btn-ghost btn-sm" href="/weather/">Radar, tides, tropics &amp; alerts</a>
    </div>
    <?php if ($alertCount): ?>
    <div class="notice notice-error"><strong><?= icon('alert', 'icon icon-sm') ?> <?= $alertCount ?> active National Weather Service alert<?= $alertCount > 1 ? 's' : '' ?> for Corpus Christi:</strong> <?= e(implode(', ', array_unique(array_column($al['data'], 'event')))) ?>. <a href="/weather/">See details</a>.</div>
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
      <div><p class="eyebrow mb-0">Recent weather events</p><h2 id="events-h" class="mb-0">Latest Storm Reports Around Corpus Christi</h2></div>
      <a class="btn btn-ghost btn-sm" href="/weather-events/">All weather events</a>
    </div>
    <?php if ($recentEvents): ?>
    <div class="event-list"><?php foreach ($recentEvents as $ev) component('event-card', ['ev' => $ev]); ?></div>
    <?php else: ?>
    <p class="muted">No recent storm reports are on file. New National Weather Service reports appear here automatically.</p>
    <?php endif; ?>
    <p class="small muted" style="margin-top:14px">Preliminary National Weather Service Local Storm Reports for Nueces, San Patricio, Aransas, and Kleberg counties. A nearby report does not prove damage at a specific property.</p>
    <?php component('cta-storm'); ?>
  </div>
</section>

<section class="section section-gray" aria-labelledby="process-h">
  <div class="container split" style="align-items:start">
    <div class="reveal-left">
      <p class="eyebrow">How it works</p>
      <h2 id="process-h">How Corpus Christi Public Adjuster Handles Your Claim</h2>
      <p>Every claim is different, but the path is consistent and transparent. We stay involved from the first conversation until the claim is resolved&mdash;including supplements for damage found during repairs.</p>
      <p>Texas requires public adjusters to use a written, TDI-compliant contract that states <strong>&ldquo;We represent the insured only,&rdquo;</strong> gives you 72 hours to cancel, and caps compensation at 10% of the settlement.</p>
      <a class="btn btn-gold" href="/free-claim-review/">Start with a Free Claim Review</a>
    </div>
    <ol class="timeline">
      <li><div class="timeline-card"><h3>Initial consultation</h3><p>We review what happened and explain your options&mdash;free.</p></div></li>
      <li><div class="timeline-card"><h3>Property inspection</h3><p>Roof, exterior, interior, and contents&mdash;including damage that is easy to miss.</p></div></li>
      <li><div class="timeline-card"><h3>Policy analysis</h3><p>Homeowners, TWIA, flood, and commercial coverages, limits, deductibles, and exclusions.</p></div></li>
      <li><div class="timeline-card"><h3>Claim preparation</h3><p>Photos, measurements, weather records, and a line-item estimate that documents the loss.</p></div></li>
      <li><div class="timeline-card"><h3>Negotiation</h3><p>We communicate directly with the insurance company on your behalf.</p></div></li>
      <li><div class="timeline-card"><h3>Resolution</h3><p>Support through settlement, supplements, appraisal if needed, and final closure.</p></div></li>
    </ol>
  </div>
</section>

<section class="section section-navy" aria-labelledby="tools-h">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow eyebrow-gold">Free resources</p>
      <h2 id="tools-h">Free Insurance Claim Tools</h2>
      <p>Practical tools built by Corpus Christi Public Adjuster for Coastal Bend property owners. They run in your browser and use official NOAA and National Weather Service data.</p>
    </div>
    <?php component('tools-grid'); ?>
  </div>
</section>

<section class="section" aria-labelledby="codes-h">
  <div class="container split">
    <div class="reveal-left">
      <p class="eyebrow">Codes &amp; windstorm certification</p>
      <h2 id="codes-h">Building Codes, Windstorm Certificates, and Your Repairs</h2>
      <p>Repairs in Corpus Christi must meet the city's adopted building codes, and most coastal properties insured by TWIA also need windstorm inspections and a certificate of compliance (Form WPI-8) for covered work. Code-required work can raise repair costs.</p>
      <p>Whether your insurer pays for code upgrades depends on your policy, often through <em>ordinance or law</em> coverage. A Corpus Christi Public Adjuster checks for that coverage before the scope is settled.</p>
      <a class="btn btn-navy" href="/local-building-codes/">Corpus Christi building code guide</a>
    </div>
    <div class="reveal-right">
      <div class="table-wrap"><table class="code-table">
        <thead><tr><th scope="col">Topic</th><th scope="col">What to know</th></tr></thead>
        <tbody>
          <tr><td>Permits</td><td>Re-roofing and most structural repairs need a city permit</td></tr>
          <tr><td>Windstorm</td><td>TWIA-insured repairs generally need TDI windstorm inspection and a WPI-8</td></tr>
          <tr><td>Inspections</td><td>Schedule them before covering work so the certificate can issue</td></tr>
          <tr><td>Insurance</td><td>Code upgrades may be covered by ordinance or law coverage, up to its limit</td></tr>
        </tbody></table></div>
      <p class="small muted">Always confirm current requirements with the City of Corpus Christi and the Texas Department of Insurance before starting work.</p>
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
      <div class="feature reveal"><div class="feature-icon"><?= icon('home', 'icon') ?></div><h3>Homeowners</h3><p>Hurricane, wind, and hail damage, flooded first floors, burst pipes, fire and smoke, and contents claims for single-family homes and condos.</p><p style="margin-top:12px"><a href="/services/residential-property-claims/">Residential claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:80ms"><div class="feature-icon"><?= icon('building', 'icon') ?></div><h3>Business owners</h3><p>Retail, office, restaurant, hospitality, warehouse, and industrial properties&mdash;including business income, equipment, and inventory losses.</p><p style="margin-top:12px"><a href="/services/commercial-property-claims/">Commercial claims &rarr;</a></p></div>
      <div class="feature reveal" style="--d:160ms"><div class="feature-icon"><?= icon('layers', 'icon') ?></div><h3>Landlords, HOAs &amp; multifamily</h3><p>Apartment complexes, condominium associations, short-term rentals on the islands, and rental homes with owner and tenant coverage questions.</p><p style="margin-top:12px"><a href="/services/">All services &rarr;</a></p></div>
    </div>
    <div class="section-head reveal" style="margin:56px auto 0">
      <h3>Serving Corpus Christi and the Coastal Bend</h3>
      <div class="chip-list chip-list-center">
        <a class="chip" href="/service-areas/">Corpus Christi</a>
        <?php foreach (area_pages() as $slug => $name): ?><a class="chip" href="/service-areas/<?= e($slug) ?>/"><?= e($name) ?></a><?php endforeach; ?>
      </div>
      <p class="small muted">Plus Calallen, Flour Bluff, Annaville, Gregory, Taft, Sinton, Bishop, and nearby communities.</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="joseph-h">
  <div class="container split">
    <div class="reveal-left" style="text-align:center">
      <img src="/assets/img/joseph-dittman.webp" alt="Joseph Dittman, licensed Texas public adjuster" width="320" height="320" loading="lazy" decoding="async" class="joseph-photo" data-tilt>
    </div>
    <div class="reveal-right">
      <p class="eyebrow">Meet your adjuster</p>
      <h2 id="joseph-h">About Joseph Dittman, Licensed Public Adjuster</h2>
      <p>Joseph Dittman is a licensed Texas public adjuster, certified insurance appraiser, insurance umpire, and expert witness. His background includes carrier-side adjusting, public adjusting, appraisal work, expert witness support, and hands-on construction experience.</p>
      <p>He writes and reviews the guides on this site, covering residential, commercial, storm, hail, wind, water, fire, hurricane, and catastrophe losses, so Corpus Christi Public Adjuster readers get practical information grounded in Texas claim experience.</p>
      <div class="hero-actions">
        <a class="btn btn-navy" href="/author/joseph-dittman/">Read Joseph's profile</a>
        <a class="btn btn-ghost" href="mailto:<?= e(cfg('author_email')) ?>"><?= icon('mail', 'icon icon-sm') ?> Email Joseph directly</a>
      </div>
      <p class="small muted" style="margin-top:12px">Direct email: <a href="mailto:<?= e(cfg('author_email')) ?>"><?= e(cfg('author_email')) ?></a></p>
    </div>
  </div>
</section>

<section class="section section-alt" aria-labelledby="blog-h">
  <div class="container">
    <div class="results-bar">
      <div><p class="eyebrow mb-0">Insurance claim guides</p><h2 id="blog-h" class="mb-0">Latest From the Corpus Christi Public Adjuster Blog</h2></div>
      <a class="btn btn-ghost btn-sm" href="/blog/">View all articles</a>
    </div>
    <div class="card-grid card-grid-posts"><?php foreach ($posts as $post) component('post-card', ['post' => $post]); ?></div>
  </div>
</section>

<section class="section" aria-labelledby="faq-heading-home">
  <div class="container narrow">
    <?php component('faq', ['faqs' => $page['faqs'] ?? [], 'heading' => 'Corpus Christi Public Adjuster FAQs', 'id' => 'home']); ?>
  </div>
</section>

<section class="section section-navy" aria-labelledby="final-h">
  <?php component('aurora'); ?>
  <div class="container narrow center reveal">
    <p class="eyebrow eyebrow-gold">Free Claim Review</p>
    <h2 id="final-h">Talk With a Corpus Christi Public Adjuster Today</h2>
    <p>Insurance policies have deadlines, and evidence fades after a storm. If your property in Corpus Christi, Portland, Rockport, Port Aransas, Robstown, Kingsville, or anywhere on the Coastal Bend was damaged, start with a free, no-obligation review from Corpus Christi Public Adjuster.</p>
    <div class="hero-actions" style="justify-content:center">
      <a class="btn btn-gold btn-lg" href="/free-claim-review/">Get a Free Claim Review</a>
      <a class="btn btn-outline-light btn-lg" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> <?= e(cfg('phone_display')) ?></a>
    </div>
    <p class="small" style="margin-top:18px;color:#9fb2c4">Email: <a href="mailto:<?= e(cfg('public_email')) ?>"><?= e(cfg('public_email')) ?></a> &middot; Joseph Dittman direct: <a href="mailto:<?= e(cfg('author_email')) ?>"><?= e(cfg('author_email')) ?></a><br>Serving Corpus Christi, Nueces County, and surrounding Coastal Bend communities.</p>
  </div>
</section>
