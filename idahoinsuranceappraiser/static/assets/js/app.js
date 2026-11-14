/* Idaho Insurance Appraiser — site script (nav, drawer, effects, forms, claim tools). No dependencies. */
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
    $$(".menu li.open").forEach(function (o) { if (o === except) return; o.classList.remove("open"); var b = $("[data-drop]", o); if (b) b.setAttribute("aria-expanded", "false"); });
  };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    var open = function () { closeDrops(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); if (li.classList.contains("open")) closeDrops(); else open(); });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); open(); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim");
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    if (!drawer) return;
    scrim.hidden = false;
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
    setTimeout(function () { if (!isOpen()) scrim.hidden = true; }, 300);
    if (refocus) burger.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(true); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1100) closeDrawer(false); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(true); } });

  /* ---------- scroll effects: solid header, progress, back-to-top, parallax, timeline ---------- */
  var head = $(".head"), bar = $(".progress span"), toTop = $(".to-top");
  var px = $$("[data-parallax]"), tl = $("[data-tline]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = root.scrollHeight - window.innerHeight, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + (-r.top * k).toFixed(1) + "px,0)";
    });
    if (tl) {
      var tr = tl.getBoundingClientRect(), line = vh * 0.65;
      var p = Math.max(0, Math.min(1, (line - tr.top) / Math.max(1, tr.height)));
      tl.style.setProperty("--p", reduce ? 1 : p.toFixed(3));
      $$(".tstep", tl).forEach(function (s) { s.classList.toggle("on", reduce || s.getBoundingClientRect().top < line); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0"; requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.09 + "s"); }); });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- region carousel ---------- */
  $$("[data-carousel]").forEach(function (c) {
    var track = $(".car-track", c);
    $$(".car-btn", c).forEach(function (b) {
      b.addEventListener("click", function () {
        var card = $(".region", track), w = card ? card.getBoundingClientRect().width + 22 : 300;
        track.scrollBy({ left: w * parseInt(b.getAttribute("data-dir"), 10), behavior: reduce ? "auto" : "smooth" });
      });
    });
  });

  /* ---------- glossary search ---------- */
  var gf = $("#gloss-filter"), gc = $("[data-gcount]");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0, terms = $$(".glossary .gterm");
    terms.forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) shown++; });
    if (gc) gc.textContent = q ? shown + " of " + terms.length + " terms match" : "";
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and someone from Idaho Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "The form couldn’t be sent just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@idahoinsuranceappraiser.com\">info@idahoinsuranceappraiser.com</a>."; msg.classList.add("err"); })
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
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  /* 1. Claim gap & net recovery estimator */
  var gapCalc = function (ins, own, land, feeType, fee, hours, ump, useUmp) {
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var cost = feeType === "pct" ? gain * fee / 100 : feeType === "hourly" ? fee * hours : fee;
    if (useUmp) cost += ump / 2;
    return { gap: gap, award: award, gain: gain, cost: cost, net: gain - cost };
  };
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var ftEl = $("[name=feetype]", r), feeType = ftEl ? ftEl.value : "none";
    var fee = num($("[name=fee]", r)), hours = num($("[name=hours]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var hr = $("[data-hourly]", r); if (hr) hr.hidden = feeType !== "hourly";
    if (!ftEl) { fee = 0; useUmp = false; }
    var c = gapCalc(ins, own, land, feeType, fee, hours, ump, useUmp);
    set("[data-o=gap]", money(c.gap), r);
    set("[data-o=award]", money(c.award), r);
    set("[data-o=gain]", money(c.gain), r);
    set("[data-o=cost]", money(c.cost), r);
    set("[data-o=net]", money(c.net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(c.gap / ins * 100) + "%" : "—", r);
    var be = $("[data-o=breakeven]", r);
    if (be) {
      // smallest landing point (in 1% steps) where net >= 0
      var found = null;
      for (var p = 0; p <= 100; p++) { if (gapCalc(ins, own, p / 100, feeType, fee, hours, ump, useUmp).net >= 0 && c.gap > 0) { found = p; break; } }
      be.textContent = c.gap <= 0 ? "—" : found === null ? "Not reached" : found + "% of the gap";
    }
    var sc = $("[data-o=scen]", r);
    if (sc) sc.innerHTML = [30, 50, 80].map(function (p) {
      var n = gapCalc(ins, own, p / 100, feeType, fee, hours, ump, useUmp).net;
      return '<div class="' + (n < 0 ? "neg" : "") + (Math.round(land * 100) === p ? " cur" : "") + '"><small>Lands at ' + p + '%</small><b>' + money(n) + '</b></div>';
    }).join("");
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
      if (!ins || !own) t = "Enter both estimates to see the amount in dispute.";
      else if (c.gap <= 0) t = "Your number isn’t higher than the insurer’s. Appraisal settles what a covered loss costs; with no gap, there’s nothing to appraise.";
      else if (ftEl && c.net <= 0) t = "At these inputs, appraisal costs could swallow the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (c.gap / ins < 0.1 && c.gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The amount in dispute is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. RCV vs ACV holdback */
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

  /* 3. Roof pitch & squares */
  tool("roof", function (r) {
    var modeEl = $("[name=mode]:checked", r), mode = modeEl ? modeEl.value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r)), carrier = num($("[name=carrier]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=deg]", (Math.atan(pitch / 12) * 180 / Math.PI).toFixed(1) + "°", r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=vs]", carrier ? ((sq - carrier >= 0 ? "+" : "−") + Math.abs(sq - carrier).toFixed(2) + " sq (" + (carrier ? Math.round((sq - carrier) / carrier * 100) : 0) + "%)") : "—", r);
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge. Check that the insurer’s estimate includes it." : pitch >= 7 ? "At 7/12 some insurers begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.";
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=thresh]", money(pd), r);
    var lad = $("[data-o=ladder]", r);
    if (lad) lad.innerHTML = [0.5, 1, 2, 3, 5].map(function (p) {
      var pay = Math.max(0, loss - covA * p / 100);
      return '<div class="' + (pay <= 0 ? "neg" : "") + (p === pct ? " cur" : "") + '"><small>' + p + '% pays</small><b>' + money(pay) + '</b></div>';
    }).join("");
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payouts." : loss <= pd ? "This loss falls entirely within the percentage deductible, so that deductible would leave no claim payment." : "The loss is " + money(loss - pd) + " above the percentage deductible.", r);
    var st = $(".stack", r);
    if (st && loss > 0) { var a = Math.min(pd, loss) / loss * 100; st.children[0].style.width = a + "%"; st.children[1].style.width = (100 - a) + "%"; }
  });

  /* 5. Claim timeline builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-set target." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarps, water extraction and board-up protect the claim and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies allow 60 days after the insurer’s request. Count from the date on the request letter." },
      { d: add(45 + num($("[name=appr]", r))), t: "Name your appraiser (if appraisal is demanded)", n: "Assumes a written demand 45 days after the loss. Many clauses allow 20 days to name an appraiser; check yours." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Policies set a deadline to finish repairs and claim the holdback. Confirm the exact period in your policy." },
      { d: add(num($("[name=suit]", r))), t: "Suit-limitation date from your policy", n: "Idaho law can affect how this clause applies. Confirm the real deadline with an Idaho attorney well before this date." }
    ].sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + "<em>" + badge + "</em></b><strong>" + esc(p.t) + "</strong><br><span>" + esc(p.n) + "</span></li>";
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var dol = $("[name=dol]"); if (dol) dol.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var icsEsc = function (s) { return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Idaho Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:iia-" + ds(p.d) + "-" + i + "@idahoinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + icsEsc(p.t), "DESCRIPTION:" + icsEsc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "idaho-claim-timeline.ics";
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
      set("[data-o=score]", answered ? pct : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1f7a52" : pct >= 45 ? "#f2d900" : "#d9622b"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the items below before you demand appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) ul.innerHTML = todo.length ? todo.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") : "<li>Nothing flagged yet.</li>";
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

  /* 7. Roof snow load estimator */
  tool("snow", function (r) {
    var depth = num($("[name=depth]", r)), dens = num($("[name=type]", r)), ice = num($("[name=ice]", r)), rain = num($("[name=rain]", r));
    var design = num($("[name=design]", r)), area = num($("[name=area]", r));
    var snowPsf = depth / 12 * dens, icePsf = ice / 12 * 57, rainPsf = rain * 5.2;
    var psf = snowPsf + icePsf + rainPsf, share = design > 0 ? psf / design : 0;
    set("[data-o=psf]", psf.toFixed(1) + " lb/ft²", r);
    set("[data-o=snowpsf]", snowPsf.toFixed(1) + " lb/ft²", r);
    set("[data-o=icepsf]", icePsf.toFixed(1) + " lb/ft²", r);
    set("[data-o=rainpsf]", rainPsf.toFixed(1) + " lb/ft²", r);
    set("[data-o=share]", design > 0 ? Math.round(share * 100) + "%" : "—", r);
    set("[data-o=total]", area > 0 ? Math.round(psf * area).toLocaleString("en-US") + " lb (" + (psf * area / 2000).toFixed(1) + " tons)" : "—", r);
    var b = $("[data-o=bar]", r); if (b) b.style.width = Math.min(100, share / 1.2 * 100) + "%";
    set("[data-o=msg]", design <= 0 ? "Enter the roof’s design snow load to compare." : share >= 1 ? "This estimate meets or exceeds the design load. Keep people out from under the roof, watch for sagging or cracking, and call a qualified professional." : share >= 0.8 ? "Close to the design load. Watch for warning signs and consider professional snow removal before more snow or rain arrives." : share >= 0.5 ? "A substantial load, but below the design figure. Keep an eye on drifts, valleys and areas below higher roofs." : "Well below the design load for an even layer. Drifts and sliding snow can still concentrate weight in spots.", r);
  });
})();
