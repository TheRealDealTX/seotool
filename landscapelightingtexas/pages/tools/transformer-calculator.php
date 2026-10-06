<?php defined('LLT') or die(http_response_code(404));
$P['eyebrow'] = 'Low-voltage planning';
$P['lead'] = 'Size a 12V landscape lighting transformer and check voltage drop for your wire gauge, run length and wiring method — with the tap setting to use.';
$P['tools_js'] = true;
$P['hero_no_cta'] = true;
?>
<section class="section">
  <div class="container reveal"><?php widget_transformer(); ?></div>
</section>
<section class="section alt">
  <div class="container narrow prose reveal">
<h2>How the Calculator Works</h2>
<p>Low-voltage landscape lighting steps 120V house power down to about 12V. Two numbers decide whether a system performs: <strong>transformer load</strong> and <strong>voltage drop</strong>.</p>
<ul>
<li><strong>Transformer size:</strong> add up fixture wattage and divide by 0.8. Running a transformer at 80% or less keeps it cool and leaves room to add fixtures.</li>
<li><strong>Voltage drop:</strong> current flowing through cable loses voltage over distance. We use <em>V = 2 × L × I × R ÷ 1,000</em>, where L is run length in feet, I is amps (watts ÷ 12) and R is the cable resistance per 1,000 feet.</li>
<li><strong>Taps:</strong> multi-tap transformers offer 12, 13, 14 and 15V outputs, so you can push a little extra voltage down a long run and land near 11–12V at the fixtures.</li>
</ul>
<div class="table-wrap"><table><thead><tr><th>Wire gauge</th><th>Resistance (Ω per 1,000 ft)</th><th>Typical use</th></tr></thead><tbody>
<tr><td>16 AWG</td><td>4.02</td><td>Fixture leads, very short runs</td></tr>
<tr><td>14 AWG</td><td>2.53</td><td>Light loads under ~60W, short runs</td></tr>
<tr><td>12 AWG</td><td>1.59</td><td>The workhorse for most home runs</td></tr>
<tr><td>10 AWG</td><td>1.00</td><td>Long runs and heavy loads</td></tr>
<tr><td>8 AWG</td><td>0.63</td><td>Feeder runs to distant hubs</td></tr>
</tbody></table></div>
<h2>Why Hub Wiring Matters</h2>
<p>Daisy-chaining fixtures along one cable puts the full load at the far end, so the last lights are dimmer. Hub (or split-load) wiring runs a heavier cable to a central point and branches out with short, equal leads — every fixture sees nearly the same voltage. It is standard practice on Landscape Lighting Texas installations. Learn more in our <a href="/low-voltage-landscape-lighting-guide/">low-voltage lighting guide</a>.</p>

  </div>
</section>
<?php faqs([
    ['What size transformer do I need?', 'Total your LED wattage and divide by 0.8, then round up to the next standard size (75W, 150W, 200W, 300W and so on). Leave room for future fixtures.'],
    ['How much voltage drop is acceptable?', 'Aim for fixtures between about 10.8V and 12V. Most LEDs tolerate a wider range, but consistent voltage keeps brightness and color even.'],
    ['Do I need an electrician?', 'Low-voltage cable work generally does not, but adding a new 120V outlet or circuit for the transformer should be done by a licensed electrician.'],
]); ?>
<section class="section">
  <div class="container">
    <?php section_head('More free tools', 'Keep Planning Your Project'); tool_cards('/tools/transformer-calculator/'); ?>
  </div>
</section>
<?php cta_band();
