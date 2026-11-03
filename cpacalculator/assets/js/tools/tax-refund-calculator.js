(function () {
  var form = document.getElementById('refund-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var kids = +v('kids') || 0, deps = +v('deps') || 0;
    var itemize = C.str(f, 'dedType') === 'item';
    var r = C.estimate({
      year: yr, status: s, seniors: +v('seniors') || 0,
      wages: v('wages'), seIncome: v('seIncome'), seExpenses: v('seExpenses'), otherIncome: v('otherIncome'),
      otherAdjustments: v('adjust'), itemized: itemize ? v('itemized') : 0,
      tips: v('tips'), overtime: v('overtime')
    });
    // Credits in Form 1040 order: other nonrefundable credits, then CTC/ODC (Schedule 8812), then refundable ACTC.
    var taxBefore = r.incomeTaxBeforeCredits;
    var nonref = Math.min(Math.max(0, v('credits')), taxBefore);
    var t1 = taxBefore - nonref;
    var ctcFull = kids * d.ctc.amount + deps * 500;
    var reduce = Math.ceil(Math.max(0, r.agi - d.ctc.phaseStart[s]) / 1000) * 50;
    var ctcAllowed = Math.max(0, ctcFull - reduce);
    var ctcUsed = Math.min(ctcAllowed, t1);
    var incomeTax = t1 - ctcUsed;
    var seNet = Math.max(0, v('seIncome') - v('seExpenses'));
    var earned = v('wages') + Math.max(0, seNet - r.se.half);
    var actc = kids ? Math.max(0, Math.min(ctcAllowed - ctcUsed, kids * d.ctc.refundable, 0.15 * Math.max(0, earned - 2500))) : 0;
    var totalTax = incomeTax + r.se.total + r.niit;
    var withheld = v('withheld') + v('otherWithheld');
    var refundable = Math.max(0, v('refundable'));
    var paid = withheld + v('estPaid') + actc + refundable;
    var diff = paid - totalTax;
    var refund = diff >= 0;

    C.set(tool, 'label', refund ? 'Estimated refund' : 'Estimated amount you owe');
    C.big(tool, 'result', Math.abs(diff));
    var big = C.$('[data-out="result"]', tool);
    if (big) { big.classList.toggle('good', refund); big.classList.toggle('bad', !refund); }
    var sub = 'Total tax ' + C.money(totalTax) + ' vs. ' + C.money(paid) + ' paid and refundable credits';
    if (!refund && -diff >= 1000 && withheld < totalTax * 0.9) sub += ' · an underpayment penalty may apply';
    C.set(tool, 'sub', sub);
    C.set(tool, 'tax', C.money(totalTax));
    C.set(tool, 'paid', C.money(paid));
    C.set(tool, 'eff', C.pct(r.gross ? totalTax / r.gross : 0));
    C.set(tool, 'marg', Math.round(r.marginal * 100) + '%');

    // Payments vs tax meter
    var max = Math.max(paid, totalTax) || 1;
    var covered = Math.min(paid, totalTax);
    var m = [
      { label: 'Tax covered by payments', value: covered, color: '#0e7490' },
      refund ? { label: 'Overpaid (your refund)', value: diff, color: '#10b981' } : { label: 'Shortfall (you owe)', value: -diff, color: '#e11d48' }
    ];
    C.$('[data-meter]', tool).innerHTML = m.map(function (x) { return '<span style="width:' + (x.value / max * 100) + '%;background:' + x.color + '"></span>'; }).join('');
    C.legend(C.$('[data-meter-legend]', tool), m.filter(function (x) { return x.value > 0; }));

    var itemWasSmaller = itemize && v('itemized') > 0 && !r.usedItemized;
    var rows = [
      ['Total income', C.money(r.gross)],
      ['Adjustments (incl. ½ SE tax)', '−' + C.money(r.gross - r.agi), 1],
      ['Adjusted gross income', C.money(r.agi)],
      [(r.usedItemized ? 'Itemized' : 'Standard') + ' deduction', '−' + C.money(r.deduction), 1]
    ];
    if (r.belowLine) rows.push(['Tips / overtime / senior deduction', '−' + C.money(r.belowLine), 1]);
    if (r.qbi) rows.push(['QBI deduction (20%)', '−' + C.money(r.qbi), 1]);
    rows.push(['Taxable income', C.money(r.taxable)]);
    rows.push(['Tax before credits', C.money(taxBefore)]);
    if (nonref) rows.push(['Other nonrefundable credits', '−' + C.money(nonref), 1]);
    if (ctcUsed) rows.push(['Child / dependent credit', '−' + C.money(ctcUsed), 1]);
    if (r.se.total) rows.push(['Self-employment tax', C.money(r.se.total), 1]);
    if (r.niit) rows.push(['Net investment income tax', C.money(r.niit), 1]);
    rows.push(['Total tax', C.money(totalTax)]);
    rows.push(['Federal withholding', C.money(withheld), 1]);
    if (v('estPaid')) rows.push(['Estimated payments', C.money(v('estPaid')), 1]);
    if (actc) rows.push(['Additional Child Tax Credit (refundable)', C.money(actc), 1]);
    if (refundable) rows.push(['Other refundable credits', C.money(refundable), 1]);
    rows.push(['Total payments', C.money(paid)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>' + (refund ? 'Refund' : 'Amount owed') + '</span><b>' + C.money(Math.abs(diff)) + '</b></li>';

    var note = '';
    if (itemWasSmaller) note += 'Your itemized deductions are less than the ' + C.money(r.std) + ' standard deduction, so the standard deduction was used. ';
    if ((kids > 0 && r.agi < 71000) || r.agi < 27000) note += 'Your income suggests you may qualify for the Earned Income Tax Credit, which is not included — check the IRS EITC Assistant; it would increase your refund. ';
    if (kids >= 3 && actc) note += 'With three or more children, the alternative ACTC formula may give a slightly larger refundable credit. ';
    note += 'Excludes state tax, AMT and the Additional Medicare Tax on wages. ';
    var el = C.$('[data-out="note"]', tool);
    if (el) el.innerHTML = note + '<a href="/our-methodology/">Methodology</a>.';
  });
})();
