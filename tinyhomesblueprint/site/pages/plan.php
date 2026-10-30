<?php
require_once __DIR__ . '/../inc/plan-svg.php';
$slug = $ROUTE['plan'];
$p = $PLANS[$slug];

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
    'Files included' => 'PDF, CAD and image files',
];
$schema = [
    '@context' => 'https://schema.org', '@type' => 'Product', 'name' => $p['name'] . ' - ' . $p['title'],
    'description' => $p['intro'], 'sku' => $p['name'], 'image' => abs_url($p['image']),
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
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', '/tiny-house-plans/'], [$p['name'], null]],
    'schema' => [$schema],
    'og_image' => substr($p['image'], -4) === '.svg' ? null : abs_url($p['image']),
]);
?>
<section class="section" style="padding-top:28px">
  <div class="wrap plan-hero">
    <div>
      <p class="eyebrow"><?= e($p['name']) ?></p>
      <h1><?= e($p['title']) ?></h1>
      <p class="lead"><?= e($p['intro']) ?></p>
      <img src="<?= e($p['image']) ?>" width="800" height="430" alt="<?= e($p['name'] . (isset($p['rooms']) ? ' front elevation drawing' : ' rendering') . ': ' . $p['title']) ?>">
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
      <p class="plan-no">Complete plan set</p>
      <span class="price"><?= money($p['price']) ?></span>
      <ul class="check-list">
        <li>Dimensioned floor plan and elevations</li>
        <li>Roof and wall framing specifications</li>
        <li>PDF, CAD and image files</li>
        <li>Delivered digitally after order confirmation</li>
      </ul>
      <a class="btn btn-wood" href="<?= e($order) ?>">Order this plan</a>
      <a class="btn btn-outline" href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> Order by phone</a>
      <p class="form-note">Want changes? Mention them in your order and Tiny Homes Blueprint will quote the modification.</p>
    </aside>
  </div>
</section>

<?php if ($p['floorplan']): ?>
<section class="section section-alt" id="floor-plan">
  <div class="wrap">
    <div class="section-head"><h2><?= e($p['name']) ?> floor plan</h2>
      <p class="lead"><?= e($p['width'] . ' x ' . $p['depth']) ?> footprint<?= $p['loft_sqft'] ? ', with the ' . $p['loft_sqft'] . ' sq ft loft shown dashed over the rooms below it' : '' ?>. Room sizes are nominal. The purchased plan set has full wall, window and door dimensions.</p></div>
    <figure class="plan-drawing"><img src="<?= e($p['floorplan']) ?>" alt="<?= e($p['name'] . ' floor plan: ' . implode(', ', array_map(fn($r) => strtolower($r[0]), $p['rooms']))) ?>" loading="lazy"></figure>
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
</section>
<?php endif; ?>

<section class="section<?= $p['floorplan'] ? '' : ' section-alt' ?>">
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

<section class="section<?= $p['floorplan'] ? ' section-alt' : '' ?>">
  <div class="wrap two-col top">
    <div class="prose">
      <h2>What will <?= e($p['name']) ?> cost to build?</h2>
      <p>Using typical 2026 costs of $150&ndash;$330 per sq ft for an owner-built home and $250&ndash;$500 per sq ft with a builder, a <?= number_format($p['sqft']) ?> sq ft house like <?= e($p['name']) ?> generally falls between <strong><?= money($p['sqft'] * 150) ?> and <?= money($p['sqft'] * 330) ?></strong> owner-built, or <strong><?= money($p['sqft'] * 250) ?> to <?= money($p['sqft'] * 500) ?></strong> with a general contractor, before <?= $p['mobile'] ? 'the trailer, ' : '' ?>land, utilities and site work. Your region, finishes and <?= $p['mobile'] ? 'trailer' : 'foundation' ?> move the number most.</p>
      <p><a class="btn btn-sm" href="/tools/tiny-house-cost-calculator/">Estimate it in the cost calculator</a></p>
    </div>
    <div class="prose">
      <h2>Where this plan works</h2>
      <?php if ($p['mobile']): ?>
      <p>This is a tiny house on wheels, drawn to the common road limits of 8.5 ft wide and 13.5 ft tall. Check your state's height limit and your trailer's GVWR before you build. The <a href="/tools/tiny-house-trailer-weight-calculator/">trailer weight calculator</a> estimates the finished weight, and the <a href="/blog/tiny-house-zoning-laws/">zoning guide</a> covers where a tiny house on wheels can be parked and lived in.</p>
      <?php else: ?>
      <p>This plan is designed for a permanent foundation (<?= e(lcfirst($p['foundation'])) ?>), so it is reviewed like any other small house. Where local rules allow units of this size, it can also serve as an <a href="/adu-plans/">ADU or backyard cottage</a>. Check <a href="/blog/tiny-house-zoning-laws/">tiny house zoning rules</a> and minimum dwelling sizes in your county before you build.</p>
      <?php endif; ?>
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
    ['What files come with ' . $p['name'] . '?', '<p>The plan set includes the drawings as PDF, CAD and image files: a dimensioned floor plan, exterior elevations and roof and wall framing specifications.</p>'],
    ['Can ' . $p['name'] . ' be modified?', '<p>Yes. Tiny Homes Blueprint can flip the layout, adjust room sizes, add or remove a loft, or change the ' . ($p['mobile'] ? 'trailer length' : 'foundation') . '. <a href="' . e($order) . '">Request a modification quote</a>.</p>'],
    $p['mobile']
        ? ['Can ' . $p['name'] . ' be built on a foundation instead?', '<p>Yes. Many owners build a trailer plan on piers or a slab, which can open up a wider range of permit options. Tell us your site and we will note what changes, such as the floor framing and tie-downs.</p>']
        : ['Can I build ' . $p['name'] . ' on a trailer?', '<p>No. At ' . e($p['depth']) . ' deep it is wider than the 8.5 ft road limit and is designed for a permanent foundation. For road-legal designs, see our <a href="/tiny-house-on-wheels-plans/">tiny house on wheels plans</a>.</p>'],
    ['How do I order?', '<p>Use the order button on this page or call ' . SITE_PHONE . '. We confirm your plan and file needs, send a secure payment link and deliver the files by email.</p>'],
]); ?>
</div></section>
<?php cta_band('Questions about ' . $p['name'] . '?', 'Call Tiny Homes Blueprint or send a message. We answer within one business day.', 'Ask about this plan', $order); ?>
<?php page_end(); ?>
