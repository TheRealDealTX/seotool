/* Nevada Insurance Appraiser — site script: nav, drawer, effects, lead forms, claim tools. No dependencies.
   Every tool computes in the browser; nothing typed into a tool is stored or sent. */
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
  var closeSubs = function (except) {
    $$(".has-sub.open").forEach(function (li) { if (li === except) return; li.classList.remove("open"); $(".sub-btn", li).setAttribute("aria-expanded", "false"); });
  };
  $$(".has-sub").forEach(function (li) {
    var btn = $(".sub-btn", li), t;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !li.classList.contains("open");
      closeSubs(li);
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    var hover = function () { return window.matchMedia("(hover: hover)").matches; };
    li.addEventListener("mouseenter", function () { if (!hover()) return; clearTimeout(t); closeSubs(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover()) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".has-sub")) closeSubs(); });

  /* ---------- mobile drawer (outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".drawer-scrim"), lastFocus = null;
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    lastFocus = document.activeElement;
    scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    document.documentElement.classList.add("lock"); body.classList.add("lock");
    requestAnimationFrame(function () { body.classList.add("drawer-open"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!isOpen()) return;
    body.classList.remove("drawer-open");
    document.documentElement.classList.remove("lock"); body.classList.remove("lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!isOpen()) scrim.hidden = true; }, reduce ? 0 : 300);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (drawer && burger && scrim) {
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
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeSubs(); closeDrawer(); } });

  /* ---------- header, back-to-top, parallax ---------- */
  var head = $(".head"), toTop = $(".to-top"), px = $$("[data-parallax]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -0.15).toFixed(1) + "px,0)";
    });
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  var targets = $$(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
    var cio = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { $$("[data-count]", en.target).forEach(count); cio.unobserve(en.target); } }); }, { threshold: 0.4 });
    $$(".counters").forEach(function (el) { cio.observe(el); });
  } else { targets.forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- region tabs ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
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
        var k = e.key;
        if (k === "ArrowRight" || k === "ArrowDown") { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (k === "ArrowLeft" || k === "ArrowUp") { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
        if (k === "Home") { e.preventDefault(); select(0, true); }
        if (k === "End") { e.preventDefault(); select(tabs.length - 1, true); }
      });
    });
  });

  /* ---------- glossary search ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".glossary .term").forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
    set("[data-gloss-count]", n + (n === 1 ? " term" : " terms"));
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      var em = $("[type=email]", form);
      if (em && em.value && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value)) bad.push(em);
      $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      if (bad.length) { bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); }); msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thanks. Your claim details were received, and someone from Nevada Insurance Appraiser will reach out, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error("send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@nevadainsuranceappraiser.com\">info@nevadainsuranceappraiser.com</a>."; msg.classList.add("err"); })
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

  /* 1. Claim gap & fee estimator (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins), gain = gap * land, award = ins + gain;
    var half = useUmp ? ump / 2 : 0;
    var cost = (feeType === "pct" ? gain * fee / 100 : fee) + half;
    var net = gain - cost;
    // break-even: the gain at which net = 0, as a share of the gap
    var beGain = feeType === "pct" ? (fee >= 100 ? Infinity : half / (1 - fee / 100)) : fee + half;
    var be = gap > 0 ? beGain / gap : Infinity;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=breakeven]", !isFinite(be) ? "not reachable" : be > 1 ? "more than 100% of gap" : Math.ceil(be * 100) + "% of gap", r);
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, award, 1), s = stack.children;
      s[0].style.width = (ins / total * 100) + "%";
      s[1].style.width = (Math.max(0, net) / total * 100) + "%";
      s[2].style.width = (Math.min(cost, Math.max(gain, 0)) / total * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your number isn’t higher than the insurer’s. Appraisal resolves how much a covered loss costs; with no gap, there is nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these inputs, appraisal costs would absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else if ($("[name=fee]", r) && be > 0.7) t = "Appraisal only pays off if the award captures most of the gap. Make sure every line item is well documented before deciding.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready before you call.";
      m.textContent = t;
    }
  });

  /* 2. Depreciation recovery */
  tool("dep", function (r) {
    var rcv = 0, dep = 0, cap = (num($("[name=cap]", r)) || 80) / 100;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, Math.max(0, age) / life) * c;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r)), nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), full = Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(nonrec ? 0 : Math.max(0, full - first)), r);
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

  /* 3. Roof squares & tile */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var type = $("[name=rtype]", r).value, isTile = type !== "shingle";
    $$("[data-rt]", r).forEach(function (el) { el.hidden = !isTile; });
    var tpsEl = $("[name=tps]", r);
    if (r._lastType !== type) { if (type === "clay" && num(tpsEl) === 90) tpsEl.value = 100; if (type === "tile" && num(tpsEl) === 100) tpsEl.value = 90; r._lastType = type; }
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", order.toFixed(2), r);
    if (isTile) {
      var tps = num(tpsEl), field = Math.round(sq * tps), broken = num($("[name=broken]", r));
      set("[data-o=unitlabel]", "Field tiles on the roof (approx.)", r);
      set("[data-o=units]", field.toLocaleString("en-US"), r);
      set("[data-o=brokenpct]", field > 0 ? (broken / field * 100).toFixed(1) + "%" : "—", r);
    } else {
      set("[data-o=unitlabel]", "Shingle bundles (3 per square, with waste)", r);
      set("[data-o=units]", String(Math.ceil(order * 3)), r);
    }
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12, estimating software usually adds steep-roof labor. Check that the insurer’s estimate includes it." : pitch >= 7 ? "At 7/12 some estimates begin applying steep charges. Confirm how yours treats this pitch." : isTile ? "Tile at walkable pitch still breaks under foot traffic. Expect some extra breakage allowance when tile is lifted and reset." : "Walkable pitch: a steep-roof charge typically isn’t expected.";
  });

  /* 4. Percentage deductible (wind/hail or earthquake) */
  tool("deduct", function (r) {
    var kind = $("[name=kind]", r).value;
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=share]", loss > 0 ? Math.round(Math.min(pd, loss) / loss * 100) + "%" : "—", r);
    var what = kind === "quake" ? "earthquake" : "wind/hail";
    var note = kind === "quake" ? " Earthquake damage usually requires a separate policy or endorsement; a standard homeowners policy generally excludes it." : "";
    set("[data-o=below]", (loss <= 0 ? "Enter an estimated loss to compare payouts." : loss <= pd ? "This loss falls entirely within the " + what + " deductible, so no payment would be owed under it." : "The loss exceeds the " + what + " deductible by " + money(loss - pd) + ".") + note, r);
    var bar = $(".stack", r);
    if (bar) { var a = loss > 0 ? Math.min(pd, loss) / loss * 100 : 0; bar.children[0].style.width = a + "%"; bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%"; }
  });

  /* 5. Claim calendar builder (.ics export) */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-set target." },
      { d: add(num($("[name=mitig]", r))), t: "Mitigation finished, receipts saved", n: "Tarping, drying and board-up protect the claim and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often counted from the date of the insurer’s request. Check the request letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Policies set a deadline to finish repairs and claim held-back depreciation. Confirm yours." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "The deadline in your policy to file a lawsuit. Talk to a Nevada attorney well before it." }
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
      if (!plan.length) { var d = $('[data-tool="dates"] [name=dol]'); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Nevada Insurance Appraiser//Claim Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:nvia-" + ds(p.d) + "-" + i + "@nevadainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "nevada-claim-calendar.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal file scorecard */
  $$('[data-tool="ready"]').forEach(function (r) {
    var items = $$(".quiz li", r);
    var calc = function () {
      var got = 0, max = 0, answered = 0, todo = [];
      items.forEach(function (li) {
        var w = parseInt(li.getAttribute("data-w"), 10) || 1; max += w;
        var yes = $(".yes", li).getAttribute("aria-pressed") === "true", no = $(".no", li).getAttribute("aria-pressed") === "true";
        if (yes) got += w;
        if (yes || no) answered++;
        if (no) todo.push({ w: w, t: li.getAttribute("data-fix") });
      });
      todo.sort(function (a, b) { return b.w - a.w; });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? String(pct) : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#2d6a46" : pct >= 45 ? "#c8961f" : "#2f3a8f"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects. The next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before appraisal is demanded; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) { ul.innerHTML = ""; (todo.length ? todo : [{ t: "Nothing flagged yet." }]).forEach(function (x) { var li = document.createElement("li"); li.textContent = x.t; ul.appendChild(li); }); }
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

  /* 7. Smoke & ash cleaning scope estimator */
  tool("smoke", function (r) {
    var sf = num($("[name=sf]", r)), ch = num($("[name=ch]", r)), level = $("[name=level]", r).value;
    var k = { light: 0.7, moderate: 1, heavy: 1.5 }[level] || 1;
    // wall + ceiling area: ceiling = floor area; walls approximated from a square plan with interior partitions (perimeter × 2.2)
    var side = Math.sqrt(Math.max(sf, 0)), wallArea = side * 4 * 2.2 * ch, area = sf + wallArea;
    var surface = area * num($("[name=p_surface]", r)) * k;
    var hvac = num($("[name=hvac]", r)) * num($("[name=p_hvac]", r)) * (level === "heavy" ? 1.4 : 1);
    var contents = num($("[name=rooms]", r)) * num($("[name=p_room]", r)) * k;
    var air = num($("[name=days]", r)) * num($("[name=p_day]", r));
    var floor = sf * num($("[name=p_floor]", r)) * k;
    var ext = sf * num($("[name=p_ext]", r));
    var useAttic = $("[name=attic]", r).checked;
    var attic = useAttic ? sf * num($("[name=p_attic]", r)) : 0;
    var total = surface + hvac + contents + air + floor + ext + attic;
    set("[data-o=area]", Math.round(area).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=surface]", money(surface), r);
    set("[data-o=hvac]", money(hvac), r);
    set("[data-o=contents]", money(contents), r);
    set("[data-o=air]", money(air), r);
    set("[data-o=floor]", money(floor), r);
    set("[data-o=ext]", money(ext), r);
    set("[data-o=attic]", useAttic ? money(attic) : "not included", r);
    set("[data-o=total]", money(total), r);
    set("[data-o=msg]", sf <= 0 ? "Enter the home’s floor area to build a scope." : "Illustrative only. Compare each line with your insurer’s estimate: missing HVAC, contents or attic work is where smoke scopes most often fall short." + (level === "heavy" ? " With heavy residue, some materials may need replacement rather than cleaning." : ""), r);
  });
})();
