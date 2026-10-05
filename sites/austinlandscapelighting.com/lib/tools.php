<?php
/**
 * Markup for the interactive tools. The logic lives in assets/js/tools.js and
 * is keyed on the data-tool attribute. Each tool_*() returns HTML that can be
 * embedded on its own page or inside a blog post.
 */
declare(strict_types=1);
if (!defined('ALL_SITE')) { http_response_code(404); exit; }

function tool_markup(string $slug, bool $embedded = false): string
{
    $fn = 'tool_' . str_replace('-', '_', $slug);
    if (!function_exists($fn)) {
        return '';
    }
    $html = $fn();
    if ($embedded) {
        $t = tools()[$slug];
        return '<aside class="tool-embed" aria-label="' . e($t['name']) . '"><p class="eyebrow">Interactive tool</p><h3>' . e($t['name']) . '</h3>' . $html . '<p class="tool-embed__link"><a href="' . e($t['path']) . '">Open the full ' . e($t['name']) . ' ' . icon('arrow', 'ico ico--sm') . '</a></p></aside>';
    }
    return $html;
}

function field_number(string $name, string $label, int|float $value, int|float $min, int|float $max, int|float $step = 1, string $hint = ''): string
{
    $h = $hint ? '<small>' . e($hint) . '</small>' : '';
    return '<label class="field"><span>' . e($label) . '</span><input type="number" name="' . e($name) . '" value="' . $value . '" min="' . $min . '" max="' . $max . '" step="' . $step . '" inputmode="decimal">' . $h . '</label>';
}

function field_range(string $name, string $label, int|float $value, int|float $min, int|float $max, int|float $step = 1, string $unit = ''): string
{
    return '<label class="field field--range"><span>' . e($label) . ' <output name="' . e($name) . '_out">' . $value . '</output>' . e($unit) . '</span><input type="range" name="' . e($name) . '" value="' . $value . '" min="' . $min . '" max="' . $max . '" step="' . $step . '"></label>';
}

function field_select(string $name, string $label, array $options, string $selected = ''): string
{
    $o = '';
    foreach ($options as $val => $text) {
        $sel = (string) $val === $selected ? ' selected' : '';
        $o .= '<option value="' . e((string) $val) . '"' . $sel . '>' . e($text) . '</option>';
    }
    return '<label class="field"><span>' . e($label) . '</span><select name="' . e($name) . '">' . $o . '</select></label>';
}

function tool_fixture_calculator(): string
{
    return '<div class="tool" data-tool="fixtures">
  <form class="tool__form form-grid" onsubmit="return false">
    ' . field_number('facade', 'Front facade width (ft)', 48, 0, 400, 1, 'Measure along the street-facing wall') . '
    ' . field_select('stories', 'Stories', ['1' => 'One story', '2' => 'Two stories', '3' => 'Three or more'], '1') . '
    ' . field_number('columns', 'Columns, piers or gables to accent', 2, 0, 30) . '
    ' . field_number('trees_small', 'Small trees / ornamentals (under 15 ft)', 2, 0, 40) . '
    ' . field_number('trees_large', 'Large trees (15 ft and taller)', 1, 0, 40) . '
    ' . field_number('path', 'Walkway and driveway edge to light (ft)', 40, 0, 1000, 5) . '
    ' . field_number('steps', 'Sets of steps', 1, 0, 20) . '
    ' . field_select('patio', 'Patio or deck', ['0' => 'None', '1' => 'Small (under 200 sq ft)', '2' => 'Medium (200 to 500 sq ft)', '3' => 'Large / outdoor kitchen'], '1') . '
    ' . field_select('pool', 'Pool or water feature', ['0' => 'No', '1' => 'Yes'], '0') . '
    ' . field_number('beds', 'Garden beds or planting areas', 2, 0, 30) . '
  </form>
  <div class="tool__result" aria-live="polite">
    <div class="tool__hero"><span class="tool__big" data-out="total">0</span><span class="tool__biglabel">fixtures recommended</span></div>
    <ul class="bars" data-out="bars"></ul>
    <dl class="tool__kv">
      <div><dt>Transformer</dt><dd data-out="transformer">–</dd></div>
      <div><dt>System wattage (LED)</dt><dd data-out="watts">–</dd></div>
      <div><dt>Planning range</dt><dd data-out="range">–</dd></div>
      <div><dt>Typical install time</dt><dd data-out="time">–</dd></div>
    </dl>
    <p class="tool__note" data-out="note"></p>
    <p class="tool__fine">Planning estimate only. Fixture counts depend on beam spreads, tree canopy, facade texture and how much contrast you prefer. Your free on-site design from Austin Landscape Lighting is exact.</p>
    <a class="btn btn--primary" href="/contact/">Get an exact design and quote ' . icon('arrow') . '</a>
  </div>
</div>';
}

function tool_cost_estimator(): string
{
    return '<div class="tool" data-tool="cost">
  <form class="tool__form form-grid" onsubmit="return false">
    ' . field_range('fixtures', 'Fixtures', 18, 4, 80, 1, '') . '
    ' . field_select('grade', 'Fixture grade', ['good' => 'Good: cast brass, integrated LED', 'better' => 'Better: machined brass, replaceable LED lamps', 'best' => 'Best: premium brass/copper, adjustable optics'], 'better') . '
    ' . field_select('controls', 'Controls', ['timer' => 'Astronomic timer', 'photocell' => 'Photocell + timer', 'smart' => 'Smart Wi-Fi/Bluetooth with zones'], 'photocell') . '
    ' . field_select('zones', 'Lighting zones', ['1' => 'One zone', '2' => 'Two zones (front and back)', '3' => 'Three or more zones'], '1') . '
    ' . field_select('terrain', 'Site conditions', ['easy' => 'Open beds, mulch, turf', 'mixed' => 'Some hardscape crossings or slopes', 'hard' => 'Rock, retaining walls, long wire runs'], 'easy') . '
    ' . field_select('design', 'Design', ['included' => 'Design included with installation', 'plan' => 'Stand-alone paid lighting plan'], 'included') . '
  </form>
  <div class="tool__result" aria-live="polite">
    <div class="tool__hero"><span class="tool__big" data-out="range">–</span><span class="tool__biglabel">planning range, installed</span></div>
    <ul class="bars" data-out="bars"></ul>
    <dl class="tool__kv">
      <div><dt>Per fixture, all-in</dt><dd data-out="perfixture">–</dd></div>
      <div><dt>Transformer size</dt><dd data-out="transformer">–</dd></div>
      <div><dt>Monthly energy (6 h/night)</dt><dd data-out="energy">–</dd></div>
      <div><dt>Warranty</dt><dd>2-year workmanship + fixture warranties</dd></div>
    </dl>
    <p class="tool__fine">Ranges reflect typical Austin Landscape Lighting projects and are not a quote. Your written estimate is itemized and firm.</p>
    <a class="btn btn--primary" href="/contact/">Request an itemized estimate ' . icon('arrow') . '</a>
  </div>
</div>';
}

function tool_led_savings_calculator(): string
{
    return '<div class="tool" data-tool="led">
  <form class="tool__form form-grid" onsubmit="return false">
    ' . field_number('fixtures', 'Number of fixtures', 16, 1, 200) . '
    ' . field_select('halogen', 'Current halogen lamp', ['20' => '20 W (MR16, path lights)', '35' => '35 W (MR16 uplights)', '50' => '50 W (PAR36 / large uplights)'], '35') . '
    ' . field_select('led', 'LED replacement', ['3' => '3 W (path light)', '5' => '5 W (standard uplight)', '7' => '7 W (bright uplight)', '9' => '9 W (large tree)'], '5') . '
    ' . field_number('hours', 'Hours on per night', 6, 1, 14, 0.5) . '
    ' . field_number('rate', 'Electricity rate ($/kWh)', 0.14, 0.05, 0.60, 0.01, 'Austin Energy residential averages about $0.14') . '
    ' . field_number('lamp_cost', 'Halogen lamp replacement cost ($ each)', 6, 0, 40, 0.5, 'Halogens last about 2,000 h; LEDs 40,000 h') . '
  </form>
  <div class="tool__result" aria-live="polite">
    <div class="tool__hero"><span class="tool__big" data-out="annual">–</span><span class="tool__biglabel">saved per year</span></div>
    <div class="compare-bars">
      <div class="compare-bars__row"><span>Halogen</span><span class="compare-bars__bar"><i data-out="bar_h" style="--w:100%"></i></span><b data-out="kwh_h">–</b></div>
      <div class="compare-bars__row"><span>LED</span><span class="compare-bars__bar compare-bars__bar--led"><i data-out="bar_l" style="--w:15%"></i></span><b data-out="kwh_l">–</b></div>
    </div>
    <dl class="tool__kv">
      <div><dt>Power draw</dt><dd data-out="watts">–</dd></div>
      <div><dt>Energy saved per year</dt><dd data-out="kwh">–</dd></div>
      <div><dt>Lamp replacements avoided (10 yrs)</dt><dd data-out="lamps">–</dd></div>
      <div><dt>10-year total savings</dt><dd data-out="decade">–</dd></div>
    </dl>
    <p class="tool__fine">Estimate based on your inputs. Most Austin Landscape Lighting LED retrofits also fix the voltage-drop dimming common in older halogen runs.</p>
    <a class="btn btn--primary" href="/services/led-upgrade-and-retrofit/">See LED retrofit options ' . icon('arrow') . '</a>
  </div>
</div>';
}

function tool_transformer_calculator(): string
{
    return '<div class="tool" data-tool="transformer">
  <form class="tool__form form-grid" onsubmit="return false">
    ' . field_number('uplights', 'Uplights (5 W each)', 8, 0, 100) . '
    ' . field_number('pathlights', 'Path lights (3 W each)', 6, 0, 100) . '
    ' . field_number('downlights', 'Tree downlights / moonlights (7 W each)', 2, 0, 50) . '
    ' . field_number('wall', 'Wall wash / hardscape lights (4 W each)', 2, 0, 100) . '
    ' . field_number('other', 'Other fixtures, total watts', 0, 0, 2000, 1) . '
    ' . field_number('run', 'Longest wire run (ft)', 90, 10, 400, 5) . '
    ' . field_select('gauge', 'Wire gauge', ['12' => '12 AWG (standard)', '10' => '10 AWG (long runs)', '14' => '14 AWG (short runs only)'], '12') . '
  </form>
  <div class="tool__result" aria-live="polite">
    <div class="tool__hero"><span class="tool__big" data-out="size">–</span><span class="tool__biglabel">recommended transformer</span></div>
    <div class="meter"><span class="meter__fill" data-out="meter"></span><span class="meter__label" data-out="load">–</span></div>
    <dl class="tool__kv">
      <div><dt>Connected load</dt><dd data-out="watts">–</dd></div>
      <div><dt>With 25% headroom</dt><dd data-out="headroom">–</dd></div>
      <div><dt>Voltage drop on longest run</dt><dd data-out="drop">–</dd></div>
      <div><dt>Suggested tap</dt><dd data-out="tap">–</dd></div>
    </dl>
    <p class="tool__note" data-out="note"></p>
    <p class="tool__fine">Rule of thumb only. We size every Austin Landscape Lighting transformer from the actual wire plan and meter the voltage at each fixture during the night aiming visit.</p>
  </div>
</div>';
}

function tool_color_temperature_guide(): string
{
    $pic = picture('landscape-lighting-austin-1', 'Austin stone home lit with warm landscape lighting', ['sizes' => '(max-width: 900px) 100vw, 60vw']);
    return '<div class="tool tool--kelvin" data-tool="kelvin">
  <div class="kelvin__scene">' . $pic . '<span class="kelvin__tint" data-out="tint"></span><span class="kelvin__badge"><b data-out="k">2700</b>K</span></div>
  <form class="tool__form" onsubmit="return false">
    <label class="field field--range"><span>Color temperature <output name="kelvin_out">2700</output> K</span><input class="kelvin__range" type="range" name="kelvin" min="2000" max="5000" step="50" value="2700"></label>
    <div class="kelvin__chips" role="group" aria-label="Presets">
      <button type="button" data-k="2200">2200K Candle</button><button type="button" data-k="2700">2700K Warm white</button><button type="button" data-k="3000">3000K Soft white</button><button type="button" data-k="4000">4000K Neutral</button><button type="button" data-k="5000">5000K Daylight</button>
    </div>
  </form>
  <div class="tool__result" aria-live="polite">
    <h4 data-out="title">Warm white</h4>
    <p data-out="desc"></p>
    <dl class="tool__kv">
      <div><dt>Best for</dt><dd data-out="bestfor">–</dd></div>
      <div><dt>Avoid on</dt><dd data-out="avoid">–</dd></div>
      <div><dt>Our verdict</dt><dd data-out="verdict">–</dd></div>
    </dl>
  </div>
</div>';
}

function tool_sunset_timer(): string
{
    return '<div class="tool tool--sunset" data-tool="sunset">
  <div class="sunset__today">
    <div class="sunset__arc" aria-hidden="true"><svg viewBox="0 0 300 160"><path d="M20 150 A130 130 0 0 1 280 150" fill="none" stroke="rgba(255,255,255,.12)" stroke-width="2" stroke-dasharray="4 6"/><circle class="sunset__sun" r="10" cx="150" cy="20" data-out="sun"/></svg></div>
    <p class="eyebrow" data-out="date">Today in Austin</p>
    <dl class="tool__kv tool__kv--big">
      <div><dt>Sunset</dt><dd data-out="sunset">–</dd></div>
      <div><dt>Civil dusk (lights on)</dt><dd data-out="dusk">–</dd></div>
      <div><dt>Sunrise</dt><dd data-out="sunrise">–</dd></div>
      <div><dt>Night length</dt><dd data-out="night">–</dd></div>
    </dl>
  </div>
  <form class="tool__form form-grid" onsubmit="return false">
    ' . field_select('off', 'Turn off', ['23:00' => '11:00 pm', '00:00' => 'Midnight', '01:00' => '1:00 am', 'dawn' => 'At dawn (photocell / astronomic)', '6h' => '6 hours after dusk'], '23:00') . '
    ' . field_select('offset', 'Switch on', ['0' => 'At sunset', '15' => '15 min after sunset', '30' => '30 min after sunset (civil dusk)', '-15' => '15 min before sunset'], '15') . '
  </form>
  <div class="tool__result" aria-live="polite">
    <p class="tool__note">Tonight your lights run <b data-out="on">–</b> to <b data-out="offtime">–</b>, about <b data-out="hours">–</b>.</p>
    <table class="tool__table"><thead><tr><th>Month</th><th>Sunset (1st)</th><th>Dusk</th><th>Sunrise</th><th>Hours on</th></tr></thead><tbody data-out="table"></tbody></table>
    <p class="tool__fine">Calculated for Austin, TX (30.27° N, 97.74° W) in Central Time with daylight saving applied. An astronomic timer or photocell from Austin Landscape Lighting tracks this automatically so you never reset a clock.</p>
  </div>
</div>';
}

function tool_lighting_visualizer(): string
{
    $toggles = [
        ['uplight', 'Architectural uplighting', 'Uplights graze the facade and columns', 6, '/services/architectural-uplighting/'],
        ['path', 'Path lights', 'Low, shielded path lights every 6 to 8 ft', 5, '/services/path-and-walkway-lighting/'],
        ['moon', 'Tree moonlighting', 'Downlights in the canopy cast soft shadows', 3, '/services/garden-and-tree-lighting/'],
        ['treeup', 'Tree uplighting', 'Narrow beams up the trunks into the canopy', 2, '/services/garden-and-tree-lighting/'],
        ['steps', 'Step lights', 'Recessed lights on risers and walls', 3, '/services/path-and-walkway-lighting/'],
        ['window', 'Interior warmth', 'Warm interior light balanced with the exterior', 0, '/tools/color-temperature-guide/'],
        ['porch', 'Entry sconces', 'Dimmed to 2700K so they do not glare', 2, '/services/security-and-safety-lighting/'],
        ['stars', 'Dark-sky friendly', 'Shielded fixtures keep the stars visible', 0, '/services/custom-lighting-design/'],
    ];
    $tg = '';
    foreach ($toggles as $i => [$key, $label, $hint, $count, $href]) {
        $checked = in_array($key, ['uplight', 'path', 'window', 'stars'], true) ? ' checked' : '';
        $tg .= '<label class="viz__toggle"><input type="checkbox" name="' . $key . '" data-count="' . $count . '"' . $checked . '><span class="viz__switch"></span><span class="viz__text"><b>' . e($label) . '</b><small>' . e($hint) . '</small></span><a class="viz__link" href="' . e($href) . '" aria-label="Learn about ' . e($label) . '">' . icon('arrow', 'ico ico--sm') . '</a></label>';
    }
    return '<div class="tool tool--viz" data-tool="viz">
  <div class="viz__scene" data-out="scene">' . visualizer_scene() . '</div>
  <div class="viz__panel">
    <div class="viz__toggles">' . $tg . '</div>
    <div class="viz__summary" aria-live="polite">
      <div><span class="tool__big" data-out="count">0</span><span class="tool__biglabel">fixtures in this scene</span></div>
      <div><span class="tool__big tool__big--sm" data-out="range">–</span><span class="tool__biglabel">planning range</span></div>
    </div>
    <a class="btn btn--primary" href="/contact/">Design this for my home ' . icon('arrow') . '</a>
  </div>
</div>';
}

/** SVG night scene used by the visualizer and the homepage hero. */
function visualizer_scene(string $id = 'viz'): string
{
    return <<<SVG
<svg class="scene" viewBox="0 0 1200 620" role="img" aria-label="Illustration of a home at night with landscape lighting">
  <defs>
    <linearGradient id="{$id}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05070f"/><stop offset=".65" stop-color="#0b1326"/><stop offset="1" stop-color="#15213a"/></linearGradient>
    <linearGradient id="{$id}-ground" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101a14"/><stop offset="1" stop-color="#070b09"/></linearGradient>
    <radialGradient id="{$id}-warm" cx=".5" cy="1" r=".9"><stop offset="0" stop-color="#ffcf7a" stop-opacity=".95"/><stop offset=".45" stop-color="#ffb347" stop-opacity=".35"/><stop offset="1" stop-color="#ffb347" stop-opacity="0"/></radialGradient>
    <radialGradient id="{$id}-pool" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#ffd9a0" stop-opacity=".9"/><stop offset="1" stop-color="#ffd9a0" stop-opacity="0"/></radialGradient>
    <radialGradient id="{$id}-moon" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#e8f1ff" stop-opacity=".55"/><stop offset="1" stop-color="#e8f1ff" stop-opacity="0"/></radialGradient>
    <linearGradient id="{$id}-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2e3a"/><stop offset="1" stop-color="#1b1f2a"/></linearGradient>
    <linearGradient id="{$id}-win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2ad"/><stop offset="1" stop-color="#f6b65a"/></linearGradient>
    <filter id="{$id}-blur"><feGaussianBlur stdDeviation="6"/></filter>
    <filter id="{$id}-blur2"><feGaussianBlur stdDeviation="14"/></filter>
  </defs>
  <rect width="1200" height="620" fill="url(#{$id}-sky)"/>
  <g class="scene__stars" data-layer="stars">
    <circle cx="90" cy="70" r="1.4"/><circle cx="210" cy="40" r="1"/><circle cx="330" cy="110" r="1.2"/><circle cx="450" cy="60" r=".9"/><circle cx="560" cy="130" r="1.3"/><circle cx="700" cy="50" r="1"/><circle cx="820" cy="95" r="1.5"/><circle cx="940" cy="40" r="1"/><circle cx="1050" cy="120" r="1.2"/><circle cx="1140" cy="70" r="1"/><circle cx="150" cy="160" r=".8"/><circle cx="640" cy="20" r="1.1"/><circle cx="1000" cy="180" r=".9"/><circle cx="380" cy="30" r=".8"/><circle cx="880" cy="160" r="1"/>
  </g>
  <circle cx="1040" cy="90" r="26" fill="#f4f1e8" opacity=".9"/><circle cx="1030" cy="84" r="22" fill="#0b1326" opacity=".85"/>
  <rect y="430" width="1200" height="190" fill="url(#{$id}-ground)"/>
  <g class="scene__hill" fill="#0d1520"><path d="M0 440 Q200 400 420 436 T900 428 T1200 440 V460 H0z"/></g>
  <g class="scene__tree-l" transform="translate(150 300)">
    <rect x="-9" y="60" width="18" height="90" fill="#1a1510"/>
    <ellipse cx="0" cy="30" rx="95" ry="70" fill="#0f1d16"/><ellipse cx="-40" cy="50" rx="60" ry="45" fill="#0c1811"/><ellipse cx="50" cy="55" rx="55" ry="40" fill="#101f17"/>
  </g>
  <g class="scene__tree-r" transform="translate(1040 290)">
    <rect x="-10" y="70" width="20" height="90" fill="#1a1510"/>
    <ellipse cx="0" cy="40" rx="105" ry="80" fill="#0f1d16"/><ellipse cx="-50" cy="60" rx="60" ry="45" fill="#0c1811"/><ellipse cx="55" cy="65" rx="60" ry="42" fill="#101f17"/>
  </g>
  <g class="scene__house">
    <polygon points="380,300 600,190 820,300" fill="#232838"/>
    <rect x="400" y="300" width="400" height="150" fill="url(#{$id}-wall)"/>
    <rect x="800" y="330" width="140" height="120" fill="#1a1e29"/>
    <rect x="260" y="330" width="140" height="120" fill="#1a1e29"/>
    <rect x="560" y="360" width="80" height="90" rx="3" fill="#1a1510"/>
    <rect x="430" y="330" width="60" height="60" rx="2" class="scene__win" fill="url(#{$id}-win)"/>
    <rect x="710" y="330" width="60" height="60" rx="2" class="scene__win" fill="url(#{$id}-win)"/>
    <rect x="850" y="350" width="40" height="40" rx="2" class="scene__win" fill="url(#{$id}-win)"/>
    <rect x="300" y="350" width="40" height="40" rx="2" class="scene__win" fill="url(#{$id}-win)"/>
    <rect x="520" y="300" width="14" height="150" fill="#2c3142"/><rect x="666" y="300" width="14" height="150" fill="#2c3142"/>
  </g>
  <g class="scene__path" fill="#171d22"><path d="M560 450 Q600 520 520 620 H720 Q680 520 640 450z"/></g>
  <g class="scene__steps" fill="#1e252c"><rect x="548" y="450" width="104" height="10"/><rect x="540" y="460" width="120" height="10"/><rect x="532" y="470" width="136" height="10"/></g>
  <g class="scene__beds" fill="#0f1a12"><ellipse cx="330" cy="470" rx="110" ry="22"/><ellipse cx="870" cy="470" rx="110" ry="22"/></g>

  <g class="lamp lamp--uplight" data-layer="uplight">
    <polygon points="415,450 470,300 490,300 445,450" fill="url(#{$id}-warm)"/><polygon points="500,450 545,300 565,300 535,450" fill="url(#{$id}-warm)"/><polygon points="640,450 665,300 685,300 675,450" fill="url(#{$id}-warm)"/><polygon points="750,450 770,300 790,300 785,450" fill="url(#{$id}-warm)"/><polygon points="280,450 320,330 340,330 310,450" fill="url(#{$id}-warm)"/><polygon points="880,450 900,330 920,330 915,450" fill="url(#{$id}-warm)"/>
    <g fill="#ffd9a0"><circle cx="430" cy="452" r="3"/><circle cx="518" cy="452" r="3"/><circle cx="658" cy="452" r="3"/><circle cx="768" cy="452" r="3"/><circle cx="295" cy="452" r="3"/><circle cx="898" cy="452" r="3"/></g>
    <rect x="400" y="300" width="400" height="150" fill="#f7c572" opacity=".10"/>
  </g>
  <g class="lamp lamp--path" data-layer="path">
    <g filter="url(#{$id}-blur)" fill="#ffc46b" opacity=".55"><ellipse cx="545" cy="520" rx="38" ry="12"/><ellipse cx="655" cy="520" rx="38" ry="12"/><ellipse cx="520" cy="575" rx="42" ry="13"/><ellipse cx="690" cy="575" rx="42" ry="13"/><ellipse cx="500" cy="612" rx="44" ry="10"/></g>
    <g fill="#f8d9a3"><rect x="543" y="498" width="4" height="22"/><rect x="653" y="498" width="4" height="22"/><rect x="518" y="553" width="4" height="22"/><rect x="688" y="553" width="4" height="22"/><rect x="498" y="592" width="4" height="20"/></g>
    <g fill="#ffe9c4"><ellipse cx="545" cy="497" rx="8" ry="3"/><ellipse cx="655" cy="497" rx="8" ry="3"/><ellipse cx="520" cy="552" rx="8" ry="3"/><ellipse cx="690" cy="552" rx="8" ry="3"/><ellipse cx="500" cy="591" rx="8" ry="3"/></g>
  </g>
  <g class="lamp lamp--moon" data-layer="moon">
    <polygon points="150,330 40,470 290,470" fill="url(#{$id}-moon)"/>
    <polygon points="1040,330 920,470 1180,470" fill="url(#{$id}-moon)"/>
    <g fill="#dde9ff" opacity=".35" filter="url(#{$id}-blur)"><ellipse cx="160" cy="468" rx="110" ry="16"/><ellipse cx="1045" cy="468" rx="120" ry="16"/></g>
  </g>
  <g class="lamp lamp--treeup" data-layer="treeup">
    <polygon points="140,450 110,330 190,330 160,450" fill="url(#{$id}-warm)"/><polygon points="1030,450 990,330 1090,330 1050,450" fill="url(#{$id}-warm)"/>
    <g fill="#ffd9a0"><circle cx="150" cy="452" r="3"/><circle cx="1040" cy="452" r="3"/></g>
    <ellipse cx="150" cy="330" rx="95" ry="70" fill="#f7c572" opacity=".12"/><ellipse cx="1040" cy="330" rx="105" ry="80" fill="#f7c572" opacity=".12"/>
  </g>
  <g class="lamp lamp--steps" data-layer="steps">
    <g fill="#ffc46b" opacity=".8" filter="url(#{$id}-blur)"><rect x="552" y="456" width="96" height="4"/><rect x="544" y="466" width="112" height="4"/><rect x="536" y="476" width="128" height="4"/></g>
  </g>
  <g class="lamp lamp--window" data-layer="window">
    <g filter="url(#{$id}-blur2)" fill="#ffd27a" opacity=".35"><rect x="430" y="330" width="60" height="60"/><rect x="710" y="330" width="60" height="60"/><rect x="850" y="350" width="40" height="40"/><rect x="300" y="350" width="40" height="40"/></g>
  </g>
  <g class="lamp lamp--porch" data-layer="porch">
    <g fill="#ffe2ad"><rect x="548" y="372" width="6" height="10" rx="1"/><rect x="646" y="372" width="6" height="10" rx="1"/></g>
    <g filter="url(#{$id}-blur)" fill="#ffcf7a" opacity=".55"><circle cx="551" cy="377" r="16"/><circle cx="649" cy="377" r="16"/></g>
  </g>
  <g class="fireflies" aria-hidden="true"><circle cx="240" cy="420" r="2"/><circle cx="960" cy="400" r="2"/><circle cx="700" cy="560" r="1.6"/><circle cx="420" cy="590" r="1.6"/><circle cx="1120" cy="520" r="1.8"/></g>
</svg>
SVG;
}

function tool_lighting_style_quiz(): string
{
    $q = [
        ['What does your home look like from the street?', ['modern' => 'Clean lines, stucco or steel, big glass', 'classic' => 'Brick or limestone, columns, symmetry', 'hill' => 'Native stone, metal roof, lots of trees', 'resort' => 'Pool, patio, outdoor kitchen is the star']],
        ['Which word should people think at night?', ['modern' => 'Striking', 'classic' => 'Elegant', 'hill' => 'Natural', 'resort' => 'Inviting']],
        ['How do you use the yard after dark?', ['resort' => 'Entertaining and swimming', 'hill' => 'Quiet evenings, stargazing', 'classic' => 'Mostly curb appeal coming home', 'modern' => 'Dinner on the patio, showing off the architecture']],
        ['Pick a color temperature', ['hill' => '2400K candlelight', 'classic' => '2700K warm white', 'resort' => '2700K with color-tunable accents', 'modern' => '3000K crisp white']],
        ['Your trees are...', ['hill' => 'Mature live oaks and cedar elms', 'classic' => 'A few specimen trees by the entry', 'modern' => 'Sculptural: agave, yucca, palms', 'resort' => 'Around the pool and patio']],
        ['How much drama?', ['modern' => 'High contrast, bold shadows', 'classic' => 'Balanced, even, timeless', 'hill' => 'Subtle, you barely notice the fixtures', 'resort' => 'Layered scenes I can change by mood']],
        ['Controls?', ['modern' => 'App, scenes, voice', 'resort' => 'App with zones for party vs quiet', 'classic' => 'Astronomic timer, set and forget', 'hill' => 'Photocell, minimal tech']],
        ['Budget mindset', ['classic' => 'Invest once in brass that lasts', 'modern' => 'Premium optics, fewer fixtures', 'resort' => 'Phase it: front now, pool later', 'hill' => 'Light only what matters']],
    ];
    $html = '<div class="tool tool--quiz" data-tool="quiz"><div class="quiz__progress"><span data-out="bar"></span></div><div class="quiz__steps">';
    foreach ($q as $i => [$question, $opts]) {
        $html .= '<fieldset class="quiz__step" data-step="' . $i . '"' . ($i ? ' hidden' : '') . '><legend><span class="eyebrow">Question ' . ($i + 1) . ' of ' . count($q) . '</span>' . e($question) . '</legend><div class="quiz__opts">';
        foreach ($opts as $style => $label) {
            $html .= '<label class="quiz__opt"><input type="radio" name="q' . $i . '" value="' . $style . '"><span>' . e($label) . '</span></label>';
        }
        $html .= '</div></fieldset>';
    }
    $html .= '</div><div class="quiz__result" data-out="result" hidden></div><div class="quiz__nav"><button type="button" class="btn btn--ghost" data-quiz="back" disabled>Back</button><button type="button" class="btn btn--primary" data-quiz="next" disabled>Next ' . icon('arrow') . '</button></div></div>';
    return $html;
}
