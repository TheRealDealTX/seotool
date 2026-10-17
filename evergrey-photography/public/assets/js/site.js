/* Evergrey Photography — shared behaviour */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- header: solid on scroll, hide on scroll down ---------- */
  var header = $('.site-header');
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (header) {
      header.classList.toggle('scrolled', y > 40);
      if (!document.body.classList.contains('nav-open')) {
        header.classList.toggle('hide', y > 400 && y > lastY + 4);
        if (y < lastY - 4) header.classList.remove('hide');
      }
    }
    lastY = y;
    var top = $('.to-top');
    if (top) top.classList.toggle('show', y > 900);
    var bar = $('.progress');
    if (bar) {
      var art = $('.prose');
      if (art) {
        var r = art.getBoundingClientRect();
        var p = Math.min(1, Math.max(0, -r.top / (r.height - window.innerHeight * .6)));
        bar.style.width = (p * 100).toFixed(2) + '%';
      }
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- mobile nav ---------- */
  var toggle = $('.nav-toggle');
  var panel = $('#mobile-nav');
  function setNav(open) {
    if (!toggle || !panel) return;
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    panel.classList.toggle('open', open);
    panel.setAttribute('aria-hidden', open ? 'false' : 'true');
    document.body.classList.toggle('nav-open', open);
    if (open) {
      header && header.classList.remove('hide');
      var first = panel.querySelector('a');
      setTimeout(function () { first && first.focus({ preventScroll: true }); }, 350);
    }
  }
  if (toggle && panel) {
    toggle.addEventListener('click', function () { setNav(toggle.getAttribute('aria-expanded') !== 'true'); });
    $$('a', panel).forEach(function (a) { a.addEventListener('click', function () { setNav(false); }); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && panel.classList.contains('open')) { setNav(false); toggle.focus(); }
      if (e.key === 'Tab' && panel.classList.contains('open')) {
        var f = [toggle].concat($$('a', panel));
        var i = f.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 1120 && panel.classList.contains('open')) setNav(false); });
  }

  /* ---------- reveal on scroll ---------- */
  var revealEls = $$('[data-reveal], .img-reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting || en.boundingClientRect.top < 0) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
    revealEls.forEach(function (el, i) {
      var d = el.getAttribute('data-delay');
      if (d) el.style.transitionDelay = d + 'ms';
      io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- parallax ---------- */
  var para = $$('[data-parallax]');
  if (para.length && !reduce) {
    var ticking = false;
    var run = function () {
      var vh = window.innerHeight;
      para.forEach(function (el) {
        var host = el.parentElement.getBoundingClientRect();
        if (host.bottom < -100 || host.top > vh + 100) return;
        var speed = parseFloat(el.getAttribute('data-parallax')) || .15;
        var off = (host.top + host.height / 2 - vh / 2) * -speed;
        el.style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
      });
      ticking = false;
    };
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(run); } }, { passive: true });
    window.addEventListener('resize', run);
    run();
  }

  /* ---------- hero slideshow ---------- */
  var slides = $$('.hero-slides figure');
  var dots = $$('.hero-dots button');
  if (slides.length > 1) {
    var cur = 0, timer;
    var go = function (n) {
      slides[cur].classList.remove('active'); dots[cur] && dots[cur].classList.remove('active');
      cur = (n + slides.length) % slides.length;
      var img = slides[cur].querySelector('img');
      if (img && img.dataset.src) { img.src = img.dataset.src; img.removeAttribute('data-src'); }
      slides[cur].classList.add('active'); dots[cur] && dots[cur].classList.add('active');
      clearTimeout(timer); if (!reduce) timer = setTimeout(function () { go(cur + 1); }, 6000);
    };
    dots.forEach(function (d, i) { d.addEventListener('click', function () { go(i); }); });
    // warm the next slides after load
    window.addEventListener('load', function () {
      slides.forEach(function (s) { var im = s.querySelector('img[data-src]'); if (im) { var p = new Image(); p.src = im.dataset.src; } });
    });
    if (!reduce) timer = setTimeout(function () { go(1); }, 6000);
  }

  /* ---------- drag-to-scroll strip ---------- */
  $$('.strip').forEach(function (strip) {
    var down = false, sx = 0, sl = 0, moved = false;
    strip.addEventListener('mousedown', function (e) { down = true; moved = false; sx = e.pageX; sl = strip.scrollLeft; strip.classList.add('dragging'); });
    window.addEventListener('mouseup', function () { down = false; strip.classList.remove('dragging'); });
    strip.addEventListener('mousemove', function (e) {
      if (!down) return; e.preventDefault();
      var dx = e.pageX - sx; if (Math.abs(dx) > 3) moved = true; strip.scrollLeft = sl - dx;
    });
    strip.addEventListener('click', function (e) { if (moved) e.preventDefault(); }, true);
  });

  /* ---------- before / after ---------- */
  $$('.compare').forEach(function (c) {
    var input = c.querySelector('input');
    var set = function (v) { c.style.setProperty('--pos', v + '%'); };
    input.addEventListener('input', function () { set(input.value); });
    set(input.value);
    if (!reduce && 'IntersectionObserver' in window) {
      var o = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting) return; o.disconnect();
        var t0 = null;
        var anim = function (t) {
          if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1600);
          var v = 50 + Math.sin(k * Math.PI * 2) * 22; input.value = v; set(v);
          if (k < 1) requestAnimationFrame(anim); else { input.value = 50; set(50); }
        };
        requestAnimationFrame(anim);
      }, { threshold: .5 });
      o.observe(c);
    }
  });

  /* ---------- filter chips (journal + portfolio) ---------- */
  $$('[data-filter-group]').forEach(function (group) {
    var target = $(group.getAttribute('data-filter-group'));
    if (!target) return;
    $$('.chip', group).forEach(function (chip) {
      chip.addEventListener('click', function () {
        $$('.chip', group).forEach(function (c) { c.classList.remove('active'); c.setAttribute('aria-pressed', 'false'); });
        chip.classList.add('active'); chip.setAttribute('aria-pressed', 'true');
        var f = chip.getAttribute('data-filter');
        $$('[data-cat]', target).forEach(function (el) {
          var show = f === 'all' || el.getAttribute('data-cat').split(' ').indexOf(f) > -1;
          el.classList.toggle('hidden', !show);
          if (show) { el.classList.add('in'); }
        });
      });
    });
  });

  /* ---------- lightbox ---------- */
  var lb = $('.lightbox');
  if (lb) {
    var items = $$('.g-item');
    var lbImg = $('img', lb), lbCap = $('figcaption', lb), idx = 0, lastFocus;
    var visible = function () { return items.filter(function (i) { return !i.classList.contains('hidden'); }); };
    var show = function (el) {
      var list = visible(); idx = list.indexOf(el);
      lbImg.src = el.getAttribute('data-full'); lbImg.alt = el.querySelector('img').alt;
      lbCap.textContent = el.getAttribute('data-cap') || '';
    };
    var open = function (el) { lastFocus = el; show(el); lb.classList.add('open'); lb.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden'; $('.lb-close', lb).focus(); };
    var close = function () { lb.classList.remove('open'); lb.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; lastFocus && lastFocus.focus(); };
    var step = function (d) { var list = visible(); show(list[(idx + d + list.length) % list.length]); };
    items.forEach(function (el) { el.addEventListener('click', function () { open(el); }); });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', function () { step(-1); });
    $('.lb-next', lb).addEventListener('click', function () { step(1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') step(1); if (e.key === 'ArrowLeft') step(-1);
    });
    var tx = 0;
    lb.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1); });
  }

  /* ---------- table of contents highlight ---------- */
  var tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var tio = new IntersectionObserver(function (en) {
      en.forEach(function (e) {
        if (e.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('active'); }); var a = map[e.target.id]; a && a.classList.add('active'); }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); h && tio.observe(h); });
  }

  /* ---------- back to top ---------- */
  var tt = $('.to-top');
  if (tt) tt.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* ---------- contact form ---------- */
  var form = $('#inquiry-form');
  if (form) {
    var started = Date.now();
    var ts = form.querySelector('[name="ts"]'); if (ts) ts.value = String(started);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = $('.form-status', form);
      var btn = form.querySelector('button[type="submit"]');
      if (!form.checkValidity()) { form.reportValidity(); return; }
      btn.disabled = true; status.className = 'form-status'; status.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (d) {
          if (d.ok) { form.reset(); status.className = 'form-status ok'; status.textContent = 'Thank you — your note is on its way. We reply within two business days.'; }
          else { status.className = 'form-status err'; status.textContent = (d.error || 'Something went wrong.') + ' You can also email info@evergrey-photography.com.'; }
        })
        .catch(function () { status.className = 'form-status err'; status.textContent = 'We could not send that right now. Please email info@evergrey-photography.com.'; })
        .then(function () { btn.disabled = false; });
    });
  }

  /* prefill inquiry from query string (?type=elopement&date=2027-06-12) */
  if (form && location.search) {
    var q = new URLSearchParams(location.search);
    ['type', 'date', 'location'].forEach(function (k) { var el = form.querySelector('[name="' + k + '"]'); if (el && q.get(k)) el.value = q.get(k); });
    if (q.get('estimate')) { var m = form.querySelector('[name="message"]'); if (m) m.value = 'My estimate from your pricing tool: ' + q.get('estimate') + '\n\n'; }
  }

  var yr = $('[data-year]'); if (yr) yr.textContent = new Date().getFullYear();
})();
