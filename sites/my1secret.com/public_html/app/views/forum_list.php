<?php defined('M1S') || exit;
$base = $community ? community_url($community) : '/forum/';
?>
<?php if ($community): ?>
<header class="community-head" style="--c:<?= e($community['color']) ?>">
  <div class="community-banner"></div>
  <div class="community-title">
    <span class="community-icon" aria-hidden="true"><?= e(mb_substr($community['name'], 0, 1)) ?></span>
    <div>
      <h1><?= e($community['title']) ?></h1>
      <p class="muted">/forum/<?= e($community['slug']) ?> · <?= plural($total ?? 0, 'post') ?></p>
    </div>
    <a class="btn btn-accent" href="/submit/?c=<?= e($community['slug']) ?>">Create a post</a>
  </div>
</header>
<?php else: ?>
<header class="page-head">
  <h1>Community Forum</h1>
  <p class="lede">Ask questions, share what worked, and vote up the best answers. Pick a community or browse everything below.</p>
</header>
<?php endif; ?>

<div class="layout">
  <div class="content">
    <?= sort_tabs($base, $sort, $t) ?>
    <div class="feed">
      <?php foreach ($threads as $th): ?><?= thread_row($th, $votes[(int)$th['id']] ?? 0, !$community) ?><?php endforeach; ?>
      <?php if (!$threads): ?><p class="empty">Nothing here yet. <a href="/submit/<?= $community ? '?c=' . e($community['slug']) : '' ?>">Start the first discussion.</a></p><?php endif; ?>
    </div>
    <?= pager($page, $hasNext, $base . ($sort !== 'hot' ? '?sort=' . $sort . ($sort === 'top' ? '&t=' . $t : '') : '')) ?>
  </div>
  <aside class="sidebar">
    <?php if ($community): ?>
      <section class="widget">
        <h2>About this community</h2>
        <p><?= e($community['description']) ?></p>
        <a class="btn btn-accent btn-block" href="/submit/?c=<?= e($community['slug']) ?>">Create a post</a>
      </section>
      <?php if (!empty($articles)): ?>
        <section class="widget">
          <h2>Related guides</h2>
          <?php foreach ($articles as $a): ?><?= article_card($a, 'sm') ?><?php endforeach; ?>
          <a href="<?= e(topic_url($topicSlug)) ?>">More guides →</a>
        </section>
      <?php endif; ?>
      <section class="widget">
        <h2>Community rules</h2>
        <ol class="rules"><li>Be kind and useful.</li><li>No spam or self-promotion.</li><li>Protect everyone's privacy.</li><li>Posts are opinions, not professional advice.</li></ol>
        <a href="/community-guidelines/">Full guidelines →</a>
      </section>
      <?= communities_widget($community['slug']) ?>
    <?php else: ?>
      <?= communities_widget(null, $counts ?? []) ?>
      <?= topics_widget() ?>
    <?php endif; ?>
  </aside>
</div>
