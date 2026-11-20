<?php defined('WCA') || exit;
$addPhotosUrl = $l['claimed'] ? '/account/listings/edit/?id=' . (int)$l['id'] : '/claim/' . $l['slug'] . '/';
$landmarks = [
    ['Downtown Dayton', 39.7589, -84.1916], ['Cox Arboretum MetroPark', 39.6487, -84.2229], ['Dayton Mall', 39.6326, -84.2215],
    ['Wilson Park', 39.6625, -84.2370], ['Austin Landing', 39.5945, -84.2266], ['Wright-Patterson AFB', 39.7900, -84.0900],
];
$dist = function ($a, $b, $c, $d) {
    $r = 3958.8; $p = M_PI / 180;
    $x = sin(($c - $a) * $p / 2) ** 2 + cos($a * $p) * cos($c * $p) * sin(($d - $b) * $p / 2) ** 2;
    return 2 * $r * asin(sqrt($x));
};
$facts = array_filter([
    'Rent' => rent_label($l), 'Bedrooms' => beds_label($l), 'Bathrooms' => $l['baths'], 'Size' => sqft_label($l),
    'Property type' => LISTING_TYPES[$l['type']] ?? 'Apartments', 'Year built' => $l['year_built'], 'Units' => $l['units'],
    'Pets' => pets_label($l), 'Age restriction' => $l['age_restriction'], 'Affordable housing' => $l['income_restricted'] ? 'Income restrictions apply' : null,
    'ZIP code' => $l['zip'],
]);
?>
<div class="wrap listing">
  <?php if ($l['status'] !== 'published'): ?><div class="alert alert-info">Preview: this listing is <strong><?= e($l['status']) ?></strong> and not visible to the public.</div><?php endif; ?>
  <?php if (!$l['has_photos']): ?>
  <section class="gallery gallery-empty">
    <figure class="gallery-main">
      <img src="<?= e(photo_url($l['photos'][0])) ?>" alt="Illustration – no photos of <?= e($l['name']) ?> yet" width="1200" height="720" fetchpriority="high">
      <figcaption class="no-photos">
        <span class="no-photos-icon" aria-hidden="true">📷</span>
        <strong>No photos of <?= e($l['name']) ?> yet</strong>
        <span>Own or manage this property? Add real photos so renters can see it.</span>
        <a class="btn btn-accent" href="<?= e($addPhotosUrl) ?>" rel="nofollow">📷 Add Photos</a>
      </figcaption>
    </figure>
  </section>
  <?php else: ?>
  <section class="gallery" data-gallery>
    <figure class="gallery-main">
      <img src="<?= e(photo_url($l['photos'][0])) ?>" alt="<?= e($l['name']) ?> – photo 1" width="1200" height="800" data-gallery-main fetchpriority="high">
    </figure>
    <div class="gallery-thumbs">
      <?php foreach ($l['photos'] as $i => $p): ?>
        <button type="button" data-src="<?= e(photo_url($p)) ?>" aria-label="Show photo <?= $i + 1 ?>" class="<?= $i ? '' : 'active' ?>"><img src="<?= e(photo_url($p, true)) ?>" alt="" loading="lazy" width="160" height="107"></button>
      <?php endforeach; ?>
    </div>
  </section>
  <?php endif; ?>

  <div class="listing-grid">
    <div class="listing-main">
      <header class="listing-head">
        <div class="badges">
          <?php if ($l['claimed']): ?><span class="badge badge-verified">✓ Verified owner</span><?php endif; ?>
          <?php if ($l['featured']): ?><span class="badge">Popular</span><?php endif; ?>
          <?php if ($l['income_restricted']): ?><span class="badge badge-soft">Income-based</span><?php endif; ?>
          <?php if ($l['age_restriction']): ?><span class="badge badge-soft"><?= e($l['age_restriction']) ?> community</span><?php endif; ?>
        </div>
        <h1><?= e($l['name']) ?></h1>
        <p class="addr"><?= e($l['address']) ?>, <?= e($l['city']) ?>, <?= e($l['state']) ?> <?= e($l['zip']) ?></p>
        <div class="key-facts">
          <div><span>Rent</span><strong><?= e(rent_label($l)) ?></strong></div>
          <div><span>Beds</span><strong><?= e(beds_label($l)) ?></strong></div>
          <?php if (sqft_label($l)): ?><div><span>Size</span><strong><?= e(sqft_label($l)) ?></strong></div><?php endif; ?>
          <div><span>Pets</span><strong><?= e(pets_label($l)) ?></strong></div>
        </div>
        <div class="listing-actions">
          <button type="button" class="btn btn-ghost btn-sm fav-btn-inline" data-fav="<?= (int)$l['id'] ?>" aria-pressed="false">♥ Save</button>
          <label class="btn btn-ghost btn-sm"><input type="checkbox" data-compare="<?= (int)$l['id'] ?>" hidden> ⇄ Compare</label>
          <button type="button" class="btn btn-ghost btn-sm" data-share>↗ Share</button>
        </div>
      </header>

      <section class="block">
        <h2>About <?= e($l['name']) ?></h2>
        <?php foreach (preg_split('/\n{2,}/', trim($l['description'])) as $para): ?><p><?= nl2br(e($para)) ?></p><?php endforeach; ?>
        <p><?= e($l['name']) ?> is located at <?= e($l['address']) ?> in <?= e($l['city']) ?>, Ohio<?= $l['city'] !== 'West Carrollton' ? ', next to West Carrollton' : '' ?>.
        <?= $l['beds_max'] !== null ? 'Floor plans range from ' . e(strtolower(beds_label($l))) . '. ' : '' ?>
        <?= $l['rent_min'] ? 'Advertised rents have started around ' . money($l['rent_min']) . ' per month. ' : '' ?>
        Rents, availability and specials change, so confirm details with the leasing office.</p>
      </section>

      <section class="block">
        <h2>Property details</h2>
        <dl class="facts">
          <?php foreach ($facts as $k => $v): ?><div><dt><?= e($k) ?></dt><dd><?= e($v) ?></dd></div><?php endforeach; ?>
        </dl>
      </section>

      <?php if ($l['amenities']): ?>
      <section class="block">
        <h2>Amenities</h2>
        <ul class="amenities">
          <?php foreach ($l['amenities'] as $a): ?><li><?= e($a) ?></li><?php endforeach; ?>
        </ul>
      </section>
      <?php endif; ?>

      <section class="block">
        <h2>Pet policy</h2>
        <p><strong><?= e(pets_label($l)) ?>.</strong> <?= $l['pet_notes'] ? e($l['pet_notes']) . '.' : '' ?> Always confirm pet rent, deposits, breed and weight limits before applying.
        <?php if (is_pet_friendly($l)): ?>See more <a href="/apartments/pet-friendly/">pet-friendly apartments in West Carrollton</a>.<?php endif; ?></p>
      </section>

      <section class="block">
        <h2>Estimate your monthly cost</h2>
        <div class="cost-calc card form" data-cost-calc data-rent="<?= (int)($l['rent_min'] ?: 1000) ?>" data-pets="<?= is_pet_friendly($l) ? 1 : 0 ?>">
          <div class="grid-2">
            <label>Monthly rent ($)<input type="number" data-c="rent" value="<?= (int)($l['rent_min'] ?: 1000) ?>" min="0" step="10"></label>
            <label>Bedrooms<select data-c="beds"><option value="0">Studio</option><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option></select></label>
            <label>Pets<select data-c="pets"><option value="0">None</option><option value="1">1 pet</option><option value="2">2 pets</option></select></label>
            <label>Renters insurance<select data-c="ins"><option value="15">Basic (~$15)</option><option value="25">Plus (~$25)</option><option value="0">I have it</option></select></label>
          </div>
          <div class="cost-out">
            <div><span>Rent</span><b data-o="rent"></b></div>
            <div><span>Utilities (est.)</span><b data-o="util"></b></div>
            <div><span>Internet (est.)</span><b data-o="net"></b></div>
            <div><span>Pet rent (est.)</span><b data-o="pet"></b></div>
            <div><span>Insurance</span><b data-o="ins"></b></div>
            <div class="total"><span>Estimated total</span><b data-o="total"></b></div>
          </div>
          <p class="small muted">Utility estimates are rough Ohio averages by apartment size. Income needed at 30% of gross: <b data-o="income"></b>/yr.</p>
        </div>
      </section>

      <section class="block">
        <h2>Location &amp; nearby</h2>
        <?php if ($l['lat']): ?>
        <div id="listing-map" class="listing-map" data-lat="<?= e($l['lat']) ?>" data-lng="<?= e($l['lng']) ?>" data-name="<?= e($l['name']) ?>"></div>
        <ul class="nearby">
          <?php foreach ($landmarks as [$n, $la, $lo]): ?>
            <li><span><?= e($n) ?></span><b>~<?= number_format($dist((float)$l['lat'], (float)$l['lng'], $la, $lo), 1) ?> mi</b></li>
          <?php endforeach; ?>
        </ul>
        <p class="small muted">Straight-line distances, approximate. Map pin location is approximate.</p>
        <?php endif; ?>
        <p><a href="https://www.google.com/maps/dir/?api=1&destination=<?= rawurlencode($l['address'] . ', ' . $l['city'] . ', OH ' . $l['zip']) ?>" target="_blank" rel="noopener nofollow">Get directions ↗</a> · <a href="/west-carrollton-living-guide/">West Carrollton living guide</a></p>
      </section>
    </div>

    <aside class="listing-side">
      <div class="contact-card card">
        <?php if ($l['show_contact']): ?>
          <h2 class="h4">Contact <?= e($l['name']) ?></h2>
          <ul class="contact-list">
            <?php if ($l['phone']): ?><li><a class="btn btn-block" href="tel:<?= e(preg_replace('/[^0-9+]/', '', $l['phone'])) ?>">📞 <?= e($l['phone']) ?></a></li><?php endif; ?>
            <?php if ($l['email']): ?><li><a class="btn btn-ghost btn-block" href="mailto:<?= e($l['email']) ?>?subject=<?= rawurlencode('Inquiry from WestCarrolltonApartments.com') ?>">✉️ Email the leasing office</a></li><?php endif; ?>
            <?php if ($l['website']): ?><li><a class="btn btn-ghost btn-block" href="<?= e($l['website']) ?>" target="_blank" rel="noopener">🌐 Visit website</a></li><?php endif; ?>
          </ul>
          <?php if ($l['office_hours']): ?><p class="small"><strong>Office hours:</strong> <?= e($l['office_hours']) ?></p><?php endif; ?>
          <p class="small muted">✓ Contact details provided by the verified owner/manager.</p>
        <?php else: ?>
          <h2 class="h4">Contact details</h2>
          <div class="locked">
            <p>🔒 Phone, email and website are hidden until the owner or manager verifies this listing.</p>
          </div>
          <p class="small">Renters: <a href="/contact/?subject=<?= rawurlencode('Question about ' . $l['name']) ?>">ask us about this property</a>.</p>
          <hr>
          <h3 class="h5">Own or manage <?= e($l['name']) ?>?</h3>
          <p class="small">Claim it for a one-time <strong>$<?= listing_price_cents() / 100 ?></strong> to show your contact details and manage photos, rents and amenities.</p>
          <a class="btn btn-accent btn-block" href="/claim/<?= e($l['slug']) ?>/" rel="nofollow">Claim this listing</a>
        <?php endif; ?>
      </div>
      <div class="card side-tools">
        <h3 class="h5">Helpful tools</h3>
        <a href="/tools/rent-affordability-calculator/">🧮 Can I afford this rent?</a>
        <a href="/tools/roommate-rent-splitter/">🤝 Split rent with a roommate</a>
        <a href="/tools/moving-cost-estimator/">🚚 Estimate moving costs</a>
        <a href="/tools/room-planner/">🛋️ Plan your furniture layout</a>
      </div>
      <p class="small muted">Spotted outdated info? <a href="/contact/?subject=<?= rawurlencode('Correction: ' . $l['name']) ?>">Send a correction</a>. Last updated <?= e(time_ago($l['updated_at'])) ?>.</p>
    </aside>
  </div>

  <?php if ($similar): ?>
  <section class="section-tight">
    <h2>Nearby apartments</h2>
    <div class="card-grid">
      <?php foreach ($similar as $s) partial('partials/card', ['l' => $s]); ?>
    </div>
  </section>
  <?php endif; ?>

  <section class="section-tight">
    <?php partial('partials/products', ['products' => $products, 'heading' => 'Move-in essentials for your new apartment']); ?>
  </section>
</div>
<div class="compare-bar" data-compare-bar hidden>
  <div class="wrap"><span><strong data-compare-count>0</strong> selected to compare</span><a class="btn btn-sm" data-compare-go href="/compare/">Compare now</a><button type="button" class="linklike" data-compare-clear>Clear</button></div>
</div>
