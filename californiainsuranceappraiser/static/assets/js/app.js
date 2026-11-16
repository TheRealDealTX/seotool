/* California Insurance Appraiser — site script (nav, drawer, reveal, forms, claim tools). No dependencies. */
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

  /* ---------- desktop dropdowns (CSS hover works without JS; buttons add click/keyboard) ---------- */
  var closeSubs = function (except) {
    $$(".has-sub.open").forEach(function (li) { if (li === except) return; li.classList.remove("open"); $(".sub-btn", li).setAttribute("aria-expanded", "false"); });
  };
  $$(".sub-btn").forEach(function (btn) {
    var li = btn.parentElement;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !li.classList.contains("open");
      closeSubs(li);
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".has-sub")) closeSubs(); });

  /* ---------- mobile drawer ---------- */
  var drawer = $("#drawer"), menuBtn = $(".menu-btn"), scrim = $(".scrim");
  var lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    menuBtn.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!drawer || !body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    menuBtn.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!body.classList.contains("drawer-open")) scrim.hidden = true; }, 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (drawer && menuBtn) {
    menuBtn.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") !== "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); $("#" + o.getAttribute("aria-controls")).hidden = true; });
        b.setAttribute("aria-expanded", open ? "true" : "false");
        $("#" + b.getAttribute("aria-controls")).hidden = !open;
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1100) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeSubs(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, back-to-top, parallax, timeline fill ---------- */
  var head = $(".site-head"), toTop = $(".to-top"), px = $$("[data-parallax]"), tl = $("[data-tl]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -0.15).toFixed(1) + "px,0)";
    });
    if (tl) {
      var r = tl.getBoundingClientRect(), mid = vh * 0.65;
      var p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      tl.style.setProperty("--p", (p * 100).toFixed(1) + "%");
      $$(".tl-step", tl).forEach(function (s, i, all) { s.classList.toggle("on", p >= (i + 0.5) / all.length || s.getBoundingClientRect().top < mid - r.height * 0.9); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------- reveal (staggered), counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  $$(".pgrid, .ledger-in, .tl, .svc-more, .map-grid").forEach(function (g) {
    $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); });
  });
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(reveal); }

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter"), gc = $("[data-gloss-count]");
  if (gf) {
    var terms = $$(".glossary .term");
    var upd = function () {
      var q = gf.value.trim().toLowerCase(), n = 0;
      terms.forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
      if (gc) gc.textContent = q ? n + " of " + terms.length + " terms match" : terms.length + " terms";
    };
    gf.addEventListener("input", upd); upd();
  }

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      if (bad.length) { bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); }); msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and someone from California Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@californiainsuranceappraiser.com\">info@californiainsuranceappraiser.com</a>."; msg.classList.add("err"); })
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

  /* 1. Appraisal payoff estimator (home mini + full) */
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
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
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
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal resolves how much a covered loss costs; with no gap, there is nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready when you call.";
      m.textContent = t;
    }
  });

  /* 2. ACV & holdback */
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
        $("input", tr).focus();
      }
      var x = e.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof area & pitch */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), mat = $("[name=mat]", r).value;
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", order.toFixed(2), r);
    var units = { tile: ["Approx. field tiles (≈90/sq)", Math.ceil(order * 90)], shingle: ["Shingle bundles (3/sq)", Math.ceil(order * 3)], shake: ["Shake bundles (≈4/sq)", Math.ceil(order * 4)], low: ["Membrane rolls (≈1/sq)", Math.ceil(order)] }[mat];
    set("[data-o=unitlabel]", units[0], r);
    set("[data-o=units]", units[1].toLocaleString("en-US"), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var note;
    if (mat === "low" && pitch > 3) note = "Low-slope membranes are generally for pitches of 3/12 or less. Check the roofing type on your estimate.";
    else if (mat === "tile" && pitch < 4) note = "Many tile systems need at least a 4/12 pitch, or special underlayment below it. Check what is actually installed.";
    else if (pitch >= 8) note = "At " + pitch + "/12 most estimating software adds a steep-roof charge. Check that the carrier’s estimate includes it.";
    else if (pitch >= 7) note = "At 7/12 some carriers start applying steep charges. Confirm how your estimate treats this pitch.";
    else note = "Walkable pitch: a steep-roof charge usually isn’t expected. High or hillside roofs may still need extra access costs.";
    set("[data-o=steep]", note, r);
  });

  /* 4. Earthquake (percentage) deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, Math.min(loss, covA) - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, Math.min(loss, covA) - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(pd, loss) - Math.min(flat, loss))), r);
    set("[data-o=below]", loss <= 0 ? "Enter estimated earthquake damage to compare payments." : loss <= pd ? "This damage falls entirely within the earthquake deductible, so the dwelling coverage would pay nothing for it." : "The damage exceeds the deductible by " + money(loss - pd) + ".", r);
    var bar = $(".stack", r);
    if (bar) {
      var a = loss > 0 ? Math.min(pd, loss) / loss * 100 : 0;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%";
    }
  });

  /* 5. California claim timeline builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    var em = $("[name=emerg]", r), rc = $("[name=rcm]", r), su = $("[name=suitm]", r);
    if (em && !em.dataset.bound) {
      em.dataset.bound = "1";
      em.addEventListener("change", function () { rc.value = em.checked ? 36 : 12; su.value = em.checked ? 24 : 12; });
    }
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00");
    var rep = $("[name=reported]", r).value ? new Date($("[name=reported]", r).value + "T12:00:00") : base;
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var addD = function (d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; };
    var addM = function (d, n) { var x = new Date(d); x.setMonth(x.getMonth() + n); return x; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    var rcm = num(rc) || 12, sm = num(su) || 12;
    plan = [
      { d: addD(rep, 15), t: "Insurer should have acknowledged the claim", n: "California regulations generally require acknowledgment within 15 calendar days of notice." },
      { d: addD(rep, 55), t: "Check on the coverage decision", n: "Insurers generally must accept or deny within 40 days after receiving proof of claim. This date assumes proof of claim about 15 days after notice." },
      { d: addM(base, rcm), t: "Replacement cost (holdback) window, as entered", n: "Commonly at least 12 months from the first ACV payment, or 36 months after a declared state of emergency. This date counts from the loss; confirm with your policy." },
      { d: addM(base, sm), t: "Policy suit-limitation date, before tolling", n: "Commonly 12 months, or 24 months for losses tied to a declared emergency. California tolls the period while the claim is open, so the real date may be later. Ask an attorney." }
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
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//California Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:cia-" + ds(p.d) + "-" + i + "@californiainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "california-claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness check */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1f6f72" : pct >= 45 ? "#b58150" : "#ba0c2f"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the documentation a panel expects; the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each one weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) {
        ul.textContent = "";
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

  /* 7. Rebuild cost & underinsurance check */
  tool("rebuild", function (r) {
    var sqft = num($("[name=sqft]", r)), psf = num($("[name=psf]", r)), covA = num($("[name=cova]", r));
    var erc = num($("[name=erc]", r)) / 100, codePct = num($("[name=code]", r)) / 100, codeCost = num($("[name=codecost]", r));
    var debris = num($("[name=debris]", r)), debPct = num($("[name=debrispct]", r)) / 100;
    var rebuild = sqft * psf;
    var avail = covA * (1 + erc);
    var codeUsed = Math.min(codeCost, covA * codePct);
    var debrisExtra = Math.min(debris, covA * debPct);
    var debrisLeft = debris - debrisExtra;               // remainder comes out of the dwelling limit
    var project = rebuild + codeCost + debris;
    var dwellingNeed = rebuild + debrisLeft;
    var dwellingPaid = Math.min(dwellingNeed, avail);
    var covered = dwellingPaid + codeUsed + debrisExtra;
    var short = Math.max(0, project - covered);
    var ratio = project > 0 ? covered / project : 0;
    set("[data-o=rebuild]", money(rebuild), r);
    set("[data-o=avail]", money(avail), r);
    set("[data-o=codeused]", money(codeUsed), r);
    set("[data-o=debrisused]", money(debrisExtra + Math.min(debrisLeft, Math.max(0, avail - rebuild))), r);
    set("[data-o=project]", money(project), r);
    set("[data-o=short]", money(short), r);
    set("[data-o=ratio]", project > 0 ? Math.round(ratio * 100) + "%" : "—", r);
    var m = $("[data-o=meter]", r);
    if (m) { m.style.width = Math.min(100, ratio * 100) + "%"; m.style.backgroundColor = ratio >= 0.98 ? "#1f6f72" : ratio >= 0.85 ? "#b58150" : "#ba0c2f"; }
    set("[data-o=msg]", !project ? "Enter your home’s size and a local rebuild cost." : short <= 0 ? "At these figures your limits appear to cover the project. A detailed estimate is still the only way to know." : ratio >= 0.85 ? "A modest shortfall. A detailed rebuild estimate could show whether extended replacement cost and code coverage close it." : "A significant shortfall. Get a detailed local rebuild estimate and confirm every coverage before you accept the carrier’s figure.", r);
  });
})();
