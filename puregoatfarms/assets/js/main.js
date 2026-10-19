/* Pure Goat Farms — site interactions and visual effects. No dependencies. */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Header shrink, progress bar, back-to-top.
  var header = $('.site-header');
  var progress = $('.read-progress span');
  var toTop = $('.to-top');
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 20);
    if (toTop) toTop.classList.toggle('is-visible', y > 700);
    if (progress) {
      var h = document.body.scrollHeight - window.innerHeight;
      progress.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    }
    parallax();
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  // Mobile nav + dropdown toggles.
  var toggle = $('.nav-toggle');
  if (toggle) toggle.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  $$('.sub-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
      var li = b.parentNode;
      var open = li.classList.toggle('is-open');
      b.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.body.classList.remove('nav-open');
      $$('.has-sub.is-open').forEach(function (li) { li.classList.remove('is-open'); });
    }
  });

  // Scroll reveal with a small stagger for siblings.
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        var sibs = $$('.reveal', el.parentNode).filter(function (s) { return s.parentNode === el.parentNode; });
        el.style.setProperty('--d', Math.min(sibs.indexOf(el), 6) * 0.08 + 's');
        el.classList.add('is-in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Animated counters.
  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    if (reduce || !isFinite(end)) { el.textContent = end + suffix; return; }
    var start = null;
    function step(t) {
      if (!start) start = t;
      var p = Math.min(1, (t - start) / 1400);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = '0' + suffix;
    requestAnimationFrame(step);
  }
  var counters = $$('[data-count]');
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { countUp(en.target); co.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  }

  // Bar charts inside articles grow when visible.
  $$('.bar-chart').forEach(function (bc) {
    if (!('IntersectionObserver' in window)) { bc.classList.add('is-in'); return; }
    var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { bc.classList.add('is-in'); o.disconnect(); } }, { threshold: 0.3 });
    o.observe(bc);
  });

  // Gentle parallax on hero media.
  var para = $$('[data-parallax]');
  function parallax() {
    if (reduce || window.innerWidth < 900) return;
    para.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var off = (r.top + r.height / 2 - window.innerHeight / 2) * parseFloat(el.getAttribute('data-parallax'));
      el.style.transform = 'translate3d(0,' + (-off).toFixed(1) + 'px,0)';
    });
  }

  // 3D tilt + spotlight on cards (pointer devices only).
  if (!reduce && window.matchMedia('(hover: hover)').matches) {
    $$('.tilt').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        el.style.transform = 'perspective(900px) rotateX(' + ((0.5 - y) * 7).toFixed(2) + 'deg) rotateY(' + ((x - 0.5) * 9).toFixed(2) + 'deg) translateY(-4px)';
        el.style.setProperty('--mx', (x * 100) + '%');
        el.style.setProperty('--my', (y * 100) + '%');
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
    $$('.magnetic').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        el.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.25).toFixed(1) + 'px)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  // Table of contents: highlight the section in view.
  var tocLinks = $$('.post-toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var to = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove('is-active'); });
          map[en.target.id].classList.add('is-active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) to.observe(h); });
  }

  // Copy link.
  $$('.copy-link').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = b.getAttribute('data-url');
      (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () {
        toast('Link copied to clipboard');
      }, function () { window.prompt('Copy this link:', url); });
    });
  });

  // Blog filter + search.
  var grid = $('[data-filterable]');
  if (grid) {
    var items = $$('.post-grid__item', grid);
    var search = $('[data-search]');
    var empty = $('.empty-state');
    var cat = 'all';
    function apply() {
      var q = search ? search.value.trim().toLowerCase() : '';
      var shown = 0;
      items.forEach(function (it) {
        var ok = (cat === 'all' || it.getAttribute('data-cats').split(' ').indexOf(cat) > -1) &&
          (!q || it.getAttribute('data-text').indexOf(q) > -1);
        it.hidden = !ok;
        if (ok) { shown++; var c = $('.reveal', it); if (c) c.classList.add('is-in'); }
      });
      if (empty) empty.hidden = shown > 0;
    }
    $$('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        $$('[data-filter]').forEach(function (x) { x.classList.remove('is-on'); });
        b.classList.add('is-on');
        cat = b.getAttribute('data-filter');
        apply();
      });
    });
    if (search) search.addEventListener('input', apply);
  }

  // FAQ search.
  var fs = $('[data-faq-search]');
  if (fs) fs.addEventListener('input', function () {
    var q = fs.value.trim().toLowerCase(), any = false;
    $$('[data-faq-group]').forEach(function (g) {
      var vis = 0;
      $$('.faq__item', g).forEach(function (d) {
        var ok = !q || d.textContent.toLowerCase().indexOf(q) > -1;
        d.hidden = !ok;
        if (ok) { vis++; if (q) d.open = true; }
      });
      g.hidden = vis === 0;
      any = any || vis > 0;
    });
    var em = $('.empty-state'); if (em) em.hidden = any;
  });

  // Start-here checklist, remembered per browser.
  $$('[data-checklist]').forEach(function (box) {
    var boxes = $$('input[type=checkbox]', box);
    var done = $('[data-done]', box);
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem('pgf-checklist') || '[]'); } catch (e) {}
    boxes.forEach(function (b, i) { b.checked = saved.indexOf(i) > -1; });
    function upd() {
      var on = [];
      boxes.forEach(function (b, i) { if (b.checked) on.push(i); });
      done.textContent = on.length;
      try { localStorage.setItem('pgf-checklist', JSON.stringify(on)); } catch (e) {}
    }
    box.addEventListener('change', upd);
    upd();
  });

  // Range slider fill.
  $$('input[type=range]').forEach(function (r) {
    function fill() { r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%'); }
    r.addEventListener('input', fill); fill();
  });

  // Toasts (newsletter result).
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'toast'; t.setAttribute('role', 'status'); t.textContent = msg;
    document.body.appendChild(t);
    requestAnimationFrame(function () { t.classList.add('is-on'); });
    setTimeout(function () { t.classList.remove('is-on'); setTimeout(function () { t.remove(); }, 500); }, 4200);
  }
  var sub = /[?&]subscribed=([01])/.exec(location.search);
  if (sub) {
    toast(sub[1] === '1' ? 'Thanks for subscribing — your first field note is on the way.' : 'Please enter a valid email address to subscribe.');
    if (history.replaceState) history.replaceState(null, '', location.pathname + location.hash);
  }

  onScroll();
})();
