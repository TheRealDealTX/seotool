/* Michigan Insurance Appraiser — site script: nav, drawer, effects, forms and claim tools. No dependencies.
   Every calculator runs in the browser; nothing typed into a tool is sent or stored. */
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
  root.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var canHover = window.matchMedia("(hover: hover)").matches;

  /* ---------- desktop mega menus ---------- */
  var closeMenus = function (except) {
    $$(".mm.open").forEach(function (li) {
      if (li === except) return;
      li.classList.remove("open");
      var b = $(".mm-btn", li); if (b) b.setAttribute("aria-expanded", "false");
    });
  };
  $$(".mm").forEach(function (li) {
    var btn = $(".mm-btn", li), t;
    var open = function () { closeMenus(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    var shut = function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (ev) { ev.stopPropagation(); li.classList.contains("open") ? shut() : open(); });
    li.addEventListener("mouseenter", function () { if (!canHover) return; clearTimeout(t); open(); });
    li.addEventListener("mouseleave", function () { if (!canHover) return; t = setTimeout(shut, 200); });
    li.addEventListener("focusout", function (ev) { if (!li.contains(ev.relatedTarget)) shut(); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".mm")) closeMenus(); });

  /* ---------- mobile drawer (outside the fixed header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim"), lastFocus = null, scrimTimer;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    clearTimeout(scrimTimer);
    scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!drawer || !body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    scrimTimer = setTimeout(function () { scrim.hidden = true; }, 340);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (burger && drawer && scrim) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1060) closeDrawer(); });
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeMenus(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, back-to-top, parallax CTA, timeline fill ---------- */
  var head = $(".masthead"), toTop = $(".to-top"), px = $$("[data-parallax]"), tl = $("[data-timeline]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 24);
    if (toTop) toTop.classList.toggle("show", y > 900);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      var lim = r.height * 0.12, v = Math.max(-lim, Math.min(lim, (r.top + r.height / 2 - vh / 2) * -k));
      el.style.transform = "translate3d(0," + v.toFixed(1) + "px,0)";
    });
    if (tl) {
      var b = tl.getBoundingClientRect(), mid = vh * 0.62, fill = $(".tl-fill", tl);
      var pct = Math.max(0, Math.min(1, (mid - b.top) / b.height));
      if (fill) fill.style.height = (pct * 100) + "%";
      $$(".tl-step", tl).forEach(function (s) { s.classList.toggle("on", s.getBoundingClientRect().top + 28 < mid); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function (ev) { ev.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1300;
    if (reduce) { el.textContent = end; return; }
    el.textContent = "0";
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 4) * 0.08 + "s"); }); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.08, rootMargin: "0px 0px -20px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(reveal); }

  /* ---------- region tabs (all panels show without JS) ---------- */
  $$("[data-tabs]").forEach(function (wrap) {
    var tabs = $$(".rtab", wrap), panels = $$(".rpanel", wrap);
    wrap.classList.add("js-tabs");
    var pick = function (i, focus) {
      tabs.forEach(function (t, j) { t.setAttribute("aria-selected", j === i ? "true" : "false"); t.tabIndex = j === i ? 0 : -1; });
      panels.forEach(function (p, j) { p.classList.toggle("on", j === i); });
      if (focus) tabs[i].focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { pick(i); });
      t.addEventListener("keydown", function (ev) {
        if (ev.key === "ArrowRight") { ev.preventDefault(); pick((i + 1) % tabs.length, true); }
        if (ev.key === "ArrowLeft") { ev.preventDefault(); pick((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
    pick(0);
  });

  /* ---------- tool rail ---------- */
  var rail = $("[data-rail-track]");
  $$("[data-rail]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!rail) return;
      var card = $(".tcard", rail), w = card ? card.getBoundingClientRect().width + 18 : 320;
      rail.scrollBy({ left: w * parseInt(b.getAttribute("data-rail"), 10), behavior: reduce ? "auto" : "smooth" });
    });
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0;
    $$(".g-row").forEach(function (row) {
      var hit = !q || row.textContent.toLowerCase().indexOf(q) > -1;
      row.hidden = !hit; if (hit) shown++;
    });
    set("[data-gloss-count]", shown + (shown === 1 ? " term" : " terms"));
    var none = $(".gloss-none"); if (none) none.hidden = shown > 0;
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      $$("[aria-invalid]", form).forEach(function (f) { f.removeAttribute("aria-invalid"); });
      var bad = $$("[required]", form).filter(function (f) {
        if (f.type === "checkbox") return !f.checked;
        if (f.type === "email") return !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(f.value.trim());
        return !f.value.trim();
      });
      if (bad.length) {
        bad.forEach(function (f) { f.setAttribute("aria-invalid", "true"); });
        msg.textContent = "Please complete the highlighted fields, including the consent box.";
        msg.classList.add("err"); bad[0].focus(); return;
      }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and we’ll be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@michiganinsuranceappraiser.com\">info@michiganinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding helper ---------- */
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
      run();
    });
  }
  var pctTxt = function (x) { return Math.round(x * 100) + "%"; };
  var fmtDate = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };

  /* 1. Claim gap & fee estimator (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var ft = $("[name=feetype]", r) ? $("[name=feetype]", r).value : null;
    var fee = num($("[name=fee]", r)), rate = num($("[name=rate]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var fixed = useUmp ? ump / 2 : 0, pctFee = 0;
    if (ft === "flat") fixed += fee;
    else if (ft === "hourly") fixed += fee * rate;
    else if (ft === "pct") pctFee = Math.min(Math.max(fee, 0), 100) / 100;
    var cost = ft ? fixed + gain * pctFee : 0, net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    var be = $("[data-o=breakeven]", r);
    if (be) {
      var need = pctFee < 1 ? fixed / (1 - pctFee) : Infinity;
      be.textContent = gap <= 0 ? "—" : need <= 0 ? "0% (any increase helps)" : need > gap ? "Not reached at 100%" : pctTxt(need / gap) + " of the gap";
    }
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
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. With no gap, there’s nothing for an appraisal panel to decide.";
      else if (ft && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line second opinion is usually a better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. A documented supplement request may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready.";
      m.textContent = t;
    }
  });

  /* 2. RCV vs ACV holdback */
  tool("dep", function (r) {
    var rcv = 0, dep = 0, cap = (num($("[name=cap]", r)) || 80) / 100;
    $$("tbody tr", r).forEach(function (tr) {
      var c = num($("[name=rcv]", tr)), age = num($("[name=age]", tr)), life = num($("[name=life]", tr)) || 1;
      var d = Math.min(cap, Math.max(0, age) / life) * c;
      rcv += c; dep += d;
      var o = $("[data-o=row]", tr); if (o) o.textContent = money(c - d);
    });
    var ded = num($("[name=deduct]", r)), paid = num($("[name=paid]", r)), win = num($("[name=window]", r));
    var nonrec = $("[name=nonrec]", r) && $("[name=nonrec]", r).checked;
    var acv = rcv - dep, first = Math.max(0, acv - ded - paid);
    var total = nonrec ? first : Math.max(0, rcv - ded - paid);
    set("[data-o=rcv]", money(rcv), r);
    set("[data-o=dep]", money(dep), r);
    set("[data-o=acv]", money(acv), r);
    set("[data-o=first]", money(first), r);
    set("[data-o=held]", money(total - first), r);
    set("[data-o=total]", money(total), r);
    set("[data-o=deppct]", rcv ? Math.round(dep / rcv * 100) + "%" : "0%", r);
    var by = new Date(); by.setDate(by.getDate() + win);
    set("[data-o=by]", win > 0 && !nonrec ? by.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" }) : "—", r);
  });
  $$('[data-tool="dep"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (ev) {
      if (ev.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = ""; });
        tb.appendChild(tr);
        r.dispatchEvent(new Event("input"));
      }
      var x = ev.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof squares, pitch & eave ice barrier */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), ohIn = num($("[name=oh]", r)), oh = ohIn / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = Math.ceil(sq * (1 + waste) * 3 - 1e-9) / 3;
    var est = num($("[name=est]", r)), eave = num($("[name=eave]", r)), bar = num($("[name=bar]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", order.toFixed(2), r);
    set("[data-o=bundles]", String(Math.ceil(order * 3 - 1e-9)), r);
    /* Ice barrier: from the eave edge to `bar` inches inside the wall line, measured up the slope.
       A 36-inch roll with a 3-inch side lap covers about 33 inches per row. */
    var slopeIn = (ohIn + bar) * mult, rows = slopeIn > 0 ? Math.ceil(slopeIn / 33 - 1e-9) : 0;
    set("[data-o=ice]", eave > 0 && rows ? rows + (rows === 1 ? " row · " : " rows · ") + Math.round(rows * 3 * eave).toLocaleString("en-US") + " sq ft" : "—", r);
    var vs = $("[data-o=vs]", r);
    if (vs) {
      if (!est) vs.textContent = "—";
      else { var d = order - est; vs.textContent = (d >= 0 ? "+" : "−") + Math.abs(d).toFixed(2) + " sq (" + (d >= 0 ? "+" : "−") + Math.abs(Math.round(d / est * 100)) + "%)"; }
    }
    set("[data-o=steep]", pitch >= 8 ? "At " + pitch + "/12, estimating software normally adds steep-roof labor. Check the carrier’s estimate for it, plus high-roof charges on two-story walls." : pitch >= 7 ? "At 7/12, some carriers start applying steep charges. Confirm how your estimate treats this pitch." : pitch <= 3 ? "Pitches under 4/12 often need special underlayment or a low-slope roofing system. Confirm what the estimate assumes." : "A walkable pitch: no steep-roof charge is usually expected.", r);
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var trig = $("[name=trig]", r) ? $("[name=trig]", r).checked : true;
    var pctd = covA * pct / 100, applied = trig ? pctd : flat;
    set("[data-o=pd]", money(applied), r);
    set("[data-o=pctd]", money(pctd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pctd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, pctd) - Math.min(loss, flat))), r);
    var t;
    if (!loss) t = "Enter an estimated loss to compare payments.";
    else if (!trig) t = "If the percentage deductible doesn’t apply to this cause of loss, the flat deductible usually does. Confirm the wording in your policy.";
    else if (loss <= applied) t = "This loss falls entirely within the percentage deductible, so no claim payment would be owed on it.";
    else t = "The loss exceeds the deductible by " + money(loss - applied) + ".";
    set("[data-o=below]", t, r);
    var bar = $(".stack", r);
    if (bar) {
      var a = loss > 0 ? Math.min(applied, loss) / loss * 100 : 0;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%";
    }
  });

  /* 5. Claim deadline planner with general Michigan tolling estimate + .ics */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var day = function (s) { return s ? new Date(s + "T12:00:00") : null; };
    var add = function (from, days) { var d = new Date(from); d.setDate(d.getDate() + days); return d; };
    var ntc = day($("[name=ntc]", r).value), den = day($("[name=den]", r).value);
    var yr = new Date(base); yr.setFullYear(yr.getFullYear() + 1);
    plan = [
      { d: add(base, num($("[name=inv]", r))), t: "Contents inventory target", n: "Room-by-room list with photos, ages and replacement prices." },
      { d: add(base, num($("[name=rcd]", r))), t: "Holdback window closes (per your entry)", n: "Finish repairs and send invoices to recover withheld depreciation. Confirm the exact period in your policy and the carrier’s letters." },
      { d: yr, t: "One year after the loss (before any tolling)", n: "Michigan generally requires suits on a property policy within one year of the loss, or longer if the policy allows. Talk to a Michigan attorney well before this date." }
    ];
    if (ntc && den && den >= ntc) {
      var paused = Math.round((den - ntc) / 864e5);
      plan.push({ d: add(yr, paused), t: "Estimated suit-limitation date with tolling", n: "Adds the " + paused + " days between your notice and the formal denial, under the general tolling rule. A planning estimate only; confirm with a Michigan attorney." });
    } else if (ntc && !den) {
      plan.push({ d: ntc, t: "Notice given: tolling may be running", n: "Under the general rule, the limitation period is paused from notice until a formal denial. Keep every letter and ask an attorney how your dates apply." });
    }
    plan.sort(function (a, b) { return a.d - b.d; });
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
      var remind = $('[data-tool="dates"] [name=remind]'); remind = remind && remind.checked;
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (dt) { return dt.getFullYear() + pad(dt.getMonth() + 1) + pad(dt.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Michigan Insurance Appraiser//Claim Deadline Planner//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:mia-" + ds(p.d) + "-" + i + "@michiganinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n));
        if (remind) ics.push("BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc(p.t), "TRIGGER:-P14D", "END:VALARM");
        ics.push("END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "michigan-claim-deadlines.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal readiness score */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#3fae7c" : pct >= 45 ? "#FFCB05" : "#D4552E"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional look at the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
      var ul = $("[data-o=todo]", r);
      if (ul) {
        ul.textContent = "";
        (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); });
      }
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

  /* 7. Ice dam risk & illustrative repair cost */
  tool("ice", function (r) {
    var v = function (n) { var el = $("[name=" + n + "]", r); return el ? parseFloat(el.value) || 0 : 0; };
    var barrier = $("[name=barrier]", r).checked;
    var pts = Math.max(0, Math.min(10, v("zone") + v("ins") + v("vent") + v("shape") - (barrier ? 2 : 0)));
    var label = pts < 3 ? "Low" : pts < 5 ? "Moderate" : pts < 7.5 ? "High" : "Very high";
    set("[data-o=risk]", label + " (" + pts.toFixed(1).replace(".0", "") + "/10)", r);
    var bar = $("[data-o=bar]", r); if (bar) bar.style.width = (pts * 10) + "%";
    var dry = num($("[name=dry]", r)), ins = num($("[name=insul]", r)), fl = num($("[name=floor]", r)), rooms = num($("[name=rooms]", r));
    /* Broad illustrative unit ranges (not quotes): drywall/plaster $4–9/sf, insulation $1.50–3.50/sf, flooring $6–14/sf, paint $450–900/room. */
    var low = dry * 4 + ins * 1.5 + fl * 6 + rooms * 450, high = dry * 9 + ins * 3.5 + fl * 14 + rooms * 900;
    set("[data-o=low]", money(low), r);
    set("[data-o=high]", money(high), r);
    var tips = [];
    if (v("ins") >= 1.5) tips.push("More attic insulation reduces the heat that melts roof snow.");
    if (v("vent") >= 1) tips.push("Balanced soffit-to-ridge ventilation keeps the roof deck cold.");
    if (!barrier) tips.push("If the roof is replaced, confirm the estimate includes an eave ice-and-water barrier.");
    set("[data-o=imsg]", (low > 0 ? "Compare this range with the interior lines in the carrier’s estimate. " : "") + (tips.length ? tips.join(" ") : "Your setup already addresses the main causes of ice dams."), r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
