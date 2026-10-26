<?php
/** Blog post template. Expects $slug; included from /blog/<slug>/index.php. */
require_once dirname(__DIR__) . '/bootstrap.php';
$b = $POSTS[$slug];
$path = "/blog/$slug/";
$crumbs = [['Home', '/'], ['Blog', '/blog/'], [$b['h1'], $path]];

page_start([
    'title'       => $b['title'],
    'description' => $b['description'],
    'path'        => $path,
    'image'       => $b['image'],
    'type'        => 'article',
    'published'   => $b['date'],
    'body'        => 'page-post',
    'schema'      => [
        [
            '@type'            => 'BlogPosting',
            'headline'         => $b['h1'],
            'description'      => $b['description'],
            'image'            => abs_url(img($b['image'])),
            'datePublished'    => $b['date'],
            'dateModified'     => $b['date'],
            'mainEntityOfPage' => abs_url($path),
            'author'           => ['@type' => 'Organization', 'name' => SITE['name'], 'url' => abs_url('/')],
            'publisher'        => ['@id' => abs_url('/#business')],
        ],
        breadcrumb_schema($crumbs),
        faq_schema($b['faqs']),
    ],
]);
page_hero('Bastrop Roofing Blog · ' . $b['minutes'] . ' min read', $b['h1'], $b['excerpt'], $crumbs, $b['image'], [['More roofing guides', '/blog/']]);
?>
<section class="section">
  <div class="container with-sidebar">
    <article class="prose">
      <p class="post-meta"><?= icon('clock') ?> Published <time datetime="<?= e($b['date']) ?>"><?= fmt_date($b['date']) ?></time> by Bastrop Roofing</p>
      <figure class="prose-figure"><img src="<?= img($b['image']) ?>" alt="<?= e($b['h1']) ?>" width="1200" height="655" loading="lazy"></figure>
      <?= $b['html'] ?>
    </article>
    <?php sidebar(); ?>
  </div>
</section>
<?php faq_block($b['faqs'], 'Quick Answers'); ?>
<section class="section section-tint">
  <div class="container">
    <div class="section-head reveal"><span class="eyebrow">Keep reading</span><h2 class="section-title small">More Roofing Guides for Bastrop Homeowners</h2></div>
    <div class="card-grid card-grid-3">
<?php $n = 0; foreach ($POSTS as $k => $p): if ($k === $slug || $n++ >= 3) continue; ?>
      <a class="post-card reveal" href="/blog/<?= $k ?>/">
        <img src="<?= img($p['image']) ?>" alt="" width="1200" height="655" loading="lazy">
        <span class="post-card-body"><small><?= fmt_date($p['date']) ?></small><strong><?= e($p['h1']) ?></strong></span>
      </a>
<?php endforeach; ?>
    </div>
  </div>
</section>
<?php
cta_band();
page_end();
