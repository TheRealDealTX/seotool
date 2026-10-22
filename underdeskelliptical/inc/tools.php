<?php
// Interactive tools. Each has a standalone page at /tools/<slug>/ and can be embedded
// in any post with [[tool:<id>]]. The markup lives here; behavior is in assets/js/site.js
// (keyed on data-tool), so every tool works the same wherever it is embedded.

const TOOLS = [
    'which-under-desk-elliptical-quiz' => [
        'id' => 'quiz', 'short' => 'Which Elliptical Is Right for Me?',
        'title' => 'Which Under Desk Elliptical Should I Buy? (60-Second Quiz)',
        'h1' => 'Which Under Desk Elliptical Is Right for You?',
        'description' => 'Answer five quick questions and get a personalized under desk elliptical recommendation for your desk, budget, noise needs and mobility.',
        'intro' => 'Five questions, no email required. We match your answers against every under desk elliptical, desk bike and walking pad we cover and show the three best fits.',
    ],
    'under-desk-elliptical-calorie-calculator' => [
        'id' => 'calories', 'short' => 'Calorie Calculator',
        'title' => 'Under Desk Elliptical Calorie Calculator: Calories Burned Per Hour',
        'h1' => 'Under Desk Elliptical Calories Burned Calculator',
        'description' => 'Estimate how many calories an under desk elliptical burns per session, week and month based on your weight, minutes and pedaling effort.',
        'intro' => 'Enter your weight, how long you pedal and how hard. The calculator uses MET values from the Compendium of Physical Activities to estimate calories burned, plus the extra calories compared with sitting still.',
    ],
    'under-desk-elliptical-steps-calculator' => [
        'id' => 'steps', 'short' => 'Steps Converter',
        'title' => 'Under Desk Elliptical to Steps Converter: Does It Count as Steps?',
        'h1' => 'Under Desk Elliptical Steps Converter',
        'description' => 'Convert minutes on an under desk elliptical into equivalent walking steps and see how close you get to your daily step goal.',
        'intro' => 'Wrist trackers often miss seated pedaling. This converter turns your elliptical minutes into an effort-matched step equivalent so you can log it fairly.',
    ],
    'desk-clearance-checker' => [
        'id' => 'clearance', 'short' => 'Desk Clearance Checker',
        'title' => 'Will an Under Desk Elliptical Fit Under My Desk? Clearance Checker',
        'h1' => 'Under Desk Elliptical Desk Clearance Checker',
        'description' => 'Check whether your knees will hit the desk before you buy. Enter your desk height and knee height to see which under desk elliptical fits.',
        'intro' => 'The number one return reason for under desk ellipticals is knees hitting the desk. Two measurements and ten seconds will tell you whether a machine will fit.',
    ],
    'desk-pedal-timer' => [
        'id' => 'timer', 'short' => 'Desk Pedal Timer',
        'title' => 'Desk Pedal Timer: Interval Timer for Under Desk Elliptical Workouts',
        'h1' => 'Under Desk Elliptical Interval Timer',
        'description' => 'A free interval timer for under desk elliptical sessions. Set pedal and rest blocks, get a gentle chime, and track minutes and calories as you work.',
        'intro' => 'Pedal in short blocks through your workday without watching the clock. Set your intervals, start the timer and get back to work. A soft chime tells you when to switch.',
    ],
    'compare-under-desk-ellipticals' => [
        'id' => 'finder', 'short' => 'Compare All Models',
        'title' => 'Compare Under Desk Ellipticals Side by Side (Filterable Table)',
        'h1' => 'Compare Under Desk Ellipticals',
        'description' => 'Filter and compare every under desk elliptical, motorized model, desk bike and walking pad we cover by type, noise, standing use and suitability for seniors.',
        'intro' => 'Every model we cover in one table. Filter by what matters to you, then click through to check today\'s price on Amazon.',
    ],
];

function tool_widget(string $id): string
{
    $fn = 'tool_' . $id;
    if (!function_exists($fn)) {
        throw new RuntimeException("Unknown tool: $id");
    }
    $slug = array_search($id, array_column(TOOLS, 'id', null));
    $page = array_keys(TOOLS)[$slug];
    $link = CURRENT_PATH === "/tools/$page/" ? '' : '<p class="tool-link"><a href="/tools/' . $page . '/">Open the full ' . e(TOOLS[$page]['short']) . ' &rarr;</a></p>';
    return '<div class="tool" data-tool="' . e($id) . '">' . $fn() . $link . '</div>';
}

function tool_calories(): string
{
    return <<<'HTML'
<h3 class="tool-title">Calorie Burn Calculator</h3>
<form class="tool-form" onsubmit="return false">
  <div class="field"><label>Your weight</label>
    <div class="inline"><input type="number" name="weight" value="170" min="70" max="500" inputmode="decimal" aria-label="Weight">
    <select name="unit" aria-label="Unit"><option value="lb">lb</option><option value="kg">kg</option></select></div></div>
  <div class="field"><label>Minutes per day: <output name="minOut">60</output></label>
    <input type="range" name="minutes" min="5" max="240" step="5" value="60"></div>
  <div class="field"><label>Effort</label>
    <div class="seg">
      <label><input type="radio" name="met" value="2.0"><span>Light<small>easy, while typing</small></span></label>
      <label><input type="radio" name="met" value="2.8" checked><span>Moderate<small>steady, can talk</small></span></label>
      <label><input type="radio" name="met" value="3.5"><span>Hard<small>breathing harder</small></span></label>
    </div></div>
  <div class="field"><label>Days per week: <output name="daysOut">5</output></label>
    <input type="range" name="days" min="1" max="7" value="5"></div>
</form>
<div class="tool-results" aria-live="polite">
  <div class="stat"><span class="stat-num" data-out="session">0</span><span class="stat-label">calories per session</span></div>
  <div class="stat"><span class="stat-num" data-out="extra">0</span><span class="stat-label">extra vs. sitting</span></div>
  <div class="stat"><span class="stat-num" data-out="week">0</span><span class="stat-label">extra per week</span></div>
  <div class="stat"><span class="stat-num" data-out="lbs">0</span><span class="stat-label">lb per month*</span></div>
</div>
<div class="bars" aria-hidden="true">
  <div class="bar"><span>Sitting</span><i data-bar="sit"></i><b data-barv="sit"></b></div>
  <div class="bar"><span>Under desk elliptical</span><i data-bar="ude" class="accent"></i><b data-barv="ude"></b></div>
  <div class="bar"><span>Walking 3 mph</span><i data-bar="walk"></i><b data-barv="walk"></b></div>
</div>
<p class="tool-note">*Extra calories only, at 3,500 calories per pound, if your diet stays the same. Estimates use MET values (sitting 1.3, walking 3.5) and will vary with your stride rate, resistance and body.</p>
HTML;
}

function tool_steps(): string
{
    return <<<'HTML'
<h3 class="tool-title">Elliptical-to-Steps Converter</h3>
<form class="tool-form" onsubmit="return false">
  <div class="field"><label>Minutes pedaled: <output name="minOut">45</output></label>
    <input type="range" name="minutes" min="5" max="240" step="5" value="45"></div>
  <div class="field"><label>Effort</label>
    <div class="seg">
      <label><input type="radio" name="met" value="2.0"><span>Light</span></label>
      <label><input type="radio" name="met" value="2.8" checked><span>Moderate</span></label>
      <label><input type="radio" name="met" value="3.5"><span>Hard</span></label>
    </div></div>
  <div class="field"><label>Daily step goal</label>
    <select name="goal"><option>5000</option><option>7500</option><option selected>10000</option><option>12000</option></select></div>
</form>
<div class="steps-out" aria-live="polite">
  <div class="ring"><svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="52" class="ring-bg"/><circle cx="60" cy="60" r="52" class="ring-fg" data-ring/></svg><div class="ring-label"><strong data-out="steps">0</strong><span>step equivalent</span></div></div>
  <p data-out="summary"></p>
</div>
<p class="tool-note">Effort-matched estimate: one minute of brisk walking (about 100 steps) is treated as the same work as a minute of pedaling at the same energy cost. Your tracker will count differently. Log sessions as a workout to get credit.</p>
HTML;
}

function tool_clearance(): string
{
    return <<<'HTML'
<h3 class="tool-title">Desk Clearance Checker</h3>
<form class="tool-form" onsubmit="return false">
  <div class="field"><label>Floor to underside of desk (inches)</label>
    <input type="number" name="desk" value="27" min="15" max="50" step="0.5" inputmode="decimal">
    <small>Measure to the lowest point: keyboard tray, drawer or frame bar.</small></div>
  <div class="field"><label>Floor to top of your knee, seated (inches)</label>
    <input type="number" name="knee" value="21" min="12" max="35" step="0.5" inputmode="decimal">
    <small>Sit in your normal chair with feet flat and measure to the top of your thigh at the knee.</small></div>
  <div class="field"><label>Type of machine</label>
    <select name="pedal">
      <option value="8.5">Low-profile / mini (about 8–9 in pedal height)</option>
      <option value="10" selected>Standard seated elliptical (about 10 in)</option>
      <option value="12">Tall or motorized model (about 12 in)</option>
      <option value="13">Under desk bike (about 13 in)</option>
    </select></div>
</form>
<div class="clear-out" aria-live="polite">
  <div class="meter"><div class="meter-fill" data-meter></div></div>
  <p class="verdict" data-out="verdict"></p>
  <p data-out="advice"></p>
</div>
<p class="tool-note">Pedal heights are typical ranges. Check the "height" spec in the Amazon listing of the model you choose and re-run the check with that number.</p>
HTML;
}

function tool_timer(): string
{
    return <<<'HTML'
<h3 class="tool-title">Pedal Interval Timer</h3>
<form class="tool-form" onsubmit="return false">
  <div class="field-row">
    <div class="field"><label>Pedal (min)</label><input type="number" name="work" value="10" min="1" max="120"></div>
    <div class="field"><label>Rest (min)</label><input type="number" name="rest" value="20" min="0" max="120"></div>
    <div class="field"><label>Rounds</label><input type="number" name="rounds" value="6" min="1" max="24"></div>
  </div>
</form>
<div class="timer" aria-live="polite">
  <p class="timer-phase" data-out="phase">Ready</p>
  <p class="timer-clock" data-out="clock">10:00</p>
  <p class="timer-sub">Round <span data-out="round">1</span> of <span data-out="rounds">6</span> &middot; <span data-out="total">0</span> min pedaled today</p>
  <div class="timer-btns"><button type="button" class="btn" data-act="start">Start</button><button type="button" class="btn btn-ghost" data-act="reset">Reset</button></div>
</div>
<p class="tool-note">Keep this tab open. Your total minutes are saved in this browser for today only.</p>
HTML;
}

function tool_quiz(): string
{
    $data = [];
    foreach (PRODUCTS as $k => $p) {
        if (in_array($p['type'], ['accessory', 'tracker'])) {
            continue;
        }
        $data[$k] = ['n' => $p['name'], 't' => $p['type'], 'b' => $p['best_for'], 'q' => $p['noise'], 's' => $p['seniors'], 'st' => $p['standing'],
            'u' => amz_url($k), 'r' => $p['review'], 'i' => thumb($p['image'])];
    }
    $json = json_encode($data, JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_APOS);
    return <<<HTML
<h3 class="tool-title">Find Your Under Desk Elliptical</h3>
<form class="quiz" onsubmit="return false">
  <fieldset><legend>1. How will you use it?</legend>
    <label><input type="radio" name="use" value="seated" checked> Sitting at my desk or in a chair</label>
    <label><input type="radio" name="use" value="standing"> Standing (I have a standing desk)</label>
    <label><input type="radio" name="use" value="both"> Both</label></fieldset>
  <fieldset><legend>2. What's your main goal?</legend>
    <label><input type="radio" name="goal" value="move" checked> Move more and feel less stiff</label>
    <label><input type="radio" name="goal" value="burn"> Burn calories / lose weight</label>
    <label><input type="radio" name="goal" value="circ"> Circulation, rehab or limited mobility</label></fieldset>
  <fieldset><legend>3. How important is silence?</legend>
    <label><input type="radio" name="noise" value="high" checked> Very: I'm on calls or share a room</label>
    <label><input type="radio" name="noise" value="low"> Some hum is fine</label></fieldset>
  <fieldset><legend>4. Budget</legend>
    <label><input type="radio" name="budget" value="low"> As low as possible</label>
    <label><input type="radio" name="budget" value="mid" checked> Mid-range for better build</label>
    <label><input type="radio" name="budget" value="high"> Premium is fine</label></fieldset>
  <fieldset><legend>5. Who is it for?</legend>
    <label><input type="radio" name="who" value="me" checked> Me, an office or remote worker</label>
    <label><input type="radio" name="who" value="senior"> A senior or someone easing back into exercise</label></fieldset>
  <button type="button" class="btn" data-act="quiz">Show my matches</button>
</form>
<div class="quiz-results" aria-live="polite"></div>
<script type="application/json" class="quiz-data">{$json}</script>
<p class="tool-note">As an Amazon Associate we earn from qualifying purchases. That never changes which product the quiz picks.</p>
HTML;
}

function tool_finder(): string
{
    $rows = '';
    foreach (PRODUCTS as $k => $p) {
        if (in_array($p['type'], ['accessory', 'tracker'])) {
            continue;
        }
        $quiet = in_array($p['noise'], ['Whisper quiet', 'Very quiet', 'Quiet']) ? 1 : 0;
        $rows .= '<tr data-type="' . e($p['type']) . '" data-quiet="' . $quiet . '" data-seniors="' . (int) $p['seniors'] . '" data-standing="' . (int) $p['standing'] . '">'
            . '<td><strong>' . e($p['name']) . '</strong>' . ($p['review'] ? '<br><a class="small" href="' . e($p['review']) . '">Our guide</a>' : '') . '</td>'
            . '<td>' . e(PRODUCT_TYPES[$p['type']]) . '</td><td>' . e($p['best_for']) . '</td><td>' . e($p['noise'] ?? '—') . '</td>'
            . '<td>' . ($p['seniors'] ? '✔' : '—') . '</td><td>' . ($p['standing'] ? '✔' : '✘') . '</td>'
            . '<td>' . amz_button($k, 'Check Price', 'btn-sm') . '</td></tr>';
    }
    return <<<HTML
<h3 class="tool-title">Under Desk Elliptical Comparison Table</h3>
<div class="chips" role="group" aria-label="Filters">
  <button type="button" class="chip on" data-f="all">All</button>
  <button type="button" class="chip" data-f="manual">Manual</button>
  <button type="button" class="chip" data-f="motorized">Motorized</button>
  <button type="button" class="chip" data-f="quiet">Quiet</button>
  <button type="button" class="chip" data-f="seniors">Seniors</button>
  <button type="button" class="chip" data-f="standing">Standing use</button>
  <button type="button" class="chip" data-f="desk-bike">Desk bikes</button>
  <button type="button" class="chip" data-f="walking-pad">Walking pads</button>
</div>
<div class="table-wrap"><table class="compare finder"><thead><tr><th>Model</th><th>Type</th><th>Best for</th><th>Noise</th><th>Seniors</th><th>Standing</th><th></th></tr></thead><tbody>{$rows}</tbody></table></div>
<p class="tool-note"><span data-out="count"></span></p>
HTML;
}
