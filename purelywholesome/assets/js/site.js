/* Purely Wholesome Farm - site behaviour: header, menus, search, scroll effects, filters. */
(function () {
  'use strict';
  const doc = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  doc.classList.add('js');

  // ---------- Header ----------
  const header = document.querySelector('[data-header]');
  const bar = document.querySelector('.progress span');
  const isPost = document.body.classList.contains('is-post');
  let ticking = false;
  function onScroll() {
    const y = window.scrollY;
    header.classList.toggle('is-scrolled', y > 10);
    if (isPost && bar) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    }
    ticking = false;
  }
  window.addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
  onScroll();

  // ---------- Menus ----------
  // The mobile drawer lives outside the header: the header's backdrop-filter would
  // otherwise become the containing block for a position:fixed panel.
  const menuBtn = document.querySelector('[data-menu]');
  const drawer = document.querySelector('[data-drawer]');
  let drawerTimer = null;
  function setDrawer(open) {
    clearTimeout(drawerTimer);
    menuBtn.setAttribute('aria-expanded', open);
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('menu-open', open);
    if (open) {
      drawer.hidden = false;
      requestAnimationFrame(() => requestAnimationFrame(() => drawer.classList.add('is-open')));
    } else {
      drawer.classList.remove('is-open');
      drawerTimer = setTimeout(() => { drawer.hidden = true; }, 350);
    }
  }
  menuBtn.addEventListener('click', () => setDrawer(menuBtn.getAttribute('aria-expanded') !== 'true'));
  drawer.addEventListener('click', (e) => { if (e.target === drawer || e.target.closest('a, [data-search-open]')) setDrawer(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !drawer.hidden) setDrawer(false); });
  window.matchMedia('(min-width: 961px)').addEventListener('change', (m) => { if (m.matches) setDrawer(false); });
  const megaBtn = document.querySelector('[data-mega-toggle]');
  if (megaBtn) {
    megaBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = megaBtn.parentElement.classList.toggle('is-open');
      megaBtn.setAttribute('aria-expanded', open);
    });
    document.addEventListener('click', (e) => {
      if (!megaBtn.parentElement.contains(e.target)) { megaBtn.parentElement.classList.remove('is-open'); megaBtn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // ---------- Search overlay ----------
  const overlay = document.querySelector('[data-search-overlay]');
  const input = overlay.querySelector('[data-search-input]');
  const results = overlay.querySelector('[data-search-results]');
  const hint = results.innerHTML;
  let index = null, active = -1;
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  function openSearch(q) {
    overlay.hidden = false;
    requestAnimationFrame(() => overlay.classList.add('is-open'));
    document.body.style.overflow = 'hidden';
    if (q) input.value = q;
    input.focus();
    if (!index) fetch('/search-index.json').then((r) => r.json()).then((d) => { index = d; render(); });
    else render();
  }
  function closeSearch() {
    overlay.classList.remove('is-open');
    document.body.style.overflow = '';
    setTimeout(() => { overlay.hidden = true; }, 200);
  }
  function render() {
    const q = input.value.trim().toLowerCase();
    if (!q || !index) { results.innerHTML = hint; bindHints(); return; }
    const terms = q.split(/\s+/);
    const hits = index.map((it) => {
      const t = it.t.toLowerCase(), d = (it.d + ' ' + it.c).toLowerCase();
      let s = 0;
      for (const w of terms) { if (t.includes(w)) s += 3; else if (d.includes(w)) s += 1; else return null; }
      if (t.startsWith(q)) s += 2;
      return [s, it];
    }).filter(Boolean).sort((a, b) => b[0] - a[0]).slice(0, 8);
    active = -1;
    results.innerHTML = hits.length ? '<ul class="search__list">' + hits.map(([, it]) =>
      '<li><a href="' + it.u + '">' + (it.i ? '<img src="' + esc(it.i) + '" alt="" loading="lazy">' : '<span class="search__tool">⚙</span>') +
      '<span><small>' + esc(it.c) + '</small><strong>' + esc(it.t) + '</strong></span></a></li>').join('') + '</ul>' +
      '<a class="search__all" href="/?s=' + encodeURIComponent(q) + '">See all results for “' + esc(q) + '” →</a>'
      : '<p class="search__hint">No matches yet. Press Enter to search everything.</p>';
  }
  function bindHints() {
    results.querySelectorAll('[data-q]').forEach((b) => b.addEventListener('click', () => { input.value = b.dataset.q; render(); input.focus(); }));
  }
  bindHints();
  input.addEventListener('input', render);
  input.addEventListener('keydown', (e) => {
    const links = results.querySelectorAll('.search__list a');
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      active = (active + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
      links.forEach((l, i) => l.classList.toggle('is-active', i === active));
    } else if (e.key === 'Enter' && active >= 0 && links[active]) {
      e.preventDefault(); window.location = links[active].href;
    }
  });
  document.querySelectorAll('[data-search-open]').forEach((b) => b.addEventListener('click', () => openSearch()));
  overlay.querySelectorAll('[data-search-close]').forEach((b) => b.addEventListener('click', closeSearch));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !overlay.hidden) closeSearch();
    if (e.key === '/' && overlay.hidden && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); }
  });

  // ---------- Reveal on scroll + counters ----------
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-in'));
  }
  const counters = document.querySelectorAll('[data-count]');
  const countUp = (el) => {
    const target = parseInt(el.dataset.count, 10);
    if (reduce) { el.textContent = target; return; }
    const start = performance.now();
    const step = (now) => {
      const p = Math.min(1, (now - start) / 1400);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if ('IntersectionObserver' in window) {
    const co = new IntersectionObserver((entries) => entries.forEach((en) => { if (en.isIntersecting) { countUp(en.target); co.unobserve(en.target); } }), { threshold: 0.6 });
    counters.forEach((c) => co.observe(c));
  } else counters.forEach(countUp);

  // ---------- Hero parallax ----------
  const group = document.querySelector('[data-parallax-group]');
  if (group && !reduce && window.matchMedia('(pointer: fine)').matches) {
    const layers = group.querySelectorAll('[data-depth]');
    let mx = 0, my = 0, raf = null;
    window.addEventListener('pointermove', (e) => {
      mx = e.clientX / window.innerWidth - 0.5; my = e.clientY / window.innerHeight - 0.5;
      if (!raf) raf = requestAnimationFrame(() => {
        layers.forEach((l) => { const d = parseFloat(l.dataset.depth) * 260; l.style.translate = (-mx * d) + 'px ' + (-my * d) + 'px'; });
        raf = null;
      });
    }, { passive: true });
  }

  // ---------- Tilt cards ----------
  if (!reduce && window.matchMedia('(pointer: fine)').matches) {
    document.querySelectorAll('.tilt').forEach((card) => {
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = 'perspective(900px) rotateY(' + x * 6 + 'deg) rotateX(' + -y * 6 + 'deg) translateY(-4px)';
        card.style.setProperty('--mx', (x + 0.5) * 100 + '%'); card.style.setProperty('--my', (y + 0.5) * 100 + '%');
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }

  // ---------- Table of contents ----------
  const toc = document.querySelector('[data-toc]');
  if (toc) {
    const toggle = toc.querySelector('[data-toc-toggle]');
    toggle.addEventListener('click', () => { const o = toc.classList.toggle('is-open'); toggle.setAttribute('aria-expanded', o); });
    const links = Array.from(toc.querySelectorAll('a'));
    const map = new Map(links.map((a) => [decodeURIComponent(a.hash.slice(1)), a]));
    if ('IntersectionObserver' in window) {
      const to = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) { links.forEach((l) => l.classList.remove('is-active')); const a = map.get(en.target.id); if (a) a.classList.add('is-active'); }
        });
      }, { rootMargin: '-15% 0px -75% 0px' });
      map.forEach((_, id) => { const h = document.getElementById(id); if (h) to.observe(h); });
    }
    links.forEach((a) => a.addEventListener('click', () => { toc.classList.remove('is-open'); }));
  }
  const copyBtn = document.querySelector('[data-copy-link]');
  if (copyBtn) copyBtn.addEventListener('click', () => {
    const url = document.querySelector('link[rel=canonical]').href;
    if (navigator.share && window.matchMedia('(pointer: coarse)').matches) navigator.share({ title: document.title, url }).catch(() => {});
    else if (navigator.clipboard) navigator.clipboard.writeText(url).then(() => { copyBtn.classList.add('is-done'); setTimeout(() => copyBtn.classList.remove('is-done'), 1600); });
  });

  // ---------- Archive filters ----------
  const filters = document.querySelector('[data-filters]');
  const cards = document.querySelector('[data-cards]');
  const more = document.querySelector('[data-more]');
  if (cards) {
    let topic = 'all', text = '', expanded = false;
    const items = Array.from(cards.children);
    const empty = document.querySelector('[data-empty]');
    const apply = () => {
      const filtering = topic !== 'all' || text;
      let shown = 0;
      items.forEach((c) => {
        const match = (topic === 'all' || c.dataset.topic === topic) && (!text || c.dataset.search.includes(text));
        const hidden = !match || (!filtering && !expanded && c.classList.contains('is-more'));
        c.hidden = hidden;
        if (!hidden) { shown++; c.classList.add('is-in'); }
      });
      if (empty) empty.hidden = shown > 0;
      if (more) more.parentElement.hidden = filtering || expanded;
    };
    if (filters) {
      filters.querySelectorAll('[data-filter]').forEach((b) => b.addEventListener('click', () => {
        filters.querySelectorAll('[data-filter]').forEach((x) => x.classList.toggle('is-active', x === b));
        topic = b.dataset.filter; apply();
      }));
      filters.querySelector('[data-filter-search]').addEventListener('input', (e) => { text = e.target.value.trim().toLowerCase(); apply(); });
    }
    if (more) more.addEventListener('click', () => { expanded = true; apply(); });
    apply();
  }

  // ---------- Newsletter ----------
  document.querySelectorAll('[data-subscribe]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const msg = form.querySelector('.subscribe__msg');
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } })
        .then((r) => r.json()).then((d) => {
          msg.textContent = d.ok ? 'You’re on the list. Welcome to the farm!' : 'Please check your email address.';
          form.classList.toggle('is-done', d.ok);
        }).catch(() => form.submit());
    });
  });

  // Hero search: open the instant-search overlay with what was typed so far.
  const heroSearch = document.querySelector('[data-hero-search]');
  if (heroSearch) heroSearch.addEventListener('focus', () => { if (window.innerWidth > 720) { heroSearch.blur(); openSearch(heroSearch.value); } });
})();
