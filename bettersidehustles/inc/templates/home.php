<?php
$posts = all_posts();
$cityPosts = array_values(array_filter($posts, fn($p) => ($p['category'] ?? '') === 'City Guides'));
$latest = array_slice(array_values(array_filter($posts, fn($p) => ($p['category'] ?? '') !== 'City Guides')), 0, 3);
$latestCities = array_slice($cityPosts, 0, 3);
$cities = array_map(fn($p) => [$p['city'] ?? preg_replace('/^Best (Side )?Hustles in /', '', $p['h1']), $p['state'] ?? '', $p['url']], $cityPosts);
usort($cities, fn($a, $b) => strcmp($a[0], $b[0]));
$quiz = tool_html('quiz', 'full');

$faq = [
    ['q' => 'What is Better Side Hustles?', 'a' => 'Better Side Hustles is a free resource that helps you find, start and grow a side hustle. We publish platform guides (Fiverr, Uber, Udemy, Shopify and more), side hustle guides for 70+ US cities and free calculators for income, taxes and pricing.'],
    ['q' => 'What is the best side hustle to start in 2026?', 'a' => 'The best side hustle is the one that fits the hours, skills and money you have right now. Delivery and rideshare pay fastest; freelancing, digital marketing and local services like cleaning pay more per hour; courses, print-on-demand and affiliate sites take longer but can grow. Take our 60-second quiz to get matched.'],
    ['q' => 'How do I find side jobs near me?', 'a' => 'Start with our city guides — each one lists the gig apps, local services and seasonal work that pay in that city. Then check local Facebook groups, Nextdoor, TaskRabbit, Rover and Craigslist gigs, and offer your service to neighbors directly.'],
    ['q' => 'Can I start a side hustle with no money?', 'a' => 'Yes. Freelancing on Fiverr, online tutoring, pet sitting, delivery on a bike and selling things you already own all cost little or nothing to start. Spend money only after a hustle has earned its first few hundred dollars.'],
    ['q' => 'How much can a side hustle realistically make?', 'a' => 'Most people earn $300 to $1,500 a month working 5–15 hours a week. Skilled freelance and digital marketing work can pass $3,000 a month part-time. Use our side hustle income calculator to see what your hours are worth.'],
    ['q' => 'Do I have to pay taxes on side hustle income?', 'a' => 'Yes. If you net $400 or more from self-employment in a year you owe self-employment tax, plus regular income tax. Setting aside 25–30% of profit is a safe rule — our side hustle tax calculator gives you a closer number.'],
];

$meta = [
    'title' => 'Better Side Hustles | Side Hustle Ideas & Side Jobs Near You',
    'og_title' => 'Better Side Hustles — Find a Side Hustle That Actually Pays',
    'description' => 'Better Side Hustles helps you find side hustle ideas that pay: platform guides, side jobs in 70+ US cities and free income, tax and pricing calculators.',
    'url' => '/',
    'bodyClass' => 'is-home',
    'schema' => [
        ['@type' => 'WebPage', '@id' => SITE_URL . '/#webpage', 'url' => SITE_URL . '/', 'name' => 'Better Side Hustles', 'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#org']],
        schema_faq($faq),
    ],
];
require __DIR__ . '/header.php';
?>
<section class="hero">
  <canvas class="coin-canvas" aria-hidden="true"></canvas>
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow"><i></i>Better Side Hustles · Updated for 2026</span>
      <h1>Find a side hustle that <span class="hl">actually pays</span> — and fits your life.</h1>
      <p class="lead">Better Side Hustles gives you honest side hustle ideas, real pay ranges and free calculators, so you can stop scrolling and start earning extra money this week.</p>
      <div class="btn-row">
        <a class="btn btn-green btn-lg" href="#quiz"><?= icon('target') ?>Find my side hustle</a>
        <a class="btn btn-ghost btn-lg" href="#cities"><?= icon('pin') ?>Side hustles near me</a>
      </div>
      <div class="hero-stats">
        <div><b data-countup="<?= count($posts) ?>" data-suffix="+"><?= count($posts) ?>+</b><span>in-depth guides</span></div>
        <div><b data-countup="<?= count($cityPosts) ?>"><?= count($cityPosts) ?></b><span>city side hustle guides</span></div>
        <div><b data-countup="<?= count(TOOLS) ?>"><?= count(TOOLS) ?></b><span>free money tools</span></div>
      </div>
    </div>
    <div class="phone-wrap" aria-hidden="true">
      <div class="phone">
        <div class="phone-screen">
          <div class="phone-bal"><small>Side hustle earnings this week</small><b data-total>$0.00</b><span class="up">▲ 18% vs last week</span></div>
          <svg class="spark" viewBox="0 0 260 56" preserveAspectRatio="none"><defs><linearGradient id="sparkfill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7ED957" stop-opacity=".45"/><stop offset="1" stop-color="#7ED957" stop-opacity="0"/></linearGradient></defs><path class="area" d="M0 50 L30 44 L60 46 L90 34 L120 38 L150 24 L180 28 L210 14 L240 16 L260 6 L260 56 L0 56Z"/><path d="M0 50 L30 44 L60 46 L90 34 L120 38 L150 24 L180 28 L210 14 L240 16 L260 6"/></svg>
          <ul class="earn-feed"></ul>
        </div>
        <div class="phone-chip chip-1"><?= icon('dollar') ?>+$85 Fiverr order</div>
        <div class="phone-chip chip-2"><?= icon('chart') ?>Goal: 64% reached</div>
      </div>
    </div>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">
<?php $ideas = ['Freelance writing', 'Food delivery', 'Dog walking', 'Rideshare driving', 'Online tutoring', 'Print-on-demand', 'UGC videos', 'Social media management', 'Airbnb cleaning', 'Udemy courses', 'Handyman jobs', 'Thrift flipping', 'Virtual assistant', 'Local SEO', 'Pressure washing', 'Affiliate marketing'];
foreach (array_merge($ideas, $ideas) as $i) echo '<span>' . e($i) . '</span>'; ?>
</div></div>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="pill">Welcome to Better Side Hustles</span>
      <h2>Side hustle ideas for every schedule</h2>
      <p>Whether you have five spare hours or twenty, there is a side hustle that fits. Better Side Hustles groups the best ideas into four paths so you can see your options at a glance.</p>
    </div>
    <div class="grid grid-4">
      <a class="card cat-card glow reveal" href="/fiverr/"><img src="/wp-content/uploads/2023/07/bettersidehustles-freelancing.webp" alt="Freelancing side hustles" width="84" height="84" loading="lazy"><h3>Freelancing</h3><p>Writing, design, marketing and admin work you can sell on Fiverr or directly to clients.</p></a>
      <a class="card cat-card glow reveal" href="/lyft-uber/"><img src="/wp-content/uploads/2023/07/bettersidehustles-transportation.webp" alt="Transportation side hustles" width="84" height="84" loading="lazy"><h3>Transportation</h3><p>Rideshare, food and grocery delivery and courier gigs that pay out within days.</p></a>
      <a class="card cat-card glow reveal" href="/udemy/"><img src="/wp-content/uploads/2023/07/bettersidehustles-courses.webp" alt="Online course side hustles" width="84" height="84" loading="lazy"><h3>Courses</h3><p>Turn what you know into an online course on Udemy, Skillshare or Thinkific.</p></a>
      <a class="card cat-card glow reveal" href="/shopify/"><img src="/wp-content/uploads/2023/07/bettersidehustles-ecommerce.webp" alt="E-commerce side hustles" width="84" height="84" loading="lazy"><h3>E-Commerce</h3><p>Print-on-demand, digital products and reselling with a Shopify store.</p></a>
    </div>
  </div>
</section>

<section class="section section-soft" id="quiz">
  <div class="wrap split">
    <div class="reveal">
      <span class="pill">60-second quiz</span>
      <h2>Not sure where to start? Let us match you.</h2>
      <p>The Better Side Hustles matcher weighs your time, goals, skills, budget and whether you have a car — then ranks 18 proven side hustles for you. No email required.</p>
      <ul class="checks">
        <li><?= icon('check') ?><span><strong>Personal results</strong> — three ranked matches with typical pay.</span></li>
        <li><?= icon('check') ?><span><strong>Straight to the how-to</strong> — each match links to a step-by-step guide.</span></li>
        <li><?= icon('check') ?><span><strong>Then plan your number</strong> with the <a href="/tools/income-calculator/">income calculator</a>.</span></li>
      </ul>
    </div>
    <div><?= $quiz ?></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="pill">Platform guides</span>
      <h2>Side hustles you can start on these platforms</h2>
      <p>Better Side Hustles breaks down how each platform pays, what it costs to start and how much people realistically earn.</p>
    </div>
    <div class="grid grid-2">
      <?php foreach (PLATFORMS as $slug => [$name, $logo, $blurb]): ?>
      <a class="card plat-card glow reveal" href="/<?= $slug ?>/"><img src="<?= e($logo) ?>" alt="<?= e($name) ?> logo" width="64" height="64" loading="lazy"><div><h3><?= e($name) ?> side hustle</h3><p><?= e($blurb) ?></p></div><span class="go"><?= icon('arrow') ?></span></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section section-soft" id="cities">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="pill">Side jobs near you</span>
      <h2>Find the best side hustles in your city</h2>
      <p>Local pay, busy seasons and neighborhood demand change everything. Better Side Hustles has a dedicated guide for <?= count($cityPosts) ?> US cities — type yours below.</p>
    </div>
    <form class="finder reveal" data-city-finder data-cities="<?= e(json_encode($cities, JSON_UNESCAPED_SLASHES)) ?>" role="search">
      <label class="search"><?= icon('search') ?><span class="sr-only" hidden>City</span><input type="search" placeholder="Search a city — e.g. Indianapolis, Sacramento, Austin" aria-label="Search city guides" autocomplete="off"><button class="btn btn-sm" type="submit">Go</button></label>
      <ul></ul>
    </form>
    <div class="city-chips reveal">
      <?php foreach (['indianapolis', 'sacramento', 'santa-ana', 'houston', 'chicago', 'austin', 'phoenix', 'new-york', 'atlanta', 'denver', 'seattle', 'miami'] as $c):
          $p = content_load("best-side-hustles-in-$c"); if (!$p) continue; ?>
      <a href="<?= e($p['url']) ?>"><?= e($p['city'] ?? ucwords(str_replace('-', ' ', $c))) ?></a>
      <?php endforeach; ?>
      <a href="/best-hustles-in-los-angeles/">Los Angeles</a>
      <a href="/side-hustles-you-can-do-in-hawaii-aloha-spirit-while-earning/">Hawaii</a>
      <a href="/side-job-hustles-in-texas-emerging-trends-and-opportunities-for-all/">Texas</a>
      <a href="/blog/?cat=city-guides">All cities →</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split rev">
    <div class="reveal">
      <span class="pill">Why Better Side Hustles</span>
      <h2>Small, steady income adds up faster than you think</h2>
      <p>Most people quit a side hustle before it compounds. Better Side Hustles is built to keep you going: we show you realistic pay instead of hype, the fees each platform takes and the next step that grows your income.</p>
      <ul class="checks">
        <li><?= icon('check') ?><span><strong>Real numbers.</strong> Pay ranges, fees and startup costs in every guide.</span></li>
        <li><?= icon('check') ?><span><strong>Local and online.</strong> City-specific gigs plus work you can do from your phone or laptop.</span></li>
        <li><?= icon('check') ?><span><strong>Free tools.</strong> Calculators for income, gig driving, taxes, freelance rates and product profit.</span></li>
      </ul>
      <a class="btn" href="/about/">How Better Side Hustles works</a>
    </div>
    <div class="growth reveal" aria-label="Example: $400 a month side hustle income invested over five years">
      <strong style="color:var(--ink)">$400/month from a side hustle, invested at 7%</strong>
      <div class="growth-bars">
        <div style="--h:12%"><span>$4.9k</span></div><div style="--h:26%"><span>$10.2k</span></div><div style="--h:41%"><span>$16.0k</span></div><div style="--h:57%"><span>$22.2k</span></div><div style="--h:74%"><span>$28.9k</span></div><div style="--h:92%"><span>$35.9k</span></div>
      </div>
      <div class="growth-labels"><span>Yr 1</span><span>Yr 2</span><span>Yr 3</span><span>Yr 4</span><span>Yr 5</span><span>Yr 6</span></div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="pill">Free calculators</span>
      <h2>Run the numbers before you start</h2>
      <p>Every Better Side Hustles tool is free, works on your phone and shows results instantly.</p>
    </div>
    <div class="grid grid-4">
      <?php foreach (TOOLS as $slug => [, $name, $desc, $ic]): ?>
      <a class="card tool-card glow reveal" href="/tools/<?= $slug ?>/"><span class="ti"><?= icon($ic) ?></span><h3><?= e($name) ?></h3><p><?= e($desc) ?></p><span class="more">Open tool <?= icon('arrow') ?></span></a>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="pill">How it works</span>
      <h2>From idea to first payout in three steps</h2>
    </div>
    <div class="grid grid-3 how">
      <div class="card how-step reveal"><h3>Pick your hustle</h3><p>Take the quiz or browse the Better Side Hustles platform and city guides to find work that fits your time and skills.</p></div>
      <div class="card how-step reveal"><h3>Set it up in a weekend</h3><p>Follow the step-by-step checklist in each guide: sign-ups, gear, pricing and your first listing or shift.</p></div>
      <div class="card how-step reveal"><h3>Track and grow</h3><p>Use our calculators to price smarter, set aside taxes and decide when to raise rates or add a second income stream.</p></div>
    </div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap">
    <div class="section-head reveal">
      <span class="pill">Fresh from the blog</span>
      <h2>Latest side hustle guides</h2>
    </div>
    <div class="grid grid-3">
      <?php foreach (array_merge($latest, $latestCities) as $p) echo post_card($p); ?>
    </div>
    <p style="text-align:center;margin-top:32px"><a class="btn btn-outline" href="/blog/">See all <?= count($posts) ?> guides</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="pill">Side hustle gear</span>
      <h2>The starter kit we recommend</h2>
      <p>You don't need much to start, but a few inexpensive tools make side hustles faster and more professional. These are the picks Better Side Hustles readers ask about most.</p>
      <a class="btn" href="/side-hustle-gear/"><?= icon('box') ?>See the full gear guide</a>
    </div>
    <div><?= gear_box(['phone-mount', 'ring-light', 'label-printer', 'book-side-hustle'], 'Four tools that pay for themselves') ?></div>
  </div>
</section>

<section class="section section-soft">
  <div class="wrap" style="max-width:860px">
    <div class="section-head reveal">
      <span class="pill">FAQ</span>
      <h2>Side hustle questions, answered</h2>
    </div>
    <div class="faq">
      <?php foreach ($faq as $i => $f): ?>
      <details<?= $i === 0 ? ' open' : '' ?>><summary><?= e($f['q']) ?></summary><div><p><?= e($f['a']) ?></p></div></details>
      <?php endforeach; ?>
    </div>
    <p style="text-align:center;margin-top:28px">Have a question we didn't cover? <a href="/contact/">Contact the Better Side Hustles team</a>.</p>
  </div>
</section>
<?php require __DIR__ . '/footer.php'; ?>
