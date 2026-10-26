<?php
$posts = all_posts();
$cats = [];
foreach ($posts as $p) {
    $c = $p['category'] ?? 'Guides';
    $cats[category_slug($c)] = [$c, ($cats[category_slug($c)][1] ?? 0) + 1];
}
$meta = [
    'title' => 'Side Hustle Blog: Guides, Ideas & City Side Jobs | ' . SITE_NAME,
    'description' => 'Every Better Side Hustles guide in one place: side hustle ideas, platform how-tos and the best side jobs in ' . count(array_filter($posts, fn($p) => ($p['category'] ?? '') === 'City Guides')) . ' US cities. Search or filter by topic.',
    'url' => '/blog/',
    'schema' => [
        ['@type' => 'CollectionPage', 'name' => 'Side Hustle Blog', 'url' => SITE_URL . '/blog/', 'isPartOf' => ['@id' => SITE_URL . '/#website'],
         'mainEntity' => ['@type' => 'ItemList', 'numberOfItems' => count($posts), 'itemListElement' => array_map(fn($p, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($p['url'])], $posts, array_keys($posts))]],
        schema_breadcrumbs([['Home', '/'], ['Blog', '/blog/']]),
    ],
];
require __DIR__ . '/header.php';
?>
<section class="page-hero">
  <canvas class="coin-canvas" data-density="0.35" aria-hidden="true"></canvas>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Blog</nav>
    <span class="pill">The Better Side Hustles blog</span>
    <h1>Side hustle guides, ideas and city side jobs</h1>
    <p class="dek"><?= count($posts) ?> practical guides on making extra money — from phone side hustles and digital marketing to the best side hustles in your city.</p>
  </div>
</section>
<section class="section" style="padding-top:48px">
  <div class="wrap">
    <div class="filter-bar">
      <div class="chips" role="group" aria-label="Filter by topic">
        <button type="button" data-filter-cat="all" class="active">All</button>
        <?php foreach ($cats as $slug => [$name, $n]): ?>
        <button type="button" data-filter-cat="<?= e($slug) ?>"><?= e($name) ?> (<?= $n ?>)</button>
        <?php endforeach; ?>
      </div>
      <label class="blog-search"><?= icon('search') ?><input type="search" data-filter-search placeholder="Search guides or cities" aria-label="Search guides"></label>
    </div>
    <p class="count-note">Showing <span data-filter-count><?= count($posts) ?></span> guides</p>
    <div class="grid grid-3" data-filter-grid>
      <?php foreach ($posts as $i => $p) echo post_card($p, $i > 5); ?>
    </div>
    <div class="empty" data-filter-empty hidden><p>No guides match that search yet. Try a nearby city or <a href="/tools/side-hustle-quiz/">take the quiz</a>.</p></div>
  </div>
</section>
<?php require __DIR__ . '/footer.php'; ?>
