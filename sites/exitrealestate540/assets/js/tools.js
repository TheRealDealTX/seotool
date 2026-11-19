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
})();
