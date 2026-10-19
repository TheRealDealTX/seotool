/* Kingwood Roofers — homeowner tools: cost estimator, pitch & area, storm self-check, roof age, homepage quick tools. */
(function () {
  "use strict";
  function $(sel, root) { return (root || document).querySelector(sel); }
  function val(form, name) {
    var el = form.querySelector("[name='" + name + "']:checked") || form.querySelector("[name='" + name + "']");
    return el ? el.value : null;
  }
  function out(form, key, text) { var el = $("[data-out='" + key + "']", form); if (el) el.textContent = text; }
  function money(n) { return "$" + (Math.round(n / 50) * 50).toLocaleString("en-US"); }
  function bind(form, fn) {
    form.querySelectorAll("input[type=range]").forEach(function (r) {
      var o = form.querySelector("output[for='" + r.id + "']");
      var fmt = r.getAttribute("data-fmt") || "";
      var big = +r.max > 1900 && +r.min > 1900;   // years: no thousands separator
      function upd() { if (o) o.textContent = (big ? r.value : Number(r.value).toLocaleString("en-US")) + fmt; }
      r.addEventListener("input", upd); upd();
    });
    form.addEventListener("input", fn); form.addEventListener("change", fn); fn();
  }

  // Installed price per sq ft of roof area (Houston-area planning ranges, 2026) and typical life here (years).
  var MAT = {
    "3tab": [4.00, 5.25, "3-tab asphalt shingles", 18],
    "arch": [4.50, 7.25, "Architectural asphalt shingles", 24],
    "class4": [5.50, 8.50, "Class 4 impact-resistant shingles", 27],
    "metal": [10.00, 16.00, "Standing-seam metal", 45],
    "stone": [9.00, 14.00, "Stone-coated steel", 40],
    "tile": [11.00, 18.00, "Concrete tile", 45],
    "shake": [0, 0, "Wood shake", 20]
  };
  var PITCH = { low: [1.06, 1.00], med: [1.15, 1.08], steep: [1.32, 1.22] };

  function roofCost(sqft, stories, matKey, pitchKey, layers, deckPct, trees) {
    var m = MAT[matKey], p = PITCH[pitchKey];
    var footprint = sqft / (stories === 2 ? 1.65 : stories === 3 ? 2.2 : 1);
    var area = footprint * 1.12 * p[0];
    var storyF = stories === 1 ? 1 : stories === 2 ? 1.06 : 1.12;
    var treeF = 1 + trees * 0.025;
    var lo = area * m[0] * p[1] * storyF * treeF, hi = area * m[1] * p[1] * storyF * treeF;
    var tear = layers === "2" ? area * 0.45 : layers === "shake" ? area * 1.6 : 0;   // shake: extra tear-off + new sheathing
    var deck = area * deckPct * 3.6;
    return { area: area, lo: lo + tear + deck, hi: hi + tear * 1.3 + deck * 1.35, m: m };
  }

  /* ---------- 1. full cost calculator ---------- */
  var cost = $("[data-tool='cost']");
  if (cost) bind(cost, function () {
    var c = roofCost(+val(cost, "sqft"), +val(cost, "stories"), val(cost, "material"), val(cost, "pitch"), val(cost, "layers"), +val(cost, "deck") / 100, +val(cost, "trees"));
    out(cost, "range", money(c.lo) + " – " + money(c.hi));
    out(cost, "area", Math.round(c.area).toLocaleString("en-US") + " sq ft");
    out(cost, "squares", (c.area / 100).toFixed(1));
    out(cost, "mat", c.m[2]);
    out(cost, "life", "~" + c.m[3] + " years");
    out(cost, "persq", "$" + Math.round(c.lo / (c.area / 100)).toLocaleString("en-US") + " – $" + Math.round(c.hi / (c.area / 100)).toLocaleString("en-US"));
  });

  /* ---------- homepage quick cost ---------- */
  var qc = $("[data-tool='quickcost']");
  if (qc) bind(qc, function () {
    var c = roofCost(+val(qc, "sqft"), +val(qc, "stories"), val(qc, "material"), "med", "1", 0.08, 1);
    out(qc, "range", money(c.lo) + " – " + money(c.hi));
    out(qc, "note", "About " + Math.round(c.area / 100) + " squares of " + c.m[2].toLowerCase() + ", typical life ~" + c.m[3] + " years.");
  });

  /* ---------- roof life (shared by homepage quick tool and the full estimator) ---------- */
  function life(form, matName, extra) {
    var year = +val(form, "year"), now = new Date().getFullYear();
    var age = Math.max(0, now - year);
    var base = { "3tab": 18, arch: 24, class4: 27, metal: 45, shake: 20 }[val(form, matName)];
    var trees = +val(form, "trees");
    var exp = base - trees * 1.5 + (extra || 0);
    exp = Math.max(8, exp);
    var left = Math.max(0, exp - age);
    var usedPct = Math.min(100, age / exp * 100);
    $("[data-out='used']", form).style.width = usedPct + "%";
    $("[data-out='leftbar']", form).style.width = (100 - usedPct) + "%";
    var lvl = usedPct >= 90 ? ["Plan your replacement", "Your roof is at or past its expected life here. Get a free inspection before the next storm season and start budgeting; an aged roof also affects many insurance policies."]
      : usedPct >= 65 ? ["Late in life", "Expect more repairs from here. Annual inspections, especially after storms, catch leaks before they reach decking and drywall."]
        : usedPct >= 35 ? ["Mid-life", "Keep valleys and gutters clear of needles and have it checked after hail or high wind."]
          : ["Plenty of life left", "Protect it: trim limbs over the roof, keep gutters flowing and inspect after major storms."];
    return { age: age, exp: exp, left: left, when: now + Math.round(left), lvl: lvl };
  }

  var ql = $("[data-tool='quicklife']");
  if (ql) bind(ql, function () {
    var l = life(ql, "lmat", 0);
    out(ql, "left", l.left < 1 ? "Time to plan" : "~" + Math.round(l.left) + " years");
    out(ql, "advice", l.lvl[1]);
  });

  var age = $("[data-tool='age']");
  if (age) bind(age, function () {
    var vent = { good: 1.5, some: 0, poor: -2.5 }[val(age, "vent")];
    var storms = -1.5 * +val(age, "storms");
    var clean = +val(age, "clean") * 1.2;
    var l = life(age, "material", vent + storms + clean);
    out(age, "left", l.left < 1 ? "At or past its life" : "~" + Math.round(l.left) + " years");
    out(age, "age", l.age + (l.age === 1 ? " year" : " years"));
    out(age, "life", "~" + Math.round(l.exp) + " years");
    out(age, "when", l.left < 1 ? "Now" : String(l.when));
    out(age, "level", l.lvl[0]);
    out(age, "advice", l.lvl[1]);
  });

  /* ---------- 2. pitch & area ---------- */
  var pitch = $("[data-tool='pitch']");
  if (pitch) bind(pitch, function () {
    var rise = +val(pitch, "rise"), len = +val(pitch, "length"), wid = +val(pitch, "width"), over = +val(pitch, "overhang");
    var shape = val(pitch, "shape");
    var mult = Math.sqrt(rise * rise + 144) / 12;
    var deg = Math.atan(rise / 12) * 180 / Math.PI;
    var area = (len + over * 2) * (wid + over * 2) * mult;
    var waste = shape === "hip" ? 0.15 : shape === "complex" ? 0.2 : 0.1;
    var squares = area / 100, order = squares * (1 + waste);
    var walk = rise <= 4 ? ["Low slope", "Below 4/12 needs low-slope materials (shingles need 2/12 minimum with special underlayment). Needles and water sit longer here."]
      : rise <= 7 ? ["Walkable", "A standard install with no steep-slope charges."]
        : rise <= 9 ? ["Steep", "Common on Kingwood two-stories. Crews need roof jacks and harnesses; expect a modest steep-slope labor charge."]
          : ["Very steep", "Specialty staging required; labor costs rise noticeably."];
    out(pitch, "deg", deg.toFixed(1) + "°");
    out(pitch, "pitch", rise + "/12");
    out(pitch, "mult", mult.toFixed(3));
    out(pitch, "area", Math.round(area).toLocaleString("en-US") + " sq ft");
    out(pitch, "squares", squares.toFixed(1));
    out(pitch, "order", order.toFixed(1) + " (+" + Math.round(waste * 100) + "% waste)");
    out(pitch, "bundles", String(Math.ceil(order * 3)));
    out(pitch, "walk", walk[0]);
    out(pitch, "walknote", walk[1]);
    var w = 260, h = Math.min(170, w / 2 * rise / 12);
    $("[data-pitch-tri]", pitch).setAttribute("points", (150 - w / 2) + ",190 150," + (190 - h) + " " + (150 + w / 2) + ",190");
    $("[data-pitch-rise]", pitch).setAttribute("y1", 190 - h);
    var lab = $("[data-pitch-label]", pitch);
    lab.textContent = rise + "/12 · " + deg.toFixed(0) + "°";
    lab.setAttribute("y", Math.max(18, 180 - h));
  });

  /* ---------- 3. storm damage self-check ---------- */
  var storm = $("[data-tool='storm']");
  if (storm) bind(storm, function () {
    var score = 0;
    storm.querySelectorAll("input[type=checkbox]:checked").forEach(function (c) { score += +c.value; });
    var a = +val(storm, "age");
    score += a >= 15 ? 3 : a >= 10 ? 2 : a >= 6 ? 1 : 0;
    var any = storm.querySelectorAll("input[type=checkbox]:checked").length > 0;
    var pct = any ? Math.min(100, Math.round(score / 25 * 100)) : 0;
    var lvl = pct >= 50 ? ["High likelihood of damage", "Several signs point to real storm damage. Don't wait: many Texas policies have reporting deadlines, and hidden leaks grow. Book a free inspection so we can document it before you call your insurer."]
      : pct >= 22 ? ["Possible damage", "Some warning signs are present. Hail and limb damage often can't be seen from the ground, so a free, photo-documented inspection is the safest next step."]
        : pct > 0 ? ["Low likelihood", "Few signs of damage. Watch your ceilings after the next heavy rain, and consider a free inspection if your roof is older than 10 years."]
          : ["Check the boxes that apply", "Walk around your property (stay off the roof) and tick anything you notice."];
    $("[data-out='meter']", storm).style.width = pct + "%";
    out(storm, "pct", pct + "%");
    out(storm, "level", lvl[0]);
    out(storm, "advice", lvl[1]);
  });
})();
