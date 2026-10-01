<?php
defined('FR_APP') || exit; // no direct web access (host ignores .htaccess)
/** @var array $a article  @var string $headingLevel */
$headingLevel ??= 'h3';
$hidden ??= false;
?>
<article class="card article-card" data-category="<?= e($a['category_slug']) ?>" data-reveal<?= $hidden ? ' hidden' : '' ?>>
  <div class="card-media"><?= photo($a['image'], '(min-width: 1100px) 360px, (min-width: 700px) 45vw, 100vw') ?></div>
  <div class="card-body">
    <p class="card-meta"><span class="tag"><?= e($a['category']) ?></span> <time datetime="<?= e($a['date']) ?>"><?= e(display_date($a['date'])) ?></time></p>
    <<?= $headingLevel ?> class="card-title"><a href="<?= e($a['url']) ?>" class="card-link"><?= e($a['title']) ?></a></<?= $headingLevel ?>>
    <p><?= e($a['excerpt']) ?></p>
    <span class="card-more" aria-hidden="true">Read article <?= icon('arrow', 'icon icon-sm') ?></span>
  </div>
</article>
