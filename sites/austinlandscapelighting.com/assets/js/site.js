/* Austin Landscape Lighting - shared site behavior.
   Header, mobile nav, scroll progress, reveal-on-scroll, parallax, counters,
   cursor spotlight, card glow + tilt, compare slider, lights toggle, hero
   scene, star fields, process line, TOC highlighting, gallery lightbox,
   technique explorer, contact-form validation. No dependencies. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(pointer: fine)').matches;

  /* ---- Header + progress + back-to-top ---- */
  const header = $('[data-header]');
  const progress = $('[data-progress]');
  const toTop = $('[data-totop]');
  const onScroll = () => {
    const y = window.scrollY;
    if (header) header.classList.toggle('is-scrolled', y > 24);
    if (progress) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
    }
    if (toTop) toTop.classList.toggle('is-visible', y > 600);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', (e) => { e.preventDefault(); window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }); });

  /* ---- Mobile nav ---- */
  const menuBtn = $('[data-menu]');
  const nav = $('[data-nav]');
  if (menuBtn && nav) {
    nav.id = 'primary-nav';
    const setOpen = (open) => {
      nav.classList.toggle('is-open', open);
      menuBtn.setAttribute('aria-expanded', String(open));
      menuBtn.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      document.body.style.overflow = open ? 'hidden' : '';
    };
    menuBtn.addEventListener('click', () => setOpen(!nav.classList.contains('is-open')));
    nav.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
    window.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
    window.addEventListener('resize', () => { if (window.innerWidth > 960) setOpen(false); });
  }

  /* ---- Lights toggle (site-wide "flip the switch") ---- */
  const lightsBtn = $('[data-lights-toggle]');
  const setLights = (off) => {
    document.body.classList.toggle('lights-off', off);
    if (lightsBtn) lightsBtn.setAttribute('aria-pressed', String(off));
    $$('[data-hero-switch]').forEach((b) => { b.querySelector('span:last-child').textContent = off ? 'Turn the lights on' : 'Flip the switch'; });
    $$('.scene[data-hero-scene]').forEach((s) => s.classList.toggle('lights-off', off));
  };
  if (lightsBtn) lightsBtn.addEventListener('click', () => setLights(!document.body.classList.contains('lights-off')));
  $$('[data-hero-switch]').forEach((b) => b.addEventListener('click', () => setLights(!document.body.classList.contains('lights-off'))));
  if (!$('.hero-note') && lightsBtn) {
    const note = document.createElement('div');
    note.className = 'hero-note';
    note.textContent = 'This is your yard without Austin Landscape Lighting. Flip the switch back on.';
    document.body.appendChild(note);
  }

  /* ---- Reveal on scroll ---- */
  const revealEls = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('in'));
  }

  /* ---- Count-up numbers ---- */
  const counters = $$('[data-count]');
  if (counters.length) {
    const run = (el) => {
      const end = parseFloat(el.dataset.count);
      const dec = parseInt(el.dataset.decimals || '0', 10);
      const dur = 1400;
      const t0 = performance.now();
      const step = (t) => {
        const p = Math.min(1, (t - t0) / dur);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = (end * eased).toFixed(dec);
        if (p < 1) requestAnimationFrame(step); else el.textContent = end.toFixed(dec);
      };
      if (reduced) { el.textContent = end.toFixed(dec); return; }
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      const cio = new IntersectionObserver((entries) => {
        entries.forEach((en) => { if (en.isIntersecting) { run(en.target); cio.unobserve(en.target); } });
      }, { threshold: 0.4 });
      counters.forEach((c) => cio.observe(c));
    } else counters.forEach(run);
  }

  /* ---- Parallax ---- */
  const px = $$('[data-parallax]');
  if (px.length && !reduced) {
    let ticking = false;
    const update = () => {
      const vh = window.innerHeight;
      px.forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) return;
        const speed = parseFloat(el.dataset.parallax) || 0.15;
        const offset = (r.top + r.height / 2 - vh / 2) * speed * -1;
        el.style.transform = `translate3d(0, ${offset.toFixed(1)}px, 0)`;
      });
      ticking = false;
    };
    window.addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(update); ticking = true; } }, { passive: true });
    update();
  }

  /* ---- Cursor spotlight on dark sections ---- */
  if (fine) {
    $$('[data-spotlight]').forEach((sec) => {
      sec.addEventListener('pointermove', (e) => {
        const r = sec.getBoundingClientRect();
        sec.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100).toFixed(2) + '%');
        sec.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100).toFixed(2) + '%');
      });
    });
  }

  /* ---- Card glow + tilt ---- */
  if (fine && !reduced) {
    $$('.card').forEach((card) => {
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        card.style.setProperty('--gx', (x * 100).toFixed(1) + '%');
        card.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
        if (card.classList.contains('tilt')) {
          card.style.transform = `translateY(-6px) rotateX(${((0.5 - y) * 6).toFixed(2)}deg) rotateY(${((x - 0.5) * 6).toFixed(2)}deg)`;
        }
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }

  /* ---- Star fields ---- */
  $$('[data-stars]').forEach((wrap) => {
    const n = 40;
    const frag = document.createDocumentFragment();
    for (let i = 0; i < n; i++) {
      const s = document.createElement('i');
      s.style.left = (Math.random() * 100).toFixed(2) + '%';
      s.style.top = (Math.random() * 100).toFixed(2) + '%';
      s.style.setProperty('--d', (2 + Math.random() * 4).toFixed(2) + 's');
      s.style.setProperty('--dl', (Math.random() * 4).toFixed(2) + 's');
      s.style.opacity = (0.2 + Math.random() * 0.6).toFixed(2);
      s.style.width = s.style.height = (1 + Math.random() * 1.6).toFixed(1) + 'px';
      frag.appendChild(s);
    }
    wrap.appendChild(frag);
  });

  /* ---- Hero canvas: stars + drifting fireflies ---- */
  const canvas = $('[data-hero-canvas]');
  if (canvas && !reduced) {
    const ctx = canvas.getContext('2d');
    let w, h, stars = [], flies = [];
    const resize = () => {
      const r = canvas.parentElement.getBoundingClientRect();
      w = canvas.width = Math.floor(r.width * devicePixelRatio);
      h = canvas.height = Math.floor(r.height * devicePixelRatio);
      stars = Array.from({ length: 140 }, () => ({ x: Math.random() * w, y: Math.random() * h * 0.7, r: Math.random() * 1.4 * devicePixelRatio, p: Math.random() * Math.PI * 2, s: 0.4 + Math.random() }));
      flies = Array.from({ length: 18 }, () => ({ x: Math.random() * w, y: h * (0.4 + Math.random() * 0.6), vx: (Math.random() - 0.5) * 0.3, vy: (Math.random() - 0.5) * 0.2, p: Math.random() * Math.PI * 2, r: (1.5 + Math.random() * 2) * devicePixelRatio }));
    };
    let last = 0;
    const draw = (t) => {
      if (document.hidden) { requestAnimationFrame(draw); return; }
      if (t - last < 1000 / 40) { requestAnimationFrame(draw); return; }
      last = t;
      ctx.clearRect(0, 0, w, h);
      const off = document.body.classList.contains('lights-off');
      stars.forEach((s) => {
        const a = 0.35 + 0.45 * Math.sin(t / 900 * s.s + s.p);
        ctx.globalAlpha = a; ctx.fillStyle = '#fff';
        ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2); ctx.fill();
      });
      if (!off) {
        flies.forEach((f) => {
          f.x += f.vx * devicePixelRatio; f.y += f.vy * devicePixelRatio;
          f.vx += (Math.random() - 0.5) * 0.02; f.vy += (Math.random() - 0.5) * 0.02;
          f.vx = Math.max(-0.5, Math.min(0.5, f.vx)); f.vy = Math.max(-0.3, Math.min(0.3, f.vy));
          if (f.x < 0) f.x = w; if (f.x > w) f.x = 0; if (f.y < h * 0.3) f.y = h; if (f.y > h) f.y = h * 0.3;
          const a = 0.25 + 0.65 * Math.max(0, Math.sin(t / 700 + f.p));
          const g = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r * 5);
          g.addColorStop(0, `rgba(255,224,160,${a})`); g.addColorStop(1, 'rgba(255,179,71,0)');
          ctx.globalAlpha = 1; ctx.fillStyle = g;
          ctx.beginPath(); ctx.arc(f.x, f.y, f.r * 5, 0, Math.PI * 2); ctx.fill();
        });
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(draw);
    };
    resize();
    window.addEventListener('resize', resize);
    requestAnimationFrame(draw);
  }

  /* ---- Hero scene: lights come on after load ---- */
  $$('.scene[data-hero-scene]').forEach((s) => {
    setTimeout(() => s.classList.add('is-lit'), reduced ? 0 : 500);
  });

  /* ---- Compare slider ---- */
  $$('[data-compare]').forEach((c) => {
    const range = $('.compare__range', c);
    const set = (v) => c.style.setProperty('--pos', v + '%');
    set(range.value);
    range.addEventListener('input', () => set(range.value));
    let auto;
    if (!reduced && 'IntersectionObserver' in window) {
      const io = new IntersectionObserver((en) => {
        if (en[0].isIntersecting && !c.dataset.played) {
          c.dataset.played = '1';
          let v = 38, dir = 1, n = 0;
          auto = setInterval(() => {
            v += dir * 0.9;
            if (v > 70 || v < 25) { dir *= -1; n++; }
            range.value = v.toFixed(1); set(range.value);
            if (n >= 2) clearInterval(auto);
          }, 16);
          io.disconnect();
        }
      }, { threshold: 0.5 });
      io.observe(c);
      range.addEventListener('pointerdown', () => clearInterval(auto));
    }
  });

  /* ---- Process line fill ---- */
  const proc = $('[data-process]');
  if (proc) {
    const fill = $('.process__fill', proc);
    const upd = () => {
      const r = proc.getBoundingClientRect();
      const vh = window.innerHeight;
      const p = Math.min(1, Math.max(0, (vh - r.top) / (r.height + vh * 0.4)));
      fill.style.setProperty('--fill', (p * 100).toFixed(1) + '%');
    };
    window.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  /* ---- TOC active state ---- */
  const toc = $('[data-toc]');
  if (toc && 'IntersectionObserver' in window) {
    const links = $$('a', toc);
    const heads = links.map((a) => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
    const hio = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          links.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    heads.forEach((h) => hio.observe(h));
  }

  /* ---- Gallery filters + lightbox ---- */
  const gallery = $('[data-gallery]');
  if (gallery) {
    const figs = $$('figure', gallery);
    $$('[data-filter]').forEach((btn) => btn.addEventListener('click', () => {
      $$('[data-filter]').forEach((b) => b.classList.toggle('is-active', b === btn));
      const f = btn.dataset.filter;
      figs.forEach((fig) => fig.classList.toggle('is-hidden', f !== 'all' && fig.dataset.cat !== f));
    }));
  }
  const lbTargets = $$('[data-lightbox] img, .gallery-strip img, .masonry img');
  if (lbTargets.length) {
    const lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Image viewer');
    lb.innerHTML = '<button class="lightbox__close" aria-label="Close">✕</button><button class="lightbox__prev" aria-label="Previous">⌄</button><img alt=""><button class="lightbox__next" aria-label="Next">⌄</button><p class="lightbox__cap"></p>';
    document.body.appendChild(lb);
    const img = $('img', lb), cap = $('.lightbox__cap', lb);
    let visible = [], idx = 0;
    const show = (i) => {
      idx = (i + visible.length) % visible.length;
      const t = visible[idx];
      img.src = t.dataset.full || t.currentSrc || t.src; img.alt = t.alt; cap.textContent = t.alt;
    };
    const open = (t) => {
      visible = lbTargets.filter((el) => !el.closest('.is-hidden'));
      show(visible.indexOf(t)); lb.classList.add('is-open'); document.body.style.overflow = 'hidden';
    };
    const close = () => { lb.classList.remove('is-open'); document.body.style.overflow = ''; };
    lbTargets.forEach((t) => t.addEventListener('click', () => open(t)));
    $('.lightbox__close', lb).addEventListener('click', close);
    $('.lightbox__prev', lb).addEventListener('click', () => show(idx - 1));
    $('.lightbox__next', lb).addEventListener('click', () => show(idx + 1));
    lb.addEventListener('click', (e) => { if (e.target === lb) close(); });
    window.addEventListener('keydown', (e) => {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') show(idx - 1); if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ---- Technique explorer (homepage) ---- */
  const tech = $('[data-tech]');
  if (tech) {
    const items = $$('.tech__item', tech);
    const scene = $('.scene', tech);
    const cap = $('[data-tech-caption]', tech);
    const layers = $$('.lamp', scene);
    const activate = (btn) => {
      items.forEach((b) => b.classList.toggle('is-active', b === btn));
      const on = (btn.dataset.layers || '').split(' ');
      layers.forEach((l) => l.classList.toggle('is-on', on.includes(l.dataset.layer)));
      scene.classList.add('is-lit');
      layers.forEach((l) => { l.style.opacity = on.includes(l.dataset.layer) ? '1' : '0.06'; });
      if (cap) cap.innerHTML = `<strong>${btn.dataset.title}</strong>${btn.dataset.desc}`;
    };
    items.forEach((b) => { b.addEventListener('click', () => activate(b)); b.addEventListener('mouseenter', () => { if (fine) activate(b); }); });
    if (items[0]) activate(items[0]);
  }

  /* ---- Contact form: light client validation ---- */
  $$('[data-estimate-form]').forEach((form) => {
    const pageField = form.querySelector('[name="page"]');
    if (pageField) pageField.value = location.pathname;
    form.addEventListener('submit', (e) => {
      let ok = true;
      $$('[required]', form).forEach((f) => {
        const bad = !f.value.trim() || (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.classList.toggle('is-invalid', bad);
        if (bad) ok = false;
      });
      if (!ok) { e.preventDefault(); const first = $('.is-invalid', form); if (first) first.focus(); return; }
      const btn = $('button[type="submit"]', form);
      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
    });
  });

  /* ---- Smooth anchor offsets for sticky header ---- */
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (!a || a.getAttribute('href') === '#' || a.hasAttribute('data-totop')) return;
    const t = document.getElementById(a.getAttribute('href').slice(1));
    if (!t) return;
    e.preventDefault();
    const y = t.getBoundingClientRect().top + window.scrollY - 90;
    window.scrollTo({ top: y, behavior: reduced ? 'auto' : 'smooth' });
    history.pushState(null, '', a.getAttribute('href'));
  });

  /* ---- Service-area map (index page) ---- */
  const map = $('[data-map]');
  if (map) {
    const pins = $$('.map-pin', map);
    const name = $('[data-map-name]', map), desc = $('[data-map-desc]', map), link = $('[data-map-link]', map);
    const act = (p) => {
      pins.forEach((x) => x.classList.toggle('is-active', x === p));
      if (name) name.textContent = p.dataset.city;
      if (desc) desc.textContent = p.dataset.desc;
      if (link) { link.href = p.dataset.href; link.textContent = `See ${p.dataset.city} lighting →`; }
    };
    pins.forEach((p) => { p.addEventListener('click', () => act(p)); p.addEventListener('mouseenter', () => { if (fine) act(p); }); });
    if (pins[0]) act(pins[0]);
  }

  /* ---- Blog category filter ---- */
  const catNav = $('[data-cat-nav]');
  if (catNav) {
    const cards = $$('[data-cat-card]');
    $$('button', catNav).forEach((b) => b.addEventListener('click', () => {
      $$('button', catNav).forEach((x) => x.classList.toggle('is-active', x === b));
      cards.forEach((c) => { c.style.display = (b.dataset.cat === 'all' || c.dataset.catCard === b.dataset.cat) ? '' : 'none'; });
    }));
  }
})();
