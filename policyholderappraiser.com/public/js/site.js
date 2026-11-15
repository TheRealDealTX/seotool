/* policyholderappraiser.com - header shadow, mobile nav, async contact form. */
(function () {
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.site-nav');

  function onScroll() {
    if (header) header.classList.toggle('scrolled', window.scrollY > 8);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) toggle.click();
    });
  }

  document.querySelectorAll('form[data-contact]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var button = form.querySelector('button[type="submit"]');
      var data = new FormData(form);
      data.append('page', location.pathname);
      if (button) { button.disabled = true; button.textContent = 'Sending...'; }
      fetch(form.getAttribute('action'), { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().then(function (j) { return { ok: r.ok && j.ok, msg: j.message }; }); })
        .then(function (res) {
          if (res.ok) { window.location.href = '/thank-you/'; return; }
          throw new Error(res.msg || 'Could not send');
        })
        .catch(function (err) {
          if (status) { status.className = 'form-status err'; status.textContent = (err.message || 'Something went wrong.') + ' Please call or text (832) 503-5866.'; }
          if (button) { button.disabled = false; button.textContent = form.getAttribute('data-label') || 'Send'; }
        });
    });
  });
})();
