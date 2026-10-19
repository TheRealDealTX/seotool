<?php
require dirname(__DIR__) . '/inc/config.php';

$posts = all_posts();
$featured = array_shift($posts);
$cats = array_values(array_unique(array_map(fn($p) => $p['category'], all_posts())));
sort($cats);

$page = [
    'title' => 'Insurance Adjuster Advice: Salary & Career Guides',
    'description' => 'Insurance adjuster advice on salary, pay rates, licensing and career paths for staff, independent, CAT and public adjusters. New guides every few weeks.',
    'path' => BLOG_BASE,
    'image' => 'office-team.webp',
    'schema' => [[
        '@type' => 'Blog',
        'name' => 'Insurance Adjuster Advice',
        'url' => base_url() . BLOG_BASE,
        'blogPost' => array_values(array_map(fn($p) => ['@type' => 'BlogPosting', 'headline' => $p['title'], 'url' => base_url() . post_url($p), 'datePublished' => $p['date']], all_posts())),
    ]],
];
require SITE_ROOT . '/inc/header.php';
?>
<section class="page-hero">
  <div class="hero-media"><img src="/assets/img/office-team.webp" alt="" width="1200" height="675"></div>
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span>Insurance Adjuster Advice</nav>
    <span class="eyebrow">The blog</span>
    <h1>Insurance Adjuster Advice</h1>
    <p>Salary breakdowns, pay structures, state guides and career advice for adjusters at every stage &mdash; from your first license to your tenth storm season.</p>
  </div>
</section>

<section class="section">
  <div class="container">
<?php if ($featured): ?>
    <article class="featured-post reveal">
      <a href="<?= e(post_url($featured)) ?>" tabindex="-1" aria-hidden="true"><img src="/assets/img/<?= e($featured['image']) ?>" alt="" width="1200" height="675"></a>
      <div class="fp-body">
        <div class="post-meta"><span class="chip">Latest</span><time datetime="<?= e($featured['date']) ?>"><?= e(fmt_date($featured['date'])) ?></time></div>
        <h2><a href="<?= e(post_url($featured)) ?>"><?= e($featured['title']) ?></a></h2>
        <p><?= e($featured['excerpt']) ?></p>
        <a class="btn btn-gold" href="<?= e(post_url($featured)) ?>" style="align-self:flex-start">Read the guide <?= icon('arrow', 16) ?></a>
      </div>
    </article>
<?php endif; ?>
    <div class="filter-bar tabs" role="tablist" aria-label="Filter by category" style="display:flex;width:fit-content;margin-inline:auto">
      <button class="tab" type="button" data-cat="all" aria-selected="true">All</button>
<?php foreach ($cats as $c): ?>
      <button class="tab" type="button" data-cat="<?= e($c) ?>" aria-selected="false"><?= e($c) ?></button>
<?php endforeach; ?>
    </div>
    <div class="post-grid">
<?php foreach ($posts as $p) echo str_replace('<article class="post-card reveal">', '<article class="post-card reveal" data-cat="' . e($p['category']) . '">', post_card($p)); ?>
    </div>
  </div>
</section>
<?= course_cta() ?>
<?php require SITE_ROOT . '/inc/footer.php'; ?>
