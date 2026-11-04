<?php defined('CPA') or exit;
$Y = $TAX['years'][(string) TAX_YEAR];
$pct = fn(float $x, int $dp = 1): string => number_format($x * 100, $dp) . '%';
/* Long-term capital gains tax stacked on top of ordinary taxable income, using the year's 0/15/20% brackets. */
$ltcg = function (float $ord, float $gain, string $st) use ($Y): float {
  $prev = 0; $tax = 0;
  foreach ($Y['ltcg'][$st] as [$top, $rate]) {
    $top = $top ?? INF;
    $lo = max($prev, $ord); $hi = min($top, $ord + $gain);
    if ($hi > $lo) $tax += ($hi - $lo) * $rate;
    $prev = $top;
  }
  return $tax;
};
/* Example A: single seller. */
$buy = 300000; $close_buy = 5000; $impr = 60000; $sale = 780000; $sell_cost = 45000;
$realized = $sale - $sell_cost;
$basis = $buy + $close_buy + $impr;
$gain = $realized - $basis;
$excl = min($gain, 250000);
$taxable_gain = $gain - $excl;
$wages = 95000;
$ord = max(0, $wages - $Y['std']['single']);
$cg_tax = $ltcg($ord, $taxable_gain, 'single');
$niit = 0.038 * min($taxable_gain, max(0, $wages + $taxable_gain - $Y['niit']['single']));
/* Example B: married couple, same numbers. */
$excl_mfj = min($gain, 500000);
/* Example C: partial exclusion after 15 months, job relocation. */
$months = 15; $gain_c = 180000;
$max_c = 250000 * $months / 24;
$taxable_c = max(0, $gain_c - $max_c);
/* Example D: depreciation recapture on a home office / rental period. */
$dep = 30000;
echo post_open($SLUG, '2026-11-04'); ?>
<p class="lead">Most homeowners never pay capital gains tax on home sale profits, because federal law lets you exclude up to $250,000 of profit ($500,000 for married couples filing jointly) when you sell your main home. But the exclusion has conditions, the profit is figured from your adjusted basis rather than what you paid, and gains above the limit are taxed at <?= TAX_YEAR ?> capital gains rates. This guide explains the rules for selling a house, how to calculate your gain, and what happens if you do not qualify for the full exclusion, with worked examples.</p>

<div class="callout"><?= icon('home') ?><p><strong>Quick answer:</strong> if you owned and lived in the home as your main residence for at least two of the five years before the sale, and have not used the exclusion in the past two years, you can exclude up to <?= money(250000) ?> of gain (<?= money(500000) ?> married filing jointly). Gain above that is usually taxed at 0%, 15% or 20%. Estimate yours with the <a href="/calculators/capital-gains-tax/">capital gains tax calculator</a>.</p></div>

<h2 id="how-it-works">How capital gains tax on home sale profits works</h2>
<p>When you sell a house for more than your adjusted basis, the profit is a capital gain. If you owned the home more than one year it is a long-term gain, taxed at the preferential rates below; one year or less, it is short-term and taxed like wages. For a main home, Section 121 of the tax code then lets you exclude a large part or all of that gain.</p>
<div class="formula">Amount realized = sale price − selling costs (commissions, title, transfer taxes, legal fees)<br>Adjusted basis = purchase price + buying costs + capital improvements − depreciation and certain credits<br>Gain = amount realized − adjusted basis<br>Taxable gain = gain − Section 121 exclusion</div>

<h2 id="exclusion">The $250,000 / $500,000 home sale exclusion</h2>
<p>To claim the full exclusion, you must pass three tests:</p>
<ol>
<li><strong>Ownership test:</strong> you owned the home for at least 24 months during the 5 years ending on the date of sale.</li>
<li><strong>Use test:</strong> you lived in it as your main home for at least 24 months in that same 5-year window. The months do not need to be consecutive, and the ownership and use periods do not need to overlap. Short absences such as vacations count as time living there.</li>
<li><strong>Look-back test:</strong> you did not exclude gain from another home sale in the 2 years before this sale.</li>
</ol>
<p>Married couples filing jointly get up to <?= money(500000) ?> if <em>either</em> spouse meets the ownership test, <em>both</em> meet the use test, and <em>neither</em> used the exclusion in the prior two years. If only one spouse qualifies, the couple can exclude up to <?= money(250000) ?>. A surviving spouse can still claim up to <?= money(500000) ?> if the home is sold within two years of the spouse's death and the other requirements were met just before the death.</p>
<p>The exclusion amounts are set in the law and are not adjusted for inflation. Proposals to raise or eliminate them have been introduced in Congress, but the One Big Beautiful Bill Act did not change Section 121, so the $250,000 and $500,000 limits apply for <?= TAX_YEAR ?>. Members of the military, Foreign Service and intelligence community on qualified extended duty can elect to suspend the 5-year window for up to 10 years.</p>

<h2 id="basis">Calculating your gain: basis and improvements</h2>
<p>Your gain is often much smaller than "sale price minus purchase price," because both sides get adjusted.</p>
<div class="table-wrap"><table>
<thead><tr><th>Adds to basis (lowers gain)</th><th>Does not add to basis</th></tr></thead>
<tbody>
<tr><td>Purchase price</td><td>Repairs and maintenance (painting, fixing leaks)</td></tr>
<tr><td>Settlement costs at purchase: title insurance, recording fees, transfer taxes, legal fees, survey</td><td>Mortgage interest, property taxes, homeowners insurance</td></tr>
<tr><td>Capital improvements: additions, new roof, HVAC, kitchen or bath remodel, landscaping, new windows</td><td>Points deducted as mortgage interest</td></tr>
<tr><td>Special assessments for local improvements (sidewalks, sewers)</td><td>Improvements later removed or replaced (the old roof's cost)</td></tr>
</tbody></table></div>
<p>Basis is reduced by any depreciation you claimed (for a home office or rental use), casualty losses deducted and certain energy credits. Keep closing statements and receipts for improvements for as long as you own the home, plus at least three years after you file the return reporting the sale. Inherited homes generally get a basis equal to fair market value at the date of death, which often wipes out most of the gain; gifted homes carry over the giver's basis.</p>

<h2 id="example">Worked example: capital gains tax on home sale gains above the exclusion</h2>
<p>A single filer bought a home for <?= money($buy) ?>, paid <?= money($close_buy) ?> in buying costs, and spent <?= money($impr) ?> on improvements over the years. They sell for <?= money($sale) ?> and pay <?= money($sell_cost) ?> in commissions and closing costs. They meet the 2-out-of-5-year tests and earn <?= money($wages) ?> in wages in <?= TAX_YEAR ?>.</p>
<div class="table-wrap"><table>
<caption class="sr-only">Home sale gain and tax worked example, <?= TAX_YEAR ?></caption>
<tbody>
<tr><td>Sale price</td><td class="n"><?= money($sale) ?></td></tr>
<tr><td>Selling costs</td><td class="n">−<?= money($sell_cost) ?></td></tr>
<tr><td><b>Amount realized</b></td><td class="n"><b><?= money($realized) ?></b></td></tr>
<tr><td>Adjusted basis (<?= money($buy) ?> + <?= money($close_buy) ?> + <?= money($impr) ?>)</td><td class="n">−<?= money($basis) ?></td></tr>
<tr><td><b>Gain</b></td><td class="n"><b><?= money($gain) ?></b></td></tr>
<tr><td>Section 121 exclusion (single)</td><td class="n">−<?= money($excl) ?></td></tr>
<tr><td><b>Taxable long-term gain</b></td><td class="n"><b><?= money($taxable_gain) ?></b></td></tr>
<tr><td>Ordinary taxable income (wages − <?= money($Y['std']['single']) ?> standard deduction)</td><td class="n"><?= money($ord) ?></td></tr>
<tr><td>Capital gains tax (gain stacked on top of ordinary income)</td><td class="n"><?= money($cg_tax) ?></td></tr>
<tr><td>Net investment income tax (3.8% on MAGI above <?= money($Y['niit']['single']) ?>)</td><td class="n"><?= money($niit) ?></td></tr>
<tr><td><b>Total federal tax on the sale</b></td><td class="n"><b><?= money($cg_tax + $niit) ?></b></td></tr>
</tbody></table></div>
<p>The gain sits on top of the seller's <?= money($ord) ?> of ordinary taxable income. Because that is already above the <?= money($Y['ltcg']['single'][0][0]) ?> top of the 0% bracket, the whole <?= money($taxable_gain) ?> falls in the 15% bracket. The 3.8% net investment income tax applies only to the <?= money(max(0, $wages + $taxable_gain - $Y['niit']['single'])) ?> by which modified AGI exceeds <?= money($Y['niit']['single']) ?>. Excluded gain does not count toward the NIIT. The capital gain also raises AGI, which can affect other items such as credits and Medicare premiums.</p>
<p><strong>Same sale, married filing jointly:</strong> if both spouses lived in the home for two of the last five years, the exclusion is <?= money(500000) ?>, which covers the entire <?= money($gain) ?> gain. Taxable gain: <?= money($gain - $excl_mfj) ?>.</p>

<h2 id="rates">2026 capital gains tax rates</h2>
<p>Taxable gain from a home held more than a year uses the long-term rates. The thresholds apply to total taxable income, including the gain:</p>
<div class="table-wrap"><table>
<thead><tr><th>Rate</th><th class="n">Single</th><th class="n">Married filing jointly</th><th class="n">Head of household</th></tr></thead>
<tbody>
<?php $labels = ['0%', '15%', '20%']; for ($i = 0; $i < 3; $i++): ?>
<tr><td><b><?= $labels[$i] ?></b></td><?php foreach (['single', 'mfj', 'hoh'] as $st): $b = $Y['ltcg'][$st]; $from = $i ? $b[$i - 1][0] : 0; $to = $b[$i][0]; ?><td class="n"><?= $to === null ? 'Over ' . money($from) : ($i ? money($from + 1) . ' – ' : 'Up to ') . money($to) ?></td><?php endforeach; ?></tr>
<?php endfor; ?>
</tbody></table></div>
<p>High earners may also owe the 3.8% net investment income tax on the taxable portion of the gain. Many states tax capital gains as ordinary income, so check your state's rules too.</p>

<h2 id="partial">Partial exclusion if you sell early</h2>
<p>If you fail the 2-year tests or used the exclusion within the past two years, you may still get a reduced exclusion if the main reason for the sale was:</p>
<ul>
<li><strong>A change in place of employment:</strong> a safe harbor applies if your new job location is at least 50 miles farther from the home than your old one (or 50 miles away if you had no job before).</li>
<li><strong>Health:</strong> moving to obtain or provide care for a disease, illness or injury, for yourself or a family member, often documented by a doctor's recommendation.</li>
<li><strong>Unforeseen circumstances:</strong> events such as death, divorce or legal separation, multiple births from one pregnancy, losing a job and qualifying for unemployment, a casualty or disaster damaging the home, or condemnation.</li>
</ul>
<p>The reduced limit is the full exclusion multiplied by the qualifying months (the shorter of your ownership, use, or time since the last exclusion) divided by 24.</p>
<p><strong>Example:</strong> a single owner lives in a home for <?= $months ?> months, then takes a job 300 miles away and sells at a <?= money($gain_c) ?> gain. Maximum exclusion = <?= money(250000) ?> × <?= $months ?>/24 = <?= money($max_c) ?>. Taxable gain = <?= money($taxable_c) ?>. Note that the fraction reduces the <em>dollar limit</em>, not the gain itself, so a smaller gain can still be fully excluded.</p>

<h2 id="depreciation">Home office, rental use and depreciation recapture</h2>
<p>Depreciation claimed after May 6, 1997 for business or rental use of the home cannot be excluded. That amount, called unrecaptured Section 1250 gain, is taxed at your ordinary rate up to a maximum of 25%. For example, if you deducted <?= money($dep) ?> of depreciation on a home office or while renting out the house, up to <?= money($dep) ?> of the gain is taxable at a rate of up to 25% (at most <?= money($dep * 0.25) ?>), even if the rest is fully excluded.</p>
<ul>
<li><strong>Home office inside the home</strong> (a spare bedroom): no need to split the gain, but the depreciation is taxable. The <a href="/calculators/home-office-deduction/">home office deduction calculator</a> compares the simplified method, which involves no depreciation, with the regular method.</li>
<li><strong>Separate structure</strong> (a detached studio or rental unit): you allocate the gain between the residence and the business part; only the residential part can be excluded.</li>
<li><strong>Rental before it was your home:</strong> for periods after 2008 when the property was not your main home (nonqualified use), a proportional share of the gain is not excludable. Time after you move out, within the 5-year window, generally does not count as nonqualified use.</li>
</ul>
<p>Depreciation schedules are covered in the <a href="/calculators/depreciation-calculator/">depreciation calculator</a>.</p>
<div class="callout warn"><?= icon('shield') ?><p><strong>A loss on a personal home is not deductible.</strong> If you sell your main home for less than your adjusted basis, you cannot deduct the loss. Losses on rental or business property follow different rules.</p></div>

<h2 id="reporting">Reporting the sale and Form 1099-S</h2>
<p>The closing agent usually files <strong>Form 1099-S</strong> to report the gross proceeds. They can skip it if you certify in writing that the full gain is excludable, which generally requires a sale price of <?= money(250000) ?> or less (<?= money(500000) ?> for married sellers) and that you meet the exclusion rules.</p>
<ul>
<li><strong>Entire gain excluded and no 1099-S:</strong> you generally do not report the sale at all.</li>
<li><strong>You received a 1099-S, or part of the gain is taxable:</strong> report the sale on Form 8949 and Schedule D, entering the exclusion as an adjustment (code H) so that only the taxable part is taxed.</li>
<li><strong>Depreciation was claimed:</strong> the business part may also go on Form 4797.</li>
</ul>
<p>If a large gain will be due, consider making an estimated tax payment for the quarter of the sale to avoid an underpayment penalty; see <a href="/blog/quarterly-taxes-101-guide/">Quarterly Taxes 101</a>. For how a gain interacts with your other income, see <a href="/blog/how-much-federal-tax-will-i-pay/">how much federal income tax will I pay</a>, and for filing-status trade-offs, <a href="/blog/married-filing-separately/">married filing separately vs jointly</a>.</p>

<?= faq_block([
  ['How do I avoid capital gains tax on home sale profits?', '<p>Live in the home as your main residence for at least two of the five years before selling and do not use the exclusion more than once every two years. That lets you exclude up to $250,000 of gain ($500,000 married filing jointly). Keeping records of improvements and selling costs also lowers the gain subject to capital gains tax on home sale proceeds.</p>'],
  ['Do I have to pay capital gains tax if I buy another house?', '<p>No rule requires reinvesting the proceeds, and buying another home does not defer tax. That rollover rule was repealed in 1997 and replaced by the $250,000/$500,000 exclusion. (A 1031 exchange applies only to investment or business property, not a main home.)</p>'],
  ['What is the capital gains tax rate on a home sale in ' . TAX_YEAR . '?', '<p>Taxable gain on a home owned more than one year is taxed at 0%, 15% or 20%, depending on taxable income. For ' . TAX_YEAR . ', the 0% rate applies up to ' . money($Y['ltcg']['single'][0][0]) . ' of taxable income for single filers (' . money($Y['ltcg']['mfj'][0][0]) . ' joint) and 20% starts above ' . money($Y['ltcg']['single'][1][0]) . ' (' . money($Y['ltcg']['mfj'][1][0]) . ' joint). The 3.8% NIIT may also apply.</p>'],
  ['What if I lived in my house less than 2 years?', '<p>You may qualify for a partial exclusion if you sold because of a job change at least 50 miles farther away, health reasons or unforeseen circumstances. The limit is prorated by the months you qualified divided by 24. Otherwise the gain is taxable, at short-term rates if you owned the home a year or less.</p>'],
  ['Do I have to report the sale of my home to the IRS?', '<p>If the entire gain is excludable and you did not receive Form 1099-S, you generally do not need to report it. If you received a 1099-S or any gain is taxable, report the sale on Form 8949 and Schedule D.</p>'],
  ['At what age do you not pay capital gains on a home sale?', '<p>There is no age-based exemption today. The over-55 one-time exclusion was replaced in 1997 by the $250,000/$500,000 exclusion, which is available at any age, as often as every two years.</p>'],
]) ?>
<?= post_close($SLUG, 'capital-gains-tax', ['how-much-federal-tax-will-i-pay', 'married-filing-separately', 'quarterly-taxes-101-guide']) ?>
