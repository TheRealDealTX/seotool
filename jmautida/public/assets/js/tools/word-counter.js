/* Word counter & text analyzer: counts, readability, keyword density, platform limits, case tools. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, debounce, app } = window.JT;
  const LIMITS = [['title', 'SEO title', 60], ['meta', 'Meta description', 160], ['x', 'X post', 280], ['gbp', 'Google Business post', 1500], ['ig', 'Instagram caption', 2200], ['li', 'LinkedIn post', 3000], ['sms', 'SMS', 160]];
  const STOP = new Set('a about above after again against all am an and any are as at be because been before being below between both but by can could did do does doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just me more most my myself no nor not now of off on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why will with would you your yours yourself yourselves also get got may might must shall us via per s t don dont can’t im it’s i’m you’re we’re'.split(' '));
  const SAMPLE = 'Hutto homeowners trust local roofers who show up on time and explain every option. A good roof inspection takes about an hour. The inspector checks shingles, flashing, vents and gutters, then documents any storm or hail damage with photos.\n\nIf repairs are needed, you get a written estimate before any work starts. Most roof repairs are finished in a single day, and a full roof replacement usually takes two to three days depending on the size of the home and the weather.';

  app.innerHTML = `
    <div class="toolbar">
      <div class="toolbar-group">
        <select class="select select-sm" id="case" aria-label="Change text case" style="width:auto"><option value="">Change case…</option><option value="upper">UPPERCASE</option><option value="lower">lowercase</option><option value="title">Title Case</option><option value="sentence">Sentence case</option></select>
        <select class="select select-sm" id="clean" aria-label="Clean up text" style="width:auto"><option value="">Clean up…</option><option value="spaces">Remove extra spaces</option><option value="lines">Remove line breaks</option><option value="blank">Remove empty lines</option><option value="quotes">Straighten quotes</option></select>
        <button type="button" class="btn btn-sm btn-ghost" id="find-toggle" aria-expanded="false">${icon('search')}Find &amp; replace</button>
      </div>
      <div class="toolbar-group">${btn('copy-text', 'Copy', { icon: 'copy', ghost: true })}${btn('save', 'Download', { icon: 'download', ghost: true })}${btn('clear', 'Clear', { icon: 'trash', ghost: true, cls: 'btn-danger' })}</div>
    </div>
    <div class="find-bar" id="find-bar" hidden><input class="input input-sm" id="find" placeholder="Find"><input class="input input-sm" id="replace" placeholder="Replace with"><label class="check-row"><input type="checkbox" id="find-case"> Match case</label><span class="muted" id="find-count"></span>${btn('replace-all', 'Replace all', { size: 'btn-sm' })}</div>
    <div class="wc-layout">
      <div class="pane"><textarea class="textarea" id="source" placeholder="Start typing or paste your text…" aria-label="Text to analyze" style="min-height:440px"></textarea></div>
      <aside class="wc-side">
        <div class="stat-grid wc-stats">
          <div class="stat big"><strong id="s-words">0</strong><span>Words</span></div>
          <div class="stat"><strong id="s-chars">0</strong><span>Characters</span></div>
          <div class="stat"><strong id="s-nospace">0</strong><span>No spaces</span></div>
          <div class="stat"><strong id="s-sentences">0</strong><span>Sentences</span></div>
          <div class="stat"><strong id="s-paras">0</strong><span>Paragraphs</span></div>
          <div class="stat"><strong id="s-read">0m</strong><span>Reading</span></div>
          <div class="stat"><strong id="s-speak">0m</strong><span>Speaking</span></div>
        </div>
        <div class="card"><div class="group-title" style="margin-top:0">Readability</div><div class="readability"><div class="score-ring small" id="r-ring" style="--score:0"><div><strong id="r-score">—</strong></div></div><div><strong id="r-label">—</strong><p class="muted" id="r-detail" style="margin:4px 0 0;font-size:14px"></p></div></div></div>
        <div class="card"><div class="group-title" style="margin-top:0">Limit <select class="select select-sm" id="limit" style="width:auto;height:30px">${LIMITS.map(([k, n, l]) => `<option value="${k}">${n} · ${l}</option>`).join('')}<option value="custom">Custom goal…</option></select></div>
          <input class="input input-sm" id="custom-limit" type="number" min="1" placeholder="Characters" hidden style="margin-bottom:10px">
          <div class="meter" id="limit-meter"><i></i></div><p class="muted" id="limit-text" style="margin:8px 0 0;font-size:14px"></p></div>
      </aside>
    </div>
    <div class="grid-2" style="margin-top:14px">
      <div class="card"><div class="group-title" style="margin-top:0">Keyword density <span class="tabs sub" role="tablist" id="ngram" style="margin:0">${[1, 2, 3].map((n, i) => `<button type="button" class="tab" role="tab" data-n="${n}" aria-selected="${i === 0}">${n} word${n > 1 ? 's' : ''}</button>`).join('')}</span></div><div id="density"></div></div>
      <div class="card"><div class="group-title" style="margin-top:0">Long sentences <span id="long-count"></span></div><div id="long"></div></div>
    </div>`;

  const src = $('#source');
  let ngram = 1;
  const segWords = text => {
    if (typeof Intl.Segmenter === 'function') return [...new Intl.Segmenter(undefined, { granularity: 'word' }).segment(text)].filter(s => s.isWordLike).map(s => s.segment);
    return text.match(/[\p{L}\p{N}]+(?:['’-][\p{L}\p{N}]+)*/gu) || [];
  };
  const sentencesOf = text => {
    if (typeof Intl.Segmenter === 'function') return [...new Intl.Segmenter(undefined, { granularity: 'sentence' }).segment(text)].map(s => s.segment.trim()).filter(s => /[\p{L}\p{N}]/u.test(s));
    return text.split(/(?<=[.!?])\s+|\n+/).map(s => s.trim()).filter(s => /[\p{L}\p{N}]/u.test(s));
  };
  function syllables(word) {
    let w = word.toLowerCase().replace(/[^a-z]/g, '');
    if (!w) return 0; if (w.length <= 3) return 1;
    w = w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, '').replace(/^y/, '');
    const m = w.match(/[aeiouy]{1,2}/g); return Math.max(1, m ? m.length : 1);
  }
  const mins = (words, wpm) => { if (!words) return '0m'; const t = words / wpm; return t < 1 ? `${Math.max(1, Math.round(t * 60))}s` : `${Math.floor(t)}m ${Math.round((t % 1) * 60)}s`; };

  function analyze() {
    const text = src.value, trimmed = text.trim();
    const words = segWords(text), wc = words.length, sentences = sentencesOf(text);
    $('#s-words').textContent = wc.toLocaleString();
    $('#s-chars').textContent = [...text].length.toLocaleString();
    $('#s-nospace').textContent = [...text.replace(/\s/g, '')].length.toLocaleString();
    $('#s-sentences').textContent = sentences.length.toLocaleString();
    $('#s-paras').textContent = trimmed ? trimmed.split(/\n\s*\n/).length : 0;
    $('#s-read').textContent = mins(wc, 238); $('#s-speak').textContent = mins(wc, 140);

    // Flesch reading ease (English).
    if (wc >= 5 && sentences.length) {
      const syl = words.reduce((s, w) => s + syllables(w), 0);
      const fre = Math.max(0, Math.min(100, 206.835 - 1.015 * (wc / sentences.length) - 84.6 * (syl / wc)));
      const grade = Math.max(0, 0.39 * (wc / sentences.length) + 11.8 * (syl / wc) - 15.59);
      const label = fre >= 80 ? 'Very easy' : fre >= 70 ? 'Easy' : fre >= 60 ? 'Plain English' : fre >= 50 ? 'Fairly difficult' : fre >= 30 ? 'Difficult' : 'Very difficult';
      $('#r-score').textContent = Math.round(fre); $('#r-ring').style.setProperty('--score', Math.round(fre));
      $('#r-ring').style.setProperty('--ring', fre >= 60 ? 'var(--ok)' : fre >= 40 ? 'var(--warn)' : 'var(--danger)');
      $('#r-label').textContent = `${label} · grade ${grade.toFixed(1)}`;
      $('#r-detail').textContent = `Flesch reading ease. ${(wc / sentences.length).toFixed(1)} words per sentence, ${(syl / wc).toFixed(2)} syllables per word.`;
    } else { $('#r-score').textContent = '—'; $('#r-ring').style.setProperty('--score', 0); $('#r-label').textContent = 'Add more text'; $('#r-detail').textContent = 'Readability needs at least a full sentence.'; }

    limit();
    density(words);
    const long = sentences.filter(s => segWords(s).length > 25);
    $('#long-count').textContent = long.length ? `${long.length}` : '';
    $('#long').innerHTML = long.length ? `<ul class="long-list">${long.slice(0, 8).map(s => `<li><span class="tag">${segWords(s).length} words</span> ${esc(s.length > 220 ? s.slice(0, 220) + '…' : s)}</li>`).join('')}</ul>` : `<p class="muted" style="margin:0">${wc ? 'No sentences over 25 words — nice and scannable.' : 'Sentences over 25 words will appear here.'}</p>`;
    store.set('words:draft', text.length < 300000 ? text : '');
    if (find.value) findCount();
  }
  function density(words) {
    const lower = words.map(w => w.toLowerCase());
    const counts = new Map();
    for (let i = 0; i + ngram <= lower.length; i++) {
      const gram = lower.slice(i, i + ngram);
      if (ngram === 1 ? STOP.has(gram[0]) || gram[0].length < 3 || /^\d+$/.test(gram[0]) : STOP.has(gram[0]) || STOP.has(gram[gram.length - 1])) continue;
      const k = gram.join(' '); counts.set(k, (counts.get(k) || 0) + 1);
    }
    const top = [...counts].filter(([, c]) => ngram === 1 || c > 1).sort((a, b) => b[1] - a[1]).slice(0, 10);
    const total = Math.max(1, lower.length);
    $('#density').innerHTML = top.length ? `<div class="density">${top.map(([k, c]) => { const pct = (c * ngram / total) * 100; return `<div class="density-row"><span>${esc(k)}</span><div class="meter${pct > 4 ? ' warn' : ''}"><i style="width:${Math.min(100, pct * 10)}%"></i></div><b>${c}× · ${pct.toFixed(1)}%</b></div>`; }).join('')}</div>` : `<p class="muted" style="margin:0">${words.length ? 'No repeated phrases yet.' : 'Top keywords and phrases will appear here.'}</p>`;
  }
  function limit() {
    const sel = $('#limit').value, custom = sel === 'custom';
    $('#custom-limit').hidden = !custom;
    const max = custom ? Number($('#custom-limit').value) || 0 : LIMITS.find(l => l[0] === sel)[2];
    const len = [...src.value].length, meter = $('#limit-meter');
    if (!max) { meter.querySelector('i').style.width = '0'; $('#limit-text').textContent = 'Enter a character goal.'; return; }
    meter.querySelector('i').style.width = Math.min(100, (len / max) * 100) + '%';
    meter.className = 'meter' + (len > max ? ' bad' : len > max * 0.9 ? ' warn' : '');
    $('#limit-text').textContent = len > max ? `${(len - max).toLocaleString()} characters over the ${max.toLocaleString()} limit.` : `${(max - len).toLocaleString()} characters left of ${max.toLocaleString()}.`;
    store.set('words:limit', sel);
  }

  const smallWords = new Set('a an and as at but by for in nor of on or per the to vs via'.split(' '));
  const CASES = {
    upper: t => t.toUpperCase(), lower: t => t.toLowerCase(),
    title: t => t.toLowerCase().replace(/[\p{L}\p{N}]+(?:['’][\p{L}]+)*/gu, (w, i) => (i > 0 && smallWords.has(w) ? w : w[0].toUpperCase() + w.slice(1))),
    sentence: t => t.toLowerCase().replace(/(^\s*\p{L}|[.!?]\s+\p{L})/gu, m => m.toUpperCase()).replace(/\bi\b/g, 'I'),
  };
  const CLEAN = { spaces: t => t.replace(/[ \t]+/g, ' ').replace(/ *\n */g, '\n').trim(), lines: t => t.replace(/\s*\n+\s*/g, ' ').trim(), blank: t => t.replace(/\n\s*\n+/g, '\n'), quotes: t => t.replace(/[‘’]/g, "'").replace(/[“”]/g, '"') };
  const apply = fn => { const s = src.selectionStart, e = src.selectionEnd; if (e > s) src.setRangeText(fn(src.value.slice(s, e)), s, e, 'select'); else src.value = fn(src.value); analyze(); };
  $('#case').addEventListener('change', e => { if (CASES[e.target.value]) { apply(CASES[e.target.value]); toast('Case changed'); } e.target.value = ''; });
  $('#clean').addEventListener('change', e => { if (CLEAN[e.target.value]) { apply(CLEAN[e.target.value]); toast('Text cleaned'); } e.target.value = ''; });

  const find = $('#find');
  const findRe = () => new RegExp(find.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), $('#find-case').checked ? 'g' : 'gi');
  const findCount = () => { $('#find-count').textContent = find.value ? `${(src.value.match(findRe()) || []).length} found` : ''; };
  $('#find-toggle').addEventListener('click', () => { const open = $('#find-bar').hidden; $('#find-bar').hidden = !open; $('#find-toggle').setAttribute('aria-expanded', String(open)); if (open) find.focus(); });
  find.addEventListener('input', findCount); $('#find-case').addEventListener('change', findCount);
  $('#replace-all').addEventListener('click', () => { if (!find.value) return; const n = (src.value.match(findRe()) || []).length; src.value = src.value.replace(findRe(), () => $('#replace').value); analyze(); toast(`Replaced ${n} match${n === 1 ? '' : 'es'}`); });

  $$('#ngram .tab').forEach(b => b.addEventListener('click', () => { ngram = Number(b.dataset.n); $$('#ngram .tab').forEach(x => x.setAttribute('aria-selected', String(x === b))); density(segWords(src.value)); }));
  $('#limit').addEventListener('change', limit); $('#custom-limit').addEventListener('input', limit);
  $('#copy-text').addEventListener('click', () => copy(src.value));
  $('#save').addEventListener('click', () => download(src.value, 'text.txt'));
  $('#clear').addEventListener('click', () => { src.value = ''; analyze(); src.focus(); });
  src.addEventListener('input', debounce(analyze, 120));

  const savedLimit = store.get('words:limit'); if (savedLimit) $('#limit').value = savedLimit;
  src.value = store.get('words:draft') || SAMPLE;
  analyze();
  status('Counts update as you type. Your draft is saved only in this browser.');
})();
