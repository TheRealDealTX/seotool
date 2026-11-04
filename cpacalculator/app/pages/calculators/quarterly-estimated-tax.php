<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$due = $y['quarterlyDue'];
$P['title'] = "Quarterly Estimated Tax Calculator $Y — 1040-ES Safe Harbor | CPA Calculator";
$P['description'] = "Free $Y quarterly estimated tax calculator. Find each 1040-ES payment amount, the 100%/110% safe harbor, $Y due dates and the first-year no-penalty rule.";
$P['scripts'] = ['/assets/js/tools/quarterly-estimated-tax.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Worked example: mirrors the JS engine (single, 1099 income only, standard deduction, QBI). */
function qet_example(float $net, string $status = 'single'): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $base = $net * 0.9235;
  $se = min($base, $y['ssWageBase']) * 0.124 + $base * 0.029;
  $agi = $net - $se / 2;
  $before = max(0, $agi - $y['std'][$status]);
  $qbi = min(($net - $se / 2) * 0.2, $before * 0.2);
  $inc = fed_tax(max(0, $before - $qbi), $status)['tax'];
  return ['se' => $se, 'inc' => $inc, 'total' => $se + $inc, 'agi' => $agi];
}
$ex = qet_example(70000);
$exPrior = 9000;
$ex90 = $ex['total'] * 0.9;
$exReq = min($ex90, $exPrior);
$priorYear = $Y - 1;

echo tool_hero('quarterly-estimated-tax', "Quarterly Estimated Tax Calculator $Y",
  "Figure out exactly what to send the IRS each quarter. Enter this year’s expected income and last year’s tax to see your safe-harbor minimum, the 90% current-year amount, a payment plan for every $Y due date, and whether the first-year rule means you owe no penalty at all.",
  ['100% / 110% safe harbor', '2026 Form 1040-ES due dates', 'First-year no-penalty check', 'Tracks payments already made']);
?>
<section class="tool" aria-label="Quarterly estimated tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="qet-form" novalidate>
        <?= year_field() ?>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>This year’s expected income</legend>
          <div class="grid-2">
            <?= money_field('seIncome', '1099 / self-employment income', 85000, 'Gross 1099-NEC, 1099-K and other business receipts you expect for the full year.') ?>
            <?= money_field('seExpenses', 'Business expenses', 15000, 'Expected deductible business costs (Schedule C).') ?>
          </div>
          <div class="grid-2">
            <?= money_field('wages', 'W-2 wages', '', 'Expected salary from any job this year (W-2 Box 1).') ?>
            <?= money_field('otherIncome', 'Other income', '', 'Interest, dividends, rental profit, unemployment, retirement distributions and other taxable income.') ?>
          </div>
          <details class="more"><summary>Deductions &amp; credits</summary>
            <div class="grid-2">
              <?= money_field('adjust', 'Adjustments to income', '', 'SEP-IRA / Solo 401(k) contributions, self-employed health insurance, traditional IRA, HSA — anything that reduces AGI.') ?>
              <?= money_field('itemized', 'Itemized deductions (if larger)', '', 'Used only if larger than the ' . money($y['std']['single']) . ' (single) standard deduction. SALT is capped at ' . money($y['saltCap']) . '.') ?>
            </div>
            <div class="field"><label for="f-kids">Children under 17</label><select id="f-kids" name="kids"><?php for ($i = 0; $i <= 6; $i++) echo "<option value=\"$i\">$i</option>"; ?></select><span class="hint">Child Tax Credit: <?= money($y['ctc']['amount']) ?> each, up to <?= money($y['ctc']['refundable']) ?> refundable</span></div>
          </details>
        </fieldset>
        <fieldset class="fieldset"><legend>Withholding &amp; payments</legend>
          <div class="grid-2">
            <?= money_field('withheld', 'Federal withholding for the year', '', 'Total federal income tax withheld from paychecks (W-2 Box 2), pensions or unemployment for the full year. The IRS treats withholding as paid evenly.') ?>
            <?= money_field('paid', 'Estimated payments already made', '', 'Total 1040-ES payments already sent for this tax year, including any prior-year overpayment applied.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Last year (<?= $priorYear ?>) — for the safe harbor</legend>
          <div class="grid-2">
            <?= money_field('priorTax', 'Total tax on last year’s return', 9000, 'Form 1040 line 24 minus refundable credits. Enter 0 if you owed no tax. Leave blank if you don’t know.', 'Not your refund or balance due.') ?>
            <?= money_field('priorAgi', 'Last year’s AGI', 60000, 'Form 1040 line 11. Above $150,000 ($75,000 married filing separately) the safe harbor rises to 110%.') ?>
          </div>
          <label class="check"><input type="checkbox" name="fullYear" checked> Last year’s return covered a full 12 months and I was a U.S. citizen or resident all year</label>
          <label class="check"><input type="checkbox" name="farmer"> At least two-thirds of my gross income is from farming or fishing</label>
        </fieldset>
        <div class="field"><span class="lbl">Payment plan</span><div class="seg" role="radiogroup" aria-label="Payment plan">
          <label><input type="radio" name="plan" value="safe" checked><span>Minimum to avoid a penalty</span></label>
          <label><input type="radio" name="plan" value="full"><span>Pay the full projected tax</span></label>
        </div></div>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="label">Recommended payment per quarter</div>
          <div class="res-big" data-out="perq">$0</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Projected <span data-out="yr"><?= $Y ?></span> tax</small><b data-out="tax">$0</b></div>
            <div class="kpi"><small>Required annual payment</small><b data-out="req">$0</b></div>
            <div class="kpi"><small>Still to pay this year</small><b data-out="left">$0</b></div>
            <div class="kpi"><small data-out="balLabel">Due when you file</small><b data-out="bal">$0</b></div>
          </div>
          <div class="res-label" style="margin-bottom:8px">Form 1040-ES payment schedule</div>
          <div class="quarters" data-quarters></div>
          <ul class="rows" data-rows></ul>
          <p class="note">Assumes equal installments. If your income arrives unevenly, the annualized income installment method (Form 2210, Schedule AI) can lower early payments. Excludes state tax. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="what-are-estimated-taxes">What are quarterly estimated taxes?</h2>
      <p>The U.S. tax system is pay-as-you-go. Employees pay through paycheck withholding; anyone with income that isn’t withheld on — freelance and 1099 work, a side business, rental income, investment gains, alimony from pre-2019 divorces — is expected to send money to the IRS during the year using <strong>Form 1040-ES</strong>. Those four installments are your quarterly estimated taxes. They cover both income tax and <a href="/calculators/self-employment-tax/">self-employment tax</a>.</p>
      <p>You generally must make estimated payments if you expect to owe <strong>$1,000 or more</strong> when you file, after subtracting withholding and refundable credits. Skip them and the IRS adds an underpayment penalty, figured like interest on each late installment.</p>

      <h2 id="how-to-use">How to use this quarterly estimated tax calculator</h2>
      <ol>
        <li><strong>Enter this year’s expected income.</strong> Best guesses are fine — you can re-run the numbers each quarter as the year unfolds. Include business expenses so the calculator works from net profit.</li>
        <li><strong>Add withholding and payments.</strong> If you or your spouse have a W-2 job, withholding counts toward your required payments, and the IRS treats it as paid evenly through the year no matter when it was taken out.</li>
        <li><strong>Enter last year’s total tax and AGI.</strong> That’s Form 1040 line 24 (total tax) and line 11 (AGI) from your <?= $priorYear ?> return. These unlock the prior-year safe harbor, which is usually the easiest way to guarantee no penalty.</li>
        <li><strong>Choose a plan.</strong> “Minimum to avoid a penalty” pays the safe-harbor amount; “Pay the full projected tax” aims for a $0 balance in April.</li>
      </ol>

      <h2 id="safe-harbor">Safe-harbor rules: how much you must pay</h2>
      <p>You won’t owe an underpayment penalty if your withholding plus timely estimated payments reach the <strong>smaller</strong> of these two amounts — called the required annual payment:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Test</th><th>Required payment</th><th>Notes</th></tr></thead><tbody>
        <tr><td>Current-year</td><td>90% of this year’s tax</td><td>Requires an accurate projection; 66⅔% for qualifying farmers and fishermen</td></tr>
        <tr><td>Prior-year</td><td>100% of last year’s tax</td><td>Only if last year’s return covered 12 months</td></tr>
        <tr><td>Prior-year, high income</td><td>110% of last year’s tax</td><td>If last year’s AGI exceeded $150,000 ($75,000 married filing separately); does not apply to farmers/fishermen</td></tr>
        <tr><td>Small balance</td><td>No payments needed</td><td>If tax after withholding and refundable credits is under $1,000</td></tr>
      </tbody></table></div>
      <p>The prior-year test is popular because you know the number in advance. Even if your income doubles this year, paying 100% (or 110%) of last year’s tax in four equal installments means no penalty — you simply settle the rest when you file.</p>
      <div class="formula">Required annual payment = min(90% × current-year tax, 100% or 110% × prior-year tax)<br>Each installment = (required annual payment − withholding) ÷ 4<br>Balance due at filing = current-year tax − withholding − estimated payments</div>

      <h2 id="first-year">Do I have to pay quarterly taxes my first year?</h2>
      <p>It depends on what you owed last year — not on whether this is your first year self-employed. The tax code has a specific exception (Internal Revenue Code §6654(e)(2)): <strong>you owe no underpayment penalty for this year if all three of these are true</strong>:</p>
      <ol>
        <li>You had <strong>no total tax liability</strong> for last year (Form 1040 line 24 was zero, or you weren’t required to file),</li>
        <li>last year was a <strong>full 12-month</strong> tax year, and</li>
        <li>you were a <strong>U.S. citizen or resident</strong> for all of last year.</li>
      </ol>
      <p>“No liability” means zero tax, not “I got a refund.” Many people starting a business had a W-2 job last year and paid tax through withholding. They don’t qualify for the first-year exception, but they get something nearly as good: the prior-year safe harbor. If last year’s total tax was $4,000, paying $4,000 this year ($1,000 a quarter, or a mix of withholding and estimates) protects you from penalties no matter how much your new business earns.</p>
      <div class="callout warn"><?= icon('spark') ?><p><strong>No penalty isn’t no tax.</strong> The first-year rule only removes the penalty. You’ll still owe the full balance — income tax plus 15.3% self-employment tax — by April 15, <?= $Y + 1 ?>. Setting aside 25–30% of each payment as it arrives avoids a painful surprise. Our guide covers this in depth: <a href="/blog/do-i-have-to-pay-quarterly-taxes-my-first-year/">Do I have to pay quarterly taxes my first year?</a></p></div>
      <p>To check it here, enter <strong>0</strong> as last year’s total tax and keep the 12-month box ticked; the calculator will flag the exception and still show what to set aside.</p>

      <h2 id="example">Worked example</h2>
      <p>A single freelancer expects $85,000 of 1099 income and $15,000 of expenses in <?= $Y ?> (net profit $70,000), with no W-2 job. Last year’s total tax was <?= money($exPrior) ?> and AGI was $60,000.</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Projected self-employment tax</td><td class="n"><?= money($ex['se']) ?></td></tr>
        <tr><td>Projected income tax (after standard deduction and QBI)</td><td class="n"><?= money($ex['inc']) ?></td></tr>
        <tr><td>Projected <?= $Y ?> total tax</td><td class="n"><?= money($ex['total']) ?></td></tr>
        <tr><td>90% of current-year tax</td><td class="n"><?= money($ex90) ?></td></tr>
        <tr><td>100% of prior-year tax (AGI under $150,000)</td><td class="n"><?= money($exPrior) ?></td></tr>
        <tr><td><strong>Required annual payment (smaller)</strong></td><td class="n"><strong><?= money($exReq) ?></strong></td></tr>
        <tr><td>Each quarterly payment</td><td class="n"><?= money($exReq / 4) ?></td></tr>
        <tr><td>Balance due at filing</td><td class="n"><?= money($ex['total'] - $exReq) ?></td></tr>
      </tbody></table></div>
      <p>Paying <?= money($exReq / 4) ?> on each due date avoids any penalty. To owe nothing in April instead, the freelancer would pay <?= money($ex['total'] / 4) ?> a quarter.</p>

      <h2 id="due-dates"><?= $Y ?> estimated tax due dates</h2>
      <p>The four “quarters” aren’t equal three-month periods. When a date falls on a weekend or legal holiday, the deadline moves to the next business day.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Installment</th><th>Income earned</th><th>Due date</th></tr></thead><tbody>
        <tr><td>1st</td><td>January 1 – March 31</td><td><?= e($due[0]) ?></td></tr>
        <tr><td>2nd</td><td>April 1 – May 31</td><td><?= e($due[1]) ?></td></tr>
        <tr><td>3rd</td><td>June 1 – August 31</td><td><?= e($due[2]) ?></td></tr>
        <tr><td>4th</td><td>September 1 – December 31</td><td><?= e($due[3]) ?></td></tr>
      </tbody></table></div>
      <p>You can skip the January payment if you file your <?= $Y ?> return and pay the full balance by February 1, <?= $Y + 1 ?>. Farmers and fishermen can make a single payment by January 15 or file and pay by March 1.</p>

      <h2 id="uneven-income">Uneven income? The annualized installment method</h2>
      <p>The standard rules assume you earn evenly and pay 25% each quarter. If most of your income arrives late in the year — a big Q4 contract, a December capital gain — you can use the <strong>annualized income installment method</strong> on Form 2210, Schedule AI. It sizes each installment to the income you actually earned by the end of that period, so smaller early payments aren’t penalized. You must attach Schedule AI to your return to claim it. This calculator uses equal installments; if your income is lumpy, treat the early-quarter numbers as conservative.</p>

      <h2 id="how-to-pay">How to pay estimated taxes</h2>
      <ul>
        <li><strong>IRS Direct Pay</strong> — free bank transfer at irs.gov/payments; choose “Estimated Tax” and Form 1040-ES.</li>
        <li><strong>Your IRS Online Account</strong> — schedule payments and see what’s been credited.</li>
        <li><strong>EFTPS</strong> — the Treasury’s free system, useful for scheduling a full year of payments in advance.</li>
        <li><strong>Debit or credit card</strong> through an IRS-approved processor (a fee applies), or a check with the 1040-ES voucher.</li>
        <li><strong>Increase W-2 withholding</strong> — if you also have a job, extra withholding on a new W-4 counts as paid evenly through the year, which can cure an early-quarter shortfall.</li>
      </ul>

      <h2 id="penalty">What if you miss a payment?</h2>
      <p>The underpayment penalty is calculated separately for each installment, using the IRS underpayment interest rate (the federal short-term rate plus 3 percentage points), from the due date until you pay or until April 15. Paying late is still better than not paying, because the penalty stops growing once the shortfall is made up. Read more in <a href="/blog/quarterly-taxes-101-guide/">Quarterly Taxes 101</a>, estimate your full-year bill with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>, or check withholding with the <a href="/calculators/paycheck-calculator/">paycheck calculator</a>.</p>

<?= faq_block([
  ['How do I calculate my quarterly estimated taxes?', "<p>Project this year’s total tax (income tax plus self-employment tax, minus credits). Your required annual payment is the smaller of 90% of that amount or 100% of last year’s tax (110% if last year’s AGI was over \$150,000). Subtract expected withholding and divide by four. In the example above, that’s " . money($exReq / 4) . " per quarter.</p>"],
  ['Do I have to pay quarterly taxes my first year?', '<p>Not if you had zero total tax last year, last year was a full 12-month year and you were a U.S. citizen or resident all year — then no underpayment penalty applies. If you did owe tax last year, paying 100% of that amount (110% if AGI was over $150,000) in quarterly installments avoids the penalty. Either way the full tax is still due when you file.</p>'],
  ["When are $Y quarterly taxes due?", '<p>' . implode(', ', $due) . '. If a date falls on a weekend or holiday, it moves to the next business day.</p>'],
  ['What is the safe harbor for estimated taxes?', '<p>Pay at least the smaller of 90% of this year’s tax or 100% of last year’s tax through withholding and on-time estimated payments. If last year’s AGI was above $150,000 ($75,000 married filing separately), the prior-year figure is 110%.</p>'],
  ['Do I need to make estimated payments if I have a W-2 job too?', '<p>Only if withholding won’t cover the required annual payment and you’ll owe $1,000 or more. Many people with side income simply raise their W-4 withholding instead, which the IRS treats as paid evenly over the year.</p>'],
  ['Can I pay all my estimated tax at once?', '<p>You can pay early, and a single payment by the first due date covers the year. Paying everything in January of the following year, however, leaves the earlier installments late, so a penalty can still apply unless you use the annualized method or have enough withholding.</p>'],
  ['Is the penalty for not paying quarterly taxes big?', '<p>It works like interest: the IRS underpayment rate (federal short-term rate plus 3%) applied to each missed installment for the time it was late. It’s rarely huge, but it is avoidable with the safe-harbor payments shown above.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('quarterly-estimated-tax', ['1099-tax-calculator', 'self-employment-tax', 'federal-income-tax', 'tax-refund-calculator', 'paycheck-calculator', 's-corp-tax-savings']) ?></div>
