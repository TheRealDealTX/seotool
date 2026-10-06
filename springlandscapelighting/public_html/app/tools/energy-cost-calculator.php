<?php defined('SLT') || exit; ?>
<div class="tool" data-tool="energy">
  <div class="tool__in">
    <h3>System details</h3>
    <div class="tool__fields">
      <label class="fld"><span>Number of fixtures</span><input type="number" min="1" max="500" value="20" data-in="n" inputmode="numeric"></label>
      <label class="fld"><span>Avg. watts per fixture</span><input type="number" min="0.5" max="100" step="0.1" value="5" data-in="w" inputmode="decimal"><small>LED landscape fixtures are often 3–12 W.</small></label>
      <label class="fld"><span>Hours per night</span><input type="number" min="0.5" max="14" step="0.5" value="6" data-in="h" inputmode="decimal"></label>
      <label class="fld"><span>Nights per month</span><input type="number" min="1" max="31" value="30" data-in="d" inputmode="numeric"></label>
      <label class="fld fld--full"><span>Electricity rate ($ per kWh)</span><input type="number" min="0.01" max="1" step="0.01" value="0.16" data-in="r" inputmode="decimal"><small>Use the all-in average price from your bill or Electricity Facts Label.</small></label>
    </div>
    <div class="presets" style="margin-top:16px"><button type="button" class="chip" data-set='{"n":10,"w":4,"h":5}'>Small</button><button type="button" class="chip" data-set='{"n":20,"w":5,"h":6}'>Medium</button><button type="button" class="chip" data-set='{"n":40,"w":7,"h":8}'>Large</button><button type="button" class="chip" data-set='{"w":20}'>Halogen (20 W)</button></div>
  </div>
  <div class="tool__out">
    <div class="tool__hero"><small>Estimated monthly cost</small><strong data-out="mo">$2.88</strong><span>to run your landscape lighting</span></div>
    <div class="tool__grid">
      <div class="stat-mini"><small>System load</small><strong data-out="tw">100 W</strong></div>
      <div class="stat-mini"><small>Per night</small><strong data-out="kn">0.60 kWh</strong></div>
      <div class="stat-mini"><small>Per month</small><strong data-out="km">18.0 kWh</strong></div>
      <div class="stat-mini"><small>Per year</small><strong data-out="ky">216 kWh</strong></div>
      <div class="stat-mini"><small>Cost per night</small><strong data-out="cn">$0.10</strong></div>
      <div class="stat-mini"><small>Cost per year</small><strong data-out="cy">$34.56</strong></div>
    </div>
    <div class="tool__msg" data-out="msg">That is a relatively low operating cost.</div>
    <p class="tool__note">Planning estimate only. Transformer losses, dimming, voltage drop and billing structure affect real usage.</p>
  </div>
</div>
