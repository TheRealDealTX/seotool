/* Dogwood DIY - site behavior: mobile nav, sticky header, scroll effects,
   falling petals, reading progress, table of contents, project finder. */
(() => {
  document.documentElement.classList.remove('no-js');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Mobile nav ---- */
  const btn = document.querySelector('.menu-btn');
  const nav = document.getElementById('main-nav');
  const backdrop = document.querySelector('.nav-backdrop');
  const setNav = (open) => {
    if (!btn || !nav) return;
    nav.classList.toggle('is-open', open);
    backdrop && backdrop.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    if (open) { const first = nav.querySelector('a'); first && first.focus({ preventScroll: true }); }
  };
  if (btn && nav) {
    btn.addEventListener('click', () => setNav(btn.getAttribute('aria-expanded') !== 'true'));
    backdrop && backdrop.addEventListener('click', () => setNav(false));
    nav.addEventListener('click', (e) => { if (e.target.closest('a')) setNav(false); });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { setNav(false); btn.focus(); }
    });
    window.matchMedia('(min-width: 961px)').addEventListener('change', (m) => { if (m.matches) setNav(false); });
  }

  /* ---- Header shadow, back-to-top, progress, hero parallax ---- */
  const header = document.querySelector('.site-header');
  const toTop = document.querySelector('.to-top');
  const progress = document.querySelector('.progress');
  const article = document.querySelector('.prose');
  const heroBg = document.querySelector('.hero-bg');
  let ticking = false;
  const onScroll = () => {
    const y = window.scrollY;
    header && header.classList.toggle('is-scrolled', y > 10);
    toTop && toTop.classList.toggle('show', y > 700);
    if (progress && article) {
      const r = article.getBoundingClientRect();
      const total = r.height - window.innerHeight * 0.6;
      const pct = Math.min(100, Math.max(0, (-r.top / total) * 100));
      progress.style.width = pct + '%';
    }
    if (heroBg && !reduce && y < window.innerHeight * 1.2) heroBg.style.transform = `translateY(${y * 0.28}px)`;
    ticking = false;
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  toTop && toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

  /* ---- Reveal on scroll ---- */
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('in'));
  }

  /* ---- Count-up numbers ---- */
  document.querySelectorAll('[data-count]').forEach((el) => {
    const end = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (reduce) { el.textContent = end + suffix; return; }
    const run = () => {
      const t0 = performance.now();
      const step = (t) => {
        const p = Math.min(1, (t - t0) / 1400);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3))) + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      const o = new IntersectionObserver((es) => { if (es[0].isIntersecting) { run(); o.disconnect(); } });
      o.observe(el);
    } else run();
  });

  /* ---- Falling dogwood petals (hero) ---- */
  const canvas = document.getElementById('petals');
  if (canvas && !reduce) {
    const ctx = canvas.getContext('2d');
    let w, h, petals = [];
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const resize = () => {
      w = canvas.clientWidth; h = canvas.clientHeight;
      canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.round(Math.min(34, w / 38));
      petals = Array.from({ length: n }, () => newPetal(true));
    };
    const newPetal = (anywhere) => ({
      x: Math.random() * w, y: anywhere ? Math.random() * h : -20,
      s: 6 + Math.random() * 9, vy: 0.35 + Math.random() * 0.8, vx: -0.3 + Math.random() * 0.6,
      r: Math.random() * Math.PI, vr: -0.02 + Math.random() * 0.04, sway: Math.random() * 100,
      pink: Math.random() < 0.35, a: 0.55 + Math.random() * 0.4,
    });
    const draw = (p) => {
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.globalAlpha = p.a;
      ctx.fillStyle = p.pink ? '#f4c3cd' : '#fffaf2';
      ctx.beginPath();
      ctx.moveTo(0, -p.s);
      ctx.bezierCurveTo(p.s * 0.9, -p.s * 0.8, p.s * 0.8, p.s * 0.6, 0, p.s);
      ctx.bezierCurveTo(-p.s * 0.8, p.s * 0.6, -p.s * 0.9, -p.s * 0.8, 0, -p.s);
      ctx.fill();
      ctx.fillStyle = 'rgba(181,87,59,.55)';
      ctx.beginPath(); ctx.arc(0, -p.s * 0.82, p.s * 0.12, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    };
    let visible = true;
    new IntersectionObserver((es) => { visible = es[0].isIntersecting; }).observe(canvas);
    const loop = (t) => {
      if (visible) {
        ctx.clearRect(0, 0, w, h);
        petals.forEach((p, i) => {
          p.sway += 0.01; p.x += p.vx + Math.sin(p.sway + t / 2000) * 0.4; p.y += p.vy; p.r += p.vr;
          if (p.y > h + 20 || p.x < -30 || p.x > w + 30) petals[i] = newPetal(false);
          draw(p);
        });
      }
      requestAnimationFrame(loop);
    };
    resize(); window.addEventListener('resize', resize); requestAnimationFrame(loop);
  }

  /* ---- Table of contents highlight ---- */
  const tocLinks = [...document.querySelectorAll('.toc a')];
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const map = new Map(tocLinks.map((a) => [a.getAttribute('href').slice(1), a]));
    const tio = new IntersectionObserver((es) => {
      es.forEach((en) => {
        if (en.isIntersecting) {
          tocLinks.forEach((a) => a.classList.remove('active'));
          const a = map.get(en.target.id); a && a.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    map.forEach((_, id) => { const h = document.getElementById(id); h && tio.observe(h); });
  }

  /* ---- Project finder (home + blog) ---- */
  document.querySelectorAll('[data-finder]').forEach((finder) => {
    const target = document.querySelector(finder.dataset.finder);
    if (!target) return;
    finder.addEventListener('click', (e) => {
      const b = e.target.closest('button'); if (!b) return;
      finder.querySelectorAll('button').forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      const tag = b.dataset.tag;
      target.querySelectorAll('[data-tags]').forEach((card) => {
        const show = tag === 'all' || card.dataset.tags.split(' ').includes(tag);
        card.classList.toggle('is-hidden', !show);
        if (show && !reduce) { card.animate([{ opacity: 0, transform: 'translateY(14px)' }, { opacity: 1, transform: 'none' }], { duration: 380, easing: 'cubic-bezier(.2,.8,.2,1)' }); }
      });
    });
  });

  /* ---- Copy link ---- */
  document.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', () => {
    const done = () => { const t = b.textContent; b.textContent = 'Copied!'; setTimeout(() => { b.textContent = t; }, 1600); };
    if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done, done); else done();
  }));

  /* ---- Contact / newsletter status messages ---- */
  const params = new URLSearchParams(location.search);
  const msg = document.querySelector('[data-form-status]');
  if (msg && params.has('sent')) {
    msg.hidden = false;
    msg.textContent = params.get('sent') === '1' ? 'Thanks! Your message is on its way - we usually reply within a few days.' : 'Sorry, something went wrong. Please email us directly at info@dogwooddiy.com.';
    if (params.get('sent') !== '1') msg.classList.add('err');
  }
})();
