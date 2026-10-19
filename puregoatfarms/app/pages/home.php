<?php
defined('PGF') || exit;

$posts = posts_sorted();
$featuredSlug = array_key_first($posts);
$homeFaq = [
    ['What is Pure Goat Farms?', 'Pure Goat Farms is a family-run dairy-goat farm and field guide. We publish practical, tested advice on goat milk production, dairy breeds, health care and everyday farm life, plus free calculators for goat keepers.'],
    ['Is Pure Goat Farms a real working farm?', 'Yes. Pure Goat Farms started with two Nigerian Dwarf does and has grown into a mixed herd of 27 goats across six breeds. Every routine we write about runs on our own goats for at least a full season first.'],
    ['How much milk does a goat produce per day?', 'Most full-size dairy goats produce about 0.5 to 1.5 gallons (4 to 12 pounds) of milk per day, while Nigerian Dwarfs give about 1 to 2 quarts. Breed, age, feed and stage of lactation all change the number.'],
    ['Can I visit Pure Goat Farms?', 'Pure Goat Farms is not currently open to the public, but we do make seasonal exceptions. Send us a note through the contact page and ask.'],
    ['Are the Pure Goat Farms tools free to use?', 'Yes. Every calculator on Pure Goat Farms — milk yield, lactation curve, cheese herd size, kidding dates, feed and breed finder — is free and runs right in your browser.'],
];

$page = [
    'path'   => '/',
    'title'  => 'Pure Goat Farms — Practical Goat Farming, Milk & Dairy Guides',
    'og_title' => 'Pure Goat Farms — Practical Goat Farming, Health & Dairy Guides',
    'desc'   => 'Pure Goat Farms is a working dairy-goat farm sharing field-tested guides on goat milk production, breeds, health and farm life — plus free goat calculators.',
    'preload' => IMG['hero_768'],
    'body_class' => 'page-home',
    'tools_js' => true,
    'schema' => [
        ['@type' => 'WebPage', '@id' => SITE_URL . '/#webpage', 'url' => SITE_URL . '/', 'name' => 'Pure Goat Farms — Practical Goat Farming, Milk & Dairy Guides', 'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#organization'], 'primaryImageOfPage' => abs_url(IMG['hero'])],
        schema_faq($homeFaq),
    ],
];

ob_start();
?>
<section class="hero">
  <div class="hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span><span class="blob blob--3"></span><span class="grain"></span></div>
  <div class="container hero__grid">
    <div class="hero__copy">
      <p class="eyebrow reveal"><span class="dot"></span> Working dairy herd · Field-tested guides</p>
      <h1 class="reveal"><span class="h1-brand">Pure Goat Farms</span> Raised on browse, <em>not just grass.</em></h1>
      <p class="hero__lead reveal">Welcome to Pure Goat Farms — a working goat farm sharing what actually works: how much milk a goat really gives, breed notes, health checklists, milking routines and kidding-season field notes, all tested on our own herd before they ever hit the page.</p>
      <div class="hero__actions reveal">
        <a class="btn btn--rust btn--lg magnetic" href="/blog/">Read Goat Farming Blog <?= icon('arrow') ?></a>
        <a class="btn btn--ghost btn--lg" href="/tools/">Try the Free Tools</a>
      </div>
      <ul class="hero__trust reveal">
        <li><?= icon('check') ?> Field-tested on 27 goats</li>
        <li><?= icon('check') ?> Real numbers, plain language</li>
        <li><?= icon('check') ?> 7 free goat calculators</li>
      </ul>
    </div>
    <div class="hero__media reveal" data-parallax="0.06">
      <div class="hero__frame">
        <img src="<?= IMG['hero_768'] ?>" srcset="<?= IMG['hero_768'] ?> 768w, <?= IMG['hero'] ?> 853w" sizes="(max-width: 900px) 90vw, 480px" alt="Dairy goats walking across green pasture at Pure Goat Farms" width="768" height="768" fetchpriority="high">
      </div>
      <div class="float-chip float-chip--a"><strong data-count="27">27</strong><span>goats in the herd</span></div>
      <div class="float-chip float-chip--b"><strong data-count="6">6</strong><span>breeds on pasture</span></div>
      <div class="float-chip float-chip--c"><?= icon('pail') ?><span>Milked twice daily</span></div>
      <svg class="spin-badge" viewBox="0 0 200 200" aria-hidden="true">
        <defs><path id="circ" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs>
        <circle cx="100" cy="100" r="96" />
        <text><textPath href="#circ">FIELD-TESTED • FARM-WRITTEN • SINCE DAY ONE • </textPath></text>
        <image href="<?= UPLOADS ?>cropped-Pure-Goat-Farms-Site-Icon-192x192.webp" x="62" y="62" width="76" height="76"/>
      </svg>
    </div>
  </div>
  <div class="hero__scroll" aria-hidden="true"><span></span></div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
<?php for ($i = 0; $i < 2; $i++): ?>
    <span>Milking &amp; Dairy</span><span class="sep">✦</span><span>Goat Breeds</span><span class="sep">✦</span><span>Health &amp; Care</span><span class="sep">✦</span><span>Kidding Season</span><span class="sep">✦</span><span>Farm Life</span><span class="sep">✦</span><span>Cheese Making</span><span class="sep">✦</span><span>Pasture Rotation</span><span class="sep">✦</span>
<?php endfor; ?>
  </div>
</div>

<section class="section stats">
  <div class="container">
    <h2 class="sr-only">Pure Goat Farms by the numbers</h2>
    <div class="stats__grid">
      <div class="stat reveal"><strong data-count="27">27</strong><span>Goats milked, kidded &amp; trimmed</span></div>
      <div class="stat reveal"><strong data-count="6">6</strong><span>Breeds across the herd</span></div>
      <div class="stat reveal"><strong data-count="10" data-suffix="+">10+</strong><span>Years of field notes</span></div>
      <div class="stat reveal"><strong data-count="<?= count(TOOLS) ?>"><?= count(TOOLS) ?></strong><span>Free goat calculators</span></div>
    </div>
  </div>
</section>

<section class="section" id="topics">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">What we cover</p>
      <h2>Five things every goat keeper needs to get right.</h2>
      <p>Every ear-tag below is a doorway into the notes we wish existed when we started. Pure Goat Farms organizes its guides the same way we organize the chores: milk, daily life, breeds and health — plus the tools to plan it all.</p>
    </div>
    <div class="tag-grid">
<?php foreach (CATEGORIES as $slug => $c): $n = count(posts_in($slug)); ?>
      <a class="ear-tag reveal tilt" href="/category/<?= $slug ?>/">
        <span class="ear-tag__hole" aria-hidden="true"></span>
        <span class="ear-tag__num"><?= $c['num'] ?></span>
        <span class="ear-tag__icon"><?= icon($c['icon']) ?></span>
        <h3><?= e($c['name']) ?></h3>
        <p><?= e($c['blurb']) ?></p>
        <span class="ear-tag__count"><?= $n ?> guide<?= $n === 1 ? '' : 's' ?> <?= icon('arrow') ?></span>
      </a>
<?php endforeach; ?>
      <a class="ear-tag ear-tag--dark reveal tilt" href="/tools/">
        <span class="ear-tag__hole" aria-hidden="true"></span>
        <span class="ear-tag__num">05</span>
        <span class="ear-tag__icon"><?= icon('chart') ?></span>
        <h3>Farm Tools</h3>
        <p>Calculators for milk yield, lactation, cheese, kidding dates, feed and breed choice.</p>
        <span class="ear-tag__count"><?= count(TOOLS) ?> free tools <?= icon('arrow') ?></span>
      </a>
    </div>
  </div>
</section>

<section class="section section--sand milk-quick" id="milk-estimator">
  <div class="container milk-quick__grid">
    <div class="milk-quick__copy reveal">
      <p class="eyebrow">Interactive</p>
      <h2>How much milk does a goat produce?</h2>
      <p>It is the question Pure Goat Farms gets asked more than any other. Pick a breed and slide through the lactation to see what a healthy doe typically gives — per milking, per day and across a full season.</p>
      <p class="muted small">Typical figures for well-fed does milked twice daily. For a full lactation curve, open the <a href="/tools/goat-milk-production-estimator/">Goat Milk Production Estimator</a>.</p>
      <a class="link-arrow" href="/how-much-milk-does-a-goat-produce-per-day/">See the breed-by-breed chart <?= icon('arrow') ?></a>
    </div>
    <div class="milk-widget reveal" data-tool="quick-milk">
      <div class="chip-row" role="radiogroup" aria-label="Breed">
        <button type="button" class="chip is-on" data-breed="saanen" role="radio" aria-checked="true">Saanen</button>
        <button type="button" class="chip" data-breed="alpine" role="radio" aria-checked="false">Alpine</button>
        <button type="button" class="chip" data-breed="lamancha" role="radio" aria-checked="false">LaMancha</button>
        <button type="button" class="chip" data-breed="nubian" role="radio" aria-checked="false">Nubian</button>
        <button type="button" class="chip" data-breed="nigerian" role="radio" aria-checked="false">Nigerian Dwarf</button>
      </div>
      <label class="range-label" for="qm-month">Month of lactation: <output id="qm-month-out">2</output></label>
      <input id="qm-month" type="range" min="1" max="10" value="2" step="1">
      <div class="milk-widget__body">
        <div class="pail-viz" aria-hidden="true">
          <div class="pail-viz__pail"><span class="pail-viz__milk"></span><span class="pail-viz__wave"></span></div>
          <span class="pail-viz__handle"></span>
        </div>
        <dl class="milk-widget__stats" aria-live="polite">
          <div><dt>Per milking</dt><dd id="qm-milking">—</dd></div>
          <div><dt>Per day</dt><dd id="qm-day">—</dd></div>
          <div><dt>Full season</dt><dd id="qm-season">—</dd></div>
        </dl>
      </div>
    </div>
  </div>
</section>

<section class="section" id="latest">
  <div class="container">
    <div class="section-head section-head--row reveal">
      <div>
        <p class="eyebrow">Latest</p>
        <h2>Fresh from the field.</h2>
        <p>New notes from the Pure Goat Farms barn, the milking stand and the pasture — published as we learn it.</p>
      </div>
      <a class="btn btn--ghost" href="/blog/">Read More Blogs</a>
    </div>
    <div class="post-grid post-grid--home">
<?php $i = 0; foreach ($posts as $slug => $p): if ($i++ >= 4) break; ?>
      <?= post_card($slug, $p, $slug === $featuredSlug ? 'post-card--feature' : '') ?>
<?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section--forest tools-band">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow eyebrow--light">Free goat tools</p>
      <h2>Plan the herd with real numbers.</h2>
      <p>The same calculators we use around Pure Goat Farms to plan breeding, milk, feed and cheese — free, fast and private (everything runs in your browser).</p>
    </div>
    <div class="tool-grid">
<?php foreach (array_slice(TOOLS, 0, 6, true) as $slug => $t): ?>
      <?= tool_card($slug, $t) ?>
<?php endforeach; ?>
    </div>
    <p class="center reveal"><a class="btn btn--gold" href="/tools/">See all <?= count(TOOLS) ?> tools</a></p>
  </div>
</section>

<section class="section why">
  <div class="container why__grid">
    <div class="why__media reveal">
      <img src="<?= IMG['story_768'] ?>" alt="The Pure Goat Farms herd resting together in tall grass" width="768" height="768" loading="lazy">
      <div class="why__badge"><strong>100%</strong><span>tested on our own herd</span></div>
    </div>
    <div class="why__copy">
      <p class="eyebrow reveal">Why Pure Goat Farms</p>
      <h2 class="reveal">Written on the farm, not around it.</h2>
      <p class="reveal">No recycled listicles. Every Pure Goat Farms guide comes from chores we have actually done, more than once, in every season.</p>
      <ol class="why__list">
        <li class="reveal"><span class="why__n">01</span><div><h3>Tested on our own herd first</h3><p>If a method doesn't hold up on our 27 goats across a full year, it doesn't go in a guide.</p></div></li>
        <li class="reveal"><span class="why__n">02</span><div><h3>Plain language, real numbers</h3><p>Actual gestation windows, actual feed ratios, actual milk weights — not vague ranges pulled from a textbook.</p></div></li>
        <li class="reveal"><span class="why__n">03</span><div><h3>Built for every scale</h3><p>Whether you keep two pet wethers or run forty dairy does, the advice scales down without losing the detail.</p></div></li>
      </ol>
    </div>
  </div>
</section>

<section class="section section--sand story">
  <div class="container story__grid">
    <div class="story__copy">
      <p class="eyebrow reveal">Our story</p>
      <h2 class="reveal">A small dairy herd that turned into a field guide.</h2>
      <p class="reveal">Pure Goat Farms started with two Nigerian Dwarf does and a lot of mistakes. A decade later we're milking, kidding, and pasture-managing a mixed herd — and writing down everything we had to learn the hard way.</p>
      <p class="reveal">This site is the notebook we wish we'd had on day one: specific, seasonal, and written for people actually doing the chores. That is the whole idea behind Pure Goat Farms.</p>
      <a class="btn btn--rust reveal" href="/about/">Learn Our Story <?= icon('arrow') ?></a>
    </div>
    <div class="timeline reveal">
      <div class="timeline__item"><span class="timeline__year">Day one</span><p>Two Nigerian Dwarf does, one bad fence, and our first kidding season.</p></div>
      <div class="timeline__item"><span class="timeline__year">Growing</span><p>Nubians join the Nigerians in the dairy line, and the milking routine gets serious.</p></div>
      <div class="timeline__item"><span class="timeline__year">Expanding</span><p>Boer crosses arrive for meat and browse management; rotational grazing begins.</p></div>
      <div class="timeline__item"><span class="timeline__year">Today</span><p>27 goats across six breeds, a working milking parlor — and this field guide.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container narrow">
    <div class="section-head center reveal">
      <p class="eyebrow">Questions</p>
      <h2>About Pure Goat Farms</h2>
    </div>
    <?= faq_html($homeFaq, '') ?>
    <p class="center"><a class="link-arrow" href="/faq/">More goat questions answered <?= icon('arrow') ?></a></p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
