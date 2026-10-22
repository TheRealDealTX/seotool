/* Corpus Christi Public Adjuster — hurricane deductible + claim deadline calculators (no dependencies). */
(function () {
  'use strict';
  function num(v) { var n = parseFloat(String(v || '').replace(/[^0-9.]/g, '')); return isNaN(n) ? 0 : n; }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }

  /* ---------- Hurricane deductible calculator ---------- */
  var ded = document.querySelector('[data-ded-calc]');
  if (ded) {
    var f = ded.querySelector('form');
    var out = function (k) { return ded.querySelector('[data-o="' + k + '"]'); };
    var flatWrap = ded.querySelector('[data-flat]');
    var run = function () {
      var limit = num(f.limit.value), dmg = num(f.damage.value), type = f.type.value;
      flatWrap.hidden = type !== 'flat';
      var d = type === 'flat' ? num(f.flat.value) : limit * parseFloat(type);
      var you = Math.min(d, dmg);
      var ins = Math.max(0, dmg - d);
      if (limit) ins = Math.min(ins, limit);
      out('ded').textContent = money(d);
      out('damage').textContent = money(dmg);
      out('you').textContent = money(you);
      out('ins').textContent = money(ins);
      var share = dmg ? Math.round(you / dmg * 100) : 0;
      ded.querySelector('[data-o-gauge]').style.width = share + '%';
      out('share').textContent = dmg ? (d >= dmg
        ? 'This damage is at or below your deductible, so the policy would likely pay nothing for it.'
        : 'You would cover about ' + share + '% of this damage; the policy responds to the remaining ' + (100 - share) + '%.')
        : 'Enter your numbers to see how much of the damage you would pay.';
      var rows = '';
      [0.01, 0.02, 0.05, 0.10].forEach(function (p) {
        var dd = limit * p;
        rows += '<tr' + (String(p) === type || (type === '0.10' && p === 0.1) ? ' style="color:#ffbc7d;font-weight:700"' : '') + '><td>' + Math.round(p * 100) + '% (' + money(dd) + ')</td><td>' + money(Math.min(dd, dmg)) + '</td><td>' + money(Math.max(0, dmg - dd)) + '</td></tr>';
      });
      ded.querySelector('[data-o-table]').innerHTML = limit ? rows : '<tr><td colspan="3">Enter your Coverage A limit.</td></tr>';
    };
    f.addEventListener('input', run);
    f.addEventListener('change', run);
    f.addEventListener('reset', function () { setTimeout(run, 0); });
    ded.querySelector('[data-example]').addEventListener('click', function () { f.limit.value = '300,000'; f.type.value = '0.02'; f.damage.value = '18,000'; run(); });
    run();
  }

  /* ---------- Claim deadline calculator ---------- */
  var dl = document.querySelector('[data-deadline-calc]');
  if (dl) {
    var form = dl.querySelector('form');
    var list = dl.querySelector('[data-deadlines]');
    var rules = JSON.parse(dl.getAttribute('data-rules') || '[]');
    function addDays(d, n) { var x = new Date(d.getTime()); x.setDate(x.getDate() + n); return x; }
    function isBiz(d) { var w = d.getDay(); return w !== 0 && w !== 6; }
    function addBiz(d, n) { var x = new Date(d.getTime()); while (n > 0) { x.setDate(x.getDate() + 1); if (isBiz(x)) n--; } return x; }
    function addYears(d, n) { var x = new Date(d.getTime()); x.setFullYear(x.getFullYear() + n); return x; }
    function parse(v) { if (!v) return null; var p = v.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
    function fmt(d) { return d.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); }
    var run2 = function () {
      var base = { loss: parse(form.loss.value), notice: parse(form.notice.value), docs: parse(form.docs.value), decision: parse(form.decision.value) };
      var kind = form.kind.value;
      var cat = form.cat && form.cat.checked;
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var items = [];
      rules.forEach(function (r) {
        if (r.applies && r.applies.indexOf(kind) === -1) return;
        var from = base[r.from];
        if (!from) { items.push({ r: r, date: null }); return; }
        var n = r.n + (cat && r.cat ? r.cat : 0);
        var d = r.unit === 'biz' ? addBiz(from, n) : r.unit === 'years' ? addYears(from, n) : addDays(from, n);
        if (r.plus) d = addDays(d, r.plus);
        items.push({ r: r, date: d });
      });
      items.sort(function (a, b) { return (a.date ? a.date.getTime() : 9e15) - (b.date ? b.date.getTime() : 9e15); });
      var nextSet = false;
      list.innerHTML = items.map(function (it) {
        var cls = '';
        if (it.date && it.date < today) cls = 'is-past';
        else if (it.date && !nextSet) { cls = 'is-next'; nextSet = true; }
        var when = it.date ? fmt(it.date) + (it.date >= today ? ' · in ' + Math.round((it.date - today) / 86400000) + ' days' : ' · passed') : 'Enter the ' + it.r.fromLabel + ' to calculate';
        return '<li class="' + cls + '"><b>' + it.r.label + '</b><span class="when">' + when + '</span><small>' + it.r.note + '</small></li>';
      }).join('');
    };
    form.addEventListener('input', run2);
    form.addEventListener('change', run2);
    run2();
  }
})();
