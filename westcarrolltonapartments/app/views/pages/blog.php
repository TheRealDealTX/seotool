<?php defined('WCA') || exit; ?>
<section class="page-head"><div class="wrap">
  <h1><?= $cat ? e($cat) . ' for West Carrollton Renters' : 'The West Carrollton Renter Blog' ?></h1>
  <p class="lead">Practical, local advice for renting in West Carrollton and the Dayton area: lease checklists, Ohio tenant rights, budgeting, moving and making a small space feel like home.</p>
  <div class="quick-links small-links">
    <a href="/blog/" class="<?= $cat ? '' : 'active' ?>">All</a>
    <?php foreach (post_categories() as $s => $n): ?><a href="/blog/category/<?= $s ?>/" class="<?= $cat === $n ? 'active' : '' ?>"><?= e($n) ?></a><?php endforeach; ?>
  </div>
</div></section>
<div class="wrap section-tight">
  <div class="card-grid">
    <?php foreach ($posts as $p): ?>
    <article class="card post-card">
      <a class="card-img" href="/blog/<?= e($p['slug']) ?>/"><img src="<?= e(photo_url($p['image'], true)) ?>" alt="" loading="lazy" width="640" height="427"></a>
      <div class="card-body">
        <p class="eyebrow"><a href="/blog/category/<?= category_slug($p['category']) ?>/"><?= e($p['category']) ?></a></p>
        <h2 class="h3"><a href="/blog/<?= e($p['slug']) ?>/"><?= e($p['title']) ?></a></h2>
        <p class="muted"><?= e($p['excerpt']) ?></p>
      </div>
    </article>
    <?php endforeach; ?>
  </div>
</div>
