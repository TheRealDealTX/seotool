<?php defined('SLT') || exit; ?>
<div class="tool" data-tool="led">
  <div class="tool__in">
    <h3>Your current system</h3>
    <div class="tool__fields">
      <label class="fld"><span>Fixtures</span><input type="number" min="1" max="300" value="25" data-in="n"></label>
      <label class="fld"><span>Halogen watts each</span><input type="number" min="5" max="75" value="20" data-in="hw"></label>
      <label class="fld"><span>LED watts each</span><input type="number" min="1" max="20" step="0.5" value="5" data-in="lw"></label>
      <label class="fld"><span>Hours per night</span><input type="number" min="1" max="14" step="0.5" value="6" data-in="h"></label>
      <label class="fld"><span>Rate ($/kWh)</span><input type="number" min="0.01" max="1" step="0.01" value="0.15" data-in="r"></label>
      <label class="fld"><span>Halogen lamp cost ($)</span><input type="number" min="0" max="50" value="8" data-in="lamp"><small>Halogen lamps often last ~2,000–4,000 hrs.</small></label>
      <label class="fld fld--full"><span>Upgrade budget per fixture ($, optional)</span><input type="number" min="0" max="1000" value="0" data-in="cost"><small>Enter your quote to estimate payback.</small></label>
    </div>
  </div>
  <div class="tool__out">
    <div class="tool__hero"><small>Estimated yearly savings</small><strong data-out="save">$123</strong><span data-out="pct">75% less energy</span></div>
    <div class="bars">
      <div class="bar"><span>Halogen</span><div class="bar__track"><div class="bar__fill bar__fill--hal" data-out="bh"></div></div><b data-out="ch">$164</b></div>
      <div class="bar"><span>LED</span><div class="bar__track"><div class="bar__fill" data-out="bl"></div></div><b data-out="cl">$41</b></div>
    </div>
    <div class="tool__grid" style="margin-top:16px">
      <div class="stat-mini"><small>kWh saved / yr</small><strong data-out="kwh">821</strong></div>
      <div class="stat-mini"><small>Lamp swaps avoided / yr</small><strong data-out="lamps">27</strong></div>
      <div class="stat-mini"><small>Lamp cost avoided</small><strong data-out="lampc">$219</strong></div>
      <div class="stat-mini"><small>Payback</small><strong data-out="pay">—</strong></div>
    </div>
    <p class="tool__note">Assumes 365 nights a year and an average 3,000-hour halogen lamp life. Labor, transformer changes and fixture replacement are not included.</p>
  </div>
</div>
