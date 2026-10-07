<?php
defined('GAP') || exit;
$meta = ['title' => 'Free Arborist Calculators & Gear Tools', 'desc' => 'Free tools for tree work: climbing kit builder, rigging load calculator, rope length and tree height, 2-stroke fuel mix, spark plug decoder and chain file sizes.', 'canonical' => '/tools/'];
?>
<section class="cat-hero"><div class="wrap">
  <?= crumbs([['Tools', '/tools/']]) ?>
  <h1>Free tools for tree work</h1>
  <p class="lede">Quick calculators and finders for climbers, riggers and saw hands. They run in your browser and are free to use.</p>
</div></section>
<section class="wrap"><div class="tool-grid">
<?php foreach (TOOLS as $slug => [$name, $blurb, $kind]): ?>
  <a class="tool-card tilt reveal" href="/tools/<?= $slug ?>/"><img src="<?= kind_img($kind) ?>" alt="" width="72" height="72"><h2><?= e($name) ?></h2><p><?= e($blurb) ?></p><span class="link-arrow">Open tool</span></a>
<?php endforeach; ?>
</div></section>
