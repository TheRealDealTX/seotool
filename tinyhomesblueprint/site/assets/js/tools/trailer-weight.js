// Tiny Homes Blueprint - tiny house trailer weight calculator.
// Component weights scaled by trailer length (L, ft). Calibrated so a typical finished
// 24 ft tiny house lands around 10,000-14,000 lb including the trailer.
(function () {
  var form = document.getElementById('tw');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var num = (window.THB && THB.num) || function (n) { return Number(n).toLocaleString('en-US'); };

  var FRAME = { '2x4': 70, '2x6': 90, steel: 50, sips: 85 };
  var FRAME_N = { '2x4': 'Wood 2x4', '2x6': 'Wood 2x6', steel: 'Steel stud', sips: 'SIPs' };
  var SIDING = { vinyl: 14, wood: 40, metal: 25, fiber: 70 };
  var SIDING_N = { vinyl: 'vinyl', wood: 'wood', metal: 'metal', fiber: 'fiber cement' };
  var ROOFING = { metal: 11, shingle: 30 };     // lb per ft of (L + 2) roof length
  var INTERIOR = { pine: 40, drywall: 60 };
  var GVWR = [
    [7000, 'Tandem 3,500 lb axles', 'bumper'],
    [10000, 'Tandem 5,200 lb axles', 'any'],
    [14000, 'Tandem 7,000 lb axles', 'any'],
    [16000, 'Tandem 8,000 or triple 5,200 lb axles', 'any'],
    [21000, 'Triple 7,000 lb axles', 'gooseneck']
  ];
  var SCALE = 24000;

  function val(n) { return form.elements[n].value; }
  function r100(n) { return Math.round(n / 100) * 100; }
  function lb(n) { return num(r100(n)) + ' lb'; }

  function calc() {
    var L = +val('len'), type = val('type'), goose = type === 'gooseneck';
    var frame = val('frame'), siding = val('siding'), roof = val('roof'), interior = val('interior');
    var lofts = +val('lofts'), water = +val('water'), contents = +val('contents');
    $('tw-len-out').textContent = L;
    $('tw-water-out').textContent = water;
    $('tw-contents-out').textContent = num(contents);

    var parts = [
      ['Trailer', goose ? 140 * L + 700 : 125 * L + 300],
      ['Floor system', 35 * L],
      ['Wall framing (' + FRAME_N[frame] + ')', FRAME[frame] * L],
      ['Siding (' + SIDING_N[siding] + ')', SIDING[siding] * L],
      ['Roof framing & sheathing', 27.5 * (L + 2)],
      ['Roofing (' + roof + ')', ROOFING[roof] * (L + 2)],
      ['Interior walls & ceiling', INTERIOR[interior] * L],
      ['Windows & doors', 18 * L],
      ['Flooring', 12 * L],
      ['Kitchen, bath & appliances', 900 + 20 * L],
      ['Electrical, plumbing & HVAC', 350 + 8 * L]
    ];
    if (lofts) parts.push([lofts > 1 ? 'Lofts (2)' : 'Loft', 450 * lofts]);
    if (water) parts.push(['Water (' + water + ' gal)', water * 8.34]);
    if (contents) parts.push(['Belongings', contents]);

    var total = 0;
    parts.forEach(function (p) { total += p[1]; });
    var lo = total * 0.9, hi = total * 1.1;

    $('tw-total').textContent = lb(total);
    $('tw-sub').textContent = 'Likely range ' + num(r100(lo)) + ' - ' + num(r100(hi)) + ' lb for a ' + L + ' ft ' + (goose ? 'gooseneck' : 'bumper-pull') + ' build';
    $('tw-plf').textContent = num(Math.round(total / L / 10) * 10) + ' lb';
    var tw = goose ? [0.15, 0.25] : [0.10, 0.15];
    $('tw-tongue').textContent = num(r100(total * tw[0])) + ' - ' + num(r100(total * tw[1])) + ' lb';
    $('tw-tongue-l').textContent = goose ? 'pin weight on the truck (15-25%)' : 'tongue weight on the hitch (10-15%)';

    // Gauge.
    var g = '<div class="gauge-fill" style="width:' + Math.min(100, total / SCALE * 100).toFixed(1) + '%"></div>' +
      '<div class="gauge-range" style="left:' + Math.min(100, lo / SCALE * 100).toFixed(1) + '%;width:' + Math.min(100 - lo / SCALE * 100, (hi - lo) / SCALE * 100).toFixed(1) + '%"></div>';
    GVWR.forEach(function (r) { g += '<div class="gauge-tick" style="left:' + (r[0] / SCALE * 100).toFixed(1) + '%"><span>' + r[0] / 1000 + 'k</span></div>'; });
    $('tw-gauge').innerHTML = g;

    // GVWR table: recommend the smallest rating with >=10% margin over the HIGH estimate.
    var rec = null;
    GVWR.forEach(function (r) { if (!rec && hi <= r[0] * 0.9 && (r[2] === 'any' || r[2] === type)) rec = r[0]; });
    $('tw-gvwr').innerHTML = GVWR.map(function (r) {
      var m = (r[0] - total) / r[0] * 100;
      var chip = m < 0 ? '<span class="chip chip-bad">Over by ' + num(r100(total - r[0])) + ' lb</span>'
        : m < 10 ? '<span class="chip chip-warn">' + Math.round(m) + '% tight</span>'
        : '<span class="chip chip-ok">' + Math.round(m) + '% spare</span>';
      var note = r[2] === 'gooseneck' ? ' <small class="muted">(usually gooseneck)</small>' : r[2] === 'bumper' ? ' <small class="muted">(bumper pull)</small>' : '';
      return '<tr' + (r[0] === rec ? ' class="rec"' : '') + '><td><b>' + num(r[0]) + ' lb</b>' + (r[0] === rec ? '<br><small style="color:var(--ok);font-weight:700">Recommended</small>' : '') + '</td><td>' + r[1] + note + '</td><td class="num">' + chip + '</td></tr>';
    }).join('');

    // Breakdown.
    var sorted = parts.slice().sort(function (a, b) { return b[1] - a[1]; });
    $('tw-bk').innerHTML = sorted.map(function (p) { return '<li><span>' + p[0] + '</span><b>' + lb(p[1]) + '</b></li>'; }).join('');

    // Flags and tow guidance.
    var flags = [];
    if (rec) flags.push(['good', '<strong>Suggested trailer: ' + num(rec) + ' lb GVWR or higher.</strong> That leaves at least 10% margin above the high end of your estimate.']);
    else flags.push(['bad', '<strong>Heavier than common tiny house trailers.</strong> Even a 21,000 lb gooseneck leaves under 10% margin. Shorten the house or choose lighter materials.']);
    if (!goose && hi > 14000) flags.push(['', 'Above about 14,000 lb, a gooseneck is often easier and more stable to tow than a bumper pull.']);
    var guide;
    if (hi <= 7000) guide = 'Many half-ton pickups and some large SUVs are rated to tow in this range when properly equipped.';
    else if (hi <= 10000) guide = 'Some well-equipped half-ton pickups are rated this high, but a 3/4-ton (2500-series) truck gives more margin for long tows.';
    else if (hi <= 14000) guide = 'Plan on a 3/4-ton or 1-ton (2500/3500-series) pickup. Most half-ton trucks are not rated this high.';
    else if (hi <= 18000) guide = 'This usually takes a heavy-duty 1-ton pickup, often a dually, and a gooseneck hitch is strongly recommended.';
    else guide = 'This is at or beyond the limit of most pickups once you include the truck\'s own weight (GCWR). Consider a medium-duty truck or a professional tiny house mover.';
    flags.push(['', '<strong>Tow vehicle:</strong> ' + guide + ' Ratings vary by vehicle, so check your owner\'s manual and door-jamb sticker.']);
    if (water >= 40) flags.push(['', 'Towing with ' + water + ' gallons adds ' + num(Math.round(water * 8.34)) + ' lb. Consider filling tanks at your destination.']);
    $('tw-flags').innerHTML = flags.map(function (f) { return '<li' + (f[0] ? ' class="' + f[0] + '"' : '') + '>' + f[1] + '</li>'; }).join('');
  }

  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  calc();
})();
