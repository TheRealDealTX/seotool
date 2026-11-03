<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "S Corp Tax Calculator $Y — LLC vs S Corp Tax Savings | CPA Calculator";
$P['description'] = "Free $Y S corp tax calculator. Compare LLC or sole prop taxes with an S corporation paying a reasonable salary and see your savings after payroll costs.";
$P['scripts'] = ['/assets/js/tools/s-corp-tax-savings.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* PHP mirror of the JS comparison (standard deduction, no other income, non-SSTB). */
function scorp_qbi(float $inc, float $wages, float $before, string $s, int $year = TAX_YEAR): float {
  global $TAX;
  $inc = max(0, $inc);
  $T = $TAX['years'][(string) $year]['qbiThreshold'][$s];
  $R = ($s === 'mfj' ? 2 : 1) * ($year >= 2026 ? 75000 : 50000);
  $phase = min(1, max(0, ($before - $T) / $R));
  $tent = 0.2 * $inc; $lim = min($tent, 0.5 * $wages);
  $ded = $phase <= 0 ? $tent : ($phase >= 1 ? $lim : $tent - ($tent - $lim) * $phase);
  return max(0, min($ded, $before * 0.2));
}
function scorp_compare(float $profit, float $salary, float $costs, string $s = 'single', int $year = TAX_YEAR): array {
  global $TAX;
  $yy = $TAX['years'][(string) $year];
  $std = $yy['std'][$s];
  // Sole proprietor / single-member LLC
  $base = $profit * 0.9235;
  $se = min($base, $yy['ssWageBase']) * 0.124 + $base * 0.029 + max(0, $base - $yy['addlMedicare'][$s]) * 0.009;
  $half = (min($base, $yy['ssWageBase']) * 0.124 + $base * 0.029) / 2;
  $agiA = $profit - $half;
  $befA = max(0, $agiA - $std);
  $qA = scorp_qbi($profit - $half, 0, $befA, $s, $year);
  $incA = fed_tax(max(0, $befA - $qA), $s, $year)['tax'];
  // S corporation
  $er = min($salary, $yy['ssWageBase']) * 0.062 + $salary * 0.0145;
  $ee = min($salary, $yy['ssWageBase']) * 0.062 + $salary * 0.0145 + max(0, $salary - $yy['addlMedicare'][$s]) * 0.009;
  $k1 = $profit - $salary - $er - $costs;
  $agiB = $salary + $k1;
  $befB = max(0, $agiB - $std);
  $qB = scorp_qbi($k1, $salary, $befB, $s, $year);
  $incB = fed_tax(max(0, $befB - $qB), $s, $year)['tax'];
  $a = $se + $incA; $b = $er + $ee + $incB + $costs;
  return compact('se', 'half', 'agiA', 'qA', 'incA', 'er', 'ee', 'k1', 'agiB', 'qB', 'incB', 'std') + ['taxA' => max(0, $befA - $qA), 'taxB' => max(0, $befB - $qB), 'soleTotal' => $a, 'scorpTotal' => $b, 'savings' => $a - $b];
}
$ex = scorp_compare(100000, 50000, 2000);

echo tool_hero('s-corp-tax-savings', "S Corp Tax Savings Calculator $Y",
  "Should your LLC elect S corp status? Enter your business profit and a reasonable salary to compare self-employment tax and income tax as a sole proprietor or LLC against an S corporation — including employer payroll tax, the QBI deduction and the extra cost of running payroll.",
  ['LLC vs S corp side by side', "$Y payroll & QBI rules", 'Break-even profit', 'Reasonable-salary check']);
?>
<section class="tool" aria-label="S corp tax savings calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="scorp-form" novalidate>
        <div class="grid-2">
          <?= year_field() ?>
          <?= money_field('state', 'State income tax rate (optional)', '', 'A flat rate applied to AGI in both scenarios. Leave blank for federal only. Some states charge S corps an entity-level tax (e.g. California 1.5%) — add that to annual costs.', '', '%') ?>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Your business</legend>
          <?= money_field('profit', 'Net business profit (before paying yourself)', 120000, 'Revenue minus business expenses — Schedule C line 31 today. Do not subtract owner draws.') ?>
          <input type="range" min="0" max="500000" step="1000" data-range-for="profit" aria-label="Business profit slider">
          <?= money_field('salary', 'Reasonable salary you’d pay yourself as an S corp', 60000, 'W-2 wages the S corp would pay you. The IRS requires a reasonable salary for the work you do before taking distributions.') ?>
          <input type="range" min="0" max="300000" step="1000" data-range-for="salary" aria-label="Salary slider">
          <label class="check"><input type="checkbox" name="sstb"> Specified service business (health, law, accounting, consulting, financial services, performing arts, athletics)</label>
        </fieldset>
        <fieldset class="fieldset"><legend>Other income &amp; costs</legend>
          <div class="grid-2">
            <?= money_field('other', 'Other taxable income', '', 'Spouse’s wages, interest, dividends or other income on the same return. It changes your bracket in both scenarios.') ?>
            <?= money_field('costs', 'Extra annual S corp costs', 2000, 'Payroll service, the separate Form 1120-S return, state annual fees and franchise taxes, extra bookkeeping. Typically $1,500–$3,500 a year.') ?>
          </div>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="saveLabel">Estimated annual S corp savings</div>
          <div class="res-big good" data-out="save">$0</div>
          <div class="res-sub"><span data-out="summary">—</span></div>
          <div class="kpis">
            <div class="kpi"><small>Sole prop / LLC tax</small><b data-out="soleTotal">$0</b></div>
            <div class="kpi"><small>S corp tax + costs</small><b data-out="scorpTotal">$0</b></div>
            <div class="kpi"><small>Payroll tax saved</small><b data-out="payrollSaved">$0</b></div>
            <div class="kpi"><small>Break-even (same salary %)</small><b data-out="breakeven">—</b></div>
          </div>
          <div class="res-label">Sole prop / LLC</div>
          <div class="meter" aria-hidden="true"><span data-meter-a style="background:#f59e0b"></span></div>
          <div class="res-label">S corporation (incl. costs)</div>
          <div class="meter" aria-hidden="true"><span data-meter-b style="background:#10b981"></span></div>
          <div class="table-wrap" style="margin-top:4px"><table>
            <thead><tr><th>Item</th><th class="n">Sole prop / LLC</th><th class="n">S corp</th></tr></thead>
            <tbody data-compare></tbody>
          </table></div>
          <div class="res-label" style="margin-bottom:6px">Savings at other salary levels</div>
          <ul class="rows" data-sens></ul>
          <p class="note" data-out="warn">—</p>
          <p class="note">Estimate only. Federal tax uses the standard deduction; QBI includes the W-2 wage limit and SSTB phase-out. Excludes retirement plans, health insurance and state-specific S corp rules. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-it-works">How an S corp saves tax</h2>
      <p>As a sole proprietor or single-member LLC, <strong>all</strong> of your net profit is subject to 15.3% self-employment tax (12.4% Social Security up to the <?= money($y['ssWageBase']) ?> wage base for <?= $Y ?>, plus 2.9% Medicare on everything). An LLC is a legal structure, not a tax status — by default the IRS taxes a single-member LLC exactly like a sole proprietorship.</p>
      <p>When your LLC or corporation elects <strong>S corporation</strong> status, your profit is split into two pieces:</p>
      <ul>
        <li>a <strong>reasonable salary</strong> paid through payroll, which is subject to Social Security and Medicare (7.65% from you, 7.65% from the company), and</li>
        <li>the remaining profit, passed through to you on a <strong>Schedule K-1</strong> and taken as distributions, which is subject to income tax but <strong>not</strong> to payroll or self-employment tax.</li>
      </ul>
      <p>The savings come from that second piece. Income tax doesn’t go away — you pay it on both the salary and the K-1 income — so the real question is whether the payroll tax you avoid on distributions is bigger than the extra costs of running an S corp.</p>
      <div class="formula">Sole prop: SE tax (15.3% × 92.35% of profit) + income tax<br>S corp: FICA on salary (7.65% + 7.65%) + income tax on salary + K-1 + extra costs<br>K-1 income = profit − salary − employer payroll tax − S corp costs<br>Savings = sole prop total − S corp total</div>

      <h2 id="how-to-use">How to use the S corp tax calculator</h2>
      <ol>
        <li><strong>Net business profit</strong> — your revenue minus deductible expenses, before paying yourself. If you file Schedule C today, use line 31.</li>
        <li><strong>Reasonable salary</strong> — what the S corp would pay you on a W-2. Use the slider to see how savings change as salary moves.</li>
        <li><strong>Specified service business</strong> — tick this for health, law, accounting, consulting and similar fields, where the QBI deduction phases out at higher incomes.</li>
        <li><strong>Other income and costs</strong> — a spouse’s wages or investment income on the same return change your bracket. Annual S corp costs default to $2,000.</li>
      </ol>
      <p>The results show both scenarios line by line, the payroll tax saved, the break-even profit at your chosen salary percentage, and a table of savings at salaries from 30% to 70% of profit.</p>

      <h2 id="example">Worked example: $100,000 of profit</h2>
      <p>A single owner with $100,000 of net profit in <?= $Y ?>, no other income, considering an S corp election with a $50,000 salary and $2,000 of extra annual costs:</p>
      <div class="table-wrap"><table>
        <thead><tr><th></th><th class="n">Sole prop / LLC</th><th class="n">S corp</th></tr></thead><tbody>
        <tr><td>Self-employment tax</td><td class="n"><?= money($ex['se']) ?></td><td class="n">—</td></tr>
        <tr><td>Payroll tax on $50,000 salary (employer + employee)</td><td class="n">—</td><td class="n"><?= money($ex['er'] + $ex['ee']) ?></td></tr>
        <tr><td>K-1 distribution</td><td class="n">—</td><td class="n"><?= money($ex['k1']) ?></td></tr>
        <tr><td>QBI deduction</td><td class="n">−<?= money($ex['qA']) ?></td><td class="n">−<?= money($ex['qB']) ?></td></tr>
        <tr><td>Taxable income</td><td class="n"><?= money($ex['taxA']) ?></td><td class="n"><?= money($ex['taxB']) ?></td></tr>
        <tr><td>Federal income tax</td><td class="n"><?= money($ex['incA']) ?></td><td class="n"><?= money($ex['incB']) ?></td></tr>
        <tr><td>Extra S corp costs</td><td class="n">—</td><td class="n">$2,000</td></tr>
        <tr><td><strong>Total</strong></td><td class="n"><strong><?= money($ex['soleTotal']) ?></strong></td><td class="n"><strong><?= money($ex['scorpTotal']) ?></strong></td></tr>
      </tbody></table></div>
      <p>The S corp saves about <strong><?= money($ex['savings']) ?> a year</strong>. Most of it is payroll tax avoided on the <?= money($ex['k1']) ?> K-1 distribution, partly offset by a smaller QBI deduction (the salary isn’t qualified business income) and the $2,000 of added costs.</p>

      <h2 id="reasonable-salary">What is a reasonable salary?</h2>
      <p>The IRS requires S corp owners who work in the business to pay themselves “reasonable compensation” before taking distributions. There’s no fixed percentage. Reasonable means roughly what the business would have to pay someone else to do the work you do, considering:</p>
      <ul>
        <li>your duties, hours and experience;</li>
        <li>what comparable businesses pay for similar roles (salary surveys, Bureau of Labor Statistics data, job listings);</li>
        <li>the company’s revenue and the portion generated by your personal services.</li>
      </ul>
      <p>A setup that pays a tiny salary and takes most profit as distributions invites the IRS to reclassify distributions as wages, with back payroll taxes, penalties and interest. The 60/40 or 50/50 “rules” you’ll see online are rules of thumb, not law — document how you set your salary. The calculator flags salaries under about 30% of profit.</p>

      <h2 id="when-worth-it">When is an S corp worth it?</h2>
      <p>Because the savings are roughly 15.3% of the distribution minus fixed costs, an S corp usually starts to make sense once net profit is consistently in the <strong>$60,000–$80,000+</strong> range, and the benefit grows with profit until your salary reaches the Social Security wage base. The calculator’s break-even figure finds the profit level where savings turn positive at your chosen salary percentage. Below it, the payroll service, extra tax return and state fees cost more than you save.</p>
      <div class="callout warn"><?= icon('shield') ?><p><strong>Hidden trade-offs:</strong> a lower salary means lower Social Security earnings for your future benefit, and smaller salary-based retirement contributions (a Solo 401(k) employer contribution is 25% of W-2 wages in an S corp versus about 20% of net SE earnings as a sole proprietor). Some states impose entity taxes or don’t recognize S corps at all, and you’ll need to run payroll with withholding and quarterly payroll filings.</p></div>

      <h2 id="qbi">How the QBI deduction changes the math</h2>
      <p>The 20% qualified business income deduction, made permanent by the One Big Beautiful Bill Act, applies to sole proprietors and S corp owners alike — but S corp salary is <strong>not</strong> qualified business income. Only the K-1 portion counts, so moving profit into salary reduces your QBI deduction a little. That’s why the income tax line is often slightly <em>higher</em> under an S corp.</p>
      <p>Above <?= money($y['qbiThreshold']['single']) ?> of taxable income (<?= money($y['qbiThreshold']['mfj']) ?> married filing jointly) in <?= $Y ?>, two limits phase in over the next $75,000 ($150,000 joint): the deduction becomes capped at 50% of W-2 wages paid by the business, and specified service businesses lose it entirely. A sole proprietor with no employees has no W-2 wages, so at high incomes the S corp salary can actually <em>preserve</em> a QBI deduction a sole proprietor would lose. The calculator models both limits.</p>

      <h2 id="how-to-elect">How to elect S corp status</h2>
      <ol>
        <li>Form an LLC or corporation in your state (if you haven’t already).</li>
        <li>File <strong>Form 2553</strong> with the IRS. To be effective for the current year it’s generally due within 2 months and 15 days of the start of the tax year — March 15 for a calendar-year business. Late-election relief is available in many cases.</li>
        <li>Set up payroll and pay yourself a reasonable salary with federal and state withholding.</li>
        <li>File Form 1120-S each year by March 15 and issue yourself a Schedule K-1.</li>
      </ol>
      <p>Still a sole proprietor? See what you owe today with the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> and <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>, and keep up with <a href="/calculators/quarterly-estimated-tax/">quarterly estimated taxes</a> on your K-1 income after the election. Our guide to <a href="/blog/1099-taxes-for-physicians/">1099 taxes for physicians</a> covers the S corp decision for high earners in a specified service field.</p>

<?= faq_block([
  ['How much tax does an S corp save?', "<p>Roughly 15.3% of the profit you take as distributions instead of salary (2.9% once your salary is above the Social Security wage base), minus the extra cost of payroll and a separate return. For a single owner with \$100,000 of profit and a \$50,000 salary, the estimated $Y savings is about " . money($ex['savings']) . " a year after \$2,000 of costs.</p>"],
  ['At what income does an S corp make sense?', '<p>Usually when net profit is steadily above about $60,000–$80,000. Below that, the reasonable salary eats most of the profit and fixed costs outweigh the payroll tax saved. Use the break-even figure in the calculator for your own numbers.</p>'],
  ['Is an LLC or S corp better for taxes?', '<p>An LLC on its own is taxed like a sole proprietorship (or partnership), with self-employment tax on all profit. An LLC that elects S corp status keeps its legal structure but changes its tax treatment, so the question is really “should my LLC elect S corp taxation?” The answer depends on profit, a defensible salary and your state’s rules.</p>'],
  ['Do S corp owners pay self-employment tax?', '<p>Not on S corp income. Owner-employees pay FICA on their W-2 salary through payroll (7.65% withheld plus 7.65% paid by the company). K-1 distributions are not subject to self-employment or payroll tax.</p>'],
  ['What percentage of S corp profit should be salary?', '<p>There is no legal percentage. Salary must be reasonable for the services you perform, based on what similar businesses pay. Many owners land between 40% and 60% of profit, but the right number depends on your role and industry — document your reasoning.</p>'],
  ['Does an S corp lower my income tax?', '<p>Generally no. You pay income tax on both salary and K-1 income. Income tax can even rise slightly because salary does not qualify for the 20% QBI deduction. The savings come from avoiding payroll tax on distributions.</p>'],
  ['When is the deadline to elect S corp status?', '<p>File Form 2553 no more than 2 months and 15 days after the start of the tax year the election should take effect — March 15 for calendar-year businesses. A new business has 2 months and 15 days from its start date.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('s-corp-tax-savings', ['self-employment-tax', '1099-tax-calculator', 'quarterly-estimated-tax', 'mileage-deduction', 'home-office-deduction', 'profit-margin']) ?></div>
