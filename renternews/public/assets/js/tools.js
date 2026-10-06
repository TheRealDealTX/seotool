/* Renter News — interactive tools. Each tool page has [data-tool="<slug>"]. */
(function () {
  "use strict";
  var root = document.querySelector("[data-tool]");
  if (!root) return;
  function $(s, r) { return (r || root).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || root).querySelectorAll(s)); }
  function num(name) { var el = $('[name="' + name + '"]'); var v = parseFloat(el && el.value); return isFinite(v) ? v : 0; }
  function money(v, d) { return (v < 0 ? "-$" : "$") + Math.abs(v).toLocaleString("en-US", { maximumFractionDigits: d || 0, minimumFractionDigits: d || 0 }); }
  function out(k, v) { var el = $('[data-out="' + k + '"]'); if (el) el.innerHTML = v; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
  function bindRanges() {
    $$('input[type="range"]').forEach(function (r) {
      var o = $('output[data-for="' + r.name + '"]');
      var show = function () { if (o) o.textContent = r.value + (r.dataset.fmt === "yr" ? (r.value == 1 ? " year" : " years") : r.dataset.fmt); };
      r.addEventListener("input", show); show();
    });
  }
  function seg(attr, cb) {
    $$("[data-" + attr + "]").forEach(function (b) {
      b.addEventListener("click", function () {
        $$("[data-" + attr + "]").forEach(function (x) { x.classList.toggle("is-on", x === b); });
        cb(b.dataset[attr]);
      });
    });
  }
  function live(fn) { var f = $("[data-form]") || root; f.addEventListener("input", fn); f.addEventListener("change", fn); fn(); }
  function bar(label, value, pct, color) {
    return '<div class="sbar"><div class="sbar-top"><span>' + label + "</span><span>" + value + '</span></div><div class="sbar-track"><div class="sbar-fill" style="width:' + Math.max(0, Math.min(100, pct)) + "%" + (color ? ";background:" + color : "") + '"></div></div></div>';
  }
  var printBtn = $("[data-print]"); if (printBtn) printBtn.addEventListener("click", function () { print(); });

  var tools = {
    /* ---------- Rent affordability ---------- */
    "rent-affordability-calculator": function () {
      var period = "year";
      seg("period", function (p) {
        var inc = $('[name="income"]');
        inc.value = Math.round(p === "month" ? num("income") / 12 : num("income") * 12);
        period = p; calc();
      });
      var fill = $(".g-fill");
      function calc() {
        var monthly = period === "year" ? num("income") / 12 : num("income"), debts = num("debts"), util = num("utilities"), pct = num("pct") / 100;
        var r30 = monthly * 0.3 - util, r5030 = monthly * 0.5 - debts - util, r40 = monthly * 12 / 40;
        var target = Math.max(0, Math.min(monthly * pct - util, r40));
        var dti = monthly ? (target + util + debts) / monthly * 100 : 0;
        out("rent", money(target));
        out("rentNote", Math.round(pct * 100) + "% of income, minus utilities");
        out("r30", money(Math.max(0, r30)) + "/mo");
        out("r5030", money(Math.max(0, r5030)) + "/mo");
        out("r40", money(r40) + "/mo");
        out("dti", dti.toFixed(0) + "%");
        var p = Math.min(1, monthly ? (target + util) / monthly / 0.5 : 0);
        fill.style.strokeDashoffset = 252 * (1 - p);
        fill.style.stroke = pct <= 0.3 ? "#0f9d8a" : pct <= 0.4 ? "#e0b520" : "#e4572e";
        var adv = pct <= 0.3 ? "Within the 30% guideline: this leaves room for savings and surprises."
          : pct <= 0.4 ? "Above 30%: households spending more than 30% of income on housing are considered cost-burdened. Budget carefully."
          : "Severely stretched: spending over 40% on housing leaves little margin. Consider roommates, a cheaper area or a smaller unit.";
        if (monthly * pct - util > r40) adv += " Note: many landlords require yearly income of 40× the rent, which caps you at " + money(r40) + ".";
        out("advice", adv);
      }
      live(calc);
    },

    /* ---------- Rent split ---------- */
    "rent-split-calculator": function () {
      var method = "equal", box = $("[data-mates]");
      var mates = store("rn-split") || [{ n: "You", v: 180 }, { n: "Roommate 2", v: 140 }];
      function drawRows() {
        var lbl = method === "size" ? "sq ft" : method === "income" ? "$/mo" : "";
        box.innerHTML = mates.map(function (m, i) {
          return '<div class="mate"><input aria-label="Name" data-n="' + i + '" value="' + esc(m.n) + '">' +
            '<input aria-label="' + (lbl || "weight") + '" type="number" min="0" data-v="' + i + '" value="' + m.v + '" placeholder="' + lbl + '"' + (method === "equal" ? " disabled" : "") + ">" +
            '<button type="button" aria-label="Remove" data-rm="' + i + '"' + (mates.length < 3 ? " disabled" : "") + ">×</button></div>";
        }).join("");
      }
      box.addEventListener("input", function (e) {
        var t = e.target;
        if (t.dataset.n) mates[+t.dataset.n].n = t.value;
        if (t.dataset.v) mates[+t.dataset.v].v = parseFloat(t.value) || 0;
        calc();
      });
      box.addEventListener("click", function (e) { var b = e.target.closest("[data-rm]"); if (b) { mates.splice(+b.dataset.rm, 1); drawRows(); calc(); } });
      $("[data-add-mate]").addEventListener("click", function () {
        if (mates.length >= 6) return;
        mates.push({ n: "Roommate " + (mates.length + 1), v: 120 }); drawRows(); calc();
      });
      seg("method", function (m) {
        method = m;
        if (m === "income") mates.forEach(function (x) { if (x.v < 500) x.v = 3500; });
        if (m === "size") mates.forEach(function (x) { if (x.v >= 500) x.v = 150; });
        drawRows(); calc();
      });
      var summary = "";
      function calc() {
        store("rn-split", mates);
        var rent = num("rent"), util = num("utilities"), tot = mates.reduce(function (s, m) { return s + (m.v || 0); }, 0);
        var res = mates.map(function (m) {
          var share = method === "equal" || !tot ? 1 / mates.length : (m.v || 0) / tot;
          return { n: m.n || "Roommate", r: rent * share, u: util / mates.length, s: share };
        });
        var max = Math.max.apply(null, res.map(function (r) { return r.r + r.u; })) || 1;
        $("[data-split]").innerHTML = res.map(function (r) {
          return bar(esc(r.n) + " <small style='color:var(--muted)'>(" + (r.s * 100).toFixed(0) + "%)</small>", money(r.r + r.u), (r.r + r.u) / max * 100);
        }).join("");
        summary = "Rent split (" + method + "): " + res.map(function (r) { return r.n + " " + money(r.r + r.u); }).join(", ") + " — total " + money(rent + util) + "/mo";
      }
      $("[data-copy-result]").addEventListener("click", function () {
        var b = this; (navigator.clipboard ? navigator.clipboard.writeText(summary) : Promise.reject()).then(function () { b.textContent = "Copied!"; setTimeout(function () { b.textContent = "Copy summary"; }, 1500); }, function () { prompt("Copy:", summary); });
      });
      drawRows(); live(calc);
    },

    /* ---------- Rent increase ---------- */
    "rent-increase-calculator": function () {
      function calc() {
        var cur = num("current"), nw = num("proposed"), capEl = $('[name="cap"]'), cap = parseFloat(capEl.value), months = num("months") || 12;
        var diff = nw - cur, pct = cur ? diff / cur * 100 : 0;
        out("pct", (pct >= 0 ? "+" : "") + pct.toFixed(1) + "%");
        out("month", money(diff));
        out("lease", money(diff * months));
        out("income", money(nw * 12 / 0.3) + "/yr");
        if (isFinite(cap)) {
          var capRent = cur * (1 + cap / 100);
          out("capRent", money(capRent, 0));
          out("cmp", pct > cap ? "<span style='color:#e4572e'>Above your " + cap + "% cap by " + money(nw - capRent) + "/mo</span>" : "<span style='color:#0f9d8a'>Within your " + cap + "% cap</span>");
        } else { out("capRent", "—"); out("cmp", diff > 0 ? money(diff) + " more each month" : diff < 0 ? "A decrease" : "No change"); }
        var m = Math.max(cur, nw, 1);
        $("[data-bars]").innerHTML = bar("Current rent", money(cur), cur / m * 100, "#5aa4ee") + bar("Proposed rent", money(nw), nw / m * 100, pct > (isFinite(cap) ? cap : 99) ? "#e4572e" : "");
      }
      live(calc);
    },

    /* ---------- Move-in cost ---------- */
    "moving-cost-calculator": function () {
      // Rough planning midpoints by home size: [DIY truck, truck + loaders, full service]
      var LOCAL = [[150, 450, 700], [200, 650, 1100], [260, 900, 1700], [320, 1200, 2500]];
      var COLORS = ["#1f5c99", "#2f7fd0", "#b8960b", "#0f9d8a", "#e4572e", "#5b5fc7", "#f08c00", "#8796ad"];
      function calc() {
        var rent = num("rent"), size = +$('[name="size"]').value, mv = $('[name="move"]').value, miles = num("miles");
        var moveCost = mv === "none" ? 40 : LOCAL[size][{ diy: 0, labor: 1, full: 2 }[mv]];
        if (mv !== "none" && miles > 50) moveCost += (miles - 50) * (mv === "full" ? 3.5 + size : 1.2);
        var items = [
          ["First month's rent", rent],
          ["Security deposit", rent * parseFloat($('[name="deposit"]').value)],
          ["Last month's rent", $('[name="last"]').checked ? rent : 0],
          ["Application fees", num("appfee")],
          ["Broker / admin fee", num("broker")],
          ["Pet deposit / fee", num("pet")],
          ["Moving", moveCost],
          ["Utilities & supplies", num("utilities") + num("supplies")]
        ].filter(function (x) { return x[1] > 0; });
        var total = items.reduce(function (s, x) { return s + x[1]; }, 0);
        out("total", money(total));
        var off = 0, circ = 2 * Math.PI * 15.915;
        $("[data-donut]").innerHTML = '<circle cx="21" cy="21" r="15.915" stroke="var(--paper-2)"/>' + items.map(function (x, i) {
          var len = total ? x[1] / total * circ : 0, s = '<circle cx="21" cy="21" r="15.915" stroke="' + COLORS[i % 8] + '" stroke-dasharray="' + len + " " + (circ - len) + '" stroke-dashoffset="' + (-off) + '"/>';
          off += len; return s;
        }).join("");
        $("[data-legend]").innerHTML = items.map(function (x, i) { return '<li><i style="background:' + COLORS[i % 8] + '"></i>' + x[0] + "<b>" + money(x[1]) + "</b></li>"; }).join("");
      }
      live(calc);
    },

    /* ---------- Rent vs buy ---------- */
    "rent-vs-buy-calculator": function () {
      bindRanges();
      function calc() {
        var rent = num("rent"), rg = num("rentGrowth") / 100, price = num("price"), down = num("down") / 100, rate = num("rate") / 100,
          years = Math.round(num("years")), tax = num("tax") / 100, maint = num("maint") / 100, appr = num("appr") / 100, inv = num("invest") / 100;
        var loan = price * (1 - down), mr = rate / 12, n = 360;
        var pmt = mr ? loan * mr / (1 - Math.pow(1 + mr, -n)) : loan / n;
        var upfront = price * down + price * 0.03;
        var renterInv = upfront, bal = loan, value = price, r = rent, rentSeries = [], buySeries = [];
        for (var m = 1; m <= years * 12; m++) {
          var interest = bal * mr; bal = Math.max(0, bal - (pmt - interest));
          var ownCost = pmt + value * (tax + maint) / 12;
          renterInv = renterInv * (1 + inv / 12) + Math.max(0, ownCost - r);
          value *= 1 + appr / 12;
          if (m % 12 === 0) {
            r *= 1 + rg;
            rentSeries.push(renterInv);
            buySeries.push(value * 0.94 - bal);
          }
        }
        var rNW = rentSeries[rentSeries.length - 1] || 0, bNW = buySeries[buySeries.length - 1] || 0, buyWins = bNW > rNW;
        out("verdictLabel", "After " + years + (years === 1 ? " year" : " years"));
        out("verdict", buyWins ? "Buying wins" : "Renting wins");
        out("gap", "by about " + money(Math.abs(bNW - rNW)));
        out("pmt", money(pmt) + "/mo");
        out("upfront", money(upfront));
        out("rentNW", money(rNW));
        out("buyNW", money(bNW));
        chart(rentSeries, buySeries);
      }
      function chart(a, b) {
        var all = a.concat(b), max = Math.max.apply(null, all.concat([1])), min = Math.min.apply(null, all.concat([0])), W = 520, H = 220, p = 44;
        var x = function (i) { return p + i * (W - p - 10) / Math.max(a.length - 1, 1); }, y = function (v) { return 10 + (max - v) / (max - min || 1) * (H - 40); };
        var path = function (s) { return s.map(function (v, i) { return (i ? "L" : "M") + x(i).toFixed(1) + " " + y(v).toFixed(1); }).join(" "); };
        var g = "";
        for (var k = 0; k <= 4; k++) { var v = min + (max - min) * k / 4; g += '<line class="lc-grid" x1="' + p + '" x2="' + W + '" y1="' + y(v) + '" y2="' + y(v) + '"/><text x="0" y="' + (y(v) + 4) + '">' + (Math.abs(v) >= 1000 ? "$" + Math.round(v / 1000) + "k" : "$" + Math.round(v)) + "</text>"; }
        a.forEach(function (_, i) { if (a.length <= 10 || i % Math.ceil(a.length / 8) === 0) g += '<text x="' + x(i) + '" y="' + (H - 6) + '" text-anchor="middle">Yr ' + (i + 1) + "</text>"; });
        $("[data-chart]").innerHTML = '<div class="lc-legend"><span style="--c:#0f9d8a">Rent + invest</span><span style="--c:#e4572e">Buy</span></div><svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Net worth over time, renting vs buying">' + g +
          '<path class="lc-path" stroke="#0f9d8a" d="' + path(a) + '"/><path class="lc-path" stroke="#e4572e" d="' + path(b) + '"/></svg>';
      }
      live(calc);
    },

    /* ---------- Renters insurance ---------- */
    "renters-insurance-calculator": function () {
      var ROOMS = {
        "Living room": [["Sofa & chairs", 1200], ["TV & electronics", 900], ["Tables, shelves & decor", 500], ["Rugs & lamps", 300]],
        "Bedroom(s)": [["Beds & mattresses", 1200], ["Dressers & furniture", 600], ["Bedding & linens", 300]],
        "Clothing & accessories": [["Clothing", 2500], ["Shoes & bags", 700], ["Jewelry & watches", 500]],
        "Kitchen": [["Small appliances", 400], ["Cookware & dishes", 500], ["Food & pantry", 200]],
        "Electronics & office": [["Laptop & computers", 1300], ["Phones & tablets", 900], ["Desk & office chair", 400], ["Gaming, cameras & audio", 500]],
        "Other": [["Bikes & sports gear", 500], ["Tools & household", 300], ["Books, music & hobbies", 400]]
      };
      var saved = store("rn-inv") || {}, box = $("[data-inventory]");
      box.innerHTML = Object.keys(ROOMS).map(function (room, ri) {
        return '<details class="inv-room"' + (ri < 2 ? " open" : "") + '><summary><span>' + room + '</span><b data-room-total="' + ri + '"></b></summary><div class="inv-items">' +
          ROOMS[room].map(function (it, ii) {
            var k = ri + "-" + ii, v = saved[k] != null ? saved[k] : it[1];
            return "<label>" + it[0] + '<input type="number" min="0" step="50" inputmode="numeric" data-k="' + k + '" data-r="' + ri + '" value="' + v + '"></label>';
          }).join("") + "</div></details>";
      }).join("");
      function calc() {
        var rooms = Object.keys(ROOMS).map(function () { return 0; }), total = 0, inv = {};
        $$("[data-k]").forEach(function (i) { var v = parseFloat(i.value) || 0; inv[i.dataset.k] = v; rooms[+i.dataset.r] += v; total += v; });
        store("rn-inv", inv);
        rooms.forEach(function (v, i) { $('[data-room-total="' + i + '"]').textContent = money(v); });
        var cover = Math.ceil(total * 1.1 / 5000) * 5000;
        out("cover", money(cover));
        out("raw", "Your inventory totals " + money(total) + " (rounded up with a 10% cushion)");
        var max = Math.max.apply(null, rooms.concat([1]));
        $("[data-rooms]").innerHTML = Object.keys(ROOMS).map(function (r, i) { return bar(r, money(rooms[i]), rooms[i] / max * 100); }).join("");
        var jewel = parseFloat($('[data-k="2-2"]').value) || 0, liab = +$('[name="liability"]').value;
        var adv = ["Ask for <strong>replacement cost</strong> coverage, not actual cash value, so you can buy new items after a loss.",
          "Liability: " + money(liab) + " covers injuries to guests or damage you accidentally cause to others' property.",
          "Check the <strong>loss of use / additional living expenses</strong> limit, which pays for a hotel and extra costs if a fire makes your home unlivable.",
          "Take photos or a video walkthrough of every room and store it in the cloud."];
        if (jewel > 1500) adv.splice(1, 0, "Jewelry worth " + money(jewel) + " may exceed your policy's sub-limit for jewelry; ask about a scheduled item rider.");
        $("[data-advice]").innerHTML = adv.map(function (a) { return "<li>" + a + "</li>"; }).join("");
      }
      live(calc);
    },

    /* ---------- Lease notice ---------- */
    "lease-notice-calculator": function () {
      var endEl = $('[name="end"]');
      if (!endEl.value) { var d0 = new Date(); d0.setMonth(d0.getMonth() + 4, 0); endEl.value = d0.toISOString().slice(0, 10); }
      var deadline;
      function fmt(d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "long", day: "numeric", year: "numeric" }); }
      function calc() {
        if (!endEl.value) return;
        var end = new Date(endEl.value + "T12:00"), days = num("days");
        deadline = new Date(end); deadline.setDate(deadline.getDate() - days);
        if ($('[name="month"]').checked && deadline.getDate() !== 1) deadline = new Date(deadline.getFullYear(), deadline.getMonth(), 1, 12);
        var today = new Date(); today.setHours(12, 0, 0, 0);
        var left = Math.round((deadline - today) / 864e5);
        out("deadline", fmt(deadline));
        out("left", left > 0 ? left + " days from today" : left === 0 ? "That's today!" : "<span style='color:#e4572e'>" + -left + " days ago — check your lease for renewal terms</span>");
        var remind = new Date(deadline); remind.setDate(remind.getDate() - 14);
        var steps = [["#8796ad", "Start apartment hunting", remind], ["#e0b520", "Give written notice (deadline)", deadline], ["#0f9d8a", "Move-out walkthrough & photos", new Date(end.getTime() - 2 * 864e5)], ["#1f5c99", "Lease ends", end]];
        $("[data-timeline]").innerHTML = steps.map(function (s) { return '<div class="tl" style="--c:' + s[0] + '"><strong>' + s[1] + "</strong>" + fmt(s[2]) + "</div>"; }).join("");
      }
      $("[data-ics]").addEventListener("click", function () {
        if (!deadline) return;
        var r = new Date(deadline); r.setDate(r.getDate() - 7);
        var d = function (x) { return x.toISOString().slice(0, 10).replace(/-/g, ""); };
        var next = new Date(r); next.setDate(next.getDate() + 1);
        var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Renter News//Lease Notice//EN", "BEGIN:VEVENT", "UID:" + Date.now() + "@renternews.net",
          "DTSTAMP:" + new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z", "DTSTART;VALUE=DATE:" + d(r), "DTEND;VALUE=DATE:" + d(next),
          "SUMMARY:Lease notice due " + deadline.toLocaleDateString("en-US"), "DESCRIPTION:Give written move-out notice by " + deadline.toDateString() + ". Calculated at renternews.net/tools/lease-notice-calculator/",
          "BEGIN:VALARM", "TRIGGER:-PT0M", "ACTION:DISPLAY", "DESCRIPTION:Lease notice reminder", "END:VALARM", "END:VEVENT", "END:VCALENDAR"].join("\r\n");
        var a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([ics], { type: "text/calendar" })); a.download = "lease-notice-reminder.ics"; a.click();
      });
      live(calc);
    },

    /* ---------- Fire safety checklist ---------- */
    "fire-safety-checklist": function () {
      var GROUPS = [
        ["Alarms", [["alarm-bed", 12, "Working smoke alarm inside or right outside every sleeping area", "Test monthly with the test button."],
          ["alarm-test", 8, "I tested my smoke alarms in the last month", "Report broken or missing alarms to your landlord in writing."],
          ["co", 8, "Working carbon monoxide alarm (if the building has gas appliances or an attached garage)", ""]]],
        ["Escape", [["plan", 10, "I know two ways out of my apartment and the building", "Walk the route; count doors to the nearest stairwell."],
          ["exits", 8, "Doors, hallways and windows used for escape are not blocked", ""],
          ["stairs", 6, "I know to use stairs, not elevators, in a fire", ""],
          ["meet", 4, "Household has an outside meeting place", ""]]],
        ["Kitchen", [["cook", 10, "I stay in the kitchen when frying, grilling or boiling", "Unattended cooking is a leading cause of home fires."],
          ["lid", 5, "I keep a lid nearby to smother a pan fire (never water on grease)", ""],
          ["clear", 4, "Towels, paper and packaging are kept away from the stovetop", ""]]],
        ["Heat & power", [["heater", 7, "Space heaters are 3 feet from anything that can burn and plugged into the wall", ""],
          ["cords", 5, "No overloaded power strips or cords under rugs", ""],
          ["battery", 6, "E-bike / scooter batteries are charged while I'm awake, with the original charger, away from exits", ""],
          ["candles", 4, "Candles are never left unattended", ""]]],
        ["Ready", [["ext", 5, "I have a fire extinguisher and know how to use it (PASS)", ""],
          ["ins", 6, "I have renters insurance and an inventory of my belongings", ""],
          ["docs", 2, "Copies of IDs and important documents are stored in the cloud", ""]]]
      ];
      var state = store("rn-fire") || {}, box = $("[data-checklist]");
      box.innerHTML = GROUPS.map(function (g) {
        return '<div class="cl-group"><h3>' + g[0] + "</h3>" + g[1].map(function (it) {
          return '<label class="cl-item"><input type="checkbox" data-id="' + it[0] + '"' + (state[it[0]] ? " checked" : "") + "><span>" + it[2] + (it[3] ? "<small>" + it[3] + "</small>" : "") + "</span></label>";
        }).join("") + "</div>";
      }).join("");
      var all = [].concat.apply([], GROUPS.map(function (g) { return g[1]; })), totalW = all.reduce(function (s, x) { return s + x[1]; }, 0), ring = $(".r-fill");
      function calc() {
        var got = 0, todo = [];
        all.forEach(function (it) {
          var cb = $('[data-id="' + it[0] + '"]'); state[it[0]] = cb.checked;
          cb.closest(".cl-item").classList.toggle("is-done", cb.checked);
          if (cb.checked) got += it[1]; else todo.push(it);
        });
        store("rn-fire", state);
        var score = Math.round(got / totalW * 100);
        out("score", score);
        ring.style.strokeDashoffset = 327 * (1 - score / 100);
        ring.style.stroke = score >= 80 ? "#0f9d8a" : score >= 50 ? "#e0b520" : "#e4572e";
        out("grade", score >= 90 ? "Excellent — you're well prepared." : score >= 70 ? "Good — a few gaps to close." : score >= 40 ? "Fair — fix the top items this week." : "At risk — start with your smoke alarms and escape plan.");
        todo.sort(function (a, b) { return b[1] - a[1]; });
        $("[data-todo]").innerHTML = todo.length ? todo.slice(0, 5).map(function (t) { return "<li>" + t[2] + "</li>"; }).join("") : "<li>Nothing left. Re-check monthly!</li>";
      }
      $("[data-reset]").addEventListener("click", function () { $$("[data-id]").forEach(function (c) { c.checked = false; }); calc(); });
      box.addEventListener("change", calc); calc();
    }
  };
  bindRanges();
  var fn = tools[root.dataset.tool]; if (fn) fn();
})();
