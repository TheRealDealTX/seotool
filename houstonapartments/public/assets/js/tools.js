/* Houston Apartments — renter tools (calculators, checklists, commute finder) */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var money = function (n) { return '$' + Math.round(Math.max(0, n) || 0).toLocaleString(); };
  var num = function (root, name) { var el = $('[name="' + name + '"]', root); return el ? parseFloat(el.value) || 0 : 0; };
  var out = function (root, key) { return $('[data-out="' + key + '"]', root); };
  var store = {
    get: function (k, d) { try { return JSON.parse(localStorage.getItem('ha-tool-' + k)) || d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem('ha-tool-' + k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };
  var app = $('[data-tool]');
  if (!app) return;
  var tool = app.getAttribute('data-tool');
  var bind = function (fn) { app.addEventListener('input', fn); app.addEventListener('change', fn); fn(); };

  /* ---------- rent affordability ---------- */
  if (tool === 'rent-affordability-calculator') {
    bind(function () {
      var hourly = $('[name=ra_type]:checked', app).value === 'hour';
      $$('[data-show]', app).forEach(function (el) { el.hidden = el.getAttribute('data-show') !== (hourly ? 'hour' : 'year'); });
      var yearly = (hourly ? num(app, 'ra_rate') * num(app, 'ra_hours') * 52 : num(app, 'ra_income')) + num(app, 'ra_extra');
      var monthly = yearly / 12, debt = num(app, 'ra_debt');
      var max = monthly / 3, forty = yearly / 40, comfy = Math.max(0, monthly * 0.30 - debt * 0.5);
      out(app, 'max').textContent = money(max);
      out(app, 'monthly').textContent = money(monthly);
      out(app, 'forty').textContent = money(forty);
      out(app, 'comfy').textContent = money(Math.min(comfy, max));
      out(app, 'gauge').style.width = Math.min(100, max / 4000 * 100) + '%';
      var cap = Math.max(500, Math.round(max / 50) * 50);
      out(app, 'link').href = '/apartments/under-' + cap + '/';
    });
  }

  /* ---------- move-in costs ---------- */
  if (tool === 'move-in-cost-calculator') {
    var date = $('[name=mc_date]', app);
    if (!date.value) { var d = new Date(); d.setDate(d.getDate() + 30); date.value = d.toISOString().slice(0, 10); }
    bind(function () {
      var rent = num(app, 'mc_rent'), pets = num(app, 'mc_pets');
      var first = rent, label = 'First month’s rent';
      if ($('[name=mc_prorate]', app).checked && date.value) {
        var dt = new Date(date.value + 'T12:00:00'), days = new Date(dt.getFullYear(), dt.getMonth() + 1, 0).getDate();
        var left = days - dt.getDate() + 1;
        first = rent / days * left;
        label = 'Prorated rent (' + left + ' of ' + days + ' days)';
      }
      var lines = [
        [label, first], ['Security deposit', num(app, 'mc_deposit')], ['Admin fee', num(app, 'mc_admin')],
        ['Application fees', num(app, 'mc_app') * num(app, 'mc_adults')],
        ['Pet fees / deposits', num(app, 'mc_petfee') * pets], ['First month pet rent', num(app, 'mc_petrent') * pets]
      ];
      var due = lines.reduce(function (s, l) { return s + l[1]; }, 0);
      var extra = num(app, 'mc_util') + parseFloat($('[name=mc_movers]', app).value);
      out(app, 'due').textContent = money(due);
      out(app, 'total').textContent = money(due + extra);
      out(app, 'lines').innerHTML = lines.filter(function (l) { return l[1] > 0; }).map(function (l) { return '<dt>' + l[0] + '</dt><dd>' + money(l[1]) + '</dd>'; }).join('') +
        '<dt>Utilities &amp; movers (not due at signing)</dt><dd>' + money(extra) + '</dd>';
    });
  }

  /* ---------- roommate split ---------- */
  if (tool === 'rent-split-calculator') {
    var mates = $('[data-mates]', app);
    var addMate = function (name, size, bath, income) {
      var row = document.createElement('div');
      row.className = 'mate';
      row.innerHTML = '<label class="field">Name<input name="m_name" value="' + name + '"></label>' +
        '<label class="field" data-m="size">Bedroom sq ft<input type="number" name="m_size" value="' + size + '" min="40"></label>' +
        '<label class="check" data-m="size"><input type="checkbox" name="m_bath"' + (bath ? ' checked' : '') + '> Private bath</label>' +
        '<label class="field" data-m="income">Yearly income<span class="money-in"><i>$</i><input type="number" name="m_income" value="' + income + '" min="0" step="1000"></span></label>' +
        '<button type="button" class="mate-x" aria-label="Remove">×</button>';
      mates.appendChild(row);
    };
    addMate('Roommate 1', 160, true, 65000);
    addMate('Roommate 2', 130, false, 52000);
    $('[data-add-mate]', app).addEventListener('click', function () { addMate('Roommate ' + (mates.children.length + 1), 120, false, 50000); update(); });
    mates.addEventListener('click', function (e) { if (e.target.closest('.mate-x') && mates.children.length > 2) { e.target.closest('.mate').remove(); update(); } });
    var update = function () {
      var mode = $('[name=rs_mode]:checked', app).value, rent = num(app, 'rs_rent'), util = num(app, 'rs_util');
      var rows = $$('.mate', mates);
      $$('[data-m]', mates).forEach(function (el) { el.hidden = el.getAttribute('data-m') !== mode; });
      var weights = rows.map(function (r) {
        if (mode === 'size') return (parseFloat($('[name=m_size]', r).value) || 0) * ($('[name=m_bath]', r).checked ? 1.15 : 1);
        if (mode === 'income') return parseFloat($('[name=m_income]', r).value) || 0;
        return 1;
      });
      var total = weights.reduce(function (a, b) { return a + b; }, 0) || 1;
      out(app, 'split').innerHTML = rows.map(function (r, i) {
        var share = rent * weights[i] / total + util / rows.length;
        return '<div class="split-row"><span>' + ($('[name=m_name]', r).value || 'Roommate') + '</span><strong>' + money(share) + '</strong><small>' + Math.round(weights[i] / total * 100) + '% of rent</small></div>';
      }).join('');
    };
    bind(update);
  }

  /* ---------- true-cost comparison ---------- */
  if (tool === 'apartment-cost-comparison') {
    var cols = $('[data-cols]', app);
    var fields = [['name', 'Apartment', 'text'], ['rent', 'Monthly rent', 'money'], ['util', 'Utilities / mo', 'money'], ['parking', 'Parking / mo', 'money'],
      ['fees', 'Other monthly fees', 'money'], ['pet', 'Pet rent / mo', 'money'], ['free', 'Free weeks (special)', 'num'], ['miles', 'Commute miles (one way)', 'num'], ['tolls', 'Tolls / mo', 'money']];
    var addCol = function (vals) {
      var c = document.createElement('div'); c.className = 'cmp-col';
      c.innerHTML = fields.map(function (f) {
        var v = vals[f[0]] != null ? vals[f[0]] : '';
        if (f[2] === 'money') return '<label class="field">' + f[1] + '<span class="money-in"><i>$</i><input type="number" data-f="' + f[0] + '" value="' + v + '" min="0" step="5"></span></label>';
        return '<label class="field">' + f[1] + '<input ' + (f[2] === 'num' ? 'type="number" min="0" step="0.5"' : '') + ' data-f="' + f[0] + '" value="' + v + '"></label>';
      }).join('') + '<div class="cmp-total"><span>True monthly cost</span><strong>$0</strong><small></small></div><button type="button" class="mate-x" aria-label="Remove">×</button>';
      cols.appendChild(c);
    };
    addCol({ name: 'Inner Loop high-rise', rent: 1850, util: 140, parking: 75, fees: 45, pet: 0, free: 6, miles: 4, tolls: 0 });
    addCol({ name: 'Suburban garden', rent: 1350, util: 170, parking: 0, fees: 30, pet: 0, free: 0, miles: 18, tolls: 60 });
    $('[data-add-col]', app).addEventListener('click', function () { if (cols.children.length < 4) { addCol({ name: 'Apartment ' + (cols.children.length + 1) }); update(); } });
    cols.addEventListener('click', function (e) { if (e.target.closest('.mate-x') && cols.children.length > 2) { e.target.closest('.cmp-col').remove(); update(); } });
    var update = function () {
      var term = Math.max(1, num(app, 'cc_term')), mile = num(app, 'cc_mile'), days = num(app, 'cc_days');
      var totals = $$('.cmp-col', cols).map(function (c) {
        var g = function (k) { return parseFloat($('[data-f=' + k + ']', c).value) || 0; };
        var rent = g('rent'), special = rent * 12 / 52 * g('free') / term;
        var drive = g('miles') * 2 * days * mile;
        var t = rent - special + g('util') + g('parking') + g('fees') + g('pet') + drive + g('tolls');
        $('.cmp-total strong', c).textContent = money(t);
        $('.cmp-total small', c).textContent = 'incl. ' + money(drive) + ' driving' + (special ? ', −' + money(special) + ' special' : '');
        return [c, t];
      });
      var best = Math.min.apply(null, totals.map(function (t) { return t[1]; }));
      totals.forEach(function (t) { t[0].classList.toggle('best', t[1] === best); });
    };
    bind(update);
  }

  /* ---------- commute finder ---------- */
  if (tool === 'commute-apartment-finder' && window.L) {
    var mapEl = $('#commute-map'), circle = null, marker = null, center = null;
    var map = L.map(mapEl, { scrollWheelZoom: false }).setView([29.76, -95.37], 10);
    if (L.maplibreGL && window.HA_MAP) L.maplibreGL({ style: HA_MAP.style, attribution: HA_MAP.attr, interactive: false }).addTo(map);
    else L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap' }).addTo(map);
    var miles = function () { return num(app, 'cf_miles'); };
    var draw = function () {
      out(app, 'miles').textContent = miles() + ' miles';
      var lo = Math.round(miles() / 40 * 60), hi = Math.round(miles() / 20 * 60);
      out(app, 'drive').textContent = 'Roughly ' + lo + '–' + hi + ' minutes by car, depending on traffic.';
      if (!center) return;
      if (circle) map.removeLayer(circle);
      if (marker) map.removeLayer(marker);
      circle = L.circle(center, { radius: miles() * 1609.34, color: '#ff6b4a', weight: 3, fillOpacity: 0.08 }).addTo(map);
      marker = L.marker(center, { icon: L.divIcon({ className: '', html: '<div class="home-pin"></div>', iconSize: [18, 18] }) }).addTo(map);
      map.fitBounds(circle.getBounds(), { padding: [20, 20] });
      var pts = [];
      for (var i = 0; i < 36; i++) {
        var a = i / 36 * 2 * Math.PI, dLat = miles() / 69 * Math.cos(a), dLng = miles() / (69 * Math.cos(center[0] * Math.PI / 180)) * Math.sin(a);
        pts.push((center[0] + dLat).toFixed(5) + ',' + (center[1] + dLng).toFixed(5));
      }
      var link = out(app, 'link');
      link.href = '/apartments/?poly=' + encodeURIComponent(pts.join(';'));
      link.hidden = false;
    };
    app.addEventListener('input', function (e) { if (e.target.name === 'cf_miles') draw(); });
    $$('[data-place]', app).forEach(function (b) {
      b.addEventListener('click', function () { center = b.getAttribute('data-place').split(',').map(Number); $('[name=cf_addr]', app).value = b.textContent + ', Houston'; out(app, 'msg').textContent = ''; draw(); });
    });
    var find = function () {
      var q = $('[name=cf_addr]', app).value.trim(), msg = out(app, 'msg');
      if (!q) { msg.className = 'form-msg err'; msg.textContent = 'Enter an address or pick a place.'; return; }
      msg.className = 'form-msg'; msg.textContent = 'Finding that address…';
      fetch('/api/geocode?q=' + encodeURIComponent(/tx|texas|houston/i.test(q) ? q : q + ', Houston, TX')).then(function (r) { return r.json(); }).then(function (j) {
        if (!j.lat) { msg.className = 'form-msg err'; msg.textContent = 'We couldn’t find that address. Try adding the ZIP code, or pick a place above.'; return; }
        msg.textContent = ''; center = [j.lat, j.lng]; draw();
      }).catch(function () { msg.className = 'form-msg err'; msg.textContent = 'Something went wrong – please try again.'; });
    };
    $('[data-find]', app).addEventListener('click', find);
    $('[name=cf_addr]', app).addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); find(); } });
    draw();
  }

  /* ---------- checklists (saved in this browser) ---------- */
  var list = $('[data-checklist]', app);
  if (list) {
    var key = list.getAttribute('data-checklist'), state = store.get(key, {});
    var boxes = $$('input[type=checkbox][data-key]', list);
    var texts = $$('input[name^=cl_], textarea[name^=cl_]', list);
    boxes.forEach(function (b) { b.checked = !!state[b.getAttribute('data-key')]; });
    texts.forEach(function (t) { if (state[t.name]) t.value = state[t.name]; });
    var refresh = function () {
      var done = boxes.filter(function (b) { return b.checked; }).length, pct = Math.round(done / boxes.length * 100);
      out(list, 'pct').textContent = pct + '% done';
      out(list, 'bar').style.width = pct + '%';
      var cd = out(list, 'countdown'), dt = $('[name=cl_date]', list);
      if (cd && dt && dt.value) {
        var days = Math.ceil((new Date(dt.value + 'T12:00:00') - new Date()) / 864e5);
        cd.textContent = days > 0 ? days + ' days until your move' : days === 0 ? 'Moving day – good luck!' : 'Moved ' + -days + ' days ago';
      }
    };
    list.addEventListener('change', function () {
      boxes.forEach(function (b) { state[b.getAttribute('data-key')] = b.checked; });
      texts.forEach(function (t) { state[t.name] = t.value; });
      store.set(key, state); refresh();
    });
    list.addEventListener('input', function (e) { if (e.target.name) { state[e.target.name] = e.target.value; store.set(key, state); } });
    $('[data-reset-list]', list).addEventListener('click', function () {
      if (!confirm('Clear this checklist?')) return;
      state = {}; store.set(key, state);
      boxes.forEach(function (b) { b.checked = false; }); texts.forEach(function (t) { t.value = ''; }); refresh();
    });
    refresh();
  }
})();
