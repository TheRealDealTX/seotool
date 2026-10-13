<?php
require $_SERVER['DOCUMENT_ROOT'] . '/inc/tool.php';
$faqs = [
    ['How do insurance companies calculate depreciation?', '<p>Most use a straight-line method: the item’s age divided by its expected useful life, multiplied by its replacement cost—then adjusted for condition. Life expectancy tables vary by carrier and estimating software, which is why two estimates can depreciate the same item differently.</p>'],
    ['Can labor be depreciated in Texas?', '<p>Policy language and estimating settings vary, and this is a frequently disputed item. If your estimate depreciates labor, ask the insurer to explain the basis in writing, and have a public adjuster review it.</p>'],
    ['How do I get my recoverable depreciation back?', '<p>On a replacement cost policy, complete the repairs or replacement and send the insurer proof—final invoices, receipts and photos—within the time your policy allows. Many policies set a deadline, so check yours.</p>'],
];
tool_start('depreciation-calculator', 'Depreciation (ACV) Calculator',
    'Insurance Depreciation Calculator (ACV vs RCV) | Sugar Land Public Adjuster',
    'Free depreciation calculator for insurance claims. Estimate actual cash value and recoverable depreciation for roofs, flooring, appliances and contents.',
    'Insurance Depreciation (ACV) Calculator',
    'Estimate how much an insurer will depreciate each damaged item—and how much of that money you can still recover on a replacement cost policy.', $faqs);
?>
<form class="tool" id="deprec" onsubmit="return false">
  <h2>Add damaged items</h2>
  <div class="tool-grid">
    <label>Item type
      <select name="preset">
        <option value="25">Architectural shingle roof (≈25 yr)</option>
        <option value="20">3-tab shingle roof (≈20 yr)</option>
        <option value="40">Metal roof (≈40 yr)</option>
        <option value="10">Carpet (≈10 yr)</option>
        <option value="25">Hardwood / tile flooring (≈25 yr)</option>
        <option value="15">Laminate / vinyl plank (≈15 yr)</option>
        <option value="10">Interior paint (≈10 yr)</option>
        <option value="15">Central A/C condenser (≈15 yr)</option>
        <option value="12">Water heater (≈12 yr)</option>
        <option value="13">Major appliance (≈13 yr)</option>
        <option value="15">Wood fence (≈15 yr)</option>
        <option value="7">Television / electronics (≈7 yr)</option>
        <option value="10">Sofa / upholstered furniture (≈10 yr)</option>
        <option value="5">Clothing (≈5 yr)</option>
        <option value="custom">Custom life expectancy…</option>
      </select>
    </label>
    <label>Description (optional)<input type="text" name="desc" placeholder="e.g. Living room carpet" maxlength="80"></label>
    <label>Replacement cost <span class="money"><input type="number" name="cost" min="0" step="50" value="18000" inputmode="decimal"></span></label>
    <label>Age (years)<input type="number" name="age" min="0" step="0.5" value="8" inputmode="decimal"></label>
    <label>Life expectancy (years)<input type="number" name="life" min="1" step="1" value="25" inputmode="decimal"></label>
    <label>Maximum depreciation % <span class="hint">Cap applied to very old items (set 100 for none)</span><input type="number" name="cap" min="0" max="100" step="5" value="80" inputmode="decimal"></label>
  </div>
  <div class="tool-results" aria-live="polite">
    <div class="result-grid">
      <div class="result"><span>Depreciation</span><strong data-out="dep">—</strong></div>
      <div class="result hl"><span>Actual cash value</span><strong data-out="acv">—</strong></div>
      <div class="result good"><span>Recoverable (RCV policy)</span><strong data-out="rec">—</strong></div>
    </div>
    <div class="tool-actions"><button type="button" class="btn btn-primary" data-add>Add to my list</button></div>
  </div>
  <div class="table-wrap mt-2" data-list-wrap hidden>
    <table class="data-table">
      <thead><tr><th>Item</th><th>Cost</th><th>Age / life</th><th>Depreciation</th><th>ACV</th><th></th></tr></thead>
      <tbody data-list></tbody>
      <tfoot><tr><th>Total</th><th data-t="cost"></th><th></th><th data-t="dep"></th><th data-t="acv"></th><th></th></tr></tfoot>
    </table>
  </div>
</form>
<section class="prose mt-2">
  <h2>ACV vs. RCV in plain English</h2>
  <p><strong>Replacement cost value (RCV)</strong> is what it costs today to replace the item new. <strong>Actual cash value (ACV)</strong> is RCV minus depreciation. On a replacement cost policy, the insurer usually pays ACV first and releases the withheld (“recoverable”) depreciation after you replace or repair. On an ACV policy—including many Texas roof schedules for older roofs—depreciation is generally not recoverable.</p>
  <p>Excessive depreciation is one of the most common reasons claims are underpaid. If the numbers look aggressive, a <a href="/">Sugar Land public adjuster</a> can challenge the age, condition and life-expectancy assumptions. Also see the <a href="/tools/insurance-claim-settlement-calculator/">settlement calculator</a>.</p>
</section>
<?php tool_end($faqs); ?>
