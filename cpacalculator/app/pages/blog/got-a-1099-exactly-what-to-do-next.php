<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$due = $Y['quarterlyDue'];
/* Worked example: $40,000 of 1099-NEC income, $6,000 expenses, single, no other income. */
$ex_gross = 40000; $ex_exp = 6000;
$ex_net = $ex_gross - $ex_exp;
$ex_se_base = $ex_net * 0.9235;
$ex_se = min($ex_se_base, $Y['ssWageBase']) * 0.124 + $ex_se_base * 0.029;
$ex_agi = $ex_net - $ex_se / 2;
$ex_pre_qbi = max(0, $ex_agi - $Y['std']['single']);
$ex_qbi = min($ex_net * 0.20, $ex_pre_qbi * 0.20);
$ex_taxable = max(0, $ex_pre_qbi - $ex_qbi);
$ex_inc = fed_tax($ex_taxable, 'single')['tax'];
$ex_total = $ex_se + $ex_inc;
echo post_open($SLUG, '2026-11-03'); ?>
<p class="lead">A 1099 means someone paid you without withholding any tax. That is not a problem, and it is not a sign of trouble with the IRS. It simply means the job of setting tax aside, and later reporting the income, now belongs to you. This guide walks through exactly what to do with a 1099, in order: identify the form, check it, work out what you owe, pay it, and file it correctly. If you are on the other side and need to send 1099s, there is a section for payers at the end.</p>

<div class="callout"><?= icon('spark') ?><p><strong>The short version:</strong> confirm the form is right, add up <em>all</em> your self-employment income (not only what is on 1099s), subtract business expenses, and set aside money for both income tax and self-employment tax. Pay quarterly if you will owe $1,000 or more, then report everything on Schedule C and Schedule SE with your Form 1040.</p></div>

<h2 id="which-1099">Step 1: Identify which 1099 you received</h2>
<p>"1099" is a family of information returns. Each one reports a different kind of payment, and where it goes on your return depends on which form you have. The payer sends a copy to the IRS too, so the IRS already knows about this income.</p>
<div class="table-wrap"><table>
<thead><tr><th>Form</th><th>What it reports</th><th>Where it usually goes</th></tr></thead>
<tbody>
<tr><td><b>1099-NEC</b></td><td>Pay for services from a business that treated you as a non-employee (freelance, contract, consulting work)</td><td>Schedule C (plus Schedule SE)</td></tr>
<tr><td><b>1099-K</b></td><td>Payments processed through card networks and third-party apps or marketplaces (PayPal, Venmo for business, Etsy, eBay, rideshare apps)</td><td>Schedule C for business sales; Form 8949 / Schedule D for personal items sold at a gain</td></tr>
<tr><td><b>1099-MISC</b></td><td>Rents, royalties, prizes and awards, certain other income</td><td>Schedule E (rents, royalties) or Schedule 1 "other income"; Schedule C if it is part of a business</td></tr>
<tr><td><b>1099-INT</b></td><td>Interest from banks, brokerages, Treasury bonds</td><td>Form 1040 (Schedule B if over $1,500)</td></tr>
<tr><td><b>1099-DIV</b></td><td>Dividends and capital gain distributions</td><td>Form 1040 (Schedule B if over $1,500); qualified dividends get capital gains rates</td></tr>
<tr><td><b>1099-B</b></td><td>Sales of stocks, funds and crypto through a broker</td><td>Form 8949 and Schedule D</td></tr>
<tr><td><b>1099-R / 1099-G</b></td><td>Retirement distributions / unemployment and state refunds</td><td>Form 1040 and Schedule 1</td></tr>
</tbody></table></div>
<p>Most people searching for 1099 tax help have a <strong>1099-NEC</strong> or a <strong>1099-K</strong>, which is self-employment income. The rest of this guide focuses on those, because they carry self-employment tax on top of regular income tax. Interest and dividends on a 1099-INT or 1099-DIV are simply added to your other income and do not trigger self-employment tax.</p>

<h3 id="thresholds">The 2026 reporting thresholds changed</h3>
<p>The One Big Beautiful Bill Act (OBBBA), signed in July 2025, changed when payers must send these forms:</p>
<ul>
<li><strong>1099-NEC and 1099-MISC:</strong> the long-standing $600 threshold rises to <strong>$2,000</strong> for payments made after December 31, 2025, with inflation adjustments starting after 2026. So 2025 payments (forms you received in early 2026) still used $600, while 2026 payments (forms arriving in early 2027) use $2,000.</li>
<li><strong>1099-K:</strong> the law restored the original threshold of <strong>more than $20,000 and more than 200 transactions</strong> for payment apps and online marketplaces, replacing the planned drop to $600. Some states require their own 1099-K at much lower amounts, so you can still receive one below the federal threshold.</li>
</ul>
<div class="callout warn"><?= icon('shield') ?><p><strong>No form does not mean no tax.</strong> The thresholds only decide whether the payer has to send a form. Every dollar of business income is taxable whether you receive a 1099, receive one with the wrong amount, or receive nothing at all. Keep your own income records from invoices, bank deposits and platform reports.</p></div>

<h2 id="check">Step 2: Check the 1099 for errors</h2>
<p>Before you use the numbers, compare the form with your own records:</p>
<ol>
<li><strong>Your name and taxpayer ID</strong> (SSN or EIN). A wrong number can cause IRS matching notices later.</li>
<li><strong>The amount.</strong> Does it match what you actually received from this payer during the calendar year? Payments sent in late December but received in January can create timing differences.</li>
<li><strong>The box.</strong> Contract pay belongs in Box 1 of a 1099-NEC. If it shows up on a 1099-MISC as "other income," the tax treatment and the IRS matching can differ.</li>
<li><strong>Duplicates.</strong> If a client paid you through PayPal, you could get a 1099-NEC from the client and a 1099-K from PayPal for the same money. You report the income once, but keep records showing the overlap.</li>
<li><strong>Fees on a 1099-K.</strong> A 1099-K shows <em>gross</em> payments before platform fees, refunds and shipping. You report the gross figure and deduct the fees and refunds as expenses, so that the totals tie to the form.</li>
</ol>
<h3 id="corrections">How to get a 1099 corrected</h3>
<p>If something is wrong, contact the payer and ask for a corrected form (the payer checks the "CORRECTED" box and files it with the IRS). If the payer will not fix it before you file, report the amount you can prove, keep the documentation, and be ready to explain the difference if the IRS sends a CP2000 matching notice. If you never got a form you expected, you do not need to wait for it: report the income from your records.</p>
<p>If you believe you were really an employee, not a contractor, you can ask the IRS for a determination on <strong>Form SS-8</strong> and report your share of Social Security and Medicare on <strong>Form 8919</strong> instead of paying the full self-employment tax.</p>

<h2 id="what-you-owe">Step 3: Work out how much tax you owe on 1099 income</h2>
<p>Here is how to pay taxes on 1099 income, conceptually: you owe two separate federal taxes on your <em>net profit</em> (income minus business expenses).</p>
<ul>
<li><strong>Self-employment tax: 15.3%</strong> on 92.35% of net profit, made up of 12.4% Social Security (on earnings up to the <?= TAX_YEAR ?> wage base of <?= money($Y['ssWageBase']) ?>) and 2.9% Medicare (no cap). An extra 0.9% Medicare tax applies above <?= money($Y['addlMedicare']['single']) ?> single or <?= money($Y['addlMedicare']['mfj']) ?> married filing jointly. It applies once net self-employment earnings reach $400.</li>
<li><strong>Income tax</strong> at your normal bracket rates, after the standard deduction (<?= money($Y['std']['single']) ?> single, <?= money($Y['std']['mfj']) ?> married filing jointly for <?= TAX_YEAR ?>), the deduction for half of your self-employment tax and, for most sole proprietors, the 20% qualified business income (QBI) deduction, which OBBBA made permanent.</li>
</ul>
<div class="formula">Net profit = 1099 income − business expenses<br>SE tax = net profit × 92.35% × 15.3%<br>Taxable income = net profit − ½ SE tax − standard deduction − QBI deduction<br>Total federal tax = SE tax + income tax on taxable income</div>
<h3 id="example">Worked example</h3>
<p>Say you are single, earned <?= money($ex_gross) ?> on 1099-NECs in <?= TAX_YEAR ?>, had <?= money($ex_exp) ?> of business expenses and no other income.</p>
<div class="table-wrap"><table><tbody>
<tr><td>Net profit (<?= money($ex_gross) ?> − <?= money($ex_exp) ?>)</td><td class="n"><?= money($ex_net) ?></td></tr>
<tr><td>Self-employment tax (<?= money($ex_net) ?> × 92.35% × 15.3%)</td><td class="n"><?= money($ex_se) ?></td></tr>
<tr><td>Minus half of SE tax and the <?= money($Y['std']['single']) ?> standard deduction</td><td class="n"><?= money($ex_pre_qbi) ?></td></tr>
<tr><td>Minus QBI deduction (20%, limited to 20% of taxable income)</td><td class="n">−<?= money($ex_qbi) ?></td></tr>
<tr><td>Taxable income</td><td class="n"><?= money($ex_taxable) ?></td></tr>
<tr><td>Federal income tax</td><td class="n"><?= money($ex_inc) ?></td></tr>
<tr><td><b>Total federal tax</b> (<?= number_format($ex_total / $ex_gross * 100, 1) ?>% of gross receipts)</td><td class="n"><b><?= money($ex_total) ?></b></td></tr>
</tbody></table></div>
<p>Notice that self-employment tax is the larger bill here. That surprises many first-time freelancers, and it is why a "10% bracket" does not mean setting aside 10%. Plug your own numbers into the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> to see income tax, SE tax and a suggested quarterly payment together, or use the <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> for the Schedule SE piece alone. State income tax, if your state has one, comes on top.</p>
<div class="callout"><?= icon('wallet') ?><p><strong>A practical savings rule:</strong> many freelancers move 25–30% of every payment into a separate savings account the day it arrives. Your actual rate depends on your income, deductions and state, so use the calculator once and set your own percentage.</p></div>

<h2 id="expenses">Step 4: Track write-offs and records</h2>
<p>Every legitimate business expense lowers <em>both</em> taxes, which is why good records are the best 1099 tax advice there is. Common deductions include:</p>
<ul>
<li>Software, subscriptions, web hosting and professional tools</li>
<li>Equipment and computers (often fully deductible in year one under Section 179 or 100% bonus depreciation, which OBBBA restored for property acquired after January 19, 2025; see the <a href="/calculators/depreciation-calculator/">depreciation calculator</a>)</li>
<li>Business mileage at <?= number_format($Y['mileage'] * 100, 1) ?>¢ per mile for <?= TAX_YEAR ?>, or actual vehicle costs (<a href="/calculators/mileage-deduction/">mileage deduction calculator</a>)</li>
<li>A home office used regularly and exclusively for work (<a href="/calculators/home-office-deduction/">home office deduction calculator</a>)</li>
<li>The business share of phone and internet</li>
<li>Platform, payment processing and marketplace fees (important when your 1099-K shows gross amounts)</li>
<li>Professional fees, licenses, insurance, education related to your current work</li>
<li>Self-employed health insurance premiums and retirement contributions (SEP IRA or Solo 401(k)), taken as adjustments on Schedule 1 rather than on Schedule C</li>
</ul>
<p>Keep receipts, invoices, bank and card statements and a mileage log. A separate business bank account makes all of this much easier and is the single habit most tax preparers recommend first.</p>

<h2 id="quarterly">Step 5: Pay estimated taxes during the year</h2>
<p>Because nobody withholds tax from 1099 income, the IRS expects you to pay as you go through quarterly estimated taxes if you will owe <strong>$1,000 or more</strong> when you file. The <?= TAX_YEAR ?> due dates are:</p>
<div class="table-wrap"><table>
<thead><tr><th>Income earned</th><th>Payment due</th></tr></thead>
<tbody>
<tr><td>January 1 – March 31</td><td><?= e($due[0]) ?></td></tr>
<tr><td>April 1 – May 31</td><td><?= e($due[1]) ?></td></tr>
<tr><td>June 1 – August 31</td><td><?= e($due[2]) ?></td></tr>
<tr><td>September 1 – December 31</td><td><?= e($due[3]) ?></td></tr>
</tbody></table></div>
<p>You avoid the underpayment penalty if your payments plus withholding cover at least 90% of this year's tax, or 100% of last year's tax (110% if last year's adjusted gross income was over $150,000). Pay online with IRS Direct Pay, EFTPS or your IRS Online Account. The <a href="/blog/quarterly-taxes-101-guide/">Quarterly Taxes 101 guide</a> covers the details, and if this is your first year with 1099 income, read <a href="/blog/do-i-have-to-pay-quarterly-taxes-my-first-year/">do I have to pay quarterly taxes my first year?</a> The <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> works out each payment.</p>
<p><strong>Also have a W-2 job?</strong> You can raise the withholding at that job (line 4(c) of a new Form W-4) instead of making estimated payments. Withholding counts as if it were paid evenly through the year, even if you increase it in the fall.</p>

<h2 id="file">Step 6: File your return with the right forms</h2>
<p>At tax time, 1099-NEC and business 1099-K income flows through these forms:</p>
<ol>
<li><strong>Schedule C</strong> (Profit or Loss From Business): report gross receipts from all 1099s <em>plus</em> any unreported income, then list expenses by category. The result is your net profit.</li>
<li><strong>Schedule SE</strong>: computes self-employment tax on that profit.</li>
<li><strong>Schedule 1</strong>: carries Schedule C profit to your income and takes the deduction for half of SE tax, plus any SEP or Solo 401(k) and self-employed health insurance deductions.</li>
<li><strong>Schedule 2</strong>: carries the SE tax to your Form 1040.</li>
<li><strong>Form 8995</strong> (or 8995-A at higher incomes): the QBI deduction.</li>
<li><strong>Form 1040</strong>: where it all lands, along with your estimated payments, which you list on the return so the IRS credits them.</li>
</ol>
<p>Received a 1099-K for personal items sold at a loss, like used furniture or concert tickets sold below cost? That is not business income. Report it on Form 8949 so the gross proceeds are offset by your cost and the IRS's matching system sees why no tax is due.</p>
<p>If your net profit is high and steady, it can be worth comparing a sole proprietorship with an S corporation election. The <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a> shows when a reasonable salary plus distributions starts to beat Schedule C.</p>

<h2 id="payers">How to prepare a 1099 (if you're the payer)</h2>
<p>If your business pays contractors, you are the one who issues 1099s. The basic process:</p>
<ol>
<li><strong>Collect a Form W-9</strong> from every contractor before the first payment. It gives you their legal name, tax classification and taxpayer ID. Payments to most corporations are exempt (attorneys' fees are an exception).</li>
<li><strong>Track payments by calendar year.</strong> For payments made in 2026, a 1099-NEC is required once you pay a contractor <strong>$2,000 or more</strong> for services (it was $600 for 2025 payments). Payments you made by credit card or through PayPal or a similar app are reported by the processor on a 1099-K, so leave those out of your 1099-NEC.</li>
<li><strong>Fill in the form.</strong> Payer and recipient details, and the total in Box 1 (nonemployee compensation). Report any backup withholding in Box 4.</li>
<li><strong>Furnish and file by January 31.</strong> 1099-NEC copies go to both the contractor and the IRS by January 31 of the following year (the next business day if it falls on a weekend). 1099-MISC is due to recipients by January 31 and to the IRS by the end of February on paper or March 31 if e-filed.</li>
<li><strong>E-file if you have 10 or more.</strong> If you file 10 or more information returns of any type in total, you must file electronically, for example through the IRS's free Information Returns Intake System (IRIS).</li>
</ol>
<p>If you discover a mistake, file a corrected form with the "CORRECTED" box checked and send the recipient a copy. Late or incorrect forms can carry per-form penalties that rise the longer they go unfixed.</p>

<h2 id="checklist">1099 checklist</h2>
<ul>
<li>Identify every 1099 type you received and where it goes on your return</li>
<li>Check names, ID numbers and amounts; request corrections early</li>
<li>Add income that was not reported on any form</li>
<li>Total your business expenses with receipts and a mileage log</li>
<li>Estimate your tax with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a></li>
<li>Make quarterly payments, or raise W-2 withholding</li>
<li>File Schedule C, Schedule SE and Form 1040 by April 15</li>
</ul>
<p>If you also have a regular job, our guide to <a href="/blog/understanding-your-w-2/">understanding your W-2</a> explains how that side of your return fits in.</p>

<?= faq_block([
  ['What do I do with a 1099 form?', '<p>Check it for errors, then use it to report the income on your tax return. Freelance and contract income from a 1099-NEC or business 1099-K goes on Schedule C, with self-employment tax on Schedule SE. Interest and dividends (1099-INT, 1099-DIV) go directly on Form 1040. You do not attach the 1099 to your return; keep it with your records.</p>'],
  ['How much should I set aside for taxes on 1099 income?', '<p>Many freelancers set aside 25–30% of each payment, but the right amount depends on your income, expenses, filing status and state. Self-employment tax alone is about 14.1% of net profit (15.3% × 92.35%) before income tax. Use the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> to find your own rate.</p>'],
  ['Do I have to pay taxes if I made less than $600 (or $2,000) on a 1099?', '<p>Yes. The $600 and new $2,000 amounts only decide whether the payer must send you a form. All business income is taxable, and self-employment tax applies once your net self-employment earnings reach $400 for the year.</p>'],
  ['What is the new 1099 threshold for 2026?', '<p>For payments made after December 31, 2025, businesses must issue a 1099-NEC or 1099-MISC once payments to a person reach $2,000, up from $600. The 1099-K threshold for payment apps and marketplaces is more than $20,000 and more than 200 transactions. Some states have lower 1099-K thresholds.</p>'],
  ['What if I never received a 1099 I was expecting?', '<p>Report the income anyway using your own records, such as invoices and bank deposits. You do not need to wait for the form, and the IRS does not require you to have it to file. If the payer later files a 1099 with a different amount, keep documentation to support the figure you reported.</p>'],
  ['Can I deduct expenses if I only have 1099 income?', '<p>Yes. Ordinary and necessary business expenses are deducted on Schedule C, which reduces both income tax and self-employment tax. You can also take the standard deduction on your personal return; business expenses are not itemized deductions.</p>'],
]) ?>
<?= post_close($SLUG, '1099-tax-calculator', ['quarterly-taxes-101-guide', 'do-i-have-to-pay-quarterly-taxes-my-first-year', '1099-taxes-for-physicians']) ?>
