/* Oklahoma Insurance Appraiser — site script (nav, effects, forms, claim tools). No dependencies. */
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

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    body.classList.add("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-close", drawer); if (c) c.focus(); }, 60);
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1100) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- scroll effects: header, progress, back-to-top ring, parallax, stepper ---------- */
  var head = $(".head"), bar = $(".progress"), toTop = $(".to-top"), ring = $(".to-top .ring circle");
  var px = $$("[data-parallax]"), stepper = $(".stepper");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight, p = h > 0 ? y / h : 0;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + p + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (ring) ring.style.strokeDashoffset = (150.8 * (1 - p)).toFixed(1);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0)";
    });
    if (stepper) {
      var sr = stepper.getBoundingClientRect(), mid = window.innerHeight * 0.65, fill = $(".fill", stepper);
      var vertical = window.innerWidth <= 1100;
      var pct = Math.max(0, Math.min(1, (mid - sr.top) / (sr.height || 1)));
      if (!vertical) pct = Math.max(0, Math.min(1, (mid - sr.top + 200) / 400));
      if (fill) { if (vertical) { fill.style.width = ""; fill.style.height = (pct * 100) + "%"; } else { fill.style.height = ""; fill.style.width = (pct * 100) + "%"; } }
      var steps = $$("li", stepper);
      steps.forEach(function (s, i) { s.classList.toggle("on", vertical ? s.getBoundingClientRect().top < mid : pct >= (i / Math.max(1, steps.length - 1)) - 0.001 && pct > 0); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), suf = el.getAttribute("data-suffix") || "", t0 = null, dur = 1500;
    if (reduce) { el.textContent = end + suf; return; }
    var step = function (t) { if (!t0) t0 = t; var q = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - q, 3))) + suf; if (q < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); if (el.hasAttribute("data-count")) count(el); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv, .rv-wipe", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.09 + "s"); }); });
  var targets = $$(".rv, .rv-wipe, [data-counters]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.12, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(reveal); }

  /* ---------- expanding region panels ---------- */
  $$("[data-panels]").forEach(function (wrap) {
    var ps = $$(".panel", wrap);
    var pick = function (p) { ps.forEach(function (o) { var on = o === p; o.classList.toggle("on", on); o.setAttribute("aria-expanded", on ? "true" : "false"); }); };
    ps.forEach(function (p) {
      p.addEventListener("click", function () { pick(p); });
      p.addEventListener("focus", function () { pick(p); });
      p.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches && window.innerWidth > 1100) pick(p); });
    });
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0;
    $$(".glossary dt").forEach(function (dt) {
      var dd = dt.nextElementSibling;
      var hit = !q || (dt.textContent + " " + dd.textContent).toLowerCase().indexOf(q) > -1;
      dt.hidden = dd.hidden = !hit;
      if (hit) shown++;
    });
    var none = $(".glossary-none"); if (none) none.hidden = shown > 0;
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please fill in the required fields and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you — we received your claim details. Someone from Oklahoma Insurance Appraiser will get back to you, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "Your message didn’t go through. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@oklahomainsuranceappraiser.com\">info@oklahomainsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding helper ---------- */
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
  var bars = function (stack, parts) { if (!stack) return; var s = stack.children; parts.forEach(function (w, i) { if (s[i]) s[i].style.width = Math.max(0, Math.min(100, w)) + "%"; }); };

  /* 1. Claim gap & fee estimator (also the home mini check) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.55;
    var ft = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), hrs = num($("[name=hours]", r));
    var hoursBox = $("[data-hours]", r); if (hoursBox) hoursBox.hidden = ft !== "hourly";
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var cost = ft === "pct" ? gain * fee / 100 : ft === "hourly" ? fee * hrs : fee;
    if (!$("[name=fee]", r)) cost = 0;
    if (useUmp) cost += num($("[name=umpire]", r)) / 2;
    var net = gain - cost;
    set("[data-o=gap]", money(gap), r); set("[data-o=award]", money(award), r); set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r); set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=ratio]", cost > 0 ? (net / cost).toFixed(1) + " : 1" : "—", r);
    var total = Math.max(own, award, 1);
    bars($(".stack", r), [ins / total * 100, Math.max(0, net) / total * 100, Math.min(cost, gain) / total * 100]);
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the amount in dispute.";
      else if (gap <= 0) t = "Your figure isn’t higher than the carrier’s. Appraisal settles how much a covered loss costs — with no gap, there’s nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these inputs, appraisal costs could swallow the whole increase. A line-by-line estimate review or a documented supplement is usually the better first move.";
      else if (cost > 0 && net / cost < 1.5) t = "You’d likely come out ahead, but fees would take a large share of the increase. Test lower fee options or a stronger-documented scenario before committing.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The amount in dispute is large enough that appraisal may be worth discussing. Have both estimates and your photos ready when you call.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
  tool("dep", function (r) {
    var rows = $$("tbody tr", r), rcv = 0, dep = 0;
    var cap = (num($("[name=cap]", r)) || 80) / 100;
    var labor = num($("[name=labor]", r)) / 100;
    var matOnly = $("[name=nolabor]", r) && $("[name=nolabor]", r).checked;
    rows.forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var base = matOnly ? c * (1 - labor) : c;
      var d = Math.min(cap, age / life) * base;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), full = Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r); set("[data-o=dep]", money(dep), r); set("[data-o=acv]", money(acv), r);
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
    var price = num($("[name=price]", r)), stories = num($("[name=stories]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=edge]", mode === "dims" ? Math.round(2 * (L + 2 * oh) + 2 * (W + 2 * oh) * mult) + " lf (gable estimate)" : "—", r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var msg = pitch >= 8 ? "At " + pitch + "/12, estimating software commonly adds a steep-roof charge — check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 some carriers start applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.";
    if (stories >= 2) msg += " Two-story eaves often carry a separate high-roof charge as well.";
    set("[data-o=steep]", msg, r);
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=below]", loss > 0 && loss <= pd ? "This loss sits entirely inside the percentage deductible — the policy would pay nothing toward it." : loss > 0 ? "The loss is " + money(loss - pd) + " above your percentage deductible." : "Enter an estimated loss to compare payments.", r);
    var tb = $("[data-o=compare]", r);
    if (tb) tb.innerHTML = [1, 2, 5].map(function (p) { var d = covA * p / 100; return '<tr' + (p === pct ? ' class="cur"' : '') + '><td>' + p + '%</td><td class="mono">' + money(d) + '</td><td class="mono">' + money(Math.max(0, loss - d)) + '</td></tr>'; }).join("");
    if (loss > 0) { var a = Math.min(pd, loss) / loss * 100; bars($(".stack", r), [a, 100 - a]); }
  });

  /* 5. Claim timeline planner */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, rq = $("[name=req]", r) ? $("[name=req]", r).value : "";
    var list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Choose your date of loss</b><span>Your milestones will appear here.</span></li>"; plan = []; return; }
    var base = new Date(d0 + "T12:00:00"), reqBase = rq ? new Date(rq + "T12:00:00") : null;
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(base, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies call for prompt notice. Report as soon as you can — this is a self-set target." },
      { d: add(base, num($("[name=mitig]", r))), t: "Temporary repairs done, receipts saved", n: "Tarps, board-up and water extraction protect the property and the claim." },
      { d: add(base, num($("[name=appr]", r))), t: "Decide on supplement vs. appraisal", n: "A checkpoint so a disagreement doesn’t drift. Compare estimates and run the gap estimator." },
      { d: add(base, num($("[name=rcd]", r))), t: "Recoverable depreciation window", n: "Confirm the repair-completion window in your policy and send invoices before it closes." },
      { d: add(base, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Check the ‘Suit Against Us’ condition. Speak with an Oklahoma attorney well before this date." }
    ];
    if (reqBase) plan.push({ d: add(reqBase, num($("[name=pol]", r))), t: "Sworn proof of loss due", n: "Counted from the date of the carrier’s written request." });
    plan.sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + '<em>' + badge + '</em></b><strong>' + p.t + '</strong><br><span>' + p.n + '</span></li>';
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) return;
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Oklahoma Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:oia-" + ds(p.d) + "-" + i + "@oklahomainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness check (letter grade) */
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
      var grade = pct >= 90 ? "A" : pct >= 75 ? "B" : pct >= 55 ? "C" : pct >= 35 ? "D" : "F";
      set("[data-o=score]", answered ? pct : "–", r);
      set("[data-o=grade]", answered ? "Grade " + grade : "", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { arc.style.strokeDashoffset = 251.3 - 251.3 * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1d5c42" : pct >= 55 ? "#d98a3a" : "#c4552f"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your grade." : pct >= 75 ? "Solid file. You have what an appraisal panel expects — the next step is a professional look at the dollar gap." : pct >= 55 ? "Close, but not there yet. Finish the items below before demanding appraisal; each missing piece weakens your figure." : "Not ready. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) ul.innerHTML = todo.length ? todo.map(function (t) { return "<li>" + t + "</li>"; }).join("") : "<li>Nothing flagged yet.</li>";
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

  /* 7. Roof payment schedule (illustrative schedules) */
  var schedPct = function (s, age) {
    if (s === "a") return age <= 3 ? 100 : Math.max(30, 100 - 5 * (age - 3));
    if (s === "b") return age <= 1 ? 100 : Math.max(25, 100 - 6 * (age - 1));
    if (s === "c") return age < 5 ? 100 : age < 10 ? 80 : age < 15 ? 60 : 40;
    return null;
  };
  tool("sched", function (r) {
    var rcv = num($("[name=rcv]", r)), age = Math.max(0, num($("[name=age]", r))), s = $("[name=sched]", r).value;
    var box = $("[data-custom]", r); if (box) box.hidden = s !== "custom";
    var pct = s === "custom" ? Math.max(0, Math.min(100, num($("[name=pct]", r)))) : schedPct(s, age);
    var val = rcv * pct / 100;
    var dsel = num($("[name=ded]", r)), ded = dsel > 0 ? num($("[name=cova]", r)) * dsel / 100 : num($("[name=flat]", r));
    var pay = Math.max(0, val - ded), dedApplied = Math.min(ded, val), cut = rcv - val;
    set("[data-o=pct]", pct + "%", r); set("[data-o=val]", money(val), r); set("[data-o=ded]", money(dedApplied), r);
    set("[data-o=cut]", money(cut), r); set("[data-o=pay]", money(pay), r); set("[data-o=share]", money(rcv - pay), r);
    if (rcv > 0) bars($(".stack", r), [pay / rcv * 100, dedApplied / rcv * 100, cut / rcv * 100]);
    set("[data-o=msg]", !rcv ? "Enter the roof’s replacement cost to begin." : pay <= 0 ? "At this age and deductible, the scheduled roof value doesn’t clear the deductible — the roof portion of the claim would pay nothing." : "Illustrative only. Your endorsement’s own table controls, and appraisal decides the replacement cost the percentage is applied to.", r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
