<?php
defined('INC') || exit;
page_start(['title' => 'Photo Credits | Vintique Flea', 'description' => 'Credits and licenses for the photographs used on vintiqueflea.com.', 'path' => '/photo-credits/']);
$labels = ['cc0' => 'CC0 1.0 (public domain dedication)', 'pdm' => 'Public Domain Mark'];
?>
<div class="wrap narrow">
  <?= breadcrumbs([['Photo Credits', '/photo-credits/']]) ?>
  <article class="prose">
    <h1>Photo credits</h1>
    <p>The photographs on this site are free-to-use images released into the public domain (CC0) or marked as public domain, found through <a href="https://openverse.org/" rel="noopener">Openverse</a>. Attribution isn't required, but we like to thank the photographers.</p>
    <ul>
<?php foreach (PHOTOS as $name => [$w, $h, $title, $creator, $license, $source, $landing]): ?>
      <li><a href="<?= e($landing) ?>" rel="noopener nofollow"><?= e($title ?: $name) ?></a><?= $creator ? ' by ' . e($creator) : '' ?>, via <?= e(ucfirst($source)) ?>, <?= e($labels[$license] ?? strtoupper($license)) ?></li>
<?php endforeach; ?>
    </ul>
  </article>
</div>
<?php page_end();
