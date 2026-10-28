/* Helpers shared by every tool page. */
(function () {
  'use strict';
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const icon = name => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${(window.JM_ICONS || {})[name] || ''}</svg>`;

  let toastBox;
  function toast(message, type = 'ok') {
    if (!toastBox) { toastBox = document.createElement('div'); toastBox.className = 'toasts'; toastBox.setAttribute('aria-live', 'polite'); document.body.append(toastBox); }
    const t = document.createElement('div');
    t.className = `toast ${type === 'error' ? 'error' : ''}`; t.textContent = message;
    toastBox.append(t);
    setTimeout(() => { t.classList.add('out'); setTimeout(() => t.remove(), 260); }, 2600);
  }
  function status(message, type = '') {
    const el = $('#status'); if (!el) return;
    el.textContent = message || ''; el.className = `status-line ${type}`;
  }
  function download(data, name, type = 'text/plain;charset=utf-8') {
    const blob = data instanceof Blob ? data : new Blob([data], { type });
    const url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = name; document.body.append(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 15000);
  }
  async function copy(text, label = 'Copied to clipboard') {
    try { await navigator.clipboard.writeText(text); toast(label); return true; }
    catch {
      const ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.append(ta); ta.select();
      const ok = document.execCommand('copy'); ta.remove();
      toast(ok ? label : 'Copy failed — select the text and press Ctrl/⌘ + C', ok ? 'ok' : 'error'); return ok;
    }
  }
  const debounce = (fn, ms = 200) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };
  const store = {
    get(key, fallback = null) { try { const v = localStorage.getItem('jm:' + key); return v === null ? fallback : JSON.parse(v); } catch { return fallback; } },
    set(key, value) { try { localStorage.setItem('jm:' + key, JSON.stringify(value)); } catch { /* storage full or blocked */ } },
    del(key) { try { localStorage.removeItem('jm:' + key); } catch { /* ignore */ } },
  };
  const bytes = n => {
    if (!Number.isFinite(n)) return '—';
    const u = ['B', 'KB', 'MB', 'GB']; let i = 0;
    while (n >= 1024 && i < u.length - 1) { n /= 1024; i++; }
    return `${n >= 100 || i === 0 ? Math.round(n) : n.toFixed(1)} ${u[i]}`;
  };
  const btn = (id, label, opts = {}) => `<button type="button" class="btn ${opts.primary ? 'btn-primary' : opts.ghost ? 'btn-ghost' : ''} ${opts.size || 'btn-sm'} ${opts.cls || ''}" id="${id}"${opts.title ? ` title="${esc(opts.title)}"` : ''}${opts.attrs ? ' ' + opts.attrs : ''}>${opts.icon ? icon(opts.icon) : ''}${label}</button>`;

  // Accessible tabs: <div class="tabs" role="tablist"> buttons[data-tab] + panels[data-panel]
  function tabs(container, onChange) {
    const buttons = $$('[role="tab"]', container);
    const select = (name, focus) => {
      buttons.forEach(b => {
        const on = b.dataset.tab === name;
        b.setAttribute('aria-selected', String(on)); b.tabIndex = on ? 0 : -1;
        const panel = document.getElementById(b.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
        if (on && focus) b.focus();
      });
      onChange?.(name);
    };
    buttons.forEach((b, i) => {
      b.addEventListener('click', () => select(b.dataset.tab));
      b.addEventListener('keydown', e => {
        const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (d) { e.preventDefault(); select(buttons[(i + d + buttons.length) % buttons.length].dataset.tab, true); }
      });
    });
    return { select };
  }
  const tabBar = (id, items, cls = '') => `<div class="tabs ${cls}" role="tablist" id="${id}">${items.map(([k, label, ic], i) => `<button type="button" class="tab" role="tab" id="${id}-${k}" data-tab="${k}" aria-controls="${id}-panel-${k}" aria-selected="${i === 0}" tabindex="${i === 0 ? 0 : -1}">${ic ? icon(ic) : ''}${label}</button>`).join('')}</div>`;
  const tabPanel = (id, key, content, first) => `<div role="tabpanel" id="${id}-panel-${key}" aria-labelledby="${id}-${key}"${first ? '' : ' hidden'}>${content}</div>`;

  // Drag-and-drop files onto an element.
  function dropTarget(el, onFiles) {
    let depth = 0;
    el.addEventListener('dragenter', e => { e.preventDefault(); depth++; el.classList.add('over'); });
    el.addEventListener('dragover', e => { e.preventDefault(); });
    el.addEventListener('dragleave', () => { if (--depth <= 0) { depth = 0; el.classList.remove('over'); } });
    el.addEventListener('drop', e => { e.preventDefault(); depth = 0; el.classList.remove('over'); if (e.dataTransfer?.files?.length) onFiles([...e.dataTransfer.files]); });
  }
  // Tab key inserts two spaces in code editors.
  function tabIndent(textarea, unit = '  ') {
    textarea.addEventListener('keydown', e => {
      if (e.key !== 'Tab' || e.ctrlKey || e.metaKey || e.altKey) return;
      e.preventDefault();
      const { selectionStart: s, selectionEnd: en, value } = textarea;
      if (s === en && !e.shiftKey) { textarea.setRangeText(unit, s, en, 'end'); }
      else {
        const lineStart = value.lastIndexOf('\n', s - 1) + 1;
        const block = value.slice(lineStart, en);
        const out = e.shiftKey ? block.replace(new RegExp(`^${unit}`, 'gm'), '') : block.replace(/^/gm, unit);
        textarea.setRangeText(out, lineStart, en, 'select');
      }
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
    });
  }

  window.JT = { $, $$, esc, icon, toast, status, download, copy, debounce, store, bytes, btn, tabs, tabBar, tabPanel, dropTarget, tabIndent, app: $('#tool-app') };
})();
