(function () {
  var form = document.getElementById('se-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var net = v('profit') + v('farm') + v('k1');
    var ssWages = Math.max(0, v('wages'));
    var medRaw = C.str(f, 'medWages');
    var medWages = medRaw === '' ? ssWages : Math.max(0, v('medWages'));
    var base = Math.max(0, net) * 0.9235;
    var below = base < 400;
    var room = Math.max(0, d.ssWageBase - ssWages);
    var ssBase = below ? 0 : Math.min(base, room);
    var ss = ssBase * 0.124;
    var med = below ? 0 : base * 0.029;
    var addlTh = d.addlMedicare[s];
    var addl = below ? 0 : Math.max(0, base - Math.max(0, addlTh - medWages)) * 0.009;
    var se = ss + med, half = se / 2;

    // Income tax value of the ½ SE deduction (engine already includes it; add it back to compare).
    var withDed = C.estimate({ year: yr, status: s, wages: ssWages, seIncome: Math.max(0, net) });
    var noDed = C.estimate({ year: yr, status: s, wages: ssWages, seIncome: Math.max(0, net), otherAdjustments: -withDed.se.half });
    var saved = Math.max(0, noDed.incomeTax - withDed.incomeTax);

    C.big(tool, 'se', se);
    C.set(tool, 'ss', C.money(ss));
    C.set(tool, 'med', C.money(med));
    C.set(tool, 'half', C.money(half));
    C.set(tool, 'eff', C.pct(net > 0 ? (se + addl) / net : 0, 2));
    C.set(tool, 'wb', C.money(d.ssWageBase));
    var sub;
    if (net <= 0) sub = 'No self-employment tax on a net loss.';
    else if (below) sub = 'Net SE earnings of ' + C.money(base) + ' are under $400 — no SE tax owed.';
    else sub = (addl > 0 ? 'Plus ' + C.money(addl) + ' Additional Medicare Tax (Form 8959) · ' : '') + 'Set aside ' + C.money((se + addl) / 4) + ' per quarter';
    C.set(tool, 'sub', sub);

    // Wage-base meter
    var wb = d.ssWageBase;
    var wPart = Math.min(ssWages, wb), sPart = Math.min(ssBase, wb - wPart), left = Math.max(0, wb - wPart - sPart);
    var m = [
      { label: 'W-2 Social Security wages', value: wPart, color: '#6366f1' },
      { label: 'Self-employment earnings taxed 12.4%', value: sPart, color: '#f59e0b' },
      { label: 'Wage base left', value: left, color: '#e2e8f0' }
    ];
    C.$('[data-meter]', tool).innerHTML = m.map(function (x) { return '<span style="width:' + (x.value / wb * 100) + '%;background:' + x.color + '"></span>'; }).join('');
    C.legend(C.$('[data-meter-legend]', tool), m.filter(function (x) { return x.value > 0; }));

    var keep = Math.max(0, net - se - addl);
    var segs = [
      { label: 'Social Security', value: ss, color: '#f59e0b' },
      { label: 'Medicare', value: med, color: '#0e7490' },
      { label: 'Additional Medicare', value: addl, color: '#e11d48' },
      { label: 'Profit after SE tax', value: keep, color: '#10b981' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [];
    rows.push(['Schedule C net profit', C.money(v('profit'))]);
    if (v('farm')) rows.push(['Schedule F farm profit', C.money(v('farm')), 1]);
    if (v('k1')) rows.push(['Partnership SE earnings', C.money(v('k1')), 1]);
    rows.push(['Net SE earnings (× 92.35%)', C.money(base)]);
    if (ssWages) rows.push(['Wage base left after W-2 wages', C.money(room), 1]);
    rows.push(['Social Security: 12.4% × ' + C.money(ssBase), C.money(ss), 1]);
    rows.push(['Medicare: 2.9% × ' + C.money(below ? 0 : base), C.money(med), 1]);
    rows.push(['Schedule SE tax', C.money(se)]);
    if (addl > 0) rows.push(['Additional Medicare 0.9% (Form 8959)', C.money(addl)]);
    rows.push(['Deduction for ½ SE tax (Schedule 1)', '−' + C.money(half)]);
    rows.push(['Income tax saved by that deduction', '≈ ' + C.money(saved), 1]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Total SE + Additional Medicare</span><b>' + C.money(se + addl) + '</b></li>';
  });
})();
