/* Color contrast checker: WCAG 2 ratios, APCA Lc, nearest accessible fixes, CVD simulation, palette matrix. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, copy, store, btn, tabs, tabBar, tabPanel, debounce, app } = window.JT;

  // ---------- Color math ----------
  const probe = document.createElement('span');
  function parse(input) {
    const v = String(input).trim();
    if (!v) return null;
    let m = v.match(/^#?([\da-f]{3,8})$/i);
    if (m && [3, 4, 6, 8].includes(m[1].length)) {
      let h = m[1]; if (h.length <= 4) h = [...h].map(c => c + c).join('');
      return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16));
    }
    probe.style.color = ''; probe.style.color = v;
    if (!probe.style.color) return null;
    document.body.append(probe);
    const rgb = getComputedStyle(probe).color.match(/[\d.]+/g)?.slice(0, 3).map(Number);
    probe.remove();
    return rgb && rgb.length === 3 ? rgb.map(Math.round) : null;
  }
  const hex = rgb => '#' + rgb.map(x => Math.max(0, Math.min(255, Math.round(x))).toString(16).padStart(2, '0')).join('');
  const lin = c => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  const lum = rgb => 0.2126 * lin(rgb[0]) + 0.7152 * lin(rgb[1]) + 0.0722 * lin(rgb[2]);
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  function apca(text, bg) {
    const Y = rgb => { const [r, g, b] = rgb.map(c => (c / 255) ** 2.4); let y = 0.2126729 * r + 0.7151522 * g + 0.072175 * b; if (y < 0.022) y += (0.022 - y) ** 1.414; return y; };
    const yt = Y(text), yb = Y(bg);
    if (Math.abs(yb - yt) < 0.0005) return 0;
    let c;
    if (yb > yt) { c = (yb ** 0.56 - yt ** 0.57) * 1.14; return c < 0.1 ? 0 : (c - 0.027) * 100; }
    c = (yb ** 0.65 - yt ** 0.62) * 1.14; return c > -0.1 ? 0 : (c + 0.027) * 100;
  }
  function toHsl([r, g, b]) {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2; let h = 0, s = 0;
    if (max !== min) { const d = max - min; s = l > 0.5 ? d / (2 - max - min) : d / (max + min); h = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4; h /= 6; }
    return [h, s, l];
  }
  function fromHsl([h, s, l]) {
    if (!s) return [l, l, l].map(x => x * 255);
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q;
    const f = t => { t = (t + 1) % 1; return t < 1 / 6 ? p + (q - p) * 6 * t : t < 1 / 2 ? q : t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 : p; };
    return [f(h + 1 / 3), f(h), f(h - 1 / 3)].map(x => x * 255);
  }
  // Closest passing color by moving lightness only (keeps hue and saturation).
  function nearest(color, other, target) {
    const [h, s, l] = toHsl(color), found = [];
    for (const dirn of [-1, 1]) {
      for (let step = 1; step <= 100; step++) {
        const nl = l + dirn * step / 100;
        if (nl < 0 || nl > 1) break;
        const c = fromHsl([h, s, nl]).map(Math.round);
        if (ratio(c, other) >= target) { found.push({ c, d: step }); break; }
      }
    }
    return found.sort((a, b) => a.d - b.d)[0]?.c || null;
  }
  const CVD = {
    protanopia: [0.567, 0.433, 0, 0.558, 0.442, 0, 0, 0.242, 0.758],
    deuteranopia: [0.625, 0.375, 0, 0.7, 0.3, 0, 0, 0.3, 0.7],
    tritanopia: [0.95, 0.05, 0, 0, 0.433, 0.567, 0, 0.475, 0.525],
    achromatopsia: [0.299, 0.587, 0.114, 0.299, 0.587, 0.114, 0.299, 0.587, 0.114],
  };
  const sim = (rgb, m) => [0, 1, 2].map(i => m[i * 3] * rgb[0] + m[i * 3 + 1] * rgb[1] + m[i * 3 + 2] * rgb[2]).map(Math.round);

  // ---------- UI ----------
  const q = new URLSearchParams(location.search);
  const initial = store.get('contrast:pair', { fg: '#2f3747', bg: '#f5f6f8' });
  const startFg = parse(q.get('fg') ? '#' + q.get('fg').replace('#', '') : initial.fg) ? (q.get('fg') ? '#' + q.get('fg').replace('#', '') : initial.fg) : '#2f3747';
  const startBg = parse(q.get('bg') ? '#' + q.get('bg').replace('#', '') : initial.bg) ? (q.get('bg') ? '#' + q.get('bg').replace('#', '') : initial.bg) : '#f5f6f8';
  const eyedrop = 'EyeDropper' in window;
  const colorField = (id, label, value) => `<div class="field"><label for="${id}">${label}</label><div class="color-row"><input type="color" id="${id}-picker" value="${hex(parse(value))}" aria-label="${label} picker"><input class="input" id="${id}" value="${esc(value)}" spellcheck="false" autocomplete="off">${eyedrop ? `<button type="button" class="icon-btn" data-eye="${id}" aria-label="Pick ${label.toLowerCase()} from screen">${icon('pipette')}</button>` : ''}</div></div>`;

  app.innerHTML = tabBar('cc', [['pair', 'Check a pair', 'contrast'], ['palette', 'Palette matrix', 'layers']]) +
    tabPanel('cc', 'pair', `
      <div class="contrast-grid">
        <div class="card" style="display:grid;gap:14px;align-content:start">
          ${colorField('fg', 'Text color', startFg)}
          ${colorField('bg', 'Background color', startBg)}
          <div class="btn-row">${btn('swap', 'Swap', { icon: 'swap', ghost: true })}${btn('share', 'Share link', { icon: 'share', ghost: true })}</div>
          <div class="ratio-box"><span class="eyebrow">Contrast ratio</span><div class="ratio" id="ratio">—</div><span class="rating" id="rating"></span><div class="apca"><span class="eyebrow">APCA</span><strong id="apca">—</strong><small id="apca-note" class="muted"></small></div></div>
        </div>
        <div class="contrast-preview" id="preview">
          <span class="eyebrow" style="color:inherit;opacity:.8">Live preview</span>
          <h2 style="font-size:clamp(28px,3vw,40px);margin:12px 0">Good design includes everyone.</h2>
          <p style="font-size:24px;margin:0 0 10px">Large text · 24px regular</p>
          <p style="font-size:16px;margin:0 0 16px">Normal text at 16px. Readable color combinations make your message clear for every visitor, in every light.</p>
          <p style="font-size:13px;margin:0 0 20px;opacity:1">Small print at 13px — the hardest case.</p>
          <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center"><span class="demo-btn" id="demo-btn">Primary button</span><a href="#" onclick="return false" style="color:inherit;text-decoration:underline">A text link</a><span class="demo-icon">${icon('check')}</span></div>
        </div>
      </div>
      <div class="checks results" id="results" style="margin-top:14px"></div>
      <div class="group-title">Suggested fixes</div><div id="fixes" class="fix-grid"></div>
      <div class="group-title">Color vision simulation <span class="muted" style="text-transform:none;letter-spacing:0">approximate</span></div><div id="cvd" class="cvd-grid"></div>`, true) +
    tabPanel('cc', 'palette', `
      <label class="field">Colors (one per line or comma-separated, up to 12)<textarea class="input" id="palette-in" rows="3" spellcheck="false">#06080c, #ffffff, #4ff0b4, #8f7dff, #ff7847, #8790a1</textarea></label>
      <div class="toolbar" style="margin-top:12px"><div class="toolbar-group"><label class="check-row"><input type="radio" name="pm" value="4.5" checked> AA normal (4.5)</label><label class="check-row"><input type="radio" name="pm" value="3"> AA large / UI (3)</label><label class="check-row"><input type="radio" name="pm" value="7"> AAA (7)</label></div></div>
      <div class="table-wrap"><table class="matrix" id="matrix"></table></div>
      <p class="muted" style="font-size:13px">Rows are text colors, columns are backgrounds. Click a cell to inspect that pair.</p>`);
  tabs($('#cc'));

  const fgIn = $('#fg'), bgIn = $('#bg');
  function update() {
    const fg = parse(fgIn.value), bg = parse(bgIn.value);
    fgIn.classList.toggle('invalid', !fg); bgIn.classList.toggle('invalid', !bg);
    if (!fg || !bg) { status('Use a hex code like #2f3747, rgb(47 55 71), hsl(220 20% 23%) or a color name.', 'error'); return; }
    $('#fg-picker').value = hex(fg); $('#bg-picker').value = hex(bg);
    const r = ratio(fg, bg), rFloor = Math.floor(r * 100) / 100, lc = apca(fg, bg);
    $('#ratio').textContent = `${rFloor.toFixed(2)}:1`;
    const level = r >= 7 ? ['AAA', 'Excellent'] : r >= 4.5 ? ['AA', 'Good'] : r >= 3 ? ['AA Large', 'Large text only'] : ['Fail', 'Poor'];
    $('#rating').textContent = `${level[1]} · ${level[0]}`; $('#rating').className = `rating ${r >= 4.5 ? 'ok' : r >= 3 ? 'warn' : 'fail'}`;
    const alc = Math.abs(lc);
    $('#apca').textContent = `Lc ${lc.toFixed(1)}`;
    $('#apca-note').textContent = alc >= 90 ? 'Ideal for body text' : alc >= 75 ? 'Good for body text' : alc >= 60 ? 'Large or bold text' : alc >= 45 ? 'Headlines and large text only' : alc >= 30 ? 'Non-text elements only' : 'Not readable';
    const pv = $('#preview'); pv.style.color = hex(fg); pv.style.background = hex(bg);
    $('#demo-btn').style.background = hex(fg); $('#demo-btn').style.color = hex(bg);
    const checks = [['AA · Normal text', 4.5, 'Body copy under 24px (18.7px bold)'], ['AA · Large text', 3, '24px+ regular or 18.7px+ bold'], ['AA · UI components', 3, 'Icons, borders, focus rings, inputs'], ['AAA · Normal text', 7, 'Enhanced contrast for body copy'], ['AAA · Large text', 4.5, 'Enhanced contrast for large text']];
    $('#results').innerHTML = checks.map(([n, t, d]) => `<div class="check"><span class="badge ${r >= t ? '' : 'fail'}">${r >= t ? 'PASS' : 'FAIL'}</span><strong>${n}</strong><p>${d} · needs ${t}:1</p></div>`).join('');
    const fixes = [];
    for (const [t, name] of [[4.5, 'AA'], [7, 'AAA']]) {
      if (r >= t) continue;
      const f1 = nearest(fg, bg, t), f2 = nearest(bg, fg, t);
      if (f1) fixes.push({ which: 'fg', c: f1, label: `Text → ${name}`, r: ratio(f1, bg), bg, fg: f1 });
      if (f2) fixes.push({ which: 'bg', c: f2, label: `Background → ${name}`, r: ratio(fg, f2), bg: f2, fg });
    }
    $('#fixes').innerHTML = fixes.length ? fixes.map((f, i) => `<button type="button" class="fix-card" data-fix="${i}" style="background:${hex(f.bg)};color:${hex(f.fg)}"><strong>Aa</strong><span>${f.label}</span><code>${hex(f.c)} · ${f.r.toFixed(2)}:1</code></button>`).join('') : `<p class="muted" style="margin:0">${icon('check')} This pair already meets AAA for normal text.</p>`;
    $$('[data-fix]').forEach(b => b.addEventListener('click', () => { const f = fixes[+b.dataset.fix]; (f.which === 'fg' ? fgIn : bgIn).value = hex(f.c); update(); toast(`Applied ${hex(f.c)}`); }));
    $('#cvd').innerHTML = Object.entries(CVD).map(([name, m]) => { const a = sim(fg, m), b = sim(bg, m), rr = ratio(a, b); return `<div class="cvd" style="background:${hex(b)};color:${hex(a)}"><strong>Aa</strong><span>${name[0].toUpperCase() + name.slice(1)}</span><code>${rr.toFixed(2)}:1</code></div>`; }).join('');
    store.set('contrast:pair', { fg: fgIn.value, bg: bgIn.value });
    status(`Contrast ${rFloor.toFixed(2)}:1 — ${r >= 4.5 ? 'passes' : 'fails'} WCAG AA for normal text.`, r >= 4.5 ? 'ok' : 'error');
  }
  [fgIn, bgIn].forEach(i => i.addEventListener('input', debounce(update, 80)));
  ['fg', 'bg'].forEach(k => $(`#${k}-picker`).addEventListener('input', e => { $('#' + k).value = e.target.value; update(); }));
  $('#swap').addEventListener('click', () => { [fgIn.value, bgIn.value] = [bgIn.value, fgIn.value]; update(); });
  $('#share').addEventListener('click', () => { const f = parse(fgIn.value), b = parse(bgIn.value); if (f && b) copy(`${location.origin}${location.pathname}?fg=${hex(f).slice(1)}&bg=${hex(b).slice(1)}`, 'Share link copied'); });
  $$('[data-eye]').forEach(b => b.addEventListener('click', async () => { try { const r = await new EyeDropper().open(); $('#' + b.dataset.eye).value = r.sRGBHex; update(); } catch { /* cancelled */ } }));
  update();

  // ---------- Palette matrix ----------
  function matrix() {
    const colors = $('#palette-in').value.split(/[\n,;]+/).map(s => s.trim()).filter(Boolean).slice(0, 12).map(s => ({ s, c: parse(s) })).filter(x => x.c);
    const target = Number(document.querySelector('[name="pm"]:checked').value);
    if (colors.length < 2) { $('#matrix').innerHTML = '<tr><td class="muted">Add at least two valid colors.</td></tr>'; return; }
    const head = `<tr><th></th>${colors.map(b => `<th><span class="sw" style="background:${hex(b.c)}"></span>${esc(hex(b.c))}</th>`).join('')}</tr>`;
    const rows = colors.map(f => `<tr><th><span class="sw" style="background:${hex(f.c)}"></span>${esc(hex(f.c))}</th>${colors.map(b => { if (f === b) return '<td class="same">—</td>'; const r = ratio(f.c, b.c); return `<td><button type="button" class="cell ${r >= target ? 'pass' : 'fail'}" style="background:${hex(b.c)};color:${hex(f.c)}" data-fg="${hex(f.c)}" data-bg="${hex(b.c)}">Aa<small>${(Math.floor(r * 100) / 100).toFixed(2)}</small></button></td>`; }).join('')}</tr>`).join('');
    $('#matrix').innerHTML = head + rows;
    store.set('contrast:palette', $('#palette-in').value);
  }
  const savedPal = store.get('contrast:palette'); if (savedPal) $('#palette-in').value = savedPal;
  $('#palette-in').addEventListener('input', debounce(matrix, 200));
  $$('[name="pm"]').forEach(r => r.addEventListener('change', matrix));
  $('#matrix').addEventListener('click', e => { const c = e.target.closest('[data-fg]'); if (!c) return; fgIn.value = c.dataset.fg; bgIn.value = c.dataset.bg; $('#cc-pair').click(); update(); });
  matrix();
})();
