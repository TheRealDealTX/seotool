/* Arkansas Insurance Appraiser — site script (nav, drawer, reveal, forms, claim tools). No dependencies.
   Every tool runs in the browser; nothing typed into a tool is sent or stored. */
(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var money = function (n) {
    if (!isFinite(n)) n = 0;
    return (n < 0 ? "−$" : "$") + Math.round(Math.abs(n)).toLocaleString("en-US");
  };
  var num = function (el) { if (!el) return 0; var v = parseFloat(String(el.value).replace(/[^0-9.\-]/g, "")); return isFinite(v) ? v : 0; };
  var val = function (r, name) { return num($('[name="' + name + '"]', r)); };
  var set = function (r, key, text) { $$('[data-o="' + key + '"]', r).forEach(function (el) { el.textContent = text; }); };
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var body = document.body, root = document.documentElement;
  root.classList.remove("no-js");

  /* ---------- desktop dropdowns ---------- */
  var closeSubs = function (except) {
    $$(".menu .has-sub.open").forEach(function (li) { if (li === except) return; li.classList.remove("open"); $(".sub-btn", li).setAttribute("aria-expanded", "false"); });
  };
  $$(".menu .has-sub").forEach(function (li) {
    var btn = $(".sub-btn", li), t;
    var open = function () { closeSubs(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); if (li.classList.contains("open")) closeSubs(); else open(); });
    li.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) { clearTimeout(t); open(); } });
    li.addEventListener("mouseleave", function () { if (window.matchMedia("(hover: hover)").matches) { t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); } });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".menu")) closeSubs(); });

  /* ---------- mobile drawer (lives outside the fixed header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim"), lastFocus = null;
  function openDrawer() {
    lastFocus = document.activeElement;
    scrim.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    body.classList.add("lock");
    requestAnimationFrame(function () { body.classList.add("drawer-open"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  }
  function closeDrawer() {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!body.classList.contains("drawer-open")) scrim.hidden = true; }, 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (drawer && burger && scrim) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
    $$(".acc", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var was = b.getAttribute("aria-expanded") === "true";
        $$(".acc", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); });
        b.setAttribute("aria-expanded", was ? "false" : "true");
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1060) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeSubs(); closeDrawer(); } });

  /* ---------- header, parallax, back-to-top ring ---------- */
  var hdr = $(".hdr"), toTop = $(".totop"), ring = $(".totop-ring circle");
  var px = $$("[data-parallax]"), ticking = false;
  function onScroll() {
    var y = window.scrollY || window.pageYOffset, h = root.scrollHeight - window.innerHeight;
    if (hdr) hdr.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 700);
    if (ring) ring.style.strokeDashoffset = (144.5 * (1 - (h > 0 ? Math.min(1, y / h) : 0))).toFixed(1);
    if (!reduce) px.forEach(function (el) {
      var box = el.parentElement.getBoundingClientRect();
      if (box.bottom < 0 || box.top > window.innerHeight) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      el.style.transform = "translate3d(0," + ((box.top + box.height / 2 - window.innerHeight / 2) * -k).toFixed(1) + "px,0)";
    });
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function (e) { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- staggered reveal + counters ---------- */
  function count(el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null;
    if (reduce || !isFinite(end)) return;
    el.textContent = "0";
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1400); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  }
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.08 + "s"); }); });
  var targets = $$(".rv");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
    var co = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { $$("[data-count]", en.target).forEach(count); co.unobserve(en.target); } }); }, { threshold: 0.4 });
    $$(".counts").forEach(function (el) { co.observe(el); });
  } else { targets.forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- region rail ---------- */
  $$("[data-rail]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var rail = btn.closest(".sec").querySelector(".rail"); if (!rail) return;
      var card = rail.querySelector(".region"); var step = card ? card.getBoundingClientRect().width + 22 : 320;
      rail.scrollBy({ left: step * parseInt(btn.getAttribute("data-rail"), 10), behavior: reduce ? "auto" : "smooth" });
    });
  });

  /* ---------- glossary filter ---------- */
  var gq = $("#gloss-q");
  if (gq) gq.addEventListener("input", function () {
    var q = gq.value.trim().toLowerCase(), shown = 0;
    $$(".glossary .term").forEach(function (t) { var hit = !q || t.textContent.toLowerCase().indexOf(q) > -1; t.hidden = !hit; if (hit) shown++; });
    var c = $("[data-gcount]"); if (c) c.textContent = shown + (shown === 1 ? " term" : " terms") + (q ? " match" : "");
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg"; msg.textContent = "";
      var bad = $$("[required]", form).filter(function (f) {
        var miss = f.type === "checkbox" ? !f.checked : !f.value.trim() || (f.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value.trim()));
        f.setAttribute("aria-invalid", miss ? "true" : "false");
        return miss;
      });
      if (bad.length) { msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (!d || !d.ok) throw new Error("send failed");
          form.reset();
          msg.textContent = "Thank you. Your claim details were received, and someone from Arkansas Insurance Appraiser will reach out, usually within one business day.";
          msg.classList.add("ok");
        })
        .catch(function () {
          msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@arkansasinsuranceappraiser.com\">info@arkansasinsuranceappraiser.com</a>.";
          msg.classList.add("err");
        })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (r) {
      var run = function () { fn(r); };
      r.addEventListener("input", run);
      r.addEventListener("change", run);
      r.addEventListener("click", function (e) { if (e.target.closest("[data-run]")) setTimeout(run, 0); });
      $$(".slider input[type=range]", r).forEach(function (s) {
        var out = s.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = s.value + (s.getAttribute("data-unit") || ""); };
        s.addEventListener("input", upd); upd();
      });
      run();
    });
  }
  var API = window.AIA = {};

  /* 1. Claim gap & fee estimator */
  function gapMath(o) {
    var gap = Math.max(0, o.yours - o.insurer);
    var cost = function (gross) {
      var c = o.feetype === "pct" ? gross * o.fee / 100 : o.feetype === "hourly" ? o.hours * o.rate : o.fee;
      return c + o.umpire / 2;
    };
    var at = function (share) { var g = gap * share; var c = cost(g); return { gross: g, cost: c, net: g - c }; };
    var be = null;
    if (gap > 0) { for (var s = 0; s <= 100; s++) { if (at(s / 100).net > 0) { be = s; break; } } }
    return { gap: gap, pct: o.insurer > 0 ? gap / o.insurer * 100 : null, at: at, breakeven: be };
  }
  API.gap = gapMath;
  tool("gapfee", function (r) {
    var ft = $('[name="feetype"]', r);
    var o = { insurer: val(r, "insurer"), yours: val(r, "yours"), feetype: ft ? ft.value : "none", fee: val(r, "fee"), hours: val(r, "hours"), rate: val(r, "rate"), umpire: val(r, "umpire") };
    if (!ft) { o.fee = 0; o.umpire = 0; }
    var hr = $("[data-hourly]", r); if (hr) hr.hidden = o.feetype !== "hourly";
    var m = gapMath(o), land = val(r, "land") / 100, mine = m.at(land);
    set(r, "gap", money(m.gap));
    set(r, "pct", m.pct === null ? "—" : Math.round(m.pct) + "%");
    set(r, "gross", money(mine.gross));
    set(r, "net", money(mine.net));
    set(r, "breakeven", m.breakeven === null ? "Not reached" : m.breakeven + "% of the gap");
    var tb = $('[data-o="scen"]', r);
    if (tb) tb.innerHTML = [0.25, 0.5, 0.75].map(function (s) {
      var x = m.at(s);
      return "<tr><td>" + (s * 100) + "% of the gap</td><td>" + money(x.gross) + "</td><td>" + money(x.cost) + '</td><td class="' + (x.net > 0 ? "pos" : "neg") + '">' + money(x.net) + "</td></tr>";
    }).join("");
    var meter = $(".meter", r);
    if (meter && meter.children.length === 3) {
      var total = Math.max(o.insurer + mine.gross, 1);
      meter.children[0].style.width = (o.insurer / total * 100) + "%";
      meter.children[1].style.width = (Math.max(0, mine.net) / total * 100) + "%";
      meter.children[2].style.width = (Math.min(mine.cost, mine.gross) / total * 100) + "%";
    }
    var t;
    if (!o.insurer || !o.yours) t = "Enter both estimates to see the amount in dispute.";
    else if (m.gap <= 0) t = "Your estimate isn’t higher than the carrier’s, so there is no price gap for appraisal to resolve.";
    else if (ft && mine.net <= 0) t = "At these inputs, costs could absorb the recovery. An estimate review or a documented supplement is usually a better first step.";
    else if (m.pct < 10 && m.gap < 5000) t = "The gap is real but narrow. A supplement with good photos may close it without formal appraisal.";
    else t = "The amount in dispute is large enough that appraisal may be worth discussing. These figures are illustrative.";
    set(r, "msg", t);
  });

  /* 2. RCV vs ACV holdback */
  function holdMath(rows, o) {
    var rcv = 0, dep = 0, depAll = 0;
    rows.forEach(function (x) {
      var share = Math.min(o.cap, x.life > 0 ? x.age / x.life : 0);
      var mat = x.rcv * (1 - Math.min(100, Math.max(0, x.labor)) / 100);
      var dFull = x.rcv * share, dMat = mat * share;
      rcv += x.rcv; depAll += dFull; dep += o.matonly ? dMat : dFull;
      x.acv = x.rcv - (o.matonly ? dMat : dFull);
    });
    var acv = rcv - dep, first = Math.max(0, acv - o.deduct);
    var total = o.acvonly ? first : Math.max(0, rcv - o.deduct);
    var firstAll = Math.max(0, rcv - depAll - o.deduct);
    return { rcv: rcv, dep: dep, depAll: depAll, acv: acv, first: first, held: Math.max(0, total - first), total: total, laborDiff: first - firstAll };
  }
  API.hold = holdMath;
  tool("holdback", function (r) {
    var rows = $$("tbody tr", r).map(function (tr) { return { tr: tr, rcv: num($('[name="rcv"]', tr)), labor: num($('[name="labor"]', tr)), age: num($('[name="age"]', tr)), life: num($('[name="life"]', tr)) }; });
    var capv = val(r, "cap");
    var o = { cap: capv >= 100 ? 1 : capv / 100, deduct: val(r, "deduct"), matonly: $('[name="matonly"]', r).checked, acvonly: $('[name="acvonly"]', r).checked };
    var m = holdMath(rows, o);
    rows.forEach(function (x) { var c = $('[data-o="row"]', x.tr); if (c) c.textContent = money(x.acv); });
    set(r, "rcv", money(m.rcv)); set(r, "dep", money(m.dep)); set(r, "depall", money(m.depAll));
    set(r, "first", money(m.first)); set(r, "held", money(m.held)); set(r, "total", money(m.total));
    set(r, "labordiff", money(m.laborDiff));
    set(r, "msg", o.matonly ? "With labor left undepreciated, the first check is " + money(m.laborDiff) + " higher than if the whole line were depreciated. Illustrative only; see the guide on labor depreciation." :
      "This view depreciates labor along with materials. Check “materials only” to compare.");
  });
  $$('[data-tool="holdback"]').forEach(function (r) {
    var tb = $("tbody", r);
    r.addEventListener("click", function (e) {
      if (e.target.closest("[data-add]")) {
        var tr = tb.rows[0].cloneNode(true);
        $$("input", tr).forEach(function (i) { i.value = i.name === "labor" ? "40" : ""; });
        tb.appendChild(tr);
        $("input", tr).focus();
      }
      var x = e.target.closest(".rm");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof pitch & squares */
  function roofMath(o) {
    var oh = o.oh / 12, L = o.len + 2 * oh, W = o.wid + 2 * oh;
    var foot = L * W, mult = Math.sqrt(1 + Math.pow(o.pitch / 12, 2));
    var surface = foot * mult, sq = surface / 100, order = Math.ceil(sq * (1 + o.waste / 100) * 3) / 3;
    var rake = o.style === "gable" ? 2 * 2 * (W / 2) * mult : 0;
    var drip = 2 * L + (o.style === "gable" ? rake : 2 * W);
    var hipLen = Math.sqrt(Math.pow(W / 2, 2) * 2 + Math.pow(W / 2 * o.pitch / 12, 2));
    var ridge = o.style === "gable" ? L : Math.max(0, L - W) + 4 * hipLen;
    return { mult: mult, angle: Math.atan(o.pitch / 12) * 180 / Math.PI, surface: surface, sq: sq, order: order, bundles: Math.ceil(order * 3), drip: drip, ridge: ridge };
  }
  API.roof = roofMath;
  tool("roof", function (r) {
    var st = $('[name="style"]', r), opt = st.options[st.selectedIndex];
    var o = { len: val(r, "len"), wid: val(r, "wid"), oh: val(r, "oh"), pitch: val(r, "pitch"), style: st.value, waste: parseFloat(opt.getAttribute("data-waste")) || 10 };
    var m = roofMath(o), price = val(r, "price");
    set(r, "mult", m.angle.toFixed(1) + "° / ×" + m.mult.toFixed(3));
    set(r, "surface", Math.round(m.surface).toLocaleString("en-US") + " sq ft");
    set(r, "sq", m.sq.toFixed(2));
    set(r, "waste", o.waste + "%");
    set(r, "order", m.order.toFixed(2) + " sq");
    set(r, "bundles", String(m.bundles));
    set(r, "drip", Math.round(m.drip) + " lin ft");
    set(r, "ridge", Math.round(m.ridge) + " lin ft");
    set(r, "cost", price ? money(m.order * price) : "—");
    set(r, "steep", o.pitch >= 8 ? "At " + o.pitch + "/12, estimating software commonly adds a steep-roof labor charge. Check that the carrier’s estimate includes it." :
      o.pitch >= 7 ? "At 7/12 many estimates begin adding steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: a steep-roof charge usually isn’t expected, but check for high-roof charges on two-story eaves.");
  });

  /* 4. Percentage deductible */
  function dedMath(o) {
    var pd = o.cova * o.pct / 100;
    return { pd: pd, pdpay: Math.max(0, o.loss - pd), flatpay: Math.max(0, o.loss - o.flat), diff: Math.min(o.loss, pd) - Math.min(o.loss, o.flat) };
  }
  API.ded = dedMath;
  tool("pctded", function (r) {
    var o = { cova: val(r, "cova"), pct: val(r, "pct"), flat: val(r, "flat"), loss: val(r, "loss") };
    var m = dedMath(o);
    set(r, "pd", money(m.pd)); set(r, "pdpay", money(m.pdpay)); set(r, "flatpay", money(m.flatpay)); set(r, "diff", money(m.diff));
    var tb = $('[data-o="cmp"]', r);
    if (tb) tb.innerHTML = [1, 2, 3, 5].map(function (p) { var x = dedMath({ cova: o.cova, pct: p, flat: o.flat, loss: o.loss }); return "<tr" + (p === o.pct ? ' style="font-weight:800"' : "") + "><td>" + p + "%</td><td>" + money(x.pd) + "</td><td>" + money(x.pdpay) + "</td></tr>"; }).join("");
    var meter = $(".meter", r);
    if (meter && o.loss > 0) { var a = Math.min(m.pd, o.loss) / o.loss * 100; meter.children[0].style.width = a + "%"; meter.children[1].style.width = (100 - a) + "%"; }
    set(r, "below", !o.loss ? "Enter an estimated loss to compare." : o.loss <= m.pd ? "This loss falls entirely within the percentage deductible, so no payment would be owed under it." : "The loss exceeds the deductible by " + money(o.loss - m.pd) + ".");
  });

  /* 5. Claim timeline builder + .ics */
  var plan = [];
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  API.addDays = addDays;
  tool("timeline", function (r) {
    var list = $('[data-o="list"]', r), d0 = $('[name="dol"]', r).value, rq = $('[name="req"]', r).value;
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here, in date order.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var polBase = rq ? new Date(rq + "T12:00:00") : base;
    plan = [
      { d: addDays(base, val(r, "notice")), t: "Report the claim to your insurer", n: "Policies require prompt notice. This is your own target date." },
      { d: addDays(base, val(r, "mitig")), t: "Temporary repairs done, receipts saved", n: "Tarping, water extraction and board-up protect the property and are usually reimbursable." },
      { d: addDays(base, val(r, "est")), t: "Have your own itemized estimate", n: "A line-item estimate from a contractor or estimator to compare with the carrier’s." },
      { d: addDays(polBase, val(r, "pol")), t: "Proof of loss due" + (rq ? "" : " (if requested)"), n: rq ? "Counted from the carrier’s request date you entered." : "Counted from the date of loss as a placeholder. Enter the request date for an exact figure." },
      { d: addDays(base, val(r, "appr")), t: "Planning marker: name an appraiser", n: "Policies often allow about 20 days after a written demand. Recount from the demand date once one is sent." },
      { d: addDays(base, val(r, "rcd")), t: "Replacement-cost recovery deadline", n: "Finish repairs and claim the holdback before your policy’s deadline. Ask in writing for an extension if needed." },
      { d: addDays(base, val(r, "suit")), t: "Suit-limitation date (check your policy)", n: "Talk with an Arkansas attorney well before this date if the claim is unresolved." }
    ].sort(function (a, b) { return a.d - b.d; });
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + "<em>" + badge + "</em></b><strong>" + p.t + "</strong><span>" + p.n + "</span></li>";
    }).join("");
  });
  function icsText(items) {
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
    var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
    var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
    var out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Arkansas Insurance Appraiser//Claim Timeline//EN", "CALSCALE:GREGORIAN"];
    items.forEach(function (p, i) {
      out.push("BEGIN:VEVENT", "UID:aia-" + ds(p.d) + "-" + i + "@arkansasinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(addDays(p.d, 1)), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n), "END:VEVENT");
    });
    out.push("END:VCALENDAR");
    return out.join("\r\n");
  }
  API.ics = function () { return icsText(plan); };
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) { var d = btn.closest(".calc").querySelector('[name="dol"]'); if (d) d.focus(); return; }
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([icsText(plan)], { type: "text/calendar;charset=utf-8" }));
      a.download = "arkansas-claim-timeline.ics";
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
      set(r, "score", answered ? String(pct) : "–");
      set(r, "count", answered + " / " + items.length);
      var arc = $('[data-o="arc"]', r);
      if (arc) { arc.style.strokeDashoffset = (314.2 - 314.2 * (answered ? pct : 0) / 100).toFixed(1); arc.style.stroke = pct >= 75 ? "#157570" : pct >= 45 ? "#c9822b" : "#8f1d24"; }
      set(r, "verdict", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what a panel expects; the next step is a professional look at the dollar gap." :
        pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal." : "Not ready yet. Demanding appraisal now risks an incomplete award. Work through the list first.");
      var ul = $('[data-o="todo"]', r);
      if (ul) { ul.innerHTML = ""; (todo.length ? todo : ["Nothing flagged yet."]).forEach(function (t) { var li = document.createElement("li"); li.textContent = t; ul.appendChild(li); }); }
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

  /* 7. Ice load on a limb */
  function iceMath(o) {
    var rft = o.dia / 2 / 12, t = o.ice / 12, L = o.len;
    var iceVol = Math.PI * L * (Math.pow(rft + t, 2) - Math.pow(rft, 2)) * o.twig;
    var woodVol = Math.PI * L * rft * rft;
    var ice = iceVol * 57.2, wood = woodVol * 55;
    return { ice: ice, wood: wood, inc: wood > 0 ? ice / wood * 100 : 0, all: ice * o.count };
  }
  API.ice = iceMath;
  tool("ice", function (r) {
    var o = { dia: val(r, "dia"), len: val(r, "len"), ice: val(r, "ice"), twig: val(r, "twig") || 1, count: val(r, "count") };
    var m = iceMath(o);
    var lb = function (n) { return Math.round(n).toLocaleString("en-US") + " lb"; };
    set(r, "ice1", lb(m.ice)); set(r, "wood", lb(m.wood)); set(r, "inc", Math.round(m.inc) + "%"); set(r, "all", lb(m.all));
    set(r, "msg", m.inc >= 100 ? "The ice can more than double the load on the limb, before any wind. That is why sound limbs fail in Arkansas ice storms. Illustrative only." :
      "Even a thin coat adds real weight, and wind multiplies it. Illustrative only; not an engineering analysis.");
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
