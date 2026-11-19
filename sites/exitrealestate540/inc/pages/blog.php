<?php
defined('ERE') or exit;
$posts = array_values(all_posts());
$crumbs = [['Home', '/'], ['Blog', '/blog/']];
page_head([
    'title' => 'Real Estate Blog: Texas Buying, Selling & Claims Guides | Exit Real Estate 540',
    'description' => 'Every guide on Exit Real Estate 540: Texas home buying, selling, investing, property taxes, Houston living and home insurance claims - updated for ' . date('Y') . '.',
    'path' => '/blog/',
    'crumbs' => $crumbs,
    'schema' => [[
        '@type' => 'Blog', '@id' => abs_url('/blog/#blog'), 'url' => abs_url('/blog/'), 'name' => 'Exit Real Estate 540 Blog',
        'publisher' => ['@id' => abs_url('/#organization')],
        'blogPost' => array_map(fn($p) => ['@type' => 'BlogPosting', 'headline' => $p['title'], 'url' => abs_url($p['url']), 'datePublished' => $p['date']], array_slice($posts, 0, 20)),
    ]],
]);
?>
<section class="page-head">
  <div class="wrap">
    <?php breadcrumbs($crumbs); ?>
    <h1>The Exit Real Estate 540 Blog</h1>
    <p class="lead">Practical, Texas-specific guides for every stage of owning property - from your first offer to your last closing, and everything that can go wrong in between.</p>
    <div class="chips">
<?php foreach (cfg('categories') as $slug => $cat): ?>
      <a class="chip" href="/category/<?= $slug ?>/"><?= e($cat['name']) ?></a>
<?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap grid">
<?php foreach ($posts as $p) echo post_card($p); ?>
  </div>
</section>
<?php page_foot();
