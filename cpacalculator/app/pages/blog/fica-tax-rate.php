<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$Yp = $TAX['years'][(string) (TAX_YEAR - 1)];
$base = $Y['ssWageBase']; $base_prev = $Yp['ssWageBase'];
$amT = $Y['addlMedicare'];
/* FICA on wages for a single filer (employer withholds 0.9% on wages over $200,000 regardless of status). */
$fica = function (float $w) use ($base, $amT): array {
  $ss = min($w, $base) * 0.062;
  $med = $w * 0.0145;
  $addl = max(0, $w - $amT['single']) * 0.009;
  $er = $ss + $med; /* employer matches 6.2% + 1.45%, not the 0.9% */
  return ['w' => $w, 'ss' => $ss, 'med' => $med, 'addl' => $addl, 'ee' => $ss + $med + $addl, 'er' => $er, 'rate' => ($ss + $med + $addl) / $w];
};
$ex = array_map($fica, [50000, 150000, 250000]);
/* Self-employed example: $100,000 net profit. */
$se_net = 100000; $se_base = $se_net * 0.9235;
$se_ss = min($se_base, $base) * 0.124; $se_med = $se_base * 0.029; $se = $se_ss + $se_med;
/* Two-employer excess Social Security example. */
$j1 = 120000; $j2 = 90000;
$withheld = ($j1 + $j2) * 0.062; $max_ss = $base * 0.062; $excess = $withheld - $max_ss;
$pct = fn(float $x, int $dp = 2): string => number_format($x * 100, $dp) . '%';
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">The FICA tax rate for <?= TAX_YEAR ?> is <strong>7.65%</strong> of wages for employees: 6.2% for Social Security on wages up to <?= money($base) ?>, plus 1.45% for Medicare on all wages. Your employer pays a matching 7.65%, and high earners pay an extra 0.9% Additional Medicare tax that the employer does not match. Self-employed people pay both halves, 15.3%. This guide explains each piece, the Medicare tax rate, how the wage cap works, and how to get excess Social Security tax back if you had more than one job.</p>

<div class="callout"><?= icon('wallet') ?><p><strong>See it on your paycheck:</strong> the <a href="/calculators/paycheck-calculator/">paycheck calculator</a> shows Social Security, Medicare and federal income tax withholding per pay period, including the switch-off when you pass the <?= money($base) ?> wage base.</p></div>

<h2 id="what-is-fica">What is FICA tax?</h2>
<p>FICA stands for the Federal Insurance Contributions Act, the law that funds Social Security and Medicare through payroll taxes. It is separate from federal income tax: FICA is a flat percentage of wages, with no standard deduction and no brackets, and it shows up on your pay stub as two lines, usually labeled "Social Security" (or OASDI) and "Medicare." On your W-2, Box 4 shows Social Security tax withheld and Box 6 shows Medicare tax withheld.</p>

<h2 id="rates">FICA tax rate for <?= TAX_YEAR ?></h2>
<div class="table-wrap"><table>
<caption class="sr-only"><?= TAX_YEAR ?> FICA tax rates</caption>
<thead><tr><th>Tax</th><th class="n">Employee</th><th class="n">Employer</th><th class="n">Self-employed</th><th>Applies to</th></tr></thead>
<tbody>
<tr><td>Social Security (OASDI)</td><td class="n">6.2%</td><td class="n">6.2%</td><td class="n">12.4%</td><td>Wages up to <?= money($base) ?></td></tr>
<tr><td>Medicare (HI)</td><td class="n">1.45%</td><td class="n">1.45%</td><td class="n">2.9%</td><td>All wages, no cap</td></tr>
<tr><td>Additional Medicare</td><td class="n">0.9%</td><td class="n">None</td><td class="n">0.9%</td><td>Wages or SE income above <?= money($amT['single']) ?> single / <?= money($amT['mfj']) ?> joint</td></tr>
<tr class="total"><td><b>Total (below the wage base)</b></td><td class="n"><b>7.65%</b></td><td class="n"><b>7.65%</b></td><td class="n"><b>15.3%</b></td><td></td></tr>
</tbody></table></div>
<p>The 6.2% and 1.45% rates have been unchanged for decades. What changes every year is the Social Security wage base, which is indexed to national average wage growth.</p>

<h3 id="wage-base">The Social Security wage base</h3>
<div class="table-wrap"><table>
<caption class="sr-only">Social Security wage base by year</caption>
<thead><tr><th>Year</th><th class="n">Wage base</th><th class="n">Maximum employee Social Security tax</th></tr></thead>
<tbody>
<tr><td><?= TAX_YEAR ?></td><td class="n"><?= money($base) ?></td><td class="n"><?= money($base * 0.062, 2) ?></td></tr>
<tr><td><?= TAX_YEAR - 1 ?></td><td class="n"><?= money($base_prev) ?></td><td class="n"><?= money($base_prev * 0.062, 2) ?></td></tr>
</tbody></table></div>
<p>Once your wages for the year pass the wage base, your employer stops withholding Social Security tax for the rest of the year, so your take-home pay rises in the last paychecks of the year. Medicare tax never stops.</p>

<h2 id="medicare-tax-rate">Medicare tax rate and the Additional Medicare tax</h2>
<p>The regular Medicare tax rate is 1.45% for employees and 1.45% for employers, on every dollar of wages. On top of that, the <strong>Additional Medicare tax</strong> of 0.9% applies to wages and self-employment income above these thresholds, which are set in law and are not adjusted for inflation:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Additional Medicare tax thresholds</caption>
<thead><tr><th>Filing status</th><th class="n">Threshold</th></tr></thead>
<tbody>
<tr><td>Single, head of household, qualifying surviving spouse</td><td class="n"><?= money($amT['single']) ?></td></tr>
<tr><td>Married filing jointly</td><td class="n"><?= money($amT['mfj']) ?></td></tr>
<tr><td>Married filing separately</td><td class="n"><?= money($amT['mfs']) ?></td></tr>
</tbody></table></div>
<p>Employers must begin withholding the extra 0.9% once your wages from that employer exceed <?= money($amT['single']) ?> in a year, regardless of your filing status, and they do not match it. The tax you actually owe is settled on <strong>Form 8959</strong> with your return. That can create surprises in both directions: a married couple each earning <?= money(150000) ?> has no Additional Medicare withheld but owes it on the <?= money(300000 - $amT['mfj']) ?> above the <?= money($amT['mfj']) ?> joint threshold, while a single filer with one <?= money(220000) ?> job has the right amount withheld automatically.</p>
<p>Investment income is not subject to FICA, but higher-income taxpayers may owe the separate 3.8% net investment income tax, which uses the same thresholds.</p>

<h2 id="examples">FICA tax examples at <?= money(50000) ?>, <?= money(150000) ?> and <?= money(250000) ?></h2>
<p>Here is what an employee filing single pays in FICA at three salaries in <?= TAX_YEAR ?>, along with the employer's matching share:</p>
<div class="table-wrap"><table>
<caption class="sr-only"><?= TAX_YEAR ?> FICA tax examples</caption>
<thead><tr><th>Wages</th><th class="n">Social Security 6.2%</th><th class="n">Medicare 1.45%</th><th class="n">Add'l Medicare 0.9%</th><th class="n">Employee total</th><th class="n">Effective rate</th><th class="n">Employer pays</th></tr></thead>
<tbody>
<?php foreach ($ex as $r): ?>
<tr><td><b><?= money($r['w']) ?></b></td><td class="n"><?= money($r['ss'], 2) ?></td><td class="n"><?= money($r['med'], 2) ?></td><td class="n"><?= money($r['addl'], 2) ?></td><td class="n"><?= money($r['ee'], 2) ?></td><td class="n"><?= $pct($r['rate']) ?></td><td class="n"><?= money($r['er'], 2) ?></td></tr>
<?php endforeach; ?>
</tbody></table></div>
<ul>
<li><strong><?= money(50000) ?>:</strong> straightforward 7.65%, or <?= money($ex[0]['ee'], 2) ?> for the year.</li>
<li><strong><?= money(150000) ?>:</strong> still under the wage base, so the full 7.65% applies: <?= money($ex[1]['ee'], 2) ?>.</li>
<li><strong><?= money(250000) ?>:</strong> Social Security tax stops at <?= money($base * 0.062, 2) ?> because only the first <?= money($base) ?> is taxed, Medicare continues on all <?= money(250000) ?>, and the 0.9% Additional Medicare tax applies to the <?= money(250000 - $amT['single']) ?> above <?= money($amT['single']) ?>. The effective FICA rate drops to <?= $pct($ex[2]['rate']) ?>.</li>
</ul>
<p>Note that pre-tax 401(k) deferrals reduce wages for income tax but <em>not</em> for FICA; Box 3 and Box 5 of your W-2 are usually higher than Box 1 for that reason. Health insurance premiums and HSA contributions made through a cafeteria plan, by contrast, are generally exempt from FICA too. Our guide to <a href="/blog/understanding-your-w-2/">understanding your W-2</a> walks through those boxes.</p>

<div class="callout warn"><?= icon('shield') ?><p><strong>The new tips and overtime deductions do not cut FICA.</strong> The OBBBA deductions for qualified tips and overtime pay (2025 through 2028) reduce federal <em>income</em> tax only. Tips and overtime remain fully subject to Social Security and Medicare tax.</p></div>

<h2 id="self-employed">FICA tax rate for the self-employed: 15.3%</h2>
<p>If you work for yourself, there is no employer to pay the other half, so you pay both through <strong>self-employment tax</strong> on Schedule SE. The rate is 15.3% (12.4% Social Security plus 2.9% Medicare), applied to 92.35% of your net self-employment earnings. The 92.35% factor mirrors the fact that employees do not pay FICA on the employer's share.</p>
<p>For example, <?= money($se_net) ?> of net profit gives <?= money($se_base) ?> of net earnings subject to the tax. Social Security tax is <?= money($se_ss, 2) ?> and Medicare tax is <?= money($se_med, 2) ?>, for total self-employment tax of <?= money($se, 2) ?>. You then deduct half of that, <?= money($se / 2, 2) ?>, as an adjustment to income. If you also have W-2 wages, those wages use up part of the Social Security wage base first. The <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> handles all of this, and <a href="/blog/1099-vs-w2/">1099 vs W-2</a> compares the two arrangements in detail.</p>

<h2 id="excess-ss">Too much Social Security withheld? Getting a refund</h2>
<p>Each employer withholds Social Security tax independently, up to the wage base, without knowing what your other employers paid you. If you changed jobs or worked two jobs and your combined wages exceeded <?= money($base) ?>, you will have too much withheld.</p>
<p>Say you earned <?= money($j1) ?> from one employer and <?= money($j2) ?> from another in <?= TAX_YEAR ?>. Together they withheld <?= money($withheld, 2) ?> of Social Security tax, but the most anyone owes is <?= money($max_ss, 2) ?>. You claim the <strong><?= money($excess, 2) ?></strong> difference as a credit on <strong>Schedule 3 (Form 1040)</strong>, on the line for excess Social Security and tier 1 RRTA tax withheld. It reduces your tax or increases your refund; you can preview the effect with the <a href="/calculators/tax-refund-calculator/">tax refund calculator</a>.</p>
<ul>
<li>This credit works only when the excess comes from <strong>two or more employers</strong>. If a single employer withheld too much, ask that employer to refund it and issue a corrected W-2 (Form W-2c).</li>
<li>Married couples calculate the limit separately for each spouse. You cannot combine one spouse's excess with the other's shortfall.</li>
<li>There is no refund for "excess" Medicare tax, because Medicare has no wage cap. Extra Additional Medicare withholding, however, is credited when you file Form 8959.</li>
</ul>

<h2 id="exemptions">Who is exempt from FICA tax?</h2>
<p>A few groups do not pay FICA on some or all of their earnings:</p>
<ul>
<li><strong>Students working for their school.</strong> Students enrolled and regularly attending classes at a college or university are generally exempt on wages from that same school (the "student FICA exception"). Full-time employees and some medical residents do not qualify.</li>
<li><strong>Certain nonresident aliens.</strong> Students, scholars, teachers and researchers in F-1, J-1, M-1 or Q status are generally exempt on wages for work allowed by their visa while they remain nonresident aliens for tax purposes.</li>
<li><strong>Members of certain religious groups.</strong> Members of recognized religious sects that conscientiously oppose public insurance (such as some Amish and Mennonite communities) can apply for exemption on Form 4029, and qualifying ministers can apply for exemption from self-employment tax on ministerial earnings using Form 4361.</li>
<li><strong>Children working for a parent.</strong> Wages paid to a child under 18 by a parent's sole proprietorship (or a partnership owned only by the parents) are exempt from FICA.</li>
<li><strong>Some government employees.</strong> Certain state and local government workers covered by a public retirement system instead of Social Security are exempt from the 6.2% Social Security tax, though most still pay Medicare tax.</li>
</ul>
<p>If you think FICA was withheld in error, ask the employer for a refund first. If that fails, you can request one from the IRS on Form 843.</p>

<?= faq_block([
  ['What is the FICA tax rate for 2026?', '<p>The FICA tax rate for ' . TAX_YEAR . ' is 7.65% for employees: 6.2% Social Security on wages up to ' . money($base) . ' and 1.45% Medicare on all wages. Employers pay a matching 7.65%. An extra 0.9% Additional Medicare tax applies to wages above ' . money($amT['single']) . ' (single) or ' . money($amT['mfj']) . ' (married filing jointly), with no employer match.</p>'],
  ['What is the Medicare tax rate?', '<p>The Medicare tax rate is 1.45% for employees and 1.45% for employers on all wages, or 2.9% for the self-employed. Earnings above ' . money($amT['single']) . ' for single filers, ' . money($amT['mfj']) . ' for joint filers or ' . money($amT['mfs']) . ' for married filing separately also owe the 0.9% Additional Medicare tax, for a top employee rate of 2.35%.</p>'],
  ['What is the maximum Social Security tax for 2026?', '<p>Social Security tax applies only to the first ' . money($base) . ' of wages in ' . TAX_YEAR . ', so the most an employee pays is ' . money($base * 0.062, 2) . '. For ' . (TAX_YEAR - 1) . ', the wage base was ' . money($base_prev) . ' and the maximum was ' . money($base_prev * 0.062, 2) . '. Medicare tax has no maximum.</p>'],
  ['Why is FICA so high on my paycheck?', '<p>FICA takes a flat 7.65% from the first dollar you earn, with no standard deduction, so for many lower and middle-income workers it is larger than their federal income tax withholding. It also applies to 401(k) deferrals, which reduce income tax but not FICA.</p>'],
  ['Can I get FICA taxes refunded?', '<p>You can recover excess Social Security tax if two or more employers together withheld more than ' . money($base * 0.062, 2) . ' in ' . TAX_YEAR . ', by claiming a credit on Schedule 3 of Form 1040. If one employer over-withheld or withheld FICA you were exempt from, ask that employer for a refund and corrected W-2, or file Form 843 if the employer will not fix it.</p>'],
  ['Do self-employed people pay FICA?', '<p>Not under that name. Self-employed people pay self-employment tax at 15.3% (12.4% Social Security plus 2.9% Medicare) on 92.35% of net earnings, plus the 0.9% Additional Medicare tax above the thresholds. Half of self-employment tax is deductible.</p>'],
]) ?>
<?= post_close($SLUG, 'paycheck-calculator', ['understanding-your-w-2', '1099-vs-w2', 'bonus-tax-rate']) ?>
