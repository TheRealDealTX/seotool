(function () {
  var form = document.getElementById('scorp-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;

  /* §199A with the taxable-income phase-in: W-2 wage limit (50% of wages) and SSTB phase-out.
     OBBBA widened the phase-in range to $75,000 / $150,000 (joint) starting in 2026. */
  function qbiDed(qbiInc, wages, before, s, yr, sstb) {
    qbiInc = Math.max(0, qbiInc);
    var T = C.year(yr).qbiThreshold[s];
    var R = (s === 'mfj' ? 2 : 1) * (+yr >= 2026 ? 75000 : 50000);
    var phase = C.clamp((before - T) / R, 0, 1);
    var inc = sstb ? qbiInc * (1 - phase) : qbiInc, w = sstb ? wages * (1 - phase) : wages;
    var tent = 0.2 * inc, lim = Math.min(tent, 0.5 * w);
    var ded = phase <= 0 ? tent : (phase >= 1 ? lim : tent - (tent - lim) * phase);
    return Math.max(0, Math.min(ded, before * 0.2));
  }
  function sole(o) {
    var se = C.seTax(o.profit, o.s, o.yr, 0);
    var agi = Math.max(0, o.profit + o.other - se.half);
    var before = Math.max(0, agi - C.stdDeduction(o.s, o.yr));
    var q = qbiDed(o.profit - se.half, 0, before, o.s, o.yr, o.sstb);
    var taxable = Math.max(0, before - q), it = C.bracketTax(taxable, o.s, o.yr);
    var state = agi * o.state;
    return { se: se.total, agi: agi, qbi: q, taxable: taxable, income: it.tax, marginal: it.marginal, state: state, total: se.total + it.tax + state };
  }
  function scorp(o) {
    var d = C.year(o.yr), sal = Math.max(0, o.salary);
    var er = Math.min(sal, d.ssWageBase) * 0.062 + sal * 0.0145;
    var ee = C.fica(sal, o.s, o.yr).total;
    var k1 = o.profit - sal - er - o.costs;
    var agi = Math.max(0, sal + k1 + o.other);
    var before = Math.max(0, agi - C.stdDeduction(o.s, o.yr));
    var q = qbiDed(k1, sal, before, o.s, o.yr, o.sstb);
    var taxable = Math.max(0, before - q), it = C.bracketTax(taxable, o.s, o.yr);
    var state = agi * o.state;
    return { er: er, ee: ee, payroll: er + ee, k1: k1, agi: agi, qbi: q, taxable: taxable, income: it.tax, marginal: it.marginal, state: state,
      taxes: er + ee + it.tax + state, total: er + ee + it.tax + state + o.costs };
  }

  function neg(x) { return x > 0 ? '−' + C.money(x) : '$0'; }
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var o = { yr: v('year'), s: C.str(f, 'status'), profit: v('profit'), salary: v('salary'), other: v('other'),
      state: C.clamp(v('state'), 0, 20) / 100, costs: v('costs'), sstb: !!v('sstb') };
    var a = sole(o), b = scorp(o), save = a.total - b.total;
    var bigEl = C.$('[data-out="save"]', tool);
    bigEl.className = 'res-big ' + (save >= 0 ? 'good' : 'bad');
    C.set(tool, 'saveLabel', save >= 0 ? 'Estimated annual S corp savings' : 'S corp would cost you more');
    C.big(tool, 'save', Math.abs(save));
    C.set(tool, 'summary', o.profit > 0 ? (save >= 0
      ? 'About ' + C.pct(save / o.profit) + ' of profit, or ' + C.money(save / 12) + ' a month, after ' + C.money(o.costs) + ' of extra S corp costs.'
      : 'At this profit and salary, payroll and compliance costs outweigh the self-employment tax saved.') : 'Enter your net business profit.');
    C.set(tool, 'soleTotal', C.money(a.total));
    C.set(tool, 'scorpTotal', C.money(b.total));
    C.set(tool, 'payrollSaved', C.money(a.se - b.payroll));
    // Break-even profit at the same salary-to-profit ratio
    var ratio = o.profit > 0 ? C.clamp(o.salary / o.profit, 0, 1) : 0.5, be = null;
    for (var p = 5000; p <= 1000000; p += 1000) {
      var oo = Object.assign({}, o, { profit: p, salary: p * ratio });
      if (sole(oo).total - scorp(oo).total > 0) { be = p; break; }
    }
    C.set(tool, 'breakeven', be ? '≈ ' + C.money(be) : 'none ≤ $1M');

    // Comparison table
    var r = [
      ['Net business profit', C.money(o.profit), C.money(o.profit)],
      ['Owner salary (W-2)', '—', C.money(o.salary)],
      ['K-1 distribution', '—', C.money(b.k1)],
      ['Self-employment tax', C.money(a.se), '—'],
      ['Employer payroll tax (7.65%)', '—', C.money(b.er)],
      ['Employee FICA withheld', '—', C.money(b.ee)],
      ['QBI deduction', neg(a.qbi), neg(b.qbi)],
      ['Taxable income', C.money(a.taxable), C.money(b.taxable)],
      ['Federal income tax', C.money(a.income), C.money(b.income)]
    ];
    if (o.state) r.push(['State income tax', C.money(a.state), C.money(b.state)]);
    r.push(['Extra S corp costs', '—', C.money(o.costs)]);
    C.$('[data-compare]', tool).innerHTML = r.map(function (x) { return '<tr><td>' + x[0] + '</td><td class="n">' + x[1] + '</td><td class="n">' + x[2] + '</td></tr>'; }).join('') +
      '<tr><td><strong>Total cost</strong></td><td class="n"><strong>' + C.money(a.total) + '</strong></td><td class="n"><strong>' + C.money(b.total) + '</strong></td></tr>';

    // Meter: S corp total vs sole prop total
    var mx = Math.max(a.total, b.total, 1);
    C.$('[data-meter-a]', tool).style.width = (a.total / mx * 100) + '%';
    C.$('[data-meter-b]', tool).style.width = (b.total / mx * 100) + '%';

    // Salary sensitivity
    C.$('[data-sens]', tool).innerHTML = [0.3, 0.4, 0.5, 0.6, 0.7].map(function (pc) {
      var oo = Object.assign({}, o, { salary: o.profit * pc }), sv = sole(oo).total - scorp(oo).total;
      return '<li><span>Salary ' + Math.round(pc * 100) + '% of profit (' + C.money(oo.salary) + ')</span><b>' + C.money(sv) + '</b></li>';
    }).join('');

    // Warnings
    var w = [];
    if (o.salary > o.profit) w.push('Your salary is higher than the business profit — the S corp would show a loss.');
    else if (o.profit > 0 && o.salary < o.profit * 0.3) w.push('A salary under ~30% of profit is a common IRS audit flag. Base it on what you’d pay someone else to do your job.');
    if (b.k1 < 0 && o.salary <= o.profit) w.push('Salary + employer payroll tax + costs exceed profit, so the K-1 shows a loss.');
    if (o.salary > C.year(o.yr).ssWageBase) w.push('Salary above the ' + C.money(C.year(o.yr).ssWageBase) + ' Social Security wage base saves little extra payroll tax.');
    if (!w.length) w.push('Payroll tax is saved only on the K-1 distribution (' + C.money(Math.max(0, b.k1)) + '). Your salary is still subject to the full 15.3% FICA.');
    C.set(tool, 'warn', w.join(' '));
  });
})();
