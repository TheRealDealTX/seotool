<?php /** @var array $p */ $eager = $eager ?? false; ?>
<article class="card reveal">
  <a href="/<?= e($p['slug']) ?>/" class="card-link">
    <div class="card-media">
      <img src="<?= e(thumb($p['image'])) ?>" srcset="<?= e(img_srcset($p['image'])) ?>" sizes="(max-width: 640px) 100vw, (max-width: 1100px) 50vw, 300px" width="768" height="512" alt="<?= e($p['image_alt']) ?>" <?= $eager ? '' : 'loading="lazy" ' ?>decoding="async">
      <span class="card-tag"><?= e(primary_cat($p)) ?></span>
    </div>
    <div class="card-body">
      <h3 class="card-title"><?= e($p['title']) ?></h3>
      <p class="card-meta"><?= reading_time($p) ?> min read</p>
    </div>
  </a>
</article>
