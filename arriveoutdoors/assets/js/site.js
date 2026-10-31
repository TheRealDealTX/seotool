/* Arrive Outdoors — shared script: nav, place search, forecast, hike score, sun math. */
(function () {
  "use strict";
  var AO = (window.AO = window.AO || {});

  // ---- nav ----
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".menu-btn");
    if (b) {
      var nav = document.getElementById("nav");
      var open = nav.classList.toggle("open");
      b.setAttribute("aria-expanded", open ? "true" : "false");
    }
  });

  // ---- helpers ----
  AO.$ = function (s, r) { return (r || document).querySelector(s); };
  AO.$$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  AO.esc = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  AO.store = {
    get: function (k, d) { try { var v = localStorage.getItem("ao:" + k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem("ao:" + k, JSON.stringify(v)); } catch (e) {} }
  };
  AO.num = function (el) { var v = parseFloat(typeof el === "string" ? AO.$(el).value : el.value); return isNaN(v) ? 0 : v; };
  AO.radio = function (name) { var r = AO.$('input[name="' + name + '"]:checked'); return r ? r.value : null; };
  AO.fmtTime = function (d, tz) {
    if (!d || isNaN(d)) return "—";
    return d.toLocaleTimeString([], { hour: "numeric", minute: "2-digit", timeZone: tz || undefined });
  };
  AO.scoreColor = function (s) { return s >= 80 ? "#2f8a57" : s >= 65 ? "#9aa83a" : s >= 50 ? "#d99a2b" : "#c74f3a"; };
  AO.scoreLabel = function (s) { return s >= 80 ? "Great" : s >= 65 ? "Good" : s >= 50 ? "Fair" : "Poor"; };

  // ---- place search (Open-Meteo geocoding, no key) ----
  AO.geocode = function (q) {
    var u = "https://geocoding-api.open-meteo.com/v1/search?count=6&language=en&format=json&name=" + encodeURIComponent(q);
    return fetch(u).then(function (r) { return r.json(); }).then(function (j) { return j.results || []; });
  };
  AO.placeLabel = function (p) { return [p.name, p.admin1, p.country_code === "US" ? "" : p.country].filter(Boolean).join(", "); };
  AO.placePicker = function (input, onPick) {
    var box = document.createElement("div"); box.className = "ac-list";
    input.parentNode.insertBefore(box, input.nextSibling);
    var t, items = [], idx = -1;
    function close() { box.innerHTML = ""; items = []; idx = -1; }
    function pick(p) { input.value = AO.placeLabel(p); close(); onPick({ name: AO.placeLabel(p), lat: p.latitude, lon: p.longitude, elevation: p.elevation, tz: p.timezone }); }
    function render() {
      if (!items.length) { box.innerHTML = ""; return; }
      box.innerHTML = "<ul role='listbox'>" + items.map(function (p, i) {
        return "<li role='option' data-i='" + i + "'" + (i === idx ? " class='active'" : "") + ">" + AO.esc(AO.placeLabel(p)) +
          (p.elevation != null ? " <span class='muted small'>· " + Math.round(p.elevation * 3.281).toLocaleString() + " ft</span>" : "") + "</li>";
      }).join("") + "</ul>";
    }
    input.setAttribute("autocomplete", "off");
    input.addEventListener("input", function () {
      clearTimeout(t);
      var q = input.value.trim();
      if (q.length < 2) { close(); return; }
      t = setTimeout(function () { AO.geocode(q).then(function (r) { items = r; idx = -1; render(); }).catch(close); }, 250);
    });
    input.addEventListener("keydown", function (e) {
      if (!items.length) return;
      if (e.key === "ArrowDown") { idx = Math.min(items.length - 1, idx + 1); render(); e.preventDefault(); }
      else if (e.key === "ArrowUp") { idx = Math.max(0, idx - 1); render(); e.preventDefault(); }
      else if (e.key === "Enter") { pick(items[Math.max(0, idx)]); e.preventDefault(); }
      else if (e.key === "Escape") close();
    });
    box.addEventListener("mousedown", function (e) {
      var li = e.target.closest("li"); if (li) { e.preventDefault(); pick(items[+li.dataset.i]); }
    });
    input.addEventListener("blur", function () { setTimeout(close, 150); });
  };
  AO.locateMe = function (cb, statusEl) {
    if (!navigator.geolocation) { if (statusEl) statusEl.textContent = "Location isn't available in this browser."; return; }
    if (statusEl) statusEl.textContent = "Finding your location…";
    navigator.geolocation.getCurrentPosition(function (pos) {
      if (statusEl) statusEl.textContent = "";
      cb({ name: "My location", lat: pos.coords.latitude, lon: pos.coords.longitude });
    }, function () { if (statusEl) statusEl.textContent = "Couldn't get your location — search for a place instead."; }, { timeout: 10000 });
  };

  // ---- forecast + hike score ----
  var WX = {
    0: ["Clear", "☀️"], 1: ["Mostly clear", "🌤️"], 2: ["Partly cloudy", "⛅"], 3: ["Overcast", "☁️"],
    45: ["Fog", "🌫️"], 48: ["Freezing fog", "🌫️"], 51: ["Light drizzle", "🌦️"], 53: ["Drizzle", "🌦️"], 55: ["Heavy drizzle", "🌧️"],
    56: ["Freezing drizzle", "🌧️"], 57: ["Freezing drizzle", "🌧️"], 61: ["Light rain", "🌦️"], 63: ["Rain", "🌧️"], 65: ["Heavy rain", "🌧️"],
    66: ["Freezing rain", "🌧️"], 67: ["Freezing rain", "🌧️"], 71: ["Light snow", "🌨️"], 73: ["Snow", "🌨️"], 75: ["Heavy snow", "❄️"],
    77: ["Snow grains", "🌨️"], 80: ["Showers", "🌦️"], 81: ["Showers", "🌧️"], 82: ["Violent showers", "🌧️"], 85: ["Snow showers", "🌨️"],
    86: ["Heavy snow showers", "❄️"], 95: ["Thunderstorms", "⛈️"], 96: ["Thunderstorms + hail", "⛈️"], 99: ["Severe thunderstorms", "⛈️"]
  };
  AO.wx = function (c) { return WX[c] || ["—", "🌡️"]; };

  AO.forecast = function (lat, lon, opts) {
    opts = opts || {};
    var daily = "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min," +
      "precipitation_sum,precipitation_probability_max,snowfall_sum,wind_speed_10m_max,wind_gusts_10m_max,uv_index_max,sunrise,sunset";
    var u = "https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon +
      (opts.elevation != null ? "&elevation=" + opts.elevation : "") +
      "&daily=" + daily + "&hourly=freezing_level_height&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=auto&forecast_days=7";
    return fetch(u).then(function (r) { if (!r.ok) throw new Error("forecast " + r.status); return r.json(); });
  };

  // Score one forecast day for hiking (0-100) and collect warnings.
  AO.hikeScore = function (d, i) {
    var s = 100, w = [];
    var hi = d.temperature_2m_max[i], lo = d.temperature_2m_min[i], feel = d.apparent_temperature_max[i];
    var pp = d.precipitation_probability_max[i] || 0, pr = d.precipitation_sum[i] || 0, sn = d.snowfall_sum[i] || 0;
    var gust = d.wind_gusts_10m_max[i] || 0, uv = d.uv_index_max[i] || 0, code = d.weather_code[i];
    var t = Math.max(hi, feel || hi);
    if (hi < 50) s -= (50 - hi) * 1.4;
    if (t > 78) s -= (t - 78) * 2.4;
    s -= pp * 0.35;
    if ((code >= 51 && code <= 67) || (code >= 80 && code <= 82)) s -= (code === 65 || code === 67 || code === 82 || pr >= 0.5) ? 25 : 12;
    else if (pr >= 0.25) s -= 10;
    if (gust > 25) s -= (gust - 25) * 1.4;
    if (code >= 95) { s -= 25; w.push("Thunderstorms forecast — plan to be off summits and exposed ridges by early afternoon."); }
    if ((code >= 71 && code <= 77) || code === 85 || code === 86 || sn > 0.5) { s -= 12; w.push("Snow expected (" + sn.toFixed(1) + " in) — traction and route-finding may be needed."); }
    if (t >= 95) w.push("Extreme heat (feels like " + Math.round(t) + "°F) — start at dawn, carry extra water, avoid exposed trails midday.");
    else if (t >= 88) w.push("Hot (feels like " + Math.round(t) + "°F) — start early and carry more water than usual.");
    if (gust >= 40) w.push("Strong gusts to " + Math.round(gust) + " mph — dangerous on ridges and for tents.");
    else if (gust >= 30) w.push("Gusty winds to " + Math.round(gust) + " mph on exposed terrain.");
    if (lo <= 32) w.push("Freezing overnight (low " + Math.round(lo) + "°F) — campers need a warm sleep system.");
    if (uv >= 8) w.push("Very high UV (index " + Math.round(uv) + ") — sun hoodie, hat and sunscreen.");
    if (pp >= 60 && code < 95) w.push(pp + "% chance of precipitation — pack rain gear.");
    s = Math.max(0, Math.min(100, Math.round(s)));
    return { score: s, warnings: w };
  };

  AO.renderForecast = function (el, place) {
    el.innerHTML = "<p class='status'>Loading the 7-day forecast for " + AO.esc(place.name) + "…</p>";
    return AO.forecast(place.lat, place.lon, { elevation: place.elevation }).then(function (j) {
      var d = j.daily, tz = j.timezone, html = "<div class='fc-days'>", warns = [];
      for (var i = 0; i < d.time.length; i++) {
        var dt = new Date(d.time[i] + "T12:00:00");
        var hs = AO.hikeScore(d, i), wx = AO.wx(d.weather_code[i]);
        hs.warnings.forEach(function (x) { warns.push("<b>" + dt.toLocaleDateString([], { weekday: "short" }) + ":</b> " + AO.esc(x)); });
        html += "<div class='fc-day'><b>" + (i === 0 ? "Today" : dt.toLocaleDateString([], { weekday: "short", month: "short", day: "numeric" })) + "</b>" +
          "<div style='font-size:1.6rem' aria-hidden='true'>" + wx[1] + "</div><div class='small'>" + wx[0] + "</div>" +
          "<div class='t'>" + Math.round(d.temperature_2m_max[i]) + "° / " + Math.round(d.temperature_2m_min[i]) + "°</div>" +
          "<div class='small muted'>💧 " + (d.precipitation_probability_max[i] || 0) + "% · 💨 " + Math.round(d.wind_gusts_10m_max[i] || 0) + " mph</div>" +
          "<span class='score' style='background:" + AO.scoreColor(hs.score) + "' title='Hike score'>" + hs.score + " " + AO.scoreLabel(hs.score) + "</span></div>";
      }
      html += "</div>";
      // freezing level from hourly (midday values)
      var fl = j.hourly && j.hourly.freezing_level_height, flText = "";
      if (fl && fl.length) {
        var noon = fl.filter(function (_, k) { return k % 24 === 13; }).filter(function (v) { return v != null; });
        if (noon.length) {
          var k = (j.hourly_units && j.hourly_units.freezing_level_height === "ft") ? 1 : 3.281;
          var mn = Math.min.apply(null, noon) * k, mx = Math.max.apply(null, noon) * k;
          flText = "<p class='small muted'>Midday freezing level this week: " + (Math.round(mn / 100) * 100).toLocaleString() + "–" + (Math.round(mx / 100) * 100).toLocaleString() + " ft. Above that elevation, expect snow and ice rather than rain.</p>";
        }
      }
      html += "<p class='small muted' style='margin-top:10px'>Today: sunrise " + d.sunrise[0].slice(11) + " · sunset " + d.sunset[0].slice(11) + " (local time, " + AO.esc(tz) + "). " +
        "Forecast data: <a href='https://open-meteo.com/' rel='nofollow noopener'>Open-Meteo</a>. Always check the <a href='https://www.weather.gov/' rel='nofollow noopener'>National Weather Service</a> before you go.</p>" + flText;
      if (warns.length) html += "<div class='fc-warn'><strong>Heads-up this week</strong>" + warns.slice(0, 8).map(function (x) { return "<div>" + x + "</div>"; }).join("") + "</div>";
      el.innerHTML = html;
      if (AO.fx) AO.fx.weatherFor(el.classList.contains("forecast") ? el : (el.closest(".forecast") || el), d.weather_code[0]);
      return j;
    }).catch(function () {
      el.innerHTML = "<p class='err'>The forecast couldn't be loaded right now. Try again in a minute, or check <a href='https://www.weather.gov/'>weather.gov</a>.</p>";
    });
  };

  // ---- sun position math (NOAA) ----
  function rad(d) { return d * Math.PI / 180; }
  function deg(r) { return r * 180 / Math.PI; }
  // Returns {sunrise, sunset, noon, goldenAM, goldenPM, civilDawn, civilDusk} as Date objects (UTC instants).
  AO.sunTimes = function (date, lat, lon) {
    var y = date.getFullYear(), m = date.getMonth() + 1, dd = date.getDate();
    var a = Math.floor((14 - m) / 12), yy = y + 4800 - a, mm = m + 12 * a - 3;
    var jdn = dd + Math.floor((153 * mm + 2) / 5) + 365 * yy + Math.floor(yy / 4) - Math.floor(yy / 100) + Math.floor(yy / 400) - 32045;
    var n = jdn - 2451545.0 + 0.0008;
    var Js = n - lon / 360;
    var M = (357.5291 + 0.98560028 * Js) % 360;
    var C = 1.9148 * Math.sin(rad(M)) + 0.02 * Math.sin(rad(2 * M)) + 0.0003 * Math.sin(rad(3 * M));
    var L = (M + C + 180 + 102.9372) % 360;
    var Jt = 2451545.0 + Js + 0.0053 * Math.sin(rad(M)) - 0.0069 * Math.sin(rad(2 * L));
    var dec = Math.asin(Math.sin(rad(L)) * Math.sin(rad(23.4397)));
    function at(alt) {
      var c = (Math.sin(rad(alt)) - Math.sin(rad(lat)) * Math.sin(dec)) / (Math.cos(rad(lat)) * Math.cos(dec));
      if (c > 1 || c < -1) return null;
      var w = deg(Math.acos(c));
      return [Jt - w / 360, Jt + w / 360];
    }
    function toDate(j) { return j == null ? null : new Date((j - 2440587.5) * 86400000); }
    var sr = at(-0.833), civ = at(-6), gold = at(6);
    return {
      noon: toDate(Jt),
      sunrise: sr && toDate(sr[0]), sunset: sr && toDate(sr[1]),
      civilDawn: civ && toDate(civ[0]), civilDusk: civ && toDate(civ[1]),
      goldenAMEnd: gold && toDate(gold[0]), goldenPMStart: gold && toDate(gold[1]),
      polar: sr ? null : (Math.sin(rad(lat)) * Math.sin(dec) > 0 ? "day" : "night")
    };
  };
})();
