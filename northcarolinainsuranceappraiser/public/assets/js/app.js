/* North Carolina Insurance Appraiser — site script (nav, drawer, effects, forms, claim tools). No dependencies. */
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
  var hover = window.matchMedia("(hover: hover)");

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!hover.matches) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover.matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the fixed header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), bg = $(".drawer-bg"), hideT;
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    clearTimeout(hideT);
    if (bg) bg.hidden = false;
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function (refocus) {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    hideT = setTimeout(function () { if (bg && !isOpen()) bg.hidden = true; }, 320);
    if (refocus) burger.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(true); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1100) closeDrawer(false); });
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeDrops(); closeDrawer(true); } });

  /* ---------- solid header, back-to-top ring, parallax ---------- */
  var head = $(".head"), toTop = $(".to-top"), ring = $(".ring-fill");
  var px = reduce ? [] : $$("[data-parallax]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 700);
    if (ring) ring.style.strokeDashoffset = (144.5 * (1 - (h > 0 ? Math.min(1, y / h) : 0))).toFixed(1);
    px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0)";
    });
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function (ev) { ev.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1500;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  $$(".pgrid,.lgrid,.storm-rail,.steps,.ggrid,.tlist,.region-rail,.who,.mapgrid").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); }); });
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.12, rootMargin: "0px 0px -30px 0px" });
    $$(".rv, .ribbon").forEach(function (el) { io.observe(el); });
  } else { $$(".rv, .ribbon").forEach(reveal); }

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter"), gc = $("[data-gcount]");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".glossary .term").forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
    if (gc) gc.textContent = q ? n + (n === 1 ? " term matches" : " terms match") : "";
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please fill in the required fields and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your details arrived safely, and someone from North Carolina Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@northcarolinainsuranceappraiser.com\">info@northcarolinainsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binder ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (root) {
      var run = function () { fn(root); };
      root.addEventListener("input", run);
      root.addEventListener("change", run);
      root.addEventListener("click", function (ev) { if (ev.target.closest("[data-run]")) setTimeout(run, 0); });
      $$(".range input[type=range]", root).forEach(function (r) {
        var out = r.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = r.value + (r.getAttribute("data-unit") || ""); };
        r.addEventListener("input", upd); upd();
      });
      run();
    });
  }
  /* add/remove rows in item tables (holdback + splitter) */
  $$('[data-tool="dep"], [data-tool="split"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (ev) {
      if (ev.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr);
      }
      var x = ev.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 1. Settlement gap estimator (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var netAt = function (share) {
      var gain = gap * share;
      var cost = (feeType === "pct" ? gain * fee / 100 : fee) + (useUmp ? ump / 2 : 0);
      return { gain: gain, cost: cost, net: gain - cost };
    };
    var o = netAt(land), award = ins + o.gain;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(o.gain), r);
    set("[data-o=cost]", money(o.cost), r);
    set("[data-o=net]", money(o.net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=s30]", money(netAt(0.3).net), r);
    set("[data-o=s50]", money(netAt(0.5).net), r);
    set("[data-o=s80]", money(netAt(0.8).net), r);
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, award, 1), s = stack.children;
      s[0].style.width = (ins / total * 100) + "%";
      s[1].style.width = (Math.max(0, o.net) / total * 100) + "%";
      s[2].style.width = (Math.min(o.cost, o.gain) / total * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your figure isn’t higher than the carrier’s. Appraisal resolves how much a covered loss costs; with no gap there’s nothing to appraise.";
      else if ($("[name=fee]", r) && o.net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate audit is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready. Figures are illustrative.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0, cap = num($("[name=cap]", r)) / 100 || 0.8;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", nonrec ? money(0) : money(Math.min(dep, Math.max(0, rcv - ded) - first)), r);
    set("[data-o=total]", money(nonrec ? first : Math.max(0, rcv - ded)), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
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
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste), price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software usually adds a steep-roof labor charge. Check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 some estimates begin applying steep charges. Confirm how yours treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.", r);
  });

  /* 4. Named-storm deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.min(loss, pd) - Math.min(loss, flat)), r);
    set("[data-o=below]", loss > 0 && loss <= pd ? "This loss sits entirely inside the percentage deductible, so no payment would be owed under it." : loss > 0 ? "The loss exceeds the percentage deductible by " + money(loss - pd) + ". Figures are illustrative." : "Enter an estimated loss to compare payments.", r);
    var bar = $(".stack", r);
    if (bar && loss > 0) { var a = Math.min(pd, loss) / loss * 100; bar.children[0].style.width = a + "%"; bar.children[1].style.width = (100 - a) + "%"; }
  });

  /* 5. Claim timeline planner + .ics */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you safely can; this target is your own." },
      { d: add(num($("[name=mitig]", r))), t: "Temporary repairs done, receipts saved", n: "Tarping, drying and board-up protect the property and are usually part of the claim." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often counted from the date of the carrier’s written request. Check your letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Finish repairs and request the holdback before the deadline in your loss settlement section." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Many property forms say three years from the loss; confirm yours and speak with a North Carolina attorney well before this." }
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
      if (!plan.length) { var d = $('[name=dol]'); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//North Carolina Insurance Appraiser//Claim Timeline Planner//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:ncia-" + ds(p.d) + "-" + i + "@northcarolinainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "nc-claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Preparedness checkup */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1f5136" : pct >= 45 ? "#e27a4f" : "#b8522c"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting close. Close the gaps below before you demand appraisal; each one weakens your number if it’s missing." : "Not ready yet. Demanding appraisal now risks a weak award. Work through the list below first.", r);
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

  /* 7. Wind vs. flood damage splitter */
  tool("split", function (r) {
    var mix = num($("[name=mix]", r)) / 100, wind = 0, flood = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var a = num($("[name=amt]", tr)), c = $("[name=cause]", tr).value;
      if (c === "wind") wind += a; else if (c === "flood") flood += a; else { wind += a * mix; flood += a * (1 - mix); }
    });
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r));
    var hded = pct > 0 ? covA * pct / 100 : flat;
    var hopay = Math.min(covA || Infinity, Math.max(0, wind - hded));
    var has = $("[name=hasflood]", r).checked;
    $$("[data-flood]", r).forEach(function (el) { el.hidden = !has; });
    var fl = num($("[name=flimit]", r)), fded = num($("[name=fded]", r));
    var flpay = has ? Math.min(fl, Math.max(0, flood - fded)) : 0;
    var total = wind + flood, gap = Math.max(0, total - hopay - flpay);
    set("[data-o=total]", money(total), r);
    set("[data-o=wind]", money(wind), r);
    set("[data-o=flood]", money(flood), r);
    set("[data-o=hded]", money(Math.min(hded, wind)), r);
    set("[data-o=hopay]", money(hopay), r);
    set("[data-o=flpay]", money(flpay), r);
    set("[data-o=gap]", money(gap), r);
    var s = $(".stack", r).children, t = Math.max(total, 1);
    s[0].style.width = (hopay / t * 100) + "%"; s[1].style.width = (flpay / t * 100) + "%"; s[2].style.width = (gap / t * 100) + "%";
    set("[data-o=msg]", !total ? "Add damage items to see the split." : !has && flood > 0 ? "Without a flood policy, the " + money(flood) + " allocated to flood would generally stay with you. That’s why the evidence behind each allocation matters. Illustrative only." : "Moving the slider shows how much depends on how unclear items are documented. Illustrative only; real allocations rest on evidence and policy wording.", r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
