<?php
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

$crumbs = [['Home', '/'], ['Service Areas', '/service-areas/']];
$all = array_values(areas());
$items = array_map(fn($a) => [$a['city'] . ', TX', $a['path']], $all);
$page = [
    'title' => 'Landscape Lighting Service Areas Around Austin, TX',
    'description' => 'Austin Landscape Lighting serves Austin, Round Rock, Cedar Park, Pflugerville, Georgetown, Bee Cave, Lakeway, Westlake Hills, Rollingwood, Kyle and Buda.',
    'path' => '/service-areas/',
    'active' => '/service-areas/',
    'image' => 'landscape-lighting-austin-tx-2',
    'schema' => [schema_webpage(['title' => 'Service Areas', 'description' => 'Cities served by Austin Landscape Lighting.', 'path' => '/service-areas/'], 'CollectionPage'), schema_breadcrumb($crumbs), schema_itemlist($items, 'Austin Landscape Lighting service areas')],
];
// Simple projected map: lng/lat -> svg coords
$minLng = -98.15; $maxLng = -97.45; $minLat = 29.95; $maxLat = 30.75;
$px = fn($lng) => round(60 + ($lng - $minLng) / ($maxLng - $minLng) * 680);
$py = fn($lat) => round(40 + ($maxLat - $lat) / ($maxLat - $minLat) * 520);
ob_start();
echo sub_hero(['eyebrow' => 'Service areas', 'h1' => 'Landscape Lighting Across Greater Austin', 'intro' => 'Austin Landscape Lighting is based in Austin and works across Travis, Williamson and Hays counties. Pick your city for local design notes, neighborhoods and FAQs, or call and we will tell you if we reach you.', 'image' => 'landscape-lighting-austin-tx-2', 'image_alt' => 'Austin Landscape Lighting project in Central Texas', 'crumbs' => $crumbs]);
?>
<section class="section">
  <div class="container feature-split">
    <div class="map-wrap" data-map data-reveal="left">
      <svg viewBox="0 0 800 600" role="img" aria-label="Map of cities served by Austin Landscape Lighting">
        <defs><radialGradient id="mapglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffb347" stop-opacity=".25"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient></defs>
        <circle cx="<?= $px(BIZ['lng']) ?>" cy="<?= $py(BIZ['lat']) ?>" r="260" fill="url(#mapglow)"/>
        <g stroke="rgba(255,255,255,.08)" stroke-width="1"><?php for ($i = 0; $i <= 8; $i++) echo '<line x1="' . (60 + $i * 85) . '" y1="40" x2="' . (60 + $i * 85) . '" y2="560"/>'; for ($i = 0; $i <= 6; $i++) echo '<line x1="60" y1="' . (40 + $i * 86) . '" x2="740" y2="' . (40 + $i * 86) . '"/>'; ?></g>
        <path d="M <?= $px(-97.80) ?> 40 Q <?= $px(-97.70) ?> <?= $py(30.4) ?> <?= $px(-97.75) ?> <?= $py(30.25) ?> T <?= $px(-97.85) ?> 560" fill="none" stroke="rgba(159,193,255,.35)" stroke-width="3" stroke-linecap="round"/>
        <text x="<?= $px(-97.78) ?>" y="<?= $py(30.6) ?>" fill="rgba(159,193,255,.5)" font-size="12" font-family="Manrope" transform="rotate(-78 <?= $px(-97.78) ?> <?= $py(30.6) ?>)">I-35</text>
        <?php foreach ($all as $a): $x = $px($a['lng']); $y = $py($a['lat']); $home = $a['slug'] === 'austin'; ?>
        <g class="map-pin" data-city="<?= e($a['city']) ?>" data-desc="<?= e($a['county'] . ' · ' . $a['drive']) ?>" data-href="<?= e($a['path']) ?>" tabindex="0" role="button" aria-label="<?= e($a['city']) ?>">
          <?php if ($home): ?><circle class="pulse" cx="<?= $x ?>" cy="<?= $y ?>" r="8"/><?php endif; ?>
          <circle cx="<?= $x ?>" cy="<?= $y ?>" r="<?= $home ? 9 : 6 ?>"/>
          <text x="<?= $x + 14 ?>" y="<?= $y + 5 ?>"><?= e($a['city']) ?></text>
        </g>
        <?php endforeach; ?>
      </svg>
      <div class="map-info"><div><strong data-map-name>Austin</strong><span data-map-desc>Travis County</span></div><a class="btn btn--ghost btn--sm" data-map-link href="/service-areas/austin/">See Austin lighting →</a></div>
    </div>
    <div data-reveal="right">
      <p class="eyebrow">Where we work</p>
      <h2 class="display">Twelve cities, one Austin-based crew</h2>
      <p class="lede">Hover a pin to see each community. Austin Landscape Lighting schedules design visits at dusk so you see your property the way the lighting will, and most cities are within a 30-minute drive of our shop.</p>
      <ul class="checks">
        <li><?= icon('pin') ?><div><strong>Travis County</strong><span>Austin, Bee Cave, Lakeway, Westlake Hills, Rollingwood, Pflugerville</span></div></li>
        <li><?= icon('pin') ?><div><strong>Williamson County</strong><span>Round Rock, Cedar Park, Georgetown</span></div></li>
        <li><?= icon('pin') ?><div><strong>Hays County</strong><span>Kyle, Buda, Dripping Springs</span></div></li>
      </ul>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container">
    <?= section_head('Choose your city', 'Local lighting notes for every community', 'Each page covers the housing stock, trees, terrain and HOA considerations that shape a design there.') ?>
    <div class="area-grid">
      <?php foreach ($all as $i => $a): ?>
      <a class="card card--area" href="<?= e($a['path']) ?>" data-reveal style="--delay:<?= ($i % 3) * 80 ?>ms">
        <span class="card__media"><?= picture($a['image'], $a['image_alt'], ['sizes' => '(max-width: 760px) 100vw, 33vw']) ?></span>
        <span class="card__body"><small><?= e($a['county']) ?></small><h3>Landscape lighting in <?= e($a['city']) ?>, TX</h3><p><?= e(mb_strimwidth($a['intro'], 0, 130, '…')) ?></p><span class="card__more">Local details <?= icon('arrow') ?></span></span>
      </a>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<?= cta_band('Not sure if we reach you?', 'Call Austin Landscape Lighting. If your property is within about 45 minutes of Austin we are usually glad to make the drive.') ?>
<?php
render_page($page, ob_get_clean());
