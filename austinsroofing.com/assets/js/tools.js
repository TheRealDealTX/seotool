/* Austin Roofing — interactive tools. Each <div class="tool" data-tool="key">
   is replaced with a working widget. All maths runs in the browser; nothing
   is sent anywhere. Figures are planning ranges, labelled as such. */
(function () {
  'use strict';

  var PHONE = '(956) 465-6045';
  var TEL = 'tel:+19564656045';

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function round1(n) { return Math.round(n * 10) / 10; }
  function track(name, extra) { if (window.gtag) window.gtag('event', 'tool_use', Object.assign({ tool_name: name }, extra || {})); }
  function ctaHtml(text) {
    return '<div class="tool__cta"><a class="btn btn--red" href="/contact-us/">' + (text || 'Get an exact free quote') + '</a>' +
      '<a class="btn btn--ghost" href="' + TEL + '">Call ' + PHONE + '</a></div>';
  }
  function head(el, fallback, icon) {
    var t = el.getAttribute('data-heading') || fallback;
    return '<div class="tool__head"><h3>' + t + '</h3></div>';
  }
  /* Segmented button group helper: returns html; value read via data-value on pressed button */
  function seg(name, options, current) {
    return '<div class="seg" role="group" data-seg="' + name + '">' + options.map(function (o) {
      return '<button type="button" data-value="' + o[0] + '" aria-pressed="' + (String(o[0]) === String(current)) + '">' + o[1] + '</button>';
    }).join('') + '</div>';
  }
  function bindSegs(root, onChange) {
    $$('.seg', root).forEach(function (g) {
      g.addEventListener('click', function (ev) {
        var b = ev.target.closest('button');
        if (!b) return;
        $$('button', g).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        onChange();
      });
    });
  }
  function segVal(root, name) {
    var b = $('[data-seg="' + name + '"] [aria-pressed="true"]', root);
    return b ? b.getAttribute('data-value') : null;
  }

  var PITCH = { 2: 1.014, 3: 1.031, 4: 1.054, 5: 1.083, 6: 1.118, 7: 1.158, 8: 1.202, 9: 1.25, 10: 1.302, 11: 1.357, 12: 1.414 };

  /* 1. Roof replacement cost calculator ------------------------------------ */
  var MATERIALS = {
    threetab: { name: '3-tab asphalt shingles', lo: 380, hi: 500, life: '15–20 yrs' },
    arch: { name: 'Architectural shingles', lo: 450, hi: 650, life: '20–25 yrs' },
    class4: { name: 'Class 4 impact-resistant shingles', lo: 575, hi: 800, life: '25–30 yrs' },
    stone: { name: 'Stone-coated steel', lo: 900, hi: 1400, life: '40–50 yrs' },
    metal: { name: 'Standing seam metal', lo: 1000, hi: 1600, life: '40–60 yrs' }
  };
  function costTool(el) {
    el.innerHTML = head(el, 'Austin Roof Replacement Cost Calculator') +
      '<div class="tool__grid"><div class="tool__fields">' +
      '<label>Home size (living area) <span class="range-val" data-out="sqft">2,000 sq ft</span><input type="range" name="sqft" min="800" max="6000" step="50" value="2000"></label>' +
      '<div class="field-label">Stories ' + seg('stories', [[1, '1 story'], [2, '2 stories']], 1) + '</div>' +
      '<div class="field-label">Roof pitch ' + seg('pitch', [[4, 'Low (4/12)'], [6, 'Medium (6/12)'], [9, 'Steep (9/12)'], [12, 'Very steep (12/12)']], 6) + '</div>' +
      '<div class="field-label">Roof shape ' + seg('shape', [['1.0', 'Simple gable'], ['1.08', 'Hip roof'], ['1.16', 'Complex (valleys, dormers)']], '1.08') + '</div>' +
      '<label>Roofing material<select name="material">' + Object.keys(MATERIALS).map(function (k) {
        return '<option value="' + k + '"' + (k === 'arch' ? ' selected' : '') + '>' + MATERIALS[k].name + '</option>';
      }).join('') + '</select></label>' +
      '<div class="field-label">Layers to tear off ' + seg('layers', [[1, '1 layer'], [2, '2 layers']], 1) + '</div>' +
      '</div><div class="tool__result" aria-live="polite">' +
      '<h4>Estimated installed cost</h4><div class="big-num" data-out="range">—</div>' +
      '<ul class="result-rows"><li><span>Roof area</span><span data-out="area"></span></li><li><span>Roofing squares (incl. waste)</span><span data-out="squares"></span></li>' +
      '<li><span>Installed price per square</span><span data-out="psq"></span></li><li><span>Typical lifespan in Texas</span><span data-out="life"></span></li></ul>' +
      '<p class="tool__note">Planning range for the Austin area in 2026, based on typical installed prices. Decking repairs, permits, gutters and insurance-related work are not included. Your free inspection gives you an exact written price.</p>' +
      ctaHtml() + '</div></div>';
    var used = false;
    function calc() {
      var sqft = +$('[name=sqft]', el).value;
      var stories = +segVal(el, 'stories');
      var pitch = +segVal(el, 'pitch');
      var shape = +segVal(el, 'shape');
      var layers = +segVal(el, 'layers');
      var m = MATERIALS[$('[name=material]', el).value];
      var footprint = sqft / stories * 1.15; // eaves overhang + garage allowance
      var area = footprint * PITCH[pitch] * shape;
      var squares = area / 100 * 1.12;
      var steep = pitch >= 12 ? 1.25 : pitch >= 9 ? 1.12 : 1;
      var story = stories === 2 ? 1.05 : 1;
      var tear = layers === 2 ? [60, 90] : [0, 0];
      var lo = squares * (m.lo * steep * story + tear[0]);
      var hi = squares * (m.hi * steep * story + tear[1]);
      $('[data-out=sqft]', el).textContent = sqft.toLocaleString('en-US') + ' sq ft';
      $('[data-out=range]', el).innerHTML = '<span style="white-space:nowrap">' + money(lo) + '</span> – <span style="white-space:nowrap">' + money(hi) + '</span><small>' + m.name + '</small>';
      $('[data-out=area]', el).textContent = Math.round(area).toLocaleString('en-US') + ' sq ft';
      $('[data-out=squares]', el).textContent = round1(squares) + ' squares';
      $('[data-out=psq]', el).textContent = money(lo / squares) + ' – ' + money(hi / squares);
      $('[data-out=life]', el).textContent = m.life;
      if (used) track('cost'); used = true;
    }
    el.addEventListener('input', calc);
    el.addEventListener('change', calc);
    bindSegs(el, calc);
    calc();
  }

  /* 2. Roofing squares & bundles ------------------------------------------- */
  function squaresTool(el) {
    var pitchOpts = Object.keys(PITCH).map(function (p) { return '<option value="' + p + '"' + (p === '6' ? ' selected' : '') + '>' + p + '/12</option>'; }).join('');
    el.innerHTML = head(el, 'Roofing Square & Shingle Bundle Calculator') +
      '<div class="tool__grid"><div class="tool__fields">' +
      '<div class="field-label">Measure by ' + seg('mode', [['dims', 'Length × width'], ['area', 'Footprint sq ft']], 'dims') + '</div>' +
      '<div class="row2" data-show="dims"><label>House length (ft)<input type="number" name="len" min="10" max="300" value="60" inputmode="decimal"></label>' +
      '<label>House width (ft)<input type="number" name="wid" min="10" max="300" value="35" inputmode="decimal"></label></div>' +
      '<label data-show="area" hidden>Ground footprint incl. garage (sq ft)<input type="number" name="fp" min="200" max="20000" value="2100" inputmode="decimal"></label>' +
      '<div class="row2"><label>Roof pitch<select name="pitch">' + pitchOpts + '</select></label>' +
      '<label>Eave overhang (in)<input type="number" name="oh" min="0" max="36" value="12" inputmode="decimal"></label></div>' +
      '<div class="field-label">Roof style (waste factor) ' + seg('waste', [['10', 'Gable · 10%'], ['15', 'Hip · 15%'], ['18', 'Complex · 18%']], '10') + '</div>' +
      '<label>Underlayment type<select name="ul"><option value="10">Synthetic (≈10 squares/roll)</option><option value="4">#15 felt (≈4 squares/roll)</option><option value="2">#30 felt (≈2 squares/roll)</option></select></label>' +
      '</div><div class="tool__result" aria-live="polite"><h4>Your roof measures about</h4><div class="big-num" data-out="sq">—</div>' +
      '<ul class="result-rows"><li><span>Roof surface area</span><span data-out="area"></span></li><li><span>Shingle bundles (3 per square)</span><span data-out="bundles"></span></li>' +
      '<li><span>Underlayment rolls</span><span data-out="ul"></span></li><li><span>Starter strip (linear ft)</span><span data-out="starter"></span></li>' +
      '<li><span>Ridge cap (linear ft)</span><span data-out="ridge"></span></li><li><span>Drip edge (10 ft pieces)</span><span data-out="drip"></span></li>' +
      '<li><span>Coil nails (approx.)</span><span data-out="nails"></span></li></ul>' +
      '<p class="tool__note">Estimates for a rectangular house. Valleys, dormers and multiple roof planes change the numbers — a roofer measures every plane before ordering.</p>' +
      ctaHtml('Get a professional measurement') + '</div></div>';
    var used = false;
    function calc() {
      var mode = segVal(el, 'mode');
      $$('[data-show]', el).forEach(function (n) { n.hidden = n.getAttribute('data-show') !== mode; });
      var oh = (+$('[name=oh]', el).value || 0) / 12;
      var L, W;
      if (mode === 'dims') { L = +$('[name=len]', el).value || 0; W = +$('[name=wid]', el).value || 0; }
      else { var fp = +$('[name=fp]', el).value || 0; W = Math.sqrt(fp / 1.6); L = W * 1.6; }
      L += oh * 2; W += oh * 2;
      var pitch = $('[name=pitch]', el).value;
      var area = L * W * PITCH[pitch];
      var waste = +segVal(el, 'waste') / 100;
      var squares = area / 100 * (1 + waste);
      var sqUp = Math.ceil(squares * 3) / 3;
      var perim = 2 * (L + W);
      $('[data-out=sq]', el).innerHTML = round1(squares) + ' squares<small>' + Math.round(area).toLocaleString('en-US') + ' sq ft of roof + ' + Math.round(waste * 100) + '% waste</small>';
      $('[data-out=area]', el).textContent = Math.round(area).toLocaleString('en-US') + ' sq ft';
      $('[data-out=bundles]', el).textContent = Math.ceil(sqUp * 3) + ' bundles';
      $('[data-out=ul]', el).textContent = Math.ceil(squares / +$('[name=ul]', el).value) + ' rolls';
      $('[data-out=starter]', el).textContent = Math.ceil(perim) + ' ft';
      $('[data-out=ridge]', el).textContent = Math.ceil(segVal(el, 'waste') === '10' ? L : L + W * 1.4) + ' ft';
      $('[data-out=drip]', el).textContent = Math.ceil(perim / 10) + ' pieces';
      $('[data-out=nails]', el).textContent = Math.ceil(squares * 320).toLocaleString('en-US');
      if (used) track('squares'); used = true;
    }
    el.addEventListener('input', calc);
    el.addEventListener('change', calc);
    bindSegs(el, calc);
    calc();
  }

  /* 3. Roof pitch calculator with live diagram ----------------------------- */
  function pitchTool(el) {
    el.innerHTML = head(el, 'Roof Pitch Calculator') +
      '<div class="tool__grid"><div class="tool__fields">' +
      '<div class="field-label">I know the… ' + seg('mode', [['ratio', 'Rise per 12 in of run'], ['measure', 'Rise and run'], ['angle', 'Angle']], 'ratio') + '</div>' +
      '<label data-show="ratio">Rise (inches per 12 in) <span class="range-val" data-out="riseLbl">6</span><input type="range" name="rise" min="0" max="24" step="0.5" value="6"></label>' +
      '<div class="row2" data-show="measure" hidden><label>Rise (in)<input type="number" name="mr" value="30" min="0" inputmode="decimal"></label><label>Run (in)<input type="number" name="mrun" value="60" min="1" inputmode="decimal"></label></div>' +
      '<label data-show="angle" hidden>Angle (degrees)<input type="number" name="deg" value="26.6" min="0" max="75" step="0.1" inputmode="decimal"></label>' +
      '<svg class="pitch-svg" viewBox="0 0 400 230" role="img" aria-label="Roof pitch diagram">' +
      '<defs><pattern id="shg" width="20" height="10" patternUnits="userSpaceOnUse"><rect width="20" height="10" fill="#6b5f57"/><path d="M0 9.5h20M10 0v10" stroke="#4d433d" stroke-width="1"/></pattern></defs>' +
      '<rect x="60" y="150" width="280" height="70" fill="#F3F2EC" stroke="#363636" stroke-width="2"/>' +
      '<rect x="180" y="175" width="40" height="45" fill="#1E93AB"/>' +
      '<polygon data-roof points="40,150 200,70 360,150" fill="url(#shg)" stroke="#E62727" stroke-width="4" stroke-linejoin="round"/>' +
      '<line data-rise x1="200" y1="150" x2="200" y2="70" stroke="#E62727" stroke-dasharray="5 4" stroke-width="2"/>' +
      '<line x1="40" y1="150" x2="200" y2="150" stroke="#1E93AB" stroke-dasharray="5 4" stroke-width="2"/>' +
      '<text data-label x="208" y="115" font-size="15" font-weight="700" fill="#E62727">6/12</text>' +
      '<text x="100" y="168" font-size="12" fill="#1E93AB" font-weight="700">run</text></svg>' +
      '</div><div class="tool__result" aria-live="polite"><h4>Roof pitch</h4><div class="big-num" data-out="pitch">—</div>' +
      '<ul class="result-rows"><li><span>Angle</span><span data-out="deg"></span></li><li><span>Slope (grade)</span><span data-out="grade"></span></li>' +
      '<li><span>Area multiplier</span><span data-out="mult"></span></li><li><span>Category</span><span data-out="cat"></span></li><li><span>Suitable roofing</span><span data-out="mat"></span></li></ul>' +
      '<p class="tool__note">Multiply your home’s footprint (with overhangs) by the area multiplier to get actual roof surface area.</p>' + ctaHtml('Have us measure your roof') + '</div></div>';
    var used = false;
    function calc() {
      var mode = segVal(el, 'mode');
      $$('[data-show]', el).forEach(function (n) { n.hidden = n.getAttribute('data-show') !== mode; });
      var rise;
      if (mode === 'ratio') rise = +$('[name=rise]', el).value;
      else if (mode === 'measure') rise = (+$('[name=mr]', el).value || 0) / Math.max(+$('[name=mrun]', el).value || 1, 1) * 12;
      else rise = Math.tan(Math.min(+$('[name=deg]', el).value || 0, 75) * Math.PI / 180) * 12;
      var deg = Math.atan(rise / 12) * 180 / Math.PI;
      var mult = Math.sqrt(1 + Math.pow(rise / 12, 2));
      var r = round1(rise);
      var cat, mat;
      if (rise < 2) { cat = 'Flat / low slope'; mat = 'TPO, EPDM, modified bitumen, coatings'; }
      else if (rise < 4) { cat = 'Low slope'; mat = 'Shingles with full self-adhered underlayment, metal'; }
      else if (rise < 7) { cat = 'Conventional (walkable)'; mat = 'Any shingle, metal, stone-coated steel'; }
      else if (rise < 10) { cat = 'Steep'; mat = 'Shingles, metal, tile — steep-roof safety needed'; }
      else { cat = 'Very steep'; mat = 'Shingles, metal, slate — specialty install'; }
      $('[data-out=riseLbl]', el).textContent = r;
      $('[data-out=pitch]', el).innerHTML = r + '/12<small>' + r + ' in of rise per 12 in of run</small>';
      $('[data-out=deg]', el).textContent = round1(deg) + '°';
      $('[data-out=grade]', el).textContent = Math.round(rise / 12 * 100) + '%';
      $('[data-out=mult]', el).textContent = '× ' + mult.toFixed(3);
      $('[data-out=cat]', el).textContent = cat;
      $('[data-out=mat]', el).textContent = mat;
      var peak = 150 - Math.min(rise / 12 * 160, 140);
      $('[data-roof]', el).setAttribute('points', '40,150 200,' + peak + ' 360,150');
      $('[data-rise]', el).setAttribute('y2', peak);
      var lbl = $('[data-label]', el);
      lbl.textContent = r + '/12';
      lbl.setAttribute('y', Math.max((150 + peak) / 2, 20));
      if (used) track('pitch'); used = true;
    }
    el.addEventListener('input', calc);
    bindSegs(el, calc);
    calc();
  }

  /* 4. Repair or replace quiz --------------------------------------------- */
  var QUIZ = [
    ['How old is your roof?', [['Under 10 years', 0], ['10–15 years', 1], ['15–20 years', 2], ['20+ years or not sure', 3]]],
    ['Is water getting inside?', [['No leaks', 0], ['One small leak or stain', 1], ['Leaks in more than one spot', 3]]],
    ['What do the shingles look like?', [['Flat and intact', 0], ['A few missing or lifted', 1], ['Curling, cracking or bald patches', 3]]],
    ['How much granule grit is in your gutters?', [['Barely any', 0], ['Some after storms', 1], ['A lot — gutters look sandy', 2]]],
    ['Has a hail or wind storm hit since the roof went on?', [['No', 0], ['Small hail / moderate wind', 1], ['Large hail (quarter-size+) or major wind', 3]]],
    ['From the ground, is the roof line straight?', [['Yes, straight', 0], ['Not sure', 1], ['It sags or dips', 4]]],
    ['How is the attic?', [['Dry, no daylight', 0], ['Hot but dry', 1], ['Damp, stained or I can see daylight', 3]]]
  ];
  function quizTool(el) {
    var answers = [];
    function render() {
      var i = answers.length;
      if (i >= QUIZ.length) return result();
      var q = QUIZ[i];
      el.innerHTML = head(el, 'Repair or Replace? Roof Quiz') +
        '<div class="quiz__bar"><span style="width:' + (i / QUIZ.length * 100) + '%"></span></div>' +
        '<p class="quiz__step">Question ' + (i + 1) + ' of ' + QUIZ.length + '</p><p class="quiz__q">' + q[0] + '</p>' +
        '<div class="quiz__opts">' + q[1].map(function (o, k) { return '<button type="button" data-k="' + k + '">' + o[0] + '</button>'; }).join('') + '</div>' +
        (i ? '<p style="margin-top:14px"><button type="button" class="btn btn--outline" data-back>← Back</button></p>' : '');
    }
    function result() {
      var score = answers.reduce(function (a, b) { return a + b; }, 0);
      var max = QUIZ.reduce(function (a, q) { return a + q[1][q[1].length - 1][1]; }, 0);
      var pct = score / max;
      var verdict, text, sev;
      if (answers[5] === 4) { sev = 3; verdict = 'Get it inspected right away'; text = 'A sagging roof line can mean water-damaged decking or structural problems. Please have a roofer look before the next heavy rain.'; }
      else if (pct < 0.25) { sev = 0; verdict = 'Likely a repair — or nothing at all'; text = 'Your answers point to a roof with plenty of life left. Small issues like a lifted shingle or cracked pipe boot can usually be fixed in one visit.'; }
      else if (pct < 0.5) { sev = 1; verdict = 'A repair probably makes sense'; text = 'There are some warning signs, but a targeted repair is often enough. An inspection will confirm whether the damage is local or roof-wide.'; }
      else if (pct < 0.72) { sev = 2; verdict = 'Borderline — get a professional opinion'; text = 'Your roof is showing age or storm damage in several ways. Compare a repair quote with a replacement quote — and if hail was involved, check whether insurance may cover it.'; }
      else { sev = 3; verdict = 'Replacement is likely the better value'; text = 'Multiple signs point to a roof near the end of its life. Repairs may only buy a season or two. A free inspection will tell you for sure.'; }
      el.innerHTML = head(el, 'Repair or Replace? Roof Quiz') + '<div class="quiz__bar"><span style="width:100%"></span></div>' +
        '<div class="tool__result" aria-live="polite"><h4>Your result</h4><p><span class="sev sev--' + sev + '">Score ' + score + ' / ' + max + '</span></p>' +
        '<div class="big-num" style="font-size:1.9rem">' + verdict + '</div><p style="margin-top:12px;color:#d9eaee">' + text + '</p>' +
        ctaHtml('Book a free inspection') + '<p style="margin-top:14px"><button type="button" class="btn btn--ghost" data-restart>Retake quiz</button></p></div>';
      track('quiz', { score: score });
    }
    el.addEventListener('click', function (ev) {
      var b = ev.target.closest('button');
      if (!b) return;
      if (b.hasAttribute('data-k')) { var q = QUIZ[answers.length]; answers.push(q[1][+b.getAttribute('data-k')][1]); render(); }
      else if (b.hasAttribute('data-back')) { answers.pop(); render(); }
      else if (b.hasAttribute('data-restart')) { answers = []; render(); }
    });
    render();
  }

  /* 5. Hail size & damage checker ------------------------------------------ */
  var HAIL = [
    ['pea', 'Pea', 0.25], ['marble', 'Marble', 0.5], ['penny', 'Penny', 0.75], ['quarter', 'Quarter', 1],
    ['ping', 'Ping-pong', 1.5], ['golf', 'Golf ball', 1.75], ['tennis', 'Tennis ball', 2.5], ['base', 'Baseball', 2.75], ['soft', 'Softball', 4]
  ];
  var ROOFS = {
    threetab: ['3-tab shingles', 1.0], arch: ['Architectural shingles', 1.25], class4: ['Class 4 impact-resistant shingles', 2.0],
    metal: ['Metal roof', 1.75], tile: ['Clay / concrete tile', 1.5], flat: ['Flat roof (TPO / mod-bit)', 1.5]
  };
  var SEV = [
    ['Damage unlikely', 'Hail this size rarely damages this roof type. Look for dented gutters or AC fins as a gauge — if those are fine, the roof usually is too.'],
    ['Damage possible', 'Older or brittle roofing can bruise at this size. Check for granules in gutters and dents on metal vents. An inspection is a good idea if the roof is 10+ years old.'],
    ['Damage likely', 'Hail this size commonly bruises shingles, knocks off granules and cracks tile or seams. Get an inspection and photograph the hail and any dents before they melt or are cleaned up.'],
    ['Severe damage expected', 'Expect punctures, cracked or broken roofing and functional damage. Check the attic for leaks, call for emergency tarping if needed, and contact your insurer soon.']
  ];
  function hailTool(el) {
    el.innerHTML = head(el, 'Hail Size & Roof Damage Checker') +
      '<div class="tool__grid"><div class="tool__fields"><div class="field-label">What size was the hail?</div>' +
      '<div class="hail-scale" data-hail>' + HAIL.map(function (h, i) {
        var px = Math.round(8 + h[2] * 11);
        return '<button type="button" data-i="' + i + '" aria-pressed="' + (i === 3) + '"><span class="hail-ball" style="width:' + px + 'px;height:' + px + 'px"></span>' + h[1] + '<br>' + h[2] + '″</button>';
      }).join('') + '</div>' +
      '<label>Your roof type<select name="roof">' + Object.keys(ROOFS).map(function (k) { return '<option value="' + k + '"' + (k === 'arch' ? ' selected' : '') + '>' + ROOFS[k][0] + '</option>'; }).join('') + '</select></label>' +
      '<div class="field-label">Roof age ' + seg('age', [['0', 'Under 5 yrs'], ['1', '5–15 yrs'], ['2', '15+ yrs']], '1') + '</div>' +
      '</div><div class="tool__result" aria-live="polite"><h4>Likely result</h4><div data-out="ball" style="height:110px;display:flex;align-items:flex-end;justify-content:center;margin-bottom:8px"></div>' +
      '<p><span class="sev" data-out="sev"></span></p><p data-out="text" style="color:#d9eaee"></p>' +
      '<ul class="result-rows"><li><span>Hail diameter</span><span data-out="size"></span></li><li><span>Damage threshold for this roof</span><span data-out="thr"></span></li></ul>' +
      '<p class="tool__note">General guidance from typical hail-impact thresholds. Wind-driven hail, roof age and material condition all change real-world results.</p>' +
      ctaHtml('Schedule a free hail inspection') + '</div></div>';
    var used = false;
    function calc() {
      var i = +$('[data-hail] [aria-pressed="true"]', el).getAttribute('data-i');
      var h = HAIL[i];
      var roof = ROOFS[$('[name=roof]', el).value];
      var age = +segVal(el, 'age');
      var thr = roof[1] * (age === 2 ? 0.8 : age === 1 ? 0.92 : 1);
      var r = h[2] / thr;
      var s = r < 0.75 ? 0 : r < 1 ? 1 : r < 1.6 ? 2 : 3;
      var px = Math.round(16 + h[2] * 22);
      $('[data-out=ball]', el).innerHTML = '<span class="hail-ball hail-drop" style="width:' + px + 'px;height:' + px + 'px"></span>';
      var sv = $('[data-out=sev]', el);
      sv.className = 'sev sev--' + s; sv.textContent = SEV[s][0];
      $('[data-out=text]', el).textContent = SEV[s][1];
      $('[data-out=size]', el).textContent = h[2] + ' in (' + h[1].toLowerCase() + ')';
      $('[data-out=thr]', el).textContent = '≈ ' + round1(thr * 100) / 100 + ' in';
      if (used) track('hail', { size: h[2] }); used = true;
    }
    $('[data-hail]', el).addEventListener('click', function (ev) {
      var b = ev.target.closest('button');
      if (!b) return;
      $$('[data-hail] button', el).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      calc();
    });
    el.addEventListener('change', calc);
    bindSegs(el, calc);
    calc();
  }

  /* 6. Roof lifespan calculator -------------------------------------------- */
  var LIFE = {
    threetab: ['3-tab asphalt shingles', 17], arch: ['Architectural shingles', 22], class4: ['Class 4 impact-resistant shingles', 27],
    metal: ['Metal (standing seam)', 50], stone: ['Stone-coated steel', 45], tile: ['Clay / concrete tile', 45], tpo: ['TPO / flat membrane', 20]
  };
  function gaugeSvg(pct) {
    var a = Math.PI * (1 - pct);
    var x = 130 + 100 * Math.cos(a), y = 130 - 100 * Math.sin(a);
    return '<svg class="gauge" viewBox="0 0 260 150" role="img" aria-label="Remaining roof life gauge">' +
      '<defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#E62727"/><stop offset=".5" stop-color="#f2b200"/><stop offset="1" stop-color="#00AD48"/></linearGradient></defs>' +
      '<path d="M30 130 A100 100 0 0 1 230 130" fill="none" stroke="rgba(255,255,255,.15)" stroke-width="22" stroke-linecap="round"/>' +
      '<path d="M30 130 A100 100 0 0 1 230 130" fill="none" stroke="url(#gg)" stroke-width="22" stroke-linecap="round" stroke-dasharray="' + (314 * pct) + ' 400"/>' +
      '<line x1="130" y1="130" x2="' + x.toFixed(1) + '" y2="' + y.toFixed(1) + '" stroke="#fff" stroke-width="5" stroke-linecap="round"/><circle cx="130" cy="130" r="9" fill="#fff"/></svg>';
  }
  function lifespanTool(el) {
    el.innerHTML = head(el, 'Roof Lifespan Calculator') +
      '<div class="tool__grid"><div class="tool__fields">' +
      '<label>Roof material<select name="mat">' + Object.keys(LIFE).map(function (k) { return '<option value="' + k + '"' + (k === 'arch' ? ' selected' : '') + '>' + LIFE[k][0] + '</option>'; }).join('') + '</select></label>' +
      '<label>Roof age <span class="range-val" data-out="ageLbl">10 years</span><input type="range" name="age" min="0" max="60" value="10"></label>' +
      '<div class="field-label">Attic ventilation ' + seg('vent', [['1', 'Good'], ['0.9', 'Average'], ['0.8', 'Poor / not sure']], '0.9') + '</div>' +
      '<div class="field-label">Sun exposure ' + seg('sun', [['1.05', 'Mostly shaded'], ['1', 'Mixed'], ['0.92', 'Full Texas sun']], '0.92') + '</div>' +
      '<div class="field-label">Major hail storms since install ' + seg('hail', [['1', 'None'], ['0.92', 'One'], ['0.82', 'Two or more']], '1') + '</div>' +
      '<div class="field-label">Maintenance ' + seg('maint', [['1.03', 'Regular'], ['1', 'Occasional'], ['0.93', 'Never']], '1') + '</div>' +
      '</div><div class="tool__result" aria-live="polite"><h4>Estimated life remaining</h4><div data-out="gauge"></div><div class="big-num" data-out="left" style="text-align:center">—</div>' +
      '<p data-out="text" style="color:#d9eaee;margin-top:10px"></p>' +
      '<ul class="result-rows"><li><span>Expected total life in your conditions</span><span data-out="total"></span></li><li><span>Typical rated life</span><span data-out="base"></span></li></ul>' +
      '<p class="tool__note">Estimates based on typical Central Texas performance. Storm damage, installation quality and ventilation can shorten or extend real life.</p>' + ctaHtml('Get a free roof check-up') + '</div></div>';
    var used = false;
    function calc() {
      var m = LIFE[$('[name=mat]', el).value];
      var age = +$('[name=age]', el).value;
      var f = +segVal(el, 'vent') * +segVal(el, 'sun') * +segVal(el, 'hail') * +segVal(el, 'maint');
      var total = m[1] * f;
      var left = Math.max(total - age, 0);
      var pct = Math.max(Math.min(left / total, 1), 0);
      var text;
      if (pct > 0.6) text = 'Plenty of life left. Keep gutters clear and have the roof checked after major storms.';
      else if (pct > 0.3) text = 'Mid-life. Annual inspections and quick repairs now will help you reach the end of its rated life.';
      else if (left > 0) text = 'Getting close to the end of its service life. Start budgeting for a replacement and get an inspection before storm season.';
      else text = 'Past its expected life in these conditions. Have it inspected soon — especially before the spring hail season.';
      $('[data-out=ageLbl]', el).textContent = age + (age === 1 ? ' year' : ' years');
      $('[data-out=gauge]', el).innerHTML = gaugeSvg(pct);
      $('[data-out=left]', el).innerHTML = (left < 1 ? '0' : Math.round(left)) + ' years<small>' + Math.round(pct * 100) + '% of its life remaining</small>';
      $('[data-out=text]', el).textContent = text;
      $('[data-out=total]', el).textContent = '≈ ' + Math.round(total) + ' years';
      $('[data-out=base]', el).textContent = m[1] + ' years';
      if (used) track('lifespan'); used = true;
    }
    el.addEventListener('input', calc);
    el.addEventListener('change', calc);
    bindSegs(el, calc);
    calc();
  }

  var TOOLS = { cost: costTool, squares: squaresTool, pitch: pitchTool, quiz: quizTool, hail: hailTool, lifespan: lifespanTool };
  function init() {
    $$('.tool[data-tool]').forEach(function (el) {
      var fn = TOOLS[el.getAttribute('data-tool')];
      if (fn) { try { fn(el); } catch (e) { if (window.console) console.error(e); } }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
