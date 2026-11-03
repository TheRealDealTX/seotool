<?php defined('SCC') || exit; ?>
<div class="tool" data-tool="battery">
  <div class="tool-head"><?= icon('battery', 22) ?><strong>Solar Camera Battery &amp; Power Calculator</strong><span>Energy in vs energy out</span></div>
  <form class="tool-body" autocomplete="off">
    <div class="tool-inputs">
      <div class="row2">
        <div class="field"><label for="bt-mah">Battery (mAh)</label><input id="bt-mah" type="number" name="mah" value="10000" min="500" max="60000" step="100"><small>On the spec sheet, e.g. 5,000–13,000 mAh</small></div>
        <div class="field"><label for="bt-v">Cell voltage</label><select id="bt-v" name="v"><option value="3.6">3.6 V Li-ion</option><option value="3.7" selected>3.7 V Li-ion</option><option value="3.2">3.2 V LiFePO4</option><option value="7.4">7.4 V pack</option><option value="12">12 V battery</option></select></div>
      </div>
      <div class="field"><label for="bt-ev">Motion events per day <output data-for="ev"></output></label><input id="bt-ev" type="range" name="ev" min="0" max="200" step="1" value="30"><small>Quiet backyard 5–15 · front of house 20–50 · busy street or driveway 80+</small></div>
      <div class="field"><label for="bt-clip">Average clip length <output data-for="clip" data-suffix=" s"></output></label><input id="bt-clip" type="range" name="clip" min="5" max="120" step="5" value="20"></div>
      <div class="field"><label for="bt-live">Live view per day <output data-for="live" data-suffix=" min"></output></label><input id="bt-live" type="range" name="live" min="0" max="60" step="1" value="3"></div>
      <div class="field"><span class="lbl">Connection</span><div class="seg">
        <label><input type="radio" name="net" value="wifi" checked><span>Wi‑Fi</span></label>
        <label><input type="radio" name="net" value="lte"><span>4G LTE SIM</span></label>
      </div></div>
      <div class="field"><span class="lbl">Video &amp; night mode</span><div class="seg">
        <label><input type="radio" name="res" value="1" checked><span>2K / 3K</span></label>
        <label><input type="radio" name="res" value="1.35"><span>4K</span></label>
        <label><input type="checkbox" name="spot" value="1"><span>Color spotlight at night</span></label>
      </div></div>
      <div class="row2">
        <div class="field"><label for="bt-pw">Panel size (W)</label><select id="bt-pw" name="pw"><option value="2.5">2.5 W (built-in)</option><option value="3">3 W</option><option value="5" selected>5 W</option><option value="6">6 W</option><option value="10">10 W</option><option value="20">20 W</option></select></div>
        <div class="field"><label for="bt-n">Cameras</label><input id="bt-n" type="number" name="n" value="1" min="1" max="16"></div>
      </div>
      <div class="field"><label for="bt-psh">Peak sun hours <output data-for="psh" data-dec="1" data-suffix=" h"></output></label><input id="bt-psh" type="range" name="psh" min="0.5" max="7" step="0.1" value="2.5"><small>Winter: ~1–2 h (UK, Pacific NW, Canada), 2–3 h (most of US), 4+ h (Southwest). Summer: 4–7 h.</small></div>
      <div class="field"><span class="lbl">Panel exposure</span><div class="seg">
        <label><input type="radio" name="exp" value="1" checked><span>Full sun</span></label>
        <label><input type="radio" name="exp" value="0.6"><span>Part shade</span></label>
        <label><input type="radio" name="exp" value="0.25"><span>Mostly shade</span></label>
      </div></div>
      <div class="field"><label for="bt-cloud">Cloudy days in a row to simulate <output data-for="cloud"></output></label><input id="bt-cloud" type="range" name="cloud" min="0" max="10" step="1" value="3"></div>
      <label class="chk"><input type="checkbox" name="cold" value="1"><span>Freezing temperatures<em>Cuts usable capacity ~20% and stops charging below 32 °F / 0 °C on most cameras</em></span></label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="result-hero"><div class="big" data-o="days">—</div><p data-o="sum"></p></div>
      <div class="verdict" data-o="verdict"></div>
      <div class="results">
        <div class="res"><b data-o="use">—</b><span>Energy used per camera per day</span></div>
        <div class="res"><b data-o="gain">—</b><span>Solar harvest per day (average)</span></div>
        <div class="res"><b data-o="cap">—</b><span>Usable battery energy</span></div>
        <div class="res"><b data-o="need">—</b><span>Minimum panel for this site</span></div>
      </div>
      <h4>Battery level over 14 days (cloudy spell starts day 4)</h4>
      <div class="chart" data-o="chart"></div>
      <h4>Where the energy goes</h4>
      <div class="bars" data-o="bars"></div>
      <div data-o="multi"></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-act="share">Copy share link</button><button type="button" class="btn btn-line btn-sm" data-act="reset">Reset</button></div>
      <p class="tool-note">Estimates use typical draw figures for battery cameras (deep sleep between events, ~3 W while recording on Wi‑Fi, ~4 W on LTE) and 70% panel-to-battery efficiency. Real cameras vary by model and firmware.</p>
    </div>
  </form>
</div>
