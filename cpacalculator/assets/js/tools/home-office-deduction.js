(function () {
  var form = document.getElementById('ho-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var own = C.str(f, 'housing') !== 'rent';
    C.$$('[data-when]', f).forEach(function (el) { var off = el.dataset.when !== (own ? 'own' : 'rent'); el.hidden = off; el.style.display = off ? 'none' : ''; });

    var office = Math.max(0, v('office')), home = Math.max(0, v('home'));
    var pct = home > 0 ? C.clamp(office / home, 0, 1) : 0;
    var profit = Math.max(0, v('profit'));

    // Simplified: $rate × up to 300 sq ft, limited to business profit, no carryover.
    var simpleRaw = Math.min(300, office) * d.homeOfficeSimplifiedRate;
    var simple = Math.min(simpleRaw, profit);

    // Regular method (Form 8829 tiers).
    var interest = own ? v('interest') * pct : 0, ptax = own ? v('ptax') * pct : 0;
    var rent = own ? 0 : v('rent') * pct;
    var ins = v('ins') * pct, util = v('util') * pct, rep = v('repairs') * pct, hoa = own ? v('hoa') * pct : 0, direct = v('direct');
    var depBase = own ? Math.max(0, v('basis') - v('land')) * pct : 0;
    var m = +C.str(f, 'first') || 0;
    var depFrac = m ? (12 - m + 0.5) / 12 / 39 : 1 / 39; // mid-month convention in year one
    var dep = depBase * depFrac;
    var t1 = interest + ptax;
    var t2Raw = rent + ins + util + rep + hoa + direct;
    var t2 = Math.min(t2Raw, Math.max(0, profit - t1));
    var t3 = Math.min(dep, Math.max(0, profit - t1 - t2));
    var regular = t1 + t2 + t3;
    var carry = (t2Raw - t2) + (dep - t3);

    var best = Math.max(simple, regular), regWins = regular > simple;
    var w = v('wages');
    var base = C.estimate({ year: yr, status: s, wages: w, seIncome: profit });
    var withDed = C.estimate({ year: yr, status: s, wages: w, seIncome: profit, seExpenses: best });
    var save = Math.max(0, base.totalFederal - withDed.totalFederal);

    C.big(tool, 'best', best);
    C.set(tool, 'simple', C.money(simple));
    C.set(tool, 'regular', C.money(regular));
    C.set(tool, 'pct', C.pct(pct));
    C.set(tool, 'save', C.money(save));
    C.set(tool, 'winner', best <= 0 ? 'Enter your office size and business profit to compare methods' :
      (regular === simple ? 'Both methods give the same deduction' :
      (regWins ? 'Regular method wins by ' : 'Simplified method wins by ') + C.money(Math.abs(regular - simple)) + ' · saves ≈ ' + C.money(save) + ' in federal tax'));

    var tot = simple + regular || 1;
    C.$('[data-meter]', tool).innerHTML = '<span style="width:' + (simple / tot * 100) + '%;background:#f59e0b" title="Simplified ' + C.money(simple) + '"></span><span style="width:' + (regular / tot * 100) + '%;background:#0e7490" title="Regular ' + C.money(regular) + '"></span>';

    var segs = [
      { label: own ? 'Mortgage interest & property tax' : 'Rent', value: own ? t1 : Math.min(rent, t2), color: '#0e7490' },
      { label: 'Insurance, utilities, repairs' + (own ? ', HOA' : '') + ', direct', value: own ? t2 : Math.max(0, t2 - Math.min(rent, t2)), color: '#6366f1' },
      { label: 'Depreciation', value: t3, color: '#10b981' },
      { label: 'Carried forward', value: carry, color: '#cbd5e1' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [['Business-use % (' + office.toLocaleString() + ' ÷ ' + home.toLocaleString() + ' sq ft)', C.pct(pct, 2)]];
    rows.push(['Simplified: ' + Math.min(300, office).toLocaleString() + ' sq ft × $' + d.homeOfficeSimplifiedRate, C.money(simpleRaw)]);
    if (simple < simpleRaw) rows.push(['Limited to business profit', C.money(simple), 'sub']);
    if (own) { rows.push(['Mortgage interest (business share)', C.money(interest), 'sub']); rows.push(['Real estate taxes (business share)', C.money(ptax), 'sub']); }
    else rows.push(['Rent (business share)', C.money(rent), 'sub']);
    rows.push(['Insurance', C.money(ins), 'sub']);
    rows.push(['Utilities', C.money(util), 'sub']);
    if (rep) rows.push(['Repairs & maintenance', C.money(rep), 'sub']);
    if (hoa) rows.push(['HOA fees', C.money(hoa), 'sub']);
    if (direct) rows.push(['Direct office expenses (100%)', C.money(direct), 'sub']);
    if (own) rows.push(['Depreciation (' + C.money(depBase) + ' ÷ 39' + (m ? ', mid-month' : '') + ')', C.money(dep), 'sub']);
    if (carry > 0.5) rows.push(['Over income limit — carried to next year', C.money(carry)]);
    rows.push(['Regular method (Form 8829)', C.money(regular)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Best deduction (' + (regWins ? 'regular' : 'simplified') + ')</span><b>' + C.money(best) + '</b></li>';

    C.set(tool, 'limitnote', (carry > 0.5 || simple < simpleRaw ? 'Your deduction is capped by business profit (gross-income limitation). ' : '') +
      'Estimate only — tax savings include federal income tax and self-employment tax at your ' + Math.round(withDed.marginal * 100) + '% bracket; state tax not included.' + (own ? ' Under the regular method, the business share of mortgage interest and property tax moves off Schedule A.' : ''));
  });
})();
