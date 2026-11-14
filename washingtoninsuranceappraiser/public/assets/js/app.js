/* Washington Insurance Appraiser — site script (nav, drawer, effects, forms, claim calculators). No dependencies.
   Nothing entered into the calculators is stored or sent anywhere. */
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
  document.documentElement.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    var hover = function () { return window.matchMedia("(hover: hover)").matches; };
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!hover()) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover()) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
    li.addEventListener("focusout", function (e) { if (!li.contains(e.relatedTarget)) { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".drawer-scrim"), lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    if (scrim) scrim.hidden = false;
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    if (burger) burger.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    setTimeout(function () { if (scrim && !body.classList.contains("drawer-open")) scrim.hidden = true; }, 320);
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1180) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- header, progress bar, back-to-top, parallax, steps line ---------- */
  var head = $(".site-head"), bar = $(".progress span"), toTop = $(".to-top");
  var px = $$("[data-parallax]"), steps = $("[data-steps]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0)";
    });
    if (steps) {
      var sr = steps.getBoundingClientRect(), mid = window.innerHeight * 0.62;
      var line = $(".steps-line span", steps);
      var pct = Math.max(0, Math.min(1, (mid - sr.top) / sr.height));
      if (line) line.style.height = (pct * 100) + "%";
      $$(".step", steps).forEach(function (s) { s.classList.toggle("on", s.getBoundingClientRect().top < mid); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); var s = $(".skip"); if (s) s.focus({ preventScroll: true }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1500;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); }); });
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  var targets = $$(".rv, .numbers");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(reveal); }

  /* ---------- peril rail buttons ---------- */
  $$("[data-rail]").forEach(function (b) {
    b.addEventListener("click", function () {
      var rail = b.closest(".sec").querySelector(".rail");
      if (!rail) return;
      var item = rail.querySelector(".rail-item");
      var step = item ? item.getBoundingClientRect().width + 18 : 300;
      rail.scrollBy({ left: step * parseInt(b.getAttribute("data-rail"), 10), behavior: reduce ? "auto" : "smooth" });
    });
  });

  /* ---------- glossary search ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".glossary .gl-item").forEach(function (it) {
      var hit = !q || it.textContent.toLowerCase().indexOf(q) > -1;
      it.hidden = !hit; if (hit) n++;
    });
    set("[data-gl-count]", n + (n === 1 ? " term" : " terms") + (q ? " match “" + gf.value.trim() + "”" : ""));
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and someone from Washington Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@washingtoninsuranceappraiser.com\">info@washingtoninsuranceappraiser.com</a>."; msg.classList.add("err"); })
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

  /* 1. Appraisal payoff (home mini + full) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var cost = feeType === "pct" ? gain * fee / 100 : fee;
    if (useUmp) cost += ump / 2;
    var net = gain - cost;
    set("[data-o=gap]", money(gap), r); set("[data-o=award]", money(award), r); set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r); set("[data-o=net]", money(net), r);
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
      else if (gap <= 0) t = "Your number isn’t higher than the insurer’s. Appraisal resolves how much a covered loss costs, so with no gap there’s nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. Replacement cost holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0, cap = (num($("[name=cap]", r)) || 80) / 100;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r)), nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded);
    set("[data-o=rcv]", money(rcv), r); set("[data-o=dep]", money(dep), r); set("[data-o=acv]", money(acv), r); set("[data-o=first]", money(first), r);
    set("[data-o=held]", nonrec ? money(0) : money(Math.min(dep, Math.max(0, rcv - ded) - first)), r);
    set("[data-o=total]", money(nonrec ? first : Math.max(0, rcv - ded)), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
  });
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (e) {
      if (e.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr);
      }
      var x = e.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof pitch & squares */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100, surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, most estimating software adds a steep-roof charge. Check that the insurer’s estimate includes it." : pitch >= 7 ? "At 7/12, steep charges often begin. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.", r);
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.min(pd, loss) - Math.min(flat, loss)), r);
    set("[data-o=below]", loss <= pd && loss > 0 ? "This loss falls entirely within the percentage deductible, so no payment would be owed under it." : loss > 0 ? "The loss is " + money(loss - pd) + " more than the percentage deductible." : "Enter an estimated loss to compare payments.", r);
    var b = $(".stack", r);
    if (b && loss > 0) { var a = Math.min(pd, loss) / loss * 100; b.children[0].style.width = a + "%"; b.children[1].style.width = (100 - a) + "%"; }
  });

  /* 5. Claim timeline planner + .ics export */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-set target." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarps, water extraction and board-up protect the claim and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies allow 60 days after the insurer asks. Count from the date on its letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Policies set a deadline to finish repairs and claim holdback. Confirm the exact number of days in your policy." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Washington law sets a one-year minimum and many homeowner policies use one year. Talk to an attorney well before this date." }
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
      if (!plan.length) { var d = $("[name=dol]"); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Washington Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:wia-" + ds(p.d) + "-" + i + "@washingtoninsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "washington-claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness quiz */
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
      set("[data-o=score]", answered ? pct : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#008457" : pct >= 45 ? "#e8bd00" : "#e8613c"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the documentation a panel expects. The next step is a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) {
        ul.innerHTML = "";
        (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); });
      }
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

  /* 7. Wildfire total-loss coverage check */
  tool("fire", function (r) {
    var sqft = num($("[name=sqft]", r)), psf = num($("[name=psf]", r)), codePct = num($("[name=code]", r)) / 100, debris = num($("[name=debris]", r));
    var covA = num($("[name=cova]", r)), erc = num($("[name=erc]", r)) / 100, ol = num($("[name=ol]", r)) / 100;
    var cpct = num($("[name=cpct]", r)) / 100, contents = num($("[name=contents]", r));
    var base = sqft * psf, code = base * codePct, need = base + code + debris;
    var aext = covA * (1 + erc), olAmt = covA * ol, have = aext + olAmt;
    var diff = need - have, climit = covA * cpct, cgap = contents - climit;
    set("[data-o=base]", money(base), r); set("[data-o=codeamt]", money(code), r); set("[data-o=deb]", money(debris), r);
    set("[data-o=aext]", money(aext), r); set("[data-o=olamt]", money(olAmt), r);
    set("[data-o=need]", money(need), r); set("[data-o=have]", money(have), r);
    set("[data-o=gaplabel]", diff > 0 ? "Estimated shortfall" : "Estimated cushion", r);
    set("[data-o=short]", money(Math.abs(diff)), r);
    set("[data-o=cgap]", money(climit) + (cgap > 0 ? " / " + money(cgap) + " short" : " / covered"), r);
    var m;
    if (!need || !covA) m = "Enter your home size, rebuild cost and dwelling limit.";
    else if (diff > 0) m = "On these figures, rebuilding could cost about " + money(diff) + " more than the dwelling, extended replacement and code coverage available. Check how your policy treats debris removal, and get local rebuild bids.";
    else m = "On these figures, your dwelling coverage looks like it could cover the rebuild with about " + money(-diff) + " to spare. Real bids after a large fire can run higher, so test a higher cost per square foot too.";
    if (cgap > 0 && need && covA) m += " Your contents estimate is about " + money(cgap) + " above the contents limit.";
    set("[data-o=firemsg]", m, r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
