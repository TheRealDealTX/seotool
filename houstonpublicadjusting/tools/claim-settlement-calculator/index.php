<?php
require dirname(__DIR__, 2) . '/inc/tools.php';
tool_page([
    'slug' => 'claim-settlement-calculator',
    'title' => 'Insurance Claim Settlement Calculator (RCV, ACV & Depreciation)',
    'desc' => 'Free insurance claim settlement calculator from Houston Public Adjusters. Estimate your ACV check, recoverable depreciation and total payout after your deductible.',
    'h1' => 'Insurance Claim Settlement Calculator',
    'lede' => 'See how replacement cost, depreciation, your deductible and prior payments add up to the checks you should receive &mdash; and spot when the numbers don&rsquo;t add up.',
    'form' => '
<form data-tool="settlement" data-out="out-settlement" class="tool-grid">
  <label>Replacement cost value (RCV)<input name="rcv" inputmode="decimal" value="42000"><span class="hint">Total from the estimate, before depreciation</span></label>
  <label>Depreciation (%)<input name="dep_pct" inputmode="decimal" value="25"><span class="hint">Depreciation &divide; RCV on the carrier estimate</span></label>
  <label>Deductible ($)<input name="deductible" inputmode="decimal" value="4200"><span class="hint">For a % deductible use the hurricane deductible tool</span></label>
  <label>Payments already received ($)<input name="prior" inputmode="decimal" value="0"></label>
  <label>Policy type<select name="policy"><option value="rcv">Replacement cost (RCV)</option><option value="acv">Actual cash value (ACV)</option></select><span class="hint">Most Texas HO-3 / HO-B dwelling coverage is RCV; many older roofs are ACV</span></label>
</form>
<div class="tool-result" id="out-settlement" aria-live="polite"></div>',
    'prose' => '
<h2>How an insurance claim settlement is calculated</h2>
<p>Most Houston homeowners policies pay a property claim in two stages. First the insurer pays the <strong>actual cash value (ACV)</strong>: the replacement cost of the damaged items minus depreciation and minus your deductible. Once repairs are completed and invoiced, a replacement-cost policy releases the <strong>recoverable depreciation</strong> it withheld.</p>
<p>The formula is simple: <em>RCV &minus; depreciation &minus; deductible = first check</em>, and <em>RCV &minus; deductible = total</em> on a replacement-cost policy. What is not simple is the RCV itself. The carrier&rsquo;s estimate sets the ceiling on everything that follows, and that is where most underpaid claims start: missing line items, wrong quantities, low unit pricing, no overhead and profit, or no code-upgrade items.</p>
<h2>Where Houston public adjusters find missing money</h2>
<ul class="checklist">
  <li>Roof systems scoped for repair when the damage supports full replacement</li>
  <li>Missing drip edge, starter course, ice-and-water shield, ridge vent and code-required items</li>
  <li>Interior water damage scoped as &ldquo;paint only&rdquo; with no drywall, insulation or cabinetry</li>
  <li>Excessive depreciation on labor or on items with plenty of life left</li>
  <li>General contractor overhead and profit left off a multi-trade job</li>
  <li>Contents, additional living expenses and debris removal never claimed</li>
</ul>
<p>If the carrier&rsquo;s RCV looks low next to your contractor&rsquo;s bid, the gap is worth a second look. Houston Public Adjusters build an independent Xactimate estimate so the comparison is line by line.</p>',
    'faqs' => [
        ['What is the difference between RCV and ACV?', 'Replacement cost value (RCV) is what it costs to repair or replace the damaged property with new materials of like kind and quality. Actual cash value (ACV) is RCV minus depreciation for age and wear. A replacement-cost policy pays ACV first, then the withheld depreciation once you repair.'],
        ['How do I get my recoverable depreciation?', 'Complete the repairs, then send the insurer the final invoice and proof of payment within the time the policy allows (often 180 days to two years, depending on the policy). The insurer releases the depreciation up to the amount actually spent.'],
        ['Is the deductible subtracted from the first check or the total?', 'From the claim as a whole. In practice it is subtracted from the first ACV payment, which is why the first check can look much smaller than the estimate.'],
    ],
]);
