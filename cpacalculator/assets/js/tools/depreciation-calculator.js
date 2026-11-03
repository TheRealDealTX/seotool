(function () {
  var form = document.getElementById('dep-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;

  /* IRS Pub. 946 Table A-1 — GDS, half-year convention (percent). */
  var HY = {
    3: [33.33, 44.45, 14.81, 7.41],
    5: [20.00, 32.00, 19.20, 11.52, 11.52, 5.76],
    7: [14.29, 24.49, 17.49, 12.49, 8.93, 8.92, 8.93, 4.46],
    10: [10.00, 18.00, 14.40, 11.52, 9.22, 7.37, 6.55, 6.55, 6.56, 6.55, 3.28],
    15: [5.00, 9.50, 8.55, 7.70, 6.93, 6.23, 5.90, 5.90, 5.91, 5.90, 5.91, 5.90, 5.91, 5.90, 5.91, 2.95],
    20: [3.750, 7.219, 6.677, 6.177, 5.713, 5.285, 4.888, 4.522, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 4.462, 4.461, 2.231]
  };
  /* Section 179 [limit, phase-out threshold] by year placed in service. */
  var S179 = { 2020: [1040000, 2590000], 2021: [1050000, 2620000], 2022: [1080000, 2700000], 2023: [1160000, 2890000], 2024: [1220000, 3050000], 2025: [2500000, 4000000], 2026: [2560000, 4090000] };
  /* Bonus rate for property acquired before Jan 20, 2025 (TCJA phase-down) by year placed in service. */
  var PHASE = { 2020: 100, 2021: 100, 2022: 100, 2023: 80, 2024: 60, 2025: 40, 2026: 20 };

  /* Declining-balance → straight-line MACRS rates (fractions) for any convention fraction of year one. */
  function dbRates(life, factor, firstFrac) {
    var rate = factor ? factor / life : 0, rem = 1, remLife = life, out = [];
    for (var k = 0; rem > 1e-9 && k < life + 2; k++) {
      var dep;
      if (k === 0) { dep = factor ? rem * rate * firstFrac : firstFrac / life; remLife = life - firstFrac; }
      else if (remLife <= 1) dep = rem;
      else { dep = Math.max(factor ? rem * rate : 0, rem / remLife); remLife -= 1; }
      dep = Math.min(dep, rem);
      out.push(dep); rem -= dep;
    }
    return out;
  }
  /* Real property: straight-line, mid-month convention. */
  function realRates(life, month) {
    var first = (12 - month + 0.5) / 12 / life, out = [first], rem = 1 - first;
    while (rem > 1e-9) { var d = Math.min(1 / life, rem); out.push(d); rem -= d; }
    return out;
  }
  /* Book methods: depreciation per asset-year, then spread across calendar years by the first-year fraction. */
  function bookSchedule(method, basis, salvage, n, f) {
    var D = Math.max(0, basis - salvage), A = [], bv = basis, syd = n * (n + 1) / 2;
    for (var k = 1; k <= n; k++) {
      var dep;
      if (method === 'sl') dep = D / n;
      else if (method === 'syd') dep = D * (n - k + 1) / syd;
      else { dep = Math.max(bv * 2 / n, (bv - salvage) / (n - k + 1)); dep = Math.min(dep, Math.max(0, bv - salvage)); }
      A.push(dep); bv -= dep;
    }
    var cal = [];
    for (var i = 0; i <= n; i++) {
      var amt = (i < n ? f * A[i] : 0) + (i > 0 ? (1 - f) * A[i - 1] : 0);
      if (i < n || amt > 0.005) cal.push(amt);
    }
    return cal;
  }

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var method = C.str(f, 'method') || 'macrs', macrs = method === 'macrs';
    var cls = C.str(f, 'cls'), real = cls === '27.5' || cls === '39';
    C.$$('[data-when]', f).forEach(function (el) { var off = el.dataset.when !== (macrs ? 'macrs' : 'book'); el.hidden = off; el.style.display = off ? 'none' : ''; });
    C.$$('[data-when-personal]', f).forEach(function (el) { el.hidden = real; el.style.display = real ? 'none' : ''; });

    var month = +C.str(f, 'month') || 1, py = +C.str(f, 'pyear') || C.defaultYear;
    var basis = Math.max(0, v('cost')) * C.clamp(v('bizPct'), 0, 100) / 100;
    var mtr = C.clamp(v('rate'), 0, 60) / 100;
    var sched = [], rates = [], s179 = 0, bonus = 0, bonusRate = 0, notes = [], regBasis = basis, salvage = 0;

    if (macrs) {
      var bizUse = v('bizPct');
      if (!real) {
        var lim = S179[py] || S179[2026];
        var cap = Math.max(0, lim[0] - Math.max(0, v('cost') - lim[1]));
        var listedOk = bizUse > 50;
        s179 = listedOk ? Math.min(Math.max(0, v('s179')), basis, cap) : 0;
        if (v('s179') > s179 + 0.5) notes.push(listedOk ? 'Section 179 limited to ' + C.money(s179) + ' (asset basis / ' + py + ' cap of ' + C.money(lim[0]) + ').' : 'Section 179 and bonus need more than 50% business use for listed property.');
        var b = C.str(f, 'bonus');
        bonusRate = b === '100' ? (py >= 2025 ? 100 : PHASE[py]) : b === 'phase' ? (PHASE[py] || 0) : 0;
        if (b === '100' && py < 2025) notes.push('100% bonus requires acquisition after Jan 19, 2025 — using the ' + PHASE[py] + '% rate for ' + py + '.');
        if (!listedOk) bonusRate = 0;
        bonus = (basis - s179) * bonusRate / 100;
        regBasis = basis - s179 - bonus;
        var conv = C.str(f, 'conv');
        var life = cls === '15sl' ? 15 : +cls;
        if (cls === '15sl') rates = dbRates(15, 0, conv === 'mq' ? [10.5, 7.5, 4.5, 1.5][Math.floor((month - 1) / 3)] / 12 : 0.5);
        else if (conv === 'mq') rates = dbRates(life, life >= 15 ? 1.5 : 2, [10.5, 7.5, 4.5, 1.5][Math.floor((month - 1) / 3)] / 12);
        else rates = HY[life].map(function (p) { return p / 100; });
        if (conv === 'hy' && month >= 10) notes.push('Placed in service in Q4 — if this is most of your property for the year, the mid-quarter convention applies.');
        if (bizUse <= 50) notes.push('50% or less business use: listed property must use ADS straight-line instead.');
      } else {
        rates = realRates(+cls, month);
        notes.push('Real property uses straight-line with the mid-month convention; buildings are not eligible for bonus depreciation.');
      }
      if (regBasis <= 0.005) rates = [];
      sched = rates.map(function (r) { return regBasis * r; });
      if (sched.length) sched[0] += s179 + bonus; else sched = [s179 + bonus];
      notes.push('MACRS ignores salvage value.');
    } else {
      salvage = Math.min(Math.max(0, v('salvage')), basis);
      var n = Math.round(C.clamp(v('life') || 1, 1, 50));
      sched = bookSchedule(method, basis, salvage, n, (13 - month) / 12);
      notes.push('First year prorated for ' + (13 - month) + ' month' + (month === 12 ? '' : 's') + ' of use.');
    }

    var total = sched.reduce(function (a, x) { return a + x; }, 0);
    var y1 = sched[0] || 0;
    C.big(tool, 'y1', y1);
    C.set(tool, 'biglabel', macrs ? 'First-year tax deduction (' + py + ')' : 'First-year depreciation (' + py + ')');
    C.set(tool, 'basis', C.money(macrs ? basis : basis - salvage));
    C.set(tool, 'total', C.money(total));
    C.set(tool, 'years', String(sched.length));
    C.set(tool, 'taxval', C.money(y1 * mtr));
    var later = Math.max(0, total - y1);
    C.set(tool, 'sub', basis <= 0 ? 'Enter the asset cost to build a schedule' :
      C.pct(basis ? y1 / basis : 0) + ' of the basis in year one · ' + C.money(later) + ' over the following ' + Math.max(0, sched.length - 1) + ' years' + (mtr ? ' · ≈ ' + C.money(y1 * mtr) + ' tax saved in year one' : ''));

    var segs = macrs ? [
      { label: 'Section 179', value: s179, color: '#f59e0b' },
      { label: 'Bonus depreciation (' + bonusRate + '%)', value: bonus, color: '#6366f1' },
      { label: 'Regular MACRS, year 1', value: y1 - s179 - bonus, color: '#0e7490' },
      { label: 'Depreciated in later years', value: later, color: '#10b981' },
      { label: 'Personal use (not deductible)', value: Math.max(0, v('cost') - basis), color: '#cbd5e1' }
    ] : [
      { label: 'Year-1 depreciation', value: y1, color: '#0e7490' },
      { label: 'Later years', value: later, color: '#10b981' },
      { label: 'Salvage value', value: salvage, color: '#cbd5e1' },
      { label: 'Personal use (not deductible)', value: Math.max(0, v('cost') - basis), color: '#e2e8f0' }
    ];
    segs = segs.filter(function (x) { return x.value > 0.5; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var names = { macrs: 'MACRS', sl: 'Straight-line', ddb: 'Double-declining balance', syd: 'Sum-of-years’-digits' };
    var rows = [['Method', names[method] + (macrs ? ' · ' + (cls === '15sl' ? '15-year SL' : cls + '-year') : ' · ' + Math.round(C.clamp(v('life') || 1, 1, 50)) + ' years')]];
    rows.push(['Business basis' + (v('bizPct') < 100 ? ' (' + v('bizPct') + '% of ' + C.money(v('cost')) + ')' : ''), C.money(basis)]);
    if (macrs) {
      if (s179) rows.push(['Section 179 expense', '−' + C.money(s179), 'sub']);
      if (bonus) rows.push(['Bonus depreciation (' + bonusRate + '%)', '−' + C.money(bonus), 'sub']);
      rows.push(['Basis for regular MACRS', C.money(regBasis)]);
      if (rates.length) rows.push(['Year-1 MACRS (' + (rates[0] * 100).toFixed(rates[0] < 0.1 ? 3 : 2) + '%)', C.money(y1 - s179 - bonus), 'sub']);
    } else {
      rows.push(['Salvage value', '−' + C.money(salvage), 'sub']);
      rows.push(['Depreciable amount', C.money(basis - salvage)]);
    }
    rows.push(['Year-2 depreciation', C.money(sched[1] || 0)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Year-1 deduction</span><b>' + C.money(y1) + '</b></li>';
    C.set(tool, 'note', notes.join(' '));

    // Schedule table.
    C.set(tool, 'ratehead', macrs ? 'MACRS rate' : '% of depreciable cost');
    var acc = 0, start = macrs ? basis : basis, html = '';
    sched.forEach(function (d, i) {
      acc += d;
      var r = macrs ? (rates[i] != null ? (rates[i] * 100).toFixed(3).replace(/0$/, '') + '%' : '—') : C.pct(basis - salvage > 0 ? d / (basis - salvage) : 0, 2);
      if (macrs && i === 0 && (s179 || bonus)) r += ' + 179/bonus';
      html += '<tr><td>' + (py + i) + '</td><td class="n">' + r + '</td><td class="n">' + C.money(d) + '</td><td class="n">' + C.money(acc) + '</td><td class="n">' + C.money(Math.max(0, start - acc)) + '</td></tr>';
    });
    C.$('[data-schedule]', tool).innerHTML = html || '<tr><td colspan="5">Enter an asset cost to see the schedule.</td></tr>';
  });
})();
