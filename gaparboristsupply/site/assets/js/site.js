/* Gap Arborist Supply — site behaviour: cart, saved, compare, search, listing filters, effects. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const money = n => '$' + Math.round(n).toLocaleString('en-US');
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const kindImg = k => '/assets/img/kinds/' + k + '.svg';
  const imgOf = x => x.i || kindImg(x.k);

  // ---- storage (browser only; wrapped so private mode never breaks the page) ----
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem('gap.' + k)) ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem('gap.' + k, JSON.stringify(v)); } catch { /* ignore */ } },
  };
  const Gap = window.Gap = {
    cart: () => store.get('cart', []),           // [{p,n,pr,k,q}]
    saved: () => store.get('saved', []),         // [{p,n,pr,k}]
    compare: () => store.get('compare', []),     // [{p,n,pr,k}]
    setCart(c) { store.set('cart', c); updateBadges(); document.dispatchEvent(new CustomEvent('gap:cart')); },
    setSaved(s) { store.set('saved', s); updateBadges(); document.dispatchEvent(new CustomEvent('gap:saved')); },
    add(item, q = 1, from) {
      const c = Gap.cart(); const hit = c.find(i => i.p === item.p);
      if (hit) hit.q = Math.min(99, hit.q + q); else c.push({ ...item, q });
      Gap.setCart(c);
      if (from) fly(from, item);
      toast(`Added <b>${esc(item.n)}</b> · <a href="/cart/">View cart</a>`);
    },
    money, esc, kindImg, imgOf, toast,
    lite: null,
    async catalog() {
      if (Gap.lite) return Gap.lite;
      try { Gap.lite = await (await fetch('/assets/data/catalog-lite.json')).json(); } catch { Gap.lite = []; }
      return Gap.lite;
    },
  };

  function updateBadges() {
    const n = Gap.cart().reduce((a, i) => a + i.q, 0), s = Gap.saved().length;
    $$('[data-cart-count]').forEach(b => { const was = b.textContent; b.textContent = n; b.hidden = !n; if (was !== String(n)) { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); } });
    $$('[data-saved-count]').forEach(b => { b.textContent = s; b.hidden = !s; });
    const savedSet = new Set(Gap.saved().map(i => i.p));
    $$('[data-save]').forEach(btn => { const host = btn.closest('[data-product]'); if (host) btn.classList.toggle('on', savedSet.has(JSON.parse(host.dataset.product).p)); });
  }

  let toastT;
  function toast(html) {
    const t = $('.toast'); if (!t) return;
    t.innerHTML = html; t.classList.add('show');
    clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('show'), 2800);
  }

  function fly(fromEl, item) {
    const target = $('.cart-btn'); if (!target || reduce) return;
    const a = fromEl.getBoundingClientRect(), b = target.getBoundingClientRect();
    const img = document.createElement('img');
    img.src = imgOf(item); img.className = 'flyer'; img.alt = '';
    img.style.left = a.left + a.width / 2 - 30 + 'px'; img.style.top = a.top + a.height / 2 - 30 + 'px';
    document.body.appendChild(img);
    const dx = b.left + b.width / 2 - (a.left + a.width / 2), dy = b.top + b.height / 2 - (a.top + a.height / 2);
    img.animate([
      { transform: 'translate(0,0) scale(1)', opacity: 1 },
      { transform: `translate(${dx * .5}px, ${dy - 120}px) scale(.8) rotate(-20deg)`, opacity: 1, offset: .5 },
      { transform: `translate(${dx}px, ${dy}px) scale(.2) rotate(-40deg)`, opacity: .4 },
    ], { duration: 750, easing: 'cubic-bezier(.4,0,.2,1)' }).onfinish = () => img.remove();
  }

  // ---- delegated clicks: add / save / qty ----
  document.addEventListener('click', e => {
    const add = e.target.closest('[data-add]');
    if (add) {
      const host = add.closest('[data-product]'); if (!host) return;
      const item = JSON.parse(host.dataset.product);
      const qi = $('[data-qty] input', host.closest('.pdp') || host);
      const q = qi && host.classList.contains('pdp') ? Math.max(1, Math.min(99, +qi.value || 1)) : 1;
      Gap.add(item, q, add);
      add.classList.add('added'); const label = add.textContent; add.textContent = 'Added ✓';
      setTimeout(() => { add.classList.remove('added'); add.textContent = label; }, 1400);
      return;
    }
    const save = e.target.closest('[data-save]');
    if (save) {
      const host = save.closest('[data-product]'); if (!host) return;
      const item = JSON.parse(host.dataset.product);
      let s = Gap.saved();
      if (s.some(i => i.p === item.p)) { s = s.filter(i => i.p !== item.p); toast('Removed from saved'); }
      else { s.push(item); toast(`Saved <b>${esc(item.n)}</b> · <a href="/cart/#saved">View saved</a>`); }
      Gap.setSaved(s);
      return;
    }
    const step = e.target.closest('[data-step]');
    if (step) { const inp = $('input', step.parentNode); inp.value = Math.max(1, Math.min(99, (+inp.value || 1) + +step.dataset.step)); }
  });

  // ---- compare ----
  function renderCompareBar() {
    const bar = $('.compare-bar'); if (!bar) return;
    const list = Gap.compare();
    bar.hidden = !list.length;
    $('.compare-items', bar).innerHTML = list.map(i => `<span><img src="${imgOf(i)}" alt="">${esc(i.n)}</span>`).join('');
    const set = new Set(list.map(i => i.p));
    $$('[data-compare]').forEach(cb => { const host = cb.closest('[data-product]'); if (host) cb.checked = set.has(JSON.parse(host.dataset.product).p); });
  }
  document.addEventListener('change', e => {
    const cb = e.target.closest('[data-compare]'); if (!cb) return;
    const item = JSON.parse(cb.closest('[data-product]').dataset.product);
    let list = Gap.compare().filter(i => i.p !== item.p);
    if (cb.checked) {
      if (list.length >= 3) { cb.checked = false; toast('Compare up to 3 items at a time'); return; }
      list.push(item);
    }
    store.set('compare', list); renderCompareBar();
  });
  document.addEventListener('click', async e => {
    if (e.target.closest('[data-compare-clear]')) { store.set('compare', []); renderCompareBar(); }
    if (e.target.closest('[data-compare-open]')) {
      const cat = await Gap.catalog(), list = Gap.compare().map(c => cat.find(x => x.p === c.p) || { p: c.p, n: c.n, pr: c.pr, k: c.k, i: c.i, s: [] });
      const keys = [...new Set(list.flatMap(x => (x.s || []).map(s => s[0])))];
      const row = (label, f) => `<tr><th>${esc(label)}</th>${list.map(x => `<td>${f(x)}</td>`).join('')}</tr>`;
      $('.compare-table').innerHTML = `<table><thead><tr><th></th>${list.map(x => `<td><img src="${imgOf(x)}" alt=""><a href="${esc(x.p)}">${esc(x.n)}</a></td>`).join('')}</tr></thead><tbody>`
        + row('Typical price', x => money(x.pr)) + row('Brand', x => esc(x.bn || '—'))
        + keys.map(k => row(k, x => esc(((x.s || []).find(s => s[0] === k) || [, '—'])[1]))).join('') + '</tbody></table>';
      $('.compare-dialog').showModal();
    }
  });

  // ---- live search suggestions ----
  $$('[data-livesearch]').forEach(input => {
    const box = input.parentNode.querySelector('.suggest');
    let idx = -1;
    const run = async () => {
      const q = input.value.trim().toLowerCase();
      if (q.length < 2) { box.hidden = true; return; }
      const words = q.split(/\s+/), cat = await Gap.catalog();
      const hits = cat.map(x => {
        const hay = (x.n + ' ' + x.bn + ' ' + x.t + ' ' + x.p).toLowerCase();
        if (!words.every(w => hay.includes(w.replace(/s$/, '')))) return null;
        return [words.reduce((a, w) => a + (x.n.toLowerCase().includes(w) ? 3 : 1), 0), x];
      }).filter(Boolean).sort((a, b) => b[0] - a[0]).slice(0, 6).map(h => h[1]);
      idx = -1;
      box.innerHTML = hits.map(x => `<a href="${esc(x.p)}"><img src="${imgOf(x)}" alt=""><span><b>${esc(x.n)}</b><small>${esc(x.bn)} · ${money(x.pr)}</small></span></a>`).join('')
        + `<a class="s-all" href="/search/?q=${encodeURIComponent(input.value.trim())}">See all results for “${esc(input.value.trim())}”</a>`;
      box.hidden = false;
    };
    let t; input.addEventListener('input', () => { clearTimeout(t); t = setTimeout(run, 120); });
    input.addEventListener('focus', () => { if (input.value.trim().length > 1) run(); });
    input.addEventListener('keydown', e => {
      const links = $$('a', box); if (box.hidden || !links.length) return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        e.preventDefault(); idx = (idx + (e.key === 'ArrowDown' ? 1 : -1) + links.length) % links.length;
        links.forEach((l, i) => l.classList.toggle('active', i === idx));
      } else if (e.key === 'Enter' && idx >= 0) { e.preventDefault(); location.href = links[idx].href; }
      else if (e.key === 'Escape') box.hidden = true;
    });
    document.addEventListener('click', e => { if (!input.parentNode.contains(e.target)) box.hidden = true; });
  });

  // ---- listing filters / sort / show more ----
  $$('[data-listing]').forEach(root => {
    const grid = $('[data-grid]', root); if (!grid) return;
    const cards = $$('.card', grid), order = cards.slice();
    const PAGE = 24; let shown = PAGE;
    const more = $('[data-more]', root), count = $('[data-count]', root), empty = $('[data-empty]', root);
    const priceIn = $('[data-filter-price]', root), priceOut = $('[data-price-out]', root);
    const apply = () => {
      const brand = $('[data-filter-brand]', root)?.value || '';
      const max = priceIn ? +priceIn.value : Infinity;
      const dept = $('[data-filter-dept]:checked', root)?.value || '';
      const uses = $$('[data-filter-use]:checked', root).map(i => i.value);
      const pro = $('[data-filter-level]', root)?.checked;
      const sort = $('[data-sort]', root)?.value || '';
      if (priceOut && priceIn) priceOut.textContent = money(max);
      let list = order.filter(c => (!brand || c.dataset.brand === brand) && +c.dataset.price <= max
        && (!dept || c.dataset.dept === dept) && (!uses.length || uses.some(u => (c.dataset.use || '').split(' ').includes(u)))
        && (!pro || c.dataset.level === 'pro'));
      if (sort === 'price-asc') list.sort((a, b) => a.dataset.price - b.dataset.price);
      if (sort === 'price-desc') list.sort((a, b) => b.dataset.price - a.dataset.price);
      if (sort === 'name') list.sort((a, b) => a.dataset.name.localeCompare(b.dataset.name));
      cards.forEach(c => c.classList.add('hide'));
      list.forEach((c, i) => { grid.appendChild(c); c.classList.toggle('hide', i >= shown); if (i < shown) c.classList.add('in'); });
      if (count) count.textContent = list.length;
      if (empty) empty.hidden = list.length > 0;
      if (more) more.hidden = list.length <= shown;
    };
    root.addEventListener('input', e => { if (e.target.matches('[data-filter-price]')) { shown = PAGE; apply(); } });
    root.addEventListener('change', () => { shown = PAGE; apply(); });
    more?.addEventListener('click', () => { shown += PAGE; apply(); });
    apply();
  });

  // ---- tabs ----
  $$('[data-tabs]').forEach(t => {
    const tabs = $$('[role=tab]', t), ink = $('.tab-ink', t);
    const moveInk = b => { if (ink) { ink.style.left = b.offsetLeft + 'px'; ink.style.width = b.offsetWidth + 'px'; } };
    const select = b => {
      tabs.forEach(x => { const on = x === b; x.setAttribute('aria-selected', on); $('#' + x.getAttribute('aria-controls')).hidden = !on; });
      moveInk(b);
    };
    tabs.forEach(b => b.addEventListener('click', () => select(b)));
    t.addEventListener('keydown', e => {
      const i = tabs.indexOf(document.activeElement); if (i < 0) return;
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { const n = tabs[(i + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length]; n.focus(); select(n); }
    });
    const hashTab = tabs.find(b => location.hash && b.getAttribute('aria-controls') === 'c-' + location.hash.slice(1));
    requestAnimationFrame(() => select(hashTab || tabs.find(b => b.getAttribute('aria-selected') === 'true') || tabs[0]));
  });

  // ---- shelves ----
  $$('[data-shelf]').forEach(shelf => {
    const wrap = shelf.parentNode;
    $('[data-shelf-prev]', wrap)?.addEventListener('click', () => shelf.scrollBy({ left: -shelf.clientWidth * .8, behavior: 'smooth' }));
    $('[data-shelf-next]', wrap)?.addEventListener('click', () => shelf.scrollBy({ left: shelf.clientWidth * .8, behavior: 'smooth' }));
  });

  // ---- mobile nav ----
  const toggle = $('.nav-toggle');
  toggle?.addEventListener('click', () => { const open = document.body.classList.toggle('nav-open'); toggle.setAttribute('aria-expanded', open); });
  document.addEventListener('click', e => { if (document.body.classList.contains('nav-open') && !e.target.closest('.mainnav, .nav-toggle')) { document.body.classList.remove('nav-open'); toggle.setAttribute('aria-expanded', 'false'); } });

  // ---- reveal on scroll ----
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal, .kit-visual, .rings-art').forEach(el => io.observe(el));
  } else $$('.reveal, .kit-visual, .rings-art').forEach(el => el.classList.add('in'));

  // ---- 3D tilt + spotlight ----
  if (fine && !reduce) {
    document.addEventListener('pointermove', e => {
      const el = e.target.closest('.tilt, .tilt-deep'); if (!el) return;
      const r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      const k = el.classList.contains('tilt-deep') ? 10 : 5;
      el.style.transform = `perspective(900px) rotateX(${(.5 - y) * k}deg) rotateY(${(x - .5) * k}deg) translateY(-3px)`;
      el.style.setProperty('--mx', x * 100 + '%'); el.style.setProperty('--my', y * 100 + '%');
      const img = el.classList.contains('tilt-deep') && $('img', el);
      if (img) img.style.transform = `translate(${(x - .5) * 18}px, ${(y - .5) * 18}px)`;
    }, { passive: true });
    document.addEventListener('pointerout', e => {
      const el = e.target.closest('.tilt, .tilt-deep'); if (!el || el.contains(e.relatedTarget)) return;
      el.style.transform = ''; const img = $('img', el); if (img && el.classList.contains('tilt-deep')) img.style.transform = '';
    });
  }

  // ---- scroll: rope progress, sticky header shadow, parallax, sticky buy bar ----
  const header = $('.site-header'), layers = $$('.hero-layers .layer'), sticky = $('.sticky-buy'), buyRow = $('.buy-row');
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    const y = scrollY, max = document.documentElement.scrollHeight - innerHeight;
    document.documentElement.style.setProperty('--rope', (max > 0 ? Math.min(100, y / max * 100) : 0) + '%');
    header?.classList.toggle('scrolled', y > 10);
    if (!reduce) layers.forEach(l => { l.style.transform = `translateY(${y * l.dataset.depth}px)`; });
    if (sticky && buyRow) { const show = buyRow.getBoundingClientRect().bottom < 0; sticky.hidden = false; sticky.classList.toggle('show', show); }
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // ---- hero canvas: drifting leaves and sawdust ----
  const cv = $('.hero-canvas');
  if (cv && !reduce) {
    const ctx = cv.getContext('2d'); let W, H, dpr, parts = [], mouse = { x: -999, y: -999 }, run = true;
    const colors = ['#6b8f3e', '#c8e03c', '#2f5d3a', '#8a5a36', '#f26b1d'];
    const size = () => { dpr = Math.min(2, devicePixelRatio || 1); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    const make = (top) => {
      const leaf = Math.random() < .55;
      return { x: Math.random() * W, y: top ? -20 : Math.random() * H, s: leaf ? 6 + Math.random() * 9 : 1 + Math.random() * 2.2, leaf,
        vy: leaf ? .35 + Math.random() * .6 : .2 + Math.random() * .5, vx: (Math.random() - .5) * .4, r: Math.random() * 6.3, vr: (Math.random() - .5) * .04,
        sw: Math.random() * 6.3, c: leaf ? colors[Math.floor(Math.random() * 4)] : 'rgba(236,211,165,.7)' };
    };
    size(); parts = Array.from({ length: Math.min(70, Math.round(W / 16)) }, () => make(false));
    addEventListener('resize', size);
    cv.parentNode.addEventListener('pointermove', e => { const r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    new IntersectionObserver(([en]) => { run = en.isIntersecting; if (run) requestAnimationFrame(tick); }).observe(cv);
    function tick() {
      if (!run) return;
      ctx.clearRect(0, 0, W, H);
      for (const p of parts) {
        p.sw += .02; p.x += p.vx + Math.sin(p.sw) * (p.leaf ? .6 : .2); p.y += p.vy; p.r += p.vr;
        const dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < 9000) { const f = (9000 - d2) / 9000 * 2.4; p.x += dx / Math.sqrt(d2 + 1) * f; p.y += dy / Math.sqrt(d2 + 1) * f; p.vr += .002; }
        if (p.y > H + 20 || p.x < -30 || p.x > W + 30) Object.assign(p, make(true));
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillStyle = p.c;
        if (p.leaf) {
          ctx.globalAlpha = .75; ctx.beginPath(); ctx.moveTo(0, -p.s);
          ctx.quadraticCurveTo(p.s * .7, 0, 0, p.s); ctx.quadraticCurveTo(-p.s * .7, 0, 0, -p.s); ctx.fill();
          ctx.strokeStyle = 'rgba(13,28,20,.35)'; ctx.lineWidth = .8; ctx.beginPath(); ctx.moveTo(0, -p.s); ctx.lineTo(0, p.s); ctx.stroke();
        } else { ctx.fillRect(-p.s / 2, -p.s / 2, p.s, p.s * .6); }
        ctx.restore();
      }
      requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // Cross-tab sync
  addEventListener('storage', e => { if (e.key && e.key.startsWith('gap.')) { updateBadges(); renderCompareBar(); } });
  updateBadges(); renderCompareBar();
})();
