<?php defined('SLT') || exit; ?>
<div class="tool" data-tool="estimator">
  <div class="tool__in">
    <h3>Describe your property</h3>
    <div class="tool__fields">
      <label class="fld"><span>Front facade width (ft)</span><input type="number" min="0" max="400" value="70" data-in="facade"></label>
      <label class="fld"><span>Columns / entry features</span><input type="number" min="0" max="20" value="2" data-in="cols"></label>
      <label class="fld"><span>Walkway length (ft)</span><input type="number" min="0" max="500" value="40" data-in="walk"></label>
      <label class="fld"><span>Driveway length (ft)</span><input type="number" min="0" max="800" value="0" data-in="drive"></label>
      <label class="fld"><span>Large trees (oaks, pines)</span><input type="number" min="0" max="40" value="2" data-in="big"></label>
      <label class="fld"><span>Small trees / palms / ornamentals</span><input type="number" min="0" max="40" value="2" data-in="small"></label>
      <label class="fld"><span>Patio / deck area (sq ft)</span><input type="number" min="0" max="5000" value="300" data-in="patio"></label>
      <label class="fld"><span>Exterior steps</span><input type="number" min="0" max="60" value="3" data-in="steps"></label>
      <label class="fld fld--full"><span>Style</span><select data-in="style"><option value="0.8">Subtle &amp; minimal</option><option value="1" selected>Balanced</option><option value="1.25">Dramatic showcase</option></select></label>
    </div>
  </div>
  <div class="tool__out">
    <div class="tool__hero"><small>Estimated fixtures</small><strong data-out="total">22</strong><span data-out="sum">planning-level estimate</span></div>
    <table class="ktable"><thead><tr><th>Area</th><th>Fixtures</th><th>Approx. W</th></tr></thead><tbody data-out="rows"></tbody></table>
    <div class="tool__grid" style="margin-top:14px">
      <div class="stat-mini"><small>Total LED load</small><strong data-out="watts">110 W</strong></div>
      <div class="stat-mini"><small>Suggested transformer</small><strong data-out="tx">300 W</strong></div>
    </div>
    <p class="tool__note">Rule-of-thumb spacing only. A site walkthrough refines every number: good design often uses fewer, better-placed fixtures.</p>
  </div>
</div>
