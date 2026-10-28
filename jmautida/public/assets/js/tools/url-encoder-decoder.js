/* URL toolkit: encode/decode, URL parser with editable query, UTM builder, Base64. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, tabs, tabBar, tabPanel, debounce, bytes, app } = window.JT;

  app.innerHTML = tabBar('ut', [['code', 'Encode / Decode', 'swap'], ['parse', 'URL parser', 'list'], ['utm', 'UTM builder', 'trend'], ['b64', 'Base64', 'hash']]) +
    tabPanel('ut', 'code', `
      <div class="toolbar"><div class="toolbar-group">
        <div class="segmented" role="radiogroup" aria-label="Direction" id="dir"><button type="button" role="radio" data-dir="encode" aria-checked="true">Encode</button><button type="button" role="radio" data-dir="decode" aria-checked="false">Decode</button></div>
        <select class="select select-sm" id="enc-mode" aria-label="Encoding type" style="width:auto"><option value="component">Component (encodeURIComponent)</option><option value="uri">Full URL (encodeURI)</option><option value="form">Form data (spaces → +)</option></select>
        <label class="check-row"><input type="checkbox" id="lines"> Each line separately</label>
      </div><div class="toolbar-group">${btn('swap', 'Swap', { icon: 'swap', ghost: true })}${btn('copy-code', 'Copy result', { icon: 'copy' })}</div></div>
      <div class="panes"><div class="pane"><div class="pane-head">Input</div><textarea class="code" id="code-in" spellcheck="false" style="min-height:260px;white-space:pre-wrap">https://example.com/search?q=roof repair & hail damage&city=Round Rock, TX</textarea></div>
      <div class="pane"><div class="pane-head">Result</div><textarea class="code" id="code-out" spellcheck="false" readonly style="min-height:260px;white-space:pre-wrap;word-break:break-all"></textarea></div></div>`, true) +
    tabPanel('ut', 'parse', `
      <label class="field">URL to inspect<input class="input" id="parse-in" type="url" value="https://www.example.com:443/services/roof-repair/?utm_source=google&utm_medium=cpc&utm_campaign=spring%20promo&gclid=abc123#quote"></label>
      <div id="parse-parts" class="tag-table" style="margin-top:14px"></div>
      <div class="group-title">Query parameters <span>${btn('add-param', 'Add', { icon: 'plus', ghost: true, size: 'btn-xs' })}</span></div>
      <div id="params" class="param-list"></div>
      <div class="toolbar" style="margin-top:14px"><div class="toolbar-group">${btn('strip-tracking', 'Remove tracking params', { icon: 'wand', ghost: true })}${btn('sort-params', 'Sort A–Z', { ghost: true })}</div></div>
      <div class="code-out"><pre id="rebuilt"></pre><button type="button" class="btn btn-xs" id="copy-rebuilt">${icon('copy')}Copy</button></div>`) +
    tabPanel('ut', 'utm', `<div class="side-layout">
      <div class="card" style="display:grid;gap:12px">
        <label class="field">Preset<select class="select" id="utm-preset"><option value="">Choose a preset…</option><option value="google">Google Ads</option><option value="meta">Facebook / Instagram ads</option><option value="gbp">Google Business Profile</option><option value="email">Email newsletter</option><option value="linkedin">LinkedIn post</option><option value="qr">Print / QR code</option><option value="sms">SMS</option></select></label>
        <label class="field">Website URL *<input class="input" id="utm-url" type="url" placeholder="https://example.com/landing-page"></label>
        <label class="field">Campaign source * <small>utm_source — e.g. google, facebook, newsletter</small><input class="input" id="utm-source" list="sources"></label>
        <label class="field">Campaign medium * <small>utm_medium — e.g. cpc, social, email</small><input class="input" id="utm-medium" list="mediums"></label>
        <label class="field">Campaign name * <small>utm_campaign — e.g. spring-sale</small><input class="input" id="utm-campaign"></label>
        <label class="field">Campaign term <small>utm_term — paid keywords</small><input class="input" id="utm-term"></label>
        <label class="field">Campaign content <small>utm_content — ad or link variation</small><input class="input" id="utm-content"></label>
        <label class="field">Campaign ID <small>utm_id</small><input class="input" id="utm-id"></label>
        <div style="display:flex;gap:16px;flex-wrap:wrap"><label class="check-row"><input type="checkbox" id="utm-lower" checked> Lowercase values</label><label class="check-row"><input type="checkbox" id="utm-dash" checked> Spaces → dashes</label></div>
        <datalist id="sources"><option>google</option><option>facebook</option><option>instagram</option><option>linkedin</option><option>newsletter</option><option>bing</option><option>youtube</option><option>tiktok</option><option>gbp</option></datalist>
        <datalist id="mediums"><option>cpc</option><option>paid_social</option><option>social</option><option>email</option><option>organic</option><option>referral</option><option>display</option><option>qr</option><option>sms</option></datalist>
      </div>
      <div style="display:grid;gap:14px;align-content:start;min-width:0">
        <div class="card"><div class="group-title" style="margin-top:0">Your campaign URL</div><div class="utm-result" id="utm-result">Fill in the URL, source, medium and campaign.</div>
          <div class="btn-row" style="margin-top:14px">${btn('utm-copy', 'Copy URL', { icon: 'copy', primary: true })}${btn('utm-save', 'Save to history', { icon: 'plus', ghost: true })}<a class="btn btn-sm btn-ghost" id="utm-open" target="_blank" rel="noopener noreferrer">${icon('arrow')}Test link</a></div>
          <p class="muted" id="utm-warn" style="font-size:13px;margin:12px 0 0"></p></div>
        <div class="card"><div class="group-title" style="margin-top:0">Recent links <span>${btn('utm-csv', 'CSV', { icon: 'download', ghost: true, size: 'btn-xs' })} ${btn('utm-clear', 'Clear', { ghost: true, size: 'btn-xs' })}</span></div><div id="utm-history" class="history"></div></div>
      </div></div>`) +
    tabPanel('ut', 'b64', `
      <div class="toolbar"><div class="toolbar-group">
        <div class="segmented" role="radiogroup" aria-label="Base64 direction" id="b64-dir"><button type="button" role="radio" data-dir="encode" aria-checked="true">Encode</button><button type="button" role="radio" data-dir="decode" aria-checked="false">Decode</button></div>
        <label class="check-row"><input type="checkbox" id="b64-url"> URL-safe (Base64URL)</label>
      </div><div class="toolbar-group">${btn('b64-file', 'File → data URI', { icon: 'upload', ghost: true })}<input type="file" id="b64-input" hidden>${btn('b64-copy', 'Copy result', { icon: 'copy' })}</div></div>
      <div class="panes"><div class="pane"><div class="pane-head">Input</div><textarea class="code" id="b64-in" spellcheck="false" style="min-height:240px;white-space:pre-wrap">Hello from Bohol 🇵🇭 to Texas 🤠</textarea></div>
      <div class="pane"><div class="pane-head">Result <span id="b64-meta"></span></div><textarea class="code" id="b64-out" readonly spellcheck="false" style="min-height:240px;white-space:pre-wrap;word-break:break-all"></textarea></div></div>`);
  tabs($('#ut'));
  const seg = (root, val) => $$('[role="radio"]', root).forEach(b => b.setAttribute('aria-checked', String(b.dataset.dir === val)));

  // ---------- Encode / Decode ----------
  let dir = 'encode';
  const encoders = {
    component: [encodeURIComponent, decodeURIComponent],
    uri: [encodeURI, decodeURI],
    form: [s => encodeURIComponent(s).replace(/%20/g, '+'), s => decodeURIComponent(s.replace(/\+/g, ' '))],
  };
  function codeRun() {
    const [enc, dec] = encoders[$('#enc-mode').value], fn = dir === 'encode' ? enc : dec;
    const input = $('#code-in').value;
    try {
      $('#code-out').value = $('#lines').checked ? input.split('\n').map(fn).join('\n') : fn(input);
      status(`${dir === 'encode' ? 'Encoded' : 'Decoded'} ${input.length.toLocaleString()} characters.`, 'ok');
    } catch { $('#code-out').value = ''; status('This input has malformed percent-encoding (e.g. a % not followed by two hex digits).', 'error'); }
  }
  $$('#dir [role="radio"]').forEach(b => b.addEventListener('click', () => { dir = b.dataset.dir; seg($('#dir'), dir); codeRun(); }));
  $('#enc-mode').addEventListener('change', codeRun); $('#lines').addEventListener('change', codeRun);
  $('#code-in').addEventListener('input', debounce(codeRun, 120));
  $('#swap').addEventListener('click', () => { $('#code-in').value = $('#code-out').value; dir = dir === 'encode' ? 'decode' : 'encode'; seg($('#dir'), dir); codeRun(); });
  $('#copy-code').addEventListener('click', () => copy($('#code-out').value));
  codeRun();

  // ---------- Parser ----------
  let parsedUrl = null;
  const TRACKING = /^(utm_\w+|gclid|gbraid|wbraid|fbclid|msclkid|mc_cid|mc_eid|_hsenc|_hsmi|igshid|yclid|dclid|ttclid|li_fat_id|ref|ref_src)$/i;
  function parseRun() {
    let v = $('#parse-in').value.trim();
    if (v && !/^[a-z][\w+.-]*:/i.test(v)) v = 'https://' + v;
    try { parsedUrl = new URL(v); } catch { parsedUrl = null; $('#parse-parts').innerHTML = '<div><code>error</code><span style="color:var(--danger)">Not a valid URL.</span></div>'; $('#params').innerHTML = ''; $('#rebuilt').textContent = ''; return; }
    paintParams(); rebuild();
  }
  function paintParts() {
    const u = parsedUrl;
    $('#parse-parts').innerHTML = [['protocol', u.protocol], ['host', u.hostname], ['port', u.port || `(default ${u.protocol === 'https:' ? 443 : 80})`], ['path', decodeSafe(u.pathname)], ['query', u.search || '—'], ['fragment', u.hash || '—'], ['origin', u.origin]]
      .map(([k, val]) => `<div><code>${k}</code><span>${esc(val)}</span></div>`).join('');
  }
  const decodeSafe = s => { try { return decodeURIComponent(s); } catch { return s; } };
  function paintParams() {
    const rows = [...parsedUrl.searchParams.entries()];
    $('#params').innerHTML = rows.length ? rows.map(([k, val], i) => paramRow(k, val, i)).join('') : '<p class="muted" style="margin:0">No query parameters.</p>';
  }
  const paramRow = (k, val, i) => `<div class="param-row" data-i="${i}"><input class="input input-sm" data-k value="${esc(k)}" aria-label="Parameter name"><input class="input input-sm" data-v value="${esc(val)}" aria-label="Parameter value">${TRACKING.test(k) ? '<span class="tag">tracking</span>' : '<span></span>'}<button type="button" class="icon-btn" aria-label="Remove parameter">${icon('x')}</button></div>`;
  function rebuild() {
    if (!parsedUrl) return;
    const sp = new URLSearchParams();
    $$('#params .param-row').forEach(r => { const k = $('[data-k]', r).value; if (k) sp.append(k, $('[data-v]', r).value); });
    parsedUrl.search = sp.toString();
    paintParts();
    $('#rebuilt').textContent = parsedUrl.href;
  }
  $('#parse-in').addEventListener('input', debounce(parseRun, 200));
  $('#params').addEventListener('input', debounce(rebuild, 120));
  $('#params').addEventListener('click', e => { if (e.target.closest('.icon-btn')) { e.target.closest('.param-row').remove(); rebuild(); } });
  $('#add-param').addEventListener('click', () => { if (!parsedUrl) return; if ($('#params p')) $('#params').innerHTML = ''; $('#params').insertAdjacentHTML('beforeend', paramRow('', '', Date.now())); $('#params .param-row:last-child [data-k]').focus(); });
  $('#strip-tracking').addEventListener('click', () => { let n = 0; $$('#params .param-row').forEach(r => { if (TRACKING.test($('[data-k]', r).value)) { r.remove(); n++; } }); rebuild(); toast(n ? `Removed ${n} tracking parameter${n === 1 ? '' : 's'}` : 'No tracking parameters found'); });
  $('#sort-params').addEventListener('click', () => { const rows = $$('#params .param-row').sort((a, b) => $('[data-k]', a).value.localeCompare($('[data-k]', b).value)); rows.forEach(r => $('#params').append(r)); rebuild(); });
  $('#copy-rebuilt').addEventListener('click', () => copy($('#rebuilt').textContent));
  parseRun();

  // ---------- UTM builder ----------
  const PRESETS = {
    google: { source: 'google', medium: 'cpc', term: '{keyword}' }, meta: { source: 'facebook', medium: 'paid_social', content: '{{ad.name}}' },
    gbp: { source: 'gbp', medium: 'organic', campaign: 'google-business-profile' }, email: { source: 'newsletter', medium: 'email' },
    linkedin: { source: 'linkedin', medium: 'social' }, qr: { source: 'print', medium: 'qr' }, sms: { source: 'sms', medium: 'sms' },
  };
  const F = ['url', 'source', 'medium', 'campaign', 'term', 'content', 'id'];
  const u = k => $('#utm-' + k);
  const savedForm = store.get('utm:form', {}); F.forEach(k => { if (savedForm[k]) u(k).value = savedForm[k]; });
  let history = store.get('utm:history', []);
  function clean(v) { let s = v.trim(); if ($('#utm-dash').checked) s = s.replace(/\s+/g, '-'); if ($('#utm-lower').checked && !/[{}]/.test(s)) s = s.toLowerCase(); return s; }
  function utmBuild() {
    store.set('utm:form', Object.fromEntries(F.map(k => [k, u(k).value])));
    const raw = u('url').value.trim(), warn = [];
    if (!raw || !u('source').value.trim() || !u('medium').value.trim() || !u('campaign').value.trim()) { $('#utm-result').textContent = 'Fill in the URL, source, medium and campaign.'; $('#utm-result').classList.add('muted'); $('#utm-open').removeAttribute('href'); $('#utm-warn').textContent = ''; return null; }
    let url;
    try { url = new URL(/^https?:\/\//i.test(raw) ? raw : 'https://' + raw); } catch { $('#utm-result').textContent = 'Enter a valid website URL.'; return null; }
    for (const k of F.slice(1)) { const v = u(k).value; if (v.trim()) url.searchParams.set('utm_' + k, clean(v)); else url.searchParams.delete('utm_' + k); }
    if (/[A-Z]/.test(F.slice(1).map(k => u(k).value).join('')) && !$('#utm-lower').checked) warn.push('Mixed case creates separate rows in Google Analytics — keep values lowercase.');
    if (url.hash) warn.push('Fragments (#) stay at the end of the URL, after the UTM parameters.');
    const href = url.href.replace(/%7B/gi, '{').replace(/%7D/gi, '}');
    $('#utm-result').textContent = href; $('#utm-result').classList.remove('muted');
    $('#utm-open').href = href; $('#utm-warn').textContent = warn.join(' ');
    return href;
  }
  function paintHistory() {
    $('#utm-history').innerHTML = history.length ? history.map((h, i) => `<div class="history-row"><div><strong>${esc(h.campaign)}</strong><small>${esc(h.source)} / ${esc(h.medium)} · ${new Date(h.at).toLocaleDateString()}</small><code>${esc(h.url)}</code></div><button type="button" class="icon-btn" data-copy="${i}" aria-label="Copy link">${icon('copy')}</button></div>`).join('') : '<p class="muted" style="margin:0">Saved links appear here (stored only in this browser).</p>';
  }
  F.forEach(k => u(k).addEventListener('input', debounce(utmBuild, 100)));
  ['utm-lower', 'utm-dash'].forEach(id => $('#' + id).addEventListener('change', utmBuild));
  $('#utm-preset').addEventListener('change', e => { const p = PRESETS[e.target.value]; if (!p) return; ['source', 'medium', 'term', 'content'].forEach(k => { u(k).value = p[k] || ''; }); if (p.campaign) u('campaign').value = p.campaign; utmBuild(); e.target.value = ''; toast('Preset applied'); });
  $('#utm-copy').addEventListener('click', () => { const h = utmBuild(); if (h) copy(h, 'Campaign URL copied'); else toast('Complete the required fields first', 'error'); });
  $('#utm-save').addEventListener('click', () => {
    const h = utmBuild(); if (!h) return toast('Complete the required fields first', 'error');
    history = [{ url: h, source: clean(u('source').value), medium: clean(u('medium').value), campaign: clean(u('campaign').value), at: Date.now() }, ...history.filter(x => x.url !== h)].slice(0, 25);
    store.set('utm:history', history); paintHistory(); toast('Saved to history');
  });
  $('#utm-history').addEventListener('click', e => { const b = e.target.closest('[data-copy]'); if (b) copy(history[+b.dataset.copy].url); });
  $('#utm-clear').addEventListener('click', () => { history = []; store.set('utm:history', history); paintHistory(); });
  $('#utm-csv').addEventListener('click', () => { if (!history.length) return toast('No saved links yet', 'error'); download([['Date', 'Campaign', 'Source', 'Medium', 'URL'], ...history.map(h => [new Date(h.at).toISOString().slice(0, 10), h.campaign, h.source, h.medium, h.url])].map(r => r.map(v => `"${String(v).replace(/"/g, '""')}"`).join(',')).join('\r\n'), 'utm-links.csv', 'text/csv;charset=utf-8'); });
  utmBuild(); paintHistory();

  // ---------- Base64 ----------
  let bdir = 'encode';
  const toB64 = str => { const b = new TextEncoder().encode(str); let s = ''; for (let i = 0; i < b.length; i += 8192) s += String.fromCharCode(...b.subarray(i, i + 8192)); return btoa(s); };
  const fromB64 = str => { let s = str.trim().replace(/\s+/g, '').replace(/-/g, '+').replace(/_/g, '/'); s = s.replace(/^data:[^,]*,/, ''); while (s.length % 4) s += '='; return new TextDecoder('utf-8', { fatal: true }).decode(Uint8Array.from(atob(s), c => c.charCodeAt(0))); };
  function b64Run() {
    const v = $('#b64-in').value;
    try {
      let r = bdir === 'encode' ? toB64(v) : fromB64(v);
      if (bdir === 'encode' && $('#b64-url').checked) r = r.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
      $('#b64-out').value = r; $('#b64-meta').textContent = `${r.length.toLocaleString()} chars`; status(bdir === 'encode' ? 'Encoded as UTF-8 Base64.' : 'Decoded Base64 to text.', 'ok');
    } catch { $('#b64-out').value = ''; $('#b64-meta').textContent = ''; status('That is not valid Base64, or it decodes to binary data rather than UTF-8 text.', 'error'); }
  }
  $$('#b64-dir [role="radio"]').forEach(b => b.addEventListener('click', () => { bdir = b.dataset.dir; seg($('#b64-dir'), bdir); b64Run(); }));
  $('#b64-in').addEventListener('input', debounce(b64Run, 120)); $('#b64-url').addEventListener('change', b64Run);
  $('#b64-copy').addEventListener('click', () => copy($('#b64-out').value));
  $('#b64-file').addEventListener('click', () => $('#b64-input').click());
  $('#b64-input').addEventListener('change', () => {
    const f = $('#b64-input').files[0]; $('#b64-input').value = ''; if (!f) return;
    if (f.size > 5 * 1024 * 1024) return toast('Files up to 5 MB, please', 'error');
    const r = new FileReader();
    r.onload = () => { $('#b64-out').value = r.result; $('#b64-meta').textContent = `${f.name} · ${bytes(f.size)} → ${bytes(r.result.length)}`; status('Data URI ready — paste it into CSS or HTML.', 'ok'); };
    r.readAsDataURL(f);
  });
  b64Run();
  status('Converts as you type. Nothing leaves your browser.');
})();
