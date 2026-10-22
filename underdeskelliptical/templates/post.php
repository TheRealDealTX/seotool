<?php
if (!defined('ROOT')) { http_response_code(404); exit; }
/** @var array $post */
$cat = $post['category'];
$crumbs = [['Home', '/'], [CATEGORIES[$cat][0], "/topic/$cat/"], [$post['h1'], $post['url']]];

$body = render_shortcodes($post['body']);
[$body, $toc] = add_heading_ids($body);
$tocHtml = toc_html($toc);
// TOC goes before the first h2 unless the author placed [[toc]] explicitly.
if (str_contains($body, '[[toc]]')) {
    $body = str_replace('[[toc]]', $tocHtml, $body);
} elseif ($tocHtml) {
    $pos = strpos($body, '<h2');
    $body = $pos === false ? $body : substr($body, 0, $pos) . $tocHtml . substr($body, $pos);
}
$words = str_word_count(strip_tags($body));
$minutes = max(3, (int) round($words / 230));

$schema = [
    [
        '@type' => ($post['schema_type'] ?? 'Article'), '@id' => SITE_URL . $post['url'] . '#article',
        'headline' => $post['h1'], 'description' => $post['description'],
        'image' => abs_url($post['image'] ?? DEFAULT_IMAGE),
        'datePublished' => $post['published'] . 'T08:00:00+00:00', 'dateModified' => $post['updated'] . 'T08:00:00+00:00',
        'author' => ['@type' => 'Organization', 'name' => AUTHOR_NAME, 'url' => SITE_URL . '/about-us/'],
        'publisher' => ['@id' => SITE_URL . '/#org'], 'mainEntityOfPage' => SITE_URL . $post['url'],
        'keywords' => $post['keyword'] ?? '', 'wordCount' => $words, 'articleSection' => CATEGORIES[$cat][0],
    ],
    schema_breadcrumbs($crumbs),
];
if (!empty($post['faq'])) {
    $schema[] = schema_faq($post['faq']);
}
if (!empty($post['itemlist'])) {
    $items = [];
    foreach ($post['itemlist'] as $i => $k) {
        $items[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => product($k)['name'], 'url' => amz_url($k)];
    }
    $schema[] = ['@type' => 'ItemList', 'name' => $post['h1'], 'itemListElement' => $items];
}

page_start([
    'title' => $post['title'], 'description' => $post['description'], 'image' => $post['image'] ?? null,
    'og_type' => 'article', 'published' => $post['published'], 'updated' => $post['updated'],
    'schema' => $schema, 'preload' => $post['image'] ?? null, 'body_class' => 'is-post',
]);
?>
<div class="wrap post-layout">
  <article class="post">
    <?= breadcrumbs_html($crumbs) ?>
    <h1><?= e($post['h1']) ?></h1>
    <p class="post-meta">By <a href="/about-us/"><?= e(AUTHOR_NAME) ?></a> &middot; Updated <time datetime="<?= e($post['updated']) ?>"><?= e(fmt_date($post['updated'])) ?></time> &middot; <?= $minutes ?> min read</p>
    <p class="disclosure">This guide contains affiliate links. As an Amazon Associate, <?= e(SITE_NAME) ?> earns from qualifying purchases at no extra cost to you. <a href="/affiliate-disclosure/">Learn more</a>.</p>
<?php if (!empty($post['image'])): ?>
    <figure class="post-hero"><img src="<?= e($post['image']) ?>" alt="<?= e($post['image_alt'] ?? $post['h1']) ?>" width="1536" height="1024" fetchpriority="high"></figure>
<?php endif; ?>
<?php if (!empty($post['summary'])): ?>
    <div class="key-takeaways"><p class="kt-title">Quick answer</p><?= render_shortcodes($post['summary']) ?></div>
<?php endif; ?>
    <div class="prose">
<?= $body ?>
    </div>
<?php if (!empty($post['faq'])): ?>
    <?= faq_html($post['faq']) ?>
<?php endif; ?>
    <aside class="author-box">
      <img src="<?= e(SITE_ICON) ?>" alt="" width="64" height="64" loading="lazy">
      <div><p class="author-name"><?= e(AUTHOR_NAME) ?></p>
      <p>We research under desk ellipticals, desk bikes and walking pads by comparing manufacturer specs, owner reviews and exercise research, then write plain-English guides for people who sit for work. <a href="/about-us/">How we research</a>.</p></div>
    </aside>
<?php if (!empty($post['tags'])): ?>
    <p class="post-tags">Tagged:
<?php foreach ($post['tags'] as $t): if (isset(TAGS[$t])): ?>
      <a href="/tag/<?= e($t) ?>/"><?= e(TAGS[$t][0]) ?></a>
<?php endif; endforeach; ?>
    </p>
<?php endif; ?>
  </article>
  <aside class="sidebar">
    <div class="side-box side-quiz">
      <p class="side-title">Not sure which to buy?</p>
      <p>Answer 5 quick questions and get matched to the right under desk elliptical.</p>
      <a class="btn" href="/tools/which-under-desk-elliptical-quiz/">Take the 60-second quiz</a>
    </div>
    <div class="side-box">
      <p class="side-title">Our top picks</p>
      <ol class="side-picks">
<?php foreach (['cubii-jr2', 'deskcycle-ellipse', 'sunny-sf-e3872', 'ancheer'] as $k): $p = product($k); ?>
        <li><a href="<?= e(amz_url($k)) ?>" <?= amz_attrs() ?>><strong><?= e($p['name']) ?></strong><span><?= e($p['best_for']) ?></span></a></li>
<?php endforeach; ?>
      </ol>
    </div>
    <div class="side-box">
      <p class="side-title">Free tools</p>
      <ul class="side-links">
<?php foreach (TOOLS as $slug => $t): ?>
        <li><a href="/tools/<?= e($slug) ?>/"><?= e($t['short']) ?></a></li>
<?php endforeach; ?>
      </ul>
    </div>
  </aside>
</div>
<section class="related wrap">
  <h2>Keep reading</h2>
  <div class="grid grid-3">
<?php foreach (related_posts($post, 3) as $r): ?>
    <?= post_card($r) ?>
<?php endforeach; ?>
  </div>
</section>
<?php page_end();
