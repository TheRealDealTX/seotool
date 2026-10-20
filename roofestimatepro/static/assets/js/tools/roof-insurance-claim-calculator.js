/* Roof Insurance Claim Calculator */
(function () {
  "use strict";
  var D = REP.data, M = REP.money;

  var LOW = { tpo: ["TPO membrane", 22], pvc: ["PVC membrane", 27], epdm: ["EPDM membrane", 27], modbit: ["Modified bitumen", 17],
    bur: ["Built-up roof (BUR)", 25], silicone: ["Silicone coating", 12], acrylic: ["Acrylic coating", 10] };
  function mat(key) {
    if (LOW[key]) return { key: key, name: LOW[key][0], life: LOW[key][1] };
    var all = D.materials || [];
    for (var i = 0; i < all.length; i++) if (all[i].key === key) return all[i];
    return all[0] || { key: key, name: key, life: 30 };
  }
  function schedPct(v) {
    var a = Math.max(0, v.age);
    var p = a < 3 ? v.sch1 : a < 6 ? v.sch2 : a < 9 ? v.sch3 : a < 12 ? v.sch4 : a < 15 ? v.sch5 : v.sch6;
    return Math.min(100, Math.max(0, p));
  }
  var SETTLE = { rcv: "Replacement cost (depreciation recoverable)", acv: "Actual cash value on the roof (depreciation not recoverable)", schedule: "Roof payment schedule" };

  REP.tool({
    id: "roof-insurance-claim-calculator",
    name: "Roof Insurance Claim Calculator",
    init: function (form, run) {
      form.querySelector('[name="material"]').addEventListener("change", function (e) {
        form.querySelector('[name="life"]').value = mat(e.target.value).life;
        run();
      });
    },
    compute: function (v) {
      var build = v.rcv_mode === "build";
      var roofLI = build ? Math.max(0, v.squares) * Math.max(0, v.rcv_sq) : Math.max(0, v.rcv_direct);
      var others = build ? [["Gutters & downspouts", v.gutters], ["Fence", v.fence], ["Interior", v.interior], ["Other items", v.other]] : [];
      var otherLI = others.reduce(function (a, o) { return a + Math.max(0, o[1]); }, 0);
      var LI = roofLI + otherLI;
      if (LI <= 0) return { warnings: ["Enter the roof's replacement cost, or its squares and price per square, to see the claim breakdown."] };

      var ms = Math.min(100, Math.max(0, v.mat_share)) / 100, tr = Math.max(0, v.tax_rate) / 100;
      var tax = LI * ms * tr;
      var ovh = v.op ? LI * Math.max(0, v.ovh) / 100 : 0, prf = v.op ? LI * Math.max(0, v.prf) / 100 : 0, op = ovh + prf;
      var RCV = LI + tax + op;
      var roofRCV = RCV * roofLI / LI, otherRCV = RCV - roofRCV;

      // Depreciation rate
      var m = mat(v.material), d, depNote = "";
      if (v.dep_mode === "pct") { d = Math.min(100, Math.max(0, v.dep_pct)) / 100; depNote = REP.pct(d * 100) + " (entered)"; }
      else {
        if (!(v.life > 0)) return { warnings: ["Enter a life expectancy greater than zero."] };
        var cap = v.cap > 0 ? Math.min(100, v.cap) / 100 : 1;
        var raw = Math.max(0, v.age) / v.life;
        d = Math.min(cap, raw);
        depNote = REP.num(v.age, 1) + " of " + v.life + " yrs" + (raw > cap ? ", capped at " + REP.pct(cap * 100, 0) : "");
      }
      // Share of RCV that depreciation applies to
      var base = v.dep_base === "materials" ? (LI * ms + tax + op * ms) / RCV : 1;
      function dep(x) { return x * base * d; }

      var rec = 0, nonrec = 0, schedP = null, notes = [], warnings = [];
      if (v.settle === "rcv") rec = dep(RCV);
      else if (v.settle === "acv") { nonrec = dep(roofRCV); rec = dep(otherRCV); }
      else { schedP = schedPct(v); nonrec = roofRCV * (1 - schedP / 100); rec = dep(otherRCV); }
      var withheld = rec + nonrec, ACV = RCV - withheld;

      var ded = v.ded_mode === "pct" ? Math.max(0, v.cov_a) * Math.max(0, v.ded_pct) / 100 : Math.max(0, v.ded_flat);
      var prior = Math.max(0, v.prior);
      var covered = RCV - nonrec;                       // most the policy pays before deductible
      var insurerTotal = Math.max(0, covered - ded);    // total owed if all depreciation is recovered
      var first = Math.max(0, ACV - ded - prior);
      var holdback = Math.max(0, insurerTotal - prior - first);
      var dedApplied = Math.min(ded, covered);
      var oop = RCV - insurerTotal;                     // deductible + non-recoverable depreciation

      if (ded >= covered) warnings.push("The deductible (" + M(ded) + ") is at or above the covered amount on these numbers (" + M(covered) + "), so the carrier would owe nothing. Before deciding what to do, have the damage and the estimate checked (carrier and contractor estimates often miss items), and ask your agent how a claim may affect your policy.");
      else if (ACV - prior <= ded) warnings.push("The ACV does not clear the deductible, so the first check is $0. The remaining deductible comes out of the recoverable depreciation once the work is done.");
      if (prior > insurerTotal) warnings.push("Prior payments exceed what these inputs say is owed. Check the prior payment amount and the estimate.");

      if (!v.op) notes.push("O&P is off. At 10% + 10% it would add " + M(LI * 0.2) + " of RCV. It is commonly owed when a general contractor is reasonably needed, often with three or more trades. Check the claim facts and your policy.");
      else if (build && others.filter(function (o) { return o[1] > 0; }).length < 2) notes.push("O&P is on. Expect the carrier to ask why a general contractor is needed if the loss is mostly roof-only; document the trades involved.");
      if (v.settle === "rcv") notes.push("To collect the " + M(holdback) + " holdback, replace the roof within the policy's time limit and send the final invoice. Recovery is limited to what is actually spent.");
      if (v.settle === "acv") notes.push("With an ACV roof endorsement, the " + M(nonrec) + " of roof depreciation is not paid back. Depreciation on non-roof items is still recoverable here; confirm with your endorsement.");
      if (v.settle === "schedule") notes.push("Schedule pays " + REP.pct(schedP, 0) + " of the roof RCV at age " + REP.num(v.age, 1) + ". Replace the defaults with the percentages in your policy's schedule for your roof type.");
      if (!build && v.settle !== "rcv") notes.push("With a single estimate total, the whole RCV is treated as roof. Use “Build it from squares” to separate gutters, fence and interior.");
      if (v.dep_base === "materials") notes.push("Depreciating materials only. Whether labor can be depreciated varies by state and policy; check yours.");
      notes.push("Texas Insurance Code ch. 707: a contractor may not waive, pay or rebate your " + M(ded) + " deductible.");
      notes.push("Want the carrier's estimate checked line by line? Our claim estimate review is $50 (roofestimatepro.com/claim/).");

      var rows = [];
      if (build) rows.push(["Roof", REP.num(v.squares, 1) + " sq × " + M(v.rcv_sq), M(roofLI)]);
      else rows.push(["Line-item total", "", M(roofLI)]);
      others.forEach(function (o) { if (o[1] > 0) rows.push([o[0], "", M(o[1])]); });
      rows.push(["Sales tax on materials", REP.pct(ms * 100, 0) + " × " + REP.pct(tr * 100, 2), M(tax)]);
      if (v.op) { rows.push(["Overhead", REP.pct(v.ovh, 0), M(ovh)]); rows.push(["Profit", REP.pct(v.prf, 0), M(prf)]); }
      rows.push(["Replacement cost value (RCV)", "", M(RCV)]);
      if (rec) rows.push(["Less recoverable depreciation", v.settle === "rcv" ? depNote : "non-roof items", "−" + M(rec)]);
      if (nonrec) rows.push(["Less non-recoverable depreciation", v.settle === "schedule" ? "schedule " + REP.pct(schedP, 0) : depNote, "−" + M(nonrec)]);
      rows.push(["Actual cash value (ACV)", "", M(ACV)]);
      rows.push(["Less deductible", v.ded_mode === "pct" ? REP.pct(v.ded_pct, 1) + " of " + M(v.cov_a) : "flat", "−" + M(dedApplied)]);
      if (prior) rows.push(["Less prior payments", "", "−" + M(prior)]);
      rows.push(["First payment", "", M(first)]);
      if (holdback) rows.push(["Plus depreciation released after repairs", "", M(holdback)]);

      return {
        headline: { label: "First payment (ACV − deductible − prior payments)", value: first, format: "money",
          sub: holdback > 0 ? "+ " + M(holdback) + " recoverable after the roof is replaced" : "No recoverable holdback on these inputs" },
        kpis: [
          { label: "Recoverable depreciation (holdback)", value: holdback, format: "money" },
          { label: "Total from insurer (incl. prior payments)", value: insurerTotal, format: "money" },
          { label: "Your out-of-pocket", value: oop, format: "money" },
          { label: "Replacement cost value", value: RCV, format: "money" },
          { label: "Depreciation withheld", text: M(withheld) + " (" + REP.pct(withheld / RCV * 100) + ")" },
          { label: "Deductible", value: ded, format: "money" }
        ],
        breakdown: { title: "How the RCV gets paid", items: [
          { label: "First payment", value: first },
          { label: "Recoverable holdback", value: holdback },
          { label: "Prior payments", value: Math.min(prior, insurerTotal) },
          { label: "Deductible (you)", value: dedApplied },
          { label: "Non-recoverable depreciation (you)", value: nonrec }
        ] },
        warnings: warnings,
        table: { title: "Claim summary", head: ["Item", "Basis", "Amount"], rows: rows, foot: ["Total from insurer", "", M(insurerTotal)] },
        notes: notes,
        summary: [
          "RCV: " + M(RCV) + " (line items " + M(LI) + ", tax " + M(tax) + (v.op ? ", O&P " + M(op) : ", no O&P") + ")",
          "Settlement: " + SETTLE[v.settle] + (schedP != null ? " at " + schedP + "%" : ""),
          "Depreciation: " + (v.dep_mode === "age" ? m.name + ", " : "") + depNote + (v.dep_base === "materials" ? ", materials only" : ", all line items") + " = " + M(withheld) + " withheld",
          "ACV: " + M(ACV),
          "Deductible: " + M(ded) + (v.ded_mode === "pct" ? " (" + v.ded_pct + "% of " + M(v.cov_a) + " Coverage A)" : ""),
          "Prior payments: " + M(prior),
          "First payment: " + M(first) + "; recoverable holdback: " + M(holdback),
          "Total from insurer: " + M(insurerTotal) + "; homeowner out-of-pocket: " + M(oop)
        ]
      };
    }
  });
})();
