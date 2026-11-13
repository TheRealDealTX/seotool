/* stormclaims.org upload form. Talks to the Rise Document Portal Apps Script
   through its doPost JSON entry point: config -> start -> upload (per file)
   -> finish. If the script has no doPost yet, falls back to the old page. */
(function () {
  'use strict';
  var API = document.body.getAttribute('data-api');
  var CATS = [
    { key: 'policy', title: 'Policy & declarations page', hint: 'Policy, dec page, endorsements', accept: '.pdf,image/*,.doc,.docx' },
    { key: 'carrier', title: 'Carrier letters & estimates', hint: 'Insurance estimate, denial/payment letters, emails. Drop the carrier estimate here and we fill in the claim details.', accept: '.pdf,image/*,.doc,.docx,.esx,.txt', parse: true },
    { key: 'contractor', title: 'Your estimate & measurements', hint: 'Contractor estimate, EagleView/Hover reports, invoices', accept: '.pdf,image/*,.xlsx,.xls,.csv,.doc,.docx,.esx', parse: true },
    { key: 'photos', title: 'Photos & videos', hint: 'Damage photos, inspection photos, short videos', accept: 'image/*,video/*,.heic,.zip' },
    { key: 'signed', title: 'Signed contract / LOR', hint: 'Signed PA contract, letter of representation', accept: '.pdf,image/*' },
    { key: 'other', title: 'Other', hint: 'Anything else for this claim', accept: '' }
  ];
  var REMEMBER = ['company', 'repName', 'repEmail', 'repPhone'];
  var FILL_FIELDS = ['insuredName', 'insuredPhone', 'insuredEmail', 'street', 'city', 'state', 'zip', 'carrier', 'claimNumber', 'policyNumber', 'dateOfLoss', 'lossType'];
  var LABELS = { insuredName: 'homeowner name', insuredPhone: 'homeowner phone', insuredEmail: 'homeowner email', street: 'street', city: 'city', state: 'state', zip: 'ZIP', carrier: 'insurance company', claimNumber: 'claim #', policyNumber: 'policy #', dateOfLoss: 'date of loss', lossType: 'type of loss' };

  var MAX_MB = 25, queue = {}, busy = false, parsedFiles = {};

  function $(id) { return document.getElementById(id); }
  function fmt(b) { return b > 1048576 ? (b / 1048576).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1024)) + ' KB'; }
  function store(k, v) { try { localStorage.setItem('rise_portal_' + k, v); } catch (e) {} }
  function recall(k) { try { return localStorage.getItem('rise_portal_' + k) || ''; } catch (e) { return ''; } }

  function api(body) {
    return fetch(API, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(body), redirect: 'follow' })
      .then(function (r) { return r.text(); })
      .then(function (txt) {
        var j; try { j = JSON.parse(txt); } catch (e) { throw new Error('The upload service gave an unexpected reply. Please try again.'); }
        if (!j.ok) throw new Error(j.error || 'Something went wrong.');
        return j;
      });
  }

  // ---- boot: check the backend, otherwise fall back to the old page ----
  function fallback() {
    $('loading').innerHTML = '<p>Opening the upload tool… <a href="' + API + '">Tap here if it doesn\'t open.</a></p>';
    location.replace(API);
  }
  api({ action: 'config' }).then(function (cfg) {
    MAX_MB = cfg.maxFileMb || 25;
    if (cfg.requireCode) $('codeWrap').classList.remove('hidden');
    $('maxNote').textContent = 'Up to ' + MAX_MB + ' MB per file.';
    $('loading').classList.add('hidden');
    $('formView').classList.remove('hidden');
  }).catch(fallback);

  // ---- remembered contact info ----
  REMEMBER.forEach(function (k) { var v = recall(k); if (v && $(k)) $(k).value = v; });

  // ---- category boxes ----
  var catsEl = $('cats');
  CATS.forEach(function (c) {
    queue[c.key] = [];
    var box = document.createElement('div');
    box.className = 'cat' + (c.parse ? ' cat-parse' : '');
    box.innerHTML = '<div class="cat-head"><div><div class="cat-title"></div><div class="cat-hint"></div></div>' +
      '<button type="button" class="btn btn-ghost btn-add">+ Add files</button></div>' +
      '<input type="file" multiple class="hidden"><ul class="files"></ul>';
    box.querySelector('.cat-title').textContent = c.title;
    box.querySelector('.cat-hint').textContent = c.hint;
    var input = box.querySelector('input');
    if (c.accept) input.setAttribute('accept', c.accept);
    var list = box.querySelector('.files');
    box.querySelector('.btn-add').addEventListener('click', function () { if (!busy) input.click(); });
    input.addEventListener('change', function () { addFiles(c, input.files, list); input.value = ''; });
    ['dragenter', 'dragover'].forEach(function (ev) { box.addEventListener(ev, function (e) { e.preventDefault(); if (!busy) box.classList.add('drag'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { box.addEventListener(ev, function (e) { e.preventDefault(); box.classList.remove('drag'); }); });
    box.addEventListener('drop', function (e) { if (!busy && e.dataTransfer) addFiles(c, e.dataTransfer.files, list); });
    catsEl.appendChild(box);
  });

  // The "fast fill" drop zone adds to the carrier category and parses.
  var fast = $('fastfill'), fastInput = $('fastfillInput');
  fast.addEventListener('click', function (e) { if (e.target.tagName !== 'INPUT' && !busy) fastInput.click(); });
  fastInput.addEventListener('change', function () { addFiles(CATS[1], fastInput.files, catsEl.children[1].querySelector('.files')); fastInput.value = ''; });
  ['dragenter', 'dragover'].forEach(function (ev) { fast.addEventListener(ev, function (e) { e.preventDefault(); fast.classList.add('drag'); }); });
  ['dragleave', 'drop'].forEach(function (ev) { fast.addEventListener(ev, function (e) { e.preventDefault(); fast.classList.remove('drag'); }); });
  fast.addEventListener('drop', function (e) { if (!busy && e.dataTransfer) addFiles(CATS[1], e.dataTransfer.files, catsEl.children[1].querySelector('.files')); });

  function addFiles(cat, files, list) {
    Array.prototype.forEach.call(files || [], function (file) {
      var item = { file: file, status: 'ready' };
      var li = document.createElement('li');
      var nm = document.createElement('span'); nm.className = 'nm'; nm.textContent = file.name;
      var sz = document.createElement('span'); sz.className = 'sz'; sz.textContent = fmt(file.size);
      var st = document.createElement('span'); st.className = 'st';
      var x = document.createElement('button'); x.type = 'button'; x.className = 'x'; x.setAttribute('aria-label', 'Remove'); x.textContent = '×';
      if (file.size > MAX_MB * 1048576) { item.status = 'toolarge'; st.className = 'st err'; st.textContent = 'Over ' + MAX_MB + ' MB'; }
      x.addEventListener('click', function () {
        if (busy) return;
        queue[cat.key] = queue[cat.key].filter(function (i) { return i !== item; });
        li.remove(); updateSummary();
      });
      li.appendChild(nm); li.appendChild(sz); li.appendChild(st); li.appendChild(x);
      item.el = li; item.stEl = st;
      list.appendChild(li);
      queue[cat.key].push(item);
      if (cat.parse && isPdf(file) && item.status === 'ready') maybeAutofill(file, st);
    });
    updateSummary();
  }

  function isPdf(file) { return /\.pdf$/i.test(file.name) || file.type === 'application/pdf'; }

  // ---- autofill from an estimate PDF ----
  function maybeAutofill(file, stEl) {
    var sig = file.name + ':' + file.size;
    if (parsedFiles[sig]) return;
    parsedFiles[sig] = true;
    stEl.className = 'st up'; stEl.textContent = 'Reading…';
    PdfText.lines(file, 3).then(function (lines) {
      var res = ScopeParser.parse(lines.join('\n'));
      var filled = applyFields(res.fields);
      stEl.className = 'st'; stEl.textContent = '';
      if (filled.length) {
        showFill('Filled ' + filled.length + ' field' + (filled.length > 1 ? 's' : '') + ' from ' + file.name + ': ' +
          filled.map(function (k) { return LABELS[k]; }).join(', ') + '. Please double-check them.');
      } else if (!lines.length) {
        showFill('Couldn\'t read text from ' + file.name + ' (it may be a scanned image). The file is still attached; please type the claim details.', true);
      } else {
        showFill('No claim details were found in ' + file.name + '. The file is still attached.', true);
      }
    }).catch(function () {
      stEl.className = 'st'; stEl.textContent = '';
      showFill('Couldn\'t read ' + file.name + ' automatically. The file is still attached; please type the claim details.', true);
    });
  }

  function applyFields(fields) {
    var filled = [];
    FILL_FIELDS.forEach(function (k) {
      var el = $(k), v = fields[k];
      if (!el || !v) return;
      var current = el.value.trim();
      if (current && !(k === 'state' && current === 'TX' && !el.dataset.touched)) return;   // never overwrite what was typed
      if (el.tagName === 'SELECT') {
        var ok = Array.prototype.some.call(el.options, function (o) { return o.value === v || o.text === v; });
        if (!ok) return;
      }
      el.value = v;
      el.classList.add('autofilled');
      filled.push(k);
    });
    return filled;
  }
  FILL_FIELDS.forEach(function (k) {
    var el = $(k); if (!el) return;
    el.addEventListener('input', function () { el.dataset.touched = '1'; el.classList.remove('autofilled'); });
    el.addEventListener('change', function () { el.dataset.touched = '1'; el.classList.remove('autofilled'); });
  });

  function showFill(msg, warn) {
    var el = $('fillMsg'); el.textContent = msg; el.className = 'fill-msg' + (warn ? ' warn' : ' ok');
  }

  function allItems() {
    var out = [];
    CATS.forEach(function (c) { queue[c.key].forEach(function (i) { out.push({ key: c.key, item: i }); }); });
    return out;
  }
  function updateSummary() {
    var items = allItems().filter(function (x) { return x.item.status !== 'toolarge'; });
    var bytes = items.reduce(function (s, x) { return s + x.item.file.size; }, 0);
    $('summary').textContent = items.length ? items.length + ' file' + (items.length > 1 ? 's' : '') + ' · ' + fmt(bytes) : 'No files added yet';
  }

  function showError(m) { var el = $('msg'); el.textContent = m; el.className = 'msg err'; el.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
  function clearError() { $('msg').className = 'msg hidden'; }

  function readB64(file) {
    return new Promise(function (resolve, reject) {
      var fr = new FileReader();
      fr.onload = function () { var s = String(fr.result); resolve(s.slice(s.indexOf(',') + 1)); };
      fr.onerror = function () { reject(new Error('Could not read ' + file.name)); };
      fr.readAsDataURL(file);
    });
  }

  // ---- submit ----
  $('f').addEventListener('submit', function (e) {
    e.preventDefault();
    if (busy) return;
    clearError();
    var form = {};
    Array.prototype.forEach.call($('f').elements, function (el) { if (el.name) form[el.name] = el.value; });
    if (form.website) return; // honeypot
    var required = Array.prototype.filter.call($('f').querySelectorAll('[required]'), function (el) { return !el.value.trim(); });
    if (required.length) { required[0].focus(); return showError('Please fill in the required fields marked with *.'); }
    var todo = allItems().filter(function (x) { return x.item.status === 'ready' || x.item.status === 'error'; });
    if (!todo.length) return showError('Please add at least one document.');
    REMEMBER.forEach(function (k) { store(k, form[k] || ''); });
    run(form, todo);
  });

  async function run(form, todo) {
    busy = true;
    var btn = $('submitBtn'); btn.disabled = true; btn.textContent = 'Uploading…';
    var bar = $('bar'), fill = bar.querySelector('i'); bar.classList.remove('hidden'); fill.style.width = '0';
    var uploaded = [], failed = 0, done = 0;
    try {
      var session = await api({ action: 'start', form: form });
      var idx = 0;
      async function worker() {
        while (idx < todo.length) {
          var x = todo[idx++], it = x.item;
          it.status = 'uploading'; it.stEl.className = 'st up'; it.stEl.textContent = 'Uploading…';
          try {
            var b64 = await readB64(it.file);
            var res = await api({ action: 'upload', token: session.token, category: x.key, fileName: it.file.name, mimeType: it.file.type || '', base64: b64 });
            it.status = 'done'; it.stEl.className = 'st ok'; it.stEl.textContent = 'Uploaded';
            uploaded.push({ category: x.key, name: res.name });
          } catch (err) {
            it.status = 'error'; it.stEl.className = 'st err'; it.stEl.textContent = 'Failed'; it.stEl.title = err.message || '';
            failed++;
          }
          done++; fill.style.width = Math.round(done / todo.length * 100) + '%';
        }
      }
      await Promise.all([worker(), worker(), worker()]);
      if (uploaded.length) await api({ action: 'finish', token: session.token, uploaded: uploaded });
      if (failed) {
        showError(failed + ' file' + (failed > 1 ? 's' : '') + ' did not upload. ' + (uploaded.length ? 'The others were received. ' : '') + 'Press "Upload documents" again to retry the failed ones.');
      } else {
        $('formView').classList.add('hidden');
        $('doneText').textContent = uploaded.length + ' file' + (uploaded.length > 1 ? 's were' : ' was') + ' received for ' + form.insuredName + ' — ' + form.street + '. Our team has been notified.';
        $('doneView').classList.remove('hidden');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } catch (err) {
      showError(err.message || 'Something went wrong. Please try again.');
    } finally {
      busy = false; btn.disabled = false; btn.textContent = 'Upload documents';
      setTimeout(function () { bar.classList.add('hidden'); }, 800);
    }
  }

  $('againBtn').addEventListener('click', function () {
    FILL_FIELDS.concat(['notes']).forEach(function (k) { if ($(k)) { $(k).value = ''; $(k).classList.remove('autofilled'); delete $(k).dataset.touched; } });
    $('state').value = 'TX';
    CATS.forEach(function (c) { queue[c.key] = []; });
    parsedFiles = {};
    Array.prototype.forEach.call(document.querySelectorAll('.files'), function (ul) { ul.innerHTML = ''; });
    $('fillMsg').className = 'fill-msg hidden';
    updateSummary(); clearError();
    $('doneView').classList.add('hidden'); $('formView').classList.remove('hidden');
    window.scrollTo({ top: 0 });
  });
}());
