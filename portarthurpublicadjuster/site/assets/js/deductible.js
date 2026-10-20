/* Hurricane / wind & hail deductible calculator. Runs entirely in the browser. */
(function () {
  'use strict';
  var root = document.querySelector('[data-deductible]');
  if (!root) return;
  var form = root.querySelector('[data-ded-form]');
  function num(name) {
    var el = form.querySelector('[name="' + name + '"]');
    var n = parseFloat(((el && el.value) || '').replace(/[^0-9.]/g, ''));
    return isNaN(n) ? null : n;
  }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function out(k, v) { var el = root.querySelector('[data-out="' + k + '"]'); if (el) el.textContent = v; }
  function pct() {
    var r = form.querySelector('[name="pct"]:checked');
    if (!r) return null;
    if (r.value === 'custom') return num('custom');
    return parseFloat(r.value);
  }
  function update() {
    var cova = num('cova'), p = pct(), flat = num('flat'), loss = num('loss');
    var custom = form.querySelector('[name="pct"]:checked').value === 'custom';
    root.querySelector('[data-custom]').hidden = !custom;
    var warn = root.querySelector('[data-warn]');
    warn.hidden = true;
    if (!cova || p === null) {
      out('ded', '$0'); out('ded-note', !cova ? 'Enter your dwelling limit' : 'Enter a percentage');
      ['flat', 'diff', 'pay', 'absorb'].forEach(function (k) { out(k, '—'); });
      root.querySelector('[data-compare]').innerHTML = '<tr><td colspan="3" class="muted">Enter a dwelling limit to compare.</td></tr>';
      bars(0, 0);
      return;
    }
    if (p > 25) { warn.textContent = 'That percentage looks unusually high—double-check your declarations page.'; warn.hidden = false; }
    var ded = cova * p / 100;
    out('ded', money(ded));
    out('ded-note', p + '% of ' + money(cova) + ' Coverage A');
    out('flat', flat !== null ? money(flat) : '—');
    out('diff', flat !== null ? (ded >= flat ? '+' : '−') + money(Math.abs(ded - flat)) : '—');
    if (loss !== null) {
      var pay = Math.max(0, loss - ded), absorb = Math.min(loss, ded);
      out('pay', money(pay)); out('absorb', money(absorb));
      bars(pay, absorb);
      if (loss <= ded) { warn.textContent = 'This damage is at or below your deductible, so the policy would likely pay nothing for it. A professional estimate sometimes finds damage that was missed—get one before deciding not to file.'; warn.hidden = false; }
    } else {
      out('pay', '—'); out('absorb', '—'); bars(0, 0);
    }
    var rows = [1, 2, 3, 5, 10].map(function (q) {
      var d = cova * q / 100;
      var cls = Math.abs(q - p) < 1e-9 ? ' class="is-current"' : '';
      return '<tr' + cls + '><td>' + q + '%</td><td>' + money(d) + '</td><td>' + (loss !== null ? money(Math.max(0, loss - d)) : '—') + '</td></tr>';
    });
    root.querySelector('[data-compare]').innerHTML = rows.join('');
  }
  function bars(pay, absorb) {
    var t = pay + absorb;
    root.querySelector('[data-bar="pay"]').style.width = (t ? pay / t * 100 : 0) + '%';
    root.querySelector('[data-bar="absorb"]').style.width = (t ? absorb / t * 100 : 0) + '%';
  }
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  form.querySelectorAll('.input-money input').forEach(function (el) {
    el.addEventListener('blur', function () {
      var n = parseFloat((el.value || '').replace(/[^0-9.]/g, ''));
      if (!isNaN(n)) el.value = Math.round(n).toLocaleString('en-US');
    });
  });
  form.addEventListener('reset', function () { setTimeout(update, 0); });
  root.querySelector('[data-example]').addEventListener('click', function () {
    form.querySelector('[name="cova"]').value = '250,000';
    form.querySelector('[name="pct"][value="2"]').checked = true;
    form.querySelector('[name="flat"]').value = '1,000';
    form.querySelector('[name="loss"]').value = '18,000';
    update();
  });
  root.querySelector('[data-print]').addEventListener('click', function () {
    var d = root.querySelector('[data-print-date]'); if (d) d.textContent = new Date().toLocaleDateString();
    window.print();
  });
  update();
})();
