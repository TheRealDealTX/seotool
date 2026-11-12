/* Montana Insurance Appraiser — site script: nav, drawer, effects, forms, claim tools. No dependencies. */
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
  var hover = window.matchMedia("(hover: hover)");

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!hover.matches) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover.matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (rendered outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), shade = $(".shade"), hideT;
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    clearTimeout(hideT);
    if (shade) shade.hidden = false;
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function (refocus) {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    hideT = setTimeout(function () { if (shade && !isOpen()) shade.hidden = true; }, 320);
    if (refocus) burger.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(true); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) closeDrawer(false); });
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeDrops(); closeDrawer(true); } });

  /* ---------- scroll progress, solid header, back-to-top ---------- */
  var head = $(".head"), bar = $(".progress span"), toTop = $(".to-top"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("solid", y > 24);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0).toFixed(4) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function (ev) { ev.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); var s = $(".skip"); if (s) s.focus({ preventScroll: true }); });

  /* ---------- staggered reveal ---------- */
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 8) * 0.07 + "s"); }); });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter"), gc = $("[data-gcount]");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".glossary .term").forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
    if (gc) gc.textContent = q ? n + (n === 1 ? " term matches" : " terms match") : "";
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      var em = $("[type=email]", form);
      if (!bad.length && em && em.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em.value)) bad = [em];
      if (bad.length) { msg.textContent = "Please complete the required fields (with a valid email) and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thanks. Your details arrived, and Montana Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@montanainsuranceappraiser.com\">info@montanainsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binder ---------- */
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
  /* add/remove rows in item tables (holdback + snow layers) */
  $$('[data-tool="dep"], [data-tool="snow"]').forEach(function (r) {
    var tb = $("tbody", r);
    if (!tb) return;
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

  /* 1. Claim gap & fee calculator */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = num($("[name=land]", r)) / 100;
    var feeType = $("[name=feetype]", r).value, fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r));
    var half = $("[name=useump]", r).checked ? ump / 2 : 0;
    var gap = Math.max(0, own - ins);
    var gain = gap * land;
    var cost = (feeType === "pct" ? gain * fee / 100 : fee) + half;
    var net = gain - cost;
    var even = null;
    if (gap > 0) {
      if (feeType === "pct") even = fee >= 100 ? Infinity : half / (gap * (1 - fee / 100));
      else even = (fee + half) / gap;
    }
    set("[data-o=gap]", money(gap), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=award]", money(ins + gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=even]", even === null ? "—" : even > 1 ? "Not reached" : Math.ceil(even * 100) + "% of the gap", r);
    var s = $(".stack", r).children, total = Math.max(own, ins + gain, 1);
    s[0].style.width = (ins / total * 100) + "%";
    s[1].style.width = (Math.max(0, net) / total * 100) + "%";
    s[2].style.width = (Math.min(cost, gain) / total * 100) + "%";
    var t;
    if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
    else if (gap <= 0) t = "Your number isn’t higher than the carrier’s, so there’s no amount in dispute to appraise.";
    else if (even > 1) t = "At these fees, even a full award wouldn’t cover the cost of appraisal. Start with a line-by-line estimate review or a documented supplement.";
    else if (net <= 0) t = "At this award level, costs absorb the increase. The award would need to land past the break-even point to help you.";
    else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
    else t = "The disputed amount looks large enough to discuss appraisal. Have both estimates and dated photos ready. All figures are illustrative.";
    set("[data-o=msg]", t, r);
  });

  /* 2. Depreciation & holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0, cap = num($("[name=cap]", r)) / 100 || 0.8;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      set("[data-o=row]", money(c - d), tr);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded);
    var total = nonrec ? first : Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(total - first), r);
    set("[data-o=total]", money(total), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
  });

  /* 3. Roof pitch & squares */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r).value;
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = Math.ceil(sq * (1 + waste) * 3) / 3, price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", order.toFixed(2), r);
    set("[data-o=bundles]", String(Math.round(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimates usually add a steep-roof labor charge. Check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 some estimates begin adding steep charges. Confirm how yours treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected. Figures are illustrative.", r);
  });

  /* 4. Wind/hail % deductible, one or two storms */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var two = $("[name=second]", r).checked, loss2 = two ? num($("[name=loss2]", r)) : 0;
    $$("[data-second]", r).forEach(function (el) { el.hidden = !two; });
    var pd = covA * pct / 100;
    var pay1 = Math.max(0, loss - pd), pay2 = Math.max(0, loss2 - pd);
    var absorb = Math.min(loss, pd) + (two ? Math.min(loss2, pd) : 0);
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(pay1), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.min(loss, pd) - Math.min(loss, flat)), r);
    set("[data-o=pay2]", money(pay2), r);
    set("[data-o=season]", money(absorb), r);
    var all = loss + loss2, s = $(".stack", r).children;
    if (all > 0) { var a = absorb / all * 100; s[0].style.width = a + "%"; s[1].style.width = (100 - a) + "%"; }
    set("[data-o=below]", !loss ? "Enter an estimated loss to compare payments." : loss <= pd ? "This storm sits entirely inside the percentage deductible, so no payment would be owed for it. Figures are illustrative." : "Storm 1 exceeds the deductible by " + money(loss - pd) + "." + (two ? " Across both storms you’d absorb " + money(absorb) + "." : "") + " Figures are illustrative.", r);
  });

  /* 5. Claim deadline calendar + .ics */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><strong>Pick your date of loss</strong><br><span>Your dated milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you safely can; this target is your own." },
      { d: add(num($("[name=mitig]", r))), t: "Temporary repairs done, receipts saved", n: "Tarping, drying and board-up protect the property and are usually part of the claim." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often counted from the carrier’s written request. Check your letter." },
      { d: add(num($("[name=season]", r))), t: "Aim to finish exterior repairs before winter", n: "Roofing and siding work slows sharply once snow arrives in much of Montana." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Finish repairs and request the holdback before the deadline in your loss settlement section." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date (placeholder)", n: "Confirm the real period in your policy and with a Montana attorney well before this date." }
    ].sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + " <em>" + badge + "</em></b><strong>" + p.t + "</strong><br><span>" + p.n + "</span></li>";
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var d = $("[name=dol]"); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Montana Insurance Appraiser//Claim Deadline Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:mtia-" + ds(p.d) + "-" + i + "@montanainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "montana-claim-deadlines.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal readiness quiz */
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
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#13306b" : pct >= 45 ? "#f28c28" : "#b4441c"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next question is whether the dollar gap justifies the cost." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each one weakens your number if it’s missing." : "Not ready yet. Demanding appraisal now risks a weak award. Work through the list below first.", r);
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

  /* 7. Roof snow load estimator (full tool uses layer rows; the homepage mini uses one layer) */
  tool("snow", function (r) {
    var rows = $$("tbody tr", r), psf = 0, depth = 0;
    if (!rows.length) rows = [r];
    rows.forEach(function (row) {
      var d = num($("[name=depth]", row)), dens = num($("[name=dens]", row));
      var l = d / 12 * dens;
      psf += l; depth += d;
      if (row !== r) set("[data-o=row]", l.toFixed(1) + " psf", row);
    });
    var area = num($("[name=area]", r)), design = num($("[name=design]", r));
    var share = design > 0 ? psf / design : 0;
    set("[data-o=psf]", psf.toFixed(1) + " psf", r);
    set("[data-o=depth]", depth.toFixed(0) + " in", r);
    set("[data-o=share]", design > 0 ? Math.round(share * 100) + "%" : "—", r);
    set("[data-o=weight]", area > 0 ? Math.round(psf * area).toLocaleString("en-US") + " lb" : "—", r);
    set("[data-o=trucks]", area > 0 ? (psf * area / 5000).toFixed(1) : "—", r);
    var b = $("[data-o=bar]", r);
    if (b) { b.style.width = Math.min(100, share * 100) + "%"; b.className = share >= 1 ? "over" : share >= 0.75 ? "warn" : ""; }
    set("[data-o=msg]", !psf ? "Enter the snow on your roof to estimate its weight." : !design ? "Add a design load to compare. Your building department can tell you the right figure." : share >= 1 ? "This estimate is at or above the design figure entered. Keep people out from under the roof and get a professional to assess it; don’t climb onto a loaded roof." : share >= 0.75 ? "This estimate is getting close to the design figure entered. Watch for sagging, cracking sounds or sticking doors, and consider professional snow removal." : "This estimate is below the design figure entered. Drifts can still load parts of the roof far more than average. Figures are illustrative.", r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
