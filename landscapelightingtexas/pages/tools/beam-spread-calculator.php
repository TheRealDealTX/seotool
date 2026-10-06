<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Beam angles';
$P['lead'] = 'Calculate how wide a landscape light beam will be at any distance, see the footcandles on your target, and find the right beam angle for trees, columns, walls and signs.';
$P['tools_js'] = true;
$P['hero_no_cta'] = true;
?>
<section class="section">
  <div class="container reveal"><?php widget_beam(); ?></div>
</section>
<section class="section alt">
  <div class="container narrow prose reveal">
<h2>The Beam Spread Formula</h2>
<p>A fixture's beam angle tells you how fast its light spreads. The diameter of the lit circle at any distance is <em>2 × distance × tan(angle ÷ 2)</em>. A 36° beam, for example, covers about 9.7 feet at 15 feet — perfect for a medium tree or a facade bay.</p>
<div class="table-wrap"><table><thead><tr><th>Beam angle</th><th>Spread at 10 ft</th><th>Spread at 20 ft</th><th>Best for</th></tr></thead><tbody>
<tr><td>10°</td><td>1.7 ft</td><td>3.5 ft</td><td>Tall palms, flagpoles, narrow columns</td></tr>
<tr><td>15°</td><td>2.6 ft</td><td>5.3 ft</td><td>Columns, chimneys, tall narrow trees</td></tr>
<tr><td>25°</td><td>4.4 ft</td><td>8.9 ft</td><td>Trunks, small trees, architectural details</td></tr>
<tr><td>36°</td><td>6.5 ft</td><td>13.0 ft</td><td>Medium trees, facade sections</td></tr>
<tr><td>45°</td><td>8.3 ft</td><td>16.6 ft</td><td>Wide canopies, shrubs, wall washing</td></tr>
<tr><td>60°</td><td>11.5 ft</td><td>23.1 ft</td><td>Broad walls, large shrub masses</td></tr>
</tbody></table></div>
<h2>Footcandles and Brightness</h2>
<p>Footcandles measure the light that actually lands on a surface. Landscape lighting is subtle: 1–5 footcandles reads as a soft accent, 5–10 is a strong focal point, and anything much brighter tends to look harsh against a dark sky. That is why designers often prefer two modest fixtures cross-lighting a tree over one powerful spotlight. See our guide to <a href="/how-to-light-live-oak-trees/">lighting live oak trees</a> for real-world fixture counts.</p>

  </div>
</section>
<?php faqs([
    ['What beam angle should I use for a tree?', 'It depends on the tree height and distance. Narrow 15–25° beams suit tall, slim trees and trunks; 36–60° beams suit wide canopies like live oaks, usually with two or more fixtures.'],
    ['Does beam angle affect brightness?', 'Yes. The same lumens spread over a wider area produce fewer footcandles, so wide beams look softer.'],
    ['Should I aim lights straight up?', 'Usually slightly angled toward the feature and away from viewers, with glare shields where fixtures are visible from paths or windows.'],
]); ?>
<section class="section">
  <div class="container">
    <?php section_head('More free tools', 'Keep Planning Your Project'); tool_cards('/tools/beam-spread-calculator/'); ?>
  </div>
</section>
<?php cta_band();
