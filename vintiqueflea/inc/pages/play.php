<?php
page_start([
    'title' => 'Free Vintage Games & Design Tools | Play at Vintique Flea',
    'description' => 'Play free vintage-themed games: guess the decade, haggle with a flea market vendor, design a mid-century room, find your vintage style and more.',
    'path' => '/play/',
]);
$items = [];
$i = 1;
foreach (GAMES as $slug => $g) {
    $items[] = ['@type' => 'ListItem', 'position' => $i++, 'url' => abs_url("/play/$slug/"), 'name' => $g['name']];
}
add_schema(['@type' => 'ItemList', 'name' => 'Vintique Flea games', 'itemListElement' => $items]);
?>
<div class="wrap">
  <?= breadcrumbs([['Play', '/play/']]) ?>
  <header class="page-head">
    <h1>Play around: vintage games &amp; tools</h1>
    <p class="lede">Waiting for the next market? Sharpen your treasure-hunting skills with these free browser games. No sign-up, no downloads, just retro fun on any device.</p>
  </header>
  <div class="game-grid game-grid--big">
<?php foreach (GAMES as $slug => $g): ?>
    <a class="game-card" href="/play/<?= $slug ?>/">
      <span class="game-card__icon" aria-hidden="true"><?= $g['icon'] ?></span>
      <span class="game-card__name"><?= e($g['name']) ?></span>
      <span class="game-card__blurb"><?= e($g['blurb']) ?></span>
      <span class="btn btn--small btn--primary">Play now</span>
    </a>
<?php endforeach; ?>
    <a class="game-card" href="/#wheel-spin">
      <span class="game-card__icon" aria-hidden="true">🎡</span>
      <span class="game-card__name">Treasure Wheel</span>
      <span class="game-card__blurb">Spin for a random curated find, right on our homepage.</span>
      <span class="btn btn--small btn--primary">Spin it</span>
    </a>
  </div>
</div>
<?php page_end();
