/* Colorado Insurance Appraiser — site script (nav, drawer, effects, forms, claim tools). No dependencies. */
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
  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

  /* ---------- desktop dropdowns ---------- */
  var closeSubs = function (except) {
    $$(".nav .has-sub.open").forEach(function (li) { if (li === except) return; li.classList.remove("open"); $(".sub-btn", li).setAttribute("aria-expanded", "false"); });
  };
  $$(".nav .has-sub").forEach(function (li) {
    var btn = $(".sub-btn", li), t;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = li.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      closeSubs(li);
    });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); closeSubs(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav")) closeSubs(); });

  /* ---------- mobile drawer (rendered outside the header) ---------- */
  var drawer = $("#drawer"), menuBtn = $(".menu-btn"), lastFocus = null, scrollY0 = 0;
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    if (!drawer || isOpen()) return;
    lastFocus = document.activeElement;
    scrollY0 = window.scrollY;
    body.style.top = -scrollY0 + "px";
    body.classList.add("drawer-open", "scroll-lock");
    menuBtn.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function (restore) {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "scroll-lock");
    body.style.top = "";
    if (restore !== false) window.scrollTo(0, scrollY0);
    menuBtn.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    if (restore !== false && lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (menuBtn && drawer) {
    menuBtn.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeSubs(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, progress, back-to-top, parallax, timeline ---------- */
  var head = $(".site-head"), bar = $(".progress span"), toTop = $(".to-top"), px = $$("[data-parallax]"), tl = $("[data-timeline]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30 || isOpen());
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.12;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0) scale(1.12)";
    });
    if (tl) {
      var r2 = tl.getBoundingClientRect(), mid = window.innerHeight * 0.65;
      var p = Math.max(0, Math.min(1, (mid - r2.top) / r2.height));
      tl.style.setProperty("--tl", p.toFixed(3));
      $$(".tl-step", tl).forEach(function (s) { var sr = s.getBoundingClientRect(); s.classList.toggle("on", (window.innerWidth > 900 ? r2.top : sr.top) < mid && (window.innerWidth > 900 ? (sr.left + sr.width / 2 - r2.left) / r2.width <= p + 0.02 : true)); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- reveal on scroll + counters ---------- */
  var count = function (el) {
    if (el.dataset.done) return; el.dataset.done = "1";
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var q = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - q, 3))); if (q < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(reveal); }

  /* ---------- region tabs ---------- */
  $$("[data-regions]").forEach(function (wrap) {
    var tabs = $$("[role=tab]", wrap);
    var select = function (i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
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
  var gq = $("#gl-q");
  if (gq) gq.addEventListener("input", function () {
    var q = gq.value.trim().toLowerCase(), n = 0;
    $$(".gl-item").forEach(function (it) { var hit = !q || it.textContent.toLowerCase().indexOf(q) > -1; it.hidden = !hit; if (hit) n++; });
    set("[data-gl-count]", n + (n === 1 ? " term" : " terms"));
    var none = $(".gl-none"); if (none) none.hidden = n > 0;
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      $$(".bad", form).forEach(function (f) { f.classList.remove("bad"); });
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      var em = $("[type=email]", form);
      if (em && em.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value.trim())) bad.push(em);
      if (bad.length) { bad.forEach(function (f) { f.classList.add("bad"); }); msg.textContent = "Please complete the highlighted fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you — your details were received. Someone from Colorado Insurance Appraiser will reach out, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error("send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@coloradoinsuranceappraiser.com\">info@coloradoinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding helper ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (root) {
      var run = function () { fn(root); };
      root.addEventListener("input", run);
      root.addEventListener("change", run);
      root.addEventListener("click", function (e) { if (e.target.closest("[data-run], .x")) setTimeout(run, 0); });
      $$(".range input[type=range]", root).forEach(function (r) {
        var out = r.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = r.value + (r.getAttribute("data-unit") || ""); };
        r.addEventListener("input", upd); upd();
      });
      run();
    });
  }
  function rowsTool(name) {
    $$('[data-tool="' + name + '"]').forEach(function (r) {
      var tb = $("tbody", r);
      r.addEventListener("click", function (e) {
        if (e.target.closest("[data-add]")) {
          var tr = tb.rows[0].cloneNode(true);
          $$("input", tr).forEach(function (i) { i.value = ""; });
          tb.appendChild(tr);
          var f = $("input", tr); if (f) f.focus();
        }
        var x = e.target.closest(".x");
        if (x && tb.rows.length > 1) x.closest("tr").remove();
      });
    });
  }
  rowsTool("dep"); rowsTool("roof");

  /* 1. Award gap & fee estimator (home mini + full tool) */
  window.CIA = window.CIA || {};
  var gapMath = CIA.gapMath = function (ins, own, land, feeType, fee, hours, ump, useUmp) {
    var gap = Math.max(0, own - ins);
    var award = ins + gap * land;
    var gain = award - ins;
    var cost = feeType === "pct" ? gain * fee / 100 : feeType === "hourly" ? fee * hours : fee;
    if (useUmp) cost += ump / 2;
    return { gap: gap, award: award, gain: gain, cost: cost, net: gain - cost };
  };
  tool("gap", function (r) {
    var full = !!$("[name=feetype]", r);
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = num($("[name=land]", r)) / 100;
    var feeType = full ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), hours = num($("[name=hours]", r)), ump = num($("[name=umpire]", r));
    var useUmp = full ? $("[name=useump]", r).checked : false;
    $$("[data-show]", r).forEach(function (el) { el.hidden = el.getAttribute("data-show") !== feeType; });
    var m = gapMath(ins, own, land, feeType, fee, hours, ump, useUmp);
    set("[data-o=gap]", money(m.gap), r);
    set("[data-o=award]", money(m.award), r);
    set("[data-o=gain]", money(m.gain), r);
    set("[data-o=cost]", money(m.cost), r);
    set("[data-o=net]", money(m.net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(m.gap / ins * 100) + "%" : "—", r);
    [25, 50, 75].forEach(function (p) {
      var s = gapMath(ins, own, p / 100, feeType, fee, hours, ump, useUmp);
      set("[data-o=a" + p + "]", money(s.award), r); set("[data-o=n" + p + "]", money(s.net), r);
    });
    var be = $("[data-o=breakeven]", r);
    if (be) {
      // smallest landing share whose net >= 0
      var fixed = (feeType === "flat" ? fee : feeType === "hourly" ? fee * hours : 0) + (useUmp ? ump / 2 : 0);
      var share = feeType === "pct" ? (fee >= 100 ? Infinity : fixed / (m.gap * (1 - fee / 100))) : fixed / m.gap;
      be.textContent = !m.gap ? "—" : share > 1 ? "Above 100% — costs exceed the gap" : Math.ceil(share * 100) + "% of the gap";
    }
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, m.award, 1), s3 = Math.min(m.cost, m.gain);
      stack.children[0].style.width = (ins / total * 100) + "%";
      stack.children[1].style.width = (Math.max(0, m.gain - s3) / total * 100) + "%";
      stack.children[2].style.width = (s3 / total * 100) + "%";
    }
    var msg = $("[data-o=msg]", r);
    if (msg) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (m.gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal resolves how much a covered loss costs — with no gap, there’s nothing to appraise.";
      else if (full && m.net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (m.gap / ins < 0.1 && m.gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      msg.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
  var depMath = CIA.depMath = function (items, cap, op, deduct, prior, nonrec) {
    var rcv = 0, dep = 0;
    items.forEach(function (it) { var c = it.rcv * (op ? 1.2 : 1); var d = Math.min(cap, it.age / (it.life || 1)) * c; rcv += c; dep += d; it.acv = c - d; });
    var acv = rcv - dep;
    var first = Math.max(0, acv - deduct - prior);
    var total = Math.max(0, (nonrec ? acv : rcv) - deduct - prior);
    return { rcv: rcv, dep: dep, acv: acv, first: first, held: Math.max(0, total - first), total: total };
  };
  tool("dep", function (r) {
    var items = $$("tbody tr", r).map(function (tr) { return { tr: tr, rcv: num($("[name=rcv]", tr)), age: num($("[name=age]", tr)), life: num($("[name=life]", tr)) }; });
    var m = depMath(items, num($("[name=cap]", r)) / 100 || 0.8, $("[name=op]", r).checked, num($("[name=deduct]", r)), num($("[name=prior]", r)), $("[name=nonrec]", r).checked);
    items.forEach(function (it) { var o = $("[data-o=row]", it.tr); if (o) o.textContent = money(it.acv); });
    set("[data-o=rcv]", money(m.rcv), r); set("[data-o=dep]", money(m.dep), r); set("[data-o=acv]", money(m.acv), r);
    set("[data-o=first]", money(m.first), r); set("[data-o=held]", money(m.held), r); set("[data-o=total]", money(m.total), r);
    set("[data-o=deppct]", m.rcv ? Math.round(m.dep / m.rcv * 100) + "%" : "0%", r);
  });

  /* 3. Roof pitch & squares (multi-plane) */
  var roofMath = CIA.roofMath = function (planes, waste) {
    var plan = 0, surf = 0, steep = 0;
    planes.forEach(function (p) { var mult = Math.sqrt(1 + Math.pow(p.pitch / 12, 2)); var s = p.area * mult; p.sq = s / 100; plan += p.area; surf += s; if (p.pitch >= 7) steep += s; });
    return { plan: plan, surface: surf, sq: surf / 100, order: surf / 100 * (1 + waste), steepSq: steep / 100 };
  };
  tool("roof", function (r) {
    var planes = $$("tbody tr", r).map(function (tr) { return { tr: tr, area: num($("[name=parea]", tr)), pitch: num($("[name=ppitch]", tr)) }; });
    var m = roofMath(planes, num($("[name=waste]", r)) / 100);
    planes.forEach(function (p) { var o = $("[data-o=prow]", p.tr); if (o) o.textContent = p.sq.toFixed(2); });
    var price = num($("[name=price]", r)), car = num($("[name=carrier]", r));
    set("[data-o=plan]", Math.round(m.plan).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=surface]", Math.round(m.surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", m.sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(m.order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(m.order * 3)), r);
    set("[data-o=steepsq]", m.steepSq.toFixed(2) + " sq", r);
    set("[data-o=cost]", price ? money(m.order * price) : "—", r);
    set("[data-o=vs]", car ? ((m.sq - car >= 0 ? "+" : "−") + Math.abs(m.sq - car).toFixed(2) + " sq (" + (car ? Math.round((m.sq - car) / car * 100) : 0) + "%)") : "—", r);
    set("[data-o=steep]", m.steepSq > 0 ? m.steepSq.toFixed(2) + " squares sit at 7/12 or steeper. Check that the carrier’s estimate includes steep-roof labor for those planes." : "No planes at 7/12 or steeper, so steep-roof charges typically wouldn’t apply.", r);
  });

  /* 4. Hail percentage deductible */
  var dedMath = CIA.dedMath = function (covA, pct, flat, loss) {
    var pd = covA * pct / 100;
    return { pd: pd, pdpay: Math.max(0, loss - pd), flatpay: Math.max(0, loss - flat), diff: Math.min(loss, pd) - Math.min(loss, flat) };
  };
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var m = dedMath(covA, pct, flat, loss);
    set("[data-o=pd]", money(m.pd), r); set("[data-o=pdpay]", money(m.pdpay), r); set("[data-o=flatpay]", money(m.flatpay), r); set("[data-o=diff]", money(m.diff), r);
    [1, 2, 3].forEach(function (p) { var s = dedMath(covA, p, flat, loss); set("[data-o=d" + p + "]", money(s.pd), r); set("[data-o=p" + p + "]", money(s.pdpay), r); });
    set("[data-o=below]", !loss ? "Enter an estimated loss to compare payouts." : loss <= m.pd ? "This loss falls entirely within the percentage deductible, so no payment would be owed under it." : "The loss exceeds the percentage deductible by " + money(loss - m.pd) + ".", r);
    var bar = $(".stack", r);
    if (bar) { var a = loss > 0 ? Math.min(m.pd, loss) / loss * 100 : 0; bar.children[0].style.width = a + "%"; bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%"; }
  });

  /* 5. Claim timeline builder (.ics export) */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, de = $("[name=est]", r).value;
    var list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), est = de ? new Date(de + "T12:00:00") : null;
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(base, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you reasonably can." },
      { d: add(base, num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarping, dry-out and board-up protect the property and are usually part of the claim." },
      { d: add(base, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Check the insurer’s letter: the window often runs from its request date." }
    ];
    if (est) {
      var dem = add(est, num($("[name=appr]", r)));
      plan.push({ d: dem, t: "Decide whether to demand appraisal", n: "Compare estimates, gather documentation and decide whether to make a written appraisal demand." });
      plan.push({ d: add(dem, num($("[name=name]", r))), t: "Name your appraiser (if appraisal is demanded)", n: "Many appraisal clauses give each side 20 days after a demand to name an appraiser." });
    }
    plan.push({ d: add(base, num($("[name=rcd]", r))), t: "Recoverable depreciation window", n: "Confirm the exact time your policy allows to complete repairs and claim the holdback." });
    plan.push({ d: add(base, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Read the Suit Against Us clause and confirm the date with a Colorado attorney well before it arrives." });
    plan.sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + ' <em>' + badge + '</em></b><strong>' + p.t + '</strong><span>' + p.n + '</span></li>';
    }).join("");
  });
  CIA.ics = function () {
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
    var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
    var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
    var out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Colorado Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
    plan.forEach(function (p, i) {
      var end = new Date(p.d); end.setDate(end.getDate() + 1);
      out.push("BEGIN:VEVENT", "UID:cia-" + ds(p.d) + "-" + i + "@coloradoinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
    });
    out.push("END:VCALENDAR");
    return out.join("\r\n");
  };
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var d = $("[name=dol]"); if (d) d.focus(); return; }
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([CIA.ics()], { type: "text/calendar" }));
      a.download = "colorado-claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness check (Yes / Partly / No) */
  $$('[data-tool="ready"]').forEach(function (r) {
    var items = $$(".quiz li", r);
    var calc = function () {
      var got = 0, max = 0, answered = 0, todo = [];
      items.forEach(function (li) {
        var w = parseFloat(li.getAttribute("data-w")) || 1; max += w;
        var on = $("[aria-pressed=true]", li);
        if (on) { answered++; var v = parseFloat(on.getAttribute("data-v")); got += w * v; if (v < 1) todo.push(li.getAttribute("data-fix")); }
      });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? pct : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1f7a4d" : pct >= 45 ? "#c98a00" : "#002868"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the documentation a panel expects; the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before invoking appraisal — each one weakens your number." : "Not ready yet. Invoking appraisal now risks locking in a low award. Work through the list first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) { ul.innerHTML = ""; (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); }); }
      set("[data-o=count]", answered + " / " + items.length, r);
    };
    items.forEach(function (li) {
      $$("button", li).forEach(function (b) {
        b.addEventListener("click", function () { $$("button", li).forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); }); calc(); });
      });
    });
    var reset = $("[data-reset]", r);
    if (reset) reset.addEventListener("click", function () { $$(".ypn button", r).forEach(function (b) { b.setAttribute("aria-pressed", "false"); }); calc(); });
    calc();
  });

  /* 7. Hail size & roof impact checker. Approximate reference values for ice spheres at terminal speed. */
  var HAIL = { "0.75": [0.3, 20], "1": [0.8, 25], "1.25": [2.0, 31], "1.5": [4.3, 36], "1.75": [8.1, 40], "2": [13.9, 44], "2.5": [29.6, 50], "2.75": [41.5, 53], "3": [61.0, 56], "4": [154.0, 65] };
  var hailMath = CIA.hailMath = function (size, thresh, age, wind) {
    var ratio = size / thresh;
    var adj = ratio * (1 + Math.min(age, 25) * 0.012) * (1 + wind * 0.08);
    var band = adj < 0.8 ? "Low" : adj < 1 ? "Possible" : adj < 1.3 ? "Likely" : "Very likely";
    return { ratio: ratio, adj: adj, band: band, energy: (HAIL[String(size)] || [0, 0])[0], speed: (HAIL[String(size)] || [0, 0])[1] };
  };
  tool("hail", function (r) {
    var sizeSel = $("[name=size]", r), roofSel = $("[name=roof]", r);
    var size = parseFloat(sizeSel.value), thresh = parseFloat(roofSel.value);
    var m = hailMath(size, thresh, num($("[name=age]", r)), num($("[name=wind]", r)));
    set("[data-o=band]", m.band, r);
    set("[data-o=energy]", "≈ " + m.energy + " ft-lb", r);
    set("[data-o=speed]", "≈ " + m.speed + " mph", r);
    set("[data-o=thresh]", "≈ " + thresh + " in", r);
    set("[data-o=ratio]", Math.round(m.ratio * 100) + "%", r);
    var bar = $("[data-o=meter]", r); if (bar) bar.style.width = Math.min(100, m.adj / 1.6 * 100) + "%";
    var name = roofSel.options[roofSel.selectedIndex].getAttribute("data-name").toLowerCase();
    set("[data-o=advice]", m.band === "Low"
      ? "Hail this size is usually below the threshold often cited for new " + name + ". Still check gutters, vents, screens and window wraps — soft metals dent at smaller sizes."
      : m.band === "Possible"
        ? "Close to the commonly cited threshold for " + name + ". Age, brittleness and wind can tip the balance; an on-site inspection with test squares is worth it."
        : "Hail this size often exceeds the threshold cited for " + name + ". Photograph every slope, soft metal and elevation before repairs, and keep the stones’ photos.", r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
