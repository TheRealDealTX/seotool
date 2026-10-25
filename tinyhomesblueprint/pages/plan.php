<?php
$slug = $ROUTE['plan'];
$p = $PLANS[$slug];
$others = array_values(array_diff(array_keys($PLANS), [$slug]));

// Plan-specific copy. Facts come from $PLANS; the descriptions are written per plan.
$intro = [
    'plan-12-2418' => 'Plan 12-2418 is a rustic 700 sq ft tiny house plan with three bedrooms, two baths and a covered front porch, drawn on a compact 20 x 38 ft footprint. It works as an affordable primary residence, a family vacation cabin or a roomy backyard ADU where zoning allows.',
    'plan-12-2417' => 'Plan 12-2417 is a single-level 700 sq ft tiny cabin plan with two bedrooms and one full bath on a 20 x 38 ft footprint. With everything on one floor and no stairs, it suits full-time living, downsizing and aging in place as well as weekend getaways.',
][$slug];
$layout = [
    'plan-12-2418' => [
        'The side main entrance opens into an open living area with direct access to the covered front porch, so the porch works as an extra outdoor room in good weather.',
        'The kitchen is large enough for either a dining table or an island, which is rare in a home this size.',
        'Off the living room, a flexible room with a retractable wall can be a formal dining room, a home office or a guest bedroom, and it opens up to the living area when you entertain.',
        'Bedrooms sit at the far end of the house for privacy, and the second floor adds sleeping space without enlarging the footprint.',
        'Laundry is on the main floor, and the plan can be flipped on the lot to put the porch at the rear for a view or for privacy from the road.',
    ],
    'plan-12-2417' => [
        'A side entry leads into one open great room that combines living, kitchen and dining, with access to the covered front porch.',
        'The flexible kitchen fits a table or an island, so you can choose more prep space or a dedicated dining spot.',
        'A flex room with a retractable wall can be closed off as a guest room or office, or opened up to extend the living area.',
        'Both bedrooms are grouped at the far end of the house for quiet and privacy, sharing a bath with a full shower.',
        'Main-floor laundry and a single level make it easy to live in long-term, and the plan can be flipped to put the porch at the rear.',
    ],
][$slug];

$specs = [
    'Plan number' => $p['name'], 'Heated area' => number_format($p['sqft']) . ' sq ft',
    'Bedrooms' => $p['beds'], 'Bathrooms' => $p['baths'], 'Floors' => $p['floors'],
    'Width' => $p['width'], 'Depth' => $p['depth'], 'Overall height' => $p['height'], 'Ceiling height' => $p['ceiling'],
    'Roof' => $p['roof'], 'Exterior walls' => $p['walls'],
    'Files included' => 'PDF, CAD and image files',
];
$schema = [
    '@context' => 'https://schema.org', '@type' => 'Product', 'name' => $p['name'] . ' - ' . $p['title'],
    'description' => $intro, 'sku' => $p['name'], 'image' => abs_url($p['image']),
    'brand' => ['@type' => 'Brand', 'name' => SITE_NAME],
    'offers' => ['@type' => 'Offer', 'price' => $p['price'], 'priceCurrency' => 'USD', 'availability' => 'https://schema.org/InStock',
        'url' => abs_url($PATH), 'seller' => ['@id' => SITE_URL . '/#org']],
    'additionalProperty' => [
        ['@type' => 'PropertyValue', 'name' => 'Square feet', 'value' => $p['sqft']],
        ['@type' => 'PropertyValue', 'name' => 'Bedrooms', 'value' => $p['beds']],
        ['@type' => 'PropertyValue', 'name' => 'Bathrooms', 'value' => $p['baths']],
    ],
];
page_start([
    'breadcrumbs' => [['Home', '/'], ['Tiny House Plans', '/tiny-house-plans/'], [$p['name'], null]],
    'schema' => [$schema],
    'og_image' => abs_url($p['image']),
]);
?>
<section class="section" style="padding-top:28px">
  <div class="wrap plan-hero">
    <div>
      <p class="eyebrow"><?= e($p['name']) ?></p>
      <h1><?= e($p['title']) ?></h1>
      <p class="lead"><?= e($intro) ?></p>
      <img src="<?= e($p['image']) ?>" width="800" height="430" alt="<?= e($p['name'] . ' rendering: ' . $p['title']) ?>">
      <ul class="plan-specs" style="font-size:1rem;margin-top:18px">
        <li><?= icon('ruler') ?> <?= number_format($p['sqft']) ?> sq ft</li>
        <li><?= icon('bed') ?> <?= $p['beds'] ?> bedrooms</li>
        <li><?= icon('bath') ?> <?= $p['baths'] ?> bath<?= $p['baths'] > 1 ? 's' : '' ?></li>
        <li><?= icon('stairs') ?> <?= $p['floors'] ?> floor<?= $p['floors'] > 1 ? 's' : '' ?></li>
        <li><?= icon('layout') ?> <?= e($p['width'] . ' x ' . $p['depth']) ?></li>
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
      <a class="btn btn-wood" href="/contact/?plan=<?= e(urlencode($p['name'])) ?>#form">Order this plan</a>
      <a class="btn btn-outline" href="tel:<?= SITE_TEL ?>"><?= icon('phone') ?> Order by phone</a>
      <p class="form-note">Want changes? Mention them in your order and Tiny Homes Blueprint will quote the modification.</p>
    </aside>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap two-col top">
    <div class="prose">
      <h2>Floor plan highlights</h2>
      <ul class="check-list"><?php foreach ($layout as $l): ?><li><?= e($l) ?></li><?php endforeach; ?></ul>
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

<section class="section">
  <div class="wrap two-col top">
    <div class="prose">
      <h2>What will <?= e($p['name']) ?> cost to build?</h2>
      <p>Using typical 2026 costs of $150&ndash;$330 per sq ft for an owner-built home and $250&ndash;$500 per sq ft with a builder, a <?= number_format($p['sqft']) ?> sq ft house like <?= e($p['name']) ?> generally falls between <strong><?= money($p['sqft'] * 150) ?> and <?= money($p['sqft'] * 330) ?></strong> owner-built, or <strong><?= money($p['sqft'] * 250) ?> to <?= money($p['sqft'] * 500) ?></strong> with a general contractor, before land, utilities and site work. Your region, finishes and foundation move the number most.</p>
      <p><a class="btn btn-sm" href="/tools/tiny-house-cost-calculator/">Estimate it in the cost calculator</a></p>
    </div>
    <div class="prose">
      <h2>Where this plan works</h2>
      <p>At 20 ft wide this is a foundation home, not a tiny house on wheels. It fits most rural and suburban lots and, where local rules allow units of this size, it can serve as an <a href="/adu-plans/">ADU or backyard cottage</a>. Check <a href="/blog/tiny-house-zoning-laws/">tiny house zoning rules</a> and minimum dwelling sizes in your county before you build.</p>
      <p>Explore similar designs: <?php foreach ($p['styles'] as $i => $s) { echo ($i ? ', ' : '') . '<a href="/' . e($s) . '/">' . e($ROUTES["/$s/"]['nav']) . '</a>'; } ?>.</p>
    </div>
  </div>
</section>

<?php if ($others): ?>
<section class="section section-alt"><div class="wrap">
  <h2>Similar tiny house plans</h2>
  <?php plan_grid($others); ?>
</div></section>
<?php endif; ?>

<section class="section"><div class="narrow">
<?php faq_block([
    ['What files come with ' . $p['name'] . '?', '<p>The plan set includes the drawings as PDF, CAD and image files: a dimensioned floor plan, exterior elevations and roof and wall framing specifications.</p>'],
    ['Can ' . $p['name'] . ' be modified?', '<p>Yes. Tiny Homes Blueprint can flip the layout, move the porch, adjust room sizes or change the foundation. <a href="/contact/?plan=' . e(urlencode($p['name'])) . '#form">Request a modification quote</a>.</p>'],
    ['Can I build ' . $p['name'] . ' on a trailer?', '<p>No. At ' . e($p['width']) . ' wide it is designed for a permanent foundation. For road-legal designs see our <a href="/tiny-house-on-wheels-plans/">tiny house on wheels plans</a> guide.</p>'],
    ['How do I order?', '<p>Use the order button on this page or call ' . SITE_PHONE . '. We confirm your plan and file needs, send a secure payment link and deliver the files by email.</p>'],
]); ?>
</div></section>
<?php cta_band('Questions about ' . $p['name'] . '?', 'Call Tiny Homes Blueprint or send a message. We answer within one business day.', 'Ask about this plan', '/contact/?plan=' . urlencode($p['name']) . '#form'); ?>
<?php page_end(); ?>
