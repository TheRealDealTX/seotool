<?php
defined('TR_ROOT') || exit;

$faqs = [
    ['q' => 'Is the roof inspection really free?', 'a' => 'Yes. Temple Roofers inspects residential roofs in Temple and nearby communities at no cost and with no obligation to hire us. You get photos of what we found and a plain-language explanation, even when the answer is that your roof is in good shape.'],
    ['q' => 'How do I know if hail damaged my roof?', 'a' => 'Hail damage is hard to judge from the ground. Dented gutters, downspouts, AC fins or mailboxes and heavy granule wash at the downspouts are good clues. If you see them, schedule an inspection so one of our Temple roofers can check the shingles up close instead of guessing. Please do not climb onto the roof yourself.'],
    ['q' => 'Should I repair my roof or replace it?', 'a' => 'It depends on the roof\'s age, how widespread the damage is and the condition of the decking underneath. Isolated problems on a younger roof are usually repairable. Widespread hail bruising, brittle shingles or repeated leaks in several places often point toward replacement. We explain both options when both are realistic.'],
    ['q' => 'Do you help with roof insurance claims?', 'a' => 'We document storm damage with photos and measurements, prepare a written repair estimate and can be on site when your adjuster inspects if you would like. We are roofers, not public adjusters, so we do not negotiate your claim. Texas law also requires homeowners to pay their own deductible, and we never waive or rebate it.'],
    ['q' => 'How long does a roof replacement take?', 'a' => 'Many single-family re-roofs are completed in one to three working days once materials are delivered. Larger or steeper roofs, decking replacement and Central Texas weather can extend that. You will get an expected schedule before work begins.'],
    ['q' => 'What roofing materials hold up best in Central Texas?', 'a' => 'Architectural and impact-resistant (Class 4) asphalt shingles and standing-seam metal are popular choices around Temple because they handle wind, hail and heat better than basic 3-tab shingles. The right pick depends on your budget, roof pitch, HOA rules and how long you plan to stay in the home.'],
    ['q' => 'What should I do if my roof is leaking right now?', 'a' => 'Move valuables away from the drip, catch water in a bucket, and if a ceiling is bulging with water, keep people clear of it. Take photos for your records and call (512) 297-7580. Our Temple roofers can arrange temporary protection and a permanent repair once it is safe to work on the roof.'],
    ['q' => 'Which areas do you serve?', 'a' => 'We are based in Temple and serve Belton, Troy, Salado, Little River-Academy, Morgan\'s Point Resort, Nolanville, Harker Heights and Rogers, along with homes and businesses across the surrounding Bell County area.'],
    ['q' => 'Do you work on commercial buildings?', 'a' => 'Yes. Along with homes, we inspect and repair low-slope and metal roofs on commercial properties, and we plan work to keep disruption to your business as low as practical.'],
];

$posts = array_slice(posts(), 0, 3);
$services = services();
$areas = areas();

layout_start([
    'title'         => 'Temple Roofers | Roof Repair & Replacement in Temple, TX',
    'raw_title'     => true,
    'description'   => 'Temple Roofers offers roof repair, roof replacement, storm and hail damage repair and free roof inspections in Temple, TX. Call (512) 297-7580.',
    'path'          => '/',
    'body_class'    => 'page-home',
    'preload_image' => 'hero-texas-home-roof',
    'schema'        => [schema_faq($faqs)],
    'scripts'       => ['js/weather.js'],
]);
?>
<section class="hero">
  <div class="hero__bg" data-parallax><?= img('hero-texas-home-roof', 'Single-family home with an asphalt shingle roof under a blue sky', ['sizes' => '100vw', 'priority' => true, 'class' => 'hero__img']) ?></div>
  <div class="container hero__inner">
    <div class="hero__copy">
      <p class="eyebrow eyebrow--light hero__eyebrow"><?= icon('map-pin') ?> Roofing contractor in Temple, Texas</p>
      <h1 class="hero__title">Trusted <span class="text-gold">Temple Roofers</span> for Repairs, Replacements &amp; Storm Damage</h1>
      <p class="hero__lead">From small roof leaks to complete roof replacements, Temple Roofers helps Central Texas homeowners protect their properties with reliable roofing solutions and free roof inspections.</p>
      <div class="btn-row">
        <a class="btn btn--gold btn--lg" href="/free-roof-inspection/"><?= icon('clipboard-check') ?> Get My Free Roof Inspection</a>
        <a class="btn btn--outline-light btn--lg" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> Call <?= e(cfg('phone_display')) ?></a>
      </div>
      <ul class="hero__points">
        <li><?= icon('check') ?> No-cost, no-obligation inspections</li>
        <li><?= icon('check') ?> Photo-documented findings</li>
        <li><?= icon('check') ?> Residential &amp; commercial</li>
      </ul>
    </div>
    <div class="hero__form">
      <?php lead_form(['variant' => 'compact', 'id' => 'hero', 'title' => 'Book your free roof inspection', 'subtitle' => 'Takes about a minute. We will call to confirm a time.', 'button' => 'Get My Free Inspection']); ?>
    </div>
  </div>
</section>

<section class="stats-strip" aria-label="Temple Roofers at a glance">
  <div class="container stats-strip__grid">
    <div class="stat reveal"><span class="stat__num">$<span data-count="0">0</span></span><span class="stat__label">Cost of a roof inspection</span></div>
    <div class="stat reveal"><span class="stat__num" data-count="12">12</span><span class="stat__label">Roofing services</span></div>
    <div class="stat reveal"><span class="stat__num" data-count="<?= count($areas) ?>"><?= count($areas) ?></span><span class="stat__label">Bell County communities served</span></div>
    <div class="stat reveal"><span class="stat__num" data-count="3">3</span><span class="stat__label">Free online roofing tools</span></div>
  </div>
</section>

<section class="section local-intro">
  <div class="container split">
    <div class="split__copy reveal">
      <p class="eyebrow">Roofing in Central Texas</p>
      <h2 class="section-title">What Temple Homeowners Should Know About Their Roofs</h2>
      <p>Roofs in Temple work harder than the brochures suggest. As Temple roofers, we see the same pattern on house after house: a spring of hail and straight-line winds, a summer that bakes the shingles for weeks at a time, and sudden downpours that find every weak spot in the flashing. None of that shows up on day one. It shows up as curled tabs on the west-facing slope, a stain on a bedroom ceiling, or granules piling up at the bottom of a downspout.</p>
      <p>Understanding those local stresses is the first step to making good decisions about repairs, maintenance and eventually replacement. Here is what Bell County weather does to a typical roof.</p>
      <a class="text-link" href="/blog/">Read our Temple roofing guides <?= icon('arrow-right') ?></a>
    </div>
    <div class="split__media reveal">
      <figure class="media-frame"><?= img('storm-clouds-over-homes', 'Dark storm clouds building over a residential neighborhood', ['sizes' => '(max-width: 900px) 100vw, 50vw']) ?></figure>
    </div>
  </div>
  <div class="container">
    <div class="factor-grid">
      <article class="factor reveal"><span class="factor__icon"><?= icon('wind') ?></span><h3>Strong winds</h3><p>Straight-line winds from spring storms lift shingle edges and break the adhesive seal strips. Once a tab is creased, the next gust can tear it away completely.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('cloud-lightning') ?></span><h3>Severe thunderstorms</h3><p>Central Texas storms often arrive in clusters in spring and again in fall, combining wind, hail, lightning and falling limbs in one afternoon.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('cloud-hail') ?></span><h3>Hail</h3><p>Hail bruises shingles, knocks off the protective granules and dents vents and gutters. Damage is often invisible from the yard but shortens the roof's life.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('cloud-rain') ?></span><h3>Heavy rainfall</h3><p>Downpours of an inch or more in an hour overwhelm undersized gutters and push water sideways under flashing at walls, chimneys and valleys.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('thermometer') ?></span><h3>Intense summer heat</h3><p>Long stretches in the upper 90s and above heat dark shingles far past the air temperature, softening asphalt and speeding up aging.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('sun') ?></span><h3>UV deterioration</h3><p>Strong Texas sun breaks down exposed asphalt, rubber pipe boots and sealants. Cracked boots around plumbing vents are one of the most common leak sources we find.</p></article>
      <article class="factor reveal"><span class="factor__icon"><?= icon('fan') ?></span><h3>Ventilation &amp; attic heat</h3><p>A poorly ventilated attic traps heat and moisture under the decking, cooking shingles from below and driving up cooling bills. Balanced intake and exhaust matters.</p></article>
      <article class="factor factor--cta reveal"><h3>Not sure how your roof is holding up?</h3><p>Get a free, no-obligation inspection and photos of what we find.</p><a class="btn btn--gold btn--sm" href="/free-roof-inspection/">Book an inspection</a></article>
    </div>
  </div>
</section>

<section class="section section--alt" id="services">
  <div class="container">
    <?= section_head('Our roofing services', 'Roofing Services for Temple Homes and Businesses', 'Every service our Temple roofers offer starts the same way: a careful inspection and a clear explanation of what your roof actually needs, whether that is a small repair, storm restoration or a full replacement.') ?>
    <div class="card-grid card-grid--3">
      <?php foreach ($services as $s): ?>
      <?= service_card($s) ?>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section inspection-feature">
  <div class="container split split--reverse">
    <div class="split__media reveal">
      <figure class="media-frame media-frame--accent"><?= img('roofer-inspecting-roof', 'Roofing professional inspecting asphalt shingles on a residential roof', ['sizes' => '(max-width: 900px) 100vw, 50vw']) ?></figure>
      <div class="badge-float"><strong>$0</strong><span>Free · No obligation</span></div>
    </div>
    <div class="split__copy reveal">
      <p class="eyebrow">Free roof inspections</p>
      <h2 class="section-title">Free Roof Inspections for Temple Homeowners</h2>
      <p>A free roof inspection is the easiest way to find out where your roof stands before a small problem becomes an expensive one. Our Temple roofers walk the roof (so you never have to), check the attic where it is accessible, and photograph anything that needs attention.</p>
      <ul class="check-list">
        <li><?= icon('check') ?><span><strong>Shingles and surface:</strong> missing, creased, cracked, curled or hail-bruised shingles and granule loss.</span></li>
        <li><?= icon('check') ?><span><strong>Flashing:</strong> walls, chimneys, valleys, skylights and drip edge.</span></li>
        <li><?= icon('check') ?><span><strong>Roof penetrations:</strong> plumbing pipe boots, vents and exhaust caps.</span></li>
        <li><?= icon('check') ?><span><strong>Ventilation:</strong> intake and exhaust balance and signs of attic heat or moisture.</span></li>
        <li><?= icon('check') ?><span><strong>Storm-related concerns:</strong> hail impacts, wind lift and debris damage, documented with photos.</span></li>
        <li><?= icon('check') ?><span><strong>Visible deterioration:</strong> soft decking, sagging, rot and gutter or fascia problems.</span></li>
      </ul>
      <p class="note-line"><?= icon('shield') ?> The inspection is free and carries no obligation. If the roof is fine, we will tell you.</p>
      <div class="btn-row">
        <a class="btn btn--navy" href="/free-roof-inspection/">See how the inspection works</a>
        <a class="btn btn--ghost" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <?= e(cfg('phone_display')) ?></a>
      </div>
    </div>
  </div>
</section>

<section class="section section--navy why">
  <div class="container">
    <?= section_head('Why Temple Roofers', 'What You Can Expect From Our Team', 'No sales pressure and no vague promises. Here is what you should expect from Temple roofers you invite onto your property.') ?>
    <div class="why-grid">
      <article class="why-card reveal"><span class="why-card__icon"><?= icon('message') ?></span><h3>Clear communication</h3><p>You will know when we are coming, what we found and what happens next. We answer questions in plain language, not roofing jargon.</p></article>
      <article class="why-card reveal"><span class="why-card__icon"><?= icon('wrench') ?></span><h3>Practical options</h3><p>When a repair will do the job, we say so. When replacement makes more sense, we explain why and show you the evidence.</p></article>
      <article class="why-card reveal"><span class="why-card__icon"><?= icon('camera') ?></span><h3>Detailed inspections</h3><p>Every inspection comes with photos of the problem areas, so you can see exactly what we saw on the roof.</p></article>
      <article class="why-card reveal"><span class="why-card__icon"><?= icon('document') ?></span><h3>Transparent estimates</h3><p>Written, itemized estimates that spell out materials, scope and what is not included, so you can compare apples to apples.</p></article>
      <article class="why-card reveal"><span class="why-card__icon"><?= icon('cloud-lightning') ?></span><h3>Central Texas weather know-how</h3><p>We plan materials, ventilation and installation details around the wind, hail and heat that Bell County roofs actually face.</p></article>
      <article class="why-card reveal"><span class="why-card__icon"><?= icon('building') ?></span><h3>Residential &amp; commercial</h3><p>From a single-story ranch home to a low-slope commercial roof, we handle repairs, replacements and inspections.</p></article>
    </div>
  </div>
</section>

<section class="section process">
  <div class="container">
    <?= section_head('How it works', 'How Our Roofing Process Works', 'Our Temple roofers keep the process simple and predictable, from the first phone call to the final cleanup.') ?>
    <ol class="steps">
      <li class="step reveal"><span class="step__num">1</span><span class="step__icon"><?= icon('phone') ?></span><h3>Contact us</h3><p>Call <?= e(cfg('phone_display')) ?> or send the form. Tell us what you are noticing.</p></li>
      <li class="step reveal"><span class="step__num">2</span><span class="step__icon"><?= icon('calendar') ?></span><h3>Schedule a free inspection</h3><p>We set a time that works for you and inspect the roof, flashing, vents and attic.</p></li>
      <li class="step reveal"><span class="step__num">3</span><span class="step__icon"><?= icon('camera') ?></span><h3>Review the findings</h3><p>We walk you through the photos and explain what is urgent and what can wait.</p></li>
      <li class="step reveal"><span class="step__num">4</span><span class="step__icon"><?= icon('document') ?></span><h3>Discuss repair or replacement</h3><p>You get a written estimate with realistic options and no pressure to decide on the spot.</p></li>
      <li class="step reveal"><span class="step__num">5</span><span class="step__icon"><?= icon('home') ?></span><h3>Complete the work</h3><p>We complete the agreed work, clean up the site and review the finished roof with you.</p></li>
    </ol>
  </div>
</section>

<section class="section section--alt compare">
  <div class="container">
    <?= section_head('Repair or replace?', 'Roof Repair vs. Roof Replacement', 'There is no one-size-fits-all answer, but these patterns help explain what we usually recommend and why.') ?>
    <div class="table-wrap reveal">
      <table class="compare-table">
        <thead><tr><th scope="col">Situation</th><th scope="col"><?= icon('wrench') ?> Repair is often enough</th><th scope="col"><?= icon('home') ?> Replacement may make sense</th></tr></thead>
        <tbody>
          <tr><th scope="row">Roof age</th><td>Roof is well within its expected service life</td><td>Roof is near or past the end of its expected life</td></tr>
          <tr><th scope="row">Extent of damage</th><td>A few missing or damaged shingles in one area</td><td>Widespread hail bruising or wind damage on several slopes</td></tr>
          <tr><th scope="row">Leaks</th><td>A single leak traced to a pipe boot, flashing or one spot</td><td>Recurring leaks in multiple places despite past repairs</td></tr>
          <tr><th scope="row">Shingle condition</th><td>Shingles are flexible and holding their granules</td><td>Brittle, curling or heavily bald shingles across the roof</td></tr>
          <tr><th scope="row">Decking</th><td>Solid decking with no sagging</td><td>Soft, rotted or sagging decking in several areas</td></tr>
          <tr><th scope="row">Long-term plans</th><td>Selling soon or budgeting for a replacement later</td><td>Staying for years and wanting impact-resistant or metal upgrades</td></tr>
        </tbody>
      </table>
    </div>
    <p class="center-note reveal">Want to dig deeper? Explore <a href="/services/roof-repair-temple-tx/">roof repair</a>, <a href="/services/roof-replacement-temple-tx/">roof replacement</a>, or estimate a budget with our <a href="/tools/roof-replacement-cost-calculator/">roof replacement cost calculator</a>.</p>
  </div>
</section>

<section class="section weather-preview" aria-labelledby="wx-preview-title">
  <div class="container weather-preview__inner">
    <div class="weather-preview__copy reveal">
      <p class="eyebrow eyebrow--light">Live conditions</p>
      <h2 class="section-title" id="wx-preview-title">Temple Weather Right Now</h2>
      <p>Storm season matters to every roof in Bell County. Check live Temple conditions, the seven-day outlook and any active National Weather Service alerts — and if a storm has just passed, our Temple roofers can check your roof for free.</p>
      <a class="btn btn--gold" href="/weather/"><?= icon('cloud-sun') ?> Full 7-day roofing forecast</a>
    </div>
    <div class="weather-preview__widget reveal" data-weather="compact" aria-live="polite">
      <div class="wx-loading"><span class="spinner" aria-hidden="true"></span> Loading live Temple weather…</div>
      <noscript><p>Live weather needs JavaScript. <a href="/weather/">Open the weather page</a>.</p></noscript>
    </div>
  </div>
</section>

<section class="section tools-feature">
  <div class="container">
    <?= section_head('Free roofing tools', 'Plan Smarter With Free Roofing Tools', 'Estimate a replacement budget, measure your roof pitch and area, or run through a quick storm-damage self-check — no sign-up required.') ?>
    <div class="tool-grid">
      <?php foreach (catalog('tools') as $slug => $t): ?>
      <?= tool_card($slug, $t) ?>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section--alt areas-feature">
  <div class="container split split--top">
    <div class="split__copy reveal">
      <p class="eyebrow">Service areas</p>
      <h2 class="section-title">Serving Temple and Nearby Bell County Communities</h2>
      <p>Temple is home base, and most of our work happens right here, from older homes near downtown to newer subdivisions on the west and south sides of town. Our Temple roofers also travel to the surrounding communities listed here.</p>
      <a class="btn btn--navy" href="/service-areas/">View all service areas</a>
    </div>
    <div class="area-grid">
      <?php foreach ($areas as $a): ?>
      <?= area_card($a) ?>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<?php if ($posts): ?>
<section class="section blog-feature">
  <div class="container">
    <?= section_head('From the blog', 'Latest Roofing Guides for Temple Homeowners', 'Practical, locally focused advice on storms, maintenance, costs and materials.') ?>
    <div class="card-grid card-grid--3">
      <?php foreach ($posts as $p): ?>
      <?= post_card($p) ?>
      <?php endforeach; ?>
      <?php if (count($posts) < 3): ?>
      <article class="card card--more reveal">
        <div class="card__body">
          <span class="tool-card__icon"><?= icon('book') ?></span>
          <h3 class="card__title">More guides on the way</h3>
          <p>New articles on roof costs, inspections, lifespan, storm recovery and maintenance are published every few days. In the meantime, try our free tools or check the live Temple forecast.</p>
          <a class="card__link" href="/tools/">Explore roofing tools <?= icon('arrow-right') ?></a>
        </div>
      </article>
      <?php endif; ?>
    </div>
    <p class="center-note"><a class="btn btn--ghost" href="/blog/">Visit the roofing blog</a></p>
  </div>
</section>
<?php endif; ?>

<section class="section section--alt">
  <div class="container container--narrow">
    <?= faq_html($faqs, 'Roofing FAQs for Temple Homeowners', 'Straight answers to the questions Temple roofers hear most often.') ?>
  </div>
</section>

<?php final_cta('Concerned About Your Roof? Schedule a Free Inspection.', 'Whether it is a fresh storm, a stubborn leak or a roof that is simply getting old, Temple Roofers will take a look at no cost and give you honest answers. Our Temple roofers serve homeowners and businesses across Temple and nearby Bell County communities.', '/'); ?>
<?php layout_end([]);
