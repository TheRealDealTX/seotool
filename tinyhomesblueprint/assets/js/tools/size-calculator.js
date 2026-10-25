// Tiny Homes Blueprint - "how big should my tiny house be" size calculator.
// Adds a low/high square-foot allowance per zone, then ~10% for walls and circulation.
(function () {
  var form = document.getElementById('sz');
  if (!form) return;
  var $ = function (id) { return document.getElementById(id); };
  var num = (window.THB && THB.num) || function (n) { return Number(n).toLocaleString('en-US'); };
  var STYLES = {};
  try { STYLES = JSON.parse($('sz-style-data').textContent); } catch (e) { STYLES = {}; }

  var REFS = [
    { name: 'Tiny house on wheels', note: '8.5 x 24 ft trailer', lo: 0, hi: 204, label: '204 sq ft' },
    { name: 'IRC Appendix AQ tiny house', note: 'Code definition, lofts excluded', lo: 0, hi: 400, label: 'up to 400 sq ft' },
    { name: 'Typical ADU', note: 'Common local size caps', lo: 400, hi: 800, label: '400-800 sq ft', range: true },
    { name: 'Tiny Homes Blueprint plans', note: '20 x 38 ft footprint', lo: 0, hi: 700, label: '700 sq ft' }
  ];
  var WHEEL_LENGTHS = [16, 18, 20, 22, 24, 26, 28, 30, 32];
  var FOOTPRINTS = [[10, 16], [12, 16], [12, 20], [12, 24], [14, 24], [16, 24], [16, 28], [16, 32], [20, 30], [20, 38], [24, 32], [24, 40]];

  function val(n) { var el = form.elements[n]; return el ? el.value : null; }
  function add(a, b, k) { k = k || 1; return [a[0] + b[0] * k, a[1] + b[1] * k]; }
  function mul(a, k) { return [a[0] * k, a[1] * k]; }
  function r10(n) { return Math.round(n / 10) * 10; }
  function clampInput(el, write) {
    var v = Math.round(+el.value), mn = +el.min, mx = +el.max;
    if (el.value === '' || isNaN(v)) v = mn;
    v = Math.max(mn, Math.min(mx, v));
    if (write && el.value !== String(v)) el.value = v;
    return v;
  }

  function calc(e) {
    var write = !e || e.type !== 'input';
    var adults = clampInput($('sz-adults'), write), kids = clampInput($('sz-kids'), write);
    var people = adults + kids;
    var pets = +val('pets'), wfh = val('wfh'), cook = val('cook'), store = val('store');
    var guests = val('guests'), part = val('occ') === 'part', wheels = val('mob') === 'wheels';
    form.querySelectorAll('[data-step]').forEach(function (b) {
      var el = $(b.dataset.for), v = +el.value;
      b.disabled = b.dataset.step < 0 ? v <= +el.min : v >= +el.max;
    });

    var sleepAdults = adults === 1 ? [45, 70] : [65, 100];
    if (adults > 2) sleepAdults = add(sleepAdults, [50, 80], adults - 2);
    var sleepKids = mul([30, 55], kids);
    var kitchen = { light: [25, 35], daily: [40, 60], serious: [60, 90] }[cook];
    if (people > 2) kitchen = add(kitchen, [5, 10], people - 2);
    var bath = people >= 4 ? [45, 70] : [30, 45];
    var living = [40, 70];
    if (people > 2) living = add(living, [15, 25], people - 2);
    living = add(living, { rare: [0, 0], some: [10, 20], often: [25, 45] }[guests]);
    living = add(living, [[0, 0], [5, 10], [10, 20]][Math.min(pets, 2)]);
    var work = { none: [0, 0], some: [10, 20], full: [30, 60] }[wfh];
    var storage = { min: [15, 25], avg: [25, 45], lots: [55, 90] }[store];
    storage = add(storage, [8, 15], people - 1);
    if (part) { kitchen = mul(kitchen, 0.85); storage = mul(storage, 0.6); living = mul(living, 0.9); }

    var zones = [
      ['Sleeping', add(sleepAdults, sleepKids), adults + ' adult' + (adults > 1 ? 's' : '') + (kids ? ', ' + kids + ' child' + (kids > 1 ? 'ren' : '') : '')],
      ['Kitchen', kitchen], ['Bathroom', bath], ['Living & dining', living],
      ['Work space', work], ['Storage', storage]
    ];
    var sub = [0, 0];
    zones.forEach(function (z) { sub = add(sub, z[1]); });
    var circ = mul(sub, 0.10);
    zones.push(['Walls & circulation', circ]);
    var tot = [r10(sub[0] + circ[0]), r10(sub[1] + circ[1])];
    var mid = (tot[0] + tot[1]) / 2;

    $('sz-total').textContent = num(tot[0]) + ' - ' + num(tot[1]) + ' sq ft';
    $('sz-sub').textContent = (wheels ? 'Total living space including sleeping lofts, ' : 'Total heated floor area, ') + (part ? 'part-time use' : 'full-time living');

    var maxZ = 1;
    zones.forEach(function (z) { maxZ = Math.max(maxZ, z[1][1]); });
    $('sz-zones').innerHTML = zones.filter(function (z) { return z[1][1] > 0; }).map(function (z) {
      var lo = r10(z[1][0]) || Math.round(z[1][0]), hi = r10(z[1][1]) || Math.round(z[1][1]);
      return '<li><span>' + z[0] + '</span><b>' + lo + ' - ' + hi + ' sq ft</b><div class="bar"><i style="width:' + ((z[1][0] + z[1][1]) / 2 / maxZ * 100).toFixed(1) + '%"></i></div></li>';
    }).join('');

    var flags = [], fpTxt, fpLbl, mainTxt, mainLbl;
    if (wheels) {
      // Adults' beds go in the loft (with the loft roughly the size of the sleeping zone).
      var loft = [r10(sleepAdults[0] * 1.1), r10(sleepAdults[1] * 1.1)];
      var main = [tot[0] - loft[0], tot[1] - loft[1]];
      var mainMid = (main[0] + main[1]) / 2;
      var len = null;
      for (var i = 0; i < WHEEL_LENGTHS.length; i++) if (WHEEL_LENGTHS[i] * 8.5 >= mainMid) { len = WHEEL_LENGTHS[i]; break; }
      fpTxt = len ? '8.5 x ' + len + ' ft' : '8.5 x 32+ ft';
      fpLbl = len ? 'trailer, about ' + Math.round(len * 8.5) + ' sq ft main floor' : 'longer than most tiny house trailers';
      mainTxt = num(main[0]) + '-' + num(main[1]) + ' + ' + loft[0] + '-' + loft[1];
      mainLbl = 'sq ft main floor + sleeping loft';
      if (!len || mainMid > 255) flags.push(['bad', '<strong>That is a lot of house for a trailer.</strong> Above about 32 ft, trailers get heavy and hard to tow and park. Consider a gooseneck with a raised bedroom, two lofts, or a foundation home such as an <a href="/adu-plans/">ADU</a>.']);
      if (kids > 0) flags.push(['', 'Kids usually get a second loft or bunk nook on wheels. Their ' + r10(sleepKids[0]) + '-' + r10(sleepKids[1]) + ' sq ft of sleeping space is counted on the main floor here.']);
    } else {
      var fp = null;
      for (var j = 0; j < FOOTPRINTS.length; j++) if (FOOTPRINTS[j][0] * FOOTPRINTS[j][1] >= mid) { fp = FOOTPRINTS[j]; break; }
      fp = fp || FOOTPRINTS[FOOTPRINTS.length - 1];
      fpTxt = fp[0] + ' x ' + fp[1] + ' ft';
      fpLbl = 'footprint, ' + fp[0] * fp[1] + ' sq ft';
      mainTxt = tot[1] <= 400 ? 'Yes' : mid <= 400 ? 'Borderline' : 'No';
      mainLbl = 'under the 400 sq ft IRC tiny house limit';
      if (adults + kids >= 3) flags.push(['', 'With ' + people + ' people, a separate bedroom for kids or a second loft makes daily life much easier. ' + (mid > 450 ? 'Our <a href="/plans/plan-12-2418/">3-bedroom 700 sq ft plan</a> is designed for this.' : 'See <a href="/tiny-house-plans-with-loft/">plans with a loft</a>.')]);
    }
    if (wfh === 'full') flags.push(['', 'Full-time remote work: plan a dedicated desk spot with a door or partition if anyone else is home during the day.']);
    if (part && !flags.length) flags.push(['good', 'For weekend or seasonal use you can lean toward the low end of the range.']);

    $('sz-fp').textContent = fpTxt; $('sz-fp-l').textContent = 'suggested ' + fpLbl;
    $('sz-main').textContent = mainTxt; $('sz-main-l').textContent = mainLbl;
    $('sz-flags').innerHTML = flags.map(function (f) { return '<li' + (f[0] ? ' class="' + f[0] + '"' : '') + '>' + f[1] + '</li>'; }).join('');

    // Comparison chart.
    var max = Math.max(900, Math.ceil(tot[1] * 1.1 / 100) * 100);
    var rows = [{ name: 'Your recommended size', note: wheels ? 'incl. lofts' : 'heated floor area', lo: tot[0], hi: tot[1], label: num(tot[0]) + '-' + num(tot[1]) + ' sq ft', range: true, you: true }].concat(REFS);
    $('sz-compare').innerHTML = rows.map(function (r) {
      var l = r.lo / max * 100, w = (r.hi - r.lo) / max * 100;
      var end = l + w, inside = end > 62;
      var pos = inside ? 'right:' + (100 - end).toFixed(1) + '%;padding:0 8px 0 0;' + (r.range && !r.you ? '' : 'color:#fff') : 'left:' + end.toFixed(1) + '%';
      return '<div class="compare-row' + (r.you ? ' you' : '') + '"><span>' + r.name + '<small>' + r.note + '</small></span>' +
        '<div class="compare-track" role="img" aria-label="' + r.name + ': ' + r.label + '"><i class="' + (r.range && !r.you ? 'range' : '') + '" style="left:' + l.toFixed(1) + '%;width:' + w.toFixed(1) + '%"></i>' +
        '<em style="' + pos + '">' + r.label + '</em></div></div>';
    }).join('');
    var ax = '';
    for (var t = 0; t <= 4; t++) ax += '<span>' + num(max * t / 4) + '</span>';
    $('sz-axis').innerHTML = ax;

    // Style suggestions.
    var picks;
    if (wheels) {
      picks = [['tiny-house-on-wheels-plans', 'Built around 8.5 ft width, 13.5 ft height and trailer weight limits.'],
        ['tiny-house-plans-with-loft', 'Lofts are how a ' + fpTxt + ' house fits real beds.'],
        mid > 380 ? ['adu-plans', 'If the trailer gets too long, a backyard ADU gives you room to spread out.'] : ['shipping-container-home-plans', 'A 20 or 40 ft container can be trucked to a new site if you need to move later.']];
    } else if (mid <= 320) {
      picks = [['small-cabin-plans', 'Simple cabins in the 200-400 sq ft range are easy to frame and heat.'],
        ['a-frame-house-plans', 'An A-frame adds a big sleeping loft under the roof without a bigger footprint.'],
        ['shed-to-tiny-house', 'At this size, converting a well-built shed can be the cheapest route.']];
    } else if (mid <= 520) {
      picks = [['tiny-cottage-plans', 'Cottage layouts at 300-600 sq ft fit a real bedroom and a porch.'],
        ['small-cabin-plans', 'A 16 x 24 or 20 x 30 cabin suits this size well.'],
        kids ? ['tiny-house-plans-with-loft', 'A loft gives kids their own sleeping space.'] : ['adu-plans', 'This size works as a backyard ADU in many cities.']];
    } else {
      picks = [['adu-plans', 'Most ADU limits fall between 400 and 800 sq ft, right in your range.'],
        ['small-farmhouse-plans', 'Farmhouse layouts add a mudroom and porch for rural living.'],
        ['small-cabin-plans', 'Our 700 sq ft cabin plans have 2 or 3 bedrooms on a 20 x 38 ft footprint.']];
    }
    $('sz-styles').innerHTML = picks.map(function (p) {
      var s = STYLES[p[0]]; if (!s) return '';
      return '<a class="style-pick" href="' + s.url + '"><span class="link-ico">' + s.icon + '</span><strong>' + s.name + '</strong><span>' + p[1] + '</span></a>';
    }).join('');
  }

  form.addEventListener('click', function (e) {
    var b = e.target.closest('[data-step]');
    if (!b) return;
    var el = $(b.dataset.for);
    el.value = Math.max(+el.min, Math.min(+el.max, (+el.value || 0) + +b.dataset.step));
    calc();
  });
  form.addEventListener('input', calc);
  form.addEventListener('change', calc);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  calc();
})();
