<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Gallery', '/gallery/']];
$items = gallery_items();
$cats = array_values(array_unique(array_column($items, 'cat')));
sort($cats);
$page = [
    'title' => 'Landscape Lighting Gallery: Austin Projects After Dark',
    'description' => 'Browse Austin Landscape Lighting projects: facades, trees, paths, pools, patios, backyards and commercial properties across Austin, lit at night.',
    'path' => '/gallery/',
    'active' => '/gallery/',
    'image' => 'best-landscape-lighting-austin-1',
    'schema' => [schema_webpage(['title' => 'Gallery', 'description' => 'Austin Landscape Lighting project gallery.', 'path' => '/gallery/'], 'CollectionPage'), schema_breadcrumb($crumbs), ['@type' => 'ImageGallery', 'name' => 'Austin Landscape Lighting project gallery', 'url' => url('/gallery/'), 'numberOfItems' => count($items)]],
];
ob_start();
echo sub_hero(['eyebrow' => 'Gallery', 'h1' => 'Austin After Dark: The Project Gallery', 'intro' => 'A look at the homes, trees, pools and storefronts Austin Landscape Lighting has brought to life. Filter by type and tap any photo to view it full size. Every scene uses 2700K warm-white LED and solid brass fixtures.', 'image' => 'best-landscape-lighting-austin-1', 'image_alt' => 'Best landscape lighting in Austin: lit limestone home at night', 'crumbs' => $crumbs]);
?>
<section class="section">
  <div class="container">
    <div class="filters" data-reveal>
      <button type="button" class="is-active" data-filter="all">All (<?= count($items) ?>)</button>
      <?php foreach ($cats as $c): $n = count(array_filter($items, fn($i) => $i['cat'] === $c)); ?><button type="button" data-filter="<?= e($c) ?>"><?= e($c) ?> (<?= $n ?>)</button><?php endforeach; ?>
    </div>
    <div class="masonry" data-gallery>
      <?php foreach ($items as $i => $it): ?>
      <figure data-cat="<?= e($it['cat']) ?>" data-reveal style="--delay:<?= ($i % 6) * 40 ?>ms">
        <img src="<?= img($it['name'], true) ?>" data-full="<?= img($it['name']) ?>" alt="<?= e($it['alt']) ?>" width="720" height="405" loading="lazy" decoding="async">
        <figcaption><?= e($it['alt']) ?></figcaption>
      </figure>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?= cta_band('Want your home in this gallery?', 'Book a free dusk consultation and Austin Landscape Lighting will show you what your facade, trees and paths can look like after dark.') ?>
<?php
render_page($page, ob_get_clean());
