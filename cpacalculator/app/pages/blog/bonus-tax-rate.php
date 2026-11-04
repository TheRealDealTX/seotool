<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$pct = fn(float $x, int $dp = 1): string => number_format($x * 100, $dp) . '%';
/* Bonus example: single filer, salary + bonus, standard deduction. Withholding = 22% flat + FICA; actual = change in fed tax. */
$bonus = function (float $salary, float $b) use ($Y): array {
  $before = fed_tax(max(0, $salary - $Y['std']['single']), 'single')['tax'];
  $after = fed_tax(max(0, $salary + $b - $Y['std']['single']), 'single')['tax'];
  $ss = max(0, min($salary + $b, $Y['ssWageBase']) - min($salary, $Y['ssWageBase'])) * 0.062;
  $med = $b * 0.0145 + max(0, $salary + $b - max($salary, $Y['addlMedicare']['single'])) * 0.009;
  $wh = $b * 0.22;
  $actual = $after - $before;
  return ['salary' => $salary, 'bonus' => $b, 'wh' => $wh, 'actual' => $actual, 'rate' => $b > 0 ? $actual / $b : 0, 'diff' => $wh - $actual,
    'fica' => $ss + $med, 'net' => $b - $wh - $ss - $med];
};
$b5 = $bonus(70000, 5000);
$b20 = $bonus(70000, 20000);
$contrast = [$bonus(40000, 5000), $b5, $b20, $bonus(150000, 20000), $bonus(240000, 20000)];
/* Simplified aggregate method: biweekly salary + bonus annualized; standard deduction stands in for the Pub 15-T adjustment. */
$per = 70000 / 26;
$reg_wh = fed_tax(max(0, $per * 26 - $Y['std']['single']), 'single')['tax'] / 26;
$agg_wh = fed_tax(max(0, ($per + 5000) * 26 - $Y['std']['single']), 'single')['tax'] / 26 - $reg_wh;
/* Million-dollar example. */
$big = 1500000;
$big_wh = 1000000 * 0.22 + ($big - 1000000) * 0.37;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">Calculating tax on bonus pay trips people up because two different numbers are involved: what your employer <em>withholds</em> from the bonus check, and what you actually <em>owe</em> on it when you file. For <?= TAX_YEAR ?>, the federal bonus tax rate for withholding is a flat 22% (37% on supplemental wages over $1 million), plus Social Security and Medicare. Your real tax on the bonus is your marginal rate, which may be higher or lower. This guide explains both, with worked examples.</p>

<div class="callout"><?= icon('wallet') ?><p><strong>Quick answer:</strong> on a <?= money(5000) ?> bonus for someone earning <?= money(70000) ?>, expect about <?= money($b5['wh']) ?> of federal income tax withholding (22%) and <?= money($b5['fica']) ?> of FICA, leaving roughly <?= money($b5['net']) ?> before state tax. Bonuses are not taxed at a higher rate than salary; they are just withheld differently. See your per-check result in the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>.</p></div>

<h2 id="bonus-tax-rate">What is the bonus tax rate in 2026?</h2>
<p>The IRS treats bonuses as <strong>supplemental wages</strong>, the same category as commissions, overtime paid separately, severance, back pay, awards and prizes. Employers have two approved ways to withhold federal income tax on them:</p>
<div class="table-wrap"><table>
<thead><tr><th>Supplemental wages paid in the year</th><th>Federal income tax withholding</th></tr></thead>
<tbody>
<tr><td>Up to $1,000,000</td><td>22% flat (percentage method) <em>or</em> aggregate method, employer's choice</td></tr>
<tr><td>Above $1,000,000</td><td>37% mandatory on the excess, regardless of Form W-4</td></tr>
</tbody></table></div>
<p>Both rates match tax brackets: 22% is the third bracket and 37% the top one. The One Big Beautiful Bill Act (OBBBA) made the current bracket structure permanent, so the 22% and 37% supplemental rates continue for <?= TAX_YEAR ?> and beyond. On top of income tax, bonuses carry the same FICA taxes as regular pay and usually state income tax.</p>
<p>For example, a <?= money($big) ?> bonus would have <?= money(1000000 * 0.22) ?> withheld on the first $1 million (22%) and <?= money(($big - 1000000) * 0.37) ?> on the remaining <?= money($big - 1000000) ?> (37%), for <?= money($big_wh) ?> of federal income tax withholding before FICA. The $1 million counts all supplemental wages from the same employer during the calendar year, not each check separately.</p>

<h2 id="methods">Percentage method vs aggregate method</h2>
<p><strong>Percentage (flat-rate) method.</strong> If the bonus is paid separately from your regular wages, or identified separately on the same check, the employer can simply withhold 22%. This option is available only if income tax was withheld from your regular wages in the current or prior year. It ignores your W-4 entirely, which is why it is the most common method.</p>
<p><strong>Aggregate method.</strong> The employer adds the bonus to your regular wages for the pay period, calculates withholding on the total as if it were a normal paycheck, then subtracts what it would have withheld from the regular wages alone. Because payroll software assumes you earn that inflated amount every period, the aggregate method can withhold more than 22% on a large bonus.</p>
<p>Simplified illustration: a single employee paid <?= money($per, 2) ?> every two weeks receives a <?= money(5000) ?> bonus in the same check. Annualized, that period looks like <?= money(($per + 5000) * 26) ?> of salary. Withholding on the combined check, minus regular withholding, comes to about <?= money($agg_wh) ?> on the bonus, an effective <?= $pct($agg_wh / 5000) ?>. (Actual payroll uses the IRS Publication 15-T tables, so your employer's figure will differ somewhat.)</p>
<div class="formula">Percentage method: bonus × 22% (37% above $1M)<br>Aggregate method: withholding on (regular pay + bonus) − withholding on regular pay alone</div>

<h2 id="fica">Social Security, Medicare and state tax on a bonus</h2>
<ul>
<li><strong>Social Security:</strong> 6.2% until your total <?= TAX_YEAR ?> wages from that employer reach <?= money($Y['ssWageBase']) ?>. If your salary already exceeds the wage base, the bonus owes no Social Security.</li>
<li><strong>Medicare:</strong> 1.45% on the full bonus, plus 0.9% Additional Medicare withholding on wages above <?= money($Y['addlMedicare']['single']) ?> from one employer in the year.</li>
<li><strong>State income tax:</strong> states that tax wages handle bonuses in different ways. Some publish a flat supplemental withholding rate, some require the aggregate method, and states without a wage income tax withhold nothing. Check your state revenue department's employer withholding guide.</li>
<li><strong>Local tax:</strong> cities and counties with a wage tax generally apply it to bonuses as well.</li>
</ul>
<p>Read more about payroll taxes in our <a href="/blog/fica-tax-rate/">FICA tax rate guide</a>.</p>

<h2 id="calculating-tax-on-bonus">Calculating tax on bonus pay: withholding vs actual tax</h2>
<p>Withholding is just a prepayment. When you file, the bonus is added to your other wages in Box 1 of your <a href="/blog/understanding-your-w-2/">W-2</a> and taxed at your ordinary rates. The real tax on a bonus is the difference between your federal tax with and without it. Here are two examples for a single filer earning <?= money(70000) ?> with the <?= money($Y['std']['single']) ?> standard deduction:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Federal tax on a bonus for a $70,000 salary, <?= TAX_YEAR ?>, single</caption>
<thead><tr><th></th><th class="n"><?= money(5000) ?> bonus</th><th class="n"><?= money(20000) ?> bonus</th></tr></thead>
<tbody>
<tr><td>Federal withholding at 22%</td><td class="n"><?= money($b5['wh']) ?></td><td class="n"><?= money($b20['wh']) ?></td></tr>
<tr><td>Social Security + Medicare</td><td class="n"><?= money($b5['fica']) ?></td><td class="n"><?= money($b20['fica']) ?></td></tr>
<tr><td><b>Bonus after federal withholding and FICA</b></td><td class="n"><b><?= money($b5['net']) ?></b></td><td class="n"><b><?= money($b20['net']) ?></b></td></tr>
<tr><td>Actual added federal income tax at filing</td><td class="n"><?= money($b5['actual']) ?></td><td class="n"><?= money($b20['actual']) ?></td></tr>
<tr><td>Actual rate on the bonus</td><td class="n"><?= $pct($b5['rate']) ?></td><td class="n"><?= $pct($b20['rate']) ?></td></tr>
<tr><td>Over (under) withheld</td><td class="n"><?= money($b5['diff']) ?></td><td class="n"><?= money($b20['diff']) ?></td></tr>
</tbody></table></div>
<p>At <?= money(70000) ?>, taxable income before the bonus is <?= money(70000 - $Y['std']['single']) ?>, already inside the 22% bracket, and both bonuses stay within it. So the 22% withholding matches the actual tax exactly. That is not true at every income. The same calculation at other salaries:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Bonus withholding vs actual federal tax at different salaries</caption>
<thead><tr><th>Salary</th><th class="n">Bonus</th><th class="n">Withheld (22%)</th><th class="n">Actual tax</th><th class="n">Actual rate</th><th class="n">Over (under)</th></tr></thead>
<tbody>
<?php foreach ($contrast as $r): ?>
<tr><td><?= money($r['salary']) ?></td><td class="n"><?= money($r['bonus']) ?></td><td class="n"><?= money($r['wh']) ?></td><td class="n"><?= money($r['actual']) ?></td><td class="n"><?= $pct($r['rate']) ?></td><td class="n"><?= money($r['diff']) ?></td></tr>
<?php endforeach; ?>
</tbody></table></div>
<p>Lower earners in the 12% bracket are over-withheld and get the excess back as part of their refund. Higher earners in the 24%, 32% or higher brackets are under-withheld and owe the difference at tax time, which surprises people who assume the 22% was the whole bill. If that describes you, increase withholding on your W-4 or set money aside. The <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> shows whether your total withholding will cover your bill.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>A bonus cannot push all your income into a higher bracket.</strong> Only the dollars above a bracket threshold are taxed at the higher rate. If a bonus crosses from 22% into 24%, only the part above the line is taxed at 24%. Your take-home pay always goes up with a bonus.</p></div>

<h2 id="step-by-step">Calculating tax on bonus checks, step by step</h2>
<ol>
<li><strong>Federal withholding.</strong> Multiply the bonus by 22% (or check your pay stub if your employer uses the aggregate method).</li>
<li><strong>Social Security.</strong> 6.2% of the bonus, but only on the part that keeps your year-to-date wages under <?= money($Y['ssWageBase']) ?>.</li>
<li><strong>Medicare.</strong> 1.45% of the bonus, plus 0.9% on any wages above <?= money($Y['addlMedicare']['single']) ?>.</li>
<li><strong>State and local.</strong> Apply your state's supplemental rate or regular withholding.</li>
<li><strong>Pre-tax deductions.</strong> If your plan lets you defer part of a bonus into a 401(k), that portion is not subject to federal income tax withholding (FICA still applies).</li>
<li><strong>Check the true cost.</strong> Find your marginal rate with the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> and compare it with 22% to see whether you will owe or get money back.</li>
</ol>
<p>For a broader look at how marginal and effective rates work at different incomes, see <a href="/blog/how-much-federal-tax-will-i-pay/">how much federal income tax will I pay</a>.</p>

<h2 id="reduce">Ways to reduce tax on a bonus</h2>
<ul>
<li><strong>Increase your 401(k) deferral</strong> for the bonus check, up to the <?= TAX_YEAR ?> employee limit of <?= money($Y['k401']) ?> (plus catch-up contributions if you are 50 or older).</li>
<li><strong>Fund an HSA</strong> through payroll if you have a qualifying high-deductible health plan; HSA contributions made through a cafeteria plan also avoid FICA.</li>
<li><strong>Ask about timing.</strong> Some employers let you choose whether a year-end bonus is paid in December or January, which can shift the income into a lower-income year.</li>
<li><strong>Bunch deductions.</strong> A large bonus year can be a good year for charitable gifts if you itemize.</li>
</ul>
<p>Bonuses do not qualify for the OBBBA deductions for qualified overtime or tips. Overtime premium pay may be deductible, but a discretionary or performance bonus is not overtime, even if it is paid alongside an overtime check.</p>

<h2 id="special-cases">Special cases</h2>
<ul>
<li><strong>Non-cash bonuses</strong> such as gift cards are taxable wages. Small, occasional non-cash gifts like a holiday ham can be a non-taxable de minimis fringe benefit, but cash and gift cards never are.</li>
<li><strong>Sign-on and retention bonuses</strong> are supplemental wages taxed the same way. If you must repay one after leaving, the tax treatment depends on whether you repay in the same year or a later year.</li>
<li><strong>Bonuses to 1099 contractors</strong> are just more business income. No tax is withheld; they are subject to income tax and self-employment tax. Use the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> instead.</li>
</ul>

<?= faq_block([
  ['How much tax is taken out of a bonus?', '<p>For ' . TAX_YEAR . ', most employers withhold a flat 22% for federal income tax (37% on supplemental wages over $1 million), plus 6.2% Social Security up to the wage base and 1.45% Medicare. A ' . money(5000) . ' bonus at a ' . money(70000) . ' salary typically nets about ' . money($b5['net']) . ' before state tax.</p>'],
  ['Are bonuses taxed at a higher rate?', '<p>No. Bonuses are often withheld at a different rate than regular pay, but when you file they are taxed at the same ordinary rates as salary. If 22% was more than your marginal rate, you get the difference back; if less, you owe it.</p>'],
  ['What is the formula for calculating tax on a bonus?', '<p>For withholding: bonus × 22% federal + bonus × 6.2% Social Security (up to the wage base) + bonus × 1.45% Medicare, plus state tax. When calculating tax on bonus pay for your actual bill at filing, compute your federal tax with and without the bonus; the difference is the real cost.</p>'],
  ['Why was my bonus taxed at 40% or more?', '<p>Federal 22% plus 7.65% FICA is already close to 30%, and state tax can add several more points. If your employer used the aggregate method, payroll may also have treated the bonus period as if you earned that amount every period, withholding at a higher bracket. Any excess comes back when you file.</p>'],
  ['Is a $1 million bonus taxed at 37%?', '<p>Only the portion of supplemental wages above $1 million in a calendar year is subject to mandatory 37% withholding. The first $1 million can be withheld at 22%.</p>'],
  ['Can I avoid taxes on my bonus by putting it in my 401(k)?', '<p>If your plan allows bonus deferrals, the amount you contribute to a traditional 401(k) avoids federal income tax now, up to the annual limit of ' . money($Y['k401']) . ' for ' . TAX_YEAR . '. Social Security and Medicare still apply.</p>'],
]) ?>
<?= post_close($SLUG, 'paycheck-calculator', ['how-much-federal-tax-will-i-pay', 'understanding-your-w-2', '1099-vs-w2']) ?>
