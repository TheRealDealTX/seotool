(function () {
  var form = document.getElementById('grossup-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var LIMIT = 1000000;

  function aggregate(per, extra, freq, s, yr) {
    var d = C.year(yr), std = d.std[s];
    var t = function (w) { return C.bracketTax(Math.max(0, w * freq - std), s, yr).tax / freq; };
    return Math.max(0, t(per + extra) - t(per));
  }

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr), sup = d.supplemental;
    var target = v('net'), method = C.str(f, 'method') || 'flat';
    var salary = v('salary'), freq = +C.str(f, 'freq') || 26, ytd = v('ytdWages');
    var stateR = C.clamp(v('stateRate'), 0, 20) / 100, fica = v('fica');
    var aggBox = C.$('[data-agg-only]', form); if (aggBox) aggBox.hidden = method !== 'aggregate';
    var base = d.ssWageBase, addlT = d.addlMedicare.single;

    function taxes(G) {
      var under = Math.min(G, LIMIT), over = Math.max(0, G - LIMIT);
      var fed = (method === 'aggregate' ? aggregate(salary / freq, under, freq, s, yr) : under * sup.rate) + over * sup.over1mRate;
      var ss = fica ? Math.max(0, Math.min(ytd + G, base) - Math.min(ytd, base)) * 0.062 : 0;
      var med = fica ? G * 0.0145 + (Math.max(0, ytd + G - addlT) - Math.max(0, ytd - addlT)) * 0.009 : 0;
      var st = G * stateR;
      return { fed: fed, ss: ss, med: med, state: st, total: fed + ss + med + st, net: G - fed - ss - med - st };
    }
    // Net is increasing in gross (combined marginal rate < 100%), so a binary search finds the exact gross.
    var lo = target, hi = Math.max(1, target) * 2;
    while (taxes(hi).net < target && hi < 1e12) hi *= 2;
    for (var i = 0; i < 100; i++) { var mid = (lo + hi) / 2; if (taxes(mid).net < target) lo = mid; else hi = mid; }
    var gross = target > 0 ? Math.round(hi * 100) / 100 : 0;
    var t = taxes(gross);

    C.big(tool, 'gross', gross, function (n) { return C.money(n, 2); });
    C.set(tool, 'grossSub', target > 0 ? 'Pay ' + C.money(gross, 2) + ' so the employee receives ' + C.money(target, 2) + ' — a gross-up of ' + C.money(gross - target, 2) : 'Enter the net amount to start');
    C.set(tool, 'fed', C.money(t.fed, 2));
    C.set(tool, 'fica', C.money(t.ss + t.med, 2));
    C.set(tool, 'state', C.money(t.state, 2));
    C.set(tool, 'rate', C.pct(gross ? t.total / gross : 0, 2));

    var flatRate = sup.rate + (fica ? (ytd + gross <= base ? 0.0765 : 0) : 0) + stateR;
    var simple = method === 'flat' && gross <= LIMIT && (!fica || (ytd + gross <= base && ytd + gross <= addlT));
    C.set(tool, 'formula', simple
      ? 'Gross = ' + C.money(target, 2) + ' ÷ (1 − ' + C.pct(flatRate, 2) + ') = ' + C.money(gross, 2)
      : 'Solved iteratively: gross − taxes(gross) = ' + C.money(target, 2) + ' → gross = ' + C.money(gross, 2) +
        (method === 'aggregate' ? ' (aggregate withholding depends on salary)' : ' (wage base or $1M threshold crossed)'));

    var segs = [
      { label: 'Federal income tax', value: t.fed, color: '#0e7490' },
      { label: 'Social Security & Medicare', value: t.ss + t.med, color: '#f59e0b' },
      { label: 'State income tax', value: t.state, color: '#8b5cf6' },
      { label: 'Net to employee', value: t.net, color: '#10b981' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [['Gross payment', C.money(gross, 2)]];
    rows.push(['Federal withholding (' + (method === 'aggregate' ? 'aggregate method' : C.pct(sup.rate, 0) + (gross > LIMIT ? ' / ' + C.pct(sup.over1mRate, 0) + ' over $1M' : '')) + ')', '−' + C.money(t.fed, 2)]);
    if (fica) {
      rows.push(['Social Security (6.2%' + (t.ss < gross * 0.062 - 0.005 ? ', wage base ' + C.money(base) + ' reached' : '') + ')', '−' + C.money(t.ss, 2)]);
      rows.push(['Medicare (1.45%' + (t.med > gross * 0.0145 + 0.005 ? ' + 0.9% additional' : '') + ')', '−' + C.money(t.med, 2)]);
    }
    if (t.state) rows.push(['State tax (' + C.pct(stateR, 2) + ')', '−' + C.money(t.state, 2)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Net to employee</span><b>' + C.money(t.net, 2) + '</b></li>' +
      '<li class="sub"><span>Gross-up amount (taxes covered)</span><b>' + C.money(gross - target, 2) + '</b></li>';
  });
})();
