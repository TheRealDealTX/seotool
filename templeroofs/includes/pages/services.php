<?php
defined('TR_ROOT') || exit;
$crumbs = [['Roofing Services', '/services/']];
$groups = [
    'Repairs & storm damage' => ['roof-repair-temple-tx', 'storm-damage-roof-repair-temple-tx', 'hail-damage-roof-repair-temple-tx', 'wind-damage-roof-repair-temple-tx', 'emergency-roof-leak-repair-temple-tx', 'roof-insurance-claim-assistance-temple-tx'],
    'New roofs & materials'  => ['roof-replacement-temple-tx', 'asphalt-shingle-roofing-temple-tx', 'metal-roofing-temple-tx', 'commercial-roofing-temple-tx'],
    'Inspections & drainage' => ['roof-inspection-temple-tx', 'gutters-roof-drainage-temple-tx'],
];
layout_start([
    'title'       => 'Roofing Services in Temple, TX',
    'description' => 'Roof repair, replacement, storm, hail and wind damage, metal, shingle and commercial roofing, inspections and gutters from Temple Roofers.',
    'path'        => '/services/',
    'crumbs'      => $crumbs,
    'image'       => 'roof-replacement-tear-off',
    'preload_image' => 'roof-replacement-tear-off',
]);
page_hero(['h1' => 'Roofing Services in Temple, TX', 'lead' => 'Repairs, replacements, storm restoration and inspections for homes and commercial buildings across Temple and nearby Bell County communities.', 'image' => 'roof-replacement-tear-off', 'alt' => 'Roof replacement in progress with new underlayment on the decking', 'crumbs' => $crumbs, 'eyebrow' => 'What we do']);
?>
<section class="section">
  <div class="container">
    <div class="intro-block reveal">
      <p>Temple Roofers handles the full range of roofing work Central Texas properties need, from a single cracked pipe boot to a complete tear-off and re-roof. Whatever brings you here, the first step is the same: a free, no-obligation inspection so the recommendation is based on what is actually happening on your roof, not a guess. Pick a service below to learn how we approach it, what warning signs to look for and how Bell County weather affects your options.</p>
    </div>
    <?php foreach ($groups as $label => $slugs): ?>
    <h2 class="group-title reveal"><?= e($label) ?></h2>
    <div class="card-grid card-grid--3">
      <?php foreach ($slugs as $slug): if ($s = service($slug)) echo service_card($s); endforeach; ?>
    </div>
    <?php endforeach; ?>
  </div>
</section>
<section class="section section--alt">
  <div class="container split">
    <div class="split__copy reveal">
      <h2 class="section-title">Not Sure Which Service You Need?</h2>
      <p>Most homeowners do not call because they know they need "flashing repair" — they call because there is a stain on the ceiling or the neighbors are getting new roofs after a storm. That is exactly what the free inspection is for. We identify the cause, show you photos and explain whether a repair, a claim conversation with your insurer or a replacement makes the most sense.</p>
      <p>Prefer to research first? Try the <a href="/tools/storm-damage-checklist/">storm damage self-check</a> or estimate a project with the <a href="/tools/roof-replacement-cost-calculator/">roof replacement cost calculator</a>.</p>
    </div>
    <div class="split__media reveal"><figure class="media-frame"><?= img('roofer-inspecting-roof', 'Roofer checking shingles during a roof inspection', ['sizes' => '(max-width: 900px) 100vw, 50vw']) ?></figure></div>
  </div>
</section>
<?php final_cta('Get a Free Roof Inspection in Temple', '', '/services/'); ?>
<?php layout_end();
