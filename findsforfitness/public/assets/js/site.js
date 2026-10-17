/* findsforfitness.com - header, mobile nav, scroll effects */
(function () {
  "use strict";
  var doc = document.documentElement;
  var body = document.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var panel = document.querySelector("[data-mobile-nav]");
  var lastFocus = null;

  function setNav(open) {
    if (!toggle || !panel) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    body.classList.toggle("nav-open", open);
    if (open) {
      lastFocus = document.activeElement;
      panel.hidden = false;
      // next frame so the transition runs after display is applied
      requestAnimationFrame(function () { panel.classList.add("is-open"); });
      var first = panel.querySelector("a");
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 250);
    } else {
      panel.classList.remove("is-open");
      if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    }
  }
  if (toggle && panel) {
    toggle.addEventListener("click", function () {
      setNav(toggle.getAttribute("aria-expanded") !== "true");
    });
    panel.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNav(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setNav(false);
      if (e.key === "Tab" && panel.classList.contains("is-open")) {
        var items = [toggle].concat(Array.prototype.slice.call(panel.querySelectorAll("a, button")));
        var i = items.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
        else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
      }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1080 && panel.classList.contains("is-open")) setNav(false);
    });
  }

  /* ---------- header + progress + parallax ---------- */
  var header = document.querySelector("[data-header]");
  var bar = document.querySelector(".progress span");
  var heroImg = document.querySelector(".hero-bg img, .page-hero-bg img, .post-hero-bg img");
  var lastY = window.scrollY;
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle("is-solid", y > 30);
      var hide = y > 400 && y > lastY + 4 && !body.classList.contains("nav-open");
      if (hide) header.classList.add("is-hidden");
      else if (y < lastY - 4 || y < 400) header.classList.remove("is-hidden");
    }
    if (bar) {
      var h = doc.scrollHeight - window.innerHeight;
      bar.style.setProperty("--p", h > 0 ? Math.min(1, y / h) : 0);
    }
    if (heroImg && !reduce && y < window.innerHeight * 1.2) heroImg.style.setProperty("--py", y * 0.25 + "px");
    lastY = y;
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- reveal on scroll ---------- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- count-up stats ---------- */
  document.querySelectorAll("[data-count]").forEach(function (el) {
    if (reduce) return;
    var end = parseInt(el.getAttribute("data-count"), 10), start = null;
    el.textContent = "0";
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min(1, (ts - start) / 1400);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    setTimeout(function () { requestAnimationFrame(step); }, 900);
  });

  /* ---------- card tilt + tool glow (pointer devices only) ---------- */
  if (window.matchMedia("(hover: hover) and (pointer: fine)").matches && !reduce) {
    document.querySelectorAll("[data-tilt]").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = "perspective(900px) rotateX(" + (-y * 5) + "deg) rotateY(" + (x * 6) + "deg) translateY(-6px)";
      });
      card.addEventListener("mouseleave", function () { card.style.transform = ""; });
    });
    document.querySelectorAll(".tool-card").forEach(function (c) {
      c.addEventListener("mousemove", function (e) {
        var r = c.getBoundingClientRect();
        c.style.setProperty("--mx", e.clientX - r.left + "px");
        c.style.setProperty("--my", e.clientY - r.top + "px");
      });
    });
  }

  /* ---------- table of contents: active section + collapse on mobile ---------- */
  var toc = document.querySelector("[data-toc]");
  if (toc) {
    if (window.innerWidth <= 1080) toc.removeAttribute("open");
    var links = toc.querySelectorAll("a");
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    if ("IntersectionObserver" in window) {
      var tio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && map[en.target.id]) {
            links.forEach(function (l) { l.classList.remove("is-active"); });
            map[en.target.id].classList.add("is-active");
          }
        });
      }, { rootMargin: "-20% 0px -70% 0px" });
      Object.keys(map).forEach(function (id) { var el = document.getElementById(id); if (el) tio.observe(el); });
    }
    toc.addEventListener("click", function (e) {
      if (e.target.closest("a") && window.innerWidth <= 1080) toc.removeAttribute("open");
    });
  }

  /* ---------- blog filters ---------- */
  var chips = document.querySelectorAll("[data-filter]");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      var f = chip.getAttribute("data-filter");
      chips.forEach(function (c) { c.classList.toggle("is-on", c === chip); });
      document.querySelectorAll("[data-filter-grid] > [data-cat]").forEach(function (card) {
        var show = f === "all" || card.getAttribute("data-cat") === f;
        card.classList.toggle("is-hidden", !show);
        if (show) card.classList.add("is-in");
      });
    });
  });

  /* ---------- form confirmations ---------- */
  if (/[?&]sent=1/.test(location.search)) {
    var ok = document.querySelector("[data-form-ok]");
    if (ok) ok.hidden = false;
    document.querySelectorAll(".nl-form").forEach(function (f) {
      var p = document.createElement("p");
      p.className = "nl-ok";
      p.textContent = "Thanks! You're on the list.";
      if (!ok) f.insertAdjacentElement("afterend", p);
    });
  }

  /* ---------- back to top ---------- */
  var top = document.querySelector("[data-to-top]");
  if (top) top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });
})();
