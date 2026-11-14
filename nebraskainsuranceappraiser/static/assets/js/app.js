/* Nebraska Insurance Appraiser — site script: navigation, effects, lead forms and claim tools. No dependencies. */
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
  var root = document.documentElement, body = document.body;
  root.classList.remove("no-js"); root.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function (except) {
    $$(".menu li.open").forEach(function (li) {
      if (li === except) return;
      li.classList.remove("open");
      var b = $("[data-drop]", li); if (b) b.setAttribute("aria-expanded", "false");
    });
  };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    var open = function () { closeDrops(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (li.classList.contains("open")) { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } else open();
    });
    li.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) { clearTimeout(t); open(); } });
    li.addEventListener("mouseleave", function () { if (window.matchMedia("(hover: hover)").matches) { t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); } });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the fixed header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim");
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    if (!drawer) return;
    if (scrim) scrim.hidden = false;
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    burger.setAttribute("aria-expanded", "true");
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function (focusBurger) {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!isOpen() && scrim) scrim.hidden = true; }, 320);
    if (focusBurger) burger.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(true); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1020) closeDrawer(false); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(true); } });

  /* ---------- solid header, back-to-top, horizontal process fill ---------- */
  var head = $(".head"), toTop = $(".to-top"), htime = $("[data-htime]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (htime) {
      var r = htime.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh * 0.8 - r.top) / (r.height + vh * 0.35)));
      var fill = $(".htime-fill", htime), steps = $$(".hstep", htime);
      var vertical = window.innerWidth <= 1020;
      if (fill) {
        if (vertical) { fill.style.height = (p * (r.height - 20)) + "px"; fill.style.width = ""; }
        else { fill.style.width = (p * (r.width - 44)) + "px"; fill.style.height = ""; }
      }
      steps.forEach(function (s, i) { s.classList.toggle("on", p >= (i / Math.max(1, steps.length - 1)) - 0.02 || reduce); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- reveal and counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0"; requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  var targets = $$(".rv, .tally");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        if (en.target.classList.contains("tally")) $$("[data-count]", en.target).forEach(count);
        io.unobserve(en.target);
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- region tabs ---------- */
  $$("[data-regions]").forEach(function (wrap) {
    var tabs = $$("[role=tab]", wrap);
    var select = function (i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        $("#" + t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
        if (e.key === "Home") { e.preventDefault(); select(0, true); }
        if (e.key === "End") { e.preventDefault(); select(tabs.length - 1, true); }
      });
    });
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".gterm").forEach(function (g) { var hit = !q || g.textContent.toLowerCase().indexOf(q) > -1; g.hidden = !hit; if (hit) n++; });
    set("[data-gloss-count]", n + (n === 1 ? " term" : " terms"));
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg"; msg.textContent = "";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      var em = $("[type=email]", form);
      if (em && em.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em.value)) bad.push(em);
      $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      if (bad.length) { bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); }); msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (!d || !d.ok) throw new Error("send failed");
          form.reset(); msg.textContent = "Thank you. Your claim details were received, and a Nebraska Insurance Appraiser team member will reach out, usually within one business day."; msg.classList.add("ok");
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@nebraskainsuranceappraiser.com\">info@nebraskainsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binder ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (r) {
      var run = function () { fn(r); };
      r.addEventListener("input", run);
      r.addEventListener("change", run);
      $$(".range input[type=range]", r).forEach(function (rg) {
        var out = rg.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = rg.value + (rg.getAttribute("data-unit") || ""); };
        rg.addEventListener("input", upd); upd();
      });
      r._run = run;
      run();
    });
  }
  var bars = function (r, parts) {
    var st = $(".stack", r); if (!st) return;
    var tot = parts.reduce(function (a, b) { return a + Math.max(0, b); }, 0) || 1;
    parts.forEach(function (p, i) { if (st.children[i]) st.children[i].style.width = (Math.max(0, p) / tot * 100) + "%"; });
  };

  /* 1. Award gap & fee estimator (full + home mini) */
  window.NIA = window.NIA || {};
  NIA.gap = function (ins, own, land, feeType, fee, rate, useUmp, ump) {
    var gap = Math.max(0, own - ins), gain = gap * land, cost;
    if (feeType === "pct") cost = gain * fee / 100; else if (feeType === "hourly") cost = fee * rate; else cost = fee;
    if (useUmp) cost += ump / 2;
    return { gap: gap, award: ins + gain, gain: gain, cost: cost, net: gain - cost };
  };
  tool("gap", function (r) {
    var g = function (n) { return $("[name=" + n + "]", r); };
    var ins = num(g("insurer")), own = num(g("yours")), land = g("land") ? num(g("land")) / 100 : 0.5;
    var full = !!g("feetype");
    var ft = full ? g("feetype").value : "none", fee = num(g("fee")), rate = num(g("rate")), useUmp = full && g("useump").checked, ump = num(g("umpire"));
    var hr = $("[data-fee-hourly]", r); if (hr) hr.hidden = ft !== "hourly";
    var o = full ? NIA.gap(ins, own, land, ft, fee, rate, useUmp, ump) : NIA.gap(ins, own, land, "flat", 0, 0, false, 0);
    set("[data-o=gap]", money(o.gap), r);
    set("[data-o=pct]", ins > 0 ? Math.round(o.gap / ins * 100) + "%" : "—", r);
    set("[data-o=award]", money(o.award), r);
    set("[data-o=cost]", money(o.cost), r);
    set("[data-o=net]", money(o.net), r);
    [25, 50, 75].forEach(function (p) { if ($("[data-o=s" + p + "]", r)) set("[data-o=s" + p + "]", money(NIA.gap(ins, own, p / 100, ft, fee, rate, useUmp, ump).net), r); });
    bars(r, [ins, Math.max(0, o.net), Math.min(o.cost, o.gain)]);
    var m = $("[data-o=msg]", r);
    if (m) m.textContent = !ins || !own ? "Enter both estimates to see the disputed amount."
      : o.gap <= 0 ? "Your number isn’t higher than the carrier’s, so there is no gap to appraise."
      : full && o.net <= 0 ? "At these inputs, fees could absorb the whole recovery. A line-by-line estimate review is usually the better first step."
      : (o.gap / ins < 0.1 && o.gap < 5000) ? "The gap is real but narrow. A documented supplement request may close it without appraisal."
      : "The gap is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
  });

  /* 2. ACV holdback (install year based) */
  NIA.dep = function (rows, lossYear, cap, ded, acvOnly) {
    var rcv = 0, dep = 0;
    rows.forEach(function (x) { var age = Math.max(0, lossYear - x.year); var d = Math.min(cap, age / (x.life || 1)) * x.rcv; rcv += x.rcv; dep += d; x.acv = x.rcv - d; });
    var acv = rcv - dep, first = Math.max(0, acv - ded), total = acvOnly ? first : Math.max(0, rcv - ded);
    return { rcv: rcv, dep: dep, acv: acv, first: first, held: Math.max(0, total - first), total: total };
  };
  tool("dep", function (r) {
    var rows = $$("tbody tr", r).map(function (tr) { return { tr: tr, rcv: num($("[name=rcv]", tr)), year: num($("[name=year]", tr)), life: num($("[name=life]", tr)) }; });
    var o = NIA.dep(rows, num($("[name=lossyear]", r)), (num($("[name=cap]", r)) || 80) / 100, num($("[name=deduct]", r)), $("[name=nonrec]", r).checked);
    rows.forEach(function (x) { set("[data-o=row]", money(x.acv), x.tr); });
    set("[data-o=rcv]", money(o.rcv), r); set("[data-o=dep]", money(o.dep), r); set("[data-o=acv]", money(o.acv), r);
    set("[data-o=first]", money(o.first), r); set("[data-o=held]", money(o.held), r); set("[data-o=total]", money(o.total), r);
    set("[data-o=deppct]", o.rcv ? Math.round(o.dep / o.rcv * 100) + "%" : "0%", r);
  });
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (e) {
      if (e.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr); $("input", tr).focus(); r._run();
      }
      var x = e.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r._run(); }
    });
  });

  /* 3. Roof square & pitch converter (multi-section) */
  NIA.pitch = function (p) { return Math.sqrt(1 + Math.pow(p / 12, 2)); };
  tool("roof", function (r) {
    var surface = 0, steepest = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var a = num($("[name=parea]", tr)), p = num($("[name=ppitch]", tr));
      var s = a * NIA.pitch(p); surface += s; if (a > 0 && p > steepest) steepest = p;
      set("[data-o=psq]", (s / 100).toFixed(2), tr);
    });
    var waste = num($("[name=waste]", r)) / 100, price = num($("[name=price]", r));
    var sq = surface / 100, order = sq * (1 + waste);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=steepest]", steepest ? steepest + "/12" : "—", r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", steepest >= 8 ? "At " + steepest + "/12, estimating software commonly adds steep-roof labor. Check that the carrier’s estimate includes it for that section." : steepest >= 7 ? "At 7/12 some carriers begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitches: steep-roof charges are not typically expected.", r);
  });

  /* 4. Hail deductible */
  NIA.deduct = function (covA, pct, flat, loss) { var pd = covA * pct / 100; return { pd: pd, pdpay: Math.max(0, loss - pd), flatpay: Math.max(0, loss - flat), diff: Math.max(0, Math.min(loss, pd) - Math.min(loss, flat)), share: loss > 0 ? Math.min(1, pd / loss) : 0 }; };
  tool("deduct", function (r) {
    var loss = num($("[name=loss]", r));
    var o = NIA.deduct(num($("[name=cova]", r)), num($("[name=pct]", r)), num($("[name=flat]", r)), loss);
    set("[data-o=pd]", money(o.pd), r); set("[data-o=pdpay]", money(o.pdpay), r); set("[data-o=flatpay]", money(o.flatpay), r);
    set("[data-o=diff]", money(o.diff), r); set("[data-o=share]", loss > 0 ? Math.round(o.share * 100) + "%" : "—", r);
    set("[data-o=below]", !loss ? "Enter an estimated loss to compare payments." : loss <= o.pd ? "This loss falls entirely within the wind/hail deductible, so no claim payment would be owed under it." : "The loss exceeds the wind/hail deductible by " + money(loss - o.pd) + ".", r);
    bars(r, [Math.min(o.pd, loss), o.pdpay]);
  });

  /* 5. Claim calendar builder */
  var plan = [];
  NIA.addDays = function (base, d) { var x = new Date(base); x.setDate(x.getDate() + d); return x; };
  NIA.addMonths = function (base, m) { var x = new Date(base), day = x.getDate(); x.setDate(1); x.setMonth(x.getMonth() + m); var last = new Date(x.getFullYear(), x.getMonth() + 1, 0).getDate(); x.setDate(Math.min(day, last)); return x; };
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: NIA.addDays(base, num($("[name=notice]", r))), t: "Report the claim (target)", n: "Policies require prompt notice. Report as soon as you can; this is your own target date." },
      { d: NIA.addDays(base, num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarping, board-up and drying protect the claim and are usually reimbursable." },
      { d: NIA.addDays(base, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many forms count from the carrier’s written request. Check your letters." },
      { d: NIA.addDays(base, num($("[name=rcd]", r))), t: "Repairs done to recover depreciation", n: "Replacement cost policies often set a deadline to finish repairs and claim the holdback." },
      { d: NIA.addMonths(base, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Use the period in your own policy. Talk to a Nebraska attorney well before this date." }
    ].sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + "<em>" + badge + "</em></b><strong>" + p.t + "</strong><br><span>" + p.n + "</span></li>";
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var r = btn.closest("[data-tool]");
      if (!plan.length) { var dl = $("[name=dol]", r); if (dl) dl.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Nebraska Insurance Appraiser//Claim Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        ics.push("BEGIN:VEVENT", "UID:nia-" + ds(p.d) + "-" + i + "@nebraskainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(NIA.addDays(p.d, 1)), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n") + "\r\n"], { type: "text/calendar" }));
      a.download = "nebraska-claim-calendar.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal readiness check */
  $$('[data-tool="ready"]').forEach(function (r) {
    var items = $$(".quiz li", r);
    var calc = function () {
      var got = 0, max = 0, answered = 0, todo = [];
      items.forEach(function (li) {
        var w = parseInt(li.getAttribute("data-w"), 10) || 1; max += w;
        var yes = $(".yes", li).getAttribute("aria-pressed") === "true", no = $(".no", li).getAttribute("aria-pressed") === "true";
        if (yes) got += w; if (yes || no) answered++; if (no) todo.push(li.getAttribute("data-fix"));
      });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? String(pct) : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { arc.style.strokeDashoffset = 251.3 - 251.3 * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#002A86" : pct >= 45 ? "#E6B400" : "#B4532A"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects. The next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before demanding appraisal; each one weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list first.", r);
      var ul = $("[data-o=todo]", r);
      ul.innerHTML = "";
      (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); });
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

  /* 7. Slope-by-slope repair gap */
  NIA.slope = function (total, approved, price, prem, extras, ded) {
    approved = Math.min(approved, total);
    var partial = approved * price * (1 + prem / 100), full = total * price + extras;
    return { partial: partial, full: full, gap: Math.max(0, full - partial), share: total > 0 ? approved / total : 0, ppay: Math.max(0, partial - ded), fpay: Math.max(0, full - ded) };
  };
  tool("slope", function (r) {
    var g = function (n) { return num($("[name=" + n + "]", r)); };
    var total = g("total"), o = NIA.slope(total, g("approved"), g("price"), g("prem"), g("extras"), g("deduct"));
    set("[data-o=gap]", money(o.gap), r); set("[data-o=partial]", money(o.partial), r); set("[data-o=full]", money(o.full), r);
    set("[data-o=ppay]", money(o.ppay), r); set("[data-o=fpay]", money(o.fpay), r);
    set("[data-o=share]", total > 0 ? Math.round(o.share * 100) + "%" : "—", r);
    bars(r, [o.share, 1 - o.share]);
    set("[data-o=msg]", !total ? "Enter the total roof squares." : o.share >= 1 ? "The carrier approved the whole roof. Any remaining dispute is about price or line items, not scope." : o.ppay <= 0 ? "At these figures the partial repair does not exceed your deductible, so the scope question decides whether anything is paid." : "The disputed slopes are worth about " + money(o.gap) + ". Slope-by-slope photos, matching evidence and shingle condition decide this kind of dispute.", r);
  });
})();
