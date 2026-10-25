/* Hate to Love the Split — interactions */
(function () {
  "use strict";
  var doc = document.documentElement, body = document.body;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");
  var scrim = document.querySelector("[data-nav-scrim]");
  var mq = window.matchMedia("(max-width: 960px)");

  function setNav(open) {
    body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (open) {
      scrim.hidden = false;
      var first = nav.querySelector("a");
      if (first) setTimeout(function () { first.focus(); }, 60);
    } else {
      setTimeout(function () { if (!body.classList.contains("nav-open")) scrim.hidden = true; }, 300);
    }
  }
  if (toggle && nav && scrim) {
    toggle.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
    scrim.addEventListener("click", function () { setNav(false); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
    document.addEventListener("keydown", function (e) {
      if (!body.classList.contains("nav-open")) return;
      if (e.key === "Escape") { setNav(false); toggle.focus(); }
      if (e.key === "Tab") { // keep focus inside the open drawer
        var items = [toggle].concat(Array.prototype.slice.call(nav.querySelectorAll("a")));
        var i = items.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
        else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
      }
    });
    var onMq = function () { if (!mq.matches) setNav(false); };
    if (mq.addEventListener) mq.addEventListener("change", onMq); else mq.addListener(onMq);
  }

  /* ---------- header + progress + parallax ---------- */
  var header = document.querySelector("[data-header]");
  var bar = document.querySelector(".progress span");
  var isPost = body.classList.contains("is-post");
  var parallax = document.querySelector("[data-parallax]") || document.querySelector(".post-hero-bg");
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 40);
    if (bar && isPost) {
      var h = doc.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + "%";
    }
    if (parallax && !reduce && y < window.innerHeight * 1.2) {
      parallax.style.transform = "translate3d(0," + (y * 0.25).toFixed(1) + "px,0)";
    }
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { window.requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- reveal on scroll + counters ---------- */
  function countUp(el) {
    var end = parseInt(el.getAttribute("data-count"), 10), suffix = el.getAttribute("data-suffix") || "";
    if (reduce || !end) return;
    var start = null, dur = 1400;
    function step(t) {
      if (!start) start = t;
      var p = Math.min(1, (t - start) / dur), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * eased) + (p === 1 ? suffix : "");
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  // Reveal anything whose top has passed 92% of the viewport. A position check
  // (rather than IntersectionObserver) also catches elements skipped over by
  // anchor jumps or fast scrolling.
  var pending = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  function revealCheck() {
    var limit = window.innerHeight * 0.92;
    pending = pending.filter(function (el) {
      if (el.getBoundingClientRect().top > limit) return true;
      el.classList.add("in");
      el.querySelectorAll("[data-count]").forEach(countUp);
      return false;
    });
  }
  var rTick = false;
  var onReveal = function () { if (!rTick && pending.length) { rTick = true; requestAnimationFrame(function () { rTick = false; revealCheck(); }); } };
  window.addEventListener("scroll", onReveal, { passive: true });
  window.addEventListener("resize", onReveal);
  window.addEventListener("load", revealCheck);
  revealCheck();

  /* ---------- before / after slider ---------- */
  document.querySelectorAll("[data-ba]").forEach(function (ba) {
    var range = ba.querySelector(".ba-range");
    var set = function (v) { ba.style.setProperty("--pos", v + "%"); };
    range.addEventListener("input", function () { set(range.value); });
    // gentle intro sweep so people notice it is interactive
    if (!reduce && "IntersectionObserver" in window) {
      var played = false;
      new IntersectionObserver(function (en, obs) {
        if (!en[0].isIntersecting || played) return;
        played = true; obs.disconnect();
        var t0 = null;
        (function anim(t) {
          if (!t0) t0 = t;
          var p = (t - t0) / 1800;
          if (p >= 1) { set(50); range.value = 50; return; }
          var v = 50 + Math.sin(p * Math.PI * 2) * 30;
          set(v.toFixed(1)); range.value = v;
          requestAnimationFrame(anim);
        })(performance.now());
      }, { threshold: 0.5 }).observe(ba);
    }
  });

  /* ---------- card tilt (mouse only) ---------- */
  if (!reduce && window.matchMedia("(hover: hover) and (pointer: fine)").matches) {
    document.querySelectorAll("[data-tilt]").forEach(function (el) {
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(900px) rotateX(" + (-y * 5).toFixed(2) + "deg) rotateY(" + (x * 6).toFixed(2) + "deg) translateY(-4px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = ""; });
    });
  }

  /* ---------- contact form status ---------- */
  var note = document.querySelector("[data-form-note]");
  if (note) {
    var q = window.location.search;
    if (/sent=1/.test(q)) note.textContent = "Thanks! Your message is on its way. We'll reply soon.";
    else if (/error=1/.test(q)) note.innerHTML = 'Hmm, that didn\'t send. Please email us directly at <a href="mailto:info@hatetolovethesplit.com">info@hatetolovethesplit.com</a>.';
  }
})();
