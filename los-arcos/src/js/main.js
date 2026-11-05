/* Los Arcos — concept site interactions (no dependencies) */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');

  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }

  /* ---------- Toast ---------- */
  var toastEl, toastT;
  function toast(msg) {
    if (!toastEl) { toastEl = d.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); toastEl.setAttribute('aria-live', 'polite'); d.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('is-visible');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('is-visible'); }, 3800);
  }

  /* Placeholder links (resident portal, application, social) */
  $$('[data-placeholder]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      toast(a.getAttribute('data-placeholder') || 'Demo link: this will connect to the live property portal.');
    });
  });

  /* ---------- Announcement banner ---------- */
  var ann = $('.announce');
  if (ann) {
    if (store('la-announce') === 'closed') ann.hidden = true;
    var x = $('.announce__close', ann);
    x && x.addEventListener('click', function () { ann.hidden = true; store('la-announce', 'closed'); });
  }

  /* ---------- Sticky header ---------- */
  var header = $('.header');
  function onScroll() { header && header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- Mobile menu ---------- */
  var btn = $('.menu-btn'), nav = $('#site-nav');
  function setMenu(open) {
    if (open && header) {
      header.classList.remove('is-hidden');
      /* open the panel right under the header, wherever the header sits (bars above it at page top) */
      nav.style.setProperty('--nav-top', Math.max(0, Math.round(header.getBoundingClientRect().bottom)) + 'px');
    }
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    nav.classList.toggle('is-open', open);
    d.body.classList.toggle('nav-open', open);
  }
  if (btn && nav) {
    btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('is-open')) { setMenu(false); btn.focus(); } });
    $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    window.addEventListener('resize', function () { if (window.innerWidth > 1100) setMenu(false); });
  }

  /* ---------- Hero slider ---------- */
  var hero = $('.hero');
  if (hero) {
    var slides = $$('.hero__slide', hero), msgs = $$('.hero__msg', hero), dots = $$('.hero__dot', hero), pause = $('.hero__pause', hero);
    var i = 0, timer, paused = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function go(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('is-active', k === i); });
      msgs.forEach(function (m, k) { m.classList.toggle('is-active', k === i); m.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
      dots.forEach(function (b, k) { b.classList.toggle('is-active', k === i); b.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      var img = slides[i].querySelector('img[data-src]');
      if (img) { img.src = img.getAttribute('data-src'); img.srcset = img.getAttribute('data-srcset'); img.removeAttribute('data-src'); }
      schedule();
    }
    function schedule() { clearTimeout(timer); if (!paused) timer = setTimeout(function () { go(i + 1); }, 7000); }
    dots.forEach(function (b, k) { b.addEventListener('click', function () { go(k); }); });
    function setPaused(p) {
      paused = p; hero.classList.toggle('is-paused', p);
      if (pause) { pause.setAttribute('aria-label', p ? 'Play slideshow' : 'Pause slideshow'); pause.innerHTML = p ? '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>' : '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>'; }
      schedule();
    }
    pause && pause.addEventListener('click', function () { setPaused(!paused); });
    setPaused(paused);
    // warm up remaining slides after load
    window.addEventListener('load', function () {
      setTimeout(function () { $$('img[data-src]', hero).forEach(function (img) { var p = new Image(); p.srcset = img.getAttribute('data-srcset'); p.sizes = '100vw'; p.src = img.getAttribute('data-src'); }); }, 1500);
    });
  }


  /* =========================================================
     Advanced effects (progressive enhancement)
     ========================================================= */
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* Split headings into words for staggered reveals */
  function splitWords(el) {
    if (el.getAttribute('data-split-done')) return;
    var i = 0, walker = d.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      var parts = node.nodeValue.split(/(\s+)/), frag = d.createDocumentFragment();
      parts.forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
        var w = d.createElement('span'); w.className = 'w';
        var inner = d.createElement('span'); inner.style.setProperty('--i', i++); inner.textContent = part;
        w.appendChild(inner); frag.appendChild(w);
      });
      node.parentNode.replaceChild(frag, node);
    });
    el.setAttribute('data-split-done', '1');
  }
  if (!reduce) {
    $$('.hero__title').forEach(splitWords);
    $$('.section h2:not(.sr-only), .page-hero h1, .section h1, .cta h2').forEach(function (h) {
      if (h.closest('.form-card') || h.closest('.portal')) return;
      splitWords(h); h.classList.add('split-words', 'reveal');
    });
    /* clip-path hides an element from IntersectionObserver, so watch its parent */
    var clips = $$('.arch-img, .page-hero__img');
    clips.forEach(function (a) { a.classList.add('clip-reveal'); });
    if ('IntersectionObserver' in window) {
      var clipIO = new IntersectionObserver(function (ents) {
        ents.forEach(function (en) {
          if (!en.isIntersecting) return;
          Array.prototype.forEach.call(en.target.children, function (c) { if (c.classList.contains('clip-reveal')) c.classList.add('is-in'); });
          clipIO.unobserve(en.target);
        });
      }, { threshold: 0.12 });
      clips.forEach(function (a) { clipIO.observe(a.parentNode); });
    } else { clips.forEach(function (a) { a.classList.add('is-in'); }); }
  }

  /* Scroll progress (CSS scroll-timeline where supported, JS fallback) + smart header */
  var prog = d.createElement('div'); prog.className = 'progress'; prog.setAttribute('aria-hidden', 'true'); d.body.appendChild(prog);
  var cssProgress = window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()');
  var lastY = window.scrollY, dir = 0, dirStart = lastY, ticking = false;
  function onFrame() {
    var y = window.scrollY, max = d.documentElement.scrollHeight - window.innerHeight;
    if (!cssProgress) prog.style.setProperty('--p', max > 0 ? (y / max).toFixed(4) : 0);
    var nd = y > lastY ? 1 : (y < lastY ? -1 : dir);
    if (nd !== dir) { dir = nd; dirStart = lastY; }
    if (header && !reduce && !d.body.classList.contains('nav-open')) {
      if (y < 120 || (dir < 0 && dirStart - y > 40)) header.classList.remove('is-hidden');
      else if (dir > 0 && y - dirStart > 60 && y > 320) header.classList.add('is-hidden');
    }
    lastY = y; ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onFrame); } }, { passive: true });
  d.addEventListener('focusin', function (e) { if (header && header.contains(e.target)) header.classList.remove('is-hidden'); });

  /* Animated counters */
  function countUp(el) {
    var raw = el.getAttribute('data-count'), target = parseFloat(raw), dec = (raw.split('.')[1] || '').length;
    var suffix = el.getAttribute('data-suffix') || '', start = null, dur = 1600;
    function step(ts) {
      if (!start) start = ts;
      var t = Math.min(1, (ts - start) / dur), e = 1 - Math.pow(1 - t, 3);
      el.textContent = (target * e).toFixed(dec).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + suffix;
      if (t < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !reduce) {
    var cio = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { countUp(en.target); cio.unobserve(en.target); } });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* Cursor spotlight + 3D tilt, magnetic buttons, hero drift (desktop pointers only) */
  if (finePointer && !reduce) {
    $$('.tile, .plan, .card, .theme, .portal, .amenity-list li, .rating-card, .commute div').forEach(function (card) {
      card.classList.add('fx-card');
      var tilt = card.matches('.tile, .plan, .portal, .rating-card');
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        card.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); card.style.setProperty('--my', (y * 100).toFixed(1) + '%');
        if (tilt) { card.classList.add('is-tilting'); card.style.transform = 'perspective(900px) rotateX(' + ((0.5 - y) * 6).toFixed(2) + 'deg) rotateY(' + ((x - 0.5) * 8).toFixed(2) + 'deg) translateY(-6px)'; }
      });
      card.addEventListener('pointerleave', function () { card.classList.remove('is-tilting'); card.style.transform = ''; });
    });
    $$('.btn').forEach(function (b) {
      b.classList.add('magnetic');
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.28).toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
    var heroInner = $('.hero__inner .wrap');
    if (hero && heroInner) {
      heroInner.style.transition = 'transform .8s cubic-bezier(.2,.7,.2,1)';
      hero.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect();
        heroInner.style.transform = 'translate3d(' + (((e.clientX - r.left) / r.width - 0.5) * -14).toFixed(1) + 'px,' + (((e.clientY - r.top) / r.height - 0.5) * -10).toFixed(1) + 'px,0)';
      });
      hero.addEventListener('pointerleave', function () { heroInner.style.transform = ''; });
    }
  }

  /* ---------- Scroll reveal ---------- */
  var rv = $$('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    rv.forEach(function (el) { io.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('is-in'); }); }

  /* ---------- Filters (floor plans + gallery) ---------- */
  $$('[data-filter-group]').forEach(function (group) {
    var target = $(group.getAttribute('data-filter-group'));
    var buttons = $$('.filter', group);
    var live = $('[data-filter-status]', group.parentNode);
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.getAttribute('data-filter');
        buttons.forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        var n = 0;
        $$('[data-cat]', target).forEach(function (item) {
          var show = f === 'all' || item.getAttribute('data-cat').split(' ').indexOf(f) > -1;
          item.hidden = !show; if (show) n++;
        });
        if (live) live.textContent = n + (n === 1 ? ' result' : ' results') + ' shown';
      });
    });
  });

  /* ---------- Lightbox ---------- */
  var lb = $('.lightbox');
  if (lb) {
    var lbImg = $('img', lb), lbCap = $('.lightbox__cap', lb), items = [], cur = 0, lastFocus;
    function visible() { return $$('.masonry figure').filter(function (f) { return !f.hidden; }); }
    function show(n) {
      items = visible(); cur = (n + items.length) % items.length;
      var b = $('button', items[cur]);
      lbImg.src = b.getAttribute('data-full'); lbImg.alt = $('img', b).alt; lbCap.textContent = $('img', b).alt + '  ·  ' + (cur + 1) + ' / ' + items.length;
    }
    function open(n) { lastFocus = d.activeElement; lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); d.body.style.overflow = 'hidden'; show(n); $('.lb-close', lb).focus(); }
    function close() { lb.classList.remove('is-open'); lb.setAttribute('aria-hidden', 'true'); d.body.style.overflow = ''; lastFocus && lastFocus.focus(); }
    $$('.masonry button').forEach(function (b) {
      b.addEventListener('click', function () { open(visible().indexOf(b.parentNode)); });
    });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', function () { show(cur - 1); });
    $('.lb-next', lb).addEventListener('click', function () { show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    d.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(cur - 1);
      if (e.key === 'ArrowRight') show(cur + 1);
      if (e.key === 'Tab') { var f = $$('.lb-btn', lb); var idx = f.indexOf(d.activeElement); e.preventDefault(); f[(idx + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus(); }
    });
  }

  /* ---------- Virtual tour tabs ---------- */
  $$('[data-tour]').forEach(function (b) {
    b.addEventListener('click', function () {
      $$('[data-tour]').forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      var img = $('.tour-frame img'); if (img) { img.src = b.getAttribute('data-img'); img.srcset = ''; img.alt = b.getAttribute('data-alt'); }
      var lbl = $('[data-tour-label]'); if (lbl) lbl.textContent = b.textContent.trim() + ' — 3D tour coming soon';
    });
  });

  /* ---------- Tour date picker rules ---------- */
  var date = $('#tour-date');
  if (date) {
    var t = new Date(); t.setDate(t.getDate() + 1);
    if (t.getDay() === 0) t.setDate(t.getDate() + 1);
    date.min = t.toISOString().slice(0, 10);
    var m = new Date(); m.setDate(m.getDate() + 60); date.max = m.toISOString().slice(0, 10);
  }

  /* ---------- Forms (front-end only) ---------- */
  $$('form[data-demo-form]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, first = null;
      $$('[required]', form).forEach(function (el) {
        var field = el.closest('.field'), bad = !el.value.trim() || (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value));
        if (el.id === 'tour-date' && el.value) { var day = new Date(el.value + 'T12:00:00').getDay(); if (day === 0) bad = true; }
        if (field) field.classList.toggle('has-error', bad);
        el.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad) { ok = false; first = first || el; }
      });
      if (!ok) { first.focus(); return; }

      /* ==========================================================
         LEASING CRM / EMAIL HOOK
         Connect this form to the property's lead system here, e.g.
         POST new FormData(form) to the CRM endpoint (Entrata, RealPage,
         Yardi RentCafe, Knock, Funnel) or a form/email service.
         Example:
           fetch('https://YOUR-CRM-ENDPOINT', { method: 'POST', body: new FormData(form) })
         ========================================================== */

      var data = new FormData(form), name = (data.get('first_name') || data.get('name') || '').toString().split(' ')[0];
      var success = form.parentNode.querySelector('.form-success');
      var nameSlot = success && success.querySelector('[data-name]');
      if (nameSlot) nameSlot.textContent = name ? ', ' + name : '';
      var when = success && success.querySelector('[data-when]');
      if (when && data.get('tour_date')) {
        var dt = new Date(data.get('tour_date') + 'T12:00:00');
        when.textContent = ' for ' + dt.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' }) + (data.get('tour_time') ? ' at ' + data.get('tour_time') : '');
      }
      form.classList.add('is-done');
      if (success) { success.classList.add('is-visible'); success.setAttribute('tabindex', '-1'); success.focus(); }
    });
    $$('input,select,textarea', form).forEach(function (el) {
      el.addEventListener('input', function () { var f = el.closest('.field'); if (f) f.classList.remove('has-error'); });
    });
  });

  /* Floor plan "Check Availability" -> prefill contact page */
  var params = new URLSearchParams(location.search), plan = params.get('plan');
  if (plan) { var sel = $('#tour-plan'); if (sel) { $$('option', sel).forEach(function (o) { if (o.value === plan) sel.value = plan; }); } }

  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
