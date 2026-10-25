/* Monetizing Influencers - site.js
   Navigation, scroll effects, card tilt, counters, hero canvas, confetti,
   copy buttons and AJAX forms. Exposes window.MI helpers for tool pages. */
(function () {
  'use strict';
  var doc = document, root = doc.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var MI = window.MI = {};

  /* ---- mobile nav ---- */
  var toggle = doc.querySelector('.nav-toggle'), nav = doc.getElementById('main-nav');
  if (toggle && nav) {
    var setNav = function (open) {
      nav.classList.toggle('open', open);
      doc.body.classList.toggle('menu-open', open);
      toggle.setAttribute('aria-expanded', open);
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      doc.body.style.overflow = open ? 'hidden' : '';
      if (!open) nav.querySelectorAll('.has-sub.open').forEach(function (li) { li.classList.remove('open'); });
    };
    toggle.addEventListener('click', function () { setNav(!nav.classList.contains('open')); });
    nav.querySelectorAll('.has-sub > a').forEach(function (a) {
      a.addEventListener('click', function (ev) {
        if (window.innerWidth > 1020) return;
        var li = a.parentElement;
        // first tap (or a tap on the caret) expands the group; a second tap on the label follows the link
        if (!li.classList.contains('open') || ev.target.closest('.caret')) { ev.preventDefault(); li.classList.toggle('open'); }
      });
    });
    nav.addEventListener('click', function (ev) {
      var a = ev.target.closest('a');
      if (a && !ev.defaultPrevented && window.innerWidth <= 1020) setNav(false);
    });
    doc.addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && nav.classList.contains('open')) { setNav(false); toggle.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 1020 && nav.classList.contains('open')) setNav(false); });
  }

  /* ---- header state, progress bar, back-to-top ---- */
  var header = doc.querySelector('.site-header'), bar = doc.querySelector('.scroll-progress'), top = doc.querySelector('.to-top');
  function onScroll() {
    var y = window.scrollY, h = root.scrollHeight - window.innerHeight;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? y / h : 0) + ')';
    if (top) top.classList.toggle('show', y > 900);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* ---- reveal on scroll ---- */
  var reveals = doc.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var el = en.target, sibs = el.parentElement ? Array.prototype.indexOf.call(el.parentElement.children, el) : 0;
          el.style.transitionDelay = Math.min(sibs, 6) * 70 + 'ms';
          el.classList.add('in');
          io.unobserve(el);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---- animated counters: <b data-count="250" data-prefix="$" data-suffix="K"> ---- */
  function runCount(el) {
    var end = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
    var pre = el.dataset.prefix || '', suf = el.dataset.suffix || '', t0 = null, dur = 1600;
    if (reduce) { el.textContent = pre + end.toLocaleString(undefined, { minimumFractionDigits: dec }) + suf; return; }
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1), v = end * (1 - Math.pow(1 - p, 3));
      el.textContent = pre + v.toLocaleString(undefined, { minimumFractionDigits: dec, maximumFractionDigits: dec }) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = doc.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { runCount(en.target); co.unobserve(en.target); } });
    }, { threshold: .5 });
    counters.forEach(function (c) { co.observe(c); });
  } else counters.forEach(runCount);

  /* ---- cursor glow, card spotlight + tilt, magnetic buttons ---- */
  if (fine && !reduce) {
    var glow = doc.querySelector('.cursor-glow');
    window.addEventListener('pointermove', function (e) {
      if (glow) glow.style.transform = 'translate(' + e.clientX + 'px,' + e.clientY + 'px)';
    }, { passive: true });
    doc.querySelectorAll('.card').forEach(function (card) {
      var tilt = card.classList.contains('tilt');
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
        card.style.setProperty('--mx', x + 'px');
        card.style.setProperty('--my', y + 'px');
        if (tilt) card.style.transform = 'perspective(900px) rotateX(' + ((y / r.height - .5) * -7) + 'deg) rotateY(' + ((x / r.width - .5) * 9) + 'deg) translateY(-4px)';
      });
      card.addEventListener('pointerleave', function () { card.style.transform = ''; });
    });
    doc.querySelectorAll('.btn-glow').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--x', e.clientX - r.left + 'px');
        b.style.setProperty('--y', e.clientY - r.top + 'px');
      });
    });
    doc.querySelectorAll('.magnetic').forEach(function (m) {
      m.addEventListener('pointermove', function (e) {
        var r = m.getBoundingClientRect();
        m.style.transform = 'translate(' + (e.clientX - r.left - r.width / 2) * .25 + 'px,' + (e.clientY - r.top - r.height / 2) * .35 + 'px)';
      });
      m.addEventListener('pointerleave', function () { m.style.transform = ''; });
    });
    /* phone parallax */
    var phone = doc.querySelector('.phone'), stage = doc.querySelector('.phone-stage');
    if (phone && stage) {
      stage.addEventListener('pointermove', function (e) {
        var r = stage.getBoundingClientRect();
        phone.style.transform = 'rotateY(' + ((e.clientX - r.left) / r.width - .5) * 24 + 'deg) rotateX(' + ((e.clientY - r.top) / r.height - .5) * -18 + 'deg)';
      });
      stage.addEventListener('pointerleave', function () { phone.style.transform = ''; });
    }
  }

  /* ---- typewriter: <span class="typer" data-words='["a","b"]'> ---- */
  doc.querySelectorAll('.typer').forEach(function (el) {
    var words; try { words = JSON.parse(el.dataset.words); } catch (e) { return; }
    if (reduce || !words.length) return;
    var wi = 0, ci = words[0].length, del = true;
    setTimeout(function tick() {
      var w = words[wi];
      ci += del ? -1 : 1;
      el.textContent = w.slice(0, ci);
      var wait = del ? 45 : 85;
      if (!del && ci === w.length) { del = true; wait = 1800; }
      else if (del && ci === 0) { del = false; wi = (wi + 1) % words.length; wait = 300; }
      setTimeout(tick, wait);
    }, 2200);
  });

  /* ---- floating hearts on the hero phone ---- */
  var screen = doc.querySelector('.phone-screen');
  if (screen && !reduce) {
    var heart = '<svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/></svg>';
    var colors = ['#ff3d9a', '#29b6f6', '#ffcc33', '#8b5cf6', '#2ee59d'];
    setInterval(function () {
      if (doc.hidden) return;
      var h = doc.createElement('span');
      h.className = 'heart-burst';
      h.innerHTML = heart;
      h.style.right = 10 + Math.random() * 40 + 'px';
      h.style.bottom = '60px';
      h.style.color = colors[Math.floor(Math.random() * colors.length)];
      h.style.setProperty('--dx', (Math.random() * 60 - 30) + 'px');
      h.style.setProperty('--rot', (Math.random() * 60 - 30) + 'deg');
      screen.appendChild(h);
      setTimeout(function () { h.remove(); }, 2700);
    }, 700);
  }

  /* ---- hero canvas: drifting nodes that connect (a "network" of creators) ---- */
  var cv = doc.getElementById('hero-canvas');
  if (cv && !reduce) {
    var ctx = cv.getContext('2d'), pts = [], W, H, dpr = Math.min(window.devicePixelRatio || 1, 2), mouse = { x: -999, y: -999 };
    var syms = ['$', '♥', '★', '+'];
    function size() {
      W = cv.offsetWidth; H = cv.offsetHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(90, W * H / 14000));
      pts = [];
      for (var i = 0; i < n; i++) pts.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .4, vy: (Math.random() - .5) * .4, s: Math.random() < .14 ? syms[i % 4] : null, r: 1 + Math.random() * 1.8 });
    }
    size();
    window.addEventListener('resize', size);
    cv.parentElement.addEventListener('pointermove', function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    cv.parentElement.addEventListener('pointerleave', function () { mouse.x = mouse.y = -999; });
    (function frame() {
      if (!doc.hidden) {
        ctx.clearRect(0, 0, W, H);
        for (var i = 0; i < pts.length; i++) {
          var p = pts[i];
          p.x += p.vx; p.y += p.vy;
          if (p.x < 0 || p.x > W) p.vx *= -1;
          if (p.y < 0 || p.y > H) p.vy *= -1;
          var dxm = p.x - mouse.x, dym = p.y - mouse.y, dm = Math.sqrt(dxm * dxm + dym * dym);
          if (dm < 120) { p.x += dxm / dm * 1.2; p.y += dym / dm * 1.2; }
          for (var j = i + 1; j < pts.length; j++) {
            var q = pts[j], dx = p.x - q.x, dy = p.y - q.y, d = dx * dx + dy * dy;
            if (d < 15000) {
              ctx.strokeStyle = 'rgba(80,170,255,' + (1 - d / 15000) * .22 + ')';
              ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(q.x, q.y); ctx.stroke();
            }
          }
          if (p.s) { ctx.fillStyle = p.s === '♥' ? 'rgba(255,61,154,.75)' : p.s === '$' ? 'rgba(46,229,157,.75)' : 'rgba(255,204,51,.7)'; ctx.font = '700 15px Outfit, sans-serif'; ctx.fillText(p.s, p.x - 4, p.y + 5); }
          else { ctx.fillStyle = 'rgba(160,210,255,.7)'; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.283); ctx.fill(); }
        }
      }
      requestAnimationFrame(frame);
    })();
  }

  /* ---- confetti ---- */
  MI.confetti = function (n) {
    if (reduce) return;
    var c = doc.createElement('canvas'); c.id = 'confetti'; doc.body.appendChild(c);
    var x = c.getContext('2d'), w = c.width = window.innerWidth, h = c.height = window.innerHeight, ps = [], cols = ['#29b6f6', '#1f6bff', '#8b5cf6', '#ff3d9a', '#ffcc33', '#2ee59d'];
    for (var i = 0; i < (n || 160); i++) ps.push({ x: w / 2, y: h * .45, vx: (Math.random() - .5) * 18, vy: Math.random() * -16 - 4, g: .4 + Math.random() * .2, s: 5 + Math.random() * 6, r: Math.random() * 6, vr: (Math.random() - .5) * .3, c: cols[i % cols.length] });
    var t = 0;
    (function f() {
      x.clearRect(0, 0, w, h);
      ps.forEach(function (p) { p.vy += p.g; p.vx *= .99; p.x += p.vx; p.y += p.vy; p.r += p.vr; x.save(); x.translate(p.x, p.y); x.rotate(p.r); x.fillStyle = p.c; x.fillRect(-p.s / 2, -p.s / 4, p.s, p.s / 2); x.restore(); });
      if (++t < 170) requestAnimationFrame(f); else c.remove();
    })();
  };

  /* ---- copy buttons: <button class="copy-btn" data-copy="#id"> ---- */
  MI.copy = function (text, btn) {
    function done() { if (btn) { var o = btn.innerHTML; btn.textContent = 'Copied!'; setTimeout(function () { btn.innerHTML = o; }, 1600); } }
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, done);
    else { var t = doc.createElement('textarea'); t.value = text; doc.body.appendChild(t); t.select(); try { doc.execCommand('copy'); } catch (e) {} t.remove(); done(); }
  };
  doc.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy]');
    if (!b) return;
    var src = doc.querySelector(b.dataset.copy);
    if (src) MI.copy(src.value !== undefined && src.tagName !== 'DIV' && src.tagName !== 'PRE' ? src.value : src.innerText.replace(/\s*Copy\s*$/, ''), b);
  });

  /* ---- table of contents highlight ---- */
  var tocLinks = doc.querySelectorAll('.toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var to = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('is-current'); }); var a = map[en.target.id]; if (a) a.classList.add('is-current'); }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = doc.getElementById(id); if (h) to.observe(h); });
  }

  /* ---- AJAX forms (fall back to normal POST without JS) ---- */
  doc.querySelectorAll('form.js-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var btn = f.querySelector('[type=submit]'), label = btn ? btn.innerHTML : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      var fd = new FormData(f);
      fd.append('ajax', '1');
      fetch(f.action, { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          var old = f.parentElement.querySelector('.flash'); if (old) old.remove();
          var p = doc.createElement('p');
          p.className = 'flash ' + (j.ok ? 'ok' : 'err');
          p.setAttribute('role', j.ok ? 'status' : 'alert');
          p.textContent = j.message;
          f.parentElement.insertBefore(p, f);
          if (j.ok) { f.reset(); MI.confetti(); }
        })
        .catch(function () { f.submit(); })
        .finally(function () { if (btn) { btn.disabled = false; btn.innerHTML = label; } });
    });
  });

  MI.fmt = function (n) { return '$' + Math.round(n).toLocaleString(); };
  MI.fmtNum = function (n) {
    if (n >= 1e6) return (n / 1e6).toFixed(n >= 1e7 ? 0 : 1).replace(/\.0$/, '') + 'M';
    if (n >= 1e3) return (n / 1e3).toFixed(n >= 1e4 ? 0 : 1).replace(/\.0$/, '') + 'K';
    return String(Math.round(n));
  };
})();
