/* Katy Roofer — live Katy, TX weather (Open-Meteo forecast + NWS alerts). No API key needed. */
(function () {
  "use strict";
  var LAT = 29.7858, LON = -95.8245;
  var API = "https://api.open-meteo.com/v1/forecast?latitude=" + LAT + "&longitude=" + LON +
    "&current=temperature_2m,apparent_temperature,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_gusts_10m,wind_direction_10m,is_day" +
    "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,wind_gusts_10m_max,uv_index_max,sunrise,sunset" +
    "&temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch&timezone=America%2FChicago&forecast_days=7";
  var ALERTS = "https://api.weather.gov/alerts/active?point=" + LAT + "," + LON;

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
  function day(iso, short) {
    var d = new Date(iso + "T12:00:00");
    return d.toLocaleDateString("en-US", short ? { weekday: "short" } : { weekday: "long" });
  }
  function md(iso) { return new Date(iso + "T12:00:00").toLocaleDateString("en-US", { month: "short", day: "numeric" }); }
  function time(iso) { return new Date(iso).toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }); }

  /* Roof-risk rating for a day: thunderstorms or strong gusts are what damage roofs. */
  function risk(d, i) {
    var c = d.weather_code[i], g = d.wind_gusts_10m_max[i], p = d.precipitation_probability_max[i] || 0;
    if (c === 96 || c === 99 || g >= 50) return ["high", "High roof risk"];
    if (c === 95 || c === 82 || g >= 35 || (c >= 80 && p >= 60)) return ["mod", "Moderate"];
    return ["low", "Low risk"];
  }
  function esc(s) { var e = document.createElement("div"); e.textContent = s == null ? "" : String(s); return e.innerHTML; }

  function renderMini(el, w) {
    var c = w.current, d = w.daily, cc = code(c.weather_code);
    var days = "";
    for (var i = 1; i <= 3; i++) {
      days += "<div><b>" + day(d.time[i], true) + "</b><span style='font-size:1.5rem'>" + code(d.weather_code[i])[0] + "</span><br>" +
        r(d.temperature_2m_max[i]) + "° / " + r(d.temperature_2m_min[i]) + "°</div>";
    }
    el.innerHTML = "<div class='eyebrow' style='color:var(--gold)'><span class='dot'></span>Live in Katy, TX</div>" +
      "<div class='wx-now'><div class='ic'>" + cc[0] + "</div><div><div class='t'>" + r(c.temperature_2m) + "°F</div>" +
      "<div>" + cc[1] + " · Feels " + r(c.apparent_temperature) + "°</div></div></div>" +
      "<div style='margin-top:10px;color:#aab8cb;font-size:.92rem'>Wind " + r(c.wind_speed_10m) + " mph " + dir(c.wind_direction_10m) +
      " · Gusts " + r(c.wind_gusts_10m) + " mph · Humidity " + r(c.relative_humidity_2m) + "%</div>" +
      "<div class='wx-days'>" + days + "</div>" +
      "<a class='btn btn-sm btn-light' style='margin-top:18px;width:100%' href='/weather/'>Full 7-day forecast</a>";
  }

  function renderCurrent(el, w) {
    var c = w.current, d = w.daily, cc = code(c.weather_code);
    el.innerHTML = "<div class='wx-now'><div class='ic' style='font-size:4.4rem'>" + cc[0] + "</div><div><div class='t' style='font-size:4.4rem'>" +
      r(c.temperature_2m) + "°F</div><div style='font-size:1.1rem'>" + cc[1] + " · Feels like " + r(c.apparent_temperature) + "°F</div>" +
      "<div style='color:#aab8cb;font-size:.85rem;margin-top:4px'>Updated " + time(c.time) + " CT</div></div></div>" +
      "<div class='wx-metrics'>" +
      "<div><small>Humidity</small><b>" + r(c.relative_humidity_2m) + "%</b></div>" +
      "<div><small>Wind</small><b>" + r(c.wind_speed_10m) + " mph " + dir(c.wind_direction_10m) + "</b></div>" +
      "<div><small>Gusts</small><b>" + r(c.wind_gusts_10m) + " mph</b></div>" +
      "<div><small>Precip (now)</small><b>" + c.precipitation.toFixed(2) + " in</b></div>" +
      "<div><small>UV index today</small><b>" + r(d.uv_index_max[0]) + "</b></div>" +
      "<div><small>Sunrise / Sunset</small><b>" + time(d.sunrise[0]).replace(" AM", "a") + " / " + time(d.sunset[0]).replace(" PM", "p") + "</b></div>" +
      "</div>";
  }

  function renderForecast(el, w) {
    var d = w.daily, html = "";
    for (var i = 0; i < d.time.length; i++) {
      var cc = code(d.weather_code[i]), rk = risk(d, i);
      html += "<div class='wx-day' data-reveal style='--d:" + (i * 0.06) + "s'>" +
        "<div class='d'>" + (i === 0 ? "Today" : day(d.time[i], true)) + "</div><div class='dt'>" + md(d.time[i]) + "</div>" +
        "<div class='ic' aria-hidden='true'>" + cc[0] + "</div><div class='desc'>" + cc[1] + "</div>" +
        "<div><span class='hi'>" + r(d.temperature_2m_max[i]) + "°</span> <span class='lo'>" + r(d.temperature_2m_min[i]) + "°</span></div>" +
        "<div class='row' title='Chance of rain'>💧 " + (d.precipitation_probability_max[i] || 0) + "% · " + d.precipitation_sum[i].toFixed(2) + "\"</div>" +
        "<div class='row' title='Max wind gust'>💨 gusts " + r(d.wind_gusts_10m_max[i]) + " mph</div>" +
        "<span class='risk " + rk[0] + "'>" + rk[1] + "</span></div>";
    }
    el.innerHTML = html;
    requestAnimationFrame(function () { el.querySelectorAll("[data-reveal]").forEach(function (x) { x.classList.add("in"); }); });

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
      var worst = 0, worstDay = null;
      for (var k = 0; k < d.time.length; k++) {
        var lvl = { low: 0, mod: 1, high: 2 }[risk(d, k)[0]];
        if (lvl > worst) { worst = lvl; worstDay = k; }
      }
      outlook.innerHTML = worst === 0
        ? "<b>Quiet week for roofs.</b> No thunderstorms or damaging gusts in the 7-day forecast — a good window for repairs, inspections and replacements."
        : worst === 1
          ? "<b>Watch " + (worstDay === 0 ? "today" : day(d.time[worstDay])) + ".</b> Showers, thunderstorms or gusty winds are possible. Clear gutters and secure loose items; check your roof afterward."
          : "<b>Severe weather possible " + (worstDay === 0 ? "today" : day(d.time[worstDay])) + ".</b> Thunderstorms with hail or damaging gusts are in the forecast. Park vehicles inside, photograph your roof beforehand, and book a free inspection after the storm passes.";
    }
  }

  function renderAlerts(el, data) {
    var feats = (data && data.features) || [];
    if (!feats.length) {
      el.className = "alert-box";
      el.innerHTML = "<h3>✅ No active National Weather Service alerts for Katy</h3><p style='margin:0;color:var(--muted)'>Checked " +
        new Date().toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" }) + ". This box updates every time the page loads.</p>";
      return;
    }
    el.className = "alert-box active";
    el.innerHTML = feats.slice(0, 4).map(function (f) {
      var p = f.properties;
      return "<h3>⚠️ " + esc(p.event) + "</h3><p style='margin:0 0 6px'>" + esc(p.headline) + "</p>" +
        "<p style='margin:0 0 14px;color:var(--muted);font-size:.9rem'>Until " + esc(new Date(p.ends || p.expires).toLocaleString("en-US", { weekday: "short", hour: "numeric", minute: "2-digit" })) + " · Source: NWS</p>";
    }).join("");
  }

  var mini = document.querySelector("[data-wx-mini]");
  var full = document.querySelector("[data-wx-forecast]");
  var cur = document.querySelector("[data-wx-current]");
  var alerts = document.querySelector("[data-wx-alerts]");
  if (!mini && !full && !cur) return;

  function getJSON(url, opts) {
    // Give up after 10s so a slow API never leaves "Loading…" on screen.
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
    if (mini) renderMini(mini, w);
    if (cur) renderCurrent(cur, w);
    if (full) renderForecast(full, w);
  }).catch(function () {
    [mini, cur, full].forEach(function (el) {
      if (!el) return;
      var link = "<a href='https://forecast.weather.gov/MapClick.php?lat=" + LAT + "&lon=" + LON + "' rel='noopener' target='_blank' style='color:inherit'>National Weather Service forecast for Katy</a>";
      el.innerHTML = el === mini
        ? "<div class='eyebrow' style='color:var(--gold)'>Katy, TX weather</div><div class='wx-now'><div class='ic'>⛅</div><div><div style='font-family:var(--head);font-size:1.4rem;font-weight:800'>Live data is reloading</div>" +
          "<div style='color:#aab8cb'>Open the full forecast or check the " + link + ".</div></div></div><a class='btn btn-sm btn-light' style='margin-top:18px;width:100%' href='/weather/'>Katy 7-day forecast</a>"
        : "<p style='grid-column:1/-1'>Live weather is temporarily unavailable. Refresh in a moment, or see the " + link + ".</p>";
    });
  });

  if (alerts) {
    getJSON(ALERTS, { headers: { Accept: "application/geo+json" } })
      .then(function (d) { renderAlerts(alerts, d); })
      .catch(function () { alerts.innerHTML = "<p style='margin:0'>Alert feed unavailable — check <a href='https://www.weather.gov/hgx/' target='_blank' rel='noopener'>weather.gov/hgx</a>.</p>"; });
  }
})();
