<?php defined('APP') || exit;

cache_public();
$posts = blog_posts();
$cat = get('category');
$cats = array_unique(array_column($posts, 'category'));
sort($cats);
if ($cat !== '' && in_array($cat, $cats, true)) $posts = array_filter($posts, fn($p) => $p['category'] === $cat);
$crumbs = [['The Sublet', '/'], ['Guides', '/blog/']];
ob_start(); ?>
<div class="wrap">
  <?= breadcrumbs_html($crumbs) ?>
  <header class="page-head">
    <h1>Sublet guides &amp; advice</h1>
    <p class="lead">Practical, plain-English guides from The Sublet for renters and hosts: subletting legally, sublease agreements, travel-nurse and intern housing, avoiding scams and more.</p>
  </header>
  <p class="chips"><a href="/blog/"<?= $cat === '' ? ' aria-current="page"' : '' ?>>All</a><?php foreach ($cats as $c): ?><a href="/blog/?category=<?= e(rawurlencode($c)) ?>"<?= $c === $cat ? ' aria-current="page"' : '' ?>><?= blog_category_icon($c) ?> <?= e($c) ?></a><?php endforeach; ?></p>
  <div class="grid three posts"><?php foreach ($posts as $p) echo blog_card($p); ?></div>
</div>
<?php
page([
    'title' => 'Sublet Guides for Renters & Hosts | The Sublet',
    'description' => 'Guides to subletting legally, sublease agreements, travel nurse and intern housing, rental scams, packing and pricing — from The Sublet.',
    'canonical' => '/blog/',
    'robots' => $cat !== '' ? 'noindex, follow' : 'index, follow',
    'body' => ob_get_clean(),
    'schema' => [schema_breadcrumbs($crumbs)],
]);
