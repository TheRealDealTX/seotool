<?php
[$crumbs, $crumb_schema] = breadcrumbs([['Home', '/'], ['Military Bases', null]]);
$by_state = [];
foreach (bases() as $b) $by_state[$b['state']][] = $b;
ksort($by_state);
$pins = array_map(fn($l) => ['slug' => $l['slug'], 'title' => $l['title'], 'lat' => $l['lat'], 'lng' => $l['lng'], 'addr' => $l['address'], 'price' => price_label($l), 'img' => listing_image($l)['src']], listings());
layout_start([
    'title' => 'Military Bases',
    'description' => 'Military housing by installation: Fort Hood, Joint Base San Antonio, Fort Bliss, Fort Bragg, Camp Lejeune, JBLM, Fort Campbell, Naval Station Norfolk, Camp Pendleton, Fort Carson and Fort Benning.',
    'path' => '/marine-bases/',
    'image' => '/wp-content/uploads/2025/06/Fort-Cavazos-Hood.webp',
    'leaflet' => true,
    'schema' => [$crumb_schema],
]);
?>
<section class="page-hero">
  <div class="wrap">
    <?= $crumbs ?>
    <p class="eyebrow">Army · Navy · Air Force · Marine Corps</p>
    <h1>Military bases</h1>
    <p class="lead">Is your service member heading to a new duty station, or is your future Marine about to stand on the yellow footprints? Pick an installation to see housing communities, floor plans and local resources.</p>
    <div class="branch-filter chips" role="group" aria-label="Filter by branch" data-branch-filter>
      <button type="button" class="chip-toggle" aria-pressed="true" data-branch="">All</button>
      <button type="button" class="chip-toggle" aria-pressed="false" data-branch="army">Army</button>
      <button type="button" class="chip-toggle" aria-pressed="false" data-branch="air force">Air Force</button>
      <button type="button" class="chip-toggle" aria-pressed="false" data-branch="navy">Navy</button>
      <button type="button" class="chip-toggle" aria-pressed="false" data-branch="marine corps">Marine Corps</button>
    </div>
  </div>
</section>
<section class="section section-tight">
  <div class="wrap">
    <div class="base-cards" data-base-cards>
      <?php foreach (bases() as $b): $n = count(listings_for_base($b['slug'])); $img = $b['image']['src'] ?? listing_image(listings_for_base($b['slug'])[0] ?? ['images' => []])['src']; ?>
      <a class="card base-card" href="/bases/<?= e($b['slug']) ?>/" data-branch="<?= e(strtolower($b['branch'])) ?>">
        <span class="card-media"><img src="<?= e($img) ?>" alt="" loading="lazy" width="600" height="375"><span class="chip chip-dark"><?= e($b['branch']) ?></span></span>
        <span class="card-body">
          <strong class="card-title"><?= e($b['name']) ?></strong>
          <span class="card-addr"><?= icon('pin') ?> <?= e($b['city'] . ', ' . $b['state']) ?></span>
          <span class="muted small"><?= e($b['blurb']) ?></span>
          <span class="base-count"><?= $n ?> listing<?= $n === 1 ? '' : 's' ?> <?= icon('arrow') ?></span>
        </span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section section-alt" data-listings>
  <div class="wrap">
    <div class="section-head"><div><p class="eyebrow">Explore</p><h2>Every listing on the map</h2></div></div>
    <div class="map-panel"><div class="map map-tall" data-map data-map-auto></div></div>
    <script type="application/json" data-pins><?= json_encode($pins, JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
    <p class="muted">Don't see your duty station? We're adding installations all the time. If you live at a base we don't cover yet and want to help, <a href="/contact-us/">send us a message</a>.</p>
  </div>
</section>
<?= cta_band() ?>
<?php layout_end();
