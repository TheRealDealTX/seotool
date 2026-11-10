/* West Virginia Insurance Appraiser — site script (nav, effects, forms, claim tools). No dependencies.
   Every tool runs locally; nothing typed into a tool is sent or stored. */
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
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function (except) {
    $$(".menu .has-drop.open").forEach(function (li) {
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
    li.addEventListener("mouseleave", function () { if (window.matchMedia("(hover: hover)").matches) t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim"), lastFocus = null;
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    lastFocus = document.activeElement;
    scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!isOpen()) scrim.hidden = true; }, 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", function () { isOpen() ? closeDrawer() : openDrawer(); });
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, back-to-top, parallax, timeline fill ---------- */
  var head = $(".head"), toTop = $(".to-top"), px = $$("[data-parallax]"), tline = $("[data-timeline]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -k).toFixed(1) + "px,0)";
    });
    if (tline) {
      var tr = tline.getBoundingClientRect();
      var pct = clamp((vh * 0.85 - tr.top) / (tr.height + vh * 0.35), 0, 1);
      tline.style.setProperty("--fill", (reduce ? 1 : pct).toFixed(3));
      var steps = $$(".tl-step", tline);
      steps.forEach(function (s, i) { s.classList.toggle("on", reduce || pct >= (i + 0.5) / steps.length); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); var m = $("#main"); if (m) { m.setAttribute("tabindex", "-1"); m.focus({ preventScroll: true }); } });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.12, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(reveal); }

  /* ---------- storm carousel ---------- */
  $$("[data-carousel]").forEach(function (track) {
    var sec = track.closest("section");
    $$("[data-car]", sec).forEach(function (b) {
      b.addEventListener("click", function () {
        var card = track.querySelector("li");
        var w = card ? card.getBoundingClientRect().width + 20 : 320;
        track.scrollBy({ left: w * parseInt(b.getAttribute("data-car"), 10), behavior: reduce ? "auto" : "smooth" });
      });
    });
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".glossary .term").forEach(function (t) {
      var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1;
      t.hidden = !hit; if (hit) n++;
    });
    var c = $("[data-gloss-count]"); if (c) c.textContent = n + (n === 1 ? " term" : " terms") + (q ? " match" : "");
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      $$(".bad", form).forEach(function (f) { f.classList.remove("bad"); });
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { bad.forEach(function (f) { f.classList.add("bad"); }); msg.textContent = "Please fill in the highlighted fields and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you — your details arrived. Someone from West Virginia Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "The form couldn’t be sent just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@westvirginiainsuranceappraiser.com\">info@westvirginiainsuranceappraiser.com</a>."; msg.classList.add("err"); })
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
  var bars = function (stack, parts) {
    if (!stack) return;
    var tot = parts.reduce(function (a, b) { return a + Math.max(0, b); }, 0) || 1;
    Array.prototype.forEach.call(stack.children, function (s, i) { s.style.width = (Math.max(0, parts[i] || 0) / tot * 100) + "%"; });
  };

  /* 1. Claim gap & fee estimator (and the home mini check) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var ft = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), hrs = num($("[name=hours]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    $$("[data-show]", r).forEach(function (el) { el.hidden = el.getAttribute("data-show") !== ft; });
    var gap = Math.max(0, own - ins);
    var costAt = function (gain) { var c = ft === "pct" ? gain * fee / 100 : ft === "hourly" ? fee * hrs : fee; return c + (useUmp ? ump / 2 : 0); };
    var netAt = function (l) { var g = gap * clamp(l, 0, 1); return g - costAt(g); };
    var gain = gap * land, award = ins + gain, cost = costAt(gain), net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=s-low]", money(netAt(land - 0.30)), r);
    set("[data-o=s-mid]", money(net), r);
    set("[data-o=s-high]", money(netAt(land + 0.25)), r);
    // break-even: smallest landing share where net >= 0
    var be = "—";
    if (gap > 0) {
      if (ft === "pct") be = fee >= 100 ? "never" : (useUmp && ump > 0 ? Math.ceil((ump / 2) / (gap * (1 - fee / 100)) * 100) + "%" : "0%");
      else { var fixed = costAt(0); be = fixed / gap > 1 ? "above 100%" : Math.ceil(fixed / gap * 100) + "%"; }
    }
    set("[data-o=be]", be, r);
    bars($(".stack", r), [ins, Math.max(0, net), Math.min(cost, gain)]);
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your estimate isn’t higher than the insurer’s. Appraisal settles how much a covered loss costs — with no gap, there is nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these numbers, appraisal costs could swallow the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready when you call.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV & holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0, cap = (num($("[name=cap]", r)) || 80) / 100;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      set("[data-o=row]", money(c - d), tr);
    });
    var ded = num($("[name=deduct]", r)), nonrec = $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), total = nonrec ? first : Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(total - first), r);
    set("[data-o=total]", money(total), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
    var s = $("[name=start]", r).value, days = num($("[name=days]", r));
    var by = "—";
    if (nonrec) by = "Not applicable (ACV only)";
    else if (s && days) { var d0 = new Date(s + "T12:00:00"); d0.setDate(d0.getDate() + days); by = d0.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }); }
    else if (days) by = days + " days after the first check";
    set("[data-o=by]", by, r);
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

  /* 3. Roof squares & pitch */
  tool("roof", function (r) {
    var mode = ($("[name=mode]:checked", r) || {}).value || "dims";
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
    var msg = pitch >= 8 ? "At " + pitch + "/12 estimating software normally adds a steep-roof labor charge. Check that the insurer’s estimate includes it." : pitch >= 7 ? "At 7/12 some estimates begin to add steep charges. Confirm how yours treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.";
    if (carrier && order - carrier > 1.5) msg += " Your count is well above the carrier’s — look for a missing slope, porch roof or wrong pitch.";
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
    set("[data-o=below]", loss > 0 && loss <= pd ? "This loss falls entirely inside the percentage deductible, so nothing would be paid under it." : loss > 0 ? "The loss exceeds the percentage deductible by " + money(loss - pd) + "." : "Enter an estimated loss to compare payouts.", r);
    bars($(".stack", r), [Math.min(pd, loss), Math.max(0, loss - pd)]);
    var lad = $("[data-o=ladder]", r);
    if (lad) lad.innerHTML = [0.5, 1, 2, 3, 5].map(function (p) {
      var d = covA * p / 100;
      return "<tr" + (p === pct ? ' class="on"' : "") + "><td>" + p + "% (" + money(d) + ")</td><td>" + money(Math.min(loss, d)) + "</td><td>" + money(Math.max(0, loss - d)) + "</td></tr>";
    }).join("") + "<tr><td>Flat " + money(flat) + "</td><td>" + money(Math.min(loss, flat)) + "</td><td>" + money(Math.max(0, loss - flat)) + "</td></tr>";
  });

  /* 5. Claim timeline planner + .ics export */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Choose your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies ask for prompt notice. Report as soon as you can; this is a self-set target." },
      { d: add(num($("[name=mitig]", r))), t: "Temporary repairs done, receipts saved", n: "Tarps, drying and board-up protect the property and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often counted from the insurer’s written request. Check the date on its letter." },
      { d: add(num($("[name=pol]", r)) + num($("[name=appr]", r))), t: "Appraiser named (if appraisal is demanded around the proof-of-loss date)", n: "Many appraisal clauses allow a set number of days after a written demand. Recalculate from the actual demand date." },
      { d: add(num($("[name=rcd]", r))), t: "Repairs finished to recover depreciation", n: "Policies set a window to complete repairs and claim the holdback. Ask in writing before it ends if you need more time." },
      { d: add(num($("[name=suit]", r))), t: "Suit-limitation date in the policy", n: "Confirm your policy’s wording and talk to a West Virginia attorney well before this date." }
    ].sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + "<em>" + badge + "</em></b><strong>" + p.t + "</strong><span>" + p.n + "</span></li>";
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var dol = $('[name=dol]'); if (dol) dol.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//West Virginia Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:wvia-" + ds(p.d) + "-" + i + "@westvirginiainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness scorecard */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#15370d" : pct >= 45 ? "#c9952b" : "#b8336a"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects — the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before invoking appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks a binding award on an incomplete scope. Work through the list below first.", r);
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

  /* 7. Mine subsidence limit */
  tool("mine", function (r) {
    var covA = num($("[name=cova]", r)), cap = num($("[name=cap]", r)), dpct = num($("[name=dpct]", r));
    var dmin = num($("[name=dmin]", r)), dmax = num($("[name=dmax]", r)), rep = num($("[name=repair]", r));
    var has = $("[name=has]", r).checked;
    var lim = has ? Math.min(covA || Infinity, cap || Infinity) : 0;
    if (!isFinite(lim)) lim = 0;
    var ded = has ? lim * dpct / 100 : 0;
    if (has && dmax > 0) ded = Math.min(ded, dmax);
    if (has && dmin > 0) ded = Math.max(ded, dmin);
    var pay = has ? Math.max(0, Math.min(rep - ded, lim)) : 0;
    set("[data-o=lim]", money(lim), r);
    set("[data-o=ded]", money(ded), r);
    set("[data-o=pay]", money(pay), r);
    set("[data-o=over]", money(Math.max(0, rep - ded - lim)), r);
    set("[data-o=share]", rep > 0 ? Math.round(pay / rep * 100) + "%" : "—", r);
    bars($(".stack", r), [pay, Math.max(0, rep - pay)]);
    set("[data-o=note]", !has ? "Without the endorsement, a standard policy’s earth-movement exclusion usually applies. Check your declarations page." : rep > lim + ded ? "The repair estimate exceeds the subsidence limit. An accurate amount of loss still matters if other coverages may apply." : "The estimated repair fits within the subsidence limit after the deductible.", r);
  });
})();
