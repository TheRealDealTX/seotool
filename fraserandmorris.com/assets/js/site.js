/* fraserandmorris.com - nav, scroll effects, petals, seasons, form status */
(function () {
  "use strict";
  var doc = document, body = doc.body;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var header = doc.querySelector(".site-header");
  var toggle = doc.querySelector(".nav-toggle");
  var nav = doc.getElementById("site-nav");
  var mobile = window.matchMedia("(max-width: 960px)");

  /* ---------- Mobile navigation ---------- */
  function setNav(open) {
    body.classList.toggle("nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    if (!open) {
      doc.querySelectorAll(".has-sub.open").forEach(function (li) {
        li.classList.remove("open");
        li.querySelector("button").setAttribute("aria-expanded", "false");
      });
    }
  }
  if (toggle && nav) {
    toggle.addEventListener("click", function () { setNav(!body.classList.contains("nav-open")); });
    nav.addEventListener("click", function (e) {
      var a = e.target.closest("a");
      if (a && body.classList.contains("nav-open")) setNav(false);
    });
    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && body.classList.contains("nav-open")) { setNav(false); toggle.focus(); }
    });
    var onChange = function (e) { if (!e.matches) setNav(false); };
    if (mobile.addEventListener) mobile.addEventListener("change", onChange); else mobile.addListener(onChange);
  }
  doc.querySelectorAll(".has-sub > button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.parentElement, open = !li.classList.contains("open");
      li.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });
  doc.addEventListener("click", function (e) {
    if (mobile.matches) return;
    doc.querySelectorAll(".has-sub.open").forEach(function (li) {
      if (!li.contains(e.target)) { li.classList.remove("open"); li.querySelector("button").setAttribute("aria-expanded", "false"); }
    });
  });

  /* ---------- Header state, parallax, back-to-top ---------- */
  var toTop = doc.querySelector(".to-top");
  var ring = toTop && toTop.querySelector(".ring circle");
  var parallax = reduce ? [] : Array.prototype.slice.call(doc.querySelectorAll("[data-parallax]"));
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("is-solid", y > 40);
    if (toTop) {
      var max = doc.documentElement.scrollHeight - window.innerHeight;
      toTop.classList.toggle("show", y > 600);
      if (ring && max > 0) ring.style.setProperty("--off", String(151 - 151 * Math.min(1, y / max)));
    }
    var vh = window.innerHeight;
    parallax.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var speed = parseFloat(el.getAttribute("data-parallax")) || 0.2;
      var offset = (r.top + r.height / 2 - vh / 2) * -speed;
      el.style.transform = "translate3d(0," + offset.toFixed(1) + "px,0)";
    });
    ticking = false;
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* ---------- Reveal on scroll ---------- */
  var revealEls = doc.querySelectorAll(".reveal, .reveal-img, .process");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---------- Service card spotlight ---------- */
  doc.querySelectorAll(".service").forEach(function (card) {
    card.addEventListener("pointermove", function (e) {
      var r = card.getBoundingClientRect();
      card.style.setProperty("--mx", (e.clientX - r.left) + "px");
      card.style.setProperty("--my", (e.clientY - r.top) + "px");
    });
  });

  /* ---------- Seasons tabs ---------- */
  doc.querySelectorAll("[data-tabs]").forEach(function (root) {
    var tabs = root.querySelectorAll(".tab");
    var panels = root.querySelectorAll(".panel");
    var imgs = root.querySelectorAll(".season-media img");
    function select(i, focus) {
      tabs.forEach(function (t, j) {
        t.setAttribute("aria-selected", i === j ? "true" : "false");
        t.tabIndex = i === j ? 0 : -1;
        panels[j].hidden = i !== j;
        if (imgs[j]) imgs[j].classList.toggle("on", i === j);
      });
      if (focus) tabs[i].focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(i); });
      t.addEventListener("keydown", function (e) {
        if (e.key === "ArrowRight") select((i + 1) % tabs.length, true);
        if (e.key === "ArrowLeft") select((i - 1 + tabs.length) % tabs.length, true);
      });
    });
  });

  /* ---------- Falling petals in hero ---------- */
  var canvas = doc.querySelector(".hero canvas");
  if (canvas && !reduce && canvas.getContext) {
    var ctx = canvas.getContext("2d"), petals = [], W = 0, H = 0, dpr = Math.min(window.devicePixelRatio || 1, 2), running = true;
    var colors = ["rgba(240,199,166,.85)", "rgba(255,255,255,.75)", "rgba(169,183,155,.8)", "rgba(224,150,120,.75)"];
    function size() {
      W = canvas.offsetWidth; H = canvas.offsetHeight;
      canvas.width = W * dpr; canvas.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function petal(init) {
      return {
        x: Math.random() * W, y: init ? Math.random() * H : -20, r: 4 + Math.random() * 6,
        vy: .35 + Math.random() * .7, vx: -.2 + Math.random() * .6, a: Math.random() * Math.PI * 2,
        va: (Math.random() - .5) * .03, sway: Math.random() * 2, c: colors[(Math.random() * colors.length) | 0]
      };
    }
    size();
    var count = W < 640 ? 14 : 28;
    for (var i = 0; i < count; i++) petals.push(petal(true));
    window.addEventListener("resize", size);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { running = en[0].isIntersecting; if (running) requestAnimationFrame(draw); }).observe(canvas);
    }
    var t = 0;
    function draw() {
      if (!running) return;
      t += .01;
      ctx.clearRect(0, 0, W, H);
      petals.forEach(function (p, k) {
        p.y += p.vy; p.x += p.vx + Math.sin(t * 2 + p.sway) * .35; p.a += p.va;
        if (p.y > H + 20 || p.x > W + 20 || p.x < -20) petals[k] = petal(false);
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.scale(1, .55 + Math.abs(Math.sin(t + p.sway)) * .45);
        ctx.fillStyle = p.c; ctx.beginPath();
        ctx.moveTo(0, -p.r); ctx.quadraticCurveTo(p.r, 0, 0, p.r); ctx.quadraticCurveTo(-p.r, 0, 0, -p.r); ctx.fill();
        ctx.restore();
      });
      requestAnimationFrame(draw);
    }
    requestAnimationFrame(draw);
  }

  /* ---------- Contact form status ---------- */
  var status = doc.querySelector(".form-status");
  if (status) {
    var q = window.location.search;
    if (/[?&]sent=1/.test(q)) { status.className = "form-status ok"; status.textContent = "Thank you - your message is on its way. We will be in touch shortly."; }
    else if (/[?&]error=1/.test(q)) { status.className = "form-status err"; status.textContent = "Sorry, something went wrong. Please check the form and try again, or email us directly."; }
  }

  var year = doc.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
