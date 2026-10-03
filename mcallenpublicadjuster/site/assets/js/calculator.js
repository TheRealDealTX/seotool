/* Insurance Claim Settlement Calculator — runs entirely in the browser. */
(function () {
  'use strict';
  var root = document.querySelector('[data-calculator]');
  if (!root) return;
  var form = root.querySelector('[data-calc-form]');
  var outs = {};
  root.querySelectorAll('[data-out]').forEach(function (el) { outs[el.getAttribute('data-out')] = el; });
  var warn = root.querySelector('[data-warn]');
  var bars = { ins: root.querySelector('[data-bar="ins"]'), dep: root.querySelector('[data-bar="dep"]'), oop: root.querySelector('[data-bar="oop"]') };
  var last = null;

  function num(name) {
    var v = (form.elements[name].value || '').replace(/[^0-9.]/g, '');
    var n = parseFloat(v);
    return isFinite(n) && n > 0 ? n : 0;
  }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }

  /** Pure calculation — exported for testing as window.mpaCalc. */
  function calc(i) {
    var R = Math.max(0, i.rcv);
    var nc = Math.min(Math.max(0, i.noncov), R);
    var cov = R - nc;
    var dep = i.depmode === 'pct' ? cov * Math.min(Math.max(0, i.dep), 100) / 100 : Math.max(0, i.dep);
    dep = Math.min(dep, cov);
    var acv = cov - dep;
    var L = i.limit > 0 ? i.limit : Infinity;
    var ded = Math.max(0, i.ded);
    var initialGross = Math.min(Math.max(acv - ded, 0), L);
    var maxPay = i.rc ? Math.min(Math.max(cov - ded, 0), L) : initialGross;
    var recoverable = Math.max(0, maxPay - initialGross);
    var prev = Math.max(0, i.prev);
    var initial = Math.max(0, initialGross - prev);
    var remaining = Math.max(0, maxPay - prev);
    var total = maxPay;
    var oop = Math.max(0, R - total);
    var warnings = [];
    if (ded > 0 && ded >= cov && cov > 0) warnings.push('The deductible is equal to or larger than the covered loss, so no claim payment is estimated.');
    if (L !== Infinity && (i.rc ? cov - ded : acv - ded) > L) warnings.push('The claim exceeds the policy limit you entered; payments are capped at the limit.');
    if (prev > maxPay && maxPay > 0) warnings.push('Payments already received exceed the estimated amount owed. Review the estimate and payment letters carefully.');
    if (!i.rc && dep > 0) warnings.push('On an actual cash value basis, depreciation is not recoverable and is included in your out-of-pocket cost.');
    return { rcv: cov, dep: dep, acv: acv, initial: initial, initialGross: initialGross, recoverable: recoverable, remaining: remaining, total: total, oop: oop, full: R, noncov: nc, ded: ded, prev: prev, limit: L, warnings: warnings };
  }
  window.mpaCalc = calc;

  function inputs() {
    return {
      rcv: num('rcv'), dep: num('dep'), depmode: form.querySelector('input[name="depmode"]:checked').value,
      ded: num('ded'), prev: num('prev'), noncov: num('noncov'), limit: num('limit'), rc: form.elements.rcpolicy.checked
    };
  }
  function update() {
    var i = inputs();
    var r = calc(i);
    last = { i: i, r: r };
    outs.rcv.textContent = money(r.rcv);
    outs.dep.textContent = (r.dep ? '−' : '') + money(r.dep);
    outs.acv.textContent = money(r.acv);
    outs.initial.textContent = money(r.initial);
    outs.recoverable.textContent = money(r.recoverable);
    outs.remaining.textContent = money(r.remaining);
    outs.total.textContent = money(r.total);
    outs.oop.textContent = money(r.oop);
    var paidNow = Math.max(0, r.total - r.recoverable);
    var base = r.full || 1;
    bars.ins.style.width = (r.full ? paidNow / base * 100 : 0) + '%';
    bars.dep.style.width = (r.full ? r.recoverable / base * 100 : 0) + '%';
    bars.oop.style.width = (r.full ? r.oop / base * 100 : 0) + '%';
    warn.hidden = !r.warnings.length;
    warn.textContent = r.warnings.join(' ');
  }
  // Format money fields on blur.
  form.querySelectorAll('input[inputmode="decimal"]').forEach(function (el) {
    el.addEventListener('blur', function () {
      var pct = el.name === 'dep' && form.querySelector('input[name="depmode"]:checked').value === 'pct';
      var n = parseFloat((el.value || '').replace(/[^0-9.]/g, ''));
      if (isFinite(n) && el.value !== '') el.value = pct ? String(n) : n.toLocaleString('en-US', { maximumFractionDigits: 2 });
    });
  });
  form.addEventListener('input', update);
  form.addEventListener('change', function (e) {
    if (e.target.name === 'depmode') {
      root.querySelector('[data-dep-money]').classList.toggle('input-money', e.target.value === 'amt');
      form.elements.dep.placeholder = e.target.value === 'pct' ? '30' : '7,200';
    }
    update();
  });
  form.addEventListener('reset', function () { setTimeout(function () { root.querySelector('[data-dep-money]').classList.add('input-money'); update(); }, 0); });
  root.querySelector('[data-example]').addEventListener('click', function () {
    form.elements.rcv.value = '24,000'; form.elements.dep.value = '7,200'; form.querySelector('input[value="amt"]').checked = true;
    form.elements.ded.value = '5,000'; form.elements.prev.value = '0'; form.elements.noncov.value = '0'; form.elements.limit.value = ''; form.elements.rcpolicy.checked = true;
    root.querySelector('[data-dep-money]').classList.add('input-money');
    update();
  });
  root.querySelector('[data-print]').addEventListener('click', function () {
    var d = root.querySelector('[data-print-date]'); if (d) d.textContent = new Date().toLocaleDateString();
    window.print();
  });
  root.querySelector('[data-download]').addEventListener('click', function () {
    if (!last) update();
    var i = last.i, r = last.r;
    var lines = [
      'INSURANCE CLAIM SETTLEMENT ESTIMATE',
      'Prepared with the McAllen Public Adjuster claim calculator — ' + new Date().toLocaleString(),
      'https://mcallenpublicadjuster.com/claim-calculator/',
      '',
      'INPUTS',
      'Replacement cost (full project):   ' + money(i.rcv),
      'Depreciation:                      ' + (i.depmode === 'pct' ? i.dep + '%' : money(i.dep)),
      'Deductible:                        ' + money(i.ded),
      'Payments already received:         ' + money(i.prev),
      'Non-covered costs:                 ' + money(i.noncov),
      'Policy limit:                      ' + (i.limit ? money(i.limit) : 'Not entered'),
      'Policy basis:                      ' + (i.rc ? 'Replacement cost (recoverable depreciation)' : 'Actual cash value'),
      '',
      'RESULTS',
      'Covered replacement cost (RCV):    ' + money(r.rcv),
      'Depreciation:                      ' + money(r.dep),
      'Actual cash value (ACV):           ' + money(r.acv),
      'Estimated initial (ACV) payment:   ' + money(r.initial),
      'Potential recoverable depreciation:' + ' ' + money(r.recoverable),
      'Estimated remaining payment:       ' + money(r.remaining),
      'Total estimated proceeds:          ' + money(r.total),
      'Estimated out-of-pocket cost:      ' + money(r.oop),
      ''
    ].concat(r.warnings.length ? ['NOTES', r.warnings.join('\n'), ''] : []).concat([
      'DISCLAIMER: Educational estimate only. Not an offer, coverage decision, or guarantee.',
      'Actual settlements depend on your policy, endorsements, limits, deductibles, depreciation',
      'methods, repair deadlines, and the facts of your claim.',
      '',
      'Questions? Free Claim Review: https://mcallenpublicadjuster.com/free-claim-review/',
      'McAllen Public Adjuster · +1 (832) 503-5866 · info@mcallenpublicadjuster.com'
    ]);
    var blob = new Blob([lines.join('\r\n')], { type: 'text/plain;charset=utf-8' });
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'claim-settlement-estimate.txt';
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
  });
  update();
})();
