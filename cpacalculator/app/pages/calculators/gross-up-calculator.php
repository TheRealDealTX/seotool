<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Gross Up Calculator $Y: Net to Gross Pay | CPA Calculator";
$P['description'] = "Free $Y gross up calculator. Find the gross bonus or payment that nets an exact amount after 22% federal withholding, Social Security, Medicare and state tax.";
$P['scripts'] = ['/assets/js/tools/gross-up-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

$sup = $y['supplemental'];
/* Server-side mirror of the calculator: binary search on gross so that gross − taxes = net. */
function grossup_ex(float $net, string $method = 'flat', float $state = 0, float $salary = 75000, int $freq = 26, float $ytd = 0, string $status = 'single'): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $std = $y['std'][$status];
  $taxes = function (float $g) use ($y, $method, $state, $salary, $freq, $ytd, $status, $std): array {
    $under = min($g, 1000000); $over = max(0, $g - 1000000);
    if ($method === 'aggregate') {
      $per = $salary / $freq;
      $t = fn(float $w): float => fed_tax(max(0, $w * $freq - $std), $status)['tax'] / $freq;
      $fed = $t($per + $under) - $t($per);
    } else {
      $fed = $under * $y['supplemental']['rate'];
    }
    $fed += $over * $y['supplemental']['over1mRate'];
    $base = $y['ssWageBase'];
    $ss = max(0, min($ytd + $g, $base) - min($ytd, $base)) * 0.062;
    $med = $g * 0.0145 + (max(0, $ytd + $g - 200000) - max(0, $ytd - 200000)) * 0.009;
    $st = $g * $state;
    return ['fed' => $fed, 'ss' => $ss, 'med' => $med, 'state' => $st, 'net' => $g - $fed - $ss - $med - $st];
  };
  $lo = $net; $hi = $net * 2;
  while ($taxes($hi)['net'] < $net) $hi *= 2;
  for ($i = 0; $i < 100; $i++) { $mid = ($lo + $hi) / 2; if ($taxes($mid)['net'] < $net) $lo = $mid; else $hi = $mid; }
  $gross = round($hi, 2);
  return ['gross' => $gross, 'net' => $net] + $taxes($gross);
}
$ex = grossup_ex(5000);
$exState = grossup_ex(5000, 'flat', 0.05);
$exAgg = grossup_ex(5000, 'aggregate');
$exCap = grossup_ex(5000, 'flat', 0, 75000, 26, 182000);
$rate = $sup['rate'] + 0.0765;
$amounts = [1000, 2500, 5000, 10000, 25000];

echo tool_hero('gross-up-calculator', "Gross Up Calculator $Y",
  "Work backward from the check you want someone to receive. Enter the net amount and this gross-up calculator finds the gross payment that covers federal withholding, Social Security, Medicare and state tax, using the " . round($sup['rate'] * 100) . "% supplemental rate or the aggregate method with the employee’s salary.",
  ['Net-to-gross in one step', 'Flat 22% or aggregate', 'Social Security wage base', 'Formula shown']);
?>
<section class="tool" aria-label="Gross up calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="grossup-form" novalidate>
        <?= year_field() ?>
        <fieldset class="fieldset"><legend>Amount</legend>
          <?= money_field('net', 'Desired net (take-home) amount', 5000, 'The exact amount the employee should receive after taxes, e.g. a $5,000 bonus “after taxes” or a relocation reimbursement.') ?>
          <input type="range" min="0" max="50000" step="100" data-range-for="net" aria-label="Net amount slider">
        </fieldset>
        <fieldset class="fieldset"><legend>Federal withholding method</legend>
          <div class="field"><span class="lbl">Method</span><div class="seg" role="radiogroup" aria-label="Withholding method">
            <label><input type="radio" name="method" value="flat" checked><span>Supplemental flat <?= round($sup['rate'] * 100) ?>%</span></label>
            <label><input type="radio" name="method" value="aggregate"><span>Aggregate (with salary)</span></label>
          </div></div>
          <div data-agg-only hidden>
            <?= status_field() ?>
            <div class="grid-2">
              <?= money_field('salary', 'Employee’s annual salary', 75000, 'Regular annual wages. Under the aggregate method the payment is added to a regular paycheck and withheld as if earned every period.') ?>
              <div class="field"><label for="f-freq">Pay frequency</label><select id="f-freq" name="freq">
                <option value="52">Weekly</option><option value="26" selected>Every two weeks</option><option value="24">Twice a month</option><option value="12">Monthly</option>
              </select></div>
            </div>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Payroll &amp; state taxes</legend>
          <label class="check"><input type="checkbox" name="fica" checked> Include Social Security and Medicare (FICA)</label>
          <div class="grid-2">
            <?= money_field('ytdWages', 'Wages paid so far this year', '', 'Year-to-date wages before this payment. Social Security (6.2%) stops at the ' . money($y['ssWageBase']) . ' wage base; 0.9% Additional Medicare starts above $200,000.', 'Leave blank if well under the wage base.') ?>
            <?= money_field('stateRate', 'State (and local) tax rate', '', 'Your state’s supplemental or flat withholding rate. Enter 0 for states with no wage income tax.', '', '%') ?>
          </div>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Gross payment needed</div>
          <div class="res-big" data-out="gross">$0</div>
          <div class="res-sub" data-out="grossSub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Federal withholding</small><b data-out="fed">$0</b></div>
            <div class="kpi"><small>Social Security + Medicare</small><b data-out="fica">$0</b></div>
            <div class="kpi"><small>State tax</small><b data-out="state">$0</b></div>
            <div class="kpi"><small>Total tax rate on gross</small><b data-out="rate">0%</b></div>
          </div>
          <div class="formula" data-out="formula">—</div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Gross payment breakdown"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note">Estimate of withholding on the payment; the employee’s final tax depends on their whole return. Aggregate method approximated with the IRS annual percentage method. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="what-is-gross-up">What is a gross-up?</h2>
      <p>A gross-up is an extra amount added to a payment so the taxes on it are covered and the recipient ends up with a specific net amount. Employers gross up bonuses (“$5,000 after taxes”), relocation and moving reimbursements, sign-on awards, gift cards and other taxable fringe benefits, and settlement payments. Because the gross-up itself is also taxable wages, you can’t just add the taxes on the net amount; you have to solve for the gross that leaves the right amount after taxes on the whole thing. This gross up calculator does that instantly.</p>

      <h2 id="how-to-use">How to use the gross up calculator</h2>
      <ol>
        <li><strong>Enter the net amount</strong> the employee should receive.</li>
        <li><strong>Pick the federal method.</strong> Most payroll systems withhold a flat <?= round($sup['rate'] * 100) ?>% on supplemental wages paid separately. Choose aggregate if the payment rides along with a regular paycheck, then enter the employee’s salary, pay frequency and filing status.</li>
        <li><strong>Set payroll and state taxes.</strong> Keep FICA on for normal wages, add year-to-date wages if the employee is near the <?= money($y['ssWageBase']) ?> Social Security wage base, and enter your state supplemental rate.</li>
      </ol>
      <p>The result shows the gross payment, a breakdown of every tax, and the exact formula used.</p>

      <h2 id="formula">Gross-up formula</h2>
      <p>When every tax is a flat percentage, the gross-up formula is simple: divide the net amount by one minus the total tax rate.</p>
      <div class="formula">Gross = Net ÷ (1 − total tax rate)<br>Total tax rate = federal <?= round($sup['rate'] * 100) ?>% + Social Security 6.2% + Medicare 1.45% + state %<br>= <?= round($sup['rate'] * 100) ?>% + 7.65% + state = <?= number_format($rate * 100, 2) ?>% + state</div>
      <p>With no state tax, a <?= money(5000) ?> net payment needs <?= money(5000) ?> ÷ (1 − <?= number_format($rate, 4) ?>) = <strong><?= money($ex['gross'], 2) ?></strong>. The rate changes when the payment crosses the Social Security wage base (6.2% stops), reaches $200,000 of wages (0.9% Additional Medicare starts) or pushes supplemental wages over $1 million (federal jumps to <?= round($sup['over1mRate'] * 100) ?>%). In those cases, and for the aggregate method where federal withholding depends on salary, the calculator solves for gross numerically: it searches for the gross amount where gross minus all taxes equals your target, to the cent.</p>
      <div class="callout warn"><?= icon('shield') ?><p><strong>Common mistake:</strong> adding 29.65% to the net amount ($5,000 × 1.2965 = $6,482.50) under-grosses the payment. Taxes apply to the gross-up too, so the correct figure is <?= money($ex['gross'], 2) ?>.</p></div>

      <h2 id="example">Worked example: <?= money($ex['net']) ?> net bonus</h2>
      <p>An employer wants an employee to take home exactly <?= money($ex['net']) ?> from a separately paid bonus in <?= $Y ?>, with the flat supplemental method and the employee below the Social Security wage base:</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Gross bonus</td><td class="n"><?= money($ex['gross'], 2) ?></td></tr>
        <tr><td>Federal withholding (<?= round($sup['rate'] * 100) ?>%)</td><td class="n">−<?= money($ex['fed'], 2) ?></td></tr>
        <tr><td>Social Security (6.2%)</td><td class="n">−<?= money($ex['ss'], 2) ?></td></tr>
        <tr><td>Medicare (1.45%)</td><td class="n">−<?= money($ex['med'], 2) ?></td></tr>
        <tr><td><strong>Net to employee</strong></td><td class="n"><strong><?= money($ex['net'], 2) ?></strong></td></tr>
        <tr><td>Gross-up (taxes covered by employer)</td><td class="n"><?= money($ex['gross'] - $ex['net'], 2) ?></td></tr>
      </tbody></table></div>
      <p>Other scenarios for the same <?= money($ex['net']) ?> net:</p>
      <ul>
        <li><strong>With a 5% state tax:</strong> gross is <?= money($exState['gross'], 2) ?> (<?= money(5000) ?> ÷ (1 − <?= number_format($rate + 0.05, 4) ?>)).</li>
        <li><strong>Aggregate method, <?= money(75000) ?> salary paid biweekly, single:</strong> gross is <?= money($exAgg['gross'], 2) ?>, because the combined paycheck is withheld at higher bracket rates.</li>
        <li><strong>Employee already at <?= money(182000) ?> of wages:</strong> only part of the payment owes Social Security before the <?= money($y['ssWageBase']) ?> wage base is reached, so gross drops to <?= money($exCap['gross'], 2) ?>.</li>
      </ul>

      <h2 id="by-hand">How to gross up a payment by hand</h2>
      <ol>
        <li><strong>Add up the tax rates</strong> that apply to the payment: federal supplemental, Social Security (if the employee is under the wage base), Medicare and state.</li>
        <li><strong>Subtract the total from 1.</strong> At <?= number_format($rate * 100, 2) ?>% with no state tax, that leaves <?= number_format(1 - $rate, 4) ?>.</li>
        <li><strong>Divide the net amount by that number</strong> to get the gross payment.</li>
        <li><strong>Check your work:</strong> multiply the gross by each rate, subtract the taxes, and confirm the result equals the target net. Round to the cent and adjust by a penny if needed.</li>
      </ol>
      <p>If the employee will cross the Social Security wage base partway through the payment, split it: gross up the part below the base at the full rate and the part above it without the 6.2%, or let the calculator do the search for you.</p>

      <h2 id="table">Gross-up table (<?= $Y ?>, flat <?= round($sup['rate'] * 100) ?>% + FICA, no state tax)</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Net amount</th><th class="n">Gross needed</th><th class="n">Federal</th><th class="n">FICA</th><th class="n">Gross-up</th></tr></thead><tbody>
<?php foreach ($amounts as $a): $g = grossup_ex($a); ?>
        <tr><td><?= money($a) ?></td><td class="n"><?= money($g['gross'], 2) ?></td><td class="n"><?= money($g['fed'], 2) ?></td><td class="n"><?= money($g['ss'] + $g['med'], 2) ?></td><td class="n"><?= money($g['gross'] - $a, 2) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>

      <h2 id="when">When employers gross up payments</h2>
      <ul>
        <li><strong>Bonuses promised “net”.</strong> Holiday or spot bonuses where the employee should see a round number. See how bonuses are normally taxed with the <a href="/calculators/bonus-tax-calculator/">bonus tax calculator</a> and our <a href="/blog/bonus-tax-rate/">bonus tax rate guide</a>.</li>
        <li><strong>Relocation benefits.</strong> Moving expense reimbursements are taxable wages for most employees, so many relocation packages include a gross-up.</li>
        <li><strong>Taxable fringe benefits.</strong> Gift cards, awards that don’t qualify as tax-free achievement awards, and personal use of a company car are all wages.</li>
        <li><strong>Executive and settlement payments.</strong> Contracts sometimes require the company to cover the tax on a payment.</li>
      </ul>
      <p>The employer also pays its own share of Social Security and Medicare (7.65%) on the full gross amount, plus federal and state unemployment taxes where they apply, so the total cost of a gross-up is higher than the gross figure.</p>

      <h2 id="withholding-vs-tax">Withholding vs. the employee’s actual tax</h2>
      <p>A gross-up covers <em>withholding</em>, not necessarily the employee’s final tax. If the employee’s marginal rate is 24% or higher, the <?= round($sup['rate'] * 100) ?>% withheld may not cover the full federal tax on the payment; if it’s 12%, they’ll get some back as a refund. Some employers gross up at the employee’s marginal rate instead. To see what the payment really adds to a tax bill, use the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> or the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>.</p>

<?= faq_block([
  ['How do you calculate a gross-up?', "<p>Divide the net amount by one minus the total tax rate. With " . round($sup['rate'] * 100) . "% federal and 7.65% FICA, the rate is " . number_format($rate * 100, 2) . "%, so a " . money(5000) . " net payment needs " . money(5000) . " ÷ " . number_format(1 - $rate, 4) . " = " . money($ex['gross'], 2) . " gross.</p>"],
  ['What is the gross-up formula?', '<p>Gross = Net ÷ (1 − tax rate). Use the combined federal, Social Security, Medicare and state rate as a decimal. If the payment crosses the Social Security wage base or uses aggregate withholding, solve iteratively as this calculator does.</p>'],
  ['Why not just add the tax to the net amount?', '<p>Because the extra money is taxable too. Adding 29.65% to $5,000 gives $6,482.50, but after 29.65% of taxes on that amount the employee only nets about $4,560. The gross-up formula accounts for tax on the tax.</p>'],
  ['What tax rate should I use to gross up a bonus?', "<p>Most employers use the federal supplemental rate of " . round($sup['rate'] * 100) . "% (" . round($sup['over1mRate'] * 100) . "% on supplemental wages over \$1 million), 6.2% Social Security up to the " . money($y['ssWageBase']) . " wage base, 1.45% Medicare, and the state’s supplemental rate.</p>"],
  ['Does a gross-up include Social Security and Medicare?', '<p>Usually, yes. FICA is withheld from wages, so a gross-up meant to deliver an exact net amount must cover it. Turn off the FICA option for payments that aren’t subject to it.</p>'],
  ['Is a grossed-up payment reported on the W-2?', '<p>Yes. The full gross amount, including the gross-up, is taxable wages reported on the employee’s Form W-2, and the withholding is credited against their tax for the year.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('gross-up-calculator', ['bonus-tax-calculator', 'paycheck-calculator', 'federal-income-tax', 'salary-to-hourly', 'tax-refund-calculator', 'overtime-calculator']) ?></div>
