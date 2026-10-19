<?php
defined('PGF') || exit;

$posts = posts_sorted();
$crumbs = [['Home', '/'], ['Blog', '/blog/']];
$items = [];
$i = 1;
foreach ($posts as $slug => $p) {
    $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => SITE_URL . "/$slug/", 'name' => $p['title']];
}
$page = [
    'path'   => '/blog/',
    'title'  => 'Goat Farming Blog — Milk, Breeds & Health Guides | Pure Goat Farms',
    'desc'   => 'The Pure Goat Farms blog: field-tested guides on goat milk production, milking schedules, dairy breeds, health and farm life from a working goat farm.',
    'crumbs' => $crumbs,
    'schema' => [
        ['@type' => 'CollectionPage', '@id' => SITE_URL . '/blog/#webpage', 'url' => SITE_URL . '/blog/', 'name' => 'Pure Goat Farms Blog', 'isPartOf' => ['@id' => SITE_URL . '/#website'], 'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $items]],
    ],
];
ob_start();
?>
<section class="page-hero">
  <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <p class="eyebrow reveal">Pure Goat Farms Blog</p>
    <h1 class="reveal">Goat farming field notes.</h1>
    <p class="page-hero__lead reveal">Milking routines, breed comparisons, health checklists and farm-life lessons — written from the milking stand, not a stock-photo library.</p>
    <div class="filter-bar reveal" role="toolbar" aria-label="Filter by category">
      <button class="chip is-on" type="button" data-filter="all">All</button>
<?php foreach (CATEGORIES as $slug => $c): ?>
      <button class="chip" type="button" data-filter="<?= $slug ?>"><?= e($c['name']) ?></button>
<?php endforeach; ?>
      <label class="search-field"><?= icon('search') ?><span class="sr-only">Search articles</span><input type="search" placeholder="Search guides…" data-search></label>
    </div>
  </div>
</section>
<section class="section section--tight">
  <div class="container">
    <div class="post-grid" data-filterable>
<?php foreach ($posts as $slug => $p): ?>
      <div class="post-grid__item" data-cats="<?= e(implode(' ', $p['cats'])) ?>" data-text="<?= e(strtolower($p['title'] . ' ' . $p['excerpt'])) ?>"><?= post_card($slug, $p) ?></div>
<?php endforeach; ?>
    </div>
    <p class="empty-state" hidden>No guides match that search yet. <a href="/contact/">Ask us</a> and it may become the next one.</p>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
