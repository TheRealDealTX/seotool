<?php defined('SLT') || exit; require_once APP . '/partials/house-scene.php'; $GLOBALS["VIZ_N"] = ($GLOBALS["VIZ_N"] ?? 0) + 1; $vn = $GLOBALS["VIZ_N"]; ?>
<div class="viz" data-tool="visualizer">
  <div class="viz__stage scene win-on" style="--lc:#ffc27a;--int:1">
    <?= house_scene('viz' . $vn, true, true, 'xMidYMax meet') ?>
    <div class="viz__badge"><i></i><span data-out="kname">2700K · Warm white</span></div>
  </div>
  <div class="viz__panel">
    <div class="viz__col">
    <h3>Design your night</h3>
    <p>Switch layers on and off, then tune the color and brightness. Every setting updates the estimate below.</p>
    <div class="presets" role="group" aria-label="Presets">
      <button type="button" class="chip" data-preset="subtle">Subtle</button>
      <button type="button" class="chip is-on" data-preset="balanced">Balanced</button>
      <button type="button" class="chip" data-preset="showcase">Showcase</button>
      <button type="button" class="chip" data-preset="welcome">Path &amp; entry</button>
    </div>
    <div class="toggles">
      <label class="tgl"><?= icon('house') ?>Architectural<input type="checkbox" data-layer="arch" checked><span class="tgl__sw"></span></label>
      <label class="tgl"><?= icon('footprints') ?>Path &amp; driveway<input type="checkbox" data-layer="path" checked><span class="tgl__sw"></span></label>
      <label class="tgl"><?= icon('trees') ?>Trees &amp; garden<input type="checkbox" data-layer="tree" checked><span class="tgl__sw"></span></label>
      <label class="tgl"><?= icon('waves') ?>Patio &amp; outdoor living<input type="checkbox" data-layer="patio" checked><span class="tgl__sw"></span></label>
    </div>
    </div>
    <div class="viz__col">
    <label class="rng"><span class="rng__top">Color temperature <output data-out="k">2700K</output></span><input class="kelvin" type="range" min="2200" max="5000" step="100" value="2700" data-in="k"></label>
    <label class="rng"><span class="rng__top">Brightness <output data-out="int">100%</output></span><input type="range" min="20" max="100" step="5" value="100" data-in="int"></label>
    </div>
    <div class="viz__col">
    <div class="viz__stats">
      <div class="stat-mini"><small>Fixtures</small><strong data-out="fx">28</strong></div>
      <div class="stat-mini"><small>Est. load</small><strong data-out="w">150 W</strong></div>
      <div class="stat-mini"><small>Per month*</small><strong data-out="mo">$3.17</strong></div>
      <div class="stat-mini"><small>Transformer</small><strong data-out="tx">300 W</strong></div>
    </div>
    <p class="tool__note">*Illustrative: 6 hours a night at $0.15/kWh with typical LED wattages. Real designs vary by property.</p>
    </div>
  </div>
</div>
