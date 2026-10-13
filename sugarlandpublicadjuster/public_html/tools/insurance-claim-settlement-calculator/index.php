<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/tool.php';
$faqs = [
    ['Why is my first insurance check smaller than the estimate?', '<p>On a replacement cost policy, most insurers first pay the <strong>actual cash value</strong>—the replacement cost minus depreciation and your deductible. The withheld depreciation is usually “recoverable” once repairs are completed and documented, within the time your policy allows.</p>'],
    ['What if my contractor’s estimate is much higher than the insurer’s?', '<p>That gap is common. It usually comes from missed line items, unit-price differences, matching, code upgrades or overhead and profit. A Sugar Land public adjuster compares the two estimates line by line and submits a documented supplement for what was missed.</p>'],
    ['Is the deductible subtracted from the insurer’s estimate or mine?', '<p>The deductible is subtracted from the covered loss amount the insurer agrees to. Either way you pay it—so it belongs in your budget, not in the “gap” you can recover.</p>'],
];
tool_start('insurance-claim-settlement-calculator', 'Insurance Claim Settlement Calculator',
    'Insurance Claim Settlement Calculator | Sugar Land Public Adjuster',
    'Free claim settlement calculator: compare the insurer’s payment with your real repair cost after deductible and depreciation. By a Sugar Land public adjuster.',
    'Insurance Claim Settlement Calculator',
    'See what your insurer is actually paying, what depreciation you can still recover, and how far the settlement falls short of the real repair cost.', $faqs);
?>
<form class="tool" id="settle" onsubmit="return false">
  <h2>Your claim numbers</h2>
  <div class="tool-grid">
    <label>Contractor / your repair estimate <span class="hint">What it really costs to restore the property</span><span class="money"><input type="number" name="real" min="0" step="100" value="38000" inputmode="decimal"></span></label>
    <label>Insurer’s estimate (replacement cost) <span class="hint">“RCV” or “Replacement Cost Value” on their estimate</span><span class="money"><input type="number" name="rcv" min="0" step="100" value="24000" inputmode="decimal"></span></label>
    <label>Depreciation withheld <span class="hint">Total depreciation shown on the insurer’s estimate</span><span class="money"><input type="number" name="dep" min="0" step="100" value="6500" inputmode="decimal"></span></label>
    <label>Deductible <span class="hint">Dollar amount (use the deductible calculator for % deductibles)</span><span class="money"><input type="number" name="ded" min="0" step="100" value="4000" inputmode="decimal"></span></label>
    <label>Non-recoverable depreciation <span class="hint">Usually $0 on RCV policies; all of it on ACV policies</span><span class="money"><input type="number" name="nonrec" min="0" step="100" value="0" inputmode="decimal"></span></label>
    <label>Policy type
      <select name="policy"><option value="rcv">Replacement cost (RCV)</option><option value="acv">Actual cash value (ACV)</option></select>
    </label>
  </div>
  <div class="tool-results" aria-live="polite">
    <div class="result-grid">
      <div class="result"><span>First check (ACV)</span><strong data-out="acv">—</strong></div>
      <div class="result"><span>Recoverable later</span><strong data-out="recov">—</strong></div>
      <div class="result hl"><span>Insurer pays in total</span><strong data-out="total">—</strong></div>
      <div class="result bad"><span>Shortfall vs. real cost</span><strong data-out="gap">—</strong></div>
    </div>
    <p class="mt-2 mb-0"><strong data-out="pct">—</strong> of the real repair cost (after your deductible) is covered.</p>
    <div class="bar"><i data-out="bar" style="width:0"></i></div>
    <p class="mb-0" data-out="msg"></p>
  </div>
  <div class="tool-actions"><button type="button" class="btn btn-primary" data-open-popup>Have a Sugar Land public adjuster review this gap</button><button type="button" class="btn btn-outline" onclick="window.print()">Print results</button></div>
</form>

<section class="prose mt-2">
  <h2>How to read your insurance estimate</h2>
  <ul>
    <li><strong>RCV (replacement cost value):</strong> the insurer’s price to repair or replace with like kind and quality, before depreciation.</li>
    <li><strong>Depreciation:</strong> the reduction for age and condition. On an RCV policy most of it is <em>recoverable</em> once repairs are finished.</li>
    <li><strong>ACV (actual cash value):</strong> RCV minus depreciation. This is usually the first check.</li>
    <li><strong>Deductible:</strong> your share of every covered loss—flat dollars or a percentage of your dwelling limit.</li>
  </ul>
  <p>If the shortfall is large, the problem is usually the <em>scope</em> (what the insurer included), not just the price. Missing rooms, matching, code-required items and overhead and profit are the usual suspects. Read more in <a href="/how-much-does-a-public-adjuster-cost-in-texas/">how much a public adjuster costs in Texas</a> and <a href="/services/denied-underpaid-claims/">underpaid claims</a>.</p>
</section>
<?php tool_end($faqs); ?>
