<div class="tool-panel height-calc">
  <form class="tool-controls" onsubmit="return false">
    <label class="slider-field"><span>Distance from the trunk <output data-d-out>60 ft</output></span><input type="range" min="10" max="200" value="60" step="1" data-d></label>
    <label class="slider-field"><span>Angle to the treetop <output data-a-out>45°</output></span><input type="range" min="10" max="80" value="45" step="1" data-a></label>
    <label class="slider-field"><span>Your eye height <output data-eye-out>5.5 ft</output></span><input type="range" min="4" max="7" value="5.5" step="0.1" data-eye></label>
    <label class="slider-field"><span>Tie-in point, as % of tree height <output data-tie-out>75%</output></span><input type="range" min="40" max="95" value="75" step="1" data-tie></label>
    <fieldset class="seg seg-sm"><legend>Climbing system</legend>
      <label><input type="radio" name="rs" value="mrs" checked><span><b>Moving rope</b></span></label>
      <label><input type="radio" name="rs" value="srs"><span><b>Stationary rope</b></span></label>
    </fieldset>
  </form>
  <div class="height-output">
    <svg class="height-scene" viewBox="0 0 360 300" aria-hidden="true">
      <path class="hs-ground" d="M0 270 H360"/>
      <g data-hs-tree><path class="hs-trunk" d="M290 270 V120" data-hs-trunk/><circle class="hs-crown" cx="290" cy="110" r="46" data-hs-crown/></g>
      <g data-hs-person><circle class="hs-head" cx="40" cy="236" r="7"/><path class="hs-body" d="M40 243 V262 M40 262 l-7 8 M40 262 l7 8 M40 248 l-8 6 M40 248 l9 -4"/></g>
      <path class="hs-sight" d="M40 236 L290 70" data-hs-sight/>
      <path class="hs-arc" d="" data-hs-arc/>
      <path class="hs-dist" d="M40 282 H290" /><text x="165" y="296" class="hs-label" data-hs-dist>60 ft</text>
      <circle class="hs-tie" cx="290" cy="110" r="5" data-hs-tie/>
    </svg>
    <div class="stats">
      <div class="stat"><small>Tree height</small><b data-h>—</b></div>
      <div class="stat"><small>Tie-in height</small><b data-tie-h>—</b></div>
      <div class="stat"><small>Minimum rope</small><b data-rope>—</b><span data-rope-note></span></div>
    </div>
    <p class="verdict" data-rope-verdict></p>
  </div>
</div>
<div class="tool-recs"><h2>Climbing rope and throw line</h2><div class="grid products-grid" data-tool-recs></div></div>
