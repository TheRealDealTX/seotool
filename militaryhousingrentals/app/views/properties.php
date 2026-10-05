<?php
// Listing archive. Also used by base.php with $archive set.
$archive ??= [
    'path' => '/properties/',
    'title' => 'Military Housing Rentals Near Base',
    'h1' => 'Military housing listings',
    'intro' => 'Browse on-base housing communities and military-friendly rentals at installations across the country. Filter by base, bedrooms and amenities, switch to the map, or save favorites to compare later.',
    'description' => 'Search military housing rentals and on-base family housing near Fort Hood, JBSA, Fort Bragg, Camp Lejeune, JBLM, Fort Campbell, Camp Pendleton, Fort Carson and more.',
    'items' => listings(),
    'base' => null,
    'crumbs' => [['Home', '/'], ['Listings', null]],
];
$items = $archive['items'];
usort($items, fn($a, $b) => strcmp($b['date'], $a['date']));
$amen = [];
foreach ($items as $l) foreach ($l['amenities'] as $a) $amen[$a] = ($amen[$a] ?? 0) + 1;
arsort($amen);
[$crumbs, $crumb_schema] = breadcrumbs($archive['crumbs']);
$pins = array_map(fn($l) => [
    'slug' => $l['slug'], 'title' => $l['title'], 'lat' => $l['lat'], 'lng' => $l['lng'],
    'addr' => $l['address'], 'price' => price_label($l), 'img' => listing_image($l)['src'],
], $items);

layout_start([
    'title' => $archive['title'],
    'description' => $archive['description'],
    'path' => $archive['path'],
    'image' => $archive['image'] ?? null,
    'nav' => '/properties/',
    'leaflet' => true,
    'schema' => [$crumb_schema, [
        '@type' => 'CollectionPage', 'url' => abs_url($archive['path']), 'name' => $archive['title'],
        'mainEntity' => ['@type' => 'ItemList', 'numberOfItems' => count($items), 'itemListElement' => array_map(fn($l, $i) => [
            '@type' => 'ListItem', 'position' => $i + 1, 'url' => abs_url('/properties/' . $l['slug'] . '/'), 'name' => $l['title'],
        ], $items, array_keys($items))],
    ]],
]);
?>
<section class="page-hero<?= !empty($archive['hero_img']) ? ' page-hero-img' : '' ?>">
  <?php if (!empty($archive['hero_img'])): ?><div class="hero-bg" aria-hidden="true"><img src="<?= e($archive['hero_img']) ?>" alt=""></div><?php endif; ?>
  <div class="wrap">
    <?= $crumbs ?>
    <?php if (!empty($archive['eyebrow'])): ?><p class="eyebrow"><?= e($archive['eyebrow']) ?></p><?php endif; ?>
    <h1><?= e($archive['h1']) ?></h1>
    <p class="lead"><?= e($archive['intro']) ?></p>
  </div>
</section>

<?php if (!empty($archive['before'])) echo $archive['before']; ?>

<section class="section section-tight" data-listings>
  <div class="wrap">
    <form class="filters card" data-filters onsubmit="return false">
      <label class="field field-grow"><span>Search</span>
        <input type="search" name="q" placeholder="Neighborhood, city, operator or amenity" autocomplete="off">
      </label>
      <?php if (!$archive['base']): ?>
      <label class="field"><span>Installation</span>
        <select name="base">
          <option value="">All bases</option>
          <?php foreach (bases() as $b): ?><option value="<?= e($b['slug']) ?>"><?= e($b['name']) ?></option><?php endforeach; ?>
        </select>
      </label>
      <?php endif; ?>
      <label class="field"><span>Bedrooms</span>
        <select name="beds"><option value="">Any</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option></select>
      </label>
      <label class="field"><span>Bathrooms</span>
        <select name="baths"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="2.5">2.5+</option></select>
      </label>
      <label class="field"><span>Sort by</span>
        <select name="sort"><option value="new">Newest</option><option value="beds">Most bedrooms</option><option value="sqft">Largest</option><option value="az">Name A–Z</option></select>
      </label>
      <div class="filter-row">
        <div class="chips" role="group" aria-label="Amenities">
          <?php foreach (array_slice(array_keys($amen), 0, 8) as $a): ?>
            <button type="button" class="chip-toggle" data-amenity="<?= e(strtolower($a)) ?>" aria-pressed="false"><?= e($a) ?></button>
          <?php endforeach; ?>
          <button type="button" class="chip-toggle chip-saved" data-saved-only aria-pressed="false"><?= icon('heart') ?> Saved</button>
        </div>
        <div class="view-toggle" role="group" aria-label="View">
          <button type="button" data-view="grid" aria-pressed="true"><?= icon('grid') ?> Grid</button>
          <button type="button" data-view="map" aria-pressed="false"><?= icon('map') ?> Map</button>
        </div>
      </div>
    </form>
    <p class="result-count" aria-live="polite"><strong data-count-shown><?= count($items) ?></strong> of <?= count($items) ?> listings <button type="button" class="link-btn" data-reset hidden>Clear filters</button></p>
    <div class="map-panel" data-map-panel hidden>
      <div class="map" data-map></div>
      <p class="fineprint">Pins show the approximate location of each community or its leasing office.</p>
    </div>
    <div class="card-grid" data-grid>
      <?php foreach ($items as $l) echo listing_card($l); ?>
    </div>
    <div class="empty card" data-empty hidden>
      <?= icon('search') ?>
      <h3>No listings match those filters</h3>
      <p>Try removing a filter, or <a href="/contact-us/">tell us which base you're moving to</a> and we'll help you look.</p>
    </div>
  </div>
  <script type="application/json" data-pins><?= json_encode($pins, JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP) ?></script>
</section>

<?php if (!empty($archive['after'])) echo $archive['after']; ?>
<?= cta_band() ?>
<?php layout_end();
