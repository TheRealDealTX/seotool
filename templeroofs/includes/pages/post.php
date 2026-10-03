<?php
defined('TR_ROOT') || exit;
/** @var array $post */
$p = $post;
$crumbs = [['Roofing Blog', '/blog/'], [category_name($p['category']), '/blog/category/' . $p['category'] . '/'], [$p['title'], $p['url']]];
layout_start([
    'title'          => $p['seo_title'],
    'description'    => $p['meta_description'],
    'path'           => $p['url'],
    'crumbs'         => $crumbs,
    'image'          => $p['image'],
    'og_type'        => 'article',
    'published_time' => $p['date']->format('c'),
    'body_class'     => 'page-post',
    'schema'         => [schema_post($p), schema_faq($p['faqs'] ?? [])],
    'scripts'        => ['js/post.js'],
]);
$more = [];
foreach ($p['related_posts'] ?? [] as $slug) {
    if ($slug !== $p['slug'] && ($o = post($slug))) {
        $more[$slug] = $o;
    }
}
foreach (posts() as $o) {
    if (count($more) >= 3) {
        break;
    }
    if ($o['slug'] !== $p['slug'] && !isset($more[$o['slug']])) {
        $more[$o['slug']] = $o;
    }
}
?>
<div class="reading-progress" aria-hidden="true"><span data-progress></span></div>
<article class="post">
  <header class="post-header">
    <div class="container container--narrow">
      <?= breadcrumbs_html($crumbs) ?>
      <a class="tag" href="/blog/category/<?= e($p['category']) ?>/"><?= e(category_name($p['category'])) ?></a>
      <h1 class="post-header__title"><?= e($p['title']) ?></h1>
      <p class="post-meta">
        <span><?= icon('calendar') ?> Published <time datetime="<?= e($p['date']->format('Y-m-d')) ?>"><?= e(format_date($p['date'])) ?></time></span>
        <span><?= icon('clock') ?> <?= (int) $p['minutes'] ?> min read</span>
        <span><?= icon('user') ?> Temple Roofers</span>
      </p>
    </div>
    <div class="container post-header__media">
      <figure class="post-figure"><?= img($p['image'], $p['image_alt'], ['sizes' => '(max-width: 1100px) 100vw, 1100px', 'priority' => true]) ?></figure>
    </div>
  </header>
  <div class="container post-layout">
    <div class="prose post-body" data-post-body>
      <?= render_body($p['body'], 'Worried about your roof after reading this?') ?>
      <?= faq_html($p['faqs'] ?? [], 'Frequently Asked Questions') ?>
      <div class="post-end-cta">
        <h2>Get a Free Roof Inspection in Temple</h2>
        <p>Photos, plain-language findings and honest advice — at no cost and with no obligation.</p>
        <div class="btn-row"><a class="btn btn--gold" href="/free-roof-inspection/">Book My Free Inspection</a><a class="btn btn--ghost" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <?= e(cfg('phone_display')) ?></a></div>
      </div>
    </div>
    <aside class="sidebar">
      <div class="sidebar__sticky">
        <nav class="side-card toc" aria-label="On this page" data-toc hidden>
          <p class="side-card__title">On this page</p>
          <ol></ol>
        </nav>
        <div class="side-card side-card--navy">
          <p class="side-card__title">Free roof inspection</p>
          <p>Not sure what you are seeing? We will take a look for free.</p>
          <a class="btn btn--gold btn--block" href="/free-roof-inspection/">Schedule now</a>
          <a class="btn btn--outline-light btn--block" href="<?= e(tel_href()) ?>"><?= icon('phone') ?> <?= e(cfg('phone_display')) ?></a>
        </div>
      </div>
    </aside>
  </div>
</article>
<div class="container">
  <?= related_html($p['related_services'] ?? [], []) ?>
</div>
<?php if ($more): ?>
<section class="section section--alt">
  <div class="container">
    <?= section_head('Keep reading', 'More Roofing Guides') ?>
    <div class="card-grid card-grid--3">
      <?php foreach (array_slice($more, 0, 3) as $o): ?><?= post_card($o) ?><?php endforeach; ?>
    </div>
  </div>
</section>
<?php endif; ?>
<?php layout_end();
