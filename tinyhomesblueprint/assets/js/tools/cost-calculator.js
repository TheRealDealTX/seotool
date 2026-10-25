// Tiny Homes Blueprint - tiny house cost calculator.
// Canonical model shared across the site: $/sq ft by labor and finish level, plus
// trailer/foundation, utilities, permits and extras as separate line items.
(function () {
  var form = document.getElementById('cc');
  if (!form) return;
  var usd = (window.THB && THB.usd) || function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };

  // [low, high] $/sq ft for structure + finishes. Index = finish level (0 basic, 1 mid, 2 high).
  var RATES = {
    diy:     [[150, 220], [190, 260], [240, 330]],
    builder: [[250, 330], [300, 400], [380, 500]]
  };
  // How the structure cost splits into trades (sums to 1).
  var SHARES = [
    ['shell', 'Shell & framing', 'Floor system, walls, sheathing, siding', 0.20],
    ['roof', 'Roofing', 'Roof framing, underlayment, metal or shingles', 0.07],
    ['windows', 'Windows & doors', 'Exterior doors, windows, skylights', 0.09],
    ['insul', 'Insulation', 'Walls, floor and roof, air sealing', 0.05],
    ['elec', 'Electrical', 'Panel, wiring, fixtures, devices', 0.08],
    ['plumb', 'Plumbing', 'Supply, drains, vents, fixtures hookup', 0.08],
    ['hvac', 'HVAC', 'Mini-split or heater, ventilation', 0.06],
    ['interior', 'Interior finishes', 'Wall and ceiling finish, flooring, trim, paint', 0.20],
    ['kb', 'Kitchen & bath', 'Cabinets, counters, sinks, shower, toilet', 0.17]
  ];
  var SHELL_KEYS = { shell: 1, roof: 1, windows: 1 };
  var APPLIANCES = [[2500, 5000], [5000, 10000], [10000, 20000]];
  var FINISH_NAMES = ['basic', 'mid-range', 'high-end'];
  var LABOR_NAMES = { diy: 'DIY', partial: 'DIY + hired trades', builder: 'builder-built' };

  var $ = function (id) { return document.getElementById(id); };
  var last = null;

  function val(name) {
    var el = form.elements[name];
    if (!el) return null;
    if (el.type === 'checkbox') return el.checked;
    return el.value;
  }
  function clamp(n, a, b) { return Math.max(a, Math.min(b, n)); }
  function r100(n) { return Math.round(n / 100) * 100; }
  function r1k(n) { return Math.round(n / 1000) * 1000; }

  function rate(labor, f) {
    if (labor === 'partial') {
      var d = RATES.diy[f], b = RATES.builder[f];
      return [(d[0] + b[0]) / 2, (d[1] + b[1]) / 2];
    }
    return RATES[labor][f];
  }

  function syncBase(type) {
    // THOW is always on a trailer; foundation homes use piers or slab; a shell can sit on any.
    var labels = form.querySelectorAll('[data-base]');
    var allowed = type === 'thow' ? ['trailer'] : type === 'foundation' ? ['piers', 'slab'] : ['trailer', 'piers', 'slab'];
    labels.forEach(function (l) { l.hidden = allowed.indexOf(l.dataset.base) < 0; });
    $('cc-base-field').hidden = type === 'thow';
    var cur = val('base');
    if (allowed.indexOf(cur) < 0) form.querySelector('input[name=base][value=' + allowed[0] + ']').checked = true;
  }

  function calc() {
    var size = +val('size');
    var type = val('type');
    syncBase(type);
    var base = val('base');
    var finish = +val('finish');
    var labor = val('labor');
    var util = val('util');
    var land = Math.max(0, +val('land') || 0);
    var shellOnly = type === 'shell';
    var onTrailer = base === 'trailer';
    var f = clamp((size - 150) / 850, 0, 1); // 0 at 150 sq ft, 1 at 1,000 sq ft
    var items = [];
    var flags = [];

    $('cc-size-out').textContent = size;
    $('cc-deliv-txt').firstChild.nodeValue = onTrailer ? 'Delivery & transport' : 'Site prep & delivery';

    // Structure and finishes.
    var rt = rate(labor, finish);
    var sLo = size * rt[0], sHi = size * rt[1];
    if (shellOnly) {
      // A dried-in shell is ~45-55% of the full finished cost at the same labor level.
      sLo *= 0.45; sHi *= 0.55;
      var shellShare = 0.20 + 0.07 + 0.09;
      SHARES.forEach(function (s) {
        var k = SHELL_KEYS[s[0]] ? s[3] / shellShare : 0;
        items.push({ key: s[0], name: s[1], note: k ? s[2] : 'Not included in a shell', lo: sLo * k, hi: sHi * k, group: 'build' });
      });
    } else {
      SHARES.forEach(function (s) {
        items.push({ key: s[0], name: s[1], note: s[2], lo: sLo * s[3], hi: sHi * s[3], group: 'build' });
      });
    }
    if (val('loft')) items.push({ key: 'loft', name: 'Sleeping loft', note: 'About 10% of structure cost', lo: sLo * 0.10, hi: sHi * 0.10, group: 'build' });

    // Toilet goes into kitchen & bath for finished builds.
    if (!shellOnly) {
      var kb = items.filter(function (i) { return i.key === 'kb'; })[0];
      if (val('toilet') === 'compost') { kb.lo += 900; kb.hi += 2000; kb.note = 'Cabinets, counters, fixtures, composting toilet'; }
      else { kb.lo += 300; kb.hi += 800; kb.note = 'Cabinets, counters, fixtures, flush toilet'; }
    }

    // Trailer or foundation.
    var bLo, bHi, bName, bNote;
    if (onTrailer) {
      var len = clamp(Math.ceil(size / 8.5), 16, 40);
      var ft = clamp((len - 16) / 16, 0, 1);
      bLo = 6000 + ft * 4000; bHi = 8000 + ft * 4000;
      bName = 'Trailer'; bNote = 'About ' + len + ' ft deck at 8.5 ft wide';
      if (size > 340) flags.push(['bad', '<strong>Too big for one trailer?</strong> ' + size + ' sq ft on an 8.5 ft wide trailer needs about ' + Math.ceil(size / 8.5) + ' ft of deck. Most tiny house trailers top out around 32&ndash;40 ft. Consider a loft, a gooseneck or a foundation.']);
    } else if (base === 'piers') {
      bLo = 4000 + f * 3000; bHi = 7000 + f * 3000;
      bName = 'Foundation (piers)'; bNote = 'Concrete piers or helical piles';
    } else {
      bLo = 8000 + f * 6000; bHi = 14000 + f * 6000;
      bName = 'Foundation (slab)'; bNote = 'Gravel base, forms, insulation, concrete';
    }
    items.push({ key: 'base', name: bName, note: bNote, lo: bLo, hi: bHi, group: 'base' });

    // Utilities.
    if (util === 'grid') items.push({ key: 'util', name: 'Utilities (grid hookup)', note: 'Power, water and sewer connections', lo: 3000 + f * 3000, hi: 9000 + f * 6000, group: 'util' });
    else if (util === 'solar') items.push({ key: 'util', name: 'Utilities (off-grid solar)', note: 'Panels, batteries, inverter, installed', lo: 8000 + f * 8000, hi: 18000 + f * 12000, group: 'util' });
    else items.push({ key: 'util', name: 'Utilities', note: 'Not included', lo: 0, hi: 0, group: 'util' });

    // Permits and plans.
    if (val('permits')) {
      if (onTrailer) items.push({ key: 'permits', name: 'Plans & permits', note: 'Plan set, inspections or third-party certification', lo: 1000, hi: 3500, group: 'permits' });
      else items.push({ key: 'permits', name: 'Plans & permits', note: 'Plan set, building permit, engineering if required', lo: 2500, hi: 8000, group: 'permits' });
    } else {
      items.push({ key: 'permits', name: 'Plans & permits', note: 'Not included', lo: 0, hi: 0, group: 'permits' });
    }

    // Extras.
    if (val('appliances')) {
      if (shellOnly) flags.push(['', 'Appliances are left out of a shell-only estimate. Add them when you price the finish-out.']);
      else items.push({ key: 'appl', name: 'Appliances', note: FINISH_NAMES[finish] + ' package', lo: APPLIANCES[finish][0], hi: APPLIANCES[finish][1], group: 'extras' });
    }
    if (val('delivery')) {
      if (onTrailer) items.push({ key: 'deliv', name: 'Delivery & transport', note: 'Professional tow, permits, setup', lo: 1500, hi: 5000, group: 'extras' });
      else items.push({ key: 'deliv', name: 'Site prep & delivery', note: 'Clearing, grading, driveway access', lo: 3000, hi: 10000, group: 'extras' });
    }
    if (land > 0) items.push({ key: 'land', name: 'Land', note: 'Your figure', lo: land, hi: land, group: 'land' });

    // Advice flags.
    if (shellOnly) flags.unshift(['', '<strong>Shell only:</strong> framing, roofing, windows and doors. Insulation, systems and interior finishes are excluded, and the shell is priced at 45&ndash;55% of the full cost.']);
    if (val('toilet') === 'flush' && util !== 'grid' && !shellOnly) flags.push(['', 'A flush toilet without a sewer hookup needs a septic system, often $8,000&ndash;$20,000 or more. It is not included here.']);
    if (labor === 'diy' && !shellOnly) flags.push(['', 'Many jurisdictions require licensed trades for electrical and plumbing even on owner-built homes. Check before you budget for full DIY.']);

    // Totals.
    var tLo = 0, tHi = 0, landAmt = 0;
    items.forEach(function (i) { i.lo = r100(i.lo); i.hi = r100(i.hi); tLo += i.lo; tHi += i.hi; if (i.key === 'land') landAmt = i.lo; });
    var groups = { build: [0, 0], base: [0, 0], util: [0, 0], permits: [0, 0], extras: [0, 0], land: [0, 0] };
    items.forEach(function (i) { groups[i.group][0] += i.lo; groups[i.group][1] += i.hi; });

    var typeName = shellOnly ? 'shell' : type === 'thow' ? 'tiny house on wheels' : 'tiny house on a foundation';
    var sub = size + ' sq ft ' + typeName + ', ' + FINISH_NAMES[finish] + ' finishes, ' + LABOR_NAMES[labor];

    $('cc-total').textContent = usd(r1k(tLo)) + ' - ' + usd(r1k(tHi));
    $('cc-sub').textContent = sub;
    $('cc-psf').textContent = usd((tLo - landAmt) / size) + ' - ' + usd((tHi - landAmt) / size);
    $('cc-mid').textContent = usd(r1k((tLo + tHi) / 2));

    var rowDefs = [
      ['build', shellOnly ? 'Shell structure' : 'Structure & finishes'],
      ['base', onTrailer ? 'Trailer' : 'Foundation'],
      ['util', 'Utilities'], ['permits', 'Plans & permits'], ['extras', 'Appliances & extras'], ['land', 'Land']
    ];
    $('cc-rows').innerHTML = rowDefs.filter(function (r) { return groups[r[0]][1] > 0; }).map(function (r) {
      var g = groups[r[0]];
      return '<li><span>' + r[1] + '</span><b>' + rangeTxt(g[0], g[1]) + '</b></li>';
    }).join('');

    $('cc-flags').innerHTML = flags.map(function (fl) { return '<li' + (fl[0] ? ' class="' + fl[0] + '"' : '') + '>' + fl[1] + '</li>'; }).join('');

    var maxMid = 1;
    items.forEach(function (i) { maxMid = Math.max(maxMid, (i.lo + i.hi) / 2); });
    var totMid = (tLo + tHi) / 2 || 1;
    $('cc-table').innerHTML = items.map(function (i) {
      var mid = (i.lo + i.hi) / 2;
      var pct = Math.round(mid / totMid * 100);
      return '<tr' + (i.hi === 0 ? ' class="zero"' : '') + '><td>' + i.name + '<small>' + i.note + '</small></td>' +
        '<td class="num">' + (i.hi ? usd(i.lo) : '-') + '</td><td class="num">' + (i.hi ? usd(i.hi) : '-') + '</td>' +
        '<td class="bar-col"><div class="lbar" title="' + pct + '% of total"><i style="width:' + (mid / maxMid * 100).toFixed(1) + '%"></i></div></td></tr>';
    }).join('');
    $('cc-tlo').textContent = usd(tLo);
    $('cc-thi').textContent = usd(tHi);

    last = { sub: sub, items: items, tLo: tLo, tHi: tHi, landAmt: landAmt, size: size };
  }

  function rangeTxt(lo, hi) { return lo === hi ? usd(lo) : usd(lo) + ' - ' + usd(hi); }

  function estimateText() {
    if (!last) return '';
    var lines = ['Tiny house cost estimate (Tiny Homes Blueprint)', last.sub, ''];
    last.items.forEach(function (i) { if (i.hi) lines.push(i.name + ': ' + rangeTxt(i.lo, i.hi)); });
    lines.push('', 'Total: ' + rangeTxt(last.tLo, last.tHi));
    lines.push('Per sq ft (before land): ' + usd((last.tLo - last.landAmt) / last.size) + ' - ' + usd((last.tHi - last.landAmt) / last.size));
    lines.push('', 'Planning estimate only. ' + location.href.split('#')[0]);
    return lines.join('\n');
  }

  function copy() {
    var text = estimateText(), status = $('cc-copy-status');
    function done(ok) { status.textContent = ok ? 'Estimate copied to your clipboard.' : 'Copy failed. Select the breakdown table and copy it manually.'; }
    function fallback() {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      document.body.removeChild(ta); done(ok);
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
    else fallback();
  }

  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  $('cc-copy').addEventListener('click', copy);
  $('cc-print').addEventListener('click', function () { window.print(); });
  calc();
})();
