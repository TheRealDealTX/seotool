/* Hawaii Insurance Appraiser — site script (nav, drawer, reveal, forms, claim tools). No dependencies. */
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
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 160); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), shade = $(".drawer-bg");
  var openDrawer = function () {
    if (shade) shade.hidden = false;
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    burger.setAttribute("aria-expanded", "true");
    setTimeout(function () { var c = $(".drawer-close", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    if (burger) { burger.setAttribute("aria-expanded", "false"); }
    if (drawer) { drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true"); }
    setTimeout(function () { if (shade && !body.classList.contains("drawer-open")) shade.hidden = true; }, 320);
    if (burger && burger.offsetParent) burger.focus();
  };
  if (burger && drawer) {
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1180) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- header, back-to-top, parallax ---------- */
  var head = $(".head"), toTop = $(".to-top"), px = $$("[data-parallax]"), ticking = false;
  var onScroll = function () {
    var y = window.scrollY;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0)";
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
    el.textContent = "0";
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); }); });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- island tabs (all panels visible without JS) ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
    var tabs = $$("[role=tab]", wrap);
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var p = document.getElementById(t.getAttribute("aria-controls"));
        if (p) p.hidden = !on;
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown" || e.key === "ArrowRight") { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
    select(0);
  });

  /* ---------- glossary search ---------- */
  var gf = $("#gloss-filter"), gc = $("[data-gcount]");
  if (gf) {
    var terms = $$(".gterm");
    var run = function () {
      var q = gf.value.trim().toLowerCase(), n = 0;
      terms.forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) n++; });
      if (gc) gc.textContent = q ? n + " of " + terms.length + " terms match" : terms.length + " terms";
    };
    gf.addEventListener("input", run); run();
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
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Mahalo — your claim details were received. Someone from Hawaii Insurance Appraiser will reach out, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@hawaiiinsuranceappraiser.com\">info@hawaiiinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding helper ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (root) {
      var go = function () { fn(root); };
      root.addEventListener("input", go);
      root.addEventListener("change", go);
      root.addEventListener("click", function (e) { if (e.target.closest("[data-run]")) setTimeout(go, 0); });
      $$(".range input[type=range]", root).forEach(function (r) {
        var out = r.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = r.value + (r.getAttribute("data-unit") || ""); };
        r.addEventListener("input", upd); upd();
      });
      go();
    });
  }

  /* 1. Claim gap & fee estimator (home mini + full tool) */
  function gapCost(r, gain) {
    var ftEl = $("[name=feetype]", r);
    if (!ftEl) return 0;
    var fee = num($("[name=fee]", r)), cost;
    if (ftEl.value === "pct") cost = gain * fee / 100;
    else if (ftEl.value === "hourly") cost = fee * num($("[name=hours]", r));
    else cost = fee;
    return cost + num($("[name=travel]", r)) + num($("[name=umpire]", r)) / 2;
  }
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var gap = Math.max(0, own - ins);
    var award = ins + gap * land, gain = award - ins;
    var cost = gapCost(r, gain), net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    [30, 50, 80].forEach(function (p) { var g = gap * p / 100; set("[data-o=s" + p + "]", money(g - gapCost(r, g)), r); });
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
      var hasFees = !!$("[name=feetype]", r);
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal resolves how much a covered loss costs — with no gap, there is nothing to appraise.";
      else if (hasFees && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready before you call.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
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
    var surface = foot * mult, sq = surface / 100, order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    var metal = $("[name=mat]", r) && $("[name=mat]", r).value === "metal";
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=unitlabel]", metal ? "Panel coverage to order (sq ft)" : "Shingle bundles (3 per square)", r);
    set("[data-o=bundles]", metal ? Math.ceil(order * 100).toLocaleString("en-US") : String(Math.ceil(order * 3)), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge — check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 some carriers begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected, but high-roof charges may still apply on two-story sections.";
  });

  /* 4. Hurricane deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=below]", loss > 0 && loss <= pd ? "This loss falls entirely within the hurricane deductible — no payment would be owed under that deductible." : loss > 0 ? "The loss exceeds the hurricane deductible by " + money(loss - pd) + "." : "Enter an estimated loss to compare payouts.", r);
    var bar = $(".stack", r);
    if (bar) {
      var a = loss > 0 ? Math.min(pd, loss) / loss * 100 : 0;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%";
    }
  });

  /* 5. Claim timeline builder + .ics */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is a self-imposed target." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarps, dry-out and board-up protect the claim and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies count this from the carrier’s written request. Check the date in your letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Confirm the exact number of days in your policy and ask for an extension in writing if repairs are delayed." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Read the Suit Against Us clause. Talk to a Hawaii attorney well before this date." }
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
      if (!plan.length) { var d = $('[data-tool="dates"] [name=dol]'); if (d) d.focus(); return; }
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Hawaii Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:hia-" + ds(p.d) + "-" + i + "@hawaiiinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "hawaii-claim-timeline.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal readiness check */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#2E7D5B" : pct >= 45 ? "#F2B544" : "#6B3FA0"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the documentation a panel expects — the next step is a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before anyone invokes appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
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

  /* 7. Condo deductible share */
  tool("condo", function (r) {
    var loss = num($("[name=loss]", r)), val = num($("[name=value]", r)), dtype = $("[name=dtype]", r).value;
    var ded = num($("[name=ded]", r)), share = num($("[name=share]", r)) / 100;
    var la = num($("[name=la]", r)), d6 = num($("[name=d6]", r));
    var dd = dtype === "pct" ? val * ded / 100 : ded;
    var absorb = Math.min(dd, loss), master = Math.max(0, loss - dd);
    var assess = absorb * share;
    var ho6 = Math.max(0, Math.min(la, assess - d6));
    var oop = assess - ho6;
    set("[data-o=dd]", money(dd), r);
    set("[data-o=absorb]", money(absorb), r);
    set("[data-o=master]", money(master), r);
    set("[data-o=assess]", money(assess), r);
    set("[data-o=ho6]", money(ho6), r);
    set("[data-o=oop]", money(oop), r);
    var msg;
    if (!loss) msg = "Enter the building loss to see how the deductible could be shared.";
    else if (loss <= dd) msg = "The whole loss sits inside the master deductible, so the master policy would pay nothing and the association bears all of it.";
    else if (assess - d6 > la) msg = "Your assessment is higher than your loss assessment limit plus its deductible. Ask your agent whether a higher limit is available.";
    else msg = "Your HO-6 loss assessment coverage appears large enough for this scenario. Confirm it applies to deductible assessments.";
    set("[data-o=cmsg]", msg, r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
