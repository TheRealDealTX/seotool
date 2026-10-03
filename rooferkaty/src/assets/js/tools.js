/* Katy Roofer — homeowner tools: cost estimator, pitch & area calculator, storm damage self-check. */
(function () {
  "use strict";
  function $(sel, root) { return (root || document).querySelector(sel); }
  function val(form, name) {
    var el = form.querySelector("[name='" + name + "']:checked") || form.querySelector("[name='" + name + "']");
    return el ? el.value : null;
  }
  function money(n) { return "$" + (Math.round(n / 50) * 50).toLocaleString("en-US"); }
  function bindOutputs(form) {
    form.querySelectorAll("input[type=range]").forEach(function (r) {
      var out = form.querySelector("output[for='" + r.id + "']");
      var fmt = r.getAttribute("data-fmt") || "";
      function upd() { if (out) out.textContent = Number(r.value).toLocaleString("en-US") + fmt; }
      r.addEventListener("input", upd); upd();
    });
  }

  /* ---------- 1. Roof replacement cost estimator ---------- */
  var cost = $("[data-tool='cost']");
  if (cost) {
    // Installed price per sq ft of roof area (Houston-area planning ranges, 2026).
    var MAT = {
      "3tab": [4.00, 5.25, "3-tab asphalt shingles", 20],
      "arch": [4.50, 7.25, "Architectural asphalt shingles", 28],
      "class4": [5.50, 8.50, "Class 4 impact-resistant shingles", 30],
      "metal": [10.00, 16.00, "Standing-seam metal", 50],
      "stone": [9.00, 14.00, "Stone-coated steel", 45],
      "tile": [11.00, 18.00, "Concrete tile", 50]
    };
    var PITCH = { low: [1.06, 1.00], med: [1.15, 1.08], steep: [1.32, 1.22] };
    var calcCost = function () {
      var sqft = +val(cost, "sqft"), stories = +val(cost, "stories"), m = MAT[val(cost, "material")], p = PITCH[val(cost, "pitch")];
      var layers = +val(cost, "layers"), deck = +val(cost, "deck") / 100;
      var footprint = sqft / (stories === 2 ? 1.65 : stories === 3 ? 2.2 : 1);
      var area = footprint * 1.12 * p[0];                       // overhangs + slope
      var storyF = stories === 1 ? 1 : stories === 2 ? 1.06 : 1.12;
      var lo = area * m[0] * p[1] * storyF, hi = area * m[1] * p[1] * storyF;
      var extraTear = (layers - 1) * area * 0.45;
      var deckCost = area * deck * 3.6;
      lo += extraTear + deckCost; hi += extraTear * 1.3 + deckCost * 1.35;
      $("[data-out='range']", cost).textContent = money(lo) + " – " + money(hi);
      $("[data-out='area']", cost).textContent = Math.round(area).toLocaleString("en-US") + " sq ft";
      $("[data-out='squares']", cost).textContent = (area / 100).toFixed(1);
      $("[data-out='mat']", cost).textContent = m[2];
      $("[data-out='life']", cost).textContent = "~" + m[3] + " years";
      $("[data-out='persq']", cost).textContent = "$" + Math.round(lo / (area / 100)).toLocaleString("en-US") + " – $" + Math.round(hi / (area / 100)).toLocaleString("en-US");
    };
    bindOutputs(cost);
    cost.addEventListener("input", calcCost); cost.addEventListener("change", calcCost); calcCost();
  }

  /* ---------- 2. Roof pitch & area calculator ---------- */
  var pitch = $("[data-tool='pitch']");
  if (pitch) {
    var calcPitch = function () {
      var rise = +val(pitch, "rise"), len = +val(pitch, "length"), wid = +val(pitch, "width"), over = +val(pitch, "overhang");
      var shape = val(pitch, "shape");
      var mult = Math.sqrt(rise * rise + 144) / 12;
      var deg = Math.atan(rise / 12) * 180 / Math.PI;
      var foot = (len + over * 2) * (wid + over * 2);
      var area = foot * mult;
      var waste = shape === "hip" ? 0.15 : shape === "complex" ? 0.2 : 0.1;
      var squares = area / 100, order = squares * (1 + waste);
      var walk = rise <= 4 ? ["Low slope", "Needs low-slope materials below 4/12 (shingles require 2/12 minimum with special underlayment)."]
        : rise <= 7 ? ["Walkable", "Typical for Katy homes. Standard install, no extra steep charges."]
          : rise <= 9 ? ["Steep", "Crews need roof jacks and harnesses; expect a modest steep-slope labor charge."]
            : ["Very steep", "Specialty staging required; labor costs rise noticeably."];
      $("[data-out='deg']", pitch).textContent = deg.toFixed(1) + "°";
      $("[data-out='pitch']", pitch).textContent = rise + "/12";
      $("[data-out='mult']", pitch).textContent = mult.toFixed(3);
      $("[data-out='area']", pitch).textContent = Math.round(area).toLocaleString("en-US") + " sq ft";
      $("[data-out='squares']", pitch).textContent = squares.toFixed(1);
      $("[data-out='order']", pitch).textContent = order.toFixed(1) + " (+" + Math.round(waste * 100) + "% waste)";
      $("[data-out='bundles']", pitch).textContent = Math.ceil(order * 3);
      $("[data-out='walk']", pitch).textContent = walk[0];
      $("[data-out='walknote']", pitch).textContent = walk[1];
      // triangle drawing
      var w = 260, h = Math.min(170, w / 2 * rise / 12);
      var tri = $("[data-pitch-tri]", pitch);
      tri.setAttribute("points", (150 - w / 2) + ",190 150," + (190 - h) + " " + (150 + w / 2) + ",190");
      $("[data-pitch-rise]", pitch).setAttribute("y1", 190 - h);
      $("[data-pitch-label]", pitch).textContent = rise + "/12 · " + deg.toFixed(0) + "°";
      $("[data-pitch-label]", pitch).setAttribute("y", Math.max(18, 180 - h));
    };
    bindOutputs(pitch);
    pitch.addEventListener("input", calcPitch); pitch.addEventListener("change", calcPitch); calcPitch();
  }

  /* ---------- 3. Storm damage self-check ---------- */
  var storm = $("[data-tool='storm']");
  if (storm) {
    var calcStorm = function () {
      var score = 0;
      storm.querySelectorAll("input[type=checkbox]:checked").forEach(function (c) { score += +c.value; });
      var age = +val(storm, "age");
      score += age >= 15 ? 3 : age >= 10 ? 2 : age >= 6 ? 1 : 0;
      var pct = Math.min(100, Math.round(score / 22 * 100));
      var lvl = pct >= 55 ? ["High likelihood of damage", "Several signs point to real storm damage. Don't wait — most Texas policies have filing deadlines, and hidden leaks grow. Book a free inspection so we can document it with photos before you call your insurer."]
        : pct >= 25 ? ["Possible damage", "Some warning signs are present. Damage from hail often isn't visible from the ground, so a free, photo-documented inspection is the safest next step."]
          : pct > 0 ? ["Low likelihood", "Few signs of damage. Keep an eye on ceilings after the next heavy rain, and consider a free inspection if your roof is older than 10 years."]
            : ["Check the boxes that apply", "Walk around your property (stay off the roof) and tick anything you notice."];
      $("[data-out='meter']", storm).style.width = pct + "%";
      $("[data-out='meter']", storm).style.backgroundPosition = (100 - pct) + "% 0";
      $("[data-out='pct']", storm).textContent = pct + "%";
      $("[data-out='level']", storm).textContent = lvl[0];
      $("[data-out='advice']", storm).textContent = lvl[1];
    };
    bindOutputs(storm);
    storm.addEventListener("input", calcStorm); storm.addEventListener("change", calcStorm); calcStorm();
  }
})();
