/* Wind Chill & Heat Index Calculator (NWS formulas) */
(function () {
  "use strict";
  var $ = AO.$;
  function heatIndex(T, R) {
    var hi = 0.5 * (T + 61 + (T - 68) * 1.2 + R * 0.094);
    if ((hi + T) / 2 < 80) return hi;
    hi = -42.379 + 2.04901523 * T + 10.14333127 * R - 0.22475541 * T * R - 0.00683783 * T * T - 0.05481717 * R * R +
      0.00122874 * T * T * R + 0.00085282 * T * R * R - 0.00000199 * T * T * R * R;
    if (R < 13 && T >= 80 && T <= 112) hi -= ((13 - R) / 4) * Math.sqrt((17 - Math.abs(T - 95)) / 17);
    if (R > 85 && T >= 80 && T <= 87) hi += ((R - 85) / 10) * ((87 - T) / 5);
    return hi;
  }
  function windChill(T, V) { return 35.74 + 0.6215 * T - 35.75 * Math.pow(V, 0.16) + 0.4275 * T * Math.pow(V, 0.16); }
  function calc() {
    var T = AO.num("#t"), R = Math.min(100, Math.max(0, AO.num("#rh"))), V = Math.max(0, AO.num("#v"));
    var html, f, risk, cls;
    if (T <= 50 && V > 3) {
      f = windChill(T, V);
      if (f <= -48) { risk = "Frostbite on exposed skin in about 5 minutes or less. Dangerous — postpone or turn back."; cls = "warn"; }
      else if (f <= -32) { risk = "Frostbite possible in about 10 minutes. Cover all skin; limit time exposed."; cls = "warn"; }
      else if (f <= -18) { risk = "Frostbite possible in about 30 minutes on exposed skin."; cls = "warn"; }
      else if (f <= 15) { risk = "Very cold. Wind layer, insulated gloves and a hat; watch for numb fingers and toes."; cls = "tip"; }
      else { risk = "Cool to cold. Wind matters more than the thermometer suggests — carry a windproof shell."; cls = "tip"; }
      html = "<div class='result-big'>" + Math.round(f) + "°F</div><p class='result-sub'>Wind chill at " + T + "°F with " + V + " mph wind</p>";
    } else if (T >= 80) {
      f = heatIndex(T, R);
      if (f >= 125) { risk = "Extreme danger: heat stroke is likely with exertion. Don't hike."; cls = "warn"; }
      else if (f >= 103) { risk = "Danger: heat exhaustion and heat stroke are likely with prolonged exertion. Hike only at dawn, in shade, with plenty of water and electrolytes."; cls = "warn"; }
      else if (f >= 90) { risk = "Extreme caution: heat cramps and heat exhaustion possible. Start early, slow down, rest in shade."; cls = "warn"; }
      else { risk = "Caution: fatigue is possible with prolonged activity. Drink regularly."; cls = "tip"; }
      html = "<div class='result-big'>" + Math.round(f) + "°F</div><p class='result-sub'>Heat index at " + T + "°F and " + R + "% humidity (in shade — full sun can add up to 15°F)</p>";
    } else {
      html = "<div class='result-big'>" + T + "°F</div><p class='result-sub'>Feels like the air temperature — wind chill applies at 50°F and below with wind over 3 mph, heat index at 80°F and above.</p>";
      risk = "Comfortable range for most hiking. Layers still matter: temperatures drop about 3–5°F per 1,000 ft you climb."; cls = "tip";
    }
    html += "<div class='callout " + cls + "'>" + risk + "</div>";
    $("#result").innerHTML = html;
  }
  $("#feelform").addEventListener("input", calc);
  calc();
})();
