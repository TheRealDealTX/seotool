/* Maine Insurance Appraiser — site script: navigation, effects, lead forms and claim tools. No dependencies. */
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
  var closeDrops = function (except) {
    $$(".has-drop.open").forEach(function (li) { if (li === except) return; li.classList.remove("open"); $(".drop-btn", li).setAttribute("aria-expanded", "false"); });
  };
  $$(".has-drop").forEach(function (li) {
    var btn = $(".drop-btn", li), t;
    var open = function () { closeDrops(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); if (li.classList.contains("open")) closeDrops(); else open(); });
    li.addEventListener("mouseenter", function () { if (!matchMedia("(hover: hover)").matches) return; clearTimeout(t); open(); });
    li.addEventListener("mouseleave", function () { if (!matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { closeDrops(); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger");
  var lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    body.classList.add("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (burger && drawer) {
    burger.addEventListener("click", function (e) { e.preventDefault(); openDrawer(); });
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function (e) { e.preventDefault(); closeDrawer(); }); });
    $$(".drawer-nav a, .drawer-foot a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(); }); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1020) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- solid header, back-to-top, parallax ---------- */
  var hdr = $(".hdr"), toTop = $(".to-top"), px = $$("[data-parallax]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    if (hdr) hdr.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var box = el.parentElement.parentElement.getBoundingClientRect();
      if (box.bottom < 0 || box.top > innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      var shift = (box.top + box.height / 2 - innerHeight / 2) * -k, cap = box.height * 0.28;
      el.style.transform = "translate3d(0," + Math.max(-cap, Math.min(cap, shift)).toFixed(1) + "px,0)";
    });
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1400); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0"; requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  var targets = $$(".rv, .counts");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        if (en.target.classList.contains("counts")) $$("[data-count]", en.target).forEach(count);
        io.unobserve(en.target);
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- region rail ---------- */
  $$(".rail-wrap").forEach(function (w) {
    var rail = $(".rail", w);
    $$("[data-rail]", w).forEach(function (b) {
      b.addEventListener("click", function () {
        var card = $(".rcard", rail), dx = card ? card.getBoundingClientRect().width + 20 : 320;
        rail.scrollBy({ left: dx * parseInt(b.getAttribute("data-rail"), 10), behavior: reduce ? "auto" : "smooth" });
      });
    });
  });

  /* ---------- glossary search ---------- */
  var gq = $("#gloss-q");
  if (gq) gq.addEventListener("input", function () {
    var q = gq.value.trim().toLowerCase(), n = 0;
    $$(".gterm").forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
    set("[data-gcount]", n + (n === 1 ? " term" : " terms"));
    var none = $(".gnone"); if (none) none.hidden = n > 0;
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      $$("[required]", form).forEach(function (f) { f.setAttribute("aria-invalid", bad.indexOf(f) > -1 ? "true" : "false"); });
      if (bad.length) { msg.textContent = "Please fill in the required fields and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details arrived, and someone from Maine Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else throw new Error("send");
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@maineinsuranceappraiser.com\">info@maineinsuranceappraiser.com</a>."; msg.classList.add("err"); })
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
  var iso = function (d) { var z = function (n) { return (n < 10 ? "0" : "") + n; }; return d.getFullYear() + "-" + z(d.getMonth() + 1) + "-" + z(d.getDate()); };
  var fmtDate = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };

  /* 1. Settlement gap projector (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var costAt = function (gain) { return (feeType === "pct" ? gain * fee / 100 : fee) + (useUmp ? ump / 2 : 0); };
    var award = ins + gap * land, gain = award - ins, cost = $("[name=fee]", r) ? costAt(gain) : 0, net = gain - cost;
    set("[data-o=gap]", money(gap), r); set("[data-o=award]", money(award), r); set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r); set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    var stack = $(".stack", r);
    if (stack) { var total = Math.max(own, award, 1), s = stack.children; s[0].style.width = (ins / total * 100) + "%"; s[1].style.width = (Math.max(0, net) / total * 100) + "%"; s[2].style.width = (Math.min(cost, gain) / total * 100) + "%"; }
    var sc = $("[data-o=scen]", r);
    if (sc) sc.innerHTML = [0.25, 0.5, 0.75].map(function (k) { var a = ins + gap * k, g = a - ins, n = g - costAt(g); return "<tr><td>" + (k * 100) + "% of gap</td><td>" + money(a) + "</td><td>" + money(n) + "</td></tr>"; }).join("");
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the amount in dispute.";
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal decides what a covered loss costs; with no gap there’s nothing to appraise.";
      else if ($("[name=fee]", r) && net <= 0) t = "At these inputs the costs could swallow the whole increase. A line-item estimate review or a documented supplement is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The amount in dispute is large enough that appraisal may be worth discussing. Have both itemized estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. Depreciation & holdback */
  tool("dep", function (r) {
    var rows = $$("tbody tr", r), rcv = 0, dep = 0;
    var cap = num($("[name=cap]", r)) / 100 || 0.8;
    rows.forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep;
    var first = Math.max(0, acv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", nonrec ? money(0) : money(Math.min(dep, Math.max(0, rcv - ded) - first)), r);
    set("[data-o=total]", money(nonrec ? first : Math.max(0, rcv - ded)), r);
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
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), ohIn = num($("[name=oh]", r)), oh = ohIn / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100, surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    // Ice barrier: from the eave edge to 24 in. inside the wall line, measured along the slope, in 36 in. courses.
    var need = (ohIn + 24) / 12 * mult, courses = Math.max(1, Math.ceil(need / 3));
    var eave = mode === "dims" ? 2 * (L + 2 * oh) : 2 * Math.sqrt(foot * 1.6);
    var iwArea = courses * 3 * eave;
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=deg]", (Math.atan(pitch / 12) * 180 / Math.PI).toFixed(1) + "°", r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=iw]", courses + (courses === 1 ? " course" : " courses"), r);
    set("[data-o=iwa]", Math.round(iwArea).toLocaleString("en-US") + " sq ft / " + Math.ceil(iwArea / 200) + " rolls", r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software usually adds steep-roof labor. Check that the carrier’s estimate includes it, along with the full ice-barrier area." : pitch >= 7 ? "At 7/12 some carriers begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge isn’t usually expected, but the ice barrier still is.", r);
  });

  /* 4. Percentage deductible checker */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=need]", money(pd), r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payments." : loss <= pd ? "This loss sits entirely inside the percentage deductible, so no payment would be owed under it." : "The loss exceeds the percentage deductible by " + money(loss - pd) + ".", r);
    var bar = $(".stack", r);
    if (bar && loss > 0) { var a = Math.min(pd, loss) / loss * 100; bar.children[0].style.width = a + "%"; bar.children[1].style.width = (100 - a) + "%"; }
  });

  /* 5. Claim date tracker */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    plan = [
      { d: add(base, num($("[name=notice]", r))), t: "Report the claim (target)", n: "Policies require prompt notice. Report as soon as you reasonably can." },
      { d: add(base, num($("[name=mitig]", r))), t: "Temporary repairs done, receipts saved", n: "Tarps, heat, water extraction and board-up protect the claim and are usually reimbursable." },
      { d: add(base, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often counted from the carrier’s written request. Check the date in its letter." },
      { d: add(today, num($("[name=appr]", r))), t: "Name your appraiser (if appraisal is demanded today)", n: "Many appraisal clauses give each side about 20 days after a written demand." },
      { d: add(base, num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Finish repairs and claim the holdback within the time your policy allows." },
      { d: add(base, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Read the Suit Against Us condition and talk with a Maine attorney well before this date." }
    ].sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmtDate(p.d) + "<em>" + badge + "</em></b><strong>" + p.t + "</strong><br><span>" + p.n + "</span></li>";
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var d = $('[data-tool="dates"] [name=dol]'); if (d) d.focus(); return; }
      var ds = function (d) { return iso(d).replace(/-/g, ""); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/([,;])/g, "\\$1"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Maine Insurance Appraiser//Claim Date Tracker//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:mia-" + ds(p.d) + "-" + i + "@maineinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n") + "\r\n"], { type: "text/calendar" }));
      a.download = "maine-claim-dates.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal file strength test */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#2f7a54" : pct >= 45 ? "#e2683c" : "#133458"; }
      var verdict = !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the documentation an appraisal panel expects — the next step is a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you invoke appraisal; each one weakens your number if it’s missing." : "Not ready yet. Invoking appraisal now risks locking in a low award. Work through the list below first.";
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

  /* 7. Seasonal camp vacancy check */
  $$('[data-tool="camp"] [name=found]').forEach(function (el) { if (!el.value) el.value = iso(new Date()); });
  $$('[data-tool="camp"] [name=last]').forEach(function (el) { if (!el.value) { var d = new Date(); d.setDate(d.getDate() - 75); el.value = iso(d); } });
  tool("camp", function (r) {
    var last = $("[name=last]", r).value, found = $("[name=found]", r).value;
    var th = num($("[name=thresh]", r)), chk = num($("[name=check]", r));
    var heat = $("[name=heat]", r).checked, drain = $("[name=drain]", r).checked, alarm = $("[name=alarm]", r).checked;
    var todo = [], msg;
    if (!last || !found) { set("[data-o=days]", "–", r); set("[data-o=msg]", "Enter both dates to count the unoccupied days.", r); $("[data-o=todo]", r).innerHTML = ""; return; }
    var a = new Date(last + "T12:00:00"), b = new Date(found + "T12:00:00");
    var days = Math.round((b - a) / 864e5);
    if (days < 0) { set("[data-o=days]", "–", r); set("[data-o=msg]", "The date found is before the last stay. Check the dates.", r); $("[data-o=todo]", r).innerHTML = ""; return; }
    var cross = new Date(a); cross.setDate(cross.getDate() + th);
    var margin = th - days;
    set("[data-o=days]", days + (days === 1 ? " day" : " days"), r);
    set("[data-o=cross]", fmtDate(cross), r);
    set("[data-o=margin]", margin >= 0 ? margin + " days left in the window" : Math.abs(margin) + " days past the window", r);
    set("[data-o=gapchk]", chk > 0 ? Math.min(chk, days) + " days" : days + " days (no checks)", r);
    var steps = (heat ? 1 : 0) + (drain ? 1 : 0) + (alarm ? 1 : 0);
    set("[data-o=steps]", steps + " of 3", r);
    if (margin < 0) msg = "The building had been unoccupied longer than the window you chose. Read your policy’s vacancy and unoccupancy wording and any seasonal endorsement closely; some limits may apply, depending on the definitions and the cause of loss.";
    else if (margin <= 14) msg = "You were close to the policy window when the damage was found. Proof of when people were last there, and of heat, will matter.";
    else msg = "The unoccupied period was inside the window you chose. The freeze-protection proof below is still the first thing an adjuster will ask about.";
    if (!heat && !drain) msg += " Neither heat nor a drained system is checked; many policies require one or the other for freezing losses, so gather whatever shows the steps you did take.";
    set("[data-o=msg]", msg, r);
    todo.push("Proof of the last stay: receipts, ferry or toll records, photos, messages.");
    if (heat) todo.push("Fuel delivery slips, propane or oil account history, and electric bills for the period.");
    if (drain) todo.push("Plumber’s winterizing invoice or photos of the shut-off and drained lines.");
    if (alarm) todo.push("Alarm or smart-thermostat logs and alert history around the date of loss.");
    if (chk > 0) todo.push("Dated notes or texts from whoever checked the property every " + chk + " days.");
    else todo.push("Names and dates of anyone who visited, plowed or checked the property.");
    todo.push("Photos of the damage before cleanup, and the mitigation company’s moisture readings.");
    $("[data-o=todo]", r).innerHTML = todo.map(function (t) { return "<li>" + t + "</li>"; }).join("");
  });
})();
