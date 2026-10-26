/* Houston Apartments — maps: search app with freehand draw, home mini-map, property map */
(function () {
  'use strict';
  if (!window.L) return;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var MS = window.HA_MAP || {};
  var HOUSTON = [29.7604, -95.3698];

  function baseMap(el, opts) {
    var map = L.map(el, Object.assign({ zoomControl: true, attributionControl: true, minZoom: 8, maxZoom: 18 }, opts || {}));
    if (L.maplibreGL && window.maplibregl && MS.style) {
      L.maplibreGL({ style: MS.style, attribution: MS.attr, interactive: false }).addTo(map);
    } else {
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap', maxZoom: 19 }).addTo(map);
    }
    return map;
  }
  function shortPrice(p) {
    if (!p) return 'Call';
    return p >= 1000 ? '$' + (p / 1000).toFixed(p % 1000 >= 50 ? 1 : 0).replace('.0', '') + 'k' : '$' + p;
  }
  function pinIcon(price, cls) {
    return L.divIcon({ className: 'pin' + (cls ? ' ' + cls : ''), html: '<span>' + shortPrice(price) + '</span>', iconSize: [0, 0] });
  }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

  function cardHTML(c) {
    var photos = c.photos.length ? c.photos : ['/assets/img/Houston-High-Rise.webp'];
    var imgs = photos.map(function (src, k) { return '<img src="' + esc(src) + '" alt="" loading="lazy" decoding="async" width="600" height="400">'; }).join('');
    var dots = photos.length > 1 ? '<span class="card-dots">' + photos.map(function (_, k) { return '<i' + (k ? '' : ' class="on"') + '></i>'; }).join('') + '</span>' : '';
    var badges = (c['new'] ? '<span class="badge badge-new">New build</span>' : '') + (c.special ? '<span class="badge badge-hot">Special</span>' : '') + (c.pets ? '<span class="badge">Pet friendly</span>' : '');
    return '<article class="card tilt reveal" data-id="' + c.id + '">' +
      '<a class="card-media" href="' + esc(c.url) + '" tabindex="-1" aria-hidden="true"><div class="card-slides">' + imgs + '</div>' + dots + '<span class="card-badges">' + badges + '</span></a>' +
      '<button class="fav" type="button" aria-label="Save ' + esc(c.name) + '" aria-pressed="false" data-fav="' + c.id + '">♥</button>' +
      '<div class="card-body"><p class="card-price">' + esc(c.price) + '</p><h3 class="card-title"><a href="' + esc(c.url) + '">' + esc(c.name) + '</a></h3>' +
      '<p class="card-addr">' + esc(c.address) + '</p><p class="card-meta"><span>' + esc(c.beds) + '</span>' + (c.sqft ? '<span>' + esc(c.sqft) + '</span>' : '') +
      (c.rating ? '<span class="stars">★ ' + c.rating + '</span>' : '') + '</p></div></article>';
  }
  function popupHTML(c) {
    return '<a class="pop" href="' + esc(c.url) + '"><img src="' + esc(c.photos[0] || '/assets/img/Houston-High-Rise.webp') + '" alt=""><div><strong>' + esc(c.name) + '</strong><span class="pp">' + esc(c.price) + '</span> · ' + esc(c.beds) + '</div></a>';
  }

  /* ------------------------------------------------------------ search app */
  var app = $('#search-app');
  if (app) initSearch(app);

  function initSearch(app) {
    var form = $('#filters', app), mapEl = $('#search-map', app), pane = $('.map-pane', app);
    var listEl = $('[data-results]', app), totalEl = $('[data-total]', app), avgEl = $('[data-avg]', app), pager = $('[data-pager]', app), chipsEl = $('[data-chips]', app);
    var drawBtn = $('[data-draw]', app), clearBtn = $('[data-clear-draw]', app), moveChk = $('[data-move-search]', app), hint = $('.draw-hint', app);
    var center = JSON.parse(app.getAttribute('data-center'));
    var map = baseMap(mapEl, { center: [center[0], center[1]], zoom: center[2], zoomControl: false });
    L.control.zoom({ position: 'bottomright' }).addTo(map);

    var cluster = L.markerClusterGroup ? L.markerClusterGroup({ showCoverageOnHover: false, maxClusterRadius: 45, disableClusteringAtZoom: 15 }) : L.layerGroup();
    map.addLayer(cluster);
    var markers = {}, cards = {}, polyLayer = null, poly = null, useBounds = false, firstFit = true, reqId = 0, page = 1, mapMovedByCode = false;

    /* --- state <-> form <-> URL --- */
    var params = new URLSearchParams(location.search);
    function setForm() {
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name) return;
        var v = params.get(el.name);
        if (el.type === 'checkbox') el.checked = v === el.value;
        else if (el.type === 'radio') el.checked = (v || '') === el.value;
        else if (v !== null) el.value = v;
      });
      $$('[data-multi]', form).forEach(function (g) {
        var vals = (params.get(g.getAttribute('data-multi')) || '').split(',');
        $$('input', g).forEach(function (i) { i.checked = vals.indexOf(i.value) > -1; });
      });
      if (params.get('poly')) {
        poly = params.get('poly').split(';').map(function (p) { return p.split(',').map(Number); }).filter(function (p) { return p.length === 2 && !isNaN(p[0]); });
        if (poly.length > 2) drawPoly(); else poly = null;
      }
      page = +(params.get('page') || 1);
    }
    function state() {
      var s = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name || el.closest('[data-multi]')) return;
        if ((el.type === 'checkbox' || el.type === 'radio') && !el.checked) return;
        if (el.value !== '') s[el.name] = el.value;
      });
      $$('[data-multi]', form).forEach(function (g) {
        var vals = $$('input:checked', g).map(function (i) { return i.value; });
        if (vals.length) s[g.getAttribute('data-multi')] = vals.join(',');
      });
      if (poly) s.poly = poly.map(function (p) { return p[0].toFixed(5) + ',' + p[1].toFixed(5); }).join(';');
      if (page > 1) s.page = page;
      return s;
    }

    /* --- fetching --- */
    var timer;
    function search(resetPage) {
      if (resetPage) page = 1;
      clearTimeout(timer);
      timer = setTimeout(run, 120);
    }
    function run() {
      var s = state(), q = new URLSearchParams(s);
      history.replaceState(null, '', '/apartments/' + (q.toString() ? '?' + q : ''));
      if (useBounds && !poly && moveChk.checked) {
        var b = map.getBounds();
        q.set('bounds', [b.getSouth(), b.getWest(), b.getNorth(), b.getEast()].map(function (n) { return n.toFixed(5); }).join(','));
      }
      q.set('per', 24);
      var id = ++reqId;
      app.classList.add('loading');
      fetch('/api/search?' + q).then(function (r) { return r.json(); }).then(function (res) {
        if (id !== reqId) return;
        app.classList.remove('loading');
        render(res);
      }).catch(function () { app.classList.remove('loading'); listEl.innerHTML = '<div class="no-results">Couldn’t load listings. Please refresh.</div>'; });
      ui();
    }

    function render(res) {
      totalEl.textContent = res.total.toLocaleString() + (res.total === 1 ? ' apartment' : ' apartments');
      avgEl.textContent = res.avg ? '· avg. starting rent $' + res.avg.toLocaleString() : '';
      cards = {};
      if (!res.items.length) {
        listEl.innerHTML = '<div class="no-results"><h3>No matches here yet</h3><p>Try widening your price range, removing a filter, or drawing a bigger area.</p><button class="btn btn-outline" type="button" data-reset>Reset filters</button></div>';
      } else {
        listEl.innerHTML = res.items.map(cardHTML).join('');
        res.items.forEach(function (c) { cards[c.id] = c; });
      }
      window.HA_reveal && window.HA_reveal(listEl);
      window.HA_syncFavs && window.HA_syncFavs(listEl);
      listEl.parentNode.scrollTop = 0;

      /* markers */
      cluster.clearLayers();
      markers = {};
      var latlngs = [];
      res.markers.forEach(function (m, i) {
        var mk = L.marker([m[1], m[2]], { icon: pinIcon(m[3], firstFit ? 'drop' : ''), riseOnHover: true });
        mk.on('click', function () { openPin(m[0], m); });
        markers[m[0]] = mk;
        cluster.addLayer(mk);
        latlngs.push([m[1], m[2]]);
      });
      if (firstFit && latlngs.length && !poly) {
        mapMovedByCode = true;
        map.fitBounds(latlngs, { padding: [60, 60], maxZoom: 14 });
      }
      firstFit = false;

      /* pager */
      pager.innerHTML = '';
      if (res.pages > 1) {
        for (var n = 1; n <= res.pages; n++) {
          var b = document.createElement('button');
          b.type = 'button'; b.textContent = n;
          if (n === res.page) b.setAttribute('aria-current', 'page');
          b.addEventListener('click', (function (n) { return function () { page = n; run(); }; })(n));
          pager.appendChild(b);
        }
      }
    }

    function openPin(id, m) {
      var c = cards[id];
      var mk = markers[id];
      if (c) {
        mk.bindPopup(popupHTML(c), { offset: [0, -28], closeButton: false }).openPopup();
        var card = listEl.querySelector('[data-id="' + id + '"]');
        if (card) {
          card.scrollIntoView({ behavior: 'smooth', block: 'center' });
          card.classList.add('hl');
          setTimeout(function () { card.classList.remove('hl'); }, 1600);
        }
      } else {
        location.href = '/apartment/' + m[4] + '/';
      }
    }

    /* card hover ↔ pin highlight */
    listEl.addEventListener('mouseover', function (e) {
      var card = e.target.closest('.card');
      $$('.pin.hl', mapEl).forEach(function (p) { p.classList.remove('hl'); });
      if (!card) return;
      var mk = markers[card.getAttribute('data-id')];
      if (mk && mk._icon) mk._icon.classList.add('hl');
    });

    /* --- filter UI --- */
    form.addEventListener('change', function (e) {
      if (e.target.name === 'area') {
        firstFit = true; useBounds = false; clearPoly(true);
        var opt = e.target.value;
        if (!opt) { mapMovedByCode = true; map.setView(HOUSTON, 10); }
      }
      search(true);
    });
    var qTimer;
    form.q.addEventListener('input', function () { clearTimeout(qTimer); qTimer = setTimeout(function () { firstFit = true; useBounds = false; search(true); }, 350); });

    $$('[data-dd]', form).forEach(function (dd) {
      var btn = $('.dd-btn', dd), panel = $('.dd-panel', dd);
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        var open = panel.hidden;
        closeAll();
        panel.hidden = !open;
        btn.setAttribute('aria-expanded', String(open));
      });
      panel.addEventListener('click', function (e) { e.stopPropagation(); });
    });
    var more = $('[data-more]', form), morePanel = $('#more-panel');
    more.addEventListener('click', function (e) { e.stopPropagation(); var open = morePanel.hidden; closeAll(); morePanel.hidden = !open; more.setAttribute('aria-expanded', String(open)); });
    morePanel.addEventListener('click', function (e) { e.stopPropagation(); });
    $('[data-more-done]', form).addEventListener('click', closeAll);
    function closeAll() {
      $$('.dd-panel', form).forEach(function (p) { p.hidden = true; });
      $$('.dd-btn', form).forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
      morePanel.hidden = true;
    }
    document.addEventListener('click', closeAll);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closeAll(); if (drawing) stopDraw(); } });

    $$('[data-preset]', form).forEach(function (b) {
      b.addEventListener('click', function () {
        var v = b.getAttribute('data-preset').split(',');
        form.price_min.value = v[0] === '0' ? '' : v[0];
        form.price_max.value = v[1] || '';
        search(true);
      });
    });
    app.addEventListener('click', function (e) {
      if (!e.target.closest('[data-reset]')) return;
      form.reset();
      $$('[data-multi] input', form).forEach(function (i) { i.checked = false; });
      clearPoly(true); useBounds = false; firstFit = true;
      search(true);
    });

    var labels = { pets: 'Pets', parking: 'Parking', special: 'Specials', furnished: 'Furnished', essential: 'Essential housing' };
    function ui() {
      var s = state();
      var priceBtn = $('[data-label="price"]', form), bedsBtn = $('[data-label="beds"]', form);
      var pl = s.price_min || s.price_max ? (s.price_min ? '$' + (+s.price_min).toLocaleString() : '$0') + ' – ' + (s.price_max ? '$' + (+s.price_max).toLocaleString() : 'Any') : 'Price';
      priceBtn.textContent = pl; priceBtn.parentNode.classList.toggle('active', pl !== 'Price');
      var bl = s.beds ? s.beds.split(',').map(function (b) { return b === '0' ? 'Studio' : b === '4' ? '4+' : b; }).join(', ') + ' bd' : '';
      if (s.baths) bl += (bl ? ' · ' : '') + s.baths + '+ ba';
      bedsBtn.textContent = bl || 'Beds / Baths'; bedsBtn.parentNode.classList.toggle('active', !!bl);
      form.area.classList.toggle('active', !!s.area);
      form.sort.classList.toggle('active', !!s.sort);
      var moreCount = ['parking', 'special', 'furnished', 'essential', 'sqft', 'year'].filter(function (k) { return s[k]; }).length + (s.amen ? s.amen.split(',').length : 0);
      var badge = $('.count-badge', more);
      badge.hidden = !moreCount; badge.textContent = moreCount; more.classList.toggle('active', moreCount > 0);

      chipsEl.innerHTML = '';
      var chip = function (text, clear) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = text;
        b.addEventListener('click', function () { clear(); search(true); });
        chipsEl.appendChild(b);
      };
      if (poly) chip('Drawn area', function () { clearPoly(true); });
      Object.keys(labels).forEach(function (k) { if (s[k]) chip(labels[k], function () { form[k].checked = false; }); });
      if (s.amen) s.amen.split(',').forEach(function (a) {
        var box = $('[data-multi="amen"] input[value="' + a + '"]', form);
        if (box) chip(box.parentNode.textContent.trim(), function () { box.checked = false; });
      });
    }

    /* --- search as I move --- */
    map.on('moveend', function () {
      if (mapMovedByCode) { mapMovedByCode = false; return; }
      if (!moveChk.checked || poly) return;
      useBounds = true;
      search(true);
    });
    moveChk.addEventListener('change', function () { useBounds = moveChk.checked; search(true); });

    /* --- freehand draw --- */
    var drawing = false, pts = [], line = null;
    function startDraw() {
      drawing = true;
      drawBtn.classList.add('on'); $('span:last-child', drawBtn).textContent = 'Cancel';
      pane.classList.add('drawing'); hint.hidden = false;
      map.dragging.disable(); map.doubleClickZoom.disable(); map.boxZoom.disable();
      if (window.matchMedia('(max-width: 900px)').matches) app.classList.add('show-map');
    }
    function stopDraw() {
      drawing = false; pts = [];
      if (line) { map.removeLayer(line); line = null; }
      drawBtn.classList.remove('on'); $('span:last-child', drawBtn).textContent = 'Draw area';
      pane.classList.remove('drawing'); hint.hidden = true;
      map.dragging.enable(); map.doubleClickZoom.enable(); map.boxZoom.enable();
    }
    drawBtn.addEventListener('click', function () { drawing ? stopDraw() : startDraw(); });
    clearBtn.addEventListener('click', function () { clearPoly(true); useBounds = false; search(true); });

    var c = map.getContainer(), down = false;
    function ll(e) {
      var r = c.getBoundingClientRect();
      return map.containerPointToLatLng([e.clientX - r.left, e.clientY - r.top]);
    }
    c.addEventListener('pointerdown', function (e) {
      if (!drawing || e.target.closest('.leaflet-control')) return;
      e.preventDefault();
      down = true; pts = [ll(e)];
      c.setPointerCapture && c.setPointerCapture(e.pointerId);
      line = L.polyline(pts, { color: '#e2445c', weight: 3, dashArray: '6 6' }).addTo(map);
    });
    c.addEventListener('pointermove', function (e) {
      if (!drawing || !down) return;
      var p = ll(e), last = pts[pts.length - 1];
      if (map.latLngToContainerPoint(p).distanceTo(map.latLngToContainerPoint(last)) < 4) return;
      pts.push(p); line.setLatLngs(pts);
    });
    function finish() {
      if (!drawing || !down) return;
      down = false;
      if (pts.length < 6) { stopDraw(); return; }
      poly = simplify(pts.map(function (p) { return [p.lat, p.lng]; }), 0.0004);
      stopDraw();
      drawPoly();
      useBounds = false;
      search(true);
    }
    c.addEventListener('pointerup', finish);
    c.addEventListener('pointercancel', finish);
    c.style.touchAction = 'pan-x pan-y';
    app.addEventListener('touchmove', function (e) { if (drawing && down) e.preventDefault(); }, { passive: false });

    function drawPoly() {
      if (polyLayer) map.removeLayer(polyLayer);
      polyLayer = L.polygon(poly, { color: '#e2445c', weight: 3, fillColor: '#e2445c', fillOpacity: 0.08, className: 'drawn-area' }).addTo(map);
      mapMovedByCode = true;
      map.fitBounds(polyLayer.getBounds(), { padding: [40, 40] });
      clearBtn.hidden = false;
    }
    function clearPoly(silent) {
      poly = null;
      if (polyLayer) { map.removeLayer(polyLayer); polyLayer = null; }
      clearBtn.hidden = true;
      if (!silent) search(true);
    }
    /* Douglas-Peucker on lat/lng pairs */
    function simplify(points, tol) {
      if (points.length < 4) return points;
      var sqTol = tol * tol;
      function segDist(p, a, b) {
        var x = a[0], y = a[1], dx = b[0] - x, dy = b[1] - y;
        if (dx || dy) { var t = ((p[0] - x) * dx + (p[1] - y) * dy) / (dx * dx + dy * dy); if (t > 1) { x = b[0]; y = b[1]; } else if (t > 0) { x += dx * t; y += dy * t; } }
        dx = p[0] - x; dy = p[1] - y; return dx * dx + dy * dy;
      }
      function dp(first, last, out) {
        var max = sqTol, idx = -1;
        for (var i = first + 1; i < last; i++) { var d = segDist(points[i], points[first], points[last]); if (d > max) { idx = i; max = d; } }
        if (idx > -1) { if (idx - first > 1) dp(first, idx, out); out.push(points[idx]); if (last - idx > 1) dp(idx, last, out); }
      }
      var out = [points[0]]; dp(0, points.length - 1, out); out.push(points[points.length - 1]);
      return out.length >= 3 ? out.slice(0, 200) : points.slice(0, 200);
    }

    /* --- mobile map/list toggle --- */
    var toggle = $('[data-view-toggle]', app);
    toggle.addEventListener('click', function () {
      var on = app.classList.toggle('show-map');
      toggle.innerHTML = on ? '<span class="ico ico-list" aria-hidden="true"></span> <span>List</span>' : '<span class="ico ico-map" aria-hidden="true"></span> <span>Map</span>';
      setTimeout(function () { map.invalidateSize(); }, 50);
    });

    setForm();
    if (params.get('draw')) setTimeout(startDraw, 600);
    run();
  }

  /* ------------------------------------------------------------ home mini map */
  var home = $('#home-map');
  if (home) {
    var hm = baseMap(home, { center: HOUSTON, zoom: 10, scrollWheelZoom: false, zoomControl: false, attributionControl: true });
    var loaded = false;
    var load = function () {
      if (loaded) return; loaded = true;
      fetch('/api/search?per=12').then(function (r) { return r.json(); }).then(function (res) {
        var pts = [];
        var byId = {};
        res.items.forEach(function (c) { byId[c.id] = c; });
        res.markers.forEach(function (m, i) {
          setTimeout(function () {
            var mk = L.marker([m[1], m[2]], { icon: pinIcon(m[3], 'drop') }).addTo(hm);
            if (byId[m[0]]) mk.bindPopup(popupHTML(byId[m[0]]), { offset: [0, -28], closeButton: false });
          }, 120 * i);
          pts.push([m[1], m[2]]);
        });
        if (pts.length) hm.fitBounds(pts, { padding: [50, 50], maxZoom: 12 });
      });
    };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e, o) { if (e[0].isIntersecting) { load(); o.disconnect(); } }, { rootMargin: '200px' }).observe(home);
    else load();
  }

  /* ------------------------------------------------------------ property map */
  var pm = $('#prop-map');
  if (pm && pm.getAttribute('data-lat')) {
    var lat = +pm.getAttribute('data-lat'), lng = +pm.getAttribute('data-lng');
    var m2 = baseMap(pm, { center: [lat, lng], zoom: 14, scrollWheelZoom: false });
    L.marker([lat, lng], { icon: L.divIcon({ className: '', html: '<div class="home-pin"></div>', iconSize: [18, 18] }) }).addTo(m2)
      .bindTooltip(pm.getAttribute('data-name'), { direction: 'top', offset: [0, -10], permanent: true });
    L.circle([lat, lng], { radius: 1609, color: '#5b3fd6', weight: 1, fillOpacity: 0.05, dashArray: '4 6' }).addTo(m2);
  }
})();
