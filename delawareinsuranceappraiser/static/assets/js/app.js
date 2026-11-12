/* Delaware Insurance Appraiser — site script (nav, drawer, reveal, forms, claim worksheets). No dependencies. */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var money = function (n, dec) {
    if (!isFinite(n)) n = 0;
    return (n < 0 ? "−$" : "$") + Math.abs(n).toLocaleString("en-US", { minimumFractionDigits: dec || 0, maximumFractionDigits: dec || 0 });
  };
  var num = function (el) { if (!el) return 0; var v = parseFloat(String(el.value).replace(/[^0-9.\-]/g, "")); return isFinite(v) ? v : 0; };
  var set = function (sel, val, root) { var el = $(sel, root); if (el) el.textContent = val; };
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = $("[data-drop]", o); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    var hover = function () { return window.matchMedia("(hover: hover)").matches; };
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!hover()) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover()) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    body.classList.add("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    if (burger) burger.setAttribute("aria-expanded", "false");
    if (drawer) { drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true"); }
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1260) closeDrawer(); });
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- scroll: header, progress, back-to-top, roadmap fill ---------- */
  var head = $(".head"), bar = $(".progress span"), toTop = $(".to-top"), road = $("[data-road]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("compact", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (road) {
      var r = road.getBoundingClientRect(), mid = window.innerHeight * 0.62;
      var pct = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      var fill = $(".road-fill", road);
      if (fill) fill.style.height = (pct * (r.height - 20)) + "px";
      $$(".road-step", road).forEach(function (s) { s.classList.toggle("on", s.getBoundingClientRect().top < mid); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------- reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  var targets = $$(".rv");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
    var co = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { count(en.target); co.unobserve(en.target); } }); }, { threshold: 0.6 });
    $$("[data-count]").forEach(function (el) { co.observe(el); });
  } else { targets.forEach(reveal); }

  /* ---------- county tabs ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
    var tabs = $$("[role=tab]", wrap);
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute("aria-controls"));
        if (p) p.hidden = !on;
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (ev) {
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") { ev.preventDefault(); select((i + 1) % tabs.length, true); }
        if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") { ev.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
    select(0);
  });

  /* ---------- glossary search ---------- */
  var gf = $("#term-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0;
    $$(".glossary .term").forEach(function (t) {
      var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1;
      t.hidden = !hit; if (hit) shown++;
    });
    var none = $(".filter-none"); if (none) none.hidden = shown > 0;
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      var label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you — your claim details arrived. Someone from Delaware Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@delawareinsuranceappraiser.com\">info@delawareinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- worksheet binding ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (root) {
      var run = function () { fn(root); };
      root.addEventListener("input", run);
      root.addEventListener("change", run);
      root.addEventListener("click", function (ev) { if (ev.target.closest("[data-run]")) setTimeout(run, 0); });
      $$(".range input[type=range]", root).forEach(function (r) {
        var out = r.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = r.value + (r.getAttribute("data-unit") || ""); };
        r.addEventListener("input", upd); upd();
      });
      run();
    });
  }
  window.DIA = { money: money };

  /* 1. Claim gap & fee estimator (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r));
    var ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var award = ins + gap * land;
    var gain = award - ins;
    var cost = feeType === "pct" ? gain * fee / 100 : fee;
    if (useUmp) cost += ump / 2;
    var net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, award, 1), s = stack.children;
      s[0].style.width = (ins / total * 100) + "%";
      s[1].style.width = (Math.max(0, net) / total * 100) + "%";
      s[2].style.width = (Math.max(0, Math.min(cost, gain)) / total * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the amount in dispute.";
      else if (gap <= 0) t = "Your figure isn’t higher than the insurer’s. Appraisal settles how much a covered loss costs — with no gap, there’s nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The amount in dispute is large enough that appraisal may be worth discussing. Have both estimates and your photos ready. (Illustrative figures.)";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0;
    var cap = (num($("[name=cap]", r)) || 80) / 100;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep;
    var first = Math.max(0, acv - ded);
    var full = Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(nonrec ? 0 : full - first), r);
    set("[data-o=total]", money(nonrec ? first : full), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
  });
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (ev) {
      if (ev.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr);
      }
      var x = ev.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof pitch & squares */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software typically adds a steep-roof labor charge. Check that the insurer’s estimate includes it." : pitch >= 7 ? "At 7/12 some estimates begin applying steep charges. Confirm how yours treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.", r);
  });

  /* 4. Hurricane deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payments." : loss <= pd ? "This loss falls entirely within the percentage deductible, so the policy would pay nothing under it." : "The loss exceeds the percentage deductible by " + money(loss - pd) + ".", r);
    var st = $(".stack", r);
    if (st && loss > 0) { var a = Math.min(pd, loss) / loss * 100; st.children[0].style.width = a + "%"; st.children[1].style.width = (100 - a) + "%"; }
  });

  /* 5. Claim deadline calendar */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. This is a self-set target; report as soon as you can." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and keep receipts", n: "Tarps, drying and board-up protect the property and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies count this window from the insurer’s request. Check the date in your letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Confirm the exact repair-completion deadline in your policy to collect the holdback." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date (as entered)", n: "Policies often shorten the time to sue. Ask a Delaware attorney well before this date." }
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
      if (!plan.length) { var dol = $('[name=dol]'); if (dol) dol.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Delaware Insurance Appraiser//Claim Deadline Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:dia-" + ds(p.d) + "-" + i + "@delawareinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n") + "\r\n"], { type: "text/calendar" }));
      a.download = "delaware-claim-deadlines.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness check */
  $$('[data-tool="ready"]').forEach(function (r) {
    var items = $$(".quiz li", r);
    var calc = function () {
      var got = 0, max = 0, answered = 0, todo = [];
      items.forEach(function (li) {
        var w = parseInt(li.getAttribute("data-w"), 10) || 1; max += w;
        var yes = $(".yes", li).getAttribute("aria-pressed") === "true";
        var no = $(".no", li).getAttribute("aria-pressed") === "true";
        if (yes) got += w;
        if (yes || no) answered++;
        if (no) todo.push(li.getAttribute("data-fix"));
      });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? String(pct) : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#233D4D" : pct >= 45 ? "#f0795b" : "#c24a2c"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before invoking appraisal — each one weakens your number if it’s missing." : "Not ready yet. Invoking appraisal now risks locking in a low award. Work through the list below first.", r);
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

  /* 7. Wind vs. flood split */
  tool("split", function (r) {
    var total = num($("[name=total]", r)), wind = num($("[name=wind]", r)) / 100;
    var covA = num($("[name=cova]", r)), hpct = num($("[name=hpct]", r)), hflat = num($("[name=hflat]", r));
    var fded = num($("[name=fded]", r)), flim = num($("[name=flim]", r));
    var wamt = total * wind, famt = total - wamt;
    var hded = hpct > 0 ? covA * hpct / 100 : hflat;
    var hpay = Math.max(0, wamt - hded);
    var fpay = flim > 0 ? Math.min(flim, Math.max(0, famt - fded)) : 0;
    var paid = hpay + fpay, oop = Math.max(0, total - paid);
    set("[data-o=wamt]", money(wamt), r);
    set("[data-o=hded]", money(hded), r);
    set("[data-o=hpay]", money(hpay), r);
    set("[data-o=famt]", money(famt), r);
    set("[data-o=fpay]", money(fpay), r);
    set("[data-o=paid]", money(paid), r);
    set("[data-o=oop]", money(oop), r);
    var st = $(".stack", r);
    if (st) { var t = Math.max(total, 1); st.children[0].style.width = (hpay / t * 100) + "%"; st.children[1].style.width = (fpay / t * 100) + "%"; st.children[2].style.width = (oop / t * 100) + "%"; }
    var msg;
    if (!total) msg = "Enter the total building damage to see the split.";
    else if (flim <= 0 && famt > 0) msg = "With no flood policy, every dollar allocated to flood is yours to cover. Careful documentation of wind-created openings matters most here.";
    else if (wamt > 0 && wamt <= hded) msg = "The wind portion is within the homeowners deductible, so that policy pays nothing at this split.";
    else msg = "Try other splits: the allocation, the hurricane deductible and the flood limit all move your share. Figures are illustrative.";
    set("[data-o=smsg]", msg, r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
