<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Color temperature';
$P['lead'] = 'Drag from candle-warm 2200K to daylight 5000K and watch how color temperature changes stone, trees, water and garden paths at night.';
$P['tools_js'] = true;
$P['hero_no_cta'] = true;
?>
<section class="section">
  <div class="container reveal"><?php widget_kelvin(); ?></div>
</section>
<section class="section alt">
  <div class="container narrow prose reveal">
<h2>What Is Color Temperature?</h2>
<p>Color temperature, measured in Kelvin (K), describes how warm or cool white light looks. Lower numbers are amber and candle-like; higher numbers are crisp and blue-white. It has nothing to do with heat — a 5000K LED runs no hotter than a 2700K LED.</p>
<div class="table-wrap"><table><thead><tr><th>Kelvin</th><th>Look</th><th>Typical landscape use</th></tr></thead><tbody>
<tr><td>2200K</td><td>Amber, candlelight</td><td>Patios, fire features, dark-sky areas</td></tr>
<tr><td>2700K</td><td>Warm white</td><td>Facades, entries, paths — the residential standard</td></tr>
<tr><td>3000K</td><td>Soft white</td><td>Trees and foliage, modern architecture</td></tr>
<tr><td>4000K</td><td>Neutral white</td><td>Specimen plants, commercial exteriors</td></tr>
<tr><td>5000K</td><td>Daylight</td><td>Security and utility only</td></tr>
</tbody></table></div>
<h2>Choosing the Right Kelvin for Texas Homes</h2>
<p>Limestone, Austin stone and red brick glow at 2700K, which is why it is our default for architecture. Live oaks and other foliage often look more natural at 3000K, and some designs pair 2700K on the house with 3000K in the trees. Whatever you choose, keep it consistent — mixing a 2700K path light with a 4000K floodlight is one of the most common reasons a yard looks &ldquo;off.&rdquo;</p>
<p>Warm light is also better for the night sky and wildlife, which matters in Hill Country and West Texas communities with outdoor lighting ordinances. Our <a href="/landscape-lighting-color-temperature-guide/">full color temperature guide</a> goes deeper, and the <a href="/services/architectural-uplighting/">architectural uplighting</a> page shows how we put it into practice.</p>

  </div>
</section>
<?php faqs([
    ['What color temperature is best for landscape lighting?', '2700K is the most popular choice for homes because it flatters stone, brick and wood. 3000K is common for trees and foliage.'],
    ['Do warmer lights attract fewer bugs?', 'Generally, warm amber light attracts fewer insects than cool, blue-rich light, though no light is completely bug-free.'],
    ['Can I change color temperature later?', 'With tunable or RGBW smart fixtures, yes. With standard fixtures, color temperature is set by the lamp or LED module chosen.'],
]); ?>
<section class="section">
  <div class="container">
    <?php section_head('More free tools', 'Keep Planning Your Project'); tool_cards('/tools/color-temperature-visualizer/'); ?>
  </div>
</section>
<?php cta_band();
