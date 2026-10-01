<?php
/** @var array|null $only list of slugs to show (default all)  @var string $headingLevel */
$only ??= null;
$headingLevel ??= 'h3';
$list = $only ? array_intersect_key(services(), array_flip($only)) : services();
?>
<ul class="card-grid service-grid" role="list">
  <?php foreach ($list as $slug => $s): ?>
  <li class="card service-card" data-reveal>
    <span class="card-icon"><?= icon($s['icon']) ?></span>
    <<?= $headingLevel ?> class="card-title"><a href="/services/<?= e($slug) ?>/" class="card-link"><?= e($s['name']) ?></a></<?= $headingLevel ?>>
    <p><?= e($s['card']) ?></p>
    <span class="card-more" aria-hidden="true">Learn more <?= icon('arrow', 'icon icon-sm') ?></span>
  </li>
  <?php endforeach; ?>
</ul>
