/* Backpack Size & Torso Fit Calculator */
(function () {
  "use strict";
  var $ = AO.$;
  function torsoSize(t) {
    if (t < 15) return ["Extra small", "XS"];
    if (t < 17) return ["Small", "S"];
    if (t < 19.5) return ["Medium", "M"];
    if (t < 21.5) return ["Large", "L"];
    return ["Extra large", "XL"];
  }
  function hipSize(h) {
    if (!h) return null;
    if (h < 28) return "XS hipbelt (roughly under 28 in)";
    if (h < 32) return "S hipbelt (roughly 26–32 in)";
    if (h < 38) return "M hipbelt (roughly 30–38 in)";
    if (h < 44) return "L hipbelt (roughly 36–44 in)";
    return "XL hipbelt or a pack with interchangeable belts";
  }
  function capacity(trip, nights, style) {
    var ranges = {
      day: [[18, 30], "Day hikes: water, layers, food, first aid and the Ten Essentials."],
      short: [[35, 50], "1–3 nights with modern compact gear."],
      multi: [[50, 65], "3–5 nights, or shorter trips with a bear canister or winter layers."],
      long: [[65, 80], "Week-long trips, winter camping, or carrying shared gear for kids."]
    };
    var k = trip === "day" ? "day" : nights <= 3 ? "short" : nights <= 5 ? "multi" : "long";
    var r = ranges[k][0].slice();
    if (style === "ul" && k !== "day") { r[0] -= 10; r[1] -= 10; }
    if (style === "bulky" && k !== "day") { r[0] += 5; r[1] += 10; }
    return [r, ranges[k][1]];
  }
  function calc() {
    var t = AO.num("#torso"), h = AO.num("#hips"), trip = AO.radio("trip") || "overnight";
    var nights = AO.num("#nights"), style = AO.radio("style") || "std";
    $("#nights-row").style.display = trip === "day" ? "none" : "";
    var html = "";
    if (t > 0) {
      var s = torsoSize(t);
      html += "<div class='result-big'>" + s[0] + " (" + s[1] + ")</div><p class='result-sub'>Pack size for a " + t + "-inch torso. Sizing varies by brand — check the maker's chart, and choose an adjustable harness if you're between sizes.</p>";
    } else html += "<p class='result-sub'>Enter your torso length to get a pack size.</p>";
    var c = capacity(trip, nights, style);
    html += "<ul class='result-list'><li><span>Recommended capacity</span><span>" + c[0][0] + "–" + c[0][1] + " L</span></li>";
    var hs = hipSize(h);
    if (hs) html += "<li><span>Hipbelt</span><span>" + hs + "</span></li>";
    html += "</ul><p class='small muted'>" + c[1] + "</p>";
    html += "<div class='callout tip'><strong>Fit check:</strong> with the pack loaded, the hipbelt's padding should sit centered on your hip bones (iliac crest), shoulder straps should wrap over your shoulders with no gap, and load lifters should angle back at roughly 45°.</div>";
    $("#result").innerHTML = html;
  }
  $("#packsizeform").addEventListener("input", calc);
  $("#packsizeform").addEventListener("change", calc);
  calc();
})();
