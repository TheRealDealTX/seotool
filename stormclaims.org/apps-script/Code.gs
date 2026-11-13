/**
 * Rise Public Adjusting — Contractor Document Portal
 * ---------------------------------------------------
 * Referral contractors upload claim documents from one public link (no login).
 * Every submission:
 *   1. Files into Google Drive:  Rise PA – Portal Uploads / <Insured Name – Loss Address> / <Doc type> /
 *   2. Finds the matching card on the Trello "PA FILES" board (by insured name, address or claim #)
 *      — or creates one in "Files in PA - Need to send LOR" using the board's card template —
 *      and attaches the Drive folder link, fills custom fields, and comments what was uploaded.
 *   3. Logs the submission to a "Portal Submissions Log" sheet and emails you a notice.
 *
 * Deploy: Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone.
 * Script Properties (Project Settings > Script Properties):
 *   TRELLO_KEY       (required)  Trello API key
 *   TRELLO_TOKEN     (required)  Trello API token for your account
 *   PORTAL_CODE      (optional)  access code contractors must enter; leave unset for no code
 *   NOTIFY_EMAIL     (optional)  where new-upload notices go; defaults to the script owner
 *   ROOT_FOLDER_ID   (auto)      created on first run; set it yourself to use an existing folder
 *   LOG_SHEET_ID     (auto)      created on first run
 *   SIGNING_SECRET   (auto)      created on first run
 */

// ---------------- Configuration ----------------

var CONFIG = {
  ROOT_FOLDER_NAME: 'Rise PA – Portal Uploads',
  LOG_SHEET_NAME: 'Portal Submissions Log',

  TRELLO_BOARD_ID: '67b13f26f25df461859e3b23',          // PA FILES
  TRELLO_NEW_CARD_LIST_ID: '67b13f4929c1d47c33d03d0d',   // Files in PA - Need to send LOR
  TRELLO_ATTACHMENT_NAME: 'Drive – Claim Documents',

  // PA FILES custom field ids
  CF: {
    ADDRESS: '68ac7d87617e931333bf9140',          // text
    INSURANCE_COMPANY: '6858be7f0932e9b88c41b5ad', // text
    SALES_PERSON: '6858bc1a13408f5a525b9241',      // text
    SALES_PERSON_EMAIL: '6858bc1a13408f5a525b923e',// text
    CLAIM_NUMBER: '6a79ebb5d02d4e048f016b43',      // number (only set when the claim # is all digits)
    CREATION_DATE: '69ae005d8b53e427b2c0530e',     // date
    CREATE_DATE: '69cd54ba1246611dfb8b60c8'        // date
  },

  // Upload categories -> Drive subfolder names (order = order on the page)
  CATEGORIES: {
    policy:     '01 Policy & Declarations',
    carrier:    '02 Carrier Letters & Estimates',
    contractor: '03 Contractor Estimate & Measurements',
    photos:     '04 Photos & Videos',
    signed:     '05 Signed Contract & LOR',
    other:      '06 Other'
  },

  MAX_FILE_MB: 25,   // per file; google.script.run payloads get unreliable much past this once base64-encoded
  MAX_FILES_PER_SUBMISSION: 150,
  TOKEN_TTL_HOURS: 6
};

// ---------------- Web app entry ----------------

function doGet() {
  var t = HtmlService.createTemplateFromFile('Index');
  t.requireCode = !!prop_('PORTAL_CODE');
  t.maxFileMb = CONFIG.MAX_FILE_MB;
  return t.evaluate()
    .setTitle('Rise Public Adjusting – Document Upload')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * JSON entry point for the stormclaims.org form. Same three steps as the
 * google.script.run calls above, wrapped so a plain browser fetch() can use
 * them: POST a JSON body (sent as text/plain so no CORS preflight) with an
 * "action" of config | start | upload | finish.
 */
function doPost(e) {
  var out;
  try {
    var body = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    var action = String(body.action || '');
    if (action === 'config') {
      out = { ok: true, requireCode: !!prop_('PORTAL_CODE'), maxFileMb: CONFIG.MAX_FILE_MB, maxFiles: CONFIG.MAX_FILES_PER_SUBMISSION };
    } else if (action === 'start') {
      var s = startSubmission(body.form || {});
      out = { ok: true, token: s.token, folderName: s.folderName };
    } else if (action === 'upload') {
      var u = uploadFile(body.token, body.category, body.fileName, body.mimeType, body.base64);
      out = { ok: true, id: u.id, name: u.name };
    } else if (action === 'finish') {
      var fin = finishSubmission(body.token, body.uploaded || []);
      out = { ok: true, fileCount: fin.fileCount };
    } else {
      throw new Error('Unknown action.');
    }
  } catch (err) {
    out = { ok: false, error: String((err && err.message) || err) };
  }
  return ContentService.createTextOutput(JSON.stringify(out)).setMimeType(ContentService.MimeType.JSON);
}

// ---------------- Client-callable functions ----------------

/**
 * Step 1: validate the form, create/find the claim folder and its subfolders.
 * Returns a signed token the browser passes back with each file.
 */
function startSubmission(form) {
  form = sanitizeForm_(form || {});
  checkAccessCode_(form.accessCode);

  var missing = [];
  if (!form.insuredName) missing.push('Insured name');
  if (!form.street) missing.push('Loss address (street)');
  if (!form.city) missing.push('City');
  if (!form.state) missing.push('State');
  if (!form.zip) missing.push('ZIP');
  if (!form.company) missing.push('Your company');
  if (!form.repName) missing.push('Your name');
  if (!form.repEmail) missing.push('Your email');
  if (missing.length) throw new Error('Please fill in: ' + missing.join(', '));
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.repEmail)) throw new Error('Please enter a valid email address.');

  var root = getRootFolder_();
  var folderName = claimFolderName_(form);
  var claimFolder = findClaimFolder_(root, form) || getOrCreateChild_(root, folderName);
  folderName = claimFolder.getName();

  var submissionId = Utilities.getUuid();
  var issued = Date.now();
  var payload = { s: submissionId, f: claimFolder.getId(), t: issued };

  // Keep the form server-side so finishSubmission can't be fed different data.
  CacheService.getScriptCache().put('sub_' + submissionId, JSON.stringify(form), 21600);

  return {
    token: signToken_(payload),
    folderName: folderName
  };
}

/**
 * Step 2: one call per file. base64 is the file body (no data: prefix).
 */
function uploadFile(token, category, fileName, mimeType, base64) {
  var claim = verifyToken_(token);
  var subName = CONFIG.CATEGORIES[category];
  if (!subName) throw new Error('Unknown document type.');

  var bytes = Utilities.base64Decode(base64);
  if (bytes.length > CONFIG.MAX_FILE_MB * 1024 * 1024) {
    throw new Error(fileName + ' is larger than ' + CONFIG.MAX_FILE_MB + ' MB.');
  }

  var countKey = 'cnt_' + claim.s;
  var cache = CacheService.getScriptCache();
  var count = Number(cache.get(countKey) || 0) + 1;
  if (count > CONFIG.MAX_FILES_PER_SUBMISSION) throw new Error('Too many files in one submission.');
  cache.put(countKey, String(count), 21600);

  var claimFolder = DriveApp.getFolderById(claim.f);
  var sub = getOrCreateChild_(claimFolder, subName);
  var safeName = cleanFileName_(fileName) || ('upload-' + count);
  var blob = Utilities.newBlob(bytes, mimeType || 'application/octet-stream', uniqueName_(sub, safeName));
  var file = sub.createFile(blob);
  return { id: file.getId(), name: file.getName() };
}

/**
 * Step 3: after all files are in, update Trello, log, and notify.
 * uploaded = [{category, name}]
 */
function finishSubmission(token, uploaded) {
  var claim = verifyToken_(token);
  var cache = CacheService.getScriptCache();
  var raw = cache.get('sub_' + claim.s);
  if (!raw) throw new Error('This upload session expired. Please submit again.');
  var form = JSON.parse(raw);
  uploaded = (uploaded || []).slice(0, CONFIG.MAX_FILES_PER_SUBMISSION);

  var folder = DriveApp.getFolderById(claim.f);
  var folderUrl = folder.getUrl();

  var trello = { ok: false, cardUrl: '', created: false, error: '' };
  try {
    trello = syncTrello_(form, folderUrl, uploaded);
  } catch (e) {
    trello.error = String(e && e.message || e);
  }

  try { logSubmission_(form, folderUrl, uploaded, trello); } catch (e) { /* logging is best-effort */ }
  try { notifyOwner_(form, folderUrl, uploaded, trello); } catch (e) { /* email is best-effort */ }

  cache.remove('sub_' + claim.s);
  cache.remove('cnt_' + claim.s);

  return { ok: true, fileCount: uploaded.length };
}

// ---------------- Trello ----------------

function syncTrello_(form, folderUrl, uploaded) {
  var key = prop_('TRELLO_KEY'), token = prop_('TRELLO_TOKEN');
  if (!key || !token) throw new Error('Trello key/token not set in Script Properties.');

  var card = findMatchingCard_(form);
  var created = false;
  if (!card) {
    card = trello_('post', '/cards', {
      idList: CONFIG.TRELLO_NEW_CARD_LIST_ID,
      name: form.insuredName,
      desc: cardDescription_(form),
      pos: 'top'
    });
    created = true;
    setCustomFieldsOnNewCard_(card.id, form);
  } else {
    fillBlankCustomFields_(card, form);
  }

  // Attach the folder link once.
  var attachments = trello_('get', '/cards/' + card.id + '/attachments', { fields: 'url' });
  var already = attachments.some(function (a) { return a.url === folderUrl; });
  if (!already) {
    trello_('post', '/cards/' + card.id + '/attachments', { url: folderUrl, name: CONFIG.TRELLO_ATTACHMENT_NAME });
  }

  trello_('post', '/cards/' + card.id + '/actions/comments', { text: uploadComment_(form, folderUrl, uploaded, created) });

  return { ok: true, cardUrl: card.shortUrl || card.url || '', created: created, error: '' };
}

/** Match on claim #, then street address, then insured name (open cards on PA FILES). */
function findMatchingCard_(form) {
  var cards = trello_('get', '/boards/' + CONFIG.TRELLO_BOARD_ID + '/cards/open', {
    fields: 'name,desc,shortUrl,url',
    customFieldItems: 'true'
  });
  return pickMatch_(cards, form);
}

function pickMatch_(cards, form) {
  var claimNo = normClaim_(form.claimNumber);
  var streetKey = streetKey_(form.street);
  var nameKey = normName_(form.insuredName);

  function cfText(card, fieldId) {
    var items = card.customFieldItems || [];
    for (var i = 0; i < items.length; i++) {
      if (items[i].idCustomField === fieldId && items[i].value) {
        return String(items[i].value.text || items[i].value.number || '');
      }
    }
    return '';
  }

  if (claimNo && claimNo.length >= 5) {
    for (var i = 0; i < cards.length; i++) {
      var c = cards[i];
      if (normClaim_(cfText(c, CONFIG.CF.CLAIM_NUMBER)) === claimNo) return c;
      if (normClaim_(c.desc || '').indexOf(claimNo) !== -1) return c;
    }
  }
  if (streetKey) {
    for (var j = 0; j < cards.length; j++) {
      var d = cards[j];
      if (streetKey_(cfText(d, CONFIG.CF.ADDRESS)) === streetKey) return d;
      if (streetKey_(extractLossAddress_(d.desc || '')) === streetKey) return d;
    }
  }
  if (nameKey) {
    for (var k = 0; k < cards.length; k++) {
      if (normName_(cards[k].name) === nameKey) return cards[k];
    }
  }
  return null;
}

function cardDescription_(f) {
  var addr = fullAddress_(f);
  return [
    '**Phone #:** ' + (f.insuredPhone || ''),
    '',
    '**Email:** ' + (f.insuredEmail || ''),
    '',
    '**Claim #:** ' + (f.claimNumber || ''),
    '',
    '**Policy #:** ' + (f.policyNumber || ''),
    '',
    '**Type of Loss:** ' + (f.lossType || ''),
    '',
    '**Loss Address:** ' + addr,
    '',
    '**Insurance:** ' + (f.carrier || ''),
    '',
    '**Date of Loss:** ' + (f.dateOfLoss || ''),
    '',
    '---',
    '**Referred by:** ' + f.repName + ' – ' + f.company + (f.repPhone ? ' – ' + f.repPhone : '') + ' – ' + f.repEmail
  ].join('\n');
}

function uploadComment_(f, folderUrl, uploaded, created) {
  var lines = [];
  lines.push((created ? 'New file from contractor portal' : 'New documents from contractor portal') +
    ' — ' + f.repName + ' (' + f.company + ')');
  if (f.notes) lines.push('', '**Notes:** ' + f.notes);
  lines.push('', '**Uploaded (' + uploaded.length + '):**');
  var byCat = {};
  uploaded.forEach(function (u) {
    var label = CONFIG.CATEGORIES[u.category] || 'Other';
    (byCat[label] = byCat[label] || []).push(u.name);
  });
  Object.keys(byCat).sort().forEach(function (label) {
    lines.push('- ' + label.replace(/^\d+\s/, '') + ': ' + byCat[label].join(', '));
  });
  lines.push('', '[Open Drive folder](' + folderUrl + ')');
  return lines.join('\n').slice(0, 15000);
}

function setCustomFieldsOnNewCard_(cardId, f) {
  var today = new Date();
  today.setHours(12, 0, 0, 0);
  setCF_(cardId, CONFIG.CF.ADDRESS, { text: fullAddress_(f) });
  if (f.carrier) setCF_(cardId, CONFIG.CF.INSURANCE_COMPANY, { text: f.carrier });
  setCF_(cardId, CONFIG.CF.SALES_PERSON, { text: f.repName + ' (' + f.company + ')' });
  setCF_(cardId, CONFIG.CF.SALES_PERSON_EMAIL, { text: f.repEmail });
  if (/^\d+$/.test(f.claimNumber || '')) setCF_(cardId, CONFIG.CF.CLAIM_NUMBER, { number: f.claimNumber });
  setCF_(cardId, CONFIG.CF.CREATION_DATE, { date: today.toISOString() });
  setCF_(cardId, CONFIG.CF.CREATE_DATE, { date: today.toISOString() });
}

/** On an existing card, only fill fields that are empty — never overwrite your team's data. */
function fillBlankCustomFields_(card, f) {
  var have = {};
  (card.customFieldItems || []).forEach(function (i) { have[i.idCustomField] = true; });
  if (!have[CONFIG.CF.ADDRESS]) setCF_(card.id, CONFIG.CF.ADDRESS, { text: fullAddress_(f) });
  if (!have[CONFIG.CF.INSURANCE_COMPANY] && f.carrier) setCF_(card.id, CONFIG.CF.INSURANCE_COMPANY, { text: f.carrier });
  if (!have[CONFIG.CF.SALES_PERSON]) setCF_(card.id, CONFIG.CF.SALES_PERSON, { text: f.repName + ' (' + f.company + ')' });
  if (!have[CONFIG.CF.SALES_PERSON_EMAIL]) setCF_(card.id, CONFIG.CF.SALES_PERSON_EMAIL, { text: f.repEmail });
  if (!have[CONFIG.CF.CLAIM_NUMBER] && /^\d+$/.test(f.claimNumber || '')) {
    setCF_(card.id, CONFIG.CF.CLAIM_NUMBER, { number: f.claimNumber });
  }
}

function setCF_(cardId, fieldId, value) {
  try {
    trello_('put', '/cards/' + cardId + '/customField/' + fieldId + '/item', { value: value }, true);
  } catch (e) {
    // A single field failing shouldn't stop the upload from being linked.
  }
}

function trello_(method, path, params, asJsonBody) {
  var key = prop_('TRELLO_KEY'), token = prop_('TRELLO_TOKEN');
  var url = 'https://api.trello.com/1' + path;
  var auth = 'key=' + encodeURIComponent(key) + '&token=' + encodeURIComponent(token);
  var opts = { method: method, muteHttpExceptions: true };

  if (method === 'get') {
    url += '?' + auth + '&' + toQuery_(params || {});
  } else if (asJsonBody) {
    url += '?' + auth;
    opts.contentType = 'application/json';
    opts.payload = JSON.stringify(params || {});
  } else {
    url += '?' + auth;
    opts.payload = params || {};
  }

  var res = UrlFetchApp.fetch(url, opts);
  var code = res.getResponseCode();
  if (code < 200 || code >= 300) {
    throw new Error('Trello ' + method.toUpperCase() + ' ' + path + ' failed (' + code + '): ' + res.getContentText().slice(0, 200));
  }
  var text = res.getContentText();
  return text ? JSON.parse(text) : {};
}

// ---------------- Drive helpers ----------------

function getRootFolder_() {
  var id = prop_('ROOT_FOLDER_ID');
  if (id) {
    try { return DriveApp.getFolderById(id); } catch (e) { /* fall through and recreate */ }
  }
  var it = DriveApp.getFoldersByName(CONFIG.ROOT_FOLDER_NAME);
  var folder = it.hasNext() ? it.next() : DriveApp.createFolder(CONFIG.ROOT_FOLDER_NAME);
  setProp_('ROOT_FOLDER_ID', folder.getId());
  return folder;
}

/** Reuse an existing claim folder when the same street address was typed differently ("Dr" vs "Drive"). */
function findClaimFolder_(root, form) {
  var key = streetKey_(form.street);
  if (!key) return null;
  var it = root.getFolders();
  while (it.hasNext()) {
    var f = it.next();
    var parts = f.getName().split(' – ');
    if (parts.length > 1 && streetKey_(parts.slice(1).join(' – ')) === key &&
        (!form.zip || f.getName().indexOf(form.zip.slice(0, 5)) !== -1)) return f;
  }
  return null;
}

function getOrCreateChild_(parent, name) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var it = parent.getFoldersByName(name);
    return it.hasNext() ? it.next() : parent.createFolder(name);
  } finally {
    lock.releaseLock();
  }
}

function uniqueName_(folder, name) {
  if (!folder.getFilesByName(name).hasNext()) return name;
  var dot = name.lastIndexOf('.');
  var base = dot > 0 ? name.slice(0, dot) : name;
  var ext = dot > 0 ? name.slice(dot) : '';
  var stamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone() || 'America/Chicago', 'yyyy-MM-dd HHmmss');
  return base + ' (' + stamp + ')' + ext;
}

// ---------------- Logging & notification ----------------

function logSubmission_(f, folderUrl, uploaded, trello) {
  var ss;
  var id = prop_('LOG_SHEET_ID');
  if (id) { try { ss = SpreadsheetApp.openById(id); } catch (e) { ss = null; } }
  if (!ss) {
    ss = SpreadsheetApp.create(CONFIG.LOG_SHEET_NAME);
    DriveApp.getFileById(ss.getId()).moveTo(getRootFolder_());
    setProp_('LOG_SHEET_ID', ss.getId());
    ss.getSheets()[0].appendRow(['Submitted', 'Insured', 'Loss Address', 'Claim #', 'Carrier', 'Company', 'Rep', 'Rep Email',
      'Rep Phone', 'Files', 'Drive Folder', 'Trello Card', 'Card', 'Trello Error', 'Notes']);
    ss.getSheets()[0].setFrozenRows(1);
  }
  ss.getSheets()[0].appendRow([
    new Date(), f.insuredName, fullAddress_(f), f.claimNumber, f.carrier, f.company, f.repName, f.repEmail,
    f.repPhone, uploaded.length, folderUrl, trello.cardUrl || '', trello.ok ? (trello.created ? 'Created' : 'Updated') : 'FAILED',
    trello.error || '', f.notes
  ]);
}

function notifyOwner_(f, folderUrl, uploaded, trello) {
  var to = prop_('NOTIFY_EMAIL') || Session.getEffectiveUser().getEmail();
  if (!to) return;
  var status = trello.ok
    ? (trello.created ? 'New Trello card created' : 'Added to existing Trello card')
    : 'Trello update FAILED — ' + escapeHtml_(trello.error);
  var html = '<p><b>' + escapeHtml_(f.repName) + '</b> (' + escapeHtml_(f.company) + ') uploaded ' + uploaded.length +
    ' file(s) for <b>' + escapeHtml_(f.insuredName) + '</b> — ' + escapeHtml_(fullAddress_(f)) + '.</p>' +
    '<p>' + status + '</p>' +
    '<p><a href="' + folderUrl + '">Open Drive folder</a>' +
    (trello.cardUrl ? ' &nbsp;|&nbsp; <a href="' + trello.cardUrl + '">Open Trello card</a>' : '') + '</p>' +
    (f.notes ? '<p><b>Notes:</b> ' + escapeHtml_(f.notes) + '</p>' : '');
  MailApp.sendEmail({
    to: to,
    subject: 'Portal upload: ' + f.insuredName + ' (' + f.company + ')',
    htmlBody: html,
    replyTo: f.repEmail
  });
}

// ---------------- Security helpers ----------------

function checkAccessCode_(code) {
  var required = prop_('PORTAL_CODE');
  if (!required) return;
  if (String(code || '').trim().toLowerCase() !== String(required).trim().toLowerCase()) {
    throw new Error('Access code is incorrect.');
  }
}

function signingSecret_() {
  var s = prop_('SIGNING_SECRET');
  if (!s) { s = Utilities.getUuid() + Utilities.getUuid(); setProp_('SIGNING_SECRET', s); }
  return s;
}

function signToken_(payload) {
  var body = Utilities.base64EncodeWebSafe(JSON.stringify(payload));
  var sig = Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(body, signingSecret_()));
  return body + '.' + sig;
}

function verifyToken_(token) {
  var parts = String(token || '').split('.');
  if (parts.length !== 2) throw new Error('Invalid upload session. Please reload the page.');
  var expected = Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(parts[0], signingSecret_()));
  if (expected !== parts[1]) throw new Error('Invalid upload session. Please reload the page.');
  var payload = JSON.parse(Utilities.newBlob(Utilities.base64DecodeWebSafe(parts[0])).getDataAsString());
  if (Date.now() - payload.t > CONFIG.TOKEN_TTL_HOURS * 3600 * 1000) {
    throw new Error('This upload session expired. Please reload the page.');
  }
  return payload;
}

// ---------------- Pure helpers ----------------

function sanitizeForm_(f) {
  var fields = ['accessCode', 'company', 'repName', 'repEmail', 'repPhone', 'insuredName', 'insuredPhone', 'insuredEmail',
    'street', 'city', 'state', 'zip', 'carrier', 'claimNumber', 'policyNumber', 'lossType', 'dateOfLoss', 'notes'];
  var out = {};
  fields.forEach(function (k) {
    var v = f[k] == null ? '' : String(f[k]);
    v = v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim();
    out[k] = v.slice(0, k === 'notes' ? 2000 : 200);
  });
  out.state = out.state.toUpperCase();
  return out;
}

function fullAddress_(f) {
  return f.street + ', ' + f.city + ', ' + f.state + ' ' + f.zip;
}

function claimFolderName_(f) {
  var name = titleCase_(f.insuredName) + ' – ' + f.street + ', ' + f.city + ' ' + f.state + ' ' + f.zip;
  return name.replace(/[\/\\:*?"<>|#]/g, '-').replace(/\s+/g, ' ').trim().slice(0, 180);
}

function titleCase_(s) {
  s = String(s || '').trim().replace(/\s+/g, ' ');
  if (s !== s.toUpperCase() && s !== s.toLowerCase()) return s; // respect mixed case as typed
  return s.toLowerCase().replace(/(^|[\s\-'&\/])([a-z])/g, function (m, p, c) { return p + c.toUpperCase(); });
}

function cleanFileName_(n) {
  return String(n || '').replace(/[\/\\:*?"<>|\u0000-\u001F]/g, '-').trim().slice(0, 180);
}

function normName_(s) {
  return String(s || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
}

function normClaim_(s) {
  return String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');
}

var STREET_SUFFIX_ = {
  street: 'st', st: 'st', drive: 'dr', dr: 'dr', avenue: 'ave', ave: 'ave', av: 'ave', road: 'rd', rd: 'rd',
  lane: 'ln', ln: 'ln', court: 'ct', ct: 'ct', circle: 'cir', cir: 'cir', boulevard: 'blvd', blvd: 'blvd',
  parkway: 'pkwy', pkwy: 'pkwy', place: 'pl', pl: 'pl', trail: 'trl', trl: 'trl', way: 'way', terrace: 'ter',
  ter: 'ter', highway: 'hwy', hwy: 'hwy', cove: 'cv', cv: 'cv', loop: 'loop', point: 'pt', pt: 'pt'
};
var DIRS_ = { north: 'n', south: 's', east: 'e', west: 'w', n: 'n', s: 's', e: 'e', w: 'w' };

/** "10940 Castle Dr., Frisco TX" -> "10940 castle dr" — house number + street, normalized. */
function streetKey_(s) {
  s = String(s || '').split(',')[0].toLowerCase().replace(/[.#]/g, ' ').replace(/\s+/g, ' ').trim();
  var m = s.match(/^(\d+[a-z]?)\s+(.+)$/);
  if (!m) return '';
  var words = m[2].split(' ').filter(Boolean).map(function (w) {
    return STREET_SUFFIX_[w] || DIRS_[w] || w;
  });
  // Drop unit designators and anything after them
  var cut = words.findIndex(function (w) { return /^(apt|unit|ste|suite|bldg)$/.test(w); });
  if (cut > 0) words = words.slice(0, cut);
  // Stop after the street suffix (plus a trailing direction) so "Castle Dr. Frisco" == "Castle Drive"
  var suffixes = {};
  Object.keys(STREET_SUFFIX_).forEach(function (k) { suffixes[STREET_SUFFIX_[k]] = true; });
  for (var i = 1; i < words.length; i++) {
    if (suffixes[words[i]]) {
      var end = (i + 1 < words.length && /^[nsew]$/.test(words[i + 1])) ? i + 2 : i + 1;
      words = words.slice(0, end);
      break;
    }
  }
  return m[1] + ' ' + words.join(' ');
}

/** Pull the "**Loss Address:** ..." line out of a PA FILES card description. */
function extractLossAddress_(desc) {
  var m = String(desc || '').match(/Loss Address:\**\s*\[?([^\]\n]+)/i);
  return m ? m[1].trim() : '';
}

function toQuery_(o) {
  return Object.keys(o).map(function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(o[k]); }).join('&');
}

function escapeHtml_(s) {
  return String(s || '').replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  });
}

function prop_(k) { return PropertiesService.getScriptProperties().getProperty(k); }
function setProp_(k, v) { PropertiesService.getScriptProperties().setProperty(k, v); }

// ---------------- One-time setup / test ----------------

/**
 * Run this once from the editor (select "setup" then Run) to grant permissions,
 * create the Drive root folder, and confirm the Trello connection.
 */
function setup() {
  var root = getRootFolder_();
  signingSecret_();
  Logger.log('Drive root folder: ' + root.getUrl());
  if (!prop_('TRELLO_KEY') || !prop_('TRELLO_TOKEN')) {
    Logger.log('Trello: add TRELLO_KEY and TRELLO_TOKEN in Project Settings > Script Properties, then run setup again.');
    return;
  }
  var board = trello_('get', '/boards/' + CONFIG.TRELLO_BOARD_ID, { fields: 'name,url' });
  Logger.log('Trello connected to board: ' + board.name + ' (' + board.url + ')');
}