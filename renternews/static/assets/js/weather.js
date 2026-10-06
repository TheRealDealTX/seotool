/* Renter News — live weather page (National Weather Service, api.weather.gov) */
(function () {
  "use strict";
  var app = document.querySelector("[data-weather-app]");
  if (!app || !window.RNWX) return;
  var W = window.RNWX;
  function $(s) { return app.querySelector(s); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var place = W.getPlace(), unit = W.getUnit(), timer, model;
  var QUICK = [
    ["New York", "NY", 40.7143, -74.006], ["Los Angeles", "CA", 34.0522, -118.2437], ["Chicago", "IL", 41.85, -87.65],
    ["Houston", "TX", 29.7633, -95.3633], ["Phoenix", "AZ", 33.4484, -112.074], ["Philadelphia", "PA", 39.9524, -75.1636],
    ["San Antonio", "TX", 29.4241, -98.4936], ["Dallas", "TX", 32.7831, -96.8067], ["Miami", "FL", 25.7743, -80.1937],
    ["Atlanta", "GA", 33.749, -84.388], ["Seattle", "WA", 47.6062, -122.3321], ["Denver", "CO", 39.7392, -104.9847]
  ];
  $("[data-wx-quick]").innerHTML = QUICK.map(function (q, i) { return '<button type="button" data-q="' + i + '">' + q[0] + "</button>"; }).join("");
  $("[data-wx-quick]").addEventListener("click", function (e) {
    var b = e.target.closest("[data-q]"); if (!b) return;
    var q = QUICK[+b.dataset.q]; choose({ name: q[0], admin: q[1], lat: q[2], lon: q[3] });
  });

  /* Units */
  app.querySelectorAll("[data-unit]").forEach(function (b) {
    b.classList.toggle("is-on", b.dataset.unit === unit);
    b.addEventListener("click", function () {
      unit = b.dataset.unit; W.setUnit(unit);
      app.querySelectorAll("[data-unit]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      if (model) render(model);
    });
  });

  /* Offline US city + ZIP search (GeoNames lists in /assets/data/) */
  var input = $("[data-wx-input]"), sug = $("[data-wx-suggest]"), results = [], active = -1, cities, zipFiles = {};
  function norm(s) { return s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[^a-z0-9 ]/g, "").replace(/^saint /, "st "); }
  function loadCities() { return cities ? Promise.resolve(cities) : fetch("/assets/data/us-cities.json").then(function (r) { return r.json(); }).then(function (d) { cities = d.map(function (c) { c.push(norm(c[0])); return c; }); return cities; }); }
  function loadZips(d) { return zipFiles[d] || (zipFiles[d] = fetch("/assets/data/zips-" + d + ".json").then(function (r) { return r.json(); })); }
  input.addEventListener("focus", loadCities, { once: true });
  input.addEventListener("input", function () {
    var q = input.value.trim();
    if (q.length < 2) { sug.classList.remove("is-open"); return; }
    var p;
    if (/^\d{3,5}$/.test(q)) {
      p = loadZips(q[0]).then(function (z) {
        return z.filter(function (r) { return r[0].indexOf(q) === 0; }).slice(0, 8).map(function (r) { return { name: r[1], admin: r[2], lat: r[3], lon: r[4], label: r[0] + " · " + r[1] + ", " + r[2] }; });
      });
    } else {
      var parts = q.split(","), nq = norm(parts[0].trim()), st = (parts[1] || "").trim().toUpperCase();
      p = loadCities().then(function (cs) {
        var out = [];
        for (var i = 0; i < cs.length && out.length < 8; i++) {
          var c = cs[i];
          if (c[5].indexOf(nq) === 0 && (!st || c[1].indexOf(st) === 0)) out.push(c);
        }
        if (out.length < 8) for (var j = 0; j < cs.length && out.length < 8; j++) {
          if (cs[j][5].indexOf(" " + nq) > 0 && out.indexOf(cs[j]) < 0 && (!st || cs[j][1].indexOf(st) === 0)) out.push(cs[j]);
        }
        return out.map(function (c) { return { name: c[0], admin: c[1], lat: c[2], lon: c[3], label: c[0] + ", " + c[1] }; });
      });
    }
    p.then(function (rs) {
      if (input.value.trim() !== q) return;
      results = rs; active = -1;
      sug.innerHTML = rs.length ? rs.map(function (r, i) { return '<li role="option" data-i="' + i + '">' + esc(r.label) + "</li>"; }).join("") : "<li>No US matches. Try a city name or ZIP code.</li>";
      sug.classList.add("is-open");
    }).catch(function () {});
  });
  input.addEventListener("keydown", function (e) {
    var items = sug.querySelectorAll("[data-i]");
    if ((e.key === "ArrowDown" || e.key === "ArrowUp") && items.length) {
      e.preventDefault(); active = (active + (e.key === "ArrowDown" ? 1 : -1) + items.length) % items.length;
      items.forEach(function (li, i) { li.setAttribute("aria-selected", i === active); });
    } else if (e.key === "Escape") sug.classList.remove("is-open");
  });
  sug.addEventListener("click", function (e) { var li = e.target.closest("[data-i]"); if (li) pick(+li.dataset.i); });
  $("[data-wx-search]").addEventListener("submit", function (e) { e.preventDefault(); if (results.length) pick(active >= 0 ? active : 0); });
  document.addEventListener("click", function (e) { if (!e.target.closest("[data-wx-search]")) sug.classList.remove("is-open"); });
  function pick(i) {
    var r = results[i]; if (!r) return;
    sug.classList.remove("is-open"); input.value = "";
    choose({ name: r.name, admin: r.admin, lat: r.lat, lon: r.lon });
  }

  /* Geolocation: name comes from the NWS points lookup */
  $("[data-wx-locate]").addEventListener("click", function () {
    if (!navigator.geolocation) return;
    var btn = this; btn.textContent = "Locating…";
    navigator.geolocation.getCurrentPosition(function (pos) {
      btn.textContent = "Use my location";
      var p = { name: "My location", admin: "", lat: +pos.coords.latitude.toFixed(4), lon: +pos.coords.longitude.toFixed(4) };
      W.points(p).then(function (pt) { if (pt.city) { p.name = pt.city; p.admin = pt.state; } choose(p); })
        .catch(function () { showError("The National Weather Service only covers the United States and its territories."); });
    }, function () { btn.textContent = "Location blocked"; setTimeout(function () { btn.textContent = "Use my location"; }, 2500); }, { timeout: 10000 });
  });

  function choose(p) { place = p; W.setPlace(p); load(true); window.scrollTo({ top: app.offsetTop - 120, behavior: "smooth" }); }

  /* Helpers */
  var T = function (f) { return W.temp(f, unit); };
  function speed(mph) { return mph == null ? "–" : unit === "c" ? Math.round(mph * 1.609) + " km/h" : Math.round(mph) + " mph"; }
  function fmtTime(d, opts) { try { return new Date(d).toLocaleTimeString("en-US", Object.assign({ timeZone: model.tz }, opts || { hour: "numeric", minute: "2-digit" })); } catch (e) { return new Date(d).toLocaleTimeString("en-US", opts); } }
  function compass(deg) { return deg == null ? "" : ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][Math.round(deg / 45) % 8]; }
  // NOAA sunrise equation (accurate to a minute or two)
  function sun(lat, lon, date, rise) {
    var rad = Math.PI / 180, start = Date.UTC(date.getUTCFullYear(), 0, 0), N = Math.floor((date - start) / 864e5);
    var lngHour = lon / 15, t = N + ((rise ? 6 : 18) - lngHour) / 24, M = 0.9856 * t - 3.289;
    var L = (M + 1.916 * Math.sin(M * rad) + 0.02 * Math.sin(2 * M * rad) + 282.634 + 360) % 360;
    var RA = (Math.atan(0.91764 * Math.tan(L * rad)) / rad + 360) % 360;
    RA = (RA + Math.floor(L / 90) * 90 - Math.floor(RA / 90) * 90) / 15;
    var sinDec = 0.39782 * Math.sin(L * rad), cosDec = Math.cos(Math.asin(sinDec));
    var cosH = (Math.cos(90.833 * rad) - sinDec * Math.sin(lat * rad)) / (cosDec * Math.cos(lat * rad));
    if (cosH > 1 || cosH < -1) return null;
    var H = (rise ? 360 - Math.acos(cosH) / rad : Math.acos(cosH) / rad) / 15;
    var UT = ((H + RA - 0.06571 * t - 6.622 - lngHour) % 24 + 24) % 24;
    var d = new Date(Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate()));
    return new Date(d.getTime() + UT * 3600e3);
  }

  function fx(mood) {
    var h = "";
    if (mood === "rain" || mood === "storm") for (var i = 0; i < 60; i++) h += '<i style="left:' + Math.random() * 110 + "%;animation-duration:" + (0.5 + Math.random() * 0.5) + "s;animation-delay:" + (-Math.random() * 2) + 's"></i>';
    else if (mood === "snow") for (var j = 0; j < 50; j++) h += '<i style="left:' + Math.random() * 100 + "%;animation-duration:" + (4 + Math.random() * 5) + "s;animation-delay:" + (-Math.random() * 8) + 's"></i>';
    else if (mood === "night") for (var k = 0; k < 40; k++) h += '<i style="left:' + Math.random() * 100 + "%;top:" + Math.random() * 100 + "%;animation-delay:" + (-Math.random() * 3) + 's"></i>';
    else if (mood === "clear") h = '<span class="orb"></span>';
    return '<div class="wx-fx ' + (mood === "snow" ? "snow" : mood === "night" ? "stars" : "") + '">' + h + "</div>";
  }
  function det(k, v, s) { return '<div class="wx-detail"><small>' + k + "</small><b>" + v + "</b><span>" + s + "</span></div>"; }
  function showError(msg) { $("[data-wx-hero]").innerHTML = "<p>" + esc(msg) + "</p>"; }

  function render(d) {
    model = d;
    var c = d.now, inf = W.info(c.icon, c.text), today = d.daily[0] || {};
    var hi = today.hi != null ? today.hi : Math.max.apply(null, d.hourly.slice(0, 12).map(function (h) { return h.temp; }));
    var lo = today.lo != null ? today.lo : Math.min.apply(null, d.hourly.slice(0, 24).map(function (h) { return h.temp; }));
    var hero = $("[data-wx-hero]");
    hero.dataset.mood = inf.mood;
    hero.innerHTML = fx(inf.mood) + '<div class="wxh-grid"><div>' +
      '<div class="wxh-place"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>' + esc(place.name) + (place.admin ? ", " + esc(place.admin) : "") + "</div>" +
      '<div class="wxh-main">' + W.icon(inf.kind) + '<div class="wxh-temp">' + T(c.temp) + "</div></div>" +
      '<div class="wxh-desc">' + esc(inf.text) + "</div>" +
      '<div class="wxh-sub">Feels like ' + T(c.feels) + " · High " + T(hi) + " · Low " + T(lo) + "</div>" +
      '<div class="wxh-sub">' + (c.station ? "Observed at " + esc(c.station) + ", " : "Forecast for ") + fmtTime(c.time) + " local time</div></div>" +
      '<div class="wxh-stats">' +
      "<div><small>Wind</small><b>" + speed(c.wind) + "</b> " + (compass(c.dirDeg) || esc(c.dir || "")) + "</div>" +
      "<div><small>Humidity</small><b>" + (c.hum != null ? Math.round(c.hum) + "%" : "–") + "</b></div>" +
      "<div><small>Rain chance</small><b>" + (d.hourly[0].pop || 0) + "%</b> next hour</div>" +
      "<div><small>Today</small><b>" + (today.pop || 0) + "%</b> rain chance</div>" +
      "</div></div>" + (today.detail ? '<p class="wxh-detail">' + esc(today.name) + ": " + esc(today.detail) + "</p>" : "");

    /* Hourly SVG chart */
    var hrs = d.hourly.slice(0, 24), temps = hrs.map(function (h) { return h.temp; });
    var mn = Math.min.apply(null, temps), mx = Math.max.apply(null, temps), Wd = 960, Hd = 200, pad = 30;
    var x = function (k) { return pad + k * (Wd - pad * 2) / (hrs.length - 1); };
    var y = function (t) { return 60 + (mx - t) / Math.max(mx - mn, 1) * 70; };
    var line = hrs.map(function (_, k) { return (k ? "L" : "M") + x(k).toFixed(1) + " " + y(temps[k]).toFixed(1); }).join(" ");
    var svg = '<svg viewBox="0 0 ' + Wd + " " + Hd + '" role="img" aria-label="Temperature over the next 24 hours"><defs><linearGradient id="hlg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#2f7fd0" stop-opacity=".35"/><stop offset="1" stop-color="#2f7fd0" stop-opacity="0"/></linearGradient></defs>' +
      '<path class="hl-area" d="' + line + " L" + x(hrs.length - 1) + " 150 L" + x(0) + ' 150 Z"/><path class="hl-line" d="' + line + '"/>';
    hrs.forEach(function (h, k) {
      if (k % 2) return;
      var ic = W.icon(W.info(h.icon).kind).replace(/^<svg[^>]*>/, "").replace("</svg>", "");
      svg += '<text class="hl-t" x="' + x(k) + '" y="' + (y(temps[k]) - 12) + '" text-anchor="middle">' + T(temps[k]) + "</text>" +
        '<circle cx="' + x(k) + '" cy="' + y(temps[k]) + '" r="3.5" fill="#2f7fd0"/>' +
        '<g transform="translate(' + (x(k) - 12) + ' 152) scale(.375)">' + ic + "</g>" +
        '<text x="' + x(k) + '" y="194" text-anchor="middle">' + (k ? fmtTime(h.t, { hour: "numeric" }) : "Now") + "</text>" +
        (h.pop ? '<text class="hl-p" x="' + x(k) + '" y="' + (y(temps[k]) + 22) + '" text-anchor="middle">' + h.pop + "%</text>" : "");
    });
    $("[data-wx-hourly]").innerHTML = svg + "</svg>";

    /* Daily */
    var all = [];
    d.daily.forEach(function (x_) { if (x_.hi != null) all.push(x_.hi); if (x_.lo != null) all.push(x_.lo); });
    var dmin = Math.min.apply(null, all), dmax = Math.max.apply(null, all), span = Math.max(dmax - dmin, 1);
    $("[data-wx-daily]").innerHTML = d.daily.map(function (x_) {
      var di = W.info(x_.icon, x_.text), l = x_.lo != null ? x_.lo : x_.hi, h = x_.hi != null ? x_.hi : x_.lo;
      return '<div class="wx-day" title="' + esc(x_.detail) + '"><div><b>' + esc(x_.name.replace(/ Night$/, "")) + "</b><small>" + new Date(x_.date).toLocaleDateString("en-US", { month: "short", day: "numeric" }) + "</small></div>" +
        W.icon(di.kind) + "<div>" + esc(x_.text) + "<small>" + (x_.pop || 0) + "% rain · wind " + esc(unit === "c" ? x_.wind.replace(/(\d+)/g, function (m) { return Math.round(m * 1.609); }).replace("mph", "km/h") : x_.wind) + "</small></div>" +
        '<div class="wx-range"><span>' + T(x_.lo) + '</span><div class="wx-range-track"><i style="left:' + ((l - dmin) / span * 100) + "%;right:" + ((dmax - h) / span * 100) + '%"></i></div><span>' + T(x_.hi) + "</span></div></div>";
    }).join("");

    /* Details */
    var now = new Date(), rise = sun(place.lat, place.lon, now, true), set = sun(place.lat, place.lon, now, false);
    var vis = c.vis == null ? "–" : unit === "c" ? (c.vis * 1.609).toFixed(0) + " km" : c.vis.toFixed(c.vis < 10 ? 1 : 0) + " mi";
    $("[data-wx-details]").innerHTML =
      det("Sunrise", rise ? fmtTime(rise) : "–", "Sunset " + (set ? fmtTime(set) : "–")) +
      det("Wind gusts", c.gust ? speed(c.gust) : "None reported", c.dirDeg != null ? "From the " + compass(c.dirDeg) : "Wind " + esc(c.dir || "")) +
      det("Dew point", T(c.dew), c.dew > 65 ? "Muggy" : c.dew > 55 ? "Slightly humid" : "Comfortable") +
      det("Pressure", c.pressure ? Math.round(c.pressure) + " hPa" : "–", "Station reading") +
      det("Visibility", vis, c.station ? esc(c.station) : "") +
      det("Tonight", T(today.lo), esc((today.nightDetail || "").split(".")[0] || "Overnight low"));
    tips(d, inf, hi, lo);
  }

  function loadAlerts() {
    var box = $("[data-wx-alerts]"); box.innerHTML = "";
    W.getJSON("https://api.weather.gov/alerts/active?point=" + (+place.lat).toFixed(4) + "," + (+place.lon).toFixed(4))
      .then(function (d) {
        box.innerHTML = (d.features || []).slice(0, 4).map(function (f) {
          var p = f.properties;
          return '<details class="wx-alert"><summary>⚠ ' + esc(p.event) + " — " + esc(p.headline || "") + "</summary><p>" + esc((p.description || "").slice(0, 1200)) + (p.instruction ? "\n\n" + esc(p.instruction.slice(0, 600)) : "") + "</p></details>";
        }).join("");
      }).catch(function () {});
  }

  function tips(d, inf, hi, lo) {
    var t = [];
    if (hi >= 90) t.push("Heat today: keep blinds closed in the afternoon, check on older neighbors, and report a broken air conditioner to your landlord in writing if your lease or local code requires cooling.");
    if (lo <= 32) t.push("Freezing temperatures: keep heat on (at least 55°F) even when you're away, open sink cabinets on exterior walls, and report any loss of heat to your landlord right away.");
    if (inf.mood === "storm" || inf.mood === "rain") t.push("Wet weather: photograph any leak or water intrusion with a timestamp and report it to your landlord in writing. Renters insurance usually covers your belongings, not the building.");
    if (inf.mood === "snow") t.push("Snow: check your lease for who clears walkways and parking, and keep a path to exits clear.");
    if ((d.now.gust || 0) >= 40) t.push("High winds: bring in balcony furniture, grills and plants, which can become projectiles.");
    t.push("Using a space heater? Keep it 3 feet from anything that can burn, plug it straight into the wall, and turn it off when you leave. Score your home with our <a href=\"/tools/fire-safety-checklist/\">fire safety checklist</a>.");
    t.push("Never run a generator, grill or camp stove indoors or on a balcony: carbon monoxide can build up quickly. Make sure your unit has a working CO alarm.");
    $("[data-wx-tips]").innerHTML = "<ul>" + t.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul>";
  }

  function load(fresh) {
    W.load(place, fresh).then(render).catch(function () {
      showError("Sorry, the National Weather Service forecast is unavailable for this location right now. NWS covers the United States and its territories; please try again in a few minutes.");
    });
    loadAlerts();
    clearInterval(timer);
    timer = setInterval(function () { W.load(place, true).then(render).catch(function () {}); loadAlerts(); }, 600000);
  }
  load();
})();
