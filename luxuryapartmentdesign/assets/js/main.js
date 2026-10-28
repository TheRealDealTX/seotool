/* Luxury Apartment Design — site-wide behaviour */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var store = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  // Tool helpers: read a form into an object, re-run on every change,
  // and show/hide [data-show="value"] blocks for the active radio choice.
  function vals(form) {
    var o = {};
    $$('input, select', form).forEach(function (el) {
      if (!el.name) return;
      if (el.type === 'radio') { if (el.checked) o[el.name] = isNaN(el.value) ? el.value : +el.value; }
      else if (el.type === 'checkbox') o[el.name] = el.checked;
      else if (el.type === 'number') o[el.name] = parseFloat(el.value) || 0;
      else o[el.name] = el.value;
    });
    return o;
  }
  function bind(form, fn) {
    function go() {
      var v = vals(form);
      $$('[data-show]', form).forEach(function (el) {
        var keys = el.getAttribute('data-show').split(' ');
        el.hidden = !keys.some(function (k) { for (var n in v) if (v[n] === k) return true; return false; });
      });
      fn(v);
    }
    form.addEventListener('input', go);
    form.addEventListener('change', go);
    go();
  }
  function fmt(n, d) { return Number(n).toLocaleString('en-US', { maximumFractionDigits: d === undefined ? 1 : d, minimumFractionDigits: 0 }); }
  function ftin(inches) { var f = Math.floor(inches / 12), i = Math.round(inches - f * 12); if (i === 12) { f++; i = 0; } return f + "' " + i + '"'; }
  window.LAD = { $: $, $$: $$, store: store, vals: vals, bind: bind, fmt: fmt, ftin: ftin };

  // Mobile nav
  var toggle = $('.nav-toggle'), nav = $('#main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Wrap tables so they scroll on phones
  $$('.prose table').forEach(function (t) {
    if (t.parentElement.classList.contains('table-wrap')) return;
    var w = document.createElement('div');
    w.className = 'table-wrap';
    t.parentNode.insertBefore(w, t);
    w.appendChild(t);
  });

  // Reading progress, back-to-top, TOC highlight
  var bar = $('.progress span'), top = $('.to-top'), prose = $('.prose');
  var tocLinks = $$('.toc a'), heads = tocLinks.map(function (a) { return document.getElementById(a.getAttribute('href').slice(1)); });
  function onScroll() {
    var y = window.scrollY;
    if (top) top.classList.toggle('is-visible', y > 900);
    if (bar && prose && document.body.classList.contains('is-article')) {
      var r = prose.getBoundingClientRect(), total = r.height - window.innerHeight * 0.5;
      bar.style.width = Math.max(0, Math.min(100, (-r.top + 120) / total * 100)) + '%';
    }
    if (heads.length) {
      var idx = -1;
      heads.forEach(function (h, i) { if (h && h.getBoundingClientRect().top < 140) idx = i; });
      tocLinks.forEach(function (a, i) { a.classList.toggle('is-active', i === idx); });
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  // Tickable checklists, remembered per article
  var ck = $('[data-checklist-key]');
  $$('.checklist').forEach(function (list, li) {
    var key = 'lad-ck-' + (ck ? ck.getAttribute('data-checklist-key') : location.pathname) + '-' + li;
    var done = store.get(key, []);
    var items = $$('li', list);
    var prog = document.createElement('p');
    prog.className = 'checklist__progress';
    list.appendChild(prog);
    function update() { prog.textContent = $$('li.is-done', list).length + ' of ' + items.length + ' done'; }
    items.forEach(function (it, i) {
      it.setAttribute('role', 'checkbox');
      it.setAttribute('tabindex', '0');
      if (done.indexOf(i) > -1) it.classList.add('is-done');
      it.setAttribute('aria-checked', it.classList.contains('is-done'));
      function flip() {
        it.classList.toggle('is-done');
        it.setAttribute('aria-checked', it.classList.contains('is-done'));
        store.set(key, items.map(function (x, j) { return x.classList.contains('is-done') ? j : -1; }).filter(function (j) { return j > -1; }));
        update();
      }
      it.addEventListener('click', function (e) { if (e.target.tagName !== 'A') flip(); });
      it.addEventListener('keydown', function (e) { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); flip(); } });
    });
    update();
  });

  // Copy link buttons
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var txt = b.getAttribute('data-copy'), old = b.textContent;
      (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () {
        b.textContent = 'Copied!';
        setTimeout(function () { b.textContent = old; }, 1600);
      }, function () { window.prompt('Copy this link:', txt); });
    });
  });

  // AJAX newsletter
  $$('form[data-ajax]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      if (!window.fetch) return;
      e.preventDefault();
      var status = $('.form-status', f);
      status.textContent = 'Subscribing…';
      fetch(f.action, { method: 'POST', body: new FormData(f), headers: { 'X-Requested-With': 'fetch' } })
        .then(function (r) { return r.json(); })
        .then(function (d) { status.textContent = d.message; if (d.ok) f.reset(); })
        .catch(function () { status.textContent = 'Something went wrong. Please try again.'; });
    });
  });

  // Blog filter
  var fin = $('[data-filter-input]'), flist = $('[data-filter-list]');
  if (fin && flist) {
    var cat = '';
    var apply = function () {
      var q = fin.value.trim().toLowerCase(), shown = 0;
      $$('[data-cat]', flist).forEach(function (el) {
        var ok = (!cat || el.getAttribute('data-cat') === cat) && (!q || el.getAttribute('data-text').indexOf(q) > -1);
        el.hidden = !ok;
        if (ok) shown++;
      });
      $('[data-filter-empty]').hidden = shown > 0;
    };
    fin.addEventListener('input', apply);
    $$('[data-filter-cat]').forEach(function (b) {
      b.addEventListener('click', function () {
        cat = b.getAttribute('data-filter-cat');
        $$('[data-filter-cat]').forEach(function (x) { x.classList.toggle('is-active', x === b); });
        apply();
      });
    });
  }

  // Search overlay with instant results
  var ov = $('.search-overlay'), input = $('#site-search'), results = $('.search-overlay__results'), index = null;
  function openSearch() {
    ov.hidden = false;
    input.focus();
    if (!index) {
      fetch('/search-index.json').then(function (r) { return r.json(); }).then(function (d) { index = d; run(); }).catch(function () { index = []; });
    }
  }
  function closeSearch() { ov.hidden = true; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function run() {
    if (!index) return;
    var q = input.value.trim().toLowerCase();
    if (q.length < 2) { results.innerHTML = ''; return; }
    var terms = q.split(/\s+/);
    var hits = index.map(function (it) {
      var hay = (it.t + ' ' + it.k).toLowerCase(), s = 0;
      terms.forEach(function (t) { if (hay.indexOf(t) > -1) s += it.t.toLowerCase().indexOf(t) > -1 ? 3 : 1; else s -= 5; });
      return [s, it];
    }).filter(function (h) { return h[0] > 0; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 8);
    results.innerHTML = hits.length ? hits.map(function (h) {
      return '<li><a href="' + h[1].u + '"><small>' + esc(h[1].c) + '</small>' + esc(h[1].t) + '</a></li>';
    }).join('') : '<li><a href="/search/?q=' + encodeURIComponent(q) + '">Search all content for “' + esc(q) + '”</a></li>';
  }
  if (ov) {
    $$('[data-search-open]').forEach(function (b) { b.addEventListener('click', openSearch); });
    $$('[data-search-close]').forEach(function (b) { b.addEventListener('click', closeSearch); });
    ov.addEventListener('click', function (e) { if (e.target === ov) closeSearch(); });
    input.addEventListener('input', run);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !ov.hidden) closeSearch();
      if (e.key === '/' && ov.hidden && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
    });
  }
})();
