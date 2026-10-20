/* Roof Depreciation Calculator */
(function () {
  "use strict";
  var D = REP.data, M = REP.money;

  // Low-slope systems (lives = midpoint of the shared-brief range; price = midpoint $/sf × 100).
  var LOW = [
    { key: "tpo", name: "TPO membrane (60-mil)", life: 22, sq: 850 },
    { key: "pvc", name: "PVC membrane (60-mil)", life: 27, sq: 1100 },
    { key: "epdm", name: "EPDM membrane (60-mil)", life: 27, sq: 875 },
    { key: "modbit", name: "Modified bitumen (2-ply)", life: 17, sq: 925 },
    { key: "bur", name: "Built-up roof (BUR)", life: 25, sq: 950 },
    { key: "silicone", name: "Silicone roof coating", life: 12, sq: 475 },
    { key: "acrylic", name: "Acrylic roof coating", life: 10, sq: 390 }
  ];
  var COND = { good: 10, average: 0, poor: -15 };
  var COND_NAME = { good: "well maintained", average: "average", poor: "poor / neglected" };

  function mat(key) {
    var all = (D.materials || []).map(function (m) { return { key: m.key, name: m.name, life: m.life, sq: Math.round((m.range[0] + m.range[1]) / 2), low: false }; })
      .concat(LOW.map(function (m) { return { key: m.key, name: m.name, life: m.life, sq: m.sq, low: true }; }));
    for (var i = 0; i < all.length; i++) if (all[i].key === key) return all[i];
    return all[0];
  }
  function yrs(t) {
    var y = Math.floor(t + 1e-9), m = Math.round((t - y) * 12);
    if (m === 12) { y++; m = 0; }
    return y + " yr" + (y === 1 ? "" : "s") + (m ? " " + m + " mo" : "");
  }

  function chart(rcv, eff, cap, age) {
    var W = 420, H = 230, L = 46, R = 12, T = 24, B = 24;
    var xMax = Math.max(1, Math.ceil(Math.max(eff, age) * 1.05));
    var hasR = rcv > 0, base = hasR ? rcv : 100;
    var raw = base / 4, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10)), f = raw / mag;
    var step = (f <= 1 ? 1 : f <= 2 ? 2 : f <= 2.5 ? 2.5 : f <= 5 ? 5 : 10) * mag, top = step * Math.ceil(base / step - 1e-9);
    function val(t) { return base * (1 - Math.min(cap, t / eff)); }
    function X(t) { return L + (t / xMax) * (W - L - R); }
    function Y(v) { return T + (1 - v / top) * (H - T - B); }
    var pts = [], steps = 120;
    for (var i = 0; i <= steps; i++) { var t = xMax * i / steps; pts.push(X(t).toFixed(1) + "," + Y(val(t)).toFixed(1)); }
    var g = [];
    for (var v = 0; v <= top + 1e-9; v += step) {
      var y = Y(v).toFixed(1);
      g.push('<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y + '" y2="' + y + '" stroke="rgba(255,255,255,.08)" stroke-width="1"/>');
      g.push('<text x="' + (L - 8) + '" y="' + (+y + 4) + '" text-anchor="end" font-size="12" fill="#8ba29f">' + (hasR ? (v >= 1000 ? "$" + REP.num(v / 1000) + "k" : "$" + Math.round(v)) : Math.round(v) + "%") + "</text>");
    }
    var tick = xMax <= 12 ? 2 : xMax <= 35 ? 5 : 10;
    for (var a = 0; a <= xMax; a += tick) g.push('<text x="' + X(a).toFixed(1) + '" y="' + (H - 6) + '" text-anchor="middle" font-size="12" fill="#8ba29f">' + a + "</text>");
    var ax = X(age), ay = Y(val(age)), lbl = hasR ? M(val(age)) : Math.round(val(age)) + "%";
    var anchor = ax > W * 0.7 ? "end" : "start", dx = anchor === "end" ? -12 : 12;
    var hover = [];
    for (var h = 0; h <= Math.min(xMax, 100); h++) hover.push('<circle cx="' + X(h).toFixed(1) + '" cy="' + Y(val(h)).toFixed(1) + '" r="7" fill="transparent"><title>Age ' + h + ": " + (hasR ? M(val(h)) : Math.round(val(h)) + "% of value") + "</title></circle>");
    return '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="' + (hasR ? "Actual cash value" : "Value remaining") + ' by roof age">' +
      '<text x="' + L + '" y="13" font-size="13" font-weight="600" fill="#c4d3d1">' + (hasR ? "ACV by roof age (years)" : "Value left (% of RCV) by roof age (years)") + "</text>" +
      g.join("") +
      '<polyline points="' + pts.join(" ") + '" fill="none" stroke="#1fa59e" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>' +
      '<line x1="' + ax.toFixed(1) + '" x2="' + ax.toFixed(1) + '" y1="' + T + '" y2="' + (H - B) + '" stroke="#FCBE8E" stroke-width="1" stroke-dasharray="3 3"/>' +
      '<circle cx="' + ax.toFixed(1) + '" cy="' + ay.toFixed(1) + '" r="6" fill="#FCBE8E" stroke="#0f1d1c" stroke-width="2"/>' +
      '<text x="' + (ax + dx).toFixed(1) + '" y="' + Math.max(T + 14, ay - 10).toFixed(1) + '" text-anchor="' + anchor + '" font-size="13" font-weight="700" fill="#fff">Now: ' + lbl + "</text>" +
      hover.join("") + "</svg>";
  }

  REP.tool({
    id: "roof-depreciation-calculator",
    name: "Roof Depreciation Calculator",
    init: function (form, run) {
      form.querySelector('[name="material"]').addEventListener("change", function (e) {
        var m = mat(e.target.value);
        form.querySelector('[name="life"]').value = m.life;
        form.querySelector('[name="rcv_sq"]').value = m.sq;
        run();
      });
      form.querySelectorAll('[name="condition"]').forEach(function (r) {
        r.addEventListener("change", function () {
          if (r.checked) { form.querySelector('[name="cond_adj"]').value = COND[r.value]; run(); }
        });
      });
    },
    compute: function (v) {
      var m = mat(v.material);
      if (!(v.life > 0)) return { warnings: ["Enter a life expectancy greater than zero."] };
      var age = Math.max(0, v.age_y) + Math.min(11, Math.max(0, v.age_m)) / 12;
      var adj = Math.max(-90, v.cond_adj);
      var eff = v.life * (1 + adj / 100);
      var cap = Math.min(100, Math.max(0, v.cap || 0)) / 100;
      if (v.cap <= 0) cap = 1;
      var raw = age / eff, dep = Math.min(cap, raw);
      var rcv = v.rcv_mode === "squares" ? Math.max(0, v.squares) * Math.max(0, v.rcv_sq) : v.rcv_mode === "dollars" ? Math.max(0, v.rcv) : 0;
      var depD = rcv * dep, acv = rcv - depD, remain = Math.max(0, eff - age);
      var warnings = [], notes = [];
      if (v.rcv_mode !== "none" && rcv <= 0) warnings.push("Enter a replacement cost (or choose “Percent only”) to see depreciation in dollars.");

      var rows = [], last = Math.ceil(Math.max(eff, age));
      for (var y = 0; y <= Math.min(last, 100); y++) {
        var d = Math.min(cap, y / eff);
        rows.push([y + (Math.floor(age) === y ? " (now)" : ""), REP.pct(d * 100), rcv > 0 ? M(rcv * (1 - d)) : REP.pct((1 - d) * 100)]);
      }

      if (raw > cap && cap < 1) notes.push("Straight-line depreciation would be " + REP.pct(raw * 100) + "; the " + REP.pct(cap * 100, 0) + " cap limits it.");
      if (raw >= 1) notes.push("The roof is at or past its effective life. If it was still keeping water out before the storm, ask whether the estimate applies a maximum depreciation; many do.");
      if (adj !== 0) notes.push("Condition adjustment of " + (adj > 0 ? "+" : "") + adj + "% changes the effective life from " + v.life + " to " + REP.num(eff, 1) + " years.");
      if (m.key === "silicone" || m.key === "acrylic") notes.push("Coatings are renewable. If the roof was recoated, measure age from the last recoat and bring the records.");
      notes.push("On a replacement cost policy this depreciation is usually recoverable after the roof is replaced. ACV-only roofs and roof payment schedules usually do not pay it back. Check your policy.");
      if (rcv > 0) notes.push("Think the carrier's depreciation is too high? Our $50 claim estimate review (/claim/) checks age, life and missing line items.");

      var kpis = [
        { label: "Depreciation", text: REP.pct(dep * 100) },
        { label: "Roof age", text: yrs(age) },
        { label: "Remaining useful life", text: remain > 0 ? yrs(remain) : "0 (at or past life)" },
        { label: "Effective life used", text: REP.num(eff, 1) + " yrs" },
        { label: "Depreciation per year", text: REP.pct(100 / eff) + (rcv > 0 ? " · " + M(rcv / eff) : "") }
      ];
      if (rcv > 0) kpis.splice(1, 0, { label: "Depreciation $", value: depD, format: "money" });
      else kpis.splice(1, 1);

      return {
        headline: rcv > 0
          ? { label: "Actual cash value (ACV)", value: acv, format: "money", sub: REP.pct(dep * 100) + " depreciated · " + M(depD) + " withheld from " + M(rcv) + " RCV" }
          : { label: "Depreciation", text: REP.pct(dep * 100), sub: "Value remaining " + REP.pct((1 - dep) * 100) + " of replacement cost" },
        figure: chart(rcv, eff, cap, age),
        kpis: kpis,
        breakdown: rcv > 0 ? { title: "Replacement cost split", items: [{ label: "Actual cash value", value: acv }, { label: "Depreciation", value: depD }] } : null,
        warnings: warnings,
        table: { title: "Year-by-year schedule", head: ["Age (yrs)", "Depreciation", rcv > 0 ? "ACV" : "Value left"], rows: rows, scroll: true },
        notes: notes,
        summary: [
          "Material: " + m.name + ", life " + v.life + " yrs" + (adj ? " (" + (adj > 0 ? "+" : "") + adj + "% condition → " + REP.num(eff, 1) + " yrs)" : ""),
          "Condition: " + (COND_NAME[v.condition] || v.condition),
          "Roof age: " + yrs(age),
          "Max depreciation: " + (cap >= 1 ? "no cap" : REP.pct(cap * 100, 0)),
          "Depreciation: " + REP.pct(dep * 100) + (rcv > 0 ? " = " + M(depD) + " of " + M(rcv) + " RCV" : ""),
          rcv > 0 ? "Actual cash value: " + M(acv) : "Value remaining: " + REP.pct((1 - dep) * 100),
          "Remaining useful life: " + (remain > 0 ? yrs(remain) : "0")
        ]
      };
    }
  });
})();
