<?php defined('SLT') || exit; ?>
<div class="tool" data-tool="sunset" style="grid-template-columns:1fr">
  <div class="tool__in">
    <div class="tool__fields tool__fields--3">
      <label class="fld"><span>Lights on</span><select data-in="on"><option value="0">At sunset</option><option value="15" selected>15 min after sunset</option><option value="30">30 min after sunset</option></select></label>
      <label class="fld"><span>Lights off</span><select data-in="off"><option value="22">10:00 p.m.</option><option value="23" selected>11:00 p.m.</option><option value="24">Midnight</option><option value="25">1:00 a.m.</option><option value="dawn">Sunrise (dusk to dawn)</option></select></label>
      <label class="fld"><span>System load (W)</span><input type="number" min="1" max="3000" value="150" data-in="w"></label>
    </div>
    <div class="tool__grid tool__grid--4" style="margin:20px 0">
      <div class="stat-mini"><small>Sunset today</small><strong data-out="today">—</strong></div>
      <div class="stat-mini"><small>Run-hours / year</small><strong data-out="hrs">—</strong></div>
      <div class="stat-mini"><small>kWh / year</small><strong data-out="kwh">—</strong></div>
      <div class="stat-mini"><small>Cost / yr @ $0.15</small><strong data-out="cost">—</strong></div>
    </div>
    <div class="table-wrap" style="margin:0"><table class="ktable"><thead><tr><th>Month</th><th>Sunset (15th)</th><th>Sunrise</th><th>Lights on</th><th>Hours / night</th></tr></thead><tbody data-out="rows"></tbody></table></div>
    <p class="tool__note">Calculated for Spring, TX (30.08° N, 95.42° W) with Central Time and daylight saving applied. An astronomical timer follows these shifts automatically.</p>
  </div>
</div>
