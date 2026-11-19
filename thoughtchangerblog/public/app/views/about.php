<?php
$count = count(posts());
$start = array_slice(featured_posts(), 0, 3);
$topics = [
    'Life is fleeting' => 'life-is-fleeting-5-ways-to-slow-it-down', 'Leveling up' => 'heres-what-it-means-to-level-up',
    'Staying in your lane' => 'stick-to-your-lane', 'Becoming seasoned' => 'becoming-seasoned',
    'Island time' => 'how-island-time-can-be-all-the-time', 'Your own light' => 'the-power-of-your-own-light',
    'Complacency' => '11-signs-youre-stuck-in-complacency', 'Letting go' => 'the-subtle-difference-between-giving-up-and-letting-go',
    'Boundaries' => 'boundaries-vs-barriers', 'Gratitude' => 'gratitude-is-the-highest-attitude',
    'Having an inkling' => 'meaning-begins-with-an-inkling', 'Finding your calling' => 'how-do-you-know-when-your-calling-has-called',
    'The rabbit hole' => 'how-to-love-the-rabbit-hole', 'Progress, not perfection' => '6-reasons-why-progress-not-perfection',
];
view('head', ['meta' => [
    'title' => 'About Us - Thought Changer',
    'description' => 'Thought Changer exists for one simple reason:change begins with a thought. Not the loud, dramatic kind. The small ones.',
    'canonical' => '/about-us/', 'bodyClass' => 'page about', 'preload' => '/wp-content/uploads/2026/01/Thought-Changer-BG.webp',
    'schema' => [
        ['@type' => 'AboutPage', '@id' => SITE_URL . '/about-us/#webpage', 'url' => SITE_URL . '/about-us/', 'name' => 'About Us - Thought Changer',
         'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#organization']],
        ['@type' => 'BreadcrumbList', 'itemListElement' => [['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => SITE_URL . '/'], ['@type' => 'ListItem', 'position' => 2, 'name' => 'About Us']]],
    ],
]]);
?>
<section class="about-hero">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap about-hero-inner">
    <img class="about-emblem" src="<?= SITE_ICON ?>" width="96" height="96" alt="" aria-hidden="true">
    <span class="eyebrow">About Thought Changer</span>
    <h1 class="page-title">About Us</h1>
    <p class="about-lede">Thought Changer exists for one simple reason:<br><strong>change begins with a thought.</strong></p>
  </div>
  <svg class="hero-wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0c240 50 480 75 720 75S1200 50 1440 0v90H0Z" fill="currentColor"/></svg>
</section>

<section class="band about-story">
  <div class="wrap about-split">
    <div class="prose reveal">
      <p class="about-big">Not the loud, dramatic kind.<br>The small ones.<br>The fleeting realizations.</p>
      <p>The moments that make you pause and see something—yourself, a situation, or the world—a little differently. This site was created to explore those moments.</p>
      <p>Every day presents metaphors, lessons, and quiet signals we often overlook. A conversation that lingers longer than expected. A routine that suddenly feels heavy. A small shift in perspective that changes how we respond instead of react. Thought Changer shines a light on those experiences and the takeaways hidden inside them.</p>
      <p>This isn’t a place for quick fixes or empty motivation. It’s a space for reflection. For noticing patterns. For understanding how <a href="/mindset/">mindset</a> shapes action—and how action reinforces mindset.</p>
    </div>
    <aside class="about-quote reveal">
      <svg viewBox="0 0 48 48" width="44" height="44" aria-hidden="true"><path fill="currentColor" d="M10 34c-3 0-5-2.6-5-6.4C5 19 10.7 12.5 18 10l1.5 2.6c-4.6 2-7.5 5.6-7.9 9.4h1.3c3 0 5.1 2.2 5.1 5.4 0 3.6-2.8 6.6-8 6.6Zm21 0c-3 0-5-2.6-5-6.4C26 19 31.7 12.5 39 10l1.5 2.6c-4.6 2-7.5 5.6-7.9 9.4h1.3c3 0 5.1 2.2 5.1 5.4 0 3.6-2.8 6.6-8 6.6Z"/></svg>
      <p>Sometimes, all it takes is one thought—seen clearly—to change everything that follows.</p>
      <span>One thought at a time.</span>
    </aside>
  </div>
</section>

<section class="band band-soft">
  <div class="wrap">
    <h2 class="section-title reveal">One Thought at a Time</h2>
    <p class="section-lede reveal">Growth doesn’t happen all at once. It happens gradually, through accumulated awareness. A single thought questioned. A belief reframed. A habit examined honestly. Over time, those small mental shifts create meaningful change.</p>
    <div class="steps">
      <div class="step reveal"><span class="step-n">01</span><h3>Notice</h3><p>Catch the small moment—the phrase, the pattern, the feeling—before it slips past. Like an <a href="/meaning-begins-with-an-inkling/">inkling</a> worth following.</p></div>
      <div class="step reveal"><span class="step-n">02</span><h3>Reframe</h3><p>Look again from a new angle. A metaphor, a <a href="/quotes/">quote</a>, or a question can shift how something familiar feels.</p></div>
      <div class="step reveal"><span class="step-n">03</span><h3>Choose</h3><p>Carry one insight into your day. Not an overhaul—just <a href="/6-reasons-why-progress-not-perfection/">progress, not perfection</a>.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2 class="section-title reveal">What You’ll Find Here</h2>
    <div class="explore-grid">
      <a class="explore reveal" href="/mindset/"><span class="explore-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26"><path fill="currentColor" d="M12 2a10 10 0 1 1 0 20 10 10 0 0 1 0-20Zm0 2a8 8 0 1 0 0 16 8 8 0 0 0 0-16Zm4.2 3.8-2.4 6-6 2.4 2.4-6 6-2.4ZM12 11a1 1 0 1 0 0 2 1 1 0 0 0 0-2Z"/></svg></span><h3>Mindset</h3><p>The subtle patterns of thought that shape daily choices and long-term direction.</p><span class="explore-go">Explore mindset →</span></a>
      <a class="explore reveal" href="/quotes/"><span class="explore-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26"><path fill="currentColor" d="M5 18c-1.5 0-2.5-1.3-2.5-3.2C2.5 10.5 5.3 7.2 9 6l.8 1.3C7.5 8.3 6 10.1 5.8 12h.7c1.5 0 2.5 1.1 2.5 2.7C9 16.5 7.6 18 5 18Zm10.5 0c-1.5 0-2.5-1.3-2.5-3.2 0-4.3 2.8-7.6 6.5-8.8l.8 1.3c-2.3 1-3.8 2.8-4 4.7h.7c1.5 0 2.5 1.1 2.5 2.7 0 1.8-1.4 3.3-4 3.3Z"/></svg></span><h3>Quotes</h3><p>Lines worth sitting with—what they mean and how to carry them into real life.</p><span class="explore-go">Read the quotes →</span></a>
      <a class="explore reveal" href="/blog/"><span class="explore-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26"><path fill="currentColor" d="M12 2c.5 4.7 2.8 7.5 8 8-5.2.5-7.5 3.3-8 8-.5-4.7-2.8-7.5-8-8 5.2-.5 7.5-3.3 8-8Zm7 12c.2 2 1.2 3 3 3.2-1.8.2-2.8 1.2-3 3.3-.2-2.1-1.2-3.1-3-3.3 1.8-.2 2.8-1.2 3-3.2Z"/></svg></span><h3>Meanings &amp; Metaphors</h3><p>Everyday phrases and images—rivers, rainbows, island time—and the insight inside them.</p><span class="explore-go">Browse all <?= $count ?> articles →</span></a>
      <a class="explore reveal" href="/recommended-reads/"><span class="explore-icon" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26"><path fill="currentColor" d="M4 3h4a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm1 2v14h2V5H5Zm6-2h4a1 1 0 0 1 1 1v16a1 1 0 0 1-1 1h-4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm1 2v14h2V5h-2Zm5.6.3 3.8-1 .5 1.9 3.6 13.5-.5 1-3.9 1-1-.6L17 6.3l.6-1Zm1.4 2.1 3.1 11.6 1-.3L19.9 7.1l-.9.3Z"/></svg></span><h3>The Bookshelf</h3><p>The books behind our articles, for when you want to go deeper on a theme.</p><span class="explore-go">See recommended reads →</span></a>
    </div>
  </div>
</section>

<section class="band band-soft">
  <div class="wrap">
    <h2 class="section-title reveal">How We Write</h2>
    <div class="values">
      <div class="value reveal"><h3>Reflection over noise</h3><p>No urgency, no hype. Writing meant to be felt, not rushed.</p></div>
      <div class="value reveal"><h3>Insight, not instructions</h3><p>Not answers, but better questions—and practical ways to try them.</p></div>
      <div class="value reveal"><h3>Honest about nuance</h3><p>Life holds <a href="/want-some-clarity-embrace-the-dichotomy/">two truths at once</a>. We try to, too.</p></div>
      <div class="value reveal"><h3>Meet you where you are</h3><p>No pressure to transform overnight. No promises of instant results.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2 class="section-title reveal">Start Here</h2>
    <p class="section-lede reveal">New to Thought Changer? These are the reflections readers return to most.</p>
    <div class="grid grid-3">
      <?php foreach ($start as $p) view('card', ['p' => $p]); ?>
    </div>
    <div class="topic-cloud reveal">
      <span class="chips-label">Popular topics:</span>
      <?php foreach ($topics as $label => $slug): ?><a href="/<?= $slug ?>/"><?= e($label) ?></a><?php endforeach; ?>
    </div>
  </div>
</section>

<section class="cta-band">
  <div class="cta-bg" aria-hidden="true"></div>
  <div class="wrap-narrow cta-inner reveal">
    <h2>Say Hello</h2>
    <p>Have a thought to share, a question, or a reflection sparked by something you read here? We read every message.</p>
    <div class="hero-ctas">
      <a href="/contact-us/" class="btn btn-light">Contact Us</a>
      <a href="mailto:<?= SITE_EMAIL ?>" class="btn btn-cyan"><?= SITE_EMAIL ?></a>
    </div>
  </div>
</section>
<?php view('foot'); ?>
