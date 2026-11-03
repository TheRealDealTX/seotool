(function () {
  var form = document.getElementById('qet-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var kids = +v('kids') || 0;
    var r = C.estimate({
      year: yr, status: s, wages: v('wages'), seIncome: v('seIncome'), seExpenses: v('seExpenses'),
      otherIncome: v('otherIncome'), otherAdjustments: v('adjust'), itemized: v('itemized'), kids: kids
    });
    // Refundable Additional Child Tax Credit (Schedule 8812): unused CTC, capped per child and at 15% of earned income over $2,500.
    var seNet = Math.max(0, v('seIncome') - v('seExpenses'));
    var ctcAllowed = kids ? C.ctc(kids, r.agi, s, yr) : 0;
    var ctcUsed = Math.min(ctcAllowed, r.incomeTaxBeforeCredits);
    var earned = v('wages') + Math.max(0, seNet - r.se.half);
    var actc = Math.max(0, Math.min(ctcAllowed - ctcUsed, kids * d.ctc.refundable, 0.15 * Math.max(0, earned - 2500)));
    var tax = Math.max(0, r.incomeTax + r.se.total + r.niit - actc);

    var farmer = C.val(f, 'farmer'), fullYear = C.val(f, 'fullYear');
    var priorKnown = C.str(f, 'priorTax').trim() !== '';
    var priorTax = Math.max(0, v('priorTax')), priorAgi = v('priorAgi');
    var highInc = priorAgi > (s === 'mfs' ? 75000 : 150000);
    var priorPct = farmer ? 1 : highInc ? 1.1 : 1;
    var curPct = farmer ? 2 / 3 : 0.9;
    var curReq = tax * curPct;
    var priorOk = priorKnown && fullYear;
    var priorReq = priorOk ? priorTax * priorPct : Infinity;
    var firstYear = priorOk && priorTax === 0;
    var required = firstYear ? 0 : Math.min(curReq, priorReq);
    var method = firstYear ? 'first-year exception' : priorReq <= curReq ? Math.round(priorPct * 100) + '% of last year’s tax' : (farmer ? '66⅔%' : '90%') + ' of this year’s tax';
    var withheld = v('withheld'), paid = v('paid');
    var smallBal = tax - withheld < 1000;
    var plan = C.str(f, 'plan');
    var target = plan === 'full' ? tax : required;
    var need = plan === 'safe' && (smallBal || firstYear) ? 0 : Math.max(0, target - withheld);
    var perQ = need / 4;
    var left = Math.max(0, need - paid);
    var bal = tax - withheld - Math.max(paid, need);

    C.set(tool, 'label', plan === 'full' ? 'Payment per quarter to owe $0 at filing' : 'Minimum payment per quarter to avoid a penalty');
    C.big(tool, 'perq', perQ);
    var sub;
    if (firstYear) sub = 'No penalty possible: you had no tax last year (first-year exception). ' + (plan === 'full' ? '' : 'Still set aside ' + C.money(Math.max(0, tax - withheld) / 4) + ' a quarter for the bill.');
    else if (smallBal) sub = 'You’ll owe under $1,000 after withholding — estimated payments aren’t required.';
    else if (plan === 'full') sub = 'Covers your full projected tax; the penalty-free minimum is ' + C.money(Math.max(0, required - withheld) / 4) + ' a quarter.';
    else sub = 'Based on ' + method + (priorKnown ? '' : ' — enter last year’s tax to check the prior-year safe harbor') + '.';
    C.set(tool, 'sub', sub);
    C.set(tool, 'yr', String(yr));
    C.set(tool, 'tax', C.money(tax));
    C.set(tool, 'req', C.money(required));
    C.set(tool, 'left', C.money(left));
    C.set(tool, 'balLabel', bal >= 0 ? 'Due when you file' : 'Projected refund');
    C.set(tool, 'bal', C.money(Math.abs(bal)));

    // Quarter schedule: payments already made are applied to the earliest installments.
    var pool = paid, now = new Date();
    C.$('[data-quarters]', tool).innerHTML = d.quarterlyDue.map(function (date, i) {
      var applied = Math.min(pool, perQ); pool -= applied;
      var owe = perQ - applied, status;
      var passed = false; try { var dt = new Date(date); passed = !isNaN(dt) && dt < now; } catch (e) {}
      if (perQ <= 0) status = 'Nothing due';
      else if (owe < 0.5) status = 'Covered ✓';
      else if (applied > 0) status = C.money(owe) + ' still due' + (passed ? ' — pay now' : '');
      else status = passed ? 'Past due — pay now' : 'Due';
      return '<div><small>Q' + (i + 1) + ' · ' + date + '</small><b>' + C.money(perQ) + '</b><small>' + status + '</small></div>';
    }).join('');

    var rows = [
      ['Income tax after credits', C.money(r.incomeTax)],
      ['Self-employment tax', C.money(r.se.total)]
    ];
    if (r.niit) rows.push(['Net investment income tax', C.money(r.niit)]);
    if (actc) rows.push(['Refundable child tax credit', '−' + C.money(actc)]);
    rows.push(['Projected total tax', C.money(tax)]);
    rows.push([(farmer ? '66⅔%' : '90%') + ' of this year’s tax', C.money(curReq), 1]);
    rows.push([priorOk ? Math.round(priorPct * 100) + '% of last year’s tax' : 'Prior-year safe harbor', priorOk ? C.money(priorReq) : 'n/a', 1]);
    rows.push(['Required annual payment (smaller)', C.money(required)]);
    if (withheld) rows.push(['Withholding (treated as paid evenly)', '−' + C.money(withheld)]);
    rows.push([plan === 'full' ? 'Estimated payments to owe $0' : 'Estimated payments needed', C.money(need)]);
    if (paid) rows.push(['Payments already made', '−' + C.money(paid), 1]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Still to pay this year</span><b>' + C.money(left) + '</b></li>';
  });
})();
