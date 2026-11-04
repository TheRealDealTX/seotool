/* State income tax engine (JS mirror of app/state-calc.php — keep the two in sync) + calculator UI.
 * Data: window.STATES (inlined by PHP from app/data/states.json). Federal part via CPA.estimate. */
(function () {
  'use strict';
  var C = window.CPA, D = window.STATES || {};
  if (!C) return;

  function brackets(S, st) {
    var b = S.brackets[st];
    if (typeof b === 'string') b = S.brackets[b];
    return b || S.brackets.single || [[null, 0]];
  }
  function bracketTax(taxable, br) {
    var prev = 0, tax = 0, marg = br[0] ? br[0][1] : 0, layers = [];
    taxable = Math.max(0, taxable);
    for (var i = 0; i < br.length; i++) {
      var top = br[i][0] == null ? Infinity : br[i][0], rate = br[i][1];
      var amt = Math.max(0, Math.min(taxable, top) - prev);
      layers.push({ from: prev, to: top, rate: rate, amount: amt, tax: amt * rate });
      tax += amt * rate;
      if (taxable > prev) marg = rate;
      prev = top;
    }
    return { tax: tax, marginal: marg, layers: layers };
  }
  function lin(v, x, a, b, min) {
    min = min || 0;
    if (x <= a) return v;
    if (x >= b) return min;
    return v - (v - min) * (x - a) / (b - a);
  }
  function ctExtra(agi, st) {
    var c = function (x, per) { return Math.ceil(x / per); }, ph, r1, r2;
    if (st === 'mfj') {
      ph = agi > 100500 ? Math.min(20000, 2000 * c(agi - 100500, 5000)) * 0.025 : 0;
      r1 = agi > 210000 ? Math.min(500, 50 * c(agi - 210000, 10000)) : 0;
      r2 = agi > 400000 ? Math.min(6300, Math.min(5400, 180 * c(agi - 400000, 10000)) + (agi > 1000000 ? 100 * c(agi - 1000000, 10000) : 0)) : 0;
    } else if (st === 'hoh') {
      ph = agi > 78500 ? Math.min(16000, 1600 * c(agi - 78500, 5000)) * 0.025 : 0;
      r1 = agi > 168000 ? Math.min(400, 40 * c(agi - 168000, 8000)) : 0;
      r2 = agi > 320000 ? Math.min(5040, Math.min(4200, 140 * c(agi - 320000, 8000)) + (agi > 800000 ? 80 * c(agi - 800000, 8000) : 0)) : 0;
    } else {
      var start = st === 'mfs' ? 50250 : 56500, step = st === 'mfs' ? 2500 : 5000;
      ph = agi > start ? Math.min(10000, 1000 * c(agi - start, step)) * 0.025 : 0;
      r1 = agi > 105000 ? Math.min(250, 25 * c(agi - 105000, 5000)) : 0;
      r2 = agi > 200000 ? Math.min(3150, 90 * c(Math.min(agi, 500000) - 200000, 5000) + (agi > 500000 ? 50 * c(agi - 500000, 5000) : 0)) : 0;
    }
    return ph + r1 + r2;
  }

  /* o: wages, otherIncome, status, kids, pretax, nyc, yonkers, localRate (decimal) */
  function calc(code, o) {
    var S = D[code];
    var wages = o.wages || 0, other = o.otherIncome || 0, st = o.status || 'single', kids = o.kids || 0, pretax = o.pretax || 0;
    var f = C.estimate({ wages: wages, otherIncome: other, status: st, kids: kids, pretax: pretax });
    var fed = { gross: f.gross, agi: f.agi, std: f.std, taxable: f.taxable, tax: f.incomeTax, marginal: f.marginal, fica: f.fica.total, ss: f.fica.ss, medicare: f.fica.medicare + f.fica.addl };
    var gross = wages + other, fedAgi = fed.agi;
    var agi = Math.max(0, gross - (S.pretaxDeductible === false ? 0 : pretax));
    var sp = S.special || '';
    var r = { code: code, gross: gross, stateAgi: agi, std: 0, exemptions: 0, fedTaxDed: 0, taxable: 0, taxBefore: 0, credits: 0, tax: 0,
              marginal: 0, topRate: 0, layers: [], nyc: 0, yonkers: 0, local: 0, fed: fed };
    if (S.type !== 'none') {
      var persons = st === 'mfj' ? 2 : 1;
      var std = S.std[st] != null ? S.std[st] : (S.std.single || 0);
      if (S.stdPhase && S.stdPhase[st]) std = lin(std, agi, S.stdPhase[st][0], S.stdPhase[st][1], S.stdPhase[st][2]);
      if (sp === 'mn') {
        var t1 = st === 'mfs' ? 122200 : 244400, t2 = st === 'mfs' ? 168900 : 337800;
        std -= Math.min(0.8 * std, 0.03 * Math.max(0, Math.min(agi, t2) - t1) + 0.10 * Math.max(0, agi - t2));
      }
      var ex = S.exemption || {};
      var pers = ex.personalByStatus && ex.personalByStatus[st] != null ? ex.personalByStatus[st] : (ex.personal || 0) * persons;
      var dep = (ex.dependent || 0) * kids;
      if (sp === 'al') dep = (agi <= 50000 ? 1000 : agi <= 100000 ? 500 : 300) * kids;
      if (sp === 'oh') { var per = agi <= 40000 ? 2400 : agi <= 80000 ? 2150 : agi < 500000 ? 1900 : 0; pers = per * persons; dep = per * kids; }
      if (sp === 'nm') dep = 4000 * Math.max(0, kids - 1);
      if (sp === 'md') {
        var k = (st === 'mfj' || st === 'hoh') ? (agi <= 150000 ? 1 : agi <= 175000 ? 0.5 : agi <= 200000 ? 0.25 : 0)
                                             : (agi <= 100000 ? 1 : agi <= 125000 ? 0.5 : agi <= 150000 ? 0.25 : 0);
        pers *= k; dep *= k;
      }
      if (S.exemptionPhase && S.exemptionPhase[st]) pers = lin(pers, agi, S.exemptionPhase[st][0], S.exemptionPhase[st][1]);
      if (S.exemptionCliff && S.exemptionCliff[st] != null && agi > S.exemptionCliff[st]) { pers = 0; dep = 0; }
      if (S.allowancePhase) { var kk = lin(1, agi, S.allowancePhase[0], S.allowancePhase[1]); std *= kk; pers *= kk; dep *= kk; }
      var fd = 0, fit = fed.tax, mode = S.fedTaxDeduction || '';
      if (mode === 'full') fd = fit;
      else if (mode === 'mo') { var p = agi <= 25000 ? 0.35 : agi <= 50000 ? 0.25 : agi <= 100000 ? 0.15 : agi <= 125000 ? 0.05 : 0; fd = Math.min(fit * p, st === 'mfj' ? 10000 : 5000); }
      else if (mode === 'or') {
        var th = st === 'mfj' ? [250000, 260000, 270000, 280000, 290000] : [125000, 130000, 135000, 140000, 145000];
        var kf = fedAgi < th[0] ? 1 : fedAgi < th[1] ? 0.8 : fedAgi < th[2] ? 0.6 : fedAgi < th[3] ? 0.4 : fedAgi < th[4] ? 0.2 : 0;
        fd = Math.min(fit, 8500 * kf);
      }
      var taxable = Math.max(0, agi - std - pers - dep - fd);
      var br = brackets(S, st);
      var use = (S.lowIncome && taxable <= S.lowIncome.max) ? S.lowIncome.brackets : br;
      var bt = bracketTax(taxable, use);
      var tax = bt.tax;
      if (S.addOver && taxable > S.addOver[0]) tax += S.addOver[1];
      if (sp === 'ct') tax += ctExtra(agi, st);
      if (S.recapture && agi > S.recapture.start) tax += Math.max(0, taxable * bt.marginal - tax) * Math.min(1, (agi - S.recapture.start) / S.recapture.span);
      if (sp === 'vt' && fedAgi > 150000) tax = Math.max(tax, 0.03 * fedAgi);
      var cr = 0;
      if (S.credits) {
        var pc = S.credits.personalCredit || 0, dc = S.credits.dependentCredit || 0;
        if (sp === 'ca') {
          var cth = st === 'mfj' ? 504411 : st === 'hoh' ? 378310 : 252203;
          var cut = fedAgi > cth ? 6 * Math.ceil((fedAgi - cth) / 2500) : 0;
          cr = Math.max(0, pc - cut) * persons + Math.max(0, dc - cut) * kids;
        } else cr = pc * persons + dc * kids;
        if (S.creditCliff && S.creditCliff[st] != null && fedAgi > S.creditCliff[st]) cr = 0;
      }
      if (sp === 'ut') {
        var u = S.utCredit;
        cr += Math.max(0, u.rate * ((u.fedStd[st] != null ? u.fedStd[st] : u.fedStd.single) + u.depExemption * kids) - u.phaseRate * Math.max(0, agi - u.phaseStart[st]));
      }
      r.std = std; r.exemptions = pers + dep; r.fedTaxDed = fd; r.taxable = taxable;
      r.taxBefore = tax; r.credits = Math.min(cr, tax); r.tax = Math.max(0, tax - cr);
      r.marginal = bt.marginal; r.topRate = br[br.length - 1][1]; r.layers = bt.layers;
      if (o.nyc && S.localTax && S.localTax.nyc) {
        var nb = S.localTax.nyc.brackets[st] || S.localTax.nyc.brackets.single;
        r.nyc = bracketTax(taxable, nb).tax;
      }
      if (o.yonkers && S.localTax && S.localTax.yonkers) r.yonkers = r.tax * S.localTax.yonkers.pctOfState;
    }
    var lr = o.localRate || 0;
    if (lr > 0) r.local = (S.localBase === 'taxable' ? r.taxable : gross) * lr;
    r.localTotal = r.nyc + r.yonkers + r.local;
    r.effective = gross > 0 ? r.tax / gross : 0;
    r.total = fed.tax + fed.fica + r.tax + r.localTotal;
    r.net = gross - r.total - pretax;
    return r;
  }

  window.CPA_STATE = { calc: calc, brackets: brackets, bracketTax: bracketTax, data: D };

  /* ---------------- calculator UI (hub + per-state pages) ---------------- */
  /* Sortable tables: <table data-sortable>, <th data-sort="num|text">, numeric cells carry data-v. */
  C.$$('table[data-sortable]').forEach(function (t) {
    C.$$('th[data-sort]', t).forEach(function (th) {
      var col = Array.prototype.indexOf.call(th.parentNode.children, th);
      th.tabIndex = 0; th.style.cursor = 'pointer'; th.setAttribute('aria-sort', 'none');
      var go = function () {
        var asc = th.getAttribute('aria-sort') !== 'ascending';
        C.$$('th[data-sort]', t).forEach(function (h) { h.setAttribute('aria-sort', 'none'); });
        th.setAttribute('aria-sort', asc ? 'ascending' : 'descending');
        var body = t.tBodies[0], rows = Array.prototype.slice.call(body.rows), num = th.dataset.sort === 'num';
        rows.sort(function (a, b) {
          var x = a.cells[col], y = b.cells[col];
          x = num ? +(x.dataset.v || 0) : x.textContent.trim(); y = num ? +(y.dataset.v || 0) : y.textContent.trim();
          return (num ? x - y : x.localeCompare(y)) * (asc ? 1 : -1);
        });
        rows.forEach(function (r) { body.appendChild(r); });
      };
      th.addEventListener('click', go);
      th.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
    });
  });

  var form = document.getElementById('state-form');
  if (!form) return;
  var tool = form.closest('.tool');
  var sel = form.elements.state;
  var nycBox = C.$('[data-nyc]', form);
  var pct = function (n) { return (Math.round(n * 10000) / 100).toString().replace(/\.?0+$/, '') + '%'; };
  C.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var code = sel ? sel.value : f.elements.state.value;
    var S = D[code];
    if (!S) return;
    if (nycBox) nycBox.hidden = !S.localTax;
    var h = C.$('[data-state-link]', tool);
    if (h && h.getAttribute('href') !== '/calculators/state-income-tax/' + S.slug + '/') { h.href = '/calculators/state-income-tax/' + S.slug + '/'; h.textContent = S.name + ' income tax guide →'; }
    var st = C.str(f, 'status');
    var nyc = !!(S.localTax && f.elements.nyc && f.elements.nyc.checked);
    var yon = !!(S.localTax && f.elements.yonkers && f.elements.yonkers.checked);
    var r = calc(code, { wages: v('wages'), otherIncome: v('otherIncome'), status: st, kids: +v('kids') || 0, pretax: v('pretax'),
                         nyc: nyc, yonkers: yon, localRate: v('localRate') / 100 });
    var pretax = v('pretax');
    C.big(tool, 'tax', r.tax);
    C.set(tool, 'stateName', S.name);
    C.set(tool, 'eff', C.pct(r.effective, 2));
    C.set(tool, 'marg', S.type === 'none' ? 'None' : pct(r.marginal));
    C.set(tool, 'top', S.type === 'none' ? 'No income tax' : pct(r.topRate));
    C.set(tool, 'total', C.money(r.total));
    C.set(tool, 'summary', S.type === 'none'
      ? S.name + ' has no state income tax on wages · take-home ≈ ' + C.money(r.net) + '/yr'
      : 'On ' + C.money(r.gross) + ' of income · ' + S.year + ' ' + S.name + ' rates · take-home ≈ ' + C.money(r.net) + '/yr');
    C.set(tool, 'netYear', C.money(r.net));
    C.set(tool, 'netMonth', C.money(r.net / 12));
    C.set(tool, 'netBiweekly', C.money(r.net / 26));
    C.set(tool, 'fedTax', C.money(r.fed.tax));
    var segs = [
      { label: 'Federal income tax', value: r.fed.tax, color: '#0e7490' },
      { label: S.name + ' income tax', value: r.tax, color: '#ef4444' },
      { label: 'Local / city tax', value: r.localTotal, color: '#a855f7' },
      { label: 'Social Security & Medicare', value: r.fed.fica, color: '#f59e0b' },
      { label: 'Pre-tax 401(k)', value: pretax, color: '#6366f1' },
      { label: 'Take-home pay', value: Math.max(0, r.net), color: '#10b981' }
    ].filter(function (s) { return s.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);
    var rows = [['Gross income', C.money(r.gross)]];
    if (S.type !== 'none') {
      if (pretax && S.pretaxDeductible === false) rows.push(['401(k) not deductible in ' + S.name, '—']);
      else if (pretax) rows.push(['Pre-tax 401(k)', '−' + C.money(pretax)]);
      if (r.std) rows.push([code === 'SC' ? 'SC income-adjusted deduction' : 'State standard deduction', '−' + C.money(r.std)]);
      if (r.exemptions) rows.push(['Exemptions', '−' + C.money(r.exemptions)]);
      if (r.fedTaxDed) rows.push(['Federal income tax deduction', '−' + C.money(r.fedTaxDed)]);
      rows.push([S.name + ' taxable income', C.money(r.taxable)]);
      rows.push(['Tax before credits', C.money(r.taxBefore)]);
      if (r.credits) rows.push(['State credits', '−' + C.money(r.credits)]);
    }
    rows.push([S.name + ' income tax', C.money(r.tax)]);
    if (r.nyc) rows.push(['NYC resident tax', C.money(r.nyc)]);
    if (r.yonkers) rows.push(['Yonkers surcharge', C.money(r.yonkers)]);
    if (r.local) rows.push(['Local income tax (' + v('localRate') + '%)', C.money(r.local)]);
    rows.push(['Federal income tax', C.money(r.fed.tax)]);
    rows.push(['Social Security & Medicare', C.money(r.fed.fica)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Total tax</span><b>' + C.money(r.total) + '</b></li>';
    var bEl = C.$('[data-brackets]', tool);
    if (bEl) {
      if (S.type === 'none' || !r.layers.length) bEl.innerHTML = '<p class="hint">' + S.name + ' does not tax wages, so there are no brackets to fill.</p>';
      else {
        var mx = r.layers.reduce(function (a, l) { return Math.max(a, l.amount); }, 1);
        bEl.innerHTML = r.layers.map(function (l) {
          var range = C.money(l.from) + (l.to === Infinity ? '+' : ' – ' + C.money(l.to));
          return '<div class="br-row' + (l.amount > 0 ? ' on' : '') + '"><span class="br-rate">' + pct(l.rate) + '</span>' +
            '<span class="br-bar"><span style="width:' + (l.amount / mx * 100) + '%"></span></span><span class="br-amt">' + (l.amount > 0 ? C.money(l.tax) : '—') +
            '</span><span class="br-range">' + range + '</span></div>';
        }).join('');
      }
    }
  });
})();
