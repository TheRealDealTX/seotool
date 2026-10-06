/* Renter News — shared site script */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function store(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  }

  /* Theme toggle */
  var tbtn = $("[data-theme-toggle]");
  if (tbtn) tbtn.addEventListener("click", function () {
    var dark = doc.dataset.theme ? doc.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    doc.dataset.theme = dark ? "light" : "dark";
    store("rn-theme", doc.dataset.theme);
  });

  /* Mobile menu */
  var menuBtn = $("[data-menu]"), nav = $("#main-nav"), scrim;
  function closeMenu() { nav.classList.remove("is-open"); menuBtn.setAttribute("aria-expanded", "false"); if (scrim) { scrim.remove(); scrim = null; } }
  if (menuBtn && nav) menuBtn.addEventListener("click", function () {
    if (nav.classList.contains("is-open")) return closeMenu();
    nav.classList.add("is-open"); menuBtn.setAttribute("aria-expanded", "true");
    scrim = document.createElement("div"); scrim.className = "nav-scrim"; scrim.addEventListener("click", closeMenu);
    (document.querySelector(".site-header") || document.body).appendChild(scrim);
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && nav && nav.classList.contains("is-open")) closeMenu(); });

  /* Header search */
  var sbtn = $("[data-search-toggle]"), spop = $(".search-pop");
  if (sbtn && spop) sbtn.addEventListener("click", function () {
    if (spop.classList.contains("is-open") && spop.q.value.trim()) return spop.submit();
    spop.classList.toggle("is-open");
    if (spop.classList.contains("is-open")) setTimeout(function () { spop.q.focus(); }, 200);
  });

  /* Scroll: sticky header shadow + reading progress */
  var header = $(".site-header"), prog = $(".progress"), article = $(".article .prose");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 10);
    if (prog && article) {
      var r = article.getBoundingClientRect(), total = r.height - innerHeight * 0.6;
      prog.style.setProperty("--p", Math.max(0, Math.min(1, -r.top / Math.max(total, 1))));
    }
  }
  addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* Reveal on scroll + count up */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-in"); io.unobserve(e.target);
        var n = $("[data-count]", e.target); if (n) countUp(n);
      });
    }, { rootMargin: "0px 0px -40px 0px" });
    $$(".reveal").forEach(function (el, i) { el.style.transitionDelay = (i % 4) * 70 + "ms"; io.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("is-in"); }); }
  function countUp(el) {
    var end = +el.dataset.count, t0 = performance.now();
    (function step(t) { var p = Math.min(1, (t - t0) / 1100); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); })(t0);
  }

  /* Category filter chips (home) */
  var grid = $("[data-filter-grid]");
  $$("[data-filter]").forEach(function (b) {
    b.addEventListener("click", function () {
      $$("[data-filter]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
      var f = b.dataset.filter;
      $$(".card", grid).forEach(function (c) { c.classList.toggle("is-hidden", f !== "all" && c.dataset.cat !== f); });
      if (grid && !$$(".card:not(.is-hidden)", grid).length) location.href = "/news/category/" + f + "/";
    });
  });

  /* Share */
  $$("[data-share]").forEach(function (box) {
    var copy = $("[data-copy]", box), nat = $("[data-native-share]", box);
    if (copy) copy.addEventListener("click", function () {
      (navigator.clipboard ? navigator.clipboard.writeText(box.dataset.url) : Promise.reject()).then(function () {
        copy.classList.add("copied"); setTimeout(function () { copy.classList.remove("copied"); }, 1600);
      }, function () { prompt("Copy this link:", box.dataset.url); });
    });
    if (nat && navigator.share) {
      nat.hidden = false;
      nat.addEventListener("click", function () { navigator.share({ title: box.dataset.title, url: box.dataset.url }).catch(function () {}); });
    }
  });

  /* Contact form */
  var cf = $("[data-contact]");
  if (cf) cf.addEventListener("submit", function (e) {
    e.preventDefault();
    var st = $("[data-form-status]", cf), btn = $("button[type=submit]", cf);
    btn.disabled = true; st.textContent = "Sending…";
    fetch(cf.action, { method: "POST", body: new FormData(cf), headers: { Accept: "application/json" } })
      .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
      .then(function (d) {
        if (d.ok) { cf.reset(); st.textContent = "Thanks! Your message has been sent to the newsroom."; }
        else { st.textContent = d.error || "Sorry, something went wrong. Please email info@renternews.net."; }
      })
      .catch(function () { st.textContent = "Sorry, something went wrong. Please email info@renternews.net."; })
      .then(function () { btn.disabled = false; });
  });

  /* ---------------- Weather (National Weather Service, api.weather.gov) ---------------- */
  // NWS icon codes -> our animated icon kinds
  var NWS_KIND = {
    skc: "sun", few: "sun", hot: "sun", wind_skc: "sun", wind_few: "sun",
    sct: "partly", bkn: "partly", wind_sct: "partly", wind_bkn: "partly",
    ovc: "cloud", wind_ovc: "cloud", cold: "cloud",
    rain: "rain", rain_showers: "rain", rain_showers_hi: "rain", fzra: "rain", rain_fzra: "rain", rain_sleet: "rain",
    tsra: "storm", tsra_sct: "storm", tsra_hi: "storm", tornado: "storm", hurricane: "storm", tropical_storm: "storm",
    snow: "snow", sleet: "snow", blizzard: "snow", rain_snow: "snow", snow_sleet: "snow", snow_fzra: "snow",
    fog: "fog", haze: "fog", smoke: "fog", dust: "fog"
  };
  function wxInfo(iconUrl, text) {
    var m = /\/icons\/land\/(day|night)\/([a-z_]+)/.exec(iconUrl || ""), isDay = !m || m[1] === "day";
    var kind = (m && NWS_KIND[m[2]]) || "cloud";
    if (!isDay && (kind === "sun" || kind === "partly")) kind = kind === "sun" ? "moon" : "partlynight";
    var mood = { sun: "clear", partly: "clear", moon: "night", partlynight: "night", cloud: "cloud", fog: "fog", rain: "rain", snow: "snow", storm: "storm" }[kind];
    return { text: text || "", kind: kind, mood: mood, isDay: isDay };
  }
  function wxIcon(kind) {
    var sun = '<g class="sun-rays" stroke="#ffcf3f" stroke-width="3" stroke-linecap="round"><path d="M32 6v6M32 52v6M6 32h6M52 32h6M13.6 13.6l4.2 4.2M46.2 46.2l4.2 4.2M13.6 50.4l4.2-4.2M46.2 17.8l4.2-4.2"/></g><circle cx="32" cy="32" r="11" fill="#ffcf3f"/>';
    var moon = '<path d="M38 14a18 18 0 1 0 12 30A15 15 0 0 1 38 14z" fill="#f4e7b2"/>';
    var cloud = function (x, y, c) { return '<g class="cloud-a" transform="translate(' + x + ' ' + y + ')"><path d="M14 40h30a10 10 0 0 0 0-20 14 14 0 0 0-27-2A11 11 0 0 0 14 40z" fill="' + (c || "#e9eef6") + '"/></g>'; };
    var s = "";
    switch (kind) {
      case "sun": s = sun; break;
      case "moon": s = moon; break;
      case "partly": s = '<g transform="translate(-8 -8) scale(.85)">' + sun + "</g>" + cloud(4, 8); break;
      case "partlynight": s = '<g transform="translate(-6 -8) scale(.8)">' + moon + "</g>" + cloud(4, 8); break;
      case "cloud": s = cloud(-2, -2, "#c9d3e1") + cloud(6, 6); break;
      case "fog": s = cloud(2, -4, "#c9d3e1") + '<g stroke="#c9d3e1" stroke-width="3" stroke-linecap="round"><path d="M12 46h40M18 53h30"/></g>'; break;
      case "rain": s = cloud(2, -6, "#b9c6d8") + '<g stroke="#5aa4ee" stroke-width="3" stroke-linecap="round"><path class="drop" d="M22 44v6"/><path class="drop" d="M32 46v6"/><path class="drop" d="M42 44v6"/></g>'; break;
      case "snow": s = cloud(2, -6, "#dfe7f2") + '<g fill="#fff"><circle class="flake" cx="22" cy="48" r="2.5"/><circle class="flake" cx="32" cy="50" r="2.5"/><circle class="flake" cx="42" cy="48" r="2.5"/></g>'; break;
      case "storm": s = cloud(2, -6, "#8f9cb3") + '<path class="bolt" d="M34 38l-8 12h7l-4 10 11-14h-7l4-8z" fill="#ffcf3f"/>'; break;
    }
    return '<svg class="wx-ico" viewBox="0 0 64 64" aria-hidden="true">' + s + "</svg>";
  }
  var DEFAULT_PLACE = { name: "New York", admin: "NY", lat: 40.7143, lon: -74.006 };
  function getPlace() { try { var p = JSON.parse(store("rn-place")); return p && p.lat ? p : DEFAULT_PLACE; } catch (e) { return DEFAULT_PLACE; } }
  function setPlace(p) { store("rn-place", JSON.stringify(p)); }
  function getUnit() { return store("rn-unit") || "f"; }
  function ss(k, v) { try { if (v === undefined) return JSON.parse(sessionStorage.getItem(k)); sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }

  var NWS = "https://api.weather.gov";
  function getJSON(u) {
    return fetch(u, { headers: { Accept: "application/geo+json" } }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }
  function retry(u) { return getJSON(u).catch(function () { return new Promise(function (r) { setTimeout(r, 900); }).then(function () { return getJSON(u); }); }); }
  function pointsFor(p) {
    var key = "rn-pt:" + (+p.lat).toFixed(3) + "," + (+p.lon).toFixed(3), c = null;
    try { c = JSON.parse(store(key)); } catch (e) {}
    if (c && Date.now() - c.ts < 7 * 864e5) return Promise.resolve(c);
    return retry(NWS + "/points/" + (+p.lat).toFixed(4) + "," + (+p.lon).toFixed(4)).then(function (d) {
      var q = d.properties, rl = q.relativeLocation && q.relativeLocation.properties;
      var pt = { ts: Date.now(), forecast: q.forecast, hourly: q.forecastHourly, stations: q.observationStations, tz: q.timeZone,
        city: rl && rl.city, state: rl && rl.state };
      store(key, JSON.stringify(pt)); return pt;
    });
  }
  var C = function (f) { return f == null ? null : f * 1.8 + 32; };   // °C -> °F
  // Normalized model, always in °F / mph / inHg-free units (hPa, miles); views convert.
  function loadWeather(p, fresh) {
    var ck = "rn-wx:" + (+p.lat).toFixed(3) + "," + (+p.lon).toFixed(3), hit = !fresh && ss(ck);
    if (hit && Date.now() - hit.ts < 10 * 60000) return Promise.resolve(hit);
    return pointsFor(p).then(function (pt) {
      var obs = retry(pt.stations).then(function (s) {
        var st = s.features && s.features[0]; if (!st) return null;
        return retry(st.id + "/observations/latest").then(function (o) { o.properties.stationName = st.properties.name; return o.properties; });
      }).catch(function () { return null; });
      return Promise.all([retry(pt.forecast), retry(pt.hourly), obs]).then(function (r) {
        var periods = r[0].properties.periods, hours = r[1].properties.periods, o = r[2];
        var hourly = hours.slice(0, 25).map(function (h) {
          return { t: h.startTime, temp: h.temperature, pop: (h.probabilityOfPrecipitation || {}).value || 0, icon: h.icon, text: h.shortForecast,
            hum: (h.relativeHumidity || {}).value, wind: parseInt(h.windSpeed, 10) || 0, dir: h.windDirection, dew: C((h.dewpoint || {}).value) };
        });
        var daily = [];
        periods.forEach(function (q, i) {
          if (q.isDaytime) {
            var night = periods[i + 1] && !periods[i + 1].isDaytime ? periods[i + 1] : null;
            daily.push({ date: q.startTime, name: q.name, hi: q.temperature, lo: night ? night.temperature : null, icon: q.icon, text: q.shortForecast,
              pop: Math.max((q.probabilityOfPrecipitation || {}).value || 0, night ? (night.probabilityOfPrecipitation || {}).value || 0 : 0),
              wind: q.windSpeed, detail: q.detailedForecast, nightDetail: night && night.detailedForecast });
          } else if (i === 0) {
            daily.push({ date: q.startTime, name: q.name, hi: null, lo: q.temperature, icon: q.icon, text: q.shortForecast,
              pop: (q.probabilityOfPrecipitation || {}).value || 0, wind: q.windSpeed, detail: q.detailedForecast });
          }
        });
        var h0 = hourly[0], fresh = o && o.temperature && o.temperature.value != null && Date.now() - new Date(o.timestamp) < 3 * 3600e3;
        var now = {
          temp: fresh ? C(o.temperature.value) : h0.temp,
          text: fresh && o.textDescription ? o.textDescription : h0.text,
          icon: fresh && o.icon ? o.icon : h0.icon,
          feels: fresh ? C((o.heatIndex || {}).value != null ? o.heatIndex.value : (o.windChill || {}).value != null ? o.windChill.value : o.temperature.value) : h0.temp,
          hum: fresh && o.relativeHumidity.value != null ? o.relativeHumidity.value : h0.hum,
          dew: fresh && o.dewpoint.value != null ? C(o.dewpoint.value) : h0.dew,
          wind: fresh && o.windSpeed.value != null ? o.windSpeed.value / 1.609 : h0.wind,
          dirDeg: fresh ? o.windDirection.value : null, dir: h0.dir,
          gust: fresh && o.windGust.value != null ? o.windGust.value / 1.609 : null,
          pressure: fresh && o.barometricPressure.value != null ? o.barometricPressure.value / 100 : null,
          vis: fresh && o.visibility.value != null ? o.visibility.value / 1609.34 : null,
          time: fresh ? o.timestamp : h0.t, station: fresh ? o.stationName : null
        };
        var model = { ts: Date.now(), tz: pt.tz, city: pt.city, state: pt.state, now: now, hourly: hourly, daily: daily };
        ss(ck, model); return model;
      });
    });
  }
  function temp(f, unit) { return f == null ? "–" : Math.round(unit === "c" ? (f - 32) / 1.8 : f) + "°"; }
  window.RNWX = { info: wxInfo, icon: wxIcon, getPlace: getPlace, setPlace: setPlace, getUnit: getUnit,
    setUnit: function (u) { store("rn-unit", u); }, load: loadWeather, temp: temp, points: pointsFor, getJSON: retry, store: store };

  /* Header pill, sidebar card and home band */
  var mini = $("[data-wx-mini]"), card = $("[data-wx-card]"), band = $("[data-wx-band-now]");
  if (mini || card || band) {
    var place = getPlace(), unit = getUnit();
    loadWeather(place).then(function (d) {
      var c = d.now, inf = wxInfo(c.icon, c.text), t = temp(c.temp, unit);
      if (mini) mini.innerHTML = wxIcon(inf.kind) + "<span>" + place.name + " <b>" + t + "</b></span>";
      var days = function (n) {
        var h = "", list = d.daily.slice(1, n + 1);
        list.forEach(function (x) {
          h += "<div>" + x.name.slice(0, 3) + wxIcon(wxInfo(x.icon).kind) + "<b>" + temp(x.hi, unit) + "</b> " + temp(x.lo, unit) + "</div>";
        });
        return '<div class="wxc-days">' + h + "</div>";
      };
      var now = '<div class="wxc-now">' + wxIcon(inf.kind) + '<div><div class="wxc-temp">' + t + '</div><div class="wxc-city">' + place.name +
        '</div><div class="wxc-desc">' + inf.text + " · Feels " + temp(c.feels, unit) + "</div></div></div>";
      if (card) { card.dataset.mood = inf.mood; $(".wx-card-body", card).innerHTML = now + days(4); }
      if (band) band.innerHTML = now + days(6);
    }).catch(function () {
      if (mini) mini.innerHTML = "<span>Weather</span>";
      if (card) $(".wx-card-body", card).innerHTML = '<p>Weather is unavailable right now. <a href="/weather/" style="color:#fff;text-decoration:underline">Try the weather page</a>.</p>';
      if (band) band.innerHTML = "<p>Live weather is unavailable right now.</p>";
    });
  }
})();
