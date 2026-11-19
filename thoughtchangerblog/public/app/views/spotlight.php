<?php /** @var array $pr */ $hue = (crc32($pr['title']) % 360); ?>
<aside class="spotlight reveal" aria-label="Reader pick">
  <span class="book book-sm" style="--h:<?= $hue ?>" aria-hidden="true"><span class="book-title"><?= e($pr['title']) ?></span></span>
  <div>
    <span class="eyebrow">Reader pick</span>
    <p><strong><?= e($pr['title']) ?></strong><?php if (!empty($pr['by'])): ?> by <?= e($pr['by']) ?><?php endif; ?> — <?= e($pr['blurb'] ?? '') ?></p>
    <a class="amz-link" href="<?= e(amazon_url($pr)) ?>" rel="sponsored nofollow noopener" target="_blank" data-amz="<?= e($pr['title']) ?>">Check it out on Amazon →</a>
  </div>
</aside>
