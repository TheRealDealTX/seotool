<?php defined('SNW') || (http_response_code(404) && exit); ?>
<article class="post">
  <header class="post-head">
    <div class="wrap narrow">
      <?php partial('breadcrumbs', ['crumbs' => [['Blog', '/blog/'], [$cat['name'], '/blog/category/' . $post['category'] . '/'], [$post['title'], '']]]) ?>
      <p class="eyebrow"><a href="/blog/category/<?= e($post['category']) ?>/"><?= e($cat['name']) ?></a></p>
      <h1><?= e($post['title']) ?></h1>
      <p class="meta">By <a href="/about-seattle-northwest-homes/"><?= e(cfg('agent')) ?></a> · <time datetime="<?= e($post['date']) ?>"><?= fmt_date($post['date']) ?></time><?= $post['modified'] > $post['date'] ? ' · Updated <time datetime="' . e($post['modified']) . '">' . fmt_date($post['modified']) . '</time>' : '' ?> · <?= reading_time($post['body']) ?> min read</p>
    </div>
  </header>
  <figure class="post-hero wrap">
    <img src="<?= e(post_image($post)) ?>" alt="<?= e($post['image_alt'] ?: $post['title']) ?>" width="1400" height="933" fetchpriority="high">
  </figure>
  <div class="wrap narrow prose post-body">
<?= $post['body'] . "\n" ?>
    <?php partial('faq', ['faq' => $post['faq'] ?? []]) ?>
    <aside class="author-box">
      <img src="/assets/img/brand/logo-square.webp" alt="" width="72" height="72" loading="lazy">
      <div><p><strong>Written by <?= e(cfg('agent')) ?>, <?= e(cfg('name')) ?></strong></p>
      <p class="muted">We help buyers and sellers across Seattle's neighborhoods. Have a question about this article? <a href="/contact-seattle-real-estate-agents/">Get in touch</a>.</p></div>
    </aside>
  </div>
</article>
<section class="section alt">
  <div class="wrap">
    <h2>Keep Reading</h2>
    <div class="grid-3">
<?php foreach ($related as $p) partial('post-card', ['p' => $p]); ?>
    </div>
  </div>
</section>
<?php partial('cta') ?>
