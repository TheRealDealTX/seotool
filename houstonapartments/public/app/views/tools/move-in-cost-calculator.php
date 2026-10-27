<div class="tool-grid2">
  <div class="tool-form">
    <div class="field-row">
      <label class="field">Monthly rent<span class="money-in"><i>$</i><input type="number" name="mc_rent" value="1400" min="0" step="25"></span></label>
      <label class="field">Move-in date<input type="date" name="mc_date"></label>
    </div>
    <div class="field-row">
      <label class="field">Security deposit<span class="money-in"><i>$</i><input type="number" name="mc_deposit" value="300" min="0" step="25"></span></label>
      <label class="field">Admin fee<span class="money-in"><i>$</i><input type="number" name="mc_admin" value="200" min="0" step="25"></span></label>
    </div>
    <div class="field-row">
      <label class="field">Application fee (each)<span class="money-in"><i>$</i><input type="number" name="mc_app" value="60" min="0" step="5"></span></label>
      <label class="field">Adults applying<input type="number" name="mc_adults" value="1" min="1" max="6"></label>
    </div>
    <div class="field-row three">
      <label class="field">Pets<input type="number" name="mc_pets" value="0" min="0" max="4"></label>
      <label class="field">Pet fee/deposit (each)<span class="money-in"><i>$</i><input type="number" name="mc_petfee" value="350" min="0" step="25"></span></label>
      <label class="field">Pet rent / mo (each)<span class="money-in"><i>$</i><input type="number" name="mc_petrent" value="25" min="0" step="5"></span></label>
    </div>
    <div class="field-row">
      <label class="field">Utility deposits &amp; setup<span class="money-in"><i>$</i><input type="number" name="mc_util" value="100" min="0" step="25"></span></label>
      <label class="field">Movers
        <select name="mc_movers"><option value="0">Doing it myself</option><option value="250">Truck rental only (~$250)</option><option value="800" selected>Local movers (~$800)</option><option value="1600">Full-service (~$1,600)</option></select>
      </label>
    </div>
    <label class="check"><input type="checkbox" name="mc_prorate" checked> Charge prorated rent for the first month</label>
  </div>
  <div class="tool-result">
    <p class="tr-label">Due at lease signing</p>
    <p class="tr-big" data-out="due">$0</p>
    <dl class="tr-list" data-out="lines"></dl>
    <p class="tr-label">Total moving budget</p>
    <p class="tr-mid" data-out="total">$0</p>
    <p class="tr-note">Lease through Houston Apartments and you may earn a move-in reward of up to $<?= SITE['cashback'] ?>.</p>
  </div>
</div>
