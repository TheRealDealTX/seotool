<?php defined('M1S') || exit; ?>
<header class="page-head">
  <h1><?= e($heading) ?></h1>
  <?php if ($intro): ?><p class="lede"><?= e($intro) ?></p><?php endif; ?>
  <nav class="topic-tabs" aria-label="Topics">
    <a href="/blog/"<?= $activeTopic === null && $base === '/blog/' ? ' aria-current="page"' : '' ?>>All</a>
    <?php foreach (topics() as $t): ?><a href="<?= e(topic_url($t)) ?>"<?= $activeTopic === $t['slug'] ? ' aria-current="page"' : '' ?>><?= e($t['name']) ?></a><?php endforeach; ?>
  </nav>
</header>
<div class="layout">
  <div class="content">
    <div class="card-grid card-grid-2">
      <?php foreach ($articles as $a): ?><?= article_card($a) ?><?php endforeach; ?>
    </div>
    <?php if (!$articles): ?><p class="empty">No articles here yet.</p><?php endif; ?>
    <?= pager($page, $hasNext, $base) ?>
  </div>
  <aside class="sidebar">
    <?php if (!empty($community)): ?>
      <section class="widget widget-accent">
        <h2>Discuss it in <?= e($community['name']) ?></h2>
        <p><?= e($community['description']) ?></p>
        <a class="btn btn-accent btn-block" href="<?= e(community_url($community)) ?>">Visit the community</a>
      </section>
    <?php endif; ?>
    <?= topics_widget($activeTopic) ?>
    <?= communities_widget() ?>
  </aside>
</div>
