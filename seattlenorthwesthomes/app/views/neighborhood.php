<?php defined('SNW') || (http_response_code(404) && exit);
partial('page-hero', ['title' => $hood['name'] . ' Homes for Sale & Neighborhood Guide', 'image' => photo($hood['image']),
    'crumbs' => [['Neighborhoods', '/neighborhoods/'], [$hood['name'], '']], 'lead' => $hood['area'] . ' · ZIP ' . $hood['zip']]); ?>
<section class="section tight">
  <div class="wrap listing-layout">
    <div class="prose">
      <p class="lead"><?= e($hood['intro']) ?></p>
<?php foreach ($hood['body'] as [$h2, $para]): ?>
      <h2><?= e($h2) ?></h2>
      <p><?= e($para) ?></p>
<?php endforeach ?>
    </div>
    <aside class="sidebar">
      <div class="sticky-card">
        <h2 class="h3"><?= e($hood['name']) ?> Highlights</h2>
        <ul class="checks">
<?php foreach ($hood['highlights'] as $x): ?><li><?= e($x) ?></li><?php endforeach ?>
        </ul>
        <a class="btn btn-accent btn-block" href="/buy-a-home-in-seattle/">Get <?= e($hood['name']) ?> Listing Alerts</a>
      </div>
    </aside>
  </div>
</section>
<section class="section alt">
  <div class="wrap">
    <h2><?= e($hood['name']) ?> Homes for Sale</h2>
<?php if ($homes): ?>
    <div class="grid-3">
<?php foreach ($homes as $l) partial('listing-card', ['l' => $l]); ?>
    </div>
<?php else: ?>
    <p>We don't have a featured home in <?= e($hood['name']) ?> right now. <a href="/buy-a-home-in-seattle/">Tell us what you're looking for</a> and we'll send new <?= e($hood['name']) ?> listings the moment they hit the market.</p>
<?php endif ?>
    <p><a class="link-arrow" href="/homes-for-sale/">Browse all Seattle homes for sale</a></p>
  </div>
</section>
<section class="section">
  <div class="wrap narrow">
    <?php partial('faq', ['faq' => $faq, 'heading' => 'Living in ' . $hood['name'] . ': FAQ']) ?>
<?php if ($posts): ?>
    <h2>Related Reading</h2>
    <ul class="link-list">
<?php foreach ($posts as $p): ?><li><a href="/blog/<?= e($p['slug']) ?>/"><?= e($p['title']) ?></a></li><?php endforeach ?>
    </ul>
<?php endif ?>
    <h2>Explore Nearby Neighborhoods</h2>
    <p class="tag-list">
<?php foreach (neighborhoods() as $s => $h) if ($s !== $slug): ?><a href="/neighborhoods/<?= $s ?>/"><?= e($h['name']) ?></a><?php endif ?>
    </p>
  </div>
</section>
<?php partial('cta', ['title' => 'Selling a home in ' . $hood['name'] . '?', 'text' => 'Get a free pricing review based on recent ' . $hood['name'] . ' sales.']) ?>
