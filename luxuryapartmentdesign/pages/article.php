<?php
/** @var array $a */
$cat = CATEGORIES[$a['category']] ?? ['name' => 'Articles'];
$path = '/' . $a['slug'] . '/';
[$body, $toc] = add_heading_ids(article_body($a['slug']));
$crumbs = [['Home', '/'], [$cat['name'], '/category/' . $a['category'] . '/'], [$a['h1'], $path]];
$tool = !empty($a['tool']) && isset(TOOLS[$a['tool']]) ? $a['tool'] : null;

$related = [];
foreach ($a['related'] ?? [] as $s) {
    if (($r = article($s)) && $s !== $a['slug']) {
        $related[$s] = $r;
    }
}
foreach (articles_in($a['category']) as $s => $r) {
    if (count($related) >= 3) {
        break;
    }
    if ($s !== $a['slug'] && !isset($related[$s])) {
        $related[$s] = $r;
    }
}

$schema = [
    [
        '@type' => 'BlogPosting',
        '@id' => url($path) . '#article',
        'headline' => $a['h1'],
        'description' => $a['description'],
        'image' => [url(img_url($a['image']))],
        'datePublished' => $a['published'] . 'T08:00:00+00:00',
        'dateModified' => ($a['updated'] ?? $a['published']) . 'T08:00:00+00:00',
        'author' => ['@type' => 'Organization', 'name' => SITE_NAME . ' Editorial Team', 'url' => url('/about-us/')],
        'publisher' => ['@id' => url('/#organization')],
        'mainEntityOfPage' => url($path),
        'articleSection' => $cat['name'],
        'keywords' => implode(', ', array_merge([$a['keyword']], $a['secondary_keywords'] ?? [])),
        'wordCount' => $a['words'],
        'inLanguage' => 'en-US',
    ],
    schema_breadcrumbs($crumbs),
    schema_faq($a['faq'] ?? []),
];

page_head([
    'title' => $a['title'],
    'description' => $a['description'],
    'path' => $path,
    'image' => $a['image'],
    'type' => 'article',
    'published' => $a['published'],
    'updated' => $a['updated'] ?? $a['published'],
    'schema' => $schema,
    'preload' => img_url($a['image']),
    'body_class' => 'is-article',
]);
?>
<article class="article">
  <header class="article-hero">
    <div class="container container--narrow">
      <?= breadcrumbs_html($crumbs) ?>
      <a class="eyebrow" href="/category/<?= e($a['category']) ?>/"><?= e($cat['name']) ?></a>
      <h1><?= e($a['h1']) ?></h1>
      <p class="article-hero__dek"><?= e($a['excerpt'] ?? '') ?></p>
      <div class="byline">
        <span>By the <a href="/about-us/"><?= e(SITE_NAME) ?> Editorial Team</a></span>
        <span>Updated <time datetime="<?= e($a['updated'] ?? $a['published']) ?>"><?= fmt_date($a['updated'] ?? $a['published']) ?></time></span>
        <span><?= icon('clock') ?> <?= $a['minutes'] ?> min read</span>
      </div>
    </div>
    <figure class="container article-hero__figure">
      <img src="<?= img_url($a['image']) ?>" srcset="<?= img_url($a['image'], true) ?> 600w, <?= img_url($a['image']) ?> 1200w" sizes="(max-width: 1100px) 100vw, 1100px" alt="<?= e($a['image_alt'] ?? $a['h1']) ?>" width="1200" height="800" fetchpriority="high">
    </figure>
  </header>

  <div class="container article-layout">
    <aside class="article-aside">
      <?php if ($toc): ?>
      <nav class="toc" aria-label="Table of contents">
        <p class="toc__title">In this guide</p>
        <ol>
          <?php foreach ($toc as [$id, $text]): ?>
          <li><a href="#<?= e($id) ?>"><?= e($text) ?></a></li>
          <?php endforeach; ?>
          <?php if (!empty($a['faq'])): ?><li><a href="#faq">FAQ</a></li><?php endif; ?>
        </ol>
      </nav>
      <?php endif; ?>
      <?php if ($tool): ?>
      <div class="aside-tool"><?= tool_card($tool) ?></div>
      <?php endif; ?>
    </aside>

    <div class="article-main">
      <?php if (!empty($a['key_takeaways'])): ?>
      <div class="takeaways">
        <p class="takeaways__title">Key takeaways</p>
        <ul>
          <?php foreach ($a['key_takeaways'] as $k): ?><li><?= e($k) ?></li><?php endforeach; ?>
        </ul>
      </div>
      <?php endif; ?>

      <div class="prose" data-checklist-key="<?= e($a['slug']) ?>">
        <?= $body ?>
      </div>

      <?php if ($tool): $t = TOOLS[$tool]; ?>
      <div class="tool-cta">
        <span class="tool-cta__icon"><?= icon($t['icon']) ?></span>
        <div>
          <p class="tool-cta__label">Free interactive tool</p>
          <p class="tool-cta__name"><?= e($t['name']) ?>: <?= e(lcfirst($t['short'])) ?></p>
        </div>
        <a class="btn btn--gold" href="/tools/<?= $tool ?>/">Try it free</a>
      </div>
      <?php endif; ?>

      <?= faq_block($a['faq'] ?? []) ?>

      <div class="share">
        <span>Share this guide:</span>
        <a href="https://pinterest.com/pin/create/button/?url=<?= rawurlencode(url($path)) ?>&amp;media=<?= rawurlencode(url(img_url($a['image']))) ?>&amp;description=<?= rawurlencode($a['h1']) ?>" target="_blank" rel="noopener">Pinterest</a>
        <a href="https://www.facebook.com/sharer/sharer.php?u=<?= rawurlencode(url($path)) ?>" target="_blank" rel="noopener">Facebook</a>
        <a href="mailto:?subject=<?= rawurlencode($a['h1']) ?>&amp;body=<?= rawurlencode(url($path)) ?>">Email</a>
        <button type="button" class="link-btn" data-copy="<?= e(url($path)) ?>">Copy link</button>
      </div>

      <div class="author-box">
        <img src="/assets/img/icon-192.png" alt="" width="64" height="64" loading="lazy">
        <div>
          <p class="author-box__name"><?= e(SITE_NAME) ?> Editorial Team</p>
          <p>We research designer standards, measure real rooms and test every recommendation against apartment realities: tight footprints, lease rules and budgets. <a href="/editorial-policy/">How we write our guides</a>.</p>
        </div>
      </div>
    </div>
  </div>
</article>

<?php if ($related): ?>
<section class="section section--tint">
  <div class="container">
    <h2 class="section__title">Keep reading</h2>
    <div class="grid grid--3">
      <?php foreach (array_slice($related, 0, 3) as $r) echo article_card($r); ?>
    </div>
  </div>
</section>
<?php endif; ?>

<?= newsletter_block() ?>
<?php page_foot(); ?>
