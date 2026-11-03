<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "1099 Tax Calculator $Y with Deductions | CPA Calculator";
$P['description'] = "Free $Y 1099 tax calculator with deductions. Estimate self-employment tax, income tax, write-offs and quarterly payments for freelancers and contractors.";
$P['scripts'] = ['/assets/js/tools/1099-tax-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Worked example numbers rendered server-side (mirrors the JS engine for a single filer with no W-2). */
function ex1099(float $gross, float $exp, string $status = 'single'): array {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $net = max(0, $gross - $exp);
  $base = $net * 0.9235;
  $se = min($base, $y['ssWageBase']) * 0.124 + $base * 0.029;
  $agi = $net - $se / 2;
  $before = max(0, $agi - $y['std'][$status]);
  $qbi = min($net * 0.2, $before * 0.2);
  $taxable = max(0, $before - $qbi);
  $inc = fed_tax($taxable, $status)['tax'];
  return compact('net', 'base', 'se', 'agi', 'qbi', 'taxable', 'inc') + ['total' => $se + $inc, 'std' => $y['std'][$status]];
}
$ex = ex1099(60000, 8000);

echo tool_hero('1099-tax-calculator', "1099 Tax Calculator $Y",
  "Built for freelancers, independent contractors, gig workers and side hustlers. Enter your 1099 income and write-offs to see your self-employment tax, federal income tax, how much to set aside, and your quarterly estimated payments — with the $Y IRS rates.",
  ['Self-employment tax + income tax', 'Guided deduction finder', 'QBI deduction included', 'Quarterly payment plan']);
?>
<section class="tool" aria-label="1099 tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="t1099-form" novalidate>
        <div class="grid-2">
          <?= year_field() ?>
          <div class="field"><label for="f-work">Type of work</label><select id="f-work" name="work">
            <option value="general">Freelancer / contractor</option><option value="gig">Rideshare / delivery driver</option><option value="creator">Creator / online seller</option>
            <option value="physician">Physician / locums / medical</option><option value="realestate">Real estate agent</option><option value="consultant">Consultant / IT / designer</option>
          </select></div>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Income</legend>
          <?= money_field('income', '1099 / self-employment income (gross)', 60000, 'Total of your 1099-NEC, 1099-K and 1099-MISC payments plus any cash or app payments not reported on a 1099.') ?>
          <input type="range" min="0" max="400000" step="1000" data-range-for="income" aria-label="1099 income slider">
          <div class="grid-2">
            <?= money_field('wages', 'W-2 wages from a job (if any)', '', 'Salary from an employer. It fills the lower brackets first and counts toward the Social Security wage base.') ?>
            <?= money_field('withheld', 'Federal tax withheld from W-2', '', 'W-2 Box 2. Withholding counts toward what you owe on 1099 income.') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Business expenses &amp; write-offs</legend>
          <?= money_field('expenses', 'Business expenses you already know', 8000, 'Supplies, software, advertising, equipment, contractors, fees, insurance, travel, 50% of business meals — anything ordinary and necessary for the business.') ?>
          <details class="more" open><summary>Find more deductions (guided)</summary>
            <p class="hint" id="work-tip" style="margin-top:0">Common write-offs for freelancers.</p>
            <div class="grid-2">
              <?= money_field('miles', 'Business miles driven', '', 'Trips between clients/job sites — not your commute. ' . $Y . ' standard rate: ' . ($y['mileage'] * 100) . '¢ per mile.', '', '') ?>
              <?= money_field('sqft', 'Home office (sq ft)', '', 'Space used regularly and exclusively for work. Simplified method: $5 per sq ft, max 300 sq ft.', '', '') ?>
            </div>
            <div class="grid-2">
              <?= money_field('phone', 'Phone bill per month', '', 'Your monthly cell bill.') ?>
              <?= money_field('phonePct', 'Phone business use', 50, 'Percentage of phone use that is for work.', '', '%') ?>
            </div>
            <div class="grid-2">
              <?= money_field('internet', 'Internet bill per month', '', 'Home internet service.') ?>
              <?= money_field('internetPct', 'Internet business use', 50, 'Percentage of internet use that is for work.', '', '%') ?>
            </div>
          </details>
          <details class="more"><summary>Retirement &amp; health insurance (adjustments)</summary>
            <div class="grid-2">
              <?= money_field('health', 'Self-employed health insurance', '', 'Premiums for you, your spouse and dependents if you are not eligible for an employer plan. Deducted on Schedule 1.') ?>
              <?= money_field('retire', 'SEP-IRA / Solo 401(k) contribution', '', 'Employer-side contributions are deductible. SEP limit is roughly 20% of net SE earnings.') ?>
            </div>
          </details>
        </fieldset>
        <fieldset class="fieldset"><legend>Payments made</legend>
          <?= money_field('paid', 'Estimated tax payments already made this year', '', 'Total of the quarterly 1040-ES payments you have sent the IRS this year.') ?>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Total estimated federal tax</div>
          <div class="res-big" data-out="total">$0</div>
          <div class="res-sub" data-out="setaside">—</div>
          <div class="kpis">
            <div class="kpi"><small>Self-employment tax</small><b data-out="se">$0</b></div>
            <div class="kpi"><small>Federal income tax</small><b data-out="inc">$0</b></div>
            <div class="kpi"><small>Effective rate</small><b data-out="eff">0%</b></div>
            <div class="kpi"><small>Marginal bracket</small><b data-out="marg">0%</b></div>
          </div>
          <div class="res-label" style="margin-bottom:8px" data-out="qlabel">Quarterly estimated payments</div>
          <div class="quarters" data-quarters></div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your 1099 income goes"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note">Estimate only — excludes state tax and AMT; QBI shown before specified-service phase-outs above <?= money($y['qbiThreshold']['single']) ?> (single). <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-1099-taxes-work">How 1099 taxes work</h2>
      <p>When you’re paid on a 1099, no one withholds tax from your checks. You become both the employee and the employer, which means you owe two federal taxes on your profit:</p>
      <ul>
        <li><strong>Self-employment tax of 15.3%</strong> — 12.4% Social Security (on the first <?= money($y['ssWageBase']) ?> of combined earnings in <?= $Y ?>) plus 2.9% Medicare, charged on 92.35% of your net profit. An extra 0.9% Medicare applies above $200,000 ($250,000 joint).</li>
        <li><strong>Federal income tax</strong> at your normal bracket rate (10% to 37%) on what’s left after the standard deduction, half of your SE tax and the 20% qualified business income (QBI) deduction.</li>
      </ul>
      <p>That’s why a common rule of thumb is to <strong>set aside 25–30% of every 1099 payment</strong> for federal taxes — more if you also live in a state with income tax. This 1099 tax calculator replaces the rule of thumb with your actual number.</p>
      <div class="formula">Net profit = 1099 income − business expenses<br>SE tax = net profit × 92.35% × 15.3%<br>Taxable income = net profit − ½ SE tax − standard deduction − QBI (20%)<br>Total tax = SE tax + income tax on taxable income</div>

      <h2 id="example">1099 tax example: $60,000 of freelance income</h2>
      <p>A single freelancer with $60,000 of 1099-NEC income and $8,000 of business expenses in <?= $Y ?>:</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Net profit (Schedule C)</td><td class="n"><?= money($ex['net']) ?></td></tr>
        <tr><td>Self-employment tax (<?= money($ex['base']) ?> × 15.3%)</td><td class="n"><?= money($ex['se']) ?></td></tr>
        <tr><td>Adjusted gross income (profit − ½ SE tax)</td><td class="n"><?= money($ex['agi']) ?></td></tr>
        <tr><td>Standard deduction</td><td class="n">−<?= money($ex['std']) ?></td></tr>
        <tr><td>QBI deduction (20%)</td><td class="n">−<?= money($ex['qbi']) ?></td></tr>
        <tr><td>Taxable income</td><td class="n"><?= money($ex['taxable']) ?></td></tr>
        <tr><td>Federal income tax</td><td class="n"><?= money($ex['inc']) ?></td></tr>
        <tr><td><strong>Total federal tax</strong></td><td class="n"><strong><?= money($ex['total']) ?></strong></td></tr>
        <tr><td>Quarterly payment (÷ 4)</td><td class="n"><?= money($ex['total'] / 4) ?></td></tr>
      </tbody></table></div>
      <p>That’s about <?= round($ex['total'] / 60000 * 100) ?>% of gross 1099 income. Notice that self-employment tax is larger than income tax here — very common for earners under about $100,000.</p>

      <h2 id="deductions">Common 1099 tax deductions</h2>
      <p>Every legitimate expense lowers <em>both</em> taxes, so a $1,000 deduction typically saves a freelancer in the 12% bracket around $250–$270. The most overlooked write-offs:</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Deduction</th><th>How it works in <?= $Y ?></th></tr></thead><tbody>
        <tr><td>Vehicle / mileage</td><td><?= ($y['mileage'] * 100) ?>¢ per business mile, or actual costs × business-use %. <a href="/calculators/mileage-deduction/">Mileage calculator</a></td></tr>
        <tr><td>Home office</td><td>$5/sq ft up to 300 sq ft ($1,500), or actual expenses × office %. <a href="/calculators/home-office-deduction/">Home office calculator</a></td></tr>
        <tr><td>Phone &amp; internet</td><td>Business-use percentage of the bill.</td></tr>
        <tr><td>Software, equipment &amp; tools</td><td>Generally deductible in full the year you buy them (Section 179 / 100% bonus depreciation). <a href="/calculators/depreciation-calculator/">Depreciation calculator</a></td></tr>
        <tr><td>Health insurance</td><td>100% of premiums for you and your family if you’re not eligible for an employer plan.</td></tr>
        <tr><td>Retirement contributions</td><td>SEP-IRA or Solo 401(k) — the employee deferral limit is <?= money($y['k401']) ?> for <?= $Y ?>, plus employer contributions.</td></tr>
        <tr><td>Business meals</td><td>50% of meals with clients or while traveling for work.</td></tr>
        <tr><td>Fees &amp; services</td><td>Platform fees (Upwork, Etsy, Stripe), bank fees, legal and accounting, business insurance.</td></tr>
      </tbody></table></div>

      <h2 id="quarterly">Quarterly estimated taxes for 1099 workers</h2>
      <p>If you expect to owe $1,000 or more when you file, the IRS expects you to pay during the year using Form 1040-ES. <?= $Y ?> due dates:</p>
      <ul><?php foreach ($y['quarterlyDue'] as $i => $d) echo '<li><strong>Q' . ($i + 1) . ':</strong> ' . $d . '</li>'; ?></ul>
      <p>To avoid an underpayment penalty, pay at least 90% of this year’s tax or 100% of last year’s tax (110% if your AGI was over $150,000). The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> works out the safe-harbor amount, and our guide answers <a href="/blog/do-i-have-to-pay-quarterly-taxes-my-first-year/">whether you have to pay quarterly taxes your first year</a>.</p>

      <h2 id="physicians">1099 tax calculator for physicians and high earners</h2>
      <p>Locum tenens doctors, moonlighting residents, CRNAs and other 1099 medical professionals face a few extra rules that this calculator models:</p>
      <ul>
        <li><strong>Social Security wage base:</strong> the 12.4% Social Security portion stops at <?= money($y['ssWageBase']) ?> of combined W-2 and self-employment earnings — enter your W-2 hospital salary so it isn’t taxed twice.</li>
        <li><strong>Additional Medicare tax:</strong> 0.9% on earnings above $200,000 ($250,000 joint).</li>
        <li><strong>QBI limits:</strong> medicine is a “specified service” business, so the 20% QBI deduction phases out above <?= money($y['qbiThreshold']['single']) ?> of taxable income (<?= money($y['qbiThreshold']['mfj']) ?> joint). Treat the QBI line as a best case at higher incomes.</li>
        <li><strong>Retirement:</strong> a Solo 401(k) or SEP-IRA can shelter tens of thousands of dollars of 1099 income.</li>
      </ul>
      <p>Read the full <a href="/blog/1099-taxes-for-physicians/">1099 physician tax guide</a>, or compare an <a href="/calculators/s-corp-tax-savings/">S corp election</a> once your profit passes roughly $80,000.</p>

      <h2 id="1099-vs-w2">1099 vs. W-2: why your tax bill is higher</h2>
      <p>An employee earning $60,000 has 7.65% FICA withheld and the employer pays the other 7.65%. A contractor earning the same $60,000 pays the full 15.3% — but also gets to deduct half of it, plus business expenses and the QBI deduction. When comparing a 1099 offer with a W-2 salary, a 1099 rate needs to be roughly 20–30% higher to come out even once you add self-employment tax, health insurance and unpaid time off. Our <a href="/calculators/salary-to-hourly/">salary to hourly calculator</a> helps with that comparison.</p>

      <h2 id="what-to-do">Got a 1099? What to do next</h2>
      <ol>
        <li>Check every 1099 for the correct name, TIN and amount.</li>
        <li>Total all income — including payments under $600 that didn’t generate a form.</li>
        <li>Gather receipts and bank records for expenses.</li>
        <li>Run the numbers above and set aside the recommended amount.</li>
        <li>File Schedule C and Schedule SE with your Form 1040.</li>
      </ol>
      <p>Our step-by-step guide covers each one: <a href="/blog/got-a-1099-exactly-what-to-do-next/">Got a 1099? Here’s exactly what to do next</a>.</p>

<?= faq_block([
  ['How much tax do I pay on 1099 income?', "<p>Most 1099 earners pay 15.3% self-employment tax on 92.35% of net profit plus federal income tax at 10–37%. In practice the total usually lands between 20% and 30% of profit for incomes from \$30,000 to \$150,000. For example, \$60,000 of 1099 income with \$8,000 of expenses produces about " . money($ex['total']) . " of federal tax for a single filer in $Y.</p>"],
  ['How much should I set aside for 1099 taxes?', '<p>A safe starting point is 25–30% of each payment for federal taxes, plus your state rate. Use the calculator’s “set aside” percentage for a personalized figure and update it each quarter as your income changes.</p>'],
  ['What is the self-employment tax rate for ' . $Y . '?', "<p>15.3% — 12.4% Social Security on the first " . money($y['ssWageBase']) . " of net earnings and 2.9% Medicare on everything, applied to 92.35% of net profit. A 0.9% Additional Medicare Tax applies above \$200,000 (single) or \$250,000 (joint). You can deduct half of SE tax when figuring income tax.</p>"],
  ['Does this 1099 tax calculator include deductions?', '<p>Yes. Enter known business expenses, then use the guided section for mileage, home office, phone and internet, plus adjustments for self-employed health insurance and SEP/Solo 401(k) contributions. The standard deduction and the 20% QBI deduction are applied automatically.</p>'],
  ['Do I have to pay taxes on 1099 income under $600?', '<p>Yes. The $600 threshold (rising to $2,000 for payments made after 2025) only decides whether the payer must send a form. All self-employment income is taxable, and SE tax applies once your net earnings reach $400.</p>'],
  ['Can I use this as a 1099 tax calculator for 2025?', '<p>Yes — choose 2025 in the tax year menu to use the 2025 brackets, standard deduction, Social Security wage base and mileage rate.</p>'],
  ['What happens if I don’t pay quarterly taxes on 1099 income?', '<p>The IRS charges an underpayment penalty — essentially interest at the federal short-term rate plus 3% — on each quarter you underpaid. It’s not catastrophic, but it adds up. Paying 100% of last year’s tax (110% above $150k AGI) in four installments avoids it entirely.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('1099-tax-calculator', ['self-employment-tax', 'quarterly-estimated-tax', 's-corp-tax-savings', 'mileage-deduction', 'home-office-deduction', 'federal-income-tax']) ?></div>
