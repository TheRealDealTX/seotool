<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$amounts = [30000, 50000, 75000, 100000, 150000];
$rows = [];
foreach (['single', 'mfj'] as $st) foreach ($amounts as $amt) $rows[$st][$amt] = salary_breakdown($amt, $st);
$sal_link = fn(int $amt): string => in_array($amt, SALARY_PAGES, true) ? '<a href="/calculators/federal-income-tax/' . $amt . '/">' . money($amt) . '</a>' : money($amt);
$pct = fn(float $x, int $dp = 1): string => number_format($x * 100, $dp) . '%';
$ex = $rows['single'][75000];
$top_slice = 0;
foreach ($ex['layers'] as $l) if ($l['amount'] > 0) $top_slice = $l['amount'];
$table = function (string $st) use ($rows, $sal_link, $pct): string {
  $h = '<div class="table-wrap"><table><caption class="sr-only">' . TAX_YEAR . ' federal income tax by salary — ' . e(status_label($st)) . '</caption><thead><tr><th>Salary</th><th class="n">Taxable</th><th class="n">Income tax</th><th class="n">Effective</th><th class="n">Marginal</th><th class="n">FICA</th><th class="n">Take-home</th></tr></thead><tbody>';
  foreach ($rows[$st] as $amt => $r) {
    $h .= '<tr><td><b>' . $sal_link($amt) . '</b></td><td class="n">' . money($r['taxable']) . '</td><td class="n">' . money($r['tax']) . '</td><td class="n">' . $pct($r['effective']) . '</td><td class="n">' . ($r['taxable'] > 0 ? $pct($r['marginal'], 0) : '0%') . '</td><td class="n">' . money($r['fica']) . '</td><td class="n">' . money($r['net']) . '</td></tr>';
  }
  return $h . '</tbody></table></div>';
};
echo post_open($SLUG, '2026-11-03'); ?>
<p class="lead">How much federal income tax you will pay depends on three things: how much you earn, your filing status, and which deductions and credits you claim. The fastest way to understand it is to see real numbers. Below are worked <?= TAX_YEAR ?> examples at five common salaries for single filers and married couples filing jointly, computed with the same tax tables our calculators use, followed by a step-by-step explanation of how the math works.</p>

<div class="callout"><?= icon('flag') ?><p><strong>Want your exact number?</strong> The <a href="/calculators/federal-income-tax/">federal income tax calculator</a> adds credits, itemized deductions, the new tips, overtime and senior deductions, and other income. The examples here assume only W-2 wages and the standard deduction.</p></div>

<h2 id="quick-answer">Quick answer: 2026 federal tax by salary</h2>
<p>For <?= TAX_YEAR ?>, a single filer earning <?= money(50000) ?> pays about <?= money($rows['single'][50000]['tax']) ?> in federal income tax, an effective rate of <?= $pct($rows['single'][50000]['effective']) ?>. At <?= money(100000) ?>, it is about <?= money($rows['single'][100000]['tax']) ?> (<?= $pct($rows['single'][100000]['effective']) ?>). Married couples filing jointly pay much less on the same household income because their brackets and standard deduction are twice as wide.</p>

<h2 id="single">Single filers</h2>
<?= $table('single') ?>
<p>Click any salary to open a full breakdown page for that income. "Taxable income" is salary minus the <?= money($Y['std']['single']) ?> standard deduction. "FICA" is Social Security (6.2%) and Medicare (1.45%), which are withheld from wages separately from income tax. "Take-home" is salary minus federal income tax and FICA, before state tax and any pre-tax benefits such as 401(k) contributions.</p>

<h2 id="married">Married filing jointly</h2>
<?= $table('mfj') ?>
<p>These figures assume the salary is the couple's combined wages and they take the <?= money($Y['std']['mfj']) ?> joint standard deduction. Compare the two tables: at <?= money(75000) ?>, a married couple pays <?= money($rows['mfj'][75000]['tax']) ?> versus <?= money($rows['single'][75000]['tax']) ?> for a single filer. Heads of household fall in between, with a <?= money($Y['std']['hoh']) ?> standard deduction and wider brackets than single filers.</p>

<h2 id="how-it-works">How federal income tax is calculated</h2>
<div class="formula">Gross income − adjustments = Adjusted gross income (AGI)<br>AGI − standard (or itemized) deduction − other deductions = Taxable income<br>Tax on taxable income from the brackets − credits = Federal income tax</div>
<ol>
<li><strong>Start with gross income</strong>: wages, self-employment profit, interest, dividends, capital gains, retirement distributions and so on.</li>
<li><strong>Subtract adjustments</strong> such as traditional 401(k) contributions (already excluded from W-2 Box 1), deductible IRA and HSA contributions, half of self-employment tax and student loan interest. The result is AGI.</li>
<li><strong>Subtract the standard deduction</strong> (or itemized deductions if larger). For <?= TAX_YEAR ?> that is <?= money($Y['std']['single']) ?> single, <?= money($Y['std']['mfj']) ?> married filing jointly and <?= money($Y['std']['hoh']) ?> head of household. You may also qualify for the new deductions described below.</li>
<li><strong>Apply the tax brackets</strong> to the remaining taxable income.</li>
<li><strong>Subtract credits</strong>, such as the child tax credit, which reduce tax dollar for dollar.</li>
</ol>

<h2 id="brackets">The 2026 tax brackets</h2>
<p>The U.S. uses a progressive system: each rate applies only to the slice of taxable income inside its bracket. These are the <?= TAX_YEAR ?> brackets for single filers:</p>
<?= bracket_table('single') ?>
<p>And for married couples filing jointly:</p>
<?= bracket_table('mfj') ?>

<h2 id="worked-example">Worked example: $75,000 salary, single</h2>
<p>Here is the full calculation for a single filer earning <?= money(75000) ?> in wages:</p>
<div class="table-wrap"><table><tbody>
<tr><td>Salary</td><td class="n"><?= money($ex['gross']) ?></td></tr>
<tr><td>Standard deduction</td><td class="n">−<?= money($ex['std']) ?></td></tr>
<tr><td><b>Taxable income</b></td><td class="n"><b><?= money($ex['taxable']) ?></b></td></tr>
<?php foreach ($ex['layers'] as $l): if ($l['amount'] <= 0) continue; ?>
<tr><td><?= round($l['rate'] * 100) ?>% on <?= money($l['amount']) ?> (<?= money($l['from']) ?> – <?= money(min($l['to'], $ex['taxable'])) ?>)</td><td class="n"><?= money($l['tax'], 2) ?></td></tr>
<?php endforeach; ?>
<tr><td><b>Federal income tax</b></td><td class="n"><b><?= money($ex['tax'], 2) ?></b></td></tr>
<tr><td>Effective rate (tax ÷ salary)</td><td class="n"><?= $pct($ex['effective']) ?></td></tr>
<tr><td>Marginal rate (rate on the next dollar)</td><td class="n"><?= $pct($ex['marginal'], 0) ?></td></tr>
</tbody></table></div>
<p>Even though this person is "in the <?= round($ex['marginal'] * 100) ?>% bracket," only the top <?= money($top_slice) ?> of taxable income is taxed at <?= round($ex['marginal'] * 100) ?>%. Their tax is <?= $pct($ex['effective']) ?> of salary. See the full page for <a href="/calculators/federal-income-tax/75000/">federal tax on $75,000</a> for paycheck-level detail.</p>

<h2 id="effective-marginal">Effective vs. marginal tax rate</h2>
<p>Your <strong>marginal rate</strong> is the rate on your next dollar of taxable income, which matters for decisions like a raise, a bonus or a 401(k) contribution. Your <strong>effective rate</strong> is total income tax divided by income, which tells you what share of your pay actually goes to federal income tax. Because of the standard deduction and the lower brackets, the effective rate is always well below the marginal rate.</p>
<div class="callout"><?= icon('spark') ?><p><strong>A raise never lowers your take-home pay because of brackets.</strong> Moving into a higher bracket only changes the tax on the dollars inside that bracket. What can reduce benefits at certain incomes are phase-outs of credits and deductions, not the brackets themselves.</p></div>

<h2 id="what-changes">What can change your federal tax</h2>
<ul>
<li><strong>Pre-tax retirement contributions.</strong> A traditional 401(k) deferral of up to <?= money($Y['k401']) ?> for <?= TAX_YEAR ?> lowers taxable income dollar for dollar. At a <?= $pct($rows['single'][75000]['marginal'], 0) ?> marginal rate, each $1,000 contributed cuts federal tax by about <?= money(1000 * $rows['single'][75000]['marginal']) ?>.</li>
<li><strong>Child tax credit.</strong> Up to <?= money($Y['ctc']['amount']) ?> per qualifying child for <?= TAX_YEAR ?>, with up to <?= money($Y['ctc']['refundable']) ?> refundable, phasing out above <?= money($Y['ctc']['phaseStart']['single']) ?> of AGI (<?= money($Y['ctc']['phaseStart']['mfj']) ?> joint).</li>
<li><strong>New OBBBA deductions (2025–2028).</strong> Up to <?= money($Y['tipsMax']) ?> of qualified tips, up to <?= money($Y['overtimeMax']['single']) ?> of qualified overtime premium pay (<?= money($Y['overtimeMax']['mfj']) ?> joint), and an extra <?= money($Y['senior']['amount']) ?> deduction for each taxpayer age 65 or older, each phasing out at higher incomes and available even if you take the standard deduction.</li>
<li><strong>Itemized deductions.</strong> Mortgage interest, charitable gifts and state and local taxes (capped at <?= money($Y['saltCap']) ?> for <?= TAX_YEAR ?>) help only if they exceed your standard deduction.</li>
<li><strong>Other income.</strong> Long-term capital gains and qualified dividends use separate 0%/15%/20% rates (<a href="/calculators/capital-gains-tax/">capital gains tax calculator</a>). Freelance income adds self-employment tax on top of income tax (<a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>).</li>
</ul>

<h2 id="withholding">Will I owe or get a refund?</h2>
<p>Federal income tax is usually paid through withholding from each paycheck, shown in Box 2 of your W-2. Whether you get a refund depends on whether that withholding was more or less than the tax calculated above. If your situation changed (a second job, a new child, side income), update your Form W-4. The <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> compares your withholding with your projected tax, and the <a href="/calculators/paycheck-calculator/">paycheck calculator</a> shows the effect per check. Our guide to <a href="/blog/understanding-your-w-2/">understanding your W-2</a> explains where each number comes from.</p>
<p>If you have income without withholding, you may need to pay during the year instead; see <a href="/blog/quarterly-taxes-101-guide/">Quarterly Taxes 101</a>.</p>

<h2 id="more-salaries">Federal tax at other salaries</h2>
<p>Breakdown pages for more incomes, each with single and married figures:</p>
<ul class="pill-links">
<?php foreach (SALARY_PAGES as $amt): ?>
<li><a href="/calculators/federal-income-tax/<?= $amt ?>/"><?= money($amt) ?></a></li>
<?php endforeach; ?>
</ul>

<?= faq_block([
  ['How much federal tax do I pay on $50,000 in 2026?', '<p>A single filer earning $50,000 in wages and taking the standard deduction pays about ' . money($rows['single'][50000]['tax']) . ' in federal income tax for 2026, an effective rate of ' . $pct($rows['single'][50000]['effective']) . '. A married couple filing jointly with the same income pays about ' . money($rows['mfj'][50000]['tax']) . '. Social Security and Medicare add another ' . money($rows['single'][50000]['fica']) . '.</p>'],
  ['How much federal tax do I pay on $100,000?', '<p>For 2026, a single filer with $100,000 of wages pays about ' . money($rows['single'][100000]['tax']) . ' in federal income tax (' . $pct($rows['single'][100000]['effective']) . ' effective, ' . $pct($rows['single'][100000]['marginal'], 0) . ' marginal). Married filing jointly, the same income owes about ' . money($rows['mfj'][100000]['tax']) . '.</p>'],
  ['What percentage of my paycheck goes to federal taxes?', '<p>It depends on income and filing status. In the examples above, federal income tax takes ' . $pct($rows['single'][30000]['effective']) . ' to ' . $pct($rows['single'][150000]['effective']) . ' of salary for single filers between $30,000 and $150,000, and FICA adds 7.65% on wages up to the Social Security wage base.</p>'],
  ['What is the standard deduction for 2026?', '<p>For 2026 the standard deduction is ' . money($Y['std']['single']) . ' for single filers and married filing separately, ' . money($Y['std']['mfj']) . ' for married filing jointly and ' . money($Y['std']['hoh']) . ' for heads of household. Taxpayers 65 or older or blind get an additional amount.</p>'],
  ['Does being in the 22% bracket mean I pay 22% of my income?', '<p>No. Only the portion of taxable income inside the 22% bracket is taxed at 22%. Lower slices are taxed at 10% and 12%, and the standard deduction is not taxed at all, so your overall effective rate is much lower.</p>'],
  ['Do these examples include state tax?', '<p>No. They show federal income tax and FICA only. Most states also tax wages, at rates that vary by state; a few have no wage income tax.</p>'],
]) ?>
<?= post_close($SLUG, 'federal-income-tax', ['understanding-your-w-2', 'quarterly-taxes-101-guide', 'do-i-have-to-pay-quarterly-taxes-my-first-year']) ?>
