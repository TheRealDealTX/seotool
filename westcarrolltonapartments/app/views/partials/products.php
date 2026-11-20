<?php defined('WCA') || exit; /** @var array $products */ ?>
<aside class="products" aria-label="Recommended products">
  <h3><?= e($heading ?? 'Recommended products') ?></h3>
  <div class="product-grid">
  <?php foreach ($products as $p): ?>
    <a class="product" href="<?= e(amazon_url($p['query'])) ?>" target="_blank" rel="nofollow sponsored noopener">
      <span class="product-icon" aria-hidden="true"><?= e($p['icon'] ?? '🛒') ?></span>
      <span class="product-name"><?= e($p['name']) ?></span>
      <?php if (!empty($p['why'])): ?><span class="product-why"><?= e($p['why']) ?></span><?php endif; ?>
      <span class="product-cta">View on Amazon →</span>
    </a>
  <?php endforeach; ?>
  </div>
  <p class="small muted">As an Amazon Associate we earn from qualifying purchases. Prices and availability are shown on Amazon.</p>
</aside>
