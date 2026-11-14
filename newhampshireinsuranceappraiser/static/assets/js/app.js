/* New Hampshire Insurance Appraiser — site script (nav, drawer, reveal, forms, claim calculators). No dependencies. Nothing is stored. */
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

  /* ---------- desktop dropdowns ---------- */
  var body = document.body;
  document.documentElement.classList.remove("no-js");
  var closeDrops = function () { $$(".menu li.open").forEach(function (o) { o.classList.remove("open"); var b = o.querySelector(".drop-btn"); if (b) b.setAttribute("aria-expanded", "false"); }); };
  $$(".menu .drop-btn").forEach(function (btn) {
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

  /* ---------- mobile drawer ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), scrim = $(".scrim");
  var openDrawer = function () {
    if (scrim) scrim.hidden = false;
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    burger.setAttribute("aria-expanded", "true");
    drawer.removeAttribute("inert"); drawer.setAttribute("aria-hidden", "false");
    setTimeout(function () { var c = $(".drawer-x", drawer); if (c) c.focus(); }, 60);
  };
  var closeDrawer = function () {
    var was = body.classList.contains("drawer-open");
    body.classList.remove("drawer-open", "lock");
    if (burger) burger.setAttribute("aria-expanded", "false");
    if (drawer) { drawer.setAttribute("inert", ""); drawer.setAttribute("aria-hidden", "true"); }
    if (scrim) setTimeout(function () { if (!body.classList.contains("drawer-open")) scrim.hidden = true; }, 320);
    if (was && burger && document.activeElement && drawer.contains(document.activeElement)) burger.focus();
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
    window.addEventListener("resize", function () { if (window.innerWidth > 1020) closeDrawer(); });
  }
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- header state, back-to-top, process fill ---------- */
  var head = $(".hdr"), toTop = $(".to-top");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY, h = document.documentElement.scrollHeight - window.innerHeight;
    if (head) head.classList.toggle("solid", y > 40);
    if (toTop) toTop.classList.toggle("show", y > 900);
    var st = $(".steps");
    if (st) {
      var sr = st.getBoundingClientRect(), vh = window.innerHeight;
      var pct = Math.max(0, Math.min(1, (vh * 0.85 - sr.top) / (vh * 0.6)));
      var fill = $(".steps-line i", st);
      if (fill) fill.style.width = (pct * 100).toFixed(1) + "%";
      var items = $$(".step", st);
      items.forEach(function (s, i) {
        var on = window.innerWidth > 1020 ? (pct > 0 && pct >= i / Math.max(1, items.length - 1) - 0.001) : s.getBoundingClientRect().top < vh * 0.7;
        s.classList.toggle("on", on);
      });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

  /* ---------- reveal, counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), suf = el.getAttribute("data-suffix") || "", t0 = null, dur = 1600;
    if (reduce) { el.textContent = end + suf; return; }
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suf; if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var reveal = function (el) { el.classList.add("in"); if (el.hasAttribute("data-count")) count(el); $$("[data-count]", el).forEach(count); };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 8) * 0.08 + "s"); }); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) { ents.forEach(function (en) { if (en.isIntersecting) { reveal(en.target); io.unobserve(en.target); } }); }, { threshold: .12, rootMargin: "0px 0px -40px 0px" });
    $$(".rv, .ribbon").forEach(function (el) { io.observe(el); });
  } else { $$(".rv, .ribbon").forEach(reveal); }

  /* ---------- region explorer ---------- */
  $$("[data-regions]").forEach(function (wrap) {
    var tabs = $$("[role=tab]", wrap);
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowDown" || e.key === "ArrowRight") { e.preventDefault(); select((i + 1) % tabs.length, true); }
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") { e.preventDefault(); select((i - 1 + tabs.length) % tabs.length, true); }
      });
    });
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        var on = i === j;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        $("#" + t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tabs[i].focus();
    }
  });

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase();
    var n = 0;
    $$(".glossary .g-item").forEach(function (it) {
      var hit = !q || it.textContent.toLowerCase().indexOf(q) > -1;
      it.hidden = !hit; if (hit) n++;
    });
    var c = $("[data-gloss-count]"); if (c) c.textContent = n + (n === 1 ? " term" : " terms") + (q ? " found" : "");
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      if (bad.length) { msg.textContent = "Please complete the highlighted fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form);
      btn.disabled = true; var label = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thanks — your claim details were received. A New Hampshire Insurance Appraiser team member will reach out, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error(d && d.error ? d.error : "send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@newhampshireinsuranceappraiser.com\">info@newhampshireinsuranceappraiser.com</a>."; msg.classList.add("err"); })
        .then(function () { btn.disabled = false; btn.innerHTML = label; });
    });
  });

  /* ---------- bind helper ---------- */
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

  /* 1. Appraisal value estimator (home mini + full tool) */
  tool("gap", function (r) {
    var ins = num($("[name=insurer]", r)), own = num($("[name=yours]", r));
    var land = $("[name=land]", r) ? num($("[name=land]", r)) / 100 : 0.6;
    var feeType = $("[name=feetype]", r) ? $("[name=feetype]", r).value : "flat";
    var fee = num($("[name=fee]", r));
    var ump = num($("[name=umpire]", r));
    var useUmp = $("[name=useump]", r) ? $("[name=useump]", r).checked : false;
    var gap = Math.max(0, own - ins);
    var award = ins + gap * land;
    var gain = award - ins;
    var cost = feeType === "pct" ? gain * fee / 100 : fee;
    if (useUmp) cost += ump / 2;
    var net = gain - cost;
    set("[data-o=gap]", money(gap), r);
    set("[data-o=award]", money(award), r);
    set("[data-o=gain]", money(gain), r);
    set("[data-o=cost]", money(cost), r);
    set("[data-o=net]", money(net), r);
    set("[data-o=pct]", ins > 0 ? Math.round(gap / ins * 100) + "%" : "—", r);
    var stack = $(".stack", r);
    if (stack) {
      var total = Math.max(own, award, 1);
      var s = stack.children;
      s[0].style.width = (ins / total * 100) + "%";
      s[1].style.width = (Math.max(0, net) / total * 100) + "%";
      s[2].style.width = (Math.min(cost, gain) / total * 100) + "%";
    }
    var m = $("[data-o=msg]", r);
    if (m) {
      var t;
      if (!ins || !own) t = "Enter both estimates to see the disputed amount.";
      else if (gap <= 0) t = "Your number isn’t higher than the insurer’s. Appraisal resolves how much a covered loss costs — with no gap, there’s nothing to appraise.";
      else if (net <= 0) t = "At these inputs, appraisal costs could absorb the entire recovery. A line-by-line estimate review is usually the better first step.";
      else if (gap / ins < 0.1 && gap < 5000) t = "The gap is real but narrow. Supplementing the claim with documentation may close it without formal appraisal.";
      else t = "The disputed amount is large enough that appraisal may be worth discussing. Have both estimates and your photos ready before you call.";
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

  /* 3. Roof squares */
  tool("roof", function (r) {
    var mode = $("[name=mode]:checked", r) ? $("[name=mode]:checked", r).value : "dims";
    $$("[data-mode]", r).forEach(function (el) { el.hidden = el.getAttribute("data-mode") !== mode; });
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), oh = num($("[name=oh]", r)) / 12;
    var foot = mode === "dims" ? (L + 2 * oh) * (W + 2 * oh) : num($("[name=area]", r));
    var pitch = num($("[name=pitch]", r));
    var mult = Math.sqrt(1 + Math.pow(pitch / 12, 2));
    var waste = num($("[name=waste]", r)) / 100;
    var surface = foot * mult;
    var sq = surface / 100;
    var order = sq * (1 + waste);
    var price = num($("[name=price]", r));
    set("[data-o=mult]", mult.toFixed(3), r);
    set("[data-o=surface]", Math.round(surface).toLocaleString() + " sq ft", r);
    set("[data-o=sq]", sq.toFixed(2), r);
    set("[data-o=order]", (Math.ceil(order * 3) / 3).toFixed(2), r);
    set("[data-o=bundles]", Math.ceil(order * 3).toString(), r);
    set("[data-o=cost]", price ? money(order * price) : "—", r);
    var steep = $("[data-o=steep]", r);
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge — check that the insurer’s estimate includes it." : pitch >= 7 ? "At 7/12 some insurers begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: no steep-roof charge is typically expected.";
  });

  /* 4. Percentage deductible */
  tool("deduct", function (r) {
    var covA = num($("[name=cova]", r)), pct = num($("[name=pct]", r)), flat = num($("[name=flat]", r)), loss = num($("[name=loss]", r));
    var pd = covA * pct / 100;
    set("[data-o=pd]", money(pd), r);
    set("[data-o=pdpay]", money(Math.max(0, loss - pd)), r);
    set("[data-o=flatpay]", money(Math.max(0, loss - flat)), r);
    set("[data-o=diff]", money(pd - flat), r);
    set("[data-o=below]", loss <= pd && loss > 0 ? "This loss falls entirely within the percentage deductible — no claim payment would be owed under that deductible." : loss > 0 ? "The loss exceeds the percentage deductible by " + money(loss - pd) + "." : "Enter an estimated loss to compare payouts.", r);
    var bar = $(".stack", r);
    if (bar && loss > 0) {
      var a = Math.min(pd, loss) / loss * 100;
      bar.children[0].style.width = a + "%";
      bar.children[1].style.width = (100 - a) + "%";
    }
  });

  /* 5. Claim deadline planner */
  var plan = [];
  tool("dates", function (r) {
    var d0 = $("[name=dol]", r).value;
    var list = $("[data-o=timeline]", r);
    if (!d0) { list.innerHTML = "<li><b>Pick your date of loss</b><span>Milestones will appear here.</span></li>"; return; }
    var base = new Date(d0 + "T12:00:00");
    var today = new Date(); today.setHours(12, 0, 0, 0);
    var add = function (days) { var d = new Date(base); d.setDate(d.getDate() + days); return d; };
    var fmt = function (d) { return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric", year: "numeric" }); };
    plan = [
      { d: add(num($("[name=notice]", r))), t: "Target date to report the claim", n: "Policies require ‘prompt’ notice. Report as soon as you can; this is a self-imposed target." },
      { d: add(num($("[name=mitig]", r))), t: "Finish temporary repairs & save receipts", n: "Tarps, water extraction and board-up protect the claim and are usually reimbursable." },
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies give 60 days after the insurer’s request. Count from the request date in your letter." },
      { d: add(num($("[name=rcd]", r))), t: "Recoverable depreciation window closes", n: "Policies set a deadline to complete repairs and claim holdback. Confirm the exact number of days in your policy." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date (check your policy)", n: "Use the window stated in your own policy. Talk to a New Hampshire attorney well before this date." }
    ].sort(function (a, b) { return a.d - b.d; });
    list.innerHTML = plan.map(function (p) {
      var diff = Math.round((p.d - today) / 864e5);
      var cls = diff < 0 ? "past" : diff <= 30 ? "soon" : "";
      var badge = diff < 0 ? Math.abs(diff) + " days ago" : diff === 0 ? "today" : "in " + diff + " days";
      return '<li class="' + cls + '"><b>' + fmt(p.d) + '<em>' + badge + '</em></b><strong>' + p.t + '</strong><br><span>' + p.n + '</span></li>';
    }).join("");
  });
  $$("[data-ics]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (!plan.length) return;
      var pad = function (n) { return (n < 10 ? "0" : "") + n; };
      var ds = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); };
      var stamp = new Date().toISOString().replace(/[-:]/g, "").split(".")[0] + "Z";
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//New Hampshire Insurance Appraiser//Claim Deadline Calendar//EN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:nhia-" + ds(p.d) + "-" + i + "@newhampshireinsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + p.t, "DESCRIPTION:" + p.n.replace(/,/g, "\\,"), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "nh-claim-deadlines.ics";
      document.body.appendChild(a); a.click(); a.remove();
    });
  });

  /* 6. Readiness score */
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#002A86" : pct >= 45 ? "#EFAE0E" : "#C9542C"; }
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

  /* 7. Snow weight on the roof (illustrative) */
  tool("snow", function (r) {
    var L = num($("[name=len]", r)), W = num($("[name=wid]", r)), d = num($("[name=depth]", r)), dens = num($("[name=dens]", r)), ice = num($("[name=ice]", r)), bench = num($("[name=bench]", r));
    var area = L * W;
    var psf = d / 12 * dens + ice / 12 * 57;
    var lbs = psf * area;
    set("[data-o=psf]", psf.toFixed(1) + " lb/ft²", r);
    set("[data-o=area]", Math.round(area).toLocaleString("en-US") + " sq ft", r);
    set("[data-o=lbs]", Math.round(lbs).toLocaleString("en-US") + " lb", r);
    set("[data-o=tons]", (lbs / 2000).toFixed(1) + " tons", r);
    var share = bench > 0 ? psf / bench : 0;
    set("[data-o=share]", bench > 0 ? Math.round(share * 100) + "%" : "—", r);
    var bar = $("[data-o=bar]", r);
    if (bar) { bar.style.width = Math.min(100, share * 100) + "%"; bar.style.background = share >= 0.75 ? "#C9542C" : share >= 0.5 ? "#EFAE0E" : "#002A86"; }
    var t;
    if (!area || (!d && !ice)) t = "Enter the roof size and the depth of snow or ice.";
    else if (!bench) t = "Add a benchmark load from your building official to compare.";
    else if (share >= 0.75) t = "That’s a heavy load relative to your benchmark. Don’t go up on the roof — consider calling a professional, and photograph any sagging, cracking or sticking doors.";
    else if (share >= 0.5) t = "A meaningful load. Watch for ice dams at the eaves and interior stains, and photograph conditions with the date.";
    else t = "Well under your benchmark on these inputs. Keep an eye on eaves and valleys, where drifting and ice build up first.";
    set("[data-o=smsg]", t, r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
