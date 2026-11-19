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
    case 'fha-loan-calculator': ?>
<form class="calc" data-tool="fha-loan-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('price', 'Home price', 300000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('down', 'Down payment', 3.5, ['suf' => '%', 'step' => 0.5, 'min' => 3.5, 'help' => 'FHA minimum is 3.5% with a 580+ credit score.']) ?>
    <?= fld('rate', 'Interest rate', 6.25, ['suf' => '%', 'step' => 0.125]) ?>
    <?= sel('term', 'Loan term', [30 => '30 years', 15 => '15 years'], 30) ?>
    <?= fld('tax', 'Property tax rate', 2.2, ['suf' => '%/yr', 'step' => 0.05]) ?>
    <?= fld('ins', 'Homeowners insurance', 3000, ['pre' => '$', 'suf' => '/yr', 'step' => 50]) ?>
    <?= fld('hoa', 'HOA dues', 0, ['pre' => '$', 'suf' => '/mo', 'step' => 5]) ?>
    <?= fld('limit', 'County FHA loan limit', 541287, ['pre' => '$', 'step' => 1, 'help' => '2026 one-unit limit for Harris and surrounding counties.']) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('total', 'Estimated monthly payment', true) ?>
    <div class="bars" data-out-bars="breakdown"></div>
    <div class="stats">
      <?= out('base', 'Base loan') ?>
      <?= out('ufmip', 'Upfront MIP (1.75%)') ?>
      <?= out('loan', 'Total loan with UFMIP') ?>
      <?= out('miprate', 'Annual MIP rate') ?>
      <?= out('mipdur', 'MIP lasts') ?>
      <?= out('cash', 'Down payment') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'va-loan-calculator': ?>
<form class="calc" data-tool="va-loan-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('price', 'Home price', 350000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('down', 'Down payment', 0, ['suf' => '%', 'step' => 0.5]) ?>
    <?= fld('rate', 'Interest rate', 6.0, ['suf' => '%', 'step' => 0.125]) ?>
    <?= sel('term', 'Loan term', [30 => '30 years', 15 => '15 years'], 30) ?>
    <?= sel('use', 'VA loan use', ['first' => 'First use', 'subsequent' => 'After first use'], 'first') ?>
    <?= sel('exempt', 'Funding fee exempt?', ['0' => 'No', '1' => 'Yes (VA disability, DIC, Purple Heart)'], '0') ?>
    <?= fld('tax', 'Property tax rate', 2.2, ['suf' => '%/yr', 'step' => 0.05]) ?>
    <?= fld('ins', 'Homeowners insurance', 3200, ['pre' => '$', 'suf' => '/yr', 'step' => 50]) ?>
    <?= fld('hoa', 'HOA dues', 0, ['pre' => '$', 'suf' => '/mo', 'step' => 5]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('total', 'Estimated monthly payment', true) ?>
    <div class="bars" data-out-bars="breakdown"></div>
    <div class="stats">
      <?= out('feepct', 'Funding fee rate') ?>
      <?= out('fee', 'Funding fee (financed)') ?>
      <?= out('loan', 'Total loan') ?>
      <?= out('pi', 'Principal & interest') ?>
      <?= out('cash', 'Down payment') ?>
      <?= out('pmi', 'Monthly mortgage insurance') ?>
    </div>
  </div>
</form>
<?php break;
    case 'down-payment-calculator': ?>
<form class="calc" data-tool="down-payment-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('price', 'Target home price', 320000, ['pre' => '$', 'step' => 1000]) ?>
    <?= sel('loan', 'Loan type', ['conv20' => 'Conventional, 20% (no PMI)', 'conv5' => 'Conventional, 5%', 'conv3' => 'Conventional, 3% (first-time)', 'fha' => 'FHA, 3.5%', 'va' => 'VA, 0%', 'usda' => 'USDA, 0%', 'custom' => 'Custom percentage'], 'fha') ?>
    <?= fld('custom', 'Custom down payment', 10, ['suf' => '%', 'step' => 0.5]) ?>
    <?= fld('closing', 'Closing costs', 3, ['suf' => '% of price', 'step' => 0.25]) ?>
    <?= fld('assist', 'Assistance / gifts / seller credits', 0, ['pre' => '$', 'step' => 500]) ?>
    <?= fld('saved', 'Saved so far', 8000, ['pre' => '$', 'step' => 500]) ?>
    <?= fld('monthly', 'You can save each month', 750, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('ret', 'Savings interest rate', 4, ['suf' => '%/yr', 'step' => 0.25]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('need', 'Cash you need at closing', true) ?>
    <div class="stats">
      <?= out('down', 'Down payment') ?>
      <?= out('cc', 'Closing costs') ?>
      <?= out('gap', 'Still to save') ?>
      <?= out('time', 'Time to save') ?>
      <?= out('date', 'Ready by') ?>
      <?= out('loanamt', 'Loan amount') ?>
    </div>
    <div class="table-wrap" data-out-table="types"></div>
  </div>
</form>
<?php break;
    case 'rent-affordability-calculator': ?>
<form class="calc" data-tool="rent-affordability-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('gross', 'Gross annual income', 60000, ['pre' => '$', 'step' => 1000, 'help' => 'Before taxes, all earners on the lease.']) ?>
    <?= fld('net', 'Monthly take-home pay', 3900, ['pre' => '$', 'step' => 50]) ?>
    <?= fld('debts', 'Monthly debt payments', 350, ['pre' => '$', 'step' => 25, 'help' => 'Car, student loans, minimum card payments.']) ?>
    <?= fld('utils', 'Utilities you pay', 200, ['pre' => '$', 'suf' => '/mo', 'step' => 10, 'help' => 'Electric, water, internet, renters insurance.']) ?>
    <?= fld('groceries', 'Groceries & essentials', 450, ['pre' => '$', 'suf' => '/mo', 'step' => 25]) ?>
    <?= fld('multiple', 'Landlord income requirement', 3, ['suf' => 'x rent', 'step' => 0.5, 'min' => 1]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('target', 'Comfortable rent target', true) ?>
    <div class="stats">
      <?= out('r30', '30% rule (incl. utilities)') ?>
      <?= out('r503020', '50/30/20 budget') ?>
      <?= out('rland', 'Landlord income test') ?>
      <?= out('pct', 'Target as % of gross') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'home-equity-calculator': ?>
<form class="calc" data-tool="home-equity-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('value', 'Home value', 400000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('balance', 'Mortgage balance(s)', 220000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('cltv', 'Max combined loan-to-value', 80, ['suf' => '%', 'step' => 1, 'max' => 100, 'help' => 'Texas homestead limit is 80%.']) ?>
    <?= fld('draw', 'Amount you want to borrow', 50000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('rate', 'HELOC interest rate', 8.25, ['suf' => '%', 'step' => 0.125]) ?>
    <?= fld('drawyrs', 'Draw period', 10, ['suf' => 'years', 'step' => 1, 'min' => 1]) ?>
    <?= fld('repyrs', 'Repayment period', 20, ['suf' => 'years', 'step' => 1, 'min' => 1]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('avail', 'You may be able to borrow up to', true) ?>
    <div class="stats">
      <?= out('equity', 'Total equity') ?>
      <?= out('equitypct', 'Equity %') ?>
      <?= out('io', 'Interest-only payment (draw)') ?>
      <?= out('amort', 'Repayment-period payment') ?>
      <?= out('newcltv', 'Combined LTV after draw') ?>
      <?= out('totalint', 'Total interest (est.)') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'cash-out-refinance-calculator': ?>
<form class="calc" data-tool="cash-out-refinance-calculator" novalidate>
  <div class="calc__inputs">
    <fieldset><legend>Today</legend>
    <?= fld('value', 'Home value', 400000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('balance', 'Current loan balance', 220000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('currate', 'Current rate', 4.5, ['suf' => '%', 'step' => 0.125]) ?>
    <?= fld('remaining', 'Years remaining', 24, ['step' => 1, 'min' => 1]) ?>
    </fieldset>
    <fieldset><legend>New loan</legend>
    <?= fld('cash', 'Cash you want', 60000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('ltv', 'Max loan-to-value', 80, ['suf' => '%', 'step' => 1, 'help' => 'Texas homestead cash-out cap is 80%.']) ?>
    <?= fld('newrate', 'New rate', 6.5, ['suf' => '%', 'step' => 0.125]) ?>
    <?= sel('term', 'New term', [30 => '30 years', 20 => '20 years', 15 => '15 years'], 30) ?>
    <?= fld('costs', 'Closing costs', 2.5, ['suf' => '% of loan', 'step' => 0.25]) ?>
    </fieldset>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('cashout', 'Cash in hand', true) ?>
    <div class="stats">
      <?= out('maxcash', 'Maximum cash available') ?>
      <?= out('newloan', 'New loan amount') ?>
      <?= out('newpay', 'New payment (P&I)') ?>
      <?= out('oldpay', 'Current payment (P&I)') ?>
      <?= out('diff', 'Monthly change') ?>
      <?= out('ltvafter', 'Loan-to-value') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'capital-gains-tax-calculator': ?>
<form class="calc" data-tool="capital-gains-tax-calculator" novalidate>
  <div class="calc__inputs">
    <fieldset><legend>The sale</legend>
    <?= fld('sale', 'Sale price', 550000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('sellcost', 'Selling costs', 35000, ['pre' => '$', 'step' => 500, 'help' => 'Commissions, title, fees, concessions.']) ?>
    </fieldset>
    <fieldset><legend>Your basis</legend>
    <?= fld('purchase', 'Original purchase price', 240000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('buycost', 'Purchase closing costs (eligible)', 4000, ['pre' => '$', 'step' => 250]) ?>
    <?= fld('improve', 'Capital improvements', 30000, ['pre' => '$', 'step' => 500]) ?>
    <?= fld('dep', 'Depreciation claimed (rental / office)', 0, ['pre' => '$', 'step' => 500]) ?>
    </fieldset>
    <fieldset><legend>You</legend>
    <?= sel('status', 'Filing status', ['single' => 'Single', 'mfj' => 'Married filing jointly', 'hoh' => 'Head of household', 'mfs' => 'Married filing separately'], 'mfj') ?>
    <?= sel('qualify', 'Owned & lived in it 2 of last 5 years?', ['1' => 'Yes', '0' => 'No'], '1') ?>
    <?= sel('held', 'Owned more than one year?', ['1' => 'Yes', '0' => 'No'], '1') ?>
    <?= fld('income', 'Other taxable income', 120000, ['pre' => '$', 'step' => 1000, 'help' => 'Taxable income before this sale.']) ?>
    </fieldset>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('tax', 'Estimated federal tax', true) ?>
    <div class="stats">
      <?= out('basis', 'Adjusted basis') ?>
      <?= out('gain', 'Total gain') ?>
      <?= out('excl', 'Excluded (Sec. 121)') ?>
      <?= out('taxable', 'Taxable gain') ?>
      <?= out('niit', 'Incl. 3.8% NIIT') ?>
      <?= out('eff', 'Effective rate on gain') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'cap-rate-calculator': ?>
<form class="calc" data-tool="cap-rate-calculator" novalidate>
  <div class="calc__inputs">
    <?= fld('price', 'Purchase price / value', 400000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('rent', 'Gross monthly rent', 3200, ['pre' => '$', 'step' => 25]) ?>
    <?= fld('other', 'Other monthly income', 0, ['pre' => '$', 'step' => 10]) ?>
    <?= fld('vacancy', 'Vacancy & credit loss', 6, ['suf' => '%', 'step' => 1]) ?>
    <?= fld('tax', 'Property tax', 8800, ['pre' => '$', 'suf' => '/yr', 'step' => 100]) ?>
    <?= fld('ins', 'Insurance', 3000, ['pre' => '$', 'suf' => '/yr', 'step' => 50]) ?>
    <?= fld('mgmt', 'Management', 8, ['suf' => '% of rent', 'step' => 0.5]) ?>
    <?= fld('maint', 'Repairs & reserves', 10, ['suf' => '% of rent', 'step' => 0.5]) ?>
    <?= fld('opother', 'Other expenses (HOA, utilities)', 0, ['pre' => '$', 'suf' => '/yr', 'step' => 100]) ?>
    <?= fld('target', 'Your target cap rate', 6.5, ['suf' => '%', 'step' => 0.25]) ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('cap', 'Cap rate', true) ?>
    <div class="stats">
      <?= out('noi', 'Net operating income') ?>
      <?= out('egi', 'Effective gross income') ?>
      <?= out('opex', 'Operating expenses') ?>
      <?= out('ratio', 'Expense ratio') ?>
      <?= out('value', 'Value at target cap rate') ?>
      <?= out('vsprice', 'vs. price') ?>
    </div>
  </div>
</form>
<?php break;
    case 'house-flipping-calculator': ?>
<form class="calc" data-tool="house-flipping-calculator" novalidate>
  <div class="calc__inputs">
    <fieldset><legend>Deal</legend>
    <?= fld('arv', 'After-repair value (ARV)', 360000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('price', 'Purchase price', 220000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('rehab', 'Rehab budget', 45000, ['pre' => '$', 'step' => 500]) ?>
    <?= fld('contingency', 'Contingency', 10, ['suf' => '% of rehab', 'step' => 1]) ?>
    <?= fld('months', 'Months held', 5, ['step' => 1, 'min' => 1]) ?>
    </fieldset>
    <fieldset><legend>Costs & financing</legend>
    <?= fld('buyclose', 'Buying closing costs', 2, ['suf' => '% of price', 'step' => 0.25]) ?>
    <?= fld('hold', 'Taxes, insurance, utilities', 650, ['pre' => '$', 'suf' => '/mo', 'step' => 25]) ?>
    <?= fld('sellcost', 'Selling costs', 8, ['suf' => '% of ARV', 'step' => 0.25]) ?>
    <?= fld('ltc', 'Loan amount', 85, ['suf' => '% of price+rehab', 'step' => 5, 'help' => 'Set to 0 for an all-cash deal.']) ?>
    <?= fld('rate', 'Loan interest rate', 11, ['suf' => '%', 'step' => 0.25]) ?>
    <?= fld('points', 'Loan points', 2, ['suf' => '%', 'step' => 0.25]) ?>
    </fieldset>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('profit', 'Projected net profit', true) ?>
    <div class="stats">
      <?= out('mao', 'Max offer (70% rule)') ?>
      <?= out('allin', 'All-in cost') ?>
      <?= out('cash', 'Cash needed') ?>
      <?= out('roi', 'Return on cash') ?>
      <?= out('annual', 'Annualized return') ?>
      <?= out('margin', 'Profit as % of ARV') ?>
    </div>
    <div class="table-wrap" data-out-table="lines"></div>
  </div>
</form>
<?php break;
    case '1031-exchange-calculator': ?>
<form class="calc" data-tool="1031-exchange-calculator" novalidate>
  <div class="calc__inputs">
    <label class="fld"><span class="fld__label">Sale (relinquished property) closing date</span><span class="fld__input"><input type="date" name="closedate" id="f-closedate" value="<?= date('Y-m-d') ?>"></span></label>
    <?= fld('sale', 'Sale price', 600000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('sellcost', 'Selling costs', 40000, ['pre' => '$', 'step' => 500]) ?>
    <?= fld('basis', 'Adjusted basis (after depreciation)', 300000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('dep', 'Depreciation taken', 80000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('oldloan', 'Mortgage paid off at sale', 250000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('newprice', 'Replacement property price', 650000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('newloan', 'New mortgage on replacement', 330000, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('keep', 'Cash you keep (not reinvested)', 0, ['pre' => '$', 'step' => 1000]) ?>
    <?= fld('cgrate', 'Your capital gains rate', 15, ['suf' => '%', 'step' => 1]) ?>
    <?= sel('niit', 'Subject to 3.8% NIIT?', ['0' => 'No', '1' => 'Yes'], '0') ?>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('deferred', 'Estimated tax deferred', true) ?>
    <div class="stats">
      <?= out('day45', 'Identify by (day 45)') ?>
      <?= out('day180', 'Close by (day 180)') ?>
      <?= out('realized', 'Realized gain') ?>
      <?= out('boot', 'Taxable boot') ?>
      <?= out('taxnow', 'Tax due now (est.)') ?>
      <?= out('taxsale', 'Tax with no exchange') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'price-per-square-foot-calculator': ?>
<form class="calc calc--wide" data-tool="price-per-square-foot-calculator" novalidate>
  <div class="calc__inputs calc__inputs--full">
    <div class="row-2">
      <?= fld('sqft', 'Your home\'s living area', 2100, ['suf' => 'sq ft', 'step' => 10]) ?>
      <?= fld('compare', 'Value to compare (list price or appraisal district value)', 395000, ['pre' => '$', 'step' => 1000]) ?>
    </div>
    <div class="items items--comps" data-comps>
      <div class="items__head" aria-hidden="true"><span>Comparable (address or note)</span><span>Sale price</span><span>Living sq ft</span><span>$/sq ft</span></div>
<?php foreach ([['123 Oak St', 372000, 1980], ['456 Elm Dr', 401000, 2250], ['789 Pine Ln', 355000, 1900], ['', '', ''], ['', '', ''], ['', '', '']] as $c): ?>
      <div class="items__row"><input type="text" aria-label="Comparable" placeholder="Address or note" value="<?= e($c[0]) ?>"><input type="number" inputmode="decimal" aria-label="Sale price" min="0" step="500" value="<?= e($c[1]) ?>"><input type="number" inputmode="decimal" aria-label="Living square feet" min="0" step="10" value="<?= e($c[2]) ?>"><output class="items__ppsf">-</output></div>
<?php endforeach; ?>
    </div>
  </div>
  <div class="calc__results" aria-live="polite">
    <?= out('indicated', 'Value implied by median comp $/sq ft', true) ?>
    <div class="stats">
      <?= out('median', 'Median $/sq ft') ?>
      <?= out('avg', 'Average $/sq ft') ?>
      <?= out('yours', 'Your value per sq ft') ?>
      <?= out('diff', 'Difference vs. your value') ?>
    </div>
    <p class="calc__note" data-out="note"></p>
  </div>
</form>
<?php break;
    case 'moving-checklist':
        $lists = [
            '6-8 weeks before' => [
                'Set a moving budget and date; get at least three moving quotes',
                'Check each mover\'s USDOT number (interstate) or Texas DMV registration (in-state)',
                'Ask how movers cover damage: full value protection vs. minimum per-pound liability',
                'Declutter: sell, donate or toss what you will not move',
                'Request school records and find new doctors, dentists and vets',
                'Start a moving folder for quotes, receipts and contracts',
            ],
            '3-4 weeks before' => [
                'Book movers or a truck and reserve elevators or parking if needed',
                'Buy boxes, tape, markers and furniture pads',
                'Photograph valuables and electronics before packing (also great for insurance)',
                'Submit a USPS change of address',
                'Schedule utility shutoff at your old home and setup at your new one',
                'Choose a retail electricity plan for the new address (Houston is a deregulated market)',
                'Set up internet installation for move-in day',
                'Update your homeowners or renters insurance to start at the new address',
            ],
            '1-2 weeks before' => [
                'Pack room by room and label boxes with room and contents',
                'Confirm the moving date, time and arrival window in writing',
                'Refill prescriptions and pack an essentials box (meds, chargers, documents, snacks)',
                'Update your address with banks, employer, subscriptions and insurers',
                'Arrange childcare and pet care for moving day',
                'Defrost and clean the refrigerator if you are moving it',
            ],
            'Moving day' => [
                'Keep documents, keys, valuables and medications with you',
                'Walk the movers through the home and point out fragile items',
                'Read the inventory and bill of lading before signing',
                'Do a final walk-through: closets, attic, garage, cabinets',
                'Photograph the empty home and record meter readings',
            ],
            'First 30-90 days (Texas)' => [
                'Inspect your belongings and file any damage claim with the mover promptly',
                'Change or rekey the locks',
                'Find the main water shutoff, breaker panel and gas shutoff',
                'Test smoke and carbon monoxide alarms; replace HVAC filters',
                'New to Texas: register your vehicle (generally within 30 days of moving)',
                'New to Texas: get a Texas driver license (generally within 90 days)',
                'Update your voter registration',
                'Homeowners: file your homestead exemption with the county appraisal district',
                'Homeowners: look up your MUD, HOA and flood zone details',
                'Review your flood insurance needs (NFIP policies usually have a 30-day wait)',
            ],
        ];
        $i = 0; ?>
<div class="checklist" data-tool="moving-checklist">
  <div class="checklist__progress"><div class="progress"><span data-progress-bar></span></div><p><strong data-progress-text>0 of 0</strong> tasks done <button type="button" class="linkbtn" data-reset>Reset</button> <button type="button" class="linkbtn" data-print>Print</button></p></div>
<?php foreach ($lists as $head => $items): ?>
  <fieldset class="checklist__group"><legend><?= e($head) ?></legend>
<?php foreach ($items as $it): $i++; ?>
    <label class="check"><input type="checkbox" data-id="m<?= $i ?>"><span><?= e($it) ?></span></label>
<?php endforeach; ?>
  </fieldset>
<?php endforeach; ?>
</div>
<?php break;
    case 'home-inventory-checklist': ?>
<div class="inventory" data-tool="home-inventory-checklist">
  <div class="inventory__bar">
    <label class="fld"><span class="fld__label">Room</span><span class="fld__input"><select data-room>
      <?php foreach (['Living room', 'Kitchen', 'Dining room', 'Primary bedroom', 'Bedroom 2', 'Bedroom 3', 'Bathrooms', 'Home office', 'Laundry', 'Garage', 'Attic / storage', 'Outdoor / patio', 'Closets', 'Other'] as $r): ?><option><?= e($r) ?></option><?php endforeach; ?>
    </select></span></label>
    <div class="inventory__actions">
      <button type="button" class="btn btn--primary" data-add>+ Add item</button>
      <button type="button" class="btn btn--ghost" data-csv>Export CSV</button>
      <button type="button" class="btn btn--ghost" data-print>Print</button>
      <button type="button" class="linkbtn" data-clear>Clear all</button>
    </div>
  </div>
  <div class="inventory__summary" aria-live="polite"><div class="stat stat--big"><span class="stat__label">Total replacement value</span><output class="stat__value" data-total>$0</output></div><p><span data-count>0</span> items &middot; <span data-rooms>0</span> rooms</p></div>
  <div class="table-wrap"><table class="inventory__table"><thead><tr><th>Room</th><th>Item</th><th>Brand / model</th><th>Serial #</th><th>Year bought</th><th class="num">Qty</th><th class="num">Replacement cost (each)</th><th></th></tr></thead><tbody data-rows></tbody></table></div>
  <p class="inventory__empty" data-empty>No items yet. Pick a room and click <strong>Add item</strong>. Start with electronics, appliances, furniture, jewelry and tools.</p>
  <div class="table-wrap"><table><thead><tr><th>Room</th><th class="num">Items</th><th class="num">Value</th></tr></thead><tbody data-byroom></tbody></table></div>
  <p class="fine">Your inventory is saved only in this browser on this device. Export a CSV and store it in the cloud or email it to yourself.</p>
</div>
<?php break;
    }
    return ob_get_clean();
}
