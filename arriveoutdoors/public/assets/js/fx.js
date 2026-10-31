/* Arrive Outdoors — visual effects: starfield, shooting stars, fireflies, campfire embers,
   weather particles, parallax, scroll reveals, counters. Honors prefers-reduced-motion. */
(function () {
  "use strict";
  var AO = (window.AO = window.AO || {});
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fx = (AO.fx = {});
  var rand = function (a, b) { return a + Math.random() * (b - a); };

  // ---------------------------------------------------------------- particle engine
  function Scene(canvas, modes, opts) {
    this.c = canvas; this.x = canvas.getContext("2d"); this.modes = modes; this.o = opts || {};
    this.p = []; this.t = 0; this.running = false; this.shoot = null; this.nextShoot = rand(2, 5);
    var self = this;
    this.resize = function () {
      var r = canvas.getBoundingClientRect(), d = Math.min(window.devicePixelRatio || 1, 2);
      self.w = r.width; self.h = r.height; canvas.width = r.width * d; canvas.height = r.height * d;
      self.x.setTransform(d, 0, 0, d, 0, 0); self.seed();
    };
    this.resize();
    window.addEventListener("resize", this.resize);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { es.forEach(function (e) { e.isIntersecting ? self.start() : self.stop(); }); }).observe(canvas);
    } else this.start();
  }
  Scene.prototype.has = function (m) { return this.modes.indexOf(m) >= 0; };
  Scene.prototype.seed = function () {
    var w = this.w, h = this.h, p = (this.p = []), area = w * h;
    if (this.has("stars")) {
      var n = Math.min(420, Math.round(area / 2600)), top = this.o.starTop || 0.7;
      for (var i = 0; i < n; i++) p.push({ k: "s", x: rand(0, w), y: Math.pow(Math.random(), 1.6) * h * top, r: Math.random() < 0.08 ? rand(1.1, 1.8) : rand(0.3, 1), a: rand(0.3, 1), tw: rand(0.5, 2.2), ph: rand(0, 6.28) });
    }
    if (this.has("fireflies")) {
      var f = Math.max(8, Math.min(34, Math.round(w / 45)));
      for (var j = 0; j < f; j++) p.push({ k: "f", x: rand(0, w), y: rand(h * 0.55, h * 0.95), vx: rand(-0.25, 0.25), vy: rand(-0.15, 0.15), ph: rand(0, 6.28), sp: rand(0.6, 1.6), r: rand(1.2, 2.4) });
    }
    if (this.has("embers")) { for (var k = 0; k < 70; k++) p.push(this.ember(true)); }
    if (this.has("rain")) { for (var m = 0; m < Math.round(area / 3500); m++) p.push({ k: "r", x: rand(0, w), y: rand(0, h), l: rand(8, 18), v: rand(6, 11) }); }
    if (this.has("snow")) { for (var q = 0; q < Math.round(area / 5000); q++) p.push({ k: "n", x: rand(0, w), y: rand(0, h), r: rand(0.8, 2.6), v: rand(0.3, 1.1), ph: rand(0, 6.28) }); }
  };
  Scene.prototype.ember = function (init) {
    var w = this.w, h = this.h, cx = this.o.emberX != null ? this.o.emberX * w : w / 2, spread = this.o.emberSpread || w * 0.35;
    return { k: "e", x: cx + rand(-spread, spread), y: init ? rand(h * 0.3, h) : h + rand(0, 40), vx: rand(-0.3, 0.3), vy: rand(-1.6, -0.5), life: init ? rand(0, 1) : 0, max: rand(0.8, 1), r: rand(0.8, 2.4), ph: rand(0, 6.28) };
  };
  Scene.prototype.start = function () { if (this.running || reduce) return; this.running = true; this.last = performance.now(); var s = this; requestAnimationFrame(function f(now) { if (!s.running) return; s.frame(now); requestAnimationFrame(f); }); };
  Scene.prototype.stop = function () { this.running = false; };
  Scene.prototype.frame = function (now) {
    var dt = Math.min(0.05, (now - this.last) / 1000); this.last = now; this.t += dt;
    var g = this.x, w = this.w, h = this.h, t = this.t;
    g.clearRect(0, 0, w, h);
    for (var i = 0; i < this.p.length; i++) {
      var p = this.p[i];
      if (p.k === "s") {
        var a = p.a * (0.55 + 0.45 * Math.sin(t * p.tw + p.ph));
        g.fillStyle = "rgba(255,255,255," + a.toFixed(3) + ")";
        g.beginPath(); g.arc(p.x, p.y, p.r, 0, 6.283); g.fill();
        if (p.r > 1.2) { g.fillStyle = "rgba(200,220,255," + (a * 0.18).toFixed(3) + ")"; g.beginPath(); g.arc(p.x, p.y, p.r * 3.5, 0, 6.283); g.fill(); }
      } else if (p.k === "f") {
        p.ph += dt * p.sp; p.x += p.vx + Math.sin(p.ph * 0.7) * 0.3; p.y += p.vy + Math.cos(p.ph * 0.5) * 0.2;
        if (p.x < -10) p.x = w + 10; if (p.x > w + 10) p.x = -10; if (p.y < h * 0.45) p.vy = Math.abs(p.vy); if (p.y > h) p.vy = -Math.abs(p.vy);
        var glow = Math.max(0, Math.sin(p.ph * 1.7)); if (glow < 0.05) continue;
        var gr = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 7);
        gr.addColorStop(0, "rgba(232,255,140," + (0.9 * glow).toFixed(3) + ")"); gr.addColorStop(0.25, "rgba(200,255,90," + (0.35 * glow).toFixed(3) + ")"); gr.addColorStop(1, "rgba(180,255,80,0)");
        g.fillStyle = gr; g.beginPath(); g.arc(p.x, p.y, p.r * 7, 0, 6.283); g.fill();
      } else if (p.k === "e") {
        p.life += dt * 0.35; p.ph += dt * 3; p.x += p.vx + Math.sin(p.ph) * 0.35; p.y += p.vy;
        if (p.life > p.max || p.y < -20) { this.p[i] = this.ember(false); continue; }
        var al = Math.sin(Math.PI * p.life / p.max) * (0.6 + 0.4 * Math.sin(p.ph * 2.3));
        var eg = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r * 4);
        eg.addColorStop(0, "rgba(255,220,140," + al.toFixed(3) + ")"); eg.addColorStop(0.35, "rgba(255,120,40," + (al * 0.6).toFixed(3) + ")"); eg.addColorStop(1, "rgba(255,80,20,0)");
        g.fillStyle = eg; g.beginPath(); g.arc(p.x, p.y, p.r * 4, 0, 6.283); g.fill();
      } else if (p.k === "r") {
        p.y += p.v * 60 * dt; p.x -= p.v * 9 * dt; if (p.y > h) { p.y = -20; p.x = rand(0, w + 60); }
        g.strokeStyle = "rgba(170,205,235,.45)"; g.lineWidth = 1; g.beginPath(); g.moveTo(p.x, p.y); g.lineTo(p.x - p.l * 0.15, p.y + p.l); g.stroke();
      } else if (p.k === "n") {
        p.ph += dt; p.y += p.v * 40 * dt; p.x += Math.sin(p.ph) * 0.4; if (p.y > h) { p.y = -5; p.x = rand(0, w); }
        g.fillStyle = "rgba(255,255,255,.85)"; g.beginPath(); g.arc(p.x, p.y, p.r, 0, 6.283); g.fill();
      }
    }
    // shooting stars
    if (this.has("stars") && this.o.shooting !== false) {
      this.nextShoot -= dt;
      if (!this.shoot && this.nextShoot <= 0) {
        this.shoot = { x: rand(w * 0.15, w * 0.9), y: rand(0, h * 0.3), vx: -rand(500, 800), vy: rand(180, 320), life: 0 };
        this.nextShoot = rand(4, 9);
      }
      var s = this.shoot;
      if (s) {
        s.life += dt; s.x += s.vx * dt; s.y += s.vy * dt;
        var len = 0.12, tx = s.x - s.vx * len, ty = s.y - s.vy * len, fade = Math.max(0, 1 - s.life / 0.9);
        var lg = g.createLinearGradient(s.x, s.y, tx, ty);
        lg.addColorStop(0, "rgba(255,255,255," + fade + ")"); lg.addColorStop(1, "rgba(255,255,255,0)");
        g.strokeStyle = lg; g.lineWidth = 1.6; g.beginPath(); g.moveTo(s.x, s.y); g.lineTo(tx, ty); g.stroke();
        if (s.life > 0.9) this.shoot = null;
      }
    }
    if (this.has("flash") && Math.random() < 0.004) { g.fillStyle = "rgba(255,255,255,.25)"; g.fillRect(0, 0, w, h); }
  };
  fx.scene = function (canvas, modes, opts) { return new Scene(canvas, modes, opts); };

  // Weather particles for a forecast box, from a WMO weather code
  fx.weatherFor = function (box, code) {
    if (reduce || !box) return;
    var modes = (code >= 71 && code <= 77) || code === 85 || code === 86 ? ["snow"] :
      code >= 95 ? ["rain", "flash"] : (code >= 51 && code <= 67) || (code >= 80 && code <= 82) ? ["rain"] : ["stars"];
    var c = document.createElement("canvas"); c.className = "wx"; box.insertBefore(c, box.firstChild);
    fx.scene(c, modes, { starTop: 1, shooting: modes[0] === "stars" });
  };

  // ---------------------------------------------------------------- page behaviors
  function init() {
    // canvases declared in markup: <canvas class="fx" data-fx="stars fireflies">
    Array.prototype.forEach.call(document.querySelectorAll("canvas[data-fx]"), function (c) {
      var o = {};
      if (c.dataset.emberX) o.emberX = +c.dataset.emberX;
      if (c.dataset.starTop) o.starTop = +c.dataset.starTop;
      fx.scene(c, c.dataset.fx.split(/\s+/), o);
    });

    // header: transparent over hero, frosted after scrolling; hide on scroll down
    var hdr = document.querySelector(".site-header"), lastY = 0, bar = document.querySelector(".progress-trail");
    var par = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
    var ticking = false;
    function onScroll() {
      var y = window.scrollY;
      if (hdr) {
        hdr.classList.toggle("scrolled", y > 30);
        hdr.classList.toggle("hide", y > 500 && y > lastY + 4 && !document.getElementById("nav").classList.contains("open"));
        if (y < lastY - 4) hdr.classList.remove("hide");
      }
      lastY = y;
      if (bar) { var max = document.documentElement.scrollHeight - innerHeight; bar.style.width = (max > 0 ? (y / max) * 100 : 0) + "%"; }
      if (!reduce) par.forEach(function (el) { if (y < innerHeight * 1.5) el.style.transform = "translate3d(0," + (y * +el.dataset.parallax).toFixed(1) + "px,0)"; });
      ticking = false;
    }
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
    onScroll();

    // split headline words for a staggered reveal
    Array.prototype.forEach.call(document.querySelectorAll("[data-split]"), function (el) {
      if (reduce) return;
      var words = el.textContent.trim().split(/\s+/);
      el.innerHTML = words.map(function (w, i) { return '<span class="w" style="animation-delay:' + (0.15 + i * 0.07).toFixed(2) + 's">' + w.replace(/[&<>]/g, "") + "</span>"; }).join(" ");
      el.classList.add("split-words");
    });

    // reveal on scroll + charts + counters
    var io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target; el.classList.add("in"); el.classList.remove("pre");
        if (el.dataset.count) count(el);
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }) : null;
    Array.prototype.forEach.call(document.querySelectorAll(".reveal,.reveal-stagger,.chart.pre,[data-count]"), function (el) {
      if (io && !reduce) io.observe(el); else { el.classList.add("in"); el.classList.remove("pre"); if (el.dataset.count) el.textContent = el.dataset.count + (el.dataset.suffix || ""); }
    });
    function count(el) {
      var to = +el.dataset.count, suf = el.dataset.suffix || "", t0 = performance.now(), dur = 1400;
      (function step(now) { var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3); el.textContent = Math.round(to * e) + suf; if (k < 1) requestAnimationFrame(step); })(t0);
    }

    // cursor spotlight on tool cards
    document.addEventListener("pointermove", function (e) {
      var c = e.target.closest && e.target.closest(".tool-card"); if (!c) return;
      var r = c.getBoundingClientRect(); c.style.setProperty("--mx", (e.clientX - r.left) + "px"); c.style.setProperty("--my", (e.clientY - r.top) + "px");
    });

    // table of contents: highlight current section
    var toc = document.querySelectorAll(".toc a[href^='#']");
    if (toc.length && io) {
      var map = {};
      Array.prototype.forEach.call(toc, function (a) { var s = document.getElementById(a.getAttribute("href").slice(1)); if (s) map[s.id] = a; });
      var tio = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { Array.prototype.forEach.call(toc, function (a) { a.classList.remove("on"); }); map[e.target.id].classList.add("on"); } });
      }, { rootMargin: "-20% 0px -70% 0px" });
      Object.keys(map).forEach(function (id) { tio.observe(document.getElementById(id)); });
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
