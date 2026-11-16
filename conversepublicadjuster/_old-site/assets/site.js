(function () {
  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Days since the storm (Sept 11, 2026, Central Time)
  var since = document.querySelectorAll('[data-days-since]');
  if (since.length) {
    var storm = new Date('2026-09-11T22:12:00-05:00');
    var days = Math.max(0, Math.floor((Date.now() - storm.getTime()) / 86400000));
    since.forEach(function (el) { el.textContent = days; });
  }

  // Contact form: posts to contact.php on Hostinger; falls back to a phone prompt if that is unavailable
  var form = document.getElementById('claim-form');
  if (form) {
    var status = document.getElementById('form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.website && form.website.value) { return; } // honeypot
      status.className = 'form-status';
      status.textContent = 'Sending…';
      var data = new FormData(form);
      fetch(form.getAttribute('action'), { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
        .then(function (j) {
          if (j && j.ok) {
            status.className = 'form-status ok';
            status.textContent = 'Received. We will call you back today, usually within the hour during business hours.';
            form.reset();
          } else { throw new Error('bad'); }
        })
        .catch(function () {
          status.className = 'form-status err';
          status.innerHTML = 'The form could not send. Call or text <a href="tel:+18325035866">(832) 503-5866</a> and we will take it from there.';
        });
    });
  }
})();
