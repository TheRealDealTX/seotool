/* Roof Repair Cost Calculator */
(function () {
  "use strict";
  var M = REP.money, D = REP.data;

  // key, ticket label, qty unit (for the Qty column)
  var ITEMS = [
    ["shg", "Shingle replacement (per 100 sq ft patch)", "patch"],
    ["ridge", "Ridge cap", "lf"],
    ["boot", "Pipe boot replacement", "ea"],
    ["chim", "Chimney flashing", "ea"],
    ["step", "Step / wall flashing", "lf"],
    ["valley", "Valley repair", "lf"],
    ["deck", "Decking replacement (4×8 sheet)", "sheet"],
    ["drip", "Drip edge", "lf"],
    ["sky", "Skylight re-flash", "ea"],
    ["vent", "Box vent / turbine replacement", "ea"]
  ];
  var PITCH = { walk: 1, p8: 1.15, p10: 1.3, p12: 1.45 };
  var PITCH_NAME = { walk: "walkable pitch", p8: "7–8/12 pitch", p10: "9–10/12 pitch", p12: "11/12+ pitch" };
  var STORY = { 1: 1, 2: 1.1, 3: 1.2 };
  var TIER = { budget: 0, typical: 0.5, premium: 1 };

  function pick(lo, hi, t) { return lo + (hi - lo) * t; }

  REP.tool({
    id: "roof-repair-cost-calculator",
    name: "Roof Repair Cost Calculator",
    compute: function (v) {
      var t = TIER[v.tier] != null ? TIER[v.tier] : 0.5;
      var reg = REP.region(v.region).factor;
      var mult = (PITCH[v.pitch] || 1) * (STORY[v.stories] || 1) * reg;
      var rows = [], lines = [], warnings = [];
      var lo = 0, hi = 0, mid = 0;

      function add(label, qtyText, unitLo, unitHi, qty, scaled) {
        var k = scaled ? mult : 1;
        if (unitHi < unitLo) { var s = unitLo; unitLo = unitHi; unitHi = s; }
        var a = qty * unitLo * k, b = qty * unitHi * k, c = qty * pick(unitLo, unitHi, t) * k;
        lo += a; hi += b; mid += c;
        rows.push([label, qtyText, M(pick(unitLo, unitHi, t) * k), M(c)]);
        lines.push(label + ": " + qtyText + " = " + M(c));
      }

      ITEMS.forEach(function (it) {
        var key = it[0], q = Math.max(0, v["q_" + key]);
        if (!v["use_" + key]) return;
        if (!q) { warnings.push(it[1] + " is switched on with a quantity of 0."); return; }
        add(it[1], REP.num(q) + " " + it[2], v["lo_" + key], v["hi_" + key], q, true);
      });
      if (v.use_tarp) {
        var ta = Math.max(0, v.q_tarp);
        var tlo = v.lo_tarpb + ta * v.lo_tarps, thi = v.hi_tarpb + ta * v.hi_tarps;
        add("Emergency tarp (setup + " + REP.num(ta) + " sq ft)", "1 ea", tlo, thi, 1, true);
      }
      if (v.use_leak) add("Leak investigation / inspection", "1 ea", v.lo_leak, v.hi_leak, 1, false);

      if (!rows.length) return { warnings: warnings.concat(["Switch on at least one repair item to build a ticket."]) };

      var minC = Math.max(0, v.minimum);
      var billed = Math.max(mid, minC), billedLo = Math.max(lo, minC), billedHi = Math.max(hi, minC);
      if (mid < minC) rows.push(["Minimum service charge adjustment", "", "", M(minC - mid)]);

      var notes = [];
      if (mid < minC) notes.push("The items total " + M(mid) + ", below the " + M(minC) + " minimum service charge, so the job is billed at the minimum. Bundling other small fixes into the same visit costs little extra.");
      if (mult !== 1) notes.push("Line prices include a ×" + mult.toFixed(2) + " factor for " + PITCH_NAME[v.pitch] + ", " + v.stories + " stor" + (v.stories > 1 ? "ies" : "y") + " and " + REP.region(v.region).name + ".");

      // Repair or replace
      var arch = (D.materials || []).filter(function (m) { return m.key === "arch"; })[0];
      var range = arch ? arch.range : [450, 650];
      var sqft = Math.max(0, v.roof_sqft), repl = 0, ratio = null;
      if (sqft > 0) {
        repl = sqft / 100 * pick(range[0], range[1], t) * reg;
        ratio = billed / repl;
        if (ratio >= 0.25) notes.push("Repair or replace? This repair is " + Math.round(ratio * 100) + "% of an estimated " + M(repl) + " architectural-shingle replacement. Above about 25–30%, get a replacement price before you commit to the repair.");
      }
      if (v.age >= 20) notes.push("At " + v.age + " years the roof is at or past typical shingle life in Texas. Expect repairs to be harder to match and get a replacement quote alongside this one.");
      else if (v.age >= 15) notes.push("At " + v.age + " years, shingles are likely brittle and discontinued; repairs may not match. Ask the roofer to assess the whole roof, not only the leak.");
      if (v.use_tarp) notes.push("Emergency tarping to prevent further damage is normally reimbursable on a covered storm claim. Keep the invoice and photos.");
      if (v.use_deck) notes.push("Decking replacement needs the shingles above it removed; include a shingle patch line for the same area.");
      if (v.use_chim || v.use_sky) notes.push("Chimney and skylight leaks are often flashing failures (wear), which insurance usually does not cover unless storm damage caused them.");

      var kpis = [
        { label: "Low – high range", text: M(billedLo) + " – " + M(billedHi) },
        { label: "Line items", text: String(rows.length - (mid < minC ? 1 : 0)) },
        { label: "Access & region factor", text: "×" + mult.toFixed(2) }
      ];
      if (ratio != null) kpis.push({ label: "Share of a new roof (" + M(repl) + ")", text: REP.pct(ratio * 100, 0) });

      var summary = ["Repair ticket (" + v.tier + " pricing), " + PITCH_NAME[v.pitch] + ", " + v.stories + " stor" + (v.stories > 1 ? "ies" : "y") + ", " + REP.region(v.region).name]
        .concat(lines);
      if (mid < minC) summary.push("Minimum service charge applies: " + M(minC));
      summary.push("Estimated repair cost: " + M(billed) + " (range " + M(billedLo) + "–" + M(billedHi) + ")");
      if (ratio != null) summary.push("Estimated full replacement for comparison: " + M(repl) + " (" + sqft + " sq ft, architectural shingles); repair = " + Math.round(ratio * 100) + "%");
      if (v.age) summary.push("Roof age: " + v.age + " years");

      return {
        headline: { label: "Estimated repair cost", value: billed, format: "money",
          sub: "Range " + M(billedLo) + " – " + M(billedHi) + " (budget to premium)" },
        kpis: kpis,
        warnings: warnings,
        table: { title: "Repair ticket", head: ["Item", "Qty", "Unit", "Amount"], rows: rows, foot: ["Total", "", "", M(billed)] },
        notes: notes,
        summary: summary
      };
    }
  });
})();
