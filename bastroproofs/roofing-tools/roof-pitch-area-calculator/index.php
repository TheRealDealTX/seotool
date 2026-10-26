<?php
$slug = 'roof-pitch-area-calculator';
$toolFaqs = [
    ['q' => 'What does roof pitch mean?', 'a' => 'Pitch is how many inches a roof rises for every 12 inches of horizontal run. A 6/12 roof rises 6 inches per foot, which is about 26.6 degrees. Most Bastrop homes fall between 4/12 and 9/12.'],
    ['q' => 'What is a roofing square?', 'a' => 'A roofing square is 100 square feet of roof surface. Roofers price and order materials by the square, so a 2,500 square foot roof is 25 squares before waste.'],
    ['q' => 'How do I find my roof pitch without climbing up?', 'a' => 'Look at a gable end from the ground and compare the slope to the diagram as you move the slider, or check your home\'s plans. We measure pitch precisely during every free inspection, so you never need to go on the roof.'],
];
$toolBody = <<<'HTML'
<h2>How to Measure Your Roof Safely</h2>
<p>You never need to climb onto a roof to use this calculator. Measure the outside length and width of the house at ground level, estimate the overhang at the eaves, and match the pitch slider to the slope you see at a gable end. The tool multiplies the footprint by the pitch factor to find the true sloped surface area.</p>
<h2>Common Roof Pitches in Bastrop</h2>
<table>
<thead><tr><th>Pitch</th><th>Angle</th><th>Area multiplier</th><th>Typical use</th></tr></thead>
<tbody>
<tr><td>3/12</td><td>14.0°</td><td>1.031</td><td>Porches, metal shop and barn roofs</td></tr>
<tr><td>4/12</td><td>18.4°</td><td>1.054</td><td>Ranch homes, many metal roofs</td></tr>
<tr><td>6/12</td><td>26.6°</td><td>1.118</td><td>Most subdivision homes</td></tr>
<tr><td>8/12</td><td>33.7°</td><td>1.202</td><td>Two-story and traditional homes</td></tr>
<tr><td>12/12</td><td>45.0°</td><td>1.414</td><td>Steep farmhouse and Victorian styles</td></tr>
</tbody>
</table>
<p>Got your squares? Plug them into the <a href="/roofing-tools/roof-replacement-cost-calculator/">roof replacement cost calculator</a>, or ask about <a href="/services/residential-roofing-bastrop-tx/">residential roofing in Bastrop</a> for an exact measurement and quote from <a href="/">Bastrop Roofing</a>.</p>
HTML;
require dirname(__DIR__, 2) . '/includes/templates/tool.php';
