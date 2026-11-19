<?php /** @var array $products */ $heading = $heading ?? 'Recommended Reading'; $showFrom = $showFrom ?? false; if (!$products) return; ?>
<aside class="products reveal" aria-label="<?= e($heading) ?>">
  <div class="products-head">
    <span class="eyebrow">From the Bookshelf</span>
    <h3><?= e($heading) ?></h3>
    <p><?= e($intro ?? 'If this topic resonated with you, these go deeper:') ?></p>
  </div>
  <div class="product-grid">
  <?php foreach ($products as $i => $pr): $hue = (crc32($pr['title']) % 360); ?>
    <div class="product-wrap">
    <a class="product" href="<?= e(amazon_url($pr)) ?>" rel="sponsored nofollow noopener" target="_blank" data-amz="<?= e($pr['title']) ?>">
      <span class="book" style="--h:<?= $hue ?>" aria-hidden="true"><span class="book-title"><?= e($pr['title']) ?></span><?php if (!empty($pr['by'])): ?><span class="book-by"><?= e($pr['by']) ?></span><?php endif; ?></span>
      <span class="product-info">
        <strong><?= e($pr['title']) ?></strong>
        <?php if (!empty($pr['by'])): ?><span class="by">by <?= e($pr['by']) ?></span><?php endif; ?>
        <span class="blurb"><?= e($pr['blurb'] ?? '') ?></span>
        <span class="amz-btn">View on Amazon <svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M14 3h7v7h-2V6.4l-9.3 9.3-1.4-1.4L17.6 5H14V3ZM5 5h6v2H5v12h12v-6h2v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2Z"/></svg></span>
      </span>
    </a>
    <?php if ($showFrom && !empty($pr['from'])): $src = post_by_slug($pr['from'][0]); ?>
      <p class="product-from">Recommended in <a href="/<?= e($src['slug']) ?>/"><?= e($src['title']) ?></a><?= count($pr['from']) > 1 ? ' +' . (count($pr['from']) - 1) . ' more' : '' ?></p>
    <?php endif; ?>
    </div>
  <?php endforeach; ?>
  </div>
  <p class="disclosure"><em>As an Amazon Associate, Thought Changer earns from qualifying purchases. If you buy through these links, we may earn a small commission at no extra cost to you.</em></p>
</aside>
