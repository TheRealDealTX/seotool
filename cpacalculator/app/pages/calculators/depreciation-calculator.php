<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$P['title'] = "Depreciation Calculator $Y — MACRS, Straight-Line & Section 179 | CPA Calculator";
$P['description'] = "Free depreciation calculator with MACRS tables, straight-line, double-declining balance and sum-of-years-digits, plus Section 179 and $Y bonus depreciation.";
$P['scripts'] = ['/assets/js/tools/depreciation-calculator.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* IRS Pub. 946 Table A-1: GDS half-year convention percentages (same numbers as the JS). */
$MACRS = [
  3 => [33.33, 44.45, 14.81, 7.41],
  5 => [20.00, 32.00, 19.20, 11.52, 11.52, 5.76],
  7 => [14.29, 24.49, 17.49, 12.49, 8.93, 8.92, 8.93, 4.46],
  10 => [10.00, 18.00, 14.40, 11.52, 9.22, 7.37, 6.55, 6.55, 6.56, 6.55, 3.28],
  15 => [5.00, 9.50, 8.55, 7.70, 6.93, 6.23, 5.90, 5.90, 5.91, 5.90, 5.91, 5.90, 5.91, 5.90, 5.91, 2.95],
  20 => [3.750, 7.219, 6.677, 6.177, 5.713, 5.285, 4.888, 4.522, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 2.231],
];
/* Section 179 dollar limit and phase-out threshold by tax year (2025–2026 per OBBBA, indexed for 2026). */
$S179 = [2026 => [2560000, 4090000], 2025 => [2500000, 4000000], 2024 => [1220000, 3050000], 2023 => [1160000, 2890000]];

$exCost = 50000;
$ex5 = array_map(fn($p) => $exCost * $p / 100, $MACRS[5]);
$exSl = ($exCost - 5000) / 5;

echo tool_hero('depreciation-calculator', "Depreciation Calculator",
  "Build a year-by-year depreciation schedule in seconds. Choose straight-line, double-declining balance, sum-of-the-years’-digits or MACRS (with the official IRS percentage tables), then add Section 179 expensing or 100% bonus depreciation to see your first-year tax deduction.",
  ['MACRS 3- to 39-year tables', 'Section 179 & bonus', 'SL, DDB & SYD book methods', 'Printable schedule']);
?>
<section class="tool" aria-label="Depreciation calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="dep-form" novalidate>
        <div class="field"><span class="lbl">Depreciation method</span><div class="seg" role="radiogroup" aria-label="Depreciation method">
          <label><input type="radio" name="method" value="macrs" checked><span>MACRS (tax)</span></label>
          <label><input type="radio" name="method" value="sl"><span>Straight-line</span></label>
          <label><input type="radio" name="method" value="ddb"><span>Double-declining</span></label>
          <label><input type="radio" name="method" value="syd"><span>Sum-of-years’-digits</span></label>
        </div></div>
        <fieldset class="fieldset"><legend>Asset</legend>
          <div class="grid-2">
            <?= money_field('cost', 'Asset cost (basis)', $exCost, 'Purchase price plus sales tax, shipping, installation and other costs to get the asset ready for use.') ?>
            <?= money_field('bizPct', 'Business use', 100, 'Percentage of use that is for business. Listed property such as cars must be used more than 50% for business to use MACRS accelerated methods, Section 179 or bonus depreciation.', '', '%') ?>
          </div>
          <div class="grid-2">
            <div class="field"><label for="f-month">Month placed in service</label><select id="f-month" name="month">
              <?php foreach (['January','February','March','April','May','June','July','August','September','October','November','December'] as $i => $m) echo '<option value="' . ($i + 1) . '"' . ($i === 2 ? ' selected' : '') . '>' . $m . '</option>'; ?>
            </select></div>
            <div class="field"><label for="f-pyear">Year placed in service</label><select id="f-pyear" name="pyear">
              <?php for ($i = $Y; $i >= $Y - 6; $i--) echo '<option value="' . $i . '"' . ($i === $Y ? ' selected' : '') . '>' . $i . '</option>'; ?>
            </select></div>
          </div>
          <div class="grid-2" data-when="book">
            <?= money_field('salvage', 'Salvage value', 5000, 'What you expect the asset to be worth at the end of its useful life. Ignored for MACRS.') ?>
            <?= money_field('life', 'Useful life (years)', 5, 'How many years you expect to use the asset (1–50).', '', '') ?>
          </div>
          <div data-when="macrs">
            <div class="field"><label for="f-cls">MACRS property class (GDS)</label><select id="f-cls" name="cls">
              <option value="3">3-year — tractor units, special tools</option>
              <option value="5" selected>5-year — computers, vehicles</option>
              <option value="7">7-year — furniture, machinery</option>
              <option value="10">10-year — vessels, fruit trees</option>
              <option value="15">15-year — land improvements</option>
              <option value="15sl">15-year SL — qualified improvements</option>
              <option value="20">20-year — farm buildings</option>
              <option value="27.5">27.5-year — residential rental</option>
              <option value="39">39-year — nonresidential real</option>
            </select></div>
            <div class="field" data-when-personal><label for="f-conv">Convention</label><select id="f-conv" name="conv">
              <option value="hy">Half-year (most common)</option>
              <option value="mq">Mid-quarter</option>
            </select><span class="hint">Mid-quarter is required if more than 40% of the depreciable property you placed in service this year went in during October–December.</span></div>
          </div>
        </fieldset>
        <fieldset class="fieldset" data-when="macrs"><legend>First-year write-offs</legend>
          <div data-when-personal>
            <div class="grid-2">
              <?= money_field('s179', 'Section 179 expense', '', 'Amount you elect to expense immediately. Limited to the annual cap, your business taxable income and the asset’s business basis.') ?>
              <div class="field"><label for="f-bonus">Bonus depreciation</label><select id="f-bonus" name="bonus">
                <option value="100">100% — acquired after Jan 19, 2025</option>
                <option value="phase">Acquired before Jan 20, 2025 (phase-down rate)</option>
                <option value="0" selected>None / elect out</option>
              </select></div>
            </div>
          </div>
          <?= money_field('rate', 'Your marginal tax rate', 24, 'Federal bracket (plus state rate if you like). Used to estimate the tax value of the deduction.', '', '%') ?>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label" data-out="biglabel">First-year depreciation deduction</div>
          <div class="res-big" data-out="y1">$0</div>
          <div class="res-sub" data-out="sub">—</div>
          <div class="kpis">
            <div class="kpi"><small>Depreciable basis</small><b data-out="basis">$0</b></div>
            <div class="kpi"><small>Total depreciation</small><b data-out="total">$0</b></div>
            <div class="kpi"><small>Tax years in schedule</small><b data-out="years">0</b></div>
            <div class="kpi"><small>Year-1 tax value</small><b data-out="taxval">$0</b></div>
          </div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="How the asset cost is recovered"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note"><span data-out="note">Estimate only.</span> <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
    <div class="table-wrap"><table>
      <caption class="sr-only">Year-by-year depreciation schedule</caption>
      <thead><tr><th>Tax year</th><th class="n" data-out="ratehead">Rate</th><th class="n">Depreciation</th><th class="n">Accumulated</th><th class="n">Book value (end of year)</th></tr></thead>
      <tbody data-schedule></tbody>
    </table></div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use this depreciation calculator</h2>
      <p>Pick a method, enter what the asset cost and when you started using it, and the calculator builds a full depreciation schedule with the deduction, accumulated depreciation and remaining book value for every year.</p>
      <ul>
        <li><strong>MACRS (tax)</strong> — the method the IRS requires for most business property placed in service after 1986. Choose the property class; salvage value and useful life don’t apply. Add a Section 179 election or bonus depreciation to see how much you can write off in year one.</li>
        <li><strong>Straight-line, double-declining balance and sum-of-the-years’-digits</strong> — book (financial statement) methods. Enter salvage value and useful life. The first year is prorated by the month the asset was placed in service.</li>
      </ul>
      <p>Enter a business-use percentage below 100% for mixed-use assets, such as a vehicle you also drive personally. The schedule below the calculator updates live and prints cleanly with the “Print / save PDF” button.</p>

      <h2 id="methods">Depreciation methods and formulas</h2>
      <h3 id="straight-line">Straight-line depreciation</h3>
      <p>The simplest method spreads the cost evenly over the asset’s useful life.</p>
      <div class="formula">Annual depreciation = (cost − salvage value) ÷ useful life</div>
      <p>A <?= money($exCost) ?> machine with a $5,000 salvage value and a 5-year life depreciates <?= money($exSl) ?> a year. If it’s placed in service in March, year one gets 10/12 of that and the remaining 2/12 falls in a sixth calendar year.</p>
      <h3 id="double-declining">Double-declining balance (DDB)</h3>
      <p>An accelerated method that applies twice the straight-line rate to the remaining book value, so the deduction is largest in the early years.</p>
      <div class="formula">DDB rate = 2 ÷ useful life<br>Depreciation = book value at start of year × DDB rate<br>Switch to straight-line when SL on the remaining balance is larger; never go below salvage</div>
      <h3 id="syd">Sum-of-the-years’-digits (SYD)</h3>
      <p>Another accelerated method. For a 5-year asset the digits add to 15 (5+4+3+2+1), so year one takes 5/15 of the depreciable cost, year two 4/15, and so on.</p>
      <div class="formula">SYD = n(n+1) ÷ 2<br>Depreciation in year k = (cost − salvage) × (n − k + 1) ÷ SYD</div>

      <h2 id="macrs">MACRS depreciation explained</h2>
      <p>The Modified Accelerated Cost Recovery System is the tax depreciation system for most US business property. Under the General Depreciation System (GDS), personal property in the 3-, 5-, 7- and 10-year classes uses 200% declining balance switching to straight-line; 15- and 20-year property uses 150% declining balance; and real property uses straight-line. Salvage value is always zero.</p>
      <p><strong>Conventions</strong> decide how much depreciation you get in the first year:</p>
      <ul>
        <li><strong>Half-year</strong> — treats personal property as placed in service at mid-year, whatever the actual month. That’s why a 5-year asset is depreciated over six tax years.</li>
        <li><strong>Mid-quarter</strong> — required when more than 40% of the year’s depreciable personal property (excluding real property and amounts expensed) is placed in service in the last three months. Each asset is treated as placed in service at the middle of its quarter.</li>
        <li><strong>Mid-month</strong> — used for residential rental (27.5-year) and nonresidential real property (39-year). The asset is treated as placed in service in the middle of its month.</li>
      </ul>
      <h3 id="macrs-table">MACRS percentage table (half-year convention)</h3>
      <p>These are the IRS Publication 946 Table A-1 rates the calculator uses. Multiply the rate by the asset’s depreciable basis (after any Section 179 and bonus).</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Year</th><?php foreach (array_keys($MACRS) as $c) echo '<th class="n">' . $c . '-year</th>'; ?></tr></thead><tbody>
<?php for ($r = 0; $r < 21; $r++): ?>
        <tr><td><?= $r + 1 ?></td><?php foreach ($MACRS as $rates) echo '<td class="n">' . (isset($rates[$r]) ? number_format($rates[$r], $rates === $MACRS[20] ? 3 : 2) . '%' : '') . '</td>'; ?></tr>
<?php endfor; ?>
      </tbody></table></div>
      <p>Residential rental property is recovered over 27.5 years and nonresidential real property over 39 years, straight-line with the mid-month convention: a full year is 3.636% (27.5-year) or 2.564% (39-year), and the first year is prorated by month.</p>

      <h2 id="example">Worked example: <?= money($exCost) ?> of equipment</h2>
      <p>A business buys <?= money($exCost) ?> of computers and office equipment (5-year property) and places it in service in March <?= $Y ?>. It’s the only property placed in service that year, so the half-year convention applies.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Tax year</th><th class="n">MACRS rate</th><th class="n">Depreciation</th><th class="n">Book value</th></tr></thead><tbody>
<?php $bv = $exCost; foreach ($ex5 as $i => $dep): $bv -= $dep; ?>
        <tr><td><?= $Y + $i ?></td><td class="n"><?= number_format($MACRS[5][$i], 2) ?>%</td><td class="n"><?= money($dep) ?></td><td class="n"><?= money(max(0, $bv)) ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <p>With <strong>100% bonus depreciation</strong> (the equipment was acquired after January 19, 2025), the entire <?= money($exCost) ?> is deducted in <?= $Y ?>. At a 24% marginal rate that’s about <?= money($exCost * 0.24) ?> of federal income tax saved in the first year instead of <?= money($ex5[0] * 0.24) ?>.</p>

      <h2 id="section-179">Section 179 and bonus depreciation in <?= $Y ?></h2>
      <p>Two provisions let businesses deduct much or all of an asset’s cost in the year it’s placed in service instead of over its recovery period. The One Big Beautiful Bill Act (OBBBA) expanded both.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Tax year</th><th class="n">Section 179 limit</th><th class="n">Phase-out begins</th><th>Bonus depreciation</th></tr></thead><tbody>
<?php foreach ($S179 as $yr => [$lim, $ph]): ?>
        <tr><td><?= $yr ?></td><td class="n"><?= money($lim) ?></td><td class="n"><?= money($ph) ?></td><td><?= $yr >= 2025 ? '100% for property acquired after Jan 19, 2025; ' . ($yr === 2025 ? '40%' : '20%') . ' if acquired earlier' : ($yr === 2024 ? '60%' : '80%') ?></td></tr>
<?php endforeach; ?>
      </tbody></table></div>
      <ul>
        <li><strong>Section 179</strong> is an election to expense qualifying property — equipment, off-the-shelf software, qualified improvement property and certain roof, HVAC, fire-protection and security improvements to nonresidential buildings. The limit drops dollar-for-dollar once total qualifying purchases exceed the phase-out threshold, and the deduction can’t exceed your business taxable income (excess carries forward). SUVs over 6,000 lbs are capped at a lower Section 179 amount.</li>
        <li><strong>Bonus depreciation</strong> applies automatically to new and used property with a recovery period of 20 years or less unless you elect out by class. It isn’t limited by business income, so it can create a loss. OBBBA permanently restored 100% bonus depreciation for property acquired after January 19, 2025.</li>
        <li><strong>Order:</strong> Section 179 comes first, then bonus depreciation on what’s left, then regular MACRS on any remaining basis — the same order this calculator follows.</li>
      </ul>
      <div class="callout warn"><?= icon('shield') ?><p><strong>Watch the fine print.</strong> Passenger cars are subject to annual “luxury auto” depreciation caps; listed property must be used more than 50% for business; and if business use later drops, part of the deduction is recaptured. Residential rental buildings and nonresidential buildings themselves (27.5- and 39-year property) aren’t eligible for bonus depreciation.</p></div>

      <h2 id="book-vs-tax">Book depreciation vs tax depreciation</h2>
      <p>Many businesses keep two sets of numbers. Financial statements often use straight-line over an estimated useful life with a salvage value, while the tax return uses MACRS, Section 179 and bonus depreciation to lower taxable income sooner. The difference creates a temporary “book-tax difference” that reverses over the asset’s life. Accelerating depreciation doesn’t change the total you deduct — it changes <em>when</em> you deduct it, and when you sell, depreciation you claimed is generally recaptured as ordinary income (personal property) or taxed at up to 25% (real property).</p>

      <h2 id="related">Related tools and guides</h2>
      <p>A home office used in your business is depreciated as 39-year property — the <a href="/calculators/home-office-deduction/">home office deduction calculator</a> handles that for you. Vehicles can use the standard mileage rate instead of depreciation; compare both with the <a href="/calculators/mileage-deduction/">mileage deduction calculator</a>. To see how a big first-year deduction changes your tax bill, plug it into the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> or the <a href="/calculators/s-corp-tax-savings/">S corp tax savings calculator</a>, and adjust your <a href="/calculators/quarterly-estimated-tax/">quarterly estimated taxes</a> (our <a href="/blog/quarterly-taxes-101-guide/">quarterly taxes guide</a> explains the rules).</p>

<?= faq_block([
  ['How do you calculate depreciation?', '<p>For straight-line, subtract salvage value from cost and divide by the useful life. For tax purposes most assets use MACRS: multiply the depreciable basis by the IRS percentage for the asset’s class and year. For example, 5-year property under the half-year convention takes 20% in year one, 32% in year two, then 19.2%, 11.52%, 11.52% and 5.76%.</p>'],
  ['What is the MACRS depreciation rate for a 5-year or 7-year asset?', '<p>Using the half-year convention, 5-year property is depreciated 20.00%, 32.00%, 19.20%, 11.52%, 11.52% and 5.76% over six tax years. 7-year property is depreciated 14.29%, 24.49%, 17.49%, 12.49%, 8.93%, 8.92%, 8.93% and 4.46% over eight tax years.</p>'],
  ['Is bonus depreciation 100% in ' . $Y . '?', '<p>Yes, for qualifying property acquired after January 19, 2025. The One Big Beautiful Bill Act permanently restored 100% bonus depreciation. Property acquired under a binding contract before January 20, 2025 still follows the old phase-down: 40% if placed in service in 2025 and 20% in 2026.</p>'],
  ['What is the Section 179 limit for ' . $Y . '?', '<p>' . money($S179[$Y][0]) . ', reduced dollar-for-dollar once total qualifying property placed in service exceeds ' . money($S179[$Y][1]) . '. The deduction is also limited to your business taxable income; anything over that carries forward.</p>'],
  ['Should I use Section 179 or bonus depreciation?', '<p>With 100% bonus depreciation back, many businesses can simply use bonus. Section 179 is useful when you want to expense only part of an asset or choose asset by asset, and it covers some building improvements that bonus doesn’t. Bonus can create a net operating loss, while Section 179 can’t exceed business income. Many states don’t conform to federal bonus depreciation, which can tip the decision.</p>'],
  ['What is the difference between double-declining balance and MACRS?', '<p>MACRS for 3- to 10-year property is a 200% (double) declining balance method, but with a set recovery period, zero salvage value, a required convention and an automatic switch to straight-line. Book DDB uses your estimated useful life and stops at salvage value.</p>'],
  ['Can I depreciate land?', '<p>No. Land doesn’t wear out, so it’s never depreciable. When you buy a building, split the price between land and building and depreciate only the building. Land improvements such as fences, sidewalks and parking lots are depreciable over 15 years.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('depreciation-calculator', ['home-office-deduction', 'mileage-deduction', '1099-tax-calculator', 's-corp-tax-savings', 'profit-margin', 'break-even']) ?></div>
