/* Solar CCTV Camera — site interactions (no dependencies). */
(function () {
  'use strict';
  var d = document, w = window, root = d.documentElement;
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile nav */
  var toggle = d.querySelector('.nav-toggle'), nav = d.getElementById('site-nav');
  if (toggle && nav) {
    var setNav = function (open) {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open);
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      d.body.classList.toggle('nav-open', open);
    };
    toggle.addEventListener('click', function () { setNav(!nav.classList.contains('is-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('is-open')) { setNav(false); toggle.focus(); } });
    w.addEventListener('resize', function () { if (w.innerWidth > 1020 && nav.classList.contains('is-open')) setNav(false); });
    nav.querySelectorAll('.sub-toggle').forEach(function (b) {
      b.addEventListener('click', function () {
        var sub = b.nextElementSibling, open = sub.classList.toggle('is-open');
        b.setAttribute('aria-expanded', open);
      });
    });
  }

  /* Header state + charge bar (scroll progress) */
  var header = d.querySelector('.site-header'), bar = d.querySelector('.charge-bar span');
  var hero = d.querySelector('.home-hero');
  var ticking = false;
  function onScroll() {
    var y = w.scrollY || w.pageYOffset;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    var h = root.scrollHeight - w.innerHeight;
    if (bar) bar.style.setProperty('--p', h > 0 ? Math.min(1, y / h).toFixed(4) : 0);
    if (hero) heroFrame();
    if (cycle) cycleFrame();
    ticking = false;
  }
  w.addEventListener('scroll', function () { if (!ticking) { ticking = true; w.requestAnimationFrame(onScroll); } }, { passive: true });
  w.addEventListener('resize', onScroll);

  /* Reveal on scroll */
  var rev = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in w && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    rev.forEach(function (el) { io.observe(el); });
  } else rev.forEach(function (el) { el.classList.add('is-in'); });

  /* Count-up numbers */
  d.querySelectorAll('[data-count]').forEach(function (el) {
    var end = parseFloat(el.getAttribute('data-count')), dec = (el.getAttribute('data-count').split('.')[1] || '').length;
    var run = function () {
      if (reduce) { el.textContent = end.toFixed(dec); return; }
      var t0 = null;
      (function step(ts) { t0 = t0 || ts; var p = Math.min(1, (ts - t0) / 1400); el.textContent = (end * (1 - Math.pow(1 - p, 3))).toFixed(dec); if (p < 1) w.requestAnimationFrame(step); })(performance.now());
    };
    if ('IntersectionObserver' in w) {
      var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { run(); o.disconnect(); } });
      o.observe(el);
    } else run();
  });

  /* TOC highlight */
  var tocLinks = d.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in w) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var heads = Object.keys(map).map(function (id) { return d.getElementById(id); }).filter(Boolean);
    var tio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('is-current'); });
          map[e.target.id].classList.add('is-current');
        }
      });
    }, { rootMargin: '-80px 0px -70% 0px' });
    heads.forEach(function (h) { tio.observe(h); });
  }

  /* Range input fill */
  function fill(r) { var p = (r.value - r.min) / (r.max - r.min) * 100; r.style.setProperty('--fill', p + '%'); }
  d.addEventListener('input', function (e) { if (e.target.type === 'range') fill(e.target); });
  d.querySelectorAll('input[type=range]').forEach(fill);
  w.scFill = fill;

  /* ---------- Home hero: one solar day per scroll ---------- */
  var orb, rig, hud, clockEl, stateEl, battEl;
  if (hero) {
    orb = hero.querySelector('.orb'); rig = hero.querySelector('.rig'); hud = hero.querySelector('.battery-hud');
    clockEl = hero.querySelector('[data-clock]'); stateEl = hero.querySelector('[data-state]'); battEl = hero.querySelector('[data-batt]');
  }
  function heroFrame() {
    var r = hero.getBoundingClientRect(), span = hero.offsetHeight - w.innerHeight;
    var t = reduce ? 0.35 : Math.max(0, Math.min(1, -r.top / (span || 1)));
    hero.style.setProperty('--t', t.toFixed(4));
    // Sun: travels a parabolic arc from left horizon to right horizon over t 0..0.72
    var s = Math.min(1, t / 0.72), vw = w.innerWidth, vh = w.innerHeight;
    var x = 0.02 * vw + s * 0.88 * vw, y = vh * 0.84 - Math.sin(s * Math.PI) * vh * 0.72;
    if (orb) { orb.style.setProperty('--sx', x + 'px'); orb.style.setProperty('--sy', y + 'px'); }
    var charge = Math.max(0, Math.sin(s * Math.PI)) * (t < 0.72 ? 1 : 0);
    if (rig) rig.style.setProperty('--charge', charge.toFixed(3));
    // Simulated battery: charges through the day, drains slowly at night
    var batt = t < 0.72 ? 58 + 40 * (1 - Math.cos(s * Math.PI)) / 2 : 98 - (t - 0.72) / 0.28 * 14;
    if (hud) hud.style.setProperty('--batt', batt.toFixed(1));
    if (battEl) battEl.textContent = Math.round(batt) + '%';
    var hour = 6 + t * 18, hh = Math.floor(hour) % 24, mm = Math.floor((hour % 1) * 60);
    if (clockEl) clockEl.textContent = (hh % 12 || 12) + ':' + (mm < 10 ? '0' : '') + mm + (hh < 12 ? ' AM' : ' PM');
    if (stateEl) stateEl.textContent = t < 0.72 ? (charge > 0.15 ? 'Charging from sun' : 'Low sun, trickle charge') : 'Night: IR on, on battery';
  }

  /* ---------- Home: 24h battery chart drawn on scroll ---------- */
  var cycle = d.querySelector('.cycle-chart');
  var battPath = cycle && cycle.querySelector('.batt');
  if (battPath && battPath.getTotalLength) cycle.style.setProperty('--len', Math.ceil(battPath.getTotalLength()));
  function cycleFrame() {
    var r = cycle.getBoundingClientRect(), vh = w.innerHeight;
    var p = reduce ? 1 : Math.max(0, Math.min(1, (vh - r.top) / (vh * 0.9)));
    cycle.style.setProperty('--draw', p.toFixed(3));
  }

  onScroll();
})();
