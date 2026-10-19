/* Homepage quick salary estimator */
(function () {
  'use strict';
  var form = document.getElementById('quick-est');
  if (!form || !window.IAS || !IAS.salary) return;
  var years = document.getElementById('q-years');
  var MIN = 30000, MAX = 230000;
  function pos(n) { return Math.max(0, Math.min(100, (n - MIN) / (MAX - MIN) * 100)); }
  function update() {
    var r = IAS.salary.estimate({
      role: form.querySelector('input[name=role]:checked').value,
      line: document.getElementById('q-line').value,
      years: +years.value,
      stateIndex: 1
    });
    document.getElementById('q-years-out').textContent = years.value + (years.value === '20' ? '+' : '');
    document.getElementById('q-mid').textContent = IAS.money(r.mid);
    document.getElementById('q-label').textContent = r.label;
    document.getElementById('q-range').textContent = IAS.money(r.low) + ' - ' + IAS.money(r.high);
    document.getElementById('q-hour').textContent = IAS.money(r.hourly).replace(/^\$/, '$') + '/hr';
    document.getElementById('q-month').textContent = IAS.money(r.monthly);
    var band = document.getElementById('q-band');
    band.style.left = pos(r.low) + '%';
    band.style.width = (pos(r.high) - pos(r.low)) + '%';
    document.getElementById('q-pin').style.left = pos(r.mid) + '%';
  }
  form.addEventListener('input', update);
  form.addEventListener('change', update);
  update();
})();
