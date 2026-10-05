<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Blog', '/blog/']];
$all = array_values(posts());
$items = array_map(fn($p) => [$p['h1'], $p['path']], $all);
$page = [
    'title' => 'Landscape Lighting Blog: Ideas, Costs & Design Guides',
    'description' => 'Guides from Austin Landscape Lighting on fixture counts, costs, design rules, trees, pools, backyards and choosing a landscape lighting company in Austin, TX.',
    'path' => '/blog/',
    'active' => '/blog/',
    'image' => 'landscape-lighting-ideas-austin-1',
    'schema' => [schema_webpage(['title' => 'Blog', 'description' => 'Austin Landscape Lighting blog.', 'path' => '/blog/'], 'CollectionPage'), schema_breadcrumb($crumbs), schema_itemlist($items, 'Austin Landscape Lighting articles')],
];
ob_start();
echo sub_hero(['eyebrow' => 'Blog', 'h1' => 'Landscape Lighting Ideas, Costs and Design Guides', 'intro' => 'Practical articles from the Austin Landscape Lighting design team: how many fixtures you need, what systems cost, which techniques suit live oaks and limestone, and how to compare contractors.', 'crumbs' => $crumbs, 'cta' => false]);
?>
<section class="section">
  <div class="container">
    <div class="cat-nav" data-cat-nav>
      <button type="button" class="is-active" data-cat="all">All articles (<?= count($all) ?>)</button>
      <?php foreach (post_categories() as $c => $n): ?><button type="button" data-cat="<?= e($c) ?>"><?= e($c) ?> (<?= $n ?>)</button><?php endforeach; ?>
    </div>
    <div class="blog-grid">
      <?php foreach ($all as $i => $p): ?>
      <div data-cat-card="<?= e($p['category']) ?>" style="display:contents"><?= post_card($p, $i === 0) ?></div>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section--alt section--tight">
  <div class="container">
    <?= section_head('Do the math first', 'Free planning tools', 'Pair the guides with our calculators for fixture counts, cost, LED savings and transformer sizing.', 'left') ?>
    <div class="grid grid--4"><?php foreach (array_slice(array_values(tools()), 0, 4) as $i => $t) echo tool_card($t, $i); ?></div>
  </div>
</section>
<?= cta_band() ?>
<?php
render_page($page, ob_get_clean());
