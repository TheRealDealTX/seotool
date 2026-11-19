<?php
defined('ERE') or exit;

/** Numeric input. $o: pre, suf, step, min, max, help */
function fld(string $id, string $label, $value, array $o = []): string
{
    $pre = isset($o['pre']) ? '<span class="affix">' . e($o['pre']) . '</span>' : '';
    $suf = isset($o['suf']) ? '<span class="affix">' . e($o['suf']) . '</span>' : '';
    $help = isset($o['help']) ? '<small>' . e($o['help']) . '</small>' : '';
    return '<label class="fld"><span class="fld__label">' . e($label) . '</span>'
        . '<span class="fld__input">' . $pre . '<input type="number" inputmode="decimal" name="' . e($id) . '" id="f-' . e($id) . '" value="' . e($value) . '"'
        . ' step="' . e($o['step'] ?? 'any') . '" min="' . e($o['min'] ?? 0) . '"' . (isset($o['max']) ? ' max="' . e($o['max']) . '"' : '') . '>' . $suf . '</span>' . $help . '</label>';
}

function sel(string $id, string $label, array $opts, $value = null, string $help = ''): string
{
    $h = '<label class="fld"><span class="fld__label">' . e($label) . '</span><span class="fld__input"><select name="' . e($id) . '" id="f-' . e($id) . '">';
    foreach ($opts as $v => $t) {
        $h .= '<option value="' . e($v) . '"' . ((string) $v === (string) $value ? ' selected' : '') . '>' . e($t) . '</option>';
    }
    return $h . '</select></span>' . ($help ? '<small>' . e($help) . '</small>' : '') . '</label>';
}

function out(string $key, string $label, bool $big = false): string
{
    return '<div class="stat' . ($big ? ' stat--big' : '') . '"><span class="stat__label">' . e($label) . '</span><output class="stat__value" data-out="' . e($key) . '">-</output></div>';
}

function tool_view(string $slug): string
{
    ob_start();
    switch ($slug) {
    case 'mortgage-calculator': ?>
<form class="calc" data-tool="mortgage-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('price', 'Home price', 350000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('down', 'Down payment', 10, ['suf' => '%', 'step' => 0.5, 'max' => 100]) ?>
    <?= fld('rate', 'Interest rate', 6.5, ['suf' => '%', 'step' => 0.125]) ?>
    <?= sel('term', 'Loan term', [30 => '30 years', 20 => '20 years', 15 => '15 years', 10 => '10 years'], 30) ?>
    <?= fld('tax', 'Property tax rate', 2.2, ['suf' => '%/yr', 'step' => 0.05, 'help' => 'Total of all local rates. Many Houston-area homes: 1.8%-2.6%.']) ?>
    <?= fld('ins', 'Homeowners insurance', 3200, ['pre' => '$', 'suf' => '/yr', 'step' => 50]) ?>
    <?= fld('pmi', 'PMI rate', 0.6, ['suf' => '%/yr', 'step' => 0.05, 'help' => 'Applied only while you have under 20% equity.']) ?>
    <?= fld('hoa', 'HOA dues', 50, ['pre' => '$', 'suf' => '/mo', 'step' => 5]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('total', 'Estimated monthly payment', true) ?>
    <div class="bars" data-out-bars="breakdown"></div>
    <div class="stats">
      <?= out('pi', 'Principal & interest') ?>
      <?= out('taxm', 'Property tax') ?>
      <?= out('insm', 'Insurance') ?>
      <?= out('pmim', 'PMI') ?>
      <?= out('loan', 'Loan amount') ?>
      <?= out('interest', 'Total interest') ?>
      <?= out('pmiend', 'PMI ends') ?>
      <?= out('cash', 'Down payment') ?>
    </div>
  </div>
  <details class="calc__table"><summary>Show yearly amortization schedule</summary><div class="table-wrap" data-out-table="amort"></div></details>
</form>
<?php break;
    case 'home-affordability-calculator': ?>
<form class="calc" data-tool="home-affordability-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('income', 'Gross annual household income', 100000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('debts', 'Monthly debt payments', 500, ['pre' => '$', 'step' => 25, 'help' => 'Car, student loans, minimum card payments, child support.']) ?>
    <?= fld('downcash', 'Cash for down payment', 35000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('rate', 'Interest rate', 6.5, ['suf' => '%', 'step' => 0.125]) ?>
    <?= sel('term', 'Loan term', [30 => '30 years', 15 => '15 years'], 30) ?>
    <?= fld('tax', 'Property tax rate', 2.2, ['suf' => '%/yr', 'step' => 0.05]) ?>
    <?= fld('insrate', 'Insurance (as % of price)', 0.9, ['suf' => '%/yr', 'step' => 0.05, 'help' => 'Houston-area premiums often run 0.7%-1.2% of value.']) ?>
    <?= fld('hoa', 'HOA dues', 50, ['pre' => '$', 'suf' => '/mo', 'step' => 5]) ?>
    <?= sel('profile', 'DTI limits', ['28/36' => 'Conservative (28% / 36%)', '31/43' => 'Moderate (31% / 43%)', '36/50' => 'Aggressive (36% / 50%)'], '28/36') ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('price', 'You can afford a home up to', true) ?>
    <div class="stats">
      <?= out('payment', 'Monthly payment') ?>
      <?= out('loan', 'Loan amount') ?>
      <?= out('downpct', 'Down payment') ?>
      <?= out('limit', 'Limiting factor') ?>
      <?= out('front', 'Housing ratio') ?>
      <?= out('back', 'Total DTI') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'rent-vs-buy-calculator': ?>
<form class="calc" data-tool="rent-vs-buy-calculator" novalidate>
  <div class="calc__inputs">
    <fieldset><legend>Buying</legend>
    <?= fld('price', 'Home price', 325000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('down', 'Down payment', 10, ['suf' => '%', 'step' => 1]) ?>
    <?= fld('rate', 'Mortgage rate', 6.5, ['suf' => '%', 'step' => 0.125]) ?>
    <?= fld('tax', 'Property tax rate', 2.2, ['suf' => '%/yr', 'step' => 0.05]) ?>
    <?= fld('ins', 'Insurance', 3000, ['pre' => '$', 'suf' => '/yr', 'step' => 50]) ?>
    <?= fld('maint', 'Maintenance', 1, ['suf' => '% of value/yr', 'step' => 0.1]) ?>
    <?= fld('hoa', 'HOA', 50, ['pre' => '$', 'suf' => '/mo', 'step' => 5]) ?>
    <?= fld('appr', 'Home appreciation', 3, ['suf' => '%/yr', 'step' => 0.25]) ?>
    </fieldset>
    <fieldset><legend>Renting</legend>
    <?= fld('rent', 'Monthly rent', 2100, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('rentinc', 'Annual rent increase', 3, ['suf' => '%', 'step' => 0.25]) ?>
    <?= fld('invest', 'Investment return', 6, ['suf' => '%/yr', 'step' => 0.25, 'help' => 'What the renter earns investing the savings.']) ?>
    <?= fld('years', 'Years you plan to stay', 7, ['step' => 1, 'min' => 1, 'max' => 30]) ?>
    </fieldset>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('verdict', 'After your time frame', true) ?>
    <div class="stats">
      <?= out('buynet', 'Net wealth if you buy') ?>
      <?= out('rentnet', 'Net wealth if you rent') ?>
      <?= out('breakeven', 'Break-even year') ?>
      <?= out('ownmonthly', 'Year-1 owner cost / mo') ?>
    </div>
    <div class="chart" data-out-chart="wealth" role="img" aria-label="Net wealth by year, buying versus renting"></div>
  </div>
</form>
<?php break;
    case 'closing-cost-calculator': ?>
<form class="calc" data-tool="closing-cost-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('price', 'Purchase price', 350000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('down', 'Down payment', 10, ['suf' => '%', 'step' => 0.5]) ?>
    <?= sel('loan', 'Loan type', ['conv' => 'Conventional', 'fha' => 'FHA', 'va' => 'VA', 'cash' => 'Cash purchase'], 'conv') ?>
    <?= fld('orig', 'Origination / lender fees', 1, ['suf' => '% of loan', 'step' => 0.125]) ?>
    <?= fld('appraisal', 'Appraisal', 600, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('survey', 'Survey', 500, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('inspection', 'Home inspection', 500, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('escrowfee', 'Escrow / settlement fee', 650, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('ins', 'Annual homeowners insurance', 3200, ['pre' => '$', 'step' => 50]) ?>
    <?= fld('tax', 'Property tax rate', 2.2, ['suf' => '%/yr', 'step' => 0.05]) ?>
    <?= sel('ownerpolicy', 'Owner\'s title policy paid by', ['seller' => 'Seller (common in Texas)', 'buyer' => 'Buyer'], 'seller') ?>
    <?= fld('credit', 'Seller credit / concessions', 0, ['pre' => '$', 'step' => 500]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('cashclose', 'Estimated cash to close', true) ?>
    <div class="stats">
      <?= out('closing', 'Closing costs') ?>
      <?= out('pct', 'As % of price') ?>
      <?= out('downamt', 'Down payment') ?>
      <?= out('loanamt', 'Loan amount') ?>
    </div>
    <div class="table-wrap" data-out-table="lines"></div>
  </div>
</form>
<?php break;
    case 'seller-net-proceeds-calculator': ?>
<form class="calc" data-tool="seller-net-proceeds-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('price', 'Expected sale price', 400000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('payoff', 'Mortgage payoff balance', 220000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('listcomm', 'Listing agent commission', 3, ['suf' => '%', 'step' => 0.25]) ?>
    <?= fld('buycomm', 'Buyer agent compensation (if offered)', 2.5, ['suf' => '%', 'step' => 0.25]) ?>
    <?= fld('taxbill', 'Annual property tax bill', 8800, ['pre' => '$', 'step' => 100]) ?>
    <?= sel('month', 'Closing month', array_combine(range(1, 12), ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']), (int) date('n')) ?>
    <?= fld('repairs', 'Repairs & prep', 3000, ['pre' => '$', 'step' => 250]) ?>
    <?= fld('concessions', 'Buyer concessions', 4000, ['pre' => '$', 'step' => 250]) ?>
    <?= fld('other', 'Other fees (HOA transfer, survey, attorney)', 1200, ['pre' => '$', 'step' => 50]) ?>
    <?= sel('ownerpolicy', 'Owner\'s title policy', ['seller' => 'Seller pays (common)', 'buyer' => 'Buyer pays'], 'seller') ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('net', 'Estimated net proceeds', true) ?>
    <div class="stats">
      <?= out('costs', 'Total selling costs') ?>
      <?= out('costpct', 'Costs as % of price') ?>
      <?= out('comm', 'Commissions') ?>
      <?= out('prorate', 'Tax proration credit') ?>
    </div>
    <div class="table-wrap" data-out-table="lines"></div>
  </div>
</form>
<?php break;
    case 'rental-property-calculator': ?>
<form class="calc" data-tool="rental-property-calculator" novalidate>
  <div class="calc__inputs">
    <fieldset><legend>Purchase & loan</legend>
    <?= fld('price', 'Purchase price', 250000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('closing', 'Closing costs', 7500, ['pre' => '$', 'step' => 250]) ?>
    <?= fld('rehab', 'Repairs / rehab', 10000, ['pre' => '$', 'step' => 500]) ?>
    <?= fld('down', 'Down payment', 25, ['suf' => '%', 'step' => 1]) ?>
    <?= fld('rate', 'Interest rate', 7.25, ['suf' => '%', 'step' => 0.125]) ?>
    <?= sel('term', 'Loan term', [30 => '30 years', 15 => '15 years'], 30) ?>
    </fieldset>
    <fieldset><legend>Income & expenses</legend>
    <?= fld('rent', 'Monthly rent', 2200, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('other', 'Other income', 0, ['pre' => '$', 'suf' => '/mo', 'step' => 10]) ?>
    <?= fld('vacancy', 'Vacancy', 6, ['suf' => '%', 'step' => 1]) ?>
    <?= fld('tax', 'Property tax', 5500, ['pre' => '$', 'suf' => '/yr', 'step' => 100, 'help' => 'No homestead exemption on rentals.']) ?>
    <?= fld('ins', 'Landlord insurance', 2400, ['pre' => '$', 'suf' => '/yr', 'step' => 50]) ?>
    <?= fld('hoa', 'HOA', 0, ['pre' => '$', 'suf' => '/mo', 'step' => 5]) ?>
    <?= fld('mgmt', 'Property management', 8, ['suf' => '% of rent', 'step' => 0.5]) ?>
    <?= fld('repairs', 'Repairs & maintenance', 5, ['suf' => '% of rent', 'step' => 0.5]) ?>
    <?= fld('capex', 'CapEx reserve', 5, ['suf' => '% of rent', 'step' => 0.5]) ?>
    <?= fld('utils', 'Owner-paid utilities', 0, ['pre' => '$', 'suf' => '/mo', 'step' => 10]) ?>
    </fieldset>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('cashflow', 'Monthly cash flow', true) ?>
    <div class="stats">
      <?= out('noi', 'Net operating income (yr)') ?>
      <?= out('cap', 'Cap rate') ?>
      <?= out('coc', 'Cash-on-cash return') ?>
      <?= out('dscr', 'DSCR') ?>
      <?= out('cashin', 'Total cash invested') ?>
      <?= out('pi', 'Mortgage (P&I) / mo') ?>
      <?= out('onepct', '1% rule') ?>
      <?= out('grm', 'Gross rent multiplier') ?>
    </div>
    <div class="table-wrap" data-out-table="lines"></div>
  </div>
</form>
<?php break;
    case 'refinance-calculator': ?>
<form class="calc" data-tool="refinance-calculator" novalidate>
  <div class="calc__inputs">
    <fieldset><legend>Current loan</legend>
    <?= fld('balance', 'Current balance', 280000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('currate', 'Current rate', 7.5, ['suf' => '%', 'step' => 0.125]) ?>
    <?= fld('remaining', 'Years remaining', 27, ['step' => 1, 'min' => 1, 'max' => 40]) ?>
    </fieldset>
    <fieldset><legend>New loan</legend>
    <?= fld('newrate', 'New rate', 6.25, ['suf' => '%', 'step' => 0.125]) ?>
    <?= sel('newterm', 'New term', [30 => '30 years', 25 => '25 years', 20 => '20 years', 15 => '15 years', 10 => '10 years'], 30) ?>
    <?= fld('costs', 'Refinance closing costs', 6000, ['pre' => '$', 'step' => 250]) ?>
    <?= sel('roll', 'Pay closing costs', ['cash' => 'In cash', 'roll' => 'Roll into loan'], 'cash') ?>
    </fieldset>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('savings', 'Monthly savings', true) ?>
    <div class="stats">
      <?= out('oldpay', 'Current payment (P&I)') ?>
      <?= out('newpay', 'New payment (P&I)') ?>
      <?= out('breakeven', 'Break-even') ?>
      <?= out('interestdiff', 'Lifetime interest change') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'extra-payment-calculator': ?>
<form class="calc" data-tool="extra-payment-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('balance', 'Loan balance', 300000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('rate', 'Interest rate', 6.75, ['suf' => '%', 'step' => 0.125]) ?>
    <?= fld('remaining', 'Years remaining', 30, ['step' => 1, 'min' => 1, 'max' => 40]) ?>
    <?= fld('extram', 'Extra each month', 200, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('extray', 'Extra once a year', 0, ['pre' => '$', 'step' => 100]) ?>
    <?= fld('lump', 'One-time lump sum now', 0, ['pre' => '$', 'step' => 500]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('saved', 'Interest saved', true) ?>
    <div class="stats">
      <?= out('timesaved', 'Time saved') ?>
      <?= out('newpayoff', 'New payoff') ?>
      <?= out('payment', 'Regular payment (P&I)') ?>
      <?= out('totalint', 'Total interest with extra') ?>
    </div>
    <div class="chart" data-out-chart="balance" role="img" aria-label="Loan balance over time with and without extra payments"></div>
  </div>
</form>
<?php break;
    case 'dti-calculator': ?>
<form class="calc" data-tool="dti-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('income', 'Gross monthly income', 7500, ['pre' => '$', 'step' => 100, 'help' => 'Before taxes, all borrowers combined.']) ?>
    <?= fld('housing', 'Proposed housing payment (PITI + HOA)', 2300, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('car', 'Car loans / leases', 450, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('student', 'Student loans', 250, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('cards', 'Credit card minimums', 100, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('otherdebt', 'Other debts (personal loans, support)', 0, ['pre' => '$', 'step' => 25]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('back', 'Back-end DTI', true) ?>
    <div class="stats">
      <?= out('front', 'Front-end (housing) DTI') ?>
      <?= out('totaldebt', 'Total monthly debts') ?>
    </div>
    <div class="table-wrap" data-out-table="limits"></div>
  </div>
</form>
<?php break;
    case 'texas-property-tax-calculator': ?>
<form class="calc" data-tool="texas-property-tax-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('value', 'Appraised value', 350000, ['pre' => '$', 'step' => 1000]) ?>
    <?= sel('homestead', 'Homestead exemption', ['1' => 'Yes - my primary residence', '0' => 'No (rental / second home)'], '1') ?>
    <?= sel('senior', 'Age 65+ or disabled', ['0' => 'No', '1' => 'Yes'], '0') ?>
    <?= fld('school', 'School district rate', 1.0, ['suf' => '%', 'step' => 0.01]) ?>
    <?= fld('county', 'County rate', 0.39, ['suf' => '%', 'step' => 0.01]) ?>
    <?= fld('city', 'City rate', 0.52, ['suf' => '%', 'step' => 0.01]) ?>
    <?= fld('other', 'Other (MUD, college, hospital, flood)', 0.35, ['suf' => '%', 'step' => 0.01]) ?>
    <?= fld('localpct', 'Local optional homestead exemption', 20, ['suf' => '% of value', 'step' => 1, 'max' => 20, 'help' => 'Counties and cities may offer up to 20%. Check your appraisal district.']) ?>
    <?= fld('localsenior', 'Local over-65 exemption (county/city)', 0, ['pre' => '$', 'step' => 1000]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('total', 'Estimated annual property tax', true) ?>
    <div class="stats">
      <?= out('monthly', 'Per month (escrow)') ?>
      <?= out('effective', 'Effective tax rate') ?>
      <?= out('saved', 'Saved by exemptions') ?>
      <?= out('noexempt', 'Bill with no exemptions') ?>
    </div>
    <div class="table-wrap" data-out-table="lines"></div>
  </div>
</form>
<?php break;
    case 'insurance-claim-depreciation-calculator': ?>
<form class="calc calc--wide" data-tool="insurance-claim-depreciation-calculator" novalidate>
  <div class="calc__inputs calc__inputs--full">
    <div class="items" data-items>
      <div class="items__head" aria-hidden="true"><span>Item or component</span><span>Replacement cost</span><span>Age (yrs)</span><span>Useful life (yrs)</span><span></span></div>
    </div>
    <div class="items__actions">
      <button type="button" class="btn btn--ghost" data-add-item>+ Add item</button>
      <?= sel('preset', 'Quick add', ['' => 'Choose a common item...', 'Asphalt shingle roof|18000|10|25' => 'Asphalt shingle roof', 'Carpet (per room)|1800|6|10' => 'Carpet', 'Interior paint (whole house)|6500|5|8' => 'Interior paint', 'HVAC system|9500|8|18' => 'HVAC system', 'Water heater|1800|7|12' => 'Water heater', 'Refrigerator|2200|5|13' => 'Refrigerator', 'Television|900|3|7' => 'Television', 'Sofa|1600|6|12' => 'Sofa', 'Laptop|1200|2|5' => 'Laptop', 'Hardwood flooring|9000|12|40' => 'Hardwood flooring', 'Drywall & insulation|4500|15|50' => 'Drywall & insulation', 'Kitchen cabinets|12000|15|25' => 'Kitchen cabinets']) ?>
    </div>
    <div class="row-2">
      <?= fld('deductible', 'Deductible', 2500, ['pre' => '$', 'step' => 100]) ?>
      <?= fld('maxdep', 'Maximum depreciation', 80, ['suf' => '%', 'step' => 5, 'max' => 100, 'help' => 'Most estimates cap depreciation; adjust to match yours.']) ?>
      <?= sel('policy', 'Loss settlement', ['rcv' => 'Replacement cost (RCV)', 'acv' => 'Actual cash value only (ACV)'], 'rcv') ?>
    </div>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('first', 'First payment (ACV less deductible)', true) ?>
    <div class="stats">
      <?= out('rcv', 'Replacement cost (RCV)') ?>
      <?= out('dep', 'Total depreciation') ?>
      <?= out('acv', 'Actual cash value (ACV)') ?>
      <?= out('recoverable', 'Recoverable after repairs') ?>
      <?= out('totalpay', 'Total if fully recovered') ?>
    </div>
  </div>
</form>
<?php break;
    case 'hurricane-prep-checklist':
        $lists = [
            'Insurance & paperwork (do this first)' => [
                'Read your declarations page: dwelling, contents, ALE/loss-of-use limits',
                'Know your hurricane / windstorm deductible in dollars, not just percent',
                'Buy flood insurance (NFIP or private) - new NFIP policies usually wait 30 days',
                'Check whether you need a TWIA windstorm policy (coastal counties)',
                'Video every room, closet, the garage, attic and exterior; upload to the cloud',
                'Photograph receipts and serial numbers for big-ticket items',
                'Save your insurer\'s claim phone number and policy number in your phone',
                'Put deeds, policies, IDs and cash in a waterproof grab bag',
            ],
            'Supplies for at least 7 days' => [
                'Water: 1 gallon per person per day, plus pets',
                'Non-perishable food and a manual can opener',
                'Prescriptions refilled, first-aid kit, glasses/contacts',
                'Flashlights, extra batteries, NOAA weather radio',
                'Phone power banks or a portable power station',
                'Cash in small bills (ATMs and card readers go down)',
                'Fill vehicles with gas and get propane / generator fuel',
                'Trash bags, bleach, gloves, N95 masks for cleanup',
                'Tarps, duct tape, plastic sheeting',
            ],
            'Protect the house' => [
                'Clear gutters, downspouts and storm drains near your home',
                'Trim dead limbs and branches overhanging the roof',
                'Bring in or tie down patio furniture, grills, trampolines, planters',
                'Install shutters or pre-cut plywood on windows',
                'Brace garage doors (the most common wind failure point)',
                'Move valuables and electronics off the floor and to upper levels',
                'Place flood barriers or sandbags at low doorways if you are flood-prone',
                'Know how to shut off main water, gas and electricity',
                'Set fridge and freezer to coldest settings; freeze water jugs',
            ],
            'Evacuation plan' => [
                'Look up your evacuation zone (Know Your Zone) and route',
                'Pick a meeting place and an out-of-area contact',
                'Plan for pets: carriers, food, vaccination records',
                'Pack a go-bag for each person',
                'Leave early if officials call for evacuation in your zone',
            ],
            'After the storm' => [
                'Stay out of floodwater and away from downed lines',
                'Never run a generator indoors or in the garage',
                'Photograph and video all damage before cleanup',
                'Report the claim promptly and write down your claim number',
                'Make temporary repairs (tarp, board-up, water extraction) and keep receipts',
                'Do not throw away damaged items until the adjuster sees them or you have photos',
                'Get repair estimates from licensed, local contractors - avoid door-to-door storm chasers',
                'Keep a log of every call, email and expense, including hotel and meals (ALE)',
            ],
        ];
        $i = 0; ?>
<div class="checklist" data-tool="hurricane-prep-checklist">
  <div class="checklist__progress"><div class="progress"><span data-progress-bar></span></div><p><strong data-progress-text>0 of 0</strong> tasks done <button type="button" class="linkbtn" data-reset>Reset</button> <button type="button" class="linkbtn" data-print>Print</button></p></div>
<?php foreach ($lists as $head => $items): ?>
  <fieldset class="checklist__group"><legend><?= e($head) ?></legend>
<?php foreach ($items as $it): $i++; ?>
    <label class="check"><input type="checkbox" data-id="h<?= $i ?>"><span><?= e($it) ?></span></label>
<?php endforeach; ?>
  </fieldset>
<?php endforeach; ?>
</div>
<?php break;
    }
    return ob_get_clean();
}
