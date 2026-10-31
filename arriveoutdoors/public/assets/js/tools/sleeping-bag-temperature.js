/* Sleeping Bag & Pad Temperature Guide */
(function () {
  "use strict";
  var $ = AO.$;
  function pad(low, shelter) {
    var r = low >= 50 ? 2 : low >= 35 ? 3 : low >= 20 ? 4 : low >= 5 ? 5 : low >= -10 ? 6 : 7;
    if (shelter === "car") r = Math.max(2, r - 1);
    return r;
  }
  function calc() {
    var low = AO.num("#low"), sleeper = AO.radio("sleeper") || "average", shelter = AO.radio("shelter") || "tent";
    var margin = { warm: 0, average: 5, cold: 12 }[sleeper];
    if (AO.$("#wind").checked) margin += 5;
    if (AO.$("#damp").checked) margin += 3;
    var comfort = Math.floor((low - margin) / 5) * 5;
    var limit = comfort - 10;
    var r = pad(low, shelter);
    var cls = comfort >= 50 ? "Summer bag" : comfort >= 30 ? "3-season bag" : comfort >= 10 ? "Cold-weather 3-season bag" : "Winter bag";
    var html = "<div class='result-big'>" + comfort + "°F</div><p class='result-sub'>Look for a bag with an ISO/EN <strong>comfort</strong> rating of " + comfort + "°F or lower (" + cls + ")</p>" +
      "<ul class='result-list'><li><span>Matching lower-limit rating (often the number on the label)</span><span>" + limit + "°F or lower</span></li>" +
      "<li><span>" + (shelter === "hammock" ? "Underquilt rating" : "Sleeping pad R-value") + "</span><span>" + (shelter === "hammock" ? comfort + "°F underquilt" : "R " + r + "+") + "</span></li>" +
      "<li><span>Expected overnight low</span><span>" + low + "°F</span></li></ul>";
    var tips = [];
    if (shelter !== "hammock" && r >= 5) tips.push("Stack pads: R-values add up, so a closed-cell foam pad (about R 2) under an inflatable gets you there without a new pad.");
    if (shelter === "hammock") tips.push("In a hammock your bag's insulation is crushed underneath you. An underquilt (or a pad inside the hammock) does the job a ground pad does in a tent.");
    if (low <= 32) tips.push("Below freezing: sleep with tomorrow's water bottle and phone inside your bag, and vent the tent to cut condensation.");
    tips.push("A bag's limit rating is where a warm sleeper stays safe curled up — not comfortable. Buy by the comfort rating if you tend to sleep cold.");
    html += tips.map(function (t) { return "<div class='callout tip'>" + t + "</div>"; }).join("");
    $("#result").innerHTML = html;
  }
  $("#bagform").addEventListener("input", calc);
  $("#bagform").addEventListener("change", calc);
  calc();
})();
