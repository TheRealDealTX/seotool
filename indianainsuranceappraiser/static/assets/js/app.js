/* Indiana Insurance Appraiser — site script (nav, drawer, reveal, forms, claim tools). No dependencies. */
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
  var root = document.documentElement, body = document.body;
  root.classList.remove("no-js"); root.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function (except) {
    $$(".menu .has-drop.open").forEach(function (o) { if (o === except) return; o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); });
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

  /* ---------- mobile drawer (rendered outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim"), lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    body.classList.add("drawer-open");
    root.classList.add("lock");
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    if (scrim) scrim.hidden = false;
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open");
    root.classList.remove("lock");
    if (burger) burger.setAttribute("aria-expanded", "false");
    if (drawer) { drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true"); }
    if (scrim) setTimeout(function () { if (!body.classList.contains("drawer-open")) scrim.hidden = true; }, 320);
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- header state, progress bar, back-to-top, process timeline ---------- */
  var head = $(".site-head"), bar = $(".progress span"), toTop = $(".to-top"), tl = $("[data-tl]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = root.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (tl) {
      var r = tl.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh * 0.85 - r.top) / (r.height + vh * 0.35)));
      tl.style.setProperty("--p", p.toFixed(3));
      var steps = $$(".tl-step", tl);
      steps.forEach(function (s, i) { s.classList.toggle("on", p >= (i + 0.35) / steps.length); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- reveal & counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  var show = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  var targets = $$(".rv, .counters");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { show(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(show); }

  /* ---------- claim-zone tabs ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
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
        if (e.key === "ArrowDown" || e.key === "ArrowRight") { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
        if (e.key === "Home") { e.preventDefault(); select(0, true); }
        if (e.key === "End") { e.preventDefault(); select(tabs.length - 1, true); }
      });
    });
  });

  /* ---------- glossary search ---------- */
  var gf = $("#gloss-filter");
  if (gf) {
    var gc = $("[data-gcount]");
    var runG = function () {
      var q = gf.value.trim().toLowerCase(), n = 0;
      $$(".glossary .g-item").forEach(function (it) { var hit = !q || it.textContent.toLowerCase().indexOf(q) > -1; it.hidden = !hit; if (hit) n++; });
      if (gc) gc.textContent = q ? n + (n === 1 ? " term matches" : " terms match") : "";
    };
    gf.addEventListener("input", runG);
  }

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
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and an Indiana Insurance Appraiser team member will reach out, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@indianainsuranceappraiser.com\">info@indianainsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding helper ---------- */
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

  /* 1. Claim gap & net recovery */
  var gapCalc = function (ins, own, land, feeType, fee, umpHalf) {
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var cost = (feeType === "pct" ? gain * fee / 100 : fee) + umpHalf;
    return { gap: gap, award: award, gain: gain, cost: cost, net: gain - cost };
  };
  window.IIA_gapCalc = gapCalc;
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = $("[name=fee]", r) ? num($("[name=fee]", r)) : 0;
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var umpHalf = useUmp ? num($("[name=umpire]", r)) / 2 : 0;
    var c = gapCalc(ins, own, land, feeType, fee, umpHalf);
    set("[data-o=gap]", money(c.gap), r);
    set("[data-o=award]", money(c.award), r);
    set("[data-o=gain]", money(c.gain), r);
    set("[data-o=cost]", money(c.cost), r);
    set("[data-o=net]", money(c.net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(c.gap / ins * 100) + "%" : "—", r);
    [30, 55, 80].forEach(function (s) { set("[data-o=s" + s + "]", money(gapCalc(ins, own, s / 100, feeType, fee, umpHalf).net), r); });
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, c.award, 1), s = stack.children;
      s[0].style.width = (ins / total * 100) + "%";
      s[1].style.width = (Math.max(0, c.net) / total * 100) + "%";
      s[2].style.width = (Math.max(0, Math.min(c.cost, c.gain)) / total * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (c.gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal values a covered loss; with no gap, there’s nothing to appraise.";
      else if ($("[name=fee]", r) && c.net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (c.gap / ins < 0.1 && c.gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready when you call.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0;
    var cap = num($("[name=cap]", r)) / 100 || 0.8;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), total = Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(nonrec ? 0 : total - first), r);
    set("[data-o=total]", money(nonrec ? first : total), r);
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
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r)), carrier = num($("[name=carrier]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=vs]", carrier ? ((order - carrier >= 0 ? "+" : "−") + Math.abs(order - carrier).toFixed(2) + " sq (" + Math.round((order - carrier) / carrier * 100) + "%)") : "—", r);
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12, estimating software usually adds a steep-roof charge. Check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 many estimates begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge typically isn’t expected.";
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.min(loss, pd) - Math.min(loss, flat)), r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payouts." : loss <= pd ? "This loss falls entirely within the percentage deductible, so no claim payment would be owed under it." : "The loss exceeds the percentage deductible by " + money(loss - pd) + ".", r);
    var bar = $(".stack", r);
    if (bar && loss > 0) {
      var a = Math.min(pd, loss) / loss * 100;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (100 - a) + "%";
    }
  });

  /* 5. Claim timeline builder + .ics export */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><strong>Pick your date of loss</strong><br><span>Your milestones will appear here.</span></li>"; plan = []; return; }
    var base = new Date(d0 + "T12:00:00");
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-set target." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarps, board-up and water extraction protect the property and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies allow 60 days from the carrier’s request. Count from the date on the request letter." },
      { d: add(num($("[name=rcd]", r))), t: "Recoverable depreciation window closes", n: "Policies set a deadline to finish repairs and claim the holdback. Confirm the number of days in your policy." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Many Indiana property policies limit lawsuits to two years from the loss. Talk to an attorney well before this date." }
    ].sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + '<em>' + badge + '</em></b><strong>' + p.t + '</strong><br><span>' + p.n + '</span></li>';
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var dl = $("[name=dol]"); if (dl) dl.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,"); };
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Indiana Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:iia-" + ds(p.d) + "-" + i + "@indianainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "indiana-claim-timeline.ics";
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
        var yes = $(".yes", li).getAttribute("aria-pressed") === "true";
        var no = $(".no", li).getAttribute("aria-pressed") === "true";
        if (yes) got += w;
        if (yes || no) answered++;
        if (no) todo.push(li.getAttribute("data-fix"));
      });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? pct : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.setAttribute("class", pct >= 75 ? "arc-good" : pct >= 45 ? "arc-mid" : "arc-low"); }
      var verdict = !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the documentation a panel expects. The next step is a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before demanding appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.";
      set("[data-o=verdict]", verdict, r);
      var ul = $("[data-o=todo]", r);
      if (ul) ul.innerHTML = todo.length ? todo.map(function (t) { return "<li>" + t + "</li>"; }).join("") : "<li>Nothing flagged yet.</li>";
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

  /* 7. Roof snow load estimator */
  tool("snow", function (r) {
    var area = num($("[name=area]", r)), depth = num($("[name=depth]", r)), dens = num($("[name=density]", r)), ice = num($("[name=ice]", r)), ref = num($("[name=ref]", r));
    var snowPsf = depth / 12 * dens, icePsf = ice / 12 * 57, psf = snowPsf + icePsf, lbs = psf * area;
    set("[data-o=psf]", psf.toFixed(1) + " lb/sq ft", r);
    set("[data-o=snowpsf]", snowPsf.toFixed(1) + " lb/sq ft", r);
    set("[data-o=icepsf]", icePsf.toFixed(1) + " lb/sq ft", r);
    set("[data-o=lbs]", Math.round(lbs).toLocaleString("en-US") + " lb (" + (lbs / 2000).toFixed(1) + " tons)", r);
    var ratio = ref > 0 ? psf / ref : 0;
    set("[data-o=ratio]", ref > 0 ? Math.round(ratio * 100) + "%" : "—", r);
    var m = $("[data-o=meter]", r);
    if (m) { m.style.width = Math.min(100, ratio * 100) + "%"; m.className = ratio >= 1 ? "hot" : ratio >= 0.75 ? "warm" : ""; }
    set("[data-o=smsg]", !area || !depth ? "Enter roof area and snow depth to estimate the load." : ratio >= 1 ? "This estimate meets or exceeds the reference load you entered. Watch for sagging, cracking or sticking doors, keep people clear and consider professional snow removal." : ratio >= 0.75 ? "This is a meaningful share of the reference load. Drifts can concentrate weight on lower roofs and valleys." : "Within the reference load you entered, though drifts and ice can still concentrate weight in spots.", r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
