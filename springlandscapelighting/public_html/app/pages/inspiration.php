<?php defined('SLT') || exit;
require_once APP . '/partials/house-scene.php';
page_hero(['title' => 'Landscape Lighting Ideas &amp; Inspiration', 'eyebrow' => 'Inspiration', 'tall' => true, 'img' => 'Spring-Landscape-Lighting-BG-2.webp',
  'sub' => 'Ideas for lighting facades, entries, trees, paths, patios and pools, and the techniques behind each look.', 'cta' => true, 'crumbs' => [['Home', '/'], ['Inspiration', null]]]);
$scene = fn($id, $layers) => '<div class="scene win-on only ' . implode(' ', array_map(fn($l) => 'on-' . $l, $layers)) . '" style="--lc:#ffc27a;position:absolute;inset:0">' . house_scene($id, true) . '</div>';
?>
<section class="sec" style="padding-top:30px">
  <div class="wrap">
    <?php section_head('Ideas by area', 'What great lighting looks like, room by outdoor room', 'Hover a tile to see the technique behind it.'); ?>
    <div class="tiles">
      <div class="tile tile--w" data-reveal><?= $scene('i1', ['arch']) ?><div class="tile__cap"><small>Architecture</small><h3>Uplighting &amp; wall washing</h3><p>Narrow beams graze brick and columns; wider floods wash broad walls. Placing fixtures a short distance from the wall avoids hot spots at the base.</p></div></div>
      <div class="tile tile--t" data-reveal data-delay="1"><img src="/assets/img/Spring-Landscape-Lighting-BG-2.webp" alt="Sculptural light glowing on a lawn" loading="lazy"><div class="tile__cap"><small>Lawn &amp; garden</small><h3>Sculptural accents</h3><p>A single decorative fixture can become a night-time focal point, especially on an open lawn where there is nothing else to light.</p></div></div>
      <div class="tile" data-reveal><img src="/assets/img/Spring-Landscape-Lighting-BG-1-960.webp" alt="Grasses lit from below" loading="lazy" style="object-position:70% 60%"><div class="tile__cap"><small>Planting beds</small><h3>Grazing ornamental grasses</h3><p>Low, close fixtures skim light across texture so grasses and foliage glow against darkness.</p></div></div>
      <div class="tile" data-reveal data-delay="1"><?= $scene('i2', ['tree']) ?><div class="tile__cap"><small>Trees</small><h3>Canopy uplighting</h3><p>Two or three fixtures around a live oak add volume. One uplight on a narrow pine adds height.</p></div></div>
      <div class="tile" data-reveal><?= $scene('i3', ['path']) ?><div class="tile__cap"><small>Arrival</small><h3>Staggered path lights</h3><p>Alternating pools of light lead the eye to the door without the runway look.</p></div></div>
      <div class="tile tile--w" data-reveal data-delay="1"><img src="/assets/img/How-Much-Electricity-Does-Landscape-Lighting-Use.webp" alt="Lantern-lit garden walkway under palms at night" loading="lazy"><div class="tile__cap"><small>Walkways</small><h3>Lanterns, palms &amp; moonlight</h3><p>Decorative lanterns mark the route while uplit palms and canopy light frame the view at the end of the path.</p></div></div>
      <div class="tile" data-reveal><?= $scene('i4', ['patio']) ?><div class="tile__cap"><small>Outdoor living</small><h3>Pergola &amp; string lighting</h3><p>Warm 2200K bulbs and soft downlight make patios comfortable for conversation, not interrogation.</p></div></div>
      <div class="tile" data-reveal data-delay="1"><?= $scene('i5', ['arch', 'path', 'tree', 'patio']) ?><div class="tile__cap"><small>Whole property</small><h3>Layered design</h3><p>All four layers, balanced. Each one does a job and none overwhelms the others.</p></div></div>
      <div class="tile" data-reveal data-delay="2"><img src="/assets/img/Spring-Landscape-Lighting-BG-1-960.webp" alt="Trees with soft light at night" loading="lazy" style="object-position:15% 30%"><div class="tile__cap"><small>Depth</small><h3>Foreground, middle, background</h3><p>Lighting at three depths makes even a small yard feel deeper from inside the house.</p></div></div>
    </div>
  </div>
</section>

<section class="sec sec--forest">
  <div class="wrap">
    <?php section_head('Ideas by home style', 'Match the light to the architecture'); ?>
    <div class="grid-2">
      <?php foreach ([
        ['Traditional brick', 'Warm 2700K uplighting on piers and between windows, grazing on columns, and soft path lights. Red and orange brick come alive under warm light.'],
        ['Stone &amp; Hill Country', 'Grazing light close to textured limestone or Austin stone emphasizes depth and shadow. 3000K often keeps pale stone crisp without going cold.'],
        ['Modern farmhouse', 'Clean, symmetrical washes on board-and-batten, downlights from eaves, and minimal fixtures. Restraint suits the style.'],
        ['Mediterranean &amp; stucco', 'Wide, even washes avoid scalloping on smooth stucco. Palms, arches and courtyards are natural focal points.'],
      ] as $i => [$t, $d]): ?>
      <div class="kv__item" data-reveal data-delay="<?= $i % 2 ?>"><?= icon('house') ?><h3><?= $t ?></h3><p><?= $d ?></p></div>
      <?php endforeach; ?>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="prose">
      <h2>Ten ideas worth stealing</h2>
      <ol>
        <li>Light the house and the biggest tree first; they define the scene from the street.</li>
        <li>Graze columns from directly below for a crisp vertical line.</li>
        <li>Moonlight a live oak from inside the canopy for dappled shadows on the lawn.</li>
        <li>Stagger path lights instead of lining both sides.</li>
        <li>Put step lights in risers or walls rather than relying on overhead light.</li>
        <li>Silhouette a sculptural plant by washing the wall behind it.</li>
        <li>Light the view from inside: what you see from the living room window matters.</li>
        <li>Use warm 2200K string lights over seating, and keep other layers 2700K–3000K.</li>
        <li>Zone the backyard separately so it can stay off until you use it.</li>
        <li>Leave some darkness. Contrast is what makes a lit feature special.</li>
      </ol>
      <p>Learn the vocabulary in <a href="/landscape-lighting-techniques/">12 landscape lighting techniques</a>, choose colors with the <a href="/tools/color-temperature-guide/">color temperature explorer</a>, or let Spring Landscape Lighting design it for you.</p>
    </div>
    <div data-reveal="right"><?php tool_embed('color-temperature-guide', false); ?></div>
  </div>
</section>
<?php cta_band(); ?>
