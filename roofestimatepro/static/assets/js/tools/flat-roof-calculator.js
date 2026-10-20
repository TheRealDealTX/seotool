/* Flat & Commercial Roof Calculator */
(function () {
  "use strict";
  var M = REP.money, N = REP.num;
  // Installed $/sf ranges (Texas 2026, DFW, incl. labor & O&P, excl. tear-off & insulation)
  var SYS = {
    tpo_ma: { name: "TPO 60-mil, mechanically attached", lo: 7.00, hi: 10.00, att: "ma", roll: [10, 100], plies: 1 },
    tpo_fa: { name: "TPO 60-mil, fully adhered", lo: 8.00, hi: 11.50, att: "fa", roll: [10, 100], plies: 1 },
    pvc: { name: "PVC 60-mil, mechanically attached", lo: 9.00, hi: 13.00, att: "ma", roll: [10, 100], plies: 1 },
    epdm_fa: { name: "EPDM 60-mil, fully adhered", lo: 7.00, hi: 10.50, att: "fa", roll: [10, 100], plies: 1 },
    modbit: { name: "Modified bitumen, 2-ply", lo: 7.50, hi: 11.00, att: "mb", roll: [3.28, 32.8], plies: 2 },
    bur: { name: "Built-up roof (BUR), 4-ply", lo: 7.50, hi: 11.50, att: "bur", roll: [3.28, 180], plies: 4 },
    silicone: { name: "Silicone coating restoration", lo: 3.50, hi: 6.00, att: "coat", mils: 20, solids: 96 },
    acrylic: { name: "Acrylic coating restoration", lo: 2.75, hi: 5.00, att: "coat", mils: 20, solids: 55 }
  };
  var COVER = { hdiso: { name: "1/2 in HD polyiso cover board", r: 2.5, k: "p_hdiso" }, gyp: { name: "1/2 in gypsum cover board", r: 0.5, k: "p_gyp" } };

  function up(x) { return x > 0 ? Math.ceil(x - 1e-9) : 0; }
  function pos(x) { return isFinite(x) && x > 0 ? x : 0; }
  function mid(s) { return Math.round((s.lo + s.hi) / 2 * 100) / 100; }

  REP.tool({
    id: "flat-roof-calculator",
    name: "Flat & Commercial Roof Calculator",
    rowDefaults: { sections: [{ name: "Main roof", l: 120, w: 80, a: 0 }] },
    init: function (form, run) {
      // Changing the system refills its midpoint price, roll size and coating defaults.
      form.querySelector('[name="system"]').addEventListener("change", function (e) {
        var s = SYS[e.target.value] || SYS.tpo_ma;
        function set(n, val) { var el = form.querySelector('[name="' + n + '"]'); if (el) el.value = val; }
        set("sys_price", mid(s));
        if (s.roll) { set("roll_w", s.roll[0]); set("roll_l", s.roll[1]); }
        if (s.mils) { set("mils", s.mils); set("solids", s.solids); }
        run();
      });
    },
    compute: function (v) {
      var s = SYS[v.system] || SYS.tpo_ma, coat = s.att === "coat";
      var field = 0, secLines = [];
      (v.rows.sections || []).forEach(function (r, i) {
        var a = pos(r.a) || pos(r.l) * pos(r.w);
        if (!a) return;
        field += a;
        secLines.push((r.name || "Section " + (i + 1)) + ": " + N(Math.round(a), 0) + " sq ft" + (pos(r.a) ? "" : " (" + pos(r.l) + " × " + pos(r.w) + " ft)"));
      });
      if (!(field > 0)) return { warnings: ["Enter at least one roof section (length × width, or an area)."] };

      var warnings = [], notes = [], rows = [], groups = { sys: 0, ins: 0, tear: 0, det: 0 };
      var reg = REP.region(v.region).factor, ls = Math.min(100, pos(v.lab_share)) / 100;
      var adj = 1 - ls + ls * reg;
      var flash = pos(v.par_lf) && pos(v.par_h) ? pos(v.par_lf) * (pos(v.par_h) + 1) : 0;
      var memSf = field + flash, sq = field / 100;

      function line(g, item, qty, unit, cost) {
        rows.push([item, qty, unit, cost == null ? "incl." : M(cost)]);
        if (cost) groups[g] += cost;
      }

      // ----- System -----
      var sysCost = memSf * pos(v.sys_price) * adj;
      line("sys", s.name + (flash ? " (incl. " + N(Math.round(flash), 0) + " sf wall flashing)" : ""), N(Math.round(memSf), 0), "sq ft", sysCost);

      var rollsTxt = "", R = 0, layers = 0, thick = 0;
      if (coat) {
        var solids = Math.min(100, Math.max(1, v.solids)) / 100;
        var gal = memSf * pos(v.mils) / (1604 * solids), pails = up(gal / 5);
        line("sys", "Coating, " + v.mils + " dry mils at " + Math.round(solids * 100) + "% solids (" + N(Math.round(gal), 0) + " gal)", N(pails, 0), "5-gal pails", null);
        rollsTxt = pails + " pails";
        var wet = field * Math.min(100, pos(v.wet_pct)) / 100;
        if (wet) line("ins", "Cut out & replace wet insulation (" + v.wet_pct + "%)", N(Math.round(wet), 0), "sq ft", wet * pos(v.wet_price) * adj);
        if (v.wet_pct > 25) warnings.push("With more than about 25% of the insulation wet, a coating usually isn't worth it. Price a tear-off and new membrane instead.");
        notes.push("Coatings go over the existing roof, so tear-off and new insulation are not included. Clean, prime where the manufacturer requires it, and reinforce seams and flashings with fabric.");
      } else {
        var rollSf = pos(v.roll_w) * pos(v.roll_l);
        var rolls = rollSf ? up(memSf * s.plies * (1 + pos(v.overlap) / 100) / rollSf) : 0;
        line("sys", "Membrane rolls, " + v.roll_w + " × " + v.roll_l + " ft" + (s.plies > 1 ? " (" + s.plies + " plies)" : ""), N(rolls, 0), "rolls", null);
        rollsTxt = rolls + " rolls";
        if (s.att === "ma") {
          var nw = Math.max(1, pos(v.roll_w) - 0.5);
          var mf = up(field / nw * (12 / Math.max(3, v.ma_spacing)) * (1 + pos(v.perim_pct) / 100));
          line("sys", "Seam fasteners & plates (" + v.ma_spacing + " in o.c., half sheets at perimeter)", N(mf, 0), "each", null);
        } else if (s.att === "fa") {
          var ag = memSf / Math.max(1, v.adh_cov);
          line("sys", "Bonding adhesive (" + N(Math.round(ag), 0) + " gal at " + v.adh_cov + " sf/gal)", N(up(ag / 5), 0), "5-gal pails", null);
        } else if (s.att === "mb") notes.push("Mod-bit plies are torch-applied, set in cold adhesive (roughly 1.5–2 gal per square per ply) or self-adhered over primer.");
        else notes.push("BUR plies are set in hot asphalt (or cold adhesive) with a flood coat and gravel or a cap sheet.");

        // ----- Tear-off -----
        var tl = Math.max(0, Math.round(v.layers));
        if (tl) line("tear", "Tear-off & disposal, " + tl + " layer" + (tl > 1 ? "s" : ""), N(Math.round(field), 0), "sq ft", field * tl * pos(v.tear_price) * reg);

        // ----- Insulation -----
        layers = Math.max(0, Math.round(v.ins_layers)); thick = pos(v.ins_in);
        var boardSf = Math.max(1, v.board_sf), perLayer = up(field * 1.03 / boardSf);
        if (layers && thick) {
          R += layers * thick * pos(v.ins_r);
          line("ins", "Polyiso insulation, " + layers + " × " + thick + " in (" + N(perLayer * layers, 0) + " boards)", N(Math.round(field), 0), "sq ft",
            field * layers * thick * pos(v.ins_price) * adj);
        }
        var cv = COVER[v.cover], coverBoards = cv ? up(field * 1.03 / boardSf) : 0;
        if (cv) {
          R += cv.r;
          line("ins", cv.name + " (" + N(coverBoards, 0) + " boards)", N(Math.round(field), 0), "sq ft", field * pos(v[cv.k]) * adj);
        }
        if (v.tapered) line("ins", "Tapered insulation system (average)", N(Math.round(field), 0), "sq ft", field * pos(v.p_taper) * adj);
        var fastened = coverBoards || (layers && thick ? perLayer : 0);
        if (fastened && s.att !== "bur") {
          var pp = Math.min(100, pos(v.perim_pct)) / 100;
          var fpb = (1 - pp) * pos(v.fpb) + pp * pos(v.fpb_perim);
          var nf = up(fastened * fpb);
          var flen = Math.ceil(layers * thick + (cv ? 0.5 : 0) + 1);
          line("ins", "Insulation fasteners, ~" + flen + " in, with 3 in plates (" + N(fpb, 1) + " per board)", N(nf, 0), "each", null);
        }
        if (tl === 0) notes.push("Recover over an existing roof: most codes allow only one recover layer, and the existing roof must be dry. Many owners still core-cut first.");
        if (tl && R < 25) notes.push("A full tear-off usually triggers the energy code's insulation requirement: about R-25 continuous above the deck in most of Texas, R-30 in the Panhandle. This build is R-" + N(R, 1) + ".");
      }

      // ----- Details -----
      if (v.drains) line("det", "Drains & scuppers (re-flash / new inserts)", N(v.drains, 0), "each", v.drains * pos(v.p_drain) * adj);
      if (v.pens) line("det", "Penetration flashings", N(v.pens, 0), "each", v.pens * pos(v.p_pen) * adj);
      if (v.crickets) line("det", "Crickets", N(v.crickets, 0), "each", v.crickets * pos(v.p_cricket) * adj);
      if (v.edge_lf) line("det", "Edge metal", N(v.edge_lf, 0), "ln ft", v.edge_lf * pos(v.p_edge) * adj);
      if (v.coping && v.par_lf) line("det", "Coping cap", N(v.par_lf, 0), "ln ft", v.par_lf * pos(v.p_coping) * adj);

      var total = groups.sys + groups.ins + groups.tear + groups.det;
      var lo = total - memSf * (pos(v.sys_price) - s.lo) * adj, hi = total + memSf * (s.hi - pos(v.sys_price)) * adj;

      if (pos(v.par_lf) && !v.drains) warnings.push("Parapet walls with no drains or scuppers will hold water. Count every drain, scupper and overflow.");
      if (v.sys_price < s.lo * 0.8 || v.sys_price > s.hi * 1.2) notes.push("Your system price is outside the typical Texas range of $" + s.lo.toFixed(2) + "–$" + s.hi.toFixed(2) + "/sf.");
      if (v.system === "acrylic") notes.push("Acrylic coatings should not be used where water ponds. Silicone handles ponding better.");
      if (reg !== 1) notes.push("Labor share (" + Math.round(ls * 100) + "%) adjusted ×" + reg.toFixed(2) + " for " + REP.region(v.region).name + ".");
      notes.push("New low-slope roofs need at least 1/4 in per foot of slope; tapered insulation and crickets fix ponding.");

      return {
        headline: { label: "Estimated installed cost", value: total, format: "money",
          sub: M(total / field, 2) + "/sf · typical range " + M(lo) + " – " + M(hi) },
        kpis: [
          { label: "Roof area", text: N(Math.round(field), 0) + " sq ft (" + N(sq, 1) + " sq)" },
          { label: "Cost per sq ft", value: total / field, format: "money2" },
          { label: coat ? "Coating" : "Insulation R-value", text: coat ? rollsTxt : "R-" + N(R, 1) },
          { label: coat ? "Gallons per square" : "Membrane", text: coat ? N(pos(v.mils) * 100 / (1604 * Math.max(0.01, v.solids / 100)), 2) : rollsTxt }
        ],
        breakdown: { title: "Where the money goes", items: [
          { label: coat ? "Coating system" : "Membrane system", value: groups.sys },
          { label: coat ? "Wet insulation repair" : "Insulation & cover board", value: groups.ins },
          { label: "Tear-off", value: groups.tear },
          { label: "Drains, flashings & metal", value: groups.det }
        ] },
        table: { title: "Line items & quantities", head: ["Item", "Qty", "Unit", "Cost"], rows: rows, foot: ["Total installed", "", "", M(total)] },
        warnings: warnings,
        notes: notes,
        summary: [
          "System: " + s.name + " at " + M(v.sys_price, 2) + "/sf installed",
          "Roof area: " + Math.round(field) + " sq ft (" + sq.toFixed(1) + " squares); membrane incl. flashing " + Math.round(memSf) + " sq ft"
        ].concat(secLines)
          .concat(["Parapets " + pos(v.par_lf) + " ln ft × " + pos(v.par_h) + " ft; edge metal " + pos(v.edge_lf) + " ln ft",
            coat ? "Coating: " + v.mils + " dry mils, " + v.solids + "% solids, " + rollsTxt + "; wet insulation " + v.wet_pct + "%"
              : "Tear-off " + v.layers + " layer(s); insulation " + layers + " × " + thick + " in polyiso + " + (COVER[v.cover] ? COVER[v.cover].name : "no cover board") + " = R-" + R.toFixed(1) + "; " + rollsTxt,
            "Drains/scuppers " + v.drains + ", penetrations " + v.pens + ", crickets " + v.crickets,
            "Location: " + REP.region(v.region).name,
            "Estimated installed cost: " + M(total) + " (" + M(total / field, 2) + "/sf; range " + M(lo) + "–" + M(hi) + ")"])
      };
    }
  });
})();
