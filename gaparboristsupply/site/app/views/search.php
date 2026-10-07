<?php
defined('GAP') || exit;
/** @var string $q */
$results = search_catalog($q);
$cats = [];
if ($q !== '') foreach ($CAT['categories'] as $c) if (stripos($c['name'] . ' ' . $c['keyword'], $q) !== false) $cats[] = $c;
$meta = ['title' => $q !== '' ? 'Search results for "' . $q . '"' : 'Search the store', 'desc' => 'Search arborist gear, tree climbing equipment, rigging, saws and safety gear.', 'canonical' => '/search/', 'noindex' => true];
?>
<section class="cat-hero"><div class="wrap">
  <?= crumbs([['Search', '/search/']]) ?>
  <h1><?= $q !== '' ? 'Results for “' . e($q) . '”' : 'Search the store' ?></h1>
  <form class="search search-lg" action="/search/" method="get" role="search">
    <label class="sr" for="q2">Search</label>
    <input id="q2" name="q" type="search" value="<?= e($q) ?>" placeholder="Try “saddle”, “silky”, “rope”, “spark plug”" data-livesearch>
    <button type="submit" aria-label="Search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg></button>
    <div class="suggest" hidden></div>
  </form>
</div></section>
<section class="wrap listing">
<?php if ($cats): ?>
  <div class="subcats"><?php foreach (array_slice($cats, 0, 8) as $k): ?><a class="subcat" href="<?= e($k['path']) ?>"><img src="<?= kind_img($k['kind']) ?>" alt="" width="40" height="40"><span><?= e($k['name']) ?></span></a><?php endforeach; ?></div>
<?php endif; ?>
<?php if ($results): ?>
  <p class="tb-count"><?= count($results) ?> products</p>
  <div class="grid products-grid"><?php foreach ($results as $p) echo product_card($p); ?></div>
<?php elseif ($q !== ''): ?>
  <p class="empty-note">No products matched “<?= e($q) ?>”. Try a shorter word, a brand name, or browse <a href="/shop-all/">all gear</a>.</p>
<?php endif; ?>
</section>
