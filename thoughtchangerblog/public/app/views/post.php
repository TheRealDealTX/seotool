<?php
/** @var array $post */
$body = post_body($post);
$url = '/' . $post['slug'] . '/';
$cat = primary_cat($post);
$products = $post['products'] ?? [];

// Table of contents from h2 ids (kept identical to the WordPress anchors Google already links to).
preg_match_all('#<h2 id="([^"]+)">(.*?)</h2>#s', $body, $hm, PREG_SET_ORDER);
$toc = array_map(fn($m) => ['id' => $m[1], 'text' => trim(strip_tags($m[2]))], $hm);

// Reader-pick spotlight before the middle H2 (skipped for posts without products).
if ($products && count($hm) >= 4) {
    ob_start(); view('spotlight', ['pr' => $products[0]]); $spot = ob_get_clean();
    $mid = $hm[(int) floor(count($hm) / 2)][0];
    $pos = strpos($body, $mid);
    if ($pos !== false) $body = substr_replace($body, $spot . "\n", $pos, 0);
}
ob_start(); view('products', ['products' => $products]); $prodHtml = ob_get_clean();
$faqHtml = '';
if (!empty($post['faq'])) {
    $faqHtml = '<div class="faq">';
    foreach ($post['faq'] as $i => $f) {
        $faqHtml .= '<details class="faq-item"' . ($i === 0 ? ' open' : '') . '><summary>' . e($f['q']) . '</summary><div class="faq-a"><p>' . $f['a'] . '</p></div></details>';
    }
    $faqHtml .= '</div>';
}
$body = str_replace(['<!--tc:products-->', '<!--tc:faq-->'], [$prodHtml, $faqHtml], $body, $n);
if (!str_contains(post_body($post), '<!--tc:products-->')) {
    $at = strpos($body, '<h2 id="h-faqs"');
    $body = $at === false ? $body . $prodHtml : substr_replace($body, $prodHtml, $at, 0);
}
// Tables scroll on small screens.
$body = preg_replace('#<table>#', '<div class="table-scroll"><table>', $body);
$body = str_replace('</table>', '</table></div>', $body);

$schema = [
    ['@type' => 'BlogPosting', '@id' => SITE_URL . $url . '#article', 'headline' => $post['title'],
     'description' => $post['description'], 'image' => SITE_URL . $post['image'],
     'datePublished' => $post['published'], 'dateModified' => $post['modified'] ?: $post['published'],
     'author' => ['@type' => 'Organization', 'name' => SITE_NAME, 'url' => SITE_URL . '/about-us/'],
     'publisher' => ['@id' => SITE_URL . '/#organization'], 'mainEntityOfPage' => SITE_URL . $url,
     'articleSection' => $post['categories'], 'wordCount' => $post['words'] ?? null, 'inLanguage' => 'en-US'],
    ['@type' => 'BreadcrumbList', 'itemListElement' => [
        ['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => SITE_URL . '/'],
        ['@type' => 'ListItem', 'position' => 2, 'name' => $cat === 'Reflections' ? 'Blog' : $cat, 'item' => SITE_URL . ($cat === 'Reflections' ? '/blog/' : cat_url($cat))],
        ['@type' => 'ListItem', 'position' => 3, 'name' => $post['title']]]],
];
if (!empty($post['faq'])) {
    $schema[] = ['@type' => 'FAQPage', 'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => $f['q'],
        'acceptedAnswer' => ['@type' => 'Answer', 'text' => strip_tags($f['a'])]], $post['faq'])];
}
$srcset = img_srcset($post['image']);
view('head', ['meta' => [
    'title' => $post['seo_title'], 'description' => $post['description'], 'canonical' => $url, 'type' => 'article',
    'image' => $post['image'], 'published' => $post['published'], 'modified' => $post['modified'],
    'schema' => $schema, 'preload' => $post['image'], 'preload_srcset' => $srcset, 'bodyClass' => 'single',
]]);
$all = posts();
$idx = array_search($post['slug'], array_column($all, 'slug'), true);
$newer = $idx > 0 ? $all[$idx - 1] : null;
$older = $all[$idx + 1] ?? null;
?>
<article class="post">
  <header class="post-hero">
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="<?= $cat === 'Reflections' ? '/blog/' : cat_url($cat) ?>"><?= e($cat === 'Reflections' ? 'Blog' : $cat) ?></a></nav>
      <h1 class="post-title"><?= e($post['title']) ?></h1>
      <div class="post-meta">
        <time datetime="<?= e($post['published']) ?>"><?= fmt_date($post['published']) ?></time>
        <?php if (!empty($post['modified']) && substr($post['modified'], 0, 10) !== substr($post['published'], 0, 10)): ?>
          <span>Updated <time datetime="<?= e($post['modified']) ?>"><?= fmt_date($post['modified']) ?></time></span>
        <?php endif; ?>
        <span><?= reading_time($post) ?> min read</span>
        <span class="post-cats"><?php foreach (array_diff($post['categories'], ['General']) as $c): ?><a href="<?= cat_url($c) ?>"><?= e($c) ?></a><?php endforeach; ?></span>
      </div>
    </div>
  </header>
  <div class="wrap post-layout">
    <div class="post-main">
      <figure class="post-figure">
        <img src="<?= e($post['image']) ?>" srcset="<?= e($srcset) ?>" sizes="(max-width: 1100px) 100vw, 760px" width="1536" height="1024" alt="<?= e($post['image_alt']) ?>" fetchpriority="high" decoding="async">
      </figure>
      <div class="prose">
<?= $body ?>
      </div>
      <div class="share" aria-label="Share this article">
        <span>Share this thought</span>
        <?php $su = urlencode(SITE_URL . $url); $st = urlencode($post['title']); ?>
        <a href="https://www.facebook.com/sharer/sharer.php?u=<?= $su ?>" target="_blank" rel="noopener" aria-label="Share on Facebook">Facebook</a>
        <a href="https://twitter.com/intent/tweet?url=<?= $su ?>&amp;text=<?= $st ?>" target="_blank" rel="noopener" aria-label="Share on X">X</a>
        <a href="https://www.pinterest.com/pin/create/button/?url=<?= $su ?>&amp;media=<?= urlencode(SITE_URL . $post['image']) ?>&amp;description=<?= $st ?>" target="_blank" rel="noopener" aria-label="Pin on Pinterest">Pinterest</a>
        <a href="mailto:?subject=<?= rawurlencode($post['title']) ?>&amp;body=<?= $su ?>" aria-label="Share by email">Email</a>
        <button type="button" class="copy-link" data-url="<?= e(SITE_URL . $url) ?>">Copy link</button>
      </div>
      <nav class="post-nav" aria-label="More articles">
        <?php if ($older): ?><a class="prev" href="/<?= e($older['slug']) ?>/"><span>Previous</span><?= e($older['title']) ?></a><?php endif; ?>
        <?php if ($newer): ?><a class="next" href="/<?= e($newer['slug']) ?>/"><span>Next</span><?= e($newer['title']) ?></a><?php endif; ?>
      </nav>
    </div>
    <aside class="post-side">
      <?php if (count($toc) > 2): ?>
      <nav class="toc" aria-label="Contents">
        <h2 class="toc-title">Content</h2>
        <ol><?php foreach ($toc as $t): ?><li><a href="#<?= e($t['id']) ?>"><?= e($t['text']) ?></a></li><?php endforeach; ?></ol>
      </nav>
      <?php endif; ?>
      <?php if ($products): ?>
      <div class="side-shelf">
        <h2 class="toc-title">On the Bookshelf</h2>
        <?php foreach (array_slice($products, 0, 3) as $pr): ?>
          <a href="<?= e(amazon_url($pr)) ?>" rel="sponsored nofollow noopener" target="_blank" data-amz="<?= e($pr['title']) ?>"><span class="book book-xs" style="--h:<?= crc32($pr['title']) % 360 ?>" aria-hidden="true"></span><span><strong><?= e($pr['title']) ?></strong><?php if (!empty($pr['by'])): ?><small><?= e($pr['by']) ?></small><?php endif; ?></span></a>
        <?php endforeach; ?>
        <p class="side-note">Affiliate links · <a href="/recommended-reads/">See all</a></p>
      </div>
      <?php endif; ?>
    </aside>
  </div>
</article>
<section class="related">
  <div class="wrap">
    <h2 class="section-title reveal">Keep Reading</h2>
    <div class="grid grid-3">
      <?php foreach (related_posts($post) as $p) view('card', ['p' => $p]); ?>
    </div>
  </div>
</section>
<?php view('foot'); ?>
