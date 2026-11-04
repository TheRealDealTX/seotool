(function () {
  var form = document.getElementById('bonus-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var LIMIT = 1000000; // supplemental wages over $1M in a calendar year: mandatory 37% withholding

  /* Pub 15-T style aggregate method: withhold on (regular + bonus) for one pay period, minus withholding on regular pay alone.
     The standard deduction stands in for the built-in allowance of the annual percentage-method tables. */
  function aggregate(per, extra, freq, s, yr) {
    var d = C.year(yr), std = d.std[s];
    var t = function (w) { return C.bracketTax(Math.max(0, w * freq - std), s, yr).tax / freq; };
    return Math.max(0, t(per + extra) - t(per));
  }

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr), method = C.str(f, 'method') || 'flat';
    var bonus = v('bonus'), salary = v('salary'), freq = +C.str(f, 'freq') || 26, ytd = v('ytdSupp');
    var sup = d.supplemental;
    var k401 = Math.min(bonus * C.clamp(v('k401Pct'), 0, 100) / 100, d.k401);
    var taxable = Math.max(0, bonus - k401);           // 401(k) deferrals escape income-tax withholding, not FICA
    var room = Math.max(0, LIMIT - ytd);
    var under = Math.min(taxable, room), over = Math.max(0, taxable - room);
    var fedUnder = method === 'aggregate' ? aggregate(salary / freq, under, freq, s, yr) : under * sup.rate;
    var fedOver = over * sup.over1mRate;
    var fed = fedUnder + fedOver;
    var base = d.ssWageBase, addlT = d.addlMedicare.single; // employers withhold 0.9% once wages pass $200,000, any status
    var ss = Math.max(0, Math.min(salary + bonus, base) - Math.min(salary, base)) * 0.062;
    var med = bonus * 0.0145 + (Math.max(0, salary + bonus - addlT) - Math.max(0, salary - addlT)) * 0.009;
    var state = taxable * C.clamp(v('stateRate'), 0, 20) / 100;
    var net = Math.max(0, bonus - fed - ss - med - state - k401);
    var withheldAll = fed + ss + med + state;

    // Actual federal income tax caused by the bonus: tax on salary + bonus minus tax on salary alone.
    var withB = C.estimate({ year: yr, status: s, wages: salary + bonus, pretax: k401 });
    var without = C.estimate({ year: yr, status: s, wages: salary });
    var actual = Math.max(0, withB.incomeTax - without.incomeTax);
    var diff = fed - actual;

    C.big(tool, 'net', net);
    C.set(tool, 'netSub', bonus > 0 ? 'You keep ' + C.pct(net / bonus) + ' of a ' + C.money(bonus) + ' bonus' + (k401 ? ' (plus ' + C.money(k401) + ' to your 401(k))' : '') : 'Enter a bonus amount to start');
    C.set(tool, 'fed', C.money(fed));
    C.set(tool, 'fica', C.money(ss + med));
    C.set(tool, 'state', C.money(state));
    C.set(tool, 'whRate', C.pct(bonus ? withheldAll / bonus : 0));
    C.big(tool, 'actual', actual);
    C.set(tool, 'actualSub', bonus > 0 ? 'Your bonus is taxed at about ' + C.pct(taxable ? actual / taxable : 0) + ' federal (marginal bracket ' + Math.round(withB.marginal * 100) + '%)' : '—');
    var dEl = C.$('[data-out="diff"]', tool);
    if (dEl) {
      dEl.classList.toggle('good', diff >= 0.5);
      dEl.classList.toggle('bad', diff <= -0.5);
    }
    C.big(tool, 'diff', Math.abs(diff));
    C.set(tool, 'diffLabel', Math.abs(diff) < 0.5 ? 'Withholding matches your actual tax' : diff > 0 ? 'Over-withheld: comes back in your refund' : 'Under-withheld: you may owe this at tax time');

    var segs = [
      { label: 'Federal income tax withheld', value: fed, color: '#0e7490' },
      { label: 'Social Security & Medicare', value: ss + med, color: '#f59e0b' },
      { label: 'State tax withheld', value: state, color: '#8b5cf6' },
      { label: '401(k) contribution', value: k401, color: '#6366f1' },
      { label: 'Net bonus', value: net, color: '#10b981' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [['Gross bonus', C.money(bonus)]];
    if (k401) rows.push(['401(k) deferral (' + v('k401Pct') + '%)', '−' + C.money(k401)]);
    if (method === 'aggregate') rows.push(['Federal withholding (aggregate method)', '−' + C.money(fedUnder)]);
    else rows.push(['Federal withholding (' + C.pct(sup.rate, 0) + ' of ' + C.money(under) + ')', '−' + C.money(fedUnder)]);
    if (over) rows.push(['Federal withholding (' + C.pct(sup.over1mRate, 0) + ' of ' + C.money(over) + ' over $1M)', '−' + C.money(fedOver)]);
    rows.push(['Social Security (6.2%' + (ss < bonus * 0.062 - 0.5 ? ', capped at ' + C.money(base) : '') + ')', '−' + C.money(ss)]);
    rows.push(['Medicare (1.45%' + (med > bonus * 0.0145 + 0.5 ? ' + 0.9%' : '') + ')', '−' + C.money(med)]);
    if (state) rows.push(['State withholding (' + v('stateRate') + '%)', '−' + C.money(state)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Net bonus deposited</span><b>' + C.money(net) + '</b></li>' +
      '<li class="sub"><span>Federal tax on salary alone</span><b>' + C.money(without.incomeTax) + '</b></li>' +
      '<li class="sub"><span>Federal tax on salary + bonus</span><b>' + C.money(withB.incomeTax) + '</b></li>' +
      '<li class="sub"><span>Actual federal tax on the bonus</span><b>' + C.money(actual) + '</b></li>';
  });
})();
