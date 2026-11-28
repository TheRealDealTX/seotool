<a class="post-card reveal" href="/blog/<?= e($a['slug']) ?>">
  <div class="pc-img"><?= photo($a['hero'], $a['hero_alt'] ?? $a['title'], '', true, '(max-width: 640px) 100vw, 380px') ?></div>
  <div class="pc-body">
    <div class="pc-meta"><span class="chip"><?= e($a['category']) ?></span><span><?= e(date('M j, Y', strtotime($a['date']))) ?></span><span><?= read_time($a['body']) ?> min read</span></div>
    <h3><?= e($a['title']) ?></h3>
    <p><?= e($a['excerpt'] ?? '') ?></p>
  </div>
</a>
