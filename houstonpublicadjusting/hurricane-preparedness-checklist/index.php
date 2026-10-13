<?php
require dirname(__DIR__) . '/inc/layout.php';
$crumbs = [['Home', '/'], ['Hurricane Preparedness Checklist', '/hurricane-preparedness-checklist/']];
$sections = [
    'Before the season (May)' => [
        'Read your declarations page: dwelling limit, hurricane deductible, contents and ALE limits',
        'Buy or renew flood insurance now — NFIP policies usually have a 30-day waiting period',
        'Confirm whether you have replacement-cost or actual-cash-value coverage on the roof',
        'Walk through every room and record a video inventory of your home and belongings',
        'Save digital copies of your policy, IDs, deed and receipts to cloud storage',
        'Photograph the roof, exterior, fences and outbuildings in their current condition',
        'Trim trees and remove dead limbs near the house and power lines',
        'Know your evacuation zone (check your county or ReadyHarris) and plan your route',
    ],
    'When a storm is forecast (72 hours out)' => [
        'Watch the National Hurricane Center and our live Houston weather tracker',
        'Secure or bring in patio furniture, grills, trampolines and yard décor',
        'Clear gutters and storm drains near your property',
        'Fill prescriptions and gather water (1 gallon per person per day), food, batteries and cash',
        'Fuel vehicles and generators; never run a generator indoors or in a garage',
        'Move valuables and important papers to an upper floor or waterproof container',
        'Charge phones and power banks; save your insurer’s claim number and our number: (832) 503-5866',
    ],
    'After the storm' => [
        'Stay safe: avoid downed lines and floodwater, and wait for officials to give the all-clear',
        'Photograph and video all damage before moving or throwing anything away',
        'Make temporary repairs to prevent more damage (tarp the roof, board windows, start drying)',
        'Keep receipts for tarps, fans, hotels, meals and mileage',
        'Report the claim promptly and write down your claim number and every conversation',
        'Keep samples of damaged materials until the insurance adjuster has inspected',
        'Get a free claim review from Houston Public Adjusters before accepting any estimate',
    ],
];
page_start([
    'title' => 'Houston Hurricane Preparedness Checklist (Insurance-Focused)',
    'desc' => 'Interactive Houston hurricane preparedness checklist from licensed public adjusters: insurance review, flood coverage, home inventory, storm prep and after-storm claim steps.',
    'path' => '/hurricane-preparedness-checklist/',
    'crumbs' => $crumbs,
    'scripts' => ['/assets/js/tools.js'],
    'schema' => [['@type' => 'HowTo', 'name' => 'Prepare a Houston home and insurance claim for hurricane season',
        'step' => array_map(fn($t) => ['@type' => 'HowToStep', 'text' => $t], array_merge(...array_values($sections)))]],
]);
echo page_hero('Houston Hurricane Preparedness Checklist', 'Most checklists stop at water and batteries. This one is built by public adjusters, so it also protects the insurance claim you may have to make. Tick items off &mdash; your progress saves in this browser.', $crumbs, 'Atlantic hurricane season: June 1 &ndash; November 30');
?>
<div class="wrap layout-sidebar">
  <div id="prep">
    <p id="prep-count" style="font-weight:700;margin:0">0 done</p>
    <div class="progress" aria-hidden="true"><i id="prep-bar"></i></div>
<?php $n = 0; foreach ($sections as $title => $items): ?>
    <h2 style="font-size:1.4rem;margin-top:28px"><?= e($title) ?></h2>
    <ul class="prep-list">
<?php foreach ($items as $item): $n++; ?>
      <li><label><input type="checkbox" id="prep-<?= $n ?>"><span><?= e($item) ?></span></label></li>
<?php endforeach; ?>
    </ul>
<?php endforeach; ?>
    <p class="no-print" style="margin-top:20px"><button class="btn btn-outline" type="button" id="prep-reset">Reset checklist</button> <button class="btn btn-outline" type="button" onclick="window.print()">Print</button></p>
    <div class="prose"><?= author_box() ?></div>
  </div>
  <aside class="sidebar">
    <div class="side-card"><h3>Helpful tools</h3><ul class="link-list">
      <li><a href="/houston-weather/">Live Houston weather &amp; alerts</a></li>
      <li><a href="/tools/hurricane-deductible-calculator/">Hurricane deductible calculator</a></li>
      <li><a href="/tools/contents-inventory/">Contents inventory builder</a></li>
      <li><a href="/tools/additional-living-expense-calculator/">ALE calculator</a></li>
      <li><a href="/houston-storm-history/">Houston storm history</a></li>
    </ul></div>
    <div class="side-card sticky"><?= lead_form('lead-prep', 'Storm damage?', 'Free claim review from Houston Public Adjusters.', true) ?></div>
  </aside>
</div>
<?php
page_end();
