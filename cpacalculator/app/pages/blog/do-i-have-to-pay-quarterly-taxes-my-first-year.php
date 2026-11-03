<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$PY = TAX_YEAR - 1;
$due = $Y['quarterlyDue'];
/* Full-year federal tax on Schedule C net profit (single, no other income, standard deduction, QBI). */
$se_calc = function (float $net) use ($Y): array {
  $base = $net * 0.9235;
  $se = $base >= 400 ? min($base, $Y['ssWageBase']) * 0.124 + $base * 0.029 : 0;
  $pre = max(0, $net - $se / 2 - $Y['std']['single']);
  $inc = fed_tax($pre - min($net, $pre) * 0.20, 'single')['tax'];
  return ['se' => $se, 'inc' => $inc, 'total' => $se + $inc];
};
/* Example B: quit a $70,000 W-2 job at the end of last year; expects $90,000 net 1099 profit this year. */
$b_prior = salary_breakdown(70000, 'single', $PY)['tax'];
$b_now = $se_calc(90000);
/* Example D: W-2 $60,000 with normal withholding plus $4,000 side profit. */
$d_side = $se_calc(4000);
$d_extra_se = 4000 * 0.9235 * 0.153;
$d_marg = salary_breakdown(60000, 'single')['marginal'];
$d_extra_inc = (4000 - $d_extra_se / 2) * 0.8 * $d_marg;
echo post_open($SLUG, '2026-11-03'); ?>
<p class="lead">You just started freelancing, picked up contract work, or opened a small business, and nobody is withholding tax from your income anymore. Do you have to pay quarterly taxes your first year? The honest answer is "it depends on last year." Many first-year self-employed people owe no penalty at all if they skip estimated payments, while others need to start in April. This guide explains the rules, with examples, so you can tell which group you are in.</p>

<div class="callout"><?= icon('spark') ?><p><strong>Quick answer:</strong> if your total tax on last year's return was <strong>$0</strong>, last year was a full 12-month tax year, and you were a U.S. citizen or resident all year, the IRS will not charge an underpayment penalty this year, even if you make no estimated payments. Otherwise, you generally need quarterly payments if you will owe $1,000 or more, and you can meet the requirement by paying 100% of last year's tax (110% if last year's AGI was over $150,000).</p></div>

<h2 id="the-rule">The general rule for estimated taxes</h2>
<p>The IRS wants tax paid as income is earned. For individuals, that means you should make estimated payments if you expect to owe at least <strong>$1,000</strong> when you file, after subtracting withholding and refundable credits. Being new to self-employment does not change that rule by itself. What protects many first-year freelancers is a set of exceptions that remove the <em>penalty</em> for not paying:</p>
<ol>
<li><strong>The zero-liability exception</strong> (prior year tax was $0)</li>
<li><strong>The $1,000 rule</strong> (you will owe less than $1,000)</li>
<li><strong>The safe harbors:</strong> pay at least 90% of this year's tax or 100% of last year's (110% for higher incomes), whichever is smaller</li>
</ol>
<p>If any of these applies, you will not owe an underpayment penalty. You still owe the tax itself by the April filing deadline.</p>

<h2 id="zero-liability">The prior-year zero liability exception</h2>
<p>This is the rule that answers most first-year questions. Under Internal Revenue Code §6654(e)(2), no underpayment penalty applies for <?= TAX_YEAR ?> if <strong>all three</strong> of these are true:</p>
<ul>
<li>You had <strong>no tax liability</strong> for <?= $PY ?>.</li>
<li>Your <?= $PY ?> tax year covered a <strong>full 12 months</strong>.</li>
<li>You were a <strong>U.S. citizen or resident</strong> for the whole of <?= $PY ?>.</li>
</ul>
<p>"No tax liability" means the <em>total tax</em> on your <?= $PY ?> Form 1040 was zero, or you were not required to file at all. It does <strong>not</strong> mean you got a refund. If your W-2 employer withheld $6,000 and your total tax was $5,000, you received a $1,000 refund but your tax liability was $5,000, so this exception does not apply.</p>
<p>Who typically qualifies:</p>
<ul>
<li>Recent graduates whose income last year was below the standard deduction</li>
<li>People who were not working, were caring for family, or were between jobs all of last year with little income</li>
<li>People whose credits (for example the child tax credit and earned income credit) reduced total tax to zero</li>
</ul>
<p>Who does not: anyone who moved to the U.S. partway through last year (not a resident for the full year), and anyone whose prior year return showed any total tax.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>No penalty is not the same as no tax.</strong> The exception only removes the penalty. If you earn $60,000 freelancing this year, you will owe the full income tax and self-employment tax in April. Without quarterly payments, that bill arrives all at once, so set the money aside as you earn it.</p></div>

<h2 id="1000-rule">The $1,000 rule</h2>
<p>If your <?= TAX_YEAR ?> tax, minus withholding and refundable credits, will be under $1,000, there is no penalty. This often covers a small side business alongside a regular job. Remember that self-employment tax counts: on a net profit of just $5,000, self-employment tax alone is about <?= money(5000 * 0.9235 * 0.153) ?> before any income tax, so the $1,000 line comes sooner than many people expect.</p>

<h2 id="safe-harbor">The 100% / 110% safe harbor (most career switchers)</h2>
<p>If you had a W-2 job last year and paid tax through withholding, the zero-liability exception will not help you. But the prior-year safe harbor usually does, and it is often generous in the first year:</p>
<div class="table-wrap"><table>
<thead><tr><th>Your <?= $PY ?> AGI</th><th>Pay at least this during <?= TAX_YEAR ?> to avoid a penalty</th></tr></thead>
<tbody>
<tr><td>$150,000 or less ($75,000 or less if married filing separately)</td><td>The smaller of 90% of your <?= TAX_YEAR ?> tax or <b>100%</b> of your <?= $PY ?> total tax</td></tr>
<tr><td>Over $150,000 (over $75,000 if MFS)</td><td>The smaller of 90% of your <?= TAX_YEAR ?> tax or <b>110%</b> of your <?= $PY ?> total tax</td></tr>
</tbody></table></div>
<p>Your <?= $PY ?> total tax only reflected income tax on your wages. Your employer paid half of your Social Security and Medicare tax, and your half was withheld from your paychecks; neither counts in the total tax on your Form 1040. As a freelancer you now owe the full 15.3% self-employment tax too, so your <?= TAX_YEAR ?> tax is often much higher than last year's. The safe harbor lets you pay based on the smaller, known number. You settle the difference in April without a penalty.</p>

<h2 id="w2-trick">The W-2 withholding trick</h2>
<p>Withholding gets special treatment: the IRS treats it as paid in four equal parts on the due dates, no matter when it was actually withheld. Estimated payments, by contrast, are credited on the date you make them. That creates two useful strategies:</p>
<ul>
<li><strong>If you left a job mid-year</strong>, the withholding from your W-2 months may already cover much of your safe-harbor amount, and it counts as spread evenly across all four quarters.</li>
<li><strong>If you or your spouse still has a job</strong>, increase withholding on Form W-4 (line 4(c), "extra withholding") to cover your side income. Even a late-year increase counts as if it had been paid evenly, which can wipe out penalties for missed earlier quarters. Married couples filing jointly can use one spouse's paycheck to cover the other's freelance tax.</li>
</ul>

<h2 id="examples">Examples</h2>
<h3 id="example-a">A: Recent graduate, zero liability last year</h3>
<p>Maya graduated in <?= $PY ?>, earned $8,000 at a part-time job (below the <?= money($TAX['years'][(string) $PY]['std']['single']) ?> standard deduction), and her <?= $PY ?> total tax was $0. In <?= TAX_YEAR ?> she freelances full time. Because her prior-year liability was zero and she was a U.S. citizen for the full 12-month year, <strong>she owes no underpayment penalty for <?= TAX_YEAR ?></strong>, even with no quarterly payments. She should still save for her April bill, and she will need quarterly payments starting in <?= TAX_YEAR + 1 ?>, when her <?= TAX_YEAR ?> tax becomes the new prior-year benchmark.</p>

<h3 id="example-b">B: Left a $70,000 job to freelance full time</h3>
<p>Jordan, single, earned $70,000 in W-2 wages in <?= $PY ?> and had a total tax of about <?= money($b_prior) ?>. He started freelancing on January 1, <?= TAX_YEAR ?> and expects <?= money(90000) ?> of net profit.</p>
<div class="table-wrap"><table><tbody>
<tr><td>Projected <?= TAX_YEAR ?> self-employment tax</td><td class="n"><?= money($b_now['se']) ?></td></tr>
<tr><td>Projected <?= TAX_YEAR ?> income tax</td><td class="n"><?= money($b_now['inc']) ?></td></tr>
<tr><td>Projected <?= TAX_YEAR ?> total tax</td><td class="n"><?= money($b_now['total']) ?></td></tr>
<tr><td>90% of <?= TAX_YEAR ?> tax</td><td class="n"><?= money($b_now['total'] * 0.9) ?></td></tr>
<tr><td>100% of <?= $PY ?> tax (AGI under $150,000)</td><td class="n"><?= money($b_prior) ?></td></tr>
<tr><td><b>Safe-harbor quarterly payment</b></td><td class="n"><b><?= money(min($b_prior, $b_now['total'] * 0.9) / 4) ?></b></td></tr>
</tbody></table></div>
<p>Jordan pays about <?= money(min($b_prior, $b_now['total'] * 0.9) / 4) ?> on each of the four due dates and is protected from penalties. He still owes roughly <?= money($b_now['total'] - min($b_prior, $b_now['total'] * 0.9)) ?> in April <?= TAX_YEAR + 1 ?>, so he keeps saving above the safe-harbor amount.</p>

<h3 id="example-c">C: Switched mid-year</h3>
<p>Priya worked a W-2 job from January through June and had federal tax withheld, then started consulting in July. Her W-2 withholding for those six months is treated as paid evenly on all four due dates. If it adds up to at least 100% of her prior-year tax (or 110% if her prior-year AGI exceeded $150,000), she needs <strong>no estimated payments at all</strong> to avoid a penalty. If it falls short, she only needs to make up the gap with her September and January payments, although making them as early as possible is safest.</p>

<h3 id="example-d">D: Side hustle on top of a full-time job</h3>
<p>Sam earns $60,000 at a job with normal withholding and makes $4,000 of profit selling photography. The side income adds roughly <?= money($d_extra_se) ?> of self-employment tax plus about <?= money($d_extra_inc) ?> of income tax at his <?= round($d_marg * 100) ?>% bracket, a total close to the $1,000 line. Rather than file quarterly vouchers, Sam adds about <?= money(($d_extra_se + $d_extra_inc) / 26) ?> per biweekly paycheck on line 4(c) of his W-4 and is covered.</p>

<h2 id="what-to-do">What to do in your first year</h2>
<ol>
<li><strong>Pull last year's return</strong> and find the total tax line. That one number tells you which rule applies.</li>
<li><strong>Estimate this year's tax</strong> with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> (or the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> for the SE portion).</li>
<li><strong>Choose your target:</strong> zero (if the zero-liability exception applies), or the smaller of 90% of this year's tax and 100%/110% of last year's.</li>
<li><strong>Divide by four and pay by each due date</strong> (<?= e(implode(', ', $due)) ?>) using IRS Direct Pay, EFTPS or your IRS Online Account, or cover it with W-2 withholding. The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> lays out each payment.</li>
<li><strong>Save the rest</strong> of your projected tax in a separate account for April.</li>
<li><strong>Check your state's rules.</strong> Most states with an income tax have their own estimated payment requirements and thresholds.</li>
</ol>
<p>For the bigger picture on deadlines, payment methods and the annualized method for lumpy income, read <a href="/blog/quarterly-taxes-101-guide/">Quarterly Taxes 101</a>. If you just received your first 1099, start with <a href="/blog/got-a-1099-exactly-what-to-do-next/">Got a 1099? Here's what to do next</a>.</p>

<h2 id="year-two">Planning ahead for year two</h2>
<p>Your first full year of self-employment becomes the benchmark for your second. If you used the zero-liability exception or the prior-year safe harbor this year, your <?= TAX_YEAR + 1 ?> safe harbor will be 100% (or 110%) of your <?= TAX_YEAR ?> total tax, which now includes self-employment tax. Expect your quarterly payments to rise noticeably in year two, and budget for both the April balance from year one and the first year-two estimate, which are due on the same day.</p>

<?= faq_block([
  ['Do I have to pay quarterly taxes my first year of self-employment?', '<p>Not always. If your total tax last year was zero, last year was a full 12-month year and you were a U.S. citizen or resident all year, there is no underpayment penalty this year even without estimated payments. Otherwise, you generally need to pay quarterly if you will owe $1,000 or more, and paying 100% of last year\'s tax (110% if your AGI was over $150,000) in four installments protects you.</p>'],
  ['Does getting a refund last year mean I had zero tax liability?', '<p>No. Zero liability means the total tax on your return was $0. A refund only means your withholding was more than your tax. If your return showed any total tax, use the prior-year safe harbor instead.</p>'],
  ['What happens if I do not pay quarterly taxes my first year?', '<p>If none of the exceptions apply, the IRS charges an underpayment penalty, figured like interest on each late or missing installment. You also still owe the full tax when you file. If an exception applies, you owe only the tax, with no penalty.</p>'],
  ['How much should I pay in quarterly taxes my first year?', '<p>The smaller of 90% of this year\'s projected tax or 100% of last year\'s total tax (110% if last year\'s AGI exceeded $150,000), divided by four. If last year\'s tax was zero and you qualify for the exception, the minimum to avoid a penalty is zero, but saving for April is still essential.</p>'],
  ['I started my business in the middle of the year. When is my first payment due?', '<p>Your first payment is due on the next quarterly due date after you first have income that requires estimated tax. For example, if you start in July, your first payment would generally be due September 15, and you can pay the year\'s required amount in the remaining installments. Because the regular penalty calculation assumes equal quarterly installments, use the annualized income installment method (Form 2210, Schedule AI) when you file so you are not penalized for the earlier quarters when you had no income.</p>'],
  ['Can W-2 withholding replace quarterly estimated payments?', '<p>Yes. Withholding from your job, or your spouse\'s job if you file jointly, counts toward the safe harbor and is treated as paid evenly through the year. Increasing it with a new Form W-4 is a simple alternative to quarterly vouchers.</p>'],
]) ?>
<?= post_close($SLUG, 'quarterly-estimated-tax', ['quarterly-taxes-101-guide', 'got-a-1099-exactly-what-to-do-next', 'how-much-federal-tax-will-i-pay']) ?>
