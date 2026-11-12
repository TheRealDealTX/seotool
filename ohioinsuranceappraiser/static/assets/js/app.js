/* Ohio Insurance Appraiser — site script: nav drawer, header, reveal, counters, carousel, forms, claim tools. No dependencies. */
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
  document.documentElement.classList.remove("no-js");
  document.documentElement.classList.add("js");

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function () { $$(".nav li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".nav [data-drop]").forEach(function (btn) {
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
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrollY0 = 0;
  var openDrawer = function () {
    scrollY0 = window.scrollY;
    body.classList.add("drawer-open");
    body.style.top = -scrollY0 + "px";
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function (restore) {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open");
    body.style.top = "";
    if (restore !== false) window.scrollTo({ top: scrollY0, left: 0, behavior: "instant" });
    burger.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    if (restore !== false) burger.focus({ preventScroll: true });
  };
  if (burger && drawer) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") === "true";
        $$(".acc", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- header state, parallax, back-to-top ---------- */
  var head = $(".site-head"), toTop = $(".top-btn"), px = $$("[data-parallax]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    if (head) head.classList.toggle("is-solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0) scale(1.12)";
    });
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var show = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".reveal", g).forEach(function (c, i) { c.style.transitionDelay = (i % 6) * 0.07 + "s"; }); });
  var targets = $$(".reveal, .counters");
  if ("IntersectionObserver" in window && !reduce) {
    body.classList.add("anim");
    var pending = targets.slice();
    var done = function (el) { show(el); io.unobserve(el); pending.splice(pending.indexOf(el), 1); };
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting && pending.indexOf(en.target) > -1) done(en.target); }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
    /* Fast scrolls can jump past an element between frames: reveal anything already above the fold line. */
    var sweep = function () { pending.slice().forEach(function (el) { if (el.getBoundingClientRect().top < window.innerHeight) done(el); }); };
    window.addEventListener("scroll", function () { requestAnimationFrame(sweep); }, { passive: true });
    window.addEventListener("load", sweep);
  } else { targets.forEach(show); }

  /* ---------- region carousel ---------- */
  $$("[data-carousel]").forEach(function (wrap) {
    var track = $(".car-track", wrap), prev = $("[data-prev]", wrap), next = $("[data-next]", wrap);
    if (!track) return;
    var step = function (dir) { var card = track.firstElementChild; var w = card ? card.getBoundingClientRect().width + 20 : 320; track.scrollBy({ left: dir * w, behavior: reduce ? "auto" : "smooth" }); };
    var upd = function () { if (prev) prev.disabled = track.scrollLeft < 8; if (next) next.disabled = track.scrollLeft + track.clientWidth > track.scrollWidth - 8; };
    if (prev) prev.addEventListener("click", function () { step(-1); });
    if (next) next.addEventListener("click", function () { step(1); });
    track.addEventListener("scroll", function () { requestAnimationFrame(upd); }, { passive: true });
    window.addEventListener("resize", upd); upd();
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#lex-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0;
    $$(".lexicon .term").forEach(function (t) {
      var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1;
      t.hidden = !hit; if (hit) shown++;
    });
    set("[data-lex-count]", shown + " of " + $$(".lexicon .term").length + " terms");
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      $$(".bad", form).forEach(function (f) { f.classList.remove("bad"); });
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      var em = $("[name=email]", form);
      if (em && em.value.trim() && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value.trim())) bad.push(em);
      if (bad.length) { bad.forEach(function (f) { f.classList.add("bad"); }); msg.textContent = "Please complete the highlighted fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you — your claim details came through. Someone from Ohio Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "The form didn’t send. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@ohioinsuranceappraiser.com\">info@ohioinsuranceappraiser.com</a>."; msg.classList.add("err"); })
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
      run();
    });
  }

  /* 1. Claim gap & fee estimator: three landing points + break-even */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var feeEl = $("[name=fee]", r), ftEl = $("[name=feetype]", r), umpEl = $("[name=umpire]", r), useEl = $("[name=useump]", r);
    var gap = Math.max(0, own - ins);
    var umpShare = (useEl && useEl.checked && umpEl) ? num(umpEl) / 2 : 0;
    var pctFee = ftEl && ftEl.value === "pct", fee = feeEl ? num(feeEl) : 0;
    var costFor = function (gain) { return feeEl ? (pctFee ? gain * fee / 100 : fee) + umpShare : 0; };
    set("[data-o=gap]", money(gap), r);
    set("[data-o=pct]", ins > 0 && gap > 0 ? Math.round(gap / ins * 100) + "% above the insurer’s figure" : "", r);
    var nets = {};
    [35, 60, 85].forEach(function (p) {
      var gain = gap * p / 100, c = costFor(gain);
      nets[p] = gain - c;
      set("[data-o=a" + p + "]", money(ins + gain), r);
      set("[data-o=c" + p + "]", money(c), r);
      set("[data-o=n" + p + "]", money(gain - c), r);
      var cell = $("[data-o=n" + p + "]", r); if (cell) cell.classList.toggle("neg", gain - c < 0);
    });
    if (feeEl) {
      var be;
      if (gap <= 0) be = "—";
      else if (pctFee) { var f = 1 - fee / 100; be = f <= 0 ? "never" : Math.min(999, Math.ceil(umpShare / (gap * f) * 100)) + "% of the gap"; }
      else { var need = (fee + umpShare) / gap * 100; be = need > 100 ? "above 100% — costs exceed the gap" : Math.ceil(need) + "% of the gap"; }
      set("[data-o=be]", be, r);
    }
    var t;
    if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
    else if (gap <= 0) t = "Your estimate isn’t above the insurer’s. Appraisal decides how much a covered loss costs — with no gap, there’s nothing for a panel to decide.";
    else if (feeEl && nets[60] <= 0) t = "At the middle outcome, appraisal costs would eat the whole increase. A documented supplement or an estimate audit is usually the better first move.";
    else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A well-documented supplement request may close it without formal appraisal.";
    else t = "The disputed amount looks large enough to discuss appraisal. Have both itemized estimates and your photos ready when you call.";
    set("[data-o=msg]", t, r);
  });

  /* 2. RCV / ACV holdback */
  tool("dep", function (r) {
    var cap = (num($("[name=cap]", r)) || 80) / 100, lab = num($("[name=labor]", r)) / 100, rcv = 0, dep = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c * (1 - lab);
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r)), nonrec = $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), total = Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(nonrec ? 0 : total - first), r);
    set("[data-o=total]", money(nonrec ? first : total), r);
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
    var pitch = num($("[name=pitch]", r)), stories = num($("[name=stories]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100, surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=deg]", (Math.atan(pitch / 12) * 180 / Math.PI).toFixed(1) + "°", r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var notes = [];
    notes.push(pitch >= 7 ? "At " + pitch + "/12, look for a steep-roof labor charge on the estimate." : "At " + pitch + "/12 the roof is usually walkable, so no steep charge is expected.");
    if (stories >= 2) notes.push("Slopes two or more stories up commonly carry a high-roof charge as well.");
    set("[data-o=steep]", notes.join(" "), r);
  });

  /* 4. Percentage deductible: compare flat, 1%, 2%, 5% */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=flatd]", money(flat), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    [1, 2, 5].forEach(function (p) { var d = covA * p / 100; set("[data-o=d" + p + "]", money(d), r); set("[data-o=p" + p + "]", money(Math.max(0, loss - d)), r); });
    $$(".scen tbody tr", r).forEach(function (tr, i) { tr.classList.toggle("hl", [0, 1, 2, 5][i] === pct); });
    set("[data-o=below]", !loss ? "Enter an estimated loss to compare payouts." : loss <= pd ? "At " + pct + "%, this loss sits entirely inside the deductible — the policy would pay nothing for it." : "At " + pct + "%, you carry " + money(pd) + " and the policy pays " + money(loss - pd) + " — " + money(pd - flat) + " more out of pocket than the flat deductible.", r);
    var bar = $(".stack", r);
    if (bar) { var a = loss > 0 ? Math.min(pd, loss) / loss * 100 : 0; bar.children[0].style.width = a + "%"; bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%"; }
  });

  /* 5. Ohio claim calendar builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, dm = $("[name=demand]", r).value;
    var list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><strong>Choose your date of loss</strong><span>Your milestones will appear here.</span></li>"; return; }
    var day = function (s, n) { var d = new Date(s + "T12:00:00"); d.setDate(d.getDate() + n); return d; };
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: day(d0, num($("[name=notice]", r))), t: "Report the claim (self-set target)", n: "Policies require prompt notice. Report as soon as you reasonably can." },
      { d: day(d0, num($("[name=mitig]", r))), t: "Finish temporary repairs and keep receipts", n: "Tarping, board-up and water extraction protect the home and the claim." },
      { d: day(d0, num($("[name=pol]", r))), t: "Sworn proof of loss, if requested", n: "Many policies allow 60 days from the insurer’s written request. Count from the request letter." },
      { d: day(d0, num($("[name=rcd]", r))), t: "Depreciation recovery window", n: "Confirm the exact number of days in your policy for finishing repairs and claiming holdback." },
      { d: day(d0, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Many Ohio policies allow one year from the loss. Talk to an Ohio attorney well before this date." }
    ];
    if (dm) {
      var a = num($("[name=appr]", r));
      plan.push({ d: day(dm, a), t: "Name your appraiser (from demand)", n: "Many appraisal clauses give each side about 20 days after a written demand. Check yours." });
      plan.push({ d: day(dm, a + 15), t: "Appraisers agree on an umpire", n: "If they can’t agree in the time the policy allows, either side may ask a court to appoint one." });
    }
    plan.sort(function (x, y) { return x.d - y.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + ' <em>' + badge + '</em></b><strong>' + p.t + '</strong><span>' + p.n + '</span></li>';
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var dol = $("[name=dol]"); if (dol) dol.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Ohio Insurance Appraiser//Claim Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:oia-" + ds(p.d) + "-" + i + "@ohioinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "ohio-claim-calendar.ics";
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1d7a74" : pct >= 45 ? "#d98a2b" : "#c12637"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects to see — the next step is a professional look at the dollar gap." : pct >= 45 ? "Close, but not there yet. Each open item below weakens your number if it’s missing when appraisal starts." : "Not ready. Demanding appraisal now could lock in a low award — work through the list first.", r);
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

  /* 7. Basement backup sublimit */
  tool("backup", function (r) {
    var loss = num($("[name=loss]", r)), cause = $("[name=cause]", r).value, lim = num($("[name=limit]", r)), ded = num($("[name=deduct]", r)), flood = num($("[name=flood]", r));
    var pay = 0, which, cap, msg;
    if (cause === "pipe") { which = "Main homeowners policy"; cap = "Dwelling / contents limits"; pay = Math.max(0, loss - ded); msg = "Sudden discharge from plumbing or an appliance is usually covered by the main policy. Disputes tend to be about scope and price — the kind of question appraisal can settle."; }
    else if (cause === "backup") {
      if (lim > 0) { which = "Water backup endorsement"; cap = money(lim); pay = Math.min(lim, Math.max(0, loss - ded)); msg = loss - ded > lim ? "The loss runs past the endorsement limit by " + money(loss - ded - lim) + ". Appraisal can’t raise a limit, so check the endorsement wording before spending on a dispute." : "The loss fits inside the endorsement limit, so the amount of loss — and any appraisal over it — directly affects what you’re paid."; }
      else { which = "None — backup is typically excluded"; cap = "$0"; pay = 0; msg = "Without a water backup endorsement, sewer and drain backup is usually excluded. Confirm with your declarations page; it’s worth adding at renewal."; }
    }
    else if (cause === "flood") {
      if (flood > 0) { which = "Separate flood policy"; cap = money(flood); pay = Math.min(flood, Math.max(0, loss - ded)); msg = "Homeowners policies exclude flood. Flood policies cover only limited items in basements, so treat this figure as an upper bound."; }
      else { which = "None — flood is excluded"; cap = "$0"; pay = 0; msg = "Surface water and river flooding are excluded from homeowners policies. Only a flood policy (NFIP or private) would respond."; }
    }
    else { which = "None — seepage is commonly excluded"; cap = "$0"; pay = 0; msg = "Slow seepage through foundation walls is usually treated as wear, maintenance or repeated leakage. If a sudden event was involved, document it carefully."; }
    var dedUsed = pay > 0 || (cause === "pipe" || (cause === "backup" && lim > 0) || (cause === "flood" && flood > 0)) ? Math.min(ded, loss) : 0;
    var you = Math.max(0, loss - pay);
    set("[data-o=pay]", money(pay), r);
    set("[data-o=which]", which, r);
    set("[data-o=cap]", cap, r);
    set("[data-o=you]", money(you), r);
    set("[data-o=share]", loss ? Math.round(pay / loss * 100) + "%" : "0%", r);
    set("[data-o=msg]", msg + (num($("[name=mitig]", r)) > 0 && cause === "backup" && lim > 0 ? " Dry-out costs usually count against the same limit." : ""), r);
    var bar = $(".stack", r);
    if (bar && loss > 0) { bar.children[0].style.width = pay / loss * 100 + "%"; bar.children[1].style.width = dedUsed / loss * 100 + "%"; bar.children[2].style.width = Math.max(0, 100 - (pay + dedUsed) / loss * 100) + "%"; }
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
