<?php defined('WCA') || exit; ?>
<section class="page-head"><div class="wrap">
  <h1>Free interactive tools for renters</h1>
  <p class="lead">Budget, plan and play before you sign a lease. Everything runs in your browser, nothing you type is sent to us.</p>
</div></section>
<div class="wrap section-tight">
  <div class="tool-grid">
    <?php foreach ($tools as $slug => [$name, $desc, $icon]): ?>
      <a class="tool-card" href="/tools/<?= $slug ?>/"><span><?= $icon ?></span><h2 class="h3"><?= e($name) ?></h2><p><?= e($desc) ?></p></a>
    <?php endforeach; ?>
  </div>
</div>
