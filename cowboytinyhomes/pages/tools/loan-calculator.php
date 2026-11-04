<?php
$GLOBALS['scripts'][] = 'tools.js';
hero([
    'eyebrow' => 'Free Tool',
    'h1'      => 'Tiny Home Loan Calculator',
    'lead'    => 'Estimate your monthly tiny home payment. Choose a loan type, adjust price, down payment, rate and term, and see total interest plus a year-by-year payoff schedule.',
    'image'   => 'Park-Model-Homes.webp',
    'cta'     => false,
]);
$presets = [
    'rv'           => ['RV loan', '8.5% · 15 yrs'],
    'personal'     => ['Personal loan', '12% · 7 yrs'],
    'heloc'        => ['HELOC / home equity', '8.25% · 20 yrs'],
    'mortgage'     => ['Mortgage', '6.75% · 30 yrs'],
    'construction' => ['Construction-to-perm', '7.25% · 30 yrs'],
];
?>
<section class="section">
  <div class="wrap">
    <div data-tool="loan">
    <div class="tool">
      <div class="tool-panel">
        <h2>Loan Details</h2>
        <div class="field">
          <label>Loan type <small style="font-weight:400;color:var(--muted)">(illustrative example rates — rates change daily)</small></label>
          <div class="chips">
<?php foreach ($presets as $k => [$label, $hint]): ?>
            <label class="chip" title="<?= e($hint) ?>"><input type="radio" name="preset" value="<?= $k ?>" data-label="<?= e($label) ?>"<?= $k === 'rv' ? ' checked' : '' ?>><span><?= e($label) ?></span></label>
<?php endforeach; ?>
          </div>
        </div>
        <div class="field">
          <div class="range-head"><label for="lc-price">Home price</label><output for="lc-price"></output></div>
          <input id="lc-price" type="range" name="price" min="20000" max="500000" step="2500" value="85000" data-fmt="money">
        </div>
        <div class="field">
          <div class="range-head"><label for="lc-down">Down payment</label><output for="lc-down"></output></div>
          <input id="lc-down" type="range" name="down" min="0" max="50" step="1" value="10" data-fmt="pct">
        </div>
        <div class="field">
          <div class="range-head"><label for="lc-rate">Interest rate (APR)</label><output for="lc-rate"></output></div>
          <input id="lc-rate" type="range" name="rate" min="2" max="20" step="0.125" value="8.5" data-fmt="rate">
        </div>
        <div class="field">
          <div class="range-head"><label for="lc-term">Loan term</label><output for="lc-term"></output></div>
          <input id="lc-term" type="range" name="term" min="2" max="30" step="1" value="15" data-fmt="yr">
        </div>
      </div>
      <div class="result-panel" aria-live="polite">
        <h2>Estimated Monthly Payment</h2>
        <div class="result-big" data-out="pay">—</div>
        <p class="result-sub">Principal and interest only. Taxes, insurance, lot rent and HOA dues are extra.</p>
        <p class="result-sub" style="margin:14px 0 0">Principal</p>
        <div class="bar"><i data-bar="principal" style="width:0"></i></div>
        <p class="result-sub" style="margin:0">Interest</p>
        <div class="bar"><i data-bar="interest" style="width:0;background:linear-gradient(90deg,#a4532d,#c97a4f)"></i></div>
        <ul class="result-rows">
          <li><span>Down payment</span><b data-out="down">—</b></li>
          <li><span>Amount financed</span><b data-out="principal">—</b></li>
          <li><span>Total interest</span><b data-out="interest">—</b></li>
          <li><span>Total cost incl. down payment</span><b data-out="total">—</b></li>
        </ul>
        <a class="btn btn--gold" data-out="link" href="/contact-us/">Talk Budget With a Designer</a>
        <a class="btn btn--ghost" href="/guides/tiny-home-financing-texas/">Financing Guide</a>
        <p class="disclaimer">Example rates and terms are illustrations, not offers. Your rate depends on credit, the lender and how the home is classified (RV, chattel or real property).</p>
      </div>
    </div>
    <details class="amort-box">
      <summary>Show year-by-year payoff schedule</summary>
      <div class="table-wrap"><table>
        <thead><tr><th>Year</th><th>Principal paid</th><th>Interest paid</th><th>Remaining balance</th></tr></thead>
        <tbody data-out="amort"></tbody>
      </table></div>
    </details>
    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap wrap--narrow prose">
    <h2>How to Use the Tiny Home Loan Calculator</h2>
    <p>Financing a tiny home is different from financing a standard house, because lenders treat each type of tiny home differently. This tiny home loan calculator lets you compare the most common options side by side. Choose a loan type to load an example rate and term, then fine-tune the price, down payment, rate and term to match real quotes from your lender.</p>
    <p>The monthly payment shown is principal and interest. Remember to budget separately for insurance, property taxes on a foundation home, lot rent in an RV park or community, and utilities.</p>

    <h2>Tiny Home Loan Types Compared</h2>
    <div class="table-wrap"><table>
      <thead><tr><th>Loan type</th><th>Best for</th><th>Typical term</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>RV loan</td><td>Tiny homes on wheels and park models with RV certification</td><td>10–20 years</td><td>Lender usually requires RVIA or similar certification</td></tr>
        <tr><td>Personal loan</td><td>Smaller projects, uncertified homes</td><td>2–7 years</td><td>Unsecured, fast, but higher rates and shorter terms</td></tr>
        <tr><td>HELOC / home equity</td><td>Backyard ADUs on property you own</td><td>10–30 years</td><td>Uses your home's equity; often variable rate</td></tr>
        <tr><td>Mortgage</td><td>Foundation tiny homes on owned land</td><td>15–30 years</td><td>Home must meet code and appraise; small homes can be harder to appraise</td></tr>
        <tr><td>Construction-to-permanent</td><td>Custom homes and ADUs built from scratch</td><td>30 years after build</td><td>Pays builder in draws, then converts to a mortgage</td></tr>
      </tbody>
    </table></div>
    <p>The example rates in the calculator are illustrations only — actual rates change daily and depend on your credit score, down payment, debt-to-income ratio and the lender. Always compare written quotes.</p>

    <h2>Interpreting Your Results</h2>
    <p>Look beyond the monthly payment. A personal loan may have a manageable payment but a short term means higher monthly cost, while a 30-year mortgage has the lowest payment but the highest total interest. The principal-versus-interest bars and the payoff schedule show exactly how much of your money goes to the lender over time. Shortening the term or increasing your down payment are the two fastest ways to cut total interest.</p>
    <p>The home type you choose shapes your financing options. A tiny home on a permanent foundation built to code — like a <a href="/custom-tiny-homes-texas/">custom tiny home</a> or <a href="/adu-builders-texas/">ADU</a> — opens the door to mortgages and home equity loans. A <a href="/tiny-homes-on-wheels-texas/">tiny home on wheels</a> usually relies on RV or personal loans. For the full picture, read our <a href="/guides/tiny-home-financing-texas/">guide to tiny home financing in Texas</a>, and get a price to finance with the <a href="/tools/tiny-home-cost-calculator/">tiny home cost calculator</a>.</p>
  </div>
</section>

<?php faq_section([
    ['Can you get a mortgage for a tiny home in Texas?',
     '<p>Yes, if the home is on a permanent foundation, on land you own, built to local code and able to appraise. Tiny homes on wheels generally do not qualify for mortgages and are financed with RV or personal loans instead.</p>'],
    ['What credit score do I need for a tiny home loan?',
     '<p>Requirements vary by lender and loan type. Higher scores unlock lower rates and longer terms; personal loans and RV loans are often more sensitive to credit than secured home equity loans.</p>'],
    ['Are the interest rates in this calculator current?',
     '<p>No. They are illustrative examples so you can compare loan types. Rates change daily, so replace them with quotes from your lender for an accurate payment.</p>'],
    ['Is it better to use a HELOC or an RV loan for a tiny home?',
     '<p>If you are building an ADU on property you own, a HELOC or cash-out refinance often offers a lower rate and longer term. An RV loan suits a certified tiny home on wheels or park model, especially if you do not own a home to borrow against.</p>'],
], 'Tiny Home Loan FAQs'); ?>

<?php related([
    '/guides/tiny-home-financing-texas/',
    '/tools/tiny-home-cost-calculator/',
    '/tools/adu-rental-income-calculator/',
    '/tools/which-tiny-home-is-right-for-me/',
], 'More Budget Planning Tools'); ?>

<?php cta_band('Know Your Budget? Let’s Design to It.'); ?>
