/* militaryhousingrentals.com — all interactive behavior. Every feature is
   progressive: pages render complete without this file. */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };
  var store = {
    get: function (k, f) { try { var v = localStorage.getItem(k); return v === null ? f : JSON.parse(v); } catch (e) { return f; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var money = function (n) { return (n < 0 ? '-$' : '$') + Math.abs(Math.round(n)).toLocaleString('en-US'); };

  /* toast */
  var toastEl = $('[data-toast]'), toastT;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('show'); }, 2200);
  }

  /* header */
  var header = $('[data-header]');
  var onScroll = function () { if (header) header.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var menuBtn = $('[data-menu]'), nav = $('#main-nav');
  if (menuBtn && nav) menuBtn.addEventListener('click', function () {
    var open = !nav.classList.contains('open');
    nav.classList.toggle('open', open); d.body.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
  });

  /* theme */
  var themeBtn = $('[data-theme-toggle]');
  if (themeBtn) themeBtn.addEventListener('click', function () {
    var dark = root.dataset.theme ? root.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme = dark ? 'light' : 'dark';
    try { localStorage.setItem('mhr-theme', root.dataset.theme); } catch (e) {}
  });

  /* hero word rotator */
  var rot = $('[data-rotate]');
  if (rot && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var words = JSON.parse(rot.dataset.rotate || '[]'), wi = 0;
    if (words.length) { rot.textContent = words[0]; setInterval(function () {
      rot.classList.add('out');
      setTimeout(function () { wi = (wi + 1) % words.length; rot.textContent = words[wi]; rot.classList.remove('out'); }, 300);
    }, 2400); }
  }

  /* count-up stats */
  var counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return; co.unobserve(en.target);
        var el = en.target, end = +el.dataset.count, t0 = performance.now();
        (function tick(t) { var p = Math.min(1, (t - t0) / 900); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(tick); })(t0);
      });
    });
    counters.forEach(function (c) { co.observe(c); });
  }

  /* reveal on scroll */
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var ro = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); } }); }, { rootMargin: '0px 0px -40px' });
    $$('.section .card, .steps li, .base-tile').forEach(function (el) {
      if (el.getBoundingClientRect().top > innerHeight) { el.classList.add('reveal'); ro.observe(el); }
    });
  }

  /* saved listings */
  var saved = store.get('mhr-saved', []);
  function syncFavs() {
    $$('[data-fav]').forEach(function (b) {
      var on = saved.indexOf(b.dataset.fav) > -1;
      b.setAttribute('aria-pressed', String(on));
      var lbl = $('[data-fav-label]', b); if (lbl) lbl.textContent = on ? 'Saved' : 'Save';
    });
    $$('[data-saved-count]').forEach(function (c) { c.textContent = saved.length; c.hidden = !saved.length; });
  }
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-fav]'); if (!b) return;
    e.preventDefault();
    var s = b.dataset.fav, i = saved.indexOf(s);
    if (i > -1) { saved.splice(i, 1); toast('Removed from saved listings'); } else { saved.push(s); toast('Saved. Find it under the heart icon.'); }
    store.set('mhr-saved', saved); syncFavs();
    b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop');
    if (window.mhrFilter) window.mhrFilter();
  });
  syncFavs();

  /* share */
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-share]'); if (!b) return;
    var data = { title: b.dataset.title || d.title, url: location.href.split('#')[0] };
    if (navigator.share) { navigator.share(data).catch(function () {}); return; }
    if (navigator.clipboard) navigator.clipboard.writeText(data.url).then(function () { toast('Link copied to clipboard'); });
  });

  /* horizontal scroller buttons */
  $$('[data-scroll]').forEach(function (b) {
    b.addEventListener('click', function () {
      var sc = b.closest('.section').querySelector('[data-scroller]');
      if (sc) sc.scrollBy({ left: +b.dataset.scroll * sc.clientWidth * 0.85, behavior: 'smooth' });
    });
  });

  /* ---------- maps (Leaflet) ---------- */
  function makeMap(el, pins) {
    if (!window.L || el._map) return el._map;
    var map = L.map(el, { scrollWheelZoom: false });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; OpenStreetMap contributors' }).addTo(map);
    var icon = L.divIcon({ className: '', html: '<div class="pin" style="width:26px;height:26px"></div>', iconSize: [26, 26], iconAnchor: [13, 26], popupAnchor: [0, -24] });
    var markers = {};
    pins.forEach(function (p) {
      var m = L.marker([p.lat, p.lng], { icon: icon, title: p.title });
      var box = d.createElement('div'); box.className = 'map-pop';
      var img = d.createElement('img'); img.src = p.img; img.alt = '';
      var t = d.createElement('strong'); t.textContent = p.title;
      var a = d.createElement('span'); a.textContent = p.addr + ' · ' + p.price;
      var link = d.createElement('a'); link.href = '/properties/' + p.slug + '/'; link.textContent = 'View listing →';
      box.append(img, t, a, link);
      m.bindPopup(box); m.addTo(map); markers[p.slug] = m;
    });
    el._map = map; el._markers = markers;
    fit(el, pins.map(function (p) { return p.slug; }));
    return map;
  }
  function fit(el, slugs) {
    var map = el._map; if (!map) return;
    var pts = [];
    Object.keys(el._markers).forEach(function (s) {
      var m = el._markers[s], on = slugs.indexOf(s) > -1;
      if (on) { if (!map.hasLayer(m)) m.addTo(map); pts.push(m.getLatLng()); } else if (map.hasLayer(m)) map.removeLayer(m);
    });
    if (pts.length === 1) map.setView(pts[0], 12);
    else if (pts.length) map.fitBounds(L.latLngBounds(pts).pad(0.2));
    else map.setView([37.8, -96], 4);
  }
  function whenLeaflet(cb) { if (window.L) cb(); else window.addEventListener('load', function () { if (window.L) cb(); }); }

  /* ---------- listing filters ---------- */
  var wrap = $('[data-listings]');
  var form = wrap && $('[data-filters]', wrap);
  if (wrap && form) {
    var grid = $('[data-grid]', wrap), cards = $$('.listing-card', grid), pins = JSON.parse(($('[data-pins]', wrap) || {}).textContent || '[]');
    var mapEl = $('[data-map]', wrap), mapPanel = $('[data-map-panel]', wrap), amen = [], savedOnly = false;
    var params = new URLSearchParams(location.search);
    ['q', 'base', 'beds', 'baths', 'sort'].forEach(function (k) { if (params.get(k) && form.elements[k]) form.elements[k].value = params.get(k); });
    if (params.get('saved')) { savedOnly = true; $('[data-saved-only]', form).setAttribute('aria-pressed', 'true'); }

    var apply = window.mhrFilter = function () {
      var q = (form.elements.q.value || '').toLowerCase().trim(), base = form.elements.base ? form.elements.base.value : '';
      var beds = +form.elements.beds.value || 0, baths = +form.elements.baths.value || 0, sort = form.elements.sort.value;
      var shown = [];
      cards.forEach(function (c) {
        var ds = c.dataset, ok = (!q || q.split(/\s+/).every(function (w) { return ds.q.indexOf(w) > -1; })) &&
          (!base || ds.base === base) && (+ds.beds >= beds) && (+ds.baths >= baths) &&
          amen.every(function (a) { return ds.q.indexOf(a) > -1; }) && (!savedOnly || saved.indexOf(ds.slug) > -1);
        c.classList.toggle('is-hidden', !ok); if (ok) shown.push(ds.slug);
      });
      var key = { new: function (c) { return c.dataset.date; }, beds: function (c) { return +c.dataset.beds; }, sqft: function (c) { return +c.dataset.sqft; }, az: function (c) { return c.querySelector('.card-title').textContent; } }[sort];
      cards.slice().sort(function (a, b) {
        var x = key(a), y = key(b);
        return sort === 'az' ? String(x).localeCompare(y) : (x < y ? 1 : x > y ? -1 : 0);
      }).forEach(function (c) { grid.appendChild(c); });
      $('[data-count-shown]', wrap).textContent = shown.length;
      $('[data-empty]', wrap).hidden = shown.length > 0;
      var active = q || base || beds || baths || amen.length || savedOnly;
      $('[data-reset]', wrap).hidden = !active;
      var p = new URLSearchParams();
      if (q) p.set('q', q); if (base) p.set('base', base); if (beds) p.set('beds', beds); if (baths) p.set('baths', baths);
      if (sort !== 'new') p.set('sort', sort); if (savedOnly) p.set('saved', '1');
      history.replaceState(null, '', location.pathname + (p.toString() ? '?' + p : ''));
      if (mapEl && mapEl._map) fit(mapEl, shown);
    };
    form.addEventListener('input', apply);
    form.addEventListener('change', apply);
    $$('[data-amenity]', form).forEach(function (b) {
      b.addEventListener('click', function () {
        var on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', String(on));
        var a = b.dataset.amenity; if (on) amen.push(a); else amen.splice(amen.indexOf(a), 1); apply();
      });
    });
    $('[data-saved-only]', form).addEventListener('click', function () {
      savedOnly = !savedOnly; this.setAttribute('aria-pressed', String(savedOnly)); apply();
    });
    $('[data-reset]', wrap).addEventListener('click', function () {
      form.reset(); amen = []; savedOnly = false;
      $$('[aria-pressed]', form).forEach(function (b) { if (!b.dataset.view) b.setAttribute('aria-pressed', 'false'); });
      apply();
    });
    $$('[data-view]', form).forEach(function (b) {
      b.addEventListener('click', function () {
        var map = b.dataset.view === 'map';
        $$('[data-view]', form).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        mapPanel.hidden = !map;
        if (map) whenLeaflet(function () { makeMap(mapEl, pins); mapEl._map.invalidateSize(); apply(); });
      });
    });
    // highlight a pin when hovering a card
    cards.forEach(function (c) {
      c.addEventListener('mouseenter', function () { var m = mapEl && mapEl._markers && mapEl._markers[c.dataset.slug]; if (m && m._icon) m._icon.firstChild.classList.add('hl'); });
      c.addEventListener('mouseleave', function () { var m = mapEl && mapEl._markers && mapEl._markers[c.dataset.slug]; if (m && m._icon) m._icon.firstChild.classList.remove('hl'); });
    });
    apply();
  }
  // standalone map (bases page)
  $$('[data-map-auto]').forEach(function (el) {
    var pins = JSON.parse((el.closest('[data-listings]').querySelector('[data-pins]') || {}).textContent || '[]');
    if ('IntersectionObserver' in window) {
      var mo = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { mo.disconnect(); whenLeaflet(function () { makeMap(el, pins); }); } });
      mo.observe(el);
    } else whenLeaflet(function () { makeMap(el, pins); });
  });
  // branch filter (bases page)
  var bf = $('[data-branch-filter]');
  if (bf) bf.addEventListener('click', function (e) {
    var b = e.target.closest('[data-branch]'); if (!b) return;
    $$('[data-branch]', bf).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    $$('[data-base-cards] .base-card').forEach(function (c) { c.classList.toggle('is-hidden', !!b.dataset.branch && c.dataset.branch.indexOf(b.dataset.branch) < 0); });
  });

  /* ---------- gallery lightbox ---------- */
  var gal = $('[data-gallery]'), lb = $('[data-lightbox]');
  if (gal && lb) {
    var items = JSON.parse($('[data-gallery-items]', gal).textContent), idx = 0, lastFocus;
    var lbImg = $('[data-lb-img]', lb), lbCap = $('[data-lb-cap]', lb);
    var show = function (i) {
      idx = (i + items.length) % items.length;
      lbImg.src = items[idx].src; lbImg.alt = items[idx].alt;
      lbCap.textContent = (idx + 1) + ' / ' + items.length + (items[idx].credit ? ' · ' + items[idx].credit : '');
    };
    var open = function (i) { lastFocus = d.activeElement; show(i); lb.hidden = false; d.body.style.overflow = 'hidden'; $('[data-lb-close]', lb).focus(); };
    var close = function () { lb.hidden = true; d.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); };
    $$('[data-index]', gal).forEach(function (b) { b.addEventListener('click', function () { open(+b.dataset.index); }); });
    $('[data-lb-close]', lb).addEventListener('click', close);
    $$('[data-lb-step]', lb).forEach(function (b) { b.addEventListener('click', function () { show(idx + +b.dataset.lbStep); }); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    d.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(idx + 1); if (e.key === 'ArrowLeft') show(idx - 1);
    });
    var tx = null;
    lb.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (tx === null) return; var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); tx = null; });
    if (items.length < 2) $$('.lb-nav', lb).forEach(function (b) { b.hidden = true; });
  }

  /* ---------- BAH calculator ---------- */
  $$('[data-widget="bah"]').forEach(function (w) {
    var ins = {}; $$('[data-bah-in]', w).forEach(function (i) { ins[i.dataset.bahIn] = i; });
    var out = {}; $$('[data-bah-out]', w).forEach(function (o) { out[o.dataset.bahOut] = o; });
    var fill = $('[data-bah-fill]', w), meter = $('[data-bah-meter]', w);
    var saved = store.get('mhr-bah', null);
    if (saved) Object.keys(saved).forEach(function (k) { if (ins[k]) ins[k].value = saved[k]; });
    var calc = function () {
      var v = {}; Object.keys(ins).forEach(function (k) { v[k] = Math.max(0, +ins[k].value || 0); });
      var total = v.rent + v.util + v.extra, left = v.bah - total, pct = v.bah ? total / v.bah * 100 : 0;
      out.total.textContent = money(total); out.left.textContent = money(left); out.year.textContent = money(left * 12);
      out.left.style.color = out.year.style.color = left < 0 ? 'var(--red)' : 'var(--green)';
      fill.style.width = Math.min(100, pct) + '%';
      fill.classList.toggle('warn', pct > 90 && pct <= 100); fill.classList.toggle('over', pct > 100);
      meter.setAttribute('aria-label', Math.round(pct) + '% of BAH used');
      out.msg.textContent = !v.bah ? 'Enter your monthly BAH to get started.' :
        pct > 100 ? 'This home costs ' + money(-left) + ' a month more than your BAH. That gap comes out of base pay.' :
        pct > 90 ? 'Tight fit: you are using ' + Math.round(pct) + '% of your BAH.' :
        'Comfortable: you keep ' + money(left) + ' a month, or ' + money(left * 12) + ' a year.';
      var s = {}; Object.keys(v).forEach(function (k) { s[k] = v[k]; }); store.set('mhr-bah', s);
    };
    w.addEventListener('input', calc); calc();
  });

  /* ---------- PCS countdown ---------- */
  $$('[data-widget="pcs"]').forEach(function (w) {
    var input = $('[data-pcs-date]', w), count = $('[data-pcs-count]', w), days = $('[data-pcs-days]', w);
    var steps = $$('[data-pcs-timeline] li', w);
    var v = store.get('mhr-pcs', '');
    if (!v) { var t = new Date(); t.setDate(t.getDate() + 75); v = t.toISOString().slice(0, 10); }
    input.value = v;
    var fmt = function (dt) { return dt.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }); };
    var run = function () {
      if (!input.value) { count.hidden = true; return; }
      var rnlt = new Date(input.value + 'T12:00:00'), now = new Date(); now.setHours(12, 0, 0, 0);
      var diff = Math.round((rnlt - now) / 864e5);
      count.hidden = false; days.textContent = Math.abs(diff);
      $('[data-pcs-label]', w).textContent = diff >= 0 ? (diff === 1 ? 'day until you report' : 'days until you report') : 'days since your report date';
      var nextSet = false;
      steps.forEach(function (li) {
        var when = new Date(rnlt); when.setDate(when.getDate() + +li.dataset.offset);
        var tag = li.querySelector('.when');
        if (!tag) { tag = d.createElement('span'); tag.className = 'when'; li.insertBefore(tag, li.firstChild); }
        tag.textContent = fmt(when);
        var done = when < now; li.classList.toggle('done', done);
        li.classList.toggle('next', !done && !nextSet); if (!done) nextSet = true;
      });
      store.set('mhr-pcs', input.value);
    };
    input.addEventListener('input', run); run();
  });

  /* ---------- blog ---------- */
  var ps = $('[data-post-search]');
  if (ps) ps.addEventListener('input', function () {
    var q = ps.value.toLowerCase().trim(), n = 0;
    $$('[data-post-q]').forEach(function (c) { var ok = !q || c.dataset.postQ.indexOf(q) > -1; c.hidden = !ok; if (ok) n++; });
    $('[data-post-empty]').hidden = n > 0;
  });
  var bar = $('.progress span'), body = $('.post-body');
  if (bar && body) {
    var prog = function () {
      var r = body.getBoundingClientRect(), h = r.height - innerHeight;
      bar.style.width = Math.max(0, Math.min(100, (-r.top / (h > 0 ? h : 1)) * 100)) + '%';
    };
    window.addEventListener('scroll', prog, { passive: true }); prog();
  }
  var tocLinks = $$('[data-toc] a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var heads = tocLinks.map(function (a) { return d.getElementById(decodeURIComponent(a.hash.slice(1))); }).filter(Boolean);
    var to = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        tocLinks.forEach(function (a) { a.classList.toggle('active', a.hash === '#' + en.target.id); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    heads.forEach(function (h) { to.observe(h); });
    if (innerWidth < 1000) { var det = $('[data-toc]'); if (det) det.open = false; }
  }
  $$('.schema-faq-section').forEach(function (s, i) {
    var q = $('.schema-faq-question', s); if (!q) return;
    q.setAttribute('role', 'button'); q.tabIndex = 0; q.setAttribute('aria-expanded', i === 0 ? 'true' : 'false');
    if (i === 0) s.classList.add('open');
    var t = function () { var o = s.classList.toggle('open'); q.setAttribute('aria-expanded', String(o)); };
    q.addEventListener('click', t);
    q.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } });
  });

  /* ---------- forms ---------- */
  $$('[data-form]').forEach(function (f) {
    var stepsEl = f.closest('.form-card').querySelector('.form-steps');
    var sets = f.hasAttribute('data-steps') ? $$('[data-step]', f) : [];
    var cur = 0;
    var valid = function (scope) {
      var ok = true;
      $$('input, textarea, select', scope).forEach(function (i) {
        if (i.type === 'hidden' || i.closest('.hp')) return;
        var bad = !i.checkValidity(); i.closest('.field') && i.closest('.field').classList.toggle('invalid', bad);
        if (bad && ok) { ok = false; i.reportValidity(); }
      });
      return ok;
    };
    var go = function (n) {
      cur = n;
      sets.forEach(function (s, i) { s.hidden = i !== cur; });
      $('[data-step-prev]', f).hidden = cur === 0;
      $('[data-step-next]', f).hidden = cur === sets.length - 1;
      $('[data-step-submit]', f).hidden = cur !== sets.length - 1;
      if (stepsEl) $$('li', stepsEl).forEach(function (li, i) { li.classList.toggle('on', i <= cur); });
    };
    if (sets.length) {
      // after a failed server-side submit, open the first step with an empty required field
      var startAt = 0;
      if (f.closest('.form-card').querySelector('.notice-err')) sets.some(function (s, i) { if (!valid(s)) { startAt = i; return true; } });
      go(startAt);
      $('[data-step-next]', f).addEventListener('click', function () { if (valid(sets[cur])) { go(cur + 1); f.scrollIntoView({ behavior: 'smooth', block: 'start' }); } });
      $('[data-step-prev]', f).addEventListener('click', function () { go(cur - 1); });
    }
    f.addEventListener('submit', function (e) {
      if (!valid(f)) { e.preventDefault(); return; }
      var btn = $('[type="submit"]', f); if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    });
  });
})();
