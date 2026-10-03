<?php
defined('TR_ROOT') || exit;
$category = $category ?? null;
$q = trim(mb_substr((string) ($_GET['q'] ?? ''), 0, 80));
$list = posts($category);
if ($q !== '') {
    $needle = mb_strtolower($q);
    $list = array_filter($list, fn ($p) => str_contains(mb_strtolower($p['title'] . ' ' . $p['excerpt'] . ' ' . strip_tags($p['body'])), $needle));
}
$cats = catalog('blog_categories');
$counts = [];
foreach (posts() as $p) {
    $counts[$p['category']] = ($counts[$p['category']] ?? 0) + 1;
}
if ($category) {
    $name = category_name($category);
    $crumbs = [['Roofing Blog', '/blog/'], [$name, '/blog/category/' . $category . '/']];
    $h1 = $name . ' Articles';
    $title = $name . ' — Temple Roofing Blog';
    $desc = 'Temple Roofers articles about ' . mb_strtolower($name) . ' for homeowners in Temple and Bell County, Texas.';
    $path = '/blog/category/' . $category . '/';
} else {
    $crumbs = [['Roofing Blog', '/blog/']];
    $h1 = 'Roofing Blog: Guides for Temple Homeowners';
    $title = 'Roofing Blog for Temple, TX Homeowners';
    $desc = 'Practical roofing guides for Temple, TX: hail and wind damage, roof costs, inspections, maintenance, materials and insurance claims.';
    $path = '/blog/';
}
$noindex = $q !== '' || ($category && empty($counts[$category]));
layout_start([
    'title' => $title, 'description' => $desc, 'path' => $path, 'crumbs' => $crumbs, 'noindex' => $noindex,
    'scripts' => ['js/blog.js'],
]);
page_hero(['h1' => $h1, 'lead' => 'Locally focused advice on storms, maintenance, costs and materials — written for Central Texas roofs.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true]);
?>
<section class="section">
  <div class="container">
    <div class="blog-tools reveal">
      <form class="blog-search" action="/blog/" method="get" role="search">
        <label class="sr-only" for="blog-q">Search articles</label>
        <?= icon('search') ?>
        <input type="search" id="blog-q" name="q" value="<?= e($q) ?>" placeholder="Search roofing articles…" data-blog-search>
        <button class="btn btn--navy btn--sm" type="submit">Search</button>
      </form>
      <nav class="cat-filter" aria-label="Blog categories">
        <a href="/blog/"<?= !$category ? ' aria-current="page"' : '' ?>>All</a>
        <?php foreach ($cats as $slug => $name): if (empty($counts[$slug])) continue; ?>
        <a href="/blog/category/<?= e($slug) ?>/"<?= $category === $slug ? ' aria-current="page"' : '' ?>><?= e($name) ?> <span><?= (int) $counts[$slug] ?></span></a>
        <?php endforeach; ?>
      </nav>
    </div>
    <?php if ($q !== ''): ?>
    <p class="result-note"><?= count($list) ?> result<?= count($list) === 1 ? '' : 's' ?> for “<?= e($q) ?>”. <a href="<?= e($path) ?>">Clear search</a></p>
    <?php endif; ?>
    <div class="card-grid card-grid--3" data-blog-list>
      <?php foreach ($list as $p): ?>
      <div class="blog-item" data-search="<?= e(mb_strtolower($p['title'] . ' ' . $p['excerpt'] . ' ' . category_name($p['category']) . ' ' . ($p['focus_keyword'] ?? ''))) ?>"><?= post_card($p, 'h2') ?></div>
      <?php endforeach; ?>
    </div>
    <p class="empty-note" data-blog-empty <?= $list ? 'hidden' : '' ?>>No published articles match that search yet. Try another term, browse <a href="/blog/">all articles</a>, or <a href="/contact/">ask us your question</a>.</p>
    <?php if (!$category && $q === ''): ?>
    <div class="callout reveal">New roofing guides are published every few days. Topics coming up include roof costs, repair-versus-replacement decisions, inspection timing, roof lifespan, wind damage, attic ventilation, insurance claims, leaks and seasonal maintenance.</div>
    <?php endif; ?>
  </div>
</section>
<?php final_cta('Have a Roofing Question? Get a Free Inspection.', '', $path); ?>
<?php layout_end();
