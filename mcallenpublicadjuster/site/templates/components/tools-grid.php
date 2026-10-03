<?php $tools = [
  ['/claim-calculator/', 'Claim Settlement Calculator', 'calc', 'Estimate RCV, ACV, recoverable depreciation, and out-of-pocket costs.'],
  ['/claim-documentation-checklist/', 'Documentation Checklist', 'clipboard', 'Interactive, printable checklist by damage type, with progress tracking.'],
  ['/storm-lookup/', 'Storm Event Lookup', 'search', 'Search NOAA storm reports near a Hidalgo County city or ZIP code.'],
  ['/weather/', 'Live McAllen Weather', 'thermo', 'Current conditions, 7-day forecast, and active NWS alerts.'],
  ['/storm-history/', 'Storm History', 'calendar', 'Filterable NOAA record of hail, wind, tornado, and flood events.'],
  ['/weather-events/', 'Recent Weather Events', 'storm', 'Automatically updated National Weather Service storm reports.'],
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
