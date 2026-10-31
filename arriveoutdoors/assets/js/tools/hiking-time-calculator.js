/* Hiking Time Calculator */
(function () {
  "use strict";
  var $ = AO.$;
  var PACE = { // flat speed (mph), climb rate (ft per added hour)
    easy: [2.0, 1000], moderate: [2.5, 1500], fast: [3.0, 2000]
  };
  var place = null;
  function hm(h) { var m = Math.round(h * 60); return Math.floor(m / 60) + " h " + (m % 60) + " min"; }
  function addH(base, h) { return new Date(base.getTime() + h * 3600000); }
  function calc() {
    var dist = AO.num("#dist"), gain = AO.num("#gain"), loss = AO.num("#loss");
    var pace = PACE[AO.radio("pace") || "moderate"], pack = parseFloat(AO.radio("pack") || "1");
    var brk = AO.num("#breaks");
    var flat = dist / pace[0];
    var climb = gain / pace[1];
    var desc = Math.max(0, loss - 1500) / 3000; // steep descents slow most people a little
    var moving = (flat + climb + desc) * pack;
    var total = moving * (1 + brk / 60);
    var res = "<div class='result-big'>" + hm(total) + "</div><p class='result-sub'>Total time with breaks (" + hm(moving) + " moving)</p><ul class='result-list'>" +
      "<li><span>Flat-ground walking</span><span>" + hm(flat * pack) + "</span></li>" +
      "<li><span>Added for " + gain.toLocaleString() + " ft of climbing</span><span>" + hm(climb * pack) + "</span></li>" +
      (desc > 0 ? "<li><span>Added for steep descent</span><span>" + hm(desc * pack) + "</span></li>" : "") +
      "<li><span>Breaks (" + brk + " min per hour)</span><span>" + hm(total - moving) + "</span></li>" +
      "<li><span>Average overall pace</span><span>" + (dist / total).toFixed(1) + " mph</span></li></ul>";
    var st = $("#start").value;
    if (st) {
      var d = $("#date").value ? new Date($("#date").value + "T00:00:00") : new Date();
      var parts = st.split(":"), start = new Date(d); start.setHours(+parts[0], +parts[1], 0, 0);
      var finish = addH(start, total), turn = addH(start, total / 2);
      res += "<ul class='result-list'><li><span>Finish time</span><span>" + AO.fmtTime(finish) + "</span></li>" +
        "<li><span>Turnaround time (out-and-back)</span><span>" + AO.fmtTime(turn) + "</span></li>";
      if (place) {
        var s = AO.sunTimes(d, place.lat, place.lon);
        if (s.sunset) {
          var latest = addH(s.sunset, -total - 0.5);
          var ok = finish <= addH(s.sunset, -0.5);
          res += "<li><span>Sunset at " + AO.esc(place.name) + "</span><span>" + AO.fmtTime(s.sunset, place.tz) + "</span></li>" +
            "<li><span>Latest start to finish 30 min before sunset</span><span>" + AO.fmtTime(latest, place.tz) + "</span></li></ul>" +
            "<div class='callout " + (ok ? "tip'><strong>On track:</strong> you should finish with daylight to spare." : "warn'><strong>Daylight:</strong> at this pace you'd finish after dark. Start earlier, shorten the route, or carry a headlamp you trust.") + "</div>";
        } else res += "</ul>";
      } else res += "</ul><p class='small muted'>Add a trailhead location to check your finish against sunset.</p>";
    }
    $("#result").innerHTML = res;
  }
  AO.placePicker($("#place"), function (p) { place = p; calc(); });
  $("#hikeform").addEventListener("input", calc);
  $("#hikeform").addEventListener("change", calc);
  calc();
})();
