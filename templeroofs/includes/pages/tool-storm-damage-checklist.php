<?php
defined('TR_ROOT') || exit;
$crumbs = [['Roofing Tools', '/tools/'], [$tool['name'], '/tools/' . $toolSlug . '/']];
$items = [
    'missing_shingles' => ['Missing shingles or pieces of shingle', 'Visible gaps, exposed felt or bare spots on the roof seen from the ground.'],
    'dented_gutters'   => ['Dented gutters, downspouts or vents', 'Fresh dents or dings in soft metal are a common sign that hail fell on the roof too.'],
    'granules'         => ['Granules near downspouts', 'Piles of sand-like shingle granules at downspout outlets or in gutters.'],
    'bent_flashing'    => ['Bent or loose flashing', 'Metal along walls, chimneys, valleys or roof edges that looks lifted, bent or out of place.'],
    'ceiling_stains'   => ['Interior ceiling or wall stains', 'New water marks, discoloration or bubbling paint inside the home.'],
    'broken_vents'     => ['Broken or damaged roof vents', 'Cracked plastic vents, dented metal vents or missing vent caps.'],
    'active_leak'      => ['Leaks after the storm', 'Water dripping inside, wet insulation or a damp attic after the storm.'],
    'debris'           => ['Loose roofing debris in the yard', 'Shingle fragments, ridge cap pieces or nails on the ground.'],
    'branches'         => ['Fallen branches on or near the roof', 'Limbs that struck the roof or are still resting on it.'],
    'other_exterior'   => ['Other visible exterior damage', 'Dented AC fins, mailbox or car, cracked siding, torn window screens or damaged fences.'],
];
$faqs = [
    ['q' => 'Does this self-check tell me if my roof is damaged?', 'a' => 'No. It organizes what you can safely see from the ground and suggests next steps. Many types of storm damage, such as hail bruising or broken shingle seals, cannot be confirmed without a close professional inspection.'],
    ['q' => 'Will my insurance cover the damage?', 'a' => 'Only your insurance company can determine coverage based on your policy and its adjuster\'s inspection. This tool does not predict claim outcomes. Temple Roofers can document damage and provide a repair estimate, but we are not public adjusters.'],
    ['q' => 'Should I go on the roof to check?', 'a' => 'No. Storm-damaged roofs can be slippery and unstable. Look from the ground, use binoculars or zoom photos, and check the attic only if it is safe to reach.'],
];
layout_start([
    'title' => 'Storm & Hail Damage Self-Check for Your Roof', 'description' => 'Free storm and hail damage checklist for Temple homeowners. Note what you see from the ground and get safe, practical next steps.',
    'path' => '/tools/' . $toolSlug . '/', 'crumbs' => $crumbs, 'schema' => [schema_faq($faqs)], 'scripts' => ['js/tools.js'], 'body_class' => 'page-tool',
]);
page_hero(['h1' => 'Storm & Hail Damage Self-Check', 'lead' => 'After wind or hail, note what you can safely see from the ground. We will suggest practical next steps — no ladder required.', 'crumbs' => $crumbs, 'actions' => false, 'compact' => true, 'eyebrow' => 'Free roofing tool']);
?>
<section class="section section--tight">
  <div class="container">
    <div class="callout callout--warn safety-banner"><?= icon('alert') ?> <span><strong>Safety first: never climb onto your roof.</strong> Stay away from downed power lines, do not touch sagging wires, and keep clear of hanging limbs. Check from the ground, through windows and — only if safely accessible — from inside the attic.</span></div>
  </div>
  <div class="container tool-layout" data-tool="storm">
    <form class="tool-panel" novalidate data-storm-form>
      <h2 class="tool-panel__title"><?= icon('checklist') ?> What do you notice?</h2>
      <p class="tool-panel__hint">Select everything you can see. Leave items unchecked if you are not sure.</p>
      <div class="check-cards">
        <?php foreach ($items as $k => [$label, $help]): ?>
        <label class="check-card">
          <input type="checkbox" name="signs" value="<?= e($k) ?>">
          <span class="check-card__box" aria-hidden="true"><?= icon('check') ?></span>
          <span class="check-card__text"><strong><?= e($label) ?></strong><small><?= e($help) ?></small></span>
        </label>
        <?php endforeach; ?>
      </div>
      <div class="form-grid">
        <div class="field">
          <label for="s-storm">What kind of storm?</label>
          <select id="s-storm" name="storm"><option value="">Not sure</option><option value="hail">Hail</option><option value="wind">High wind</option><option value="both">Hail and wind</option><option value="rain">Heavy rain</option></select>
        </div>
        <div class="field">
          <label for="s-when">When did it happen?</label>
          <select id="s-when" name="when"><option value="">Not sure</option><option value="week">Within the last week</option><option value="month">Within the last month</option><option value="older">More than a month ago</option></select>
        </div>
      </div>
      <button type="button" class="btn btn--ghost btn--sm" data-reset>Clear my answers</button>
    </form>
    <div class="tool-results" aria-live="polite" data-storm-results>
      <div class="meter" data-level="none">
        <p class="meter__label">Suggested level of follow-up</p>
        <div class="meter__track" aria-hidden="true"><span class="meter__fill" data-meter-fill></span></div>
        <p class="meter__value" data-out="level">Select what you notice</p>
        <p class="meter__text" data-out="summary">Your next steps will appear here as you check items.</p>
      </div>
      <div class="next-steps">
        <h3>Your next steps</h3>
        <ol data-out="steps"><li>Walk around the house and look at the roof, gutters and yard from the ground.</li></ol>
      </div>
      <a class="btn btn--gold btn--block" href="/free-roof-inspection/?concern=storm"><?= icon('clipboard-check') ?> Request a Free Professional Inspection</a>
      <button type="button" class="btn btn--ghost btn--block" data-print><?= icon('printer') ?> Print or save my checklist</button>
      <p class="tool-disclaimer"><?= icon('info') ?> This self-check is a guide, not a diagnosis. It cannot detect hidden damage, does not estimate a scientific probability of damage and does not predict insurance coverage.</p>
    </div>
  </div>
</section>
<section class="section section--alt">
  <div class="container container--narrow prose">
    <h2>What to Do After a Storm in Temple</h2>
    <p>Spring and fall storms in Bell County can bring hail, straight-line winds and heavy rain in the same afternoon. The hours and days afterward matter, both for limiting water damage and for keeping a clear record if you need to talk to your insurer.</p>
    <h3>Document before anything is cleaned up</h3>
    <ul>
      <li>Photograph the roof from several angles on the ground, plus gutters, downspouts, AC units, fences, cars and anything else with dents.</li>
      <li>Photograph hailstones next to a coin or ruler if they are still on the ground, and note the date and time of the storm.</li>
      <li>Photograph interior stains and wet areas, and keep receipts for emergency supplies.</li>
    </ul>
    <h3>Limit further damage safely</h3>
    <ul>
      <li>Catch drips, move belongings and turn off electricity to rooms where water is near light fixtures if it is safe to do so.</li>
      <li>Leave tarping and rooftop work to professionals. Temporary protection on a wet, damaged roof is dangerous work.</li>
    </ul>
    <h3>Watch out for storm chasers</h3>
    <p>After major storms, out-of-town crews often knock on doors. Be cautious of anyone who pressures you to sign immediately, asks for large upfront payments or offers to "cover" your deductible — that is illegal in Texas. Read more in our guide to <a href="/blog/roof-insurance-claims-texas-hailstorm/">roof insurance claims after a Texas hailstorm</a> and our <a href="/services/storm-damage-roof-repair-temple-tx/">storm damage roof repair</a> page.</p>
    <p>Keep an eye on the <a href="/weather/">live Temple weather forecast</a> for follow-up storms, and see <a href="/services/hail-damage-roof-repair-temple-tx/">hail damage</a> and <a href="/services/wind-damage-roof-repair-temple-tx/">wind damage</a> repair for what professional repairs involve.</p>
    <?= faq_html($faqs, 'Storm Damage Self-Check FAQs') ?>
  </div>
</section>
<?php final_cta('Storm Just Passed? Schedule a Free Roof Inspection.', '', '/tools/' . $toolSlug . '/'); ?>
<?php layout_end();
