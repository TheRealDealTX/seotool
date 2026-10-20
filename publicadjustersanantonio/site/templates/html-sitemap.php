<?php
component('page-hero', ['page' => $page]);
$groups = ['Pages' => all_content('pages'), 'Claim Services' => all_content('services'), 'Articles' => all_content('posts')];
?>
<section class="section"><div class="container">
  <div class="card-grid card-grid-3">
  <?php foreach ($groups as $label => $items): ?>
    <div class="sidebar-card"><h2 class="h3" style="font-size:1.2rem"><?= e($label) ?></h2><ul class="link-list">
      <?php foreach ($items as $it): if (!empty($it['noindex'])) continue; ?><li><a href="<?= e($it['path']) ?>"><?= e($it['title']) ?></a></li><?php endforeach; ?>
    </ul></div>
  <?php endforeach; ?>
  </div>
</div></section>
