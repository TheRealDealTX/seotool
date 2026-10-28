<div class="tool-grid">
  <form class="tool-form" id="budget-form" onsubmit="return false">
    <label class="field"><span class="field__label">Total budget ($)</span><input type="number" name="total" value="5000" min="100" step="50"></label>
    <label class="field"><span class="field__label">Room</span>
      <select name="room"><option value="living">Living room</option><option value="bedroom">Bedroom</option><option value="dining">Dining room</option><option value="office">Home office</option><option value="studio">Studio apartment (whole space)</option></select>
    </label>
    <fieldset>
      <legend>Your priority</legend>
      <div class="seg">
        <label><input type="radio" name="prio" value="comfort" checked><span>Comfort</span></label>
        <label><input type="radio" name="prio" value="statement"><span>Statement</span></label>
        <label><input type="radio" name="prio" value="storage"><span>Storage</span></label>
      </div>
    </fieldset>
    <fieldset>
      <legend>Approach</legend>
      <div class="seg">
        <label><input type="radio" name="diy" value="buy" checked><span>Mostly buy</span></label>
        <label><input type="radio" name="diy" value="diy"><span>Some DIY</span></label>
      </div>
    </fieldset>
  </form>
  <div class="result" id="budget-result" aria-live="polite"></div>
</div>
