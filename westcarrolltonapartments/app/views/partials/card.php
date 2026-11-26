<?php defined('WCA') || exit; /** @var array $l */ $j = listing_public_json($l); ?>
<article class="card listing-card" data-id="<?= (int)$l['id'] ?>" data-json="<?= e(json_encode($j)) ?>">
  <a class="card-img" href="<?= e($l['url']) ?>">
    <img src="<?= e(photo_url($l['photos'][0], true)) ?>" alt="<?= e($l['name']) ?> in <?= e($l['city']) ?>, OH" loading="lazy" width="640" height="427">
    <?php if ($l['paid_featured']): ?><span class="badge badge-featured">★ Featured</span><?php elseif ($l['claimed']): ?><span class="badge badge-verified">✓ Verified owner</span><?php elseif ($l['featured']): ?><span class="badge">Popular</span><?php endif; ?>
    <?php if (!$l['has_photos']): ?><span class="photo-pending">📷 Photos coming soon</span><?php endif; ?>
  </a>
  <button class="fav-btn" type="button" data-fav="<?= (int)$l['id'] ?>" aria-label="Save <?= e($l['name']) ?>" aria-pressed="false">♥</button>
  <div class="card-body">
    <h3><a href="<?= e($l['url']) ?>"><?= e($l['name']) ?></a></h3>
    <p class="muted addr"><?= e($l['address']) ?>, <?= e($l['city']) ?></p>
    <p class="price"><?= e(rent_label($l)) ?></p>
    <ul class="chips">
      <li><?= e(beds_label($l)) ?></li>
      <li><?= e(pets_label($l)) ?></li>
      <?php if ($l['income_restricted']): ?><li>Income-based</li><?php endif; ?>
      <?php if ($l['age_restriction']): ?><li><?= e($l['age_restriction']) ?></li><?php endif; ?>
    </ul>
    <label class="compare-check"><input type="checkbox" data-compare="<?= (int)$l['id'] ?>"> Compare</label>
  </div>
</article>
