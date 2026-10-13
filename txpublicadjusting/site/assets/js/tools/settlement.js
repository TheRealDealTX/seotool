/* Claim settlement calculator */
(function () {
  'use strict';
  var root = document.querySelector('[data-calc]');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var state = { policy: 'rcv', dedtype: 'flat' };
  var money = function (n) { return (n < 0 ? '-' : '') + '$' + Math.round(Math.abs(n)).toLocaleString('en-US'); };
  var num = function (k) { var v = parseFloat(($('[data-in="' + k + '"]') || {}).value); return isFinite(v) ? v : 0; };
  var out = function (k, v) { root.querySelectorAll('[data-out="' + k + '"]').forEach(function (e) { e.textContent = v; }); };

  root.querySelectorAll('[data-seg]').forEach(function (seg) {
    seg.addEventListener('click', function (e) {
      var b = e.target.closest('button');
      if (!b) return;
      seg.querySelectorAll('button').forEach(function (x) { x.classList.toggle('is-on', x === b); });
      state[seg.getAttribute('data-seg')] = b.getAttribute('data-v');
      root.querySelectorAll('[data-show]').forEach(function (el) { el.hidden = el.getAttribute('data-show') !== state.dedtype; });
      calc();
    });
  });

  function deductible() {
    return state.dedtype === 'pct' ? num('covA') * num('dedpct') / 100 : num('ded');
  }

  function totalFor(rcv, dep, ded) {
    dep = Math.min(dep, rcv);
    var acv = Math.max(0, rcv - dep - ded);
    // If the deductible is larger than ACV, the remainder eats into the holdback.
    var dedLeft = Math.max(0, ded - (rcv - dep));
    var hold = state.policy === 'rcv' ? Math.max(0, dep - dedLeft) : 0;
    return { acv: acv, hold: hold, total: acv + hold, dep: dep, lost: state.policy === 'rcv' ? 0 : dep };
  }

  function calc() {
    var rcv = num('rcv'), dep = num('dep'), ded = deductible(), paid = num('paid'), fee = num('fee') / 100;
    var r = totalFor(rcv, dep, ded);
    var now = Math.max(0, r.acv - paid);
    out('now', money(now));
    out('rcvOut', money(rcv));
    out('depOut', '-' + money(r.dep));
    out('dedOut', '-' + money(Math.min(ded, rcv)));
    out('acvOut', money(r.acv));
    out('holdOut', state.policy === 'rcv' ? money(r.hold) : '$0 (ACV policy)');
    out('paidOut', paid ? '-' + money(paid) : '$0');
    out('total', money(r.total));
    out('feeLbl', (fee * 100).toFixed(1).replace('.0', '') + '%');
    out('feeLbl2', (fee * 100).toFixed(1).replace('.0', '') + '%');

    var base = Math.max(rcv, 1);
    var segs = { pay: r.acv, hold: r.hold, ded: Math.min(ded, rcv), lost: r.lost };
    Object.keys(segs).forEach(function (k) { var el = root.querySelector('[data-bar="' + k + '"]'); if (el) el.style.width = Math.max(0, segs[k] / base * 100) + '%'; });

    var rcv2 = num('rcv2'), pa = root.querySelector('[data-pa]');
    if (rcv2 > 0) {
      // Keep the same depreciation ratio for the higher scope.
      var ratio = rcv > 0 ? r.dep / rcv : 0;
      var r2 = totalFor(rcv2, rcv2 * ratio, ded);
      var feeAmt = r2.total * fee;
      var net = r2.total - feeAmt;
      pa.hidden = false;
      out('t2', money(r2.total));
      out('feeAmt', '-' + money(feeAmt));
      out('net2', money(net));
      out('diff', (net - r.total >= 0 ? '+' : '') + money(net - r.total));
    } else {
      pa.hidden = true;
    }
    var be = fee > 0 ? (fee / (1 - fee)) * 100 : 0;
    out('breakeven', fee > 0
      ? 'Break-even: at a ' + (fee * 100).toFixed(1).replace('.0', '') + '% fee, the settlement must rise by about ' + be.toFixed(1) + '% (' + money(r.total * fee / (1 - fee)) + ' here) before hiring an adjuster leaves you ahead.'
      : '');
  }

  root.addEventListener('input', calc);
  root.addEventListener('click', function (e) {
    var a = e.target.closest('[data-act]');
    if (!a) return;
    if (a.getAttribute('data-act') === 'applydep') {
      var pct = Math.min(1, num('age') / Math.max(1, num('life')));
      $('[data-in="dep"]').value = Math.round(num('rcv') * pct);
      calc();
    }
    if (a.getAttribute('data-act') === 'print') window.print();
  });
  calc();
})();
