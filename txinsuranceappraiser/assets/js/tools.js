/* TX Insurance Appraiser — free calculators (all client-side; nothing is sent anywhere) */
(function () {
  'use strict';
  var d = document;
  var money = function (n) { return (n < 0 ? '-$' : '$') + Math.round(Math.abs(n)).toLocaleString(); };
  var num = function (f, n) { var el = f.querySelector('[name="' + n + '"]'); return el ? (parseFloat(el.value) || 0) : 0; };
  var out = function (f, k, v) { var el = f.querySelector('[data-out="' + k + '"]'); if (el) el.textContent = v; return el; };
  var bar = function (f, pct) { var el = f.querySelector('[data-out="bar"]'); if (el) el.style.width = Math.max(0, Math.min(100, pct)) + '%'; };
  function bind(f, fn) { f.addEventListener('input', fn); f.addEventListener('change', fn); fn(); }

  /* Recoverable depreciation */
  d.querySelectorAll('[data-tool="depreciation"]').forEach(function (f) {
    bind(f, function () {
      var mode = f.querySelector('[name=mode]').value;
      f.querySelectorAll('[data-show]').forEach(function (el) { el.hidden = el.getAttribute('data-show') !== mode; });
      var rcv = num(f, 'rcv'), dep;
      if (mode === 'age') { var life = Math.max(1, num(f, 'life')); dep = rcv * Math.min(1, num(f, 'age') / life); }
      else dep = Math.min(rcv, num(f, 'dep'));
      var nonPct = Math.min(100, Math.max(0, num(f, 'nonrec'))) / 100;
      var nonrec = dep * nonPct, rec = dep - nonrec, acvGross = rcv - dep;
      var ded = num(f, 'ded'), prior = num(f, 'prior');
      var acvPay = Math.max(0, acvGross - ded - prior);
      var total = Math.max(0, rcv - nonrec - ded - prior);
      out(f, 'acv', money(acvPay)); out(f, 'acvgross', money(acvGross)); out(f, 'rec', money(rec));
      out(f, 'nonrecamt', money(nonrec)); out(f, 'total', money(total));
      bar(f, total ? acvPay / total * 100 : 0);
      out(f, 'note', rec > 0
        ? 'You should receive about ' + money(acvPay) + ' now and up to ' + money(Math.min(rec, total - acvPay)) + ' more after repairs are completed and documented.'
        : 'No recoverable depreciation — this looks like ACV-only payment on these items.');
    });
  });

  /* Appraisal worth it */
  d.querySelectorAll('[data-tool="appraisal"]').forEach(function (f) {
    bind(f, function () {
      var carrier = num(f, 'carrier'), mine = num(f, 'mine'), pct = num(f, 'pct') / 100;
      out(f, 'pctlabel', Math.round(pct * 100) + '%');
      var gap = Math.max(0, mine - carrier), inc = gap * pct, award = carrier + inc;
      var type = f.querySelector('[name=feetype]').value, fee = num(f, 'fee'), feeAmt;
      if (type === 'pct_increase') feeAmt = inc * fee / 100;
      else if (type === 'pct_award') feeAmt = award * fee / 100;
      else feeAmt = fee;
      var cost = feeAmt + num(f, 'umpire') / 2, net = inc - cost;
      out(f, 'gap', money(gap)); out(f, 'award', money(award)); out(f, 'inc', money(inc)); out(f, 'cost', money(cost));
      out(f, 'net', money(net)); bar(f, inc ? net / inc * 100 : 0);
      var v = net <= 0 ? 'At these numbers appraisal costs could exceed the likely increase. Try a supplement or negotiation first — or ask us for a free second opinion.'
        : net < 2500 ? 'Marginal. Appraisal may still make sense if your evidence is strong — a free review can tell you.'
        : net < 10000 ? 'Appraisal looks worthwhile at these numbers. Gather your documentation and get a free review.'
        : 'Strong candidate for appraisal. A gap this size is worth a professional review right away.';
      out(f, 'verdict', v);
    });
  });

  /* Roof squares */
  d.querySelectorAll('[data-tool="roof"]').forEach(function (f) {
    var style = f.querySelector('[name=style]'), waste = f.querySelector('[name=waste]');
    style.addEventListener('change', function () { if (style.value !== 'custom') waste.value = style.value; });
    waste.addEventListener('input', function () { style.value = 'custom'; });
    bind(f, function () {
      var area = num(f, 'area'), len = num(f, 'len'), wid = num(f, 'wid');
      if (len && wid) area = len * wid;
      var p = num(f, 'pitch'), mult = Math.sqrt(1 + Math.pow(p / 12, 2));
      var surf = area * mult, sq = surf / 100, sqw = sq * (1 + num(f, 'waste') / 100);
      out(f, 'mult', mult.toFixed(3)); out(f, 'surf', Math.round(surf).toLocaleString() + ' sq ft');
      out(f, 'sq', sq.toFixed(1)); out(f, 'sqw', sqw.toFixed(1)); out(f, 'bundles', Math.ceil(sqw * 3));
      var c = num(f, 'carrier');
      out(f, 'cmp', !c ? 'Enter the squares from your estimate to compare.'
        : c + 0.5 < sqw ? 'Your estimate is about ' + (sqw - c).toFixed(1) + ' squares short of this calculation (' + Math.round((sqw - c) / sqw * 100) + '%). Check the measurements and waste factor.'
        : 'Your estimate’s quantity is in line with (or above) this calculation.');
    });
  });

  /* Texas deadlines */
  var HOL = {};
  function nthDow(y, m, dow, n) { var dt = new Date(y, m, 1), c = 0; while (true) { if (dt.getDay() === dow && ++c === n) return dt; dt.setDate(dt.getDate() + 1); } }
  function lastDow(y, m, dow) { var dt = new Date(y, m + 1, 0); while (dt.getDay() !== dow) dt.setDate(dt.getDate() - 1); return dt; }
  function holidays(y) {
    if (HOL[y]) return HOL[y];
    var list = [new Date(y, 0, 1), nthDow(y, 0, 1, 3), nthDow(y, 1, 1, 3), lastDow(y, 4, 1), new Date(y, 5, 19), new Date(y, 6, 4),
      nthDow(y, 8, 1, 1), nthDow(y, 9, 1, 2), new Date(y, 10, 11), nthDow(y, 10, 4, 4), new Date(y, 11, 25)];
    var s = {}; list.forEach(function (h) {
      if (h.getDay() === 6) h.setDate(h.getDate() - 1); else if (h.getDay() === 0) h.setDate(h.getDate() + 1);
      s[h.toDateString()] = 1;
    });
    return (HOL[y] = s);
  }
  function isBiz(dt) { return dt.getDay() !== 0 && dt.getDay() !== 6 && !holidays(dt.getFullYear())[dt.toDateString()]; }
  function addDays(dt, n) { var r = new Date(dt); r.setDate(r.getDate() + n); return r; }
  function addBiz(dt, n) { var r = new Date(dt); while (n > 0) { r.setDate(r.getDate() + 1); if (isBiz(r)) n--; } return r; }
  function parse(v) { if (!v) return null; var p = v.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function fmt(dt) { return dt.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); }
  d.querySelectorAll('[data-tool="deadlines"]').forEach(function (f) {
    bind(f, function () {
      var notice = parse(f.querySelector('[name=notice]').value), items = parse(f.querySelector('[name=items]').value),
          acc = parse(f.querySelector('[name=accept]').value), dem = parse(f.querySelector('[name=demand]').value),
          cat = f.querySelector('[name=cat]').checked ? 15 : 0, rows = [], today = new Date(); today.setHours(0, 0, 0, 0);
      if (notice) rows.push(['Insurer should acknowledge, begin investigating & request items', addDays(notice, 15 + cat)]);
      if (items) {
        rows.push(['Insurer should accept or reject the claim (15 business days)', addDays(addBiz(items, 15), cat)]);
        rows.push(['Latest date if the insurer properly extends (45 days)', addDays(items, 45 + cat)]);
      }
      if (acc) rows.push(['Payment due after notice of acceptance (5 business days)', addDays(addBiz(acc, 5), cat)]);
      if (dem) {
        rows.push(['Typical deadline to name appraisers (20 days — check policy)', addDays(dem, 20)]);
        rows.push(['Typical deadline for appraisers to pick an umpire (+15 days)', addDays(dem, 35)]);
      }
      var t = f.querySelector('[data-out="table"]');
      if (!rows.length) { t.innerHTML = '<tr><td>Enter the date you reported the claim to begin.</td><td></td></tr>'; return; }
      t.innerHTML = rows.map(function (r) {
        var past = r[1] < today;
        return '<tr><td>' + r[0] + '</td><td' + (past ? ' style="color:#ffb4a8"' : '') + '>' + fmt(r[1]) + (past ? ' (passed)' : '') + '</td></tr>';
      }).join('');
    });
  });

  /* Checklist with saved progress */
  d.querySelectorAll('[data-tool="checklist"]').forEach(function (f) {
    var KEY = 'txia-checklist', state = {};
    try { state = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { state = {}; }
    var boxes = f.querySelectorAll('input[data-k]');
    boxes.forEach(function (b) { b.checked = !!state[b.getAttribute('data-k')]; });
    function update() {
      var n = 0; boxes.forEach(function (b) { state[b.getAttribute('data-k')] = b.checked; if (b.checked) n++; });
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) {}
      out(f, 'count', n); out(f, 'total', boxes.length); bar(f, n / boxes.length * 100);
      f.querySelectorAll('.check-group').forEach(function (g) {
        var all = g.querySelectorAll('input'), c = g.querySelectorAll('input:checked').length;
        g.querySelector('small').textContent = c + '/' + all.length;
      });
    }
    f.addEventListener('change', update);
    var r = f.querySelector('[data-reset]');
    if (r) r.addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); update(); });
    update();
  });
})();
