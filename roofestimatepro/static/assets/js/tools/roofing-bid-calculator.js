/* Roofing Bid & Profit Calculator */
(function () {
  "use strict";
  var M = REP.money, P = function (n) { return REP.pct(n, 1).replace("-", "−"); };

  REP.tool({
    id: "roofing-bid-calculator",
    name: "Roofing Bid & Profit Calculator",
    compute: function (v) {
      var costs = [
        ["Materials (incl. tax)", v.c_mat], ["Labor", v.c_lab], ["Dump / disposal", v.c_dump],
        ["Equipment rental", v.c_equip], ["Permits & inspections", v.c_permit], ["Misc. & subcontractors", v.c_misc]
      ];
      var direct = costs.reduce(function (a, c) { return a + Math.max(0, c[1]); }, 0);
      if (direct <= 0) return { warnings: ["Enter your direct job costs (materials, labor and so on) to price the bid."] };

      var oh = v.oh_mode === "annual" ? Math.max(0, v.oh_annual) / Math.max(1, v.oh_jobs) : direct * Math.max(0, v.oh_pct) / 100;
      var C = direct + oh;
      var c = v.commission / 100, f = v.fees / 100, w = v.warranty / 100, sell = c + f + w;
      var p = Math.max(0, v.profit) / 100;
      var denom = v.p_mode === "markup" ? 1 - sell : 1 - sell - p;
      if (denom <= 0.02) return { warnings: ["Commission, fees, warranty" + (v.p_mode === "margin" ? " and net margin" : "") + " add up to " + Math.round((1 - denom) * 100) + "% of the price, which leaves nothing to cover costs. Lower one of them."] };

      var price = v.p_mode === "markup" ? C * (1 + p) / denom : C / denom;
      var sellAmt = price * sell, comm = price * c, fee = price * f, warr = price * w;
      var gross = price - direct, net = price - C - sellAmt;
      var gm = gross / price * 100, nm = net / price * 100, mu = gross / direct * 100;
      var be = C / (1 - sell);
      var sq = Math.max(0, v.squares);

      var rows = costs.filter(function (x) { return x[1] > 0; }).map(function (x) { return [x[0], "Direct", M(x[1])]; });
      rows.push(["Direct cost subtotal", "", M(direct)]);
      rows.push(["Overhead", v.oh_mode === "annual" ? M(v.oh_annual) + " ÷ " + v.oh_jobs + " jobs" : v.oh_pct + "% of direct", M(oh)]);
      rows.push(["Cost base (direct + overhead)", "", M(C)]);
      if (comm) rows.push(["Sales commission", v.commission + "% of price", M(comm)]);
      if (fee) rows.push(["Financing / card fees", v.fees + "% of price", M(fee)]);
      if (warr) rows.push(["Warranty reserve", v.warranty + "% of price", M(warr)]);
      rows.push(["Net profit", v.p_mode === "markup" ? v.profit + "% markup on cost base" : v.profit + "% of price", M(net)]);

      // Sensitivity: price at target gross margins
      var sens = [];
      ["s1", "s2", "s3", "s4", "s5"].forEach(function (k) {
        var g = v[k] / 100;
        if (!(g >= 0 && g < 0.95)) return;
        var pr = direct / (1 - g), np = pr - C - pr * sell;
        sens.push({ g: v[k], price: pr, psq: sq ? pr / sq : null, net: np, nm: np / pr * 100 });
      });

      var notes = [];
      notes.push("Definitions: gross profit = price − direct costs; net profit = gross profit − overhead − commission − fees − warranty reserve. Markup here is gross profit ÷ direct cost.");
      if (v.p_mode === "markup") notes.push("A " + v.profit + "% markup on cost is a " + P(p / (1 + p) * 100) + " margin on cost-plus-markup. This calculator compounds: markup is applied to direct cost plus overhead.");
      else notes.push("Net margin " + v.profit + "% = markup of " + P(p / (1 - p) * 100) + " on the price before selling costs (margin ÷ (1 − margin)).");
      if (v.oh_mode === "pct" && v.oh_pct === 10 && v.p_mode === "markup" && v.profit === 10) notes.push("10% overhead then 10% profit compounds to 21% on direct cost (1.10 × 1.10). The insurance 10 and 10 convention is 20% because both are figured on the subtotal.");
      if (sq) {
        var psq = price / sq;
        if (psq < 400) notes.push("At " + M(psq) + " per square this bid is below the usual Texas range for architectural shingles ($450–$650). Check that disposal, permits, decking and drip edge are in the costs.");
        if (psq > 900) notes.push("At " + M(psq) + " per square this is above shingle pricing in Texas; that is normal for metal or tile, but high for asphalt.");
      }
      if (net < 0) notes.push("This price loses money after overhead and selling costs.");
      if (nm < 5 && net >= 0) notes.push("A net margin under 5% leaves little room for a decking surprise or a callback.");

      var summary = [
        "Direct costs " + M(direct) + "; overhead " + M(oh) + " (" + (v.oh_mode === "annual" ? "annual ÷ jobs" : v.oh_pct + "% of direct") + ")",
        "Commission " + v.commission + "%, fees " + v.fees + "%, warranty " + v.warranty + "% of price",
        "Profit target: " + v.profit + "% " + (v.p_mode === "markup" ? "markup on direct + overhead (compounded)" : "net margin on price"),
        "Bid price " + M(price) + (sq ? " (" + M(price / sq) + " per square, " + sq + " sq)" : ""),
        "Gross profit " + M(gross) + " (" + P(gm) + " margin, " + P(mu) + " markup); net profit " + M(net) + " (" + P(nm) + ")",
        "Break-even price " + M(be)
      ];
      sens.forEach(function (s) { summary.push("At " + s.g + "% gross margin: " + M(s.price) + (s.psq ? " (" + M(s.psq) + "/sq)" : "") + ", net " + M(s.net)); });

      return {
        headline: { label: "Bid price", value: price, format: "money",
          sub: (sq ? M(price / sq) + " per square · " : "") + "break-even " + M(be) },
        kpis: [
          { label: "Gross profit", value: gross, format: "money" },
          { label: "Net profit", value: net, format: "money" },
          { label: "Gross margin", text: P(gm) },
          { label: "Net margin", text: P(nm) },
          { label: "Markup on direct cost", text: P(mu) },
          { label: "Price per square", text: sq ? M(price / sq) : "Enter squares" },
          { label: "Break-even price", value: be, format: "money" },
          { label: "Overhead this job", value: oh, format: "money" }
        ],
        breakdown: { title: "Where the price goes", items: [
          { label: "Materials", value: Math.max(0, v.c_mat) },
          { label: "Labor", value: Math.max(0, v.c_lab) },
          { label: "Disposal, equipment, permits, misc.", value: Math.max(0, v.c_dump) + Math.max(0, v.c_equip) + Math.max(0, v.c_permit) + Math.max(0, v.c_misc) },
          { label: "Overhead", value: oh },
          { label: "Commission, fees & warranty", value: sellAmt },
          { label: "Net profit", value: net }
        ] },
        table: { title: "Bid build-up", head: ["Item", "Basis", "Amount"], rows: rows, foot: ["Bid price", "", M(price)] },
        notes: notes,
        summary: summary,
        sens: sens
      };
    },
    after: function (v, r) {
      if (!r.sens || !r.sens.length) return;
      var out = document.getElementById("results"), act = out.querySelector(".res-actions");
      if (!act) return;
      var h = '<h2 style="font-size:.95rem;margin:4px 0 6px">Price at other gross margins</h2><div class="res-scroll"><table class="res-table"><thead><tr>' +
        ["Gross margin", "Price", "Per sq", "Net $", "Net %"].map(function (x) { return "<th>" + x + "</th>"; }).join("") +
        "</tr></thead><tbody>" + r.sens.map(function (s) {
          return "<tr><td>" + s.g + "%</td><td>" + M(s.price) + "</td><td>" + (s.psq ? M(s.psq) : "—") + "</td><td>" + M(s.net) + "</td><td>" + P(s.nm) + "</td></tr>";
        }).join("") + "</tbody></table></div>";
      var wrap = document.createElement("div");
      wrap.innerHTML = h;
      out.insertBefore(wrap, act);
    }
  });
})();
