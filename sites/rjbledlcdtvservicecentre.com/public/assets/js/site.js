/* RJB LED LCD TV Service Centre — site behaviour.
   Mobile nav, header progress, scroll reveal, card spotlight, TV channel flip,
   symptom checker, LED/LCD comparison, counters, timeline fill. No dependencies. */
(() => {
  const doc = document.documentElement;
  doc.classList.remove('no-js');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

  /* ---------- mobile nav ---------- */
  const header = $('.site-header');
  const menuBtn = $('.menu-btn');
  const panel = $('#nav-panel');
  const mq = window.matchMedia('(max-width: 960px)');

  const setMenu = (open) => {
    if (!menuBtn || !panel) return;
    panel.classList.toggle('is-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('nav-open', open);
    if (open) {
      const first = panel.querySelector('a');
      if (first) setTimeout(() => first.focus({ preventScroll: true }), 50);
    }
  };
  if (menuBtn && panel) {
    menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
    panel.addEventListener('click', (e) => {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && panel.classList.contains('is-open')) { setMenu(false); menuBtn.focus(); }
    });
    const onChange = () => { if (!mq.matches) setMenu(false); };
    mq.addEventListener ? mq.addEventListener('change', onChange) : mq.addListener(onChange);
  }
  $$('.sub-toggle').forEach((btn) => {
    btn.addEventListener('click', () => {
      const sub = document.getElementById(btn.getAttribute('aria-controls'));
      const open = btn.getAttribute('aria-expanded') !== 'true';
      btn.setAttribute('aria-expanded', String(open));
      if (sub) sub.classList.toggle('is-open', open);
    });
  });

  /* ---------- header state, read progress, back-to-top ---------- */
  const toTop = $('.to-top');
  let ticking = false;
  const onScroll = () => {
    const y = window.scrollY;
    const max = doc.scrollHeight - window.innerHeight;
    if (header) {
      header.classList.toggle('scrolled', y > 10);
      header.style.setProperty('--progress', max > 0 ? (y / max).toFixed(4) : 0);
    }
    if (toTop) toTop.classList.toggle('show', y > 700);
    $$('.band > img').forEach((img) => {
      if (reduced) return;
      const r = img.parentElement.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      img.style.transform = `translateY(${(r.top * -0.15).toFixed(1)}px)`;
    });
    const tl = $('.timeline');
    if (tl) {
      const r = tl.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, (window.innerHeight * 0.8 - r.top) / (r.height + window.innerHeight * 0.3)));
      tl.style.setProperty('--fill', p.toFixed(3));
      $$('.step', tl).forEach((s, i, all) => s.classList.toggle('lit', p >= i / all.length + 0.05));
    }
    ticking = false;
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
  if (toTop) toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduced ? 'auto' : 'smooth' }));

  /* ---------- reveal on scroll + counters ---------- */
  const countUp = (el) => {
    const end = parseFloat(el.dataset.count);
    const suffix = el.dataset.suffix || '';
    if (reduced) { el.textContent = end + suffix; return; }
    const t0 = performance.now();
    const dur = 1400;
    const tick = (t) => {
      const k = Math.min(1, (t - t0) / dur);
      el.textContent = Math.round(end * (1 - Math.pow(1 - k, 3))) + suffix;
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        $$('[data-count]', en.target).forEach(countUp);
        if (en.target.matches('[data-count]')) countUp(en.target);
        io.unobserve(en.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    $$('.reveal, .stats').forEach((el) => io.observe(el));
  } else {
    $$('.reveal').forEach((el) => el.classList.add('in'));
  }

  /* ---------- card spotlight ---------- */
  $$('.card').forEach((card) => {
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });

  /* ---------- static noise canvas ---------- */
  const noise = (canvas) => {
    const ctx = canvas.getContext('2d');
    const w = (canvas.width = 160);
    const h = (canvas.height = 100);
    const img = ctx.createImageData(w, h);
    return () => {
      const d = img.data;
      for (let i = 0; i < d.length; i += 4) {
        const v = (Math.random() * 255) | 0;
        d[i] = d[i + 1] = d[i + 2] = v;
        d[i + 3] = 255;
      }
      ctx.putImageData(img, 0, 0);
    };
  };

  /* ---------- hero TV channel flip ---------- */
  const tv = $('.tv[data-channels]');
  if (tv) {
    const screen = $('.tv-screen', tv);
    const imgs = $$('img', screen);
    const osd = $('.tv-osd', tv);
    const canvas = $('canvas', screen);
    const draw = canvas ? noise(canvas) : null;
    let idx = 0;
    const show = (i) => {
      imgs.forEach((im, j) => im.classList.toggle('on', j === i));
      if (osd) osd.textContent = 'CH ' + String(i + 1).padStart(2, '0');
    };
    const flip = () => {
      if (document.hidden) return;
      idx = (idx + 1) % imgs.length;
      screen.classList.add('flip');
      let n = 0;
      const burst = () => {
        if (draw) draw();
        if (++n < 6) requestAnimationFrame(burst);
        else { show(idx); setTimeout(() => screen.classList.remove('flip'), 120); }
      };
      burst();
    };
    setTimeout(() => { tv.classList.add('ready'); show(0); }, reduced ? 0 : 900);
    if (!reduced && imgs.length > 1) setInterval(flip, 4200);
    tv.addEventListener('click', flip);
  }

  /* ---------- 404 static ---------- */
  const st = $('canvas.static');
  if (st) {
    const draw = noise(st);
    const loop = () => { draw(); if (!reduced) setTimeout(() => requestAnimationFrame(loop), 60); };
    loop();
  }

  /* ---------- symptom checker (tabs) ---------- */
  $$('[data-tabs]').forEach((root) => {
    const tabs = $$('[role="tab"]', root);
    const select = (tab, focus) => {
      tabs.forEach((t) => {
        const on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        const p = document.getElementById(t.getAttribute('aria-controls'));
        if (p) { p.hidden = !on; if (on) { p.classList.remove('anim'); void p.offsetWidth; p.classList.add('anim'); } }
      });
      if (focus) tab.focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(t));
      t.addEventListener('keydown', (e) => {
        const k = e.key;
        if (!['ArrowDown', 'ArrowRight', 'ArrowUp', 'ArrowLeft', 'Home', 'End'].includes(k)) return;
        e.preventDefault();
        let n = i;
        if (k === 'ArrowDown' || k === 'ArrowRight') n = (i + 1) % tabs.length;
        if (k === 'ArrowUp' || k === 'ArrowLeft') n = (i - 1 + tabs.length) % tabs.length;
        if (k === 'Home') n = 0;
        if (k === 'End') n = tabs.length - 1;
        select(tabs[n], true);
      });
    });
  });

  /* ---------- LED vs LCD comparison ---------- */
  $$('[data-compare]').forEach((root) => {
    const data = JSON.parse(root.dataset.compare);
    const btns = $$('.seg button', root);
    const diagram = $('.panel-diagram', root);
    const title = $('[data-c="title"]', root);
    const text = $('[data-c="text"]', root);
    const label = $('.label', diagram);
    const meters = $$('.meter .bar i', root);
    const lampWrap = $('.lamps', diagram);
    const layout = (mode) => {
      lampWrap.innerHTML = '';
      const add = (style) => { const l = document.createElement('i'); l.className = 'lamp'; Object.assign(l.style, style); lampWrap.appendChild(l); };
      if (mode === 'ccfl') [22, 40, 58, 76].forEach((t) => add({ top: t + '%' }));
      if (mode === 'edge') { add({ left: '9%' }); add({ right: '9%' }); }
      if (mode === 'full') for (let r = 0; r < 4; r++) for (let c = 0; c < 7; c++) add({ top: 20 + r * 18 + '%', left: 14 + c * 12 + '%' });
    };
    const set = (mode) => {
      const d = data[mode];
      btns.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
      diagram.dataset.mode = mode;
      layout(mode);
      title.textContent = d.title;
      text.textContent = d.text;
      label.textContent = d.label;
      meters.forEach((m, i) => m.style.setProperty('--v', d.scores[i] + '%'));
    };
    btns.forEach((b) => b.addEventListener('click', () => set(b.dataset.mode)));
    set(btns[0].dataset.mode);
  });

  /* ---------- contact form status from query string ---------- */
  const status = new URLSearchParams(location.search).get('sent');
  const box = $('#form-status');
  if (box && status) {
    box.hidden = false;
    box.className = 'alert ' + (status === '1' ? 'alert-ok' : 'alert-err');
    box.textContent = status === '1'
      ? 'Thanks — your repair request has been sent. We will reply by email shortly.'
      : 'Sorry, the message could not be sent. Please email info@rjbledlcdtvservicecentre.com directly.';
  }
})();
