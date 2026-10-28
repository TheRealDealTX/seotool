/* Home page effects: interactive particle field and the typing terminal. */
(function () {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Particle constellation that leans toward the pointer.
  const canvas = document.getElementById('hero-canvas');
  if (canvas && !reduced) {
    const ctx = canvas.getContext('2d');
    let w = 0, h = 0, dpr = 1, points = [], running = true, raf = 0;
    const mouse = { x: -9999, y: -9999 };
    const color = () => getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#4ff0b4';
    let accent = color();
    const resize = () => {
      const r = canvas.getBoundingClientRect();
      dpr = Math.min(2, devicePixelRatio || 1); w = r.width; h = r.height;
      canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.min(110, Math.floor((w * h) / 13000));
      points = Array.from({ length: count }, () => ({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - 0.5) * 0.35, vy: (Math.random() - 0.5) * 0.35, r: Math.random() * 1.6 + 0.6 }));
    };
    const draw = () => {
      ctx.clearRect(0, 0, w, h);
      for (const p of points) {
        const dx = mouse.x - p.x, dy = mouse.y - p.y, d2 = dx * dx + dy * dy;
        if (d2 < 32000) { p.vx += dx * 0.00003; p.vy += dy * 0.00003; }
        p.vx *= 0.995; p.vy *= 0.995;
        p.vx = Math.max(-0.8, Math.min(0.8, p.vx)); p.vy = Math.max(-0.8, Math.min(0.8, p.vy));
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
      }
      ctx.strokeStyle = accent; ctx.fillStyle = accent;
      for (let i = 0; i < points.length; i++) {
        const a = points[i];
        for (let j = i + 1; j < points.length; j++) {
          const b = points[j], dx = a.x - b.x, dy = a.y - b.y, d = dx * dx + dy * dy;
          if (d < 14000) { ctx.globalAlpha = (1 - d / 14000) * 0.22; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        const md = (mouse.x - a.x) ** 2 + (mouse.y - a.y) ** 2;
        if (md < 26000) { ctx.globalAlpha = (1 - md / 26000) * 0.5; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
        ctx.globalAlpha = 0.55; ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, Math.PI * 2); ctx.fill();
      }
      ctx.globalAlpha = 1;
      if (running) raf = requestAnimationFrame(draw);
    };
    const hero = canvas.parentElement;
    hero.addEventListener('pointermove', e => { const r = canvas.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    hero.addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });
    new IntersectionObserver(([en]) => {
      const vis = en.isIntersecting;
      if (vis && !running) { running = true; raf = requestAnimationFrame(draw); } else if (!vis) { running = false; cancelAnimationFrame(raf); }
    }).observe(canvas);
    new MutationObserver(() => { accent = color(); }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    addEventListener('resize', resize);
    resize(); draw();
  }

  // Typing terminal
  const term = document.getElementById('terminal');
  if (term) {
    const scripts = [
      [['cmd', 'jm convert hero.jpg team.png --to webp -q 80'], ['out', '<span class="c">↳ hero.jpg</span>  2.4 MB → <span class="ok">566 KB  −76%</span>'], ['out', '<span class="c">↳ team.png</span>  1.1 MB → <span class="ok">188 KB  −83%</span>'], ['out', '<span class="ok">✓</span> 2 files converted in 0.4s · nothing uploaded']],
      [['cmd', 'jm audit https://yoursite.com'], ['out', '<span class="ok">✓</span> title        <span class="s">54 chars</span>'], ['out', '<span class="ok">✓</span> description  <span class="s">148 chars</span>'], ['out', '<span class="k">!</span> h1           <span class="s">missing</span> → add one'], ['out', '<span class="ok">SEO score 92/100</span>']],
      [['cmd', 'jm shift --start 19:30 --hours 9.3 --break 30'], ['out', 'logout   <span class="ok">5:18 AM</span> (next day)'], ['out', 'in Texas <span class="s">4:18 PM CDT</span>'], ['out', '<span class="c">countdown started · notify on logout</span>']],
      [['cmd', 'jm utm --source newsletter --campaign fall-sale'], ['out', '<span class="s">https://site.com/?utm_source=newsletter</span>'], ['out', '<span class="s">&amp;utm_medium=email&amp;utm_campaign=fall-sale</span>'], ['out', '<span class="ok">✓</span> copied to clipboard']],
    ];
    const sleep = ms => new Promise(r => setTimeout(r, ms));
    const line = htmlText => { const s = document.createElement('span'); s.className = 'ln'; s.innerHTML = htmlText; term.append(s); return s; };
    const run = async () => {
      if (reduced) { scripts[0].forEach(([k, t]) => line(k === 'cmd' ? `<span class="p">➜</span> ${t}` : t)); return; }
      let n = 0;
      while (true) {
        const scriptLines = scripts[n++ % scripts.length];
        while (term.children.length > 2) term.lastElementChild.remove();
        await sleep(500);
        for (const [kind, text] of scriptLines) {
          if (kind === 'cmd') {
            const el = line('<span class="p">➜</span> <span class="k">~</span> ');
            const caret = document.createElement('span'); caret.className = 'term-caret'; el.append(caret);
            for (const ch of text) { caret.before(ch); await sleep(28 + Math.random() * 45); }
            await sleep(380); caret.remove();
          } else { line(text); await sleep(240); }
        }
        await sleep(3200);
      }
    };
    run();
  }
})();
