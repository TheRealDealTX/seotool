<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$wb = $Y['ssWageBase'];
$qt = $Y['qbiThreshold'];
/* SE tax for a single filer with optional W-2 wages (SS base shared; Additional Medicare per Form 8959). */
$se = function (float $net, float $w2 = 0) use ($Y, $wb): array {
  $base = $net * 0.9235;
  $ss = min($base, max(0, $wb - min($w2, $wb))) * 0.124;
  $med = $base * 0.029;
  $thr = $Y['addlMedicare']['single'];
  $addl = max(0, $base - max(0, $thr - $w2)) * 0.009;
  return ['base' => $base, 'ss' => $ss, 'med' => $med, 'se' => $ss + $med, 'addl' => $addl];
};
$a = $se(250000);
$b = $se(60000, 200000);
/* Retirement example: $200,000 net 1099 profit, no W-2. */
$r_net = 200000;
$r = $se($r_net);
$r_comp = min($r_net - $r['se'] / 2, 360000);
$r_er = $r_comp * 0.20;
$r_solo = min($r_er + $Y['k401'], 72000);
echo post_open($SLUG, '2026-11-03'); ?>
<p class="lead">Locum tenens assignments, moonlighting shifts, telehealth contracts, expert witness work and independent practice all have one thing in common: the pay arrives on a 1099 with no tax withheld. For physicians, that brings a few complications most freelancers never face, including the Social Security wage base interacting with hospital W-2 pay, the Additional Medicare Tax, and the fact that medicine is a "specified service" that loses the QBI deduction at higher incomes. This guide walks through how 1099 physician income is taxed in <?= TAX_YEAR ?> and the planning levers that matter most.</p>

<div class="callout"><?= icon('calc') ?><p><strong>Run your numbers:</strong> the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> handles self-employment tax, income tax, the QBI deduction and quarterly payments in one place. Use it alongside the examples below.</p></div>

<h2 id="how-taxed">How 1099 physician income is taxed</h2>
<p>As an independent contractor, you are a business owner for tax purposes. Your contract income and expenses go on <strong>Schedule C</strong>, and the net profit is subject to two federal taxes:</p>
<ul>
<li><strong>Self-employment tax</strong> on 92.35% of net profit: 12.4% Social Security up to the <?= TAX_YEAR ?> wage base of <?= money($wb) ?>, plus 2.9% Medicare on everything, plus the 0.9% Additional Medicare Tax above <?= money($Y['addlMedicare']['single']) ?> (single) or <?= money($Y['addlMedicare']['mfj']) ?> (married filing jointly).</li>
<li><strong>Federal income tax</strong> at ordinary rates, which for many physicians means the 32%, 35% or 37% brackets. Half of self-employment tax is deductible in figuring income tax.</li>
</ul>
<p>Common physician 1099 situations:</p>
<div class="table-wrap"><table>
<thead><tr><th>Situation</th><th>Typical tax picture</th></tr></thead>
<tbody>
<tr><td>Full-time locums, no W-2</td><td>All income on Schedule C; full SE tax up to the wage base; owns retirement plan choices</td></tr>
<tr><td>Employed physician who moonlights</td><td>W-2 wages usually already exceed the Social Security wage base, so 1099 income mostly bears Medicare only</td></tr>
<tr><td>Resident or fellow moonlighting</td><td>W-2 below the wage base; moonlighting income bears full SE tax; often in the 22–24% bracket</td></tr>
<tr><td>Independent practice or partnership K-1</td><td>Schedule C or K-1 self-employment income; may consider an S corporation</td></tr>
</tbody></table></div>

<h2 id="wage-base">The Social Security wage base and your W-2</h2>
<p>Social Security tax stops once your combined W-2 wages and self-employment earnings reach <?= money($wb) ?> for <?= TAX_YEAR ?>. W-2 wages count first. That makes a big difference to moonlighting physicians:</p>
<div class="table-wrap"><table>
<thead><tr><th></th><th class="n">A: Locums only, $250,000 net</th><th class="n">B: $200,000 W-2 + $60,000 1099</th></tr></thead>
<tbody>
<tr><td>Net SE earnings (× 92.35%)</td><td class="n"><?= money($a['base']) ?></td><td class="n"><?= money($b['base']) ?></td></tr>
<tr><td>Social Security (12.4%)</td><td class="n"><?= money($a['ss']) ?></td><td class="n"><?= money($b['ss']) ?></td></tr>
<tr><td>Medicare (2.9%)</td><td class="n"><?= money($a['med']) ?></td><td class="n"><?= money($b['med']) ?></td></tr>
<tr><td><b>Self-employment tax</b></td><td class="n"><b><?= money($a['se']) ?></b></td><td class="n"><b><?= money($b['se']) ?></b></td></tr>
<tr><td>Additional Medicare Tax (0.9%, single)</td><td class="n"><?= money($a['addl']) ?></td><td class="n"><?= money($b['addl']) ?></td></tr>
<tr><td>Effective SE + Additional Medicare rate on 1099 profit</td><td class="n"><?= number_format(($a['se'] + $a['addl']) / 250000 * 100, 1) ?>%</td><td class="n"><?= number_format(($b['se'] + $b['addl']) / 60000 * 100, 1) ?>%</td></tr>
</tbody></table></div>
<p>In example B, the hospital W-2 already used up the wage base, so Schedule SE charges no Social Security tax on the moonlighting income. Make sure your Schedule SE reflects your W-2 Social Security wages (Box 3, plus Box 7 tips if any); tax software does this when the W-2 is entered. The <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> lets you enter W-2 wages to see the effect.</p>
<p><strong>Additional Medicare Tax</strong> is figured on Form 8959 using combined wages and self-employment earnings. Your employer withholds 0.9% only on wages over $200,000 regardless of filing status, so married physicians, and anyone with large 1099 income, often owe more at filing time than was withheld. Build it into your quarterly estimates.</p>

<h2 id="qbi">The QBI deduction: why physicians often lose it</h2>
<p>The 20% qualified business income deduction (Section 199A), made permanent by OBBBA, lets many self-employed people deduct up to 20% of their business profit. But health care is a <strong>specified service trade or business (SSTB)</strong>, and for SSTBs the deduction phases out as taxable income rises:</p>
<div class="table-wrap"><table>
<thead><tr><th>Filing status (<?= TAX_YEAR ?>)</th><th class="n">Full deduction if taxable income is at or below</th><th class="n">Phase-out range</th><th class="n">No deduction above</th></tr></thead>
<tbody>
<tr><td>Single, head of household</td><td class="n"><?= money($qt['single']) ?></td><td class="n">$75,000</td><td class="n"><?= money($qt['single'] + 75000) ?></td></tr>
<tr><td>Married filing jointly</td><td class="n"><?= money($qt['mfj']) ?></td><td class="n">$150,000</td><td class="n"><?= money($qt['mfj'] + 150000) ?></td></tr>
</tbody></table></div>
<p>OBBBA widened the phase-in ranges from $50,000/$100,000 to $75,000/$150,000 starting in <?= TAX_YEAR ?>. Within the range, both the share of QBI that counts and the deduction itself shrink, and for a sole proprietor with no employees (and so no W-2 wages paid by the business) the deduction falls away quickly. The thresholds use <em>taxable income</em> before the QBI deduction, which is why retirement contributions, the self-employed health insurance deduction and other adjustments can be worth more than their face value for a physician near the threshold: they reduce income tax directly and can restore some or all of the QBI deduction.</p>
<p>Residents, fellows and part-time physicians with moderate household income often sit below the threshold and get the full 20% deduction on moonlighting profit. Attending physicians with a full salary usually do not.</p>

<h2 id="retirement">Solo 401(k) vs. SEP IRA</h2>
<p>A self-employed retirement plan is the largest deduction available to most 1099 physicians. The two main choices:</p>
<div class="table-wrap"><table>
<thead><tr><th></th><th>Solo 401(k)</th><th>SEP IRA</th></tr></thead>
<tbody>
<tr><td>Employer contribution</td><td>Up to 20% of net SE earnings (after the half-SE-tax deduction)</td><td>Same 20% limit</td></tr>
<tr><td>Employee deferral</td><td>Up to <?= money($Y['k401']) ?> (<?= TAX_YEAR ?>), plus <?= money($Y['k401CatchUp']) ?> catch-up at 50+ and a higher catch-up at ages 60–63; <b>shared</b> with any 401(k)/403(b) deferrals at your hospital job</td><td>None</td></tr>
<tr><td>Total cap (<?= TAX_YEAR ?>)</td><td>$72,000 per unrelated employer, plus catch-ups</td><td>$72,000</td></tr>
<tr><td>Roth option</td><td>Yes, for deferrals (and employer contributions if the plan allows)</td><td>Roth SEP contributions now allowed if the provider offers it</td></tr>
<tr><td>Backdoor Roth impact</td><td>None (401(k) balances are excluded from the pro-rata rule)</td><td>SEP balances count in the pro-rata rule</td></tr>
<tr><td>Paperwork</td><td>Plan document; Form 5500-EZ once assets exceed $250,000</td><td>Minimal</td></tr>
</tbody></table></div>
<p>For a physician with <?= money($r_net) ?> of net 1099 profit and no W-2 job, the employer contribution limit is about <?= money($r_er) ?> (20% of <?= money($r_comp) ?>). A SEP IRA stops there. A Solo 401(k) adds the <?= money($Y['k401']) ?> employee deferral, for roughly <?= money($r_solo) ?> in total.</p>
<p>If you already defer the full <?= money($Y['k401']) ?> at your employer, a Solo 401(k) only offers the employer portion, the same as a SEP. A Solo 401(k) is still often preferred because it keeps the backdoor Roth clean. Hospital 457(b) plans have their own separate deferral limit and do not count against the 401(k) limit.</p>

<h3 id="backdoor-roth">A note on the backdoor Roth</h3>
<p>Most attending physicians earn too much to contribute to a Roth IRA directly, so many use the "backdoor": a nondeductible traditional IRA contribution (up to <?= money($Y['ira']) ?> for <?= TAX_YEAR ?>, plus <?= money($Y['iraCatchUp']) ?> at 50+) followed by a Roth conversion, reported on Form 8606. The catch is the pro-rata rule. Any pre-tax balance in a traditional, SEP or SIMPLE IRA on December 31 of the conversion year makes part of the conversion taxable. That is the main reason many 1099 physicians choose a Solo 401(k) over a SEP IRA, or roll SEP money into a 401(k) before converting.</p>

<h2 id="deductions">Deductible expenses for 1099 physicians</h2>
<p>Expenses that are ordinary and necessary for your contract work and not reimbursed by the agency or facility can be deducted on Schedule C:</p>
<ul>
<li>State medical licenses, DEA registration and controlled substance permits</li>
<li>Board certification, recertification and maintenance of certification fees</li>
<li>Malpractice insurance you pay yourself, including tail coverage</li>
<li>Continuing medical education (CME) courses, materials and related travel</li>
<li>Professional society and medical association dues, journals and clinical reference subscriptions</li>
<li>Travel to temporary locum assignments away from your tax home (airfare, lodging, 50% of meals), if not reimbursed</li>
<li>Business mileage at <?= number_format($Y['mileage'] * 100, 1) ?>¢ per mile for <?= TAX_YEAR ?> (<a href="/calculators/mileage-deduction/">mileage deduction calculator</a>); commuting to a regular work location does not count</li>
<li>A home office used regularly and exclusively for charting, telehealth or administration (<a href="/calculators/home-office-deduction/">home office calculator</a>)</li>
<li>Computer, phone and software used for the business, often deductible in full in the year purchased under Section 179 or 100% bonus depreciation (<a href="/calculators/depreciation-calculator/">depreciation calculator</a>)</li>
<li>Credentialing, billing, accounting and legal fees</li>
</ul>
<p>Two deductions come off the front of the return rather than Schedule C: <strong>self-employed health insurance premiums</strong> (only for months you were not eligible for a subsidized plan through an employer, including a spouse's) and <strong>retirement plan contributions</strong>.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>Watch your tax home.</strong> Travel is deductible only when you are away from your tax home on a temporary assignment. If a single locum assignment is expected to last more than a year, or you have no regular place of business, travel costs may not be deductible. Keep records of assignment dates and locations.</p></div>

<h2 id="s-corp">Should a 1099 physician form an S corporation?</h2>
<p>An S corporation can reduce payroll taxes because you pay yourself a reasonable salary (subject to Social Security and Medicare) and take the rest as distributions (not subject to either). For physicians, the math depends heavily on where your income falls relative to the wage base:</p>
<ul>
<li><strong>Full-time locums with no W-2 job:</strong> potential savings can be meaningful, because a portion of income would otherwise bear 15.3% SE tax. But "reasonable compensation" for a physician is high, which limits how much you can move into distributions.</li>
<li><strong>Employed physicians moonlighting:</strong> your W-2 already maxes out Social Security, so the 1099 income only bears 2.9% Medicare (plus 0.9% Additional Medicare, which still applies to S corp salary). Savings are usually small compared with payroll, accounting and state costs.</li>
<li><strong>State considerations:</strong> some states tax S corporations or charge minimum fees, while many offer a pass-through entity tax (PTET) election that can work around the federal SALT cap.</li>
</ul>
<p>The <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a> compares the two structures with your numbers. An S corporation also changes how retirement contributions are calculated (they are based on W-2 salary only), so model both together.</p>

<h2 id="quarterly">Quarterly estimated payments for physicians</h2>
<p>No one withholds tax from 1099 income, so you will usually need quarterly estimated payments, due <?= e(implode(', ', $Y['quarterlyDue'])) ?>. Two physician-specific points:</p>
<ul>
<li><strong>The 110% rule:</strong> if last year's AGI was over $150,000, the prior-year safe harbor requires paying 110% of last year's total tax, not 100%.</li>
<li><strong>Use your W-2:</strong> if you have hospital employment, raising withholding on your W-4 is often easier than separate estimated payments, and withholding counts as paid evenly through the year even if you increase it late.</li>
</ul>
<p>The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> works out each installment, and <a href="/blog/quarterly-taxes-101-guide/">Quarterly Taxes 101</a> covers payment methods and penalties. If this is your first year on 1099s after residency, see <a href="/blog/do-i-have-to-pay-quarterly-taxes-my-first-year/">do I have to pay quarterly taxes my first year?</a></p>

<h2 id="checklist">1099 physician tax checklist</h2>
<ul>
<li>Collect every 1099-NEC (and confirm amounts against your contracts and deposits)</li>
<li>Enter W-2 Social Security wages so Schedule SE stops at the wage base</li>
<li>Track licenses, CME, malpractice, dues, travel and equipment</li>
<li>Open a Solo 401(k) before year-end if you want employee deferrals for the year</li>
<li>Check whether your taxable income is near the QBI threshold</li>
<li>Pay quarterly estimates (110% of last year's tax if AGI exceeded $150,000)</li>
<li>Review state tax filing requirements for each state where you worked</li>
</ul>
<p>Because multi-state locums work, entity choices and retirement plans interact, many physicians work with a CPA or enrolled agent who handles medical professionals. Use the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> to arrive at that meeting with good estimates.</p>

<?= faq_block([
  ['How much should a 1099 physician set aside for taxes?', '<p>It depends on total income, filing status and state, but attending physicians with significant 1099 income often face a combined federal marginal rate of roughly 35–41% on each extra 1099 dollar once income tax, Medicare, Additional Medicare and (below the wage base) Social Security tax are included, plus state tax. Run your numbers in the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> rather than relying on a rule of thumb.</p>'],
  ['Do I pay Social Security tax on moonlighting income if I have a W-2 job?', '<p>Only up to the Social Security wage base, which is $184,500 for 2026. W-2 wages count first, so if your hospital salary already exceeds that amount, your moonlighting income bears only the 2.9% Medicare portion of self-employment tax plus any 0.9% Additional Medicare Tax.</p>'],
  ['Can physicians take the QBI deduction?', '<p>Medicine is a specified service business, so the 20% QBI deduction phases out above $201,750 of taxable income for single filers and $403,500 for married couples filing jointly in 2026, and disappears entirely $75,000 or $150,000 above those amounts. Below the thresholds, physicians qualify like any other business.</p>'],
  ['Is a Solo 401(k) or SEP IRA better for a locums physician?', '<p>A Solo 401(k) usually allows larger contributions at moderate income because it adds an employee deferral on top of the employer contribution, and its balance does not interfere with backdoor Roth conversions. If you already max out deferrals at another job, the contribution limits are similar, but the backdoor Roth advantage often still favors the Solo 401(k).</p>'],
  ['Should a 1099 physician form an S corp?', '<p>It can save payroll tax for physicians whose 1099 income is their main income, but the savings shrink when a W-2 job already covers the Social Security wage base, and a physician\'s reasonable salary must be high. Compare costs and savings with the <a href="/calculators/s-corp-tax-savings/">S corp calculator</a> and a tax professional.</p>'],
  ['Are locum tenens travel expenses deductible?', '<p>Unreimbursed travel to a temporary assignment away from your tax home, including airfare, lodging and 50% of meals, is generally deductible on Schedule C. Assignments expected to last more than one year are not temporary, and commuting to a regular work location is never deductible.</p>'],
]) ?>
<?= post_close($SLUG, '1099-tax-calculator', ['got-a-1099-exactly-what-to-do-next', 'quarterly-taxes-101-guide', 'how-much-federal-tax-will-i-pay']) ?>
