<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Paycheck Calculator $Y — Take Home Pay After Taxes | CPA Calculator";
$P['description'] = "Free $Y paycheck calculator. See take home pay per paycheck after federal withholding, Social Security, Medicare, 401(k), health insurance, HSA and state tax.";
$P['scripts'] = ['/assets/js/tools/paycheck-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Worked example mirroring the JS: salary, biweekly, 401(k) %, Section 125 health premium per check, W-4 defaults. */
function pay_example(float $salary, int $periods, float $k401Pct, float $healthPer, string $status = 'single'): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $k = $salary * $k401Pct / 100;
  $h = $healthPer * $periods;
  $fedWages = $salary - $k - $h;
  $ficaWages = $salary - $h;
  $fed = fed_tax(max(0, $fedWages - $y['std'][$status]), $status)['tax'];
  $ss = min($ficaWages, $y['ssWageBase']) * 0.062;
  $med = $ficaWages * 0.0145 + max(0, $ficaWages - 200000) * 0.009;
  $net = $salary - $k - $h - $fed - $ss - $med;
  return compact('k', 'h', 'fedWages', 'ficaWages', 'fed', 'ss', 'med', 'net') + ['gross' => $salary, 'n' => $periods];
}
$ex = pay_example(65000, 26, 5, 100);
$per = fn($x) => money($x / $ex['n'], 2);
$freqs = [['Weekly', 52], ['Biweekly (every two weeks)', 26], ['Semimonthly (twice a month)', 24], ['Monthly', 12]];

echo tool_hero('paycheck-calculator', "Paycheck Calculator $Y",
  "Find your take-home pay for every paycheck. Enter your salary or hourly rate, how often you’re paid and your deductions — 401(k), health insurance, HSA — to see federal withholding, Social Security, Medicare, optional state tax and net pay, per paycheck and per year.",
  ["$Y IRS withholding tables", 'Weekly to monthly pay', '401(k), HSA & benefits', 'Per-paycheck + annual view']);
?>
<section class="tool" aria-label="Paycheck calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="pay-form" novalidate>
        <?= year_field() ?>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Pay</legend>
          <div class="grid-2">
            <?= money_field('gross', 'Gross pay', 65000, 'Pay before any taxes or deductions. Choose below whether this is per year, per paycheck or per hour.') ?>
            <div class="field"><label for="f-basis">This amount is</label><select id="f-basis" name="basis"><option value="year">Per year (salary)</option><option value="period">Per paycheck</option><option value="hour">Per hour</option></select></div>
          </div>
          <div class="grid-2">
            <div class="field"><label for="f-freq">Pay frequency</label><select id="f-freq" name="freq">
              <option value="52">Weekly (52 paychecks)</option><option value="26" selected>Biweekly (26)</option><option value="24">Semimonthly (24)</option><option value="12">Monthly (12)</option><option value="1">Annually (1)</option>
            </select></div>
            <?= money_field('hours', 'Hours per week', 40, 'Only used when you enter an hourly rate.', '', '') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Pre-tax deductions</legend>
          <div class="grid-2">
            <?= money_field('k401', 'Traditional 401(k) / 403(b)', 5, 'Reduces federal (and most state) taxable wages, but not Social Security and Medicare. ' . $Y . ' limit: ' . money($y['k401']) . ' plus ' . money($y['k401CatchUp']) . ' catch-up at 50+.', '', '') ?>
            <div class="field"><label for="f-k401Type">401(k) entered as</label><select id="f-k401Type" name="k401Type"><option value="pct">% of gross pay</option><option value="amt">$ per paycheck</option></select></div>
          </div>
          <label class="check"><input type="checkbox" name="catchup"> I’m 50 or older (allow catch-up contributions)</label>
          <div class="grid-2">
            <?= money_field('health', 'Health & dental premiums per check', 100, 'Your share of employer health premiums taken pre-tax through a Section 125 cafeteria plan — exempt from income tax and FICA.') ?>
            <?= money_field('hsa', 'HSA / FSA per check', '', 'Payroll HSA and health FSA contributions are exempt from income tax and FICA. ' . $Y . ' HSA limit: ' . money($y['hsa']['self']) . ' self-only, ' . money($y['hsa']['family']) . ' family.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Other deductions &amp; state tax</legend>
          <div class="grid-2">
            <?= money_field('post', 'After-tax deductions per check', '', 'Roth 401(k), union dues, life insurance, wage garnishments, charitable payroll gifts — taken after taxes.') ?>
            <?= money_field('state', 'State income tax rate (flat)', '', 'Optional. Your state’s flat or approximate effective rate, applied to federal taxable wages. Leave blank for states with no income tax.', '', '%') ?>
          </div>
          <details class="more"><summary>W-4 settings (Steps 2–4)</summary>
            <label class="check"><input type="checkbox" name="step2"> Step 2 box checked (two jobs, or spouse also works)</label>
            <div class="grid-2">
              <?= money_field('dep', 'Step 3: dependent credits (annual)', '', 'Usually ' . money($y['ctc']['amount']) . ' per child under 17 plus $500 per other dependent.') ?>
              <?= money_field('otherInc', 'Step 4(a): other income (annual)', '', 'Non-job income you want withheld for, such as interest or dividends.') ?>
            </div>
            <div class="grid-2">
              <?= money_field('w4ded', 'Step 4(b): deductions (annual)', '', 'Deductions above the standard deduction you expect to claim.') ?>
              <?= money_field('extra', 'Step 4(c): extra withholding (per paycheck)', '', 'Additional federal tax you asked your employer to withhold each pay period.') ?>
            </div>
          </details>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Take-home pay per paycheck</div>
          <div class="res-big good" data-out="net">$0</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Annual take-home</small><b data-out="netA">$0</b></div>
            <div class="kpi"><small>Federal withholding</small><b data-out="fed">$0</b></div>
            <div class="kpi"><small>Social Security + Medicare</small><b data-out="fica">$0</b></div>
            <div class="kpi"><small>Total tax rate</small><b data-out="rate">0%</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your gross pay goes"></svg><ul class="legend" data-legend></ul></div>
          <div class="table-wrap" style="margin-top:0"><table>
            <caption class="sr-only">Paycheck breakdown per paycheck and per year</caption>
            <thead><tr><th>Item</th><th class="n">Per paycheck</th><th class="n">Annual</th></tr></thead>
            <tbody data-table></tbody>
          </table></div>
          <p class="note" data-out="note">Federal withholding follows the IRS percentage method for 2020-and-later W-4s, annualized. Actual paychecks can differ slightly due to rounding and employer setup. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use this paycheck calculator</h2>
      <ol>
        <li><strong>Enter your pay.</strong> Type your annual salary, the gross amount of one paycheck, or your hourly rate and weekly hours.</li>
        <li><strong>Choose your pay frequency and filing status.</strong> Use the filing status from your Form W-4 — it drives your federal withholding.</li>
        <li><strong>Add pre-tax deductions.</strong> Enter your traditional 401(k) as a percentage or a dollar amount per paycheck, plus health insurance premiums and payroll HSA contributions.</li>
        <li><strong>Optional extras.</strong> Add after-tax deductions such as Roth 401(k), a flat state income tax rate, and any W-4 adjustments (Step 2 checkbox, dependents, extra withholding).</li>
      </ol>
      <p>The results show net pay for one paycheck and for the full year, with every line broken out so you can match it to your pay stub.</p>

      <h2 id="how-calculated">How take-home pay is calculated</h2>
      <p>Your paycheck starts with gross pay and loses money in a fixed order. The key detail is that not every deduction reduces every tax:</p>
      <div class="formula">Federal taxable wages = gross − 401(k) − health premiums − HSA<br>FICA wages = gross − health premiums − HSA (401(k) does <em>not</em> reduce FICA)<br>Take-home = gross − pre-tax deductions − federal withholding − Social Security − Medicare − state tax − after-tax deductions</div>
      <div class="table-wrap"><table>
        <thead><tr><th>Deduction</th><th>Lowers federal income tax?</th><th>Lowers Social Security &amp; Medicare?</th></tr></thead><tbody>
        <tr><td>Traditional 401(k), 403(b), 457(b)</td><td>Yes</td><td>No</td></tr>
        <tr><td>Health, dental, vision premiums (Section 125)</td><td>Yes</td><td>Yes</td></tr>
        <tr><td>HSA or health FSA through payroll</td><td>Yes</td><td>Yes</td></tr>
        <tr><td>Roth 401(k), union dues, garnishments</td><td>No</td><td>No</td></tr>
      </tbody></table></div>

      <h2 id="federal-withholding">Federal income tax withholding</h2>
      <p>Employers figure withholding with the IRS percentage method in Publication 15-T. For a Form W-4 from 2020 or later, they annualize your taxable wages for the pay period, subtract an amount equal to the standard deduction for your W-4 filing status (<?= money($y['std']['single']) ?> single, <?= money($y['std']['mfj']) ?> married filing jointly, <?= money($y['std']['hoh']) ?> head of household in <?= $Y ?>), apply the tax brackets, subtract any Step 3 dependent credits and divide by the number of paychecks. This calculator does the same.</p>
      <ul>
        <li><strong>Step 2 checkbox</strong> — for two jobs or two working spouses. It splits the standard deduction and the brackets in half for each job, which withholds more.</li>
        <li><strong>Step 3</strong> — dependent credits reduce withholding dollar-for-dollar across the year.</li>
        <li><strong>Step 4</strong> — add other income, extra deductions or a flat extra amount per paycheck.</li>
      </ul>
      <p>Withholding is an estimate of your tax, not the tax itself. If your withholding runs higher than your actual liability you get a refund; lower and you owe. The <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> compares the two, and the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> shows your full-year liability.</p>

      <h2 id="fica">Social Security and Medicare (FICA)</h2>
      <p>Every paycheck has 6.2% withheld for Social Security on wages up to the <?= $Y ?> wage base of <?= money($y['ssWageBase']) ?>, and 1.45% for Medicare with no cap. Once your year-to-date wages pass <?= money($y['ssWageBase']) ?>, Social Security withholding stops for the rest of the year, so high earners see bigger checks late in the year (the calculator shows the yearly average). Employers also withhold an extra 0.9% Additional Medicare Tax on wages over $200,000 in a calendar year, regardless of filing status. Your employer pays a matching 7.65% that doesn’t come out of your check. If you’re self-employed, you pay both halves — see the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a>.</p>

      <h2 id="frequency">Pay frequency: weekly, biweekly, semimonthly or monthly</h2>
      <p>Your annual pay and taxes are the same however often you’re paid; only the slice per check changes. Biweekly pay gives 26 checks a year, so two months each year contain a third paycheck. Semimonthly pay gives 24 slightly larger checks.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Frequency</th><th class="n">Paychecks per year</th><th class="n">Gross per check on $65,000</th><th class="n">Take-home per check*</th></tr></thead><tbody>
<?php foreach ($freqs as [$label, $n]): ?>
        <tr><td><?= $label ?></td><td class="n"><?= $n ?></td><td class="n"><?= money(65000 / $n, 2) ?></td><td class="n"><?= money($ex['net'] / $n, 2) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p class="hint">*Single filer, 5% traditional 401(k) and <?= money($ex['h']) ?> a year of pre-tax health premiums, no state tax.</p>

      <h2 id="example">Worked example: $65,000 salary paid biweekly</h2>
      <p>A single employee earns $65,000 a year, paid every two weeks (26 checks), contributes 5% to a traditional 401(k) and pays $100 per paycheck for health insurance pre-tax.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Item</th><th class="n">Per paycheck</th><th class="n">Annual</th></tr></thead><tbody>
        <tr><td>Gross pay</td><td class="n"><?= $per($ex['gross']) ?></td><td class="n"><?= money($ex['gross']) ?></td></tr>
        <tr><td>401(k) (5%)</td><td class="n">−<?= $per($ex['k']) ?></td><td class="n">−<?= money($ex['k']) ?></td></tr>
        <tr><td>Health insurance (pre-tax)</td><td class="n">−<?= $per($ex['h']) ?></td><td class="n">−<?= money($ex['h']) ?></td></tr>
        <tr><td>Federal withholding (on <?= money($ex['fedWages']) ?> − <?= money($y['std']['single']) ?>)</td><td class="n">−<?= $per($ex['fed']) ?></td><td class="n">−<?= money($ex['fed']) ?></td></tr>
        <tr><td>Social Security (6.2% of <?= money($ex['ficaWages']) ?>)</td><td class="n">−<?= $per($ex['ss']) ?></td><td class="n">−<?= money($ex['ss']) ?></td></tr>
        <tr><td>Medicare (1.45%)</td><td class="n">−<?= $per($ex['med']) ?></td><td class="n">−<?= money($ex['med']) ?></td></tr>
        <tr><td><strong>Take-home pay</strong></td><td class="n"><strong><?= $per($ex['net']) ?></strong></td><td class="n"><strong><?= money($ex['net']) ?></strong></td></tr>
      </tbody></table></div>
      <p>Notice the 401(k) cut federal withholding but not Social Security and Medicare, while the health premium cut both. The 401(k) costs <?= $per($ex['k']) ?> per check in contributions but reduces take-home by less, because it also lowers federal tax.</p>

      <h2 id="by-salary">Take-home pay by salary (<?= $Y ?>, single, biweekly)</h2>
      <p>Federal taxes only, standard W-4, no pre-tax deductions and no state tax:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Salary</th><th class="n">Federal withholding / yr</th><th class="n">FICA / yr</th><th class="n">Take-home / yr</th><th class="n">Per biweekly check</th></tr></thead><tbody>
<?php foreach ([30000, 40000, 50000, 60000, 75000, 90000, 100000, 125000, 150000] as $amt): $b = salary_breakdown($amt, 'single'); ?>
        <tr><td><?= money($amt) ?></td><td class="n"><?= money($b['tax']) ?></td><td class="n"><?= money($b['fica']) ?></td><td class="n"><?= money($b['net']) ?></td><td class="n"><?= money($b['net'] / 26, 2) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>

      <h2 id="state-tax">What about state and local taxes?</h2>
      <p>State income tax varies widely. Nine states have no tax on wages (Alaska, Florida, Nevada, New Hampshire, South Dakota, Tennessee, Texas, Washington and Wyoming), several use a single flat rate, and the rest use their own brackets. Enter your state’s flat rate — or your approximate effective state rate — in the optional field and the calculator applies it to your federal taxable wages. Some cities and counties also levy local wage taxes, and a few states require employee contributions for disability or paid family leave; add those as after-tax deductions for a closer match to your stub.</p>

      <h2 id="increase-take-home">Ways to change your take-home pay</h2>
      <ul>
        <li><strong>Update your W-4</strong> if you got a big refund last year — fewer dollars withheld means larger checks now. If you owed, add Step 4(c) extra withholding.</li>
        <li><strong>Use pre-tax benefits.</strong> HSA and FSA contributions avoid income tax <em>and</em> FICA, the most tax-efficient dollars in your paycheck.</li>
        <li><strong>Check the new deductions.</strong> Qualified tips and overtime premium are deductible on your <?= $Y ?> return (up to <?= money($y['tipsMax']) ?> of tips and <?= money($y['overtimeMax']['single']) ?> of overtime premium, <?= money($y['overtimeMax']['mfj']) ?> joint). You can reflect them in W-4 Step 4(b) so less is withheld.</li>
        <li><strong>Compare offers properly.</strong> Use the <a href="/calculators/salary-to-hourly/">salary to hourly calculator</a> to compare pay on equal terms.</li>
      </ul>
      <p>New job? Our guide to <a href="/blog/understanding-your-w-2/">understanding your W-2</a> explains every box you’ll see at year-end, and <a href="/blog/how-much-federal-tax-will-i-pay/">how much federal tax will I pay</a> walks through examples by salary.</p>

<?= faq_block([
  ['How do I calculate my take-home pay?', '<p>Start with gross pay, subtract pre-tax deductions (401(k), health premiums, HSA), then federal income tax withholding, 6.2% Social Security, 1.45% Medicare, any state and local tax, and after-tax deductions. For a $65,000 single earner paid biweekly with a 5% 401(k) and $100 health premium, take-home is about ' . $per($ex['net']) . ' per paycheck.</p>'],
  ['How much is $65,000 a year after taxes?', '<p>With no deductions, a single filer keeps about ' . money(salary_breakdown(65000, 'single')['net']) . ' after federal income tax and FICA in ' . $Y . ', or ' . money(salary_breakdown(65000, 'single')['net'] / 26, 2) . ' per biweekly paycheck, before state tax.</p>'],
  ['What percentage of my paycheck goes to taxes?', '<p>FICA is always 7.65% up to the Social Security wage base. Federal withholding usually adds 5% to 15% for middle incomes, plus 0% to about 10% for state tax. Most workers see 15% to 30% of gross pay withheld for taxes in total.</p>'],
  ['Does contributing to a 401(k) lower my taxes?', '<p>A traditional 401(k) lowers federal and most state income tax withholding, but Social Security and Medicare are still withheld on those dollars. A Roth 401(k) is taken after tax and lowers neither.</p>'],
  ['Why is my paycheck smaller than the calculator shows?', '<p>Common reasons: state or local taxes, state disability or paid-leave programs, benefits not entered (life insurance, parking, ESPP), a W-4 with the Step 2 box checked or extra withholding, or a bonus taxed at the 22% supplemental rate.</p>'],
  ['Is biweekly or semimonthly pay better?', '<p>Neither changes your annual pay or tax. Biweekly gives 26 smaller checks (with two “extra” paycheck months a year); semimonthly gives 24 larger checks on fixed dates.</p>'],
  ['How are bonuses taxed?', '<p>Employers usually withhold a flat 22% federal rate on supplemental wages up to $1 million (37% above), plus FICA. It’s withholding only — the bonus is taxed at your normal rates when you file.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('paycheck-calculator', ['federal-income-tax', 'tax-refund-calculator', 'salary-to-hourly', '1099-tax-calculator', 'quarterly-estimated-tax', 'self-employment-tax']) ?></div>
