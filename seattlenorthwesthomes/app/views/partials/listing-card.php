<?php defined('SNW') || (http_response_code(404) && exit); $h = neighborhoods()[$l['neighborhood']]; ?>
<article class="card listing-card">
  <a class="card-media" href="/homes-for-sale/<?= e($l['slug']) ?>/">
    <img src="<?= photo($l['images'][0], true) ?>" alt="<?= e($l['title']) ?> in <?= e($h['name']) ?>, Seattle" width="720" height="480" loading="lazy" decoding="async">
    <span class="badge badge-<?= e(strtolower(str_replace(' ', '-', $l['status']))) ?>"><?= e($l['status']) ?></span>
  </a>
  <div class="card-body">
    <p class="price"><?= money($l['price']) ?></p>
    <h3 class="card-title"><a href="/homes-for-sale/<?= e($l['slug']) ?>/"><?= e($l['title']) ?></a></h3>
    <p class="facts"><span><?= $l['beds'] ?> bd</span><span><?= fmt_baths($l['baths']) ?> ba</span><span><?= number_format($l['sqft']) ?> sq ft</span></p>
    <p class="loc"><?= e($h['name']) ?>, Seattle, WA <?= e($l['zip']) ?> · <?= e($l['type']) ?></p>
  </div>
</article>
