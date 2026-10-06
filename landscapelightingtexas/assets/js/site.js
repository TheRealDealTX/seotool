/* Landscape Lighting Texas — site behavior.
   Header, nav, reveals, parallax, hero light switch, fireflies, dusk scrollytelling,
   horizontal gallery, counters, carousels, before/after, quote form, city search. */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  /* ---------- Header + scroll progress ---------- */
  var header = $('[data-header]');
  var bar = $('.scroll-progress');
  var lastY = 0;
  function onScrollChrome() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle('is-scrolled', y > 30);
      header.classList.toggle('is-hidden', y > 500 && y > lastY + 4 && !document.body.classList.contains('nav-open'));
      if (y < lastY - 4) header.classList.remove('is-hidden');
    }
    lastY = y;
    if (bar) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty('--sp', max > 0 ? (y / max).toFixed(4) : 0);
    }
  }

  /* ---------- Mobile nav ---------- */
  var toggle = $('[data-nav-toggle]');
  if (toggle) toggle.addEventListener('click', function () {
    var open = document.body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', open);
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (open && header) header.classList.remove('is-hidden');
  });
  // Close the menu after following a link or on Escape.
  $$('.main-nav a').forEach(function (a) { a.addEventListener('click', function () { if (document.body.classList.contains('nav-open')) toggle.click(); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && document.body.classList.contains('nav-open')) toggle.click(); });
  $$('.submenu-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
      var m = b.nextElementSibling, open = !m.classList.contains('is-open');
      m.classList.toggle('is-open', open);
      b.setAttribute('aria-expanded', open);
    });
  });

  /* ---------- Split headings into words ---------- */
  $$('[data-split]').forEach(function (el) {
    if (reduce) return;
    var words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(function (w, i) {
      return '<span class="split-word"><span style="--i:' + i + '">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span></span>';
    }).join(' ');
    el.classList.add('split-ready');
  });

  /* ---------- Reveal on scroll ---------- */
  var revealEls = $$('.reveal, .reveal-zoom, [data-split], .tx-map');
  // Stagger siblings inside grids.
  $$('.card-grid, .grid-3, .grid-2, .grid-4, .stats, .faq-list, .steps').forEach(function (g) {
    $$(':scope > .reveal, :scope > li', g).forEach(function (c, i) { c.style.setProperty('--d', (i % 6) * 0.08 + 's'); });
  });
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Counters ---------- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var dec = (String(el.getAttribute('data-count')).split('.')[1] || '').length;
    if (reduce) { el.textContent = target.toLocaleString('en-US', { minimumFractionDigits: dec }); return; }
    var start = null, dur = 1800;
    function step(t) {
      if (!start) start = t;
      var p = clamp((t - start) / dur, 0, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = (target * e).toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { countUp(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.4 });
    $$('[data-count]').forEach(function (el) { cio.observe(el); });
  }

  /* ---------- Cursor glow + glow cards + magnetic buttons + tilt ---------- */
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var cursor = $('.cursor-glow');
  if (fine && !reduce) {
    document.body.classList.add('has-cursor');
    window.addEventListener('pointermove', function (e) {
      if (cursor) { cursor.style.setProperty('--cx', e.clientX + 'px'); cursor.style.setProperty('--cy', e.clientY + 'px'); }
    }, { passive: true });
    document.addEventListener('pointermove', function (e) {
      var card = e.target.closest && e.target.closest('.glow-card');
      if (card) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      }
    }, { passive: true });
    $$('.magnetic').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.setProperty('--bx', ((e.clientX - r.left - r.width / 2) * 0.25) + 'px');
        b.style.setProperty('--by', ((e.clientY - r.top - r.height / 2) * 0.35) + 'px');
      });
      b.addEventListener('pointerleave', function () { b.style.setProperty('--bx', '0px'); b.style.setProperty('--by', '0px'); });
    });
    $$('.tilt').forEach(function (c) {
      c.addEventListener('pointermove', function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        c.style.transform = 'perspective(900px) rotateY(' + (x * 7) + 'deg) rotateX(' + (-y * 7) + 'deg) translateY(-6px)';
      });
      c.addEventListener('pointerleave', function () { c.style.transform = ''; });
    });
  }

  /* ---------- Hero: lights switch, spotlight, fireflies, stars ---------- */
  var hero = $('[data-hero]');
  if (hero) {
    var sw = $('[data-light-switch]', hero);
    var setLights = function (on, x, y) {
      if (x != null) { hero.style.setProperty('--lx', x + '%'); hero.style.setProperty('--ly', y + '%'); }
      hero.classList.toggle('lights-on', on);
      if (sw) { sw.setAttribute('aria-pressed', on); $('.switch-label', sw).textContent = on ? 'Lights on' : 'Lights off'; }
    };
    setTimeout(function () { setLights(true, 58, 62); }, reduce ? 0 : 700);
    if (sw) sw.addEventListener('click', function () { setLights(!hero.classList.contains('lights-on'), 70, 70); });
    if (fine && !reduce) hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      hero.style.setProperty('--sx', ((e.clientX - r.left) / r.width * 100) + '%');
      hero.style.setProperty('--sy', ((e.clientY - r.top) / r.height * 100) + '%');
    });
  }
  $$('canvas.fireflies').forEach(function (cv) {
    if (reduce) return;
    var ctx = cv.getContext('2d'), flies = [], w, h, dpr = Math.min(window.devicePixelRatio || 1, 2), running = true;
    function size() { w = cv.offsetWidth; h = cv.offsetHeight; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    size(); window.addEventListener('resize', size);
    var n = Math.round(clamp(w / 28, 18, 60));
    for (var i = 0; i < n; i++) flies.push({ x: Math.random() * w, y: h * 0.35 + Math.random() * h * 0.65, r: 0.8 + Math.random() * 1.8,
      vx: (Math.random() - 0.5) * 0.35, vy: (Math.random() - 0.5) * 0.25, ph: Math.random() * 6.28, sp: 0.01 + Math.random() * 0.03 });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { running = en[0].isIntersecting; if (running) requestAnimationFrame(tick); }).observe(cv);
    function tick() {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      flies.forEach(function (f) {
        f.ph += f.sp; f.x += f.vx + Math.sin(f.ph * 0.7) * 0.25; f.y += f.vy + Math.cos(f.ph * 0.5) * 0.2;
        if (f.x < -10) f.x = w + 10; if (f.x > w + 10) f.x = -10; if (f.y < h * 0.2) f.vy = Math.abs(f.vy); if (f.y > h) f.vy = -Math.abs(f.vy);
        var a = 0.35 + 0.65 * Math.pow((Math.sin(f.ph) + 1) / 2, 3);
        var g = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r * 7);
        g.addColorStop(0, 'rgba(255,236,170,' + a + ')'); g.addColorStop(0.25, 'rgba(255,200,90,' + a * 0.45 + ')'); g.addColorStop(1, 'rgba(255,180,60,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(f.x, f.y, f.r * 7, 0, 6.283); ctx.fill();
      });
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });

  /* ---------- Scroll-driven effects (parallax, dusk, h-gallery, steps) ---------- */
  var parallax = $$('[data-parallax]');
  var heroImgs = hero ? $$('.hero-media img', hero) : [];
  var dusk = $('[data-dusk]');
  var duskSteps = dusk ? $$('.dusk-step', dusk) : [];
  var duskDots = dusk ? $$('.dusk-dots span', dusk) : [];
  var hg = $('[data-hgallery]');
  var hgTrack = hg ? $('.hgallery-track', hg) : null;
  var stepsLists = $$('.steps');
  var desktop = window.matchMedia('(min-width: 1025px)');

  function onScrollFx() {
    var vh = window.innerHeight;
    if (!reduce) {
      parallax.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        var k = parseFloat(el.getAttribute('data-parallax')) || 0.2;
        el.style.transform = 'translate3d(0,' + ((r.top) * -k).toFixed(1) + 'px,0)';
      });
      if (heroImgs.length && window.scrollY < vh * 1.2) {
        heroImgs.forEach(function (im) { im.style.setProperty('--hy', (window.scrollY * 0.35).toFixed(1) + 'px'); });
      }
    }
    if (dusk) {
      var dr = dusk.getBoundingClientRect();
      var p = clamp(-dr.top / (dr.height - vh), 0, 1);
      dusk.style.setProperty('--p', p.toFixed(3));
      // Light "zones" bloom one by one through radial masks.
      var stage = clamp(p * 4, 0, 4);
      var r1 = 0.5 + clamp(stage - 0.6, 0, 1) * 40, r2 = 0.5 + clamp(stage - 1.5, 0, 1) * 45, r3 = 0.5 + clamp(stage - 2.4, 0, 1) * 60;
      dusk.style.setProperty('--mask',
        'radial-gradient(' + r1 + '% ' + (r1 * 0.9) + '% at 50% 88%, #000 30%, transparent 75%),' +
        'radial-gradient(' + r2 + '% ' + (r2 * 1.1) + '% at 18% 40%, #000 30%, transparent 75%),' +
        'radial-gradient(' + r2 + '% ' + (r2 * 1.1) + '% at 85% 35%, #000 30%, transparent 75%),' +
        'radial-gradient(' + r3 + '% ' + (r3 * 0.8) + '% at 52% 38%, #000 30%, transparent 75%)');
      dusk.style.setProperty('--full', clamp((stage - 3.2) / 0.8, 0, 1).toFixed(3));
      var idx = Math.min(duskSteps.length - 1, Math.floor(p * duskSteps.length * 0.999));
      duskSteps.forEach(function (s, i) { s.classList.toggle('is-active', i === idx); });
      duskDots.forEach(function (s, i) { s.classList.toggle('is-active', i === idx); });
    }
    if (hg && hgTrack && desktop.matches && !reduce) {
      var gr = hg.getBoundingClientRect();
      var gp = clamp(-gr.top / (gr.height - vh), 0, 1);
      var dist = hgTrack.scrollWidth - window.innerWidth;
      hgTrack.style.setProperty('--hx', (-dist * gp).toFixed(1) + 'px');
      hg.style.setProperty('--hp', gp.toFixed(3));
      $$('.hg-item img', hgTrack).forEach(function (im, i) { im.style.setProperty('--ix', ((gp * 8 - i * 1.6) * 6).toFixed(1) + '%'); });
    }
    stepsLists.forEach(function (s) {
      var r = s.getBoundingClientRect();
      s.style.setProperty('--steps-p', clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1).toFixed(3));
    });
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () { onScrollChrome(); onScrollFx(); ticking = false; });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- Before / after ---------- */
  $$('[data-ba]').forEach(function (ba) {
    var range = $('.ba-range', ba);
    var set = function (v) { ba.style.setProperty('--pos', v + '%'); };
    range.addEventListener('input', function () { set(range.value); });
    // Gentle intro sweep when it scrolls into view.
    if ('IntersectionObserver' in window && !reduce) {
      var o = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting) return; o.disconnect();
        var t0 = null;
        (function anim(t) {
          if (!t0) t0 = t; var k = clamp((t - t0) / 1800, 0, 1);
          var v = 50 + Math.sin(k * Math.PI * 2) * 30 * (1 - k);
          set(v); range.value = v; if (k < 1) requestAnimationFrame(anim);
        })(performance.now());
      }, { threshold: 0.5 });
      o.observe(ba);
    }
  });

  /* ---------- Reviews carousel ---------- */
  $$('[data-carousel]').forEach(function (c) {
    var track = $('.reviews-track', c);
    var by = function (dir) { var card = track.firstElementChild; track.scrollBy({ left: dir * (card.offsetWidth + 22), behavior: 'smooth' }); };
    $('[data-prev]', c).addEventListener('click', function () { by(-1); });
    $('[data-next]', c).addEventListener('click', function () { by(1); });
    if (!reduce) {
      var timer = setInterval(function () {
        if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 5) track.scrollTo({ left: 0, behavior: 'smooth' }); else by(1);
      }, 6000);
      c.addEventListener('pointerenter', function () { clearInterval(timer); });
    }
  });

  /* ---------- TOC active state ---------- */
  var toc = $('[data-toc]');
  if (toc && 'IntersectionObserver' in window) {
    var links = $$('a', toc);
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { links.forEach(function (a) { a.classList.remove('is-active'); }); var a = map[en.target.id]; if (a) a.classList.add('is-active'); }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* ---------- City search (areas) ---------- */
  var cs = $('[data-city-search]');
  if (cs) {
    var dir = $('[data-city-dir]'), empty = $('[data-city-empty]');
    cs.addEventListener('input', function () {
      var q = cs.value.trim().toLowerCase(), any = false;
      $$('.city-group', dir).forEach(function (g) {
        var shown = 0;
        $$('li', g).forEach(function (li) { var m = !q || li.textContent.toLowerCase().indexOf(q) > -1; li.hidden = !m; if (m) shown++; });
        g.hidden = shown === 0; if (shown) any = true;
      });
      if (empty) empty.hidden = any;
    });
  }

  /* ---------- Blog search ---------- */
  var bs = $('[data-blog-search]');
  if (bs) bs.addEventListener('input', function () {
    var q = bs.value.trim().toLowerCase();
    $$('[data-post]').forEach(function (p) { p.hidden = q && p.textContent.toLowerCase().indexOf(q) < 0; });
  });

  /* ---------- Gallery filter + lightbox ---------- */
  var gal = $('[data-gallery]');
  if (gal) {
    $$('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        $$('[data-filter]').forEach(function (x) { x.classList.toggle('is-on', x === b); });
        $$('figure', gal).forEach(function (fig) { fig.classList.toggle('is-hidden', f !== 'all' && fig.getAttribute('data-cat').indexOf(f) < 0); });
      });
    });
    var lb = document.createElement('div');
    lb.className = 'lightbox'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    lb.innerHTML = '<button type="button" aria-label="Close">×</button><div><img alt=""><p></p></div>';
    document.body.appendChild(lb);
    var close = function () { lb.classList.remove('is-open'); };
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.tagName === 'BUTTON') close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    $$('figure', gal).forEach(function (fig) {
      fig.tabIndex = 0;
      var open = function () {
        var im = $('img', fig);
        $('img', lb).src = im.getAttribute('data-full') || im.src; $('img', lb).alt = im.alt;
        $('p', lb).textContent = ($('strong', fig) || {}).textContent || '';
        lb.classList.add('is-open'); $('button', lb).focus();
      };
      fig.addEventListener('click', open);
      fig.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(); });
    });
  }

  /* ---------- Quote form ---------- */
  $$('[data-quote-form]').forEach(function (form) {
    var status = $('.qf-status', form);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $$('[required]', form).forEach(function (inp) {
        var bad = !inp.value.trim() || (inp.type === 'email' && !/^\S+@\S+\.\S+$/.test(inp.value)) || (inp.type === 'tel' && inp.value.replace(/\D/g, '').length < 10);
        inp.closest('.field').classList.toggle('is-invalid', bad);
        if (bad) ok = false;
      });
      if (!ok) { status.className = 'qf-status err'; status.textContent = 'Please add your first name, a valid email and a 10-digit phone number.'; return; }
      var btn = $('button[type=submit]', form); btn.disabled = true;
      status.className = 'qf-status'; status.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          status.className = 'qf-status ' + (d.ok ? 'ok' : 'err');
          status.textContent = d.message;
          if (d.ok) form.reset();
        })
        .catch(function () { status.className = 'qf-status err'; status.textContent = 'Something went wrong. Please call us at +1 (281) 704-7210.'; })
        .then(function () { btn.disabled = false; });
    });
  });
})();
