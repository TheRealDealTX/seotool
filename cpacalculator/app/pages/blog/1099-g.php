<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">Form 1099-G, <em>Certain Government Payments</em>, is sent by federal, state and local government agencies to report money they paid you. For most people, a 1099-G reports one of two things: <strong>unemployment benefits</strong>, which are taxable on your federal return, or a <strong>state or local income tax refund</strong>, which is taxable only in some situations. This guide explains each box on the 1099-G, when the amounts are taxable, how the tax benefit rule works for state refunds, and where each number goes on your return.</p>

<div class="callout"><?= icon('refund') ?><p><strong>Collected unemployment this year?</strong> If no tax was withheld from your benefits, you may owe at filing time. Plug the benefits into the <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> as other income to see whether you will get a refund or have a balance due.</p></div>

<h2 id="what-is-1099-g">What Form 1099-G reports</h2>
<p>A government agency must send a 1099-G when it pays you at least $10 in unemployment compensation or state or local tax refunds, credits or offsets, and for certain other payments such as taxable grants and agricultural payments. The form is due to you by January 31 for payments made the previous calendar year. Many states no longer mail it automatically; instead, you download it from your state's unemployment or revenue department website. The IRS receives a copy, so the amounts should match what you report.</p>

<h2 id="boxes">Form 1099-G box by box</h2>
<div class="table-wrap"><table>
<caption class="sr-only">Form 1099-G boxes and where they go</caption>
<thead><tr><th>Box</th><th>What it reports</th><th>Taxable?</th><th>Where it goes</th></tr></thead>
<tbody>
<tr><td><b>1</b></td><td>Unemployment compensation</td><td>Yes, federally</td><td>Schedule 1, unemployment compensation line</td></tr>
<tr><td><b>2</b></td><td>State or local income tax refunds, credits or offsets</td><td>Only if you itemized and got a tax benefit</td><td>Schedule 1, taxable refunds line</td></tr>
<tr><td><b>3</b></td><td>The tax year the Box 2 refund relates to</td><td>Informational</td><td>Used to apply the tax benefit rule</td></tr>
<tr><td><b>4</b></td><td>Federal income tax withheld</td><td>Credit against your tax</td><td>Form 1040, federal tax withheld from other forms</td></tr>
<tr><td><b>5</b></td><td>RTAA payments (Reemployment Trade Adjustment Assistance)</td><td>Yes</td><td>Schedule 1, other income</td></tr>
<tr><td><b>6</b></td><td>Taxable grants</td><td>Yes</td><td>Schedule 1 other income, or your business schedule if business-related</td></tr>
<tr><td><b>7</b></td><td>Agriculture payments</td><td>Yes</td><td>Schedule F (or Form 4835)</td></tr>
<tr><td><b>8</b></td><td>Checkbox: Box 2 is trade or business income</td><td>Informational</td><td>Report the Box 2 amount on the business schedule</td></tr>
<tr><td><b>9</b></td><td>Market gain on Commodity Credit Corporation loans</td><td>Yes</td><td>Schedule F</td></tr>
<tr><td><b>10a–11</b></td><td>State, state ID and state income tax withheld</td><td>Informational</td><td>Your state return</td></tr>
</tbody></table></div>

<h2 id="unemployment">Box 1: Is unemployment taxable on a 1099-G?</h2>
<p>Yes. Unemployment compensation is fully taxable on your federal return, the same as wages for income tax purposes. (The partial exclusion that applied to 2020 benefits was a one-time pandemic measure and has not been renewed.) It is not subject to Social Security or Medicare tax, and it is not earned income for the earned income tax credit.</p>
<p>Report the Box 1 amount on <strong>Schedule 1 (Form 1040)</strong> on the line for unemployment compensation; it then flows into your adjusted gross income. If you repaid some benefits in the same year you received them, subtract the repayment and write the details as the instructions direct. Repayments of benefits from an earlier year follow different rules, so check the Schedule 1 instructions.</p>
<p>State treatment varies. Most states with an income tax also tax unemployment, but several exempt it fully or partly. Check your state return instructions.</p>

<h3 id="withholding">Box 4: Withholding on unemployment</h3>
<p>Unemployment benefits do not have federal tax withheld unless you ask. You can request a flat 10% federal withholding by giving the paying agency <strong>Form W-4V</strong> (many states let you choose this in the online claim). Whatever was withheld appears in Box 4, and you claim it on Form 1040 with your other withholding.</p>
<p>If you did not have tax withheld, consider making an estimated payment, especially if you received benefits for several months. The 10% withholding is often below your actual rate once benefits are added to other income for the year. The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> shows what to pay, and our guide to <a href="/blog/quarterly-taxes-101-guide/">quarterly taxes</a> covers the due dates.</p>

<h2 id="state-refunds">Box 2: Are state tax refunds on a 1099-G taxable?</h2>
<p>Often not. A state or local income tax refund is taxable on your federal return <strong>only if you deducted that state income tax as an itemized deduction in the year you paid it, and the deduction actually reduced your federal tax</strong>. This is called the <strong>tax benefit rule</strong>: you only owe tax on getting back money that previously gave you a tax break.</p>
<ul>
<li><strong>You took the standard deduction</strong> in the year the refund relates to: the refund is <strong>not taxable</strong>. You can ignore Box 2 on your federal return.</li>
<li><strong>You itemized and deducted state and local sales tax instead of income tax:</strong> a state income tax refund is generally not taxable.</li>
<li><strong>You itemized and deducted state income tax:</strong> the refund may be partly or fully taxable, depending on how much the deduction helped.</li>
</ul>
<p>The Schedule 1 instructions include a State and Local Income Tax Refund Worksheet that works through the details. Tax software runs it automatically if you enter the prior year's figures.</p>

<h3 id="examples">Simple examples of the tax benefit rule</h3>
<p>Each example is a single filer who received a state tax refund in <?= TAX_YEAR ?> for their <?= TAX_YEAR - 1 ?> state taxes. For <?= TAX_YEAR - 1 ?>, the single standard deduction was $15,750 and the SALT cap was $40,000.</p>
<div class="table-wrap"><table>
<caption class="sr-only">Tax benefit rule examples for state refunds</caption>
<thead><tr><th>Situation on the <?= TAX_YEAR - 1 ?> return</th><th class="n">Refund (Box 2)</th><th class="n">Taxable</th><th>Why</th></tr></thead>
<tbody>
<tr><td>Took the $15,750 standard deduction</td><td class="n">$900</td><td class="n">$0</td><td>No state tax was deducted, so there was no benefit.</td></tr>
<tr><td>Itemized $22,000, including $7,000 of state income tax</td><td class="n">$900</td><td class="n">$900</td><td>Itemized deductions beat the standard deduction by $6,250, more than the refund.</td></tr>
<tr><td>Itemized $16,150, including $7,000 of state income tax</td><td class="n">$900</td><td class="n">$400</td><td>Itemizing beat the standard deduction by only $400, so only $400 of the refund was a benefit.</td></tr>
<tr><td>Paid $32,000 state income tax and $12,000 property tax, deduction limited to the $40,000 cap</td><td class="n">$3,000</td><td class="n">$0</td><td>Even after the refund, taxes paid were $41,000, still above the cap, so the deduction would have been the same.</td></tr>
</tbody></table></div>
<p>That last case matters more now that the SALT cap has risen under the One Big Beautiful Bill Act (it is <?= money($Y['saltCap']) ?> for <?= TAX_YEAR ?>, reduced for higher incomes). People whose state and local taxes were above the cap often owe nothing on a state refund. If any part of the refund is taxable, report it on <strong>Schedule 1</strong> on the line for taxable refunds, credits or offsets of state and local income taxes.</p>

<div class="callout warn"><?= icon('shield') ?><p><strong>Offsets count too.</strong> If your state refund was applied to next year's estimated tax, or taken to pay a debt such as past-due child support, it still counts as a refund you received, and Box 2 will include it. The same tax benefit rule applies.</p></div>

<h2 id="other-boxes">Other 1099-G boxes</h2>
<ul>
<li><strong>Box 5, RTAA payments:</strong> wage supplements under the Reemployment Trade Adjustment Assistance program for older workers who took lower-paying jobs. They are taxable and generally reported as other income on Schedule 1.</li>
<li><strong>Box 6, taxable grants:</strong> certain government grants. Report grants received for a business on that business's schedule (for example, <a href="/blog/schedule-c-tax-form/">Schedule C</a>); report other taxable grants as other income. Some disaster-relief and similar payments are excluded and are not reported in this box.</li>
<li><strong>Box 7, agriculture payments:</strong> USDA and other government farm program payments, reported on Schedule F.</li>
<li><strong>Box 9, market gain:</strong> gain on repaying Commodity Credit Corporation loans at a lower rate, also for farmers.</li>
</ul>

<h2 id="fraud">A 1099-G for unemployment you never received</h2>
<p>Unemployment identity theft is common: someone files a claim using your name and Social Security number, and you find out when a 1099-G arrives for benefits you never got. Do not report the fraudulent income. Instead:</p>
<ol>
<li><strong>Report the fraud to the state agency</strong> that issued the form, using its identity-theft or fraud reporting process, and ask for a corrected 1099-G showing $0.</li>
<li><strong>File your return accurately,</strong> reporting only income you actually received. The IRS says you should not delay filing while waiting for the corrected form.</li>
<li><strong>Protect your identity:</strong> review your credit reports, consider a credit freeze, and report the theft at IdentityTheft.gov. If you suspect someone has also used your Social Security number to file a tax return, the IRS has a separate identity theft affidavit, Form 14039.</li>
</ol>
<p>If you were laid off and received benefits but the amount on the form is wrong, contact the state agency for a correction as well. If you discover an error after filing, file an <a href="/blog/amended-tax-return/">amended tax return</a> once you have the corrected figures.</p>

<h2 id="how-to-report">How to report a 1099-G: quick checklist</h2>
<ol>
<li><strong>Box 1:</strong> enter on Schedule 1 as unemployment compensation.</li>
<li><strong>Box 2:</strong> check the prior year's return. Standard deduction, or sales tax deducted instead of income tax? Not taxable. Itemized state income tax? Run the refund worksheet and enter any taxable part on Schedule 1.</li>
<li><strong>Box 4:</strong> include with your federal withholding on Form 1040.</li>
<li><strong>Boxes 5–9:</strong> report on Schedule 1 other income, or on Schedule C or F if they relate to a business or farm.</li>
<li><strong>State boxes:</strong> use on your state return, which may treat unemployment and refunds differently.</li>
</ol>
<p>To see how unemployment changes your overall tax, add it to your wages in the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>. If you are back at work, the <a href="/calculators/paycheck-calculator/">paycheck calculator</a> helps you adjust W-4 withholding to cover the tax on benefits you already received. For wage income, our guide to <a href="/blog/understanding-your-w-2/">understanding your W-2</a> explains the matching boxes on that form.</p>

<?= faq_block([
  ['What is a 1099-G form?', '<p>Form 1099-G, Certain Government Payments, is sent by government agencies to report payments such as unemployment compensation, state or local income tax refunds, taxable grants and agricultural payments. You use it to report those amounts on your federal and state returns.</p>'],
  ['Do I have to report a 1099-G on my taxes?', '<p>You must report unemployment compensation (Box 1) and other taxable payments in Boxes 5 through 9. A state tax refund in Box 2 only needs to be reported if you itemized deductions and deducted state income tax in the year the refund relates to, and only to the extent it gave you a tax benefit.</p>'],
  ['Is my state tax refund taxable?', '<p>Only if you itemized deductions on your federal return in the year you paid the tax, deducted state income tax (not sales tax), and the deduction lowered your federal tax. If you took the standard deduction, a state refund is not taxable federally.</p>'],
  ['How much tax will I owe on unemployment?', '<p>Unemployment is taxed at your ordinary federal income tax rate, the same as wages, but without Social Security or Medicare tax. How much you owe depends on your total income and filing status. If you chose 10% withholding, that may or may not cover it; a tax refund calculator can show the difference.</p>'],
  ['Where do I get my 1099-G?', '<p>From the agency that paid you: your state unemployment office for Box 1, and your state or local tax department for Box 2. Many states provide the 1099-G online through your account rather than by mail. It should be available by January 31.</p>'],
  ['What if I got a 1099-G for unemployment I did not file for?', '<p>That usually means identity theft. Report it to the state agency that issued the form and ask for a corrected 1099-G, do not include the amount as income, and file your return on time based on the income you actually received.</p>'],
]) ?>
<?= post_close($SLUG, 'tax-refund-calculator', ['amended-tax-return', 'quarterly-taxes-101-guide', 'understanding-your-w-2']) ?>
