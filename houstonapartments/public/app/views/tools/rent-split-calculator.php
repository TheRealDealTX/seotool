<div class="tool-grid2">
  <div class="tool-form">
    <div class="field-row">
      <label class="field">Total monthly rent<span class="money-in"><i>$</i><input type="number" name="rs_rent" value="2100" min="0" step="25"></span></label>
      <label class="field">Utilities &amp; internet / mo<span class="money-in"><i>$</i><input type="number" name="rs_util" value="220" min="0" step="10"></span></label>
    </div>
    <div class="seg-toggle" role="radiogroup" aria-label="Split method">
      <label><input type="radio" name="rs_mode" value="even" checked><span>Even</span></label>
      <label><input type="radio" name="rs_mode" value="size"><span>By room size</span></label>
      <label><input type="radio" name="rs_mode" value="income"><span>By income</span></label>
    </div>
    <div class="mates" data-mates></div>
    <button type="button" class="btn btn-outline btn-sm" data-add-mate>＋ Add roommate</button>
  </div>
  <div class="tool-result">
    <p class="tr-label">Each person pays</p>
    <div class="split-out" data-out="split"></div>
    <p class="tr-note">Utilities are split evenly. Room-size mode adds 15% weight for a private bathroom.</p>
  </div>
</div>
