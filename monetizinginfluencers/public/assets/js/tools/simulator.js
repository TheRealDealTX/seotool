/* Creator Income Stream Simulator */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var form = $('sim-form');
  if (!form) return;
  var C = 2 * Math.PI * 80, NS = 'http://www.w3.org/2000/svg';
  var S = [
    { k: 'brand', name: 'Brand deals', color: '#29b6f6', f: function (g) { return g('brand_n') * g('brand_r'); } },
    { k: 'aff', name: 'Affiliate', color: '#8b5cf6', f: function (g) { return g('aff_c') * g('aff_cv') / 100 * g('aff_cm'); } },
    { k: 'ads', name: 'Ad revenue', color: '#ff3d9a', f: function (g) { return g('ads_v') / 1000 * g('ads_rpm'); } },
    { k: 'prod', name: 'Digital products', color: '#ffcc33', f: function (g) { return g('prod_s') * g('prod_p'); } },
    { k: 'mem', name: 'Memberships', color: '#2ee59d', f: function (g) { return g('mem_n') * g('mem_p'); } },
    { k: 'ugc', name: 'UGC videos', color: '#ff8a3d', f: function (g) { return g('ugc_n') * g('ugc_r'); } }
  ];
  var PRESETS = {
    starter: { brand_n: 1, brand_r: 250, aff_c: 1500, aff_cv: 2.5, aff_cm: 5, ads_v: 60000, ads_rpm: 2, prod_s: 0, prod_p: 19, mem_n: 0, mem_p: 5, ugc_n: 2, ugc_r: 150 },
    growing: { brand_n: 3, brand_r: 600, aff_c: 6000, aff_cv: 3, aff_cm: 8, ads_v: 400000, ads_rpm: 3.5, prod_s: 40, prod_p: 29, mem_n: 120, mem_p: 6, ugc_n: 3, ugc_r: 300 },
    pro: { brand_n: 6, brand_r: 2500, aff_c: 30000, aff_cv: 3.5, aff_cm: 12, ads_v: 2500000, ads_rpm: 6, prod_s: 220, prod_p: 49, mem_n: 1200, mem_p: 8, ugc_n: 0, ugc_r: 500 },
    zero: { brand_n: 0, brand_r: 0, aff_c: 0, aff_cv: 0, aff_cm: 0, ads_v: 0, ads_rpm: 0, prod_s: 0, prod_p: 0, mem_n: 0, mem_p: 0, ugc_n: 0, ugc_r: 0 }
  };

  var donut = $('sim-donut'), arcs = {};
  S.forEach(function (s) {
    var c = document.createElementNS(NS, 'circle');
    c.setAttribute('cx', 100); c.setAttribute('cy', 100); c.setAttribute('r', 80);
    c.setAttribute('stroke', s.color); c.style.strokeDasharray = '0 ' + C; c.style.strokeDashoffset = 0;
    donut.appendChild(c); arcs[s.k] = c;
  });

  function g(id) { return parseFloat($(id).value) || 0; }
  function money(n) { return '$' + Math.round(n).toLocaleString(); }
  function fmtOut(input) {
    var o = $(input.id + '-o'), u = o.dataset.unit, n = parseFloat(input.value);
    o.textContent = u === '$' ? '$' + n.toLocaleString() : u === '%' ? n.toFixed(1) + '%' : (window.MI ? MI.fmtNum(n) : n);
  }
  var shown = 0;
  function tweenTotal(to) {
    var from = shown, t0 = null; shown = to;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { $('sim-month').textContent = money(to); return; }
    (function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 700, 1), e = 1 - Math.pow(1 - p, 3);
      $('sim-month').textContent = money(from + (to - from) * e);
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  var lastBand = '';
  function update() {
    form.querySelectorAll('input[type=range]').forEach(fmtOut);
    var vals = S.map(function (s) { return Math.max(0, s.f(g)); });
    var total = vals.reduce(function (a, b) { return a + b; }, 0);
    tweenTotal(total);
    $('sim-year').textContent = money(total * 12);

    var offset = 0, active = 0, hhi = 0, legend = $('sim-legend');
    legend.innerHTML = '';
    S.forEach(function (s, i) {
      var share = total ? vals[i] / total : 0, len = share * C;
      $('g-' + s.k).textContent = money(vals[i]) + '/mo';
      arcs[s.k].style.strokeDasharray = Math.max(0, len - (share > 0 && share < 1 ? 2 : 0)) + ' ' + C;
      arcs[s.k].style.strokeDashoffset = -offset;
      offset += len;
      if (vals[i] > 0) active++;
      hhi += share * share;
      var li = document.createElement('li');
      li.innerHTML = '<i style="background:' + s.color + '"></i>' + s.name + '<b>' + Math.round(share * 100) + '%</b>';
      legend.appendChild(li);
    });
    $('sim-streams').textContent = active;
    var score = total ? Math.round((1 - hhi) / (1 - 1 / S.length) * 100) : 0;
    $('sim-score').textContent = score + '/100';
    $('sim-meter').style.width = score + '%';
    var band, msg;
    if (!total) { band = 'none'; msg = 'Add some income to see your diversification score.'; }
    else if (score < 30) { band = 'low'; msg = 'Highly concentrated: one stream drives almost everything. A platform change or lost client could cut your income overnight. Add a second stream next.'; }
    else if (score < 60) { band = 'mid'; msg = 'Moderately diversified. You have a backup, but one stream still dominates. Grow an owned stream like products or memberships.'; }
    else { band = 'high'; msg = 'Well diversified. Losing any single stream would hurt, not sink you. Focus on growing your highest-margin streams.'; }
    $('sim-verdict').textContent = msg;
    if (band === 'high' && lastBand && lastBand !== 'high' && window.MI) MI.confetti(90);
    lastBand = band;
  }

  function applyPreset(name) {
    var p = PRESETS[name];
    Object.keys(p).forEach(function (id) { $(id).value = p[id]; });
    document.querySelectorAll('[data-preset]').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.preset === name); });
    update();
  }
  document.querySelectorAll('[data-preset]').forEach(function (b) { b.addEventListener('click', function () { applyPreset(b.dataset.preset); }); });
  form.addEventListener('input', function () {
    document.querySelectorAll('[data-preset]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
    update();
  });
  applyPreset('starter');
})();
