/* Houston Apartments — site-wide interactions and effects */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Header state + reading progress */
  var header = $('.site-header');
  var bar = $('.progress span');
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 24);
    if (bar) {
      var h = doc.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Mobile drawer */
  var burger = $('.burger'), drawer = $('#drawer');
  if (burger && drawer) {
    var setNav = function (open) {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      drawer.hidden = !open;
      document.body.classList.toggle('nav-open', open);
    };
    burger.addEventListener('click', function () { setNav(burger.getAttribute('aria-expanded') !== 'true'); });
    drawer.addEventListener('click', function (e) { if (e.target.closest('a')) setNav(false); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !drawer.hidden) { setNav(false); burger.focus(); } });
    window.addEventListener('resize', function () { if (window.innerWidth > 1240 && !drawer.hidden) setNav(false); });
  }

  /* Scroll reveal */
  var revealIO = 'IntersectionObserver' in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); revealIO.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0 }) : null;   // threshold 0: very tall blocks (long posts) must still reveal
  window.HA_reveal = function (root) {
    $$('.reveal:not(.in)', root).forEach(function (el) {
      if (revealIO && !reduce) revealIO.observe(el); else el.classList.add('in');
    });
  };
  window.HA_reveal();

  /* Animated counters */
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count')) || 0;
    if (reduce || target === 0) { el.textContent = target.toLocaleString(); return; }
    var start = null, dur = 1600;
    function step(t) {
      if (!start) start = t;
      var p = Math.min(1, (t - start) / dur), eased = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(target * eased).toLocaleString();
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var cio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); cio.unobserve(e.target); } });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cio.observe(c); });
  } else counters.forEach(countUp);

  /* Typewriter in the hero */
  var typer = $('.typer');
  if (typer && !reduce) {
    var words = JSON.parse(typer.getAttribute('data-words') || '[]'), wi = 0, ci = words[0] ? words[0].length : 0, del = true;
    setTimeout(function tick() {
      var w = words[wi];
      ci += del ? -1 : 1;
      typer.textContent = w.slice(0, ci);
      var delay = del ? 38 : 70;
      if (!del && ci === w.length) { del = true; delay = 2200; }
      else if (del && ci === 0) { del = false; wi = (wi + 1) % words.length; delay = 300; }
      setTimeout(tick, delay);
    }, 2600);
  }

  /* Twinkling stars over the skyline */
  var canvas = $('.hero-stars');
  if (canvas && !reduce) {
    var ctx = canvas.getContext('2d'), stars = [], dpr = Math.min(2, window.devicePixelRatio || 1);
    var size = function () {
      canvas.width = canvas.offsetWidth * dpr; canvas.height = canvas.offsetHeight * dpr;
      stars = [];
      for (var i = 0; i < 90; i++) stars.push({ x: Math.random() * canvas.width, y: Math.random() * canvas.height * 0.55, r: Math.random() * 1.4 * dpr + 0.3, p: Math.random() * Math.PI * 2, s: 0.6 + Math.random() * 1.6 });
    };
    size();
    window.addEventListener('resize', size);
    var heroVisible = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) { heroVisible = e[0].isIntersecting; }).observe(canvas);
    (function draw(t) {
      if (heroVisible) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        stars.forEach(function (s) {
          var a = 0.35 + 0.65 * Math.abs(Math.sin(s.p + t / 1000 * s.s));
          ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, 6.283); ctx.fillStyle = 'rgba(255,255,255,' + a.toFixed(2) + ')'; ctx.fill();
        });
      }
      requestAnimationFrame(draw);
    })(0);
  }

  /* 3D tilt + glare on cards and frames */
  if (fine && !reduce) {
    document.addEventListener('pointermove', function (e) {
      var el = e.target.closest && e.target.closest('.tilt');
      $$('.tilt.tilting').forEach(function (t) { if (t !== el) { t.classList.remove('tilting'); t.style.transform = ''; } });
      if (!el) return;
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
      el.classList.add('tilting');
      el.style.transform = 'perspective(900px) rotateX(' + (-y * 6).toFixed(2) + 'deg) rotateY(' + (x * 8).toFixed(2) + 'deg) translateY(-4px)';
    }, { passive: true });
    document.addEventListener('pointermove', function (e) {
      var tile = e.target.closest && e.target.closest('.hood-tile');
      if (!tile) return;
      var r = tile.getBoundingClientRect();
      tile.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
      tile.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
    }, { passive: true });
    /* Magnetic buttons */
    $$('.magnetic').forEach(function (b) {
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.18) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.25) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
  }

  /* Card photo sliders (hover/swipe through photos) */
  document.addEventListener('pointermove', function (e) {
    var media = e.target.closest && e.target.closest('.card-media');
    if (!media || e.pointerType !== 'mouse') return;
    var imgs = media.querySelectorAll('.card-slides img');
    if (imgs.length < 2) return;
    var r = media.getBoundingClientRect();
    var i = Math.min(imgs.length - 1, Math.floor((e.clientX - r.left) / r.width * imgs.length));
    slideTo(media, i);
  }, { passive: true });
  document.addEventListener('pointerout', function (e) {
    var media = e.target.closest && e.target.closest('.card-media');
    if (media && !media.contains(e.relatedTarget)) slideTo(media, 0);
  });
  function slideTo(media, i) {
    var slides = media.querySelector('.card-slides');
    if (!slides || slides._i === i) return;
    slides._i = i;
    slides.style.transform = 'translateX(' + (-100 * i) + '%)';
    $$('.card-dots i', media).forEach(function (d, k) { d.classList.toggle('on', k === i); });
  }
  window.HA_slideTo = slideTo;

  /* Favorites (kept in this browser only) */
  var favKey = 'ha-favs';
  function favs() { try { return JSON.parse(localStorage.getItem(favKey) || '[]'); } catch (e) { return []; } }
  function syncFavs(root) {
    var f = favs();
    $$('[data-fav]', root).forEach(function (b) { b.setAttribute('aria-pressed', String(f.indexOf(+b.getAttribute('data-fav')) > -1)); });
  }
  window.HA_syncFavs = syncFavs;
  syncFavs();
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-fav]');
    if (!b) return;
    e.preventDefault();
    var id = +b.getAttribute('data-fav'), f = favs(), i = f.indexOf(id);
    if (i > -1) f.splice(i, 1); else f.push(id);
    try { localStorage.setItem(favKey, JSON.stringify(f)); } catch (err) { /* private mode */ }
    b.setAttribute('aria-pressed', String(i === -1));
  });

  /* Carousels */
  $$('[data-scroll]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var c = btn.closest('.section').querySelector('[data-carousel]');
      if (c) c.scrollBy({ left: c.clientWidth * 0.9 * +btn.getAttribute('data-scroll'), behavior: 'smooth' });
    });
  });

  /* Tabs (neighborhood groups) */
  $$('.tabs [data-tab]').forEach(function (t) {
    t.addEventListener('click', function () {
      var wrap = t.closest('.section');
      $$('[data-tab]', wrap).forEach(function (x) { x.setAttribute('aria-selected', String(x === t)); });
      $$('[data-panel]', wrap).forEach(function (p) {
        var on = p.getAttribute('data-panel') === t.getAttribute('data-tab');
        p.hidden = !on;
        if (on) $$('.reveal', p).forEach(function (r) { r.classList.remove('in'); void r.offsetWidth; r.classList.add('in'); });
      });
    });
  });

  /* Floor-plan tabs */
  $$('[data-plan-tab]').forEach(function (t) {
    t.addEventListener('click', function () {
      var v = t.getAttribute('data-plan-tab');
      $$('[data-plan-tab]').forEach(function (x) { x.setAttribute('aria-selected', String(x === t)); });
      $$('.plan-group').forEach(function (g) { g.hidden = v !== 'all' && g.getAttribute('data-beds') !== v; });
    });
  });

  /* Long floor-plan lists: show four, then a "show more" toggle */
  $$('.plans').forEach(function (list) {
    var extra = $$('.plan', list).slice(4);
    if (!extra.length) return;
    extra.forEach(function (p) { p.classList.add('more-hidden'); });
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'btn btn-outline btn-sm show-more';
    b.textContent = 'Show ' + extra.length + ' more floor plan' + (extra.length > 1 ? 's' : '');
    b.addEventListener('click', function () { extra.forEach(function (p) { p.classList.remove('more-hidden'); }); b.remove(); });
    list.appendChild(b);
  });

  /* Budget calculator */
  var calc = $('[data-calc]');
  if (calc) {
    var range = $('input[type=range]', calc);
    var fmt = function (n) { return '$' + Math.round(n).toLocaleString(); };
    var update = function () {
      var inc = +range.value, rent = inc / 12 / 3, low = inc / 12 * 0.25;
      $('.calc-income', calc).textContent = fmt(inc);
      $('.calc-rent', calc).textContent = fmt(rent);
      $('.calc-range', calc).textContent = fmt(low) + ' – ' + fmt(rent);
      $('.gauge-fill', calc).style.width = Math.min(100, (rent - 600) / (6000 - 600) * 100) + '%';
      $('.calc-go', calc).href = '/apartments/under-' + Math.round(rent / 50) * 50 + '/';
    };
    range.addEventListener('input', update);
    update();
  }

  /* Lead modal + forms */
  var modal = $('#lead-modal');
  var lastFocus = null;
  function openLead(trigger) {
    if (!modal) return;
    lastFocus = trigger;
    var form = $('form', modal), forLine = $('.lead-for', modal);
    form.reset();
    $('.form-msg', form).textContent = '';
    $$('[data-us-phone]', form).forEach(function (i) { i.classList.remove('valid', 'invalid'); var er = i.parentNode.querySelector('.field-err'); if (er) er.hidden = true; });
    form.property_id.value = trigger.getAttribute('data-lead-prop') || '';
    form.page.value = location.pathname;
    var name = trigger.getAttribute('data-lead-name');
    forLine.hidden = !name;
    forLine.textContent = name ? 'About: ' + name : '';
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    setTimeout(function () { form.name.focus(); }, 50);
  }
  function closeLead() {
    if (!modal || modal.hidden) return;
    modal.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && document.body.contains(lastFocus)) lastFocus.focus();
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-lead]');
    if (t) { e.preventDefault(); openLead(t); return; }
    if (e.target.closest('[data-close]')) closeLead();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeLead(); });

  /* Free-search popup: once per browser session, 5 s after the first page view. Skipped
     for people who already sent a request, and never shown over another open dialog. */
  (function () {
    var seen;
    try { seen = sessionStorage.getItem('ha-popup') || localStorage.getItem('ha-lead-sent'); } catch (e) { seen = '1'; }
    if (seen || !modal || $('.form-card .lead-form')) return;   // not on the contact page, which already has the form
    try { sessionStorage.setItem('ha-popup', 'scheduled'); } catch (e) { return; }
    setTimeout(function () {
      var busy = !modal.hidden || $('.lightbox:not([hidden])') || document.body.classList.contains('nav-open') ||
        (document.activeElement && /INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName));
      if (busy) return;
      var t = document.createElement('button');
      t.setAttribute('data-lead-name', '');
      openLead(t);
      lastFocus = null;
      try { sessionStorage.setItem('ha-popup', 'shown'); } catch (e) { /* ignore */ }
    }, 5000);
  })();

  /* Back to top (the header is sticky, so an #top anchor never scrolls) */
  document.addEventListener('click', function (e) {
    if (!e.target.closest('[data-to-top]')) return;
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
  });

  /*
   * US phone field: "+1 " is fixed, digits format as "+1 (832) 297-3982" while typing,
   * and the form only submits with a US area code. Mirrors us_phone() in bootstrap.php.
   */
  var NON_US = [204, 226, 236, 249, 250, 257, 263, 289, 306, 343, 354, 365, 367, 368, 382, 403, 416, 418, 428, 431, 437, 438, 450, 460,
    468, 474, 506, 514, 519, 548, 579, 581, 584, 587, 600, 604, 613, 622, 639, 647, 672, 683, 705, 709, 742, 753, 778, 780,
    782, 807, 819, 825, 867, 873, 879, 902, 905, 242, 246, 264, 268, 284, 345, 441, 473, 649, 658, 664, 721, 758, 767, 784,
    809, 829, 849, 868, 869, 876, 500, 521, 522, 523, 524, 525, 526, 527, 528, 529, 533, 544, 566, 577, 588, 700, 710, 800,
    822, 833, 844, 855, 866, 877, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 900, 976];
  function phoneDigits(v) { var d = String(v).replace(/\D/g, ''); if (d.indexOf('1') === 0 && d.length > 10) d = d.slice(1); else if (/^\+?1/.test(String(v).trim())) d = d.slice(1); return d.slice(0, 10); }
  function formatPhone(d) {
    var s = '+1 ';
    if (!d.length) return s;
    s += '(' + d.slice(0, 3);
    if (d.length >= 3) s += ') ';
    if (d.length > 3) s += d.slice(3, 6);
    if (d.length > 6) s += '-' + d.slice(6, 10);
    return s;
  }
  function phoneProblem(d) {
    if (d.length < 10) return d.length ? 'Enter all 10 digits of your phone number.' : 'Please enter your phone number.';
    var area = +d.slice(0, 3), ex = d.slice(3, 6);
    if (d[0] < '2' || d[1] === '9' || d.slice(1, 3) === '11' || NON_US.indexOf(area) > -1 || /^(37|96)/.test(d)) return 'Please use a US phone number – ' + d.slice(0, 3) + ' isn’t a US area code.';
    if (ex[0] < '2' || ex.slice(1) === '11' || ex === '555' || /^(\d)\1{9}$/.test(d) || /^\d{3}(1234567|0000000)$/.test(d)) return 'That phone number doesn’t look valid.';
    return '';
  }
  function setupPhone(input) {
    var err = input.parentNode.querySelector('.field-err');
    var show = function (force) {
      var d = phoneDigits(input.value), p = phoneProblem(d);
      var visible = p && (force || d.length >= 10 || (d.length >= 3 && /area code/.test(p)));
      input.setCustomValidity(p);
      input.classList.toggle('invalid', !!visible);
      input.classList.toggle('valid', !p);
      if (err) { err.hidden = !visible; err.textContent = visible ? p : ''; }
      var msg = input.form && input.form.querySelector('.form-msg.err');
      if (!p && msg) { msg.textContent = ''; msg.className = 'form-msg'; }
      return !p;
    };
    input.addEventListener('focus', function () { if (!input.value) input.value = '+1 '; requestAnimationFrame(function () { input.setSelectionRange(input.value.length, input.value.length); }); });
    input.addEventListener('blur', function () { if (phoneDigits(input.value) === '') input.value = ''; else show(true); });
    input.addEventListener('keydown', function (e) {
      // never delete the fixed "+1 " prefix
      if ((e.key === 'Backspace' && input.selectionStart <= 3 && input.selectionEnd <= 3) || (e.key === 'Delete' && input.selectionStart < 3)) e.preventDefault();
    });
    input.addEventListener('input', function () {
      var d = phoneDigits(input.value);
      input.value = formatPhone(d);
      input.setSelectionRange(input.value.length, input.value.length);
      show(false);
    });
    input._validate = function () { return show(true); };
  }
  $$('[data-us-phone]').forEach(setupPhone);

  $$('.lead-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = $('.form-msg', form), btn = $('button[type=submit]', form);
      if (!form.name.value.trim()) {
        msg.className = 'form-msg err'; msg.textContent = 'Please add your name.'; form.name.focus(); return;
      }
      if (form.phone._validate && !form.phone._validate()) {
        msg.className = 'form-msg err'; msg.textContent = 'Please enter a valid US phone number.'; form.phone.focus(); return;
      }
      if (!/^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(form.email.value.trim())) {
        msg.className = 'form-msg err'; msg.textContent = 'Please enter a valid email address.'; form.email.focus(); return;
      }
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch('/api/lead', { method: 'POST', body: new FormData(form) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) throw new Error(j.error || 'Something went wrong.');
          msg.className = 'form-msg ok';
          msg.textContent = 'Thanks! A Houston Apartments locator will reach out shortly.';
          form.reset();
          $$('[data-us-phone]', form).forEach(function (i) { i.classList.remove('valid', 'invalid'); });
          try { sessionStorage.setItem('ha-popup', 'done'); localStorage.setItem('ha-lead-sent', '1'); } catch (er) { /* storage blocked */ }
          if (window.gtag) gtag('event', 'generate_lead', { form_location: location.pathname });
          confetti(btn);
        })
        .catch(function (err) { msg.className = 'form-msg err'; msg.textContent = err.message + ' You can also call ' + '(832) 720-7978.'; })
        .finally(function () { btn.disabled = false; btn.textContent = 'Send my request'; });
    });
  });

  /* Small celebratory burst on successful submit */
  function confetti(origin) {
    if (reduce) return;
    var r = origin.getBoundingClientRect(), colors = ['#f5a524', '#e2445c', '#5b3fd6', '#1d4466'];
    for (var i = 0; i < 36; i++) {
      var p = document.createElement('i');
      p.style.cssText = 'position:fixed;z-index:2000;width:8px;height:12px;border-radius:2px;pointer-events:none;left:' + (r.left + r.width / 2) + 'px;top:' + (r.top + r.height / 2) + 'px;background:' + colors[i % 4];
      document.body.appendChild(p);
      var a = Math.random() * Math.PI * 2, v = 80 + Math.random() * 160;
      p.animate([{ transform: 'translate(0,0) rotate(0)', opacity: 1 },
        { transform: 'translate(' + Math.cos(a) * v + 'px,' + (Math.sin(a) * v - 80) + 'px) rotate(' + (Math.random() * 720) + 'deg)', opacity: 0 }],
        { duration: 900 + Math.random() * 500, easing: 'cubic-bezier(.2,.8,.2,1)' }).onfinish = (function (el) { return function () { el.remove(); }; })(p);
    }
  }

  /* Property gallery lightbox */
  var lb = $('#lightbox');
  if (lb) {
    var list = JSON.parse($('.lb-data', lb).textContent), idx = 0, img = $('img', lb), cap = $('figcaption', lb);
    var show = function (i) { idx = (i + list.length) % list.length; img.src = list[idx]; cap.textContent = (idx + 1) + ' / ' + list.length; };
    document.addEventListener('click', function (e) {
      var o = e.target.closest('[data-open]');
      if (o) { list = JSON.parse($('.lb-data', lb).textContent); show(+o.getAttribute('data-open')); lb.hidden = false; document.body.style.overflow = 'hidden'; return; }
      var z = e.target.closest('[data-zoom]');
      if (z) { list = [z.getAttribute('data-zoom')]; show(0); lb.hidden = false; document.body.style.overflow = 'hidden'; return; }
      if (e.target.closest('[data-lb]')) show(idx + +e.target.closest('[data-lb]').getAttribute('data-lb'));
      if (e.target.closest('[data-lb-close]') || e.target === lb) { lb.hidden = true; document.body.style.overflow = ''; }
    });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') { lb.hidden = true; document.body.style.overflow = ''; }
      if (e.key === 'ArrowRight') show(idx + 1);
      if (e.key === 'ArrowLeft') show(idx - 1);
    });
    var sx = 0;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { var dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 40) show(idx + (dx < 0 ? 1 : -1)); });
  }
})();
