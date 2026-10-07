<div class="tool-panel rig-calc">
  <form class="tool-controls" onsubmit="return false" data-rig-form>
    <label class="field"><span>Species</span><select data-species></select></label>
    <label class="slider-field"><span>Diameter <output data-dia-out>14 in</output></span><input type="range" min="4" max="40" value="14" step="1" data-dia></label>
    <label class="slider-field"><span>Length <output data-len-out>6 ft</output></span><input type="range" min="1" max="20" value="6" step="0.5" data-len></label>
    <label class="slider-field"><span>Free fall before the rope catches <output data-drop-out>2 ft</output></span><input type="range" min="0" max="10" value="2" step="0.5" data-drop></label>
    <label class="slider-field"><span>Rope in the system (rigging point to lowering device) <output data-rope-out>40 ft</output></span><input type="range" min="10" max="120" value="40" step="5" data-ropelen></label>
    <label class="field"><span>Rigging rope</span><select data-rope></select></label>
  </form>
  <div class="rig-output">
    <svg class="rig-scene" viewBox="0 0 320 300" aria-hidden="true">
      <path class="rig-limb" d="M20 46 Q160 26 300 40"/><circle class="rig-block" cx="160" cy="40" r="9"/>
      <path class="rig-line" d="M160 49 V120" data-rig-line/>
      <g data-rig-log transform="translate(160 150)"><rect class="rig-wood" x="-60" y="-16" width="120" height="32" rx="16" data-rig-logshape/><ellipse class="rig-end" cx="60" cy="0" rx="9" ry="16"/></g>
      <path class="rig-ground" d="M0 288 H320"/>
    </svg>
    <div class="stats">
      <div class="stat"><small>Log weight</small><b data-weight>—</b><span data-weight-note></span></div>
      <div class="stat"><small>Peak load if the rope is locked off</small><b data-peak>—</b><span data-peak-note></span></div>
      <div class="stat"><small>Rope strength needed at 10:1 for the static weight</small><b data-mbs>—</b></div>
    </div>
    <div class="gauge"><span class="gauge-fill" data-gauge></span><span class="gauge-label" data-gauge-label></span></div>
    <p class="verdict" data-verdict></p>
    <p class="fine">Estimate only, using typical green weights and a simple elastic rope model with no friction or rope running. Real loads depend on the rope, the rigging point, friction and technique. When in doubt, take smaller pieces.</p>
  </div>
</div>
<div class="tool-recs"><h2>Rigging gear for the job</h2><div class="grid products-grid" data-tool-recs></div></div>
