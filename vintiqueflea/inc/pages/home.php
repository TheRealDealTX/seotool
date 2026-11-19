<?php
defined('INC') || exit;
page_start([
    'title' => 'Vintique Flea | Houston Vintage Market & Curated Finds',
    'description' => "Houston's curated indoor vintage market at Silver Street Studios: mid-century modern, vintage clothing, architectural salvage, rustic decor and food trucks.",
    'path' => '/',
    'body_class' => 'home',
]);
// Featured picks: first two products of each category
$featured = [];
foreach (SHOP as $slug => $c) {
    $featured[] = $c['products'][0] + ['cat' => $slug];
}
$wheel = [];
foreach (SHOP as $slug => $c) {
    foreach ($c['products'] as $p) {
        $wheel[] = ['n' => $p['name'], 'i' => $p['icon'], 'note' => $p['note'], 'u' => amazon_url($p), 'c' => $c['name'], 'cu' => "/shop/$slug/"];
    }
}
add_schema([
    '@type' => 'Place',
    'name' => VENUE['name'] . ' (' . SITE_NAME . ')',
    'address' => venue_address(),
]);
?>
<section class="hero">
  <div class="wrap hero__inner">
    <div class="hero__copy">
      <p class="eyebrow">Silver Street Studios · Washington Avenue Arts District</p>
      <h1>Houston's curated marketplace of <span class="hl">interesting things</span></h1>
      <p class="lede">Mid-century modern, vintage clothing, architectural salvage and industrial, rustic home decor, local food trucks and more, all under one roof. Founded by the people who created Rice Village Flea.</p>
      <div class="hero__ctas">
        <a class="btn btn--primary" href="/events/">See market dates</a>
        <a class="btn btn--ghost" href="/shop/">Shop curated finds</a>
      </div>
    </div>
    <div class="hero__art" aria-hidden="true">
      <div class="burst"></div>
      <div class="hero__tags">
        <span class="tag tag--teal">🪑 Mid-Century</span>
        <span class="tag tag--rust">👗 Vintage Clothing</span>
        <span class="tag tag--olive">🏭 Salvage</span>
        <span class="tag tag--mustard">🌾 Rustic Decor</span>
        <span class="tag tag--teal">🚚 Food Trucks</span>
        <span class="tag tag--rust">📻 Vinyl</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <h2>What you'll find at Vintique Flea</h2>
      <p>Every booth is curated. No mass-produced filler, just the good stuff. Browse by category, then find the originals at our next market.</p>
    </div>
    <div class="cat-grid">
<?php foreach (SHOP as $slug => $c): ?>
      <a class="cat cat--<?= e($c['color']) ?>" href="/shop/<?= $slug ?>/">
        <span class="cat__icon" aria-hidden="true"><?= $c['icon'] ?></span>
        <span class="cat__name"><?= e($c['name']) ?></span>
        <span class="cat__more">Explore <span aria-hidden="true">→</span></span>
      </a>
<?php endforeach; ?>
      <a class="cat cat--olive" href="/food-trucks/">
        <span class="cat__icon" aria-hidden="true">🚚</span>
        <span class="cat__name">Local Food Trucks</span>
        <span class="cat__more">Explore <span aria-hidden="true">→</span></span>
      </a>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wheel-wrap">
    <div class="wheel-copy">
      <p class="eyebrow">Feeling lucky?</p>
      <h2>Spin the Treasure Wheel</h2>
      <p>Can't decide what to hunt for? Give the wheel a spin and we'll pull a random find from our curated picks. Every spin is a new treasure.</p>
      <button class="btn btn--primary" id="wheel-spin" type="button">Spin the wheel</button>
      <div class="wheel-result" id="wheel-result" aria-live="polite"></div>
    </div>
    <div class="wheel" aria-hidden="true">
      <div class="wheel__disc" id="wheel-disc">
<?php $icons = ['🪑','👗','🏭','🌾','🏺','📻','🍸','🧰']; foreach ($icons as $i => $ic): ?>
        <span style="--i:<?= $i ?>"><?= $ic ?></span>
<?php endforeach; ?>
      </div>
      <div class="wheel__pointer"></div>
    </div>
  </div>
  <script type="application/json" id="wheel-data"><?= json_encode($wheel, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_HEX_TAG) ?></script>
</section>

<section class="section">
  <div class="wrap visit">
    <div class="visit__card">
      <h2>Visit the market</h2>
      <p>Vintique Flea has always called <strong>Silver Street Studios</strong> home, a converted warehouse in the heart of Houston's Washington Avenue Arts District. It's indoors, so rain or Houston heat never cancels the fun.</p>
      <dl class="facts">
        <div><dt>Where</dt><dd><?= e(VENUE['street']) ?>, <?= e(VENUE['city']) ?>, <?= e(VENUE['region']) ?> <?= e(VENUE['postal']) ?></dd></div>
        <div><dt>When</dt><dd><?= UPCOMING_EVENTS ? e(UPCOMING_EVENTS[0]['name']) . ': ' . e(implode(' · ', UPCOMING_EVENTS[0]['hours'] ?? [])) : 'Seasonal weekend editions. Get the next dates by email.' ?></dd></div>
        <div><dt>Also</dt><dd>Local food trucks, beer &amp; wine. Kids have historically been admitted free.</dd></div>
      </dl>
      <a class="btn btn--primary" href="/events/">Market dates &amp; details</a>
    </div>
    <div class="visit__card visit__card--accent">
      <h2>Never miss a market</h2>
      <p>Join the list for new market dates, vendor announcements and the occasional treasure-hunting tip. No spam, ever.</p>
      <?= newsletter_form('home') ?>
      <p class="small">Selling vintage, salvage or handmade goods? <a href="/vendors/">Apply to be a vendor</a>.</p>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap">
    <div class="section__head">
      <h2>Play around</h2>
      <p>Games and tools for vintage lovers. Test your eye, sharpen your haggling, and design your dream room.</p>
    </div>
    <div class="game-grid">
<?php foreach (GAMES as $slug => $g): ?>
      <a class="game-card" href="/play/<?= $slug ?>/">
        <span class="game-card__icon" aria-hidden="true"><?= $g['icon'] ?></span>
        <span class="game-card__name"><?= e($g['name']) ?></span>
        <span class="game-card__blurb"><?= e($g['blurb']) ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section__head">
      <h2>Curated finds you can shop today</h2>
      <p>Can't wait for the next market? These picks capture the Vintique Flea look and ship to your door.</p>
    </div>
    <?= product_grid($featured) ?>
    <?= disclosure() ?>
  </div>
</section>

<?php $guides = load_guides(); if ($guides): ?>
<section class="section section--alt">
  <div class="wrap">
    <div class="section__head">
      <h2>Guides for vintage lovers</h2>
      <p>Houston shopping, decorating with old things, and how to get the best deal at any flea market.</p>
    </div>
    <div class="guide-grid">
<?php foreach (array_slice($guides, 0, 6, true) as $gslug => $g): ?>
      <a class="guide-card" href="/guides/<?= $gslug ?>/">
        <span class="guide-card__cat"><?= e($g['category']) ?></span>
        <span class="guide-card__title"><?= e($g['h1']) ?></span>
        <span class="guide-card__intro"><?= e($g['intro']) ?></span>
      </a>
<?php endforeach; ?>
    </div>
    <p class="center"><a class="btn btn--ghost" href="/guides/">All guides</a></p>
  </div>
</section>
<?php endif; ?>
<?php page_end();
