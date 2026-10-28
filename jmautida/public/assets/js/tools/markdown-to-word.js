/* Markdown to Word: toolbar editor, sanitized live preview, DOCX/HTML/rich-text export. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, debounce, dropTarget, tabIndent, app } = window.JT;
  if (!window.marked || !window.docx) { app.innerHTML = '<div class="empty"><h3>Document libraries did not load.</h3><p>Please reload the page.</p></div>'; return; }
  const SAMPLE = '# Website project brief\n\nPrepared by **J & J Web Marketing** for a new client.\n\n## Goals\n\n1. Launch a fast, mobile-first website.\n2. Rank for *roof repair* searches in the local area.\n3. Turn visitors into booked inspections.\n\n## Scope\n\n- [x] Discovery call\n- [x] Sitemap and wireframes\n- [ ] Design and development\n- [ ] SEO setup and launch\n\n> Good websites get out of the way of good businesses.\n\n## Timeline\n\n| Phase | Deliverable | Weeks |\n| --- | --- | --- |\n| Design | Homepage and key templates | 2 |\n| Build | Responsive website | 3 |\n| Launch | SEO, analytics and training | 1 |\n\n```\nnpm run build\n```\n\nQuestions? Visit [jmautida.com](https://jmautida.com/contact).';
  const settings = Object.assign({ name: 'document', font: 'Calibri', size: 11, page: 'letter', numbers: true }, store.get('md:settings', {}));

  const tb = (act, label, title) => `<button type="button" class="btn btn-xs btn-ghost md-btn" data-act="${act}" title="${title}" aria-label="${title}">${label}</button>`;
  app.innerHTML = `
    <div class="toolbar">
      <div class="toolbar-group md-tools" role="toolbar" aria-label="Formatting">
        ${tb('h1', 'H1', 'Heading 1')}${tb('h2', 'H2', 'Heading 2')}${tb('h3', 'H3', 'Heading 3')}<span class="sep"></span>
        ${tb('bold', '<b>B</b>', 'Bold (Ctrl/⌘ + B)')}${tb('italic', '<i>I</i>', 'Italic (Ctrl/⌘ + I)')}${tb('strike', '<s>S</s>', 'Strikethrough')}${tb('code', '&lt;/&gt;', 'Inline code')}<span class="sep"></span>
        ${tb('ul', '• List', 'Bullet list')}${tb('ol', '1. List', 'Numbered list')}${tb('task', '☑ Task', 'Task list')}${tb('quote', '❝', 'Quote')}<span class="sep"></span>
        ${tb('link', 'Link', 'Link (Ctrl/⌘ + K)')}${tb('table', 'Table', 'Insert table')}${tb('hr', '—', 'Divider')}${tb('pre', '{ }', 'Code block')}
      </div>
      <div class="toolbar-group">${btn('import', 'Open', { icon: 'upload', ghost: true })}${btn('sample', 'Sample', { ghost: true })}<input type="file" id="file" accept=".md,.markdown,.txt,text/plain,text/markdown" hidden></div>
    </div>
    <div class="panes">
      <div class="pane"><div class="pane-head"><span>Markdown</span><span id="md-stats"></span></div><textarea class="code" id="source" spellcheck="true" aria-label="Markdown source" style="white-space:pre-wrap;min-height:520px"></textarea></div>
      <div class="pane"><div class="pane-head"><span>Document preview</span><span class="muted" id="page-label"></span></div><div class="document-preview" id="document"></div></div>
    </div>
    <div class="card md-export" style="margin-top:14px">
      <div class="form-grid" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">
        <label class="field">File name<input class="input input-sm" id="doc-name" maxlength="80"></label>
        <label class="field">Font<select class="select select-sm" id="doc-font"><option>Calibri</option><option>Arial</option><option>Aptos</option><option>Georgia</option><option>Times New Roman</option><option>Garamond</option><option>Verdana</option></select></label>
        <label class="field">Size<select class="select select-sm" id="doc-size">${[10, 10.5, 11, 12, 13, 14].map(s => `<option value="${s}">${s} pt</option>`).join('')}</select></label>
        <label class="field">Page<select class="select select-sm" id="doc-page"><option value="letter">US Letter</option><option value="a4">A4</option></select></label>
        <label class="check-row" style="align-self:end;height:36px"><input type="checkbox" id="doc-numbers"> Page numbers</label>
      </div>
      <div class="btn-row" style="margin-top:16px">${btn('export', 'Export Word (.docx)', { icon: 'download', primary: true })}${btn('rich', 'Copy rich text', { icon: 'copy', ghost: true, title: 'Paste into Google Docs, Gmail or Outlook' })}${btn('html', 'HTML', { icon: 'code', ghost: true })}${btn('save-md', 'Markdown', { icon: 'file', ghost: true })}</div>
    </div>`;

  const src = $('#source');
  tabIndent(src);
  $('#doc-name').value = settings.name; $('#doc-font').value = settings.font; $('#doc-size').value = String(settings.size); $('#doc-page').value = settings.page; $('#doc-numbers').checked = settings.numbers;

  // Sanitize marked's output with a strict allowlist; images become alt-text placeholders.
  function fragment(text) {
    const raw = new DOMParser().parseFromString(marked.parse(text, { gfm: true, breaks: false }), 'text/html');
    const allowed = new Set('P H1 H2 H3 H4 H5 H6 STRONG EM B I S DEL CODE PRE BLOCKQUOTE UL OL LI TABLE THEAD TBODY TR TD TH HR BR A'.split(' '));
    function clean(node) {
      if (node.nodeType === Node.TEXT_NODE) return document.createTextNode(node.textContent);
      if (node.nodeType !== Node.ELEMENT_NODE) return document.createTextNode('');
      if (node.tagName === 'IMG') return document.createTextNode(`[Image: ${node.getAttribute('alt') || 'image'}]`);
      if (node.tagName === 'INPUT' && node.getAttribute('type') === 'checkbox') return document.createTextNode(node.hasAttribute('checked') ? '☑ ' : '☐ ');
      if (!allowed.has(node.tagName)) return document.createTextNode(node.textContent || '');
      const el = document.createElement(node.tagName.toLowerCase());
      if (node.tagName === 'A') { const href = (node.getAttribute('href') || '').trim(); if (/^(https?:\/\/|mailto:)/i.test(href)) { el.setAttribute('href', href); el.setAttribute('target', '_blank'); el.setAttribute('rel', 'noopener noreferrer'); } }
      if (node.tagName === 'OL' && /^\d{1,6}$/.test(node.getAttribute('start') || '')) el.setAttribute('start', node.getAttribute('start'));
      if (/^T[DH]$/.test(node.tagName) && /^(left|center|right)$/.test(node.getAttribute('align') || '')) el.setAttribute('align', node.getAttribute('align'));
      node.childNodes.forEach(c => el.append(clean(c)));
      return el;
    }
    const f = document.createDocumentFragment(); raw.body.childNodes.forEach(n => f.append(clean(n))); return f;
  }
  function render() {
    const doc = $('#document');
    doc.replaceChildren(fragment(src.value));
    doc.style.fontFamily = `"${settings.font}", sans-serif`; doc.style.fontSize = `${settings.size * 1.333}px`;
    $('#page-label').textContent = `${settings.font} · ${settings.size}pt · ${settings.page === 'a4' ? 'A4' : 'Letter'}`;
    const words = (src.value.match(/[\p{L}\p{N}]+(?:['’-][\p{L}\p{N}]+)*/gu) || []).length;
    $('#md-stats').textContent = `${words.toLocaleString()} words · ${Math.max(words ? 1 : 0, Math.round(words / 238))} min read`;
    store.set('md:draft', src.value.length < 300000 ? src.value : '');
  }
  const saveSettings = () => {
    Object.assign(settings, { name: $('#doc-name').value.trim() || 'document', font: $('#doc-font').value, size: Number($('#doc-size').value), page: $('#doc-page').value, numbers: $('#doc-numbers').checked });
    store.set('md:settings', settings); render();
  };
  ['doc-name', 'doc-font', 'doc-size', 'doc-page', 'doc-numbers'].forEach(id => $('#' + id).addEventListener('change', saveSettings));

  // Toolbar actions
  function wrap(before, after = before, placeholder = 'text') {
    const s = src.selectionStart, e = src.selectionEnd, sel = src.value.slice(s, e) || placeholder;
    src.setRangeText(before + sel + after, s, e, 'end');
    src.setSelectionRange(s + before.length, s + before.length + sel.length); src.focus(); render();
  }
  function linePrefix(prefix, numbered) {
    const s = src.selectionStart, e = src.selectionEnd, v = src.value;
    const start = v.lastIndexOf('\n', s - 1) + 1, endIdx = v.indexOf('\n', e), end = endIdx < 0 ? v.length : endIdx;
    let n = 1;
    const out = v.slice(start, end).split('\n').map(l => (numbered ? `${n++}. ` : prefix) + l.replace(/^(#{1,6} |> |- \[[ x]\] |[-*+] |\d+\. )/, '')).join('\n');
    src.setRangeText(out, start, end, 'select'); src.focus(); render();
  }
  function insertBlock(text) { const s = src.selectionStart, before = src.value.slice(0, s); const lead = before && !before.endsWith('\n\n') ? (before.endsWith('\n') ? '\n' : '\n\n') : ''; src.setRangeText(lead + text + '\n', s, src.selectionEnd, 'end'); src.focus(); render(); }
  const ACTIONS = {
    h1: () => linePrefix('# '), h2: () => linePrefix('## '), h3: () => linePrefix('### '),
    bold: () => wrap('**'), italic: () => wrap('*'), strike: () => wrap('~~'), code: () => wrap('`', '`', 'code'),
    ul: () => linePrefix('- '), ol: () => linePrefix('', true), task: () => linePrefix('- [ ] '), quote: () => linePrefix('> '),
    link: () => { const s = src.selectionStart, e = src.selectionEnd, sel = src.value.slice(s, e) || 'link text'; src.setRangeText(`[${sel}](https://)`, s, e, 'end'); const p = s + sel.length + 3; src.setSelectionRange(p, p + 8); src.focus(); render(); },
    table: () => insertBlock('| Column 1 | Column 2 | Column 3 |\n| --- | --- | --- |\n| Cell | Cell | Cell |\n| Cell | Cell | Cell |'),
    hr: () => insertBlock('---'), pre: () => wrap('```\n', '\n```', 'code'),
  };
  $$('.md-btn').forEach(b => b.addEventListener('click', () => ACTIONS[b.dataset.act]()));
  src.addEventListener('keydown', e => {
    if (!(e.ctrlKey || e.metaKey)) return;
    const k = e.key.toLowerCase();
    if (k === 'b') { e.preventDefault(); ACTIONS.bold(); } else if (k === 'i') { e.preventDefault(); ACTIONS.italic(); } else if (k === 'k') { e.preventDefault(); e.stopPropagation(); ACTIONS.link(); }
  });
  src.addEventListener('input', debounce(render, 150));

  const readFile = async f => {
    if (!f) return;
    if (f.size > 2 * 1024 * 1024) return toast('Please choose a file under 2 MB', 'error');
    try { src.value = await f.text(); $('#doc-name').value = f.name.replace(/\.[^.]+$/, '') || 'document'; saveSettings(); toast(`Opened ${f.name}`); } catch { toast('This file could not be read', 'error'); }
  };
  $('#import').addEventListener('click', () => $('#file').click());
  $('#file').addEventListener('change', () => { readFile($('#file').files[0]); $('#file').value = ''; });
  dropTarget(src.parentElement, files => readFile(files[0]));
  $('#sample').addEventListener('click', () => { src.value = SAMPLE; render(); });

  const fileBase = () => (settings.name || 'document').replace(/[\\/:*?"<>|]+/g, '-');
  $('#save-md').addEventListener('click', () => download(src.value, fileBase() + '.md', 'text/markdown;charset=utf-8'));
  const styledHTML = () => {
    const css = `body{font-family:"${settings.font}",Arial,sans-serif;font-size:${settings.size}pt;line-height:1.55;color:#111;max-width:760px;margin:40px auto;padding:0 20px}h1,h2,h3{line-height:1.2}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px 10px;text-align:left}th{background:#f3f4f6}blockquote{border-left:4px solid #ddd;margin:0;padding-left:16px;color:#555;font-style:italic}pre{background:#f6f8fa;padding:12px;border-radius:6px;overflow:auto}code{font-family:Consolas,monospace;font-size:.92em}`;
    const title = $('#document h1')?.textContent || settings.name;
    return `<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<title>${esc(title)}</title>\n<style>${css}</style>\n</head>\n<body>\n${$('#document').innerHTML}\n</body>\n</html>`;
  };
  $('#html').addEventListener('click', () => download(styledHTML(), fileBase() + '.html', 'text/html;charset=utf-8'));
  $('#rich').addEventListener('click', async () => {
    const htmlDoc = styledHTML();
    try {
      if (!window.ClipboardItem) throw 0;
      await navigator.clipboard.write([new ClipboardItem({ 'text/html': new Blob([htmlDoc], { type: 'text/html' }), 'text/plain': new Blob([$('#document').innerText], { type: 'text/plain' }) })]);
      toast('Rich text copied — paste into Google Docs or email');
    } catch {
      const sel = getSelection(), range = document.createRange(); range.selectNodeContents($('#document')); sel.removeAllRanges(); sel.addRange(range);
      const ok = document.execCommand('copy'); sel.removeAllRanges(); toast(ok ? 'Rich text copied' : 'Copy failed — select the preview and copy manually', ok ? 'ok' : 'error');
    }
  });

  // DOCX export
  $('#export').addEventListener('click', async () => {
    render(); $('#export').disabled = true; status('Building your Word document…');
    try {
      const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ExternalHyperlink, Footer, AlignmentType, PageNumber, BorderStyle, ShadingType } = docx;
      const half = Math.round(settings.size * 2);
      function runs(node, opts = {}) {
        if (node.nodeType === Node.TEXT_NODE) return node.textContent ? [new TextRun({ ...opts, text: node.textContent })] : [];
        if (node.nodeType !== Node.ELEMENT_NODE) return [];
        const tag = node.tagName;
        if (tag === 'BR') return [new TextRun({ ...opts, break: 1 })];
        const style = { ...opts, ...(['STRONG', 'B', 'TH'].includes(tag) ? { bold: true } : {}), ...(['EM', 'I'].includes(tag) ? { italics: true } : {}), ...(['DEL', 'S'].includes(tag) ? { strike: true } : {}), ...(tag === 'CODE' ? { font: 'Consolas', size: half - 2, shading: { type: ShadingType.CLEAR, fill: 'F2F4F7' } } : {}) };
        const children = [...node.childNodes].flatMap(n => runs(n, style));
        if (tag === 'A' && node.hasAttribute('href')) return [new ExternalHyperlink({ link: node.getAttribute('href'), children: children.map(c => c) })];
        return children;
      }
      function blocks(container, depth = 0) {
        return [...container.childNodes].flatMap(node => {
          if (node.nodeType === Node.TEXT_NODE) return node.textContent.trim() ? [new Paragraph({ children: runs(node) })] : [];
          if (node.nodeType !== Node.ELEMENT_NODE) return [];
          const tag = node.tagName;
          if (tag === 'UL' || tag === 'OL') {
            let index = Number(node.getAttribute('start') || 1);
            return [...node.children].flatMap(li => {
              const inline = [...li.childNodes].filter(n => !['UL', 'OL'].includes(n.tagName)).flatMap(n => (n.tagName === 'P' ? [...n.childNodes].flatMap(c => runs(c)) : runs(n)));
              const task = /^[☑☐]/.test(li.textContent.trim());
              const para = new Paragraph({ children: tag === 'OL' ? [new TextRun(`${index++}. `), ...inline] : inline, ...(tag === 'UL' && !task ? { bullet: { level: Math.min(depth, 8) } } : { indent: { left: 360 * (depth + 1) } }), spacing: { after: 80 } });
              return [para, ...[...li.children].filter(n => ['UL', 'OL'].includes(n.tagName)).flatMap(n => { const holder = document.createElement('div'); holder.append(n.cloneNode(true)); return blocks(holder, depth + 1); })];
            });
          }
          if (tag === 'TABLE') {
            const rows = [...node.querySelectorAll('tr')];
            return [new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, rows: rows.map((row, ri) => new TableRow({ tableHeader: ri === 0 && !!row.querySelector('th'), children: [...row.children].map(cell => new TableCell({ shading: cell.tagName === 'TH' ? { type: ShadingType.CLEAR, fill: 'F3F4F6' } : undefined, margins: { top: 60, bottom: 60, left: 100, right: 100 }, children: [new Paragraph({ alignment: cell.getAttribute('align') === 'center' ? AlignmentType.CENTER : cell.getAttribute('align') === 'right' ? AlignmentType.RIGHT : AlignmentType.LEFT, children: runs(cell) })] })) })) }), new Paragraph({ text: '', spacing: { after: 120 } })];
          }
          if (tag === 'BLOCKQUOTE') return [...node.children].length ? [...node.childNodes].filter(n => n.nodeType === 1 || n.textContent.trim()).map(n => new Paragraph({ children: runs(n, { italics: true, color: '555555' }), indent: { left: 480 }, border: { left: { style: BorderStyle.SINGLE, size: 12, color: 'CCCCCC', space: 12 } }, spacing: { after: 160 } })) : [new Paragraph({ children: runs(node, { italics: true }), indent: { left: 480 } })];
          if (tag === 'PRE') return node.textContent.replace(/\n$/, '').split('\n').map(line => new Paragraph({ shading: { type: ShadingType.CLEAR, fill: 'F6F8FA' }, spacing: { after: 0 }, children: [new TextRun({ text: line || ' ', font: 'Consolas', size: half - 2 })] }));
          if (tag === 'HR') return [new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'CCCCCC', space: 1 } }, spacing: { after: 200 } })];
          return [new Paragraph({ children: runs(node), ...(/^H[1-6]$/.test(tag) ? { heading: HeadingLevel['HEADING_' + tag[1]] } : {}), spacing: { after: 160 } })];
        });
      }
      const children = blocks($('#document'));
      const size = settings.page === 'a4' ? { width: 11906, height: 16838 } : { width: 12240, height: 15840 };
      const footers = settings.numbers ? { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: ['Page ', PageNumber.CURRENT, ' of ', PageNumber.TOTAL_PAGES], size: 18, color: '888888' })] })] }) } : undefined;
      const file = new Document({
        creator: 'JM Autida — Markdown to Word', title: $('#document h1')?.textContent || settings.name,
        styles: { default: { document: { run: { font: settings.font, size: half } } } },
        sections: [{ properties: { page: { size, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } }, ...(footers ? { footers } : {}), children: children.length ? children : [new Paragraph('')] }],
      });
      download(await Packer.toBlob(file), fileBase() + '.docx');
      status('Your Word document is downloading.', 'ok');
    } catch (err) { console.error(err); status('Word export failed. Try a smaller document, or download HTML or Markdown instead.', 'error'); }
    finally { $('#export').disabled = false; }
  });

  src.value = store.get('md:draft') || SAMPLE;
  render();
  status('Preview updates as you type. Drafts are saved only in this browser.');
})();
