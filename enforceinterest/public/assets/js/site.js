/* Enforce Interest — site behaviour: nav, scroll effects, hero accrual meter, scroll clock, contact form. */
(function () {
  "use strict";
  var d = document, w = window;
  var reduce = w.matchMedia && w.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || d).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || d).querySelectorAll(s)); };
  var fmt = function (n) { return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); };

  /* ---------- header, progress, to-top, parallax (one rAF scroll loop) ---------- */
  var hdr = $(".site-header"), bar = $(".scroll-progress span"), top = $(".to-top");
  var par = $$("[data-parallax]");
  var ticking = false;
  function onScroll() {
    var y = w.scrollY || d.documentElement.scrollTop;
    var h = d.documentElement.scrollHeight - w.innerHeight;
    if (hdr) hdr.classList.toggle("scrolled", y > 8);
    if (bar) bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    if (top) top.classList.toggle("show", y > 900);
    if (!reduce) par.forEach(function (el) { el.style.transform = "translate3d(0," + (y * parseFloat(el.dataset.parallax)) + "px,0)"; });
    clockUpdate();
    ticking = false;
  }
  w.addEventListener("scroll", function () { if (!ticking) { ticking = true; w.requestAnimationFrame(onScroll); } }, { passive: true });
  if (top) top.addEventListener("click", function () { w.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- nav ---------- */
  var tog = $(".nav-toggle"), mob = $("#mobile-nav");
  if (tog && mob) {
    var isOpen = function () { return tog.getAttribute("aria-expanded") === "true"; };
    var lockY = 0;
    var setMenu = function (open) {
      if (open === isOpen()) return;
      if (open) {  // freeze the page where it is (overflow:hidden alone lets iOS and some browsers jump)
        lockY = w.scrollY || d.documentElement.scrollTop;
        d.body.style.top = -lockY + "px";
      }
      tog.setAttribute("aria-expanded", open);
      tog.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      mob.classList.toggle("open", open);
      if (open) mob.removeAttribute("inert"); else mob.setAttribute("inert", "");
      d.documentElement.classList.toggle("nav-open", open);
      if (open) mob.scrollTop = 0;
      else { d.body.style.top = ""; w.scrollTo({ top: lockY, left: 0, behavior: "instant" }); }
    };
    tog.addEventListener("click", function () { setMenu(!isOpen()); });
    mob.addEventListener("click", function (e) {
      var h = e.target.closest(".mn-head");
      if (h) {  // accordion section
        var g = h.parentNode, o = !g.classList.contains("open");
        g.classList.toggle("open", o);
        h.setAttribute("aria-expanded", o);
        return;
      }
      var a = e.target.closest("a");
      if (a) {  // close after choosing a link; same-page anchors scroll after the page is unlocked
        var hash = a.getAttribute("href").indexOf("#") > -1 && a.pathname === location.pathname ? a.hash : "";
        setMenu(false);
        if (hash) { e.preventDefault(); var t = d.querySelector(hash); if (t) t.scrollIntoView(); history.pushState(null, "", hash); }
      }
    });
    d.addEventListener("keydown", function (e) { if (e.key === "Escape" && isOpen()) { setMenu(false); tog.focus({ preventScroll: true }); } });
    w.addEventListener("resize", function () { if (w.innerWidth > 1060 && isOpen()) setMenu(false); });
    w.addEventListener("pageshow", function () { if (isOpen()) setMenu(false); });  // back/forward cache
  }
  $$(".nav-item").forEach(function (it) {
    var b = $("button", it), t;
    var set = function (o) { it.classList.toggle("open", o); b.setAttribute("aria-expanded", o); };
    b.addEventListener("click", function (e) { e.stopPropagation(); var o = !it.classList.contains("open"); $$(".nav-item.open").forEach(function (x) { if (x !== it) { x.classList.remove("open"); $("button", x).setAttribute("aria-expanded", "false"); } }); set(o); });
    it.addEventListener("mouseenter", function () { clearTimeout(t); set(true); });
    it.addEventListener("mouseleave", function () { t = setTimeout(function () { set(false); }, 160); });
  });
  d.addEventListener("click", function () { $$(".nav-item.open").forEach(function (x) { x.classList.remove("open"); $("button", x).setAttribute("aria-expanded", "false"); }); });
  d.addEventListener("keydown", function (e) { if (e.key === "Escape") d.dispatchEvent(new Event("click")); });

  /* ---------- reveal + counters ---------- */
  function countUp(el) {
    var end = parseFloat(el.dataset.count), suf = el.dataset.suffix || "", t0 = null, dur = 1400;
    if (reduce) { el.textContent = end + suf; return; }
    function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3); el.textContent = Math.round(end * e) + suf; if (p < 1) w.requestAnimationFrame(step); }
    w.requestAnimationFrame(step);
  }
  var targets = $$("[data-reveal],[data-stagger],.bar,.rate-cards");
  if ("IntersectionObserver" in w) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        $$("[data-count]", en.target).forEach(countUp);
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (t) { io.observe(t); });
  } else targets.forEach(function (t) { t.classList.add("in"); });
  w.addEventListener("load", function () { d.body.classList.add("loaded"); });
  setTimeout(function () { d.body.classList.add("loaded"); }, 600);

  /* ---------- hero accrual meter ---------- */
  var acc = $("#accrual");
  if (acc) {
    var st = { amt: 50000, rate: 18, days: 90, shown: 0, raf: 0 };
    var C1 = 402.1, C2 = 326.7;
    var el = {
      amt: $("[data-acc-amt]", acc), day: $("[data-acc-day]", acc), rate: $("[data-acc-rate]", acc),
      claim: $("[data-acc-claim]", acc), ringDay: $("[data-ring-day]", acc), slider: $("[data-acc-slider]", acc),
      fill: $(".ring .fill", acc), over: $(".ring .over", acc)
    };
    var paint = function (days) {
      var v = st.amt * st.rate / 100 / 365 * days, s = fmt(v), i = s.lastIndexOf(".");
      el.amt.innerHTML = s.slice(0, i) + "<small>" + s.slice(i) + "</small>";
      el.ringDay.textContent = Math.round(days);
      // outer ring: first 365 days late; inner ring: second year
      el.fill.style.strokeDashoffset = C1 * (1 - Math.min(days, 365) / 365);
      el.over.style.strokeDashoffset = C2 * (1 - Math.max(0, Math.min(days - 365, 365)) / 365);
    };
    var meta = function () {
      el.day.textContent = fmt(st.amt * st.rate / 100 / 365);
      el.rate.textContent = st.rate.toFixed(2) + "% / yr";
      el.claim.textContent = "$" + st.amt.toLocaleString("en-US");
    };
    var animateTo = function (target) {
      cancelAnimationFrame(st.raf);
      if (reduce) { st.shown = target; paint(target); return; }
      var from = st.shown, t0 = null, dur = 900;
      var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3); st.shown = from + (target - from) * e; paint(st.shown); if (p < 1) st.raf = requestAnimationFrame(step); };
      st.raf = requestAnimationFrame(step);
    };
    $$("[data-rate]", acc).forEach(function (b) { b.addEventListener("click", function () { st.rate = parseFloat(b.dataset.rate); $$("[data-rate]", acc).forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); meta(); paint(st.shown); }); });
    $$("[data-amt]", acc).forEach(function (b) { b.addEventListener("click", function () { st.amt = parseFloat(b.dataset.amt); $$("[data-amt]", acc).forEach(function (x) { x.setAttribute("aria-pressed", x === b); }); meta(); paint(st.shown); }); });
    el.slider.addEventListener("input", function () { st.days = +el.slider.value; cancelAnimationFrame(st.raf); st.shown = st.days; paint(st.days); });
    meta(); paint(0);
    setTimeout(function () { animateTo(st.days); }, 500);
    // slow "live" drift: a few extra seconds of accrual so the cents visibly move
    if (!reduce) setInterval(function () { if (Math.abs(st.shown - st.days) < 0.5) { st.shown += 1 / 2880; paint(st.shown); } }, 1000);
  }

  /* ---------- scroll-driven 60-day clock ---------- */
  var steps = $$("[data-step]").filter(function (s) { return s.dataset.day !== undefined; });
  var clockDay = $("[data-clock-day]"), clockBar = $("[data-clock-bar]"), clockStatus = $("[data-clock-status]"), prog = $("[data-steps-prog]");
  var lastActive = -1;
  function clockUpdate() {
    if (!steps.length || !clockDay) return;
    var mid = w.innerHeight * 0.55, active = 0;
    steps.forEach(function (s, i) { if (s.getBoundingClientRect().top < mid) active = i; });
    var box = steps[0].parentNode.getBoundingClientRect();
    var p = Math.max(0, Math.min(1, (mid - box.top) / box.height));
    if (prog) prog.style.transform = "scaleY(" + p + ")";
    var a = steps[active], b = steps[Math.min(active + 1, steps.length - 1)];
    var ra = a.getBoundingClientRect().top, rb = b.getBoundingClientRect().top;
    var f = b === a ? 0 : Math.max(0, Math.min(1, (mid - ra) / (rb - ra || 1)));
    var day = Math.round(+a.dataset.day + (+b.dataset.day - +a.dataset.day) * f);
    clockDay.textContent = day > 60 ? "Day " + day + " · late" : "Day " + day;
    clockDay.style.color = day > 60 ? "#ff8a70" : "";
    clockBar.style.transform = "scaleX(" + Math.min(1, day / 80) + ")";
    if (active !== lastActive) {
      steps.forEach(function (s, i) { s.classList.toggle("active", i <= active); });
      clockStatus.innerHTML = a.dataset.status;
      lastActive = active;
    }
  }

  /* ---------- Hinojos before/after tabs ---------- */
  $$('[role="tablist"]').forEach(function (tl) {
    var tabs = $$('[role="tab"]', tl);
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        tabs.forEach(function (x) { var on = x === t; x.setAttribute("aria-selected", on); var p = d.getElementById(x.getAttribute("aria-controls")); if (p) p.hidden = !on; });
      });
    });
  });

  /* ---------- TOC active state ---------- */
  var tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in w) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove("active"); }); var a = map[en.target.id]; if (a) a.classList.add("active"); } });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var h = d.getElementById(id); if (h) tio.observe(h); });
  }

  /* ---------- blog filters ---------- */
  var filters = $("[data-filters]");
  if (filters) {
    filters.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      $$("button", filters).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
      var f = b.dataset.filter;
      $$("[data-posts] > a").forEach(function (c) { c.style.display = f === "all" || c.dataset.cat === f ? "" : "none"; });
    });
  }

  /* ---------- contact form ---------- */
  var form = $("#claim-form");
  if (form) {
    var started = Date.now();
    var tfield = form.querySelector('input[name="t"]');
    var drop = $("#file-drop"), lab = $("[data-file-label]");
    var fileIn = drop && $("input", drop);
    if (fileIn) fileIn.addEventListener("change", function () {
      var n = fileIn.files.length, tot = 0; for (var i = 0; i < n; i++) tot += fileIn.files[i].size;
      lab.textContent = n ? n + " file" + (n > 1 ? "s" : "") + " selected (" + (tot / 1048576).toFixed(1) + " MB)" : "Drop or choose claim letters, payment stubs, estimates";
      drop.classList.toggle("has", n > 0);
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var status = $(".form-status", form), btn = $('button[type="submit"]', form);
      status.className = "form-status"; status.textContent = "";
      if (!form.checkValidity()) { status.className = "form-status err"; status.textContent = "Please fill in your name, a valid email, a short description and the consent box."; form.reportValidity && form.reportValidity(); return; }
      if (fileIn && fileIn.files.length) {
        var tot = 0; for (var i = 0; i < fileIn.files.length; i++) tot += fileIn.files[i].size;
        if (fileIn.files.length > 5 || tot > 10 * 1048576) { status.className = "form-status err"; status.textContent = "Please attach up to 5 files, 10 MB total — or email larger files to info@enforceinterest.com."; return; }
      }
      tfield.value = String(Math.round((Date.now() - started) / 1000));
      btn.disabled = true; var old = btn.innerHTML; btn.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: false, message: "Something went wrong. Please email info@enforceinterest.com." }; }); })
        .then(function (j) { status.className = "form-status " + (j.ok ? "ok" : "err"); status.textContent = j.message; if (j.ok) { form.reset(); if (lab) lab.textContent = "Drop or choose claim letters, payment stubs, estimates"; } })
        .catch(function () { status.className = "form-status err"; status.textContent = "We couldn't send that. Please email info@enforceinterest.com."; })
        .then(function () { btn.disabled = false; btn.innerHTML = old; });
    });
  }

  onScroll();
})();
