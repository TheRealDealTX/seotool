/* Sunrise, Sunset & Daylight Calculator */
(function () {
  "use strict";
  var $ = AO.$, place = null;
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  function dur(a, b) { var m = Math.round((b - a) / 60000); return Math.floor(m / 60) + " h " + (m % 60) + " min"; }
  function calc() {
    if (!place) { $("#result").innerHTML = "<p class='result-sub'>Search for a trailhead, park or town (or use your location) to see sunrise, sunset and golden hour.</p>"; return; }
    var d = $("#date").value ? new Date($("#date").value + "T12:00:00") : new Date();
    var s = AO.sunTimes(d, place.lat, place.lon), tz = place.tz;
    var html = "<h2 style='margin:0'>" + AO.esc(place.name) + "</h2><p class='result-sub'>" + d.toLocaleDateString([], { weekday: "long", month: "long", day: "numeric", year: "numeric" }) + (tz ? " · times in " + AO.esc(tz) : " · times in your device's time zone") + "</p>";
    if (s.polar) {
      html += "<div class='result-big'>" + (s.polar === "day" ? "Midnight sun" : "Polar night") + "</div>";
    } else {
      html += "<div class='row'><div><span class='small muted'>SUNRISE</span><div class='result-big'>" + AO.fmtTime(s.sunrise, tz) + "</div></div>" +
        "<div><span class='small muted'>SUNSET</span><div class='result-big'>" + AO.fmtTime(s.sunset, tz) + "</div></div></div>" +
        "<ul class='result-list'><li><span>First light (civil dawn)</span><span>" + AO.fmtTime(s.civilDawn, tz) + "</span></li>" +
        "<li><span>Morning golden hour</span><span>" + AO.fmtTime(s.sunrise, tz) + " – " + AO.fmtTime(s.goldenAMEnd, tz) + "</span></li>" +
        "<li><span>Solar noon</span><span>" + AO.fmtTime(s.noon, tz) + "</span></li>" +
        "<li><span>Evening golden hour</span><span>" + AO.fmtTime(s.goldenPMStart, tz) + " – " + AO.fmtTime(s.sunset, tz) + "</span></li>" +
        "<li><span>Last light (civil dusk)</span><span>" + AO.fmtTime(s.civilDusk, tz) + "</span></li>" +
        "<li><span>Daylight</span><span>" + dur(s.sunrise, s.sunset) + "</span></li>" +
        "<li><span>Usable light (dawn to dusk)</span><span>" + dur(s.civilDawn, s.civilDusk) + "</span></li></ul>";
    }
    // Year view: daylight on the 15th of each month
    var rows = "", y = d.getFullYear();
    for (var m = 0; m < 12; m++) {
      var t = AO.sunTimes(new Date(y, m, 15, 12), place.lat, place.lon);
      rows += "<tr><td>" + MONTHS[m] + " 15</td><td>" + (t.sunrise ? AO.fmtTime(t.sunrise, tz) : "—") + "</td><td>" + (t.sunset ? AO.fmtTime(t.sunset, tz) : "—") + "</td><td>" + (t.sunrise ? dur(t.sunrise, t.sunset) : (t.polar === "day" ? "24 h" : "0 h")) + "</td></tr>";
    }
    html += "<h3>Daylight through the year</h3><div class='table-wrap'><table><thead><tr><th>Date</th><th>Sunrise</th><th>Sunset</th><th>Daylight</th></tr></thead><tbody>" + rows + "</tbody></table></div>" +
      "<p class='small muted'>Calculated with the NOAA solar equations for sea level; in deep canyons and on west-facing slopes the sun disappears earlier than the official sunset.</p>";
    $("#result").innerHTML = html;
  }
  AO.placePicker($("#place"), function (p) { place = p; calc(); });
  $("#locate").addEventListener("click", function () {
    AO.locateMe(function (p) { p.tz = Intl.DateTimeFormat().resolvedOptions().timeZone; place = p; calc(); }, $("#status"));
  });
  $("#date").valueAsDate = new Date();
  $("#date").addEventListener("change", calc);
  calc();
})();
