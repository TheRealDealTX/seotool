<div class="tool-panel kit-builder">
  <form class="tool-controls" data-kit-form onsubmit="return false">
    <fieldset class="seg"><legend>How do you climb?</legend>
      <label><input type="radio" name="sys" value="mrs" checked><span><b>Moving rope</b><small>MRS / DdRT</small></span></label>
      <label><input type="radio" name="sys" value="srs"><span><b>Stationary rope</b><small>SRS / SRT</small></span></label>
      <label><input type="radio" name="sys" value="spurs"><span><b>Removals</b><small>Spurs + flipline</small></span></label>
    </fieldset>
    <label class="slider-field"><span>Budget <output data-budget-out>$1,800</output></span>
      <input type="range" min="400" max="5000" step="50" value="1800" data-budget>
    </label>
    <fieldset class="checks"><legend>Add extras</legend>
      <label class="check"><input type="checkbox" value="throw" checked> Throw line &amp; weight</label>
      <label class="check"><input type="checkbox" value="saw" checked> Hand saw</label>
      <label class="check"><input type="checkbox" value="bag"> Gear bag</label>
    </fieldset>
  </form>
  <div class="kit-result">
    <div class="kit-summary">
      <svg class="budget-ring" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="track"/><circle cx="60" cy="60" r="52" class="fill" data-ring/></svg>
      <div class="kit-total"><small>Kit total</small><b data-kit-total>$0</b><span data-kit-status></span></div>
      <button class="btn btn-chain" type="button" data-kit-add>Add whole kit to cart</button>
    </div>
    <ol class="kit-slots" data-kit-slots></ol>
    <p class="fine">Typical prices. Every piece of life-support gear must be compatible with the rest of your system, inspected before use, and used by a trained climber following the manufacturer's instructions.</p>
  </div>
</div>
