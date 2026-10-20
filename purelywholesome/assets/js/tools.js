/* Purely Wholesome Farm - interactive tools. Each <section data-tool="slug"> is wired up here. */
(function () {
  'use strict';

  // ---------- helpers ----------
  const $ = (root, sel) => root.querySelector(sel);
  const out = (root, key) => root.querySelector('[data-out="' + key + '"]');
  const set = (root, key, html) => { const el = out(root, key); if (el) el.innerHTML = html; };
  const val = (form, name) => {
    const el = form.elements[name];
    if (!el) return null;
    if (el instanceof RadioNodeList) return el.value;
    if (el.type === 'checkbox') return el.checked;
    return el.value;
  };
  const round = (n, d = 0) => { const f = Math.pow(10, d); return Math.round(n * f) / f; };
  const fToC = (f) => (f - 32) * 5 / 9;
  const cToF = (c) => c * 9 / 5 + 32;
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // Kitchen fractions: nearest 1/8, 1/4, 1/3, 1/2 ...
  function fraction(n) {
    if (n <= 0) return '0';
    const whole = Math.floor(n + 1e-9);
    const rest = n - whole;
    const options = [[0, ''], [1 / 8, '⅛'], [1 / 4, '¼'], [1 / 3, '⅓'], [3 / 8, '⅜'], [1 / 2, '½'], [5 / 8, '⅝'], [2 / 3, '⅔'], [3 / 4, '¾'], [7 / 8, '⅞'], [1, '']];
    let best = options[0];
    for (const o of options) if (Math.abs(o[0] - rest) < Math.abs(best[0] - rest)) best = o;
    const w = best[0] === 1 ? whole + 1 : whole;
    if (!w && !best[1]) return '⅛';
    return (w ? String(w) : '') + best[1];
  }

  // Express a weight of salt as cups / tablespoons / teaspoons of that salt.
  function volume(grams, gPerTsp) {
    const tsp = grams / gPerTsp;
    if (tsp >= 12) return fraction(tsp / 48) + ' cup' + (tsp / 48 > 1.05 ? 's' : '');
    if (tsp >= 3) return fraction(tsp / 3) + ' tbsp';
    return fraction(tsp) + ' tsp';
  }

  function hours(h) {
    if (h < 1) return Math.round(h * 60) + ' min';
    if (h >= 48) return round(h / 24, 1) + ' days';
    return round(h, 1) + ' hr';
  }

  function bind(root, fn) {
    const form = $(root, 'form');
    const run = () => fn(root, form);
    form.addEventListener('input', run);
    form.addEventListener('change', run);
    run();
    return run;
  }

  // ---------- Brine calculator ----------
  const SALTS = { // grams per teaspoon
    diamond: [2.8, 'Diamond Crystal kosher salt'], morton: [4.8, 'Morton kosher salt'], table: [5.9, 'table salt'],
    sea: [5.0, 'fine sea salt'], coarse: [4.0, 'coarse sea salt'],
  };
  const CUTS = { // brining window in hours at a 5% brine
    breast: [0.5, 1.5, 'Longer turns boneless meat spongy.'], pieces: [1.5, 3, ''], whole: [4, 8, ''],
    spatch: [2, 4, ''], turkeybreast: [4, 6, ''], turkey: [10, 16, 'Use a cooler with ice packs if it won’t fit in the fridge.'],
    chops: [1, 3, ''], shoulder: [8, 12, ''],
    brisket: [12, 24, 'For corned beef you need a curing brine with pink curing salt #1 and 5-7 days. See our brisket guide.'],
  };
  const brine = (root, form) => {
    const water = parseFloat(val(form, 'water')) || 0;
    const ml = water * parseFloat(val(form, 'unit'));
    const pct = parseFloat(val(form, 'strength'));
    form.elements.strengthOut.value = pct + '%';
    const [gPerTsp, saltName] = SALTS[val(form, 'salt')];
    const saltG = ml * pct / 100;
    set(root, 'salt', volume(saltG, gPerTsp));
    set(root, 'saltg', round(saltG) + ' g of ' + saltName);
    if (val(form, 'sugar')) {
      const sugarG = saltG / 2;
      set(root, 'sugar', volume(sugarG, 4.2));
      set(root, 'sugarg', round(sugarG) + ' g white or brown sugar');
    } else {
      set(root, 'sugar', 'None'); set(root, 'sugarg', 'Salt-only brine');
    }
    const [lo, hi, note] = CUTS[val(form, 'cut')];
    const k = 5 / pct;
    set(root, 'time', hours(lo * k) + ' – ' + hours(hi * k));
    set(root, 'timenote', pct === 5 ? 'Classic 5% brine' : 'Adjusted for a ' + pct + '% brine');
    out(root, 'gauge').style.width = ((pct - 2) / 6 * 100) + '%';
    let msg = pct <= 3 ? 'A gentle brine: forgiving if you brine longer, great for overnight turkey.' : pct >= 7 ? 'A strong, quick brine: set a timer, it gets salty fast.' : 'A classic all-purpose brine.';
    if (note) msg += ' ' + note;
    set(root, 'note', msg);
  };

  // ---------- Lamb cooking calculator ----------
  const DONE = { rare: [125, 'Rare'], mr: [135, 'Medium-rare'], m: [145, 'Medium'], mw: [150, 'Medium-well'], w: [160, 'Well done'] };
  const LAMB = {
    chops: { carry: 3, rest: '5 min', time: { rare: 2.5, mr: 3.5, m: 4.5, mw: 5.5, w: 6.5 }, unit: 'side' },
    thick: { carry: 4, rest: '5-8 min', time: { rare: 4, mr: 5, m: 6, mw: 7, w: 8 }, unit: 'side', note: 'Sear 2 minutes per side, then finish in a 400°F oven.' },
    lollipops: { carry: 3, rest: '3-5 min', time: { rare: 2, mr: 2.5, m: 3, mw: 3.5, w: 4 }, unit: 'side' },
    rack: { carry: 5, rest: '10 min', time: { rare: 12, mr: 17, m: 22, mw: 25, w: 30 }, unit: 'oven', note: 'Sear fat-side down first, then roast at 425°F.' },
    legbone: { carry: 8, rest: '15-20 min', perLb: { rare: 18, mr: 22, m: 26, mw: 28, w: 30 } },
    legboneless: { carry: 8, rest: '15-20 min', perLb: { rare: 23, mr: 27, m: 31, mw: 33, w: 35 } },
    shoulder: { slow: true, rest: '20-30 min' },
  };
  const lamb = (root, form) => {
    const cut = LAMB[val(form, 'cut')];
    const w = parseFloat(val(form, 'weight'));
    form.elements.weightOut.value = w + ' lb';
    root.querySelector('[data-weight]').hidden = !(cut.perLb || cut.slow);
    root.querySelector('[data-doneness]').disabled = !!cut.slow;
    const mercury = out(root, 'mercury');
    if (cut.slow) {
      set(root, 'pull', '195-205°F'); set(root, 'pullc', '90-96°C, fork-tender');
      set(root, 'final', 'Pull-apart'); set(root, 'rest', 'Rest ' + cut.rest);
      const lo = Math.round(w * 40 / 15) * 15, hi = Math.round(w * 55 / 15) * 15;
      set(root, 'time', hours(lo / 60) + ' – ' + hours(hi / 60)); set(root, 'timenote', 'Covered, at 300°F');
      set(root, 'note', 'Shoulder is cooked past “doneness” on purpose: the connective tissue needs time to melt.');
      mercury.style.height = '100%';
      return;
    }
    const d = val(form, 'done');
    const [final, label] = DONE[d];
    const pull = final - cut.carry;
    set(root, 'pull', pull + '°F'); set(root, 'pullc', round(fToC(pull)) + '°C');
    set(root, 'final', final + '°F'); set(root, 'rest', label + ' · rest ' + cut.rest);
    if (cut.perLb) {
      const m = cut.perLb[d] * w;
      set(root, 'time', hours((m - 10) / 60) + ' – ' + hours((m + 10) / 60)); set(root, 'timenote', 'At 325°F, about ' + cut.perLb[d] + ' min/lb');
    } else if (cut.unit === 'side') {
      set(root, 'time', cut.time[d] + ' min'); set(root, 'timenote', 'per side, medium-high heat');
    } else {
      set(root, 'time', cut.time[d] + ' min'); set(root, 'timenote', 'in the oven after searing');
    }
    let note = cut.note ? cut.note + ' ' : '';
    if (final < 145) note += 'USDA’s minimum for whole cuts of lamb is 145°F with a 3-minute rest; lower temperatures are a personal choice.';
    set(root, 'note', note);
    mercury.style.height = Math.min(100, (final - 100) / 65 * 100) + '%';
  };

  // ---------- Lamb plate builder ----------
  const PLATE = {
    starch: {
      spring: ['Lemon-herb new potatoes', 'Minted pea and orzo salad', 'Herbed couscous'],
      summer: ['Grilled corn with herb butter', 'Lemony orzo salad', 'Smashed baby potatoes'],
      fall: ['Garlic and rosemary roasted potatoes', 'Creamy polenta', 'Wild rice pilaf'],
      winter: ['Garlic mashed potatoes', 'Potato gratin', 'Roasted root vegetable mash'],
    },
    veg: {
      spring: ['Grilled asparagus with lemon zest', 'Buttered spring peas with mint', 'Roasted baby carrots'],
      summer: ['Charred zucchini ribbons', 'Grilled eggplant with tahini', 'Blistered green beans'],
      fall: ['Honey-roasted carrots and parsnips', 'Roasted Brussels sprouts', 'Roasted golden beets'],
      winter: ['Garlicky sautéed spinach', 'Braised red cabbage', 'Roasted butternut squash'],
    },
    bright: {
      spring: ['Cucumber-yogurt tzatziki', 'Radish and herb salad'],
      summer: ['Watermelon, feta and mint salad', 'Tomato and burrata salad'],
      fall: ['Apple and fennel slaw', 'Pomegranate and arugula salad'],
      winter: ['Citrus and shaved fennel salad', 'Quick pickled red onions'],
    },
    sauce: {
      weeknight: [['Classic mint sauce', '/mint-sauce-for-lamb/'], ['Garlic-yogurt sauce', '/best-sauce-for-lamb-chops/']],
      party: [['Red wine pan sauce', '/lamb-chop-sauces/'], ['Romesco', '/romesco-sauce-recipe/']],
      grill: [['Chimichurri-style herb sauce', '/lamb-chop-sauces/'], ['Mint-tomato sauce', '/mint-tomato-sauce-for-lamb/']],
      holiday: [['Lamb gravy from the pan', '/lamb-gravy-turning-every-roast-into-magic/'], ['Mint-tomato sauce', '/mint-tomato-sauce-for-lamb/']],
    },
    wine: { weeknight: 'Côtes du Rhône', party: 'Rioja or Bordeaux', grill: 'Zinfandel or Malbec', holiday: 'Syrah or Cabernet Sauvignon' },
  };
  const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
  const plate = (root, form) => {
    const s = val(form, 'season'), st = val(form, 'style');
    const items = [
      ['Starch', pick(PLATE.starch[s])], ['Vegetable', pick(PLATE.veg[s])], ['Something bright', pick(PLATE.bright[s])],
    ];
    const sauce = pick(PLATE.sauce[st]);
    const main = st === 'holiday' ? 'Herb-crusted rack or roast leg of lamb' : st === 'grill' ? 'Grilled lamb chops' : st === 'party' ? 'Frenched lamb lollipops' : 'Pan-seared lamb chops';
    const mainUrl = st === 'holiday' ? '/roasted-lamb-leg/' : st === 'party' ? '/how-chefs-plate-lamb-lollipops/' : '/pan-seared-lamb-chops/';
    set(root, 'plate',
      '<div class="plate__center"><span>The main</span><a href="' + mainUrl + '">' + esc(main) + '</a></div>' +
      '<ul class="plate__ring">' + items.map((i, n) => '<li style="--i:' + n + '"><span>' + i[0] + '</span>' + esc(i[1]) + '</li>').join('') +
      '<li style="--i:3"><span>Sauce</span><a href="' + sauce[1] + '">' + esc(sauce[0]) + '</a></li></ul>' +
      '<p class="plate__wine">🍷 Pour a ' + esc(PLATE.wine[st]) + '</p>');
  };

  // ---------- Goat gestation ----------
  const fmtDate = (d) => d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' });
  const addDays = (d, n) => { const x = new Date(d); x.setDate(x.getDate() + n); return x; };
  const gestation = (root, form) => {
    const input = form.elements.bred;
    if (!input.value) {
      const d = new Date(); d.setDate(d.getDate() - 60);
      input.value = d.toISOString().slice(0, 10);
    }
    const bred = new Date(input.value + 'T12:00:00');
    const days = parseInt(val(form, 'breed'), 10);
    const name = (val(form, 'doe') || '').trim() || 'your doe';
    const due = addDays(bred, days);
    const today = new Date(); today.setHours(12, 0, 0, 0);
    const left = Math.round((due - today) / 864e5);
    const along = Math.round((today - bred) / 864e5);
    set(root, 'due', fmtDate(due));
    set(root, 'window', 'Likely between ' + fmtDate(addDays(due, -5)) + ' and ' + fmtDate(addDays(due, 5)));
    if (left > 0) { set(root, 'count', left + ' days'); set(root, 'countnote', 'Day ' + Math.max(0, along) + ' of about ' + days); }
    else if (left > -6) { set(root, 'count', 'Any day now'); set(root, 'countnote', 'Watch ' + esc(name) + ' closely'); }
    else { set(root, 'count', 'Past due'); set(root, 'countnote', 'More than 5 days over: call your vet'); }
    const pct = Math.max(0, Math.min(100, along / days * 100));
    out(root, 'bar').style.width = pct + '%';
    set(root, 'barlabel', Math.round(pct) + '%');
    const steps = [
      [0, 'Bred', 'Note the date and the buck. If the buck ran with the herd, this is his first day in.'],
      [19, 'Watch for heat', 'If ' + esc(name) + ' comes back into heat around days 18-21, she probably didn’t settle.'],
      [30, 'Confirm pregnancy', 'A blood pregnancy test is reliable from about day 30; ultrasound from around day 40.'],
      [days - 60, 'Dry off', 'If she’s in milk, dry her off about two months before kidding.'],
      [days - 42, 'Feed for the last trimester', 'Most kid growth happens now. Raise nutrition gradually: good hay, minerals and, if needed, a little grain.'],
      [days - 30, 'CD&T booster', 'Most vets give the pre-kidding CD&T booster about 4 weeks out so kids get antibodies through colostrum.'],
      [days - 14, 'Kidding kit & pen', 'Clean, bedded kidding pen; towels, iodine, gloves, colostrum and a thermometer on hand.'],
      [days - 7, 'Daily checks', 'Feel the tail ligaments, watch the udder fill and look for restlessness or loss of appetite.'],
      [days, 'Due date', 'Most does kid within five days either side of this date.'],
    ];
    set(root, 'timeline', steps.map(([d, t, txt]) => {
      const date = addDays(bred, d);
      const state = date < today ? 'done' : (Math.abs((date - today) / 864e5) < 8 ? 'now' : '');
      return '<li class="' + state + '"><time>' + date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) + '</time><strong>' + t + '</strong><p>' + txt + '</p></li>';
    }).join(''));
    root.dataset.due = due.toISOString().slice(0, 10);
    root.dataset.doe = name;
  };
  function icsDownload(root) {
    const due = (root.dataset.due || '').replace(/-/g, '');
    if (!due) return;
    const end = new Date(root.dataset.due + 'T12:00:00'); end.setDate(end.getDate() + 1);
    const ics = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Purely Wholesome Farm//Goat Due Date//EN', 'BEGIN:VEVENT',
      'UID:' + due + '-' + Date.now() + '@purelywholesome.com', 'DTSTAMP:' + new Date().toISOString().replace(/[-:]/g, '').slice(0, 15) + 'Z',
      'DTSTART;VALUE=DATE:' + due, 'DTEND;VALUE=DATE:' + end.toISOString().slice(0, 10).replace(/-/g, ''),
      'SUMMARY:Kidding due: ' + root.dataset.doe, 'DESCRIPTION:Expected kidding date (±5 days). Calculated at purelywholesome.com/tools/goat-gestation-calculator/',
      'BEGIN:VALARM', 'TRIGGER:-P7D', 'ACTION:DISPLAY', 'DESCRIPTION:Kidding in about a week', 'END:VALARM', 'END:VEVENT', 'END:VCALENDAR'].join('\r\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' }));
    a.download = 'kidding-due-date.ics';
    document.body.appendChild(a); a.click(); a.remove();
  }

  // ---------- Goat temperature ----------
  const goatTemp = (root, form) => {
    let t = parseFloat(val(form, 'temp'));
    const unit = val(form, 'unit');
    const status = out(root, 'status');
    if (isNaN(t)) { set(root, 'headline', 'Enter a reading'); set(root, 'advice', ''); return; }
    const f = unit === 'C' ? cToF(t) : t;
    const kid = val(form, 'age') === 'kid';
    const hot = val(form, 'hot');
    const top = 103.5 + (kid ? 0.5 : 0) + (hot ? 0.5 : 0);
    let cls, head, advice;
    if (f < 100) { cls = 'danger'; head = 'Dangerously low'; advice = (kid ? 'A chilled kid can’t suckle or digest. ' : '') + 'Warm the goat now (warm towels, a heat source out of reach, warm-water bottle for kids) and call your vet. A low temperature can mean hypothermia, shock or advanced illness.'; }
    else if (f < 101.5) { cls = 'warn'; head = 'Below normal'; advice = 'Recheck in 30 minutes with a well-lubricated thermometer held until it beeps. If it stays low, or the goat is off feed or not chewing cud, call your vet.'; }
    else if (f <= top) { cls = 'ok'; head = 'Normal'; advice = 'That’s a healthy reading. If something still seems off, check appetite, cud chewing, manure and eyelid color (FAMACHA).'; }
    else if (f < 104.5) { cls = 'warn'; head = hot ? 'Slightly high (heat may explain it)' : 'Elevated'; advice = 'Move the goat to shade, offer cool water and recheck in an hour. A reading that stays above 104°F is a fever.'; }
    else if (f < 106) { cls = 'danger'; head = 'Fever'; advice = 'Call your vet. Fever often points to infection such as pneumonia or mastitis. Keep the goat hydrated and separated from the herd.'; }
    else { cls = 'danger'; head = 'Emergency: very high'; advice = 'Cool the goat with cool (not ice-cold) water on the legs and belly, provide shade and airflow, and call your vet immediately.'; }
    status.className = 'status status--' + cls;
    set(root, 'headline', head + ' · ' + round(f, 1) + '°F / ' + round(fToC(f), 1) + '°C');
    set(root, 'advice', advice);
    const pos = Math.max(0, Math.min(100, (f - 98) / 8 * 100));
    out(root, 'pin').style.left = pos + '%';
  };

  // ---------- Egg planner ----------
  const eggs = (root, form) => {
    const perWeek = parseInt(val(form, 'eggs'), 10);
    form.elements.eggsOut.value = perWeek + ' (' + round(perWeek / 12, 1) + ' dozen)';
    const perYear = parseInt(val(form, 'breed'), 10);
    const winter = val(form, 'winter');
    const henWeek = perYear / 52 * (winter ? 0.6 : 1);
    const hens = Math.max(2, Math.ceil(perWeek / henWeek));
    set(root, 'count', hens);
    set(root, 'coop', hens * 4 + ' sq ft');
    set(root, 'run', hens * 10 + ' sq ft');
    set(root, 'nests', Math.max(1, Math.ceil(hens / 4)));
    set(root, 'roost', round(hens * 10 / 12, 1) + ' ft');
    set(root, 'feed', round(hens * 0.25 * 7, 1) + ' lb');
    set(root, 'water', round(hens * 0.13, 1) + ' gal');
    set(root, 'peak', Math.round(hens * perYear / 52));
    set(root, 'hens', Array.from({ length: Math.min(hens, 30) }, (_, i) => '<span style="--d:' + i * 40 + 'ms">' + (i % 7 === 3 ? '🐓' : '🐔') + '</span>').join('') + (hens > 30 ? '<em>+' + (hens - 30) + '</em>' : ''));
  };

  // ---------- Canning altitude ----------
  const canning = (root, form) => {
    let alt = parseFloat(val(form, 'alt')) || 0;
    if (val(form, 'altunit') === 'm') alt *= 3.28084;
    const base = parseInt(val(form, 'time'), 10) || 0;
    const method = val(form, 'method');
    out(root, 'jar').style.bottom = Math.min(80, alt / 10000 * 80) + '%';
    if (alt > 10000) { set(root, 'big', 'Not covered'); set(root, 'bignote', 'Tested guidance stops at 10,000 ft. Contact your extension office.'); set(root, 'band', round(alt) + ' ft'); return; }
    if (method === 'bath') {
      const add = alt <= 1000 ? 0 : alt <= 3000 ? 5 : alt <= 6000 ? 10 : alt <= 8000 ? 15 : 20;
      set(root, 'biglabel', 'Process for');
      set(root, 'big', (base + add) + ' min');
      set(root, 'bignote', add ? base + ' min + ' + add + ' min for altitude' : 'No adjustment needed below 1,000 ft');
      set(root, 'band', alt <= 1000 ? '0-1,000 ft' : alt <= 3000 ? '1,001-3,000 ft' : alt <= 6000 ? '3,001-6,000 ft' : alt <= 8000 ? '6,001-8,000 ft' : '8,001-10,000 ft');
    } else if (method === 'weighted') {
      const psi = alt <= 1000 ? 10 : 15;
      set(root, 'biglabel', 'Pressure');
      set(root, 'big', psi + ' psi');
      set(root, 'bignote', 'for the recipe’s full ' + base + ' minutes');
      set(root, 'band', alt <= 1000 ? '0-1,000 ft' : 'Above 1,000 ft');
    } else {
      const psi = alt <= 2000 ? 11 : alt <= 4000 ? 12 : alt <= 6000 ? 13 : alt <= 8000 ? 14 : 15;
      set(root, 'biglabel', 'Pressure');
      set(root, 'big', psi + ' psi');
      set(root, 'bignote', 'for the recipe’s full ' + base + ' minutes. Have the gauge tested yearly.');
      set(root, 'band', alt <= 2000 ? '0-2,000 ft' : alt <= 4000 ? '2,001-4,000 ft' : alt <= 6000 ? '4,001-6,000 ft' : alt <= 8000 ? '6,001-8,000 ft' : '8,001-10,000 ft');
    }
  };

  // ---------- Pumpkin pie troubleshooter ----------
  const PIE = {
    watery: ['Watery or runny center', [
      ['Underbaked', 'Bake until the edges are set and the center has only a slight jiggle, about 175°F on an instant-read thermometer. It firms more as it cools.'],
      ['Wet puree', 'Homemade puree holds a lot of water. Drain it in a cheesecloth-lined sieve or cook it down in a pan until thick enough to hold a spoon upright.'],
      ['Cut too soon', 'Custard needs at least 2 hours at room temperature (better: overnight in the fridge) to set fully.'],
      ['Too much liquid', 'Stick to the recipe’s ratio of milk or cream to puree and eggs; extra liquid without extra egg won’t set.'],
    ], '/pumpkin-pie-filling/'],
    cracked: ['Cracked top', [
      ['Overbaked', 'Pull it while the center still wobbles slightly. Carryover heat finishes the job.'],
      ['Oven too hot', 'Bake at 350°F or lower once the crust is set. An oven thermometer often reveals a hot oven.'],
      ['Cooled too fast', 'Cool on a rack away from drafts. Don’t move a hot pie straight into the fridge.'],
    ], '/perfect-pumpkin-pie/'],
    soggy: ['Soggy bottom crust', [
      ['Crust not blind-baked', 'Blind-bake with weights until the bottom looks dry and lightly golden, then fill.'],
      ['Bottom not hot enough', 'Bake on the lowest rack or on a preheated baking sheet so the base gets direct heat.'],
      ['Filling sat in the crust', 'Pour the filling into a warm crust and get it in the oven right away.'],
    ], '/blind-baking/'],
    weeping: ['Liquid pooling after cooling', [
      ['Overbaked custard', 'When egg proteins overcook they squeeze out liquid. Bake to about 175°F, not more.'],
      ['Uneven heat', 'Bake in the center of the oven and shield the crust edges instead of turning up the heat.'],
    ], '/pumpkin-pie-filling/'],
    grainy: ['Grainy or curdled texture', [
      ['Eggs overcooked', 'Lower the temperature and pull the pie sooner; curdling means the custard went well past set.'],
      ['Stringy puree', 'Blend the puree smooth, or push it through a sieve, especially from carving pumpkins.'],
      ['Spices not mixed in', 'Whisk spices and sugar together before adding to the puree to avoid gritty pockets.'],
    ], '/sugar-pumpkin-vs-carving-pumpkin/'],
    sunken: ['Puffed up, then sank', [
      ['Too much air', 'Whisk gently instead of beating with a mixer; air bubbles puff in the oven and collapse as they cool.'],
      ['Overbaked', 'A soufflé-like dome means the eggs went too far. Pull earlier.'],
    ], '/perfect-pumpkin-pie/'],
    edges: ['Crust edges burnt', [
      ['No crust shield', 'Cover the rim with a foil ring or pie shield after the first 15-20 minutes.'],
      ['Long blind bake plus long bake', 'When you blind-bake, shield the edges for the second bake from the start.'],
    ], '/blind-baking/'],
    bland: ['Bland flavor', [
      ['Old spices', 'Ground spices lose aroma within about a year. Toast whole spices and grind fresh for a big difference.'],
      ['Not enough salt', 'A good pinch of salt makes the pumpkin and spices taste like more.'],
      ['Watery pumpkin', 'Roasting the pumpkin instead of boiling concentrates its flavor.'],
    ], '/pumpkin-pie-spices/'],
  };
  const pie = (root, form) => {
    const picked = Array.from(form.querySelectorAll('input[name="s"]:checked')).map((i) => i.value);
    if (!picked.length) { set(root, 'diagnosis', '<p class="diagnosis__empty">Pick a problem above to see what caused it and how to fix it.</p>'); return; }
    set(root, 'diagnosis', picked.map((k) => {
      const [title, causes, link] = PIE[k];
      return '<article class="diag"><h3>' + title + '</h3><ol>' + causes.map((c, i) => '<li style="--d:' + i * 60 + 'ms"><strong>' + c[0] + '.</strong> ' + c[1] + '</li>').join('') + '</ol><a href="' + link + '">Read the full guide →</a></article>';
    }).join('') + '<p class="diagnosis__tip"><strong>The doneness test:</strong> edges set, center jiggles like gelatin over about a 2-inch circle, about 175°F inside.</p>');
  };

  // ---------- Recipe scaler ----------
  const UNI = { '½': 0.5, '⅓': 1 / 3, '⅔': 2 / 3, '¼': 0.25, '¾': 0.75, '⅛': 0.125, '⅜': 0.375, '⅝': 0.625, '⅞': 0.875 };
  function parseQty(str) {
    const s = str.replace(/([0-9])([½⅓⅔¼¾⅛⅜⅝⅞])/g, '$1 $2');
    const num = '(\\d+\\s+\\d+/\\d+|\\d+/\\d+|\\d+(?:\\.\\d+)?|[½⅓⅔¼¾⅛⅜⅝⅞]|\\d+\\s+[½⅓⅔¼¾⅛⅜⅝⅞])';
    const m = s.match(new RegExp('^\\s*' + num + '(?:\\s*(?:-|–|to)\\s*' + num + ')?'));
    if (!m) return null;
    const toNum = (t) => {
      t = t.trim();
      let total = 0;
      for (const part of t.split(/\s+/)) {
        if (UNI[part] !== undefined) total += UNI[part];
        else if (part.includes('/')) { const [a, b] = part.split('/'); total += parseFloat(a) / parseFloat(b); }
        else total += parseFloat(part);
      }
      return total;
    };
    return { a: toNum(m[1]), b: m[2] ? toNum(m[2]) : null, rest: s.slice(m[0].length) };
  }
  const fmtQty = (n) => (n >= 10 ? String(Math.round(n)) : fraction(n));
  const scaler = (root, form) => {
    const from = parseFloat(val(form, 'from')) || 1;
    const to = parseFloat(val(form, 'to')) || 1;
    const f = to / from;
    set(root, 'factor', round(f, 2) + '×  ·  ' + to + ' servings');
    const lines = val(form, 'list').split('\n').filter((l) => l.trim());
    set(root, 'list', lines.map((l) => {
      const q = parseQty(l);
      if (!q) return '<li>' + esc(l) + '</li>';
      const qty = fmtQty(q.a * f) + (q.b !== null ? '–' + fmtQty(q.b * f) : '');
      return '<li><b>' + qty + '</b>' + esc(q.rest) + '</li>';
    }).join(''));
  };

  const INIT = {
    'brine-calculator': brine, 'lamb-cooking-calculator': lamb, 'lamb-sides-builder': plate,
    'goat-gestation-calculator': gestation, 'goat-temperature-checker': goatTemp, 'egg-production-planner': eggs,
    'canning-altitude-adjuster': canning, 'pumpkin-pie-troubleshooter': pie, 'recipe-scaler': scaler,
  };

  document.querySelectorAll('[data-tool]').forEach((root) => {
    const fn = INIT[root.dataset.tool];
    if (!fn) return;
    const run = bind(root, fn);
    root.classList.add('is-ready');
    const shuffle = root.querySelector('[data-shuffle]');
    if (shuffle) shuffle.addEventListener('click', () => { run(); root.querySelector('.plate').classList.remove('spin'); void root.offsetWidth; root.querySelector('.plate').classList.add('spin'); });
    const ics = root.querySelector('[data-ics]');
    if (ics) ics.addEventListener('click', () => icsDownload(root));
    root.querySelectorAll('[data-factor]').forEach((b) => b.addEventListener('click', () => {
      const form = root.querySelector('form');
      form.elements.to.value = Math.round((parseFloat(form.elements.from.value) || 1) * parseFloat(b.dataset.factor) * 100) / 100;
      run();
    }));
    const copy = root.querySelector('[data-copy]');
    if (copy) copy.addEventListener('click', () => {
      const text = Array.from(root.querySelectorAll('.scaled li')).map((li) => li.textContent).join('\n');
      (navigator.clipboard ? navigator.clipboard.writeText(text) : Promise.reject()).then(() => { copy.textContent = 'Copied!'; }, () => { copy.textContent = 'Select and copy'; });
    });
  });
})();
