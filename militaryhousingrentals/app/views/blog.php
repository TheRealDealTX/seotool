<?php
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], ['Blog', null]]);
$all = posts();
layout_start([
    'title' => 'Blog',
    'description' => 'PCS checklists, BAH explainers, lease and SCRA guides, and tips for living in base housing, written for service members and military families.',
    'path' => '/blog/',
    'schema' => [$crumb_schema, ['@type' => 'Blog', 'url' => abs_url('/blog/'), 'name' => cfg('name') . ' Blog',
        'blogPost' => array_map(fn($p) => ['@type' => 'BlogPosting', 'headline' => $p['title'], 'url' => abs_url('/' . $p['slug'] . '/'), 'datePublished' => $p['date']], $all)]],
]);
$lead = $all[0];
?>
<section class="page-hero">
  <div class="wrap">
    <?= $crumbs ?>
    <h1>Military housing blog</h1>
    <p class="lead">Practical guides for every stage of a PCS, from the day orders drop to the day you get your keys.</p>
    <label class="blog-search"><?= icon('search') ?><input type="search" placeholder="Search articles" data-post-search aria-label="Search articles"></label>
  </div>
</section>
<section class="section section-tight">
  <div class="wrap">
    <a class="card post-lead" href="/<?= e($lead['slug']) ?>/">
      <span class="card-media"><img src="<?= e($lead['image']['src'] ?? cfg('og_image')) ?>" alt="" width="900" height="560"></span>
      <span class="card-body">
        <span class="eyebrow">Latest article</span>
        <strong class="post-lead-title"><?= e($lead['title']) ?></strong>
        <span class="card-excerpt"><?= e($lead['excerpt']) ?></span>
        <span class="card-meta"><?= e(fmt_date($lead['date'])) ?> &middot; <?= reading_time($lead['slug']) ?> min read</span>
      </span>
    </a>
    <div class="card-grid" data-post-grid>
      <?php foreach (array_slice($all, 1) as $p): ?>
        <div data-post-q="<?= e(strtolower($p['title'] . ' ' . $p['excerpt'])) ?>"><?= post_card($p) ?></div>
      <?php endforeach; ?>
    </div>
    <p class="empty-inline" data-post-empty hidden>No articles match that search.</p>
  </div>
</section>
<?= cta_band() ?>
<?php layout_end();
