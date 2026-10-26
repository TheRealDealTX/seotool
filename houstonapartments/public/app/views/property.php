<?php
defined('HA_ROOT') || exit;
$d = $p['d'];
$photos = $d['photos'] ?: ['/assets/img/Houston-High-Rise.webp'];
$plans = $d['floorplans'] ?? [];
$prices = $d['prices'] ?? [];
$bedGroups = [];
foreach ($plans as $pl) {
    $bedGroups[$pl['beds']][] = $pl;
}
ksort($bedGroups);
foreach (array_keys($prices) as $b) {
    $bedGroups[(int) $b] ??= [];
}
ksort($bedGroups);
$area = $areaKey ? AREAS[$areaKey] : null;
$addr = trim($p['street'] . ', ' . $p['city'] . ', TX ' . $p['zip'], ', ');
$facts = array_filter([
    'Rent'       => Listings::priceLabel($p),
    'Bedrooms'   => beds_range($p),
    'Size'       => $p['sqft_min'] ? number_format($p['sqft_min']) . ($p['sqft_max'] != $p['sqft_min'] ? '–' . number_format($p['sqft_max']) : '') . ' sqft' : null,
    'Built'      => $p['year_built'],
    'Units'      => $p['units'],
    'Stories'    => $p['stories'],
]);
?>
<nav class="crumbs wrap" aria-label="Breadcrumb">
  <a href="/">Houston Apartments</a><span>/</span>
  <?php if ($area): ?><a href="/<?= $areaKey ?>/"><?= e($area['name']) ?></a><span>/</span><?php else: ?><a href="/apartments/">Apartments</a><span>/</span><?php endif ?>
  <span aria-current="page"><?= e($p['name']) ?></span>
</nav>

<section class="gallery wrap" data-gallery>
  <?php foreach (array_slice($photos, 0, 5) as $k => $src): ?>
    <button type="button" class="g-item g<?= $k ?>" data-open="<?= $k ?>" aria-label="Open photo <?= $k + 1 ?>">
      <img src="<?= e($src) ?>" alt="<?= e($p['name']) ?> photo <?= $k + 1 ?>" <?= $k ? 'loading="lazy"' : 'fetchpriority="high"' ?> width="900" height="600">
    </button>
  <?php endforeach ?>
  <button type="button" class="g-all" data-open="0"><span class="ico ico-grid" aria-hidden="true"></span> View all <?= count($photos) ?> photos</button>
</section>

<div class="wrap prop-layout">
  <div class="prop-main">
    <header class="prop-head reveal">
      <div class="prop-tags">
        <?php if ($p['neighborhood']): ?><span class="pill"><?= e($p['neighborhood']) ?></span><?php endif ?>
        <?php if ($p['pets']): ?><span class="pill pill-soft">🐾 Pet friendly</span><?php endif ?>
        <?php if ($p['parking']): ?><span class="pill pill-soft">🚗 Parking</span><?php endif ?>
        <?php if ($p['rating']): ?><span class="pill pill-soft">★ <?= e($p['rating']) ?> Google rating</span><?php endif ?>
      </div>
      <h1><?= e($p['name']) ?></h1>
      <p class="prop-addr"><span class="ico ico-pin" aria-hidden="true"></span> <?= e($addr) ?></p>
      <div class="facts">
        <?php foreach ($facts as $k => $v): ?><div><span><?= e($k) ?></span><strong><?= e($v) ?></strong></div><?php endforeach ?>
      </div>
    </header>

    <?php if ($d['special'] ?? ''): ?>
      <div class="special-box reveal"><strong>Move-in special:</strong> <?= e($d['special']) ?></div>
    <?php endif ?>

    <section class="prop-sec reveal" id="pricing">
      <h2>Pricing &amp; floor plans</h2>
      <?php if ($bedGroups): ?>
      <div class="tabs plan-tabs" role="tablist">
        <button role="tab" type="button" aria-selected="true" data-plan-tab="all">All</button>
        <?php foreach ($bedGroups as $b => $_): ?><button role="tab" type="button" aria-selected="false" data-plan-tab="<?= $b ?>"><?= beds_label($b) ?></button><?php endforeach ?>
      </div>
      <div class="plan-groups">
        <?php foreach ($bedGroups as $b => $list): ?>
          <div class="plan-group" data-beds="<?= $b ?>">
            <div class="plan-group-head">
              <h3><?= beds_label($b) ?></h3>
              <p><?= isset($prices[$b]) ? 'Starting at <strong>' . money($prices[$b]) . '</strong>/mo' : 'Call for current pricing' ?></p>
            </div>
            <div class="plans">
              <?php foreach ($list as $pl): ?>
                <div class="plan">
                  <?php if ($pl['image']): ?>
                    <button type="button" class="plan-img" data-zoom="<?= e($pl['image']) ?>" aria-label="Enlarge floor plan"><img src="<?= e($pl['image']) ?>" alt="<?= e($p['name'] . ' ' . beds_label($b) . ' floor plan, ' . $pl['sqft'] . ' sqft') ?>" loading="lazy" width="300" height="240"></button>
                  <?php else: ?>
                    <div class="plan-img plan-ph" aria-hidden="true"><span class="ico ico-plan"></span></div>
                  <?php endif ?>
                  <div class="plan-info">
                    <strong><?= beds_label($b) ?> · <?= rtrim(rtrim(number_format($pl['baths'], 1), '0'), '.') ?> Bath</strong>
                    <span><?= number_format($pl['sqft']) ?> sqft</span>
                    <?php if ($pl['available']): ?><span class="avail">Available <?= e($pl['available']) ?></span><?php endif ?>
                  </div>
                  <button type="button" class="btn btn-outline btn-sm" data-lead data-lead-prop="<?= $p['id'] ?>" data-lead-name="<?= e($p['name'] . ' – ' . beds_label($b) . ', ' . $pl['sqft'] . ' sqft') ?>">Check availability</button>
                </div>
              <?php endforeach ?>
              <?php if (!$list): ?><p class="muted">Floor plan details coming soon – ask us for the latest layouts.</p><?php endif ?>
            </div>
          </div>
        <?php endforeach ?>
      </div>
      <?php else: ?>
        <p class="muted">Floor plans and pricing are available on request.</p>
      <?php endif ?>
      <p class="fine">Prices and availability change frequently and are not guaranteed. Square footage is approximate.</p>
    </section>

    <?php if ($d['about'] ?? []): ?>
    <section class="prop-sec reveal" id="about">
      <h2>About <?= e($p['name']) ?></h2>
      <div class="prose"><?php foreach ($d['about'] as $para): ?><p><?= e($para) ?></p><?php endforeach ?></div>
    </section>
    <?php endif ?>

    <?php if ($d['amenities'] ?? []): ?>
    <section class="prop-sec reveal" id="amenities">
      <h2>Amenities</h2>
      <div class="amen-cols">
        <?php foreach ($d['amenities'] as $group => $list): ?>
          <div><h3><?= e($group === 'Luxuries' ? 'Extras' : $group) ?></h3><ul class="amen-list"><?php foreach ($list as $a): ?><li><?= e($a) ?></li><?php endforeach ?></ul></div>
        <?php endforeach ?>
      </div>
    </section>
    <?php endif ?>

    <section class="prop-sec reveal" id="location">
      <h2>Location</h2>
      <div id="prop-map" class="prop-map" data-lat="<?= e($p['lat']) ?>" data-lng="<?= e($p['lng']) ?>" data-name="<?= e($p['name']) ?>"></div>
      <p class="muted"><?= e($addr) ?><?= $p['neighborhood'] ? ' · ' . e($p['neighborhood']) : '' ?></p>
    </section>

    <?php if ($d['schools'] ?? []): ?>
    <section class="prop-sec reveal" id="schools">
      <h2>Schools</h2>
      <div class="school-grid">
        <?php foreach ($d['schools'] as $k => $v): ?><div class="school"><span><?= e($k) ?></span><strong><?= e($v) ?></strong></div><?php endforeach ?>
      </div>
      <p class="fine">School assignments can change. Verify with the district before signing a lease.</p>
    </section>
    <?php endif ?>

    <?php if ($d['faqs'] ?? []): ?>
    <section class="prop-sec reveal" id="faq">
      <h2><?= e($p['name']) ?> FAQs</h2>
      <div class="faq">
        <?php foreach ($d['faqs'] as $f): if (!$f['a']) continue; ?>
          <details><summary><?= e($f['q']) ?></summary>
            <?php if (count($f['a']) > 2): ?><p><?= e($f['a'][0]) ?></p><ul><?php foreach (array_slice($f['a'], 1) as $li): ?><li><?= e($li) ?></li><?php endforeach ?></ul>
            <?php else: ?><p><?= e(implode(' ', $f['a'])) ?></p><?php endif ?>
          </details>
        <?php endforeach ?>
      </div>
    </section>
    <?php endif ?>
  </div>

  <aside class="prop-side">
    <div class="contact-card">
      <p class="cc-price"><?= e(Listings::priceLabel($p)) ?></p>
      <p class="cc-sub"><?= e(beds_range($p)) ?><?= $d['hours'] ?? '' ? ' · Office ' . e($d['hours']) : '' ?></p>
      <button class="btn btn-grad btn-block btn-lg" type="button" data-lead data-lead-prop="<?= $p['id'] ?>" data-lead-name="<?= e($p['name']) ?>">Check availability</button>
      <button class="btn btn-outline btn-block" type="button" data-lead data-lead-prop="<?= $p['id'] ?>" data-lead-name="Tour: <?= e($p['name']) ?>">Schedule a tour</button>
      <a class="btn btn-ghost btn-block" href="tel:<?= SITE['phone_raw'] ?>">Call <?= SITE['phone'] ?></a>
      <div class="cashback"><span class="cb-amt">$<?= SITE['cashback'] ?></span><span>back when you lease <?= e($p['name']) ?> through Houston Apartments</span></div>
    </div>
  </aside>
</div>

<?php if ($nearby): ?>
<section class="section nearby">
  <div class="wrap">
    <div class="section-head reveal"><div><span class="pill">Nearby</span><h2>More apartments near <?= e($p['name']) ?></h2></div>
      <a class="link-arrow" href="/apartments/<?= $areaKey ? '?area=' . $areaKey : '' ?>">See on map</a></div>
    <div class="carousel" data-carousel>
      <?php foreach ($nearby as $i => $c): require HA_APP . '/views/partials/card.php'; endforeach ?>
    </div>
  </div>
</section>
<?php endif ?>

<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photos">
  <button class="lb-x" type="button" data-lb-close aria-label="Close">×</button>
  <button class="lb-nav lb-prev" type="button" data-lb="-1" aria-label="Previous">‹</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-nav lb-next" type="button" data-lb="1" aria-label="Next">›</button>
  <script type="application/json" class="lb-data"><?= json_encode(array_values($photos), JSON_UNESCAPED_SLASHES) ?></script>
</div>
<div class="sticky-cta"><span><?= e(Listings::priceLabel($p)) ?></span><button class="btn btn-grad" type="button" data-lead data-lead-prop="<?= $p['id'] ?>" data-lead-name="<?= e($p['name']) ?>">Check availability</button></div>
