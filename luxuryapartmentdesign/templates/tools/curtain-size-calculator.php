<div class="tool-grid">
  <form class="tool-form" id="curtain-form" onsubmit="return false">
    <div class="field-row">
      <label class="field"><span class="field__label">Window width (in)</span><input type="number" name="ww" value="48" min="12" max="300"><small>Outside edge of the trim to outside edge</small></label>
      <label class="field"><span class="field__label">Window height (in)</span><input type="number" name="wh" value="60" min="12" max="200"></label>
    </div>
    <div class="field-row">
      <label class="field"><span class="field__label">Top of window to ceiling (in)</span><input type="number" name="above" value="14" min="0" max="80"></label>
      <label class="field"><span class="field__label">Bottom of window to floor (in)</span><input type="number" name="below" value="22" min="0" max="80"></label>
    </div>
    <fieldset>
      <legend>Length style</legend>
      <div class="seg">
        <label><input type="radio" name="len" value="float" checked><span>Float</span></label>
        <label><input type="radio" name="len" value="kiss"><span>Kiss</span></label>
        <label><input type="radio" name="len" value="break"><span>Break</span></label>
        <label><input type="radio" name="len" value="puddle"><span>Puddle</span></label>
      </div>
    </fieldset>
    <fieldset>
      <legend>Fullness</legend>
      <div class="seg">
        <label><input type="radio" name="full" value="1.5"><span>1.5× tailored</span></label>
        <label><input type="radio" name="full" value="2" checked><span>2× standard</span></label>
        <label><input type="radio" name="full" value="2.5"><span>2.5× luxurious</span></label>
      </div>
    </fieldset>
    <label class="field"><span class="field__label">Panel width you are buying (in)</span>
      <select name="pw"><option value="50">50 in.</option><option value="54" selected>54 in.</option></select>
    </label>
  </form>
  <div class="result" id="curtain-result" aria-live="polite"></div>
</div>
