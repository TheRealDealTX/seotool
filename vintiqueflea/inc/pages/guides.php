<?php
defined('INC') || exit;
/** @var array $guides */
page_start([
    'title' => 'Vintage Shopping & Decorating Guides | Vintique Flea',
    'description' => 'Guides for vintage lovers: Houston vintage shopping, flea market tips, spotting mid-century modern furniture and decorating with salvage.',
    'path' => '/guides/',
]);
$byCat = [];
foreach ($guides as $s => $g) {
    $byCat[$g['category']][$s] = $g;
}
ksort($byCat);
?>
<div class="wrap">
  <?= breadcrumbs([['Guides', '/guides/']]) ?>
  <header class="page-head">
    <h1>Guides for vintage lovers</h1>
    <p class="lede">Where to shop vintage in Houston, how to spot real mid-century modern, how to haggle like a pro, and how to make old things look right at home.</p>
  </header>
<?php foreach ($byCat as $cat => $list): ?>
  <section class="section section--tight">
    <h2><?= e($cat) ?></h2>
    <div class="guide-grid">
<?php foreach ($list as $s => $g): ?>
      <a class="guide-card" href="/guides/<?= $s ?>/">
        <?= photo('g-' . $s, '', 'guide-card__img', false, '(max-width: 640px) 100vw, 380px') ?>
        <span class="guide-card__cat"><?= (int) $g['read_minutes'] ?> min read</span>
        <span class="guide-card__title"><?= e($g['h1']) ?></span>
        <span class="guide-card__intro"><?= e($g['intro']) ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </section>
<?php endforeach; ?>
</div>
<?php page_end();
