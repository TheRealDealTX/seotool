/* Alabama Insurance Appraiser — claim tools. Runs entirely in the browser. */
(function () {
  "use strict";
  var d = document;
  var usd = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });
  function n(v) { var x = parseFloat(v); return isFinite(x) && x > 0 ? x : 0; }
  function val(f, name) {
    var el = f.querySelector('[name="' + name + '"]:checked') || f.querySelector('[name="' + name + '"]');
    return el ? el.value : "";
  }
  function out(f, key, text) { f.querySelectorAll('[data-out="' + key + '"]').forEach(function (e) { e.textContent = text; }); }
  function bar(f, key, pct) { var b = f.querySelector('[data-bar="' + key + '"]'); if (b) b.style.width = Math.max(0, Math.min(100, pct)) + "%"; }
  function bind(f, fn) { f.addEventListener("input", fn); f.addEventListener("change", fn); fn(); }

  /* Claim gap */
  d.querySelectorAll('[data-tool="gap"]').forEach(function (f) {
    bind(f, function () {
      var c = n(val(f, "carrier")), k = n(val(f, "contractor")), ded = n(val(f, "deductible")), dep = n(val(f, "dep"));
      var acvOnly = val(f, "policy") === "acv";
      var gap = k - c, max = Math.max(c, k, 1);
      out(f, "gap", (gap < 0 ? "−" : "") + usd.format(Math.abs(gap)));
      out(f, "carrierFmt", usd.format(c)); out(f, "contractorFmt", usd.format(k));
      bar(f, "carrier", c / max * 100); bar(f, "contractor", k / max * 100);
      out(f, "gapPct", c ? (gap / c * 100).toFixed(1) + "%" : "—");
      var first = Math.max(0, c - dep - ded);
      var recov = acvOnly ? 0 : Math.min(dep, Math.max(0, c - ded));
      var depRatio = c ? dep / c : 0;
      var kNet = acvOnly ? Math.max(0, k - k * depRatio - ded) : Math.max(0, k - ded);
      out(f, "firstPay", usd.format(first));
      out(f, "recov", acvOnly ? "Not recoverable (ACV policy)" : usd.format(recov));
      out(f, "carrierNet", usd.format(first + recov));
      out(f, "contractorNet", usd.format(kNet));
      var msg;
      if (!c || !k) msg = "Enter both estimate totals to compare.";
      else if (gap <= 0) msg = "The carrier's estimate is at or above the contractor's. Appraisal is unlikely to help on value alone.";
      else if (gap < 2500 || gap / c < 0.1) msg = "A smaller gap. A well-documented supplement or re-inspection request is often the most efficient next step.";
      else if (gap < 10000) msg = "A meaningful gap. Have the estimates compared line by line to see how much of it is clearly supported before choosing appraisal.";
      else msg = "A significant gap. An estimate review is a good first step, and if the differences are well supported, appraisal may be worth considering.";
      out(f, "advice", msg);
    });
  });

  /* Depreciation */
  d.querySelectorAll('[data-tool="dep"]').forEach(function (f) {
    var item = f.querySelector('[name="item"]'), life = f.querySelector('[name="life"]');
    item.addEventListener("change", function () { if (item.value !== "custom") life.value = item.value; });
    life.addEventListener("input", function () { item.value = "custom"; });
    bind(f, function () {
      var rcv = n(val(f, "rcv")), L = n(life.value) || 1, age = n(val(f, "age")), cond = parseFloat(val(f, "cond")) || 1;
      var cap = Math.min(100, n(val(f, "cap")) || 100) / 100;
      var pct = Math.min(cap, (age / L) * cond);
      var depAmt = rcv * pct;
      out(f, "acv", usd.format(rcv - depAmt));
      out(f, "pct", (pct * 100).toFixed(1) + "%");
      bar(f, "dep", pct * 100);
      out(f, "rcvFmt", usd.format(rcv));
      out(f, "depAmt", usd.format(depAmt));
      out(f, "remain", Math.max(0, L - age).toFixed(1) + " years");
    });
  });

  /* Roof squares */
  d.querySelectorAll('[data-tool="roof"]').forEach(function (f) {
    bind(f, function () {
      var L = n(val(f, "len")), W = n(val(f, "wid")), o = n(val(f, "over")) / 12 * 2;
      var pitch = parseFloat(val(f, "pitch")) || 6, waste = parseFloat(val(f, "style")) || 10;
      var stories = n(val(f, "stories")) || 1;
      var foot = (L + o) * (W + o);
      var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
      var area = foot * mult, sq = area / 100, sqW = sq * (1 + waste / 100);
      out(f, "foot", Math.round(foot).toLocaleString() + " sq ft");
      out(f, "mult", mult.toFixed(3) + "×");
      out(f, "area", Math.round(area).toLocaleString() + " sq ft");
      out(f, "sq", sq.toFixed(2));
      out(f, "waste", waste + "%");
      out(f, "sqWaste", (Math.ceil(sqW * 3) / 3).toFixed(2) + " sq");
      out(f, "bundles", Math.ceil(sqW * 3).toLocaleString());
      var notes = [];
      if (pitch >= 8) notes.push("At " + pitch + "/12 this roof is steep enough that most estimates should include steep-slope labor charges.");
      if (stories >= 2) notes.push("Two-story roofs commonly carry high-roof (additional story) charges.");
      if (pitch <= 3) notes.push("Slopes of 3/12 and below are low-slope; standard shingles generally aren't suitable, so check the material on the estimate.");
      if (!notes.length) notes.push("Compare these squares and the waste percentage with the roof section of your insurance estimate.");
      out(f, "steep", notes.join(" "));
    });
  });

  /* Hurricane deductible */
  d.querySelectorAll('[data-tool="hurr"]').forEach(function (f) {
    var custom = f.querySelector('[name="custom"]');
    bind(f, function () {
      var A = n(val(f, "covA")), pct = n(custom.value) || parseFloat(val(f, "pct")) || 2;
      var aop = n(val(f, "aop")), loss = n(val(f, "loss"));
      var ded = A * pct / 100;
      out(f, "ded", usd.format(ded));
      out(f, "pctFmt", pct + "% of " + usd.format(A));
      out(f, "pay", usd.format(Math.max(0, loss - ded)));
      out(f, "payAop", usd.format(Math.max(0, loss - aop)));
      out(f, "extra", usd.format(Math.max(0, Math.min(loss, ded) - Math.min(loss, aop))));
      out(f, "note", loss && loss <= ded
        ? "At this size the storm damage would fall entirely within the deductible, so no payment would be due for the dwelling."
        : "Percentage deductibles usually apply only when the policy's hurricane or named-storm trigger is met. Other wind and hail losses may use your regular deductible.");
    });
  });

  /* Checklist with localStorage */
  d.querySelectorAll('[data-tool="checklist"]').forEach(function (wrap) {
    var KEY = "aia-checklist-v1", state = {};
    try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { state = {}; }
    var boxes = wrap.querySelectorAll("[data-check]");
    function update() {
      var done = 0;
      boxes.forEach(function (b) { if (b.checked) done++; });
      var pct = Math.round(done / boxes.length * 100);
      wrap.querySelector("[data-ring]").style.setProperty("--v", pct);
      out(wrap, "pct", pct + "%");
      out(wrap, "done", done + " of " + boxes.length + " gathered");
      wrap.querySelectorAll(".check-group").forEach(function (g) {
        var bs = g.querySelectorAll("[data-check]"), c = 0;
        bs.forEach(function (b) { if (b.checked) c++; });
        g.querySelector("[data-group-count]").textContent = c + "/" + bs.length;
      });
    }
    boxes.forEach(function (b) {
      b.checked = !!state[b.getAttribute("data-check")];
      b.addEventListener("change", function () {
        state[b.getAttribute("data-check")] = b.checked;
        try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* storage unavailable */ }
        update();
      });
    });
    wrap.querySelector("[data-print]").addEventListener("click", function () { window.print(); });
    wrap.querySelector("[data-reset]").addEventListener("click", function () {
      state = {}; boxes.forEach(function (b) { b.checked = false; });
      try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
      update();
    });
    update();
  });
})();
