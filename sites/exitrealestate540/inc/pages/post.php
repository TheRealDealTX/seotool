<?php
defined('ERE') or exit;
$cat = category($post['category']);
$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$cat['name'], $cat['url']], [$post['title'], $post['url']]];
$body = render_body($post['body']);
$toc = toc($post['body']);
$image = abs_url('/assets/img/og/' . $post['slug'] . '.png');
if (!is_file(ROOT . '/assets/img/og/' . $post['slug'] . '.png')) $image = abs_url('/assets/img/og-default.png');
$schema = [[
    '@type' => 'BlogPosting',
    '@id' => abs_url($post['url'] . '#article'),
    'headline' => $post['title'],
    'description' => $post['description'],
    'image' => $image,
    'datePublished' => date('c', strtotime($post['date'])),
    'dateModified' => date('c', strtotime($post['updated'])),
    'author' => ['@type' => 'Organization', 'name' => cfg('author'), 'url' => abs_url('/about/')],
    'publisher' => ['@id' => abs_url('/#organization')],
    'mainEntityOfPage' => abs_url($post['url']),
    'articleSection' => $cat['name'],
    'keywords' => $post['keyword'],
    'wordCount' => $post['words'],
    'inLanguage' => 'en-US',
]];
if (!empty($post['faq'])) $schema[] = schema_faq($post['faq']);
page_head([
    'title' => $post['seo_title'] . ' | ' . cfg('short'),
    'og_title' => $post['title'],
    'description' => $post['description'],
    'path' => $post['url'],
    'type' => 'article',
    'image' => $image,
    'published' => $post['date'],
    'modified' => $post['updated'],
    'crumbs' => $crumbs,
    'schema' => $schema,
    'body_class' => 'single',
]);
$hasProducts = !empty($post['products']) || str_contains($post['body'], '[[product:');
?>
<article class="post">
  <header class="post__head cat-<?= e($post['category']) ?>">
    <div class="wrap wrap--narrow">
      <?php breadcrumbs(array_slice($crumbs, 0, 3)); ?>
      <a class="card__cat" href="<?= e($cat['url']) ?>"><?= e($cat['name']) ?></a>
      <h1><?= e($post['title']) ?></h1>
      <p class="lead"><?= e($post['excerpt']) ?></p>
      <p class="post__meta">
        <span>By <a href="/about/"><?= e(cfg('author')) ?></a></span>
        <span><?= icon('clock') ?> <?= (int) $post['read_minutes'] ?> min read</span>
        <span>Updated <time datetime="<?= e($post['updated']) ?>"><?= e(fmt_date($post['updated'])) ?></time></span>
      </p>
    </div>
  </header>
  <div class="wrap post__layout">
    <aside class="post__aside">
<?php if (count($toc) > 2): ?>
      <nav class="toc" aria-label="On this page">
        <p class="toc__title">On this page</p>
        <ol>
<?php foreach ($toc as [$id, $t]): ?>
          <li><a href="#<?= e($id) ?>"><?= e($t) ?></a></li>
<?php endforeach; ?>
        </ol>
      </nav>
<?php endif; ?>
<?php foreach ($post['tools'] ?? [] as $t) echo tool_card($t, 'tool-card tool-card--side'); ?>
    </aside>
    <div class="prose">
<?php if ($hasProducts): ?>
      <p class="disclosure">This article contains affiliate links. If you buy through them we may earn a commission at no cost to you. <a href="/affiliate-disclosure/">Details</a>.</p>
<?php endif; ?>
      <?= $body ?>

<?php if (!empty($post['faq'])): ?>
      <section class="faq" aria-labelledby="faq">
        <h2 id="faq">Frequently asked questions</h2>
<?php foreach ($post['faq'] as [$q, $a]): ?>
        <details><summary><?= e($q) ?></summary><p><?= e($a) ?></p></details>
<?php endforeach; ?>
      </section>
<?php endif; ?>

<?php if (!empty($post['products'])): ?>
      <section class="gear">
        <h2 id="recommended-gear">Recommended gear</h2>
        <div class="products products--stack">
<?php foreach ($post['products'] as $k) echo product_card($k, true); ?>
        </div>
      </section>
<?php endif; ?>
      <p class="post__note">This guide is for general education and is not legal, tax, insurance or financial advice. Laws, rates and programs change - confirm details for your situation with a licensed professional.</p>
    </div>
  </div>
</article>
<?php
$related = [];
foreach ($post['related'] ?? [] as $s) if (($p = get_post($s)) && $s !== $post['slug']) $related[$s] = $p;
foreach (posts_in($post['category']) as $s => $p) if ($s !== $post['slug'] && !isset($related[$s])) $related[$s] = $p;
$related = array_slice(array_values($related), 0, 3);
if ($related): ?>
<section class="section section--tint">
  <div class="wrap">
    <div class="section__head"><h2>Keep reading</h2></div>
    <div class="grid">
<?php foreach ($related as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<?php endif;
page_foot();
