<?php
$l = $listing;
$b = base($l['base']);
$imgs = $l['images'] ?: [listing_image($l)];
$similar = array_values(array_filter(listings(), fn($o) => $o['slug'] !== $l['slug'] && $o['base'] === $l['base']));
foreach (newest_listings(12) as $o) if (count($similar) < 3 && $o['slug'] !== $l['slug'] && !in_array($o, $similar, true)) $similar[] = $o;
$similar = array_slice($similar, 0, 3);
$desc_text = trim(preg_replace('/\s+/', ' ', strip_tags($l['description'])));
$meta_desc = $l['seo_desc'] ?? mb_strimwidth($desc_text, 0, 155, '…');
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], [$b['name'], '/bases/' . $b['slug'] . '/'], [$l['title'], null]]);

$details = array_filter([
    'Installation'   => ['building', '<a href="/bases/' . e($b['slug']) . '/">' . e($b['name']) . '</a>'],
    'Managed by'     => ['home', e($l['operator'] ?? '')],
    'Eligibility'    => ['users', e($l['eligibility'] ?? '')],
    'Floor plans'    => ['bed', e(implode(' · ', array_filter([$l['beds_range'] ? $l['beds_range'] . ' bedrooms' : '', $l['baths_range'] ?? '' ? $l['baths_range'] . ' baths' : '', $l['sqft_range'] ? $l['sqft_range'] . ' sq ft' : ''])))],
    'Rent'           => ['calc', e($l['price'] ? price_label($l) : ($l['rent_note'] ?? 'Set by your BAH for active-duty residents. Call for current rates.'))],
    'Utilities'      => ['bolt', e($l['utilities'] ?? '')],
    'Pets'           => ['paw', e($l['pets'] ?? '')],
    'Office hours'   => ['clock', e($l['hours'] ?? '')],
    'Phone'          => ['phone', $l['phone'] ? '<a href="tel:' . e(preg_replace('/[^0-9+]/', '', $l['phone'])) . '">' . e($l['phone']) . '</a>' . (!empty($l['phone_note']) ? '<br><small class="muted">' . e($l['phone_note']) . '</small>' : '') : ''],
    'Email'          => ['mail', $l['email'] ? '<a href="mailto:' . e($l['email']) . '">' . e($l['email']) . '</a>' : ''],
], fn($v) => $v[1] !== '');

$schema = array_filter([
    '@type' => 'Accommodation', '@id' => abs_url('/properties/' . $l['slug'] . '/#listing'),
    'name' => $l['title'], 'description' => $desc_text, 'url' => abs_url('/properties/' . $l['slug'] . '/'),
    'image' => array_map(fn($i) => abs_url($i['src']), array_slice($imgs, 0, 6)),
    'address' => ['@type' => 'PostalAddress', 'streetAddress' => explode(',', $l['address'])[0]] + address_parts($l['address']),
    'geo' => ['@type' => 'GeoCoordinates', 'latitude' => $l['lat'], 'longitude' => $l['lng']],
    'numberOfBedrooms' => $l['beds'], 'numberOfBathroomsTotal' => $l['baths'],
    'floorSize' => $l['sqft'] ? ['@type' => 'QuantitativeValue', 'value' => $l['sqft'], 'unitCode' => 'FTK'] : null,
    'amenityFeature' => array_map(fn($a) => ['@type' => 'LocationFeatureSpecification', 'name' => $a, 'value' => true], $l['amenities']),
    'petsAllowed' => !empty($l['pets']) && !preg_match('/^no\b/i', $l['pets']),
    'telephone' => $l['phone'],
]);

function address_parts($addr) {
    $p = array_map('trim', explode(',', $addr));
    $last = end($p);
    preg_match('/([A-Z]{2})\s*(\d{5})?/', $last, $m);
    return array_filter(['addressLocality' => $p[count($p) - 2] ?? null, 'addressRegion' => $m[1] ?? null, 'postalCode' => $m[2] ?? null, 'addressCountry' => 'US']);
}

layout_start([
    'title' => $l['title'],
    'description' => $meta_desc,
    'path' => '/properties/' . $l['slug'] . '/',
    'image' => $imgs[0]['src'],
    'nav' => '/properties/',
    'schema' => [$crumb_schema, $schema],
]);
?>
<article class="listing" data-listing="<?= e($l['slug']) ?>">
  <div class="wrap">
    <?= $crumbs ?>
    <header class="listing-head">
      <div>
        <div class="tags">
          <a class="chip chip-dark" href="/bases/<?= e($b['slug']) ?>/"><?= e($b['name']) ?></a>
          <?php if ($l['featured']): ?><a class="chip chip-accent" href="/bases/featured/"><?= icon('star') ?> Featured</a><?php endif; ?>
          <span class="chip"><?= e($b['branch']) ?></span>
        </div>
        <h1><?= e($l['title']) ?></h1>
        <p class="listing-addr"><?= icon('pin') ?> <?= e($l['address']) ?></p>
      </div>
      <div class="listing-price">
        <strong><?= e(price_label($l)) ?></strong>
        <span class="muted"><?= $l['price'] ? 'Starting rent' : 'Call for current rates' ?></span>
      </div>
    </header>

    <div class="gallery gallery-n<?= min(5, count($imgs)) ?>" data-gallery>
      <?php foreach (array_slice($imgs, 0, 5) as $i => $img): ?>
        <button type="button" class="gallery-item<?= $i === 0 ? ' gallery-main' : '' ?>" data-index="<?= $i ?>" aria-label="View photo <?= $i + 1 ?> of <?= count($imgs) ?>">
          <img src="<?= e($img['src']) ?>" alt="<?= e($img['alt'] ?: $l['title'] . ' photo ' . ($i + 1)) ?>" <?= $i ? 'loading="lazy"' : 'fetchpriority="high"' ?>>
          <?php if ($i === 4 && count($imgs) > 5): ?><span class="gallery-more">+<?= count($imgs) - 5 ?> photos</span><?php endif; ?>
        </button>
      <?php endforeach; ?>
      <?php if (count($imgs) > 1): ?><button type="button" class="btn btn-light btn-sm gallery-all" data-index="0"><?= icon('image') ?> All <?= count($imgs) ?> photos</button><?php endif; ?>
      <script type="application/json" data-gallery-items><?= json_encode(array_map(fn($i) => ['src' => $i['src'], 'alt' => $i['alt'] ?? '', 'credit' => $i['credit'] ?? ''], $imgs), JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
    </div>
    <?php if (!empty($l['photo_note'])): ?><p class="fineprint photo-note"><?= e($l['photo_note']) ?></p><?php endif; ?>

    <div class="listing-layout">
      <div class="listing-main">
        <ul class="key-facts">
          <?php if ($l['beds']): ?><li><?= icon('bed') ?><strong><?= e(fmt_num($l['beds'])) ?></strong><span>Bedrooms</span></li><?php endif; ?>
          <?php if ($l['baths']): ?><li><?= icon('bath') ?><strong><?= e(fmt_num($l['baths'])) ?></strong><span>Bathrooms</span></li><?php endif; ?>
          <?php if ($l['sqft']): ?><li><?= icon('ruler') ?><strong><?= e(fmt_num($l['sqft'])) ?></strong><span>Sq ft</span></li><?php endif; ?>
          <li><?= icon('shield') ?><strong><?= e($b['short']) ?></strong><span>Installation</span></li>
        </ul>
        <p class="fineprint">Featured floor plan shown. <?= $l['beds_range'] ? 'This community offers ' . e($l['beds_range']) . ' bedroom homes.' : '' ?> Floor plans and availability vary.</p>

        <section class="listing-section">
          <h2>About this community</h2>
          <div class="prose"><?= $l['description'] ?></div>
        </section>

        <?php if ($l['highlights']): ?>
        <section class="listing-section">
          <h2>Highlights</h2>
          <ul class="checks"><?php foreach ($l['highlights'] as $h): ?><li><?= icon('check') ?> <?= e($h) ?></li><?php endforeach; ?></ul>
        </section>
        <?php endif; ?>

        <section class="listing-section">
          <h2>Property details</h2>
          <dl class="details">
            <?php foreach ($details as $k => [$ic, $v]): ?>
              <div><dt><?= icon($ic) ?> <?= e($k) ?></dt><dd><?= $v ?></dd></div>
            <?php endforeach; ?>
          </dl>
        </section>

        <?php if ($l['amenities']): ?>
        <section class="listing-section">
          <h2>Home features</h2>
          <ul class="amenities"><?php foreach ($l['amenities'] as $a): ?><li><?= icon('check') ?> <?= e($a) ?></li><?php endforeach; ?></ul>
        </section>
        <?php endif; ?>

        <?php if ($l['schools'] || $l['nearby']): ?>
        <section class="listing-section two-col-tight">
          <?php if ($l['schools']): ?><div><h2>Nearby schools</h2><ul class="plain"><?php foreach ($l['schools'] as $s): ?><li><?= icon('school') ?> <?= e($s) ?></li><?php endforeach; ?></ul></div><?php endif; ?>
          <?php if ($l['nearby']): ?><div><h2>Nearby</h2><ul class="plain"><?php foreach ($l['nearby'] as $s): ?><li><?= icon('pin') ?> <?= e($s) ?></li><?php endforeach; ?></ul></div><?php endif; ?>
        </section>
        <?php endif; ?>

        <section class="listing-section">
          <h2>Location</h2>
          <div class="map-embed">
            <iframe loading="lazy" title="Map of <?= e($l['address']) ?>" src="https://maps.google.com/maps?q=<?= rawurlencode($l['address']) ?>&amp;t=m&amp;z=14&amp;output=embed&amp;iwloc=near" referrerpolicy="no-referrer-when-downgrade"></iframe>
          </div>
          <p><a class="link-arrow" href="https://www.google.com/maps/dir/?api=1&amp;destination=<?= rawurlencode($l['address']) ?>" target="_blank" rel="noopener">Get directions <?= icon('arrow') ?></a></p>
        </section>

        <section class="listing-section"><?= widget_bah() ?></section>

        <?php if (!empty($l['sources'])): ?>
        <section class="listing-section sources">
          <h2>Sources</h2>
          <p class="fineprint">Details on this page were checked against these public sources. Rent, eligibility and availability change, so confirm with the community.</p>
          <ul class="plain small"><?php foreach ($l['sources'] as $u): ?><li><a href="<?= e($u) ?>" target="_blank" rel="noopener nofollow"><?= e(preg_replace('#^https?://(www\.)?#', '', rtrim($u, '/'))) ?></a></li><?php endforeach; ?></ul>
        </section>
        <?php endif; ?>
      </div>

      <aside class="listing-side">
        <div class="card contact-card" data-sticky>
          <p class="contact-price"><?= e(price_label($l)) ?></p>
          <p class="muted">Contact the community to check eligibility, waitlist times and move-in dates.</p>
          <?php if ($l['phone']): ?>
            <a class="btn btn-primary btn-block btn-lg" href="tel:<?= e(preg_replace('/[^0-9+]/', '', $l['phone'])) ?>"><?= icon('phone') ?> Call <?= e($l['phone']) ?></a>
          <?php else: ?>
            <a class="btn btn-primary btn-block btn-lg" href="<?= e(cfg('phone_href')) ?>"><?= icon('phone') ?> Call for more info</a>
          <?php endif; ?>
          <?php if ($l['website']): ?><a class="btn btn-outline btn-block" href="<?= e($l['website']) ?>" target="_blank" rel="noopener"><?= icon('globe') ?> Visit their website</a><?php endif; ?>
          <div class="contact-row">
            <button type="button" class="btn btn-light" data-fav="<?= e($l['slug']) ?>" aria-pressed="false"><?= icon('heart') ?> <span data-fav-label>Save</span></button>
            <button type="button" class="btn btn-light" data-share data-title="<?= e($l['title']) ?>"><?= icon('share') ?> Share</button>
          </div>
          <p class="fineprint">Listing details come from the housing operator's public information. Confirm everything with the community before signing a lease.</p>
        </div>
      </aside>
    </div>
  </div>
</article>

<?php if ($similar): ?>
<section class="section section-alt">
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">Keep looking</p><h2>Similar listings</h2></div><a class="link-arrow" href="/properties/">All listings <?= icon('arrow') ?></a></div>
    <div class="card-grid"><?php foreach ($similar as $o) echo listing_card($o); ?></div>
  </div>
</section>
<?php endif; ?>

<div class="lightbox" data-lightbox hidden role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button type="button" class="lb-close" data-lb-close aria-label="Close"><?= icon('x') ?></button>
  <button type="button" class="lb-nav lb-prev" data-lb-step="-1" aria-label="Previous photo"><?= icon('arrow', 'flip') ?></button>
  <figure><img data-lb-img alt=""><figcaption data-lb-cap></figcaption></figure>
  <button type="button" class="lb-nav lb-next" data-lb-step="1" aria-label="Next photo"><?= icon('arrow') ?></button>
</div>
<?php layout_end();
