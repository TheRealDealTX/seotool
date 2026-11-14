/* Virginia Insurance Appraiser — site script: navigation, scroll effects, forms and claim tools. No dependencies. */
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
  var closeDrops = function (except) {
    $$(".has-drop.open").forEach(function (li) { if (li === except) return; li.classList.remove("open"); $(".drop-btn", li).setAttribute("aria-expanded", "false"); });
  };
  $$(".has-drop").forEach(function (li) {
    var btn = $(".drop-btn", li), t;
    btn.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var open = !li.classList.contains("open");
      closeDrops(li);
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    li.addEventListener("mouseenter", function () { if (!window.matchMedia("(hover: hover)").matches) return; clearTimeout(t); closeDrops(li); li.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
    li.addEventListener("mouseleave", function () { if (!window.matchMedia("(hover: hover)").matches) return; t = setTimeout(function () { li.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 180); });
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".has-drop")) closeDrops(); });

  /* ---------- mobile drawer (lives outside the header) ---------- */
  var drawer = $("#drawer"), burger = $(".burger"), shade = $(".drawer-shade"), lastFocus = null;
  var openDrawer = function () {
    lastFocus = document.activeElement;
    shade.hidden = false;
    drawer.removeAttribute("inert");
    drawer.setAttribute("aria-hidden", "false");
    burger.setAttribute("aria-expanded", "true");
    requestAnimationFrame(function () { body.classList.add("drawer-open", "lock"); });
    setTimeout(function () { var x = $(".drawer-x", drawer); if (x) x.focus(); }, 60);
  };
  var closeDrawer = function () {
    if (!body.classList.contains("drawer-open")) return;
    body.classList.remove("drawer-open", "lock");
    drawer.setAttribute("inert", "");
    drawer.setAttribute("aria-hidden", "true");
    burger.setAttribute("aria-expanded", "false");
    setTimeout(function () { if (!body.classList.contains("drawer-open")) shade.hidden = true; }, 320);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  };
  if (drawer && burger && shade) {
    burger.addEventListener("click", openDrawer);
    $$("[data-close]").forEach(function (el) { el.addEventListener("click", closeDrawer); });
    $$("a", drawer).forEach(function (a) { a.addEventListener("click", closeDrawer); });
    $$(".acc-btn", drawer).forEach(function (b) {
      b.addEventListener("click", function () {
        var open = b.getAttribute("aria-expanded") !== "true";
        $$(".acc-btn", drawer).forEach(function (o) { o.setAttribute("aria-expanded", "false"); $("#" + o.getAttribute("aria-controls")).hidden = true; });
        b.setAttribute("aria-expanded", open ? "true" : "false");
        $("#" + b.getAttribute("aria-controls")).hidden = !open;
      });
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1180) closeDrawer(); });
  }
  document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { closeDrops(); closeDrawer(); } });

  /* ---------- scroll: solid header, progress bar, back-to-top, parallax, process track ---------- */
  var head = $(".head"), bar = $(".progress span"), toTop = $(".to-top"), px = $$("[data-parallax]"), track = $("[data-track]");
  var ticking = false;
  var onScroll = function () {
    var y = window.scrollY || window.pageYOffset, vh = window.innerHeight, h = document.documentElement.scrollHeight - vh;
    if (head) head.classList.toggle("solid", y > 30);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (toTop) toTop.classList.toggle("show", y > 800);
    if (!reduce) px.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = parseFloat(el.getAttribute("data-parallax")) || 0.15;
      var lim = el.offsetHeight * 0.08, dy = Math.max(-lim, Math.min(lim, (r.top + r.height / 2 - vh / 2) * -k));
      el.style.transform = "translate3d(0," + dy.toFixed(1) + "px,0)";
    });
    if (track) {
      var tr = track.getBoundingClientRect(), mid = vh * 0.7;
      var p = Math.max(0, Math.min(1, (mid - tr.top) / Math.max(1, tr.height)));
      track.style.setProperty("--p", reduce ? 1 : p.toFixed(3));
      var vertical = window.innerWidth <= 1020;
      $$(".step", track).forEach(function (s, i, all) {
        var on = vertical ? s.getBoundingClientRect().top < mid : p >= (i + 0.5) / all.length;
        s.classList.toggle("on", reduce || on);
      });
    }
    ticking = false;
  };
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------- staggered reveal + counters ---------- */
  var count = function (el) {
    var end = parseFloat(el.getAttribute("data-count")), t0 = null, dur = 1500;
    if (reduce || !isFinite(end)) return;
    var step = function (t) { if (!t0) t0 = t; var q = Math.min(1, (t - t0) / dur); el.textContent = Math.round(end * (1 - Math.pow(1 - q, 3))); if (q < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  $$("[data-stagger]").forEach(function (g) { $$(".rv", g).forEach(function (c, i) { c.style.setProperty("--d", (i % 6) * 0.07 + "s"); }); });
  var targets = $$(".rv, .ledger");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        $$("[data-count]", en.target).forEach(count);
        io.unobserve(en.target);
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -30px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else { targets.forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- glossary filter ---------- */
  var gf = $("#gloss-filter");
  if (gf) gf.addEventListener("input", function () {
    var q = gf.value.trim().toLowerCase(), shown = 0;
    $$(".gterm").forEach(function (g) { var hit = !q || g.textContent.toLowerCase().indexOf(q) > -1; g.hidden = !hit; if (hit) shown++; });
    set("[data-gloss-count]", shown + (shown === 1 ? " term" : " terms") + (q ? " match “" + gf.value.trim() + "”" : ""));
  });

  /* ---------- lead forms ---------- */
  $$("form[data-lead]").forEach(function (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var msg = $(".form-msg", form);
      msg.className = "form-msg";
      var bad = $$("[required]", form).filter(function (f) { return f.type === "checkbox" ? !f.checked : !f.value.trim(); });
      $$("[required]", form).forEach(function (f) { f.setAttribute("aria-invalid", bad.indexOf(f) > -1 ? "true" : "false"); });
      if (bad.length) { msg.textContent = "Please complete the required fields, including the consent box."; msg.classList.add("err"); bad[0].focus(); return; }
      var btn = $("button[type=submit]", form), label = btn.innerHTML;
      btn.disabled = true; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d && d.ok) { form.reset(); msg.textContent = "Thank you. Your claim details were received, and someone from Virginia Insurance Appraiser will be in touch, usually within one business day."; msg.classList.add("ok"); }
          else { throw new Error("send failed"); }
        })
        .catch(function () { msg.innerHTML = "We couldn’t send the form just now. Please call <a href=\"tel:+18445371427\">(844) 537-1427</a> or email <a href=\"mailto:info@virginiainsuranceappraiser.com\">info@virginiainsuranceappraiser.com</a>."; msg.classList.add("err"); })
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
      else if (gap <= 0) t = "Your number isn’t higher than the carrier’s. Appraisal resolves how much a covered loss costs — with no gap, there’s nothing to appraise.";
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
    if (steep) steep.textContent = pitch >= 8 ? "At " + pitch + "/12 most estimating software adds a steep-roof charge — check that the carrier’s estimate includes it." : pitch >= 7 ? "At 7/12 some carriers begin applying steep charges. Confirm how your estimate treats this pitch." : "Walkable pitch: no steep-roof charge is typically expected.";
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
      { d: add(num($("[name=pol]", r))), t: "Sworn proof of loss (if requested)", n: "Many policies give 60 days after the carrier’s request. Count from the request date in your letter." },
      { d: add(num($("[name=rcd]", r))), t: "Recoverable depreciation window closes", n: "Policies set a deadline to complete repairs and claim holdback. Confirm the exact number of days in your policy." },
      { d: add(num($("[name=suit]", r))), t: "Policy suit-limitation date", n: "Virginia policies commonly allow two years from the loss to file suit. Talk to a Virginia attorney well before this date." }
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
      var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Virginia Insurance Appraiser//Claim Planner//EN"];
      plan.forEach(function (p, i) {
        var end = new Date(p.d); end.setDate(end.getDate() + 1);
        ics.push("BEGIN:VEVENT", "UID:gia-" + ds(p.d) + "-" + i + "@virginiainsuranceappraiser.com", "DTSTAMP:" + stamp, "DTSTART;VALUE=DATE:" + ds(p.d), "DTEND;VALUE=DATE:" + ds(end), "SUMMARY:" + p.t, "DESCRIPTION:" + p.n.replace(/,/g, "\\,"), "END:VEVENT");
      });
      ics.push("END:VCALENDAR");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([ics.join("\r\n")], { type: "text/calendar" }));
      a.download = "virginia-claim-deadlines.ics";
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
      if (arc) { var L = 251.3; arc.style.strokeDashoffset = L - L * (answered ? pct : 0) / 100; arc.style.stroke = pct >= 75 ? "#1F7A4D" : pct >= 45 ? "#F08A4B" : "#00297B"; }
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

  /* 7. Fallen tree claim splitter */
  tool("tree", function (r) {
    var hit = Math.max(0, Math.floor(num($("[name=hit]", r)))), blk = Math.max(0, Math.floor(num($("[name=block]", r)))), oth = Math.max(0, Math.floor(num($("[name=other]", r))));
    var per = num($("[name=per]", r)), crane = num($("[name=crane]", r)), struct = num($("[name=struct]", r));
    var cap1 = num($("[name=cap1]", r)), cap2 = num($("[name=cap2]", r)), ded = num($("[name=ded]", r));
    var dwell = crane + struct;
    var eligible = hit + blk;
    var rmAll = (eligible + oth) * per;
    var rmCov = Math.min(eligible * Math.min(per, cap1), cap2);
    var rmGap = rmAll - rmCov;
    var covered = dwell + rmCov;
    var pay = Math.max(0, covered - ded);
    var dedPaid = Math.min(ded, covered);
    var oop = rmGap + dedPaid;
    set("[data-o=dwell]", money(dwell), r);
    set("[data-o=rmall]", money(rmAll), r);
    set("[data-o=rmcov]", money(rmCov), r);
    set("[data-o=rmgap]", money(rmGap), r);
    set("[data-o=oop]", money(oop), r);
    set("[data-o=pay]", money(pay), r);
    var stack = $(".stack", r), tot = Math.max(1, dwell + rmAll);
    if (stack) {
      var payDwell = Math.max(0, dwell - dedPaid), payRm = Math.max(0, pay - payDwell);
      stack.children[0].style.width = (payDwell / tot * 100) + "%";
      stack.children[1].style.width = (payRm / tot * 100) + "%";
      stack.children[2].style.width = (oop / tot * 100) + "%";
    }
    var m;
    if (!eligible && !dwell) m = "Enter your trees and costs to see the split.";
    else if (eligible * Math.min(per, cap1) > cap2) m = "The per-loss removal limit caps what the policy pays for hauling trees away. Lifting a tree off the house is normally part of the dwelling repair instead.";
    else if (oth > 0) m = "Trees that fell without hitting a covered structure or blocking a driveway usually aren’t covered for removal, so their cost stays with you.";
    else m = "Removal for these trees falls within the limits you entered. Confirm those limits in your own policy.";
    set("[data-o=tmsg]", m, r);
  });

  var y = $("[data-year]"); if (y) y.textContent = new Date().getFullYear();
})();
