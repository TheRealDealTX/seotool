(function () {
  var form = document.getElementById('pay-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var freqName = { 52: 'weekly', 26: 'biweekly', 24: 'semimonthly', 12: 'monthly', 1: 'annual' };
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var n = +C.str(f, 'freq') || 26;
    var basis = C.str(f, 'basis');
    var g = Math.max(0, v('gross'));
    var gross = basis === 'period' ? g * n : basis === 'hour' ? g * Math.max(0, v('hours')) * 52 : g;

    // Pre-tax deductions (annual)
    var limit = d.k401 + (C.val(f, 'catchup') ? d.k401CatchUp : 0);
    var k401Want = C.str(f, 'k401Type') === 'amt' ? Math.max(0, v('k401')) * n : gross * C.clamp(v('k401'), 0, 100) / 100;
    var k401 = Math.min(k401Want, limit, gross);
    var health = Math.max(0, v('health')) * n;
    var hsa = Math.max(0, v('hsa')) * n;
    var s125 = Math.min(health + hsa, gross);
    var fedWages = Math.max(0, gross - k401 - s125);
    var ficaWages = Math.max(0, gross - s125);

    // Federal withholding — Pub 15-T percentage method for 2020+ W-4, annualized.
    var step2 = C.val(f, 'step2');
    var std = C.stdDeduction(s, yr, 0);
    var adj = fedWages + Math.max(0, v('otherInc')) - Math.max(0, v('w4ded')) - (step2 ? std / 2 : std);
    var tent = step2 ? C.bracketTax(2 * Math.max(0, adj), s, yr).tax / 2 : C.bracketTax(adj, s, yr).tax;
    var fed = Math.max(0, tent - Math.max(0, v('dep'))) + Math.max(0, v('extra')) * n;

    // FICA: employer withholds Additional Medicare on wages over $200,000 regardless of filing status.
    var ss = Math.min(ficaWages, d.ssWageBase) * 0.062;
    var med = ficaWages * 0.0145;
    var addl = Math.max(0, ficaWages - 200000) * 0.009;
    var fica = ss + med + addl;
    var state = fedWages * C.clamp(v('state'), 0, 20) / 100;
    var post = Math.max(0, v('post')) * n;
    var net = gross - k401 - s125 - fed - fica - state - post;

    C.big(tool, 'net', net / n, function (x) { return C.money(x, 2); });
    var nm = freqName[n] || '';
    C.set(tool, 'sub', gross > 0 ? (n > 1 ? 'Per ' + nm + ' paycheck · ' : '') + C.money(net / 12) + ' per month · from ' + C.money(gross / n, 2) + ' gross' + (n > 1 ? ' per check' : '') : 'Enter your pay to start');
    C.set(tool, 'netA', C.money(net));
    C.set(tool, 'fed', C.money(fed / n, 2));
    C.set(tool, 'fica', C.money(fica / n, 2));
    C.set(tool, 'rate', C.pct(gross ? (fed + fica + state) / gross : 0));
    var big = C.$('[data-out="net"]', tool);
    if (big) { big.classList.toggle('good', net >= 0); big.classList.toggle('bad', net < 0); }

    var segs = [
      { label: 'Take-home pay', value: net, color: '#10b981' },
      { label: 'Federal income tax', value: fed, color: '#0e7490' },
      { label: 'Social Security & Medicare', value: fica, color: '#f59e0b' },
      { label: 'State income tax', value: state, color: '#e11d48' },
      { label: '401(k) & HSA savings', value: k401 + Math.min(hsa, s125), color: '#6366f1' },
      { label: 'Health premiums', value: Math.max(0, s125 - hsa), color: '#94a3b8' },
      { label: 'After-tax deductions', value: post, color: '#a855f7' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var lines = [['Gross pay', gross, 0]];
    if (k401) lines.push(['Traditional 401(k)', -k401, 1]);
    if (health) lines.push(['Health, dental & vision', -Math.min(health, s125), 1]);
    if (hsa) lines.push(['HSA / FSA', -Math.max(0, s125 - health), 1]);
    lines.push(['Federal taxable wages', fedWages, 2]);
    lines.push(['Federal income tax', -fed, 1]);
    lines.push(['Social Security (6.2%)', -ss, 1]);
    lines.push(['Medicare (1.45%' + (addl ? ' + 0.9%' : '') + ')', -(med + addl), 1]);
    if (state) lines.push(['State income tax (' + C.clamp(v('state'), 0, 20) + '%)', -state, 1]);
    if (post) lines.push(['After-tax deductions', -post, 1]);
    var cell = function (x) { return (x < 0 ? '−' : '') + C.money(Math.abs(x), 2); };
    C.$('[data-table]', tool).innerHTML = lines.map(function (l) {
      var lab = l[2] === 2 ? '<em>' + l[0] + '</em>' : l[0];
      return '<tr><td>' + lab + '</td><td class="n">' + cell(l[1] / n) + '</td><td class="n">' + C.money(l[1]) + '</td></tr>';
    }).join('') + '<tr><td><strong>Take-home pay</strong></td><td class="n"><strong>' + C.money(net / n, 2) + '</strong></td><td class="n"><strong>' + C.money(net) + '</strong></td></tr>';

    var note = 'Federal withholding follows the IRS percentage method for 2020-and-later W-4s, annualized. ';
    if (k401Want > k401 + 0.5 && k401 === limit) note += '401(k) capped at the ' + C.money(limit) + ' annual limit. ';
    if (ficaWages > d.ssWageBase) note += 'Social Security stops once wages pass ' + C.money(d.ssWageBase) + '; per-check figures are yearly averages. ';
    if (hsa && hsa > d.hsa.family) note += 'HSA entry exceeds the ' + C.money(d.hsa.family) + ' family limit. ';
    var el = C.$('[data-out="note"]', tool);
    if (el) el.innerHTML = note + 'Actual paychecks can differ slightly due to rounding and employer setup. <a href="/our-methodology/">Methodology</a>.';
  });
})();
