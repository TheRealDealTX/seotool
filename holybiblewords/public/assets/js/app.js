/* Holy Bible Words — progressive web app layer.
 * The server renders every page; this script adds app-like navigation (no full
 * reloads), seamless version switching, the book/chapter/verse picker, verse
 * actions (highlight, bookmark, note, copy, share, image), parallel view,
 * listen, reading plan, saved items, settings and offline support. */
(() => {
  'use strict';

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const icon = n => `<svg class="ic" aria-hidden="true"><use href="#i-${n}"/></svg>`;
  let VERS = null;   // versions.json once loaded
  // KJV [brackets] mark translator-supplied words (italics); other versions use brackets literally
  const verseHtml = (t, ver = 'ta') => (VERS?.[ver]?.italics === false ? esc(t) : esc(t).replace(/\[([^\]]*)\]/g, '<i>$1</i>'));
  const plain = t => String(t || '').replace(/\s+/g, ' ').trim();
  const native = () => window.Capacitor?.isNativePlatform?.() || document.body.classList.contains('native-app');

  // ---------- storage ----------
  const store = {
    get(k, d) { try { const v = localStorage.getItem('hbw.' + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('hbw.' + k, JSON.stringify(v)); } catch (e) { /* private mode */ } },
  };
  const settings = Object.assign({ theme: 'auto', font: 'serif', size: 19, lh: 1.75, layout: 'verses', nums: true, parallel: false, pver: 'auto' }, store.get('settings', {}));
  const saveSettings = () => { store.set('settings', settings); applySettings(); };
  const darkMQ = matchMedia('(prefers-color-scheme: dark)');
  const isDark = () => settings.theme === 'dark' || (settings.theme === 'auto' && darkMQ.matches);
  function applySettings() {
    const d = document.documentElement;
    d.dataset.theme = settings.theme; d.dataset.font = settings.font; d.dataset.layout = settings.layout;
    // browser / phone status-bar colour follows the chosen theme, not just the system one
    document.querySelectorAll('meta[name=theme-color]').forEach(m => {
      m.dataset.orig ??= m.content;
      m.content = settings.theme === 'auto' ? m.dataset.orig : isDark() ? '#11161c' : settings.theme === 'sepia' ? '#f3ead8' : '#1b5e8f';
    });
    document.querySelectorAll('[data-action=theme]').forEach(b => {
      b.setAttribute('aria-pressed', String(isDark()));
      b.setAttribute('aria-label', isDark() ? 'Light mode' : 'Dark mode');
      b.title = isDark() ? 'Light mode' : 'Dark mode';
    });
    d.dataset.nums = settings.nums ? 'on' : 'off';
    d.style.setProperty('--reader-size', settings.size + 'px'); d.style.setProperty('--reader-lh', settings.lh);
  }
  const marks = {
    hl: store.get('hl', {}), bm: store.get('bm', {}), notes: store.get('notes', {}),
    save() { store.set('hl', this.hl); store.set('bm', this.bm); store.set('notes', this.notes); },
  };
  const prefVer = () => store.get('ver', 'ta');

  // ---------- data ----------
  let booksP, versP;
  const getBooks = () => booksP ??= fetch('/data/books.json').then(r => r.json()).then(list => {
    const by = {}; list.forEach((b, i) => { b.i = i; by[b.slug] = b; }); return { list, by };
  });
  const getVers = () => versP ??= fetch('/data/versions.json').then(r => r.json()).then(v => (VERS = v));
  const chapterCache = new Map();
  function getChapter(ver, book, ch) {
    const k = `${ver}/${book}/${ch}`;
    if (!chapterCache.has(k)) {
      chapterCache.set(k, fetch(`/api/chapter/${k}`).then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
        .catch(e => { chapterCache.delete(k); throw e; }));
    }
    return chapterCache.get(k);
  }
  // version shown side by side / compared with `v`
  const DEFAULT_PAIR = { ta: 'ceb', ml: 'ta', ceb: 'ta' };
  const pairVer = v => (settings.pver && settings.pver !== 'auto' && settings.pver !== v ? settings.pver : DEFAULT_PAIR[v] || 'ta');
  // rows of a chapter (from the API) that overlap verses n..to
  const rowsFor = (d, n, to = n) => d.rows.filter(r => r[1] >= n && r[0] <= to);
  const rangeLabel = r => (r[0] === r[1] ? `${r[0]}` : `${r[0]}–${r[1]}`);
  const bookName = (b, vers, ver) => b.names[vers[ver].nameKey];
  const urlFor = (ver, book, ch, v) => `/${ver}/` + (book ? `${book}/` : '') + (ch ? `${ch}/` : '') + (v ? `${v}/` : '');
  const keyOf = (book, ch, v) => `${book}.${ch}.${v}`;
  const parseKey = k => { const [book, ch, v] = k.split('.'); return { book, ch: +ch, v: +v }; };

  // ---------- ui helpers ----------
  let toastT;
  function toast(msg) {
    const t = $('#toast'); t.textContent = msg; t.classList.add('show');
    clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('show'), 2200);
  }
  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); }
    catch (e) {
      const ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove();
    }
    toast('Copied');
  }
  async function shareIt({ title, text, url, files }) {
    const cap = window.Capacitor?.Plugins?.Share;
    try {
      if (cap && !files) { await cap.share({ title, text, url, dialogTitle: 'Share' }); return; }
      if (files && navigator.canShare?.({ files })) { await navigator.share({ files, title, text }); return; }
      if (navigator.share && !files) { await navigator.share({ title, text, url }); return; }
    } catch (e) { if (e?.name === 'AbortError') return; }
    copyText([text, url].filter(Boolean).join('\n'));
  }

  // sheets (bottom sheet on phones, dialog on desktop)
  let sheetClose = null;
  function openSheet(title, bodyHtml, onClose) {
    closeSheet(true);
    const root = $('#sheet-root');
    root.innerHTML = `<div class="sheet-backdrop"></div><div class="sheet" role="dialog" aria-modal="true" aria-label="${esc(title)}">
      <div class="sheet-head"><h2>${esc(title)}</h2><button class="icon-btn" type="button" data-close aria-label="Close">${icon('x')}</button></div>
      <div class="sheet-body">${bodyHtml}</div></div>`;
    const sheet = $('.sheet', root), bd = $('.sheet-backdrop', root);
    requestAnimationFrame(() => { sheet.classList.add('open'); bd.classList.add('open'); });
    bd.addEventListener('click', () => closeSheet());
    $('[data-close]', root).addEventListener('click', () => closeSheet());
    sheetClose = onClose || null;
    return $('.sheet-body', root);
  }
  function closeSheet(instant) {
    const root = $('#sheet-root');
    if (!root.firstChild) return;
    const fn = sheetClose; sheetClose = null;
    if (instant) { root.innerHTML = ''; } else {
      $$('.sheet, .sheet-backdrop', root).forEach(n => n.classList.remove('open'));
      setTimeout(() => { if (!sheetClose) root.innerHTML = ''; }, 220);
    }
    fn && fn();
  }
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeSheet(); });

  // ---------- navigation (server-rendered pages swapped in place) ----------
  const progress = $('#progress');
  let navToken = 0;
  function isAppLink(a) {
    if (!a || a.target || a.hasAttribute('download') || a.origin !== location.origin) return false;
    const p = a.pathname;
    if (/^\/(api|data|assets|wp-content)\//.test(p) || /\.[a-z0-9]+$/i.test(p)) return false;
    return true;
  }
  async function navigate(url, opts = {}) {
    const u = new URL(url, location.href);
    if (opts.push !== false && u.pathname === location.pathname && u.search === location.search && u.hash) {
      history.pushState(history.state, '', u.href); scrollToHash(u.hash); return;
    }
    const token = ++navToken;
    stopListening();
    if (opts.push !== false) history.replaceState({ ...(history.state || {}), y: scrollY }, '');
    progress.className = 'on';
    $('#main').classList.add('leaving');
    try {
      const res = await fetch(u.href, { headers: { 'X-Requested-With': 'hbw' } });
      const html = await res.text();
      if (token !== navToken) return;
      const doc = new DOMParser().parseFromString(html, 'text/html');
      const main = doc.getElementById('main');
      if (!main) throw new Error('no main');
      // only adopt the response URL for real redirects: offline, the service worker
      // answers with the cached /offline/ shell and we must stay on the requested page
      const finalUrl = new URL(res.redirected && res.url ? res.url : u.href);
      finalUrl.hash = u.hash;
      $('#main').replaceWith(main);
      document.title = doc.title;
      document.documentElement.lang = doc.documentElement.lang;
      applySettings();
      const sw = $('.ver-switch', doc), cur = $('.topbar .ver-switch');
      if (sw && cur) cur.replaceWith(sw);
      const canon = $('link[rel=canonical]', doc);
      if (canon) $('link[rel=canonical]').href = canon.href;
      if (opts.push !== false) history.pushState({ y: 0 }, '', finalUrl.href);
      else if (finalUrl.href !== location.href) history.replaceState(history.state, '', finalUrl.href);
      initPage();
      if (opts.anchor) restoreAnchor(opts.anchor);
      else if (finalUrl.hash) scrollToHash(finalUrl.hash);
      else window.scrollTo(0, opts.y || 0);
      window.gtag?.('event', 'page_view', { page_location: finalUrl.href, page_title: doc.title });
    } catch (e) {
      location.href = u.href;
    } finally {
      if (token === navToken) { progress.className = 'done'; setTimeout(() => { if (progress.className === 'done') progress.className = ''; }, 400); }
    }
  }
  function scrollToHash(hash) {
    const el = document.getElementById(decodeURIComponent(hash.slice(1)));
    if (!el) return;
    el.scrollIntoView({ block: 'start' });
    const v = el.closest('.v');
    if (v) { v.classList.add('flash'); setTimeout(() => v.classList.remove('flash'), 1800); }
  }
  document.addEventListener('click', e => {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const a = e.target.closest('a[href]');
    if (!a || !isAppLink(a)) return;
    // version switcher: keep the reader's exact place
    if (a.closest('.ver-switch')) {
      e.preventDefault();
      switchVersion(a.dataset.ver, a.getAttribute('href'));
      return;
    }
    // verse numbers inside the reader open the verse sheet instead of navigating
    if (a.classList.contains('vn') && a.closest('.chapter')) return;
    e.preventDefault();
    closeSheet(true);
    navigate(a.href);
  });
  window.addEventListener('popstate', e => navigate(location.href, { push: false, y: e.state?.y || 0 }));
  document.addEventListener('submit', e => {
    const f = e.target;
    if (!f.matches('form.jump')) return;
    e.preventDefault();
    const q = f.q.value.trim();
    if (!q) return;
    const v = f.v?.value || prefVer();
    navigate('/search/?' + new URLSearchParams({ q, v }));
  });

  // ---------- version switching ----------
  function captureAnchor() {
    const vs = $$('.chapter .v');
    if (!vs.length) return null;
    const top = ($('.reader-bar')?.getBoundingClientRect().bottom || 0) + 4;
    const v = vs.find(el => el.getBoundingClientRect().bottom > top) || vs[0];
    return { v: v.dataset.v, offset: v.getBoundingClientRect().top };
  }
  function restoreAnchor(a) {
    const el = document.getElementById('v' + a.v);
    if (el) window.scrollTo(0, scrollY + el.getBoundingClientRect().top - a.offset);
  }
  function switchVersion(ver, href) {
    store.set('ver', ver);
    const page = $('#main').dataset.page;
    if (page === 'home') { applyHomeVersion(ver); return; }
    // pages that aren't tied to a version just re-render with the new preference
    if (!$('#main').dataset.switch) { markVersion(ver); initPage(); return; }
    const anchor = page === 'chapter' ? captureAnchor() : null;
    navigate(href, { anchor });
  }

  // ---------- page init ----------
  function initPage() {
    const main = $('#main');
    const page = main.dataset.page;
    const navKey = { home: 'home', search: 'search', votd: 'votd', plan: 'plan', saved: 'saved', chapter: 'read', verse: 'read', book: 'read', version: 'read' }[page];
    $$('[data-nav]').forEach(a => a.classList.toggle('on', a.dataset.nav === navKey));
    if (!main.dataset.switch) markVersion(prefVer());
    else if (main.dataset.ver) store.set('ver', main.dataset.ver);
    updateReadLinks();
    ({ home: initHome, chapter: initChapter, verse: initVerse, votd: initVotd, plan: initPlan, saved: initSaved, app: initApp, offline: initOffline }[page] || (() => {}))(main);
  }
  function updateReadLinks() {
    const last = store.get('last', null);
    const href = last ? urlFor(prefVer(), last.book, last.ch) + (last.v > 1 ? '#v' + last.v : '') : urlFor(prefVer(), 'genesis', 1);
    $$('.js-read-link').forEach(a => { a.href = href; });
  }

  // ---------- home ----------
  function initHome(main) {
    const ver = prefVer();
    if (ver !== 'ta') applyHomeVersion(ver);
    const last = store.get('last', null);
    const box = $('[data-continue]', main);
    if (last && box) {
      getBooks().then(async ({ by }) => {
        const vers = await getVers(); const b = by[last.book]; if (!b) return;
        const link = $('.continue-link', box);
        link.href = urlFor(prefVer(), last.book, last.ch) + (last.v > 1 ? '#v' + last.v : '');
        link.textContent = `${bookName(b, vers, prefVer())} ${last.ch}` + (last.v > 1 ? `:${last.v}` : '');
        box.hidden = false;
      });
    }
    initVotd(main);
  }
  function markVersion(ver) {
    $$('.topbar .ver-switch a').forEach(a => { const on = a.dataset.ver === ver; a.classList.toggle('on', on); on ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current'); });
  }
  function applyHomeVersion(ver) {
    markVersion(ver);
    $$('#main .book-grid a, #main .chip[data-keep-ver], #main .continue-link').forEach(a => {
      a.setAttribute('href', a.getAttribute('href').replace(/^\/[a-z]+\//, `/${ver}/`));
    });
    const f = $('#main form.jump input[name=v]'); if (f) f.value = ver;
    getBooks().then(async ({ by }) => {
      const vers = await getVers();
      $$('#main .book-grid a').forEach(a => {
        const b = by[a.dataset.book]; if (!b) return;
        a.firstChild.textContent = bookName(b, vers, ver);
        a.classList.toggle('na', b.available[ver] === 0);
      });
      $$('#main .chip[data-keep-ver]').forEach(a => {
        const m = a.getAttribute('href').match(/^\/\w+\/(\w+)\/(\d+)\//); const b = m && by[m[1]];
        if (b) a.textContent = `${bookName(b, vers, ver)} ${m[2]}`;
      });
    });
    const card = $('[data-votd]');
    if (card) refreshVotd(card, ver, card.dataset.date === localDate() ? card.dataset.date : localDate(), true);
    updateReadLinks();
  }

  // ---------- verse of the day ----------
  function localDate(d = new Date()) {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  }
  function initVotd(main) {
    const card = $('[data-votd]', main);
    if (!card) return;
    const want = localDate();
    const ver = main.dataset.page === 'home' ? prefVer() : card.dataset.ver;
    if (card.dataset.date !== want || card.dataset.ver !== ver) refreshVotd(card, ver, want);
    // roll over at local midnight if the page stays open
    const now = new Date(), next = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 5);
    clearTimeout(initVotd.t);
    initVotd.t = setTimeout(() => { const c = $('[data-votd]'); if (c) refreshVotd(c, c.dataset.ver, localDate()); }, next - now);
  }
  async function refreshVotd(card, ver, date) {
    try {
      const [d, vers] = await Promise.all([fetch('/api/votd?date=' + date).then(r => r.json()), getVers()]);
      const shown = d.src[ver];
      card.dataset.date = date; card.dataset.ver = ver; card.dataset.ref = keyOf(d.book, d.ch, d.v);
      const dt = new Date(date + 'T12:00:00');
      $('time', card).textContent = dt.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
      $('time', card).setAttribute('datetime', date);
      const q = $('.votd-text', card); q.innerHTML = verseHtml(d.text[ver], shown); q.lang = vers[shown].lang;
      $('.votd-ref', card).innerHTML = `<a href="${urlFor(ver, d.book, d.ch, d.v)}">${esc(d.ref[ver])} <span class="badge">${esc(vers[shown].short)}</span></a>`;
      let note = $('.note', card);
      if (shown !== ver) {
        if (!note) { note = document.createElement('p'); note.className = 'note'; $('.votd-ref', card).after(note); }
        note.textContent = `Not yet available in ${vers[ver].label} — showing ${vers[shown].label}.`;
      } else note?.remove();
      $('.votd-actions a', card).href = urlFor(ver, d.book, d.ch) + '#v' + d.v;
    } catch (e) { /* keep server-rendered verse */ }
  }
  function votdPayload() {
    const card = $('[data-votd]');
    const { book, ch, v } = parseKey(card.dataset.ref);
    const short = $('.votd-ref .badge', card).textContent;
    const ref = plain(Array.from($('.votd-ref a', card).childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join(''));
    return { text: plain($('.votd-text', card).textContent), ref, short, url: location.origin + urlFor(card.dataset.ver, book, ch, v) };
  }

  // ---------- chapter reader ----------
  let readSaveT;
  function initChapter(main) {
    const art = $('.chapter', main);
    if (!art) return;
    const { ver, book } = art.dataset; const ch = +art.dataset.ch;
    paintMarks(art);
    art.addEventListener('click', e => {
      const v = e.target.closest('.v');
      if (!v || e.target.closest('.par')) return;
      e.preventDefault();
      $$('.v.sel', art).forEach(x => x.classList.remove('sel'));
      v.classList.add('sel');
      verseSheet(ver, book, ch, +v.dataset.v, () => v.classList.remove('sel'));
    });
    if (settings.parallel) setParallel(true);
    $('[data-action=parallel]', main)?.setAttribute('aria-pressed', String(!!settings.parallel));
    const remember = () => {
      const a = captureAnchor();
      const last = { ver, book, ch, v: a ? +a.v : 1, ts: Date.now() };
      store.set('last', last);
      pushHistory(last);
      updateReadLinks();
    };
    remember();
    window.removeEventListener('scroll', initChapter.onScroll);
    initChapter.onScroll = () => { clearTimeout(readSaveT); readSaveT = setTimeout(() => { if ($('.chapter')) remember(); }, 600); };
    window.addEventListener('scroll', initChapter.onScroll, { passive: true });
    planButton(main, book, ch);
  }
  function pushHistory(item) {
    let h = store.get('history', []);
    h = h.filter(x => !(x.book === item.book && x.ch === item.ch));
    h.unshift({ ver: item.ver, book: item.book, ch: item.ch, v: item.v || 1, ts: item.ts || Date.now() });
    store.set('history', h.slice(0, 60));
  }
  function paintMarks(root) {
    $$('.v', root).forEach(el => {
      const art = el.closest('[data-book]');
      const k = keyOf(art.dataset.book, art.dataset.ch, el.dataset.v);
      if (marks.hl[k]) el.dataset.hl = marks.hl[k]; else delete el.dataset.hl;
      el.classList.toggle('bm', !!marks.bm[k]);
      el.classList.toggle('has-note', !!marks.notes[k]);
    });
  }
  async function setParallel(on) {
    const art = $('.chapter');
    if (!art) return;
    $$('.par', art).forEach(n => n.remove());
    art.classList.toggle('parallel', on);
    art.closest('.reader-wrap')?.classList.toggle('wide', on);
    $('[data-action=parallel]')?.setAttribute('aria-pressed', String(on));
    if (!on) return;
    const { ver, book } = art.dataset; const o = pairVer(ver);
    try {
      const [d, vers] = await Promise.all([getChapter(o, book, art.dataset.ch), getVers()]);
      if (!art.isConnected || !art.classList.contains('parallel')) return;
      const used = new Set();
      $$('.v', art).forEach(el => {
        const n = +el.dataset.v, to = +(el.dataset.to || n);
        const rows = rowsFor(d, n, to).filter(r => !used.has(r[0]));
        rows.forEach(r => used.add(r[0]));
        const span = document.createElement('span');
        span.className = 'par'; span.lang = vers[o].lang;
        span.innerHTML = `<b>${esc(vers[o].short)}</b>` + (rows.length
          ? rows.map(r => (rows.length > 1 || r[0] !== n || r[1] !== to ? `<sup>${rangeLabel(r)}</sup> ` : '') + verseHtml(r[3], r[2]) + (r[2] !== o ? ` <span class="fb-tag">${esc(vers[r[2]].short)}</span>` : '')).join(' ')
          : '<em>See the verse above</em>');
        el.after(span);
      });
    } catch (e) { toast('Couldn’t load the other version'); }
  }

  // verse actions sheet
  async function verseSheet(ver, book, ch, v, onClose) {
    const [{ by }, vers] = await Promise.all([getBooks(), getVers()]);
    const b = by[book];
    const el = document.getElementById('v' + v);
    const text = el ? plain(Array.from(el.childNodes).filter(n => !(n.classList?.contains('vn') || n.classList?.contains('fb-tag'))).map(n => n.textContent).join('')) : '';
    const fbSrc = el?.querySelector('.fb-tag')?.dataset.src;
    const to = +(el?.dataset.to || v);
    const ref = `${bookName(b, vers, fbSrc || ver)} ${ch}:${v}${to > v ? '–' + to : ''}`;
    const k = keyOf(book, ch, v);
    const url = location.origin + urlFor(ver, book, ch, v);
    const short = vers[fbSrc || ver].short;
    const colors = ['yellow', 'green', 'blue', 'pink'];
    const body = openSheet(ref, `
      <p class="sheet-verse">${esc(text)}</p>
      <div class="hl-row" aria-label="Highlight">${colors.map(c => `<button type="button" data-hl="${c}" aria-label="Highlight ${c}" style="background:var(--hl-${c})" class="${marks.hl[k] === c ? 'on' : ''}"></button>`).join('')}
        <button type="button" class="clear" data-hl="" aria-label="Remove highlight">${icon('x')}</button></div>
      <div class="actions-grid">
        <button type="button" data-a="bm" class="${marks.bm[k] ? 'on' : ''}">${icon('bookmark')}${marks.bm[k] ? 'Saved' : 'Bookmark'}</button>
        <button type="button" data-a="note">${icon('pen')}Note</button>
        <button type="button" data-a="copy">${icon('copy')}Copy</button>
        <button type="button" data-a="share">${icon('share')}Share</button>
        <button type="button" data-a="image">${icon('image')}Image</button>
        <button type="button" data-a="compare">${icon('compare')}Compare</button>
        <button type="button" data-a="listen">${icon('play')}Listen</button>
        <button type="button" data-a="open">${icon('right')}Verse page</button>
      </div><div data-extra></div>`, onClose);
    body.addEventListener('click', async e => {
      const hl = e.target.closest('[data-hl]');
      if (hl) {
        if (hl.dataset.hl) marks.hl[k] = hl.dataset.hl; else delete marks.hl[k];
        marks.save(); paintMarks($('.chapter')); closeSheet(); return;
      }
      const btn = e.target.closest('[data-a]'); if (!btn) return;
      const a = btn.dataset.a, extra = $('[data-extra]', body);
      if (a === 'bm') {
        if (marks.bm[k]) delete marks.bm[k]; else marks.bm[k] = Date.now();
        marks.save(); paintMarks($('.chapter')); toast(marks.bm[k] ? 'Bookmarked' : 'Bookmark removed'); closeSheet();
      } else if (a === 'note') {
        extra.innerHTML = `<p></p><label class="sr-only" for="note">Note</label><textarea id="note" placeholder="Write a note…">${esc(marks.notes[k]?.text || '')}</textarea>
          <p><button class="btn" type="button" data-save-note>${icon('check')} Save note</button></p>`;
        $('textarea', extra).focus();
        $('[data-save-note]', extra).onclick = () => {
          const t = $('textarea', extra).value.trim();
          if (t) marks.notes[k] = { text: t, ts: Date.now() }; else delete marks.notes[k];
          marks.save(); paintMarks($('.chapter')); toast('Note saved'); closeSheet();
        };
      } else if (a === 'copy') {
        copyText(`“${text}” — ${ref} (${short})\n${url}`);
      } else if (a === 'share') {
        shareIt({ title: ref, text: `“${text}” — ${ref} (${short})`, url });
      } else if (a === 'image') {
        imageSheet(text, `${ref} · ${short}`);
      } else if (a === 'compare') {
        extra.innerHTML = '<p class="muted">Loading…</p>';
        try {
          const others = Object.keys(vers).filter(k => k !== ver);
          const parts = await Promise.all(others.map(async o => {
            const d = await getChapter(o, book, ch);
            const own = d.verses[v - 1] !== null;
            const rows = rowsFor(d, v, to).filter(r => r[2] === o);
            return `<div class="compare-item" lang="${vers[o].lang}"><h2><a href="${urlFor(o, book, ch, v)}">${esc(bookName(b, vers, o))} ${ch}:${rows.length ? rows.map(rangeLabel).join(', ') : v} · ${esc(vers[o].short)}</a></h2>
              <p>${own && rows.length ? rows.map(r => verseHtml(r[3], o)).join(' ') : '<em>Not yet available in ' + esc(vers[o].label) + '.</em>'}</p></div>`;
          }));
          extra.innerHTML = `<div class="compare">${parts.join('')}</div>`;
        } catch (err) { extra.innerHTML = '<p class="muted">Couldn’t load the other versions.</p>'; }
      } else if (a === 'listen') {
        closeSheet(); startListening(v);
      } else if (a === 'open') {
        closeSheet(true); navigate(urlFor(ver, book, ch, v));
      }
    });
  }

  // verse image (1080×1080 canvas)
  function drawVerseImage(text, ref) {
    const S = 1080, c = document.createElement('canvas'); c.width = c.height = S;
    const g = c.getContext('2d');
    const grad = g.createLinearGradient(0, 0, S, S); grad.addColorStop(0, '#1d5aa0'); grad.addColorStop(1, '#1f9a5a');
    g.fillStyle = grad; g.fillRect(0, 0, S, S);
    g.fillStyle = 'rgba(255,255,255,.08)'; g.beginPath(); g.arc(S * .85, S * .12, 260, 0, 7); g.fill();
    g.beginPath(); g.arc(S * .1, S * .95, 220, 0, 7); g.fill();
    const quote = `“${text}”`;
    let size = 64, lines;
    const wrap = sz => {
      g.font = `${sz}px Georgia, 'Times New Roman', serif`;
      const words = quote.split(/\s+/), out = []; let line = '';
      for (const w of words) { const t = line ? line + ' ' + w : w; if (g.measureText(t).width > S - 180 && line) { out.push(line); line = w; } else line = t; }
      out.push(line); return out;
    };
    do { lines = wrap(size); size -= 4; } while (lines.length * size * 1.45 > S - 380 && size > 26);
    size += 4; const lh = size * 1.45;
    g.fillStyle = '#fff'; g.textAlign = 'center'; g.textBaseline = 'middle';
    const top = (S - 120 - lines.length * lh) / 2 + lh / 2;
    lines.forEach((l, i) => g.fillText(l, S / 2, top + i * lh));
    g.font = `600 40px system-ui, -apple-system, 'Segoe UI', sans-serif`;
    g.fillText(ref, S / 2, top + lines.length * lh + 40);
    g.font = `500 28px system-ui, -apple-system, sans-serif`; g.fillStyle = 'rgba(255,255,255,.8)';
    g.fillText('holybiblewords.com', S / 2, S - 70);
    return c;
  }
  function imageSheet(text, ref) {
    const c = drawVerseImage(text, ref);
    const url = c.toDataURL('image/png');
    const body = openSheet('Verse image', `<img class="img-preview" src="${url}" alt="${esc(ref)}">
      <div class="verse-actions"><a class="btn" download="${esc(ref.replace(/[^\w]+/g, '-'))}.png" href="${url}">${icon('download')} Save image</a>
      <button class="btn ghost" type="button" data-share-img>${icon('share')} Share</button></div>`);
    $('[data-share-img]', body).onclick = () => c.toBlob(b => {
      const file = new File([b], 'verse.png', { type: 'image/png' });
      if (navigator.canShare?.({ files: [file] })) shareIt({ files: [file], title: ref, text: ref });
      else toast('Use “Save image”, then share it from your photos');
    });
  }

  // listen (speech synthesis)
  let speaking = false;
  function startListening(fromVerse = 1) {
    if (!('speechSynthesis' in window)) { toast('Listening isn’t supported on this device'); return; }
    stopListening();
    const art = $('.chapter'); if (!art) return;
    const lang = art.lang === 'en' ? 'en-US' : 'fil-PH';
    const voices = speechSynthesis.getVoices();
    const voice = voices.find(v => v.lang.startsWith(art.lang === 'en' ? 'en' : 'fil')) || null;
    const verses = $$('.v', art).filter(el => +el.dataset.v >= fromVerse);
    speaking = true; setListenBtn(true);
    verses.forEach((el, i) => {
      const u = new SpeechSynthesisUtterance(plain(Array.from(el.childNodes).filter(n => !(n.classList?.contains('vn') || n.classList?.contains('fb-tag'))).map(n => n.textContent).join('')));
      u.lang = lang; if (voice) u.voice = voice; u.rate = .95;
      u.onstart = () => { $$('.v.speaking').forEach(x => x.classList.remove('speaking')); el.classList.add('speaking'); el.scrollIntoView({ block: 'center', behavior: 'smooth' }); };
      if (i === verses.length - 1) u.onend = () => stopListening();
      speechSynthesis.speak(u);
    });
  }
  function stopListening() {
    if (!speaking) return;
    speaking = false; try { speechSynthesis.cancel(); } catch (e) { /* ignore */ }
    $$('.v.speaking').forEach(x => x.classList.remove('speaking')); setListenBtn(false);
  }
  function setListenBtn(on) {
    const b = $('[data-action=listen]'); if (!b) return;
    b.innerHTML = icon(on ? 'pause' : 'play'); b.setAttribute('aria-pressed', String(on));
  }

  // ---------- verse page ----------
  function initVerse(main) {
    const art = $('.verse-page', main); if (!art) return;
    const { ver, book } = art.dataset; const ch = +art.dataset.ch, v = +art.dataset.v;
    store.set('last', { ver, book, ch, v, ts: Date.now() });
    pushHistory({ ver, book, ch, v }); updateReadLinks();
    const k = keyOf(book, ch, v);
    const save = $('[data-action=verse-save]', main);
    const paint = () => { save.innerHTML = icon('bookmark') + (marks.bm[k] ? ' Saved' : ' Save'); };
    paint();
    const text = plain($('.verse-card p', art).textContent);
    const ref = $('.verse-card footer', art).textContent.trim();
    const url = location.origin + urlFor(ver, book, ch, v);
    $('[data-action=verse-copy]', main).onclick = () => copyText(`“${text}” — ${ref}\n${url}`);
    $('[data-action=verse-share]', main).onclick = () => shareIt({ title: ref, text: `“${text}” — ${ref}`, url });
    $('[data-action=verse-image]', main).onclick = () => imageSheet(text, ref);
    save.onclick = () => { if (marks.bm[k]) delete marks.bm[k]; else marks.bm[k] = Date.now(); marks.save(); paint(); toast(marks.bm[k] ? 'Bookmarked' : 'Bookmark removed'); };
  }

  // ---------- picker ----------
  async function openPicker(curBook, curCh) {
    const [{ list, by }, vers] = await Promise.all([getBooks(), getVers()]);
    const ver = $('.chapter, .verse-page, #main[data-ver]')?.dataset.ver || $('#main').dataset.ver || prefVer();
    let testament = by[curBook]?.t || 'ot';
    const body = openSheet('Go to', '');
    const showBooks = () => {
      body.innerHTML = `<input class="picker-filter" type="search" placeholder="Filter books, or type John 3:16" aria-label="Filter books">
        <div class="tabs" role="tablist"><button role="tab" data-t="ot" aria-selected="${testament === 'ot'}">Old Testament</button><button role="tab" data-t="nt" aria-selected="${testament === 'nt'}">New Testament</button></div>
        <ul class="book-grid"></ul>`;
      const grid = $('.book-grid', body), input = $('.picker-filter', body);
      const draw = () => {
        const f = input.value.trim().toLowerCase().replace(/\s+/g, ' ');
        const items = list.filter(b => f ? (bookName(b, vers, ver).toLowerCase().includes(f) || b.names.en.toLowerCase().includes(f) || b.slug.includes(f.replace(/ /g, '')) || b.abbr.includes(f.replace(/ /g, ''))) : b.t === testament);
        grid.innerHTML = items.map(b => `<li><a href="${urlFor(ver, b.slug)}" data-pick="${b.slug}" class="${b.slug === curBook ? 'cur' : ''}${b.available[ver] === 0 ? ' na' : ''}">${esc(bookName(b, vers, ver))}<small>${b.verses.length}</small></a></li>`).join('')
          || '<li class="muted">Press Enter to go to that reference</li>';
      };
      draw();
      input.addEventListener('input', draw);
      input.addEventListener('keydown', async e => {
        if (e.key !== 'Enter') return;
        e.preventDefault();
        const r = await fetch('/api/ref?' + new URLSearchParams({ q: input.value, v: ver })).then(r => r.json()).catch(() => null);
        if (r?.url) { closeSheet(true); navigate(r.url); }
        else { const first = $('[data-pick]', grid); if (first) showChapters(first.dataset.pick); }
      });
      $$('[data-t]', body).forEach(t => t.onclick = () => { testament = t.dataset.t; input.value = ''; showBooks(); });
      grid.addEventListener('click', e => { const a = e.target.closest('[data-pick]'); if (!a) return; e.preventDefault(); e.stopPropagation(); showChapters(a.dataset.pick); });
      if (matchMedia('(min-width: 700px)').matches) input.focus();
    };
    const showChapters = slug => {
      const b = by[slug];
      if (b.verses.length === 1) { showVerses(slug, 1); return; }
      body.innerHTML = `<div class="picker-crumb"><button type="button" data-back>${icon('left')} Books</button><span>${esc(bookName(b, vers, ver))}</span></div>
        <ul class="num-grid">${b.verses.map((_, i) => `<li><a href="${urlFor(ver, slug, i + 1)}" data-ch="${i + 1}"${slug === curBook && i + 1 === curCh ? ' aria-current="page"' : ''}>${i + 1}</a></li>`).join('')}</ul>
        <p class="muted">Tap a chapter to read it, or long-press to pick a verse.</p>`;
      $('[data-back]', body).onclick = showBooks;
      $$('[data-ch]', body).forEach(a => {
        let t;
        a.addEventListener('pointerdown', () => { t = setTimeout(() => { t = 'long'; showVerses(slug, +a.dataset.ch); }, 450); });
        a.addEventListener('pointerup', () => { if (t !== 'long') clearTimeout(t); });
        a.addEventListener('pointerleave', () => { if (t !== 'long') clearTimeout(t); });
        a.addEventListener('click', e => { if (t === 'long') { e.preventDefault(); e.stopPropagation(); } });
        a.addEventListener('contextmenu', e => e.preventDefault());
      });
    };
    const showVerses = (slug, c) => {
      const b = by[slug];
      body.innerHTML = `<div class="picker-crumb"><button type="button" data-back>${icon('left')} ${b.verses.length === 1 ? 'Books' : 'Chapters'}</button><span>${esc(bookName(b, vers, ver))} ${c}</span></div>
        <p><a class="btn" href="${urlFor(ver, slug, c)}">${icon('book')} Read chapter ${c}</a></p>
        <ul class="num-grid small">${Array.from({ length: b.verses[c - 1] }, (_, i) => `<li><a href="${urlFor(ver, slug, c)}#v${i + 1}">${i + 1}</a></li>`).join('')}</ul>`;
      $('[data-back]', body).onclick = () => (b.verses.length === 1 ? showBooks() : showChapters(slug));
    };
    if (curBook && by[curBook] && $('#main').dataset.page === 'book') showChapters(curBook); else showBooks();
  }

  // ---------- settings ----------
  function openSettings() {
    const seg = (name, opts) => `<div class="seg" data-set="${name}">${opts.map(([v, l]) => `<button type="button" data-val="${v}" class="${String(settings[name]) === String(v) ? 'on' : ''}">${l}</button>`).join('')}</div>`;
    const body = openSheet('Reading settings', `
      <div class="set-row"><span>Theme</span>${seg('theme', [['auto', 'Auto'], ['light', 'Light'], ['sepia', 'Sepia'], ['dark', 'Dark']])}</div>
      <div class="set-row"><span>Text size</span><input type="range" min="14" max="30" step="1" value="${settings.size}" data-range="size" aria-label="Text size"></div>
      <div class="set-row"><span>Font</span>${seg('font', [['serif', 'Serif'], ['sans', 'Sans']])}</div>
      <div class="set-row"><span>Line spacing</span>${seg('lh', [['1.5', 'Compact'], ['1.75', 'Normal'], ['2.05', 'Relaxed']])}</div>
      <div class="set-row"><span>Layout</span>${seg('layout', [['verses', 'Verse per line'], ['para', 'Paragraph']])}</div>
      <div class="set-row"><span>Verse numbers</span>${seg('nums', [['true', 'Show'], ['false', 'Hide']])}</div>
      <div class="set-row"><span>Side by side</span>${seg('parallel', [['false', 'Off'], ['true', 'On']])}</div>
      <div class="set-row"><span>Side by side with</span>${seg('pver', [['auto', 'Auto'], ...Object.entries(VERS || {}).map(([k, v]) => [k, v.short])])}</div>
      ${native() && window.Capacitor?.Plugins?.LocalNotifications ? `<div class="set-row"><span>Daily verse reminder</span>${seg('remind', [['false', 'Off'], ['true', '7:00 AM']])}</div>` : ''}
      <div class="set-row"><span>Offline reading</span><a href="/app/">Download a version</a></div>`);
    body.addEventListener('click', e => {
      const b = e.target.closest('[data-val]'); if (!b) return;
      const name = b.parentElement.dataset.set; let val = b.dataset.val;
      if (val === 'true' || val === 'false') val = val === 'true';
      else if (name === 'lh') val = +val;
      settings[name] = val; saveSettings();
      $$('button', b.parentElement).forEach(x => x.classList.toggle('on', x === b));
      if (name === 'parallel' || (name === 'pver' && settings.parallel)) setParallel(settings.parallel);
      if (name === 'remind') setReminder(val);
    });
    $('[data-range=size]', body).addEventListener('input', e => { settings.size = +e.target.value; saveSettings(); });
  }
  async function setReminder(on) {
    const LN = window.Capacitor?.Plugins?.LocalNotifications; if (!LN) return;
    try {
      await LN.cancel({ notifications: [{ id: 7001 }] });
      if (!on) return;
      const p = await LN.requestPermissions();
      if (p.display !== 'granted') { toast('Notifications are turned off for this app'); return; }
      await LN.schedule({ notifications: [{ id: 7001, title: 'Verse of the Day', body: 'Your verse for today is ready.', schedule: { on: { hour: 7, minute: 0 }, allowWhileIdle: true }, extra: { url: '/verse-of-the-day/' } }] });
      toast('Daily reminder set for 7:00 AM');
    } catch (e) { toast('Couldn’t set the reminder'); }
  }

  // ---------- global actions ----------
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-action]'); if (!b) return;
    const a = b.dataset.action;
    if (a === 'settings') openSettings();
    else if (a === 'theme') { settings.theme = isDark() ? 'light' : 'dark'; saveSettings(); toast(isDark() ? 'Dark mode on' : 'Dark mode off'); }
    else if (a === 'picker') openPicker(b.dataset.book, +b.dataset.ch);
    else if (a === 'parallel') { settings.parallel = !settings.parallel; saveSettings(); setParallel(settings.parallel); }
    else if (a === 'listen') { speaking ? stopListening() : startListening(+(captureAnchor()?.v || 1)); }
    else if (a === 'share-votd') { const p = votdPayload(); shareIt({ title: 'Verse of the Day — ' + p.ref, text: `“${p.text}” — ${p.ref} (${p.short})`, url: p.url }); }
    else if (a === 'image-votd') { const p = votdPayload(); imageSheet(p.text, `${p.ref} · ${p.short}`); }
    else if (a === 'install') installApp();
    else if (a === 'offline') downloadVersion(b.dataset.ver, b);
  });

  // keyboard and swipe chapter navigation
  document.addEventListener('keydown', e => {
    if (e.target.closest('input, textarea, [contenteditable]') || $('#sheet-root').firstChild || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === 'ArrowLeft') $('.reader-bar a[rel=prev]')?.click();
    else if (e.key === 'ArrowRight') $('.reader-bar a[rel=next]')?.click();
    else if (e.key === '/') { const q = $('#main form.jump input[name=q]'); if (q) { e.preventDefault(); q.focus(); } else { e.preventDefault(); openPicker(); } }
  });
  let sx = 0, sy = 0, st = 0;
  document.addEventListener('touchstart', e => { if (e.touches.length === 1) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; st = Date.now(); } }, { passive: true });
  document.addEventListener('touchend', e => {
    if (!$('.chapter') || $('#sheet-root').firstChild || !sx) return;
    const dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Date.now() - st < 600 && Math.abs(dx) > 80 && Math.abs(dy) < 50 && !getSelection().toString()) {
      $(`.reader-bar a[rel=${dx < 0 ? 'next' : 'prev'}]`)?.click();
    }
    sx = 0;
  }, { passive: true });

  // ---------- reading plan (Bible in a year) ----------
  async function planDays() {
    const { list } = await getBooks();
    const all = [];
    list.forEach(b => b.verses.forEach((_, i) => all.push([b.slug, i + 1])));
    const days = [];
    for (let d = 0; d < 365; d++) days.push(all.slice(Math.floor(d * all.length / 365), Math.floor((d + 1) * all.length / 365)));
    return { days, total: all.length };
  }
  const dayDiff = (a, b) => Math.round((new Date(b + 'T12:00:00') - new Date(a + 'T12:00:00')) / 864e5);
  async function initPlan(main) {
    const box = $('#plan-app', main); if (!box) return;
    const [{ days, total }, { by }, vers] = await Promise.all([planDays(), getBooks(), getVers()]);
    const plan = store.get('plan', null);
    if (!plan) {
      box.innerHTML = `<div class="plan-day"><h2>Start today</h2><p class="muted">Day 1 begins with Genesis 1–3. Each day lists 3–4 chapters; tick them off as you read, in either version.</p>
        <p><button class="btn" type="button" data-start>${icon('calendar')} Start the plan</button></p></div>`;
      $('[data-start]', box).onclick = () => { store.set('plan', { start: localDate(), done: {} }); initPlan(main); };
      return;
    }
    let day = Math.min(364, Math.max(0, dayDiff(plan.start, localDate())));
    const draw = () => {
      const done = Object.keys(plan.done).length;
      const ver = prefVer();
      box.innerHTML = `<p><strong>${done}</strong> of ${total} chapters read · ${Math.round(done / total * 100)}%</p>
        <div class="plan-progress"><div style="width:${done / total * 100}%"></div></div>
        <div class="plan-nav"><button class="btn ghost" type="button" data-d="-1" ${day === 0 ? 'style="visibility:hidden"' : ''}>${icon('left')} Day ${day}</button>
        <button class="btn ghost" type="button" data-today>Today</button>
        <button class="btn ghost" type="button" data-d="1" ${day === 364 ? 'style="visibility:hidden"' : ''}>Day ${day + 2} ${icon('right')}</button></div>
        <div class="plan-day"><h2>Day ${day + 1} <small class="muted">${new Date(new Date(plan.start + 'T12:00:00').getTime() + day * 864e5).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}</small></h2>
        <ul>${days[day].map(([s, c]) => `<li><input type="checkbox" data-k="${s}.${c}" ${plan.done[s + '.' + c] ? 'checked' : ''} aria-label="Mark ${esc(bookName(by[s], vers, ver))} ${c} read">
          <a href="${urlFor(ver, s, c)}">${esc(bookName(by[s], vers, ver))} ${c}</a></li>`).join('')}</ul></div>
        <p><button class="btn ghost" type="button" data-reset>Restart plan</button></p>`;
    };
    draw();
    box.onclick = e => {
      const t = e.target.closest('button'); if (!t) return;
      if (t.dataset.d) { day += +t.dataset.d; draw(); }
      else if ('today' in t.dataset) { day = Math.min(364, Math.max(0, dayDiff(plan.start, localDate()))); draw(); }
      else if ('reset' in t.dataset && confirm('Restart the reading plan from today? Your progress will be cleared.')) { store.set('plan', null); localStorage.removeItem('hbw.plan'); initPlan(main); }
    };
    box.onchange = e => {
      const k = e.target.dataset.k; if (!k) return;
      if (e.target.checked) plan.done[k] = 1; else delete plan.done[k];
      store.set('plan', plan); draw();
    };
  }
  function planButton(main, book, ch) {
    const plan = store.get('plan', null); if (!plan) return;
    const foot = $('.chapter-foot', main); if (!foot) return;
    const k = `${book}.${ch}`;
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'btn ghost';
    const paint = () => { b.innerHTML = icon('check') + (plan.done[k] ? ' Read' : ' Mark as read'); b.classList.toggle('on', !!plan.done[k]); };
    paint();
    b.onclick = () => { if (plan.done[k]) delete plan.done[k]; else plan.done[k] = 1; store.set('plan', plan); paint(); toast(plan.done[k] ? 'Marked as read' : 'Unmarked'); };
    foot.insertBefore(b, foot.lastElementChild);
  }

  // ---------- saved ----------
  async function initSaved(main) {
    const box = $('#saved-app', main); if (!box) return;
    const [{ by }, vers] = await Promise.all([getBooks(), getVers()]);
    const ver = prefVer();
    const textOf = async (book, ch, v) => { try { const d = await getChapter(ver, book, ch); const r = rowsFor(d, v)[0]; return r ? [r[3], r[2]] : ['', ver]; } catch (e) { return ['', ver]; } };
    const label = (book, ch, v) => `${bookName(by[book], vers, ver)} ${ch}${v ? ':' + v : ''}`;
    const show = async tab => {
      $$('.tabs [data-tab]', main).forEach(t => t.setAttribute('aria-selected', String(t.dataset.tab === tab)));
      let items = [];
      if (tab === 'bookmarks') items = Object.entries(marks.bm).sort((a, b) => b[1] - a[1]).map(([k]) => ({ k }));
      if (tab === 'highlights') items = Object.entries(marks.hl).map(([k, c]) => ({ k, c }));
      if (tab === 'notes') items = Object.entries(marks.notes).sort((a, b) => b[1].ts - a[1].ts).map(([k, n]) => ({ k, note: n.text }));
      if (tab === 'history') {
        const h = store.get('history', []);
        box.innerHTML = h.length ? `<ol class="results">${h.map(x => `<li><a href="${urlFor(ver, x.book, x.ch)}${x.v > 1 ? '#v' + x.v : ''}"><strong>${esc(label(x.book, x.ch))}</strong><time>${new Date(x.ts).toLocaleString()}</time></a></li>`).join('')}</ol>
          <p><button class="btn ghost" type="button" data-clear-history>Clear history</button></p>` : '<p class="empty">Chapters you read will appear here.</p>';
        $('[data-clear-history]', box)?.addEventListener('click', () => { store.set('history', []); show('history'); });
        return;
      }
      items = items.filter(x => by[parseKey(x.k).book]);
      if (!items.length) { box.innerHTML = `<p class="empty">No ${tab} yet. Tap any verse while reading to add one.</p>`; return; }
      box.innerHTML = '<p class="muted">Loading…</p>';
      const rows = await Promise.all(items.slice(0, 300).map(async x => {
        const { book, ch, v } = parseKey(x.k);
        const t = await textOf(book, ch, v);
        return `<li class="saved-item"><a href="${urlFor(ver, book, ch)}#v${v}"><strong>${x.c ? `<span class="swatch" style="background:var(--hl-${x.c})"></span>` : ''}${esc(label(book, ch, v))}</strong>
          <span>${verseHtml(t[0], t[1])}</span>${x.note ? `<span class="muted">✎ ${esc(x.note)}</span>` : ''}</a>
          <button class="icon-btn" type="button" data-remove="${x.k}" aria-label="Remove">${icon('x')}</button></li>`;
      }));
      box.innerHTML = `<ol class="results">${rows.join('')}</ol>`;
      box.onclick = e => {
        const r = e.target.closest('[data-remove]'); if (!r) return;
        const k = r.dataset.remove;
        delete { bookmarks: marks.bm, highlights: marks.hl, notes: marks.notes }[tab][k];
        marks.save(); r.closest('li').remove();
      };
    };
    $$('.tabs [data-tab]', main).forEach(t => t.onclick = () => show(t.dataset.tab));
    show('bookmarks');
  }

  // ---------- install + offline ----------
  let installEvt = null;
  window.addEventListener('beforeinstallprompt', e => { e.preventDefault(); installEvt = e; $$('[data-action=install]').forEach(b => { b.hidden = false; }); });
  async function installApp() {
    if (!installEvt) { toast('Use your browser menu: “Install app” or “Add to Home Screen”'); return; }
    installEvt.prompt(); await installEvt.userChoice; installEvt = null;
    $$('[data-action=install]').forEach(b => { b.hidden = true; });
  }
  function initApp(main) {
    if (installEvt) $$('[data-action=install]', main).forEach(b => { b.hidden = false; });
    const done = store.get('offline', {});
    const st = $('[data-offline-status]', main);
    getVers().then(vers => {
      const list = Object.keys(done).filter(k => done[k]).map(k => vers[k]?.label).filter(Boolean);
      if (st) st.textContent = list.length ? 'Downloaded: ' + list.join(', ') : '';
    });
  }
  async function downloadVersion(ver, btn) {
    if (!('caches' in window)) { toast('Offline reading isn’t supported in this browser'); return; }
    const { list } = await getBooks();
    const cache = await caches.open('hbw-data');
    const label = btn.textContent;
    btn.disabled = true;
    let n = 0;
    try {
      // also fetch the version that fills this one's gaps (AB -> Ang Pulong sa Dios)
      const vers = await getVers();
      const want = [ver, ...(vers[ver].fallback || []).slice(0, 1)];
      const urls = want.flatMap(k => list.map(b => `/data/${k}/${b.slug}.json`));
      for (const url of urls) {
        if (!(await cache.match(url))) {
          const res = await fetch(url, { cache: 'no-cache' });
          if (!res.ok) throw new Error(res.status);
          await cache.put(url, res);
        }
        btn.textContent = `Downloading… ${Math.round(++n / urls.length * 100)}%`;
      }
      for (const u of ['/data/books.json', '/data/versions.json', '/data/votd.json', '/offline/']) await cache.add(u).catch(() => {});
      const done = store.get('offline', {}); done[ver] = Date.now(); store.set('offline', done);
      btn.innerHTML = icon('check') + ' Downloaded';
      toast('Saved — you can now read it without a connection');
      const st = $('[data-offline-status]'); if (st) initApp($('#main'));
    } catch (e) {
      btn.textContent = label; btn.disabled = false; toast('Download failed — check your connection');
    }
  }
  // offline shell: render a chapter from downloaded data when the page itself isn't cached
  // Offline shell: the service worker serves the cached /offline/ page for any page
  // that isn't saved on the device; render the requested route from downloaded data.
  async function initOffline(main) {
    let books, vers;
    try { [books, vers] = await Promise.all([getBooks(), getVers()]); } catch (e) { return; }
    const { list, by } = books;
    const path = location.pathname;
    const done = store.get('offline', {});
    const have = Object.keys(vers).filter(k => done[k]);
    const versionLinks = (mk) => $$('.topbar .ver-switch a').forEach(a => { a.setAttribute('href', mk(a.dataset.ver)); });
    const notDownloaded = ver => `<p class="notice">${esc(vers[ver].label)} isn’t downloaded on this device. ${have.length
      ? 'Downloaded: ' + have.map(k => `<a href="/${k}/">${esc(vers[k].label)}</a>`).join(', ') + '.'
      : 'Connect to the internet and download a version on the <a href="/app/">Get the app</a> page.'}</p>`;
    let m;

    // chapter or verse
    if ((m = path.match(/^\/([a-z]+)\/([a-z0-9]+)\/(\d+)\/(?:(\d+)\/)?$/)) && vers[m[1]] && by[m[2]]) {
      const [, ver, book, ch, v] = m;
      const b = by[book];
      main.dataset.switch = '1';
      versionLinks(k => urlFor(k, book, ch));
      markVersion(ver);
      let d;
      try { d = await getChapter(ver, book, ch); } catch (e) {
        main.innerHTML = `<div class="wrap narrow"><h1>${esc(bookName(b, vers, ver))} ${ch}</h1>${notDownloaded(ver)}</div>`; return;
      }
      const idx = list.indexOf(b);
      const prev = +ch > 1 ? [book, +ch - 1] : idx > 0 ? [list[idx - 1].slug, list[idx - 1].verses.length] : null;
      const next = +ch < b.verses.length ? [book, +ch + 1] : idx < list.length - 1 ? [list[idx + 1].slug, 1] : null;
      const lbl = r => `${esc(bookName(by[r[0]], vers, ver))} ${r[1]}`;
      main.dataset.page = 'chapter';
      main.innerHTML = `<div class="reader-bar">${prev ? `<a class="icon-btn" rel="prev" href="${urlFor(ver, prev[0], prev[1])}" aria-label="Previous chapter">${icon('left')}</a>` : '<span class="icon-btn"></span>'}
        <button type="button" class="picker-btn" data-action="picker" data-book="${book}" data-ch="${ch}"><span>${esc(bookName(b, vers, ver))} ${ch}</span>${icon('down')}</button>
        ${next ? `<a class="icon-btn" rel="next" href="${urlFor(ver, next[0], next[1])}" aria-label="Next chapter">${icon('right')}</a>` : '<span class="icon-btn"></span>'}</div>
        <div class="wrap reader-wrap"><article class="chapter" lang="${vers[ver].lang}" data-ver="${ver}" data-book="${book}" data-ch="${ch}">
        <h1><span class="book-title">${esc(bookName(b, vers, ver))}</span> <span class="ch-num">${ch}</span></h1>
        <div class="verses">${d.rows.map(r => `<span class="v${r[2] === ver ? '' : ' fb'}" id="v${r[0]}" data-v="${r[0]}"${r[1] > r[0] ? ` data-to="${r[1]}"` : ''}>${Array.from({ length: r[1] - r[0] }, (_, j) => `<span class="v-anchor" id="v${r[0] + j + 1}"></span>`).join('')}<a class="vn" href="${urlFor(ver, book, ch, r[0])}">${rangeLabel(r)}</a> ${verseHtml(r[3], r[2])}${r[2] === ver ? '' : ` <span class="fb-tag" data-src="${r[2]}">${esc(vers[r[2]].short)}</span>`}</span> `).join('')}</div></article>
        <nav class="chapter-foot">${prev ? `<a class="btn ghost" href="${urlFor(ver, prev[0], prev[1])}">${icon('left')} ${lbl(prev)}</a>` : '<span></span>'}${next ? `<a class="btn" href="${urlFor(ver, next[0], next[1])}">${lbl(next)} ${icon('right')}</a>` : '<span></span>'}</nav>
        <p class="ver-credit">Offline copy · ${esc(vers[ver].fullTitle || vers[ver].label)}</p></div>`;
      document.title = `${bookName(b, vers, ver)} ${ch} | Holy Bible Words`;
      initChapter(main);
      if (v) scrollToHash('#v' + v);
      return;
    }

    // book: chapter grid
    if ((m = path.match(/^\/([a-z]+)\/([a-z0-9]+)\/$/)) && vers[m[1]] && by[m[2]]) {
      const [, ver, book] = m; const b = by[book];
      main.dataset.switch = '1'; versionLinks(k => urlFor(k, book)); markVersion(ver);
      main.innerHTML = `<div class="wrap"><header class="page-head"><h1>${esc(bookName(b, vers, ver))}</h1><p class="muted">${esc(vers[ver].label)} · offline</p></header>
        ${done[ver] ? '' : notDownloaded(ver)}
        <ul class="num-grid">${b.verses.map((_, i) => `<li><a href="${urlFor(ver, book, i + 1)}">${i + 1}</a></li>`).join('')}</ul></div>`;
      return;
    }

    // version: books grid
    if ((m = path.match(/^\/([a-z]+)\/$/)) && vers[m[1]]) {
      const ver = m[1];
      main.dataset.switch = '1'; versionLinks(k => `/${k}/`); markVersion(ver);
      const grid = t => `<ul class="book-grid">${list.filter(b => b.t === t).map(b => `<li><a href="${urlFor(ver, b.slug)}">${esc(bookName(b, vers, ver))}<small>${b.verses.length}</small></a></li>`).join('')}</ul>`;
      main.innerHTML = `<div class="wrap"><header class="page-head"><h1>${esc(vers[ver].label)}</h1><p class="muted">Offline</p></header>
        ${done[ver] ? '' : notDownloaded(ver)}
        <section class="books-section"><h2>Old Testament</h2>${grid('ot')}</section><section class="books-section"><h2>New Testament</h2>${grid('nt')}</section></div>`;
      return;
    }

    // anything else (home, search, …): an offline start page
    const last = store.get('last', null);
    const ver = have.includes(prefVer()) ? prefVer() : have[0] || prefVer();
    main.innerHTML = `<div class="wrap narrow"><header class="page-head"><h1>You’re offline</h1>
      <p class="muted">${have.length ? 'You can keep reading the versions saved on this device.' : 'No version is downloaded on this device yet.'}</p></header>
      ${last && by[last.book] ? `<section class="continue"><h2>Continue reading</h2><a class="continue-link" href="${urlFor(have.includes(last.ver) ? last.ver : ver, last.book, last.ch)}${last.v > 1 ? '#v' + last.v : ''}">${esc(bookName(by[last.book], vers, have.includes(last.ver) ? last.ver : ver))} ${last.ch}</a></section>` : ''}
      ${have.length ? `<section><h2>Saved on this device</h2><div class="ver-cards">${have.map(k => `<a class="ver-card" href="/${k}/"><strong>${esc(vers[k].label)}</strong><span>Downloaded · read offline</span>${icon('right')}</a>`).join('')}</div></section>`
        : '<p class="notice">Connect to the internet, open the <a href="/app/">Get the app</a> page and tap a version to download it.</p>'}</div>`;
  }

  // ---------- boot ----------
  applySettings();
  getVers().catch(() => {});
  darkMQ.addEventListener?.('change', applySettings);
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => navigator.serviceWorker.register('/sw.js').catch(() => {}));
  }
  // native app (Capacitor) integration
  const plugins = window.Capacitor?.Plugins;
  plugins?.LocalNotifications?.addListener?.('localNotificationActionPerformed', ev => {
    const u = ev?.notification?.extra?.url; if (u) navigate(u);
  });
  plugins?.App?.addListener?.('backButton', ({ canGoBack }) => {
    if ($('#sheet-root').firstChild) closeSheet();
    else if (canGoBack) history.back();
    else plugins.App.exitApp();
  });
  plugins?.App?.addListener?.('appUrlOpen', ({ url }) => {
    try { const u = new URL(url); if (u.hostname.endsWith('holybiblewords.com')) navigate(u.pathname + u.search + u.hash); } catch (e) { /* ignore */ }
  });
  if (plugins?.StatusBar) {
    const dark = () => document.documentElement.dataset.theme === 'dark' || (document.documentElement.dataset.theme === 'auto' && matchMedia('(prefers-color-scheme: dark)').matches);
    const paint = () => plugins.StatusBar.setStyle({ style: dark() ? 'DARK' : 'LIGHT' }).catch(() => {});
    paint(); matchMedia('(prefers-color-scheme: dark)').addEventListener?.('change', paint);
    document.addEventListener('click', () => setTimeout(paint, 50));
  }
  initPage();
  if (location.hash) setTimeout(() => scrollToHash(location.hash), 50);
})();
