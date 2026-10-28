<?php
require dirname(__DIR__, 2) . '/includes/layout.php';

$body = <<<'HTML'
<h2>How the Austin Roof Cost Calculator Works</h2>
<p class="lead">Roofers don’t price a roof by your home’s square footage — they price it by <strong>roofing squares</strong> (100 sq ft of roof surface). This calculator converts your living area into an estimated roof area, then applies typical 2026 installed prices for the Austin area.</p>
<ol class="steps">
  <li><h3>Footprint</h3><p>Living area ÷ stories, plus about 15% for eaves and an attached garage.</p></li>
  <li><h3>Pitch &amp; shape</h3><p>Steeper and more complex roofs have more surface area — a 6/12 hip roof adds roughly 20%.</p></li>
  <li><h3>Waste</h3><p>About 12% is added for cuts at valleys, hips and edges.</p></li>
  <li><h3>Price per square</h3><p>Material-specific installed ranges, adjusted for steep pitch, two stories and extra tear-off layers.</p></li>
</ol>
<h2>Typical Installed Price per Square in Austin (2026 planning ranges)</h2>
<div class="table-wrap"><table>
  <thead><tr><th>Material</th><th>Installed per square</th><th>Typical life in Texas</th></tr></thead>
  <tbody>
    <tr><td>3-tab asphalt shingles</td><td>$380 – $500</td><td>15–20 years</td></tr>
    <tr><td>Architectural (dimensional) shingles</td><td>$450 – $650</td><td>20–25 years</td></tr>
    <tr><td>Class 4 impact-resistant shingles</td><td>$575 – $800</td><td>25–30 years</td></tr>
    <tr><td>Stone-coated steel</td><td>$900 – $1,400</td><td>40–50 years</td></tr>
    <tr><td>Standing seam metal</td><td>$1,000 – $1,600</td><td>40–60 years</td></tr>
  </tbody>
</table></div>
<p>These are general planning ranges, not quotes. Your actual price depends on access, decking condition, ventilation upgrades, flashing details, permit requirements and the specific product line chosen.</p>
<h2>What the Calculator Doesn’t Include</h2>
<ul>
  <li><strong>Decking replacement</strong> — rotted plywood or OSB is usually priced per sheet once the old roof is off.</li>
  <li><strong>Ventilation upgrades</strong> — ridge vent, added intake or power-vent removal. See <a href="/blog/attic-ventilation-upgrade-benefits/">attic ventilation upgrade benefits</a>.</li>
  <li><strong>Gutters, skylights and chimney work</strong>.</li>
  <li><strong>Permits</strong> — requirements vary by city; read our guide to <a href="/blog/roof-replacement-permit-requirements/">roof replacement permit requirements</a>.</li>
  <li><strong>Insurance</strong> — if hail or wind damaged the roof, your policy may cover much of the cost after your deductible.</li>
</ul>
<p>For a deeper breakdown, read <a href="/blog/how-much-does-it-cost-to-replace-a-roof/">how much it costs to replace a roof on a 1,500 sq ft house</a> and our <a href="/blog/cost-of-asphalt-shingles-per-square/">shingle price per square guide</a>, or let Austin Roofing measure your roof for an exact <a href="/services/roof-replacement/">roof replacement</a> quote.</p>
HTML;

render_tool([
    'slug' => 'roof-cost-calculator',
    'title' => 'Roof Replacement Cost Calculator (Austin, TX) | Austin Roofing',
    'description' => 'Free roof replacement cost calculator for Austin, TX. Estimate roofing squares and installed cost by home size, pitch, roof shape and material in seconds.',
    'lead' => 'Estimate what a new roof costs in the Austin area — by home size, pitch, roof shape, material and tear-off layers.',
    'intro' => '<p>Move the slider and pick your options — the estimate updates instantly. Nothing you enter leaves your browser.</p>',
    'body' => $body,
    'related' => ['roof-replacement', 'shingle-roofing', 'metal-roofing', 'roof-inspection'],
    'faqs' => [
        ['How accurate is this roof cost calculator?', '<p>It gives a realistic planning range for typical Austin homes. Exact pricing requires measuring every roof plane and checking decking, ventilation and flashing — which Austin Roofing does for free.</p>'],
        ['How many squares is a 2,000 sq ft house?', '<p>A one-story 2,000 sq ft home with a medium-pitch hip roof usually needs roughly 28–32 squares including waste. A two-story home of the same size needs about half as many.</p>'],
        ['Why is metal so much more expensive than shingles?', '<p>Metal panels cost more per square and take more skilled labor to install, but they typically last two to three times as long as asphalt shingles in Texas heat.</p>'],
        ['Will insurance pay for my new roof?', '<p>If hail or wind caused the damage, your homeowners policy may cover replacement minus your deductible. Wear and tear is not covered. <a href="/services/roof-insurance-claims/">Learn how we help with claims</a>.</p>'],
    ],
]);
