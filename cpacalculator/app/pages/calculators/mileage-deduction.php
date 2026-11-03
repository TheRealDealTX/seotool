<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Mileage Deduction Calculator $Y — IRS Rate " . ($y['mileage'] * 100) . "¢ per Mile | CPA Calculator";
$P['description'] = "Free $Y mileage deduction and reimbursement calculator. Use the IRS " . ($y['mileage'] * 100) . "¢ business rate, log trips, compare actual car costs and estimate tax savings.";
$P['scripts'] = ['/assets/js/tools/mileage-deduction.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Non-business rates (not in tax.json). Medical/moving per IRS annual notice; charity fixed by statute. */
$OTHER = ['2026' => ['medical' => 0.205, 'charity' => 0.14], '2025' => ['medical' => 0.21, 'charity' => 0.14]];
$rate = $y['mileage'];
$rateC = rtrim(rtrim(number_format($rate * 100, 1), '0'), '.');
$prevY = (string) ($Y - 1);

/* Worked example (mirrors the JS): 12,000 business miles of 18,000 total, $300 parking, 22% bracket, self-employed. */
$exMiles = 12000; $exTotal = 18000; $exPark = 300;
$exCosts = ['Gas' => 3000, 'Insurance' => 1800, 'Repairs & maintenance' => 900, 'Depreciation' => 4000, 'Registration & fees' => 300];
$exStd = $exMiles * $rate + $exPark;
$exCostSum = array_sum($exCosts);
$exAct = $exCostSum * $exMiles / $exTotal + $exPark;
$exSE = $exStd * 0.9235 * 0.153;
$exFed = ($exStd - $exSE / 2) * 0.22;

echo tool_hero('mileage-deduction', "Mileage Deduction Calculator $Y",
  "Work out your mileage deduction or reimbursement at the $Y IRS standard rate of {$rateC}¢ per business mile. Log individual trips, add parking and tolls, compare the standard rate with your actual car expenses, and estimate how much the deduction saves you in income and self-employment tax.",
  ["$Y IRS rate: {$rateC}¢ / mile", 'Trip log', 'Standard vs actual expenses', 'Tax savings estimate']);
?>
<section class="tool" aria-label="Mileage deduction calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="mileage-form" novalidate>
        <div class="field"><span class="lbl">Purpose of the driving</span><div class="seg" role="radiogroup" aria-label="Purpose of the driving">
          <label><input type="radio" name="purpose" value="business" checked><span>Business</span></label>
          <label><input type="radio" name="purpose" value="medical"><span>Medical</span></label>
          <label><input type="radio" name="purpose" value="charity"><span>Charity</span></label>
          <label><input type="radio" name="purpose" value="moving"><span>Military move</span></label>
        </div></div>
        <div class="grid-2">
          <?= year_field() ?>
          <div class="field"><label for="f-rate">Rate per mile <span class="tip" tabindex="0" data-tip="Filled in with the IRS standard rate for the year and purpose. Edit it to use a different employer reimbursement rate.">?</span></label>
            <div class="inp suf" data-suf="¢"><input id="f-rate" name="rate" inputmode="decimal" autocomplete="off" data-money value="<?= $rate * 100 ?>"></div>
            <span class="hint" data-out="rateHint"><?= $Y ?> business rate: <?= $rateC ?>¢ per mile</span></div>
        </div>
        <fieldset class="fieldset"><legend>Miles driven</legend>
          <div class="grid-2">
            <?= money_field('miles', 'Miles for this purpose (year total)', 10000, 'Total qualifying miles from your log. Commuting between home and a regular workplace does not count.', '', '') ?>
            <?= money_field('parking', 'Parking fees & tolls', '', 'Business (or medical/charity) parking and tolls are deductible on top of the mileage rate.') ?>
          </div>
          <details class="more"><summary>Trip log — add individual trips</summary>
            <div data-trips></div>
            <button type="button" class="btn-ghost" data-add-trip>+ Add a trip</button>
            <p class="hint">Trips are added to the miles above. Tick “round trip” to double the one-way distance.</p>
          </details>
        </fieldset>
        <div data-actual-wrap>
          <details class="more" open><summary>Compare actual car expenses (business)</summary>
            <?= money_field('totalMiles', 'Total miles driven this year (all purposes)', 15000, 'Odometer reading at year end minus start of year. Sets your business-use percentage.', '', '') ?>
            <div class="grid-3">
              <?= money_field('gas', 'Gas & oil', 2400) ?>
              <?= money_field('insurance', 'Insurance', 1500) ?>
              <?= money_field('repairs', 'Repairs, tires, maintenance', 600) ?>
            </div>
            <div class="grid-3">
              <?= money_field('depr', 'Depreciation or lease payments', 3500, 'Annual depreciation (subject to luxury-auto limits) or lease payments. Use our depreciation calculator for the figure.') ?>
              <?= money_field('reg', 'Registration & fees', 300) ?>
              <?= money_field('otherCar', 'Other (loan interest, washes)', '', 'Self-employed people can include the business share of car loan interest. Employees cannot.') ?>
            </div>
          </details>
        </div>
        <fieldset class="fieldset"><legend>Tax savings estimate</legend>
          <div class="grid-2">
            <div class="field"><label for="f-marginal">Federal tax bracket</label><select id="f-marginal" name="marginal">
              <?php foreach ([10, 12, 22, 24, 32, 35, 37] as $m) echo '<option value="' . $m . '"' . ($m === 22 ? ' selected' : '') . '>' . $m . '%</option>'; ?>
            </select><span class="hint">Not sure? Check the <a href="/calculators/federal-income-tax/">federal tax calculator</a>.</span></div>
            <?= money_field('state', 'State income tax rate', '', 'Optional flat state rate.', '', '%') ?>
          </div>
          <label class="check"><input type="checkbox" name="se" checked> I’m self-employed (deduction also cuts 15.3% self-employment tax)</label>
          <?= money_field('reimb', 'Reimbursement received from employer (optional)', '', 'Under an accountable plan, reimbursement up to the IRS rate is tax-free. Any excess is taxable wages.') ?>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="dedLabel">Your mileage deduction</div>
          <div class="res-big" data-out="ded">$0</div>
          <div class="res-sub"><span data-out="summary">—</span></div>
          <div class="kpis">
            <div class="kpi"><small>Standard mileage</small><b data-out="kStd">$0</b></div>
            <div class="kpi"><small>Actual expenses</small><b data-out="kAct">—</b></div>
            <div class="kpi"><small>Est. tax savings</small><b data-out="kSave">$0</b></div>
            <div class="kpi"><small>Business use</small><b data-out="kPct">—</b></div>
          </div>
          <div class="res-label">Standard mileage rate</div>
          <div class="meter" aria-hidden="true"><span data-meter-std style="background:#10b981"></span></div>
          <div class="res-label">Actual expense method</div>
          <div class="meter" aria-hidden="true"><span data-meter-act style="background:#0e7490"></span></div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="How much of the deduction comes back as tax savings"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note" data-out="note">—</p>
          <p class="note">Tax savings are an estimate at the bracket you choose; SE tax savings assume earnings below the Social Security wage base. <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="rates"><?= $Y ?> IRS mileage rates</h2>
      <p>The IRS sets standard mileage rates each year. For <?= $Y ?> the business rate is <strong><?= $rateC ?> cents per mile</strong><?php if (isset($TAX['years'][$prevY])): ?>, up from <?= $TAX['years'][$prevY]['mileage'] * 100 ?>¢ in <?= $prevY ?><?php endif; ?>. The rate is meant to cover the full cost of operating a car — gas, maintenance, insurance, registration and depreciation — so you don’t deduct those separately when you use it.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Purpose</th><th class="n"><?= $Y ?></th><?php if (isset($OTHER[$prevY])): ?><th class="n"><?= $prevY ?></th><?php endif; ?></tr></thead><tbody>
        <tr><td>Business</td><td class="n"><?= $rateC ?>¢</td><?php if (isset($OTHER[$prevY])): ?><td class="n"><?= $TAX['years'][$prevY]['mileage'] * 100 ?>¢</td><?php endif; ?></tr>
        <tr><td>Medical &amp; military moving</td><td class="n"><?= $OTHER[(string) $Y]['medical'] * 100 ?>¢</td><?php if (isset($OTHER[$prevY])): ?><td class="n"><?= $OTHER[$prevY]['medical'] * 100 ?>¢</td><?php endif; ?></tr>
        <tr><td>Charitable service</td><td class="n">14¢</td><?php if (isset($OTHER[$prevY])): ?><td class="n">14¢</td><?php endif; ?></tr>
      </tbody></table></div>
      <p>The charitable rate is fixed by law and doesn’t change with inflation. Rates are announced in an IRS notice each December — check <a href="https://www.irs.gov/tax-professionals/standard-mileage-rates" rel="noopener">irs.gov</a> for the official figures. The calculator fills in the rate automatically when you change the year or purpose, and you can type a different rate (for example, your employer’s reimbursement rate).</p>

      <h2 id="how-to-use">How to use the mileage deduction calculator</h2>
      <ol>
        <li><strong>Choose the purpose</strong> — business, medical, charity or a military move — and the tax year.</li>
        <li><strong>Enter your miles.</strong> Type the year’s total from your mileage log, or open the trip log and add trips one at a time (tick “round trip” to double the distance).</li>
        <li><strong>Add parking and tolls</strong>, which are deductible on top of the standard rate.</li>
        <li><strong>Compare actual expenses</strong> (business only): enter total miles driven and your car costs to see whether the actual expense method gives a bigger deduction.</li>
        <li><strong>Estimate your tax savings</strong> by choosing your federal bracket and whether you’re self-employed.</li>
      </ol>

      <h2 id="formula">Mileage deduction formula</h2>
      <div class="formula">Standard method = business miles × <?= $rateC ?>¢ + parking &amp; tolls<br>Business use % = business miles ÷ total miles<br>Actual method = total car costs × business use % + parking &amp; tolls<br>Tax savings ≈ deduction × (bracket + state rate) + SE tax saved</div>
      <p>For self-employed drivers the deduction lowers both income tax and self-employment tax, so every business mile is worth more than the deduction rate times your bracket. At a 22% bracket, a self-employed driver saves roughly 33–35 cents in total tax for every dollar of mileage deduction.</p>

      <h2 id="example">Worked example: standard rate vs actual expenses</h2>
      <p>A self-employed consultant drives 18,000 miles in <?= $Y ?>, of which <?= number_format($exMiles) ?> are business miles (a <?= round($exMiles / $exTotal * 100, 1) ?>% business-use percentage), and pays $<?= $exPark ?> in business parking.</p>
      <div class="table-wrap"><table><tbody>
        <tr><td>Standard method: <?= number_format($exMiles) ?> × <?= $rateC ?>¢ + $<?= $exPark ?> parking</td><td class="n"><strong><?= money($exStd) ?></strong></td></tr>
<?php foreach ($exCosts as $k => $c): ?>
        <tr><td>&nbsp;&nbsp;<?= $k ?></td><td class="n"><?= money($c) ?></td></tr>
<?php endforeach; ?>
        <tr><td>Actual method: <?= money($exCostSum) ?> × <?= round($exMiles / $exTotal * 100, 1) ?>% + $<?= $exPark ?> parking</td><td class="n"><strong><?= money($exAct) ?></strong></td></tr>
      </tbody></table></div>
      <p>The standard rate wins by <?= money($exStd - $exAct) ?>. In the 22% bracket, the <?= money($exStd) ?> deduction saves about <?= money($exSE) ?> of self-employment tax and <?= money($exFed) ?> of federal income tax — roughly <strong><?= money($exSE + $exFed) ?></strong> in total. Actual expenses tend to win for expensive vehicles with high depreciation, poor fuel economy or high insurance, or when business use is very high.</p>

      <h2 id="who-can-deduct">Who can deduct mileage?</h2>
      <ul>
        <li><strong>Self-employed people, freelancers and gig workers</strong> deduct business mileage on Schedule C (or Schedule F for farmers). This is the most common use — rideshare and delivery drivers, real estate agents, contractors and consultants. See the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> to see the effect on your total tax.</li>
        <li><strong>Employees</strong> generally can’t deduct unreimbursed mileage on their federal return. The One Big Beautiful Bill Act made the suspension of miscellaneous itemized deductions permanent. Exceptions include Armed Forces reservists, qualified performing artists and fee-basis government officials. Ask your employer to reimburse you instead.</li>
        <li><strong>Medical mileage</strong> for trips to doctors, hospitals and pharmacies counts toward the medical expense deduction, which you can claim only if you itemize and only above 7.5% of AGI.</li>
        <li><strong>Charitable mileage</strong> driving for a qualified charity is deductible at 14¢ per mile if you itemize.</li>
        <li><strong>Moving mileage</strong> is deductible only for active-duty military members moving under orders.</li>
      </ul>

      <h2 id="reimbursement">Mileage reimbursement</h2>
      <p>Many employers reimburse employees for driving their own cars for work. Under an <strong>accountable plan</strong> — you substantiate the miles and return any excess — reimbursement up to the IRS rate is tax-free and doesn’t appear as wages on your W-2. If your employer pays more than the IRS rate, the excess is taxable income. If they pay less, employees can’t deduct the difference federally. Enter the amount you were reimbursed under <em>Tax savings estimate</em> to see the excess or shortfall. Employers may use the calculator as a <strong>mileage reimbursement calculator</strong> by entering their own rate per mile.</p>

      <h2 id="what-counts">What counts as business mileage?</h2>
      <ul>
        <li>Driving between two work locations, or from your office to a client, customer or job site.</li>
        <li>Trips to the bank, post office or supply store for the business.</li>
        <li>Travel to a temporary work location away from your regular place of business.</li>
        <li>From a qualifying <a href="/calculators/home-office-deduction/">home office</a> (your principal place of business) to other work locations.</li>
      </ul>
      <p><strong>Commuting doesn’t count</strong> — driving from home to your regular office or workplace is personal, even if you take calls on the way.</p>

      <h2 id="records">Mileage log requirements</h2>
      <p>The IRS requires a written record made at or near the time of each trip. For each trip, record the <strong>date, destination, business purpose and miles driven</strong>, plus your odometer readings at the start and end of the year. Apps that track trips by GPS are fine. Without a log, the deduction can be disallowed entirely in an audit. If you use actual expenses, also keep receipts for every car expense.</p>
      <div class="callout warn"><?= icon('shield') ?><p><strong>Choosing a method:</strong> to use the standard rate on a car you own, you must choose it in the first year the car is used for business. After that you can switch between methods year to year (using straight-line depreciation). If you lease, using the standard rate commits you for the whole lease. Fleets of five or more vehicles used at once can’t use the standard rate.</p></div>
      <p>Self-employed? Mileage deductions reduce your quarterly estimates too — see the <a href="/calculators/quarterly-estimated-tax/">quarterly estimated tax calculator</a> and our guide to <a href="/blog/got-a-1099-exactly-what-to-do-next/">what to do after getting a 1099</a>. Buying a vehicle for business? The <a href="/calculators/depreciation-calculator/">depreciation calculator</a> covers Section 179 and bonus depreciation.</p>

<?= faq_block([
  ["What is the IRS mileage rate for $Y?", "<p>The $Y standard mileage rate is {$rateC}¢ per mile for business driving, " . ($OTHER[(string) $Y]['medical'] * 100) . "¢ for medical and military moving, and 14¢ for charitable driving. Check irs.gov for official updates.</p>"],
  ['How do I calculate my mileage deduction?', "<p>Multiply your business miles by the standard rate and add business parking and tolls. For example, 10,000 business miles × {$rateC}¢ = " . money(10000 * $rate) . ". Or use the actual expense method: total car costs × your business-use percentage.</p>"],
  ['Is it better to take mileage or actual expenses?', '<p>The standard rate is simpler and usually wins for economical cars driven many miles. Actual expenses often win for expensive vehicles, high insurance costs or very high business use. The calculator shows both side by side.</p>'],
  ['How much does a mileage deduction save in taxes?', "<p>A deduction isn’t a dollar-for-dollar refund. Your savings equal the deduction times your tax rate. For a self-employed person in the 22% bracket, a " . money(10000 * $rate) . " deduction saves roughly " . money(10000 * $rate * 0.9235 * 0.153 + (10000 * $rate - 10000 * $rate * 0.9235 * 0.153 / 2) * 0.22) . " in federal income and self-employment tax combined.</p>"],
  ['Can W-2 employees deduct mileage?', '<p>Generally no. Unreimbursed employee expenses are no longer deductible on federal returns, and the One Big Beautiful Bill Act made that permanent. A few groups — Armed Forces reservists, qualified performing artists and fee-basis officials — are exceptions. Some states still allow the deduction.</p>'],
  ['Is mileage reimbursement taxable?', '<p>Not if it’s paid under an accountable plan at or below the IRS standard rate and you substantiate the miles. Amounts above the IRS rate, or flat car allowances without substantiation, are taxable wages.</p>'],
  ['Can I deduct my commute?', '<p>No. Driving between your home and your regular place of work is a personal commuting expense. Trips from your regular workplace to clients, or from a qualifying home office to other work sites, are deductible.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('mileage-deduction', ['1099-tax-calculator', 'self-employment-tax', 'home-office-deduction', 'depreciation-calculator', 'quarterly-estimated-tax', 's-corp-tax-savings']) ?></div>
