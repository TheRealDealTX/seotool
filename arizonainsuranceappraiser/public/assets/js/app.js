/* Arizona Insurance Appraiser — site script (nav, drawer, reveal, forms, claim calculators). No dependencies. */
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
  var body = document.body, root = document.documentElement;
  root.classList.remove("no-js"); root.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function (except) {
    $$(".menu li.open").forEach(function (o) { if (o === except) return; o.classList.remove("open"); var b = $("[data-drop]", o); if (b) b.setAttribute("aria-expanded", "false"); });
  };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); closeDrops(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), veil = $(".drawer-veil"), lastFocus = null, hideT;
  var openDrawer = function () {
    clearTimeout(hideT);
    lastFocus = document.activeElement;
    if (veil) veil.hidden = false;
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open"); root.classList.add("lock"); body.classList.add("lock"); });
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!drawer || !body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock"); root.classList.remove("lock");
    burger.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    hideT = setTimeout(function () { if (veil) veil.hidden = true; }, 300);
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1120) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- header state, back-to-top, parallax ---------- */
  var head = $(".site-head"), toTop = $(".to-top"), px = $$("[data-parallax]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var box = el.parentElement.getBoundingClientRect();
      if (box.bottom < 0 || box.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.12;
      var lim = box.height * 0.1;  // the image layer overhangs its section by 14% each side; stay inside that
      var off = Math.max(-lim, Math.min(lim, (box.top + box.height / 2 - window.innerHeight / 2) * -k));
      el.style.transform = "translate3d(0," + off.toFixed(1) + "px,0)";
    });
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$(".pgrid, .cgrid, .trows, .posts, .myths, .regions, .idx, .chips").forEach(function (g) {
    $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); });
  });
  var targets = $$(".rv");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(reveal); }

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".glossary dt").forEach(function (dt) {
      var dd = dt.nextElementSibling;
      var hit = !q || (dt.textContent + " " + dd.textContent).toLowerCase().indexOf(q) > -1;
      dt.hidden = dd.hidden = !hit;
      if (hit) n++;
    });
    set("[data-gloss-count]", n + (n === 1 ? " term" : " terms") + (q ? " match" : ""));
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
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and someone from Arizona Insurance Appraiser will reach out, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@arizonainsuranceappraiser.com\">info@arizonainsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (r) {
      var run = function () { fn(r); };
      r.addEventListener("input", run);
      r.addEventListener("change", run);
      r.addEventListener("click", function (e) { if (e.target.closest("[data-run]")) setTimeout(run, 0); });
      $$(".range input[type=range]", r).forEach(function (rg) {
        var out = rg.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = rg.value + (rg.getAttribute("data-unit") || ""); };
        rg.addEventListener("input", upd); upd();
      });
      run();
    });
  }

  /* 1. Appraisal payoff estimator (home mini + full tool) */
  $$('[data-tool="gap"] [name=docs]').forEach(function (sel) {
    sel.addEventListener("change", function () {
      var r = sel.closest("[data-tool]"), rg = $("[name=land]", r);
      if (rg) { rg.value = sel.value; rg.dispatchEvent(new Event("input", { bubbles: true })); }
    });
  });
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = num($("[name=land]", r)) / 100;
    var feeEl = $("[name=fee]", r), feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num(feeEl), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var gain = gap * land;
    var award = ins + gain;
    var umpShare = useUmp ? ump / 2 : 0;
    var cost = feeEl ? (feeType === "pct" ? gain * fee / 100 : fee) + umpShare : 0;
    var net = gain - cost;
    // Break-even: smallest share of the gap where net >= 0.
    var be = null;
    if (feeEl && gap > 0) {
      be = feeType === "pct" ? (fee >= 100 ? Infinity : umpShare / (gap * (1 - fee / 100))) : (fee + umpShare) / gap;
    }
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=breakeven]", be === null ? "—" : be > 1 ? "Not reachable" : Math.ceil(be * 100) + "% of the gap", r);
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
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal settles how much a covered loss costs; with no gap, there is nothing to appraise.";
      else if (feeEl && net <= 0) t = "At these inputs, appraisal costs would absorb the whole recovery. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready when you call.";
      m.textContent = t;
    }
  });

  /* 2. Depreciation recovery */
  tool("dep", function (r) {
    var rows = $$("tbody tr", r), rcv = 0, dep = 0;
    var cap = (num($("[name=cap]", r)) || 80) / 100;
    rows.forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, Math.max(0, age) / life) * c;
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

  /* 3. Roof pitch, squares & material */
  tool("roof", function (r) {
    var modeEl = $("[name=mode]:checked", r), mode = modeEl ? modeEl.value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    var mat = $("[name=mat]", r) ? $("[name=mat]", r).value : "tile";
    var unitLabel = { tile: "Approx. field tiles (90/square)", shingle: "Shingle bundles (3/square)", metal: "Approx. 3-ft panels (by area)", foam: "Foam area (sq ft, no waste)" }[mat];
    var units = mat === "tile" ? Math.ceil(order * 90) : mat === "shingle" ? Math.ceil(order * 3) : Math.round(surface);
    if (mat === "metal") {
      // panels = area with waste / (3 ft coverage × panel run); run ≈ rafter length from eave to ridge.
      var run = mode === "dims" ? ((W + 2 * oh) / 2) * mult : Math.sqrt(foot) / 2 * mult;
      units = run > 0 ? Math.ceil(surface * (1 + waste) / (3 * run)) : 0;
    }
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (mat === "foam" ? sq : order).toFixed(2), r);
    set("[data-o=unitlabel]", unitLabel, r);
    set("[data-o=units]", units.toLocaleString("en-US"), r);
    set("[data-o=cost]", price ? money((mat === "foam" ? sq : order) * price) : "—", r);
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = mat === "foam"
      ? (pitch > 2 ? "Spray foam is normally used on low-slope roofs; check that the pitch entered is right." : "Low-slope foam roofs are priced by area and thickness. Confirm the carrier measured coating and foam separately.")
      : pitch >= 8 ? "At " + pitch + "/12 most estimating systems add a steep-roof labor charge. Check that the carrier’s estimate includes it."
      : pitch >= 7 ? "At 7/12 some carriers start applying steep charges. Confirm how your estimate treats this pitch."
      : "Walkable pitch: a steep charge is not usually expected." + (mat === "tile" ? " Tile still needs careful walking; note any breakage caused by inspections." : "");
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payouts." : loss <= pd ? "This loss falls entirely within the percentage deductible, so no payment would be owed under it." : "The loss exceeds the percentage deductible by " + money(loss - pd) + ".", r);
    var bar = $(".stack", r);
    if (bar && loss > 0) {
      var a = Math.min(pd, loss) / loss * 100;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (100 - a) + "%";
    }
  });

  /* 5. Claim deadline calendar */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Pick your date of loss</b><span>Your deadlines will appear here.</span></li>"; plan = []; return; }
    var base = new Date(d0 + "T12:00:00");
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is your own target." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarps, drying and board-up protect the claim and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies allow 60 days from the carrier’s written request. Count from the date on that letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Confirm the exact number of days your policy allows to finish repairs and claim the holdback." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Many policies require any lawsuit within one or two years of the loss. Talk to an Arizona attorney well before this." }
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
      if (!plan.length) { var d = $('[data-tool="dates"] [name=dol]'); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Arizona Insurance Appraiser//Claim Deadline Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:aia-" + ds(p.d) + "-" + i + "@arizonainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "arizona-claim-deadlines.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Claim file readiness check */
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
      set("[data-o=score]", answered ? pct : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1f9e95" : pct >= 45 ? "#d4a43a" : "#8e1b1b"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before invoking appraisal; each missing item weakens your number." : "Not ready yet. Invoking appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) {
        ul.textContent = "";
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

  /* 7. Tile roof repair-or-replace checker */
  tool("tile", function (r) {
    var sq = num($("[name=sq]", r)), tps = num($("[name=tps]", r)) || 90, broken = num($("[name=broken]", r));
    var slopes = num($("[name=slopes]", r)) / 100, uage = num($("[name=uage]", r)), avail = $("[name=avail]", r).value;
    var ptile = num($("[name=ptile]", r)), psq = num($("[name=psq]", r));
    var total = sq * tps, share = total > 0 ? broken / total : 0;
    // Score 0-100: breakage share (up to 40), underlayment age (up to 35), availability (up to 25).
    var sBreak = Math.min(40, share / 0.08 * 40);
    var sAge = uage >= 25 ? 35 : uage >= 20 ? 28 : uage >= 15 ? 18 : uage >= 10 ? 8 : 0;
    var sAvail = avail === "no" ? 25 : avail === "unknown" ? 12 : 0;
    var score = Math.round(Math.min(100, sBreak + sAge + sAvail));
    var verdict = score >= 65 ? "Strong" : score >= 40 ? "Arguable" : "Weak";
    set("[data-o=verdict]", verdict + " (" + score + "/100)", r);
    var meter = $("[data-o=meter]", r); if (meter) meter.style.left = "calc(" + score + "% - 3px)";
    set("[data-o=share]", (share * 100).toFixed(1) + "%", r);
    set("[data-o=repair]", money(broken * ptile), r);
    set("[data-o=slope]", money(sq * slopes * psq), r);
    set("[data-o=full]", money(sq * psq), r);
    var why = [];
    why.push(share >= 0.05 ? "Breakage is spread across a meaningful share of the roof." : share >= 0.02 ? "Breakage is moderate; slope-by-slope documentation will matter." : "Breakage is a small share of the roof, which favors repair on its own.");
    why.push(uage >= 20 ? "At " + uage + " years the underlayment may not survive tiles being lifted and reset. Get photos and a roofer’s written opinion." : uage >= 15 ? "Underlayment is middle-aged; its condition should be checked in several places." : "Underlayment is relatively young, which supports a true repair.");
    why.push(avail === "no" ? "A discontinued tile makes a matching repair difficult, especially on visible slopes." : avail === "unknown" ? "Find out whether the exact tile is still made or available as salvage." : "Matching tile is available, which supports repair of isolated damage.");
    set("[data-o=why]", why.join(" "), r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
