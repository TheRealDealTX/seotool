/* thesublet.com — interactive tools (all client-side) */
(function () {
  'use strict';
  var d = document;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var money = function (n) { return '$' + (Math.round(n * 100) / 100).toLocaleString('en-US', { minimumFractionDigits: n % 1 ? 2 : 0, maximumFractionDigits: 2 }); };
  var num = function (f, n) { var v = parseFloat((f.elements[n] || {}).value); return isFinite(v) ? v : 0; };
  var store = {
    get: function (k, def) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch (e) { return def; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var iso = function (dt) { return dt.getFullYear() + '-' + String(dt.getMonth() + 1).padStart(2, '0') + '-' + String(dt.getDate()).padStart(2, '0'); };
  var parse = function (s) { var p = (s || '').split('-'); return p.length === 3 ? new Date(+p[0], +p[1] - 1, +p[2]) : null; };
  var dim = function (y, m) { return new Date(y, m + 1, 0).getDate(); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  function dayRate(rent, method, y, m) {
    if (method === '30') return rent / 30;
    if (method === '365') return rent * 12 / 365;
    return rent / dim(y, m);
  }
  /** Rent for an inclusive date range, month by month. Returns {total, months:[{label, days, full, amount}]} */
  function rentForRange(rent, start, end, method) {
    var out = { total: 0, months: [] };
    if (!start || !end || end < start) return out;
    var cur = new Date(start.getFullYear(), start.getMonth(), 1);
    while (cur <= end) {
      var y = cur.getFullYear(), m = cur.getMonth(), days = dim(y, m);
      var first = (y === start.getFullYear() && m === start.getMonth()) ? start.getDate() : 1;
      var last = (y === end.getFullYear() && m === end.getMonth()) ? end.getDate() : days;
      var occ = last - first + 1, full = occ === days;
      var amt = full ? rent : dayRate(rent, method, y, m) * occ;
      out.months.push({ label: cur.toLocaleString('en-US', { month: 'short', year: 'numeric' }), days: occ, full: full, amount: amt });
      out.total += amt;
      cur = new Date(y, m + 1, 1);
    }
    return out;
  }

  /* ---------- cost calculator ---------- */
  var cost = $('[data-calc=cost]');
  if (cost) {
    var today = new Date(), s0 = new Date(today.getFullYear(), today.getMonth() + 1, 15), e0 = new Date(s0.getFullYear(), s0.getMonth() + 3, 14);
    cost.elements.start.value = iso(s0); cost.elements.end.value = iso(e0);
    var runCost = function () {
      var rent = num(cost, 'rent'), s = parse(cost.elements.start.value), e = parse(cost.elements.end.value), method = cost.elements.method.value;
      var out = $('[data-out=cost]');
      if (!s || !e || e < s) { out.innerHTML = '<p class="err">Choose a move-out date after the move-in date.</p>'; return; }
      var r = rentForRange(rent, s, e, method);
      var nMonths = r.months.length, totalDays = Math.round((e - s) / 864e5) + 1;
      var monthsEq = totalDays / 30.4375;
      var util = num(cost, 'util') * monthsEq, other = num(cost, 'other') * monthsEq, fees = num(cost, 'fees'), dep = num(cost, 'deposit');
      var first = r.months[0] ? r.months[0].amount : 0;
      var upfront = first + dep + fees;
      var total = r.total + util + other + fees + (cost.elements.refund.checked ? 0 : dep);
      out.innerHTML = '<div class="out-grid">'
        + '<div class="out-box hi"><strong>' + money(upfront) + '</strong><span>Upfront (first month + deposit + fees)</span></div>'
        + '<div class="out-box"><strong>' + money(total) + '</strong><span>Total cost of the stay' + (cost.elements.refund.checked ? ' (deposit returned)' : '') + '</span></div>'
        + '<div class="out-box"><strong>' + money(total / monthsEq) + '</strong><span>Effective cost per month</span></div>'
        + '<div class="out-box"><strong>' + totalDays + ' days</strong><span>≈ ' + monthsEq.toFixed(1) + ' months across ' + nMonths + ' calendar months</span></div></div>'
        + '<div class="table-scroll"><table class="tbl" style="margin-top:12px"><tr><th>Month</th><th>Days</th><th>Rent</th></tr>'
        + r.months.map(function (m) { return '<tr><td>' + m.label + '</td><td>' + m.days + (m.full ? ' (full)' : ' (prorated)') + '</td><td>' + money(m.amount) + '</td></tr>'; }).join('')
        + '<tr><th>Rent subtotal</th><th></th><th>' + money(r.total) + '</th></tr></table></div>';
    };
    cost.addEventListener('input', runCost); cost.addEventListener('change', runCost); runCost();
  }

  /* ---------- sublet vs lease vs hotel ---------- */
  var cmpF = $('[data-calc=compare]');
  if (cmpF) {
    var runCmp = function () {
      var mo = Math.max(1, num(cmpF, 'months'));
      var sub = (num(cmpF, 's_rent') + num(cmpF, 's_util')) * mo + num(cmpF, 's_fees');
      var lease = (num(cmpF, 'l_rent') + num(cmpF, 'l_util') + num(cmpF, 'l_furn')) * mo + num(cmpF, 'l_fees');
      var nights = Math.round(mo * 30.4375);
      var hotel = num(cmpF, 'h_rate') * nights * (1 + num(cmpF, 'h_tax') / 100) + num(cmpF, 'h_food') * mo;
      var rows = [['Sublet', sub, ''], ['Short-term lease', lease, 'b2'], ['Extended-stay hotel', hotel, 'b3']];
      var max = Math.max(sub, lease, hotel) || 1, min = Math.min(sub, lease, hotel);
      $('[data-out=compare]').innerHTML = '<h3>Total for ' + mo + ' month' + (mo > 1 ? 's' : '') + '</h3>'
        + rows.map(function (r) { return '<div class="bar-row"><span>' + r[0] + (r[1] === min ? ' ✓' : '') + '</span><div class="bar ' + r[2] + '" style="width:' + Math.max(4, r[1] / max * 100) + '%"></div><strong>' + money(Math.round(r[1])) + '</strong></div>'; }).join('')
        + '<p class="small muted">Per month: sublet ' + money(Math.round(sub / mo)) + ' · lease ' + money(Math.round(lease / mo)) + ' · hotel ' + money(Math.round(hotel / mo)) + ' (' + nights + ' nights). Placeholder defaults — enter real quotes.</p>';
    };
    cmpF.addEventListener('input', runCmp); runCmp();
  }

  /* ---------- proration ---------- */
  var pro = $('[data-calc=proration]');
  if (pro) {
    var t = new Date(); pro.elements.date.value = iso(new Date(t.getFullYear(), t.getMonth(), Math.min(t.getDate(), 28)));
    var runPro = function () {
      var rent = num(pro, 'rent'), dt = parse(pro.elements.date.value), out = $('[data-out=proration]');
      if (!dt) { out.innerHTML = ''; return; }
      var y = dt.getFullYear(), m = dt.getMonth(), days = dim(y, m);
      var occ = pro.elements.kind.value === 'in' ? days - dt.getDate() + 1 : dt.getDate();
      var a = rent / days * occ, b = rent / 30 * Math.min(occ, 30), c = rent * 12 / 365 * occ;
      out.innerHTML = '<p>You occupy <strong>' + occ + ' of ' + days + ' days</strong> in ' + dt.toLocaleString('en-US', { month: 'long', year: 'numeric' }) + '.</p><div class="out-grid">'
        + '<div class="out-box hi"><strong>' + money(Math.round(a * 100) / 100) + '</strong><span>Actual days (' + money(Math.round(rent / days * 100) / 100) + '/day)</span></div>'
        + '<div class="out-box"><strong>' + money(Math.round(b * 100) / 100) + '</strong><span>30-day month (' + money(Math.round(rent / 30 * 100) / 100) + '/day)</span></div>'
        + '<div class="out-box"><strong>' + money(Math.round(c * 100) / 100) + '</strong><span>365-day year (' + money(Math.round(rent * 12 / 365 * 100) / 100) + '/day)</span></div></div>';
    };
    pro.addEventListener('input', runPro); pro.addEventListener('change', runPro); runPro();
  }

  /* ---------- packing checklist ---------- */
  var cl = $('[data-checklist]');
  if (cl) {
    var base = {
      'Documents & money': ['Photo ID / passport', 'Signed sublease (printed or saved)', 'Host contact & address', 'Health insurance card', 'Debit/credit cards', 'Offer letter / contract (interns & nurses)', 'Nursing license & certifications', 'Car registration & insurance'],
      'Bedroom & bath': ['One set of sheets (check if provided)', 'Pillowcase or travel pillow', 'Towel & washcloth', 'Shower shoes', 'Toiletries & medications', 'Hair dryer (if not provided)', 'Small first-aid kit', 'Earplugs & sleep mask'],
      'Clothes': ['Work outfits / scrubs', 'Everyday clothes for 7–10 days', 'Layers for the local season', 'Rain jacket / umbrella', 'Comfortable walking shoes', 'Workout clothes', 'Laundry bag & detergent pods'],
      'Tech & work': ['Laptop & charger', 'Phone charger (long cable)', 'Power strip / extension cord', 'Headphones', 'Portable battery', 'Universal adapter for older outlets'],
      'Kitchen & home': ['Reusable water bottle', 'Coffee setup you love', 'Food storage containers', 'Basic spices (small)', 'Dish sponge', 'Command hooks (renter-friendly)', 'Hangers'],
      'Move-in day': ['Phone photos of every room (condition)', 'Meter readings photo', 'Spare key plan', 'Snacks & water', 'Cleaning wipes', 'Small toolkit / screwdriver']
    };
    var st = store.get('ts_pack', { checked: {}, custom: [] });
    var gWrap = $('[data-cl-groups]', cl);
    var draw = function () {
      var groups = JSON.parse(JSON.stringify(base));
      if (st.custom.length) groups['My items'] = st.custom.slice();
      var total = 0, done = 0;
      gWrap.innerHTML = Object.keys(groups).map(function (g) {
        return '<div class="cl-group"><h3>' + esc(g) + '</h3>' + groups[g].map(function (it) {
          var k = g + '::' + it, on = !!st.checked[k]; total++; if (on) done++;
          return '<label class="' + (on ? 'done' : '') + '"><input type="checkbox" data-k="' + esc(k) + '"' + (on ? ' checked' : '') + '><span>' + esc(it) + '</span>'
            + (g === 'My items' ? ' <button type="button" class="btn btn-sm btn-ghost" data-rm="' + esc(it) + '" aria-label="Remove">×</button>' : '') + '</label>';
        }).join('') + '</div>';
      }).join('');
      $('[data-cl-progress]', cl).textContent = done + ' of ' + total + ' packed';
    };
    gWrap.addEventListener('change', function (e) { var k = e.target.getAttribute('data-k'); if (!k) return; if (e.target.checked) st.checked[k] = 1; else delete st.checked[k]; store.set('ts_pack', st); draw(); });
    gWrap.addEventListener('click', function (e) { var r = e.target.getAttribute('data-rm'); if (r == null) return; e.preventDefault(); st.custom = st.custom.filter(function (x) { return x !== r; }); delete st.checked['My items::' + r]; store.set('ts_pack', st); draw(); });
    $('[data-cl-add]', cl).addEventListener('submit', function (e) { e.preventDefault(); var v = this.elements.item.value.trim(); if (v && st.custom.indexOf(v) < 0) { st.custom.push(v.slice(0, 80)); store.set('ts_pack', st); } this.reset(); draw(); });
    $('[data-cl-reset]', cl).addEventListener('click', function () { if (confirm('Clear all ticks and custom items?')) { st = { checked: {}, custom: [] }; store.set('ts_pack', st); draw(); } });
    $('[data-cl-print]', cl).addEventListener('click', function () { window.print(); });
    draw();
  }

  /* ---------- room planner ---------- */
  var pl = $('[data-planner]');
  if (pl) {
    var svg = $('[data-pl-svg]', pl), NS = 'http://www.w3.org/2000/svg', S = 40; // px per ft
    var ps = store.get('ts_room', { w: 12, l: 11, items: [] });
    var sel = -1, drag = null;
    pl.querySelector('[name=w]').value = ps.w; pl.querySelector('[name=l]').value = ps.l;
    var save = function () { store.set('ts_room', ps); };
    var colors = ['#cfe5d6', '#bfe0f2', '#ffe2b8', '#f6d0c4', '#e1d7f3', '#d9e8c4'];
    var drawRoom = function () {
      var W = ps.w * S, L = ps.l * S, pad = 20;
      svg.setAttribute('viewBox', (-pad) + ' ' + (-pad) + ' ' + (W + pad * 2) + ' ' + (L + pad * 2));
      var h = '<rect x="0" y="0" width="' + W + '" height="' + L + '" fill="#fbfcfb" stroke="#1d2a24" stroke-width="4"/>';
      for (var x = S; x < W; x += S) h += '<line x1="' + x + '" y1="0" x2="' + x + '" y2="' + L + '" stroke="#e3ebe6"/>';
      for (var y = S; y < L; y += S) h += '<line x1="0" y1="' + y + '" x2="' + W + '" y2="' + y + '" stroke="#e3ebe6"/>';
      ps.items.forEach(function (it, i) {
        var w = (it.r ? it.d : it.w) * S, dd = (it.r ? it.w : it.d) * S;
        h += '<g data-i="' + i + '" style="cursor:move"><rect x="' + it.x + '" y="' + it.y + '" width="' + w + '" height="' + dd + '" rx="4" fill="' + colors[i % colors.length] + '" stroke="' + (i === sel ? '#e46f4c' : '#2f6f4f') + '" stroke-width="' + (i === sel ? 4 : 2) + '"/>'
          + '<text x="' + (it.x + w / 2) + '" y="' + (it.y + dd / 2 + 5) + '" text-anchor="middle" font-size="14" font-family="system-ui" fill="#1d2a24" pointer-events="none">' + esc(it.n) + '</text></g>';
      });
      h += '<text x="' + (W / 2) + '" y="-6" text-anchor="middle" font-size="13" fill="#5b6b62">' + ps.w + ' ft</text>';
      h += '<text x="-8" y="' + (L / 2) + '" text-anchor="middle" font-size="13" fill="#5b6b62" transform="rotate(-90 -8 ' + (L / 2) + ')">' + ps.l + ' ft</text>';
      svg.innerHTML = h;
      var area = ps.items.reduce(function (a, it) { return a + (it.n === 'Rug' ? 0 : it.w * it.d); }, 0);
      $('[data-pl-info]', pl).textContent = 'Room ' + (ps.w * ps.l).toFixed(0) + ' sq ft · furniture covers ~' + area.toFixed(0) + ' sq ft (' + Math.round(area / (ps.w * ps.l) * 100) + '%). Drag to move; grid squares are 1 ft.';
    };
    var pt = function (e) { var p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); };
    svg.addEventListener('pointerdown', function (e) {
      var g = e.target.closest('g[data-i]');
      sel = g ? +g.getAttribute('data-i') : -1;
      if (g) { var p = pt(e), it = ps.items[sel]; drag = { dx: p.x - it.x, dy: p.y - it.y }; svg.setPointerCapture(e.pointerId); }
      drawRoom();
    });
    svg.addEventListener('pointermove', function (e) {
      if (!drag || sel < 0) return;
      var p = pt(e), it = ps.items[sel], w = (it.r ? it.d : it.w) * S, dd = (it.r ? it.w : it.d) * S;
      it.x = Math.max(0, Math.min(ps.w * S - w, Math.round((p.x - drag.dx) / (S / 4)) * (S / 4)));
      it.y = Math.max(0, Math.min(ps.l * S - dd, Math.round((p.y - drag.dy) / (S / 4)) * (S / 4)));
      drawRoom();
    });
    svg.addEventListener('pointerup', function () { if (drag) { drag = null; save(); } });
    pl.addEventListener('input', function (e) {
      if (e.target.name === 'w' || e.target.name === 'l') { var v = parseFloat(e.target.value); if (v >= 5 && v <= 40) { ps[e.target.name] = v; save(); drawRoom(); } }
    });
    pl.querySelector('[name=add]').addEventListener('change', function () {
      if (!this.value) return; var p = this.value.split('|');
      ps.items.push({ n: p[0], w: +p[1], d: +p[2], x: 0, y: 0, r: false }); sel = ps.items.length - 1; this.value = ''; save(); drawRoom();
    });
    $('[data-pl-rotate]', pl).addEventListener('click', function () { if (sel > -1) { var it = ps.items[sel]; it.r = !it.r; it.x = Math.min(it.x, Math.max(0, ps.w * S - (it.r ? it.d : it.w) * S)); it.y = Math.min(it.y, Math.max(0, ps.l * S - (it.r ? it.w : it.d) * S)); save(); drawRoom(); } });
    $('[data-pl-delete]', pl).addEventListener('click', function () { if (sel > -1) { ps.items.splice(sel, 1); sel = -1; save(); drawRoom(); } });
    $('[data-pl-reset]', pl).addEventListener('click', function () { if (confirm('Remove all furniture?')) { ps.items = []; sel = -1; save(); drawRoom(); } });
    drawRoom();
  }

  /* ---------- city quiz ---------- */
  var quiz = $('[data-quiz]');
  if (quiz) {
    // Broad, general tags only: cost 1 (lower) – 3 (higher); car-free 0–2; climate warm|mild|seasons; size big|mid|college
    var C = [
      ['New York', '/sublets/ny/new-york/', 3, 2, 'seasons', 'big', ['finance', 'tech', 'health', 'explore'], 'culture'],
      ['San Francisco', '/sublets/ca/san-francisco/', 3, 2, 'mild', 'big', ['tech'], 'outdoors'],
      ['Boston', '/sublets/ma/boston/', 3, 2, 'seasons', 'big', ['health', 'study', 'tech', 'finance'], 'culture'],
      ['Washington, DC', '/sublets/dc/washington/', 3, 2, 'seasons', 'big', ['gov', 'health'], 'culture'],
      ['Chicago', '/sublets/il/chicago/', 2, 2, 'seasons', 'big', ['finance', 'health', 'tech', 'explore'], 'culture'],
      ['Seattle', '/sublets/wa/seattle/', 3, 1, 'mild', 'big', ['tech', 'health'], 'outdoors'],
      ['Los Angeles', '/sublets/ca/los-angeles/', 3, 0, 'warm', 'big', ['finance', 'explore', 'health'], 'culture'],
      ['Philadelphia', '/sublets/pa/philadelphia/', 2, 2, 'seasons', 'big', ['health', 'study', 'finance'], 'culture'],
      ['Austin', '/sublets/tx/austin/', 2, 0, 'warm', 'mid', ['tech', 'study', 'explore'], 'culture'],
      ['Denver', '/sublets/co/denver/', 2, 1, 'seasons', 'mid', ['tech', 'health', 'explore'], 'outdoors'],
      ['Houston', '/sublets/tx/houston/', 1, 0, 'warm', 'big', ['health', 'finance'], 'culture'],
      ['Atlanta', '/sublets/ga/atlanta/', 2, 0, 'warm', 'big', ['health', 'finance', 'tech'], 'culture'],
      ['Miami', '/sublets/fl/miami/', 3, 0, 'warm', 'big', ['finance', 'explore', 'health'], 'outdoors'],
      ['Nashville', '/sublets/tn/nashville/', 2, 0, 'mild', 'mid', ['health', 'explore'], 'culture'],
      ['Minneapolis', '/sublets/mn/minneapolis/', 1, 1, 'seasons', 'mid', ['health', 'finance'], 'outdoors'],
      ['Pittsburgh', '/sublets/pa/pittsburgh/', 1, 1, 'seasons', 'mid', ['health', 'study', 'tech'], 'calm'],
      ['San Diego', '/sublets/ca/san-diego/', 3, 0, 'warm', 'big', ['health', 'tech', 'explore'], 'outdoors'],
      ['Portland', '/sublets/or/portland/', 2, 1, 'mild', 'mid', ['explore', 'health'], 'outdoors'],
      ['Salt Lake City', '/sublets/ut/salt-lake-city/', 1, 1, 'seasons', 'mid', ['health', 'explore', 'tech'], 'outdoors'],
      ['Rochester, MN', '/sublets/mn/rochester/', 1, 0, 'seasons', 'mid', ['health'], 'calm'],
      ['Ann Arbor', '/sublets/mi/ann-arbor/', 2, 1, 'seasons', 'college', ['study', 'health'], 'calm'],
      ['Madison', '/sublets/wi/madison/', 1, 1, 'seasons', 'college', ['study', 'health', 'gov'], 'outdoors'],
      ['Boulder', '/sublets/co/boulder/', 3, 1, 'seasons', 'college', ['study', 'tech'], 'outdoors'],
      ['Chapel Hill', '/sublets/nc/chapel-hill/', 2, 0, 'mild', 'college', ['study', 'health'], 'calm'],
      ['Gainesville', '/sublets/fl/gainesville/', 1, 0, 'warm', 'college', ['study', 'health'], 'calm'],
      ['Tucson', '/sublets/az/tucson/', 1, 0, 'warm', 'college', ['study', 'explore'], 'outdoors'],
      ['Raleigh', '/sublets/nc/raleigh/', 2, 0, 'mild', 'mid', ['tech', 'study', 'health'], 'calm'],
      ['Columbus', '/sublets/oh/columbus/', 1, 0, 'seasons', 'mid', ['study', 'health', 'finance'], 'calm']
    ];
    $('[data-quiz-go]', quiz).addEventListener('click', function () {
      var a = {}; $$('input:checked', quiz).forEach(function (i) { a[i.name] = i.value; });
      var budget = +a.budget;
      var scored = C.map(function (c) {
        var s = 0;
        if (c[6].indexOf(a.why) > -1) s += 4;
        s += 3 - Math.abs(c[2] - budget) * 1.5;
        if (a.car === 'yes') s += c[3] * 1.5; else s += 1;
        if (a.climate === 'mild') s += 1; else if (c[4] === a.climate) s += 2.5; else if (c[4] === 'mild') s += 1;
        if (c[5] === a.size) s += 2.5;
        if (c[7] === a.weekend) s += 2;
        return { c: c, s: s };
      }).sort(function (x, y) { return y.s - x.s; }).slice(0, 5);
      $('[data-out=quiz]').innerHTML = '<h3>Your top matches</h3>' + scored.map(function (r, i) {
        return '<div class="match"><span class="match-n">' + (i + 1) + '</span><div><strong>' + esc(r.c[0]) + '</strong><br><a href="' + r.c[1] + '">City guide &amp; sublets →</a></div></div>';
      }).join('') + '<p class="small muted">Just for fun — based on broad generalisations. Read each guide and compare real listings.</p>';
      $('[data-out=quiz]').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }
})();
