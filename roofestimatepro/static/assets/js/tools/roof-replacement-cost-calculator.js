/* Roof Replacement Cost Calculator */
(function () {
  "use strict";
  var D = REP.data, M = REP.money;

  function mat(key) { return D.materials.filter(function (m) { return m.key === key; })[0] || D.materials[0]; }
  function steepAdj(r) { return r > 12 ? 0.45 : r >= 11 ? 0.30 : r >= 9 ? 0.20 : r >= 7 ? 0.10 : 0; }
  var STORY = { 1: 0, 2: 0.08, 3: 0.15 };
  var CPLX = { simple: 0, moderate: 0.05, complex: 0.12 };
  var EXISTING = { asphalt: 1, shake: 1.4, metal: 1.3, tile: 1.8 };

  REP.tool({
    id: "roof-replacement-cost-calculator",
    name: "Roof Replacement Cost Calculator",
    init: function (form, run) {
      // Changing the material refills its default unit prices.
      form.querySelector('[name="material"]').addEventListener("change", function (e) {
        var m = mat(e.target.value);
        form.querySelector('[name="mat_price"]').value = m.mat;
        form.querySelector('[name="acc_price"]').value = m.acc;
        form.querySelector('[name="lab_price"]').value = m.lab;
        run();
      });
    },
    compute: function (v) {
      var m = mat(v.material), rise = v.pitch, pf = REP.pitchFactor(rise);
      var roofSf;
      if (v.area_mode === "known") roofSf = Math.max(0, v.roof_sqft);
      else {
        var perim = 4 * Math.sqrt(Math.max(0, v.footprint));
        roofSf = (v.footprint + perim * (v.overhang / 12)) * pf;
      }
      if (roofSf <= 0) return { warnings: ["Enter a roof area or footprint to see an estimate."] };

      var wastePct = (D.waste[m.waste] || D.waste.shingle)[v.complexity] / 100;
      var sq = roofSf / 100, sqOrder = sq * (1 + wastePct);
      var reg = REP.region(v.region).factor;
      var steep = steepAdj(rise), story = STORY[v.stories] || 0, cplx = CPLX[v.complexity] || 0;
      var laborMult = (1 + steep) * (1 + story) * (1 + cplx) * reg;

      var product = sqOrder * v.mat_price;
      var acc = sq * v.acc_price;
      var materials = product + acc;
      var tax = materials * v.tax / 100;
      var labor = sq * v.lab_price * laborMult;
      var tear = v.layers > 0 ? sq * (v.tear1 + (v.layers - 1) * v.tear_add) * (EXISTING[v.existing] || 1) * (1 + steep) * (1 + story) * reg : 0;
      var sheets = Math.ceil(roofSf * v.deck_pct / 100 / 32);
      var deck = sheets * v.deck_price * reg;
      var extras = v.skylights * v.sky_price + v.chimneys * v.chim_price + v.gutter_lf * v.gutter_price;
      var sub = materials + tax + labor + tear + deck + extras;
      var op = sub * v.op / 100;
      var total = sub + op + v.permit;

      var rows = [
        [m.name, REP.num(sqOrder, 1) + " sq", M(product)],
        ["Accessories (underlayment, starter, ridge, drip edge, vents)", REP.num(sq, 1) + " sq", M(acc)],
        ["Sales tax on materials (" + v.tax + "%)", "", M(tax)],
        ["Install labor" + (laborMult !== 1 ? " (×" + laborMult.toFixed(2) + ")" : ""), REP.num(sq, 1) + " sq", M(labor)]
      ];
      if (tear) rows.push(["Tear-off & disposal, " + v.layers + " layer" + (v.layers > 1 ? "s" : ""), REP.num(sq, 1) + " sq", M(tear)]);
      if (sheets) rows.push(["Decking replacement", sheets + " sheets", M(deck)]);
      if (v.skylights) rows.push(["Skylight re-flash", v.skylights, M(v.skylights * v.sky_price)]);
      if (v.chimneys) rows.push(["Chimney re-flash", v.chimneys, M(v.chimneys * v.chim_price)]);
      if (v.gutter_lf) rows.push(["Seamless gutters", v.gutter_lf + " lf", M(v.gutter_lf * v.gutter_price)]);
      rows.push(["Overhead & profit (" + v.op + "%)", "", M(op)]);
      if (v.permit) rows.push(["Permit & inspection", "", M(v.permit)]);

      var notes = [];
      if (rise < 3 && m.waste === "shingle") notes.push("Shingles need at least 2/12 pitch (4/12 for standard underlayment). Below that, price a low-slope system with the flat roof calculator.");
      if (m.key === "arch") notes.push("Upgrading to Class 4 impact-resistant shingles here would add about " + M(sqOrder * (mat("class4").mat - m.mat) * 1.2 * (1 + v.tax / 100)) + ". Ask your insurer about the premium discount.");
      if (v.region === "houston") notes.push("Inside the TWIA catastrophe area, the roof must be installed and inspected to windstorm code (WPI-8). Budget for 6-nail or high-wind installation.");
      if (v.deck_pct >= 50) notes.push("At this level of decking replacement, ask for a full re-deck price; it is often cheaper per sheet.");

      return {
        headline: { label: "Estimated replacement cost", value: total, format: "money",
          sub: "Typical range " + M(total * 0.9) + " – " + M(total * 1.15) },
        kpis: [
          { label: "Roof area", text: REP.num(Math.round(roofSf), 0) + " sq ft" },
          { label: "Squares to order (" + Math.round(wastePct * 100) + "% waste)", text: REP.num(sqOrder, 1) },
          { label: "Cost per square", value: total / sq, format: "money" },
          { label: "Cost per sq ft of roof", value: total / roofSf, format: "money2" }
        ],
        breakdown: { title: "Where the money goes", items: [
          { label: "Materials + tax", value: materials + tax },
          { label: "Install labor", value: labor },
          { label: "Tear-off & disposal", value: tear },
          { label: "Decking", value: deck },
          { label: "Extras", value: extras },
          { label: "Overhead & profit", value: op },
          { label: "Permit", value: v.permit }
        ] },
        table: { title: "Line items", head: ["Item", "Qty", "Amount"], rows: rows, foot: ["Total", "", M(total)] },
        notes: notes,
        summary: [
          "Material: " + m.name,
          "Roof area: " + Math.round(roofSf) + " sq ft (" + sq.toFixed(1) + " squares, " + Math.round(wastePct * 100) + "% waste), pitch " + rise + "/12, " + v.stories + " stor" + (v.stories > 1 ? "ies" : "y") + ", " + v.complexity + " roof",
          "Location: " + REP.region(v.region).name,
          "Tear-off: " + v.layers + " layer(s) of " + v.existing + "; decking " + v.deck_pct + "%",
          "Estimated total: " + M(total) + " (range " + M(total * 0.9) + "–" + M(total * 1.15) + ")"
        ]
      };
    }
  });
})();
