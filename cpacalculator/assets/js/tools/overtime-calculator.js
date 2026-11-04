(function () {
  var form = document.getElementById('ot-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = +v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var rate = v('rate'), reg = v('regHours'), h15 = v('ot15'), h2 = v('ot2');
    var weeks = C.clamp(v('weeks') || 52, 0, 53), otWeeks = C.clamp(v('otWeeks'), 0, weeks);
    var flsa = v('flsa'), dtOver40 = v('dtOver40');

    // Weekly pay
    var regPay = rate * reg, pay15 = rate * 1.5 * h15, pay2 = rate * 2 * h2, otPay = pay15 + pay2;
    // Only FLSA overtime (hours over 40 in the workweek) counts, and only the half-time premium on those hours.
    var over40 = Math.max(0, reg + h15 + h2 - 40);
    var qualHours = flsa ? Math.min(h15 + (dtOver40 ? h2 : 0), over40) : 0;
    var qualWeek = qualHours * rate * 0.5;
    var straightWeek = rate * (h15 + h2);

    // Annual
    var regAnnual = regPay * weeks, otAnnual = otPay * otWeeks;
    var annual = regAnnual + otAnnual;
    var qualified = qualWeek * otWeeks;
    var nonQual = Math.max(0, otAnnual - straightWeek * otWeeks - qualified);
    var magi = v('magi') > 0 ? v('magi') : annual;

    // Deduction: cap by status, $100 less per $1,000 of MAGI over the threshold, none for married filing separately, 2025–2028 only.
    var cap = d.overtimeMax[s], po = d.obbbaPhaseOut;
    var phase = Math.max(0, magi - po.start[s]) * po.per1000 / 1000;
    var inYears = yr >= 2025 && yr <= 2028;
    var ded = (s === 'mfs' || !inYears) ? 0 : Math.max(0, Math.min(qualified, cap) - phase);

    var base = C.estimate({ year: yr, status: s, wages: annual });
    var withDed = C.estimate({ year: yr, status: s, wages: annual, overtime: ded });
    var saved = Math.max(0, base.incomeTax - withDed.incomeTax);
    var ficaOt = C.fica(annual, s, yr).total - C.fica(regAnnual, s, yr).total;

    C.big(tool, 'otAnnual', otAnnual);
    C.set(tool, 'otSub', C.money(otPay, 2) + ' overtime per week · ' + C.money(regPay + otPay, 2) + ' total weekly pay');
    C.set(tool, 'otRate', C.money(rate * 1.5, 2) + '/hr');
    C.set(tool, 'dtRate', C.money(rate * 2, 2) + '/hr');
    C.set(tool, 'annual', C.money(annual));
    C.set(tool, 'qual', C.money(qualified));
    C.big(tool, 'saved', saved);
    var why;
    if (s === 'mfs') why = 'Married filing separately can’t claim the overtime deduction; you must file jointly.';
    else if (!inYears) why = 'The deduction applies to tax years 2025 through 2028 only.';
    else if (!flsa) why = 'Only overtime required by the FLSA qualifies — exempt employees don’t get this deduction.';
    else if (!qualified) why = 'No qualified overtime: only hours over 40 in a workweek count.';
    else why = 'Deduction of ' + C.money(ded) + ' on ' + C.money(qualified) + ' of qualified premium' +
      (qualified > cap ? ' (capped at ' + C.money(cap) + ')' : '') + (phase > 0 ? ', reduced ' + C.money(Math.min(phase, Math.min(qualified, cap))) + ' by the MAGI phase-out' : '') +
      ' · ' + Math.round(withDed.marginal * 100) + '% bracket';
    C.set(tool, 'savedSub', why);

    var segs = [
      { label: 'Regular pay', value: regAnnual, color: '#94a3b8' },
      { label: 'Overtime at straight time', value: straightWeek * otWeeks, color: '#0e7490' },
      { label: 'Qualified OT premium (deductible)', value: qualified, color: '#10b981' },
      { label: 'Other OT premium (not deductible)', value: nonQual, color: '#f59e0b' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [
      ['Regular pay (' + reg + ' h × ' + C.money(rate, 2) + ' × ' + weeks + ' wk)', C.money(regAnnual)],
      ['Overtime pay (' + otWeeks + ' wk)', C.money(otAnnual)]
    ];
    if (h15) rows.push(['<span>' + h15 + ' h × ' + C.money(rate * 1.5, 2) + ' (1.5×) per week</span>', C.money(pay15 * otWeeks), 'sub']);
    if (h2) rows.push(['<span>' + h2 + ' h × ' + C.money(rate * 2, 2) + ' (2×) per week</span>', C.money(pay2 * otWeeks), 'sub']);
    rows.push(['Annual gross pay', C.money(annual)]);
    rows.push(['Qualified overtime premium (½ × rate × ' + qualHours + ' h × ' + otWeeks + ' wk)', C.money(qualified)]);
    rows.push(['Deduction limit (' + (s === 'mfj' ? 'joint' : 'per return') + ')', C.money(cap)]);
    if (phase > 0) rows.push(['Phase-out (MAGI ' + C.money(magi) + ' over ' + C.money(po.start[s]) + ')', '−' + C.money(phase)]);
    rows.push(['Overtime deduction (Schedule 1-A)', C.money(ded)]);
    rows.push(['Federal income tax without deduction', C.money(base.incomeTax)]);
    rows.push(['Federal income tax with deduction', C.money(withDed.incomeTax)]);
    rows.push(['Social Security & Medicare on overtime (still owed)', C.money(ficaOt)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0].replace(/<\/?span[^>]*>/g, '') + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Federal tax saved</span><b>' + C.money(saved) + '</b></li>';
  });
})();
