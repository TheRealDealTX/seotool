<?php defined('APP') || exit;

$p = blog_post($params[0]);
if (!$p) not_found('That guide doesn’t exist.');
cache_public();
$crumbs = [['The Sublet', '/'], ['Guides', '/blog/'], [$p['title'], '/blog/' . $p['slug'] . '/']];
$related = array_slice(array_filter(blog_posts(), fn($x) => $x['slug'] !== $p['slug'] && $x['category'] === $p['category']), 0, 3);
if (count($related) < 3) $related = array_slice(array_filter(blog_posts(), fn($x) => $x['slug'] !== $p['slug']), 0, 3);
$amz = array_map(fn($a) => $a + ['icon' => '🛒'], $p['amazon'] ?? []);
ob_start(); ?>
<div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <article class="post narrow">
    <header class="post-head">
      <p class="post-cat"><?= blog_category_icon($p['category']) ?> <?= e($p['category']) ?></p>
      <h1><?= e($p['title']) ?></h1>
      <p class="muted small">By The Sublet team · <?= e(fmt_date($p['date'])) ?> · <?= (int)($p['read_min'] ?? 6) ?> min read</p>
    </header>
    <?php $cover = photo('blog.' . $p['slug']); if ($cover): ?><figure class="post-cover"><img src="<?= e($cover['file']) ?>" alt="<?= e($cover['alt']) ?>" width="<?= (int)$cover['w'] ?>" height="<?= (int)$cover['h'] ?>" fetchpriority="high"></figure><?php endif; ?>
    <div class="prose"><?= $p['body'] ?></div>
    <?= faq_html($p['faqs'] ?? []) ?>
    <?= amazon_block($amz, 'Useful gear for this') ?>
    <aside class="cta-box">
      <h2 class="h3">Have a place to sublet?</h2>
      <p>List it on The Sublet free, or get a verified listing for <?= e(price_label()) ?> that goes live instantly.</p>
      <a class="btn" href="/post-a-sublet/">List your place</a> <a class="btn btn-ghost" href="/sublets/">Find a sublet</a>
    </aside>
    <p class="small muted">This article is general information, not legal, tax or financial advice. Rules vary by state, city and lease — check yours.</p>
  </article>
  <?php if ($related): ?>
  <section class="section"><h2>Keep reading</h2><div class="grid three"><?php foreach ($related as $r) echo blog_card($r); ?></div></section>
  <?php endif; ?>
</div>
<?php
page([
    'title' => $p['title'] . ' | The Sublet',
    'description' => $p['description'],
    'canonical' => '/blog/' . $p['slug'] . '/',
    'og_type' => 'article',
    'og_image' => ($cv = photo('blog.' . $p['slug'])) ? base_url($cv['file']) : null,
    'body' => ob_get_clean(),
    'schema' => array_values(array_filter([schema_article($p), schema_breadcrumbs($crumbs), schema_faq($p['faqs'] ?? [])])),
]);
