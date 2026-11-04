(function () {
  var form = document.getElementById('estate-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;

  /* Unified transfer tax (IRC §2001(c)) from tax.json estate.brackets. */
  function unified(amt, br) {
    var tax = 0, prev = 0;
    for (var i = 0; i < br.length; i++) {
      var top = br[i][0] == null ? Infinity : br[i][0];
      if (amt > prev) tax += (Math.min(amt, top) - prev) * br[i][1];
      prev = top;
    }
    return tax;
  }
  var maritalInput = form.elements.marital;

  CPA.bind(form, function (f) {
    var v = function (n) { return Math.max(0, C.val(f, n)); };
    var yr = C.val(f, 'year'), d = C.year(yr), br = d.estate.brackets, exempt = d.estate.exemption;
    var assets = [
      ['Home & real estate', v('home')], ['Bank & investments', v('invest')], ['Retirement accounts', v('retire')],
      ['Life insurance', v('life')], ['Business interests', v('biz')], ['Other assets', v('other')]
    ];
    var gross = assets.reduce(function (a, x) { return a + x[1]; }, 0);
    var debts = v('debts'), expenses = v('expenses');
    var net = Math.max(0, gross - debts - expenses);
    var charity = Math.min(v('charity'), net);
    var allSpouse = !!C.val(f, 'allSpouse');
    maritalInput.disabled = allSpouse;
    var marital = allSpouse ? net - charity : Math.min(v('marital'), net - charity);
    if (allSpouse) maritalInput.value = Math.round(marital).toLocaleString('en-US');
    var taxableEstate = Math.max(0, net - charity - marital);
    var gifts = v('gifts'), dsue = Math.min(v('dsue'), exempt);
    var base = taxableEstate + gifts;
    var tentative = unified(base, br);
    var available = exempt + dsue;
    var credit = unified(available, br);
    var tax = Math.max(0, tentative - credit);
    var eff = gross > 0 ? tax / gross : 0;
    var unused = Math.max(0, exempt - base); // DSUE the surviving spouse could receive (basic exclusion only)

    var big = C.$('[data-out="tax"]', tool);
    big.classList.toggle('good', tax < 0.5);
    big.classList.toggle('bad', tax >= 0.5);
    C.big(tool, 'tax', tax);
    var sum;
    if (tax >= 0.5) sum = C.money(base - available) + ' over the ' + C.money(available) + ' exemption, taxed at 40%.';
    else if (marital > 0 && unused > 0) sum = 'No federal estate tax. Elect portability on Form 706 to pass ' + C.money(unused) + ' of unused exemption to your spouse.';
    else sum = 'No federal estate tax — the estate is ' + C.money(available - base) + ' under the exemption.';
    C.set(tool, 'summary', sum);
    C.set(tool, 'gross', C.money(gross));
    C.set(tool, 'taxable', C.money(taxableEstate));
    C.set(tool, 'eff', C.pct(eff));
    if (marital > 0) { C.set(tool, 'kpi4l', 'Portable to spouse (DSUE)'); C.set(tool, 'kpi4', C.money(unused)); }
    else { C.set(tool, 'kpi4l', 'Exemption available'); C.set(tool, 'kpi4', C.money(available)); }

    var toHeirs = Math.max(0, gross - debts - expenses - charity - marital - tax);
    var segs = [
      { label: 'Debts & expenses', value: Math.min(gross, debts + expenses), color: '#94a3b8' },
      { label: 'To spouse', value: marital, color: '#0e7490' },
      { label: 'To charity', value: charity, color: '#6366f1' },
      { label: 'Federal estate tax', value: tax, color: '#e11d48' },
      { label: 'To other heirs', value: toHeirs, color: '#10b981' }
    ].filter(function (x) { return x.value > 0.5; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [];
    assets.forEach(function (a) { if (a[1]) rows.push([a[0], C.money(a[1]), 'sub']); });
    rows.push(['Gross estate', C.money(gross)]);
    rows.push(['Debts & mortgages', '−' + C.money(debts), 'sub']);
    rows.push(['Funeral & administration', '−' + C.money(expenses), 'sub']);
    if (marital) rows.push(['Marital deduction', '−' + C.money(marital), 'sub']);
    if (charity) rows.push(['Charitable deduction', '−' + C.money(charity), 'sub']);
    rows.push(['Taxable estate', C.money(taxableEstate)]);
    rows.push(['+ Adjusted taxable gifts', C.money(gifts)]);
    rows.push(['Tax base', C.money(base)]);
    rows.push(['Tentative tax (18%–40%)', C.money(tentative)]);
    rows.push(['Exemption ' + C.money(exempt) + (dsue ? ' + DSUE ' + C.money(dsue) : ''), C.money(available), 'sub']);
    rows.push(['Applicable credit', '−' + C.money(Math.min(credit, tentative))]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Federal estate tax</span><b>' + C.money(tax) + '</b></li>';
  });
})();
