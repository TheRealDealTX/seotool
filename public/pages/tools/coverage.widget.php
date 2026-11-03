<?php defined('SCC') || (http_response_code(404) && exit); ?>
<div class="tool" data-tool="coverage">
  <div class="tool-head"><?= icon('eye', 22) ?><strong>Camera Coverage &amp; Detail Calculator</strong><span>Field of view + pixel density</span></div>
  <form class="tool-body" autocomplete="off">
    <div class="tool-inputs">
      <div class="field"><label for="cv-res">Camera resolution</label>
        <select id="cv-res" name="hp"><option value="1920">1080p (1920 px wide)</option><option value="2304">3MP (2304 px)</option><option value="2560" selected>2K / 4MP (2560 px)</option><option value="2880">5MP (2880 px)</option><option value="3840">4K / 8MP (3840 px)</option></select>
      </div>
      <div class="field"><label for="cv-fov">Horizontal field of view <output data-for="fov" data-suffix="°"></output></label><input id="cv-fov" type="range" name="fov" min="20" max="160" value="105"><small>Wide cameras 100–130°, telephoto lenses 30–50°. Use the horizontal (not diagonal) figure.</small></div>
      <div class="field"><span class="lbl">Units</span><div class="seg">
        <label><input type="radio" name="u" value="ft" checked><span>Feet</span></label>
        <label><input type="radio" name="u" value="m"><span>Meters</span></label>
      </div></div>
      <div class="field"><label for="cv-d">Distance to target <output data-for="d"></output></label><input id="cv-d" type="range" name="d" min="5" max="150" value="30"><small>e.g. camera to the end of the driveway or the gate</small></div>
    </div>
    <div class="tool-out" aria-live="polite">
      <div class="result-hero"><div class="big" data-o="w">—</div><p data-o="sum"></p></div>
      <div class="chart" data-o="viz"></div>
      <h4>Maximum distance for each level of detail</h4>
      <div class="table-wrap"><table class="table"><thead><tr><th>Level</th><th>Needs</th><th>Max distance</th></tr></thead><tbody data-o="tbl"></tbody></table></div>
      <div class="btn-row"><button type="button" class="btn btn-line btn-sm" data-act="share">Copy share link</button></div>
      <p class="tool-note">Detail levels follow the DORI pixel-density guideline from IEC/EN 62676-4: detect 25 px/m, observe 62 px/m, recognize 125 px/m, identify 250 px/m. Compression, night mode and motion blur reduce real-world detail.</p>
    </div>
  </form>
</div>
