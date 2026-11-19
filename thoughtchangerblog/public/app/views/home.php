<?php
$featured = featured_posts();
view('head', ['meta' => [
    'title' => 'Thought Changer - One Thought at a Time.',
    'description' => 'Thought Changer is a space for reflection, perspective, and intentional living. Explore the everyday moments that shape how we think.',
    'canonical' => '/', 'bodyClass' => 'home', 'preload' => '/wp-content/uploads/2026/01/Thought-Changer-BG.webp',
    'schema' => [['@type' => 'WebPage', '@id' => SITE_URL . '/#webpage', 'url' => SITE_URL . '/', 'name' => 'Thought Changer - One Thought at a Time.',
                  'isPartOf' => ['@id' => SITE_URL . '/#website'], 'about' => ['@id' => SITE_URL . '/#organization']]],
]]);
?>
<section class="hero">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="hero-inner wrap">
    <h1 class="script-title hero-title">One Thought Can Change Everything.</h1>
    <p class="hero-lede">Thought Changer is a space for reflection, perspective, and intentional living. Here, we explore the everyday moments and quiet metaphors that shape how we think—and how we act. Not with noise or urgency, but with awareness.</p>
    <div class="hero-ctas">
      <a href="/blog/" class="btn btn-dark">Latest Articles</a>
      <a href="/quotes/" class="btn btn-accent">Read Quotes</a>
    </div>
  </div>
  <svg class="hero-wave" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0c240 50 480 75 720 75S1200 50 1440 0v90H0Z" fill="currentColor"/></svg>
</section>

<section class="intro wrap-narrow reveal">
  <p>Life rarely announces its lessons. They appear in routines, conversations, pauses, and patterns we almost miss. Thought Changer exists to slow things down—to notice what’s already there and uncover the insight beneath it.</p>
  <p class="intro-pull">This isn’t about motivation or answers.<br>It’s about noticing. Reframing. Choosing differently.</p>
  <p>Each piece you’ll find here is an invitation to think deeper, reflect longer, and carry something forward after you leave.</p>
</section>

<section class="featured" id="featured">
  <div class="wrap">
    <span class="eyebrow center-block reveal">Readers’ favorites</span>
    <h2 class="section-title reveal">Featured Articles</h2>
    <div class="feature-grid">
      <?php foreach (array_slice($featured, 0, 3) as $i => $p): ?>
      <a class="feature reveal<?= $i === 0 ? ' feature-lg' : '' ?>" href="/<?= e($p['slug']) ?>/">
        <img src="<?= e($i === 0 ? $p['image'] : thumb($p['image'])) ?>" srcset="<?= e(img_srcset($p['image'])) ?>" sizes="(max-width: 900px) 100vw, <?= $i === 0 ? '60vw' : '35vw' ?>" width="1536" height="1024" alt="<?= e($p['image_alt']) ?>" loading="lazy" decoding="async">
        <span class="feature-rank" aria-hidden="true"><?= $i + 1 ?></span>
        <span class="feature-text"><span class="card-tag"><?= e(primary_cat($p)) ?></span><strong><?= e($p['title']) ?></strong><span class="feature-desc"><?= e($p['description']) ?></span><span class="feature-more">Read article →</span></span>
      </a>
      <?php endforeach; ?>
    </div>
    <ol class="ranked" start="4">
      <?php foreach (array_slice($featured, 3, 8) as $i => $p): ?>
      <li class="reveal">
        <a href="/<?= e($p['slug']) ?>/">
          <span class="ranked-n"><?= $i + 4 ?></span>
          <img src="<?= e(str_replace('-768x512', '-300x200', thumb($p['image']))) ?>" width="300" height="200" alt="<?= e($p['image_alt']) ?>" loading="lazy" decoding="async">
          <span class="ranked-body"><small><?= e(primary_cat($p)) ?> · <?= reading_time($p) ?> min</small><strong><?= e($p['title']) ?></strong></span>
        </a>
      </li>
      <?php endforeach; ?>
    </ol>
  </div>
</section>

<section class="band band-soft">
  <div class="wrap">
    <h2 class="section-title accent reveal">Quotes</h2>
    <div class="grid grid-4">
      <?php foreach (array_slice(posts_in('Quotes'), 0, 8) as $p) view('card', ['p' => $p]); ?>
    </div>
    <p class="center"><a href="/quotes/" class="btn btn-dark">See More Quotes</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2 class="section-title reveal">Mindsets</h2>
    <div class="grid grid-4">
      <?php foreach (array_slice(posts_in('Mindset'), 0, 12) as $p) view('card', ['p' => $p]); ?>
    </div>
    <p class="center"><a href="/mindset/" class="btn btn-accent">See More Mindset Tips</a></p>
  </div>
</section>

<section class="cta-band">
  <div class="cta-bg" aria-hidden="true"></div>
  <div class="wrap-narrow cta-inner reveal">
    <h2>Take the Thought Further</h2>
    <p>If something here sparked a question, reflection, or idea, we’d love to hear from you. And if you’re looking to spend more time with a theme or mindset, our guides are designed to help you go deeper, at your own pace.</p>
    <div class="hero-ctas">
      <a href="/contact-us/" class="btn btn-light">Contact Us</a>
      <a href="/blog/" class="btn btn-cyan">Explore More</a>
    </div>
  </div>
</section>

<section class="band band-soft">
  <div class="wrap">
    <?php view('products', ['products' => array_slice(bookshelf_items(), 0, 4), 'heading' => 'Books That Change How You Think', 'intro' => 'A few of the reads we return to most—each one a quiet nudge toward clearer thinking.']); ?>
    <p class="center"><a href="/recommended-reads/" class="btn btn-dark">Browse the Bookshelf</a></p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2 class="section-title reveal">All Articles</h2>
    <div class="grid grid-4">
      <?php foreach (array_slice(posts(), 0, 20) as $p) view('card', ['p' => $p]); ?>
    </div>
    <p class="center"><a href="/blog/" class="btn btn-accent">See More Articles</a></p>
  </div>
</section>
<?php view('foot'); ?>
