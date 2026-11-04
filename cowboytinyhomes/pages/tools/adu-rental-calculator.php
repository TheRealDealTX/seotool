<?php
$GLOBALS['scripts'][] = 'tools.js';
hero([
    'eyebrow' => 'Free Tool',
    'h1'      => 'ADU Rental Income Calculator',
    'lead'    => 'Find out what a backyard ADU or casita could earn. Compare long-term and short-term rental income against your expenses and loan payment to see cash flow, ROI and payback.',
    'image'   => 'Accessory-Dwelling-Units.webp',
    'cta'     => false,
]);
?>
<section class="section">
  <div class="wrap">
    <div class="tool" data-tool="adu-rental">
      <div class="tool-panel">
        <h2>Build &amp; Financing</h2>
        <div class="field">
          <div class="range-head"><label for="ar-build">ADU build cost (all-in)</label><output for="ar-build"></output></div>
          <input id="ar-build" type="range" name="build" min="40000" max="350000" step="5000" value="150000" data-fmt="money">
        </div>
        <div class="field">
          <label>How will you pay?</label>
          <div class="chips">
            <label class="chip"><input type="radio" name="funding" value="loan" checked><span>Financed</span></label>
            <label class="chip"><input type="radio" name="funding" value="cash"><span>All cash</span></label>
          </div>
        </div>
        <div data-funding>
          <div class="field">
            <div class="range-head"><label for="ar-down">Down payment</label><output for="ar-down"></output></div>
            <input id="ar-down" type="range" name="down" min="0" max="80" step="5" value="20" data-fmt="pct">
          </div>
          <div class="field-row">
            <div class="field">
              <div class="range-head"><label for="ar-rate">Interest rate</label><output for="ar-rate"></output></div>
              <input id="ar-rate" type="range" name="rate" min="3" max="14" step="0.25" value="8" data-fmt="rate">
            </div>
            <div class="field">
              <div class="range-head"><label for="ar-term">Term</label><output for="ar-term"></output></div>
              <input id="ar-term" type="range" name="term" min="5" max="30" step="1" value="20" data-fmt="yr">
            </div>
          </div>
        </div>

        <h2>Rental Income</h2>
        <div class="field">
          <div class="chips">
            <label class="chip"><input type="radio" name="mode" value="ltr" checked><span>Long-term rental</span></label>
            <label class="chip"><input type="radio" name="mode" value="str"><span>Short-term rental</span></label>
          </div>
        </div>
        <div data-mode="ltr">
          <div class="field-row">
            <div class="field"><label for="ar-rent">Monthly rent ($)</label><input id="ar-rent" type="number" name="rent" min="0" step="25" value="1400"></div>
            <div class="field"><label for="ar-vac">Vacancy (%)</label><input id="ar-vac" type="number" name="vacancy" min="0" max="50" step="1" value="5"></div>
          </div>
        </div>
        <div data-mode="str" hidden>
          <div class="field-row">
            <div class="field"><label for="ar-nightly">Nightly rate ($)</label><input id="ar-nightly" type="number" name="nightly" min="0" step="5" value="125"></div>
            <div class="field"><label for="ar-stay">Average stay (nights)</label><input id="ar-stay" type="number" name="stay" min="1" step="1" value="3"></div>
          </div>
          <div class="field">
            <div class="range-head"><label for="ar-occ">Occupancy</label><output for="ar-occ"></output></div>
            <input id="ar-occ" type="range" name="occupancy" min="10" max="95" step="5" value="60" data-fmt="pct">
          </div>
          <div class="field-row">
            <div class="field"><label for="ar-clean">Cleaning cost per stay ($)</label><input id="ar-clean" type="number" name="clean" min="0" step="5" value="60"></div>
            <div class="field"><label for="ar-plat">Platform fees (%)</label><input id="ar-plat" type="number" name="platform" min="0" max="30" step="1" value="3"></div>
          </div>
        </div>

        <h2>Expenses</h2>
        <div class="field-row">
          <div class="field"><label for="ar-tax">Added property tax ($/yr)</label><input id="ar-tax" type="number" name="tax" min="0" step="100" value="2500"></div>
          <div class="field"><label for="ar-ins">Added insurance ($/yr)</label><input id="ar-ins" type="number" name="ins" min="0" step="50" value="700"></div>
        </div>
        <div class="field-row">
          <div class="field"><label for="ar-maint">Maintenance (% of income)</label><input id="ar-maint" type="number" name="maint" min="0" max="30" step="1" value="5"></div>
          <div class="field"><label for="ar-mgmt">Management (% of income)</label><input id="ar-mgmt" type="number" name="mgmt" min="0" max="40" step="1" value="0"></div>
        </div>
        <div class="field"><label for="ar-util">Utilities you pay ($/mo)</label><input id="ar-util" type="number" name="util" min="0" step="10" value="0"></div>
      </div>

      <div class="result-panel" aria-live="polite">
        <h2>Monthly Cash Flow</h2>
        <div class="result-big" data-out="net">—</div>
        <p class="result-sub">After expenses and loan payment</p>
        <p class="result-sub" style="margin:14px 0 0">Income</p>
        <div class="bar"><i data-bar="income" style="width:0"></i></div>
        <p class="result-sub" style="margin:0">Expenses + loan payment</p>
        <div class="bar"><i data-bar="costs" style="width:0;background:linear-gradient(90deg,#a4532d,#c97a4f)"></i></div>
        <ul class="result-rows">
          <li><span>Rental income (monthly)</span><b data-out="income">—</b></li>
          <li><span>Operating expenses (monthly)</span><b data-out="expenses">—</b></li>
          <li><span>Loan payment (monthly)</span><b data-out="debt">—</b></li>
          <li><span>Annual cash flow</span><b data-out="annual">—</b></li>
          <li><span>Cash-on-cash return</span><b data-out="roi">—</b></li>
          <li><span>Simple payback on build cost</span><b data-out="payback">—</b></li>
        </ul>
        <a class="btn btn--gold" data-out="link" href="/contact-us/">Plan My Rental ADU</a>
        <a class="btn btn--ghost" href="/adu-builders-texas/">ADU Building Options</a>
        <p class="disclaimer">Illustrative estimate only — not financial or tax advice. Rents, occupancy, taxes and short-term rental rules vary by city and neighborhood.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--narrow prose">
    <h2>How to Use the ADU Rental Income Calculator</h2>
    <p>A backyard accessory dwelling unit can turn unused yard space into steady income. This ADU rental income calculator shows whether the numbers work on your property before you spend a dollar on plans. Enter your all-in build cost first — the price of the casita plus design, permits, site work and utility connections. If you are not sure, the <a href="/tools/tiny-home-cost-calculator/">tiny home cost calculator</a> will give you a realistic range for an ADU in Texas.</p>
    <p>Next, tell the calculator how you will pay. If you finance, set the down payment, rate and term to match the loan you expect, such as a HELOC, cash-out refinance or construction loan. If you pay cash, the cash-on-cash return equals your return on the full build cost.</p>

    <h2>Long-Term vs Short-Term Rental</h2>
    <p><strong>Long-term rentals</strong> (6 to 12-month leases) offer predictable income and less work. Enter a realistic monthly rent for a studio or one-bedroom in your area and a vacancy allowance — 5% is about two to three weeks empty per year.</p>
    <p><strong>Short-term rentals</strong> through booking platforms can earn more per month, but income swings with seasons and local events, and you pay for cleaning, supplies, platform fees and more of your own time. Occupancy is the share of nights booked; 50% to 70% is a common planning range for a well-reviewed unit. Important: many Texas cities regulate short-term rentals with permits, occupancy limits, hotel occupancy taxes or outright restrictions in some zones, and HOAs may ban them. Check the rules for your address before you count on short-term income.</p>

    <h2>Understanding the Results</h2>
    <ul>
      <li><strong>Monthly cash flow</strong> is what is left after operating expenses and the loan payment. Positive cash flow means the ADU pays for itself; negative means you are subsidizing it while it builds equity.</li>
      <li><strong>Cash-on-cash return</strong> divides annual cash flow by the cash you actually put in (your down payment). It is the best quick measure of how hard your money is working.</li>
      <li><strong>Simple payback</strong> divides the full build cost by annual net operating income (income minus expenses, before loan payments). It answers, "How many years of rent does it take to cover what I spent?"</li>
    </ul>
    <p>Not included: the increase in your property's market value, tax deductions such as depreciation, rent growth and the personal value of housing a family member. In many cases those are the biggest benefits of all. Property taxes deserve special attention in Texas — an ADU increases your appraised value, and income-producing units may not receive the same homestead treatment as your main house. Ask your county appraisal district or a tax professional for specifics.</p>
    <p>Ready to see what fits on your lot? Cowboy Tiny Homes designs <a href="/adu-builders-texas/">ADUs, casitas and granny flats</a> across Texas, and every design package starts with a feasibility study that checks zoning, setbacks and utility access for your address.</p>
  </div>
</section>

<?php faq_section([
    ['How much rent can a backyard ADU earn in Texas?',
     '<p>It varies widely by city and neighborhood. A studio or one-bedroom casita in a major Texas metro often rents for roughly what comparable small apartments nearby rent for. Check local listings for similar units and plug those numbers into the calculator.</p>'],
    ['Can I use my ADU as an Airbnb in Texas?',
     '<p>Sometimes. Short-term rental rules are set by each city and many HOAs, and they range from simple registration to permits, taxes and restrictions in certain zones. Confirm your local rules before building with short-term rental income in mind.</p>'],
    ['What is a good cash-on-cash return for an ADU?',
     '<p>Many owners consider 6% to 10% or more a solid return, but goals differ. A family member living rent-free can make a negative-cash-flow ADU worthwhile, while an investor may require positive cash flow from day one.</p>'],
    ['Does an ADU increase my property taxes?',
     '<p>Usually, yes. Adding a permanent living unit increases your appraised value. The calculator includes an "added property tax" field so you can estimate the impact. Your county appraisal district can explain how it will be assessed.</p>'],
    ['How can I make my ADU more profitable?',
     '<p>Keep the design efficient, include a full kitchen and laundry, give it a private entrance and outdoor space, and choose durable finishes that keep maintenance low. Cowboy Tiny Homes designs rental ADUs with these priorities in mind.</p>'],
], 'ADU Rental Income FAQs'); ?>

<?php related([
    '/adu-builders-texas/',
    '/tools/tiny-home-loan-calculator/',
    '/guides/tiny-home-financing-texas/',
    '/tools/tiny-home-cost-calculator/',
], 'Plan Your Rental ADU'); ?>

<?php cta_band('Build a Backyard ADU That Pays You Back'); ?>
