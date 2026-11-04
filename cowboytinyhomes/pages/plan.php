<?php
// Plan page: buy box, "have us build it", drawing previews, 3D viewer, Texas notes, cost
// estimate with Texas regional factors and the materials summary. Routed for every plan in
// inc/plans.php; pages/gonzales-modern-living.php includes it with its own extra copy.
require_once __DIR__ . '/../inc/plan-svg.php';
require_once __DIR__ . '/../inc/store.php';
global $PLANS;
$slug = $GLOBALS['page']['plan'];
$p = $PLANS[$slug];
$set = plan_sets()[$slug] ?? null;
$est = $set['estimate'] ?? null;
$dir = "/assets/plans/$slug";
$buyOnline = store_ready($slug);
$upper = !empty($p['upper']);
$GLOBALS['scripts'][] = 'plan-page.js';

$buyLink = '/contact-us/?' . http_build_query(['project' => 'Plan purchase: ' . $p['name'], 'ptype' => 'Design / plans only',
    'note' => 'I would like to buy ' . $p['ref'] . ' plan set (' . money($p['price']) . ').']) . '#form';
$buildLink = '/contact-us/?' . http_build_query(['project' => 'Build ' . $p['ref'], 'size' => $p['sqft'],
    'ptype' => ['single' => 'Small single-family home', 'adu' => 'ADU / casita / guest house', 'park' => 'Park model home', 'thow' => 'Tiny home on wheels', 'studio' => 'Custom tiny home'][$p['category']],
    'note' => 'I would like Cowboy Tiny Homes to build ' . $p['ref'] . ' plan (' . number_format($p['sqft']) . ' sq ft).']) . '#form';
$modLink = '/contact-us/?' . http_build_query(['project' => 'Modify ' . $p['ref'], 'ptype' => 'Design / plans only', 'note' => 'Changes I would like to ' . $p['ref'] . ' plan: ']) . '#form';

// Similar plans: same category first, then the closest in size.
$others = array_filter(array_keys($PLANS), fn($s) => $s !== $slug);
usort($others, fn($a, $b) => ($PLANS[$b]['category'] === $p['category']) <=> ($PLANS[$a]['category'] === $p['category'])
    ?: abs($PLANS[$a]['sqft'] - $p['sqft']) <=> abs($PLANS[$b]['sqft'] - $p['sqft']));
$others = array_slice($others, 0, 3);

$specs = ['Total living area' => number_format($p['sqft']) . ' sq ft'];
if ($upper) $specs += ['First floor' => number_format($p['main_sqft']) . ' sq ft', 'Second floor' => number_format($p['upper_sqft']) . ' sq ft'];
if ($p['loft_sqft']) $specs += ['Main floor' => number_format($p['main_sqft']) . ' sq ft', 'Loft' => $p['loft_sqft'] . ' sq ft'];
$specs += [
    'Bedrooms' => $p['bed_label'], 'Bathrooms' => $p['bath_label'],
    'Levels' => $upper ? 'Two stories' : ($p['has_loft'] ? 'Main floor + loft' : 'Single level'),
    'Footprint' => $p['width'] . ' x ' . $p['depth'], 'Overall height' => $p['height'], 'Ceiling height' => $p['ceiling'],
    'Roof' => $p['roof'], 'Exterior walls' => $p['walls'], 'Foundation' => $p['foundation'],
];
if ($set) {
    $hv = $set['hvac'];
    $specs += [
        'Electrical' => $set['electrical']['service'] . ', ' . $set['electrical']['circuits'] . ' circuits',
        'Heating & cooling' => $hv ? 'Ductless heat pump, ' . number_format($hv['outdoor_btu']) . ' BTU' . (count($hv['heads']) > 1 ? ', ' . count($hv['heads']) . ' zones' : '') : 'Ductless mini-split',
        'Windows / doors' => $set['openings']['windows'] . ' windows (SHGC 0.25 max.), ' . $set['openings']['doors'] . ' doors',
        'Files included' => 'PDF drawing set, DXF (CAD), CSV, OBJ (3D), PNG',
    ];
}
$GLOBALS['schema'][] = [
    '@type' => 'Product', '@id' => abs_url($p['url']) . '#plan', 'name' => $p['name'] . ' house plan', 'description' => $p['intro'], 'sku' => 'CTH-' . strtoupper($slug),
    'image' => array_values(array_filter([abs_url($p['image']), $slug === 'gonzales-modern-living' ? abs_url(img_url('3.webp')) : null])),
    'brand' => ['@id' => SITE_URL . '/#business'],
    'offers' => ['@type' => 'Offer', 'price' => (string)$p['price'], 'priceCurrency' => 'USD', 'availability' => 'https://schema.org/InStock',
        'url' => abs_url($p['url']), 'seller' => ['@id' => SITE_URL . '/#business']],
    'additionalProperty' => [
        ['@type' => 'PropertyValue', 'name' => 'Square feet', 'value' => $p['sqft']],
        ['@type' => 'PropertyValue', 'name' => 'Bedrooms', 'value' => $p['beds']],
        ['@type' => 'PropertyValue', 'name' => 'Bathrooms', 'value' => $p['baths']],
    ],
];
$fmtBytes = fn($b) => $b > 1e6 ? number_format($b / 1e6, 1) . ' MB' : number_format(max(1, $b / 1e3)) . ' KB';
$roomRows = function (array $rooms, string $suffix = '') {
    foreach ($rooms as [$label, $x, $y, $w, $d]) {
        echo '<tr><td>' . e(ucwords(strtolower($label))) . $suffix . '</td><td class="num">' . e(svg_ft($w) . ' x ' . svg_ft($d)) . '</td><td class="num">' . round($w * $d) . ' sq ft</td></tr>';
    }
};
$tabs = [['floor', $upper ? 'First floor' : 'Floor plan']];
if ($upper) $tabs[] = ['floor2', 'Second floor'];
$tabs = array_merge($tabs, [['elec', 'Electrical'], ['plumb', 'Plumbing'], ['elev', 'Elevations'], ['3d', '3D model']]);
[$ruleHead, $ruleText] = texas_rules($p);
$t = trail($GLOBALS['path']);
?>
<section class="hero hero--page plan-hero-band"><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><ol><?php foreach ($t as $i => [$label, $path]) echo $i === count($t) - 1 ? '<li aria-current="page">' . e($label) . '</li>' : '<li><a href="' . e($path) . '">' . e($label) . '</a></li>'; ?></ol></nav>
  <p class="eyebrow"><?= e(PLAN_CATEGORIES[$p['category']] . ' · ' . implode(' · ', $p['styles'])) ?></p>
  <h1><?= e($GLOBALS['plan_h1'] ?? $p['title']) ?></h1>
  <p class="lead"><?= e($p['intro']) ?></p>
</div></section>

<section class="section section--tight">
  <div class="wrap plan-top">
    <div class="plan-main">
      <figure class="img-frame plan-hero-img"><img src="<?= e($p['image']) ?>" width="1200" height="750" alt="<?= e($p['name']) ?> 3D rendering, front view"></figure>
      <ul class="plan-facts">
        <li><strong><?= number_format($p['sqft']) ?></strong><span>sq ft</span></li>
        <li><strong><?= e($p['beds'] ? (string)$p['beds'] : '—') ?></strong><span><?= $p['beds'] == 1 ? 'bedroom' : 'bedrooms' ?></span></li>
        <li><strong><?= e((string)$p['baths']) ?></strong><span>baths</span></li>
        <li><strong><?= $upper ? '2' : ($p['has_loft'] ? '1 + loft' : '1') ?></strong><span><?= $upper ? 'stories' : 'level' ?></span></li>
        <li><strong><?= e($p['width'] . ' x ' . $p['depth']) ?></strong><span>footprint</span></li>
      </ul>
    </div>
    <aside class="card buy-box" id="order">
      <p class="buy-kicker">Complete plan set · instant download</p>
      <p class="buy-price"><?= money($p['price']) ?></p>
      <?php if (($_GET['checkout'] ?? '') === 'canceled'): ?><div class="alert alert--err" role="status">Checkout was canceled. Your card was not charged.</div><?php endif; ?>
      <ul class="checklist">
        <?php if ($set): ?>
        <li><?= count($set['sheets']) ?>-sheet construction drawing set (24 x 36 PDF)</li>
        <li>Floor plan<?= $upper ? 's' : '' ?>, elevations, section, slab and roof framing</li>
        <li>Electrical plan, panel schedule, load calc and heat pump sizing</li>
        <li>Plumbing plan with supply, drain-waste-vent and fixture schedule</li>
        <li><?= $set['material_lines'] ?>-line materials list and Texas cost estimate</li>
        <li>CAD file (DXF), 3D model (OBJ) and images</li>
        <?php endif; ?>
        <li>License to build one home</li>
      </ul>
      <?php if ($buyOnline): ?>
      <form method="post" action="/order/checkout/">
        <input type="hidden" name="plan" value="<?= e($slug) ?>">
        <button class="btn btn--gold btn--block" type="submit">Buy &amp; download now</button>
      </form>
      <p class="form-note">Secure checkout by Stripe: cards, Apple Pay and Google Pay. Your download link appears on screen and by email.</p>
      <?php else: ?>
      <a class="btn btn--gold btn--block" href="<?= e($buyLink) ?>">Order this plan</a>
      <p class="form-note">Send the form and we will email a secure payment link and your files, or call <a href="<?= PHONE_HREF ?>"><?= PHONE ?></a>.</p>
      <?php endif; ?>
      <div class="buy-build">
        <strong>Want us to build it?</strong>
        <p><?= e(PLAN_CREDIT) ?></p>
        <a class="btn btn--outline btn--block btn--sm" href="<?= e($buildLink) ?>">Get a build quote</a>
      </div>
    </aside>
  </div>
</section>

<?php if ($set): ?>
<section class="section section--alt" id="plan-set">
  <div class="wrap">
    <div class="section-head"><h2>Inside <?= e($p['ref']) ?> plan set</h2>
      <p class="section-intro">Preview each drawing before you buy. The full set adds every dimension, the door, window, panel and fixture schedules, framing details and the Texas code notes on each sheet.</p></div>
    <div class="plan-tabs" data-tabs>
      <div class="plan-tab-list" role="tablist" aria-label="Plan set previews">
        <?php foreach ($tabs as $i => [$id, $label]): ?>
        <button role="tab" id="tab-<?= $id ?>" aria-controls="panel-<?= $id ?>" aria-selected="<?= $i ? 'false' : 'true' ?>"<?= $i ? ' tabindex="-1"' : '' ?><?= $id === '3d' ? ' data-3d-tab' : '' ?>><?= $label ?></button>
        <?php endforeach; ?>
      </div>
      <div class="plan-tab-panel" role="tabpanel" id="panel-floor" aria-labelledby="tab-floor">
        <figure class="plan-drawing"><img src="<?= $dir ?>/floor.svg" alt="<?= e($p['name'] . ' ' . ($upper ? 'first floor' : 'floor') . ' plan: ' . strtolower(implode(', ', array_column($p['rooms'], 0)))) ?>" loading="lazy"></figure>
        <div class="table-wrap"><table>
          <thead><tr><th>Room</th><th class="num">Size</th><th class="num">Area</th></tr></thead>
          <tbody><?php $roomRows($p['rooms']); $roomRows($p['loft'] ?? [], ' (loft)'); ?></tbody>
        </table></div>
      </div>
      <?php if ($upper): ?>
      <div class="plan-tab-panel" role="tabpanel" id="panel-floor2" aria-labelledby="tab-floor2" hidden>
        <figure class="plan-drawing"><img src="<?= $dir ?>/floor2.svg" alt="<?= e($p['name'] . ' second floor plan: ' . strtolower(implode(', ', array_column($p['upper'], 0)))) ?>" loading="lazy"></figure>
        <div class="table-wrap"><table>
          <thead><tr><th>Room</th><th class="num">Size</th><th class="num">Area</th></tr></thead>
          <tbody><?php $roomRows($p['upper']); ?></tbody>
        </table></div>
      </div>
      <?php endif; ?>
      <div class="plan-tab-panel" role="tabpanel" id="panel-elec" aria-labelledby="tab-elec" hidden>
        <figure class="plan-drawing"><img src="<?= $dir ?>/electrical.svg" alt="<?= e($p['name']) ?> electrical plan preview with receptacles, switches, lighting, ceiling fans and circuits" loading="lazy"></figure>
        <?php if ($upper): ?><figure class="plan-drawing"><img src="<?= $dir ?>/electrical2.svg" alt="<?= e($p['name']) ?> second floor electrical plan preview" loading="lazy"></figure><?php endif; ?>
        <ul class="stats plan-stats">
          <li class="stat"><strong><?= e(explode(',', $set['electrical']['service'])[0]) ?></strong><span>electrical service</span></li>
          <li class="stat"><strong><?= $set['electrical']['circuits'] ?></strong><span>circuits on the panel schedule</span></li>
          <li class="stat"><strong><?= $set['electrical']['fans'] ?></strong><span>ceiling fans</span></li>
          <li class="stat"><strong><?= $hv ? rtrim(rtrim(number_format($hv['outdoor_btu'] / 12000, 2), '0'), '.') : '—' ?> ton</strong><span>heat pump, <?= $hv ? count($hv['heads']) : 0 ?> head<?= $hv && count($hv['heads']) > 1 ? 's' : '' ?></span></li>
        </ul>
      </div>
      <div class="plan-tab-panel" role="tabpanel" id="panel-plumb" aria-labelledby="tab-plumb" hidden>
        <figure class="plan-drawing"><img src="<?= $dir ?>/plumbing.svg" alt="<?= e($p['name']) ?> plumbing plan preview with hot and cold supply and drain lines" loading="lazy"></figure>
        <?php if ($upper): ?><figure class="plan-drawing"><img src="<?= $dir ?>/plumbing2.svg" alt="<?= e($p['name']) ?> second floor plumbing plan preview" loading="lazy"></figure><?php endif; ?>
        <ul class="stats plan-stats">
          <li class="stat"><strong><?= $set['plumbing']['fixtures'] ?></strong><span>plumbing fixtures</span></li>
          <li class="stat"><strong><?= $set['plumbing']['dfu'] ?> DFU</strong><span>drainage fixture units</span></li>
          <li class="stat"><strong><?= e($set['plumbing']['drain']) ?></strong><span>building drain</span></li>
          <li class="stat"><strong><?= $set['plumbing']['water_heater'] === 'tank' ? 'Tank' : 'Tankless' ?></strong><span>electric water heater</span></li>
        </ul>
      </div>
      <div class="plan-tab-panel" role="tabpanel" id="panel-elev" aria-labelledby="tab-elev" hidden>
        <div class="elev-grid">
          <?php foreach (['front', 'rear', 'left', 'right'] as $f): ?>
          <figure class="plan-drawing"><img src="<?= $dir ?>/elevation-<?= $f ?>.svg" alt="<?= e($p['name'] . ' ' . $f) ?> elevation" loading="lazy"><figcaption><?= ucfirst($f) ?> elevation</figcaption></figure>
          <?php endforeach; ?>
        </div>
      </div>
      <div class="plan-tab-panel" role="tabpanel" id="panel-3d" aria-labelledby="tab-3d" hidden>
        <div class="viewer" data-model="<?= $dir ?>/model.json">
          <p class="viewer-status">Loading 3D model…</p>
          <canvas aria-label="Interactive 3D model of <?= e($p['name']) ?>. Drag to rotate, scroll or pinch to zoom."></canvas>
          <div class="viewer-tools">
            <button type="button" class="chip" data-3d="roof" aria-pressed="false">Roof off (see inside)</button>
            <button type="button" class="chip" data-3d="top">Top view</button>
            <button type="button" class="chip" data-3d="front">Front</button>
            <button type="button" class="chip" data-3d="reset">Reset</button>
          </div>
        </div>
        <p class="form-note">Drag to rotate, scroll or pinch to zoom.<?= $upper ? ' "Roof off" lifts the roof and the second floor to show the first floor.' : '' ?> The download includes this model as an OBJ file for SketchUp, Blender or Revit.</p>
      </div>
    </div>

    <div class="grid-2 set-contents">
      <div>
        <h3>Sheets in the drawing set</h3>
        <ul class="sheet-list"><?php foreach ($set['sheets'] as [$no, $title]): ?><li><span class="sheet-no"><?= e($no) ?></span> <?= e(ucwords(strtolower($title))) ?></li><?php endforeach; ?></ul>
      </div>
      <div>
        <h3>Files in your download (<?= $fmtBytes($set['zip_bytes']) ?> zip)</h3>
        <ul class="file-list">
          <?php foreach ($set['files'] as [$name, $bytes]): if (strpos($name, 'Images/') === 0) continue; ?>
          <li><span><?= e($name) ?></span><span class="muted"><?= $fmtBytes($bytes) ?></span></li>
          <?php endforeach; ?>
          <li><span>Images/ (<?= count(array_filter($set['files'], fn($f) => strpos($f[0], 'Images/') === 0)) ?> PNG renders and drawings)</span><span class="muted"><?= $fmtBytes(array_sum(array_map(fn($f) => strpos($f[0], 'Images/') === 0 ? $f[1] : 0, $set['files']))) ?></span></li>
        </ul>
      </div>
    </div>
  </div>
</section>
<?php endif; ?>

<section class="section">
  <div class="wrap grid-2 plan-detail">
    <div class="prose">
      <h2>Floor plan highlights</h2>
      <ul class="checklist"><?php foreach ($p['layout'] as $l): ?><li><?= e($l) ?></li><?php endforeach; ?></ul>
      <h2>Key features</h2>
      <ul><?php foreach ($p['features'] as $f): ?><li><?= e($f) ?></li><?php endforeach; ?></ul>
      <div class="callout"><p><strong>Texas tip:</strong> <?= e($p['texas']) ?></p></div>
    </div>
    <div>
      <h2>Plan specifications</h2>
      <div class="table-wrap"><table class="spec-table"><tbody>
        <?php foreach ($specs as $k => $v): ?><tr><th scope="row"><?= e($k) ?></th><td><?= e((string)$v) ?></td></tr><?php endforeach; ?>
      </tbody></table></div>
    </div>
  </div>
</section>

<?php if (isset($GLOBALS['plan_story'])) ($GLOBALS['plan_story'])(); ?>

<section class="section section--ink build-band">
  <div class="wrap grid-2">
    <div>
      <p class="eyebrow">Design-build in Texas</p>
      <h2>Have Cowboy Tiny Homes build it</h2>
      <p>We build our plans across San Antonio, Austin, Dallas, Fort Worth, Houston and rural Texas: site visit, permit drawings sealed by a Texas engineer where required, the slab designed from your geotechnical report, and construction by one team.</p>
      <p><strong><?= e(PLAN_CREDIT) ?></strong></p>
      <div class="btn-row"><a class="btn btn--gold" href="<?= e($buildLink) ?>">Get a free build quote</a><a class="btn btn--ghost" href="<?= PHONE_HREF ?>">Call <?= PHONE ?></a></div>
    </div>
    <ol class="steps build-steps">
      <li><strong>Free consult</strong> We look at your land, budget and timeline.</li>
      <li><strong>Site & feasibility</strong> Zoning, utilities, soils and, on the coast, windstorm rules.</li>
      <li><strong>Permit set</strong> We adapt this plan to your lot and get it engineered.</li>
      <li><strong>Build</strong> One crew from slab to move-in.</li>
    </ol>
  </div>
</section>

<section class="section section--alt" id="cost">
  <div class="wrap">
  <?php if ($est): ?>
    <div class="section-head"><h2>What will <?= e($p['name']) ?> cost to build in Texas?</h2>
      <p class="section-intro">Built from this plan's own <?= $set['material_lines'] ?>-line materials takeoff plus labor by trade, then adjusted for each Texas market. Pick your area and finish level.</p></div>
    <div class="cost-tool" data-cost='<?= e(json_encode(['cats' => $est['categories'], 'permits' => $est['permits'], 'sqft' => $est['sqft']])) ?>'>
      <div class="cost-controls card">
        <div class="field"><label for="c-region">Where in Texas?</label>
          <select id="c-region"><?php foreach ($est['regions'] as [$name, $f]): ?><option value="<?= $f ?>"<?= $name === 'San Antonio metro' ? ' selected' : '' ?>><?= e($name) ?></option><?php endforeach; ?></select></div>
        <div class="field"><label for="c-finish">Finish level</label>
          <select id="c-finish"><option value="0.85">Basic</option><option value="1" selected>Mid-range (as specified)</option><option value="1.35">High-end</option></select></div>
        <div class="field"><span class="field-label">Who builds it?</span>
          <div class="chips"><button type="button" class="chip" data-build="diy" aria-pressed="false">Owner-builder</button><button type="button" class="chip" data-build="gc" aria-pressed="true">Builder (like us)</button></div></div>
        <div class="cost-total"><span>Estimated build cost</span><strong data-out="total"><?= money($est['gc_total']) ?></strong><span data-out="psf"><?= money($est['gc_psf']) ?> per sq ft</span></div>
        <p class="form-note">Excludes land, utility connections, driveway, the geotechnical report and engineering<?= $p['mobile'] ? ', and the tow vehicle' : '' ?>. Coastal sites add windstorm upgrades. A planning estimate, not a bid.</p>
      </div>
      <div class="cost-bars" aria-live="polite">
        <?php foreach ($est['categories'] as $c): ?>
        <div class="bar-row" data-cat="<?= e($c['name']) ?>"><span class="bar-label"><?= e($c['name']) ?></span><span class="bar-track"><span class="bar-m"></span><span class="bar-l"></span></span><span class="bar-val"><?= money($c['materials'] + $c['labor']) ?></span></div>
        <?php endforeach; ?>
        <p class="bar-key"><span class="key-m"></span> Materials <span class="key-l"></span> Labor</p>
      </div>
    </div>
    <p class="btn-row"><a class="btn btn--sm btn--outline" href="/tools/tiny-home-cost-calculator/">Open the full cost calculator</a><a class="btn btn--sm btn--ink" href="<?= e($buildLink) ?>">Get an exact quote from us</a></p>
  <?php endif; ?>
  </div>
</section>

<?php if ($set): ?>
<section class="section" id="materials">
  <div class="wrap">
    <div class="section-head"><h2><?= e($p['name']) ?> materials list</h2>
      <p class="section-intro">Every plan set includes a <?= $set['material_lines'] ?>-line takeoff with quantities, units and prices, ready to send to a lumberyard for a quote. The summary by category:</p></div>
    <div class="table-wrap"><table class="materials-table">
      <thead><tr><th>Category</th><th class="num">Lines</th><th>Includes</th><th class="num">Materials</th></tr></thead>
      <tbody>
      <?php foreach ($set['materials'] as $c): ?>
        <tr><td><strong><?= e($c['name']) ?></strong></td><td class="num"><?= $c['lines'] ?></td><td class="muted"><?= e(implode('; ', array_map(fn($x) => trim(preg_replace('/\s*\(.*?\)\s*/', ' ', $x)), array_slice($c['examples'], 0, 3)))) ?><?= $c['lines'] > 3 ? '…' : '' ?></td><td class="num"><?= money($c['total']) ?></td></tr>
      <?php endforeach; ?>
        <tr><td><strong>Total materials</strong></td><td class="num"><?= $set['material_lines'] ?></td><td></td><td class="num"><strong><?= money($est['materials']) ?></strong></td></tr>
      </tbody>
    </table></div>
  </div>
</section>
<?php endif; ?>

<section class="section section--alt">
  <div class="wrap">
    <div class="section-head"><h2>Built for Texas</h2></div>
    <div class="grid-2">
      <div class="prose">
        <h3><?= e($ruleHead) ?></h3>
        <p><?= $ruleText ?></p>
        <h3>Permits, stamps and engineering</h3>
        <p>The drawing set is organized the way Texas building departments expect: a cover sheet with code, load and climate notes, plans, elevations, a section, the slab, framing, electrical and plumbing. These are planning drawings, not stamped construction documents. Many cities, lenders and insurers will ask for a Texas-licensed engineer's or architect's seal, a site plan and energy-code forms, so plan for that review before you build.</p>
      </div>
      <div>
        <ul class="texas-notes">
          <?php foreach (texas_build_notes($p) as [$h, $txt]): ?><li><strong><?= e($h) ?></strong><span><?= e($txt) ?></span></li><?php endforeach; ?>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section"><div class="wrap">
  <div class="section-head"><h2>Similar Texas house plans</h2></div>
  <?php plan_grid($others); ?>
  <p class="btn-row"><a class="btn btn--outline" href="/home-designs/">Browse all <?= count($PLANS) ?> plans</a></p>
</div></section>

<?php
faq_section([
    ['What comes with ' . $p['ref'] . ' plan set?', $set
        ? '<p>One zip file with a ' . count($set['sheets']) . '-sheet construction drawing set (24 x 36 in. PDF: cover with Texas code notes, floor plan' . ($upper ? 's for both floors' : '') . ($p['has_loft'] ? ', loft plan' : '') . ', elevations, section, ' . ($p['mobile'] ? 'trailer' : 'foundation') . ', roof framing, electrical, plumbing, materials list and cost estimate), a DXF CAD file, the materials list and cost estimate as spreadsheets (CSV), a 3D model (OBJ) and PNG images.</p>'
        : '<p>A full construction drawing set (PDF), a CAD file, the materials list and cost estimate, and a 3D model.</p>'],
    ['Will Cowboy Tiny Homes build ' . $p['name'] . ' for me?', '<p>Yes. We build our plans across Texas. ' . e(PLAN_CREDIT) . ' <a href="' . e($buildLink) . '">Ask for a build quote</a>.</p>'],
    ['How do I get the files after I pay?', $buyOnline
        ? '<p>Right away. After checkout you land on a download page, and we email the same link. It works for a year and up to ' . DOWNLOAD_MAX . ' downloads, and you can get a fresh link at <a href="/order/lookup/">Find my plan download</a>.</p>'
        : '<p>Send the order form on this page or call ' . PHONE . '. We confirm your plan, send a secure payment link and email the files.</p>'],
    ['Are these plans stamped or permit-ready in Texas?', '<p>No. They are planning and permit-development drawings, not stamped documents. Texas cities that require a permit review plans under the IRC with their own amendments, and many want a Texas-licensed engineer\'s seal, especially on the slab and on coastal wind design. We can arrange that, or your own engineer or architect can review and stamp the set.</p>'],
    ['Does ' . $p['name'] . ' work on the Gulf Coast?', '<p>With an upgrade. The plans assume 115 mph inland design wind. Houston-area and coastal sites need engineered wind design, impact-rated or protected windows, and, inside the Texas Department of Insurance catastrophe area, TDI windstorm certification (WPI-8).</p>'],
    ['Can ' . $p['name'] . ' be modified?', '<p>Yes. We can flip the layout, change room sizes, swap the slab for pier-and-beam, or add a porch. <a href="' . e($modLink) . '">Ask for a modification quote</a>.</p>'],
    ['What does the license allow?', '<p>Your purchase includes a license to build one home from the plan. You can print and share the drawings with your builder, lender and permit office for that build. See the <a href="/terms-of-sale/">terms of sale</a>.</p>'],
], $p['name'] . ' FAQs');
cta_band('Build ' . $p['name'] . ' in Texas', 'Talk with Cowboy Tiny Homes about building this plan on your land, or tailoring it to fit. Free consultation.');
