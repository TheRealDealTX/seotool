<?php $crumbs = breadcrumbs_for($page); if ($crumbs): ?>
<nav class="breadcrumbs" aria-label="Breadcrumb">
  <ol>
    <?php foreach ($crumbs as $i => [$name, $path]): $last = $i === count($crumbs) - 1; ?>
    <li><?php if ($last): ?><span aria-current="page"><?= e($name) ?></span><?php else: ?><a href="<?= e($path) ?>"><?= e($name) ?></a><?php endif; ?></li>
    <?php endforeach; ?>
  </ol>
</nav>
<?php endif; ?>
