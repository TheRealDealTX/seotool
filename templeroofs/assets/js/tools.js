/* Temple Roofers — roofing tools: cost calculator, pitch & area calculator, storm self-check. */
(function () {
  'use strict';

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function round(n, d) { var f = Math.pow(10, d || 0); return Math.round(n * f) / f; }
  function fmt(n, d) { return round(n, d).toLocaleString('en-US', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  /** Read a numeric input. Returns {ok, value, msg}. Empty -> fallback when allowed. */
  function readNum(input, opts) {
    var raw = input.value.trim();
    var errEl = document.getElementById(input.id + '-err');
    var res = { ok: true, value: null, msg: '' };
    if (raw === '') {
      if (opts.optional) { res.value = null; }
      else { res.ok = false; res.msg = opts.label + ' is required.'; }
    } else {
      var v = Number(raw);
      if (!isFinite(v)) { res.ok = false; res.msg = 'Enter a number.'; }
      else if (v < opts.min || v > opts.max) { res.ok = false; res.msg = opts.label + ' must be between ' + opts.min.toLocaleString() + ' and ' + opts.max.toLocaleString() + '.'; }
      else { res.value = v; }
    }
    if (errEl) { errEl.textContent = res.msg; errEl.hidden = res.ok; }
    if (res.ok) input.removeAttribute('aria-invalid'); else input.setAttribute('aria-invalid', 'true');
    return res;
  }

  /* =====================================================================
     1. Roof replacement cost calculator
     ===================================================================== */
  var costForm = $('[data-cost-form]');
  if (costForm) {
    var cfgEl = document.getElementById('cost-config');
    var C = JSON.parse(cfgEl.textContent);
    var out = function (k) { return $('[data-out="' + k + '"]'); };
    var tbody = $('[data-breakdown]');
    var bars = $('[data-bars]');
    var deck = $('#c-decking'), deckOut = $('#c-decking-out');

    var factorFor = function (table, key) {
      var best = 1;
      Object.keys(table).map(Number).sort(function (a, b) { return a - b; }).forEach(function (k) { if (key >= k) best = table[k]; });
      return best;
    };

    var calcCost = function () {
      deckOut.textContent = deck.value + '%';
      var area = readNum($('#c-area'), { label: 'Floor area', min: 400, max: 20000 });
      var waste = readNum($('#c-waste'), { label: 'Waste allowance', min: 0, max: 30, optional: true });
      if (!area.ok || !waste.ok) {
        out('total').textContent = 'Check your inputs';
        ['roof-area', 'squares', 'per-square'].forEach(function (k) { out(k).textContent = '—'; });
        out('material-label').textContent = '';
        tbody.innerHTML = '';
        bars.innerHTML = '';
        return;
      }
      var stories = parseInt($('#c-stories').value, 10);
      var rise = parseFloat($('#c-pitch').value);
      var mat = C.materials[$('#c-material').value];
      var layers = parseInt($('#c-layers').value, 10);
      var cx = C.complexity[$('#c-complexity').value];
      var deckPct = parseFloat(deck.value) / 100;
      var wastePct = (waste.value === null ? cx.waste : waste.value) / 100;

      var footprint = area.value / stories * C.overhang_factor;
      var slope = Math.sqrt(1 + Math.pow(rise / 12, 2));
      var roofArea = footprint * slope;
      var installSq = roofArea / 100;
      var orderSq = roofArea * (1 + wastePct) / 100;
      var laborMult = factorFor(C.pitch_labor, rise) * (C.story_labor[stories] || 1) * cx.labor;
      var sheets = Math.ceil(roofArea * deckPct / 32);

      var lines = [
        ['Roofing materials', orderSq * mat.material[0], orderSq * mat.material[1]],
        ['Underlayment, flashing & accessories', orderSq * C.accessories_per_square[0], orderSq * C.accessories_per_square[1]],
        ['Installation labor', installSq * mat.labor[0] * laborMult, installSq * mat.labor[1] * laborMult],
        ['Tear-off & disposal (' + layers + ' layer' + (layers === 1 ? '' : 's') + ')', installSq * layers * C.tearoff_per_square_per_layer[0], installSq * layers * C.tearoff_per_square_per_layer[1]],
        ['Decking (' + sheets + ' sheet' + (sheets === 1 ? '' : 's') + ')', sheets * C.decking_per_sheet[0], sheets * C.decking_per_sheet[1]]
      ];
      var lo = 0, hi = 0;
      lines.forEach(function (l) { lo += l[1]; hi += l[2]; });

      out('total').textContent = money(lo) + ' – ' + money(hi);
      out('material-label').textContent = mat.label + ' · ' + rise + '/12 pitch · ' + stories + ' stor' + (stories === 1 ? 'y' : 'ies');
      out('roof-area').textContent = fmt(roofArea);
      out('squares').textContent = fmt(orderSq, 1);
      out('per-square').textContent = money(lo / installSq) + '–' + money(hi / installSq);

      tbody.innerHTML = lines.map(function (l) {
        return '<tr><td>' + esc(l[0]) + '</td><td>' + money(l[1]) + '</td><td>' + money(l[2]) + '</td></tr>';
      }).join('') + '<tr class="total-row"><td>Estimated total</td><td>' + money(lo) + '</td><td>' + money(hi) + '</td></tr>';

      var maxHi = Math.max.apply(null, lines.map(function (l) { return l[2]; })) || 1;
      bars.innerHTML = lines.map(function (l) {
        var mid = (l[1] + l[2]) / 2;
        return '<div class="bar"><span>' + esc(l[0].split(' (')[0]) + '</span><span class="bar__track"><span class="bar__fill" style="width:' + (mid / maxHi * 100).toFixed(1) + '%"></span></span></div>';
      }).join('');
    };

    costForm.addEventListener('input', calcCost);
    costForm.addEventListener('change', calcCost);
    costForm.addEventListener('submit', function (e) { e.preventDefault(); });
    $('[data-reset]', costForm).addEventListener('click', function () { costForm.reset(); calcCost(); });
    calcCost();
  }

  /* =====================================================================
     2. Roof pitch & area calculator
     ===================================================================== */
  var pitchForm = $('[data-pitch-form]');
  if (pitchForm) {
    var o = function (k) { return $('[data-out="' + k + '"]'); };
    var svg = $('[data-pitch-svg]');
    var modeVal = function (name) { var r = pitchForm.querySelector('input[name="' + name + '"]:checked'); return r ? r.value : ''; };

    var drawDiagram = function (rise, run) {
      // Base fixed at 280px; height scaled by slope, capped to fit the viewBox.
      var base = 280, maxH = 140;
      var h = Math.min(base * rise / run, maxH);
      var w = h === maxH && rise > 0 ? maxH * run / rise : base;
      var x0 = 300 - w, y0 = 160;
      $('[data-pd-tri]', svg).setAttribute('points', x0 + ',160 300,160 300,' + (160 - h));
      var r = $('[data-pd-rise]', svg);
      r.setAttribute('y2', 160 - h);
      $('[data-pd-run]', svg).setAttribute('x', x0 + w / 2);
      $('[data-pd-run]', svg).textContent = 'Run ' + fmt(run, 2).replace(/\.?0+$/, '') + '"';
      var rt = $('[data-pd-risetxt]', svg);
      rt.setAttribute('y', 160 - h / 2 + 4);
      rt.setAttribute('x', 306);
      rt.textContent = 'Rise ' + fmt(rise, 2).replace(/\.?0+$/, '') + '"';
      var ang = Math.atan2(rise, run);
      var R = 44;
      var ax = x0 + R * Math.cos(ang), ay = y0 - R * Math.sin(ang);
      $('[data-pd-arc]', svg).setAttribute('d', 'M' + (x0 + R) + ' ' + y0 + ' A' + R + ' ' + R + ' 0 0 0 ' + ax.toFixed(1) + ' ' + ay.toFixed(1));
      var lbl = $('[data-pd-angle]', svg);
      lbl.setAttribute('x', x0 + R + 8);
      lbl.setAttribute('y', 152);
      lbl.textContent = fmt(ang * 180 / Math.PI, 1) + '°';
    };

    var classify = function (p) {
      if (p < 2) return 'Flat / very low slope: requires a membrane roofing system rather than shingles.';
      if (p < 4) return 'Low slope: shingles are generally only allowed from 2/12 to below 4/12 with double-layer underlayment — check manufacturer and code requirements.';
      if (p < 7) return 'Conventional slope: the most common range for Central Texas homes and suitable for shingles and metal.';
      if (p < 10) return 'Steep slope: expect added labor and safety equipment.';
      return 'Very steep slope: specialized staging and higher labor costs are typical.';
    };

    var calcPitch = function () {
      var mode = modeVal('mode'), amode = modeVal('amode');
      $$('[data-mode-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-mode-panel') !== mode; });
      $$('[data-area-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-area-panel') !== amode; });

      var rise, run = 12, ok = true;
      if (mode === 'rise') {
        var r1 = readNum($('#p-rise'), { label: 'Rise', min: 0, max: 48 });
        var r2 = readNum($('#p-run'), { label: 'Run', min: 1, max: 48 });
        ok = r1.ok && r2.ok;
        if (ok) { rise = r1.value; run = r2.value; }
      } else {
        var a = readNum($('#p-angle'), { label: 'Angle', min: 0, max: 75 });
        ok = a.ok;
        if (ok) { rise = Math.tan(a.value * Math.PI / 180) * 12; run = 12; }
      }
      var footprint = null;
      if (amode === 'dims') {
        var L = readNum($('#p-length'), { label: 'Length', min: 1, max: 500 });
        var W = readNum($('#p-width'), { label: 'Width', min: 1, max: 500 });
        var OH = readNum($('#p-overhang'), { label: 'Overhang', min: 0, max: 48 });
        if (L.ok && W.ok && OH.ok) {
          var oh = OH.value / 12;
          footprint = (L.value + 2 * oh) * (W.value + 2 * oh);
        } else ok = false;
      } else {
        var F = readNum($('#p-flat'), { label: 'Footprint area', min: 10, max: 100000 });
        if (F.ok) footprint = F.value; else ok = false;
      }
      var wst = readNum($('#p-waste'), { label: 'Waste', min: 0, max: 30 });
      if (!wst.ok) ok = false;

      if (rise === undefined) {
        ['pitch', 'angle', 'multiplier', 'grade'].forEach(function (k) { o(k).textContent = '—'; });
      } else {
        var ratio = rise / run;
        var per12 = ratio * 12;
        var multiplier = Math.sqrt(1 + ratio * ratio);
        o('pitch').textContent = fmt(per12, 2).replace(/\.00$/, '') + '/12';
        o('angle').textContent = fmt(Math.atan(ratio) * 180 / Math.PI, 1) + '°';
        o('multiplier').textContent = fmt(multiplier, 3);
        o('grade').textContent = fmt(ratio * 100, 1) + '%';
        o('class').textContent = classify(per12);
        drawDiagram(rise, run);
      }
      if (!ok || footprint === null || rise === undefined) {
        ['footprint', 'area', 'squares', 'bundles'].forEach(function (k) { o(k).textContent = '—'; });
        return;
      }
      var m = Math.sqrt(1 + Math.pow(rise / run, 2));
      var area = footprint * m;
      var squares = area * (1 + wst.value / 100) / 100;
      var bundles = Math.ceil(squares * parseInt($('#p-bundles').value, 10) - 1e-9);
      o('footprint').textContent = fmt(footprint);
      o('area').textContent = fmt(area);
      o('squares').textContent = fmt(squares, 1);
      o('bundles').textContent = fmt(bundles);
    };
    pitchForm.addEventListener('input', calcPitch);
    pitchForm.addEventListener('change', calcPitch);
    pitchForm.addEventListener('submit', function (e) { e.preventDefault(); });
    calcPitch();
  }

  /* =====================================================================
     3. Storm & hail damage self-check (qualitative guidance only)
     ===================================================================== */
  var stormForm = $('[data-storm-form]');
  if (stormForm) {
    // Weight = how strongly a sign suggests a professional should look (not a probability).
    var SIGNS = {
      missing_shingles: { w: 3, step: 'Missing shingles leave the underlayment exposed. Photograph the area from the ground and arrange a prompt inspection — temporary protection may be needed before the next rain.' },
      dented_gutters: { w: 2, step: 'Dents in gutters, downspouts or vents often mean hail also struck the shingles. Photograph the dents with a coin or ruler for scale.' },
      granules: { w: 2, step: 'Heavy granule wash can indicate hail bruising or an aging roof. Take a photo of the pile and note when you noticed it.' },
      bent_flashing: { w: 2, step: 'Lifted or bent flashing lets wind-driven rain in at walls, chimneys and edges. Have it checked before the next storm.' },
      ceiling_stains: { w: 3, step: 'Mark the edge of each stain with pencil and date it so you can see if it grows. Check the attic above only if it is safe to reach.' },
      broken_vents: { w: 2, step: 'Cracked or dented vents can leak around their base. Note which vents and on which side of the house.' },
      active_leak: { w: 4, step: 'For active leaks: move belongings, catch water in containers, and keep clear of any sagging ceiling. If water is near light fixtures or outlets, turn off power to that area at the breaker if it is safe to do so.' },
      debris: { w: 1, step: 'Collect a few shingle fragments in a bag as evidence, and photograph where they landed.' },
      branches: { w: 3, step: 'Do not try to remove limbs from the roof yourself. A tree professional should remove large limbs, then the roof decking should be checked for punctures.' },
      other_exterior: { w: 1, step: 'Photograph other damaged items (AC fins, fences, siding, vehicles) — they help show the storm\'s intensity at your address.' }
    };
    var levels = [
      { min: 0, key: 'none', pos: 4, title: 'No visible signs selected', text: 'You have not noted any visible damage. Hail and wind damage can still be hard to see from the ground, so keep an eye on ceilings and gutters over the next few rains.' },
      { min: 1, key: 'low', pos: 28, title: 'Monitor and consider an inspection', text: 'The signs you noted are minor on their own. A free inspection is reasonable if the storm was strong or your roof is older.' },
      { min: 3, key: 'medium', pos: 60, title: 'A professional inspection is recommended', text: 'Several signs together suggest the roof may have been affected. A professional inspection can confirm what is happening up close.' },
      { min: 6, key: 'high', pos: 92, title: 'Schedule an inspection soon', text: 'Your answers include signs that often lead to leaks or further damage. Arrange an inspection promptly and protect the interior in the meantime.' }
    ];
    var meter = $('.meter');
    var fill = $('[data-meter-fill]');

    var calcStorm = function () {
      var checked = $$('input[name="signs"]:checked', stormForm).map(function (i) { return i.value; });
      var score = checked.reduce(function (s, k) { return s + SIGNS[k].w; }, 0);
      var lvl = levels[0];
      levels.forEach(function (l) { if (score >= l.min) lvl = l; });
      if (checked.indexOf('active_leak') > -1 || (checked.indexOf('ceiling_stains') > -1 && checked.indexOf('missing_shingles') > -1)) lvl = levels[3];

      meter.setAttribute('data-level', lvl.key);
      fill.style.left = lvl.pos + '%';
      $('[data-out="level"]').textContent = lvl.title;
      $('[data-out="summary"]').textContent = lvl.text;

      var storm = $('#s-storm').value, when = $('#s-when').value;
      var steps = ['Stay off the roof. Check from the ground, through windows and — only if safely accessible — from the attic.'];
      checked.sort(function (a, b) { return SIGNS[b].w - SIGNS[a].w; }).forEach(function (k) { steps.push(SIGNS[k].step); });
      if (storm === 'hail' || storm === 'both') steps.push('Write down the storm date and approximate hail size. Hail damage is often invisible from the ground, so a close inspection matters even if the roof looks fine.');
      if (storm === 'wind' || storm === 'both') steps.push('Wind can break shingle seals without removing shingles. Watch for shingles that lift or flap on breezy days.');
      if (checked.length) steps.push('Photograph everything before cleanup and keep receipts for any emergency supplies.');
      if (when === 'older') steps.push('Damage noticed weeks after a storm is still worth documenting. Insurance policies have their own reporting deadlines, so check your policy or ask your agent.');
      if (checked.length) steps.push('If you plan to contact your insurer, a roofer\'s photos and repair estimate can help — but only your insurance company decides coverage. Never sign with a contractor who offers to waive your deductible.');
      steps.push(lvl.key === 'none' ? 'If anything changes, come back to this checklist or request a free inspection for peace of mind.' : 'Request a free, no-obligation inspection from Temple Roofers to confirm what is happening up close.');
      $('[data-out="steps"]').innerHTML = steps.map(function (s) { return '<li>' + esc(s) + '</li>'; }).join('');
    };
    stormForm.addEventListener('change', calcStorm);
    $('[data-reset]', stormForm).addEventListener('click', function () { stormForm.reset(); calcStorm(); });
    var printBtn = $('[data-print]');
    if (printBtn) printBtn.addEventListener('click', function () { window.print(); });
    calcStorm();
  }
})();
