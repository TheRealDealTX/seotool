// Yasmin's Blog: header, nav, theme, scroll reveal, tilt, filters.
(function () {
  var d = document, root = d.documentElement, body = d.body;
  root.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;

  // Header state + reading progress, in one rAF-throttled scroll handler.
  var header = d.querySelector('.site-header'), lastY = 0, ticking = false;
  function onScroll() {
    var y = window.scrollY, h = root.scrollHeight - innerHeight;
    header.classList.toggle('scrolled', y > 10);
    header.classList.toggle('hide', y > 300 && y > lastY && !body.classList.contains('nav-open'));
    root.style.setProperty('--p', h > 0 ? (y / h).toFixed(4) : 0);
    lastY = y; ticking = false;
  }
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // Mobile nav
  var toggle = d.querySelector('.nav-toggle');
  toggle.addEventListener('click', function () {
    var open = body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  // Theme toggle
  d.querySelector('.theme-toggle').addEventListener('click', function () {
    var cur = root.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var next = cur === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('yb-theme', next); } catch (e) {}
  });

  // Scroll reveal
  var els = d.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('in'); });
  }

  if (fine && !reduce) {
    // 3D tilt on cover art
    d.querySelectorAll('.tilt').forEach(function (el) {
      var host = el.closest('.card, .feature, .plate') || el;
      host.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(900px) rotateY(' + (x * 8) + 'deg) rotateX(' + (-y * 8) + 'deg)';
      });
      host.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
    // Spotlight that follows the cursor across the hero
    var hero = d.querySelector('.hero');
    if (hero) hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      hero.style.setProperty('--mx', (e.clientX - r.left) + 'px');
      hero.style.setProperty('--my', (e.clientY - r.top) + 'px');
    });
  }

  // Journal filters + search
  var grid = d.querySelector('.filterable');
  if (grid) {
    var cards = grid.querySelectorAll('.card'), cat = 'all', q = '';
    var empty = d.querySelector('.empty'), input = d.querySelector('[data-search-input]');
    function apply() {
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.dataset.cat === cat) && (!q || c.dataset.search.indexOf(q) > -1);
        c.classList.toggle('gone', !ok);
        if (ok) { shown++; c.classList.add('in'); }
      });
      empty.hidden = shown > 0;
    }
    d.querySelectorAll('.filter').forEach(function (b) {
      b.addEventListener('click', function () {
        d.querySelectorAll('.filter').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on'); cat = b.dataset.filter; apply();
      });
    });
    input.addEventListener('input', function () { q = input.value.trim().toLowerCase(); apply(); });
  }
})();
