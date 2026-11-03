<?php
defined('CPA') or exit;
$Y = TAX_YEAR;
$y = $TAX['years'][(string) $Y];
$rate = $y['homeOfficeSimplifiedRate'];
$P['title'] = "Home Office Deduction Calculator $Y — Simplified vs Regular Method | CPA Calculator";
$P['description'] = "Free $Y home office deduction calculator. Compare the simplified \${$rate}/sq ft method with the regular method and depreciation, and see your federal tax savings.";
$P['scripts'] = ['/assets/js/tools/home-office-deduction.js'];
$P['modified'] = date('Y-m-d', filemtime(__FILE__));

/* Federal tax on self-employment profit (mirrors CPA.estimate for one filer with no W-2). */
function ho_fed_total(float $profit, string $status = 'single'): float {
  global $TAX;
  $y = $TAX['years'][(string) TAX_YEAR];
  $base = max(0, $profit) * 0.9235;
  $se = $base < 400 ? 0 : min($base, $y['ssWageBase']) * 0.124 + $base * 0.029;
  $agi = max(0, $profit - $se / 2);
  $before = max(0, $agi - $y['std'][$status]);
  $qbi = min(max(0, $profit) * 0.2, $before * 0.2);
  return $se + fed_tax(max(0, $before - $qbi), $status)['tax'];
}
/* Worked example: 200 sq ft office in a 2,000 sq ft owned home, $60,000 net profit. */
$ex = ['office' => 200, 'home' => 2000, 'interest' => 12000, 'ptax' => 4000, 'ins' => 1500, 'util' => 3600, 'rep' => 1000, 'basis' => 350000, 'land' => 70000, 'profit' => 60000];
$ex['pct'] = $ex['office'] / $ex['home'];
$ex['simple'] = min(300, $ex['office']) * $rate;
$ex['t1'] = ($ex['interest'] + $ex['ptax']) * $ex['pct'];
$ex['t2'] = ($ex['ins'] + $ex['util'] + $ex['rep']) * $ex['pct'];
$ex['dep'] = ($ex['basis'] - $ex['land']) * $ex['pct'] / 39;
$ex['regular'] = $ex['t1'] + $ex['t2'] + $ex['dep'];
$ex['taxBase'] = ho_fed_total($ex['profit']);
$ex['saveSimple'] = $ex['taxBase'] - ho_fed_total($ex['profit'] - $ex['simple']);
$ex['saveRegular'] = $ex['taxBase'] - ho_fed_total($ex['profit'] - $ex['regular']);

echo tool_hero('home-office-deduction', "Home Office Deduction Calculator $Y",
  "Work from home and run your own business? Compare the IRS simplified method (\${$rate} per square foot, up to 300 sq ft) with the regular actual-expense method — mortgage interest or rent, utilities, insurance, repairs and depreciation — and see which gives the bigger deduction and how much federal tax it saves.",
  ['Simplified vs regular method', 'Depreciation over 39 years', 'Gross-income limit applied', 'Estimated tax savings']);
?>
<section class="tool" aria-label="Home office deduction calculator">
  <div class="wrap">
    <div class="tool-box">
      <form class="tool-form" id="ho-form" novalidate>
        <div class="grid-2">
          <?= year_field() ?>
          <div class="field"><span class="lbl">Your home</span><div class="seg" role="radiogroup" aria-label="Own or rent">
            <label><input type="radio" name="housing" value="own" checked><span>I own</span></label>
            <label><input type="radio" name="housing" value="rent"><span>I rent</span></label>
          </div></div>
        </div>
        <?= status_field() ?>
        <fieldset class="fieldset"><legend>Office size</legend>
          <div class="grid-2">
            <?= money_field('office', 'Office area (sq ft)', 200, 'Space used regularly and exclusively for business. A spare room, or a clearly defined part of a room.', '', '') ?>
            <?= money_field('home', 'Total home area (sq ft)', 2000, 'Finished living area of the whole home. Used to work out your business-use percentage.', '', '') ?>
          </div>
        </fieldset>
        <fieldset class="fieldset"><legend>Business income</legend>
          <?= money_field('profit', 'Net business profit before the home office', 60000, 'Schedule C gross income minus all other business expenses. The home office deduction cannot exceed this amount (the gross-income limitation).') ?>
          <input type="range" min="0" max="300000" step="1000" data-range-for="profit" aria-label="Business profit slider">
          <?= money_field('wages', 'W-2 wages (if any)', '', 'Wages from a job. Used only to estimate your tax bracket and Social Security wage base — W-2 employees cannot take the home office deduction for their job.') ?>
        </fieldset>
        <fieldset class="fieldset"><legend>Annual home expenses (whole home)</legend>
          <div data-when="rent" hidden><?= money_field('rent', 'Rent paid for the year', 21600, 'Total rent for the year (12 × monthly rent).') ?></div>
          <div class="grid-2" data-when="own">
            <?= money_field('interest', 'Mortgage interest', 12000, 'Form 1098 box 1. Only interest — not principal.') ?>
            <?= money_field('ptax', 'Real estate taxes', 4000, 'Property tax paid on the home for the year.') ?>
          </div>
          <div class="grid-2">
            <?= money_field('ins', 'Homeowners / renters insurance', 1500, 'Annual premium for the whole home.') ?>
            <?= money_field('util', 'Utilities', 3600, 'Electricity, gas, water, trash and home internet for the whole home.') ?>
          </div>
          <div class="grid-2">
            <?= money_field('repairs', 'General repairs & maintenance', 1000, 'Repairs that benefit the whole home (roof patch, furnace service, painting the exterior).') ?>
            <div data-when="own"><?= money_field('hoa', 'HOA / condo fees', '', 'Homeowners association dues for the year.') ?></div>
          </div>
          <?= money_field('direct', 'Direct office expenses', '', 'Costs only for the office itself (painting or repairing the office). Deductible at 100%, not by percentage.') ?>
          <details class="more" data-when="own" open><summary>Depreciation (homeowners)</summary>
            <div class="grid-2">
              <?= money_field('basis', 'Home cost basis', 350000, 'Purchase price plus closing costs and permanent improvements. If the home is worth less today, use the lower fair market value.') ?>
              <?= money_field('land', 'Land value (not depreciable)', 70000, 'Land never depreciates. Your property tax bill usually splits land and building values.') ?>
            </div>
            <div class="field"><label for="f-first">First year using this office?</label><select id="f-first" name="first">
              <option value="0">No — used all year</option>
              <?php foreach (['January','February','March','April','May','June','July','August','September','October','November','December'] as $i => $m) echo '<option value="' . ($i + 1) . '">Yes — started in ' . $m . '</option>'; ?>
            </select><span class="hint">The first year uses the IRS mid-month convention for 39-year property.</span></div>
          </details>
        </fieldset>
        <?= tool_actions() ?>
      </form>
      <div class="tool-out" aria-live="polite">
        <div class="tool-out-inner">
          <div class="res-label">Your best home office deduction</div>
          <div class="res-big good" data-out="best">$0</div>
          <div class="res-sub" data-out="winner">—</div>
          <div class="kpis">
            <div class="kpi"><small>Simplified method</small><b data-out="simple">$0</b></div>
            <div class="kpi"><small>Regular method</small><b data-out="regular">$0</b></div>
            <div class="kpi"><small>Business-use %</small><b data-out="pct">0%</b></div>
            <div class="kpi"><small>Est. federal tax saved</small><b data-out="save">$0</b></div>
          </div>
          <div class="res-label" style="margin-bottom:4px">Simplified vs regular</div>
          <div class="meter" data-meter role="img" aria-label="Simplified compared with regular method"></div>
          <div class="donut-wrap"><svg data-donut viewBox="0 0 100 100" role="img" aria-label="Regular method deduction by type"></svg><ul class="legend" data-legend></ul></div>
          <ul class="rows" data-rows></ul>
          <p class="note"><span data-out="limitnote">Estimate only — federal tax savings include income tax and self-employment tax; state tax not included.</span> <a href="/our-methodology/">Methodology</a>.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="tool-content">
  <div class="wrap">
    <article class="prose">
      <h2 id="how-to-use">How to use the home office deduction calculator</h2>
      <p>This calculator works out both IRS methods side by side and shows the larger one. You need three things: the size of your office, the size of your home, and your annual home costs.</p>
      <ol>
        <li><strong>Choose own or rent.</strong> Homeowners deduct a share of mortgage interest, property tax and depreciation; renters deduct a share of rent.</li>
        <li><strong>Enter square footage.</strong> Your office area divided by your home’s total area is your <em>business-use percentage</em> — the share of each home expense you can deduct under the regular method.</li>
        <li><strong>Enter your net business profit</strong> before the home office. The deduction can’t be bigger than this (more on that below), and it drives the tax-savings estimate.</li>
        <li><strong>Add annual expenses for the whole home.</strong> The calculator applies your percentage automatically. Costs that only affect the office, such as painting it, go in “direct office expenses” and count in full.</li>
      </ol>
      <p>The results panel shows each method, the winner, a line-by-line Form 8829-style breakdown and an estimate of how much federal income tax and self-employment tax the deduction saves.</p>

      <h2 id="who-qualifies">Who can take the home office deduction?</h2>
      <p>The deduction is for people who are <strong>self-employed</strong> — sole proprietors, freelancers, independent contractors, single-member LLC owners and partners — plus some statutory employees. To qualify, the space must be used:</p>
      <ul>
        <li><strong>Regularly and exclusively</strong> for business. A desk in the corner of the guest room counts only if that defined area is never used for anything personal. (Daycare providers and inventory storage are exceptions to the exclusive-use rule.)</li>
        <li><strong>As your principal place of business</strong>, or as a place where you regularly meet clients, or as a separate structure (such as a detached studio) used for the business. Doing your admin and management work at home counts even if you perform services elsewhere.</li>
      </ul>
      <div class="callout warn"><?= icon('shield') ?><p><strong>W-2 employees can’t deduct a home office</strong> for their employer’s work, even if they work remotely full time. Unreimbursed employee expenses were suspended from 2018 and the One Big Beautiful Bill Act made that permanent. If you have both a job and a side business, only the side business can use the deduction.</p></div>

      <h2 id="simplified-method">The simplified method: $<?= $rate ?> per square foot</h2>
      <p>The simplified method lets you deduct <strong>$<?= $rate ?> for each square foot</strong> of qualifying office space, up to 300 square feet — a maximum of <strong><?= money(300 * $rate) ?></strong> a year. There’s no Form 8829, no receipts for home costs and no depreciation to track or recapture when you sell.</p>
      <div class="formula">Simplified deduction = min(office sq ft, 300) × $<?= $rate ?></div>
      <p>The trade-offs: you can’t deduct actual expenses above that cap, you can’t carry unused amounts to next year, and the deduction still can’t exceed your business’s gross income limit. Homeowners using it keep deducting mortgage interest and property tax in full on Schedule A if they itemize.</p>

      <h2 id="regular-method">The regular method (actual expenses, Form 8829)</h2>
      <p>The regular method deducts the business share of what it actually costs to run your home:</p>
      <div class="formula">Business-use % = office sq ft ÷ total home sq ft<br>Regular deduction = business-use % × (rent or mortgage interest + property tax + insurance + utilities + repairs + HOA)<br>&nbsp;&nbsp;+ direct office expenses + depreciation<br>Depreciation = (home basis − land value) × business-use % ÷ 39</div>
      <p>Depreciation is the piece most people forget. Because a home office is treated as nonresidential real property, the business share of the building (never the land) is depreciated straight-line over <strong>39 years</strong>, using the mid-month convention in the first year. The basis is the lower of what you paid (plus improvements) or the home’s fair market value when you started using the office. Depreciation lowers your basis, and when you sell, the depreciation claimed after May 6, 1997 is taxed at up to 25% (“unrecaptured Section 1250 gain”) even if the rest of the gain is excluded.</p>
      <p>Mortgage principal, the cost of lawn care and expenses for rooms you don’t use for business are never deductible.</p>

      <h2 id="example">Worked example: simplified vs regular</h2>
      <p>A single freelancer owns a <?= number_format($ex['home']) ?> sq ft home and uses a <?= $ex['office'] ?> sq ft spare bedroom exclusively as an office — a <?= round($ex['pct'] * 100) ?>% business-use percentage. Their <?= $Y ?> net business profit is <?= money($ex['profit']) ?>.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Expense</th><th class="n">Whole home</th><th class="n">Business share</th></tr></thead><tbody>
        <tr><td>Mortgage interest</td><td class="n"><?= money($ex['interest']) ?></td><td class="n"><?= money($ex['interest'] * $ex['pct']) ?></td></tr>
        <tr><td>Real estate taxes</td><td class="n"><?= money($ex['ptax']) ?></td><td class="n"><?= money($ex['ptax'] * $ex['pct']) ?></td></tr>
        <tr><td>Insurance</td><td class="n"><?= money($ex['ins']) ?></td><td class="n"><?= money($ex['ins'] * $ex['pct']) ?></td></tr>
        <tr><td>Utilities</td><td class="n"><?= money($ex['util']) ?></td><td class="n"><?= money($ex['util'] * $ex['pct']) ?></td></tr>
        <tr><td>Repairs</td><td class="n"><?= money($ex['rep']) ?></td><td class="n"><?= money($ex['rep'] * $ex['pct']) ?></td></tr>
        <tr><td>Depreciation (<?= money($ex['basis'] - $ex['land']) ?> building × <?= round($ex['pct'] * 100) ?>% ÷ 39)</td><td class="n">—</td><td class="n"><?= money($ex['dep']) ?></td></tr>
        <tr><td><strong>Regular method</strong></td><td class="n"></td><td class="n"><strong><?= money($ex['regular']) ?></strong></td></tr>
        <tr><td><strong>Simplified method</strong> (<?= $ex['office'] ?> sq ft × $<?= $rate ?>)</td><td class="n"></td><td class="n"><strong><?= money($ex['simple']) ?></strong></td></tr>
      </tbody></table></div>
      <p>The regular method is worth <?= money($ex['regular'] - $ex['simple']) ?> more. Because a home office deduction lowers both self-employment tax and income tax, it saves this freelancer roughly <strong><?= money($ex['saveRegular']) ?></strong> in federal tax with the regular method versus about <?= money($ex['saveSimple']) ?> with the simplified method. (Under the regular method, the <?= money($ex['t1']) ?> of business-share interest and taxes moves from Schedule A to Schedule C, which matters only if you itemize.)</p>

      <h2 id="which-method">Which method should you choose?</h2>
      <div class="table-wrap"><table>
        <thead><tr><th></th><th>Simplified method</th><th>Regular method</th></tr></thead><tbody>
        <tr><td>Deduction</td><td>$<?= $rate ?>/sq ft, max <?= money(300 * $rate) ?></td><td>Actual expenses × business-use %, no cap</td></tr>
        <tr><td>Record keeping</td><td>Square footage and proof of exclusive use</td><td>Receipts for every home expense, basis records</td></tr>
        <tr><td>Depreciation</td><td>None (zero depreciation for those years)</td><td>39-year straight line; recaptured on sale</td></tr>
        <tr><td>Over the income limit</td><td>Lost — no carryover</td><td>Excess carries forward to future years</td></tr>
        <tr><td>Form</td><td>Schedule C line 30 worksheet</td><td>Form 8829</td></tr>
        <tr><td>Usually better for</td><td>Renters with low rent, small offices, people who want simplicity</td><td>Larger offices, high-cost homes, high rent</td></tr>
      </tbody></table></div>
      <p>You can switch methods from year to year. If you go back to the regular method after using the simplified method, you use the optional depreciation tables for the remaining recovery period.</p>

      <h2 id="income-limit">The gross-income limitation and carryovers</h2>
      <p>A home office can’t create or increase a business loss. Under the regular method, Form 8829 applies the deduction in three tiers:</p>
      <ol>
        <li><strong>Mortgage interest and real estate taxes</strong> (business share) — always allowed, because you could deduct them anyway.</li>
        <li><strong>Operating expenses</strong> — rent, insurance, utilities, repairs and HOA fees — allowed up to the profit that remains.</li>
        <li><strong>Depreciation</strong> — allowed last, up to any profit still left.</li>
      </ol>
      <p>Anything disallowed in tiers 2 and 3 carries forward to next year’s Form 8829. The calculator applies this order automatically and shows any carryover. Under the simplified method, the amount over the limit is simply lost.</p>

      <h2 id="tips">Tips to get the deduction right</h2>
      <ul>
        <li><strong>Measure and photograph</strong> the space so you can prove exclusive use if asked.</li>
        <li><strong>Separate direct and indirect costs.</strong> Painting your office is 100% deductible; painting the whole house is indirect.</li>
        <li><strong>Don’t double-count.</strong> If you deduct your internet as a business expense elsewhere, leave it out of utilities here.</li>
        <li><strong>Remember the rest of your write-offs.</strong> Office furniture and computers are deducted separately, often in full the first year — see the <a href="/calculators/depreciation-calculator/">depreciation calculator</a>. Driving from a qualifying home office to clients is deductible business mileage, not commuting — see the <a href="/calculators/mileage-deduction/">mileage deduction calculator</a>.</li>
        <li><strong>See the whole picture.</strong> Plug your deduction into the <a href="/calculators/1099-tax-calculator/">1099 tax calculator</a> or <a href="/calculators/self-employment-tax/">self-employment tax calculator</a> to update your <a href="/calculators/quarterly-estimated-tax/">quarterly estimated payments</a>. New to 1099 work? Read <a href="/blog/got-a-1099-exactly-what-to-do-next/">Got a 1099? Here’s exactly what to do next</a>.</li>
      </ul>

<?= faq_block([
  ['How much can I deduct for a home office?', '<p>With the simplified method, $' . $rate . ' per square foot up to 300 sq ft — a maximum of ' . money(300 * $rate) . '. With the regular method there’s no fixed cap: you deduct your business-use percentage of rent or mortgage interest, property tax, insurance, utilities, repairs and depreciation, limited to your business profit. In our example, a 200 sq ft office in a 2,000 sq ft home produces ' . money($ex['regular']) . ' under the regular method.</p>'],
  ['Is the regular or simplified home office method better?', '<p>The regular method usually wins for larger offices, homeowners with high interest and property taxes, and renters in expensive areas. The simplified method wins when your office is small, your housing costs are low or you value simplicity and want to avoid depreciation recapture. The calculator compares both instantly.</p>'],
  ['Can W-2 employees take the home office deduction?', '<p>No. Employees who work from home for an employer can’t deduct a home office on their federal return. The deduction is for self-employed people, partners and certain statutory employees. Some states still allow unreimbursed employee expenses.</p>'],
  ['Do I have to pay back home office depreciation when I sell?', '<p>Depreciation you claimed (or could have claimed) after May 6, 1997 is taxed as unrecaptured Section 1250 gain at a maximum 25% rate when you sell, even if the rest of your gain is excluded under the $250,000/$500,000 home sale exclusion. The simplified method avoids this because it has no depreciation.</p>'],
  ['Can I deduct a home office if I rent?', '<p>Yes. Renters multiply annual rent (plus renters insurance, utilities and repairs they pay) by the business-use percentage. Rent is often the largest single home office expense, so renters in high-cost cities frequently get far more from the regular method than the ' . money(300 * $rate) . ' simplified cap.</p>'],
  ['What if my home office deduction is more than my business income?', '<p>The deduction can’t create a loss. Under the regular method, mortgage interest and property tax are allowed in full, but excess operating expenses and depreciation carry forward to next year. Under the simplified method, the excess is lost.</p>'],
  ['Does a home office have to be a separate room?', '<p>No. A clearly defined area of a room qualifies if it’s used regularly and only for business. Measure just that area. A dining table you also eat at doesn’t qualify.</p>'],
]) ?>
    </article>
  </div>
</section>
<div class="wrap"><?= related_tools('home-office-deduction', ['1099-tax-calculator', 'self-employment-tax', 'mileage-deduction', 'depreciation-calculator', 'quarterly-estimated-tax', 's-corp-tax-savings']) ?></div>
