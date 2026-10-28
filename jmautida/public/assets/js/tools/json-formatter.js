/* JSON formatter: validate with error location, repair, tree view, sort, convert to CSV/YAML/TypeScript. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, bytes, dropTarget, tabIndent, debounce, app } = window.JT;
  const SAMPLE = '{"id":1024,"name":"Rise Marketing","active":true,"tags":["seo","web design","ppc"],"owner":{"name":"Jane Doe","email":"jane@example.com"},"locations":[{"city":"Austin","state":"TX","clients":42},{"city":"Houston","state":"TX","clients":31,"opened":"2024-05-01"}],"rating":4.9,"notes":null}';

  app.innerHTML = `
    <div class="toolbar">
      <div class="toolbar-group">
        ${btn('format', 'Format', { icon: 'braces', primary: true })}${btn('minify', 'Minify', { ghost: true })}${btn('repair', 'Repair', { icon: 'wand', ghost: true, title: 'Fix comments, trailing commas, single quotes and unquoted keys' })}
        <select class="select select-sm" id="indent" aria-label="Indentation" style="width:auto"><option value="2">2 spaces</option><option value="4">4 spaces</option><option value="tab">Tabs</option></select>
        <label class="check-row"><input type="checkbox" id="sort"> Sort keys</label>
      </div>
      <div class="toolbar-group">${btn('sample', 'Sample', { ghost: true })}${btn('import', 'Open file', { icon: 'upload', ghost: true })}${btn('clear', 'Clear', { icon: 'trash', ghost: true, cls: 'btn-danger' })}<input type="file" id="file" accept=".json,application/json,text/plain" hidden></div>
    </div>
    <div class="panes">
      <div class="pane"><div class="pane-head"><span>Input</span><span id="in-meta"></span></div><textarea class="code" id="source" spellcheck="false" placeholder="Paste JSON here or drop a .json file…" aria-label="JSON input"></textarea></div>
      <div class="pane"><div class="pane-head" style="padding-left:6px">
        <div class="tabs sub" role="tablist" id="views" style="margin:0;border:0;background:transparent">
          <button type="button" class="tab" role="tab" aria-selected="true" data-view="text">Text</button><button type="button" class="tab" role="tab" aria-selected="false" data-view="tree">Tree</button><button type="button" class="tab" role="tab" aria-selected="false" data-view="convert">Convert</button>
        </div>
        <div class="toolbar-group"><select class="select select-sm" id="target" aria-label="Convert to" hidden style="width:auto;height:30px"><option value="csv">CSV</option><option value="yaml">YAML</option><option value="ts">TypeScript</option></select>
        <button type="button" class="btn btn-xs btn-ghost" id="expand" hidden>Expand all</button><button type="button" class="btn btn-xs btn-ghost" id="collapse" hidden>Collapse</button>
        <button type="button" class="btn btn-xs" id="copy">${icon('copy')}Copy</button><button type="button" class="btn btn-xs" id="save">${icon('download')}Save</button></div></div>
        <div id="error" class="json-error" hidden></div>
        <textarea class="code" id="output" spellcheck="false" readonly aria-label="Formatted output"></textarea>
        <div class="json-tree" id="tree" hidden></div>
        <div class="path-bar" id="path-bar" hidden><code id="path">$</code><button type="button" class="btn btn-xs btn-ghost" id="copy-path">Copy path</button></div>
      </div>
    </div>
    <div class="stat-grid" id="stats" style="margin-top:14px"></div>`;

  const src = $('#source'), out = $('#output');
  tabIndent(src);
  let view = 'text', parsed, mode = 'format', valid = false;

  const indent = () => ($('#indent').value === 'tab' ? '\t' : Number($('#indent').value));
  const sortDeep = v => Array.isArray(v) ? v.map(sortDeep) : v && typeof v === 'object' ? Object.keys(v).sort((a, b) => a.localeCompare(b)).reduce((o, k) => (o[k] = sortDeep(v[k]), o), {}) : v;

  function locate(err, text) {
    const msg = String(err.message || err);
    let line, col, m = msg.match(/line (\d+) column (\d+)/i);
    if (m) { line = +m[1]; col = +m[2]; }
    else if ((m = msg.match(/position (\d+)/i))) { const pos = +m[1], before = text.slice(0, pos); line = before.split('\n').length; col = pos - before.lastIndexOf('\n'); }
    else if (/Unexpected end/i.test(msg)) { const lines = text.split('\n'); line = lines.length; col = lines[lines.length - 1].length + 1; }
    return { msg: msg.replace(/^JSON\.parse: /, '').replace(/ in JSON at position \d+.*$/, ''), line, col };
  }
  function showError(e, text, select) {
    const { msg, line, col } = locate(e, text);
    let snippet = '';
    if (line) {
      const lines = text.split('\n'), from = Math.max(0, line - 3);
      snippet = lines.slice(from, line).map((l, i) => `${String(from + i + 1).padStart(4)} │ ${l}`).join('\n') + `\n${' '.repeat(7 + col - 1)}^`;
      if (line > 0 && select) { const pos = lines.slice(0, line - 1).reduce((s, l) => s + l.length + 1, 0) + col - 1; src.setSelectionRange(pos, pos + 1); }
    }
    $('#error').hidden = false;
    $('#error').innerHTML = `<strong>${icon('x')} Invalid JSON${line ? ` — line ${line}, column ${col}` : ''}</strong><p>${esc(msg)}</p>${snippet ? `<pre>${esc(snippet)}</pre>` : ''}<button type="button" class="btn btn-xs" id="try-repair">${icon('wand')}Try auto-repair</button>`;
    $('#try-repair').addEventListener('click', () => $('#repair').click());
    status(`Invalid JSON${line ? ` at line ${line}, column ${col}` : ''}: ${msg}`, 'error');
  }

  function stats(v, text) {
    let keys = 0, nodes = 0, depth = 0;
    const walk = (x, d) => { nodes++; depth = Math.max(depth, d); if (Array.isArray(x)) x.forEach(y => walk(y, d + 1)); else if (x && typeof x === 'object') for (const k in x) { keys++; walk(x[k], d + 1); } };
    walk(v, 0);
    const type = Array.isArray(v) ? `Array(${v.length})` : v === null ? 'null' : typeof v;
    $('#stats').innerHTML = `<div class="stat"><strong>${esc(type)}</strong><span>Root</span></div><div class="stat"><strong>${keys.toLocaleString()}</strong><span>Keys</span></div><div class="stat"><strong>${nodes.toLocaleString()}</strong><span>Values</span></div><div class="stat"><strong>${depth}</strong><span>Max depth</span></div><div class="stat"><strong>${bytes(new Blob([text]).size)}</strong><span>Input size</span></div>`;
  }

  function process(m = mode, typing = false) {
    mode = m;
    const text = src.value;
    $('#in-meta').textContent = text ? `${text.split('\n').length} lines` : '';
    $('#error').hidden = true;
    if (!text.trim()) { out.value = ''; $('#tree').innerHTML = ''; $('#stats').innerHTML = ''; valid = false; status('Paste JSON to get started.'); return; }
    try { parsed = JSON.parse(text); valid = true; }
    catch (e) { valid = false; out.value = ''; $('#tree').innerHTML = ''; showError(e, text, !typing); return; }
    if ($('#sort').checked) parsed = sortDeep(parsed);
    out.value = mode === 'minify' ? JSON.stringify(parsed) : JSON.stringify(parsed, null, indent());
    stats(parsed, text);
    if (view === 'tree') renderTree();
    if (view === 'convert') convert();
    store.set('json:last', text.length < 200000 ? text : '');
    status(`Valid JSON · ${mode === 'minify' ? 'minified' : 'formatted'}${$('#sort').checked ? ', keys sorted' : ''}.`, 'ok');
  }

  // ---------- Repair ----------
  function repair(s) {
    let o = '', i = 0; const n = s.length;
    while (i < n) {
      const c = s[i];
      if (c === '"') { let j = i + 1; while (j < n && s[j] !== '"') { if (s[j] === '\\') j++; j++; } o += s.slice(i, j + 1); i = j + 1; continue; }
      if (c === "'") { let j = i + 1, str = ''; while (j < n && s[j] !== "'") { if (s[j] === '\\' && s[j + 1] === "'") { str += "'"; j += 2; continue; } if (s[j] === '\\') { str += s[j] + (s[j + 1] ?? ''); j += 2; continue; } str += s[j] === '"' ? '\\"' : s[j]; j++; } o += `"${str}"`; i = j + 1; continue; }
      if (c === '/' && s[i + 1] === '/') { while (i < n && s[i] !== '\n') i++; continue; }
      if (c === '/' && s[i + 1] === '*') { const e = s.indexOf('*/', i + 2); i = e < 0 ? n : e + 2; continue; }
      if (c === ',') { let j = i + 1; while (j < n && /\s/.test(s[j])) j++; if (s[j] === '}' || s[j] === ']') { i++; continue; } }
      if (/[A-Za-z_$]/.test(c)) {
        let j = i; while (j < n && /[\w$-]/.test(s[j])) j++;
        const word = s.slice(i, j); let k = j; while (k < n && /\s/.test(s[k])) k++;
        if (s[k] === ':' && !['true', 'false', 'null'].includes(word)) o += `"${word}"`;
        else o += ({ True: 'true', False: 'false', None: 'null', undefined: 'null', NaN: 'null', Infinity: 'null' })[word] ?? word;
        i = j; continue;
      }
      o += c; i++;
    }
    return o.replace(/^﻿/, '');
  }

  // ---------- Tree ----------
  const pathPart = (k, isIndex) => isIndex ? `[${k}]` : /^[A-Za-z_$][\w$]*$/.test(k) ? `.${k}` : `[${JSON.stringify(k)}]`;
  let nodeCount = 0;
  function node(key, value, path, depth, isIndex) {
    if (++nodeCount > 5000) return '';
    const label = key === null ? '' : `<span class="jk" data-path="${esc(path)}">${isIndex ? key : esc(JSON.stringify(key))}</span><span class="jp">: </span>`;
    if (value && typeof value === 'object') {
      const arr = Array.isArray(value), entries = arr ? value.map((v, i) => [i, v]) : Object.entries(value);
      const summary = arr ? `Array(${value.length})` : `{${entries.length} key${entries.length === 1 ? '' : 's'}}`;
      if (!entries.length) return `<div class="jl">${label}<span class="jn">${arr ? '[]' : '{}'}</span></div>`;
      return `<details${depth < 2 ? ' open' : ''}><summary>${label}<span class="jt">${summary}</span></summary><div class="jc">${entries.map(([k, v]) => node(k, v, path + pathPart(k, arr), depth + 1, arr)).join('')}</div></details>`;
    }
    const t = value === null ? 'null' : typeof value;
    return `<div class="jl">${label}<span class="jv ${t}" data-path="${esc(path)}">${esc(t === 'string' ? JSON.stringify(value) : String(value))}</span></div>`;
  }
  function renderTree() {
    if (!valid) return;
    nodeCount = 0;
    $('#tree').innerHTML = node(null, parsed, '$', 0, false) + (nodeCount > 5000 ? '<p class="muted">Showing the first 5,000 values.</p>' : '');
  }
  $('#tree').addEventListener('click', e => {
    const el = e.target.closest('[data-path]'); if (!el) return;
    $('#path').textContent = el.dataset.path; $('#path-bar').hidden = false;
  });
  $('#copy-path').addEventListener('click', () => copy($('#path').textContent, 'Path copied'));
  $('#expand').addEventListener('click', () => $$('#tree details').forEach(d => { d.open = true; }));
  $('#collapse').addEventListener('click', () => $$('#tree details').forEach((d, i) => { d.open = i === 0; }));

  // ---------- Converters ----------
  const isObj = v => v && typeof v === 'object' && !Array.isArray(v);
  function flatten(obj, prefix = '', outObj = {}) {
    for (const [k, v] of Object.entries(obj)) {
      const key = prefix ? `${prefix}.${k}` : k;
      if (isObj(v) && Object.keys(v).length) flatten(v, key, outObj);
      else if (Array.isArray(v)) outObj[key] = v.every(x => x === null || typeof x !== 'object') ? v.join('; ') : JSON.stringify(v);
      else outObj[key] = v;
    }
    return outObj;
  }
  function toCSV(v) {
    const rows = (Array.isArray(v) ? v : [v]).map(r => (isObj(r) ? flatten(r) : { value: r }));
    const headers = []; rows.forEach(r => Object.keys(r).forEach(k => { if (!headers.includes(k)) headers.push(k); }));
    const cell = x => { if (x === null || x === undefined) return ''; const s = typeof x === 'object' ? JSON.stringify(x) : String(x); return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
    return [headers.map(cell).join(','), ...rows.map(r => headers.map(h => cell(r[h])).join(','))].join('\n');
  }
  function yamlScalar(v) {
    if (v === null) return 'null';
    if (typeof v !== 'string') return String(v);
    if (v === '' || /^(true|false|null|yes|no|on|off|~)$/i.test(v) || /^[-+]?(\d|\.\d)/.test(v) || /[:#\[\]{},&*!|>'"%@`]|^\s|\s$|^-/.test(v) || v.includes('\n')) return JSON.stringify(v);
    return v;
  }
  function toYAML(v, ind = 0) {
    const sp = '  '.repeat(ind);
    if (Array.isArray(v)) {
      if (!v.length) return '[]';
      return v.map(x => {
        if (isObj(x) && Object.keys(x).length) { const inner = toYAML(x, ind + 1).replace(/^\s+/, ''); return `${sp}- ${inner}`; }
        if (Array.isArray(x) && x.length) return `${sp}-\n${toYAML(x, ind + 1)}`;
        return `${sp}- ${Array.isArray(x) ? '[]' : isObj(x) ? '{}' : yamlScalar(x)}`;
      }).join('\n');
    }
    if (isObj(v)) {
      const keys = Object.keys(v); if (!keys.length) return '{}';
      return keys.map(k => {
        const key = /^[\w.-]+$/.test(k) && !/^\d/.test(k) ? k : JSON.stringify(k), x = v[k];
        if ((isObj(x) && Object.keys(x).length) || (Array.isArray(x) && x.length)) return `${sp}${key}:\n${toYAML(x, ind + 1)}`;
        return `${sp}${key}: ${Array.isArray(x) ? '[]' : isObj(x) ? '{}' : yamlScalar(x)}`;
      }).join('\n');
    }
    return sp + yamlScalar(v);
  }
  function toTS(value) {
    const interfaces = new Map(), names = new Set();
    const pascal = k => { const s = String(k).replace(/[^A-Za-z0-9]+(.)?/g, (_, c) => (c ? c.toUpperCase() : '')).replace(/^./, c => c.toUpperCase()); return /^[A-Za-z_]/.test(s) ? s : 'T' + s; };
    const singular = n => String(n).replace(/ies$/i, 'y').replace(/(?<!s)s$/i, '') || 'Item';
    const uniq = n => { let x = n, i = 2; while (names.has(x)) x = n + i++; names.add(x); return x; };
    function typesOf(values, name) {
      const set = new Set(), objs = values.filter(isObj), arrs = values.filter(Array.isArray);
      if (objs.length) set.add(objectType(objs, name));
      if (arrs.length) { const items = [].concat(...arrs); set.add(items.length ? (t => (t.includes('|') ? `(${t})[]` : `${t}[]`))(typesOf(items, singular(name))) : 'unknown[]'); }
      values.filter(v => !isObj(v) && !Array.isArray(v)).forEach(v => set.add(v === null ? 'null' : typeof v));
      return [...set].join(' | ') || 'unknown';
    }
    function objectType(objs, name) {
      const iname = uniq(pascal(name)), keys = [];
      objs.forEach(o => Object.keys(o).forEach(k => { if (!keys.includes(k)) keys.push(k); }));
      const lines = keys.map(k => {
        const present = objs.filter(o => k in o);
        const key = /^[A-Za-z_$][\w$]*$/.test(k) ? k : JSON.stringify(k);
        return `  ${key}${present.length < objs.length ? '?' : ''}: ${typesOf(present.map(o => o[k]), k)};`;
      });
      interfaces.set(iname, `export interface ${iname} {\n${lines.join('\n')}\n}`);
      return iname;
    }
    const root = typesOf([value], 'Root');
    const body = [...interfaces.values()].reverse().join('\n\n');
    return (interfaces.has(root) ? '' : `export type Root = ${root};\n\n`) + body;
  }
  function convert() {
    if (!valid) return;
    const t = $('#target').value;
    try { out.value = t === 'csv' ? toCSV(parsed) : t === 'yaml' ? toYAML(parsed) : toTS(parsed); status(`Converted to ${t === 'ts' ? 'TypeScript' : t.toUpperCase()}.`, 'ok'); }
    catch (e) { out.value = ''; status('Conversion failed: ' + e.message, 'error'); }
  }

  // ---------- Views & actions ----------
  $$('#views .tab').forEach(b => b.addEventListener('click', () => {
    view = b.dataset.view;
    $$('#views .tab').forEach(x => x.setAttribute('aria-selected', String(x === b)));
    out.hidden = view === 'tree'; $('#tree').hidden = view !== 'tree'; $('#path-bar').hidden = view !== 'tree' || $('#path').textContent === '$';
    $('#target').hidden = view !== 'convert'; $('#expand').hidden = $('#collapse').hidden = view !== 'tree';
    if (view === 'tree') renderTree(); else if (view === 'convert') convert(); else process();
  }));
  $('#target').addEventListener('change', convert);
  $('#format').addEventListener('click', () => { if (view === 'convert') $('#views .tab').click(); process('format'); });
  $('#minify').addEventListener('click', () => { if (view !== 'text') $('#views .tab').click(); process('minify'); });
  $('#indent').addEventListener('change', () => process());
  $('#sort').addEventListener('change', () => process());
  $('#repair').addEventListener('click', () => {
    const fixed = repair(src.value);
    try { JSON.parse(fixed); src.value = JSON.stringify(JSON.parse(fixed), null, indent()); process('format'); toast('Repaired and formatted'); }
    catch (e) { src.value = fixed; process(); toast('Partly repaired — check the remaining error', 'error'); }
  });
  $('#sample').addEventListener('click', () => { src.value = SAMPLE; process('format'); });
  $('#clear').addEventListener('click', () => { src.value = ''; process(); src.focus(); store.del('json:last'); });
  $('#copy').addEventListener('click', () => { const text = view === 'tree' ? out.value || JSON.stringify(parsed, null, indent()) : out.value; if (text) copy(text); });
  $('#save').addEventListener('click', () => {
    if (!valid) return toast('Fix the JSON first', 'error');
    const t = view === 'convert' ? $('#target').value : 'json';
    const ext = { json: 'json', csv: 'csv', yaml: 'yaml', ts: 'ts' }[t], type = { json: 'application/json', csv: 'text/csv', yaml: 'text/yaml', ts: 'text/plain' }[t];
    download(view === 'tree' ? JSON.stringify(parsed, null, indent()) : out.value, `data.${ext}`, type + ';charset=utf-8');
  });
  const readFile = async f => { if (!f) return; if (f.size > 20 * 1024 * 1024) return toast('Files up to 20 MB, please', 'error'); src.value = await f.text(); process('format'); };
  $('#import').addEventListener('click', () => $('#file').click());
  $('#file').addEventListener('change', () => { readFile($('#file').files[0]); $('#file').value = ''; });
  dropTarget(src.parentElement, files => readFile(files[0]));
  src.addEventListener('input', debounce(() => process(mode, true), 300));
  src.addEventListener('paste', () => setTimeout(() => process('format', true), 0));

  src.value = store.get('json:last') || SAMPLE;
  process('format');
})();
