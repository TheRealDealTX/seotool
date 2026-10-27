<?php
// Listing card. Expects $c from Listings::card(); $i optional index.
defined('HA_ROOT') || exit;
$photos = $c['photos'] ?: ['/assets/img/Houston-High-Rise.webp'];
?>
<article class="card tilt" data-id="<?= $c['id'] ?>">
  <a class="card-media" href="<?= e($c['url']) ?>" tabindex="-1" aria-hidden="true">
    <div class="card-slides">
      <?php foreach ($photos as $k => $src): ?>
        <img src="<?= e($src) ?>" alt="" loading="lazy" decoding="async" width="600" height="400"<?= $k ? ' class="later"' : '' ?>>
      <?php endforeach ?>
    </div>
    <?php if (count($photos) > 1): ?><span class="card-dots"><?php foreach ($photos as $k => $_): ?><i<?= $k ? '' : ' class="on"' ?>></i><?php endforeach ?></span><?php endif ?>
    <span class="card-badges">
      <?php if ($c['new']): ?><span class="badge badge-new">New build</span><?php endif ?>
      <?php if ($c['special']): ?><span class="badge badge-hot">Special</span><?php endif ?>
      <?php if ($c['pets']): ?><span class="badge">Pet friendly</span><?php endif ?>
    </span>
  </a>
  <button class="fav" type="button" aria-label="Save <?= e($c['name']) ?>" aria-pressed="false" data-fav="<?= $c['id'] ?>">♥</button>
  <div class="card-body">
    <h3 class="card-title"><a href="<?= e($c['url']) ?>"><?= e($c['name']) ?></a></h3>
    <p class="card-addr"><?= e($c['address']) ?></p>
    <p class="card-meta"><span><?= e($c['beds']) ?></span><?php if ($c['sqft']): ?><span><?= e($c['sqft']) ?></span><?php endif ?><?php if ($c['rating']): ?><span class="stars">★ <?= e($c['rating']) ?></span><?php endif ?></p>
    <p class="card-price"><?= e($c['price']) ?></p>
  </div>
</article>
