<?php
/** @var string $heading @var string $intro @var array $posts @var bool $filters @var array $crumbs */
$heroTitle = $heading; $heroLede = e($intro); $heroEyebrow = count($posts) . ' articles';
include __DIR__ . '/partials/page-hero.php';
$present = array_unique(array_column($posts, 'topic'));
?>
<section class="section section--tight">
  <div class="wrap">
    <?php if ($filters): ?>
      <div class="filters" data-filters>
        <div class="filters__chips" role="group" aria-label="Filter by topic">
          <button type="button" class="pill is-active" data-filter="all">All</button>
          <?php foreach (TOPICS as $k => [$label]): if (!in_array($k, $present, true)) continue; ?>
            <button type="button" class="pill" data-filter="<?= $k ?>"><?= e($label) ?></button>
          <?php endforeach ?>
        </div>
        <label class="filters__search"><?= icon('search') ?><input type="search" placeholder="Filter articles…" data-filter-search aria-label="Filter articles"></label>
      </div>
    <?php endif ?>
    <?php if ($posts): ?>
      <div class="cards" data-cards>
        <?php foreach (array_values($posts) as $i => $p): ?><?= card($p, $i < 24 ? 'reveal' : 'reveal is-more') ?><?php endforeach ?>
      </div>
      <p class="empty" data-empty hidden>No articles match that filter.</p>
      <?php if (count($posts) > 24): ?><div class="more"><button type="button" class="btn btn--ghost" data-more>Show more articles</button></div><?php endif ?>
    <?php else: ?>
      <p class="empty">Nothing here yet. <a href="/blog/">Browse the whole journal</a>.</p>
    <?php endif ?>
  </div>
</section>
