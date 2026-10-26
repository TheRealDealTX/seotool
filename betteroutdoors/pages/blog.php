<?php defined('BO') || exit;
// Blog index: every post, with live search and category filters.
$crumbs = [['Home', '/'], ['Blog', '/blog/']];
$items = [];
$i = 1;
foreach ($POSTS as $s => $p) $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => SITE_URL . '/' . $s . '/', 'name' => $p['h1']];
$cats = array_values(array_unique(array_column($POSTS, 'cat')));
page_head([
    'title' => 'Better Outdoors Blog: Compound Bow Reviews & Archery Guides',
    'desc'  => 'The Better Outdoors blog: compound bow reviews for Mathews, Bear Archery and PSE, plus bow tuning guides, draw length help and ready-to-hunt package advice.',
    'path'  => '/blog/',
    'schema' => [breadcrumb_schema($crumbs), ['@type' => 'CollectionPage', 'name' => 'Better Outdoors Blog', 'url' => SITE_URL . '/blog/', 'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $items]]],
]);
?>
<section class="page-hero mist-after">
  <div class="wrap">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>The Better Outdoors Blog</h1>
    <p>Honest compound bow reviews, step-by-step tuning guides and practical bowhunting advice. Search or filter to find what you need.</p>
  </div>
</section>
<section class="section-mist" style="padding:10px 0 90px">
  <div class="wrap">
    <div class="filter-bar">
      <div class="chips" role="group" aria-label="Filter by category">
        <button type="button" class="on" data-cat="all">All</button>
<?php foreach ($cats as $c): ?>
        <button type="button" data-cat="<?= e($c) ?>"><?= e($c) ?></button>
<?php endforeach; ?>
      </div>
      <label class="filter-search"><i class="fa-solid fa-magnifying-glass" aria-hidden="true"></i><input type="search" id="filter-q" placeholder="Search guides…" aria-label="Search guides"></label>
    </div>
    <div class="post-grid" data-filter-grid>
<?php $first = true; foreach ($POSTS as $s => $p) { echo post_card($s, $p, !$first); $first = false; } ?>
    </div>
    <p class="no-results" hidden>No guides match that search yet. Try &ldquo;Bear&rdquo;, &ldquo;Mathews&rdquo; or &ldquo;draw length&rdquo;.</p>
  </div>
</section>
<?php page_foot(); ?>
