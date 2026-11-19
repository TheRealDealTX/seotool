<?php
/** @var string $slug @var array $game */
page_start([
    'title' => $game['seo_title'],
    'description' => $game['description'],
    'path' => "/play/$slug/",
    'css' => ['/assets/css/games.css'],
    'js' => ["/assets/js/games/$slug.js"],
    'body_class' => 'game-page',
]);
add_schema([
    '@type' => 'WebApplication',
    'name' => $game['name'],
    'url' => abs_url("/play/$slug/"),
    'description' => $game['description'],
    'applicationCategory' => 'GameApplication',
    'operatingSystem' => 'Any (web browser)',
    'isAccessibleForFree' => true,
    'offers' => ['@type' => 'Offer', 'price' => 0, 'priceCurrency' => 'USD'],
    'publisher' => ['@id' => SITE_URL . '/#org'],
]);
?>
<div class="wrap">
  <?= breadcrumbs([['Play', '/play/'], [$game['name'], "/play/$slug/"]]) ?>
  <header class="page-head page-head--icon page-head--compact">
    <span class="page-head__icon" aria-hidden="true"><?= $game['icon'] ?></span>
    <div>
      <h1><?= e($game['name']) ?></h1>
      <p class="lede"><?= e($game['how']) ?></p>
    </div>
  </header>
  <div id="game-root" class="game" data-game="<?= e($slug) ?>">
    <noscript><p class="notice">This game needs JavaScript turned on.</p></noscript>
  </div>
  <section class="section section--tight">
    <h2>More games</h2>
    <div class="game-grid">
<?php foreach (GAMES as $s => $g): if ($s === $slug) continue; ?>
      <a class="game-card" href="/play/<?= $s ?>/">
        <span class="game-card__icon" aria-hidden="true"><?= $g['icon'] ?></span>
        <span class="game-card__name"><?= e($g['name']) ?></span>
        <span class="game-card__blurb"><?= e($g['blurb']) ?></span>
      </a>
<?php endforeach; ?>
    </div>
  </section>
  <?= disclosure() ?>
</div>
<?php page_end();
