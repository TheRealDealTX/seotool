<?php
require __DIR__ . '/includes/layout.php';

page_start([
    'title' => 'Austin Roofing | Trusted Austin Roofing Company & Roofers, TX',
    'description' => 'Austin Roofing is a local Austin roofing company for roof repair, replacement, hail & storm damage and commercial roofs. Free inspections — call (956) 465-6045.',
    'path' => '/',
    'hero_home' => true,
    'body_class' => 'page-home',
    'preload' => '/wp-content/uploads/2025/12/Austin-Roofing-BG-1.webp',
]);
?>
<section class="home-hero">
  <canvas class="weather" data-weather="rain" aria-hidden="true"></canvas>
  <div class="lightning" aria-hidden="true"></div>
  <div class="container home-hero__inner">
    <div>
      <p class="eyebrow"><?= icon('pin') ?> Austin, TX &amp; Central Texas</p>
      <h1>Austin Roofing</h1>
      <p class="home-hero__tag">The Austin Roofing Company Built for Texas Heat, Hail &amp; Wind</p>
      <p class="home-hero__lead">From a single leak to a full roof replacement, Austin Roofing protects homes, businesses and multi-family properties across the Austin metro with honest inspections, quality materials and workmanship that holds up to Central Texas weather.</p>
      <div class="btn-row">
        <a class="btn btn--red btn--lg" href="/contact-us/"><?= icon('clipboard') ?> Get a FREE Quote</a>
        <a class="btn btn--ghost btn--lg" href="tel:<?= BIZ['phone_href'] ?>"><?= icon('phone') ?> <?= e(BIZ['phone_display']) ?></a>
      </div>
      <ul class="hero-badges">
        <li><?= icon('check') ?> Free roof inspections</li>
        <li><?= icon('check') ?> 24/7 emergency service</li>
        <li><?= icon('check') ?> Insurance claim documentation</li>
        <li><?= icon('check') ?> Residential &amp; commercial</li>
      </ul>
    </div>
    <div class="hero-card" id="quote">
      <h2>Free Roofing Estimate</h2>
      <p>Tell us about your roof and an Austin Roofing specialist will get back to you fast.</p>
      <?php quote_form(true, '/ (hero)'); ?>
    </div>
  </div>
  <div class="weather-toggle" role="group" aria-label="Preview Austin weather">
    <button type="button" data-mode="rain" aria-pressed="true"><?= icon('rain') ?> Rain</button>
    <button type="button" data-mode="hail" aria-pressed="false"><?= icon('hail') ?> Hail</button>
    <button type="button" data-mode="sun" aria-pressed="false"><?= icon('sun') ?> Heat</button>
  </div>
  <div class="roof-divider" aria-hidden="true"></div>
</section>

<section class="section" id="about">
  <div class="container intro-grid">
    <div>
      <p class="eyebrow">Your local Austin roofers</p>
      <h2>A Local Austin Roofing Company You Can Actually Trust</h2>
      <p class="lead">Your roof is the first thing standing between your family and a June hailstorm, a 105°F August afternoon or a sideways spring downpour. At <strong>Austin Roofing</strong>, we build and repair roofs that are ready for all three.</p>
      <p>We are an Austin roofing contractor serving homeowners, business owners, property managers and HOAs throughout Travis, Williamson and Hays counties. Whether you need a quick roof repair, help after storm damage, a commercial roof coating or a complete roof replacement, our crews deliver clear communication, quality materials and craftsmanship that lasts.</p>
      <p>Every Austin Roofing project starts the same way: a free, photo-documented inspection and a straight answer about what your roof really needs — even when that answer is a small repair instead of a new roof.</p>
      <ul class="checklist">
        <li>Local experts who understand Austin’s climate</li>
        <li>Honest repair-vs-replace recommendations with photos</li>
        <li>Fast response — especially after hail and wind storms</li>
        <li>Quality materials from trusted manufacturers</li>
        <li>No-pressure, free quotes on every project</li>
      </ul>
      <a class="btn btn--red" href="/about-us/">Learn More About Austin Roofing</a>
    </div>
    <div class="roof-build" aria-hidden="true">
      <svg viewBox="0 0 480 380">
        <defs>
          <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6f4f7"/><stop offset="1" stop-color="#F3F2EC"/></linearGradient>
          <clipPath id="roofclip"><polygon points="40,190 240,40 440,190"/></clipPath>
        </defs>
        <rect width="480" height="380" rx="28" fill="url(#sky)"/>
        <circle cx="400" cy="70" r="30" fill="#f7c948" opacity=".85"/>
        <rect x="80" y="190" width="320" height="160" fill="#fff" stroke="#363636" stroke-width="3"/>
        <rect x="210" y="260" width="60" height="90" fill="#1E93AB"/>
        <rect x="115" y="225" width="60" height="50" fill="#cfe9ef" stroke="#363636" stroke-width="3"/>
        <rect x="305" y="225" width="60" height="50" fill="#cfe9ef" stroke="#363636" stroke-width="3"/>
        <polygon points="40,190 240,40 440,190" fill="#d9d4c7"/>
        <g clip-path="url(#roofclip)">
          <?php for ($r = 0; $r < 8; $r++): $y = 172 - $r * 19; ?>
          <g class="shingle-row" style="transition-delay:<?= $r * 140 ?>ms">
            <rect x="30" y="<?= $y ?>" width="420" height="20" fill="<?= $r % 2 ? '#5c524b' : '#665b53' ?>"/>
            <?php for ($x = 30 + ($r % 2) * 18; $x < 450; $x += 36): ?><line x1="<?= $x ?>" y1="<?= $y ?>" x2="<?= $x ?>" y2="<?= $y + 20 ?>" stroke="#3f3732" stroke-width="2"/><?php endfor; ?>
            <line x1="30" y1="<?= $y + 19 ?>" x2="450" y2="<?= $y + 19 ?>" stroke="#3f3732" stroke-width="2"/>
          </g>
          <?php endfor; ?>
        </g>
        <polyline points="30,197 240,40 450,197" fill="none" stroke="#E62727" stroke-width="12" stroke-linejoin="round" stroke-linecap="round"/>
        <rect x="320" y="70" width="34" height="70" fill="#E62727"/>
      </svg>
    </div>
  </div>
</section>

<section class="section section--dark section--tight">
  <div class="container stats">
    <div class="stat"><div class="stat__num">24/7</div><div class="stat__label">Emergency roof service</div></div>
    <div class="stat"><div class="stat__num" data-count="<?= count(SERVICES) ?>"><?= count(SERVICES) ?></div><div class="stat__label">Roofing services under one roof</div></div>
    <div class="stat"><div class="stat__num" data-count="12" data-suffix="+">12+</div><div class="stat__label">Central Texas cities served</div></div>
    <div class="stat"><div class="stat__num">$0</div><div class="stat__label">Inspections &amp; quotes</div></div>
  </div>
</section>

<section class="section section--dark" id="services">
  <div class="container">
    <h2 class="section-title">Austin Roofing Services</h2>
    <p class="section-lead">A complete range of Austin roofing services for homeowners, business owners and property managers — repair, restoration, replacement and storm recovery, all from one accountable team.</p>
    <?php service_cards(['roof-repair', 'roof-replacement', 'hail-damage-repair', 'wind-damage-repair', 'roof-restoration', 'commercial-roofing', 'commercial-roof-coatings', 'multifamily-roofing', 'roof-insurance-claims']); ?>
    <div class="btn-row" style="justify-content:center;margin-top:36px">
      <a class="btn btn--red btn--lg" href="/services/">View All Austin Roofing Services</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">Why Homeowners Choose Austin Roofing</h2>
    <p class="section-lead">Choosing roofers in Austin should not feel like guesswork. Our philosophy is simple: do what is right, explain it clearly and deliver quality that lasts.</p>
    <div class="compare">
      <div class="compare__bad">
        <h3><?= icon('alert') ?> What too many Austin homeowners deal with</h3>
        <ul>
          <li>Storm chasers who leave town before the warranty does</li>
          <li>Being pushed into a full replacement when a repair would do</li>
          <li>Cheap materials and corners cut where you can’t see them</li>
          <li>Slow callbacks during storm season</li>
          <li>No explanation of what is actually wrong with the roof</li>
        </ul>
      </div>
      <div class="compare__good">
        <h3><?= icon('shield') ?> The Austin Roofing way</h3>
        <ul>
          <li>A local Austin roofing contractor that stays after the storm</li>
          <li>Repair vs replace options with photos so you decide</li>
          <li>Materials chosen for Texas heat, UV and hail</li>
          <li>Fast inspections and temporary protection after storms</li>
          <li>Insured, safety-focused crews that follow building codes and manufacturer specs</li>
        </ul>
      </div>
    </div>
    <div class="feature-grid" style="margin-top:34px">
      <div class="feature reveal"><h3><?= icon('hail') ?> Storm damage specialists</h3><p>After hail or wind, we provide quick inspections, emergency tarping and the photo documentation your insurance claim needs.</p></div>
      <div class="feature reveal"><h3><?= icon('camera') ?> Honest assessments</h3><p>We show you photos of every issue and give you repair, restoration and replacement options that fit your budget.</p></div>
      <div class="feature reveal"><h3><?= icon('building') ?> Full-service capabilities</h3><p>Homes, commercial buildings and multi-family communities — one Austin roofing company for every property you own.</p></div>
      <div class="feature reveal"><h3><?= icon('clipboard') ?> Free inspections &amp; quotes</h3><p>Our goal is clarity, not pressure. Every inspection and estimate from Austin Roofing is free with no obligation.</p></div>
    </div>
  </div>
</section>

<section class="section section--cream section--shingles">
  <div class="container">
    <h2 class="section-title">How an Austin Roofing Project Works</h2>
    <p class="section-lead">Four simple steps from first call to finished roof — with photos and plain-English answers at every stage.</p>
    <ol class="steps">
      <li class="reveal"><h3>Free inspection</h3><p>We inspect the roof, attic and flashing and photograph everything we find.</p></li>
      <li class="reveal"><h3>Clear options</h3><p>You get a written quote with repair, restoration or replacement options — no pressure.</p></li>
      <li class="reveal"><h3>Expert installation</h3><p>Our crew completes the work to code and manufacturer spec; most homes take one to two days.</p></li>
      <li class="reveal"><h3>Cleanup &amp; walkthrough</h3><p>Magnetic nail sweep, debris haul-off and a final walkthrough with photos of the finished roof.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="container tools-teaser">
    <div>
      <p class="eyebrow"><?= icon('calc') ?> Free roofing tools</p>
      <h2>What Will a New Roof Cost in Austin?</h2>
      <p>Get a realistic planning range in seconds. Our Austin roof replacement cost calculator uses your home’s size, roof pitch, shape and material to estimate squares and installed cost — then Austin Roofing can turn it into an exact, free quote.</p>
      <p>Try our other free tools too:</p>
      <ul class="sidebar__links">
        <?php foreach (TOOLS as $slug => $t): ?>
        <li><a href="/roofing-tools/<?= $slug ?>/"><?= icon($t['icon']) ?> <?= e($t['name']) ?></a></li>
        <?php endforeach; ?>
      </ul>
    </div>
    <?php tool('cost'); ?>
  </div>
</section>

<section class="section section--cream">
  <div class="container split">
    <div>
      <p class="eyebrow">Built for Central Texas</p>
      <h2>Roofs Designed for Austin Weather</h2>
      <p>Austin’s weather is hard on roofs. Spring storms can drop golf-ball hail across Travis and Williamson counties in minutes, straight-line winds peel back shingles and flashing, and months of triple-digit heat bake asphalt and dry out sealants. A roof that would last 30 years up north may only last 18–25 here if it is not built for it.</p>
      <p>That is why Austin Roofing pays attention to the details that matter in this climate: impact-resistant shingle options, proper attic ventilation, high-temperature underlayment under metal, sealed flashing and fasteners placed to the manufacturer’s high-wind pattern.</p>
      <a class="btn btn--outline" href="/roofing-tools/hail-damage-checker/">Check if hail damaged your roof →</a>
    </div>
    <div class="feature-grid">
      <div class="feature reveal"><h3><?= icon('sun') ?> Heat &amp; UV</h3><p>Ventilation, reflective options and heat-rated underlayment slow shingle aging.</p></div>
      <div class="feature reveal"><h3><?= icon('hail') ?> Hail</h3><p>Class 4 impact-resistant shingles and metal roofs stand up to Texas hail.</p></div>
      <div class="feature reveal"><h3><?= icon('wind') ?> Wind</h3><p>High-wind nailing patterns, sealed starter rows and secured ridge caps.</p></div>
      <div class="feature reveal"><h3><?= icon('rain') ?> Heavy rain</h3><p>Self-adhered membrane in valleys and around every penetration.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <h2 class="section-title">Austin Roofing Service Areas</h2>
    <p class="section-lead">Based in Austin and serving the surrounding Central Texas communities — from East and South Austin to Round Rock, Cedar Park, Georgetown, Kyle and San Marcos.</p>
    <?php area_cards(); ?>
  </div>
</section>

<section class="section section--cream">
  <div class="container">
    <h2 class="section-title">Latest Roofing Guides</h2>
    <p class="section-lead">Straight answers from Austin roofers on costs, materials, insurance and keeping your roof healthy.</p>
    <?php post_cards(3); ?>
    <div class="btn-row" style="justify-content:center;margin-top:30px"><a class="btn btn--outline" href="/blog/">Read More Articles</a></div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:900px">
    <?php faq_block([
        ['How do I choose the best Austin roofing company?', '<p>Look for a local Austin roofing company with a verifiable phone number and email, written estimates, proof of insurance, manufacturer-backed materials and a clear warranty. Avoid contractors who pressure you to sign on the spot after a storm. Austin Roofing offers free inspections with photos so you can compare options with confidence.</p>'],
        ['Does Austin Roofing offer free roof inspections?', '<p>Yes. Every inspection and quote from Austin Roofing is free with no obligation — for storm damage, leaks, aging roofs, real-estate transactions or just peace of mind.</p>'],
        ['How much does a new roof cost in Austin, TX?', '<p>Most Austin homes fall somewhere between about 15 and 40 roofing squares, and installed prices vary widely by material — architectural shingles cost far less per square than standing seam metal. Use our <a href="/roofing-tools/roof-cost-calculator/">roof cost calculator</a> for a planning range, then book a free inspection for an exact price.</p>'],
        ['Can Austin Roofing help with my hail damage insurance claim?', '<p>Yes. We inspect and photograph the damage, provide a detailed report and can meet your insurance adjuster on the roof so the damage is fully seen. We are roofers, not public adjusters — your policy and claim decisions stay between you and your insurer. <a href="/services/roof-insurance-claims/">Learn more about claim help</a>.</p>'],
        ['Do you handle commercial and multi-family roofing in Austin?', '<p>Absolutely. Austin Roofing repairs, coats and replaces TPO, EPDM, modified bitumen, built-up and metal roofs on retail, office, industrial and multi-family properties, with scheduling that keeps tenants and residents disruption to a minimum.</p>'],
        ['How fast can Austin roofers respond to an emergency leak?', '<p>We offer 24/7 emergency service. Call <a href="tel:+19564656045">(956) 465-6045</a> and we will get a crew out to tarp and stop the leak as quickly as possible, then schedule the permanent repair.</p>'],
    ], 'Austin Roofing FAQs'); ?>
  </div>
</section>

<?php
cta_band('Get Your Free Roof Inspection From Austin Roofing', 'Unexpected storm damage, a commercial roofing upgrade or simply a professional opinion on an aging roof — Austin Roofing is ready with honest answers and roofs built to last.');
page_end();
