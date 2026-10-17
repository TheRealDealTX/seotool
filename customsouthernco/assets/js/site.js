/* Custom Southern Co. — header, mobile nav, scroll effects, blog filter */
(function () {
  "use strict";
  var doc = document.documentElement;
  var body = document.body;
  doc.classList.add("js");

  /* ---- mobile nav ---- */
  var burger = document.querySelector(".burger");
  var mnav = document.getElementById("mobile-nav");
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    mnav.setAttribute("aria-hidden", String(!open));
    if (open) {
      var first = mnav.querySelector("a");
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 350);
    }
  }
  if (burger && mnav) {
    burger.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
    mnav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && body.classList.contains("nav-open")) { setNav(false); burger.focus(); }
      if (e.key === "Tab" && body.classList.contains("nav-open")) {
        var f = [burger].concat([].slice.call(mnav.querySelectorAll("a")));
        var i = f.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 980 && body.classList.contains("nav-open")) setNav(false); });
  }

  /* ---- tools dropdown ---- */
  var drop = document.querySelector(".has-drop");
  if (drop) {
    var dbtn = drop.querySelector(".drop-btn");
    dbtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = !drop.classList.contains("is-open");
      drop.classList.toggle("is-open", open);
      dbtn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (e) {
      if (!drop.contains(e.target)) { drop.classList.remove("is-open"); dbtn.setAttribute("aria-expanded", "false"); }
    });
    drop.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { drop.classList.remove("is-open"); dbtn.setAttribute("aria-expanded", "false"); dbtn.focus(); }
    });
  }

  /* ---- scroll: header state, progress, back-to-top, hero parallax ---- */
  var header = document.querySelector(".site-header");
  var bar = document.querySelector(".progress span");
  var top = document.querySelector(".to-top");
  var heroBg = document.querySelector(".hero-bg");
  var isPost = body.classList.contains("is-post");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 10);
    if (top) top.classList.toggle("show", y > 700);
    if (bar && isPost) {
      var h = doc.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (h > 0 ? Math.min(1, y / h) : 0) + ")";
    }
    if (heroBg && !reduce && y < window.innerHeight) heroBg.style.transform = "translate3d(0," + y * 0.25 + "px,0)";
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  /* ---- reveal on scroll + counters ---- */
  var reveals = document.querySelectorAll(".reveal");
  function countUp(el) {
    var end = parseInt(el.getAttribute("data-count"), 10) || 0, start = null;
    function step(t) {
      if (!start) start = t;
      var p = Math.min(1, (t - start) / 1400);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add("in");
        en.target.querySelectorAll("[data-count]").forEach(countUp);
        io.unobserve(en.target);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
    document.querySelectorAll("[data-count]").forEach(function (el) { el.textContent = el.getAttribute("data-count"); });
  }

  /* ---- table of contents highlight ---- */
  var tocLinks = document.querySelectorAll(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("is-active"); });
          var a = map[en.target.id];
          if (a) a.classList.add("is-active");
        }
      });
    }, { rootMargin: "0px 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* ---- season tabs ---- */
  var tabs = document.querySelectorAll('[role="tab"]');
  function selectTab(t) {
    tabs.forEach(function (o) {
      var on = o === t;
      o.setAttribute("aria-selected", String(on));
      o.tabIndex = on ? 0 : -1;
      document.getElementById(o.getAttribute("aria-controls")).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t); });
    t.addEventListener("keydown", function (e) {
      var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
      if (!d) return;
      var n = tabs[(i + d + tabs.length) % tabs.length];
      selectTab(n); n.focus();
    });
  });

  /* ---- blog filter + search ---- */
  var grid = document.querySelector("[data-blog-grid]");
  if (grid) {
    var cat = "all", q = "";
    var cards = grid.querySelectorAll(".card");
    var empty = document.querySelector("[data-blog-empty]");
    var chips = document.querySelectorAll("[data-filter]");
    var apply = function () {
      var shown = 0;
      cards.forEach(function (c) {
        var ok = (cat === "all" || c.dataset.cat === cat) && (!q || c.dataset.search.indexOf(q) > -1);
        c.classList.toggle("is-hidden", !ok);
        if (ok) { shown++; c.classList.add("in"); }
      });
      empty.hidden = shown > 0;
    };
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        chips.forEach(function (o) { o.classList.toggle("is-active", o === ch); });
        cat = ch.dataset.filter; apply();
      });
    });
    var s = document.querySelector("[data-blog-search]");
    s.addEventListener("input", function () { q = s.value.trim().toLowerCase(); apply(); });
  }

  /* ---- copy link ---- */
  document.querySelectorAll(".copy-link").forEach(function (b) {
    b.addEventListener("click", function () {
      var url = b.getAttribute("data-url"), label = b.querySelector("span");
      var done = function () { label.textContent = "Copied!"; setTimeout(function () { label.textContent = "Copy link"; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, done); else done();
    });
  });

  /* ---- supply checklist memory ---- */
  var sup = document.querySelectorAll(".supplies input");
  if (sup.length) {
    var key = "csc-sup:" + location.pathname, saved = [];
    try { saved = JSON.parse(localStorage.getItem(key) || "[]"); } catch (e) { saved = []; }
    sup.forEach(function (box, i) {
      box.checked = saved.indexOf(i) > -1;
      box.addEventListener("change", function () {
        var on = [];
        sup.forEach(function (b, j) { if (b.checked) on.push(j); });
        try { localStorage.setItem(key, JSON.stringify(on)); } catch (e) { /* storage blocked */ }
      });
    });
  }

  /* ---- contact form ---- */
  var form = document.querySelector(".contact-form");
  if (form) {
    var status = form.querySelector(".form-status");
    var params = new URLSearchParams(location.search);
    if (params.has("sent")) {
      status.hidden = false;
      var ok = params.get("sent") === "1";
      status.classList.toggle("is-error", !ok);
      status.textContent = ok ? "Thanks! Your message is on its way." : "Sorry, something went wrong. Please email info@customsouthernco.com directly.";
    }
    form.addEventListener("submit", function (e) {
      if (!window.fetch) return;
      e.preventDefault();
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          status.hidden = false; status.textContent = d.message; status.classList.toggle("is-error", !d.ok);
          if (d.ok) form.reset();
        })
        .catch(function () {
          status.hidden = false; status.classList.add("is-error");
          status.textContent = "Sorry, something went wrong. Please email info@customsouthernco.com directly.";
        })
        .then(function () { btn.disabled = false; });
    });
  }
})();
