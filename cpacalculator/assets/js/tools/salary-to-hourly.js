(function () {
  var form = document.getElementById('s2h-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;

  function afterTax(annual, o) {
    var k = annual * o.k401;
    var e = C.estimate({ year: o.yr, status: o.s, wages: annual, pretax: k });
    var state = Math.max(0, annual - k) * o.state;
    var net = Math.max(0, annual - e.incomeTax - e.fica.total - state - k);
    return { fed: e.incomeTax, fica: e.fica.total, state: state, k401: k, net: net, marginal: e.marginal };
  }
  /* Net after tax for 1099 income of G (no benefits, pays full SE tax, QBI applies). */
  function net1099(G, o) {
    var e = C.estimate({ year: o.yr, status: o.s, seIncome: G });
    return G - e.incomeTax - e.se.total - Math.max(0, G - e.se.half) * o.state;
  }

  try {
    if (new URLSearchParams(location.search).get('mode') === 'toSalary') {
      var tb = C.$('[data-tab="toSalary"]', tool); if (tb) tb.click();
    }
  } catch (e) {}
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var toSalary = !C.$('[data-panel="toSalary"]', f).hidden;
    f.elements.mode.value = toSalary ? 'toSalary' : 'toHourly';
    var o = { yr: v('year'), s: C.str(f, 'status'), state: C.clamp(v('state'), 0, 20) / 100, k401: C.clamp(v('k401'), 0, 100) / 100 };
    var H = C.clamp(v('hours') || 40, 1, 100), unpaid = C.clamp(v('unpaid'), 0, 51), pto = C.clamp(v('pto'), 0, 200);
    var W = 52 - unpaid;
    var hourly, annual, ot = 0;
    if (toSalary) {
      hourly = v('hourly');
      ot = v('ot');
      annual = hourly * H * W + hourly * 1.5 * ot * W;
    } else {
      annual = v('salary');
      hourly = W > 0 && H > 0 ? annual / (H * W) : 0;
    }
    var workedWeeks = Math.max(1, W - pto / 5);
    var trueHourly = annual / ((H + ot) * workedWeeks);
    var t = afterTax(annual, o), ratio = annual > 0 ? t.net / annual : 0;

    C.set(tool, 'bigLabel', toSalary ? 'Annual salary' : 'Hourly wage');
    C.big(tool, 'big', toSalary ? annual : hourly, toSalary ? null : function (n) { return C.money(n, 2); });
    C.set(tool, 'summary', toSalary
      ? C.money(hourly, 2) + '/hr × ' + H + ' hrs × ' + W + ' weeks' + (ot ? ' + ' + ot + ' overtime hrs/week at 1.5×' : '')
      : C.money(annual) + ' ÷ (' + H + ' hrs × ' + W + ' weeks = ' + (H * W).toLocaleString() + ' paid hours)');
    C.set(tool, 'kAnnual', C.money(annual));
    C.set(tool, 'kNet', C.money(t.net));
    C.set(tool, 'kNetHr', C.money(hourly * ratio, 2));
    C.set(tool, 'kTrue', C.money(trueHourly, 2));

    var daily = hourly * H / 5 + (toSalary ? hourly * 1.5 * ot / 5 : 0);
    var weekly = W > 0 ? annual / W : 0;
    var periods = [
      ['Hourly', hourly, 2], ['Daily (' + (H / 5).toFixed(1).replace(/\.0$/, '') + ' hrs)', daily, 2], ['Weekly', weekly, 0],
      ['Biweekly (26/yr)', annual / 26, 0], ['Semimonthly (24/yr)', annual / 24, 0], ['Monthly', annual / 12, 0], ['Annual', annual, 0]
    ];
    C.$('[data-periods]', tool).innerHTML = periods.map(function (p) {
      return '<tr><td>' + p[0] + '</td><td class="n">' + C.money(p[1], p[2]) + '</td><td class="n">' + C.money(p[1] * ratio, p[2]) + '</td></tr>';
    }).join('');

    var segs = [
      { label: 'Federal income tax', value: t.fed, color: '#0e7490' },
      { label: 'Social Security & Medicare', value: t.fica, color: '#f59e0b' },
      { label: 'State tax', value: t.state, color: '#f43f5e' },
      { label: '401(k) contribution', value: t.k401, color: '#6366f1' },
      { label: 'Take-home pay', value: t.net, color: '#10b981' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    // 1099 equivalent: contract income that nets the same as W-2 pay + benefits.
    var ben = annual * C.clamp(v('benefits'), 0, 100) / 100;
    var target = t.net + t.k401 + ben, lo = 0, hi = Math.max(1000, annual * 3 + ben * 2);
    for (var i = 0; i < 60; i++) { var mid = (lo + hi) / 2; if (net1099(mid, o) < target) lo = mid; else hi = mid; }
    var G = annual > 0 ? hi : 0;
    var billable = (H + ot) * Math.max(1, 52 - unpaid - pto / 5), avgHr = annual / ((H + ot) * Math.max(1, W));
    C.$('[data-c1099]', tool).innerHTML =
      '<li><span>W-2 take-home + 401(k) + benefits (' + C.money(ben) + ')</span><b>' + C.money(target) + '</b></li>' +
      '<li><span>1099 income needed to match</span><b>' + C.money(G) + '</b></li>' +
      '<li class="sub"><span>Billable hours (' + (H + ot) + ' × ' + Math.max(1, 52 - unpaid - pto / 5).toFixed(1).replace(/\.0$/, '') + ' wks, no paid time off)</span><b>' + Math.round(billable).toLocaleString() + '</b></li>' +
      '<li class="total"><span>Equivalent 1099 hourly rate</span><b>' + C.money(G / billable, 2) + '</b></li>';
    C.set(tool, 'c1099note', annual > 0 ? 'A contractor would need about ' + C.pct(avgHr > 0 ? G / billable / avgHr - 1 : 0, 0) + ' more per hour than the W-2 rate to come out even, after self-employment tax, lost benefits and unpaid time off.' : '—');
  });
})();
