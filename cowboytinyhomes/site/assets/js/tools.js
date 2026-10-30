// Cowboy Tiny Homes — interactive planning tools.
// Each tool mounts on an element with data-tool="<name>". The shared cost
// model below is the single source for every cost figure the tools show.
(function () {
  'use strict';

  // Texas 2026 planning ranges, $ per finished sq ft at "standard" finishes,
  // builder-built (not DIY). Size limits are typical for each home type.
  var COST = {
    thow:   { label: 'Tiny home on wheels', low: 175, high: 300, min: 120, max: 400, def: 260 },
    park:   { label: 'Park model home',      low: 150, high: 260, min: 250, max: 399, def: 399 },
    adu:    { label: 'ADU / casita',         low: 190, high: 340, min: 300, max: 1200, def: 600 },
    custom: { label: 'Custom tiny or small home on a foundation', low: 175, high: 320, min: 400, max: 1800, def: 900 }
  };
  var FINISH = { basic: 0.85, standard: 1, premium: 1.3 };

  function money(n) {
    n = Math.round(n / 500) * 500;
    return '$' + n.toLocaleString('en-US');
  }
  function money0(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function $(root, sel) { return root.querySelector(sel); }
  function $$(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function val(root, name) {
    var el = root.querySelector('[name="' + name + '"]:checked') || root.querySelector('[name="' + name + '"]:not([type=radio]):not([type=checkbox])');
    return el ? el.value : '';
  }
  function num(root, name) { var v = parseFloat(val(root, name)); return isNaN(v) ? 0 : v; }
  function setText(root, sel, txt) { var el = root.querySelector(sel); if (el) el.textContent = txt; }
  function setHref(root, sel, href) { var el = root.querySelector(sel); if (el) el.href = href; }
  function qs(obj) {
    var out = [];
    for (var k in obj) if (obj.hasOwnProperty(k) && obj[k] !== '' && obj[k] != null) out.push(encodeURIComponent(k) + '=' + encodeURIComponent(obj[k]));
    return out.join('&');
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function param(name) {
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(window.location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : '';
  }
  // Monthly principal & interest payment.
  function payment(principal, ratePct, years) {
    if (principal <= 0) return 0;
    var r = ratePct / 100 / 12, n = Math.max(1, Math.round(years * 12));
    if (r === 0) return principal / n;
    return principal * r / (1 - Math.pow(1 + r, -n));
  }
  function bindRangeOutputs(root) {
    $$(root, 'input[type=range]').forEach(function (r) {
      var out = root.querySelector('output[for="' + r.id + '"]');
      var fmt = r.getAttribute('data-fmt') || '';
      function upd() {
        if (!out) return;
        var v = Number(r.value);
        out.textContent = fmt === 'money' ? money0(v) : fmt === 'pct' ? v + '%' : fmt === 'yr' ? v + ' yrs' :
          fmt === 'sqft' ? v.toLocaleString('en-US') + ' sq ft' : fmt === 'rate' ? v.toFixed(2) + '%' : v.toLocaleString('en-US');
      }
      r.addEventListener('input', upd);
      upd();
    });
  }
  function live(root, fn) {
    root.addEventListener('input', fn);
    root.addEventListener('change', fn);
  }

  var tools = {};

  // Homepage quick estimate: type + size + finish => range.
  tools['mini-estimate'] = function (root) {
    var size = $(root, '[name=size]');
    function setLimits() {
      var c = COST[val(root, 'type')];
      size.min = c.min; size.max = c.max;
      if (+size.value < c.min || +size.value > c.max) size.value = c.def;
      size.dispatchEvent(new Event('input'));
    }
    function calc() {
      var c = COST[val(root, 'type')], f = FINISH[val(root, 'finish')], s = +size.value;
      $(root, '[data-out=range]').textContent = money(c.low * f * s) + ' – ' + money(c.high * f * s);
      $(root, '[data-out=note]').textContent = c.label + ', ' + s + ' sq ft, ' + val(root, 'finish') + ' finishes. Land, utilities and site work are extra.';
      var link = $(root, '[data-out=link]');
      if (link) link.href = '/tools/tiny-home-cost-calculator/?type=' + val(root, 'type') + '&size=' + s + '&finish=' + val(root, 'finish');
    }
    bindRangeOutputs(root);
    $$(root, '[name=type]').forEach(function (el) { el.addEventListener('change', function () { setLimits(); calc(); }); });
    root.addEventListener('input', calc);
    root.addEventListener('change', calc);
    setLimits();
    calc();
  };

  // ---------------------------------------------------------------------
  // Full cost calculator.
  // Add-on ranges (low, high). Some only apply to certain home types.
  var ADDONS = {
    design:   { label: 'Design, engineering & permits', low: 3500, high: 12000, types: ['thow', 'park', 'adu', 'custom'] },
    site:     { label: 'Site prep & foundation / pad',  low: 6000, high: 30000, types: ['thow', 'park', 'adu', 'custom'] },
    utility:  { label: 'Utility hookups (water, power, sewer)', low: 5000, high: 25000, types: ['thow', 'park', 'adu', 'custom'] },
    septic:   { label: 'Septic system',                 low: 7000, high: 18000, types: ['thow', 'park', 'adu', 'custom'] },
    well:     { label: 'Water well',                    low: 9000, high: 30000, types: ['thow', 'park', 'adu', 'custom'] },
    solar:    { label: 'Solar power system',            low: 12000, high: 35000, types: ['thow', 'park', 'adu', 'custom'] },
    porch:    { label: 'Covered porch or deck',         low: 5000, high: 20000, types: ['thow', 'park', 'adu', 'custom'] },
    delivery: { label: 'Delivery & setup',              low: 2000, high: 8000, types: ['thow', 'park'] },
    hvac:     { label: 'Ductless mini-split upgrade',   low: 3000, high: 9000, types: ['thow', 'park', 'adu', 'custom'] },
    appl:     { label: 'Appliance package',             low: 3500, high: 12000, types: ['thow', 'park', 'adu', 'custom'] }
  };

  tools['cost-calculator'] = function (root) {
    var size = $(root, '[name=size]');
    if (!size) return;
    var pType = param('type'), pSize = parseInt(param('size'), 10), pFinish = param('finish');
    if (COST[pType]) { var r = root.querySelector('[name=type][value="' + pType + '"]'); if (r) r.checked = true; }
    if (FINISH[pFinish]) { var f = root.querySelector('[name=finish][value="' + pFinish + '"]'); if (f) f.checked = true; }

    function setLimits(keep) {
      var c = COST[val(root, 'type')];
      size.min = c.min; size.max = c.max;
      if (!keep && (+size.value < c.min || +size.value > c.max)) size.value = c.def;
      size.dispatchEvent(new Event('input'));
      $$(root, '[data-addon]').forEach(function (cb) {
        var a = ADDONS[cb.getAttribute('data-addon')], ok = a.types.indexOf(val(root, 'type')) !== -1;
        cb.disabled = !ok;
        if (!ok) cb.checked = false;
        var wrap = cb.closest('label'); if (wrap) wrap.style.opacity = ok ? '' : '.45';
      });
    }
    function calc() {
      var type = val(root, 'type'), c = COST[type], fin = val(root, 'finish') || 'standard', fm = FINISH[fin], s = +size.value;
      var regionEl = $(root, '[name=region]'), rf = regionEl ? (+regionEl.value || 1) : 1;
      var regionName = regionEl ? regionEl.options[regionEl.selectedIndex].text : 'Texas average';
      var beds = num(root, 'beds'), lofts = num(root, 'lofts');
      var rows = [];
      rows.push({ label: 'Home build (' + s + ' sq ft, ' + fin + ')', low: c.low * fm * s, high: c.high * fm * s });
      // Extra bedrooms add walls, doors, windows and a closet; lofts add framing, stairs or a ladder.
      var extraBeds = Math.max(0, beds - 1);
      if (extraBeds) rows.push({ label: extraBeds + ' extra bedroom' + (extraBeds > 1 ? 's' : '') + ' (walls, doors, closets)', low: 3000 * extraBeds * fm, high: 7000 * extraBeds * fm });
      if (lofts) rows.push({ label: lofts + ' sleeping loft' + (lofts > 1 ? 's' : '') + ' with stairs or ladder', low: 2500 * lofts * fm, high: 6500 * lofts * fm });
      $$(root, '[data-addon]:checked').forEach(function (cb) {
        var a = ADDONS[cb.getAttribute('data-addon')];
        rows.push({ label: a.label, low: a.low, high: a.high });
      });
      // Regional labor and material prices scale every line.
      rows.forEach(function (r) { r.low *= rf; r.high *= rf; });
      var low = 0, high = 0;
      rows.forEach(function (r) { low += r.low; high += r.high; });
      setText(root, '[data-out=total]', money(low) + ' – ' + money(high));
      setText(root, '[data-out=persqft]', money0(low / s) + ' – ' + money0(high / s) + ' per sq ft all-in');
      var list = $(root, '[data-out=rows]');
      if (list) {
        list.innerHTML = rows.map(function (r) {
          var pct = Math.max(3, Math.round((r.low + r.high) / (low + high) * 100));
          return '<li style="display:block"><span style="display:flex;justify-content:space-between;gap:10px"><span>' + esc(r.label) + '</span><b>' +
            money(r.low) + ' – ' + money(r.high) + '</b></span><div class="bar"><i style="width:' + pct + '%"></i></div></li>';
        }).join('');
      }
      var mid = (low + high) / 2, rate = num(root, 'rate') || 8.5;
      var pay = payment(mid * 0.9, rate, 15);
      setText(root, '[data-out=monthly]', money0(pay) + '/mo');
      setText(root, '[data-out=monthly-note]', 'Midpoint ' + money(mid) + ', 10% down, ' + rate.toFixed(2) + '% for 15 years (illustrative).');
      setHref(root, '[data-out=link]', '/contact-us/?' + qs({ project: type, size: s, budget: money(low) + '-' + money(high), note: c.label + ', ' + fin + ' finishes, ' + beds + ' bed, ' + lofts + ' loft, ' + regionName }));
    }
    bindRangeOutputs(root);
    $$(root, '[name=type]').forEach(function (el) { el.addEventListener('change', function () { setLimits(false); calc(); }); });
    live(root, calc);
    // Apply the type's limits before the URL size, or the range would clamp it.
    var c0 = COST[val(root, 'type')];
    size.min = c0.min; size.max = c0.max;
    if (pSize) size.value = Math.max(c0.min, Math.min(c0.max, pSize));
    setLimits(!!pSize);
    calc();
  };

  // ---------------------------------------------------------------------
  // Quiz: which tiny home is right for me. Each answer adds points to types.
  var QUIZ_TYPES = {
    thow:   { label: 'Tiny home on wheels', url: '/tiny-homes-on-wheels-texas/', why: 'You value mobility and flexibility. A tiny house on a bumper-pull or gooseneck trailer can follow you to an RV park, family land or a new job, and it is often regulated as an RV instead of a house.' },
    park:   { label: 'Park model home', url: '/park-model-homes-texas/', why: 'You want a cabin-style home under 400 sq ft that can sit in an RV park, on ranch or lake land, or serve as a getaway — more room than a THOW, without a full foundation build.' },
    adu:    { label: 'ADU / backyard casita', url: '/adu-builders-texas/', why: 'You already have (or will have) a home lot. A permanent accessory dwelling unit adds space for family, guests or rental income and adds lasting value to the property.' },
    custom: { label: 'Custom tiny or small home on a foundation', url: '/custom-tiny-homes-texas/', why: 'You want a permanent, full-time home on your own land, built to the International Residential Code, with the easiest path to a conventional mortgage and resale.' }
  };

  tools['quiz'] = function (root) {
    var qsEls = $$(root, '.quiz-q');
    if (!qsEls.length) return;
    var answers = [], cur = 0;
    var prog = $(root, '.quiz-progress i');
    var back = $(root, '[data-quiz-back]');
    var result = $(root, '.quiz-result');
    function show(i) {
      cur = i;
      qsEls.forEach(function (q, k) { q.classList.toggle('is-active', k === i); });
      if (result) result.classList.remove('is-active');
      if (prog) prog.style.width = Math.round(i / qsEls.length * 100) + '%';
      if (back) back.hidden = i === 0;
      var first = qsEls[i] && qsEls[i].querySelector('.quiz-opt');
      if (first && answers.length) first.focus();
    }
    function finish() {
      var score = { thow: 0, park: 0, adu: 0, custom: 0 }, max = 0;
      answers.forEach(function (a) {
        a.split(',').forEach(function (pair) {
          var p = pair.split(':'); if (score.hasOwnProperty(p[0])) score[p[0]] += +p[1];
        });
      });
      // Max possible = sum of best option per question.
      qsEls.forEach(function (q) {
        var best = 0;
        $$(q, '.quiz-opt').forEach(function (o) {
          var tot = {}; o.getAttribute('data-score').split(',').forEach(function (pair) { var p = pair.split(':'); tot[p[0]] = +p[1]; });
          for (var k in tot) if (tot[k] > best) best = tot[k];
        });
        max += best;
      });
      var ranked = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; });
      var top = QUIZ_TYPES[ranked[0]];
      setText(root, '[data-out=top]', top.label);
      setText(root, '[data-out=why]', top.why);
      setHref(root, '[data-out=top-link]', top.url);
      setHref(root, '[data-out=quote]', '/contact-us/?' + qs({ project: ranked[0], note: 'Quiz match: ' + top.label }));
      var bars = $(root, '[data-out=bars]');
      if (bars) bars.innerHTML = ranked.map(function (k) {
        var pct = Math.max(5, Math.min(100, Math.round(score[k] / max * 100)));
        return '<div class="match"><a href="' + QUIZ_TYPES[k].url + '"><strong>' + esc(QUIZ_TYPES[k].label) + '</strong></a><b>' + pct + '% match</b><div class="bar"><i style="width:' + pct + '%"></i></div></div>';
      }).join('');
      qsEls.forEach(function (q) { q.classList.remove('is-active'); });
      if (prog) prog.style.width = '100%';
      if (back) back.hidden = true;
      if (result) { result.classList.add('is-active'); result.setAttribute('tabindex', '-1'); result.focus(); }
    }
    qsEls.forEach(function (q, i) {
      $$(q, '.quiz-opt').forEach(function (o) {
        o.addEventListener('click', function () {
          answers[i] = o.getAttribute('data-score');
          answers.length = i + 1;
          if (i + 1 < qsEls.length) show(i + 1); else finish();
        });
      });
    });
    if (back) back.addEventListener('click', function () { if (cur > 0) show(cur - 1); });
    $$(root, '[data-quiz-restart]').forEach(function (b) { b.addEventListener('click', function () { answers = []; show(0); }); });
    show(0);
  };

  // ---------------------------------------------------------------------
  // Size planner. Room sizes are typical small-home planning areas (sq ft).
  tools['size-planner'] = function (root) {
    var rooms = $$(root, '[data-room]');
    if (!rooms.length) return;
    rooms.forEach(function (r) {
      var out = $(r, 'output'), min = +(r.getAttribute('data-min') || 0), max = +(r.getAttribute('data-max') || 6);
      $$(r, 'button').forEach(function (b) {
        b.addEventListener('click', function () {
          var v = +out.value || 0;
          v = Math.max(min, Math.min(max, v + (b.getAttribute('data-step') === '+' ? 1 : -1)));
          out.value = v; out.textContent = v;
          calc();
        });
      });
    });
    function calc() {
      var interior = 0, loft = 0, porch = 0, beds = 0;
      rooms.forEach(function (r) {
        var n = +$(r, 'output').value || 0, a = +r.getAttribute('data-sqft'), kind = r.getAttribute('data-kind') || '';
        if (kind === 'loft') loft += n * a;
        else if (kind === 'porch') porch += n * a;
        else interior += n * a;
        if (r.getAttribute('data-room') === 'bedroom') beds += n;
      });
      var circ = Math.round(interior * 0.15);
      var total = interior + circ;
      setText(root, '[data-out=total]', total.toLocaleString('en-US') + ' sq ft');
      setText(root, '[data-out=detail]', interior + ' sq ft of rooms + ' + circ + ' sq ft for walls, halls and stairs (15%).');
      setText(root, '[data-out=loft]', loft ? loft + ' sq ft (not counted in footprint)' : 'None');
      setText(root, '[data-out=porch]', porch ? porch + ' sq ft (outdoor)' : 'None');
      var fit = $(root, '[data-out=fit]');
      var fits = [];
      Object.keys(COST).forEach(function (k) {
        var c = COST[k], tag, txt;
        if (total <= c.max && total >= c.min * 0.8) { tag = 'yes'; txt = 'Fits'; }
        else if (total < c.min * 0.8) { tag = k === 'thow' || k === 'park' ? 'yes' : 'maybe'; txt = tag === 'yes' ? 'Fits' : 'Smaller than typical'; }
        else if (total <= c.max * 1.15) { tag = 'maybe'; txt = 'Tight — trim a room'; }
        else { tag = 'no'; txt = 'Too large'; }
        if (k === 'thow' && total > 300 && tag === 'yes') { tag = 'maybe'; txt = 'Long trailer needed'; }
        fits.push({ k: k, tag: tag, txt: txt });
      });
      if (fit) fit.innerHTML = fits.map(function (f) {
        return '<li><span>' + esc(COST[f.k].label) + '</span><span class="tag tag--' + f.tag + '">' + esc(f.txt) + '</span></li>';
      }).join('');
      // Budget: cheapest fitting type at standard finishes.
      var best = fits.filter(function (f) { return f.tag !== 'no'; }).map(function (f) { return f.k; });
      var lowT = Infinity, highT = 0;
      best.forEach(function (k) { lowT = Math.min(lowT, COST[k].low * total); highT = Math.max(highT, COST[k].high * total); });
      setText(root, '[data-out=budget]', best.length ? money(lowT) + ' – ' + money(highT) : 'Custom quote');
      var type = best.length ? best[best.length - 1] : 'custom';
      setHref(root, '[data-out=link]', '/contact-us/?' + qs({ project: type, size: total, note: beds + ' bedroom plan from the size planner' + (loft ? ', plus ' + loft + ' sq ft loft' : '') }));
      setHref(root, '[data-out=calc]', '/tools/tiny-home-cost-calculator/?' + qs({ type: type, size: Math.max(COST[type].min, Math.min(COST[type].max, total)), finish: 'standard' }));
    }
    calc();
  };

  // ---------------------------------------------------------------------
  // ADU rental income calculator.
  tools['adu-rental'] = function (root) {
    if (!$(root, '[name=build]')) return;
    bindRangeOutputs(root);
    function modeSync() {
      var st = val(root, 'mode') === 'str';
      $$(root, '[data-mode]').forEach(function (el) { el.hidden = el.getAttribute('data-mode') !== (st ? 'str' : 'ltr'); });
      var fin = val(root, 'funding') === 'loan';
      $$(root, '[data-funding]').forEach(function (el) { el.hidden = !fin; });
    }
    function calc() {
      modeSync();
      var build = num(root, 'build'), loan = val(root, 'funding') === 'loan';
      var downPct = loan ? num(root, 'down') : 100, rate = num(root, 'rate'), term = num(root, 'term');
      var cash = build * downPct / 100, principal = build - cash;
      var debt = loan ? payment(principal, rate, term) : 0;
      var income, platform = 0, cleaning = 0;
      if (val(root, 'mode') === 'str') {
        var nights = 30.4 * num(root, 'occupancy') / 100, nightly = num(root, 'nightly');
        var stays = nights / Math.max(1, num(root, 'stay'));
        income = nights * nightly;
        cleaning = stays * num(root, 'clean');
        platform = income * num(root, 'platform') / 100;
      } else {
        income = num(root, 'rent') * (1 - num(root, 'vacancy') / 100);
      }
      var tax = num(root, 'tax') / 12, ins = num(root, 'ins') / 12, maint = income * num(root, 'maint') / 100;
      var util = num(root, 'util'), mgmt = income * num(root, 'mgmt') / 100;
      var expenses = tax + ins + maint + util + mgmt + platform + cleaning;
      var net = income - expenses - debt;
      var annual = net * 12;
      var roi = cash > 0 ? annual / cash * 100 : 0;
      var noi = (income - expenses) * 12;
      setText(root, '[data-out=net]', (net < 0 ? '−' : '') + money0(Math.abs(net)) + '/mo');
      setText(root, '[data-out=income]', money0(income));
      setText(root, '[data-out=expenses]', money0(expenses));
      setText(root, '[data-out=debt]', money0(debt));
      setText(root, '[data-out=annual]', (annual < 0 ? '−' : '') + money0(Math.abs(annual)));
      setText(root, '[data-out=roi]', cash > 0 ? roi.toFixed(1) + '%' : '—');
      setText(root, '[data-out=payback]', noi > 0 ? (build / noi).toFixed(1) + ' years' : 'Does not pay back at these numbers');
      var tot = Math.max(income, expenses + debt, 1);
      var bi = $(root, '[data-bar=income]'), be = $(root, '[data-bar=costs]');
      if (bi) bi.style.width = Math.round(income / tot * 100) + '%';
      if (be) be.style.width = Math.round((expenses + debt) / tot * 100) + '%';
      setHref(root, '[data-out=link]', '/contact-us/?' + qs({ project: 'adu', budget: money0(build), note: 'ADU rental: ' + (val(root, 'mode') === 'str' ? 'short-term' : 'long-term') + ', est. ' + money0(income) + '/mo income, ' + money0(net) + '/mo cash flow' }));
    }
    live(root, calc);
    calc();
  };

  // ---------------------------------------------------------------------
  // Loan calculator with presets and amortization.
  var LOAN_PRESETS = {
    rv:       { rate: 8.5, term: 15 },
    personal: { rate: 12, term: 7 },
    heloc:    { rate: 8.25, term: 20 },
    mortgage: { rate: 6.75, term: 30 },
    construction: { rate: 7.25, term: 30 }
  };
  tools['loan'] = function (root) {
    var rateEl = $(root, '[name=rate]'), termEl = $(root, '[name=term]');
    if (!rateEl || !termEl) return;
    bindRangeOutputs(root);
    $$(root, '[name=preset]').forEach(function (p) {
      p.addEventListener('change', function () {
        var pr = LOAN_PRESETS[p.value]; if (!pr) return;
        rateEl.value = pr.rate; termEl.value = pr.term;
        rateEl.dispatchEvent(new Event('input')); termEl.dispatchEvent(new Event('input'));
      });
    });
    function calc() {
      var price = num(root, 'price'), downPct = num(root, 'down'), rate = num(root, 'rate'), term = num(root, 'term');
      var down = price * downPct / 100, principal = Math.max(0, price - down);
      var pay = payment(principal, rate, term), n = Math.round(term * 12);
      var totalPaid = pay * n, interest = Math.max(0, totalPaid - principal);
      setText(root, '[data-out=pay]', money0(pay) + '/mo');
      setText(root, '[data-out=principal]', money0(principal));
      setText(root, '[data-out=down]', money0(down));
      setText(root, '[data-out=interest]', money0(interest));
      setText(root, '[data-out=total]', money0(totalPaid + down));
      var bp = $(root, '[data-bar=principal]'), bi = $(root, '[data-bar=interest]');
      var t = principal + interest || 1;
      if (bp) bp.style.width = Math.round(principal / t * 100) + '%';
      if (bi) bi.style.width = Math.round(interest / t * 100) + '%';
      // Year-by-year schedule.
      var body = $(root, '[data-out=amort]');
      if (body) {
        var bal = principal, r = rate / 100 / 12, html = '';
        for (var y = 1; y <= Math.ceil(term); y++) {
          var yp = 0, yi = 0;
          for (var m = 0; m < 12 && bal > 0.005; m++) {
            var int = bal * r, pr = Math.min(bal, pay - int);
            if (r === 0) { int = 0; pr = Math.min(bal, pay); }
            yi += int; yp += pr; bal -= pr;
          }
          html += '<tr><td>Year ' + y + '</td><td>' + money0(yp) + '</td><td>' + money0(yi) + '</td><td>' + money0(Math.max(0, bal)) + '</td></tr>';
          if (bal <= 0.005) break;
        }
        body.innerHTML = html;
      }
      var preset = $(root, '[name=preset]:checked');
      setHref(root, '[data-out=link]', '/contact-us/?' + qs({ budget: money0(price), note: 'Loan estimate: ' + (preset ? preset.getAttribute('data-label') : 'custom') + ', ' + downPct + '% down, ' + rate + '% for ' + term + ' yrs = ' + money0(pay) + '/mo' }));
    }
    live(root, calc);
    calc();
  };

  window.CTH = { COST: COST, FINISH: FINISH, ADDONS: ADDONS, money: money, money0: money0, val: val, payment: payment, bindRangeOutputs: bindRangeOutputs, tools: tools };

  document.addEventListener('DOMContentLoaded', function () {
    $$(document, '[data-tool]').forEach(function (el) {
      var fn = tools[el.getAttribute('data-tool')];
      if (fn) fn(el);
    });
  });
})();
