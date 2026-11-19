<?php
defined('ERE') or exit;
$crumbs = [['Home', '/'], ['Recommended Gear', '/recommended-products/']];
$groups = [];
foreach (products() as $k => $p) $groups[$p[1]][] = $k;
page_head([
    'title' => 'Best Home Safety, Storm Prep & Homeowner Gear for Texas | ERE540',
    'description' => 'Our picks for Texas homeowners: hurricane and flood prep, leak detectors, smoke and CO alarms, fireproof safes, smart thermostats, moving supplies and real estate books.',
    'path' => '/recommended-products/',
    'crumbs' => $crumbs,
    'schema' => [[
        '@type' => 'ItemList', 'name' => 'Recommended homeowner gear',
        'itemListElement' => array_map(fn($k, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'name' => products()[$k][0]], array_keys(products()), range(0, count(products()) - 1)),
    ]],
]);
?>
<section class="page-head">
  <div class="wrap">
    <?php breadcrumbs($crumbs); ?>
    <h1>Recommended Gear for Texas Homeowners</h1>
    <p class="lead">The tools and supplies we would want in our own homes - chosen for Gulf Coast weather, Texas heat and the realities of buying, owning and protecting property.</p>
    <p class="disclosure">As an Amazon Associate we earn from qualifying purchases. Links go to Amazon search results so you always see current listings, sellers and prices. <a href="/affiliate-disclosure/">Affiliate disclosure</a>.</p>
    <div class="chips">
<?php foreach (cfg('product_groups') as $g => [$name]): ?>
      <a class="chip" href="#<?= e($g) ?>"><?= e($name) ?></a>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php foreach (cfg('product_groups') as $g => [$name, $desc]): if (empty($groups[$g])) continue; ?>
<section class="section section--compact" id="<?= e($g) ?>">
  <div class="wrap">
    <div class="section__head"><div><h2><?= e($name) ?></h2><p><?= e($desc) ?></p></div></div>
    <div class="products">
<?php foreach ($groups[$g] as $k) echo product_card($k); ?>
    </div>
  </div>
</section>
<?php endforeach;
page_foot();
