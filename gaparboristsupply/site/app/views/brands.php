<?php
defined('GAP') || exit;
$meta = ['title' => 'Arborist Gear Brands A–Z', 'desc' => 'Every arborist gear brand we carry, from Petzl, Buckingham and Weaver to Husqvarna, Silky, Teufelberger and Yale Cordage. Browse tree gear by brand.', 'canonical' => '/brands/'];
$all = $CAT['brands'];
uasort($all, fn($a, $b) => strcasecmp($a['name'], $b['name']));
$groups = [];
foreach ($all as $b) $groups[ctype_alpha($b['name'][0]) ? strtoupper($b['name'][0]) : '#'][] = $b;
?>
<section class="cat-hero"><div class="wrap">
  <?= crumbs([['Brands', '/brands/']]) ?>
  <h1>Arborist gear brands</h1>
  <p class="lede">The makers tree crews trust, from climbing hardware specialists to the saw and power equipment names on every jobsite.</p>
  <nav class="az" aria-label="Jump to letter"><?php foreach (array_keys($groups) as $L): ?><a href="#b-<?= $L === '#' ? 'num' : $L ?>"><?= $L ?></a><?php endforeach; ?></nav>
</div></section>
<section class="wrap brand-index">
<?php foreach ($groups as $L => $list): ?>
  <div class="az-group reveal" id="b-<?= $L === '#' ? 'num' : $L ?>"><h2><?= $L ?></h2>
    <div class="brand-tiles"><?php foreach ($list as $b): ?><a class="brand-tile tilt" href="<?= e($b['path']) ?>"><b><?= e($b['name']) ?></b><span><?= count($b['products']) ? count($b['products']) . ' products' : 'Brand profile' ?></span></a><?php endforeach; ?></div>
  </div>
<?php endforeach; ?>
</section>
