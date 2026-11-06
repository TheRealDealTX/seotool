/* Studio at 1660 Richmond: concept site interactions (no dependencies) */
(function () {
  'use strict';
  var d = document, root = d.documentElement;
  root.classList.add('js');

  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- Toast ---------- */
  var toastEl, toastT;
  function toast(msg) {
    if (!toastEl) { toastEl = d.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); toastEl.setAttribute('aria-live', 'polite'); d.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('is-visible');
    clearTimeout(toastT); toastT = setTimeout(function () { toastEl.classList.remove('is-visible'); }, 4200);
  }

  /* Placeholder links (resident portal, application, social): paid add-ons in the live build */
  $$('[data-placeholder]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      toast(a.getAttribute('data-placeholder') || 'Demo link: this will connect to the live property portal.');
    });
  });

  /* ---------- Announcement banner ---------- */
  var ann = $('.announce');
  if (ann) {
    if (store('s1660-announce') === 'closed') ann.hidden = true;
    var x = $('.announce__close', ann);
    x && x.addEventListener('click', function () { ann.hidden = true; store('s1660-announce', 'closed'); });
  }

  /* ---------- Sticky header ---------- */
  var header = $('.header');
  function onScroll() { header && header.classList.toggle('is-scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- Mobile menu ----------
     The panel is position:fixed. The header never gets transform/filter/backdrop-filter,
     so the panel is laid out against the viewport, not trapped inside the header. */
  var btn = $('.menu-btn'), nav = $('#site-nav');
  function setMenu(open) {
    if (open && header) {
      /* show the header instantly so we measure its final position, not a mid-slide one */
      var tr = header.style.transition;
      header.style.transition = 'none';
      header.classList.remove('is-hidden');
      var bottom = header.getBoundingClientRect().bottom;
      header.offsetHeight; header.style.transition = tr;
      nav.style.setProperty('--nav-top', Math.max(0, Math.round(bottom)) + 'px');
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
    window.addEventListener('resize', function () { if (window.innerWidth > 1140) setMenu(false); });
  }

  /* ---------- Hero slideshow ---------- */
  var hero = $('.hero');
  if (hero) {
    var slides = $$('.hero__slide', hero), msgs = $$('.hero__msg', hero), dots = $$('.hero__dot', hero), pause = $('.hero__pause', hero), count = $('.hero__count', hero);
    var i = 0, timer, paused = reduce;
    function go(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('is-active', k === i); });
      msgs.forEach(function (m, k) { m.classList.toggle('is-active', k === i); m.setAttribute('aria-hidden', k === i ? 'false' : 'true'); });
      dots.forEach(function (b, k) { b.classList.toggle('is-active', k === i); b.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      if (count) count.textContent = '0' + (i + 1) + ' / 0' + slides.length;
      var img = slides[i].querySelector('img[data-src]');
      if (img) { img.srcset = img.getAttribute('data-srcset'); img.src = img.getAttribute('data-src'); img.removeAttribute('data-src'); }
      schedule();
    }
    function schedule() { clearTimeout(timer); if (!paused) timer = setTimeout(function () { go(i + 1); }, 7000); }
    dots.forEach(function (b, k) { b.addEventListener('click', function () { go(k); }); });
    function setPaused(p) {
      paused = p; hero.classList.toggle('is-paused', p);
      if (pause) { pause.setAttribute('aria-label', p ? 'Play slideshow' : 'Pause slideshow'); pause.innerHTML = p ? '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>' : '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>'; }
      schedule();
    }
    pause && pause.addEventListener('click', function () { setPaused(!paused); });
    setPaused(paused);
    window.addEventListener('load', function () {
      setTimeout(function () { $$('img[data-src]', hero).forEach(function (img) { var p = new Image(); p.sizes = '100vw'; p.srcset = img.getAttribute('data-srcset'); p.src = img.getAttribute('data-src'); }); }, 1800);
    });
  }

  /* =========================================================
     Advanced effects (progressive enhancement, off for reduced motion)
     ========================================================= */

  /* Word-by-word headline reveal. Class is "words-reveal" (".split" is a layout class). */
  function splitWords(el) {
    if (el.getAttribute('data-words-done')) return;
    var n = 0, walker = d.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (node) {
      var parts = node.nodeValue.split(/(\s+)/), frag = d.createDocumentFragment();
      parts.forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
        var w = d.createElement('span'); w.className = 'w';
        var inner = d.createElement('span'); inner.style.setProperty('--i', n++); inner.textContent = part;
        w.appendChild(inner); frag.appendChild(w);
      });
      node.parentNode.replaceChild(frag, node);
    });
    el.setAttribute('data-words-done', '1');
  }
  if (!reduce) {
    $$('.hero__title').forEach(splitWords);
    $$('.section h2:not(.sr-only), .page-hero h1, .section h1, .cta h2').forEach(function (h) {
      if (h.closest('.form-card') || h.closest('.portal') || h.closest('.tile')) return;
      splitWords(h); h.classList.add('words-reveal', 'reveal');
    });
    /* clip-path hides an element from IntersectionObserver, so observe its parent instead */
    var clips = $$('.split__media > .frame, .page-hero__img');
    clips.forEach(function (a) { a.classList.add('clip-reveal'); });
    if ('IntersectionObserver' in window) {
      var clipIO = new IntersectionObserver(function (ents) {
        ents.forEach(function (en) {
          if (!en.isIntersecting) return;
          Array.prototype.forEach.call(en.target.children, function (c) { if (c.classList.contains('clip-reveal')) c.classList.add('is-in'); });
          clipIO.unobserve(en.target);
        });
      }, { threshold: 0.12 });
      var parents = [];
      clips.forEach(function (a) { if (parents.indexOf(a.parentNode) < 0) { parents.push(a.parentNode); clipIO.observe(a.parentNode); } });
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
      if (y < 160 || (dir < 0 && dirStart - y > 40)) header.classList.remove('is-hidden');
      else if (dir > 0 && y - dirStart > 60 && y > 360) header.classList.add('is-hidden');
    }
    lastY = y; ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onFrame); } }, { passive: true });
  d.addEventListener('focusin', function (e) { if (header && header.contains(e.target)) header.classList.remove('is-hidden'); });

  /* Animated counters */
  function countUp(el) {
    var raw = el.getAttribute('data-count'), target = parseFloat(raw), dec = (raw.split('.')[1] || '').length;
    var suffix = el.getAttribute('data-suffix') || '', start = null, dur = 1600, grp = el.getAttribute('data-nogroup') === null;
    function step(ts) {
      if (!start) start = ts;
      var t = Math.min(1, (ts - start) / dur), e = 1 - Math.pow(1 - t, 3), v = (target * e).toFixed(dec);
      el.textContent = (grp ? v.replace(/\B(?=(\d{3})+(?!\d))/g, ',') : v) + suffix;
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

  /* Cursor spotlight + 3D tilt, magnetic buttons, hero drift (fine pointers only) */
  if (finePointer && !reduce) {
    $$('.tile, .card, .portal, .amenity-list li, .commute div, .steps li, .plan-feature').forEach(function (card) {
      card.classList.add('fx-card');
      var tilt = card.matches('.tile, .portal, .why .card');
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.style.setProperty('--mx', (px * 100).toFixed(1) + '%'); card.style.setProperty('--my', (py * 100).toFixed(1) + '%');
        if (tilt) { card.classList.add('is-tilting'); card.style.transform = 'perspective(900px) rotateX(' + ((0.5 - py) * 6).toFixed(2) + 'deg) rotateY(' + ((px - 0.5) * 8).toFixed(2) + 'deg) translateY(-6px)'; }
      });
      card.addEventListener('pointerleave', function () { card.classList.remove('is-tilting'); card.style.transform = ''; });
    });
    $$('.btn, .badge-spin').forEach(function (b) {
      b.classList.add('magnetic');
      var k = b.classList.contains('badge-spin') ? 0.25 : 0.2;
      b.addEventListener('pointermove', function (e) {
        var r = b.getBoundingClientRect();
        b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * k).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * (k + 0.08)).toFixed(1) + 'px)';
      });
      b.addEventListener('pointerleave', function () { b.style.transform = ''; });
    });
    var heroInner = $('.hero__inner .wrap');
    if (hero && heroInner) {
      heroInner.style.transition = 'transform .8s cubic-bezier(.2,.75,.2,1)';
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

  /* ---------- Lazy Google Map (iframe injected near the viewport) ---------- */
  $$('[data-map]').forEach(function (box) {
    var load = function () {
      if (box.querySelector('iframe')) return;
      var f = d.createElement('iframe');
      f.src = box.getAttribute('data-map'); f.title = box.getAttribute('data-title') || 'Map';
      f.loading = 'lazy'; f.referrerPolicy = 'no-referrer-when-downgrade'; f.allowFullscreen = true;
      box.appendChild(f);
      var ph = box.querySelector('.map__load'); if (ph) ph.remove();
    };
    var b = box.querySelector('button'); b && b.addEventListener('click', load);
    if ('IntersectionObserver' in window) {
      var mio = new IntersectionObserver(function (ents) { if (ents[0].isIntersecting) { load(); mio.disconnect(); } }, { rootMargin: '300px' });
      mio.observe(box);
    }
  });

  /* ---------- Filters (gallery) ---------- */
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
        if (live) live.textContent = n + (n === 1 ? ' photo' : ' photos') + ' shown';
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
      var b = $('button', items[cur]), im = $('img', b);
      lbImg.src = b.getAttribute('data-full'); lbImg.alt = im.alt;
      lbCap.textContent = im.alt + '  ·  ' + (cur + 1) + ' / ' + items.length;
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

  /* ---------- Contact tabs (Tour / Question) ---------- */
  var tabs = $$('[role="tab"]');
  function selectTab(t, focus) {
    tabs.forEach(function (o) {
      var on = o === t; o.setAttribute('aria-selected', on ? 'true' : 'false'); o.tabIndex = on ? 0 : -1;
      var p = d.getElementById(o.getAttribute('aria-controls')); if (p) p.hidden = !on;
    });
    if (focus) t.focus();
  }
  tabs.forEach(function (t, k) {
    t.addEventListener('click', function () { selectTab(t); });
    t.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); selectTab(tabs[(k + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length], true); }
    });
  });
  if (tabs.length && location.hash === '#question') { var qt = d.getElementById('tab-question'); qt && selectTab(qt); }

  /* ---------- Tour date picker rules (weekdays, next 60 days) ---------- */
  var date = $('#tour-date');
  function iso(dt) { return dt.getFullYear() + '-' + ('0' + (dt.getMonth() + 1)).slice(-2) + '-' + ('0' + dt.getDate()).slice(-2); }
  if (date) {
    var t = new Date(); t.setDate(t.getDate() + 1);
    while (t.getDay() === 0 || t.getDay() === 6) t.setDate(t.getDate() + 1);
    date.min = iso(t);
    var m = new Date(); m.setDate(m.getDate() + 60); date.max = iso(m);
  }

  /* ---------- Forms (front-end only) ---------- */
  $$('form[data-demo-form]').forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, first = null;
      $$('[required]', form).forEach(function (el) {
        var field = el.closest('.field'), bad;
        if (el.type === 'radio') {
          bad = !form.querySelector('input[name="' + el.name + '"]:checked');
        } else {
          bad = !el.value.trim() || (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value));
          if (el.id === 'tour-date' && el.value) {
            var day = new Date(el.value + 'T12:00:00').getDay();
            if (day === 0 || day === 6 || (el.min && el.value < el.min) || (el.max && el.value > el.max)) bad = true;
          }
        }
        if (field) field.classList.toggle('has-error', bad);
        el.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad) { ok = false; first = first || el; }
      });
      if (!ok) { first.focus(); return; }

      /* ==========================================================
         LEASING CRM / EMAIL HOOK
         Connect this form to the property's lead system here, e.g.
         POST new FormData(form) to Buildium's lead intake, a CRM
         (Knock, Funnel, Zoho, HubSpot) or a form/email service that
         forwards to leasing@fatproperty.com.
         Example:
           fetch('https://YOUR-CRM-OR-FORM-ENDPOINT', { method: 'POST', body: new FormData(form) })
         ========================================================== */

      var data = new FormData(form), name = (data.get('first_name') || data.get('name') || '').toString().trim().split(' ')[0];
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
      el.addEventListener('change', function () { var f = el.closest('.field'); if (f) f.classList.remove('has-error'); });
    });
  });

  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
