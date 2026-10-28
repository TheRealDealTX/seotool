<div class="tool-grid">
  <form class="tool-form" id="paint-form" onsubmit="return false">
    <div class="field-row--3 field-row">
      <label class="field"><span class="field__label">Length (ft)</span><input type="number" name="len" value="14" min="1" step="0.5"></label>
      <label class="field"><span class="field__label">Width (ft)</span><input type="number" name="wid" value="12" min="1" step="0.5"></label>
      <label class="field"><span class="field__label">Height (ft)</span><input type="number" name="hei" value="8" min="6" step="0.5"></label>
    </div>
    <div class="field-row">
      <label class="field"><span class="field__label">Doors</span><input type="number" name="doors" value="1" min="0" max="20"></label>
      <label class="field"><span class="field__label">Windows</span><input type="number" name="wins" value="2" min="0" max="30"></label>
    </div>
    <fieldset>
      <legend>Coats</legend>
      <div class="seg">
        <label><input type="radio" name="coats" value="1"><span>1</span></label>
        <label><input type="radio" name="coats" value="2" checked><span>2</span></label>
        <label><input type="radio" name="coats" value="3"><span>3</span></label>
      </div>
    </fieldset>
    <label class="field"><span class="field__label"><input type="checkbox" name="ceiling"> Paint the ceiling too</span></label>
    <label class="field"><span class="field__label"><input type="checkbox" name="primer"> I need primer (dark-to-light, patches, new drywall or glossy walls)</span></label>
    <div class="field-row">
      <label class="field"><span class="field__label">Coverage (sq ft/gal)</span><input type="number" name="cov" value="350" min="200" max="450" step="10"></label>
      <label class="field"><span class="field__label">Price per gallon ($)</span><input type="number" name="price" value="45" min="0" step="1"></label>
    </div>
  </form>
  <div class="result" id="paint-result" aria-live="polite"></div>
</div>
