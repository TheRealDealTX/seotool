/* Corpus Christi weather app: animated NEXRAD radar loop (Iowa Environmental Mesonet tiles on Leaflet). */
(function () {
  'use strict';
  var el = document.getElementById('wx-radar');
  if (!el || !window.L) return;
  var lat = parseFloat(el.getAttribute('data-lat')), lon = parseFloat(el.getAttribute('data-lon'));
  var map = L.map(el, { scrollWheelZoom: false, zoomControl: true, attributionControl: true }).setView([lat, lon], 8);
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 12, subdomains: 'abcd',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
  }).addTo(map);
  L.circleMarker([lat, lon], { radius: 6, color: '#ffbc7d', weight: 3, fillColor: '#0a1120', fillOpacity: 1 }).addTo(map).bindTooltip('Corpus Christi');

  // Frames: 50 minutes ago -> now, in 5-minute steps.
  var offsets = [50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0];
  var stamp = Math.floor(Date.now() / 300000); // bust tile caches every 5 minutes
  var layers = offsets.map(function (m) {
    var name = 'nexrad-n0q-900913' + (m ? '-m' + (m < 10 ? '0' : '') + m + 'm' : '');
    return L.tileLayer('https://mesonet.agron.iastate.edu/cache/tile.py/1.0.0/' + name + '/{z}/{x}/{y}.png?_=' + stamp, {
      opacity: 0, maxZoom: 12, attribution: 'NEXRAD via <a href="https://mesonet.agron.iastate.edu/">IEM</a>'
    }).addTo(map);
  });
  var slider = document.querySelector('[data-radar-slider]');
  var label = document.querySelector('[data-radar-time]');
  var btn = document.querySelector('[data-radar-play]');
  var idx = offsets.length - 1, timer = null;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(i) {
    layers.forEach(function (l, j) { l.setOpacity(j === i ? 0.75 : 0); });
    idx = i;
    if (slider) slider.value = String(i);
    var t = new Date(Math.floor(Date.now() / 300000) * 300000 - offsets[i] * 60000);
    if (label) label.textContent = (offsets[i] ? offsets[i] + ' min ago · ' : 'Latest · ') + t.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  }
  var pauseIcon = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>';
  var playIcon = '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M7 5v14l12-7z"/></svg>';
  function play() {
    stop();
    timer = setInterval(function () { show(idx >= offsets.length - 1 ? 0 : idx + 1); }, 650);
    if (btn) { btn.innerHTML = pauseIcon; btn.setAttribute('aria-label', 'Pause radar animation'); }
  }
  function stop() {
    if (timer) clearInterval(timer);
    timer = null;
    if (btn) { btn.innerHTML = playIcon; btn.setAttribute('aria-label', 'Play radar animation'); }
  }
  if (slider) slider.addEventListener('input', function () { stop(); show(parseInt(slider.value, 10)); });
  if (btn) btn.addEventListener('click', function () { if (timer) stop(); else play(); });
  show(idx);
  // Start the loop only when the map is on screen.
  if (!reduce && 'IntersectionObserver' in window) {
    var started = false;
    new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting && !started) { started = true; play(); } });
    }).observe(el);
  } else { stop(); }
})();
