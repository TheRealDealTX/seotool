(function () {
  var form = document.getElementById('tips-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = +v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var tips = v('cashTips') + v('cardTips'), wages = v('wages');
    var se = v('selfEmployed'), seExp = se ? v('seExp') : 0;
    var seBox = C.$('[data-se-only]', form); if (seBox) seBox.hidden = !se;
    var occ = v('occupation'), ssn = v('ssn');

    var gross = wages + tips;
    var magi = v('magi') > 0 ? v('magi') : Math.max(0, gross - seExp);
    var po = d.obbbaPhaseOut;
    var phase = Math.max(0, magi - po.start[s]) * po.per1000 / 1000;
    var limit = se ? Math.max(0, tips - seExp) : tips;          // self-employed: can't exceed net income from the tipped business
    var inYears = yr >= 2025 && yr <= 2028;
    var eligible = s !== 'mfs' && occ && ssn && inYears;
    var ded = eligible ? Math.max(0, Math.min(limit, d.tipsMax) - phase) : 0;

    var opts = function (extra) {
      var o = se ? { year: yr, status: s, wages: wages, seIncome: tips, seExpenses: seExp } : { year: yr, status: s, wages: gross };
      for (var k in extra) o[k] = extra[k];
      return o;
    };
    var without = C.estimate(opts({}));
    var withDed = C.estimate(opts({ tips: ded }));
    var noTips = C.estimate({ year: yr, status: s, wages: wages });
    var saved = Math.max(0, without.incomeTax - withDed.incomeTax);
    var payroll = se ? withDed.se.total : C.fica(gross, s, yr).total - C.fica(wages, s, yr).total;
    var incOnTips = Math.max(0, withDed.incomeTax - noTips.incomeTax);
    var kept = Math.max(0, tips - seExp - payroll - incOnTips);

    C.big(tool, 'saved', saved);
    var why;
    if (!tips) why = 'Enter your tips to start';
    else if (s === 'mfs') why = 'Married filing separately can’t claim the tips deduction; you must file jointly.';
    else if (!inYears) why = 'The deduction applies to tax years 2025 through 2028 only.';
    else if (!occ) why = 'Only tips in an occupation on the IRS list of customarily tipped jobs qualify.';
    else if (!ssn) why = 'You need a Social Security number valid for employment on your return.';
    else why = 'Deduction of ' + C.money(ded) + ' on ' + C.money(tips) + ' of tips' +
      (limit > d.tipsMax ? ' (capped at ' + C.money(d.tipsMax) + ')' : '') +
      (se && limit < tips ? ' (limited to net business income)' : '') +
      (phase > 0 ? ', reduced ' + C.money(Math.min(phase, Math.min(limit, d.tipsMax))) + ' by the MAGI phase-out' : '') +
      ' · ' + Math.round(without.marginal * 100) + '% bracket before the deduction';
    C.set(tool, 'savedSub', why);
    C.set(tool, 'tips', C.money(tips));
    C.set(tool, 'ded', C.money(ded));
    C.set(tool, 'payroll', C.money(payroll));
    C.set(tool, 'payrollLabel', se ? 'Self-employment tax' : 'Social Security & Medicare on tips');
    C.set(tool, 'incOnTips', C.money(incOnTips));

    var segs = [
      { label: 'Federal income tax on tips', value: incOnTips, color: '#0e7490' },
      { label: se ? 'Self-employment tax' : 'Social Security & Medicare', value: payroll, color: '#f59e0b' },
      { label: 'Business expenses', value: seExp, color: '#6366f1' },
      { label: 'Tips you keep (before state tax)', value: kept, color: '#10b981' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [
      ['Cash tips', C.money(v('cashTips'))],
      ['Card / electronic tips', C.money(v('cardTips'))],
      ['Wages (excluding tips)', C.money(wages)]
    ];
    if (se) rows.push(['Business expenses (self-employed)', '−' + C.money(seExp)]);
    rows.push(['Modified AGI used for phase-out', C.money(magi)]);
    rows.push(['Tips deduction limit', C.money(d.tipsMax)]);
    if (phase > 0) rows.push(['Phase-out (over ' + C.money(po.start[s]) + ')', '−' + C.money(phase)]);
    rows.push(['Tips deduction (Schedule 1-A)', C.money(ded)]);
    rows.push(['Taxable income without deduction', C.money(without.taxable)]);
    rows.push(['Taxable income with deduction', C.money(withDed.taxable)]);
    rows.push(['Federal income tax without deduction', C.money(without.incomeTax)]);
    rows.push(['Federal income tax with deduction', C.money(withDed.incomeTax)]);
    rows.push([(se ? 'Self-employment tax' : 'FICA on tips') + ' (not reduced)', C.money(payroll)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Federal income tax saved</span><b>' + C.money(saved) + '</b></li>';
  });
})();
