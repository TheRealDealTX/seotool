<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$pct = fn(float $x, int $dp = 1): string => number_format($x * 100, $dp) . '%';
/* Same $100,000 of owner income: partnership K-1 (box 1 + guaranteed payments) vs S corp (W-2 salary + K-1 box 1). */
$ord = 60000; $gp = 40000;
$p_base = ($ord + $gp) * 0.9235;
$p_se = min($p_base, $Y['ssWageBase']) * 0.124 + $p_base * 0.029;
$s_wage = $gp; $s_k1 = $ord;
$s_fica = min($s_wage, $Y['ssWageBase']) * 0.124 + $s_wage * 0.029;
/* S corp stock basis roll-forward. */
$b0 = 20000; $b_inc = $s_k1; $b_dist = 50000; $b_end = $b0 + $b_inc - $b_dist;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">A K1 tax form, officially Schedule K-1, reports your share of income, deductions and credits from a partnership, S corporation, estate or trust. The entity itself usually pays no federal income tax; instead it passes the results through to its owners or beneficiaries, who report them on their own returns. That is why a K-1 often arrives late, why it can show income you never received in cash, and why its boxes land in several different places on your Form 1040. This guide explains all three types of K-1 and the boxes that matter most for <?= TAX_YEAR ?>.</p>

<div class="callout"><?= icon('building') ?><p><strong>Quick answer:</strong> partnerships and multi-member LLCs issue K-1s from Form 1065, S corporations from Form 1120-S, and estates and trusts from Form 1041. You pay tax on your share of the income shown, whether or not it was distributed. Most K-1 business income goes on Schedule E, Part II or III, with interest, dividends and capital gains carried to their usual lines.</p></div>

<h2 id="what-is-k1">What is a K1 tax form?</h2>
<p>Pass-through entities file an information return showing the business's total income, deductions and credits, then split those items among owners on Schedule K-1. You generally do not attach the K-1 to your return; you use it to fill out your return, and the IRS receives its own copy to match against what you report.</p>
<div class="table-wrap"><table>
<thead><tr><th>K-1 type</th><th>Issued by</th><th>Recipient</th><th>Self-employment tax?</th></tr></thead>
<tbody>
<tr><td><b>Form 1065 K-1</b></td><td>Partnerships and multi-member LLCs</td><td>Partners and LLC members</td><td>Often yes, on general partners' income and guaranteed payments</td></tr>
<tr><td><b>Form 1120-S K-1</b></td><td>S corporations</td><td>Shareholders</td><td>No; owner-employees pay FICA on W-2 wages instead</td></tr>
<tr><td><b>Form 1041 K-1</b></td><td>Estates and trusts</td><td>Beneficiaries</td><td>No</td></tr>
</tbody></table></div>

<h2 id="form-1065">Partnership K-1 (Form 1065): key boxes</h2>
<div class="table-wrap"><table>
<thead><tr><th>Box</th><th>Item</th><th>Where it usually goes</th></tr></thead>
<tbody>
<tr><td>1</td><td>Ordinary business income (loss)</td><td>Schedule E, Part II</td></tr>
<tr><td>2 / 3</td><td>Net rental real estate / other rental income</td><td>Schedule E, Part II (passive rules may apply)</td></tr>
<tr><td>4a–4c</td><td>Guaranteed payments for services, for capital, and total</td><td>Schedule E, Part II</td></tr>
<tr><td>5, 6a–6c, 7</td><td>Interest, dividends (ordinary, qualified, equivalents), royalties</td><td>Form 1040 / Schedule B; royalties on Schedule E</td></tr>
<tr><td>8, 9a–9c, 10</td><td>Short-term and long-term capital gains, 28% gain, unrecaptured §1250 gain, net §1231 gain</td><td>Schedule D / Form 4797</td></tr>
<tr><td>11, 12, 13</td><td>Other income, Section 179 deduction, other deductions (coded)</td><td>Varies by code</td></tr>
<tr><td>14</td><td>Self-employment earnings (code A)</td><td>Schedule SE</td></tr>
<tr><td>15, 17, 18</td><td>Credits, AMT items, tax-exempt income and nondeductible expenses</td><td>Varies by code</td></tr>
<tr><td>19</td><td>Distributions</td><td>Reduces basis; taxable only if more than basis</td></tr>
<tr><td>20</td><td>Other information, including code Z (Section 199A / QBI information)</td><td>Form 8995 or 8995-A</td></tr>
<tr><td>21</td><td>Foreign taxes paid or accrued</td><td>Form 1116 or Schedule 3</td></tr>
</tbody></table></div>
<p>Part II of the partnership K-1 also shows whether you are a general or limited partner (item G), your share of profit, loss and capital (item J), your share of liabilities (item K) and your capital account analysis (item L). If international items exist, the partnership attaches Schedule K-3 and checks box 16.</p>

<h3 id="guaranteed-payments">Guaranteed payments and self-employment tax</h3>
<p>Partners are not employees, so they do not receive a W-2. Payments for services that do not depend on profit are <strong>guaranteed payments</strong> (box 4) and are always subject to self-employment tax. A general partner's share of ordinary income (box 1) is generally subject to SE tax too, and box 14, code A, combines these into net earnings from self-employment. Limited partners generally owe SE tax only on guaranteed payments for services, but recent Tax Court decisions look at what a partner actually does rather than the label, so active owners of LLCs and limited partnerships should not assume the exception applies. Guaranteed payments are also not qualified business income.</p>

<h2 id="form-1120s">S corporation K-1 (Form 1120-S): key boxes</h2>
<div class="table-wrap"><table>
<thead><tr><th>Box</th><th>Item</th></tr></thead>
<tbody>
<tr><td>1</td><td>Ordinary business income (loss), reported on Schedule E, Part II</td></tr>
<tr><td>2 / 3</td><td>Net rental real estate / other rental income</td></tr>
<tr><td>4, 5a–5b, 6</td><td>Interest, ordinary and qualified dividends, royalties</td></tr>
<tr><td>7, 8a–8c, 9</td><td>Capital gains, collectibles gain, unrecaptured §1250 gain, net §1231 gain</td></tr>
<tr><td>10, 11, 12</td><td>Other income, Section 179 deduction, other deductions</td></tr>
<tr><td>13</td><td>Credits</td></tr>
<tr><td>15</td><td>AMT items</td></tr>
<tr><td>16</td><td>Items affecting shareholder basis, including code D (distributions)</td></tr>
<tr><td>17</td><td>Other information, including code V (Section 199A / QBI information)</td></tr>
</tbody></table></div>
<p>S corporation K-1 income is <strong>not</strong> subject to self-employment tax. Owners who work in the business must instead pay themselves reasonable compensation on a W-2, which carries FICA. That split is the main tax appeal of an S corporation. Here is the same <?= money($ord + $gp) ?> of owner income structured both ways for <?= TAX_YEAR ?>:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Partnership vs S corporation self-employment and payroll tax, <?= TAX_YEAR ?></caption>
<thead><tr><th></th><th class="n">Partnership / LLC</th><th class="n">S corporation</th></tr></thead>
<tbody>
<tr><td>Guaranteed payment / W-2 salary</td><td class="n"><?= money($gp) ?></td><td class="n"><?= money($s_wage) ?></td></tr>
<tr><td>K-1 box 1 ordinary income</td><td class="n"><?= money($ord) ?></td><td class="n"><?= money($s_k1) ?></td></tr>
<tr><td>Income subject to SE tax or FICA</td><td class="n"><?= money($p_base) ?> (92.35% of <?= money($ord + $gp) ?>)</td><td class="n"><?= money($s_wage) ?></td></tr>
<tr><td><b>SE tax / total FICA (both halves)</b></td><td class="n"><b><?= money($p_se) ?></b></td><td class="n"><b><?= money($s_fica) ?></b></td></tr>
</tbody></table></div>
<p>The S corporation structure saves about <?= money($p_se - $s_fica) ?> in payroll-type taxes here, before the costs of running payroll, a separate corporate return and state fees, and assuming <?= money($s_wage) ?> is a defensible reasonable salary for the work performed. The <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a> runs this comparison with your numbers, and our guide to <a href="/blog/irs-form-2553/">IRS Form 2553</a> explains how to make the election. Partners can check their SE tax with the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a>.</p>

<h2 id="form-1041">Estate and trust K-1 (Form 1041)</h2>
<p>Estates and trusts are taxed on income they keep and pass income they distribute to beneficiaries, up to distributable net income (DNI). The beneficiary's K-1 shows interest (box 1), ordinary and qualified dividends (2a–2b), short-term and long-term capital gains (3, 4a–4c), other portfolio income (5), business and rental income (6–8), directly apportioned deductions (9), the estate tax deduction (10), final-year deductions (11), AMT items (12), credits (13) and other information, including Section 199A details (14). Final-year deductions can include excess deductions and unused capital loss carryovers when the estate or trust terminates. Inheritances themselves are not income; only the income the estate or trust earned and distributed shows up on the K-1.</p>

<h2 id="basis">Basis: why your K-1 income is not the same as cash</h2>
<p>You are taxed on your share of income whether or not the entity distributed it. Your <strong>basis</strong> tracks the after-tax money you have in the entity, so income you already paid tax on is not taxed again when you take it out.</p>
<ul>
<li><strong>Increases:</strong> contributions, your share of income (including tax-exempt income) and, for partners, your share of partnership liabilities.</li>
<li><strong>Decreases:</strong> distributions, your share of losses and deductions, and nondeductible expenses.</li>
<li><strong>Distributions above basis</strong> are generally taxed as capital gain.</li>
<li><strong>Losses</strong> are deductible only to the extent of basis, then the at-risk rules, then the passive activity rules, then the excess business loss limit.</li>
</ul>
<p>S corporation shareholders get basis for stock and for loans they personally made to the company, but not for the company's bank debt. Shareholders must attach Form 7203 when they claim a loss, receive a distribution, dispose of stock or receive a loan repayment. A simple stock basis roll-forward:</p>
<div class="table-wrap"><table>
<caption class="sr-only">S corporation stock basis example</caption>
<tbody>
<tr><td>Beginning stock basis</td><td class="n"><?= money($b0) ?></td></tr>
<tr><td>Plus K-1 box 1 income</td><td class="n">+<?= money($b_inc) ?></td></tr>
<tr><td>Less distributions (box 16, code D)</td><td class="n">−<?= money($b_dist) ?></td></tr>
<tr><td><b>Ending stock basis</b></td><td class="n"><b><?= money($b_end) ?></b></td></tr>
</tbody></table></div>
<p>The <?= money($b_dist) ?> distribution is tax-free because the shareholder already reported <?= money($b_inc) ?> of income and had enough basis to cover it.</p>

<h2 id="qbi">K-1s and the QBI deduction</h2>
<p>Most pass-through business income qualifies for the 20% qualified business income deduction, which the One Big Beautiful Bill Act made permanent. The entity reports what you need in box 20, code Z (Form 1065) or box 17, code V (Form 1120-S): your share of QBI, W-2 wages, the unadjusted basis of qualified property and whether the business is a specified service trade or business. For <?= TAX_YEAR ?>, the wage and service-business limits begin above taxable income of <?= money($Y['qbiThreshold']['single']) ?> (<?= money($Y['qbiThreshold']['mfj']) ?> married filing jointly), phasing in over a range that OBBBA widened to <?= money(75000) ?> (<?= money(150000) ?> joint). Guaranteed payments and S corporation wages are not QBI. You claim the deduction on Form 8995 or 8995-A.</p>

<h2 id="timing">When does the K1 tax form arrive?</h2>
<div class="table-wrap"><table>
<thead><tr><th>Entity return</th><th>Due date (calendar year)</th><th>Extended due date</th></tr></thead>
<tbody>
<tr><td>Form 1065 (partnership)</td><td>March 15</td><td>September 15</td></tr>
<tr><td>Form 1120-S (S corporation)</td><td>March 15</td><td>September 15</td></tr>
<tr><td>Form 1041 (estate or trust)</td><td>April 15</td><td>September 30</td></tr>
</tbody></table></div>
<p>The entity must furnish K-1s by its return due date, including extensions, so a K-1 from an extended partnership can arrive in September, well after the April 15 individual deadline. If you are waiting on one, file Form 4868 to extend your own return to October 15, and pay an estimate of the tax by April 15 to limit interest and penalties. K-1 income also has no withholding, so owners with significant pass-through income usually make <a href="/blog/quarterly-taxes-101-guide/">quarterly estimated payments</a>; the <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> helps size them. If a corrected K-1 arrives after you file, you may need an <a href="/blog/amended-tax-return/">amended tax return</a>.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>Do not ignore a K-1 because no cash came with it.</strong> The IRS receives a copy, and unreported K-1 income can trigger a matching notice. If the numbers look wrong, contact the entity for a corrected K-1 rather than reporting different amounts.</p></div>

<h2 id="state">State K-1s and pass-through entity taxes</h2>
<p>Many states require their own K-1 equivalent (California, for example, issues Schedule K-1 (568) for LLCs and K-1 (100S) for S corporations), and the state amounts can differ from federal ones because of state adjustments. If the business operates in a state where you do not live, you may have to file a nonresident return there, although the entity may withhold tax or file a composite return on your behalf. Many states also let pass-through entities elect to pay state income tax at the entity level (a PTET election), which can give owners a federal deduction outside the SALT cap of <?= money($Y['saltCap']) ?>. Your share of that entity-level tax, and any credit you can claim for it, appears on the state K-1.</p>
<p>For sole proprietors, the equivalent of all this is Schedule C; see our <a href="/blog/schedule-c-tax-form/">Schedule C tax form guide</a>. If you sell an interest in the entity, the <a href="/calculators/capital-gains-tax/">capital gains tax calculator</a> estimates the tax on the gain.</p>

<?= faq_block([
  ['What is a K1 tax form used for?', '<p>A K1 tax form (Schedule K-1) reports each owner\'s or beneficiary\'s share of income, deductions and credits from a partnership, S corporation, estate or trust. You use it to complete your own return; the entity sends a copy to the IRS.</p>'],
  ['Do I have to pay taxes on a K-1?', '<p>Yes, you generally owe tax on the income shown, even if you received no cash distribution. Losses may be deductible, subject to basis, at-risk, passive activity and excess business loss limits. Distributions themselves are usually not taxed unless they exceed your basis.</p>'],
  ['Is K-1 income subject to self-employment tax?', '<p>Partnership guaranteed payments are, and general partners usually owe SE tax on their share of ordinary income (box 14). S corporation K-1 income is not subject to SE tax; owner-employees pay FICA on W-2 wages instead. Trust and estate K-1 income is not subject to SE tax.</p>'],
  ['When should I receive my K-1?', '<p>Partnership and S corporation K-1s are due by March 15 for calendar-year entities, or September 15 if the entity extends. Estate and trust K-1s are due by April 15, or September 30 with an extension. If yours is late, extend your own return with Form 4868.</p>'],
  ['What is the difference between a K-1 and a 1099?', '<p>A 1099 reports payments made to you. A K-1 reports your ownership share of an entity\'s results, including income that may not have been paid out. K-1 items can also carry special character, such as capital gains, rental income and QBI information, that a 1099-NEC does not.</p>'],
  ['Can I file my taxes without my K-1?', '<p>You should not file using guesses if the K-1 is expected soon. File an extension, pay an estimate by April 15, and complete your return once the K-1 arrives. If you file and the K-1 later differs, you may need to amend.</p>'],
]) ?>
<?= post_close($SLUG, 's-corp-tax-savings', ['irs-form-2553', 'schedule-c-tax-form', 'quarterly-taxes-101-guide']) ?>
