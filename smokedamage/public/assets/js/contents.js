/* Contents Replacement Cost & Depreciation Calculator.
   Unlimited line items, saved to this browser only (localStorage). */
(function () {
  "use strict";
  var tbody = document.getElementById("rows");
  var tpl = document.getElementById("row-tpl");
  if (!tbody || !tpl) return;
  var track = window.sdTrack || function () {};
  var KEY = "sd_contents_v1";
  var FIELDS = ["item", "category", "brand", "model", "qty", "age", "condition", "cost", "dep", "tax", "notes"];
  var money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" });
  var completed = false;

  function num(v) { var n = parseFloat(v); return isFinite(n) && n > 0 ? n : 0; }
  function calc(d) {
    var qty = num(d.qty), cost = num(d.cost), tax = Math.min(num(d.tax), 100), dep = Math.min(num(d.dep), 100);
    var rcv = qty * cost * (1 + tax / 100);
    var depamt = rcv * dep / 100;
    return { rcv: rcv, depamt: depamt, acv: rcv - depamt };
  }
  function rowData(tr) {
    var d = {};
    FIELDS.forEach(function (k) { var el = tr.querySelector('[data-k="' + k + '"]'); d[k] = el ? el.value : ""; });
    return d;
  }
  function addRow(d, after) {
    var tr = tpl.content.firstElementChild.cloneNode(true);
    if (d) FIELDS.forEach(function (k) { var el = tr.querySelector('[data-k="' + k + '"]'); if (el && d[k] !== undefined) el.value = d[k]; });
    if (after && after.nextSibling) tbody.insertBefore(tr, after.nextSibling); else if (after) tbody.appendChild(tr); else tbody.appendChild(tr);
    update(tr);
    return tr;
  }
  function update(tr) {
    var c = calc(rowData(tr));
    tr.querySelector('[data-out="rcv"]').textContent = money.format(c.rcv);
    tr.querySelector('[data-out="depamt"]').textContent = money.format(c.depamt);
    tr.querySelector('[data-out="acv"]').textContent = money.format(c.acv);
  }
  function totals() {
    var t = { rcv: 0, dep: 0, acv: 0, n: 0, q: 0 };
    tbody.querySelectorAll("tr").forEach(function (tr) {
      var d = rowData(tr), c = calc(d);
      t.rcv += c.rcv; t.dep += c.depamt; t.acv += c.acv; t.n += 1; t.q += num(d.qty);
    });
    document.getElementById("t-rcv").textContent = money.format(t.rcv);
    document.getElementById("t-dep").textContent = money.format(t.dep);
    document.getElementById("t-acv").textContent = money.format(t.acv);
    document.getElementById("t-count").textContent = t.n + " / " + t.q;
    if (!completed && t.rcv > 0 && t.n >= 3) { completed = true; track("calculator_complete", { tool: "contents" }); }
  }
  function save() {
    var rows = [];
    tbody.querySelectorAll("tr").forEach(function (tr) { rows.push(rowData(tr)); });
    try { localStorage.setItem(KEY, JSON.stringify(rows)); } catch (e) { /* storage unavailable: list still works this session */ }
  }
  function load() {
    var rows = null;
    try { rows = JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { rows = null; }
    if (rows && rows.length) rows.forEach(function (d) { addRow(d); });
    else { addRow(); addRow(); addRow(); }
    totals();
  }

  tbody.addEventListener("input", function (e) { var tr = e.target.closest("tr"); if (tr) { update(tr); totals(); save(); } });
  tbody.addEventListener("change", function (e) { var tr = e.target.closest("tr"); if (tr) { update(tr); totals(); save(); } });
  tbody.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-act]"); if (!btn) return;
    var tr = btn.closest("tr");
    if (btn.getAttribute("data-act") === "dup") { var n = addRow(rowData(tr), tr); n.querySelector('[data-k="item"]').focus(); }
    else { var next = tr.nextElementSibling || tr.previousElementSibling; tr.remove(); if (!tbody.children.length) addRow(); (next || tbody.querySelector("tr")).querySelector("input").focus(); }
    totals(); save();
  });
  document.getElementById("add-row").addEventListener("click", function () { var tr = addRow(); tr.querySelector('[data-k="item"]').focus(); totals(); save(); });
  document.getElementById("clear-all").addEventListener("click", function () {
    if (!confirm("Remove every item from this list? This can't be undone.")) return;
    tbody.innerHTML = ""; addRow(); totals(); save();
  });
  document.getElementById("filter").addEventListener("input", function (e) {
    var q = e.target.value.trim().toLowerCase();
    tbody.querySelectorAll("tr").forEach(function (tr) {
      var d = rowData(tr); var hay = (d.item + " " + d.category + " " + d.brand + " " + d.model + " " + d.notes).toLowerCase();
      tr.hidden = q && hay.indexOf(q) === -1;
    });
  });
  document.getElementById("sort").addEventListener("change", function (e) {
    var k = e.target.value; if (!k) return;
    var rows = [].slice.call(tbody.querySelectorAll("tr"));
    rows.sort(function (a, b) {
      var da = rowData(a), db = rowData(b);
      if (k === "rcv") return calc(db).rcv - calc(da).rcv;
      return (da[k] || "").localeCompare(db[k] || "") || (da.item || "").localeCompare(db.item || "");
    });
    rows.forEach(function (r) { tbody.appendChild(r); });
    save();
  });
  function csvCell(v) { v = String(v == null ? "" : v); if (/^[=+\-@]/.test(v)) v = "'" + v; return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  document.getElementById("export-csv").addEventListener("click", function () {
    var head = ["Item", "Category", "Brand", "Model", "Quantity", "Approx. age (yrs)", "Pre-loss condition", "Replacement cost per item", "Est. depreciation %", "Sales tax %", "RCV", "Est. depreciation", "Est. ACV", "Notes"];
    var lines = [head.join(",")];
    var t = { rcv: 0, dep: 0, acv: 0 };
    tbody.querySelectorAll("tr").forEach(function (tr) {
      var d = rowData(tr), c = calc(d);
      if (!d.item && !num(d.cost)) return;
      t.rcv += c.rcv; t.dep += c.depamt; t.acv += c.acv;
      lines.push([d.item, d.category, d.brand, d.model, d.qty, d.age, d.condition, d.cost, d.dep, d.tax, c.rcv.toFixed(2), c.depamt.toFixed(2), c.acv.toFixed(2), d.notes].map(csvCell).join(","));
    });
    lines.push(["TOTALS", "", "", "", "", "", "", "", "", "", t.rcv.toFixed(2), t.dep.toFixed(2), t.acv.toFixed(2), ""].map(csvCell).join(","));
    lines.push("");
    lines.push(csvCell("This calculator is an organizational and estimating tool. Your insurance policy and carrier's applicable claim evaluation determine how replacement cost, depreciation, and actual cash value are handled."));
    var blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "contents-inventory-" + new Date().toISOString().slice(0, 10) + ".csv";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
    track("contents_export", { format: "csv" });
  });
  document.getElementById("print-list").addEventListener("click", function () {
    var pd = document.getElementById("print-date");
    if (pd) pd.textContent = "Prepared " + new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" }) + " with the SmokeDamage.com Contents RCV / ACV Calculator.";
    track("contents_export", { format: "print" });
    window.print();
  });
  document.querySelectorAll('a[data-cta="contents-calc"]').forEach(function (a) { a.addEventListener("click", function () { track("calculator_to_form", { tool: "contents" }); }); });
  load();
})();
