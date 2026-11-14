/* South Dakota Insurance Appraiser — site script: nav, drawer, effects, forms and claim calculators. No dependencies; nothing is stored. */
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
  var html = document.documentElement, body = document.body;
  html.classList.remove("no-js"); html.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = $("[data-drop]", o); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    var hover = function () { return window.matchMedia("(hover: hover)").matches; };
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!hover()) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover()) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim"), lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    scrim.hidden = false;
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    setTimeout(function () { if (!body.classList.contains("drawer-open")) scrim.hidden = true; }, 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (burger && drawer && scrim) {
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1020) closeDrawer(); });
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, back-to-top, parallax, process rail ---------- */
  var head = $(".head"), toTop = $(".to-top"), px = $$("[data-parallax]"), rail = $("[data-rail]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.12;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -k).toFixed(1) + "px,0)";
    });
    if (rail) {
      var rr = rail.getBoundingClientRect(), mid = vh * 0.65;
      var pct = Math.max(0, Math.min(1, (mid - rr.top) / Math.max(1, rr.height)));
      var fill = $(".rail-fill", rail);
      if (fill) { fill.style.width = (pct * 100) + "%"; rail.style.setProperty("--fill", (pct * 100) + "%"); }
      $$(".rail-step", rail).forEach(function (s) { s.classList.toggle("on", s.getBoundingClientRect().top < mid); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1500;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  $$(".rv").forEach(function (el) {
    var sibs = $$(":scope > .rv", el.parentElement);
    var i = sibs.indexOf(el);
    if (i > 0) el.style.setProperty("--d", Math.min(i, 8) * 0.07 + "s");
  });
  var counters = $$("[data-count]");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
    var co = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { count(en.target); co.unobserve(en.target); } });
    }, { threshold: 0.5 });
    counters.forEach(function (el) { co.observe(el); });
  } else {
    $$(".rv").forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- region tabs ---------- */
  $$("[data-regions]").forEach(function (wrap) {
    var tabs = $$("[role=tab]", wrap);
    var select = function (i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute("aria-controls"));
        if (p) p.hidden = !on;
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (ev) {
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") { ev.preventDefault(); select((i + 1) % tabs.length, true); }
        if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") { ev.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
    select(0);
  });

  /* ---------- glossary search ---------- */
  var gf = $("#gloss-filter"), gc = $("[data-gcount]");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), n = 0;
    $$(".gterm").forEach(function (row) {
      var hit = !q || row.textContent.toLowerCase().indexOf(q) > -1;
      row.hidden = !hit; if (hit) n++;
    });
    if (gc) gc.textContent = n + (n === 1 ? " term" : " terms") + (q ? " match" + (n === 1 ? "es" : "") + " “" + gf.value.trim() + "”" : "");
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please fill in the required fields and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and a South Dakota Insurance Appraiser team member will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error("send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@southdakotainsuranceappraiser.com\">info@southdakotainsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- calculator binding ---------- */
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
  var SD = window.SDIA = {};

  /* 1. Appraisal payoff estimator (home mini + full) */
  SD.payoff = function (ins, own, land, feeType, fee, ump, useUmp) {
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var cost = (feeType === "pct" ? gain * fee / 100 : fee) + (useUmp ? ump / 2 : 0);
    var fixed = (feeType === "pct" ? 0 : fee) + (useUmp ? ump / 2 : 0), rate = feeType === "pct" ? fee / 100 : 0;
    var be = gap > 0 && rate < 1 ? fixed / (gap * (1 - rate)) : Infinity;
    return { gap: gap, award: award, gain: gain, cost: cost, net: gain - cost, be: be };
  };
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var full = !!$("[name=fee]", r);
    var o = SD.payoff(ins, own, land, full ? $("[name=feetype]", r).value : "flat", num($("[name=fee]", r)), num($("[name=umpire]", r)), full && $("[name=useump]", r).checked);
    set("[data-o=gap]", money(o.gap), r); set("[data-o=award]", money(o.award), r); set("[data-o=gain]", money(o.gain), r);
    set("[data-o=cost]", money(o.cost), r); set("[data-o=net]", money(o.net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(o.gap / ins * 100) + "%" : "—", r);
    set("[data-o=be]", !isFinite(o.be) ? "—" : o.be > 1 ? "Not reachable" : Math.ceil(o.be * 100) + "% of the gap", r);
    var stack = $(".stack", r);
    if (stack) {
      var tot = Math.max(own, o.award, 1), s = stack.children;
      s[0].style.width = (ins / tot * 100) + "%";
      s[1].style.width = (Math.max(0, o.net) / tot * 100) + "%";
      s[2].style.width = (Math.min(o.cost, o.gain) / tot * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (o.gap <= 0) t = "Your number isn’t higher than the carrier’s. With no gap, there’s nothing for an appraisal panel to value.";
      else if (full && o.net <= 0) t = "At these inputs, appraisal costs would swallow the increase. A line-by-line estimate review is usually the better first step.";
      else if (o.gap / ins < 0.1 && o.gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount looks large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. Depreciation recovery */
  SD.dep = function (rows, cap, ded, acvOnly) {
    var rcv = 0, dep = 0;
    rows.forEach(function (x) { var d = Math.min(cap, x.age / Math.max(1, x.life)) * x.rcv; rcv += x.rcv; dep += d; x.acv = x.rcv - d; });
    var acv = rcv - dep, first = Math.max(0, acv - ded), total = acvOnly ? first : Math.max(0, rcv - ded);
    return { rcv: rcv, dep: dep, acv: acv, first: first, held: total - first, total: total };
  };
  tool("dep", function (r) {
    var rows = $$("tbody tr", r).map(function (tr) { return { tr: tr, rcv: num($("[name=rcv]", tr)), age: num($("[name=age]", tr)), life: num($("[name=life]", tr)) || 1 }; });
    var o = SD.dep(rows, (num($("[name=cap]", r)) || 80) / 100, num($("[name=deduct]", r)), $("[name=nonrec]", r).checked);
    rows.forEach(function (x) { set("[data-o=row]", money(x.acv), x.tr); });
    set("[data-o=rcv]", money(o.rcv), r); set("[data-o=dep]", money(o.dep), r); set("[data-o=acv]", money(o.acv), r);
    set("[data-o=first]", money(o.first), r); set("[data-o=held]", money(o.held), r); set("[data-o=total]", money(o.total), r);
    set("[data-o=deppct]", o.rcv ? Math.round(o.dep / o.rcv * 100) + "%" : "0%", r);
  });
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (ev) {
      if (ev.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr); $("input", tr).focus();
      }
      var x = ev.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof squares & slope factor */
  SD.roof = function (foot, pitch, waste) {
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2)), surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    return { mult: mult, surface: surface, sq: sq, order: Math.ceil(order * 3) / 3, bundles: Math.ceil(order * 3) };
  };
  tool("roof", function (r) {
    var mode = ($("[name=mode]:checked", r) || {}).value || "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), o = SD.roof(foot, pitch, num($("[name=waste]", r)) / 100), price = num($("[name=price]", r));
    set("[data-o=mult]", o.mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(o.surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", o.sq.toFixed(2), r);
    set("[data-o=order]", o.order.toFixed(2), r);
    set("[data-o=bundles]", String(o.bundles), r);
    set("[data-o=cost]", price ? money(o.order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software normally adds a steep-roof charge. Check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12, some carriers start applying steep charges. Confirm how your estimate treats this pitch." : "A walkable pitch: no steep-roof charge is usually expected.", r);
  });

  /* 4. Hail percentage deductible */
  SD.deduct = function (covA, pct, flat, loss) {
    var pd = covA * pct / 100;
    return { pd: pd, pdpay: Math.max(0, loss - pd), flatpay: Math.max(0, loss - flat), diff: Math.min(pd, loss) - Math.min(flat, loss) };
  };
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var o = SD.deduct(covA, pct, flat, loss);
    set("[data-o=pd]", money(o.pd), r); set("[data-o=pdpay]", money(o.pdpay), r); set("[data-o=flatpay]", money(o.flatpay), r); set("[data-o=diff]", money(o.diff), r);
    set("[data-o=below]", !loss ? "Enter an estimated loss to compare payouts." : loss <= o.pd ? "This loss falls entirely inside the percentage deductible, so the policy would pay nothing under it." : "The loss exceeds the percentage deductible by " + money(loss - o.pd) + ".", r);
    var bar = $(".stack", r);
    if (bar) { var a = loss > 0 ? Math.min(o.pd, loss) / loss * 100 : 0; bar.children[0].style.width = a + "%"; bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%"; }
    var lad = $("[data-o=ladder]", r);
    if (lad) lad.innerHTML = [0.5, 1, 2, 3, 5].map(function (p) {
      var x = SD.deduct(covA, p, flat, loss);
      return "<tr" + (p === pct ? ' class="cur"' : "") + "><td>" + p + "%</td><td>" + money(x.pd) + "</td><td>" + money(x.pdpay) + "</td></tr>";
    }).join("");
  });

  /* 5. Appraisal calendar builder (.ics) */
  var plan = [];
  SD.addDays = function (iso, days) { var d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + days); return d; };
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, dm = $("[name=demand]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; plan = []; return; }
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: SD.addDays(d0, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies call for prompt notice. Report as soon as you can; this is a self-set target." },
      { d: SD.addDays(d0, num($("[name=mitig]", r))), t: "Finish temporary repairs and keep receipts", n: "Tarping, board-up and drying protect the property and are usually reimbursable." },
      { d: SD.addDays(d0, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often counted from the carrier’s written request. Check the date on the request letter." },
      { d: SD.addDays(d0, num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Confirm the exact window in your policy’s loss settlement section." },
      { d: SD.addDays(d0, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Read the Suit Against Us clause and talk to a South Dakota attorney well before this date." }
    ];
    if (dm) plan.push({ d: SD.addDays(dm, num($("[name=appr]", r))), t: "Name your appraiser", n: "Many appraisal clauses give each side a set number of days after the written demand." });
    plan.sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + "<em>" + badge + "</em></b><strong>" + p.t + "</strong><br><span>" + p.n + "</span></li>";
    }).join("");
  });
  SD.ics = function (items) {
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
    var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
    var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
    var out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//South Dakota Insurance Appraiser//Appraisal Calendar//EN", "CALSCALE:GREGORIAN"];
    items.forEach(function (p, i) {
      var end = new Date(p.d); end.setDate(end.getDate() + 1);
      out.push("BEGIN:VEVENT", "UID:sdia-" + ds(p.d) + "-" + i + "@southdakotainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
    });
    out.push("END:VCALENDAR");
    return out.join("\r\n");
  };
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var d = $("[name=dol]"); if (d) d.focus(); return; }
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([SD.ics(plan)], { type: "text/calendar" }));
      a.download = "appraisal-calendar.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Claim file readiness grader */
  SD.grade = function (pct) { return pct >= 90 ? "A" : pct >= 75 ? "B" : pct >= 60 ? "C" : pct >= 45 ? "D" : "F"; };
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
      set("[data-o=score]", answered ? pct : 0, r);
      set("[data-o=grade]", answered ? SD.grade(pct) : "–", r);
      set("[data-o=count]", answered + " / " + items.length, r);
      set("[data-o=verdict]", !answered ? "Answer the questions to see your grade." : pct >= 75 ? "Strong file. You have what an appraisal panel expects. The next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before demanding appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      ul.innerHTML = todo.length ? todo.map(function (t) { return "<li>" + t + "</li>"; }).join("") : "<li>Nothing flagged yet.</li>";
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

  /* 7. Coinsurance penalty */
  SD.coins = function (value, pct, limit, loss, ded) {
    var req = value * pct / 100, ratio = req > 0 ? Math.min(1, limit / req) : 1;
    var full = Math.max(0, Math.min(limit, loss - ded)), pay = Math.max(0, Math.min(limit, loss * ratio - ded));
    return { req: req, ratio: ratio, full: full, pay: pay, pen: full - pay, need: req };
  };
  tool("coins", function (r) {
    var o = SD.coins(num($("[name=value]", r)), num($("[name=pct]", r)), num($("[name=limit]", r)), num($("[name=loss]", r)), num($("[name=deduct]", r)));
    set("[data-o=req]", money(o.req), r); set("[data-o=ratio]", Math.round(o.ratio * 100) + "%", r);
    set("[data-o=full]", money(o.full), r); set("[data-o=pay]", money(o.pay), r); set("[data-o=pen]", money(o.pen), r); set("[data-o=need]", money(o.need), r);
    var b = $("[data-o=bar]", r); if (b) b.style.width = Math.round(o.ratio * 100) + "%";
    set("[data-o=cmsg]", o.ratio >= 1 ? "You meet the coinsurance requirement at these figures, so no penalty applies." : "You carry " + Math.round(o.ratio * 100) + "% of the required insurance, so the policy may pay only that share of the loss. Raising the limit to about " + money(o.need) + " would meet the requirement.", r);
  });

  var yEl = $("[data-year]"); if (yEl) yEl.textContent = new Date().getFullYear();
})();
