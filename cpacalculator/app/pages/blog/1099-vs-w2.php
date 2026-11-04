<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$pct = fn(float $x, int $dp = 1): string => number_format($x * 100, $dp) . '%';
/* 1099 math: net profit -> SE tax, half-SE adjustment, standard deduction, QBI (20% of QBI reduced by half SE tax), income tax. Single, no other income. */
$c1099 = function (float $net) use ($Y): array {
  $base = $net * 0.9235;
  $se = min($base, $Y['ssWageBase']) * 0.124 + $base * 0.029;
  $agi = $net - $se / 2;
  $pre = max(0, $agi - $Y['std']['single']);
  $qbi = 0.20 * min(max(0, $net - $se / 2), $pre);
  $taxable = max(0, $pre - $qbi);
  $inc = fed_tax($taxable, 'single')['tax'];
  return ['net' => $net, 'base' => $base, 'se' => $se, 'half' => $se / 2, 'agi' => $agi, 'std' => $Y['std']['single'], 'qbi' => $qbi,
    'taxable' => $taxable, 'inc' => $inc, 'total' => $se + $inc, 'take' => $net - $se - $inc];
};
$amt = 75000;
$w2 = salary_breakdown($amt, 'single');
$k = $c1099($amt);
$employer_fica = min($amt, $Y['ssWageBase']) * 0.062 + $amt * 0.0145;
/* Gross 1099 income needed to match the W-2 take-home (bisection). */
$lo = $amt; $hi = $amt * 1.6;
for ($i = 0; $i < 60; $i++) { $mid = ($lo + $hi) / 2; if ($c1099($mid)['take'] < $w2['net']) $lo = $mid; else $hi = $mid; }
$equiv = $hi;
$equiv_hr = $equiv / 2080;
$w2_hr = $amt / 2080;
$premium = $equiv / $amt - 1;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">The 1099 vs W-2 question comes down to one thing: who is responsible for the taxes, benefits and paperwork. A W-2 employee has taxes withheld from every paycheck and splits Social Security and Medicare with the employer. A 1099 contractor is paid in full, pays both halves of those taxes as self-employment tax, and runs their own business, with the deductions and the risks that come with it. This guide compares the two side by side, with <?= TAX_YEAR ?> numbers, and shows how to translate a W-2 salary into an equivalent 1099 rate.</p>

<div class="callout"><?= icon('scale') ?><p><strong>Quick answer:</strong> on the same <?= money($amt) ?> of pay, a single W-2 employee keeps about <?= money($w2['net']) ?> after federal income tax and FICA, while a 1099 contractor with no expenses keeps about <?= money($k['take']) ?>. To match the W-2 take-home, the contractor needs roughly <?= money(round($equiv, -2)) ?> of revenue, about <?= $pct($premium, 0) ?> more, before counting the cost of benefits the employer no longer provides.</p></div>

<h2 id="differences">1099 vs W-2: the key differences</h2>
<p>"W-2" and "1099" are the names of the tax forms each type of worker receives at year-end. A <a href="/blog/understanding-your-w-2/">Form W-2</a> reports an employee's wages and the taxes withheld. A Form 1099-NEC reports payments to a non-employee, with nothing withheld. People often say "1099 employee," but that is a contradiction in terms: a worker who properly receives a 1099 is a <strong>1099 contractor</strong> (an independent contractor), not an employee.</p>
<div class="table-wrap"><table>
<thead><tr><th></th><th>W-2 employee</th><th>1099 contractor</th></tr></thead>
<tbody>
<tr><td><b>Income tax</b></td><td>Withheld from each paycheck based on Form W-4</td><td>Nothing withheld; you pay through quarterly estimated payments</td></tr>
<tr><td><b>Social Security and Medicare</b></td><td>You pay 7.65%; employer pays another 7.65%</td><td>You pay both halves: 15.3% self-employment tax on 92.35% of net profit</td></tr>
<tr><td><b>Business expenses</b></td><td>Generally not deductible for federal purposes</td><td>Deductible on Schedule C, reducing income tax and SE tax</td></tr>
<tr><td><b>QBI deduction</b></td><td>Not available on wages</td><td>Up to 20% of qualified business income</td></tr>
<tr><td><b>Benefits</b></td><td>Often health insurance, 401(k) match, paid leave</td><td>None from the client; you fund your own</td></tr>
<tr><td><b>Unemployment and workers' comp</b></td><td>Generally covered</td><td>Generally not covered</td></tr>
<tr><td><b>Control over the work</b></td><td>Employer directs how, when and where</td><td>You decide how the result is achieved</td></tr>
<tr><td><b>Tax forms</b></td><td>W-4 at hire, W-2 at year-end, Form 1040</td><td>W-9 at hire, 1099-NEC (or 1099-K), Schedule C and Schedule SE</td></tr>
</tbody></table></div>
<p>For payments made in <?= TAX_YEAR ?>, a business must send a 1099-NEC once it pays a contractor <?= money(2000) ?> or more in the year, up from $600 under the old rule. That threshold only controls the form. Every dollar of contract income is taxable whether or not a 1099 arrives. If you have just received one, see <a href="/blog/got-a-1099-exactly-what-to-do-next/">Got a 1099? Here is exactly what to do next</a>.</p>

<h2 id="taxes">How taxes differ: W-2 vs 1099</h2>
<p>Both workers pay the same federal income tax brackets. The difference is in payroll taxes and deductions.</p>
<p><strong>W-2 employees</strong> pay 6.2% Social Security on wages up to the <?= TAX_YEAR ?> wage base of <?= money($Y['ssWageBase']) ?> and 1.45% Medicare on all wages, plus an extra 0.9% Medicare above <?= money($Y['addlMedicare']['single']) ?>. The employer matches the 7.65% and never shows it on your pay stub. (Our guide to the <a href="/blog/fica-tax-rate/">FICA tax rate</a> covers the details.)</p>
<p><strong>1099 contractors</strong> pay self-employment tax: 12.4% Social Security and 2.9% Medicare on 92.35% of net profit. The 92.35% factor mimics the fact that an employer's half of FICA is not taxable wages to an employee. Contractors then deduct half of their SE tax as an adjustment to income, and most can claim the 20% qualified business income (QBI) deduction, which the One Big Beautiful Bill Act (OBBBA) made permanent. You can model your own numbers with the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a>.</p>
<div class="formula">SE tax = net profit × 92.35% × 15.3% (12.4% stops at the Social Security wage base)<br>Taxable income = net profit − ½ SE tax − standard deduction − QBI deduction</div>

<h2 id="comparison">Same pay, two ways: <?= money($amt) ?> as W-2 vs 1099</h2>
<p>Here is a single filer with no other income earning <?= money($amt) ?> in <?= TAX_YEAR ?>, first as an employee and then as a contractor with no business expenses. Both take the <?= money($Y['std']['single']) ?> standard deduction.</p>
<div class="table-wrap"><table>
<caption class="sr-only"><?= money($amt) ?> as W-2 wages vs 1099 income, <?= TAX_YEAR ?>, single</caption>
<thead><tr><th></th><th class="n">W-2 employee</th><th class="n">1099 contractor</th></tr></thead>
<tbody>
<tr><td>Gross pay / net profit</td><td class="n"><?= money($amt) ?></td><td class="n"><?= money($amt) ?></td></tr>
<tr><td>Half of SE tax (adjustment)</td><td class="n">—</td><td class="n">−<?= money($k['half']) ?></td></tr>
<tr><td>Standard deduction</td><td class="n">−<?= money($w2['std']) ?></td><td class="n">−<?= money($k['std']) ?></td></tr>
<tr><td>QBI deduction (20%)</td><td class="n">—</td><td class="n">−<?= money($k['qbi']) ?></td></tr>
<tr><td><b>Taxable income</b></td><td class="n"><b><?= money($w2['taxable']) ?></b></td><td class="n"><b><?= money($k['taxable']) ?></b></td></tr>
<tr><td>Federal income tax</td><td class="n"><?= money($w2['tax']) ?></td><td class="n"><?= money($k['inc']) ?></td></tr>
<tr><td>Employee FICA / self-employment tax</td><td class="n"><?= money($w2['fica']) ?></td><td class="n"><?= money($k['se']) ?></td></tr>
<tr><td><b>Total federal tax</b></td><td class="n"><b><?= money($w2['tax'] + $w2['fica']) ?></b></td><td class="n"><b><?= money($k['total']) ?></b></td></tr>
<tr><td><b>Take-home before state tax</b></td><td class="n"><b><?= money($w2['net']) ?></b></td><td class="n"><b><?= money($k['take']) ?></b></td></tr>
</tbody></table></div>
<p>The contractor pays <?= money($k['se'] - $w2['fica']) ?> more in payroll-type tax, because they cover the employer's half too. The QBI deduction and the SE tax adjustment pull their income tax down by <?= money($w2['tax'] - $k['inc']) ?>, which softens the gap but does not close it. Net result: the contractor keeps <?= money($w2['net'] - $k['take']) ?> less. Meanwhile, the employer in the W-2 column also paid <?= money($employer_fica) ?> of its own FICA, money it saves by hiring a contractor.</p>
<p>In real life most contractors have deductible expenses (software, equipment, a <a href="/calculators/home-office-deduction/">home office</a>, <a href="/calculators/mileage-deduction/">business mileage</a>) that reduce both taxes, so their actual gap may be smaller. Run your own figures in the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>.</p>

<h2 id="equivalent-rate">How to convert a W-2 salary to a 1099 rate</h2>
<p>To keep the same after-tax income as the <?= money($amt) ?> W-2 job, our model contractor would need about <strong><?= money(round($equiv, -2)) ?></strong> of net profit. Over a 2,080-hour year that is roughly <?= money($equiv_hr, 2) ?> an hour, versus <?= money($w2_hr, 2) ?> for the employee. That covers taxes only. A fair 1099 rate should also replace what the employer was paying for:</p>
<ul>
<li><strong>Health insurance.</strong> Self-employed people can usually deduct premiums as an adjustment to income, but they pay the full premium.</li>
<li><strong>Retirement match.</strong> A Solo 401(k) or SEP-IRA lets you save more than most employees can, but there is no match. The <?= TAX_YEAR ?> employee deferral limit is <?= money($Y['k401']) ?>.</li>
<li><strong>Paid time off and unbillable hours.</strong> Contractors are paid only for billable work. If you bill 1,600 hours instead of 2,080, your hourly rate must rise to earn the same annual amount.</li>
<li><strong>Business costs.</strong> Equipment, insurance, accounting and marketing are now yours.</li>
</ul>
<div class="formula">Target 1099 revenue ≈ tax-equivalent amount + annual benefits value + business expenses<br>Target hourly rate = target revenue ÷ expected billable hours</div>
<p>To translate salaries into hourly figures, the <a href="/calculators/salary-to-hourly/">salary to hourly calculator</a> is a quick check.</p>

<h2 id="classification">1099 contractor or employee? The IRS classification tests</h2>
<p>You do not get to choose W-2 or 1099 status by contract alone. The IRS looks at the whole relationship using common-law rules, grouped into three categories:</p>
<div class="table-wrap"><table>
<thead><tr><th>Category</th><th>Points toward employee</th><th>Points toward contractor</th></tr></thead>
<tbody>
<tr><td><b>Behavioral control</b></td><td>The company dictates hours, methods, sequence, tools; provides detailed training; evaluates how work is done</td><td>You decide how, when and where to do the work; evaluation is based on results</td></tr>
<tr><td><b>Financial control</b></td><td>Paid by the hour or salary; expenses reimbursed; company supplies equipment; no chance of profit or loss</td><td>Significant investment in your own tools; unreimbursed expenses; you serve multiple clients and can earn a profit or take a loss</td></tr>
<tr><td><b>Relationship of the parties</b></td><td>Benefits such as insurance or paid leave; indefinite relationship; work is a key part of the company's regular business</td><td>Written contract for a defined project; no benefits; services offered to the public</td></tr>
</tbody></table></div>
<p>No single factor decides the outcome. Other agencies use their own tests: the Department of Labor applies an "economic reality" test for wage-and-hour law, and some states use a stricter "ABC test" for state payroll taxes and unemployment, under which a worker is presumed to be an employee unless all three conditions are met. A worker can therefore be a contractor for one purpose and an employee for another.</p>

<h2 id="misclassification">What if you are misclassified?</h2>
<p>If you were paid on a 1099 but the facts look like employment, you have options:</p>
<ol>
<li><strong>Form SS-8.</strong> Either the worker or the business can ask the IRS for a formal determination of worker status. Expect it to take months.</li>
<li><strong>Form 8919.</strong> A worker who believes they were an employee can use Form 8919 to pay only the employee's share of Social Security and Medicare (7.65%) on the wages, instead of the full 15.3% SE tax. You need a qualifying reason, such as having filed an SS-8 or having received a determination from the IRS.</li>
<li><strong>State agencies.</strong> State labor and unemployment departments handle claims for unemployment benefits, minimum wage and overtime.</li>
</ol>
<div class="callout warn"><?= icon('shield') ?><p><strong>For businesses:</strong> misclassifying employees can mean back payroll taxes, penalties and interest, plus state liabilities. If you are unsure, the IRS Voluntary Classification Settlement Program (VCSP) lets eligible businesses reclassify workers going forward with reduced federal liability for past years.</p></div>

<h2 id="which-pays-more">Which pays more, 1099 or W-2?</h2>
<p>At the same headline number, W-2 nearly always pays more once you count the employer's FICA and benefits. A 1099 role pays more only when the rate is high enough to cover the extra tax, the lost benefits and unbillable time, and when you can use the contractor advantages:</p>
<ul>
<li><strong>Deductions.</strong> Ordinary and necessary business expenses come off the top. <?= TAX_YEAR ?> rules include 100% bonus depreciation for qualifying property and a mileage rate of <?= number_format($Y['mileage'] * 100, 1) ?>¢ per mile.</li>
<li><strong>Bigger retirement contributions</strong> through a Solo 401(k), combining employee deferrals with employer profit-sharing.</li>
<li><strong>Entity choices.</strong> Once profit is high enough, an S corporation election can reduce self-employment tax by splitting income between a reasonable salary and distributions. The <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a> shows the break-even.</li>
<li><strong>Control.</strong> More clients means less dependence on one employer.</li>
</ul>
<p>The trade-off is responsibility: contractors must make <a href="/blog/quarterly-taxes-101-guide/">quarterly estimated tax payments</a>, keep records and file Schedule C. Our <a href="/blog/schedule-c-tax-form/">Schedule C tax form guide</a> walks through it line by line.</p>

<h2 id="both">Can you be W-2 and 1099 at the same time?</h2>
<p>Yes, and many people are: a full-time job plus freelance work on the side. You file one Form 1040 with your W-2 wages and a Schedule C for the side business. Two details matter. First, W-2 wages count toward the Social Security wage base before SE income, so a high earner may owe only the 2.9% Medicare portion on side income. Second, you can avoid quarterly payments by increasing W-4 withholding at your job to cover the tax on your 1099 income. A worker cannot, however, be both an employee and a contractor of the same company for the same type of work.</p>

<?= faq_block([
  ['What is the difference between 1099 and W-2?', '<p>A W-2 employee has income tax and FICA withheld, splits Social Security and Medicare with the employer and usually receives benefits. A 1099 contractor is paid without withholding, pays 15.3% self-employment tax on 92.35% of net profit, deducts business expenses and makes quarterly estimated payments. The difference in the 1099 vs W-2 question is classification, not just paperwork.</p>'],
  ['Is it better to be 1099 or W-2?', '<p>At the same pay, W-2 is usually better financially because the employer pays half of FICA and often provides benefits. In our ' . TAX_YEAR . ' example, ' . money($amt) . ' as W-2 leaves about ' . money($w2['net'] - $k['take']) . ' more after federal tax than the same amount on a 1099. A 1099 role can come out ahead when the rate is high enough and you have meaningful deductions.</p>'],
  ['How much more should I charge as a 1099 contractor?', '<p>Enough to cover the extra self-employment tax, lost benefits, unbillable time and business expenses. Taxes alone required about ' . $pct($premium, 0) . ' more revenue in our ' . money($amt) . ' example; once benefits and unpaid time are added, many contractors price well above that. Use the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> to test a rate.</p>'],
  ['Do 1099 employees pay more taxes?', '<p>A properly classified 1099 contractor (not an employee) pays both the employee and employer shares of Social Security and Medicare, so their payroll-type tax is roughly double. The half-SE-tax adjustment and the QBI deduction reduce income tax, but total federal tax is typically higher at the same pay.</p>'],
  ['How do I know if I should be W-2 or 1099?', '<p>The IRS weighs behavioral control, financial control and the relationship of the parties. If the company controls how and when you work, supplies your tools and treats the role as ongoing, you are likely an employee. You or the business can file Form SS-8 to get an IRS determination.</p>'],
  ['What happens if my employer pays me on a 1099 but I should be W-2?', '<p>You can file Form SS-8 for a determination and use Form 8919 to pay only the employee share of Social Security and Medicare on those wages instead of full self-employment tax. State labor agencies can address unemployment and wage claims.</p>'],
]) ?>
<?= post_close($SLUG, '1099-tax-calculator', ['got-a-1099-exactly-what-to-do-next', 'schedule-c-tax-form', 'quarterly-taxes-101-guide']) ?>
