<?php defined('HA_ROOT') || exit; ?>
<article class="post">
  <header class="post-hero">
    <div class="wrap narrow">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Houston Apartments</a><span>/</span><a href="/houston-apartments-blog/">Blog</a></nav>
      <h1 class="fade-up"><?= e($post['title']) ?></h1>
      <p class="post-meta fade-up d1"><img class="byline-avatar" src="<?= e(FOUNDER['avatar']) ?>" alt="" width="30" height="30">By <a href="/about-houston-apartments/#joseph-dittman"><?= e(FOUNDER['name']) ?></a>, Houston apartment locator · <time datetime="<?= e(substr($post['date'], 0, 10)) ?>"><?= date('F j, Y', strtotime($post['date'])) ?></time><?php if ($post['modified'] > $post['date']): ?> · Updated <?= date('F j, Y', strtotime($post['modified'])) ?><?php endif ?></p>
    </div>
    <?php if ($post['image']): ?>
      <div class="wrap post-cover fade-up d2"><img src="<?= e($post['image']) ?>" alt="<?= e($post['image_alt'] ?: $post['title']) ?>" width="1200" height="630" fetchpriority="high"></div>
    <?php endif ?>
  </header>
  <div class="wrap prose-grid">
    <div class="prose wp-content"><?= $post['content'] ?>
      <aside class="author-box">
        <img src="<?= e(FOUNDER['avatar']) ?>" alt="Joseph Dittman" width="84" height="84" loading="lazy">
        <div><h3>About the author: <?= e(FOUNDER['name']) ?></h3><p><?= e(FOUNDER['short']) ?> <a href="/about-houston-apartments/#joseph-dittman">More about Joseph</a>.</p></div>
      </aside>
    </div>
    <aside class="side-card sticky reveal d1">
      <h3>Find it on the map</h3>
      <p>Compare rents, floor plans and amenities across Houston with our draw-on-map search.</p>
      <a class="btn btn-grad btn-block" href="/apartments/">Search Houston apartments</a>
      <?php foreach ($featured as $c): ?>
        <a class="mini-card" href="<?= e($c['url']) ?>"><img src="<?= e($c['photos'][0] ?? '/assets/img/Houston-High-Rise.webp') ?>" alt="" loading="lazy" width="80" height="60"><span><strong><?= e($c['name']) ?></strong><small><?= e($c['price']) ?></small></span></a>
      <?php endforeach ?>
    </aside>
  </div>
</article>
<section class="section blog-strip">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="pill">Keep reading</span><h2>More from the Houston Apartments blog</h2></div></div>
    <div class="post-grid"><?php foreach ($related as $i => $post): require HA_APP . '/views/partials/post-card.php'; endforeach ?></div>
  </div>
</section>
