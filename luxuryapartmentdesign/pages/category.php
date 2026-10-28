<?php
/** @var string $slug */
$c = CATEGORIES[$slug];
$path = '/category/' . $slug . '/';
$list = articles_in($slug);
$crumbs = [['Home', '/'], [$c['name'], $path]];
$items = [];
$i = 1;
foreach ($list as $a) {
    $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => url('/' . $a['slug'] . '/'), 'name' => $a['h1']];
}
page_head([
    'title' => $c['title'],
    'description' => $c['description'],
    'path' => $path,
    'image' => $c['image'],
    'schema' => [
        ['@type' => 'CollectionPage', '@id' => url($path), 'name' => $c['title'], 'description' => $c['description'], 'isPartOf' => ['@id' => url('/#website')]],
        ['@type' => 'ItemList', 'itemListElement' => $items],
        schema_breadcrumbs($crumbs),
    ],
]);
?>
<section class="page-hero">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow"><?= count($list) ?> guides</p>
    <h1><?= e($c['title']) ?></h1>
    <p class="page-hero__lead"><?= e($c['intro']) ?></p>
    <nav class="chips" aria-label="Topics">
      <?php foreach (CATEGORIES as $s => $cc): ?>
      <a class="chip<?= $s === $slug ? ' is-active' : '' ?>" href="/category/<?= $s ?>/"><?= e($cc['name']) ?></a>
      <?php endforeach; ?>
    </nav>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3">
      <?php foreach ($list as $a) echo article_card($a); ?>
    </div>
  </div>
</section>
<section class="section section--tint">
  <div class="container">
    <h2 class="section__title">Free tools to plan your space</h2>
    <div class="grid grid--3 tools-grid">
      <?php foreach (array_slice(array_keys(TOOLS), 0, 3) as $t) echo tool_card($t); ?>
    </div>
  </div>
</section>
<?= newsletter_block() ?>
<?php page_foot(); ?>
