<?php
require dirname(__DIR__, 2) . '/includes/layout.php';

$body = <<<'HTML'
<h2>What Is Roof Pitch?</h2>
<p class="lead">Roof pitch is how many inches a roof rises for every 12 inches it runs horizontally. A 6/12 roof climbs 6 inches per foot — about 26.6°. Pitch decides which materials you can use, how much surface area you are buying and how much labor and safety equipment the job needs.</p>
<h2>How to Measure Your Roof Pitch</h2>
<ol class="steps">
  <li><h3>Use a level</h3><p>Hold a 12-inch level horizontally against the rafter or roof surface.</p></li>
  <li><h3>Measure the rise</h3><p>From the 12-inch mark on the level, measure straight up (or down) to the roof.</p></li>
  <li><h3>Read the pitch</h3><p>That measurement in inches is your rise — enter it above.</p></li>
</ol>
<p>Measuring from the attic on a rafter is the safest method. Please don’t climb onto a steep roof — Austin Roofing will measure it for you during a free <a href="/services/roof-inspection/">roof inspection</a>.</p>
<h2>Common Pitches and What They Mean</h2>
<div class="table-wrap"><table>
  <thead><tr><th>Pitch</th><th>Angle</th><th>Category</th><th>Typical roofing</th></tr></thead>
  <tbody>
    <tr><td>Under 2/12</td><td>&lt; 9.5°</td><td>Flat / low slope</td><td>TPO, EPDM, modified bitumen, coatings</td></tr>
    <tr><td>2/12 – 4/12</td><td>9.5° – 18.4°</td><td>Low slope</td><td>Shingles with full self-adhered underlayment, metal</td></tr>
    <tr><td>4/12 – 7/12</td><td>18.4° – 30.3°</td><td>Conventional</td><td>Any shingle, metal, stone-coated steel</td></tr>
    <tr><td>7/12 – 9/12</td><td>30.3° – 36.9°</td><td>Steep</td><td>Shingles, metal, tile</td></tr>
    <tr><td>10/12 and up</td><td>39.8°+</td><td>Very steep</td><td>Shingles, metal, slate — specialty install</td></tr>
  </tbody>
</table></div>
<h2>Why Pitch Matters for Cost</h2>
<p>Two houses with identical footprints can have very different roof areas. A 12/12 roof has about 41% more surface than a flat one over the same footprint — and steep roofs need harnesses, roof jacks and slower installation. Use the multiplier with our <a href="/roofing-tools/roofing-square-calculator/">roofing square calculator</a> or <a href="/roofing-tools/roof-cost-calculator/">roof cost calculator</a>, and learn more in <a href="/blog/what-is-a-square-in-roofing/">what is a square in roofing</a>.</p>
HTML;

render_tool([
    'slug' => 'roof-pitch-calculator',
    'title' => 'Roof Pitch Calculator: Pitch, Angle & Multiplier | Austin Roofing',
    'description' => 'Free roof pitch calculator. Enter rise and run, or an angle, to get roof pitch, degrees, slope percentage and the area multiplier — with a live roof diagram.',
    'lead' => 'Get your roof pitch, angle, slope and area multiplier from rise and run — with a live roof diagram.',
    'intro' => '<p>Drag the slider, enter measured rise and run, or type an angle. The diagram updates as you go.</p>',
    'body' => $body,
    'related' => ['roof-replacement', 'roof-installation', 'shingle-roofing', 'metal-roofing'],
    'weather' => 'sun',
    'faqs' => [
        ['What is the most common roof pitch in Austin?', '<p>Most Austin-area homes have conventional pitches between about 4/12 and 8/12, with steeper roofs common on newer two-story and Hill Country homes.</p>'],
        ['What is the minimum pitch for shingles?', '<p>Asphalt shingle manufacturers generally allow 2/12 to 4/12 only with special double-layer or self-adhered underlayment, and standard installation at 4/12 and above.</p>'],
        ['How do I convert pitch to degrees?', '<p>Degrees = arctangent(rise ÷ 12). A 6/12 pitch is about 26.6°, 8/12 is 33.7° and 12/12 is 45°.</p>'],
        ['Does a steeper roof cost more?', '<p>Yes. It has more surface area and needs more safety equipment and labor time, so the price per square rises on roofs steeper than about 8/12.</p>'],
    ],
]);
