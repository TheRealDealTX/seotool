/* Connected Renter — site behaviour: header, nav, reveal effects, search, tabs, forms. */
(function () {
  'use strict';
  var d = document, w = window, root = d.documentElement;
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  /* header state, progress bar, back-to-top */
  var header = $('.site-header'), prog = $('.progress'), top = $('.to-top');
  function onScroll() {
    var y = w.scrollY || 0, h = root.scrollHeight - w.innerHeight;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (prog) prog.style.setProperty('--p', h > 0 ? Math.min(1, y / h) : 0);
    if (top) top.classList.toggle('show', y > 700);
  }
  w.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (top) top.addEventListener('click', function () { w.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* mobile nav */
  var menuBtn = $('.menu-btn');
  if (menuBtn) menuBtn.addEventListener('click', function () {
    var open = d.body.classList.toggle('nav-open');
    menuBtn.setAttribute('aria-expanded', open);
  });

  /* dropdown menus */
  var desktop = w.matchMedia('(min-width: 1081px)');
  $$('.has-menu').forEach(function (li) {
    var btn = $('button', li), t;
    function set(open) { li.classList.toggle('open', open); btn.setAttribute('aria-expanded', open); }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = !li.classList.contains('open');
      $$('.has-menu.open').forEach(function (o) { if (o !== li) { o.classList.remove('open'); $('button', o).setAttribute('aria-expanded', 'false'); } });
      set(willOpen);
    });
    li.addEventListener('mouseenter', function () { if (desktop.matches) { clearTimeout(t); set(true); } });
    li.addEventListener('mouseleave', function () { if (desktop.matches) t = setTimeout(function () { set(false); }, 160); });
  });
  d.addEventListener('click', function (e) {
    if (!e.target.closest('.has-menu')) $$('.has-menu.open').forEach(function (o) { o.classList.remove('open'); $('button', o).setAttribute('aria-expanded', 'false'); });
  });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') $$('.has-menu.open').forEach(function (o) { o.classList.remove('open'); $('button', o).setAttribute('aria-expanded', 'false'); $('button', o).focus(); });
  });

  /* scroll reveal */
  var rev = $$('.reveal');
  if ('IntersectionObserver' in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    rev.forEach(function (el) { io.observe(el); });
  } else rev.forEach(function (el) { el.classList.add('in'); });

  /* animated counters */
  function count(el) {
    var end = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '', pre = el.getAttribute('data-prefix') || '';
    if (reduce) { el.textContent = pre + end.toLocaleString() + suf; return; }
    var t0 = null, dur = 1600;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + Math.round(end * e).toLocaleString() + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var cs = $$('[data-count]');
  if ('IntersectionObserver' in w) {
    var co = new IntersectionObserver(function (en) { en.forEach(function (x) { if (x.isIntersecting) { count(x.target); co.unobserve(x.target); } }); }, { threshold: 0.4 });
    cs.forEach(function (el) { co.observe(el); });
  } else cs.forEach(count);

  /* card spotlight follows the pointer */
  d.addEventListener('pointermove', function (e) {
    var c = e.target.closest && e.target.closest('.card');
    if (!c) return;
    var r = c.getBoundingClientRect();
    c.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    c.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });

  /* subtle parallax on hero visual */
  var hv = $('.hero-visual');
  if (hv && !reduce) {
    $('.hero').addEventListener('pointermove', function (e) {
      var x = (e.clientX / w.innerWidth - 0.5) * 14, y = (e.clientY / w.innerHeight - 0.5) * 14;
      hv.style.transform = 'translate(' + x + 'px,' + y + 'px)';
    });
  }

  /* journey tabs */
  $$('[role="tablist"]').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    function sel(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
        var p = d.getElementById(t.getAttribute('aria-controls')); if (p) p.hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { sel(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key, n = null;
        if (k === 'ArrowDown' || k === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (k === 'ArrowUp' || k === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (n) { e.preventDefault(); sel(n); n.focus(); }
      });
    });
  });

  /* search (hero finder + Ctrl/Cmd-K palette) */
  var INDEX = w.CR_INDEX || [];
  function search(q, limit) {
    q = q.trim().toLowerCase();
    if (!q) return [];
    var words = q.split(/\s+/);
    return INDEX.map(function (it) {
      var hay = (it.t + ' ' + it.d + ' ' + (it.k || '')).toLowerCase(), s = 0;
      words.forEach(function (wd) { if (it.t.toLowerCase().indexOf(wd) > -1) s += 3; if (hay.indexOf(wd) > -1) s += 1; else s -= 2; });
      return { it: it, s: s };
    }).filter(function (x) { return x.s > 0; }).sort(function (a, b) { return b.s - a.s; }).slice(0, limit || 8).map(function (x) { return x.it; });
  }
  function itemHTML(it, kind) {
    return '<a href="' + it.u + '"><svg class="icon" aria-hidden="true"><use href="#i-' + (it.i || 'arrow') + '"/></svg><span><strong>' + esc(it.t) + '</strong><small>' + esc(it.d) + '</small></span>' + (kind ? '<span class="kind">' + esc(it.kind) + '</span>' : '') + '</a>';
  }
  function bindList(input, box, kind, onEmpty) {
    var act = -1;
    function render() {
      var res = search(input.value, 7); act = -1;
      if (!input.value.trim()) { box.innerHTML = onEmpty ? onEmpty() : ''; box.classList.toggle('show', !!onEmpty); return; }
      box.innerHTML = res.length ? res.map(function (r) { return itemHTML(r, kind); }).join('') : '<div class="palette-empty">No matches — try “movers”, “credit” or “insurance”.</div>';
      box.classList.add('show');
    }
    input.addEventListener('input', render);
    input.addEventListener('focus', render);
    input.addEventListener('keydown', function (e) {
      var links = $$('a', box);
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault(); if (!links.length) return;
        act = (act + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
        links.forEach(function (l, i) { l.classList.toggle('active', i === act); });
        links[act].scrollIntoView({ block: 'nearest' });
      } else if (e.key === 'Enter') {
        var target = links[act] || links[0]; if (target) { e.preventDefault(); w.location.href = target.getAttribute('href'); }
      }
    });
    return render;
  }
  var finder = $('.finder input'), fres = $('.finder-results');
  if (finder && fres) {
    bindList(finder, fres, false);
    d.addEventListener('click', function (e) { if (!e.target.closest('.finder')) fres.classList.remove('show'); });
  }
  var pal = $('.palette');
  if (pal) {
    var pin = $('input', pal), plist = $('.palette-list', pal);
    var renderPal = bindList(pin, plist, true, function () {
      return INDEX.filter(function (x) { return x.f; }).map(function (r) { return itemHTML(r, true); }).join('');
    });
    function openPal() { pal.classList.add('open'); pin.value = ''; renderPal(); setTimeout(function () { pin.focus(); }, 30); }
    function closePal() { pal.classList.remove('open'); }
    $$('[data-open-search]').forEach(function (b) { b.addEventListener('click', openPal); });
    pal.addEventListener('click', function (e) { if (e.target === pal) closePal(); });
    d.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); pal.classList.contains('open') ? closePal() : openPal(); }
      else if (e.key === '/' && !/input|textarea|select/i.test(d.activeElement.tagName)) { e.preventDefault(); openPal(); }
      else if (e.key === 'Escape') closePal();
    });
  }

  /* table of contents highlight */
  var toc = $$('.toc a');
  if (toc.length && 'IntersectionObserver' in w) {
    var map = {};
    toc.forEach(function (a) { var id = a.getAttribute('href').slice(1), h = d.getElementById(id); if (h) map[id] = a; });
    var to = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { toc.forEach(function (a) { a.classList.remove('active'); }); var a = map[x.target.id]; if (a) a.classList.add('active'); } });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { to.observe(d.getElementById(id)); });
  }

  /* blog category filter */
  var fl = $('.filters');
  if (fl) {
    var btns = $$('button', fl), posts = $$('[data-cat]');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var c = b.getAttribute('data-filter');
        btns.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        posts.forEach(function (p) { p.hidden = c !== 'all' && p.getAttribute('data-cat') !== c; });
      });
    });
  }

  /* range inputs: paint the filled track */
  function paint(r) { var p = (r.value - r.min) / (r.max - r.min) * 100; r.style.setProperty('--fill', p + '%'); }
  $$('input[type=range]').forEach(function (r) { paint(r); r.addEventListener('input', function () { paint(r); }); });
  w.CRpaint = paint;

  /* contact + newsletter forms open the visitor's mail app (no server-side mail) */
  $$('form[data-mailto]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!f.checkValidity()) { f.reportValidity(); return; }
      var to = f.getAttribute('data-mailto'), fd = new FormData(f), lines = [], subj = f.getAttribute('data-subject') || 'Connected Renter enquiry';
      fd.forEach(function (v, k) { if (k === 'subject' && v) subj = v; else if (v) lines.push(k.charAt(0).toUpperCase() + k.slice(1) + ': ' + v); });
      w.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(lines.join('\n'));
      var m = $('.form-msg', f); if (m) m.classList.add('show');
    });
  });

  var yr = $('[data-year]'); if (yr) yr.textContent = new Date().getFullYear();
})();

/* v2 interactions: moving-day toggle, scroll story, horizontal gallery, flip cards */
(function () {
  'use strict';
  var d = document, w = window;
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }

  /* hero: Moving day <-> Move-in day */
  var tg = $('[data-mode-toggle]'), hero = $('.phero');
  if (tg && hero) {
    var auto = setInterval(function () { flip(); }, 6500);
    function flip(user) {
      var on = tg.getAttribute('aria-pressed') !== 'true';
      tg.setAttribute('aria-pressed', on);
      hero.classList.toggle('home-mode', on);
      $$('[data-day]', hero).forEach(function (el) { el.hidden = (el.getAttribute('data-day') === 'home') !== on; });
      if (user) clearInterval(auto);
    }
    tg.addEventListener('click', function () { flip(true); });
    if (reduce) clearInterval(auto);
  }

  /* pinned scroll story */
  $$('.story').forEach(function (st) {
    var steps = $$('.story-step', st), bgs = $$('.story-bg', st), dots = $$('.story-dots i', st), road = $('.road', st), n = steps.length, cur = -1;
    function upd() {
      var r = st.getBoundingClientRect(), total = st.offsetHeight - w.innerHeight;
      var p = Math.min(1, Math.max(0, -r.top / (total || 1)));
      var i = Math.min(n - 1, Math.floor(p * n));
      if (road) road.style.setProperty('--p', p.toFixed(4));
      if (i !== cur) {
        cur = i;
        [steps, bgs, dots].forEach(function (arr) { arr.forEach(function (el, k) { el.classList.toggle('on', k === i); }); });
      }
    }
    w.addEventListener('scroll', upd, { passive: true }); w.addEventListener('resize', upd); upd();
  });

  /* pinned horizontal gallery (desktop); native swipe on small screens */
  $$('.hgal').forEach(function (g) {
    var track = $('.hgal-track', g), bar = $('.hgal-bar', g), mq = w.matchMedia('(max-width: 720px)');
    function size() {
      if (mq.matches) { g.style.height = ''; track.style.transform = ''; return; }
      var extra = Math.max(0, track.scrollWidth - w.innerWidth);
      g.style.height = (w.innerHeight + extra) + 'px';
      g._extra = extra; upd();
    }
    function upd() {
      if (mq.matches) return;
      var r = g.getBoundingClientRect(), p = Math.min(1, Math.max(0, -r.top / (g._extra || 1)));
      track.style.transform = 'translate3d(' + (-p * g._extra) + 'px,0,0)';
      if (bar) bar.style.setProperty('--p', p.toFixed(4));
    }
    w.addEventListener('scroll', upd, { passive: true }); w.addEventListener('resize', size);
    w.addEventListener('load', size); size();
  });

  /* myth/fact flip cards */
  $$('.flip').forEach(function (f) {
    f.addEventListener('click', function () { var on = f.classList.toggle('flipped'); f.setAttribute('aria-pressed', on); });
  });

  /* header over photo heroes */
  var h = $('.site-header');
  if (h && d.body.classList.contains('has-photo-hero')) h.classList.add('over');
})();
