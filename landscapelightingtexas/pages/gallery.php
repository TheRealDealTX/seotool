<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Gallery';
$P['lead'] = 'Facades, live oaks, pools, paths and patios — a look at what professional landscape lighting does for Texas properties after dark.';
$items = [
    ['architectural-uplighting', 'Architectural Uplighting', 'Stone facade grazed with warm uplights', 'architecture'],
    ['oak-tree-uplighting', 'Live Oak Uplighting', 'Multiple uplights sculpt a mature canopy', 'trees'],
    ['pool-lighting', 'Pool & Spa Lighting', 'Water, palms and patio layered together', 'water'],
    ['garden-pathway-lighting', 'Garden Pathway', 'Path lights and bed accents along a stone walk', 'paths trees'],
    ['driveway-lighting', 'Driveway Bollards', 'Even light along a long drive and stone pillars', 'paths architecture'],
    ['patio-lighting', 'Patio String Lighting', 'Bistro lights and downlights for outdoor living', 'living'],
    ['landscape-lighting-texas-home', 'Whole-Property Design', 'Trees, beds, path and facade in one scene', 'architecture trees paths'],
];
?>
<section class="section">
  <div class="container">
    <div class="filter-bar reveal" role="group" aria-label="Filter gallery">
      <button type="button" class="is-on" data-filter="all">All</button><button type="button" data-filter="architecture">Architecture</button>
      <button type="button" data-filter="trees">Trees &amp; gardens</button><button type="button" data-filter="paths">Paths &amp; drives</button>
      <button type="button" data-filter="water">Pools</button><button type="button" data-filter="living">Outdoor living</button>
    </div>
    <div class="masonry" data-gallery>
      <?php foreach ($items as [$img, $t, $s, $cat]): ?>
      <figure class="reveal" data-cat="<?= $cat ?>"><img src="<?= img_url($img, 800) ?>" data-full="<?= img_url($img) ?>" alt="<?= e($t . ' — ' . $s) ?>" width="800" height="533" loading="lazy"><figcaption><strong><?= e($t) ?></strong><span><?= e($s) ?></span></figcaption></figure>
      <?php endforeach; ?>
    </div>
  </div>
</section>
<section class="section alt">
  <div class="container grid-2" style="align-items:center">
    <div>
      <?php section_head('Before &amp; after', 'Same Home. Different Night.', '', 'left'); ?>
      <p class="reveal" style="color:var(--muted)">Drag the slider to compare a property without lighting and with a layered Landscape Lighting Texas design: grazed stone, uplit trees, and soft path light leading to the door.</p>
      <p class="reveal"><a class="link-arrow" href="/tools/lighting-design-simulator/">Try the full lighting simulator <?= icon('arrow', 16) ?></a></p>
    </div>
    <?php before_after('oak-tree-uplighting', 'Live oak and home with landscape lighting'); ?>
  </div>
</section>
<section class="section">
  <div class="container">
    <?php section_head('Get inspired', 'Find the Right Service for Your Property'); service_cards('', 4); ?>
  </div>
</section>
<?php cta_band('Imagine Your Home in This Light', '');
