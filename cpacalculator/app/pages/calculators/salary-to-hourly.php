<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Salary to Hourly Calculator $Y — Hourly, Weekly & After-Tax Pay | CPA Calculator";
$P['description'] = "Free salary to hourly calculator. Convert annual salary to hourly, daily, weekly, biweekly and monthly pay (or hourly to salary), before and after $Y taxes.";
$P['scripts'] = ['/assets/js/tools/salary-to-hourly.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

$ex = salary_breakdown(60000, 'single');
$exHr = 60000 / 2080;

echo tool_hero('salary-to-hourly', 'Salary to Hourly Calculator',
  "Convert an annual salary to an hourly wage — or an hourly rate to a yearly salary — and see daily, weekly, biweekly, semimonthly and monthly pay side by side, before and after $Y federal taxes. Adjust hours, unpaid time off and paid vacation, and compare a W-2 job with a 1099 contract rate.",
  ['Salary ↔ hourly, both ways', 'Every pay period', "After-tax pay ($Y rates)", '1099 vs W-2 rate helper']);
?>
<section class="tool" aria-label="Salary to hourly calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="s2h-form" novalidate>
        <div class="tool-tabs" data-tabs>
          <button type="button" data-tab="toHourly" aria-selected="true">Salary → hourly</button>
          <button type="button" data-tab="toSalary" aria-selected="false">Hourly → salary</button>
        </div>
        <input type="hidden" name="mode" value="toHourly">
        <div data-panel="toHourly">
          <?= money_field('salary', 'Annual salary (gross)', 60000, 'Your yearly pay before taxes and deductions, including any guaranteed bonus.') ?>
          <input type="range" min="10000" max="400000" step="1000" data-range-for="salary" aria-label="Salary slider">
        </div>
        <div data-panel="toSalary" hidden>
          <div class="grid-2">
            <?= money_field('hourly', 'Hourly wage', 25, 'Your base pay per hour before taxes.') ?>
            <?= money_field('ot', 'Overtime hours per week', '', 'Hours above your regular schedule paid at time-and-a-half (1.5×).', '', '') ?>
          </div>
        </div>
        <fieldset class="fieldset"><legend>Work schedule</legend>
          <div class="grid-3">
            <?= money_field('hours', 'Hours per week', 40, 'Regular paid hours in a typical week.', '', '') ?>
            <?= money_field('unpaid', 'Unpaid weeks off', '', 'Weeks per year you are not paid at all (unpaid leave, seasonal gaps). Paid weeks = 52 − this.', '', '') ?>
            <?= money_field('pto', 'Paid vacation & holiday days', 15, 'Days you are paid but don’t work. Used for your “true” hourly rate and the 1099 comparison. US employers commonly give 10–15 days of PTO plus 8–11 holidays.', '', '') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Taxes (for after-tax pay)</legend>
          <div class="grid-2">
            <?= year_field() ?>
            <?= money_field('state', 'State income tax rate', '', 'Optional flat rate applied to wages. Leave blank for states with no income tax.', '', '%') ?>
          </div>
          <?= status_field() ?>
          <?= money_field('k401', 'Pre-tax 401(k) contribution', '', "Percent of pay you contribute pre-tax. $Y limit: " . money($y['k401']) . '.', '', '%') ?>
        </fieldset>
        <details class="more"><summary>1099 vs W-2: what contract rate equals this job?</summary>
          <?= money_field('benefits', 'Value of employer benefits', 20, 'Health insurance, retirement match, life/disability insurance and other benefits as a % of salary. Often 20–30%.', '', '%') ?>
          <p class="hint">We find the 1099 income that leaves you with the same take-home pay plus benefits after self-employment tax (15.3%), income tax with the QBI deduction, and no paid time off.</p>
        </details>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="bigLabel">Hourly wage</div>
          <div class="res-big" data-out="big">$0</div>
          <div class="res-sub"><span data-out="summary">—</span></div>
          <div class="kpis">
            <div class="kpi"><small>Annual gross</small><b data-out="kAnnual">$0</b></div>
            <div class="kpi"><small>Take-home per year</small><b data-out="kNet">$0</b></div>
            <div class="kpi"><small>After-tax hourly</small><b data-out="kNetHr">$0</b></div>
            <div class="kpi"><small>True hourly (hrs worked)</small><b data-out="kTrue">$0</b></div>
          </div>
          <div class="table-wrap" style="margin-top:0"><table>
            <thead><tr><th>Pay period</th><th class="n">Gross</th><th class="n">After tax</th></tr></thead>
            <tbody data-periods></tbody>
          </table></div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your pay goes"></svg><ul class="legend" data-legend></ul></div>
          <div class="res-label" style="margin-bottom:6px">1099 contract rate equivalent</div>
          <ul class="rows" data-c1099></ul>
          <p class="note" data-out="c1099note">—</p>
          <p class="note">After-tax figures use the <?= $Y ?> federal brackets, standard deduction and FICA; state tax is a flat estimate. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-convert">How to convert salary to hourly</h2>
      <p>To turn an annual salary into an hourly wage, divide the salary by the number of hours you’re paid for in a year. A full-time schedule is 40 hours a week for 52 weeks, or <strong>2,080 hours</strong>. Paid vacation and holidays are included in those 2,080 hours because you’re paid for them.</p>
      <div class="formula">Hourly wage = annual salary ÷ (hours per week × paid weeks per year)<br>Annual salary = hourly wage × hours per week × paid weeks per year<br>Quick rule: hourly ≈ salary ÷ 2,000 (or salary ≈ hourly × 2,000)</div>
      <p>The shortcut works because 2,080 is close to 2,000: a $50,000 salary is about $25 an hour, and $30 an hour is about $60,000 a year. For an exact figure, use the calculator — it handles part-time schedules, unpaid weeks off and overtime.</p>

      <h2 id="how-to-use">How to use the calculator</h2>
      <ol>
        <li><strong>Pick a direction.</strong> “Salary → hourly” converts a yearly salary; “Hourly → salary” converts an hourly wage and can add overtime at time-and-a-half.</li>
        <li><strong>Set your schedule.</strong> Enter hours per week, any unpaid weeks off, and paid vacation and holiday days.</li>
        <li><strong>Add tax details.</strong> Filing status, an optional state tax rate and pre-tax 401(k) percentage produce after-tax pay for every period.</li>
        <li><strong>Compare with contract work.</strong> Open the 1099 section to see the hourly rate a freelance or contract job must pay to match the W-2 job.</li>
      </ol>
      <p>You’ll get hourly, daily, weekly, biweekly, semimonthly, monthly and annual pay in one table, plus your “true” hourly rate — what you earn for each hour you actually work once paid time off is taken out.</p>

      <h2 id="example">Worked example: $60,000 a year</h2>
      <ul>
        <li>Hourly: $60,000 ÷ 2,080 hours = <strong><?= money($exHr, 2) ?></strong> per hour.</li>
        <li>Weekly: $60,000 ÷ 52 = <?= money(60000 / 52, 2) ?>. Biweekly: <?= money(60000 / 26, 2) ?>. Semimonthly: <?= money(60000 / 24, 2) ?>. Monthly: <?= money(5000, 2) ?>.</li>
        <li>After tax (<?= $Y ?>, single, standard deduction, no state tax): federal income tax ≈ <?= money($ex['tax']) ?> and Social Security plus Medicare ≈ <?= money($ex['fica']) ?>, leaving about <strong><?= money($ex['net']) ?></strong> a year — <?= money($ex['net'] / 2080, 2) ?> per hour or <?= money($ex['net'] / 26) ?> per biweekly paycheck.</li>
        <li>With 15 paid days off, you actually work 49 weeks, so your true pay per hour worked is <?= money(60000 / (40 * 49), 2) ?>.</li>
      </ul>

      <h2 id="salary-table">Salary to hourly conversion table (<?= $Y ?>)</h2>
      <p>Based on 40 hours a week and 52 paid weeks (2,080 hours). After-tax hourly assumes a single filer with the <?= $Y ?> standard deduction and no state income tax.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Annual salary</th><th class="n">Hourly</th><th class="n">Weekly</th><th class="n">Monthly</th><th class="n">After-tax hourly</th></tr></thead><tbody>
<?php foreach ([30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 90000, 100000, 120000, 150000, 200000] as $s): $b = salary_breakdown($s, 'single'); ?>
        <tr><td><?= money($s) ?></td><td class="n"><?= money($s / 2080, 2) ?></td><td class="n"><?= money($s / 52) ?></td><td class="n"><?= money($s / 12) ?></td><td class="n"><?= money($b['net'] / 2080, 2) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>

      <h2 id="hourly-table">Hourly to salary conversion table</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Hourly wage</th><th class="n">Annual (2,080 hrs)</th><th class="n">Monthly</th><th class="n">Biweekly</th><th class="n">Part-time (20 hrs/wk)</th></tr></thead><tbody>
<?php foreach ([15, 17, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50, 60, 75, 100] as $h): ?>
        <tr><td><?= money($h) ?>/hr</td><td class="n"><?= money($h * 2080) ?></td><td class="n"><?= money($h * 2080 / 12) ?></td><td class="n"><?= money($h * 80) ?></td><td class="n"><?= money($h * 1040) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>

      <h2 id="pay-periods">Biweekly vs. semimonthly vs. monthly pay</h2>
      <p>Pay frequency doesn’t change your annual salary, only the size of each check. <strong>Biweekly</strong> means every other week — 26 paychecks a year, so two months each year have three paydays. <strong>Semimonthly</strong> means twice a month, usually on the 15th and last day — 24 paychecks, each slightly larger than a biweekly check. <strong>Weekly</strong> is 52 checks. When budgeting from a biweekly paycheck, multiply by 26 and divide by 12 to get a true monthly figure; multiplying by two understates your monthly income.</p>

      <h2 id="after-tax">Salary to hourly after taxes</h2>
      <p>Your take-home hourly rate is your gross rate minus federal income tax, Social Security (6.2% up to the <?= money($y['ssWageBase']) ?> wage base in <?= $Y ?>), Medicare (1.45%, plus 0.9% above $200,000), state and local income tax, and pre-tax deductions such as 401(k) contributions and health premiums. The calculator applies the <?= $Y ?> federal brackets and standard deduction for your filing status. For a paycheck-level breakdown with withholding and benefits, use the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>; for the full annual picture see the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>.</p>
      <div class="callout"><?= icon('spark') ?><p><strong>Overtime tip:</strong> for 2025 through 2028, the One Big Beautiful Bill Act lets eligible hourly workers deduct the “half” premium portion of qualified overtime pay — up to $12,500 ($25,000 joint) — on their federal return. Overtime is still subject to Social Security and Medicare.</p></div>

      <h2 id="1099-vs-w2">1099 vs. W-2: comparing a contract rate to a salary</h2>
      <p>A contract or freelance hourly rate isn’t comparable to a W-2 hourly wage. As a 1099 contractor you:</p>
      <ul>
        <li>pay <strong>both halves of Social Security and Medicare</strong> — 15.3% self-employment tax instead of 7.65% (you can deduct half, and may get the 20% QBI deduction);</li>
        <li>buy your own <strong>health insurance and retirement</strong> with no employer match;</li>
        <li>aren’t paid for <strong>vacation, holidays or sick days</strong>, so you bill fewer hours.</li>
      </ul>
      <p>The calculator’s 1099 section solves for the contract income that leaves you with the same take-home pay plus benefits, then divides by your billable hours. As a rough guide, a contract rate typically needs to be 25–40% higher than the W-2 hourly wage to break even. For the taxes on contract income itself, see the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> and <a href="/calculators/self-employment-tax/">self-employment tax calculator</a>, or read <a href="/blog/got-a-1099-exactly-what-to-do-next/">what to do when you get a 1099</a>.</p>

      <h2 id="tips">Tips when comparing job offers</h2>
      <ul>
        <li>Compare <strong>total compensation</strong>: salary, bonus, 401(k) match, health premiums you’d pay, and PTO.</li>
        <li>Salaried exempt jobs often involve unpaid extra hours — enter your real weekly hours to see the true hourly rate.</li>
        <li>Check state income tax: the same salary nets several thousand dollars more in a no-income-tax state.</li>
        <li>Read your <a href="/blog/understanding-your-w-2/">W-2</a> at year end to confirm your actual taxable wages.</li>
      </ul>

<?= faq_block([
  ['How do I convert my salary to an hourly wage?', '<p>Divide your annual salary by the number of paid hours in a year. For a full-time job that is 2,080 hours (40 hours × 52 weeks). For example, $60,000 ÷ 2,080 = ' . money($exHr, 2) . ' per hour.</p>'],
  ['How much is $50,000 a year per hour?', '<p>$50,000 a year is ' . money(50000 / 2080, 2) . ' per hour at 40 hours a week for 52 weeks. After ' . $Y . ' federal income tax and FICA for a single filer, that is about ' . money(salary_breakdown(50000, 'single')['net'] / 2080, 2) . ' per hour, before state tax.</p>'],
  ['How much is $25 an hour annually?', '<p>$25 an hour is $52,000 a year full time (2,080 hours), about $4,333 a month or $2,000 every two weeks. Working 30 hours a week, it is $39,000.</p>'],
  ['Does salary to hourly include paid vacation?', '<p>Yes. Paid vacation and holidays are part of the 2,080 paid hours, so the standard conversion already includes them. If you want your pay per hour actually worked, enter your paid days off — the calculator shows a “true hourly” rate that excludes them.</p>'],
  ['How many work hours are in a year?', '<p>A full-time year is 2,080 hours (52 weeks × 40 hours). After 10 holidays and 10 vacation days, the hours actually worked drop to about 1,920.</p>'],
  ['What hourly rate should I charge as a 1099 contractor?', '<p>Enough to cover self-employment tax, benefits you no longer receive and unpaid time off. Most contractors need 25–40% more per hour than an equivalent W-2 wage. Open the 1099 section of the calculator for a figure based on your own salary and benefits.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('salary-to-hourly', ['paycheck-calculator', 'federal-income-tax', '1099-tax-calculator', 'tax-refund-calculator', 'self-employment-tax', 'quarterly-estimated-tax']) ?></div>
