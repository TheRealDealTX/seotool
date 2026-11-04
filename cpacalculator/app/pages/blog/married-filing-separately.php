<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
/* Worked example: spouse A earns $120,000, spouse B earns $40,000 in W-2 wages, standard deduction, no credits. */
$inc_a = 120000; $inc_b = 40000;
$j_taxable = max(0, $inc_a + $inc_b - $Y['std']['mfj']);
$j_tax = fed_tax($j_taxable, 'mfj')['tax'];
$a_taxable = max(0, $inc_a - $Y['std']['mfs']);
$b_taxable = max(0, $inc_b - $Y['std']['mfs']);
$a = fed_tax($a_taxable, 'mfs');
$b = fed_tax($b_taxable, 'mfs');
$s_tax = $a['tax'] + $b['tax'];
$diff = $s_tax - $j_tax;
$j_marg = fed_tax($j_taxable, 'mfj')['marginal'];
$pc = fn(float $x): string => round($x * 100) . '%';
/* Where MFS brackets stop matching single brackets. */
$mfs35 = $Y['brackets']['mfs'][5][0];
$single35 = $Y['brackets']['single'][5][0];
$saltMfs = $Y['saltCap'] / 2;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">Married filing separately (MFS) lets each spouse file their own return and report only their own income, deductions and credits. For most couples it costs more than filing jointly, because the separate status loses or limits a long list of credits and deductions. But "most" is not "all." Married filing separately can make sense when one spouse has large medical expenses, is on an income-driven student loan plan, or simply does not want to be liable for the other spouse's tax. This guide compares married filing separately vs jointly for <?= TAX_YEAR ?>, with the brackets, the rules you give up, and a worked example.</p>

<div class="callout"><?= icon('spark') ?><p><strong>The short version:</strong> run the numbers both ways before you choose. In the example below, a couple earning <?= money($inc_a) ?> and <?= money($inc_b) ?> pays <?= money($diff) ?> more by filing separately, before counting any credits they would lose. Filing separately usually wins only when it unlocks something specific: a medical deduction, a lower student loan payment, or protection from a spouse's tax problems.</p></div>

<h2 id="what-is-mfs">What married filing separately means</h2>
<p>If you are legally married on December 31, the IRS treats you as married for the whole year. You then have two choices: <strong>married filing jointly</strong> (MFJ), where you combine everything on one return, or <strong>married filing separately</strong>, where each spouse files a return showing their own income and deductions.</p>
<p>Choosing MFS does not change anything legally about your marriage. It is purely a tax filing choice, and you can make a different choice every year.</p>

<h2 id="brackets">Married filing separately tax brackets for <?= TAX_YEAR ?></h2>
<p>The MFS brackets are exactly half of the joint brackets. Through the 32% bracket, that makes them identical to the single brackets. The difference shows up at the top: the 35% bracket ends at <?= money($mfs35) ?> for separate filers versus <?= money($single35) ?> for single filers, so high earners reach the 37% rate much sooner.</p>
<?= bracket_table('mfs') ?>
<p>Here is how the two married statuses compare on the key numbers:</p>
<div class="table-wrap"><table>
<caption class="sr-only"><?= TAX_YEAR ?> married filing jointly vs separately key figures</caption>
<thead><tr><th>Item (<?= TAX_YEAR ?>)</th><th class="n">Married filing jointly</th><th class="n">Married filing separately (each)</th></tr></thead>
<tbody>
<tr><td>Standard deduction</td><td class="n"><?= money($Y['std']['mfj']) ?></td><td class="n"><?= money($Y['std']['mfs']) ?></td></tr>
<tr><td>Top of 12% bracket</td><td class="n"><?= money($Y['brackets']['mfj'][1][0]) ?></td><td class="n"><?= money($Y['brackets']['mfs'][1][0]) ?></td></tr>
<tr><td>Top of 24% bracket</td><td class="n"><?= money($Y['brackets']['mfj'][3][0]) ?></td><td class="n"><?= money($Y['brackets']['mfs'][3][0]) ?></td></tr>
<tr><td>37% bracket starts above</td><td class="n"><?= money($Y['brackets']['mfj'][5][0]) ?></td><td class="n"><?= money($mfs35) ?></td></tr>
<tr><td>SALT deduction cap</td><td class="n"><?= money($Y['saltCap']) ?></td><td class="n"><?= money($saltMfs) ?></td></tr>
<tr><td>Additional Medicare / NIIT threshold</td><td class="n"><?= money($Y['addlMedicare']['mfj']) ?></td><td class="n"><?= money($Y['addlMedicare']['mfs']) ?></td></tr>
<tr><td>Child tax credit phase-out starts</td><td class="n"><?= money($Y['ctc']['phaseStart']['mfj']) ?></td><td class="n"><?= money($Y['ctc']['phaseStart']['mfs']) ?></td></tr>
<tr><td>Net capital loss deduction limit</td><td class="n">$3,000</td><td class="n">$1,500</td></tr>
</tbody></table></div>
<p>Because almost every number is exactly halved, two spouses with <em>equal</em> incomes and no special deductions usually pay about the same total either way. The gap opens when incomes are uneven: filing jointly lets the higher earner's income spill into the lower brackets the other spouse is not using.</p>

<h2 id="example">Married filing separately vs jointly: a worked example</h2>
<p>Take a couple where one spouse earns <?= money($inc_a) ?> and the other earns <?= money($inc_b) ?> in W-2 wages. They have no children, take the standard deduction and have no other income. Using the <?= TAX_YEAR ?> tables:</p>
<div class="table-wrap"><table>
<caption class="sr-only">MFJ vs MFS example for <?= money($inc_a) ?> and <?= money($inc_b) ?></caption>
<thead><tr><th></th><th class="n">Joint return</th><th class="n">Spouse A (MFS)</th><th class="n">Spouse B (MFS)</th></tr></thead>
<tbody>
<tr><td>Wages</td><td class="n"><?= money($inc_a + $inc_b) ?></td><td class="n"><?= money($inc_a) ?></td><td class="n"><?= money($inc_b) ?></td></tr>
<tr><td>Standard deduction</td><td class="n">−<?= money($Y['std']['mfj']) ?></td><td class="n">−<?= money($Y['std']['mfs']) ?></td><td class="n">−<?= money($Y['std']['mfs']) ?></td></tr>
<tr><td>Taxable income</td><td class="n"><?= money($j_taxable) ?></td><td class="n"><?= money($a_taxable) ?></td><td class="n"><?= money($b_taxable) ?></td></tr>
<tr><td>Federal income tax</td><td class="n"><?= money($j_tax) ?></td><td class="n"><?= money($a['tax']) ?></td><td class="n"><?= money($b['tax']) ?></td></tr>
<tr><td>Marginal rate</td><td class="n"><?= $pc($j_marg) ?></td><td class="n"><?= $pc($a['marginal']) ?></td><td class="n"><?= $pc($b['marginal']) ?></td></tr>
<tr class="total"><td><b>Total household tax</b></td><td class="n"><b><?= money($j_tax) ?></b></td><td class="n" colspan="2"><b><?= money($s_tax) ?></b></td></tr>
</tbody></table></div>
<p>Filing separately costs this couple <strong><?= money($diff) ?></strong> a year. The reason is visible in the marginal rates: on separate returns, part of spouse A's income is taxed at <?= $pc($a['marginal']) ?> while spouse B still has room in the 12% bracket. On a joint return, all of their income fits inside the brackets up to <?= $pc($j_marg) ?>. If they had children, the gap would usually widen, because some credits disappear entirely on separate returns.</p>
<p>You can test your own numbers with the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>: run it once as married filing jointly with combined income, then twice as married filing separately with each spouse's income, and add the two separate results.</p>

<h2 id="what-you-lose">Credits and deductions you lose or limit by filing separately</h2>
<p>The bigger cost of married filing separately is often not the brackets but the benefits the tax code denies or shrinks for separate filers:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Tax benefits affected by married filing separately</caption>
<thead><tr><th>Benefit</th><th>Effect of filing separately</th></tr></thead>
<tbody>
<tr><td>Earned income tax credit</td><td>Generally not allowed. A limited exception applies to a separated spouse who has a qualifying child living with them for more than half the year and who lived apart from the other spouse for the last six months of the year (or is legally separated under an agreement).</td></tr>
<tr><td>American opportunity and lifetime learning credits</td><td>Not allowed.</td></tr>
<tr><td>Student loan interest deduction</td><td>Not allowed.</td></tr>
<tr><td>Child and dependent care credit</td><td>Generally not allowed unless you lived apart and meet the rules to be treated as unmarried. The tax-free dependent care FSA limit is also halved for each spouse.</td></tr>
<tr><td>Premium tax credit (Marketplace insurance)</td><td>Generally not allowed, with exceptions for victims of domestic abuse or spousal abandonment.</td></tr>
<tr><td>Adoption credit</td><td>Generally not allowed unless you lived apart and meet the rules to be treated as unmarried.</td></tr>
<tr><td>New OBBBA deductions for tips, overtime and seniors</td><td>Married taxpayers must file jointly to claim the qualified tips deduction, the qualified overtime deduction and the extra <?= money($Y['senior']['amount']) ?> senior deduction.</td></tr>
<tr><td>Traditional IRA deduction and Roth IRA contributions</td><td>If you lived with your spouse at any time during the year, the phase-out range is only $0 to $10,000 of modified AGI, which eliminates the deduction (if you are covered by a workplace plan) and the Roth contribution for most people.</td></tr>
<tr><td>SALT and capital losses</td><td>The state and local tax cap is <?= money($saltMfs) ?> per spouse, and net capital losses are limited to $1,500 against ordinary income.</td></tr>
</tbody></table></div>
<p>A few more rules catch couples off guard:</p>
<ul>
<li><strong>The itemizing rule.</strong> If one spouse itemizes deductions, the other spouse must itemize too. Their standard deduction becomes zero, even if their own itemized deductions are tiny. Couples have to coordinate who claims shared costs like mortgage interest and property tax (generally, the spouse who paid it, from their own funds).</li>
<li><strong>Social Security benefits.</strong> For most filers, a "base amount" of income can be received before any Social Security benefits are taxable. For married filing separately taxpayers who lived with their spouse at any time during the year, the base amount is <strong>$0</strong>, so up to 85% of benefits can be taxable regardless of income.</li>
<li><strong>Child tax credit.</strong> It is still available on a separate return, but only the parent who claims the child as a dependent can take it, and the phase-out starts at <?= money($Y['ctc']['phaseStart']['mfs']) ?> of AGI instead of <?= money($Y['ctc']['phaseStart']['mfj']) ?>.</li>
</ul>

<h2 id="when-mfs-wins">When married filing separately makes sense</h2>
<p>Despite the long list above, there are real situations where married filing separately is the better choice:</p>
<h3 id="medical">Large medical or casualty expenses</h3>
<p>Medical expenses are deductible only above 7.5% of AGI. On a joint return, the floor is based on combined income. If the lower-earning spouse had large medical bills, filing separately applies the 7.5% floor to that spouse's income alone, which can unlock a sizable deduction. Remember that the other spouse must then itemize too, so this only works when the medical deduction is large enough to beat the lost standard deduction and lost credits.</p>
<h3 id="student-loans">Income-driven student loan repayment</h3>
<p>Federal income-driven repayment plans calculate the monthly payment from your adjusted gross income on your tax return. For a borrower married to a higher earner, filing separately can keep the spouse's income out of the calculation and lower the payment substantially, sometimes by more than the extra tax. Plan rules have changed repeatedly, including new plans created by the 2025 tax law, so confirm with your loan servicer how your specific plan treats a separate return before you decide. This is one of the most common reasons couples choose MFS.</p>
<h3 id="liability">Protection from a spouse's tax liability</h3>
<p>A joint return makes both spouses <strong>jointly and severally liable</strong>: the IRS can collect the full tax, interest and penalties from either spouse, even if the error came entirely from the other spouse's income. Filing separately limits your liability to your own return. If you have doubts about your spouse's reporting, are separated, or are in the middle of a divorce, MFS is often the safer choice. (If you already filed jointly, innocent spouse relief may help, but it is harder to get than avoiding the problem in the first place.)</p>
<h3 id="refund-offset">Protecting a refund from a spouse's debts</h3>
<p>A joint refund can be taken to pay one spouse's past-due child support, federal debts or state taxes. Injured spouse relief (Form 8379) can recover your share, but filing separately avoids the offset of your refund in the first place.</p>

<div class="callout warn"><?= icon('shield') ?><p><strong>Timing matters.</strong> You can switch from married filing separately to a joint return later by filing an amended return within the normal three-year window. You generally <em>cannot</em> switch from a joint return to separate returns after the filing deadline has passed. If you are unsure, see our guide to the <a href="/blog/amended-tax-return/">amended tax return</a> process before you file.</p></div>

<h2 id="community-property">Married filing separately in community property states</h2>
<p>In the nine community property states, Arizona, California, Idaho, Louisiana, Nevada, New Mexico, Texas, Washington and Wisconsin, income earned during the marriage generally belongs half to each spouse. That changes the math: when you file separately, each spouse typically reports <strong>half of the community income</strong> plus all of their own separate income (for example, income from property owned before the marriage, depending on state law). Alaska allows couples to opt in to community property treatment by agreement.</p>
<p>The practical effect is that filing separately in a community property state often produces results close to filing jointly on income, while still losing the credits listed above. It can also defeat the student loan strategy, since half of the higher earner's wages land on the borrower's return. Each spouse attaches <strong>Form 8958</strong>, <em>Allocation of Tax Amounts Between Certain Individuals in Community Property States</em>, to show how income, deductions and withholding were split. Rules for separated spouses and registered domestic partners differ.</p>

<h2 id="how-to-decide">How to decide: a quick checklist</h2>
<ol>
<li><strong>Run both versions.</strong> Calculate the joint return, then both separate returns, and compare the combined total. Include every credit, not just the bracket tax.</li>
<li><strong>Price in non-tax effects.</strong> Add the annual change in student loan payments, or the value of liability protection to you.</li>
<li><strong>Check withholding.</strong> If you switch to MFS, each spouse's withholding may fall short, since W-4 settings often assume a joint return. The <a href="/calculators/paycheck-calculator/">paycheck calculator</a> and <a href="/calculators/tax-refund-calculator/">tax refund calculator</a> help you see whether you will owe.</li>
<li><strong>Consider head of household.</strong> If you lived apart from your spouse for the last six months of the year and support a qualifying child, you may qualify, which gives a larger standard deduction and wider brackets than MFS.</li>
</ol>
<p>For background on how brackets and deductions combine, see <a href="/blog/how-much-federal-tax-will-i-pay/">how much federal income tax will I pay</a>. If either spouse has freelance income, the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> adds self-employment tax, which is calculated per person no matter how you file.</p>

<?= faq_block([
  ['Is it better to file married filing separately or jointly?', '<p>For most couples, filing jointly produces a lower total tax because the joint brackets let a higher earner use the lower brackets the other spouse leaves empty, and several credits are only available on a joint return. Married filing separately tends to win only in specific cases: large medical expenses for one spouse, income-driven student loan payments, or when one spouse wants to avoid liability for the other\'s tax.</p>'],
  ['What do you lose when married filing separately?', '<p>Separate filers generally cannot claim the earned income tax credit, education credits, the student loan interest deduction, the premium tax credit, or (unless living apart) the child and dependent care credit or adoption credit. They also cannot claim the new tips, overtime and senior deductions, face a $0 to $10,000 IRA phase-out range, a ' . money($saltMfs) . ' SALT cap and a $1,500 capital loss limit.</p>'],
  ['Does married filing separately get the same standard deduction as single?', '<p>Yes. For ' . TAX_YEAR . ' the standard deduction for married filing separately is ' . money($Y['std']['mfs']) . ', the same as for single filers and half of the ' . money($Y['std']['mfj']) . ' joint amount. However, if your spouse itemizes, you must itemize too and your standard deduction is zero.</p>'],
  ['Can I file married filing separately if my spouse files jointly?', '<p>No. A joint return requires both spouses to agree and sign. If either spouse files separately, the other must also file as married filing separately (or as head of household if they qualify as considered unmarried).</p>'],
  ['Does married filing separately help with student loans?', '<p>Often, yes. Income-driven repayment plans base payments on the AGI shown on your tax return, so filing separately can exclude a spouse\'s income and lower the payment. In community property states, though, half of community income may still be counted. Compare the payment savings against the extra tax and confirm the current plan rules with your servicer.</p>'],
  ['Can I change from married filing separately to jointly after filing?', '<p>Yes. You can generally amend separate returns to a joint return within three years of the original due date by filing Form 1040-X. The reverse is not allowed: once the filing deadline passes, you cannot change a joint return into separate returns.</p>'],
]) ?>
<?= post_close($SLUG, 'federal-income-tax', ['how-much-federal-tax-will-i-pay', 'amended-tax-return', 'understanding-your-w-2']) ?>
