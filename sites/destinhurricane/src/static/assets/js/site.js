/* Destin Hurricane - page behaviour. Every feature looks for its data-* hook
   and does nothing when the hook is absent.
   Live sources: api.weather.gov (CORS, fetched in the browser) and the NHC,
   proxied through /api/storms.php and /api/nhc-feed.php. Evacuation zones and
   Okaloosa shelter status come from /api/zone.php. */
(function () {
  "use strict";

  var DESTIN = { lat: 30.3935, lon: -86.4958, label: "Destin" };
  var MIRAMAR = { lat: 30.3740, lon: -86.3590 };         // Walton County side (NWS Tallahassee)
  var NWS = "https://api.weather.gov";
  var PHONE = "(850) 203-3385", TEL = "+18502033385";

  function q(sel, root) { return (root || document).querySelector(sel); }
  function qa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function usd(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
  function val(v, fallback) { var n = parseFloat(String(v).replace(/[^0-9.\-]/g, "")); return isNaN(n) ? (fallback || 0) : n; }
  function json(url) {
    return fetch(url, { headers: { Accept: "application/geo+json, application/json" } }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    });
  }
  function when(iso) {
    try {
      return new Date(iso).toLocaleString("en-US", { timeZone: "America/Chicago", weekday: "short", month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }) + " CT";
    } catch (e) { return iso; }
  }
  function miles(lat1, lon1, lat2, lon2) {
    var r = Math.PI / 180, dLat = (lat2 - lat1) * r, dLon = (lon2 - lon1) * r;
    var h = Math.pow(Math.sin(dLat / 2), 2) + Math.cos(lat1 * r) * Math.cos(lat2 * r) * Math.pow(Math.sin(dLon / 2), 2);
    return 7917.6 * Math.asin(Math.sqrt(h));
  }
  function heading(deg) {
    var pts = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
    return pts[Math.round((deg % 360) / 22.5) % 16];
  }
  function saffir(kt) {
    kt = +kt;
    return kt >= 137 ? "Cat 5" : kt >= 113 ? "Cat 4" : kt >= 96 ? "Cat 3" : kt >= 83 ? "Cat 2" : kt >= 64 ? "Cat 1" : kt >= 34 ? "Tropical storm" : "Depression";
  }
  var KIND = { HU: "Hurricane", TS: "Tropical Storm", TD: "Tropical Depression", STS: "Subtropical Storm", STD: "Subtropical Depression", PTC: "Potential Tropical Cyclone", PC: "Post-Tropical Cyclone" };

  /* ---------------- mobile navigation panel ---------------- */
  var mast = q("[data-mast]"), burger = q("[data-menu-btn]"), panel = q("[data-nav]"), scrim = q("[data-nav-scrim]");
  var wide = window.matchMedia("(min-width: 1080px)");
  function isOpen() { return panel && panel.classList.contains("is-open"); }
  function toggleNav(open) {
    if (!burger || !panel) return;
    if (open) {
      document.documentElement.style.setProperty("--drawer-top", Math.round(mast.getBoundingClientRect().bottom) + "px");
      scrim.hidden = false;
      requestAnimationFrame(function () { scrim.classList.add("is-on"); });
    } else {
      scrim.classList.remove("is-on");
      setTimeout(function () { if (!isOpen()) scrim.hidden = true; }, 220);
    }
    panel.classList.toggle("is-open", open);
    document.documentElement.classList.toggle("menu-open", open);
    burger.setAttribute("aria-expanded", String(open));
    q(".burger-label", burger).textContent = open ? "Close" : "Menu";
    if (open) { var first = q("a", panel); if (first) first.focus({ preventScroll: true }); }
  }
  if (burger && panel) {
    burger.addEventListener("click", function () { toggleNav(!isOpen()); });
    scrim.addEventListener("click", function () { toggleNav(false); });
    panel.addEventListener("click", function (e) { if (e.target.closest("a") && isOpen()) toggleNav(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && isOpen()) { toggleNav(false); burger.focus(); } });
    var onWide = function () { if (wide.matches && isOpen()) toggleNav(false); };
    if (wide.addEventListener) wide.addEventListener("change", onWide); else if (wide.addListener) wide.addListener(onWide);
    window.addEventListener("pageshow", function () { if (isOpen()) toggleNav(false); });
  }

  /* ---------------- header shadow + back to top ---------------- */
  var totop = q("[data-totop]"), queued = false;
  function onScroll() {
    queued = false;
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (mast) mast.classList.toggle("is-raised", y > 24);
    if (totop) totop.classList.toggle("is-on", y > 900);
  }
  window.addEventListener("scroll", function () { if (!queued) { queued = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (totop) totop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: "smooth" }); q("#content").focus({ preventScroll: true }); });

  /* ---------------- gentle reveal ---------------- */
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window) {
    var targets = qa(".tile, .place, .fact, .rows > li, .deadline, .person, .pair, .timeline > li, .toolcard, .claimcard");
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.05 });
    targets.forEach(function (el) {
      var sibs = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.setProperty("--d", Math.min(sibs, 5));
      el.classList.add("rise");
      io.observe(el);
    });
    document.documentElement.classList.add("motion");
    window.addEventListener("beforeprint", function () { targets.forEach(function (el) { el.classList.add("is-in"); }); });
    setTimeout(function () { targets.forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) el.classList.add("is-in"); }); }, 900);
  }

  /* ---------------- NWS alerts: Destin (NWS Mobile) + Miramar Beach (NWS Tallahassee) ---------------- */
  var alertsCache = null;
  function coastAlerts() {
    if (!alertsCache) {
      alertsCache = Promise.all([DESTIN, MIRAMAR].map(function (p) {
        return json(NWS + "/alerts/active?point=" + p.lat + "," + p.lon).then(function (d) { return d.features || []; }).catch(function () { return null; });
      })).then(function (lists) {
        if (lists[0] === null && lists[1] === null) throw new Error("NWS unreachable");
        var seen = {}, out = [];
        lists.forEach(function (l) { (l || []).forEach(function (f) { if (!seen[f.id]) { seen[f.id] = 1; out.push(f); } }); });
        var rank = { Extreme: 4, Severe: 3, Moderate: 2, Minor: 1 };
        return out.sort(function (a, b) { return (rank[b.properties.severity] || 0) - (rank[a.properties.severity] || 0); });
      });
    }
    return alertsCache;
  }
  var strip = q("[data-alertbar]");
  if (strip) {
    var stripText = q("[data-alertbar-text]");
    coastAlerts().then(function (list) {
      if (!list.length) { stripText.textContent = "No National Weather Service watches or warnings for Destin or South Walton right now."; return; }
      var names = [];
      list.forEach(function (f) { if (names.indexOf(f.properties.event) < 0) names.push(f.properties.event); });
      if (/Warning/.test(names[0])) strip.classList.add("is-warning"); else if (/Watch/.test(names[0])) strip.classList.add("is-watch");
      stripText.innerHTML = "<strong>Now in effect:</strong> " + esc(names.slice(0, 3).join(" · ")) + (names.length > 3 ? " +" + (names.length - 3) + " more" : "");
    }).catch(function () { stripText.textContent = "Live NWS alerts did not load. Check weather.gov/mob for Okaloosa and weather.gov/tae for Walton."; });
  }
  qa("[data-nws-alerts]").forEach(function (box) {
    coastAlerts().then(function (list) {
      if (!list.length) { box.innerHTML = '<div class="calm"><h3>No active alerts</h3><p>NWS Mobile (Okaloosa) and NWS Tallahassee (Walton) have no watches, warnings or advisories in effect for Destin or Miramar Beach. Reload for the latest.</p></div>'; return; }
      box.innerHTML = list.map(function (f) {
        var p = f.properties;
        return '<article class="wxalert sev-' + esc(p.severity) + '"><h3>' + esc(p.event) + '</h3><div class="small muted">' + esc(p.senderName) + " · issued " + esc(when(p.sent)) + (p.ends || p.expires ? " · until " + esc(when(p.ends || p.expires)) : "") + "</div>" +
          (p.headline ? "<p>" + esc(p.headline) + "</p>" : "") + "<details><summary>Read the full alert</summary><pre>" + esc((p.description || "") + "\n\n" + (p.instruction || "")) + "</pre></details></article>";
      }).join("");
    }).catch(function () { box.innerHTML = '<p class="muted">The National Weather Service did not respond. Open <a href="https://www.weather.gov/mob/">weather.gov/mob</a> or <a href="https://www.weather.gov/tae/">weather.gov/tae</a>.</p>'; });
  });

  /* ---------------- active storms (NHC) ---------------- */
  qa("[data-storms]").forEach(function (box) {
    var mini = box.hasAttribute("data-compact");
    json("/api/storms.php").then(function (d) {
      var storms = (d.activeStorms || []).filter(function (s) { return /^al/i.test(s.id); });
      if (!storms.length) {
        box.innerHTML = '<div class="calm"><h3>No named storms in the Atlantic or Gulf</h3><p>The National Hurricane Center is not tracking an active Atlantic-basin system right now. ' + (mini ? 'See the <a href="/destin-hurricane-tracker/">7-day outlook</a>.' : "The outlook maps below show areas being watched.") + "</p></div>";
        return;
      }
      storms.sort(function (a, b) { return miles(DESTIN.lat, DESTIN.lon, a.latitudeNumeric, a.longitudeNumeric) - miles(DESTIN.lat, DESTIN.lon, b.latitudeNumeric, b.longitudeNumeric); });
      box.innerHTML = storms.map(function (s) {
        var mph = Math.round(s.intensity * 1.15078 / 5) * 5;
        var away = Math.round(miles(DESTIN.lat, DESTIN.lon, s.latitudeNumeric, s.longitudeNumeric));
        var name = (KIND[s.classification] || s.classification) + " " + s.name;
        var adv = s.publicAdvisory ? s.publicAdvisory.advNum : "";
        if (mini) {
          return '<div class="storm-mini"><span class="livetag">Active</span><h3>' + esc(name) + "</h3><p>" + mph + " mph · " + away.toLocaleString() + " mi from Destin · moving " + heading(s.movementDir) + " " + esc(s.movementSpeed) + " mph</p><p class=\"small muted\">NHC advisory " + esc(adv) + " · " + esc(when(s.lastUpdate)) + "</p></div>";
        }
        var num = s.id.substr(2, 2);
        var cone = "https://www.nhc.noaa.gov/storm_graphics/AT" + num + "/" + s.id.toUpperCase() + "_5day_cone.png";
        var links = [["Public advisory", s.publicAdvisory], ["Discussion", s.forecastDiscussion], ["Wind odds", s.windSpeedProbabilities], ["All graphics", s.forecastGraphics]]
          .filter(function (l) { return l[1] && l[1].url; })
          .map(function (l) { return '<a href="' + esc(l[1].url) + '" target="_blank" rel="noopener">' + l[0] + "</a>"; }).join("");
        return '<article class="storm"><div class="storm-top"><div><span class="livetag">Live from NHC</span><h3>' + esc(name) + '</h3><div class="small">Updated ' + esc(when(s.lastUpdate)) + '</div></div><div class="storm-cat">' + esc(s.classification === "HU" ? saffir(s.intensity) : (KIND[s.classification] || "")) + "</div></div>" +
          '<div class="storm-body"><div><div class="kv">' +
          "<div><span>Wind</span><b>" + mph + " mph</b></div><div><span>Pressure</span><b>" + esc(s.pressure) + " mb</b></div>" +
          "<div><span>Moving</span><b>" + heading(s.movementDir) + " " + esc(s.movementSpeed) + " mph</b></div><div><span>To Destin</span><b>" + away.toLocaleString() + " mi</b></div>" +
          "<div><span>Center</span><b>" + esc(s.latitude + " " + s.longitude) + "</b></div><div><span>Advisory</span><b>#" + esc(adv || "-") + "</b></div>" +
          '</div><div class="storm-links">' + links + '</div><p class="note">Miles are measured from Destin to the center. Wind, surge and rain reach far beyond the center.</p></div>' +
          '<figure style="margin:0"><a href="' + esc(cone) + '" target="_blank" rel="noopener"><img src="' + esc(cone) + '" alt="NHC five-day forecast cone for ' + esc(name) + '" loading="lazy" onerror="this.closest(\'figure\').hidden=true"></a><figcaption class="note">NHC five-day cone: the likely path of the center only.</figcaption></figure></div></article>';
      }).join("");
    }).catch(function () {
      box.innerHTML = '<div class="calm"><h3>Storm data did not load</h3><p>Go straight to <a href="https://www.nhc.noaa.gov/">hurricanes.gov</a> for the latest advisory.</p></div>';
    });
  });

  /* ---------------- NHC product feed + NWS text products ---------------- */
  qa("[data-nhc-feed]").forEach(function (box) {
    json("/api/nhc-feed.php").then(function (d) {
      var items = (d.items || []).slice(0, 10);
      box.innerHTML = items.length ? items.map(function (it) {
        return '<div class="feeditem"><a href="' + esc(it.link) + '" target="_blank" rel="noopener">' + esc(it.title) + '</a><div class="small muted">' + esc(it.pubDate) + "</div></div>";
      }).join("") : '<p class="muted">The NHC has no Atlantic products posted right now.</p>';
    }).catch(function () { box.innerHTML = '<p class="muted">The NHC feed is unavailable. Visit <a href="https://www.nhc.noaa.gov/">nhc.noaa.gov</a>.</p>'; });
  });
  qa("[data-nws-product]").forEach(function (box) {
    var type = box.getAttribute("data-nws-product"), office = box.getAttribute("data-office") || "MOB";
    var officeName = office === "TAE" ? "NWS Tallahassee" : "NWS Mobile";
    json(NWS + "/products/types/" + type + "/locations/" + office).then(function (d) {
      var g = d["@graph"] || [];
      if (!g.length) { box.innerHTML = '<p class="muted">' + officeName + " has no recent " + esc(type) + " product.</p>"; return; }
      return json(g[0]["@id"]).then(function (p) {
        var hrs = (Date.now() - new Date(p.issuanceTime).getTime()) / 36e5;
        box.innerHTML = '<p class="small muted">' + esc(p.productName) + " · " + officeName + " · issued " + esc(when(p.issuanceTime)) + (hrs > 72 ? " (no newer statement since)" : "") + '</p><div class="product-text">' + esc(p.productText) + "</div>";
      });
    }).catch(function () { box.innerHTML = '<p class="muted">Product unavailable. See <a href="https://www.weather.gov/' + office.toLowerCase() + '/">weather.gov/' + office.toLowerCase() + "</a>.</p>"; });
  });

  /* ---------------- weather desk ---------------- */
  function toF(c) { return c == null ? null : Math.round(c * 9 / 5 + 32); }
  function toMph(k) { return k == null ? null : Math.round(k * 0.621371); }
  var nowBox = q("[data-wx-current]");
  if (nowBox) {
    json(NWS + "/stations/KDTS/observations/latest").then(function (d) {
      var p = d.properties, t = toF(p.temperature.value), w = toMph(p.windSpeed.value), g = toMph(p.windGust.value);
      var inHg = p.barometricPressure.value ? (p.barometricPressure.value / 3386.39).toFixed(2) : null;
      nowBox.innerHTML = '<div class="wxnow">' + (p.icon ? '<img src="' + esc(p.icon.replace("size=medium", "size=large")) + '" alt="" width="84" height="84">' : "") +
        '<div><div class="wxtemp">' + (t != null ? t + "°" : "–") + "</div><strong>" + esc(p.textDescription || "") + "</strong></div></div>" +
        '<div class="kv" style="margin-top:16px"><div><span>Wind</span><b>' + (w != null ? (p.windDirection.value != null ? heading(p.windDirection.value) + " " : "") + w + " mph" : "Calm") + "</b></div>" +
        "<div><span>Gusts</span><b>" + (g ? g + " mph" : "–") + "</b></div><div><span>Humidity</span><b>" + (p.relativeHumidity.value != null ? Math.round(p.relativeHumidity.value) + "%" : "–") + "</b></div>" +
        "<div><span>Pressure</span><b>" + (inHg ? inHg + " in" : "–") + "</b></div><div><span>Dew point</span><b>" + (p.dewpoint.value != null ? toF(p.dewpoint.value) + "°" : "–") + "</b></div><div><span>Visibility</span><b>" + (p.visibility.value != null ? Math.round(p.visibility.value / 1609) + " mi" : "–") + "</b></div></div>" +
        '<p class="note">Destin Executive Airport (KDTS) · observed ' + esc(when(p.timestamp)) + "</p>";
    }).catch(function () { nowBox.innerHTML = '<p class="muted">Current conditions are unavailable right now.</p>'; });
  }
  var gridPromise = null;
  function gridPoint() { if (!gridPromise) gridPromise = json(NWS + "/points/" + DESTIN.lat + "," + DESTIN.lon).then(function (d) { return d.properties; }); return gridPromise; }
  var fcBox = q("[data-wx-forecast]");
  if (fcBox) {
    gridPoint().then(function (p) { return json(p.forecast); }).then(function (d) {
      var per = d.properties.periods || [];
      fcBox.innerHTML = '<div class="fcrow">' + per.filter(function (x) { return x.isDaytime || x.number === 1; }).slice(0, 7).map(function (x) {
        var rain = x.probabilityOfPrecipitation && x.probabilityOfPrecipitation.value != null ? '<div class="small">Rain ' + x.probabilityOfPrecipitation.value + "%</div>" : "";
        return '<div class="fcday"><b>' + esc(x.name) + '</b><img src="' + esc(x.icon) + '" alt="" loading="lazy"><strong>' + esc(x.temperature) + "°</strong><div>" + esc(x.shortForecast) + '</div><div class="small muted">' + esc(x.windDirection + " " + x.windSpeed) + "</div>" + rain + "</div>";
      }).join("") + '</div><details style="margin-top:14px"><summary><strong>Forecast wording from NWS Mobile</strong></summary>' + per.slice(0, 8).map(function (x) { return "<p><strong>" + esc(x.name) + ":</strong> " + esc(x.detailedForecast) + "</p>"; }).join("") + "</details>";
    }).catch(function () { fcBox.innerHTML = '<p class="muted">Forecast unavailable. Use <a href="https://forecast.weather.gov/MapClick.php?lat=30.3935&amp;lon=-86.4958">forecast.weather.gov</a>.</p>'; });
  }
  function span(validTime) {
    var parts = validTime.split("/"), m = /P(?:(\d+)D)?T?(?:(\d+)H)?/.exec(parts[1] || "PT1H");
    return { start: new Date(parts[0]).getTime(), hours: ((+(m[1] || 0)) * 24 + (+(m[2] || 0))) || 1 };
  }
  var windBox = q("[data-wx-wind]"), rainBox = q("[data-wx-rain]");
  if (windBox || rainBox) {
    gridPoint().then(function (p) { return json(p.forecastGridData); }).then(function (d) {
      var g = d.properties, now = Date.now();
      if (windBox) {
        var hours = [];
        [["w", g.windSpeed], ["g", g.windGust]].forEach(function (pair) {
          ((pair[1] || {}).values || []).forEach(function (v) {
            var t = span(v.validTime);
            for (var h = 0; h < t.hours; h++) {
              var ts = t.start + h * 36e5;
              if (ts < now - 36e5 || ts > now + 72 * 36e5) continue;
              var i = Math.floor((ts - now) / 36e5) + 1;
              hours[i] = hours[i] || { ts: ts };
              hours[i][pair[0]] = toMph(v.value);
            }
          });
        });
        hours = hours.filter(Boolean).slice(0, 72);
        var top = Math.max.apply(null, hours.map(function (h) { return Math.max(h.w || 0, h.g || 0); }).concat([20]));
        var peak = hours.reduce(function (a, h) { return (h.g || 0) > (a.g || 0) ? h : a; }, {});
        windBox.innerHTML = "<p><strong>Highest forecast gust in the next 72 hours: " + (peak.g || "–") + " mph</strong>" + (peak.ts ? " (" + esc(when(new Date(peak.ts).toISOString())) + ")" : "") + "</p>" +
          '<div class="bars" role="img" aria-label="Hourly forecast gusts for Destin over the next 72 hours; peak ' + (peak.g || 0) + ' mph">' + hours.map(function (h) {
            return '<div class="' + ((h.g || 0) >= 39 ? "gust" : "") + '" style="height:' + Math.max(2, ((h.g || h.w || 0) / top) * 100) + '%" title="' + esc(when(new Date(h.ts).toISOString())) + ": " + (h.w || 0) + " mph, gusts " + (h.g || 0) + ' mph"></div>';
          }).join("") + '</div><div class="bars-labels"><span>Now</span><span>+24 h</span><span>+48 h</span><span>+72 h</span></div>' +
          '<p class="note">Each bar is one hour; height is the forecast gust. Coral bars are gusts of 39 mph or more, the tropical-storm threshold. Source: NWS gridded forecast for Destin.</p>';
      }
      if (rainBox) {
        var r24 = 0, r72 = 0, rAll = 0;
        ((g.quantitativePrecipitation || {}).values || []).forEach(function (v) {
          var t = span(v.validTime);
          if (t.start + t.hours * 36e5 < now) return;
          var inches = (v.value || 0) / 25.4, ahead = (t.start - now) / 36e5;
          if (ahead < 24) r24 += inches;
          if (ahead < 72) r72 += inches;
          rAll += inches;
        });
        rainBox.innerHTML = '<div class="facts facts--3" style="margin:0"><div class="fact"><strong>' + r24.toFixed(2) + '"</strong><span>Next 24 hours</span></div><div class="fact"><strong>' + r72.toFixed(2) + '"</strong><span>Next 72 hours</span></div><div class="fact"><strong>' + rAll.toFixed(2) + '"</strong><span>Whole forecast</span></div></div>' +
          '<p class="note">NWS quantitative precipitation forecast for Destin. Tropical rain bands can double these numbers locally.</p>';
      }
    }).catch(function () {
      if (windBox) windBox.innerHTML = '<p class="muted">The wind forecast did not load.</p>';
      if (rainBox) rainBox.innerHTML = '<p class="muted">The rainfall forecast did not load.</p>';
    });
  }

  /* ---------------- evacuation zone lookup ---------------- */
  var zoneForm = q("[data-zone-form]");
  if (zoneForm) {
    var zoneOut = q("[data-zone-result]");
    var OFFICIAL = '<a href="https://myokaloosa.gov/gis_ps" target="_blank" rel="noopener">Okaloosa County zone search</a>, <a href="https://www.waltoncountyem.org/" target="_blank" rel="noopener">Walton County Emergency Management</a> or <a href="https://www.floridadisaster.org/knowyourzone/" target="_blank" rel="noopener">floridadisaster.org/knowyourzone</a>';
    var MEANING = {
      A: "Zone A is ordered out first: the Gulf-front and lowest bayfront land, including the barrier-island beaches. Okaloosa ordered Zones A and B out before Hurricane Isaias.",
      B: "Zone B is the next ring of low ground along Choctawhatchee Bay, the bayous and Santa Rosa Sound. Expect to leave for most hurricane threats.",
      C: "Zone C sits a little higher but can still flood in a strong surge. Orders reach it for stronger or larger storms.",
      D: "Zone D floods only in severe surge scenarios. Watch the county's order for each storm.",
      E: "Zone E is the outermost zone and is ordered out only for the most extreme surge forecasts."
    };
    zoneForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var addr = zoneForm.address.value.trim();
      if (addr.length < 6) { zoneOut.innerHTML = "<p>Type a full street address, such as <em>4100 Legendary Dr, Destin, FL</em>.</p>"; return; }
      zoneOut.innerHTML = '<p class="loading">Matching the address and checking county zone maps…</p>';
      json("/api/zone.php?address=" + encodeURIComponent(addr)).then(function (d) {
        if (d.error) { zoneOut.innerHTML = "<p><strong>" + esc(d.error) + "</strong></p><p>Add the city and ZIP, or use the " + OFFICIAL + ".</p>"; return; }
        var html = "", z = d.zone;
        if (z && /^[A-E]$/.test(z)) {
          html += '<div class="zonebox"><span class="zonebadge zone-' + z + '">' + z + '</span><div><div class="big">Evacuation Zone ' + z + "</div><div class=\"small muted\">" + esc(d.matched) + " · " + esc(d.county) + "</div></div></div><p style=\"margin-top:14px\">" + MEANING[z] + "</p>";
          if (d.conflict) html += '<p class="note"><strong>Check this one:</strong> the county layer labels this area both ' + esc(d.conflict.join(" and ")) + ". We show the more cautious zone. Confirm with Okaloosa County Public Safety at 850-651-7150.</p>";
        } else if (z === "G" || z === "H") {
          html += '<div class="big">Military installation</div><p>' + esc(d.matched) + " lies on " + (z === "G" ? "Eglin Air Force Base" : "Hurlburt Field") + " property. Follow base emergency instructions" + (d.zone_info ? ": " + esc(d.zone_info) : ".") + "</p>";
        } else if (d.supported) {
          html += '<div class="zonebox"><span class="zonebadge zone-none">No<br>zone</span><div><div class="big">Outside the surge zones</div><div class="small muted">' + esc(d.matched) + " · " + esc(d.county) + "</div></div></div><p style=\"margin-top:14px\">County maps do not put this address in a storm-surge evacuation zone. Leave anyway if you live in a mobile or manufactured home or an RV, if your street floods in heavy rain, or if you rely on powered medical equipment.</p>";
        } else {
          html += '<div class="big">' + esc(d.county || "Outside this lookup") + "</div><p>" + esc(d.matched) + "</p><p>This tool covers Okaloosa and Walton counties. For anywhere else in Florida use <a href=\"https://www.floridadisaster.org/knowyourzone/\" target=\"_blank\" rel=\"noopener\">floridadisaster.org/knowyourzone</a>.</p>";
        }
        if (d.source_note) html += '<p class="note">' + esc(d.source_note) + "</p>";
        if (d.shelters && d.shelters.length) {
          html += '<h3 style="margin-top:20px;font-size:1.1rem">Closest county shelter sites</h3><div class="table-scroll"><table><thead><tr><th>Shelter</th><th>Address</th><th>Status (county GIS)</th><th>Distance</th></tr></thead><tbody>' +
            d.shelters.map(function (s) { return "<tr><td><strong>" + esc(s.name) + "</strong></td><td>" + esc(s.address) + "</td><td>" + (s.status ? '<span class="statuspill' + (/open/i.test(s.status) ? " is-open" : "") + '">' + esc(s.status) + "</span>" : "–") + "</td><td>" + esc(s.miles) + " mi</td></tr>"; }).join("") +
            '</tbody></table></div><p class="note">Shelters open only when the county activates them. Confirm before you drive: Okaloosa shelter line 850-609-7000, Walton County EM 850-892-8065.</p>';
        }
        html += '<p class="note">Zone maps are planning tools. Orders are issued storm by storm, by zone. The order your county actually issues is the one to follow.</p>';
        zoneOut.innerHTML = html;
      }).catch(function () { zoneOut.innerHTML = "<p>The lookup did not respond. Use the " + OFFICIAL + ".</p>"; });
    });
  }

  /* ---------------- live Okaloosa shelter list ---------------- */
  qa("[data-shelters]").forEach(function (box) {
    json("/api/zone.php?shelters=1").then(function (d) {
      var list = d.shelters || [];
      if (!list.length) throw new Error("empty");
      box.innerHTML = '<div class="table-scroll"><table><thead><tr><th>Shelter site</th><th>Address</th><th>Status in county GIS</th></tr></thead><tbody>' +
        list.map(function (s) { return "<tr><td><strong>" + esc(s.name) + "</strong></td><td>" + esc(s.address) + "</td><td>" + (s.status ? '<span class="statuspill' + (/open/i.test(s.status) ? " is-open" : "") + '">' + esc(s.status) + "</span>" : "–") + "</td></tr>"; }).join("") +
        '</tbody></table></div><p class="note">Read live from Okaloosa County\'s public shelter layer. The county may update its website, radio and AlertOkaloosa before this layer changes, so call 850-609-7000 before you go.</p>';
    }).catch(function () { box.innerHTML = '<p class="muted">The county shelter layer did not load. Call 850-609-7000 or check <a href="https://myokaloosa.com/emergency-management">myokaloosa.com/emergency-management</a>.</p>'; });
  });

  /* ---------------- preparedness checklist ---------------- */
  var ck = q("[data-checklist-form]");
  if (ck) {
    var ckOut = q("[data-checklist-out]");
    ck.addEventListener("submit", function (e) {
      e.preventDefault();
      var people = Math.max(1, val(ck.people.value, 1)), pets = Math.max(0, val(ck.pets.value, 0)), days = Math.max(3, val(ck.days.value, 7));
      var home = ck.home.value, zone = ck.zone.value, groups = [];
      groups.push(["Water and food for " + days + " days", [
        (people * days + pets * Math.ceil(days / 2)) + " gallons of drinking water",
        "Bathtub and buckets filled for flushing once a warning is issued",
        (people * days * 3) + " no-cook meals: tuna and chicken pouches, peanut butter, crackers, fruit cups",
        "Manual can opener, paper plates, zip bags and contractor trash bags",
        "Two coolers; freeze jugs of water two days ahead"]]);
      var health = ["Two weeks of prescriptions and a printed medication list", "First-aid kit, sunscreen and insect repellent", "Spare glasses, contact supplies and hearing-aid batteries"];
      if (ck.meds.checked) health.push("Insulated bag and ice plan for refrigerated medicine; ask the pharmacy about an emergency early refill");
      if (ck.medical.checked) health.push("Backup power for medical equipment and a place on the Florida Special Needs Registry (snr.flhealthresponse.com) before the season");
      groups.push(["Health", health]);
      var power = ["A flashlight or headlamp per person plus spare batteries", "Battery or crank NOAA Weather Radio", "Charged power banks and car chargers", "Cash in small bills"];
      if (home !== "mobile") power.push("Generator fuel, outdoor-rated cords and a battery CO alarm. The generator stays outside, 20+ feet from openings");
      groups.push(["Power and contact", power]);
      groups.push(["Insurance and documents", ["Photos of every page of your homeowners, wind and flood policies, saved to the cloud", "A narrated video of every room, closet, the roof and the yard", "IDs, deeds or lease, titles and bank details in a sealed waterproof pouch", "Insurer claim phone numbers written on paper"]]);
      var house = [];
      if (home === "house") house.push("Shutters up or pre-cut plywood ready for every opening", "Garage door braced", "Patio furniture, grills, kayaks and paddleboards brought inside");
      if (home === "condo") house.push("Ask the association when elevators and water will be shut off", "Clear the balcony completely", "Photograph your unit and its contents; your HO-6 policy covers what the master policy does not");
      if (home === "mobile") house.push("Leave for every hurricane order, whatever your zone: manufactured homes are not safe in hurricane winds", "Check anchors and tie-downs now");
      if (home === "rental") house.push("Photograph the unit and your belongings", "Renters insurance covers your things; the owner's policy does not");
      if (ck.pool.checked) house.push("Keep the pool full, shock it and switch off pump power");
      if (ck.boat.checked) house.push("Haul the boat or move it to a protected hole early; Destin Harbor and bay marinas fill fast");
      house.push("Valuables and electronics off the floor", "Know where the main water valve and breaker are");
      groups.push(["Protecting the property", house]);
      var go = ["Fill the tank when a storm enters the 5-day cone", "Pick a destination north of I-10 and a second route"];
      if (zone === "A" || zone === "B") go.unshift("You are in Zone " + zone + ": leave as soon as an order is issued. Bridges such as the Marler and Brooks bridges may close when sustained winds reach about 40 mph");
      if (zone === "unknown") go.unshift("Look up your zone with the county zone search before the season");
      groups.push(["Evacuation", go]);
      if (pets) groups.push(["Pets (" + pets + ")", [days + " days of food and " + Math.ceil(pets * days / 2) + " gallons of extra water", "Crate or carrier, leash and ID tags", "Vaccination records for pet-friendly shelters", "A pet-friendly hotel or friend lined up in advance"]]);
      if (ck.infants.checked) groups.push(["Babies and children", ["Formula, bottles, diapers and wipes for " + days + " days", "Games and books that need no power", "Children's medicine and copies of records"]]);
      if (ck.seniors.checked) groups.push(["Older adults", ["Spare batteries for hearing aids and mobility devices", "A neighbor or relative who checks in before and after", "Special-needs registration if care is needed during a storm"]]);
      var total = groups.reduce(function (a, g) { return a + g[1].length; }, 0);
      ckOut.innerHTML = '<div class="result"><div class="big">' + total + " items</div><p style=\"margin:0\">Built for " + people + (people === 1 ? " person" : " people") + (pets ? " and " + pets + (pets === 1 ? " pet" : " pets") : "") + ", " + days + " days on your own.</p></div>" +
        '<div class="checklist-out">' + groups.map(function (g, i) {
          return "<h4>" + esc(g[0]) + "</h4><ul>" + g[1].map(function (item, j) { var id = "ck" + i + "-" + j; return '<li><input type="checkbox" id="' + id + '"><label for="' + id + '">' + esc(item) + "</label></li>"; }).join("") + "</ul>";
        }).join("") + '</div><div class="btnrow no-print"><button type="button" class="btn btn--line" data-print>Print this list</button></div>';
    });
  }
  document.addEventListener("click", function (e) { if (e.target.closest("[data-print]")) window.print(); });

  /* ---------------- preparedness budget ---------------- */
  var cost = q("[data-cost-form]");
  if (cost) {
    var costOut = q("[data-cost-out]");
    var runCost = function () {
      var p = Math.max(1, val(cost.people.value, 1)), d = Math.max(3, val(cost.days.value, 7)), pets = Math.max(0, val(cost.pets.value, 0)), win = val(cost.windows.value);
      var lines = [["Water, " + p * d + " gallons", p * d * 1.6], ["Shelf-stable food", p * d * 14], ["First aid and refills", 45 + p * 10], ["Lights, batteries, radio, power banks", 85 + p * 15], ["Tarps, rope, gloves, bags", 75]];
      if (pets) lines.push(["Pet food and water", pets * d * 3]);
      if (cost.shutters.value === "plywood") lines.push(["Plywood and fasteners, " + win + " openings", win * 55]);
      if (cost.shutters.value === "panels") lines.push(["Storm panels, " + win + " openings", win * 160]);
      if (cost.generator.value === "portable") lines.push(["Portable generator, cords, CO alarm", 1050]);
      if (cost.generator.value === "inverter") lines.push(["Inverter generator, cords, CO alarm", 1450]);
      if (cost.generator.value !== "none") lines.push(["Generator fuel, " + d + " days", d * 8 * 0.75 * 3.4]);
      if (cost.evac.value === "hotel") lines.push(["Inland hotel " + Math.min(d, 4) + " nights, meals, fuel", Math.min(d, 4) * (160 + p * 45) + 90]);
      if (cost.evac.value === "family") lines.push(["Fuel and road meals", 90 + p * 40]);
      var sum = lines.reduce(function (a, l) { return a + l[1]; }, 0);
      costOut.innerHTML = '<div class="result"><span class="small muted">Estimated storm-prep budget</span><div class="big">' + usd(sum) + '</div><div class="table-scroll"><table><tbody>' +
        lines.map(function (l) { return "<tr><td>" + esc(l[0]) + '</td><td style="text-align:right">' + usd(l[1]) + "</td></tr>"; }).join("") +
        '</tbody></table></div><p class="note">Rough 2026 retail prices. Florida sales-tax holidays on disaster supplies, when the Legislature enacts them, lower the bill.</p></div>';
    };
    cost.addEventListener("input", runCost); runCost();
  }

  /* ---------------- hurricane deductible ---------------- */
  var ded = q("[data-deductible-form]");
  if (ded) {
    var dedOut = q("[data-deductible-out]");
    var runDed = function () {
      var amount = ded.type.value === "flat" ? val(ded.flat.value) : val(ded.coverage.value) * val(ded.percent.value) / 100;
      var used = Math.max(0, val(ded.used.value));
      var left = Math.max(0, amount - used);
      var damage = val(ded.damage.value), owed = Math.max(0, damage - left);
      dedOut.innerHTML = '<div class="result"><div class="resgrid"><div><span>Hurricane deductible</span><div class="big">' + usd(amount) + "</div></div><div><span>Still to absorb this year</span><div class=\"big\">" + usd(left) + "</div></div><div><span>Insurer's share (estimate)</span><div class=\"big\">" + usd(owed) + "</div></div></div>" +
        '<p style="margin:12px 0 0">' + (damage <= left ? "<strong>The damage is inside your remaining hurricane deductible,</strong> so this storm alone may produce no payment. Report it anyway: under s. 627.701(5), Florida, for most personal residential policies, applies one hurricane deductible per calendar year, and the insurer may ask you to report below-deductible losses so they count toward it." : "You absorb " + usd(left) + " and the insurer would owe roughly " + usd(owed) + " before depreciation, limits and exclusions.") + "</p>" +
        '<p class="note">If a later hurricane hits in the same calendar year, the deductible is the greater of what remains or your all-other-perils deductible. Flood is separate: an NFIP or private flood policy has its own deductibles.</p></div>';
    };
    ded.addEventListener("input", runDed); runDed();
  }

  /* ---------------- supply quantities ---------------- */
  var sup = q("[data-supply-form]");
  if (sup) {
    var supOut = q("[data-supply-out]");
    var runSup = function () {
      var a = val(sup.adults.value), k = val(sup.kids.value), dogs = val(sup.dogs.value), cats = val(sup.cats.value), d = Math.max(1, val(sup.days.value, 7)), ppl = a + k;
      var water = ppl * d + dogs * d * 0.5 + cats * d * 0.15, meals = ppl * d * 3;
      var rows = [["Drinking water", Math.ceil(water) + " gal", Math.ceil(water / 2.5) + " jugs of 2.5 gal, or " + Math.ceil(water * 128 / 16.9 / 24) + " cases of 24 bottles"],
        ["Meals", meals + "", Math.ceil(meals * 0.6) + " cans and " + Math.ceil(meals * 0.4) + " pouches or boxes"],
        ["AA/AAA batteries", (ppl * 8 + 8) + "", "Lights, radio, fans"],
        ["Power banks", Math.max(1, ppl) + " x 10,000 mAh", "About 2-3 phone charges each"],
        ["Contractor bags", Math.ceil(d * 1.5) + "", "Trash, debris, rain covers"],
        ["Wipes and towels", Math.ceil(ppl * d / 3) + " packs", "Water may be off or under a boil notice"],
        ["Cash", "$" + (ppl * 100 + 100), "Small bills"]];
      if (dogs) rows.push(["Dog food", Math.ceil(dogs * d * 0.6) + " lb", "Plus " + Math.ceil(dogs * d * 0.5) + " gal water"]);
      if (cats) rows.push(["Cat food and litter", Math.ceil(cats * d * 0.15) + " lb food, " + Math.ceil(cats * d * 0.7) + " lb litter", "Plus " + Math.ceil(cats * d * 0.15) + " gal water"]);
      supOut.innerHTML = '<div class="table-scroll"><table><thead><tr><th>Item</th><th>How much</th><th>Shopping note</th></tr></thead><tbody>' + rows.map(function (r) { return "<tr><td><strong>" + r[0] + "</strong></td><td>" + r[1] + "</td><td>" + r[2] + "</td></tr>"; }).join("") + "</tbody></table></div>";
    };
    sup.addEventListener("input", runSup); runSup();
  }

  /* ---------------- generator runtime ---------------- */
  var gen = q("[data-generator-form]");
  if (gen) {
    var genOut = q("[data-generator-out]");
    var LOADS = { fridge: 200, freezer: 150, fan: 75, lights: 60, tv: 120, router: 20, phone: 30, window_ac: 900, microwave: 1000, cpap: 60, well: 1000, sump: 800 };
    var runGen = function () {
      var rated = val(gen.rated.value), tank = val(gen.tank.value), watts = 0, surge = 0;
      Object.keys(LOADS).forEach(function (k) { var el = gen.elements[k]; if (el && el.checked) { watts += LOADS[k]; if (/fridge|freezer|window_ac|well|sump/.test(k)) surge = Math.max(surge, LOADS[k] * 2); } });
      watts += val(gen.other.value);
      var gph = rated ? 0.15 * rated / 1000 + 0.55 * watts / 1000 : 0;
      if (gen.fuel.value === "propane") gph *= 1.35;
      if (gen.fuel.value === "diesel") gph *= 0.75;
      var hrs = gph ? tank / gph : 0, week = gph * 12 * 7, share = rated ? Math.min(1, watts / rated) : 0;
      genOut.innerHTML = '<div class="result"><div class="resgrid"><div><span>Running load</span><div class="big">' + watts.toLocaleString() + ' W</div></div><div><span>Hours per tank</span><div class="big">' + (hrs ? hrs.toFixed(1) : "–") + '</div></div><div><span>Fuel for a week at 12 h/day</span><div class="big">' + Math.ceil(week) + " gal</div></div></div>" +
        (watts + surge > rated ? '<p style="margin:12px 0 0"><strong>Too much at once:</strong> start-up surge pushes the load to about ' + (watts + surge).toLocaleString() + " W, above the " + rated.toLocaleString() + " W rating. Start motors one at a time or drop a load.</p>" : '<p style="margin:12px 0 0">Load is about ' + Math.round(share * 100) + "% of rated output" + (share > 0.8 ? ", which shortens runtime and adds wear." : ", a comfortable range.") + "</p>") +
        '<p class="note">Estimates only. Fuel lines form fast in Okaloosa and Walton once a warning is issued; store fuel in approved cans, away from the house.</p></div>';
    };
    gen.addEventListener("input", runGen); runGen();
  }

  /* ---------------- damage log (localStorage only) ---------------- */
  var log = q("[data-damage-log]");
  if (log) {
    var KEY = "dh-damage-log", rows = [];
    try { rows = JSON.parse(localStorage.getItem(KEY) || "[]"); } catch (e) { rows = []; }
    var logForm = q("[data-damage-form]"), logList = q("[data-damage-list]");
    var keep = function () { try { localStorage.setItem(KEY, JSON.stringify(rows)); } catch (e) { /* storage blocked */ } };
    var draw = function () {
      if (!rows.length) { logList.innerHTML = '<p class="muted">Nothing logged yet. Add one line per damaged room, item or structure.</p>'; return; }
      var total = rows.reduce(function (a, r) { return a + val(r.cost); }, 0);
      logList.innerHTML = '<div class="table-scroll"><table><thead><tr><th>Date</th><th>Where / what</th><th>Damage and cause</th><th>Photo refs</th><th>Est. cost</th><th class="no-print"><span class="sr">Remove</span></th></tr></thead><tbody>' +
        rows.map(function (r, i) { return "<tr><td>" + esc(r.date) + "</td><td>" + esc(r.area) + "</td><td>" + esc(r.desc) + '<br><span class="small muted">' + esc(r.cause) + "</span></td><td>" + esc(r.photos) + "</td><td>" + usd(val(r.cost)) + '</td><td class="no-print"><button type="button" class="btn btn--line btn--sm" data-drop="' + i + '">Remove</button></td></tr>'; }).join("") +
        '<tr><td colspan="4"><strong>Total estimated loss</strong></td><td><strong>' + usd(total) + '</strong></td><td class="no-print"></td></tr></tbody></table></div>';
    };
    logList.addEventListener("click", function (e) { var b = e.target.closest("[data-drop]"); if (b) { rows.splice(+b.getAttribute("data-drop"), 1); keep(); draw(); } });
    logForm.addEventListener("submit", function (e) {
      e.preventDefault();
      rows.push({ date: logForm.date.value, area: logForm.area.value, desc: logForm.desc.value, cause: logForm.cause.value, photos: logForm.photos.value, cost: logForm.cost.value });
      keep(); draw(); logForm.reset();
    });
    q("[data-damage-csv]").addEventListener("click", function () {
      var csv = "Date,Area,Description,Cause,Photos,Estimated cost\n" + rows.map(function (r) {
        return [r.date, r.area, r.desc, r.cause, r.photos, r.cost].map(function (v) { return '"' + String(v || "").replace(/"/g, '""') + '"'; }).join(",");
      }).join("\n");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([csv], { type: "text/csv" }));
      a.download = "storm-damage-log.csv"; document.body.appendChild(a); a.click(); a.remove();
    });
    draw();
  }

  /* ---------------- alert sign-up ---------------- */
  qa("[data-subscribe-form]").forEach(function (f) {
    var out = q("[data-subscribe-out]", f);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      out.textContent = "Saving…";
      fetch("/api/subscribe.php", { method: "POST", body: new URLSearchParams(new FormData(f)) }).then(function (r) { return r.json(); }).then(function (d) {
        out.innerHTML = d.ok ? "<strong>Signed up.</strong> Destin storm updates will go to " + esc(d.email) + ". Every message has an unsubscribe link." : "<strong>" + esc(d.error || "That did not work.") + "</strong>";
        if (d.ok) f.reset();
      }).catch(function () { out.textContent = "We could not save that just now. Please try again shortly."; });
    });
  });

  /* ---------------- free claim review forms ---------------- */
  qa("[data-lead-form]").forEach(function (f) {
    var out = q("[data-lead-out]", f), btn = q("button[type=submit]", f);
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!f.checkValidity()) {
        out.className = "leadform-out is-error";
        out.textContent = "Please add your name, phone, property city or ZIP, and tick the acknowledgment box.";
        var bad = q(":invalid", f); if (bad) bad.focus();
        return;
      }
      out.className = "leadform-out"; out.textContent = "Sending…"; btn.disabled = true;
      var body = new URLSearchParams(new FormData(f));
      body.append("page", location.pathname);
      fetch("/api/lead.php", { method: "POST", body: body }).then(function (r) { return r.json(); }).then(function (d) {
        if (d.ok) {
          out.innerHTML = "<strong>Thanks, " + esc(d.name) + ".</strong> Your request reached The Lawgical Firm. Someone from the firm will reach out soon. Need to talk now? Call <a href=\"tel:" + TEL + "\">" + PHONE + "</a>.";
          qa("input:not([type=checkbox]), textarea", f).forEach(function (el) { el.value = ""; });
          if (window.gtag) window.gtag("event", "generate_lead");
        } else { out.className = "leadform-out is-error"; out.textContent = d.error || "Something went wrong. Please call " + PHONE + "."; }
      }).catch(function () { out.className = "leadform-out is-error"; out.textContent = "The request did not go through. Please call " + PHONE + "."; })
        .then(function () { btn.disabled = false; });
    });
  });

  /* ---------------- tabs ---------------- */
  qa("[data-tabs]").forEach(function (wrap) {
    var tabs = qa("[role=tab]", wrap);
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () {
        tabs.forEach(function (x) { var on = x === t; x.setAttribute("aria-selected", String(on)); x.tabIndex = on ? 0 : -1; var p = document.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = !on; });
      });
      t.addEventListener("keydown", function (e) {
        var n = e.key === "ArrowRight" ? i + 1 : e.key === "ArrowLeft" ? i - 1 : null;
        if (n === null) return;
        n = (n + tabs.length) % tabs.length; tabs[n].click(); tabs[n].focus();
      });
    });
  });
})();
