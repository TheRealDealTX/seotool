// Tiny Homes Blueprint - off-grid solar calculator for tiny houses.
(function () {
  var form = document.getElementById('sol');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var num = (window.THB && THB.num) || function (n, d) { return Number(n).toLocaleString('en-US', { maximumFractionDigits: d || 0 }); };
  var usd = (window.THB && THB.usd) || function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };

  // key: [name, watts, hours/day, qty, advice (for heavy loads), severity]
  var PRESETS = {
    lights:    ['LED lights', 9, 5, 6],
    fridge12:  ['12 V DC fridge', 50, 10, 1],
    fridgeac:  ['AC fridge (efficient)', 120, 9, 1],
    laptop:    ['Laptop', 60, 6, 1],
    phone:     ['Phone charging', 10, 2, 2],
    router:    ['Wi-Fi router', 12, 24, 1],
    tv:        ['TV (40 in LED)', 60, 3, 1],
    pump:      ['Water pump (12 V)', 60, 0.5, 1],
    fan:       ['Ventilation fan', 30, 6, 1],
    washer:    ['Washing machine', 500, 0.5, 1],
    microwave: ['Microwave', 1000, 0.25, 1, 'A microwave is fine in short bursts, but it sets the minimum size of your inverter.', ''],
    coffee:    ['Coffee maker', 900, 0.25, 1, 'Coffee makers are resistive heaters. A stovetop or propane option saves battery.', ''],
    induction: ['Induction cooktop', 1800, 1, 1, 'Induction cooking works off-grid but needs a large battery and a 3,000 W+ inverter, ideally on 48 V. Many off-grid homes cook on propane instead.', ''],
    minisplit: ['Mini-split (heat/cool)', 700, 8, 1, 'Heating and cooling are the biggest off-grid loads. Size for your worst month and consider propane or wood heat for winter.', ''],
    wellpump:  ['Well pump', 1000, 1, 1, 'Well pumps can draw 2-3x their running watts at startup. Size the inverter for that surge or fit a soft-start.', ''],
    heater:    ['Electric water heater', 4500, 1.5, 1, 'An electric tank water heater can use more energy than the rest of the house combined. Use a propane tankless or heat-pump water heater instead.', 'bad'],
    custom:    ['Custom appliance', 100, 1, 1]
  };
  var DEFAULTS = ['lights', 'fridge12', 'laptop', 'phone', 'router', 'tv', 'pump', 'fan'];
  var INVERTERS = [1000, 1500, 2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 15000];
  var rows = [];

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function mkRow(key) { var p = PRESETS[key]; return { key: key, name: p[0], w: p[1], h: p[2], q: p[3] }; }
  function wh(r) { return Math.max(0, r.w) * Math.max(0, r.h) * Math.max(0, r.q); }
  function isHeavy(r) { return r.w >= 1000 || (PRESETS[r.key] && PRESETS[r.key][4] && r.key !== 'microwave' && r.key !== 'coffee'); }

  // Preset dropdown.
  $('sol-preset').innerHTML = Object.keys(PRESETS).filter(function (k) { return k !== 'custom'; }).map(function (k) {
    var p = PRESETS[k]; return '<option value="' + k + '">' + esc(p[0]) + ' (' + num(p[1]) + ' W)</option>';
  }).join('');

  function renderRows() {
    $('sol-rows').innerHTML = rows.map(function (r, i) {
      var id = 'sol-r' + i;
      return '<tr data-i="' + i + '"' + (isHeavy(r) ? ' class="heavy"' : '') + '>' +
        '<td class="c-name"><label class="sr" for="' + id + '-n">Appliance name</label><input type="text" id="' + id + '-n" data-f="name" value="' + esc(r.name) + '" maxlength="40"></td>' +
        '<td class="c-w" data-l="Watts"><label class="sr" for="' + id + '-w">Watts for ' + esc(r.name) + '</label><input type="number" id="' + id + '-w" data-f="w" min="0" max="20000" step="1" value="' + r.w + '" inputmode="decimal"></td>' +
        '<td class="c-h" data-l="Hrs/day"><label class="sr" for="' + id + '-h">Hours per day for ' + esc(r.name) + '</label><input type="number" id="' + id + '-h" data-f="h" min="0" max="24" step="0.25" value="' + r.h + '" inputmode="decimal"></td>' +
        '<td class="c-q" data-l="Qty"><label class="sr" for="' + id + '-q">Quantity of ' + esc(r.name) + '</label><input type="number" id="' + id + '-q" data-f="q" min="0" max="50" step="1" value="' + r.q + '" inputmode="numeric"></td>' +
        '<td class="c-wh" data-wh>' + num(wh(r)) + ' Wh</td>' +
        '<td class="c-x"><button type="button" class="x-btn" data-del="' + i + '" aria-label="Remove ' + esc(r.name) + '">&times;</button></td></tr>';
    }).join('') || '<tr><td colspan="6" class="muted" style="padding:16px 6px">No appliances yet. Add one below.</td></tr>';
  }

  function calc() {
    var psh = +form.elements.psh.value, days = +form.elements.days.value;
    var lfp = form.elements.bat.value === 'lfp', V = +form.elements.volt.value;
    $('sol-psh-out').textContent = psh;
    $('sol-days-out').textContent = days;

    var daily = 0, smallPeak = 0, bigPeak = 0, flags = [], seen = {};
    rows.forEach(function (r) {
      daily += wh(r);
      var load = Math.max(0, r.w) * Math.max(0, r.q);
      if (r.w >= 1000) bigPeak = Math.max(bigPeak, load); else smallPeak += load;
      var p = PRESETS[r.key];
      if (r.q > 0 && r.h > 0 && p && p[4] && !seen[r.key]) { seen[r.key] = 1; flags.push([p[5] || '', '<strong>' + esc(r.name) + ':</strong> ' + p[4]]); }
      else if (r.q > 0 && r.key === 'custom' && r.w >= 1500 && !seen['c' + r.name]) { seen['c' + r.name] = 1; flags.push(['', '<strong>' + esc(r.name) + ' (' + num(r.w) + ' W):</strong> a heavy load. If it makes heat (heaters, kettles, dryers), consider propane or running it only on sunny afternoons.']); }
    });
    // Live-update the Wh cells without rebuilding inputs.
    $('sol-rows').querySelectorAll('tr[data-i]').forEach(function (tr) {
      var r = rows[+tr.dataset.i]; if (!r) return;
      tr.querySelector('[data-wh]').textContent = num(wh(r)) + ' Wh';
      tr.classList.toggle('heavy', !!isHeavy(r));
    });
    $('sol-sum').textContent = num(daily) + ' Wh';

    var arrayW = daily / psh / 0.75;
    var panels = Math.max(daily > 0 ? 1 : 0, Math.ceil(arrayW / 400));
    var dod = lfp ? 0.8 : 0.5;
    var battWh = daily * days / dod;
    var ah = battWh / V;
    var peak = smallPeak + bigPeak;
    var invNeed = peak * 1.25, inv = INVERTERS[INVERTERS.length - 1];
    for (var i = 0; i < INVERTERS.length; i++) if (INVERTERS[i] >= invNeed) { inv = INVERTERS[i]; break; }
    if (daily === 0) inv = 0;
    var installed = panels * 400;
    var cc = Math.ceil(installed / V * 1.25 / 10) * 10;

    $('sol-wh').textContent = num(daily) + ' Wh/day';
    $('sol-sub').textContent = 'About ' + num(daily * 30 / 1000) + ' kWh per month. Array needs ~' + num(arrayW) + ' W at ' + psh + ' sun hours.';
    $('sol-array').textContent = num(installed) + ' W';
    $('sol-array-l').textContent = 'solar array (' + panels + ' x 400 W panel' + (panels === 1 ? '' : 's') + ')';
    $('sol-batt').textContent = num(battWh / 1000, 1) + ' kWh';
    $('sol-batt-l').textContent = (lfp ? 'LiFePO4' : 'lead-acid') + ' bank, ' + num(ah) + ' Ah at ' + V + ' V';
    $('sol-inv').textContent = num(inv) + ' W';
    $('sol-inv-l').textContent = 'inverter (peak ' + num(peak) + ' W x 1.25)';
    $('sol-cc').textContent = num(cc) + ' A';
    $('sol-cc-l').textContent = 'MPPT charge controller at ' + V + ' V';

    var kwh = battWh / 1000;
    var eqLo = installed * 0.5 + kwh * (lfp ? 250 : 150) + inv * 0.35 + 800;
    var eqHi = installed * 0.9 + kwh * (lfp ? 450 : 300) + inv * 0.75 + 2500;
    if (daily === 0) { eqLo = eqHi = 0; }
    var r500 = function (n) { return Math.round(n / 500) * 500; };
    $('sol-cost').textContent = usd(r500(eqLo)) + ' - ' + usd(r500(eqHi));
    $('sol-cost-pro').textContent = usd(r500(eqLo * 1.6)) + ' - ' + usd(r500(eqHi * 2.2));

    if (V === 12 && (inv > 2000 || installed > 1600)) flags.unshift(['', '<strong>Consider 24 V or 48 V.</strong> At 12 V, a ' + num(inv) + ' W inverter can pull over ' + num(inv / 12) + ' A, which needs very heavy cables.']);
    if (!lfp && days >= 3) flags.push(['', 'A ' + days + '-day lead-acid bank is large and heavy (roughly ' + num(kwh * 60) + ' lb). LiFePO4 cuts that weight by about two-thirds.']);
    if (daily > 6000) flags.unshift(['bad', '<strong>Big daily load.</strong> Most off-grid tiny houses use 1-4 kWh a day. Moving heating, cooking and hot water to propane is the fastest way to shrink this system.']);
    else if (daily > 0 && daily <= 2500 && !flags.length) flags.push(['good', 'A lean, efficient load. This is a very manageable off-grid system for a tiny house.']);
    if (panels > 8) flags.push(['', panels + ' panels is more than most tiny house roofs hold. Plan for a ground mount.']);
    $('sol-flags').innerHTML = flags.map(function (f) { return '<li' + (f[0] ? ' class="' + f[0] + '"' : '') + '>' + f[1] + '</li>'; }).join('');
  }

  // Table editing.
  $('sol-rows').addEventListener('input', function (e) {
    var t = e.target, tr = t.closest('tr[data-i]'); if (!tr || !t.dataset.f) return;
    var r = rows[+tr.dataset.i]; if (!r) return;
    if (t.dataset.f === 'name') { r.name = t.value; return; }
    var v = parseFloat(t.value); r[t.dataset.f] = isNaN(v) ? 0 : Math.max(0, v);
    calc();
  });
  $('sol-rows').addEventListener('click', function (e) {
    var b = e.target.closest('[data-del]'); if (!b) return;
    var i = +b.dataset.del;
    rows.splice(i, 1); renderRows(); calc();
    var next = $('sol-rows').querySelector('[data-del="' + Math.min(i, rows.length - 1) + '"]');
    (next || $('sol-preset')).focus();
  });
  function addRow(key) {
    rows.push(mkRow(key)); renderRows(); calc();
    var inp = $('sol-r' + (rows.length - 1) + '-' + (key === 'custom' ? 'n' : 'w'));
    if (inp) { inp.focus(); if (key === 'custom') inp.select(); }
  }
  $('sol-add').addEventListener('click', function () { addRow($('sol-preset').value); });
  $('sol-custom').addEventListener('click', function () { addRow('custom'); });

  $('sol-region').addEventListener('change', function () {
    if (this.value !== 'custom') { form.elements.psh.value = this.value; calc(); }
  });
  form.elements.psh.addEventListener('input', function () {
    var v = this.value, opt = $('sol-region').querySelector('option[value="' + v + '"]');
    $('sol-region').value = opt ? v : 'custom';
  });
  form.addEventListener('change', function (e) { if (!e.target.closest('#sol-rows')) calc(); });
  form.addEventListener('input', function (e) { if (!e.target.closest('#sol-rows')) calc(); });
  form.addEventListener('submit', function (e) { e.preventDefault(); });

  rows = DEFAULTS.map(mkRow);
  renderRows();
  calc();
})();
