<?php defined('WCA') || exit; ?>
<article class="wrap post">
  <header class="post-head narrow">
    <p class="eyebrow"><a href="/blog/category/<?= category_slug($p['category']) ?>/"><?= e($p['category']) ?></a></p>
    <h1><?= e($p['title']) ?></h1>
    <p class="muted small">By the West Carrollton Apartments team · <time datetime="<?= e($p['updated'] ?? $p['date']) ?>">Updated <?= e(date('F j, Y', strtotime($p['updated'] ?? $p['date']))) ?></time></p>
  </header>
  <img class="post-hero" src="<?= e(photo_url($p['image'])) ?>" alt="" width="1200" height="800" fetchpriority="high">
  <div class="post-layout">
    <div class="prose">
      <?= post_body_html($p) ?>
      <?php if (!empty($p['faq'])): ?>
      <section class="faq">
        <h2>Frequently asked questions</h2>
        <?php foreach ($p['faq'] as $f): ?><details><summary><?= e($f['q']) ?></summary><p><?= e($f['a']) ?></p></details><?php endforeach; ?>
      </section>
      <?php endif; ?>
    </div>
    <aside class="post-side">
      <div class="card sticky">
        <h3 class="h5">Looking for an apartment?</h3>
        <p class="small">Compare every community in West Carrollton, OH with rents, pets and amenities.</p>
        <a class="btn btn-block" href="/apartments/">Browse apartments</a>
        <a class="btn btn-ghost btn-block" href="/tools/apartment-match-quiz/">Take the match quiz</a>
      </div>
    </aside>
  </div>
  <?php if ($related): ?>
  <section class="section-tight">
    <h2>Keep reading</h2>
    <div class="card-grid">
      <?php foreach ($related as $r): ?>
      <article class="card post-card">
        <a class="card-img" href="/blog/<?= e($r['slug']) ?>/"><img src="<?= e(photo_url($r['image'], true)) ?>" alt="" loading="lazy" width="640" height="427"></a>
        <div class="card-body"><p class="eyebrow"><?= e($r['category']) ?></p><h3><a href="/blog/<?= e($r['slug']) ?>/"><?= e($r['title']) ?></a></h3></div>
      </article>
      <?php endforeach; ?>
    </div>
  </section>
  <?php endif; ?>
</article>
