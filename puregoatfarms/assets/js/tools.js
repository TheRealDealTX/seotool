/* Pure Goat Farms — interactive goat calculators. Each tool initialises from
   its [data-tool] container; all maths runs locally in the browser. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var LB_PER_GAL = 8.6, L_PER_GAL = 3.78541, KG_PER_L = 1.032, KG_PER_LB = 0.45359237;

  function fmt(n, d) {
    if (!isFinite(n)) return '—';
    return Number(n.toFixed(d === undefined ? 1 : d)).toLocaleString(undefined, { maximumFractionDigits: d === undefined ? 1 : d });
  }
  function num(el, fallback) { var v = parseFloat(el && el.value); return isFinite(v) ? v : (fallback || 0); }
  function on(els, fn) { (Array.isArray(els) ? els : [els]).forEach(function (el) { if (el) { el.addEventListener('input', fn); el.addEventListener('change', fn); } }); }
  function goatIcon() {
    return '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 4c-1 2-1 4 0 5"/><path d="M17 4c1 2 1 4 0 5"/><path d="M7 9c0 4 2 7 5 9 3-2 5-5 5-9a5 5 0 0 0-10 0z"/><path d="M12 18v3"/></svg>';
  }

  // ---- Lactation model -----------------------------------------------------
  // Wood's curve y = a * t^b * e^(-c t), scaled so 305 days sum to the breed total.
  var BREEDS = {
    saanen: { name: 'Saanen', total: 2700 }, alpine: { name: 'Alpine', total: 2450 },
    toggenburg: { name: 'Toggenburg', total: 2250 }, lamancha: { name: 'LaMancha', total: 2200 },
    oberhasli: { name: 'Oberhasli', total: 2150 }, nubian: { name: 'Nubian', total: 1900 },
    mini: { name: 'Mini dairy', total: 1200 }, nigerian: { name: 'Nigerian Dwarf', total: 780 }
  };
  var WB = 0.25, WC = 0.0045, SHAPE_SUM = 0;
  function shape(t) { return Math.pow(t, WB) * Math.exp(-WC * t); }
  for (var d = 1; d <= 305; d++) SHAPE_SUM += shape(d);
  function curve(total, factor) {
    var a = total * factor / SHAPE_SUM;
    return function (t) { return a * shape(Math.max(1, t)); };
  }

  // ---- Homepage quick milk widget -------------------------------------------
  var qm = $('[data-tool="quick-milk"]');
  if (qm) (function () {
    var breed = 'saanen';
    var month = $('#qm-month', qm), out = $('#qm-month-out', qm);
    var pail = $('.pail-viz', qm);
    function render() {
      var f = curve(BREEDS[breed].total, 1);
      var day = Math.round(num(month) * 30.4 - 15);
      var lb = f(day);
      out.textContent = month.value;
      $('#qm-milking', qm).innerHTML = fmt(lb / 2) + ' lb<small>≈ ' + fmt(lb / 2 / LB_PER_GAL * 16, 1) + ' cups</small>';
      $('#qm-day', qm).innerHTML = fmt(lb) + ' lb<small>≈ ' + fmt(lb / LB_PER_GAL, 2) + ' gal / ' + fmt(lb * KG_PER_LB / KG_PER_L) + ' L</small>';
      $('#qm-season', qm).innerHTML = fmt(BREEDS[breed].total, 0) + ' lb<small>≈ ' + fmt(BREEDS[breed].total / LB_PER_GAL, 0) + ' gallons</small>';
      pail.style.setProperty('--fill', Math.min(92, 12 + lb / 13 * 80) + '%');
    }
    $$('[data-breed]', qm).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('[data-breed]', qm).forEach(function (x) { x.classList.remove('is-on'); x.setAttribute('aria-checked', 'false'); });
        b.classList.add('is-on'); b.setAttribute('aria-checked', 'true');
        breed = b.getAttribute('data-breed');
        render();
      });
    });
    on(month, render);
    render();
  })();

  // ---- Milk yield calculator --------------------------------------------------
  var my = $('[data-tool="goat-milk-yield-calculator"]');
  if (my) (function () {
    var daily = $('#my-daily'), unit = $('#my-unit'), share = $('#my-share'), shareOut = $('#my-share-out');
    var milkings = 2;
    function toL(v, u) { return u === 'gallons' ? v * L_PER_GAL : u === 'pounds' ? v * KG_PER_LB / KG_PER_L : v; }
    function label(v, u) { return u === 'gallons' ? fmt(v, 2) + ' gal' : u === 'pounds' ? fmt(v, 1) + ' lb' : fmt(v, 2) + ' L'; }
    function render() {
      var d = num(daily), u = unit.value, s = num(share) / 100;
      shareOut.textContent = Math.round(s * 100) + '%';
      if (d <= 0) { $('#my-per').textContent = 'Enter a daily yield'; return; }
      var kept = d * (1 - s), per = kept / milkings;
      $('#my-per').textContent = label(per, u);
      $('#my-cups').textContent = 'per milking · about ' + fmt(toL(per, u) * 4.22675, 1) + ' US cups';
      $('#my-kept').textContent = label(kept, u);
      $('#my-kids').textContent = label(d * s, u);
      $('#my-week').textContent = label(kept * 7, u);
      var html = '';
      var names = ['AM', 'PM', 'Midday'];
      for (var i = 0; i < milkings; i++) html += '<span style="--w:' + (1 - s) / milkings + '">' + (milkings === 1 ? 'Milking' : names[i] || '#' + (i + 1)) + '</span>';
      if (s > 0) html += '<span class="kid" style="--w:' + s + '">Kids</span>';
      $('#my-split').innerHTML = html;
    }
    $$('.seg button', my).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.seg button', my).forEach(function (x) { x.classList.remove('is-on'); x.setAttribute('aria-checked', 'false'); });
        b.classList.add('is-on'); b.setAttribute('aria-checked', 'true');
        milkings = parseInt(b.getAttribute('data-v'), 10);
        render();
      });
    });
    on([daily, unit, share], render);
    render();
  })();

  // ---- Production estimator with lactation chart -----------------------------
  var pe = $('[data-tool="goat-milk-production-estimator"]');
  if (pe) (function () {
    var breedEl = $('#pe-breed'), ageEl = $('#pe-age'), dimEl = $('#pe-dim'), todayEl = $('#pe-today');
    var svg = $('#pe-chart'), tip = $('#pe-tip'), note = $('#pe-note');
    var W = 720, H = 300, L = 46, R = 18, T = 22, B = 34, NS = 'http://www.w3.org/2000/svg';
    var state = {};
    function el(name, attrs, parent) {
      var n = document.createElementNS(NS, name);
      for (var k in attrs) n.setAttribute(k, attrs[k]);
      if (parent) parent.appendChild(n);
      return n;
    }
    function render() {
      var b = BREEDS[breedEl.value], factor = num(ageEl, 1);
      var f = curve(b.total, factor);
      var dim = Math.round(num(dimEl)), today = num(todayEl), calibrated = false;
      if (dim > 0 && today > 0) {
        var scale = today / f(dim);
        var base = f;
        f = function (t) { return base(t) * scale; };
        calibrated = true;
      }
      var days = Math.max(305, calibrated ? Math.min(600, dim + 20) : 305);
      var pts = [], max = 0, peakDay = 1, sum = 0;
      for (var t = 1; t <= days; t++) {
        var y = f(t);
        pts.push(y);
        if (y > max) { max = y; peakDay = t; }
        if (t <= 305) sum += y;
      }
      state = { f: f, days: days, pts: pts };
      var step = max > 6 ? 1 : max > 3 ? 0.5 : 0.25, yMax = Math.ceil(max * 1.15 / (4 * step)) * 4 * step;
      var x = function (t) { return L + (t - 1) / (days - 1) * (W - L - R); };
      var y = function (v) { return H - B - v / yMax * (H - T - B); };
      state.x = x; state.y = y;
      svg.innerHTML = '';
      var defs = el('defs', {}, svg);
      var g = el('linearGradient', { id: 'peGrad', x1: 0, x2: 0, y1: 0, y2: 1 }, defs);
      el('stop', { offset: '0', 'stop-color': '#C89A3B', 'stop-opacity': '.45' }, g);
      el('stop', { offset: '1', 'stop-color': '#C89A3B', 'stop-opacity': '0' }, g);
      var grid = el('g', { class: 'grid' }, svg), axis = el('g', { class: 'axis' }, svg);
      for (var i = 0; i <= 4; i++) {
        var v = yMax / 4 * i, yy = y(v);
        el('line', { x1: L, x2: W - R, y1: yy, y2: yy }, grid);
        el('text', { x: L - 8, y: yy + 4, 'text-anchor': 'end' }, axis).textContent = fmt(v, 1);
      }
      for (var m = 0; m * 30.4 <= days; m += (days > 400 ? 2 : 1)) {
        var xx = x(Math.max(1, m * 30.4));
        el('text', { x: xx, y: H - 12, 'text-anchor': 'middle' }, axis).textContent = m === 0 ? 'Kid' : 'M' + m;
      }
      el('text', { x: 6, y: 14 }, axis).textContent = 'lb/day';
      var d = '';
      pts.forEach(function (v, i2) { d += (i2 ? 'L' : 'M') + x(i2 + 1).toFixed(1) + ',' + y(v).toFixed(1); });
      el('path', { class: 'area', d: d + 'L' + x(days) + ',' + y(0) + 'L' + x(1) + ',' + y(0) + 'Z' }, svg);
      var line = el('path', { class: 'line', d: d }, svg);
      line.style.setProperty('--len', Math.ceil(line.getTotalLength()));
      var pk = el('g', { class: 'peak' }, svg);
      el('circle', { cx: x(peakDay), cy: y(max), r: 7 }, pk);
      el('text', { x: x(peakDay) + 12, y: y(max) - 10 }, pk).textContent = 'Peak ' + fmt(max) + ' lb · day ' + peakDay;
      if (calibrated) {
        var you = el('g', { class: 'you' }, svg);
        el('circle', { cx: x(dim), cy: y(today), r: 7 }, you);
      }
      state.hover = el('line', { class: 'hover-line', x1: 0, x2: 0, y1: T, y2: H - B, visibility: 'hidden' }, svg);
      $('#pe-peak').textContent = fmt(max) + ' lb/day';
      $('#pe-avg').textContent = fmt(sum / 305) + ' lb (' + fmt(sum / 305 / LB_PER_GAL, 2) + ' gal)';
      $('#pe-season').textContent = fmt(sum, 0) + ' lb (' + fmt(sum / LB_PER_GAL, 0) + ' gal)';
      $('#pe-week').textContent = fmt(sum / 305 * 7, 0) + ' lb';
      note.textContent = calibrated
        ? 'Curve calibrated to your doe: ' + fmt(today) + ' lb on day ' + dim + ' of her lactation (green dot).'
        : 'Typical ' + b.name + ' curve for a healthy doe milked twice daily. Add today\'s numbers to calibrate it to your doe.';
    }
    svg.addEventListener('pointermove', function (e) {
      if (!state.f) return;
      var r = svg.getBoundingClientRect();
      var px = (e.clientX - r.left) / r.width * W;
      var t = Math.round(1 + (px - L) / (W - L - R) * (state.days - 1));
      if (t < 1 || t > state.days) { tip.hidden = true; state.hover.setAttribute('visibility', 'hidden'); return; }
      var v = state.pts[t - 1];
      state.hover.setAttribute('x1', state.x(t)); state.hover.setAttribute('x2', state.x(t));
      state.hover.setAttribute('visibility', 'visible');
      tip.hidden = false;
      tip.style.left = (state.x(t) / W * 100) + '%';
      tip.style.top = (state.y(v) / H * 100) + '%';
      tip.textContent = 'Day ' + t + ': ' + fmt(v) + ' lb (' + fmt(v / LB_PER_GAL, 2) + ' gal)';
    });
    svg.addEventListener('pointerleave', function () { tip.hidden = true; if (state.hover) state.hover.setAttribute('visibility', 'hidden'); });
    on([breedEl, ageEl, dimEl, todayEl], render);
    render();
  })();

  // ---- Cheese herd calculator (same maths as the original post tool) ---------
  var ch = $('[data-tool="goat-cheese-herd-calculator"]');
  if (ch) (function () {
    var ids = ['amount', 'unit', 'type', 'yield', 'days', 'kids'], f = {};
    ids.forEach(function (k) { f[k] = $('#ch-' + k); });
    function render() {
      var amt = num(f.amount);
      if (amt <= 0) { $('#ch-goats').textContent = 'Enter an amount'; return; }
      var lb = f.unit.value === 'ounces' ? amt / 16 : f.unit.value === 'kilograms' ? amt * 2.20462 : amt;
      var galPerLb = num(f.type), daily = num(f.yield), days = num(f.days), kids = num(f.kids);
      var need = lb * galPerLb, perGoat = daily * days * (1 - kids);
      var exact = need / perGoat, goats = Math.max(1, Math.ceil(exact));
      $('#ch-goats').textContent = goats + (goats === 1 ? ' goat' : ' goats');
      var icons = '';
      for (var i = 0; i < Math.min(goats, 30); i++) icons += '<span style="animation-delay:' + (i * 0.05) + 's">' + goatIcon() + '</span>';
      $('#ch-icons').innerHTML = icons + (goats > 30 ? '<span>+' + (goats - 30) + '</span>' : '');
      $('#ch-detail').textContent = 'Assumes about ' + fmt(galPerLb, 1) + ' gallon' + (galPerLb === 1 ? '' : 's') + ' of milk per finished pound and a ' + days + '-day collection window.' + (exact < 1 ? ' One goat may produce more than enough for this batch.' : '');
      $('#ch-milk').textContent = fmt(need) + ' gal';
      $('#ch-pergoat').textContent = fmt(perGoat) + ' gal';
      $('#ch-cups').textContent = fmt(need * 16, 0) + ' cups';
    }
    on(ids.map(function (k) { return f[k]; }), render);
    render();
  })();

  // ---- Gestation & kidding timeline -------------------------------------------
  var ge = $('[data-tool="goat-gestation-calculator"]');
  if (ge) (function () {
    var dateEl = $('#ge-date'), breedEl = $('#ge-breed'), nameEl = $('#ge-name'), events = [];
    var t0 = new Date(); t0.setHours(12, 0, 0, 0);
    var def = new Date(t0); def.setDate(def.getDate() - 60);
    dateEl.value = iso(def);
    function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
    function add(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
    function nice(d) { return d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); }
    function render() {
      if (!dateEl.value) return;
      var p = dateEl.value.split('-');
      var bred = new Date(+p[0], p[1] - 1, +p[2], 12);
      var gest = parseInt(breedEl.value, 10);
      var due = add(bred, gest), who = nameEl.value.trim() || 'your doe';
      events = [
        [0, 'Bred', 'Note the buck and date in your herd records.'],
        [21, 'Watch for a return to heat', 'If ' + who + ' comes back into heat around days 18–24, she probably did not settle.'],
        [30, 'Pregnancy blood test possible', 'A blood test can confirm pregnancy from about 30 days after breeding.'],
        [45, 'Ultrasound window opens', 'Ultrasound can usually confirm pregnancy and count kids from about day 45.'],
        [gest - 60, 'Dry off', 'Stop milking about 60 days before kidding so the udder can rest and rebuild.'],
        [gest - 50, 'Increase nutrition', 'Most fetal growth happens in the last 6–8 weeks. Improve forage and adjust grain gradually.'],
        [gest - 30, 'CDT booster', 'A booster about a month before kidding raises antibodies in the colostrum. Follow your vet\'s protocol.'],
        [gest - 10, 'Prep the kidding pen & kit', 'Clean, dry pen; towels, iodine, gloves, bulb syringe, frozen colostrum and your vet\'s number.'],
        [gest - 5, 'Kidding window opens', 'Watch for a full, tight udder, loose tail ligaments and restlessness.'],
        [gest, 'Estimated kidding date', 'The average goat gestation is about 150 days.'],
        [gest + 5, 'Kidding window closes', 'If she has not kidded and shows no signs, check in with your vet.']
      ];
      $('#ge-due').textContent = nice(due);
      $('#ge-window').textContent = 'Normal window: ' + nice(add(bred, gest - 5)) + ' – ' + nice(add(bred, gest + 5));
      var left = Math.round((due - t0) / 864e5), passed = Math.round((t0 - bred) / 864e5);
      $('#ge-count').textContent = left >= 0 ? left : Math.abs(left);
      $('#ge-count-l').textContent = left > 0 ? 'days to go' : left === 0 ? 'due today!' : 'days since due date';
      var pct = Math.max(0, Math.min(100, passed / gest * 100));
      $('#ge-progress').style.width = pct + '%';
      var tm = $('#ge-today');
      tm.style.display = passed >= 0 && passed <= gest ? 'block' : 'none';
      tm.style.left = pct + '%';
      var nextFound = false, html = '';
      events.forEach(function (ev, i) {
        var dt = add(bred, ev[0]), past = dt < t0, cls = '';
        if (past) cls = 'is-past'; else if (!nextFound) { cls = 'is-next'; nextFound = true; }
        html += '<li class="' + cls + '" style="animation-delay:' + i * 0.04 + 's"><span class="tl-date">' + nice(dt) + '<span class="tl-day">Day ' + ev[0] + '</span></span><div><strong>' + ev[1] + '</strong><p>' + ev[2] + '</p></div></li>';
      });
      $('#ge-timeline').innerHTML = html;
      ge._bred = bred; ge._who = who;
    }
    $('#ge-ics').addEventListener('click', function () {
      if (!ge._bred) return;
      var lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Pure Goat Farms//Kidding Calculator//EN', 'CALSCALE:GREGORIAN'];
      events.forEach(function (ev, i) {
        var d1 = add(ge._bred, ev[0]), d2 = add(d1, 1);
        var f = function (d) { return iso(d).replace(/-/g, ''); };
        lines.push('BEGIN:VEVENT', 'UID:pgf-' + f(ge._bred) + '-' + i + '@puregoatfarms.com', 'DTSTAMP:' + f(new Date()) + 'T000000Z',
          'DTSTART;VALUE=DATE:' + f(d1), 'DTEND;VALUE=DATE:' + f(d2),
          'SUMMARY:' + (ge._who === 'your doe' ? '' : ge._who + ': ') + ev[1], 'DESCRIPTION:' + ev[2].replace(/,/g, '\\,'), 'END:VEVENT');
      });
      lines.push('END:VCALENDAR');
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([lines.join('\r\n')], { type: 'text/calendar' }));
      a.download = 'kidding-timeline.ics';
      document.body.appendChild(a); a.click(); a.remove();
    });
    on([dateEl, breedEl, nameEl], render);
    render();
  })();

  // ---- Feed & hay calculator --------------------------------------------------
  var fd = $('[data-tool="goat-feed-calculator"]');
  if (fd) (function () {
    var inputs = $$('input', fd);
    function v(id) { return Math.max(0, num($('#' + id))); }
    function render() {
      var mN = v('fd-m-n'), mW = v('fd-m-w'), milk = v('fd-m-milk'), dN = v('fd-d-n'), dW = v('fd-d-w'), bN = v('fd-b-n'), bW = v('fd-b-w');
      var hay = mN * mW * 0.035 + dN * dW * 0.025 + bN * bW * 0.025;
      var grain = mN * milk / 3;
      var water = (mN * mW + dN * dW + bN * bW) / 100 + mN * milk / LB_PER_GAL * 1.5;
      var month = 30.4, bale = v('fd-bale') || 50;
      var bales = hay * month / bale;
      $('#fd-hay').textContent = fmt(hay) + ' lb';
      $('#fd-hay-m').textContent = fmt(hay * month, 0) + ' lb/month · ≈ ' + fmt(bales, 1) + ' bales';
      $('#fd-grain').textContent = fmt(grain) + ' lb';
      $('#fd-grain-m').textContent = fmt(grain * month, 0) + ' lb/month · ≈ ' + fmt(grain * month / 50, 1) + ' bags';
      $('#fd-water').textContent = fmt(water) + ' gal';
      var cost = bales * v('fd-bale-p') + grain * month / 50 * v('fd-bag-p');
      var goats = mN + dN + bN;
      $('#fd-cost').textContent = '$' + fmt(cost, 0);
      $('#fd-cost-s').textContent = goats ? '≈ $' + fmt(cost / goats, 0) + ' per goat per month' : 'Add some goats';
    }
    on(inputs, render);
    render();
  })();

  // ---- Breed finder quiz ------------------------------------------------------
  var bf = $('[data-tool="dairy-goat-breed-finder"]');
  if (bf) (function () {
    var T = {
      saanen:     { n: 'Saanen', url: '/best-dairy-goat-breeds-for-milk/#saanen-the-volume-champion', d: 'The volume champion — about a gallon a day of mild milk, with a calm temperament.', vol: 5, fat: 1, small: 1, heat: 2, cold: 4, quiet: 5, easy: 4 },
      alpine:     { n: 'Alpine', url: '/best-dairy-goat-breeds-for-milk/#alpine-reliable-and-hardy', d: 'Hardy, high-producing and famously persistent through the lactation.', vol: 5, fat: 2, small: 1, heat: 3, cold: 5, quiet: 3, easy: 3 },
      toggenburg: { n: 'Toggenburg', url: '/best-dairy-goat-breeds-for-milk/#toggenburg-the-original-swiss-dairy-goat', d: 'A classic Swiss dairy goat that milks well in cold climates.', vol: 4, fat: 1, small: 2, heat: 2, cold: 5, quiet: 3, easy: 2 },
      lamancha:   { n: 'LaMancha', url: '/best-dairy-goat-breeds-for-milk/#lamancha-the-easy-going-all-rounder', d: 'Calm, quiet and productive — the easy-going all-rounder.', vol: 4, fat: 3, small: 1, heat: 4, cold: 3, quiet: 5, easy: 5 },
      oberhasli:  { n: 'Oberhasli', url: '/best-dairy-goat-breeds-for-milk/#oberhasli-quiet-and-efficient', d: 'Gentle, quiet and efficient, with sweet, mild milk.', vol: 4, fat: 3, small: 2, heat: 3, cold: 4, quiet: 4, easy: 4 },
      nubian:     { n: 'Nubian', url: '/best-dairy-goat-breeds-for-milk/#nubian-rich-sweet-and-vocal', d: 'Rich, sweet, high-butterfat milk and great heat tolerance — but vocal.', vol: 3, fat: 4, small: 1, heat: 5, cold: 2, quiet: 1, easy: 3 },
      nigerian:   { n: 'Nigerian Dwarf', url: '/best-dairy-goat-breeds-for-milk/#nigerian-dwarf-small-goat-rich-milk', d: 'Small, friendly and the richest milk of any dairy breed.', vol: 1, fat: 5, small: 5, heat: 4, cold: 3, quiet: 3, easy: 5 },
      mini:       { n: 'Mini dairy cross', url: '/best-dairy-goat-breeds-for-milk/#what-about-mini-dairy-goats-and-crosses', d: 'Nigerian crossed with a standard breed: more milk than a Nigerian in a smaller frame.', vol: 2, fat: 4, small: 4, heat: 3, cold: 3, quiet: 3, easy: 4 }
    };
    var form = $('#bf-quiz'), steps = $$('.quiz__q', form), back = $('#bf-back'), bar = $('#bf-bar');
    var cur = 0;
    function show(i) {
      cur = i;
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      back.hidden = i === 0;
      bar.style.width = (i / steps.length * 100) + '%';
      var first = $('input', steps[i]); if (first && i) first.focus({ preventScroll: true });
    }
    function score(a) {
      return Object.keys(T).map(function (k) {
        var b = T[k], s = 0;
        s += a.goal === 'volume' ? b.vol * 3 : a.goal === 'rich' ? b.fat * 3 : (b.vol + b.fat) * 1.5;
        s += a.space === 'small' ? b.small * 3 : a.space === 'medium' ? b.small + 4 : b.vol + (5 - b.small) * 0.5;
        s += a.climate === 'hot' ? b.heat * 2 : a.climate === 'cold' ? b.cold * 2 : 6;
        s += a.noise === 'quiet' ? b.quiet * 2 : 6;
        s += a.experience === 'new' ? b.easy * 2 : b.easy * 0.5 + 5;
        return { k: k, s: s };
      }).sort(function (x, y) { return y.s - x.s; });
    }
    function finish() {
      var a = {};
      new FormData(form).forEach(function (v, k) { a[k] = v; });
      var res = score(a), top = res[0].s;
      bar.style.width = '100%';
      $('#bf-list').innerHTML = res.slice(0, 3).map(function (r, i) {
        var b = T[r.k], pct = Math.round(r.s / top * (97 - i * 2));
        return '<li style="animation-delay:' + i * 0.12 + 's"><span class="match-ring" style="--pct:' + pct + '"><b>' + pct + '%</b></span><div><h3>' + b.n + '</h3><p>' + b.d + ' <a href="' + b.url + '">Read more</a></p></div></li>';
      }).join('');
      form.hidden = true;
      $('#bf-result').hidden = false;
    }
    form.addEventListener('change', function (e) {
      if (e.target.type !== 'radio') return;
      setTimeout(function () { if (cur < steps.length - 1) show(cur + 1); else finish(); }, 220);
    });
    back.addEventListener('click', function () { if (cur > 0) show(cur - 1); });
    $('#bf-restart').addEventListener('click', function () {
      form.reset(); form.hidden = false; $('#bf-result').hidden = true; show(0);
    });
    show(0);
  })();

  // ---- Milk unit converter ----------------------------------------------------
  var cv = $('[data-tool="goat-milk-converter"]');
  if (cv) (function () {
    var U = {
      lb: ['Pounds', function (v) { return v * KG_PER_LB / KG_PER_L; }, 2],
      kg: ['Kilograms', function (v) { return v / KG_PER_L; }, 2],
      oz: ['Ounces (weight)', function (v) { return v / 16 * KG_PER_LB / KG_PER_L; }, 1],
      gal: ['US gallons', function (v) { return v * L_PER_GAL; }, 3],
      qt: ['US quarts', function (v) { return v * 0.946353; }, 2],
      pt: ['US pints', function (v) { return v * 0.473176; }, 2],
      cup: ['US cups', function (v) { return v * 0.236588; }, 1],
      l: ['Liters', function (v) { return v; }, 2],
      ml: ['Milliliters', function (v) { return v / 1000; }, 0]
    };
    var val = $('#cv-val'), unit = $('#cv-unit');
    function render() {
      var liters = U[unit.value][1](Math.max(0, num(val)));
      $('#cv-out').innerHTML = Object.keys(U).map(function (k) {
        var per = U[k][1](1), out = liters / per;
        return '<div class="conv__cell' + (k === unit.value ? ' is-from' : '') + '"><strong>' + fmt(out, U[k][2]) + '</strong><span>' + U[k][0] + '</span></div>';
      }).join('');
    }
    on([val, unit], render);
    render();
  })();
})();
