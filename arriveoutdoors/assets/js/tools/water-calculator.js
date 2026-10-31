/* Hiking Water Calculator */
(function () {
  "use strict";
  var $ = AO.$;
  var BASE = { easy: 0.4, moderate: 0.6, hard: 0.85 }; // liters per hour at ~70°F for a 154 lb adult
  function calc() {
    var hours = AO.num("#hours"), temp = AO.num("#temp"), wt = AO.num("#weight") || 154;
    var effort = AO.radio("effort") || "moderate", humid = $("#humid").checked, alt = $("#alt").checked;
    var r = BASE[effort];
    if (temp > 70) r *= 1 + (temp - 70) * 0.03; else r *= Math.max(0.6, 1 - (70 - temp) * 0.01);
    r *= Math.min(1.4, Math.max(0.75, wt / 154));
    if (humid && temp > 75) r *= 1.1;
    if (alt) r *= 1.1;
    r = Math.max(0.25, r);
    var total = r * hours, oz = total * 33.814, lb = total * 2.2046;
    var src = AO.num("#sources");
    var carry = src > 0 ? total / (src + 1) : total;
    var html = "<div class='result-big'>" + total.toFixed(1) + " L</div><p class='result-sub'>(" + Math.round(oz) + " fl oz) for the whole hike — about " + r.toFixed(2) + " L per hour</p>" +
      "<ul class='result-list'><li><span>Water weight if you carry it all</span><span>" + lb.toFixed(1) + " lb</span></li>" +
      "<li><span>Carry between refills (" + src + " reliable source" + (src === 1 ? "" : "s") + ")</span><span>" + carry.toFixed(1) + " L</span></li>" +
      "<li><span>Drink about every 20 minutes</span><span>" + Math.round(r * 33.814 / 3) + " oz</span></li></ul>";
    var tips = [];
    if (hours >= 2 && (temp >= 80 || effort === "hard")) tips.push("Over two hours of hot or hard hiking, add electrolytes (sodium) — water alone can't replace what you sweat out.");
    if (temp >= 90) tips.push("In 90°F+ heat, plan to be off exposed trail by late morning and carry at least 1 L more than this estimate.");
    if (src > 0) tips.push("Only count a source if it's reliable this season, and bring a filter or purifier.");
    tips.push("This is an estimate. Sweat rates vary a lot between people — weigh yourself before and after a long hike to learn yours.");
    html += tips.map(function (t, i) { return "<div class='callout " + (i === tips.length - 1 ? "tip" : "warn") + "'>" + t + "</div>"; }).join("");
    $("#result").innerHTML = html;
  }
  $("#waterform").addEventListener("input", calc);
  $("#waterform").addEventListener("change", calc);
  calc();
})();
