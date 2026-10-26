/* Bastrop Roofing — site behavior, weather effects and interactive roofing tools.
   No framework, no build step. */
(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const money = (n) => '$' + Math.round(n).toLocaleString('en-US');
  const num = (n, d = 0) => Number(n).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });

  /* ------------------------------------------------------------ Header & nav */
  const header = $('.site-header');
  const nav = $('#main-nav');
  const menuBtn = $('.menu-btn');
  const setMenu = (open) => {
    if (!nav || !menuBtn) return;
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  menuBtn && menuBtn.addEventListener('click', () => setMenu(!nav.classList.contains('is-open')));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });
  document.addEventListener('click', (e) => {
    if (document.body.classList.contains('nav-open') && !nav.contains(e.target) && !menuBtn.contains(e.target)) setMenu(false);
  });
  $$('.drop-toggle').forEach((btn) => btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const li = btn.closest('li');
    const open = !li.classList.contains('is-open');
    $$('.has-drop.is-open').forEach((o) => { o.classList.remove('is-open'); $('.drop-toggle', o).setAttribute('aria-expanded', 'false'); });
    li.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', String(open));
  }));

  /* ------------------------------------------------------------ Scroll effects */
  const progress = $('.scroll-progress span');
  const toTop = $('.to-top');
  const onScroll = () => {
    const y = window.scrollY;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = (max > 0 ? (y / max) * 100 : 0) + '%';
    header && header.classList.toggle('is-stuck', y > 10);
    toTop && toTop.classList.toggle('is-visible', y > 700);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  toTop && toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }));

  const reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-visible'));
  }

  /* Count-up numbers */
  const counters = $$('[data-count]');
  const runCount = (el) => {
    const target = Number(el.dataset.count);
    const suffix = el.dataset.suffix || '+';
    if (reduceMotion) { el.textContent = target + suffix; return; }
    const start = performance.now();
    const step = (t) => {
      const p = Math.min(1, (t - start) / 1400);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))) + (p === 1 ? suffix : '');
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if (counters.length && 'IntersectionObserver' in window) {
    const co = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { runCount(en.target); co.unobserve(en.target); }
    }), { threshold: 0.6 });
    counters.forEach((c) => co.observe(c));
  } else counters.forEach(runCount);

  /* ------------------------------------------------------------ Weather canvas */
  class Weather {
    constructor(canvas) {
      this.c = canvas;
      this.ctx = canvas.getContext('2d');
      this.mode = canvas.dataset.weather || 'rain';
      this.hero = canvas.hasAttribute('data-hero');
      this.parts = [];
      this.visible = true;
      this.t = 0;
      this.resize();
      window.addEventListener('resize', () => this.resize());
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(([en]) => { this.visible = en.isIntersecting; if (this.visible) this.loop(); }).observe(canvas);
      }
      this.seed();
      this.loop();
    }
    resize() {
      const r = this.c.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      this.w = r.width; this.h = r.height;
      this.c.width = r.width * dpr; this.c.height = r.height * dpr;
      this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    count() {
      const area = (this.w * this.h) / 10000;
      const base = { rain: 1.6, hail: .55, wind: .5, sun: .22 }[this.mode];
      return Math.min(this.hero ? 420 : 160, Math.round(area * base * (this.hero ? 1 : .55)));
    }
    make(initial) {
      const m = this.mode;
      const p = { x: Math.random() * this.w, y: initial ? Math.random() * this.h : -20 - Math.random() * 60 };
      if (m === 'rain') Object.assign(p, { len: 10 + Math.random() * 16, v: 9 + Math.random() * 8, a: .15 + Math.random() * .35 });
      if (m === 'hail') Object.assign(p, { r: 1.5 + Math.random() * 3.2, v: 6 + Math.random() * 6, vy: 0, bounced: 0, a: .55 + Math.random() * .4 });
      if (m === 'wind') Object.assign(p, { x: initial ? Math.random() * this.w : -60, y: Math.random() * this.h, len: 40 + Math.random() * 120, v: 8 + Math.random() * 10, a: .06 + Math.random() * .16, wave: Math.random() * 6.28, leaf: Math.random() < .18 });
      if (m === 'sun') Object.assign(p, { y: initial ? Math.random() * this.h : this.h + 10, r: 1 + Math.random() * 2.5, v: .2 + Math.random() * .5, a: .1 + Math.random() * .4, drift: Math.random() * 6.28 });
      return p;
    }
    seed() { this.parts = Array.from({ length: this.count() }, () => this.make(true)); }
    set(mode) { this.mode = mode; this.seed(); }
    loop() {
      if (this.raf || !this.visible) return;
      const tick = () => {
        this.raf = null;
        if (!this.visible) return;
        this.draw();
        this.raf = requestAnimationFrame(tick);
      };
      this.raf = requestAnimationFrame(tick);
    }
    draw() {
      const { ctx, w, h } = this;
      this.t += 1;
      ctx.clearRect(0, 0, w, h);
      const m = this.mode;
      if (m === 'sun') {
        const g = ctx.createRadialGradient(w * .82, h * .12, 10, w * .82, h * .12, Math.max(w, h) * .6);
        const pulse = .2 + Math.sin(this.t / 60) * .04;
        g.addColorStop(0, `rgba(255,196,110,${pulse + .25})`);
        g.addColorStop(.25, `rgba(240,177,115,${pulse * .6})`);
        g.addColorStop(1, 'rgba(240,177,115,0)');
        ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
        ctx.save(); ctx.translate(w * .82, h * .12); ctx.rotate(this.t / 900);
        for (let i = 0; i < 12; i++) {
          ctx.rotate(Math.PI / 6);
          ctx.fillStyle = 'rgba(255,210,150,.05)';
          ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.max(w, h), -40); ctx.lineTo(Math.max(w, h), 40); ctx.fill();
        }
        ctx.restore();
      }
      for (let i = 0; i < this.parts.length; i++) {
        const p = this.parts[i];
        if (m === 'rain') {
          ctx.strokeStyle = `rgba(190,220,245,${p.a})`; ctx.lineWidth = 1.2;
          ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x - p.len * .25, p.y + p.len); ctx.stroke();
          p.y += p.v; p.x -= p.v * .25;
          if (p.y > h) {
            ctx.strokeStyle = `rgba(190,220,245,${p.a * .8})`;
            ctx.beginPath(); ctx.ellipse(p.x, h - 3, 6, 1.6, 0, 0, Math.PI * 2); ctx.stroke();
            this.parts[i] = this.make(false);
          }
        } else if (m === 'hail') {
          ctx.fillStyle = `rgba(235,245,255,${p.a})`;
          ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
          if (!p.bounced) { p.y += p.v; if (p.y > h - p.r) { p.bounced = 1; p.vy = -p.v * (.25 + Math.random() * .2); p.vx = (Math.random() - .5) * 3; } }
          else { p.vy += .5; p.y += p.vy; p.x += p.vx; p.a -= .02; if (p.a <= 0) this.parts[i] = this.make(false); }
          if (p.y > h + 10) this.parts[i] = this.make(false);
        } else if (m === 'wind') {
          p.wave += .05;
          const yy = p.y + Math.sin(p.wave) * 8;
          if (p.leaf) {
            ctx.save(); ctx.translate(p.x, yy); ctx.rotate(p.wave * 2);
            ctx.fillStyle = `rgba(201,129,61,${p.a + .35})`;
            ctx.fillRect(-7, -1, 14, 2);
            ctx.restore();
          } else {
            ctx.strokeStyle = `rgba(220,235,250,${p.a})`; ctx.lineWidth = 1.4;
            ctx.beginPath(); ctx.moveTo(p.x, yy);
            ctx.quadraticCurveTo(p.x - p.len / 2, yy - 6 * Math.sin(p.wave), p.x - p.len, yy); ctx.stroke();
          }
          p.x += p.v;
          if (p.x - p.len > w) this.parts[i] = this.make(false);
        } else if (m === 'sun') {
          p.drift += .01;
          ctx.fillStyle = `rgba(255,220,170,${p.a * (.6 + .4 * Math.sin(p.drift * 3))})`;
          ctx.beginPath(); ctx.arc(p.x + Math.sin(p.drift) * 10, p.y, p.r, 0, Math.PI * 2); ctx.fill();
          p.y -= p.v;
          if (p.y < -10) this.parts[i] = this.make(false);
        }
      }
      if (this.parts.length < this.count()) this.parts.push(this.make(false));
    }
  }

  const weathers = [];
  if (!reduceMotion) $$('.weather-canvas').forEach((c) => weathers.push(new Weather(c)));

  /* Lightning flashes in hero during rain/hail */
  const lightning = $('.lightning');
  let heroMode = 'rain';
  if (lightning && !reduceMotion) {
    const strike = () => {
      if (heroMode === 'rain' || heroMode === 'hail') {
        lightning.classList.remove('flash'); void lightning.offsetWidth; lightning.classList.add('flash');
      }
      setTimeout(strike, 5000 + Math.random() * 9000);
    };
    setTimeout(strike, 2500);
  }

  /* Hero weather switcher */
  const weatherInfo = {
    sun:  ['Sun & Heat', 'Months of 95°F+ days bake shingles and dry out sealants. Reflective metal roofing and balanced attic ventilation help a Bastrop roof last longer.', '/services/metal-roofing-bastrop-tx/', 'Bastrop metal roofing'],
    rain: ['Heavy Rain', 'Wind-driven rain finds every weak spot — cracked pipe boots, loose flashing and worn valleys. Bastrop Roofing traces leaks to the source.', '/services/roof-repair-bastrop-tx/', 'Roof leak repair'],
    hail: ['Spring Hail', 'Hail bruises shingles and dents metal in ways you cannot see from the ground. Get a free inspection after every major storm.', '/services/hail-damage-roof-repair-bastrop-tx/', 'Hail damage repair'],
    wind: ['High Wind', 'Gusts break shingle seals, peel back trim and drop pine limbs onto roofs across the Lost Pines.', '/services/storm-damage-roof-repair-bastrop-tx/', 'Storm damage repair'],
  };
  const heroCanvas = weathers.find((w) => w.hero);
  $$('[data-set-weather]').forEach((btn) => btn.addEventListener('click', () => {
    const mode = btn.dataset.setWeather;
    heroMode = mode;
    $$('[data-set-weather]').forEach((b) => b.classList.toggle('is-active', b === btn));
    heroCanvas && heroCanvas.set(mode);
    const [title, text, href, label] = weatherInfo[mode];
    $('[data-weather-title]').textContent = title;
    $('[data-weather-text]').textContent = text;
    const link = $('[data-weather-link]');
    link.href = href;
    link.firstChild.textContent = label + ' ';
  }));

  /* Rain sliding down standing seam panels */
  const drops = $('.seam-drops');
  if (drops && !reduceMotion) {
    for (let i = 0; i < 18; i++) {
      const d = document.createElement('i');
      d.style.left = (5.5 + Math.floor(Math.random() * 9) * 11.1) + '%';
      d.style.animationDuration = (1.2 + Math.random() * 1.6) + 's';
      d.style.animationDelay = (Math.random() * 3) + 's';
      drops.appendChild(d);
    }
  }

  /* ------------------------------------------------------------ Roof anatomy builder */
  const anatomy = $('[data-anatomy]');
  if (anatomy) {
    const layers = $$('.layer', anatomy);
    const items = $$('[data-layer-btn]');
    const show = (n, hot) => {
      layers.forEach((l) => {
        const i = Number(l.dataset.layer);
        l.classList.toggle('is-on', i <= n);
        l.classList.toggle('is-hot', i === hot);
      });
      items.forEach((it) => it.classList.toggle('is-active', Number(it.dataset.layerBtn) === hot));
    };
    let timer;
    const play = () => {
      clearInterval(timer);
      let n = -1;
      show(-1, -1);
      timer = setInterval(() => {
        n++;
        show(n, n);
        if (n >= layers.length - 1) { clearInterval(timer); setTimeout(() => show(layers.length - 1, -1), 900); }
      }, reduceMotion ? 10 : 650);
    };
    items.forEach((it) => $('button', it).addEventListener('click', () => { clearInterval(timer); const n = Number(it.dataset.layerBtn); show(n, n); }));
    $('[data-anatomy-play]', anatomy).addEventListener('click', play);
    if ('IntersectionObserver' in window) {
      const ao = new IntersectionObserver(([en]) => { if (en.isIntersecting) { play(); ao.disconnect(); } }, { threshold: .4 });
      ao.observe(anatomy);
    } else show(layers.length - 1, -1);
  }

  /* ------------------------------------------------------------ Tools */
  const fillRange = (r) => {
    const p = ((r.value - r.min) / (r.max - r.min)) * 100;
    r.style.setProperty('--fill', p + '%');
  };
  $$('.tool input[type=range]').forEach((r) => { fillRange(r); r.addEventListener('input', () => fillRange(r)); });

  const val = (root, name) => {
    const els = $$(`[name="${name}"]`, root);
    if (!els.length) return null;
    if (els[0].type === 'radio') { const c = els.find((e) => e.checked); return c ? c.value : null; }
    if (els[0].type === 'checkbox') return els[0].checked;
    return els[0].value;
  };
  const out = (root, key, text) => { const el = $(`[data-out="${key}"]`, root); if (el) el.textContent = text; return el; };
  const bump = (el) => { if (!el || reduceMotion) return; el.classList.remove('bump'); void el.offsetWidth; el.classList.add('bump'); };

  const tools = {
    /* Roof replacement cost */
    cost(root) {
      const rates = { arch: [4.5, 7], class4: [5.5, 8.5], rpanel: [6, 10], seam: [10, 16], stone: [9, 14] };
      const pitch = { low: [1.054, 1], med: [1.118, 1], steep: [1.25, 1.1], vsteep: [1.414, 1.2] };
      const calc = () => {
        const sqft = Number(val(root, 'sqft'));
        const stories = Number(val(root, 'stories'));
        const [mult, labor] = pitch[val(root, 'pitch')];
        const [lo, hi] = rates[val(root, 'material')];
        const footprint = (sqft / stories) * 1.12; // garage/porch & overhang allowance
        const area = footprint * mult;
        let low = area * lo * labor, high = area * hi * labor;
        if (stories === 2) { low *= 1.05; high *= 1.07; }
        if (val(root, 'layers') === '2') { low += area * .4; high += area * .7; }
        if (val(root, 'decking')) { low += area * .15 * 2.8; high += area * .15 * 4.2; }
        if (val(root, 'vent')) { low += 350; high += 900; }
        if (val(root, 'gutters')) { const lf = Math.sqrt(footprint) * 4 * .75; low += lf * 8; high += lf * 14; }
        out(root, 'sqft', num(sqft));
        bump(out(root, 'low', money(Math.round(low / 100) * 100)));
        bump(out(root, 'high', money(Math.round(high / 100) * 100)));
        out(root, 'area', num(area) + ' sq ft');
        out(root, 'squares', num(area / 100, 1));
        out(root, 'rate', '$' + lo.toFixed(2) + '–$' + hi.toFixed(2) + '/sq ft');
        const bar = $('[data-out="bar"]', root);
        if (bar) bar.style.width = Math.min(100, (high / 90000) * 100) + '%';
      };
      root.addEventListener('input', calc); root.addEventListener('change', calc); calc();
    },

    /* Metal vs shingle lifetime cost */
    compare(root) {
      const svg = $('.compare-chart', root);
      const calc = () => {
        const area = Number(val(root, 'area'));
        const years = Number(val(root, 'years'));
        const sr = Number(val(root, 'shingleRate')) || 5.75;
        const mr = Number(val(root, 'metalRate')) || 12.5;
        const sl = Math.max(5, Number(val(root, 'shingleLife')) || 20);
        const ml = Math.max(5, Number(val(root, 'metalLife')) || 50);
        const inf = (Number(val(root, 'inflation')) || 0) / 100;
        const save = Number(val(root, 'savings')) || 0;
        const series = (rate, life, savings) => {
          const pts = []; let total = 0, count = 0;
          for (let y = 0; y <= years; y++) {
            if (y % life === 0 && (y < years || y === 0)) { total += area * rate * Math.pow(1 + inf, y); count++; }
            if (y > 0) total -= savings;
            pts.push(total);
          }
          return { pts, total, count };
        };
        const s = series(sr, sl, 0), m = series(mr, ml, save);
        out(root, 'area', num(area)); out(root, 'years', years);
        bump(out(root, 'shingleTotal', money(s.total)));
        bump(out(root, 'metalTotal', money(m.total)));
        out(root, 'shingleCount', s.count + (s.count === 1 ? ' roof' : ' roofs') + ' over ' + years + ' yrs');
        out(root, 'metalCount', m.count + (m.count === 1 ? ' roof' : ' roofs') + ' over ' + years + ' yrs');
        let be = s.pts.findIndex((v, i) => i > 0 && m.pts[i] <= v);
        const diff = Math.abs(s.total - m.total);
        out(root, 'verdict', m.total < s.total
          ? `Metal saves about ${money(diff)} over ${years} years${be > 0 ? `, breaking even around year ${be}` : ''}.`
          : `Shingles cost about ${money(diff)} less over ${years} years. Metal pays off if you stay longer than a shingle roof lasts.`);
        // chart
        const W = 400, H = 200, pad = 34, max = Math.max(...s.pts, ...m.pts) * 1.08 || 1;
        const x = (i) => pad + (i / years) * (W - pad - 10);
        const y = (v) => H - 22 - (v / max) * (H - 36);
        const path = (pts) => pts.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
        $('.line-shingle', svg).setAttribute('d', path(s.pts));
        $('.line-metal', svg).setAttribute('d', path(m.pts));
        let grid = '', axis = '';
        for (let k = 0; k <= 4; k++) {
          const v = (max / 4) * k;
          grid += `<line x1="${pad}" x2="${W - 10}" y1="${y(v)}" y2="${y(v)}"/>`;
          axis += `<text x="2" y="${y(v) + 3}">$${Math.round(v / 1000)}k</text>`;
        }
        for (let k = 0; k <= years; k += years > 25 ? 10 : 5) axis += `<text x="${x(k) - 6}" y="${H - 6}">${k}y</text>`;
        $('.grid', svg).innerHTML = grid; $('.axis', svg).innerHTML = axis;
      };
      root.addEventListener('input', calc); calc();
    },

    /* Roof pitch & area */
    pitch(root) {
      const roof = $('.ps-roof', root), rise = $('.ps-rise', root);
      const calc = () => {
        const L = Number(val(root, 'length')) || 0, W = Number(val(root, 'width')) || 0;
        const oh = Number(val(root, 'overhang')) / 12;
        const p = Number(val(root, 'pitch'));
        const waste = Number(val(root, 'waste')) / 100;
        const mult = Math.sqrt(1 + Math.pow(p / 12, 2));
        const angle = Math.atan(p / 12) * 180 / Math.PI;
        const area = (L + oh * 2) * (W + oh * 2) * mult;
        const sq = (area * (1 + waste)) / 100;
        out(root, 'overhang', val(root, 'overhang'));
        out(root, 'pitch', p + '/12');
        bump(out(root, 'area', num(area)));
        out(root, 'angle', angle.toFixed(1) + '°');
        out(root, 'mult', mult.toFixed(3));
        out(root, 'squares', num(sq, 1));
        out(root, 'bundles', num(Math.ceil(sq * 3)));
        out(root, 'rolls', num(Math.ceil(area * 1.1 / 1000)));
        out(root, 'walk', p <= 6 ? 'Yes (≤6/12)' : p <= 9 ? 'With care' : 'Steep — harness');
        const peak = 124 - Math.min(110, (p / 12) * 130);
        roof.setAttribute('points', `20,124 150,${peak} 280,124`);
        rise.setAttribute('d', `M150 124 V ${peak}`);
        $('.ps-angle', root).textContent = angle.toFixed(1) + '°';
        $('.ps-rise-t', root).textContent = p + '"';
        $('.ps-rise-t', root).setAttribute('y', (124 + peak) / 2 + 4);
      };
      root.addEventListener('input', calc); root.addEventListener('change', calc); calc();
    },

    /* Repair or replace quiz */
    quiz(root) {
      const total = Number(root.dataset.total);
      const steps = $$('.quiz-step', root);
      const bar = $('.quiz-progress span', root);
      const answers = [];
      const go = (i) => {
        steps.forEach((s, k) => s.classList.toggle('is-current', k === i));
        bar.style.width = (Math.min(i, total) / total) * 100 + '%';
      };
      const finish = () => {
        const score = answers.reduce((a, b) => a + b, 0), max = total * 3, pct = score / max;
        const needle = $('.gauge-needle', root);
        needle.style.transform = 'rotate(-90deg)';
        requestAnimationFrame(() => requestAnimationFrame(() => { needle.style.transform = `rotate(${-90 + pct * 180}deg)`; }));
        let v, d;
        if (pct < .34) { v = 'A repair is likely the smart move'; d = 'Your roof sounds fundamentally healthy. A targeted repair should solve the problem and protect the rest of the roof. Book a free inspection to confirm and get a written repair price.'; }
        else if (pct < .62) { v = 'It could go either way — get it inspected'; d = 'Your answers point to a roof in the middle of its life. A repair may buy several good years, or replacement may be the better value. A hands-on inspection with photos will settle it.'; }
        else { v = 'Replacement is probably the better investment'; d = 'Age, widespread wear or repeated leaks suggest repairs will keep adding up. A new roof — shingle or metal — will likely cost less over time. Ask us about insurance if storms played a part.'; }
        out(root, 'verdict', v); out(root, 'detail', d);
        go(total);
      };
      $$('.quiz-option', root).forEach((btn) => btn.addEventListener('click', () => {
        const i = Number(btn.closest('.quiz-step').dataset.step);
        answers[i] = Number(btn.dataset.points);
        answers.length = i + 1;
        if (i + 1 >= total) finish(); else go(i + 1);
      }));
      $$('.quiz-back', root).forEach((b) => b.addEventListener('click', () => go(Number(b.closest('.quiz-step').dataset.step) - 1)));
      $('.quiz-restart', root).addEventListener('click', () => { answers.length = 0; go(0); });
    },

    /* Storm damage checklist */
    checklist(root) {
      const boxes = $$('input[type=checkbox]', root);
      const max = boxes.reduce((a, b) => a + Number(b.dataset.weight), 0);
      const calc = () => {
        const score = boxes.filter((b) => b.checked).reduce((a, b) => a + Number(b.dataset.weight), 0);
        const strong = boxes.some((b) => b.checked && Number(b.dataset.weight) === 3);
        $('[data-out="meter"]', root).style.width = (score ? Math.max(8, (score / (max * .5)) * 100) : 0) + '%';
        let level, advice;
        if (!score) { level = 'Nothing checked yet'; advice = 'Walk around the property and tick anything you notice. Stay off the roof — ground-level checks are enough.'; }
        else if (strong && score >= 6) { level = 'High — schedule an inspection now'; advice = 'Several strong signs of roof damage. Call (512) 297-7580 today; if water is coming in, ask about emergency tarping. Photograph everything before cleanup.'; }
        else if (strong || score >= 4) { level = 'Moderate — inspection recommended'; advice = 'You are seeing signs that often go with roof damage. Book a free inspection this week so any damage is documented while it is fresh.'; }
        else { level = 'Low — keep an eye on it'; advice = 'Minor signs only. Damage is possible but less likely. A free inspection gives peace of mind, especially if neighbors are filing claims.'; }
        out(root, 'level', level); out(root, 'advice', advice);
      };
      root.addEventListener('change', calc);
      const pr = $('[data-action="print"]', root);
      pr && pr.addEventListener('click', () => window.print());
      calc();
    },
  };
  $$('[data-tool]').forEach((root) => { const fn = tools[root.dataset.tool]; fn && fn(root); });

  /* ------------------------------------------------------------ Estimate form */
  $$('.estimate-form').forEach((form) => form.addEventListener('submit', (e) => {
    let ok = true;
    $$('[required]', form).forEach((f) => {
      const bad = !f.value.trim() || (f.type === 'tel' && f.value.replace(/\D/g, '').length < 7);
      f.classList.toggle('is-invalid', bad);
      if (bad) ok = false;
    });
    if (!ok) { e.preventDefault(); const first = $('.is-invalid', form); first && first.focus(); return; }
    const btn = $('button[type=submit]', form);
    btn.disabled = true; btn.firstChild.textContent = 'Sending… ';
  }));
})();
