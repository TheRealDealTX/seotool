<?php
/** @var array $post */
$toc = post_toc($post['body']);
$crumbs = [['Blog', '/blog/'], [$post['title'], $post['path']]];
$schema = [[
    '@type'            => 'BlogPosting',
    '@id'              => url($post['path']) . '#article',
    'headline'         => $post['title'],
    'description'      => $post['description'],
    'image'            => ['@type' => 'ImageObject', 'url' => url($post['image']), 'width' => $post['image_w'], 'height' => $post['image_h']],
    'datePublished'    => $post['published'] . 'T08:00:00-05:00',
    'dateModified'     => $post['updated'] . 'T08:00:00-05:00',
    'author'           => ['@type' => 'Organization', 'name' => 'Best Jobs Pro Editorial Team', 'url' => url('/about/')],
    'publisher'        => ['@id' => SITE_URL . '/#organization'],
    'mainEntityOfPage' => url($post['path']),
    'keywords'         => $post['keyword'],
    'wordCount'        => $post['words'],
    'inLanguage'       => 'en-US',
]];
if (!empty($post['faqs'])) {
    $schema[] = faq_schema($post['faqs']);
}
page_start([
    // Keep the brand suffix only while the title stays short enough not to be truncated in search results.
    'title'       => mb_strlen($post['seo_title']) <= 46 ? $post['seo_title'] . ' | Best Jobs Pro' : $post['seo_title'],
    'og_title'    => $post['title'],
    'description' => $post['description'],
    'path'        => $post['path'],
    'image'       => $post['image'],
    'type'        => 'article',
    'published'   => $post['published'],
    'updated'     => $post['updated'],
    'preload'     => $post['image'],
    'crumbs'      => $crumbs,
    'schema'      => $schema,
]);
?>
<div class="read-progress" aria-hidden="true"><span></span></div>
<header class="article-hero">
  <div class="wrap">
    <?= breadcrumbs($crumbs) ?>
    <h1><?= e($post['title']) ?></h1>
    <div class="article-meta">
      <span><?= icon('users') ?> Best Jobs Pro Editorial Team</span>
      <span><?= icon('calendar') ?> Updated <time datetime="<?= e($post['updated']) ?>"><?= e(nice_date($post['updated'])) ?></time></span>
      <span><?= icon('book') ?> <?= $post['minutes'] ?> min read</span>
    </div>
    <figure class="article-cover"><img src="<?= e($post['image']) ?>" alt="<?= e($post['image_alt']) ?>" width="<?= (int)$post['image_w'] ?>" height="<?= (int)$post['image_h'] ?>" fetchpriority="high"></figure>
  </div>
</header>
<div class="wrap article-layout">
  <article class="prose">
    <?= render_post_body($post) ?>
<?php if (!empty($post['faqs'])): ?>
    <?= faq_block($post['faqs'], 'Frequently asked questions', 'faq') ?>
<?php endif; ?>
    <div class="author-box">
      <img src="/assets/img/site/Best-Jobs-Pro-Logo.webp" alt="" width="500" height="426" loading="lazy">
      <p><strong>Written by the Best Jobs Pro Editorial Team.</strong> Our recruiters place job seekers with employers across Texas every day and share what they learn here. First published <?= e(nice_date($post['published'])) ?>.</p>
    </div>
  </article>
  <aside>
    <nav class="toc" aria-label="On this page">
      <p class="toc__t">On this page</p>
      <ol>
<?php foreach ($toc as $t): ?>
        <li><a href="#<?= e($t['id']) ?>"><?= e($t['text']) ?></a></li>
<?php endforeach; ?>
<?php if (!empty($post['faqs'])): ?>
        <li><a href="#faq">FAQs</a></li>
<?php endif; ?>
      </ol>
      <div class="toc__cta"><p>Looking for work in Texas?</p><a class="btn btn--sm" href="/applications/">Apply with Best Jobs Pro</a></div>
    </nav>
  </aside>
</div>
<?php
$related = array_filter(array_map('get_post', $post['related'] ?? []));
if (count($related) < 3) {
    foreach (all_posts() as $p) {
        if ($p['slug'] !== $post['slug'] && !isset($related[$p['slug']]) && count($related) < 3) {
            $related[] = $p;
        }
    }
}
?>
<section class="related">
  <div class="wrap">
    <div class="section__head"><h2>Keep reading</h2></div>
    <div class="posts">
<?php foreach (array_slice($related, 0, 3) as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<?= cta_band() ?>
<?php page_end(!empty($post['tool']) ? ['/assets/js/tools.js'] : []);
