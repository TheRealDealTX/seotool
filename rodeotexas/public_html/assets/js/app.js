/* Rodeo Texas — progressive enhancement. The site works without JavaScript;
   this adds the mobile menu, favorites, sharing, auto-filtering and maps. */
(function () {
  'use strict';
  var FAV_KEY = 'rodeotexas:favorites';
  var LEAFLET = {
    css: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css',
    cssSri: 'sha384-c6Rcwz4e4CITMbu/NBmnNS8yN2sC3cUElMEMfP3vqqKFp7GOYaaBBCqmaWBjmkjb',
    js: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js',
    jsSri: 'sha384-NElt3Op+9NBMCYaef5HxeJmU4Xeard/Lku8ek6hoPTvYkQPh3zLIrJP7KiRocsxO'
  };

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]; }); }

  /* ---------- mobile navigation */
  var toggle = $('.nav-toggle'), nav = $('#site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) { nav.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
    });
  }

  /* ---------- favorites (localStorage; nothing is sent to the server) */
  function readFavs() {
    try { var v = JSON.parse(localStorage.getItem(FAV_KEY) || '[]'); return Array.isArray(v) ? v : []; } catch (e) { return []; }
  }
  function writeFavs(list) {
    try { localStorage.setItem(FAV_KEY, JSON.stringify(list)); } catch (e) { /* private mode */ }
    syncFavUi();
  }
  function isFav(slug) { return readFavs().some(function (f) { return f.slug === slug; }); }
  function syncFavUi() {
    var favs = readFavs();
    $all('[data-fav-count]').forEach(function (el) { el.textContent = favs.length; el.hidden = favs.length === 0; });
    $all('[data-fav]').forEach(function (btn) {
      var on = favs.some(function (f) { return f.slug === btn.getAttribute('data-fav'); });
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      var label = btn.querySelector('[data-fav-label]');
      if (label) { label.textContent = on ? 'Saved' : 'Save'; }
    });
  }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-fav]');
    if (!btn) { return; }
    e.preventDefault();
    var slug = btn.getAttribute('data-fav');
    var favs = readFavs();
    if (isFav(slug)) {
      favs = favs.filter(function (f) { return f.slug !== slug; });
      announce('Removed from favorites');
    } else {
      favs.push({ slug: slug, title: btn.getAttribute('data-title') || '', date: btn.getAttribute('data-date') || '' });
      announce('Saved to favorites');
    }
    writeFavs(favs);
  });
  var live = document.createElement('div');
  live.className = 'visually-hidden'; live.setAttribute('aria-live', 'polite');
  document.body.appendChild(live);
  function announce(msg) { live.textContent = ''; setTimeout(function () { live.textContent = msg; }, 50); }
  syncFavUi();

  var favBox = $('[data-favorites]');
  if (favBox) {
    var favs = readFavs(), empty = $('#favorites-empty'), clear = $('[data-fav-clear]');
    if (!favs.length) { empty.hidden = false; }
    else {
      clear.hidden = false;
      fetch('/api/events.json?slugs=' + encodeURIComponent(favs.map(function (f) { return f.slug; }).join(',')))
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var found = {};
          favBox.innerHTML = data.events.map(function (ev) { found[ev.slug] = 1; return cardHtml(ev); }).join('');
          favs.filter(function (f) { return !found[f.slug]; }).forEach(function (f) {
            favBox.insertAdjacentHTML('beforeend', '<p class="notice">“' + esc(f.title) + '” is no longer listed. <button type="button" class="btn btn--ghost" data-fav="' + esc(f.slug) + '">Remove</button></p>');
          });
          syncFavUi();
        })
        .catch(function () { favBox.innerHTML = '<p class="notice">Could not load your favorites. Please try again.</p>'; });
      clear.addEventListener('click', function () { writeFavs([]); favBox.innerHTML = ''; empty.hidden = false; clear.hidden = true; });
    }
  }
  function cardHtml(ev) {
    var d = new Date(ev.start_date + 'T12:00:00');
    var mon = d.toLocaleString('en-US', { month: 'short' });
    return '<article class="event-card event-card--compact"><div class="date-block" aria-hidden="true"><span class="date-block__m">' + esc(mon) + '</span><span class="date-block__d">' + d.getDate() + '</span><span class="date-block__y">' + d.getFullYear() + '</span></div>' +
      '<div class="event-card__body"><h3 class="event-card__title"><a href="' + esc(ev.url) + '">' + esc(ev.title) + '</a></h3>' +
      '<p class="event-card__meta">' + esc(ev.dates) + '</p><p class="event-card__place">' + esc(ev.place) + '</p>' +
      '<div class="event-card__tags"><span class="badge badge--' + esc(ev.status) + '">' + esc(ev.status_label) + '</span>' + (ev.association ? '<span class="tag tag--assoc">' + esc(ev.association) + '</span>' : '') + '</div></div>' +
      '<button type="button" class="fav-btn" data-fav="' + esc(ev.slug) + '" data-title="' + esc(ev.title) + '" data-date="' + esc(ev.start_date) + '" aria-pressed="false" aria-label="Save ' + esc(ev.title) + ' to favorites"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z"/></svg></button></article>';
  }

  /* ---------- share */
  $all('[data-share]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.getAttribute('data-share-url'), title = btn.getAttribute('data-share-title');
      if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); return; }
      if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(function () { btn.textContent = 'Link copied'; announce('Link copied to clipboard'); setTimeout(function () { btn.textContent = 'Share'; }, 2500); });
      } else { window.prompt('Copy this link:', url); }
    });
  });

  /* ---------- filters: apply select changes immediately */
  var form = $('form[data-autosubmit]');
  if (form) {
    $all('select, input[type="date"]', form).forEach(function (el) {
      el.addEventListener('change', function () {
        $all('input, select', form).forEach(function (f) { if (!f.value) { f.disabled = true; } });   // keep URLs short
        form.submit();
      });
    });
  }

  /* ---------- maps (Leaflet + OpenStreetMap tiles, loaded only when needed) */
  var leafletPromise = null;
  function loadLeaflet() {
    if (window.L) { return Promise.resolve(window.L); }
    if (leafletPromise) { return leafletPromise; }
    leafletPromise = new Promise(function (resolve, reject) {
      var l = document.createElement('link');
      l.rel = 'stylesheet'; l.href = LEAFLET.css; l.integrity = LEAFLET.cssSri; l.crossOrigin = 'anonymous';
      document.head.appendChild(l);
      var s = document.createElement('script');
      s.src = LEAFLET.js; s.integrity = LEAFLET.jsSri; s.crossOrigin = 'anonymous';
      s.onload = function () { resolve(window.L); };
      s.onerror = reject;
      document.head.appendChild(s);
    });
    return leafletPromise;
  }
  function baseMap(el, L) {
    var map = L.map(el, { scrollWheelZoom: false });
    L.tileLayer(el.getAttribute('data-tiles'), { maxZoom: 18, attribution: el.getAttribute('data-attribution') }).addTo(map);
    return map;
  }
  function marker(L, ev) {
    return L.circleMarker([ev.lat, ev.lng], {
      radius: 8, weight: 3, color: ev.status === 'canceled' ? '#9b1c1c' : '#7a3b1b',
      fillColor: ev.precise ? '#b0431b' : '#ffffff', fillOpacity: ev.precise ? 0.9 : 1
    });
  }

  var mapEl = $('#event-map');
  if (mapEl) {
    Promise.all([loadLeaflet(), fetch(mapEl.getAttribute('data-map-endpoint')).then(function (r) { return r.json(); })])
      .then(function (res) {
        var L = res[0], data = res[1];
        mapEl.innerHTML = '';
        var map = baseMap(mapEl, L);
        var bounds = [];
        var groups = {};
        data.events.forEach(function (ev) {
          if (ev.lat == null) { return; }
          var k = ev.lat.toFixed(4) + ',' + ev.lng.toFixed(4);
          (groups[k] = groups[k] || []).push(ev);
        });
        Object.keys(groups).forEach(function (k) {
          var evs = groups[k], ev = evs[0];
          var html = '<strong>' + esc(ev.place) + '</strong><ul style="padding-left:1rem;margin:.3rem 0">' + evs.map(function (x) {
            return '<li><a href="' + esc(x.url) + '">' + esc(x.title) + '</a><br>' + esc(x.dates) + (x.status === 'canceled' ? ' — Canceled' : '') + '</li>';
          }).join('') + '</ul>' + (ev.precise ? '' : '<em>City location (approximate)</em>');
          marker(L, ev).bindPopup(html).addTo(map);
          bounds.push([ev.lat, ev.lng]);
        });
        if (bounds.length) { map.fitBounds(bounds, { padding: [30, 30], maxZoom: 11 }); }
        else { map.setView([31.3, -99.3], 6); }
        var list = $('#map-list');
        if (list) {
          list.innerHTML = '<p class="result-count">' + data.count + ' event' + (data.count === 1 ? '' : 's') + ' on the map</p>' + data.events.map(cardHtml).join('');
          syncFavUi();
        }
      })
      .catch(function () { mapEl.innerHTML = '<p class="map-fallback">The map could not be loaded. Please use the list view.</p>'; });
  }

  var mini = $('[data-mini-map]');
  if (mini && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting) { return; }
      io.disconnect();
      loadLeaflet().then(function (L) {
        var lat = parseFloat(mini.getAttribute('data-lat')), lng = parseFloat(mini.getAttribute('data-lng'));
        var precise = mini.getAttribute('data-precise') === '1';
        var map = baseMap(mini, L);
        map.setView([lat, lng], precise ? 14 : 11);
        marker(L, { lat: lat, lng: lng, precise: precise }).bindPopup(esc(mini.getAttribute('data-label'))).addTo(map);
      }).catch(function () { mini.hidden = true; });
    }, { rootMargin: '200px' });
    io.observe(mini);
  }
})();
