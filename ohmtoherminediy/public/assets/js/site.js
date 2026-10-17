/* Oh, Mother Mine DIY — shared site script: nav, effects, small widgets */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Mobile nav ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  var header = document.querySelector(".site-header");
  function setNav(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("open", open);
    document.body.classList.toggle("nav-open", open);
    if (open) {
      var r = header.getBoundingClientRect();
      doc.style.setProperty("--top-offset", Math.max(0, r.top) + "px");
      var first = nav.querySelector("a");
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 150);
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setNav(toggle.getAttribute("aria-expanded") !== "true"); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { setNav(false); toggle.focus(); }
      if (e.key === "Tab" && nav.classList.contains("open")) {
        var items = [toggle].concat([].slice.call(nav.querySelectorAll("a")));
        var i = items.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
        else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
      }
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 960 && nav.classList.contains("open")) setNav(false); });
  }

  /* ---------- Scroll effects ---------- */
  var toTop = document.querySelector(".to-top");
  var progress = document.querySelector(".reading-progress");
  var article = document.querySelector(".prose");
  var heroImg = document.querySelector(".hero-media img");
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("scrolled", y > 10);
    if (toTop) toTop.classList.toggle("show", y > 700);
    if (progress && article) {
      var r = article.getBoundingClientRect();
      var total = r.height - window.innerHeight * 0.6;
      var p = Math.min(1, Math.max(0, -r.top / Math.max(1, total)));
      progress.style.transform = "scaleX(" + p + ")";
    }
    if (heroImg && !reduce && y < 1200) heroImg.style.setProperty("--py", (y * 0.25) + "px");
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add("in"); }); }

  /* ---------- Count-up numbers ---------- */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseFloat(el.getAttribute("data-count")), suf = el.getAttribute("data-suffix") || "", t0 = null;
        cio.unobserve(el);
        if (reduce) { el.textContent = end + suf; return; }
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / 1600), e = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(end * e) + suf;
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- Card tilt (pointer devices) ---------- */
  if (!reduce && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll("[data-tilt]").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = "translateY(-8px) perspective(900px) rotateX(" + (-y * 5) + "deg) rotateY(" + (x * 6) + "deg)";
      });
      card.addEventListener("mouseleave", function () { card.style.transform = ""; });
    });
  }

  /* ---------- Before / after slider ---------- */
  document.querySelectorAll(".ba").forEach(function (ba) {
    var input = ba.querySelector("input[type=range]");
    function set(v) { ba.style.setProperty("--pos", v + "%"); }
    if (input) input.addEventListener("input", function () { set(input.value); });
    if (!reduce && "IntersectionObserver" in window) {
      var played = false;
      new IntersectionObserver(function (en, obs) {
        if (en[0].isIntersecting && !played) {
          played = true; obs.disconnect();
          var t0 = null;
          (function anim(ts) {
            if (!t0) t0 = ts;
            var p = Math.min(1, (ts - t0) / 1800), v = 50 + Math.sin(p * Math.PI * 2) * 28;
            set(v); if (input) input.value = v;
            if (p < 1) requestAnimationFrame(anim);
          })(performance.now());
        }
      }, { threshold: 0.6 }).observe(ba);
    }
  });

  /* ---------- Range fill ---------- */
  function fillRange(r) { var p = (r.value - r.min) / (r.max - r.min) * 100; r.style.setProperty("--fill", p + "%"); }
  document.querySelectorAll("input[type=range]").forEach(function (r) { fillRange(r); r.addEventListener("input", function () { fillRange(r); }); });
  window.OMM = window.OMM || {};
  window.OMM.fillRange = fillRange;

  /* ---------- Toast ---------- */
  window.OMM.toast = function (msg) {
    var t = document.querySelector(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.classList.add("show");
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove("show"); }, 2200);
  };

  /* ---------- Table of contents highlight ---------- */
  var tocLinks = document.querySelectorAll(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove("active"); }); var a = map[en.target.id]; if (a) a.classList.add("active"); }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    document.querySelectorAll(".prose h2[id]").forEach(function (h) { tio.observe(h); });
  }

  /* ---------- Supplies checklist (remembered per post) ---------- */
  var sup = document.querySelector(".supplies[data-key]");
  if (sup) {
    var key = "omm-sup-" + sup.getAttribute("data-key"), saved = [];
    try { saved = JSON.parse(localStorage.getItem(key) || "[]"); } catch (e) { saved = []; }
    sup.querySelectorAll("li").forEach(function (li, i) {
      li.setAttribute("role", "checkbox"); li.setAttribute("tabindex", "0");
      function sync() { li.setAttribute("aria-checked", li.classList.contains("done") ? "true" : "false"); }
      if (saved.indexOf(i) > -1) li.classList.add("done");
      sync();
      function flip() {
        li.classList.toggle("done"); sync();
        var d = []; sup.querySelectorAll("li").forEach(function (x, j) { if (x.classList.contains("done")) d.push(j); });
        try { localStorage.setItem(key, JSON.stringify(d)); } catch (e) { /* storage unavailable */ }
      }
      li.addEventListener("click", flip);
      li.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); flip(); } });
    });
  }

  /* ---------- Copy link ---------- */
  document.querySelectorAll("[data-copy-link]").forEach(function (b) {
    b.addEventListener("click", function () {
      var url = location.href;
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { window.OMM.toast("Link copied!"); }, function () { window.OMM.toast(url); });
      else window.OMM.toast(url);
    });
  });

  /* ---------- Project filter (blog index) ---------- */
  var grid = document.querySelector("[data-filter-grid]");
  if (grid) {
    var chips = document.querySelectorAll("[data-filter]");
    var search = document.querySelector("[data-search]");
    var empty = document.querySelector(".empty-msg");
    var current = "all";
    function apply() {
      var q = search ? search.value.trim().toLowerCase() : "", shown = 0;
      grid.querySelectorAll(".card").forEach(function (c) {
        var okCat = current === "all" || c.getAttribute("data-cat") === current;
        var okQ = !q || c.textContent.toLowerCase().indexOf(q) > -1;
        var on = okCat && okQ;
        c.classList.toggle("hide", !on); if (on) shown++;
      });
      if (empty) empty.style.display = shown ? "none" : "block";
    }
    chips.forEach(function (ch) {
      ch.addEventListener("click", function () {
        current = ch.getAttribute("data-filter");
        chips.forEach(function (x) { x.setAttribute("aria-pressed", x === ch ? "true" : "false"); });
        apply();
      });
    });
    if (search) search.addEventListener("input", apply);
    var q0 = new URLSearchParams(location.search).get("q");
    if (search && q0) { search.value = q0; apply(); }
  }

  /* ---------- Forms (contact + newsletter) ---------- */
  document.querySelectorAll("form[data-ajax]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = f.querySelector(".form-note"), btn = f.querySelector("button[type=submit]");
      if (btn) btn.disabled = true;
      if (note) note.textContent = "Sending…";
      fetch(f.getAttribute("action"), { method: "POST", body: new FormData(f), headers: { "Accept": "application/json" } })
        .then(function (r) { return r.json().catch(function () { return { ok: r.ok }; }); })
        .then(function (d) {
          if (d && d.ok) { if (note) note.textContent = d.message || "Thank you! We'll be in touch."; f.reset(); }
          else { if (note) note.textContent = (d && d.message) || "Something went wrong. Please email info@ohmtoherminediy.com."; }
        })
        .catch(function () { if (note) note.textContent = "Couldn't send right now. Please email info@ohmtoherminediy.com."; })
        .then(function () { if (btn) btn.disabled = false; });
    });
  });

  var yr = document.querySelector("[data-year]");
  if (yr) yr.textContent = new Date().getFullYear();
})();
