<div class="tool-panel fuel-calc">
  <form class="tool-controls" onsubmit="return false">
    <fieldset class="seg seg-sm"><legend>Units</legend>
      <label><input type="radio" name="u" value="gal" checked><span><b>US gallons</b></span></label>
      <label><input type="radio" name="u" value="l"><span><b>Liters</b></span></label>
    </fieldset>
    <label class="slider-field"><span>Fuel amount <output data-amt-out>1 gal</output></span><input type="range" min="0.25" max="5" step="0.25" value="1" data-amt></label>
    <fieldset class="seg seg-sm ratios"><legend>Ratio</legend>
      <label><input type="radio" name="r" value="50" checked><span><b>50:1</b></span></label>
      <label><input type="radio" name="r" value="40"><span><b>40:1</b></span></label>
      <label><input type="radio" name="r" value="32"><span><b>32:1</b></span></label>
      <label><input type="radio" name="r" value="25"><span><b>25:1</b></span></label>
    </fieldset>
  </form>
  <div class="fuel-output">
    <svg class="jerry" viewBox="0 0 200 240" aria-hidden="true">
      <defs><clipPath id="can"><path d="M30 50 h120 l20 20 v150 a10 10 0 0 1 -10 10 h-130 a10 10 0 0 1 -10 -10 v-160 a10 10 0 0 1 10 -10z"/></clipPath></defs>
      <g clip-path="url(#can)"><rect class="jerry-gas" x="0" y="80" width="200" height="160" data-gas/><rect class="jerry-oil" x="0" y="80" width="200" height="0" data-oil/></g>
      <path class="jerry-can" d="M30 50 h120 l20 20 v150 a10 10 0 0 1 -10 10 h-130 a10 10 0 0 1 -10 -10 v-160 a10 10 0 0 1 10 -10z"/>
      <path class="jerry-spout" d="M150 50 l18 -26 h18 l-12 30"/><path class="jerry-handle" d="M50 50 v-20 h60 v20"/>
    </svg>
    <div class="stats">
      <div class="stat big"><small>Add this much 2-stroke oil</small><b data-oz>2.6 fl oz</b><span data-ml>76 ml</span></div>
      <div class="stat"><small>Mix</small><b data-mix>1 gal at 50:1</b></div>
    </div>
    <table class="mix-table"><caption>Quick reference, US fluid ounces of oil</caption><thead><tr><th>Gas</th><th>50:1</th><th>40:1</th><th>32:1</th></tr></thead><tbody data-mix-table></tbody></table>
  </div>
</div>
<div class="tool-recs"><h2>Fuel, oil and the saws that burn it</h2><div class="grid products-grid" data-tool-recs></div></div>
