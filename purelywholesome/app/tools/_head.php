<?php /** @var array $tool @var string $slug */ ?>
<div class="tool__head">
  <span class="tool__icon"><?= icon($tool['icon']) ?></span>
  <div>
    <p class="tool__eyebrow">Free interactive tool</p>
    <h2 class="tool__name"><?= e($tool['name']) ?></h2>
    <p class="tool__short"><?= e($tool['short']) ?></p>
  </div>
</div>
