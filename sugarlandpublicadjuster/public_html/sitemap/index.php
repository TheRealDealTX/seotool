<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
require $_SERVER['DOCUMENT_ROOT'] . '/inc/pages.php';
$path = '/sitemap/';
$crumbs = [['Home', '/'], ['Sitemap', $path]];
page_start([
    'title' => 'Sitemap | Sugar Land Public Adjuster',
    'description' => 'Every page on the Sugar Land Public Adjuster website: services, tools and calculators, storm center, blog articles and contact information.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
]);
page_hero('Sitemap', '', $crumbs);
?>
<section class="section">
  <div class="container prose">
    <h2>Pages</h2>
    <ul class="sitemap-list">
<?php foreach (PAGES as [$p, $t]): ?>
      <li><a href="<?= e($p) ?>"><?= e($t) ?></a></li>
<?php endforeach; ?>
    </ul>
    <h2>Articles</h2>
    <ul class="sitemap-list">
<?php foreach (POSTS as $p): ?>
      <li><a href="/<?= e($p['slug']) ?>/"><?= e($p['title']) ?></a></li>
<?php endforeach; ?>
      <li><a href="/category/general/">Category: General</a></li>
    </ul>
    <p class="small muted">XML sitemap: <a href="/sitemap_index.xml">/sitemap_index.xml</a></p>
  </div>
</section>
<?php page_end(); ?>
