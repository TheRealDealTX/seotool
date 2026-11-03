<?php defined('SCC') || (http_response_code(404) && exit); ?>
<div class="tool" data-tool="cost">
  <div class="tool-head"><?= icon('dollar', 22) ?><strong>Solar vs Wired Camera Cost Calculator</strong><span>Total cost of ownership</span></div>
  <form class="tool-body" autocomplete="off">
    <div class="tool-inputs">
      <div class="row2">
        <div class="field"><label for="co-n">Cameras</label><input id="co-n" type="number" name="n" value="4" min="1" max="32"></div>
        <div class="field"><label for="co-y">Years to compare</label><select id="co-y" name="y"><option value="3">3</option><option value="5" selected>5</option><option value="8">8</option><option value="10">10</option></select></div>
      </div>
      <div class="field"><label for="co-run">Average cable run per camera <output data-for="run" data-suffix=" ft"></output></label><input id="co-run" type="range" name="run" min="10" max="500" step="10" value="60"></div>
      <div class="field"><span class="lbl">How would the cable be run?</span><div class="seg">
        <label><input type="radio" name="route" value="0" checked><span>Along walls / attic</span></label>
        <label><input type="radio" name="route" value="1"><span>Trenched underground</span></label>
      </div></div>
      <div class="field"><span class="lbl">Installation</span><div class="seg">
        <label><input type="radio" name="pro" value="0" checked><span>DIY</span></label>
        <label><input type="radio" name="pro" value="1"><span>Professional</span></label>
      </div></div>
      <p class="toc-title" style="margin-top:18px">Solar camera assumptions</p>
      <div class="row2">
        <div class="field"><label for="co-sp">Camera + panel ($)</label><input id="co-sp" type="number" name="sp" value="150" min="0" step="10"></div>
        <div class="field"><label for="co-sub">Cloud plan ($/mo, all cams)</label><input id="co-sub" type="number" name="sub" value="0" min="0" step="1"></div>
      </div>
      <div class="field"><label for="co-bat">Battery replacement ($ per camera, every 3 yrs)</label><input id="co-bat" type="number" name="bat" value="40" min="0" step="5"></div>
      <p class="toc-title" style="margin-top:18px">Wired PoE assumptions</p>
      <div class="row2">
        <div class="field"><label for="co-wp">PoE camera ($)</label><input id="co-wp" type="number" name="wp" value="110" min="0" step="10"></div>
        <div class="field"><label for="co-nvr">NVR + hard drive ($)</label><input id="co-nvr" type="number" name="nvr" value="250" min="0" step="10"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="co-kwh">Electricity ($/kWh)</label><input id="co-kwh" type="number" name="kwh" value="0.17" min="0" step="0.01"></div>
        <div class="field"><label for="co-tr">Trenching ($/ft)</label><input id="co-tr" type="number" name="tr" value="8" min="0" step="1"></div>
      </div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="result-hero"><div class="big" data-o="win">—</div><p data-o="sum"></p></div>
      <div class="results">
        <div class="res"><b data-o="s">—</b><span>Solar total</span></div>
        <div class="res"><b data-o="w">—</b><span>Wired PoE total</span></div>
        <div class="res"><b data-o="s1">—</b><span>Solar per camera</span></div>
        <div class="res"><b data-o="w1">—</b><span>Wired per camera</span></div>
      </div>
      <h4>Cumulative cost by year</h4>
      <div class="chart" data-o="chart"></div>
      <p class="tool-note"><span style="color:#f97316">━</span> solar &nbsp; <span style="color:#1d4ed8">━</span> wired PoE</p>
      <h4>Wired cost breakdown</h4>
      <div class="bars" data-o="bars"></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-act="share">Copy share link</button><button type="button" class="btn btn-line btn-sm" data-act="reset">Reset</button></div>
      <p class="tool-note">Defaults are typical US prices in late 2026: Cat6 outdoor cable ≈ $0.40/ft, conduit ≈ $0.60/ft when trenched, pro install ≈ $150 per wired drop and ≈ $60 per solar camera, PoE draw ≈ 6 W per camera + 15 W NVR. Edit any value to match your quotes.</p>
    </div>
  </form>
</div>
