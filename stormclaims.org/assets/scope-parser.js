/* Scope parser: pulls claim details out of the text of an insurance estimate
   (Xactimate, Symbility and similar). Pure function, no DOM, so it can be
   unit-tested in Node. Input is the document text with one line per visual
   line; output is {fields:{...}, found:[...]} with only the fields it is
   confident about. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.ScopeParser = factory();
}(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var CARRIERS = [
    ['State Farm', /state\s*farm/i], ['Allstate', /allstate/i], ['USAA', /\busaa\b/i],
    ['Farmers', /farmers\s+(insurance|group)|\bfarmers\b(?!\s+(market|branch))/i],
    ['Liberty Mutual', /liberty\s*mutual/i], ['Travelers', /travelers/i], ['Nationwide', /nationwide/i],
    ['Progressive', /progressive/i], ['American Family', /american\s+family|\bamfam\b/i], ['Chubb', /\bchubb\b/i],
    ['Texas Farm Bureau', /texas\s+farm\s+bureau|txfb/i], ['TWIA', /\btwia\b|texas\s+windstorm/i],
    ['Safeco', /safeco/i], ['The Hartford', /hartford/i], ['Amica', /\bamica\b/i], ['Lemonade', /lemonade/i],
    ['Hippo', /\bhippo\b/i], ['Kin Insurance', /\bkin\s+insurance|kin\.com/i], ['Openly', /\bopenly\b/i],
    ['SageSure', /sagesure/i], ['Homesite', /homesite/i], ['Assurant', /assurant/i], ['Foremost', /foremost/i],
    ['Mercury', /mercury\s+insurance|\bmercury\b/i], ['Kemper', /kemper/i], ['Allied Trust', /allied\s+trust/i],
    ['AAA', /\baaa\b|csaa/i], ['Erie', /\berie\b/i], ['Auto-Owners', /auto[\s-]?owners/i], ['Germania', /germania/i],
    ['Universal Property', /universal\s+property|universal\s+insurance/i], ['Citizens', /citizens\s+property|citizensfla/i],
    ['Heritage', /heritage\s+(property|insurance)|heritagepci/i], ['Tower Hill', /tower\s*hill/i], ['Slide', /slide\s+insurance/i],
    ['American Integrity', /american\s+integrity/i], ['Florida Peninsula', /florida\s+peninsula/i],
    ['Security First', /security\s+first/i], ['Frontline', /frontline/i], ['Wellington', /wellington/i],
    ['Homeowners of America', /homeowners\s+of\s+america|\bhoaic\b/i], ['National Lloyds', /national\s+lloyds/i],
    ['Cypress', /cypress\s+(property|insurance|texas)/i], ['Encompass', /encompass/i], ['Ameriprise', /ameriprise/i],
    ['Stillwater', /stillwater/i], ['Narragansett Bay', /narragansett/i], ['Occidental', /occidental/i],
    ['UPC', /\bupc\b|united\s+property/i], ['Bankers', /bankers\s+insurance/i], ['Branch', /\bbranch\s+insurance/i],
    ['Westwood', /westwood/i], ['Spinnaker', /spinnaker/i], ['Velocity', /velocity\s+risk/i], ['QBE', /\bqbe\b/i],
    ['Hanover', /hanover/i], ['Pure', /\bpure\s+insurance|privilege\s+underwriters/i], ['AIG', /\baig\b/i],
    ['Berkshire Hathaway', /berkshire/i], ['GEICO', /geico/i], ['Lighthouse', /lighthouse\s+(property|insurance)/i],
    ['Vault', /\bvault\s+insurance/i], ['Elephant', /elephant\s+insurance/i], ['Centauri', /centauri/i],
    ['Loggerhead', /loggerhead/i], ['Olympus', /olympus\s+insurance/i], ['Southern Oak', /southern\s+oak/i],
    ['Edison', /edison\s+insurance/i], ['People\'s Trust', /people'?s\s+trust/i], ['Gulfstream', /gulfstream/i]
  ];

  var EMAIL_CARRIERS = {
    'statefarm.com': 'State Farm', 'allstate.com': 'Allstate', 'usaa.com': 'USAA', 'farmersinsurance.com': 'Farmers',
    'libertymutual.com': 'Liberty Mutual', 'travelers.com': 'Travelers', 'nationwide.com': 'Nationwide',
    'progressive.com': 'Progressive', 'amfam.com': 'American Family', 'chubb.com': 'Chubb', 'txfb-ins.com': 'Texas Farm Bureau',
    'twia.org': 'TWIA', 'safeco.com': 'Safeco', 'thehartford.com': 'The Hartford', 'amica.com': 'Amica', 'lemonade.com': 'Lemonade',
    'hippo.com': 'Hippo', 'kin.com': 'Kin Insurance', 'openly.com': 'Openly', 'sagesure.com': 'SageSure', 'homesite.com': 'Homesite',
    'assurant.com': 'Assurant', 'foremost.com': 'Foremost', 'mercuryinsurance.com': 'Mercury', 'kemper.com': 'Kemper',
    'erieinsurance.com': 'Erie', 'auto-owners.com': 'Auto-Owners', 'germaniainsurance.com': 'Germania',
    'universalproperty.com': 'Universal Property', 'citizensfla.com': 'Citizens', 'heritagepci.com': 'Heritage',
    'thig.com': 'Tower Hill', 'slideinsurance.com': 'Slide', 'aiicfl.com': 'American Integrity', 'geico.com': 'GEICO'
  };

  // Labels we understand, in the forms they appear in estimate headers.
  var LABELS = [
    ['insuredName', /^(insured|insured name|named insured|policyholder|customer|client)$/i],
    ['property', /^(property|property address|loss address|loss location|risk address|location|address of loss|job address)$/i],
    ['homePhone', /^(home|home phone|phone)$/i],
    ['cellPhone', /^(cellular|cell|mobile|cell phone)$/i],
    ['business', /^(business|work|office)$/i],
    ['email', /^(e-?mail|email address)$/i],
    ['claimRep', /^(claim rep\.?|claim rep|adjuster|desk adjuster|field adjuster|claims adjuster|claim representative|claim handler)$/i],
    ['estimator', /^(estimator|contractor|prepared by)$/i],
    ['company', /^(company|insurance company|insurer|carrier|insurance carrier)$/i],
    ['claimNumber', /^(claim number|claim #|claim no\.?|claim|claim id|claim nbr)$/i],
    ['policyNumber', /^(policy number|policy #|policy no\.?|policy|policy nbr)$/i],
    ['lossType', /^(type of loss|loss type|cause of loss|peril|loss cause)$/i],
    ['dateOfLoss', /^(date of loss|loss date|dol|d\.o\.l\.?|date of incident)$/i],
    ['ignore', /^(date contacted|date received|date inspected|date entered|date est\.? completed|price list|estimate|position|file number|reference|dates?|date est\. completed|labor efficiency|business|fax|website|web|job|job #|job number|ref|opp|rep)$/i]
  ];

  var SUFFIXES = 'st|street|dr|drive|ave|avenue|av|rd|road|ln|lane|ct|court|cir|circle|blvd|boulevard|pkwy|parkway|pl|place|trl|trail|way|ter|terrace|hwy|highway|cv|cove|loop|pt|point|run|path|pass|xing|crossing|bend|hollow|holw|ridge|rdg|park|sq|square|row|walk|trce|trace|mnr|manor|vw|view|est|estates|cres|crescent|gln|glen|grv|grove|hts|heights|is|isle|lndg|landing|mdw|meadows?|ml|mill|spur|vly|valley|fwy|freeway|expy|expressway|byp|bypass|aly|alley';
  var SUFFIX_RE = new RegExp('\\b(' + SUFFIXES + ')\\.?(\\s+(n|s|e|w|ne|nw|se|sw|north|south|east|west))?\\b\\.?', 'i');

  function clean(s) { return String(s || '').replace(/\s+/g, ' ').trim(); }

  function titleCase(s) {
    s = clean(s);
    if (!s || s !== s.toUpperCase()) return s;
    return s.toLowerCase().replace(/(^|[\s\-'&\/(])([a-z])/g, function (m, p, c) { return p + c.toUpperCase(); })
      .replace(/\b(Ii|Iii|Iv|Llc|Hoa|Jr|Sr)\b/g, function (m) { return m.toUpperCase(); });
  }

  /* "LAST, FIRST" -> "First Last" when it looks like a single person. */
  function personName(s) {
    s = clean(s).replace(/\s*(&|and)\s*$/i, '');
    var m = s.match(/^([A-Za-z' -]+),\s*([A-Za-z' .-]+)$/);
    if (m && !/&| and /i.test(s)) s = m[2] + ' ' + m[1];
    return titleCase(s);
  }

  /* Split a line into [{label,value,index}] at "Label:" boundaries.
     For each colon, take the longest known label ending there; otherwise
     up to three capitalised words, so "JOHN DOE Home:" yields "Home". */
  function splitLabels(line) {
    var out = [], last = null;
    for (var i = 0; i < line.length; i++) {
      if (line[i] !== ':') continue;
      if (i + 1 < line.length && !/\s/.test(line[i + 1])) continue;      // "http://", "12:00"
      if (i > 0 && /\d/.test(line[i - 1])) continue;                     // times
      var before = line.slice(Math.max(0, i - 40), i);
      var label = knownLabelAtEnd(before);
      if (!label) {
        var m = before.match(/(?:^|\s)((?:[A-Z][\w.#\/&'-]*)(?:\s+(?:[A-Z][\w.#\/&'-]*|of|de)){0,2})$/);
        if (!m) continue;
        label = m[1];
      }
      var start = i - label.length;
      if (start > 0 && !/\s/.test(line[start - 1])) continue;
      if (last) last.value = clean(line.slice(last.end, start));
      last = { label: clean(label), index: start, end: i + 1, value: '' };
      out.push(last);
    }
    if (last) last.value = clean(line.slice(last.end));
    return out;
  }

  var KNOWN_LABEL_WORDS = [];
  (function () {
    var src = LABELS.map(function (l) { return l[1].source; }).join('|');
    src.replace(/\(|\)|\^|\$/g, '').split('|').forEach(function (s) {
      s = s.replace(/\\\./g, '.').replace(/\?/g, '').trim();
      if (s && s.length > 1) KNOWN_LABEL_WORDS.push(s);
    });
    KNOWN_LABEL_WORDS.sort(function (a, b) { return b.length - a.length; });
  }());

  function knownLabelAtEnd(before) {
    var low = before.toLowerCase();
    for (var i = 0; i < KNOWN_LABEL_WORDS.length; i++) {
      var w = KNOWN_LABEL_WORDS[i];
      if (low.slice(-w.length) === w) {
        var at = before.length - w.length;
        if (at === 0 || /\s/.test(before[at - 1])) return before.slice(at);
        // "Claim Rep." may appear as "Claim Rep" with the dot stripped; allow trailing dot variants
      }
      if (w.slice(-1) === '.' && low.slice(-(w.length - 1)) === w.slice(0, -1)) {
        var at2 = before.length - (w.length - 1);
        if (at2 === 0 || /\s/.test(before[at2 - 1])) return before.slice(at2);
      }
    }
    return '';
  }

  function labelKey(label) {
    for (var i = 0; i < LABELS.length; i++) if (LABELS[i][1].test(label)) return LABELS[i][0];
    return null;
  }

  var CSZ_RE = /^(.*?)[,\s]+([A-Z]{2})\s+(\d{5})(?:-\d{4})?\s*(?:usa?)?$/i;

  /* Split "123 Main St, Houston, TX 77002" / "123 Main St Houston TX 77002" into parts. */
  function splitAddress(text) {
    text = clean(text).replace(/\s+,/g, ',');
    var m = text.match(CSZ_RE);
    if (!m) return null;
    var rest = m[1].replace(/,\s*$/, ''), state = m[2].toUpperCase(), zip = m[3];
    var street, city;
    var comma = rest.lastIndexOf(',');
    if (comma > 0) { street = clean(rest.slice(0, comma)); city = clean(rest.slice(comma + 1)); }
    else {
      var sm = SUFFIX_RE.exec(rest);
      if (sm) {
        var cut = sm.index + sm[0].length;
        var tail = rest.slice(cut);
        var unit = tail.match(/^\s*(#\s*\w+|(apt|unit|ste|suite|bldg|lot|no\.?)\s*\.?\s*\w+)/i);
        if (unit) cut += unit[0].length;
        street = clean(rest.slice(0, cut)); city = clean(rest.slice(cut));
      } else {
        var words = rest.split(' ');
        street = words.slice(0, -1).join(' '); city = words.slice(-1).join(' ');
      }
    }
    if (!street || !/\d/.test(street)) return null;
    return { street: titleCase(street), city: titleCase(city.replace(/,$/, '')), state: state, zip: zip };
  }

  function parseDate(s) {
    s = clean(s);
    var m = s.match(/(\d{4})-(\d{2})-(\d{2})/);
    if (m) return m[0];
    m = s.match(/(\d{1,2})[\/\-.](\d{1,2})[\/\-.](\d{2,4})/);
    if (m) {
      var y = m[3].length === 2 ? '20' + m[3] : m[3];
      return y + '-' + ('0' + m[1]).slice(-2) + '-' + ('0' + m[2]).slice(-2);
    }
    var MON = { jan: 1, feb: 2, mar: 3, apr: 4, may: 5, jun: 6, jul: 7, aug: 8, sep: 9, oct: 10, nov: 11, dec: 12 };
    m = s.match(/([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2}),?\s+(\d{4})/);
    if (m && MON[m[1].toLowerCase()]) return m[3] + '-' + ('0' + MON[m[1].toLowerCase()]).slice(-2) + '-' + ('0' + m[2]).slice(-2);
    return '';
  }

  function lossType(s) {
    s = String(s || '').toLowerCase();
    if (!s) return '';
    var hail = /hail/.test(s), wind = /wind|storm|hurricane|tornado|weather/.test(s);
    if (hail && wind) return 'Hail & Wind';
    if (hail) return 'Hail';
    if (wind) return 'Wind';
    if (/water|plumb|pipe|leak|sewer|drain|appliance|overflow|flood/.test(s)) return 'Water / Plumbing';
    if (/fire|smoke|lightning/.test(s)) return 'Fire / Smoke';
    if (/freez|ice|snow/.test(s)) return 'Freeze';
    if (/tree|impact|fall|vehicle|collapse/.test(s)) return 'Tree / Impact';
    return 'Other';
  }

  function phone(s) {
    var m = String(s || '').match(/\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}/);
    return m ? m[0] : '';
  }

  function emailOf(s) {
    var m = String(s || '').match(/[\w.+-]+@[\w-]+(\.[\w-]+)+/);
    return m ? m[0] : '';
  }

  function carrierFromText(s) {
    for (var i = 0; i < CARRIERS.length; i++) if (CARRIERS[i][1].test(s)) return CARRIERS[i][0];
    return '';
  }

  function carrierFromEmail(e) {
    var d = String(e || '').toLowerCase().split('@')[1] || '';
    var keys = Object.keys(EMAIL_CARRIERS);
    for (var i = 0; i < keys.length; i++) if (d === keys[i] || d.slice(-keys[i].length - 1) === '.' + keys[i]) return EMAIL_CARRIERS[keys[i]];
    return '';
  }

  function parse(text) {
    var lines = String(text || '').split(/\r?\n/).map(clean).filter(Boolean);
    var f = {}, found = [];
    var section = 'insured';          // insured | rep | estimator
    var repEmails = [], insuredEmails = [], companies = [], propertyIdx = -1, propertyRaw = '';

    for (var i = 0; i < lines.length && i < 120; i++) {
      var pairs = splitLabels(lines[i]);
      for (var j = 0; j < pairs.length; j++) {
        var key = labelKey(pairs[j].label), v = pairs[j].value;
        if (!key) continue;
        if (key === 'claimRep') { section = 'rep'; continue; }
        if (key === 'estimator') { section = 'estimator'; continue; }
        if (key === 'insuredName') { if (!f.insuredName && v) f.insuredName = personName(v); section = 'insured'; continue; }
        if (key === 'property') { if (!propertyRaw && v) { propertyRaw = v; propertyIdx = i; } continue; }
        if (key === 'homePhone' || key === 'cellPhone') {
          if (section === 'insured' && phone(v)) { if (key === 'cellPhone' || !f.insuredPhone) f.insuredPhone = phone(v); }
          continue;
        }
        if (key === 'email') { var e = emailOf(v); if (e) (section === 'insured' ? insuredEmails : repEmails).push(e); continue; }
        if (key === 'company') { if (v) companies.push({ section: section, value: v }); continue; }
        if (key === 'claimNumber') { if (!f.claimNumber && v && /\w/.test(v)) f.claimNumber = v.replace(/\s+(policy|type|date).*$/i, ''); continue; }
        if (key === 'policyNumber') { if (!f.policyNumber && v && /\w/.test(v)) f.policyNumber = v; continue; }
        if (key === 'lossType') { if (!f.lossTypeRaw && v) f.lossTypeRaw = v; continue; }
        if (key === 'dateOfLoss') { if (!f.dateOfLoss) { var d = parseDate(v); if (d) f.dateOfLoss = d; } continue; }
      }
    }

    // Property may be split across lines: "Property: 123 Main St" / "Houston, TX 77002".
    if (propertyRaw) {
      var addr = splitAddress(propertyRaw);
      if (!addr && propertyIdx >= 0) {
        for (var k = propertyIdx + 1; k <= propertyIdx + 3 && k < lines.length && !addr; k++) {
          var cand = lines[k];
          var p = splitLabels(cand);
          if (p.length && p[0].index === 0) break;                // next labelled line, stop
          if (p.length) cand = cand.slice(0, p[0].index);          // trailing label on same line
          addr = splitAddress(propertyRaw + ', ' + clean(cand));
        }
      }
      if (addr) { f.street = addr.street; f.city = addr.city; f.state = addr.state; f.zip = addr.zip; }
      else if (/\d/.test(propertyRaw)) f.street = titleCase(propertyRaw);
    }

    if (insuredEmails.length) f.insuredEmail = insuredEmails[0];

    // Carrier: explicit company label on the rep/insured block, then known-name scan, then rep e-mail domain.
    var carrier = '';
    for (var c = 0; c < companies.length && !carrier; c++) {
      if (companies[c].section !== 'estimator') carrier = carrierFromText(companies[c].value) || clean(companies[c].value);
    }
    if (!carrier) carrier = carrierFromText(lines.slice(0, 25).join('\n'));
    for (var r = 0; r < repEmails.length && !carrier; r++) carrier = carrierFromEmail(repEmails[r]);
    if (carrier) f.carrier = carrier;

    if (f.lossTypeRaw) { f.lossType = lossType(f.lossTypeRaw); delete f.lossTypeRaw; }

    Object.keys(f).forEach(function (k) { if (f[k]) found.push(k); else delete f[k]; });
    return { fields: f, found: found };
  }

  return { parse: parse, splitAddress: splitAddress, parseDate: parseDate, lossType: lossType, splitLabels: splitLabels };
}));
