/* thesublet.com — site behaviour (no framework) */
(function () {
  'use strict';
  var d = document;
  d.documentElement.classList.add('js');
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var store = {
    get: function (k, def) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : def; } catch (e) { return def; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var money = function (n) { return '$' + Math.round(n).toLocaleString('en-US'); };

  /* ---------- mobile nav ---------- */
  var toggle = $('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = !d.body.classList.contains('nav-open');
      d.body.classList.toggle('nav-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    $$('#site-nav a').forEach(function (a) { a.addEventListener('click', function () { d.body.classList.remove('nav-open'); toggle.setAttribute('aria-expanded', 'false'); }); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && d.body.classList.contains('nav-open')) { d.body.classList.remove('nav-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); } });
  }

  /* ---------- confirm buttons / check-all ---------- */
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-confirm]');
    if (b && !window.confirm(b.getAttribute('data-confirm'))) e.preventDefault();
  });
  $$('[data-checkall]').forEach(function (c) {
    c.addEventListener('change', function () { $$('input[name="ids[]"]', c.closest('form')).forEach(function (x) { x.checked = c.checked; }); });
  });

  /* ---------- CSRF for forms on cached pages + AJAX submit ---------- */
  var csrfPromise = null;
  function csrf() {
    if (!csrfPromise) csrfPromise = fetch('/api/csrf', { credentials: 'same-origin', cache: 'no-store' }).then(function (r) { return r.json(); }).then(function (j) { return j.token; });
    return csrfPromise;
  }
  $$('form[data-csrf]').forEach(function (f) {
    var filled = false;
    var fill = function () { if (filled) return; filled = true; csrf().then(function (t) { $$('input[name=_csrf]', f).forEach(function (i) { i.value = t; }); }); };
    f.addEventListener('focusin', fill);
    f.addEventListener('pointerdown', fill);
    var det = f.closest('details'); if (det) det.addEventListener('toggle', fill);
  });
  $$('form.js-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = $('.form-msg', f), btn = $('button[type=submit]', f);
      msg.className = 'form-msg'; msg.textContent = 'Sending…'; btn.disabled = true;
      csrf().then(function (t) {
        $$('input[name=_csrf]', f).forEach(function (i) { i.value = t; });
        return fetch(f.action, { method: 'POST', body: new FormData(f), credentials: 'same-origin' });
      }).then(function (r) { return r.json(); }).then(function (j) {
        msg.textContent = j.ok ? j.message : (j.error || 'Something went wrong.');
        msg.className = 'form-msg ' + (j.ok ? 'ok' : 'err');
        if (j.ok) { f.reset(); $$('input,textarea,select,button', f).forEach(function (x) { if (x.type !== 'hidden') x.disabled = true; }); }
        else btn.disabled = false;
      }).catch(function () { msg.textContent = 'Network error — please try again.'; msg.className = 'form-msg err'; btn.disabled = false; });
    });
  });

  /* ---------- favorites ---------- */
  var favs = store.get('ts_favs', []);
  function syncFavs() {
    $$('[data-fav]').forEach(function (b) {
      var on = favs.indexOf(+b.getAttribute('data-fav')) > -1;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (b.classList.contains('fav-btn')) b.textContent = on ? '♥' : '♡';
      else b.textContent = on ? '♥ Saved' : '♡ Save';
    });
    $$('.fav-count').forEach(function (c) { c.textContent = favs.length; c.hidden = !favs.length; });
  }
  d.addEventListener('click', function (e) {
    var b = e.target.closest('[data-fav]');
    if (!b) return;
    e.preventDefault();
    var id = +b.getAttribute('data-fav'), i = favs.indexOf(id);
    if (i > -1) favs.splice(i, 1); else favs.unshift(id);
    favs = favs.slice(0, 60);
    store.set('ts_favs', favs);
    syncFavs();
  });

  /* ---------- compare ---------- */
  var cmp = store.get('ts_cmp', []);
  function syncCmp() {
    $$('[data-compare]').forEach(function (c) { c.checked = cmp.indexOf(+c.getAttribute('data-compare')) > -1; });
    $$('.compare-bar').forEach(function (bar) {
      bar.hidden = cmp.length < 1;
      var n = $('[data-cmp-count]', bar); if (n) n.textContent = cmp.length;
      var l = $('[data-cmp-link]', bar); if (l) l.href = '/compare/?ids=' + cmp.join(',');
    });
  }
  d.addEventListener('change', function (e) {
    var c = e.target.closest('[data-compare]');
    if (!c) return;
    var id = +c.getAttribute('data-compare'), i = cmp.indexOf(id);
    if (c.checked && i < 0) { if (cmp.length >= 4) { c.checked = false; alert('You can compare up to 4 listings.'); return; } cmp.push(id); }
    if (!c.checked && i > -1) cmp.splice(i, 1);
    store.set('ts_cmp', cmp); syncCmp();
  });
  d.addEventListener('click', function (e) { if (e.target.closest('[data-cmp-clear]')) { cmp = []; store.set('ts_cmp', cmp); syncCmp(); } });

  /* ---------- Leaflet loader ---------- */
  var leafletP = null;
  function leaflet() {
    if (window.L) return Promise.resolve(window.L);
    if (leafletP) return leafletP;
    leafletP = new Promise(function (res, rej) {
      var css = d.createElement('link'); css.rel = 'stylesheet'; css.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      css.integrity = 'sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY='; css.crossOrigin = ''; d.head.appendChild(css);
      var s = d.createElement('script'); s.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
      s.integrity = 'sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo='; s.crossOrigin = '';
      s.onload = function () { res(window.L); }; s.onerror = rej; d.head.appendChild(s);
    });
    return leafletP;
  }
  function tiles(L, map) {
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);
  }

  /* ---------- directory: live filters, map ---------- */
  var dir = $('.directory');
  if (dir) {
    var form = $('.filters', dir), results = $('[data-results]', dir), empty = $('[data-empty]', dir);
    var countEl = $('[data-count]', dir), countLbl = $('[data-count-label]', dir), pager = $('.pager', dir);
    var locked = JSON.parse(dir.getAttribute('data-locked') || '[]') || {};
    var current = [], map = null, markers = null, timer = null;
    // seed with server-rendered cards for the map
    var seed = function () { return $$('.card', results).map(function (c) { return +c.getAttribute('data-id'); }); };

    function params() {
      var p = new URLSearchParams(new FormData(form));
      Array.from(p.keys()).forEach(function (k) { if (!p.get(k)) p.delete(k); });
      return p;
    }
    function render(j) {
      current = j.items;
      results.innerHTML = j.items.map(function (c) { return c.html; }).join('');
      empty.hidden = j.items.length > 0;
      countEl.textContent = j.total; countLbl.textContent = j.total === 1 ? 'sublet' : 'sublets';
      if (pager) pager.hidden = true;
      syncFavs(); syncCmp(); drawMarkers();
    }
    function load(updateUrl) {
      var p = params();
      var q = new URLSearchParams(p);
      if (locked.state) q.set('state', locked.state);
      if (locked.city) q.set('city', locked.city);
      Object.keys(locked).forEach(function (k) { if (k !== 'state' && k !== 'city') q.set(k, locked[k]); });
      q.set('per', '200');
      dir.classList.add('is-loading');
      fetch('/api/listings?' + q.toString()).then(function (r) { return r.json(); }).then(function (j) {
        dir.classList.remove('is-loading'); render(j);
        if (updateUrl) { var s = p.toString(); history.replaceState(null, '', location.pathname + (s ? '?' + s : '')); }
      }).catch(function () { dir.classList.remove('is-loading'); });
    }
    form.addEventListener('submit', function (e) { e.preventDefault(); load(true); });
    form.addEventListener('change', function () { load(true); });
    form.addEventListener('input', function (e) { if (e.target.type === 'number' || e.target.type === 'search') { clearTimeout(timer); timer = setTimeout(function () { load(true); }, 450); } });

    function drawMarkers() {
      if (!map || !window.L) return;
      markers.clearLayers();
      var pts = [];
      current.forEach(function (c) {
        if (c.lat == null) return;
        var m = L.circleMarker([c.lat, c.lng], { radius: 9, color: '#fff', weight: 2, fillColor: c.verified ? '#2f6f4f' : '#e46f4c', fillOpacity: .95 });
        m.bindPopup('<strong>' + money(c.rent) + '/mo</strong><br><a href="' + esc(c.url) + '">' + esc(c.title) + '</a><br><small>' + esc(c.type) + ' · ' + esc(c.from_h) + ' → ' + esc(c.to_h) + '</small>');
        markers.addLayer(m); pts.push([c.lat, c.lng]);
      });
      if (pts.length) map.fitBounds(pts, { padding: [30, 30], maxZoom: 13 });
    }
    $$('.vt-btn', dir).forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-view');
        $$('.vt-btn', dir).forEach(function (x) { x.classList.toggle('is-on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        var wrap = $('.map-wrap', dir); wrap.hidden = v !== 'map';
        if (v === 'map') {
          leaflet().then(function (L) {
            if (!map) {
              var lat = +dir.getAttribute('data-lat') || 39.5, lng = +dir.getAttribute('data-lng') || -98.35, z = +dir.getAttribute('data-zoom') || 4;
              map = L.map('map', { scrollWheelZoom: false }).setView([lat, lng], z);
              tiles(L, map); markers = L.layerGroup().addTo(map);
              if (!current.length) { load(false); } else drawMarkers();
            } else { map.invalidateSize(); drawMarkers(); }
          });
        }
      });
    });
    // initial data for the map without re-rendering server HTML
    if (seed().length) {
      var q0 = params(); if (locked.state) q0.set('state', locked.state); if (locked.city) q0.set('city', locked.city);
      Object.keys(locked).forEach(function (k) { if (k !== 'state' && k !== 'city') q0.set(k, locked[k]); });
      q0.set('per', '200');
      fetch('/api/listings?' + q0.toString()).then(function (r) { return r.json(); }).then(function (j) { current = j.items; drawMarkers(); }).catch(function () {});
    }
  }

  /* ---------- listing map (approximate circle) ---------- */
  var lmap = $('#lmap');
  if (lmap) {
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      leaflet().then(function (L) {
        var ll = [+lmap.getAttribute('data-lat'), +lmap.getAttribute('data-lng')];
        var m = L.map(lmap, { scrollWheelZoom: false }).setView(ll, 14);
        tiles(L, m);
        if (lmap.getAttribute('data-exact')) L.circleMarker(ll, { radius: 10, color: '#fff', weight: 3, fillColor: '#0f9d8a', fillOpacity: 1 }).addTo(m);
        else L.circle(ll, { radius: 600, color: '#2f6f4f', fillColor: '#2f6f4f', fillOpacity: .15 }).addTo(m);
      });
    });
    io.observe(lmap);
  }

  /* ---------- pin picker on listing forms ---------- */
  var pin = $('#pinmap');
  if (pin) {
    var f = pin.closest('form');
    var latI = $('input[name=lat]', f), lngI = $('input[name=lng]', f);
    leaflet().then(function (L) {
      var has = latI.value && lngI.value;
      var m = L.map(pin, { scrollWheelZoom: false }).setView(has ? [+latI.value, +lngI.value] : [39.5, -98.35], has ? 14 : 4);
      tiles(L, m);
      var mk = has ? L.circle([+latI.value, +lngI.value], { radius: 500, color: '#2f6f4f' }).addTo(m) : null;
      m.on('click', function (e) {
        latI.value = e.latlng.lat.toFixed(5); lngI.value = e.latlng.lng.toFixed(5);
        if (mk) mk.setLatLng(e.latlng); else mk = L.circle(e.latlng, { radius: 500, color: '#2f6f4f' }).addTo(m);
      });
      $('[data-pin-clear]', f).addEventListener('click', function () { latI.value = ''; lngI.value = ''; if (mk) { m.removeLayer(mk); mk = null; } });
    });
  }

  /* ---------- favorites page ---------- */
  var favList = $('[data-favorites-list]');
  if (favList) {
    if (!favs.length) { favList.innerHTML = ''; $('[data-fav-empty]').hidden = false; }
    else fetch('/api/listings?ids=' + favs.join(',') + '&per=60').then(function (r) { return r.json(); }).then(function (j) {
      var byId = {}; j.items.forEach(function (c) { byId[c.id] = c; });
      var html = favs.map(function (id) { return byId[id] ? byId[id].html : ''; }).join('');
      favList.innerHTML = html; $('[data-fav-empty]').hidden = !!html; syncFavs(); syncCmp();
    });
  }

  /* ---------- compare page ---------- */
  var cmpT = $('[data-compare-table]');
  if (cmpT) {
    var qsIds = new URLSearchParams(location.search).get('ids');
    var ids = qsIds ? qsIds.split(',').map(Number).filter(Boolean).slice(0, 4) : cmp;
    if (!ids.length) { cmpT.innerHTML = ''; $('[data-cmp-empty]').hidden = false; }
    else fetch('/api/listings?full=1&ids=' + ids.join(',')).then(function (r) { return r.json(); }).then(function (j) {
      if (!j.items.length) { cmpT.innerHTML = ''; $('[data-cmp-empty]').hidden = false; return; }
      var it = j.items;
      var rows = [
        ['', function (c) { return (c.photo ? '<img src="' + esc(c.photo) + '" alt="" width="200" height="133" style="border-radius:8px;object-fit:cover">' : '') + '<br><a href="' + esc(c.url) + '"><strong>' + esc(c.title) + '</strong></a>'; }],
        ['Rent', function (c) { return money(c.rent) + '/mo' + (c.utilities ? ' (utilities incl.)' : ''); }],
        ['Deposit', function (c) { return c.deposit ? money(c.deposit) : '—'; }],
        ['Location', function (c) { return esc((c.neighborhood ? c.neighborhood + ', ' : '') + c.city + ', ' + c.state); }],
        ['Type', function (c) { return esc(c.type) + (c.furnished ? ', furnished' : ', unfurnished'); }],
        ['Beds / baths', function (c) { return esc(c.beds) + ' / ' + esc(c.baths); }],
        ['Dates', function (c) { return esc(c.from_h) + ' → ' + esc(c.to_h); }],
        ['Min stay', function (c) { return c.min_stay + ' mo'; }],
        ['Pets', function (c) { return esc(c.pets_h); }],
        ['Amenities', function (c) { return esc((c.amenities || []).join(', ')) || '—'; }],
        ['Host', function (c) { return c.verified ? '✔ Verified host' : 'Free listing'; }],
        ['', function (c) { return '<button class="btn btn-sm btn-ghost" data-cmp-remove="' + c.id + '">Remove</button>'; }]
      ];
      cmpT.innerHTML = '<table class="tbl">' + rows.map(function (r) { return '<tr><th>' + r[0] + '</th>' + it.map(function (c) { return '<td>' + r[1](c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</table>';
    });
    d.addEventListener('click', function (e) {
      var b = e.target.closest('[data-cmp-remove]'); if (!b) return;
      cmp = cmp.filter(function (x) { return x !== +b.getAttribute('data-cmp-remove'); }); store.set('ts_cmp', cmp);
      location.href = '/compare/?ids=' + cmp.join(',');
    });
  }

  syncFavs(); syncCmp();
})();

/* v2 effects: scroll reveal, counters, header depth */
(function () {
  'use strict';
  var d = document, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var els = Array.prototype.slice.call(d.querySelectorAll('.reveal, .card, .post-card'));
  if (!('IntersectionObserver' in window) || reduce) { els.forEach(function (e) { e.classList.add('in'); }); }
  else {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (e) { if (!e.classList.contains('reveal')) e.classList.add('reveal'); io.observe(e); });
    // anything already on screen at load
    setTimeout(function () { els.forEach(function (e) { var r = e.getBoundingClientRect(); if (r.top < innerHeight) e.classList.add('in'); }); }, 60);
  }
  // count-up numbers
  var nums = Array.prototype.slice.call(d.querySelectorAll('[data-count]'));
  if (nums.length && 'IntersectionObserver' in window && !reduce) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return; cio.unobserve(en.target);
        var el = en.target, to = +el.getAttribute('data-count') || 0, t0 = performance.now(), dur = 1400;
        (function step(t) { var p = Math.min(1, (t - t0) / dur), v = Math.round(to * (1 - Math.pow(1 - p, 3))); el.textContent = v.toLocaleString('en-US'); if (p < 1) requestAnimationFrame(step); })(t0);
      });
    }, { threshold: 0.4 });
    nums.forEach(function (n) { n.textContent = '0'; cio.observe(n); });
  }
  // header shadow on scroll
  var h = d.querySelector('.site-header');
  if (h) { var on = function () { h.classList.toggle('scrolled', window.scrollY > 8); }; on(); window.addEventListener('scroll', on, { passive: true }); }
})();
