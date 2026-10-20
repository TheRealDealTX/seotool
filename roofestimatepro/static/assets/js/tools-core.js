/* Roof Estimate Pro — shared calculator engine.
 *
 * Each tool page has <form id="tool-form" data-tool="slug"> and an empty
 * <div id="results">, then loads its own script which calls
 *
 *   REP.tool({ id: "slug", name: "Tool name", compute(v) { return result; } })
 *
 * compute() receives the form values (numbers already parsed, checkboxes as
 * booleans, dynamic rows as arrays under v.rows[name]) and returns:
 *
 *   { headline: { label, value, format, text, sub },
 *     kpis:     [{ label, value, format, unit, text }],
 *     breakdown:{ title, items: [{ label, value }], format },
 *     table:    { title, head: [], rows: [[]], foot: [], scroll },
 *     figure:   "<svg…>",
 *     warnings: [], notes: [],
 *     summary:  ["plain-text lines for print / estimator hand-off"] }
 *
 * Everything else (persistence, share links, printing, the estimator hand-off,
 * the mobile total bar) lives here so the tools stay small.
 */
(function () {
  "use strict";

  var COLORS = ["#1fa59e", "#FCBE8E", "#0c6f8a", "#f29d5c", "#9fd9d5", "#c58b5c", "#6b8f8b", "#e5d5c3", "#3b5f5c"];
  var D = window.REP_DATA || {};

  function toNum(s) {
    if (typeof s === "number") return s;
    var n = parseFloat(String(s == null ? "" : s).replace(/[$,%\s]/g, ""));
    return isFinite(n) ? n : 0;
  }
  function money(n, dec) {
    if (!isFinite(n)) return "—";
    dec = dec == null ? (Math.abs(n) < 100 && n % 1 !== 0 ? 2 : 0) : dec;
    var s = Math.abs(n).toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
    return (n < 0 ? "−$" : "$") + s;
  }
  function num(n, dec) {
    if (!isFinite(n)) return "—";
    dec = dec == null ? (n % 1 === 0 ? 0 : 1) : dec;
    return n.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }
  function pct(n, dec) { return isFinite(n) ? num(n, dec == null ? 1 : dec) + "%" : "—"; }
  function fmt(v, f, unit) {
    if (f === "money") return money(v, 0);
    if (f === "money2") return money(v, 2);
    if (f === "pct") return pct(v);
    if (f === "int") return num(Math.round(v), 0);
    if (f === "text") return String(v);
    var s = num(v, typeof f === "number" ? f : undefined);
    return unit ? s + " " + unit : s;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  // Geometry helpers shared by several tools.
  function pitchFactor(rise) { return Math.sqrt(1 + Math.pow(rise / 12, 2)); }
  function hipFactor(rise) { return Math.sqrt(rise * rise + 288) / 12; }
  function region(key) {
    var all = (D.regions || []);
    for (var i = 0; i < all.length; i++) if (all[i].key === key) return all[i];
    return { key: key, name: key, factor: 1 };
  }

  function storage() { try { var t = "__rep"; localStorage.setItem(t, t); localStorage.removeItem(t); return localStorage; } catch (e) { return null; } }

  function b64e(obj) { try { return btoa(unescape(encodeURIComponent(JSON.stringify(obj)))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); } catch (e) { return ""; } }
  function b64d(s) { try { s = s.replace(/-/g, "+").replace(/_/g, "/"); while (s.length % 4) s += "="; return JSON.parse(decodeURIComponent(escape(atob(s)))); } catch (e) { return null; } }

  function toast(msg) {
    var t = document.querySelector(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("show"); }, 2200);
  }

  function tween(el, to, f) {
    var from = el._v == null ? 0 : el._v;
    el._v = to;
    if (!isFinite(to) || window.matchMedia("(prefers-reduced-motion: reduce)").matches || Math.abs(to - from) < 1e-9) { el.textContent = fmt(to, f); return; }
    var t0 = performance.now(), dur = 450;
    cancelAnimationFrame(el._raf);
    (function step(t) {
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(from + (to - from) * e, f);
      if (k < 1) el._raf = requestAnimationFrame(step); else el.textContent = fmt(to, f);
    })(t0);
  }

  function tool(cfg) {
    var form = document.getElementById("tool-form");
    var out = document.getElementById("results");
    if (!form || !out) return;
    var key = "rep:" + cfg.id;
    var store = storage();
    var defaults = snapshot();
    var last = null;

    // ----- dynamic rows -----
    function rowContainers() { return form.querySelectorAll("[data-rows]"); }
    function addRow(container, values) {
      var tpl = document.getElementById(container.getAttribute("data-template"));
      var node = tpl.content.firstElementChild.cloneNode(true);
      var n = container.children.length + 1;
      node.querySelectorAll("[data-k]").forEach(function (inp) {
        var k = inp.getAttribute("data-k");
        if (values && values[k] != null) {
          if (inp.type === "checkbox") inp.checked = !!values[k]; else inp.value = values[k];
        }
        if (inp.hasAttribute("data-autoname") && !(values && values[k])) inp.value = inp.getAttribute("data-autoname") + " " + n;
      });
      container.appendChild(node);
      return node;
    }
    form.addEventListener("click", function (e) {
      var add = e.target.closest("[data-add-row]");
      if (add) { e.preventDefault(); var c = form.querySelector('[data-rows="' + add.getAttribute("data-add-row") + '"]'); var r = addRow(c); var f = r.querySelector("input,select"); if (f) f.focus(); run(); return; }
      var del = e.target.closest(".row-del");
      if (del) { e.preventDefault(); var item = del.closest(".row-item"); var cont = item.parentNode; if (cont.children.length > (+cont.getAttribute("data-min") || 0)) { item.remove(); run(); } else toast("At least one row is needed"); }
    });

    function snapshot() {
      var o = { f: {}, rows: {} };
      form.querySelectorAll("[name]").forEach(function (el) {
        if (el.type === "radio") { if (el.checked) o.f[el.name] = el.value; }
        else if (el.type === "checkbox") o.f[el.name] = el.checked;
        else o.f[el.name] = el.value;
      });
      form.querySelectorAll("[data-rows]").forEach(function (c) {
        o.rows[c.getAttribute("data-rows")] = Array.prototype.map.call(c.children, function (r) {
          var x = {};
          r.querySelectorAll("[data-k]").forEach(function (el) { x[el.getAttribute("data-k")] = el.type === "checkbox" ? el.checked : el.value; });
          return x;
        });
      });
      return o;
    }
    function restore(o) {
      if (!o) return;
      Object.keys(o.f || {}).forEach(function (n) {
        var els = form.querySelectorAll('[name="' + n + '"]');
        els.forEach(function (el) {
          if (el.type === "radio") el.checked = el.value === o.f[n];
          else if (el.type === "checkbox") el.checked = !!o.f[n];
          else el.value = o.f[n];
        });
      });
      Object.keys(o.rows || {}).forEach(function (name) {
        var c = form.querySelector('[data-rows="' + name + '"]');
        if (!c || !o.rows[name].length) return;
        c.innerHTML = "";
        o.rows[name].forEach(function (v) { addRow(c, v); });
      });
    }
    function values() {
      var s = snapshot(), v = { rows: {} };
      Object.keys(s.f).forEach(function (n) {
        var el = form.querySelector('[name="' + n + '"]');
        var raw = s.f[n];
        v[n] = (el && (el.type === "number" || el.type === "range" || el.hasAttribute("data-num") || el.getAttribute("inputmode") === "decimal")) ? toNum(raw) : raw;
      });
      form.querySelectorAll("[data-rows]").forEach(function (c) {
        v.rows[c.getAttribute("data-rows")] = Array.prototype.map.call(c.children, function (r) {
          var x = {};
          r.querySelectorAll("[data-k]").forEach(function (el) {
            var k = el.getAttribute("data-k");
            x[k] = el.type === "checkbox" ? el.checked : (el.type === "number" || el.hasAttribute("data-num") || el.getAttribute("inputmode") === "decimal") ? toNum(el.value) : el.value;
          });
          return x;
        });
      });
      return v;
    }

    // ----- render -----
    function render(r) {
      var h = [];
      if (r.headline) {
        var hl = r.headline;
        h.push('<div class="headline"><small>' + esc(hl.label) + '</small><div class="big" data-tw="' + (hl.text ? "" : hl.format || "money") + '">' +
          (hl.text ? esc(hl.text) : fmt(hl.value, hl.format || "money")) + "</div>" + (hl.sub ? '<div class="sub">' + esc(hl.sub) + "</div>" : "") + "</div>");
      }
      if (r.figure) h.push('<div class="tool-figure" aria-hidden="true">' + r.figure + "</div>");
      if (r.kpis && r.kpis.length) {
        h.push('<div class="kpis">');
        r.kpis.forEach(function (k) { h.push('<div class="kpi"><small>' + esc(k.label) + "</small><b>" + (k.text != null ? esc(k.text) : fmt(k.value, k.format, k.unit)) + "</b></div>"); });
        h.push("</div>");
      }
      if (r.warnings && r.warnings.length) r.warnings.forEach(function (w) { h.push('<div class="res-warn">' + esc(w) + "</div>"); });
      if (r.breakdown && r.breakdown.items) {
        var items = r.breakdown.items.filter(function (i) { return i.value > 0; });
        var tot = items.reduce(function (a, i) { return a + i.value; }, 0) || 1;
        if (r.breakdown.title) h.push('<h2 style="font-size:.95rem;margin:4px 0 6px">' + esc(r.breakdown.title) + "</h2>");
        h.push('<div class="stackbar" role="img" aria-label="Breakdown chart">');
        items.forEach(function (i, ix) { h.push('<i style="width:' + (i.value / tot * 100).toFixed(2) + "%;background:" + COLORS[ix % COLORS.length] + '" title="' + esc(i.label) + '"></i>'); });
        h.push('</div><ul class="legend">');
        items.forEach(function (i, ix) { h.push('<li><i style="background:' + COLORS[ix % COLORS.length] + '"></i><span>' + esc(i.label) + "</span><b>" + fmt(i.value, r.breakdown.format || "money") + "</b><em>" + Math.round(i.value / tot * 100) + "%</em></li>"); });
        h.push("</ul>");
      }
      if (r.table && r.table.rows && r.table.rows.length) {
        var t = r.table;
        if (t.title) h.push('<h2 style="font-size:.95rem;margin:4px 0 6px">' + esc(t.title) + "</h2>");
        h.push((t.scroll ? '<div class="res-scroll">' : "") + '<table class="res-table"><thead><tr>' + t.head.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("") + "</tr></thead><tbody>");
        t.rows.forEach(function (row) { h.push("<tr>" + row.map(function (c) { return "<td>" + esc(c) + "</td>"; }).join("") + "</tr>"); });
        h.push("</tbody>" + (t.foot ? "<tfoot><tr>" + t.foot.map(function (c) { return "<td>" + esc(c) + "</td>"; }).join("") + "</tr></tfoot>" : "") + "</table>" + (t.scroll ? "</div>" : ""));
      }
      if (r.notes && r.notes.length) h.push('<ul class="res-notes">' + r.notes.map(function (n) { return "<li>" + esc(n) + "</li>"; }).join("") + "</ul>");
      h.push('<div class="res-actions">' +
        '<a class="btn btn--peach wide" href="/get-estimate/?tool=' + encodeURIComponent(cfg.id) + '" data-handoff>' + ICON_USER + "Have a pro estimator review this</a>" +
        '<button type="button" class="btn btn--ghost-light" data-act="print">' + ICON_PRINT + "Print / PDF</button>" +
        '<button type="button" class="btn btn--ghost-light" data-act="share">' + ICON_LINK + "Copy link</button>" +
        '<button type="button" class="btn btn--ghost-light wide" data-act="reset">' + ICON_RESET + "Reset to defaults</button></div>");
      h.push('<p class="res-disclaimer">Planning estimate based on the inputs and unit prices shown. Actual pricing depends on a site inspection, material selection and the contractor. Not an insurance determination or a binding quote.</p>');

      var prev = out.querySelector(".headline .big");
      var prevVal = prev ? prev._v : null;
      out.innerHTML = '<h2>Your results <span class="live-dot">Live</span></h2>' + h.join("");
      var big = out.querySelector(".headline .big");
      if (big && r.headline && !r.headline.text) { big._v = prevVal; tween(big, r.headline.value, r.headline.format || "money"); }
      var mt = document.querySelector(".mobile-total");
      if (mt && r.headline) mt.querySelector("b").textContent = r.headline.text || fmt(r.headline.value, r.headline.format || "money");
    }

    // Conditional fields: data-show="name=val1|val2" (prefix with ! to invert)
    function applyShow(v) {
      form.querySelectorAll("[data-show]").forEach(function (el) {
        var rule = el.getAttribute("data-show"), neg = rule.charAt(0) === "!";
        if (neg) rule = rule.slice(1);
        var p = rule.split("="), cur = v[p[0]];
        var hit = p[1].split("|").some(function (x) { return String(cur) === x || (x === "true" && cur === true) || (x === "false" && cur === false); });
        el.hidden = neg ? hit : !hit;
      });
    }

    function run() {
      var v = values(), r;
      applyShow(v);
      try { r = cfg.compute(v) || {}; } catch (e) { r = { warnings: ["Check the inputs — " + e.message] }; if (window.console) console.error(e); }
      last = r;
      render(r);
      if (store) try { store.setItem(key, JSON.stringify(snapshot())); } catch (e) {}
      if (cfg.after) cfg.after(v, r);
    }
    var deb;
    form.addEventListener("input", function (e) {
      if (e.target.type === "range") { var o = form.querySelector('output[for="' + e.target.id + '"]'); if (o) o.textContent = e.target.value + (e.target.getAttribute("data-suffix") || ""); }
      clearTimeout(deb); deb = setTimeout(run, 120);
    });
    form.addEventListener("change", run);
    form.addEventListener("submit", function (e) { e.preventDefault(); run(); });

    out.addEventListener("click", function (e) {
      var b = e.target.closest("[data-act]"), ho = e.target.closest("[data-handoff]");
      if (ho) {
        try {
          sessionStorage.setItem("rep_handoff", JSON.stringify({ tool: cfg.name, url: shareUrl(), lines: (last && last.summary) || [] }));
        } catch (err) {}
        return;
      }
      if (!b) return;
      var act = b.getAttribute("data-act");
      if (act === "print") { stampPrint(); window.print(); }
      if (act === "share") {
        var u = shareUrl();
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(u).then(function () { toast("Link copied — it reopens this estimate"); }, function () { prompt("Copy this link:", u); });
        else prompt("Copy this link:", u);
      }
      if (act === "reset") {
        if (store) try { store.removeItem(key); } catch (err) {}
        rowContainers().forEach(function (c) { c.innerHTML = ""; });
        restore(defaults);
        rowContainers().forEach(function (c) { if (!c.children.length) addRow(c); });
        form.querySelectorAll("input[type=range]").forEach(function (r) { var o = form.querySelector('output[for="' + r.id + '"]'); if (o) o.textContent = r.value + (r.getAttribute("data-suffix") || ""); });
        if (history.replaceState) history.replaceState(null, "", location.pathname);
        run(); toast("Reset to defaults");
      }
    });

    function shareUrl() { return location.origin + location.pathname + "?s=" + b64e(snapshot()); }
    function stampPrint() {
      var ph = document.querySelector(".print-head time");
      if (ph) ph.textContent = new Date().toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
    }

    // ----- boot -----
    var qs = new URLSearchParams(location.search).get("s");
    var saved = qs ? b64d(qs) : null;
    if (!saved && store) try { saved = JSON.parse(store.getItem(key) || "null"); } catch (e) {}
    if (saved) restore(saved);
    rowContainers().forEach(function (c) {
      if (!c.children.length) { var n = +c.getAttribute("data-start") || 1; for (var i = 0; i < n; i++) addRow(c, (cfg.rowDefaults && cfg.rowDefaults[c.getAttribute("data-rows")] || [])[i]); }
    });
    form.querySelectorAll("input[type=range]").forEach(function (r) { var o = form.querySelector('output[for="' + r.id + '"]'); if (o) o.textContent = r.value + (r.getAttribute("data-suffix") || ""); });
    if (cfg.init) cfg.init(form, run);
    run();

    // Mobile sticky total
    var mt = document.querySelector(".mobile-total");
    if (mt && "IntersectionObserver" in window) {
      var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { mt.classList.toggle("show", !en.isIntersecting && en.boundingClientRect.top > 0); }); });
      io.observe(out);
      mt.addEventListener("click", function () { out.scrollIntoView({ behavior: "smooth", block: "start" }); });
    }
    return { run: run, values: values };
  }

  var ICON_USER = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>';
  var ICON_PRINT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M6 14h12v7H6z"/></svg>';
  var ICON_LINK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>';
  var ICON_RESET = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7"/><path d="M3 4v5h5"/></svg>';

  window.REP = {
    tool: tool, money: money, num: num, pct: pct, fmt: fmt, toNum: toNum, esc: esc,
    pitchFactor: pitchFactor, hipFactor: hipFactor, region: region, toast: toast,
    data: D, colors: COLORS
  };
})();
