<?php
/** @var array $page */
[$body, $toc] = render_body($page['body']);

// City guides: a "top picks" jump list built from the article's own hustle headings.
$picks = [];
if (($page['category'] ?? '') === 'City Guides' && preg_match_all('/<h3 id="([^"]+)">(.*?)<\/h3>/s', $body, $m, PREG_SET_ORDER)) {
    foreach (array_slice($m, 0, 8) as $h) {
        $picks[] = [$h[1], preg_replace('/^\d+[.)]\s*/', '', trim(html_entity_decode(strip_tags($h[2]), ENT_QUOTES, 'UTF-8')))];
    }
}

$related = [];
foreach ($page['related'] ?? [] as $r) {
    if ($r !== $page['slug'] && ($p = content_load($r))) {
        $related[$r] = $p;
    }
}
foreach (all_posts() as $p) {
    if (count($related) >= 3) {
        break;
    }
    if ($p['slug'] !== $page['slug'] && !isset($related[$p['slug']]) && ($p['category'] ?? '') === ($page['category'] ?? '')) {
        $related[$p['slug']] = $p;
    }
}

$sidebarTool = !empty($page['tool']) ? tool_html($page['tool'], 'sidebar') : '';
$gear = !empty($page['gear']) ? gear_box($page['gear'], 'Gear for this side hustle') : '';
$cat = $page['category'] ?? 'Guides';
$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$cat, '/blog/?cat=' . category_slug($cat)], [$page['h1'], $page['url']]];

$meta = [
    'title' => $page['title'],
    'description' => $page['description'],
    'url' => $page['url'],
    'image' => $page['image'] ?? null,
    'type' => 'article',
    'published' => $page['published'],
    'modified' => $page['modified'] ?? $page['published'],
    'bodyClass' => 'is-article',
    'schema' => [
        [
            '@type' => 'BlogPosting',
            '@id' => abs_url($page['url']) . '#article',
            'headline' => $page['h1'],
            'description' => $page['description'],
            'image' => abs_url($page['image'] ?? SITE_IMAGE),
            'datePublished' => $page['published'] . 'T08:00:00+00:00',
            'dateModified' => ($page['modified'] ?? $page['published']) . 'T08:00:00+00:00',
            'author' => ['@type' => 'Organization', 'name' => SITE_NAME . ' Editorial Team', 'url' => SITE_URL . '/about/'],
            'publisher' => ['@id' => SITE_URL . '/#org'],
            'mainEntityOfPage' => abs_url($page['url']),
            'articleSection' => $cat,
            'wordCount' => str_word_count(strip_tags($page['body'])),
        ],
        schema_breadcrumbs($crumbs),
        schema_faq($page['faq'] ?? []),
    ],
];
require __DIR__ . '/header.php';
?>
<div class="read-progress" aria-hidden="true"><span></span></div>
<section class="page-hero">
  <canvas class="coin-canvas" data-density="0.35" aria-hidden="true"></canvas>
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="/blog/">Blog</a><span>/</span><a href="/blog/?cat=<?= e(category_slug($cat)) ?>"><?= e($cat) ?></a></nav>
    <span class="pill"><?= e($page['kicker'] ?? $cat) ?></span>
    <h1><?= e($page['h1']) ?></h1>
    <?php if (!empty($page['dek'])): ?><p class="dek"><?= e($page['dek']) ?></p><?php endif; ?>
    <div class="byline">
      <span><?= icon('users') ?>By the <?= e(SITE_NAME) ?> team</span>
      <span><?= icon('calendar') ?>Updated <time datetime="<?= e($page['modified'] ?? $page['published']) ?>"><?= e(nice_date($page['modified'] ?? $page['published'])) ?></time></span>
      <span><?= icon('clock') ?><?= reading_minutes($page['body']) ?> min read</span>
    </div>
  </div>
  <div style="height:72px"></div>
</section>

<div class="wrap article-layout">
  <article class="article-body">
    <?php if (!empty($page['image'])): ?>
    <figure class="feature-img"><img src="<?= e($page['image']) ?>" alt="<?= e($page['image_alt'] ?? $page['h1']) ?>" width="900" height="600" fetchpriority="high"></figure>
    <?php endif; ?>

    <?php if ($picks): ?>
    <div class="top-picks">
      <h2><?= icon('sparkle') ?>Top side hustles in <?= e($page['city'] ?? 'this guide') ?></h2>
      <ol>
        <?php foreach ($picks as [$id, $text]): ?><li><a href="#<?= e($id) ?>"><?= e($text) ?></a></li><?php endforeach; ?>
      </ol>
    </div>
    <?php elseif (count($toc) > 3): ?>
    <nav class="toc toc-inline" aria-label="In this article"><h2>In this article</h2><ol>
      <?php foreach ($toc as [$id, $text]): ?><li><a href="#<?= e($id) ?>"><?= e($text) ?></a></li><?php endforeach; ?>
    </ol></nav>
    <?php endif; ?>

    <?= $body ?>

    <?php if (!empty($page['faq']) && schema_faq($page['faq'])): ?>
    <section class="article-faq" id="faq">
      <h2 id="faq-heading">Frequently asked questions</h2>
      <div class="faq">
        <?php foreach ($page['faq'] as $i => $f): if (empty($f['q'])) continue; ?>
        <details<?= $i === 0 ? ' open' : '' ?>><summary><?= e(strip_tags($f['q'])) ?></summary><div><p><?= $f['a'] ?></p></div></details>
        <?php endforeach; ?>
      </div>
    </section>
    <?php endif; ?>

    <?= $gear ?>

    <div class="author-box">
      <img src="<?= SITE_ICON ?>" alt="" width="64" height="64" loading="lazy">
      <p><strong><?= e(SITE_NAME) ?> Editorial Team.</strong> We research side hustles the practical way — platform fees, real pay ranges and what it takes to land your first dollar. <a href="/about/">How we write our guides</a>.</p>
    </div>
    <p class="updated-note">Last reviewed <?= e(nice_date($page['modified'] ?? $page['published'])) ?>. Pay ranges are estimates and vary by city, season and effort. This article may contain affiliate links; see our <a href="/affiliate-disclosure/">disclosure</a>.</p>
  </article>

  <aside class="sidebar">
    <?php if (count($toc) > 2): ?>
    <nav class="toc" aria-label="Table of contents"><h2>On this page</h2><ol>
      <?php foreach ($toc as [$id, $text]): ?><li><a href="#<?= e($id) ?>"><?= e($text) ?></a></li><?php endforeach; ?>
    </ol></nav>
    <?php endif; ?>
    <?= $sidebarTool ?>
  </aside>
</div>

<?php if ($related): ?>
<section class="related">
  <div class="wrap">
    <h2>Keep reading</h2>
    <div class="grid grid-3">
      <?php foreach ($related as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<?php endif; ?>
<?php require __DIR__ . '/footer.php'; ?>
