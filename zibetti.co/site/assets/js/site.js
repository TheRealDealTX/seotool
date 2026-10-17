/* zibetti.co — shared interactions */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- header: solid on scroll, hide on scroll down ---------- */
  var header = document.querySelector(".site-header");
  var onHero = header && header.classList.contains("on-hero");
  var lastY = window.scrollY;
  var toTop = document.querySelector(".to-top");
  function onScroll() {
    var y = window.scrollY;
    if (header && !document.body.classList.contains("nav-open")) {
      header.classList.toggle("scrolled", y > 40);
      if (onHero) header.classList.toggle("on-hero", y <= 40);
      // Auto-hide on scroll only on desktop; on phones the menu button stays in reach.
      if (window.innerWidth > 1020) {
        if (y > 400 && y > lastY + 4) header.classList.add("hidden");
        else if (y < lastY - 4) header.classList.remove("hidden");
      } else {
        header.classList.remove("hidden");
      }
    }
    if (toTop) toTop.classList.toggle("show", y > 900);
    lastY = y;
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- mobile nav ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");
  function setNav(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    nav.classList.toggle("open", open);
    document.body.classList.toggle("nav-open", open);
    if (open) {
      header.classList.remove("hidden");
      var first = nav.querySelector("a");
      if (first) setTimeout(function () { first.focus({ preventScroll: true }); }, 350);
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setNav(toggle.getAttribute("aria-expanded") !== "true"); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { setNav(false); toggle.focus(); }
      if (e.key === "Tab" && nav.classList.contains("open")) {
        var items = [toggle].concat(Array.prototype.slice.call(nav.querySelectorAll("a")));
        var i = items.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); items[items.length - 1].focus(); }
        else if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); items[0].focus(); }
      }
    });
    window.addEventListener("resize", function () { if (window.innerWidth > 1020 && nav.classList.contains("open")) setNav(false); });
  }

  /* ---------- reveal on scroll ---------- */
  var revealEls = document.querySelectorAll(".reveal, .reveal-img, .step");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- parallax ---------- */
  var plx = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  if (plx.length && !reduce) {
    var ticking = false;
    var update = function () {
      var vh = window.innerHeight;
      plx.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var speed = parseFloat(el.getAttribute("data-parallax")) || 0.2;
        var off = (r.top + r.height / 2 - vh / 2) * -speed;
        el.style.transform = "translate3d(0," + off.toFixed(1) + "px,0)";
      });
      ticking = false;
    };
    window.addEventListener("scroll", function () { if (!ticking) { requestAnimationFrame(update); ticking = true; } }, { passive: true });
    update();
  }

  /* ---------- hero slideshow ---------- */
  var slides = document.querySelectorAll(".hero-slides figure");
  var dots = document.querySelectorAll(".slide-dots button");
  if (slides.length > 1) {
    var cur = 0, timer;
    var show = function (n) {
      slides[cur].classList.remove("active");
      if (dots[cur]) dots[cur].classList.remove("active");
      cur = (n + slides.length) % slides.length;
      slides[cur].classList.add("active");
      if (dots[cur]) { dots[cur].classList.remove("active"); void dots[cur].offsetWidth; dots[cur].classList.add("active"); }
    };
    var play = function () { clearInterval(timer); if (!reduce) timer = setInterval(function () { show(cur + 1); }, 6000); };
    dots.forEach(function (d, i) { d.addEventListener("click", function () { show(i); play(); }); });
    play();
  }

  /* ---------- drag-to-scroll film strip ---------- */
  document.querySelectorAll(".strip").forEach(function (strip) {
    var down = false, startX = 0, startL = 0, moved = false;
    strip.addEventListener("pointerdown", function (e) {
      if (e.pointerType !== "mouse") return;
      down = true; moved = false; startX = e.clientX; startL = strip.scrollLeft;
      strip.classList.add("dragging");
    });
    window.addEventListener("pointermove", function (e) {
      if (!down) return;
      var dx = e.clientX - startX;
      if (Math.abs(dx) > 3) moved = true;
      strip.scrollLeft = startL - dx;
    });
    window.addEventListener("pointerup", function () { if (down) { down = false; strip.classList.remove("dragging"); } });
    strip.addEventListener("click", function (e) { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
  });

  /* ---------- counters ---------- */
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseFloat(el.getAttribute("data-count")), suffix = el.getAttribute("data-suffix") || "";
        cio.unobserve(el);
        if (reduce) { el.textContent = end + suffix; return; }
        var t0 = null;
        var step = function (t) {
          if (!t0) t0 = t;
          var p = Math.min((t - t0) / 1800, 1), eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(end * eased) + suffix;
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- portfolio filter + lightbox ---------- */
  var filterBtns = document.querySelectorAll(".filters button");
  var figs = Array.prototype.slice.call(document.querySelectorAll(".masonry figure"));
  filterBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.getAttribute("data-filter");
      filterBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      figs.forEach(function (fig) {
        var show = f === "all" || (fig.getAttribute("data-cat") || "").indexOf(f) > -1;
        fig.classList.toggle("hide", !show);
      });
    });
  });
  var lb = document.querySelector(".lightbox");
  if (lb && figs.length) {
    var lbImg = lb.querySelector("img"), lbCap = lb.querySelector("p"), idx = 0, opener = null;
    var visible = function () { return figs.filter(function (f) { return !f.classList.contains("hide"); }); };
    var open = function (fig) {
      var v = visible(); idx = v.indexOf(fig);
      var img = fig.querySelector("img");
      lbImg.src = img.getAttribute("data-full") || img.src; lbImg.alt = img.alt;
      lbCap.textContent = fig.querySelector("figcaption") ? fig.querySelector("figcaption").textContent : "";
      lb.classList.add("open"); document.body.classList.add("nav-open");
      lb.querySelector(".lb-close").focus();
    };
    var close = function () { lb.classList.remove("open"); document.body.classList.remove("nav-open"); if (opener) opener.focus(); };
    var go = function (d) { var v = visible(); open(v[(idx + d + v.length) % v.length]); };
    figs.forEach(function (fig) {
      fig.setAttribute("tabindex", "0");
      fig.setAttribute("role", "button");
      fig.addEventListener("click", function () { opener = fig; open(fig); });
      fig.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); opener = fig; open(fig); } });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { go(-1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { go(1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") go(-1);
      if (e.key === "ArrowRight") go(1);
    });
  }

  /* ---------- article: reading progress + toc highlight ---------- */
  var bar = document.querySelector(".progress");
  var article = document.querySelector(".prose[data-article]");
  if (bar && article) {
    var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc-box a[href^='#']"));
    var heads = tocLinks.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var prog = function () {
      var r = article.getBoundingClientRect();
      var p = Math.min(Math.max(-r.top / (r.height - window.innerHeight * 0.6), 0), 1);
      bar.style.transform = "scaleX(" + p.toFixed(3) + ")";
      var active = -1;
      heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top < 140) active = i; });
      tocLinks.forEach(function (a, i) { a.classList.toggle("active", i === active); });
    };
    window.addEventListener("scroll", prog, { passive: true });
    prog();
  }

  /* ---------- contact form status from query string ---------- */
  var status = document.querySelector("[data-form-status]");
  if (status) {
    var q = new URLSearchParams(location.search);
    if (q.get("sent") === "1") { status.hidden = false; status.textContent = "Thank you! Your note is on its way. We reply to every inquiry within two business days."; }
    else if (q.get("sent") === "0") { status.hidden = false; status.className = "notice err"; status.textContent = "Something went wrong sending your message. Please email info@zibetti.co directly."; }
  }

  var yr = document.querySelectorAll("[data-year]");
  yr.forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
