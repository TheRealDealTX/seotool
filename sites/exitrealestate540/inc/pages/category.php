<?php
defined('ERE') or exit;
$posts = array_values(posts_in($cat['slug']));
$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$cat['name'], $cat['url']]];
$relTools = [];
foreach ($posts as $p) foreach ($p['tools'] ?? [] as $t) $relTools[$t] = true;
page_head([
    'title' => $cat['title'] . ' | Exit Real Estate 540',
    'description' => $cat['description'],
    'path' => $cat['url'],
    'crumbs' => $crumbs,
    'schema' => [[
        '@type' => 'CollectionPage', 'url' => abs_url($cat['url']), 'name' => $cat['title'], 'description' => $cat['description'],
        'isPartOf' => ['@id' => abs_url('/#website')],
        'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => array_map(fn($p, $i) => ['@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url($p['url']), 'name' => $p['title']], $posts, array_keys($posts))],
    ]],
]);
?>
<section class="page-head cat-<?= e($cat['slug']) ?>">
  <div class="wrap">
    <?php breadcrumbs($crumbs); ?>
    <h1><?= e($cat['title']) ?></h1>
    <p class="lead"><?= e($cat['description']) ?></p>
  </div>
</section>
<section class="section">
  <div class="wrap grid">
<?php foreach ($posts as $p) echo post_card($p); ?>
  </div>
</section>
<?php if ($relTools): ?>
<section class="section section--tint">
  <div class="wrap">
    <div class="section__head"><h2>Tools for <?= e(strtolower($cat['name'])) ?></h2></div>
    <div class="tool-grid">
<?php foreach (array_keys($relTools) as $t) echo tool_card($t); ?>
    </div>
  </div>
</section>
<?php endif;
page_foot();
