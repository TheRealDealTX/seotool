/* stonecoatedroofs.com — interactive tools. Every figure is a planning estimate. */
(function () {
  "use strict";
  var d = document;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function money(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
  function num(n) { return Math.round(n).toLocaleString("en-US"); }
  function val(t, name) {
    var el = t.querySelector("[name=" + name + "]:checked") || t.querySelector("[name=" + name + "]");
    return el ? parseFloat(el.value) : 0;
  }
  var store = {
    get: function (k, f) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : f; } catch (e) { return f; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  /* range inputs: fill + live output */
  function wireRanges(t, fn) {
    $$("input[type=range]", t).forEach(function (r) {
      var out = t.querySelector("output[for=" + r.id + "]"), fmt = r.getAttribute("data-fmt") || "";
      function paint() {
        r.style.setProperty("--fill", ((r.value - r.min) / (r.max - r.min) * 100) + "%");
        if (out) out.textContent = fmt === "$" ? money(r.value) : fmt === "%" ? r.value + "%" : fmt === "yr" ? r.value + " yrs" : fmt === "sf" ? num(r.value) + " sq ft" : fmt === "$sf" ? "$" + parseFloat(r.value).toFixed(2) : r.value;
      }
      r.addEventListener("input", function () { paint(); fn(); }); paint();
    });
    $$("input:not([type=range]), select", t).forEach(function (i) { i.addEventListener("change", fn); i.addEventListener("input", fn); });
    fn();
  }
  function bars(el, rows) {
    var max = Math.max.apply(null, rows.map(function (r) { return r[1]; })) || 1;
    el.innerHTML = rows.map(function (r) {
      return '<div class="b' + (r[2] ? " alt" : "") + '"><label><span>' + r[0] + "</span><span>" + r[3] + '</span></label><div class="t"><i style="width:' + (r[1] / max * 100).toFixed(1) + '%"></i></div></div>';
    }).join("");
  }
  function set(t, k, v) { var el = t.querySelector("[data-o=" + k + "]"); if (el) el.textContent = v; }

  /* 1. Stone coated roof cost calculator */
  $$("[data-tool=cost]").forEach(function (t) {
    wireRanges(t, function () {
      var foot = val(t, "foot"), pitch = val(t, "pitch"), cx = val(t, "complex"), prof = val(t, "profile"), tear = val(t, "tear"), meth = val(t, "method");
      var area = foot * pitch * 1.1;                     /* + eaves/overhang allowance */
      var sq = area / 100;
      var lo = area * 10 * prof * meth * (1 + cx) + area * tear;
      var hi = area * 18 * prof * meth * (1 + cx) + area * tear * 1.6;
      var mid = (lo + hi) / 2;
      var alo = area * 4.5 * (1 + cx) + area * tear, ahi = area * 7.5 * (1 + cx) + area * tear * 1.6;
      set(t, "range", money(lo) + " – " + money(hi));
      set(t, "squares", sq.toFixed(1) + " squares (" + num(area) + " sq ft)");
      set(t, "persq", money(mid / sq) + " / square");
      set(t, "asphalt", money(alo) + " – " + money(ahi));
      set(t, "life", "~" + Math.round(mid / 55).toLocaleString("en-US") + " per year of roof life");
      var b = t.querySelector(".bars");
      if (b) bars(b, [["Stone coated steel (mid)", mid, 0, money(mid)], ["Asphalt shingle (mid)", (alo + ahi) / 2, 1, money((alo + ahi) / 2)], ["Asphalt × 3 replacements over 55 yrs", (alo + ahi) / 2 * 3, 1, money((alo + ahi) / 2 * 3)]]);
    });
  });

  /* 2. Lifetime cost (stone coated vs asphalt) */
  $$("[data-tool=lifetime]").forEach(function (t) {
    var svg = t.querySelector("svg.chart");
    wireRanges(t, function () {
      var area = val(t, "area"), yrs = val(t, "years"), sc = val(t, "sc"), as = val(t, "as"), life = val(t, "alife"), prem = val(t, "prem"), disc = val(t, "disc") / 100, inf = 0.03;
      var stone = [], asph = [], s = area * sc, a = area * as, sav = 0, br = null;
      for (var y = 0; y <= yrs; y++) {
        if (y > 0) sav += prem * disc * Math.pow(1 + inf, y);            /* premium savings */
        if (y > 0 && y % life === 0) a += area * as * Math.pow(1 + inf, y) * 1.08; /* tear-off & replace */
        if (y > 0 && y % 7 === 0) a += 450 * Math.pow(1 + inf, y);     /* storm-cycle repairs */
        stone.push(s); asph.push(a);
        if (br === null && s - sav <= a && y > 0) br = y;
      }
      var net = s - sav;
      set(t, "stone", money(s)); set(t, "sav", "−" + money(sav)); set(t, "asph", money(asph[yrs]));
      set(t, "diff", net < asph[yrs] ? money(asph[yrs] - net) + " saved with stone coated" : money(net - asph[yrs]) + " more for stone coated");
      set(t, "even", br === null ? "Not within " + yrs + " years" : "Year " + br);
      set(t, "reroofs", Math.floor(yrs / life) + " asphalt replacements");
      if (svg) {
        var W = 600, H = 240, max = Math.max(stone[yrs], asph[yrs], area * sc) * 1.08;
        function path(arr) { return arr.map(function (v, i) { return (i ? "L" : "M") + (i / yrs * W).toFixed(1) + " " + (H - v / max * H).toFixed(1); }).join(" "); }
        svg.innerHTML = '<path d="' + path(asph) + '" stroke="#8a8077" stroke-width="3" fill="none" stroke-dasharray="6 5"/>' +
          '<path d="' + path(stone) + '" stroke="#d98a63" stroke-width="3.5" fill="none"/>' +
          (br !== null ? '<line x1="' + (br / yrs * W) + '" x2="' + (br / yrs * W) + '" y1="0" y2="' + H + '" stroke="rgba(255,255,255,.3)" stroke-dasharray="3 4"/><text x="' + (br / yrs * W + 6) + '" y="16" fill="#f2c4a6" font-size="13">break-even</text>' : "") +
          '<text x="0" y="' + (H + 18) + '" fill="#b8ada1" font-size="12">Year 0</text><text x="' + (W - 50) + '" y="' + (H + 18) + '" fill="#b8ada1" font-size="12">Year ' + yrs + "</text>";
      }
    });
  });

  /* 3. Insurance discount estimator */
  $$("[data-tool=insurance]").forEach(function (t) {
    wireRanges(t, function () {
      var prem = val(t, "prem"), disc = val(t, "disc") / 100, yrs = val(t, "years"), home = val(t, "home"), ded = val(t, "ded") / 100;
      var yr = prem * disc, total = 0;
      for (var y = 1; y <= yrs; y++) total += yr * Math.pow(1.04, y - 1);   /* premiums trend ~4%/yr */
      set(t, "year", money(yr)); set(t, "month", money(yr / 12)); set(t, "total", money(total));
      set(t, "ded", money(home * ded));
      var b = t.querySelector(".bars");
      if (b) bars(b, [["Premium today", prem, 1, money(prem) + "/yr"], ["With Class 4 discount", prem - yr, 0, money(prem - yr) + "/yr"]]);
    });
  });

  /* 4. Hail storm readiness / hail damage checklist */
  $$("[data-tool=hail]").forEach(function (t) {
    var ring = t.querySelector(".fg"), C = 2 * Math.PI * 70;
    if (ring) { ring.style.strokeDasharray = C; }
    function run() {
      var score = 0, max = 0;
      $$("input[type=checkbox]", t).forEach(function (c) { var w = parseFloat(c.getAttribute("data-w")); max += w; if (c.checked) score += w; });
      var pct = Math.round(score / max * 100);
      set(t, "score", pct);
      if (ring) { ring.style.strokeDashoffset = C * (1 - pct / 100); ring.style.stroke = pct < 25 ? "#6fbf8a" : pct < 55 ? "#e3a548" : "#e46b34"; }
      var v = pct < 25 ? ["Low concern", "Few damage signs. Keep an eye on it and schedule a routine inspection after the next big storm."]
        : pct < 55 ? ["Get an inspection", "Several warning signs. Have the roof inspected and photographed before you call your carrier — hidden bruising shortens shingle life."]
          : ["Likely replacement", "Multiple serious signs. A full inspection and insurance claim are worth starting now — and it's the moment to upgrade to Class 4 stone coated steel."];
      set(t, "verdict", v[0]); set(t, "advice", v[1]);
      store.set("scr_hail", $$("input[type=checkbox]", t).map(function (c) { return c.checked; }));
    }
    var saved = store.get("scr_hail", []);
    $$("input[type=checkbox]", t).forEach(function (c, i) { c.checked = !!saved[i]; c.addEventListener("change", run); });
    var rs = t.querySelector("[data-reset]"); if (rs) rs.addEventListener("click", function () { $$("input[type=checkbox]", t).forEach(function (c) { c.checked = false; }); run(); });
    run();
  });

  /* 5. Maintenance checklist + log */
  $$("[data-tool=maint]").forEach(function (t) {
    var key = "scr_maint", logKey = "scr_maint_log", st = store.get(key, {});
    $$("input[type=checkbox]", t).forEach(function (c) {
      c.checked = !!st[c.id];
      c.addEventListener("change", function () { st[c.id] = c.checked; store.set(key, st); prog(); });
    });
    function prog() {
      $$("[data-season]", t).forEach(function (s) {
        var all = $$("input[type=checkbox]", s), done = all.filter(function (c) { return c.checked; }).length;
        var o = s.querySelector("[data-prog]"); if (o) o.textContent = done + " / " + all.length + " done";
      });
    }
    prog();
    var form = t.querySelector("form.log-form"), body = t.querySelector(".log-table tbody"), log = store.get(logKey, []);
    function draw() {
      body.innerHTML = log.length ? log.map(function (r, i) {
        return "<tr><td>" + esc(r.date) + "</td><td>" + esc(r.type) + "</td><td>" + esc(r.notes) + '</td><td><button type="button" class="btn-sm" data-del="' + i + '" aria-label="Delete entry">×</button></td></tr>';
      }).join("") : '<tr><td colspan="4" class="muted">No entries yet — add your first inspection above.</td></tr>';
      $$("[data-del]", body).forEach(function (b) { b.addEventListener("click", function () { log.splice(+b.getAttribute("data-del"), 1); store.set(logKey, log); draw(); }); });
    }
    function esc(s) { return String(s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    if (form) {
      form.date.value = new Date().toISOString().slice(0, 10);
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        log.unshift({ date: form.date.value, type: form.type.value, notes: form.notes.value });
        store.set(logKey, log); form.notes.value = ""; draw();
      });
      draw();
    }
    var csv = t.querySelector("[data-csv]");
    if (csv) csv.addEventListener("click", function () {
      var rows = [["Date", "Type", "Notes"]].concat(log.map(function (r) { return [r.date, r.type, r.notes]; }));
      var blob = new Blob([rows.map(function (r) { return r.map(function (c) { return '"' + String(c).replace(/"/g, '""') + '"'; }).join(","); }).join("\n")], { type: "text/csv" });
      var a = d.createElement("a"); a.href = URL.createObjectURL(blob); a.download = "roof-maintenance-log.csv"; a.click();
    });
    var pr = t.querySelector("[data-print]"); if (pr) pr.addEventListener("click", function () { window.print(); });
  });

  /* 6. Roof weight calculator */
  $$("[data-tool=weight]").forEach(function (t) {
    var mats = [["Stone coated steel", 1.6, 2.4], ["Standing seam metal", 0.9, 1.5], ["Asphalt shingle (architectural)", 2.3, 4.3], ["Wood shake", 3, 4.5], ["Concrete tile", 9, 10], ["Clay tile", 8, 12], ["Natural slate", 8, 15]];
    wireRanges(t, function () {
      var area = val(t, "area"), sc = mats[0][2] * area;
      set(t, "stone", num(sc) + " lb"); set(t, "tons", (sc / 2000).toFixed(1) + " tons");
      set(t, "vs", num(area * 9.5 - sc) + " lb lighter than concrete tile");
      bars(t.querySelector(".bars"), mats.map(function (m, i) { var w = m[2] * area; return [m[0], w, i !== 0, num(m[1] * area) + "–" + num(w) + " lb"]; }));
    });
  });
})();
