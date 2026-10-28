/* Image converter: batch convert/compress/resize in the browser with canvas encoders. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, store, bytes, btn, dropTarget, app } = window.JT;
  const MAX_FILES = 100, MAX_BYTES = 60 * 1024 * 1024, MAX_PIXELS = 50e6;
  const FORMATS = { webp: ['image/webp', 'webp', 'WebP'], avif: ['image/avif', 'avif', 'AVIF'], jpeg: ['image/jpeg', 'jpg', 'JPG'], png: ['image/png', 'png', 'PNG'] };
  const defaults = { format: 'webp', quality: 80, resize: 'none', size: 1920, target: false, targetKb: 200, bg: '#ffffff' };
  const settings = Object.assign({}, defaults, store.get('img:settings', {}));
  let files = [], seq = 0, generation = 0, avif = false, pendingZip = false;

  app.innerHTML = `
  <div class="dropzone" id="drop" tabindex="0" role="button" aria-label="Add images: click to browse, drop files or paste">
    <span class="tool-icon">${icon('upload')}</span>
    <h3>Drop images here, or click to browse</h3>
    <p>JPG, PNG, GIF, BMP, WebP, AVIF, SVG, ICO, HEIC (Safari) · up to ${MAX_FILES} files · paste with Ctrl/⌘ + V</p>
    <input type="file" id="file-input" accept="image/*,.heic,.heif,.svg,.ico" multiple hidden>
  </div>
  <div class="img-settings card" style="margin-top:14px">
    <div class="field"><span>Convert to</span><div class="segmented" role="radiogroup" aria-label="Output format" id="formats">
      ${Object.entries(FORMATS).map(([k, f]) => `<button type="button" role="radio" data-format="${k}" aria-checked="${settings.format === k}"${k === 'avif' ? ' hidden' : ''}>${f[2]}</button>`).join('')}
    </div></div>
    <label class="field" id="quality-field"><span>Quality <b id="quality-value">${settings.quality}%</b></span><input type="range" id="quality" min="5" max="100" step="1" value="${settings.quality}"></label>
    <div class="field"><span>Resize</span><div style="display:flex;gap:8px">
      <select class="select select-sm" id="resize"><option value="none">Original size</option><option value="width">Max width</option><option value="height">Max height</option><option value="long">Longest side</option><option value="percent">Scale %</option></select>
      <input class="input input-sm" type="number" id="size" min="1" max="16000" value="${settings.size}" aria-label="Resize value" style="width:110px">
    </div></div>
    <div class="field"><label class="check-row"><input type="checkbox" id="target"${settings.target ? ' checked' : ''}> Target file size</label>
      <div style="display:flex;gap:8px;align-items:center"><input class="input input-sm" type="number" id="target-kb" min="5" max="50000" value="${settings.targetKb}" aria-label="Target size in KB" style="width:110px"><span class="muted">KB max</span></div></div>
    <label class="field" id="bg-field"><span>JPG background</span><div style="display:flex;gap:8px;align-items:center"><input type="color" id="bg" value="${settings.bg}"><span class="muted" style="font-size:13px">fills transparency</span></div></label>
  </div>
  <div class="toolbar" style="margin-top:14px">
    <div class="toolbar-group" id="summary"><span class="muted">No images yet — add some to get started.</span></div>
    <div class="toolbar-group">${btn('reconvert', 'Re-convert', { icon: 'refresh', ghost: true })}${btn('zip', 'Download all (.zip)', { icon: 'download', primary: true })}${btn('clear', 'Clear', { icon: 'trash', ghost: true, cls: 'btn-danger' })}</div>
  </div>
  <div class="file-list" id="list"></div>
  <dialog class="compare-dialog" id="compare"><div class="compare-head"><strong id="compare-title"></strong><span class="muted" id="compare-meta"></span><button type="button" class="icon-btn" id="compare-close" aria-label="Close comparison">${icon('x')}</button></div>
  <div class="compare-stage" id="compare-stage"><img id="cmp-after" alt="Converted image"><div class="cmp-before-wrap" id="cmp-before-wrap"><img id="cmp-before" alt="Original image"></div><div class="cmp-handle" id="cmp-handle"><span>${icon('swap')}</span></div>
  <span class="cmp-label left">Original</span><span class="cmp-label right">Converted</span></div>
  <input type="range" id="cmp-range" min="0" max="100" value="50" aria-label="Comparison position"></dialog>`;

  const input = $('#file-input'), drop = $('#drop'), list = $('#list');
  $('#resize').value = settings.resize;

  // Feature-detect AVIF encoding.
  (function detectAvif() {
    const c = document.createElement('canvas'); c.width = c.height = 2;
    c.toBlob(b => {
      avif = !!b && b.type === 'image/avif';
      if (avif) $('[data-format="avif"]').hidden = false;
      else if (settings.format === 'avif') setFormat('webp');
    }, 'image/avif', 0.5);
  })();

  function save() { store.set('img:settings', settings); }
  function syncUI() {
    $$('[data-format]').forEach(b => b.setAttribute('aria-checked', String(b.dataset.format === settings.format)));
    $('#quality-field').style.opacity = settings.format === 'png' ? '.45' : '1';
    $('#quality').disabled = settings.format === 'png';
    $('#bg-field').hidden = settings.format !== 'jpeg';
    $('#size').disabled = settings.resize === 'none';
    $('#target-kb').disabled = !settings.target;
  }
  function setFormat(f) { settings.format = f; save(); syncUI(); convertAll(); }
  $$('[data-format]').forEach(b => b.addEventListener('click', () => setFormat(b.dataset.format)));
  let qTimer;
  $('#quality').addEventListener('input', e => { settings.quality = Number(e.target.value); $('#quality-value').textContent = settings.quality + '%'; save(); clearTimeout(qTimer); qTimer = setTimeout(convertAll, 350); });
  $('#resize').addEventListener('change', e => { settings.resize = e.target.value; if (settings.resize === 'percent' && settings.size > 400) { settings.size = 50; $('#size').value = 50; } save(); syncUI(); convertAll(); });
  $('#size').addEventListener('change', e => { settings.size = Math.max(1, Math.min(16000, Number(e.target.value) || 1)); e.target.value = settings.size; save(); convertAll(); });
  $('#target').addEventListener('change', e => { settings.target = e.target.checked; save(); syncUI(); convertAll(); });
  $('#target-kb').addEventListener('change', e => { settings.targetKb = Math.max(5, Number(e.target.value) || 200); e.target.value = settings.targetKb; save(); if (settings.target) convertAll(); });
  $('#bg').addEventListener('change', e => { settings.bg = e.target.value; save(); if (settings.format === 'jpeg') convertAll(); });
  syncUI();

  drop.addEventListener('click', () => input.click());
  drop.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
  input.addEventListener('change', () => { addFiles([...input.files]); input.value = ''; });
  dropTarget(drop, addFiles);
  document.addEventListener('paste', e => {
    const items = [...(e.clipboardData?.items || [])].filter(i => i.type.startsWith('image/')).map(i => i.getAsFile()).filter(Boolean);
    if (items.length) { e.preventDefault(); addFiles(items.map((f, i) => new File([f], f.name && f.name !== 'image.png' ? f.name : `pasted-${Date.now()}-${i + 1}.png`, { type: f.type }))); }
  });

  function addFiles(incoming) {
    const accepted = [];
    for (const f of incoming) {
      if (files.length + accepted.length >= MAX_FILES) { toast(`Up to ${MAX_FILES} images at a time`, 'error'); break; }
      const isImage = f.type.startsWith('image/') || /\.(heic|heif|svg|ico|avif|webp|bmp)$/i.test(f.name);
      if (!isImage) { toast(`${f.name} is not an image`, 'error'); continue; }
      if (f.size > MAX_BYTES) { toast(`${f.name} is larger than 60 MB`, 'error'); continue; }
      accepted.push({ id: ++seq, file: f, name: f.name, srcUrl: URL.createObjectURL(f), state: 'queued' });
    }
    if (!accepted.length) return;
    files.push(...accepted);
    render();
    processQueue(accepted, generation);
  }

  function decode(item) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.decoding = 'async';
      img.onload = () => {
        let w = img.naturalWidth, h = img.naturalHeight;
        if (/svg/i.test(item.file.type || item.name)) {
          // Vectors have no fixed pixel size: rasterize with a 1024px long side by default.
          if (!w || !h) { w = 1024; h = 1024; }
          const s = 1024 / Math.max(w, h); if (s > 1) { w = Math.round(w * s); h = Math.round(h * s); }
        }
        if (!w || !h) return reject(new Error('Could not read image dimensions.'));
        resolve({ img, w, h });
      };
      img.onerror = () => reject(new Error(/heic|heif/i.test(item.file.type + item.name) ? 'This browser cannot read HEIC. Open the page in Safari, or export the photo as JPG first.' : 'This file could not be decoded as an image.'));
      img.src = item.srcUrl;
    });
  }

  function targetSize(w, h, scaleExtra = 1) {
    let tw = w, th = h;
    const v = settings.size;
    if (settings.resize === 'width' && w > v) { tw = v; th = h * v / w; }
    else if (settings.resize === 'height' && h > v) { th = v; tw = w * v / h; }
    else if (settings.resize === 'long' && Math.max(w, h) > v) { const s = v / Math.max(w, h); tw = w * s; th = h * s; }
    else if (settings.resize === 'percent') { const s = Math.min(400, v) / 100; tw = w * s; th = h * s; }
    tw *= scaleExtra; th *= scaleExtra;
    if (tw * th > MAX_PIXELS) { const s = Math.sqrt(MAX_PIXELS / (tw * th)); tw *= s; th *= s; }
    return [Math.max(1, Math.round(Math.min(16384, tw))), Math.max(1, Math.round(Math.min(16384, th)))];
  }

  // Downscale in halving steps for sharper results on large reductions.
  function draw(img, sw, sh, tw, th, mime) {
    let src = img, cw = sw, ch = sh;
    while (cw / 2 >= tw * 1.05 && ch / 2 >= th * 1.05) {
      const step = document.createElement('canvas');
      step.width = Math.round(cw / 2); step.height = Math.round(ch / 2);
      const sctx = step.getContext('2d'); sctx.imageSmoothingQuality = 'high';
      sctx.drawImage(src, 0, 0, step.width, step.height);
      src = step; cw = step.width; ch = step.height;
    }
    const canvas = document.createElement('canvas');
    canvas.width = tw; canvas.height = th;
    const ctx = canvas.getContext('2d');
    ctx.imageSmoothingQuality = 'high';
    if (mime === 'image/jpeg') { ctx.fillStyle = settings.bg; ctx.fillRect(0, 0, tw, th); }
    ctx.drawImage(src, 0, 0, tw, th);
    return canvas;
  }
  const encode = (canvas, mime, q) => new Promise((resolve, reject) => canvas.toBlob(b => (b ? resolve(b) : reject(new Error('The browser could not encode this format.'))), mime, q));

  async function convert(item) {
    const [mime, ext] = FORMATS[settings.format];
    const { img, w, h } = await decode(item);
    item.w = w; item.h = h;
    const lossy = mime !== 'image/png';
    let q = settings.quality / 100, scale = 1, blob, tw, th;
    for (let attempt = 0; attempt < 7; attempt++) {
      [tw, th] = targetSize(w, h, scale);
      const canvas = draw(img, w, h, tw, th, mime);
      if (settings.target && lossy) {
        const limit = settings.targetKb * 1024;
        blob = await encode(canvas, mime, q);
        if (blob.size > limit) {
          // Binary-search the highest quality that fits.
          let lo = 0.05, hi = q, best = null;
          for (let i = 0; i < 7; i++) {
            const mid = (lo + hi) / 2, b = await encode(canvas, mime, mid);
            if (b.size <= limit) { best = b; lo = mid; } else hi = mid;
          }
          if (!best) { const b = await encode(canvas, mime, 0.05); if (b.size <= limit) best = b; }
          if (best) { blob = best; break; }
          scale *= 0.8; continue;
        }
        break;
      }
      blob = await encode(canvas, mime, lossy ? q : undefined);
      if (settings.target && !lossy && blob.size > settings.targetKb * 1024) { scale *= 0.8; continue; }
      break;
    }
    if (blob.type !== mime) throw new Error(`${FORMATS[settings.format][2]} encoding is not supported in this browser.`);
    if (item.out?.url) URL.revokeObjectURL(item.out.url);
    const base = item.name.replace(/\.[^.]+$/, '') || 'image';
    item.out = { blob, url: URL.createObjectURL(blob), w: tw, h: th, name: `${base}.${ext}`, missed: settings.target && blob.size > settings.targetKb * 1024 };
  }

  async function processQueue(items, gen) {
    for (const item of items) {
      if (gen !== generation || !files.includes(item)) return;
      item.state = 'working'; item.error = ''; renderItem(item);
      try { await convert(item); if (gen !== generation) return; item.state = 'done'; }
      catch (err) { item.state = 'error'; item.error = err.message; }
      renderItem(item); summary();
    }
    if (gen === generation) {
      const done = files.filter(f => f.state === 'done').length;
      if (done) status(`${done} image${done === 1 ? '' : 's'} converted in your browser. Nothing was uploaded.`, 'ok');
      if (pendingZip && !files.some(f => f.state === 'queued' || f.state === 'working')) { pendingZip = false; buildZip(); }
    }
  }
  function convertAll() {
    if (!files.length) return;
    generation++;
    files.forEach(f => { f.state = 'queued'; });
    render();
    processQueue([...files], generation);
  }

  function summary() {
    const done = files.filter(f => f.state === 'done');
    const before = done.reduce((s, f) => s + f.file.size, 0), after = done.reduce((s, f) => s + f.out.blob.size, 0);
    const pct = before ? Math.round((1 - after / before) * 100) : 0;
    $('#summary').innerHTML = files.length
      ? `<strong>${files.length} image${files.length === 1 ? '' : 's'}</strong><span class="muted">${bytes(before)} → ${bytes(after)}</span>${done.length ? `<span class="badge ${pct >= 0 ? '' : 'warn'}">${pct >= 0 ? '−' + pct : '+' + Math.abs(pct)}%</span>` : ''}`
      : '<span class="muted">No images yet — add some to get started.</span>';
    $('#zip').disabled = !files.length;
    $('#reconvert').disabled = !files.length;
    $('#clear').disabled = !files.length;
  }

  function itemHTML(f) {
    const saved = f.state === 'done' ? Math.round((1 - f.out.blob.size / f.file.size) * 100) : 0;
    const right = f.state === 'done'
      ? `<div class="fi-out"><strong>${bytes(f.out.blob.size)}</strong><span class="badge ${saved >= 0 ? '' : 'warn'}">${saved >= 0 ? '−' + saved : '+' + Math.abs(saved)}%</span></div><small class="muted">${f.out.w}×${f.out.h} · ${esc(f.out.name)}${f.out.missed ? ' · <span style="color:var(--warn)">above target</span>' : ''}</small>`
      : f.state === 'error' ? `<small style="color:var(--danger)">${esc(f.error)}</small>`
      : `<div class="fi-progress"><i></i></div><small class="muted">${f.state === 'working' ? 'Converting…' : 'Queued'}</small>`;
    return `<div class="fi-thumb">${f.state === 'error' ? icon('image') : `<img src="${f.out?.url || f.srcUrl}" alt="" loading="lazy">`}</div>
      <div class="fi-meta"><strong title="${esc(f.name)}">${esc(f.name)}</strong><small class="muted">${bytes(f.file.size)}${f.w ? ` · ${f.w}×${f.h}` : ''} · ${esc((f.file.type || 'image').replace('image/', '').toUpperCase())}</small></div>
      <div class="fi-result">${right}</div>
      <div class="fi-actions">
        <button type="button" class="icon-btn" data-act="compare" aria-label="Compare ${esc(f.name)}" ${f.state === 'done' ? '' : 'disabled'}>${icon('eye')}</button>
        <button type="button" class="icon-btn" data-act="download" aria-label="Download ${esc(f.name)}" ${f.state === 'done' ? '' : 'disabled'}>${icon('download')}</button>
        <button type="button" class="icon-btn" data-act="remove" aria-label="Remove ${esc(f.name)}">${icon('x')}</button>
      </div>`;
  }
  function renderItem(f) {
    const el = list.querySelector(`[data-id="${f.id}"]`);
    if (el) { el.className = `file-item ${f.state}`; el.innerHTML = itemHTML(f); }
  }
  function render() {
    list.innerHTML = files.map(f => `<div class="file-item ${f.state}" data-id="${f.id}">${itemHTML(f)}</div>`).join('');
    summary();
  }
  list.addEventListener('click', e => {
    const b = e.target.closest('[data-act]'); if (!b) return;
    const f = files.find(x => x.id === Number(b.closest('[data-id]').dataset.id)); if (!f) return;
    if (b.dataset.act === 'download') download(f.out.blob, f.out.name);
    if (b.dataset.act === 'remove') {
      URL.revokeObjectURL(f.srcUrl); if (f.out?.url) URL.revokeObjectURL(f.out.url);
      files = files.filter(x => x !== f); render();
    }
    if (b.dataset.act === 'compare') openCompare(f);
  });

  $('#reconvert').addEventListener('click', convertAll);
  $('#clear').addEventListener('click', () => {
    generation++; pendingZip = false;
    files.forEach(f => { URL.revokeObjectURL(f.srcUrl); if (f.out?.url) URL.revokeObjectURL(f.out.url); });
    files = []; render(); status('');
  });
  $('#zip').addEventListener('click', () => {
    if (files.some(f => f.state === 'queued' || f.state === 'working')) { pendingZip = true; status('Finishing conversions, then your ZIP will download…'); return; }
    buildZip();
  });
  async function buildZip() {
    const done = files.filter(f => f.state === 'done');
    if (!done.length) return;
    if (!window.JSZip) { toast('ZIP library failed to load — download files individually', 'error'); return; }
    const zip = new JSZip(), used = new Set();
    for (const f of done) {
      let name = f.out.name, n = 1;
      while (used.has(name.toLowerCase())) name = f.out.name.replace(/(\.[^.]+)$/, `-${n++}$1`);
      used.add(name.toLowerCase()); zip.file(name, f.out.blob);
    }
    $('#zip').disabled = true; status('Building ZIP…');
    try { download(await zip.generateAsync({ type: 'blob', compression: 'STORE' }), `converted-${settings.format === 'jpeg' ? 'jpg' : settings.format}-images.zip`); status(`ZIP with ${done.length} images is downloading.`, 'ok'); }
    catch { status('Could not build the ZIP. Try downloading files individually.', 'error'); }
    finally { $('#zip').disabled = false; }
  }

  // Before/after comparison
  const dialog = $('#compare'), range = $('#cmp-range');
  function setPos(v) { $('#cmp-before-wrap').style.clipPath = `inset(0 ${100 - v}% 0 0)`; $('#cmp-handle').style.left = v + '%'; }
  function openCompare(f) {
    $('#cmp-before').src = f.srcUrl; $('#cmp-after').src = f.out.url;
    $('#compare-title').textContent = f.name;
    $('#compare-meta').textContent = `${bytes(f.file.size)} → ${bytes(f.out.blob.size)} · ${f.out.w}×${f.out.h}`;
    range.value = 50; setPos(50);
    if (dialog.showModal) dialog.showModal(); else dialog.setAttribute('open', '');
  }
  range.addEventListener('input', () => setPos(range.value));
  const stage = $('#compare-stage');
  const fromPointer = e => { const r = stage.getBoundingClientRect(); const v = Math.max(0, Math.min(100, ((e.clientX - r.left) / r.width) * 100)); range.value = v; setPos(v); };
  stage.addEventListener('pointerdown', e => { stage.setPointerCapture(e.pointerId); fromPointer(e); });
  stage.addEventListener('pointermove', e => { if (stage.hasPointerCapture(e.pointerId)) fromPointer(e); });
  $('#compare-close').addEventListener('click', () => dialog.close ? dialog.close() : dialog.removeAttribute('open'));
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });

  summary();
  status('Ready. Your images are processed on this device and never uploaded.');
})();
