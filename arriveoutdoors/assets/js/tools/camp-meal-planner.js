/* Camp Meal & Food Weight Planner */
(function () {
  "use strict";
  var $ = AO.$;
  var CAL = { car: 2300, backpack: 3000, hard: 3800 };      // per average adult per day
  var DENSITY = { car: 70, backpack: 110, hard: 125 };     // calories per ounce, realistic mix
  var PLAN = {
    car: [["Breakfast", 0.22, "Eggs, bacon or sausage, tortillas, coffee"], ["Lunch", 0.25, "Sandwiches or wraps, fruit, chips"], ["Snacks", 0.15, "Trail mix, cheese, jerky"], ["Dinner", 0.30, "Foil-packet meals, chili, pasta, burgers"], ["Dessert", 0.08, "S'mores, cookies"]],
    backpack: [["Breakfast", 0.20, "Granola with powdered milk, or instant oatmeal + nut butter packet; instant coffee"], ["Lunch", 0.22, "Tortillas, hard cheese, salami or tuna packets"], ["Snacks", 0.28, "Trail mix, bars, dried fruit, chocolate — eat every 1–2 hours"], ["Dinner", 0.25, "Freeze-dried meal, or ramen/couscous + olive oil + protein"], ["Dessert", 0.05, "Hot cocoa, cookies"]],
    hard: [["Breakfast", 0.20, "Double oatmeal with nut butter and olive oil; coffee"], ["Lunch", 0.20, "Tortillas, peanut butter, cheese, salami"], ["Snacks", 0.32, "Bars, nuts, chocolate, chips — 250–300 cal per hour on the move"], ["Dinner", 0.24, "Large freeze-dried meal plus olive oil packet"], ["Dessert", 0.04, "Cocoa, candy"]]
  };
  function calc() {
    var people = Math.max(1, AO.num("#people")), days = Math.max(1, AO.num("#days")), type = AO.radio("style") || "backpack";
    var cold = $("#cold").checked, big = AO.num("#size");
    var perDay = CAL[type] * (1 + (big - 1) * 0.15) * (cold ? 1.15 : 1);
    var total = perDay * people * days, oz = total / DENSITY[type];
    var html = "<div class='result-big'>" + Math.round(perDay).toLocaleString() + " cal</div><p class='result-sub'>per person per day · " + Math.round(total).toLocaleString() + " calories for the group</p>" +
      "<ul class='result-list'><li><span>Food weight per person per day</span><span>" + (perDay / DENSITY[type] / 16).toFixed(2) + " lb</span></li>" +
      "<li><span>Total food weight</span><span>" + (oz / 16).toFixed(1) + " lb</span></li>" +
      "<li><span>Target calorie density</span><span>" + DENSITY[type] + "+ cal/oz</span></li></ul>" +
      "<h3>Daily plan per person</h3><div class='table-wrap'><table><thead><tr><th>Meal</th><th>Calories</th><th>Ideas</th></tr></thead><tbody>";
    PLAN[type].forEach(function (m) { html += "<tr><td><strong>" + m[0] + "</strong></td><td>" + Math.round(perDay * m[1] / 10) * 10 + "</td><td>" + m[2] + "</td></tr>"; });
    html += "</tbody></table></div>";
    if (type !== "car") html += "<div class='callout tip'><strong>Lighten it:</strong> olive oil (about 240 cal/oz), nut butter and nuts (160–190 cal/oz) are the densest foods you can carry. Repackage everything into zip bags and leave boxes at home.</div>";
    if (days > 4 && type !== "car") html += "<div class='callout tip'>Over four or more days, plan a resupply or cache — carrying more than about 8 lb of food each makes packs heavy fast.</div>";
    $("#result").innerHTML = html;
  }
  $("#mealform").addEventListener("input", calc);
  $("#mealform").addEventListener("change", calc);
  calc();
})();
