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
      stateIndex: +document.getElementById('q-metro').value
    });
    document.getElementById('q-years-out').textContent = years.value + (years.value === '20' ? '+' : '');
    document.getElementById('q-mid').textContent = IAS.money(r.mid);
    var metro = document.getElementById('q-metro');
    document.getElementById('q-label').textContent = r.label + ' \u00b7 ' + metro.selectedOptions[0].text;
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

/* Texas claim season planner */
(function () {
  'use strict';
  var wrap = document.querySelector('[data-seasons]');
  if (!wrap) return;
  var data = JSON.parse(wrap.getAttribute('data-seasons'));
  var keys = Object.keys(data);
  var names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var level = ['Quiet', 'Some activity', 'Busy', 'Peak season'];
  var rowsEl = wrap.querySelector('.season-rows');
  var buttons = wrap.querySelectorAll('.season-month');
  // Heat strip under each month = combined intensity
  buttons.forEach(function (b) {
    var m = +b.getAttribute('data-m'), total = 0;
    keys.forEach(function (k) { total += data[k].m[m]; });
    b.querySelector('.heat').style.opacity = Math.min(1, 0.15 + total / 8);
  });
  function show(m) {
    buttons.forEach(function (b) { b.setAttribute('aria-selected', +b.getAttribute('data-m') === m ? 'true' : 'false'); });
    var peak = [];
    rowsEl.innerHTML = keys.map(function (k) {
      var v = data[k].m[m];
      if (v >= 2) peak.push(data[k].label.toLowerCase());
      return '<div class="season-row"><div><b>' + data[k].label + '</b><small>' + data[k].where + '</small></div>' +
        '<div class="season-meter">' + [1, 2, 3].map(function (i) { return '<i class="' + (v >= i ? 'on' : '') + '"></i>'; }).join('') + '</div>' +
        '<span class="season-level">' + level[v] + '</span></div>';
    }).join('');
    wrap.querySelector('.season-title').textContent = names[m] + ' in Texas';
    wrap.querySelector('.season-text').textContent = peak.length
      ? 'Expect strong claim volume from ' + peak.join(' and ') + '. Independent and CAT adjusters with a Texas license are in demand.'
      : 'A quieter month for new storm claims - a good time to get licensed, finish continuing education and join IA firm rosters before the next season.';
  }
  wrap.addEventListener('click', function (e) { var b = e.target.closest('.season-month'); if (b) show(+b.getAttribute('data-m')); });
  show(new Date().getMonth());
})();
