/* Alaska Insurance Appraiser — site script: nav, drawer, effects, forms and claim tools. No dependencies. */
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
  var hoverable = window.matchMedia("(hover: hover)").matches;

  /* ---------- desktop dropdowns ---------- */
  var closeSubs = function (except) {
    $$(".has-sub.open").forEach(function (li) {
      if (li === except) return;
      li.classList.remove("open");
      var b = $(".sub-btn", li); if (b) b.setAttribute("aria-expanded", "false");
    });
  };
  $$(".has-sub").forEach(function (li) {
    var btn = $(".sub-btn", li), t;
    var open = function () { closeSubs(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    var shut = function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); li.classList.contains("open") ? shut() : open(); });
    li.addEventListener("mouseenter", function () { if (!hoverable) return; clearTimeout(t); open(); });
    li.addEventListener("mouseleave", function () { if (!hoverable) return; t = setTimeout(shut, 180); });
    li.addEventListener("focusout", function (e) { if (!li.contains(e.relatedTarget)) shut(); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".has-sub")) closeSubs(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim");
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    if (!drawer) return;
    scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus({ preventScroll: true }); }, 60);
  };
  var closeDrawer = function (restoreFocus) {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("aria-hidden", "true");
    drawer.setAttribute("inert", "");
    burger.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!isOpen()) scrim.hidden = true; }, 300);
    if (restoreFocus) burger.focus({ preventScroll: true });
  };
  if (drawer && burger) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(true); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1180) closeDrawer(false); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeSubs(); if (isOpen()) closeDrawer(true); }
  });

  /* ---------- scroll effects: solid header, back to top, hero parallax, process trail ---------- */
  var head = $(".site-head"), toTop = $(".to-top"), px = $$("[data-parallax]"), trail = $("[data-trail]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 40);
    if (toTop) toTop.classList.toggle("show", y > 700);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      el.style.transform = "translate3d(0," + (y * (parseFloat(el.getAttribute("data-parallax")) || 0.2)).toFixed(1) + "px,0)";
    });
    if (trail) {
      var r = trail.getBoundingClientRect(), mid = vh * 0.62;
      var pct = Math.max(0, Math.min(1, (mid - r.top) / Math.max(1, r.height)));
      var line = $(".trail-line i", trail);
      if (line) { line.style.width = (pct * 100) + "%"; line.style.setProperty("--fill", (pct * 100) + "%"); }
      var steps = $$(".trail-step", trail);
      steps.forEach(function (s, i) {
        var sr = s.getBoundingClientRect();
        var wide = window.innerWidth > 1020;
        s.classList.toggle("on", wide ? pct >= (i / steps.length) + 0.02 : sr.top < mid);
      });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); }); });
  var targets = $$(".rv");
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
    var co = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { count(en.target); co.unobserve(en.target); } });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { co.observe(el); });
  } else {
    targets.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- glossary search ---------- */
  var gq = $("#gq");
  if (gq) {
    var terms = $$(".gloss .term"), gc = $("[data-gcount]"), none = $("[data-gnone]");
    var filt = function () {
      var q = gq.value.trim().toLowerCase(), n = 0;
      terms.forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
      if (gc) gc.textContent = q ? n + " of " + terms.length + " terms match" : terms.length + " terms";
      if (none) none.hidden = n > 0;
    };
    gq.addEventListener("input", filt); filt();
  }

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      $$("[required]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); });
      if (bad.length) { msg.textContent = "Please fill in the required fields and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (!d || !d.ok) throw new Error("send failed");
          form.reset();
          msg.textContent = "Thanks, your claim details were received. Someone from Alaska Insurance Appraiser will be in touch, usually within one business day.";
          msg.classList.add("ok");
        })
        .catch(function () {
          msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@alaskainsuranceappraiser.com\">info@alaskainsuranceappraiser.com</a>.";
          msg.classList.add("err");
        })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binder ---------- */
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

  /* 1. Appraisal gap & fee estimator (full + home mini) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r)), travel = num($("[name=travel]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var award = ins + gap * land;
    var gain = award - ins;
    var cost = (feeType === "pct" ? gain * fee / 100 : fee) + travel + (useUmp ? ump / 2 : 0);
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
      s[2].style.width = (Math.min(cost, gain) / total * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal resolves how much a covered loss costs; with no gap there is nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV depreciation & holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0, cap = (num($("[name=cap]", r)) || 80) / 100;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      set("[data-o=row]", money(c - d), tr);
    });
    var ded = num($("[name=deduct]", r)), nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), full = Math.max(0, rcv - ded);
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
    r.addEventListener("click", function (e) {
      if (e.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr);
        $("input", tr).focus();
      }
      var x = e.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof area & pitch */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var eave = num($("[name=eave]", r)), iws = eave * 6;   /* two 36-inch courses along the eaves */
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=iws]", Math.round(iws).toLocaleString("en-US") + " sq ft (" + Math.ceil(iws / 200) + " rolls)", r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge. Check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 some estimates begin applying steep charges. Confirm how yours treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.", r);
  });

  /* 4. Percentage deductible (earthquake / wind) */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.min(loss, pd) - Math.min(loss, flat)), r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payouts." : loss <= pd ? "This loss falls entirely within the percentage deductible, so no payment would be owed under it. Small estimate differences matter here." : "The loss exceeds the percentage deductible by " + money(loss - pd) + ".", r);
    var bar = $(".stack", r);
    if (bar) {
      var a = loss > 0 ? Math.min(pd, loss) / loss * 100 : 0;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%";
    }
  });

  /* 5. Claim timeline planner + .ics export */
  var plan = [];
  tool("dates", function (r) {
    var input = $("[name=dol]", r), list = $("[data-o=timeline]", r);
    if (!input.value) {
      var d = new Date(); d.setDate(d.getDate() - 10);
      input.value = d.getFullYear() + "-" + ("0" + (d.getMonth() + 1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2);
    }
    var base = new Date(input.value + "T12:00:00");
    if (isNaN(base)) { list.innerHTML = "<li><b>Pick your date of loss</b>Milestones will appear here.</li>"; plan = []; return; }
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var x = new Date(base); x.setDate(x.getDate() + days); return x; };
    var fmt = function (x) { return x.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you reasonably can." },
      { d: add(num($("[name=mitig]", r))), t: "Protect the property and keep receipts", n: "Tarps, heat, snow removal and drying protect the claim and are often reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies count this from the date of the carrier’s request. Check your letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Confirm the exact period in your policy and ask in writing for more time if repairs are delayed." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Use the period in your policy. Talk to an Alaska attorney well before this date." }
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
      if (!plan.length) return;
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Alaska Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:aia-" + ds(p.d) + "-" + i + "@alaskainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "alaska-claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal file checkup */
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
      var ring = $("[data-o=ring]", r);
      if (ring) { ring.style.setProperty("--p", answered ? pct : 0); ring.style.setProperty("--ring", pct >= 75 ? "#1E7A4E" : pct >= 45 ? "#FFB612" : "#B3261E"); }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects. The next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before invoking appraisal; each one weakens your number if it is missing." : "Not ready yet. Invoking appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) {
        ul.innerHTML = "";
        (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); });
      }
      set("[data-o=count]", answered + " / " + items.length, r);
    };
    items.forEach(function (li) {
      $$(".yn button", li).forEach(function (b) {
        b.addEventListener("click", function () {
          $$(".yn button", li).forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
          calc();
        });
      });
    });
    var reset = $("[data-reset]", r);
    if (reset) reset.addEventListener("click", function () { $$(".yn button", r).forEach(function (b) { b.setAttribute("aria-pressed", "false"); }); calc(); });
    calc();
  });

  /* 7. Roof snow load */
  tool("snow", function (r) {
    var psf = num($("[name=d1]", r)) / 12 * num($("[name=t1]", r)) + num($("[name=d2]", r)) / 12 * num($("[name=t2]", r));
    var area = num($("[name=area]", r)), design = num($("[name=design]", r));
    var lbs = psf * area, share = design > 0 ? psf / design : 0;
    set("[data-o=psf]", psf.toFixed(1) + " lb/ft²", r);
    set("[data-o=share]", design > 0 ? Math.round(share * 100) + "%" : "—", r);
    set("[data-o=lbs]", Math.round(lbs).toLocaleString("en-US") + " lb", r);
    set("[data-o=tons]", (lbs / 2000).toFixed(1) + " tons", r);
    set("[data-o=trucks]", (lbs / 5000).toFixed(1) + " pickups (5,000 lb each)", r);
    var bar = $("[data-o=bar]", r); if (bar) bar.style.width = Math.min(100, share * 100) + "%";
    set("[data-o=snowmsg]", !design ? "Enter a design load to compare." : share >= 1 ? "The estimated load meets or exceeds the design figure you entered. Keep people clear and get professional help to remove it safely." : share >= 0.8 ? "The load is close to the design figure. Watch for sagging, cracking or sticking doors, and plan safe removal." : share >= 0.5 ? "A meaningful load. Keep an eye on drifts, valleys and areas below higher roofs." : "Well under the design figure you entered, on average. Drifts can still concentrate load.", r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
