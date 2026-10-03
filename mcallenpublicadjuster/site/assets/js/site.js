/* McAllen Public Adjuster — site behaviour (no dependencies). */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Mobile navigation ---- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  function closeNav() {
    document.body.classList.remove('nav-open');
    if (toggle) { toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Open menu'); }
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      if (open) { var first = nav.querySelector('a'); if (first) first.focus(); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        if (document.body.classList.contains('nav-open')) { closeNav(); toggle.focus(); }
        document.querySelectorAll('.nav-item.is-open').forEach(function (li) {
          li.classList.remove('is-open');
          var b = li.querySelector('.sub-toggle'); if (b) b.setAttribute('aria-expanded', 'false');
        });
      }
    });
    document.addEventListener('click', function (e) {
      if (document.body.classList.contains('nav-open') && !nav.contains(e.target) && !toggle.contains(e.target)) closeNav();
    });
  }
  document.querySelectorAll('.sub-toggle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var li = btn.closest('.nav-item');
      var open = !li.classList.contains('is-open');
      document.querySelectorAll('.nav-item.is-open').forEach(function (o) {
        if (o !== li) { o.classList.remove('is-open'); var b = o.querySelector('.sub-toggle'); if (b) b.setAttribute('aria-expanded', 'false'); }
      });
      li.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* ---- Sticky header state ---- */
  var header = document.getElementById('site-header');
  var ticking = false;
  var parallaxEls = reduceMotion ? [] : Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
  var timelines = Array.prototype.slice.call(document.querySelectorAll('.timeline'));
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    parallaxEls.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom > 0 && r.top < window.innerHeight) {
        el.style.transform = 'translate3d(0,' + Math.round(-r.top * 0.18) + 'px,0)';
      }
    });
    timelines.forEach(function (tl) {
      var r = tl.getBoundingClientRect();
      var vh = window.innerHeight;
      var p = Math.min(1, Math.max(0, (vh * 0.75 - r.top) / r.height));
      tl.style.setProperty('--progress', p.toFixed(3));
    });
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---- Reveal on scroll + counters ---- */
  function animateCount(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    if (isNaN(target)) return;
    var decimals = (el.getAttribute('data-count').split('.')[1] || '').length;
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduceMotion) { el.textContent = target.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix; return; }
    var start = null, dur = 1400;
    function step(ts) {
      if (!start) start = ts;
      var t = Math.min(1, (ts - start) / dur);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = (target * eased).toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix;
      if (t < 1) window.requestAnimationFrame(step);
    }
    window.requestAnimationFrame(step);
  }
  var revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .timeline li, [data-count]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-visible');
          if (en.target.hasAttribute('data-count')) animateCount(en.target);
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); if (el.hasAttribute('data-count')) animateCount(el); });
  }

  /* ---- Table of contents highlighting ---- */
  var tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove('is-current'); });
          map[en.target.id].classList.add('is-current');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* ---- Free Claim Review forms ---- */
  var forms = document.querySelectorAll('form[data-claim-form]');
  function refreshToken(form) {
    return fetch('/api/form-token.php', { credentials: 'same-origin', cache: 'no-store' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { if (j && j.token) form.querySelector('[name="csrf_token"]').value = j.token; })
      .catch(function () {});
  }
  function clearErrors(form) {
    form.querySelectorAll('.field.has-error').forEach(function (f) { f.classList.remove('has-error'); });
    form.querySelectorAll('.field-error').forEach(function (n) { n.remove(); });
    form.querySelectorAll('[aria-invalid]').forEach(function (n) { n.removeAttribute('aria-invalid'); });
  }
  function showFieldError(form, name, msg) {
    var input = form.querySelector('[name="' + name + '"]') || form.querySelector('[name="' + name + '[]"]');
    if (!input) return;
    var field = input.closest('.field');
    if (!field) return;
    field.classList.add('has-error');
    input.setAttribute('aria-invalid', 'true');
    var p = document.createElement('span');
    p.className = 'field-error';
    p.id = input.id + '-err';
    p.textContent = msg;
    input.setAttribute('aria-describedby', p.id);
    field.appendChild(p);
  }
  function setStatus(form, cls, html) {
    var s = form.querySelector('.form-status');
    s.innerHTML = '<div class="notice ' + cls + '">' + html + '</div>';
    s.focus({ preventScroll: true });
    s.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'center' });
  }
  function escapeHtml(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function validate(form) {
    var errs = {};
    var v = function (n) { var el = form.querySelector('[name="' + n + '"]'); return el ? el.value.trim() : ''; };
    if (v('full_name').length < 2) errs.full_name = 'Please enter your full name.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v('email'))) errs.email = 'Please enter a valid email address.';
    var digits = v('phone').replace(/\D/g, '');
    if (digits.length < 10 || digits.length > 15) errs.phone = 'Please enter a valid phone number, including area code.';
    if (v('location').length < 2) errs.location = 'Please enter the property city or ZIP code.';
    if (!v('claim_type')) errs.claim_type = 'Please choose a claim type.';
    if (!v('claim_status')) errs.claim_status = 'Please choose the claim status.';
    if (v('message').length < 10) errs.message = 'Please describe what happened (at least a sentence).';
    var ack = form.querySelector('[name="privacy_ack"]');
    if (ack && !ack.checked) errs.privacy_ack = 'Please confirm the privacy acknowledgement.';
    var files = form.querySelector('input[type="file"]');
    if (files && files.files.length) {
      if (files.files.length > 3) errs['attachments'] = 'Please attach no more than 3 files.';
      for (var i = 0; i < files.files.length; i++) {
        if (files.files[i].size > 8 * 1024 * 1024) { errs['attachments'] = 'Each file must be smaller than 8 MB.'; break; }
      }
    }
    return errs;
  }
  forms.forEach(function (form) {
    refreshToken(form);
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return; // let the browser post normally
      e.preventDefault();
      clearErrors(form);
      var errs = validate(form);
      var keys = Object.keys(errs);
      if (keys.length) {
        keys.forEach(function (k) { showFieldError(form, k, errs[k]); });
        setStatus(form, 'notice-error', 'Please correct the highlighted fields.');
        var firstBad = form.querySelector('[aria-invalid="true"]');
        if (firstBad) firstBad.focus();
        return;
      }
      var btn = form.querySelector('button[type="submit"]');
      var label = btn.querySelector('.btn-label');
      var orig = label.textContent;
      btn.classList.add('is-loading'); btn.disabled = true; label.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' }, credentials: 'same-origin' })
        .then(function (r) { return r.json().catch(function () { return { ok: false, message: 'Unexpected server response. Please call us instead.' }; }); })
        .then(function (res) {
          if (res.token) form.querySelector('[name="csrf_token"]').value = res.token;
          if (res.ok) {
            form.innerHTML = '<div class="form-success" role="status" tabindex="-1"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg><h3>Request received</h3><p>' + escapeHtml(res.message) + '</p></div>';
            var s = form.querySelector('.form-success'); if (s) s.focus();
            if (window.gtag) window.gtag('event', 'generate_lead', { form: 'free_claim_review' });
            return;
          }
          if (res.errors) Object.keys(res.errors).forEach(function (k) { showFieldError(form, k, res.errors[k]); });
          setStatus(form, 'notice-error', escapeHtml(res.message || 'Something went wrong. Please try again.'));
        })
        .catch(function () {
          setStatus(form, 'notice-error', 'We could not reach the server. Please check your connection or call us.');
        })
        .then(function () {
          if (form.contains(btn)) { btn.classList.remove('is-loading'); btn.disabled = false; label.textContent = orig; }
        });
    });
  });
})();
