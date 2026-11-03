(function () {
  var form = document.getElementById('fed-form');
  if (!form) return;
  var tool = form.closest('.tool');
  var C = window.CPA;
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var detailed = !C.$('[data-panel="detailed"]', f).hidden;
    var r = C.estimate({
      year: v('year'), status: C.str(f, 'status'), seniors: +v('seniors') || 0,
      wages: v('wages'),
      seIncome: detailed ? v('seIncome') : 0, seExpenses: detailed ? v('seExpenses') : 0,
      otherIncome: detailed ? v('otherIncome') : 0, stcg: detailed ? v('stcg') : 0, ltcg: detailed ? v('ltcg') : 0,
      pretax: detailed ? v('pretax') : 0, hsa: detailed ? v('hsa') : 0, itemized: detailed ? v('itemized') : 0,
      tips: detailed ? v('tips') : 0, overtime: detailed ? v('overtime') : 0,
      kids: detailed ? +v('kids') || 0 : 0, credits: detailed ? v('credits') : 0
    });
    var payroll = r.fica.total + r.se.total;
    var fedAll = r.incomeTax + r.niit;
    var pretax = detailed ? v('pretax') + v('hsa') : 0;
    var take = Math.max(0, r.gross - fedAll - payroll - pretax);
    C.big(tool, 'tax', fedAll);
    C.set(tool, 'eff', C.pct(r.gross ? fedAll / r.gross : 0));
    C.set(tool, 'marg', Math.round(r.marginal * 100) + '%');
    C.set(tool, 'taxable', C.money(r.taxable));
    C.set(tool, 'summary', 'On ' + C.money(r.gross) + ' of income · take-home ≈ ' + C.money(take) + '/yr (' + C.money(take / 12) + '/mo)');
    var w = v('withheld');
    if (w > 0) {
      var diff = w - (fedAll + r.se.total);
      C.set(tool, 'refundLabel', diff >= 0 ? 'Estimated refund' : 'Estimated amount owed');
      C.set(tool, 'refund', C.money(Math.abs(diff)));
    } else { C.set(tool, 'refundLabel', 'Monthly take-home'); C.set(tool, 'refund', C.money(take / 12)); }
    var segs = [
      { label: 'Federal income tax', value: fedAll, color: '#0e7490' },
      { label: r.se.total ? 'FICA + self-employment tax' : 'Social Security & Medicare', value: payroll, color: '#f59e0b' },
      { label: 'Pre-tax savings', value: pretax, color: '#6366f1' },
      { label: 'Take-home (before state tax)', value: take, color: '#10b981' }
    ].filter(function (s) { return s.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);
    var rows = [
      ['Gross income', C.money(r.gross)],
      ['Adjustments (pre-tax, ½ SE tax)', '−' + C.money(r.gross - r.agi)],
      ['Adjusted gross income (AGI)', C.money(r.agi)],
      [(r.usedItemized ? 'Itemized' : 'Standard') + ' deduction', '−' + C.money(r.deduction)]
    ];
    if (r.belowLine) rows.push(['Tips / overtime / senior deduction', '−' + C.money(r.belowLine)]);
    if (r.qbi) rows.push(['QBI deduction (20%)', '−' + C.money(r.qbi)]);
    rows.push(['Taxable income', C.money(r.taxable)]);
    rows.push(['Tax before credits', C.money(r.incomeTaxBeforeCredits)]);
    if (r.credits) rows.push(['Credits', '−' + C.money(r.credits)]);
    if (r.niit) rows.push(['Net investment income tax (3.8%)', C.money(r.niit)]);
    if (r.se.total) rows.push(['Self-employment tax', C.money(r.se.total)]);
    if (r.fica.total) rows.push(['FICA withheld from wages', C.money(r.fica.total)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Federal income tax</span><b>' + C.money(fedAll) + '</b></li>';
    C.brackets(C.$('[data-brackets]', tool), r.layers);
  });
})();
