(function () {
  var form = document.getElementById('uppen-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var DAY = 864e5;
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  function parseDue(s) {
    var m = /^([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})$/.exec(String(s).trim());
    return m ? Date.UTC(+m[3], MONTHS.indexOf(m[1]), +m[2]) : NaN;
  }
  function iso(t) { return new Date(t).toISOString().slice(0, 10); }
  function fromIso(s) { var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || ''); return m ? Date.UTC(+m[1], +m[2] - 1, +m[3]) : NaN; }
  function shortDate(t) { return new Date(t).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' }); }
  function leap(y) { return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0; }
  /* Interest on `amt` for each day after `from` through `to`, at the rate of the calendar quarter the day falls in. */
  function interest(amt, from, to, Y, rates) {
    var p = 0;
    for (var t = from + DAY; t <= to; t += DAY) {
      var d = new Date(t), yr = d.getUTCFullYear(), m = d.getUTCMonth();
      var i = yr <= Y ? (m < 6 ? 0 : m < 9 ? 1 : 2) : (m < 3 ? 3 : 4);
      p += amt * rates[i] / (leap(yr) ? 366 : 365);
    }
    return p;
  }
  var dateInputs = C.$$('[data-pdate]', form);

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var Y = +C.str(f, 'year'), d = C.year(Y), status = C.str(f, 'status');
    var due = d.quarterlyDue.map(parseDue);
    var end = Date.UTC(Y + 1, 3, 15);

    // Keep payment dates and rate labels in step with the tax year.
    if (form.dataset.y !== String(Y)) {
      if (form.dataset.y) dateInputs.forEach(function (el, i) { el.value = iso(due[i]); });
      form.dataset.y = String(Y);
      ['Apr – Jun ' + Y, 'Jul – Sep ' + Y, 'Oct – Dec ' + Y, 'Jan – Mar ' + (Y + 1), 'Apr 1 – 15, ' + (Y + 1)].forEach(function (t, i) { C.set(tool, 'rl' + (i + 1), t); });
      C.$$('label[for^="f-pay"]', form).forEach(function (l, i) { if (l.firstChild && l.firstChild.nodeType === 3) l.firstChild.nodeValue = 'Q' + (i + 1) + ' payment (due ' + d.quarterlyDue[i].replace(/, \d{4}$/, '') + ') '; });
    }

    var actual = !!v('actualWh');
    C.$('#up-wh-actual', form).hidden = !actual;
    C.$('#up-wh-total', form).hidden = actual;
    var whPer = actual ? [v('wh1'), v('wh2'), v('wh3'), v('wh4')] : [0, 0, 0, 0].map(function () { return v('withheld') / 4; });
    var wh = whPer.reduce(function (a, b) { return a + b; }, 0);
    var prior = C.str(f, 'prior');
    C.$('#up-prior-fields', form).hidden = prior !== 'filed';

    var tax = Math.max(0, v('tax'));
    var limit = status === 'mfs' ? 75000 : 150000;
    var factor = v('priorAgi') > limit ? 1.10 : 1.00;
    var cur90 = tax * 0.9, priorReq = v('priorTax') * factor;
    var rap = prior === 'filed' ? Math.min(cur90, priorReq) : cur90;
    var basis = prior === 'filed' && priorReq < cur90 ? Math.round(factor * 100) + '% of last year’s tax' : '90% of this year’s tax';
    var inst = rap / 4;
    var rates = [1, 2, 3, 4, 5].map(function (n) { return Math.max(0, v('r' + n)) / 100; });

    var pays = [], est = 0;
    due.forEach(function (t, i) { if (whPer[i] > 0) pays.push({ amt: whPer[i], t: t, k: 0 }); });
    for (var n = 1; n <= 4; n++) {
      var amt = v('pay' + n);
      if (amt <= 0) continue;
      var t = fromIso(dateInputs[n - 1] && dateInputs[n - 1].value);
      pays.push({ amt: amt, t: isFinite(t) ? t : due[n - 1], k: 1 });
      est += amt;
    }
    pays.sort(function (a, b) { return a.t - b.t || a.k - b.k; });

    var rem = [inst, inst, inst, inst], pen = [0, 0, 0, 0], onTime = [0, 0, 0, 0], lateAmt = 0, unpaidAmt = 0;
    pays.forEach(function (p) {
      var a = p.amt;
      for (var i = 0; i < 4 && a > 0.004; i++) {
        if (rem[i] <= 0.004) continue;
        var use = Math.min(a, rem[i]);
        rem[i] -= use; a -= use;
        if (p.t > due[i]) { pen[i] += interest(use, due[i], Math.min(p.t, end), Y, rates); if (p.t <= end) lateAmt += use; else unpaidAmt += use; }
        else onTime[i] += use;
      }
    });
    rem.forEach(function (r, i) { if (r > 0.004) { pen[i] += interest(r, due[i], end, Y, rates); unpaidAmt += r; } });
    var jan31 = !!v('jan31');
    if (jan31) pen[3] = 0;

    // Exceptions
    var exc = '';
    if (tax <= 0) exc = 'No tax for the year — no penalty.';
    else if (prior === 'zero') exc = 'Exception: you had no tax liability for a full 12-month prior year, so no penalty applies.';
    else if (tax - wh < 1000) exc = 'Exception: tax minus withholding is under $1,000 (' + C.money(Math.max(0, tax - wh)) + '), so no penalty applies.';
    var total = exc ? 0 : pen.reduce(function (a, b) { return a + b; }, 0);
    var short = onTime.map(function (x) { return Math.max(0, inst - x); });
    var bal = tax - wh - est;

    var big = C.$('[data-out="pen"]', tool);
    big.classList.toggle('good', total < 0.005);
    big.classList.toggle('bad', total >= 0.005);
    C.big(tool, 'pen', total, function (x) { return C.money(x, 2); });
    var summary;
    if (exc) summary = exc;
    else if (total < 0.005) summary = 'Every installment was covered on time — no penalty. Safe harbor: ' + basis + '.';
    else summary = 'Required payments are based on ' + basis + '. ' + short.filter(function (s) { return s > 0.004; }).length + ' of 4 installments were short on their due date.';
    C.set(tool, 'summary', summary);
    C.set(tool, 'rap', C.money(rap));
    C.set(tool, 'inst', C.money(inst));
    C.set(tool, 'lateAmt', C.money(exc ? 0 : lateAmt + unpaidAmt));
    C.set(tool, 'bal', bal >= 0 ? C.money(bal) : 'Refund ' + C.money(-bal));

    C.$('[data-quarters]', tool).innerHTML = due.map(function (t, i) {
      var p = exc ? 0 : pen[i];
      var sub = short[i] > 0.004 ? 'short ' + C.money(short[i]) + (i === 3 && jan31 ? ' · waived (Jan 31)' : '') : 'paid on time';
      return '<div><small>Q' + (i + 1) + ' · ' + shortDate(t) + '</small><b>' + C.money(p, 2) + '</b><small>' + sub + '</small></div>';
    }).join('');

    var paidOn = onTime.reduce(function (a, b) { return a + b; }, 0);
    var segs = [
      { label: 'Paid on time', value: paidOn, color: '#10b981' },
      { label: 'Paid late', value: lateAmt, color: '#f59e0b' },
      { label: 'Unpaid by Apr 15', value: unpaidAmt, color: '#e11d48' }
    ].filter(function (x) { return x.value > 0.5; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [
      ['This year’s total tax', C.money(tax)],
      ['90% of this year’s tax', C.money(cur90), 'sub']
    ];
    if (prior === 'filed') rows.push([Math.round(factor * 100) + '% of last year’s tax' + (factor > 1 ? ' (AGI over ' + C.money(limit) + ')' : ''), C.money(priorReq), 'sub']);
    rows.push(['Required annual payment', C.money(rap)]);
    rows.push(['Withholding' + (actual ? ' (actual dates)' : ' (25% per due date)'), C.money(wh)]);
    rows.push(['Estimated payments', C.money(est)]);
    if (!exc) pen.forEach(function (p, i) { if (p > 0.004 || (i === 3 && jan31 && short[3] > 0)) rows.push(['Q' + (i + 1) + ' penalty', C.money(p, 2), 'sub']); });
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Estimated penalty</span><b>' + C.money(total, 2) + '</b></li>';

    var note = 'Regular method; rates default to 7% — confirm each quarter’s rate in the IRS interest rate announcement. ';
    if (!exc && total > 0 && !actual) note += 'Back-loaded income? The annualized method (Schedule AI) may cut this. ';
    if (!exc && total > 0) note += 'Waivers are available for casualties, disasters, or retirement after 62 / disability with reasonable cause.';
    C.set(tool, 'exnote', note);
  });
})();
