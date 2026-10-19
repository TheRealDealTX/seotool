<?php
defined('PGF') || exit;

$p = POSTS[$slug];
[$body, $toc] = add_heading_ids(post_body($slug));
$minutes = read_minutes($body);
[$img, $iw, $ih] = $p['image'];
$cat = $p['cats'][0];
$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$p['title'], "/$slug/"]];
$url = SITE_URL . "/$slug/";

$schema = [
    [
        '@type' => 'BlogPosting',
        '@id' => $url . '#article',
        'headline' => $p['title'],
        'description' => $p['desc'],
        'url' => $url,
        'mainEntityOfPage' => $url,
        'image' => ['@type' => 'ImageObject', 'url' => abs_url($img), 'width' => $iw, 'height' => $ih],
        'datePublished' => iso_date($p['date']),
        'dateModified' => iso_date($p['modified']),
        'author' => ['@type' => 'Organization', 'name' => 'The Pure Goat Farms Team', 'url' => SITE_URL . '/about/'],
        'publisher' => ['@id' => SITE_URL . '/#organization'],
        'articleSection' => array_map(fn($c) => CATEGORIES[$c]['name'], $p['cats']),
        'wordCount' => str_word_count(strip_tags($body)),
        'inLanguage' => 'en-US',
    ],
];
if (!empty($p['faq'])) {
    $schema[] = schema_faq($p['faq']);
}

// Related posts: share a category first, then newest.
$related = [];
foreach (posts_sorted() as $s => $q) {
    if ($s !== $slug && array_intersect($q['cats'], $p['cats'])) $related[$s] = $q;
}
foreach (posts_sorted() as $s => $q) {
    if ($s !== $slug && !isset($related[$s])) $related[$s] = $q;
}
$related = array_slice($related, 0, 3, true);
$tool = $p['tool'] ?? null;

$page = [
    'path'      => "/$slug/",
    'title'     => $p['seo'] . ' — Pure Goat Farms',
    'og_title'  => $p['title'],
    'desc'      => $p['desc'],
    'image'     => $img,
    'type'      => 'article',
    'published' => $p['date'],
    'modified'  => $p['modified'],
    'crumbs'    => $crumbs,
    'schema'    => $schema,
    'preload'   => $img,
    'body_class' => 'page-post',
];
ob_start();
?>
<article class="post">
  <header class="post-hero">
    <div class="page-hero__bg" aria-hidden="true"><span class="blob blob--1"></span><span class="blob blob--2"></span></div>
    <div class="container post-hero__inner">
      <?= breadcrumbs_html($crumbs) ?>
      <div class="post-hero__meta reveal">
        <?php foreach ($p['cats'] as $c) echo cat_link($c); ?>
      </div>
      <h1 class="reveal"><?= e($p['title']) ?></h1>
      <p class="post-hero__byline reveal">
        <span>By <a href="/about/">The Pure Goat Farms Team</a></span>
        <span><?= icon('calendar') ?> <time datetime="<?= e($p['date']) ?>"><?= e(fmt_date($p['date'])) ?></time></span>
<?php if ($p['modified'] !== $p['date']): ?>
        <span>Updated <time datetime="<?= e($p['modified']) ?>"><?= e(fmt_date($p['modified'])) ?></time></span>
<?php endif; ?>
        <span><?= icon('clock') ?> <?= $minutes ?> min read</span>
      </p>
      <figure class="post-hero__img reveal">
        <img src="<?= e($img) ?>" alt="<?= e($p['alt']) ?>" width="<?= $iw ?>" height="<?= $ih ?>" fetchpriority="high">
      </figure>
    </div>
  </header>

  <div class="container post-layout">
    <aside class="post-toc" aria-label="Table of contents">
      <div class="post-toc__inner">
        <p class="post-toc__title">Table of Contents</p>
        <ol>
<?php foreach ($toc as [$id, $text]): ?>
          <li><a href="#<?= e($id) ?>"><?= e($text) ?></a></li>
<?php endforeach; ?>
<?php if (!empty($p['faq'])): ?>
          <li><a href="#faq-h">FAQs</a></li>
<?php endif; ?>
        </ol>
      </div>
    </aside>
    <div class="post-body prose">
      <?= $body ?>
<?php if (!empty($p['faq'])): ?>
      <?= faq_html($p['faq'], 'FAQs') ?>
<?php endif; ?>
      <div class="share">
        <span>Share this guide:</span>
        <a href="https://www.facebook.com/sharer/sharer.php?u=<?= rawurlencode($url) ?>" target="_blank" rel="noopener">Facebook</a>
        <a href="https://pinterest.com/pin/create/button/?url=<?= rawurlencode($url) ?>&amp;media=<?= rawurlencode(abs_url($img)) ?>&amp;description=<?= rawurlencode($p['title']) ?>" target="_blank" rel="noopener">Pinterest</a>
        <a href="https://twitter.com/intent/tweet?url=<?= rawurlencode($url) ?>&amp;text=<?= rawurlencode($p['title']) ?>" target="_blank" rel="noopener">X</a>
        <button type="button" class="copy-link" data-url="<?= e($url) ?>">Copy link</button>
      </div>
      <div class="author-box">
        <img src="<?= UPLOADS ?>cropped-Pure-Goat-Farms-Site-Icon-192x192.webp" alt="" width="64" height="64" loading="lazy">
        <div>
          <p class="author-box__name">Written by the Pure Goat Farms Team</p>
          <p>We're a family-run dairy-goat farm with 27 goats across six breeds. Every guide is tested on our own herd before it's published. <a href="/about/">More about us</a>.</p>
        </div>
      </div>
    </div>
    <aside class="post-side">
<?php if ($tool): $t = TOOLS[$tool]; ?>
      <div class="side-card side-card--tool">
        <span class="side-card__icon"><?= icon($t['icon']) ?></span>
        <p class="side-card__kicker">Free tool</p>
        <p class="side-card__title"><?= e($t['name']) ?></p>
        <p><?= e($t['desc']) ?></p>
        <a class="btn btn--rust btn--sm" href="/tools/<?= $tool ?>/">Open the tool</a>
      </div>
<?php endif; ?>
      <div class="side-card">
        <p class="side-card__kicker">Browse topics</p>
        <ul class="side-links">
<?php foreach (CATEGORIES as $s => $c): ?>
          <li><a href="/category/<?= $s ?>/"><?= icon($c['icon']) ?> <?= e($c['name']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
    </aside>
  </div>
</article>

<section class="section section--sand">
  <div class="container">
    <div class="section-head section-head--row reveal">
      <div><p class="eyebrow">Keep reading</p><h2>More from the field.</h2></div>
      <a class="btn btn--ghost" href="/blog/">All articles</a>
    </div>
    <div class="post-grid post-grid--3">
<?php foreach ($related as $s => $q): ?>
      <?= post_card($s, $q) ?>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php
render_page($page, ob_get_clean());
