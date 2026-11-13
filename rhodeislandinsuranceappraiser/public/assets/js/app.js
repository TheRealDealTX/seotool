/* Rhode Island Insurance Appraiser: navigation, effects, forms and claim tools. No dependencies; nothing is stored. */
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

  /* ---------- desktop dropdowns ---------- */
  var closeSubs = function (except) {
    $$(".has-sub.open").forEach(function (li) { if (li !== except) { li.classList.remove("open"); $(".sub-btn", li).setAttribute("aria-expanded", "false"); } });
  };
  $$(".has-sub").forEach(function (li) {
    var btn = $(".sub-btn", li), t;
    var open = function () { closeSubs(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); if (li.classList.contains("open")) closeSubs(); else open(); });
    li.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) { clearTimeout(t); open(); } });
    li.addEventListener("mouseleave", function () { if (window.matchMedia("(hover: hover)").matches) { t = setTimeout(function () { closeSubs(); }, 180); } });
    li.addEventListener("focusout", function (e) { if (!li.contains(e.relatedTarget)) { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeSubs(); });

  /* ---------- mobile drawer (outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    body.classList.add("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1020) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeSubs(); closeDrawer(); } });

  /* ---------- header state, progress bar, back to top ---------- */
  var hdr = $(".hdr"), bar = $(".progress span"), toTop = $(".to-top"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (hdr) hdr.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  $$(".rv").forEach(function (el) {
    var sib = el.parentElement ? $$(":scope > .rv", el.parentElement) : [];
    var i = sib.indexOf(el);
    if (i > 0) el.style.setProperty("--d", (Math.min(i, 6) * 0.07) + "s");
  });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
    var cio = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { $$("[data-count]", en.target).forEach(count); cio.unobserve(en.target); } });
    }, { threshold: 0.4 });
    $$(".facts-band").forEach(function (el) { cio.observe(el); });
  } else {
    $$(".rv").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- region tabs ---------- */
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
        if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
        if (e.key === "Home") { e.preventDefault(); select(0, true); }
        if (e.key === "End") { e.preventDefault(); select(tabs.length - 1, true); }
      });
    });
    select(0);
  });

  /* ---------- scroll rails ---------- */
  $$(".rail-wrap").forEach(function (w) {
    var rail = $("[data-rail]", w);
    var go = function (dir) { var c = rail.firstElementChild; var step = c ? c.getBoundingClientRect().width + 20 : 320; rail.scrollBy({ left: dir * step, behavior: reduce ? "auto" : "smooth" }); };
    var p = $("[data-rail-prev]", w), n = $("[data-rail-next]", w);
    if (p) p.addEventListener("click", function () { go(-1); });
    if (n) n.addEventListener("click", function () { go(1); });
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0;
    $$(".g-item").forEach(function (it) { var hit = !q || it.textContent.toLowerCase().indexOf(q) > -1; it.hidden = !hit; if (hit) shown++; });
    set("[data-gloss-count]", shown + (shown === 1 ? " term" : " terms") + (q ? " match" : ""));
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      var em = $("[type=email]", form);
      if (em && em.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em.value)) bad.push(em);
      $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      if (bad.length) { bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); }); msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and someone from Rhode Island Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else throw new Error("send failed");
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@rhodeislandinsuranceappraiser.com\">info@rhodeislandinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding ---------- */
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
  function rowTable(name) {
    $$('[data-tool="' + name + '"]').forEach(function (r) {
      var tb = $("tbody", r);
      r.addEventListener("click", function (e) {
        if (e.target.closest("[data-add]")) {
          var tr = tb.rows[0].cloneNode(true);
          $$("input", tr).forEach(function (i) { i.value = ""; });
          $$("select", tr).forEach(function (s) { s.selectedIndex = 0; });
          tb.appendChild(tr);
        }
        var x = e.target.closest(".x");
        if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
      });
    });
  }

  /* 1. Settlement gap estimator (home mini + full) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var ftEl = $("[name=feetype]", r), ft = ftEl ? ftEl.value : null;
    var fee = num($("[name=fee]", r)), rate = num($("[name=rate]", r));
    var hr = $("[data-hourly]", r); if (hr) hr.hidden = ft !== "hourly";
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var ump = num($("[name=umpire]", r));
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var cost = !ft ? 0 : ft === "pct" ? gain * fee / 100 : ft === "hourly" ? fee * rate : fee;
    if (useUmp) cost += ump / 2;
    var net = gain - cost;
    set("[data-o=gap]", money(gap), r); set("[data-o=award]", money(award), r); set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r); set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=costpct]", gain > 0 ? Math.round(cost / gain * 100) + "%" : "—", r);
    var st = $(".stack", r);
    if (st) { var tot = Math.max(own, award, 1), s = st.children; s[0].style.width = (ins / tot * 100) + "%"; s[1].style.width = (Math.max(0, net) / tot * 100) + "%"; s[2].style.width = (Math.min(cost, gain) / tot * 100) + "%"; }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the amount in dispute.";
      else if (gap <= 0) t = "Your estimate isn’t higher than the carrier’s, so there’s no amount in dispute to appraise.";
      else if (ft && net <= 0) t = "At these inputs, appraisal costs would absorb the whole increase. A line-by-line estimate review is usually a better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
  tool("dep", function (r) {
    var cap = (num($("[name=cap]", r)) || 75) / 100, rcv = 0, dep = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, Math.max(0, age) / life) * c;
      rcv += c; dep += d;
      set("[data-o=row]", money(c - d), tr);
    });
    var ded = num($("[name=deduct]", r)), nonrec = $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), full = Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r); set("[data-o=dep]", money(dep), r); set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(nonrec ? 0 : full - first), r);
    set("[data-o=total]", money(nonrec ? first : full), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
  });
  rowTable("dep");

  /* 3. Roof area & pitch */
  tool("roof", function (r) {
    var mc = $("[name=mode]:checked", r), mode = mc ? mc.value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100, surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=deg]", (Math.atan(pitch / 12) * 180 / Math.PI).toFixed(1) + "°", r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software usually adds a steep charge. Check that your estimate includes it." : pitch >= 7 ? "At 7/12 some estimates begin adding steep charges. Check how yours treats this pitch." : "Walkable pitch: a steep charge usually isn’t expected.", r);
  });

  /* 4. Hurricane deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=break]", money(pd), r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payments." : loss <= pd ? "This loss falls entirely within the hurricane deductible, so no payment would be owed if that deductible applies." : "The loss is " + money(loss - pd) + " above the hurricane deductible.", r);
    var st = $(".stack", r);
    if (st) { var a = loss > 0 ? Math.min(pd, loss) / loss * 100 : 0; st.children[0].style.width = a + "%"; st.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%"; }
  });

  /* 5. Claim timeline builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, rq = $("[name=req]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><strong>Pick your date of loss</strong><br><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), reqD = rq ? new Date(rq + "T12:00:00") : null;
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(base, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-set target." },
      { d: add(base, num($("[name=mitig]", r))), t: "Finish temporary repairs and keep receipts", n: "Tarping, water extraction and board-up protect the property and are often reimbursable." },
      { d: add(reqD || base, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: reqD ? "Counted from the carrier’s request date you entered." : "Often counted from the carrier’s written request. Enter the request date above if you have one." },
      { d: add(base, num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Policies set a deadline to finish repairs and claim the holdback. Confirm the exact number of days." },
      { d: add(base, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Many policies limit suits to two years from the loss. Talk to a Rhode Island attorney well before this date." }
    ];
    var ap = num($("[name=appr]", r));
    if (ap) plan.push({ d: add(today, ap), t: "If appraisal is demanded today: name your appraiser by", n: "Many policies allow about 20 days after a written demand. Check your policy." });
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
      if (!plan.length) { var d = $('[data-tool="dates"] [name=dol]'); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/([,;])/g, "\\$1"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Rhode Island Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:ria-" + ds(p.d) + "-" + i + "@rhodeislandinsuranceappraiser.com", "DTSTAMP:" + stamp,
          "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "rhode-island-claim-timeline.ics";
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
        var yes = $(".yes", li).getAttribute("aria-pressed") === "true", no = $(".no", li).getAttribute("aria-pressed") === "true";
        if (yes) got += w;
        if (yes || no) answered++;
        if (no) todo.push(li.getAttribute("data-fix"));
      });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? String(pct) : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1d6b3a" : pct >= 45 ? "#FEC500" : "#23317A"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects. Next step: a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before invoking appraisal; each one weakens your number." : "Not ready yet. Invoking appraisal now risks a low award. Work through the list below first.", r);
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

  /* 7. Wind vs. flood splitter */
  tool("split", function (r) {
    var wind = 0, flood = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var a = num($("[name=amt]", tr)), c = $("[name=cause]", tr).value, wp = $("[name=wpct]", tr);
      var share = c === "wind" ? 1 : c === "flood" ? 0 : Math.max(0, Math.min(100, num(wp))) / 100;
      if (c !== "mixed" && wp) wp.value = c === "wind" ? 100 : 0;
      wind += a * share; flood += a * (1 - share);
    });
    var covA = num($("[name=cova]", r)), hp = num($("[name=hpct]", r)), std = num($("[name=std]", r)), fd = num($("[name=fded]", r));
    var hded = hp > 0 ? covA * hp / 100 : std;
    var hnet = Math.max(0, wind - hded), fnet = Math.max(0, flood - fd);
    var dedCarried = Math.min(wind, hded) + Math.min(flood, fd);
    set("[data-o=wind]", money(wind), r); set("[data-o=flood]", money(flood), r);
    set("[data-o=hded]", money(hded), r); set("[data-o=hnet]", money(hnet), r); set("[data-o=fnet]", money(fnet), r); set("[data-o=ded]", money(dedCarried), r);
    var st = $(".stack", r), tot = wind + flood;
    if (st) { st.children[0].style.width = (tot ? wind / tot * 100 : 0) + "%"; st.children[1].style.width = (tot ? flood / tot * 100 : 0) + "%"; }
    set("[data-o=msg]", !tot ? "Add the damaged items to see the split." : wind <= hded && wind > 0 ? "The wind portion is at or below the homeowner deductible you chose, so the homeowner policy may pay nothing on these figures." : "Illustrative split only. Each insurer decides causation under its own policy.", r);
  });
  rowTable("split");

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
