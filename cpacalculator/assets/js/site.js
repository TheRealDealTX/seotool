/* CPA Calculator — site interactions: nav, scroll progress, reveal, parallax, counters, TOC, tabs. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Mobile nav
  var btn = d.querySelector('.nav-toggle'), nav = d.getElementById('main-nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Scroll progress, header shadow, parallax floaters
  var bar = d.querySelector('.scroll-progress'), hdr = d.querySelector('.site-header');
  var floaters = d.querySelectorAll('.floaters span');
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || 0, h = root.scrollHeight - innerHeight;
    if (bar) bar.style.setProperty('--p', h > 0 ? Math.min(1, y / h) : 0);
    if (hdr) hdr.classList.toggle('scrolled', y > 8);
    if (!reduce && y < 1200) for (var i = 0; i < floaters.length; i++) floaters[i].style.setProperty('--sy', y + 'px');
    ticking = false;
  }
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // Reveal + one-shot animations (stairs, timeline, counters)
  function count(el) {
    var to = parseFloat(el.dataset.count), dp = (el.dataset.count.split('.')[1] || '').length;
    var pre = el.dataset.pre || '', suf = el.dataset.suf || '';
    var fmt = function (n) { return el.hasAttribute('data-plain') ? String(Math.round(n)) : n.toLocaleString('en-US', { minimumFractionDigits: dp, maximumFractionDigits: dp }); };
    if (reduce) { el.textContent = pre + fmt(to) + suf; return; }
    var t0 = null;
    (function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / 1400), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + fmt(to * e) + suf;
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }
  var targets = d.querySelectorAll('.reveal, .stairs, .timeline, [data-count]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add('in');
        if (el.dataset.count) count(el);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    targets.forEach(function (el) { io.observe(el); });
  } else targets.forEach(function (el) { el.classList.add('in'); if (el.dataset.count) count(el); });

  // Table of contents: build from h2[id] inside .prose and highlight the active section
  var toc = d.querySelector('[data-toc]');
  if (toc) {
    var hs = d.querySelectorAll('.prose h2[id]');
    toc.innerHTML = Array.prototype.map.call(hs, function (h) { return '<li><a href="#' + h.id + '">' + h.textContent + '</a></li>'; }).join('');
    if ('IntersectionObserver' in window) {
      var links = toc.querySelectorAll('a');
      var tio = new IntersectionObserver(function (en) {
        en.forEach(function (e) {
          if (!e.isIntersecting) return;
          links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id); });
        });
      }, { rootMargin: '-20% 0px -70% 0px' });
      hs.forEach(function (h) { tio.observe(h); });
    }
  }

  // Generic tabs: [data-tabs] > button[data-tab=x] toggles [data-panel=x]
  d.querySelectorAll('[data-tabs]').forEach(function (tabs) {
    var scope = tabs.closest('.tool') || d;
    tabs.querySelectorAll('button[data-tab]').forEach(function (b) {
      b.setAttribute('role', 'tab');
      b.addEventListener('click', function () {
        tabs.querySelectorAll('button[data-tab]').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
        scope.querySelectorAll('[data-panel]').forEach(function (p) { p.hidden = p.dataset.panel !== b.dataset.tab; });
        var f = scope.querySelector('form'); if (f) f.dispatchEvent(new Event('change'));
      });
    });
  });
})();
