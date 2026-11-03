(function () {
  var form = document.getElementById('mileage-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  /* Non-business rates aren't in tax.json: medical/moving per IRS notices; charity is fixed by statute at 14¢. */
  var OTHER = { '2026': { medical: 0.205, moving: 0.205, charity: 0.14 }, '2025': { medical: 0.21, moving: 0.21, charity: 0.14 } };
  var LABEL = { business: 'Business', medical: 'Medical', moving: 'Military moving', charity: 'Charity' };
  function defRate(yr, p) {
    if (p === 'business') return C.year(yr).mileage;
    var o = OTHER[String(yr)] || OTHER['2026'];
    return o[p] || 0;
  }
  var rateEl = form.elements.rate;
  function resetRate() { rateEl.value = +(defRate(C.val(form, 'year'), C.str(form, 'purpose')) * 100).toFixed(1); }
  form.elements.year.addEventListener('change', resetRate);
  C.$$('input[name="purpose"]', form).forEach(function (r) { r.addEventListener('change', resetRate); });
  try {
    var q = new URLSearchParams(location.search);
    if ((q.has('year') || q.has('purpose')) && !q.has('rate')) {
      if (q.has('year')) form.elements.year.value = q.get('year');
      C.$$('input[name="purpose"]', form).forEach(function (r) { r.checked = r.value === (q.get('purpose') || 'business'); });
      resetRate();
    }
  } catch (e) {}

  // Trip log rows
  var list = C.$('[data-trips]', form), n = 0;
  function addTrip(desc, miles, rt) {
    n++;
    var row = document.createElement('div');
    row.className = 'grid-3';
    row.setAttribute('data-trip', '');
    row.innerHTML =
      '<div class="field"><label for="trip-d' + n + '">Trip ' + n + '</label><div class="inp"><input id="trip-d' + n + '" type="text" placeholder="Client visit, supply run…" value="' + (desc || '') + '"></div></div>' +
      '<div class="field"><label for="trip-m' + n + '">Miles (one way)</label><div class="inp"><input id="trip-m' + n + '" inputmode="decimal" data-trip-miles placeholder="0" value="' + (miles || '') + '"></div></div>' +
      '<div class="field"><span class="lbl">Options</span><label class="check" style="margin:8px 0 0"><input type="checkbox" data-trip-rt' + (rt ? ' checked' : '') + '> Round trip</label>' +
      '<button type="button" class="btn-ghost" data-trip-del aria-label="Remove trip ' + n + '">Remove</button></div>';
    list.appendChild(row);
    row.querySelector('[data-trip-del]').addEventListener('click', function () { row.remove(); form.dispatchEvent(new Event('change')); });
  }
  C.$('[data-add-trip]', form).addEventListener('click', function () { addTrip(); form.dispatchEvent(new Event('change')); var i = list.lastElementChild.querySelector('input'); if (i) i.focus(); });

  CPA.bind(form, function (f) {
    var v = function (k) { return C.val(f, k); };
    var yr = v('year'), purpose = C.str(f, 'purpose') || 'business', biz = purpose === 'business';
    var rate = (rateEl.value === '' ? defRate(yr, purpose) * 100 : C.num(rateEl.value)) / 100;
    var tripMiles = 0, trips = 0;
    C.$$('[data-trip]', list).forEach(function (row) {
      var m = C.num(row.querySelector('[data-trip-miles]').value);
      if (m > 0) { trips++; tripMiles += m * (row.querySelector('[data-trip-rt]').checked ? 2 : 1); }
    });
    var miles = v('miles') + tripMiles;
    var parking = v('parking');
    var std = miles * rate + parking;
    C.set(tool, 'rateHint', LABEL[purpose] + ' rate for ' + yr + ': ' + (defRate(yr, purpose) * 100).toFixed(1).replace(/\.0$/, '') + '¢ per mile' + (purpose === 'business' ? '' : ' — confirm on irs.gov'));
    C.$('[data-actual-wrap]', f).hidden = !biz;

    // Actual expense method (business only)
    var total = Math.max(v('totalMiles'), miles), pctBiz = total > 0 ? miles / total : 0;
    var costs = v('gas') + v('insurance') + v('repairs') + v('depr') + v('reg') + v('otherCar');
    var actual = biz && costs > 0 ? costs * pctBiz + parking : 0;
    var best = Math.max(std, actual), useActual = actual > std;

    // Tax savings estimate
    var marg = (+v('marginal') || 0) / 100, st = C.clamp(v('state'), 0, 20) / 100;
    var seOn = biz && v('se');
    var seSaved = seOn ? best * 0.9235 * 0.153 : 0;
    var fedSaved = (best - seSaved / 2) * marg;
    var stSaved = best * st;
    var saved = fedSaved + seSaved + stSaved;

    var reimb = v('reimb');
    C.big(tool, 'ded', best);
    C.set(tool, 'dedLabel', biz ? 'Your mileage deduction' : (purpose === 'charity' ? 'Charitable mileage deduction' : purpose === 'medical' ? 'Medical mileage (before 7.5% AGI floor)' : 'Moving mileage deduction'));
    C.set(tool, 'summary', miles.toLocaleString('en-US') + ' miles × ' + (rate * 100).toFixed(1).replace(/\.0$/, '') + '¢' + (parking ? ' + ' + C.money(parking) + ' parking & tolls' : '') +
      (biz && actual ? ' · ' + (useActual ? 'actual expenses win by ' + C.money(actual - std) : 'standard rate wins by ' + C.money(std - actual)) : ''));
    C.set(tool, 'kStd', C.money(std));
    C.set(tool, 'kAct', biz && actual ? C.money(actual) : '—');
    C.set(tool, 'kSave', C.money(saved));
    C.set(tool, 'kPct', biz && v('totalMiles') ? C.pct(pctBiz, 0) : '—');
    var mx = Math.max(std, actual, 1);
    C.$('[data-meter-std]', tool).style.width = (std / mx * 100) + '%';
    C.$('[data-meter-act]', tool).style.width = (actual / mx * 100) + '%';

    var rows = [['Logged miles', v('miles').toLocaleString('en-US')]];
    if (trips) rows.push(['Trip log (' + trips + ' trip' + (trips > 1 ? 's' : '') + ')', '+' + tripMiles.toLocaleString('en-US') + ' mi']);
    rows.push(['Total ' + LABEL[purpose].toLowerCase() + ' miles', miles.toLocaleString('en-US')]);
    rows.push(['Standard mileage (× ' + (rate * 100).toFixed(1).replace(/\.0$/, '') + '¢)', C.money(miles * rate)]);
    if (parking) rows.push(['Parking & tolls', C.money(parking)]);
    if (biz && actual) {
      rows.push(['Actual car costs', C.money(costs)]);
      rows.push(['× business use ' + C.pct(pctBiz, 1), C.money(costs * pctBiz), 'sub']);
    }
    if (reimb) {
      var diff = reimb - std;
      rows.push(['Reimbursed by employer', C.money(reimb)]);
      rows.push([diff > 0 ? 'Excess over IRS rate (taxable wages)' : 'Shortfall vs IRS rate', C.money(Math.abs(diff)), 'sub']);
    }
    if (seSaved) rows.push(['Self-employment tax saved', C.money(seSaved)]);
    rows.push(['Federal income tax saved (' + Math.round(marg * 100) + '%)', C.money(fedSaved)]);
    if (stSaved) rows.push(['State tax saved', C.money(stSaved)]);
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Deduction (' + (useActual ? 'actual expense' : 'standard mileage') + ' method)</span><b>' + C.money(best) + '</b></li>';

    var segs = [
      { label: 'Federal income tax saved', value: fedSaved, color: '#0e7490' },
      { label: 'Self-employment tax saved', value: seSaved, color: '#f59e0b' },
      { label: 'State tax saved', value: stSaved, color: '#6366f1' },
      { label: 'Rest of deduction (not cash back)', value: Math.max(0, best - saved), color: '#cbd5e1' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var notes = {
      business: useActual ? 'Actual expenses give the bigger deduction. Remember: if you use actual expenses (with MACRS depreciation) in the first year a car is used for business, you can’t switch that car to the standard rate later.' :
        'The standard mileage rate gives the bigger deduction. Choose it in the first year you use a car for business to keep the option of switching to actual expenses later.',
      medical: 'Medical mileage is an itemized deduction: only total medical costs above 7.5% of AGI are deductible, so actual savings may be lower.',
      charity: 'Charitable mileage is fixed by law at 14¢ and is deducted only if you itemize. Starting in 2026, itemized charitable deductions are reduced by 0.5% of AGI.',
      moving: 'Only active-duty members of the Armed Forces moving under military orders can deduct moving mileage.'
    };
    C.set(tool, 'note', notes[purpose]);
  });
})();
