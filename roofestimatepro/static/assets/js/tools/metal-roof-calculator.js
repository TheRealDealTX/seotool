/* Metal Roof Calculator */
(function () {
  "use strict";
  var D = REP.data, M = REP.money, N = REP.num;
  var PROFILES = {
    ss16: { name: "16 in standing seam", cov: 16, fam: "ss", gauge: 24 },
    ss12: { name: "12 in standing seam", cov: 12, fam: "ss", gauge: 24 },
    ss18: { name: "18 in standing seam", cov: 18, fam: "ss", gauge: 24 },
    rpanel: { name: "R-panel / PBR", cov: 36, fam: "ef", gauge: 26 },
    "5v": { name: "5V crimp", cov: 24, fam: "ef", gauge: 26 }
  };
  var UND = { ht: "High-temp synthetic underlayment", htsa: "High-temp peel & stick underlayment", syn: "Standard synthetic underlayment" };

  function up(x) { return x > 0 ? Math.ceil(x - 1e-9) : 0; }
  function pos(x) { return isFinite(x) && x > 0 ? x : 0; }
  function steepAdj(r) { return r > 12 ? 0.45 : r >= 11 ? 0.30 : r >= 9 ? 0.20 : r >= 7 ? 0.10 : 0; }
  function ftIn(ft) { var inch = Math.round(ft * 12), f = Math.floor(inch / 12), i = inch - f * 12; return f + "' " + i + '"'; }

  REP.tool({
    id: "metal-roof-calculator",
    name: "Metal Roof Calculator",
    rowDefaults: { planes: [
      { name: "Main roof", shape: "rect", eave: 50, slope: 18, n: 2 },
      { name: "Back porch", shape: "rect", eave: 24, slope: 10, n: 1 }
    ] },
    init: function (form, run) {
      // Changing the profile refills its coverage width and usual gauge.
      form.querySelector('[name="panel"]').addEventListener("change", function (e) {
        var p = PROFILES[e.target.value] || PROFILES.ss16;
        form.querySelector('[name="cov_in"]').value = p.cov;
        form.querySelectorAll('[name="gauge"]').forEach(function (r) { r.checked = +r.value === p.gauge; });
        run();
      });
    },
    compute: function (v) {
      var P = PROFILES[v.panel] || PROFILES.ss16, ss = P.fam === "ss";
      var cov = v.cov_in > 0 ? v.cov_in : P.cov, covFt = cov / 12;
      var gm = { 29: v.g29, 26: v.g26, 24: v.g24 }[v.gauge];
      if (!(gm > 0)) gm = 1;
      var psf = (ss ? v.p_ss : v.panel === "5v" ? v.p_5v : v.p_rpanel) * gm;
      var ohFt = pos(v.overhang_in) / 12, rise = v.pitch;
      var warnings = [], notes = [], rows = [];
      var area = 0, panels = 0, panelLf = 0, clips = 0, matCost = 0, cutRows = [], summaryCuts = [];

      function cutLen(slope) { return Math.ceil((slope + ohFt) * 12 - 1e-9) / 12; }
      function clipsFor(n, cut) { return n * (Math.ceil(cut * 12 / Math.max(6, v.clip_in) - 1e-9) + 1); }

      if (v.size_mode === "total") {
        var w = D.waste.metal[v.complexity] || D.waste.metal.moderate;
        area = pos(v.total_sf);
        var len = pos(v.panel_len), cut = cutLen(len);
        if (area > 0 && len > 0) {
          panels = up(area * (1 + w / 100) / (covFt * len));
          panelLf = panels * cut;
          clips = clipsFor(panels, cut);
          cutRows.push(["Panels, " + ftIn(cut) + " (" + w + "% waste)", panels, panelLf]);
        }
      } else {
        (v.rows.planes || []).forEach(function (r, i) {
          var eave = pos(r.eave), slope = pos(r.slope), n = Math.max(1, Math.round(r.n || 1));
          if (!eave || !slope) return;
          var across = up(eave * 12 / cov), cut = cutLen(slope), tri = r.shape === "tri";
          var full = tri ? Math.ceil(across / 2) + 1 : across;
          var label = (r.name || "Plane " + (i + 1)) + (n > 1 ? " ×" + n : "") + (tri ? " (hip end)" : "");
          area += (tri ? eave * slope / 2 : eave * slope) * n;
          panels += full * n;
          panelLf += full * n * cut;
          clips += clipsFor(full * n, cut);
          cutRows.push([label + ": " + (tri ? "longest " : "") + ftIn(cut), full * n, full * n * cut]);
          summaryCuts.push(label + ": " + full * n + " panels @ " + ftIn(cut) + (tri ? " (cut on the diagonal)" : ""));
        });
      }
      if (!(area > 0) || !panels) return { warnings: ["Enter at least one roof plane with an eave length and slope length (or a total area and panel length)."] };

      var sq = area / 100, panelSf = panelLf * covFt;
      cutRows.forEach(function (c) {
        var cost = c[2] * covFt * psf;
        matCost += cost;
        rows.push([c[0], N(c[1], 0), "panels", M(cost)]);
      });
      var panelCost = matCost;
      function add(item, qty, unit, price) {
        if (!(qty > 0)) return 0;
        var cost = qty * pos(price);
        rows.push([item, N(qty, 0), unit, M(cost)]);
        matCost += cost;
        return cost;
      }

      // Trim in 10'6" pieces, lapped
      var eff = Math.max(1, v.trim_len - pos(v.trim_lap) / 12), trimPcs = 0;
      [["Eave trim", v.eave_lf, v.p_eave], ["Rake / gable trim", v.rake_lf, v.p_rake], ["Ridge & hip cap", v.ridge_lf, v.p_ridge],
       ["Valley", v.valley_lf, v.p_valley], ["Sidewall / endwall flashing", v.wall_lf, v.p_wall]].forEach(function (t) {
        var pcs = up(pos(t[1]) / eff);
        trimPcs += pcs;
        add(t[0] + " (" + N(pos(t[1]), 0) + " ln ft)", pcs, "pcs", t[2]);
      });

      // Closures: profile-matched at eaves (exposed fastener) and both sides of ridges/hips
      var closures = (ss ? 0 : up(pos(v.eave_lf) / covFt)) + up(pos(v.ridge_lf) * 2 / covFt);
      add(ss ? "Ridge / hip Z-closures" : "Inside & outside foam closures", closures, "each", v.p_closure);

      // Fasteners
      var trimScrews = trimPcs * 10;
      if (ss) {
        add("Standing seam clips (" + v.clip_in + " in spacing)", clips, "each", v.p_clip);
        add("Pancake screws for clips & trim (" + N(clips + trimScrews, 0) + ")", up((clips + trimScrews) / 250), "bags of 250", v.p_pancake);
      } else {
        var screws = panelSf / 100 * pos(v.screws_sq);
        add("Panel screws (" + N(Math.round(screws), 0) + ")", up(screws / 250), "bags of 250", v.p_screws);
        add("Trim / stitch screws (" + N(trimScrews, 0) + ")", up(trimScrews / 250), "bags of 250", v.p_pancake);
      }

      // Underlayment, butyl, sealant
      var uc = { ht: v.cov_ht, htsa: v.cov_htsa, syn: v.cov_syn }[v.und] || v.cov_ht;
      var up_ = { ht: v.p_ht, htsa: v.p_htsa, syn: v.p_syn }[v.und] || v.p_ht;
      var undRolls = up(sq * 1.05 / Math.max(0.5, uc));
      add(UND[v.und] || UND.ht, undRolls, "rolls", up_);
      var sideLaps = !ss && rise < 3 ? panelLf : 0;
      var butylLf = pos(v.eave_lf) + 2 * pos(v.ridge_lf) + 2 * pos(v.valley_lf) + pos(v.wall_lf) + sideLaps;
      add("Butyl tape (" + N(Math.round(butylLf), 0) + " ln ft" + (sideLaps ? " incl. side laps" : "") + ")", up(butylLf / 45), "rolls", v.p_butyl);
      add("Tube sealant", Math.max(2, up(trimPcs / 4)), "tubes", v.p_sealant);

      var tax = matCost * pos(v.tax) / 100;
      var reg = REP.region(v.region).factor, steep = steepAdj(rise);
      var rate = ss ? v.lab_ss : v.lab_ef;
      var labor = sq * pos(rate) * (1 + steep) * reg;
      var tear = v.tear_on ? sq * (pos(v.tear1) + (Math.max(1, v.layers) - 1) * pos(v.tear_add)) * (1 + steep) * reg : 0;
      var sub = matCost + tax + labor + tear, op = sub * pos(v.op) / 100, total = sub + op;
      rows.push(["Sales tax on materials (" + v.tax + "%)", "", "", M(tax)]);
      rows.push(["Install labor (" + P.name + (steep || reg !== 1 ? ", ×" + ((1 + steep) * reg).toFixed(2) : "") + ")", N(sq, 1), "sq", M(labor)]);
      if (tear) rows.push(["Tear-off & disposal, " + v.layers + " layer" + (v.layers > 1 ? "s" : ""), N(sq, 1), "sq", M(tear)]);
      rows.push(["Overhead & profit (" + v.op + "%)", "", "", M(op)]);

      // Slope checks
      if (ss) {
        if (rise < 0.25) warnings.push("Standing seam needs at least 1/4 in 12.");
        else if (rise < 3) notes.push("Below 3/12 most snap-lock panels are not rated. Use a mechanically seamed (double-lock) panel approved for " + (rise < 1 ? rise * 4 + "/4" : rise) + " in 12.");
      } else if (v.panel === "5v") {
        if (rise < 3) warnings.push("5V crimp generally needs at least 3/12. Choose R-panel with lap sealant or standing seam for this slope.");
      } else {
        if (rise < 0.5) warnings.push("Exposed-fastener R-panel needs at least 1/2 in 12, with sealant at the laps.");
        else if (rise < 3) notes.push("Below 3/12 the code requires applied lap sealant on lapped panels. Butyl tape for the side laps is included.");
      }
      if (v.und === "syn") notes.push("Most standing seam manufacturers require a high-temperature underlayment (about 240°F or higher). Check the panel install guide before using standard synthetic.");
      if (v.gauge === 29 && ss) notes.push("29 gauge is unusual for standing seam. 24 gauge resists hail dents better.");
      if (v.region === "houston") notes.push("In the TWIA area, use a panel and attachment covered by a TDI product evaluation or an engineer's design; clip and screw spacing near edges is often tighter than these defaults.");
      notes.push("Check your homeowner policy for a cosmetic damage exclusion on metal roofs; many Texas policies do not pay for hail dents that don't let water in.");

      return {
        headline: { label: "Estimated installed cost", value: total, format: "money",
          sub: "Materials " + M(matCost + tax) + " · labor & tear-off " + M(labor + tear) },
        kpis: [
          { label: "Panels", text: N(panels, 0) + " (" + N(Math.round(panelLf), 0) + " ln ft)" },
          { label: "Roof area", text: N(Math.round(area), 0) + " sq ft (" + N(sq, 1) + " sq)" },
          { label: ss ? "Clips" : "Panel screws", text: ss ? N(clips, 0) : N(Math.round(panelSf / 100 * pos(v.screws_sq)), 0) },
          { label: "Installed per square", value: total / sq, format: "money" }
        ],
        breakdown: { title: "Where the money goes", items: [
          { label: "Panels", value: panelCost },
          { label: "Trim, closures, fasteners & underlayment", value: matCost - panelCost },
          { label: "Sales tax", value: tax },
          { label: "Install labor", value: labor },
          { label: "Tear-off", value: tear },
          { label: "Overhead & profit", value: op }
        ] },
        table: { title: "Cut list & line items", head: ["Item", "Qty", "Unit", "Cost"], rows: rows, foot: ["Installed total", "", "", M(total)] },
        warnings: warnings,
        notes: notes,
        summary: [
          "Panel: " + P.name + ", " + cov + " in coverage, " + v.gauge + " ga, pitch " + rise + "/12",
          "Roof area " + Math.round(area) + " sq ft (" + sq.toFixed(1) + " sq); " + panels + " panels, " + Math.round(panelLf) + " ln ft (" + Math.round(panelSf) + " sq ft of panel)"
        ].concat(summaryCuts)
          .concat(["Trim: eave " + pos(v.eave_lf) + ", rake " + pos(v.rake_lf) + ", ridge/hip " + pos(v.ridge_lf) + ", valley " + pos(v.valley_lf) + ", wall " + pos(v.wall_lf) + " ln ft (" + trimPcs + " pieces)",
            (ss ? "Clips: " + clips : "Panel screws: " + Math.round(panelSf / 100 * pos(v.screws_sq))) + "; underlayment " + undRolls + " rolls",
            "Location: " + REP.region(v.region).name + (tear ? "; tear-off " + v.layers + " layer(s)" : "; no tear-off"),
            "Materials " + M(matCost + tax) + ", labor " + M(labor) + (tear ? ", tear-off " + M(tear) : "") + ", O&P " + M(op),
            "Estimated installed cost: " + M(total)])
      };
    }
  });
})();
