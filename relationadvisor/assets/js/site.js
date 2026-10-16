/* RelationAdvisor — site script (no dependencies) */
(function () {
  'use strict';
  var d = document, w = window;
  d.documentElement.classList.remove('no-js');
  var reduce = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function $(s, c) { return (c || d).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); }

  /* ---------- toast ---------- */
  var toastEl;
  function toast(msg) {
    if (!toastEl) { toastEl = d.createElement('div'); toastEl.className = 'toast'; toastEl.setAttribute('role', 'status'); d.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('show');
    clearTimeout(toastEl._t); toastEl._t = setTimeout(function () { toastEl.classList.remove('show'); }, 1800);
  }
  function copyText(text) {
    if (navigator.clipboard && w.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (res, rej) {
      var ta = d.createElement('textarea'); ta.value = text; ta.setAttribute('readonly', ''); ta.style.position = 'fixed'; ta.style.opacity = '0';
      d.body.appendChild(ta); ta.select();
      try { d.execCommand('copy') ? res() : rej(); } catch (e) { rej(e); } finally { d.body.removeChild(ta); }
    });
  }

  /* ---------- header & mobile nav ---------- */
  var header = $('.site-header'), nav = $('#site-nav'), toggle = $('.nav-toggle'), overlay = $('.nav-overlay');
  var mq = w.matchMedia('(max-width: 980px)');
  function setNav(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (overlay) overlay.classList.toggle('show', open);
    d.body.classList.toggle('nav-open', open);
    if (open) { var first = nav.querySelector('a, button'); if (first) first.focus(); }
  }
  if (toggle) {
    toggle.addEventListener('click', function () { setNav(toggle.getAttribute('aria-expanded') !== 'true'); });
    if (overlay) overlay.addEventListener('click', function () { setNav(false); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { setNav(false); toggle.focus(); }
      if (e.key === 'Tab' && nav.classList.contains('open') && mq.matches) {
        var f = [toggle].concat($$('a, button', nav).filter(function (el) { return el.offsetParent !== null; }));
        var i = f.indexOf(d.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
    $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { if (mq.matches) setNav(false); }); });
    var onMq = function () { if (!mq.matches) setNav(false); };
    mq.addEventListener ? mq.addEventListener('change', onMq) : mq.addListener(onMq);
  }
  $$('.has-sub > button').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var li = btn.parentNode, open = !li.classList.contains('open');
      $$('.has-sub.open').forEach(function (o) { if (o !== li) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); } });
      li.classList.toggle('open', open); btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  d.addEventListener('click', function (e) {
    if (mq.matches) return;
    $$('.has-sub.open').forEach(function (o) { if (!o.contains(e.target)) { o.classList.remove('open'); o.firstElementChild.setAttribute('aria-expanded', 'false'); } });
  });

  /* ---------- scroll effects ---------- */
  var bar = $('.progress'), toTop = $('.to-top'), article = $('.prose');
  var ticking = false;
  function onScroll() {
    var y = w.pageYOffset;
    if (header) header.classList.toggle('scrolled', y > 10);
    if (toTop) toTop.classList.toggle('show', y > 700);
    if (bar && article) {
      var r = article.getBoundingClientRect(), total = r.height - w.innerHeight;
      var p = total > 0 ? Math.min(1, Math.max(0, -r.top / total)) : 0;
      bar.style.width = (p * 100) + '%';
    }
    ticking = false;
  }
  w.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', function () { w.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* ---------- reveal on scroll ---------- */
  var revs = $$('.reveal');
  if ('IntersectionObserver' in w && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revs.forEach(function (el) { io.observe(el); });
  } else { revs.forEach(function (el) { el.classList.add('in'); }); }

  /* ---------- counters ---------- */
  var counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in w) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseInt(el.getAttribute('data-count'), 10), suffix = el.getAttribute('data-suffix') || '';
        co.unobserve(el);
        if (reduce) { el.textContent = end.toLocaleString() + suffix; return; }
        var t0 = null;
        (function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1400); k = 1 - Math.pow(1 - k, 3);
          el.textContent = Math.round(end * k).toLocaleString() + suffix; if (k < 1) requestAnimationFrame(step); })(performance.now());
      });
    }, { threshold: 0.4 });
    counters.forEach(function (c) { co.observe(c); });
  }

  /* ---------- subtle 3D tilt on cards (mouse only) ---------- */
  if (!reduce && w.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    $$('.tilt').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        el.style.transform = 'perspective(900px) rotateY(' + (x * 6) + 'deg) rotateX(' + (-y * 6) + 'deg) translateY(-6px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- hero: rotating word + floating hearts ---------- */
  var swap = $('.swap');
  if (swap && !reduce) {
    var words = (swap.getAttribute('data-words') || '').split('|'), wi = 0;
    setInterval(function () {
      wi = (wi + 1) % words.length;
      swap.style.transition = 'opacity .3s, transform .3s'; swap.style.opacity = 0; swap.style.transform = 'translateY(10px)';
      setTimeout(function () { swap.textContent = words[wi]; swap.style.opacity = 1; swap.style.transform = 'none'; }, 300);
    }, 2600);
  }
  var hearts = $('.hearts');
  if (hearts && !reduce) {
    for (var h = 0; h < 14; h++) {
      var i = d.createElement('i'); i.textContent = '♥';
      i.style.left = (Math.random() * 100) + '%'; i.style.fontSize = (10 + Math.random() * 18) + 'px';
      i.style.animationDuration = (12 + Math.random() * 14) + 's'; i.style.animationDelay = (-Math.random() * 20) + 's';
      hearts.appendChild(i);
    }
  }

  /* ---------- site search ---------- */
  var index = null;
  function loadIndex() {
    if (index) return Promise.resolve(index);
    return fetch('/assets/search.json').then(function (r) { return r.json(); }).then(function (j) { index = j; return j; });
  }
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  $$('.search-box').forEach(function (box) {
    var input = $('input', box), list = $('.search-results', box);
    if (!input || !list) return;
    input.addEventListener('focus', loadIndex, { once: true });
    input.addEventListener('input', function () {
      var q = input.value.trim().toLowerCase();
      if (q.length < 2) { list.classList.remove('show'); list.innerHTML = ''; return; }
      loadIndex().then(function (idx) {
        var terms = q.split(/\s+/);
        var hits = idx.filter(function (p) { var hay = (p.t + ' ' + p.k + ' ' + p.c).toLowerCase(); return terms.every(function (t) { return hay.indexOf(t) > -1; }); }).slice(0, 8);
        list.innerHTML = hits.length ? hits.map(function (p) { return '<li><a href="' + p.u + '">' + esc(p.t) + '<small>' + esc(p.c) + '</small></a></li>'; }).join('')
          : '<li class="empty">No matches yet — try “first date”, “breakup” or “pickup lines”.</li>';
        list.classList.add('show');
      });
    });
    input.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { var a = $('a', list); if (a) { e.preventDefault(); a.focus(); } }
      if (e.key === 'Escape') { list.classList.remove('show'); }
    });
    list.addEventListener('keydown', function (e) {
      var links = $$('a', list), i = links.indexOf(d.activeElement);
      if (e.key === 'ArrowDown' && i < links.length - 1) { e.preventDefault(); links[i + 1].focus(); }
      if (e.key === 'ArrowUp') { e.preventDefault(); i > 0 ? links[i - 1].focus() : input.focus(); }
      if (e.key === 'Escape') { list.classList.remove('show'); input.focus(); }
    });
    d.addEventListener('click', function (e) { if (!box.contains(e.target)) list.classList.remove('show'); });
  });

  /* ---------- tabs ---------- */
  $$('[role="tablist"]').forEach(function (tl) {
    var tabs = $$('[role="tab"]', tl);
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab, panel = d.getElementById(t.getAttribute('aria-controls'));
        t.setAttribute('aria-selected', on ? 'true' : 'false'); t.tabIndex = on ? 0 : -1;
        if (panel) { panel.hidden = !on; if (on) { panel.classList.remove('fade-in'); void panel.offsetWidth; panel.classList.add('fade-in'); } }
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var n = e.key === 'ArrowRight' ? i + 1 : e.key === 'ArrowLeft' ? i - 1 : null;
        if (n === null) return; e.preventDefault(); n = (n + tabs.length) % tabs.length; tabs[n].focus(); select(tabs[n]);
      });
    });
  });

  /* ---------- line of the day ---------- */
  var lotd = $('.lotd-card');
  if (lotd) {
    var data = JSON.parse($('#lotd-data').textContent), q = $('blockquote', lotd), src = $('.src', lotd), k = new Date().getDate() % data.length;
    function show(n) {
      k = (n + data.length) % data.length; q.classList.add('out');
      setTimeout(function () { q.textContent = data[k].l; src.textContent = 'From: ' + data[k].t; src.href = data[k].u; q.classList.remove('out'); }, 250);
    }
    show(k);
    $('[data-next]', lotd).addEventListener('click', function () { show(k + 1); });
    $('[data-copy]', lotd).addEventListener('click', function () { copyText(data[k].l).then(function () { toast('Copied to clipboard ♥'); }); });
  }

  /* ---------- copy buttons on lines & notes ---------- */
  var copyIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
  $$('.prose ol.lines > li, .prose .note-card').forEach(function (el) {
    var b = d.createElement('button'); b.type = 'button'; b.className = 'copy-btn'; b.setAttribute('aria-label', 'Copy this text'); b.innerHTML = copyIcon;
    b.addEventListener('click', function () {
      var text = el.innerText.trim();
      copyText(text).then(function () { b.classList.add('done'); toast('Copied to clipboard ♥'); setTimeout(function () { b.classList.remove('done'); }, 1500); });
    });
    el.appendChild(b);
  });
  $$('[data-share-copy]').forEach(function (b) {
    b.addEventListener('click', function () { copyText(location.href).then(function () { toast('Link copied'); }); });
  });

  /* ---------- table of contents highlight ---------- */
  var tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in w) {
    var map = {};
    tocLinks.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var heads = Object.keys(map).map(function (id) { return d.getElementById(id); }).filter(Boolean);
    var to = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { tocLinks.forEach(function (a) { a.classList.remove('active'); }); var a = map[en.target.id]; if (a) a.classList.add('active'); }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    heads.forEach(function (h) { to.observe(h); });
  }

  /* ---------- article list filters ---------- */
  var fl = $('.filters');
  if (fl) {
    var cards = $$('[data-cat]'), chips = $$('.chip[data-filter]', fl), fi = $('input', fl), none = $('.no-results'), cur = 'all';
    var params = new URLSearchParams(location.search);
    if (params.get('topic')) cur = params.get('topic');
    function apply() {
      var q = fi ? fi.value.trim().toLowerCase() : '', shown = 0;
      cards.forEach(function (c) {
        var ok = (cur === 'all' || c.getAttribute('data-cat') === cur) && (!q || c.textContent.toLowerCase().indexOf(q) > -1);
        c.style.display = ok ? '' : 'none'; if (ok) shown++;
      });
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-filter') === cur ? 'true' : 'false'); });
      if (none) none.style.display = shown ? 'none' : 'block';
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { cur = c.getAttribute('data-filter'); apply(); }); });
    if (fi) fi.addEventListener('input', apply);
    apply();
  }

  /* ---------- contact form ---------- */
  var form = $('#contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = $('.alert', form.parentNode), btn = $('button[type="submit"]', form);
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (j) {
          msg.className = 'alert ' + (j.ok ? 'ok' : 'err');
          msg.textContent = j.ok ? 'Thank you! Your message is on its way — we reply within 2 business days.' : (j.error || 'Something went wrong. Please email info@relationadvisor.com directly.');
          if (j.ok) form.reset();
        })
        .catch(function () { msg.className = 'alert err'; msg.textContent = 'Network error. Please email info@relationadvisor.com directly.'; })
        .then(function () { btn.disabled = false; btn.textContent = 'Send message'; });
    });
  }
})();
