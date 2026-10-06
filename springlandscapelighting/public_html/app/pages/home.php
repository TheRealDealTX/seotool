<?php defined('SLT') || exit;
require_once APP . '/partials/house-scene.php';
$meta['preload'] = '/assets/img/Spring-Landscape-Lighting-BG-1.webp';
$meta['body_class'] = 'pg-home';
add_schema(['@type' => 'Service', 'name' => 'Landscape lighting design and installation', 'provider' => ['@id' => SITE_URL . '/#business'],
    'areaServed' => 'Spring, TX', 'serviceType' => 'Landscape lighting', 'url' => SITE_URL . '/']);
$posts = POSTS; uasort($posts, fn($a, $b) => strcmp($b['date'], $a['date']));
?>
<!-- ============ HERO ============ -->
<section class="hero" aria-labelledby="hero-title">
  <div class="hero__bg" data-parallax="0.18"><img src="/assets/img/Spring-Landscape-Lighting-BG-1.webp" alt="Ornamental grasses and trees glowing under warm landscape lighting at night" width="1920" height="1277" fetchpriority="high"></div>
  <div class="hero__dark" aria-hidden="true"></div>
  <div class="hero__shade" aria-hidden="true"></div>
  <canvas class="fireflies" data-count="40" aria-hidden="true"></canvas>
  <span class="hero__lamp" aria-hidden="true">Move your cursor to light the garden</span>
  <div class="wrap">
    <div class="hero__inner">
      <span class="eyebrow eyebrow--glow" data-reveal>Landscape lighting design &amp; installation · Spring, Texas</span>
      <h1 class="hero__title" id="hero-title" data-split>Spring Landscape Lighting: make your home <em>exceptional</em> after sunset</h1>
      <p class="hero__sub" data-reveal data-delay="2">Spring Landscape Lighting designs, installs and maintains custom low-voltage LED lighting that adds warmth, safety and curb appeal to homes across Spring, Klein and North Houston. Every plan is built around your property and finished with a night-time fine-tuning visit.</p>
      <div class="btn-row" data-reveal data-delay="3">
        <a class="btn btn--glow btn--lg" href="/quote/" data-magnetic><?= icon('sparkles') ?>Get a Free Lighting Plan</a>
        <a class="btn btn--ghost btn--lg" href="#visualizer"><?= icon('sliders-horizontal') ?>Try the Lighting Visualizer</a>
      </div>
      <div class="hero__badges" data-reveal data-delay="4">
        <span class="hero__badge"><?= icon('zap') ?><span><strong>Low-voltage LED</strong> systems</span></span>
        <span class="hero__badge"><?= icon('compass') ?><span><strong>Custom</strong> site-specific design</span></span>
        <span class="hero__badge"><?= icon('moon') ?><span><strong>Night-time</strong> aiming visit</span></span>
        <span class="hero__badge"><?= icon('map-pin') ?><span><strong>Local</strong> to Spring, TX</span></span>
      </div>
    </div>
  </div>
  <div class="hero__hint" aria-hidden="true"><i></i>Scroll</div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">
  <?php for ($k = 0; $k < 2; $k++): foreach (['Architectural <em>uplighting</em>', 'Path &amp; driveway', 'Live oak <em>moonlighting</em>', 'Patio &amp; pool', 'Smart <em>controls</em>', 'LED upgrades', 'Spring Landscape Lighting'] as $t): ?>
  <span class="marquee__item"><?= $t ?></span>
  <?php endforeach; endfor; ?>
</div></div>

<!-- ============ INTRO ============ -->
<section class="sec">
  <div class="wrap split">
    <div>
      <span class="eyebrow" data-reveal>Outdoor lighting designed for Spring, Texas</span>
      <h2 data-split>Lighting that changes how you <em class="glow">experience</em> home</h2>
      <p data-reveal data-delay="1">Every property has its own rhythm. Spring Landscape Lighting uses layered light to reveal architecture, guide movement and create a calm, polished atmosphere, without flooding your yard or your neighbors' windows.</p>
      <p data-reveal data-delay="2">Great landscape lighting is not about adding the most fixtures. It is about understanding how you use your outdoor spaces, which features deserve attention, and where darkness should remain. That restraint is what makes a home feel finished at night instead of overlit.</p>
      <ul class="checks" data-reveal data-delay="3">
        <li><?= icon('check') ?><span><strong>Site-specific design.</strong> Plans built around your architecture, trees, viewing angles and routines.</span></li>
        <li><?= icon('check') ?><span><strong>Clean, careful installation.</strong> Concealed wire, protected beds and precisely aimed fixtures.</span></li>
        <li><?= icon('check') ?><span><strong>Built for Gulf Coast weather.</strong> Quality low-voltage components installed for heat, humidity and heavy rain.</span></li>
      </ul>
      <div class="btn-row" data-reveal data-delay="3"><a class="btn btn--glow" href="/about-us/" data-magnetic>About Spring Landscape Lighting <?= icon('arrow-right') ?></a></div>
    </div>
    <div data-reveal="right">
      <div class="frame">
        <img src="/assets/img/Spring-Landscape-Lighting-BG-2.webp" alt="Sculptural LED garden light glowing on a lawn at night" loading="lazy" data-parallax="0.08">
        <div class="frame__tag"><?= icon('lightbulb') ?><span><strong>Warm 2700K–3000K light</strong>The color most Spring homes look best in.</span></div>
      </div>
    </div>
  </div>
</section>

<!-- ============ DUSK TO NIGHT (scroll scene) ============ -->
<section class="dusk" aria-label="Scroll to watch a home light up layer by layer">
  <div class="dusk__sticky">
    <div class="dusk__sky"></div><div class="dusk__stars"></div><div class="dusk__moon"></div>
    <div class="dusk__copy">
      <span class="eyebrow eyebrow--glow">Scroll to light it up</span>
      <h2>From sunset to <em class="glow">showpiece</em></h2>
      <div class="dusk__steps">
        <p class="dusk__step is-on">The sun goes down and a beautiful home <strong>disappears</strong> into the dark.</p>
        <p class="dusk__step"><strong>Architectural lighting</strong> brings brick, columns and rooflines back to life.</p>
        <p class="dusk__step"><strong>Path lighting</strong> makes every arrival feel safe and welcoming.</p>
        <p class="dusk__step"><strong>Tree lighting</strong> adds height, depth and drama to the landscape.</p>
        <p class="dusk__step"><strong>Patio lighting</strong> keeps outdoor living going long after dark.</p>
      </div>
      <div class="dusk__bar"><span></span><span></span><span></span><span></span></div>
    </div>
    <div class="dusk__scene scene" style="--lc:#ffc27a"><?= house_scene('dusk', false) ?></div>
    <span class="dusk__label">A layered plan by Spring Landscape Lighting</span>
  </div>
</section>

<!-- ============ SERVICES ============ -->
<section class="sec sec--forest" id="services">
  <div class="wrap">
    <?php section_head('Our services', 'Landscape lighting services for every part of your property', 'From the first uplight on your facade to the smart timer that runs it all, Spring Landscape Lighting handles design, installation, repair and upgrades.'); ?>
    <div class="grid-3">
      <?php $i = 0; foreach (SERVICES as $k => $s) echo service_card($k, $s, $i++); ?>
    </div>
    <div class="btn-row btn-row--center" data-reveal><a class="btn btn--ghost" href="/services/">View all services <?= icon('arrow-right') ?></a></div>
  </div>
</section>

<!-- ============ BEFORE / AFTER ============ -->
<section class="sec">
  <div class="wrap split split--rev">
    <div>
      <span class="eyebrow" data-reveal>See the difference</span>
      <h2 data-split>Same garden. <em class="glow">Different night.</em></h2>
      <p data-reveal data-delay="1">Drag the slider. On the left, what most yards look like after sunset: flat and unreadable. On the right, what thoughtful accent lighting does to texture, depth and mood.</p>
      <p data-reveal data-delay="2">Spring Landscape Lighting plans each fixture for an intended effect: grazing light across textured grasses, soft uplight into a canopy, a warm pool of light where you actually walk. Nothing random, nothing glaring.</p>
      <div class="btn-row" data-reveal data-delay="3"><a class="btn btn--glow" href="/inspiration/" data-magnetic>Explore lighting ideas <?= icon('arrow-right') ?></a></div>
    </div>
    <div data-reveal="left">
      <div class="ba">
        <img src="/assets/img/Spring-Landscape-Lighting-BG-1-960.webp" alt="Garden with landscape lighting on" loading="lazy">
        <img class="ba__before" src="/assets/img/Spring-Landscape-Lighting-BG-1-960.webp" alt="" loading="lazy">
        <span class="ba__tag ba__tag--l">Lights off</span><span class="ba__tag ba__tag--r">Lights on</span>
        <div class="ba__line"></div><div class="ba__handle" aria-hidden="true">⇆</div>
        <input type="range" min="0" max="100" value="50" aria-label="Compare lights off and lights on">
      </div>
    </div>
  </div>
</section>

<!-- ============ VISUALIZER ============ -->
<section class="sec sec--forest" id="visualizer">
  <div class="wrap">
    <?php section_head('Interactive', 'Design your own night in seconds', 'Turn each lighting layer on and off, slide the color temperature from candle-warm to moonlight, and watch the estimated load and running cost update live.'); ?>
    <div data-reveal="zoom"><?php tool_embed('lighting-visualizer', false); ?></div>
  </div>
</section>

<!-- ============ FACTS ============ -->
<section class="sec--tight">
  <div class="wrap">
    <div class="stats" data-reveal>
      <div class="stat"><strong><span data-count-to="12">12</span>V</strong><p>Low-voltage systems: safer around beds, pools and kids</p></div>
      <div class="stat"><strong>~<span data-count-to="75">75</span>%</strong><p>Less energy for a 5 W LED vs a 20 W halogen lamp</p></div>
      <div class="stat"><strong><span data-count-to="2700">2700</span>K</strong><p>The warm white we start most Spring homes with</p></div>
      <div class="stat"><strong><span data-count-to="6">6</span></strong><p>Steps from first call to final night-time adjustment</p></div>
    </div>
  </div>
</section>

<!-- ============ PROCESS ============ -->
<section class="sec" id="process">
  <div class="wrap">
    <?php section_head('Simple from start to finish', 'From first walkthrough to final night-time adjustment', 'Our process keeps every project clear, collaborative and focused on the finished effect. Here is how Spring Landscape Lighting takes a property from dark to dialed in.'); ?>
    <?php process_strip(); ?>
    <div class="btn-row btn-row--center" data-reveal><a class="btn btn--ghost" href="/our-process/">See the full process <?= icon('arrow-right') ?></a></div>
  </div>
</section>

<!-- ============ WHY (light) ============ -->
<section class="sec sec--light">
  <div class="wrap">
    <?php section_head('Why homeowners choose us', 'A better lighting plan starts with better listening', 'Spring Landscape Lighting is a design-led company. These principles shape every system we install.'); ?>
    <div class="kv">
      <div class="kv__item" data-reveal><?= icon('message-circle') ?><h3>We listen before we design</h3><p>The system should support the way you live, not force your property into a preset package.</p></div>
      <div class="kv__item" data-reveal data-delay="1"><?= icon('eye') ?><h3>We light with restraint</h3><p>Balance, contrast and comfortable brightness instead of flooding every surface. Darkness is part of the design.</p></div>
      <div class="kv__item" data-reveal data-delay="2"><?= icon('shield-check') ?><h3>We plan for the long run</h3><p>Fixture quality, connections, drainage, plant growth and Texas weather are all considered from day one.</p></div>
      <div class="kv__item" data-reveal><?= icon('leaf') ?><h3>We respect the landscape</h3><p>Wire is concealed, beds are protected, roots are avoided and the site is left clean.</p></div>
      <div class="kv__item" data-reveal data-delay="1"><?= icon('moon') ?><h3>We finish after dark</h3><p>Fixtures are aimed and adjusted at night, when glare, shadows and balance can actually be judged.</p></div>
      <div class="kv__item" data-reveal data-delay="2"><?= icon('map-pin') ?><h3>We are local</h3><p>Spring Landscape Lighting knows the trees, soils, HOAs and home styles common across North Houston.</p></div>
    </div>
  </div>
</section>

<!-- ============ TOOLS ============ -->
<section class="sec">
  <div class="wrap">
    <?php section_head('Free planning tools', 'Plan smarter with our lighting calculators', 'Built by Spring Landscape Lighting for homeowners: estimate fixtures, size a transformer, compare LED savings, check running costs and more.'); ?>
    <div class="grid-3">
      <?php $i = 0; foreach (TOOLS as $k => $t) { if ($k === 'lighting-visualizer') continue; echo tool_card($k, $t, $i++); } ?>
    </div>
  </div>
</section>

<!-- ============ LOCAL ============ -->
<section class="sec sec--forest">
  <div class="wrap split">
    <div>
      <span class="eyebrow" data-reveal>Local landscape lighting in Spring, TX</span>
      <h2 data-split>Designed for North Houston homes and Texas conditions</h2>
      <p data-reveal data-delay="1">Spring properties often combine mature live oaks and pines, deep front yards, brick or stone elevations, pools, patios and dense planting. A successful plan has to work with all of it, and survive heat, humidity, heavy rain, irrigation and shifting soil.</p>
      <p data-reveal data-delay="2">Spring Landscape Lighting provides custom outdoor lighting for homeowners throughout Spring, Klein, Champion Forest, Gleannloch Farms, Augusta Pines, The Woodlands and surrounding communities.</p>
      <div class="pills" data-reveal data-delay="3">
        <?php foreach (AREAS as $k => $a): ?><a class="pill" href="/service-areas/<?= $k ?>/"><?= icon('map-pin') ?><?= e($a['short']) ?></a><?php endforeach; ?>
      </div>
    </div>
    <div class="areamap" data-reveal="zoom" aria-hidden="true">
      <span class="areamap__ring" style="--i:6%"></span><span class="areamap__ring" style="--i:22%;animation-direction:reverse"></span><span class="areamap__ring" style="--i:38%"></span>
      <span class="areamap__pin areamap__pin--main" style="--x:50%;--y:50%"><i></i>Spring</span>
      <span class="areamap__pin" style="--x:58%;--y:16%;--d:.4s"><i></i>The Woodlands</span>
      <span class="areamap__pin" style="--x:22%;--y:30%;--d:.8s"><i></i>Gleannloch Farms</span>
      <span class="areamap__pin" style="--x:34%;--y:72%;--d:1.2s"><i></i>Champion Forest</span>
      <span class="areamap__pin" style="--x:66%;--y:78%;--d:1.6s"><i></i>Klein</span>
      <span class="areamap__pin" style="--x:80%;--y:42%;--d:2s"><i></i>Augusta Pines</span>
    </div>
  </div>
</section>

<!-- ============ BLOG ============ -->
<section class="sec">
  <div class="wrap">
    <?php section_head('Project inspiration & guides', 'Warm, refined, and designed to belong', 'Lighting ideas, planning guides and honest cost advice for homes in Spring, The Woodlands, Klein and nearby North Houston communities.'); ?>
    <div class="grid-3">
      <?php $i = 0; foreach ($posts as $k => $p) { if ($i++ >= 3) break; echo post_card($k, $p); } ?>
    </div>
    <div class="btn-row btn-row--center" data-reveal><a class="btn btn--ghost" href="/blog/">See more articles <?= icon('arrow-right') ?></a></div>
  </div>
</section>

<!-- ============ QUOTE ============ -->
<section class="sec sec--forest" id="quote">
  <div class="wrap split">
    <div>
      <span class="eyebrow" data-reveal>Complimentary consultation</span>
      <h2 data-split>Request your free lighting plan</h2>
      <p data-reveal data-delay="1">Tell us a little about your property. Spring Landscape Lighting will contact you to talk through your ideas, answer questions and schedule a walkthrough. You do not need to know how many fixtures you want; a short description is enough to start.</p>
      <div class="ccards" data-reveal data-delay="2">
        <a class="ccard" href="tel:<?= PHONE_TEL ?>"><?= icon('phone') ?><span><small>Call us</small><strong><?= PHONE ?></strong></span></a>
        <a class="ccard" href="mailto:<?= EMAIL ?>"><?= icon('mail') ?><span><small>Email</small><strong><?= EMAIL ?></strong></span></a>
      </div>
    </div>
    <div class="formcard" data-reveal="right">
      <h3>Tell us about your project</h3>
      <?php quote_form('home'); ?>
    </div>
  </div>
</section>

<!-- ============ FAQ ============ -->
<section class="sec" id="faq">
  <div class="wrap" style="max-width:900px">
    <?php section_head('Helpful answers', 'Questions homeowners ask before they start', 'Still deciding what your home needs? Here is what people most often ask Spring Landscape Lighting.'); ?>
    <?php faq_block([
        ['How much does landscape lighting cost in Spring, TX?', 'Cost depends on property size, the number of fixtures and zones, fixture quality, wire runs, controls and installation complexity. Spring Landscape Lighting provides a custom plan and a clear proposal after reviewing your property, so you know exactly what you are getting.'],
        ['Do you use LED low-voltage lighting?', 'Yes. Professional low-voltage LED systems use a fraction of the energy of older halogen lamps, last far longer, and give precise control over brightness, beam spread and color temperature.'],
        ['Can you repair or upgrade an existing lighting system?', 'Yes. We troubleshoot dim or dead fixtures, damaged wire, failed transformers, poor placement, outdated lamps and timer problems, and we convert halogen systems to LED.'],
        ['Will installation damage my landscaping?', 'We use careful methods to minimize disruption: wire is buried and concealed, planting beds are protected, tree roots are avoided, and work areas are left clean.'],
        ['Can the lights run automatically?', 'Yes. Systems can use astronomical timers that track sunset all year, photocells, separate zones with different schedules, dimming and app-based smart control.'],
        ['How much electricity will it use?', 'Usually very little. A 20-fixture LED system at 5 watts each running six hours a night uses about 18 kWh a month, roughly $3 at $0.16 per kWh. Try our free energy cost calculator to test your own numbers.'],
    ], '', false); ?>
    <div class="btn-row btn-row--center" data-reveal><a class="btn btn--ghost" href="/faq/">More answers <?= icon('arrow-right') ?></a></div>
  </div>
</section>

<?php cta_band(); ?>
