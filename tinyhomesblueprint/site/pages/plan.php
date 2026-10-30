<?php
require_once __DIR__ . '/../inc/plan-svg.php';
require_once __DIR__ . '/../inc/store.php';
$slug = $ROUTE['plan'];
$p = $PLANS[$slug];
$set = plan_sets()[$slug] ?? null;
$dir = "/assets/plans/$slug";
$has3d = $set && is_file(__DIR__ . "/..$dir/3d.webp");
$buyOnline = store_ready($slug);

// Similar plans: most shared styles first, then closest in size.
$others = array_filter(array_keys($PLANS), fn($s) => $s !== $slug);
usort($others, function ($a, $b) use ($PLANS, $p) {
    $sa = count(array_intersect($PLANS[$a]['styles'], $p['styles'])); $sb = count(array_intersect($PLANS[$b]['styles'], $p['styles']));
    return $sb <=> $sa ?: abs($PLANS[$a]['sqft'] - $p['sqft']) <=> abs($PLANS[$b]['sqft'] - $p['sqft']);
});
$others = array_slice($others, 0, 3);

$specs = [
    'Plan number' => $p['name'], 'Total living area' => number_format($p['sqft']) . ' sq ft',
];
if ($p['loft_sqft']) $specs += ['Main floor' => number_format($p['main_sqft']) . ' sq ft', 'Loft' => $p['loft_sqft'] . ' sq ft'];
$specs += [
    'Bedrooms' => $p['beds'], 'Bathrooms' => $p['baths'], 'Levels' => $p['has_loft'] ? 'Main floor + loft' : ($p['floors'] > 1 ? $p['floors'] . ' floors' : 'Single level'),
    'Footprint' => $p['width'] . ' x ' . $p['depth'], 'Overall height' => $p['height'], 'Ceiling height' => $p['ceiling'],
    'Roof' => $p['roof'], 'Exterior walls' => $p['walls'], 'Foundation' => $p['foundation'],
];
if ($set) $specs += [
    'Electrical' => $set['electrical']['service'] . ', ' . $set['electrical']['circuits'] . ' circuits',
    'Heating & cooling' => 'Ductless mini-split heat pump' . ($set['electrical']['hvac_heads'] > 1 ? ' (' . $set['electrical']['hvac_heads'] . ' zones)' : ''),
    'Windows / doors' => $set['openings']['windows'] . ' windows, ' . $set['openings']['doors'] . ' doors',
    'Files included' => 'PDF drawing set, DXF (CAD), CSV, OBJ (3D), PNG',
];
// Plans drawn from geometry show the 3D render up top; the two photo plans keep their photo.
$image = $has3d && substr($p['image'], -4) === '.svg' ? "$dir/3d.webp" : $p['image'];
$schema = [
    '@context' => 'https://schema.org', '@type' => 'Product', 'name' => $p['name'] . ' - ' . $p['title'],
    'description' => $p['intro'], 'sku' => $p['name'],
    'image' => array_values(array_filter([abs_url($p['image']), $has3d ? abs_url("$dir/3d.webp") : null])),
    'brand' => ['@type' => 'Brand', 'name' => SITE_NAME],
    'offers' => ['@type' => 'Offer', 'price' => $p['price'], 'priceCurrency' => 'USD', 'availability' => 'https://schema.org/InStock',
        'url' => abs_url($PATH), 'seller' => ['@id' => SITE_URL . '/#org']],
    'additionalProperty' => [
        ['@type' => 'PropertyValue', 'name' => 'Square feet', 'value' => $p['sqft']],
        ['@type' => 'PropertyValue', 'name' => 'Bedrooms', 'value' => $p['beds']],
        ['@type' => 'PropertyValue', 'name' => 'Bathrooms', 'value' => $p['baths']],
    ],
];
$order = '/contact/?plan=' . urlencode($p['name']) . '#form';
$est = $set['estimate'] ?? null;
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', '/tiny-house-plans/'], [$p['name'], null]],
    'schema' => [$schema],
    'og_image' => $has3d ? abs_url("$dir/3d.webp") : (substr($p['image'], -4) === '.svg' ? null : abs_url($p['image'])),
]);
$fmtBytes = fn($b) => $b > 1e6 ? number_format($b / 1e6, 1) . ' MB' : number_format(max(1, $b / 1e3)) . ' KB';
?>
<section class="section" style="padding-top:28px">
  <div class="wrap plan-hero">
    <div>
      <p class="eyebrow"><?= e($p['name']) ?></p>
      <h1><?= e($p['title']) ?></h1>
      <p class="lead"><?= e($p['intro']) ?></p>
      <img src="<?= e($image) ?>" width="<?= $image === "$dir/3d.webp" ? 1200 : 800 ?>" height="<?= $image === "$dir/3d.webp" ? 750 : 430 ?>" alt="<?= e($p['name'] . ($image === "$dir/3d.webp" ? ' 3D rendering' : (isset($p['rooms']) && substr($p['image'], -4) === '.svg' ? ' front elevation drawing' : ' rendering')) . ': ' . $p['title']) ?>">
      <ul class="plan-specs" style="font-size:1rem;margin-top:18px">
        <li><?= icon('ruler') ?> <?= number_format($p['sqft']) ?> sq ft</li>
        <li><?= icon('bed') ?> <?= $p['beds'] ?> bedroom<?= $p['beds'] > 1 ? 's' : '' ?></li>
        <li><?= icon('bath') ?> <?= $p['baths'] ?> bath<?= $p['baths'] > 1 ? 's' : '' ?></li>
        <li><?= icon('stairs') ?> <?= $p['has_loft'] ? 'Loft' : ($p['floors'] > 1 ? $p['floors'] . ' floors' : '1 level') ?></li>
        <li><?= icon('layout') ?> <?= e($p['width'] . ' x ' . $p['depth']) ?></li>
        <?php if ($p['mobile']): ?><li><?= icon('wheels') ?> On wheels</li><?php endif; ?>
      </ul>
    </div>
    <aside class="panel buy-box" id="order">
      <p class="plan-no">Complete plan set &middot; instant download</p>
      <span class="price"><?= money($p['price']) ?></span>
      <?php if (($_GET['checkout'] ?? '') === 'canceled'): ?><div class="alert alert-err" role="status" style="margin-bottom:12px">Checkout was canceled. Your card was not charged.</div><?php endif; ?>
      <ul class="check-list">
        <?php if ($set): ?>
        <li><?= count($set['sheets']) ?>-sheet construction drawing set (24 x 36 PDF)</li>
        <li>Floor plan, elevations, section, foundation and roof framing</li>
        <li>Electrical plan with panel schedule and load calc</li>
        <li>Plumbing plan: supply, drain-waste-vent, fixture schedule</li>
        <li><?= $set['material_lines'] ?>-line materials list and cost estimate</li>
        <li>CAD file (DXF), 3D model (OBJ) and images</li>
        <?php else: ?>
        <li>Dimensioned floor plan and elevations</li>
        <li>Roof and wall framing specifications</li>
        <li>PDF, CAD and image files</li>
        <?php endif; ?>
        <li>License to build one home</li>
      </ul>
      <?php if ($buyOnline): ?>
      <form method="post" action="/order/checkout/">
        <input type="hidden" name="plan" value="<?= e($slug) ?>">
        <button class="btn btn-wood" type="submit"><?= icon('file') ?> Buy &amp; download now</button>
      </form>
      <p class="form-note secure-note"><?= icon('shield') ?> Secure checkout by Stripe. Cards, Apple Pay and Google Pay. Download link on screen and by email.</p>
      <a class="btn btn-outline" href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> Questions? <?= SITE_PHONE ?></a>
      <?php else: ?>
      <a class="btn btn-wood" href="<?= e($order) ?>">Order this plan</a>
      <a class="btn btn-outline" href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> Order by phone</a>
      <?php endif; ?>
      <p class="form-note">Want changes? <a href="<?= e($order) ?>">Ask for a modification quote</a>.</p>
    </aside>
  </div>
</section>

<?php if ($set): ?>
<section class="section section-alt" id="plan-set">
  <div class="wrap">
    <div class="section-head"><h2>Inside the <?= e($p['name']) ?> plan set</h2>
      <p class="lead">Preview every drawing type before you buy. The purchased set adds the full dimensions, door and window schedules, panel and fixture schedules, framing details and notes on each sheet.</p></div>
    <div class="tabs" data-tabs>
      <div class="tab-list" role="tablist" aria-label="Plan set previews">
        <button role="tab" id="tab-floor" aria-controls="panel-floor" aria-selected="true">Floor plan</button>
        <button role="tab" id="tab-elec" aria-controls="panel-elec" aria-selected="false" tabindex="-1">Electrical</button>
        <button role="tab" id="tab-plumb" aria-controls="panel-plumb" aria-selected="false" tabindex="-1">Plumbing</button>
        <button role="tab" id="tab-elev" aria-controls="panel-elev" aria-selected="false" tabindex="-1">Elevations</button>
        <button role="tab" id="tab-3d" aria-controls="panel-3d" aria-selected="false" tabindex="-1" data-3d-tab>3D model</button>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-floor" aria-labelledby="tab-floor">
        <figure class="plan-drawing"><img src="<?= $dir ?>/floor.svg" alt="<?= e($p['name'] . ' floor plan: ' . implode(', ', array_map(fn($r) => strtolower($r[0]), $p['rooms']))) ?>" loading="lazy"></figure>
        <div class="table-wrap"><table>
          <thead><tr><th>Room</th><th class="num">Size</th><th class="num">Area</th></tr></thead>
          <tbody>
          <?php foreach ($p['rooms'] as [$label, $x, $y, $w, $d]): ?>
            <tr><td><?= e(ucwords(strtolower($label))) ?></td><td class="num"><?= e(svg_ft($w) . ' x ' . svg_ft($d)) ?></td><td class="num"><?= round($w * $d) ?> sq ft</td></tr>
          <?php endforeach; foreach ($p['loft'] ?? [] as [$label, $x, $y, $w, $d]): ?>
            <tr><td><?= e(ucwords(strtolower($label))) ?> (upper level)</td><td class="num"><?= e(svg_ft($w) . ' x ' . svg_ft($d)) ?></td><td class="num"><?= round($w * $d) ?> sq ft</td></tr>
          <?php endforeach; ?>
          </tbody>
        </table></div>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-elec" aria-labelledby="tab-elec" hidden>
        <figure class="plan-drawing"><img src="<?= $dir ?>/electrical.svg" alt="<?= e($p['name']) ?> electrical plan preview with receptacles, switches, lighting and circuits" loading="lazy"></figure>
        <ul class="stat-row">
          <li><strong><?= e($set['electrical']['service']) ?></strong><span>service</span></li>
          <li><strong><?= $set['electrical']['circuits'] ?></strong><span>branch circuits, panel schedule included</span></li>
          <li><strong><?= $set['electrical']['receptacles'] ?></strong><span>receptacles (GFCI where required)</span></li>
          <li><strong><?= $set['electrical']['lights'] ?></strong><span>light fixtures and fans</span></li>
          <li><strong><?= $set['electrical']['alarms'] ?></strong><span>smoke / CO alarms</span></li>
        </ul>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-plumb" aria-labelledby="tab-plumb" hidden>
        <figure class="plan-drawing"><img src="<?= $dir ?>/plumbing.svg" alt="<?= e($p['name']) ?> plumbing plan preview with hot and cold supply and drain lines" loading="lazy"></figure>
        <ul class="stat-row">
          <li><strong><?= $set['plumbing']['fixtures'] ?></strong><span>plumbing fixtures</span></li>
          <li><strong><?= $set['plumbing']['dfu'] ?> DFU</strong><span>drainage fixture units</span></li>
          <li><strong><?= e($set['plumbing']['drain']) ?></strong><span>building drain</span></li>
          <li><strong><?= $set['plumbing']['water_heater'] === 'tank' ? 'Tank' : 'Tankless' ?></strong><span>electric water heater</span></li>
          <li><strong>PEX + PVC</strong><span>supply and DWV, sized per IPC</span></li>
        </ul>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-elev" aria-labelledby="tab-elev" hidden>
        <div class="elev-grid">
          <?php foreach (['front', 'rear', 'left', 'right'] as $f): ?>
          <figure class="plan-drawing"><img src="<?= $dir ?>/elevation-<?= $f ?>.svg" alt="<?= e($p['name'] . ' ' . $f) ?> elevation" loading="lazy"><figcaption><?= ucfirst($f) ?> elevation</figcaption></figure>
          <?php endforeach; ?>
        </div>
      </div>
      <div class="tab-panel" role="tabpanel" id="panel-3d" aria-labelledby="tab-3d" hidden>
        <div class="viewer" data-model="<?= $dir ?>/model.json">
          <p class="viewer-status">Loading 3D model&hellip;</p>
          <canvas aria-label="Interactive 3D model of <?= e($p['name']) ?>. Drag to rotate, scroll or pinch to zoom."></canvas>
          <div class="viewer-tools">
            <button type="button" class="chip" data-3d="roof" aria-pressed="false">Roof off (see inside)</button>
            <button type="button" class="chip" data-3d="top">Top view</button>
            <button type="button" class="chip" data-3d="front">Front</button>
            <button type="button" class="chip" data-3d="reset">Reset</button>
          </div>
        </div>
        <p class="form-note">Drag to rotate, scroll or pinch to zoom. The download includes this model as an OBJ file for SketchUp, Blender or Revit.</p>
      </div>
    </div>

    <div class="two-col top set-contents">
      <div>
        <h3>Sheets in the drawing set</h3>
        <ul class="sheet-list">
          <?php foreach ($set['sheets'] as [$no, $title]): ?><li><span class="sheet-no"><?= e($no) ?></span> <?= e(ucwords(strtolower($title))) ?></li><?php endforeach; ?>
        </ul>
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
  <div class="wrap two-col top">
    <div class="prose">
      <h2>Floor plan highlights</h2>
      <ul class="check-list"><?php foreach ($p['layout'] as $l): ?><li><?= e($l) ?></li><?php endforeach; ?></ul>
      <h2>Key features</h2>
      <ul><?php foreach ($p['features'] as $f): ?><li><?= e($f) ?></li><?php endforeach; ?></ul>
    </div>
    <div>
      <h2>Plan specifications</h2>
      <div class="table-wrap"><table class="spec-table"><tbody>
        <?php foreach ($specs as $k => $v): ?><tr><th scope="row"><?= e($k) ?></th><td><?= e($v) ?></td></tr><?php endforeach; ?>
      </tbody></table></div>
    </div>
  </div>
</section>

<section class="section section-alt" id="cost">
  <div class="wrap">
  <?php if ($est): ?>
    <div class="section-head"><h2>What will <?= e($p['name']) ?> cost to build?</h2>
      <p class="lead">This estimate is built from the plan's own materials takeoff (<?= $set['material_lines'] ?> line items) at 2026 US average prices, plus labor by trade. Adjust it for your region and finishes.</p></div>
    <div class="cost-tool" data-cost='<?= e(json_encode(['cats' => $est['categories'], 'permits' => $est['permits'], 'sqft' => $est['sqft']])) ?>'>
      <div class="cost-controls panel">
        <div class="field"><label for="c-region">Region</label>
          <select id="c-region"><option value="0.86">Lower-cost area (rural South, Midwest)</option><option value="1" selected>US average</option><option value="1.18">Higher-cost area (Northeast, Mountain West)</option><option value="1.42">Very high cost (coastal CA, NYC, Seattle)</option></select></div>
        <div class="field"><label for="c-finish">Finish level</label>
          <select id="c-finish"><option value="0.85">Basic</option><option value="1" selected>Mid-range (as specified)</option><option value="1.35">High-end</option></select></div>
        <div class="field"><span class="label">Who builds it?</span>
          <div class="chip-row" style="margin:0"><button type="button" class="chip" data-build="diy" aria-pressed="false">Owner-builder</button><button type="button" class="chip" data-build="gc" aria-pressed="true">General contractor</button></div></div>
        <div class="cost-total"><span class="muted">Estimated build cost</span><strong data-out="total"><?= money($est['gc_total']) ?></strong><span data-out="psf" class="muted"><?= money($est['gc_psf']) ?> per sq ft</span></div>
        <p class="form-note">Excludes land, utility connections, site work beyond grading<?= $p['mobile'] ? ', and the tow vehicle' : '' ?>. Owner-builder totals include licensed help for electrical, plumbing and HVAC rough-in.</p>
      </div>
      <div class="cost-bars" aria-live="polite">
        <?php foreach ($est['categories'] as $c): ?>
        <div class="bar-row" data-cat="<?= e($c['name']) ?>"><span class="bar-label"><?= e($c['name']) ?></span><span class="bar"><span class="bar-m"></span><span class="bar-l"></span></span><span class="bar-val"><?= money($c['materials'] + $c['labor']) ?></span></div>
        <?php endforeach; ?>
        <p class="bar-key"><span class="key-m"></span> Materials <span class="key-l"></span> Labor</p>
      </div>
    </div>
    <p class="mt-2"><a class="btn btn-sm btn-outline" href="/tools/tiny-house-cost-calculator/">Try the full cost calculator</a></p>
  <?php else: ?>
    <div class="prose">
      <h2>What will <?= e($p['name']) ?> cost to build?</h2>
      <p>Using typical 2026 costs of $150&ndash;$330 per sq ft for an owner-built home and $250&ndash;$500 per sq ft with a builder, a <?= number_format($p['sqft']) ?> sq ft house like <?= e($p['name']) ?> generally falls between <strong><?= money($p['sqft'] * 150) ?> and <?= money($p['sqft'] * 330) ?></strong> owner-built, or <strong><?= money($p['sqft'] * 250) ?> to <?= money($p['sqft'] * 500) ?></strong> with a general contractor, before <?= $p['mobile'] ? 'the trailer, ' : '' ?>land, utilities and site work.</p>
      <p><a class="btn btn-sm" href="/tools/tiny-house-cost-calculator/">Estimate it in the cost calculator</a></p>
    </div>
  <?php endif; ?>
  </div>
</section>

<?php if ($set): ?>
<section class="section" id="materials">
  <div class="wrap">
    <div class="section-head"><h2><?= e($p['name']) ?> materials list</h2>
      <p class="lead">Every plan set includes a <?= $set['material_lines'] ?>-line takeoff with quantities, units and prices, ready to send to a lumberyard or supplier for a quote. Here is the summary by category.</p></div>
    <div class="table-wrap"><table class="materials-table">
      <thead><tr><th>Category</th><th class="num">Line items</th><th>Includes</th><th class="num">Materials</th></tr></thead>
      <tbody>
      <?php foreach ($set['materials'] as $c): ?>
        <tr><td><strong><?= e($c['name']) ?></strong></td><td class="num"><?= $c['lines'] ?></td><td class="muted"><?= e(implode('; ', array_map(fn($x) => preg_replace('/\s*\(.*?\)\s*/', ' ', $x), array_slice($c['examples'], 0, 3)))) ?><?= $c['lines'] > 3 ? '&hellip;' : '' ?></td><td class="num"><?= money($c['total']) ?></td></tr>
      <?php endforeach; ?>
        <tr><td><strong>Total materials</strong></td><td class="num"><?= $set['material_lines'] ?></td><td></td><td class="num"><strong><?= money($est['materials']) ?></strong></td></tr>
      </tbody>
    </table></div>
  </div>
</section>
<?php endif; ?>

<section class="section<?= $set ? ' section-alt' : '' ?>">
  <div class="wrap two-col top">
    <div class="prose">
      <h2>Where this plan works</h2>
      <?php if ($p['mobile']): ?>
      <p>This is a tiny house on wheels, drawn to the common road limits of 8.5 ft wide and 13.5 ft tall. Check your state's height limit and your trailer's GVWR before you build. The <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a> estimates the finished weight, and the <a href="/blog/tiny-house-zoning-laws/">zoning guide</a> covers where a tiny house on wheels can be parked and lived in.</p>
      <?php else: ?>
      <p>This plan is designed for a permanent foundation (<?= e(lcfirst($p['foundation'])) ?>), so it is reviewed like any other small house. Where local rules allow units of this size, it can also serve as an <a href="/adu-plans/">ADU or backyard cottage</a>. Check <a href="/blog/tiny-house-zoning-laws/">tiny house zoning rules</a> and minimum dwelling sizes in your county before you build.</p>
      <?php endif; ?>
    </div>
    <div class="prose">
      <h2>Permits and engineering</h2>
      <p>The drawing set is organized the way building departments expect: cover sheet with code and load notes, plans, elevations, a section, foundation, framing, electrical and plumbing. Many jurisdictions will also ask for a local engineer's or architect's stamp, energy-code forms or a site plan, so plan for that review.</p>
      <p>Explore similar designs: <?php foreach ($p['styles'] as $i => $s) { echo ($i ? ', ' : '') . '<a href="/' . e($s) . '/">' . e($ROUTES["/$s/"]['nav']) . '</a>'; } ?>.</p>
    </div>
  </div>
</section>

<section class="section"><div class="wrap">
  <h2>Similar tiny house plans</h2>
  <?php plan_grid($others, false); ?>
  <p class="mt-2"><a class="btn btn-outline" href="/tiny-house-plans/">Browse all <?= count($PLANS) ?> plans <?= icon('arrow') ?></a></p>
</div></section>

<section class="section section-alt"><div class="narrow">
<?php faq_block([
    ['What files come with ' . $p['name'] . '?', $set
        ? '<p>One zip file with a ' . count($set['sheets']) . '-sheet construction drawing set (24 x 36 in. PDF: cover, floor plan' . ($p['has_loft'] ? ', loft plan' : '') . ', elevations, section, foundation, roof framing, electrical, plumbing, materials list and cost estimate), a DXF CAD file, the materials list and cost estimate as spreadsheets (CSV), a 3D model (OBJ) and PNG images.</p>'
        : '<p>The plan set includes the drawings as PDF, CAD and image files: a dimensioned floor plan, exterior elevations and roof and wall framing specifications.</p>'],
    ['How do I get the files after I pay?', $buyOnline
        ? '<p>Instantly. After checkout you land on a download page, and we email the same link. The link works for a year and up to ' . DOWNLOAD_MAX . ' downloads, and you can request a fresh one any time from <a href="/order/lookup/">Find my plan download</a>.</p>'
        : '<p>Use the order button on this page or call ' . SITE_PHONE . '. We confirm your plan and file needs, send a secure payment link and deliver the files by email.</p>'],
    ['Are these plans stamped or permit-ready everywhere?', '<p>No plan is permit-ready in every jurisdiction. The set includes the sheets most building departments ask for, but codes, snow and wind loads, and energy rules vary. Have a local engineer or architect review it and stamp it if your jurisdiction requires that.</p>'],
    ['Can ' . $p['name'] . ' be modified?', '<p>Yes. Tiny Homes Blueprint can flip the layout, adjust room sizes, add or remove a loft, or change the ' . ($p['mobile'] ? 'trailer length' : 'foundation') . '. <a href="' . e($order) . '">Request a modification quote</a>.</p>'],
    $p['mobile']
        ? ['Can ' . $p['name'] . ' be built on a foundation instead?', '<p>Yes. Many owners build a trailer plan on piers or a slab, which can open up a wider range of permit options. Tell us your site and we will note what changes, such as the floor framing and tie-downs.</p>']
        : ['Can I build ' . $p['name'] . ' on a trailer?', '<p>No. At ' . e($p['depth']) . ' deep it is wider than the 8.5 ft road limit and is designed for a permanent foundation. For road-legal designs, see our <a href="/tiny-house-on-wheels-plans/">tiny house on wheels plans</a>.</p>'],
    ['What does the license allow?', '<p>Your purchase includes a license to build one home from the plan. You can print and share the drawings with your builder, lender and permit office for that build. See the <a href="/terms-conditions/">terms</a> for details.</p>'],
]); ?>
</div></section>
<?php cta_band('Questions about ' . $p['name'] . '?', 'Call Tiny Homes Blueprint or send a message. We answer within one business day.', 'Ask about this plan', $order); ?>
<?php if ($set): ?><script type="module" src="<?= asset('/assets/js/plan-page.js') ?>"></script><?php endif; ?>
<?php page_end(); ?>
