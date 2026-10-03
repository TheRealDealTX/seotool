/* Storm History filters + Storm Event Lookup. Data: /api/storms.php (NOAA NCEI + NWS LSR). */
(function () {
  'use strict';
  var app = document.querySelector('[data-storm-app]');
  if (!app) return;
  var mode = app.getAttribute('data-storm-app');
  var events = [];
  var map = null, layer = null;
  var famColor = { hail: '#3b82c4', wind: '#c89b48', tornado: '#b42318', flood: '#1d7a8a', tropical: '#6b3fa0', winter: '#5b7c99', other: '#536476' };
  var famLabel = { hail: 'Hail', wind: 'Wind', tornado: 'Tornado', flood: 'Flood & heavy rain', tropical: 'Tropical', winter: 'Freeze & winter', other: 'Other' };

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fmtDate(d) { var p = d.split('-'); var m = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][+p[1] - 1]; return m + ' ' + (+p[2]) + ', ' + p[0]; }
  function hailLabel(i) { var s = [[4.5, 'softball+'], [4, 'softball'], [2.75, 'baseball'], [2.5, 'tennis ball'], [2, 'hen egg'], [1.75, 'golf ball'], [1.5, 'ping pong ball'], [1.25, 'half dollar'], [1, 'quarter'], [0.88, 'nickel'], [0.75, 'penny'], [0.5, 'marble']]; for (var k = 0; k < s.length; k++) if (i >= s[k][0]) return s[k][1]; return 'pea'; }
  function severity(e) {
    if (e.hail_in) return (+e.hail_in).toFixed(2).replace(/0$/, '') + '" hail (' + hailLabel(+e.hail_in) + ')';
    if (e.wind_mph) return e.wind_mph + ' mph' + (e.mag_type ? ' ' + e.mag_type : ' wind');
    if (e.tor_scale) return e.tor_scale + ' tornado';
    return '—';
  }
  function srcLink(e) { return '<a href="' + esc(e.url) + '" target="_blank" rel="noopener">' + (e.src === 'NCEI' ? 'NCEI record' : 'NWS report') + '</a>'; }
  function miles(a, b, c, d) {
    var R = 3958.8, toR = Math.PI / 180;
    var dLat = (c - a) * toR, dLon = (d - b) * toR;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a * toR) * Math.cos(c * toR) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  }

  /* ---- Map ---- */
  function initMap() {
    var el = app.querySelector('[data-map]');
    if (!el || !window.L || map) return;
    map = L.map(el, { scrollWheelZoom: false }).setView([26.27, -98.2], 9);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 15, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }).addTo(map);
    layer = L.layerGroup().addTo(map);
  }
  function drawMap(list, center, radius) {
    if (!map) return;
    layer.clearLayers();
    var pts = [];
    list.forEach(function (e) {
      if (e.lat == null || e.lon == null) return;
      pts.push([e.lat, e.lon]);
      L.circleMarker([e.lat, e.lon], { radius: e.hail_in ? 4 + Math.min(8, e.hail_in * 2.5) : 6, color: '#fff', weight: 1, fillColor: famColor[e.fam] || '#536476', fillOpacity: 0.85 })
        .bindPopup('<strong>' + esc(e.type) + '</strong><br>' + fmtDate(e.date) + ' &middot; ' + esc(e.loc) + '<br>' + esc(severity(e)) + '<br>' + srcLink(e))
        .addTo(layer);
    });
    if (center) {
      L.circle(center, { radius: radius * 1609.34, color: '#10243a', weight: 2, fillOpacity: 0.05 }).addTo(layer);
      L.marker(center).addTo(layer);
      map.fitBounds(L.latLng(center).toBounds(radius * 1609.34 * 2.2));
    } else if (pts.length) {
      map.fitBounds(pts, { padding: [20, 20], maxZoom: 11 });
    }
  }

  /* ---- Load data ---- */
  function load() {
    return fetch(app.getAttribute('data-api'), { credentials: 'same-origin' })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (j) { events = j.events || []; return j; });
  }

  /* ================= Storm History ================= */
  function historyApp() {
    var form = app.querySelector('[data-filters]');
    var rowsEl = app.querySelector('[data-rows]');
    var pager = app.querySelector('[data-pager]');
    var countEl = app.querySelector('[data-count-label]');
    var chart = app.querySelector('[data-chart]');
    var chartLabels = app.querySelector('[data-chart-labels]');
    var tip = app.querySelector('[data-chart-tip]');
    var perPage = 25, page = 1, filtered = [];

    function readFilters() {
      var f = new FormData(form);
      return { fam: f.get('fam'), from: f.get('from'), to: f.get('to'), loc: (f.get('loc') || '').toLowerCase().trim(), wind: parseFloat(f.get('wind')) || 0, hail: parseFloat(f.get('hail')) || 0, q: (f.get('q') || '').toLowerCase().trim() };
    }
    function apply() {
      var f = readFilters();
      filtered = events.filter(function (e) {
        if (f.fam && e.fam !== f.fam) return false;
        if (f.from && e.date < f.from) return false;
        if (f.to && e.date > f.to) return false;
        if (f.loc && ((e.loc || '') + ' ' + (e.area || '')).toLowerCase().indexOf(f.loc) === -1) return false;
        if (f.wind && !(e.wind_mph >= f.wind)) return false;
        if (f.hail && !(e.hail_in >= f.hail)) return false;
        if (f.q && ((e.text || '') + ' ' + e.type).toLowerCase().indexOf(f.q) === -1) return false;
        return true;
      });
      page = 1;
      countEl.textContent = filtered.length.toLocaleString() + ' matching event' + (filtered.length === 1 ? '' : 's') + ' of ' + events.length.toLocaleString();
      renderRows(); renderChart(); drawMap(filtered);
    }
    function renderRows() {
      var start = (page - 1) * perPage;
      var slice = filtered.slice(start, start + perPage);
      rowsEl.innerHTML = slice.length ? slice.map(function (e) {
        var t = e.text || ''; var short = t.length > 260 ? t.slice(0, 257) + '…' : t;
        return '<tr><td>' + fmtDate(e.date) + '</td><td class="ev-type">' + esc(e.type) + '</td><td>' + esc(e.loc) + '</td><td>' + esc(severity(e)) + '</td><td class="ev-narr">' + esc(short) + '</td><td>' + srcLink(e) + '</td></tr>';
      }).join('') : '<tr><td colspan="6">No events match these filters. Try widening the date range or clearing a filter.</td></tr>';
      var pages = Math.ceil(filtered.length / perPage);
      if (pages <= 1) { pager.innerHTML = ''; return; }
      var html = '<button type="button" data-p="' + (page - 1) + '"' + (page === 1 ? ' disabled' : '') + '>&larr; Prev</button>';
      var lo = Math.max(1, page - 2), hi = Math.min(pages, lo + 4);
      for (var p = lo; p <= hi; p++) html += '<button type="button" data-p="' + p + '"' + (p === page ? ' aria-current="true"' : '') + '>' + p + '</button>';
      html += '<button type="button" data-p="' + (page + 1) + '"' + (page === pages ? ' disabled' : '') + '>Next &rarr;</button>';
      pager.innerHTML = html + '<span class="small muted" style="align-self:center">Page ' + page + ' of ' + pages + '</span>';
    }
    function renderChart() {
      if (!filtered.length) { chart.innerHTML = ''; chartLabels.innerHTML = ''; return; }
      var counts = {}, min = 9999, max = 0;
      filtered.forEach(function (e) { var y = +e.date.slice(0, 4); counts[y] = (counts[y] || 0) + 1; min = Math.min(min, y); max = Math.max(max, y); });
      var top = 0; for (var y in counts) top = Math.max(top, counts[y]);
      var html = '';
      for (var yr = min; yr <= max; yr++) {
        var c = counts[yr] || 0;
        html += '<button type="button" class="bar" data-year="' + yr + '" style="height:' + (c ? Math.max(4, (c / top) * 100) : 0) + '%" aria-label="' + yr + ': ' + c + ' events" title="' + yr + ': ' + c + '"></button>';
      }
      chart.innerHTML = html;
      chartLabels.innerHTML = '<span>' + min + '</span><span>' + max + '</span>';
    }
    pager.addEventListener('click', function (e) { var b = e.target.closest('button[data-p]'); if (!b || b.disabled) return; page = +b.getAttribute('data-p'); renderRows(); rowsEl.closest('.table-wrap').scrollIntoView({ block: 'start' }); });
    chart.addEventListener('mouseover', function (e) { var b = e.target.closest('.bar'); if (b) tip.textContent = b.getAttribute('aria-label') + ' — click to filter to this year'; });
    chart.addEventListener('focusin', function (e) { var b = e.target.closest('.bar'); if (b) tip.textContent = b.getAttribute('aria-label') + ' — press Enter to filter to this year'; });
    chart.addEventListener('click', function (e) {
      var b = e.target.closest('.bar'); if (!b) return;
      var y = b.getAttribute('data-year');
      form.elements.from.value = y + '-01-01'; form.elements.to.value = y + '-12-31'; apply();
    });
    var t;
    form.addEventListener('input', function () { clearTimeout(t); t = setTimeout(apply, 180); });
    form.addEventListener('reset', function () { setTimeout(apply, 0); });
    initMap();
    load().then(apply).catch(function () { countEl.textContent = 'Interactive filters are temporarily unavailable. The most recent significant events are listed below.'; });
  }

  /* ================= Storm Lookup ================= */
  function lookupApp() {
    var form = app.querySelector('[data-lookup]');
    var out = app.querySelector('[data-lookup-results]');
    var status = app.querySelector('[data-lookup-status]');
    var places = JSON.parse(app.querySelector('[data-places]').textContent);
    var ready = load().catch(function () { status.innerHTML = '<span class="notice notice-error" style="display:block">Storm data could not be loaded. Please try again later.</span>'; });
    initMap();
    function resolve(where) {
      var w = where.trim().toLowerCase();
      if (/^\d{5}$/.test(w)) { for (var i = 0; i < places.zips.length; i++) if (places.zips[i].zip === w) return { name: 'ZIP ' + w, lat: places.zips[i].lat, lon: places.zips[i].lon }; return null; }
      var norm = function (s) { return s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/, ?tx$/, '').trim(); };
      for (var k = 0; k < places.places.length; k++) if (norm(places.places[k].name) === norm(w)) return places.places[k];
      for (k = 0; k < places.places.length; k++) if (norm(places.places[k].name).indexOf(norm(w)) === 0) return places.places[k];
      return null;
    }
    function addDays(d, n) { var x = new Date(d + 'T12:00:00'); x.setDate(x.getDate() + n); return x.toISOString().slice(0, 10); }
    form.addEventListener('submit', function () {
      var f = new FormData(form);
      var loc = resolve(f.get('where') || '');
      if (!loc) { status.innerHTML = '<span class="notice notice-error" style="display:block">Please enter a Hidalgo County city (for example McAllen, Mission, Edinburg, Pharr) or a 5-digit ZIP code such as 78501.</span>'; return; }
      status.textContent = 'Searching…';
      ready.then(function () {
        var radius = +f.get('radius'), fam = f.get('fam'), date = f.get('date'), win = +f.get('window'), from = f.get('from'), to = f.get('to');
        if (date) { from = addDays(date, -win); to = addDays(date, win); }
        var res = events.filter(function (e) {
          if (fam && e.fam !== fam) return false;
          if (!fam && e.fam === 'other') return false;
          if (from && e.date < from) return false;
          if (to && e.date > to) return false;
          if (e.lat != null && e.lon != null) { e._d = miles(loc.lat, loc.lon, e.lat, e.lon); return e._d <= radius; }
          // County/zone-wide records have no point; include only when a date filter narrows them.
          e._d = null;
          return !!(from || to);
        });
        res.sort(function (a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : 0; });
        status.textContent = '';
        var head = '<p><strong>' + res.length + ' report' + (res.length === 1 ? '' : 's') + '</strong> within ' + radius + ' miles of ' + esc(loc.name) + (from || to ? ' between ' + (from ? fmtDate(from) : 'the start of records') + ' and ' + (to ? fmtDate(to) : 'today') : ' (all dates)') + '.</p>';
        if (!res.length) {
          out.innerHTML = head + '<p>No matching reports. Storms are not always reported where they occur, so this does not mean no storm affected the area. Try a larger radius or wider date window, or check <a href="/weather-events/">recent weather events</a>.</p>';
        } else {
          out.innerHTML = head + '<div class="table-wrap"><table><thead><tr><th>Date</th><th>Event</th><th>Location</th><th>Distance</th><th>Source</th></tr></thead><tbody>' + res.slice(0, 150).map(function (e) {
            return '<tr><td>' + fmtDate(e.date) + (e.time ? '<br><span class="small muted">' + esc(e.time) + '</span>' : '') + '</td><td><strong>' + esc(e.type) + '</strong><br><span class="small">' + esc(severity(e)) + '</span></td><td>' + esc(e.loc) + (e.text ? '<br><span class="small muted">' + esc(e.text.slice(0, 160)) + (e.text.length > 160 ? '…' : '') + '</span>' : '') + '</td><td>' + (e._d == null ? 'County/zone-wide' : e._d.toFixed(1) + ' mi') + '</td><td>' + srcLink(e) + (e.src !== 'NCEI' ? '<br><span class="small muted">Preliminary</span>' : '') + '</td></tr>';
          }).join('') + '</tbody></table></div>' + (res.length > 150 ? '<p class="small muted">Showing the 150 most recent matches. Narrow the dates to see more.</p>' : '') +
          '<div class="callout callout-gold"><span class="callout-title">How to use these results</span><ul><li>Save or print the official record for any event that matches your date of loss.</li><li>Photograph damage before repairs and keep dated photos with the weather record.</li><li>Use the <a href="/claim-documentation-checklist/">documentation checklist</a> to organize your claim file.</li><li>Remember: a nearby report supports, but does not prove, damage at your property.</li></ul></div>';
        }
        drawMap(res, [loc.lat, loc.lon], radius);
      });
    });
  }

  if (mode === 'history') historyApp(); else lookupApp();
})();
