/* Gutter & Downspout Calculator */
(function () {
  "use strict";
  var M = REP.money;

  var RAIN = { houston: 7, dfw: 6.5, central: 6.5, sa: 6.5, south: 6.5, east: 6.5, west: 5, other: 6 };
  var PRICES = {
    aluminum: { g5: [8, 14], g6: [10, 18], d23: [7, 11], d34: [9, 14], el: [8, 15] },
    steel: { g5: [10, 16], g6: [12, 20], d23: [9, 14], d34: [11, 17], el: [10, 18] },
    copper: { g5: [25, 35], g6: [30, 40], d23: [20, 30], d34: [25, 38], el: [25, 45] }
  };
  var MAT = { aluminum: "Seamless aluminum", steel: "Galvalume / galvanized steel", copper: "Copper" };

  function pitchFactor(r) { return r >= 12 ? 1.3 : r >= 9 ? 1.2 : r >= 6 ? 1.1 : r >= 4 ? 1.05 : 1.0; }
  function esc(s) { return REP.esc(s); }

  REP.tool({
    id: "gutter-calculator",
    name: "Gutter & Downspout Calculator",
    rowDefaults: { runs: [
      { name: "Front", lf: 48, area: 750 }, { name: "Back", lf: 48, area: 750 },
      { name: "Left side", lf: 32, area: 300 }, { name: "Right side", lf: 32, area: 300 }
    ] },
    init: function (form, run) {
      form.querySelector('[name="rain"]').addEventListener("change", function (e) {
        if (RAIN[e.target.value] != null) form.querySelector('[name="intensity"]').value = RAIN[e.target.value];
        run();
      });
      form.querySelector('[name="material"]').addEventListener("change", function (e) {
        var p = PRICES[e.target.value]; if (!p) return;
        Object.keys(p).forEach(function (k) {
          form.querySelector('[name="' + k + '_lo"]').value = p[k][0];
          form.querySelector('[name="' + k + '_hi"]').value = p[k][1];
        });
        run();
      });
    },
    compute: function (v) {
      var I = v.intensity, warnings = [];
      if (!(I > 0)) return { warnings: ["Enter a design rainfall intensity above 0 in/hr."] };
      var pf = pitchFactor(v.pitch);
      var cap5 = v.k5 / I, cap6 = v.k6 / I;

      // Build the list of runs
      var runs = [];
      if (v.mode === "total") {
        var n = Math.max(1, Math.round(v.n_runs));
        if (v.total_lf > 0) for (var i = 0; i < n; i++) runs.push({ name: "Run " + (i + 1), lf: v.total_lf / n, area: Math.max(0, v.total_area) / n });
      } else {
        var given = 0, blankLf = 0;
        (v.rows.runs || []).forEach(function (r, ix) {
          if (!(r.lf > 0)) return;
          runs.push({ name: r.name || "Run " + (ix + 1), lf: r.lf, area: Math.max(0, r.area), est: !(r.area > 0) });
          if (r.area > 0) given += r.area; else blankLf += r.lf;
        });
        if (blankLf > 0) {
          var left = Math.max(0, v.total_area - given);
          if (left <= 0) warnings.push("Some runs have no drainage area and the total roof area is already used up by the other runs. Enter an area for each run.");
          runs.forEach(function (r) { if (r.est) r.area = left * r.lf / blankLf; });
        }
      }
      if (!runs.length) return { warnings: ["Enter at least one gutter run with a length."] };

      // Size each run
      var needMax = 5;
      runs.forEach(function (r) {
        r.adj = r.area * pf;
        r.need = r.adj <= cap5 ? 5 : r.adj <= cap6 ? 6 : 7;
        if (r.need > needMax) needMax = r.need;
      });
      var size = v.size === "5" ? 5 : v.size === "6" ? 6 : Math.min(6, needMax);
      var dsKey = v.ds === "23" ? "23" : v.ds === "34" ? "34" : (size === 6 ? "34" : "23");
      var dsCap = dsKey === "34" ? v.cap34 : v.cap23;
      var gCap = size === 6 ? cap6 : cap5;
      var spacing = Math.max(10, v.spacing);

      var totLf = 0, totDs = 0, totAdj = 0, split = [];
      runs.forEach(function (r) {
        r.ds = Math.max(1, Math.ceil(r.lf / spacing - 1e-9), Math.ceil(r.adj / dsCap - 1e-9));
        if (r.adj > gCap) { var need = Math.ceil(r.adj / gCap - 1e-9); if (need > r.ds) { r.ds = need; split.push(r.name); } }
        totLf += r.lf; totDs += r.ds; totAdj += r.adj;
      });
      if (v.size === "5" && needMax > 5) warnings.push('Some runs need more than a 5" gutter at ' + I + ' in/hr. Runs are split with extra downspouts where needed (see Sizing by run), but 6" gutters are the better fix.');
      if (needMax > 6) warnings.push("At least one run exceeds 6\" gutter capacity as a single section and is split with extra downspouts. On very large roofs, consider 7\" commercial gutters or box gutters.");

      var dsEach = v.stories * v.story_h + 2;
      var dsLf = totDs * dsEach;
      var elbows = totDs * Math.max(0, v.elbows);
      var reg = REP.region(v.region).factor;
      var gk = size === 6 ? "g6" : "g5", dk = "d" + dsKey;
      var lines = [
        [size + '" K-style gutter (' + MAT[v.material].toLowerCase() + ")", REP.num(Math.round(totLf)) + " lf", totLf, v[gk + "_lo"], v[gk + "_hi"]],
        [(dsKey === "34" ? "3×4" : "2×3") + " in downspouts", REP.num(Math.round(dsLf)) + " lf", dsLf, v[dk + "_lo"], v[dk + "_hi"]],
        ["Elbows", elbows + " ea", elbows, v.el_lo, v.el_hi]
      ];
      if (v.guards) lines.push(["Gutter guards", REP.num(Math.round(totLf)) + " lf", totLf, v.gd_lo, v.gd_hi]);
      if (v.removal) lines.push(["Remove & haul off old gutters", REP.num(Math.round(totLf)) + " lf", totLf, v.rm_lo, v.rm_hi]);

      var lo = 0, hi = 0, rows = [], bd = [];
      lines.forEach(function (l) {
        var a = l[2] * Math.min(l[3], l[4]) * reg, b = l[2] * Math.max(l[3], l[4]) * reg;
        lo += a; hi += b;
        rows.push([l[0], l[1], M(a), M(b)]);
        bd.push({ label: l[0], value: (a + b) / 2 });
      });
      var mid = (lo + hi) / 2;

      var notes = [];
      if (v.size === "auto") notes.push(needMax <= 5
        ? 'Every run fits a 5" gutter at ' + I + " in/hr (limit " + REP.num(Math.round(cap5)) + " sq ft of adjusted area per run)."
        : '6" gutters recommended: at least one run carries more than the ' + REP.num(Math.round(cap5)) + ' sq ft a 5" gutter handles at ' + I + " in/hr. Using one size around the house keeps the look consistent.");
      if (split.length) notes.push("Extra downspouts added to split: " + split.join(", ") + ".");
      if (reg !== 1) notes.push("Prices scaled ×" + reg.toFixed(2) + " for " + REP.region(v.region).name + ".");
      if (v.material === "steel" && (v.region === "houston" || v.rain === "houston")) notes.push("Steel gutters rust at cut edges in coastal air; aluminum or copper holds up better on the Gulf Coast.");
      notes.push("Gutters dented by hail are commonly included on a covered hail claim. Photograph the dents before removal.");

      var runRows = runs.map(function (r) {
        return [r.name, REP.num(Math.round(r.lf)), REP.num(Math.round(r.adj)) + (r.est ? "*" : ""), r.need > 6 ? '6" + split' : r.need + '"', String(r.ds)];
      });

      var dsName = dsKey === "34" ? "3×4" : "2×3";
      var summary = [
        "Design rainfall " + I + " in/hr; pitch factor " + pf.toFixed(2) + "; 5\" limit " + Math.round(cap5) + " sq ft, 6\" limit " + Math.round(cap6) + " sq ft per run",
        "Recommended: " + size + "\" K-style " + MAT[v.material].toLowerCase() + " gutters with " + totDs + " " + dsName + " downspouts"
      ];
      runs.forEach(function (r) { summary.push(r.name + ": " + Math.round(r.lf) + " lf, " + Math.round(r.adj) + " sq ft adjusted, needs " + (r.need > 6 ? "6\" + split" : r.need + "\"") + ", " + r.ds + " downspout(s)"); });
      summary.push("Gutter " + Math.round(totLf) + " lf; downspout " + Math.round(dsLf) + " lf; " + elbows + " elbows" + (v.guards ? "; guards" : "") + (v.removal ? "; remove old gutters" : ""));
      summary.push("Estimated installed cost: " + M(mid) + " (range " + M(lo) + "–" + M(hi) + ")");

      return {
        headline: { label: "Estimated installed cost", value: mid, format: "money",
          sub: "Range " + M(lo) + " – " + M(hi) + " · " + size + '" K-style with ' + dsName + " downspouts" },
        kpis: [
          { label: "Recommended gutter", text: size + '" K-style' },
          { label: "Downspouts", text: totDs + " × " + dsName },
          { label: "Gutter length", text: REP.num(Math.round(totLf)) + " ln ft" },
          { label: "Downspout length", text: REP.num(Math.round(dsLf)) + " ln ft" }
        ],
        warnings: warnings,
        breakdown: { title: "Where the money goes", items: bd },
        table: { title: "Materials & installation", head: ["Item", "Qty", "Low", "High"], rows: rows, foot: ["Total", "", M(lo), M(hi)] },
        notes: notes,
        summary: summary,
        runRows: runRows,
        anyEst: runs.some(function (r) { return r.est; })
      };
    },
    after: function (v, r) {
      if (!r.runRows) return;
      var out = document.getElementById("results"), act = out.querySelector(".res-actions");
      if (!act) return;
      var h = '<h2 style="font-size:.95rem;margin:4px 0 6px">Sizing by run</h2><div class="res-scroll"><table class="res-table"><thead><tr>' +
        ["Run", "LF", "Adj. sq ft", "Size", "Spouts"].map(function (c) { return "<th>" + c + "</th>"; }).join("") +
        "</tr></thead><tbody>" + r.runRows.map(function (row) { return "<tr>" + row.map(function (c) { return "<td>" + esc(c) + "</td>"; }).join("") + "</tr>"; }).join("") +
        "</tbody></table></div>" + (r.anyEst ? '<p class="help">* Area estimated from the total roof area, shared by length.</p>' : "");
      var wrap = document.createElement("div");
      wrap.innerHTML = h;
      out.insertBefore(wrap, act);
    }
  });
})();
