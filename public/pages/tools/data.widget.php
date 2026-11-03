<?php defined('SCC') || exit; ?>
<div class="tool" data-tool="data">
  <div class="tool-head"><?= icon('sd', 22) ?><strong>4G Data &amp; microSD Storage Calculator</strong><span>Plan your SIM and card</span></div>
  <form class="tool-body" autocomplete="off">
    <div class="tool-inputs">
      <div class="field"><label for="dt-ev">Motion events per day <output data-for="ev"></output></label><input id="dt-ev" type="range" name="ev" min="1" max="200" value="25"></div>
      <div class="field"><label for="dt-clip">Average clip length <output data-for="clip" data-suffix=" s"></output></label><input id="dt-clip" type="range" name="clip" min="5" max="120" step="5" value="20"></div>
      <div class="field"><span class="lbl">Recording resolution</span><div class="seg">
        <label><input type="radio" name="res" value="2"><span>1080p</span></label>
        <label><input type="radio" name="res" value="3" checked><span>2K / 4MP</span></label>
        <label><input type="radio" name="res" value="6"><span>4K / 8MP</span></label>
      </div></div>
      <div class="field"><span class="lbl">Video codec</span><div class="seg">
        <label><input type="radio" name="codec" value="1"><span>H.264</span></label>
        <label><input type="radio" name="codec" value="0.6" checked><span>H.265 / HEVC</span></label>
      </div><small>Check the spec sheet. H.265 files are roughly 40% smaller.</small></div>
      <div class="field"><label for="dt-live">Live view per day <output data-for="live" data-suffix=" min"></output></label><input id="dt-live" type="range" name="live" min="0" max="60" value="5"></div>
      <div class="field"><span class="lbl">Live view quality</span><div class="seg">
        <label><input type="radio" name="lq" value="0.5" checked><span>Fluent / SD</span></label>
        <label><input type="radio" name="lq" value="hd"><span>Clear / HD</span></label>
      </div></div>
      <div class="field"><span class="lbl">Clips uploaded over 4G?</span><div class="seg">
        <label><input type="radio" name="up" value="1" checked><span>Yes (cloud / phone)</span></label>
        <label><input type="radio" name="up" value="0"><span>No, microSD only</span></label>
      </div></div>
      <div class="field"><label for="dt-sd">microSD card</label><select id="dt-sd" name="sd"><option value="32">32 GB</option><option value="64">64 GB</option><option value="128" selected>128 GB</option><option value="256">256 GB</option><option value="512">512 GB</option></select></div>
      <label class="chk"><input type="checkbox" name="cont" value="1"><span>Continuous 24/7 recording to card<em>Only wired or large-battery solar systems do this</em></span></label>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="result-hero"><div class="big" data-o="gb">—</div><p data-o="sum"></p></div>
      <div class="results">
        <div class="res"><b data-o="day">—</b><span>Data per day</span></div>
        <div class="res"><b data-o="plan">—</b><span>Suggested data plan</span></div>
        <div class="res"><b data-o="sdd">—</b><span>Days on microSD before overwrite</span></div>
        <div class="res"><b data-o="clips">—</b><span>Clips the card holds</span></div>
      </div>
      <h4>Monthly data breakdown</h4>
      <div class="bars" data-o="bars"></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-act="share">Copy share link</button><button type="button" class="btn btn-line btn-sm" data-act="reset">Reset</button></div>
      <p class="tool-note">Bitrates assumed (H.264): 1080p ≈ 2 Mbps, 2K ≈ 3 Mbps, 4K ≈ 6 Mbps; H.265 ≈ 60% of that. Adds ~10% for thumbnails/protocol overhead and ~60 MB/month of keep-alive traffic. Cameras with variable bitrate may use less at night or in static scenes.</p>
    </div>
  </form>
</div>
