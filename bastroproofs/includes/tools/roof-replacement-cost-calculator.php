<?php /** Roof replacement cost calculator widget. Logic: main.js → tools.cost */ ?>
<div class="tool tool-cost" data-tool="cost">
  <div class="tool-inputs">
    <label class="field">
      <span class="field-label">Home size (heated sq ft) <output data-out="sqft">2,000</output></span>
      <input type="range" name="sqft" min="800" max="6000" step="50" value="2000">
    </label>
    <div class="field">
      <span class="field-label">Stories</span>
      <div class="seg" role="radiogroup" aria-label="Stories">
        <label><input type="radio" name="stories" value="1" checked><span>1 story</span></label>
        <label><input type="radio" name="stories" value="2"><span>2 story</span></label>
      </div>
    </div>
    <div class="field">
      <span class="field-label">Roof pitch</span>
      <div class="seg seg-4" role="radiogroup" aria-label="Roof pitch">
        <label><input type="radio" name="pitch" value="low"><span>Low<small>≤4/12</small></span></label>
        <label><input type="radio" name="pitch" value="med" checked><span>Medium<small>5–7/12</small></span></label>
        <label><input type="radio" name="pitch" value="steep"><span>Steep<small>8–10/12</small></span></label>
        <label><input type="radio" name="pitch" value="vsteep"><span>Very steep<small>11/12+</small></span></label>
      </div>
    </div>
    <label class="field">
      <span class="field-label">Roofing material</span>
      <select name="material">
        <option value="arch" selected>Architectural shingles</option>
        <option value="class4">Class 4 impact-resistant shingles</option>
        <option value="rpanel">Exposed-fastener metal (R-panel)</option>
        <option value="seam">Standing seam metal</option>
        <option value="stone">Stone-coated steel</option>
      </select>
    </label>
    <div class="field">
      <span class="field-label">Layers to tear off</span>
      <div class="seg" role="radiogroup" aria-label="Layers to tear off">
        <label><input type="radio" name="layers" value="1" checked><span>1 layer</span></label>
        <label><input type="radio" name="layers" value="2"><span>2 layers</span></label>
      </div>
    </div>
    <fieldset class="field checks">
      <legend class="field-label">Add-ons</legend>
      <label><input type="checkbox" name="decking"> Decking replacement allowance (≈15%)</label>
      <label><input type="checkbox" name="vent" checked> Ridge vent / ventilation upgrade</label>
      <label><input type="checkbox" name="gutters"> New seamless gutters</label>
    </fieldset>
  </div>
  <div class="tool-result" aria-live="polite">
    <span class="result-kicker">Estimated planning range</span>
    <div class="result-big"><span data-out="low">$0</span> – <span data-out="high">$0</span></div>
    <div class="result-bar"><span data-out="bar"></span></div>
    <dl class="result-stats">
      <div><dt>Roof area</dt><dd data-out="area">—</dd></div>
      <div><dt>Roofing squares</dt><dd data-out="squares">—</dd></div>
      <div><dt>Installed rate</dt><dd data-out="rate">—</dd></div>
    </dl>
    <p class="result-note">Planning range for Bastrop and Central Texas, not a quote. Your exact price depends on an on-site inspection of decking, flashing, ventilation and access.</p>
    <a class="btn btn-primary btn-block" href="/contact/">Get My Exact Price <?= icon('arrow') ?></a>
  </div>
</div>
