<?php defined('SLT') || exit; ?>
<div class="tool" data-tool="transformer">
  <div class="tool__in">
    <h3>1 · Transformer size</h3>
    <div class="tool__fields">
      <label class="fld"><span>Number of fixtures</span><input type="number" min="1" max="300" value="24" data-in="n"></label>
      <label class="fld"><span>Avg. watts (or VA) each</span><input type="number" min="0.5" max="75" step="0.5" value="5" data-in="w"></label>
    </div>
    <h3 style="margin-top:26px">2 · Voltage drop on one run</h3>
    <div class="tool__fields">
      <label class="fld"><span>Load on this run (W)</span><input type="number" min="1" max="600" value="60" data-in="load"></label>
      <label class="fld"><span>Run length (ft)</span><input type="number" min="5" max="500" value="100" data-in="len"></label>
      <label class="fld"><span>Wire gauge</span><select data-in="g"><option value="4.016">16/2</option><option value="2.525">14/2</option><option value="1.588" selected>12/2</option><option value="0.999">10/2</option><option value="0.628">8/2</option></select></label>
      <label class="fld"><span>Transformer tap (V)</span><select data-in="tap"><option>12</option><option>13</option><option>14</option><option>15</option></select></label>
    </div>
  </div>
  <div class="tool__out">
    <div class="tool__hero"><small>Recommended transformer</small><strong data-out="tx">300 W</strong><span data-out="txs">120 W load ÷ 0.8 = 150 W minimum</span></div>
    <div class="tool__grid">
      <div class="stat-mini"><small>Current on run</small><strong data-out="amps">5.0 A</strong></div>
      <div class="stat-mini"><small>Voltage drop</small><strong data-out="vd">1.59 V</strong></div>
      <div class="stat-mini"><small>Voltage at end</small><strong data-out="vend">10.4 V</strong></div>
      <div class="stat-mini"><small>Best tap</small><strong data-out="best">13 V</strong></div>
    </div>
    <div class="tool__msg" data-out="msg"></div>
    <p class="tool__note">Uses round-trip conductor resistance (2 × length) and assumes the whole load sits at the end of the run (worst case). Always confirm the operating range on your fixtures' spec sheet and measure with a meter.</p>
  </div>
</div>
