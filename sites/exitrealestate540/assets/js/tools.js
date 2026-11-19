/* Exit Real Estate 540 - calculators. No dependencies, no tracking. */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var usd0 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  var usd = function (n) { return isFinite(n) ? usd0.format(Math.round(n)) : '-'; };
  var pct = function (n, d) { return isFinite(n) ? n.toFixed(d === undefined ? 1 : d) + '%' : '-'; };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  function vals(form) {
    var o = {};
    $$('input[name], select[name]', form).forEach(function (el) {
      var v = el.value;
      o[el.name] = (el.type === 'number') ? (parseFloat(v) || 0) : v;
    });
    return o;
  }
  function set(form, key, text) {
    var el = form.querySelector('[data-out="' + key + '"]');
    if (el) el.textContent = text;
  }
  function html(form, sel, markup) {
    var el = form.querySelector(sel);
    if (el) el.innerHTML = markup;
  }
  function payment(principal, annualRate, years) {
    var n = years * 12, r = annualRate / 100 / 12;
    if (principal <= 0) return 0;
    if (r === 0) return principal / n;
    return principal * r / (1 - Math.pow(1 + r, -n));
  }
  function table(head, rows, foot) {
    var h = '<table><thead><tr>' + head.map(function (c, i) { return '<th' + (i ? ' class="num"' : '') + '>' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>';
    rows.forEach(function (r) { h += '<tr>' + r.map(function (c, i) { return '<td' + (i ? ' class="num"' : '') + '>' + esc(c) + '</td>'; }).join('') + '</tr>'; });
    h += '</tbody>';
    if (foot) h += '<tfoot><tr>' + foot.map(function (c, i) { return '<th' + (i ? ' class="num"' : '') + '>' + esc(c) + '</th>'; }).join('') + '</tr></tfoot>';
    return h + '</table>';
  }
  function bars(parts) {
    var total = parts.reduce(function (s, p) { return s + Math.max(0, p[1]); }, 0) || 1;
    var bar = '<div class="bars__track">' + parts.map(function (p, i) {
      return '<span class="bars__seg s' + i + '" style="width:' + (Math.max(0, p[1]) / total * 100).toFixed(2) + '%" title="' + esc(p[0]) + '"></span>';
    }).join('') + '</div>';
    var legend = '<ul class="bars__legend">' + parts.map(function (p, i) {
      return '<li><i class="s' + i + '"></i>' + esc(p[0]) + ' <b>' + usd(p[1]) + '</b></li>';
    }).join('') + '</ul>';
    return bar + legend;
  }
  /* Simple responsive SVG line chart. series: [{name, data:[...], cls}] */
  function lineChart(series, labels, fmtY) {
    var W = 640, H = 260, L = 64, R = 12, T = 12, B = 30;
    var all = []; series.forEach(function (s) { all = all.concat(s.data); });
    var max = Math.max.apply(null, all), min = Math.min(0, Math.min.apply(null, all));
    if (max === min) max = min + 1;
    var n = labels.length;
    var x = function (i) { return L + (n <= 1 ? 0 : i / (n - 1) * (W - L - R)); };
    var y = function (v) { return T + (1 - (v - min) / (max - min)) * (H - T - B); };
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" class="chart__svg" preserveAspectRatio="none">';
    for (var g = 0; g <= 4; g++) {
      var gv = min + (max - min) * g / 4, gy = y(gv);
      s += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + gy + '" y2="' + gy + '" class="chart__grid"/>';
      s += '<text x="' + (L - 8) + '" y="' + (gy + 4) + '" text-anchor="end" class="chart__lbl">' + esc(fmtY(gv)) + '</text>';
    }
    var step = Math.max(1, Math.ceil(n / 8));
    labels.forEach(function (lb, i) {
      if (i % step === 0 || i === n - 1) s += '<text x="' + x(i) + '" y="' + (H - 8) + '" text-anchor="middle" class="chart__lbl">' + esc(lb) + '</text>';
    });
    series.forEach(function (se) {
      var d = se.data.map(function (v, i) { return (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1); }).join(' ');
      s += '<path d="' + d + '" class="chart__line ' + se.cls + '"/>';
    });
    s += '</svg><ul class="chart__legend">' + series.map(function (se) { return '<li><i class="' + se.cls + '"></i>' + esc(se.name) + '</li>'; }).join('') + '</ul>';
    return s;
  }

  var tools = {};

  tools['mortgage-calculator'] = function (f) {
    var v = vals(f);
    var down = v.price * v.down / 100, loan = Math.max(0, v.price - down);
    var pi = payment(loan, v.rate, +v.term);
    var taxm = v.price * v.tax / 100 / 12, insm = v.ins / 12;
    var ltv = v.price ? loan / v.price : 0;
    var pmim = ltv > 0.8 ? loan * v.pmi / 100 / 12 : 0;
    // amortize
    var bal = loan, r = v.rate / 100 / 12, interest = 0, pmiEnd = null, rows = [], yi = 0, yp = 0, n = v.term * 12;
    for (var m = 1; m <= n && bal > 0.005; m++) {
      var it = bal * r, pr = Math.min(pi - it, bal);
      if (r === 0) pr = Math.min(pi, bal);
      bal -= pr; interest += it; yi += it; yp += pr;
      if (pmiEnd === null && pmim > 0 && bal <= v.price * 0.78) pmiEnd = m;
      if (m % 12 === 0 || bal <= 0.005) { rows.push(['Year ' + Math.ceil(m / 12), usd(yp), usd(yi), usd(Math.max(0, bal))]); yi = 0; yp = 0; }
    }
    set(f, 'total', usd(pi + taxm + insm + pmim + v.hoa));
    set(f, 'pi', usd(pi)); set(f, 'taxm', usd(taxm)); set(f, 'insm', usd(insm)); set(f, 'pmim', usd(pmim));
    set(f, 'loan', usd(loan)); set(f, 'interest', usd(interest)); set(f, 'cash', usd(down));
    set(f, 'pmiend', pmim > 0 ? (pmiEnd ? 'Year ' + Math.ceil(pmiEnd / 12) : 'n/a') : 'No PMI');
    html(f, '[data-out-bars="breakdown"]', bars([['Principal & interest', pi], ['Property tax', taxm], ['Insurance', insm], ['PMI', pmim], ['HOA', v.hoa]]));
    html(f, '[data-out-table="amort"]', table(['Year', 'Principal paid', 'Interest paid', 'Balance'], rows));
  };

  tools['home-affordability-calculator'] = function (f) {
    var v = vals(f), lim = v.profile.split('/');
    var monthly = v.income / 12, fr = lim[0] / 100, bk = lim[1] / 100;
    var maxHousing = Math.min(monthly * fr, monthly * bk - v.debts);
    var limiting = (monthly * fr <= monthly * bk - v.debts) ? 'Housing ratio' : 'Total debts';
    // payment(price) = pi(price - down) + price*(tax+ins)/1200 + hoa ; solve by bisection
    var cost = function (price) {
      var loan = Math.max(0, price - v.downcash);
      return payment(loan, v.rate, +v.term) + price * (v.tax + v.insrate) / 1200 + v.hoa;
    };
    var lo = 0, hi = 5e6, price = 0;
    if (maxHousing > v.hoa) {
      for (var i = 0; i < 80; i++) { var mid = (lo + hi) / 2; if (cost(mid) > maxHousing) hi = mid; else lo = mid; }
      price = Math.floor(lo / 1000) * 1000;
    }
    var pay = price ? cost(price) : 0;
    var loan = Math.max(0, price - v.downcash);
    set(f, 'price', price ? usd(price) : '$0');
    set(f, 'payment', usd(pay)); set(f, 'loan', usd(loan));
    set(f, 'downpct', price ? pct(Math.min(100, v.downcash / price * 100)) : '-');
    set(f, 'limit', limiting);
    set(f, 'front', pct(pay / monthly * 100)); set(f, 'back', pct((pay + v.debts) / monthly * 100));
    var note = '';
    if (price && v.downcash / price < 0.2) note = 'With less than 20% down on a conventional loan, expect PMI on top of this payment (not included). ';
    if (price && v.downcash / price < 0.035) note += 'Most loans need at least 3%-3.5% down unless you qualify for VA or USDA. ';
    set(f, 'note', note + 'Remember to budget separately for closing costs, moving and an emergency fund.');
  };

  tools['rent-vs-buy-calculator'] = function (f) {
    var v = vals(f), Y = Math.max(1, Math.min(30, Math.round(v.years)));
    var down = v.price * v.down / 100, loan = v.price - down, closing = v.price * 0.03, sellCost = 0.07;
    var pi = payment(loan, v.rate, 30), r = v.rate / 100 / 12, bal = loan, home = v.price;
    var renterPort = down + closing, rent = v.rent, buyW = [], rentW = [], labels = [], breakeven = null, ownY1 = 0;
    for (var y = 1; y <= Y; y++) {
      var ownCostYear = 0;
      for (var m = 0; m < 12; m++) {
        var it = bal * r, pr = Math.min(pi - it, bal); bal -= pr;
        var own = pi + home * v.tax / 1200 + v.ins / 12 + home * v.maint / 1200 + v.hoa;
        ownCostYear += own;
        var rentCost = rent + 15;
        renterPort = renterPort * (1 + v.invest / 1200) + (own - rentCost);
      }
      if (y === 1) ownY1 = ownCostYear / 12;
      home *= 1 + v.appr / 100;
      rent *= 1 + v.rentinc / 100;
      var buyNet = home * (1 - sellCost) - bal;
      buyW.push(buyNet); rentW.push(renterPort); labels.push('Yr ' + y);
      if (breakeven === null && buyNet >= renterPort) breakeven = y;
    }
    var b = buyW[Y - 1], rr = rentW[Y - 1];
    set(f, 'verdict', b >= rr ? 'Buying wins by ' + usd(b - rr) : 'Renting wins by ' + usd(rr - b));
    set(f, 'buynet', usd(b)); set(f, 'rentnet', usd(rr));
    set(f, 'breakeven', breakeven ? 'Year ' + breakeven : 'Not within ' + Y + ' yrs');
    set(f, 'ownmonthly', usd(ownY1));
    html(f, '[data-out-chart="wealth"]', lineChart([{ name: 'Buy: home equity after selling costs', data: buyW, cls: 'c1' }, { name: 'Rent: invested savings', data: rentW, cls: 'c2' }], labels, function (n) { return '$' + Math.round(n / 1000) + 'k'; }));
  };

  // Approximate Texas promulgated basic title premium (owner's policy), TDI schedule effective March 1, 2026.
  function txTitle(amount) {
    if (amount <= 0) return 0;
    if (amount <= 100000) return Math.max(223, 223 + (amount - 10000) * 0.0062);
    if (amount <= 1000000) return 780 + (amount - 100000) * 0.00494;
    return 5226 + (amount - 1000000) * 0.00406;
  }

  tools['closing-cost-calculator'] = function (f) {
    var v = vals(f), cash = v.loan === 'cash';
    var downAmt = cash ? v.price : v.price * v.down / 100, base = cash ? 0 : v.price - downAmt;
    var loanAmt = base;
    if (v.loan === 'fha') loanAmt = base * 1.0175;        // upfront MIP financed
    if (v.loan === 'va') loanAmt = base * (v.down >= 10 ? 1.0125 : v.down >= 5 ? 1.015 : 1.0215); // first-use funding fee financed
    var lines = [];
    if (!cash) {
      lines.push(['Origination & lender fees', loanAmt * v.orig / 100]);
      lines.push(['Appraisal', v.appraisal]);
      lines.push(['Credit report, flood cert, tax service', 150]);
      lines.push(["Lender's title policy + endorsements", 100 + 250]);
    }
    if (v.ownerpolicy === 'buyer') lines.push(["Owner's title policy (TDI rate, approx.)", txTitle(v.price)]);
    lines.push(['Escrow / settlement fee', v.escrowfee]);
    lines.push(['Survey', v.survey]);
    lines.push(['Home inspection', v.inspection]);
    lines.push(['Recording & courier fees', 150]);
    if (!cash) {
      lines.push(['Prepaid: 1st-year homeowners insurance', v.ins]);
      lines.push(['Escrow deposit: 3 months insurance', v.ins / 4]);
      lines.push(['Escrow deposit: 3 months property tax', v.price * v.tax / 100 / 4]);
      lines.push(['Prepaid interest (~15 days)', loanAmt * 0.065 / 365 * 15]);
    } else {
      lines.push(['Homeowners insurance (1st year)', v.ins]);
    }
    var total = lines.reduce(function (s, l) { return s + l[1]; }, 0) - v.credit;
    if (v.credit) lines.push(['Seller credit', -v.credit]);
    total = Math.max(0, total);
    set(f, 'cashclose', usd(downAmt + total)); set(f, 'closing', usd(total));
    set(f, 'pct', pct(total / v.price * 100)); set(f, 'downamt', usd(downAmt)); set(f, 'loanamt', cash ? '$0' : usd(loanAmt));
    html(f, '[data-out-table="lines"]', table(['Item', 'Estimate'], lines.map(function (l) { return [l[0], usd(l[1])]; }), ['Total closing costs', usd(total)]));
  };

  tools['seller-net-proceeds-calculator'] = function (f) {
    var v = vals(f);
    var comm = v.price * (v.listcomm + v.buycomm) / 100;
    var title = v.ownerpolicy === 'seller' ? txTitle(v.price) : 0;
    var prorate = v.taxbill * (+v.month - 0.5) / 12;
    var lines = [
      ['Listing agent commission', v.price * v.listcomm / 100],
      ['Buyer agent compensation', v.price * v.buycomm / 100],
      ["Owner's title policy (approx.)", title],
      ['Escrow fee (seller half)', 400],
      ['Document prep, recording, release', 300],
      ['Property tax proration (credit to buyer)', prorate],
      ['Repairs & prep', v.repairs],
      ['Buyer concessions', v.concessions],
      ['Other fees', v.other]
    ];
    var costs = lines.reduce(function (s, l) { return s + l[1]; }, 0);
    var net = v.price - costs - v.payoff;
    set(f, 'net', usd(net)); set(f, 'costs', usd(costs)); set(f, 'costpct', pct(costs / v.price * 100));
    set(f, 'comm', usd(comm)); set(f, 'prorate', usd(prorate));
    lines.push(['Mortgage payoff', v.payoff]);
    html(f, '[data-out-table="lines"]', table(['Item', 'Amount'], [['Sale price', usd(v.price)]].concat(lines.map(function (l) { return [l[0], '-' + usd(l[1])]; })), ['Estimated net to you', usd(net)]));
  };

  tools['rental-property-calculator'] = function (f) {
    var v = vals(f);
    var loan = v.price * (1 - v.down / 100), pi = payment(loan, v.rate, +v.term);
    var gross = (v.rent + v.other) * 12, vac = gross * v.vacancy / 100, egi = gross - vac;
    var pctExp = v.rent * 12 * (v.mgmt + v.repairs + v.capex) / 100;
    var opex = v.tax + v.ins + v.hoa * 12 + v.utils * 12 + pctExp;
    var noi = egi - opex, debt = pi * 12, cf = noi - debt;
    var cashIn = v.price * v.down / 100 + v.closing + v.rehab;
    set(f, 'cashflow', usd(cf / 12)); set(f, 'noi', usd(noi));
    set(f, 'cap', pct(noi / (v.price + v.rehab) * 100, 2));
    set(f, 'coc', cashIn ? pct(cf / cashIn * 100, 2) : '-');
    set(f, 'dscr', debt ? (noi / debt).toFixed(2) : 'No loan');
    set(f, 'cashin', usd(cashIn)); set(f, 'pi', usd(pi));
    var ratio = v.rent / v.price * 100;
    set(f, 'onepct', ratio.toFixed(2) + '% ' + (ratio >= 1 ? '(passes)' : '(below 1%)'));
    set(f, 'grm', gross ? (v.price / gross).toFixed(1) : '-');
    var rows = [
      ['Gross scheduled income', usd(gross)], ['Vacancy loss', '-' + usd(vac)],
      ['Property tax', '-' + usd(v.tax)], ['Insurance', '-' + usd(v.ins)], ['HOA', '-' + usd(v.hoa * 12)],
      ['Management', '-' + usd(v.rent * 12 * v.mgmt / 100)], ['Repairs', '-' + usd(v.rent * 12 * v.repairs / 100)],
      ['CapEx reserve', '-' + usd(v.rent * 12 * v.capex / 100)], ['Utilities', '-' + usd(v.utils * 12)],
      ['Net operating income', usd(noi)], ['Mortgage payments', '-' + usd(debt)]
    ];
    html(f, '[data-out-table="lines"]', table(['Annual', 'Amount'], rows, ['Annual cash flow', usd(cf)]));
  };

  function amortInterest(bal, rate, years) {
    var p = payment(bal, rate, years);
    return p * years * 12 - bal;
  }

  tools['refinance-calculator'] = function (f) {
    var v = vals(f);
    var oldPay = payment(v.balance, v.currate, v.remaining);
    var newBal = v.balance + (v.roll === 'roll' ? v.costs : 0);
    var newPay = payment(newBal, v.newrate, +v.newterm);
    var save = oldPay - newPay;
    var oldInt = amortInterest(v.balance, v.currate, v.remaining);
    var newInt = amortInterest(newBal, v.newrate, +v.newterm) + (v.roll === 'roll' ? 0 : v.costs);
    set(f, 'savings', save > 0 ? usd(save) : 'None (' + usd(save) + ')');
    set(f, 'oldpay', usd(oldPay)); set(f, 'newpay', usd(newPay));
    var be = save > 0 ? Math.ceil(v.costs / save) : null;
    set(f, 'breakeven', be ? be + ' months (' + (be / 12).toFixed(1) + ' yrs)' : 'Never');
    var d = newInt - oldInt;
    set(f, 'interestdiff', (d > 0 ? '+' : '-') + usd(Math.abs(d)));
    var note = '';
    if (save > 0 && d > 0) note = 'Your payment drops, but you pay more interest overall because the new term is longer than what is left on your current loan. Consider a shorter term or extra payments.';
    else if (save > 0) note = 'This refinance lowers both your payment and your total interest cost. If you will keep the loan past the break-even point, it is likely worth it.';
    else note = 'The new payment is higher - usually because of a shorter term. Check the lifetime interest change to see if that tradeoff works for you.';
    set(f, 'note', note);
  };

  tools['extra-payment-calculator'] = function (f) {
    var v = vals(f), r = v.rate / 100 / 12, n = Math.round(v.remaining * 12);
    var p = payment(v.balance, v.rate, v.remaining);
    function run(extraM, extraY, lump) {
      var bal = v.balance - lump, interest = 0, m = 0, series = [v.balance];
      while (bal > 0.01 && m < n + 1) {
        m++;
        var it = bal * r; interest += it;
        var pr = p - it + extraM + (m % 12 === 0 ? extraY : 0);
        bal = Math.max(0, bal - pr);
        if (m % 12 === 0) series.push(bal);
      }
      if (m % 12 !== 0) series.push(bal);
      return { months: m, interest: interest, series: series };
    }
    var base = run(0, 0, 0), ex = run(v.extram, v.extray, Math.min(v.lump, v.balance));
    var saved = base.interest - ex.interest, ms = base.months - ex.months;
    set(f, 'saved', usd(saved));
    set(f, 'timesaved', Math.floor(ms / 12) + ' yrs ' + (ms % 12) + ' mos');
    var d = new Date(); d.setMonth(d.getMonth() + ex.months);
    set(f, 'newpayoff', d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }));
    set(f, 'payment', usd(p)); set(f, 'totalint', usd(ex.interest));
    var len = base.series.length, a = ex.series.slice();
    while (a.length < len) a.push(0);
    var labels = base.series.map(function (_, i) { return 'Yr ' + i; });
    html(f, '[data-out-chart="balance"]', lineChart([{ name: 'Without extra payments', data: base.series, cls: 'c2' }, { name: 'With extra payments', data: a, cls: 'c1' }], labels, function (x) { return '$' + Math.round(x / 1000) + 'k'; }));
  };

  tools['dti-calculator'] = function (f) {
    var v = vals(f);
    var debts = v.car + v.student + v.cards + v.otherdebt, inc = v.income || 1;
    var front = v.housing / inc * 100, back = (v.housing + debts) / inc * 100;
    set(f, 'back', pct(back)); set(f, 'front', pct(front)); set(f, 'totaldebt', usd(v.housing + debts));
    var lim = [['Conventional (typical)', 28, 45], ['Conventional (max w/ strong file)', null, 50], ['FHA (typical)', 31, 43], ['FHA (with compensating factors)', null, 50], ['VA (guideline + residual income)', null, 41], ['USDA', 29, 41]];
    html(f, '[data-out-table="limits"]', table(['Guideline', 'Front-end', 'Back-end', 'You'], lim.map(function (l) {
      var ok = back <= l[2] && (l[1] === null || front <= l[1]);
      return [l[0], l[1] === null ? '-' : l[1] + '%', l[2] + '%', ok ? 'Within' : 'Over'];
    })));
  };

  tools['texas-property-tax-calculator'] = function (f) {
    var v = vals(f), hs = v.homestead === '1', sr = v.senior === '1';
    var schoolEx = hs ? 140000 + (sr ? 60000 : 0) : 0;
    var localEx = hs ? v.value * Math.min(20, v.localpct) / 100 : 0;
    var srLocal = hs && sr ? v.localsenior : 0;
    var units = [
      ['School district', v.school, schoolEx],
      ['County', v.county, localEx + srLocal],
      ['City', v.city, localEx + srLocal],
      ['Other (MUD, college, etc.)', v.other, 0]
    ];
    var total = 0, none = 0, rows = [];
    units.forEach(function (u) {
      var taxable = Math.max(0, v.value - u[2]), tax = taxable * u[1] / 100;
      total += tax; none += v.value * u[1] / 100;
      rows.push([u[0], u[1].toFixed(4) + '%', usd(u[2]), usd(taxable), usd(tax)]);
    });
    set(f, 'total', usd(total)); set(f, 'monthly', usd(total / 12));
    set(f, 'effective', pct(total / (v.value || 1) * 100, 2));
    set(f, 'saved', usd(none - total)); set(f, 'noexempt', usd(none));
    html(f, '[data-out-table="lines"]', table(['Taxing unit', 'Rate', 'Exemption', 'Taxable value', 'Tax'], rows, ['Total', '', '', '', usd(total)]));
  };

  /* ===================== tools added in round 2 ===================== */

  function piti(f, v, loan, extra) {
    var pi = payment(loan, v.rate, +v.term), taxm = v.price * v.tax / 1200, insm = v.ins / 12;
    var parts = [['Principal & interest', pi], ['Property tax', taxm], ['Insurance', insm]].concat(extra || []).concat([['HOA', v.hoa]]);
    html(f, '[data-out-bars="breakdown"]', bars(parts));
    return { pi: pi, total: parts.reduce(function (s, p) { return s + p[1]; }, 0) };
  }

  tools['fha-loan-calculator'] = function (f) {
    var v = vals(f), d = Math.max(3.5, v.down) / 100;
    var base = v.price * (1 - d), ufmip = base * 0.0175, loan = base + ufmip, ltv = 1 - d, big = base > 726200, rate;
    if (+v.term > 15) rate = big ? (ltv > 0.95 ? 0.75 : 0.70) : (ltv > 0.95 ? 0.55 : 0.50);
    else rate = big ? (ltv > 0.90 ? 0.65 : ltv > 0.78 ? 0.40 : 0.15) : (ltv > 0.90 ? 0.40 : 0.15);
    var mip = base * rate / 1200, r = piti(f, v, loan, [['FHA MIP', mip]]);
    set(f, 'total', usd(r.total)); set(f, 'base', usd(base)); set(f, 'ufmip', usd(ufmip)); set(f, 'loan', usd(loan));
    set(f, 'miprate', rate.toFixed(2) + '% / yr'); set(f, 'mipdur', ltv > 0.90 ? 'Life of loan' : '11 years'); set(f, 'cash', usd(v.price * d));
    var note = v.down < 3.5 ? 'FHA requires at least 3.5% down, so 3.5% is used. ' : '';
    if (base > v.limit) note += 'The base loan is above the county FHA limit you entered - you would need about ' + usd(v.price - v.limit) + ' down, or a different loan type. ';
    set(f, 'note', note + 'Monthly MIP is estimated on the starting balance; lenders compute it on each year\'s average balance.');
  };

  tools['va-loan-calculator'] = function (f) {
    var v = vals(f), d = v.down / 100, pct = 0;
    if (v.exempt !== '1') pct = v.down < 5 ? (v.use === 'first' ? 2.15 : 3.3) : v.down < 10 ? 1.5 : 1.25;
    var base = v.price * (1 - d), fee = base * pct / 100, r = piti(f, v, base + fee);
    set(f, 'total', usd(r.total)); set(f, 'feepct', pct ? pct.toFixed(2) + '%' : 'Exempt'); set(f, 'fee', usd(fee));
    set(f, 'loan', usd(base + fee)); set(f, 'pi', usd(r.pi)); set(f, 'cash', usd(v.price * d)); set(f, 'pmi', '$0 (none on VA)');
  };

  var DP = { conv20: ['Conventional 20%', 20], conv5: ['Conventional 5%', 5], conv3: ['Conventional 3%', 3], fha: ['FHA 3.5%', 3.5], va: ['VA 0%', 0], usda: ['USDA 0%', 0] };
  function monthsToSave(saved, monthly, ret, need) {
    if (saved >= need) return 0;
    var m = 0, bal = saved, r = ret / 1200;
    while (bal < need && m < 600) { bal = bal * (1 + r) + monthly; m++; }
    return m >= 600 ? Infinity : m;
  }
  tools['down-payment-calculator'] = function (f) {
    var v = vals(f);
    function calc(pct) {
      var down = v.price * pct / 100, cc = v.price * v.closing / 100, need = Math.max(0, down + cc - v.assist);
      return { down: down, cc: cc, need: need, months: monthsToSave(v.saved, v.monthly, v.ret, need) };
    }
    var pct = v.loan === 'custom' ? v.custom : DP[v.loan][1], c = calc(pct);
    set(f, 'need', usd(c.need)); set(f, 'down', usd(c.down) + ' (' + pct + '%)'); set(f, 'cc', usd(c.cc));
    set(f, 'gap', usd(Math.max(0, c.need - v.saved))); set(f, 'loanamt', usd(v.price - c.down));
    var fmtM = function (m) { return m === 0 ? 'Ready now' : m === Infinity ? '50+ years' : Math.floor(m / 12) + ' yrs ' + (m % 12) + ' mos'; };
    set(f, 'time', fmtM(c.months));
    var dt = new Date(); if (isFinite(c.months)) dt.setMonth(dt.getMonth() + c.months);
    set(f, 'date', isFinite(c.months) ? dt.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }) : '-');
    html(f, '[data-out-table="types"]', table(['Loan type', 'Down payment', 'Cash needed', 'Time to save'], Object.keys(DP).map(function (k) {
      var x = calc(DP[k][1]); return [DP[k][0], usd(x.down), usd(x.need), fmtM(x.months)];
    })));
  };

  tools['rent-affordability-calculator'] = function (f) {
    var v = vals(f), gm = v.gross / 12;
    var r30 = Math.max(0, gm * 0.30 - v.utils), r50 = Math.max(0, v.net * 0.50 - v.debts - v.utils - v.groceries), rl = gm / Math.max(1, v.multiple);
    var t = Math.min(r30, r50, rl);
    set(f, 'target', usd(t) + '/mo'); set(f, 'r30', usd(r30)); set(f, 'r503020', usd(r50)); set(f, 'rland', usd(rl));
    set(f, 'pct', gm ? pct((t + v.utils) / gm * 100) + ' incl. utilities' : '-');
    var lim = t === r50 ? 'your take-home budget' : t === r30 ? 'the 30% rule' : 'the landlord income test';
    set(f, 'note', 'The limiting factor is ' + lim + '. ' + (r50 < r30 * 0.8 ? 'Your debt payments are squeezing your rent budget - paying one down would free up room. ' : '') + 'Remember move-in costs: deposit, first month and possibly application and pet fees.');
  };

  tools['home-equity-calculator'] = function (f) {
    var v = vals(f), maxDebt = v.value * v.cltv / 100, avail = Math.max(0, maxDebt - v.balance), eq = v.value - v.balance;
    var io = v.draw * v.rate / 1200, am = payment(v.draw, v.rate, v.repyrs);
    set(f, 'avail', usd(avail)); set(f, 'equity', usd(eq)); set(f, 'equitypct', v.value ? pct(eq / v.value * 100) : '-');
    set(f, 'io', usd(io)); set(f, 'amort', usd(am)); set(f, 'newcltv', v.value ? pct((v.balance + v.draw) / v.value * 100) : '-');
    set(f, 'totalint', usd(io * 12 * v.drawyrs + Math.max(0, am * 12 * v.repyrs - v.draw)));
    set(f, 'note', v.draw > avail ? 'The amount you want is more than the ' + v.cltv + '% limit allows. Reduce it to ' + usd(avail) + ' or less.' : 'Payments assume the full amount is drawn now and the rate stays the same. HELOC rates are usually variable.');
  };

  tools['cash-out-refinance-calculator'] = function (f) {
    var v = vals(f), c = v.costs / 100, maxLoan = v.value * v.ltv / 100;
    var want = (v.cash + v.balance) / (1 - c), loan = Math.min(want, maxLoan), cashout = loan - v.balance - loan * c;
    var maxcash = Math.max(0, maxLoan * (1 - c) - v.balance);
    var np = payment(loan, v.newrate, +v.term), op = payment(v.balance, v.currate, v.remaining);
    set(f, 'cashout', usd(Math.max(0, cashout))); set(f, 'maxcash', usd(maxcash)); set(f, 'newloan', usd(loan));
    set(f, 'newpay', usd(np)); set(f, 'oldpay', usd(op)); set(f, 'diff', (np >= op ? '+' : '-') + usd(Math.abs(np - op)));
    set(f, 'ltvafter', v.value ? pct(loan / v.value * 100) : '-');
    var note = want > maxLoan ? 'You asked for more than the ' + v.ltv + '% limit allows; the cash shown is the maximum. ' : '';
    if (v.newrate > v.currate) note += 'Your new rate is higher than your current one, so you would also pay more on the ' + usd(v.balance) + ' you already owe. A HELOC or home equity loan may cost less.';
    set(f, 'note', note || 'Closing costs are assumed to be paid from the loan proceeds.');
  };

  var CG = { single: [49450, 545500, 250000, 200000], mfj: [98900, 613700, 500000, 250000], hoh: [66200, 579600, 250000, 200000], mfs: [49450, 306850, 250000, 125000] };
  tools['capital-gains-tax-calculator'] = function (f) {
    var v = vals(f), b = CG[v.status];
    var basis = v.purchase + v.buycost + v.improve - v.dep, gain = v.sale - v.sellcost - basis;
    var recap = Math.max(0, Math.min(v.dep, gain)), excl = v.qualify === '1' ? Math.min(b[2], Math.max(0, gain - recap)) : 0;
    var taxable = Math.max(0, gain - excl), cg = Math.max(0, taxable - recap), tax = 0, note = '';
    set(f, 'basis', usd(basis)); set(f, 'gain', usd(gain)); set(f, 'excl', usd(excl)); set(f, 'taxable', usd(taxable));
    if (gain <= 0) { set(f, 'tax', '$0'); set(f, 'niit', '$0'); set(f, 'eff', '0%'); set(f, 'note', 'No gain - a loss on a personal residence is not deductible.'); return; }
    if (v.held !== '1') {
      set(f, 'tax', 'Ordinary rates'); set(f, 'niit', '-'); set(f, 'eff', '-');
      set(f, 'note', 'Homes owned one year or less produce short-term gains taxed at your ordinary income tax rate, and do not qualify for the exclusion.'); return;
    }
    var start = v.income + recap, at0 = Math.max(0, Math.min(b[0], start + cg) - start), at15 = Math.max(0, Math.min(b[1], start + cg) - Math.max(b[0], start));
    var at20 = Math.max(0, cg - at0 - at15);
    tax = at15 * 0.15 + at20 * 0.20 + recap * 0.25;
    var magi = v.income + taxable, niit = magi > b[3] ? 0.038 * Math.min(taxable, magi - b[3]) : 0;
    tax += niit;
    set(f, 'tax', usd(tax)); set(f, 'niit', usd(niit)); set(f, 'eff', taxable ? pct(tax / gain * 100) : '0%');
    if (recap) note += usd(recap) + ' of depreciation is taxed (estimated here at the 25% maximum) and cannot be excluded. ';
    if (v.qualify === '1' && taxable === 0) note += 'Your whole gain is covered by the exclusion - no federal tax, and Texas has no state income tax. ';
    if (v.qualify !== '1') note += 'Without meeting the 2-of-5-year test you may still qualify for a partial exclusion (job move, health, unforeseen events) - see IRS Publication 523. ';
    set(f, 'note', note + 'Estimate only; confirm with a CPA.');
  };

  tools['cap-rate-calculator'] = function (f) {
    var v = vals(f), egi = (v.rent + v.other) * 12 * (1 - v.vacancy / 100);
    var opex = v.tax + v.ins + v.rent * 12 * (v.mgmt + v.maint) / 100 + v.opother, noi = egi - opex;
    var value = v.target ? noi / (v.target / 100) : 0;
    set(f, 'cap', v.price ? pct(noi / v.price * 100, 2) : '-'); set(f, 'noi', usd(noi) + '/yr'); set(f, 'egi', usd(egi));
    set(f, 'opex', usd(opex)); set(f, 'ratio', egi ? pct(opex / egi * 100) : '-'); set(f, 'value', usd(value));
    set(f, 'vsprice', (value >= v.price ? '+' : '-') + usd(Math.abs(value - v.price)) + (value >= v.price ? ' (priced below)' : ' (priced above)'));
  };

  tools['house-flipping-calculator'] = function (f) {
    var v = vals(f), rehab = v.rehab * (1 + v.contingency / 100);
    var buyc = v.price * v.buyclose / 100, loan = (v.price + rehab) * v.ltc / 100, pts = loan * v.points / 100;
    var interest = loan * v.rate / 1200 * v.months, hold = v.hold * v.months, sell = v.arv * v.sellcost / 100;
    var allin = v.price + rehab + buyc + pts + interest + hold, profit = v.arv - sell - allin, cash = allin - loan;
    var roi = cash > 0 ? profit / cash : 0;
    set(f, 'profit', usd(profit)); set(f, 'mao', usd(v.arv * 0.7 - rehab)); set(f, 'allin', usd(allin)); set(f, 'cash', usd(cash));
    set(f, 'roi', cash > 0 ? pct(roi * 100) : '-');
    set(f, 'annual', cash > 0 && roi > -1 ? pct((Math.pow(1 + roi, 12 / Math.max(1, v.months)) - 1) * 100) : '-');
    set(f, 'margin', v.arv ? pct(profit / v.arv * 100) : '-');
    html(f, '[data-out-table="lines"]', table(['Item', 'Amount'], [
      ['Purchase price', usd(v.price)], ['Rehab incl. contingency', usd(rehab)], ['Buying closing costs', usd(buyc)],
      ['Loan points', usd(pts)], ['Loan interest (' + v.months + ' mo)', usd(interest)], ['Holding costs', usd(hold)],
      ['Selling costs', usd(sell)], ['Sale price (ARV)', usd(v.arv)]], ['Net profit', usd(profit)]));
  };

  function addDays(iso, n) {
    var p = String(iso || '').split('-'); if (p.length !== 3) return null;
    var d = new Date(Date.UTC(+p[0], +p[1] - 1, +p[2])); d.setUTCDate(d.getUTCDate() + n);
    return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
  }
  tools['1031-exchange-calculator'] = function (f) {
    var v = vals(f), realized = Math.max(0, v.sale - v.sellcost - v.basis);
    var equity = v.sale - v.sellcost - v.oldloan, reinvest = Math.max(0, equity - v.keep);
    var cashAdded = Math.max(0, v.newprice - v.newloan - reinvest), leftover = Math.max(0, reinvest - (v.newprice - v.newloan));
    var mortBoot = Math.max(0, (v.oldloan - v.newloan) - cashAdded), boot = v.keep + leftover + mortBoot;
    var recog = Math.min(boot, realized);
    function tax(g) { var rec = Math.min(v.dep, g); return rec * 0.25 + (g - rec) * v.cgrate / 100 + (v.niit === '1' ? g * 0.038 : 0); }
    var full = tax(realized), now = tax(recog);
    set(f, 'day45', addDays(v.closedate, 45) || '-'); set(f, 'day180', addDays(v.closedate, 180) || '-');
    set(f, 'realized', usd(realized)); set(f, 'boot', usd(recog)); set(f, 'taxnow', usd(now)); set(f, 'taxsale', usd(full));
    set(f, 'deferred', usd(full - now));
    var note = '';
    if (v.newprice < v.sale - v.sellcost) note += 'The replacement costs less than your net sale price, which usually creates boot. ';
    if (mortBoot > 0) note += 'Your new loan is ' + usd(v.oldloan - v.newloan) + ' smaller than the one paid off; add cash or borrow more to avoid mortgage boot. ';
    set(f, 'note', note + 'Day 180 is cut short if your tax return for the year of sale is due first - file an extension if needed. Recapture is estimated at the 25% maximum.');
  };

  tools['price-per-square-foot-calculator'] = function (f) {
    var v = vals(f), list = [];
    $$('.items__row', f).forEach(function (row) {
      var i = $$('input', row), p = parseFloat(i[1].value) || 0, s = parseFloat(i[2].value) || 0, o = $('output', row);
      if (p > 0 && s > 0) { list.push(p / s); o.textContent = '$' + (p / s).toFixed(2); } else o.textContent = '-';
    });
    if (!list.length) { set(f, 'indicated', '-'); return; }
    var s = list.slice().sort(function (a, b) { return a - b; }), n = s.length;
    var med = n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2, avg = list.reduce(function (a, b) { return a + b; }, 0) / n;
    var ind = med * v.sqft, diff = v.compare - ind;
    set(f, 'indicated', usd(ind)); set(f, 'median', '$' + med.toFixed(2)); set(f, 'avg', '$' + avg.toFixed(2));
    set(f, 'yours', v.sqft ? '$' + (v.compare / v.sqft).toFixed(2) : '-');
    set(f, 'diff', (diff >= 0 ? '+' : '-') + usd(Math.abs(diff)) + (v.compare ? ' (' + pct(diff / v.compare * 100) + ')' : ''));
    set(f, 'note', diff > 0 ? 'Your comparison value is ' + usd(diff) + ' above what the median comp suggests. If that is your appraisal district value, these comps may support a protest - include addresses, sale dates and photos.' : 'Your comparison value is at or below what the median comp suggests.');
  };

  /* --- home inventory --- */
  function initInventory(el) {
    var KEY = 'ere540-home-inventory', items = [];
    try { items = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { items = []; }
    var rows = $('[data-rows]', el), cols = ['room', 'item', 'model', 'serial', 'year', 'qty', 'cost'];
    function save() { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) { /* storage unavailable */ } }
    function totals() {
      var sum = 0, by = {};
      items.forEach(function (it) { var t = (parseFloat(it.qty) || 0) * (parseFloat(it.cost) || 0); sum += t; by[it.room] = by[it.room] || [0, 0]; by[it.room][0]++; by[it.room][1] += t; });
      $('[data-total]', el).textContent = usd(sum); $('[data-count]', el).textContent = items.length; $('[data-rooms]', el).textContent = Object.keys(by).length;
      $('[data-byroom]', el).innerHTML = Object.keys(by).sort().map(function (r) { return '<tr><td>' + esc(r) + '</td><td class="num">' + by[r][0] + '</td><td class="num">' + usd(by[r][1]) + '</td></tr>'; }).join('');
      $('[data-empty]', el).style.display = items.length ? 'none' : '';
    }
    function render() {
      rows.innerHTML = items.map(function (it, i) {
        return '<tr data-i="' + i + '"><td>' + esc(it.room) + '</td>' +
          '<td><input data-k="item" aria-label="Item" value="' + esc(it.item || '') + '" placeholder="e.g. 65-inch TV"></td>' +
          '<td><input data-k="model" aria-label="Brand and model" value="' + esc(it.model || '') + '"></td>' +
          '<td><input data-k="serial" aria-label="Serial number" value="' + esc(it.serial || '') + '"></td>' +
          '<td><input data-k="year" aria-label="Year bought" inputmode="numeric" value="' + esc(it.year || '') + '"></td>' +
          '<td class="num"><input data-k="qty" aria-label="Quantity" type="number" min="1" value="' + esc(it.qty || 1) + '"></td>' +
          '<td class="num"><input data-k="cost" aria-label="Replacement cost each" type="number" min="0" step="10" value="' + esc(it.cost || '') + '"></td>' +
          '<td><button type="button" class="items__del" aria-label="Remove item">&times;</button></td></tr>';
      }).join('');
      totals();
    }
    $('[data-add]', el).addEventListener('click', function () {
      items.push({ room: $('[data-room]', el).value, item: '', model: '', serial: '', year: '', qty: 1, cost: '' }); save(); render();
      var last = rows.querySelector('tr:last-child input'); if (last) last.focus();
    });
    rows.addEventListener('input', function (e) {
      var tr = e.target.closest('tr'); if (!tr || !e.target.dataset.k) return;
      items[+tr.dataset.i][e.target.dataset.k] = e.target.value; save(); totals();
    });
    rows.addEventListener('click', function (e) {
      if (!e.target.classList.contains('items__del')) return;
      items.splice(+e.target.closest('tr').dataset.i, 1); save(); render();
    });
    $('[data-clear]', el).addEventListener('click', function () {
      if (items.length && window.confirm('Delete every item in your inventory? Export a CSV first if you want a backup.')) { items = []; save(); render(); }
    });
    $('[data-print]', el).addEventListener('click', function () { window.print(); });
    $('[data-csv]', el).addEventListener('click', function () {
      var q = function (s) { return '"' + String(s == null ? '' : s).replace(/"/g, '""') + '"'; };
      var lines = [['Room', 'Item', 'Brand / model', 'Serial number', 'Year bought', 'Quantity', 'Replacement cost each', 'Total'].map(q).join(',')];
      items.forEach(function (it) { lines.push(cols.map(function (c) { return q(it[c]); }).concat(q((parseFloat(it.qty) || 0) * (parseFloat(it.cost) || 0))).join(',')); });
      var blob = new Blob([lines.join('\r\n')], { type: 'text/csv;charset=utf-8' }), a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'home-inventory-' + new Date().toISOString().slice(0, 10) + '.csv';
      document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
    });
    render();
  }

  /* --- insurance depreciation: dynamic rows --- */
  function itemRow(name, cost, age, life) {
    var d = document.createElement('div');
    d.className = 'items__row';
    d.innerHTML = '<input type="text" aria-label="Item" placeholder="e.g. Kitchen cabinets" value="' + esc(name || '') + '">' +
      '<input type="number" inputmode="decimal" aria-label="Replacement cost" min="0" step="50" value="' + (cost || '') + '">' +
      '<input type="number" inputmode="decimal" aria-label="Age in years" min="0" step="0.5" value="' + (age || '') + '">' +
      '<input type="number" inputmode="decimal" aria-label="Useful life in years" min="1" step="1" value="' + (life || '') + '">' +
      '<button type="button" class="items__del" aria-label="Remove item">&times;</button>';
    return d;
  }
  function initItems(f) {
    var box = $('[data-items]', f);
    [['Asphalt shingle roof', 18000, 10, 25], ['Carpet - living room', 1800, 6, 10], ['Interior paint', 3500, 5, 8]].forEach(function (r) { box.appendChild(itemRow.apply(null, r)); });
    $('[data-add-item]', f).addEventListener('click', function () { box.appendChild(itemRow()); calc(f); });
    $('#f-preset', f).addEventListener('change', function (e) {
      if (!e.target.value) return;
      var p = e.target.value.split('|'); box.appendChild(itemRow(p[0], p[1], p[2], p[3])); e.target.value = ''; calc(f);
    });
    box.addEventListener('click', function (e) { if (e.target.classList.contains('items__del')) { e.target.parentNode.remove(); calc(f); } });
  }
  tools['insurance-claim-depreciation-calculator'] = function (f) {
    var v = vals(f), rcv = 0, dep = 0;
    $$('.items__row', f).forEach(function (row) {
      var i = $$('input', row), c = parseFloat(i[1].value) || 0, a = parseFloat(i[2].value) || 0, l = parseFloat(i[3].value) || 1;
      var rate = Math.min(a / l, v.maxdep / 100);
      rcv += c; dep += c * rate;
    });
    var acv = rcv - dep, first = Math.max(0, acv - v.deductible);
    var recov = v.policy === 'rcv' ? Math.min(dep, Math.max(0, rcv - v.deductible) - first) : 0;
    set(f, 'first', usd(first)); set(f, 'rcv', usd(rcv)); set(f, 'dep', usd(dep));
    set(f, 'acv', usd(acv)); set(f, 'recoverable', v.policy === 'rcv' ? usd(recov) : '$0 (ACV policy)');
    set(f, 'totalpay', usd(first + recov));
  };

  /* --- checklist --- */
  function initChecklist(el) {
    var key = 'ere540-' + el.getAttribute('data-tool'), state = {};
    try { state = JSON.parse(localStorage.getItem(key) || '{}'); } catch (e) { state = {}; }
    var boxes = $$('input[type=checkbox]', el);
    function update() {
      var done = boxes.filter(function (b) { return b.checked; }).length;
      $('[data-progress-text]', el).textContent = done + ' of ' + boxes.length;
      $('[data-progress-bar]', el).style.width = (done / boxes.length * 100) + '%';
    }
    boxes.forEach(function (b) {
      b.checked = !!state[b.dataset.id];
      b.addEventListener('change', function () {
        state[b.dataset.id] = b.checked;
        try { localStorage.setItem(key, JSON.stringify(state)); } catch (e) { /* storage unavailable */ }
        update();
      });
    });
    $('[data-reset]', el).addEventListener('click', function () {
      boxes.forEach(function (b) { b.checked = false; }); state = {};
      try { localStorage.removeItem(key); } catch (e) { /* ignore */ }
      update();
    });
    $('[data-print]', el).addEventListener('click', function () { window.print(); });
    update();
  }

  function calc(f) {
    var fn = tools[f.getAttribute('data-tool')];
    if (fn) { try { fn(f); } catch (e) { if (window.console) console.error(e); } }
  }

  $$('form.calc[data-tool]').forEach(function (f) {
    if (f.getAttribute('data-tool') === 'insurance-claim-depreciation-calculator') initItems(f);
    f.addEventListener('input', function () { calc(f); });
    f.addEventListener('change', function () { calc(f); });
    f.addEventListener('submit', function (e) { e.preventDefault(); calc(f); });
    calc(f);
  });
  $$('.checklist[data-tool]').forEach(initChecklist);
  $$('.inventory[data-tool]').forEach(initInventory);
})();
