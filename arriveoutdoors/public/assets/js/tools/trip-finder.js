/* Trip Finder: rank parks by distance from the visitor + this month's weather score. */
(function () {
  "use strict";
  var $ = AO.$, $$ = AO.$$;
  var D = window.AO_TRIPS || [];
  var MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var origin = AO.store.get("tripOrigin", null);
  var status = $("#loc-status");

  function miles(a, b, c, d) {
    var R = 3958.8, r = Math.PI / 180, dl = (c - a) * r, dn = (d - b) * r;
    var x = Math.sin(dl / 2) * Math.sin(dl / 2) + Math.cos(a * r) * Math.cos(c * r) * Math.sin(dn / 2) * Math.sin(dn / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  // Straight-line miles → rough driving time: roads run ~25% longer than the crow flies, ~58 mph average.
  function driveHours(mi) { return (mi * 1.25) / 58; }
  function hrs(h) { if (h < 1) return Math.max(10, Math.round(h * 60 / 10) * 10) + " min"; return (Math.round(h * 2) / 2).toString().replace(".5", "½") + " hr"; }
  function col(s) { return s >= 75 ? "#23784a" : s >= 60 ? "#677516" : s >= 45 ? "#a3640b" : "#b8412a"; }
  function word(s) { return s >= 75 ? "Excellent" : s >= 60 ? "Good" : s >= 45 ? "Fair" : "Poor"; }

  function setOrigin(o) {
    origin = o; AO.store.set("tripOrigin", o);
    $("#origin-label").textContent = o.name;
    $("#origin-box").hidden = false;
    render();
  }

  // ---- location: browser geolocation ----
  $("#use-loc").addEventListener("click", function () {
    if (!navigator.geolocation) { status.textContent = "Location isn't available in this browser — enter an address or town instead."; $("#addr").focus(); return; }
    status.textContent = "Asking your browser for your location…";
    navigator.geolocation.getCurrentPosition(function (p) {
      status.textContent = "";
      var o = { name: "Your current location", lat: p.coords.latitude, lon: p.coords.longitude };
      setOrigin(o);
      reverse(o);
    }, function (err) {
      status.innerHTML = (err.code === 1 ? "Location permission was declined." : "Couldn't get your location.") + " No problem — <strong>type an address, town or ZIP code</strong> below.";
      $("#addr").focus();
    }, { timeout: 12000, maximumAge: 600000 });
  });
  // Friendly label for the coordinates (one request, OpenStreetMap Nominatim)
  function reverse(o) {
    fetch("https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=10&lat=" + o.lat + "&lon=" + o.lon, { headers: { "Accept-Language": "en" } })
      .then(function (r) { return r.json(); }).then(function (j) {
        var a = j.address || {}, n = [a.city || a.town || a.village || a.county, a.state].filter(Boolean).join(", ");
        if (n) { o.name = "Near " + n; AO.store.set("tripOrigin", o); $("#origin-label").textContent = o.name; }
      }).catch(function () {});
  }

  // ---- location: typed address (geocoded on submit only) ----
  $("#addr-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var q = $("#addr").value.trim();
    if (q.length < 2) return;
    status.textContent = "Looking up “" + q + "”…";
    var u = "https://nominatim.openstreetmap.org/search?format=jsonv2&limit=5&countrycodes=us,ca&q=" + encodeURIComponent(q);
    fetch(u, { headers: { "Accept-Language": "en" } }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (res) {
      if (!res.length) throw 0;
      if (res.length === 1) { pick(res[0]); return; }
      status.innerHTML = "Which one? " + res.map(function (r, i) { return "<button type='button' class='chip' style='cursor:pointer' data-i='" + i + "'>" + AO.esc(r.display_name.split(", ").slice(0, 3).join(", ")) + "</button>"; }).join(" ");
      $$("#loc-status button").forEach(function (b) { b.addEventListener("click", function () { pick(res[+b.dataset.i]); }); });
    }).catch(function () {
      // Fallback: Open-Meteo place-name search
      AO.geocode(q).then(function (r) {
        if (!r.length) { status.textContent = "Couldn't find that place. Try a town and state, like “Denver, CO”, or a ZIP code."; return; }
        status.textContent = "";
        setOrigin({ name: AO.placeLabel(r[0]), lat: r[0].latitude, lon: r[0].longitude });
      }).catch(function () { status.textContent = "Address search isn't responding right now. Try again in a moment."; });
    });
    function pick(r) { status.textContent = ""; setOrigin({ name: r.display_name.split(", ").slice(0, 3).join(", "), lat: +r.lat, lon: +r.lon }); }
  });
  $("#change-loc").addEventListener("click", function () { $("#origin-box").hidden = true; $("#addr").focus(); });

  // ---- ranking ----
  function render() {
    var out = $("#result");
    var m = +$("#month").value, max = +(AO.radio("drive") || 8), pref = AO.radio("pref") || "balanced";
    if (!origin) {
      out.innerHTML = "<div class='tf-empty'><div class='tf-compass' aria-hidden='true'>🧭</div><h2>Where are you starting from?</h2><p>Share your location or type an address, town or ZIP code, and we'll rank parks by drive time and " + MON[m] + " weather.</p></div>";
      return;
    }
    var w = { weather: 1.2, balanced: 4, close: 9 }[pref];
    var rows = D.map(function (d) {
      var mi = miles(origin.lat, origin.lon, d.lat, d.lon), h = driveHours(mi), s = d.sc[m];
      return { d: d, mi: mi, h: h, s: s, rank: s - h * w };
    });
    var within = rows.filter(function (r) { return max >= 99 || r.h <= max; });
    var good = within.filter(function (r) { return r.s >= 45; }).sort(function (a, b) { return b.rank - a.rank; });
    var html = "<div class='tf-head'><div><span class='kicker'>Best bets for " + MON[m] + "</span><h2>" +
      (good.length ? good.length + " park" + (good.length === 1 ? "" : "s") + (max >= 99 ? "" : " within ~" + max + " hours") : "Nothing great within ~" + max + " hours") + "</h2>" +
      "<p class='muted'>From " + AO.esc(origin.name) + ". Drive times are rough straight-line estimates — check a map before you go.</p></div></div>";
    var list = good.slice(0, 9);
    if (!list.length) {
      var near = rows.slice().sort(function (a, b) { return a.h - b.h; }).slice(0, 3);
      var bestFar = rows.filter(function (r) { return r.s >= 60; }).sort(function (a, b) { return a.h - b.h; }).slice(0, 3);
      html += "<p>Parks closest to you have poor weather in " + MON[m] + ", or none are in range. Two options:</p>";
      html += "<h3>Closest to you</h3><div class='tf-grid'>" + near.map(card).join("") + "</div>";
      if (bestFar.length) html += "<h3>Nearest with good " + MON[m] + " weather</h3><div class='tf-grid'>" + bestFar.map(card).join("") + "</div>";
    } else {
      html += "<div class='tf-grid'>" + list.map(card).join("") + "</div>";
      var skipped = within.filter(function (r) { return r.s < 45; }).sort(function (a, b) { return a.h - b.h; }).slice(0, 4);
      if (skipped.length) html += "<p class='small muted' style='margin-top:18px'>Also in range but rough in " + MON[m] + ": " + skipped.map(function (r) { return "<a href='/destinations/" + r.d.slug + "/'>" + AO.esc(r.d.short) + "</a> (" + word(r.s).toLowerCase() + ", " + r.d.hi[m] + "°/" + r.d.lo[m] + "°F)"; }).join(", ") + ".</p>";
    }
    out.innerHTML = html;
    var u = new URLSearchParams({ m: m, drive: max, pref: pref }); history.replaceState(null, "", "?" + u);
  }
  function card(r) {
    var d = r.d, m = +$("#month").value;
    var dir = "https://www.google.com/maps/dir/?api=1&origin=" + origin.lat.toFixed(4) + "," + origin.lon.toFixed(4) + "&destination=" + d.lat + "," + d.lon;
    return "<article class='tf-card'>" + (d.p ? "<img src='" + d.p + "' alt='' loading='lazy'>" : "") +
      "<div class='tf-body'><span class='score-pill' style='background:" + col(r.s) + "'>" + r.s + " · " + word(r.s) + "</span>" +
      "<h3><a href='/destinations/" + d.slug + "/'>" + AO.esc(d.name) + "</a></h3>" +
      "<div class='tf-meta'><span>🚗 ~" + hrs(r.h) + " · " + Math.round(r.mi * 1.25).toLocaleString() + " mi</span><span>🌡️ " + d.hi[m] + "° / " + d.lo[m] + "°F</span><span>💧 " + d.wet[m] + " wet days</span></div>" +
      "<div class='tf-links'><a href='/destinations/" + d.slug + "/'>Guide</a><a href='/tools/trail-weather/?lat=" + d.lat + "&lon=" + d.lon + "&name=" + encodeURIComponent(d.name) + "'>7-day forecast</a><a href='" + dir + "' target='_blank' rel='noopener'>Directions</a></div></div></article>";
  }

  // ---- init ----
  var q = new URLSearchParams(location.search), now = new Date().getMonth();
  $("#month").value = q.get("m") != null ? q.get("m") : now;
  if (q.get("drive")) { var r = $('input[name=drive][value="' + q.get("drive") + '"]'); if (r) r.checked = true; }
  if (q.get("pref")) { var p = $('input[name=pref][value="' + q.get("pref") + '"]'); if (p) p.checked = true; }
  $("#tf-opts").addEventListener("change", render);
  if (origin) { $("#origin-label").textContent = origin.name; $("#origin-box").hidden = false; }
  render();
})();
