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

  /* ---------------- Weather helpers (shared with weather.js) ---------------- */
  var WMO = {
    0: ["Clear sky", "sun"], 1: ["Mainly clear", "sun"], 2: ["Partly cloudy", "partly"], 3: ["Overcast", "cloud"],
    45: ["Fog", "fog"], 48: ["Freezing fog", "fog"], 51: ["Light drizzle", "rain"], 53: ["Drizzle", "rain"], 55: ["Heavy drizzle", "rain"],
    56: ["Freezing drizzle", "rain"], 57: ["Freezing drizzle", "rain"], 61: ["Light rain", "rain"], 63: ["Rain", "rain"], 65: ["Heavy rain", "rain"],
    66: ["Freezing rain", "rain"], 67: ["Freezing rain", "rain"], 71: ["Light snow", "snow"], 73: ["Snow", "snow"], 75: ["Heavy snow", "snow"],
    77: ["Snow grains", "snow"], 80: ["Rain showers", "rain"], 81: ["Rain showers", "rain"], 82: ["Violent showers", "rain"],
    85: ["Snow showers", "snow"], 86: ["Heavy snow showers", "snow"], 95: ["Thunderstorm", "storm"], 96: ["Thunderstorm with hail", "storm"], 99: ["Severe thunderstorm", "storm"]
  };
  function wxInfo(code, isDay) {
    var w = WMO[code] || ["—", "cloud"], kind = w[1];
    if (!isDay && (kind === "sun" || kind === "partly")) kind = kind === "sun" ? "moon" : "partlynight";
    var mood = { sun: "clear", partly: "clear", moon: "night", partlynight: "night", cloud: "cloud", fog: "fog", rain: "rain", snow: "snow", storm: "storm" }[kind];
    return { text: w[0], kind: kind, mood: mood };
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
  var DEFAULT_PLACE = { name: "New York", admin: "New York", lat: 40.7143, lon: -74.006 };
  function getPlace() { try { return JSON.parse(store("rn-place")) || DEFAULT_PLACE; } catch (e) { return DEFAULT_PLACE; } }
  function setPlace(p) { store("rn-place", JSON.stringify(p)); }
  function getUnit() { return store("rn-unit") || "f"; }
  function forecastURL(p, unit, extra) {
    var u = unit === "c";
    return "https://api.open-meteo.com/v1/forecast?latitude=" + p.lat + "&longitude=" + p.lon +
      "&current=temperature_2m,apparent_temperature,relative_humidity_2m,is_day,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m,pressure_msl,precipitation,cloud_cover,visibility,uv_index,dew_point_2m" +
      "&hourly=temperature_2m,precipitation_probability,weather_code,is_day" +
      "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,sunrise,sunset,uv_index_max,wind_speed_10m_max" +
      "&temperature_unit=" + (u ? "celsius" : "fahrenheit") + "&wind_speed_unit=" + (u ? "kmh" : "mph") +
      "&precipitation_unit=" + (u ? "mm" : "inch") + "&timezone=auto&forecast_days=7" + (extra || "");
  }
  var cache = {};
  function fetchForecast(p, unit) {
    var key = p.lat + "," + p.lon + unit;
    if (!cache[key]) cache[key] = fetch(forecastURL(p, unit)).then(function (r) { if (!r.ok) throw new Error("wx"); return r.json(); });
    return cache[key];
  }
  window.RNWX = { info: wxInfo, icon: wxIcon, getPlace: getPlace, setPlace: setPlace, getUnit: getUnit, setUnit: function (u) { store("rn-unit", u); }, fetch: fetchForecast, store: store };

  function dayName(iso, i) { return i === 0 ? "Today" : new Date(iso + "T12:00").toLocaleDateString("en-US", { weekday: "short" }); }

  /* Header pill, sidebar card and home band */
  var mini = $("[data-wx-mini]"), card = $("[data-wx-card]"), band = $("[data-wx-band-now]");
  if (mini || card || band) {
    var place = getPlace(), unit = getUnit();
    fetchForecast(place, unit).then(function (d) {
      var c = d.current, inf = wxInfo(c.weather_code, c.is_day), t = Math.round(c.temperature_2m) + "°";
      if (mini) mini.innerHTML = wxIcon(inf.kind) + "<span>" + place.name + " <b>" + t + "</b></span>";
      var days = function (n) {
        var h = "";
        for (var i = 1; i <= n; i++) h += "<div>" + dayName(d.daily.time[i], i) + wxIcon(wxInfo(d.daily.weather_code[i], 1).kind) +
          "<b>" + Math.round(d.daily.temperature_2m_max[i]) + "°</b> " + Math.round(d.daily.temperature_2m_min[i]) + "°</div>";
        return '<div class="wxc-days">' + h + "</div>";
      };
      var now = '<div class="wxc-now">' + wxIcon(inf.kind) + '<div><div class="wxc-temp">' + t + '</div><div class="wxc-city">' + place.name +
        '</div><div class="wxc-desc">' + inf.text + " · Feels " + Math.round(c.apparent_temperature) + "°</div></div></div>";
      if (card) { card.dataset.mood = inf.mood; $(".wx-card-body", card).innerHTML = now + days(4); }
      if (band) band.innerHTML = now + days(6);
    }).catch(function () {
      if (card) $(".wx-card-body", card).innerHTML = '<p>Weather is unavailable right now. <a href="/weather/" style="color:#fff;text-decoration:underline">Try the weather page</a>.</p>';
      if (band) band.innerHTML = "<p>Live weather is unavailable right now.</p>";
    });
  }
})();
