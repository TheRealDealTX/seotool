<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Bonus Tax Calculator $Y: Net Bonus & Actual Tax | CPA Calculator";
$P['description'] = "Free $Y bonus tax calculator. See the 22% federal withholding, FICA and state tax on your bonus, your net check, and what you will actually owe at tax time.";
$P['scripts'] = ['/assets/js/tools/bonus-tax-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Server-side mirror of the calculator (single filer, percentage or aggregate method, no 401(k), no state). */
function bonus_ex(float $salary, float $bonus, string $method = 'flat', int $freq = 26, string $status = 'single'): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $std = $y['std'][$status];
  if ($method === 'aggregate') {
    $per = $salary / $freq;
    $t = fn(float $w): float => fed_tax(max(0, $w * $freq - $std), $status)['tax'] / $freq;
    $fed = $t($per + $bonus) - $t($per);
  } else {
    $fed = min($bonus, 1000000) * $y['supplemental']['rate'] + max(0, $bonus - 1000000) * $y['supplemental']['over1mRate'];
  }
  $base = $y['ssWageBase'];
  $ss = max(0, min($salary + $bonus, $base) - min($salary, $base)) * 0.062;
  $med = $bonus * 0.0145 + (max(0, $salary + $bonus - 200000) - max(0, $salary - 200000)) * 0.009;
  $before = fed_tax(max(0, $salary - $std), $status)['tax'];
  $after = fed_tax(max(0, $salary + $bonus - $std), $status)['tax'];
  $actual = $after - $before;
  return compact('salary', 'bonus', 'fed', 'ss', 'med', 'before', 'after', 'actual', 'std') +
    ['net' => $bonus - $fed - $ss - $med, 'diff' => $fed - $actual, 'rate' => $bonus > 0 ? $actual / $bonus : 0];
}
$ex = bonus_ex(45000, 10000);
$agg = bonus_ex(45000, 10000, 'aggregate');
$rows = array_map(fn($s) => bonus_ex($s, 10000), [30000, 45000, 75000, 120000, 220000]);
$sup = $y['supplemental'];

echo tool_hero('bonus-tax-calculator', "Bonus Tax Calculator $Y",
  "Find out how much of your bonus you will actually take home. Enter the bonus and your salary to see the federal supplemental withholding (" . round($sup['rate'] * 100) . "%, or " . round($sup['over1mRate'] * 100) . "% over \$1 million), Social Security, Medicare and state tax, then compare it with the tax you really owe on the bonus when you file.",
  ['Percentage & aggregate methods', '$1 million / 37% rule', 'Actual tax vs withholding', '401(k) on bonus']);
?>
<section class="tool" aria-label="Bonus tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="bonus-form" novalidate>
        <div class="grid-2">
          <?= year_field() ?>
          <div class="field"><label for="f-freq">Pay frequency</label><select id="f-freq" name="freq">
            <option value="52">Weekly</option><option value="26" selected>Every two weeks</option><option value="24">Twice a month</option><option value="12">Monthly</option>
          </select></div>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Bonus &amp; salary</legend>
          <?= money_field('bonus', 'Bonus amount (gross)', 10000, 'The bonus before any taxes or deductions. Commissions, awards, severance and retention bonuses are treated the same way.') ?>
          <input type="range" min="0" max="100000" step="500" data-range-for="bonus" aria-label="Bonus amount slider">
          <?= money_field('salary', 'Annual salary (regular wages)', 75000, 'Your regular yearly pay from the same employer, before the bonus. Used for the aggregate method, the Social Security wage base and the actual-tax comparison.') ?>
        </fieldset>
        <fieldset class="fieldset"><legend>Withholding method</legend>
          <div class="field"><span class="lbl">How your employer withholds federal tax</span><div class="seg" role="radiogroup" aria-label="Withholding method">
            <label><input type="radio" name="method" value="flat" checked><span>Percentage (flat <?= round($sup['rate'] * 100) ?>%)</span></label>
            <label><input type="radio" name="method" value="aggregate"><span>Aggregate (with a paycheck)</span></label>
          </div><span class="hint">Most employers use the flat percentage method for separately paid bonuses.</span></div>
          <?= money_field('ytdSupp', 'Supplemental wages already paid this year', '', 'Earlier bonuses and commissions from this employer in the same calendar year. Supplemental wages above $1 million get mandatory ' . round($sup['over1mRate'] * 100) . '% withholding.', 'Leave blank unless you have had large bonuses this year.') ?>
        </fieldset>
        <details class="more"><summary>State tax &amp; 401(k) on the bonus</summary>
          <div class="grid-2">
            <?= money_field('stateRate', 'State supplemental rate', '', 'Many states publish a flat withholding rate for bonuses; others use your regular rate. Enter 0 for states with no wage income tax.', '', '%') ?>
            <?= money_field('k401Pct', '401(k) contribution from bonus', '', 'If your plan applies your deferral election to bonuses, this part skips federal income tax withholding (FICA still applies).', '', '%') ?>
          </div>
        </details>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Net bonus after withholding</div>
          <div class="res-big" data-out="net">$0</div>
          <div class="res-sub" data-out="netSub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Federal withholding</small><b data-out="fed">$0</b></div>
            <div class="kpi"><small>Social Security + Medicare</small><b data-out="fica">$0</b></div>
            <div class="kpi"><small>State withholding</small><b data-out="state">$0</b></div>
            <div class="kpi"><small>Total withheld</small><b data-out="whRate">0%</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your bonus goes"></svg><ul class="legend" data-legend></ul></div>
          <div class="res-label">Actual federal income tax on the bonus</div>
          <div class="res-big" data-out="actual">$0</div>
          <div class="res-sub" data-out="actualSub">—</div>
          <div class="res-label" data-out="diffLabel">Over / under-withheld</div>
          <div class="res-big" data-out="diff">$0</div>
          <ul class="rows" data-rows></ul>
          <p class="note">Estimate only. Actual tax assumes the bonus is your only change and you take the standard deduction; aggregate method approximated with the IRS annual percentage method. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use the bonus tax calculator</h2>
      <p>Calculating tax on a bonus involves two different numbers, and this calculator shows both. The first is <strong>withholding</strong>: what your employer takes out of the bonus check before it hits your bank account. The second is your <strong>actual tax</strong>: the extra federal income tax the bonus adds to your return when you file. They are rarely the same, which is why a bonus can lead to a bigger refund or a surprise bill.</p>
      <ol>
        <li><strong>Enter the gross bonus</strong> and your regular annual salary from the same employer.</li>
        <li><strong>Pick your filing status and pay frequency.</strong> These drive the aggregate method and the actual-tax comparison.</li>
        <li><strong>Choose the withholding method.</strong> If the bonus is paid as its own check, your employer almost always uses the flat percentage method. If it is added to a regular paycheck with no separate amounts, choose aggregate.</li>
        <li><strong>Open “State tax &amp; 401(k)”</strong> to add a state supplemental rate or a 401(k) percentage taken from the bonus.</li>
      </ol>
      <p>The top half of the results is your net bonus. The bottom half compares the federal withholding with the tax the bonus really costs you, so you can see whether you are likely to get some of it back.</p>

      <h2 id="bonus-tax-rate">The <?= $Y ?> federal bonus tax rate</h2>
      <p>The IRS calls bonuses <strong>supplemental wages</strong>, a category that also covers commissions, overtime paid separately from regular wages, severance, back pay, awards and prizes. For <?= $Y ?> there are two federal withholding rates for supplemental wages paid by one employer:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Supplemental wages this calendar year</th><th class="n">Federal withholding</th></tr></thead><tbody>
        <tr><td>Up to $1,000,000</td><td class="n"><?= round($sup['rate'] * 100) ?>% (optional flat rate) or aggregate method</td></tr>
        <tr><td>Over $1,000,000</td><td class="n"><?= round($sup['over1mRate'] * 100) ?>% (mandatory)</td></tr>
      </tbody></table></div>
      <p>The flat <?= round($sup['rate'] * 100) ?>% option is only available if the employer withheld income tax from your regular wages this year or last year and the bonus is identified separately. The 37% rule applies to the portion of supplemental wages above $1 million no matter what you put on your W-4. On top of federal income tax, bonuses carry the same payroll taxes as regular pay: 6.2% Social Security up to the <?= money($y['ssWageBase']) ?> wage base and 1.45% Medicare, plus 0.9% Additional Medicare once your wages from that employer pass $200,000. Our guide to the <a href="/blog/bonus-tax-rate/">bonus tax rate</a> walks through every rule in detail.</p>

      <h2 id="formula">Bonus tax formula</h2>
      <div class="formula">Federal withholding = bonus × <?= round($sup['rate'] * 100) ?>% (portion over $1M × <?= round($sup['over1mRate'] * 100) ?>%)<br>FICA = bonus × 6.2% (until wage base) + bonus × 1.45%<br>Net bonus = bonus − federal − FICA − state − 401(k)<br>Actual tax on bonus = tax(salary + bonus) − tax(salary)<br>Over-withheld = federal withholding − actual tax</div>
      <p>Under the <strong>aggregate method</strong>, your employer adds the bonus to a regular paycheck, figures withholding on the combined amount as if you earned that much every pay period, and subtracts what it would have withheld on the regular check alone. Because the combined check is annualized, it often pushes withholding into a higher bracket for that one check, which is why aggregate withholding on a bonus can look painfully high.</p>

      <h2 id="example">Worked example: <?= money($ex['bonus']) ?> bonus on a <?= money($ex['salary']) ?> salary</h2>
      <p>A single filer earning <?= money($ex['salary']) ?> a year gets a <?= money($ex['bonus']) ?> bonus paid as a separate check in <?= $Y ?>, using the percentage method:</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Gross bonus</td><td class="n"><?= money($ex['bonus']) ?></td></tr>
        <tr><td>Federal withholding (<?= round($sup['rate'] * 100) ?>%)</td><td class="n">−<?= money($ex['fed']) ?></td></tr>
        <tr><td>Social Security (6.2%)</td><td class="n">−<?= money($ex['ss']) ?></td></tr>
        <tr><td>Medicare (1.45%)</td><td class="n">−<?= money($ex['med']) ?></td></tr>
        <tr><td><strong>Net bonus (before state tax)</strong></td><td class="n"><strong><?= money($ex['net']) ?></strong></td></tr>
        <tr><td>Federal tax on salary alone (after <?= money($ex['std']) ?> standard deduction)</td><td class="n"><?= money($ex['before']) ?></td></tr>
        <tr><td>Federal tax on salary + bonus</td><td class="n"><?= money($ex['after']) ?></td></tr>
        <tr><td><strong>Actual federal tax on the bonus</strong></td><td class="n"><strong><?= money($ex['actual']) ?></strong></td></tr>
        <tr><td>Over-withheld (comes back as a refund)</td><td class="n"><?= money($ex['diff']) ?></td></tr>
      </tbody></table></div>
      <p>This worker’s taxable income stays inside the 12% bracket even with the bonus, so the bonus only costs <?= money($ex['actual']) ?> of federal income tax, an effective <?= round($ex['rate'] * 100, 1) ?>%. The employer withheld <?= round($sup['rate'] * 100) ?>%, so roughly <?= money($ex['diff']) ?> comes back at tax time, assuming the rest of their withholding is accurate.</p>
      <p>If the same bonus were added to a biweekly paycheck under the aggregate method, federal withholding would be about <?= money($agg['fed']) ?> instead of <?= money($ex['fed']) ?>, because the combined check is annualized as if the worker earned <?= money(($ex['salary'] / 26 + $ex['bonus']) * 26) ?> a year.</p>

      <h2 id="by-salary">Withholding vs. actual tax by salary</h2>
      <p>The flat <?= round($sup['rate'] * 100) ?>% rate is one-size-fits-all, so it over-withholds for lower earners and under-withholds for higher earners. Here is a <?= money(10000) ?> bonus for a single filer in <?= $Y ?>:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Salary</th><th class="n">Withheld (<?= round($sup['rate'] * 100) ?>%)</th><th class="n">Actual tax</th><th class="n">Rate on bonus</th><th class="n">Difference</th></tr></thead><tbody>
<?php foreach ($rows as $r): ?>
        <tr><td><?= money($r['salary']) ?></td><td class="n"><?= money($r['fed']) ?></td><td class="n"><?= money($r['actual']) ?></td><td class="n"><?= number_format($r['rate'] * 100, 1) ?>%</td><td class="n"><?= abs($r['diff']) < 0.5 ? 'Matches' : ($r['diff'] > 0 ? money($r['diff']) . ' over' : money(-$r['diff']) . ' under') ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p>If your salary already puts you in the 24% bracket or higher, set aside the difference or raise your W-4 withholding so you are not hit with a balance due. The <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> shows how the whole year adds up.</p>

      <h2 id="why-so-high">Why bonus checks look heavily taxed</h2>
      <p>Bonuses are not taxed at a special higher rate. They are ordinary wages and end up taxed at your normal bracket rates on your Form 1040. What feels like extra tax usually comes from three things:</p>
      <ul>
        <li><strong>Stacked withholding.</strong> Federal (<?= round($sup['rate'] * 100) ?>%), Social Security and Medicare (7.65%) and state tax combined often take 30% to 40% of the check.</li>
        <li><strong>Aggregate annualizing.</strong> A large bonus inside a regular paycheck is withheld as if you earned that much all year.</li>
        <li><strong>Other deductions.</strong> Some employers also take a 401(k) percentage, garnishments or benefit deductions from bonus checks.</li>
      </ul>
      <div class="callout"><?= icon('spark') ?><p><strong>Key point:</strong> withholding is a prepayment, not the final bill. Anything over-withheld from a bonus is credited against your total tax when you file and comes back in your refund.</p></div>

      <h2 id="reduce">Ways to reduce tax on a bonus</h2>
      <ol>
        <li><strong>Send part of it to your 401(k).</strong> Pre-tax deferrals cut federal and most state income tax (but not FICA), up to the <?= money($y['k401']) ?> employee limit for <?= $Y ?>.</li>
        <li><strong>Fund an HSA</strong> if you have a high-deductible health plan; payroll HSA contributions also avoid FICA.</li>
        <li><strong>Time it.</strong> If you can choose between a December and January payout, take it in the year you expect a lower income.</li>
        <li><strong>Bunch deductions.</strong> A big bonus year can be a good year to group charitable gifts and itemize.</li>
      </ol>
      <p>State rules vary: some states use a flat supplemental rate, some use your regular withholding, and states with no wage income tax withhold nothing. Need the whole year’s picture? Try the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> or the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>, and if you want a bonus to land at an exact after-tax amount, use the <a href="/calculators/gross-up-calculator/">gross-up calculator</a>.</p>

<?= faq_block([
  ['How much tax is taken out of a bonus?', "<p>For a separately paid bonus, most employers withhold " . round($sup['rate'] * 100) . "% federal income tax, 6.2% Social Security (until you reach the " . money($y['ssWageBase']) . " wage base) and 1.45% Medicare, plus any state tax. A " . money($ex['bonus']) . " bonus typically nets about " . money($ex['net']) . " before state tax.</p>"],
  ['What is the bonus tax rate for ' . $Y . '?', "<p>The federal supplemental withholding rate is " . round($sup['rate'] * 100) . "% on bonuses up to \$1 million in a calendar year and " . round($sup['over1mRate'] * 100) . "% on the excess. That is a withholding rate only; your real tax on the bonus is your marginal bracket rate.</p>"],
  ['How do you calculate tax on a bonus?', "<p>For withholding, multiply the bonus by " . round($sup['rate'] * 100) . "% for federal tax and 7.65% for FICA, then apply your state rate. To find the tax you actually owe, compute your federal tax on salary plus bonus, then subtract the tax on salary alone. The calculator does both.</p>"],
  ['Will I get bonus tax back?', "<p>Possibly. If your marginal rate is below " . round($sup['rate'] * 100) . "% (roughly taxable income under " . money($y['brackets']['single'][1][0]) . " for a single filer), the flat rate over-withholds and the excess comes back as part of your refund. Social Security and Medicare are not refundable unless you had multiple employers and overpaid Social Security.</p>"],
  ['Are bonuses taxed higher than regular pay?', '<p>No. Bonuses are taxed at the same rates as your salary when you file. Only the withholding method differs, and the aggregate method can make a single check look heavily taxed.</p>'],
  ['Does a 401(k) contribution lower tax on my bonus?', '<p>Yes, if your plan applies your deferral election to bonuses. The deferred amount is excluded from federal income tax withholding and from your taxable wages, though Social Security and Medicare still apply.</p>'],
  ['What happens with a bonus over $1 million?', "<p>Supplemental wages above \$1 million from the same employer in one calendar year must be withheld at " . round($sup['over1mRate'] * 100) . "%. Enter earlier bonuses in “Supplemental wages already paid this year” and the calculator splits the bonus at the \$1 million mark.</p>"],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('bonus-tax-calculator', ['gross-up-calculator', 'paycheck-calculator', 'tax-refund-calculator', 'federal-income-tax', 'overtime-calculator', 'salary-to-hourly']) ?></div>
