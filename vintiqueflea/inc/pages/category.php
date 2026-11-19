<?php
defined('INC') || exit;
/** @var string $slug @var array $cat */
page_start([
    'title' => $cat['seo_title'],
    'description' => $cat['description'],
    'path' => "/shop/$slug/",
    'body_class' => 'cat-page cat-page--' . $cat['color'],
    'image' => $slug,
]);
$items = [];
foreach ($cat['products'] as $i => $p) {
    $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $p['name'], 'url' => amazon_url($p)];
}
add_schema(['@type' => 'CollectionPage', 'name' => $cat['title'], 'description' => $cat['description'], 'url' => abs_url("/shop/$slug/"), 'mainEntity' => ['@type' => 'ItemList', 'numberOfItems' => count($items), 'itemListElement' => $items]]);
$guides = array_filter(load_guides(), fn($g) => in_array($slug, $g['shop'] ?? [], true));
?>
<div class="wrap">
  <?= breadcrumbs([['Shop', '/shop/'], [$cat['name'], "/shop/$slug/"]]) ?>
  <header class="page-head page-hero">
    <div class="page-hero__copy">
      <p class="eyebrow"><span aria-hidden="true"><?= $cat['icon'] ?></span> Shop <?= e($cat['name']) ?></p>
      <h1><?= e($cat['title']) ?></h1>
      <p class="lede"><?= e($cat['intro']) ?></p>
    </div>
    <div class="page-hero__img"><?= photo($slug, $cat['title'], '', true, '(max-width: 900px) 100vw, 520px') ?></div>
  </header>
  <?= product_grid($cat['products'], $slug) ?>
  <?= disclosure() ?>
  <div class="layout-2">
    <article class="prose"><?= $cat['body'] ?></article>
    <aside class="side">
      <div class="side-card">
        <h2>Find the originals</h2>
        <p>Vintage and one-of-a-kind <?= e(strtolower($cat['name'])) ?> pieces turn up at every Vintique Flea at Silver Street Studios.</p>
        <a class="btn btn--primary btn--block" href="/events/">Next market dates</a>
      </div>
<?php if ($guides): ?>
      <div class="side-card">
        <h2>Related guides</h2>
        <ul class="side-links">
<?php foreach ($guides as $gs => $g): ?>
          <li><a href="/guides/<?= $gs ?>/"><?= e($g['h1']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
<?php endif; ?>
      <div class="side-card">
        <h2>More to explore</h2>
        <ul class="side-links">
<?php foreach (SHOP as $s => $c): if ($s === $slug) continue; ?>
          <li><a href="/shop/<?= $s ?>/"><?= $c['icon'] ?> <?= e($c['name']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
    </aside>
  </div>
</div>
<?php page_end();
