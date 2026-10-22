<?php defined('CCPA_ROOT') || exit; $tools = [
  ['/weather/', 'Live Weather, Radar & Tides', 'thermo', 'Current conditions, hourly and 7-day forecast, animated radar, Corpus Christi Bay tides, and the tropical outlook.'],
  ['/hurricane-deductible-calculator/', 'Hurricane Deductible Calculator', 'hurricane', 'See what a 1%, 2%, or 5% named-storm deductible means in dollars before the storm.'],
  ['/claim-calculator/', 'Claim Settlement Calculator', 'calc', 'Estimate RCV, ACV, recoverable depreciation, and out-of-pocket costs.'],
  ['/claim-deadline-calculator/', 'Claim Deadline Calculator', 'calendar', 'Map Texas prompt-payment and TWIA claim timelines from your own dates.'],
  ['/claim-documentation-checklist/', 'Documentation Checklist', 'clipboard', 'Interactive, printable checklist by damage type, with progress tracking.'],
  ['/storm-lookup/', 'Storm Event Lookup', 'search', 'Search NOAA storm reports near a Coastal Bend city or ZIP code.'],
  ['/storm-history/', 'Storm History', 'storm', 'Filterable NOAA record of hurricanes, hail, wind, tornado, and flood events.'],
  ['/weather-events/', 'Recent Weather Events', 'alert', 'Automatically updated National Weather Service storm reports.'],
  ['/hurricane-season-guide/', 'Hurricane Season Guide', 'shield', 'Before-, during-, and after-the-storm steps that protect your property and your claim.'],
]; ?>
<div class="card-grid card-grid-tools">
  <?php foreach ($tools as $i => [$href, $label, $ic, $blurb]): ?>
  <a class="tool-card reveal" style="--d:<?= ($i % 3) * 80 ?>ms" href="<?= e($href) ?>">
    <span class="tool-card-icon"><?= icon($ic, 'icon') ?></span>
    <span class="tool-card-title"><?= e($label) ?></span>
    <span class="tool-card-text"><?= e($blurb) ?></span>
    <span class="service-card-more">Open tool <?= icon('arrow', 'icon icon-sm') ?></span>
  </a>
  <?php endforeach; ?>
</div>
