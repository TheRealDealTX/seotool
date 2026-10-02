/* The Colony Public Adjuster — site behaviour (no dependencies) */
'use strict';
document.documentElement.classList.add('js');
(function () {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* ---------- Mobile navigation ---------- */
  const toggle = $('.menu-toggle'), nav = $('#main-nav'), backdrop = $('.nav-backdrop');
  function setNav(open) {
    if (!toggle || !nav) return;
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
    backdrop && backdrop.classList.toggle('show', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }
  toggle && toggle.addEventListener('click', () => setNav(toggle.getAttribute('aria-expanded') !== 'true'));
  backdrop && backdrop.addEventListener('click', () => setNav(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { setNav(false); $$('.nav-drop.open').forEach(d => d.classList.remove('open')); } });
  $$('.nav-drop > button').forEach(btn => btn.addEventListener('click', () => {
    const d = btn.parentElement, open = !d.classList.contains('open');
    d.classList.toggle('open', open); btn.setAttribute('aria-expanded', String(open));
  }));

  /* ---------- Hero headline word split ---------- */
  $$('.split-words').forEach(el => {
    let i = 0;
    const walk = node => {
      [...node.childNodes].forEach(child => {
        if (child.nodeType === 3) {
          const frag = document.createDocumentFragment();
          child.textContent.split(/(\s+)/).forEach(part => {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
            const w = document.createElement('span'); w.className = 'w';
            const inner = document.createElement('span'); inner.textContent = part; inner.style.setProperty('--i', i++);
            w.appendChild(inner); frag.appendChild(w);
          });
          child.replaceWith(frag);
        } else if (child.nodeType === 1 && !child.classList.contains('kw')) walk(child);
      });
    };
    walk(el);
  });

  /* ---------- Reveal on scroll ---------- */
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
    $$('[data-reveal]').forEach(el => io.observe(el));
    $$('[data-stagger]').forEach(group => [...group.children].forEach((c, i) => {
      if (!c.hasAttribute('data-reveal')) c.setAttribute('data-reveal', '');
      c.style.setProperty('--d', i * 90); io.observe(c);
    }));
  } else {
    $$('[data-reveal],[data-stagger]>*').forEach(el => el.classList.add('in'));
  }

  /* ---------- Count-up numbers ---------- */
  const fmt = n => n.toLocaleString('en-US');
  function countUp(el) {
    const target = parseFloat(el.dataset.count), suffix = el.dataset.suffix || '', prefix = el.dataset.prefix || '';
    if (reduce) { el.textContent = prefix + fmt(target) + suffix; return; }
    const start = performance.now(), dur = 1600;
    const tick = t => {
      const p = Math.min(1, (t - start) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + fmt(Math.round(target * e)) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
  if ('IntersectionObserver' in window) {
    const co = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); } }), { threshold: .6 });
    $$('[data-count]').forEach(el => co.observe(el));
  }

  /* ---------- Scroll-linked effects (one rAF loop) ---------- */
  const header = $('.site-header'), bar = $('.scroll-progress'), top = $('.back-top');
  const ring = top && top.querySelector('circle.fg');
  const parallax = $$('[data-parallax]');
  const timelines = $$('.timeline');
  let ticking = false;
  function onScroll() {
    const y = scrollY, h = document.documentElement.scrollHeight - innerHeight, p = h > 0 ? Math.min(1, y / h) : 0;
    header && header.classList.toggle('scrolled', y > 30);
    bar && bar.style.setProperty('--sp', p);
    if (top) { top.classList.toggle('show', y > 700); if (ring) ring.style.strokeDashoffset = String(151 - 151 * p); }
    if (!reduce) {
      parallax.forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > innerHeight) return;
        const speed = parseFloat(el.dataset.parallax) || .15;
        const offset = (r.top + r.height / 2 - innerHeight / 2) * -speed;
        el.style.transform = 'translate3d(0,' + offset.toFixed(1) + 'px,0) scale(1.12)';
      });
    }
    timelines.forEach(tl => {
      const r = tl.getBoundingClientRect();
      const prog = Math.max(0, Math.min(1, (innerHeight * .85 - r.top) / (r.height + innerHeight * .35)));
      tl.style.setProperty('--tp', prog.toFixed(3));
      const steps = $$('.step', tl);
      steps.forEach((s, i) => s.classList.toggle('lit', prog >= (i + .2) / steps.length || reduce));
    });
    ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  addEventListener('resize', onScroll); onScroll();
  top && top.addEventListener('click', () => scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

  /* ---------- Sticky story (image swaps with text) ---------- */
  const story = $('.story');
  if (story && 'IntersectionObserver' in window) {
    const imgs = $$('.story-media img', story), steps = $$('.story-step', story);
    const so = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      const idx = steps.indexOf(e.target);
      steps.forEach((s, i) => s.classList.toggle('on', i === idx));
      imgs.forEach((im, i) => im.classList.toggle('on', i === idx));
    }), { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(s => so.observe(s));
  }

  /* ---------- Glossary flip cards (tap support) ---------- */
  $$('.flip').forEach(f => f.addEventListener('click', () => f.setAttribute('aria-pressed', f.getAttribute('aria-pressed') === 'true' ? 'false' : 'true')));

  /* ---------- Claim guide ---------- */
  const guide = $('#claim-guide');
  if (guide && window.TC_GUIDE) {
    const out = $('#guide-out');
    const render = () => {
      const dmg = (guide.querySelector('input[name=damage]:checked') || {}).value || 'wind';
      const st = (guide.querySelector('input[name=stage]:checked') || {}).value || 'preparing';
      const d = window.TC_GUIDE.damage[dmg], s = window.TC_GUIDE.stage[st];
      out.classList.add('swap');
      setTimeout(() => {
        out.innerHTML = '<span class="pill">' + d.label + ' · ' + s.label + '</span>' +
          '<h3>' + s.title.replace('{d}', d.label.toLowerCase()) + '</h3><p>' + s.text + '</p>' +
          '<ul>' + d.items.concat(s.items).map(i => '<li>' + i + '</li>').join('') + '</ul>' +
          '<p class="small">' + d.safety + '</p>' +
          '<div class="toolbar"><a class="button small" href="' + d.url + '">' + d.cta + '</a>' +
          '<a class="button small ghost" href="' + s.url + '">' + s.cta + '</a></div>';
        out.classList.remove('swap');
      }, reduce ? 0 : 220);
    };
    guide.addEventListener('change', render); render();
  }

  /* ---------- Blog filter ---------- */
  const search = $('#blog-search');
  if (search) {
    let cat = 'All';
    const run = () => {
      const q = search.value.trim().toLowerCase(); let n = 0;
      $$('.blog-card').forEach(c => {
        const show = (cat === 'All' || c.dataset.category === cat) && c.textContent.toLowerCase().includes(q);
        c.hidden = !show; if (show) n++;
      });
      $('#article-count').textContent = n + (n === 1 ? ' guide' : ' guides');
      $('#filter-empty').hidden = n > 0;
    };
    search.addEventListener('input', run);
    $$('[data-filter]').forEach(b => b.addEventListener('click', () => {
      cat = b.dataset.filter; $$('[data-filter]').forEach(x => x.setAttribute('aria-pressed', String(x === b))); run();
    }));
  }

  /* ---------- Article table of contents highlight ---------- */
  const tocLinks = $$('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const map = new Map(tocLinks.map(a => [a.getAttribute('href').slice(1), a]));
    const to = new IntersectionObserver(es => es.forEach(e => {
      if (e.isIntersecting) { tocLinks.forEach(a => a.classList.remove('active')); const a = map.get(e.target.id); a && a.classList.add('active'); }
    }), { rootMargin: '-20% 0px -70% 0px' });
    map.forEach((_, id) => { const el = document.getElementById(id); el && to.observe(el); });
  }

  /* ---------- Hero quick-start select ---------- */
  const quick = $('#quick-start');
  quick && quick.addEventListener('submit', e => {
    e.preventDefault();
    const v = quick.elements.type.value;
    location.href = '/contact/?type=' + encodeURIComponent(v) + '#request';
  });

  /* ---------- Contact form ---------- */
  const form = $('#contact-form');
  if (form) {
    const status = $('#form-status');
    const params = new URLSearchParams(location.search);
    const preset = params.get('type');
    if (preset && form.elements.claim_type) {
      [...form.elements.claim_type.options].forEach(o => { if (o.value === preset) o.selected = true; });
    }
    if (form.elements.ts) form.elements.ts.value = String(Date.now());
    fetch('/send-mail.php', { credentials: 'same-origin', headers: { Accept: 'application/json' } })
      .then(r => r.json()).then(d => { if (d.csrf) form.elements.csrf.value = d.csrf; }).catch(() => {});
    form.addEventListener('submit', e => {
      e.preventDefault();
      status.className = 'form-status'; status.textContent = '';
      if (!form.checkValidity()) { form.reportValidity(); return; }
      const btn = form.querySelector('button[type=submit]'); btn.disabled = true; const label = btn.innerHTML; btn.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), credentials: 'same-origin', headers: { Accept: 'application/json' } })
        .then(r => r.json().catch(() => ({ ok: false, message: 'Unexpected server response.' })))
        .then(d => {
          status.className = 'form-status ' + (d.ok ? 'ok' : 'err');
          status.textContent = d.message || (d.ok ? 'Thank you. We received your request.' : 'Something went wrong. Please call us.');
          if (d.ok) form.reset();
          if (d.csrf) form.elements.csrf.value = d.csrf;
        })
        .catch(() => { status.className = 'form-status err'; status.textContent = 'We could not send your request. Please call (832) 503-5866 or email info@thecolonypublicadjuster.com.'; })
        .finally(() => { btn.disabled = false; btn.innerHTML = label; status.focus(); });
    });
  }

  /* ---------- Year ---------- */
  $$('[data-year]').forEach(el => el.textContent = new Date().getFullYear());
})();
