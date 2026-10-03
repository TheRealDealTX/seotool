<?php
$isPost = ($page['_type'] ?? '') === 'post';
$heroImg = $page['hero_image'] ?? $page['image'] ?? '/wp-content/uploads/2026/02/League-City-Public-Adjuster-BG.webp';
?>
<section class="page-hero<?= !empty($page['hero_compact']) ? ' page-hero-compact' : '' ?>">
  <div class="page-hero-bg" aria-hidden="true" data-parallax>
    <?= img($heroImg, '', ['eager' => true, 'sizes' => '100vw', 'class' => 'page-hero-img']) ?>
  </div>
  <div class="container page-hero-inner">
    <?php component('breadcrumbs', ['page' => $page]); ?>
    <?php if (!empty($page['kicker'])): ?><p class="eyebrow eyebrow-gold"><?= e($page['kicker']) ?></p><?php elseif ($isPost && !empty($page['category'])): ?><p class="eyebrow eyebrow-gold"><?= e($page['category']) ?></p><?php endif; ?>
    <h1><?= e($page['h1'] ?? $page['title']) ?></h1>
    <?php if (!empty($page['lead'])): ?><p class="page-hero-lead"><?= e($page['lead']) ?></p><?php endif; ?>
    <?php if ($isPost): ?>
    <div class="post-meta">
      <img src="/assets/img/joseph-dittman.webp" alt="" width="40" height="40">
      <div>
        <span class="post-meta-author">By <a href="/author/joseph-dittman/">Joseph Dittman</a>, Public Adjuster</span>
        <span class="post-meta-dates">Published <time datetime="<?= e(iso_date($page['date'])) ?>"><?= e(format_date($page['date'])) ?></time><?php if (!empty($page['updated']) && $page['updated'] !== $page['date']): ?> &middot; Updated <time datetime="<?= e(iso_date($page['updated'])) ?>"><?= e(format_date($page['updated'])) ?></time><?php endif; ?> &middot; <?= reading_minutes($page['body'] ?? '') ?> min read</span>
      </div>
    </div>
    <?php elseif (empty($page['hide_hero_cta'])): ?>
    <div class="hero-actions">
      <a class="btn btn-gold" href="/free-claim-review/">Get a Free Claim Review</a>
      <a class="btn btn-outline-light" href="<?= e(tel_link()) ?>"><?= icon('phone', 'icon icon-sm') ?> Call <?= e(cfg('phone_short')) ?></a>
    </div>
    <?php endif; ?>
  </div>
</section>
