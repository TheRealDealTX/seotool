<?php
defined('GAP') || exit;
/** @var array $b */
$trail = [['Brands', '/brands/'], [$b['name'], $b['path']]];
$items = pick($b['products']);
$meta = [
    'title' => $b['title'], 'desc' => $b['meta'], 'canonical' => $b['path'],
    'jsonld' => [['@type' => 'CollectionPage', 'name' => $b['name'] . ' gear', 'url' => abs_url($b['path']), 'about' => ['@type' => 'Brand', 'name' => $b['name']]], crumbs_ld($trail)],
];
?>
<section class="cat-hero brand-hero">
  <div class="wrap">
    <?= crumbs($trail) ?>
    <div class="cat-hero-row">
      <div>
        <p class="eyebrow">Brand</p>
        <h1><?= e($b['name']) ?></h1>
        <p class="lede"><?= rich($b['intro']) ?></p>
      </div>
      <div class="brand-mark" aria-hidden="true"><?= e(mb_substr($b['name'], 0, 1)) ?></div>
    </div>
<?php if (!empty($b['known_for'])): ?>
    <ul class="known-for"><?php foreach ($b['known_for'] as $k): ?><li><?= e($k) ?></li><?php endforeach; ?></ul>
<?php endif; ?>
  </div>
</section>
<?php if ($items): ?>
<section class="wrap listing" data-listing>
  <div class="toolbar">
    <label class="tb-field"><span>Sort</span><select data-sort><option value="">Most popular</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option><option value="name">Name A–Z</option></select></label>
    <p class="tb-count"><span data-count><?= count($items) ?></span> products</p>
  </div>
  <div class="grid products-grid" data-grid><?php foreach ($items as $p) echo product_card($p); ?></div>
  <div class="more-row"><button class="btn btn-outline" type="button" data-more hidden>Show more gear</button></div>
</section>
<?php else: ?>
<section class="wrap"><p class="empty-note">We're still adding <?= e($b['name']) ?> gear to the store. In the meantime, browse <a href="/shop-all/">all gear</a> or search above.</p></section>
<?php endif; ?>
<section class="section"><div class="wrap narrow prose reveal">
  <h2>About <?= e($b['name']) ?></h2>
<?php foreach ($b['about'] ?? [] as $para): ?>
  <p><?= rich($para) ?></p>
<?php endforeach; ?>
</div></section>
