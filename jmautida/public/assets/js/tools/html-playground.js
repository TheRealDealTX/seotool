/* HTML/CSS/JS playground with sandboxed live preview, console capture, templates, autosave and share links. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, debounce, tabIndent, app } = window.JT;

  const TEMPLATES = {
    starter: { name: 'Starter', html: '<main class="card">\n  <span class="badge">✦ Live preview</span>\n  <h1>Make something good.</h1>\n  <p>Edit the HTML, CSS and JavaScript tabs — the preview updates as you type.</p>\n  <button id="hello">Say hello</button>\n</main>', css: 'body {\n  margin: 0;\n  min-height: 100vh;\n  display: grid;\n  place-items: center;\n  font-family: system-ui, sans-serif;\n  background: radial-gradient(circle at 20% 20%, #1d2b3a, #06080c 60%);\n  color: #e9edf3;\n}\n.card {\n  max-width: 420px;\n  padding: 36px;\n  border-radius: 20px;\n  background: rgba(255,255,255,.05);\n  border: 1px solid rgba(255,255,255,.1);\n}\n.badge { font: 12px monospace; color: #4ff0b4; }\nh1 { font-size: 40px; line-height: 1; margin: 14px 0; }\nbutton {\n  padding: 12px 18px;\n  border: 0;\n  border-radius: 10px;\n  background: #4ff0b4;\n  font-weight: 700;\n  cursor: pointer;\n}', js: "const button = document.querySelector('#hello');\nlet clicks = 0;\nbutton.addEventListener('click', () => {\n  clicks++;\n  button.textContent = `Hello ×${clicks} 👋`;\n  console.log('Button clicked', { clicks });\n});" },
    blank: { name: 'Blank', html: '', css: '', js: '' },
    hero: { name: 'Landing hero', html: '<header class="nav"><strong>Brand</strong><nav><a href="#">Features</a><a href="#">Pricing</a><a class="cta" href="#">Get started</a></nav></header>\n<section class="hero">\n  <p class="eyebrow">New · Version 2.0</p>\n  <h1>Build faster websites<br>without the busywork.</h1>\n  <p class="lead">A short, benefit-driven subheading that explains what you do and who it is for.</p>\n  <div class="actions"><a class="cta" href="#">Start free</a><a href="#">See a demo →</a></div>\n</section>', css: '* { box-sizing: border-box; }\nbody { margin: 0; font-family: Inter, system-ui, sans-serif; background: #fff; color: #0c111b; }\n.nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 6vw; }\n.nav nav { display: flex; gap: 22px; align-items: center; }\na { color: inherit; text-decoration: none; }\n.cta { background: #0c111b; color: #fff; padding: 10px 16px; border-radius: 10px; }\n.hero { padding: 12vh 6vw; max-width: 900px; }\n.eyebrow { color: #078a5c; font-weight: 600; }\nh1 { font-size: clamp(36px, 6vw, 68px); line-height: 1.02; letter-spacing: -0.03em; margin: 10px 0 18px; }\n.lead { font-size: 20px; color: #4a5568; max-width: 560px; }\n.actions { display: flex; gap: 18px; align-items: center; margin-top: 28px; }', js: '' },
    grid: { name: 'Card grid', html: '<section class="grid" id="grid"></section>', css: 'body { margin: 0; padding: 32px; font-family: system-ui, sans-serif; background: #f5f6f8; }\n.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }\n.card { background: #fff; border-radius: 16px; padding: 20px; box-shadow: 0 10px 30px -15px rgba(0,0,0,.25); transition: transform .2s; }\n.card:hover { transform: translateY(-4px); }\n.swatch { height: 110px; border-radius: 12px; margin-bottom: 14px; }\nh3 { margin: 0 0 6px; }\np { margin: 0; color: #666; font-size: 14px; }', js: "const grid = document.getElementById('grid');\nconst items = ['Design', 'Develop', 'Deploy', 'Measure', 'Improve', 'Repeat'];\nitems.forEach((name, i) => {\n  const hue = i * 55;\n  grid.insertAdjacentHTML('beforeend', `<article class=\"card\"><div class=\"swatch\" style=\"background:linear-gradient(135deg,hsl(${hue} 80% 60%),hsl(${hue + 40} 80% 50%))\"></div><h3>${name}</h3><p>Step ${i + 1} of the process.</p></article>`);\n});\nconsole.log(`Rendered ${items.length} cards`);" },
    flex: { name: 'Flexbox demo', html: '<div class="controls">\n  <label>justify-content\n    <select id="jc"><option>flex-start</option><option>center</option><option>flex-end</option><option>space-between</option><option>space-around</option><option>space-evenly</option></select>\n  </label>\n  <label>align-items\n    <select id="ai"><option>stretch</option><option>flex-start</option><option>center</option><option>flex-end</option></select>\n  </label>\n</div>\n<div class="box" id="box"><div>1</div><div>2</div><div>3</div></div>', css: 'body { font-family: system-ui, sans-serif; padding: 24px; background: #0b0e14; color: #e9edf3; }\n.controls { display: flex; gap: 16px; margin-bottom: 16px; }\nlabel { display: grid; gap: 6px; font: 13px monospace; }\n.box { display: flex; height: 260px; gap: 10px; padding: 10px; border: 2px dashed #4ff0b4; border-radius: 12px; }\n.box div { min-width: 70px; padding: 18px; background: #8f7dff; border-radius: 10px; font-weight: 700; text-align: center; }', js: "const box = document.getElementById('box');\nfor (const id of ['jc', 'ai']) {\n  document.getElementById(id).addEventListener('change', e => {\n    box.style[id === 'jc' ? 'justifyContent' : 'alignItems'] = e.target.value;\n    console.log(id === 'jc' ? 'justify-content:' : 'align-items:', e.target.value);\n  });\n}" },
    anim: { name: 'CSS animation', html: '<div class="loader"><span></span><span></span><span></span></div>\n<p>Pure CSS keyframes</p>', css: 'body { margin: 0; min-height: 100vh; display: grid; place-content: center; gap: 18px; background: #06080c; color: #8790a1; font-family: monospace; text-align: center; }\n.loader { display: flex; gap: 10px; justify-content: center; }\n.loader span { width: 18px; height: 18px; border-radius: 50%; background: #4ff0b4; animation: bounce 1s infinite ease-in-out; }\n.loader span:nth-child(2) { animation-delay: .15s; background: #5fd3ff; }\n.loader span:nth-child(3) { animation-delay: .3s; background: #8f7dff; }\n@keyframes bounce { 0%, 100% { transform: translateY(0); opacity: .5; } 50% { transform: translateY(-24px); opacity: 1; } }', js: '' },
  };

  app.innerHTML = `
    <div class="toolbar">
      <div class="toolbar-group">
        <select class="select select-sm" id="template" aria-label="Load a template" style="width:auto"><option value="">Templates…</option>${Object.entries(TEMPLATES).map(([k, t]) => `<option value="${k}">${esc(t.name)}</option>`).join('')}</select>
        ${btn('run', 'Run', { icon: 'play', primary: true, title: 'Run (Ctrl/⌘ + Enter)' })}
        <label class="check-row"><input type="checkbox" id="auto" checked> Auto-run</label>
      </div>
      <div class="toolbar-group">
        <select class="select select-sm" id="device" aria-label="Preview width" style="width:auto"><option value="100%">Responsive</option><option value="1280px">Laptop · 1280</option><option value="768px">Tablet · 768</option><option value="390px">Mobile · 390</option></select>
        <button type="button" class="icon-btn" id="layout" aria-label="Toggle side-by-side or stacked layout" title="Toggle layout">${icon('columns')}</button>
        <button type="button" class="icon-btn" id="full" aria-label="Fullscreen preview" title="Fullscreen preview">${icon('maximize')}</button>
        ${btn('share', 'Share', { icon: 'share', ghost: true })}${btn('save', 'Download', { icon: 'download', ghost: true })}
      </div>
    </div>
    <div class="panes playground" id="panes">
      <div class="pane">
        <div class="pane-head" style="padding-left:6px"><div class="tabs sub" role="tablist" id="code-tabs" style="margin:0;border:0;background:transparent">
          ${['html', 'css', 'js'].map((k, i) => `<button type="button" class="tab" role="tab" id="t-${k}" aria-selected="${i === 0}" aria-controls="ed-${k}" data-tab="${k}" tabindex="${i === 0 ? 0 : -1}">${k.toUpperCase()}</button>`).join('')}
        </div><button type="button" class="btn btn-xs btn-ghost" id="reset">Reset</button></div>
        ${['html', 'css', 'js'].map((k, i) => `<textarea class="code" id="ed-${k}" role="tabpanel" aria-labelledby="t-${k}" spellcheck="false" autocapitalize="off" autocomplete="off"${i ? ' hidden' : ''} placeholder="${k === 'html' ? '<!-- Markup goes here -->' : k === 'css' ? '/* Styles go here */' : '// JavaScript goes here'}"></textarea>`).join('')}
      </div>
      <div class="pane preview-pane" id="preview-pane">
        <div class="pane-head"><span>Preview <span id="dims" class="muted"></span></span><button type="button" class="btn btn-xs btn-ghost" id="exit-full" hidden>Exit fullscreen</button></div>
        <div class="preview-wrap"><iframe id="preview" title="Live preview of your code" sandbox="allow-scripts allow-modals" referrerpolicy="no-referrer"></iframe></div>
        <div class="console" id="console-wrap"><div class="console-head"><span>${icon('terminal')} Console <b id="console-count"></b></span><button type="button" class="btn btn-xs btn-ghost" id="console-clear">Clear</button></div><div class="console-log" id="console" role="log" aria-live="polite"></div></div>
      </div>
    </div>`;

  const ed = { html: $('#ed-html'), css: $('#ed-css'), js: $('#ed-js') };
  const frame = $('#preview');
  Object.values(ed).forEach(t => tabIndent(t));
  window.JT.tabs($('#code-tabs'));

  let token = '';
  function compose(forPreview) {
    const html = ed.html.value, css = ed.css.value, js = ed.js.value;
    token = Math.random().toString(36).slice(2);
    const bridge = forPreview ? `<script>(function(){var T=${JSON.stringify(token)};function s(t,a){try{parent.postMessage({__jm:T,type:t,args:[].map.call(a,function(x){try{if(x instanceof Error)return x.name+': '+x.message;return typeof x==='object'?JSON.stringify(x,null,1):String(x)}catch(e){return String(x)}})},'*')}catch(e){}}['log','info','warn','error','debug'].forEach(function(k){var o=console[k];console[k]=function(){s(k,arguments);o.apply(console,arguments)}});addEventListener('error',function(e){s('error',[e.message+(e.lineno?' (line '+e.lineno+')':'')])});addEventListener('unhandledrejection',function(e){s('error',['Unhandled promise rejection: '+(e.reason&&e.reason.message||e.reason)])})})();<\/script>` : '';
    const style = css ? `<style>\n${css}\n</style>` : '';
    const script = js ? `<script>\n${js.replace(/<\/script/gi, '<\\/script')}\n<\/script>` : '';
    if (/<html[\s>]/i.test(html) || /<!doctype/i.test(html)) {
      let doc = html;
      doc = /<\/head>/i.test(doc) ? doc.replace(/<\/head>/i, `${bridge}${style}</head>`) : doc.replace(/<html[^>]*>/i, m => `${m}<head>${bridge}${style}</head>`);
      doc = /<\/body>/i.test(doc) ? doc.replace(/<\/body>(?![\s\S]*<\/body>)/i, `${script}</body>`) : doc + script;
      return doc;
    }
    return `<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>Playground</title>\n${bridge}${style}\n</head>\n<body>\n${html}\n${script}\n</body>\n</html>`;
  }
  let logs = 0;
  function log(type, args) {
    const el = document.createElement('div'); el.className = `log ${type}`;
    el.textContent = args.join(' ');
    $('#console').append(el); $('#console').scrollTop = 1e9;
    logs++; $('#console-count').textContent = `(${logs})`;
    if ($('#console').children.length > 300) $('#console').firstChild.remove();
  }
  addEventListener('message', e => {
    if (e.source !== frame.contentWindow || !e.data || e.data.__jm !== token) return;
    log(String(e.data.type), Array.isArray(e.data.args) ? e.data.args.map(String) : []);
  });
  function run() {
    $('#console').innerHTML = ''; logs = 0; $('#console-count').textContent = '';
    frame.srcdoc = compose(true);
    store.set('play:code', { html: ed.html.value, css: ed.css.value, js: ed.js.value });
    status('Preview updated. Code runs in an isolated sandbox.');
  }
  const autoRun = debounce(() => { if ($('#auto').checked) run(); }, 450);
  Object.values(ed).forEach(t => {
    t.addEventListener('input', () => { autoRun(); store.set('play:code', { html: ed.html.value, css: ed.css.value, js: ed.js.value }); });
    t.addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); run(); } });
  });
  function load(code) { ed.html.value = code.html || ''; ed.css.value = code.css || ''; ed.js.value = code.js || ''; run(); }

  // Share links: deflate-compressed JSON in the URL hash.
  const b64 = arr => { let s = ''; for (let i = 0; i < arr.length; i += 8192) s += String.fromCharCode(...arr.subarray(i, i + 8192)); return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, ''); };
  const unb64 = s => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/')), c => c.charCodeAt(0));
  async function pack(obj) {
    const raw = new TextEncoder().encode(JSON.stringify(obj));
    if (!window.CompressionStream) return 'r' + b64(raw);
    const stream = new Blob([raw]).stream().pipeThrough(new CompressionStream('deflate-raw'));
    return 'z' + b64(new Uint8Array(await new Response(stream).arrayBuffer()));
  }
  async function unpack(str) {
    const kind = str[0], data = unb64(str.slice(1));
    if (kind === 'r') return JSON.parse(new TextDecoder().decode(data));
    const stream = new Blob([data]).stream().pipeThrough(new DecompressionStream('deflate-raw'));
    return JSON.parse(await new Response(stream).text());
  }
  $('#share').addEventListener('click', async () => {
    try {
      const hash = await pack({ html: ed.html.value, css: ed.css.value, js: ed.js.value });
      const url = `${location.origin}${location.pathname}#code=${hash}`;
      if (url.length > 60000) { toast('Code is too large for a link — download it instead', 'error'); return; }
      history.replaceState(null, '', `#code=${hash}`);
      copy(url, 'Share link copied');
    } catch { toast('Could not create a share link', 'error'); }
  });
  $('#save').addEventListener('click', () => download(compose(false), 'playground.html', 'text/html;charset=utf-8'));
  $('#run').addEventListener('click', run);
  $('#template').addEventListener('change', e => {
    const t = TEMPLATES[e.target.value]; e.target.value = '';
    if (!t) return;
    if ((ed.html.value || ed.css.value || ed.js.value) && !confirm(`Replace your current code with the “${t.name}” template?`)) return;
    load(t); toast(`Loaded ${t.name}`);
  });
  $('#reset').addEventListener('click', () => { if (confirm('Reset to the starter example? Your current code will be replaced.')) load(TEMPLATES.starter); });
  $('#device').addEventListener('change', e => { frame.style.width = e.target.value; frame.parentElement.classList.toggle('framed', e.target.value !== '100%'); sizeLabel(); });
  $('#layout').addEventListener('click', () => { const s = $('#panes').classList.toggle('stack'); $('#layout').innerHTML = icon(s ? 'rows' : 'columns'); store.set('play:stack', s); });
  if (store.get('play:stack')) { $('#panes').classList.add('stack'); $('#layout').innerHTML = icon('rows'); }
  const setFull = on => { $('#preview-pane').classList.toggle('fullscreen', on); $('#exit-full').hidden = !on; document.body.style.overflow = on ? 'hidden' : ''; };
  $('#full').addEventListener('click', () => setFull(true));
  $('#exit-full').addEventListener('click', () => setFull(false));
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && $('#preview-pane').classList.contains('fullscreen')) setFull(false); });
  $('#console-clear').addEventListener('click', () => { $('#console').innerHTML = ''; logs = 0; $('#console-count').textContent = ''; });
  const sizeLabel = () => { $('#dims').textContent = `· ${Math.round(frame.getBoundingClientRect().width)}px`; };
  new ResizeObserver(sizeLabel).observe(frame);

  (async () => {
    const m = location.hash.match(/^#code=(.+)$/);
    if (m) { try { load(await unpack(m[1])); toast('Loaded shared code'); return; } catch { toast('This share link is invalid or incomplete', 'error'); } }
    load(store.get('play:code') || TEMPLATES.starter);
  })();
})();
