/* TX Public Adjusting: site interactions (no dependencies). */
(function () {
  'use strict';
  var d = document, w = window;
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header shadow + back-to-top + reading progress
  var header = d.querySelector('[data-header]');
  var totop = d.querySelector('[data-totop]');
  var prog = d.querySelector('[data-progress]');
  function onScroll() {
    var y = w.scrollY || 0;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    if (totop) totop.classList.toggle('is-on', y > 700);
    if (prog) {
      var h = d.documentElement.scrollHeight - w.innerHeight;
      prog.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
    }
  }
  w.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile drawer
  var drawer = d.querySelector('[data-drawer]');
  var burger = d.querySelector('[data-burger]');
  function setDrawer(open) {
    if (!drawer) return;
    drawer.hidden = !open;
    d.body.style.overflow = open ? 'hidden' : '';
    if (burger) burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  if (burger) burger.addEventListener('click', function () { setDrawer(true); });
  if (drawer) {
    drawer.addEventListener('click', function (e) {
      if (e.target === drawer || e.target.closest('[data-drawer-close]') || e.target.closest('a')) setDrawer(false);
    });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDrawer(false); });
  }

  // Reveal on scroll (staggered within a parent)
  var els = d.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, sibs = el.parentElement ? el.parentElement.querySelectorAll(':scope > [data-reveal]') : [];
        var i = Array.prototype.indexOf.call(sibs, el);
        el.style.transitionDelay = (i > 0 ? Math.min(i, 6) * 70 : 0) + 'ms';
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Count-up numbers
  var counters = d.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in w && !reduce) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '';
        var t0 = null;
        function step(t) {
          if (!t0) t0 = t;
          var p = Math.min(1, (t - t0) / 1200), e = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(end * e) + suf;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
        co.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { co.observe(c); });
  }

  // Table of contents: highlight the current section
  var tocLinks = d.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in w) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var to = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove('is-current'); });
          map[en.target.id].classList.add('is-current');
        }
      });
    }, { rootMargin: '-15% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = d.getElementById(id); if (h) to.observe(h); });
  }

  // Blog category filter
  var filters = d.querySelector('[data-filters]');
  if (filters) {
    filters.addEventListener('click', function (e) {
      var b = e.target.closest('[data-filter]');
      if (!b) return;
      var f = b.getAttribute('data-filter');
      filters.querySelectorAll('[data-filter]').forEach(function (x) { x.classList.toggle('is-on', x === b); });
      d.querySelectorAll('[data-filter-grid] > [data-cat], .feature[data-cat]').forEach(function (it) {
        it.classList.toggle('is-hidden', f !== 'all' && it.getAttribute('data-cat') !== f);
        it.querySelectorAll('[data-reveal]').forEach(function (r) { r.classList.add('is-in'); });
      });
    });
  }

  // Ajax forms (progressive enhancement; plain POST still works)
  d.querySelectorAll('[data-ajax-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!w.fetch || !w.FormData) return;
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var btn = form.querySelector('[type=submit]');
      var label = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { ok: false, message: 'Something went wrong. Please call us.' }; }); })
        .then(function (res) {
          if (status) {
            status.textContent = res.message;
            status.className = 'form-status ' + (res.ok ? 'is-ok' : 'is-err');
          }
          if (res.ok) {
            form.reset();
            if (w.gtag) w.gtag('event', 'generate_lead');
          }
        })
        .catch(function () {
          if (status) { status.textContent = 'Network error. Please call or text (832) 503-5866.'; status.className = 'form-status is-err'; }
        })
        .finally(function () { if (btn) { btn.disabled = false; btn.innerHTML = label; } });
    });
  });
})();
