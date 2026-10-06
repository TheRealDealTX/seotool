/* Renter News — live weather page (Open-Meteo + NWS alerts) */
(function () {
  "use strict";
  var app = document.querySelector("[data-weather-app]");
  if (!app || !window.RNWX) return;
  var W = window.RNWX;
  function $(s) { return app.querySelector(s); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var place = W.getPlace(), unit = W.getUnit(), timer;
  var QUICK = [
    ["New York", "New York", 40.7143, -74.006], ["Los Angeles", "California", 34.0522, -118.2437], ["Chicago", "Illinois", 41.85, -87.65],
    ["Houston", "Texas", 29.7633, -95.3633], ["Phoenix", "Arizona", 33.4484, -112.074], ["Philadelphia", "Pennsylvania", 39.9524, -75.1636],
    ["San Antonio", "Texas", 29.4241, -98.4936], ["Dallas", "Texas", 32.7831, -96.8067], ["Miami", "Florida", 25.7743, -80.1937],
    ["Atlanta", "Georgia", 33.749, -84.388], ["Seattle", "Washington", 47.6062, -122.3321], ["Denver", "Colorado", 39.7392, -104.9847]
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
      load();
    });
  });

  /* City search with suggestions */
  var input = $("[data-wx-input]"), sug = $("[data-wx-suggest]"), results = [], active = -1, deb;
  input.addEventListener("input", function () {
    clearTimeout(deb);
    var q = input.value.trim();
    if (q.length < 2) { sug.classList.remove("is-open"); return; }
    deb = setTimeout(function () {
      fetch("https://geocoding-api.open-meteo.com/v1/search?count=8&language=en&format=json&name=" + encodeURIComponent(q))
        .then(function (r) { return r.json(); })
        .then(function (d) {
          results = (d.results || []).sort(function (a, b) { return (b.country_code === "US") - (a.country_code === "US"); });
          active = -1;
          sug.innerHTML = results.length ? results.map(function (r, i) {
            return '<li role="option" data-i="' + i + '">' + esc(r.name) + " <small>" + esc([r.admin1, r.country].filter(Boolean).join(", ")) + "</small></li>";
          }).join("") : "<li>No matches</li>";
          sug.classList.add("is-open");
        }).catch(function () {});
    }, 250);
  });
  input.addEventListener("keydown", function (e) {
    var items = sug.querySelectorAll("[data-i]");
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
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
    choose({ name: r.name, admin: r.admin1 || r.country || "", lat: r.latitude, lon: r.longitude, cc: r.country_code });
  }

  /* Geolocation */
  $("[data-wx-locate]").addEventListener("click", function () {
    if (!navigator.geolocation) return;
    var btn = this; btn.textContent = "Locating…";
    navigator.geolocation.getCurrentPosition(function (pos) {
      var lat = +pos.coords.latitude.toFixed(4), lon = +pos.coords.longitude.toFixed(4);
      btn.textContent = "Use my location";
      // Reverse lookup via NWS (US only); fall back to coordinates.
      fetch("https://api.weather.gov/points/" + lat + "," + lon).then(function (r) { return r.json(); }).then(function (d) {
        var rl = d.properties && d.properties.relativeLocation && d.properties.relativeLocation.properties;
        choose({ name: rl ? rl.city : "My location", admin: rl ? rl.state : "", lat: lat, lon: lon, cc: "US" });
      }).catch(function () { choose({ name: "My location", admin: "", lat: lat, lon: lon }); });
    }, function () { btn.textContent = "Location blocked"; setTimeout(function () { btn.textContent = "Use my location"; }, 2500); }, { timeout: 10000 });
  });

  function choose(p) { place = p; W.setPlace(p); load(); window.scrollTo({ top: app.offsetTop - 120, behavior: "smooth" }); }

  /* Rendering */
  function fmtTime(iso) { return new Date(iso).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }); }
  function compass(deg) { return ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][Math.round(deg / 45) % 8]; }
  function uvLabel(u) { return u < 3 ? "Low" : u < 6 ? "Moderate" : u < 8 ? "High" : u < 11 ? "Very high" : "Extreme"; }
  function aqiLabel(a) { return a <= 50 ? "Good" : a <= 100 ? "Moderate" : a <= 150 ? "Unhealthy for sensitive groups" : a <= 200 ? "Unhealthy" : a <= 300 ? "Very unhealthy" : "Hazardous"; }

  function fx(mood) {
    var h = "";
    if (mood === "rain" || mood === "storm") for (var i = 0; i < 60; i++) h += '<i style="left:' + Math.random() * 110 + "%;animation-duration:" + (0.5 + Math.random() * 0.5) + "s;animation-delay:" + (-Math.random() * 2) + 's"></i>';
    else if (mood === "snow") for (var j = 0; j < 50; j++) h += '<i style="left:' + Math.random() * 100 + "%;animation-duration:" + (4 + Math.random() * 5) + "s;animation-delay:" + (-Math.random() * 8) + 's"></i>';
    else if (mood === "night") for (var k = 0; k < 40; k++) h += '<i style="left:' + Math.random() * 100 + "%;top:" + Math.random() * 100 + "%;animation-delay:" + (-Math.random() * 3) + 's"></i>';
    else if (mood === "clear") h = '<span class="orb"></span>';
    return '<div class="wx-fx ' + (mood === "snow" ? "snow" : mood === "night" ? "stars" : "") + '">' + h + "</div>";
  }

  function render(d) {
    var c = d.current, inf = W.info(c.weather_code, c.is_day), u = unit === "c";
    var sp = u ? " km/h" : " mph", pr = u ? " mm" : " in";
    var hero = $("[data-wx-hero]");
    hero.dataset.mood = inf.mood;
    hero.innerHTML = fx(inf.mood) + '<div class="wxh-grid"><div>' +
      '<div class="wxh-place"><svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>' + esc(place.name) + (place.admin ? ", " + esc(place.admin) : "") + "</div>" +
      '<div class="wxh-main">' + W.icon(inf.kind) + '<div class="wxh-temp">' + Math.round(c.temperature_2m) + "°</div></div>" +
      '<div class="wxh-desc">' + inf.text + "</div>" +
      '<div class="wxh-sub">Feels like ' + Math.round(c.apparent_temperature) + "° · High " + Math.round(d.daily.temperature_2m_max[0]) + "° · Low " + Math.round(d.daily.temperature_2m_min[0]) + "°</div>" +
      '<div class="wxh-sub">Updated ' + fmtTime(c.time) + " local time</div></div>" +
      '<div class="wxh-stats">' +
      "<div><small>Wind</small><b>" + Math.round(c.wind_speed_10m) + sp + "</b> " + compass(c.wind_direction_10m) + "</div>" +
      "<div><small>Humidity</small><b>" + c.relative_humidity_2m + "%</b></div>" +
      "<div><small>Rain chance</small><b>" + (d.daily.precipitation_probability_max[0] ?? 0) + "%</b></div>" +
      "<div><small>UV index</small><b>" + Math.round(c.uv_index ?? d.daily.uv_index_max[0]) + "</b> " + uvLabel(c.uv_index ?? 0) + "</div>" +
      "</div></div>";

    /* Hourly SVG chart */
    var nowIdx = d.hourly.time.findIndex(function (t) { return t >= c.time.slice(0, 13); });
    if (nowIdx < 0) nowIdx = 0;
    var hrs = [];
    for (var i = nowIdx; i < nowIdx + 24 && i < d.hourly.time.length; i++) hrs.push(i);
    var temps = hrs.map(function (i) { return d.hourly.temperature_2m[i]; });
    var lo = Math.min.apply(null, temps), hi = Math.max.apply(null, temps), Wd = 960, Hd = 200, pad = 30;
    var x = function (k) { return pad + k * (Wd - pad * 2) / (hrs.length - 1); };
    var y = function (t) { return 60 + (hi - t) / Math.max(hi - lo, 1) * 70; };
    var line = hrs.map(function (_, k) { return (k ? "L" : "M") + x(k).toFixed(1) + " " + y(temps[k]).toFixed(1); }).join(" ");
    var svg = '<svg viewBox="0 0 ' + Wd + " " + Hd + '" role="img" aria-label="Temperature over the next 24 hours"><defs><linearGradient id="hlg" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stop-color="#2f7fd0" stop-opacity=".35"/><stop offset="1" stop-color="#2f7fd0" stop-opacity="0"/></linearGradient></defs>' +
      '<path class="hl-area" d="' + line + " L" + x(hrs.length - 1) + " 150 L" + x(0) + ' 150 Z"/><path class="hl-line" d="' + line + '"/>';
    hrs.forEach(function (i, k) {
      if (k % 2) return;
      var t = new Date(d.hourly.time[i]).toLocaleTimeString("en-US", { hour: "numeric" });
      var p = d.hourly.precipitation_probability[i];
      svg += '<text class="hl-t" x="' + x(k) + '" y="' + (y(temps[k]) - 12) + '" text-anchor="middle">' + Math.round(temps[k]) + "°</text>" +
        '<circle cx="' + x(k) + '" cy="' + y(temps[k]) + '" r="3.5" fill="#2f7fd0"/>' +
        '<g transform="translate(' + (x(k) - 12) + ' 152) scale(.375)">' + W.icon(W.info(d.hourly.weather_code[i], d.hourly.is_day[i]).kind).replace('<svg class="wx-ico" viewBox="0 0 64 64" aria-hidden="true">', "").replace("</svg>", "") + "</g>" +
        '<text x="' + x(k) + '" y="194" text-anchor="middle">' + (k ? t : "Now") + "</text>" +
        (p ? '<text class="hl-p" x="' + x(k) + '" y="' + (y(temps[k]) + 22) + '" text-anchor="middle">' + p + "%</text>" : "");
    });
    $("[data-wx-hourly]").innerHTML = svg + "</svg>";

    /* Daily */
    var dmin = Math.min.apply(null, d.daily.temperature_2m_min), dmax = Math.max.apply(null, d.daily.temperature_2m_max), span = Math.max(dmax - dmin, 1);
    $("[data-wx-daily]").innerHTML = d.daily.time.map(function (t, i) {
      var lo_ = d.daily.temperature_2m_min[i], hi_ = d.daily.temperature_2m_max[i], di = W.info(d.daily.weather_code[i], 1);
      var name = i === 0 ? "Today" : new Date(t + "T12:00").toLocaleDateString("en-US", { weekday: "short" });
      return '<div class="wx-day"><div><b>' + name + "</b><small>" + new Date(t + "T12:00").toLocaleDateString("en-US", { month: "short", day: "numeric" }) + "</small></div>" +
        W.icon(di.kind) + "<div>" + di.text + "<small>" + (d.daily.precipitation_probability_max[i] ?? 0) + "% rain · wind " + Math.round(d.daily.wind_speed_10m_max[i]) + sp + "</small></div>" +
        '<div class="wx-range"><span>' + Math.round(lo_) + '°</span><div class="wx-range-track"><i style="left:' + ((lo_ - dmin) / span * 100) + "%;right:" + ((dmax - hi_) / span * 100) + '%"></i></div><span>' + Math.round(hi_) + "°</span></div></div>";
    }).join("");

    /* Details */
    var vis = c.visibility != null ? (u ? (c.visibility / 1000).toFixed(1) + " km" : (c.visibility / 5280).toFixed(1) + " mi") : "—";
    $("[data-wx-details]").innerHTML =
      det("Sunrise", fmtTime(d.daily.sunrise[0]), "Sunset " + fmtTime(d.daily.sunset[0])) +
      det("Wind gusts", Math.round(c.wind_gusts_10m) + sp, "From the " + compass(c.wind_direction_10m)) +
      det("Dew point", Math.round(c.dew_point_2m) + "°", c.dew_point_2m > (u ? 18 : 65) ? "Muggy" : "Comfortable") +
      det("Pressure", Math.round(c.pressure_msl) + " hPa", "Sea level") +
      det("Cloud cover", c.cloud_cover + "%", "Visibility " + vis) +
      det("Rain today", (d.daily.precipitation_sum[0] || 0).toFixed(2) + pr, "Max UV " + Math.round(d.daily.uv_index_max[0])) +
      '<div class="wx-detail" data-aqi style="grid-column:span 2"><small>Air quality (US AQI)</small><b>…</b></div>';
    loadAQI();
    tips(d, inf);
  }
  function det(k, v, s) { return '<div class="wx-detail"><small>' + k + "</small><b>" + v + "</b><span>" + s + "</span></div>"; }

  function loadAQI() {
    fetch("https://air-quality-api.open-meteo.com/v1/air-quality?latitude=" + place.lat + "&longitude=" + place.lon + "&current=us_aqi,pm2_5")
      .then(function (r) { return r.json(); }).then(function (a) {
        var v = a.current && a.current.us_aqi, el = app.querySelector("[data-aqi]");
        if (!el || v == null) return;
        el.innerHTML = "<small>Air quality (US AQI)</small><b>" + v + "</b><span>" + aqiLabel(v) + " · PM2.5 " + Math.round(a.current.pm2_5) + ' µg/m³</span><div class="aqi-bar"><i style="left:' + Math.min(100, v / 300 * 100) + '%"></i></div>';
      }).catch(function () {});
  }

  function loadAlerts() {
    var box = $("[data-wx-alerts]"); box.innerHTML = "";
    if (place.cc && place.cc !== "US") return;
    fetch("https://api.weather.gov/alerts/active?point=" + (+place.lat).toFixed(4) + "," + (+place.lon).toFixed(4), { headers: { Accept: "application/geo+json" } })
      .then(function (r) { return r.ok ? r.json() : { features: [] }; })
      .then(function (d) {
        box.innerHTML = (d.features || []).slice(0, 4).map(function (f) {
          var p = f.properties;
          return '<details class="wx-alert"><summary>⚠ ' + esc(p.event) + " — " + esc(p.headline || "") + "</summary><p>" + esc((p.description || "").slice(0, 1200)) + (p.instruction ? "\n\n" + esc(p.instruction.slice(0, 600)) : "") + "</p></details>";
        }).join("");
      }).catch(function () {});
  }

  function tips(d, inf) {
    var t = [], c = d.current, hot = unit === "c" ? 32 : 90, cold = unit === "c" ? 0 : 32, maxT = d.daily.temperature_2m_max[0], minT = d.daily.temperature_2m_min[0];
    if (maxT >= hot) t.push("Heat today: keep blinds closed in the afternoon, check on older neighbors, and report a broken air conditioner to your landlord in writing if your lease or local code requires cooling.");
    if (minT <= cold) t.push("Freezing temperatures: keep heat on (at least 55°F) even when you're away, open sink cabinets on exterior walls, and report any loss of heat to your landlord right away.");
    if (inf.mood === "storm" || inf.mood === "rain") t.push("Wet weather: photograph any leak or water intrusion with a timestamp and report it to your landlord in writing. Renters insurance usually covers your belongings, not the building.");
    if (inf.mood === "snow") t.push("Snow: check your lease for who clears walkways and parking, and keep a path to exits clear.");
    if ((c.wind_gusts_10m || 0) >= (unit === "c" ? 60 : 40)) t.push("High winds: bring in balcony furniture, grills and plants, which can become projectiles.");
    t.push("Using a space heater? Keep it 3 feet from anything that can burn, plug it straight into the wall, and turn it off when you leave. Score your home with our <a href=\"/tools/fire-safety-checklist/\">fire safety checklist</a>.");
    t.push("Never run a generator, grill or camp stove indoors or on a balcony: carbon monoxide can build up quickly. Make sure your unit has a working CO alarm.");
    $("[data-wx-tips]").innerHTML = "<ul>" + t.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ul>";
  }

  function load() {
    W.fetch(place, unit).then(render).catch(function () {
      $("[data-wx-hero]").innerHTML = "<p>Sorry, the forecast service is unavailable right now. Please try again in a few minutes.</p>";
    });
    loadAlerts();
    clearInterval(timer);
    // Refresh every 10 minutes; a nudged latitude bypasses the in-memory cache.
    timer = setInterval(function () { W.fetch({ lat: place.lat + Math.random() * 1e-6, lon: place.lon }, unit).then(render).catch(function () {}); }, 600000);
  }
  load();
})();
