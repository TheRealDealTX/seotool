/* Saffron Supplement: shared behaviour (nav, evidence bars, mini dosage widget). */
(function () {
  var t = document.querySelector('.nav-toggle'), n = document.getElementById('site-nav');
  if (t && n) t.addEventListener('click', function () {
    var open = n.classList.toggle('open');
    t.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Homepage mini dosage widget.
  var mini = document.getElementById('mini-goal');
  if (mini) {
    var data = {
      mood: ['30 mg / day', '15 mg twice daily or 28–30 mg once', '4–8 weeks'],
      sleep: ['28 mg / day', '14 mg twice daily, or 28 mg 1 hr before bed', '2–4 weeks'],
      eyes: ['20 mg / day', 'Once daily with a meal', '3 months'],
      appetite: ['176 mg / day', '88 mg before lunch + dinner (Satiereal®)', '4–8 weeks'],
      pms: ['30 mg / day', '15 mg twice daily through the cycle', '2 cycles'],
      stress: ['28 mg / day', 'With breakfast or split AM/PM', '4–8 weeks']
    };
    var out = document.getElementById('mini-out');
    var upd = function () {
      var d = data[mini.value];
      out.innerHTML = '<span class="small">Research-matched dose</span><b>' + d[0] + '</b><span>' + d[1] + ' &middot; results in ~' + d[2] + '</span>';
    };
    mini.addEventListener('change', upd); upd();
  }
})();
