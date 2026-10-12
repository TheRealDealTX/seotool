/* Come i Cavoli a Merenda — site script */
(function () {
  var doc = document.documentElement, body = document.body;
  doc.classList.remove('no-js');

  /* ---------- Mobile nav ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('main-nav');
  function setNav(open) {
    body.classList.toggle('nav-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (open) { var first = nav.querySelector('a'); if (first) first.focus({ preventScroll: true }); }
  }
  if (toggle && nav) {
    toggle.addEventListener('click', function () { setNav(!body.classList.contains('nav-open')); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('nav-open')) { setNav(false); toggle.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 980 && body.classList.contains('nav-open')) setNav(false); });
  }

  /* ---------- Header shadow + reading progress ---------- */
  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.progress');
  function onScroll() {
    var y = window.scrollY || doc.scrollTop;
    if (header) header.classList.toggle('scrolled', y > 8);
    if (bar) {
      var h = doc.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- Reveal on scroll + meters ---------- */
  var revealEls = document.querySelectorAll('.reveal, .meter');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add('in');
        var i = el.querySelector && el.querySelector('.bar i');
        if (i) i.style.width = i.getAttribute('data-w') + '%';
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add('in');
      var i = el.querySelector('.bar i'); if (i) i.style.width = i.getAttribute('data-w') + '%';
    });
  }

  /* ---------- Sparkles in hero ---------- */
  document.querySelectorAll('.sparkles').forEach(function (box) {
    var n = parseInt(box.getAttribute('data-n') || '18', 10);
    for (var k = 0; k < n; k++) {
      var s = document.createElement('i');
      s.style.left = (Math.random() * 100) + '%';
      s.style.top = (Math.random() * 100) + '%';
      s.style.animationDelay = (Math.random() * 4) + 's';
      s.style.animationDuration = (3 + Math.random() * 4) + 's';
      var sz = 3 + Math.random() * 4; s.style.width = s.style.height = sz + 'px';
      box.appendChild(s);
    }
  });

  /* ---------- Table of contents active state ---------- */
  var tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove('active'); });
          var a = map[en.target.id]; if (a) a.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* ---------- Wrap tables for horizontal scroll on mobile ---------- */
  document.querySelectorAll('.prose table').forEach(function (t) {
    if (t.parentElement.classList.contains('tbl-wrap')) return;
    var w = document.createElement('div'); w.className = 'tbl-wrap';
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });

  /* ---------- Earring size viewer ---------- */
  var KEY = 'cavoli-px-per-mm';
  function storedScale() {
    try { var v = parseFloat(localStorage.getItem(KEY)); return v > 1 && v < 30 ? v : null; } catch (e) { return null; }
  }
  function saveScale(v) { try { localStorage.setItem(KEY, String(v)); } catch (e) {} }
  // Fallback: CSS px are defined as 96/in, i.e. ~3.78 px per mm (close on most desktops, approximate on phones)
  var pxPerMm = storedScale() || 3.7795;

  document.querySelectorAll('[data-sizer]').forEach(function (root) {
    var range = root.querySelector('input[type=range]');
    var gem = root.querySelector('.gem');
    var mmOut = root.querySelector('[data-mm]');
    var inOut = root.querySelector('[data-in]');
    var cmpOut = root.querySelector('[data-cmp]');
    var coin = root.querySelector('.coin');
    var chips = root.querySelectorAll('.chip[data-v]');
    var COMPARE = [
      [2.5, 'about a grain of rice is wide'], [3, 'a tiny, barely-there sparkle'], [4, 'a peppercorn'],
      [5, 'a pencil eraser, a little smaller'], [6, 'a pencil eraser'], [7, 'a pea'], [8, 'a chickpea'],
      [9, 'half a dime'], [10, 'a fingernail on your pinky'], [12, 'a blueberry'], [14, 'a big statement stud'],
      [20, 'about a US penny (19 mm)']
    ];
    function cmp(v) { var best = COMPARE[0]; COMPARE.forEach(function (c) { if (v >= c[0]) best = c; }); return best[1]; }
    function render() {
      var v = parseFloat(range.value);
      var px = v * pxPerMm;
      gem.style.width = gem.style.height = px + 'px';
      if (coin) { var c = 19.05 * pxPerMm; coin.style.width = coin.style.height = c + 'px'; }
      if (mmOut) mmOut.textContent = v + ' mm';
      if (inOut) inOut.textContent = (v / 25.4).toFixed(3) + ' in';
      if (cmpOut) cmpOut.textContent = 'Roughly ' + cmp(v);
      chips.forEach(function (ch) { ch.classList.toggle('on', parseFloat(ch.getAttribute('data-v')) === v); });
    }
    range.addEventListener('input', render);
    chips.forEach(function (ch) { ch.addEventListener('click', function () { range.value = ch.getAttribute('data-v'); render(); }); });

    var cal = root.querySelector('[data-calibrate]');
    if (cal) {
      var outline = cal.querySelector('.card-outline');
      var cr = cal.querySelector('input[type=range]');
      var reset = cal.querySelector('[data-reset]');
      function drawCard() { outline.style.setProperty('--cw', (85.6 * pxPerMm) + 'px'); }
      cr.value = Math.round(85.6 * pxPerMm);
      drawCard();
      cr.addEventListener('input', function () { pxPerMm = parseFloat(cr.value) / 85.6; saveScale(pxPerMm); drawCard(); render(); });
      if (reset) reset.addEventListener('click', function () {
        pxPerMm = 3.7795; try { localStorage.removeItem(KEY); } catch (e) {}
        cr.value = Math.round(85.6 * pxPerMm); drawCard(); render();
      });
    }
    render();
  });

  /* ---------- Gauge converter ---------- */
  var GAUGES = [['20g', 0.8], ['18g', 1.0], ['16g', 1.2], ['14g', 1.6], ['12g', 2.0], ['10g', 2.5], ['8g', 3.0], ['6g', 4.0], ['4g', 5.0], ['2g', 6.0], ['0g', 8.0], ['00g', 10.0], ['7/16"', 11.0], ['1/2"', 12.7], ['9/16"', 14.0], ['5/8"', 16.0], ['3/4"', 19.0], ['7/8"', 22.0], ['1"', 25.4]];
  document.querySelectorAll('[data-gauge]').forEach(function (root) {
    var sel = root.querySelector('select');
    var dot = root.querySelector('.gem');
    var out = root.querySelector('[data-gout]');
    GAUGES.forEach(function (g, i) {
      var o = document.createElement('option'); o.value = i; o.textContent = g[0] + ' — ' + g[1] + ' mm';
      if (g[0] === '18g') o.selected = true; sel.appendChild(o);
    });
    function render() {
      var g = GAUGES[parseInt(sel.value, 10)];
      var px = Math.max(2, g[1] * pxPerMm * 3);
      dot.style.width = dot.style.height = px + 'px';
      var note = g[1] <= 1.0 ? 'Standard size for most lobe earrings.' : g[1] <= 1.6 ? 'Typical for cartilage and body jewelry.' : g[1] < 5 ? 'Early stretching range.' : 'Stretched lobe territory: plugs and tunnels.';
      out.innerHTML = '<b>' + g[0] + '</b> = ' + g[1] + ' mm (' + (g[1] / 25.4).toFixed(3) + ' in). ' + note;
    }
    sel.addEventListener('change', render);
    render();
  });

  var y = document.querySelector('[data-year]'); if (y) y.textContent = new Date().getFullYear();
})();
