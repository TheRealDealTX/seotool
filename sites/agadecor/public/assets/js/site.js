/* AGA Décor — interactions. No dependencies. */
(function () {
  "use strict";
  var d = document, root = d.documentElement;
  root.classList.remove("no-js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Header: solid on scroll, mobile nav */
  var header = d.querySelector(".site-header");
  var burger = d.querySelector(".burger");
  function onScrollHeader() { if (header) header.classList.toggle("solid", window.scrollY > 40); }
  onScrollHeader();
  window.addEventListener("scroll", onScrollHeader, { passive: true });
  if (burger) {
    burger.addEventListener("click", function () {
      var open = d.body.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      d.body.style.overflow = open ? "hidden" : "";
    });
    d.querySelectorAll(".menu a").forEach(function (a) {
      a.addEventListener("click", function () { d.body.classList.remove("nav-open"); d.body.style.overflow = ""; burger.setAttribute("aria-expanded", "false"); });
    });
  }

  /* Hero headline: split words for staggered rise */
  d.querySelectorAll("[data-split]").forEach(function (el) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
            var w = d.createElement("span"); w.className = "w";
            var inner = d.createElement("span"); inner.textContent = part;
            inner.style.animationDelay = (0.15 + i++ * 0.08) + "s";
            w.appendChild(inner); frag.appendChild(w);
          });
          node.replaceChild(frag, n);
        } else if (n.nodeType === 1) { walk(n); }
      });
    })(el);
  });

  /* Reveal on scroll */
  var reveals = d.querySelectorAll(".reveal, .reveal-img");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add("in"); }); }

  /* Parallax + progress ring */
  var par = d.querySelectorAll("[data-parallax]");
  var toTop = d.querySelector(".to-top");
  var ring = toTop && toTop.querySelector("circle");
  var ticking = false;
  function frame() {
    ticking = false;
    var vh = window.innerHeight;
    if (!reduce) par.forEach(function (el) {
      var r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var p = (r.top + r.height / 2 - vh / 2) / vh;
      el.style.transform = "translate3d(0," + (p * -parseFloat(el.dataset.parallax || 12)) + "%,0)";
    });
    if (toTop) {
      var max = d.documentElement.scrollHeight - vh;
      var pct = max > 0 ? window.scrollY / max : 0;
      toTop.classList.toggle("show", window.scrollY > vh * 0.8);
      if (ring) ring.style.strokeDashoffset = 150.8 * (1 - pct);
    }
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();
  if (toTop) toTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });

  /* Falling petals canvas */
  var cv = d.getElementById("petals");
  if (cv && !reduce) {
    var ctx = cv.getContext("2d"), petals = [], W, H, dpr = Math.min(window.devicePixelRatio || 1, 2);
    var colors = ["#f1d9d2", "#e6bfb5", "#f7e7df", "#e3c99c", "#fff4ea"];
    function size() { W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    function petal(init) {
      return { x: Math.random() * W, y: init ? Math.random() * H : -20, s: 6 + Math.random() * 10, vy: 0.4 + Math.random() * 0.9,
        vx: -0.3 + Math.random() * 0.6, a: Math.random() * Math.PI * 2, va: -0.02 + Math.random() * 0.04,
        sw: Math.random() * Math.PI * 2, c: colors[(Math.random() * colors.length) | 0], o: 0.45 + Math.random() * 0.45 };
    }
    size(); window.addEventListener("resize", size);
    var count = W < 700 ? 18 : 34;
    for (var k = 0; k < count; k++) petals.push(petal(true));
    var running = true;
    new IntersectionObserver(function (e) { running = e[0].isIntersecting; if (running) requestAnimationFrame(draw); }).observe(cv);
    function draw() {
      if (!running) return;
      ctx.clearRect(0, 0, W, H);
      petals.forEach(function (p, i) {
        p.sw += 0.02; p.x += p.vx + Math.sin(p.sw) * 0.6; p.y += p.vy; p.a += p.va;
        if (p.y > H + 20) petals[i] = petal(false);
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.scale(1, 0.6 + Math.sin(p.sw) * 0.3);
        ctx.globalAlpha = p.o; ctx.fillStyle = p.c;
        ctx.beginPath(); ctx.moveTo(0, -p.s);
        ctx.bezierCurveTo(p.s * 0.9, -p.s * 0.6, p.s * 0.7, p.s * 0.6, 0, p.s);
        ctx.bezierCurveTo(-p.s * 0.7, p.s * 0.6, -p.s * 0.9, -p.s * 0.6, 0, -p.s);
        ctx.fill(); ctx.restore();
      });
      requestAnimationFrame(draw);
    }
    requestAnimationFrame(draw);
  }

  /* Hero glow follows pointer */
  var hero = d.querySelector(".hero"), glow = d.querySelector(".hero-glow");
  if (hero && glow && !reduce) hero.addEventListener("pointermove", function (e) {
    var r = hero.getBoundingClientRect();
    glow.style.left = ((e.clientX - r.left) / r.width * 100) + "%";
    glow.style.top = ((e.clientY - r.top) / r.height * 100) + "%";
  });

  /* Card tilt + shine */
  if (!reduce && window.matchMedia("(hover: hover)").matches) d.querySelectorAll(".card").forEach(function (c) {
    c.addEventListener("pointermove", function (e) {
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      c.style.transform = "perspective(900px) rotateY(" + ((x - 0.5) * 8) + "deg) rotateX(" + ((0.5 - y) * 8) + "deg)";
      c.style.setProperty("--mx", x * 100 + "%"); c.style.setProperty("--my", y * 100 + "%");
    });
    c.addEventListener("pointerleave", function () { c.style.transform = ""; });
  });

  /* Process steps: highlight + swap image */
  var steps = d.querySelectorAll(".step");
  if (steps.length) {
    var imgs = d.querySelectorAll(".process-visual img"), label = d.querySelector(".process-visual .label");
    var bar = d.querySelector(".steps .bar"), wrap = d.querySelector(".steps");
    function setStep(i) {
      steps.forEach(function (s, j) { s.classList.toggle("on", j <= i); });
      imgs.forEach(function (im, j) { im.classList.toggle("on", j === i); });
      if (label) label.textContent = steps[i].dataset.label || "";
    }
    setStep(0);
    window.addEventListener("scroll", function () {
      var mid = window.innerHeight * 0.55, cur = 0;
      steps.forEach(function (s, j) { if (s.getBoundingClientRect().top < mid) cur = j; });
      setStep(cur);
      if (bar && wrap) {
        var r = wrap.getBoundingClientRect();
        bar.style.height = Math.max(0, Math.min(r.height - 16, mid - r.top)) + "px";
      }
    }, { passive: true });
  }

  /* Palette studio */
  var scene = d.querySelector(".scene");
  if (scene) {
    var btns = d.querySelectorAll(".theme-btn"), sw = d.querySelectorAll(".swatch"), note = d.querySelector(".theme-note");
    var lights = scene.querySelector(".lights");
    if (lights) for (var n = 0; n < 26; n++) {
      var dot = d.createElement("i");
      var x = n / 25;
      dot.style.left = (x * 100) + "%";
      dot.style.top = (Math.sin(x * Math.PI * 3) * 18 + 30) + "%";
      dot.style.animationDelay = (Math.random() * 3) + "s";
      lights.appendChild(dot);
    }
    function apply(btn) {
      var p = JSON.parse(btn.dataset.palette);
      ["bg", "drape", "linen", "runner", "flower", "accent", "leaf"].forEach(function (k) { scene.style.setProperty("--c-" + k, p[k]); });
      var names = btn.dataset.names.split("|"), keys = ["flower", "runner", "linen", "accent", "drape"];
      sw.forEach(function (s, i) { s.querySelector("i").style.background = p[keys[i]]; s.querySelector("span").textContent = names[i] || ""; });
      if (note) note.textContent = btn.dataset.note;
      btns.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
    }
    btns.forEach(function (b) { b.addEventListener("click", function () { apply(b); }); });
    if (btns[0]) apply(btns[0]);
  }

  /* Gallery filters + lightbox */
  var tiles = Array.prototype.slice.call(d.querySelectorAll(".tile"));
  d.querySelectorAll(".filters button").forEach(function (b, _, all) {
    b.addEventListener("click", function () {
      var f = b.dataset.filter;
      all.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      tiles.forEach(function (t) { t.classList.toggle("hide", f !== "all" && t.dataset.cat.split(" ").indexOf(f) < 0); });
    });
  });
  var lb = d.querySelector(".lightbox");
  if (lb && tiles.length) {
    var lbImg = lb.querySelector("img"), lbCap = lb.querySelector("p"), idx = 0;
    function visible() { return tiles.filter(function (t) { return !t.classList.contains("hide"); }); }
    function show(t) {
      var im = t.querySelector("img");
      lbImg.src = im.dataset.full || im.src; lbImg.alt = im.alt;
      lbCap.textContent = t.querySelector("figcaption") ? t.querySelector("figcaption").firstChild.textContent : "";
      idx = visible().indexOf(t);
    }
    function open(t) { show(t); lb.classList.add("open"); lb.querySelector(".lb-close").focus(); }
    function close() { lb.classList.remove("open"); }
    function step(dir) { var v = visible(); show(v[(idx + dir + v.length) % v.length]); }
    tiles.forEach(function (t) {
      t.tabIndex = 0;
      t.addEventListener("click", function () { open(t); });
      t.addEventListener("keydown", function (e) { if (e.key === "Enter") open(t); });
    });
    lb.querySelector(".lb-close").addEventListener("click", close);
    lb.querySelector(".lb-prev").addEventListener("click", function () { step(-1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { step(1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    d.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close(); if (e.key === "ArrowRight") step(1); if (e.key === "ArrowLeft") step(-1);
    });
  }

  /* Rental category nav highlight */
  var catLinks = d.querySelectorAll(".cat-nav a");
  if (catLinks.length && "IntersectionObserver" in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        catLinks.forEach(function (a) { a.classList.toggle("on", a.getAttribute("href") === "#" + e.target.id); });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    d.querySelectorAll(".cat[id]").forEach(function (s) { cio.observe(s); });
  }

  /* Inquiry form: status from redirect, prefill from ?service= */
  var form = d.querySelector("form.form");
  if (form) {
    var q = new URLSearchParams(location.search);
    var ok = d.querySelector(".notice"), bad = d.querySelector(".notice.err");
    if (q.get("sent") === "1" && ok) ok.classList.add("show");
    if (q.get("sent") === "0" && bad) bad.classList.add("show");
    var svc = q.get("service");
    if (svc) form.querySelectorAll('input[name="services[]"]').forEach(function (c) { if (c.value === svc) c.checked = true; });
    var ts = form.querySelector('input[name="ts"]'); if (ts) ts.value = Date.now();
  }

  /* Year */
  d.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
