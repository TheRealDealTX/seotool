<?php
defined('HA_ROOT') || exit;
$counts = Listings::areaCounts();
$groups = [
    'Inner Loop' => ['downtown-houston-apartments', 'houston-heights-apartments', 'montrose-apartments', 'houston-medical-center-apartments', 'river-oaks-apartments', 'rice-military-apartments'],
    'West'       => ['galleria-apartments-houston', 'memorial-city-apartments', 'spring-branch-apartments', 'apartments-in-katy'],
    'North'      => ['the-woodlands-apartments', 'apartments-in-cypress-tx', 'apartments-in-conroe-tx', 'apartments-humble-tx'],
    'South & Bay' => ['sugar-land-apartments', 'apartments-in-richmond-tx', 'baytown-apartments', 'apartments-in-galveston'],
];
$homeFaqs = [
    ['Is Houston Apartments really free for renters?', 'Yes. Houston Apartments is paid by the apartment communities when you sign a lease, so our locating service costs you nothing. Lease through us and you can also get up to $' . SITE['cashback'] . ' back.'],
    ['How does the draw-on-map search work?', 'Open the map search, tap “Draw area” and trace any shape with your mouse or finger – around your office, a school zone or a stretch of the Katy Freeway. Only Houston apartments inside your shape stay on the list, and every filter still applies.'],
    ['What is the average rent for Houston apartments?', 'Most one-bedroom Houston apartments lease between about $1,100 and $1,700 a month, with Inner Loop high-rises above that and suburbs such as Katy, Cypress and Humble below it. Use the price filter to see live starting rents for each community.'],
    ['Which Houston neighborhoods are best for apartments?', 'It depends on your commute and lifestyle: the Heights and Montrose for walkable character, Downtown and Midtown for high-rise living, the Medical Center for hospital staff, and Katy, Sugar Land or The Woodlands for space and top-rated schools.'],
    ['Can Houston Apartments help with broken leases or past evictions?', 'Often, yes. Many communities have second-chance criteria. Tell your locator about your situation privately and we’ll only send properties where your application has a real chance of approval.'],
];
$schemaFaq = ['@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array_map(fn ($f) => ['@type' => 'Question', 'name' => $f[0], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f[1]]], $homeFaqs)];
?>
<script type="application/ld+json"><?= json_encode($schemaFaq, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) ?></script>

<section class="hero">
  <div class="hero-bg" aria-hidden="true">
    <span class="sun"></span>
    <span class="cloud c1"></span><span class="cloud c2"></span><span class="cloud c3"></span>
    <div class="hero-skyline"></div>
  </div>
  <div class="wrap hero-grid">
  <div class="hero-inner">
    <p class="eyebrow fade-up"><span class="dot-live"></span> Free Houston apartment locator · Since <?= SITE['founded'] ?></p>
    <h1 class="hero-title fade-up d1">Houston Apartments for Rent<br><span class="grad-text">find your <span class="typer" data-words='["luxury high-rise","pet-friendly 1-bedroom","Heights hideaway","move-in special","Katy family home base"]'>luxury high-rise</span></span></h1>
    <p class="hero-sub fade-up d2">Search Houston apartments on a live map, draw the exact area you want to live in, and filter by rent, bedrooms, pets and amenities. When you’re ready, a Houston Apartments locator books the tours – and you can earn a move-in reward of up to $<?= SITE['cashback'] ?>.</p>

    <form class="hero-search fade-up d3" action="/apartments/" method="get" role="search">
      <label class="hs-field hs-where">
        <span>Where</span>
        <input name="q" list="area-list" placeholder="Neighborhood, ZIP or community" autocomplete="off">
        <datalist id="area-list"><?php foreach (AREAS as $a): ?><option value="<?= e($a['name']) ?>"><?php endforeach ?></datalist>
      </label>
      <label class="hs-field">
        <span>Beds</span>
        <select name="beds"><option value="">Any</option><option value="0">Studio</option><option value="1">1 Bed</option><option value="2">2 Beds</option><option value="3">3 Beds</option><option value="4">4+ Beds</option></select>
      </label>
      <label class="hs-field">
        <span>Max rent</span>
        <select name="price_max"><option value="">Any</option><?php foreach ([1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000] as $p): ?><option value="<?= $p ?>">$<?= number_format($p) ?></option><?php endforeach ?></select>
      </label>
      <button class="btn btn-grad hs-go" type="submit"><span class="ico ico-search" aria-hidden="true"></span> Search</button>
    </form>
    <div class="hero-chips fade-up d4">
      <a class="chip" href="/apartments/?draw=1"><span class="ico ico-lasso" aria-hidden="true"></span> Draw on map</a>
      <a class="chip" href="/apartments/pet-friendly/">Pet friendly</a>
      <a class="chip" href="/apartments/under-1300/">Under $1,300</a>
      <a class="chip" href="/apartments/built-2020-or-later/">Newer builds</a>
      <a class="chip" href="/apartments/?beds=2,3">2–3 bedrooms</a>
    </div>
  </div>
  <div class="hero-collage fade-up d2" aria-hidden="true">
    <?php foreach (array_slice($featured, 0, 3) as $k => $c): ?>
      <a class="hc hc<?= $k ?>" href="<?= e($c['url']) ?>" tabindex="-1"><img src="<?= e($c['photos'][0] ?? '/assets/img/og-default.png') ?>" alt="" width="420" height="300"><span><strong><?= e($c['name']) ?></strong><small><?= e($c['hood']) ?></small></span></a>
    <?php endforeach ?>
    <span class="hc-badge b-draw"><span class="ico ico-lasso"></span> Draw your area</span>
    <span class="hc-badge b-pet">🐾 Pet friendly</span>
  </div>
  </div>
</section>

<section class="stats" id="stats">
  <div class="wrap stats-grid">
    <div class="stat reveal"><strong data-count="<?= max(1, $stats['count']) ?>">0</strong><span>Houston apartment communities on the map</span></div>
    <div class="stat reveal d1"><strong data-count="<?= count(AREAS) ?>">0</strong><span>neighborhoods &amp; suburbs covered</span></div>
    <div class="stat reveal d2"><strong>$<span data-count="<?= SITE['cashback'] ?>">0</span></strong><span>move-in reward when you lease with us</span></div>
    <div class="stat reveal d3"><strong>$<span data-count="0">0</span></strong><span>cost to renters – ever</span></div>
  </div>
</section>

<section class="section draw-showcase">
  <div class="wrap split">
    <div class="split-copy reveal">
      <span class="pill">New · Map search</span>
      <h2>Draw your own Houston Apartments search area</h2>
      <p>Neighborhood lines never match real life. With Houston Apartments you trace the area you actually care about – a 10-minute radius around the Texas Medical Center, both sides of Washington Avenue, or the Grand Parkway corridor in Katy – and the results update instantly.</p>
      <ul class="ticks">
        <li>Freehand lasso on desktop and mobile</li>
        <li>Filters for rent, beds, baths, pets, parking and 16 amenities</li>
        <li>Pins show starting rent so you can compare at a glance</li>
      </ul>
      <a class="btn btn-grad btn-lg magnetic" href="/apartments/?draw=1">Try drawing on the map</a>
    </div>
    <div class="split-media reveal d1">
      <div class="mini-map-frame">
        <div id="home-map" class="mini-map" data-markers="1" aria-label="Map of Houston apartments"></div>
        <svg class="lasso-demo" viewBox="0 0 400 300" aria-hidden="true"><path d="M110,90 C150,40 260,40 300,95 C340,150 300,230 220,240 C150,250 80,210 75,160 C70,125 90,105 110,90 Z"/></svg>
        <span class="map-badge"><span class="ico ico-lasso" aria-hidden="true"></span> Drawing…</span>
      </div>
    </div>
  </div>
</section>

<?php if ($featured): ?>
<section class="section featured">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="pill">Hand-picked</span>
        <h2>Featured Houston apartments</h2>
      </div>
      <div class="carousel-nav">
        <button class="round-btn" type="button" data-scroll="-1" aria-label="Previous">‹</button>
        <button class="round-btn" type="button" data-scroll="1" aria-label="Next">›</button>
        <a class="link-arrow" href="/apartments/">View all</a>
      </div>
    </div>
    <div class="carousel" data-carousel>
      <?php foreach ($featured as $i => $c): require HA_APP . '/views/partials/card.php'; endforeach ?>
    </div>
  </div>
</section>
<?php endif ?>

<section class="section hoods" id="neighborhoods">
  <div class="wrap">
    <div class="section-head reveal">
      <div>
        <span class="pill">Explore</span>
        <h2>Houston Apartments by neighborhood</h2>
        <p class="muted">Pick a side of town. Each area page has a live map, local guide and every community we work with.</p>
      </div>
      <div class="tabs" role="tablist">
        <?php $first = true; foreach ($groups as $g => $_): ?>
          <button role="tab" type="button" aria-selected="<?= $first ? 'true' : 'false' ?>" data-tab="<?= e(slugify($g)) ?>"><?= e($g) ?></button>
        <?php $first = false; endforeach ?>
      </div>
    </div>
    <?php $first = true; foreach ($groups as $g => $keys): ?>
      <div class="hood-grid" data-panel="<?= e(slugify($g)) ?>"<?= $first ? '' : ' hidden' ?>>
        <?php foreach ($keys as $i => $k): $a = AREAS[$k]; $c = $counts[$k] ?? ['count' => 0, 'min' => null]; ?>
          <a class="hood-tile reveal d<?= $i % 4 ?>" href="/<?= $k ?>/" style="--h: <?= (crc32($k) % 360) ?>">
            <span class="hood-name"><?= e($a['name']) ?></span>
            <span class="hood-tag"><?= e($a['tag']) ?></span>
            <span class="hood-meta"><?= $c['count'] ? $c['count'] . ' communit' . ($c['count'] === 1 ? 'y' : 'ies') : 'Coming soon' ?><?= $c['min'] ? ' · starts at ' . money($c['min']) : '' ?></span>
            <span class="hood-arrow" aria-hidden="true">→</span>
          </a>
        <?php endforeach ?>
      </div>
    <?php $first = false; endforeach ?>
    <div class="popular-home reveal">
      <h3>Popular Houston apartment searches</h3>
      <ul class="popular-links">
        <?php foreach (Filters::popular() as $p): $dd = Filters::describe($p); ?><li><a href="<?= e(Filters::url($p, false)) ?>"><?= e(preg_replace('/ for Rent in .*$/', '', $dd['h1'])) ?><?= $dd['price'] ? ' (' . e($dd['price']) . ')' : '' ?></a></li><?php endforeach ?>
      </ul>
    </div>
  </div>
</section>

<section class="section steps-section">
  <div class="wrap">
    <div class="section-head center reveal">
      <span class="pill">How it works</span>
      <h2>Three steps to your next Houston apartment</h2>
    </div>
    <ol class="steps">
      <li class="step reveal"><span class="step-n">1</span><h3>Tell us what matters</h3><p>Budget, move-in date, commute, pets, credit situation – share it once, by form, phone or text.</p></li>
      <li class="step reveal d1"><span class="step-n">2</span><h3>Get a curated short list</h3><p>Your Houston Apartments locator checks current specials and availability and sends only the places that fit.</p></li>
      <li class="step reveal d2"><span class="step-n">3</span><h3>Tour, lease, get paid</h3><p>We schedule the tours. Sign your lease, list us as your locator, and collect up to $<?= SITE['cashback'] ?> back.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap"><?php $founderVariant = 'compact'; require HA_APP . '/views/partials/founder.php'; ?></div>
</section>

<section class="section budget">
  <div class="wrap split">
    <div class="split-copy reveal">
      <span class="pill">Budget calculator</span>
      <h2>How much apartment can you afford in Houston?</h2>
      <p>Most Houston apartments ask that your gross monthly income is about three times the rent. Slide to your income and we’ll show your target rent – then jump straight to matching Houston apartments.</p>
    </div>
    <div class="calc reveal d1" data-calc>
      <label for="income">Annual household income</label>
      <output class="calc-income" for="income">$60,000</output>
      <input type="range" id="income" min="25000" max="250000" step="2500" value="60000">
      <div class="gauge"><div class="gauge-fill"></div></div>
      <div class="calc-result">
        <div><span>Target rent</span><strong class="calc-rent">$1,667</strong><small>/month</small></div>
        <div><span>Comfortable range</span><strong class="calc-range">$1,250 – $1,667</strong></div>
      </div>
      <a class="btn btn-grad btn-block calc-go" href="/apartments/under-1650/">See apartments in my budget</a>
    </div>
  </div>
</section>

<section class="section tools-home">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="pill">Free renter tools</span><h2>Plan your move with Houston Apartments tools</h2></div>
      <a class="link-arrow" href="<?= TOOLS_BASE ?>">All tools</a>
    </div>
    <div class="tool-grid">
      <?php $i = 0; foreach (TOOLS as $slug => $t): if ($slug === 'rent-affordability-calculator') continue; if ($i >= 6) break; ?>
        <a class="tool-card reveal d<?= $i++ % 3 ?>" href="<?= TOOLS_BASE . $slug ?>/"><span class="tool-ico" aria-hidden="true"><?= $t['icon'] ?></span><h3><?= e($t['name']) ?></h3><p><?= e($t['short']) ?></p><span class="link-arrow">Open tool</span></a>
      <?php endforeach ?>
    </div>
  </div>
</section>

<section class="section prose-section">
  <div class="wrap prose-grid">
    <article class="prose reveal">
      <h2>Why renters choose Houston Apartments</h2>
      <p>Founded in <?= SITE['founded'] ?> as <?= e(SITE['legal']) ?>, Houston Apartments started with a simple idea: apartment hunting in a city this big should feel personal. Instead of sending you a thousand links, Houston Apartments pairs you with a locator who knows which buildings have honest specials, which managers respond quickly and which neighborhoods match your commute.</p>
      <p>Because communities pay the locating fee, Houston Apartments is free for renters. You still see the same rents as walking in – often better, because we track move-in specials across the city every week.</p>

      <h3>A neighborhood for every lifestyle</h3>
      <p>Houston is the largest city in Texas and one of the most diverse in the country, so “Houston apartments” can mean almost anything. Inner Loop renters love the Heights for its bungalow-lined streets and 19th Street shops, Montrose for galleries and late-night tacos, and Downtown or Midtown for skyline views and METRORail access. Healthcare professionals look to the Medical Center, while the Galleria and Memorial City put shopping and the Energy Corridor within easy reach.</p>
      <p>If you want more space for the money, the suburbs deliver. Katy, Cypress and Sugar Land offer top-rated school districts and master-planned amenities; The Woodlands wraps apartments in trails and forest; and Baytown, Humble and Galveston keep rents friendly with quick access to the water.</p>

      <h3>Jobs, culture and things to do</h3>
      <p>Energy, healthcare, aerospace and the Port of Houston anchor one of the strongest job markets in the U.S., and the Texas Medical Center alone employs more than 100,000 people. After work there’s the Museum District, Discovery Green, Buffalo Bayou Park, Memorial Park and four major-league teams – all without the cost of living you’d find in other big cities.</p>

      <h3>Getting around</h3>
      <p>Houston sprawls, so commute time matters more than ZIP code. That’s why the Houston Apartments map search lets you draw your own boundary instead of relying on neighborhood names. Trace the drive you can live with along I-10, US-59, I-45 or the Beltway and compare every community inside it.</p>
    </article>
    <aside class="side-card reveal d1">
      <h3>Houston Apartments at a glance</h3>
      <dl>
        <dt>Service</dt><dd>Free apartment locating</dd>
        <dt>Coverage</dt><dd>Greater Houston, Katy to Baytown, Galveston to Conroe</dd>
        <dt>Cash back</dt><dd>Up to $<?= SITE['cashback'] ?> when you lease</dd>
        <dt>Since</dt><dd><?= SITE['founded'] ?></dd>
        <dt>Call or text</dt><dd><a href="tel:<?= SITE['phone_raw'] ?>"><?= SITE['phone'] ?></a></dd>
      </dl>
      <button class="btn btn-grad btn-block" type="button" data-lead>Get my short list</button>
    </aside>
  </div>
</section>

<?php if ($posts): ?>
<section class="section blog-strip">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="pill">From the blog</span><h2>Houston Apartments guides &amp; reviews</h2></div>
      <a class="link-arrow" href="/houston-apartments-blog/">All articles</a>
    </div>
    <div class="post-grid">
      <?php foreach ($posts as $i => $post): require HA_APP . '/views/partials/post-card.php'; endforeach ?>
    </div>
  </div>
</section>
<?php endif ?>

<section class="section faq-section">
  <div class="wrap narrow">
    <div class="section-head center reveal"><span class="pill">FAQ</span><h2>Questions about Houston Apartments</h2></div>
    <div class="faq">
      <?php foreach ($homeFaqs as [$q, $a]): ?>
        <details class="reveal"><summary><?= e($q) ?></summary><p><?= e($a) ?></p></details>
      <?php endforeach ?>
    </div>
  </div>
</section>
