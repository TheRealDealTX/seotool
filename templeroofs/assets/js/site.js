/* Temple Roofers — core site behaviour (no dependencies). */
(function () {
  'use strict';
  var doc = document.documentElement;
  // Elements already on screen stay visible (no flash) before reveal styles apply.
  document.querySelectorAll('.reveal').forEach(function (el) {
    if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add('is-visible');
  });
  doc.classList.add('js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Sticky header state ---------- */
  var header = document.querySelector('[data-header]');
  function onScroll() {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 24);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile navigation ---------- */
  var menuBtn = document.querySelector('[data-menu-btn]');
  var nav = document.getElementById('site-nav');
  var backdrop = document.createElement('div');
  backdrop.className = 'nav-backdrop';
  document.body.appendChild(backdrop);

  function setNav(open) {
    if (!nav || !menuBtn) return;
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) {
      var first = nav.querySelector('a, button');
      if (first) first.focus();
    }
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      setNav(menuBtn.getAttribute('aria-expanded') !== 'true');
    });
  }
  backdrop.addEventListener('click', function () { setNav(false); });

  /* ---------- Dropdown toggles (keyboard + touch + mobile accordion) ---------- */
  var toggles = document.querySelectorAll('.nav__toggle');
  function closeDrops(except) {
    toggles.forEach(function (t) {
      if (t === except) return;
      t.setAttribute('aria-expanded', 'false');
      t.parentElement.classList.remove('is-open');
    });
  }
  toggles.forEach(function (t) {
    t.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = t.getAttribute('aria-expanded') !== 'true';
      closeDrops(t);
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
      t.parentElement.classList.toggle('is-open', open);
    });
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.has-drop')) closeDrops(null);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var openToggle = document.querySelector('.nav__toggle[aria-expanded="true"]');
    closeDrops(null);
    if (openToggle) openToggle.focus();
    if (nav && nav.classList.contains('is-open')) { setNav(false); menuBtn.focus(); }
  });
  window.addEventListener('resize', function () {
    if (window.innerWidth > 1120 && nav && nav.classList.contains('is-open')) setNav(false);
  });

  /* ---------- FAQ accordions ---------- */
  document.querySelectorAll('.faq__q button').forEach(function (btn) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    var item = btn.closest('.faq__item');
    if (!panel) return;
    btn.addEventListener('click', function () {
      var open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      item.classList.toggle('is-open', open);
      if (reduceMotion) { panel.hidden = !open; return; }
      if (open) {
        panel.hidden = false;
        var h = panel.scrollHeight;
        panel.style.height = '0px';
        requestAnimationFrame(function () { panel.style.height = h + 'px'; });
      } else {
        panel.style.height = panel.scrollHeight + 'px';
        requestAnimationFrame(function () { panel.style.height = '0px'; });
      }
    });
    panel.addEventListener('transitionend', function () {
      if (btn.getAttribute('aria-expanded') === 'true') panel.style.height = '';
      else { panel.hidden = true; panel.style.height = ''; }
    });
  });

  /* ---------- Reveal on scroll + animated counters ---------- */
  function countUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduceMotion || target === 0) { el.textContent = target; return; }
    var start = null, dur = 1200;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = '0';
    requestAnimationFrame(step);
  }
  var revealEls = document.querySelectorAll('.reveal');
  var counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-visible');
        if (en.target.hasAttribute('data-count')) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
    counters.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Subtle parallax on hero images ---------- */
  var para = document.querySelectorAll('[data-parallax] img');
  if (para.length && !reduceMotion) {
    var ticking = false;
    var update = function () {
      var y = window.scrollY;
      para.forEach(function (img) {
        if (y < window.innerHeight * 1.2) img.style.transform = 'translate3d(0,' + (y * 0.18 - 40) + 'px,0)';
      });
      ticking = false;
    };
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- Lead forms: validation + submission ---------- */
  var phoneRe = /\d/g;
  function setError(form, name, msg) {
    var field = form.querySelector('[name="' + name + '"]');
    if (!field) return;
    var err = document.getElementById(field.id + '-err');
    if (msg) {
      field.setAttribute('aria-invalid', 'true');
      if (err) { err.textContent = msg; err.hidden = false; }
    } else {
      field.removeAttribute('aria-invalid');
      if (err) { err.textContent = ''; err.hidden = true; }
    }
  }
  function validate(form) {
    var errors = {};
    var v = function (n) { var f = form.querySelector('[name="' + n + '"]'); return f ? f.value.trim() : ''; };
    if (v('name').length < 2) errors.name = 'Please enter your name.';
    var digits = (v('phone').match(phoneRe) || []).join('');
    if (digits.length === 11 && digits[0] === '1') digits = digits.slice(1);
    if (digits.length !== 10) errors.phone = 'Please enter a 10-digit phone number, e.g. (254) 555-0123.';
    var email = v('email');
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) errors.email = 'Please enter a valid email address, or leave it blank.';
    var method = form.querySelector('[name="contact_method"]');
    if (method && method.value === 'email' && !email && !errors.email) errors.email = 'Please add your email address so we can reply by email.';
    var consent = form.querySelector('[name="consent"]');
    if (consent && !consent.checked) errors.consent = 'Please confirm we may contact you about this request.';
    ['name', 'phone', 'email', 'consent', 'address', 'details'].forEach(function (n) { setError(form, n, errors[n]); });
    return errors;
  }
  function showAlert(form, msg) {
    var a = form.querySelector('[data-form-alert]');
    if (!a) return;
    a.textContent = msg || '';
    a.hidden = !msg;
  }
  document.querySelectorAll('[data-lead-form]').forEach(function (form) {
    form.addEventListener('blur', function (e) {
      if (e.target.matches('input, select, textarea') && e.target.getAttribute('aria-invalid') === 'true') validate(form);
    }, true);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      showAlert(form, '');
      var errors = validate(form);
      var keys = Object.keys(errors);
      if (keys.length) {
        showAlert(form, 'Please correct the highlighted fields and try again.');
        var first = form.querySelector('[aria-invalid="true"]');
        if (first) first.focus();
        return;
      }
      if (!window.fetch || !window.FormData) { form.submit(); return; }
      var btn = form.querySelector('[data-submit]');
      btn.disabled = true;
      btn.classList.add('is-loading');
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' },
        credentials: 'same-origin'
      }).then(function (r) {
        return r.json().catch(function () { return { ok: false, errors: { _form: 'Unexpected server response.' } }; });
      }).then(function (data) {
        if (data && data.ok) {
          window.location.href = data.redirect || '/thank-you/';
          return;
        }
        var errs = (data && data.errors) || {};
        Object.keys(errs).forEach(function (k) { if (k !== '_form') setError(form, k, errs[k]); });
        showAlert(form, errs._form || 'Something went wrong. Please call us or try again.');
        var first = form.querySelector('[aria-invalid="true"]') || form.querySelector('[data-form-alert]');
        if (first && first.focus) first.focus();
        btn.disabled = false;
        btn.classList.remove('is-loading');
      }).catch(function () {
        showAlert(form, 'We could not reach the server. Please check your connection, or call us at (512) 297-7580.');
        btn.disabled = false;
        btn.classList.remove('is-loading');
      });
    });
  });
})();
