<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$pct = fn(float $x, int $dp = 1): string => number_format($x * 100, $dp) . '%';
/* Sample Schedule C: freelance designer, single, cash method, simplified home office. */
$miles = 4000; $sqft = 200;
$receipts = 92000; $returns = 0; $cogs = 0; $other_inc = 0;
$exp = [
  ['8', 'Advertising', 1200],
  ['9', 'Car and truck (' . number_format($miles) . ' business miles × ' . number_format($Y['mileage'] * 100, 1) . '¢)', $miles * $Y['mileage']],
  ['10', 'Commissions and fees (marketplace and payment fees)', 1350],
  ['11', 'Contract labor (subcontracted illustrator)', 6000],
  ['13', 'Depreciation and Section 179 (computer and monitor)', 3000],
  ['15', 'Insurance (professional liability)', 1100],
  ['17', 'Legal and professional services', 900],
  ['18', 'Office expense', 650],
  ['22', 'Supplies', 600],
  ['23', 'Taxes and licenses', 250],
  ['24a', 'Travel (conference)', 1800],
  ['24b', 'Deductible meals (50% of $1,000)', 500],
  ['25', 'Utilities (business share of phone and internet)', 960],
  ['27b', 'Other expenses from Part V (software subscriptions)', 2400],
];
$total_exp = array_sum(array_column($exp, 2));
$gross_income = $receipts - $returns - $cogs + $other_inc;
$tentative = $gross_income - $total_exp;
$home = $sqft * $Y['homeOfficeSimplifiedRate'];
$net = $tentative - $home;
$se_base = $net * 0.9235;
$se = min($se_base, $Y['ssWageBase']) * 0.124 + $se_base * 0.029;
$pre = max(0, $net - $se / 2 - $Y['std']['single']);
$qbi = 0.20 * min($net - $se / 2, $pre);
$inc = fed_tax(max(0, $pre - $qbi), 'single')['tax'];
/* Part III example. */
$p3 = ['35' => 4000, '36' => 21000, '37' => 0, '38' => 1500, '39' => 500];
$p3_40 = array_sum($p3); $p3_41 = 5200; $p3_42 = $p3_40 - $p3_41;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">The Schedule C tax form is where sole proprietors, single-member LLC owners and most freelancers report business income and expenses. Its bottom line, net profit, flows into your Form 1040 for income tax and into Schedule SE for self-employment tax, so every dollar of expense you document correctly lowers two taxes at once. This guide walks through Schedule C line by line, Parts I through V, with a sample return computed using <?= TAX_YEAR ?> figures.</p>

<div class="callout"><?= icon('receipt') ?><p><strong>In short:</strong> report gross receipts on line 1, subtract returns and cost of goods sold, list expenses on lines 8–27, subtract the home office on line 30, and carry net profit from line 31 to Schedule 1 and Schedule SE. Estimate the tax on the result with the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a>.</p></div>

<h2 id="who-files">Who files the Schedule C tax form?</h2>
<p>You file Schedule C (Form 1040), "Profit or Loss From Business," if you operate a business as a sole proprietor, which includes:</p>
<ul>
<li>Freelancers, independent contractors and gig workers paid on a 1099-NEC or 1099-K (see <a href="/blog/1099-vs-w2/">1099 vs W-2</a> if you are unsure of your status)</li>
<li>Single-member LLCs that have not elected to be taxed as a corporation</li>
<li>Statutory employees, whose W-2 has Box 13 checked</li>
<li>Spouses running a qualified joint venture, who each file their own Schedule C</li>
</ul>
<p>Each separate business gets its own Schedule C. Partnerships and multi-member LLCs file Form 1065 instead, and S corporations file Form 1120-S, with owners receiving a K-1; see our <a href="/blog/k1-tax-form/">K-1 tax form guide</a>. Your activity must be engaged in for profit; hobby income is reported differently and hobby expenses are not deductible.</p>

<h2 id="header">The top section: lines A through J</h2>
<div class="table-wrap"><table>
<thead><tr><th>Line</th><th>What to enter</th></tr></thead>
<tbody>
<tr><td><b>A</b></td><td>Principal business or profession, such as "graphic design" or "online retail"</td></tr>
<tr><td><b>B</b></td><td>Six-digit principal business code from the list in the Schedule C instructions</td></tr>
<tr><td><b>C, D, E</b></td><td>Business name (if any), employer ID number (EIN) if you have one, and business address</td></tr>
<tr><td><b>F</b></td><td>Accounting method: cash, accrual or other</td></tr>
<tr><td><b>G</b></td><td>Whether you materially participated; if not, passive activity loss limits may apply</td></tr>
<tr><td><b>H</b></td><td>Check if you started or acquired the business this year</td></tr>
<tr><td><b>I, J</b></td><td>Whether you made payments requiring Form 1099 (for example, <?= money(2000) ?> or more to a contractor in <?= TAX_YEAR ?>) and whether you filed them</td></tr>
</tbody></table></div>
<p><strong>Accounting method.</strong> Most small service businesses use the <strong>cash method</strong>: income counts when received and expenses when paid. The <strong>accrual method</strong> records income when earned and expenses when incurred. Businesses with average annual gross receipts under the inflation-adjusted small business threshold can generally use cash even with inventory. Once chosen, changing methods usually requires IRS consent on Form 3115.</p>

<h2 id="part-1">Part I: Income (lines 1–7)</h2>
<ul>
<li><strong>Line 1, gross receipts or sales:</strong> everything the business took in, whether or not a 1099 was issued. If you received a 1099-K, report its gross amount here and handle fees and refunds below; see our <a href="/blog/1099-k/">Form 1099-K guide</a>.</li>
<li><strong>Line 2, returns and allowances:</strong> refunds and discounts given after the sale.</li>
<li><strong>Line 3:</strong> line 1 minus line 2.</li>
<li><strong>Line 4, cost of goods sold:</strong> from Part III, line 42. Service businesses usually leave it blank.</li>
<li><strong>Line 5, gross profit:</strong> line 3 minus line 4.</li>
<li><strong>Line 6, other income:</strong> business income not from sales, such as interest on business accounts receivable, recovered bad debts, or a fuel tax credit or refund.</li>
<li><strong>Line 7, gross income:</strong> line 5 plus line 6.</li>
</ul>

<h2 id="part-2">Part II: Expenses (lines 8–27)</h2>
<p>Expenses must be ordinary and necessary for your business. Personal costs are not deductible, and mixed-use items (phone, internet, car) are deductible only for the business share.</p>
<div class="table-wrap"><table>
<thead><tr><th>Line</th><th>Expense</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>8</td><td>Advertising</td><td>Ads, website hosting for marketing, promotional materials</td></tr>
<tr><td>9</td><td>Car and truck expenses</td><td>Standard mileage (<?= number_format($Y['mileage'] * 100, 1) ?>¢ per mile for <?= TAX_YEAR ?>) or actual costs; complete Part IV</td></tr>
<tr><td>10</td><td>Commissions and fees</td><td>Marketplace, payment processing and referral fees</td></tr>
<tr><td>11</td><td>Contract labor</td><td>Payments to independent contractors (not employees)</td></tr>
<tr><td>12</td><td>Depletion</td><td>Natural resources such as timber or minerals</td></tr>
<tr><td>13</td><td>Depreciation and Section 179</td><td>From Form 4562; 100% bonus depreciation is available for qualifying property acquired after January 19, 2025</td></tr>
<tr><td>14</td><td>Employee benefit programs</td><td>For employees only, not the owner</td></tr>
<tr><td>15</td><td>Insurance (other than health)</td><td>Liability, business property, professional insurance</td></tr>
<tr><td>16a / 16b</td><td>Interest</td><td>Mortgage interest on business property paid to banks; other business interest</td></tr>
<tr><td>17</td><td>Legal and professional services</td><td>Attorneys, accountants, tax preparation for the business</td></tr>
<tr><td>18</td><td>Office expense</td><td>Postage, printer ink, small office items</td></tr>
<tr><td>19</td><td>Pension and profit-sharing plans</td><td>Contributions for employees; your own SEP or Solo 401(k) goes on Schedule 1</td></tr>
<tr><td>20a / 20b</td><td>Rent or lease</td><td>Vehicles, machinery and equipment; other business property such as an office</td></tr>
<tr><td>21</td><td>Repairs and maintenance</td><td>Keeping property in working order (not improvements)</td></tr>
<tr><td>22</td><td>Supplies</td><td>Materials consumed in the business, not included in COGS</td></tr>
<tr><td>23</td><td>Taxes and licenses</td><td>Business licenses, employer payroll taxes, business property taxes (not federal income tax)</td></tr>
<tr><td>24a / 24b</td><td>Travel / deductible meals</td><td>Overnight business travel; business meals are generally 50% deductible</td></tr>
<tr><td>25</td><td>Utilities</td><td>For business premises; home utilities go through the home office deduction</td></tr>
<tr><td>26</td><td>Wages</td><td>Pay to employees, less employment credits; never your own draws</td></tr>
<tr><td>27a / 27b</td><td>Energy efficient buildings deduction / other expenses</td><td>27a from Form 7205; 27b is the total from Part V</td></tr>
</tbody></table></div>
<p><strong>Line 28</strong> totals the expenses, and <strong>line 29</strong> is tentative profit (line 7 minus line 28).</p>

<h2 id="home-office">Line 30: business use of your home</h2>
<p>If you use part of your home regularly and exclusively for business, deduct it on line 30. With the <strong>simplified method</strong>, enter your home's total square footage and the business area, and deduct $<?= $Y['homeOfficeSimplifiedRate'] ?> per square foot up to 300 square feet (<?= money(300 * $Y['homeOfficeSimplifiedRate']) ?> maximum). With the <strong>regular method</strong>, you allocate actual mortgage interest or rent, utilities, insurance, repairs and depreciation on Form 8829. The <a href="/calculators/home-office-deduction/">home office deduction calculator</a> shows which method is bigger.</p>

<h2 id="line-31">Line 31: net profit or loss</h2>
<p>Line 31 is line 29 minus line 30. A profit goes to <strong>Schedule 1, line 3</strong> (and from there to Form 1040) and to <strong>Schedule SE, line 2</strong>, where self-employment tax is figured if net earnings are $400 or more. The <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> shows that piece on its own.</p>
<p>If line 31 is a loss, lines 32a and 32b ask whether all of your investment is at risk. Check <strong>32a</strong> if all of it is at risk (the normal case for a sole proprietor funding the business with their own money) and deduct the loss. Check <strong>32b</strong> if some investment is not at risk, such as nonrecourse financing, and complete Form 6198, which may limit the loss. Large business losses can also be limited by the excess business loss rules on Form 461.</p>

<h2 id="part-3">Part III: Cost of goods sold (lines 33–42)</h2>
<p>Businesses that make or sell products complete Part III. Line 33 asks how you value closing inventory (cost, lower of cost or market, or other), and line 34 asks whether you changed how you count inventory. Then:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Part III cost of goods sold example</caption>
<thead><tr><th>Line</th><th>Item</th><th class="n">Example</th></tr></thead>
<tbody>
<tr><td>35</td><td>Inventory at beginning of year</td><td class="n"><?= money($p3['35']) ?></td></tr>
<tr><td>36</td><td>Purchases, less items withdrawn for personal use</td><td class="n"><?= money($p3['36']) ?></td></tr>
<tr><td>37</td><td>Cost of labor (not paid to yourself)</td><td class="n"><?= money($p3['37']) ?></td></tr>
<tr><td>38</td><td>Materials and supplies</td><td class="n"><?= money($p3['38']) ?></td></tr>
<tr><td>39</td><td>Other costs (freight-in, packaging)</td><td class="n"><?= money($p3['39']) ?></td></tr>
<tr><td>40</td><td>Add lines 35 through 39</td><td class="n"><?= money($p3_40) ?></td></tr>
<tr><td>41</td><td>Inventory at end of year</td><td class="n">−<?= money($p3_41) ?></td></tr>
<tr><td><b>42</b></td><td><b>Cost of goods sold</b> (to line 4)</td><td class="n"><b><?= money($p3_42) ?></b></td></tr>
</tbody></table></div>
<p>Goods you bought but did not sell by year-end stay in inventory and are deducted in the year they sell. The <a href="/calculators/profit-margin/">profit margin calculator</a> helps you track gross margin per product.</p>

<h2 id="part-4">Part IV: Vehicle information (lines 43–47)</h2>
<p>If you claim car or truck expenses on line 9 and are not required to file Form 4562 for the vehicle, complete Part IV: the date the vehicle was placed in service (line 43), business, commuting and other miles (line 44), whether the vehicle was available for personal use (lines 45–46), and whether you have evidence, and if so written evidence, to support the deduction (lines 47a–47b). Commuting between home and a regular work location is not deductible. A contemporaneous mileage log is the best evidence; the <a href="/calculators/mileage-deduction/">mileage deduction calculator</a> compares the standard rate with actual costs.</p>

<h2 id="part-5">Part V: Other expenses (line 48)</h2>
<p>List any expense that does not fit lines 8–26, with a description and amount: software subscriptions, bank fees, professional dues, education that maintains your skills, shipping and postage, and similar costs. The total on line 48 goes to line 27b. Use clear descriptions; vague labels like "miscellaneous" invite questions.</p>

<h2 id="sample">Sample Schedule C tax form, filled out</h2>
<p>A single freelance designer using the cash method had <?= money($receipts) ?> of gross receipts in <?= TAX_YEAR ?>, no inventory, and a <?= $sqft ?>-square-foot home office using the simplified method:</p>
<div class="table-wrap"><table>
<caption class="sr-only">Sample Schedule C for a freelance designer, <?= TAX_YEAR ?></caption>
<thead><tr><th>Line</th><th>Description</th><th class="n">Amount</th></tr></thead>
<tbody>
<tr><td>1</td><td>Gross receipts</td><td class="n"><?= money($receipts) ?></td></tr>
<tr><td>7</td><td><b>Gross income</b></td><td class="n"><b><?= money($gross_income) ?></b></td></tr>
<?php foreach ($exp as [$ln, $d, $a]): ?>
<tr><td><?= $ln ?></td><td><?= e($d) ?></td><td class="n"><?= money($a) ?></td></tr>
<?php endforeach; ?>
<tr><td>28</td><td><b>Total expenses</b></td><td class="n"><b><?= money($total_exp) ?></b></td></tr>
<tr><td>29</td><td>Tentative profit</td><td class="n"><?= money($tentative) ?></td></tr>
<tr><td>30</td><td>Home office, simplified (<?= $sqft ?> sq ft × $<?= $Y['homeOfficeSimplifiedRate'] ?>)</td><td class="n"><?= money($home) ?></td></tr>
<tr><td>31</td><td><b>Net profit</b></td><td class="n"><b><?= money($net) ?></b></td></tr>
</tbody></table></div>
<p>From that net profit, Schedule SE produces about <?= money($se) ?> of self-employment tax. After deducting half of it, the <?= money($Y['std']['single']) ?> standard deduction and a <?= money($qbi) ?> QBI deduction, federal income tax is about <?= money($inc) ?>, for a total federal bill near <?= money($se + $inc) ?>, or <?= $pct(($se + $inc) / $net) ?> of net profit. Because none of it is withheld, this designer should be making <a href="/blog/quarterly-taxes-101-guide/">quarterly estimated payments</a>; the <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> splits it into installments.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>Keep records, not just totals.</strong> The IRS can ask you to support any line on Schedule C. Keep receipts, invoices, bank statements and your mileage log for at least three years after filing, longer for assets you are depreciating.</p></div>

<h2 id="mistakes">Common Schedule C mistakes</h2>
<ul>
<li>Reporting only income that appeared on 1099s instead of all receipts</li>
<li>Deducting owner's draws as wages, or health insurance and retirement contributions on Schedule C instead of Schedule 1</li>
<li>Claiming 100% of meals, or deducting commuting miles</li>
<li>Expensing inventory you have not sold</li>
<li>Combining two unrelated businesses on one Schedule C</li>
</ul>
<p>When profit grows, compare the cost of an S corporation election with the <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a>. For the first steps after receiving a 1099, see <a href="/blog/got-a-1099-exactly-what-to-do-next/">Got a 1099? Here is exactly what to do next</a>.</p>

<?= faq_block([
  ['What is a Schedule C tax form used for?', '<p>The Schedule C tax form reports profit or loss from a business you run as a sole proprietor or single-member LLC. It lists gross receipts, cost of goods sold and business expenses, and its net profit flows to Form 1040 and to Schedule SE for self-employment tax.</p>'],
  ['Who needs to file Schedule C?', '<p>Anyone with self-employment income from a business operated as a sole proprietorship, including freelancers, contractors, gig workers, single-member LLC owners and statutory employees. There is no minimum income to file it, and self-employment tax applies once net earnings reach $400.</p>'],
  ['Do I need to file Schedule C if I have no 1099?', '<p>Yes. Schedule C reports all business income, whether or not you received a 1099-NEC or 1099-K. The forms are information returns for the IRS; your obligation to report comes from earning the income.</p>'],
  ['Can I file Schedule C with a loss?', '<p>Yes. A loss on line 31 can offset other income such as wages, subject to the at-risk rules (Form 6198), passive activity rules if you did not materially participate, and the excess business loss limit. Repeated losses may lead the IRS to question whether the activity is a business or a hobby.</p>'],
  ['Where does health insurance go on Schedule C?', '<p>It does not. Self-employed health insurance premiums for yourself and your family are deducted on Schedule 1 as an adjustment to income, not on Schedule C. The same is true for your own SEP or Solo 401(k) contributions.</p>'],
  ['What is the difference between Schedule C and Schedule SE?', '<p>Schedule C calculates business net profit. Schedule SE uses that profit to calculate self-employment tax (Social Security and Medicare), at 15.3% on 92.35% of net earnings up to the wage base. Most self-employed people file both.</p>'],
]) ?>
<?= post_close($SLUG, '1099-tax-calculator', ['got-a-1099-exactly-what-to-do-next', '1099-k', 'quarterly-taxes-101-guide']) ?>
