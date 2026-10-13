<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/tool.php';
$faqs = [
    ['What is the maximum public adjuster fee in Texas?', '<p>Texas law caps a public adjuster’s compensation at 10% of the amount of the insurance settlement on the claim (Texas Insurance Code §4102.104). There are no upfront fees—the fee comes out of the recovery.</p>'],
    ['Does the fee apply to money the insurer already offered?', '<p>That depends on the contract you sign, so ask before you sign. Some adjusters charge only on the amount above the offer already on the table when they are hired. Use the “fee basis” setting to compare both.</p>'],
    ['When is hiring a public adjuster not worth it?', '<p>If the damage is barely above your deductible, or the insurer’s offer already matches a reliable contractor estimate, the fee may outweigh the benefit. We will tell you honestly if that is your situation.</p>'],
];
tool_start('public-adjuster-fee-calculator', 'Public Adjuster Fee Calculator',
    'Public Adjuster Fee Calculator (Texas 10% Cap) | Sugar Land Public Adjuster',
    'See what a public adjuster costs in Texas and your net recovery with and without representation. Free calculator from a Sugar Land public adjuster.',
    'Public Adjuster Fee Calculator',
    'Texas caps public adjuster fees at 10% of the settlement. See your fee, your net recovery, and the break-even point before you hire anyone.', $faqs);
?>
<form class="tool" id="fee" onsubmit="return false">
  <h2>Compare going alone vs. hiring a public adjuster</h2>
  <div class="tool-grid">
    <label>Insurer’s current offer <span class="hint">What you’d get without help ($0 if denied)</span><span class="money"><input type="number" name="offer" min="0" step="500" value="18000" inputmode="decimal"></span></label>
    <label>Expected settlement with a public adjuster <span class="hint">e.g. your contractor’s estimate, minus deductible</span><span class="money"><input type="number" name="settle" min="0" step="500" value="41000" inputmode="decimal"></span></label>
    <label>Fee percentage <span class="hint">Texas maximum is 10%</span><input type="number" name="pct" min="0" max="10" step="0.5" value="10" inputmode="decimal"></label>
    <label>Fee basis
      <select name="basis"><option value="all">Entire settlement</option><option value="new">Only the increase over the current offer</option></select>
    </label>
  </div>
  <div class="tool-results" aria-live="polite">
    <div class="result-grid">
      <div class="result"><span>On your own</span><strong data-out="alone">—</strong></div>
      <div class="result"><span>Public adjuster fee</span><strong data-out="fee">—</strong></div>
      <div class="result hl"><span>Your net with a PA</span><strong data-out="net">—</strong></div>
      <div class="result" data-out-class="diffbox"><span>Difference</span><strong data-out="diff">—</strong></div>
    </div>
    <p class="mt-2 mb-0" data-out="msg"></p>
  </div>
</form>
<section class="prose mt-2">
  <h2>How public adjuster fees work in Texas</h2>
  <p>Public adjusters are licensed by the Texas Department of Insurance and are paid a contingency fee—a percentage of what the insurer pays on the claim. By law that fee cannot exceed 10% of the settlement. You owe nothing upfront and nothing if there is no recovery.</p>
  <p>The math only works if representation increases the settlement by more than the fee. That is why we review the claim for free first. Read the full breakdown in <a href="/how-much-does-a-public-adjuster-cost-in-texas/">How Much Does a Public Adjuster Cost in Texas?</a></p>
</section>
<?php tool_end($faqs); ?>
