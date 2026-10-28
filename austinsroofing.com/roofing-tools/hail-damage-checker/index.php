<?php
require dirname(__DIR__, 2) . '/includes/layout.php';

$body = <<<'HTML'
<h2>How Hail Size Relates to Roof Damage</h2>
<p class="lead">Hail damage depends on stone size, density, wind speed and the roof material’s age and condition. Lab impact ratings give a useful rule of thumb: standard shingles start to bruise around 1 inch hail, while Class 4 impact-resistant shingles are tested against 2-inch steel balls.</p>
<div class="table-wrap"><table>
  <thead><tr><th>Hail size</th><th>Compared to</th><th>Typical roof impact</th></tr></thead>
  <tbody>
    <tr><td>¼″ – ½″</td><td>Pea – marble</td><td>Rarely damages roofs; may strip a few granules</td></tr>
    <tr><td>¾″ – 1″</td><td>Penny – quarter</td><td>Can bruise older or 3-tab shingles; dents soft metal vents</td></tr>
    <tr><td>1½″ – 1¾″</td><td>Ping-pong – golf ball</td><td>Commonly damages shingles, tile and gutters</td></tr>
    <tr><td>2½″ – 2¾″</td><td>Tennis ball – baseball</td><td>Cracks shingles and tile, dents metal, can puncture</td></tr>
    <tr><td>4″+</td><td>Softball</td><td>Severe — punctures, broken decking, skylights</td></tr>
  </tbody>
</table></div>
<h2>What to Do After a Hailstorm in Austin</h2>
<ol class="steps">
  <li><h3>Stay safe</h3><p>Don’t climb on the roof. Check ceilings and the attic for leaks.</p></li>
  <li><h3>Document</h3><p>Photograph hailstones next to a coin or ruler, plus dents on gutters, vents, AC units and cars.</p></li>
  <li><h3>Get inspected</h3><p>Hail bruises are often invisible from the ground. Book a free <a href="/services/hail-damage-repair/">hail damage inspection</a>.</p></li>
  <li><h3>Call your insurer</h3><p>Most policies have time limits for reporting damage. Learn how <a href="/services/roof-insurance-claims/">roof insurance claims</a> work.</p></li>
</ol>
<div class="callout callout--warn"><p><strong>Watch out for storm chasers.</strong> After big Central Texas hail events, out-of-town crews knock on doors. Work with a local company, never sign over your insurance check, and know that in Texas a contractor may not waive or rebate your deductible.</p></div>
<p>Read our complete guide to <a href="/blog/insurance-coverage-for-storm-damaged-roofs/">insurance coverage for storm-damaged roofs</a>, and consider <a href="/services/shingle-roofing/">Class 4 impact-resistant shingles</a> or <a href="/services/metal-roofing/">metal roofing</a> when it’s time to replace.</p>
HTML;

render_tool([
    'slug' => 'hail-damage-checker',
    'title' => 'Hail Size & Roof Damage Checker | Austin Roofing',
    'description' => 'Free hail damage checker: pick the hail size you saw and your roof type to see the damage it typically causes, plus what to do next after an Austin hailstorm.',
    'lead' => 'Choose the hail size you saw and your roof type to see what damage is likely — and what to do next.',
    'intro' => '<p>Click a hailstone size, then choose your roof type and age.</p>',
    'body' => $body,
    'weather' => 'hail',
    'related' => ['hail-damage-repair', 'roof-insurance-claims', 'emergency-roof-repair', 'roof-inspection'],
    'faqs' => [
        ['What size hail damages a roof?', '<p>Around 1 inch (quarter size) is the common threshold for damage to standard asphalt shingles. Older roofs can be damaged by smaller hail; Class 4 shingles resist up to about 2 inches.</p>'],
        ['Can hail damage be invisible?', '<p>Yes. Bruised shingles often look fine from the ground but have cracked mats and lost granules that shorten roof life and lead to leaks later.</p>'],
        ['How long do I have to file a hail claim in Texas?', '<p>Deadlines depend on your policy, and many Texas policies require you to report storm damage within a set period. Check your policy and contact your insurer promptly.</p>'],
        ['Is hail damage on metal roofs covered?', '<p>It depends on your policy. Some Texas policies exclude purely cosmetic dents on metal roofs, while functional damage that lets water in is typically covered.</p>'],
    ],
]);
