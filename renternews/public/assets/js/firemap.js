/* Renter News — incident map (Leaflet + CARTO tiles) */
(function () {
  "use strict";
  var el = document.getElementById("fire-map"), data = JSON.parse(document.getElementById("map-data").textContent);
  if (!el || !window.L) return;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var root = document.documentElement;
  var dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  var map = L.map(el, { scrollWheelZoom: false, worldCopyJump: true }).setView([38.5, -96], 4);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors', maxZoom: 18
  }).addTo(map);
  if (dark) el.classList.add("is-dark");
  map.on("focus click", function () { map.scrollWheelZoom.enable(); });

  // Spread markers that share a city so each is clickable.
  var seen = {};
  var markers = data.map(function (p) {
    var k = p.lat + "," + p.lon, n = seen[k] = (seen[k] || 0) + 1, off = (n - 1) * 0.06;
    var icon = L.divIcon({ className: "", html: '<div class="map-pin" style="--c:' + p.col + '"></div>', iconSize: [18, 18], iconAnchor: [9, 9] });
    var m = L.marker([p.lat + off * Math.sin(n), p.lon + off * Math.cos(n)], { icon: icon, title: p.t });
    m.bindPopup('<img src="' + p.img + '" alt="">' + '<a href="' + p.u + '">' + esc(p.t) + "</a><br><small>" + esc(p.city) + " · " + p.d + " · " + p.n + "</small>");
    m.p = p; return m;
  });
  var layer = L.featureGroup().addTo(map), fc = "all", fy = "all";
  var list = document.querySelector("[data-map-list]"), count = document.querySelector("[data-map-count]");
  function draw() {
    layer.clearLayers();
    var shown = markers.filter(function (m) { return (fc === "all" || m.p.c === fc) && (fy === "all" || String(m.p.y) === fy); });
    shown.forEach(function (m) { layer.addLayer(m); });
    count.textContent = shown.length + (shown.length === 1 ? " incident" : " incidents") + " shown";
    list.innerHTML = shown.map(function (m, i) {
      return '<button type="button" class="map-item" data-i="' + markers.indexOf(m) + '"><i style="--c:' + m.p.col + '"></i><span><strong>' + esc(m.p.t) + "</strong><small>" + esc(m.p.city) + " · " + m.p.d + "</small></span></button>";
    }).join("");
    if (shown.length) map.fitBounds(layer.getBounds(), { padding: [30, 30], maxZoom: 9 });
  }
  list.addEventListener("click", function (e) {
    var b = e.target.closest("[data-i]"); if (!b) return;
    var m = markers[+b.dataset.i]; map.setView(m.getLatLng(), 11); m.openPopup();
    el.scrollIntoView({ behavior: "smooth", block: "center" });
  });
  document.querySelectorAll("[data-mf]").forEach(function (b) {
    b.addEventListener("click", function () { fc = b.dataset.mf; document.querySelectorAll("[data-mf]").forEach(function (x) { x.classList.toggle("is-on", x === b); }); draw(); });
  });
  document.querySelectorAll("[data-my]").forEach(function (b) {
    b.addEventListener("click", function () { fy = b.dataset.my; document.querySelectorAll("[data-my]").forEach(function (x) { x.classList.toggle("is-on", x === b); }); draw(); });
  });
  draw();
})();
