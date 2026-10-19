<?php
defined('PGF') || exit;

$crumbs = [['Home', '/'], ['About', '/about/']];
$page = [
    'path'   => '/about/',
    'title'  => 'About Pure Goat Farms — A Family-Run Dairy Goat Farm',
    'desc'   => 'Pure Goat Farms is a family-run dairy-goat operation. Everything we publish comes from chores done on our own land, not research pulled from somewhere else.',
    'image'  => IMG['story'],
    'crumbs' => $crumbs,
    'schema' => [
        ['@type' => 'AboutPage', '@id' => SITE_URL . '/about/#webpage', 'url' => SITE_URL . '/about/', 'name' => 'About Pure Goat Farms', 'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#organization']],
    ],
];
ob_start();
?>
<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal">About Pure Goat Farms</p>
    <h1 class="reveal">Two does, one bad fence, and a decade of learning by doing.</h1>
    <p class="page-hero__lead reveal">Pure Goat Farms is a family-run dairy-goat operation. Everything we publish comes from chores done on our own land, not research pulled from somewhere else.</p>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split__copy">
      <p class="eyebrow reveal">How we started</p>
      <h2 class="reveal">From two backyard does to a working dairy herd.</h2>
      <p class="reveal">We brought home our first pair of Nigerian Dwarf does not knowing the difference between browse and pasture, or how fast a goat can find the one gap in a fence. The first year taught us more about fencing, hoof care, and patience than any book could have.</p>
      <p class="reveal">A decade on, <a href="/">Pure Goat Farms</a> is home to 27 goats across six breeds, a working milking parlor, and a rotational pasture system we rebuild every spring. We still make mistakes. We just write about them now, so you don’t have to repeat them.</p>
    </div>
    <div class="split__media reveal" data-parallax="0.05">
      <img src="<?= IMG['story_768'] ?>" alt="The Pure Goat Farms herd resting in the grass" width="768" height="768" loading="lazy">
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">How we work</p>
      <h2>Our approach to every guide we publish.</h2>
    </div>
    <div class="steps">
      <div class="step reveal"><span class="step__n">01</span><h3>Test it on the herd</h3><p>Every routine, ratio, or remedy runs on our own goats for at least one full season before it becomes a guide.</p></div>
      <div class="step reveal"><span class="step__n">02</span><h3>Write down the exact numbers</h3><p>Real feed weights, real costs, real timeframes — the specifics that generic farming advice tends to round away.</p></div>
      <div class="step reveal"><span class="step__n">03</span><h3>Update it every season</h3><p>Kidding season, breeding season, and pasture conditions change what's true. We revisit guides as things shift.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head reveal">
      <p class="eyebrow">The herd, today</p>
      <h2>What's grazing the back forty right now.</h2>
    </div>
    <div class="herd-grid">
      <div class="herd-card reveal tilt"><span class="herd-card__icon"><?= icon('pail') ?></span><h3>Nigerian Dwarf &amp; Nubian does</h3><p>Our dairy line — high butterfat, easy hand-milking, and the source of most of our <a href="/category/milking-dairy/">Milking &amp; Dairy</a> notes.</p></div>
      <div class="herd-card reveal tilt"><span class="herd-card__icon"><?= icon('leaf') ?></span><h3>Boer crosses</h3><p>Raised for meat and pasture management, and where most of our grazing and browse-line notes come from.</p></div>
      <div class="herd-card reveal tilt"><span class="herd-card__icon"><?= icon('goat') ?></span><h3>A rotating cast of kids</h3><p>Every kidding season adds a handful of new personalities — and a fresh set of first-hand notes.</p></div>
    </div>
  </div>
</section>

<section class="section section--forest">
  <div class="container split split--center">
    <div>
      <p class="eyebrow eyebrow--light reveal">What you'll find here</p>
      <h2 class="reveal">Guides, tools and straight answers.</h2>
      <p class="reveal">Pure Goat Farms publishes in-depth guides on <a href="/how-much-milk-does-a-goat-produce-per-day/">goat milk production</a>, <a href="/best-dairy-goat-breeds-for-milk/">dairy breeds</a> and <a href="/category/health-care/">health and care</a>, and builds free <a href="/tools/">calculators</a> for the planning jobs every goat keeper faces.</p>
    </div>
    <ul class="check-list reveal">
      <li><?= icon('check') ?> <?= count(POSTS) ?> in-depth field guides</li>
      <li><?= icon('check') ?> <?= count(TOOLS) ?> free goat calculators</li>
      <li><?= icon('check') ?> Answers to the questions readers actually ask</li>
      <li><?= icon('check') ?> No paywalls, no pop-ups</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="container narrow center">
    <h2 class="reveal">Have a goat question of your own?</h2>
    <p class="reveal">Send it over — if enough people ask the same thing, it usually becomes its own field note.</p>
    <a class="btn btn--rust btn--lg reveal" href="/contact/">Get in touch <?= icon('arrow') ?></a>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
