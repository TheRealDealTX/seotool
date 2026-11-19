<?php
defined('INC') || exit;
page_start([
    'title' => 'Shop Vintage-Inspired Finds: Curated Amazon Picks | Vintique Flea',
    'description' => 'Shop curated vintage-inspired finds: mid-century modern furniture, retro fashion, industrial salvage decor, rustic farmhouse pieces, vinyl gear and more.',
    'path' => '/shop/',
]);
$items = [];
$pos = 1;
foreach (SHOP as $slug => $c) {
    $items[] = ['@type' => 'ListItem', 'position' => $pos++, 'url' => abs_url("/shop/$slug/"), 'name' => $c['title']];
}
add_schema(['@type' => 'CollectionPage', 'name' => 'Shop Vintique Flea', 'url' => abs_url('/shop/'), 'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $items]]);
?>
<div class="wrap">
  <?= breadcrumbs([['Shop', '/shop/']]) ?>
  <header class="page-head">
    <h1>Shop curated vintage-inspired finds</h1>
    <p class="lede">The market only happens a few weekends a year, but the hunt never stops. We've hand-picked the pieces our shoppers love most, plus the tools to restore and display the originals you find at Vintique Flea.</p>
  </header>
</div>
<?php foreach (SHOP as $slug => $c): ?>
<section class="section section--tight">
  <div class="wrap">
    <div class="shop-row__head">
      <h2><span aria-hidden="true"><?= $c['icon'] ?></span> <a href="/shop/<?= $slug ?>/"><?= e($c['name']) ?></a></h2>
      <a class="link-more" href="/shop/<?= $slug ?>/">See all <?= e($c['name']) ?> <span aria-hidden="true">→</span></a>
    </div>
    <?= product_grid(array_slice($c['products'], 0, 4)) ?>
  </div>
</section>
<?php endforeach; ?>
<div class="wrap"><?= disclosure() ?></div>
<?php page_end();
