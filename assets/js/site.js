/* Christina Dittman Creations - Belton Banners
   Site behavior: header, nav, scroll reveals, parallax, counters, tilt, paint
   cursor, gallery strip, filters, lightbox, banner designer, forms.
   No framework, no build step. Everything degrades to plain HTML. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- Header, progress bar, mobile nav ---------- */
  const header = $('.site-header');
  const progress = $('.scroll-progress span');
  const onScroll = () => {
    const y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 10);
    if (progress) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + '%';
    }
    parallaxTick();
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  const menuBtn = $('.menu-btn');
  const nav = $('#primary-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
    });
    nav.addEventListener('click', (e) => { if (e.target.closest('a')) { nav.classList.remove('is-open'); menuBtn.setAttribute('aria-expanded', 'false'); } });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('is-open')) menuBtn.click(); });
  }

  /* ---------- Split headings into animated words ---------- */
  $$('[data-split]').forEach((el) => {
    if (reduced) return;
    let wi = 0;
    const walk = (node) => {
      Array.from(node.childNodes).forEach((child) => {
        if (child.nodeType === 3) {
          const frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach((part) => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            const w = document.createElement('span'); w.className = 'w';
            const inner = document.createElement('span'); inner.textContent = part; inner.style.setProperty('--wi', wi++);
            w.appendChild(inner); frag.appendChild(w);
          });
          node.replaceChild(frag, child);
        } else if (child.nodeType === 1 && !child.classList.contains('w')) {
          walk(child);
        }
      });
    };
    walk(el);
  });

  /* ---------- Reveal on scroll ---------- */
  // Brush frames are clipped to zero width until revealed, which makes them
  // invisible to IntersectionObserver - so their parent is observed instead.
  const revealTargets = $$('[data-reveal]');
  const brushes = $$('[data-brush]');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        const t = en.target;
        if (t.hasAttribute('data-reveal')) t.classList.add('is-visible');
        (t._brush || []).forEach((b) => b.classList.add('is-visible'));
        io.unobserve(t);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealTargets.forEach((el) => io.observe(el));
    brushes.forEach((b) => { const p = b.parentElement; (p._brush = p._brush || []).push(b); io.observe(p); });
  } else {
    revealTargets.concat(brushes).forEach((el) => el.classList.add('is-visible'));
  }

  /* ---------- Parallax ---------- */
  const parallaxEls = reduced ? [] : $$('[data-parallax]');
  let ticking = false;
  function parallaxTick() {
    if (!parallaxEls.length || ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      const vh = window.innerHeight;
      parallaxEls.forEach((el) => {
        const speed = parseFloat(el.dataset.parallax) || 0.3;
        const r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        const center = r.top + r.height / 2 - vh / 2;
        el.style.transform = `translate3d(0, ${(-center * speed).toFixed(1)}px, 0)`;
      });
      ticking = false;
    });
  }

  /* ---------- Counters ---------- */
  const counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    const cio = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        const el = en.target; cio.unobserve(el);
        const end = parseFloat(el.dataset.count); const pre = el.dataset.prefix || ''; const suf = el.dataset.suffix || '';
        if (reduced) { el.textContent = pre + end + suf; return; }
        const t0 = performance.now(); const dur = 1400;
        const step = (t) => {
          const p = Math.min(1, (t - t0) / dur); const e = 1 - Math.pow(1 - p, 3);
          el.textContent = pre + Math.round(end * e) + suf;
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
      });
    }, { threshold: 0.6 });
    counters.forEach((c) => cio.observe(c));
  }

  /* ---------- Tilt cards ---------- */
  if (finePointer && !reduced) {
    $$('[data-tilt]').forEach((card) => {
      let raf = null;
      card.addEventListener('pointermove', (e) => {
        if (raf) return;
        raf = requestAnimationFrame(() => {
          const r = card.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width - 0.5; const y = (e.clientY - r.top) / r.height - 0.5;
          card.style.transform = `perspective(900px) rotateX(${(-y * 7).toFixed(2)}deg) rotateY(${(x * 9).toFixed(2)}deg) translateY(-6px)`;
          raf = null;
        });
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }

  /* ---------- Paint trail on the hero ---------- */
  const canvas = $('.paint-canvas');
  if (canvas && finePointer && !reduced) {
    const ctx = canvas.getContext('2d');
    const hero = canvas.parentElement;
    const colors = ['#8A64A7', '#1A8084', '#9ACC6A', '#E0BE93', '#E8743B', '#F4B6C2'];
    let drops = []; let w = 0; let h = 0; let running = false;
    const size = () => { const r = hero.getBoundingClientRect(); w = canvas.width = Math.floor(r.width); h = canvas.height = Math.floor(r.height); };
    size(); window.addEventListener('resize', size);
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      for (let i = 0; i < 2; i++) {
        drops.push({ x: e.clientX - r.left + (Math.random() - .5) * 14, y: e.clientY - r.top + (Math.random() - .5) * 14, r: 3 + Math.random() * 9, c: colors[(Math.random() * colors.length) | 0], a: 0.85, vx: (Math.random() - .5) * .6, vy: .4 + Math.random() * .8 });
      }
      if (drops.length > 160) drops.splice(0, drops.length - 160);
      if (!running) { running = true; requestAnimationFrame(draw); }
    });
    function draw() {
      ctx.clearRect(0, 0, w, h);
      drops = drops.filter((d) => d.a > 0.02);
      drops.forEach((d) => {
        ctx.globalAlpha = d.a; ctx.fillStyle = d.c; ctx.beginPath(); ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2); ctx.fill();
        d.a *= 0.965; d.x += d.vx; d.y += d.vy; d.r *= 0.995;
      });
      ctx.globalAlpha = 1;
      if (drops.length) requestAnimationFrame(draw); else running = false;
    }
  }

  /* ---------- Gallery strip: drag + arrows ---------- */
  const strip = $('[data-strip]');
  if (strip) {
    const step = () => Math.min(strip.clientWidth * 0.8, 460);
    const prev = $('[data-strip-prev]'); const next = $('[data-strip-next]');
    prev && prev.addEventListener('click', () => strip.scrollBy({ left: -step(), behavior: 'smooth' }));
    next && next.addEventListener('click', () => strip.scrollBy({ left: step(), behavior: 'smooth' }));
    if (finePointer) {
      let down = false; let startX = 0; let startL = 0; let moved = false;
      strip.addEventListener('pointerdown', (e) => { down = true; moved = false; startX = e.clientX; startL = strip.scrollLeft; strip.classList.add('is-dragging'); });
      window.addEventListener('pointermove', (e) => { if (!down) return; const dx = e.clientX - startX; if (Math.abs(dx) > 4) moved = true; strip.scrollLeft = startL - dx; });
      window.addEventListener('pointerup', () => { down = false; strip.classList.remove('is-dragging'); });
      strip.addEventListener('click', (e) => { if (moved) { e.preventDefault(); moved = false; } });
    }
  }

  /* ---------- Gallery filters ---------- */
  const filters = $('[data-filters]');
  const grid = $('[data-gallery]');
  if (filters && grid) {
    const cards = $$('.creation-card', grid);
    const empty = $('[data-empty]');
    const apply = (key) => {
      let shown = 0;
      cards.forEach((c, i) => {
        const show = key === 'all' || c.dataset.cat === key;
        c.classList.toggle('is-hidden', !show);
        if (show) { c.style.setProperty('--i', shown % 6); c.classList.remove('is-visible'); void c.offsetWidth; c.classList.add('is-visible'); shown++; }
      });
      if (empty) empty.hidden = shown > 0;
    };
    filters.addEventListener('click', (e) => {
      const b = e.target.closest('[data-filter]'); if (!b) return;
      $$('[data-filter]', filters).forEach((x) => x.classList.toggle('is-active', x === b));
      apply(b.dataset.filter);
      history.replaceState(null, '', b.dataset.filter === 'all' ? location.pathname : '#' + b.dataset.filter);
    });
    const initial = location.hash.replace('#', '');
    const btn = initial && $(`[data-filter="${CSS.escape(initial)}"]`, filters);
    if (btn) btn.click();
  }

  /* ---------- Lightbox (gallery cards, product image, any [data-lightbox]) ---------- */
  const lb = $('#lightbox');
  if (lb) {
    const lbImg = $('img', lb); const lbCap = $('figcaption', lb);
    let items = []; let idx = 0;
    const collect = () => {
      const g = $('[data-gallery]');
      if (g) {
        items = $$('.creation-card:not(.is-hidden)', g).map((c) => ({ src: $('img', c).src.replace(/-800\.webp$/, '.webp'), cap: $('h3', c).textContent, href: c.getAttribute('href') }));
      } else {
        items = $$('[data-lightbox]').map((a) => ({ src: a.getAttribute('href'), cap: a.dataset.caption || '' }));
      }
    };
    const show = (i) => {
      idx = (i + items.length) % items.length; const it = items[idx];
      lbImg.src = it.src; lbImg.alt = it.cap; lbCap.innerHTML = it.cap + (it.href ? ` &middot; <a href="${it.href}" style="color:#E0BE93">Open banner →</a>` : '');
      lb.hidden = false; lb.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden';
      $('.lb-prev', lb).style.display = $('.lb-next', lb).style.display = items.length > 1 ? '' : 'none';
    };
    const close = () => { lb.hidden = true; lb.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; };
    document.addEventListener('click', (e) => {
      const a = e.target.closest('[data-lightbox]');
      if (a) { e.preventDefault(); collect(); show(items.findIndex((it) => it.src === a.getAttribute('href'))); return; }
      const media = e.target.closest('[data-gallery] .creation-card .card-media');
      if (media && finePointer) { e.preventDefault(); collect(); const card = media.closest('.creation-card'); show(items.findIndex((it) => it.href === card.getAttribute('href'))); }
    });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', () => show(idx - 1));
    $('.lb-next', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    document.addEventListener('keydown', (e) => {
      if (lb.hidden) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowRight') show(idx + 1); if (e.key === 'ArrowLeft') show(idx - 1);
    });
    let tx = 0;
    lb.addEventListener('touchstart', (e) => { tx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', (e) => { const dx = e.changedTouches[0].clientX - tx; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); });
  }

  /* ---------- Banner designer ---------- */
  const MOTIFS = { none: ['', '', '', ''], star: ['✦', '★', '✧', '⭐'], heart: ['♥', '💗', '♥', '💕'], flower: ['🌸', '🌼', '🌷', '🌿'], sunflower: ['🌻', '🌻', '🌿', '🌻'], balloon: ['🎈', '🎉', '🎈', '🎊'], pumpkin: ['🎃', '🍂', '🍁', '🎃'], leaf: ['🌿', '🍃', '🌿', '🍃'], cross: ['✝', '🕊', '✝', '🌾'], truck: ['🚜', '🚧', '🛻', '🚜'] };
  const MOTIF_LABEL = { none: 'no motif', star: 'stars', heart: 'hearts', flower: 'flowers', sunflower: 'sunflowers', balloon: 'balloons', pumpkin: 'pumpkins', leaf: 'greenery', cross: 'cross', truck: 'trucks' };
  const STYLE_LABEL = { script: 'script lettering', bold: 'bold block lettering', serif: 'elegant serif lettering' };
  $$('[data-designer]').forEach((d) => {
    const preview = $('[data-preview]', d); const l1 = $('[data-in-line1]', d); const l2 = $('[data-in-line2]', d);
    const t1 = $('.bp-line1', preview); const t2 = $('.bp-line2', preview); const motifs = $$('.motif', preview);
    const sizeSel = $('[data-in-size]', d); const wobble = $('[data-in-wobble]', d); const summary = $('[data-summary]', d);
    const state = { style: 'script', paper: 'kraft', ink: '#F5F0E6', motif: 'sunflower', size: sizeSel.value };
    const ratioOf = (s) => { const m = s.match(/(\d+)\D+(\d+)/); return m ? `${m[1]}/${m[2]}` : '48/30'; };
    const setActive = (container, attr, val) => $$(`[${attr}]`, container).forEach((b) => b.classList.toggle('is-active', b.getAttribute(attr) === val));
    const render = () => {
      t1.textContent = l1.value || ' '; t2.textContent = l2.value || ' ';
      preview.dataset.style = state.style; preview.dataset.paper = state.paper; preview.dataset.motif = state.motif;
      preview.style.setProperty('--ink', state.ink); preview.style.setProperty('--ratio', ratioOf(state.size)); preview.style.setProperty('--wobble', wobble.value);
      motifs.forEach((m, i) => { m.textContent = MOTIFS[state.motif][i]; });
      summary.textContent = `${state.size} · ${state.paper} paper · ${STYLE_LABEL[state.style]} · ${MOTIF_LABEL[state.motif]}`;
      setActive($('[data-styles]', d), 'data-style', state.style); setActive($('[data-papers]', d), 'data-paper', state.paper);
      setActive($('[data-inks]', d), 'data-ink', state.ink); setActive($('[data-motifs]', d), 'data-motif', state.motif);
      if (sizeSel.value !== state.size) sizeSel.value = state.size;
      if (state.paper === 'black' && state.ink === '#2F2F2F') { state.ink = '#F5F0E6'; render(); }
    };
    [l1, l2].forEach((i) => i.addEventListener('input', render));
    wobble.addEventListener('input', render);
    sizeSel.addEventListener('change', () => { state.size = sizeSel.value; render(); });
    d.addEventListener('click', (e) => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.hasAttribute('data-preset')) {
        l1.value = b.dataset.pLine1; l2.value = b.dataset.pLine2; state.style = b.dataset.pStyle; state.paper = b.dataset.pPaper; state.ink = b.dataset.pInk; state.motif = b.dataset.pMotif; state.size = b.dataset.pSize;
        $$('[data-preset]', d).forEach((x) => x.classList.toggle('is-active', x === b));
      } else if (b.closest('[data-styles]')) state.style = b.dataset.style;
      else if (b.closest('[data-papers]')) state.paper = b.dataset.paper;
      else if (b.closest('[data-inks]')) state.ink = b.dataset.ink;
      else if (b.closest('[data-motifs]')) state.motif = b.dataset.motif;
      else if (b.hasAttribute('data-shuffle')) {
        const pick = (arr) => arr[(Math.random() * arr.length) | 0];
        const presets = $$('[data-preset]', d); const p = pick(presets);
        l1.value = p.dataset.pLine1; l2.value = p.dataset.pLine2;
        state.style = pick(['script', 'bold', 'serif']); state.paper = pick(['kraft', 'kraft', 'cream', 'grey', 'black']);
        state.ink = pick($$('[data-ink]', $('[data-inks]', d)).map((s) => s.dataset.ink)); state.motif = pick(Object.keys(MOTIFS).filter((k) => k !== 'none')); state.size = pick(Array.from(sizeSel.options).map((o) => o.value));
      } else return;
      render();
    });
    const send = $('[data-send-design]', d);
    send && send.addEventListener('click', (e) => {
      const msg = `Banner mock-up from the designer:\n- Wording: "${l1.value}" / "${l2.value}"\n- Size: ${state.size}\n- Paper: ${state.paper}\n- Lettering: ${STYLE_LABEL[state.style]}\n- Ink color: ${state.ink}\n- Motif: ${MOTIF_LABEL[state.motif]}\n\nNotes: `;
      const form = $('.quote-form');
      if (form) {
        e.preventDefault();
        const m = form.querySelector('[name="message"]'); const w = form.querySelector('[name="wording"]'); const s = form.querySelector('[name="size"]');
        if (m) m.value = msg; if (w) w.value = `${l1.value} ${l2.value}`.trim();
        if (s) Array.from(s.options).forEach((o) => { if (o.value === state.size) s.value = o.value; });
        form.closest('section').scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
        setTimeout(() => { const f = form.querySelector('[name="name"]'); f && f.focus({ preventScroll: true }); }, 700);
        toast('Design added to the form - add your details and send.');
      } else {
        try { sessionStorage.setItem('cdc-design', msg); sessionStorage.setItem('cdc-wording', `${l1.value} ${l2.value}`.trim()); sessionStorage.setItem('cdc-size', state.size); } catch (_) {}
      }
    });
    render();
  });
  // A design carried over from another page
  try {
    const carried = sessionStorage.getItem('cdc-design');
    const form = $('.quote-form');
    if (carried && form) {
      const m = form.querySelector('[name="message"]'); if (m && !m.value) m.value = carried;
      const w = form.querySelector('[name="wording"]'); if (w && !w.value) w.value = sessionStorage.getItem('cdc-wording') || '';
      const s = form.querySelector('[name="size"]'); const sz = sessionStorage.getItem('cdc-size'); if (s && sz) s.value = sz;
      ['cdc-design', 'cdc-wording', 'cdc-size'].forEach((k) => sessionStorage.removeItem(k));
    }
  } catch (_) {}

  /* ---------- Forms (AJAX to contact.php, with full-page fallback) ---------- */
  $$('.quote-form').forEach((form) => {
    const status = $('.form-status', form);
    form.addEventListener('submit', async (e) => {
      if (!form.checkValidity()) { e.preventDefault(); form.reportValidity(); return; }
      if (!window.fetch) return;
      e.preventDefault();
      form.classList.add('is-sending'); status.className = 'form-status'; status.textContent = 'Sending…';
      try {
        const fd = new FormData(form); fd.append('ajax', '1');
        const res = await fetch(form.action, { method: 'POST', body: fd, headers: { 'Accept': 'application/json' } });
        const data = await res.json();
        if (data.ok) {
          status.className = 'form-status ok'; status.textContent = data.message || 'Sent! Christina will be in touch soon.';
          form.reset();
        } else {
          status.className = 'form-status err'; status.textContent = data.message || 'Something went wrong. Please call or text instead.';
        }
      } catch (err) {
        status.className = 'form-status err'; status.textContent = 'Could not send right now. Please call or text +1 817-729-2961.';
      }
      form.classList.remove('is-sending');
    });
  });

  /* ---------- Copy link + toast ---------- */
  let toastEl = null;
  function toast(msg) {
    if (!toastEl) { toastEl = document.createElement('div'); toastEl.className = 'toast'; document.body.appendChild(toastEl); }
    toastEl.textContent = msg; toastEl.classList.add('is-on');
    clearTimeout(toastEl._t); toastEl._t = setTimeout(() => toastEl.classList.remove('is-on'), 2800);
  }
  document.addEventListener('click', (e) => {
    const b = e.target.closest('[data-copy]'); if (!b) return;
    (navigator.clipboard ? navigator.clipboard.writeText(b.dataset.copy) : Promise.reject()).then(() => toast('Link copied'), () => toast(b.dataset.copy));
  });

  onScroll();
})();
