/* Pensacola Hurricane - site script. Each block activates only when its
   data-* hook is on the page. Live data: NWS (api.weather.gov, CORS-enabled)
   and NHC (proxied through /api/storms.php and /api/nhc-feed.php). */
(function () {
  "use strict";
  var PNS = { lat: 30.4213, lon: -87.2169 };
  var NWS = "https://api.weather.gov";
  var $ = function (sel, root) { return (root || document).querySelector(sel); };
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
  function num(v, d) { var n = parseFloat(String(v).replace(/[^0-9.\-]/g, "")); return isNaN(n) ? (d || 0) : n; }
  function getJSON(url) {
    return fetch(url, { headers: { Accept: "application/geo+json, application/json" } }).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    });
  }
  function fmtTime(iso) {
    try { return new Date(iso).toLocaleString("en-US", { timeZone: "America/Chicago", weekday: "short", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) + " CT"; }
    catch (e) { return iso; }
  }
  function milesBetween(a, b, c, d) {
    var R = 3958.8, toR = Math.PI / 180;
    var dLat = (c - a) * toR, dLon = (d - b) * toR;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a * toR) * Math.cos(c * toR) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  function compass(deg) { var d = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]; return d[Math.round(((deg % 360) / 22.5)) % 16]; }
  function category(kt) {
    kt = +kt;
    if (kt >= 137) return "Category 5 Hurricane";
    if (kt >= 113) return "Category 4 Hurricane";
    if (kt >= 96) return "Category 3 Hurricane";
    if (kt >= 83) return "Category 2 Hurricane";
    if (kt >= 64) return "Category 1 Hurricane";
    if (kt >= 34) return "Tropical Storm";
    return "Tropical Depression";
  }
  var CLASS = { HU: "Hurricane", TS: "Tropical Storm", TD: "Tropical Depression", STS: "Subtropical Storm", STD: "Subtropical Depression", PTC: "Potential Tropical Cyclone", PC: "Post-Tropical Cyclone", TY: "Typhoon" };

  /* ---------- Mobile menu (slide-in drawer) ---------- */
  var menuBtn = $("[data-menu-btn]"), nav = $(".nav-row"), backdrop = $("[data-nav-backdrop]"), header = $(".site-header");
  var mq = window.matchMedia("(max-width: 960px)");
  function menuOpen() { return nav && nav.classList.contains("is-open"); }
  function setMenu(open) {
    if (!menuBtn || !nav) return;
    if (open) {
      // Drawer starts right under the header, wherever the header is on screen.
      document.documentElement.style.setProperty("--drawer-top", Math.max(0, Math.round(header.getBoundingClientRect().bottom)) + "px");
      if (backdrop) { backdrop.hidden = false; requestAnimationFrame(function () { backdrop.classList.add("is-visible"); }); }
    } else if (backdrop) {
      backdrop.classList.remove("is-visible");
      setTimeout(function () { if (!menuOpen()) backdrop.hidden = true; }, 300);
    }
    nav.classList.toggle("is-open", open);
    document.documentElement.classList.toggle("menu-open", open);
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    var label = menuBtn.querySelector(".menu-label"); if (label) label.textContent = open ? "Close" : "Menu";
    if (open) { var first = nav.querySelector("a"); if (first) first.focus({ preventScroll: true }); }
  }
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () { setMenu(!menuOpen()); });
    if (backdrop) backdrop.addEventListener("click", function () { setMenu(false); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a") && menuOpen()) setMenu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && menuOpen()) { setMenu(false); menuBtn.focus(); } });
    var onMq = function () { if (!mq.matches && menuOpen()) setMenu(false); };
    if (mq.addEventListener) mq.addEventListener("change", onMq); else if (mq.addListener) mq.addListener(onMq);
    window.addEventListener("pageshow", function () { if (menuOpen()) setMenu(false); });
  }

  /* ---------- Scroll effects: header state, progress bar, back-to-top ---------- */
  var progress = $("[data-scroll-progress]"), toTop = $("[data-to-top]"), ticking = false;
  function onScroll() {
    ticking = false;
    var y = window.pageYOffset || document.documentElement.scrollTop;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (header) header.classList.toggle("is-scrolled", y > 40);
    if (progress) progress.style.transform = "scaleX(" + (max > 0 ? Math.min(1, y / max) : 0) + ")";
    if (toTop) toTop.classList.toggle("is-visible", y > 700);
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: "smooth" }); });

  /* ---------- Reveal on scroll + count-up stats ---------- */
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce && "IntersectionObserver" in window) {
    var groups = [
      [".section-head, .prose > h2, .page-hero .container > *, .claim-cta-inner > *", ""],
      [".card, .step, .stat, .tool, .side-box, .side-cta, .tactic-list li, .faq details, .timeline li, .table-wrap, .callout, .quiet-box", ""],
      [".lead-card", "reveal-zoom"]
    ];
    var targets = [];
    groups.forEach(function (g) {
      $$(g[0]).forEach(function (el) {
        if (el.closest(".hero") && !el.classList.contains("lead-card")) return;   // keep the hero text instant
        if (el.classList.contains("reveal")) return;
        el.classList.add("reveal"); if (g[1]) el.classList.add(g[1]);
        // stagger siblings in the same grid/list
        var sibs = Array.prototype.filter.call(el.parentNode.children, function (c) { return c.classList.contains("reveal"); });
        el.style.setProperty("--i", Math.min(sibs.indexOf(el), 6));
        targets.push(el);
      });
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (el) { io.observe(el); });
    document.documentElement.classList.add("motion");
    // Safety net: never leave anything hidden (e.g. anchors jumped past, print, odd browsers).
    setTimeout(function () { targets.forEach(function (el) { var r = el.getBoundingClientRect(); if (r.bottom < 0) el.classList.add("is-in"); }); }, 1200);
    window.addEventListener("beforeprint", function () { targets.forEach(function (el) { el.classList.add("is-in"); }); });

    var counters = $$(".stat strong").filter(function (el) { return /^\D*\d+\D*$/.test(el.textContent) && !/^\D*0\D*$/.test(el.textContent); });
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        var el = en.target, m = /^(\D*)(\d+)(\D*)$/.exec(el.textContent), end = +m[2], t0 = null;
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / 1100), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
          el.textContent = m[1] + v + m[3];
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { cio.observe(el); });
  }

  /* ---------- NWS alerts for Pensacola (alert bar + lists) ---------- */
  var alertsPromise = null;
  function pensacolaAlerts() {
    if (!alertsPromise) alertsPromise = getJSON(NWS + "/alerts/active?point=" + PNS.lat + "," + PNS.lon).then(function (d) { return d.features || []; });
    return alertsPromise;
  }
  var rank = { Extreme: 4, Severe: 3, Moderate: 2, Minor: 1, Unknown: 0 };
  var bar = $("[data-alertbar]");
  if (bar) {
    var barText = $("[data-alertbar-text]");
    pensacolaAlerts().then(function (list) {
      if (!list.length) { barText.textContent = "No active National Weather Service alerts for Pensacola right now."; return; }
      list.sort(function (a, b) { return (rank[b.properties.severity] || 0) - (rank[a.properties.severity] || 0); });
      var events = [];
      list.forEach(function (f) { if (events.indexOf(f.properties.event) < 0) events.push(f.properties.event); });
      var top = events[0];
      if (/Warning/.test(top)) bar.classList.add("is-warning"); else if (/Watch/.test(top)) bar.classList.add("is-watch");
      barText.innerHTML = "<strong>In effect for Pensacola:</strong> " + esc(events.slice(0, 4).join(" • ")) + (events.length > 4 ? " +" + (events.length - 4) + " more" : "");
    }).catch(function () { barText.textContent = "Live alerts unavailable — check weather.gov/mob for the latest Pensacola warnings."; });
  }
  $$("[data-nws-alerts]").forEach(function (box) {
    pensacolaAlerts().then(function (list) {
      if (!list.length) { box.innerHTML = '<p class="muted">No active watches, warnings or advisories for the Pensacola area from NWS Mobile. This list refreshes every time the page loads.</p>'; return; }
      list.sort(function (a, b) { return (rank[b.properties.severity] || 0) - (rank[a.properties.severity] || 0); });
      box.innerHTML = list.map(function (f) {
        var p = f.properties;
        return '<div class="alert-item sev-' + esc(p.severity) + '"><h4>' + esc(p.event) + '</h4><div class="small muted">' + esc(p.senderName) + " · Issued " + esc(fmtTime(p.sent)) + (p.ends || p.expires ? " · Until " + esc(fmtTime(p.ends || p.expires)) : "") + "</div>" +
          (p.headline ? "<p>" + esc(p.headline) + "</p>" : "") +
          "<details><summary>Full text</summary><pre>" + esc((p.description || "") + "\n\n" + (p.instruction || "")) + "</pre></details></div>";
      }).join("");
    }).catch(function () { box.innerHTML = '<p class="muted">Could not reach the National Weather Service. See <a href="https://www.weather.gov/mob/">weather.gov/mob</a>.</p>'; });
  });

  /* ---------- Active storms (NHC) ---------- */
  $$("[data-storms]").forEach(function (box) {
    var compact = box.hasAttribute("data-compact");
    getJSON("/api/storms.php").then(function (d) {
      var storms = (d.activeStorms || []).filter(function (s) { return /^al/i.test(s.id); });
      if (!storms.length) {
        box.innerHTML = '<div class="card"><h3>No active Atlantic or Gulf storms</h3><p>The National Hurricane Center is not tracking any named systems in the Atlantic basin right now. Check the 7-day outlook below for areas being watched for development.</p></div>';
        return;
      }
      storms.sort(function (a, b) { return milesBetween(PNS.lat, PNS.lon, a.latitudeNumeric, a.longitudeNumeric) - milesBetween(PNS.lat, PNS.lon, b.latitudeNumeric, b.longitudeNumeric); });
      box.innerHTML = storms.map(function (s) {
        var mph = Math.round(s.intensity * 1.15078 / 5) * 5;
        var dist = Math.round(milesBetween(PNS.lat, PNS.lon, s.latitudeNumeric, s.longitudeNumeric));
        var label = (CLASS[s.classification] || s.classification) + " " + s.name;
        var cat = s.classification === "HU" ? category(s.intensity).replace(" Hurricane", "") : (CLASS[s.classification] || "");
        var num = s.id.substr(2, 2).toUpperCase();
        var cone = "https://www.nhc.noaa.gov/storm_graphics/AT" + num + "/" + s.id.toUpperCase() + "_5day_cone.png";
        var links = [["Public advisory", s.publicAdvisory], ["Forecast discussion", s.forecastDiscussion], ["Wind probabilities", s.windSpeedProbabilities], ["All NHC graphics", s.forecastGraphics]]
          .filter(function (l) { return l[1] && l[1].url; })
          .map(function (l) { return '<a href="' + esc(l[1].url) + '" target="_blank" rel="noopener">' + l[0] + "</a>"; }).join("");
        if (compact) {
          return '<div class="hero-panel" style="margin-bottom:12px"><div class="live-pill">Active now</div><h2 style="margin:.5em 0 .3em">' + esc(label) + "</h2><p style=\"margin:0;color:#dbe6ef\">" + mph + " mph winds · " + dist + " miles from Pensacola · moving " + compass(s.movementDir) + " at " + s.movementSpeed + " mph</p><p class=\"small\" style=\"margin:.5em 0 0;color:#9fb4c7\">NHC advisory " + esc(s.publicAdvisory ? s.publicAdvisory.advNum : "") + " · " + esc(fmtTime(s.lastUpdate)) + "</p></div>";
        }
        return '<article class="storm-card"><div class="storm-top"><div><div class="live-pill" style="background:#fff">Live · NHC</div><h3>' + esc(label) + '</h3><div class="small" style="color:#9fb4c7">Updated ' + esc(fmtTime(s.lastUpdate)) + "</div></div><div class=\"storm-cat\">" + esc(cat) + "</div></div>" +
          '<div class="storm-body"><div><div class="kv">' +
          "<div><span>Max sustained wind</span><b>" + mph + " mph</b></div>" +
          "<div><span>Pressure</span><b>" + esc(s.pressure) + " mb</b></div>" +
          "<div><span>Position</span><b>" + esc(s.latitude + " " + s.longitude) + "</b></div>" +
          "<div><span>Movement</span><b>" + compass(s.movementDir) + " " + esc(s.movementSpeed) + " mph</b></div>" +
          "<div><span>Distance to Pensacola</span><b>" + dist.toLocaleString() + " mi</b></div>" +
          "<div><span>Advisory</span><b>#" + esc(s.publicAdvisory ? s.publicAdvisory.advNum : "—") + "</b></div>" +
          '</div><div class="storm-links">' + links + "</div>" +
          '<p class="note" style="margin-top:12px">Distance is measured from downtown Pensacola to the storm center; damaging winds, surge and rain extend far beyond the center.</p></div>' +
          '<div><a href="' + esc(cone) + '" target="_blank" rel="noopener"><img src="' + esc(cone) + '" alt="NHC 5-day forecast cone for ' + esc(label) + '" loading="lazy" onerror="this.parentNode.style.display=\'none\'"></a><p class="note">Official NHC 5-day forecast cone. The cone shows the probable track of the center only.</p></div></div></article>';
      }).join("");
    }).catch(function () {
      box.innerHTML = '<div class="card"><p>Live storm data is temporarily unavailable. Go straight to <a href="https://www.nhc.noaa.gov/">hurricanes.gov</a>.</p></div>';
    });
  });

  /* ---------- NHC + NWS Mobile text products (news page) ---------- */
  $$("[data-nhc-feed]").forEach(function (box) {
    getJSON("/api/nhc-feed.php").then(function (d) {
      var items = d.items || [];
      if (!items.length) { box.innerHTML = '<p class="muted">No NHC products right now.</p>'; return; }
      box.innerHTML = items.slice(0, 12).map(function (it) {
        return '<div class="alert-item" style="border-left-color:var(--sea)"><h4><a href="' + esc(it.link) + '" target="_blank" rel="noopener">' + esc(it.title) + '</a></h4><div class="small muted">' + esc(it.pubDate) + "</div></div>";
      }).join("");
    }).catch(function () { box.innerHTML = '<p class="muted">NHC feed unavailable. Visit <a href="https://www.nhc.noaa.gov/">nhc.noaa.gov</a>.</p>'; });
  });
  $$("[data-nws-product]").forEach(function (box) {
    var type = box.getAttribute("data-nws-product");
    getJSON(NWS + "/products/types/" + type + "/locations/MOB").then(function (d) {
      var g = d["@graph"] || [];
      if (!g.length) { box.innerHTML = '<p class="muted">NWS Mobile has not issued a recent ' + esc(type) + " product.</p>"; return; }
      return getJSON(g[0]["@id"]).then(function (p) {
        var age = (Date.now() - new Date(p.issuanceTime).getTime()) / 36e5;
        box.innerHTML = '<p class="small muted">' + esc(p.productName) + " · NWS Mobile/Pensacola · issued " + esc(fmtTime(p.issuanceTime)) + (age > 72 ? " (older product — no newer statement issued)" : "") + '</p><div class="product-text">' + esc(p.productText) + "</div>";
      });
    }).catch(function () { box.innerHTML = '<p class="muted">Product unavailable. See <a href="https://www.weather.gov/mob/">weather.gov/mob</a>.</p>'; });
  });

  /* ---------- Weather center ---------- */
  function cToF(c) { return c == null ? null : Math.round(c * 9 / 5 + 32); }
  function kmhToMph(k) { return k == null ? null : Math.round(k * 0.621371); }
  var nowBox = $("[data-wx-current]");
  if (nowBox) {
    getJSON(NWS + "/stations/KPNS/observations/latest").then(function (d) {
      var p = d.properties;
      var t = cToF(p.temperature.value), w = kmhToMph(p.windSpeed.value), g = kmhToMph(p.windGust.value);
      var press = p.barometricPressure.value ? (p.barometricPressure.value / 3386.39).toFixed(2) : null;
      nowBox.innerHTML = '<div class="wx-now">' + (p.icon ? '<img src="' + esc(p.icon.replace("size=medium", "size=large")) + '" alt="" width="96" height="96" style="border-radius:12px">' : "") +
        '<div><div class="wx-temp">' + (t != null ? t + "°F" : "—") + "</div><div><strong>" + esc(p.textDescription || "") + "</strong></div></div></div>" +
        '<div class="kv" style="margin-top:18px">' +
        "<div><span>Wind</span><b>" + (w != null ? (p.windDirection.value != null ? compass(p.windDirection.value) + " " : "") + w + " mph" : "Calm/NA") + "</b></div>" +
        "<div><span>Gusts</span><b>" + (g ? g + " mph" : "—") + "</b></div>" +
        "<div><span>Humidity</span><b>" + (p.relativeHumidity.value != null ? Math.round(p.relativeHumidity.value) + "%" : "—") + "</b></div>" +
        "<div><span>Pressure</span><b>" + (press ? press + " in" : "—") + "</b></div>" +
        '</div><p class="note" style="margin-top:10px">Pensacola International Airport (KPNS) · observed ' + esc(fmtTime(p.timestamp)) + "</p>";
    }).catch(function () { nowBox.innerHTML = '<p class="muted">Current conditions unavailable.</p>'; });
  }
  var pointPromise = null;
  function point() { if (!pointPromise) pointPromise = getJSON(NWS + "/points/" + PNS.lat + "," + PNS.lon).then(function (d) { return d.properties; }); return pointPromise; }
  var fcBox = $("[data-wx-forecast]");
  if (fcBox) {
    point().then(function (p) { return getJSON(p.forecast); }).then(function (d) {
      var per = d.properties.periods || [];
      fcBox.innerHTML = '<div class="forecast">' + per.filter(function (x) { return x.isDaytime || x.number === 1; }).slice(0, 7).map(function (x) {
        return '<div class="fc-day"><b>' + esc(x.name) + '</b><img src="' + esc(x.icon) + '" alt="" loading="lazy"><div><strong>' + esc(x.temperature) + "°" + esc(x.temperatureUnit) + "</strong></div><div>" + esc(x.shortForecast) + '</div><div class="muted small">Wind ' + esc(x.windDirection + " " + x.windSpeed) + "</div>" + (x.probabilityOfPrecipitation && x.probabilityOfPrecipitation.value != null ? '<div class="small">Rain ' + x.probabilityOfPrecipitation.value + "%</div>" : "") + "</div>";
      }).join("") + "</div>" +
      '<details style="margin-top:16px"><summary><strong>Detailed forecast text</strong></summary>' + per.slice(0, 8).map(function (x) { return "<p><strong>" + esc(x.name) + ":</strong> " + esc(x.detailedForecast) + "</p>"; }).join("") + "</details>";
    }).catch(function () { fcBox.innerHTML = '<p class="muted">Forecast unavailable. See <a href="https://forecast.weather.gov/MapClick.php?lat=30.4213&lon=-87.2169">forecast.weather.gov</a>.</p>'; });
  }
  function parseDur(validTime) {
    var parts = validTime.split("/"), start = new Date(parts[0]).getTime();
    var m = /P(?:(\d+)D)?T?(?:(\d+)H)?/.exec(parts[1] || "PT1H");
    var hours = (+(m[1] || 0)) * 24 + (+(m[2] || 0));
    return { start: start, hours: hours || 1 };
  }
  var windBox = $("[data-wx-wind]"), rainBox = $("[data-wx-rain]");
  if (windBox || rainBox) {
    point().then(function (p) { return getJSON(p.forecastGridData); }).then(function (d) {
      var g = d.properties, now = Date.now();
      if (windBox) {
        var hours = [];
        function expandSeries(series, key) {
          (series.values || []).forEach(function (v) {
            var t = parseDur(v.validTime);
            for (var h = 0; h < t.hours; h++) {
              var ts = t.start + h * 36e5;
              if (ts < now - 36e5 || ts > now + 72 * 36e5) continue;
              var idx = Math.floor((ts - now) / 36e5) + 1;
              hours[idx] = hours[idx] || { ts: ts };
              hours[idx][key] = kmhToMph(v.value);
            }
          });
        }
        expandSeries(g.windSpeed, "w"); expandSeries(g.windGust, "g");
        hours = hours.filter(Boolean).slice(0, 72);
        var max = Math.max.apply(null, hours.map(function (h) { return Math.max(h.w || 0, h.g || 0); }).concat([20]));
        var peak = hours.reduce(function (a, h) { return (h.g || 0) > (a.g || 0) ? h : a; }, {});
        windBox.innerHTML = '<p><strong>Peak forecast gust next 72 hours: ' + (peak.g || "—") + " mph</strong>" + (peak.ts ? " around " + esc(fmtTime(new Date(peak.ts).toISOString())) : "") + "</p>" +
          '<div class="bars" aria-label="Hourly wind and gust forecast">' + hours.map(function (h) {
            return '<div class="' + ((h.g || 0) >= 39 ? "gust" : "") + '" style="height:' + Math.max(2, ((h.g || h.w || 0) / max) * 100) + '%" title="' + esc(fmtTime(new Date(h.ts).toISOString())) + ": wind " + (h.w || 0) + " mph, gusts " + (h.g || 0) + ' mph"></div>';
          }).join("") + '</div><div class="bars-labels"><span>Now</span><span>+24h</span><span>+48h</span><span>+72h</span></div>' +
          '<p class="note">Bar height = forecast gust. Orange bars = gusts of 39 mph or more (tropical-storm force). Hover a bar for exact values. Source: NWS gridded forecast.</p>';
      }
      if (rainBox) {
        var total24 = 0, total72 = 0, total7 = 0;
        (g.quantitativePrecipitation.values || []).forEach(function (v) {
          var t = parseDur(v.validTime), endMs = t.start + t.hours * 36e5;
          if (endMs < now) return;
          var inches = (v.value || 0) / 25.4, hrsAhead = (t.start - now) / 36e5;
          if (hrsAhead < 24) total24 += inches;
          if (hrsAhead < 72) total72 += inches;
          total7 += inches;
        });
        rainBox.innerHTML = '<div class="stats stats-3">' +
          '<div class="stat"><strong>' + total24.toFixed(2) + '"</strong><span>Next 24 hours</span></div>' +
          '<div class="stat"><strong>' + total72.toFixed(2) + '"</strong><span>Next 72 hours</span></div>' +
          '<div class="stat"><strong>' + total7.toFixed(2) + '"</strong><span>Full forecast period</span></div></div>' +
          '<p class="note" style="margin-top:10px">Forecast rainfall for downtown Pensacola from the NWS gridded forecast (quantitative precipitation). Tropical rain bands can locally double these totals.</p>';
      }
    }).catch(function () {
      if (windBox) windBox.innerHTML = '<p class="muted">Wind forecast unavailable.</p>';
      if (rainBox) rainBox.innerHTML = '<p class="muted">Rainfall forecast unavailable.</p>';
    });
  }

  /* ---------- Evacuation zone checker ---------- */
  var zoneForm = $("[data-zone-form]");
  if (zoneForm) {
    var zoneOut = $("[data-zone-result]");
    var ZONE_TEXT = {
      A: "Zone A is the first to evacuate. Expect an evacuation order for any hurricane and possibly for strong tropical storms. Barrier islands and the lowest waterfront land are in Zone A.",
      B: "Zone B evacuates for Category 1 and stronger hurricanes in most plans. This is low-lying land along the bays, bayous and rivers.",
      C: "Zone C typically evacuates for Category 2 and stronger hurricanes.",
      D: "Zone D typically evacuates for Category 3 and stronger hurricanes.",
      E: "Zone E typically evacuates only for Category 4 and 5 hurricanes."
    };
    zoneForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var addr = zoneForm.address.value.trim();
      if (addr.length < 5) { zoneOut.innerHTML = "<p>Please enter a street address, for example <em>400 Quietwater Beach Rd, Pensacola Beach, FL</em>.</p>"; return; }
      zoneOut.innerHTML = '<p class="loading">Looking up your address with the U.S. Census geocoder and county GIS…</p>';
      getJSON("/api/zone.php?address=" + encodeURIComponent(addr)).then(function (d) {
        if (d.error) { zoneOut.innerHTML = "<p><strong>" + esc(d.error) + "</strong></p><p>Try adding the city and ZIP code, or use the official <a href=\"https://myescambia.com/apps/knowyourzone/\" target=\"_blank\" rel=\"noopener\">Escambia County Know Your Zone map</a> or <a href=\"https://www.floridadisaster.org/knowyourzone/\" target=\"_blank\" rel=\"noopener\">Florida's statewide lookup</a>.</p>"; return; }
        var z = d.zone, html = "";
        if (z) {
          html += '<div style="overflow:hidden"><span class="zone-badge zone-' + esc(z) + '">' + esc(z) + '</span><div class="big">Evacuation Zone ' + esc(z) + "</div><p style=\"margin:4px 0 0\">" + esc(d.matched) + " · " + esc(d.county) + "</p></div><p style=\"margin-top:14px\">" + esc(ZONE_TEXT[z] || "") + "</p>";
        } else if (d.supported) {
          html += '<div style="overflow:hidden"><span class="zone-badge zone-none">No zone</span><div class="big">Not in a storm-surge evacuation zone</div><p style="margin:4px 0 0">' + esc(d.matched) + " · " + esc(d.county) + '</p></div><p style="margin-top:14px">County maps do not place this address in an evacuation zone. You may still need to leave if you live in a mobile or manufactured home, an RV, a flood-prone street, or if you depend on electricity for medical equipment.</p>';
        } else {
          html += '<div class="big">' + esc(d.county || "Outside our coverage") + "</div><p>" + esc(d.matched) + "</p><p>This checker covers Escambia and Santa Rosa counties. Use <a href=\"https://www.floridadisaster.org/knowyourzone/\" target=\"_blank\" rel=\"noopener\">floridadisaster.org/knowyourzone</a> for other Florida counties.</p>";
        }
        if (d.zone_info) html += '<p class="note">County note: ' + esc(d.zone_info) + "</p>";
        if (d.shelters && d.shelters.length) {
          html += "<h4 style=\"margin-top:18px\">Nearest designated hurricane shelter sites (Escambia County)</h4><div class=\"table-wrap\"><table><thead><tr><th>Shelter</th><th>Address</th><th>Distance</th></tr></thead><tbody>" +
            d.shelters.map(function (s) { return "<tr><td><strong>" + esc(s.name) + "</strong><br><span class=\"small muted\">" + esc(s.type) + "</span></td><td>" + esc(s.address) + "</td><td>" + esc(s.miles) + " mi</td></tr>"; }).join("") +
            "</tbody></table></div><p class=\"note\"><strong>Not every shelter opens for every storm.</strong> Confirm which shelters are open before you leave at <a href=\"https://myescambia.com/stormcenter\" target=\"_blank\" rel=\"noopener\">myescambia.com/stormcenter</a> or by calling 311/211.</p>";
        }
        html += '<p class="note">Zones come from the county\'s public GIS layers and are for planning. Evacuation orders are issued by zone — always follow the order your county actually issues.</p>';
        zoneOut.innerHTML = html;
      }).catch(function () {
        zoneOut.innerHTML = '<p>The lookup service did not respond. Use the official <a href="https://myescambia.com/apps/knowyourzone/" target="_blank" rel="noopener">Escambia County Know Your Zone map</a>, <a href="https://www.santarosa.fl.gov/974/Emergency-Management" target="_blank" rel="noopener">Santa Rosa County Emergency Management</a> or <a href="https://www.floridadisaster.org/knowyourzone/" target="_blank" rel="noopener">floridadisaster.org/knowyourzone</a>.</p>';
      });
    });
  }

  /* ---------- Preparedness checklist generator ---------- */
  var ckForm = $("[data-checklist-form]");
  if (ckForm) {
    var ckOut = $("[data-checklist-out]");
    function buildChecklist() {
      var f = ckForm;
      var people = Math.max(1, num(f.people.value, 1)), pets = Math.max(0, num(f.pets.value, 0)), days = Math.max(3, num(f.days.value, 7));
      var home = f.home.value, zone = f.zone.value;
      var infants = f.infants.checked, seniors = f.seniors.checked, medical = f.medical.checked, meds = f.meds.checked, boat = f.boat.checked, pool = f.pool.checked;
      var water = people * days + pets * Math.ceil(days / 2);
      var sections = [];
      sections.push(["Water & food (" + days + " days)", [
        water + " gallons of drinking water (1 gal per person per day" + (pets ? " plus pets" : "") + ")",
        "Extra water for sanitation: fill bathtubs and large containers before landfall",
        (people * days * 3) + " ready-to-eat meals (canned, pouches, peanut butter, crackers)",
        "Manual can opener, paper plates, utensils and trash bags",
        "Cooler and ice packs; freeze water jugs 48 hours ahead"
      ]]);
      var med = ["First-aid kit and a 2-week supply of prescriptions", "Copies of prescriptions and a list of doctors and pharmacies", "Glasses, contacts, hearing-aid batteries"];
      if (meds) med.push("Insulin or refrigerated medicines: insulated bag + ice plan; ask your pharmacy about early refills (Florida allows early refills during a declared emergency)");
      if (medical) med.push("Power-dependent medical equipment: backup batteries, generator plan, and register with your county's special-needs shelter program before the storm");
      sections.push(["Health & medical", med]);
      var power = ["Flashlights and headlamps (one per person) + spare batteries", "NOAA weather radio (battery or hand-crank)", "Power banks charged for every phone", "Cash in small bills — ATMs and card readers fail without power"];
      if (home !== "mobile") power.push("Generator: fuel, heavy-duty extension cords, and a carbon-monoxide alarm. Never run it indoors or in the garage");
      sections.push(["Power & communication", power]);
      var docs = ["Insurance policies (homeowners, wind, flood) — photo copies in the cloud", "Photo/video walk-through of every room, closet and the roof before the storm", "IDs, deeds/lease, vehicle titles, bank info in a waterproof bag", "Contractor, adjuster and insurer phone numbers written down on paper"];
      sections.push(["Documents & insurance", docs]);
      var prop = [];
      if (home === "house") prop.push("Install shutters or pre-cut 5/8\" plywood on windows and glass doors", "Brace garage door", "Clear gutters and trim weak limbs", "Bring in or tie down patio furniture, grills and trash cans");
      if (home === "condo") prop.push("Know your building's evacuation and elevator shut-off plan", "Bring in balcony furniture and plants", "Move valuables away from sliding doors");
      if (home === "mobile") prop.push("Mobile and manufactured homes are unsafe in hurricane winds — plan to evacuate for every hurricane, regardless of zone", "Check tie-downs and anchors now");
      if (home === "rental") prop.push("Ask your landlord about shutters; photograph the unit's condition", "Renters insurance covers belongings — the landlord's policy does not");
      if (pool) prop.push("Leave the pool full; add extra chlorine and turn off pump power");
      if (boat) prop.push("Haul out or move the boat to a hurricane hole early; marinas and lifts fill quickly");
      prop.push("Move valuables and electronics off the floor in case of flooding", "Know how to shut off your main water valve and electricity");
      sections.push(["Protect the property", prop]);
      var evac = ["Fill vehicle fuel tanks when a storm is 5 days out", "Pick a destination north of I-10 or inland and a backup route"];
      if (zone === "A" || zone === "B") evac.unshift("You are in Zone " + zone + ": plan to leave early. Pensacola Beach, Perdido Key and Navarre Beach bridges may close once winds reach about 40 mph");
      if (zone === "unknown") evac.unshift("Look up your evacuation zone with our Zone Checker before the storm");
      sections.push(["Evacuation plan", evac]);
      if (pets) sections.push(["Pets (" + pets + ")", [Math.ceil(pets * days / 2) + " gallons of extra water for pets", days + " days of pet food + bowls", "Carriers/crates, leashes, ID tags and microchip info", "Vaccination records (pet-friendly shelters require them)", "Confirm a pet-friendly shelter or hotel ahead of time"]]);
      if (infants) sections.push(["Infants & children", ["Formula, bottles, diapers and wipes for " + days + " days", "Comfort items, games and books that need no power", "Child medications and copies of records"]]);
      if (seniors) sections.push(["Older adults", ["Mobility aids, spare batteries for hearing aids and scooters", "A check-in buddy who will call before and after the storm", "Register with the special-needs shelter program if you need care"]]);
      ckOut.innerHTML = '<div class="result"><div class="big">' + sections.reduce(function (a, s) { return a + s[1].length; }, 0) + ' items</div><p style="margin:0">Personalized for ' + people + " " + (people === 1 ? "person" : "people") + (pets ? ", " + pets + " pet" + (pets > 1 ? "s" : "") : "") + ", " + days + " days of self-sufficiency.</p></div>" +
        '<div class="checklist-out">' + sections.map(function (s, i) {
          return "<h4>" + esc(s[0]) + "</h4><ul>" + s[1].map(function (item, j) { var id = "ck-" + i + "-" + j; return '<li><input type="checkbox" id="' + id + '"><label for="' + id + '">' + esc(item) + "</label></li>"; }).join("") + "</ul>";
        }).join("") + '</div><div class="btn-row no-print"><button type="button" class="btn btn-dark" onclick="window.print()">Print checklist</button></div>';
    }
    ckForm.addEventListener("submit", function (e) { e.preventDefault(); buildChecklist(); });
  }

  /* ---------- Preparedness cost calculator ---------- */
  var costForm = $("[data-cost-form]");
  if (costForm) {
    var costOut = $("[data-cost-out]");
    function costCalc() {
      var f = costForm, p = Math.max(1, num(f.people.value, 1)), d = Math.max(3, num(f.days.value, 7)), pets = Math.max(0, num(f.pets.value, 0));
      var rows = [];
      rows.push(["Drinking water (" + (p * d) + " gal)", p * d * 1.6]);
      rows.push(["Non-perishable food", p * d * 14]);
      if (pets) rows.push(["Pet food & water", pets * d * 3]);
      rows.push(["First-aid kit & medicine refills", 45 + p * 10]);
      rows.push(["Flashlights, batteries, power banks, radio", 85 + p * 15]);
      if (f.shutters.value === "plywood") rows.push(["Plywood & hardware (" + num(f.windows.value) + " windows)", num(f.windows.value) * 55]);
      if (f.shutters.value === "panels") rows.push(["Storm panels (" + num(f.windows.value) + " windows)", num(f.windows.value) * 160]);
      if (f.generator.value === "portable") rows.push(["Portable generator + cords + CO alarm", 1050]);
      if (f.generator.value === "inverter") rows.push(["Inverter generator + cords + CO alarm", 1450]);
      if (f.generator.value !== "none") rows.push(["Generator fuel (" + d + " days)", d * 8 * 0.75 * 3.4]);
      if (f.evac.value === "hotel") rows.push(["Evacuation: hotel " + Math.min(d, 4) + " nights + meals + gas", Math.min(d, 4) * (160 + p * 45) + 90]);
      if (f.evac.value === "family") rows.push(["Evacuation: gas + meals on the road", 90 + p * 40]);
      rows.push(["Tarps, rope, trash bags, cleanup gloves", 75]);
      var total = rows.reduce(function (a, r) { return a + r[1]; }, 0);
      costOut.innerHTML = '<div class="result"><div class="small muted">Estimated hurricane preparation budget</div><div class="big">' + money(total) + '</div><div class="table-wrap"><table><tbody>' +
        rows.map(function (r) { return "<tr><td>" + esc(r[0]) + "</td><td style=\"text-align:right\">" + money(r[1]) + "</td></tr>"; }).join("") +
        '</tbody></table></div><p class="note">Typical 2026 Pensacola-area retail prices; actual costs vary. Florida\'s disaster-preparedness sales tax exemptions, when in effect, can lower the cost of many of these items.</p></div>';
    }
    costForm.addEventListener("input", costCalc); costCalc();
  }

  /* ---------- Hurricane deductible calculator ---------- */
  var dedForm = $("[data-deductible-form]");
  if (dedForm) {
    var dedOut = $("[data-deductible-out]");
    function dedCalc() {
      var f = dedForm, covA = num(f.coverage.value), pct = num(f.percent.value), dmg = num(f.damage.value), flat = num(f.flat.value);
      var ded = f.type.value === "flat" ? flat : covA * pct / 100;
      var payout = Math.max(0, dmg - ded);
      dedOut.innerHTML = '<div class="result"><div class="grid grid-2"><div><div class="small muted">Your hurricane deductible</div><div class="big">' + money(ded) + '</div></div><div><div class="small muted">Estimated insurer payment</div><div class="big">' + money(payout) + "</div></div></div>" +
        "<p style=\"margin-top:12px\">" + (dmg <= ded ? "<strong>Your estimated damage is below your hurricane deductible</strong>, so the policy would likely pay nothing for this event. Keep records anyway — Florida applies the hurricane deductible once per calendar year, so later storms may be covered." : "You would pay the first " + money(ded) + " and the insurer would owe about " + money(payout) + ", before depreciation, policy limits and exclusions.") + "</p>" +
        '<p class="note">Flood damage is never covered by a homeowners policy. It needs a separate NFIP or private flood policy with its own deductible.</p></div>';
    }
    dedForm.addEventListener("input", dedCalc); dedCalc();
  }

  /* ---------- Emergency supply calculator ---------- */
  var supForm = $("[data-supply-form]");
  if (supForm) {
    var supOut = $("[data-supply-out]");
    function supCalc() {
      var f = supForm, a = num(f.adults.value), k = num(f.kids.value), dg = num(f.dogs.value), ct = num(f.cats.value), d = Math.max(1, num(f.days.value, 7));
      var people = a + k;
      var water = people * d + dg * d * 0.5 + ct * d * 0.15;
      var meals = people * d * 3;
      var rows = [
        ["Drinking water", Math.ceil(water) + " gallons", "≈ " + Math.ceil(water / 2.5) + " cases of 2.5-gal jugs or " + Math.ceil(water * 128 / 16.9 / 24) + " cases of 24 × 16.9 oz bottles"],
        ["Meals", meals + " meals", "≈ " + Math.ceil(meals * 0.6) + " cans + " + Math.ceil(meals * 0.4) + " shelf-stable pouches/boxes"],
        ["Batteries (AA/AAA)", (people * 8 + 8) + " cells", "For flashlights, radios, fans"],
        ["Power banks", Math.max(1, people) + " × 10,000 mAh+", "One full phone charge ≈ 3,000–4,000 mAh"],
        ["Trash bags", Math.ceil(d * 1.5) + " heavy-duty", "Also useful as emergency rain covers"],
        ["Paper towels / wipes", Math.ceil(people * d / 3) + " rolls/packs", "Water may be off or under a boil notice"],
        ["Cash", "$" + (people * 100 + 100), "Small bills"]
      ];
      if (dg) rows.push(["Dog food", Math.ceil(dg * d * 0.6) + " lb (avg dog)", "Plus " + Math.ceil(dg * d * 0.5) + " gal water"]);
      if (ct) rows.push(["Cat food & litter", Math.ceil(ct * d * 0.15) + " lb food, " + Math.ceil(ct * d * 0.7) + " lb litter", "Plus " + Math.ceil(ct * d * 0.15) + " gal water"]);
      supOut.innerHTML = '<div class="result"><div class="table-wrap"><table><thead><tr><th>Item</th><th>Amount</th><th>How to buy it</th></tr></thead><tbody>' + rows.map(function (r) { return "<tr><td><strong>" + r[0] + "</strong></td><td>" + r[1] + "</td><td>" + r[2] + "</td></tr>"; }).join("") + "</tbody></table></div></div>";
    }
    supForm.addEventListener("input", supCalc); supCalc();
  }

  /* ---------- Generator runtime calculator ---------- */
  var genForm = $("[data-generator-form]");
  if (genForm) {
    var genOut = $("[data-generator-out]");
    var loads = { fridge: 200, freezer: 150, fan: 75, lights: 60, tv: 120, router: 20, phone: 30, window_ac: 900, microwave: 1000, cpap: 60, well: 1000, sump: 800 };
    function genCalc() {
      var f = genForm, rated = num(f.rated.value), tank = num(f.tank.value), fuel = f.fuel.value, watts = 0, startPeak = 0;
      Object.keys(loads).forEach(function (k) { var el = f.elements[k]; if (el && el.checked) { watts += loads[k]; if (/fridge|freezer|window_ac|well|sump/.test(k)) startPeak = Math.max(startPeak, loads[k] * 2); } });
      watts += num(f.other.value);
      var loadPct = rated ? Math.min(1, watts / rated) : 0;
      // Typical portable-generator consumption: ~0.15 gal/hr per kW at idle plus ~0.55 gal/hr per kW of load (gasoline).
      var galPerHr = rated ? (0.15 * rated / 1000 + 0.55 * watts / 1000) : 0;
      if (fuel === "propane") galPerHr *= 1.35;
      if (fuel === "diesel") galPerHr *= 0.75;
      var hours = galPerHr ? tank / galPerHr : 0;
      var fuelFor7 = galPerHr * 12 * 7;
      genOut.innerHTML = '<div class="result"><div class="grid grid-3"><div><div class="small muted">Running load</div><div class="big">' + watts.toLocaleString() + ' W</div></div><div><div class="small muted">Runtime per tank</div><div class="big">' + (hours ? hours.toFixed(1) + " h" : "—") + '</div></div><div><div class="small muted">Fuel for 7 days (12 h/day)</div><div class="big">' + Math.ceil(fuelFor7) + " gal</div></div></div>" +
        (watts + startPeak > rated ? '<p style="margin-top:12px"><strong>Warning:</strong> running load plus motor start-up surge (≈' + (watts + startPeak).toLocaleString() + " W) exceeds the generator's " + rated.toLocaleString() + " W rating. Stagger start-ups or drop a load.</p>" : '<p style="margin-top:12px">Load is about ' + Math.round(loadPct * 100) + "% of rated output — " + (loadPct > 0.8 ? "high; expect shorter runtime and more wear." : "a comfortable range.") + "</p>") +
        '<p class="note">Estimates only. Store fuel safely, keep the generator 20+ feet from doors and windows, and use a working CO alarm. Gas stations across Escambia and Santa Rosa often run dry before landfall.</p></div>';
    }
    genForm.addEventListener("input", genCalc); genCalc();
  }

  /* ---------- Storm damage documentation log (stored only in this browser) ---------- */
  var logRoot = $("[data-damage-log]");
  if (logRoot) {
    var KEY = "ph-damage-log-v1", items = [];
    try { items = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { items = []; }
    var logForm = $("[data-damage-form]"), list = $("[data-damage-list]");
    function save() { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) { /* private mode */ } }
    function render() {
      if (!items.length) { list.innerHTML = '<p class="muted">No entries yet. Add one item per damaged area or object.</p>'; return; }
      var total = items.reduce(function (a, i) { return a + num(i.cost); }, 0);
      list.innerHTML = '<div class="table-wrap"><table><thead><tr><th>Date</th><th>Area / item</th><th>Damage &amp; cause</th><th>Photos</th><th>Est. cost</th><th class="no-print"></th></tr></thead><tbody>' +
        items.map(function (i, idx) { return "<tr><td>" + esc(i.date) + "</td><td>" + esc(i.area) + "</td><td>" + esc(i.desc) + "<br><span class=\"small muted\">" + esc(i.cause) + "</span></td><td>" + esc(i.photos) + "</td><td>" + money(num(i.cost)) + '</td><td class="no-print"><button type="button" data-del="' + idx + '" class="btn btn-outline" style="padding:4px 10px;font-size:.8rem">Remove</button></td></tr>'; }).join("") +
        '<tr><td colspan="4"><strong>Total estimated loss</strong></td><td><strong>' + money(total) + '</strong></td><td class="no-print"></td></tr></tbody></table></div>';
    }
    list.addEventListener("click", function (e) { var b = e.target.closest("[data-del]"); if (b) { items.splice(+b.getAttribute("data-del"), 1); save(); render(); } });
    logForm.addEventListener("submit", function (e) {
      e.preventDefault();
      items.push({ date: logForm.date.value, area: logForm.area.value, desc: logForm.desc.value, cause: logForm.cause.value, photos: logForm.photos.value, cost: logForm.cost.value });
      save(); render(); logForm.reset();
    });
    $("[data-damage-print]").addEventListener("click", function () { window.print(); });
    $("[data-damage-csv]").addEventListener("click", function () {
      var csv = "Date,Area,Description,Cause,Photos,Estimated cost\n" + items.map(function (i) { return [i.date, i.area, i.desc, i.cause, i.photos, i.cost].map(function (v) { return '"' + String(v || "").replace(/"/g, '""') + '"'; }).join(","); }).join("\n");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
      a.download = "hurricane-damage-log.csv"; document.body.appendChild(a); a.click(); a.remove();
    });
    render();
  }

  /* ---------- Alerts sign-up ---------- */
  $$("[data-subscribe-form]").forEach(function (f) {
    var out = f.querySelector("[data-subscribe-out]");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      out.textContent = "Saving…";
      var body = new URLSearchParams(new FormData(f));
      fetch("/api/subscribe.php", { method: "POST", body: body }).then(function (r) { return r.json(); }).then(function (d) {
        out.innerHTML = d.ok ? "<strong>You're on the list.</strong> We'll send Pensacola storm updates to " + esc(d.email) + ". You can unsubscribe from any message." : "<strong>" + esc(d.error || "Something went wrong.") + "</strong>";
        if (d.ok) f.reset();
      }).catch(function () { out.textContent = "Could not save right now — please try again in a minute."; });
    });
  });

  /* ---------- Free case review (lead) forms ---------- */
  $$("[data-lead-form]").forEach(function (f) {
    var out = f.querySelector("[data-lead-out]"), btn = f.querySelector("button[type=submit]");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      out.className = "lead-out"; out.textContent = "Sending\u2026"; btn.disabled = true;
      var body = new URLSearchParams(new FormData(f));
      body.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: body }).then(function (r) { return r.json(); }).then(function (d) {
        if (d.ok) {
          out.innerHTML = "<strong>Thank you, " + esc(d.name) + ".</strong> Your request was received. A member of The Lawgical Firm's team will contact you shortly. For immediate help call <a href=\"tel:+14074334131\">(407) 433-4131</a>.";
          f.querySelectorAll("input:not([type=checkbox]), textarea").forEach(function (el) { el.value = ""; });
          if (window.gtag) window.gtag("event", "generate_lead");
        } else { out.className = "lead-out is-error"; out.textContent = d.error || "Something went wrong. Please call (407) 433-4131."; }
      }).catch(function () { out.className = "lead-out is-error"; out.textContent = "We couldn't send your request. Please call (407) 433-4131."; })
        .then(function () { btn.disabled = false; });
    });
  });

  /* ---------- Tabs ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
    var btns = $$("[role=tab]", wrap);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); var p = document.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = x !== b; });
      });
    });
  });
})();
