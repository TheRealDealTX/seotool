<?php
/** Storm damage checklist widget. Logic: main.js → tools.checklist. Weight = urgency. */
$groups = [
    'Around the yard' => [
        ['Shingles, shingle pieces or ridge caps on the ground', 3],
        ['Large pine limbs on or touching the roof', 3],
        ['Granules (sand-like grit) washed onto the driveway', 2],
        ['Dents or dings on cars, mailbox or patio furniture', 1],
    ],
    'Metals & gutters' => [
        ['Dents in gutters or downspouts', 2],
        ['Dented roof vents, turbines or chimney caps', 2],
        ['Bent or dented A/C condenser fins', 1],
        ['Loose or lifted metal trim, drip edge or panels', 3],
    ],
    'Inside the home' => [
        ['New water stains or drips on ceilings or walls', 3],
        ['Damp insulation or daylight visible in the attic', 3],
        ['Peeling or bubbling paint near the ceiling', 2],
        ['Musty smell in upper rooms or attic', 1],
    ],
];
?>
<div class="tool tool-check" data-tool="checklist">
  <div class="check-groups">
<?php foreach ($groups as $title => $items): ?>
    <fieldset class="check-group">
      <legend><?= e($title) ?></legend>
<?php foreach ($items as [$label, $w]): ?>
      <label class="check-item"><input type="checkbox" data-weight="<?= $w ?>"><span class="cb" aria-hidden="true"><?= icon('check') ?></span><?= e($label) ?></label>
<?php endforeach; ?>
    </fieldset>
<?php endforeach; ?>
  </div>
  <div class="tool-result" aria-live="polite">
    <span class="result-kicker">Inspection urgency</span>
    <div class="urgency"><span data-out="meter"></span></div>
    <h3 data-out="level">Nothing checked yet</h3>
    <p data-out="advice">Walk around the property and tick anything you notice. Stay off the roof — ground-level checks are enough.</p>
    <a class="btn btn-primary btn-block" href="/contact/">Schedule a Free Storm Inspection</a>
    <button type="button" class="btn btn-ghost btn-block" data-action="print">Print this checklist</button>
  </div>
</div>
