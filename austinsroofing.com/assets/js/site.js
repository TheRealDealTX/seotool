/* Austin Roofing — site behaviour: nav, sticky header, scroll progress,
   reveal-on-scroll, table of contents, and the rain / hail / sun canvas. */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile nav ----------------------------------------------------------- */
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
      document.body.style.overflow = open ? '' : 'hidden';
    });
    nav.querySelectorAll('.has-mega > a').forEach(function (a) {
      a.addEventListener('click', function (ev) {
        if (window.innerWidth > 1000) return;
        var li = a.parentElement;
        if (!li.classList.contains('is-open')) { ev.preventDefault(); li.classList.add('is-open'); }
      });
    });
  }

  /* Sticky header shadow + roof-ridge scroll progress -------------------- */
  var header = document.querySelector('.site-header');
  var bar = document.querySelector('.scroll-roof span');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('is-stuck', y > 10);
    if (bar) {
      var h = doc.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Reveal on scroll ------------------------------------------------------ */
  var revealables = document.querySelectorAll('.reveal, .roof-build, [data-count]');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-visible');
        if (en.target.hasAttribute('data-count')) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    revealables.forEach(function (el, i) {
      if (el.classList.contains('reveal')) el.style.transitionDelay = (i % 4) * 70 + 'ms';
      io.observe(el);
    });
  } else {
    revealables.forEach(function (el) { el.classList.add('is-visible'); });
  }

  function countUp(el) {
    var end = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var t0 = null;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1200, 1);
      el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suffix;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* Table of contents for blog posts -------------------------------------- */
  var toc = document.querySelector('[data-toc]');
  if (toc) {
    var heads = document.querySelectorAll('.prose--post > h2');
    heads.forEach(function (h) {
      if (!h.id) h.id = 'h-' + h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      li.appendChild(a);
      toc.appendChild(li);
    });
    if (!heads.length) toc.parentElement.remove();
  }

  /* Weather canvas: rain, hail or sun rays -------------------------------- */
  function Weather(canvas) {
    this.c = canvas;
    this.ctx = canvas.getContext('2d');
    this.mode = canvas.getAttribute('data-weather') || 'rain';
    this.parts = [];
    this.running = false;
    this.resize();
    var self = this;
    window.addEventListener('resize', function () { self.resize(); });
  }
  Weather.prototype.resize = function () {
    var r = this.c.getBoundingClientRect();
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    this.w = r.width; this.h = r.height;
    this.c.width = r.width * dpr; this.c.height = r.height * dpr;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.seed();
  };
  Weather.prototype.seed = function () {
    var n = this.mode === 'hail' ? Math.round(this.w / 14) : this.mode === 'rain' ? Math.round(this.w / 5) : 0;
    this.parts = [];
    for (var i = 0; i < n; i++) this.parts.push(this.spawn(true));
  };
  Weather.prototype.spawn = function (anywhere) {
    if (this.mode === 'hail') {
      return { x: Math.random() * this.w, y: anywhere ? Math.random() * this.h : -10, r: 1.5 + Math.random() * 3.5, vy: 6 + Math.random() * 6, vx: -1 + Math.random() * 0.6, bounce: 0 };
    }
    return { x: Math.random() * (this.w + 200), y: anywhere ? Math.random() * this.h : -20, l: 10 + Math.random() * 18, vy: 11 + Math.random() * 8, vx: -2.2, a: 0.15 + Math.random() * 0.35 };
  };
  Weather.prototype.setMode = function (m) { this.mode = m; this.seed(); };
  Weather.prototype.frame = function (t) {
    var ctx = this.ctx, w = this.w, h = this.h;
    ctx.clearRect(0, 0, w, h);
    if (this.mode === 'sun') {
      var cx = w * 0.82, cy = h * 0.05, rot = (t || 0) / 9000;
      var g = ctx.createRadialGradient(cx, cy, 0, cx, cy, h * 0.9);
      g.addColorStop(0, 'rgba(255,214,120,.55)'); g.addColorStop(0.35, 'rgba(255,170,60,.18)'); g.addColorStop(1, 'rgba(255,170,60,0)');
      ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
      ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot);
      for (var k = 0; k < 14; k++) {
        ctx.rotate(Math.PI * 2 / 14);
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(h * 1.4, -40); ctx.lineTo(h * 1.4, 40); ctx.closePath();
        ctx.fillStyle = 'rgba(255,220,150,.045)'; ctx.fill();
      }
      ctx.restore();
      // heat shimmer lines
      ctx.strokeStyle = 'rgba(255,255,255,.06)'; ctx.lineWidth = 2;
      for (var s = 0; s < 6; s++) {
        var yy = h * 0.55 + s * 22;
        ctx.beginPath();
        for (var xx = 0; xx <= w; xx += 20) ctx.lineTo(xx, yy + Math.sin(xx / 60 + (t || 0) / 500 + s) * 4);
        ctx.stroke();
      }
      return;
    }
    for (var i = 0; i < this.parts.length; i++) {
      var p = this.parts[i];
      if (this.mode === 'hail') {
        p.y += p.vy; p.x += p.vx;
        if (p.y > h - 6 && p.bounce < 1) { p.vy = -p.vy * 0.35; p.bounce++; }
        else if (p.bounce) p.vy += 0.6;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(235,248,255,.85)'; ctx.fill();
        if (p.y > h + 10 || p.x < -10) this.parts[i] = this.spawn(false);
      } else {
        p.y += p.vy; p.x += p.vx;
        ctx.strokeStyle = 'rgba(200,230,240,' + p.a + ')'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x + p.vx * 1.6, p.y + p.l); ctx.stroke();
        if (p.y > h) {
          if (Math.random() < 0.3) { ctx.beginPath(); ctx.arc(p.x, h - 2, 2 + Math.random() * 3, Math.PI, 0); ctx.strokeStyle = 'rgba(200,230,240,.25)'; ctx.stroke(); }
          this.parts[i] = this.spawn(false);
        }
      }
    }
  };
  Weather.prototype.start = function () {
    if (this.running) return;
    this.running = true;
    var self = this;
    (function loop(t) { if (!self.running) return; self.frame(t); requestAnimationFrame(loop); })();
  };
  Weather.prototype.stop = function () { this.running = false; };

  if (!reduce) {
    document.querySelectorAll('canvas.weather').forEach(function (cv) {
      var wx = new Weather(cv);
      cv._wx = wx;
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (en) { en[0].isIntersecting ? wx.start() : wx.stop(); }).observe(cv);
      } else { wx.start(); }
    });
  }

  /* Home hero weather toggle + lightning ---------------------------------- */
  var wt = document.querySelector('.weather-toggle');
  var flash = document.querySelector('.lightning');
  if (wt) {
    var heroCanvas = document.querySelector('.home-hero canvas.weather');
    wt.addEventListener('click', function (ev) {
      var b = ev.target.closest('button');
      if (!b) return;
      wt.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      var mode = b.getAttribute('data-mode');
      if (heroCanvas && heroCanvas._wx) heroCanvas._wx.setMode(mode);
      if (mode !== 'sun') strike();
    });
  }
  function strike() {
    if (!flash || reduce) return;
    flash.classList.remove('flash'); void flash.offsetWidth; flash.classList.add('flash');
  }
  if (flash && !reduce) {
    setInterval(function () {
      var hero = document.querySelector('.home-hero canvas.weather');
      if (hero && hero._wx && hero._wx.mode !== 'sun' && hero._wx.running && Math.random() < 0.5) strike();
    }, 7000);
  }

  /* Form: disable button on submit to avoid double sends ------------------ */
  document.querySelectorAll('form.quote-form').forEach(function (f) {
    f.addEventListener('submit', function () {
      var b = f.querySelector('button[type=submit]');
      if (b) { b.disabled = true; b.textContent = 'Sending…'; }
    });
  });

  /* Track phone clicks in GA4 -------------------------------------------- */
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest('a[href^="tel:"]');
    if (a && window.gtag) window.gtag('event', 'phone_click', { link_url: a.href, page_path: location.pathname });
  });
})();
