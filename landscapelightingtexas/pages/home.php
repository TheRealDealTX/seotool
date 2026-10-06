<?php defined('LLT') or die(http_response_code(404));
// Homepage. Primary keyword: "Landscape Lighting Texas" (used 14+ times in body copy).
$P['tools_js'] = true;
$P['preload'] = '/assets/img/architectural-uplighting-1600.webp';
global $CITY_POINTS;

// Texas outline (lon/lat), simplified, projected onto a 600x560 viewBox.
$tx = [[-103.04,36.5],[-100.0,36.5],[-100.0,34.56],[-99.2,34.37],[-98.5,34.1],[-97.9,33.88],[-97.2,33.85],[-96.6,33.8],[-95.8,33.86],[-95.3,33.9],[-94.6,33.65],[-94.04,33.55],
       [-94.04,32.0],[-93.85,31.4],[-93.6,31.0],[-93.7,30.3],[-93.85,29.7],[-94.7,29.35],[-95.1,29.05],[-95.9,28.6],[-96.6,28.3],[-97.2,27.75],[-97.4,27.2],[-97.4,26.6],[-97.15,25.95],
       [-97.7,26.05],[-98.3,26.15],[-99.1,26.45],[-99.45,27.0],[-99.5,27.5],[-100.1,28.1],[-100.4,28.6],[-100.7,29.1],[-101.4,29.77],[-102.0,29.8],[-102.4,29.78],[-102.7,29.65],
       [-103.0,29.1],[-103.3,29.0],[-103.8,29.25],[-104.3,29.55],[-104.6,29.95],[-104.7,30.4],[-105.0,30.7],[-105.6,31.1],[-106.2,31.5],[-106.6,31.95],[-103.06,32.0],[-103.04,36.5]];
$proj = fn($lon, $lat) => [round(($lon + 106.7) / 13.2 * 580 + 10, 1), round((36.6 - $lat) / 10.8 * 540 + 10, 1)];
$pts = implode(' ', array_map(fn($p) => implode(',', $proj($p[0], $p[1])), $tx));
$major = ['Austin', 'Houston', 'Dallas', 'San Antonio', 'El Paso', 'Lubbock', 'Corpus Christi', 'Amarillo'];
?>
<section class="hero" data-hero>
  <div class="hero-media" aria-hidden="true">
    <img class="hero-off" src="/assets/img/architectural-uplighting-1600.webp" alt="" width="1536" height="1024" fetchpriority="high">
    <img class="hero-on" src="/assets/img/architectural-uplighting-1600.webp" alt="" width="1536" height="1024">
  </div>
  <div class="hero-spot" aria-hidden="true"></div>
  <canvas class="fireflies" aria-hidden="true"></canvas>
  <div class="container hero-inner">
    <p class="hero-badge reveal"><b><?= icon('star', 12) ?> 4.9</b> 1,400+ Texas projects · 5-year warranty</p>
    <h1 class="display reveal">Landscape Lighting Texas: <span class="glow-text">Where Darkness Becomes Breathtaking</span></h1>
    <p class="lead reveal">Landscape Lighting Texas designs, installs and maintains custom LED outdoor lighting that makes Texas homes and businesses look their best after sunset — from moonlit live oaks to glowing limestone facades.</p>
    <div class="hero-actions reveal">
      <a class="btn btn-gold btn-lg magnetic" href="/quote/">Get Your Free Quote <?= icon('arrow', 18) ?></a>
      <a class="btn btn-ghost btn-lg" href="#simulator"><?= icon('sliders', 18) ?> Try the Lighting Simulator</a>
    </div>
    <div class="hero-trust reveal">
      <span><?= icon('shield', 18) ?> Licensed &amp; insured</span>
      <span><?= icon('moon', 18) ?> Free dusk consultation</span>
      <span><?= icon('award', 18) ?> 5-year workmanship warranty</span>
      <span><?= icon('pin', 18) ?> Serving all of Texas</span>
    </div>
  </div>
  <button type="button" class="hero-switch" data-light-switch aria-pressed="false" aria-label="Toggle the landscape lights"><span class="switch-track"></span><span class="switch-label">Lights off</span></button>
  <a class="scroll-cue" href="#intro" aria-label="Scroll down"><i></i>Scroll</a>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">
    <?php $cities = ['Austin', 'Houston', 'Dallas', 'San Antonio', 'Fort Worth', 'Plano', 'Frisco', 'The Woodlands', 'Sugar Land', 'Boerne', 'Georgetown', 'Corpus Christi', 'El Paso', 'Lubbock', 'McKinney', 'Southlake', 'Katy', 'New Braunfels'];
    for ($r = 0; $r < 2; $r++) foreach ($cities as $c) echo '<span>' . e($c) . '</span>'; ?>
  </div>
</div>

<section class="section" id="intro">
  <div class="container intro-grid">
    <div>
      <?php section_head('Texas’s outdoor lighting specialists', 'Your Home Deserves to Be <em>Seen</em> After Dark', '', 'left'); ?>
      <p class="lead-p reveal">You invested in the stone, the oaks, the pool and the patio. Then the sun goes down and it all disappears. Landscape Lighting Texas brings it back — with light that is designed, not just installed.</p>
      <p class="reveal" style="color:var(--muted)">Every Landscape Lighting Texas project starts the same way: a designer walks your property at dusk, when you can actually see how light behaves on your architecture and plants. From there we build a low-voltage LED plan with the right beam angles, color temperature and fixture placement for your home — then our crew installs it cleanly and fine-tunes every fixture after dark.</p>
      <?= checklist(['Professional-grade brass, copper and aluminum LED fixtures built for Texas heat and hail', 'Warm 2700K–3000K light that flatters limestone, brick and live oaks', 'Smart controls, dimming and astronomical timers on request', 'A 5-year workmanship warranty on every installation']) ?>
      <div class="hero-actions reveal"><a class="btn btn-gold magnetic" href="/about-us/">About Our Team</a><a class="btn btn-ghost" href="/gallery/">See Our Work</a></div>
    </div>
    <div class="intro-collage reveal-zoom">
      <figure class="c1"><img src="/assets/img/oak-tree-uplighting-800.webp" alt="Live oak uplighting by Landscape Lighting Texas" width="800" height="533" loading="lazy" data-parallax-img></figure>
      <figure class="c2"><img src="/assets/img/garden-pathway-lighting-800.webp" alt="Garden pathway lighting installed in Texas" width="800" height="533" loading="lazy"></figure>
      <div class="badge-float"><strong><span data-count="1400">0</span>+</strong><span>Texas properties lit</span></div>
    </div>
  </div>
</section>

<section class="dusk" data-dusk aria-label="From sunset to fully lit">
  <div class="dusk-sticky">
    <div class="dusk-sky"></div>
    <div class="dusk-sun"></div>
    <div class="dusk-photo" aria-hidden="true">
      <img class="d-off" src="/assets/img/landscape-lighting-texas-home-1600.webp" alt="" width="1000" height="667" loading="lazy">
      <img class="d-on" src="/assets/img/landscape-lighting-texas-home-1600.webp" alt="" width="1000" height="667" loading="lazy">
      <img class="d-full" src="/assets/img/landscape-lighting-texas-home-1600.webp" alt="" width="1000" height="667" loading="lazy">
    </div>
    <div class="container dusk-head"><p class="eyebrow">Scroll from sunset to showtime</p></div>
    <div class="container dusk-panel">
      <div class="dusk-steps">
        <div class="dusk-step is-active"><span class="dusk-time">7:42 PM · Sunset</span><h3>The sun sets on another Texas evening.</h3><p>Without a plan, your yard fades into flat, featureless shadow — and the front walk becomes a guessing game.</p></div>
        <div class="dusk-step"><span class="dusk-time">7:58 PM · Paths on</span><h3>First, the way home lights up.</h3><p>Soft, glare-free path light guides guests from the curb to the door and makes every step safe.</p></div>
        <div class="dusk-step"><span class="dusk-time">8:05 PM · Trees on</span><h3>Then the trees come alive.</h3><p>Uplit trunks and canopy light add depth and drama — the signature of Landscape Lighting Texas design.</p></div>
        <div class="dusk-step"><span class="dusk-time">8:10 PM · Full scene</span><h3>Finally, the whole home glows.</h3><p>Architecture, landscape and living spaces balanced into one scene — automatically, every night.</p></div>
      </div>
    </div>
    <div class="dusk-dots" aria-hidden="true"><span class="is-active"></span><span></span><span></span><span></span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('What we do', 'Landscape Lighting Texas Services for <em>Every</em> Property', 'From intimate garden accents to full estate illumination, Landscape Lighting Texas designs, installs and maintains every layer of outdoor light.'); ?>
    <?php service_cards(); ?>
    <p class="reveal" style="text-align:center;margin-top:40px"><a class="btn btn-ghost" href="/services/">Compare All Services <?= icon('arrow', 16) ?></a></p>
  </div>
</section>

<section class="section alt">
  <div class="container grid-2" style="align-items:center">
    <div>
      <?php section_head('See the difference', 'Drag to Turn the Lights On', '', 'left'); ?>
      <p class="reveal" style="color:var(--muted)">This is the same Texas home before and after a Landscape Lighting Texas design. Slide across to see what layered uplighting, path lights and tree lighting do to a property that would otherwise vanish at night.</p>
      <?= checklist(['Facade grazing brings out the texture of stone', 'Path lights create a safe, inviting route to the door', 'Tree uplights frame the home and add depth']) ?>
    </div>
    <?php before_after('architectural-uplighting', 'Texas stone home with professional landscape lighting'); ?>
  </div>
</section>

<section class="hgallery" data-hgallery aria-label="Featured work">
  <div class="hgallery-sticky">
    <div class="container"><?php section_head('Our work', 'Texas Properties, <em>Transformed</em>', '', 'left'); ?></div>
    <div class="hgallery-track">
      <?php $work = [['architectural-uplighting', 'Architectural Uplighting', 'Grazed limestone and lit gables'], ['oak-tree-uplighting', 'Live Oak Uplighting', 'A cathedral-like canopy'], ['pool-lighting', 'Pool Lighting', 'Resort nights in the backyard'],
          ['garden-pathway-lighting', 'Garden Pathway', 'Warm, guided arrivals'], ['driveway-lighting', 'Driveway Bollards', 'Safe, elegant approach'], ['patio-lighting', 'Patio String Lighting', 'Evenings outdoors, extended']];
      foreach ($work as $i => [$img, $t, $s]): ?>
      <figure class="hg-item"><img src="<?= img_url($img) ?>" alt="<?= e($t) ?> project by Landscape Lighting Texas" width="1536" height="1024" loading="lazy"><span class="hg-num">0<?= $i + 1 ?></span><figcaption><strong><?= e($t) ?></strong><span><?= e($s) ?></span></figcaption></figure>
      <?php endforeach; ?>
    </div>
    <div class="hgallery-bar"><span></span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php stats([['1400', '+', 'Projects completed'], ['5', '+', 'Years lighting Texas'], ['4.9', '★', 'Average customer rating'], ['5', '-yr', 'Workmanship warranty']]); ?>
  </div>
</section>

<section class="section alt" id="simulator">
  <div class="container">
    <?php section_head('Interactive', 'Design Your Night in <em>Real Time</em>', 'Switch on facade, tree, path and entry lighting, dim them and test color temperatures — the same layers a Landscape Lighting Texas designer balances on your property.'); ?>
    <div class="reveal"><?php widget_simulator(true); ?></div>
    <p class="reveal" style="text-align:center;margin-top:28px"><a class="link-arrow" href="/tools/lighting-design-simulator/">Open the full simulator <?= icon('arrow', 16) ?></a></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('How it works', 'From Vision to Illumination in Four Steps', 'A proven process that keeps your Landscape Lighting Texas project simple, clean and exactly what you imagined.'); ?>
    <ol class="steps">
      <li><h3>Free Dusk Consultation</h3><p>We visit at nightfall to see how light interacts with your home, trees and outdoor spaces. No pressure — just ideas.</p></li>
      <li><h3>Custom Design</h3><p>You get a lighting plan with fixture placement, beam angles, color temperature, zones and a transparent, itemized quote.</p></li>
      <li><h3>Expert Installation</h3><p>Our crew installs low-voltage wiring with narrow trenching and hand-digging around roots — most homes are done in a day.</p></li>
      <li><h3>The Reveal &amp; Tune</h3><p>We walk the property with you after dark and fine-tune every angle and intensity until it is exactly right.</p></li>
    </ol>
  </div>
</section>

<section class="section alt">
  <div class="container map-wrap">
    <div>
      <?php section_head('Statewide service', 'Landscape Lighting Texas Serves the Whole Lone Star State', '', 'left'); ?>
      <p class="reveal" style="color:var(--muted)">From Hill Country limestone and Houston’s humid gardens to North Texas estates, West Texas skies and the salt air of the Gulf Coast, Landscape Lighting Texas designs every system for local conditions — fixtures, finishes, wiring and controls included.</p>
      <ul class="pill-list reveal" style="margin:24px 0 30px">
        <?php global $AREAS; foreach ($AREAS as $slug => $a) echo '<li><a href="/areas/' . $slug . '/">' . e($a[0]) . '</a></li>'; ?>
      </ul>
      <a class="btn btn-gold magnetic reveal" href="/areas/">Find Your City</a>
    </div>
    <svg class="tx-map" viewBox="0 0 600 560" role="img" aria-label="Map of Texas showing cities served by Landscape Lighting Texas">
      <defs><radialGradient id="txFill" cx="55%" cy="60%" r="70%"><stop offset="0" stop-color="#1b2547"/><stop offset="1" stop-color="#0a1022"/></radialGradient></defs>
      <polygon class="tx-shape" points="<?= $pts ?>"/>
      <polygon class="tx-outline" points="<?= $pts ?>"/>
      <?php $i = 0; foreach ($CITY_POINTS as $name => [$lon, $lat]): [$x, $y] = $proj($lon, $lat); $isMajor = in_array($name, $major, true); ?>
      <g class="tx-city<?= $isMajor ? ' major' : '' ?>" style="--d:<?= number_format($i++ * 0.09, 2) ?>s"><title><?= e($name) ?></title>
        <circle class="halo" cx="<?= $x ?>" cy="<?= $y ?>" r="<?= $isMajor ? 7 : 5 ?>"/><circle class="dot" cx="<?= $x ?>" cy="<?= $y ?>" r="<?= $isMajor ? 3.5 : 2.5 ?>"/>
        <text x="<?= $x + 9 ?>" y="<?= $y + 4 ?>"><?= e($name) ?></text></g>
      <?php endforeach; ?>
    </svg>
  </div>
</section>

<section class="section">
  <div class="container">
    <?php section_head('Reviews', 'What Texas Homeowners Say', 'Real words from Landscape Lighting Texas clients across the state.'); ?>
    <?php testimonials(); ?>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <?php section_head('Free tools', 'Plan Your Project With Our <em>Lighting Tools</em>', 'Estimate costs, size a transformer, preview color temperature and time your lights to Texas sunsets — free tools from Landscape Lighting Texas.'); ?>
    <?php tool_cards(); ?>
  </div>
</section>

<section class="section">
  <div class="container grid-2">
    <div>
      <?php section_head('Why choose us', 'Why Homeowners Choose Landscape Lighting Texas', '', 'left'); ?>
      <div class="prose reveal">
        <p>Plenty of companies can stake a few lights in a flower bed. Landscape Lighting Texas is different because we treat light as design. We think about where people stand, what they see from the street and the patio, and how each beam adds to the whole — so your home looks balanced and natural, never like a parking lot.</p>
        <p>We also build for Texas. That means fixtures that shrug off 100-degree summers, hail and irrigation; cable sized so the last light on the run is as bright as the first; and connections sealed against our clay and caliche soils. When you hire Landscape Lighting Texas, you get a system made to work beautifully for many years — backed by a 5-year workmanship warranty.</p>
      </div>
    </div>
    <div class="grid-2" style="gap:18px">
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('bulb') ?></span><h3>Design first</h3><p>Every plan is drawn for your property after a dusk walk-through.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('shield') ?></span><h3>Built for Texas</h3><p>Brass, copper and sealed LEDs that handle heat, hail and humidity.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('leaf') ?></span><h3>Efficient LEDs</h3><p>75–80% less energy than halogen; most systems cost $10–$25 a month to run.</p></div>
      <div class="info-card reveal glow-card"><span class="info-icon"><?= icon('award') ?></span><h3>5-year warranty</h3><p>Workmanship covered, plus manufacturer warranties on fixtures.</p></div>
    </div>
  </div>
</section>

<?php faqs([
    ['How much does landscape lighting cost in Texas?', 'Most residential projects from Landscape Lighting Texas fall between $2,500 and $12,000, depending on property size, the number of fixtures and installation complexity. A starter system for a typical home runs $2,500–$5,000; full estate lighting can exceed $20,000. Try our <a href="/landscape-lighting-cost-calculator/">cost calculator</a> for a planning estimate, then request a free, itemized quote.'],
    ['Are LED landscape lights energy efficient?', 'Yes. Modern LED landscape lighting uses roughly 75–80% less energy than halogen. A typical whole-property LED system running six hours a night costs about $10–$25 a month to operate, and LEDs last tens of thousands of hours. See the numbers in our <a href="/tools/energy-savings-calculator/">LED energy savings calculator</a>.'],
    ['How long does installation take?', 'Most residential installations are completed in one day. Larger estates and commercial properties may take two to three days. We always finish with a nighttime walk-through to aim and balance every fixture.'],
    ['Will installation damage my lawn or landscaping?', 'No. Low-voltage cable is buried with narrow-blade trenching that closes up quickly, and we hand-dig around tree roots and established plantings. Any turf we disturb is restored before we leave.'],
    ['What warranty do you offer?', 'Every Landscape Lighting Texas installation carries a 5-year workmanship warranty. Fixtures also carry their manufacturers’ warranties. If something fails because of our installation, we fix it at no charge.'],
    ['Can I add to my system later?', 'Absolutely. We size transformers with room to grow, so adding fixtures, new zones or smart controls later is simple as your landscape matures.'],
], 'Common Questions, Answered'); ?>

<section class="section alt">
  <div class="container">
    <?php section_head('Resources', 'Landscape Lighting Guides &amp; Ideas', 'Practical advice from the Landscape Lighting Texas design team.'); ?>
    <div class="card-grid posts-grid"><?php foreach (array_slice(posts(), 0, 3) as $p) echo post_card($p); ?></div>
    <p class="reveal" style="text-align:center;margin-top:36px"><a class="btn btn-ghost" href="/blog/">Read More Articles <?= icon('arrow', 16) ?></a></p>
  </div>
</section>

<section class="section" id="quote">
  <div class="container grid-2" style="align-items:center">
    <div>
      <?php section_head('Free quote', 'Let’s Light Up Your Property', '', 'left'); ?>
      <p class="reveal" style="color:var(--muted)">Tell us a little about your home and what you would like to see at night. A Landscape Lighting Texas designer will reach out within one business day to schedule your free dusk consultation.</p>
      <?= checklist(['No-obligation consultation at your property', 'Custom lighting plan designed for your landscape', 'Transparent, itemized quote — no surprises', 'Licensed, insured Texas professionals', '5-year workmanship warranty']) ?>
      <p class="reveal">Prefer to talk? Call <a href="<?= PHONE_HREF ?>"><?= PHONE ?></a> · <?= HOURS ?></p>
    </div>
    <div class="reveal"><?php quote_form('Request Your Free Quote', 'Homepage'); ?></div>
  </div>
</section>

<?php cta_band('Ready to Transform Your Property After Dark?', 'Join more than 1,400 Texas property owners who have discovered what professional landscape lighting can do. Landscape Lighting Texas makes it simple from the first call to the final reveal.'); ?>
