/* Shingle & Materials Calculator */
(function () {
  "use strict";
  var D = REP.data, M = REP.money, N = REP.num;
  var STYLE_WASTE = { gable: "simple", hip: "moderate", complex: "complex" };
  var LINES = { arch: "Architectural shingles", class4: "Class 4 impact-resistant shingles", "3tab": "3-tab shingles" };
  var UND = { syn: "Synthetic underlayment", f15: "#15 felt underlayment", f30: "#30 felt underlayment" };

  function up(x) { return x > 0 ? Math.ceil(x - 1e-9) : 0; }
  function pos(x) { return isFinite(x) && x > 0 ? x : 0; }

  // Rough edge lengths for a rectangular house ~1.6:1, from roof area and pitch.
  function estimateLf(area, rise, style) {
    var pf = REP.pitchFactor(rise), hf = REP.hipFactor(rise);
    var plan = area / pf, w = Math.sqrt(plan / 1.6), l = 1.6 * w, e;
    if (style === "gable") e = { eave: 2 * l, rake: 2 * w * pf, ridge: l, hip: 0, valley: 0 };
    else if (style === "complex") e = { eave: 2 * (l + w) * 1.25, rake: 0.5 * w * pf, ridge: (l - w) * 1.5, hip: 2 * w * hf * 1.3, valley: 1.2 * w * hf };
    else e = { eave: 2 * (l + w), rake: 0, ridge: l - w, hip: 2 * w * hf, valley: 0 };
    Object.keys(e).forEach(function (k) { e[k] = Math.round(e[k]); });
    return e;
  }

  REP.tool({
    id: "shingle-calculator",
    name: "Shingle & Materials Calculator",
    compute: function (v) {
      var area = v.area_mode === "squares" ? v.squares * 100 : v.roof_sqft;
      if (!(area > 0)) return { warnings: ["Enter the roof area (or squares) to build the order list."] };
      var rise = v.pitch || 6;
      var wastePct = v.waste_mode === "custom" ? Math.max(0, v.waste_custom) : D.waste.shingle[STYLE_WASTE[v.style] || "moderate"];
      var sq = area / 100, sqOrder = sq * (1 + wastePct / 100);
      var warnings = [], notes = [];

      var lf = v.lf_mode === "measured"
        ? { eave: pos(v.eave_lf), rake: pos(v.rake_lf), ridge: pos(v.ridge_lf), hip: pos(v.hip_lf), valley: pos(v.valley_lf) }
        : estimateLf(area, rise, v.style);
      if (v.lf_mode !== "measured") notes.push("Edge lengths estimated from area: eaves " + lf.eave + ", rakes " + lf.rake + ", ridges " + lf.ridge + ", hips " + lf.hip + ", valleys " + lf.valley + " ln ft. Switch to measurements for an exact order.");
      if (v.lf_mode === "measured" && lf.eave + lf.rake === 0) warnings.push("Eaves and rakes are 0. Enter the edge lengths, or choose \"Estimate from area\".");

      var rows = [], groups = { sh: 0, cap: 0, und: 0, metal: 0, vent: 0, fast: 0 };
      function add(g, item, qty, unit, price) {
        if (!(qty > 0)) return 0;
        var cost = qty * pos(price);
        rows.push([item, N(qty, 0), unit, M(cost)]);
        groups[g] += cost;
        return cost;
      }

      // Field shingles
      var bp = v.bpsq || 3;
      var bundles = up(sqOrder * bp);
      var shPrice = v.line === "class4" ? v.p_class4 : v.line === "3tab" ? v.p_3tab : v.p_arch;
      add("sh", LINES[v.line] || LINES.arch, bundles, "bundles", shPrice);

      // Starter + hip & ridge
      var starterLf = lf.eave + (v.starter_rakes ? lf.rake : 0);
      var starterB = up(starterLf / Math.max(1, v.starter_lf));
      add("cap", "Starter strip (" + N(starterLf, 0) + " ln ft)", starterB, "bundles", v.p_starter);
      var capLf = lf.ridge + lf.hip, capCov = v.ridge_type === "cut" ? v.ridge_lf_cut : v.ridge_lf_ded;
      var capB = up(capLf / Math.max(1, capCov));
      add("cap", (v.ridge_type === "cut" ? "Hip & ridge cut from 3-tab" : "Hip & ridge cap") + " (" + N(capLf, 0) + " ln ft)", capB, "bundles",
        v.ridge_type === "cut" ? v.p_3tab : v.p_ridge);

      // Underlayment
      var lowSlope = rise < 4;
      var undCov = { syn: v.cov_syn, f15: v.cov_f15, f30: v.cov_f30 }[v.und] || v.cov_syn;
      var undPrice = { syn: v.p_syn, f15: v.p_f15, f30: v.p_f30 }[v.und] || v.p_syn;
      var undRolls = up(sq * 1.05 * (lowSlope ? 2 : 1) / Math.max(0.5, undCov));
      add("und", (UND[v.und] || UND.syn) + (lowSlope ? " (double layer)" : ""), undRolls, "rolls", undPrice);
      var iwLf = (v.iw_valleys ? lf.valley : 0) + (v.iw_eaves ? lf.eave : 0);
      var iwRolls = up(iwLf / Math.max(1, v.iw_lf));
      add("und", "Ice & water shield (" + N(iwLf, 0) + " ln ft)", iwRolls, "rolls", v.p_iw);

      // Metal
      var dripLf = lf.eave + lf.rake;
      add("metal", "Drip edge, eaves + rakes (" + N(dripLf, 0) + " ln ft)", up(dripLf * 1.05 / 10), "10-ft pcs", v.p_drip);
      if (v.flash_on) {
        add("metal", "Step flashing (" + N(pos(v.wall_lf), 0) + " ln ft of sidewall)", up(pos(v.wall_lf) * 12 / 5 / 100), "bundles of 100", v.p_step);
        add("metal", "Headwall / apron flashing (" + N(pos(v.head_lf), 0) + " ln ft)", up(pos(v.head_lf) * 1.05 / 10), "10-ft pcs", v.p_head);
      }

      // Ventilation & penetrations
      var existing = pos(v.box_vents) + pos(v.turbines), rvLf = 0;
      if (v.vent === "ridge") {
        rvLf = v.rv_lf > 0 ? v.rv_lf : Math.max(0, lf.ridge - 2);
        add("vent", "Shingle-over ridge vent (" + N(rvLf, 0) + " ln ft)", up(rvLf / 4), "4-ft pcs", v.p_rv);
        if (existing) notes.push("Remove and deck over the " + existing + " existing box vent/turbine opening" + (existing > 1 ? "s" : "") + ": mixing ridge vent with other exhaust vents short-circuits the airflow.");
        if (lf.ridge < 1) warnings.push("No ridge length to vent. Enter ridges or choose another ventilation option.");
      } else if (v.vent === "box") {
        add("vent", "Box vents", pos(v.box_vents), "each", v.p_box);
        add("vent", "Turbine vents", pos(v.turbines), "each", v.p_turb);
      }
      add("vent", "Pipe boots", pos(v.pipes), "each", v.p_boot);

      // Fasteners & sealant
      var nails = sqOrder * pos(v.nails_sq) * (v.nails === 6 ? 1.5 : 1);
      add("fast", "Coil roofing nails (" + v.nails + " per shingle, " + N(Math.round(nails), 0) + ")", up(nails / Math.max(1, v.nails_box)), "boxes", v.p_nails);
      var caps = sq * (lowSlope ? 2 : 1) * pos(v.cap_sq);
      add("fast", "Cap nails for underlayment", up(caps / Math.max(1, v.cap_box)), "boxes", v.p_cap);
      add("fast", "Roof cement / sealant", up(sq / 6 + pos(v.pipes) * 0.5), "tubes", v.p_cement);

      var mat = rows.length ? Object.keys(groups).reduce(function (a, k) { return a + groups[k]; }, 0) : 0;
      var tax = mat * pos(v.tax) / 100, total = mat + tax;
      rows.push(["Sales tax (" + v.tax + "%)", "", "", M(tax)]);

      if (rise < 2) warnings.push("Asphalt shingles cannot be installed below 2/12. Use the flat roof calculator for a low-slope system.");
      else if (lowSlope) notes.push("At " + rise + "/12 the code and shingle manufacturers require two layers of underlayment (2/12 to 4/12); rolls and cap nails are doubled.");
      if (v.nails === 6) notes.push("High-wind install: use the manufacturer's high-wind starter at eaves and rakes, and hot-dipped galvanized or stainless nails within a few miles of salt water.");
      if (v.line === "arch") notes.push("Class 4 impact-resistant shingles would add about " + M(bundles * (v.p_class4 - v.p_arch) * (1 + v.tax / 100)) + " in material. Many Texas insurers discount premiums for UL 2218 Class 4 roofs.");
      if (v.vent === "ridge" && rvLf > 0) notes.push(N(rvLf, 0) + " ft of ridge vent gives roughly " + N(rvLf * 18, 0) + " sq in of exhaust net free area at 18 sq in/ft. Check it and the soffit intake with the attic ventilation calculator.");

      return {
        headline: { label: "Estimated material cost", value: total, format: "money",
          sub: bundles + " bundles · " + N(sqOrder, 1) + " squares ordered (" + N(wastePct, 0) + "% waste)" },
        kpis: [
          { label: "Roof area", text: N(Math.round(area), 0) + " sq ft (" + N(sq, 1) + " sq)" },
          { label: "Shingle bundles", text: N(bundles, 0) },
          { label: "Material per roof square", value: total / sq, format: "money" },
          { label: "Material per sq ft", value: total / area, format: "money2" }
        ],
        breakdown: { title: "Where the money goes", items: [
          { label: "Field shingles", value: groups.sh },
          { label: "Starter & ridge cap", value: groups.cap },
          { label: "Underlayment & ice/water", value: groups.und },
          { label: "Drip edge & flashing", value: groups.metal },
          { label: "Vents & boots", value: groups.vent },
          { label: "Nails & sealant", value: groups.fast },
          { label: "Sales tax", value: tax }
        ] },
        table: { title: "Order list", head: ["Item", "Qty", "Unit", "Cost"], rows: rows, foot: ["Total", "", "", M(total)] },
        warnings: warnings,
        notes: notes,
        summary: [
          "Roof: " + Math.round(area) + " sq ft (" + sq.toFixed(1) + " squares), " + rise + "/12, " + v.style + " roof, " + wastePct + "% waste",
          "Edges (" + (v.lf_mode === "measured" ? "measured" : "estimated") + "): eaves " + lf.eave + ", rakes " + lf.rake + ", ridges " + lf.ridge + ", hips " + lf.hip + ", valleys " + lf.valley + " ln ft"
        ].concat(rows.slice(0, -1).map(function (r) { return r[0] + ": " + r[1] + " " + r[2] + " (" + r[3] + ")"; }))
          .concat(["Estimated material cost incl. " + v.tax + "% tax: " + M(total)])
      };
    }
  });
})();
