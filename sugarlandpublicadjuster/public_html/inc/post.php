<?php
/**
 * Blog post template. A post's directory holds a two-line index.php that sets
 * $slug and requires this file.
 */
require_once __DIR__ . '/layout.php';

$post = find_post($slug);
if (!$post) {
    http_response_code(404);
    require dirname(__DIR__) . '/404.php';
    exit;
}

$path = '/' . $post['slug'] . '/';
$body = file_get_contents(dirname(__DIR__) . '/content/posts/' . $post['slug'] . '.html');

// Give every H2 an id and build the table of contents.
$toc = [];
$body = preg_replace_callback('#<h2>(.*?)</h2>#s', function ($m) use (&$toc) {
    $text = trim(strip_tags($m[1]));
    $id = trim(preg_replace('#[^a-z0-9]+#', '-', strtolower(html_entity_decode($text, ENT_QUOTES))), '-');
    $toc[] = [$id, $text];
    return '<h2 id="' . $id . '">' . $m[1] . '</h2>';
}, $body);

// FAQ schema from the <details class="faq-item"> blocks in the body.
$faqs = [];
if (preg_match_all('#<details class="faq-item"><summary>(.*?)</summary>(.*?)</details>#s', $body, $mm, PREG_SET_ORDER)) {
    foreach ($mm as $f) {
        $faqs[] = [html_entity_decode(strip_tags($f[1]), ENT_QUOTES), $f[2]];
    }
}

// Inject a mid-article call-to-action after the third H2.
$cta = '<div class="inline-cta"><p><strong>Dealing with a claim right now?</strong> A licensed Sugar Land public adjuster can review your estimate for free.</p><a class="btn btn-primary" href="tel:' . SITE['phone_href'] . '">Call ' . e(SITE['phone_display']) . '</a> <button type="button" class="btn btn-outline" data-open-popup>Request a Review</button></div>';
$n = 0;
$body = preg_replace_callback('#<h2 id=#', function ($m) use (&$n, $cta) {
    $n++;
    return ($n === 3 ? $cta : '') . $m[0];
}, $body);

// Featured image: prefer the 1024px WordPress rendition when it exists.
$root = dirname(__DIR__);
$featured = preg_replace('#\.webp$#', '-1024x683.webp', $post['image']);
if (!is_file($root . $featured)) {
    $featured = $post['image'];
}
[$fw, $fh] = @getimagesize($root . $featured) ?: [1024, 683];

$words = str_word_count(strip_tags($body));
$minutes = max(1, (int) round($words / 230));
$o = SITE['origin'];

$schema = [[
    '@type' => 'BlogPosting',
    '@id' => $o . $path . '#article',
    'headline' => $post['title'],
    'description' => $post['description'],
    'image' => abs_url($post['image']),
    'datePublished' => $post['date'],
    'dateModified' => $post['modified'],
    'wordCount' => $words,
    'author' => ['@id' => $o . '/#joseph-dittman'],
    'publisher' => ['@id' => $o . '/#business'],
    'mainEntityOfPage' => ['@id' => $o . $path . '#webpage'],
    'articleSection' => 'General',
    'inLanguage' => 'en-US',
]];
if ($faqs) {
    $schema[] = faq_schema($faqs, $path);
}

$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$post['title'], $path]];
page_start([
    'title' => $post['seo_title'],
    'description' => $post['description'],
    'path' => $path,
    'type' => 'article',
    'image' => $post['image'],
    'published' => $post['date'],
    'modified' => $post['modified'],
    'author' => AUTHOR['name'],
    'breadcrumbs' => $crumbs,
    'schema' => $schema,
    'body_class' => 'single-post',
]);
?>
<section class="page-hero post-hero">
  <div class="container narrow">
    <?php breadcrumb_nav($crumbs); ?>
    <p class="eyebrow"><a href="/category/general/">General</a></p>
    <h1><?= e($post['title']) ?></h1>
    <div class="byline">
      <img src="<?= e(AUTHOR['image']) ?>" alt="Joseph Dittman" width="48" height="48">
      <div>
        <span>By <a href="<?= e(AUTHOR['url']) ?>" rel="author"><?= e(AUTHOR['name']) ?></a>, <?= e(AUTHOR['title']) ?></span>
        <span class="byline-meta">Published <time datetime="<?= e(substr($post['date'], 0, 10)) ?>"><?= e(date('F j, Y', strtotime($post['date']))) ?></time>
        <?php if (substr($post['modified'], 0, 10) !== substr($post['date'], 0, 10)): ?> &middot; Updated <time datetime="<?= e(substr($post['modified'], 0, 10)) ?>"><?= e(date('F j, Y', strtotime($post['modified']))) ?></time><?php endif; ?>
        &middot; <?= $minutes ?> min read</span>
      </div>
    </div>
  </div>
</section>

<div class="container post-layout">
  <article class="post-body prose">
    <figure class="post-featured">
      <img src="<?= e($featured) ?>" alt="<?= e($post['title']) ?>" width="<?= $fw ?>" height="<?= $fh ?>" fetchpriority="high">
    </figure>
<?php if (count($toc) > 3): ?>
    <nav class="toc" aria-label="In this article">
      <p class="toc-title">In this article</p>
      <ol>
<?php foreach ($toc as [$id, $text]): ?>
        <li><a href="#<?= e($id) ?>"><?= e($text) ?></a></li>
<?php endforeach; ?>
      </ol>
    </nav>
<?php endif; ?>
<?= $body ?>

    <?php author_box(); ?>
  </article>
  <?php sidebar_cta(); ?>
</div>

<section class="section section-alt">
  <div class="container">
    <h2 class="section-title">More from the Sugar Land Public Adjuster blog</h2>
    <div class="post-grid">
<?php $shown = 0; foreach (POSTS as $p) { if ($p['slug'] === $post['slug'] || $shown >= 3) continue; post_card($p); $shown++; } ?>
    </div>
  </div>
</section>
<?php page_end(); ?>
