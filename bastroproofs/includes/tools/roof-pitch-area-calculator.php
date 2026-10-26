<?php /** Roof pitch & area widget. Logic: main.js → tools.pitch */ ?>
<div class="tool tool-pitch" data-tool="pitch">
  <div class="tool-inputs">
    <div class="form-row">
      <label class="field"><span class="field-label">House length (ft)</span><input type="number" name="length" value="60" min="10" max="300"></label>
      <label class="field"><span class="field-label">House width (ft)</span><input type="number" name="width" value="40" min="10" max="300"></label>
    </div>
    <label class="field">
      <span class="field-label">Eave overhang (inches) <output data-out="overhang">12</output></span>
      <input type="range" name="overhang" min="0" max="36" step="1" value="12">
    </label>
    <label class="field">
      <span class="field-label">Roof pitch <output data-out="pitch">6/12</output></span>
      <input type="range" name="pitch" min="1" max="18" step="1" value="6">
    </label>
    <div class="field">
      <span class="field-label">Waste factor</span>
      <div class="seg" role="radiogroup" aria-label="Waste factor">
        <label><input type="radio" name="waste" value="10" checked><span>10% gable</span></label>
        <label><input type="radio" name="waste" value="15"><span>15% hip / complex</span></label>
      </div>
    </div>
    <svg class="pitch-svg" viewBox="0 0 300 170" role="img" aria-label="Roof pitch diagram">
      <rect class="ps-wall" x="40" y="120" width="220" height="40"></rect>
      <polygon class="ps-roof" points="20,124 150,60 280,124"></polygon>
      <path class="ps-run" d="M150 124 H 280"></path>
      <path class="ps-rise" d="M150 124 V 60"></path>
      <text class="ps-label ps-angle" x="200" y="116">26.6°</text>
      <text class="ps-label ps-rise-t" x="156" y="98">6"</text>
      <text class="ps-label ps-run-t" x="206" y="140">12"</text>
    </svg>
  </div>
  <div class="tool-result" aria-live="polite">
    <span class="result-kicker">Roof surface area</span>
    <div class="result-big"><span data-out="area">0</span> <small>sq ft</small></div>
    <dl class="result-stats result-stats-2">
      <div><dt>Pitch angle</dt><dd data-out="angle">—</dd></div>
      <div><dt>Pitch multiplier</dt><dd data-out="mult">—</dd></div>
      <div><dt>Squares (w/ waste)</dt><dd data-out="squares">—</dd></div>
      <div><dt>Shingle bundles</dt><dd data-out="bundles">—</dd></div>
      <div><dt>Underlayment rolls</dt><dd data-out="rolls">—</dd></div>
      <div><dt>Walkable?</dt><dd data-out="walk">—</dd></div>
    </dl>
    <p class="result-note">A roofing square is 100 sq ft. Bundles assume 3 per square; synthetic underlayment assumes 1,000 sq ft per roll. Dormers, valleys and porches add area — we measure exactly during the free inspection.</p>
    <a class="btn btn-primary btn-block" href="/roofing-tools/roof-replacement-cost-calculator/">Price This Roof <?= icon('arrow') ?></a>
  </div>
</div>
