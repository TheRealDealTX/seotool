<?php
$weeks = [
    '6–8 weeks before' => ['Set your budget (try our affordability calculator)', 'Check your current lease for the notice period – often 30 or 60 days', 'Start searching neighborhoods and commute areas', 'Pull your credit report and fix any errors'],
    '4–6 weeks before' => ['Tour apartments and apply to your top choice', 'Give written notice to your current landlord', 'Book movers or reserve a truck', 'Start decluttering – sell or donate what you won’t move'],
    '2–3 weeks before' => ['Choose an electricity plan and schedule service for move-in day', 'Schedule internet installation', 'Buy renters insurance (most properties require it)', 'Collect boxes, tape and packing supplies', 'Forward your mail with USPS'],
    'Moving week' => ['Confirm move-in time and key pickup with the leasing office', 'Confirm movers and parking / elevator reservations', 'Pack an essentials box: chargers, toiletries, sheets, snacks', 'Clean your old place and take photos for your deposit'],
    'Move-in day' => ['Do a move-in inspection and photograph any damage', 'Test the A/C, water heater and appliances', 'Locate the breaker box and water shut-off', 'Return keys to your old landlord and leave a forwarding address'],
    'First 30 days' => ['Update your Texas driver license address', 'Update your vehicle registration and insurance', 'Register to vote at your new address', 'Enroll kids in school or confirm zoning', 'Claim your move-in reward if you leased through a locator'],
];
?>
<div class="checklist" data-checklist="moving">
  <div class="cl-head">
    <label class="field">Move date<input type="date" name="cl_date"></label>
    <div class="cl-progress"><span data-out="pct">0%</span><div class="gauge"><div class="gauge-fill" data-out="bar"></div></div><small data-out="countdown"></small></div>
  </div>
  <?php foreach ($weeks as $w => $items): ?>
    <fieldset class="cl-group"><legend><?= e($w) ?></legend>
      <?php foreach ($items as $i => $item): ?><label class="cl-item"><input type="checkbox" data-key="<?= e(slugify($w) . '-' . $i) ?>"><span><?= e($item) ?></span></label><?php endforeach ?>
    </fieldset>
  <?php endforeach ?>
  <div class="cl-actions"><button type="button" class="btn btn-outline" onclick="window.print()">🖨 Print</button><button type="button" class="btn btn-ghost" data-reset-list>Clear checklist</button></div>
</div>
