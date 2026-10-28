<?php
$path = '/blogs/';
$crumbs = [['Home', '/'], ['All Articles', $path]];
$list = articles();
page_head([
    'title' => 'All Articles: Apartment Design Guides & Ideas',
    'description' => 'Every Luxury Apartment Design guide in one place: apartment decorating ideas, small-space storage, color palettes, renter-friendly upgrades and more.',
    'path' => $path,
    'schema' => [
        ['@type' => 'CollectionPage', '@id' => url($path), 'name' => 'All Articles', 'isPartOf' => ['@id' => url('/#website')]],
        schema_breadcrumbs($crumbs),
    ],
]);
?>
<section class="page-hero">
  <div class="container">
    <?= breadcrumbs_html($crumbs) ?>
    <h1>All Apartment Design Guides</h1>
    <p class="page-hero__lead"><?= count($list) ?> in-depth guides from <?= e(SITE_NAME) ?>, from big-picture luxury apartment interior design to the exact height to hang a frame. Filter by topic or search as you type.</p>
    <div class="filter-bar">
      <label class="sr-only" for="article-filter">Filter articles</label>
      <input id="article-filter" type="search" placeholder="Filter by keyword…" data-filter-input>
      <div class="chips" role="group" aria-label="Filter by topic">
        <button class="chip is-active" type="button" data-filter-cat="">All</button>
        <?php foreach (CATEGORIES as $s => $c): ?>
        <button class="chip" type="button" data-filter-cat="<?= $s ?>"><?= e($c['name']) ?></button>
        <?php endforeach; ?>
      </div>
    </div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid--3" data-filter-list>
      <?php foreach ($list as $a): ?>
      <div data-cat="<?= e($a['category']) ?>" data-text="<?= e(strtolower($a['title'] . ' ' . $a['excerpt'] . ' ' . $a['keyword'])) ?>"><?= article_card($a) ?></div>
      <?php endforeach; ?>
    </div>
    <p class="empty-state" data-filter-empty hidden>No guides match that filter yet. Try another word, or <a href="/contact/">suggest a topic</a>.</p>
  </div>
</section>
<?= newsletter_block() ?>
<?php page_foot(); ?>
