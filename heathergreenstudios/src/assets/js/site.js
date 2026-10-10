/* heathergreenstudios.com — interactions and visual effects (no dependencies) */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* header + progress */
  var header = $(".site-header"), bar = $(".progress");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("scrolled", y > 10);
    if (bar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = "scaleX(" + (h > 0 ? y / h : 0) + ")";
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* mobile menu */
  var toggle = $(".menu-toggle"), menu = $(".menu");
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      var open = menu.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* split headline words */
  $$(".split").forEach(function (el) {
    var html = el.innerHTML.split(/(<[^>]+>|\s+)/).map(function (part) {
      if (!part || /^\s+$/.test(part)) return part;
      if (part.charAt(0) === "<") return part;
      return '<span class="w"><span>' + part + "</span></span>";
    }).join("");
    el.innerHTML = html;
    $$(".w>span", el).forEach(function (s, i) { s.style.transitionDelay = (i * 0.06) + "s"; });
  });

  /* reveal on scroll */
  var targets = $$(".reveal, .split");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add("in"); });
  }

  /* count-up stats */
  $$("[data-count]").forEach(function (el) {
    var end = parseFloat(el.getAttribute("data-count")), done = false;
    function run() {
      if (done) return; done = true;
      if (reduce) { el.textContent = end; return; }
      var t0 = performance.now();
      (function step(t) {
        var p = Math.min(1, (t - t0) / 1600), e = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(end * e);
        if (p < 1) requestAnimationFrame(step);
      })(t0);
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en, o) { if (en[0].isIntersecting) { run(); o.disconnect(); } }).observe(el);
    } else run();
  });

  /* tilt on print plates */
  if (!reduce && window.matchMedia("(hover:hover)").matches) {
    $$(".plate").forEach(function (p) {
      p.addEventListener("mousemove", function (e) {
        var r = p.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        p.style.transform = "perspective(900px) rotateY(" + (x * 10) + "deg) rotateX(" + (-y * 10) + "deg)";
      });
      p.addEventListener("mouseleave", function () { p.style.transform = ""; });
    });

    /* ink cursor */
    var dot = document.createElement("div");
    dot.className = "ink-cursor";
    document.body.appendChild(dot);
    var mx = 0, my = 0, cx = 0, cy = 0;
    window.addEventListener("mousemove", function (e) { mx = e.clientX; my = e.clientY; dot.style.opacity = 1; });
    (function loop() {
      cx += (mx - cx) * 0.18; cy += (my - cy) * 0.18;
      dot.style.left = cx + "px"; dot.style.top = cy + "px";
      requestAnimationFrame(loop);
    })();
    $$("a, button, .plate").forEach(function (a) {
      a.addEventListener("mouseenter", function () { dot.classList.add("big"); });
      a.addEventListener("mouseleave", function () { dot.classList.remove("big"); });
    });
  }

  /* hero canvas: drifting ink blooms that react to the pointer */
  var canvas = $("#ink");
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext("2d"), W, H, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var colors = ["184,96,44", "31,138,131", "217,138,78", "70,184,172", "230,201,154"];
    var blobs = [], pointer = { x: -999, y: -999 };
    function size() {
      W = canvas.offsetWidth; H = canvas.offsetHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function seed() {
      blobs = [];
      var n = W < 700 ? 7 : 12;
      for (var i = 0; i < n; i++) {
        blobs.push({
          x: Math.random() * W, y: Math.random() * H,
          r: 90 + Math.random() * (W < 700 ? 120 : 220),
          vx: (Math.random() - 0.5) * 0.35, vy: (Math.random() - 0.5) * 0.35,
          c: colors[i % colors.length], a: 0.16 + Math.random() * 0.16,
          ph: Math.random() * Math.PI * 2
        });
      }
    }
    function draw(t) {
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = "multiply";
      blobs.forEach(function (b) {
        var dx = b.x - pointer.x, dy = b.y - pointer.y, d = Math.sqrt(dx * dx + dy * dy);
        if (d < 260 && d > 0) { b.vx += dx / d * 0.05; b.vy += dy / d * 0.05; }
        b.vx *= 0.985; b.vy *= 0.985;
        b.vx += (Math.random() - 0.5) * 0.02; b.vy += (Math.random() - 0.5) * 0.02;
        b.x += b.vx; b.y += b.vy;
        if (b.x < -b.r) b.x = W + b.r; if (b.x > W + b.r) b.x = -b.r;
        if (b.y < -b.r) b.y = H + b.r; if (b.y > H + b.r) b.y = -b.r;
        var r = b.r * (1 + Math.sin(t / 2400 + b.ph) * 0.08);
        var g = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, r);
        g.addColorStop(0, "rgba(" + b.c + "," + b.a + ")");
        g.addColorStop(0.6, "rgba(" + b.c + "," + (b.a * 0.45) + ")");
        g.addColorStop(1, "rgba(" + b.c + ",0)");
        ctx.fillStyle = g;
        ctx.beginPath(); ctx.arc(b.x, b.y, r, 0, Math.PI * 2); ctx.fill();
      });
      ctx.globalCompositeOperation = "source-over";
      if (!reduce) requestAnimationFrame(draw);
    }
    size(); seed(); requestAnimationFrame(draw);
    window.addEventListener("resize", function () { size(); seed(); });
    canvas.parentNode.addEventListener("mousemove", function (e) {
      var r = canvas.getBoundingClientRect(); pointer.x = e.clientX - r.left; pointer.y = e.clientY - r.top;
    });
    canvas.parentNode.addEventListener("mouseleave", function () { pointer.x = pointer.y = -999; });
  }

  /* journal filters */
  var filterBtns = $$(".filters button");
  filterBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.getAttribute("data-filter");
      filterBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      $$(".posts .post-card").forEach(function (c) {
        c.hidden = !(f === "all" || (c.getAttribute("data-cat") || "") === f);
      });
    });
  });

  /* table-of-contents highlighting */
  var tocLinks = $$(".toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var tio = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (e.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          var a = map[e.target.id]; if (a) a.classList.add("active");
        }
      });
    }, { rootMargin: "0px 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* art-hanging calculator */
  var hang = $("#hang-tool");
  if (hang) {
    var hEye = $("#h-eye", hang), hArt = $("#h-art", hang), hWire = $("#h-wire", hang);
    var oEye = $("#o-eye", hang), oArt = $("#o-art", hang), oWire = $("#o-wire", hang);
    var res = $("#h-result", hang), frame = $(".frame", hang), eye = $(".eye", hang);
    function calc() {
      var e = +hEye.value, a = +hArt.value, w = +hWire.value;
      oEye.textContent = e + '"'; oArt.textContent = a + '"'; oWire.textContent = w + '"';
      var nail = e + a / 2 - w;
      res.innerHTML = 'Put the nail <b>' + nail.toFixed(1) + '"</b> above the floor.<br><small>Center at ' + e + '", top edge at ' + (e + a / 2).toFixed(1) + '".</small>';
      var scale = 220 / 110; // wall preview shows 110" of height
      frame.style.height = (a * scale) + "px";
      frame.style.width = (a * scale * 0.8) + "px";
      frame.style.bottom = ((e - a / 2) * scale) + "px";
      eye.style.bottom = (e * scale) + "px";
    }
    [hEye, hArt, hWire].forEach(function (i) { i.addEventListener("input", calc); });
    calc();
  }

  /* contact form status from query string */
  var note = $("#form-note");
  if (note) {
    var q = location.search;
    if (/sent=1/.test(q)) { note.className = "notice ok"; note.textContent = "Thank you — your message is on its way. We reply within a few days."; note.hidden = false; }
    else if (/sent=0/.test(q)) { note.className = "notice err"; note.textContent = "Something went wrong. Please email info@heathergreenstudios.com directly."; note.hidden = false; }
  }

  /* year */
  $$("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });
})();
