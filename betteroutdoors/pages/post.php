<?php defined('BO') || exit;
// Single post template. Content lives in content/posts/{slug}.php and is
// buffered first so the TOC, reading time and FAQ schema can be derived from it.

$p = $POSTS[$slug];
$GLOBALS['FAQS'] = [];
ob_start();
require __DIR__ . '/../content/posts/' . $slug . '.php';
$body = ob_get_clean();

$url    = '/' . $slug . '/';
$crumbs = [['Home', '/'], [$p['cat'], '/category/tips/'], [$p['h1'], $url]];
$schema = [
    [
        '@type' => 'BlogPosting',
        '@id' => SITE_URL . $url . '#article',
        'headline' => $p['h1'],
        'description' => $p['desc'],
        'image' => SITE_URL . img_url($p['image']),
        'datePublished' => $p['date'] . 'T08:00:00+00:00',
        'dateModified' => $p['updated'] . 'T08:00:00+00:00',
        'author' => ['@type' => 'Organization', 'name' => 'Better Outdoors Editorial Team', 'url' => SITE_URL . '/about-us/'],
        'publisher' => ['@id' => SITE_URL . '/#organization'],
        'mainEntityOfPage' => SITE_URL . $url,
        'keywords' => $p['kw'],
        'articleSection' => $p['cat'],
        'wordCount' => str_word_count(strip_tags($body)),
    ],
    breadcrumb_schema($crumbs),
];
if ($GLOBALS['FAQS']) {
    $qa = [];
    foreach ($GLOBALS['FAQS'] as $q => $a) $qa[] = ['@type' => 'Question', 'name' => $q, 'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($a)]];
    $schema[] = ['@type' => 'FAQPage', 'mainEntity' => $qa];
}

page_head([
    'title' => $p['title'], 'desc' => $p['desc'], 'path' => $url, 'type' => 'article',
    'image' => img_url($p['image']), 'preload' => img_url($p['image']), 'schema' => $schema,
    'published' => $p['date'], 'modified' => $p['updated'], 'body_class' => 'is-post',
]);
?>
<article class="post">
  <header class="post-hero">
    <div class="post-hero-bg" style="background-image:url('<?= e(img_url($p['image'])) ?>')" aria-hidden="true"></div>
    <div class="wrap post-hero-inner">
      <?= breadcrumbs_html($crumbs) ?>
      <span class="chip chip-light"><?= e($p['cat']) ?></span>
      <h1><?= e($p['h1']) ?></h1>
      <p class="post-dek"><?= e($p['excerpt']) ?></p>
      <ul class="post-meta">
        <li><i class="fa-solid fa-mountain" aria-hidden="true"></i> Better Outdoors Editorial Team</li>
        <li><i class="fa-regular fa-calendar" aria-hidden="true"></i> Updated <time datetime="<?= e($p['updated']) ?>"><?= e(fmt_date($p['updated'])) ?></time></li>
        <li><i class="fa-regular fa-clock" aria-hidden="true"></i> <?= reading_minutes($body) ?> min read</li>
      </ul>
    </div>
  </header>
  <div class="wrap post-layout">
    <div class="post-main">
      <figure class="post-lead">
        <img src="<?= e(img_url($p['image'])) ?>" alt="<?= e($p['h1']) ?>" width="1200" height="800" fetchpriority="high" decoding="async">
      </figure>
      <p class="disclosure"><i class="fa-solid fa-circle-info" aria-hidden="true"></i> Better Outdoors is reader-supported. When you buy through our Amazon links we may earn a commission, at no extra cost to you. <a href="/privacy-policy/#affiliate-disclosure">Learn more</a>.</p>
      <div class="toc-mobile"><?= build_toc($body) ?></div>
      <div class="prose">
<?= $body ?>
      </div>
      <div class="author-box reveal">
        <img src="<?= img_url('cropped-Better-Outdoors-Site-Icon-192x192.webp') ?>" alt="" width="64" height="64" loading="lazy">
        <div>
          <p class="author-name">Written by the Better Outdoors Editorial Team</p>
          <p>We are bowhunters and gear nerds who test, tune and shoot the equipment we write about. Every Better Outdoors guide is checked against manufacturer specs and updated as models change. <a href="/about-us/">How we review gear</a>.</p>
        </div>
      </div>
      <div class="share">
        <span>Share this guide:</span>
        <a href="https://www.facebook.com/sharer/sharer.php?u=<?= rawurlencode(SITE_URL . $url) ?>" target="_blank" rel="noopener" aria-label="Share on Facebook"><i class="fa-brands fa-facebook-f" aria-hidden="true"></i></a>
        <a href="https://twitter.com/intent/tweet?url=<?= rawurlencode(SITE_URL . $url) ?>&amp;text=<?= rawurlencode($p['h1']) ?>" target="_blank" rel="noopener" aria-label="Share on X"><i class="fa-brands fa-x-twitter" aria-hidden="true"></i></a>
        <a href="https://pinterest.com/pin/create/button/?url=<?= rawurlencode(SITE_URL . $url) ?>&amp;media=<?= rawurlencode(SITE_URL . img_url($p['image'])) ?>" target="_blank" rel="noopener" aria-label="Pin on Pinterest"><i class="fa-brands fa-pinterest-p" aria-hidden="true"></i></a>
        <button type="button" class="copy-link" data-url="<?= e(SITE_URL . $url) ?>" aria-label="Copy link"><i class="fa-solid fa-link" aria-hidden="true"></i></button>
      </div>
    </div>
    <aside class="post-side">
      <div class="side-sticky">
        <?= build_toc($body) ?>
        <div class="side-card side-tools">
          <p class="side-title"><i class="fa-solid fa-screwdriver-wrench" aria-hidden="true"></i> Free Archery Tools</p>
          <ul>
<?php foreach ($TOOLS as $ts => $t): ?>
            <li><a href="/tools/<?= e($ts) ?>/"><i class="fa-solid <?= e($t['icon']) ?>" aria-hidden="true"></i> <?= e($t['h1']) ?></a></li>
<?php endforeach; ?>
          </ul>
        </div>
      </div>
    </aside>
  </div>
  <section class="related">
    <div class="wrap">
      <h2 class="section-title">Related Articles</h2>
      <div class="post-grid">
<?php
$rel = array_filter($POSTS, fn($k) => $k !== $slug, ARRAY_FILTER_USE_KEY);
uasort($rel, fn($a, $b) => ($b['cat'] === $p['cat']) <=> ($a['cat'] === $p['cat']));
foreach (array_slice($rel, 0, 3, true) as $rs => $rp) echo post_card($rs, $rp);
?>
      </div>
    </div>
  </section>
</article>
<?php page_foot(); ?>
