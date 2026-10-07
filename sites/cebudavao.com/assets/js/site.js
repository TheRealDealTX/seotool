/* cebudavao.com — site script (no dependencies) */
(function () {
  "use strict";
  var d = document, root = d.documentElement;
  root.classList.add("js");
  var $ = function (s, el) { return (el || d).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || d).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]; }); };
  var store = {
    get: function (k) { try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var peso = function (n) { return "₱" + Math.round(n).toLocaleString("en-PH"); };

  /* ---------- chrome ---------- */
  var tog = $(".nav-toggle"), nav = $("#primary-nav");
  if (tog) tog.addEventListener("click", function () {
    var o = nav.classList.toggle("open"); tog.setAttribute("aria-expanded", o);
  });
  $$("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
      root.dataset.theme = dark ? "light" : "dark";
      try { localStorage.setItem("cd-theme", root.dataset.theme); } catch (e) {}
    });
  });
  var dt = $("[data-phdate]");
  if (dt) dt.textContent = new Date().toLocaleDateString("en-PH", { timeZone: "Asia/Manila", weekday: "long", year: "numeric", month: "long", day: "numeric" });
  var bar = $("[data-progress]");
  if (bar) addEventListener("scroll", function () {
    var h = d.body.scrollHeight - innerHeight; bar.style.width = (h > 0 ? Math.min(100, scrollY / h * 100) : 0) + "%";
  }, { passive: true });
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      (navigator.clipboard ? navigator.clipboard.writeText(b.dataset.copy) : Promise.reject()).then(function () {
        b.setAttribute("aria-label", "Link copied"); b.style.borderColor = "var(--sea)";
      }, function () { prompt("Copy this link:", b.dataset.copy); });
    });
  });
  $$("[data-print]").forEach(function (b) { b.addEventListener("click", function () { print(); }); });

  /* ---------- ajax forms ---------- */
  $$("form[data-ajax-form]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", f), btn = $("button[type=submit]", f);
      btn.disabled = true; msg.className = "form-msg"; msg.textContent = "Sending…";
      fetch(f.action, { method: "POST", body: new FormData(f) }).then(function (r) { return r.json(); }).then(function (j) {
        msg.textContent = j.ok ? j.message : j.error; msg.classList.add(j.ok ? "ok" : "err");
        if (j.ok) f.reset();
      }).catch(function () { msg.textContent = "Sorry, that didn't go through. Please try again or email us."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; });
    });
  });

  /* ---------- weather (Open-Meteo) ---------- */
  var CITIES = {
    "cebu-city": ["Cebu City", 10.3157, 123.8854], "davao-city": ["Davao City", 7.1907, 125.4553],
    "lapu-lapu-city": ["Lapu-Lapu (Mactan)", 10.3103, 123.9494], "manila": ["Manila", 14.5995, 120.9842],
    "baguio": ["Baguio", 16.4023, 120.596], "boracay": ["Boracay", 11.9674, 121.9248], "bohol": ["Bohol", 9.6475, 123.8556],
    "siargao": ["Siargao", 9.7868, 126.1569], "el-nido": ["El Nido", 11.1784, 119.3923], "cagayan-de-oro": ["Cagayan de Oro", 8.4542, 124.6319],
    "general-santos": ["General Santos", 6.1164, 125.1716], "iloilo-city": ["Iloilo City", 10.7202, 122.5621]
  };
  var WMO = {
    0: ["☀️", "Clear sky"], 1: ["🌤️", "Mostly clear"], 2: ["⛅", "Partly cloudy"], 3: ["☁️", "Overcast"], 45: ["🌫️", "Fog"], 48: ["🌫️", "Fog"],
    51: ["🌦️", "Light drizzle"], 53: ["🌦️", "Drizzle"], 55: ["🌧️", "Heavy drizzle"], 61: ["🌦️", "Light rain"], 63: ["🌧️", "Rain"], 65: ["🌧️", "Heavy rain"],
    80: ["🌦️", "Rain showers"], 81: ["🌧️", "Heavy showers"], 82: ["⛈️", "Violent showers"], 95: ["⛈️", "Thunderstorm"], 96: ["⛈️", "Thunderstorm, hail"], 99: ["⛈️", "Severe thunderstorm"]
  };
  var wmo = function (c) { return WMO[c] || ["🌡️", "—"]; };
  var unit = store.get("cd-unit") || "c";
  var T = function (c) { return Math.round(unit === "f" ? c * 9 / 5 + 32 : c) + "°"; };
  var cache = {};
  function wx(lat, lon, key) {
    key = key || lat + "," + lon;
    if (cache[key]) return cache[key];
    var ss = null;
    try { ss = JSON.parse(sessionStorage.getItem("wx-" + key)); } catch (e) {}
    if (ss && Date.now() - ss.t < 30 * 60e3) return (cache[key] = Promise.resolve(ss.d));
    var url = "https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon +
      "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m,wind_direction_10m,precipitation,is_day" +
      "&hourly=temperature_2m,precipitation_probability,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,uv_index_max,sunrise,sunset,wind_speed_10m_max" +
      "&timezone=Asia%2FManila&forecast_days=7";
    return (cache[key] = fetch(url).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      try { sessionStorage.setItem("wx-" + key, JSON.stringify({ t: Date.now(), d: j })); } catch (e) {}
      return j;
    }));
  }
  function multiNow(keys) {
    var lats = keys.map(function (k) { return CITIES[k][1]; }).join(","), lons = keys.map(function (k) { return CITIES[k][2]; }).join(",");
    var ck = "multi-" + keys.join(",");
    try { var ss = JSON.parse(sessionStorage.getItem(ck)); if (ss && Date.now() - ss.t < 20 * 60e3) return Promise.resolve(ss.d); } catch (e) {}
    return fetch("https://api.open-meteo.com/v1/forecast?latitude=" + lats + "&longitude=" + lons + "&current=temperature_2m,weather_code&daily=temperature_2m_max,temperature_2m_min&timezone=Asia%2FManila&forecast_days=1")
      .then(function (r) { return r.json(); }).then(function (j) {
        j = Array.isArray(j) ? j : [j];
        try { sessionStorage.setItem(ck, JSON.stringify({ t: Date.now(), d: j })); } catch (e) {}
        return j;
      });
  }
  var day = function (s, opt) { return new Date(s + "T12:00:00+08:00").toLocaleDateString("en-PH", opt || { weekday: "short" }); };

  function renderCard(el) {
    var k = el.dataset.wxCard, c = CITIES[k];
    wx(c[1], c[2], k).then(function (j) {
      var cur = j.current, w = wmo(cur.weather_code), dl = j.daily, days = "";
      for (var i = 1; i < 5; i++) days += "<div>" + day(dl.time[i]) + "<br>" + wmo(dl.weather_code[i])[0] + "<br>" + T(dl.temperature_2m_max[i]) + "</div>";
      el.innerHTML = '<h3 class="widget-title">Weather · ' + esc(c[0]) + '</h3><div class="wx-card-in"><span class="wx-ico">' + w[0] + '</span><div><div class="wx-big">' + T(cur.temperature_2m) +
        '</div><div class="wx-sub">' + w[1] + " · feels " + T(cur.apparent_temperature) + "<br>Rain chance today " + (dl.precipitation_probability_max[0] || 0) + "%</div></div></div>" +
        '<div class="wx-mini-days">' + days + '</div><p class="widget-foot"><a href="/weather/' + k + '/">Full ' + esc(c[0]) + " forecast →</a></p>";
    }).catch(function () { el.innerHTML = '<p class="wx-loading">Weather unavailable right now. <a href="/weather/">Try the forecast page</a>.</p>'; });
  }
  $$("[data-wx-card]").forEach(renderCard);

  function renderStrip(el) {
    var keys = el.dataset.wxStrip.split(",").filter(function (k) { return CITIES[k]; });
    multiNow(keys).then(function (arr) {
      el.innerHTML = keys.map(function (k, i) {
        var j = arr[i]; if (!j || !j.current) return "";
        var w = wmo(j.current.weather_code);
        return '<a class="wx-tile" href="/weather/' + k + '/"><span class="wx-ico">' + w[0] + '</span><span><b>' + T(j.current.temperature_2m) + "</b>" + esc(CITIES[k][0]) +
          "<br>" + T(j.daily.temperature_2m_max[0]) + " / " + T(j.daily.temperature_2m_min[0]) + "</span></a>";
      }).join("");
    }).catch(function () { el.innerHTML = '<p class="muted">Live weather is unavailable right now.</p>'; });
  }
  $$("[data-wx-strip]").forEach(renderStrip);

  var mini = $("[data-wxmini]");
  if (mini) multiNow(["cebu-city", "davao-city"]).then(function (a) {
    mini.innerHTML = "Cebu <b>" + T(a[0].current.temperature_2m) + "</b> · Davao <b>" + T(a[1].current.temperature_2m) + "</b>";
  }).catch(function () {});

  function renderFull(el, k, lat, lon, name) {
    el.innerHTML = '<p class="wx-loading">Loading forecast…</p>';
    wx(lat, lon, k).then(function (j) {
      var c = j.current, w = wmo(c.weather_code), dl = j.daily, h = j.hourly;
      var now = Date.now(), start = 0;
      for (var i = 0; i < h.time.length; i++) { if (new Date(h.time[i] + ":00+08:00").getTime() >= now - 3600e3) { start = i; break; } }
      var hours = "";
      for (i = start; i < Math.min(start + 24, h.time.length); i++) {
        var p = h.precipitation_probability[i] || 0;
        hours += '<div class="wx-hour"><div>' + h.time[i].slice(11, 16) + "</div><div>" + wmo(h.weather_code[i])[0] + "</div><b>" + T(h.temperature_2m[i]) +
          '</b><span class="rain" title="Rain chance ' + p + '%"><i style="height:' + p + '%"></i></span><small>' + p + "%</small></div>";
      }
      var lo = Math.min.apply(null, dl.temperature_2m_min), hi = Math.max.apply(null, dl.temperature_2m_max), days = "";
      for (i = 0; i < dl.time.length; i++) {
        var l = (dl.temperature_2m_min[i] - lo) / (hi - lo || 1) * 100, r = (dl.temperature_2m_max[i] - lo) / (hi - lo || 1) * 100;
        days += '<div class="wx-day"><span>' + (i === 0 ? "Today" : day(dl.time[i], { weekday: "short", month: "short", day: "numeric" })) + "</span><span>" + wmo(dl.weather_code[i])[0] +
          "</span><span>" + T(dl.temperature_2m_min[i]) + " – <b>" + T(dl.temperature_2m_max[i]) + "</b> · 💧" + (dl.precipitation_probability_max[i] || 0) + "% · " + (dl.precipitation_sum[i] || 0).toFixed(1) + " mm" +
          '</span><span class="bar" style="margin-left:' + l * 0.9 + "%;margin-right:" + (100 - r) * 0.9 + '%"></span></div>';
      }
      var dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
      el.innerHTML = '<h2 class="sr">' + esc(name) + " weather now</h2>" +
        '<div class="wx-now"><span class="wx-ico">' + w[0] + '</span><div><div class="wx-big">' + T(c.temperature_2m) + "</div><div>" + w[1] + " in <b>" + esc(name) + "</b> · feels like " + T(c.apparent_temperature) + "</div></div></div>" +
        '<div class="wx-stats"><div>Humidity<b>' + c.relative_humidity_2m + "%</b></div><div>Wind<b>" + Math.round(c.wind_speed_10m) + " km/h " + dirs[Math.round(c.wind_direction_10m / 45) % 8] +
        "</b></div><div>Rain today<b>" + (dl.precipitation_sum[0] || 0).toFixed(1) + " mm</b></div><div>UV index max<b>" + Math.round(dl.uv_index_max[0] || 0) +
        "</b></div><div>Sunrise<b>" + dl.sunrise[0].slice(11) + "</b></div><div>Sunset<b>" + dl.sunset[0].slice(11) + "</b></div></div>" +
        "<h3>Next 24 hours</h3><div class=\"wx-hours\">" + hours + "</div><h3>7-day forecast</h3><div class=\"wx-days\">" + days + "</div>" +
        '<p class="tool-note">Updated ' + new Date().toLocaleTimeString("en-PH", { timeZone: "Asia/Manila", hour: "numeric", minute: "2-digit" }) + " PHT · Model forecast, not an official warning.</p>";
    }).catch(function () { el.innerHTML = '<p class="wx-loading">Forecast unavailable right now — please try again shortly. Official forecasts: <a href="https://www.pagasa.dost.gov.ph/">PAGASA</a>.</p>'; });
  }
  $$("[data-wx-app]").forEach(function (app) {
    var full = $("[data-wx-full]", app), sel = $("[data-wx-select]", app);
    var show = function (k) { var c = CITIES[k]; full.dataset.wxFull = k; renderFull(full, k, c[1], c[2], c[0]); };
    if (sel) {
      var saved = store.get("cd-city"); if (saved && CITIES[saved]) sel.value = saved;
      sel.addEventListener("change", function () { store.set("cd-city", sel.value); show(sel.value); });
      show(sel.value);
    } else show(full.dataset.wxFull);
    var loc = $("[data-wx-locate]", app);
    if (loc) loc.addEventListener("click", function () {
      if (!navigator.geolocation) return;
      loc.textContent = "Locating…";
      navigator.geolocation.getCurrentPosition(function (p) {
        var la = p.coords.latitude.toFixed(3), lo = p.coords.longitude.toFixed(3);
        renderFull(full, "here-" + la + lo, la, lo, "your location"); loc.textContent = "Use my location";
      }, function () { loc.textContent = "Location blocked"; });
    });
    $$("[data-unit]", app).forEach(function (b) {
      b.setAttribute("aria-pressed", b.dataset.unit === unit);
      b.addEventListener("click", function () {
        unit = b.dataset.unit; store.set("cd-unit", unit);
        $$("[data-unit]", app).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        sel ? show(sel.value) : show(full.dataset.wxFull);
        $$("[data-wx-strip]").forEach(renderStrip);
      });
    });
  });

  /* ---------- news wire ---------- */
  var ago = function (iso) {
    var m = Math.round((Date.now() - new Date(iso)) / 60000);
    return m < 60 ? m + " min ago" : m < 1440 ? Math.round(m / 60) + " hr ago" : Math.round(m / 1440) + " d ago";
  };
  function loadNews(el, topic, n) {
    var ul = $(".wire-list", el);
    fetch("/api/news.php?topic=" + topic).then(function (r) { return r.json(); }).then(function (j) {
      if (!j.items || !j.items.length) throw 0;
      ul.innerHTML = j.items.slice(0, n || 8).map(function (it) {
        return '<li><a href="' + esc(it.link) + '" target="_blank" rel="noopener nofollow">' + esc(it.title) + "</a><small>" + esc(it.source) + " · " + ago(it.date) + "</small></li>";
      }).join("");
    }).catch(function () { ul.innerHTML = '<li class="muted">Headlines are unavailable right now. Try <a href="/news/superbalita-cebu/">Cebu news sources</a> or <a href="/news/davao-sun-star/">Davao news sources</a>.</li>'; });
  }
  $$("[data-news]").forEach(function (el) { loadNews(el, el.dataset.news); });
  $$("[data-tabs]").forEach(function (t) {
    var wire = $("[data-news-tabs]", t);
    $$("[data-tab]", t).forEach(function (b) {
      b.addEventListener("click", function () {
        $$("[data-tab]", t).forEach(function (x) { x.setAttribute("aria-selected", x === b); });
        $(".wire-list", wire).innerHTML = '<li class="muted">Loading…</li>'; loadNews(wire, b.dataset.tab);
      });
    });
  });

  /* ---------- search ---------- */
  var idx = null;
  var getIdx = function () { return idx || (idx = fetch("/assets/data/search.json").then(function (r) { return r.json(); })); };
  function search(q, list) {
    q = q.trim().toLowerCase();
    if (q.length < 2) { list.innerHTML = ""; return; }
    getIdx().then(function (data) {
      var terms = q.split(/\s+/);
      var res = data.map(function (x) {
        var hay = (x.t + " " + x.e + " " + x.k + " " + x.c).toLowerCase(), s = 0;
        terms.forEach(function (t) { if (hay.indexOf(t) < 0) s -= 100; else s += (x.t.toLowerCase().indexOf(t) >= 0 ? 5 : 1); });
        return [s, x];
      }).filter(function (a) { return a[0] > 0; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 20);
      list.innerHTML = res.length ? res.map(function (a) { var x = a[1]; return '<li><a href="' + x.u + '">' + esc(x.t) + "</a><small>" + esc(x.c) + " · " + esc(x.e) + "</small></li>"; }).join("")
        : '<li class="muted">No results. Try another word — e.g. "Samal", "lechon" or "weather".</li>';
    });
  }
  var ov = $("[data-search-overlay]");
  $$("[data-search-open]").forEach(function (a) {
    a.addEventListener("click", function (e) { e.preventDefault(); ov.hidden = false; $("[data-search-input]").focus(); });
  });
  if (ov) {
    $("[data-search-close]").addEventListener("click", function () { ov.hidden = true; });
    ov.addEventListener("click", function (e) { if (e.target === ov) ov.hidden = true; });
    addEventListener("keydown", function (e) { if (e.key === "Escape") ov.hidden = true; });
    $("[data-search-input]").addEventListener("input", function (e) { search(e.target.value, $("[data-search-results]")); });
  }
  var sp = $("[data-search-page]");
  if (sp) {
    var q0 = new URLSearchParams(location.search).get("q") || "";
    sp.value = q0; search(q0, $("[data-search-results-page]"));
    sp.addEventListener("input", function () { search(sp.value, $("[data-search-results-page]")); });
  }

  /* ---------- tools ---------- */
  var TOOLS = {};
  var json = function (u) { return fetch(u).then(function (r) { return r.json(); }); };

  // Currency converter
  var fx = null;
  var rates = function () {
    if (fx) return fx;
    var s = store.get("cd-fx");
    if (s && Date.now() - s.t < 6 * 3600e3) return (fx = Promise.resolve(s.d));
    return (fx = json("https://open.er-api.com/v6/latest/PHP").then(function (j) { if (j.result !== "success") throw 0; store.set("cd-fx", { t: Date.now(), d: j }); return j; }));
  };
  var CUR = [["PHP", "Philippine peso"], ["USD", "US dollar"], ["EUR", "Euro"], ["JPY", "Japanese yen"], ["KRW", "South Korean won"], ["GBP", "British pound"], ["AUD", "Australian dollar"],
    ["CAD", "Canadian dollar"], ["SGD", "Singapore dollar"], ["HKD", "Hong Kong dollar"], ["CNY", "Chinese yuan"], ["AED", "UAE dirham"], ["SAR", "Saudi riyal"], ["QAR", "Qatari riyal"], ["KWD", "Kuwaiti dinar"], ["TWD", "Taiwan dollar"]];
  TOOLS.currency = function (el) {
    var opt = function (sel) { return CUR.map(function (c) { return '<option value="' + c[0] + '"' + (c[0] === sel ? " selected" : "") + ">" + c[0] + " — " + c[1] + "</option>"; }).join(""); };
    el.innerHTML = '<div class="tool-row"><div><label for="fx-a">Amount</label><input id="fx-a" type="number" min="0" step="any" value="100"></div>' +
      '<div><label for="fx-f">From</label><select id="fx-f">' + opt("USD") + '</select></div><div><button class="btn btn-ghost" type="button" data-swap aria-label="Swap currencies">⇄ Swap</button></div>' +
      '<div><label for="fx-t">To</label><select id="fx-t">' + opt("PHP") + '</select></div></div><div class="tool-out" aria-live="polite">…</div><div class="fx-table"></div><p class="tool-note"></p>';
    var a = $("#fx-a", el), f = $("#fx-f", el), t = $("#fx-t", el), out = $(".tool-out", el), note = $(".tool-note", el), tbl = $(".fx-table", el);
    function calc() {
      rates().then(function (j) {
        var r = j.rates, v = parseFloat(a.value) || 0, res = v / r[f.value] * r[t.value];
        out.textContent = v.toLocaleString() + " " + f.value + " = " + res.toLocaleString(undefined, { maximumFractionDigits: res < 1 ? 4 : 2 }) + " " + t.value;
        var base = f.value === "PHP" ? t.value : f.value;
        tbl.innerHTML = '<div class="table-wrap"><table><thead><tr><th>' + base + "</th><th>PHP</th></tr></thead><tbody>" + [1, 10, 50, 100, 500, 1000].map(function (n) {
          return "<tr><td>" + n.toLocaleString() + " " + base + "</td><td>" + peso(n / r[base]).replace(/^₱/, "₱") + "</td></tr>"; }).join("") + "</tbody></table></div>";
        note.innerHTML = "Mid-market reference rate, updated " + esc(j.time_last_update_utc.slice(0, 16)) + ' UTC. <a href="https://www.exchangerate-api.com" target="_blank" rel="noopener">Rates by ExchangeRate-API</a>. Banks and remittance centres add a margin.';
      }).catch(function () { out.textContent = "Rates unavailable right now."; });
    }
    [a, f, t].forEach(function (x) { x.addEventListener("input", calc); });
    $("[data-swap]", el).addEventListener("click", function () { var x = f.value; f.value = t.value; t.value = x; calc(); });
    calc();
  };
  var fxm = $("[data-fxmini]");
  if (fxm) rates().then(function (j) { fxm.textContent = "$1 = ₱" + (1 / j.rates.USD).toFixed(2); }).catch(function () {});

  // Trip budget calculator
  TOOLS.budget = function (el) {
    var DEST = { "Cebu": 1, "Davao": 0.95, "Bohol": 1.05, "Boracay": 1.35, "Siargao": 1.2, "El Nido / Coron": 1.3, "Camiguin": 0.95 };
    var STY = { budget: { room: 1200, food: 650, move: 350, l: "Backpacker / budget" }, mid: { room: 3500, food: 1500, move: 900, l: "Mid-range" }, lux: { room: 10000, food: 3500, move: 2500, l: "Comfort / luxury" } };
    var ACT = [["Island hopping tour", 1800], ["Canyoneering / waterfalls tour", 1800], ["Diving (per dive)", 2500], ["Whale shark or wildlife tour", 1200], ["Day tour with van", 2500], ["Spa / massage", 800]];
    el.innerHTML = '<div class="tool-row"><div><label for="b-d">Destination</label><select id="b-d">' + Object.keys(DEST).map(function (k) { return "<option>" + k + "</option>"; }).join("") +
      '</select></div><div><label for="b-n">Nights</label><input id="b-n" type="number" min="1" max="60" value="4"></div><div><label for="b-p">Travellers</label><input id="b-p" type="number" min="1" max="20" value="2"></div>' +
      '<div><label for="b-s">Style</label><select id="b-s">' + Object.keys(STY).map(function (k) { return '<option value="' + k + '"' + (k === "mid" ? " selected" : "") + ">" + STY[k].l + "</option>"; }).join("") + "</select></div></div>" +
      '<p><b>Activities (per person, once)</b></p><div class="check-row">' + ACT.map(function (x, i) { return '<label><input type="checkbox" value="' + i + '"> ' + x[0] + "</label>"; }).join("") + "</div>" +
      '<div class="tool-out" aria-live="polite"></div><div class="budget-break"></div><p class="tool-note">Rough planning estimate in Philippine pesos, excluding flights. Rooms are priced per room (two travellers share). Prices vary a lot by season — confirm before you book.</p>';
    function calc() {
      var m = DEST[$("#b-d", el).value], n = Math.max(1, +$("#b-n", el).value || 1), p = Math.max(1, +$("#b-p", el).value || 1), s = STY[$("#b-s", el).value];
      var rooms = Math.ceil(p / 2), room = s.room * m * rooms * n, food = s.food * m * p * (n + 1), move = s.move * m * p * (n + 1), act = 0;
      $$(".check-row input:checked", el).forEach(function (c) { act += ACT[+c.value][1] * m * p; });
      var tot = room + food + move + act;
      $(".tool-out", el).textContent = peso(tot * 0.85) + " – " + peso(tot * 1.2);
      $(".budget-break", el).innerHTML = [["Accommodation", room], ["Food", food], ["Local transport", move], ["Activities", act], ["Per person", tot / p], ["Per person / day", tot / p / (n + 1)]]
        .map(function (x) { return "<div>" + x[0] + "<b>" + peso(x[1]) + "</b></div>"; }).join("");
      rates().then(function (j) { $(".tool-out", el).insertAdjacentHTML("beforeend", ' <small class="muted">(≈ $' + Math.round(tot * j.rates.USD).toLocaleString() + ")</small>"); }).catch(function () {});
    }
    $$("input,select", el).forEach(function (x) { x.addEventListener("input", calc); x.addEventListener("change", calc); });
    calc();
  };

  // Bisaya dictionary + flashcards
  TOOLS.bisaya = function (el, compact) {
    json("/assets/data/bisaya.json").then(function (data) {
      var cats = ["all"].concat(data.map(function (x) { return x.c; }).filter(function (v, i, a) { return a.indexOf(v) === i; }));
      el.innerHTML = (compact ? "" : '<h3 class="widget-title">Search</h3>') + '<label class="sr" for="bd-q">Search words</label><input id="bd-q" type="search" placeholder="Type Bisaya, Tagalog or English — e.g. delicious, salamat, where">' +
        '<div class="chips">' + cats.map(function (c) { return '<button type="button" data-c="' + c + '" aria-pressed="' + (c === "all") + '">' + c + "</button>"; }).join("") + "</div>" +
        '<ul class="dict-list" aria-live="polite"></ul>' + (compact ? "" : '<h3 class="widget-title" style="margin-top:18px">Flashcards</h3><div class="flash"><div class="flash-card" tabindex="0" role="button" aria-label="Flip card"><div></div><div></div></div></div><p style="text-align:center"><button class="btn btn-sm" type="button" data-next>Next card</button></p>');
      var q = $("#bd-q", el), cat = "all", list = $(".dict-list", el);
      function draw() {
        var s = q.value.trim().toLowerCase();
        var res = data.filter(function (x) { return (cat === "all" || x.c === cat) && (!s || (x.b + " " + x.t + " " + x.e).toLowerCase().indexOf(s) >= 0); });
        list.innerHTML = '<li class="muted" style="font-size:.78rem"><span>BISAYA</span><span>TAGALOG</span><span>ENGLISH</span></li>' + res.slice(0, compact ? 12 : 200).map(function (x) {
          return "<li><b>" + esc(x.b) + "</b><span>" + esc(x.t) + "</span><span>" + esc(x.e) + "</span>" + (x.n ? "<small>" + esc(x.n) + "</small>" : "") + "</li>"; }).join("") +
          (res.length ? "" : '<li class="muted">No match — try a shorter word.</li>');
      }
      q.addEventListener("input", draw);
      $$("[data-c]", el).forEach(function (b) { b.addEventListener("click", function () { cat = b.dataset.c; $$("[data-c]", el).forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); draw(); }); });
      draw();
      var card = $(".flash-card", el);
      if (card) {
        var next = function () { var x = data[Math.floor(Math.random() * data.length)]; card.classList.remove("flip"); card.children[0].textContent = x.b; card.children[1].innerHTML = "<span>" + esc(x.e) + "<br><small>Tagalog: " + esc(x.t) + "</small></span>"; };
        card.addEventListener("click", function () { card.classList.toggle("flip"); });
        card.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); card.classList.toggle("flip"); } });
        $("[data-next]", el).addEventListener("click", next); next();
      }
    });
  };

  // Fish names
  TOOLS.fish = function (el, compact) {
    json("/assets/data/fish.json").then(function (data) {
      el.innerHTML = '<label class="sr" for="fi-q">Search fish</label><input id="fi-q" type="search" placeholder="e.g. lapu-lapu, milkfish, tulingan, tuna">' + '<ul class="dict-list" aria-live="polite"></ul>';
      var q = $("#fi-q", el), list = $(".dict-list", el);
      function draw() {
        var s = q.value.trim().toLowerCase();
        var res = data.filter(function (x) { return !s || (x.b + " " + x.t + " " + x.e + " " + x.s).toLowerCase().indexOf(s) >= 0; });
        list.innerHTML = '<li class="muted" style="font-size:.78rem"><span>BISAYA</span><span>TAGALOG</span><span>ENGLISH</span></li>' + res.slice(0, compact ? 10 : 100).map(function (x) {
          return "<li><b>" + esc(x.b) + "</b><span>" + esc(x.t) + "</span><span>" + esc(x.e) + "</span><small><i>" + esc(x.s) + "</i> · " + esc(x.n) + "</small></li>"; }).join("") || '<li class="muted">No match.</li>';
      }
      q.addEventListener("input", draw); draw();
    });
  };

  // Distance between cities
  TOOLS.distance = function (el) {
    json("/assets/data/cities.json").then(function (cs) {
      var opts = function (sel) { return cs.map(function (c, i) { return '<option value="' + i + '"' + (c.n === sel ? " selected" : "") + ">" + esc(c.n) + "</option>"; }).join(""); };
      el.innerHTML = '<div class="tool-row"><div><label for="ds-a">From</label><select id="ds-a">' + opts("Cebu City") + '</select></div><div><label for="ds-b">To</label><select id="ds-b">' + opts("Davao City") + "</select></div></div>" +
        '<div class="tool-out" aria-live="polite"></div><div class="budget-break"></div><p class="tool-note">Straight-line (great-circle) distance. Road distance is usually 20–50% longer, and most inter-island trips need a ferry or RoRo, which adds port time. Flight time is approximate gate-to-gate airborne time for a direct route.</p>';
      function calc() {
        var a = cs[$("#ds-a", el).value], b = cs[$("#ds-b", el).value], R = 6371, rad = Math.PI / 180;
        var x = Math.sin((b.la - a.la) * rad / 2) ** 2 + Math.cos(a.la * rad) * Math.cos(b.la * rad) * Math.sin((b.lo - a.lo) * rad / 2) ** 2;
        var km = 2 * R * Math.asin(Math.sqrt(x));
        var hm = function (h) { var m = Math.round(h * 60); return (m >= 60 ? Math.floor(m / 60) + " h " : "") + (m % 60) + " min"; };
        $(".tool-out", el).textContent = Math.round(km).toLocaleString() + " km (" + Math.round(km * 0.621).toLocaleString() + " miles)";
        $(".budget-break", el).innerHTML = "<div>Flight (direct)<b>" + (km < 120 ? "—" : hm(km / 600 + 0.35)) + "</b></div><div>Road estimate<b>" + Math.round(km * 1.35).toLocaleString() + " km</b></div><div>Driving time (no ferries)<b>" + hm(km * 1.35 / 40) + "</b></div><div>Nautical miles<b>" + Math.round(km / 1.852).toLocaleString() + "</b></div>";
      }
      $$("select", el).forEach(function (s) { s.addEventListener("change", calc); }); calc();
    });
  };

  // Festival calendar
  var nthSunday = function (y, m, n) { var dt = new Date(y, m, 1); var add = (7 - dt.getDay()) % 7; return new Date(y, m, 1 + add + 7 * (n - 1)); };
  var lastSunday = function (y, m) { var dt = new Date(y, m + 1, 0); dt.setDate(dt.getDate() - dt.getDay()); return dt; };
  var CNY = { 2026: [1, 17], 2027: [1, 6], 2028: [0, 26], 2029: [1, 13] }, EASTER = { 2026: [3, 5], 2027: [2, 28], 2028: [3, 16], 2029: [3, 1] };
  var FESTS = [
    ["Sinulog Festival", "Cebu City", "cebu", function (y) { return nthSunday(y, 0, 3); }, "Third Sunday of January — grand parade day", "/festivals/what-makes-the-sinulog-2012-festival-the-number-one-festival-in-the-philippines/"],
    ["Ati-Atihan", "Kalibo, Aklan", "other", function (y) { return nthSunday(y, 0, 3); }, "Climax on the third Sunday of January", ""],
    ["Dinagyang", "Iloilo City", "other", function (y) { return nthSunday(y, 0, 4); }, "Fourth Sunday of January", ""],
    ["Chinese New Year", "Cebu, Davao & nationwide", "both", function (y) { var c = CNY[y]; return c ? new Date(y, c[0], c[1]) : null; }, "Lunar New Year", "/events/kung-hei-fat-choy/"],
    ["EDSA People Power anniversary", "Nationwide", "other", function (y) { return new Date(y, 1, 25); }, "February 25", "/events/what-is-edsa-revolution/"],
    ["Araw ng Dabaw", "Davao City", "davao", function (y) { return new Date(y, 2, 16); }, "Davao City's founding anniversary, March 16", ""],
    ["Holy Week (Good Friday)", "Nationwide", "both", function (y) { var e = EASTER[y]; return e ? new Date(y, e[0], e[1] - 2) : null; }, "Many businesses close Thursday–Saturday", ""],
    ["Pahiyas Festival", "Lucban, Quezon", "other", function (y) { return new Date(y, 4, 15); }, "May 15", ""],
    ["Independence Day", "Nationwide", "both", function (y) { return new Date(y, 5, 12); }, "June 12", ""],
    ["Kadayawan Festival", "Davao City", "davao", function (y) { return nthSunday(y, 7, 3); }, "Third week of August (approx.)", "/festivals/whats-so-interesting-about-the-kadayawan-festival/"],
    ["MassKara Festival", "Bacolod", "other", function (y) { return nthSunday(y, 9, 4); }, "Fourth Sunday of October (approx.)", ""],
    ["Lanzones Festival", "Camiguin", "other", function (y) { return lastSunday(y, 9); }, "Late October (approx.)", "/travel/camiguin-island-guide/"],
    ["All Saints' Day (Undas)", "Nationwide", "both", function (y) { return new Date(y, 10, 1); }, "November 1", ""],
    ["Simbang Gabi begins", "Nationwide", "both", function (y) { return new Date(y, 11, 16); }, "Dawn Masses Dec 16–24", ""],
    ["Metro Manila Film Festival", "Cinemas nationwide", "both", function (y) { return new Date(y, 11, 25); }, "Opens December 25", "/entertainment/metro-manila-film-festival-guide/"],
    ["Christmas Day", "Nationwide", "both", function (y) { return new Date(y, 11, 25); }, "December 25", ""],
    ["Rizal Day", "Nationwide", "both", function (y) { return new Date(y, 11, 30); }, "December 30", ""]
  ];
  TOOLS.festivals = function (el, compact) {
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var items = FESTS.map(function (f) {
      var dte = f[3](today.getFullYear()); if (!dte || dte < today) dte = f[3](today.getFullYear() + 1);
      return dte ? { f: f, d: dte, n: Math.round((dte - today) / 864e5) } : null;
    }).filter(Boolean).sort(function (a, b) { return a.n - b.n; });
    el.innerHTML = (compact ? "" : '<div class="chips"><button type="button" aria-pressed="true" data-r="all">All</button><button type="button" aria-pressed="false" data-r="cebu">Cebu</button><button type="button" aria-pressed="false" data-r="davao">Davao</button><button type="button" aria-pressed="false" data-r="other">Elsewhere</button></div>') + '<div class="fest-list"></div>';
    function draw(r) {
      $(".fest-list", el).innerHTML = items.filter(function (x) { return r === "all" || x.f[2] === r || (x.f[2] === "both" && r !== "other"); }).slice(0, compact ? 3 : 50).map(function (x, i) {
        return '<div class="fest"><h4>' + (x.f[5] ? '<a href="' + x.f[5] + '">' + esc(x.f[0]) + "</a>" : esc(x.f[0])) + '</h4><div class="where">' + esc(x.f[1]) + '</div><div class="days">' + (x.n === 0 ? "Today!" : x.n + " days") + "</div><div>" +
          x.d.toLocaleDateString("en-PH", { weekday: "short", month: "long", day: "numeric", year: "numeric" }) + '</div><div class="where">' + esc(x.f[4]) + '</div><button class="btn btn-sm btn-ghost" type="button" data-ics="' + i + '">Add to calendar</button></div>';
      }).join("");
      $$("[data-ics]", el).forEach(function (b) {
        b.addEventListener("click", function () {
          var x = items[+b.dataset.ics], ymd = function (dd) { return dd.getFullYear() + String(dd.getMonth() + 1).padStart(2, "0") + String(dd.getDate()).padStart(2, "0"); };
          var end = new Date(x.d); end.setDate(end.getDate() + 1);
          var ics = "BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//cebudavao.com//festivals//EN\r\nBEGIN:VEVENT\r\nUID:" + ymd(x.d) + "-" + b.dataset.ics + "@cebudavao.com\r\nDTSTAMP:" + ymd(new Date()) + "T000000Z\r\nDTSTART;VALUE=DATE:" + ymd(x.d) + "\r\nDTEND;VALUE=DATE:" + ymd(end) + "\r\nSUMMARY:" + x.f[0] + "\r\nLOCATION:" + x.f[1] + "\r\nDESCRIPTION:" + x.f[4] + " (via cebudavao.com)\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n";
          var a = d.createElement("a"); a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar" })); a.download = x.f[0].replace(/\W+/g, "-").toLowerCase() + ".ics"; a.click();
        });
      });
    }
    $$("[data-r]", el).forEach(function (b) { b.addEventListener("click", function () { $$("[data-r]", el).forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); draw(b.dataset.r); }); });
    draw("all");
  };

  // Destination quiz
  TOOLS.quiz = function (el) {
    json("/assets/data/quiz.json").then(function (qs) {
      qs = qs.sort(function () { return Math.random() - 0.5; }).slice(0, 10);
      var i = 0, score = 0;
      function show() {
        if (i >= qs.length) {
          var best = store.get("cd-quiz-best") || 0; if (score > best) store.set("cd-quiz-best", score);
          el.innerHTML = '<div class="tool-out">You scored ' + score + " / " + qs.length + "</div><p>" + (score >= 8 ? "Certified island expert — daghang salamat!" : score >= 5 ? "Not bad! A few more trips and you'll ace it." : "Time to plan a trip — start with our travel guides.") +
            "</p><p class=\"tool-note\">Your best: " + Math.max(best, score) + '/10</p><button class="btn" type="button" data-again>Play again</button> <a class="btn btn-ghost" href="/category/travel/">Travel guides</a>';
          $("[data-again]", el).addEventListener("click", function () { TOOLS.quiz(el); });
          return;
        }
        var q = qs[i], opts = q.o.slice().sort(function () { return Math.random() - 0.5; });
        el.innerHTML = '<div class="meter"><i style="width:' + (i / qs.length * 100) + '%"></i></div><p class="tool-note">Question ' + (i + 1) + " of " + qs.length + " · Score " + score + "</p>" +
          '<img class="quiz-img" src="/assets/img/photos/' + q.img + '-sm.webp" alt="" onerror="this.remove()"><p class="quiz-q">' + esc(q.q) + '</p><div class="quiz-opts">' +
          opts.map(function (o) { return '<button type="button">' + esc(o) + "</button>"; }).join("") + '</div><p class="quiz-fb" aria-live="polite"></p>';
        $$(".quiz-opts button", el).forEach(function (b) {
          b.addEventListener("click", function () {
            var ok = b.textContent === q.a; if (ok) score++;
            $$(".quiz-opts button", el).forEach(function (x) { x.disabled = true; if (x.textContent === q.a) x.classList.add("ok"); });
            if (!ok) b.classList.add("bad");
            $(".quiz-fb", el).innerHTML = (ok ? "✅ Correct!" : "❌ It's " + esc(q.a) + ".") + ' <button class="btn btn-sm" type="button">Next →</button>';
            $(".quiz-fb button", el).addEventListener("click", function () { i++; show(); });
          });
        });
      }
      show();
    });
  };

  // Packing checklist
  TOOLS.packing = function (el) {
    var L = {
      "Documents & money": ["Passport / valid ID", "eTravel QR code (international trips)", "Printed or offline booking confirmations", "Some cash in small peso bills", "Debit/credit card + backup card", "GCash or Maya set up (if local)"],
      "Clothes": ["Light, quick-dry shirts", "Shorts / light trousers", "Something covering shoulders & knees (churches)", "Swimwear", "Light rain jacket", "Sandals + walking shoes", "Sweater for buses, planes & highlands"],
      "Beach & outdoors": ["Reef-safe sunscreen", "Hat & sunglasses", "Dry bag", "Aqua shoes (for rocky beaches & canyoneering)", "Insect repellent", "Reusable water bottle"],
      "Tech": ["Phone + charger", "Power bank (hand-carry only)", "Universal adapter (Type A/B/C plugs)", "Offline maps downloaded", "Local SIM / eSIM"],
      "Health": ["Prescription medicines", "Anti-diarrhoea & rehydration salts", "Plasters & antiseptic", "Motion-sickness tablets (boats)", "Travel insurance details"],
      "Typhoon season extras": ["Waterproof phone pouch", "Flashlight / headlamp", "Flexible travel dates or refundable bookings", "PAGASA & airline apps or alerts"]
    };
    var saved = store.get("cd-pack") || {};
    el.innerHTML = '<div class="meter"><i></i></div><p class="tool-note" data-count></p>' + Object.keys(L).map(function (g) {
      return '<div class="pack-group"><h4>' + esc(g) + "</h4>" + L[g].map(function (it) { var id = g + "|" + it; return '<label><input type="checkbox" data-id="' + esc(id) + '"' + (saved[id] ? " checked" : "") + "> " + esc(it) + "</label>"; }).join("") + "</div>";
    }).join("") + '<button class="btn btn-sm btn-ghost" type="button" data-reset>Reset</button> <button class="btn btn-sm btn-ghost" type="button" data-print>Print list</button>';
    function upd() {
      var all = $$("input", el), done = all.filter(function (x) { return x.checked; });
      $(".meter i", el).style.width = done.length / all.length * 100 + "%";
      $("[data-count]", el).textContent = done.length + " of " + all.length + " packed";
    }
    $$("input", el).forEach(function (x) { x.addEventListener("change", function () { saved[x.dataset.id] = x.checked; store.set("cd-pack", saved); upd(); }); });
    $("[data-reset]", el).addEventListener("click", function () { saved = {}; store.set("cd-pack", saved); $$("input", el).forEach(function (x) { x.checked = false; }); upd(); });
    $("[data-print]", el).addEventListener("click", function () { print(); });
    upd();
  };

  $$("[data-tool]").forEach(function (el) {
    var fn = TOOLS[el.dataset.tool];
    if (!fn) return;
    var compact = el.dataset.compact === "1";
    if (compact) {
      var foot = $(".widget-foot", el), box = d.createElement("div"); el.insertBefore(box, foot); fn(box, true);
    } else fn(el, false);
  });
})();
