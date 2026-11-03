/* Enforce Interest — calculators. Each tool is a [data-tool] container; all maths runs in the browser.
   Dates are handled as UTC midnights so daylight-saving changes never shift a day count. */
(function () {
  "use strict";
  var d = document, w = window;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var RATES = w.EI_RATES || {};
  var DAY = 864e5;

  /* ------------------------------------------------------------ utilities */
  function pd(s) { if (!s) return null; var p = s.split("-"); if (p.length !== 3) return null; var t = Date.UTC(+p[0], +p[1] - 1, +p[2]); return isNaN(t) ? null : new Date(t); }
  function iso(dt) { return dt ? dt.toISOString().slice(0, 10) : ""; }
  function today() { var n = new Date(); return new Date(Date.UTC(n.getFullYear(), n.getMonth(), n.getDate())); }
  function addDays(dt, n) { return new Date(dt.getTime() + n * DAY); }
  function diff(a, b) { return Math.round((b - a) / DAY); }
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  function fd(dt) { return dt ? MON[dt.getUTCMonth()] + " " + dt.getUTCDate() + ", " + dt.getUTCFullYear() : "—"; }
  function money(n) { return (n < 0 ? "-$" : "$") + Math.abs(n).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
  function num(v) { var n = parseFloat(String(v || "").replace(/[$,\s]/g, "")); return isNaN(n) ? 0 : n; }
  function pct(n) { return n.toFixed(2) + "%"; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function latestKey() { var k = Object.keys(RATES).sort(); return k[k.length - 1]; }
  function monthName(key) { var p = key.split("-"); return ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][+p[1] - 1] + " " + p[0]; }
  function rel(dt) { var n = diff(today(), dt); return n === 0 ? "today" : n > 0 ? "in " + n + " day" + (n === 1 ? "" : "s") : -n + " day" + (n === -1 ? "" : "s") + " ago"; }
  function val(form, name) { var el = form.elements[name]; if (!el) return ""; if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value; return ""; } return el.type === "checkbox" ? el.checked : el.value; }

  /* Texas holidays (Gov't Code §662.003(a)-(b)); weekend holidays are not moved. */
  var holCache = {};
  function nth(y, m, wd, n) { // n-th weekday wd (0=Sun) of month m; n=-1 => last
    if (n > 0) { var f = new Date(Date.UTC(y, m, 1)); var off = (wd - f.getUTCDay() + 7) % 7; return Date.UTC(y, m, 1 + off + 7 * (n - 1)); }
    var l = new Date(Date.UTC(y, m + 1, 0)); return Date.UTC(y, m, l.getUTCDate() - ((l.getUTCDay() - wd + 7) % 7));
  }
  function holidays(y) {
    if (holCache[y]) return holCache[y];
    var thx = nth(y, 10, 4, 4), s = {};
    [Date.UTC(y, 0, 1), nth(y, 0, 1, 3), Date.UTC(y, 0, 19), nth(y, 1, 1, 3), Date.UTC(y, 2, 2), Date.UTC(y, 3, 21),
      nth(y, 4, 1, -1), Date.UTC(y, 5, 19), Date.UTC(y, 6, 4), Date.UTC(y, 7, 27), nth(y, 8, 1, 1), Date.UTC(y, 10, 11),
      thx, thx + DAY, Date.UTC(y, 11, 24), Date.UTC(y, 11, 25), Date.UTC(y, 11, 26)].forEach(function (t) { s[t] = 1; });
    return (holCache[y] = s);
  }
  function isBiz(dt) { var g = dt.getUTCDay(); return g !== 0 && g !== 6 && !holidays(dt.getUTCFullYear())[dt.getTime()]; }
  function addBiz(dt, n) { var c = 0, x = dt; while (c < n) { x = addDays(x, 1); if (isBiz(x)) c++; } return x; }

  /* ------------------------------------------------------------ interest engine
     component: {label, due:Date, amount, pays:[{date:Date, amount}]}
     Payments on/before the due date reduce the starting balance; later payments reduce it from their date. */
  function runComponent(c, rate, through) {
    var out = { label: c.label, segs: [], interest: 0, late: 0, ontime: 0, open: 0, maxDays: 0 };
    if (!c.due || !(c.amount > 0)) return out;
    var pays = c.pays.filter(function (p) { return p.date && p.amount > 0; }).sort(function (a, b) { return a.date - b.date; });
    var bal = c.amount;
    pays.forEach(function (p) { if (p.date <= c.due) { bal -= p.amount; out.ontime += p.amount; } });
    bal = Math.max(0, bal);
    out.late = bal;
    var cur = c.due;
    pays.forEach(function (p) {
      if (p.date <= c.due || bal <= 0 || p.date > through) return;
      var days = diff(cur, p.date), i = bal * rate / 100 / 365 * days;
      out.segs.push({ label: c.label, from: cur, to: p.date, bal: bal, days: days, interest: i, open: false });
      out.interest += i; out.maxDays = Math.max(out.maxDays, diff(c.due, p.date));
      bal = Math.max(0, bal - p.amount); cur = p.date;
    });
    if (bal > 0 && through > cur) {
      var days = diff(cur, through), i = bal * rate / 100 / 365 * days;
      out.segs.push({ label: c.label, from: cur, to: through, bal: bal, days: days, interest: i, open: true });
      out.interest += i; out.maxDays = Math.max(out.maxDays, diff(c.due, through));
    }
    out.open = bal;
    return out;
  }

  function fillTable(tbl, segs) {
    var tb = $("tbody", tbl); if (!tb) return;
    tb.innerHTML = segs.length ? segs.map(function (s) {
      return "<tr><td>" + esc(s.label) + "<br><span style='opacity:.6'>" + fd(s.from) + " → " + (s.open ? "<b>" + fd(s.to) + "*</b>" : fd(s.to)) + "</span></td><td>" + money(s.bal) + "</td><td>" + s.days + "</td><td>" + money(s.interest) + "</td></tr>";
    }).join("") : "<tr><td colspan='4' style='text-align:left;opacity:.6'>No late periods yet.</td></tr>";
  }

  function download(name, text, type) {
    var b = new Blob([text], { type: type || "text/csv" }), a = d.createElement("a");
    a.href = URL.createObjectURL(b); a.download = name; d.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 100);
  }
  function copyText(t, btn) {
    var done = function () { if (btn) { var o = btn.textContent; btn.textContent = "Copied ✓"; setTimeout(function () { btn.textContent = o; }, 1600); } };
    if (navigator.clipboard && w.isSecureContext) navigator.clipboard.writeText(t).then(done, function () { fallback(); });
    else fallback();
    function fallback() { var ta = d.createElement("textarea"); ta.value = t; d.body.appendChild(ta); ta.select(); try { d.execCommand("copy"); done(); } catch (e) { } ta.remove(); }
  }
  function enc(o) { try { return btoa(unescape(encodeURIComponent(JSON.stringify(o)))); } catch (e) { return ""; } }
  function dec(s) { try { return JSON.parse(decodeURIComponent(escape(atob(s)))); } catch (e) { return null; } }
  function rateFromMonth(sel) { var k = sel && sel.value ? sel.value : latestKey(); return { key: k, base: RATES[k] || 0, float: (RATES[k] || 0) + 5 }; }
  function wireActions(root, api) {
    $$("[data-act]", root).forEach(function (b) {
      b.addEventListener("click", function () {
        var a = b.dataset.act;
        if (a === "print") w.print();
        else if (a === "copy" && api.text) copyText(api.text(), b);
        else if (a === "csv" && api.csv) download(api.csvName || "enforce-interest.csv", api.csv());
        else if (a === "link" && api.state) { var u = location.origin + location.pathname + "#s=" + enc(api.state()); history.replaceState(null, "", u); copyText(u, b); }
      });
    });
  }
  function payRow(list, tpl, date, amount) {
    var n = tpl.content.firstElementChild.cloneNode(true);
    if (date) $("[data-p=date]", n).value = date;
    if (amount) $("[data-p=amount]", n).value = amount;
    list.appendChild(n); return n;
  }
  function readPays(root) { return $$("[data-pay]", root).map(function (r) { return { date: pd($("[data-p=date]", r).value), amount: num($("[data-p=amount]", r).value) }; }); }
  function showByMode(root, mode) { $$("[data-show]", root).forEach(function (el) { el.hidden = el.dataset.show !== mode; }); }

  /* ============================================================ LEDGER (main calculator) */
  function ledger(root) {
    var form = $("form", root), wrap = $("[data-components]", root);
    var tplC = $("#tpl-component", root), tplP = $("#tpl-pay", root);
    var out = function (k) { return $('[data-out="' + k + '"]', root); };
    var note = $("[data-regime-note]", root), floatOnly = $("[data-float-only]", root);
    var last = null;
    form.elements.through.value = iso(today());

    function addComponent(c) {
      var n = tplC.content.firstElementChild.cloneNode(true), list = $("[data-pays]", n);
      var idx = $$("[data-component]", wrap).length;
      $$('input[data-c="mode"]', n).forEach(function (r) { r.name = "mode" + Date.now() + idx; });
      $("[data-c=label]", n).value = c && c.label || (idx ? "Supplement " + idx : "Original claim");
      if (c) {
        $$('input[data-c="mode"]', n).forEach(function (r) { r.checked = r.value === (c.mode || "due"); });
        $("[data-c=due]", n).value = c.due || ""; $("[data-c=items]", n).value = c.items || "";
        $("[data-c=cat]", n).checked = !!c.cat; $("[data-c=amount]", n).value = c.amount || "";
        (c.pays || []).forEach(function (p) { payRow(list, tplP, p[0], p[1]); });
      }
      if (!$$("[data-pay]", list).length) payRow(list, tplP);
      wrap.appendChild(n);
      showByMode(n, (c && c.mode) || "due");
      return n;
    }
    function readComponents() {
      return $$("[data-component]", wrap).map(function (n) {
        var mode = ($('input[data-c="mode"]:checked', n) || {}).value || "due";
        var due = null;
        if (mode === "due") due = pd($("[data-c=due]", n).value);
        else { var it = pd($("[data-c=items]", n).value); if (it) due = addDays(it, 60 + ($("[data-c=cat]", n).checked ? 15 : 0)); }
        return { node: n, label: $("[data-c=label]", n).value || "Component", mode: mode, due: due, amount: num($("[data-c=amount]", n).value), pays: readPays(n) };
      });
    }
    function regime() {
      var r = val(form, "regime"), cause = val(form, "cause"), made = pd(form.elements.claimMade.value), cut = pd("2017-09-01");
      var auto = cause === "weather" && (!made || made >= cut) ? "float" : "std";
      var eff = r === "auto" ? auto : r, msg;
      if (r === "auto") {
        if (cause === "weather" && made && made < cut) msg = "<strong>18% applies.</strong> A weather claim made before September 1, 2017 keeps the §542.060(a) rate (HB 1774, §4(b)).";
        else if (cause === "weather") msg = "<strong>Floating rate applies.</strong> Forces-of-nature claims made on or after September 1, 2017 use §542.060(c): the §304.003 rate plus 5%." + (made ? "" : " (Enter the date the claim was made to confirm.)");
        else msg = "<strong>18% applies.</strong> Non-weather claims use §542.060(a).";
      } else msg = eff === "float" ? "<strong>Floating rate selected</strong> (§542.060(c))." : "<strong>18% selected</strong> (§542.060(a)).";
      floatOnly.hidden = eff !== "float";
      var fr = rateFromMonth(form.elements.rateMonth);
      var rate = eff === "float" ? fr.float : 18;
      note.innerHTML = msg + (eff === "float" ? " Using " + monthName(fr.key) + ": " + pct(fr.base) + " + 5% = <strong>" + pct(fr.float) + "</strong>." : "");
      return { eff: eff, rate: rate, key: fr.key };
    }
    function calc() {
      var rg = regime(), through = pd(form.elements.through.value) || today();
      var comps = readComponents(), res = comps.map(function (c) {
        var lbl = $("[data-c=due]", c.node).closest(".field").querySelector(".help");
        if (c.mode === "items" && c.due) $("[data-c=items]", c.node).closest(".field").querySelector(".help").textContent = "Deadline = " + fd(c.due) + " (§542.058" + ($("[data-c=cat]", c.node).checked ? " + 15 days" : "") + ").";
        return runComponent(c, rg.rate, through);
      });
      var total = 0, late = 0, maxD = 0, open = 0, owed = 0, segs = [];
      res.forEach(function (r, i) { total += r.interest; late += r.late; maxD = Math.max(maxD, r.maxDays); open += r.open; owed += comps[i].amount; segs = segs.concat(r.segs); });
      out("total").textContent = money(total);
      out("rate").textContent = pct(rg.rate) + (rg.eff === "float" ? " (floating)" : " (§542.060(a))");
      out("late").textContent = late ? money(late) : "—";
      out("days").textContent = maxD ? maxD + " days" : "—";
      out("perday").textContent = open ? money(open * rg.rate / 100 / 365) + " on " + money(open) : "—";
      out("grand").textContent = owed ? money(owed + total) : "—";
      out("sub").textContent = comps.some(function (c) { return c.due && c.amount; })
        ? (total > 0 ? "Simple interest at " + pct(rg.rate) + " a year, through " + fd(through) + "." : "No amount was paid after its deadline (or the deadline is after the through date).")
        : "Enter a deadline and an amount to begin.";
      fillTable(out("table"), segs);
      $("[data-note]", root).textContent = segs.some(function (s) { return s.open; }) ? "* Still unpaid: interest shown through the 'accrue through' date and continues daily." : "";
      last = { rg: rg, through: through, comps: comps, res: res, total: total, segs: segs, owed: owed };
    }
    function state() {
      var f = {}; ["insured", "carrier", "claimref", "claimMade", "through"].forEach(function (k) { f[k] = form.elements[k].value; });
      f.cause = val(form, "cause"); f.regime = val(form, "regime"); f.rateMonth = form.elements.rateMonth.value;
      return { f: f, c: $$("[data-component]", wrap).map(function (n) {
        return { label: $("[data-c=label]", n).value, mode: ($('input[data-c="mode"]:checked', n) || {}).value, due: $("[data-c=due]", n).value, items: $("[data-c=items]", n).value, cat: $("[data-c=cat]", n).checked, amount: $("[data-c=amount]", n).value,
          pays: $$("[data-pay]", n).map(function (r) { return [$("[data-p=date]", r).value, $("[data-p=amount]", r).value]; }) };
      }) };
    }
    function restore(s) {
      var f = s.f || {};
      ["insured", "carrier", "claimref", "claimMade", "through"].forEach(function (k) { if (f[k] !== undefined) form.elements[k].value = f[k]; });
      ["cause", "regime"].forEach(function (k) { $$('input[name="' + k + '"]', form).forEach(function (r) { r.checked = r.value === f[k]; }); });
      if (f.rateMonth) form.elements.rateMonth.value = f.rateMonth;
      wrap.innerHTML = ""; (s.c || []).forEach(addComponent);
    }
    function text() {
      if (!last) return "";
      var f = form.elements, L = [];
      L.push("STATEMENT OF STATUTORY INTEREST — Tex. Ins. Code §542.060" + (last.rg.eff === "float" ? "(c)" : "(a)"));
      if (f.insured.value) L.push("Insured: " + f.insured.value);
      if (f.carrier.value) L.push("Carrier: " + f.carrier.value);
      if (f.claimref.value) L.push("Claim no.: " + f.claimref.value);
      L.push("Rate: " + pct(last.rg.rate) + " per year, simple" + (last.rg.eff === "float" ? " (§304.003 " + monthName(last.rg.key) + " + 5%)" : ""));
      L.push("Interest through: " + fd(last.through)); L.push("");
      last.comps.forEach(function (c, i) {
        var r = last.res[i]; if (!c.due) return;
        L.push(c.label + ": owed " + money(c.amount) + ", payment due " + fd(c.due) + ", paid by deadline " + money(r.ontime) + ", interest " + money(r.interest));
        r.segs.forEach(function (s) { L.push("   " + fd(s.from) + " to " + fd(s.to) + (s.open ? " (unpaid)" : "") + ": " + money(s.bal) + " x " + s.days + " days = " + money(s.interest)); });
      });
      L.push(""); L.push("TOTAL STATUTORY INTEREST: " + money(last.total));
      L.push("Prepared with the Enforce Interest calculator (enforceinterest.com). Estimate only; not legal advice.");
      return L.join("\n");
    }
    function csv() {
      var rows = [["Component", "From", "To", "Balance", "Days", "Rate %", "Interest", "Status"]];
      (last ? last.segs : []).forEach(function (s) { rows.push([s.label, iso(s.from), iso(s.to), s.bal.toFixed(2), s.days, last.rg.rate.toFixed(2), s.interest.toFixed(2), s.open ? "unpaid" : "paid"]); });
      rows.push(["TOTAL", "", "", "", "", "", last ? last.total.toFixed(2) : "0", ""]);
      return rows.map(function (r) { return r.map(function (c) { return '"' + String(c).replace(/"/g, '""') + '"'; }).join(","); }).join("\n");
    }

    root.addEventListener("click", function (e) {
      var t = e.target;
      if (t.closest("[data-add-component]")) { addComponent(); calc(); }
      else if (t.closest("[data-remove-component]")) { if ($$("[data-component]", wrap).length > 1) t.closest("[data-component]").remove(); calc(); }
      else if (t.closest("[data-add-pay]")) { payRow($("[data-pays]", t.closest("[data-component]")), tplP); }
      else if (t.closest("[data-remove-pay]")) { t.closest("[data-pay]").remove(); calc(); }
    });
    root.addEventListener("input", calc);
    root.addEventListener("change", function (e) {
      if (e.target.matches('input[data-c="mode"]')) showByMode(e.target.closest("[data-component]"), e.target.value);
      calc();
    });
    var h = location.hash.match(/s=([^&]+)/), s = h && dec(h[1]);
    if (s) restore(s);
    else addComponent({ label: "Original claim", mode: "due", due: iso(addDays(today(), -150)), amount: "50000", pays: [[iso(addDays(today(), -170)), "20000"], [iso(addDays(today(), -60)), "30000"]] });
    wireActions(root, { text: text, csv: csv, state: state, csvName: "statutory-interest.csv" });
    calc();
  }

  /* ============================================================ DEADLINES */
  function deadlines(root) {
    var form = $("form", root), tl = $('[data-out="tl"]', root), head = $('[data-out="headline"]', root), last = [];
    function calc() {
      var g = function (k) { return pd(form.elements[k].value); };
      var N = g("notice"), I = g("items"), A = g("accept"), E = g("extension"), L = g("loss");
      var S = form.elements.surplus.checked, C = form.elements.cat.checked ? 15 : 0, ar = form.elements.arson.checked;
      var twia = form.elements.twia.checked, wx = form.elements.weather.checked, lim = form.elements.limit.value;
      var items = [];
      var add = function (date, label, cite, note, est) { if (date) items.push({ date: date, label: label, cite: cite, note: note || "", est: !!est }); };
      if (L) add(L, "Date of loss", "", "");
      if (N) add(N, "Written notice of claim given", "§542.051(4)", "");
      if (twia) {
        if (L) add(addDays(new Date(Date.UTC(L.getUTCFullYear() + 1, L.getUTCMonth(), L.getUTCDate())), 0), "Last day to file a TWIA claim", "§2210.573(a)", "Extendable up to 180 days for good cause (§2210.205(b)).");
        if (N) add(addDays(N, 30), "TWIA may request information by", "§2210.573(b)", "");
        var base = I || N;
        if (base) add(addDays(base, 60), "TWIA must accept or deny by", "§2210.573(d)", I ? "60 days after receiving requested information." : "60 days after receiving the claim (later if TWIA requests information).", !I);
        if (A) add(addDays(A, 10), "TWIA must pay the accepted amount by", "§2210.5731", "");
      } else {
        if (N) add(addDays(S ? addBiz(N, 30) : addDays(N, 15), C), "Acknowledge, investigate & request items by", "§542.055", S ? "30 business days (surplus lines)." : "15 days after notice." + (C ? " +15 catastrophe days." : ""));
        if (I) add(addDays(ar ? addDays(I, 30) : addBiz(I, 15), C), "Accept or reject in writing by", ar ? "§542.056(b)" : "§542.056(a)", ar ? "30 days (arson suspected)." : "15 business days after the last requested item.");
        if (E) add(addDays(addDays(E, 45), C), "Decision due after 'more time' notice", "§542.056(d)", "45 days after the insurer's notice.");
        if (A) add(addDays(S ? addBiz(A, 20) : addBiz(A, 5), C), "Pay the accepted amount by", "§542.057", S ? "20 business days (surplus lines)." : "5 business days after notice of acceptance.");
        if (I) add(addDays(I, 60 + C), "60-day payment deadline", "§542.058", "Payment after this date is late; interest accrues under §542.060.");
        else if (N) add(addDays(N, 60 + C), "60-day deadline (estimate: if no items were requested)", "§542.058", "Enter the items-received date for the real deadline.", true);
        if (wx) add(addDays(today(), 61), "Earliest suit date if a 542A notice is received today", "§542A.003", "Weather claims: notice at least 61 days before filing.");
      }
      if (L) {
        var yrs = lim === "4y" ? 4 : 2, end = new Date(Date.UTC(L.getUTCFullYear() + yrs, L.getUTCMonth(), L.getUTCDate()));
        if (lim === "2y1d") end = addDays(end, 1);
        add(end, "Cautious planning date for suit limitation", lim === "4y" ? "4-year contract statute" : "policy / §16.070", "Measured from the date of loss; accrual may be later. Confirm with an attorney.");
      }
      items.sort(function (a, b) { return a.date - b.date; });
      var t = today();
      tl.innerHTML = items.map(function (it) {
        var past = it.date < t, isDeadline = /by|deadline|due|Last day/i.test(it.label);
        return '<li class="' + (past ? (isDeadline ? "late" : "past") : "") + '"><b>' + esc(it.label) + (it.est ? " (est.)" : "") + '</b><span class="d">' + fd(it.date) + " · " + rel(it.date) + "</span>" +
          '<span class="x">' + (it.cite ? it.cite + " — " : "") + esc(it.note) + "</span></li>";
      }).join("");
      var nextD = items.filter(function (it) { return it.date >= t && /by|deadline|due|Last day/i.test(it.label); })[0];
      head.textContent = !N && !L ? "Enter your notice date" : nextD ? "Next: " + nextD.label.replace(/ by$/, "") + " — " + fd(nextD.date) : "All listed deadlines have passed";
      last = items;
    }
    function text() { return "TEXAS CLAIM DEADLINES (Enforce Interest)\n" + last.map(function (i) { return fd(i.date) + "  " + i.label + (i.cite ? " [" + i.cite + "]" : ""); }).join("\n") + "\nEstimates only; not legal advice."; }
    function csv() { return "Date,Event,Authority,Note\n" + last.map(function (i) { return [iso(i.date), i.label, i.cite, i.note].map(function (c) { return '"' + String(c).replace(/"/g, '""') + '"'; }).join(","); }).join("\n"); }
    function state() { var o = {}; $$("input,select", form).forEach(function (el) { o[el.name] = el.type === "checkbox" ? el.checked : el.value; }); return o; }
    var h = location.hash.match(/s=([^&]+)/), s = h && dec(h[1]);
    if (s) Object.keys(s).forEach(function (k) { var el = form.elements[k]; if (!el) return; if (el.type === "checkbox") el.checked = s[k]; else el.value = s[k]; });
    else { form.elements.loss.value = iso(addDays(today(), -75)); form.elements.notice.value = iso(addDays(today(), -70)); form.elements.items.value = iso(addDays(today(), -40)); }
    root.addEventListener("input", calc); root.addEventListener("change", calc);
    wireActions(root, { text: text, csv: csv, state: state, csvName: "claim-deadlines.csv" });
    calc();
  }

  /* ============================================================ APPRAISAL */
  function appraisal(root) {
    var form = $("form", root), list = $("[data-pays]", root), tplP = $("#tpl-pay", root), last = null;
    var out = function (k) { return $('[data-out="' + k + '"]', root); };
    function calc() {
      var mode = val(form, "mode"); showByMode(form, mode);
      var due = mode === "due" ? pd(form.elements.due.value) : (pd(form.elements.items.value) ? addDays(pd(form.elements.items.value), 60 + (form.elements.cat.checked ? 15 : 0)) : null);
      var reg = val(form, "regime"); $("[data-float-only]", root).hidden = reg !== "float";
      var fr = rateFromMonth(form.elements.rateMonth), rate = reg === "float" ? fr.float : 18;
      var owed = Math.max(0, num(form.elements.award.value) - num(form.elements.deductible.value));
      var paidOn = pd(form.elements.awardPaid.value);
      var pays = readPays(list).filter(function (p) { return p.date && p.amount > 0; });
      var prior = pays.reduce(function (s, p) { return s + p.amount; }, 0);
      var all = pays.slice(); if (paidOn && owed - prior > 0) all.push({ date: paidOn, amount: owed - prior });
      var r = runComponent({ label: "Award balance", due: due, amount: owed, pays: all }, rate, paidOn || today());
      var paidInt = num(form.elements.paidInterest.value);
      out("total").textContent = money(r.interest);
      out("owed").textContent = owed ? money(owed) : "—";
      out("ontime").textContent = due ? money(r.ontime) : "—";
      out("late").textContent = due ? money(r.late) : "—";
      out("rate").textContent = pct(rate) + (reg === "float" ? " (" + monthName(fr.key) + " + 5%)" : "");
      out("paidInt").textContent = money(paidInt);
      out("short").textContent = money(Math.max(0, r.interest - paidInt));
      out("sub").textContent = due && owed && paidOn ? (r.late > 0 ? money(r.late) + " was unpaid at the deadline (" + fd(due) + "); interest runs until each later payment." : "Everything owed was paid by the deadline.") : "Enter the award, the payments and the dates.";
      fillTable(out("table"), r.segs);
      $("[data-note]", root).textContent = paidInt && r.interest > paidInt ? "The interest paid is " + money(r.interest - paidInt) + " less than this estimate." : paidInt ? "The interest paid covers this estimate." : "";
      last = { r: r, rate: rate, due: due, owed: owed, paidInt: paidInt };
    }
    function text() { if (!last) return ""; return ["POST-APPRAISAL INTEREST ESTIMATE (Enforce Interest)", "Owed under award (after deductible): " + money(last.owed), "Payment deadline: " + fd(last.due), "Rate: " + pct(last.rate)].concat(last.r.segs.map(function (s) { return fd(s.from) + " to " + fd(s.to) + ": " + money(s.bal) + " x " + s.days + " days = " + money(s.interest); })).concat(["Total interest: " + money(last.r.interest), "Interest already paid: " + money(last.paidInt), "Shortfall: " + money(Math.max(0, last.r.interest - last.paidInt)), "Estimate only; not legal advice."]).join("\n"); }
    function csv() { return "From,To,Balance,Days,Rate,Interest\n" + (last ? last.r.segs.map(function (s) { return [iso(s.from), iso(s.to), s.bal.toFixed(2), s.days, last.rate.toFixed(2), s.interest.toFixed(2)].join(","); }).join("\n") : ""); }
    function state() { var o = { f: {} }; $$("input,select", form).forEach(function (el) { if (!el.name) return; if (el.type === "radio") { if (el.checked) o.f[el.name] = el.value; } else o.f[el.name] = el.type === "checkbox" ? el.checked : el.value; }); o.p = $$("[data-pay]", list).map(function (r) { return [$("[data-p=date]", r).value, $("[data-p=amount]", r).value]; }); return o; }
    root.addEventListener("click", function (e) { if (e.target.closest("[data-add-pay]")) payRow(list, tplP); else if (e.target.closest("[data-remove-pay]")) { e.target.closest("[data-pay]").remove(); calc(); } });
    root.addEventListener("input", calc); root.addEventListener("change", calc);
    var h = location.hash.match(/s=([^&]+)/), s = h && dec(h[1]);
    if (s) { Object.keys(s.f || {}).forEach(function (k) { var el = form.elements[k]; if (!el) return; if (el.length && !el.tagName) $$('input[name="' + k + '"]', form).forEach(function (r) { r.checked = r.value === s.f[k]; }); else if (el.type === "checkbox") el.checked = s.f[k]; else el.value = s.f[k]; }); (s.p || []).forEach(function (p) { payRow(list, tplP, p[0], p[1]); }); }
    else { form.elements.award.value = "226500"; form.elements.deductible.value = "2500"; form.elements.due.value = "2024-05-21"; form.elements.awardPaid.value = "2025-07-18"; payRow(list, tplP, "2024-05-10", "48000"); }
    wireActions(root, { text: text, csv: csv, state: state, csvName: "appraisal-interest.csv" });
    calc();
  }

  /* ============================================================ 542A */
  function notice542a(root) {
    var form = $("form", root), out = function (k) { return $('[data-out="' + k + '"]', root); };
    function calc() {
      var N = pd(form.elements.noticeDate.value), S = pd(form.elements.suitDate.value), items = [];
      if (N) {
        items.push(["Insurer receives the notice", N, ""]);
        items.push(["Insurer's last day to request an inspection", addDays(N, 30), "§542A.004"]);
        items.push(["Inspection to be completed (if reasonably possible)", addDays(N, 60), "§542A.004"]);
        items.push(["Earliest filing date", addDays(N, 61), "§542A.003(a)"]);
        if (S) items.push([diff(N, S) >= 61 ? "Planned filing date ✓" : "Planned filing date — too early", S, diff(N, S) + " days after notice"]);
        items.sort(function (a, b) { return a[1] - b[1]; });
        out("tl").innerHTML = items.map(function (i) { var bad = /too early/.test(i[0]); return '<li class="' + (bad ? "late" : i[1] < today() ? "past" : "") + '"><b>' + i[0] + '</b><span class="d">' + fd(i[1]) + " · " + rel(i[1]) + '</span><span class="x">' + i[2] + "</span></li>"; }).join("");
        out("headline").textContent = "File on or after " + fd(addDays(N, 61));
      } else { out("tl").innerHTML = ""; out("headline").textContent = "Enter the notice date"; }
      var dem = num(form.elements.demand.value), j = num(form.elements.judgment.value), fees = num(form.elements.fees.value);
      if (dem > 0) {
        var r = j / dem, rule, fee;
        if (r >= 0.8) { rule = "≥ 0.8: full fees"; fee = fees; }
        else if (r < 0.2) { rule = "< 0.2: no fees"; fee = 0; }
        else { rule = "Fees × ratio"; fee = Math.min(fees, fees * r); }
        out("ratio").textContent = r.toFixed(3); out("rule").textContent = rule; out("fee").textContent = money(fee);
      } else { out("ratio").textContent = "—"; out("rule").textContent = "—"; out("fee").textContent = "—"; }
    }
    form.elements.noticeDate.value = iso(today());
    root.addEventListener("input", calc); root.addEventListener("change", calc);
    wireActions(root, { text: function () { return $('[data-out="tl"]', root).innerText; }, csv: function () { return "Item,Value\nRatio," + out("ratio").textContent + "\nFees," + out("fee").textContent; }, state: function () { var o = {}; $$("input", form).forEach(function (e) { o[e.name] = e.value; }); return o; } });
    calc();
  }

  /* ============================================================ PA FEE */
  function pafee(root) {
    var form = $("form", root), out = function (k) { return $('[data-out="' + k + '"]', root); };
    function calc() {
      var O = num(form.elements.offer.value), S = num(form.elements.settle.value), p = num(form.elements.pct.value) / 100, tot = form.elements.feeOnTotal.checked;
      var fee = (tot ? S : Math.max(0, S - O)) * p, warn = "";
      if (p > 0.10 || fee > S * 0.10 + 0.005) warn = '<div class="warn">Above the Texas cap: total public adjuster compensation may not exceed 10% of the insurance settlement on the claim (§4102.104(a)).</div>';
      var net = S - fee;
      out("fee").textContent = money(fee); out("net").textContent = money(net);
      out("eff").textContent = S ? (fee / S * 100).toFixed(2) + "%" : "—";
      out("gain").textContent = O ? money(net - O) : "—";
      out("be").textContent = O ? (tot ? (p < 1 ? money(O / (1 - p)) : "—") : money(O) + " (any increase is net gain)") : "—";
      out("sub").textContent = S ? "On a " + money(S) + " settlement." : "Enter the settlement.";
      out("warn").innerHTML = warn;
    }
    root.addEventListener("input", calc); root.addEventListener("change", calc); calc();
  }

  /* ============================================================ DEPRECIATION */
  function depr(root) {
    var form = $("form", root), out = function (k) { return $('[data-out="' + k + '"]', root); };
    form.elements.preset.addEventListener("change", function () { if (form.elements.preset.value !== "custom") form.elements.life.value = form.elements.preset.value; });
    function calc() {
      var rcv = num(form.elements.rcv.value), age = num(form.elements.age.value), life = Math.max(0.5, num(form.elements.life.value)), cap = Math.min(100, num(form.elements.cap.value) || 100) / 100;
      var ded = num(form.elements.ded.value), pol = val(form, "policy");
      var dep = rcv * Math.min(age / life, cap), acv = rcv - dep, basis = pol === "rcv" ? rcv : acv;
      var total = Math.max(0, basis - ded), first = Math.max(0, acv - ded), rec = Math.max(0, total - first);
      out("first").textContent = money(first); out("dep").textContent = money(dep) + " (" + (rcv ? (dep / rcv * 100).toFixed(1) : "0") + "%)";
      out("acv").textContent = money(acv); out("rec").textContent = pol === "rcv" ? money(rec) : "None (ACV policy)";
      out("total").textContent = money(total);
      out("sub").textContent = pol === "rcv" ? "The holdback of " + money(rec) + " is usually paid after repairs are completed." : "An ACV policy doesn't pay depreciation back.";
    }
    root.addEventListener("input", calc); root.addEventListener("change", calc); calc();
  }

  /* ============================================================ DEDUCTIBLE */
  function deduct(root) {
    var form = $("form", root), out = function (k) { return $('[data-out="' + k + '"]', root); };
    function calc() {
      var t = val(form, "dtype"); showByMode(form, t);
      var cov = num(form.elements.covA.value), ded = t === "pct" ? cov * num(form.elements.pct.value) / 100 : num(form.elements.flat.value);
      var loss = num(form.elements.loss.value), dep = num(form.elements.dep.value);
      out("ded").textContent = money(ded); out("loss").textContent = money(loss);
      out("pay").textContent = money(Math.max(0, loss - ded)); out("first").textContent = money(Math.max(0, loss - dep - ded));
      out("sub").textContent = t === "pct" ? num(form.elements.pct.value) + "% of a " + money(cov) + " dwelling limit." : "Flat deductible.";
      out("warn").innerHTML = loss && loss <= ded ? '<div class="warn">The estimated damage is at or below the deductible, so the policy would pay nothing for this loss.</div>' : loss && loss - ded < ded ? '<div class="ok">The claim pays ' + money(loss - ded) + " after the deductible.</div>" : "";
    }
    root.addEventListener("input", calc); root.addEventListener("change", calc); calc();
  }

  /* ============================================================ PREJUDGMENT */
  function prejudgment(root) {
    var form = $("form", root), out = function (k) { return $('[data-out="' + k + '"]', root); };
    form.elements.notice.value = "2025-03-01"; form.elements.suit.value = "2026-01-10"; form.elements.judg.value = iso(addDays(today(), 12));
    function calc() {
      var amt = num(form.elements.amt.value), N = pd(form.elements.notice.value), S = pd(form.elements.suit.value), J = pd(form.elements.judg.value);
      var fr = rateFromMonth(form.elements.rateMonth), r = fr.base;
      var cands = []; if (N) cands.push(addDays(N, 180)); if (S) cands.push(S);
      var start = cands.length ? new Date(Math.min.apply(null, cands)) : null, end = J ? addDays(J, -1) : null;
      var days = start && J ? Math.max(0, diff(start, J)) : 0;
      var i = amt * r / 100 / 365 * days;
      var O = num(form.elements.offer.value), of = pd(form.elements.offerFrom.value), ot = pd(form.elements.offerTo.value);
      if (O && of && ot && start && J) {
        var a = Math.max(of, start), b = Math.min(ot, J), ov = Math.max(0, diff(new Date(a), new Date(b)));
        i -= Math.min(amt, O) * r / 100 / 365 * ov;
      }
      i = Math.max(0, i);
      out("total").textContent = money(i); out("start").textContent = fd(start); out("end").textContent = fd(end);
      out("days").textContent = days || "—"; out("rate").textContent = pct(r) + " (" + monthName(fr.key) + ")";
      out("post").textContent = money((amt + i) * r / 100 / 365);
      out("sub").textContent = start ? "Accrual begins on the " + (N && S && addDays(N, 180) < S ? "180th day after notice" : "date suit was filed") + "." : "Enter the notice or filing date.";
    }
    root.addEventListener("input", calc); root.addEventListener("change", calc); calc();
  }

  /* ============================================================ RATE LOOKUP */
  function ratelookup(root) {
    var form = $("form", root), out = function (k) { return $('[data-out="' + k + '"]', root); };
    function calc() {
      var k = form.elements.y.value + "-" + form.elements.m.value, r = RATES[k], a = num(form.elements.amt.value);
      if (r === undefined) { out("rate").textContent = "n/a"; out("sub").textContent = "No rate published for " + monthName(k) + " yet."; ["float", "d1", "d2", "d3"].forEach(function (x) { out(x).textContent = "—"; }); return; }
      out("rate").textContent = pct(r); out("sub").textContent = "For judgments rendered in " + monthName(k) + ".";
      out("float").textContent = pct(r + 5) + (k < "2017-09" ? " (not yet in force)" : "");
      out("d1").textContent = a ? money(a * r / 36500) : "—"; out("d2").textContent = a ? money(a * (r + 5) / 36500) : "—"; out("d3").textContent = a ? money(a * 18 / 36500) : "—";
    }
    root.addEventListener("input", calc); root.addEventListener("change", calc); calc();
  }

  /* ============================================================ TIMELINE BUILDER */
  function timeline(root) {
    var KEY = "ei-timeline-v1", st = { meta: {}, events: [] };
    try { st = JSON.parse(localStorage.getItem(KEY)) || st; } catch (e) { }
    var out = function (k) { return $('[data-out="' + k + '"]', root); }, letter = $("[data-letter]", root);
    var LABEL = { notice: "Claim reported (notice)", ack: "Insurer acknowledged", request: "Insurer requested information", sent: "Requested documents sent", inspect: "Inspection", extension: "Insurer: needs more time", accept: "Insurer accepted", deny: "Insurer denied", payment: "Payment received", supplement: "Supplement submitted", appraisal: "Appraisal demanded", award: "Appraisal award", call: "Call / email", other: "Other" };
    $$("[data-meta]", root).forEach(function (el) { el.value = st.meta[el.dataset.meta] || ""; el.addEventListener("input", function () { st.meta[el.dataset.meta] = el.value; save(); }); });
    function save() { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { } render(); }
    function render() {
      var ev = st.events.map(function (e) { return { e: e, date: pd(e.date) }; }).filter(function (x) { return x.date; }).sort(function (a, b) { return a.date - b.date; });
      var marks = [], notice = ev.filter(function (x) { return x.e.type === "notice"; })[0];
      var sent = ev.filter(function (x) { return x.e.type === "sent"; }).pop(), accept = ev.filter(function (x) { return x.e.type === "accept"; })[0];
      var ack = ev.filter(function (x) { return x.e.type === "ack"; })[0];
      if (notice) marks.push({ date: addDays(notice.date, 15), label: "§542.055 acknowledgment deadline", met: ack && ack.date <= addDays(notice.date, 15) });
      var pay60 = sent ? addDays(sent.date, 60) : null, pay5 = accept ? addBiz(accept.date, 5) : null;
      if (sent) { marks.push({ date: addBiz(sent.date, 15), label: "§542.056 decision deadline (15 business days)" }); marks.push({ date: pay60, label: "§542.058 60-day payment deadline" }); }
      if (accept) marks.push({ date: pay5, label: "§542.057 payment due (5 business days after acceptance)" });
      var dueBy = [pay60, pay5].filter(Boolean).sort(function (a, b) { return a - b; })[0];
      var lateCount = 0, lateAmt = 0;
      var rows = ev.map(function (x) {
        var late = x.e.type === "payment" && dueBy && x.date > dueBy;
        if (late) { lateCount++; lateAmt += num(x.e.amt); }
        return { date: x.date, html: '<li class="' + (late ? "late" : "past") + '"><b>' + esc(LABEL[x.e.type] || x.e.type) + (x.e.amt ? " — " + money(num(x.e.amt)) : "") + '</b><span class="d">' + fd(x.date) + (late ? " · " + diff(dueBy, x.date) + " days after deadline" : "") + '</span>' + (x.e.note ? '<span class="x">' + esc(x.e.note) + "</span>" : "") + ' <button type="button" class="quiz-back" style="color:#ffb4a3;margin:4px 0 0" data-del="' + x.e.id + '">remove</button></li>' };
      }).concat(marks.map(function (m) {
        return { date: m.date, html: '<li style="opacity:.85"><b style="color:var(--gold-2)">⏱ ' + m.label + '</b><span class="d">' + fd(m.date) + " · " + rel(m.date) + "</span></li>" };
      })).sort(function (a, b) { return a.date - b.date; });
      out("tl").innerHTML = rows.map(function (r) { return r.html; }).join("");
      out("headline").textContent = !ev.length ? "No events yet" : lateCount ? lateCount + " payment" + (lateCount > 1 ? "s" : "") + " after a deadline" : "No late payment logged yet";
      out("sub").textContent = !ev.length ? "Add your first event, or load the example." : lateCount ? money(lateAmt) + " was paid after the earliest statutory payment deadline. Run it through the statutory interest calculator." : ev.length + " event" + (ev.length > 1 ? "s" : "") + " logged.";
      buildLetter(ev, sent, notice, dueBy);
    }
    function buildLetter(ev, sent, notice, dueBy) {
      var m = st.meta, reqs = ev.filter(function (x) { return x.e.type === "request"; });
      var paid = ev.filter(function (x) { return x.e.type === "payment"; }).reduce(function (s, x) { return s + num(x.e.amt); }, 0);
      var L = [fd(today()), "", (m.carrier || "[Insurance company]"), "Re: Claim no. " + (m.claimno || "[claim number]") + (m.loss ? ", date of loss " + fd(pd(m.loss)) : "") + (m.address ? ", " + m.address : ""), "", "Dear Claims Representative,", "",
        "I am writing to request a written update on the claim referenced above." + (notice ? " I reported this claim in writing on " + fd(notice.date) + "." : ""),
        sent ? "On " + fd(sent.date) + " I provided the items you requested" + (reqs.length ? " (most recently requested on " + fd(reqs[reqs.length - 1].date) + ")" : "") + "." : "",
        paid ? "To date I have received payments totaling " + money(paid) + "." : "",
        "", "Please tell me in writing:", "1. Whether you have accepted or rejected the claim, in whole or in part, and the reasons for any rejection;",
        "2. Any item, statement or form you still need from me to evaluate the claim; and", "3. The date and amount of any payment you will issue.", "",
        "As you know, Texas Insurance Code §§542.055-.058 set deadlines for acknowledging, deciding and paying first-party claims" + (dueBy ? ", and by my records payment was due by " + fd(dueBy) : "") + ". I would appreciate your response within ten days.", "",
        "Thank you,", "", (m.insured || "[Your name]")];
      letter.value = L.filter(function (x, i) { return x !== "" || L[i - 1] !== ""; }).join("\n");
    }
    root.addEventListener("click", function (e) {
      var t = e.target;
      if (t.closest("[data-add-event]")) {
        var date = $("#ev-date", root).value; if (!date) { $("#ev-date", root).focus(); return; }
        st.events.push({ id: Date.now().toString(36), type: $("#ev-type", root).value, date: date, amt: $("#ev-amt", root).value, note: $("#ev-note", root).value });
        $("#ev-amt", root).value = ""; $("#ev-note", root).value = ""; save();
      } else if (t.closest("[data-del]")) { var id = t.closest("[data-del]").dataset.del; st.events = st.events.filter(function (x) { return x.id !== id; }); save(); }
      else if (t.closest("[data-clear]")) { if (confirm("Delete every event saved in this browser?")) { st = { meta: {}, events: [] }; $$("[data-meta]", root).forEach(function (el) { el.value = ""; }); save(); } }
      else if (t.closest("[data-demo]")) {
        var b = addDays(today(), -200), mk = function (n, type, amt, note) { return { id: Math.random().toString(36).slice(2), type: type, date: iso(addDays(b, n)), amt: amt || "", note: note || "" }; };
        st.meta = { insured: "Jordan Example", carrier: "Example Mutual", claimno: "HO-123456", loss: iso(addDays(b, -3)), address: "Austin, TX" };
        st.events = [mk(0, "notice", "", "Reported hail damage online"), mk(9, "ack", "", "Adjuster assigned"), mk(21, "inspect"), mk(30, "request", "", "Asked for contractor estimate and photos"), mk(38, "sent", "", "Emailed estimate + 46 photos"), mk(52, "accept", "", "Accepted roof, disputed gutters"), mk(70, "payment", "14200"), mk(120, "supplement", "", "Decking and drip edge"), mk(185, "payment", "9800", "Supplement paid")];
        $$("[data-meta]", root).forEach(function (el) { el.value = st.meta[el.dataset.meta] || ""; }); save();
      } else if (t.closest("[data-copy-letter]")) copyText(letter.value, t.closest("[data-copy-letter]"));
    });
    wireActions(root, { csv: function () { return "Date,Event,Amount,Note\n" + st.events.slice().sort(function (a, b) { return a.date < b.date ? -1 : 1; }).map(function (e) { return [e.date, LABEL[e.type], e.amt, e.note].map(function (c) { return '"' + String(c || "").replace(/"/g, '""') + '"'; }).join(","); }).join("\n"); }, csvName: "claim-timeline.csv" });
    $("#ev-date", root).value = iso(today());
    render();
  }

  /* ============================================================ QUIZ */
  function quiz(root) {
    var steps = $$(".quiz-q", root), prog = $(".quiz-prog i", root), ans = {}, hist = [];
    var n = steps.length - 1;
    function go(i) { steps.forEach(function (s) { s.classList.remove("on"); }); steps[i].classList.add("on"); prog.style.width = (i / n * 100) + "%"; }
    function verdict() {
      var score = 0, excl = false; Object.keys(ans).forEach(function (k) { var s = ans[k].score; if (s <= -99) excl = true; else score += s; });
      var why = [], v;
      if (excl) { v = "weak"; why.push("Chapter 542&rsquo;s prompt-payment rules apply to your own first-party claims, and §542.053 excludes workers&rsquo; comp, title, mortgage guaranty, bonds and marine insurance."); }
      else if (ans.q2 && ans.q2.v === "ontime") { v = "weak"; why.push("If everything was paid within the statutory deadlines, no prompt-payment interest is owed."); }
      else { v = score >= 9 ? "strong" : score >= 5 ? "maybe" : "weak"; }
      if (!excl) {
        if (ans.q2 && /late|partial|denied_paid/.test(ans.q2.v)) why.push("Money arrived after it was first owed &mdash; the core fact behind §542.060 interest.");
        if (ans.q2 && ans.q2.v === "pending") why.push("An unpaid covered claim keeps accruing once the deadline passes.");
        if (ans.q3 && /appraisal|both/.test(ans.q3.v)) why.push("An appraisal award above prior payments is evidence that money owed was unpaid at the deadline (<em>Hinojos</em>, 2021).");
        if (ans.q3 && /supp|both/.test(ans.q3.v)) why.push("Each slow-paid supplement can carry its own interest period.");
        if (ans.q4 && ans.q4.v === "lt60") why.push("Payment within 60 days of the last requested item is usually on time under §542.058 &mdash; unless the insurer had accepted earlier (§542.057: 5 business days).");
        if (ans.q5 && ans.q5.v === "yes") why.push("Delay caused by the policyholder weakens a prompt-payment claim.");
        if (ans.q6 && ans.q6.v === "old") why.push("Older claims may be past the policy&rsquo;s suit limitation; time matters.");
      }
      var head = { strong: "Strong candidate for a review", maybe: "Worth a closer look", weak: "Probably not &mdash; but check the dates" }[v];
      var lead = { strong: "Your answers match the patterns where statutory interest is most often owed.", maybe: "Some of your answers point to a possible prompt-payment issue. The dates will decide it.", weak: "Based on your answers, a prompt-payment claim looks unlikely." }[v];
      $("[data-verdict]", root).innerHTML = '<div class="verdict ' + v + '"><span class="tag ' + (v === "strong" ? "pine" : v === "maybe" ? "gold" : "wine") + '">Result</span><h2 style="margin-top:12px">' + head + "</h2><p>" + lead + "</p><ul>" + why.map(function (x) { return "<li>" + x + "</li>"; }).join("") + '</ul><p style="font-size:.88rem;margin:0">Next: build your dates in the <a href="/tools/claim-timeline-builder/">timeline builder</a> or run the <a href="/statutory-damages-calculator/">interest calculator</a>. This check is general information, not legal advice.</p></div>';
    }
    root.addEventListener("click", function (e) {
      var b = e.target.closest("[data-q]");
      if (b) { var i = steps.indexOf(b.closest(".quiz-q")); ans[b.dataset.q] = { v: b.dataset.v, score: +b.dataset.score }; hist.push(i); if (i + 1 >= n) { verdict(); go(n); } else go(i + 1); return; }
      if (e.target.closest("[data-back]")) { var p = hist.pop(); go(p === undefined ? 0 : p); return; }
      if (e.target.closest("[data-restart]")) { ans = {}; hist = []; go(0); }
    });
    go(0);
  }

  var TOOLS = { ledger: ledger, deadlines: deadlines, appraisal: appraisal, notice542a: notice542a, pafee: pafee, depr: depr, deduct: deduct, prejudgment: prejudgment, ratelookup: ratelookup, timeline: timeline, quiz: quiz };
  $$("[data-tool]").forEach(function (el) { var f = TOOLS[el.dataset.tool]; if (f) try { f(el); } catch (err) { if (w.console) console.error(err); } });
  w.EI = { addBiz: addBiz, runComponent: runComponent, pd: pd, holidays: holidays }; // exposed for testing
})();
