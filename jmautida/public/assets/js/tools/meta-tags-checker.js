/* SEO meta tags checker: server-fetched audit, client-side scoring, previews and a tag generator. */
(function () {
  'use strict';
  const { $, $$, esc, icon, toast, status, download, copy, store, btn, tabs, tabBar, tabPanel, app, debounce } = window.JT;

  app.innerHTML = tabBar('mt', [['analyze', 'Analyze a URL', 'search'], ['generate', 'Generate tags', 'wand']]) +
    tabPanel('mt', 'analyze', `
      <form class="url-form" id="check-form" novalidate><label class="sr-only" for="url">Page URL</label>
        <input class="input" id="url" type="url" inputmode="url" placeholder="https://example.com/page" required maxlength="2048" autocomplete="url">
        <button class="btn btn-primary" id="check" type="submit">${icon('search')}Analyze page</button></form>
      <div class="chips" id="recent" style="margin-top:10px"></div>
      <div id="results" style="margin-top:18px" aria-live="polite"><div class="empty"><span class="tool-icon">${icon('search')}</span><h3>See your page like Google does.</h3><p>Enter any public URL for an SEO score, prioritized fixes, and Google &amp; social previews.</p></div></div>`, true) +
    tabPanel('mt', 'generate', `<div class="side-layout">
      <div class="card" style="display:grid;gap:14px">
        <label class="field">Page title <small id="g-title-count"></small><input class="input" id="g-title" maxlength="120" value="Roof Repair in Austin, TX | Same-Week Service"></label>
        <div class="meter" id="g-title-meter"><i></i></div>
        <label class="field">Meta description <small id="g-desc-count"></small><textarea class="input" id="g-desc" maxlength="320" rows="3">Licensed roofers fixing leaks, storm and hail damage across Austin. Free inspection and a written estimate within 48 hours.</textarea></label>
        <div class="meter" id="g-desc-meter"><i></i></div>
        <label class="field">Page URL (canonical)<input class="input" id="g-url" type="url" value="https://example.com/roof-repair"></label>
        <label class="field">Social image URL <small>1200×630 recommended</small><input class="input" id="g-image" type="url" placeholder="https://example.com/og-image.jpg"></label>
        <div class="form-grid">
          <label class="field">Site name<input class="input" id="g-site" value="Example Roofing"></label>
          <label class="field">Type<select class="select" id="g-type"><option>website</option><option>article</option><option>product</option><option>profile</option></select></label>
          <label class="field">X / Twitter handle<input class="input" id="g-twitter" placeholder="@brand"></label>
          <label class="field">Language<input class="input" id="g-lang" value="en_US"></label>
          <label class="field">Theme color<input class="input" id="g-theme" placeholder="#0a84ff"></label>
          <label class="field">Robots<select class="select" id="g-robots"><option value="index, follow">index, follow</option><option value="noindex, follow">noindex, follow</option><option value="noindex, nofollow">noindex, nofollow</option></select></label>
        </div>
      </div>
      <div style="display:grid;gap:14px;min-width:0">
        <div class="card"><div class="group-title" style="margin-top:0">Google preview</div><div id="g-serp"></div></div>
        <div class="card"><div class="group-title" style="margin-top:0">Social preview</div><div id="g-social"></div></div>
        <div class="code-out"><pre id="g-code"></pre><button type="button" class="btn btn-xs" id="g-copy">${icon('copy')}Copy HTML</button></div>
      </div></div>`);
  tabs($('#mt'));

  // Text measurement for pixel-accurate SERP truncation.
  const ctx = document.createElement('canvas').getContext('2d');
  const px = (text, font) => { ctx.font = font; return ctx.measureText(text).width; };
  const TITLE_FONT = '20px Arial', DESC_FONT = '14px Arial', TITLE_MAX = 580, DESC_MAX = 920;
  function truncate(text, font, max) {
    if (px(text, font) <= max) return text;
    const words = text.split(' '); let out = '';
    for (const w of words) { const next = out ? `${out} ${w}` : w; if (px(next + ' ...', font) > max) break; out = next; }
    return (out || text.slice(0, 20)) + ' ...';
  }
  const hostOf = u => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return u || 'example.com'; } };
  const crumbs = u => { try { const x = new URL(u); return [x.hostname, ...x.pathname.split('/').filter(Boolean)].slice(0, 4).join(' › '); } catch { return u; } };

  function serp({ title, description, url, favicon, site }) {
    const t = truncate(title || 'Untitled page', TITLE_FONT, TITLE_MAX);
    const d = truncate(description || 'No meta description — Google will pick text from the page, which may not sell the click.', DESC_FONT, DESC_MAX);
    return `<div class="serp-toggle tabs sub" role="tablist"><button type="button" class="tab" role="tab" aria-selected="true" data-view="desktop">${icon('monitor')}Desktop</button><button type="button" class="tab" role="tab" aria-selected="false" data-view="mobile">${icon('smartphone')}Mobile</button></div>
      <div class="serp" data-view="desktop"><div class="serp-site"><span class="serp-fav">${favicon ? `<img src="${esc(favicon)}" alt="" referrerpolicy="no-referrer" onerror="this.remove()">` : ''}</span><div><span class="serp-name">${esc(site || hostOf(url))}</span><span class="serp-url">${esc(crumbs(url))}</span></div></div>
      <div class="serp-title">${esc(t)}</div><div class="serp-desc">${esc(d)}</div></div>
      <div class="serp-meters"><span>Title: ${Math.round(px(title || '', TITLE_FONT))}px / ${TITLE_MAX}px · ${[...(title || '')].length} chars</span><span>Description: ${Math.round(px(description || '', DESC_FONT))}px / ${DESC_MAX}px · ${[...(description || '')].length} chars</span></div>`;
  }
  function wireSerp(root) {
    root.querySelectorAll('.serp-toggle .tab').forEach(b => b.addEventListener('click', () => {
      root.querySelectorAll('.serp-toggle .tab').forEach(x => x.setAttribute('aria-selected', String(x === b)));
      root.querySelector('.serp').dataset.view = b.dataset.view;
    }));
  }
  function social({ title, description, image, url, site, card }) {
    const img = image ? `<img src="${esc(image)}" alt="" referrerpolicy="no-referrer" onerror="this.parentNode.classList.add('noimg');this.remove()">` : '';
    const domain = hostOf(url);
    return `<div class="social-grid">
      <div class="social fb"><span class="social-label">Facebook · LinkedIn</span><div class="social-img${img ? '' : ' noimg'}">${img}</div><div class="social-body"><small>${esc(domain.toUpperCase())}</small><strong>${esc(title || 'No og:title')}</strong><p>${esc(description || '')}</p></div></div>
      <div class="social x"><span class="social-label">X · ${esc(card || 'summary_large_image')}</span><div class="social-img${img ? '' : ' noimg'}">${img}<span class="x-domain">${esc(domain)}</span></div><div class="social-body"><strong>${esc(title || 'No title')}</strong><small>From ${esc(site || domain)}</small></div></div>
    </div>`;
  }

  // ---------- Analyze ----------
  const recent = store.get('meta:recent', []);
  const paintRecent = () => { $('#recent').innerHTML = recent.length ? `<span class="muted" style="font-size:13px">Recent:</span>` + recent.map(u => `<button type="button" class="chip" data-url="${esc(u)}">${esc(hostOf(u))}</button>`).join('') : ''; };
  paintRecent();
  $('#recent').addEventListener('click', e => { const b = e.target.closest('[data-url]'); if (b) { $('#url').value = b.dataset.url; $('#check-form').requestSubmit(); } });
  const preset = new URLSearchParams(location.search).get('url');
  if (preset) $('#url').value = preset;

  const P = 'PASS', W = 'WARN', F = 'FAIL', I = 'INFO';
  function evaluate(s, finalUrl) {
    const groups = { 'Search basics': [], 'Social sharing': [], 'Content & structure': [], 'Technical': [] };
    const add = (g, label, state, detail, weight, fix = '') => groups[g].push({ label, state, detail, weight, fix });
    const tl = [...s.title].length, dl = [...s.description].length, tpx = px(s.title, TITLE_FONT), dpx = px(s.description, DESC_FONT);
    add('Search basics', 'Title tag', !tl ? F : (tl < 25 || tpx > TITLE_MAX) ? W : P, tl ? `“${s.title}” — ${tl} characters, ${Math.round(tpx)}px.` : 'No title found.', 10,
      !tl ? 'Add a unique, descriptive <title> with your main keyword near the start.' : tl < 25 ? 'Title is short — add your keyword, location or brand.' : tpx > TITLE_MAX ? 'Google will likely truncate this title. Keep it under ~580px (about 55–60 characters).' : '');
    if (s.titleCount > 1) add('Search basics', 'Multiple titles', W, `${s.titleCount} <title> elements found.`, 2, 'Keep exactly one <title> in the <head>.');
    add('Search basics', 'Meta description', !dl ? F : (dl < 70 || dpx > DESC_MAX) ? W : P, dl ? `${dl} characters, ${Math.round(dpx)}px. ${s.description}` : 'No meta description found.', 8,
      !dl ? 'Write a 140–160 character summary that sells the click.' : dl < 70 ? 'Description is short — expand it to roughly 140–160 characters.' : dpx > DESC_MAX ? 'Likely truncated in results. Trim to about 155 characters.' : '');
    if (s.descriptionCount > 1) add('Search basics', 'Duplicate descriptions', W, `${s.descriptionCount} meta descriptions found.`, 2, 'Keep one meta description.');
    const norm = u => { try { const x = new URL(u); return (x.origin + x.pathname).replace(/\/$/, '') + x.search; } catch { return u; } };
    add('Search basics', 'Canonical URL', !s.canonical ? W : (norm(s.canonical) !== norm(finalUrl) ? W : P), s.canonical ? (norm(s.canonical) === norm(finalUrl) ? `Self-referencing: ${s.canonical}` : `Points to a different URL: ${s.canonical}`) : 'No canonical link.', 6,
      !s.canonical ? 'Add <link rel="canonical" href="…"> with the preferred URL to avoid duplicate content.' : norm(s.canonical) !== norm(finalUrl) ? 'Make sure this page is meant to be consolidated into the canonical URL.' : '');
    const robots = `${s.robots} ${s.xRobots}`.toLowerCase();
    const noindex = /noindex|none/.test(robots), blocked = s.robotsTxt?.found && s.robotsTxt.allowed === false;
    add('Search basics', 'Indexable', noindex || blocked ? F : P, noindex ? `Blocked by ${/noindex|none/.test(s.xRobots.toLowerCase()) ? 'X-Robots-Tag header' : 'robots meta tag'}: ${s.robots || s.xRobots}` : blocked ? `robots.txt blocks crawling (${s.robotsTxt.rule}).` : `Allowed to index${s.robots ? ` (robots: ${s.robots})` : ''}.`, 10,
      noindex ? 'Remove noindex if this page should appear in search.' : blocked ? 'Update robots.txt so Google can crawl this URL.' : '');
    const h1 = s.headings.h1;
    add('Search basics', 'H1 heading', h1 === 1 ? P : h1 === 0 ? F : W, h1 ? `${h1} H1: ${s.h1.map(x => `“${x}”`).join(', ')}` : 'No H1 found.', 6, h1 === 0 ? 'Add one H1 that describes the page topic.' : h1 > 1 ? 'Use a single H1; demote the others to H2.' : '');
    add('Search basics', 'Mobile viewport', s.viewport ? P : F, s.viewport || 'No viewport meta tag.', 5, s.viewport ? '' : 'Add <meta name="viewport" content="width=device-width, initial-scale=1">.');
    add('Search basics', 'HTTPS', s.https ? P : F, s.https ? 'Served securely over HTTPS.' : 'Page is served over plain HTTP.', 6, s.https ? '' : 'Install an SSL certificate and redirect HTTP to HTTPS.');
    add('Search basics', 'Language', s.lang ? P : W, s.lang ? `<html lang="${s.lang}">` : 'No lang attribute on <html>.', 3, s.lang ? '' : 'Add lang="en" (or your language) to the <html> tag.');

    const og = s.og, tw = s.twitter;
    add('Social sharing', 'og:title', og['og:title'] ? P : W, og['og:title'] || 'Missing — networks fall back to <title>.', 4, og['og:title'] ? '' : 'Add <meta property="og:title">.');
    add('Social sharing', 'og:description', og['og:description'] ? P : W, og['og:description'] || 'Missing.', 3, og['og:description'] ? '' : 'Add <meta property="og:description">.');
    const absImg = /^https?:\/\//i.test(og['og:image'] || '');
    add('Social sharing', 'og:image', og['og:image'] ? (absImg ? P : W) : F, og['og:image'] || 'Missing — shares will have no image.', 5, !og['og:image'] ? 'Add a 1200×630 image with <meta property="og:image">.' : !absImg ? 'Use an absolute https:// URL for og:image.' : '');
    add('Social sharing', 'og:url & og:type', og['og:url'] && og['og:type'] ? P : W, `url: ${og['og:url'] || '—'} · type: ${og['og:type'] || '—'}`, 2, og['og:url'] && og['og:type'] ? '' : 'Add og:url and og:type (usually "website" or "article").');
    add('Social sharing', 'Twitter card', tw['twitter:card'] ? P : W, tw['twitter:card'] ? `${tw['twitter:card']}${tw['twitter:site'] ? ' · ' + tw['twitter:site'] : ''}` : 'Missing — X shows a small or no preview.', 3, tw['twitter:card'] ? '' : 'Add <meta name="twitter:card" content="summary_large_image">.');

    add('Content & structure', 'Word count', s.words >= 300 ? P : s.words >= 100 ? W : F, `${s.words.toLocaleString()} words of visible text.`, 5, s.words < 300 ? 'Thin content rarely ranks. Expand the page with genuinely useful detail.' : '');
    const img = s.images;
    add('Content & structure', 'Image alt text', !img.total || !img.missingAlt ? P : img.missingAlt / img.total > 0.3 ? F : W, img.total ? `${img.total} images · ${img.missingAlt} missing alt · ${img.emptyAlt} decorative (empty alt).` : 'No images found.', 4, img.missingAlt ? 'Describe meaningful images with alt text; use alt="" only for decorative ones.' : '');
    let skipped = false, prev = 0;
    for (const [lvl] of s.outline) { if (prev && lvl > prev + 1) skipped = true; prev = lvl; }
    add('Content & structure', 'Heading hierarchy', skipped ? W : P, `H1 ${s.headings.h1} · H2 ${s.headings.h2} · H3 ${s.headings.h3} · H4–H6 ${s.headings.h4 + s.headings.h5 + s.headings.h6}${skipped ? ' — some levels are skipped.' : ''}`, 2, skipped ? 'Avoid jumping levels (e.g. H2 → H4) so the outline stays logical.' : '');
    add('Content & structure', 'Links', s.links.internal >= 3 ? P : W, `${s.links.internal} internal · ${s.links.external} external · ${s.links.nofollow} nofollow.`, 2, s.links.internal < 3 ? 'Link to related pages to help users and crawlers.' : '');

    const types = Object.keys(s.schema.types);
    add('Technical', 'Structured data', types.length ? P : W, types.length ? `JSON-LD: ${types.join(', ')}` : s.schema.microdata ? `${s.schema.microdata} microdata items.` : 'No JSON-LD found.', 4, types.length ? '' : 'Add schema.org JSON-LD (Organization, LocalBusiness, Article, Product…) for rich results.');
    if (s.schema.errors) add('Technical', 'JSON-LD syntax', F, `${s.schema.errors} of ${s.schema.blocks} JSON-LD blocks failed to parse.`, 3, 'Fix the JSON syntax so search engines can read your structured data.');
    add('Technical', 'Response time', s.ms < 1000 ? P : s.ms < 2500 ? W : F, `${s.ms.toLocaleString()} ms to fetch the HTML from our server.`, 4, s.ms >= 1000 ? 'Improve server response (caching, a faster host or a CDN).' : '');
    add('Technical', 'HTML size', s.bytes < 500000 ? P : W, `${(s.bytes / 1024).toFixed(0)} KB${s.compressed ? ', compressed in transit' : ', not compressed'}.`, 2, s.bytes >= 500000 ? 'Large HTML slows rendering — trim inline code and markup.' : !s.compressed ? 'Enable gzip or Brotli compression on the server.' : '');
    add('Technical', 'Redirects', s.redirects.length <= 1 ? P : W, s.redirects.length ? s.redirects.map(r => `${r.status} ${r.url}`).join(' → ') + ` → ${finalUrl}` : 'No redirects.', 2, s.redirects.length > 1 ? 'Link directly to the final URL to avoid redirect chains.' : '');
    add('Technical', 'Favicon', s.favicon ? P : W, s.favicon || 'No <link rel="icon"> declared.', 2, s.favicon ? '' : 'Declare a favicon — Google shows it next to your result.');
    const rt = s.robotsTxt || {};
    add('Technical', 'robots.txt', rt.found ? P : W, rt.found ? `Found${rt.sitemaps?.length ? ` · sitemaps: ${rt.sitemaps.join(', ')}` : ' · no Sitemap line'}` : (rt.error || `Not found (HTTP ${rt.status || '—'}).`), 2, !rt.found ? 'Add a robots.txt with a Sitemap: line.' : !rt.sitemaps?.length ? 'Reference your XML sitemap in robots.txt.' : '');
    if (s.hreflang.length) add('Technical', 'hreflang', I, s.hreflang.map(h => `${h.lang}`).join(', '), 0);
    if (s.keywords) add('Technical', 'Meta keywords', I, 'Present — Google ignores this tag, and it reveals your targets to competitors.', 0);
    if (s.charset && !/utf-?8/i.test(s.charset)) add('Technical', 'Character set', W, s.charset, 1, 'Use UTF-8.');

    let total = 0, got = 0; const counts = { PASS: 0, WARN: 0, FAIL: 0 };
    Object.values(groups).flat().forEach(c => { if (c.state === I) return; counts[c.state]++; total += c.weight; got += c.weight * (c.state === P ? 1 : c.state === W ? 0.5 : 0); });
    return { groups, score: total ? Math.round((got / total) * 100) : 0, counts };
  }

  const badge = st => `<span class="badge ${st === 'PASS' ? '' : st === 'WARN' ? 'warn' : st === 'FAIL' ? 'fail' : 'info'}">${st}</span>`;
  const checkRow = c => `<div class="check">${badge(c.state)}<strong>${esc(c.label)}</strong><p>${esc(c.detail)}${c.fix ? `<br><span class="fix">${icon('wand')} ${esc(c.fix)}</span>` : ''}</p></div>`;
  let last = null;

  function renderReport(data) {
    const s = data.seo, ev = evaluate(s, data.url); last = { data, ev };
    const order = { FAIL: 0, WARN: 1, PASS: 2, INFO: 3 };
    const fixes = Object.values(ev.groups).flat().filter(c => c.state === 'FAIL' || c.state === 'WARN').sort((a, b) => order[a.state] - order[b.state] || b.weight - a.weight).slice(0, 6);
    const grade = ev.score >= 90 ? 'Excellent' : ev.score >= 75 ? 'Good' : ev.score >= 55 ? 'Needs work' : 'Poor';
    const color = ev.score >= 75 ? 'var(--ok)' : ev.score >= 55 ? 'var(--warn)' : 'var(--danger)';
    const og = s.og, tw = s.twitter;
    $('#results').innerHTML = `
      <div class="report-head">
        <div class="score-ring" style="--score:${ev.score};--ring:${color}"><div><strong>${ev.score}</strong><span>/100</span></div></div>
        <div class="report-meta"><span class="eyebrow">${esc(grade)} · SEO score</span><h3>${esc(s.title || hostOf(data.url))}</h3>
          <p class="muted">${esc(data.url)}</p>
          <div class="chips"><span class="chip">${icon('check')}${ev.counts.PASS} passed</span><span class="chip" style="color:var(--warn)">${ev.counts.WARN} warnings</span><span class="chip" style="color:var(--danger)">${ev.counts.FAIL} failed</span><span class="chip">${icon('zap')}${s.ms} ms</span><span class="chip">${(s.bytes / 1024).toFixed(0)} KB</span></div></div>
        <div class="toolbar-group">${btn('copy-report', 'Copy report', { icon: 'copy', ghost: true })}${btn('dl-report', 'JSON', { icon: 'download', ghost: true })}</div>
      </div>
      ${fixes.length ? `<div class="card fixes"><h3>${icon('wand')} Top fixes</h3><ol>${fixes.map(f => `<li><span class="badge ${f.state === 'FAIL' ? 'fail' : 'warn'}">${f.state}</span><span><strong>${esc(f.label)}:</strong> ${esc(f.fix || f.detail)}</span></li>`).join('')}</ol></div>` : `<div class="card fixes"><h3>${icon('check')} Nothing urgent — this page covers the on-page essentials.</h3></div>`}
      ${tabBar('rp', [['checks', 'All checks', 'list'], ['previews', 'Previews', 'eye'], ['content', 'Content', 'tree'], ['tags', 'Raw tags', 'code']], 'sub')}
      ${tabPanel('rp', 'checks', Object.entries(ev.groups).map(([g, items]) => `<div class="group-title">${esc(g)}<span>${items.filter(i => i.state === 'PASS').length}/${items.filter(i => i.state !== 'INFO').length}</span></div><div class="checks">${items.map(checkRow).join('')}</div>`).join(''), true)}
      ${tabPanel('rp', 'previews', `<div class="grid-2"><div class="card" id="rp-serp">${serp({ title: s.title, description: s.description, url: data.url, favicon: s.favicon, site: og['og:site_name'] })}</div>
        <div class="card">${social({ title: og['og:title'] || tw['twitter:title'] || s.title, description: og['og:description'] || s.description, image: og['og:image'] || tw['twitter:image'], url: og['og:url'] || data.url, site: og['og:site_name'], card: tw['twitter:card'] })}</div></div>`)}
      ${tabPanel('rp', 'content', `<div class="grid-2"><div class="card"><h3>Heading outline</h3>${s.outline.length ? `<ol class="outline">${s.outline.map(([l, t]) => `<li style="--lvl:${l - 1}"><span class="tag">H${l}</span>${esc(t || '(empty)')}</li>`).join('')}</ol>` : '<p class="muted">No headings found.</p>'}</div>
        <div style="display:grid;gap:14px;align-content:start"><div class="stat-grid"><div class="stat"><strong>${s.words.toLocaleString()}</strong><span>Words</span></div><div class="stat"><strong>${s.images.total}</strong><span>Images</span></div><div class="stat"><strong>${s.links.internal}</strong><span>Internal links</span></div><div class="stat"><strong>${s.links.external}</strong><span>External links</span></div></div>
        ${s.images.missingSamples.length ? `<div class="card"><h3>Images missing alt</h3><ul class="mono-list">${s.images.missingSamples.map(u => `<li>${esc(u)}</li>`).join('')}</ul></div>` : ''}
        <div class="card"><h3>Text excerpt</h3><p class="muted" style="margin:0">${esc(s.excerpt || 'No visible text.')}</p></div></div></div>`)}
      ${tabPanel('rp', 'tags', `<div class="tag-table">${[
        ['title', s.title], ['description', s.description], ['canonical', s.canonical], ['robots', s.robots], ['x-robots-tag', s.xRobots], ['viewport', s.viewport], ['charset', s.charset], ['lang', s.lang], ['theme-color', s.themeColor],
        ...Object.entries(og), ...Object.entries(tw), ['favicon', s.favicon], ['hreflang', s.hreflang.map(h => `${h.lang} → ${h.href}`).join('\n')], ['server', s.server],
      ].map(([k, v]) => `<div><code>${esc(k)}</code><span class="${v ? '' : 'muted'}">${esc(v || 'not set')}</span></div>`).join('')}</div>`)}`;
    tabs($('#rp'));
    wireSerp($('#rp-serp'));
    $('#copy-report').addEventListener('click', () => {
      const lines = [`SEO report for ${data.url}`, `Score: ${ev.score}/100 (${grade}) — ${ev.counts.PASS} passed, ${ev.counts.WARN} warnings, ${ev.counts.FAIL} failed`, ''];
      for (const [g, items] of Object.entries(ev.groups)) { lines.push(g.toUpperCase()); items.forEach(c => lines.push(`[${c.state}] ${c.label}: ${c.detail}${c.fix ? `\n        Fix: ${c.fix}` : ''}`)); lines.push(''); }
      lines.push('Generated with https://jmautida.com/tools/meta-tags-checker');
      copy(lines.join('\n'), 'Report copied');
    });
    $('#dl-report').addEventListener('click', () => download(JSON.stringify({ url: data.url, score: ev.score, checks: ev.groups, raw: s }, null, 2), `seo-report-${hostOf(data.url)}.json`, 'application/json'));
  }

  $('#check-form').addEventListener('submit', async e => {
    e.preventDefault();
    let value = $('#url').value.trim();
    if (value && !/^https?:\/\//i.test(value)) { value = 'https://' + value; $('#url').value = value; }
    let url;
    try { url = new URL(value); if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password) throw 0; }
    catch { status('Enter a valid public URL, such as https://example.com', 'error'); $('#url').focus(); return; }
    const button = $('#check'); button.disabled = true;
    $('#results').innerHTML = `<div class="empty"><div class="loader"></div><h3>Analyzing ${esc(url.hostname)}…</h3><p>Fetching the page, robots.txt and metadata. This usually takes a few seconds.</p></div>`;
    status('Fetching the page…');
    const controller = new AbortController(), timer = setTimeout(() => controller.abort(), 60000);
    try {
      const res = await fetch('/api/check.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url: url.href, mode: 'meta' }), signal: controller.signal });
      if (!(res.headers.get('content-type') || '').includes('application/json')) throw new Error('The checker service is unavailable right now. Please try again later.');
      const data = await res.json();
      if (!res.ok || data.error) throw new Error(data.error || 'The check failed. Please try again.');
      renderReport(data);
      const i = recent.indexOf(url.href); if (i >= 0) recent.splice(i, 1);
      recent.unshift(url.href); recent.length = Math.min(recent.length, 5); store.set('meta:recent', recent); paintRecent();
      status('Analysis complete. Results reflect the server-delivered HTML, not a ranking guarantee.', 'ok');
    } catch (err) {
      $('#results').innerHTML = `<div class="empty"><span class="tool-icon">${icon('x')}</span><h3>The check couldn’t finish.</h3><p>${esc(err.name === 'AbortError' ? 'The website took too long to respond.' : err.message)}</p></div>`;
      status(err.name === 'AbortError' ? 'The website took too long to respond. Try again later.' : err.message, 'error');
    } finally { clearTimeout(timer); button.disabled = false; }
  });

  // ---------- Generator ----------
  const g = id => $('#g-' + id);
  const attr = v => esc(v).replace(/\n/g, ' ');
  function meter(el, value, max) { const pct = Math.min(100, (value / max) * 100); el.querySelector('i').style.width = pct + '%'; el.className = 'meter' + (value > max ? ' bad' : value < max * 0.45 ? ' warn' : ''); }
  const generate = () => {
    const v = Object.fromEntries(['title', 'desc', 'url', 'image', 'site', 'type', 'twitter', 'lang', 'theme', 'robots'].map(k => [k, g(k).value.trim()]));
    const tpx = px(v.title, TITLE_FONT), dpx = px(v.desc, DESC_FONT);
    g('title-count').textContent = `${[...v.title].length} chars · ${Math.round(tpx)}/${TITLE_MAX}px`;
    g('desc-count').textContent = `${[...v.desc].length} chars · ${Math.round(dpx)}/${DESC_MAX}px`;
    meter(g('title-meter'), tpx, TITLE_MAX); meter(g('desc-meter'), dpx, DESC_MAX);
    g('serp').innerHTML = serp({ title: v.title, description: v.desc, url: v.url, site: v.site }); wireSerp(g('serp'));
    g('social').innerHTML = social({ title: v.title, description: v.desc, image: v.image, url: v.url, site: v.site, card: v.image ? 'summary_large_image' : 'summary' });
    const lines = [
      '<!-- Primary meta tags -->', `<title>${attr(v.title)}</title>`, `<meta name="description" content="${attr(v.desc)}">`,
      `<meta name="robots" content="${attr(v.robots)}">`, v.url && `<link rel="canonical" href="${attr(v.url)}">`, '<meta name="viewport" content="width=device-width, initial-scale=1">',
      v.theme && `<meta name="theme-color" content="${attr(v.theme)}">`, '', '<!-- Open Graph / Facebook / LinkedIn -->',
      `<meta property="og:type" content="${attr(v.type)}">`, v.site && `<meta property="og:site_name" content="${attr(v.site)}">`, v.url && `<meta property="og:url" content="${attr(v.url)}">`,
      `<meta property="og:title" content="${attr(v.title)}">`, `<meta property="og:description" content="${attr(v.desc)}">`,
      v.image && `<meta property="og:image" content="${attr(v.image)}">`, v.image && '<meta property="og:image:width" content="1200">', v.image && '<meta property="og:image:height" content="630">',
      v.lang && `<meta property="og:locale" content="${attr(v.lang)}">`, '', '<!-- X (Twitter) -->',
      `<meta name="twitter:card" content="${v.image ? 'summary_large_image' : 'summary'}">`, v.twitter && `<meta name="twitter:site" content="${attr(v.twitter.startsWith('@') ? v.twitter : '@' + v.twitter)}">`,
      `<meta name="twitter:title" content="${attr(v.title)}">`, `<meta name="twitter:description" content="${attr(v.desc)}">`, v.image && `<meta name="twitter:image" content="${attr(v.image)}">`,
    ].filter(x => x !== false && x !== undefined && x !== null && x !== '' || x === '');
    g('code').textContent = lines.join('\n').replace(/\n{3,}/g, '\n\n');
    store.set('meta:gen', v);
  };
  const saved = store.get('meta:gen');
  if (saved) Object.entries(saved).forEach(([k, val]) => { if (g(k)) g(k).value = val; });
  $$('[id^="g-"]').forEach(el => { if (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) el.addEventListener('input', debounce(generate, 120)); });
  g('copy').addEventListener('click', () => copy(g('code').textContent, 'Meta tags copied'));
  generate();
  status('Enter a URL to analyze, or switch to the generator.');
})();
