<?php /** Metal vs shingle lifetime cost widget. Logic: main.js → tools.compare */ ?>
<div class="tool tool-compare" data-tool="compare">
  <div class="tool-inputs">
    <label class="field">
      <span class="field-label">Roof area (sq ft) <output data-out="area">2,400</output></span>
      <input type="range" name="area" min="1000" max="6000" step="100" value="2400">
    </label>
    <label class="field">
      <span class="field-label">Years you plan to own the home <output data-out="years">30</output></span>
      <input type="range" name="years" min="5" max="50" step="1" value="30">
    </label>
    <div class="form-row">
      <label class="field"><span class="field-label">Shingle $/sq ft</span><input type="number" name="shingleRate" value="5.75" min="2" max="15" step="0.25"></label>
      <label class="field"><span class="field-label">Metal $/sq ft</span><input type="number" name="metalRate" value="12.50" min="4" max="25" step="0.25"></label>
    </div>
    <div class="form-row">
      <label class="field"><span class="field-label">Shingle lifespan (yrs)</span><input type="number" name="shingleLife" value="20" min="10" max="35"></label>
      <label class="field"><span class="field-label">Metal lifespan (yrs)</span><input type="number" name="metalLife" value="50" min="25" max="70"></label>
    </div>
    <div class="form-row">
      <label class="field"><span class="field-label">Cost inflation / yr (%)</span><input type="number" name="inflation" value="3" min="0" max="8" step="0.5"></label>
      <label class="field"><span class="field-label">Metal cooling savings $/yr</span><input type="number" name="savings" value="0" min="0" max="1000" step="10"></label>
    </div>
  </div>
  <div class="tool-result" aria-live="polite">
    <div class="compare-totals">
      <div class="ct ct-shingle"><span>Shingles</span><strong data-out="shingleTotal">$0</strong><small data-out="shingleCount"></small></div>
      <div class="ct ct-metal"><span>Metal</span><strong data-out="metalTotal">$0</strong><small data-out="metalCount"></small></div>
    </div>
    <svg class="compare-chart" viewBox="0 0 400 200" role="img" aria-label="Cumulative cost over time for shingle and metal roofs">
      <g class="grid"></g>
      <path class="line-shingle" d=""></path>
      <path class="line-metal" d=""></path>
      <g class="axis"></g>
    </svg>
    <div class="chart-legend"><span class="lg-shingle">Shingle (cumulative)</span><span class="lg-metal">Metal (cumulative)</span></div>
    <p class="result-verdict" data-out="verdict"></p>
    <p class="result-note">Assumptions are editable. Replacement costs grow with inflation; savings are optional. Ask your insurer about impact-rated roof discounts, which are not included.</p>
    <a class="btn btn-primary btn-block" href="/services/metal-roofing-bastrop-tx/">Explore Bastrop Metal Roofing <?= icon('arrow') ?></a>
  </div>
</div>
