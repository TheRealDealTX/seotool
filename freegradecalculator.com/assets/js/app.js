/* FreeGradeCalculator — UI layer (no dependencies) */
(function () {
  'use strict';
  var d = document, root = d.documentElement, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || d).querySelector(s); }, $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var FGC = window.FGC = window.FGC || {};

  /* theme */
  function isDark() { return root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; }
  $$('.theme-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = isDark() ? 'light' : 'dark'; root.dataset.theme = t;
      try { localStorage.setItem('fgc-theme', t); } catch (e) {}
    });
  });

  /* toast */
  FGC.toast = function (msg) {
    var t = $('#toast'); if (!t) return; t.textContent = msg; t.classList.add('show');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('show'); }, 2200);
  };

  /* confetti (celebrate good grades) */
  FGC.confetti = function () {
    if (reduce) return;
    var c = d.createElement('canvas'); c.id = 'confetti'; d.body.appendChild(c);
    var x = c.getContext('2d'), W = c.width = innerWidth, H = c.height = innerHeight, cols = ['#7c6cff', '#22d3ee', '#f472b6', '#f59e0b', '#10b981'];
    var P = []; for (var i = 0; i < 140; i++) P.push({ x: W / 2 + (Math.random() - .5) * 200, y: H * .35, vx: (Math.random() - .5) * 14, vy: Math.random() * -14 - 4, s: Math.random() * 8 + 4, r: Math.random() * 6, vr: (Math.random() - .5) * .3, c: cols[i % 5] });
    var t0 = performance.now();
    (function f(t) {
      x.clearRect(0, 0, W, H);
      P.forEach(function (p) { p.vy += .35; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.r += p.vr; x.save(); x.translate(p.x, p.y); x.rotate(p.r); x.fillStyle = p.c; x.fillRect(-p.s / 2, -p.s / 4, p.s, p.s / 2); x.restore(); });
      if (t - t0 < 2600) requestAnimationFrame(f); else c.remove();
    })(t0);
  };

  /* header + progress + to-top + bottom nav */
  var hdr = $('.site-header'), prog = $('.scroll-progress'), top = $('.to-top'), bn = $('.bottom-nav'), lastY = 0, ticking = false;
  function onScroll() {
    var y = scrollY, h = d.body.scrollHeight - innerHeight;
    if (hdr) hdr.classList.toggle('scrolled', y > 8);
    if (prog) prog.style.setProperty('--p', h > 0 ? Math.min(1, y / h) : 0);
    if (top) top.classList.toggle('show', y > 900);
    if (bn) bn.classList.toggle('hide', y > lastY + 4 && y > 300 && !d.activeElement.matches('input,textarea,select') ? true : (y < lastY - 4 ? false : bn.classList.contains('hide')));
    lastY = y;
    $$('.parallax').forEach(function (el) { var r = el.getBoundingClientRect(); el.style.transform = 'translateY(' + ((r.top + r.height / 2 - innerHeight / 2) * -0.06).toFixed(1) + 'px)'; });
    ticking = false;
  }
  addEventListener('scroll', function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();
  if (top) top.addEventListener('click', function () { scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* reveal on scroll */
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else $$('.reveal').forEach(function (el) { el.classList.add('in'); });

  /* animated counters */
  function countUp(el) {
    var end = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length, suf = el.dataset.suffix || '', t0 = null;
    (function f(t) { t0 = t0 || t; var k = Math.min(1, (t - t0) / 1400), v = end * (1 - Math.pow(1 - k, 3)); el.textContent = v.toFixed(dec) + suf; if (k < 1) requestAnimationFrame(f); })(performance.now());
  }
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); } }); });
    $$('[data-count]').forEach(function (el) { co.observe(el); });
  }

  /* typed hero words */
  var ty = $('.typed');
  if (ty && !reduce) {
    var words = JSON.parse(ty.dataset.words), wi = 0, ci = words[0].length, del = true;
    setTimeout(function step() {
      var w = words[wi];
      if (del) { ci--; if (ci <= 0) { del = false; wi = (wi + 1) % words.length; } }
      else { ci++; if (ci >= words[wi].length) { del = true; ty.textContent = words[wi]; return setTimeout(step, 1800); } }
      ty.textContent = words[wi].slice(0, Math.max(0, ci)) || '​';
      setTimeout(step, del ? 45 : 85);
    }, 2200);
  }

  /* spotlight cards */
  $$('.tool-card').forEach(function (c) {
    c.addEventListener('pointermove', function (e) { var r = c.getBoundingClientRect(); c.style.setProperty('--mx', (e.clientX - r.left) + 'px'); c.style.setProperty('--my', (e.clientY - r.top) + 'px'); });
  });

  /* mobile menu */
  var mm = $('#mobile-menu'), mt = $('.menu-toggle');
  function closeMenu() { if (!mm) return; mm.hidden = true; mt && mt.setAttribute('aria-expanded', 'false'); d.body.style.overflow = ''; }
  if (mt && mm) {
    mt.addEventListener('click', function () { mm.hidden = false; mt.setAttribute('aria-expanded', 'true'); d.body.style.overflow = 'hidden'; });
    mm.addEventListener('click', function (e) { if (e.target === mm || e.target.closest('.menu-close')) closeMenu(); });
  }

  /* command palette search */
  var pal = $('#palette'), pq = $('#palette-q'), pr = $('#palette-results'), idx = window.FGC_INDEX || [], sel = 0;
  function norm(s) { return (s || '').toLowerCase(); }
  function renderPal() {
    var q = norm(pq.value).trim(), terms = q.split(/\s+/), res = idx.filter(function (it) { var h = norm(it.t + ' ' + it.d); return terms.every(function (t) { return h.indexOf(t) > -1; }); });
    if (!q) res = idx.slice(0, 9);
    res = res.slice(0, 12); sel = 0;
    pr.innerHTML = res.length ? res.map(function (it, i) { return '<li><a href="' + it.u + '"' + (i === 0 ? ' class="sel"' : '') + '><span class="pk">' + it.k + '</span><span style="min-width:0"><span class="pt">' + it.t + '</span><span class="pd">' + it.d + '</span></span></a></li>'; }).join('') : '<li class="empty">No matches — try “gpa”, “final” or “percent”.</li>';
  }
  function openPal() { if (!pal) return; closeMenu(); pal.hidden = false; pq.value = ''; renderPal(); setTimeout(function () { pq.focus(); }, 30); d.body.style.overflow = 'hidden'; }
  function closePal() { pal.hidden = true; d.body.style.overflow = ''; }
  if (pal) {
    $$('.search-open').forEach(function (b) { b.addEventListener('click', openPal); });
    pq.addEventListener('input', renderPal);
    pal.addEventListener('click', function (e) { if (e.target === pal) closePal(); });
    pq.addEventListener('keydown', function (e) {
      var as = $$('a', pr); if (!as.length) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); as[sel].classList.remove('sel'); sel = (sel + (e.key === 'ArrowDown' ? 1 : -1) + as.length) % as.length; as[sel].classList.add('sel'); as[sel].scrollIntoView({ block: 'nearest' }); }
      if (e.key === 'Enter') { e.preventDefault(); location.href = as[sel].getAttribute('href'); }
    });
  }
  d.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); pal && (pal.hidden ? openPal() : closePal()); }
    if (e.key === 'Escape') { if (pal && !pal.hidden) closePal(); closeMenu(); }
    if (e.key === '/' && !e.target.matches('input,textarea,select,[contenteditable]')) { e.preventDefault(); openPal(); }
  });

  /* tools index filter */
  var fb = $('.filter-bar'), ts = $('#tool-filter');
  function filterTools() {
    var cat = fb ? ($('[aria-pressed="true"]', fb) || {}).dataset : null; cat = cat ? cat.cat : 'all';
    var q = ts ? norm(ts.value) : '';
    $$('[data-tool-card]').forEach(function (c) { var ok = (cat === 'all' || c.dataset.cat === cat) && norm(c.textContent).indexOf(q) > -1; c.style.display = ok ? '' : 'none'; });
    $$('.cat-block').forEach(function (b) { b.style.display = $$('[data-tool-card]', b).some(function (c) { return c.style.display !== 'none'; }) ? '' : 'none'; });
  }
  if (fb) fb.addEventListener('click', function (e) { var b = e.target.closest('button'); if (!b) return; $$('button', fb).forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }); filterTools(); });
  if (ts) ts.addEventListener('input', filterTools);
  if (fb && location.hash) { var hb = $('[data-cat="' + location.hash.slice(1) + '"]', fb); if (hb) hb.click(); }

  /* TOC scrollspy */
  var tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {}; tocLinks.forEach(function (a) { map[a.hash.slice(1)] = a; });
    var so = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('active'); }); var a = map[e.target.id]; if (a) a.classList.add('active'); } });
    }, { rootMargin: '-15% 0px -75% 0px' });
    Object.keys(map).forEach(function (id) { var h = d.getElementById(id); if (h) so.observe(h); });
  }

  /* share / copy link */
  $$('[data-share]').forEach(function (b) {
    b.addEventListener('click', function () {
      var data = { title: d.title, url: location.href };
      if (navigator.share) navigator.share(data).catch(function () {});
      else if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { FGC.toast('Link copied!'); });
    });
  });
  $$('[data-print]').forEach(function (b) { b.addEventListener('click', function () { print(); }); });
})();
