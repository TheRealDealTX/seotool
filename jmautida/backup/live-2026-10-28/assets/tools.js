'use strict';
(async function () {
  const $ = selector => document.querySelector(selector);
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const status = (message, error = false) => { $('#status').textContent = message; $('#status').classList.toggle('error', error); };
  const download = (value, name, type) => {
    const blob = value instanceof Blob ? value : new Blob([value], {type});
    const url = URL.createObjectURL(blob), a = document.createElement('a');
    a.href = url; a.download = name; a.click(); setTimeout(() => URL.revokeObjectURL(url), 10000);
  };
  const button = (id, text, dark = false) => `<button type="button" id="${id}" class="button ${dark ? 'dark' : 'outline'}">${text}</button>`;
  const pane = (heading, content) => `<section class="editor-pane"><div class="pane-heading">${heading}</div>${content}</section>`;
  const editor = (id, label, light = false, readonly = false) => `<textarea id="${id}" class="editor ${light ? 'light' : ''}" spellcheck="false" aria-label="${label}" maxlength="200000" ${readonly ? 'readonly' : ''}></textarea>`;
  const app = $('#tool-app');
  let catalog;
  try { const res = await fetch('/assets/tools.json?v=3'); catalog = await res.json(); }
  catch { status('The tools could not load. Please reload the page.', true); return; }
  const id = document.body.dataset.tool || new URLSearchParams(location.search).get('tool') || 'html';
  const tool = catalog.find(t => t[0] === id);
  if (!tool) { $('#tool-title').textContent = 'Tool not found'; app.innerHTML = '<p>Please choose a tool from <a href="/tools">the toolbox</a>.</p>'; return; }
  $('#tool-title').textContent = tool[2]; $('#tool-category').textContent = `THE TOOLBOX / ${tool[3].toUpperCase()}`;
  $('#tool-description').textContent = tool[4]; 
  const help = text => $('#help-text').textContent = text;
  const sampleHTML = `<!doctype html>\n<html lang="en">\n<head>\n<meta name="viewport" content="width=device-width, initial-scale=1">\n<style>\n  body { margin: 0; padding: 48px 30px; background: #e8eddd; color: #252a22; font-family: Arial, sans-serif; }\n  .star { font-size: 70px; color: #c9502c; }\n  h1 { font-size: 48px; line-height: 1; letter-spacing: -2px; }\n  p { line-height: 1.6; max-width: 320px; }\n  button { background: #252a22; color: white; border: 0; padding: 14px 20px; border-radius: 4px; cursor: pointer; }\n</style>\n</head>\n<body>\n  <div class="star">✳</div>\n  <h1>Make something good.</h1>\n  <p>A little design. A little code. A lot of possibility.</p>\n  <button onclick="this.textContent='Hello, maker! ✳'">Say hello ↗</button>\n</body>\n</html>`;
  if (id === 'html') {
    app.innerHTML = `<div class="toolbar"><div class="toolbar-group">${button('run','▶ Run code',true)}${button('sample','Load example')}${button('clear','Clear')}</div><div class="toolbar-group"><label for="device">Preview</label><select id="device"><option value="100%">Responsive</option><option value="768px">Tablet · 768px</option><option value="375px">Mobile · 375px</option></select>${button('save','↓ Download HTML')}</div></div><div class="editor-grid">${pane('SOURCE / HTML + CSS + JS',editor('source','HTML source code'))}${pane('LIVE PREVIEW / ISOLATED SANDBOX','<div class="preview-wrap"><iframe id="preview" title="Your HTML design preview" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe></div>')}</div>`;
    const run = () => { $('#preview').srcdoc = $('#source').value; status('Preview updated. JavaScript runs inside an isolated frame.'); };
    $('#source').value = sampleHTML; run();
    $('#run').onclick = run;
    $('#sample').onclick = () => { $('#source').value = sampleHTML; run(); };
    $('#clear').onclick = () => { $('#source').value = ''; run(); $('#source').focus(); };
    $('#device').onchange = () => { $('#preview').style.width = $('#device').value; $('#preview').style.flex = '0 0 ' + $('#device').value; };
    $('#save').onclick = () => download($('#source').value,'playground.html','text/html;charset=utf-8');
    $('#source').addEventListener('keydown', e => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') { e.preventDefault(); run(); } });
    help('Paste a complete HTML document with inline <style> and <script> tags, then choose Run code (Ctrl/⌘ + Enter). The sandbox can run JavaScript, but cannot access this website’s cookies, navigate the parent page, or open pop-ups. External assets may load when referenced by your code. PHP requires a server and cannot run in this preview. Download your code before leaving; it is not saved.');
  }
  // Rebuild Markdown output with a small allowlist. No source attributes, scripts,
  // styles, embedded objects or remote images are copied into the live document.
  function markdownFragment(text) {
    const raw = new DOMParser().parseFromString(marked.parse(text, {gfm:true,breaks:false}), 'text/html');
    const allowed = new Set('P H1 H2 H3 H4 H5 H6 STRONG EM B I S DEL CODE PRE BLOCKQUOTE UL OL LI TABLE THEAD TBODY TR TD TH HR BR A'.split(' '));
    function clean(node) {
      if (node.nodeType === Node.TEXT_NODE) return document.createTextNode(node.textContent);
      if (node.nodeType !== Node.ELEMENT_NODE) return document.createTextNode('');
      if (node.tagName === 'IMG') return document.createTextNode(`[Image: ${node.getAttribute('alt') || 'omitted'}]`);
      if (!allowed.has(node.tagName)) return document.createTextNode(node.textContent || '');
      const el = document.createElement(node.tagName.toLowerCase());
      if (node.tagName === 'A') {
        const href = node.getAttribute('href') || '';
        if (/^(https?:\/\/|mailto:)/i.test(href.trim())) { el.setAttribute('href',href.trim()); el.setAttribute('target','_blank'); el.setAttribute('rel','noopener noreferrer'); }
      }
      if (node.tagName === 'OL' && /^\d{1,6}$/.test(node.getAttribute('start') || '')) el.setAttribute('start',node.getAttribute('start'));
      node.childNodes.forEach(child => el.append(clean(child)));
      return el;
    }
    const fragment = document.createDocumentFragment(); raw.body.childNodes.forEach(n => fragment.append(clean(n))); return fragment;
  }
  if (id === 'markdown') {
    if (!window.marked || !window.docx) { status('Document libraries did not load. Please reload the page.',true); return; }
    app.innerHTML = `<div class="toolbar"><div class="toolbar-group">${button('import','↑ Import .md')}${button('sample','Load example')}${button('clear','Clear')}<input type="file" id="file" accept=".md,.markdown,.txt,text/plain,text/markdown" hidden></div><div class="toolbar-group">${button('save-md','↓ Markdown')}${button('export','↓ Export Word',true)}</div></div><div class="editor-grid">${pane('MARKDOWN / EDITOR',editor('source','Markdown source'))}${pane('DOCUMENT / PREVIEW','<div class="document-preview" id="document"></div>')}</div>`;
    const sample = '# A little idea, ready to grow\n\nA project brief by **John Raymond Autida**.\n\n## The idea\n\nBuild something useful, keep it simple, and make every detail count.\n\n### The plan\n\n1. Start with a clear purpose.\n2. Design around the people using it.\n3. Build, test, and make it better.\n\n> Good tools get out of the way of good work.\n\n## A simple checklist\n\n- Thoughtful design\n- Responsive layouts\n- Accessible interactions\n\n| Stage | Deliverable |\n| --- | --- |\n| Design | A clear direction |\n| Build | A working website |\n\nVisit [the toolbox](https://jmautida.com/tools) for more.';
    const render = () => { try { $('#document').replaceChildren(markdownFragment($('#source').value)); status('Preview updated. Ready to export as .docx.'); } catch { status('Could not render this document.',true); } };
    $('#source').value = sample; render();
    let timer; $('#source').addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(render,150); });
    $('#clear').onclick = () => { $('#source').value = ''; render(); };
    $('#sample').onclick = () => { $('#source').value = sample; render(); };
    $('#import').onclick = () => $('#file').click();
    $('#file').onchange = async () => {
      const file = $('#file').files[0]; if (!file) return;
      if (file.size > 200000) { status('Please choose a Markdown file smaller than 200 KB.',true); return; }
      try { $('#source').value = await file.text(); render(); } catch { status('This file could not be read.',true); }
      $('#file').value = '';
    };
    $('#save-md').onclick = () => download($('#source').value,'document.md','text/markdown;charset=utf-8');
    $('#export').onclick = async () => {
      render(); $('#export').disabled = true;
      try {
        const {Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType, ExternalHyperlink} = docx;
        function runs(node, opts = {}) {
          if (node.nodeType === Node.TEXT_NODE) return [new TextRun({...opts,text:node.textContent})];
          if (node.nodeType !== Node.ELEMENT_NODE) return [];
          const tag = node.tagName;
          if (tag === 'BR') return [new TextRun({...opts,break:1})];
          const style = {...opts,...(['STRONG','B','TH'].includes(tag) ? {bold:true} : {}),...(['EM','I'].includes(tag) ? {italics:true} : {}),...(['DEL','S'].includes(tag) ? {strike:true} : {}),...(tag === 'CODE' ? {font:'Consolas',size:20} : {})};
          const children = [...node.childNodes].flatMap(n => runs(n,style));
          if (tag === 'A' && node.hasAttribute('href')) return [new ExternalHyperlink({link:node.getAttribute('href'),children})];
          return children;
        }
        function blocks(container, depth = 0) {
          return [...container.childNodes].flatMap(node => {
            if (node.nodeType === Node.TEXT_NODE) return node.textContent.trim() ? [new Paragraph({children:runs(node)})] : [];
            if (node.nodeType !== Node.ELEMENT_NODE) return [];
            const tag = node.tagName;
            if (tag === 'UL' || tag === 'OL') {
              let index = Number(node.getAttribute('start') || 1);
              return [...node.children].flatMap(li => {
                const inline = [...li.childNodes].filter(n => !['UL','OL'].includes(n.tagName)).flatMap(n => runs(n));
                const para = new Paragraph({children:tag === 'OL' ? [new TextRun(`${index++}. `),...inline] : inline,...(tag === 'UL' ? {bullet:{level:Math.min(depth,8)}} : {indent:{left:360*(depth+1)}}),spacing:{after:100}});
                return [para,...[...li.children].filter(n => ['UL','OL'].includes(n.tagName)).flatMap(n => { const holder = document.createElement('div'); holder.append(n.cloneNode(true)); return blocks(holder,depth+1); })];
              });
            }
            if (tag === 'TABLE') return [new Table({width:{size:100,type:WidthType.PERCENTAGE},rows:[...node.querySelectorAll('tr')].map(row => new TableRow({children:[...row.children].map(cell => new TableCell({children:[new Paragraph({children:runs(cell)})]}))}))})];
            if (tag === 'BLOCKQUOTE') return [new Paragraph({children:runs(node,{italics:true}),indent:{left:480},spacing:{after:180}})];
            if (tag === 'PRE') return node.textContent.replace(/\n$/,'').split('\n').map(line => new Paragraph({children:[new TextRun({text:line,font:'Consolas',size:20})]}));
            if (tag === 'HR') return [new Paragraph({text:'────────────────────────',spacing:{after:160}})];
            return [new Paragraph({children:runs(node),...(/^H[1-6]$/.test(tag) ? {heading:HeadingLevel['HEADING_'+tag[1]]} : {}),spacing:{after:180}})];
          });
        }
        const children = blocks($('#document'));
        const documentFile = new Document({creator:'JM Autida Toolbox',title:$('#document h1')?.textContent || 'Document',styles:{default:{document:{run:{font:'Calibri',size:22}}}},sections:[{children:children.length ? children : [new Paragraph('')]}]});
        download(await Packer.toBlob(documentFile),'document.docx'); status('Your Word document is ready. Download started.');
      } catch (error) { status('Word export failed. Try a smaller document or download your Markdown instead.',true); }
      finally { $('#export').disabled = false; }
    };
    help('Supports headings, bold and italic text, links, lists, blockquotes, fenced code and tables. Export creates a real .docx document. Raw HTML styling is not supported; images are represented by their alt text rather than downloaded. Complex nested formatting may differ in Word. Inputs stay in this browser and are cleared when you leave.');
  }
  if (id === 'meta' || id === 'favicon') {
    $('#tool-privacy').textContent = '◈ Checks a public website';
    app.innerHTML = `<form class="url-form" id="check-form"><label for="url">Website URL<input id="url" type="url" placeholder="https://example.com" required maxlength="2048" autocomplete="url"></label><button class="button dark" id="check">Check ${id === 'meta' ? 'meta tags' : 'favicons'} ↗</button></form><div id="results" aria-live="polite"><div class="empty-results"><span class="tool-icon">${tool[1]}</span><h2>Let’s check the details.</h2><p>Enter a public website URL to see a practical, item-by-item report.</p></div></div>`;
    const check = (label, state, detail) => `<div class="check"><div class="check-label"><span class="badge ${state === 'PASS' ? '' : state === 'NOTE' ? 'warn' : 'fail'}">${state}</span>${escape(label)}</div><p>${escape(detail)}</p></div>`;
    $('#check-form').onsubmit = async event => {
      event.preventDefault();
      let url; try { url = new URL($('#url').value.trim()); if (!['http:','https:'].includes(url.protocol) || url.username || url.password) throw Error(); }
      catch { status('Enter a valid public HTTP or HTTPS URL without credentials.',true); return; }
      $('#check').disabled = true; $('#results').setAttribute('aria-busy','true'); status('Checking the website. This may take up to 45 seconds…');
      const controller = new AbortController(), timeout = setTimeout(() => controller.abort(),50000);
      try {
        const response = await fetch('/api/check.php',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:url.href,mode:id}),signal:controller.signal});
        if (!(response.headers.get('content-type') || '').includes('application/json')) throw new Error('Website checks require PHP hosting. Upload the package to Hostinger with PHP 8.2+ and cURL/DOM enabled.');
        const data = await response.json(); if (!response.ok || data.error) throw new Error(data.error || 'The check failed. Please try again.');
        let html = `<div class="result-summary"><h2>${id === 'meta' ? 'Your metadata, at a glance.' : 'The small things, checked.'}</h2><p>${escape(data.url)} · HTTP ${escape(data.status)} · Server-rendered HTML</p></div>`;
        html += '<div class="checks">'+data.checks.map(c => check(c.label,c.state,c.detail)).join('')+'</div>';
        if (id === 'meta') html += `<div class="search-preview"><span class="eyebrow">ILLUSTRATIVE SEARCH PREVIEW</span><p>${escape(new URL(data.url).hostname)}</p><div class="search-title">${escape(data.title || 'No page title found')}</div><p>${escape(data.description || 'No meta description found.')}</p></div>`;
        $('#results').innerHTML = html; status('Check complete. Results describe what the server could fetch, not a search ranking score.');
      } catch (error) { $('#results').innerHTML = '<div class="empty-results"><h2>The check could not finish.</h2><p>Review the message below, then try again.</p></div>'; status(error.name === 'AbortError' ? 'The website took too long to respond. Try again later.' : error.message,true); }
      finally { clearTimeout(timeout); $('#check').disabled = false; $('#results').removeAttribute('aria-busy'); }
    };
    help(id === 'meta' ? 'Checks server-rendered HTML for title, description, canonical URL, robots, Open Graph and Twitter tags. JavaScript-injected tags will not appear. Length recommendations are guidelines, not ranking guarantees. Sites may block automated requests. Only public HTTP/HTTPS addresses on standard ports are supported.' : 'Checks declared icons, the conventional /favicon.ico fallback, Apple touch icons and a linked manifest with up to three manifest icons. Reachability and content types are checked; visual quality and image dimensions are not decoded. Requests are bounded to keep checks fast. Browser caching can still affect which favicon you see.');
  }
  if (id === 'json') {
    app.innerHTML = `<div class="toolbar"><div class="toolbar-group">${button('format','Format JSON',true)}${button('minify','Minify')}${button('clear','Clear')}</div><div class="toolbar-group">${button('copy','Copy output')}${button('save','↓ Download')}</div></div><div class="editor-grid">${pane('JSON / INPUT',editor('source','JSON input'))}${pane('FORMATTED / OUTPUT',editor('output','JSON output',true,true))}</div>`;
    $('#source').value = '{"hello":"maker","tools":["build","write","inspect"],"ready":true}';
    const format = spaces => { try { $('#output').value = JSON.stringify(JSON.parse($('#source').value),null,spaces); status('Valid JSON. Output updated.'); } catch (error) { $('#output').value = ''; status('Invalid JSON: '+error.message,true); } };
    $('#format').onclick = () => format(2); $('#minify').onclick = () => format(0); format(2);
    $('#clear').onclick = () => { $('#source').value = ''; $('#output').value = ''; status('Cleared.'); };
    $('#copy').onclick = async () => { try { await navigator.clipboard.writeText($('#output').value); status('Copied to clipboard.'); } catch { $('#output').select(); status('Select the output and use Ctrl/⌘ + C to copy.'); } };
    $('#save').onclick = () => { if (!$('#output').value) return status('Format valid JSON before downloading.',true); download($('#output').value,'formatted.json','application/json'); };
    $('#source').oninput = () => { $('#output').value=''; status('Input changed. Choose Format or Minify to update the output.'); };
    help('Uses the browser’s JSON parser. Comments, trailing commas and unquoted keys are not valid JSON. Very large integers may lose precision; represent identifiers as strings. JSON is never uploaded.');
  }
  if (id === 'contrast') {
    app.innerHTML = `<div class="contrast-grid"><div class="color-controls"><label for="foreground">Text color</label><div class="color-row"><input type="color" id="foreground-picker" value="#242822" aria-label="Choose text color"><input type="text" id="foreground" value="#242822" maxlength="7" spellcheck="false"></div><label for="background">Background color</label><div class="color-row"><input type="color" id="background-picker" value="#f5f4ef" aria-label="Choose background color"><input type="text" id="background" value="#f5f4ef" maxlength="7" spellcheck="false"></div><div class="ratio" id="ratio"></div><span class="eyebrow">CONTRAST RATIO</span><div style="margin-top:25px">${button('swap','⇄ Swap colors')}</div></div><div class="contrast-preview" id="color-preview"><span class="eyebrow">A LITTLE PREVIEW</span><h2>Good design<br>includes everyone.</h2><p>This is normal-sized text. A readable color combination makes your message easier to understand.</p><strong>Make every word count.</strong></div></div><div class="checks results" id="contrast-results"></div>`;
    const luminance = hex => {
      const rgb = hex.match(/[a-f\d]{2}/gi).map(x => parseInt(x,16)/255).map(x => x <= .04045 ? x/12.92 : ((x+.055)/1.055)**2.4);
      return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;
    };
    const update = () => {
      const colors = ['foreground','background'].map(k => $('#'+k).value.trim());
      if (colors.some(c => !/^#[\da-f]{6}$/i.test(c))) { status('Use six-digit hex colors, such as #242822.',true); return; }
      ['foreground','background'].forEach((k,i) => $('#'+k+'-picker').value = colors[i]);
      const l = colors.map(luminance); const ratio = (Math.max(...l)+.05)/(Math.min(...l)+.05);
      $('#ratio').textContent = ratio.toFixed(2)+':1'; $('#color-preview').style.color = colors[0]; $('#color-preview').style.background = colors[1];
      $('#contrast-results').innerHTML = [['AA · Normal text',4.5],['AA · Large text',3],['AAA · Normal text',7],['AAA · Large text',4.5]].map(([name,limit]) => `<div class="check"><div class="check-label"><span class="badge ${ratio>=limit?'':'fail'}">${ratio>=limit?'PASS':'FAIL'}</span>${name}</div><p>Requires at least ${limit}:1 contrast.</p></div>`).join(''); status('Contrast calculated using WCAG relative luminance.');
    };
    ['foreground','background'].forEach(k => { $('#'+k).oninput = update; $('#'+k+'-picker').oninput = () => { $('#'+k).value = $('#'+k+'-picker').value; update(); }; });
    $('#swap').onclick = () => { const old = $('#foreground').value; $('#foreground').value = $('#background').value; $('#background').value = old; update(); }; update();
    help('WCAG 2.x defines large text as at least 18pt (24px), or 14pt (about 18.7px) bold. These results apply to opaque text and solid backgrounds. A passing color pair alone does not guarantee an accessible page. Ratios are compared before rounding.');
  }
  if (id === 'encode') {
    app.innerHTML = `<div class="toolbar"><div class="toolbar-group">${button('encode','Encode →',true)}${button('decode','Decode →')}${button('clear','Clear')}</div><div class="toolbar-group">${button('use','Use output as input')}${button('copy','Copy output')}</div></div><div class="editor-grid">${pane('TEXT / INPUT',editor('source','Text to encode or decode',true))}${pane('RESULT / OUTPUT',editor('output','Encoded or decoded result',true,true))}</div>`;
    $('#source').value = 'Hello, maker! A little idea & a lot of care.';
    const convert = fn => { try { $('#output').value = fn($('#source').value); status('Converted successfully.'); } catch { $('#output').value = ''; status('This input contains malformed percent encoding or invalid Unicode.',true); } };
    $('#encode').onclick = () => convert(encodeURIComponent); $('#decode').onclick = () => convert(decodeURIComponent);
    $('#clear').onclick = () => { $('#source').value=''; $('#output').value=''; status('Cleared.'); };
    $('#use').onclick = () => { $('#source').value=$('#output').value; $('#output').value=''; status('Output moved to input.'); };
    $('#source').oninput = () => { $('#output').value=''; status('Choose Encode or Decode to convert the input.'); };
    $('#copy').onclick = async () => { try { await navigator.clipboard.writeText($('#output').value); status('Copied to clipboard.'); } catch { $('#output').select(); status('Select the output and use Ctrl/⌘ + C to copy.'); } }; convert(encodeURIComponent);
    help('Encodes a URL component with encodeURIComponent, not an entire URL. A space becomes %20. Decoding preserves literal + characters; form-style plus-to-space conversion is not applied.');
  }
  if (id === 'time') {
    app.innerHTML = `<div class="time-layout"><section class="time-inputs"><h2>Plan your working hours.</h2><p>Edit target hours to calculate logout, or edit logout to calculate paid hours.</p><label for="start-time">Start time<input id="start-time" type="time" value="19:30" required></label><label for="target-hours">Target paid hours <span class="muted">(decimal)</span><input id="target-hours" type="number" min="0" max="168" step="any" value="9.3" inputmode="decimal" required aria-describedby="target-hint"></label><p class="muted" id="target-hint">9.3 hours means 9 hours and 18 minutes.</p><div class="break-heading"><h3>Unpaid breaks</h3>${button('add-break','+ Add break')}</div><p class="muted">Enter each break’s duration in minutes. Breaks do not count toward paid hours.</p><div id="breaks"></div><p class="calculation-mode" id="calculation-mode" role="status"></p></section><section class="time-result"><label class="eyebrow" for="logout-time">LOGOUT TIME — EDIT TO RECALCULATE HOURS</label><input id="logout-time" class="logout-input" type="time" required aria-describedby="logout-hint"><label class="day-label" for="logout-day">Logout day</label><select id="logout-day"><option value="auto">Automatic · same day or overnight</option>${Array.from({length:15},(_,d)=>`<option value="${d}">${d===0?'Same day':d===1?'Next day':d+' days later'}</option>`).join('')}</select><p class="muted" id="logout-hint">Choose “Next day” when your shift crosses midnight.</p><div class="time-summary" aria-live="polite" aria-atomic="true"><div id="finish-time" class="finish-time"></div><p id="finish-day"></p><div class="time-breakdown"><div><span>Paid working time</span><strong id="paid-duration"></strong></div><div><span>Unpaid breaks</span><strong id="break-duration"></strong></div><div><span>Total elapsed time</span><strong id="elapsed-duration"></strong></div></div><div class="decimal-explainer"><span class="eyebrow">DECIMAL HOURS, MADE CLEAR</span><h3 id="decimal-equation"></h3><p id="decimal-detail"></p></div></div></section></div>`;
    let sequence = 0, anchor = 'target';
    const duration = minutes => `${Math.floor(minutes/60)}h ${minutes%60}m`;
    const update = () => {
      $('#calculation-mode').textContent = anchor === 'target' ? 'Keeping target hours fixed. Start and break changes update logout.' : 'Keeping logout fixed. Start and break changes update paid hours.';
      try {
        const breaks = [...document.querySelectorAll('.break-minutes')].map(input=>input.value);
        const result = anchor === 'target' ? JMTime.fromTarget($('#start-time').value,$('#target-hours').value,breaks) : JMTime.fromFinish($('#start-time').value,$('#logout-time').value,$('#logout-day').value,breaks);
        const {paid,unpaid,elapsed,day,minute,hours,rounded} = result;
        const h=Math.floor(minute/60), m=minute%60;
        if (anchor === 'target') {
          $('#logout-time').value = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;
          $('#logout-day').value = String(day);
        } else $('#target-hours').value = String(hours);
        $('#finish-time').textContent = `${h%12||12}:${String(m).padStart(2,'0')} ${h>=12?'PM':'AM'}`;
        $('#finish-day').textContent = day===0?'Same day':day===1?'Next day':`${day} days later`;
        $('#paid-duration').textContent=duration(paid); $('#break-duration').textContent=duration(unpaid); $('#elapsed-duration').textContent=duration(elapsed);
        $('#decimal-equation').textContent = `${hours} hours = ${duration(paid)}`;
        const fraction=Number((hours-Math.floor(hours)).toFixed(6));
        const fractionMinutes=Number((fraction*60).toFixed(4));
        $('#decimal-detail').textContent = `${fraction} × 60 ${anchor==='finish' && Math.abs(fractionMinutes-paid%60)>0.000001?'≈':'='} ${anchor==='finish'?paid%60:fractionMinutes} minutes. ${rounded?'Paid time is rounded to the nearest minute.':anchor==='finish'?'Decimal hours are displayed to six decimal places; durations use exact whole minutes.':'The decimal part is a fraction of an hour, not a minute count.'}`;
        status(anchor==='target'?'Logout updated from your target hours and unpaid breaks.':'Target hours updated: elapsed time minus unpaid breaks.');
      } catch (error) {
        ['finish-time','paid-duration','break-duration','elapsed-duration','decimal-equation'].forEach(k=>$('#'+k).textContent='—');
        $('#finish-day').textContent='Check the inputs to calculate your shift.'; $('#decimal-detail').textContent='';
        if (anchor==='finish') $('#target-hours').value='';
        status(error.message,true);
      }
    };
    $('#target-hours').oninput=()=>{anchor='target';update();};
    $('#logout-time').oninput=()=>{anchor='finish';update();};
    $('#logout-day').onchange=()=>{anchor='finish';update();};
    $('#start-time').oninput=update;
    $('#add-break').onclick=()=>{
      const n=++sequence, row=document.createElement('div'); row.className='break-row';
      row.innerHTML=`<label for="break-${n}">Break ${n} <span class="muted">(minutes)</span><input class="break-minutes" id="break-${n}" type="number" min="0" max="10080" step="1" value="30" inputmode="numeric"></label><button type="button" class="button outline" aria-label="Remove break ${n}">Remove</button>`;
      row.querySelector('input').oninput=update;
      row.querySelector('button').onclick=()=>{row.remove();update();$('#add-break').focus();};
      $('#breaks').append(row); update(); row.querySelector('input').focus();
    };
    update();
    help('Editing target hours fixes the paid duration; editing logout time or day fixes the finish. Start and break changes keep whichever you edited last. For example, 7:30 PM plus 9.3 hours ends at 4:48 AM next day; a 30-minute break moves this to 5:18 AM. With 5:18 AM fixed, another 30-minute break reduces paid time to 8.8 hours. Decimal hours multiply by 60. Calculations use whole minutes and wall-clock times, without dates, time zones, daylight-saving changes or payroll-specific rounding.');
  }

  if (id === 'words') {
    app.innerHTML = `<div class="toolbar"><span class="eyebrow">YOUR WORDS, AT A GLANCE</span><div class="toolbar-group">${button('clear','Clear')}${button('save','↓ Download text')}</div></div>${editor('source','Text to count',true)}<div class="stats" aria-live="polite"><div class="stat"><strong id="words">0</strong><span>WORDS</span></div><div class="stat"><strong id="characters">0</strong><span>CHARACTERS</span></div><div class="stat"><strong id="paragraphs">0</strong><span>PARAGRAPHS</span></div><div class="stat"><strong id="minutes">0 min</strong><span>READING TIME</span></div></div>`;
    const count = () => {
      const text = $('#source').value, trimmed = text.trim();
      const words = typeof Intl.Segmenter === 'function' ? [...new Intl.Segmenter(undefined,{granularity:'word'}).segment(text)].filter(s=>s.isWordLike).length : (trimmed.match(/[\p{L}\p{N}]+(?:['’-][\p{L}\p{N}]+)*/gu)||[]).length;
      $('#words').textContent = words.toLocaleString(); $('#characters').textContent = [...text].length.toLocaleString(); $('#paragraphs').textContent = trimmed ? trimmed.split(/\n\s*\n/).length : 0; $('#minutes').textContent = (words ? Math.max(1,Math.ceil(words/200)) : 0)+' min'; status('Counts update as you type.');
    };
    $('#source').value = 'Good things start with a little curiosity.\n\nWrite something here and make every word count.'; $('#source').oninput = count; count();
    $('#clear').onclick = () => { $('#source').value=''; count(); }; $('#save').onclick = () => download($('#source').value,'writing.txt','text/plain;charset=utf-8');
    help('Word counts use the browser’s language-aware word segmentation when available. Characters include spaces and line breaks and are counted as Unicode code points. Paragraphs are separated by blank lines. Reading time is estimated at 200 words per minute.');
  }
})();
