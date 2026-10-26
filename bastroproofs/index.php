<?php
/** Homepage — primary keywords: bastrop roofing, roofing bastrop tx, bastrop roofer, bastrop metal roofing. */

// Front controller duties: some hosts route every unknown path here, so enforce
// the canonical host, redirect old WordPress URLs and 404 anything else.
$reqPath = strtok($_SERVER['REQUEST_URI'] ?? '/', '?') ?: '/';
$canonicalHost = 'bastroproofs.com';
if (($_SERVER['HTTP_X_FORWARDED_PROTO'] ?? '') === 'http' || ($_SERVER['HTTP_HOST'] ?? $canonicalHost) === 'www.' . $canonicalHost) {
    header('Location: https://' . $canonicalHost . ($_SERVER['REQUEST_URI'] ?? '/'), true, 301);
    exit;
}
if ($reqPath !== '/' && $reqPath !== '/index.php') {
    $redirects = [
        '#^/(sitemap_index|page-sitemap)\.xml$#'                     => '/sitemap.xml',
        '#^/(feed|comments/feed)/?$#'                                 => '/blog/',
        '#^/(wp-admin|wp-includes|wp-json|wp-login\.php|xmlrpc\.php)(/|$)#' => '/',
    ];
    foreach ($redirects as $re => $to) {
        if (preg_match($re, $reqPath)) {
            header('Location: https://' . $canonicalHost . $to, true, 301);
            exit;
        }
    }
    if (substr($reqPath, -1) !== '/' && is_dir(__DIR__ . $reqPath) && is_file(__DIR__ . $reqPath . '/index.php')) {
        header('Location: https://' . $canonicalHost . $reqPath . '/', true, 301);
        exit;
    }
    require __DIR__ . '/404.php';
    exit;
}

require __DIR__ . '/includes/bootstrap.php';

$homeFaqs = [
    ['q' => 'What roofing services does Bastrop Roofing offer?', 'a' => 'Bastrop Roofing handles roof repair, roof replacement, metal roofing, shingle roofing, roof inspections, storm and hail damage repair, emergency tarping, and commercial roofing for homes and businesses in Bastrop, TX and across Bastrop County.'],
    ['q' => 'How much does a new roof cost in Bastrop, TX?', 'a' => 'Most architectural shingle roofs in Bastrop plan out around $4.50 to $7.00 per square foot installed, and standing seam metal around $10 to $16. Use our free roof cost calculator for a planning range, then book a free inspection for an exact written price.'],
    ['q' => 'Is metal roofing a good choice in Bastrop?', 'a' => 'Yes. Bastrop metal roofing reflects summer heat, resists wind, sheds pine needles and can carry a Class A fire rating, which matters in the Lost Pines. It costs more up front but often outlasts two shingle roofs.'],
    ['q' => 'Should I get my roof inspected after a hailstorm?', 'a' => 'Yes. Hail bruises shingles in ways that are hard to see from the ground, and leaks may not appear for months. A free inspection from a Bastrop roofer documents damage while it can still be reported to your insurer.'],
    ['q' => 'Do you serve areas outside the city of Bastrop?', 'a' => 'We do. Bastrop Roofing serves all of Bastrop County, including Elgin, Smithville, Cedar Creek, Paige, McDade and Red Rock, plus the neighborhoods in and around Bastrop such as Tahitian Village, Hunters Crossing and Pine Forest.'],
    ['q' => 'How do I get a roofing estimate?', 'a' => 'Call (512) 297-7580, email info@bastroproofs.com, or send the estimate form on this page. We will schedule a free inspection, show you photos of what we find and give you a written estimate.'],
];

page_start([
    'title'       => 'Bastrop Roofing | (512) 297-7580 | Roofer in Bastrop, TX',
    'description' => 'Bastrop Roofing is your local Bastrop roofer for roof repair, replacement, metal roofing and storm damage in Bastrop, TX. Free inspections: (512) 297-7580.',
    'path'        => '/',
    'preload'     => 'A-Stronger-Roof-Starts-With-a-Clear-Plan.webp',
    'body'        => 'page-home',
    'schema'      => [
        [
            '@type'       => 'WebPage',
            '@id'         => abs_url('/#webpage'),
            'url'         => abs_url('/'),
            'name'        => 'Bastrop Roofing | Roofer in Bastrop, TX',
            'about'       => ['@id' => abs_url('/#business')],
            'isPartOf'    => ['@id' => abs_url('/#website')],
        ],
        faq_schema($homeFaqs),
    ],
]);
?>

<section class="hero" data-weather-stage>
  <img class="hero-bg" src="<?= img('A-Stronger-Roof-Starts-With-a-Clear-Plan.webp') ?>" alt="New architectural shingle roof installed by Bastrop Roofing on a home among the pines in Bastrop, TX" width="1200" height="655" fetchpriority="high">
  <canvas class="weather-canvas" data-weather="rain" data-hero aria-hidden="true"></canvas>
  <div class="lightning" aria-hidden="true"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <span class="eyebrow eyebrow-light">Roofing Bastrop TX · Lost Pines &amp; Bastrop County</span>
      <h1>Bastrop Roofing: <span class="h1-accent">Local Roofers</span> Built for Lost Pines Weather</h1>
      <p class="hero-lead">Bastrop Roofing repairs, replaces and installs shingle and metal roofs for homes and businesses across Bastrop, TX. Call a Bastrop roofer who inspects first, explains what is really going on, and puts the price in writing.</p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="tel:<?= SITE['phone_href'] ?>"><?= icon('phone') ?> Call <?= SITE['phone_short'] ?></a>
        <a class="btn btn-outline btn-lg" href="#estimate">Get a Free Estimate <?= icon('arrow') ?></a>
      </div>
      <ul class="hero-checks">
        <li><?= icon('check') ?> Free roof inspections</li>
        <li><?= icon('check') ?> Shingle &amp; metal roofing</li>
        <li><?= icon('check') ?> 24/7 storm response</li>
      </ul>
    </div>
    <div class="weather-panel reveal">
      <p class="wp-title">What is your roof up against?</p>
      <div class="wp-buttons" role="group" aria-label="Show Bastrop weather effect">
        <button type="button" data-set-weather="sun"><?= icon('sun') ?><span>Sun</span></button>
        <button type="button" data-set-weather="rain" class="is-active"><?= icon('drop') ?><span>Rain</span></button>
        <button type="button" data-set-weather="hail"><?= icon('hail') ?><span>Hail</span></button>
        <button type="button" data-set-weather="wind"><?= icon('wind') ?><span>Wind</span></button>
      </div>
      <div class="wp-info" aria-live="polite">
        <strong data-weather-title>Heavy Rain</strong>
        <p data-weather-text>Wind-driven rain finds every weak spot — cracked pipe boots, loose flashing and worn valleys. Bastrop Roofing traces leaks to the source.</p>
        <a data-weather-link href="/services/roof-repair-bastrop-tx/">Roof leak repair <?= icon('arrow') ?></a>
      </div>
    </div>
  </div>
  <div class="hero-shingles" aria-hidden="true"></div>
</section>

<section class="trust-strip">
  <div class="container trust-grid">
    <div class="trust-item"><?= icon('search') ?><span><strong>Free</strong> roof inspections</span></div>
    <div class="trust-item"><?= icon('clock') ?><span><strong>24/7</strong> storm &amp; leak calls</span></div>
    <div class="trust-item"><?= icon('layers') ?><span><strong>Metal &amp; shingle</strong> specialists</span></div>
    <div class="trust-item"><?= icon('shield') ?><span><strong>Written</strong> itemized estimates</span></div>
  </div>
</section>

<section class="section" id="about">
  <div class="container split">
    <div class="split-media reveal">
      <img src="<?= img('ABOUT-BASTROP-ROOFING.webp') ?>" alt="Bastrop Roofing crew inspecting a residential roof in Bastrop, Texas" width="1200" height="655" loading="lazy">
      <div class="media-badge"><?= icon('pin') ?><span><strong>Based in Bastrop</strong>Serving all of Bastrop County</span></div>
    </div>
    <div class="split-copy reveal">
      <span class="eyebrow">About Bastrop Roofing</span>
      <h2 class="section-title">Local Bastrop Roofers, Not Storm Chasers</h2>
      <p>Bastrop Roofing is a local roofing company serving homeowners, property managers and businesses in Bastrop, TX. We live with the same Lost Pines weather you do — long, hot summers, sudden spring hail, wind that drops pine limbs, and downpours that test every seam on a roof.</p>
      <p>That is why our approach to <strong>roofing in Bastrop, TX</strong> starts with a real inspection. We get on the roof and in the attic, photograph what we find, and explain your options in plain language — repair when repair makes sense, replacement when the roof has truly reached that point. That is what homeowners should expect from Bastrop roofing experts, and it is how roofing Bastrop TX homes should be done.</p>
      <ul class="check-list two-col">
        <li><?= icon('check') ?> Roof repair &amp; leak tracing</li>
        <li><?= icon('check') ?> Full roof replacement</li>
        <li><?= icon('check') ?> Bastrop metal roofing</li>
        <li><?= icon('check') ?> Hail &amp; storm damage</li>
        <li><?= icon('check') ?> Insurance documentation</li>
        <li><?= icon('check') ?> Commercial roofing</li>
      </ul>
      <a class="btn btn-dark" href="/about/">More About Bastrop Roofing <?= icon('arrow') ?></a>
    </div>
  </div>
</section>

<section class="section section-tint" id="services">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Bastrop Roofing Services</span>
      <h2 class="section-title">Roofing Services for Every Bastrop Home &amp; Business</h2>
      <p class="section-copy">From a single cracked pipe boot to a complete standing seam metal roof, Bastrop Roofing handles the full range of residential and commercial roofing Bastrop property owners need — as one local Bastrop roofing contractor from inspection to cleanup.</p>
    </div>
    <div class="card-grid"><?php service_cards(); ?></div>
  </div>
</section>

<section class="section metal-feature">
  <div class="metal-panels" aria-hidden="true"></div>
  <div class="container split">
    <div class="split-copy reveal">
      <span class="eyebrow eyebrow-light">Bastrop Metal Roofing</span>
      <h2 class="section-title light">Metal Roofs Made for the Lost Pines</h2>
      <p>Metal is one of the fastest-growing roof choices in Bastrop County, and for good reason. As a Bastrop metal roofer, we install standing seam, R-panel and stone-coated steel on homes, barns, shops and commercial buildings.</p>
      <div class="metal-stats">
        <div><strong data-count="50">0</strong><span>years typical lifespan</span></div>
        <div><strong>Class&nbsp;A</strong><span>fire rating possible</span></div>
        <div><strong data-count="2" data-suffix="–3×">0</strong><span>the life of shingles</span></div>
      </div>
      <ul class="check-list light">
        <li><?= icon('sun') ?> Reflects summer heat away from the attic</li>
        <li><?= icon('wind') ?> Concealed-clip systems resist wind uplift</li>
        <li><?= icon('tree') ?> Sheds pine needles instead of trapping them</li>
        <li><?= icon('flame') ?> Non-combustible surface for wildfire-prone areas</li>
      </ul>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/services/metal-roofing-bastrop-tx/">Explore Metal Roofing <?= icon('arrow') ?></a>
        <a class="btn btn-outline" href="/roofing-tools/metal-roof-vs-shingle-calculator/">Metal vs. Shingle Calculator</a>
      </div>
    </div>
    <div class="seam-demo reveal" aria-hidden="true">
      <div class="seam-roof">
        <?php for ($i = 0; $i < 9; $i++): ?><span style="--i:<?= $i ?>"></span><?php endfor; ?>
      </div>
      <div class="seam-drops"></div>
      <p class="seam-caption">Standing seam panels channel water straight off the roof — no exposed screws to leak.</p>
    </div>
  </div>
</section>

<section class="section anatomy" id="anatomy">
  <div class="container split split-wide">
    <div class="anatomy-visual reveal" data-anatomy>
      <svg viewBox="0 0 520 360" role="img" aria-label="Layers of a roof system, from decking to ridge vent">
        <defs>
          <pattern id="shingle-pat" width="34" height="18" patternUnits="userSpaceOnUse">
            <rect width="34" height="18" fill="#334758"/><path d="M0 17.5h34M17 0v9M0 9h34M8 9v9M25 9v9" stroke="#1d2b38" stroke-width="1.4"/>
          </pattern>
        </defs>
        <g class="layer" data-layer="0"><polygon points="40,300 260,110 480,300 450,300 260,136 70,300" fill="#c89b6d"/></g>
        <g class="layer" data-layer="1"><polygon points="52,290 260,112 468,290 448,290 260,128 72,290" fill="#9dc6df"/></g>
        <g class="layer" data-layer="2"><polygon points="60,284 120,232 140,232 80,284" fill="#18222d"/><polygon points="460,284 400,232 380,232 440,284" fill="#18222d"/><polygon points="246,124 260,112 274,124 260,140" fill="#18222d"/></g>
        <g class="layer" data-layer="3"><polygon points="40,292 260,100 480,292 452,292 260,126 68,292" fill="url(#shingle-pat)"/></g>
        <g class="layer" data-layer="4"><path d="M58 292 L40 304 H480 L462 292" fill="none" stroke="#c9813d" stroke-width="6"/></g>
        <g class="layer" data-layer="5"><polygon points="234,112 260,88 286,112 274,120 260,108 246,120" fill="#c9813d"/></g>
        <rect x="88" y="300" width="344" height="50" fill="#e9f3fa"/>
        <rect x="236" y="314" width="48" height="36" fill="#0a2540"/>
      </svg>
      <div class="anatomy-controls">
        <button type="button" class="btn btn-dark btn-sm" data-anatomy-play>Build the roof ▶</button>
      </div>
    </div>
    <div class="split-copy reveal">
      <span class="eyebrow">Inside a Bastrop Roofing install</span>
      <h2 class="section-title">A Roof Is a System, Not Just Shingles</h2>
      <p>Every roof we install is built layer by layer to stand up to Central Texas heat and storms. Tap a layer to see what it does.</p>
      <ol class="anatomy-list">
        <li data-layer-btn="0"><button type="button"><span>1</span><strong>Solid decking</strong><small>Soft or rotted plywood replaced so fasteners hold.</small></button></li>
        <li data-layer-btn="1"><button type="button"><span>2</span><strong>Synthetic underlayment</strong><small>A water-shedding second line of defense under the roof.</small></button></li>
        <li data-layer-btn="2"><button type="button"><span>3</span><strong>Ice &amp; water membrane</strong><small>Self-sealing barrier in valleys and around penetrations.</small></button></li>
        <li data-layer-btn="3"><button type="button"><span>4</span><strong>Shingles or metal panels</strong><small>Installed to manufacturer specs for wind and impact ratings.</small></button></li>
        <li data-layer-btn="4"><button type="button"><span>5</span><strong>Drip edge &amp; flashing</strong><small>New metal at every edge, wall and chimney — never reused.</small></button></li>
        <li data-layer-btn="5"><button type="button"><span>6</span><strong>Ridge vent</strong><small>Exhausts attic heat so the roof is not cooked from below.</small></button></li>
      </ol>
    </div>
  </div>
</section>

<section class="section section-dark" id="weather">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow eyebrow-light">Roofing in Bastrop, TX</span>
      <h2 class="section-title light">What Bastrop Weather Does to a Roof</h2>
      <p class="section-copy light">Roofing in Bastrop takes a beating from more than one direction. Knowing what to look for helps you catch problems early.</p>
    </div>
    <div class="weather-grid">
      <div class="weather-card reveal"><span class="wc-icon wc-sun"><?= icon('sun') ?></span><h3>Sun &amp; Heat</h3><p>Months of 95°F+ days dry out asphalt, crack sealants and bake shingles from above while a poorly vented attic bakes them from below.</p></div>
      <div class="weather-card reveal"><span class="wc-icon wc-hail"><?= icon('hail') ?></span><h3>Spring Hail</h3><p>Hail knocks off granules and bruises the shingle mat. Damage often hides for months before it becomes a leak.</p></div>
      <div class="weather-card reveal"><span class="wc-icon wc-wind"><?= icon('wind') ?></span><h3>High Wind</h3><p>Gusts break shingle seal strips, lift metal trim and drop loblolly pine limbs onto roofs throughout the Lost Pines.</p></div>
      <div class="weather-card reveal"><span class="wc-icon wc-rain"><?= icon('drop') ?></span><h3>Heavy Rain</h3><p>Sudden downpours expose worn flashing, cracked pipe boots and valleys clogged with pine needles.</p></div>
      <div class="weather-card reveal"><span class="wc-icon wc-tree"><?= icon('tree') ?></span><h3>Pine Debris</h3><p>Needles pile up in valleys and gutters, hold moisture, and grow algae on shaded roofs in Tahitian Village and Pine Forest.</p></div>
      <div class="weather-card reveal"><span class="wc-icon wc-fire"><?= icon('flame') ?></span><h3>Wildfire Risk</h3><p>Embers land on roofs and in gutters. Class A roof coverings and clean gutters are smart protection in Bastrop County.</p></div>
    </div>
  </div>
</section>

<section class="section" id="process">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Our Process</span>
      <h2 class="section-title">How Bastrop Roofing Works</h2>
      <p class="section-copy">A simple path from roof concern to a finished, photographed job — the way Bastrop, Texas roofing should work.</p>
    </div>
    <ol class="process">
      <li class="reveal"><span class="step-num">01</span><h3>Call or Request Online</h3><p>Tell us what you are seeing — leaks, storm damage, an aging roof — and when works for a visit.</p></li>
      <li class="reveal"><span class="step-num">02</span><h3>Free Roof Inspection</h3><p>We inspect the roof surface, flashing, ventilation and attic, and photograph everything.</p></li>
      <li class="reveal"><span class="step-num">03</span><h3>Clear Written Estimate</h3><p>Repair and replacement options, materials and price, itemized in writing — no pressure.</p></li>
      <li class="reveal"><span class="step-num">04</span><h3>Clean, Careful Install</h3><p>Property protected, work done to spec, magnetic nail sweep and a final photo walkthrough.</p></li>
    </ol>
  </div>
</section>

<section class="section section-tint" id="calculator">
  <div class="container">
    <div class="section-head center reveal">
      <span class="eyebrow">Free Bastrop Roofing cost calculator</span>
      <h2 class="section-title">What Will a New Roof Cost in Bastrop, TX?</h2>
      <p class="section-copy">Slide in your home size, pitch and material to get a Central Texas planning range instantly.</p>
    </div>
    <?php include __DIR__ . '/includes/tools/roof-replacement-cost-calculator.php'; ?>
    <div class="tool-grid tool-grid-after"><?php tool_cards(['roof-replacement-cost-calculator']); ?></div>
  </div>
</section>

<section class="section" id="areas">
  <div class="container split">
    <div class="split-copy reveal">
      <span class="eyebrow">Roofing Bastrop TX &amp; Beyond</span>
      <h2 class="section-title">Serving Bastrop and All of Bastrop County</h2>
      <p>Our crews are based in Bastrop and work every neighborhood in town, from historic homes near Main Street and Fisherman's Park to the wooded lots of Tahitian Village and the newer streets of Hunters Crossing. Outside town, Bastrop Roofing serves rural properties, barns and shops throughout the county.</p>
      <div class="chip-list">
<?php foreach (NEIGHBORHOODS as $n): ?>
        <span class="chip"><?= icon('home') ?> <?= e($n) ?></span>
<?php endforeach; ?>
      </div>
    </div>
    <div class="area-map reveal">
      <div class="map-center"><span class="pulse"></span><strong>Bastrop</strong><small>78602</small></div>
<?php
$pos = [['Elgin', 18, 8], ['McDade', 70, 10], ['Paige', 84, 34], ['Cedar Creek', 6, 60], ['Red Rock', 26, 86], ['Smithville', 80, 76]];
foreach ($AREAS as $slug => $a):
    $p = array_values(array_filter($pos, fn($x) => $x[0] === $a['name']))[0] ?? [$a['name'], 50, 50];
?>
      <a class="map-pin" href="/service-areas/<?= $slug ?>/" style="left:<?= $p[1] ?>%;top:<?= $p[2] ?>%"><?= icon('pin') ?><span><?= e($a['name']) ?></span></a>
<?php endforeach; ?>
      <a class="btn btn-dark btn-sm map-all" href="/service-areas/">All service areas</a>
    </div>
  </div>
</section>

<section class="section section-tint" id="blog">
  <div class="container">
    <div class="section-head reveal head-row">
      <div><span class="eyebrow">Bastrop Roofing Blog</span><h2 class="section-title small">Roofing Guides for Bastrop Homeowners</h2></div>
      <a class="btn btn-dark btn-sm" href="/blog/">All articles <?= icon('arrow') ?></a>
    </div>
    <div class="card-grid card-grid-3">
<?php foreach (array_slice($POSTS, 0, 3, true) as $k => $p): ?>
      <a class="post-card reveal" href="/blog/<?= $k ?>/">
        <img src="<?= img($p['image']) ?>" alt="" width="1200" height="655" loading="lazy">
        <span class="post-card-body"><small><?= fmt_date($p['date']) ?> · <?= $p['minutes'] ?> min read</small><strong><?= e($p['h1']) ?></strong><span><?= e($p['excerpt']) ?></span></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<?php faq_block($homeFaqs, 'Questions About Bastrop Roofing', 'Bastrop Roofing FAQ'); ?>

<section class="section section-dark contact-section" id="estimate">
  <canvas class="weather-canvas" data-weather="rain" aria-hidden="true"></canvas>
  <div class="container split">
    <div class="split-copy reveal">
      <span class="eyebrow eyebrow-light">Free Estimate</span>
      <h2 class="section-title light">Talk With a Bastrop Roofer About Your Roof</h2>
      <p class="light">Tell us what is happening with your roof and what kind of property you have. Bastrop Roofing will schedule a free inspection and give you a clear, written next step.</p>
      <ul class="contact-list">
        <li><a href="tel:<?= SITE['phone_href'] ?>"><span class="ci"><?= icon('phone') ?></span><span><small>Call or text</small><?= SITE['phone_display'] ?></span></a></li>
        <li><a href="mailto:<?= SITE['email'] ?>"><span class="ci"><?= icon('mail') ?></span><span><small>Email</small><?= SITE['email'] ?></span></a></li>
        <li><span class="ci"><?= icon('pin') ?></span><span><small>Service area</small>Bastrop, TX <?= SITE['zip'] ?> &amp; Bastrop County</span></li>
        <li><span class="ci"><?= icon('clock') ?></span><span><small>Hours</small><?= SITE['hours'] ?></span></li>
      </ul>
    </div>
    <div class="form-card reveal">
      <h3>Request Your Free Roof Estimate</h3>
      <?php estimate_form('Homepage'); ?>
    </div>
  </div>
</section>

<?php page_end(); ?>
