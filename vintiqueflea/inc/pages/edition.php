<?php
defined('INC') || exit;
/** @var string $slug @var array $ed */
page_start([
    'title' => $ed['seo_title'],
    'description' => $ed['description'],
    'path' => "/events/$slug/",
]);
?>
<div class="wrap">
  <?= breadcrumbs([['Events', '/events/'], [$ed['name'], "/events/$slug/"]]) ?>
  <header class="page-head page-head--icon">
    <span class="page-head__icon" aria-hidden="true"><?= $ed['icon'] ?></span>
    <div>
      <h1>Vintique Flea <?= e($ed['name']) ?>: <?= e($ed['season']) ?> vintage market in Houston</h1>
      <p class="lede"><?= e($ed['lede']) ?></p>
    </div>
  </header>
  <div class="layout-2">
    <article class="prose">
      <h2>About the <?= e(strtolower($ed['name'])) ?></h2>
      <p><?= e($ed['history']) ?></p>
      <p>Every edition brings together curated vendors selling <a href="/shop/mid-century-modern/">mid-century modern</a>, <a href="/shop/vintage-clothing/">vintage clothing</a>, <a href="/shop/architectural-salvage-industrial/">architectural salvage and industrial</a> pieces, <a href="/shop/antiques-collectibles/">antiques</a> and <a href="/shop/rustic-home-decor/">rustic home decor</a>, plus <a href="/food-trucks/">local food trucks</a>, beer and wine.</p>
      <h2>Dates for the next <?= e(strtolower($ed['season'])) ?> market</h2>
<?php $match = array_filter(UPCOMING_EVENTS, fn($e) => ($e['season'] ?? '') === strtolower($ed['season'])); ?>
<?php if ($match): $ev = reset($match); ?>
      <p><strong><?= e($ev['name']) ?></strong>: <?= e(implode(' · ', $ev['hours'] ?? [])) ?></p>
<?php else: ?>
      <p>Dates for the next <?= e(strtolower($ed['season'])) ?> edition haven't been announced yet. <a href="/events/">Check the events page</a> or join the list below to hear first.</p>
<?php endif; ?>
      <h2><?= e($ed['season']) ?> shopping tips</h2>
      <ul>
<?php foreach ($ed['tips'] as $t): ?>
        <li><?= e($t) ?></li>
<?php endforeach; ?>
      </ul>
      <h2>Location</h2>
      <p>Silver Street Studios, 2000 Edwards Street, Houston, TX 77007, in the Washington Avenue Arts District. Make a day of it with our <a href="/guides/washington-avenue-arts-district/">Arts District guide</a>.</p>
    </article>
    <aside class="side">
      <div class="side-card">
        <h2>Get the dates</h2>
        <?= newsletter_form('edition-' . $slug) ?>
      </div>
      <div class="side-card">
        <h2>Other editions</h2>
        <ul class="side-links">
<?php foreach (EDITIONS as $s => $o): if ($s === $slug) continue; ?>
          <li><a href="/events/<?= $s ?>/"><?= $o['icon'] ?> <?= e($o['name']) ?></a></li>
<?php endforeach; ?>
        </ul>
      </div>
    </aside>
  </div>
</div>
<?php page_end();
