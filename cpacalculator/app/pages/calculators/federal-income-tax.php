<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Federal Income Tax Calculator $Y — Free IRS Tax Estimator | CPA Calculator";
$P['description'] = "Free $Y federal income tax calculator. Estimate your federal tax, effective rate, marginal bracket, refund and take-home pay with the new IRS brackets and standard deduction.";
$P['scripts'] = ['/assets/js/tools/federal-income-tax.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

echo tool_hero('federal-income-tax', "Federal Income Tax Calculator $Y",
  "Estimate your $Y federal income tax in seconds — total tax, effective and marginal rates, refund or balance due, and take-home pay. Uses the official IRS brackets, the $Y standard deduction and the new deductions for tips, overtime and seniors.",
  ["Updated for $Y IRS brackets", 'W-2, 1099 & investment income', 'Refund or amount owed', 'No signup — runs in your browser']);
?>
<section class="tool" aria-label="Federal income tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="fed-form" novalidate>
        <div class="tool-tabs" data-tabs>
          <button type="button" data-tab="simple" aria-selected="true">Quick estimate</button>
          <button type="button" data-tab="detailed" aria-selected="false">Detailed</button>
        </div>
        <input type="hidden" name="mode" value="simple">
        <div class="grid-2">
          <?= year_field() ?>
          <div class="field"><label for="f-seniors">Taxpayers age 65+</label><select id="f-seniors" name="seniors"><option value="0">None</option><option value="1">One</option><option value="2">Two (joint)</option></select></div>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Income</legend>
          <?= money_field('wages', 'Wages, salary & tips (W-2)', 75000, 'Box 1 of your W-2, or your expected annual gross pay. Include bonuses.') ?>
          <input type="range" min="0" max="500000" step="1000" data-range-for="wages" aria-label="Wages slider">
          <div data-panel="detailed" hidden>
            <div class="grid-2">
              <?= money_field('seIncome', 'Self-employment / 1099 income', '', 'Gross 1099-NEC, 1099-K or Schedule C income.') ?>
              <?= money_field('seExpenses', 'Business expenses', '', 'Deductible business costs against your 1099 income.') ?>
            </div>
            <div class="grid-2">
              <?= money_field('otherIncome', 'Interest, unemployment, other', '', 'Taxable interest, ordinary dividends, unemployment, IRA distributions, rental net income.') ?>
              <?= money_field('stcg', 'Short-term capital gains', '', 'Assets held one year or less — taxed as ordinary income.') ?>
            </div>
            <?= money_field('ltcg', 'Long-term gains & qualified dividends', '', 'Taxed at 0%, 15% or 20% depending on total taxable income.') ?>
          </div>
        </fieldset>
        <div data-panel="detailed" hidden>
          <fieldset class="fieldset"><legend>Deductions &amp; adjustments</legend>
            <div class="grid-2">
              <?= money_field('pretax', 'Pre-tax 401(k) / 403(b) / IRA', '', "Traditional contributions reduce taxable wages. $Y limit: " . money($y['k401']) . ' (401k), ' . money($y['ira']) . ' (IRA).') ?>
              <?= money_field('hsa', 'HSA contributions', '', "Only contributions not made through payroll. $Y limit: " . money($y['hsa']['self']) . ' self / ' . money($y['hsa']['family']) . ' family.') ?>
            </div>
            <?= money_field('itemized', 'Itemized deductions (if any)', '', 'Mortgage interest, state & local taxes (capped at ' . money($y['saltCap']) . '), charity, medical over 7.5% of AGI. We use whichever is larger: this or the standard deduction.') ?>
            <div class="grid-2">
              <?= money_field('tips', 'Qualified tips', '', 'New for 2025–2028: up to ' . money($y['tipsMax']) . ' of qualified tips is deductible (phases out above $150k MAGI).') ?>
              <?= money_field('overtime', 'Qualified overtime premium', '', 'The “half” portion of time-and-a-half pay. Deductible up to $12,500 ($25,000 joint).') ?>
            </div>
          </fieldset>
          <fieldset class="fieldset"><legend>Credits &amp; payments</legend>
            <div class="grid-2">
              <div class="field"><label for="f-kids">Children under 17</label><select id="f-kids" name="kids"><?php for ($i = 0; $i <= 6; $i++) echo "<option value=\"$i\">$i</option>"; ?></select><span class="hint">Child Tax Credit: <?= money($y['ctc']['amount']) ?> each</span></div>
              <?= money_field('credits', 'Other credits', '', 'Education credits, dependent care credit, energy credits, etc.') ?>
            </div>
          </fieldset>
        </div>
        <?= money_field('withheld', 'Federal tax already withheld / paid', '', 'W-2 Box 2 plus any estimated payments. Leave blank to skip the refund estimate.', 'Optional — shows whether you’ll get a refund or owe.') ?>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Estimated federal income tax</div>
          <div class="res-big" data-out="tax">$0</div>
          <div class="res-sub"><span data-out="summary">—</span></div>
          <div class="kpis">
            <div class="kpi"><small>Effective rate</small><b data-out="eff">0%</b></div>
            <div class="kpi"><small>Marginal bracket</small><b data-out="marg">0%</b></div>
            <div class="kpi"><small>Taxable income</small><b data-out="taxable">$0</b></div>
            <div class="kpi"><small data-out="refundLabel">Refund / owed</small><b data-out="refund">—</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your income goes"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <div class="res-label" style="margin-bottom:6px">Your income across the brackets</div>
          <div data-brackets></div>
          <p class="note">Estimate only. Excludes state/local tax, AMT and phase-outs not listed. See <a href="/our-methodology/">our methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use this federal income tax calculator</h2>
      <p>Most people only need the <strong>Quick estimate</strong> tab: pick your filing status, enter your annual wages and you’ll instantly see your federal income tax, effective tax rate and marginal tax bracket. Switch to <strong>Detailed</strong> when you also have 1099 or freelance income, investment income, retirement contributions, itemized deductions or children.</p>
      <ol>
        <li><strong>Choose the tax year.</strong> <?= $Y ?> is the year you’re earning in now (returns filed in early <?= $Y + 1 ?>). Pick <?= $Y - 1 ?> if you’re checking or amending last year’s return.</li>
        <li><strong>Select your filing status.</strong> It sets both your standard deduction and the width of every tax bracket.</li>
        <li><strong>Enter income.</strong> Use gross annual pay (before deductions) — W-2 Box 1 if you have it.</li>
        <li><strong>Add what you’ve already paid.</strong> Enter federal withholding (W-2 Box 2) plus estimated payments to see your projected refund or balance due.</li>
      </ol>
      <p>Every result updates live, and you can copy a share link or print the breakdown for your records or your CPA.</p>

      <h2 id="how-calculated">How federal income tax is calculated</h2>
      <p>The IRS doesn’t tax your whole paycheck at one rate. Federal income tax is <strong>progressive</strong>: your income is sliced into layers and each layer is taxed at its own rate. The calculator follows the same order as Form 1040:</p>
      <div class="formula">Gross income − adjustments = AGI<br>AGI − (standard or itemized deduction) − QBI &amp; new deductions = Taxable income<br>Tax on taxable income (brackets) − credits = Federal income tax</div>
      <ol>
        <li><strong>Gross income</strong> — wages, net self-employment profit, interest, dividends, capital gains and other taxable income.</li>
        <li><strong>Adjustments</strong> — pre-tax retirement contributions, HSA contributions and half of self-employment tax come off first, giving your <strong>adjusted gross income (AGI)</strong>.</li>
        <li><strong>Deductions</strong> — you subtract the larger of the standard deduction or your itemized deductions, plus any qualified business income (QBI) deduction and the new tips, overtime and senior deductions.</li>
        <li><strong>Apply the brackets</strong> — ordinary income runs through the 10%–37% brackets; long-term capital gains and qualified dividends are stacked on top and taxed at 0%, 15% or 20%.</li>
        <li><strong>Subtract credits</strong> — credits such as the Child Tax Credit reduce the tax dollar-for-dollar.</li>
      </ol>

      <h2 id="brackets"><?= $Y ?> federal income tax brackets</h2>
      <p>These are the <?= $Y ?> federal income tax brackets published by the IRS (Rev. Proc. 2025-32), adjusted for inflation. They apply to income earned in <?= $Y ?> and reported on the return you file in <?= $Y + 1 ?>.</p>
      <ul class="pill-links" role="tablist">
        <li><a href="#brackets-single">Single</a></li><li><a href="#brackets-mfj">Married filing jointly</a></li><li><a href="#brackets-hoh">Head of household</a></li><li><a href="#brackets-mfs">Married filing separately</a></li>
      </ul>
<?php foreach (['single', 'mfj', 'hoh', 'mfs'] as $s): ?>
      <h3 id="brackets-<?= $s ?>"><?= $Y ?> tax brackets: <?= status_label($s) ?></h3>
      <?= bracket_table($s) ?>
<?php endforeach; ?>

      <h2 id="standard-deduction"><?= $Y ?> standard deduction</h2>
      <p>The standard deduction is the amount of income you can earn before any federal income tax applies. About 90% of filers take it instead of itemizing. The One Big Beautiful Bill Act made the higher standard deduction permanent and indexes it for inflation every year.</p>
      <?= std_deduction_table() ?>
      <p>Taxpayers 65 or older can also claim the new <strong>senior deduction of up to <?= money($y['senior']['amount']) ?> per person</strong> for 2025 through 2028, which phases out at 6% of modified AGI above $75,000 ($150,000 joint). The calculator applies it automatically when you select a taxpayer age 65+.</p>

      <h2 id="marginal-vs-effective">Marginal vs. effective tax rate</h2>
      <p>Your <strong>marginal rate</strong> is the rate on your <em>next</em> dollar of income — the highest bracket you reach. Your <strong>effective rate</strong> is your total federal income tax divided by your total income, and it’s always lower. A single filer earning $75,000 in <?= $Y ?> is in the 22% bracket, but only the slice of taxable income above <?= money($y['brackets']['single'][1][0]) ?> is taxed at 22% — the effective rate works out to roughly <?= round(salary_breakdown(75000, 'single')['effective'] * 100, 1) ?>%.</p>
      <div class="callout"><?= icon('spark') ?><p><strong>Myth buster:</strong> a raise can never reduce your take-home pay because of brackets. Moving into a higher bracket only affects the dollars inside that bracket.</p></div>

      <h2 id="by-salary">Federal income tax by salary (<?= $Y ?>, single filer)</h2>
      <p>Quick reference for common salaries using the standard deduction and W-2 wages. Click any amount for the full breakdown by filing status, including FICA and take-home pay.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Salary</th><th class="n">Federal income tax</th><th class="n">Effective rate</th><th class="n">Bracket</th><th class="n">Take-home after FICA</th></tr></thead><tbody>
<?php foreach ([20000, 30000, 40000, 50000, 60000, 75000, 90000, 100000, 120000, 150000, 200000, 300000] as $amt): $b = salary_breakdown($amt, 'single'); ?>
        <tr><td><a href="/calculators/federal-income-tax/<?= $amt ?>/"><?= money($amt) ?></a></td><td class="n"><?= money($b['tax']) ?></td><td class="n"><?= number_format($b['effective'] * 100, 1) ?>%</td><td class="n"><?= round($b['marginal'] * 100) ?>%</td><td class="n"><?= money($b['net']) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>

      <h2 id="example">Worked example: $90,000 salary, single</h2>
<?php $ex = salary_breakdown(90000, 'single'); ?>
      <p>Say you earn $90,000 in W-2 wages in <?= $Y ?> and file single with no other income.</p>
      <ul>
        <li>Taxable income: $90,000 − <?= money($ex['std']) ?> standard deduction = <strong><?= money($ex['taxable']) ?></strong></li>
<?php foreach ($ex['layers'] as $l): if ($l['amount'] <= 0) continue; ?>
        <li><?= round($l['rate'] * 100) ?>% on <?= money($l['amount']) ?> = <?= money($l['tax']) ?></li>
<?php endforeach; ?>
        <li>Total federal income tax: <strong><?= money($ex['tax']) ?></strong> — an effective rate of <?= number_format($ex['effective'] * 100, 1) ?>%, with a 22% marginal rate.</li>
        <li>Add Social Security and Medicare (<?= money($ex['fica']) ?>) and take-home pay before state tax is about <strong><?= money($ex['net']) ?></strong>, or <?= money($ex['net'] / 12) ?> a month.</li>
      </ul>

      <h2 id="whats-new">What’s new for <?= $Y ?></h2>
      <ul>
        <li><strong>Inflation-adjusted brackets</strong> — every bracket threshold rose about 4% for the bottom two brackets and 2.3% for the rest.</li>
        <li><strong>Bigger standard deduction</strong> — <?= money($y['std']['single']) ?> single, <?= money($y['std']['mfj']) ?> married filing jointly, <?= money($y['std']['hoh']) ?> head of household.</li>
        <li><strong>No tax on tips (up to <?= money($y['tipsMax']) ?>)</strong> and <strong>no tax on overtime premium (up to $12,500 / $25,000)</strong> as below-the-line deductions through 2028.</li>
        <li><strong>Senior deduction</strong> — an extra <?= money($y['senior']['amount']) ?> per person age 65+.</li>
        <li><strong>Child Tax Credit</strong> — <?= money($y['ctc']['amount']) ?> per qualifying child, up to <?= money($y['ctc']['refundable']) ?> refundable.</li>
        <li><strong>SALT cap</strong> — the state and local tax deduction cap is <?= money($y['saltCap']) ?> for itemizers (reduced above $500k MAGI).</li>
      </ul>

      <h2 id="lower-tax">7 legal ways to lower your federal income tax</h2>
      <ol>
        <li><strong>Max out pre-tax retirement accounts</strong> — up to <?= money($y['k401']) ?> in a 401(k) and <?= money($y['ira']) ?> in a traditional IRA (if eligible) for <?= $Y ?>.</li>
        <li><strong>Fund an HSA</strong> if you have a high-deductible health plan — it’s deductible going in and tax-free coming out for medical costs.</li>
        <li><strong>Bunch itemized deductions</strong> — group two years of charitable gifts into one year to clear the standard deduction.</li>
        <li><strong>Harvest capital losses</strong> to offset gains and up to $3,000 of ordinary income.</li>
        <li><strong>Hold investments longer than a year</strong> so gains qualify for the 0%/15%/20% rates. Try our <a href="/calculators/capital-gains-tax/">capital gains tax calculator</a>.</li>
        <li><strong>Claim every credit</strong> — Child Tax Credit, education credits, dependent care and energy credits cut tax dollar-for-dollar.</li>
        <li><strong>If you’re self-employed</strong>, track every business expense and check the QBI deduction with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>.</li>
      </ol>
      <p>Want to check your paycheck withholding instead? Use the <a href="/calculators/paycheck-calculator/">paycheck calculator</a> or the <a href="/calculators/tax-refund-calculator/">tax refund estimator</a>.</p>

<?= faq_block([
  ['How much federal income tax will I pay?', "<p>It depends on your taxable income and filing status, not your gross pay. For $Y, a single filer earning \$50,000 pays about " . money(salary_breakdown(50000, 'single')['tax']) . ", someone earning \$75,000 pays about " . money(salary_breakdown(75000, 'single')['tax']) . " and \$100,000 is about " . money(salary_breakdown(100000, 'single')['tax']) . " in federal income tax, using the standard deduction. Enter your numbers above for an exact estimate.</p>"],
  ['If I made $90,000, how much federal tax do I pay?', "<p>A single filer with \$90,000 of W-2 wages in $Y owes about " . money($ex['tax']) . " in federal income tax (" . number_format($ex['effective'] * 100, 1) . "% effective rate). Married couples filing jointly with the same income owe about " . money(salary_breakdown(90000, 'mfj')['tax']) . ".</p>"],
  ['How do I calculate federal income tax by hand?', '<p>Subtract adjustments and your standard deduction from gross income to get taxable income. Then apply each bracket rate only to the income inside that bracket and add the pieces together. Finally, subtract any tax credits. The calculator above does exactly this and shows the tax owed in each bracket.</p>'],
  ['What is the federal income tax rate for a single person?', "<p>Single filers face seven rates in $Y: 10%, 12%, 22%, 24%, 32%, 35% and 37%. The 10% rate covers the first " . money($y['brackets']['single'][0][0]) . " of taxable income and 37% applies above " . money($y['brackets']['single'][5][0]) . ". Most single filers have an effective rate between 5% and 15%.</p>"],
  ['Does this calculator include Social Security and Medicare?', '<p>Yes. FICA (6.2% Social Security up to the wage base and 1.45% Medicare, plus 0.9% Additional Medicare over $200,000) is shown in the breakdown and used for take-home pay, but it is not counted in the “federal income tax” figure because it is a separate payroll tax. For 1099 income the calculator adds self-employment tax.</p>'],
  ['Is the 2026 federal income tax calculator accurate?', '<p>It uses the official IRS tax tables, standard deductions and the new deductions created by the One Big Beautiful Bill Act. For typical W-2 and freelance situations results are usually within a few dollars of tax software. It does not compute AMT, state tax or every phase-out, so confirm complex returns with a CPA.</p>'],
  ['When are 2026 federal taxes due?', "<p>Your $Y return is due April 15, " . ($Y + 1) . ". If you are self-employed, quarterly estimated payments are due " . implode(', ', $y['quarterlyDue']) . ". See our <a href=\"/calculators/quarterly-estimated-tax/\">quarterly estimated tax calculator</a>.</p>"],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('federal-income-tax', ['paycheck-calculator', 'tax-refund-calculator', '1099-tax-calculator', 'capital-gains-tax', 'salary-to-hourly', 'quarterly-estimated-tax']) ?></div>
