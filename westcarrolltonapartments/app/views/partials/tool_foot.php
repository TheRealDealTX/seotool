<?php defined('WCA') || exit; ?>
<section class="wrap section-tight">
  <h2>More free tools</h2>
  <div class="tool-grid small">
    <?php foreach ($tools as $s => [$n, $d, $i]): if ($s === $slug) continue; ?>
      <a class="tool-card" href="/tools/<?= $s ?>/"><span><?= $i ?></span><h3><?= e($n) ?></h3></a>
    <?php endforeach; ?>
  </div>
  <?php if (!empty($products)) partial('partials/products', ['products' => $products, 'heading' => $productsHeading ?? 'Handy for your move']); ?>
</section>
<script>window.WCA_LISTINGS = <?= json_encode(array_map('listing_public_json', $all), JSON_HEX_TAG | JSON_UNESCAPED_SLASHES) ?>;</script>
