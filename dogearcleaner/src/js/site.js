/* dogearcleaner.com — mobile nav, contact form status, and the four interactive tools. */
(function () {
  'use strict';

  // ---------- mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ---------- contact form result (?sent=1 / ?error=...)
  var status = document.getElementById('form-status');
  if (status) {
    var q = new URLSearchParams(location.search);
    if (q.get('sent') === '1') {
      status.textContent = 'Thanks! Your message has been sent. We usually reply within a few days.';
      status.className = 'form-status ok'; status.hidden = false;
    } else if (q.get('error')) {
      status.textContent = 'Sorry, your message could not be sent. Please check the form and try again.';
      status.className = 'form-status err'; status.hidden = false;
    }
  }

  // ---------- helpers
  var products = {};
  var dataEl = document.getElementById('dec-products');
  if (dataEl) { try { products = JSON.parse(dataEl.textContent); } catch (e) { products = {}; } }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); }
  function val(form, name) { var el = form.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : null; }
  function all(form, name) { return Array.prototype.map.call(form.querySelectorAll('input[name="' + name + '"]:checked'), function (e) { return e.value; }); }
  function productCard(key, label) {
    var p = products[key]; if (!p) return '';
    return '<div class="product-card">' + (label ? '<span class="pc-brand">' + esc(label) + '</span>' : '') +
      '<p class="pc-name">' + esc(p.name) + '</p><p class="pc-best">' + esc(p.best) + '</p>' +
      '<div class="pc-actions"><a class="btn-amazon" href="' + p.url + '" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a>' +
      (p.review ? '<a class="pc-review" href="' + p.review + '">Read our review</a>' : '') + '</div></div>';
  }
  function show(tool, html, level) {
    var out = tool.querySelector('.tool-result');
    out.className = 'tool-result' + (level ? ' level-' + level : '');
    out.innerHTML = html; out.hidden = false;
    var r = out.getBoundingClientRect();
    if (r.top > window.innerHeight - 80 || r.top < 0) out.scrollIntoView({behavior: 'smooth', block: 'nearest'});
  }

  // ---------- 1. cleaning schedule
  function schedule(tool, form) {
    var ears = val(form, 'ears'), water = val(form, 'water'), allergy = val(form, 'allergy'),
        wax = val(form, 'wax'), history = val(form, 'history');
    if (wax === 'sore') {
      show(tool, '<h3>See your vet before starting a routine</h3><p>Red, sore ears or discharge can mean an active infection, and cleaning can sting or wash away what your vet needs to sample. Once your vet has treated the ear, come back for a maintenance schedule.</p>' +
        '<p><a href="/tools/ear-symptom-checker/">Check the symptoms</a> &middot; <a href="/ear-infection-signs/">Ear infection signs</a></p>', 'red');
      return;
    }
    var score = {upright: 0, semi: 1, floppy: 2, hairy: 2}[ears] + {rare: 0, monthly: 1, weekly: 2}[water] +
      {none: 0, seasonal: 1, chronic: 2}[allergy] + {clean: 0, some: 1, heavy: 2}[wax] + {'0': 0, '1': 1, '2': 2}[history];
    var plan;
    if (score <= 1) plan = {days: 28, label: 'Every 4 weeks', note: 'Check weekly; clean roughly once a month or whenever you see wax.'};
    else if (score <= 3) plan = {days: 14, label: 'Every 2 weeks', note: 'A light clean every other week keeps wax from building up.'};
    else if (score <= 6) plan = {days: 7, label: 'Once a week', note: 'Weekly cleaning suits dogs whose ears trap moisture or wax.'};
    else plan = {days: 4, label: 'Twice a week', note: 'High-risk ears benefit from a twice-weekly clean. If infections keep coming back, ask your vet about the cause (often allergies).'};
    var extras = [];
    if (water !== 'rare') extras.push('Clean with a drying cleaner after every swim or bath, even between scheduled cleans.');
    if (ears === 'hairy') extras.push('Ask your groomer or vet whether hair in the canal should be trimmed; don\'t pluck at home unless advised.');
    if (allergy === 'seasonal') extras.push('Step up to the next frequency during allergy season.');
    if (wax === 'heavy') extras.push('Heavy wax or a smell: if it hasn\'t improved after two weeks of cleaning, see your vet.');
    var pick = (wax === 'heavy') ? 'zymox-cleanser' : (water !== 'rare' ? 'epi-otic' : (allergy !== 'none' ? 'vetericyn-plus' : 'epi-otic'));
    var dates = [], d = new Date();
    for (var i = 0; i < 8; i++) { d = new Date(d.getTime() + plan.days * 864e5); dates.push(new Date(d)); }
    var fmt = function (x) { return x.toLocaleDateString(undefined, {weekday: 'short', month: 'short', day: 'numeric'}); };
    tool._dates = dates; tool._label = plan.label;
    show(tool, '<h3>Recommended: clean ' + plan.label.toLowerCase() + '</h3><span class="big-num">' + plan.label + '</span><p>' + plan.note + '</p>' +
      (extras.length ? '<ul><li>' + extras.join('</li><li>') + '</li></ul>' : '') +
      '<p><strong>Your next cleaning dates:</strong></p><ul class="date-list"><li>' + dates.map(fmt).join('</li><li>') + '</li></ul>' +
      '<p><button type="button" class="btn-ghost js-ics">Add these dates to my calendar (.ics)</button></p>' +
      '<p><strong>Suggested cleaner for this routine:</strong></p>' + productCard(pick), 'green');
  }
  function downloadIcs(tool) {
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    var day = function (x) { return x.getFullYear() + pad(x.getMonth() + 1) + pad(x.getDate()); };
    var lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Dog Ear Cleaner//Ear Cleaning Schedule//EN'];
    tool._dates.forEach(function (x, i) {
      var next = new Date(x.getTime() + 864e5);
      lines.push('BEGIN:VEVENT', 'UID:dec-' + day(x) + '-' + i + '@dogearcleaner.com', 'DTSTAMP:' + day(new Date()) + 'T000000Z',
        'DTSTART;VALUE=DATE:' + day(x), 'DTEND;VALUE=DATE:' + day(next), 'SUMMARY:Clean my dog\'s ears',
        'DESCRIPTION:Ear cleaning schedule (' + tool._label + ') from dogearcleaner.com. Check ears first; skip and call the vet if they look red or sore.', 'END:VEVENT');
    });
    lines.push('END:VCALENDAR');
    var blob = new Blob([lines.join('\r\n')], {type: 'text/calendar'});
    var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'dog-ear-cleaning-schedule.ics';
    document.body.appendChild(a); a.click(); setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  // ---------- 2. symptom checker
  function symptoms(tool, form) {
    var s = all(form, 's');
    if (!s.length) { show(tool, '<p>Tick at least one thing you have noticed, or if the ears look and smell normal, see <a href="/cleaning-routines/">our routine care guide</a>.</p>'); return; }
    var has = function (k) { return s.indexOf(k) > -1; };
    var red = ['tilt', 'eyes', 'deaf', 'blood', 'flap', 'pain'].filter(has);
    var amber = ['odor', 'dark', 'pus', 'red', 'swelcanal', 'coffee'].filter(has);
    var hints = [];
    if (has('coffee')) hints.push('Dry, crumbly "coffee grounds" debris is a classic sign of <strong>ear mites</strong>, especially in puppies or multi-pet homes. Mites need a vet-prescribed treatment for every pet in the house.');
    if (has('dark') && has('odor')) hints.push('Brown, greasy wax with a musty or yeasty smell often points to <strong>yeast (Malassezia)</strong>.');
    if (has('pus')) hints.push('Yellow or green discharge with a foul smell is more typical of a <strong>bacterial infection</strong>.');
    if (has('outdoor') && (has('shake') || has('pain'))) hints.push('Sudden, violent head shaking after a walk through long grass can mean a <strong>grass awn (foxtail)</strong> in the canal. Don\'t flush it; a vet needs to remove it.');
    if (has('flap')) hints.push('A puffy, fluid-filled ear flap is usually an <strong>aural hematoma</strong>, caused by shaking. It needs a vet and treatment of whatever is making the ear itch.');
    if (has('swim')) hints.push('Problems after water exposure suggest trapped moisture. Once your vet has ruled out infection, a drying cleaner after swims helps prevent repeats.');
    var hintHtml = hints.length ? '<p><strong>What these signs can point to:</strong></p><ul><li>' + hints.join('</li><li>') + '</li></ul>' : '';
    if (red.length) {
      show(tool, '<h3>See a vet today</h3><p>One or more of the signs you ticked (balance problems, eye flicking, facial drooping, bleeding, a swollen ear flap, sudden deafness or severe pain) can mean a middle or inner ear problem, a ruptured eardrum or a hematoma. <strong>Don\'t put any cleaner in the ear.</strong> Call your vet or an emergency clinic.</p>' + hintHtml +
        '<p><a href="/ear-infection-signs/">Read about serious ear infection signs</a></p>', 'red');
    } else if (amber.length || (has('scratch') && has('shake'))) {
      show(tool, '<h3>Book a vet visit in the next few days</h3><p>These signs suggest an outer ear infection (otitis externa) or mites. A vet will look down the canal and check a swab under the microscope to find out whether it\'s yeast, bacteria or mites, which decides the treatment. <strong>Don\'t clean the ear right before the appointment</strong>, because it can wash away what they need to sample.</p>' + hintHtml +
        '<p>Once it\'s treated, a gentle routine keeps it from coming back. See <a href="/cleaning-routines/">dog ear cleaning routines</a>.</p>', 'amber');
    } else {
      show(tool, '<h3>Sounds like routine home care</h3><p>Light wax and the occasional scratch or shake are normal. A gentle clean should help. Follow our <a href="/how-to-clean-dog-earss-matters/">step-by-step ear cleaning guide</a>, then recheck in a week. If it isn\'t better, or a smell, redness or discharge appears, see your vet.</p>' + hintHtml +
        productCard(has('swim') ? 'epi-otic' : 'vetericyn-plus', 'A gentle cleaner to start with'), 'green');
    }
  }

  // ---------- 3. ear cleaner finder
  function finder(tool, form) {
    var goal = val(form, 'goal'), format = val(form, 'format'), budget = val(form, 'budget'),
        natural = val(form, 'natural'), size = val(form, 'size');
    var scores = {};
    Object.keys(products).forEach(function (k) {
      var t = products[k].tags, sc = 0;
      var hasT = function (x) { return t.indexOf(x) > -1; };
      if (hasT('treatment')) { sc -= 4; }  // finder recommends cleaners, not medicated drops
      if (k === 'epi-otic-8oz') sc -= 1;   // shown as size upgrade instead
      if (format === 'wipes') sc += hasT('wipes') ? 6 : -4;
      if (format === 'liquid') sc += hasT('wipes') ? -6 : 1;
      if (goal === 'routine') sc += (hasT('alcohol-free') ? 2 : 0) + (hasT('vet-brand') ? 2 : 0) + (k === 'epi-otic' ? 2 : 0);
      if (goal === 'smelly') sc += (hasT('enzymatic') ? 4 : 0) + (hasT('drying') ? 2 : 0) + (hasT('tris-edta') ? 2 : 0);
      if (goal === 'itchy') sc += (hasT('aloe') ? 3 : 0) + (hasT('gentle') ? 2 : 0) + (hasT('no-sting') ? 2 : 0) + (k === 'pet-honesty' ? 1 : 0);
      if (goal === 'sensitive') sc += (hasT('no-sting') ? 5 : 0) + (hasT('gentle') ? 2 : 0) - (hasT('scented') ? 2 : 0);
      if (goal === 'swim') sc += (hasT('drying') ? 5 : 0) + (hasT('alcohol-free') ? 1 : 0);
      if (budget === 'value') sc += hasT('budget') ? 3 : 0;
      if (budget === 'any') sc += hasT('vet-brand') ? 1 : 0;
      if (natural === 'yes') sc += (hasT('natural') || hasT('probiotic') ? 4 : 0) + (hasT('aloe') ? 2 : 0) + (hasT('enzymatic') ? 1 : 0) - (hasT('hydrocortisone') ? 5 : 0);
      if (products[k].review) sc += 0.5;
      scores[k] = sc;
    });
    var ranked = Object.keys(scores).sort(function (a, b) { return scores[b] - scores[a]; });
    var top = ranked.slice(0, 2);
    if (size === 'large' && top[0] === 'epi-otic') top[0] = 'epi-otic-8oz';
    var why = {
      routine: 'gentle, alcohol-free cleaners made for regular maintenance',
      smelly: 'cleaners that break down wax and help with odor',
      itchy: 'soothing, low-irritation formulas for allergy-prone ears',
      sensitive: 'no-sting, fragrance-light formulas for tender ears',
      swim: 'cleaners with drying agents to pull out trapped water'
    }[goal];
    show(tool, '<h3>Your best matches</h3><p>Based on your answers we looked for ' + why + (format === 'wipes' ? ', in wipe form' : '') + '.</p>' +
      productCard(top[0], 'Top match') + productCard(top[1], 'Runner-up') +
      (goal === 'itchy' || goal === 'sensitive' ? '<p class="small">If the ear is red, hot, smelly or painful, see a vet before using any cleaner. <a href="/tools/ear-symptom-checker/">Check symptoms</a>.</p>' : '') +
      '<p><a href="/best-dog-ear-cleaner/">Compare all our top picks &rarr;</a></p>', 'green');
  }

  // ---------- 4. dose / bottle calculator
  function mlPerEar(lb) {
    if (lb < 10) return [1, 2];
    if (lb < 25) return [2, 4];
    if (lb < 50) return [4, 6];
    if (lb < 90) return [6, 8];
    return [8, 10];
  }
  function bottle(tool, form) {
    var lb = +form.querySelector('input[name="weight"]').value;
    var freq = +val(form, 'freq'), ears = +val(form, 'ears'), ml = +val(form, 'bottle');
    var r = mlPerEar(lb), avg = (r[0] + r[1]) / 2;
    var perWeek = avg * ears * freq, weeks = ml / perWeek, cleans = Math.floor(ml / (avg * ears));
    var dur = weeks >= 8 ? Math.round(weeks / 4.345) + ' months' : Math.round(weeks) + ' weeks';
    var size = lb < 25 ? 'toy or small' : lb < 50 ? 'medium' : lb < 90 ? 'large' : 'giant';
    var suggestion = (weeks < 6) ? '<p>You\'ll go through bottles quickly. A bigger size usually costs less per ounce: ' +
      '<a class="aff" href="' + (products['epi-otic-8oz'] || {}).url + '" rel="nofollow sponsored noopener" target="_blank">Epi-Otic 8 oz</a> or ' +
      '<a class="aff" href="' + (products['petmd-tris-flush'] || {}).url + '" rel="nofollow sponsored noopener" target="_blank">Pet MD Tris Flush 12 oz</a>.</p>'
      : (weeks > 52 ? '<p>This bottle will outlast most expiry dates. A smaller size may be better value. Check the date on the label.</p>' : '');
    show(tool, '<h3>About ' + r[0] + '&ndash;' + r[1] + ' mL per ear</h3><p>For a ' + lb + ' lb (' + size + ') dog, fill the canal until you can see liquid at the opening. That\'s roughly ' + r[0] + '&ndash;' + r[1] + ' mL. Follow your product\'s label first.</p>' +
      '<div class="result-stats"><div><span class="lbl">Per cleaning</span><span class="big-num">' + Math.round(avg * ears) + ' mL</span></div>' +
      '<div><span class="lbl">Cleanings per bottle</span><span class="big-num">~' + cleans + '</span></div>' +
      '<div><span class="lbl">Bottle lasts</span><span class="big-num">~' + dur + '</span></div></div>' + suggestion, 'green');
  }

  var handlers = {schedule: schedule, symptoms: symptoms, finder: finder, bottle: bottle};
  Array.prototype.forEach.call(document.querySelectorAll('[data-tool]'), function (tool) {
    var form = tool.querySelector('form'), kind = tool.getAttribute('data-tool');
    form.addEventListener('submit', function (e) { e.preventDefault(); handlers[kind](tool, form); });
    var range = form.querySelector('input[type="range"]');
    if (range) {
      var out = form.querySelector('.range-out');
      range.addEventListener('input', function () { out.textContent = range.value + ' lb'; });
    }
    tool.addEventListener('click', function (e) { if (e.target.classList.contains('js-ics')) downloadIcs(tool); });
  });
})();
