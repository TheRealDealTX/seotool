/* Live hurricane tracker map (Leaflet). Data is embedded by templates/hurricane-tracker.php from the NHC feed. */
(function () {
  'use strict';
  var app = document.querySelector('[data-tropics-app]');
  if (!app || !window.L) return;
  var storms = [];
  try { storms = JSON.parse(app.querySelector('[data-tropics]').textContent) || []; } catch (e) {}
  var home = [+app.getAttribute('data-lat'), +app.getAttribute('data-lon')];
  var el = app.querySelector('[data-map]');
  var map = L.map(el, { scrollWheelZoom: false, worldCopyJump: true }).setView([24, -82], 4);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 10, attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &middot; Storm data: NOAA NHC' }).addTo(map);
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  [800, 400, 200].forEach(function (mi, i) {
    L.circle(home, { radius: mi * 1609.34, color: '#34656D', weight: 1.5, dashArray: '6 6', fillColor: '#E9C46A', fillOpacity: 0.04 + i * 0.03 })
      .bindTooltip(mi + ' miles from Port Arthur').addTo(map);
  });
  L.circleMarker(home, { radius: 8, color: '#fff', weight: 2, fillColor: '#334443', fillOpacity: 1 }).bindPopup('<strong>Port Arthur, TX</strong>').addTo(map);
  var pts = [home];
  var colors = { HU: '#b42318', MH: '#7a0e0e', TS: '#d97706', STS: '#d97706', TD: '#2563eb', SD: '#2563eb', PTC: '#6b7280', PC: '#6b7280' };
  storms.forEach(function (s) {
    var icon = L.divIcon({ className: 'storm-pin', html: '<span class="storm-pin-dot" style="background:' + (colors[s.class] || '#6b3fa0') + '"></span><span class="storm-pin-label">' + esc(s.name) + '</span>', iconSize: [18, 18], iconAnchor: [9, 9] });
    L.marker([s.lat, s.lon], { icon: icon })
      .bindPopup('<strong>' + esc(s.label + ' ' + s.name) + '</strong><br>' + s.wind_mph + ' mph &middot; ' + (s.pressure || '—') + ' mb<br>' + Number(s.miles).toLocaleString() + ' mi ' + esc(s.bearing) + ' of Port Arthur' + (s.advisory ? '<br><a href="' + esc(s.advisory) + '" target="_blank" rel="noopener">NHC advisory</a>' : ''))
      .addTo(map);
    if (s.basin === 'al') pts.push([s.lat, s.lon]);
  });
  if (pts.length > 1) map.fitBounds(pts, { padding: [40, 40], maxZoom: 6 });
})();
