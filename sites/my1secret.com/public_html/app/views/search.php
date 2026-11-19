<?php defined('M1S') || exit; ?>
<header class="page-head">
  <h1><?= $qText !== '' ? 'Results for “' . e($qText) . '”' : 'Search' ?></h1>
  <form class="search-big" action="/search/" method="get"><input type="search" name="q" value="<?= e($qText) ?>" placeholder="Search guides and discussions" aria-label="Search" autofocus><button class="btn btn-accent">Search</button></form>
</header>
<?php if ($qText !== ''): ?>
<div class="layout">
  <div class="content">
    <section class="block">
      <h2>Guides (<?= count($articles) ?>)</h2>
      <div class="card-grid card-grid-2"><?php foreach ($articles as $a): ?><?= article_card($a) ?><?php endforeach; ?></div>
      <?php if (!$articles): ?><p class="empty">No guides match.</p><?php endif; ?>
    </section>
    <section class="block">
      <h2>Discussions (<?= count($threads) ?>)</h2>
      <div class="feed"><?php foreach ($threads as $t): ?><?= thread_row($t, $votes[(int)$t['id']] ?? 0) ?><?php endforeach; ?></div>
      <?php if (!$threads): ?><p class="empty">No discussions match. <a href="/submit/">Ask the community</a>.</p><?php endif; ?>
    </section>
  </div>
  <aside class="sidebar"><?= communities_widget() ?></aside>
</div>
<?php endif; ?>
