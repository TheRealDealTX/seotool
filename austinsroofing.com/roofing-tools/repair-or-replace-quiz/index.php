<?php
require dirname(__DIR__, 2) . '/includes/layout.php';

$body = <<<'HTML'
<h2>Repair or Replace: How Roofers Decide</h2>
<p class="lead">The quiz weighs the same things an experienced roofer looks at during an inspection: age, active leaks, shingle condition, granule loss, storm history, structural sag and attic condition. No single factor decides it — it’s the combination.</p>
<div class="pros-cons">
  <div class="pros"><h4>Repair usually makes sense when…</h4><ul>
    <li>Damage is limited to one area or one cause</li>
    <li>The roof is under about 15 years old</li>
    <li>Shingles are still flexible and holding granules</li>
    <li>The decking is solid</li>
  </ul></div>
  <div class="cons"><h4>Replacement usually makes sense when…</h4><ul>
    <li>Leaks are showing up in multiple places</li>
    <li>Shingles are curling, cracking or bald across whole slopes</li>
    <li>The roof is 18–25+ years old in Texas heat</li>
    <li>Hail damaged enough of the roof for insurance to cover it</li>
  </ul></div>
</div>
<h2>Warning Signs You Can Check Today</h2>
<ul class="checklist">
  <li>Ceiling stains or peeling paint on upper floors</li>
  <li>Granules collecting at downspout outlets</li>
  <li>Missing, lifted or creased shingles after wind</li>
  <li>Dented gutters, vents or AC fins after hail</li>
  <li>Daylight or damp insulation in the attic</li>
  <li>A sagging or wavy roof line</li>
</ul>
<p>Whatever the quiz says, a professional inspection is the only way to be certain. Austin Roofing offers free inspections with photos, and we will tell you honestly if a <a href="/services/roof-repair/">roof repair</a> is enough or a <a href="/services/roof-replacement/">roof replacement</a> is the better value. Many roofs in the middle ground are also good candidates for <a href="/services/roof-restoration/">roof restoration</a>. For more on what shortens roof life here, see <a href="/blog/residential-metal-roofing-lifespan/">metal roofing lifespan</a> or check your own roof with the <a href="/roofing-tools/roof-lifespan-calculator/">roof lifespan calculator</a>.</p>
HTML;

render_tool([
    'slug' => 'repair-or-replace-quiz',
    'title' => 'Repair or Replace Your Roof? Free Quiz | Austin Roofing',
    'description' => 'Should you repair or replace your roof? Answer 7 quick questions on age, leaks, shingles, hail and your attic for an instant answer from Austin roofers.',
    'lead' => 'Seven quick questions. One honest answer about whether your roof needs a repair, a closer look or a replacement.',
    'intro' => '<p>Tap the answer that best fits your roof. Your result appears after question seven.</p>',
    'body' => $body,
    'related' => ['roof-repair', 'roof-replacement', 'roof-restoration', 'roof-inspection'],
    'faqs' => [
        ['Is it cheaper to repair or replace a roof?', '<p>A repair is almost always cheaper up front. But if a roof needs repeated repairs or is near the end of its life, replacement can cost less over time.</p>'],
        ['How many repairs before replacing a roof?', '<p>There is no fixed number, but if you are paying for repairs every year or leaks keep appearing in new places, it is time to compare replacement quotes.</p>'],
        ['Can a roof be partially replaced?', '<p>Sometimes — for example one damaged slope. Matching older shingles can be difficult, and insurers and manufacturers have rules about partial replacements.</p>'],
        ['Does a new roof add value to my home?', '<p>A new roof can make a home easier to sell and insure, and buyers in Austin often ask about roof age during inspections.</p>'],
    ],
]);
