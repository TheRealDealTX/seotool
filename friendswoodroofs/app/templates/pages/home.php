<?php
$geo = config('geo');
$latest = array_slice(articles(), 0, 3, true);
?>
<section class="hero">
  <div class="hero-media"><?= photo('hero-roofing-crew', '100vw', true) ?></div>
  <div class="container hero-inner">
    <p class="eyebrow eyebrow--light">Roofing for Friendswood, TX homeowners</p>
    <h1>Friendswood Roofers for Roof Repair, Replacement &amp; Inspections</h1>
    <p class="lead">Friendswood Roofers helps homeowners understand what their roof needs, from a single leak to a full replacement. You get a careful look at the problem, a plain-language explanation and a written estimate before any work starts.</p>
    <div class="hero-actions">
      <a class="btn btn-accent btn-lg" href="#estimate-form"><?= icon('clipboard') ?><span>Request an Estimate</span></a>
      <a class="btn btn-light btn-lg" href="<?= e(phone_href()) ?>"><?= icon('phone') ?><span>Call Now <span class="btn-sub"><?= e(phone_display()) ?></span></span></a>
    </div>
    <ul class="hero-points" role="list">
      <li><?= icon('check', 'icon icon-sm') ?> Written estimates before work begins</li>
      <li><?= icon('check', 'icon icon-sm') ?> Photos of what we find on your roof</li>
      <li><?= icon('check', 'icon icon-sm') ?> Focused on homes in Friendswood, TX</li>
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="intro-heading">
  <div class="container split">
    <div data-reveal>
      <p class="eyebrow">About Friendswood Roofers</p>
      <h2 id="intro-heading">A roofing company that explains before it sells</h2>
      <p>Most homeowners only deal with a major roofing decision once or twice. That makes it hard to know whether a contractor's recommendation is the right one. As Friendswood roofers, our job is to make that decision easier: we look at the whole roof, show you what we see and give you options with clear pricing.</p>
      <p>Friendswood homes deal with long, hot summers, heavy rain, strong thunderstorms and the Atlantic hurricane season. Those conditions are tough on shingles, flashing and attic ventilation. Whether you need a <a href="/services/roof-repair/">roof repair</a>, a <a href="/services/roof-inspections/">roof inspection</a> or are weighing a <a href="/services/roof-replacement/">full replacement</a>, we focus on finding the cause and recommending only what the roof actually needs.</p>
      <p><a class="link-arrow" href="/about/">How we approach every roof <?= icon('arrow', 'icon icon-sm') ?></a></p>
    </div>
    <figure class="split-media" data-reveal>
      <?= photo('asphalt-shingles-closeup', '(min-width: 900px) 45vw, 100vw') ?>
      <figcaption><?= photo_credit('asphalt-shingles-closeup') ?></figcaption>
    </figure>
  </div>
</section>

<section class="section section--tint" aria-labelledby="services-heading">
  <div class="container">
    <div class="section-head" data-reveal>
      <p class="eyebrow">Roofing services</p>
      <h2 id="services-heading">Friendswood roofing services for every stage of your roof's life</h2>
      <p>From small repairs to complete replacements, each service starts with an honest assessment. Choose a service to learn about common problems, the process and what affects cost.</p>
    </div>
    <?php partial('service-cards'); ?>
    <p class="section-foot"><a class="btn btn-outline" href="/services/">View all roofing services</a></p>
  </div>
</section>

<section class="section" aria-labelledby="signs-heading">
  <div class="container">
    <div class="section-head" data-reveal>
      <p class="eyebrow">Know the warning signs</p>
      <h2 id="signs-heading">Common signs your roof needs attention</h2>
      <p>You can spot many of these from the ground or inside your home. Please don't climb onto the roof to check; use binoculars, look in the attic with a flashlight if it's safe, and call us if anything looks wrong.</p>
    </div>
    <ul class="signs-grid" role="list">
      <li data-reveal><?= icon('droplet') ?><div><h3>Stains or drips inside</h3><p>Ceiling or wall stains, bubbling paint, damp insulation or musty smells after rain.</p></div></li>
      <li data-reveal><?= icon('layers') ?><div><h3>Missing or damaged shingles</h3><p>Gaps, cracked or curled shingles, or shingles you find in the yard after wind.</p></div></li>
      <li data-reveal><?= icon('storm') ?><div><h3>Granules in gutters</h3><p>A sudden increase in sand-like granules, especially after hail, can mean shingle wear.</p></div></li>
      <li data-reveal><?= icon('home') ?><div><h3>Sagging roof lines</h3><p>Dips or waves in the roof surface may point to moisture damage in the decking.</p></div></li>
      <li data-reveal><?= icon('sun') ?><div><h3>Daylight in the attic</h3><p>Light coming through the roof deck means water can get in, too.</p></div></li>
      <li data-reveal><?= icon('wrench') ?><div><h3>Loose flashing or vents</h3><p>Metal pulling away from walls or chimneys, or cracked boots around plumbing vents.</p></div></li>
    </ul>
    <p class="section-foot" data-reveal>Seeing one of these? Read our guide on <a href="/blog/roof-repair-or-replacement-friendswood/">whether to repair or replace your roof</a>, or <a href="#estimate-form">request an estimate</a>.</p>
  </div>
</section>

<section class="section section--navy" aria-labelledby="process-heading">
  <div class="container">
    <div class="section-head section-head--light" data-reveal>
      <p class="eyebrow eyebrow--light">How it works</p>
      <h2 id="process-heading">From your first call to a finished roof</h2>
      <p>A simple, predictable process with no pressure and no surprises in the paperwork.</p>
    </div>
    <ol class="process-steps">
      <li data-reveal><span class="step-num" aria-hidden="true">1</span><h3>Tell us what's going on</h3><p>Call or send the form with your concern. Our <a href="/roofing-project-planner/">project planner</a> can help you organize the details.</p></li>
      <li data-reveal><span class="step-num" aria-hidden="true">2</span><h3>Roof assessment</h3><p>We inspect the roof and, when accessible, the attic, and take photos of what we find.</p></li>
      <li data-reveal><span class="step-num" aria-hidden="true">3</span><h3>Written estimate</h3><p>You get a clear scope, materials and price in writing, plus how any hidden issues would be handled.</p></li>
      <li data-reveal><span class="step-num" aria-hidden="true">4</span><h3>Scheduled work</h3><p>Once you approve, we agree on a start date. Weather can shift schedules, and we'll keep you informed.</p></li>
      <li data-reveal><span class="step-num" aria-hidden="true">5</span><h3>Clean-up and review</h3><p>We clean the site, walk you through the completed work and share photos for your records.</p></li>
    </ol>
  </div>
</section>

<section class="section" aria-labelledby="materials-heading">
  <div class="container">
    <div class="section-head" data-reveal>
      <p class="eyebrow">Roofing materials</p>
      <h2 id="materials-heading">An overview of roofing materials</h2>
      <p>The right material depends on your budget, how long you plan to stay and the look you want. A roof is also a system, so the parts you don't see matter as much as the surface.</p>
    </div>
    <div class="material-grid">
      <article class="card material-card" data-reveal>
        <div class="card-media"><?= photo('asphalt-shingles-closeup', '(min-width: 900px) 30vw, 100vw') ?></div>
        <div class="card-body">
          <h3>Asphalt shingles</h3>
          <p>The most common residential roofing material. Available as three-tab, dimensional (architectural) and impact-resistant products in many colors. Lower upfront cost and simple repairs.</p>
          <a class="link-arrow" href="/services/asphalt-shingle-roofing/">Asphalt shingle roofing <?= icon('arrow', 'icon icon-sm') ?></a>
        </div>
      </article>
      <article class="card material-card" data-reveal>
        <div class="card-media"><?= photo('standing-seam-metal-roof', '(min-width: 900px) 30vw, 100vw') ?></div>
        <div class="card-body">
          <h3>Metal roofing</h3>
          <p>Standing seam and exposed-fastener panel systems. Higher upfront cost, often chosen for durability, wind performance and reflective finishes.</p>
          <a class="link-arrow" href="/services/metal-roofing/">Metal roofing <?= icon('arrow', 'icon icon-sm') ?></a>
        </div>
      </article>
      <article class="card material-card material-card--list" data-reveal>
        <div class="card-body">
          <h3>The rest of the roof system</h3>
          <ul class="check-list">
            <li><strong>Decking:</strong> the wood sheathing everything attaches to.</li>
            <li><strong>Underlayment:</strong> a water-resistant layer beneath the roofing.</li>
            <li><strong>Flashing:</strong> metal that seals walls, chimneys, valleys and vents.</li>
            <li><strong>Ventilation:</strong> intake and exhaust that help manage attic heat and moisture.</li>
            <li><strong>Drip edge and gutters:</strong> guide water off the roof and away from the house.</li>
          </ul>
          <a class="link-arrow" href="/blog/asphalt-shingles-vs-metal-roofing-friendswood-tx/">Compare shingles and metal <?= icon('arrow', 'icon icon-sm') ?></a>
        </div>
      </article>
    </div>
  </div>
</section>

<?php if (config('weather.enabled')): ?>
<section class="section section--tint" aria-labelledby="weather-heading" id="weather">
  <div class="container weather-layout">
    <div class="weather-copy" data-reveal>
      <p class="eyebrow">Live radar</p>
      <h2 id="weather-heading">Friendswood Weather &amp; Roofing Planning</h2>
      <p>Weather has a direct effect on roofing schedules. Roofing work isn't done during rain, lightning or high wind, and wet surfaces need time to dry, so storms can move start dates. This live radar map centered on Friendswood shows current precipitation in the area.</p>
      <p>For watches, warnings and official forecasts, always rely on the <a href="https://www.weather.gov/hgx/" rel="noopener">National Weather Service Houston/Galveston office</a> or the <a href="https://forecast.weather.gov/MapClick.php?lat=<?= e((string) $geo['lat']) ?>&amp;lon=<?= e((string) $geo['lng']) ?>" rel="noopener">NWS forecast for Friendswood</a>. During hurricane season, follow the <a href="https://www.nhc.noaa.gov/" rel="noopener">National Hurricane Center</a>.</p>
      <p>After a storm, check from the ground or inside your home, not on the roof. If you see damage, read about <a href="/services/storm-damage-roof-repair/">storm damage roof repair</a>.</p>
    </div>
    <?php partial('weather-map'); ?>
  </div>
</section>
<?php endif; ?>

<section class="section" aria-labelledby="blog-heading">
  <div class="container">
    <div class="section-head section-head--row" data-reveal>
      <div>
        <p class="eyebrow">From the blog</p>
        <h2 id="blog-heading">Roofing guides for Friendswood homeowners</h2>
        <p>Comparing roofers in Friendswood, or planning ahead for storm season? These guides explain your options in plain language.</p>
      </div>
      <a class="btn btn-outline" href="/blog/">View all articles</a>
    </div>
    <div class="card-grid article-grid">
      <?php foreach ($latest as $a) { partial('article-card', ['a' => $a]); } ?>
    </div>
  </div>
</section>

<section class="section section--tint" aria-labelledby="faq-heading">
  <div class="container narrow">
    <div class="section-head" data-reveal>
      <p class="eyebrow">Questions</p>
      <h2 id="faq-heading">Frequently asked questions</h2>
    </div>
    <?php partial('faq-list', ['items' => home_faqs()]); ?>
    <p class="section-foot"><a class="btn btn-outline" href="/faqs/">See all roofing FAQs</a></p>
  </div>
</section>

<section class="section estimate-section" aria-labelledby="estimate-heading">
  <div class="container estimate-layout">
    <div class="estimate-aside" data-reveal>
      <p class="eyebrow">Get started</p>
      <p class="estimate-aside-title">Talk to a roofing company focused on Friendswood</p>
      <p>Send the form and we'll follow up to talk through your roof and arrange a time to look at it. Only your name, phone, address or ZIP and service are required.</p>
      <a class="call-panel" href="<?= e(phone_href()) ?>">
        <?= icon('phone') ?>
        <span><span class="call-panel-label">Prefer to call?</span><span class="call-panel-number"><?= e(phone_display()) ?></span></span>
      </a>
      <p class="small">Not sure what to say? Try the <a href="/roofing-project-planner/">Roofing Project Planner</a> first.</p>
    </div>
    <?php partial('estimate-form', ['returnTo' => '/', 'heading' => 'Request an Estimate']); ?>
  </div>
</section>
