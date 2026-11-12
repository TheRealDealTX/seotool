/* Missouri Insurance Appraiser — site script: nav, drawer, effects, forms and the seven claim tools. No dependencies.
   Everything runs in the browser and nothing is stored. */
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
  var hover = window.matchMedia("(hover: hover)");

  /* ---------- desktop dropdowns ---------- */
  var closeDd = function () { $$(".nav-l li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-dd]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".nav-l [data-dd]").forEach(function (btn) {
    var li = btn.parentElement, t;
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var was = li.classList.contains("open");
      closeDd();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!hover.matches) return; clearTimeout(t); closeDd(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover.matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".nav-l")) closeDd(); });

  /* ---------- mobile drawer (rendered outside the fixed header) ---------- */
  var drawer = $("#drawer"), opener = $(".menu-btn"), scrim = $(".scrim"), hideT;
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    clearTimeout(hideT);
    if (scrim) scrim.hidden = false;
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    opener.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function (refocus) {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    opener.setAttribute("aria-expanded", "false");
    hideT = setTimeout(function () { if (scrim && !isOpen()) scrim.hidden = true; }, 340);
    if (refocus) opener.focus();
  };
  if (opener && drawer) {
    opener.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(true); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(false); }); });
    $$(".acc", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") === "true";
        $$(".acc", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", open ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1180) closeDrawer(false); });
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeDd(); closeDrawer(true); } });

  /* ---------- solid masthead, back-to-top, parallax ---------- */
  var mast = $(".mast"), toTop = $(".totop");
  var px = reduce ? [] : $$("[data-parallax]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    if (mast) mast.classList.toggle("solid", y > 40);
    if (toTop) toTop.classList.toggle("show", y > 800);
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

  /* ---------- staggered reveal + counters + season bars ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  $$(".sgrid,.towns,.tgrid,.ngrid,.mosaic,.ledger,.mapgrid").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  $$(".season .srow").forEach(function (row, i) { $$("i", row).forEach(function (c, j) { c.style.transitionDelay = (i * 0.06 + j * 0.025) + "s"; }); });
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.12, rootMargin: "0px 0px -30px 0px" });
    $$(".rv, .season").forEach(function (el) { io.observe(el); });
  } else { $$(".rv, .season").forEach(reveal); }

  /* ---------- glossary search ---------- */
  var gq = $("#gloss-q"), gc = $("[data-gcount]");
  if (gq) gq.addEventListener("input", function () {
    var q = gq.value.trim().toLowerCase(), n = 0;
    $$(".gloss .term").forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
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
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your details arrived, and someone from Missouri Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@missouriinsuranceappraiser.com\">info@missouriinsuranceappraiser.com</a>."; msg.classList.add("err"); })
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
      $$(".slide input[type=range]", root).forEach(function (r) {
        var out = r.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = r.value + (r.getAttribute("data-unit") || ""); };
        r.addEventListener("input", upd); upd();
      });
      run();
    });
  }
  /* add / remove rows (depreciation table) */
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (ev) {
      if (ev.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr);
      }
      var x = ev.target.closest(".rm");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });
  var bars = function (root, parts, total) {
    var b = $(".bar", root); if (!b) return;
    var t = Math.max(total, 1);
    parts.forEach(function (v, i) { if (b.children[i]) b.children[i].style.width = (Math.max(0, v) / t * 100) + "%"; });
  };

  /* 1. Award & net payout estimator (also the home mini check) */
  tool("payout", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var full = !!$("[name=fee]", r);
    var ded = num($("[name=deduct]", r)), paid = num($("[name=paid]", r));
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var at = function (share) {
      var gain = gap * share, award = ins + gain;
      var cost = full ? (feeType === "pct" ? gain * fee / 100 : fee) + (useUmp ? ump / 2 : 0) : 0;
      var owed = Math.max(0, award - ded - paid);
      return { gain: gain, award: award, cost: cost, owed: owed, net: owed - cost };
    };
    var o = at(land);
    set("[data-o=gap]", money(gap), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=award]", money(o.award), r);
    set("[data-o=gain]", money(o.gain), r);
    set("[data-o=afterded]", money(Math.max(0, o.award - ded)), r);
    set("[data-o=owed]", money(o.owed), r);
    set("[data-o=cost]", money(o.cost), r);
    set("[data-o=net]", money(o.net), r);
    set("[data-o=s25]", money(at(0.25).net), r);
    set("[data-o=s50]", money(at(0.5).net), r);
    set("[data-o=s75]", money(at(0.75).net), r);
    bars(r, [ins, o.net, Math.min(o.cost, Math.max(o.owed, 0))], Math.max(own, o.award, 1));
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the amount in dispute.";
      else if (gap <= 0) t = "Your figure isn’t higher than the insurer’s. Appraisal settles what a covered loss costs; with no gap there’s nothing to appraise.";
      else if (full && o.net <= 0) t = "At these inputs, appraisal costs could swallow the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready. Figures are illustrative.";
      m.textContent = t;
    }
  });

  /* 2. Depreciation & recovery */
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
    var acv = rcv - dep, first = Math.max(0, acv - ded), total = nonrec ? first : Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(total - first), r);
    set("[data-o=total]", money(total), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
  });

  /* 3. Roof measurement */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100, layers = num($("[name=layers]", r)) || 1;
    var surface = foot * mult, sq = surface / 100, order = Math.ceil(sq * (1 + waste) * 3) / 3, price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", order.toFixed(2), r);
    set("[data-o=bundles]", String(Math.round(order * 3)), r);
    set("[data-o=tear]", layers > 1 ? (sq * (layers - 1)).toFixed(2) + " sq" : "None", r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software usually adds steep-roof labor. Check that the insurer’s estimate includes it." : pitch === 7 ? "At 7/12 some estimates begin to apply steep charges. Confirm how yours treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.", r);
  });

  /* 4. Wind & hail percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    var tb = $("[data-o=table]", r);
    if (tb) tb.innerHTML = [0.5, 1, 2, 3, 5].map(function (p) {
      var d = covA * p / 100;
      return '<tr' + (p === pct ? ' class="cur"' : "") + "><td>" + p + "%</td><td>" + money(d) + "</td><td>" + money(Math.max(0, loss - d)) + "</td></tr>";
    }).join("");
    set("[data-o=below]", !loss ? "Enter an estimated loss to compare payments." : loss <= pd ? "This loss sits entirely inside the percentage deductible, so nothing would be paid under it. Figures are illustrative." : "The loss is " + money(loss - pd) + " above the percentage deductible. Figures are illustrative.", r);
    if (loss > 0) bars(r, [Math.min(pd, loss), Math.max(0, loss - pd)], loss);
  });

  /* 5. Claim calendar builder + .ics */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    var suitDays = Math.round(num($("[name=suit]", r)) * 365.25);
    plan = [
      { d: add(base, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you safely can; this target is your own." },
      { d: add(base, num($("[name=mitig]", r))), t: "Temporary repairs done, receipts saved", n: "Tarps, drying and board-up protect the property and are usually part of the claim." },
      { d: add(base, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Often counted from the insurer’s written request instead. Check your letter." },
      { d: add(base, num($("[name=rcd]", r))), t: "Holdback (depreciation) claim window closes", n: "Finish repairs and ask for withheld depreciation before the deadline in your policy." },
      { d: add(base, suitDays), t: "Suit-limitation date from your entry", n: "Based on the period you entered. Talk with a Missouri attorney well before this date." }
    ];
    var dem = $("[name=dem]", r).value;
    if (dem) plan.push({ d: add(new Date(dem + "T12:00:00"), num($("[name=appr]", r))), t: "Name your appraiser (from the demand date)", n: "Many appraisal clauses set this window in days after the written demand. Confirm your policy’s wording." });
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
      if (!plan.length) { var d = $("[name=dol]"); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Missouri Insurance Appraiser//Claim Calendar Builder//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:moia-" + ds(p.d) + "-" + i + "@missouriinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "missouri-claim-calendar.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal readiness score */
  $$('[data-tool="ready"]').forEach(function (r) {
    var items = $$(".qs li", r);
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1f7a80" : pct >= 45 ? "#c98a3d" : "#b5652b"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before demanding appraisal; each one weakens your number." : "Not ready yet. Demanding appraisal now risks a weak award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) { ul.innerHTML = ""; (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.innerHTML = t; ul.appendChild(li); }); }
      set("[data-o=count]", answered + " / " + items.length + " answered", r);
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

  /* 7. Roof repair-or-replace splitter */
  tool("rr", function (r) {
    var total = 0, hit = 0, visits = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var s = num($("[name=size]", tr)), h = Math.min(num($("[name=hit]", tr)), s);
      total += s; hit += h; if (h > 0) visits++;
      var o = $("[data-o=share]", tr); if (o) o.textContent = s ? Math.round(h / s * 100) + "%" : "0%";
    });
    var rep = num($("[name=rep]", r)), nw = num($("[name=new]", r)), min = num($("[name=min]", r)), ded = num($("[name=ded]", r));
    var nomatch = $("[name=nomatch]", r).checked;
    var repair = Math.max(hit * rep, visits ? min : 0), full = total * nw, diff = full - repair;
    var share = total ? hit / total : 0;
    set("[data-o=total]", total.toFixed(1) + " sq", r);
    set("[data-o=hitall]", hit.toFixed(1) + " sq (" + Math.round(share * 100) + "%)", r);
    set("[data-o=repair]", money(repair), r);
    set("[data-o=full]", money(full), r);
    set("[data-o=diff]", money(diff), r);
    set("[data-o=reppay]", money(Math.max(0, repair - ded)), r);
    set("[data-o=fullpay]", money(Math.max(0, full - ded)), r);
    bars(r, [Math.min(repair, full), Math.max(0, diff)], Math.max(full, repair));
    var t;
    if (!total) t = "Enter slope sizes to compare the two scopes.";
    else if (!hit) t = "No damaged squares entered yet.";
    else if (nomatch) t = "With no matching shingles available, a repair leaves mismatched patches. How far your policy addresses matching depends on its wording; it’s a frequent appraisal issue. Illustrative only.";
    else if (repair >= full * 0.6 || share >= 0.4) t = "Damage is spread widely enough that the repair scope approaches a full roof. That’s a common point of disagreement worth documenting carefully. Illustrative only.";
    else t = "Damage is limited, so a repair scope may be reasonable if repairs can be done properly and materials match. Illustrative only.";
    set("[data-o=msg]", t, r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
