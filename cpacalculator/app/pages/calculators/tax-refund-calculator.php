<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Tax Refund Calculator $Y — Refund Estimator: Refund or Owe? | CPA Calculator";
$P['description'] = "Free tax refund calculator and $Y tax refund estimator. Compare withholding with your actual tax, with the Child Tax Credit, 1099 income and new deductions.";
$P['scripts'] = ['/assets/js/tools/tax-refund-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Refund example for W-2 filers (standard deduction, CTC with refundable ACTC per Schedule 8812). Mirrors the JS. */
function refund_example(float $wages, float $withheld, int $kids, string $status): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $std = $y['std'][$status];
  $taxable = max(0, $wages - $std);
  $tax = fed_tax($taxable, $status)['tax'];
  $ctc = max(0, $kids * $y['ctc']['amount'] - ceil(max(0, $wages - $y['ctc']['phaseStart'][$status]) / 1000) * 50);
  $used = min($ctc, $tax);
  $actc = $kids ? min($ctc - $used, $kids * $y['ctc']['refundable'], 0.15 * max(0, $wages - 2500)) : 0;
  $after = $tax - $used;
  return compact('std', 'taxable', 'tax', 'ctc', 'used', 'actc', 'after', 'withheld', 'wages') + ['refund' => $withheld + $actc - $after];
}
$ex = refund_example(55000, 4000, 1, 'hoh');
$ex2 = refund_example(28000, 1200, 2, 'hoh');

echo tool_hero('tax-refund-calculator', "Tax Refund Calculator $Y",
  "Will you get money back or owe the IRS? This tax refund estimator compares what you’ve paid through withholding and estimated payments with the tax you actually owe — including the Child Tax Credit and its refundable portion, side income, itemized deductions and the new tips, overtime and senior deductions.",
  ['Refund or balance due', 'Refundable Child Tax Credit', 'W-2 + 1099 income', 'Tips, overtime & senior deductions']);
?>
<section class="tool" aria-label="Tax refund calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="refund-form" novalidate>
        <div class="grid-2">
          <?= year_field() ?>
          <div class="field"><label for="f-seniors">Taxpayers age 65+</label><select id="f-seniors" name="seniors"><option value="0">None</option><option value="1">One</option><option value="2">Two (joint)</option></select></div>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>W-2 jobs</legend>
          <div class="grid-2">
            <?= money_field('wages', 'Wages (W-2 Box 1, all jobs)', 60000, 'Total taxable wages from every W-2 for you (and your spouse if filing jointly). Box 1 is already reduced by pre-tax 401(k) and benefits.') ?>
            <?= money_field('withheld', 'Federal tax withheld (Box 2)', 6000, 'Total federal income tax withheld from all W-2s. Use your latest pay stub’s year-to-date figure and project to December if the year isn’t over.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Other income &amp; payments</legend>
          <div class="grid-2">
            <?= money_field('seIncome', '1099 / self-employment income', '', 'Gross freelance, gig or business income (1099-NEC, 1099-K).') ?>
            <?= money_field('seExpenses', 'Business expenses', '', 'Deductible expenses against your 1099 income.') ?>
          </div>
          <div class="grid-2">
            <?= money_field('estPaid', 'Estimated tax payments made', '', 'Form 1040-ES payments for this tax year, plus any prior-year refund applied.') ?>
            <?= money_field('otherIncome', 'Interest, unemployment, other income', '', 'Taxable interest, ordinary dividends, unemployment, IRA/pension distributions and other taxable income.') ?>
          </div>
          <?= money_field('otherWithheld', 'Other federal withholding', '', 'Tax withheld on 1099-R, 1099-G (unemployment), SSA-1099 or other forms.') ?>
        </fieldset>
        <fieldset class="fieldset"><legend>Deductions</legend>
          <div class="field"><span class="lbl">Deduction</span><div class="seg" role="radiogroup" aria-label="Deduction type">
            <label><input type="radio" name="dedType" value="std" checked><span>Standard deduction</span></label>
            <label><input type="radio" name="dedType" value="item"><span>Itemize</span></label>
          </div></div>
          <div class="grid-2">
            <?= money_field('itemized', 'Itemized deductions total', '', 'Mortgage interest, state and local taxes (capped at ' . money($y['saltCap']) . '), charitable gifts and medical costs over 7.5% of AGI. Only used if you choose Itemize.') ?>
            <?= money_field('adjust', 'Adjustments to income', '', 'Traditional IRA deduction, student loan interest (up to $2,500), HSA contributions outside payroll, educator expenses, SE health insurance.') ?>
          </div>
          <details class="more"><summary>New deductions: tips &amp; overtime</summary>
            <div class="grid-2">
              <?= money_field('tips', 'Qualified tips', '', 'Up to ' . money($y['tipsMax']) . ' of qualified cash tips is deductible for 2025–2028; phases out above $150,000 MAGI ($300,000 joint).') ?>
              <?= money_field('overtime', 'Qualified overtime premium', '', 'Only the “half” of time-and-a-half. Up to ' . money($y['overtimeMax']['single']) . ' (' . money($y['overtimeMax']['mfj']) . ' joint); phases out above $150,000 MAGI ($300,000 joint).') ?>
            </div>
          </details>
        </fieldset>
        <fieldset class="fieldset"><legend>Credits</legend>
          <div class="grid-2">
            <div class="field"><label for="f-kids">Children under 17</label><select id="f-kids" name="kids"><?php for ($i = 0; $i <= 6; $i++) echo "<option value=\"$i\">$i</option>"; ?></select><span class="hint"><?= money($y['ctc']['amount']) ?> each, up to <?= money($y['ctc']['refundable']) ?> refundable</span></div>
            <div class="field"><label for="f-deps">Other dependents</label><select id="f-deps" name="deps"><?php for ($i = 0; $i <= 4; $i++) echo "<option value=\"$i\">$i</option>"; ?></select><span class="hint">$500 credit each (17+, college students, parents)</span></div>
          </div>
          <div class="grid-2">
            <?= money_field('credits', 'Other nonrefundable credits', '', 'Child and dependent care, Lifetime Learning, the nonrefundable part of the American Opportunity credit, Saver’s credit, energy credits.') ?>
            <?= money_field('refundable', 'Other refundable credits', '', 'Refundable American Opportunity credit (up to $1,000), premium tax credit due, excess Social Security withheld, etc. Do not include the EITC here unless you know the amount.') ?>
          </div>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="label">Estimated refund</div>
          <div class="res-big" data-out="result">$0</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Total tax</small><b data-out="tax">$0</b></div>
            <div class="kpi"><small>Paid + refundable credits</small><b data-out="paid">$0</b></div>
            <div class="kpi"><small>Effective rate</small><b data-out="eff">0%</b></div>
            <div class="kpi"><small>Marginal bracket</small><b data-out="marg">0%</b></div>
          </div>
          <div class="res-label" style="margin-bottom:0">Payments vs. tax</div>
          <div class="meter" data-meter role="img" aria-label="Payments compared with total tax"></div>
          <ul class="legend" data-meter-legend style="margin-bottom:16px"></ul>
          <ul class="rows" data-rows></ul>
          <p class="note" data-out="note">Estimate only. Excludes state tax, AMT and the Earned Income Tax Credit. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-refunds-work">How a tax refund works</h2>
      <p>A refund isn’t a bonus from the IRS — it’s your own money coming back because you paid more during the year than you owed. Every refund or balance due comes from one comparison on Form 1040:</p>
      <div class="formula">Refund (or amount owed) = total payments − total tax<br>Total payments = withholding + estimated payments + refundable credits<br>Total tax = income tax − nonrefundable credits + self-employment tax + other taxes</div>
      <p>If the result is positive you get a refund; if it’s negative you owe the difference by the April filing deadline. That’s why two people with the same salary can have very different refunds: their withholding, credits and side income differ.</p>

      <h2 id="how-to-use">How to use this tax refund estimator</h2>
      <ol>
        <li><strong>Pick the tax year.</strong> <?= $Y ?> is the return you’ll file in early <?= $Y + 1 ?>. Choose <?= $Y - 1 ?> to double-check a return you already filed or are about to amend.</li>
        <li><strong>Enter W-2 wages and withholding.</strong> Box 1 and Box 2 of each W-2. Mid-year? Take year-to-date figures from your latest pay stub and project them to December 31.</li>
        <li><strong>Add other income and payments.</strong> 1099 income is where surprise balances usually come from, because nobody withholds on it. Enter any estimated payments you made.</li>
        <li><strong>Choose standard or itemized deductions</strong> and enter adjustments such as IRA contributions or student loan interest. If you itemize but the standard deduction is bigger, the calculator uses the standard deduction and tells you.</li>
        <li><strong>Add your children and other credits.</strong> The calculator applies the Child Tax Credit, the $500 credit for other dependents, and figures the refundable portion of the child credit.</li>
      </ol>

      <h2 id="example">Worked examples</h2>
      <h3 id="example-1">Head of household, $55,000, one child</h3>
      <div class="table-wrap"><table><tbody>
        <tr><td>W-2 wages</td><td class="n"><?= money($ex['wages']) ?></td></tr>
        <tr><td>Standard deduction (head of household)</td><td class="n">−<?= money($ex['std']) ?></td></tr>
        <tr><td>Taxable income</td><td class="n"><?= money($ex['taxable']) ?></td></tr>
        <tr><td>Tax before credits</td><td class="n"><?= money($ex['tax']) ?></td></tr>
        <tr><td>Child Tax Credit</td><td class="n">−<?= money($ex['used']) ?></td></tr>
        <tr><td>Total tax</td><td class="n"><?= money($ex['after']) ?></td></tr>
        <tr><td>Federal tax withheld</td><td class="n"><?= money($ex['withheld']) ?></td></tr>
        <tr><td><strong>Estimated refund</strong></td><td class="n"><strong><?= money($ex['refund']) ?></strong></td></tr>
      </tbody></table></div>
      <h3 id="example-2">Head of household, $28,000, two children</h3>
      <p>Tax before credits is only <?= money($ex2['tax']) ?>, so the nonrefundable part of the Child Tax Credit wipes it out. Of the remaining <?= money($ex2['ctc'] - $ex2['used']) ?> of unused credit, the refundable Additional Child Tax Credit pays out the smallest of: the unused credit, <?= money($y['ctc']['refundable']) ?> per child (<?= money(2 * $y['ctc']['refundable']) ?>), or 15% of earned income above $2,500 (<?= money(0.15 * (28000 - 2500)) ?>) — here <strong><?= money($ex2['actc']) ?></strong>. Add the <?= money($ex2['withheld']) ?> withheld and the refund is about <strong><?= money($ex2['refund']) ?></strong>, before any Earned Income Tax Credit, which this family would likely also qualify for.</p>

      <h2 id="what-changes-refund">What makes your refund bigger or smaller</h2>
      <div class="table-wrap"><table>
        <thead><tr><th>Factor</th><th>Effect on your refund</th></tr></thead><tbody>
        <tr><td>Higher withholding (W-4 Step 4(c), fewer dependents claimed)</td><td>Bigger refund, smaller paychecks</td></tr>
        <tr><td>1099, gig or investment income with no withholding</td><td>Smaller refund or a balance due — self-employment tax adds 15.3% on 92.35% of profit</td></tr>
        <tr><td>Two jobs or two working spouses without the W-4 Step 2 box</td><td>Under-withholding; often a balance due</td></tr>
        <tr><td>Child Tax Credit, education and dependent care credits</td><td>Bigger refund; refundable credits can create one even with zero tax</td></tr>
        <tr><td>401(k), traditional IRA, HSA contributions</td><td>Lower taxable income, so less tax and a bigger refund</td></tr>
        <tr><td>New <?= $Y ?> deductions for tips, overtime and seniors</td><td>Lower tax; payroll withholding may not reflect them, so many eligible workers see larger refunds</td></tr>
      </tbody></table></div>

      <h2 id="child-tax-credit">The Child Tax Credit and its refundable portion</h2>
      <p>For <?= $Y ?> the Child Tax Credit is <?= money($y['ctc']['amount']) ?> per qualifying child under 17 with a Social Security number valid for employment. It phases out by $50 for each $1,000 of modified AGI above <?= money($y['ctc']['phaseStart']['single']) ?> (<?= money($y['ctc']['phaseStart']['mfj']) ?> married filing jointly). The credit first reduces your income tax. If the credit is larger than your tax, up to <?= money($y['ctc']['refundable']) ?> per child can be paid to you as the <strong>Additional Child Tax Credit</strong>, limited to 15% of earned income over $2,500 (Schedule 8812). Families with three or more children can use an alternative formula based on Social Security and Medicare taxes paid, which this calculator doesn’t model.</p>
      <p>Dependents who don’t qualify — children 17 and older, full-time students under 24, qualifying relatives such as parents — can bring a $500 nonrefundable credit for other dependents.</p>

      <h2 id="eitc">The Earned Income Tax Credit (not included)</h2>
      <p>The EITC is a refundable credit for low- and moderate-income workers, worth more than $8,000 for families with three or more children. It depends on earned income, AGI, filing status, the number of qualifying children and investment income, and it phases in and out on an IRS table. Because a rough approximation could badly over- or understate your refund, this calculator leaves it out and shows a reminder when your income suggests you might qualify. Use the IRS EITC Assistant on irs.gov to check eligibility and amount, then add it to the refund shown here.</p>

      <h2 id="new-deductions">New deductions to check for <?= $Y ?></h2>
      <ul>
        <li><strong>No tax on tips</strong> — up to <?= money($y['tipsMax']) ?> of qualified tips deductible for 2025 through 2028.</li>
        <li><strong>No tax on overtime</strong> — the premium portion of overtime, up to <?= money($y['overtimeMax']['single']) ?> (<?= money($y['overtimeMax']['mfj']) ?> joint).</li>
        <li><strong>Senior deduction</strong> — an extra <?= money($y['senior']['amount']) ?> per person age 65 or older, phasing out above $75,000 of MAGI ($150,000 joint), on top of the regular additional standard deduction.</li>
        <li><strong>SALT cap of <?= money($y['saltCap']) ?></strong> for itemizers, reduced for incomes above $500,000.</li>
      </ul>
      <p>All three new deductions are available whether you itemize or take the standard deduction. The calculator applies them (it doesn’t model the income phase-outs for tips and overtime, which start at $150,000 MAGI, or $300,000 joint).</p>

      <h2 id="when">When will I get my refund?</h2>
      <p>The IRS says most refunds on e-filed returns with direct deposit arrive within 21 days. By law, refunds that include the Earned Income Tax Credit or the Additional Child Tax Credit can’t be issued before mid-February, so those filers typically see money in late February or early March. Paper returns take several weeks longer. Track yours with the IRS “Where’s My Refund?” tool.</p>

      <h2 id="if-you-owe">If the estimate says you owe</h2>
      <ul>
        <li><strong>During the year:</strong> increase withholding with a new W-4 or make an estimated payment now — see the <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a>. Withholding counts as paid evenly through the year, so it can fix earlier shortfalls.</li>
        <li><strong>After year-end:</strong> fund a traditional IRA or HSA before the filing deadline — both can still lower last year’s tax.</li>
        <li><strong>At filing:</strong> pay by the April deadline even if you extend. The IRS offers short-term and monthly payment plans if you can’t pay in full.</li>
      </ul>
      <p>Want to fine-tune your paychecks instead? Use the <a href="/calculators/paycheck-calculator/">paycheck calculator</a> to see how W-4 changes affect take-home pay, the <a href="/calculators/federal-income-tax/">federal income tax calculator</a> for a full-year view, or our guide to <a href="/blog/understanding-your-w-2/">understanding your W-2</a>. 1099 income? Start with <a href="/blog/got-a-1099-exactly-what-to-do-next/">what to do after you get a 1099</a>.</p>

<?= faq_block([
  ['How do I estimate my tax refund?', '<p>Add up your total tax — income tax after credits plus any self-employment tax — and subtract it from what you paid: federal withholding, estimated payments and refundable credits. A positive result is your refund. For example, a head of household earning $55,000 with one child and ' . money($ex['withheld']) . ' withheld would get about ' . money($ex['refund']) . ' back in ' . $Y . '.</p>'],
  ["Is this a tax refund estimator for $Y?", '<p>Yes. It uses the ' . $Y . ' brackets, standard deduction, ' . money($y['ctc']['amount']) . ' Child Tax Credit and the new tips, overtime and senior deductions. Choose ' . ($Y - 1) . ' in the tax year menu for last year’s return.</p>'],
  ['Why is my refund smaller this year?', '<p>Common causes: you earned more or had side income with no withholding, a child aged out of the Child Tax Credit, you changed your W-4, or a second job pushed income into a higher bracket without enough withholding.</p>'],
  ['How much of the Child Tax Credit is refundable?', '<p>Up to ' . money($y['ctc']['refundable']) . ' per qualifying child for ' . $Y . ', limited to 15% of earned income above $2,500. The rest of the ' . money($y['ctc']['amount']) . ' credit only reduces tax you owe.</p>'],
  ['Does the calculator include the Earned Income Tax Credit?', '<p>No. The EITC depends on detailed income tables, so it’s shown as a reminder rather than calculated. If you qualify, your actual refund will be larger than this estimate. Check the amount with the IRS EITC Assistant.</p>'],
  ['Do I get a refund if I had no tax withheld?', '<p>Possibly, if you qualify for refundable credits like the Additional Child Tax Credit, the refundable American Opportunity credit or the EITC. Otherwise there’s nothing to refund, and any tax owed is due when you file.</p>'],
  ['Is a big tax refund good?', '<p>It means you overpaid during the year — an interest-free loan to the government. Some people like the forced savings; others adjust their W-4 to keep more in each paycheck. Aim for a small refund or balance due.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('tax-refund-calculator', ['federal-income-tax', 'paycheck-calculator', 'quarterly-estimated-tax', '1099-tax-calculator', 'self-employment-tax', 'salary-to-hourly']) ?></div>
