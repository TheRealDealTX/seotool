/* Solar vs wired cost calculator */
(function () {
  'use strict';
  SC.init('cost', function (form, box) {
    var o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
    var n = Math.max(1, Math.round(SC.num(form, 'n', 4))), Y = SC.num(form, 'y', 5), run = SC.num(form, 'run', 60);
    var trench = SC.num(form, 'route', 0) === 1, pro = SC.num(form, 'pro', 0) === 1;
    var sp = SC.num(form, 'sp', 150), sub = SC.num(form, 'sub', 0), bat = SC.num(form, 'bat', 40);
    var wp = SC.num(form, 'wp', 110), nvr = SC.num(form, 'nvr', 250), kwh = SC.num(form, 'kwh', 0.17), tr = SC.num(form, 'tr', 8);
    // Solar
    var sUp = n * sp + (pro ? n * 60 : 0) + n * 12; // + mounting hardware/microSD
    var sYear = function (y) { return sub * 12 + (y > 0 && y % 3 === 0 ? n * bat : 0); };
    // Wired
    var cable = n * run * (0.40 + (trench ? 0.60 : 0));
    var dig = trench ? n * run * tr * (pro ? 1.8 : 1) : 0;
    var labor = pro ? n * 150 : n * 15; // DIY: connectors, clips, drill bits
    var wUp = n * wp + nvr + cable + dig + labor;
    var wPowerYear = (n * 6 + 15) * 24 * 365 / 1000 * kwh;
    var wYear = function (y) { return wPowerYear + (y > 0 && y % 5 === 0 ? 90 : 0); }; // drive replacement ~5 yrs
    var sp_ = [[0, sUp]], wp_ = [[0, wUp]], s = sUp, w = wUp;
    for (var y = 1; y <= Y; y++) { s += sYear(y); w += wYear(y); sp_.push([y, s]); wp_.push([y, w]); }
    var cheaper = s < w ? 'Solar' : 'Wired', diff = Math.abs(w - s);
    o('win').innerHTML = SC.money(diff) + ' <small>saved</small>';
    o('sum').innerHTML = '<strong>' + cheaper + '</strong> is cheaper over ' + Y + ' years for ' + n + ' camera' + (n > 1 ? 's' : '') + ' with ' + run + ' ft runs' + (trench ? ' (trenched)' : '') + '. Wired still wins on 24/7 recording; solar wins on install effort and flexibility.';
    o('s').textContent = SC.money(s); o('w').textContent = SC.money(w);
    o('s1').textContent = SC.money(s / n); o('w1').textContent = SC.money(w / n);
    var ymax = Math.max(s, w) * 1.1, step = Math.pow(10, Math.floor(Math.log10(ymax))) / 2;
    var ticks = []; for (var t = 0; t <= ymax; t += step) ticks.push(Math.round(t));
    if (ticks.length > 6) ticks = ticks.filter(function (_, i) { return i % 2 === 0; });
    SC.lineChart(o('chart'), {
      xmin: 0, xmax: Y, ymin: 0, ymax: ymax, yticks: ticks, h: 200, label: 'Cumulative cost solar vs wired',
      xticks: sp_.map(function (p) { return [p[0], p[0] === 0 ? 'Install' : 'Yr ' + p[0]]; }),
      series: [{ pts: sp_, color: '#f97316' }, { pts: wp_, color: '#1d4ed8' }]
    });
    o('chart').querySelectorAll('text').forEach(function (t) { if (/^\d+$/.test(t.textContent)) t.textContent = '$' + (t.textContent >= 1000 ? Math.round(t.textContent / 100) / 10 + 'k' : t.textContent); });
    var parts = [['Cameras + NVR', n * wp + nvr], ['Cable' + (trench ? ' + conduit' : ''), cable], ['Trenching', dig], [pro ? 'Installer' : 'DIY supplies', labor], ['Electricity (' + Y + ' yr)', wPowerYear * Y]];
    var mx = Math.max.apply(null, parts.map(function (p) { return p[1]; })) || 1;
    o('bars').innerHTML = parts.filter(function (p) { return p[1] > 0; }).map(function (p) { return '<div class="b"><span>' + p[0] + '</span><i style="--w:' + (p[1] / mx * 100).toFixed(0) + '%"></i><span>' + SC.money(p[1]) + '</span></div>'; }).join('');
  });
})();
