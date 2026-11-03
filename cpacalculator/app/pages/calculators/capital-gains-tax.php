<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Capital Gains Tax Calculator $Y — Short & Long-Term Gains | CPA Calculator";
$P['description'] = "Free $Y capital gains tax calculator. Estimate tax on stocks, crypto, real estate or a home sale with the 0%, 15% and 20% rates, NIIT, losses and the home exclusion.";
$P['scripts'] = ['/assets/js/tools/capital-gains-tax.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Long-term rate stacking (PHP mirror of CPA.incomeTax pref portion). */
function cgt_pref_tax(float $base, float $pref, string $s, int $year = TAX_YEAR): float {
  global $TAX;
  $prev = 0; $t = 0; $end = $base + $pref;
  foreach ($TAX['years'][(string) $year]['ltcg'][$s] as [$top, $rate]) {
    $top = $top ?? INF;
    $lo = max($base, $prev); $hi = min($end, $top);
    if ($hi > $lo) $t += ($hi - $lo) * $rate;
    $prev = $top;
  }
  return $t;
}
/* Tax caused by a gain: $ord = other gross ordinary income; gain is either short-term or long-term. Standard deduction. */
function cgt_example(float $ord, float $gain, bool $long, string $s, int $year = TAX_YEAR): array {
  global $TAX;
  $yy = $TAX['years'][(string) $year];
  $std = $yy['std'][$s];
  $ordTaxable = max(0, $ord - $std);
  $left = max(0, $std - $ord);
  $g = max(0, $gain - $left);
  $baseTax = fed_tax($ordTaxable, $s, $year)['tax'];
  if ($long) $fed = fed_tax($ordTaxable, $s, $year)['tax'] + cgt_pref_tax($ordTaxable, $g, $s, $year);
  else $fed = fed_tax($ordTaxable + $g, $s, $year)['tax'];
  $magi = $ord + $gain;
  $niit = max(0, min($gain, $magi - $yy['niit'][$s])) * 0.038;
  return ['std' => $std, 'ordTaxable' => $ordTaxable, 'fedOnGain' => $fed - $baseTax, 'niit' => $niit, 'total' => $fed - $baseTax + $niit];
}
$exLT = cgt_example(70000, 20000, true, 'single');
$exST = cgt_example(70000, 20000, false, 'single');
$exHome = cgt_example(150000, 100000, true, 'mfj');
$exBig = cgt_example(180000, 150000, true, 'single');
$lt = $y['ltcg'];

echo tool_hero('capital-gains-tax', "Capital Gains Tax Calculator $Y",
  "See exactly how much tax you’ll owe when you sell stocks, crypto, a rental property or your home. The calculator stacks your gain on top of your other income, applies the $Y 0%, 15% and 20% long-term rates (or ordinary rates for short-term gains), adds the 3.8% net investment income tax and handles losses, carryovers and the home-sale exclusion.",
  ["$Y IRS 0% / 15% / 20% brackets", 'Short-term vs long-term', 'Home sale exclusion & losses', 'NIIT + optional state tax']);
?>
<section class="tool" aria-label="Capital gains tax calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="cgt-form" novalidate>
        <div class="grid-2">
          <?= year_field() ?>
          <div class="field"><label for="f-asset">What did you sell?</label><select id="f-asset" name="asset">
            <option value="stock">Stocks, ETFs or mutual funds</option>
            <option value="crypto">Cryptocurrency</option>
            <option value="rental">Rental / investment real estate</option>
            <option value="home">My primary home</option>
            <option value="collect">Collectibles (art, coins, gold, bullion)</option>
            <option value="business">Business interest or other property</option>
          </select></div>
        </div>
        <?= status_field() ?>
        <div class="field"><span class="lbl">How long did you own it?</span><div class="seg" role="radiogroup" aria-label="Holding period">
          <label><input type="radio" name="term" value="long" checked><span>More than 1 year (long-term)</span></label>
          <label><input type="radio" name="term" value="short"><span>1 year or less (short-term)</span></label>
        </div></div>
        <fieldset class="fieldset"><legend>The sale</legend>
          <div class="grid-2">
            <?= money_field('sale', 'Sale price', 50000, 'Total proceeds from the sale (Form 1099-B box 1d, or the contract price for real estate).') ?>
            <?= money_field('basis', 'Cost basis', 30000, 'What you paid, including purchase commissions, plus improvements for real estate and reinvested dividends for funds.') ?>
          </div>
          <?= money_field('fees', 'Selling costs & fees', '', 'Commissions, exchange fees, real estate agent commission, title and closing costs paid as the seller.') ?>
          <div id="cgt-rental" hidden>
            <?= money_field('depr', 'Depreciation claimed on the property', '', 'Total depreciation taken (or allowable) while you rented it. That part of the gain — “unrecaptured §1250 gain” — is taxed at up to 25%.') ?>
          </div>
          <div id="cgt-home" hidden>
            <label class="check"><input type="checkbox" name="excl" checked> I owned and lived in it at least 2 of the last 5 years (§121 exclusion)</label>
            <p class="hint" style="margin-top:-4px">Excludes up to $250,000 of gain ($500,000 married filing jointly). Losses on a personal home are not deductible.</p>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Your other income</legend>
          <?= money_field('income', 'Other taxable income for the year', 75000, 'Wages, net self-employment income, interest, retirement distributions — everything except this sale. Enter gross amounts; we subtract the standard deduction.') ?>
          <input type="range" min="0" max="600000" step="1000" data-range-for="income" aria-label="Other income slider">
        </fieldset>
        <details class="more"><summary>More options: itemized deductions, loss carryover, state tax</summary>
          <div class="grid-2">
            <?= money_field('itemized', 'Itemized deductions (if larger)', '', 'Leave blank to use the standard deduction (' . money($y['std']['single']) . ' single / ' . money($y['std']['mfj']) . ' joint in ' . $Y . ').') ?>
            <?= money_field('carry', 'Capital loss carryover from prior years', '', 'Unused capital losses from earlier years (Schedule D line 6/14). They offset this gain first.') ?>
          </div>
          <?= money_field('state', 'State income tax rate (optional)', '', 'Your state’s rate on capital gains. Most states tax them as ordinary income; several have no income tax.', '', '%') ?>
        </details>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="headline">Estimated tax on this sale</div>
          <div class="res-big" data-out="tax">$0</div>
          <div class="res-sub"><span data-out="summary">—</span></div>
          <div class="kpis">
            <div class="kpi"><small data-out="gainLabel">Capital gain</small><b data-out="gain">$0</b></div>
            <div class="kpi"><small>Rate on the gain</small><b data-out="rate">0%</b></div>
            <div class="kpi"><small>Effective tax rate</small><b data-out="eff">0%</b></div>
            <div class="kpi"><small>NIIT (3.8%)</small><b data-out="niit">$0</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Where your sale proceeds go"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <div class="res-label" style="margin-bottom:6px" data-out="stackLabel">Your gain across the long-term brackets</div>
          <ul class="rows" data-stack></ul>
          <p class="note" data-out="compare">—</p>
          <p class="note">Estimate only. Assumes no other capital gains this year and no AMT. Depreciation recapture on equipment (§1245) is ordinary income. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use the capital gains tax calculator</h2>
      <p>Capital gains tax depends on more than the profit itself. The same $20,000 gain can be taxed at 0%, 15%, 22% or more depending on how long you held the asset and how much other income you have. Enter four things and the calculator does the rest:</p>
      <ol>
        <li><strong>What you sold and how long you held it.</strong> Assets owned more than one year qualify for the lower long-term rates. Collectibles, rental property and your home each have special rules the calculator applies automatically.</li>
        <li><strong>Sale price, cost basis and selling costs.</strong> Your gain is the sale price minus what you paid (your basis) minus commissions and closing costs.</li>
        <li><strong>Your other taxable income.</strong> Long-term gains are “stacked” on top of your wages and other income, so your income decides which rate applies.</li>
        <li><strong>Filing status and year.</strong> These set the standard deduction and the 0/15/20% thresholds.</li>
      </ol>
      <p>Open <em>More options</em> to add itemized deductions, a capital loss carryover from earlier years, or a flat state tax rate. Results update as you type and you can share or print them.</p>

      <h2 id="rates">Capital gains tax rates for <?= $Y ?></h2>
      <p>Long-term capital gains and qualified dividends are taxed at 0%, 15% or 20%. The rate depends on your <strong>total taxable income</strong> (including the gain), not just the gain. These are the <?= $Y ?> thresholds published by the IRS:</p>
      <div class="table-wrap"><table>
        <caption class="sr-only"><?= $Y ?> long-term capital gains tax brackets</caption>
        <thead><tr><th>Filing status</th><th class="n">0% rate</th><th class="n">15% rate</th><th class="n">20% rate</th></tr></thead><tbody>
<?php foreach (['single', 'mfj', 'mfs', 'hoh'] as $s): ?>
        <tr><td><?= status_label($s) ?></td><td class="n">Up to <?= money($lt[$s][0][0]) ?></td><td class="n"><?= money($lt[$s][0][0] + 1) ?> – <?= money($lt[$s][1][0]) ?></td><td class="n">Over <?= money($lt[$s][1][0]) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
<?php $prevY = (string) ($Y - 1); if (isset($TAX['years'][$prevY])): $lp = $TAX['years'][$prevY]['ltcg']; ?>
      <p>For comparison, the <?= $prevY ?> thresholds (for returns being filed now) were <?= money($lp['single'][0][0]) ?> / <?= money($lp['single'][1][0]) ?> for single filers and <?= money($lp['mfj'][0][0]) ?> / <?= money($lp['mfj'][1][0]) ?> for married couples filing jointly. Select <?= $prevY ?> in the calculator to use them.</p>
<?php endif; ?>
      <p><strong>Short-term gains</strong> — on assets held one year or less — get no special rate. They are added to your ordinary income and taxed at your regular bracket, from 10% to 37%. See the full bracket tables on our <a href="/calculators/federal-income-tax/#brackets">federal income tax calculator</a>.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Type of gain</th><th>Maximum federal rate</th></tr></thead><tbody>
        <tr><td>Long-term stocks, funds, crypto, land, business assets</td><td>0% / 15% / 20%</td></tr>
        <tr><td>Short-term gains (held 1 year or less)</td><td>Ordinary rates, 10%–37%</td></tr>
        <tr><td>Collectibles (art, coins, precious metals, many gold ETFs)</td><td>Ordinary rates, capped at 28%</td></tr>
        <tr><td>Unrecaptured §1250 gain (depreciation on real estate)</td><td>Ordinary rates, capped at 25%</td></tr>
        <tr><td>Net investment income tax (high earners)</td><td>+3.8% on top</td></tr>
      </tbody></table></div>

      <h2 id="formula">How capital gains tax is calculated</h2>
      <div class="formula">Gain = sale price − cost basis − selling costs<br>Taxable gain = gain − home exclusion − loss carryover<br>Ordinary taxable income = other income − deduction<br>Tax = gain taxed in the 0/15/20% layers above ordinary income<br>NIIT = 3.8% × lesser of (gain, MAGI − threshold)</div>
      <p>The key idea is <strong>stacking</strong>. Your ordinary income fills the brackets first. Your long-term gain sits on top of it, and each slice of the gain is taxed at the rate for the layer it falls in. If your ordinary taxable income is already above the 0% threshold, every dollar of gain is taxed at 15%; if it’s below, part of the gain may be tax-free.</p>
      <p>The 3.8% <strong>net investment income tax (NIIT)</strong> applies when modified AGI exceeds <?= money($y['niit']['single']) ?> (single or head of household), <?= money($y['niit']['mfj']) ?> (married filing jointly) or <?= money($y['niit']['mfs']) ?> (married filing separately). These thresholds are fixed by law and are not adjusted for inflation. Gain excluded under the home-sale rule is not subject to NIIT.</p>

      <h2 id="example">Worked example: long-term vs short-term</h2>
      <p>A single filer earns $70,000 in wages in <?= $Y ?> and sells shares for a $20,000 profit.</p>
      <ul>
        <li>Ordinary taxable income: $70,000 − <?= money($exLT['std']) ?> standard deduction = <strong><?= money($exLT['ordTaxable']) ?></strong>. That is already above the <?= money($lt['single'][0][0]) ?> top of the 0% bracket.</li>
        <li><strong>Held more than a year:</strong> the whole $20,000 is taxed at 15% = <strong><?= money($exLT['fedOnGain']) ?></strong>.</li>
        <li><strong>Held a year or less:</strong> the gain is ordinary income in the 22% bracket = <strong><?= money($exST['fedOnGain']) ?></strong>.</li>
        <li>Waiting past the one-year mark saves <strong><?= money($exST['fedOnGain'] - $exLT['fedOnGain']) ?></strong> in federal tax.</li>
      </ul>
      <p>A higher earner sees NIIT kick in. A single filer with $180,000 of other income and a $150,000 long-term gain owes about <?= money($exBig['total'] - $exBig['niit']) ?> of regular capital gains tax plus <?= money($exBig['niit']) ?> of NIIT, for a total of <strong><?= money($exBig['total']) ?></strong> (<?= number_format($exBig['total'] / 150000 * 100, 1) ?>% of the gain).</p>

      <h2 id="home-sale">Selling your home: the $250,000 / $500,000 exclusion</h2>
      <p>Under Section 121 you can exclude up to <strong>$250,000 of gain ($500,000 if married filing jointly)</strong> on the sale of your main home if you owned it and used it as your residence for at least two of the five years before the sale, and haven’t used the exclusion in the past two years. Only the gain above the exclusion is taxable — as a long-term gain if you owned the home for more than a year.</p>
      <p>Example: a married couple bought their home for $300,000 (including improvements) and sells it for $900,000. The $600,000 gain is reduced by the $500,000 exclusion, leaving $100,000 taxable. With $150,000 of other income, that $100,000 is taxed at 15% — about <strong><?= money($exHome['fedOnGain']) ?></strong> — and their MAGI of $250,000 doesn’t exceed the NIIT threshold, so NIIT is <?= money($exHome['niit']) ?>.</p>
      <div class="callout warn"><?= icon('shield') ?><p><strong>Watch out:</strong> a loss on your personal home is not deductible. Depreciation you claimed for a home office or rental use after May 6, 1997 can’t be excluded and is taxed at up to 25%. Partial exclusions are available if you moved early for work, health or unforeseen circumstances — check IRS Publication 523.</p></div>

      <h2 id="losses">Capital losses and the $3,000 limit</h2>
      <p>If you sell at a loss, losses first offset your capital gains for the year. If losses exceed gains, you can deduct up to <strong>$3,000 of net capital loss ($1,500 if married filing separately)</strong> against ordinary income such as wages. Anything left over carries forward indefinitely to future years, keeping its short-term or long-term character. Enter a negative result (basis higher than sale price) and the calculator shows the deduction, the tax it saves at your bracket and the amount that carries forward. Enter prior-year carryovers under <em>More options</em>.</p>
      <p>Selling losing positions to offset gains is called <strong>tax-loss harvesting</strong>. Beware the wash-sale rule: if you buy the same or a substantially identical security within 30 days before or after the sale, the loss is disallowed for now and added to the basis of the new shares.</p>

      <h2 id="crypto-real-estate">Crypto, rental property and collectibles</h2>
      <ul>
        <li><strong>Cryptocurrency</strong> is property. Selling, swapping one coin for another, or spending crypto are all taxable events, taxed under the same short- and long-term rules as stocks. Brokers report sales on Form 1099-DA starting with 2025 transactions.</li>
        <li><strong>Rental real estate:</strong> the gain attributable to depreciation you claimed is “unrecaptured §1250 gain,” taxed at ordinary rates up to 25%. The rest is a regular long-term gain. Choose “Rental / investment real estate” and enter the depreciation taken. A 1031 exchange can defer the entire gain.</li>
        <li><strong>Collectibles</strong> — art, antiques, coins, stamps, gold and silver bullion and many precious-metal ETFs — are taxed at ordinary rates but no more than 28% when held over a year.</li>
      </ul>

      <h2 id="reduce">How to reduce capital gains tax</h2>
      <ol>
        <li><strong>Hold for more than a year</strong> so gains qualify for the 0/15/20% rates.</li>
        <li><strong>Use the 0% bracket.</strong> In a low-income year — between jobs, early retirement, a sabbatical — you may be able to realize gains tax-free up to the 0% threshold.</li>
        <li><strong>Harvest losses</strong> to offset gains and up to $3,000 of ordinary income.</li>
        <li><strong>Lower your taxable income</strong> with pre-tax 401(k) and HSA contributions, which can pull more of your gain into a lower rate.</li>
        <li><strong>Donate appreciated stock</strong> held over a year to charity: you avoid the gain and may deduct the full market value if you itemize.</li>
        <li><strong>Spread large sales</strong> over two tax years, or use an installment sale for real estate or a business.</li>
        <li><strong>Hold until death:</strong> heirs generally receive a stepped-up basis, wiping out the built-in gain.</li>
      </ol>
      <p>Self-employed and selling business assets too? Run your full return through the <a href="/calculators/federal-income-tax/">federal income tax calculator</a>, and check whether you need to make a <a href="/calculators/quarterly-estimated-tax/">quarterly estimated payment</a> for the quarter of the sale — large gains are a common cause of underpayment penalties. Our <a href="/blog/quarterly-taxes-101-guide/">quarterly taxes guide</a> explains the safe-harbor rules.</p>

<?= faq_block([
  ['How much capital gains tax will I pay?', "<p>It depends on how long you held the asset and your total taxable income. Long-term gains are taxed at 0%, 15% or 20%; short-term gains at your ordinary rate of 10% to 37%. For example, a single filer earning \$70,000 who sells stock for a \$20,000 long-term gain owes about " . money($exLT['fedOnGain']) . " in $Y — versus " . money($exST['fedOnGain']) . " if the shares were held a year or less.</p>"],
  ["What are the $Y capital gains tax brackets?", "<p>For $Y, the 0% rate applies to taxable income up to " . money($lt['single'][0][0]) . " (single), " . money($lt['mfj'][0][0]) . " (married filing jointly) or " . money($lt['hoh'][0][0]) . " (head of household). The 15% rate applies up to " . money($lt['single'][1][0]) . ", " . money($lt['mfj'][1][0]) . " and " . money($lt['hoh'][1][0]) . " respectively, and 20% above that.</p>"],
  ['Do I pay capital gains tax if I reinvest the money?', '<p>Yes, in most cases. Selling an investment is a taxable event even if you immediately buy something else. The exceptions are trades inside tax-advantaged accounts (401(k), IRA, HSA), a 1031 like-kind exchange of real estate held for investment, and investing gains in a qualified opportunity fund.</p>'],
  ['How do I avoid capital gains tax when selling my house?', '<p>If you owned and lived in the home for at least two of the last five years, you can exclude up to $250,000 of gain ($500,000 married filing jointly). Keep records of improvements — they increase your basis and reduce the gain. Only gain above the exclusion is taxed.</p>'],
  ['Is the 3.8% net investment income tax included?', "<p>Yes. The calculator adds NIIT when your modified AGI exceeds " . money($y['niit']['single']) . " (single), " . money($y['niit']['mfj']) . " (joint) or " . money($y['niit']['mfs']) . " (separate). It applies to the smaller of your net investment income or the amount your MAGI exceeds the threshold.</p>"],
  ['How much capital loss can I deduct?', '<p>Capital losses offset capital gains without limit. If losses exceed gains, up to $3,000 per year ($1,500 married filing separately) can reduce your ordinary income, and the rest carries forward to future years until used.</p>'],
  ['Are capital gains added to my income and pushed into a higher bracket?', '<p>Capital gains count toward your taxable income and can push part of the gain into a higher capital gains rate, but long-term gains never raise the tax rate on your wages. Short-term gains are taxed exactly like wages. Gains can, however, raise your AGI and affect income-based items such as NIIT, credits and Medicare premiums.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('capital-gains-tax', ['federal-income-tax', 'quarterly-estimated-tax', 'tax-refund-calculator', 'depreciation-calculator', '1099-tax-calculator', 'paycheck-calculator']) ?></div>
