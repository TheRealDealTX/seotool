<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/tool.php';
$faqs = [
    ['How is a percentage hurricane deductible calculated?', '<p>It is a percentage of your Coverage A (dwelling) limit shown on your declarations page—not a percentage of the damage. A 2% deductible on a $400,000 dwelling limit is $8,000.</p>'],
    ['Which deductible applies—named storm, wind/hail or all other perils?', '<p>Your policy defines it. Some policies apply a separate deductible only to named storms or hurricanes; others apply a wind/hail deductible to any wind or hail event. Water damage from a burst pipe usually falls under the all-other-perils (AOP) deductible.</p>'],
    ['Is my Sugar Land home in the TWIA coastal area?', '<p>No—Fort Bend County is outside the Texas Windstorm Insurance Association’s designated catastrophe area, so wind coverage normally comes from your regular homeowners policy.</p>'],
];
tool_start('hurricane-deductible-calculator', 'Hurricane Deductible Calculator',
    'Hurricane & Wind/Hail Deductible Calculator | Sugar Land Public Adjuster',
    'Convert a percentage hurricane or wind/hail deductible into dollars and see what your insurer would pay on a storm claim. Free tool for Sugar Land homeowners.',
    'Hurricane &amp; Wind/Hail Deductible Calculator',
    'Percentage deductibles surprise a lot of Sugar Land homeowners after a storm. Find out what yours is in dollars—before the next hurricane season.', $faqs);
?>
<form class="tool" id="hded" onsubmit="return false">
  <h2>Your policy</h2>
  <div class="tool-grid">
    <label>Dwelling limit (Coverage A) <span class="hint">On your declarations page</span><span class="money"><input type="number" name="dwell" min="0" step="5000" value="425000" inputmode="decimal"></span></label>
    <label>Hurricane / wind-hail deductible
      <select name="pct"><option value="0.01">1%</option><option value="0.02" selected>2%</option><option value="0.03">3%</option><option value="0.05">5%</option><option value="flat">Flat dollar amount</option></select>
    </label>
    <label data-flat hidden>Flat wind/hail deductible <span class="money"><input type="number" name="flat" min="0" step="250" value="2500" inputmode="decimal"></span></label>
    <label>All-other-perils (AOP) deductible <span class="hint">Applies to non-wind losses like a burst pipe</span><span class="money"><input type="number" name="aop" min="0" step="250" value="2500" inputmode="decimal"></span></label>
    <label>Estimated storm damage <span class="money"><input type="number" name="damage" min="0" step="500" value="22000" inputmode="decimal"></span></label>
  </div>
  <div class="tool-results" aria-live="polite">
    <div class="result-grid">
      <div class="result hl"><span>Wind/hurricane deductible</span><strong data-out="ded">—</strong></div>
      <div class="result"><span>vs. AOP deductible</span><strong data-out="aopdiff">—</strong></div>
      <div class="result good"><span>Insurer would pay</span><strong data-out="pays">—</strong></div>
      <div class="result"><span>You pay</span><strong data-out="you">—</strong></div>
    </div>
    <div class="bar"><i data-out="bar" style="width:0"></i></div>
    <p class="mb-0" data-out="msg"></p>
  </div>
</form>
<section class="prose mt-2">
  <h2>Why this matters in Sugar Land</h2>
  <p>Hurricane Beryl in July 2024 showed how many Fort Bend County homeowners were carrying percentage deductibles they had never converted to dollars. When damage lands just above the deductible, small scope errors decide whether you receive anything at all—so documentation matters even more. See our <a href="/services/hurricane-wind-damage-claims/">hurricane &amp; wind damage claims</a> page and the <a href="/hurricane-preparedness-checklist/">hurricane preparedness checklist</a>.</p>
</section>
<?php tool_end($faqs); ?>
