(function () {
  var form = document.getElementById('t1099-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var tips = {
    general: 'Common write-offs for freelancers: software, equipment, a home office, phone, internet, professional fees and business travel.',
    gig: 'Drivers: mileage is usually your biggest deduction — log every business mile, plus phone, tolls, parking and platform fees.',
    creator: 'Creators & sellers: platform and payment fees, cost of goods sold, shipping, cameras, lighting, editing software and props.',
    physician: 'Medical 1099s: licenses, DEA registration, CME, malpractice insurance, board fees, travel to locums assignments and a Solo 401(k).',
    realestate: 'Agents: MLS and board dues, broker desk fees, marketing, staging, mileage between showings and your license renewals.',
    consultant: 'Consultants & IT: computers, software subscriptions, co-working, certifications, home office and client travel.'
  };
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var tipEl = document.getElementById('work-tip'); if (tipEl) tipEl.textContent = tips[C.str(f, 'work')] || tips.general;
    var mileage = v('miles') * d.mileage;
    var office = Math.min(300, v('sqft')) * d.homeOfficeSimplifiedRate;
    var phone = v('phone') * 12 * C.clamp(v('phonePct'), 0, 100) / 100;
    var net = v('internet') * 12 * C.clamp(v('internetPct'), 0, 100) / 100;
    var guided = mileage + office + phone + net;
    var expenses = v('expenses') + guided;
    var income = v('income');
    var r = C.estimate({ year: yr, status: s, wages: v('wages'), seIncome: income, seExpenses: expenses, otherAdjustments: v('health') + v('retire') });
    var total = r.incomeTax + r.se.total + r.niit;
    // Tax attributable to the 1099 income = total minus tax on the W-2 job alone.
    var w2only = v('wages') ? C.estimate({ year: yr, status: s, wages: v('wages') }) : null;
    var on1099 = total - (w2only ? w2only.incomeTax : 0);
    var owed = Math.max(0, total - v('withheld') - v('paid'));
    C.big(tool, 'total', total);
    C.set(tool, 'se', C.money(r.se.total));
    C.set(tool, 'inc', C.money(r.incomeTax + r.niit));
    C.set(tool, 'eff', C.pct(income ? on1099 / income : 0));
    C.set(tool, 'marg', Math.round(r.marginal * 100) + '%');
    var pct = income > 0 ? Math.max(0, on1099) / income : 0;
    C.set(tool, 'setaside', income > 0 ? 'Set aside about ' + C.pct(pct, 0) + ' of each 1099 payment (' + C.money(on1099) + ' on your 1099 income)' : 'Enter your 1099 income to start');
    var q = d.quarterlyDue, per = owed / 4;
    C.set(tool, 'qlabel', (v('withheld') || v('paid')) ? 'Remaining balance split across quarters' : 'Quarterly estimated payments');
    C.$('[data-quarters]', tool).innerHTML = q.map(function (date, i) { return '<div><small>Q' + (i + 1) + ' · ' + date + '</small><b>' + C.money(per) + '</b></div>'; }).join('');
    var keep = Math.max(0, income - expenses - on1099);
    var segs = [
      { label: 'Self-employment tax', value: r.se.total, color: '#f59e0b' },
      { label: 'Income tax on 1099 income', value: Math.max(0, on1099 - r.se.total), color: '#0e7490' },
      { label: 'Business expenses', value: expenses, color: '#6366f1' },
      { label: 'You keep', value: keep, color: '#10b981' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);
    var rows = [['1099 gross income', C.money(income)], ['Business expenses', '−' + C.money(v('expenses'))]];
    if (guided) {
      rows.push(['Guided write-offs found', '−' + C.money(guided)]);
      if (mileage) rows.push(['<span class="sub">Mileage (' + v('miles').toLocaleString() + ' mi × ' + (d.mileage * 100).toFixed(1) + '¢)</span>', C.money(mileage), 'sub']);
      if (office) rows.push(['Home office (simplified)', C.money(office), 'sub']);
      if (phone + net) rows.push(['Phone & internet', C.money(phone + net), 'sub']);
    }
    rows.push(['Net profit (Schedule C)', C.money(Math.max(0, income - expenses))]);
    rows.push(['SE tax base (× 92.35%)', C.money(r.se.base)]);
    rows.push(['Social Security (12.4%)', C.money(r.se.ss), 'sub']);
    rows.push(['Medicare (2.9% + 0.9%)', C.money(r.se.medicare + r.se.addl), 'sub']);
    rows.push(['Deduction for ½ SE tax', '−' + C.money(r.se.half)]);
    if (v('health') + v('retire')) rows.push(['Health insurance + retirement', '−' + C.money(v('health') + v('retire'))]);
    rows.push(['Standard deduction', '−' + C.money(r.deduction)]);
    rows.push(['QBI deduction (20%)', '−' + C.money(r.qbi)]);
    rows.push(['Taxable income', C.money(r.taxable)]);
    if (v('withheld') || v('paid')) rows.push(['Withholding + payments made', '−' + C.money(v('withheld') + v('paid'))]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0].replace(/<\/?span[^>]*>/g, '') + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>' + ((v('withheld') || v('paid')) ? 'Still owed' : 'Total federal tax') + '</span><b>' + C.money((v('withheld') || v('paid')) ? owed : total) + '</b></li>';
  });
})();
