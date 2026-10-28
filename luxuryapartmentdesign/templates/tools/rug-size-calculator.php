<div class="tool-grid">
  <form class="tool-form" id="rug-form" onsubmit="return false">
    <fieldset>
      <legend>Room type</legend>
      <div class="seg">
        <label><input type="radio" name="room" value="living" checked><span>Living room</span></label>
        <label><input type="radio" name="room" value="dining"><span>Dining room</span></label>
        <label><input type="radio" name="room" value="bedroom"><span>Bedroom</span></label>
        <label><input type="radio" name="room" value="hall"><span>Entry / hallway</span></label>
      </div>
    </fieldset>
    <div class="field-row">
      <label class="field"><span class="field__label">Room length (ft)</span><input type="number" name="len" value="14" min="3" max="60" step="0.5" inputmode="decimal"></label>
      <label class="field"><span class="field__label">Room width (ft)</span><input type="number" name="wid" value="12" min="2" max="60" step="0.5" inputmode="decimal"></label>
    </div>
    <fieldset data-show="living">
      <legend>Furniture layout</legend>
      <div class="seg">
        <label><input type="radio" name="layout" value="front" checked><span>Front legs on rug</span></label>
        <label><input type="radio" name="layout" value="all"><span>All legs on rug</span></label>
        <label><input type="radio" name="layout" value="float"><span>Rug under coffee table only</span></label>
      </div>
    </fieldset>
    <div class="field-row" data-show="dining">
      <label class="field"><span class="field__label">Table length (in)</span><input type="number" name="tl" value="72" min="24" max="160"></label>
      <label class="field"><span class="field__label">Table width (in)</span><input type="number" name="tw" value="38" min="24" max="80"></label>
    </div>
    <label class="field" data-show="bedroom"><span class="field__label">Bed size</span>
      <select name="bed"><option value="twin">Twin</option><option value="full">Full</option><option value="queen" selected>Queen</option><option value="king">King</option><option value="cal">California king</option></select>
    </label>
  </form>
  <div class="result" id="rug-result" aria-live="polite"></div>
</div>
