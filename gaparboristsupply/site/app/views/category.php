<?php
defined('GAP') || exit;
/** @var array $c */
$trail = cat_trail($c['path']);
$items = pick($c['products']);
$kids = array_map(fn($k) => $CAT['categories'][$k], $c['children']);
$brandsHere = [];
foreach ($items as $it) if ($it['brand_name'] ?? '') $brandsHere[$it['brand']] = $it['brand_name'];
asort($brandsHere);
$prices = array_column($items, 'price') ?: [0];
$meta = [
    'title' => $c['title'], 'desc' => $c['meta'], 'canonical' => $c['path'],
    'jsonld' => array_filter([
        ['@type' => 'CollectionPage', 'name' => $c['h1'], 'url' => abs_url($c['path']), 'description' => $c['meta'],
         'mainEntity' => ['@type' => 'ItemList', 'numberOfItems' => count($items),
            'itemListElement' => array_map(fn($p, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($p['path']), 'name' => $p['name']], array_slice($items, 0, 30), array_keys(array_slice($items, 0, 30)))]],
        crumbs_ld($trail), faq_ld($c['faq'] ?? []),
    ]),
    'body_class' => 'is-category',
];
$isDept = $c['parent'] === null;
?>
<section class="cat-hero<?= $isDept ? ' dept-hero' : '' ?><?= !empty($c['photo']) ? ' has-photo' : '' ?>">
  <?php if (!empty($c['photo'])): ?><div class="cat-hero-photo" aria-hidden="true"><img src="<?= e($c['photo']['src']) ?>" alt="" fetchpriority="high"></div><?php else: ?><div class="cat-hero-bg" aria-hidden="true"><img src="<?= kind_img($c['kind']) ?>" alt=""></div><?php endif; ?>
  <div class="wrap">
    <?= crumbs($trail) ?>
    <div class="cat-hero-row">
      <div>
        <h1><?= e($c['h1']) ?></h1>
        <p class="lede"><?= rich($c['intro']) ?></p>
      </div>
      <div class="cat-stat"><b><?= count($items) ?></b><span>products</span><b><?= count($brandsHere) ?></b><span>brands</span></div>
    </div>
<?php if ($kids): ?>
    <div class="subcats" role="list">
<?php foreach ($kids as $k): ?>
      <a role="listitem" class="subcat" href="<?= e($k['path']) ?>"><img src="<?= kind_img($k['kind']) ?>" alt="" width="40" height="40" loading="lazy"><span><?= e($k['name']) ?><small><?= count($k['products']) ?></small></span></a>
<?php endforeach; ?>
    </div>
<?php endif; ?>
  </div>
</section>

<section class="wrap listing" data-listing>
  <div class="toolbar">
    <label class="tb-field"><span>Brand</span>
      <select data-filter-brand><option value="">All brands</option><?php foreach ($brandsHere as $slug => $name): ?><option value="<?= e($slug) ?>"><?= e($name) ?></option><?php endforeach; ?></select>
    </label>
    <label class="tb-field tb-range"><span>Max price <output data-price-out><?= money(max($prices)) ?></output></span>
      <input type="range" min="<?= min($prices) ?>" max="<?= max($prices) ?>" value="<?= max($prices) ?>" step="1" data-filter-price>
    </label>
    <label class="tb-field"><span>Sort</span>
      <select data-sort><option value="">Most popular</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option><option value="name">Name A–Z</option></select>
    </label>
    <p class="tb-count" aria-live="polite"><span data-count><?= count($items) ?></span> shown</p>
  </div>
  <div class="grid products-grid" data-grid>
<?php foreach ($items as $p) echo product_card($p); ?>
  </div>
  <p class="empty-state" data-empty hidden>Nothing matches those filters. Try another brand or raise the price limit.</p>
  <div class="more-row"><button class="btn btn-outline" type="button" data-more hidden>Show more gear</button></div>
</section>

<?php if (!empty($c['guide']) || !empty($c['faq'])): ?>
<section class="section cat-guide">
  <div class="wrap guide-layout">
    <div class="prose reveal">
      <p class="eyebrow dark">Buying guide</p>
      <?= sections_block($c['guide'] ?? []) ?>
    </div>
    <div class="guide-side">
      <?= faq_block($c['faq'] ?? []) ?>
<?php foreach (TOOLS as $slug => $t) if (in_array($c['kind'], $t[3], true)): ?>
      <a class="aside-tool tilt" href="/tools/<?= $slug ?>/"><img src="<?= kind_img($t[2]) ?>" alt="" width="64" height="64"><span><small>Free tool</small><b><?= e($t[0]) ?></b><?= e($t[1]) ?></span></a>
<?php break; endif; ?>
    </div>
  </div>
</section>
<?php endif; ?>
