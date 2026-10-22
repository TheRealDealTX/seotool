<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
/** @var array $archive */
$posts = all_posts();
if ($archive['type'] === 'blog') {
    $name = 'Under Desk Elliptical Guides, Reviews & Comparisons';
    $h1 = 'All Under Desk Elliptical Guides';
    $intro = 'Every guide, review and comparison on ' . SITE_NAME . ', in one place. Filter by topic or search to find what you need.';
    $path = '/blog/';
    $title = 'Under Desk Elliptical Blog: Reviews, Guides & Comparisons';
    $crumbs = [['Home', '/'], ['Blog', '/blog/']];
} else {
    $slug = $archive['slug'];
    $isTag = $archive['type'] === 'tag';
    [$name, $intro] = $isTag ? TAGS[$slug] : CATEGORIES[$slug];
    $posts = array_filter($posts, fn($p) => $isTag ? in_array($slug, $p['tags']) : ($p['category'] === $slug || in_array($slug, $p['also'] ?? [])));
    $h1 = $isTag ? $name . ': Under Desk Elliptical Picks' : $name . ': Under Desk Elliptical Guides';
    if ($slug === 'reviews') { $h1 = 'Under Desk Elliptical Reviews'; }
    if ($slug === 'top-picks') { $h1 = 'Top Under Desk Elliptical Picks'; }
    if ($slug === 'compare') { $h1 = 'Under Desk Elliptical Comparisons'; }
    $path = ($isTag ? '/tag/' : '/topic/') . $slug . '/';
    $title = strlen($h1 . ' | ' . SITE_NAME) <= 60 ? $h1 . ' | ' . SITE_NAME : $h1 . ' (' . date('Y', strtotime(SITE_UPDATED)) . ')';
    $crumbs = [['Home', '/'], ['Blog', '/blog/'], [$name, $path]];
}
$items = [];
$i = 0;
foreach ($posts as $p) {
    $items[] = ['@type' => 'ListItem', 'position' => ++$i, 'url' => SITE_URL . $p['url'], 'name' => $p['h1']];
}
page_start([
    'title' => $title, 'description' => mb_strimwidth($intro . ' Browse ' . count($posts) . ' ' . strtolower($name) . ' articles, reviews and buying guides from ' . SITE_NAME . '.', 0, 158, '…'), 'path' => $path,
    'schema' => [schema_breadcrumbs($crumbs), ['@type' => 'CollectionPage', 'name' => $h1, 'url' => SITE_URL . $path,
        'mainEntity' => ['@type' => 'ItemList', 'itemListElement' => $items]]],
    // Thin tag archives stay out of the index; categories and the blog are indexable hubs.
    'noindex' => $archive['type'] === 'tag' && count($posts) < 3,
]);
?>
<section class="page-hero"><div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <h1><?= e($h1) ?></h1>
  <p class="lead"><?= e($intro) ?> <?= count($posts) ?> articles.</p>
</div></section>
<div class="wrap">
<?php if ($archive['type'] === 'blog'): ?>
  <div class="chips" role="group" aria-label="Filter by topic" data-filter-grid="#post-grid">
    <button type="button" class="chip on" data-f="all">All</button>
<?php foreach (CATEGORIES as $cs => [$cn]): if (array_filter($posts, fn($p) => $p['category'] === $cs)): ?>
    <button type="button" class="chip" data-f="<?= e($cs) ?>"><?= e($cn) ?></button>
<?php endif; endforeach; ?>
  </div>
<?php else: ?>
  <p class="chips"><a class="chip" href="/blog/">All guides</a>
<?php foreach (CATEGORIES as $cs => [$cn]): ?><a class="chip<?= $path === "/topic/$cs/" ? ' on' : '' ?>" href="/topic/<?= e($cs) ?>/"><?= e($cn) ?></a> <?php endforeach; ?></p>
<?php endif; ?>
  <div class="grid grid-3" id="post-grid">
<?php foreach ($posts as $p): ?>
    <?= post_card($p, 2) ?>
<?php endforeach; ?>
  </div>
<?php if (!$posts): ?><p>No articles here yet. <a href="/blog/">Browse all guides</a>.</p><?php endif; ?>
  <div class="cta-band"><div><h2>Find your match in 60 seconds</h2><p>Our quiz compares every under desk elliptical we cover against your desk, budget and goals.</p></div><a class="btn" href="/tools/which-under-desk-elliptical-quiz/">Start the quiz</a></div>
</div>
<?php page_end();
