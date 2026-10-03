<?php /** @var array $post */ ?>
<article class="post-card reveal">
  <a class="post-card-media" href="<?= e($post['path']) ?>" tabindex="-1" aria-hidden="true">
    <?= img($post['image'] ?? '/wp-content/uploads/2026/02/McAllen-Public-Adjuster-Site-Image.webp', '', ['sizes' => '(max-width: 700px) 100vw, 400px']) ?>
  </a>
  <div class="post-card-body">
    <p class="post-card-meta"><span><?= e($post['category'] ?? 'Insurance Claims') ?></span> <time datetime="<?= e(iso_date($post['date'])) ?>"><?= e(format_date($post['date'], 'M j, Y')) ?></time></p>
    <h3 class="post-card-title"><a href="<?= e($post['path']) ?>"><?= e($post['title']) ?></a></h3>
    <p><?= e($post['excerpt'] ?? $post['description'] ?? '') ?></p>
    <a class="post-card-more" href="<?= e($post['path']) ?>" aria-label="Read: <?= e($post['title']) ?>">Read article <?= icon('arrow', 'icon icon-sm') ?></a>
  </div>
</article>
