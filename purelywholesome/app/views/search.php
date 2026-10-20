<?php /** @var string $q @var array $results */
$crumbs = [['Home', '/'], ['Search', '/']];
$heroTitle = $q === '' ? 'Search' : 'Results for “' . $q . '”';
$heroLede = $q === '' ? 'Search every recipe, guide and tool.' : count($results) . ' article' . (count($results) === 1 ? '' : 's') . ' found.';
include __DIR__ . '/partials/page-hero.php'; ?>
<section class="section section--tight">
  <div class="wrap">
    <form class="hero__search hero__search--page" action="/" method="get" role="search"><?= icon('search') ?><input type="search" name="s" value="<?= e($q) ?>" aria-label="Search"><button class="btn btn--primary" type="submit">Search</button></form>
    <?php if ($results): ?>
      <div class="cards"><?php foreach (array_slice($results, 0, 36) as $p): ?><?= card($p) ?><?php endforeach ?></div>
    <?php elseif ($q !== ''): ?>
      <p class="empty">Nothing matched. Try a simpler word like “lamb”, “brine”, “goat” or “eggs”, or <a href="/blog/">browse the journal</a>.</p>
    <?php endif ?>
  </div>
</section>
