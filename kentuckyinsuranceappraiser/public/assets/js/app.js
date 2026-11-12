/* Kentucky Insurance Appraiser — site script: navigation, drawer, motion, forms and the free claim tools.
   No dependencies. Everything runs in the browser; tool inputs are never sent or stored. */
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
  var root = document.documentElement, body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  root.classList.add("js");

  /* ---------- desktop menus ---------- */
  var closeMenus = function () {
    $$(".nav-item.open").forEach(function (li) { li.classList.remove("open"); var b = $("button", li); if (b) b.setAttribute("aria-expanded", "false"); });
  };
  $$(".nav-item > button").forEach(function (btn) {
    var li = btn.parentElement, t;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = li.classList.contains("open");
      closeMenus();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!matchMedia("(hover: hover)").matches) return; clearTimeout(t); closeMenus(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav")) closeMenus(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), opener = $(".menu-btn"), scrim = $(".scrim"), lastY = 0;
  var openDrawer = function () {
    lastY = window.scrollY;
    body.classList.add("drawer-open");
    body.style.top = -lastY + "px";
    opener.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function (keep) {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open");
    body.style.top = "";
    if (!keep) window.scrollTo(0, lastY);
    opener.setAttribute("aria-expanded", "false");
    drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true");
    if (!keep) opener.focus();
  };
  if (opener && drawer) {
    opener.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", function () { closeDrawer(); }); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", function () { closeDrawer(true); }); });
    $$(".acc", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") === "true";
        $$(".acc", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); $("#" + o.getAttribute("aria-controls")).hidden = true; });
        b.setAttribute("aria-expanded", open ? "false" : "true");
        $("#" + b.getAttribute("aria-controls")).hidden = open;
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) closeDrawer(true); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeMenus(); closeDrawer(); } });

  /* ---------- scroll: solid header, parallax, timeline fill, back to top ---------- */
  var head = $(".site-head"), toTop = $(".to-top"), px = $$("[data-parallax]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 24);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -k).toFixed(1) + "px,0) scale(1.12)";
    });
    $$(".steps").forEach(function (s) {
      var r = s.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (vh * 0.75 - r.top) / (r.height + vh * 0.25)));
      s.style.setProperty("--fill", p.toFixed(3));
      $$(".step", s).forEach(function (st, i, all) { st.classList.toggle("on", p >= (i + 0.5) / all.length || p >= 0.999); });
    });
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end.toLocaleString("en-US"); return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))).toLocaleString("en-US"); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var show = function (el) { el.classList.add("seen"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { Array.prototype.forEach.call(g.children, function (c, i) { c.style.setProperty("--i", i % 9); }); });
  var targets = $$(".reveal, [data-stagger], .counters");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { show(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(show); }

  /* ---------- glossary search ---------- */
  var gf = $("#term-search");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0;
    $$(".terms > div").forEach(function (row) {
      var hit = !q || row.textContent.toLowerCase().indexOf(q) > -1;
      row.hidden = !hit; if (hit) shown++;
    });
    set("#term-count", shown + (shown === 1 ? " term" : " terms"));
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim() || (f.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value)); });
      if (bad.length) { bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); }); msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you — we received your claim details and will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else throw new Error("send");
        })
        .catch(function () { msg.innerHTML = "The form couldn’t be sent just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@kentuckyinsuranceappraiser.com\">info@kentuckyinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (r) {
      var run = function () { fn(r); };
      r.addEventListener("input", run);
      r.addEventListener("change", run);
      $$(".range input[type=range]", r).forEach(function (rg) {
        var out = rg.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = rg.value + (rg.getAttribute("data-unit") || ""); };
        rg.addEventListener("input", upd); upd();
      });
      r._run = run;
      run();
    });
  }
  var widths = function (stack, parts) { if (!stack) return; parts.forEach(function (w, i) { if (stack.children[i]) stack.children[i].style.width = Math.max(0, w) + "%"; }); };

  /* 1. Appraisal payoff estimator */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = num($("[name=land]", r)) / 100;
    var feeEl = $("[name=fee]", r), full = !!feeEl;
    var pctFee = full && $("[name=feetype]", r).value === "pct";
    var fee = num(feeEl), ump = num($("[name=umpire]", r));
    var useUmp = full && $("[name=useump]", r).checked;
    var gap = Math.max(0, own - ins), gain = gap * land, award = ins + gain;
    var fixed = (pctFee ? 0 : fee) + (useUmp ? ump / 2 : 0);
    var cost = full ? (pctFee ? gain * fee / 100 : fee) + (useUmp ? ump / 2 : 0) : 0;
    var net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    var be = "—";
    if (full && gap > 0) {
      var keep = pctFee ? 1 - fee / 100 : 1;
      var need = keep > 0 ? fixed / (gap * keep) : Infinity;
      be = need <= 0 ? "0% of the gap" : need > 1 ? "Not reachable" : Math.ceil(need * 100) + "% of the gap";
    }
    set("[data-o=breakeven]", be, r);
    var tot = Math.max(own, award, 1);
    widths($(".stack", r), [ins / tot * 100, Math.max(0, net) / tot * 100, Math.min(cost, gain) / tot * 100]);
    var t;
    if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
    else if (gap <= 0) t = "Your number isn’t higher than the carrier’s, so there’s no amount-of-loss gap for appraisal to resolve.";
    else if (full && net <= 0) t = "At these inputs, appraisal costs would eat the whole increase. An estimate review or documented supplement is usually the better first step.";
    else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A well-documented supplement request may close it without formal appraisal.";
    else t = "The disputed amount is large enough that appraisal may be worth a conversation. Have both estimates and your photos ready. (Illustrative only.)";
    set("[data-o=msg]", t, r);
  });

  /* 2. RCV & ACV holdback */
  tool("dep", function (r) {
    var cap = num($("[name=cap]", r)) / 100 || 0.8, rcv = 0, dep = 0;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c;
      rcv += c; dep += d;
      set("[data-o=row]", money(c - d), tr);
    });
    var ded = num($("[name=deduct]", r)), acvOnly = $("[name=nonrec]", r).checked, done = $("[name=done]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded);
    var full = acvOnly ? first : Math.max(0, rcv - ded), held = Math.max(0, full - first);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
    set("[data-o=first]", money(first), r);
    set("[data-o=heldlabel]", done && !acvOnly ? "Released after repairs" : "Held back until repairs", r);
    set("[data-o=held]", money(held), r);
    set("[data-o=total]", money(full), r);
    set("[data-o=msg]", acvOnly ? "ACV-only policy: depreciation isn’t recoverable, so the first check is the whole payment (illustrative)." :
      done ? "With repairs finished and invoiced, the held-back depreciation is typically claimable — check your policy’s notice window." :
      "The holdback is usually paid once repairs are completed and documented, within the time your policy allows.", r);
  });
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (e) {
      if (e.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr); $("input", tr).focus(); r._run();
      }
      var x = e.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r._run(); }
    });
  });

  /* 3. Roof measurement */
  tool("roof", function (r) {
    var m = $("[name=mode]:checked", r), mode = m ? m.value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r)), mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + num($("[name=waste]", r)) / 100);
    var price = num($("[name=price]", r)), car = num($("[name=carrier]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    set("[data-o=vs]", car ? ((order - car >= 0 ? "+" : "−") + Math.abs(order - car).toFixed(2) + " sq (" + Math.round((order - car) / car * 100) + "%)") : "—", r);
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software commonly adds steep-slope labor. Check that the carrier’s estimate includes it." :
      pitch >= 7 ? "At 7/12, some estimates start adding steep-slope charges. Confirm how yours treats this pitch." :
      "A walkable pitch: a steep-slope charge usually isn’t expected.", r);
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=share]", loss > 0 ? Math.min(100, Math.round(pd / loss * 100)) + "%" : "—", r);
    set("[data-o=breakeven]", "Losses under " + money(pd) + " pay nothing", r);
    set("[data-o=below]", loss <= 0 ? "Enter an estimated loss to compare payouts." : loss <= pd ? "This loss sits entirely inside the percentage deductible, so no claim payment would be owed under it." : "The loss is " + money(loss - pd) + " above the percentage deductible.", r);
    if (loss > 0) { var a = Math.min(pd, loss) / loss * 100; widths($(".stack", r), [a, 100 - a]); }
  });

  /* 5. Claim timeline builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, dm = $("[name=demand]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Pick your date of loss</b><span>Milestones appear here.</span></li>"; plan = []; return; }
    var day = function (s, n) { var d = new Date(s + "T12:00:00"); d.setDate(d.getDate() + n); return d; };
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: day(d0, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies ask for prompt notice. Report as soon as you can — this is a self-set target." },
      { d: day(d0, num($("[name=mitig]", r))), t: "Temporary repairs done, receipts saved", n: "Tarps, board-up and water extraction protect the property and are usually part of the claim." },
      { d: day(d0, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies count from the carrier’s written request. Check the date in your letter." },
      { d: day(d0, num($("[name=rcd]", r))), t: "Replacement-cost holdback notice window", n: "Many policies set a window to notify the carrier you intend to claim held-back depreciation. Confirm yours." },
      { d: day(d0, num($("[name=suit]", r))), t: "Policy suit-limitation date (check yours)", n: "Read the Suit Against Us clause and talk with a Kentucky attorney well before this date." }
    ];
    if (dm) {
      var a = num($("[name=appr]", r));
      plan.push({ d: day(dm, a), t: "Name your appraiser (per your policy)", n: "Many policies give each side about 20 days after a written demand. Use your policy’s number." });
      plan.push({ d: day(dm, a + 15), t: "Umpire selection target", n: "Appraisers commonly have about 15 days to agree on an umpire before either side may ask a court to appoint one." });
    }
    plan.sort(function (x, y) { return x.d - y.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + " <em>" + badge + "</em></b><strong>" + p.t + "</strong><span>" + p.n + "</span></li>";
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var dol = $("[name=dol]", btn.closest("[data-tool]")); if (dol) dol.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kentucky Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:kia-" + ds(p.d) + "-" + i + "@kentuckyinsuranceappraiser.com", "DTSTAMP:" + stamp,
          "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "kentucky-claim-timeline.ics";
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
      var bar = $("[data-o=bar]", r);
      if (bar) { bar.style.width = (answered ? pct : 0) + "%"; bar.className = pct >= 75 ? "hi" : pct >= 45 ? "mid" : "lo"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects — the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before demanding appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks a low award. Work through the list below first.", r);
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

  /* 7. Storm tree removal coverage */
  tool("tree", function (r) {
    var n = Math.max(0, Math.floor(num($("[name=trees]", r)))), cost = num($("[name=cost]", r));
    var hit = ($("[name=hit]:checked", r) || {}).value === "yes";
    var per = num($("[name=pertree]", r)), occ = num($("[name=perocc]", r));
    var total = n * cost, capped = n * Math.min(cost, per);
    var covered = hit ? Math.min(capped, occ) : 0, oop = total - covered;
    set("[data-o=total]", money(total), r);
    set("[data-o=capped]", hit ? money(capped) : "$0", r);
    set("[data-o=covered]", money(covered), r);
    set("[data-o=oop]", money(oop), r);
    if (total > 0) widths($(".stack", r), [covered / total * 100, oop / total * 100]);
    set("[data-o=msg]", !hit ? "Many forms don’t pay to remove a tree that fell without hitting a covered structure or blocking a driveway or ramp. Check your wording." :
      covered < capped ? "The per-occurrence limit caps this one. Removing the part of a tree resting on a damaged roof is often handled with the dwelling repair instead. (Illustrative.)" :
      "Within the per-tree and per-occurrence limits shown. Your deductible may still apply to the overall loss. (Illustrative.)", r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
