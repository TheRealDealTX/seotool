<div class="tool-grid">
  <form class="tool-form" id="pal-form" onsubmit="return false">
    <div class="field">
      <span class="field__label">Start with a preset</span>
      <div class="presets" id="pal-presets"></div>
    </div>
    <div class="field-row">
      <label class="field"><span class="field__label">Base color</span><input type="color" name="base" value="#a99bc9"></label>
      <label class="field"><span class="field__label">Hex</span><input type="text" name="hex" value="#a99bc9" maxlength="7" spellcheck="false"></label>
    </div>
    <label class="field"><span class="field__label">Color harmony</span>
      <select name="harmony">
        <option value="mono">Monochromatic</option>
        <option value="analogous" selected>Analogous</option>
        <option value="complementary">Complementary</option>
        <option value="split">Split-complementary</option>
        <option value="triadic">Triadic</option>
        <option value="neutral">Warm neutral</option>
      </select>
    </label>
    <fieldset>
      <legend>Base color is the…</legend>
      <div class="seg">
        <label><input type="radio" name="role" value="main" checked><span>60% (walls)</span></label>
        <label><input type="radio" name="role" value="accent"><span>10% (accent)</span></label>
      </div>
    </fieldset>
  </form>
  <div class="result" id="pal-result" aria-live="polite"></div>
</div>
