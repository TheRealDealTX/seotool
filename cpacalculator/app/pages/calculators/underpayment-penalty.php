<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$due = $y['quarterlyDue'];
$P['title'] = "Estimated Tax Penalty Calculator $Y — IRS Form 2210 | CPA Calculator";
$P['description'] = "Free estimated tax penalty calculator for $Y. Figure the IRS underpayment penalty by quarter with the Form 2210 regular method, safe harbors and exceptions.";
$P['scripts'] = ['/assets/js/tools/underpayment-penalty.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Form 2210 regular method, mirrored by assets/js/tools/underpayment-penalty.js.
   Payments are applied to the earliest unpaid required installment first; each shortfall accrues
   interest at the quarterly rate × days ÷ (days in year) until paid or April 15 of the next year. */
function up_penalty(array $o): array {
  $Y = (int) $o['year'];
  $tz = new DateTimeZone('UTC');
  $due = array_map(fn($s) => (new DateTimeImmutable($s, $tz))->getTimestamp(), $o['due']);
  $end = (new DateTimeImmutable(($Y + 1) . '-04-15', $tz))->getTimestamp();
  $rates = $o['rates'];
  $interest = function (float $amt, int $from, int $to) use ($Y, $rates): float {
    $p = 0.0;
    for ($t = $from + 86400; $t <= $to; $t += 86400) {
      $yr = (int) gmdate('Y', $t); $m = (int) gmdate('n', $t);
      $i = $yr <= $Y ? ($m <= 6 ? 0 : ($m <= 9 ? 1 : 2)) : ($m <= 3 ? 3 : 4);
      $p += $amt * $rates[$i] / (365 + (int) gmdate('L', $t));
    }
    return $p;
  };
  $factor = $o['priorAgi'] > ($o['status'] === 'mfs' ? 75000 : 150000) ? 1.10 : 1.00;
  $rap = min(0.9 * $o['tax'], $factor * $o['priorTax']);
  $inst = $rap / 4;
  $pays = [];
  foreach ($due as $i => $t) $pays[] = ['amt' => $o['withheld'] / 4, 't' => $t, 'k' => 0];
  foreach ($o['payments'] as $i => [$amt, $date]) if ($amt > 0) $pays[] = ['amt' => $amt, 't' => (new DateTimeImmutable($date, $tz))->getTimestamp(), 'k' => 1];
  usort($pays, fn($a, $b) => [$a['t'], $a['k']] <=> [$b['t'], $b['k']]);
  $rem = array_fill(0, 4, $inst); $pen = array_fill(0, 4, 0.0); $late = []; $onTime = array_fill(0, 4, 0.0);
  foreach ($pays as $p) {
    $a = $p['amt'];
    for ($i = 0; $i < 4 && $a > 0.004; $i++) {
      if ($rem[$i] <= 0.004) continue;
      $use = min($a, $rem[$i]); $rem[$i] -= $use; $a -= $use;
      if ($p['t'] > $due[$i]) { $stop = min($p['t'], $end); $pen[$i] += $interest($use, $due[$i], $stop); $k = $i . '-' . $stop; $late[$k] = [$i, ($late[$k][1] ?? 0) + $use, (int) round(($stop - $due[$i]) / 86400)]; }
      else $onTime[$i] += $use;
    }
  }
  foreach ($rem as $i => $r) if ($r > 0.004) { $pen[$i] += $interest($r, $due[$i], $end); $k = $i . '-' . $end; $late[$k] = [$i, ($late[$k][1] ?? 0) + $r, (int) round(($end - $due[$i]) / 86400)]; }
  return ['factor' => $factor, 'rap' => $rap, 'inst' => $inst, 'pen' => $pen, 'total' => array_sum($pen), 'late' => array_values($late), 'onTime' => $onTime,
    'short' => array_map(fn($x) => $inst - $x, $onTime)];
}
$exPay = [[5000, date('Y-m-d', strtotime($due[0]))], [0, date('Y-m-d', strtotime($due[1]))], [5000, date('Y-m-d', strtotime($due[2]))], [5000, date('Y-m-d', strtotime($due[3]))]];
$ex = up_penalty(['year' => $Y, 'due' => $due, 'status' => 'single', 'tax' => 40000, 'withheld' => 10000, 'priorTax' => 30000, 'priorAgi' => 120000,
  'payments' => $exPay, 'rates' => [0.07, 0.07, 0.07, 0.07, 0.07]]);
$isoDue = array_map(fn($s) => date('Y-m-d', strtotime($s)), $due);
$short = fn($s) => preg_replace('/, \d{4}$/', '', $s);

/* Rate input for one calendar quarter of the penalty period (same markup as money_field with a % suffix). */
function up_rate_field(int $n, string $label): string {
  return '<div class="field"><label for="f-r' . $n . '"><span data-out="rl' . $n . '">' . e($label) . '</span></label><div class="inp suf" data-suf="%"><input id="f-r' . $n . '" name="r' . $n . '" inputmode="decimal" autocomplete="off" data-money value="7" placeholder="0"></div></div>';
}

echo tool_hero('underpayment-penalty', "Estimated Tax Penalty Calculator $Y",
  "Find out whether you owe the IRS underpayment penalty — and exactly how much. This calculator follows the Form 2210 regular method: it works out your required installments, applies each payment to the oldest shortfall first, and charges interest day by day until each quarter is caught up.",
  ['Form 2210 regular method', 'Payment dates & late payments', '90% / 100% / 110% safe harbors', '$1,000 and prior-year exceptions']);
?>
<section class="tool" aria-label="Estimated tax penalty calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="uppen-form" novalidate>
        <?= year_field() ?>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>This year’s tax</legend>
          <?= money_field('tax', 'Total tax after credits (incl. SE tax)', 40000, 'Form 1040 total tax (line 24) minus refundable credits such as the additional child tax credit and premium tax credit. Includes self-employment tax, additional Medicare tax and NIIT.') ?>
          <div id="up-wh-total"><?= money_field('withheld', 'Federal income tax withheld', 10000, 'W-2 Box 2, 1099 Box 4, pension and Social Security withholding for the year. Do not include estimated payments here.', 'Treated as paid evenly — 25% on each due date — the IRS default.') ?></div>
          <label class="check"><input type="checkbox" name="actualWh" value="1"> Use the dates my tax was actually withheld (Form 2210 box D)</label>
          <div id="up-wh-actual" hidden>
            <div class="grid-2">
              <?= money_field('wh1', 'Withheld Jan 1 – Mar 31', '', 'Federal withholding from paychecks dated in this period.') ?>
              <?= money_field('wh2', 'Withheld Apr 1 – May 31', '') ?>
            </div>
            <div class="grid-2">
              <?= money_field('wh3', 'Withheld Jun 1 – Aug 31', '') ?>
              <?= money_field('wh4', 'Withheld Sep 1 – Dec 31', '', 'Include year-end bonus withholding — a late-year boost only helps the fourth installment when you use actual dates.') ?>
            </div>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Last year’s return</legend>
          <div class="field"><label for="f-prior">Prior-year return</label><select id="f-prior" name="prior">
            <option value="filed">Filed a 12-month return showing tax</option>
            <option value="zero">Owed $0 tax (12-month year, US citizen/resident)</option>
            <option value="none">Didn’t file, or it was a short year</option>
          </select></div>
          <div class="grid-2" id="up-prior-fields">
            <?= money_field('priorTax', 'Prior-year total tax', 30000, 'Last year’s Form 1040 line 24 minus refundable credits.') ?>
            <?= money_field('priorAgi', 'Prior-year AGI', 120000, 'Form 1040 line 11. Over $150,000 ($75,000 married filing separately) raises the safe harbor to 110%.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Estimated tax payments (Form 1040-ES)</legend>
          <?php foreach ($due as $i => $d): $n = $i + 1; ?>
          <div class="grid-2">
            <?= money_field('pay' . $n, 'Q' . $n . ' payment (due ' . $short($d) . ')', [5000, '', 5000, 5000][$i], $n === 1 ? 'Amount of each estimated payment and the date the IRS received it. A payment made late is still credited — it just stops the penalty clock on that date.' : '') ?>
            <div class="field"><label for="f-pd<?= $n ?>">Date paid</label><div class="inp"><input type="date" id="f-pd<?= $n ?>" data-pdate="<?= $i ?>" value="<?= $isoDue[$i] ?>"></div></div>
          </div>
          <?php endforeach; ?>
          <label class="check"><input type="checkbox" name="jan31" value="1"> I filed my return and paid the full balance by January 31</label>
        </fieldset>
        <details class="more"><summary>Penalty interest rates by quarter</summary>
          <p class="hint" style="margin-top:0">The rate is the federal short-term rate plus 3 points, reset every calendar quarter. 7% is a placeholder — check the IRS quarterly interest rate announcement for the periods you were late.</p>
          <div class="grid-2">
            <?= up_rate_field(1, "Apr – Jun $Y") ?>
            <?= up_rate_field(2, "Jul – Sep $Y") ?>
          </div>
          <div class="grid-2">
            <?= up_rate_field(3, "Oct – Dec $Y") ?>
            <?= up_rate_field(4, 'Jan – Mar ' . ($Y + 1)) ?>
          </div>
          <?= up_rate_field(5, 'Apr 1 – 15, ' . ($Y + 1)) ?>
        </details>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Estimated underpayment penalty</div>
          <div class="res-big" data-out="pen">$0</div>
          <div class="res-sub" data-out="summary">—</div>
          <div class="kpis">
            <div class="kpi"><small>Required annual payment</small><b data-out="rap">$0</b></div>
            <div class="kpi"><small>Each installment (25%)</small><b data-out="inst">$0</b></div>
            <div class="kpi"><small>Paid late or unpaid</small><b data-out="lateAmt">$0</b></div>
            <div class="kpi"><small>Balance due at filing</small><b data-out="bal">$0</b></div>
          </div>
          <div class="res-label" style="margin-bottom:8px">Penalty by installment</div>
          <div class="quarters" data-quarters></div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="How your required annual payment was paid"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note" data-out="exnote">Estimate only. The IRS figures the final penalty and may compute it slightly differently. See <a href="/our-methodology/">our methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="what-is-the-penalty">What is the estimated tax penalty?</h2>
      <p>The US tax system is pay-as-you-go. Employers withhold from paychecks, and everyone else — freelancers, landlords, investors, retirees with large IRA withdrawals — is expected to send quarterly estimated payments. If you pay too little, too late, the IRS charges the <strong>underpayment of estimated tax penalty</strong> under Internal Revenue Code §6654, reported on <strong>Form 2210</strong>.</p>
      <p>Despite the name, it works like interest. Each quarter is tested separately: if a required installment wasn’t covered by its due date, the shortfall accrues a charge at the IRS underpayment rate (the federal short-term rate plus 3 percentage points) for every day it stays unpaid, up to the April 15 filing deadline. Paying a big lump sum in December doesn’t erase the penalty for the April and June installments you missed — it only stops the clock from that day forward.</p>

      <h2 id="how-to-use">How to use this underpayment penalty calculator</h2>
      <ol>
        <li><strong>Enter this year’s total tax.</strong> Use total tax after credits, including self-employment tax — the same figure Form 2210 starts from.</li>
        <li><strong>Enter withholding.</strong> By default the IRS treats withholding as paid in four equal parts on the due dates, even if most of it came out of a December bonus. Tick the box to use the actual withholding dates instead if that helps you.</li>
        <li><strong>Enter last year’s tax and AGI.</strong> These set the prior-year safe harbor: 100% of last year’s tax, or 110% if your AGI was over $150,000 ($75,000 married filing separately).</li>
        <li><strong>Enter each estimated payment and the date it was made.</strong> The <?= $Y ?> installment due dates are <?= e(implode(', ', $due)) ?>.</li>
        <li><strong>Check the rates.</strong> Each calendar quarter has its own rate; the calculator defaults to 7%, the rate that applied throughout 2025.</li>
      </ol>

      <h2 id="formula">The Form 2210 formula</h2>
      <div class="formula">Required annual payment = lesser of 90% × this year’s tax<br>&nbsp;&nbsp;or 100% × last year’s tax (110% if prior AGI &gt; $150,000)<br>Required installment = 25% × required annual payment<br>Underpayment = installment − payments credited by its due date<br>Penalty = underpayment × rate × days late ÷ 365</div>
      <p>Payments are applied to the <strong>earliest</strong> unpaid installment first. So if you skip the June payment and send a double payment in September, part of the September money is used to catch up June (ending June’s penalty on that date) and September is then short by the same amount. That cascade is why one missed quarter can produce penalties on three installments.</p>

      <h2 id="example">Worked example</h2>
      <p>A single filer owes $40,000 of total tax for <?= $Y ?>, had $10,000 withheld, and owed $30,000 last year with AGI of $120,000. She pays $5,000 of estimated tax on <?= e($short($due[0])) ?>, skips the <?= e($short($due[1])) ?> payment, and pays $5,000 on time in <?= e(explode(' ', $due[2])[0]) ?> and <?= e(explode(' ', $due[3])[0]) ?>.</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>90% of this year’s tax</td><td class="n"><?= money(36000) ?></td></tr>
        <tr><td>100% of last year’s tax (AGI under $150,000)</td><td class="n"><?= money(30000) ?></td></tr>
        <tr><td>Required annual payment (smaller of the two)</td><td class="n"><?= money($ex['rap']) ?></td></tr>
        <tr><td>Required installment (÷ 4)</td><td class="n"><?= money($ex['inst']) ?></td></tr>
        <tr><td>Withholding credited per quarter (÷ 4)</td><td class="n"><?= money(2500) ?></td></tr>
        <?php foreach ($ex['late'] as [$i, $amt, $days]): ?>
        <tr><td>Q<?= $i + 1 ?> shortfall of <?= money($amt) ?> outstanding <?= (int) $days ?> days</td><td class="n"><?= money($amt * 0.07 * $days / 365, 2) ?></td></tr>
        <?php endforeach; ?>
        <tr><td><strong>Total penalty at 7%</strong></td><td class="n"><strong><?= money($ex['total'], 2) ?></strong></td></tr>
      </tbody></table></div>
      <p>The June shortfall is caught up by the September payment, which leaves September short; the January payment catches up September, which leaves the fourth installment short until the return is filed on April 15. She still owes the remaining <?= money(40000 - 10000 - 15000) ?> balance with her return — but had she simply paid <?= money($ex['inst'] - 2500) ?> each quarter (prior-year safe harbor), the penalty would have been zero.</p>

      <h2 id="exceptions">When you owe no penalty</h2>
      <ul>
        <li><strong>The $1,000 rule.</strong> If your total tax minus withholding (and refundable credits) is under $1,000, there is no penalty, whatever your payment pattern. Estimated payments don’t count toward this test — only withholding does.</li>
        <li><strong>Zero tax last year.</strong> If last year was a full 12-month tax year, you were a US citizen or resident the whole year, and your total tax was $0, there is no penalty this year. This is what protects many people in their <a href="/blog/do-i-have-to-pay-quarterly-taxes-my-first-year/">first year of self-employment</a>.</li>
        <li><strong>Safe harbors met on time.</strong> Withholding plus timely payments reaching 90% of this year’s tax, or 100%/110% of last year’s, in each quarter.</li>
        <li><strong>File and pay by January 31.</strong> If you file your return and pay the whole balance by January 31, you don’t owe a penalty for the fourth installment.</li>
        <li><strong>Farmers and fishermen</strong> who get at least two-thirds of gross income from farming or fishing use a 66⅔% test and a single January 15 installment, or can file and pay by March 1.</li>
      </ul>

      <h2 id="waivers">Penalty waivers</h2>
      <p>The IRS can waive all or part of the penalty (Form 2210 boxes A and B) if:</p>
      <ul>
        <li>the underpayment was caused by a <strong>casualty, disaster or other unusual circumstance</strong> and imposing it would be inequitable; or</li>
        <li>you <strong>retired after reaching age 62</strong> or <strong>became disabled</strong> during the tax year or the year before, and the underpayment was due to reasonable cause rather than willful neglect.</li>
      </ul>
      <p>Taxpayers in federally declared disaster areas often get automatic postponements of the due dates. Note that the IRS “first-time abatement” policy covers failure-to-file and failure-to-pay penalties, <em>not</em> the estimated tax penalty.</p>

      <h2 id="annualized">Uneven income? The annualized method</h2>
      <p>The regular method assumes income arrives evenly. If most of your income came late in the year — a fourth-quarter capital gain, a big December contract, a year-end bonus without withholding — the <strong>annualized income installment method</strong> (Form 2210 Schedule AI, box C) can lower or eliminate the penalty. It recalculates each required installment from the income you actually earned through March 31, May 31, August 31 and December 31, using annualization factors of 4, 2.4, 1.5 and 1. This calculator uses the regular method, so treat its result as the upper bound if your income was back-loaded.</p>

      <div class="callout"><?= icon('spark') ?><p><strong>Avoid it next year:</strong> use our <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> to set your safe-harbor payments, or increase W-4 withholding — withholding late in the year still counts as paid evenly. The <a href="/blog/quarterly-taxes-101-guide/">quarterly taxes guide</a> explains how to pay.</p></div>

<?= faq_block([
  ['How is the estimated tax penalty calculated?', '<p>Each quarterly installment is 25% of the required annual payment (the lesser of 90% of this year’s tax or 100%/110% of last year’s). For every installment not covered by its due date, the IRS charges the underpayment interest rate on the shortfall for each day it remains unpaid, up to April 15. Payments go to the oldest shortfall first.</p>'],
  ['What is the IRS underpayment penalty rate?', '<p>It equals the federal short-term rate plus 3 percentage points, rounded to a whole percent and reset every calendar quarter. It was 7% throughout 2025. Check the IRS quarterly interest rate news release for the periods you need, and enter them in the rate fields above.</p>'],
  ['Will I owe a penalty if I owe less than $1,000?', '<p>No. If your total tax minus withholding and refundable credits is under $1,000, no penalty applies. Estimated payments don’t count toward this test.</p>'],
  ['Do I have to file Form 2210?', '<p>Usually not. If you owe a penalty, the IRS will figure it and send a bill, or tax software computes it for you. You must file Form 2210 when you request a waiver, use the annualized income method, treat withholding as paid on actual dates, or base your required payment on a joint return filed in only one of the two years.</p>'],
  ['Can the IRS waive the underpayment penalty?', '<p>Yes, for a casualty, disaster or other unusual circumstance, or if you retired after age 62 or became disabled in the tax year or the prior year and had reasonable cause. Request it on Form 2210 with an explanation. First-time abatement does not apply to this penalty.</p>'],
  ['Is the underpayment penalty tax-deductible?', '<p>No. The estimated tax penalty is not deductible, even for business owners.</p>'],
  ['Does extra withholding in December avoid the penalty?', '<p>Often, yes. Withholding is treated as paid evenly through the year unless you choose otherwise, so a large December withholding — from a bonus or a W-4 change — counts as if a quarter of it was paid on each due date. Estimated payments don’t get that treatment.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('underpayment-penalty', ['quarterly-estimated-tax', 'self-employment-tax', '1099-tax-calculator', 'tax-refund-calculator', 'federal-income-tax', 'paycheck-calculator']) ?></div>
