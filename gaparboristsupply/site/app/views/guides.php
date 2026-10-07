<?php
defined('GAP') || exit;
$meta = ['title' => 'Arborist Gear Buying Guides', 'desc' => 'Practical buying guides for tree climbing gear, arborist rope, Silky saws, Husqvarna chainsaws, chainsaw chaps and spark plugs, written for working arborists.', 'canonical' => '/guides/'];
?>
<section class="cat-hero"><div class="wrap">
  <?= crumbs([['Guides', '/guides/']]) ?>
  <h1>Buying guides</h1>
  <p class="lede">Straight answers to the questions climbers and crews ask before they spend money on gear.</p>
</div></section>
<section class="wrap"><div class="guide-grid">
<?php foreach ($CAT['guides'] as $g): ?>
  <a class="guide-card tilt reveal" href="<?= e($g['path']) ?>"><span class="guide-art<?= !empty($g['photo']) ? ' has-photo' : '' ?>"><?= !empty($g['photo']) ? photo_img($g['photo'], $g['kind'], '', '(max-width: 700px) 100vw, 400px') : '<img src="' . kind_img($g['kind']) . '" alt="" loading="lazy">' ?></span><span class="guide-meta"><?= (int)$g['read_minutes'] ?> min read</span><h2><?= e($g['h1']) ?></h2><p><?= e($g['dek']) ?></p></a>
<?php endforeach; ?>
</div></section>
