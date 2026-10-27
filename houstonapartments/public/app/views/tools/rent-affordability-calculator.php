<div class="tool-grid2">
  <div class="tool-form">
    <div class="seg-toggle" role="radiogroup" aria-label="Income type">
      <label><input type="radio" name="ra_type" value="year" checked><span>Yearly salary</span></label>
      <label><input type="radio" name="ra_type" value="hour"><span>Hourly pay</span></label>
    </div>
    <label class="field" data-show="year">Household income (before taxes, per year)<span class="money-in"><i>$</i><input type="number" name="ra_income" value="60000" min="0" step="1000" inputmode="numeric"></span></label>
    <div class="field-row" data-show="hour" hidden>
      <label class="field">Hourly rate<span class="money-in"><i>$</i><input type="number" name="ra_rate" value="22" min="0" step="0.5" inputmode="decimal"></span></label>
      <label class="field">Hours per week<input type="number" name="ra_hours" value="40" min="1" max="80" inputmode="numeric"></label>
    </div>
    <label class="field">Monthly debt payments <small>(car, loans, credit cards)</small><span class="money-in"><i>$</i><input type="number" name="ra_debt" value="300" min="0" step="25" inputmode="numeric"></span></label>
    <label class="field">Roommate / partner income on the lease <small>(yearly, optional)</small><span class="money-in"><i>$</i><input type="number" name="ra_extra" value="0" min="0" step="1000" inputmode="numeric"></span></label>
  </div>
  <div class="tool-result">
    <p class="tr-label">You’ll likely qualify for rent up to</p>
    <p class="tr-big" data-out="max">$0</p>
    <p class="tr-sub">per month (3× income rule)</p>
    <div class="gauge"><div class="gauge-fill" data-out="gauge"></div></div>
    <dl class="tr-list">
      <dt>Comfortable budget (≈30%, after debts)</dt><dd data-out="comfy">$0</dd>
      <dt>Gross monthly income</dt><dd data-out="monthly">$0</dd>
      <dt>40× rule check</dt><dd data-out="forty">$0</dd>
    </dl>
    <a class="btn btn-grad btn-block" data-out="link" href="/apartments/">See apartments in my budget</a>
  </div>
</div>
