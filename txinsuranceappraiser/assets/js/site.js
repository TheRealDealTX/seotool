/* TX Insurance Appraiser — site interactions (no dependencies) */
(function () {
  'use strict';
  var d = document, w = window;
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* sticky header shadow + back-to-top + reading progress */
  var header = d.querySelector('.site-header'), toTop = d.querySelector('.to-top'), prog = d.querySelector('.progress');
  var article = d.querySelector('.prose');
  function onScroll() {
    var y = w.scrollY;
    if (header) header.classList.toggle('scrolled', y > 30);
    if (toTop) toTop.classList.toggle('show', y > 700);
    if (prog && article) {
      var r = article.getBoundingClientRect(), total = r.height - w.innerHeight;
      prog.style.width = Math.max(0, Math.min(100, (-r.top / total) * 100)) + '%';
    }
  }
  w.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (toTop) toTop.addEventListener('click', function () { w.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* mobile nav: full-screen panel with explicit close button */
  var burger = d.querySelector('.burger'), mnav = d.getElementById('mnav');
  function closeNav() { if (!mnav || mnav.hidden) return; mnav.classList.remove('open'); d.body.classList.remove('nav-open'); burger.setAttribute('aria-expanded', 'false'); setTimeout(function () { mnav.hidden = true; }, 250); burger.focus(); }
  function openNav() { mnav.hidden = false; requestAnimationFrame(function () { mnav.classList.add('open'); }); d.body.classList.add('nav-open'); burger.setAttribute('aria-expanded', 'true'); var c = mnav.querySelector('.mnav-close'); if (c) c.focus(); }
  if (burger && mnav) {
    burger.addEventListener('click', function () { mnav.hidden ? openNav() : closeNav(); });
    mnav.querySelector('.mnav-close').addEventListener('click', closeNav);
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });
    mnav.querySelectorAll('.mnav-toggle').forEach(function (t) {
      t.addEventListener('click', function () {
        var s = d.getElementById(t.getAttribute('aria-controls')), open = t.getAttribute('aria-expanded') !== 'true';
        t.setAttribute('aria-expanded', open ? 'true' : 'false'); s.hidden = !open; t.parentNode.parentNode.classList.toggle('expanded', open);
      });
    });
    mnav.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(function (a) { a.addEventListener('click', closeNav); });
    w.addEventListener('resize', function () { if (w.innerWidth > 980) closeNav(); });
  }

  /* scroll reveal */
  var els = d.querySelectorAll('.reveal, .reveal-l, .reveal-r');
  if ('IntersectionObserver' in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  /* animated counters */
  var counters = d.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in w) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseFloat(el.getAttribute('data-count')), t0 = null, dur = reduce ? 1 : 1600;
        function step(ts) {
          if (!t0) t0 = ts;
          var p = Math.min(1, (ts - t0) / dur), v = Math.round(end * (1 - Math.pow(1 - p, 3)));
          el.textContent = v.toLocaleString();
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step); co.unobserve(el);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { co.observe(c); });
  }

  /* hero parallax */
  var hb = d.querySelector('.hero-bg');
  if (hb && !reduce) {
    w.addEventListener('scroll', function () {
      var y = w.scrollY; if (y < 900) hb.style.transform = 'scale(1.08) translateY(' + (y * 0.25) + 'px)';
    }, { passive: true });
  }

  /* 3D tilt on cards (pointer devices only) */
  if (!reduce && w.matchMedia('(hover: hover)').matches) {
    d.querySelectorAll('.tilt').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = 'perspective(900px) rotateX(' + (-y * 6) + 'deg) rotateY(' + (x * 8) + 'deg) translateY(-6px)';
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
  }

  /* typed rotating word in hero */
  var typed = d.querySelector('[data-words]');
  if (typed && !reduce) {
    var words = typed.getAttribute('data-words').split('|'), wi = 0, ci = words[0].length, del = true;
    setTimeout(function tick() {
      var word = words[wi];
      if (del) { ci--; if (ci <= 0) { del = false; wi = (wi + 1) % words.length; } }
      else { ci++; if (ci >= words[wi].length) { del = true; typed.textContent = words[wi]; return setTimeout(tick, 2200); } }
      typed.textContent = words[wi].slice(0, ci) || ' ';
      setTimeout(tick, del ? 45 : 85);
    }, 2600);
  }

  /* table of contents for posts */
  var toc = d.querySelector('[data-toc]');
  if (toc && article) {
    var hs = article.querySelectorAll('h2[id]'), html = '';
    hs.forEach(function (h) { html += '<li><a href="#' + h.id + '">' + h.textContent + '</a></li>'; });
    toc.innerHTML = html;
    if (!hs.length) toc.closest('.toc').style.display = 'none';
    var links = toc.querySelectorAll('a');
    if ('IntersectionObserver' in w) {
      var to = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) links.forEach(function (l) { l.classList.toggle('on', l.getAttribute('href') === '#' + en.target.id); });
        });
      }, { rootMargin: '-20% 0px -70% 0px' });
      hs.forEach(function (h) { to.observe(h); });
    }
  }

  /* copy link */
  d.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(function () { b.textContent = 'Link copied ✓'; });
    });
  });

  /* blog filter + search */
  var grid = d.querySelector('[data-posts]');
  if (grid) {
    var cards = grid.querySelectorAll('.post-card'), cat = 'all', q = '';
    function apply() {
      cards.forEach(function (c) {
        var ok = (cat === 'all' || c.getAttribute('data-cat') === cat) && (!q || c.textContent.toLowerCase().indexOf(q) > -1);
        c.classList.toggle('hide', !ok);
      });
    }
    d.querySelectorAll('.filters button').forEach(function (b) {
      b.addEventListener('click', function () {
        d.querySelectorAll('.filters button').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on'); cat = b.getAttribute('data-cat'); apply();
      });
    });
    var s = d.querySelector('[data-search]');
    if (s) s.addEventListener('input', function () { q = s.value.trim().toLowerCase(); apply(); });
  }

  /* city finder on /areas/ */
  var cf = d.querySelector('[data-cityfilter]');
  if (cf) {
    cf.addEventListener('input', function () {
      var v = cf.value.trim().toLowerCase();
      d.querySelectorAll('.city-grid li').forEach(function (li) { li.style.display = !v || li.textContent.toLowerCase().indexOf(v) > -1 ? '' : 'none'; });
      d.querySelectorAll('.region').forEach(function (r) {
        var any = Array.prototype.some.call(r.querySelectorAll('.city-grid li'), function (li) { return li.style.display !== 'none'; });
        r.style.display = any ? '' : 'none';
      });
    });
  }

  /* popup lead form: opens from [data-popup] links, after 35s, or on exit intent (once per session) */
  var modal = d.getElementById('lead-modal');
  if (modal) {
    var lastFocus = null, KEY = 'txia-popup-seen';
    var seen = function () { try { return sessionStorage.getItem(KEY); } catch (e) { return null; } };
    var mark = function () { try { sessionStorage.setItem(KEY, '1'); } catch (e) {} };
    var openModal = function () {
      if (!modal.hidden) return;
      lastFocus = d.activeElement; modal.hidden = false; d.body.classList.add('modal-open'); mark();
      if (typeof closeNav === 'function') closeNav();
      var f = modal.querySelector('input:not([type=hidden]):not([name=website])'); if (f) setTimeout(function () { f.focus(); }, 50);
    };
    var closeModal = function () { modal.hidden = true; d.body.classList.remove('modal-open'); if (lastFocus) lastFocus.focus(); };
    d.querySelectorAll('[data-popup]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); openModal(); }); });
    modal.querySelector('.modal-x').addEventListener('click', closeModal);
    var onContact = /^\/(contact-us|thank-you)\//.test(location.pathname);
    if (!onContact && !seen()) {
      setTimeout(function () { if (!seen()) openModal(); }, 35000);
      d.addEventListener('mouseout', function (e) { if (!e.relatedTarget && e.clientY < 10 && !seen()) openModal(); });
    }
  }

  /* AJAX lead forms (falls back to normal POST without JS) */
  d.querySelectorAll('form[data-ajax]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      if (!w.fetch || !w.FormData) return;
      e.preventDefault();
      var msg = f.querySelector('.form-msg'), btn = f.querySelector('[type=submit]');
      btn.disabled = true; msg.className = 'form-msg'; msg.textContent = 'Sending…';
      fetch(f.action, { method: 'POST', body: new FormData(f), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          msg.className = 'form-msg ' + (j.ok ? 'ok' : 'err'); msg.textContent = j.message;
          if (j.ok) { f.reset(); if (w.dataLayer) w.dataLayer.push({ event: 'lead_submit' }); }
        })
        .catch(function () { msg.className = 'form-msg err'; msg.textContent = 'Something went wrong. Please call (254) 421-5412.'; })
        .finally(function () { btn.disabled = false; });
    });
  });
})();
