<?php
$groups = [
    'Inside the apartment' => ['Run the shower – check water pressure and how fast hot water arrives', 'Test the A/C and heat; ask how old the unit is', 'Open and close windows; check locks and screens', 'Look under sinks and around the water heater for leaks or stains', 'Check for signs of pests (droppings, traps, bait)', 'Test outlets, lights and the garbage disposal', 'Check cell signal and ask which internet providers serve the building', 'Measure where your bed, couch and desk will go', 'Note natural light and what the windows face', 'Listen for noise from neighbors, the street or the pool'],
    'Building & grounds' => ['Walk to your parking spot – covered, garage or open?', 'Check where packages are delivered and how they’re secured', 'Look at the trash / valet trash setup', 'Visit the gym, pool and other amenities you’ll actually use', 'Check gates, lighting and entry access after dark if you can', 'Ask whether the property flooded in recent storms'],
    'Ask the leasing office' => ['What are all monthly fees on top of rent (trash, pest, amenity, parking)?', 'What do utilities usually cost for this floor plan?', 'Which move-in specials are available right now?', 'What are the pet rules, deposits and monthly pet rent?', 'How are maintenance requests handled – and how fast?', 'What does it cost to break the lease or transfer units?', 'Is renters insurance required, and how much coverage?', 'When can I move in, and is this exact unit available?'],
];
?>
<div class="checklist" data-checklist="tour">
  <div class="cl-head">
    <label class="field">Property you’re touring<input name="cl_name" placeholder="e.g. Camden Heights – unit 2104"></label>
    <div class="cl-progress"><span data-out="pct">0%</span><div class="gauge"><div class="gauge-fill" data-out="bar"></div></div></div>
  </div>
  <?php foreach ($groups as $g => $items): ?>
    <fieldset class="cl-group"><legend><?= e($g) ?></legend>
      <?php foreach ($items as $i => $item): ?><label class="cl-item"><input type="checkbox" data-key="<?= e(slugify($g) . '-' . $i) ?>"><span><?= e($item) ?></span></label><?php endforeach ?>
    </fieldset>
  <?php endforeach ?>
  <label class="field">Notes<textarea name="cl_notes" rows="4" placeholder="Likes, dislikes, rent quoted, specials offered…"></textarea></label>
  <div class="cl-actions"><button type="button" class="btn btn-outline" onclick="window.print()">🖨 Print</button><button type="button" class="btn btn-ghost" data-reset-list>Start a new property</button></div>
</div>
