/* Site-wide behavior: theme, header, effects, command palette, tool search, contact form. */
(function () {
  'use strict';
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const root = document.documentElement;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const tools = window.JM_TOOLS || [];
  const icons = window.JM_ICONS || {};
  const esc = v => String(v).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const svg = name => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${icons[name] || ''}</svg>`;
  window.JM = { svg, esc };

  $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

  // Theme
  const toggle = $('.theme-toggle');
  if (toggle) toggle.addEventListener('click', () => {
    const next = root.dataset.theme === 'light' ? 'dark' : 'light';
    root.dataset.theme = next;
    try { localStorage.setItem('jm-theme', next); } catch (e) { /* storage unavailable */ }
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', next === 'light' ? '#f5f6f8' : '#06080c');
  });

  // Header state + scroll progress
  const header = $('.header'), progress = $('.scroll-progress');
  let ticking = false;
  const onScroll = () => {
    ticking = false;
    const y = scrollY, max = document.documentElement.scrollHeight - innerHeight;
    header?.classList.toggle('scrolled', y > 8);
    progress?.style.setProperty('--progress', max > 0 ? Math.min(1, y / max) : 0);
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // Mobile menu
  const menu = $('.menu-toggle'), nav = $('#site-nav');
  if (menu && nav) {
    menu.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', e => { if (e.target.closest('a')) { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); } });
  }

  // Reveal on scroll
  const reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduced) {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(el => io.observe(el));
  } else reveals.forEach(el => el.classList.add('in'));

  // Count-up numbers
  const counters = $$('[data-count]');
  if (counters.length && 'IntersectionObserver' in window && !reduced) {
    const co = new IntersectionObserver(entries => entries.forEach(en => {
      if (!en.isIntersecting) return;
      co.unobserve(en.target);
      const el = en.target, end = Number(el.dataset.count), t0 = performance.now(), dur = 1200;
      if (!end) return;
      const step = now => {
        const p = Math.min(1, (now - t0) / dur), eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(end * eased);
        if (p < 1) requestAnimationFrame(step);
      };
      el.textContent = '0'; requestAnimationFrame(step);
    }), { threshold: 0.5 });
    counters.forEach(el => co.observe(el));
  }

  // Spotlight + tilt on cards, magnetic buttons
  if (fine && !reduced) {
    document.addEventListener('pointermove', e => {
      const card = e.target.closest('.tool-card, .role, .feature');
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    }, { passive: true });
    $$('[data-tilt], [data-tilt-strong]').forEach(el => {
      const max = el.hasAttribute('data-tilt-strong') ? 8 : 4;
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = `perspective(900px) rotateX(${(-y * max).toFixed(2)}deg) rotateY(${(x * max).toFixed(2)}deg) translateY(-3px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
    $$('[data-magnetic]').forEach(el => {
      el.addEventListener('pointermove', e => {
        const r = el.getBoundingClientRect();
        el.style.setProperty('--bx', `${((e.clientX - r.left) / r.width - 0.5) * 12}px`);
        el.style.setProperty('--by', `${((e.clientY - r.top) / r.height - 0.5) * 10}px`);
      });
      el.addEventListener('pointerleave', () => { el.style.setProperty('--bx', '0px'); el.style.setProperty('--by', '0px'); });
    });
  }

  // Scramble-text word rotator
  const glyphs = '!<>-_\\/[]{}—=+*^?#01';
  $$('.scramble').forEach(el => {
    const words = (el.dataset.words || el.textContent).split('|');
    if (words.length < 2 || reduced) return;
    let index = 0;
    const scrambleTo = word => new Promise(resolve => {
      const from = el.textContent, len = Math.max(from.length, word.length), queue = [];
      for (let i = 0; i < len; i++) queue.push({ from: from[i] || '', to: word[i] || '', start: Math.floor(Math.random() * 18), end: 18 + Math.floor(Math.random() * 18) });
      let frame = 0;
      const tick = () => {
        let out = '', done = 0;
        for (const q of queue) {
          if (frame >= q.end) { done++; out += q.to; }
          else if (frame >= q.start) out += glyphs[Math.floor(Math.random() * glyphs.length)];
          else out += q.from;
        }
        el.textContent = out;
        if (done === queue.length) resolve(); else { frame++; requestAnimationFrame(tick); }
      };
      tick();
    });
    const loop = async () => { index = (index + 1) % words.length; await scrambleTo(words[index]); setTimeout(loop, 2600); };
    setTimeout(loop, 2400);
  });

  // Fuzzy-ish tool search shared by palette and launcher
  const score = (tool, q) => {
    if (!q) return 1;
    const hay = `${tool.name} ${tool.short} ${tool.keywords} ${tool.cat}`.toLowerCase();
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    let s = 0;
    for (const t of terms) {
      if (tool.name.toLowerCase().includes(t)) s += 5;
      else if (tool.keywords.toLowerCase().includes(t)) s += 3;
      else if (hay.includes(t)) s += 1;
      else return 0;
    }
    return s;
  };
  const search = q => tools.map(t => [t, score(t, q)]).filter(x => x[1] > 0).sort((a, b) => b[1] - a[1]).map(x => x[0]);
  const item = (t, i, sel) => `<a class="palette-item" role="option" href="/tools/${t.slug}" id="opt-${t.slug}-${i}" aria-selected="${sel}" data-hue="${t.hue}"><span class="tool-icon">${svg(t.icon)}</span><div><strong>${esc(t.name)}</strong><small>${esc(t.short)}</small></div><span class="meta">${esc(t.cat)}</span></a>`;

  // Keyboard-navigable result list helper
  function listNav(input, list, getItems) {
    let active = 0;
    const paint = () => {
      const items = getItems();
      items.forEach((el, i) => el.setAttribute('aria-selected', String(i === active)));
      const el = items[active];
      if (el) { el.scrollIntoView({ block: 'nearest' }); input.setAttribute('aria-activedescendant', el.id); }
    };
    input.addEventListener('keydown', e => {
      const items = getItems();
      if (!items.length) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); active = (active + 1) % items.length; paint(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); active = (active - 1 + items.length) % items.length; paint(); }
      else if (e.key === 'Enter') { e.preventDefault(); items[active]?.click(); }
    });
    return { reset() { active = 0; paint(); } };
  }

  // Command palette (⌘K / Ctrl+K)
  let palette = null;
  function openPalette() {
    if (palette) return;
    const last = document.activeElement;
    palette = document.createElement('div');
    palette.className = 'palette';
    palette.innerHTML = `<div class="palette-box" role="dialog" aria-modal="true" aria-label="Search tools"><div class="palette-input">${svg('search')}<input type="text" placeholder="Search tools and pages…" aria-label="Search tools and pages" role="combobox" aria-expanded="true" aria-controls="palette-list" autocomplete="off"><kbd>Esc</kbd></div><div class="palette-list" id="palette-list" role="listbox"></div><div class="palette-foot"><span>↑↓ navigate</span><span>↵ open</span><span>esc close</span></div></div>`;
    document.body.append(palette);
    const input = $('input', palette), list = $('.palette-list', palette);
    const pages = [['Home', '/', 'arrow-right'], ['All tools', '/tools', 'layers'], ['About John Raymond', '/about', 'users'], ['Contact', '/contact', 'mail'], ['Suggest a tool', '/contact?topic=tool', 'message']];
    const render = () => {
      const q = input.value.trim(), results = search(q);
      let htmlOut = results.length ? `<div class="palette-group">Tools</div>${results.map((t, i) => item(t, i, false)).join('')}` : '';
      const pageHits = pages.filter(p => !q || p[0].toLowerCase().includes(q.toLowerCase()));
      if (pageHits.length) htmlOut += `<div class="palette-group">Pages</div>` + pageHits.map((p, i) => `<a class="palette-item" role="option" id="page-${i}" href="${p[1]}" aria-selected="false"><span class="tool-icon">${svg(p[2])}</span><div><strong>${esc(p[0])}</strong></div></a>`).join('');
      list.innerHTML = htmlOut || `<div class="palette-group">No matches — <a class="text-link" href="/contact?topic=tool">suggest this tool</a></div>`;
      nav.reset();
    };
    const nav = listNav(input, list, () => $$('.palette-item', list));
    const close = () => { palette?.remove(); palette = null; last?.focus?.(); };
    palette.addEventListener('click', e => { if (e.target === palette) close(); });
    palette.addEventListener('keydown', e => {
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') { e.preventDefault(); input.focus(); }
    });
    input.addEventListener('input', render);
    render(); input.focus();
  }
  $$('[data-palette]').forEach(b => b.addEventListener('click', openPalette));
  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); palette ? palette.remove() || (palette = null) : openPalette(); }
    const typing = /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName) || document.activeElement?.isContentEditable;
    if (e.key === '/' && !typing && !palette) {
      const launcher = $('[data-launcher] input');
      e.preventDefault();
      if (launcher) launcher.focus(); else openPalette();
    }
  });
  if (/Mac|iPhone|iPad/.test(navigator.platform)) $$('.kbd-btn kbd').forEach(k => { k.textContent = '⌘K'; });
  else $$('.kbd-btn kbd').forEach(k => { k.textContent = 'Ctrl K'; });

  // Hero launcher
  const launcher = $('[data-launcher]');
  if (launcher) {
    const input = $('input', launcher), list = $('.launcher-results', launcher);
    const nav = listNav(input, list, () => $$('.palette-item', list));
    const show = () => {
      const results = search(input.value.trim());
      list.innerHTML = results.length ? results.map((t, i) => item(t, i, i === 0)).join('') : `<div class="palette-group">No tool found — <a class="text-link" href="/contact?topic=tool">suggest it</a></div>`;
      list.hidden = false; input.setAttribute('aria-expanded', 'true'); nav.reset();
    };
    input.addEventListener('input', show);
    input.addEventListener('focus', show);
    input.addEventListener('keydown', e => { if (e.key === 'Escape') { list.hidden = true; input.blur(); } });
    document.addEventListener('click', e => { if (!launcher.contains(e.target)) { list.hidden = true; input.setAttribute('aria-expanded', 'false'); } });
  }

  // Toolbox filtering
  const toolSearch = $('#tool-search');
  if (toolSearch) {
    let category = 'all';
    const params = new URLSearchParams(location.search);
    if (params.get('q')) toolSearch.value = params.get('q');
    const filter = () => {
      const q = toolSearch.value.trim().toLowerCase();
      let count = 0;
      $$('#tool-grid .tool-card').forEach(card => {
        const show = (category === 'all' || card.dataset.category === category) && q.split(/\s+/).every(t => card.dataset.search.includes(t));
        card.hidden = !show; if (show) { count++; card.classList.add('in'); }
      });
      $('#tool-count').textContent = `${count} tool${count === 1 ? '' : 's'}, ready when you are.`;
      $('#no-tools').hidden = count > 0;
    };
    $$('[data-filter]').forEach(btn => btn.addEventListener('click', () => {
      category = btn.dataset.filter;
      $$('[data-filter]').forEach(b => b.setAttribute('aria-pressed', String(b === btn)));
      filter();
    }));
    toolSearch.addEventListener('input', filter);
    filter();
  }

  // Contact form
  const form = $('#contact-form');
  if (form) {
    form.elements.ts.value = String(Date.now());
    const topic = new URLSearchParams(location.search).get('topic');
    if (topic && form.querySelector(`#topic-${CSS.escape(topic)}`)) form.querySelector(`#topic-${CSS.escape(topic)}`).checked = true;
    if (topic === 'tool') form.elements.message.placeholder = 'Which tool would help you? Or what went wrong, on which page, and in which browser?';
    const status = $('#contact-status');
    form.addEventListener('submit', async e => {
      e.preventDefault();
      status.className = 'status-line';
      if (!form.checkValidity()) {
        const bad = [...form.elements].find(el => el.willValidate && !el.checkValidity());
        status.textContent = bad?.name === 'email' ? 'Please enter a valid email address.' : bad?.name === 'message' ? 'Please write a message of at least 10 characters.' : 'Please fill in your name, email and message.';
        status.classList.add('error'); bad?.focus(); return;
      }
      const data = Object.fromEntries(new FormData(form));
      const button = $('#contact-submit');
      button.disabled = true; status.textContent = 'Sending…';
      try {
        const res = await fetch('/api/contact.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
        const out = await res.json().catch(() => ({}));
        if (!res.ok || !out.ok) throw new Error(out.error || 'The message could not be sent. Please email autida@jmautida.com directly.');
        $('#form-body').hidden = true; $('#form-success').hidden = false;
      } catch (err) {
        status.textContent = err.message; status.classList.add('error');
      } finally { button.disabled = false; }
    });
  }
})();
