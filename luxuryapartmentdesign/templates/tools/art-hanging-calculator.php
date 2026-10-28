<div class="tool-grid">
  <form class="tool-form" id="art-form" onsubmit="return false">
    <fieldset>
      <legend>Where is the art going?</legend>
      <div class="seg">
        <label><input type="radio" name="mode" value="wall" checked><span>Open wall</span></label>
        <label><input type="radio" name="mode" value="furniture"><span>Above furniture</span></label>
        <label><input type="radio" name="mode" value="gallery"><span>Gallery wall</span></label>
      </div>
    </fieldset>
    <div class="field-row">
      <label class="field"><span class="field__label">Art height (in)</span><input type="number" name="ah" value="24" min="4" max="120" step="0.5"></label>
      <label class="field"><span class="field__label">Art width (in)</span><input type="number" name="aw" value="36" min="4" max="200" step="0.5"></label>
    </div>
    <label class="field"><span class="field__label">Hanger drop (in)</span><input type="number" name="drop" value="3" min="0" max="20" step="0.25"><small>Distance from the top of the frame down to the taut wire or hook.</small></label>
    <fieldset>
      <legend>Center height standard</legend>
      <div class="seg">
        <label><input type="radio" name="center" value="57" checked><span>57 in. (gallery)</span></label>
        <label><input type="radio" name="center" value="60"><span>60 in.</span></label>
      </div>
    </fieldset>
    <label class="field"><span class="field__label">Ceiling height (ft)</span><input type="number" name="ceil" value="8" min="7" max="20" step="0.5"></label>
    <div class="field-row" data-show="furniture">
      <label class="field"><span class="field__label">Furniture height (in)</span><input type="number" name="fh" value="34" min="10" max="80"><small>Top of sofa back or headboard</small></label>
      <label class="field"><span class="field__label">Furniture width (in)</span><input type="number" name="fw" value="84" min="20" max="200"></label>
    </div>
    <div class="field-row" data-show="gallery">
      <label class="field"><span class="field__label">Frames per row</span><input type="number" name="cols" value="3" min="1" max="8"></label>
      <label class="field"><span class="field__label">Rows</span><input type="number" name="rows" value="2" min="1" max="5"></label>
    </div>
    <label class="field" data-show="gallery"><span class="field__label">Gap between frames (in)</span><input type="number" name="gap" value="2.5" min="1" max="6" step="0.5"></label>
  </form>
  <div class="result" id="art-result" aria-live="polite"></div>
</div>
