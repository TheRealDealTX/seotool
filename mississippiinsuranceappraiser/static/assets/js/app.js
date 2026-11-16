/* Mississippi Insurance Appraiser — site script: nav, drawer, effects, forms, calculators. No dependencies. */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var money = function (n) {
    if (!isFinite(n)) n = 0;
    return (n < 0 ? "−$" : "$") + Math.round(Math.abs(n)).toLocaleString("en-US");
  };
  var num = function (el) { if (!el) return 0; var v = parseFloat(String(el.value).replace(/[^0-9.\-]/g, "")); return isFinite(v) ? v : 0; };
  var set = function (sel, val, root) { var el = $(sel, root); if (el) el.textContent = val; };
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var MS = window.MIA = window.MIA || {};

  /* pages with a photo hero get a transparent header until scrolled */
  if ($(".phero")) body.classList.add("phero-page");

  /* ---------- desktop dropdown panels ---------- */
  var closePanels = function (except) {
    $$(".has-panel.open").forEach(function (li) {
      if (li === except) return;
      li.classList.remove("open");
      var b = $(".nav-btn", li); if (b) b.setAttribute("aria-expanded", "false");
    });
  };
  $$(".has-panel").forEach(function (li) {
    var btn = $(".nav-btn", li), t;
    var open = function () { closePanels(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    var close = function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); li.classList.contains("open") ? close() : open(); });
    li.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) { clearTimeout(t); open(); } });
    li.addEventListener("mouseleave", function () { if (window.matchMedia("(hover: hover)").matches) { t = setTimeout(close, 180); } });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".has-panel")) closePanels(); });

  /* ---------- mobile drawer (outside the sticky header) ---------- */
  var drawer = $("#drawer"), menuBtn = $(".menu-btn"), scrim = $(".scrim");
  var lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    menuBtn.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    menuBtn.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!body.classList.contains("drawer-open")) scrim.hidden = true; }, 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  MS.closeDrawer = closeDrawer;
  if (drawer && menuBtn) {
    menuBtn.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    // Defer: making the drawer inert inside the click handler would cancel the link's navigation.
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { setTimeout(function () { lastFocus = null; closeDrawer(); }, 0); }); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var willOpen = b.getAttribute("aria-expanded") !== "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); $("#" + o.getAttribute("aria-controls")).hidden = true; });
        b.setAttribute("aria-expanded", willOpen ? "true" : "false");
        $("#" + b.getAttribute("aria-controls")).hidden = !willOpen;
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1160) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closePanels(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, progress bar, back-to-top, parallax, steps ---------- */
  var head = $(".site-head"), bar = $(".progress span"), toTop = $(".to-top");
  var px = $$("[data-parallax]");
  var steps = $("[data-steps]"), line = steps ? $(".steps-line span", steps) : null;
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight, h = document.documentElement.scrollHeight - vh;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -k).toFixed(1) + "px,0)";
    });
    if (steps && line) {
      var r = steps.getBoundingClientRect(), mid = vh * 0.65;
      var pct = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      if (window.innerWidth > 1020) { line.style.width = (pct * 100) + "%"; line.style.removeProperty("--fill"); }
      else { line.style.setProperty("--fill", (pct * 100) + "%"); }
      $$(".step", steps).forEach(function (s, i, all) {
        var on = window.innerWidth > 1020 ? pct >= (i / Math.max(1, all.length - 1)) - 0.02 : s.getBoundingClientRect().top < mid;
        s.classList.toggle("on", on);
      });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); }); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        $$("[data-count]", en.target).forEach(count);
        io.unobserve(en.target);
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv, .strip").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- glossary search ---------- */
  var gq = $("#gloss-q");
  if (gq) gq.addEventListener("input", function () {
    var q = gq.value.trim().toLowerCase(), n = 0;
    $$(".gloss .term").forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
    set("[data-gloss-count]", n + (n === 1 ? " term" : " terms"));
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg"; msg.textContent = "";
      $$(".bad", form).forEach(function (f) { f.classList.remove("bad"); });
      var bad = $$("[required]", form).filter(function (f) {
        if (f.type === "checkbox") return !f.checked;
        if (f.type === "email") return !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value.trim());
        return !f.value.trim();
      });
      if (bad.length) { bad.forEach(function (f) { f.classList.add("bad"); }); msg.textContent = "Please complete the highlighted fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (!d || !d.ok) throw new Error("send");
          form.reset(); msg.textContent = "Thank you — your claim details arrived. Someone from Mississippi Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok");
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@mississippiinsuranceappraiser.com\">info@mississippiinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- calculator binding ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (root) {
      var run = function () { fn(root); };
      root.addEventListener("input", run);
      root.addEventListener("change", run);
      root.addEventListener("click", function (e) { if (e.target.closest("[data-run]")) setTimeout(run, 0); });
      $$(".range input[type=range]", root).forEach(function (r) {
        var out = r.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = r.value + (r.getAttribute("data-unit") || ""); };
        r.addEventListener("input", upd); upd();
      });
      run();
    });
  }
  var widths = function (barEl, parts, total) {
    if (!barEl) return;
    var s = barEl.children;
    parts.forEach(function (v, i) { if (s[i]) s[i].style.width = (total > 0 ? Math.max(0, v) / total * 100 : 0) + "%"; });
  };

  /* 1. Appraisal payoff estimator */
  MS.payoff = function (ins, own, land, feeType, fee, rate, ump, useUmp) {
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var feeCost = feeType === "pct" ? gain * fee / 100 : feeType === "hourly" ? fee * rate : fee;
    var cost = feeCost + (useUmp ? ump / 2 : 0);
    var fixed = (feeType === "pct" ? 0 : feeCost) + (useUmp ? ump / 2 : 0);
    var be = null;
    if (gap > 0) { be = feeType === "pct" ? (fee >= 100 ? null : fixed / (gap * (1 - fee / 100))) : fixed / gap; }
    return { gap: gap, award: award, gain: gain, cost: cost, net: gain - cost, breakeven: be };
  };
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = num($("[name=land]", r)) / 100;
    var full = !!$("[name=fee]", r);
    var res = MS.payoff(ins, own, land, full ? $("[name=feetype]", r).value : "flat", full ? num($("[name=fee]", r)) : 0,
      full ? num($("[name=rate]", r)) : 0, full ? num($("[name=umpire]", r)) : 0, full ? $("[name=useump]", r).checked : false);
    set("[data-o=gap]", money(res.gap), r); set("[data-o=award]", money(res.award), r); set("[data-o=gain]", money(res.gain), r);
    set("[data-o=cost]", money(res.cost), r); set("[data-o=net]", money(res.net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(res.gap / ins * 100) + "%" : "—", r);
    set("[data-o=breakeven]", res.breakeven === null ? "—" : res.breakeven > 1 ? "Above 100% (fees exceed the gap)" : Math.ceil(res.breakeven * 100) + "% of the gap", r);
    widths($(".bar", r), [ins, Math.max(0, res.net), Math.min(res.cost, res.gain)], Math.max(own, res.award, 1));
    var m = $("[data-o=msg]", r), t;
    if (!m) return;
    if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
    else if (res.gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal values a covered loss — with no gap, there’s nothing to appraise.";
    else if (full && res.net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the smarter first step.";
    else if (res.gap / ins < 0.1 && res.gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
    else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready when you call.";
    m.textContent = t;
  });

  /* 2. Holdback */
  MS.holdback = function (rows, cap, labor, ded, paid, nonrec) {
    var rcv = 0, dep = 0;
    rows.forEach(function (x) { var d = Math.min(cap, x.life > 0 ? x.age / x.life : 0) * x.rcv * (1 - labor); rcv += x.rcv; dep += d; x.acv = x.rcv - d; });
    var acv = rcv - dep, first = Math.max(0, acv - ded - paid);
    var total = nonrec ? first : Math.max(0, rcv - ded - paid);
    return { rcv: rcv, dep: dep, acv: acv, first: first, held: Math.max(0, total - first), total: total };
  };
  tool("dep", function (r) {
    var rows = $$("tbody tr", r).map(function (tr) { return { tr: tr, rcv: num($("[name=rcv]", tr)), age: num($("[name=age]", tr)), life: num($("[name=life]", tr)) }; });
    var res = MS.holdback(rows, (num($("[name=cap]", r)) || 80) / 100, Math.min(100, num($("[name=labor]", r))) / 100, num($("[name=deduct]", r)), num($("[name=paid]", r)), $("[name=nonrec]", r).checked);
    rows.forEach(function (x) { set("[data-o=row]", money(x.acv), x.tr); });
    set("[data-o=rcv]", money(res.rcv), r); set("[data-o=dep]", money(res.dep), r); set("[data-o=acv]", money(res.acv), r);
    set("[data-o=first]", money(res.first), r); set("[data-o=held]", money(res.held), r); set("[data-o=total]", money(res.total), r);
    set("[data-o=deppct]", res.rcv ? Math.round(res.dep / res.rcv * 100) + "%" : "0%", r);
  });
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (e) {
      if (e.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr); $("input", tr).focus();
      }
      var x = e.target.closest(".del");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof squares */
  MS.roof = function (foot, pitch, waste) {
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2)), surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    return { mult: mult, surface: surface, sq: sq, order: Math.ceil(order * 3) / 3, bundles: Math.ceil(order * 3) };
  };
  tool("roof", function (r) {
    var mode = ($("[name=mode]:checked", r) || {}).value || "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), res = MS.roof(foot, pitch, num($("[name=waste]", r)) / 100), price = num($("[name=price]", r));
    set("[data-o=mult]", res.mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(res.surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", res.sq.toFixed(2), r);
    set("[data-o=order]", res.order.toFixed(2), r);
    set("[data-o=bundles]", String(res.bundles), r);
    set("[data-o=perim]", mode === "dims" ? Math.round(2 * (L + W + 4 * oh)).toLocaleString("en-US") + " lin ft" : "—", r);
    set("[data-o=cost]", price ? money(res.order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, most estimating software adds a steep-roof labor charge. Check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 many estimates begin applying steep charges. Confirm how yours treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected. Do check drip edge, starter and ridge lines.", r);
  });

  /* 4. Named-storm deductible */
  MS.deduct = function (covA, pct, flat, loss) { var pd = covA * pct / 100; return { pd: pd, pdpay: Math.max(0, loss - pd), flatpay: Math.max(0, loss - flat), diff: Math.min(loss, pd) - Math.min(loss, flat) }; };
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var res = MS.deduct(covA, pct, flat, loss);
    set("[data-o=pd]", money(res.pd), r); set("[data-o=pdpay]", money(res.pdpay), r); set("[data-o=flatpay]", money(res.flatpay), r); set("[data-o=diff]", money(res.diff), r);
    widths($(".bar", r), [Math.min(res.pd, loss), res.pdpay], loss);
    var lad = $("[data-o=ladder]", r);
    if (lad) lad.innerHTML = [1, 2, 3, 5, 10].map(function (p) { var x = MS.deduct(covA, p, flat, loss); return "<tr" + (p === pct ? ' class="hl"' : "") + "><td>" + p + "%</td><td>" + money(x.pd) + "</td><td>" + money(x.pdpay) + "</td></tr>"; }).join("");
    set("[data-o=below]", !loss ? "Enter an estimated loss to compare payouts." : loss <= res.pd ? "This loss falls entirely inside the percentage deductible, so that deductible would leave nothing payable." : "The loss exceeds the percentage deductible by " + money(loss - res.pd) + ".", r);
  });

  /* 5. Claim calendar */
  var plan = [];
  MS.addYears = function (iso, yrs) { var d = new Date(iso + "T12:00:00"), m = d.getMonth(); d.setFullYear(d.getFullYear() + Math.floor(yrs)); if (d.getMonth() !== m) d.setDate(0); return d; };
  MS.addDays = function (iso, days) { var d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + days); return d; };
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, dem = $("[name=demand]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Choose your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: MS.addDays(d0, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-set target." },
      { d: MS.addDays(d0, num($("[name=mitig]", r))), t: "Finish temporary repairs and keep receipts", n: "Tarping, dry-out and board-up protect the property and are usually part of the claim." },
      { d: MS.addDays(d0, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies allow 60 days from the carrier’s written request. Count from the date on that letter." },
      { d: MS.addDays(d0, num($("[name=rcd]", r))), t: "Replacement-cost (holdback) window closes", n: "Check your policy for the exact period to finish repairs and claim held-back depreciation." },
      { d: MS.addYears(d0, num($("[name=suit]", r))), t: "Lawsuit deadline to confirm with an attorney", n: "Mississippi’s general contract limitation period is three years; confirm your actual deadline with a Mississippi attorney." }
    ];
    if (dem) {
      plan.push({ d: MS.addDays(dem, 0), t: "Appraisal demanded in writing", n: "Keep a copy of the demand and proof of delivery." });
      plan.push({ d: MS.addDays(dem, num($("[name=appoint]", r))), t: "Name your appraiser by this date", n: "Many clauses give each side about 20 days after the demand. Check your policy’s wording." });
    }
    plan.sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + "<em>" + badge + "</em></b><strong>" + p.t + "</strong><span>" + p.n + "</span></li>";
    }).join("");
  });
  MS.ics = function (items) {
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
    var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
    var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
    var out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Mississippi Insurance Appraiser//Claim Calendar//EN", "CALSCALE:GREGORIAN"];
    items.forEach(function (p, i) {
      var end = new Date(p.d); end.setDate(end.getDate() + 1);
      out.push("BEGIN:VEVENT", "UID:mia-" + ds(p.d) + "-" + i + "@mississippiinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
    });
    out.push("END:VCALENDAR");
    return out.join("\r\n");
  };
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var d = $('[data-tool="dates"] [name=dol]'); if (d) d.focus(); return; }
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([MS.ics(plan)], { type: "text/calendar" }));
      a.download = "mississippi-claim-deadlines.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness checkup */
  $$('[data-tool="ready"]').forEach(function (r) {
    var items = $$(".quiz li", r);
    var calc = function () {
      var got = 0, max = 0, answered = 0, todo = [];
      items.forEach(function (li) {
        var w = parseInt(li.getAttribute("data-w"), 10) || 1; max += w;
        var yes = $(".yes", li).getAttribute("aria-pressed") === "true", no = $(".no", li).getAttribute("aria-pressed") === "true";
        if (yes) got += w;
        if (yes || no) answered++;
        if (no) todo.push(li.getAttribute("data-fix"));
      });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? String(pct) : "–", r);
      var fill = $("[data-o=fill]", r);
      if (fill) { fill.style.width = (answered ? pct : 0) + "%"; fill.style.background = pct >= 75 ? "#0F5E5A" : pct >= 45 ? "#EAAB22" : "#C21F32"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects — the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before demanding appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) { ul.innerHTML = ""; (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); }); }
      set("[data-o=count]", answered + " / " + items.length, r);
    };
    items.forEach(function (li) {
      $$(".yn button", li).forEach(function (b) {
        b.addEventListener("click", function () { $$(".yn button", li).forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); }); calc(); });
      });
    });
    var reset = $("[data-reset]", r);
    if (reset) reset.addEventListener("click", function () { $$(".yn button", r).forEach(function (b) { b.setAttribute("aria-pressed", "false"); }); calc(); });
    calc();
  });

  /* 7. Wind vs. water split */
  MS.split = function (total, windShare, covA, wdedPct, fLimit, fDed, noFlood) {
    var wind = total * windShare, flood = total - wind, wded = covA * wdedPct / 100;
    var windPay = Math.min(covA, Math.max(0, wind - wded));
    var floodPay = noFlood ? 0 : Math.min(fLimit, Math.max(0, flood - fDed));
    return { wind: wind, flood: flood, wded: wded, windPay: windPay, floodPay: floodPay, both: windPay + floodPay, gap: total - windPay - floodPay };
  };
  tool("split", function (r) {
    var total = num($("[name=total]", r)), share = num($("[name=windpct]", r)) / 100, covA = num($("[name=cova]", r)), wp = num($("[name=wded]", r));
    var fl = num($("[name=flimit]", r)), fd = num($("[name=fded]", r)), nf = $("[name=noflood]", r).checked;
    var res = MS.split(total, share, covA, wp, fl, fd, nf);
    var up = MS.split(total, Math.min(1, share + 0.1), covA, wp, fl, fd, nf);
    $$("[name=flimit],[name=fded]", r).forEach(function (i) { i.disabled = nf; });
    set("[data-o=windamt]", money(res.wind), r); set("[data-o=wdedamt]", money(res.wded), r); set("[data-o=windpay]", money(res.windPay), r);
    set("[data-o=floodamt]", money(res.flood), r); set("[data-o=floodpay]", money(res.floodPay), r); set("[data-o=gap]", money(res.gap), r);
    set("[data-o=both]", money(res.both), r);
    set("[data-o=swing]", (up.both - res.both >= 0 ? "+" : "") + money(up.both - res.both), r);
    widths($(".bar", r), [res.windPay, res.floodPay, res.gap], total);
    set("[data-o=msg]", !total ? "Enter the total damage to see the split." : nf ? "With no flood policy, every dollar attributed to flood is unpaid — documenting wind damage carefully matters a great deal." : res.gap > total * 0.25 ? "A large share is left unpaid at this split. Deductibles and limits drive much of it; evidence about causation drives the rest." : "At this split, most of the damage is paid by one policy or the other. Small shifts in the split still move real money.", r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
