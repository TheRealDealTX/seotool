/* Vermont Insurance Appraiser — site script (nav, drawer, effects, forms, claim tools). No dependencies. */
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
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector("[data-drop]"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu [data-drop]").forEach(function (btn) {
    var li = btn.parentElement, t;
    var hover = function () { return window.matchMedia("(hover: hover)").matches; };
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = li.classList.contains("open");
      closeDrops();
      if (!was) { li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
    });
    li.addEventListener("mouseenter", function () { if (!hover()) return; clearTimeout(t); closeDrops(); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!hover()) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 160); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger");
  var openDrawer = function () {
    body.classList.add("drawer-open", "lock");
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-close", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    if (burger) { burger.setAttribute("aria-expanded", "false"); }
    if (drawer) { drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true"); }
    if (burger && window.innerWidth <= 1140) burger.focus({ preventScroll: true });
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1140) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, progress, back-to-top, parallax, process fill ---------- */
  var head = $(".head"), bar = $(".progress"), toTop = $(".to-top"), px = $$("[data-parallax]"), proc = $(".steps");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = root.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("solid", y > 40);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((r.top + r.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0)";
    });
    if (proc) {
      var pr = proc.getBoundingClientRect(), mid = window.innerHeight * 0.55;
      var fill = $(".fill", proc);
      var pct = Math.max(0, Math.min(1, (mid - pr.top) / pr.height));
      if (fill) fill.style.height = (pct * (pr.height - 16)) + "px";
      $$("li", proc).forEach(function (s) { s.classList.toggle("on", s.getBoundingClientRect().top < mid); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal ---------- */
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- season tabs ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
    var tabs = $$("[role=tab]", wrap);
    var select = function (i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j, p = $("#" + t.getAttribute("aria-controls"));
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        p.hidden = !on;
        if (on) { p.classList.remove("anim"); void p.offsetWidth; p.classList.add("anim"); }
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown" || e.key === "ArrowRight") { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), any = false;
    $$(".glossary dt").forEach(function (dt) {
      var dd = dt.nextElementSibling;
      var hit = !q || (dt.textContent + " " + dd.textContent).toLowerCase().indexOf(q) > -1;
      dt.hidden = dd.hidden = !hit;
      if (hit) any = true;
    });
    var none = $(".gloss-none"); if (none) none.hidden = any;
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please fill in the required fields and tick the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details arrived, and someone from Vermont Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "The form didn’t send. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@vermontinsuranceappraiser.com\">info@vermontinsuranceappraiser.com</a>."; msg.classList.add("err"); })
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

  /* 1. Claim gap & fee estimator (full + mini) */
  var gapCost = function (gain, feeType, fee, rate, ump, useUmp) {
    var c = feeType === "pct" ? gain * fee / 100 : feeType === "hourly" ? fee * rate : fee;
    return c + (useUmp ? ump / 2 : 0);
  };
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var full = !!$("[name=land]", r);
    var land = full ? num($("[name=land]", r)) / 100 : 0;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r)), rate = num($("[name=rate]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    $$("[data-show]", r).forEach(function (el) { el.hidden = el.getAttribute("data-show") !== feeType; });
    var gap = Math.max(0, own - ins);
    var award = ins + gap * land, gain = award - ins;
    var cost = gapCost(gain, feeType, fee, rate, ump, useUmp), net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    set("[data-o=award]", money(award), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, award, 1), s = stack.children;
      s[0].style.width = (ins / total * 100) + "%";
      s[1].style.width = (Math.max(0, net) / total * 100) + "%";
      s[2].style.width = (Math.min(cost, gain) / total * 100) + "%";
    }
    var sc = $("[data-o=scen]", r);
    if (sc) sc.innerHTML = [0.3, 0.6, 0.9].map(function (k) {
      var a = ins + gap * k, g = a - ins, n = g - gapCost(g, feeType, fee, rate, ump, useUmp);
      return "<tr><td>" + Math.round(k * 100) + "% of gap</td><td>" + money(a) + "</td><td>" + money(n) + "</td></tr>";
    }).join("");
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the amount in dispute.";
      else if (gap <= 0) t = "Your number is not higher than the carrier’s. Appraisal settles how much a covered loss costs, so with no gap there is nothing to appraise.";
      else if (full && net <= 0) t = "At these inputs, appraisal costs could use up the whole increase. An estimate review or a documented supplement request is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The amount in dispute is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. RCV / ACV holdback */
  tool("dep", function (r) {
    var rows = $$("tbody tr", r), rcv = 0, dep = 0;
    var cap = (num($("[name=cap]", r)) || 80) / 100;
    var labor = num($("[name=labor]", r)) / 100;
    rows.forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, age / life) * c * (1 - labor);
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded), totalPay = Math.max(0, rcv - ded);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(nonrec ? 0 : Math.max(0, totalPay - first)), r);
    set("[data-o=total]", money(nonrec ? first : totalPay), r);
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
    var eaveLen = mode === "dims" ? 2 * (L + 2 * oh) : 2 * Math.sqrt(foot * 1.6);
    var ice = num($("[name=ice]", r)) * eaveLen;
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3)), r);
    set("[data-o=icearea]", Math.round(ice).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge. Check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 some carriers start applying steep charges. Check how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge is not usually expected.";
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pd) - Math.min(loss, flat))), r);
    set("[data-o=breakeven]", money(pd), r);
    set("[data-o=below]", loss <= pd && loss > 0 ? "This loss sits entirely inside the percentage deductible, so no payment would be owed under it." : loss > 0 ? "The loss is " + money(loss - pd) + " above the percentage deductible." : "Enter an estimated loss to compare payments.", r);
    var b = $(".stack", r);
    if (b && loss > 0) { var a = Math.min(pd, loss) / loss * 100; b.children[0].style.width = a + "%"; b.children[1].style.width = (100 - a) + "%"; }
  });

  /* 5. Claim deadline calendar */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; plan = []; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies call for prompt notice. This is your own target, not a policy deadline." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and keep receipts", n: "Tarps, water extraction and heat to dry the building protect the claim and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies allow 60 days after the carrier asks. Count from the date on the request letter." },
      { d: add(45 + num($("[name=appr]", r))), t: "Name your appraiser (if appraisal was demanded)", n: "Assumes a demand about 45 days after the loss. Count from the actual demand date." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Policies set a time to finish repairs and claim the holdback. Confirm the number of days in your policy." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Check the Suit Against Us condition. Vermont law can affect how it applies, so ask a Vermont attorney well before this date." }
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
      if (!plan.length) return;
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Vermont Insurance Appraiser//Claim Deadline Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:via-" + ds(p.d) + "-" + i + "@vermontinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "vermont-claim-deadlines.ics";
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
      set("[data-o=score]", answered ? String(pct) : "–", r);
      var arc = $("[data-o=arc]", r);
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#154734" : pct >= 45 ? "#ffcc33" : "#a8323e"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have the basics an appraisal panel expects. The next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) ul.innerHTML = todo.length ? todo.map(function (t) { return "<li>" + t + "</li>"; }).join("") : "<li>Nothing flagged yet.</li>";
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
    var depth = num($("[name=depth]", r)), dens = num($("[name=type]", r)), ice = num($("[name=ice]", r)), area = num($("[name=area]", r)), cap = num($("[name=cap]", r));
    var snowPsf = depth / 12 * dens, icePsf = ice / 12 * 57, psf = snowPsf + icePsf;
    var tons = psf * area / 2000, share = cap > 0 ? psf / cap : 0;
    set("[data-o=psf]", psf.toFixed(1) + " lb/ft²", r);
    set("[data-o=snowpsf]", snowPsf.toFixed(1) + " lb/ft²", r);
    set("[data-o=icepsf]", icePsf.toFixed(1) + " lb/ft²", r);
    set("[data-o=tons]", tons.toFixed(1) + " tons", r);
    set("[data-o=share]", cap > 0 ? Math.round(share * 100) + "%" : "—", r);
    var b = $("[data-o=bar]", r);
    if (b) { b.style.width = Math.min(100, share * 100) + "%"; b.style.background = share >= 1 ? "#a8323e" : share >= 0.75 ? "#d9a400" : "#154734"; }
    set("[data-o=snowmsg]", !cap ? "Enter a design load to compare." : share >= 1 ? "The estimated load is at or above the design load you entered. Stay off the roof and get a professional to look at it." : share >= 0.75 ? "The estimated load is close to the design load. Watch for sagging, cracking sounds or doors that start to stick." : "The estimated load is below the design load you entered. Older or damaged framing can still fail below its design value.", r);
  });
})();
