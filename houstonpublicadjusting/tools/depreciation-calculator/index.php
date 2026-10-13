<?php
require dirname(__DIR__, 2) . '/inc/tools.php';
tool_page([
    'slug' => 'depreciation-calculator',
    'title' => 'Insurance Depreciation Calculator: Roof, Flooring, HVAC & Contents',
    'desc' => 'Check your insurer’s depreciation with this free calculator from Houston Public Adjusters. Estimate actual cash value from cost, age and useful life.',
    'h1' => 'Insurance Depreciation Calculator',
    'lede' => 'Insurers depreciate roofs, flooring, appliances and contents for age and wear. Check whether the depreciation on your estimate is reasonable.',
    'form' => '
<form data-tool="depreciation" data-out="out-dep" class="tool-grid">
  <label>Item preset
    <select data-fill="life">
      <option value="">Choose an item (optional)</option>
      <option value="30">Architectural shingle roof (~30 yrs)</option>
      <option value="20">3-tab shingle roof (~20 yrs)</option>
      <option value="50">Metal roof (~50 yrs)</option>
      <option value="15">HVAC system (~15 yrs)</option>
      <option value="10">Water heater (~10 yrs)</option>
      <option value="10">Carpet (~10 yrs)</option>
      <option value="20">Laminate / vinyl plank (~20 yrs)</option>
      <option value="15">Wood fence (~15 yrs)</option>
      <option value="12">Major appliance (~12 yrs)</option>
      <option value="8">Television / electronics (~8 yrs)</option>
      <option value="10">Furniture (~10 yrs)</option>
    </select></label>
  <label>Replacement cost ($)<input name="cost" inputmode="decimal" value="18000"></label>
  <label>Age (years)<input name="age" inputmode="decimal" value="8"></label>
  <label>Useful life (years)<input name="life" inputmode="decimal" value="30"></label>
  <label>Maximum depreciation (%)<input name="cap" inputmode="decimal" value="80"><span class="hint">Many carriers cap depreciation; adjust to match your estimate</span></label>
</form>
<div class="tool-result" id="out-dep" aria-live="polite"></div>',
    'prose' => '
<h2>How insurers calculate depreciation</h2>
<p>Most carriers use straight-line depreciation: <em>age &divide; expected useful life &times; replacement cost</em>. An 8-year-old architectural shingle roof with a 30-year life is about 27% depreciated. The fights start over the inputs: the age the insurer assumes, the useful life it picks, whether it depreciates labor as well as materials, and whether condition is used to push the percentage higher.</p>
<h2>Common depreciation problems on Houston claims</h2>
<ul class="checklist">
  <li>Roof age taken from a guess instead of permits, invoices or the home&rsquo;s sale records</li>
  <li>Depreciation applied to labor, removal and disposal (contested in many claims)</li>
  <li>Useful life set unrealistically short for the material</li>
  <li>&ldquo;Condition&rdquo; adjustments with no photos or explanation</li>
  <li>Non-recoverable depreciation on a policy that is actually replacement cost</li>
</ul>
<p>Depreciation on a replacement-cost policy is usually recoverable after repair, but it still affects how much cash you have to start the work. Learn more in our <a href="/tools/claim-settlement-calculator/">settlement calculator</a>.</p>',
    'faqs' => [
        ['Is depreciation recoverable?', 'On a replacement-cost policy, yes — after the repair or replacement is completed, up to what you actually spend. On an actual-cash-value policy or ACV roof endorsement, depreciation is not recoverable.'],
        ['Can I dispute the insurer’s depreciation?', 'Yes. Ask for the depreciation breakdown by line item, then challenge the age, useful life or condition assumptions with evidence. A public adjuster can do this for you.'],
    ],
]);
