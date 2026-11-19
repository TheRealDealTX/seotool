<?php defined('SNW') || (http_response_code(404) && exit); ?>
<nav class="crumbs" aria-label="Breadcrumb"><ol>
  <li><a href="/">Home</a></li>
<?php foreach ($crumbs as $i => [$name, $href]): ?>
  <li><?php if ($i < count($crumbs) - 1): ?><a href="<?= e($href) ?>"><?= e($name) ?></a><?php else: ?><span aria-current="page"><?= e($name) ?></span><?php endif ?></li>
<?php endforeach ?>
</ol></nav>
