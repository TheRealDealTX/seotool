/* Jaz & Theo — interactive tools. Each tool mounts into
   <div class="tool" data-tool="NAME"> rendered by build.py. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var money = function (n) { return "$" + Math.round(n).toLocaleString("en-US"); };
  var pad = function (n) { return (n < 10 ? "0" : "") + n; };

  /* ================= Sun position (low-precision NOAA-style) ================= */
  var RAD = Math.PI / 180;
  function sunAltitude(ms, lat, lon) {
    var d = ms / 86400000 + 2440587.5 - 2451545.0;
    var g = (357.529 + 0.98560028 * d) * RAD;
    var q = 280.459 + 0.98564736 * d;
    var L = (q + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * RAD;
    var e = (23.439 - 0.00000036 * d) * RAD;
    var ra = Math.atan2(Math.cos(e) * Math.sin(L), Math.cos(L)) / RAD;
    var dec = Math.asin(Math.sin(e) * Math.sin(L));
    var gmst = (18.697374558 + 24.06570982441908 * d) % 24;
    var H = ((gmst * 15 + lon - ra) % 360) * RAD;
    var la = lat * RAD;
    return Math.asin(Math.sin(la) * Math.sin(dec) + Math.cos(la) * Math.cos(dec) * Math.cos(H)) / RAD;
  }
  function tzOffsetMin(ms, tz) {
    try {
      var parts = new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }).formatToParts(new Date(ms));
      var o = {};
      parts.forEach(function (p) { o[p.type] = p.value; });
      var asUTC = Date.UTC(+o.year, +o.month - 1, +o.day, +o.hour % 24, +o.minute);
      return Math.round((asUTC - Math.floor(ms / 60000) * 60000) / 60000);
    } catch (e) { return -new Date(ms).getTimezoneOffset(); }
  }
  function localMidnight(y, m, d, tz) {
    var guess = Date.UTC(y, m, d);
    var off = tzOffsetMin(guess, tz);
    var t = guess - off * 60000;
    off = tzOffsetMin(t, tz);
    return guess - off * 60000;
  }
  function fmtTime(ms, tz) {
    try { return new Intl.DateTimeFormat("en-US", { timeZone: tz, hour: "numeric", minute: "2-digit" }).format(new Date(ms)); }
    catch (e) { var dt = new Date(ms); return dt.getHours() % 12 + ":" + pad(dt.getMinutes()); }
  }
  /* Returns key light events for a local calendar day. */
  function sunDay(y, m, d, lat, lon, tz) {
    var start = localMidnight(y, m, d, tz), step = 60000, prev = sunAltitude(start, lat, lon);
    var ev = {}, alts = [prev];
    var marks = [[-6, "blueStart", "blueEnd"], [-4, "goldStart", "goldEnd"], [-0.833, "sunrise", "sunset"], [6, "goldAmEnd", "goldPmStart"]];
    var peak = { alt: prev, t: start };
    for (var i = 1; i <= 1440; i++) {
      var t = start + i * step, a = sunAltitude(t, lat, lon);
      if (a > peak.alt) peak = { alt: a, t: t };
      marks.forEach(function (mk) {
        var th = mk[0];
        if (prev < th && a >= th && !ev[mk[1]]) ev[mk[1]] = t - step * (a - th) / (a - prev);
        if (prev >= th && a < th) ev[mk[2]] = t - step * (prev - th) / (prev - a);
      });
      if (i % 10 === 0) alts.push(a);
      prev = a;
    }
    ev.start = start; ev.noon = peak.t; ev.peak = peak.alt; ev.alts = alts;
    return ev;
  }
  var CITIES = [
    ["El Paso, TX", 31.7619, -106.485, "America/Denver"],
    ["Las Cruces / White Sands, NM", 32.3199, -106.7637, "America/Denver"],
    ["Tucson, AZ", 32.2226, -110.9747, "America/Phoenix"],
    ["Phoenix / Mesa, AZ", 33.4484, -112.074, "America/Phoenix"],
    ["Safford / Gila Valley, AZ", 32.834, -109.7076, "America/Phoenix"],
    ["Sedona, AZ", 34.8697, -111.761, "America/Phoenix"],
    ["Page / Lake Powell, AZ", 36.9147, -111.4558, "America/Phoenix"],
    ["Austin, TX", 30.2672, -97.7431, "America/Chicago"],
    ["San Antonio, TX", 29.4241, -98.4936, "America/Chicago"],
    ["Los Angeles, CA", 34.0522, -118.2437, "America/Los_Angeles"],
    ["Rapid City / Badlands, SD", 44.0805, -103.231, "America/Denver"],
    ["Yellowstone, WY", 44.428, -110.5885, "America/Denver"]
  ];
  function cityOptions(sel) {
    return CITIES.map(function (c, i) { return '<option value="' + i + '"' + (i === sel ? " selected" : "") + ">" + esc(c[0]) + "</option>"; }).join("");
  }
  function todayISO() { var n = new Date(); return n.getFullYear() + "-" + pad(n.getMonth() + 1) + "-" + pad(n.getDate()); }
  function parseISO(s) { var p = (s || todayISO()).split("-"); return [+p[0], +p[1] - 1, +p[2]]; }
  function dur(a, b) { var m = Math.round((b - a) / 60000); return m >= 60 ? Math.floor(m / 60) + " h " + (m % 60) + " min" : m + " min"; }

  var ICON = {
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg>'
  };

  /* ================= Golden hour ================= */
  function goldenHour(el) {
    var compact = el.hasAttribute("data-compact");
    var ci = parseInt(el.getAttribute("data-city") || "0", 10);
    if (compact) {
      el.innerHTML = '<div class="gh-readout" aria-live="polite"></div><p class="tool-note" style="color:#f1d7b4"></p>';
      var c = CITIES[ci], d = parseISO(), ev = sunDay(d[0], d[1], d[2], c[1], c[2], c[3]);
      $(".gh-readout", el).innerHTML =
        "<div><small>Evening golden hour</small><b>" + fmtTime(ev.goldPmStart, c[3]) + "</b></div>" +
        "<div><small>Sunset</small><b>" + fmtTime(ev.sunset, c[3]) + "</b></div>" +
        "<div><small>Blue hour ends</small><b>" + fmtTime(ev.blueEnd, c[3]) + "</b></div>" +
        "<div><small>Morning golden hour</small><b>" + fmtTime(ev.goldStart, c[3]) + "</b></div>";
      var now = Date.now(), left = ev.goldPmStart - now;
      $(".tool-note", el).textContent = "Today in " + c[0] + (left > 0 ? " — golden hour starts in " + dur(now, ev.goldPmStart) + "." : now < ev.blueEnd ? " — the light is happening right now. Go outside." : " — that's a wrap for today. Tomorrow's light is a few minutes " + (d[1] < 5 || d[1] === 11 ? "later" : "different") + ".");
      return;
    }
    el.innerHTML += '<div class="tool-grid">' +
      '<div class="field"><label for="gh-city">Location</label><select id="gh-city">' + cityOptions(ci) + '<option value="geo">Use my location</option></select></div>' +
      '<div class="field"><label for="gh-date">Date</label><input type="date" id="gh-date" value="' + todayISO() + '"></div></div>' +
      '<div class="tool-out" aria-live="polite"><div class="sub gh-title"></div><div class="big gh-big"></div><div class="tool-kpis gh-kpis"></div>' +
      '<div class="day-bar" aria-hidden="true"></div><div class="day-scale" aria-hidden="true"><span>12 am</span><span>6 am</span><span>noon</span><span>6 pm</span><span>12 am</span></div>' +
      '<div class="legend"><span><i style="background:#1b1622"></i>Night</span><span><i style="background:#4a5f9c"></i>Blue hour</span><span><i style="background:#e0a95f"></i>Golden hour</span><span><i style="background:#f7e6c4"></i>Daylight</span></div></div>' +
      '<p class="tool-note">Times are calculated from the sun\'s position (sun 6° above to 4° below the horizon for golden hour, 4° to 6° below for blue hour) for open, flat horizons. Mountains, canyons and buildings bring the effective sunset earlier — plan on 15–30 minutes of buffer.</p>';
    var sel = $("#gh-city", el), date = $("#gh-date", el), geo = null;
    function run() {
      var c;
      if (sel.value === "geo") {
        if (!geo) return;
        c = ["your location", geo[0], geo[1], Intl.DateTimeFormat().resolvedOptions().timeZone];
      } else c = CITIES[+sel.value];
      var d = parseISO(date.value), ev = sunDay(d[0], d[1], d[2], c[1], c[2], c[3]), tz = c[3];
      var dateLabel = new Date(Date.UTC(d[0], d[1], d[2], 12)).toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", timeZone: "UTC" });
      $(".gh-title", el).textContent = "Evening golden hour in " + c[0] + " · " + dateLabel;
      if (!ev.sunset || !ev.goldPmStart) {
        $(".gh-big", el).textContent = "The sun stays " + (ev.peak > 0 ? "up" : "down") + " all day here.";
        $(".gh-kpis", el).innerHTML = ""; return;
      }
      $(".gh-big", el).textContent = fmtTime(ev.goldPmStart, tz) + " – " + fmtTime(ev.goldEnd, tz);
      $(".gh-kpis", el).innerHTML =
        "<div><small>Sunset</small><b>" + fmtTime(ev.sunset, tz) + "</b></div>" +
        "<div><small>Blue hour</small><b>" + fmtTime(ev.goldEnd, tz) + "–" + fmtTime(ev.blueEnd, tz) + "</b></div>" +
        "<div><small>Morning gold</small><b>" + fmtTime(ev.goldStart, tz) + "–" + fmtTime(ev.goldAmEnd, tz) + "</b></div>" +
        "<div><small>Sunrise</small><b>" + fmtTime(ev.sunrise, tz) + "</b></div>" +
        "<div><small>Evening light lasts</small><b>" + dur(ev.goldPmStart, ev.goldEnd) + "</b></div>" +
        "<div><small>Start portraits by</small><b>" + fmtTime(ev.goldPmStart - 15 * 60000, tz) + "</b></div>";
      var bar = $(".day-bar", el), day = 86400000, segs = [
        [ev.start, ev.blueStart, "#1b1622"], [ev.blueStart, ev.goldStart, "#4a5f9c"], [ev.goldStart, ev.goldAmEnd, "#e0a95f"],
        [ev.goldAmEnd, ev.goldPmStart, "#f7e6c4"], [ev.goldPmStart, ev.goldEnd, "#e0a95f"], [ev.goldEnd, ev.blueEnd, "#4a5f9c"], [ev.blueEnd, ev.start + day, "#1b1622"]
      ];
      bar.innerHTML = segs.filter(function (s) { return s[0] && s[1]; }).map(function (s) {
        return '<span style="left:' + ((s[0] - ev.start) / day * 100).toFixed(2) + "%;width:" + ((s[1] - s[0]) / day * 100).toFixed(2) + "%;background:" + s[2] + '"></span>';
      }).join("");
    }
    sel.addEventListener("change", function () {
      if (sel.value === "geo") {
        if (!navigator.geolocation) { sel.value = "0"; run(); return; }
        $(".gh-title", el).textContent = "Finding your location…";
        navigator.geolocation.getCurrentPosition(function (p) { geo = [p.coords.latitude, p.coords.longitude]; run(); },
          function () { $(".gh-title", el).textContent = "Location unavailable — pick a city instead."; sel.value = "0"; run(); }, { timeout: 8000 });
      } else run();
    });
    date.addEventListener("input", run);
    run();
  }

  /* ================= Wedding day timeline ================= */
  function timeline(el) {
    el.innerHTML += '<div class="tool-grid">' +
      '<div class="field"><label for="tl-time">Ceremony start</label><input type="time" id="tl-time" value="17:00"></div>' +
      '<div class="field"><label for="tl-len">Ceremony length <output class="range-out" for="tl-len">30 min</output></label><input type="range" id="tl-len" min="15" max="75" step="5" value="30"></div>' +
      '<div class="field"><label for="tl-fam">Family photo groups <output class="range-out" for="tl-fam">8</output></label><input type="range" id="tl-fam" min="2" max="20" value="8"></div>' +
      '<div class="field"><label for="tl-party">Wedding party size</label><select id="tl-party"><option value="15">Small (0–4)</option><option value="25" selected>Medium (5–10)</option><option value="35">Large (11+)</option></select></div>' +
      '<div class="field"><label for="tl-travel">Travel to reception</label><select id="tl-travel"><option value="0">Same venue</option><option value="15">About 15 min</option><option value="30">About 30 min</option><option value="45">45 min +</option></select></div>' +
      '<div class="field"><label for="tl-rec">Reception length <output class="range-out" for="tl-rec">4 h</output></label><input type="range" id="tl-rec" min="3" max="6" step="0.5" value="4"></div>' +
      '<div class="field"><label for="tl-city">Location (for sunset)</label><select id="tl-city">' + cityOptions(0) + '</select></div>' +
      '<div class="field"><label for="tl-date">Wedding date</label><input type="date" id="tl-date" value="' + todayISO() + '"></div>' +
      '</div><label class="toggle"><input type="checkbox" id="tl-first" checked> We\'re doing a first look</label>' +
      '<div class="tool-out" aria-live="polite"><ol class="timeline-out"></ol></div>' +
      '<div class="tool-actions"><button type="button" class="btn btn-sm" data-act="print">Print timeline</button><button type="button" class="btn btn-sm btn-ghost" data-act="copy">Copy as text</button></div>' +
      '<p class="tool-note">A starting framework, not a contract. Share it with your photographer and coordinator and adjust for hair and makeup headcount, venue access times and cultural or religious traditions.</p>';
    var ids = ["time", "len", "fam", "party", "travel", "rec", "city", "date", "first"];
    var f = {};
    ids.forEach(function (k) { f[k] = $("#tl-" + k, el); });
    var items = [];
    function hm(min) { min = ((min % 1440) + 1440) % 1440; var h = Math.floor(min / 60), m = Math.round(min % 60); if (m === 60) { h++; m = 0; } return (h % 12 || 12) + ":" + pad(m) + (h < 12 || h === 24 ? " am" : " pm"); }
    function run() {
      $$("output", el).forEach(function (o) {
        var inp = $("#" + o.getAttribute("for"), el);
        o.textContent = inp.id === "tl-len" ? inp.value + " min" : inp.id === "tl-rec" ? inp.value + " h" : inp.value;
      });
      var tp = (f.time.value || "17:00").split(":"), C = +tp[0] * 60 + +tp[1];
      var len = +f.len.value, fam = +f.fam.value * 3 + 5, party = +f.party.value, travel = +f.travel.value, rec = +f.rec.value * 60;
      var first = f.first.checked;
      var c = CITIES[+f.city.value], d = parseISO(f.date.value), ev = sunDay(d[0], d[1], d[2], c[1], c[2], c[3]);
      var midnight = ev.start, sunset = ev.sunset ? Math.round((ev.sunset - midnight) / 60000) : null;
      items = [];
      var add = function (t, title, note, key) { items.push({ t: t, title: title, note: note, key: !!key }); };
      if (first) {
        var t0 = C - 60 - party - 30 - 20;
        add(t0 - 150, "Photographer arrives — details", "Rings, invitations, shoes, florals and the dress or suit, all gathered in one spot.");
        add(t0 - 110, "Getting-ready candids", "Last touches of hair and makeup, letters and gifts exchanged.");
        add(t0 - 45, "Getting dressed", "Allow a full 20 minutes; buttons and bustles always take longer.");
        add(t0 - 20, "Travel to first-look spot", "Shade or open shade if it's midday.");
        add(t0, "First look", "Ten private minutes before the camera moves in.", true);
        add(t0 + 20, "Couple portraits", "The relaxed, unhurried set — 30 minutes.");
        add(t0 + 50, "Wedding party photos", party + " minutes, full group first, then smaller combinations.");
        add(t0 + 50 + party, "Immediate family photos", "Anyone who's ready early. The rest happen after the ceremony.");
        add(C - 30, "Couple tucked away · guests arrive", "Water, a snack and a breath.");
      } else {
        add(C - 240, "Photographer arrives — details", "Rings, invitations, shoes, florals and attire.");
        add(C - 200, "Getting-ready candids", "Hair and makeup wraps, gifts and letters.");
        add(C - 120, "Getting dressed", "Plan 20 minutes.");
        add(C - 95, "Individual portraits & wedding party (separately)", "Each side photographed with their own people.");
        add(C - 45, "Hide away · guests arrive", "Final touch-ups.");
      }
      add(C, "Ceremony", len + " minutes.", true);
      var after = C + len;
      add(after, "Recessional & receiving moment", "Hugs, confetti, the first exhale.");
      add(after + 10, "Family formals", fam + " minutes for " + f.fam.value + " groups — have a list and a helper calling names.");
      var t = after + 10 + fam;
      if (!first) {
        add(t, "Wedding party photos", party + " minutes.");
        t += party;
        add(t, "Couple portraits", "Usually 20–30 minutes during cocktail hour.");
        t += 25;
      } else {
        add(t, "Cocktail hour", "Couple joins guests — or grabs a few extra portraits.");
      }
      var R = Math.max(after + 60, t) + travel;
      if (travel) add(R - travel, "Travel to reception", travel + " minutes.");
      add(R, "Grand entrance & first dance", "", true);
      add(R + 15, "Dinner service", "Your photographer eats when you eat, so they're ready for toasts.");
      add(R + 60, "Toasts", "Lighting check: speakers face the room.");
      add(R + 90, "Parent dances · open dance floor", "");
      add(R + 120, "Cake cutting", "");
      if (sunset !== null && sunset > C - 120 && sunset < R + rec) {
        add(sunset - 25, "Golden hour portraits", "Slip out for 15 minutes — sunset in " + c[0] + " is " + hm(sunset) + ".", true);
      }
      add(R + rec - 20, "Last dance / private last dance", "");
      add(R + rec, "Grand exit", "Sparklers, bubbles or a quiet getaway — check venue rules.", true);
      items.sort(function (a, b) { return a.t - b.t; });
      $(".timeline-out", el).innerHTML = items.map(function (it, i) {
        return '<li class="' + (it.key ? "key" : "") + '" style="animation-delay:' + (i * 0.03) + 's"><time>' + hm(it.t) + "</time><div><b>" + esc(it.title) + "</b>" + (it.note ? "<span>" + esc(it.note) + "</span>" : "") + "</div></li>";
      }).join("");
    }
    ids.forEach(function (k) { f[k].addEventListener("input", run); f[k].addEventListener("change", run); });
    el.addEventListener("click", function (e) {
      var b = e.target.closest("[data-act]");
      if (!b) return;
      if (b.getAttribute("data-act") === "print") window.print();
      else {
        var txt = items.map(function (it) { return hm(it.t) + "  " + it.title; }).join("\n");
        if (navigator.clipboard) navigator.clipboard.writeText(txt);
        b.textContent = "Copied";
        setTimeout(function () { b.textContent = "Copy as text"; }, 1800);
      }
    });
    run();
  }

  /* ================= Photography budget ================= */
  function budget(el) {
    var REG = [["El Paso / Las Cruces", 2200, 4200], ["Tucson & southern Arizona", 2400, 4600], ["Phoenix metro", 2800, 5400], ["Austin", 3200, 6800], ["San Antonio", 2800, 5400], ["Los Angeles", 3800, 8500], ["Elsewhere in the US", 2600, 5600]];
    el.innerHTML += '<div class="tool-grid">' +
      '<div class="field"><label for="bg-reg">Region</label><select id="bg-reg">' + REG.map(function (r, i) { return '<option value="' + i + '">' + r[0] + "</option>"; }).join("") + "</select></div>" +
      '<div class="field"><label for="bg-hrs">Hours of coverage <output class="range-out" for="bg-hrs">8 h</output></label><input type="range" id="bg-hrs" min="2" max="12" value="8"></div>' +
      '<div class="field"><label for="bg-tier">Photographer experience</label><select id="bg-tier"><option value="0.75">Newer (1–3 years)</option><option value="1" selected>Established</option><option value="1.45">In-demand / editorial</option></select></div>' +
      '<div class="field"><label for="bg-travel">Travel</label><select id="bg-travel"><option value="0">Local</option><option value="1">Regional drive</option><option value="2">Destination (flights)</option></select></div>' +
      "</div>" +
      '<div class="tool-grid"><label class="toggle"><input type="checkbox" id="bg-second" checked> Second photographer</label>' +
      '<label class="toggle"><input type="checkbox" id="bg-eng"> Engagement session</label>' +
      '<label class="toggle"><input type="checkbox" id="bg-album"> Heirloom album</label>' +
      '<label class="toggle"><input type="checkbox" id="bg-video"> Add a videographer</label></div>' +
      '<div class="tool-out" aria-live="polite"><div class="sub">Typical total range for this setup</div><div class="big bg-big"></div><div class="sub bg-mid"></div><div class="bars bg-bars"></div></div>' +
      '<p class="tool-note">These are broad market ranges compiled for planning, not quotes — individual photographers price very differently. Use the result to set a budget line, then compare real collections and what is included.</p>';
    var ids = ["reg", "hrs", "tier", "travel", "second", "eng", "album", "video"];
    var f = {};
    ids.forEach(function (k) { f[k] = $("#bg-" + k, el); });
    function run() {
      $("output", el).textContent = f.hrs.value + " h";
      var r = REG[+f.reg.value], h = +f.hrs.value, tier = +f.tier.value;
      var scale = 0.35 + 0.65 * h / 8;
      var parts = [["Coverage (" + h + " h)", r[1] * scale * tier, r[2] * scale * tier]];
      if (f.second.checked) parts.push(["Second shooter", 60 * h * tier, 110 * h * tier]);
      if (f.eng.checked) parts.push(["Engagement session", 350 * tier, 750 * tier]);
      if (f.album.checked) parts.push(["Album", 650, 1600]);
      if (+f.travel.value === 1) parts.push(["Travel", 150, 600]);
      if (+f.travel.value === 2) parts.push(["Travel", 900, 2200]);
      if (f.video.checked) parts.push(["Videographer", r[1] * scale * 0.9, r[2] * scale * 1.05]);
      var lo = 0, hi = 0;
      parts.forEach(function (p) { lo += p[1]; hi += p[2]; });
      var round = function (n) { return Math.round(n / 50) * 50; };
      $(".bg-big", el).textContent = money(round(lo)) + " – " + money(round(hi));
      $(".bg-mid", el).textContent = "Midpoint about " + money(round((lo + hi) / 2)) + " · roughly " + money(round((lo + hi) / 2 / h)) + " per covered hour";
      var max = Math.max.apply(null, parts.map(function (p) { return (p[1] + p[2]) / 2; }));
      $(".bg-bars", el).innerHTML = parts.map(function (p) {
        var mid = (p[1] + p[2]) / 2;
        return '<div class="bar"><span>' + esc(p[0]) + '</span><div class="track"><div class="fill" data-w="' + (mid / max * 100).toFixed(1) + '"></div></div><b>' + money(round(mid)) + "</b></div>";
      }).join("");
      requestAnimationFrame(function () { $$(".fill", el).forEach(function (x) { x.style.width = x.getAttribute("data-w") + "%"; }); });
    }
    ids.forEach(function (k) { f[k].addEventListener("input", run); f[k].addEventListener("change", run); });
    run();
  }

  /* ================= Chandelier / pendant calculator ================= */
  function chandelier(el) {
    el.innerHTML += '<div class="tool-grid">' +
      '<div class="field"><label for="ch-l">Room length (ft)</label><input type="number" id="ch-l" min="4" max="60" value="14"></div>' +
      '<div class="field"><label for="ch-w">Room width (ft)</label><input type="number" id="ch-w" min="4" max="60" value="12"></div>' +
      '<div class="field"><label for="ch-c">Ceiling height (ft)</label><input type="number" id="ch-c" min="7" max="24" step="0.5" value="9"></div>' +
      '<div class="field"><label for="ch-t">Table width (in) — 0 if none</label><input type="number" id="ch-t" min="0" max="80" value="40"></div>' +
      "</div>" +
      '<div class="tool-out" aria-live="polite"><div class="sub">Suggested fixture diameter</div><div class="big ch-big"></div><div class="tool-kpis ch-kpis"></div>' +
      '<svg class="diagram" viewBox="0 0 400 230" role="img" aria-label="Side view of the fixture over the table"></svg></div>' +
      '<p class="tool-note">Rules of thumb used by lighting designers: room length + width in feet ≈ fixture diameter in inches; keep a fixture over a table about 12 in narrower than the table; hang the bottom 30–34 in above the tabletop with an 8 ft ceiling, adding about 3 in per extra foot of ceiling. With no table, keep at least 7 ft of clearance below the fixture.</p>';
    var f = {};
    ["l", "w", "c", "t"].forEach(function (k) { f[k] = $("#ch-" + k, el); f[k].addEventListener("input", run); });
    function run() {
      var L = +f.l.value || 0, W = +f.w.value || 0, Ch = +f.c.value || 8, T = +f.t.value || 0;
      var dia = L + W, maxT = T ? T - 12 : null, rec = maxT ? Math.min(dia, maxT) : dia;
      rec = Math.max(8, Math.round(rec));
      var extra = Math.max(0, Ch - 8), above = T ? [30 + extra * 3, 34 + extra * 3] : null;
      var fixH = [Math.round(Ch * 2.5), Math.round(Ch * 3)];
      $(".ch-big", el).textContent = rec + " in" + (maxT && dia > maxT ? " (capped by table)" : "");
      $(".ch-kpis", el).innerHTML =
        "<div><small>Room rule</small><b>" + dia + " in</b></div>" +
        (maxT ? "<div><small>Max for table</small><b>" + maxT + " in</b></div>" : "") +
        (above ? "<div><small>Bottom above table</small><b>" + above[0] + "–" + above[1] + " in</b></div>" : "<div><small>Clearance below</small><b>≥ 84 in</b></div>") +
        "<div><small>Fixture height</small><b>" + fixH[0] + "–" + fixH[1] + " in</b></div>" +
        "<div><small>Linear pendant over table</small><b>" + (T ? Math.round(T * 0.66 * 1.6) + "–" + Math.round(T * 0.75 * 1.7) + " in long" : "—") + "</b></div>";
      // Side elevation diagram, 1 in = scale px
      var H = Ch * 12, scale = 190 / H, floorY = 210, ceilY = floorY - H * scale;
      var tableTop = floorY - 30 * scale, tw = T ? Math.min(T, 100) * scale * 2.2 : 0;
      var fBottom = T ? tableTop - ((above[0] + above[1]) / 2) * scale : floorY - 84 * scale;
      var fw = rec * scale * 2.2, fh = ((fixH[0] + fixH[1]) / 2) * scale, cx = 200;
      if (fBottom - fh < ceilY + 6) fh = Math.max(8, fBottom - ceilY - 6);
      var s = '<line x1="20" y1="' + ceilY + '" x2="380" y2="' + ceilY + '" stroke="#4a423b" stroke-width="2"/>' +
        '<line x1="20" y1="' + floorY + '" x2="380" y2="' + floorY + '" stroke="#4a423b" stroke-width="2"/>' +
        '<line x1="' + cx + '" y1="' + ceilY + '" x2="' + cx + '" y2="' + (fBottom - fh) + '" stroke="#7a6f65" stroke-width="1.5"/>' +
        '<path d="M' + (cx - fw / 2) + "," + fBottom + " Q" + cx + "," + (fBottom - fh * 1.6) + " " + (cx + fw / 2) + "," + fBottom + 'Z" fill="#e0a95f" stroke="#98462a" stroke-width="1.5"/>' +
        '<circle cx="' + cx + '" cy="' + (fBottom + 4) + '" r="26" fill="url(#glow)"/>' +
        '<defs><radialGradient id="glow"><stop offset="0" stop-color="#ffd696" stop-opacity=".8"/><stop offset="1" stop-color="#ffd696" stop-opacity="0"/></radialGradient></defs>';
      if (T) {
        s += '<rect x="' + (cx - tw / 2) + '" y="' + tableTop + '" width="' + tw + '" height="5" fill="#7e8c6c"/>' +
          '<line x1="' + (cx - tw / 2 + 8) + '" y1="' + tableTop + '" x2="' + (cx - tw / 2 + 8) + '" y2="' + floorY + '" stroke="#7e8c6c" stroke-width="4"/>' +
          '<line x1="' + (cx + tw / 2 - 8) + '" y1="' + tableTop + '" x2="' + (cx + tw / 2 - 8) + '" y2="' + floorY + '" stroke="#7e8c6c" stroke-width="4"/>' +
          '<line x1="' + (cx + fw / 2 + 24) + '" y1="' + fBottom + '" x2="' + (cx + fw / 2 + 24) + '" y2="' + tableTop + '" stroke="#c0603a" stroke-dasharray="3 3"/>' +
          '<text x="' + (cx + fw / 2 + 30) + '" y="' + ((fBottom + tableTop) / 2 + 4) + '" font-size="11" fill="#98462a" font-family="sans-serif">' + above[0] + "–" + above[1] + ' in</text>';
      }
      s += '<text x="24" y="' + (ceilY - 6) + '" font-size="10" fill="#7a6f65" font-family="sans-serif">' + Ch + ' ft ceiling</text>' +
        '<text x="' + cx + '" y="' + (fBottom - fh - 8 > ceilY + 12 ? fBottom - fh - 8 : ceilY + 14) + '" text-anchor="middle" font-size="11" fill="#1f1b18" font-family="sans-serif">' + rec + ' in wide</text>';
      $(".diagram", el).innerHTML = s;
    }
    run();
  }

  /* ================= Peg rail planner ================= */
  function pegrail(el) {
    el.innerHTML += '<div class="tool-grid">' +
      '<div class="field"><label for="pr-w">Rail length (in)</label><input type="number" id="pr-w" min="12" max="240" value="48"></div>' +
      '<div class="field"><label for="pr-s">Target spacing <output class="range-out" for="pr-s">10 in</output></label><input type="range" id="pr-s" min="4" max="16" value="10"></div>' +
      '<div class="field"><label for="pr-m">End margin (in)</label><input type="number" id="pr-m" min="1" max="12" step="0.5" value="4"></div>' +
      '<div class="field"><label for="pr-use">Who uses it</label><select id="pr-use"><option value="adult">Adults (coats, bags)</option><option value="kids">Kids (backpacks)</option><option value="mixed">Both — two rails</option><option value="kitchen">Kitchen / mugs</option></select></div>' +
      "</div>" +
      '<div class="tool-out" aria-live="polite"><div class="sub">Pegs you need</div><div class="big pr-big"></div><div class="tool-kpis pr-kpis"></div>' +
      '<svg class="diagram" viewBox="0 0 400 120" role="img" aria-label="Peg layout diagram"></svg><div class="sub pr-list" style="margin-top:10px"></div></div>' +
      '<p class="tool-note">Mark the centers from the left end of the board. Check your pegs\' tenon size before buying a drill bit, and screw the rail into studs (usually 16 in on center) or use rated anchors.</p>';
    var f = {};
    ["w", "s", "m", "use"].forEach(function (k) { f[k] = $("#pr-" + k, el); f[k].addEventListener("input", run); f[k].addEventListener("change", run); });
    function run() {
      $("output", el).textContent = f.s.value + " in";
      var W = +f.w.value || 48, S = +f.s.value, M = +f.m.value || 4, span = Math.max(0, W - 2 * M);
      var n = Math.max(2, Math.floor(span / S) + 1), act = span / (n - 1);
      var hts = { adult: "60–66 in", kids: "40–48 in", mixed: "64 in + 44 in", kitchen: "18–20 in above counter" };
      var pos = [];
      for (var i = 0; i < n; i++) pos.push(+(M + act * i).toFixed(2));
      $(".pr-big", el).textContent = n + (f.use.value === "mixed" ? " per rail" : "") + " pegs";
      $(".pr-kpis", el).innerHTML = "<div><small>Actual spacing</small><b>" + act.toFixed(2) + " in</b></div><div><small>Rail height (top)</small><b>" + hts[f.use.value] + "</b></div><div><small>Studs crossed (16 in OC)</small><b>about " + Math.max(1, Math.floor(W / 16)) + "</b></div>";
      var sc = 360 / W, s = '<rect x="20" y="40" width="' + (W * sc) + '" height="26" rx="3" fill="#e9dccb" stroke="#98462a"/>';
      pos.forEach(function (p) {
        var x = 20 + p * sc;
        s += '<circle cx="' + x + '" cy="53" r="6" fill="#c0603a"/><line x1="' + x + '" y1="66" x2="' + x + '" y2="86" stroke="#c0603a" stroke-width="3" stroke-linecap="round"/>';
      });
      s += '<text x="20" y="110" font-size="11" fill="#7a6f65" font-family="sans-serif">0</text><text x="' + (20 + W * sc) + '" y="110" text-anchor="end" font-size="11" fill="#7a6f65" font-family="sans-serif">' + W + ' in</text>';
      $(".diagram", el).innerHTML = s;
      $(".pr-list", el).textContent = "Peg centers from the left end: " + pos.map(function (p) { return p + '"'; }).join(" · ");
    }
    run();
  }

  /* ================= Cloth napkin savings ================= */
  function napkins(el) {
    el.innerHTML += '<div class="tool-grid">' +
      '<div class="field"><label for="nk-rolls">Paper towel rolls per week <output class="range-out" for="nk-rolls">2</output></label><input type="range" id="nk-rolls" min="0.5" max="6" step="0.5" value="2"></div>' +
      '<div class="field"><label for="nk-price">Price per roll ($)</label><input type="number" id="nk-price" min="0.2" max="6" step="0.05" value="1.60"></div>' +
      '<div class="field"><label for="nk-cut">How much you\'d replace</label><select id="nk-cut"><option value="0.5">About half</option><option value="0.75" selected>Most of it</option><option value="1">All of it</option></select></div>' +
      '<div class="field"><label for="nk-n">Cloth napkins / towels to buy</label><input type="number" id="nk-n" min="4" max="60" value="24"></div>' +
      '<div class="field"><label for="nk-each">Cost each ($) — thrifted ≈ 0.50</label><input type="number" id="nk-each" min="0" max="20" step="0.25" value="2"></div>' +
      '<div class="field"><label for="nk-wash">Laundry cost per extra load ($)</label><input type="number" id="nk-wash" min="0" max="5" step="0.05" value="0.40"></div>' +
      "</div>" +
      '<div class="tool-out" aria-live="polite"><div class="sub">Estimated first-year savings</div><div class="big nk-big"></div><div class="tool-kpis nk-kpis"></div></div>' +
      '<p class="tool-note">Assumes cloth napkins ride along with laundry you\'re already doing about half the time, plus one extra small load a week. Your utility rates and habits will move the numbers.</p>';
    var f = {};
    ["rolls", "price", "cut", "n", "each", "wash"].forEach(function (k) { f[k] = $("#nk-" + k, el); f[k].addEventListener("input", run); f[k].addEventListener("change", run); });
    function run() {
      $("output", el).textContent = f.rolls.value;
      var rolls = +f.rolls.value * 52 * +f.cut.value, paper = rolls * (+f.price.value || 0);
      var upfront = (+f.n.value || 0) * (+f.each.value || 0), wash = 52 * 0.5 * (+f.wash.value || 0);
      var y1 = paper - upfront - wash, y3 = paper * 3 - upfront - wash * 3;
      var weekly = (paper - wash) / 52, be = weekly > 0 ? Math.ceil(upfront / weekly) : null;
      $(".nk-big", el).textContent = (y1 >= 0 ? "" : "−") + money(Math.abs(y1));
      $(".nk-kpis", el).innerHTML = "<div><small>Rolls avoided / year</small><b>" + Math.round(rolls) + "</b></div><div><small>Three-year savings</small><b>" + money(y3) + "</b></div><div><small>Pays for itself in</small><b>" + (be === null ? "—" : be + " weeks") + "</b></div><div><small>Up-front cost</small><b>" + money(upfront) + "</b></div>";
    }
    run();
  }

  /* ================= Wedding exit quiz ================= */
  function exitQuiz(el) {
    var Q = [
      ["When will you make your exit?", [["Before dark", { bubbles: 2, petals: 2, lavender: 2, ribbons: 1, confetti: 1, car: 1 }], ["After dark", { sparklers: 3, glow: 2, car: 1, lastdance: 1 }]]],
      ["Where does it happen?", [["Outdoors", { sparklers: 1, petals: 1, lavender: 2, confetti: 1, bubbles: 1 }], ["Indoors or covered", { ribbons: 2, glow: 2, bubbles: 1, lastdance: 1, bells: 1 }], ["Not sure yet", { ribbons: 1, bubbles: 1, car: 1 }]]],
      ["Pick the vibe", [["Classic & romantic", { sparklers: 2, petals: 2, car: 2 }], ["Boho & natural", { lavender: 3, petals: 1, ribbons: 1 }], ["Big party energy", { confetti: 3, glow: 2, sparklers: 1 }], ["Quiet & minimal", { lastdance: 3, bells: 1, car: 1 }]]],
      ["Guests include lots of kids?", [["Yes", { bubbles: 3, ribbons: 2, glow: 1 }], ["A few", { bubbles: 1, ribbons: 1 }], ["Not really", { sparklers: 1, lastdance: 1 }]]],
      ["Exit budget?", [["Under $50", { bubbles: 1, ribbons: 1, lastdance: 2, bells: 1 }], ["$50–$150", { sparklers: 1, lavender: 1, petals: 1, glow: 1 }], ["More is fine", { confetti: 1, car: 2, petals: 1 }]]]
    ];
    var R = {
      sparklers: ["Sparkler send-off", "The glowing tunnel that photographs beautifully after dark. Use long (20–36 in) low-smoke sparklers, light in waves from one end, and confirm the venue and local fire rules allow them."],
      bubbles: ["Bubble exit", "Cheap, kid-proof and pretty in backlight. Bubbles read best in late-afternoon sun; ask guests to blow toward the aisle, not into faces."],
      petals: ["Fresh or freeze-dried petal toss", "Timeless and colorful. Freeze-dried petals don't stain and many venues allow them when rice and glitter are banned."],
      lavender: ["Dried lavender toss", "Smells wonderful, looks soft and natural in photos, and is easy for most outdoor venues to clean up."],
      ribbons: ["Ribbon wands", "Reusable, mess-free and venue-friendly indoors. Pick ribbon in your palette so the motion blur reads as color."],
      glow: ["LED wands or glow sticks", "Sparkler energy without the flame — ideal for indoor venues and parties that run late."],
      confetti: ["Biodegradable confetti burst", "Maximum celebration. Confirm the venue allows it and assign two friends to launch on cue for a dramatic frame."],
      car: ["Getaway car moment", "A vintage car, a pickup with cans on the bumper or even a decorated golf cart. Plan the route so guests can line it."],
      lastdance: ["Private last dance", "Clear the room, keep your photographer, and dance alone to one song. Quiet, intimate, often the favorite photos."],
      bells: ["Ringing bells", "A soft, old-world send-off that works anywhere and costs very little."]
    };
    var step = 0, score = {};
    function render() {
      if (step >= Q.length) {
        var best = Object.keys(score).sort(function (a, b) { return score[b] - score[a]; });
        var top = R[best[0]], alt = R[best[1]];
        el.querySelector(".quiz-body").innerHTML = '<div class="quiz-progress"><span style="width:100%"></span></div><div class="quiz-step quiz-result"><div class="sub">Your best-fit exit</div><h4>' + top[0] + "</h4><p>" + top[1] + "</p>" + (alt ? "<p><strong>Runner-up:</strong> " + alt[0] + " — " + alt[1] + "</p>" : "") + '<button type="button" class="btn btn-sm btn-ghost" data-restart>Take it again</button></div>';
        return;
      }
      var q = Q[step];
      el.querySelector(".quiz-body").innerHTML = '<div class="quiz-progress"><span style="width:' + (step / Q.length * 100) + '%"></span></div><div class="quiz-step"><div class="sub">Question ' + (step + 1) + " of " + Q.length + "</div><h4>" + q[0] + '</h4><div class="seg">' + q[1].map(function (o, i) { return '<button type="button" data-opt="' + i + '">' + o[0] + "</button>"; }).join("") + "</div></div>";
    }
    el.innerHTML += '<div class="quiz-body" aria-live="polite"></div>';
    el.addEventListener("click", function (e) {
      var b = e.target.closest("[data-opt]");
      if (b) {
        var w = Q[step][1][+b.getAttribute("data-opt")][1];
        Object.keys(w).forEach(function (k) { score[k] = (score[k] || 0) + w[k]; });
        step++; render(); return;
      }
      if (e.target.closest("[data-restart]")) { step = 0; score = {}; render(); }
    });
    render();
  }

  /* ================= Engagement outfit palettes ================= */
  function outfit(el) {
    var P = {
      "Desert": [["Terracotta", "#c0603a"], ["Sand", "#e6d3b3"], ["Sage", "#9aa688"], ["Cream", "#f6efe2"], ["Rust", "#8f3f22"]],
      "City streets": [["Charcoal", "#33363b"], ["Camel", "#c19a6b"], ["Ivory", "#f4efe4"], ["Navy", "#23304a"], ["Burgundy", "#6d2433"]],
      "Mountains & forest": [["Forest", "#2f4a36"], ["Cream", "#f2ead8"], ["Mustard", "#c9972f"], ["Denim", "#5873a0"], ["Walnut", "#6a4a33"]],
      "Lake or water": [["White", "#fbfbf8"], ["Dusty blue", "#9db3c8"], ["Blush", "#e7c1b8"], ["Sand", "#e2d2b8"], ["Navy", "#25324a"]],
      "Winter lights": [["Emerald", "#1f5a46"], ["Burgundy", "#6a1f2d"], ["Cream", "#f3ead9"], ["Camel", "#b88d5f"], ["Black", "#1c1b1d"]],
      "Fields & gardens": [["Lavender", "#b6a6cc"], ["Cream", "#f6f0e2"], ["Sage", "#a8b597"], ["Butter", "#f0dc9b"], ["Dusty rose", "#cf9a96"]]
    };
    var TIPS = {
      "Desert": "Warm earth tones echo red rock and sand; avoid bright orange that disappears into the landscape. One flowing piece — a dress, a linen shirt — catches desert wind.",
      "City streets": "Concrete and glass are neutral, so you can wear richer colors. Tailored shapes and a coat or blazer look sharp against architecture.",
      "Mountains & forest": "Deep greens blend in; pull one partner into cream or mustard so you separate from the trees.",
      "Lake or water": "Light, airy tones reflect the water. Skip busy prints near the shoreline — reflections already add pattern.",
      "Winter lights": "Jewel tones glow under string lights and hold up against dark backgrounds. Add texture: wool, velvet, a knit scarf.",
      "Fields & gardens": "Soft pastels feel like spring. Coordinate rather than match — one partner in the lightest shade, the other a step deeper."
    };
    var keys = Object.keys(P), cur = keys[0];
    el.innerHTML += '<div class="seg" role="group" aria-label="Choose a setting">' + keys.map(function (k, i) { return '<button type="button" aria-pressed="' + (i === 0) + '" data-set="' + esc(k) + '">' + esc(k) + "</button>"; }).join("") + '</div><div class="tool-out" aria-live="polite" style="margin-top:16px"><div class="swatches"></div><p class="sub of-tip" style="margin:12px 0 0"></p><p class="sub of-pick" style="margin:8px 0 0"></p></div>';
    function render() {
      $(".swatches", el).innerHTML = P[cur].map(function (c) { return '<button type="button" style="background:' + c[1] + '" data-c="' + esc(c[0]) + '" aria-label="' + esc(c[0]) + " " + c[1] + '"><span>' + esc(c[0]) + "<br>" + c[1] + "</span></button>"; }).join("");
      $(".of-tip", el).textContent = TIPS[cur];
      var p = P[cur];
      $(".of-pick", el).innerHTML = "<strong>Try:</strong> one of you in " + p[0][0].toLowerCase() + " or " + p[4][0].toLowerCase() + ", the other in " + p[1][0].toLowerCase() + " or " + p[3][0].toLowerCase() + ", with " + p[2][0].toLowerCase() + " as an accent (shoes, a jacket, a bag).";
    }
    el.addEventListener("click", function (e) {
      var b = e.target.closest("[data-set]");
      if (b) { cur = b.getAttribute("data-set"); $$("[data-set]", el).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); }); render(); return; }
      var s = e.target.closest("[data-c]");
      if (s) $(".of-pick", el).innerHTML = "<strong>" + esc(s.getAttribute("data-c")) + "</strong> — build one outfit around it, then pick a lighter or deeper neighbor from the palette for your partner.";
    });
    render();
  }

  var REG = { "golden-hour": goldenHour, timeline: timeline, budget: budget, chandelier: chandelier, pegrail: pegrail, napkins: napkins, "exit-quiz": exitQuiz, outfit: outfit };
  $$("[data-tool]").forEach(function (el) {
    var fn = REG[el.getAttribute("data-tool")];
    if (!fn) return;
    var ns = $("noscript", el);
    if (ns) ns.remove();
    try { fn(el); } catch (e) { if (window.console) console.error(e); }
  });
})();
