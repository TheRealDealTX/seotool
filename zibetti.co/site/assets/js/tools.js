/* zibetti.co — interactive planning tools (golden hour, timeline, locations, estimator) */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var RAD = Math.PI / 180;

  /* ---------------- solar position ---------------- */
  function sunElevation(ms, lat, lng) {
    var n = ms / 86400000 + 2440587.5 - 2451545.0;
    var L = (280.460 + 0.9856474 * n) % 360;
    var g = ((357.528 + 0.9856003 * n) % 360) * RAD;
    var lambda = (L + 1.915 * Math.sin(g) + 0.020 * Math.sin(2 * g)) * RAD;
    var eps = (23.439 - 0.0000004 * n) * RAD;
    var ra = Math.atan2(Math.cos(eps) * Math.sin(lambda), Math.cos(lambda));
    var dec = Math.asin(Math.sin(eps) * Math.sin(lambda));
    var gmst = (18.697374558 + 24.06570982441908 * n) % 24;
    var ha = (gmst * 15 + lng) * RAD - ra;
    var la = lat * RAD;
    return Math.asin(Math.sin(la) * Math.sin(dec) + Math.cos(la) * Math.cos(dec) * Math.cos(ha)) / RAD;
  }

  // Offset (ms) of an IANA zone from UTC at a given instant.
  function tzOffset(tz, ms) {
    try {
      var parts = new Intl.DateTimeFormat("en-US", { timeZone: tz, hourCycle: "h23", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit" }).formatToParts(new Date(ms));
      var o = {};
      parts.forEach(function (p) { o[p.type] = p.value; });
      var asUTC = Date.UTC(+o.year, +o.month - 1, +o.day, +o.hour % 24, +o.minute, +o.second);
      return asUTC - Math.floor(ms / 1000) * 1000;
    } catch (e) {
      return -new Date(ms).getTimezoneOffset() * 60000;
    }
  }

  // Returns the day's samples and the key light events for a date string (yyyy-mm-dd).
  function solarDay(dateStr, lat, lng, tz) {
    var p = dateStr.split("-").map(Number);
    var noonUTC = Date.UTC(p[0], p[1] - 1, p[2], 12);
    var off = tzOffset(tz, noonUTC);
    var midnight = Date.UTC(p[0], p[1] - 1, p[2]) - off;
    var samples = [];
    for (var m = 0; m <= 1440; m++) samples.push(sunElevation(midnight + m * 60000, lat, lng));
    function cross(level, rising) {
      for (var i = 1; i < samples.length; i++) {
        var a = samples[i - 1], b = samples[i];
        if (rising ? (a < level && b >= level) : (a > level && b <= level)) {
          return i - 1 + (level - a) / (b - a); // fractional minute after local midnight
        }
      }
      return null;
    }
    var maxE = Math.max.apply(null, samples);
    return {
      samples: samples, offset: off, maxElev: maxE,
      blueAmStart: cross(-6, true), goldAmStart: cross(-4, true), sunrise: cross(-0.833, true), goldAmEnd: cross(6, true),
      goldPmStart: cross(6, false), sunset: cross(-0.833, false), bluePmStart: cross(-4, false), bluePmEnd: cross(-6, false),
      noon: samples.indexOf(maxE)
    };
  }

  function fmtMin(min, h24) {
    if (min === null || min === undefined || isNaN(min)) return "—";
    min = Math.round(min);
    min = ((min % 1440) + 1440) % 1440;
    var h = Math.floor(min / 60), m = min % 60;
    if (h24) return (h < 10 ? "0" : "") + h + ":" + (m < 10 ? "0" : "") + m;
    var ap = h >= 12 ? "pm" : "am";
    var hh = h % 12 || 12;
    return hh + ":" + (m < 10 ? "0" : "") + m + " " + ap;
  }
  function dur(a, b) {
    if (a === null || b === null) return "";
    var d = Math.round(b - a);
    return d >= 60 ? Math.floor(d / 60) + "h " + (d % 60) + "m" : d + " min";
  }
  function todayStr() {
    var d = new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }

  var PLACES = {
    provo: { n: "Provo, UT", lat: 40.2338, lng: -111.6585, tz: "America/Denver" },
    slc: { n: "Salt Lake City, UT", lat: 40.7608, lng: -111.8910, tz: "America/Denver" },
    parkcity: { n: "Park City, UT", lat: 40.6461, lng: -111.4980, tz: "America/Denver" },
    moab: { n: "Moab / Arches, UT", lat: 38.5733, lng: -109.5498, tz: "America/Denver" },
    zion: { n: "Springdale / Zion, UT", lat: 37.1889, lng: -112.9986, tz: "America/Denver" },
    bryce: { n: "Bryce Canyon, UT", lat: 37.6283, lng: -112.1677, tz: "America/Denver" },
    capreef: { n: "Capitol Reef, UT", lat: 38.2997, lng: -111.4199, tz: "America/Denver" },
    uintas: { n: "Uinta Mountains (Mirror Lake), UT", lat: 40.7011, lng: -110.8857, tz: "America/Denver" },
    salt: { n: "Bonneville Salt Flats, UT", lat: 40.7650, lng: -113.8890, tz: "America/Denver" },
    stgeorge: { n: "St. George, UT", lat: 37.0965, lng: -113.5684, tz: "America/Denver" },
    page: { n: "Page / Lake Powell, AZ", lat: 36.9147, lng: -111.4558, tz: "America/Phoenix" },
    sedona: { n: "Sedona, AZ", lat: 34.8697, lng: -111.7610, tz: "America/Phoenix" },
    tetons: { n: "Grand Teton, WY", lat: 43.7904, lng: -110.6818, tz: "America/Denver" },
    glacier: { n: "Glacier National Park, MT", lat: 48.6967, lng: -113.7183, tz: "America/Denver" },
    yosemite: { n: "Yosemite Valley, CA", lat: 37.7456, lng: -119.5936, tz: "America/Los_Angeles" },
    bigsur: { n: "Big Sur, CA", lat: 36.2704, lng: -121.8081, tz: "America/Los_Angeles" },
    banff: { n: "Banff, Canada", lat: 51.1784, lng: -115.5708, tz: "America/Edmonton" },
    tulum: { n: "Tulum, Mexico", lat: 20.2114, lng: -87.4654, tz: "America/Cancun" },
    iceland: { n: "Vík, Iceland", lat: 63.4186, lng: -19.0060, tz: "Atlantic/Reykjavik" },
    dolomites: { n: "Dolomites, Italy", lat: 46.5405, lng: 11.8550, tz: "Europe/Rome" },
    como: { n: "Lake Como, Italy", lat: 45.9853, lng: 9.2572, tz: "Europe/Rome" }
  };
  function fillPlaces(sel) {
    Object.keys(PLACES).forEach(function (k) {
      var o = document.createElement("option");
      o.value = k; o.textContent = PLACES[k].n;
      sel.appendChild(o);
    });
  }

  /* ---------------- golden hour calculator ---------------- */
  var gh = $("#golden-hour-tool");
  if (gh) {
    var gSel = $("#gh-place", gh), gDate = $("#gh-date", gh), gLat = $("#gh-lat", gh), gLng = $("#gh-lng", gh), gCustom = $("#gh-custom", gh);
    fillPlaces(gSel);
    var optC = document.createElement("option"); optC.value = "custom"; optC.textContent = "Custom coordinates / my location"; gSel.appendChild(optC);
    gDate.value = todayStr();
    var ghRender = function () {
      var place = PLACES[gSel.value], lat, lng, tz, name;
      gCustom.hidden = gSel.value !== "custom";
      if (place) { lat = place.lat; lng = place.lng; tz = place.tz; name = place.n; }
      else {
        lat = parseFloat(gLat.value); lng = parseFloat(gLng.value);
        tz = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC"; name = "your coordinates";
        if (isNaN(lat) || isNaN(lng) || Math.abs(lat) > 90 || Math.abs(lng) > 180) { $("#gh-out", gh).innerHTML = '<div class="empty">Enter a latitude and longitude, or tap “Use my location”.</div>'; return; }
      }
      if (!gDate.value) return;
      var d = solarDay(gDate.value, lat, lng, tz);
      var html = "";
      html += '<div class="result-grid">';
      html += '<div class="result golden"><div class="k">Evening golden hour</div><div class="v">' + fmtMin(d.goldPmStart) + " – " + fmtMin(d.bluePmStart) + '</div><small>' + dur(d.goldPmStart, d.bluePmStart) + ' of warm, low light</small></div>';
      html += '<div class="result blue"><div class="k">Evening blue hour</div><div class="v">' + fmtMin(d.bluePmStart) + " – " + fmtMin(d.bluePmEnd) + '</div><small>' + (d.bluePmEnd === null ? "Sky never gets fully dark tonight" : dur(d.bluePmStart, d.bluePmEnd) + " of soft twilight") + '</small></div>';
      html += '<div class="result"><div class="k">Sunrise</div><div class="v">' + fmtMin(d.sunrise) + '</div></div>';
      html += '<div class="result"><div class="k">Sunset</div><div class="v">' + fmtMin(d.sunset) + '</div></div>';
      html += '<div class="result golden"><div class="k">Morning golden hour</div><div class="v">' + fmtMin(d.goldAmStart) + " – " + fmtMin(d.goldAmEnd) + '</div></div>';
      html += '<div class="result"><div class="k">Solar noon / sun height</div><div class="v">' + fmtMin(d.noon) + '</div><small>Max elevation ' + Math.round(d.maxElev) + '°</small></div>';
      html += "</div>";
      var tip;
      if (d.sunset === null) tip = "The sun does not set on this date here — midnight-sun light means golden tones can last for hours.";
      else tip = "For portraits, start your couple session around <b>" + fmtMin(d.goldPmStart - 10) + "</b> and plan to keep shooting until <b>" + fmtMin(d.bluePmStart + 10) + "</b>. In canyons and below mountain ridges the light leaves earlier, so shave 20–40 minutes off the evening window.";
      html += '<p class="callout" style="margin-top:18px"><strong>Our timing tip</strong>' + tip + "</p>";
      html += '<p class="muted" style="font-size:.85rem">Times are for ' + name + " in local time (" + tz.replace("_", " ") + "). Calculated from the sun’s position; accuracy is within a couple of minutes on flat horizons.</p>";
      $("#gh-out", gh).innerHTML = html;
      drawArc($("#gh-arc", gh), d);
    };
    $("#gh-geo", gh).addEventListener("click", function () {
      if (!navigator.geolocation) return;
      navigator.geolocation.getCurrentPosition(function (pos) {
        gSel.value = "custom"; gLat.value = pos.coords.latitude.toFixed(4); gLng.value = pos.coords.longitude.toFixed(4); ghRender();
      }, function () { alert("We couldn't read your location. Enter coordinates instead."); });
    });
    [gSel, gDate, gLat, gLng].forEach(function (el) { el.addEventListener("input", ghRender); el.addEventListener("change", ghRender); });
    ghRender();
  }

  function drawArc(svg, d) {
    if (!svg) return;
    var W = 600, H = 200, base = 130, scale = 1.6;
    var y = function (e) { return base - e * scale; };
    var pts = [];
    for (var m = 0; m <= 1440; m += 10) pts.push((m / 1440 * W).toFixed(1) + "," + Math.max(4, Math.min(H - 4, y(d.samples[m]))).toFixed(1));
    var band = function (a, b, color, op) {
      if (a === null || b === null) return "";
      return '<rect x="' + (a / 1440 * W).toFixed(1) + '" y="0" width="' + ((b - a) / 1440 * W).toFixed(1) + '" height="' + H + '" fill="' + color + '" opacity="' + op + '"/>';
    };
    var s = '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7efe4"/><stop offset="1" stop-color="#efe3d4"/></linearGradient></defs>';
    s += '<rect width="' + W + '" height="' + H + '" rx="14" fill="url(#sky)"/>';
    s += band(d.goldAmStart, d.goldAmEnd, "#f0b26f", .35) + band(d.goldPmStart, d.bluePmStart, "#f0b26f", .45);
    s += band(d.blueAmStart, d.goldAmStart, "#8ea6cf", .35) + band(d.bluePmStart, d.bluePmEnd, "#8ea6cf", .45);
    s += '<line x1="0" x2="' + W + '" y1="' + base + '" y2="' + base + '" stroke="#1d1a17" stroke-opacity=".35" stroke-dasharray="4 5"/>';
    s += '<polyline points="' + pts.join(" ") + '" fill="none" stroke="#b4623a" stroke-width="2.5" stroke-linejoin="round"/>';
    if (d.noon !== null) s += '<circle cx="' + (d.noon / 1440 * W).toFixed(1) + '" cy="' + Math.max(10, y(d.maxElev)).toFixed(1) + '" r="9" fill="#e9a24f"><animate attributeName="r" values="8;11;8" dur="3s" repeatCount="indefinite"/></circle>';
    ["12a", "6a", "12p", "6p", "12a"].forEach(function (t, i) { s += '<text x="' + Math.min(W - 22, Math.max(4, i * W / 4 - (i ? 10 : 0))) + '" y="' + (H - 10) + '" font-size="12" font-family="Manrope, sans-serif" fill="#6f655b">' + t + "</text>"; });
    s += '<text x="8" y="' + (base - 6) + '" font-size="11" font-family="Manrope, sans-serif" fill="#6f655b">horizon</text>';
    svg.innerHTML = s;
  }

  /* ---------------- wedding day timeline builder ---------------- */
  var tl = $("#timeline-tool");
  if (tl) {
    var tPlace = $("#tl-place", tl), tDate = $("#tl-date", tl);
    fillPlaces(tPlace);
    var dt = new Date(); dt.setMonth(dt.getMonth() + 6);
    tDate.value = dt.getFullYear() + "-" + String(dt.getMonth() + 1).padStart(2, "0") + "-" + String(dt.getDate()).padStart(2, "0");
    var tlRender = function () {
      var type = $("input[name=tl-type]:checked", tl).value;
      var place = PLACES[tPlace.value];
      var day = solarDay(tDate.value || todayStr(), place.lat, place.lng, place.tz);
      var sunset = day.sunset !== null ? Math.round(day.sunset) : 20 * 60;
      $("#tl-sunset", tl).textContent = fmtMin(sunset);
      var cer = $("#tl-ceremony", tl).value;
      var hours = parseFloat($("#tl-hours", tl).value);
      $("#tl-hours-val", tl).textContent = hours + " hours";
      var firstLook = $("#tl-firstlook", tl).checked;
      var ready = $("#tl-ready", tl).checked;
      var fam = parseInt($("#tl-family", tl).value, 10);
      var cerMin;
      if ($("#tl-auto", tl).checked) {
        cerMin = type === "elopement" ? sunset - 90 : sunset - (firstLook ? 150 : 210);
        cerMin = Math.round(cerMin / 15) * 15;
        $("#tl-ceremony", tl).value = fmtMin(cerMin, true);
        $("#tl-ceremony", tl).disabled = true;
      } else {
        $("#tl-ceremony", tl).disabled = false;
        var hm = (cer || "16:00").split(":");
        cerMin = parseInt(hm[0], 10) * 60 + parseInt(hm[1], 10);
      }
      var items = [];
      var add = function (t, title, note, gold) { items.push({ t: t, title: title, note: note || "", gold: !!gold }); };
      var t;
      if (type === "elopement") {
        t = cerMin;
        var pre = [];
        if (ready) pre.push([45, "Getting ready + details", "Dress, rings, letters and the little things — usually at your rental or hotel."]);
        if (firstLook) pre.push([20, "First look", "A quiet moment just for the two of you before vows."]);
        pre.push([40, "Travel / short hike to the vow spot", "Built-in buffer for parking, trail time and wind-swept hair."]);
        var start = cerMin - pre.reduce(function (a, b) { return a + b[0]; }, 0);
        t = start;
        pre.forEach(function (p) { add(t, p[1], p[2]); t += p[0]; });
        add(cerMin, "Vows", "Read your own words, exchange rings, sign the license with your officiant and witnesses.");
        add(cerMin + 25, "Celebration + champagne pop", "Hugs with any guests, a toast, a little picnic if you like.");
        add(cerMin + 45, "Adventure portraits", "Wander, explore and let the landscape do the talking.");
        add(sunset - 45, "Golden hour portraits", "The warmest, softest light of the day.", true);
        add(sunset + 5, "Blue hour + sparklers or stargazing", "Moody twilight frames, then the last shots of the night.", true);
        var endE = start + hours * 60;
        if (endE > sunset + 30) add(endE - 1, "Wrap", "Photography ends — time for dinner under the stars.");
      } else {
        var preBlocks = [];
        if (ready) { preBlocks.push([30, "Details + flat lays", "Rings, invitations, shoes, perfume, florals."]); preBlocks.push([45, "Getting ready", "Final touches, getting into the dress and suit, letters or gifts."]); }
        if (firstLook) {
          preBlocks.push([20, "First look", "A private reveal — the most relaxed way to start the day."]);
          preBlocks.push([35, "Couple portraits", "Your main portrait session, unhurried."]);
          preBlocks.push([30, "Wedding party photos", "Groups, then fun candids with your crew."]);
        }
        preBlocks.push([30, "Tuck away before guests arrive", "Hydrate, touch up and breathe."]);
        var startW = cerMin - preBlocks.reduce(function (a, b) { return a + b[0]; }, 0);
        t = startW;
        preBlocks.forEach(function (p) { add(t, p[1], p[2]); t += p[0]; });
        add(cerMin, "Ceremony", "Typically 20–30 minutes. Remember an unplugged ceremony announcement!");
        t = cerMin + 30;
        add(t, "Family formals", "We work from your list — " + fam + " minutes for the group size you chose."); t += fam;
        if (!firstLook) { add(t, "Wedding party photos", "Fast and fun before the drinks get warm."); t += 25; add(t, "Couple portraits", "Your main portraits during cocktail hour."); t += 35; }
        else { add(t, "Join cocktail hour", "Because you did a first look, you get to enjoy it!"); t += 30; }
        var recep = Math.max(t, cerMin + 75);
        add(recep, "Grand entrance + dinner", "We grab a bite while you eat so we’re ready for toasts."); t = recep + 50;
        add(t, "Toasts", "Two or three toasts is the sweet spot."); t += 20;
        add(t, "First dance + parent dances", ""); t += 15;
        add(sunset - 25, "Sunset portraits", "A 15-minute escape for golden light — guests won’t even notice.", true);
        add(t + 10, "Cake cutting", ""); t += 25;
        add(t, "Open dancing", "Candids, dance-floor energy, details of the room.");
        var endW = startW + hours * 60;
        add(endW - 15, "Grand send-off", "Sparklers, confetti or bubbles — scheduled 15 minutes before coverage ends.");
      }
      items.sort(function (a, b) { return a.t - b.t; });
      var first = items[0].t, last = type === "elopement" ? Math.max(items[items.length - 1].t, first + hours * 60) : first + hours * 60;
      var needed = (items[items.length - 1].t - first) / 60;
      var html = '<ol class="timeline">';
      items.forEach(function (it, i) {
        html += '<li class="' + (it.gold ? "gold" : "") + '" style="animation-delay:' + (i * 40) + 'ms"><time>' + fmtMin(it.t) + "</time><div><b>" + it.title + "</b>" + (it.note ? "<span>" + it.note + "</span>" : "") + "</div></li>";
      });
      html += "</ol>";
      var warn = "";
      if (needed > hours + 0.1) warn = '<p class="notice err" style="margin-top:16px">This plan needs about ' + Math.ceil(needed * 2) / 2 + " hours of coverage. Add time or trim the morning blocks.</p>";
      $("#tl-out", tl).innerHTML = '<p class="muted" style="margin-bottom:6px">Coverage ' + fmtMin(first) + " – " + fmtMin(last) + " · sunset " + fmtMin(sunset) + " at " + place.n + "</p>" + html + warn;
    };
    $$("input, select", tl).forEach(function (el) { el.addEventListener("input", tlRender); el.addEventListener("change", tlRender); });
    $("#tl-print", tl).addEventListener("click", function () { window.print(); });
    $("#tl-copy", tl).addEventListener("click", function () {
      var txt = $$("#tl-out li", tl).map(function (li) { return li.querySelector("time").textContent + "  " + li.querySelector("b").textContent; }).join("\n");
      if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { $("#tl-copy", tl).textContent = "Copied!"; setTimeout(function () { $("#tl-copy", tl).textContent = "Copy timeline"; }, 1800); });
    });
    tlRender();
  }

  /* ---------------- Utah elopement location finder ---------------- */
  var lf = $("#location-tool");
  if (lf) {
    var LOCS = [
      { n: "Arches National Park", land: ["redrock", "desert"], s: ["spring", "fall", "winter"], hike: 1, drive: 3.5, guests: 12, permit: "National park special use permit", d: "Sandstone arches, fins and endless sky. Sunrise is quieter than sunset and the light on the rock is unreal." },
      { n: "Dead Horse Point State Park", land: ["redrock", "canyon"], s: ["spring", "fall", "winter", "summer"], hike: 0, drive: 3.5, guests: 50, permit: "State park special use permit", d: "A dramatic rim-top overlook of a gooseneck in the Colorado River — huge views with almost no walking." },
      { n: "Canyonlands – Island in the Sky", land: ["redrock", "canyon"], s: ["spring", "fall", "winter"], hike: 1, drive: 3.75, guests: 12, permit: "National park special use permit", d: "Layered canyon overlooks that drop away for miles. Mesa Arch at sunrise is iconic (and busy)." },
      { n: "Zion National Park", land: ["redrock", "canyon", "river"], s: ["spring", "fall", "winter"], hike: 1, drive: 4, guests: 12, permit: "National park special use permit", d: "Towering cliffs, cottonwoods and the Virgin River. Fall color in the canyon is a dream." },
      { n: "Bryce Canyon National Park", land: ["redrock", "snow"], s: ["spring", "summer", "fall", "winter"], hike: 1, drive: 3.75, guests: 12, permit: "National park special use permit", d: "Orange hoodoos at high elevation — cool in summer and breathtaking dusted with winter snow." },
      { n: "Capitol Reef National Park", land: ["redrock", "desert"], s: ["spring", "fall"], hike: 1, drive: 3, guests: 12, permit: "National park special use permit", d: "Quieter red-rock domes, historic orchards and a fraction of the crowds." },
      { n: "Goblin Valley State Park", land: ["desert", "redrock"], s: ["spring", "fall", "winter"], hike: 0, drive: 3, guests: 30, permit: "State park special use permit", d: "Playful mushroom-shaped hoodoos that feel like another planet." },
      { n: "Factory Butte badlands", land: ["desert"], s: ["spring", "fall"], hike: 0, drive: 3.5, guests: 10, permit: "BLM land — check current rules", d: "Gray, moonscape badlands with wild texture. Bring a high-clearance vehicle." },
      { n: "San Rafael Swell slot canyons", land: ["canyon", "redrock"], s: ["spring", "fall"], hike: 2, drive: 3, guests: 6, permit: "BLM land — check current rules", d: "Narrow, glowing slot canyons for adventurous couples. Never enter with rain in the forecast." },
      { n: "Bonneville Salt Flats", land: ["saltflats", "desert"], s: ["summer", "fall"], hike: 0, drive: 2.5, guests: 30, permit: "BLM land — check current rules", d: "A blindingly white, perfectly flat horizon. Minimal and striking — and mirror-like after rain." },
      { n: "Antelope Island State Park", land: ["lake", "desert"], s: ["spring", "fall"], hike: 0, drive: 1.5, guests: 50, permit: "State park special use permit", d: "Great Salt Lake shoreline, wild bison and golden grass. Bugs can be intense in early summer." },
      { n: "Mirror Lake Highway – Uinta Mountains", land: ["alpine", "lake", "forest"], s: ["summer", "fall"], hike: 1, drive: 2, guests: 20, permit: "National forest permit", d: "High alpine lakes, pine forests and wildflowers. The highway closes in winter." },
      { n: "Alpine Loop & Mount Timpanogos", land: ["alpine", "forest"], s: ["summer", "fall"], hike: 1, drive: 0.5, guests: 20, permit: "National forest permit", d: "Aspens, meadows and big granite peaks minutes from Provo. Peak fall color is usually late September." },
      { n: "Tibble Fork Reservoir – American Fork Canyon", land: ["alpine", "lake", "forest"], s: ["summer", "fall"], hike: 0, drive: 0.5, guests: 30, permit: "National forest permit", d: "A calm reservoir ringed by mountains — easy access for families and older guests." },
      { n: "Sundance Mountain Resort", land: ["alpine", "forest", "snow"], s: ["spring", "summer", "fall", "winter"], hike: 0, drive: 0.5, guests: 150, permit: "Private venue booking", d: "A rustic-luxe resort under Timpanogos with year-round venues, lodging and dining." },
      { n: "Guardsman Pass – Park City", land: ["alpine", "forest"], s: ["summer", "fall"], hike: 0, drive: 1, guests: 20, permit: "National forest / county rules", d: "Rolling ridgelines and glowing aspen groves with roadside access." },
      { n: "Snow Canyon State Park", land: ["redrock", "desert"], s: ["spring", "fall", "winter"], hike: 1, drive: 3.75, guests: 40, permit: "State park special use permit", d: "Red and white sandstone with black lava flows — warm enough for winter elopements." },
      { n: "Lake Powell – Glen Canyon", land: ["lake", "redrock", "canyon"], s: ["spring", "summer", "fall"], hike: 0, drive: 5, guests: 20, permit: "Recreation area special use permit", d: "Turquoise water against red canyon walls. Hire a boat and find your own private cove." },
      { n: "Bridal Veil Falls – Provo Canyon", land: ["forest", "river"], s: ["spring", "summer"], hike: 0, drive: 0.25, guests: 30, permit: "Check county / city rules", d: "A tall, two-tiered waterfall right off the canyon trail. Best when snowmelt runs high." },
      { n: "Monument Valley", land: ["desert", "redrock"], s: ["spring", "fall", "winter"], hike: 0, drive: 5.5, guests: 20, permit: "Navajo Nation tribal permit", d: "Legendary buttes on Navajo Nation land. Always work with a licensed Navajo guide." }
    ];
    var lfRender = function () {
      var season = $("#lf-season", lf).value;
      var lands = $$("input[name=lf-land]:checked", lf).map(function (i) { return i.value; });
      var hike = parseInt($("#lf-hike", lf).value, 10);
      var drive = parseFloat($("#lf-drive", lf).value);
      var guests = parseInt($("#lf-guests", lf).value, 10) || 2;
      $("#lf-drive-val", lf).textContent = drive >= 6 ? "Any distance" : "Up to " + drive + " hrs from Provo";
      var res = LOCS.map(function (l) {
        var score = 0, ok = true;
        if (season !== "any") { if (l.s.indexOf(season) > -1) score += 3; else ok = false; }
        if (lands.length) { var hit = lands.filter(function (x) { return l.land.indexOf(x) > -1; }).length; if (!hit) ok = false; score += hit * 2; }
        if (l.hike > hike) ok = false;
        if (drive < 6 && l.drive > drive) ok = false;
        if (guests > l.guests) ok = false;
        score += (6 - Math.min(l.drive, 6)) * .3;
        return { l: l, score: score, ok: ok };
      }).filter(function (r) { return r.ok; }).sort(function (a, b) { return b.score - a.score; });
      var out = $("#lf-out", lf);
      $("#lf-count", lf).textContent = res.length + (res.length === 1 ? " match" : " matches");
      if (!res.length) { out.innerHTML = '<div class="empty">No spots match all of that. Try a longer drive, a different season, or more guests allowed.</div>'; return; }
      var hikeTxt = ["Walk-up", "Short hike", "Real hike"];
      out.innerHTML = res.map(function (r, i) {
        var l = r.l;
        return '<article class="loc" style="animation-delay:' + i * 40 + 'ms"><div class="loc-top"><h3>' + l.n + '</h3><span class="score">' + (l.drive < 1 ? Math.round(l.drive * 60) + " min" : l.drive + " hrs") + '</span></div><p>' + l.d + '</p><div class="tags"><span>' + hikeTxt[l.hike] + "</span><span>Up to ~" + l.guests + " guests</span><span>" + l.permit + "</span></div></article>";
      }).join("");
    };
    $$("input, select", lf).forEach(function (el) { el.addEventListener("input", lfRender); el.addEventListener("change", lfRender); });
    lfRender();
  }

  /* ---------------- pricing estimator ---------------- */
  var est = $("#estimator");
  if (est) {
    var BASE = {
      session: { n: "Engagement / couples session", p: 750, h: 2 },
      elope: { n: "Utah elopement", p: 2400, h: 4 },
      utah: { n: "Utah wedding", p: 3600, h: 8 },
      stateside: { n: "Stateside destination", p: 5200, h: 8 },
      intl: { n: "International destination", p: 6500, h: 10 }
    };
    var money = function (n) { return "$" + n.toLocaleString("en-US"); };
    var estRender = function () {
      var k = $("input[name=est-type]:checked", est).value, b = BASE[k];
      var service = $("input[name=est-service]:checked", est).value;
      var extraH = parseInt($("#est-hours", est).value, 10);
      $("#est-hours-val", est).textContent = extraH ? "+" + extraH + (extraH === 1 ? " hour" : " hours") : "None";
      var lines = [], total = 0;
      if (service === "film") { var fp = Math.round(b.p * 0.95 / 50) * 50; lines.push([b.n + " — film only", fp]); total += fp; }
      else { lines.push([b.n + " — photography (" + b.h + " hrs)", b.p]); total += b.p; }
      if (service === "both") { var add = k === "session" ? 450 : 2000; lines.push(["Add wedding film", add]); total += add; }
      if (extraH) { var hp = extraH * (service === "both" ? 450 : 300); lines.push(["Extra coverage (" + extraH + " hrs)", hp]); total += hp; }
      if ($("#est-second", est).checked && k !== "session") { lines.push(["Second photographer", 600]); total += 600; }
      if ($("#est-engage", est).checked && k !== "session") { lines.push(["Engagement session", 500]); total += 500; }
      if ($("#est-album", est).checked) { lines.push(["Heirloom linen album", 650]); total += 650; }
      if ($("#est-raw", est).checked) { lines.push(["Unedited files on a drive", 150]); total += 150; }
      $("#est-second", est).disabled = k === "session";
      $("#est-engage", est).disabled = k === "session";
      var tEl = $("#est-total", est), from = parseInt(tEl.getAttribute("data-v") || "0", 10);
      tEl.setAttribute("data-v", total);
      var t0 = null;
      var anim = function (t) { if (!t0) t0 = t; var p = Math.min((t - t0) / 500, 1); tEl.textContent = money(Math.round(from + (total - from) * (1 - Math.pow(1 - p, 3)))); if (p < 1) requestAnimationFrame(anim); };
      requestAnimationFrame(anim);
      $("#est-lines", est).innerHTML = lines.map(function (l) { return "<li><span>" + l[0] + "</span><b>" + money(l[1]) + "</b></li>"; }).join("");
      $("#est-deposit", est).textContent = money(Math.round(total / 2));
    };
    $$("input", est).forEach(function (el) { el.addEventListener("input", estRender); el.addEventListener("change", estRender); });
    estRender();
  }
})();
