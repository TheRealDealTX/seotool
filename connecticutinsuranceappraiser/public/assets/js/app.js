/* Connecticut Insurance Appraiser — site script: nav, drawer, effects, forms and claim tools. No dependencies. */
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

  /* ---------- desktop dropdowns ---------- */
  var closeDrops = function (except) {
    $$(".has-dd.open").forEach(function (li) {
      if (li === except) return;
      li.classList.remove("open");
      var b = $(".dd-btn", li); if (b) b.setAttribute("aria-expanded", "false");
    });
  };
  $$(".has-dd").forEach(function (li) {
    var btn = $(".dd-btn", li), t;
    var open = function () { closeDrops(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); };
    var shut = function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (ev) { ev.stopPropagation(); li.classList.contains("open") ? shut() : open(); });
    li.addEventListener("mouseenter", function () { if (!canHover) return; clearTimeout(t); open(); });
    li.addEventListener("mouseleave", function () { if (!canHover) return; t = setTimeout(shut, 180); });
    li.addEventListener("focusout", function (ev) { if (!li.contains(ev.relatedTarget)) shut(); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".has-dd")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the sticky header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".drawer-scrim"), lastFocus = null, scrimTimer;
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
    scrimTimer = setTimeout(function () { scrim.hidden = true; }, 320);
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
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- scroll effects: solid header, back-to-top, parallax, timeline fill ---------- */
  var head = $(".site-head"), toTop = $(".to-top"), px = $$("[data-parallax]"), tl = $("[data-timeline]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, vh = window.innerHeight;
    if (head) head.classList.toggle("solid", y > 30);
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      var lim = r.height * 0.14, v = Math.max(-lim, Math.min(lim, (r.top + r.height / 2 - vh / 2) * -k));
      el.style.transform = "translate3d(0," + v.toFixed(1) + "px,0)";
    });
    if (tl) {
      var b = tl.getBoundingClientRect(), mid = vh * 0.6;
      var fill = $(".tl-fill", tl);
      var pct = Math.max(0, Math.min(1, (mid - b.top) / b.height));
      if (fill) fill.style.height = (pct * 100) + "%";
      $$(".tl-step", tl).forEach(function (s) { s.classList.toggle("on", s.getBoundingClientRect().top + 30 < mid); });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function (ev) { ev.preventDefault(); window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1400;
    if (reduce) { el.textContent = end; return; }
    el.textContent = "0";
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    $$(".rv").forEach(function (el) { io.observe(el); });
  } else { $$(".rv").forEach(reveal); }

  /* ---------- 3D tilt on tool cards ---------- */
  if (!reduce && canHover) {
    $$("[data-tilt]").forEach(function (el) {
      el.addEventListener("mousemove", function (ev) {
        var r = el.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width - 0.5, y = (ev.clientY - r.top) / r.height - 0.5;
        el.style.transform = "rotateY(" + (x * 9).toFixed(2) + "deg) rotateX(" + (-y * 9).toFixed(2) + "deg) translateY(-4px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = ""; });
    });
  }

  /* ---------- expanding region panels ---------- */
  $$("[data-regions]").forEach(function (wrap) {
    var panels = $$(".reg", wrap);
    var pick = function (p) { panels.forEach(function (o) { o.classList.toggle("open", o === p); }); };
    panels.forEach(function (p) {
      p.addEventListener("click", function () { pick(p); });
      p.addEventListener("focus", function () { pick(p); });
      if (canHover) p.addEventListener("mouseenter", function () { pick(p); });
      p.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); pick(p); } });
    });
  });

  /* ---------- storm almanac scroller ---------- */
  var track = $(".alm-track");
  $$("[data-alm]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (!track) return;
      var card = $(".alm-card", track), stepW = card ? card.getBoundingClientRect().width + 18 : 300;
      track.scrollBy({ left: stepW * parseInt(b.getAttribute("data-alm"), 10), behavior: reduce ? "auto" : "smooth" });
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
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@connecticutinsuranceappraiser.com\">info@connecticutinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- tool binding helper ---------- */
  function tool(name, fn) {
    $$('[data-tool="' + name + '"]').forEach(function (r) {
      var run = function () { fn(r); };
      r.addEventListener("input", run);
      r.addEventListener("change", run);
      r.addEventListener("click", function (ev) { if (ev.target.closest("[data-run]")) setTimeout(run, 0); });
      $$(".range input[type=range]", r).forEach(function (rg) {
        var out = rg.parentElement.querySelector("output");
        var upd = function () { if (out) out.textContent = rg.value + (rg.getAttribute("data-unit") || ""); };
        rg.addEventListener("input", upd); upd();
      });
      run();
    });
  }
  var pctTxt = function (x) { return Math.round(x * 100) + "%"; };

  /* 1. Claim gap & fee estimator (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.5;
    var ft = $("[name=feetype]", r) ? $("[name=feetype]", r).value : null;
    var fee = num($("[name=fee]", r)), rate = num($("[name=rate]", r)), ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins), award = ins + gap * land, gain = award - ins;
    var umpShare = useUmp ? ump / 2 : 0, cost = 0, fixed = umpShare, pctFee = 0;
    if (ft === "flat") { fixed += fee; }
    else if (ft === "hourly") { fixed += fee * rate; }
    else if (ft === "pct") { pctFee = Math.min(fee, 100) / 100; }
    cost = ft ? fixed + gain * pctFee : 0;
    var net = gain - cost;
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
      else if (ft && net <= 0) t = "At these inputs, appraisal costs could absorb the whole increase. A line-by-line estimate review is usually a better first step.";
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
    var acv = rcv - dep;
    var first = Math.max(0, acv - ded - paid);
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
      }
      var x = ev.target.closest(".x");
      if (x && tb.rows.length > 1) { x.closest("tr").remove(); r.dispatchEvent(new Event("input")); }
    });
  });

  /* 3. Roof square & pitch converter */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult, sq = surface / 100, order = Math.ceil(sq * (1 + waste) * 3 - 1e-9) / 3;
    var per = num($("[name=mat]", r)), price = num($("[name=price]", r)), est = num($("[name=est]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", order.toFixed(2), r);
    set("[data-o=bundles]", per ? String(Math.ceil(order * per)) : "n/a", r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var vs = $("[data-o=vs]", r);
    if (vs) {
      if (!est) vs.textContent = "—";
      else { var d = order - est; vs.textContent = (d >= 0 ? "+" : "−") + Math.abs(d).toFixed(2) + " sq (" + (d >= 0 ? "+" : "−") + Math.abs(Math.round(d / est * 100)) + "%)"; }
    }
    var st = $("[data-o=steep]", r);
    if (st) st.textContent = pitch >= 8 ? "At " + pitch + "/12, estimating software normally adds steep-roof labor. Check that the carrier’s estimate includes it, plus high-roof charges on two-story walls." : pitch >= 7 ? "At 7/12, some carriers start applying steep charges. Confirm how your estimate treats this pitch." : "A walkable pitch: no steep-roof charge is usually expected.";
  });

  /* 4. Hurricane & windstorm deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var trig = $("[name=trig]", r) ? $("[name=trig]", r).checked : true;
    var pctd = covA * pct / 100, applied = trig ? pctd : flat;
    set("[data-o=pd]", money(applied), r);
    set("[data-o=pctd]", money(pctd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - applied)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(Math.max(0, Math.min(loss, applied) - Math.min(loss, flat))), r);
    var t;
    if (!loss) t = "Enter an estimated loss to compare payments.";
    else if (!trig) t = "If the hurricane trigger wasn’t met, the regular deductible usually applies. Confirm the trigger wording in your policy.";
    else if (loss <= applied) t = "This loss falls entirely within the hurricane deductible, so no claim payment would be owed under it.";
    else t = "The loss exceeds the hurricane deductible by " + money(loss - applied) + ".";
    set("[data-o=below]", t, r);
    var bar = $(".stack", r);
    if (bar) {
      var a = loss > 0 ? Math.min(applied, loss) / loss * 100 : 0;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (loss > 0 ? 100 - a : 0) + "%";
    }
  });

  /* 5. Claim calendar builder */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value, list = $("[data-o=timeline]", r);
    if (!d0) { plan = []; list.innerHTML = "<li><b>Pick your date of loss</b><span>Your milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00"), today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require prompt notice. Report as soon as you can; this is your own target." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs and save receipts", n: "Tarping, drying and board-up protect the claim and are usually reimbursable." },
      { d: add(num($("[name=inv]", r))), t: "Contents inventory target", n: "Room-by-room list with photos, ages and replacement prices." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies count this window from the carrier’s written request. Check your letter." },
      { d: add(num($("[name=rcd]", r))), t: "Depreciation recovery window closes", n: "Finish repairs and send invoices to collect holdback. Confirm the exact period in your policy." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Read the Suit Against Us condition and talk to a Connecticut attorney well before this date." }
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
      var remind = $('[data-tool="dates"] [name=remind]'); remind = remind && remind.checked;
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (dt) { return dt.getFullYear() + pad(dt.getMonth() + 1) + pad(dt.getDate()); };
      var esc = function (s) { return s.replace(/\\/g, "\\\\").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Connecticut Insurance Appraiser//Claim Calendar//EN", "CALSCALE:GREGORIAN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:cia-" + ds(p.d) + "-" + i + "@connecticutinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + esc(p.t), "DESCRIPTION:" + esc(p.n));
        if (remind) ics.push("BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc(p.t), "TRIGGER:-P14D", "END:VALARM");
        ics.push("END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "connecticut-claim-deadlines.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Appraisal readiness checkup */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1E8A55" : pct >= 45 ? "#1F64E5" : "#FF6B57"; }
      set("[data-o=verdict]", !answered ? "Answer the questions to see your score." : pct >= 75 ? "Strong file. You have what an appraisal panel expects; the next step is a professional review of the dollar gap." : pct >= 45 ? "Getting there. Close the gaps below before you demand appraisal; each missing piece weakens your number." : "Not ready yet. Demanding appraisal now risks locking in a low award. Work through the list below first.", r);
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

  /* 7. Fallen tree claim calculator */
  tool("tree", function (r) {
    var hit = Math.max(0, Math.floor(num($("[name=hit]", r)))), blk = Math.max(0, Math.floor(num($("[name=blk]", r)))), yard = Math.max(0, Math.floor(num($("[name=yard]", r))));
    var cost = num($("[name=cost]", r)), per = num($("[name=per]", r)), tot = num($("[name=tot]", r));
    var crane = num($("[name=crane]", r)), rep = num($("[name=rep]", r)), ded = num($("[name=ded]", r));
    var dwell = crane + rep;
    var billed = (hit + blk + yard) * cost;
    var allowed = Math.min(tot, (hit + blk) * Math.min(per, cost));
    var oop = Math.max(0, billed - allowed);
    var pay = Math.max(0, dwell + allowed - ded);
    set("[data-o=dwell]", money(dwell), r);
    set("[data-o=billed]", money(billed), r);
    set("[data-o=allowed]", money(allowed), r);
    set("[data-o=oop]", money(oop), r);
    set("[data-o=pay]", money(pay), r);
    var t = yard > 0 ? yard + (yard === 1 ? " tree that hit nothing is" : " trees that hit nothing are") + " usually not eligible for debris removal unless it blocks a driveway or ramp. " : "";
    t += (hit + blk) * Math.min(per, cost) > tot ? "The per-loss limit caps debris removal at " + money(tot) + ". " : "";
    t += "Ask your tree service to split removal from the house, hauling and stump work on the invoice.";
    set("[data-o=tmsg]", t, r);
  });

  var yr = $("[data-year]"); if (yr) yr.textContent = new Date().getFullYear();
})();
