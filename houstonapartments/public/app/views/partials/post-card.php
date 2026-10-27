<?php
// Blog post card. Expects $post from content('posts'); $i optional index.
defined('HA_ROOT') || exit;
?>
<article class="post-card reveal d<?= ($i ?? 0) % 3 ?>">
  <a class="post-media" href="<?= e($post['path']) ?>" tabindex="-1" aria-hidden="true">
    <img src="<?= e($post['image'] ?: '/assets/img/og-default.png') ?>" alt="" loading="lazy" width="600" height="340">
  </a>
  <div class="post-body">
    <time datetime="<?= e(substr($post['date'], 0, 10)) ?>"><?= date('M j, Y', strtotime($post['date'])) ?></time>
    <h3><a href="<?= e($post['path']) ?>"><?= e($post['title']) ?></a></h3>
    <p><?= e(mb_strimwidth($post['description'] ?: $post['excerpt'], 0, 150, '…')) ?></p>
  </div>
</article>
