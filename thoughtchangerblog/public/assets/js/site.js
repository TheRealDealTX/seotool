/* Thought Changer — progressive enhancement only. The site works fully without this file. */
(function () {
  'use strict';
  var doc = document.documentElement, body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('nav-open')) { body.classList.remove('nav-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
    });
  }

  /* Scroll-driven: header state, reading progress, parallax, back-to-top */
  var bar = document.querySelector('.progress span');
  var toTop = document.querySelector('.to-top');
  var prose = document.querySelector('.prose');
  var parallax = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll('.hero-bg, .cta-bg'));
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || doc.scrollTop;
    body.classList.toggle('scrolled', y > 30);
    if (toTop) toTop.classList.toggle('show', y > 900);
    if (bar) {
      var p;
      if (prose) {
        var r = prose.getBoundingClientRect();
        p = Math.min(1, Math.max(0, (-r.top + window.innerHeight * 0.3) / r.height));
      } else {
        p = y / Math.max(1, doc.scrollHeight - window.innerHeight);
      }
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
    for (var i = 0; i < parallax.length; i++) {
      var el = parallax[i], box = el.parentNode.getBoundingClientRect();
      if (box.bottom > 0 && box.top < window.innerHeight) el.style.setProperty('--parallax', (box.top * -0.12).toFixed(1) + 'px');
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* Reveal on scroll, staggered within each group */
  var reveals = document.querySelectorAll('.reveal');
  // Crawlers/renderers use very tall viewports: show everything at once there.
  var tall = window.innerHeight > 1800 || /bot|crawl|spider|lighthouse/i.test(navigator.userAgent);
  if ('IntersectionObserver' in window && !reduce && !tall) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, sibs = el.parentNode ? el.parentNode.querySelectorAll(':scope > .reveal') : [];
        var idx = Array.prototype.indexOf.call(sibs, el);
        el.style.setProperty('--d', (Math.max(0, idx) % 4) * 0.08 + 's');
        el.classList.add('in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  window.addEventListener('beforeprint', function () { reveals.forEach(function (el) { el.classList.add('in'); }); });

  /* Table of contents: highlight the section being read */
  var tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[decodeURIComponent(a.hash.slice(1))] = a; });
    var current;
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          if (current) current.classList.remove('active');
          current = map[en.target.id];
          if (current) current.classList.add('active');
        }
      });
    }, { rootMargin: '-100px 0px -65% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* Copy link */
  var copy = document.querySelector('.copy-link');
  if (copy && navigator.clipboard) {
    copy.addEventListener('click', function () {
      navigator.clipboard.writeText(copy.getAttribute('data-url')).then(function () {
        var t = copy.textContent; copy.textContent = 'Copied!'; setTimeout(function () { copy.textContent = t; }, 1800);
      });
    });
  }

  /* Amazon click tracking (GA4) */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-amz]');
    if (a && window.gtag) window.gtag('event', 'affiliate_click', { item_name: a.getAttribute('data-amz'), link_url: a.href });
  });

  /* Forms: submit in place, fall back to a normal POST without JS */
  document.querySelectorAll('form.js-ajax').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var status = form.querySelector('.form-status');
      form.classList.add('is-sending');
      if (status) { status.classList.remove('is-error'); status.textContent = 'Sending…'; }
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (status) { status.textContent = res.message; status.classList.toggle('is-error', !res.ok); }
          if (res.ok) {
            form.querySelectorAll('input:not([type=hidden]), textarea').forEach(function (i) { i.value = ''; });
            if (window.gtag) window.gtag('event', form.querySelector('[name=form]').value === 'contact' ? 'contact_submit' : 'newsletter_signup');
          }
        })
        .catch(function () {
          if (status) { status.textContent = 'Something went wrong. Please email info@thoughtchangerblog.com.'; status.classList.add('is-error'); }
        })
        .then(function () { form.classList.remove('is-sending'); });
    });
  });
})();
