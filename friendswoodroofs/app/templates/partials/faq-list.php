<?php
/** @var array $items list of [question, answer]  @var string $headingLevel */
$headingLevel ??= 'h3';
?>
<div class="faq-list">
  <?php foreach ($items as [$q, $a]): ?>
  <details class="faq-item">
    <summary><<?= $headingLevel ?> class="faq-q"><?= e($q) ?></<?= $headingLevel ?>><?= icon('chevron', 'icon faq-icon') ?></summary>
    <div class="faq-a"><p><?= e($a) ?></p></div>
  </details>
  <?php endforeach; ?>
</div>
