<?php defined('SNW') || (http_response_code(404) && exit); $c = categories()[$p['category']] ?? ['name' => 'Articles']; ?>
<article class="card post-card">
  <a class="card-media" href="/blog/<?= e($p['slug']) ?>/">
    <img src="<?= e(post_image($p, true)) ?>" alt="<?= e($p['image_alt'] ?: $p['title']) ?>" width="720" height="480" loading="lazy" decoding="async">
  </a>
  <div class="card-body">
    <p class="eyebrow"><a href="/blog/category/<?= e($p['category']) ?>/"><?= e($c['name']) ?></a></p>
    <h3 class="card-title"><a href="/blog/<?= e($p['slug']) ?>/"><?= e($p['title']) ?></a></h3>
    <p class="muted"><?= e(excerpt($p['description'], 120)) ?></p>
    <p class="meta"><time datetime="<?= e($p['date']) ?>"><?= fmt_date($p['date']) ?></time> · <?= reading_time($p['body']) ?> min read</p>
  </div>
</article>
