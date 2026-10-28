<div class="tool-grid">
  <form class="tool-form" id="light-form" onsubmit="return false">
    <label class="field"><span class="field__label">Room type</span>
      <select name="room">
        <option value="living">Living room</option>
        <option value="bedroom">Bedroom</option>
        <option value="dining">Dining room</option>
        <option value="kitchen">Kitchen</option>
        <option value="bathroom">Bathroom</option>
        <option value="office">Home office</option>
        <option value="hall">Hallway / entry</option>
      </select>
    </label>
    <div class="field-row">
      <label class="field"><span class="field__label">Length (ft)</span><input type="number" name="len" value="14" min="2" step="0.5"></label>
      <label class="field"><span class="field__label">Width (ft)</span><input type="number" name="wid" value="12" min="2" step="0.5"></label>
    </div>
    <fieldset>
      <legend>Brightness preference</legend>
      <div class="seg">
        <label><input type="radio" name="lvl" value="0"><span>Soft</span></label>
        <label><input type="radio" name="lvl" value="0.5" checked><span>Balanced</span></label>
        <label><input type="radio" name="lvl" value="1"><span>Bright</span></label>
      </div>
    </fieldset>
    <label class="field"><span class="field__label">Bulb output (lumens)</span>
      <select name="bulb"><option value="450">450 lm (40W equivalent)</option><option value="800" selected>800 lm (60W equivalent)</option><option value="1100">1100 lm (75W equivalent)</option><option value="1600">1600 lm (100W equivalent)</option></select>
    </label>
  </form>
  <div class="result" id="light-result" aria-live="polite"></div>
</div>
