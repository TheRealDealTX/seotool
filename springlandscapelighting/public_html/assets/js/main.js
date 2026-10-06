/* Spring Landscape Lighting — site interactions */
(() => {
  const d = document, root = d.documentElement, body = d.body;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(pointer: fine)').matches;
  const $ = (s, c = d) => c.querySelector(s), $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  /* ---------- split headings into words ---------- */
  $$('[data-split]').forEach(el => {
    let i = 0;
    const walk = node => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(' ')); return; }
            const w = d.createElement('span'); w.className = 'w';
            const s = d.createElement('span'); s.textContent = part; s.style.setProperty('--i', i++);
            w.appendChild(s); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
      });
    };
    walk(el);
  });

  /* ---------- reveal on scroll ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px', threshold: .08 });
  $$('[data-reveal],[data-split],.process__step,.timeline__item').forEach(el => io.observe(el));

  /* ---------- header, progress, parallax, to-top ---------- */
  const hdr = $('[data-hdr]'), bar = $('.progress span'), top = $('.totop');
  const para = $$('[data-parallax]');
  let lastY = 0, ticking = false;
  const onScroll = () => {
    const y = scrollY, h = root.scrollHeight - innerHeight;
    hdr && hdr.classList.toggle('is-scrolled', y > 30);
    hdr && hdr.classList.toggle('is-hidden', y > 500 && y > lastY + 4 && !body.classList.contains('nav-open'));
    if (y < lastY - 4) hdr && hdr.classList.remove('is-hidden');
    lastY = y;
    if (bar) bar.style.transform = `scaleX(${h > 0 ? y / h : 0})`;
    top && top.classList.toggle('is-on', y > innerHeight * 1.2);
    if (!reduce) para.forEach(el => {
      const r = el.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) return;
      el.style.transform = `translate3d(0,${(r.top * -1) * parseFloat(el.dataset.parallax || .2)}px,0)`;
    });
    dusk && dusk();
    timeline && timeline();
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', onScroll);
  top && top.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

  /* ---------- mobile drawer ---------- */
  const burger = $('.burger'), drawer = $('#drawer');
  burger && burger.addEventListener('click', () => {
    const open = body.classList.toggle('nav-open');
    burger.setAttribute('aria-expanded', open); drawer.setAttribute('aria-hidden', !open);
    body.style.overflow = open ? 'hidden' : '';
  });
  drawer && drawer.addEventListener('click', e => { if (e.target.closest('a')) { body.classList.remove('nav-open'); body.style.overflow = ''; } });

  /* ---------- cursor glow + hero lantern ---------- */
  const glow = $('.cursor-glow');
  if (fine && glow && !reduce) {
    addEventListener('pointermove', e => {
      body.classList.add('has-cursor');
      glow.style.transform = `translate3d(${e.clientX}px,${e.clientY}px,0)`;
    }, { passive: true });
    d.addEventListener('pointerleave', () => body.classList.remove('has-cursor'));
  }
  const hero = $('.hero');
  if (hero) {
    const hint = $('.hero__lamp', hero);
    let tx = 70, ty = 45, cx = 70, cy = 45, auto = true, t0 = performance.now(), r = 0, rt = Math.max(260, innerWidth * .26);
    hero.addEventListener('pointermove', e => {
      const b = hero.getBoundingClientRect();
      tx = (e.clientX - b.left) / b.width * 100; ty = (e.clientY - b.top) / b.height * 100; auto = false;
      hint && (hint.style.opacity = 0);
    });
    hero.addEventListener('pointerleave', () => { auto = true; });
    const loop = now => {
      if (auto) { const t = (now - t0) / 1000; tx = 62 + Math.sin(t * .45) * 18; ty = 45 + Math.sin(t * .7) * 14; }
      cx += (tx - cx) * .08; cy += (ty - cy) * .08; r += (rt - r) * .04;
      hero.style.setProperty('--mx', cx + '%'); hero.style.setProperty('--my', cy + '%'); hero.style.setProperty('--r', r + 'px');
      if (scrollY < innerHeight * 1.2) requestAnimationFrame(loop); else setTimeout(() => requestAnimationFrame(loop), 300);
    };
    reduce ? (hero.style.setProperty('--r', '2000px')) : requestAnimationFrame(loop);
  }

  /* ---------- fireflies ---------- */
  $$('canvas.fireflies').forEach(cv => {
    if (reduce) return;
    const ctx = cv.getContext('2d'); let w, h, dpr, flies = [], vis = false;
    const n = +cv.dataset.count || 30;
    const size = () => { dpr = Math.min(2, devicePixelRatio || 1); w = cv.offsetWidth; h = cv.offsetHeight; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
    size(); addEventListener('resize', size);
    for (let i = 0; i < n; i++) flies.push({ x: Math.random() * w, y: h * .35 + Math.random() * h * .65, r: 1 + Math.random() * 2.2, a: Math.random() * 6.28, s: .15 + Math.random() * .45, p: Math.random() * 6.28 });
    new IntersectionObserver(es => { vis = es[0].isIntersecting; if (vis) requestAnimationFrame(draw); }).observe(cv);
    function draw(t) {
      if (!vis) return;
      ctx.clearRect(0, 0, w, h);
      flies.forEach(f => {
        f.a += (Math.random() - .5) * .25; f.x += Math.cos(f.a) * f.s; f.y += Math.sin(f.a) * f.s - .05;
        if (f.x < -10) f.x = w + 10; if (f.x > w + 10) f.x = -10; if (f.y < h * .2) f.y = h + 5; if (f.y > h + 10) f.y = h * .3;
        const o = .25 + .75 * Math.max(0, Math.sin(t / 700 + f.p));
        const g = ctx.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r * 7);
        g.addColorStop(0, `rgba(255,214,130,${o})`); g.addColorStop(.25, `rgba(255,190,90,${o * .45})`); g.addColorStop(1, 'rgba(255,170,60,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(f.x, f.y, f.r * 7, 0, 6.28); ctx.fill();
      });
      requestAnimationFrame(draw);
    }
  });

  /* ---------- tilt + spotlight cards, magnetic buttons ---------- */
  if (fine && !reduce) {
    $$('[data-tilt]').forEach(el => {
      el.addEventListener('pointermove', e => {
        const b = el.getBoundingClientRect(), x = (e.clientX - b.left) / b.width, y = (e.clientY - b.top) / b.height;
        el.style.transform = `perspective(900px) rotateX(${(.5 - y) * 6}deg) rotateY(${(x - .5) * 8}deg) translateY(-4px)`;
        el.style.setProperty('--px', x * 100 + '%'); el.style.setProperty('--py', y * 100 + '%');
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
    $$('[data-magnetic]').forEach(el => {
      el.addEventListener('pointermove', e => {
        const b = el.getBoundingClientRect();
        el.style.setProperty('--bx', (e.clientX - b.left - b.width / 2) * .22 + 'px');
        el.style.setProperty('--by', (e.clientY - b.top - b.height / 2) * .3 + 'px');
      });
      el.addEventListener('pointerleave', () => { el.style.setProperty('--bx', '0px'); el.style.setProperty('--by', '0px'); });
    });
  }

  /* ---------- counters ---------- */
  const cio = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return; cio.unobserve(e.target);
    const el = e.target, end = parseFloat(el.dataset.countTo), dec = (el.dataset.countTo.split('.')[1] || '').length, t0 = performance.now(), dur = 1600;
    const step = now => { const p = Math.min(1, (now - t0) / dur), v = end * (1 - Math.pow(1 - p, 3)); el.textContent = v.toFixed(dec); if (p < 1) requestAnimationFrame(step); };
    reduce ? (el.textContent = end) : requestAnimationFrame(step);
  }), { threshold: .5 });
  $$('[data-count-to]').forEach(el => cio.observe(el));

  /* ---------- before / after ---------- */
  $$('.ba').forEach(ba => {
    const input = $('input', ba);
    const set = v => { ba.style.setProperty('--pos', v + '%'); };
    input.addEventListener('input', () => set(input.value));
    let shown = false;
    new IntersectionObserver(es => { if (es[0].isIntersecting && !shown && !reduce) { shown = true; let t0 = performance.now();
      const a = now => { const p = Math.min(1, (now - t0) / 1800), v = 50 + Math.sin(p * Math.PI * 2) * 30 * (1 - p); set(v); input.value = v; if (p < 1) requestAnimationFrame(a); };
      requestAnimationFrame(a); } }, { threshold: .6 }).observe(ba);
  });

  /* ---------- dusk to night scroll scene ---------- */
  const duskEl = $('.dusk');
  const lerp = (a, b, t) => a + (b - a) * t;
  const mix = (c1, c2, t) => `rgb(${c1.map((v, i) => Math.round(lerp(v, c2[i], t))).join(',')})`;
  const dusk = duskEl ? () => {
    const r = duskEl.getBoundingClientRect(), total = r.height - innerHeight;
    const p = clamp(-r.top / total, 0, 1);
    const sky = $('.dusk__sky', duskEl), sc = $('.scene', duskEl);
    const n = clamp(p / .3, 0, 1);
    sky.style.setProperty('--sky1', mix([74, 104, 140], [3, 8, 14], n));
    sky.style.setProperty('--sky2', mix([233, 164, 106], [8, 20, 26], n));
    sky.style.setProperty('--sky3', mix([244, 194, 122], [14, 30, 30], n));
    duskEl.style.setProperty('--stars', clamp((p - .15) / .25, 0, 1));
    sc && sc.style.setProperty('--dark', n);
    const groups = ['arch', 'path', 'tree', 'patio'];
    const stage = clamp(Math.floor((p - .22) / .17), -1, 3);
    groups.forEach((g, i) => {
      const local = clamp((p - .22 - i * .17) / .1, 0, 1);
      $$('.lt-' + g, duskEl).forEach(el => el.style.opacity = local);
    });
    sc && sc.classList.toggle('win-on', p > .2);
    $$('.dusk__step', duskEl).forEach((s, i) => s.classList.toggle('is-on', i === stage + 1));
    $$('.dusk__bar span', duskEl).forEach((s, i) => s.style.setProperty('--f', clamp((p - .22 - i * .17) / .17, 0, 1)));
  } : null;

  /* ---------- process timeline ---------- */
  const tl = $('.timeline');
  const timeline = tl ? () => {
    const r = tl.getBoundingClientRect(); const p = clamp((innerHeight * .6 - r.top) / r.height, 0, 1);
    tl.style.setProperty('--tl', p * 100 + '%');
  } : null;

  /* ---------- TOC highlight ---------- */
  const tocLinks = $$('.toc a');
  if (tocLinks.length) {
    const map = new Map(tocLinks.map(a => [a.getAttribute('href').slice(1), a]));
    const tio = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { tocLinks.forEach(a => a.classList.remove('is-on')); map.get(e.target.id)?.classList.add('is-on'); }
    }), { rootMargin: '-20% 0px -70% 0px' });
    map.forEach((a, id) => { const h = d.getElementById(id); h && tio.observe(h); });
  }

  /* ---------- copy link ---------- */
  $$('[data-copy]').forEach(b => b.addEventListener('click', () => {
    navigator.clipboard?.writeText(location.href).then(() => { b.title = 'Link copied'; b.classList.add('is-on'); });
  }));

  /* ---------- quote forms (AJAX with graceful fallback) ---------- */
  $$('[data-qform]').forEach(f => f.addEventListener('submit', async e => {
    const st = $('.qform__status', f);
    const req = $$('[required]', f).find(i => !i.value.trim());
    if (req) { e.preventDefault(); st.className = 'qform__status err'; st.textContent = 'Please fill in your name, phone and email.'; req.focus(); return; }
    if (!window.fetch) return;
    e.preventDefault();
    const btn = $('button[type=submit]', f); btn.disabled = true; btn.querySelector('span').textContent = 'Sending…';
    try {
      const res = await fetch(f.action, { method: 'POST', body: new FormData(f), headers: { Accept: 'application/json' } });
      const j = await res.json();
      if (!j.ok) throw new Error(j.error || 'Something went wrong.');
      f.classList.add('is-sent'); st.className = 'qform__status ok';
      st.innerHTML = 'Thank you! Your request is in. We will be in touch shortly to talk through your project. Need us sooner? Call <a href="tel:+12817047210">(281) 704-7210</a>.';
      window.gtag && gtag('event', 'generate_lead');
    } catch (err) {
      st.className = 'qform__status err'; st.textContent = err.message + ' You can also call (281) 704-7210.';
      btn.disabled = false; btn.querySelector('span').textContent = 'Request My Free Consultation';
    }
  }));

  onScroll();
})();
