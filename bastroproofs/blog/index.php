<?php
require dirname(__DIR__) . '/includes/bootstrap.php';
$crumbs = [['Home', '/'], ['Blog', '/blog/']];
page_start([
    'title'       => 'Roofing Blog | Bastrop Homeowner Guides | Bastrop Roofing',
    'description' => 'Roofing guides for Bastrop, TX homeowners: roof replacement costs, metal vs. shingles, hail damage, pine trees, fire-resistant roofing and choosing a roofer.',
    'path'        => '/blog/',
    'schema'      => [breadcrumb_schema($crumbs), ['@type' => 'Blog', 'name' => 'Bastrop Roofing Blog', 'url' => abs_url('/blog/'), 'publisher' => ['@id' => abs_url('/#business')]]],
]);
page_hero('Bastrop Roofing Blog', 'Roofing Guides for Bastrop Homeowners', 'Straight answers on costs, materials, storms and maintenance — written for roofs in the Lost Pines and Bastrop County.', $crumbs, 'Roofing-Help-Built-Around-the-Condition-of-Your-Roof.webp');
?>
<section class="section">
  <div class="container">
    <div class="card-grid card-grid-3">
<?php foreach ($POSTS as $k => $p): ?>
      <a class="post-card reveal" href="/blog/<?= $k ?>/">
        <img src="<?= img($p['image']) ?>" alt="" width="1200" height="655" loading="lazy">
        <span class="post-card-body"><small><?= fmt_date($p['date']) ?> · <?= $p['minutes'] ?> min read</small><strong><?= e($p['h1']) ?></strong><span><?= e($p['excerpt']) ?></span></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php cta_band(); page_end();
