<?php defined('CPA') or exit;
/* Insolvency worksheet example (Publication 4681 method): values immediately before the cancellation. */
$liab = ['Credit card balances (including the cancelled card)' => 28000, 'Car loan' => 14000, 'Medical bills' => 4000, 'Personal loan' => 6000];
$assets = ['Checking and savings' => 2500, 'Car (fair market value)' => 12000, '401(k) balance' => 18000, 'Household goods, furniture, clothing' => 3000];
$L = array_sum($liab); $A = array_sum($assets);
$insolv = max(0, $L - $A);
$cancel = 20000;
$excluded = min($cancel, $insolv);
$taxable = $cancel - $excluded;
$tax22 = $taxable * 0.22;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">Form 1099-C, <em>Cancellation of Debt</em>, is what a lender sends when it forgives, settles or writes off $600 or more of what you owe. The IRS gets a copy too, because cancelled debt is generally taxable income. "Generally" is the key word: bankruptcy, insolvency and several other exclusions can make some or all of it tax-free, as long as you claim them correctly on Form 982. This guide explains every box on the 1099-C, when forgiven debt is taxable, how to run the insolvency worksheet, and what to do if the form is wrong.</p>

<div class="callout"><?= icon('spark') ?><p><strong>The short version:</strong> do not ignore a 1099-C, and do not assume it is all taxable either. Check the amount, then work through the exclusions below. If none apply, report the taxable amount as other income; if one does, file Form 982 with your return. You can see how much extra tax a taxable amount would add with the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>.</p></div>

<h2 id="why-taxable">Why cancelled debt counts as income</h2>
<p>When you borrowed the money, it was not income because you had to pay it back. If the lender later releases you from that obligation, you keep the benefit of money you will never repay, and the tax code treats that as income (often called "cancellation of debt" or COD income). Common sources include settled credit card balances, charged-off accounts, repossessions and foreclosures with a remaining balance, and forgiven personal or business loans.</p>
<p>The lender must file a 1099-C when it cancels $600 or more of principal. If less is cancelled, you may not get a form, but the income rules still apply.</p>

<h2 id="boxes">Form 1099-C box by box</h2>
<div class="table-wrap"><table>
<caption class="sr-only">Form 1099-C boxes</caption>
<thead><tr><th>Box</th><th>What it shows</th><th>What to check</th></tr></thead>
<tbody>
<tr><td><b>1</b></td><td>Date of identifiable event</td><td>Determines the tax year the income belongs to.</td></tr>
<tr><td><b>2</b></td><td>Amount of debt discharged</td><td>The figure the IRS will expect to see; compare it with your settlement letter.</td></tr>
<tr><td><b>3</b></td><td>Interest, if included in Box 2</td><td>Interest that would have been deductible if paid (for example, business or mortgage interest) is not income.</td></tr>
<tr><td><b>4</b></td><td>Debt description</td><td>Identifies the account; also helps you tell whether it was business or personal debt.</td></tr>
<tr><td><b>5</b></td><td>Checked if you were personally liable</td><td>If unchecked, the debt may be nonrecourse, which is treated differently (see foreclosures below).</td></tr>
<tr><td><b>6</b></td><td>Identifiable event code</td><td>A = bankruptcy, B = other judicial debt relief, C = statute of limitations or expiration of deficiency period, D = foreclosure election, E = probate or similar proceeding, F = by agreement, G = decision or policy to stop collection, H = other actual discharge.</td></tr>
<tr><td><b>7</b></td><td>Fair market value of property</td><td>Filled in for foreclosures and repossessions; used to figure gain or loss on the property.</td></tr>
</tbody></table></div>
<p>A code A in Box 6 is a strong hint that the bankruptcy exclusion applies. Codes C and G mean the lender stopped trying to collect; it is still reported as cancelled debt, so look carefully at whether you were insolvent at the time.</p>

<h2 id="not-income">When a 1099-C is not taxable income</h2>
<p>Before you get to the formal exclusions, some cancelled amounts are not income at all:</p>
<ul>
<li><strong>Gifts</strong>, such as a relative forgiving a personal loan out of generosity.</li>
<li><strong>Purchase price reductions</strong> by the seller of property you bought on credit (reduce your basis instead).</li>
<li><strong>Deductible debts:</strong> amounts that would have been deductible if you had paid them, such as a cash-basis business's unpaid expenses.</li>
<li><strong>Nonrecourse debt in a foreclosure.</strong> When property secured by nonrecourse debt is foreclosed, the whole debt is treated as the sale price of the property, so there is no separate cancellation of debt income (there may be a capital gain or loss instead).</li>
<li><strong>Certain student loan discharges</strong>, covered below.</li>
</ul>

<h2 id="exclusions">1099-C exclusions under Section 108</h2>
<p>If the cancelled debt is income, one of these exclusions may still keep it off your tax bill. Priority rules decide which one applies when several could: the bankruptcy exclusion overrides the others, insolvency takes priority over the farm and real property business exclusions, and the principal residence exclusion applies before insolvency unless you elect otherwise.</p>
<div class="table-wrap"><table>
<caption class="sr-only">Cancellation of debt exclusions</caption>
<thead><tr><th>Exclusion</th><th>Who it helps</th><th>Form 982 box</th></tr></thead>
<tbody>
<tr><td><b>Bankruptcy</b></td><td>Debt discharged in a Title 11 bankruptcy case. The entire discharge is excluded.</td><td>1a</td></tr>
<tr><td><b>Insolvency</b></td><td>Your total liabilities exceeded the fair market value of your total assets immediately before the cancellation. Excluded only up to the amount of insolvency.</td><td>1b</td></tr>
<tr><td><b>Qualified farm indebtedness</b></td><td>Debt incurred in a farming business, cancelled by a qualified lender, where most of your gross receipts came from farming.</td><td>1c</td></tr>
<tr><td><b>Qualified real property business indebtedness</b></td><td>Debt secured by business real property (not available to C corporations), limited by the property's value and basis.</td><td>1d</td></tr>
<tr><td><b>Qualified principal residence indebtedness</b></td><td>Mortgage debt used to buy, build or improve your main home, up to $750,000 ($375,000 married filing separately), for discharges before January 1, 2026 (or under a written arrangement entered into before then).</td><td>1e</td></tr>
</tbody></table></div>

<div class="callout warn"><?= icon('shield') ?><p><strong>The mortgage forgiveness exclusion has expired for new discharges.</strong> Under current law, the qualified principal residence indebtedness exclusion covers discharges before January 1, 2026, or those under a written agreement entered into before that date. Congress has extended this provision several times in the past, sometimes retroactively, so check for new legislation before filing for a 2026 discharge. Without it, homeowners may still qualify under the insolvency or bankruptcy exclusions.</p></div>

<h2 id="insolvency">The insolvency exclusion: worksheet and example</h2>
<p>Insolvency is the exclusion most people with a 1099-C for consumer debt end up using. You are insolvent to the extent your liabilities exceed the fair market value of your assets, measured <strong>immediately before</strong> the debt was cancelled. IRS Publication 4681 includes a worksheet. The important detail is what counts as an asset: <em>everything</em>, including retirement accounts, pension interests and household goods, even if they are protected from creditors.</p>
<p>Here is an example for someone who settled a credit card with <?= money($cancel) ?> forgiven:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Insolvency worksheet example</caption>
<thead><tr><th>Liabilities immediately before cancellation</th><th class="n">Amount</th></tr></thead>
<tbody>
<?php foreach ($liab as $k => $v): ?><tr><td><?= e($k) ?></td><td class="n"><?= money($v) ?></td></tr><?php endforeach; ?>
<tr class="total"><td><b>Total liabilities</b></td><td class="n"><b><?= money($L) ?></b></td></tr>
</tbody></table></div>
<div class="table-wrap"><table>
<caption class="sr-only">Insolvency worksheet assets</caption>
<thead><tr><th>Assets (fair market value)</th><th class="n">Amount</th></tr></thead>
<tbody>
<?php foreach ($assets as $k => $v): ?><tr><td><?= e($k) ?></td><td class="n"><?= money($v) ?></td></tr><?php endforeach; ?>
<tr class="total"><td><b>Total assets</b></td><td class="n"><b><?= money($A) ?></b></td></tr>
</tbody></table></div>
<div class="formula">Insolvency = <?= money($L) ?> liabilities − <?= money($A) ?> assets = <?= money($insolv) ?><br>Excluded = lesser of <?= money($cancel) ?> cancelled or <?= money($insolv) ?> insolvency = <?= money($excluded) ?><br>Taxable cancellation of debt income = <?= money($cancel) ?> − <?= money($excluded) ?> = <?= money($taxable) ?></div>
<p>In this example, <?= money($excluded) ?> is excluded by checking box 1b on Form 982 and entering that amount on line 2. The remaining <?= money($taxable) ?> is reported as income. At a 22% marginal rate, that adds about <?= money($tax22) ?> of federal income tax, far less than the <?= money($cancel * 0.22) ?> it would have cost with no exclusion. Note that the liabilities include the full balance of the cancelled card before the settlement. Keep the worksheet and supporting statements with your tax records, since the IRS can ask you to prove insolvency.</p>

<h2 id="student-loans">Student loan forgiveness and the 1099-C</h2>
<p>Student loan discharges have their own rules, and they changed at the start of <?= TAX_YEAR ?>:</p>
<ul>
<li><strong>2021 through 2025 discharges:</strong> the American Rescue Plan Act excluded most student loan forgiveness from federal income for discharges after December 31, 2020 and before January 1, 2026, including income-driven repayment forgiveness.</li>
<li><strong>Death and disability discharges:</strong> the One Big Beautiful Bill Act (OBBBA) made the exclusion for loans discharged because of the student's death or total and permanent disability permanent for discharges after 2025, with a requirement to include the student's Social Security number on the return.</li>
<li><strong>Public Service Loan Forgiveness</strong> and certain other profession-based forgiveness programs are excluded under a separate, long-standing provision.</li>
<li><strong>Other discharges after 2025</strong>, such as forgiveness at the end of an income-driven repayment plan, may be taxable federally unless Congress acts or another exclusion such as insolvency applies. Some states follow different rules. If you are close to forgiveness, it is worth planning for the possible tax.</li>
</ul>

<h2 id="report">How to report a 1099-C on your return</h2>
<ol>
<li><strong>Taxable personal debt:</strong> report the taxable amount on <strong>Schedule 1 (Form 1040)</strong>, on the line for cancellation of debt in the "other income" section.</li>
<li><strong>Business debt:</strong> report it on the schedule for that activity: Schedule C for a sole proprietorship, Schedule F for a farm or Schedule E for rental property. See our <a href="/blog/schedule-c-tax-form/">Schedule C guide</a>.</li>
<li><strong>Excluded debt:</strong> attach <strong>Form 982</strong>, <em>Reduction of Tax Attributes Due to Discharge of Indebtedness</em>, check the box for your exclusion and enter the excluded amount. Do not include the excluded amount in income.</li>
<li><strong>Foreclosures and repossessions:</strong> you may also have a sale to report on Form 8949 and Schedule D (or Form 4797 for business property), using the fair market value in Box 7 and possibly a Form 1099-A.</li>
</ol>

<h3 id="attributes">Attribute reduction: the price of an exclusion</h3>
<p>Excluded debt is not entirely free. In exchange, Part II of Form 982 requires you to reduce certain "tax attributes" by the excluded amount, in this order: net operating losses, general business credit carryovers, minimum tax credit, capital loss carryovers, basis of your property, passive activity loss and credit carryovers, and foreign tax credit carryovers. You can elect to reduce the basis of depreciable property first. The qualified principal residence exclusion instead reduces the basis of your home. For many individuals with consumer debt, the only attribute they have is property basis, and the practical effect is small.</p>

<h2 id="wrong-1099-c">What to do if your 1099-C is wrong</h2>
<ul>
<li><strong>Wrong amount or date:</strong> contact the lender with your settlement letter or payment records and ask for a corrected 1099-C. If it is not fixed in time, report the correct amount and attach a short explanation, and keep your documents.</li>
<li><strong>You paid the debt or never owed it:</strong> ask the lender to correct or withdraw the form. If it may be identity theft, report it at IdentityTheft.gov and to the lender.</li>
<li><strong>Debt already discharged in bankruptcy in an earlier year:</strong> the income, if any, belonged to the year of the discharge, and bankruptcy discharges are excluded. Keep your discharge order and explain the discrepancy if the IRS asks.</li>
<li><strong>The lender is still trying to collect after sending a 1099-C:</strong> filing the form is an information report and does not, by itself, necessarily cancel the debt under state law. Ask the lender in writing to confirm the status, and get advice if you face collection on a debt reported as cancelled.</li>
</ul>
<p>If you already filed without reporting a 1099-C, file an <a href="/blog/amended-tax-return/">amended tax return</a> rather than waiting for an IRS notice. If you expect to owe tax on cancelled debt, the <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> shows whether your withholding still covers it, and the <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> can help if you need to make a payment during the year.</p>

<?= faq_block([
  ['Is a 1099-C taxable income?', '<p>Usually, yes. Cancelled debt is generally taxable income in the year it is forgiven. However, it is not taxable if it was discharged in bankruptcy, to the extent you were insolvent immediately before the cancellation, or if another exclusion applies (qualified farm debt, qualified real property business debt, certain mortgage and student loan discharges). You claim the exclusion on Form 982.</p>'],
  ['What happens if I don\'t report a 1099-C?', '<p>The IRS receives a copy of every 1099-C and matches it against your return. If the amount is missing, you will likely get a CP2000 notice proposing additional tax, plus interest and possibly a penalty. If an exclusion applies, report it on Form 982 so the IRS can see why the amount is not in income.</p>'],
  ['How do I prove insolvency for a 1099-C?', '<p>Use the insolvency worksheet in IRS Publication 4681 to list all your liabilities and the fair market value of all your assets, including retirement accounts, immediately before the debt was cancelled. Keep statements, appraisals or other records that support the numbers. The excluded amount is the smaller of the cancelled debt or the amount by which liabilities exceeded assets.</p>'],
  ['Is forgiven credit card debt taxable?', '<p>Yes, if you settle a credit card for less than you owe and the creditor forgives $600 or more, you will usually receive a 1099-C and the forgiven amount is taxable unless you were insolvent or in bankruptcy. Many people who settle credit card debt qualify for at least a partial insolvency exclusion.</p>'],
  ['Is student loan forgiveness taxable in 2026?', '<p>It depends on the type. Discharges for death or total and permanent disability are permanently excluded under the OBBBA, and Public Service Loan Forgiveness remains tax-free. The broad American Rescue Plan exclusion covered discharges through December 31, 2025, so other forgiveness in ' . TAX_YEAR . ' may be taxable federally unless Congress extends it or you qualify for insolvency. State rules vary.</p>'],
  ['What is Form 982 used for?', '<p>Form 982 tells the IRS that you are excluding cancelled debt from income under an exclusion such as bankruptcy or insolvency, and it records the reduction of tax attributes (like loss carryovers or property basis) required in exchange. Attach it to your Form 1040 for the year of the cancellation.</p>'],
]) ?>
<?= post_close($SLUG, 'federal-income-tax', ['amended-tax-return', 'schedule-c-tax-form', '1099-g']) ?>
