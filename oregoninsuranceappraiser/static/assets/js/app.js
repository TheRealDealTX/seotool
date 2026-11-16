/* Oregon Insurance Appraiser — site script (nav, drawer, motion, forms, claim tools). No dependencies.
   Every tool runs in the browser; nothing is stored or sent. */
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
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 160); });
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1040) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- header, progress, back-to-top, parallax, trail fill ---------- */
  var head = $(".head"), bar = $(".progress"), toTop = $(".to-top");
  var px = $$("[data-parallax]"), trailEl = $("[data-trail]"), rail = $("[data-rail]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight, h = document.documentElement.scrollHeight - vh;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? y / h : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -k).toFixed(1) + "px,0)";
    });
    if (trailEl) {
      var tr = trailEl.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (vh * 0.75 - tr.top) / (tr.height + vh * 0.25)));
      trailEl.style.setProperty("--p", p.toFixed(3));
      var steps = $$(".tstep", trailEl);
      steps.forEach(function (s, i) { s.classList.toggle("on", p >= (i + 0.5) / steps.length || s.getBoundingClientRect().top < vh * 0.45); });
    }
    if (rail) {
      var art = rail.parentElement.getBoundingClientRect();
      var q = Math.max(0, Math.min(1, (vh * 0.3 - art.top) / Math.max(1, art.height - vh * 0.5)));
      rail.style.setProperty("--p", q.toFixed(3));
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 8) * 0.07 + "s"); }); });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(reveal); }

  /* ---------- region strip buttons ---------- */
  var track = $("[data-strip-track]");
  $$("[data-strip]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!track) return;
      var card = track.firstElementChild, w = card ? card.getBoundingClientRect().width + 20 : 340;
      track.scrollBy({ left: w * parseInt(b.getAttribute("data-strip"), 10), behavior: reduce ? "auto" : "smooth" });
    });
  });

  /* ---------- glossary search ---------- */
  var gf = $("#gloss-filter"), gc = $("[data-gloss-count]");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".glossary dt").forEach(function (dt) {
      var dd = dt.nextElementSibling;
      var hit = !q || (dt.textContent + " " + dd.textContent).toLowerCase().indexOf(q) > -1;
      dt.hidden = dd.hidden = !hit;
      if (hit) n++;
    });
    if (gc) gc.textContent = n + (n === 1 ? " term" : " terms") + (q ? " match “" + gf.value.trim() + "”" : "");
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please fill in the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thanks, your claim details arrived. Someone from Oregon Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@oregoninsuranceappraiser.com\">info@oregoninsuranceappraiser.com</a>."; msg.classList.add("err"); })
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

  /* 1. Appraisal payoff estimator (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.55;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var netAt = function (f) { var g = gap * f, c = (feeType === "pct" ? g * fee / 100 : fee) + (useUmp ? ump / 2 : 0); return { gain: g, cost: c, net: g - c }; };
    var cur = netAt(land), award = ins + cur.gain;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(cur.gain), r);
    set("[data-o=cost]", money(cur.cost), r);
    set("[data-o=net]", money(cur.net), r);
    set("[data-o=lo]", money(netAt(0.3).net), r);
    set("[data-o=mid]", money(netAt(0.55).net), r);
    set("[data-o=hi]", money(netAt(0.8).net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, award, 1), s = stack.children;
      s[0].style.width = (ins / total * 100) + "%";
      s[1].style.width = (Math.max(0, cur.net) / total * 100) + "%";
      s[2].style.width = (Math.min(cur.cost, cur.gain) / total * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your number isn’t higher than the insurer’s. Appraisal settles how much a covered loss costs; with no gap, there’s nothing to appraise.";
      else if ($("[name=fee]", r) && cur.net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready when you call.";
      m.textContent = t;
    }
  });

  /* 2. Depreciation & holdback tracker */
  tool("dep", function (r) {
    var rcv = 0, dep = 0;
    var cap = num($("[name=cap]", r)) / 100 || 0.8;
    var labor = Math.min(100, Math.max(0, num($("[name=labor]", r)))) / 100;
    var depLabor = !$("[name=deplabor]", r) || $("[name=deplabor]", r).value === "yes";
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var base = depLabor ? c : c * (1 - labor);
      var d = Math.min(cap, age / life) * base;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
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
      }
      var x = e.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof pitch & squares converter */
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
    set("[data-o=deg]", (Math.atan(pitch / 12) * 180 / Math.PI).toFixed(1) + "°", r);
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=cmp]", carrier ? ((order - carrier >= 0 ? "+" : "−") + Math.abs(order - carrier).toFixed(2) + " sq (" + Math.round((order - carrier) / carrier * 100) + "%)") : "—", r);
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge. Check that the insurer’s estimate includes it." : pitch >= 7 ? "At 7/12 some insurers start applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.";
  });

  /* 4. Percentage deductible checker */
  tool("deduct", function (r) {
    var type = $("[name=dtype]", r) ? $("[name=dtype]", r).value : "wind";
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.min(pd, loss) - Math.min(flat, loss)), r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payouts." : loss <= pd ? "This loss falls entirely within the percentage deductible, so that deductible would leave nothing payable." : "The loss exceeds the percentage deductible by " + money(loss - pd) + ".", r);
    set("[data-o=note]", type === "eq" ? "Earthquake deductibles are commonly 10% or more and may apply separately to each coverage. Read your endorsement." : "Wind or hail percentage deductibles usually apply only to losses from those perils. Check the declarations page.", r);
    var st = $(".stack", r);
    if (st && loss > 0) { var a = Math.min(pd, loss) / loss * 100; st.children[0].style.width = a + "%"; st.children[1].style.width = (100 - a) + "%"; }
  });
  $$('[data-tool="deduct"] [name=dtype]').forEach(function (s) {
    s.addEventListener("change", function () { var p = s.closest("[data-tool]").querySelector("[name=pct]"); p.value = s.value === "eq" ? "10" : "2"; p.dispatchEvent(new Event("change", { bubbles: true })); });
  });

  /* 5. Claim calendar builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, dem = $("[name=dem]", r) ? $("[name=dem]", r).value : "";
    var list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; plan = []; return; }
    var mk = function (s) { return new Date(s + "T12:00:00"); };
    var base = mk(d0), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(base, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-set target." },
      { d: add(base, num($("[name=mitig]", r))), t: "Finish temporary repairs and keep receipts", n: "Tarps, drying and board-up protect the property and are usually reimbursable." },
      { d: add(base, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often due a set number of days after the insurer asks. Count from the date in its letter." },
      { d: add(base, num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Replacement cost policies set a deadline to finish repairs and claim the holdback. Confirm yours." },
      { d: add(base, num($("[name=suit]", r))), t: "Policy deadline to file suit", n: "Oregon property policies commonly allow two years from the loss. Talk to an attorney well before this date." }
    ];
    if (dem) plan.push({ d: add(mk(dem), num($("[name=nameapp]", r))), t: "Name your appraiser", n: "Many appraisal clauses give each side a set number of days after a written demand to name an appraiser." });
    plan.sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + "<em>" + badge + "</em></b><strong>" + p.t + "</strong><br><span>" + p.n + "</span></li>";
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var dol = btn.closest("[data-tool]").querySelector("[name=dol]"); if (dol) dol.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Oregon Insurance Appraiser//Claim Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:oia-" + ds(p.d) + "-" + i + "@oregoninsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "oregon-claim-calendar.ics";
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1f7a52" : pct >= 45 ? "#002a86" : "#e4572e"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list first.", r);
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

  /* 7. Wildfire contents estimator */
  tool("contents", function (r) {
    var lvl = num($("[name=lvl]", r)) || 1, yrs = num($("[name=yrs]", r));
    var covA = num($("[name=cova]", r)), covC = num($("[name=covc]", r)), total = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var ins = $$("input", tr);
      total += num(ins[0]) * num(ins[1]);
    });
    var rcv = total * lvl;
    var dpct = Math.min(0.6, Math.max(0, yrs) * 0.06);
    var acv = rcv * (1 - dpct);
    var short = Math.max(0, rcv - covC);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=short]", money(short), r);
    set("[data-o=cpct]", covA ? Math.round(covC / covA * 100) + "%" : "—", r);
    set("[data-o=use]", covC ? Math.round(rcv / covC * 100) + "%" : "—", r);
    set("[data-o=dpct]", Math.round(dpct * 100) + "%", r);
    set("[data-o=msg]", !rcv ? "Enter at least one room to see an estimate." : short > 0 ? "This rough estimate is above your contents limit by " + money(short) + ". Payment is capped by the limit, so a careful inventory still matters for depreciation and any extended coverage." : "This rough estimate fits within your contents limit, with " + money(covC - rcv) + " to spare. A thorough inventory helps make sure every item is counted.", r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
