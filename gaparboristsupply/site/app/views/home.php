<?php
defined('GAP') || exit;
$meta = [
    'title' => 'Arborist Gear & Tree Climbing Supply Store',
    'desc' => 'Arborist gear for climbers and crews: saddles, rope, rigging, Silky saws, Husqvarna chainsaws and safety gear, with buying guides and free tree-work tools.',
    'canonical' => '/',
    'body_class' => 'is-home',
];
// Most-searched products from the old site, in order of the traffic they earned.
$featured = pick([
    '/jobsite/power-equipment/chainsaws/husqvarna-372xp-chainsaw/',
    '/cutting-and-pruning/hand-saws-and-scabbards/silky-sugoi/',
    '/cutting-and-pruning/hand-saws-and-scabbards/silky-gunfighter-professional-saw-330mm-handsaw/',
    '/jobsite/power-equipment/chainsaws/husqvarna-3120xp-chainsaw-power-head-only/',
    '/jobsite/power-equipment/parts/ngk-cmr6h-spark-plug/',
    '/jobsite/power-equipment/chainsaws/husqvarna-450-rancher/',
    '/climbing/climbing-gear/ascent-and-descent/mechanical-friction-devices/devices-for-mrs/hitch-hiker-2/',
    '/other-gear/soft-canopy-anchor/',
]);
$climb = pick(array_slice($CAT['categories']['/climbing/']['products'] ?? [], 0, 40));
usort($climb, fn($a, $b) => strcmp($a['kind'], $b['kind']));
$depts = array_filter(array_map(fn($p) => $CAT['categories'][$p] ?? null, $CFG['departments']));
$brands = array_filter($CAT['brands'], fn($b) => count($b['products']) > 0);
uasort($brands, fn($a, $b) => count($b['products']) <=> count($a['products']));
$brands = array_slice($brands, 0, 18);
function hero_float(string $cls, string $kind): string {
    global $CAT;
    $ph = $CAT['images'][$kind][0] ?? null;
    return $ph ? '<span class="float float-photo ' . $cls . '"><img src="' . e($ph['sm']) . '" alt=""></span>' : '<img class="float ' . $cls . '" src="' . kind_img($kind) . '" alt="">';
}
?>
<section class="hero">
  <canvas class="hero-canvas" aria-hidden="true"></canvas>
  <div class="hero-layers" aria-hidden="true">
    <div class="layer l1" data-depth="0.15"></div>
    <div class="layer l2" data-depth="0.3"></div>
    <div class="layer l3" data-depth="0.5"></div>
  </div>
  <svg class="hero-rope" viewBox="0 0 200 600" aria-hidden="true" preserveAspectRatio="none"><path d="M100 0 C 96 140, 104 260, 100 420 S 98 560, 100 600"/></svg>
  <div class="wrap hero-inner">
    <div class="hero-copy">
      <p class="eyebrow"><span class="chip-dot"></span> Climbers' store · rigging · saws · safety</p>
      <h1>Arborist gear that earns its place on the <em>saddle</em>.</h1>
      <p class="lede">Gap Arborist Supply is a tree climbing store and gear guide for working arborists, crews and serious DIY climbers: <?= count($CAT['products']) ?> hand-picked pieces of arborist gear across <?= count($CAT['categories']) ?> categories, with plain-English advice on what to buy and why.</p>
      <div class="hero-cta">
        <a class="btn btn-lg btn-chain" href="/shop-all/">Shop all gear</a>
        <a class="btn btn-lg btn-ghost-light" href="/tools/climbing-kit-builder/">Build a climbing kit</a>
      </div>
      <ul class="hero-proof">
        <li><b><?= count($CAT['brands']) ?></b> brands compared</li>
        <li><b><?= count(TOOLS) ?></b> free tree-work tools</li>
        <li><b><?= count($CAT['guides']) ?></b> in-depth buying guides</li>
      </ul>
    </div>
    <div class="hero-stage" aria-hidden="true">
      <div class="orbit">
        <?= hero_float('f1', 'saddle') ?>
        <?= hero_float('f2', 'chainsaw') ?>
        <?= hero_float('f3', 'carabiner') ?>
        <?= hero_float('f4', 'hand-saw') ?>
        <?= hero_float('f5', 'rope') ?>
        <?= hero_float('f6', 'helmet') ?>
      </div>
      <svg class="growth-rings" viewBox="0 0 400 400"><?php for ($i = 1; $i <= 9; $i++): ?><circle cx="200" cy="200" r="<?= 20 + $i * 19 + ($i % 3) * 3 ?>" style="--i:<?= $i ?>"/><?php endfor; ?></svg>
    </div>
  </div>
  <a class="scroll-cue" href="#departments" aria-label="Scroll to departments"><span></span></a>
</section>

<section class="section depts" id="departments">
  <div class="wrap">
    <div class="section-head reveal">
      <p class="eyebrow dark">Departments</p>
      <h2>Everything from the ground to the canopy</h2>
    </div>
    <div class="dept-grid">
<?php foreach ($depts as $i => $d): ?>
      <a class="dept-tile tilt reveal<?= !empty($d['photo']) ? ' has-photo' : '' ?>" href="<?= e($d['path']) ?>" style="--d:<?= $i ?>">
        <?php if (!empty($d['photo'])): ?><span class="dept-photo"><?= photo_img($d['photo'], $d['kind'], '', '(max-width: 520px) 50vw, 300px') ?></span><?php else: ?><span class="dept-art"><img src="<?= kind_img($d['kind']) ?>" alt="" loading="lazy" width="120" height="120"></span><?php endif; ?>
        <span class="dept-name"><?= e($d['name']) ?></span>
        <span class="dept-count"><?= count($d['products']) ?> items</span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section bestsellers">
  <div class="wrap">
    <div class="section-head split reveal">
      <div><p class="eyebrow dark">Most searched</p><h2>The gear tree people look up most</h2></div>
      <a class="link-arrow" href="/shop-all/">See all gear</a>
    </div>
    <div class="grid products-grid">
<?php foreach ($featured as $p) echo product_card($p); ?>
    </div>
  </div>
</section>

<section class="section kit-teaser">
  <div class="wrap kit-grid">
    <div class="kit-copy reveal">
      <p class="eyebrow">Interactive</p>
      <h2>Build your climbing kit in 60 seconds</h2>
      <p>Moving rope or stationary rope? Spur removals or pruning climbs? Tell the kit builder how you climb and what you want to spend, and it lays out a complete set of tree climbing gear with typical prices. Add the whole list to your cart in one tap.</p>
      <a class="btn btn-lg btn-chain" href="/tools/climbing-kit-builder/">Open the kit builder</a>
    </div>
    <div class="kit-visual reveal" aria-hidden="true">
      <div class="kit-orbit">
<?php foreach (['saddle', 'rope', 'friction-device', 'lanyard', 'carabiner', 'helmet', 'throw-line', 'hand-saw'] as $i => $k): ?>
        <span class="kit-node" style="--n:<?= $i ?>"><img src="<?= kind_img($k) ?>" alt=""></span>
<?php endforeach; ?>
        <span class="kit-core"><b>Your kit</b><small>8 pieces</small></span>
      </div>
    </div>
  </div>
</section>

<section class="section tools-strip">
  <div class="wrap">
    <div class="section-head split reveal">
      <div><p class="eyebrow dark">Free tools</p><h2>Do the math before you climb, rig or cut</h2></div>
      <a class="link-arrow" href="/tools/">All tools</a>
    </div>
    <div class="tool-grid">
<?php foreach (TOOLS as $slug => [$name, $blurb, $kind]): ?>
      <a class="tool-card tilt reveal" href="/tools/<?= $slug ?>/">
        <img src="<?= kind_img($kind) ?>" alt="" width="72" height="72" loading="lazy">
        <h3><?= e($name) ?></h3>
        <p><?= e($blurb) ?></p>
        <span class="link-arrow">Open tool</span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section climb-shelf">
  <div class="wrap">
    <div class="section-head split reveal">
      <div><p class="eyebrow dark">Tree climbing gear</p><h2>Fresh off the climbing wall</h2></div>
      <a class="link-arrow" href="/climbing/">Shop climbing</a>
    </div>
    <div class="shelf" data-shelf>
<?php foreach (array_slice($climb, 0, 14) as $p) echo product_card($p, 'shelf-item'); ?>
    </div>
    <div class="shelf-controls"><button type="button" class="round-btn" data-shelf-prev aria-label="Scroll left">←</button><button type="button" class="round-btn" data-shelf-next aria-label="Scroll right">→</button></div>
  </div>
</section>

<section class="section why">
  <div class="wrap why-grid">
    <div class="rings-art reveal" aria-hidden="true">
      <svg viewBox="0 0 300 300" class="trunk-rings"><?php for ($i = 1; $i <= 12; $i++): ?><ellipse cx="150" cy="152" rx="<?= 10 + $i * 11.5 ?>" ry="<?= 9 + $i * 11 ?>" style="--i:<?= $i ?>"/><?php endfor; ?></svg>
    </div>
    <div class="why-copy reveal">
      <p class="eyebrow dark">Why shop here</p>
      <h2>Arborist supply, without the catalog noise</h2>
      <div class="why-points">
        <div><h3>Picked for tree work</h3><p>Every product is here because it does a job in the tree or on the ground: climbing, rigging, cutting, cleanup or keeping a crew safe.</p></div>
        <div><h3>Honest prices</h3><p>We show the typical street price and send you to the retailer to check today's price, so there are no surprises at checkout.</p></div>
        <div><h3>Advice you can use</h3><p>Buying guides, compatibility notes and calculators written in the language crews actually use on the job.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section brands-band">
  <div class="wrap"><p class="eyebrow dark center">Brands tree crews trust</p></div>
  <div class="marquee" aria-label="Brands">
    <div class="marquee-track">
<?php for ($r = 0; $r < 2; $r++): foreach ($brands as $b): ?>
      <a href="<?= e($b['path']) ?>"<?= $r ? ' tabindex="-1" aria-hidden="true"' : '' ?>><?= e($b['name']) ?></a>
<?php endforeach; endfor; ?>
    </div>
  </div>
</section>

<?php if ($CAT['guides']): ?>
<section class="section guides-home">
  <div class="wrap">
    <div class="section-head split reveal">
      <div><p class="eyebrow dark">Buying guides</p><h2>Read this before you buy</h2></div>
      <a class="link-arrow" href="/guides/">All guides</a>
    </div>
    <div class="guide-grid">
<?php foreach (array_slice($CAT['guides'], 0, 3) as $g): ?>
      <a class="guide-card tilt reveal" href="<?= e($g['path']) ?>">
        <span class="guide-art<?= !empty($g['photo']) ? ' has-photo' : '' ?>"><?= !empty($g['photo']) ? photo_img($g['photo'], $g['kind'], '', '(max-width: 700px) 100vw, 400px') : '<img src="' . kind_img($g['kind']) . '" alt="" loading="lazy">' ?></span>
        <span class="guide-meta"><?= (int)$g['read_minutes'] ?> min read</span>
        <h3><?= e($g['h1']) ?></h3>
        <p><?= e($g['dek']) ?></p>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>

<section class="section home-seo">
  <div class="wrap narrow prose reveal">
    <h2>A tree climbing store built around the work</h2>
    <p>Good arborist gear is the difference between a day that flows and a day spent fighting your system. That is why Gap Arborist Supply is organized the way a crew thinks: <a href="/climbing/">climbing</a> gear for getting up and moving through the canopy, <a href="/rigging/">rigging</a> for bringing wood down under control, <a href="/rope/">arborist rope</a> for both, then <a href="/cutting-and-pruning/">cutting and pruning</a> tools, <a href="/jobsite/">jobsite and power equipment</a>, and the <a href="/safety/">safety gear</a> that sends everyone home.</p>
    <p>If you are new to tree climbing, start with the <a href="/tools/climbing-kit-builder/">kit builder</a> and our tree climbing gear checklist. If you run a crew, the forestry supply side of the store covers chainsaws, chaps, wedges, logging tools and the parts that keep saws running. Either way, compare up to three items side by side, save gear for later and check the current price with the retailer when you are ready.</p>
  </div>
</section>
