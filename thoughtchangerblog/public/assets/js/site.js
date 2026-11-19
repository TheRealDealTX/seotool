/* Thought Changer — progressive enhancement only. The site works fully without this file. */
(function () {
  'use strict';
  var doc = document.documentElement, body = document.body;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && body.classList.contains('nav-open')) { body.classList.remove('nav-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
    });
  }

  /* Scroll-driven: header state, reading progress, parallax, back-to-top */
  var bar = document.querySelector('.progress span');
  var toTop = document.querySelector('.to-top');
  var prose = document.querySelector('.prose');
  var parallax = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll('.hero-bg, .cta-bg'));
  var ticking = false;
  function onScroll() {
    var y = window.scrollY || doc.scrollTop;
    body.classList.toggle('scrolled', y > 30);
    if (toTop) toTop.classList.toggle('show', y > 900);
    if (bar) {
      var p;
      if (prose) {
        var r = prose.getBoundingClientRect();
        p = Math.min(1, Math.max(0, (-r.top + window.innerHeight * 0.3) / r.height));
      } else {
        p = y / Math.max(1, doc.scrollHeight - window.innerHeight);
      }
      bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
    }
    for (var i = 0; i < parallax.length; i++) {
      var el = parallax[i], box = el.parentNode.getBoundingClientRect();
      if (box.bottom > 0 && box.top < window.innerHeight) el.style.setProperty('--parallax', (box.top * -0.12).toFixed(1) + 'px');
    }
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* Reveal on scroll, staggered within each group */
  var reveals = document.querySelectorAll('.reveal');
  // Crawlers/renderers use very tall viewports: show everything at once there.
  var tall = window.innerHeight > 1800 || /bot|crawl|spider|lighthouse/i.test(navigator.userAgent);
  if ('IntersectionObserver' in window && !reduce && !tall) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, sibs = el.parentNode ? el.parentNode.querySelectorAll(':scope > .reveal') : [];
        var idx = Array.prototype.indexOf.call(sibs, el);
        el.style.setProperty('--d', (Math.max(0, idx) % 4) * 0.08 + 's');
        el.classList.add('in');
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  window.addEventListener('beforeprint', function () { reveals.forEach(function (el) { el.classList.add('in'); }); });

  /* Table of contents: highlight the section being read */
  var tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { map[decodeURIComponent(a.hash.slice(1))] = a; });
    var current;
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          if (current) current.classList.remove('active');
          current = map[en.target.id];
          if (current) current.classList.add('active');
        }
      });
    }, { rootMargin: '-100px 0px -65% 0px' });
    Object.keys(map).forEach(function (id) { var h = document.getElementById(id); if (h) tio.observe(h); });
  }

  /* Back to top (the header is sticky, so a plain #top jump would not move) */
  if (toTop) toTop.addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    var first = document.querySelector('.brand'); if (first) first.focus({ preventScroll: true });
  });

  /* Mobile search toggle */
  var sToggle = document.querySelector('.search-toggle');
  if (sToggle) sToggle.addEventListener('click', function () {
    var open = body.classList.toggle('search-open');
    sToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    body.classList.remove('nav-open');
    if (open) { var i = document.getElementById('hs'); if (i) i.focus(); }
  });

  /* Live search suggestions */
  var index = null, loading = null;
  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (!loading) loading = fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (d) {
      index = d.map(function (p) { p._t = p.t.toLowerCase(); p._o = (p.d + ' ' + p.c + ' ' + p.h).toLowerCase(); return p; });
      return index;
    });
    return loading;
  }
  function esc(s) { return s.replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function terms(q) { return q.toLowerCase().split(/[^\p{L}\p{N}']+/u).filter(function (t) { return t.length > 1; }); }
  function search(q) {
    var ts = terms(q), phrase = q.toLowerCase().trim();
    if (!ts.length) return [];
    var out = [];
    index.forEach(function (p, i) {
      var score = 0;
      for (var k = 0; k < ts.length; k++) {
        var t = ts[k], s = 0, at = p._t.indexOf(t);
        if (at > -1) s += (at === 0 || /[^a-z0-9]/.test(p._t.charAt(at - 1))) ? 10 : 6;
        if (p._o.indexOf(t) > -1) s += 2;
        if (!s) return;
        score += s;
      }
      if (ts.length > 1 && p._t.indexOf(phrase) > -1) score += 15;
      score += p.f ? 1.5 : 0;
      out.push({ p: p, s: score, i: i });
    });
    return out.sort(function (a, b) { return b.s - a.s || a.i - b.i; }).map(function (x) { return x.p; });
  }
  function highlight(text, ts) {
    var h = esc(text);
    ts.forEach(function (t) { h = h.replace(new RegExp('(' + esc(t).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig'), '<mark>$1</mark>'); });
    return h;
  }
  document.querySelectorAll('form.js-suggest').forEach(function (form) {
    var input = form.querySelector('input[type=search]'), box = form.querySelector('.suggest'), active = -1, timer;
    if (!input || !box) return;
    function items() { return box.querySelectorAll('a'); }
    function close() { box.hidden = true; input.setAttribute('aria-expanded', 'false'); active = -1; }
    function setActive(n) {
      var els = items(); if (!els.length) return;
      active = (n + els.length) % els.length;
      els.forEach(function (el, i) { el.classList.toggle('active', i === active); el.setAttribute('aria-selected', i === active ? 'true' : 'false'); });
      els[active].scrollIntoView({ block: 'nearest' });
    }
    function render() {
      var q = input.value.trim();
      if (q.length < 2) { close(); return; }
      loadIndex().then(function () {
        if (input.value.trim() !== q) return;
        var res = search(q), ts = terms(q), html = '';
        var allUrl = '/?s=' + encodeURIComponent(q);
        if (!res.length) {
          html = '<div class="sg-empty">No articles match “' + esc(q) + '”. Press Enter to search the full text.</div>';
        } else {
          html = '<div class="suggest-head"><span>Articles</span><span>' + res.length + ' match' + (res.length === 1 ? '' : 'es') + '</span></div>';
          res.slice(0, 6).forEach(function (p) {
            html += '<a class="sg" role="option" href="' + p.u + '"><img src="' + p.i + '" alt="" loading="lazy" width="64" height="43"><span><small>' + esc(p.c) + '</small><strong>' + highlight(p.t, ts) + '</strong></span></a>';
          });
        }
        html += '<a class="sg-all" role="option" href="' + allUrl + '">' + (res.length > 6 ? 'See all ' + res.length + ' results' : 'Search all articles') + ' for “' + esc(q) + '” →</a>';
        box.innerHTML = html; box.hidden = false; input.setAttribute('aria-expanded', 'true'); active = -1;
      });
    }
    input.addEventListener('focus', function () { loadIndex(); if (input.value.trim().length > 1) render(); });
    input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(render, 90); });
    input.addEventListener('keydown', function (e) {
      if (box.hidden) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
      else if (e.key === 'Escape') { close(); }
      else if (e.key === 'Enter' && active > -1) { e.preventDefault(); window.location.href = items()[active].href; }
    });
    document.addEventListener('click', function (e) { if (!form.contains(e.target)) close(); });
    form.addEventListener('submit', function (e) { if (!input.value.trim()) { e.preventDefault(); input.focus(); } });
  });

  /* Copy link */
  var copy = document.querySelector('.copy-link');
  if (copy && navigator.clipboard) {
    copy.addEventListener('click', function () {
      navigator.clipboard.writeText(copy.getAttribute('data-url')).then(function () {
        var t = copy.textContent; copy.textContent = 'Copied!'; setTimeout(function () { copy.textContent = t; }, 1800);
      });
    });
  }

  /* Amazon click tracking (GA4) */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-amz]');
    if (a && window.gtag) window.gtag('event', 'affiliate_click', { item_name: a.getAttribute('data-amz'), link_url: a.href });
  });

  /* Forms: submit in place, fall back to a normal POST without JS */
  document.querySelectorAll('form.js-ajax').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      if (!window.fetch || !window.FormData) return;
      e.preventDefault();
      var status = form.querySelector('.form-status');
      form.classList.add('is-sending');
      if (status) { status.classList.remove('is-error'); status.textContent = 'Sending…'; }
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (status) { status.textContent = res.message; status.classList.toggle('is-error', !res.ok); }
          if (res.ok) {
            form.querySelectorAll('input:not([type=hidden]), textarea').forEach(function (i) { i.value = ''; });
            if (window.gtag) window.gtag('event', form.querySelector('[name=form]').value === 'contact' ? 'contact_submit' : 'newsletter_signup');
          }
        })
        .catch(function () {
          if (status) { status.textContent = 'Something went wrong. Please email info@thoughtchangerblog.com.'; status.classList.add('is-error'); }
        })
        .then(function () { form.classList.remove('is-sending'); });
    });
  });
})();
