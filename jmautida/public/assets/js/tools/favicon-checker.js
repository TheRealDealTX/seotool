/* Favicon checker (server fetch) and favicon pack generator (canvas + ICO writer + ZIP). */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, tabs, tabBar, tabPanel, dropTarget, app } = window.JT;

  app.innerHTML = tabBar('fv', [['check', 'Check a website', 'search'], ['generate', 'Generate favicons', 'wand']]) +
    tabPanel('fv', 'check', `
      <form class="url-form" id="check-form" novalidate><label class="sr-only" for="url">Website URL</label>
        <input class="input" id="url" type="url" inputmode="url" placeholder="https://example.com" required maxlength="2048" autocomplete="url">
        <button class="btn btn-primary" id="check" type="submit">${icon('search')}Check favicons</button></form>
      <div id="results" style="margin-top:18px" aria-live="polite"><div class="empty"><span class="tool-icon">${icon('star')}</span><h3>Check the little details.</h3><p>See every icon a site declares — with previews, real pixel sizes and what to fix.</p></div></div>`, true) +
    tabPanel('fv', 'generate', `
      <div class="side-layout">
        <div style="display:grid;gap:14px">
          <div class="dropzone" id="drop" tabindex="0" role="button" aria-label="Upload a logo" style="min-height:180px">
            <span class="tool-icon">${icon('upload')}</span><h3 style="font-size:18px">Upload your logo</h3><p>Square SVG or PNG (512px+) works best</p>
            <input type="file" id="file" accept="image/png,image/svg+xml,image/jpeg,image/webp,image/gif" hidden></div>
          <div class="card" style="display:grid;gap:14px">
            <div class="field"><span>Background</span><div class="segmented" role="radiogroup" id="bg-mode"><button type="button" role="radio" data-bg="transparent" aria-checked="true">Transparent</button><button type="button" role="radio" data-bg="color" aria-checked="false">Color</button></div></div>
            <label class="field" id="bg-color-field" hidden>Background color<div style="display:flex;gap:8px"><input type="color" id="bg-color" value="#0b0e14"><input class="input input-sm" id="bg-hex" value="#0b0e14" maxlength="7" style="width:110px"></div></label>
            <label class="field">Padding <b id="pad-v">8%</b><input type="range" id="pad" min="0" max="30" value="8"></label>
            <label class="field">Corner radius <b id="rad-v">20%</b><input type="range" id="rad" min="0" max="50" value="20"></label>
            <label class="field">App name<input class="input input-sm" id="app-name" value="My Website" maxlength="60"></label>
            <div class="form-grid"><label class="field">Short name<input class="input input-sm" id="short-name" value="Website" maxlength="20"></label>
            <label class="field">Theme color<input class="input input-sm" id="theme" value="#0b0e14" maxlength="7"></label></div>
          </div>
        </div>
        <div style="display:grid;gap:14px;min-width:0">
          <div class="card"><div class="group-title" style="margin-top:0">Preview</div>
            <div class="fav-previews">
              <div class="browser-tab light"><span class="tab-ico"><canvas id="pv-tab-l" width="32" height="32"></canvas></span><span>My Website</span><span class="x">×</span></div>
              <div class="browser-tab dark"><span class="tab-ico"><canvas id="pv-tab-d" width="32" height="32"></canvas></span><span>My Website</span><span class="x">×</span></div>
              <div class="home-icons"><figure><canvas id="pv-ios" width="180" height="180"></canvas><figcaption>iOS</figcaption></figure><figure><canvas id="pv-android" width="192" height="192" class="round"></canvas><figcaption>Android</figcaption></figure></div>
            </div>
            <div class="size-strip" id="sizes"></div>
          </div>
          <div class="toolbar"><div class="toolbar-group"><span class="muted" id="gen-info">Upload a logo to generate your favicon pack.</span></div><div class="toolbar-group">${btn('zip', 'Download favicon pack', { icon: 'download', primary: true, attrs: 'disabled' })}</div></div>
          <div class="code-out"><pre id="snippet"></pre><button type="button" class="btn btn-xs" id="copy-snippet">${icon('copy')}Copy HTML</button></div>
        </div>
      </div>`);
  tabs($('#fv'));

  // ---------- Checker ----------
  const SNIPPET = `<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">`;
  const badge = st => `<span class="badge ${st === 'PASS' ? '' : st === 'NOTE' ? 'warn' : 'fail'}">${st === 'NOTE' ? 'CHECK' : st}</span>`;
  $('#check-form').addEventListener('submit', async e => {
    e.preventDefault();
    let value = $('#url').value.trim();
    if (value && !/^https?:\/\//i.test(value)) { value = 'https://' + value; $('#url').value = value; }
    let url;
    try { url = new URL(value); if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) throw 0; }
    catch { status('Enter a valid public URL, such as https://example.com', 'error'); return; }
    $('#check').disabled = true;
    $('#results').innerHTML = `<div class="empty"><div class="loader"></div><h3>Checking ${esc(url.hostname)}…</h3><p>Fetching the page, its icons and manifest.</p></div>`;
    status('Checking favicons…');
    const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 60000);
    try {
      const res = await fetch('/api/check.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url: url.href, mode: 'favicon' }), signal: controller.signal });
      if (!(res.headers.get('content-type') || '').includes('application/json')) throw new Error('The checker service is unavailable right now.');
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || 'The check failed.');
      const scored = data.checks.filter(c => c.state !== 'INFO');
      const score = Math.round(scored.reduce((s, c) => s + (c.state === 'PASS' ? 1 : c.state === 'NOTE' ? 0.5 : 0), 0) / Math.max(1, scored.length) * 100);
      const color = score >= 80 ? 'var(--ok)' : score >= 55 ? 'var(--warn)' : 'var(--danger)';
      const m = data.manifest;
      const has = label => data.icons.some(i => i.ok && i.label.startsWith(label));
      const biggest = Math.max(0, ...data.icons.filter(i => i.ok).map(i => i.vector ? 9999 : (i.width || 0)));
      const recs = [];
      if (!has('Favicon') && !has('/favicon.ico')) recs.push('Add a favicon.ico (16/32/48 px) at the site root and declare it with <link rel="icon">.');
      if (!has('Apple touch icon')) recs.push('Add a 180×180 apple-touch-icon.png for iPhone and iPad home screens.');
      if (!m) recs.push('Add a site.webmanifest with 192×192 and 512×512 icons for Android.');
      if (biggest && biggest < 48) recs.push('Your largest icon is under 48px — Google Search prefers favicons that are multiples of 48px.');
      $('#results').innerHTML = `
        <div class="report-head"><div class="score-ring" style="--score:${score};--ring:${color}"><div><strong>${score}</strong><span>/100</span></div></div>
          <div class="report-meta"><span class="eyebrow">Favicon health</span><h3>${esc(url.hostname)}</h3><p class="muted">${esc(data.url)}</p></div>
          <div class="toolbar-group">${btn('to-gen', 'Generate a favicon pack', { icon: 'wand', ghost: true })}</div></div>
        <div class="icon-gallery">${data.icons.map(i => `<figure class="icon-tile ${i.ok ? '' : 'bad'}"><div class="icon-preview">${i.ok ? `<img src="${esc(i.url)}" alt="" referrerpolicy="no-referrer" onerror="this.replaceWith(document.createTextNode('?'))">` : '<span>✕</span>'}</div>
          <figcaption><strong>${esc(i.label)}</strong><small>${i.ok ? (i.vector ? 'SVG · scalable' : `${i.width || '?'}×${i.height || '?'} · ${esc(i.format || i.type)}`) : `HTTP ${i.status || '—'}`}</small><a href="${esc(i.url)}" target="_blank" rel="noopener noreferrer nofollow">${esc(i.url.replace(/^https?:\/\//, ''))}</a></figcaption></figure>`).join('') || '<p class="muted">No icons could be fetched.</p>'}</div>
        ${recs.length ? `<div class="card fixes"><h3>${icon('wand')} Recommendations</h3><ol>${recs.map(r => `<li><span>${esc(r)}</span></li>`).join('')}</ol></div>` : ''}
        <div class="group-title">Checks</div><div class="checks">${data.checks.map(c => `<div class="check">${badge(c.state)}<strong>${esc(c.label)}</strong><p>${esc(c.detail)}</p></div>`).join('')}</div>
        ${m ? `<div class="group-title">Manifest</div><div class="tag-table">${[['name', m.name], ['short_name', m.short_name], ['display', m.display], ['theme_color', m.theme_color], ['background_color', m.background_color], ['icons', String(m.icons)]].map(([k, v]) => `<div><code>${k}</code><span class="${v ? '' : 'muted'}">${esc(v || 'not set')}${/color/.test(k) && v ? ` <i class="swatch" style="background:${esc(v)}"></i>` : ''}</span></div>`).join('')}</div>` : ''}
        <div class="group-title">Recommended HTML</div><div class="code-out"><pre>${esc(SNIPPET)}</pre><button type="button" class="btn btn-xs" id="copy-rec">${icon('copy')}Copy</button></div>`;
      $('#copy-rec').addEventListener('click', () => copy(SNIPPET));
      $('#to-gen').addEventListener('click', () => $('#fv-generate').click());
      status('Check complete. Browser caches can still show an older favicon after you update it.', 'ok');
    } catch (err) {
      $('#results').innerHTML = `<div class="empty"><span class="tool-icon">${icon('x')}</span><h3>The check couldn’t finish.</h3><p>${esc(err.name === 'AbortError' ? 'The website took too long to respond.' : err.message)}</p></div>`;
      status(err.name === 'AbortError' ? 'The website took too long to respond.' : err.message, 'error');
    } finally { clearTimeout(timer); $('#check').disabled = false; }
  });

  // ---------- Generator ----------
  const opts = Object.assign({ bg: 'transparent', color: '#0b0e14', pad: 8, rad: 20, name: 'My Website', short: 'Website', theme: '#0b0e14' }, store.get('fav:opts', {}));
  let source = null, sourceFile = null;
  const SIZES = [16, 32, 48, 180, 192, 512];

  function render(size, { round = opts.rad, forceBg = false } = {}) {
    const c = document.createElement('canvas'); c.width = c.height = size;
    const g = c.getContext('2d'); g.imageSmoothingQuality = 'high';
    const r = size * round / 100;
    const fill = opts.bg === 'color' ? opts.color : forceBg ? '#ffffff' : null;
    if (fill) {
      g.fillStyle = fill; g.beginPath();
      if (g.roundRect) g.roundRect(0, 0, size, size, r); else g.rect(0, 0, size, size);
      g.fill();
    }
    if (source) {
      const pad = size * opts.pad / 100, box = size - pad * 2;
      const w = source.naturalWidth || 512, h = source.naturalHeight || 512, s = Math.min(box / w, box / h);
      g.drawImage(source, (size - w * s) / 2, (size - h * s) / 2, w * s, h * s);
    }
    return c;
  }
  const blobOf = c => new Promise(res => c.toBlob(res, 'image/png'));
  function paint(target, canvas) { const t = $(target); const g = t.getContext('2d'); g.clearRect(0, 0, t.width, t.height); g.drawImage(canvas, 0, 0, t.width, t.height); }
  function preview() {
    $$('.browser-tab span:nth-child(2)').forEach(s => { s.textContent = opts.name || 'My Website'; });
    $('#bg-color-field').hidden = opts.bg !== 'color';
    $$('[data-bg]').forEach(b => b.setAttribute('aria-checked', String(b.dataset.bg === opts.bg)));
    $('#pad-v').textContent = opts.pad + '%'; $('#rad-v').textContent = opts.rad + '%';
    $('#snippet').textContent = packSnippet();
    if (!source) return;
    paint('#pv-tab-l', render(32)); paint('#pv-tab-d', render(32));
    paint('#pv-ios', render(180, { round: 0, forceBg: true })); paint('#pv-android', render(192));
    $('#sizes').innerHTML = '';
    SIZES.forEach(s => { const f = document.createElement('figure'); const c = render(s, s === 180 ? { round: 0, forceBg: true } : {}); c.style.width = c.style.height = Math.min(s, 96) + 'px'; f.append(c); const cap = document.createElement('figcaption'); cap.textContent = `${s}×${s}`; f.append(cap); $('#sizes').append(f); });
    store.set('fav:opts', opts);
  }

  const hasSvg = () => sourceFile?.type === 'image/svg+xml' && opts.bg === 'transparent' && opts.pad === 0;
  const packSnippet = () => `<link rel="icon" href="/favicon.ico" sizes="48x48">\n${hasSvg() ? '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n' : ''}<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n<link rel="manifest" href="/site.webmanifest">\n<meta name="theme-color" content="${opts.theme}">`;
  function ico(entries) {
    const header = 6 + 16 * entries.length, total = header + entries.reduce((s, e) => s + e.bytes.length, 0);
    const out = new Uint8Array(total), dv = new DataView(out.buffer);
    dv.setUint16(0, 0, true); dv.setUint16(2, 1, true); dv.setUint16(4, entries.length, true);
    let offset = header;
    entries.forEach((e, i) => {
      const o = 6 + i * 16;
      dv.setUint8(o, e.size >= 256 ? 0 : e.size); dv.setUint8(o + 1, e.size >= 256 ? 0 : e.size);
      dv.setUint16(o + 4, 1, true); dv.setUint16(o + 6, 32, true);
      dv.setUint32(o + 8, e.bytes.length, true); dv.setUint32(o + 12, offset, true);
      out.set(e.bytes, offset); offset += e.bytes.length;
    });
    return new Blob([out], { type: 'image/x-icon' });
  }

  async function loadLogo(file) {
    if (!file || !/^image\//.test(file.type)) { toast('Please choose an image file', 'error'); return; }
    if (file.size > 20 * 1024 * 1024) { toast('Please use an image under 20 MB', 'error'); return; }
    const url = URL.createObjectURL(file), img = new Image();
    img.onload = () => {
      if (!img.naturalWidth && file.type !== 'image/svg+xml') { toast('Could not read this image', 'error'); return; }
      source = img; sourceFile = file;
      const w = img.naturalWidth, h = img.naturalHeight;
      $('#gen-info').textContent = `${file.name} · ${w || 'vector'}${h ? '×' + h : ''}${w && w < 512 && file.type !== 'image/svg+xml' ? ' — use 512px or larger for sharp icons' : ''}`;
      $('#zip').disabled = false; preview();
      status('Logo loaded. Adjust the options, then download your favicon pack.', 'ok');
    };
    img.onerror = () => toast('Could not read this image', 'error');
    img.src = url;
  }
  const drop = $('#drop'), file = $('#file');
  drop.addEventListener('click', () => file.click());
  drop.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); file.click(); } });
  file.addEventListener('change', () => { loadLogo(file.files[0]); file.value = ''; });
  dropTarget(drop, files => loadLogo(files[0]));

  $$('[data-bg]').forEach(b => b.addEventListener('click', () => { opts.bg = b.dataset.bg; preview(); }));
  const hex = v => /^#[0-9a-f]{6}$/i.test(v);
  $('#bg-color').addEventListener('input', e => { opts.color = e.target.value; $('#bg-hex').value = opts.color; preview(); });
  $('#bg-hex').addEventListener('input', e => { if (hex(e.target.value)) { opts.color = e.target.value; $('#bg-color').value = opts.color; preview(); } });
  $('#pad').addEventListener('input', e => { opts.pad = Number(e.target.value); preview(); });
  $('#rad').addEventListener('input', e => { opts.rad = Number(e.target.value); preview(); });
  $('#app-name').addEventListener('input', e => { opts.name = e.target.value; preview(); });
  $('#short-name').addEventListener('input', e => { opts.short = e.target.value; });
  $('#theme').addEventListener('input', e => { if (hex(e.target.value)) { opts.theme = e.target.value; preview(); } });
  $('#bg-color').value = $('#bg-hex').value = opts.color; $('#pad').value = opts.pad; $('#rad').value = opts.rad;
  $('#app-name').value = opts.name; $('#short-name').value = opts.short; $('#theme').value = opts.theme;
  $('#copy-snippet').addEventListener('click', () => copy($('#snippet').textContent));

  $('#zip').addEventListener('click', async () => {
    if (!source) return;
    if (!window.JSZip) { toast('ZIP library failed to load', 'error'); return; }
    $('#zip').disabled = true; status('Generating icons…');
    try {
      const zip = new JSZip();
      const png = async (s, o) => new Uint8Array(await (await blobOf(render(s, o))).arrayBuffer());
      const icoEntries = [];
      for (const s of [16, 32, 48]) icoEntries.push({ size: s, bytes: await png(s) });
      zip.file('favicon.ico', ico(icoEntries));
      zip.file('favicon-16x16.png', icoEntries[0].bytes);
      zip.file('favicon-32x32.png', icoEntries[1].bytes);
      zip.file('favicon-48x48.png', icoEntries[2].bytes);
      zip.file('apple-touch-icon.png', await png(180, { round: 0, forceBg: true }));
      zip.file('android-chrome-192x192.png', await png(192));
      zip.file('android-chrome-512x512.png', await png(512));
      if (hasSvg()) zip.file('favicon.svg', sourceFile);
      zip.file('site.webmanifest', JSON.stringify({ name: opts.name, short_name: opts.short, icons: [{ src: '/android-chrome-192x192.png', sizes: '192x192', type: 'image/png' }, { src: '/android-chrome-512x512.png', sizes: '512x512', type: 'image/png' }], theme_color: opts.theme, background_color: opts.bg === 'color' ? opts.color : '#ffffff', display: 'standalone' }, null, 2));
      zip.file('favicon-snippet.html', `<!-- Paste inside <head> -->\n${packSnippet()}\n`);
      download(await zip.generateAsync({ type: 'blob' }), 'favicon-pack.zip');
      status('Favicon pack downloaded: upload the files to your site root and paste the snippet into <head>.', 'ok');
    } catch { status('Could not generate the pack. Try a different image.', 'error'); }
    finally { $('#zip').disabled = false; }
  });
  preview();
  status('Check a website, or switch to Generate to build a favicon pack from your logo.');
})();
