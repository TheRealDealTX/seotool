/* Attic Ventilation Calculator */
(function () {
  "use strict";
  var N = REP.num, TEAL = "#1fa59e", PEACH = "#FCBE8E", INK = "#cfdddb", MUTED = "#8ba29f";
  var EXH = { ridge: "Ridge vent", box: "Box / static vents", turbine: "Turbine vents", power: "Power attic fan" };
  var INT = { soffit: "Continuous soffit vent", soffit_ind: "Individual soffit vents", edge: "Edge / fascia intake" };

  function si(n) { return N(Math.round(n), 0) + " sq in"; }
  function t(x, y, s, o) {
    o = o || {};
    return '<text x="' + x + '" y="' + y + '" fill="' + (o.fill || INK) + '" font-size="' + (o.size || 21) +
      '" font-family="Inter,system-ui,sans-serif" text-anchor="' + (o.anchor || "middle") + '" font-weight="600">' + REP.esc(s) + "</text>";
  }
  function arrow(x1, y1, x2, y2, c, w) {
    var a = Math.atan2(y2 - y1, x2 - x1), hl = 10 + w;
    var p1 = [x2 - hl * Math.cos(a - 0.5), y2 - hl * Math.sin(a - 0.5)], p2 = [x2 - hl * Math.cos(a + 0.5), y2 - hl * Math.sin(a + 0.5)];
    return '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="' + c + '" stroke-width="' + w + '" stroke-linecap="round"/>' +
      '<polygon points="' + x2 + "," + y2 + " " + p1[0].toFixed(1) + "," + p1[1].toFixed(1) + " " + p2[0].toFixed(1) + "," + p2[1].toFixed(1) + '" fill="' + c + '"/>';
  }
  function figure(intake, exhaust, exLabel, inLabel) {
    var tot = intake + exhaust || 1, wi = 2 + 8 * intake / tot, we = 2 + 8 * exhaust / tot;
    var s = '<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg" role="img">';
    // roof + ceiling
    s += '<polygon points="40,175 300,55 560,175" fill="rgba(31,165,158,.10)" stroke="' + TEAL + '" stroke-width="3" stroke-linejoin="round"/>';
    s += '<line x1="80" y1="175" x2="520" y2="175" stroke="' + MUTED + '" stroke-width="2"/>';
    s += '<line x1="80" y1="175" x2="80" y2="230" stroke="' + MUTED + '" stroke-width="2"/><line x1="520" y1="175" x2="520" y2="230" stroke="' + MUTED + '" stroke-width="2"/>';
    // airflow
    s += '<path d="M95 165 Q 200 140 285 80" fill="none" stroke="' + TEAL + '" stroke-dasharray="4 6" stroke-width="2"/>';
    s += '<path d="M505 165 Q 400 140 315 80" fill="none" stroke="' + TEAL + '" stroke-dasharray="4 6" stroke-width="2"/>';
    s += arrow(30, 200, 72, 180, TEAL, wi) + arrow(570, 200, 528, 180, TEAL, wi);
    s += arrow(300, 60, 300, 18, PEACH, we);
    s += t(318, 32, "exhaust " + si(exhaust), { anchor: "start", fill: PEACH });
    s += t(300, 210, "intake " + si(intake) + " (both eaves)", { fill: TEAL });
    s += t(300, 240, inLabel + "  ·  " + exLabel, { size: 17, fill: MUTED });
    return s + "</svg>";
  }

  REP.tool({
    id: "attic-ventilation-calculator",
    name: "Attic Ventilation Calculator",
    compute: function (v) {
      var warnings = [], notes = [], rows = [];
      var A = v.area_mode === "dims" ? Math.max(0, v.att_len) * Math.max(0, v.att_wid) : v.attic_sqft;
      if (!(A > 0)) return { warnings: ["Enter the attic floor area (or its length and width) to size the vents."] };
      if (A > 20000) warnings.push("That is a very large attic. Large or commercial attics are often split into separate vented spaces; size each one on its own.");

      var ip = Math.min(100, Math.max(0, v.intake_pct)) / 100, ep = 1 - ip, rule = +v.rule || 150;
      if (rule === 300 && (ep < 0.4 - 1e-9 || ep > 0.5 + 1e-9)) {
        warnings.push("The 1/300 ratio only applies when 40–50% of the vent area is exhaust high on the roof. Your split puts " +
          Math.round(ep * 100) + "% in exhaust, so the calculator used 1/150.");
        rule = 150;
      }
      var total = A * 144 / rule, intake = total * ip, exhaust = total * ep;
      if (ip < 0.5) warnings.push("Intake is less than exhaust. Intake should be at least equal to exhaust, or the exhaust vents will pull air from the house or from each other.");

      var spec = function (k) { return Math.max(0, v[k]); };
      var exQty = "", exProvided = 0, exNeedTxt, inQty, inProvided, exKpi, ridgeKpi = null, fanCfm = 0;

      // ----- exhaust -----
      if (v.exhaust === "ridge") {
        var nfa = spec("ridge_nfa");
        if (!nfa) return { warnings: ["Enter the ridge vent's net free area per foot in the vent specs."] };
        var lf = Math.ceil(exhaust / nfa - 1e-9);
        exProvided = lf * nfa; exQty = lf + " ft"; exKpi = lf + " ft of ridge vent";
        rows.push(["Ridge vent", N(nfa, 1) + "/ft", exQty, si(exProvided)]);
        if (v.ridge_len > 0) {
          if (lf > v.ridge_len) {
            var short = lf - v.ridge_len, maxEx = v.ridge_len * nfa;
            warnings.push("The ridge is " + N(short, 0) + " ft too short: " + v.ridge_len + " ft of this vent supplies " + si(maxEx) + " of the " + si(exhaust) +
              " needed. It would take a vent rated about " + N(Math.ceil(exhaust / v.ridge_len * 10) / 10, 1) + " sq in/ft. If no ridge vent that size fits, switch the whole attic to box vents or turbines; do not add them alongside the ridge vent.");
            ridgeKpi = { label: "Ridge check", text: "Short " + N(short, 0) + " ft" };
          } else ridgeKpi = { label: "Ridge check", text: lf + " of " + N(v.ridge_len, 0) + " ft used" };
        } else notes.push("Enter the ridge length to check that it can hold the ridge vent you need.");
      } else if (v.exhaust === "box" || v.exhaust === "turbine") {
        var each = spec(v.exhaust === "box" ? "box_nfa" : "turbine_nfa");
        if (!each) return { warnings: ["Enter the NFA per vent in the vent specs."] };
        var n = Math.ceil(exhaust / each - 1e-9);
        exProvided = n * each; exQty = n + ""; exKpi = n + " " + (v.exhaust === "box" ? "box vents" : "turbines");
        rows.push([EXH[v.exhaust], N(each, 0) + " each", exQty, si(exProvided)]);
        notes.push("Place " + (v.exhaust === "box" ? "box vents" : "turbines") + " high on the rear slope, within 3 ft (vertically) of the ridge, spread along its length.");
      } else {
        var perSf = spec("cfm_per_sf"), fan = spec("fan_cfm");
        fanCfm = A * perSf;
        var fans = fan > 0 ? Math.ceil(fanCfm / fan - 1e-9) : 0;
        exKpi = fan > 0 ? fans + " fan" + (fans > 1 ? "s" : "") + " (" + N(Math.round(fanCfm), 0) + " CFM)" : N(Math.round(fanCfm), 0) + " CFM";
        exQty = fans ? fans + "" : "—"; exProvided = 0;
        rows.push(["Power attic fan", fan ? N(fan, 0) + " CFM" : "—", exQty, N(Math.round(fans * fan), 0) + " CFM"]);
        notes.push("Power fans are sized in airflow (CFM), not net free area, so they are not counted toward the code NFA here. " +
          "Sizing uses " + perSf + " CFM per sq ft of attic floor; add 15–20% for dark shingles or a steep roof, per most fan makers.");
        notes.push("Do not run a power fan with a ridge vent, box vents or turbines on the same attic. Close or remove the passive exhaust.");
        if (!fan) warnings.push("Enter the fan's CFM rating to get a fan count.");
        var cfmIntake = fanCfm / Math.max(1, v.cfm_per_intake) * 144;
        if (cfmIntake > intake) {
          notes.push("A " + N(Math.round(fanCfm), 0) + " CFM fan needs about " + si(cfmIntake) + " of intake (1 sq ft per " + v.cfm_per_intake + " CFM), more than the code split. Intake below is sized to the fan.");
          intake = cfmIntake;
        }
      }

      // ----- intake ----- (balanced or intake-heavy: never let rounding leave intake below exhaust)
      if (v.exhaust !== "power" && ip >= 0.5) intake = Math.max(intake, exProvided);
      if (v.intake === "soffit" || v.intake === "edge") {
        var pf = spec(v.intake === "soffit" ? "soffit_nfa" : "edge_nfa");
        if (!pf) return { warnings: ["Enter the intake vent's NFA per foot in the vent specs."] };
        var ilf = Math.ceil(intake / pf - 1e-9);
        inProvided = ilf * pf; inQty = ilf + " ft";
        rows.push([INT[v.intake], N(pf, 1) + "/ft", inQty, si(inProvided)]);
        if (v.eave_len > 0 && ilf > v.eave_len) warnings.push("You need " + ilf + " ft of intake but entered " + v.eave_len + " ft of eave. Use a higher-NFA intake product, add edge intake vents, or combine soffit and edge intake (mixing intake types is fine).");
      } else {
        var ie = spec("soffit_ind_nfa");
        if (!ie) return { warnings: ["Enter the NFA per soffit vent in the vent specs."] };
        var ni = Math.ceil(intake / ie - 1e-9);
        inProvided = ni * ie; inQty = ni + "";
        rows.push(["Individual soffit vents", N(ie, 0) + " each", inQty, si(inProvided)]);
        notes.push("Split the soffit vents evenly between the eaves on both sides, between rafter bays, and keep insulation baffles in those bays.");
      }

      var inKpi = v.intake === "soffit_ind" ? inQty + " soffit vents" : inQty + " of " + (v.intake === "soffit" ? "soffit vent" : "edge vent");
      if (v.exhaust !== "power" && inProvided < exProvided) warnings.push("As rounded, intake (" + si(inProvided) + ") is below exhaust (" + si(exProvided) + "). Add intake until it at least matches.");

      var kpis = [
        { label: "Total NFA required", text: N(total / 144, 2) + " sq ft" },
        { label: "Ratio used", text: "1/" + rule },
        v.exhaust === "power" ? { label: "Fan airflow needed", text: N(Math.round(fanCfm), 0) + " CFM" } : { label: "Exhaust NFA (" + Math.round(ep * 100) + "%)", text: si(exhaust) },
        { label: "Intake NFA" + (v.exhaust === "power" ? "" : " (" + Math.round(ip * 100) + "%)"), text: si(intake) },
        { label: "Exhaust needed", text: exKpi },
        { label: "Intake needed", text: inKpi }
      ];
      if (ridgeKpi) kpis.push(ridgeKpi);
      notes.push("Use one type of exhaust per attic space. Mixing ridge vents with box vents, turbines, gable vents or fans short-circuits the airflow.");
      if (rule === 300 && v.exhaust !== "power") notes.push("1/300 assumes the exhaust is within 3 ft of the ridge (vertically) and the intake is in the lower third of the attic. Check local code for the edition your city enforces.");

      var foot = v.exhaust === "power" ? ["Intake provided", "", "", si(inProvided)] : ["Total provided", "", "", si(exProvided + inProvided)];
      return {
        headline: { label: "Net free area required (sq in)", value: Math.round(total), format: "int",
          sub: N(total / 144, 2) + " sq ft at 1/" + rule + " for " + N(Math.round(A), 0) + " sq ft of attic" },
        figure: figure(intake, v.exhaust === "power" ? 0 : exhaust, v.exhaust === "power" ? "Power fan " + N(Math.round(fanCfm), 0) + " CFM" : exKpi, inKpi),
        kpis: kpis,
        warnings: warnings,
        table: { title: "Vents to install", head: ["Vent", "NFA", "Qty", "Provides"], rows: rows, foot: foot },
        notes: notes,
        summary: [
          "Attic floor area: " + Math.round(A) + " sq ft; ratio 1/" + rule + " (IRC R806.2)",
          "Required NFA: " + Math.round(total) + " sq in (" + (total / 144).toFixed(2) + " sq ft); intake " + Math.round(intake) + " sq in, exhaust " + (v.exhaust === "power" ? Math.round(fanCfm) + " CFM fan" : Math.round(exhaust) + " sq in"),
          "Exhaust: " + EXH[v.exhaust] + " — " + exKpi,
          "Intake: " + INT[v.intake] + " — " + inKpi
        ]
      };
    }
  });
})();
