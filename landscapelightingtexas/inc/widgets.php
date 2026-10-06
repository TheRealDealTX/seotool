<?php
// Interactive tool widgets (markup only). Behavior lives in assets/js/tools.js.
// Any page that prints one must set $P['tools_js'] = true.
defined('LLT') or die(http_response_code(404));

function qty_row(string $key, string $name, string $hint, int $val): string {
    return '<div class="qty"><div class="qty-info"><strong>' . e($name) . '</strong><small>' . e($hint) . '</small></div>'
         . '<div class="qty-ctrl"><button type="button" data-step="-1" aria-label="Fewer ' . e($name) . '">−</button>'
         . '<input type="number" min="0" max="100" value="' . $val . '" data-qty="' . $key . '" aria-label="' . e($name) . ' quantity">'
         . '<button type="button" data-step="1" aria-label="More ' . e($name) . '">+</button></div></div>';
}

function slider(string $attr, string $label, $min, $max, $step, $val, string $unit = '', string $class = ''): string {
    return '<div class="row"><label class="tl">' . e($label) . ' <span class="slider-val"><output data-out="' . $attr . '">' . $val . '</output>' . e($unit) . '</span></label>'
         . '<input class="slider ' . $class . '" type="range" min="' . $min . '" max="' . $max . '" step="' . $step . '" value="' . $val . '" data-in="' . $attr . '" aria-label="' . e($label) . '"></div>';
}

/* ---------- Cost calculator ---------- */
function widget_cost_calculator(): void { ?>
<div class="tool not-prose" data-tool="cost" id="calculator">
  <div class="tool-head"><div><p class="tool-title">Landscape Lighting Cost Calculator</p><p class="tool-sub">Planning estimates for Texas properties. Final pricing follows a site visit and lighting design.</p></div>
    <button type="button" class="btn btn-ghost btn-sm" data-reset>Reset</button></div>
  <div class="tool-cols">
    <div class="tool-body">
      <div class="row2">
        <div><label class="tl" for="c-type">Property type</label><select id="c-type" data-f="type"><option value="1">Residential</option><option value="1.15">Commercial</option></select></div>
        <div><label class="tl" for="c-area">Project area</label><select id="c-area" data-f="area">
          <option value="front">Front yard</option><option value="back">Backyard</option><option value="both" selected>Front and backyard</option>
          <option value="full">Full property</option><option value="pool">Pool or patio area</option><option value="drive">Driveway and entry</option><option value="comm">Commercial exterior</option></select></div>
      </div>
      <div class="row2">
        <div><label class="tl" for="c-quality">Fixture quality</label><select id="c-quality" data-f="quality"><option value="1">Standard</option><option value="1.3" selected>Premium (brass/copper)</option><option value="1.65">Architectural grade</option></select></div>
        <div><label class="tl" for="c-diff">Installation difficulty</label><select id="c-diff" data-f="diff"><option value="0.9">Easy access</option><option value="1" selected>Typical Texas property</option><option value="1.25">Complex (rock, roots, long runs)</option></select></div>
      </div>
      <p class="tl">Fixtures</p>
      <?= qty_row('uplights', 'Architectural uplights', 'Facades, columns, stone', 6) ?>
      <?= qty_row('path', 'Path & driveway lights', 'Walkways and drive edges', 6) ?>
      <?= qty_row('garden', 'Tree & garden lights', 'Trees, beds, accents', 4) ?>
      <?= qty_row('step', 'Step & deck lights', 'Stairs, walls, decks', 0) ?>
      <?= qty_row('pool', 'Water feature lights', 'Fountains, ponds, pool edge', 0) ?>
      <?= qty_row('security', 'Security floodlights', 'Corners, gates, garages', 0) ?>
      <p class="tl" style="margin-top:20px">Options</p>
      <div class="opt-grid">
        <label class="opt"><input type="checkbox" data-opt="smart"><span>Smart controls<small>App, zones, dimming</small></span></label>
        <label class="opt"><input type="checkbox" data-opt="zone"><span>Extra lighting zone<small>Separate circuit & timer</small></span></label>
        <label class="opt"><input type="checkbox" data-opt="removal"><span>Remove old system<small>Haul away halogen</small></span></label>
        <label class="opt"><input type="checkbox" data-opt="hardscape"><span>Hardscape work<small>Bore under walks/drive</small></span></label>
        <label class="opt"><input type="checkbox" data-opt="expansion" checked><span>Room to expand<small>+20% transformer</small></span></label>
      </div>
      <div class="row2" style="margin-top:20px">
        <div><?= slider('hours', 'Hours per night', 2, 12, 1, 6, ' h') ?></div>
        <div><label class="tl" for="c-rate">Electric rate ($/kWh)</label><input class="tool-input" id="c-rate" type="number" step="0.01" min="0.05" max="0.6" value="0.15" data-f="rate"></div>
      </div>
    </div>
    <div class="tool-body tool-result" aria-live="polite">
      <p class="result-label">Estimated installed cost</p>
      <p class="big-result" data-r="range">—</p>
      <p class="result-note" data-r="summary"></p>
      <dl class="kv">
        <div><dt>Fixtures</dt><dd data-r="count">0</dd></div>
        <div><dt>Equipment</dt><dd data-r="equip">—</dd></div>
        <div><dt>Installation labor</dt><dd data-r="labor">—</dd></div>
        <div><dt>Transformer, wire & controls</dt><dd data-r="infra">—</dd></div>
        <div><dt>Options</dt><dd data-r="opts">—</dd></div>
      </dl>
      <p class="result-label">Recommended transformer</p>
      <p class="big-result" style="font-size:2rem" data-r="xfmr">—</p>
      <div class="meter"><span data-r="loadbar"></span></div>
      <p class="meter-note" data-r="loadtext"></p>
      <dl class="kv">
        <div><dt>Connected LED load</dt><dd data-r="watts">0 W</dd></div>
        <div><dt>Monthly energy cost</dt><dd data-r="monthly">$0.00</dd></div>
        <div><dt>Yearly energy cost</dt><dd data-r="yearly">$0</dd></div>
      </dl>
      <a class="btn btn-gold btn-block" href="/quote/">Get an exact quote</a>
      <p class="result-note">Planning estimate only. Wiring distances, site conditions and the final design set the real price.</p>
    </div>
  </div>
</div>
<?php }

/* ---------- Lighting design simulator (real photo, zone masks) ---------- */
function widget_simulator(bool $compact = false): void {
    $zones = [
        'facade' => 'Facade uplights', 'trees' => 'Tree uplights', 'path' => 'Path & beds',
        'entry' => 'Entry & windows', 'accent' => 'Shrub accents',
    ];
    ?>
<div class="tool sim" data-tool="simulator">
  <?php if (!$compact): ?><div class="tool-head"><div><p class="tool-title">Lighting Design Simulator</p><p class="tool-sub">Switch zones on, dim them, change color temperature or pick a scene.</p></div></div><?php endif; ?>
  <div class="sim-stage" data-stage>
    <img class="sim-base" src="/assets/img/architectural-uplighting-1600.webp" alt="A Texas stone home at night used in the lighting simulator" width="1536" height="1024" loading="lazy">
    <?php foreach ($zones as $k => $n): ?><img class="sim-zone" data-zone-layer="<?= $k ?>" src="/assets/img/architectural-uplighting-1600.webp" alt="" width="1536" height="1024" loading="lazy"><?php endforeach; ?>
    <div class="sim-tint" data-tint></div>
    <div class="sim-moon" aria-hidden="true"></div>
  </div>
  <div class="sim-controls">
    <div class="zone-toggles">
      <?php foreach ($zones as $k => $n): ?><button type="button" class="zone-btn" data-zone="<?= $k ?>" aria-pressed="false"><i></i><?= e($n) ?></button><?php endforeach; ?>
    </div>
    <div class="scene-btns" role="group" aria-label="Scenes">
      <button type="button" data-scene="welcome">Welcome home</button><button type="button" data-scene="party">Entertaining</button>
      <button type="button" data-scene="security">Security</button><button type="button" data-scene="late">Late night</button>
      <button type="button" data-scene="all">All on</button><button type="button" data-scene="off">All off</button>
    </div>
    <div class="row2" style="margin:0">
      <div><?= slider('dim', 'Dimmer', 10, 100, 1, 85, '%') ?></div>
      <div><?= slider('kelvin', 'Color temperature', 2200, 5000, 100, 2700, 'K', 'kelvin-track') ?></div>
    </div>
    <p class="sim-readout" aria-live="polite"><span>Zones on: <strong data-r="zones">0</strong></span><span>Approx. fixtures: <strong data-r="fx">0</strong></span><span>LED load: <strong data-r="w">0 W</strong></span><span>Cost to run: <strong data-r="cost">$0</strong>/mo</span></p>
  </div>
</div>
<?php }

/* ---------- Color temperature visualizer ---------- */
function widget_kelvin(): void { ?>
<div class="tool" data-tool="kelvin">
  <div class="kv-stage">
    <img src="/assets/img/architectural-uplighting-1600.webp" alt="Stone facade lit at different color temperatures" width="1536" height="1024" loading="lazy" data-k-img>
    <div class="kv-tint" data-tint></div><div class="kv-tint2" data-tint2></div>
    <div class="kv-badge"><strong data-r="k">2700K</strong><span data-r="name">Warm white</span></div>
  </div>
  <div class="tool-body">
    <div class="seg" role="group" aria-label="Scene" style="margin-bottom:18px">
      <button type="button" class="is-on" data-img="architectural-uplighting">Stone facade</button><button type="button" data-img="oak-tree-uplighting">Live oak</button>
      <button type="button" data-img="pool-lighting">Pool</button><button type="button" data-img="garden-pathway-lighting">Garden path</button>
    </div>
    <?= slider('kelvin', 'Color temperature', 2200, 5000, 100, 2700, 'K', 'kelvin-track') ?>
    <div class="grid-2" style="gap:20px">
      <div><p class="result-label">How it reads</p><p data-r="desc" style="color:var(--muted)"></p></div>
      <div><p class="result-label">Best for</p><p data-r="best" style="color:var(--muted)"></p></div>
    </div>
  </div>
</div>
<?php }

/* ---------- Transformer + voltage drop ---------- */
function widget_transformer(): void { ?>
<div class="tool" data-tool="transformer">
  <div class="tool-head"><div><p class="tool-title">Transformer & Voltage Drop</p><p class="tool-sub">12V low-voltage systems · copper landscape cable</p></div></div>
  <div class="tool-cols">
    <div class="tool-body">
      <p class="tl">Fixtures on this run</p>
      <?= qty_row('a', 'Uplights (5 W LED)', 'Typical MR16/integrated', 8) ?>
      <?= qty_row('b', 'Path lights (3 W LED)', 'Area lights', 6) ?>
      <?= qty_row('c', 'Well/in-grade (7 W LED)', 'Higher output', 0) ?>
      <?= qty_row('d', 'Floods/tree lights (10 W LED)', 'Tall canopies', 2) ?>
      <div class="row2" style="margin-top:20px">
        <div><?= slider('len', 'Cable run to first fixture', 10, 300, 5, 100, ' ft') ?></div>
        <div><label class="tl" for="t-awg">Wire gauge</label><select id="t-awg" data-f="awg"><option value="16">16 AWG</option><option value="14">14 AWG</option><option value="12" selected>12 AWG</option><option value="10">10 AWG</option><option value="8">8 AWG</option></select></div>
      </div>
      <div class="row2">
        <div><label class="tl" for="t-method">Wiring method</label><select id="t-method" data-f="method"><option value="1">Daisy chain (load at the end)</option><option value="0.5" selected>Hub / split load</option><option value="0.65">T-method</option></select></div>
        <div><label class="tl" for="t-min">Lowest acceptable fixture voltage</label><select id="t-min" data-f="min"><option value="10.5">10.5 V (halogen)</option><option value="9" selected>9 V (most LEDs)</option></select></div>
      </div>
    </div>
    <div class="tool-body tool-result" aria-live="polite">
      <p class="result-label">Recommended transformer</p>
      <p class="big-result" data-r="xfmr">—</p>
      <div class="meter"><span data-r="bar"></span></div>
      <p class="meter-note" data-r="bartext"></p>
      <dl class="kv">
        <div><dt>Total LED load</dt><dd data-r="watts">—</dd></div>
        <div><dt>Current on the run</dt><dd data-r="amps">—</dd></div>
        <div><dt>Voltage drop</dt><dd data-r="drop">—</dd></div>
        <div><dt>Suggested tap</dt><dd data-r="tap">—</dd></div>
        <div><dt>Voltage at fixtures</dt><dd data-r="vfix">—</dd></div>
      </dl>
      <p class="result-note" data-r="advice"></p>
    </div>
  </div>
</div>
<?php }

/* ---------- Beam spread ---------- */
function widget_beam(): void { ?>
<div class="tool" data-tool="beam">
  <div class="tool-cols">
    <div class="tool-body">
      <p class="tl">Beam angle</p>
      <div class="seg" role="group" aria-label="Beam angle" style="margin-bottom:20px">
        <?php foreach ([10, 15, 25, 36, 45, 60] as $a): ?><button type="button" data-angle="<?= $a ?>"<?= $a === 36 ? ' class="is-on"' : '' ?>><?= $a ?>°</button><?php endforeach; ?>
      </div>
      <?= slider('dist', 'Distance from fixture to target', 2, 50, 1, 15, ' ft') ?>
      <?= slider('lumens', 'Fixture output', 100, 1200, 50, 350, ' lm') ?>
      <label class="tl" for="b-target">What are you lighting?</label>
      <select id="b-target" data-f="target">
        <option value="3">Column or narrow palm (≈ 2–4 ft wide)</option>
        <option value="12" selected>Small tree or crape myrtle (≈ 10–15 ft)</option>
        <option value="40">Live oak canopy (≈ 30–50 ft)</option>
        <option value="10">Wall section / facade bay (≈ 8–12 ft)</option>
        <option value="5">Sign or flag (≈ 3–6 ft)</option>
      </select>
    </div>
    <div class="tool-body tool-result" aria-live="polite">
      <svg class="beam-svg" viewBox="0 0 400 260" aria-hidden="true">
        <defs><linearGradient id="beamG" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffd58f" stop-opacity=".9"/><stop offset="1" stop-color="#ffd58f" stop-opacity=".05"/></linearGradient></defs>
        <line x1="20" y1="240" x2="380" y2="240" stroke="rgba(255,255,255,.15)"/>
        <polygon data-beam fill="url(#beamG)" points="200,240 160,20 240,20"/>
        <line data-spread x1="160" y1="20" x2="240" y2="20" stroke="#ffd58f" stroke-width="2"/>
        <rect x="190" y="236" width="20" height="10" rx="3" fill="#e9b45c"/>
        <text data-label x="200" y="14" text-anchor="middle" fill="#fff" font-size="13" font-weight="700">—</text>
      </svg>
      <p class="result-label" style="margin-top:16px">Beam diameter at target</p>
      <p class="big-result" data-r="spread">—</p>
      <dl class="kv">
        <div><dt>Lit area</dt><dd data-r="area">—</dd></div>
        <div><dt>Approx. light on target</dt><dd data-r="fc">—</dd></div>
        <div><dt>Recommended beam for your target</dt><dd data-r="rec">—</dd></div>
      </dl>
      <p class="result-note" data-r="advice"></p>
    </div>
  </div>
</div>
<?php }

/* ---------- Dusk timer ---------- */
function widget_dusk(): void {
    $cities = ['Austin' => [30.27, -97.74, 'America/Chicago'], 'Houston' => [29.76, -95.37, 'America/Chicago'], 'Dallas' => [32.78, -96.80, 'America/Chicago'],
        'Fort Worth' => [32.75, -97.33, 'America/Chicago'], 'San Antonio' => [29.42, -98.49, 'America/Chicago'], 'El Paso' => [31.76, -106.49, 'America/Denver'],
        'Corpus Christi' => [27.80, -97.40, 'America/Chicago'], 'Lubbock' => [33.58, -101.85, 'America/Chicago'], 'Amarillo' => [35.22, -101.83, 'America/Chicago'],
        'Midland' => [32.00, -102.08, 'America/Chicago'], 'McAllen' => [26.20, -98.23, 'America/Chicago'], 'Galveston' => [29.30, -94.80, 'America/Chicago'],
        'Plano' => [33.02, -96.70, 'America/Chicago'], 'The Woodlands' => [30.17, -95.49, 'America/Chicago'], 'Waco' => [31.55, -97.15, 'America/Chicago'],
        'Tyler' => [32.35, -95.30, 'America/Chicago'], 'Laredo' => [27.53, -99.51, 'America/Chicago'], 'Abilene' => [32.45, -99.73, 'America/Chicago']];
    ksort($cities); ?>
<div class="tool" data-tool="dusk">
  <div class="tool-cols">
    <div class="tool-body">
      <div class="row2">
        <div><label class="tl" for="d-city">City</label><select id="d-city" data-f="city">
          <?php foreach ($cities as $n => [$la, $lo, $tz]) echo '<option value="' . $la . ',' . $lo . ',' . $tz . '"' . ($n === 'Austin' ? ' selected' : '') . '>' . e($n) . '</option>'; ?>
        </select></div>
        <div><label class="tl" for="d-date">Date</label><input class="tool-input" id="d-date" type="date" data-f="date"></div>
      </div>
      <label class="tl" for="d-off">Lights off at</label>
      <select id="d-off" data-f="off" style="margin-bottom:20px">
        <option value="22">10:00 pm</option><option value="23" selected>11:00 pm</option><option value="0">Midnight</option><option value="1">1:00 am</option><option value="dawn">Dawn</option>
      </select>
      <div class="table-wrap"><table class="month-table"><thead><tr><th>Month</th><th>Sunset</th><th>Set lights on</th></tr></thead><tbody data-r="months"></tbody></table></div>
    </div>
    <div class="tool-body tool-result" aria-live="polite">
      <p class="result-label">Sunset</p>
      <p class="big-result" data-r="sunset">—</p>
      <dl class="kv">
        <div><dt>Civil dusk (sky fully dark-blue)</dt><dd data-r="dusk">—</dd></div>
        <div><dt>Best time to switch on</dt><dd data-r="on">—</dd></div>
        <div><dt>Sunrise</dt><dd data-r="sunrise">—</dd></div>
        <div><dt>Hours of lighting tonight</dt><dd data-r="hours">—</dd></div>
      </dl>
      <p class="result-note" data-r="advice"></p>
    </div>
  </div>
</div>
<?php }

/* ---------- Energy savings ---------- */
function widget_energy(): void { ?>
<div class="tool" data-tool="energy">
  <div class="tool-cols">
    <div class="tool-body">
      <?= slider('n', 'Number of fixtures', 1, 80, 1, 20) ?>
      <?= slider('hw', 'Halogen lamp wattage', 10, 50, 5, 20, ' W') ?>
      <?= slider('lw', 'Equivalent LED wattage', 2, 12, 1, 4, ' W') ?>
      <?= slider('h', 'Hours per night', 2, 13, 1, 6, ' h') ?>
      <div class="row2">
        <div><label class="tl" for="e-rate">Electric rate ($/kWh)</label><input class="tool-input" id="e-rate" type="number" step="0.01" min="0.05" max="0.6" value="0.15" data-f="rate"></div>
        <div><label class="tl" for="e-cost">LED retrofit cost per fixture ($)</label><input class="tool-input" id="e-cost" type="number" step="5" min="0" value="45" data-f="cost"></div>
      </div>
    </div>
    <div class="tool-body tool-result" aria-live="polite">
      <p class="result-label">You save every year</p>
      <p class="big-result" data-r="save">—</p>
      <div style="display:grid;gap:12px;margin:18px 0">
        <div><div class="kv" style="margin:0"><div><span>Halogen</span><strong data-r="hal">—</strong></div></div><div class="meter warn"><span data-r="halbar"></span></div></div>
        <div><div class="kv" style="margin:0"><div><span>LED</span><strong data-r="led">—</strong></div></div><div class="meter"><span data-r="ledbar"></span></div></div>
      </div>
      <dl class="kv">
        <div><dt>Energy saved per year</dt><dd data-r="kwh">—</dd></div>
        <div><dt>Retrofit payback (energy only)</dt><dd data-r="payback">—</dd></div>
        <div><dt>Lamp changes avoided over 10 years</dt><dd data-r="lamps">—</dd></div>
        <div><dt>10-year savings</dt><dd data-r="ten">—</dd></div>
      </dl>
      <p class="result-note">Assumes halogen lamps last about 3,000 hours and LEDs 40,000. Transformer losses not included.</p>
    </div>
  </div>
</div>
<?php }

/* ---------- Style quiz ---------- */
function widget_quiz(): void { ?>
<div class="tool" data-tool="quiz">
  <div class="quiz-progress"><span data-r="progress"></span></div>
  <div class="tool-body" style="padding:clamp(24px,4vw,44px)" data-r="stage" aria-live="polite"></div>
</div>
<?php }
