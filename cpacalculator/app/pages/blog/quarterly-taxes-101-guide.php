<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$due = $Y['quarterlyDue'];
/* Example: single freelancer, $80,000 expected net profit, no other income; last year's total tax $11,000. */
$q_net = 80000; $q_prior = 11000;
$q_seb = $q_net * 0.9235;
$q_se = min($q_seb, $Y['ssWageBase']) * 0.124 + $q_seb * 0.029;
$q_pre = max(0, $q_net - $q_se / 2 - $Y['std']['single']);
$q_qbi = min($q_net, $q_pre) * 0.20;
$q_inc = fed_tax($q_pre - $q_qbi, 'single')['tax'];
$q_total = $q_se + $q_inc;
$q_90 = $q_total * 0.90;
$q_req = min($q_90, $q_prior);
echo post_open($SLUG, '2026-11-03'); ?>
<p class="lead">The U.S. tax system is pay-as-you-go. When you work for an employer, withholding handles that automatically. When you earn money with no tax taken out (freelance work, a side business, rental income, investment gains), the IRS expects you to send in tax yourself during the year in four installments called quarterly estimated taxes. This guide explains who has to pay, the <?= TAX_YEAR ?> due dates, how to calculate each payment, the safe-harbor rules that protect you from penalties, and the quickest ways to pay.</p>

<h2 id="what-are">What are quarterly estimated taxes?</h2>
<p>Estimated taxes are advance payments toward your annual tax bill. They cover federal income tax and, if you are self-employed, self-employment tax (Social Security and Medicare). You file them with Form 1040-ES, either online or by mail, and at tax time you list the total you paid on your Form 1040. If you paid more than you owe, the difference is refunded or applied to next year. If you paid too little, you pay the balance and may owe an underpayment penalty.</p>
<p>Income that commonly needs estimated payments:</p>
<ul>
<li>Freelance, contract and gig income (1099-NEC, 1099-K). See <a href="/blog/got-a-1099-exactly-what-to-do-next/">what to do with a 1099</a>.</li>
<li>Sole proprietor, partnership and S corporation profits</li>
<li>Rental income</li>
<li>Interest, dividends and capital gains, including crypto</li>
<li>Alimony from pre-2019 divorce agreements, prizes, and other income with no withholding</li>
<li>Retirement distributions or Social Security where you chose no or low withholding</li>
</ul>

<h2 id="who">Who has to pay quarterly taxes?</h2>
<p>You generally need to make estimated payments if <strong>both</strong> of these are true:</p>
<ol>
<li>You expect to owe at least <strong>$1,000</strong> in federal tax for <?= TAX_YEAR ?> after subtracting withholding and refundable credits, and</li>
<li>Your withholding and refundable credits will be less than the <strong>smaller</strong> of 90% of your <?= TAX_YEAR ?> tax or 100% of your <?= TAX_YEAR - 1 ?> tax (110% if your <?= TAX_YEAR - 1 ?> AGI was over $150,000, or $75,000 if married filing separately).</li>
</ol>
<p>Corporations follow a separate $500 threshold. And there is one more exception: if you had <strong>zero tax liability</strong> last year, were a U.S. citizen or resident all year, and last year was a full 12 months, you owe no penalty this year no matter how little you pay in. That rule is what makes many people's first year of self-employment penalty-free; the details are in <a href="/blog/do-i-have-to-pay-quarterly-taxes-my-first-year/">do I have to pay quarterly taxes my first year?</a></p>

<h2 id="due-dates">2026 quarterly tax due dates</h2>
<p>The four "quarters" are not equal. The second covers only two months and the fourth covers four.</p>
<div class="table-wrap"><table>
<thead><tr><th>Payment</th><th>Covers income earned</th><th>Due date</th></tr></thead>
<tbody>
<tr><td>1st</td><td>January 1 – March 31, <?= TAX_YEAR ?></td><td><b><?= e($due[0]) ?></b></td></tr>
<tr><td>2nd</td><td>April 1 – May 31, <?= TAX_YEAR ?></td><td><b><?= e($due[1]) ?></b></td></tr>
<tr><td>3rd</td><td>June 1 – August 31, <?= TAX_YEAR ?></td><td><b><?= e($due[2]) ?></b></td></tr>
<tr><td>4th</td><td>September 1 – December 31, <?= TAX_YEAR ?></td><td><b><?= e($due[3]) ?></b></td></tr>
</tbody></table></div>
<p>When a date falls on a weekend or legal holiday, the deadline moves to the next business day. You can skip the January payment if you file your <?= TAX_YEAR ?> return and pay the full balance by February 1, <?= TAX_YEAR + 1 ?>. Farmers and fishermen have their own rule: one payment by January 15, or file and pay by March 1. Most states with an income tax use the same or similar dates for state estimated payments.</p>
<div class="callout"><?= icon('calendar') ?><p><strong>Set reminders now.</strong> Penalties are figured separately for each quarter, so a big catch-up payment in January does not erase a penalty for skipping April, June and September. Calendar the dates, or schedule all four payments in advance through EFTPS.</p></div>

<h2 id="safe-harbor">Safe-harbor rules: how to avoid the penalty</h2>
<p>The easiest way to stay penalty-free is to pay at least the "required annual payment," split into four equal installments. That amount is the smaller of:</p>
<div class="table-wrap"><table>
<thead><tr><th>Safe harbor</th><th>Pay at least</th><th>Best when</th></tr></thead>
<tbody>
<tr><td><b>Prior-year rule</b></td><td>100% of last year's total tax (110% if last year's AGI was over $150,000)</td><td>Income is rising or hard to predict; the target is known on day one</td></tr>
<tr><td><b>Current-year rule</b></td><td>90% of this year's total tax</td><td>Income is falling, or last year's tax was unusually high</td></tr>
<tr><td><b>Under $1,000</b></td><td>Owe less than $1,000 after withholding and credits</td><td>Small side income alongside a W-2 job</td></tr>
</tbody></table></div>
<p>"Total tax" means the total tax line on your return (income tax plus self-employment tax and other taxes, minus most credits), not the amount you owed or were refunded. A refund last year does not mean your tax was zero.</p>
<p>The prior-year rule is popular because it gives you a fixed number to hit. If your income jumps, you will still owe a balance in April, but no penalty, as long as each installment was on time.</p>

<h2 id="calculate">How to calculate your quarterly tax payments</h2>
<ol>
<li><strong>Project your income</strong> for the full year: business revenue minus expenses, plus wages, interest, dividends, gains and rental profit.</li>
<li><strong>Figure self-employment tax</strong>: net profit × 92.35% × 15.3% (12.4% Social Security up to the <?= money($Y['ssWageBase']) ?> wage base, plus 2.9% Medicare).</li>
<li><strong>Figure taxable income</strong>: total income minus half of SE tax, retirement and health insurance adjustments, the standard deduction (<?= money($Y['std']['single']) ?> single, <?= money($Y['std']['mfj']) ?> joint) or itemized deductions, and the 20% QBI deduction.</li>
<li><strong>Apply the tax brackets</strong> and subtract credits to get income tax.</li>
<li><strong>Add SE tax and income tax</strong>, then subtract expected withholding.</li>
<li><strong>Pick your target</strong> (90% of that, or 100%/110% of last year's tax, whichever is smaller) and divide by four.</li>
</ol>
<h3 id="example">Example</h3>
<p>A single freelancer expects <?= money($q_net) ?> of net profit in <?= TAX_YEAR ?>, has no other income, and paid <?= money($q_prior) ?> of total tax last year (AGI under $150,000).</p>
<div class="table-wrap"><table><tbody>
<tr><td>Self-employment tax</td><td class="n"><?= money($q_se) ?></td></tr>
<tr><td>Federal income tax (after half-SE, standard and QBI deductions)</td><td class="n"><?= money($q_inc) ?></td></tr>
<tr><td>Projected <?= TAX_YEAR ?> total tax</td><td class="n"><?= money($q_total) ?></td></tr>
<tr><td>90% of current-year tax</td><td class="n"><?= money($q_90) ?></td></tr>
<tr><td>100% of prior-year tax</td><td class="n"><?= money($q_prior) ?></td></tr>
<tr><td><b>Required annual payment</b> (the smaller)</td><td class="n"><b><?= money($q_req) ?></b></td></tr>
<tr><td><b>Each quarterly payment</b></td><td class="n"><b><?= money($q_req / 4) ?></b></td></tr>
</tbody></table></div>
<p>Paying <?= money($q_req / 4) ?> on each due date keeps this freelancer penalty-free. They would still owe about <?= money($q_total - $q_req) ?> when filing in April <?= TAX_YEAR + 1 ?>, so it is wise to keep saving beyond the safe-harbor amount. The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> runs this math with your own numbers, and the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> shows the full-year picture including write-offs.</p>

<h2 id="w2-withholding">Have a W-2 job? Use withholding instead</h2>
<p>If you or your spouse has a job, you can cover tax on side income by increasing withholding: enter an extra amount per paycheck on line 4(c) of Form W-4. Withholding is treated as paid evenly throughout the year regardless of when it actually happened, so raising it in October can fix an underpayment from earlier quarters, something an estimated payment cannot do. The <a href="/calculators/paycheck-calculator/">paycheck calculator</a> shows the effect on take-home pay.</p>

<h2 id="how-to-pay">How to pay quarterly taxes</h2>
<div class="table-wrap"><table>
<thead><tr><th>Method</th><th>How it works</th><th>Good to know</th></tr></thead>
<tbody>
<tr><td><b>IRS Direct Pay</b></td><td>Free bank-account (ACH) payment at irs.gov/payments; no enrollment</td><td>Choose "Estimated Tax" and Form 1040-ES and the correct tax year; schedule up to 365 days ahead</td></tr>
<tr><td><b>IRS Online Account</b></td><td>Pay from your account and see a history of every estimated payment</td><td>Handy at filing time to confirm the total paid</td></tr>
<tr><td><b>EFTPS</b></td><td>Treasury's free Electronic Federal Tax Payment System</td><td>Requires enrollment and a PIN by mail (allow about a week); lets you schedule all four payments at once</td></tr>
<tr><td><b>Debit or credit card / digital wallet</b></td><td>Through IRS-approved payment processors</td><td>Processor fees apply</td></tr>
<tr><td><b>Check or money order</b></td><td>Mail with a Form 1040-ES payment voucher</td><td>Payable to "U.S. Treasury"; write your SSN, tax year and "1040-ES"</td></tr>
</tbody></table></div>
<p>Whatever method you use, keep the confirmation numbers. You will need the total, and the date of each payment, when you file.</p>

<h2 id="penalties">Underpayment penalties</h2>
<p>If you pay too little or too late, the IRS charges an underpayment penalty, figured on <strong>Form 2210</strong>. It works like interest: the federal short-term rate plus 3 percentage points, adjusted each quarter, applied to the shortfall for each installment from its due date until it is paid (or until the April filing deadline). It is not a flat fine, so a small, short shortfall costs little, while skipping all four payments on a large bill adds up.</p>
<p>The IRS may waive the penalty if the underpayment was due to a casualty, disaster or other unusual circumstance, or if you retired after reaching age 62 or became disabled during the year or the prior year and the underpayment was due to reasonable cause. Taxpayers in federally declared disaster areas often get automatic deadline extensions.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>Penalty vs. interest on unpaid tax:</strong> the underpayment penalty is separate from the failure-to-pay penalty and interest that apply if you do not pay your balance by the April filing deadline. Filing an extension gives you more time to file, not more time to pay.</p></div>

<h2 id="annualized">Uneven income? The annualized installment method</h2>
<p>The standard rule assumes you earn income evenly through the year. If most of your income arrives late (a big project in November, a capital gain in December, seasonal work), equal installments would force you to pay tax on money you have not earned yet. The <strong>annualized income installment method</strong> fixes that. Using <strong>Schedule AI of Form 2210</strong>, you calculate each required installment based on the income you actually earned through the end of each period (March 31, May 31, August 31 and December 31). Lower early payments are then not penalized as long as later payments catch up.</p>
<p>It takes more record-keeping, and you must attach Form 2210 with Schedule AI to your return, but it can eliminate a penalty that the regular method would charge.</p>

<h2 id="tips">Tips for staying on track</h2>
<ul>
<li>Move a fixed percentage of every payment you receive into a separate tax savings account.</li>
<li>Recalculate after each quarter. If income changes a lot, adjust the remaining payments.</li>
<li>Count deductions you will actually take, such as mileage, home office and equipment, using the <a href="/calculators/mileage-deduction/">mileage</a> and <a href="/calculators/home-office-deduction/">home office</a> calculators.</li>
<li>Do not forget state estimated taxes; they are separate payments to your state.</li>
<li>Physicians and other high earners have extra wrinkles (110% rule, Additional Medicare Tax); see the <a href="/blog/1099-taxes-for-physicians/">1099 physician tax guide</a>.</li>
</ul>

<?= faq_block([
  ['When are quarterly taxes due in 2026?', '<p>For the 2026 tax year, estimated payments are due April 15, 2026, June 15, 2026, September 15, 2026 and January 15, 2027. If a date falls on a weekend or holiday, the deadline moves to the next business day.</p>'],
  ['How do I calculate my quarterly tax payment?', '<p>Estimate your total tax for the year (income tax plus self-employment tax), subtract withholding, and pay the smaller of 90% of that amount or 100% of last year\'s total tax (110% if last year\'s AGI exceeded $150,000), divided into four payments. The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> does this for you.</p>'],
  ['What happens if I miss a quarterly tax payment?', '<p>You may owe an underpayment penalty, calculated like interest on the missed amount from the due date until you pay. Pay as soon as you can to limit it. If you have a W-2 job, increasing withholding for the rest of the year can also reduce the penalty, because withholding counts as paid evenly through the year.</p>'],
  ['Do I have to pay quarterly taxes if I have a full-time job?', '<p>Usually not, if your withholding covers your tax or you expect to owe less than $1,000. If you have significant side income, you can either make estimated payments or raise your W-4 withholding to cover it.</p>'],
  ['Can I pay all my estimated taxes at once?', '<p>Yes. You can pay the full year\'s estimate with the first installment in April. Paying everything in January, however, does not avoid penalties for the earlier quarters you skipped.</p>'],
  ['What is the 110% rule for estimated taxes?', '<p>If your adjusted gross income last year was over $150,000 ($75,000 if married filing separately), the prior-year safe harbor requires paying 110% of last year\'s total tax instead of 100% to avoid an underpayment penalty.</p>'],
]) ?>
<?= post_close($SLUG, 'quarterly-estimated-tax', ['do-i-have-to-pay-quarterly-taxes-my-first-year', 'got-a-1099-exactly-what-to-do-next', '1099-taxes-for-physicians']) ?>
