<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
$path = '/tools/';
$crumbs = [['Home', '/'], ['Tools', $path]];
$tools = [
    ['/tools/insurance-claim-settlement-calculator/', '🧮', 'Insurance Claim Settlement Calculator', 'Compare the insurer’s payment with your real repair cost after deductible and depreciation, and see the shortfall in dollars.'],
    ['/tools/depreciation-calculator/', '📉', 'Depreciation (ACV) Calculator', 'Estimate depreciation, actual cash value and recoverable depreciation for roofs, flooring, appliances and contents.'],
    ['/tools/public-adjuster-fee-calculator/', '💲', 'Public Adjuster Fee Calculator', 'See your net recovery with and without a public adjuster under the Texas 10% fee cap, plus the break-even point.'],
    ['/tools/hurricane-deductible-calculator/', '🌀', 'Hurricane Deductible Calculator', 'Turn a 1%, 2% or 5% hurricane or wind/hail deductible into dollars and see what the insurer would pay.'],
    ['/tools/claim-deadline-calculator/', '📅', 'Texas Claim Deadline Calculator', 'Map the insurer’s Texas Prompt Payment Act deadlines from the day you reported the claim.'],
    ['/tools/home-inventory-checklist/', '📋', 'Home Inventory Builder', 'Build a room-by-room contents inventory and export it as a spreadsheet for your claim.'],
    ['/hurricane-preparedness-checklist/', '✅', 'Hurricane Preparedness Checklist', 'An interactive, printable checklist for before, during and after a Gulf storm—saved on your device.'],
    ['/sugar-land-weather/', '⛈️', 'Live Sugar Land Weather & Storm Tracker', 'Current conditions, NWS alerts, 7-day forecast, radar, tropical outlook and the Brazos River gauge.'],
    ['/sugar-land-storm-history/', '📜', 'Sugar Land Storm History', 'Major hurricanes, floods and freezes that hit Sugar Land and Fort Bend County—and the claim lessons from each.'],
];
$list = [];
foreach ($tools as $i => [$href, , $name]) {
    $list[] = ['@type' => 'ListItem', 'position' => $i + 1, 'name' => $name, 'url' => SITE['origin'] . $href];
}
page_start([
    'title' => 'Free Insurance Claim Tools & Calculators | Sugar Land Public Adjuster',
    'description' => 'Free claim calculators from a Sugar Land public adjuster: settlement gap, depreciation, PA fees, hurricane deductible, Texas deadlines and home inventory.',
    'path' => $path,
    'page_type' => 'CollectionPage',
    'breadcrumbs' => $crumbs,
    'schema' => [['@type' => 'ItemList', '@id' => SITE['origin'] . $path . '#tools', 'itemListElement' => $list]],
]);
page_hero('Free Insurance Claim Tools &amp; Calculators', 'Understand your claim before you talk to anyone. Every tool is free, works on your phone, and keeps your numbers private in your browser.', $crumbs, 'Built by a Sugar Land public adjuster');
?>
<section class="section">
  <div class="container">
    <div class="grid-3">
<?php foreach ($tools as [$href, $icon, $name, $blurb]): ?>
      <div class="card linked"><div class="icon" aria-hidden="true"><?= $icon ?></div><h2 class="h3"><a href="<?= e($href) ?>"><?= e($name) ?></a></h2><p><?= e($blurb) ?></p><span class="card-more">Open tool &rarr;</span></div>
<?php endforeach; ?>
    </div>
    <div class="callout mt-2"><p><strong>Numbers don’t add up?</strong> The tools give planning estimates. For a free review of your actual estimate, denial letter or settlement offer, call or text <?= tel_link() ?>—a Sugar Land public adjuster will walk you through it.</p></div>
  </div>
</section>
<?php page_end(); ?>
