<?php
require dirname(__DIR__, 2) . '/includes/layout.php';

$body = <<<'HTML'
<h2>What Is a Roofing Square?</h2>
<p class="lead">One roofing square equals <strong>100 square feet of roof surface</strong>. Shingles, underlayment and labor are all priced per square, so knowing your square count is the key to reading any roofing estimate. Full explanation: <a href="/blog/what-is-a-square-in-roofing/">What is a square in roofing?</a></p>
<h2>How to Calculate Roofing Squares</h2>
<ol class="steps">
  <li><h3>Measure the footprint</h3><p>Length × width of the house, plus the eave overhang on every side.</p></li>
  <li><h3>Apply the pitch</h3><p>Multiply by the pitch factor — 1.118 for a 6/12 roof. Find yours with the <a href="/roofing-tools/roof-pitch-calculator/">roof pitch calculator</a>.</p></li>
  <li><h3>Add waste</h3><p>10% for simple gables, about 15% for hip roofs, more for complex roofs.</p></li>
  <li><h3>Divide by 100</h3><p>The result is your square count. Multiply by 3 for bundles of standard architectural shingles.</p></li>
</ol>
<h2>Pitch Multipliers</h2>
<div class="table-wrap"><table>
  <thead><tr><th>Pitch</th><th>Multiplier</th><th>Pitch</th><th>Multiplier</th></tr></thead>
  <tbody>
    <tr><td>3/12</td><td>1.031</td><td>8/12</td><td>1.202</td></tr>
    <tr><td>4/12</td><td>1.054</td><td>9/12</td><td>1.250</td></tr>
    <tr><td>5/12</td><td>1.083</td><td>10/12</td><td>1.302</td></tr>
    <tr><td>6/12</td><td>1.118</td><td>11/12</td><td>1.357</td></tr>
    <tr><td>7/12</td><td>1.158</td><td>12/12</td><td>1.414</td></tr>
  </tbody>
</table></div>
<h2>Materials Per Square at a Glance</h2>
<ul>
  <li><strong>Shingles:</strong> usually 3 bundles per square for standard architectural shingles (some heavier designer lines use 4–5).</li>
  <li><strong>Underlayment:</strong> synthetic rolls cover roughly 10 squares; #15 felt about 4; #30 felt about 2. Compare them in our <a href="/blog/roofing-underlayment-material-types/">roofing underlayment types guide</a>.</li>
  <li><strong>Starter strip and drip edge:</strong> run the full perimeter of the eaves and rakes.</li>
  <li><strong>Ridge cap:</strong> covers every ridge and hip.</li>
  <li><strong>Self-adhered membrane:</strong> valleys, penetrations and low-slope areas — see <a href="/blog/ice-and-water-shield-installation-cost/">ice and water shield costs</a>.</li>
</ul>
<p>Want to turn squares into dollars? Read <a href="/blog/cost-of-asphalt-shingles-per-square/">cost of asphalt shingles per square</a> or try the <a href="/roofing-tools/roof-cost-calculator/">roof cost calculator</a>.</p>
HTML;

render_tool([
    'slug' => 'roofing-square-calculator',
    'title' => 'Roofing Square Calculator & Shingle Bundle Estimator | Austin Roofing',
    'description' => 'Free roofing square calculator: convert house dimensions and pitch into roofing squares, shingle bundles, underlayment rolls, starter, ridge cap and drip edge.',
    'lead' => 'Turn your home’s dimensions and roof pitch into squares, shingle bundles, underlayment rolls and trim — instantly.',
    'intro' => '<p>Enter length and width (or total footprint), pick your pitch and roof style. Results update as you type.</p>',
    'body' => $body,
    'related' => ['shingle-roofing', 'roof-replacement', 'roof-installation', 'roof-repair'],
    'faqs' => [
        ['How many bundles of shingles are in a square?', '<p>Most standard architectural shingles come 3 bundles per square. Some heavier premium shingles need 4 or 5 — always check the wrapper.</p>'],
        ['How much is a square of shingles?', '<p>Material alone is commonly about $100–$200 per square for architectural shingles; installed prices in Austin typically run around $450–$650 per square. See our <a href="/blog/cost-of-asphalt-shingles-per-square/">price per square guide</a>.</p>'],
        ['What waste factor should I use?', '<p>About 10% for a simple gable roof and 15% for a hip roof. Roofs with many valleys, dormers or turrets can need 18–20%.</p>'],
        ['Can I measure my roof from the ground?', '<p>Yes, for an estimate: measure the house footprint, add overhangs and apply the pitch multiplier. A roofer measures each plane for an exact order.</p>'],
    ],
]);
