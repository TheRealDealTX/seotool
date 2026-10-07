<?php
defined('GAP') || exit;
$meta = ['title' => 'Shop All Arborist Gear', 'desc' => 'Browse every piece of arborist gear in the store. Filter tree climbing gear, rigging, saws, chainsaws and safety equipment by department, brand and price.', 'canonical' => '/shop-all/', 'body_class' => 'is-shop'];
$items = array_values($CAT['products']);
$depts = array_filter(array_map(fn($p) => $CAT['categories'][$p] ?? null, $CFG['departments']));
$brandsHere = [];
foreach ($items as $it) if ($it['brand_name'] ?? '') $brandsHere[$it['brand']] = $it['brand_name'];
asort($brandsHere);
$prices = array_column($items, 'price');
?>
<section class="cat-hero"><div class="wrap">
  <?= crumbs([['Shop all', '/shop-all/']]) ?>
  <div class="cat-hero-row"><div><h1>Shop all arborist gear</h1><p class="lede">Every product in the store in one place. Narrow it down by department, brand, budget and how you work.</p></div>
  <div class="cat-stat"><b><?= count($items) ?></b><span>products</span><b><?= count($brandsHere) ?></b><span>brands</span></div></div>
</div></section>
<section class="wrap listing shop-layout" data-listing>
  <aside class="facets">
    <div class="facet"><h2>Department</h2>
      <label class="radio"><input type="radio" name="dept" value="" checked data-filter-dept> All</label>
<?php foreach ($depts as $d): ?>
      <label class="radio"><input type="radio" name="dept" value="<?= e($d['path']) ?>" data-filter-dept> <?= e($d['name']) ?> <small><?= count($d['products']) ?></small></label>
<?php endforeach; ?>
    </div>
    <div class="facet"><h2>Used for</h2>
<?php foreach (['climbing' => 'Climbing', 'rigging' => 'Rigging', 'felling' => 'Felling & bucking', 'pruning' => 'Pruning', 'ground' => 'Ground work', 'bucket' => 'Bucket truck', 'safety' => 'Safety', 'maintenance' => 'Saw maintenance', 'apparel' => 'Apparel', 'plant-health' => 'Plant health'] as $v => $l): ?>
      <label class="check"><input type="checkbox" value="<?= $v ?>" data-filter-use> <?= $l ?></label>
<?php endforeach; ?>
    </div>
    <div class="facet"><h2>Level</h2>
      <label class="check"><input type="checkbox" value="pro" data-filter-level> Pro grade only</label>
    </div>
  </aside>
  <div>
    <div class="toolbar">
      <label class="tb-field"><span>Brand</span><select data-filter-brand><option value="">All brands</option><?php foreach ($brandsHere as $slug => $name): ?><option value="<?= e($slug) ?>"><?= e($name) ?></option><?php endforeach; ?></select></label>
      <label class="tb-field tb-range"><span>Max price <output data-price-out><?= money(max($prices)) ?></output></span><input type="range" min="0" max="<?= max($prices) ?>" value="<?= max($prices) ?>" step="5" data-filter-price></label>
      <label class="tb-field"><span>Sort</span><select data-sort><option value="">Most popular</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option><option value="name">Name A–Z</option></select></label>
      <p class="tb-count" aria-live="polite"><span data-count><?= count($items) ?></span> shown</p>
    </div>
    <div class="grid products-grid" data-grid>
<?php foreach ($items as $p): $dept = '/' . explode('/', trim($p['category'], '/'))[0] . '/'; ?>
      <?= str_replace('<article ', '<article data-dept="' . e($dept) . '" data-use="' . e(implode(' ', $p['use'] ?? [])) . '" data-level="' . e($p['level'] ?? 'all') . '" ', product_card($p)) ?>
<?php endforeach; ?>
    </div>
    <p class="empty-state" data-empty hidden>Nothing matches those filters.</p>
    <div class="more-row"><button class="btn btn-outline" type="button" data-more hidden>Show more gear</button></div>
  </div>
</section>
