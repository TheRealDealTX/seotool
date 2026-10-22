<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
// Homepage. Brief: the site name "Under Desk Elliptical" must appear at least 14 times on
// this page; dev/check.php counts the occurrences inside <main>.
$posts = all_posts();
$picks = ['cubii-jr2', 'deskcycle-ellipse', 'sunny-sf-e3872', 'ancheer'];
$faq = [
    ['q' => 'What is the best under desk elliptical?', 'a' => 'For most people the Cubii JR2 is the best under desk elliptical: it is quiet, smooth and well supported. The DeskCycle Ellipse is better for low desks, the Sunny Health &amp; Fitness model is the best budget pick, and the ANCHEER is our top motorized choice. See the <a href="/what-is-the-best-under-desk-elliptical/">full rankings</a>.'],
    ['q' => 'Do under desk ellipticals actually work?', 'a' => 'Yes, for what they are designed to do. An under desk elliptical turns sitting time into light activity, burning roughly 100 to 200 extra calories an hour for most people and breaking up long periods of stillness. It will not replace a full workout. <a href="/does-an-under-desk-elliptical-work/">Read the evidence</a>.'],
    ['q' => 'What muscles does an under desk elliptical work?', 'a' => 'Mainly the quads, hamstrings, glutes and calves, with the shins and hip flexors helping. Pedaling backward shifts more work to the hamstrings and glutes. <a href="/what-muscles-does-an-under-desk-elliptical-work/">Full muscle breakdown</a>.'],
    ['q' => 'Can you stand on an under desk elliptical?', 'a' => 'Most seated models are not built for standing and can tip or break. If you want to stand, choose a compact strider made for standing like the Stamina InMotion E1000, or a walking pad. <a href="/can-you-stand-on-an-under-desk-elliptical/">Details and safe options</a>.'],
    ['q' => 'Will an under desk elliptical fit under my desk?', 'a' => 'Usually, if there is enough room between the top of your knee and the underside of the desk when your foot is raised by the pedal. Check in ten seconds with our <a href="/tools/desk-clearance-checker/">desk clearance checker</a>.'],
    ['q' => 'Is an under desk elliptical better than a walking pad?', 'a' => 'An under desk elliptical is quieter, cheaper and works at a normal sitting desk. A walking pad burns more calories and counts real steps but needs a standing desk. <a href="/under-desk-elliptical-vs-walking-pad/">Compare them</a>.'],
];
$schema = [
    schema_faq($faq),
    ['@type' => 'ItemList', 'name' => 'Best under desk ellipticals', 'itemListElement' => array_map(fn($i, $k) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => product($k)['name'], 'url' => amz_url($k)], array_keys($picks), $picks)],
];
$heroImg = '/assets/img/thumbs/What-Is-the-Best-Under-Desk-Elliptical-1.webp';
page_start([
    'title' => 'Under Desk Elliptical: Best Picks, Honest Reviews & Free Tools',
    'description' => 'Under Desk Elliptical helps you choose the best under desk elliptical: ranked picks, honest reviews, side-by-side comparisons and free calorie, steps and fit tools.',
    'path' => '/', 'schema' => $schema, 'preload' => $heroImg, 'body_class' => 'is-home',
    'image' => '/wp-content/uploads/2026/05/What-Is-the-Best-Under-Desk-Elliptical-1.webp',
]);
?>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="eyebrow" style="color:var(--gold)">Under Desk Elliptical &middot; Updated <?= e(fmt_date(SITE_UPDATED)) ?></p>
      <h1>Find the Best <em>Under Desk Elliptical</em> for Your Desk, Body and Budget</h1>
      <p class="lead">Under Desk Elliptical is an independent guide to seated ellipticals, desk bikes and walking pads. We compare specs and thousands of owner reviews, explain what the research really says, and build free tools so you can buy the right machine the first time.</p>
      <div class="hero-actions">
        <a class="btn btn-amz" href="/tools/which-under-desk-elliptical-quiz/">Find my match (60-sec quiz)</a>
        <a class="btn btn-ghost" href="/what-is-the-best-under-desk-elliptical/">See the top picks</a>
      </div>
      <ul class="hero-trust"><li>No sponsored rankings</li><li><?= count($posts) ?>+ in-depth guides</li><li>6 free interactive tools</li></ul>
    </div>
    <div class="hero-img"><img src="<?= e($heroImg) ?>" alt="Person using an under desk elliptical while working at a home office desk" width="768" height="512" fetchpriority="high"></div>
  </div>
</section>

<div class="wrap">
  <div class="stats-band">
    <div><strong><?= count(array_filter(PRODUCTS, fn($p) => !in_array($p['type'], ['accessory', 'tracker']))) ?></strong><span>models compared</span></div>
    <div><strong><?= count($posts) ?></strong><span>guides &amp; reviews</span></div>
    <div><strong>6</strong><span>free interactive tools</span></div>
    <div><strong>100%</strong><span>reader-supported</span></div>
  </div>
</div>

<section class="section" id="top-picks">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Top picks for <?= date('Y', strtotime(SITE_UPDATED)) ?></p>
      <h2>The Best Under Desk Elliptical Picks at a Glance</h2>
      <p class="lead">These four cover what most people need. Each under desk elliptical here has a long record of owner reviews, quiet operation and reliable support.</p>
    </div>
    <div class="picks">
<?php foreach ($picks as $k): $p = product($k); ?>
      <div class="pick">
        <a href="<?= e(amz_url($k)) ?>" <?= amz_attrs() ?>><img src="<?= e(thumb($p['image'])) ?>" alt="<?= e($p['name']) ?>" loading="lazy" width="768" height="512"></a>
        <div>
          <span class="pcard-badge"><?= e($p['best_for']) ?></span>
          <h3><?= e($p['name']) ?></h3>
          <p><?= e($p['summary']) ?></p>
          <?= amz_button($k) ?>
        </div>
      </div>
<?php endforeach; ?>
    </div>
    <p style="margin-top:22px"><a class="btn btn-ghost" href="/what-is-the-best-under-desk-elliptical/">Read the full best under desk elliptical rankings &rarr;</a></p>
  </div>
</section>

<section class="section alt" id="quiz">
  <div class="wrap split top">
    <div>
      <p class="eyebrow">Free tool</p>
      <h2>Which Under Desk Elliptical Is Right for You?</h2>
      <p>Seated or standing? Silent for calls or fine with a hum? Calorie burn or circulation? The right under desk elliptical depends on a few answers. Our quiz weighs them against every model we cover and shows your three best matches.</p>
      <p>Prefer to browse? Use the <a href="/tools/compare-under-desk-ellipticals/">filterable comparison table</a> to sort by noise, type and suitability for seniors.</p>
    </div>
    <div><?= tool_widget('quiz') ?></div>
  </div>
</section>

<section class="section" id="compare">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Side by side</p>
      <h2>Under Desk Elliptical Comparison Chart</h2>
      <p class="lead">How the leading models stack up on type, noise, suitability for seniors and standing use.</p>
    </div>
    <?= compare_table(['cubii-jr2', 'deskcycle-ellipse', 'sunny-sf-e3872', 'lifepro-flexstride', 'ancheer', 'legxercise', 'stamina-inmotion-e1000', 'deskcycle-2']) ?>
  </div>
</section>

<section class="section alt" id="how-to-choose">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Buying guide</p>
      <h2>How to Choose an Under Desk Elliptical in 4 Steps</h2>
    </div>
    <div class="steps-grid">
      <div><h3>Measure your desk</h3><p>Your knees rise with the pedals. Measure from the floor to the underside of the desk and run the <a href="/tools/desk-clearance-checker/">clearance checker</a> before you buy.</p></div>
      <div><h3>Pick manual or motorized</h3><p>Manual models burn more calories. <a href="/best-motorized-under-desk-elliptical/">Motorized</a> ones move your legs for you, which is ideal for circulation and limited mobility.</p></div>
      <div><h3>Prioritize quiet</h3><p>Magnetic resistance is near-silent and lasts. If you take calls, see the <a href="/quietest-under-desk-elliptical/">quietest under desk elliptical</a> picks.</p></div>
      <div><h3>Stop the slide</h3><p>Budget for a <?= amz_link('cubii-mat', 'non-slip mat') ?> and <?= amz_link('caster-cups', 'caster cups') ?> for a rolling chair. They solve the most common complaint.</p></div>
    </div>
  </div>
</section>

<section class="section" id="calories">
  <div class="wrap split top">
    <div>
      <p class="eyebrow">Free calculator</p>
      <h2>How Many Calories Does an Under Desk Elliptical Burn?</h2>
      <p>Most people burn roughly 100 to 200 calories an hour on an under desk elliptical at a light to moderate pace. Because you pedal while you work, two or three hours a day adds up to a meaningful weekly total without taking time out of your schedule.</p>
      <p>Move the sliders to see your own numbers, then read <a href="/does-under-desk-elliptical-burn-calories/">does an under desk elliptical burn calories</a> and <a href="/can-you-lose-weight-with-under-desk-elliptical/">can you lose weight with one</a>.</p>
    </div>
    <div><?= tool_widget('calories') ?></div>
  </div>
</section>

<section class="section alt" id="popular">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Most read</p>
      <h2>Popular Under Desk Elliptical Guides</h2>
      <p class="lead">The questions readers ask us most, answered in depth.</p>
    </div>
    <div class="grid grid-3">
<?php foreach (['what-muscles-does-an-under-desk-elliptical-work', 'can-you-stand-on-an-under-desk-elliptical', 'under-desk-elliptical-vs-walking-pad', 'best-under-desk-elliptical-for-seniors', 'does-under-desk-elliptical-count-as-steps', 'is-under-desk-elliptical-as-good-as-walking'] as $s): if (isset($posts[$s])): ?>
      <?= post_card($posts[$s]) ?>
<?php endif; endforeach; ?>
    </div>
  </div>
</section>

<section class="section" id="reviews">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Brand reviews</p>
      <h2>Under Desk Elliptical Reviews by Brand</h2>
      <p class="lead">Honest pros, cons and verdicts for every popular brand, including the budget names you see on Amazon.</p>
    </div>
    <div class="brand-list">
<?php
$brands = ['Cubii JR2' => 'cubii-under-desk-elliptical-is-it-really-worth-using-every-day', 'Cubii Pro' => 'cubii-pro-hd-review', 'Cubii Move' => 'cubii-move-review', 'Cubii JR1' => 'cubii-jr1-under-desk-elliptical', 'DeskCycle Ellipse' => 'deskcycle-ellipse-review', 'Stamina InMotion' => 'stamina-inmotion-review', 'FitDesk FDX 2.0' => 'fitdesk-fdx-2-review', 'Flex Fitness' => 'flex-fitness-under-desk-elliptical', 'Geoneo' => 'geoneo-under-desk-elliptical', 'Yosuda' => 'yosuda-under-desk-elliptical-reviews', 'Merach' => 'merach-under-desk-elliptical-machine', 'Fryline' => 'fryline-under-desk-elliptical', 'DamKee' => 'damkee-under-desk-elliptical', 'LVPIMAN' => 'lvpiman-under-desk-elliptical', 'JISUO' => 'jisuo-under-desk-elliptical-review', 'Putnen' => 'putnen-under-desk-elliptical', 'Mysuntown' => 'mysuntown-under-desk-elliptical', 'Viamotion' => 'viamotion-under-desk-elliptical-review', 'Fousae' => 'fousae-under-desk-elliptical', 'Fntkech' => 'under-desk-elliptical-fntkech'];
foreach ($brands as $label => $s): if (isset($posts[$s])): ?>
      <a href="/<?= e($s) ?>/"><?= e($label) ?></a>
<?php endif; endforeach; ?>
    </div>
  </div>
</section>

<section class="section alt" id="versus">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Comparisons</p>
      <h2>Under Desk Elliptical vs the Alternatives</h2>
    </div>
    <div class="vs-grid">
      <a class="vs" href="/under-desk-elliptical-vs-walking-pad/"><strong>vs Walking Pad</strong>Sit or stand? Noise, calories and desk setup compared.</a>
      <a class="vs" href="/under-desk-elliptical-vs-bike/"><strong>vs Under Desk Bike</strong>Smooth oval stride or circular pedaling, and which is kinder to knees.</a>
      <a class="vs" href="/under-desk-elliptical-vs-treadmill/"><strong>vs Treadmill</strong>Space, cost and real-world calorie burn.</a>
      <a class="vs" href="/is-under-desk-elliptical-as-good-as-walking/"><strong>vs Walking</strong>Is pedaling at your desk as good as a walk? The math.</a>
    </div>
  </div>
</section>

<section class="section" id="latest">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Fresh from the blog</p>
      <h2>Latest Under Desk Elliptical Guides</h2>
    </div>
    <div class="grid grid-3">
<?php $shown = 0; foreach ($posts as $p): if (in_array($p['slug'], ['what-muscles-does-an-under-desk-elliptical-work', 'can-you-stand-on-an-under-desk-elliptical', 'under-desk-elliptical-vs-walking-pad', 'best-under-desk-elliptical-for-seniors', 'does-under-desk-elliptical-count-as-steps', 'is-under-desk-elliptical-as-good-as-walking'])) continue; if ($shown++ >= 6) break; ?>
      <?= post_card($p) ?>
<?php endforeach; ?>
    </div>
    <p style="margin-top:22px"><a class="btn btn-ghost" href="/blog/">Browse all <?= count($posts) ?> guides &rarr;</a></p>
  </div>
</section>

<section class="section alt" id="about">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Why trust us</p>
      <h2>Why Under Desk Elliptical Exists</h2>
      <p>Most of us sit for eight or more hours a day, and finding time for the gym is hard. An under desk elliptical is one of the simplest fixes: it turns sitting time into gentle, low-impact movement you barely notice.</p>
      <p>But the market is crowded with look-alike machines and confusing claims. Under Desk Elliptical cuts through it. We compare manufacturer specs, read through owner reviews for recurring problems, and translate exercise research into plain English. Every recommendation explains who a machine is <em>and isn't</em> right for.</p>
      <p>Under Desk Elliptical is reader-supported. When you buy through our Amazon links we may earn a small commission at no cost to you. That never decides our rankings. <a href="/about-us/">Learn how we work</a>.</p>
    </div>
    <div>
      <div class="faq">
        <h2 id="faq" style="margin-top:0">Under Desk Elliptical FAQ</h2>
<?php foreach ($faq as $f): ?>
        <details><summary><?= e($f['q']) ?></summary><div><p><?= $f['a'] ?></p></div></details>
<?php endforeach; ?>
      </div>
    </div>
  </div>
</section>

<div class="wrap">
  <div class="cta-band"><div><h2>Ready to move more while you work?</h2><p>Start with the under desk elliptical our readers buy most, or take the quiz for a personal match.</p></div><div style="display:flex;gap:10px;flex-wrap:wrap"><?= amz_button('cubii-jr2', 'See the Cubii JR2') ?><a class="btn btn-ghost" style="color:#fff" href="/tools/which-under-desk-elliptical-quiz/">Take the quiz</a></div></div>
</div>
<?php page_end();
