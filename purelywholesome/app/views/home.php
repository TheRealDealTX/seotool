<?php
/** @var array $popular @var array $latest @var array $season @var string $seasonLabel @var string $seasonBlurb @var array $counts @var array $homeFaq @var array $index */
$heroImgs = array_values(array_filter([$index['sides-for-lamb-chops'] ?? null, $index['goat-pregnancy'] ?? null, $index['farm-fresh-eggs'] ?? null]));
$liveCount = count(live_posts());
?>
<section class="hero">
  <div class="hero__bg" aria-hidden="true">
    <span class="blob blob--1"></span><span class="blob blob--2"></span><span class="blob blob--3"></span>
    <span class="grain"></span>
    <?php for ($i = 0; $i < 7; $i++): ?><span class="leaf" style="--i:<?= $i ?>"><?= icon('leaf') ?></span><?php endfor ?>
  </div>
  <div class="wrap hero__grid">
    <div class="hero__copy">
      <p class="eyebrow reveal"><span class="dot"></span> Welcome to Purely Wholesome Farm</p>
      <h1 class="hero__title reveal">
        <span class="hero__brand">Purely Wholesome Farm</span>
        Grow better, cook from scratch, <em class="scribble">live simpler.<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M3 15C60 5 130 3 297 9"/></svg></em>
      </h1>
      <p class="hero__lead reveal">Purely Wholesome Farm is a farm kitchen and homestead journal. Juicy brined chicken, lamb chops with all the right sides, silky pumpkin pie, healthy goats and happy hens: real know-how from the barn and the stove, plus free tools that do the math for you.</p>
      <form class="hero__search reveal" action="/" method="get" role="search">
        <?= icon('search') ?>
        <input type="search" name="s" placeholder="What are you cooking or raising today?" aria-label="Search Purely Wholesome Farm" data-hero-search>
        <button class="btn btn--primary" type="submit">Search</button>
      </form>
      <div class="hero__ctas reveal">
        <a class="btn btn--primary btn--lg" href="/blog/">Explore the journal <?= icon('arrow') ?></a>
        <a class="btn btn--ghost btn--lg" href="/tools/"><?= icon('tool') ?> Try the farm tools</a>
      </div>
    </div>
    <div class="hero__art" data-parallax-group>
      <?php foreach ($heroImgs as $i => $p): ?>
        <a class="hero__photo hero__photo--<?= $i + 1 ?>" href="<?= post_url($p['slug']) ?>" data-depth="<?= [0.04, 0.08, 0.06][$i] ?>">
          <img src="<?= e($p['image']) ?>" alt="<?= e($p['h1']) ?>" width="<?= (int)$p['image_w'] ?>" height="<?= (int)$p['image_h'] ?>" <?= $i ? 'loading="lazy"' : 'fetchpriority="high"' ?>>
        </a>
      <?php endforeach ?>
      <a class="float-badge float-badge--a" href="/tools/brine-calculator/" data-depth="0.12"><?= icon('flask') ?><span><strong>Brine Calculator</strong><small>Exact salt for any salt brand</small></span></a>
      <a class="float-badge float-badge--b" href="/tools/goat-gestation-calculator/" data-depth="0.1"><?= icon('goat') ?><span><strong>Kidding due date</strong><small>150 days, mapped out</small></span></a>
      <span class="hand-note" data-depth="0.05">fresh from the farm ♥</span>
    </div>
  </div>
  <svg class="hero__wave" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 50c240-40 480-40 720 0s480 40 720 0v30H0Z" fill="currentColor"/></svg>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    <?php for ($r = 0; $r < 2; $r++): foreach (['Lamb chops', 'Chicken brine', 'Pumpkin pie', 'Sourdough', 'Water bath canning', 'Goat kidding', 'Farm fresh eggs', 'Sweet pickles', 'Winter waterers', 'Golden beets', 'Brisket', 'Dairy goats'] as $w): ?>
      <span><?= e($w) ?></span><i><?= icon('sprout') ?></i>
    <?php endforeach; endfor ?>
  </div>
</div>

<section class="section">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="eyebrow">Reader favorites</p>
      <h2>Most-loved on Purely Wholesome Farm</h2>
      <p>The recipes and guides thousands of home cooks and homesteaders come back to, refreshed and expanded for this season.</p>
    </header>
    <div class="bento">
      <?php foreach ($popular as $i => $p): ?>
        <a class="bento__item bento__item--<?= $i ?> reveal tilt" href="<?= post_url($p['slug']) ?>" style="--d:<?= $i * 70 ?>ms">
          <?php if ($p['image']): ?><img src="<?= e($p['image']) ?>" alt="" loading="lazy" width="<?= (int)$p['image_w'] ?>" height="<?= (int)$p['image_h'] ?>"><?php endif ?>
          <span class="bento__shade"></span>
          <span class="bento__text">
            <span class="chip chip--light"><?= e(TOPICS[$p['topic']][0] ?? '') ?></span>
            <strong><?= e($p['h1']) ?></strong>
            <?php if ($i === 0): ?><small><?= e($p['desc']) ?></small><?php endif ?>
            <span class="bento__go"><?= icon('arrow') ?></span>
          </span>
        </a>
      <?php endforeach ?>
    </div>
  </div>
</section>

<section class="section section--forest tools-band">
  <div class="tools-band__glow" aria-hidden="true"></div>
  <div class="wrap">
    <header class="section__head section__head--light reveal">
      <p class="eyebrow">Free interactive tools</p>
      <h2>Let Purely Wholesome Farm do the math</h2>
      <p>Salt ratios, pull temperatures, kidding dates, altitude adjustments: the numbers every farm kitchen needs, worked out in seconds. No sign-up, works on your phone.</p>
    </header>
    <div class="tool-cards">
      <?php $n = 0; foreach (tools() as $slug => $t): ?>
        <a class="tool-card reveal" href="/tools/<?= $slug ?>/" style="--d:<?= $n++ * 60 ?>ms">
          <span class="tool-card__icon tool-card__icon--<?= $t['color'] ?>"><?= icon($t['icon']) ?></span>
          <strong><?= e($t['name']) ?></strong>
          <small><?= e($t['short']) ?></small>
          <span class="tool-card__go">Open tool <?= icon('arrow') ?></span>
        </a>
      <?php endforeach ?>
    </div>
    <div class="try-it reveal">
      <p class="hand">Try it right here ↓</p>
      <?= render_tool('brine-calculator') ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <header class="section__head reveal">
      <p class="eyebrow">Topic hubs</p>
      <h2>Explore the Purely Wholesome Farm journal</h2>
      <p><?= $liveCount ?> practical guides, organized the way a farm day actually runs: from the barn to the stove.</p>
    </header>
    <div class="topics">
      <?php $n = 0; foreach (TOPICS as $key => [$label, $blurb, $pillar]): if (empty($counts[$key])) continue; $img = $index[$pillar]['image'] ?? ''; ?>
        <a class="topic reveal" href="/topics/<?= $key ?>/" style="--d:<?= $n++ * 50 ?>ms">
          <span class="topic__img"><?php if ($img): ?><img src="<?= e($img) ?>" alt="" loading="lazy" width="300" height="200"><?php endif ?></span>
          <span class="topic__text"><strong><?= e($label) ?></strong><small><?= e($blurb) ?></small></span>
          <span class="topic__count"><?= (int)$counts[$key] ?></span>
        </a>
      <?php endforeach ?>
    </div>
  </div>
</section>

<section class="section section--cream season">
  <div class="wrap season__grid">
    <div class="season__copy reveal">
      <p class="eyebrow"><?= icon('calendar') ?> <?= date('F') ?> on the farm</p>
      <h2>This month at Purely Wholesome Farm: <span class="hl"><?= e($seasonLabel) ?></span></h2>
      <p><?= e($seasonBlurb) ?> Here is what is on the Purely Wholesome Farm to-do list right now, and the guides that help.</p>
      <a class="btn btn--ghost" href="/blog/">See everything <?= icon('arrow') ?></a>
    </div>
    <ol class="season__list">
      <?php foreach ($season as $i => $p): ?>
        <li class="reveal" style="--d:<?= $i * 80 ?>ms">
          <a href="<?= post_url($p['slug']) ?>">
            <span class="season__num"><?= str_pad((string)($i + 1), 2, '0', STR_PAD_LEFT) ?></span>
            <?php if ($p['image']): ?><img src="<?= e($p['image']) ?>" alt="" loading="lazy" width="120" height="80"><?php endif ?>
            <span><strong><?= e($p['h1']) ?></strong><small><?= (int)$p['minutes'] ?> min read</small></span>
          </a>
        </li>
      <?php endforeach ?>
    </ol>
  </div>
</section>

<section class="section story">
  <div class="wrap story__grid">
    <div class="story__art reveal" aria-hidden="true">
      <div class="story__ring"><svg viewBox="0 0 200 200"><defs><path id="circ" d="M100 100m-80 0a80 80 0 1 1 160 0a80 80 0 1 1-160 0"/></defs><text><textPath href="#circ" textLength="490" lengthAdjust="spacing">PURELY WHOLESOME FARM · GROW BETTER · LIVE SIMPLER · </textPath></text></svg><span><?= icon('sprout') ?></span></div>
      <?php if (!empty($index['goat-care']['image'])): ?><img src="<?= e($index['goat-care']['image']) ?>" alt="" loading="lazy" width="600" height="400"><?php endif ?>
    </div>
    <div class="story__copy">
      <p class="eyebrow reveal">Our roots</p>
      <h2 class="reveal">The Purely Wholesome Farm way</h2>
      <p class="reveal">Purely Wholesome Farm started with a simple idea: farming and scratch cooking should be accessible, practical and deeply rewarding. We write the way we would explain things over the fence: what worked, what didn’t, and what we would do differently next time.</p>
      <ul class="pillars">
        <li class="reveal"><?= icon('check') ?><div><strong>Practical over theory</strong><span>Every guide ends with something you can do today, in your kitchen or your barn.</span></div></li>
        <li class="reveal"><?= icon('shield') ?><div><strong>Checked against good sources</strong><span>Food safety and animal health advice is checked against USDA, extension and veterinary references.</span></div></li>
        <li class="reveal"><?= icon('heart') ?><div><strong>Reader-first, always</strong><span>No paid guest posts. Purely Wholesome Farm is written for home cooks and homesteaders, full stop.</span></div></li>
      </ul>
      <div class="stats">
        <div class="reveal"><strong data-count="<?= $liveCount ?>"><?= $liveCount ?></strong><span>practical guides</span></div>
        <div class="reveal"><strong data-count="<?= count(tools()) ?>"><?= count(tools()) ?></strong><span>free farm tools</span></div>
        <div class="reveal"><strong data-count="<?= count(array_filter($counts)) ?>"><?= count(array_filter($counts)) ?></strong><span>topic hubs</span></div>
      </div>
      <a class="btn btn--primary reveal" href="/about-us/">Read our story <?= icon('arrow') ?></a>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="wrap">
    <header class="section__head section__head--row reveal">
      <div>
        <p class="eyebrow">Just added</p>
        <h2>Fresh from the Purely Wholesome Farm kitchen</h2>
      </div>
      <a class="btn btn--ghost" href="/blog/">All articles <?= icon('arrow') ?></a>
    </header>
    <div class="cards">
      <?php foreach ($latest as $p): ?><?= card($p, 'reveal') ?><?php endforeach ?>
    </div>
  </div>
</section>

<section class="section faq-home">
  <div class="wrap wrap--narrow">
    <header class="section__head reveal">
      <p class="eyebrow">Good to know</p>
      <h2>Questions about Purely Wholesome Farm</h2>
    </header>
    <div class="faq">
      <?php foreach ($homeFaq as $i => [$q, $a]): ?>
        <details class="faq__item reveal" <?= $i === 0 ? 'open' : '' ?>><summary><?= e($q) ?><span class="faq__icon" aria-hidden="true"></span></summary><div class="faq__a"><p><?= e($a) ?></p></div></details>
      <?php endforeach ?>
    </div>
  </div>
</section>

<section class="section newsletter-wrap">
  <div class="wrap">
    <div class="newsletter reveal">
      <div class="newsletter__deco" aria-hidden="true"><?= icon('mail') ?></div>
      <div>
        <h2>Join the Purely Wholesome Farm letter</h2>
        <p>One email a month with the season’s recipes, homestead to-dos and new tools. No spam, unsubscribe any time.</p>
      </div>
      <?php include ROOT . '/app/views/partials/subscribe-form.php' ?>
    </div>
  </div>
</section>
