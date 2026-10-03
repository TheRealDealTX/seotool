<?php $limit = $limit ?? 0; $cards = service_cards(); if ($limit) { $cards = array_slice($cards, 0, $limit); } ?>
<div class="card-grid card-grid-services">
  <?php foreach ($cards as $i => [$href, $label, $ic, $blurb]): ?>
  <a class="service-card reveal" style="--d:<?= ($i % 4) * 60 ?>ms" href="<?= e($href) ?>">
    <span class="service-card-icon"><?= icon($ic, 'icon') ?></span>
    <span class="service-card-title"><?= e($label) ?></span>
    <span class="service-card-text"><?= e($blurb) ?></span>
    <span class="service-card-more">Learn more <?= icon('arrow', 'icon icon-sm') ?></span>
  </a>
  <?php endforeach; ?>
</div>
