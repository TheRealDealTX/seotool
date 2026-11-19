<?php defined('SNW') || (http_response_code(404) && exit);
$crumbs = [['Homes for Sale', '/homes-for-sale/'], [$hood['name'], '/neighborhoods/' . $l['neighborhood'] . '/'], [$l['title'], '']]; ?>
<section class="listing-top">
  <div class="wrap">
    <?php partial('breadcrumbs', ['crumbs' => $crumbs]) ?>
    <div class="listing-head">
      <div>
        <span class="badge badge-<?= e(strtolower(str_replace(' ', '-', $l['status']))) ?>"><?= e($l['status']) ?></span>
        <h1><?= e($l['title']) ?></h1>
        <p class="loc"><?= e($hood['name']) ?>, Seattle, WA <?= e($l['zip']) ?></p>
      </div>
      <div class="listing-price">
        <p class="price big"><?= money($l['price']) ?></p>
        <p class="facts"><span><strong><?= $l['beds'] ?></strong> beds</span><span><strong><?= fmt_baths($l['baths']) ?></strong> baths</span><span><strong><?= number_format($l['sqft']) ?></strong> sq ft</span></p>
      </div>
    </div>
    <div class="gallery" data-gallery>
<?php foreach ($l['images'] as $i => $img): ?>
      <a href="<?= photo($img) ?>" class="g<?= $i ?>" data-index="<?= $i ?>"><img src="<?= photo($img, $i > 0) ?>" alt="<?= e($l['title']) ?> — photo <?= $i + 1 ?>" width="<?= $i ? 720 : 1400 ?>" height="<?= $i ? 480 : 933 ?>"<?= $i ? ' loading="lazy"' : ' fetchpriority="high"' ?> decoding="async"></a>
<?php endforeach ?>
    </div>
  </div>
</section>
<section class="section tight">
  <div class="wrap listing-layout">
    <div class="prose">
      <p class="lead"><?= e($l['summary']) ?></p>
<?php foreach ($l['description'] as $para): ?>
      <p><?= e($para) ?></p>
<?php endforeach ?>
      <h2>Home Features</h2>
      <ul class="checks cols-2">
<?php foreach ($l['features'] as $ft): ?><li><?= e($ft) ?></li><?php endforeach ?>
      </ul>
      <h2>Property Details</h2>
      <table class="details">
        <tbody>
          <tr><th scope="row">Price</th><td><?= money($l['price']) ?></td><th scope="row">Status</th><td><?= e($l['status']) ?></td></tr>
          <tr><th scope="row">Property type</th><td><?= e($l['type']) ?></td><th scope="row">Year built</th><td><?= $l['year'] ?></td></tr>
          <tr><th scope="row">Bedrooms</th><td><?= $l['beds'] ?></td><th scope="row">Bathrooms</th><td><?= fmt_baths($l['baths']) ?></td></tr>
          <tr><th scope="row">Interior</th><td><?= number_format($l['sqft']) ?> sq ft</td><th scope="row">Lot size</th><td><?= $l['lot'] ? number_format($l['lot']) . ' sq ft' : '—' ?></td></tr>
          <tr><th scope="row">Price / sq ft</th><td><?= money((int) round($l['price'] / $l['sqft'])) ?></td><th scope="row">HOA dues</th><td><?= $l['hoa'] ? money($l['hoa']) . '/mo' : 'None' ?></td></tr>
          <tr><th scope="row">Parking</th><td><?= e($l['parking']) ?></td><th scope="row">Heating / cooling</th><td><?= e($l['heating']) ?></td></tr>
          <tr><th scope="row">Neighborhood</th><td><a href="/neighborhoods/<?= e($l['neighborhood']) ?>/"><?= e($hood['name']) ?></a></td><th scope="row">ZIP code</th><td><?= e($l['zip']) ?></td></tr>
        </tbody>
      </table>
      <h2>About <?= e($hood['name']) ?></h2>
      <p><?= e($hood['intro']) ?></p>
      <p><a class="link-arrow" href="/neighborhoods/<?= e($l['neighborhood']) ?>/">Read our <?= e($hood['name']) ?> neighborhood guide</a></p>
<?php if (cfg('listing_note')): ?><p class="disclaimer"><?= e(cfg('listing_note')) ?><?= cfg('brokerage') ? ' Presented by ' . e(cfg('brokerage')) . '.' : '' ?></p><?php endif ?>
    </div>
    <aside class="sidebar">
      <div class="sticky-card">
        <h2 class="h3"><?= $l['status'] === 'Sold' ? 'Want a home like this?' : 'Interested in this home?' ?></h2>
        <p class="muted">Ask a question or schedule a private tour.</p>
        <?php partial('form-showing', ['l' => $l]) ?>
      </div>
    </aside>
  </div>
</section>
<?php if ($similar): ?>
<section class="section alt">
  <div class="wrap">
    <h2>Similar Homes for Sale</h2>
    <div class="grid-3">
<?php foreach ($similar as $s) partial('listing-card', ['l' => $s]); ?>
    </div>
  </div>
</section>
<?php endif ?>
<?php partial('cta', ['title' => 'Thinking about selling in ' . $hood['name'] . '?', 'text' => 'Find out what your home could sell for with a free, no-obligation pricing review.']) ?>
