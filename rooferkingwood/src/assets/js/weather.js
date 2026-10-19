/* Kingwood Roofers — live Kingwood, TX weather (Open-Meteo forecast + NWS alerts). No API key needed. */
(function () {
  "use strict";
  var LAT = 30.0499, LON = -95.1847;
  var API = "https://api.open-meteo.com/v1/forecast?latitude=" + LAT + "&longitude=" + LON +
    "&current=temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_gusts_10m,wind_direction_10m" +
    "&hourly=wind_gusts_10m,precipitation_probability" +
    "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max,uv_index_max,sunrise,sunset" +
    "&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FChicago&forecast_days=7";
  var ALERTS = "https://api.weather.gov/alerts/active?point=" + LAT + "," + LON;
  var NWS_LINK = "https://forecast.weather.gov/MapClick.php?lat=" + LAT + "&lon=" + LON;

  var CODES = {
    0: ["☀️", "Clear sky"], 1: ["🌤️", "Mostly clear"], 2: ["⛅", "Partly cloudy"], 3: ["☁️", "Overcast"],
    45: ["🌫️", "Fog"], 48: ["🌫️", "Freezing fog"], 51: ["🌦️", "Light drizzle"], 53: ["🌦️", "Drizzle"], 55: ["🌧️", "Heavy drizzle"],
    56: ["🌧️", "Freezing drizzle"], 57: ["🌧️", "Freezing drizzle"], 61: ["🌦️", "Light rain"], 63: ["🌧️", "Rain"], 65: ["🌧️", "Heavy rain"],
    66: ["🌧️", "Freezing rain"], 67: ["🌧️", "Freezing rain"], 71: ["🌨️", "Light snow"], 73: ["🌨️", "Snow"], 75: ["❄️", "Heavy snow"],
    77: ["🌨️", "Snow grains"], 80: ["🌦️", "Rain showers"], 81: ["🌧️", "Heavy showers"], 82: ["⛈️", "Violent showers"],
    85: ["🌨️", "Snow showers"], 86: ["🌨️", "Snow showers"], 95: ["⛈️", "Thunderstorms"], 96: ["⛈️", "T-storms with hail"], 99: ["⛈️", "Severe T-storms, hail"]
  };
  function code(c) { return CODES[c] || ["🌡️", "—"]; }
  function r(n) { return Math.round(n); }
  function dir(deg) { return ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][Math.round(deg / 45) % 8]; }
  function day(iso, short) { return new Date(iso + "T12:00:00").toLocaleDateString("en-US", { weekday: short ? "short" : "long" }); }
  function md(iso) { return new Date(iso + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" }); }
  function time(iso) { return new Date(iso).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }); }
  function esc(s) { var e = document.createElement("div"); e.textContent = s == null ? "" : String(s); return e.innerHTML; }

  /* Roof-risk rating: thunderstorms and strong gusts (limbs, shingles) are what damage Kingwood roofs. */
  function risk(d, i) {
    var c = d.weather_code[i], g = d.wind_gusts_10m_max[i], p = d.precipitation_probability_max[i] || 0;
    if (c === 96 || c === 99 || g >= 50) return ["high", "High risk"];
    if (c === 95 || c === 82 || g >= 35 || (c >= 80 && p >= 60)) return ["mod", "Moderate"];
    return ["low", "Low risk"];
  }

  var chip = document.querySelector("[data-wx-chip]");
  var desks = [].slice.call(document.querySelectorAll("[data-wx-desk]"));
  var alertBox = document.querySelector("[data-wx-alerts]");
  var alertLines = [].slice.call(document.querySelectorAll("[data-wx-alertline]"));
  var fc = document.querySelector("[data-wx-forecast]");
  var hourly = document.querySelector("[data-wx-hourly]");
  if (!chip && !desks.length && !fc && !alertBox) return;

  function renderChip(w) {
    var c = w.current, cc = code(c.weather_code);
    chip.innerHTML = "<span class='ic'>" + cc[0] + "</span><span><small><span class='pulse'></span>Live in Kingwood</small><b>" + r(c.temperature_2m) +
      "°F</b><small>" + cc[1] + " · gusts " + r(c.wind_gusts_10m) + " mph</small></span>";
  }

  function renderDesk(el, w) {
    var c = w.current, d = w.daily, cc = code(c.weather_code);
    var now = el.querySelector(".desk-now");
    now.innerHTML = "<span class='kicker light'>Right now in Kingwood</span>" +
      "<div class='big'><span class='ic' aria-hidden='true'>" + cc[0] + "</span><div><b>" + r(c.temperature_2m) + "°</b><div style='color:#fff'>" + cc[1] +
      " · feels " + r(c.apparent_temperature) + "°</div></div></div>" +
      "<div class='facts'><div><small>Wind</small><b>" + r(c.wind_speed_10m) + " mph " + dir(c.wind_direction_10m) + "</b></div>" +
      "<div><small>Gusts</small><b>" + r(c.wind_gusts_10m) + " mph</b></div>" +
      "<div><small>Humidity</small><b>" + r(c.relative_humidity_2m) + "%</b></div>" +
      "<div><small>UV today</small><b>" + r(d.uv_index_max[0]) + "</b></div></div>";
    var days = el.querySelector(".desk-days");
    if (days) {
      var html = "";
      for (var i = 0; i < 5; i++) {
        var rk = risk(d, i);
        html += "<div class='desk-day'><span class='d'>" + (i === 0 ? "Today" : day(d.time[i], true)) + "</span><span class='ic' aria-hidden='true'>" +
          code(d.weather_code[i])[0] + "</span><span class='t'>" + r(d.temperature_2m_max[i]) + "° <span>" + r(d.temperature_2m_min[i]) + "°</span></span>" +
          "<span style='font-size:.78rem'>💨 " + r(d.wind_gusts_10m_max[i]) + " mph</span><span class='risk " + rk[0] + "'>" + rk[1] + "</span></div>";
      }
      days.innerHTML = html;
    }
    var up = el.querySelector("[data-wx-updated]");
    if (up) up.textContent = "Updated " + time(c.time) + " CT";
  }

  function renderHourly(w) {
    var h = w.hourly, cur = w.current.time.slice(0, 13);
    var start = 0;
    for (var i = 0; i < h.time.length; i++) { if (h.time[i].slice(0, 13) >= cur) { start = i; break; } }
    var idx = []; for (var k = start; k < Math.min(start + 24, h.time.length); k++) idx.push(k);
    var hoursEl = document.querySelector("[data-wx-hours]");
    function draw(kind) {
      var vals = idx.map(function (j) { return kind === "gust" ? h.wind_gusts_10m[j] : (h.precipitation_probability[j] || 0); });
      var max = kind === "gust" ? Math.max(50, Math.max.apply(null, vals)) : 100;
      hourly.innerHTML = vals.map(function (v, n) {
        var hot = kind === "gust" && v >= 35;
        return "<div class='h' title='" + time(h.time[idx[n]]) + ": " + r(v) + (kind === "gust" ? " mph" : "%") + "'><span class='v'>" + r(v) + "</span>" +
          "<span class='bar" + (kind === "rain" ? " rain" : "") + "' style='height:" + Math.max(1, v / max * 85).toFixed(1) + "%" + (hot ? ";background:var(--bad)" : "") + "'></span></div>";
      }).join("");
    }
    if (hoursEl) hoursEl.innerHTML = idx.map(function (j) { return "<span>" + new Date(h.time[j]).toLocaleTimeString("en-US", { hour: "numeric" }).replace(" ", "").toLowerCase() + "</span>"; }).join("");
    draw("gust");
    document.querySelectorAll("[data-chart]").forEach(function (b) {
      b.addEventListener("click", function () {
        document.querySelectorAll("[data-chart]").forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
        draw(b.getAttribute("data-chart"));
      });
    });
  }

  function renderForecast(w) {
    var d = w.daily, html = "";
    for (var i = 0; i < d.time.length; i++) {
      var cc = code(d.weather_code[i]), rk = risk(d, i);
      html += "<div class='fc-day'><div class='d'>" + (i === 0 ? "Today" : day(d.time[i], true)) + "</div><div class='dt'>" + md(d.time[i]) + "</div>" +
        "<div class='ic' aria-hidden='true'>" + cc[0] + "</div><div class='desc'>" + cc[1] + "</div>" +
        "<div><span class='hi'>" + r(d.temperature_2m_max[i]) + "°</span> <span class='lo'>" + r(d.temperature_2m_min[i]) + "°</span></div>" +
        "<div class='row' title='Chance of rain'>💧 " + (d.precipitation_probability_max[i] || 0) + "% · " + d.precipitation_sum[i].toFixed(2) + "\"</div>" +
        "<div class='row' title='Max wind gust'>💨 " + r(d.wind_gusts_10m_max[i]) + " mph</div>" +
        "<span class='risk " + rk[0] + "'>" + rk[1] + "</span></div>";
    }
    fc.innerHTML = html;
    var tbl = document.querySelector("[data-wx-table]");
    if (tbl) {
      var rows = "";
      for (var j = 0; j < d.time.length; j++) {
        rows += "<tr><td>" + day(d.time[j]) + ", " + md(d.time[j]) + "</td><td>" + code(d.weather_code[j])[1] + "</td><td>" + r(d.temperature_2m_max[j]) +
          "° / " + r(d.temperature_2m_min[j]) + "°</td><td>" + (d.precipitation_probability_max[j] || 0) + "%</td><td>" + r(d.wind_speed_10m_max[j]) +
          " / " + r(d.wind_gusts_10m_max[j]) + " mph</td><td>" + r(d.uv_index_max[j]) + "</td></tr>";
      }
      tbl.innerHTML = rows;
    }
    var outlook = document.querySelector("[data-wx-outlook]");
    if (outlook) {
      var worst = 0, worstDay = 0;
      for (var k = 0; k < d.time.length; k++) {
        var lvl = { low: 0, mod: 1, high: 2 }[risk(d, k)[0]];
        if (lvl > worst) { worst = lvl; worstDay = k; }
      }
      var when = worstDay === 0 ? "today" : day(d.time[worstDay]);
      outlook.innerHTML = worst === 0
        ? "<b>Quiet week for roofs.</b> No thunderstorms or damaging gusts in the 7-day forecast, a good window for repairs, inspections and replacements."
        : worst === 1
          ? "<b>Watch " + when + ".</b> Showers, thunderstorms or gusty winds are possible. Clear gutters and valleys and secure loose items; check for fallen limbs afterward."
          : "<b>Severe weather possible " + when + ".</b> Thunderstorms with hail or damaging gusts are in the forecast. Park inside, photograph your roof beforehand and book a free inspection after it passes.";
    }
  }

  function renderAlerts(data) {
    var feats = (data && data.features) || [];
    var stamp = new Date().toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
    alertLines.forEach(function (el) {
      el.innerHTML = feats.length
        ? "⚠️ <b style='color:#fff'>" + esc(feats[0].properties.event) + "</b> in effect for Kingwood. <a href='/weather/'>Details</a>"
        : "✅ No active National Weather Service alerts for Kingwood (checked " + stamp + ").";
    });
    if (!alertBox) return;
    if (!feats.length) {
      alertBox.classList.remove("active");
      alertBox.innerHTML = "<h3>✅ No active National Weather Service alerts for Kingwood</h3><p style='margin:0;color:var(--muted)'>Checked " + stamp + ". This updates every time the page loads.</p>";
      return;
    }
    alertBox.classList.add("active");
    alertBox.innerHTML = feats.slice(0, 4).map(function (f) {
      var p = f.properties;
      return "<h3>⚠️ " + esc(p.event) + "</h3><p style='margin:0 0 6px'>" + esc(p.headline) + "</p>" +
        "<p style='margin:0 0 14px;color:var(--muted);font-size:.9rem'>Until " + esc(new Date(p.ends || p.expires).toLocaleString("en-US", { weekday: "short", hour: "numeric", minute: "2-digit" })) + " · Source: NWS</p>";
    }).join("");
  }

  function getJSON(url, opts) {
    var ctl = window.AbortController ? new AbortController() : null;
    var timer = ctl ? setTimeout(function () { ctl.abort(); }, 10000) : null;
    opts = opts || {};
    if (ctl) opts.signal = ctl.signal;
    return fetch(url, opts).then(function (res) {
      clearTimeout(timer);
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    });
  }

  getJSON(API).then(function (w) {
    if (chip) renderChip(w);
    desks.forEach(function (el) { renderDesk(el, w); });
    if (hourly) renderHourly(w);
    if (fc) renderForecast(w);
  }).catch(function () {
    var link = "<a href='" + NWS_LINK + "' rel='noopener' target='_blank'>National Weather Service forecast for Kingwood</a>";
    if (chip) chip.innerHTML = "<span class='ic'>⛅</span><span><small>Kingwood weather</small><b>Forecast</b><small>Tap for the storm desk</small></span>";
    desks.forEach(function (el) { el.querySelector(".desk-now").innerHTML = "<span class='kicker light'>Kingwood weather</span><p>Live data is reloading. Refresh in a moment or see the " + link + ".</p>"; });
    if (fc) fc.innerHTML = "<p style='grid-column:1/-1;padding:20px'>Live weather is temporarily unavailable. Refresh in a moment, or see the " + link + ".</p>";
    if (hourly) hourly.innerHTML = "";
  });

  if (alertBox || alertLines.length) {
    getJSON(ALERTS, { headers: { Accept: "application/geo+json" } })
      .then(renderAlerts)
      .catch(function () {
        var msg = "Alert feed unavailable. Check <a href='https://www.weather.gov/hgx/' target='_blank' rel='noopener'>weather.gov/hgx</a>.";
        alertLines.forEach(function (el) { el.innerHTML = msg; });
        if (alertBox) alertBox.innerHTML = "<p style='margin:0'>" + msg + "</p>";
      });
  }
})();
