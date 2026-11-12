/* New Jersey Insurance Appraiser — site script: nav, drawer, effects, forms and claim tools.
   No dependencies. Every tool runs in the browser; nothing is stored or sent. */
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
  document.documentElement.classList.add("js");

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function (except) {
    $$(".menu li.open").forEach(function (o) {
      if (o === except) return;
      o.classList.remove("open");
      var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false");
    });
  };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    var open = function () { closeDrops(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    var close = function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); if (li.classList.contains("open")) close(); else open(); });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); open(); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(close, 180); });
    li.addEventListener("focusout", function (e) { if (!li.contains(e.relatedTarget)) close(); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim");
  var isOpen = function () { return body.classList.contains("drawer-open"); };
  var openDrawer = function () {
    if (!drawer) return;
    if (scrim) scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function (refocus) {
    if (!drawer || !isOpen()) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    if (burger) { burger.setAttribute("aria-expanded", "false"); if (refocus) burger.focus(); }
    setTimeout(function () { if (!isOpen() && scrim) scrim.hidden = true; }, 340);
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1180) closeDrawer(false); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(true); } });

  /* ---------- scroll effects: header, progress, back-to-top, parallax, process fill ---------- */
  var head = $(".head"), bar = $(".progress span"), toTop = $(".to-top");
  var px = $$("[data-parallax]");
  var steps = $(".steps"), fill = steps ? $(".steps-fill", steps) : null, stepEls = steps ? $$(".step", steps) : [];
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight, h = document.documentElement.scrollHeight - vh;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - vh / 2) * -k).toFixed(1) + "px,0)";
    });
    if (steps) {
      var sr = steps.getBoundingClientRect(), mid = vh * 0.62;
      var pct = Math.max(0, Math.min(1, (mid - sr.top) / sr.height));
      if (fill) fill.style.height = Math.max(0, pct * (sr.height - 20)) + "px";
      stepEls.forEach(function (s) { s.classList.toggle("on", s.getBoundingClientRect().top < mid); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    if (el.getAttribute("data-done")) return;
    el.setAttribute("data-done", "1");
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1500;
    if (reduce) { el.textContent = end.toLocaleString("en-US"); return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))).toLocaleString("en-US"); if (p < 1) requestAnimationFrame(step); };
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); }); });
  var targets = $$(".rv, .rv-l, .rv-r, .ledger");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.08, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(reveal); }

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) {
    var terms = $$(".gterm"), cnt = $("[data-gcount]"), none = $(".gnone");
    var filter = function () {
      var q = gf.value.trim().toLowerCase(), shown = 0;
      terms.forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) shown++; });
      if (cnt) cnt.textContent = q ? shown + " of " + terms.length + " terms" : terms.length + " terms";
      if (none) none.hidden = shown > 0;
    };
    gf.addEventListener("input", filter); filter();
  }

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); });
      if (bad.length) { msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      var label = btn.innerHTML; btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and someone from New Jersey Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error("send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@newjerseyinsuranceappraiser.com\">info@newjerseyinsuranceappraiser.com</a>."; msg.classList.add("err"); })
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
  var widths = function (stack, parts, total) {
    if (!stack) return;
    var s = stack.children;
    parts.forEach(function (v, i) { if (s[i]) s[i].style.width = (total > 0 ? Math.max(0, v) / total * 100 : 0) + "%"; });
  };

  /* 1. Claim gap & net recovery estimator (home mini + full tool) */
  var gapCost = function (r, gain) {
    var ft = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "none";
    var fee = num($("[name=fee]", r)), rate = num($("[name=rate]", r));
    var cost = ft === "pct" ? Math.max(0, gain) * fee / 100 : ft === "hourly" ? fee * rate : ft === "flat" ? fee : 0;
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    if (useUmp) cost += num($("[name=umpire]", r)) / 2;
    return cost;
  };
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var gap = Math.max(0, own - ins);
    var gain = gap * land, award = ins + gain;
    var cost = gapCost(r, gain), net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    [30, 55, 80].forEach(function (p) { var g = gap * p / 100; set("[data-o=s" + p + "]", money(g - gapCost(r, g)), r); });
    widths($(".stack", r), [ins, net, Math.min(cost, gain)], Math.max(own, award, 1));
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal settles how much a covered loss costs, so with no gap there’s nothing to appraise.";
      else if ($("[name=feetype]", r) && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. ACV & holdback calculator */
  tool("dep", function (r) {
    var rows = $$("tbody tr", r), rcv = 0, dep = 0;
    var cap = (num($("[name=cap]", r)) || 80) / 100;
    var lab = num($("[name=labor]", r)) / 100;
    rows.forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c * (1 - lab);
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep;
    var first = Math.max(0, acv - ded);
    var total = nonrec ? first : Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(total - first), r);
    set("[data-o=total]", money(total), r);
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
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var layers = num($("[name=layers]", r)) || 1;
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=tear]", (sq * layers).toFixed(2), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var msg = pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge. Check that the carrier’s estimate includes it." : pitch === 7 ? "At 7/12 some carriers begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected.";
    if (layers > 1) msg += " With " + layers + " layers, tear-off should be priced for every layer.";
    set("[data-o=steep]", msg, r);
  });

  /* 4. Hurricane / windstorm deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), min = num($("[name=min]", r));
    var flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var trig = ($("[name=trig]:checked", r) || {}).value !== "no";
    var hd = Math.max(covA * pct / 100, min);
    var applies = trig ? hd : flat;
    set("[data-o=hd]", money(hd), r);
    set("[data-o=pd]", money(applies), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - hd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, loss - flat) - Math.max(0, loss - hd)), r);
    var t;
    if (loss <= 0) t = "Enter an estimated loss to compare payments.";
    else if (trig && loss <= hd) t = "This loss falls entirely within the hurricane deductible, so no claim payment would be owed under it.";
    else if (trig) t = "With the hurricane deductible, the policy would pay about " + money(loss - hd) + ".";
    else t = "If the trigger isn’t met, the ordinary deductible applies and the policy would pay about " + money(Math.max(0, loss - flat)) + ".";
    set("[data-o=below]", t, r);
    if (loss > 0) widths($(".stack", r), [Math.min(applies, loss), Math.max(0, loss - applies)], loss);
  });

  /* 5. Claim calendar builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, dem = $("[name=dem]", r).value;
    var list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li>"; plan = []; return; }
    var mk = function (iso) { return new Date(iso + "T12:00:00"); };
    var base = mk(d0);
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(base, num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is your own target." },
      { d: add(base, num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarps, drying and board-up protect the property and are usually reimbursable." },
      { d: add(base, num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies give 60 days, often counted from the carrier’s request. Check your letter." },
      { d: add(base, num($("[name=rcd]", r))), t: "Replacement cost notice or repair window", n: "Some policies require notice within 180 days that you intend to claim replacement cost. Confirm your form." },
      { d: add(base, num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Many New Jersey policies say 12 months from the loss. Talk to an attorney well before this date." }
    ];
    if (dem) {
      var dd = mk(dem), ap = num($("[name=appr]", r)) || 20;
      plan.push({ d: dd, t: "Appraisal demanded", n: "Date the written appraisal demand was made." });
      plan.push({ d: add(dd, ap), t: "Name your appraiser", n: "Commonly within 20 days of the demand under standard-fire-policy wording." });
      plan.push({ d: add(dd, ap + 15), t: "Umpire chosen (or ask a judge)", n: "The appraisers commonly have 15 days to agree on an umpire." });
    }
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
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//New Jersey Insurance Appraiser//Claim Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:nja-" + ds(p.d) + "-" + i + "@newjerseyinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "nj-claim-deadlines.ics";
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
        var yes = $(".yes", li).getAttribute("aria-pressed") === "true";
        var no = $(".no", li).getAttribute("aria-pressed") === "true";
        if (yes) got += w;
        if (yes || no) answered++;
        if (no) todo.push(li.getAttribute("data-fix"));
      });
      var pct = Math.round(got / max * 100);
      set("[data-o=score]", answered ? pct : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#2E7D4F" : pct >= 45 ? "#E9AE45" : "#1F1606"; }
      var verdict = !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the documentation a panel expects. Next step: a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each one weakens your number if it’s missing." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.";
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

  /* 7. Fallen tree coverage */
  tool("tree", function (r) {
    var trees = Math.max(0, Math.round(num($("[name=trees]", r))));
    var hit = Math.min(trees, Math.max(0, Math.round(num($("[name=hit]", r)))));
    var cost = num($("[name=cost]", r)), struct = num($("[name=struct]", r));
    var per = num($("[name=per]", r)), occ = num($("[name=occ]", r)), ded = num($("[name=ded]", r));
    var all = $("[name=all]", r) && $("[name=all]", r).checked;
    var elig = all ? trees : hit;
    var rem = trees * cost;
    var cov = Math.min(elig * Math.min(cost, per), occ);
    var oop = rem - cov;
    var snet = Math.max(0, struct - ded);
    var pay = snet + cov;
    set("[data-o=elig]", String(elig), r);
    set("[data-o=rem]", money(rem), r);
    set("[data-o=cov]", money(cov), r);
    set("[data-o=oop]", money(oop), r);
    set("[data-o=snet]", money(snet), r);
    set("[data-o=pay]", money(pay), r);
    var youPay = oop + Math.min(ded, struct);
    widths($(".stack", r), [snet, cov, youPay], snet + cov + youPay);
    var t;
    if (!trees) t = "Enter the number of trees down to see how debris limits apply.";
    else if (oop > cov && oop > 0) t = "Most of the tree removal bill falls outside the debris limits. Ask the tree service for an itemized invoice that separates removal from the structure and hauling from the yard.";
    else t = "The debris limits cover most of the tree removal at these inputs. Check how your carrier applies the per-storm limit.";
    set("[data-o=tmsg]", t, r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
