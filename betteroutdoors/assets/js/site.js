/* Better Outdoors - site interactions and visual effects. No dependencies. */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---- Header, progress arrow, back-to-top, parallax ---- */
  var header = $('.site-header'), prog = $('.progress'), shaft = $('.progress-shaft'), tip = $('.progress-tip');
  var toTop = $('.to-top'), heroBg = $('.hero-bg'), ridges = $$('.ridges svg');
  var ticking = false;
  function onScroll() {
    var y = window.scrollY, h = doc.scrollHeight - window.innerHeight;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (toTop) toTop.classList.toggle('show', y > 700);
    if (shaft) {
      var pct = h > 0 ? Math.min(100, (y / h) * 100) : 0;
      shaft.style.width = pct + '%';
      tip.style.left = pct + '%';
      prog.classList.toggle('on', pct > 1);
    }
    if (!reduce && y < window.innerHeight * 1.2) {
      if (heroBg) heroBg.style.translate = '0 ' + (y * 0.3) + 'px';
      ridges.forEach(function (r, i) { r.style.transform = 'translateY(' + (y * (0.06 + i * 0.07)) + 'px)'; });
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  /* ---- Mobile nav ---- */
  var toggle = $('#nav-toggle'), nav = $('#main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
      toggle.innerHTML = open ? '<i class="fa-solid fa-xmark" aria-hidden="true"></i>' : '<i class="fa-solid fa-bars" aria-hidden="true"></i>';
    });
  }

  /* ---- Search overlay ---- */
  var so = $('#search-overlay'), si = $('#search-input'), sr = $('#search-results');
  function renderSearch(q) {
    q = (q || '').trim().toLowerCase();
    var items = (window.BO_INDEX || []).filter(function (it) {
      return !q || q.split(/\s+/).every(function (w) { return (it.t + ' ' + it.k).toLowerCase().indexOf(w) > -1; });
    });
    sr.innerHTML = items.length ? items.map(function (it) {
      return '<li><a href="' + it.u + '">' + it.t.replace(/</g, '&lt;') + '<small>' + it.u + '</small></a></li>';
    }).join('') : '<li class="no-results">No matches. Try "draw length" or "Mathews".</li>';
  }
  function openSearch() { so.hidden = false; renderSearch(''); setTimeout(function () { si.focus(); }, 30); }
  function closeSearch() { so.hidden = true; }
  if (so) {
    $('#search-open').addEventListener('click', openSearch);
    $('#search-close').addEventListener('click', closeSearch);
    so.addEventListener('click', function (e) { if (e.target === so) closeSearch(); });
    si.addEventListener('input', function () { renderSearch(si.value); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !so.hidden) closeSearch();
      if (e.key === '/' && so.hidden && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
    });
  }

  /* ---- Reveal on scroll + counters ---- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        $$('[data-count]', en.target).concat(en.target.hasAttribute('data-count') ? [en.target] : []).forEach(countUp);
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('in'); });
  }
  function countUp(el) {
    if (el.dataset.done) return;
    el.dataset.done = 1;
    var end = parseFloat(el.dataset.count), suf = el.dataset.suffix || '', dur = 1400, t0 = null;
    if (reduce) { el.textContent = end + suf; return; }
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / dur), v = end * (1 - Math.pow(1 - k, 3));
      el.textContent = (end % 1 ? v.toFixed(1) : Math.round(v).toLocaleString('en-US')) + suf;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---- TOC active state ---- */
  var tocLinks = $$('.post-side .toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove('active'); });
          map[en.target.id].classList.add('active');
        }
      });
    }, { rootMargin: '-90px 0px -70% 0px' });
    $$('.prose h2[id]').forEach(function (h) { tio.observe(h); });
  }

  /* ---- Copy link ---- */
  $$('.copy-link').forEach(function (b) {
    b.addEventListener('click', function () {
      if (navigator.clipboard) navigator.clipboard.writeText(b.dataset.url);
      b.innerHTML = '<i class="fa-solid fa-check" aria-hidden="true"></i>';
      setTimeout(function () { b.innerHTML = '<i class="fa-solid fa-link" aria-hidden="true"></i>'; }, 1600);
    });
  });

  /* ---- Range input fill ---- */
  function fillRange(r) { r.style.setProperty('--p', ((r.value - r.min) / (r.max - r.min) * 100) + '%'); }
  $$('input[type=range]').forEach(function (r) { fillRange(r); r.addEventListener('input', function () { fillRange(r); }); });
  window.BO_fillRange = fillRange;

  /* ---- Hero: fireflies / drifting light particles ---- */
  function particles(canvas, opts) {
    if (!canvas || reduce) return;
    var ctx = canvas.getContext('2d'), w, h, dpr = Math.min(window.devicePixelRatio || 1, 2), ps = [];
    function size() {
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    size(); window.addEventListener('resize', size);
    var n = Math.round(Math.min(opts.max, (w * h) / opts.density));
    for (var i = 0; i < n; i++) ps.push(opts.make(w, h, true));
    var visible = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { visible = e[0].isIntersecting; }).observe(canvas);
    function frame(t) {
      if (visible) {
        ctx.clearRect(0, 0, w, h);
        ps.forEach(function (p, i) { if (opts.draw(ctx, p, t, w, h)) ps[i] = opts.make(w, h, false); });
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }
  particles($('.hero-canvas'), {
    max: 70, density: 16000,
    make: function (w, h, init) {
      return { x: Math.random() * w, y: init ? Math.random() * h : h + 10, r: Math.random() * 2.2 + .6, vy: -(Math.random() * .35 + .1), vx: (Math.random() - .5) * .3, ph: Math.random() * 6.28, hue: Math.random() < .3 ? '255,140,90' : '220,240,235' };
    },
    draw: function (ctx, p, t, w, h) {
      p.x += p.vx + Math.sin(t / 1400 + p.ph) * .25; p.y += p.vy;
      var a = .35 + Math.sin(t / 600 + p.ph) * .3;
      var g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 5);
      g.addColorStop(0, 'rgba(' + p.hue + ',' + Math.max(a, 0) + ')'); g.addColorStop(1, 'rgba(' + p.hue + ',0)');
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, p.r * 5, 0, 6.283); ctx.fill();
      return p.y < -20 || p.x < -20 || p.x > w + 20;
    }
  });

  /* ---- CTA band: falling autumn leaves ---- */
  $$('.cta-canvas').forEach(function (c) {
    var colors = ['#FF6930', '#f59e0b', '#5F9598', '#c2410c', '#fcd34d'];
    particles(c, {
      max: 26, density: 30000,
      make: function (w, h, init) {
        return { x: Math.random() * w, y: init ? Math.random() * h : -20, s: Math.random() * 8 + 6, vy: Math.random() * .6 + .35, rot: Math.random() * 6.28, vr: (Math.random() - .5) * .03, ph: Math.random() * 6.28, c: colors[Math.floor(Math.random() * colors.length)] };
      },
      draw: function (ctx, p, t, w, h) {
        p.y += p.vy; p.x += Math.sin(t / 900 + p.ph) * .7; p.rot += p.vr;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.globalAlpha = .55; ctx.fillStyle = p.c;
        ctx.beginPath(); ctx.moveTo(0, -p.s); ctx.quadraticCurveTo(p.s * .8, 0, 0, p.s); ctx.quadraticCurveTo(-p.s * .8, 0, 0, -p.s); ctx.fill();
        ctx.strokeStyle = 'rgba(0,0,0,.18)'; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(0, -p.s); ctx.lineTo(0, p.s); ctx.stroke();
        ctx.restore();
        return p.y > h + 20;
      }
    });
  });

  /* ---- Hero target: shoot an arrow ---- */
  var stage = $('.target-stage');
  if (stage) {
    var arrow = $('.arrow', stage), btn = $('.shoot-btn', stage), counter = $('.hit-count b', stage), hits = 0;
    function shoot() {
      var ang = Math.random() * 6.283, rad = Math.random() * 13;
      arrow.style.left = (50 + Math.cos(ang) * rad) + '%';
      arrow.style.top = (50 + Math.sin(ang) * rad) + '%';
      arrow.classList.remove('arrow-fly', 'arrow-quiver'); stage.classList.remove('hit');
      void arrow.offsetWidth;
      arrow.classList.add('arrow-fly');
      setTimeout(function () {
        arrow.classList.remove('arrow-fly'); arrow.classList.add('arrow-quiver'); stage.classList.add('hit');
        hits++; if (counter) counter.textContent = hits;
      }, reduce ? 0 : 700);
    }
    if (btn) btn.addEventListener('click', shoot);
    setTimeout(shoot, 900);
  }

  /* ---- Post filters (blog / category) ---- */
  var grid = $('[data-filter-grid]');
  if (grid) {
    var cards = $$('.post-card', grid), chips = $$('.chips button'), fin = $('#filter-q'), empty = $('.no-results', grid.parentNode), cat = 'all';
    var params = new URLSearchParams(location.search);
    if (fin && params.get('q')) fin.value = params.get('q');
    function apply() {
      var q = fin ? fin.value.trim().toLowerCase() : '', shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.dataset.cat === cat) && (!q || q.split(/\s+/).every(function (w) { return c.dataset.text.indexOf(w) > -1; }));
        c.hidden = !ok; if (ok) { shown++; c.classList.add('in'); }
      });
      if (empty) empty.hidden = shown > 0;
    }
    chips.forEach(function (b) {
      b.addEventListener('click', function () { chips.forEach(function (x) { x.classList.remove('on'); }); b.classList.add('on'); cat = b.dataset.cat; apply(); });
    });
    if (fin) fin.addEventListener('input', apply);
    apply();
  }

  /* ---- Home mini draw-length widget ---- */
  var mini = $('#mini-wingspan');
  if (mini) {
    var out = $('#mini-out'), lab = $('#mini-in'), bowString = $('#bow-string'), bowArrow = $('#bow-arrow');
    function upd() {
      var ws = parseFloat(mini.value), dl = Math.round(ws / 2.5 * 2) / 2;
      out.textContent = dl.toFixed(1); lab.textContent = ws + '"';
      var pull = 30 + (dl - 24) * 9;
      if (bowString) bowString.setAttribute('d', 'M60 10 L' + (60 - pull) + ' 60 L60 110');
      if (bowArrow) bowArrow.setAttribute('transform', 'translate(' + (-pull) + ',0)');
      fillRange(mini);
    }
    mini.addEventListener('input', upd); upd();
  }
})();
