<?php
// Renders one blog post. Each post folder sets $slug and includes this file.
require_once __DIR__ . '/config.php';

$post = get_post($slug ?? '');
if (!$post) {
    http_response_code(404);
    require __DIR__ . '/404.php';
    return;
}

// Build the table of contents from h2 ids in the body
preg_match_all('#<h2 id="([^"]+)">(.*?)</h2>#s', $post['body'], $m, PREG_SET_ORDER);
$toc = array_map(fn($x) => ['id' => $x[1], 'text' => trim(strip_tags($x[2]))], $m);

$url = base_url() . post_url($post);
$schema = [
    [
        '@type' => 'BlogPosting',
        '@id' => $url . '#article',
        'headline' => $post['title'],
        'description' => $post['description'],
        'image' => base_url() . '/assets/img/' . $post['image'],
        'datePublished' => $post['date'],
        'dateModified' => $post['updated'] ?? $post['date'],
        'author' => ['@type' => 'Organization', 'name' => $post['author'], 'url' => base_url() . '/about/'],
        'publisher' => ['@id' => base_url() . '/#org'],
        'mainEntityOfPage' => $url,
        'keywords' => $post['keyword'],
    ],
    [
        '@type' => 'BreadcrumbList',
        'itemListElement' => [
            ['@type' => 'ListItem', 'position' => 1, 'name' => 'Home', 'item' => base_url() . '/'],
            ['@type' => 'ListItem', 'position' => 2, 'name' => 'Insurance Adjuster Advice', 'item' => base_url() . BLOG_BASE],
            ['@type' => 'ListItem', 'position' => 3, 'name' => $post['title'], 'item' => $url],
        ],
    ],
];
if (!empty($post['faqs'])) {
    $schema[] = [
        '@type' => 'FAQPage',
        'mainEntity' => array_map(fn($f) => ['@type' => 'Question', 'name' => $f['q'], 'acceptedAnswer' => ['@type' => 'Answer', 'text' => $f['a']]], $post['faqs']),
    ];
}

$page = [
    'title' => $post['meta_title'] ?? $post['title'],
    'description' => $post['description'],
    'path' => post_url($post),
    'image' => $post['image'],
    'type' => 'article',
    'published' => $post['date'],
    'modified' => $post['updated'] ?? $post['date'],
    'schema' => $schema,
    'body_class' => 'has-hero',
];

// Related: same category first, then newest others
$related = array_filter(all_posts(), fn($p) => $p['slug'] !== $post['slug']);
uasort($related, fn($a, $b) => (($b['category'] === $post['category']) <=> ($a['category'] === $post['category'])) ?: strcmp($b['date'], $a['date']));
$related = array_slice($related, 0, 3);

require __DIR__ . '/header.php';
?>
<section class="page-hero article-hero">
  <div class="hero-media"><img src="/assets/img/<?= e($post['image']) ?>" alt="" width="1200" height="675"></div>
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span>/</span><a href="<?= BLOG_BASE ?>">Insurance Adjuster Advice</a><span>/</span><?= e($post['category']) ?></nav>
    <span class="chip"><?= e($post['category']) ?></span>
    <h1 style="margin-top:14px"><?= e($post['title']) ?></h1>
    <div class="article-meta">
      <span><?= icon('user', 16) ?> <?= e($post['author']) ?></span>
      <span><?= icon('clock', 16) ?> <?= (int) $post['read_time'] ?> min read</span>
      <span>Published <time datetime="<?= e($post['date']) ?>"><?= e(fmt_date($post['date'])) ?></time></span>
<?php if (!empty($post['updated']) && $post['updated'] !== $post['date']): ?>
      <span>Updated <time datetime="<?= e($post['updated']) ?>"><?= e(fmt_date($post['updated'])) ?></time></span>
<?php endif; ?>
    </div>
  </div>
</section>

<div class="container article-cover reveal">
  <img src="/assets/img/<?= e($post['image']) ?>" alt="<?= e($post['image_alt']) ?>" width="1200" height="675">
</div>

<div class="container article-layout">
  <aside class="toc" aria-label="Table of contents">
    <h2>On this page</h2>
    <ol>
<?php foreach ($toc as $t): ?>
      <li><a href="#<?= e($t['id']) ?>"><?= e($t['text']) ?></a></li>
<?php endforeach; ?>
<?php if (!empty($post['faqs'])): ?>
      <li><a href="#faq">FAQs</a></li>
<?php endif; ?>
    </ol>
    <div class="card" style="margin-top:28px;padding:22px">
      <div class="icon-wrap" style="margin-bottom:12px"><?= icon('calc', 22) ?></div>
      <h3 style="font-size:1.05rem">Estimate your pay</h3>
      <p style="font-size:.9rem">Try the free adjuster salary calculator.</p>
      <a class="btn btn-gold btn-sm" href="/salary-calculator/">Open calculator</a>
    </div>
    <div class="card card-dark" style="margin-top:18px;padding:22px">
      <div class="icon-wrap" style="margin-bottom:12px"><?= icon('star', 22) ?></div>
      <h3 style="font-size:1.05rem;color:#fff">Get your Texas license</h3>
      <p style="font-size:.9rem">Licensed in about a week with an online course.</p>
      <?= cert_btn('btn btn-gold btn-sm', 'Get Certified') ?>
    </div>
  </aside>
  <article class="prose">
    <?= $post['body'] ?>

<?php if (!empty($post['faqs'])): ?>
    <h2 id="faq">Frequently asked questions</h2>
    <div class="faq">
<?php foreach ($post['faqs'] as $f): ?>
      <details><summary><?= e($f['q']) ?></summary><div class="faq-a"><p><?= e($f['a']) ?></p></div></details>
<?php endforeach; ?>
    </div>
<?php endif; ?>

    <div class="author-box">
      <span class="brand-mark"><?= icon('shield', 26) ?></span>
      <p><strong><?= e($post['author']) ?></strong><br>We research insurance adjuster salary data, fee schedules and licensing rules so new and working adjusters can make better career decisions. Figures are estimates and not job offers.</p>
    </div>
  </article>
</div>

<?php if ($related): ?>
<section class="section section-soft">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Keep reading</span><h2>Related salary guides</h2></div>
    <div class="post-grid">
<?php foreach ($related as $p) echo post_card($p); ?>
    </div>
  </div>
</section>
<?php endif; ?>

<?= course_cta() ?>
<?php require __DIR__ . '/footer.php'; ?>
