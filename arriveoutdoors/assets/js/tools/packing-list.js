/* Packing List Generator */
(function () {
  "use strict";
  var $ = AO.$, $$ = AO.$$;
  // t: trip types (car, backpack, day); s: seasons (warm, shoulder, cold); x: extra flag required
  // q(o): quantity text; l: helpful link
  var ALL = ["car", "backpack", "day"], OVN = ["car", "backpack"];
  var ITEMS = [
    // Shelter & sleep
    { c: "Shelter & sleep", n: "Tent with stakes, poles and footprint", t: OVN, q: function (o) { return o.people <= 2 ? "1 (2-person)" : o.people <= 4 ? "1 (4-person) or 2 small" : Math.ceil(o.people / 4) + " tents"; } },
    { c: "Shelter & sleep", n: "Extra guylines and 2–4 spare stakes", t: OVN, s: ["shoulder", "cold"] },
    { c: "Shelter & sleep", n: "Sleeping bag or quilt rated 10°F below expected low", t: OVN, q: function (o) { return o.people + ""; }, l: "/tools/sleeping-bag-temperature/" },
    { c: "Shelter & sleep", n: "Sleeping pad (R-value 2+ summer, 4+ shoulder, 5+ winter)", t: OVN, q: function (o) { return o.people + ""; }, l: "/tools/sleeping-bag-temperature/" },
    { c: "Shelter & sleep", n: "Second closed-cell foam pad for under your inflatable", t: OVN, s: ["cold"] },
    { c: "Shelter & sleep", n: "Pillow (or stuff sack filled with clothes)", t: OVN },
    { c: "Shelter & sleep", n: "Tarp or canopy for shade and rain", t: ["car"] },
    { c: "Shelter & sleep", n: "Camp chairs", t: ["car"], q: function (o) { return o.people + ""; } },
    { c: "Shelter & sleep", n: "Camp table (if the site has none)", t: ["car"] },
    { c: "Shelter & sleep", n: "Emergency bivy or space blanket", t: ["day"] },
    // Kitchen
    { c: "Kitchen & water", n: "Stove and fuel", t: OVN, q: function (o) { return o.trip === "backpack" ? "1 canister per ~2–3 people per 3 days" : "2-burner + 1 lb propane per day"; } },
    { c: "Kitchen & water", n: "Lighter + backup matches in a zip bag", t: OVN },
    { c: "Kitchen & water", n: "Pot (and pan for car camping)", t: OVN },
    { c: "Kitchen & water", n: "Mug, bowl and long spoon each", t: OVN, q: function (o) { return o.people + " sets"; } },
    { c: "Kitchen & water", n: "Cooler with ice or ice packs", t: ["car"] },
    { c: "Kitchen & water", n: "Cutting board, knife, spatula, tongs", t: ["car"] },
    { c: "Kitchen & water", n: "Biodegradable soap, sponge, small wash basin", t: OVN },
    { c: "Kitchen & water", n: "Trash bags — pack out everything", t: ALL },
    { c: "Kitchen & water", n: "Food (meals + snacks)", t: OVN, q: function (o) { return Math.ceil(o.nights + 1) + " days × " + o.people + " people (~" + (o.trip === "backpack" ? (1.75 * (o.nights + 1) * o.people).toFixed(1) + " lb" : "plan by meal") + ")"; }, l: "/tools/camp-meal-planner/" },
    { c: "Kitchen & water", n: "Trail snacks", t: ["day"], q: function (o) { return "200–300 calories per hour per person"; } },
    { c: "Kitchen & water", n: "Water bottles or reservoir", t: ALL, q: function (o) { return o.trip === "day" ? "2–3 L per person" : "3–4 L capacity per person"; }, l: "/tools/water-calculator/" },
    { c: "Kitchen & water", n: "Water filter or purifier + backup tablets", t: ["backpack", "day"], l: "/sawyer-squeeze-gravity-setup/" },
    { c: "Kitchen & water", n: "Water jug (5–7 gal) if the site has no tap", t: ["car"] },
    { c: "Kitchen & water", n: "Bear canister or bear bag + 50 ft cord", t: ["backpack"], x: "bear" },
    { c: "Kitchen & water", n: "Bear-proof storage plan (locker or car, never the tent)", t: ["car"], x: "bear" },
    // Clothing
    { c: "Clothing", n: "Moisture-wicking base layer top", t: ALL, q: function (o) { return o.trip === "day" ? "1" : "1–2"; } },
    { c: "Clothing", n: "Hiking pants or shorts", t: ALL },
    { c: "Clothing", n: "Sun hoodie or long-sleeve sun shirt", t: ALL, s: ["warm", "shoulder"], l: "/best-sun-hoodies-for-hiking/" },
    { c: "Clothing", n: "Insulating mid layer (fleece or light puffy)", t: ALL },
    { c: "Clothing", n: "Warm insulated jacket", t: ALL, s: ["shoulder", "cold"] },
    { c: "Clothing", n: "Rain jacket", t: ALL },
    { c: "Clothing", n: "Rain pants", t: ALL, s: ["shoulder", "cold"] },
    { c: "Clothing", n: "Thermal base layer bottoms (for sleeping)", t: OVN, s: ["shoulder", "cold"] },
    { c: "Clothing", n: "Hiking socks", t: ALL, q: function (o) { return o.trip === "day" ? "1 + spare pair" : Math.min(o.nights + 1, 4) + " pairs"; } },
    { c: "Clothing", n: "Underwear", t: OVN, q: function (o) { return Math.min(o.nights + 1, 4) + ""; } },
    { c: "Clothing", n: "Sun hat", t: ALL, s: ["warm", "shoulder"] },
    { c: "Clothing", n: "Warm beanie and gloves", t: ALL, s: ["shoulder", "cold"] },
    { c: "Clothing", n: "Insulated pants or puffy booties for camp", t: OVN, s: ["cold"] },
    { c: "Clothing", n: "Hiking boots or trail shoes (broken in)", t: ALL },
    { c: "Clothing", n: "Camp shoes or sandals", t: OVN },
    { c: "Clothing", n: "Microspikes or traction devices", t: ALL, s: ["cold"] },
    { c: "Clothing", n: "Gaiters", t: ["backpack", "day"], s: ["cold"] },
    // Navigation & safety (Ten Essentials)
    { c: "Navigation & safety", n: "Map (paper) and compass", t: ["backpack", "day"] },
    { c: "Navigation & safety", n: "Phone with offline maps downloaded + battery bank", t: ALL },
    { c: "Navigation & safety", n: "Headlamp + spare batteries", t: ALL, q: function (o) { return o.people + ""; } },
    { c: "Navigation & safety", n: "First-aid kit (blister care, meds, tape, gauze)", t: ALL },
    { c: "Navigation & safety", n: "Knife or multi-tool", t: ALL },
    { c: "Navigation & safety", n: "Whistle", t: ["backpack", "day"], l: "/what-to-do-if-you-get-lost-in-the-woods/" },
    { c: "Navigation & safety", n: "Sunscreen, SPF lip balm, sunglasses", t: ALL },
    { c: "Navigation & safety", n: "Satellite messenger / PLB (trips beyond cell coverage)", t: ["backpack", "day"] },
    { c: "Navigation & safety", n: "Bear spray (in a holster, not your pack)", t: ALL, x: "bear" },
    { c: "Navigation & safety", n: "Insect repellent and head net", t: ALL, s: ["warm"] },
    { c: "Navigation & safety", n: "Trip plan left with someone at home", t: ALL },
    { c: "Navigation & safety", n: "Fire extinguisher or water bucket near the fire ring", t: ["car"], l: "/how-to-put-out-a-fire/" },
    { c: "Navigation & safety", n: "Hand and toe warmers", t: ALL, s: ["cold"] },
    // Camp & personal
    { c: "Camp & personal", n: "Backpack sized for the trip", t: ["backpack", "day"], q: function (o) { return o.trip === "day" ? "18–30 L" : o.nights <= 3 ? "40–55 L" : "55–70 L"; }, l: "/tools/backpack-size/" },
    { c: "Camp & personal", n: "Pack liner or trash-compactor bag (waterproofing)", t: ["backpack"] },
    { c: "Camp & personal", n: "Trekking poles", t: ["backpack", "day"] },
    { c: "Camp & personal", n: "Lantern", t: ["car"] },
    { c: "Camp & personal", n: "Firewood bought locally (don't move firewood) — check fire restrictions", t: ["car"] },
    { c: "Camp & personal", n: "Toothbrush, toothpaste, travel toiletries", t: OVN },
    { c: "Camp & personal", n: "Trowel, toilet paper and bags to pack it out", t: ["backpack", "day"], l: "/backpacking-hygiene/" },
    { c: "Camp & personal", n: "Hand sanitizer and wipes", t: ALL },
    { c: "Camp & personal", n: "Quick-dry towel", t: OVN },
    { c: "Camp & personal", n: "Prescription meds and glasses/contacts", t: ALL },
    { c: "Camp & personal", n: "Camping permit / reservation / park pass (printed or offline)", t: OVN },
    { c: "Camp & personal", n: "Shade + extra water for the heat of the day", t: ["car"], s: ["warm"], l: "/cool-a-tent-without-electricity/" },
    { c: "Camp & personal", n: "Battery fan for the tent", t: ["car"], s: ["warm"] },
    // Extras
    { c: "Kids", n: "Kid-sized sleeping bag and pad", t: OVN, x: "kids" },
    { c: "Kids", n: "Extra layers and a full change of clothes per kid", t: ALL, x: "kids" },
    { c: "Kids", n: "Games, cards, headlamp of their own", t: OVN, x: "kids" },
    { c: "Kids", n: "Kid carrier or extra snacks for short legs", t: ["day", "backpack"], x: "kids" },
    { c: "Dog", n: "Leash (6 ft max in most parks), collar with ID", t: ALL, x: "dog" },
    { c: "Dog", n: "Dog food, bowl and extra water", t: ALL, x: "dog" },
    { c: "Dog", n: "Poop bags; check that pets are allowed on the trail", t: ALL, x: "dog" },
    { c: "Dog", n: "Dog sleeping pad or blanket", t: OVN, x: "dog" },
    { c: "Photography", n: "Camera, spare batteries, memory cards", t: ALL, x: "photo", l: "/best-camera-for-backpacking/" },
    { c: "Photography", n: "Shoulder-strap camera clip or strap", t: ["backpack", "day"], x: "photo" },
    { c: "Photography", n: "Mini tripod", t: ALL, x: "photo" },
    { c: "Fishing", n: "Rod, reel, tackle, and a current state fishing license", t: ALL, x: "fish", l: "/grand-mesa-fishing/" },
    { c: "Water & rain", n: "Pack cover or dry bags", t: ["backpack", "day"], x: "rain" },
    { c: "Water & rain", n: "Extra tarp over the tent/kitchen", t: ["car"], x: "rain" },
    { c: "Water & rain", n: "Spare dry socks in a zip bag", t: ALL, x: "rain" },
    { c: "Desert", n: "Extra 1–2 L water per person beyond the calculator", t: ALL, x: "desert", l: "/tools/water-calculator/" },
    { c: "Desert", n: "Electrolyte mix", t: ALL, x: "desert" },
    { c: "Desert", n: "Wide-brim hat and neck shade", t: ALL, x: "desert" }
  ];

  function opts() {
    return {
      trip: AO.radio("trip") || "car",
      season: AO.radio("season") || "warm",
      nights: Math.max(0, parseInt($("#nights").value, 10) || 0),
      people: Math.max(1, parseInt($("#people").value, 10) || 1),
      extras: $$("input[name=extra]:checked").map(function (i) { return i.value; })
    };
  }
  function key(o) { return "pack:" + [o.trip, o.season, o.nights, o.people, o.extras.join("+")].join("|"); }

  function build() {
    var o = opts();
    $("#nights-row").style.display = o.trip === "day" ? "none" : "";
    if (o.trip === "day") o.nights = 0;
    var list = ITEMS.filter(function (it) {
      if (it.t.indexOf(o.trip) < 0) return false;
      if (it.s && it.s.indexOf(o.season) < 0) return false;
      if (it.x && o.extras.indexOf(it.x) < 0) return false;
      return true;
    });
    var checked = AO.store.get(key(o), {});
    var groups = {};
    list.forEach(function (it) { (groups[it.c] = groups[it.c] || []).push(it); });
    var tripName = { car: "Car camping", backpack: "Backpacking", day: "Day hike" }[o.trip];
    var html = "<h2 style='margin:0'>" + tripName + " checklist</h2><p class='result-sub'>" +
      (o.trip === "day" ? "" : o.nights + " night" + (o.nights === 1 ? "" : "s") + " · ") + o.people + " " + (o.people === 1 ? "person" : "people") +
      " · " + { warm: "Summer / warm", shoulder: "Spring & fall", cold: "Winter / cold" }[o.season] + "</p>" +
      "<div class='progress'><i id='pbar'></i></div><p class='small muted' id='pcount'></p><div class='checklist'>";
    Object.keys(groups).forEach(function (g) {
      html += "<h3>" + AO.esc(g) + " <span class='small muted'>" + groups[g].length + "</span></h3><ul>";
      groups[g].forEach(function (it) {
        var id = (g + it.n).replace(/[^a-z0-9]/gi, "").slice(0, 60), on = !!checked[id];
        html += "<li" + (on ? " class='done'" : "") + "><input type='checkbox' id='" + id + "'" + (on ? " checked" : "") + "><span><label for='" + id + "'>" + AO.esc(it.n) + "</label>" +
          (it.q ? " <span class='muted small'>— " + AO.esc(it.q(o)) + "</span>" : "") + "</span>" + (it.l ? "<a href='" + it.l + "'>guide</a>" : "") + "</li>";
      });
      html += "</ul>";
    });
    html += "</div>";
    $("#result").innerHTML = html;
    progress();
    $$("#result input[type=checkbox]").forEach(function (cb) {
      cb.addEventListener("change", function () {
        var c = AO.store.get(key(o), {});
        if (cb.checked) c[cb.id] = 1; else delete c[cb.id];
        AO.store.set(key(o), c);
        cb.closest("li").classList.toggle("done", cb.checked);
        progress();
      });
    });
    var p = new URLSearchParams({ trip: o.trip, season: o.season, nights: o.nights, people: o.people, extras: o.extras.join(",") });
    history.replaceState(null, "", "?" + p.toString());
  }
  function progress() {
    var all = $$("#result input[type=checkbox]"), done = all.filter(function (c) { return c.checked; }).length;
    $("#pbar").style.width = (all.length ? (100 * done / all.length) : 0) + "%";
    $("#pcount").textContent = done + " of " + all.length + " packed";
  }
  function fromURL() {
    var p = new URLSearchParams(location.search);
    function setRadio(n, v) { var r = $('input[name="' + n + '"][value="' + v + '"]'); if (r) r.checked = true; }
    if (p.get("trip")) setRadio("trip", p.get("trip"));
    if (p.get("season")) setRadio("season", p.get("season"));
    if (p.get("nights")) $("#nights").value = p.get("nights");
    if (p.get("people")) $("#people").value = p.get("people");
    if (p.get("extras")) p.get("extras").split(",").forEach(function (x) { var c = $('input[name=extra][value="' + x + '"]'); if (c) c.checked = true; });
  }
  fromURL();
  $("#packform").addEventListener("input", build);
  $("#packform").addEventListener("change", build);
  $("#print").addEventListener("click", function () { window.print(); });
  $("#share").addEventListener("click", function () {
    var u = location.href;
    if (navigator.share) navigator.share({ title: "My packing list", url: u }).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(u).then(function () { $("#share").textContent = "Link copied"; });
  });
  $("#reset").addEventListener("click", function () { AO.store.set(key(opts()), {}); build(); });
  build();
})();
