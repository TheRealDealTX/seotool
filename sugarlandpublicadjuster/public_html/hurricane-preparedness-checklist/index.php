<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/layout.php';
$path = '/hurricane-preparedness-checklist/';
$crumbs = [['Home', '/'], ['Storm Center', '/sugar-land-weather/'], ['Hurricane Preparedness Checklist', $path]];
$groups = [
    'Before hurricane season (by June 1)' => [
        'Read your declarations page: dwelling limit, hurricane/wind-hail deductible, AOP deductible',
        'Convert a percentage deductible to dollars with the <a href="/tools/hurricane-deductible-calculator/">deductible calculator</a>',
        'Confirm whether you carry flood insurance (NFIP policies usually have a 30-day waiting period)',
        'Check for replacement cost on the dwelling and contents, and any roof payment schedule',
        'Video every room, closet and the exterior; save it to the cloud',
        'Build a contents list with the <a href="/tools/home-inventory-checklist/">home inventory builder</a>',
        'Save policy, agent and insurer claim phone numbers in your phone and in print',
        'Trim trees and limbs that overhang the roof; clean gutters and drains',
        'Know your evacuation zone and route (Fort Bend County OEM)',
        'Sign up for Fort Bend County and City of Sugar Land emergency alerts',
    ],
    'When a storm is forecast (72–24 hours out)' => [
        'Watch the <a href="/sugar-land-weather/">live NWS alerts and tropical outlook</a>',
        'Fill prescriptions; stock water (1 gallon per person per day) and non-perishable food for 7 days',
        'Charge phones, power banks and radios; fuel vehicles and generators',
        'Bring in or tie down patio furniture, grills, trash cans and decorations',
        'Photograph the roof, fences and exterior again with today’s date',
        'Move valuables and documents up high in waterproof bags',
        'Get cash—ATMs and cards may not work during outages',
        'Set the refrigerator and freezer to their coldest settings',
    ],
    'After the storm' => [
        'Stay clear of downed lines and flooded roads; report outages to your utility',
        'Photograph and video all damage before any cleanup',
        'Make temporary repairs (tarp, board-up, water extraction) and keep every receipt',
        'Save spoiled-food lists and receipts for hotels, meals and other extra living costs',
        'Report the claim promptly and write down the claim number',
        'Don’t throw away damaged materials until they are documented',
        'Be cautious of door-to-door contractors asking you to sign an assignment or contract on the spot',
        'Call a Sugar Land public adjuster for a free review before the insurer’s inspection',
    ],
];
$howto = ['@type' => 'HowTo', '@id' => SITE['origin'] . $path . '#howto', 'name' => 'Hurricane preparedness checklist for Sugar Land homeowners', 'step' => []];
foreach ($groups as $g => $items) {
    $howto['step'][] = ['@type' => 'HowToSection', 'name' => $g, 'itemListElement' => array_map(fn($t) => ['@type' => 'HowToStep', 'text' => strip_tags($t)], $items)];
}
page_start([
    'title' => 'Hurricane Preparedness Checklist for Sugar Land, TX | Sugar Land Public Adjuster',
    'description' => 'Interactive, printable hurricane preparedness checklist for Sugar Land and Fort Bend County homeowners—insurance, home prep and what to do after the storm.',
    'path' => $path,
    'breadcrumbs' => $crumbs,
    'schema' => [$howto],
]);
page_hero('Hurricane Preparedness Checklist for Sugar Land Homeowners', 'Atlantic hurricane season runs June 1 to November 30. Check items off as you go—your progress is saved on this device—and print a copy for the fridge.', $crumbs, 'Storm Center');
?>
<div class="container content-layout">
  <div>
<?php $gi = 0; foreach ($groups as $g => $items): $gi++; ?>
    <div class="tool mb-2" data-checklist="hurricane-<?= $gi ?>">
      <h2><?= e($g) ?></h2>
      <p class="progress-label" data-progress></p>
      <div class="bar"><i data-progress-bar style="width:0"></i></div>
      <ul class="check-list-tool">
<?php foreach ($items as $t): ?>
        <li><label><input type="checkbox"><span><?= $t ?></span></label></li>
<?php endforeach; ?>
      </ul>
      <div class="tool-actions"><button type="button" class="btn btn-outline" data-reset>Reset</button><button type="button" class="btn btn-outline" onclick="window.print()">Print checklist</button></div>
    </div>
<?php endforeach; ?>
    <div class="prose">
      <h2>Insurance tips specific to Sugar Land</h2>
      <p>Fort Bend County sits outside the Texas Windstorm Insurance Association’s coastal territory, so wind damage is normally covered by your regular homeowners policy—subject to its wind/hail or named-storm deductible. Rising water is a different story: it is excluded from homeowners policies and covered only by flood insurance. After storms like Harvey, the line between wind-driven rain and flood became the biggest fight in many claims. Read our <a href="/hurricane-insurance-claim-guide-sugar-land/">hurricane claim guide</a> and see <a href="/sugar-land-storm-history/">Sugar Land’s storm history</a>.</p>
    </div>
  </div>
  <?php sidebar_cta(); ?>
</div>
<?php page_end(['scripts' => '<script src="/assets/js/tools.js?v=' . ASSET_VER . '" defer></script>']); ?>
