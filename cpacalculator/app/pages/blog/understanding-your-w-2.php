<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$ssMax = $Y['ssWageBase'] * 0.062;
/* Example: $70,000 salary, 6% 401(k), $2,400 pre-tax health premiums, $1,000 HSA through payroll. */
$w_sal = 70000; $w_k = $w_sal * 0.06; $w_hp = 2400; $w_hsa = 1000;
$w_b1 = $w_sal - $w_k - $w_hp - $w_hsa;
$w_b3 = min($w_sal - $w_hp - $w_hsa, $Y['ssWageBase']);
$w_b5 = $w_sal - $w_hp - $w_hsa;
echo post_open($SLUG, '2026-11-03'); ?>
<p class="lead">Form W-2, the Wage and Tax Statement, is the one-page summary your employer files with the IRS and the Social Security Administration each year. It shows what you earned, what was withheld, and a handful of benefits that affect your return. Nearly every number on it ends up somewhere on your Form 1040, so understanding your W-2 box by box is the fastest way to file accurately and spot a mistake before the IRS does.</p>

<div class="callout"><?= icon('spark') ?><p><strong>Key dates:</strong> employers must send W-2s to employees (and file them with the SSA) by <strong>January 31</strong>. If yours has not arrived by mid-February, ask your employer first. You need one W-2 from every employer you worked for during the year, even briefly.</p></div>

<h2 id="identity-boxes">Boxes a–f: who the form is about</h2>
<p>The lettered boxes on the left identify you and your employer:</p>
<ul>
<li><strong>Box a</strong>: your Social Security number. Check every digit; a wrong SSN means your wages may not be credited to your Social Security record.</li>
<li><strong>Box b</strong>: your employer's identification number (EIN).</li>
<li><strong>Box c</strong>: employer's name and address.</li>
<li><strong>Box d</strong>: a control number your payroll provider may use internally. It is often blank, and tax software sometimes asks for it only for matching.</li>
<li><strong>Boxes e and f</strong>: your name and address. Your name should match your Social Security card. If you changed your name, update it with the SSA so the records match.</li>
</ul>

<h2 id="wages-withholding">Boxes 1–6: wages and withholding</h2>
<p>These six boxes do most of the work on your return.</p>
<div class="table-wrap"><table>
<thead><tr><th>Box</th><th>What it shows</th><th>Where it goes</th></tr></thead>
<tbody>
<tr><td><b>1</b></td><td>Wages, tips and other compensation subject to federal <em>income</em> tax</td><td>Form 1040, line 1a</td></tr>
<tr><td><b>2</b></td><td>Federal income tax withheld</td><td>Form 1040, line 25a</td></tr>
<tr><td><b>3</b></td><td>Social Security wages (capped at <?= money($Y['ssWageBase']) ?> for <?= TAX_YEAR ?>)</td><td>Used for your Social Security record; checks for excess withholding</td></tr>
<tr><td><b>4</b></td><td>Social Security tax withheld (6.2% of Box 3)</td><td>Not on the 1040 unless you overpaid across jobs</td></tr>
<tr><td><b>5</b></td><td>Medicare wages (no cap)</td><td>Form 8959 if you owe Additional Medicare Tax</td></tr>
<tr><td><b>6</b></td><td>Medicare tax withheld (1.45%, plus 0.9% on wages over $200,000)</td><td>Form 8959 if applicable</td></tr>
</tbody></table></div>
<h3 id="why-different">Why Boxes 1, 3 and 5 are different</h3>
<p>The three wage boxes measure different things. Traditional 401(k), 403(b) and 457(b) deferrals reduce Box 1 but <em>not</em> Boxes 3 and 5, because they are still subject to Social Security and Medicare tax. Pre-tax health, dental and vision premiums, HSA contributions made through a cafeteria plan, and pre-tax commuter benefits reduce all three. Here is how that works for an employee earning <?= money($w_sal) ?>:</p>
<div class="table-wrap"><table>
<thead><tr><th>Item</th><th class="n">Box 1</th><th class="n">Boxes 3 &amp; 5</th></tr></thead>
<tbody>
<tr><td>Salary</td><td class="n"><?= money($w_sal) ?></td><td class="n"><?= money($w_sal) ?></td></tr>
<tr><td>6% traditional 401(k) deferral</td><td class="n">−<?= money($w_k) ?></td><td class="n">no change</td></tr>
<tr><td>Pre-tax health premiums (Section 125)</td><td class="n">−<?= money($w_hp) ?></td><td class="n">−<?= money($w_hp) ?></td></tr>
<tr><td>HSA contributions through payroll</td><td class="n">−<?= money($w_hsa) ?></td><td class="n">−<?= money($w_hsa) ?></td></tr>
<tr><td><b>Amount reported</b></td><td class="n"><b><?= money($w_b1) ?></b></td><td class="n"><b><?= money($w_b5) ?></b></td></tr>
</tbody></table></div>
<p>Box 4 would show <?= money($w_b3 * 0.062, 2) ?> (6.2% of <?= money($w_b3) ?>) and Box 6 would show <?= money($w_b5 * 0.0145, 2) ?> (1.45%). If you earn above the Social Security wage base, Box 3 stops at <?= money($Y['ssWageBase']) ?> while Box 5 keeps going, so Box 5 can be much larger than Box 3.</p>
<div class="callout"><?= icon('refund') ?><p><strong>Worked for two or more employers?</strong> Each employer withholds Social Security separately. If your combined Box 4 amounts exceed <?= money($ssMax, 2) ?> for <?= TAX_YEAR ?> (6.2% of <?= money($Y['ssWageBase']) ?>), you get the excess back as a credit on Schedule 3. The <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> shows how withholding in Box 2 compares with your actual tax.</p></div>

<h2 id="tips-benefits">Boxes 7–11: tips, benefits and deferred pay</h2>
<ul>
<li><strong>Box 7, Social Security tips</strong>: tips you reported to your employer. They are already included in Box 1.</li>
<li><strong>Box 8, allocated tips</strong>: tips your employer assigned to you because reported tips fell short of the required share. These are <em>not</em> in Box 1; you add them as wages and figure Social Security and Medicare on them with Form 4137.</li>
<li><strong>Box 9</strong>: no longer used and should be blank.</li>
<li><strong>Box 10, dependent care benefits</strong>: amounts paid through a dependent care FSA or provided by your employer. For <?= TAX_YEAR ?> the tax-free limit rises to $7,500 per household ($3,750 married filing separately) under OBBBA, up from $5,000. You complete Form 2441 to claim the exclusion; any excess is taxable.</li>
<li><strong>Box 11, nonqualified plans</strong>: distributions from, or vested amounts in, a nonqualified deferred compensation plan. It is informational, since the amount is already included in Box 1, but it helps the SSA apply earnings to the right year.</li>
</ul>

<h2 id="box-12">Box 12 codes explained</h2>
<p>Box 12 holds up to four coded amounts (employers issue an extra W-2 if you have more). Some codes are taxable income already included in Box 1; most are informational. The full list:</p>
<div class="table-wrap"><table>
<thead><tr><th>Code</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td><b>A / B</b></td><td>Uncollected Social Security or RRTA tax (A) and Medicare tax (B) on tips; you pay it with your return</td></tr>
<tr><td><b>C</b></td><td>Taxable cost of group-term life insurance over $50,000 (already in Boxes 1, 3, 5)</td></tr>
<tr><td><b>D</b></td><td>Traditional 401(k) elective deferrals</td></tr>
<tr><td><b>E</b></td><td>403(b) elective deferrals</td></tr>
<tr><td><b>F</b></td><td>Salary reduction SEP (SARSEP) deferrals</td></tr>
<tr><td><b>G</b></td><td>457(b) deferrals and employer contributions</td></tr>
<tr><td><b>H</b></td><td>501(c)(18)(D) plan deferrals (deductible on Schedule 1)</td></tr>
<tr><td><b>J</b></td><td>Nontaxable sick pay</td></tr>
<tr><td><b>K</b></td><td>20% excise tax on excess golden parachute payments</td></tr>
<tr><td><b>L</b></td><td>Substantiated employee business expense reimbursements (nontaxable)</td></tr>
<tr><td><b>M / N</b></td><td>Uncollected Social Security/RRTA (M) and Medicare (N) on group-term life for former employees</td></tr>
<tr><td><b>P</b></td><td>Excludable moving expense reimbursements (Armed Forces only)</td></tr>
<tr><td><b>Q</b></td><td>Nontaxable combat pay</td></tr>
<tr><td><b>R</b></td><td>Employer contributions to an Archer MSA</td></tr>
<tr><td><b>S</b></td><td>SIMPLE IRA salary reduction contributions</td></tr>
<tr><td><b>T</b></td><td>Employer-provided adoption benefits (Form 8839)</td></tr>
<tr><td><b>V</b></td><td>Income from exercising nonstatutory stock options (already in Box 1)</td></tr>
<tr><td><b>W</b></td><td>Employer and pre-tax payroll contributions to your HSA (report on Form 8889)</td></tr>
<tr><td><b>Y / Z</b></td><td>Deferrals under a Section 409A plan (Y); income from a 409A plan that failed the rules (Z)</td></tr>
<tr><td><b>AA / BB / EE</b></td><td>Roth contributions to a 401(k) (AA), 403(b) (BB) or governmental 457(b) (EE)</td></tr>
<tr><td><b>DD</b></td><td>Total cost of employer-sponsored health coverage. Informational only, <em>not</em> taxable</td></tr>
<tr><td><b>FF</b></td><td>Benefits under a qualified small employer HRA (QSEHRA)</td></tr>
<tr><td><b>GG / HH</b></td><td>Income from qualified equity grants under Section 83(i) (GG); aggregate deferrals under 83(i) elections (HH)</td></tr>
<tr><td><b>II</b></td><td>Medicaid waiver payments excluded from income</td></tr>
<tr><td><b>TA</b></td><td>Employer contributions to a "Trump account" for a child (new for 2026)</td></tr>
<tr><td><b>TP</b></td><td>Total qualified tips for the new tips deduction (new for 2026)</td></tr>
<tr><td><b>TT</b></td><td>Total qualified overtime compensation for the new overtime deduction (new for 2026)</td></tr>
</tbody></table></div>
<p>The most common codes you will see are D (or AA for Roth), W and DD. Code D matters if you also contribute to a Solo 401(k) on the side, because the employee deferral limit of <?= money($Y['k401']) ?> for <?= TAX_YEAR ?> is shared across all of your 401(k) and 403(b) plans.</p>

<h2 id="tips-overtime">New for 2026: qualified tips and overtime on your W-2</h2>
<p>OBBBA created two temporary deductions for 2025 through 2028: up to <?= money($Y['tipsMax']) ?> of <strong>qualified tips</strong>, and up to <?= money($Y['overtimeMax']['single']) ?> (<?= money($Y['overtimeMax']['mfj']) ?> married filing jointly) of <strong>qualified overtime compensation</strong>, meaning the premium part of overtime pay required by the Fair Labor Standards Act (the "half" in time-and-a-half). Both deductions phase out above $150,000 of modified AGI ($300,000 joint), are available whether or not you itemize, and are not available if you are married filing separately.</p>
<p>For 2025, employers were not required to report these amounts separately, so many workers had to use paystubs or a separate employer statement. Starting with 2026 W-2s (issued in early 2027), the form has dedicated places for them: <strong>Box 12 code TP</strong> for qualified tips, <strong>code TT</strong> for qualified overtime, and a split Box 14, where <strong>Box 14b</strong> holds the Treasury tipped occupation code that shows your job is one where tipping is customary. The tips and overtime remain in Box 1 (they are still wages); the deduction is taken separately on your return, which reduces income tax but not Social Security or Medicare tax. The <a href="/calculators/federal-income-tax/">federal income tax calculator</a> includes both deductions.</p>

<h2 id="box-13-14">Boxes 13 and 14</h2>
<p><strong>Box 13</strong> has three checkboxes:</p>
<ul>
<li><strong>Statutory employee</strong>: certain drivers, salespeople and home workers whose income is reported on Schedule C, while the employer still withholds Social Security and Medicare.</li>
<li><strong>Retirement plan</strong>: you were an active participant in a workplace plan. This can limit whether your traditional IRA contribution is deductible.</li>
<li><strong>Third-party sick pay</strong>: sick pay from an insurer or other third party.</li>
</ul>
<p><strong>Box 14</strong> ("Other") is free-form. Employers use it for items such as state disability insurance withholding (for example CA SDI or NY SDI/PFL), union dues, after-tax contributions, non-cash fringe benefits, or the value of a personal-use company car. Some of these matter: state disability withholding can count as state income tax if you itemize, for example. If a Box 14 label is unclear, ask payroll what it means.</p>

<h2 id="state-boxes">Boxes 15–20: state and local taxes</h2>
<ul>
<li><strong>Box 15</strong>: the state and your employer's state ID number</li>
<li><strong>Box 16</strong>: state wages (may differ from Box 1 because states treat some benefits differently)</li>
<li><strong>Box 17</strong>: state income tax withheld</li>
<li><strong>Boxes 18–20</strong>: local wages, local income tax withheld, and the locality name</li>
</ul>
<p>If you moved or worked in more than one state, you may see two lines here. Each state return uses its own line. Boxes 17 and 19 are also what you would claim as state and local income taxes if you itemize, subject to the <?= money($Y['saltCap']) ?> SALT cap for <?= TAX_YEAR ?> (which phases down for higher incomes).</p>

<h2 id="w2-vs-paystub">W-2 vs. your final paystub</h2>
<p>Your last paystub's year-to-date gross pay rarely matches Box 1, and that is normal. Common reasons:</p>
<ul>
<li><strong>Pre-tax deductions</strong> (401(k), health premiums, HSA, FSA, commuter benefits) are subtracted from Box 1 but included in YTD gross.</li>
<li><strong>Taxable fringe benefits</strong> (group-term life over $50,000, personal use of a company car, some gift cards) are <em>added</em> to Box 1 but never paid in cash.</li>
<li><strong>Pay dates, not work dates:</strong> a paycheck for the last week of December paid on January 2 belongs to next year's W-2.</li>
<li><strong>Year-end adjustments</strong> or reimbursements processed after your last stub.</li>
</ul>
<p>To reconcile: start with YTD gross, subtract pre-tax items, and add taxable fringe benefits. You should land on Box 1. YTD Social Security and Medicare withholding on the paystub should match Boxes 4 and 6 exactly. The <a href="/calculators/paycheck-calculator/">paycheck calculator</a> breaks down a single check the same way.</p>

<h2 id="corrections">If your W-2 is wrong or missing</h2>
<ol>
<li><strong>Ask your employer for a corrected W-2 (Form W-2c).</strong> Employers correct errors in names, SSNs, wages or withholding by issuing a W-2c to you and filing it with the SSA.</li>
<li><strong>Still missing by the end of February?</strong> Contact the IRS. It will contact the employer on your behalf. Have your dates of employment and an estimate of your wages and withholding (your final paystub works).</li>
<li><strong>Filing deadline approaching?</strong> File on time using <strong>Form 4852</strong>, a substitute W-2 based on your best figures, or request an extension.</li>
<li><strong>Already filed?</strong> If a W-2c changes your tax, file an amended return on Form 1040-X.</li>
</ol>
<p>You can also download a wage and income transcript from your IRS Online Account, which shows the W-2 data employers reported to the IRS.</p>

<h2 id="using-it">Using your W-2 to plan next year</h2>
<p>Box 2 tells you how much federal tax you have already paid. Compare it with your projected total tax: a big refund means you are over-withholding, and a balance due means you should increase withholding on Form W-4. Run your W-2 numbers through the <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> to see where you stand, and if you also have freelance income, read <a href="/blog/got-a-1099-exactly-what-to-do-next/">Got a 1099? Here's what to do next</a>, since extra W-2 withholding is one of the easiest ways to cover tax on side income.</p>

<?= faq_block([
  ['Why is Box 1 on my W-2 lower than my salary?', '<p>Box 1 shows wages subject to federal income tax. Traditional 401(k) and 403(b) deferrals, pre-tax health premiums, HSA contributions through payroll and other pre-tax benefits are subtracted, so Box 1 is usually lower than your gross salary. Taxable fringe benefits can push it the other way.</p>'],
  ['What does code DD in Box 12 mean? Is it taxable?', '<p>Code DD reports the total cost of your employer-sponsored health coverage, including both your share and your employer\'s. It is informational only and is not taxable income. You do not enter it anywhere that affects your tax.</p>'],
  ['When should I receive my W-2?', '<p>Employers must furnish W-2s by January 31. If the form has not arrived by mid-February, ask your employer. If it is still missing by the end of February, contact the IRS, and if needed file using Form 4852 as a substitute.</p>'],
  ['What is the maximum Social Security tax on a W-2 for 2026?', '<p>For 2026 the Social Security wage base is $184,500, so the most one employer should withhold is $11,439 (6.2%). If you had several employers and the total in Box 4 is higher, claim the excess as a credit on Schedule 3 of your return.</p>'],
  ['Where do I find my qualified tips and overtime for the new deductions?', '<p>On 2026 W-2s, qualified tips appear in Box 12 with code TP and qualified overtime compensation with code TT, and tipped workers will see an occupation code in Box 14b. For 2025, employers were not required to report these separately, so you may need your paystubs or a statement from your employer.</p>'],
  ['What is a W-2c?', '<p>Form W-2c is a corrected W-2. Your employer issues it to fix errors in names, Social Security numbers, wages or withholding. If you already filed using the incorrect W-2 and the correction changes your tax, file Form 1040-X.</p>'],
]) ?>
<?= post_close($SLUG, 'tax-refund-calculator', ['how-much-federal-tax-will-i-pay', 'got-a-1099-exactly-what-to-do-next', 'quarterly-taxes-101-guide']) ?>
