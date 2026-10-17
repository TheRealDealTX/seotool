/* Live-Style: header, mobile nav, scroll effects, contact form. */
(function () {
  "use strict";
  var doc = document.documentElement;
  var body = document.body;
  var header = document.querySelector("[data-header]");
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.getElementById("main-nav");
  var bar = document.querySelector(".progress span");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var hasHero = !!document.querySelector(".hero, .post-hero, .list-hero");
  if (!hasHero) body.classList.add("solid-header");

  /* ---- mobile nav ---- */
  function setNav(open) {
    nav.classList.toggle("open", open);
    body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (open) {
      var first = nav.querySelector("a");
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 350);
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setNav(!nav.classList.contains("open")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { setNav(false); toggle.focus(); }
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 1060 && nav.classList.contains("open")) setNav(false);
    });
  }

  /* ---- header state, progress bar, parallax ---- */
  var lastY = window.scrollY;
  var parallax = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  var ticking = false;
  function onScroll() {
    var y = window.scrollY;
    if (header && !body.classList.contains("nav-open")) {
      header.classList.toggle("scrolled", y > 40);
      header.classList.toggle("hidden", y > 400 && y > lastY + 4);
      if (y < lastY - 4) header.classList.remove("hidden");
    }
    lastY = y;
    if (bar) {
      var max = doc.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, y / max) : 0) + ")";
    }
    for (var i = 0; i < parallax.length; i++) {
      if (y < window.innerHeight * 1.2) parallax[i].style.transform = "translate3d(0," + (y * 0.25) + "px,0)";
    }
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---- reveal on scroll ---- */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- magnetic buttons + tilt (pointer devices only) ---- */
  if (!reduce && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll(".magnetic").forEach(function (el) {
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var x = e.clientX - r.left - r.width / 2, y = e.clientY - r.top - r.height / 2;
        el.style.transform = "translate(" + x * 0.18 + "px," + y * 0.3 + "px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = ""; });
    });
    document.querySelectorAll(".tilt").forEach(function (el) {
      var img = el.querySelector("img");
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        img.style.transform = "scale(1.08) translate(" + (-x * 14) + "px," + (-y * 14) + "px)";
      });
      el.addEventListener("mouseleave", function () { img.style.transform = ""; });
    });
  }

  /* ---- copy link ---- */
  var copy = document.querySelector("[data-copy]");
  if (copy) copy.addEventListener("click", function () {
    var done = function () { copy.textContent = "Link copied"; setTimeout(function () { copy.textContent = "Copy link"; }, 2000); };
    if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, done); else done();
  });

  /* ---- contact form ---- */
  var form = document.querySelector("[data-contact]");
  if (form) {
    var status = form.querySelector(".form-status");
    var q = location.search;
    if (q.indexOf("sent=1") > -1) status.textContent = "Thanks, your message has been sent.";
    if (q.indexOf("error=1") > -1) status.textContent = "Sorry, something went wrong. Please email info@live-style.co.uk.";
    if (window.fetch && window.FormData) form.addEventListener("submit", function (e) {
      e.preventDefault();
      var btn = form.querySelector("button");
      btn.disabled = true; status.textContent = "Sending…";
      fetch(form.action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (r) { return r.json(); })
        .then(function (d) { status.textContent = d.message; if (d.ok) form.reset(); })
        .catch(function () { status.textContent = "Sorry, something went wrong. Please email info@live-style.co.uk."; })
        .then(function () { btn.disabled = false; });
    });
  }
})();
