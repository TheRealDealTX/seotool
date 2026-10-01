<?php /** @var array $trail list of [label, path] */ ?>
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <div class="container">
    <ol>
      <?php foreach ($trail as $i => [$label, $path]): ?>
        <?php if ($i === count($trail) - 1): ?>
          <li><span aria-current="page"><?= e($label) ?></span></li>
        <?php else: ?>
          <li><a href="<?= e($path) ?>"><?= e($label) ?></a></li>
        <?php endif; ?>
      <?php endforeach; ?>
    </ol>
  </div>
</nav>
