/* Haggle Hero — Vintique Flea mini game */
(function () {
  'use strict';

  var SLUG = 'haggle-hero';
  var ITEMS_PER_GAME = 5;
  var BEST_KEY = 'vf_game_haggle_best';

  /* ---------- shared helpers ---------- */
  function amazon(q) {
    try { if (window.VF && typeof window.VF.amazon === 'function') return window.VF.amazon(q); } catch (e) {}
    return 'https://www.amazon.com/s?k=' + encodeURIComponent(q) + '&tag=josephrayditt-20';
  }
  function shopUrl(s) {
    try { if (window.VF && typeof window.VF.shopUrl === 'function') return window.VF.shopUrl(s); } catch (e) {}
    return '/shop/' + s + '/';
  }
  function store(key, val) {
    try {
      if (arguments.length > 1) { window.localStorage.setItem(key, JSON.stringify(val)); return val; }
      var raw = window.localStorage.getItem(key);
      return raw == null ? null : JSON.parse(raw);
    } catch (e) { return null; }
  }
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      var v = attrs[k];
      if (v == null || v === false) return;
      if (k === 'class') el.className = v;
      else if (k === 'text') el.textContent = v;
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? '' : v);
    });
    (kids || []).forEach(function (c) { if (c != null) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function rand(min, max) { return min + Math.random() * (max - min); }
  function money(n) { return '$' + Math.round(n).toLocaleString('en-US'); }
  function linkItem(href, ico, label, sub, amz) {
    var a = h('a', { class: 'g-link', href: href }, [
      h('span', { class: 'g-link__ico', 'aria-hidden': 'true', text: ico }),
      h('span', null, [label, sub ? h('small', { text: sub }) : null])
    ]);
    if (amz) { a.target = '_blank'; a.rel = 'sponsored nofollow noopener'; }
    return h('li', null, [a]);
  }

  /* ---------- content ---------- */
  var ITEMS = [
    { e: '🗄️', n: 'Teak mid-century credenza', c: 'Mid-Century Modern', s: 'mid-century-modern', a: 650, flaw: 'water ring on the top' },
    { e: '🧥', n: 'Faded denim trucker jacket', c: 'Vintage Clothing', s: 'vintage-clothing', a: 85, flaw: 'missing button on the cuff' },
    { e: '🛒', n: 'Factory-cart coffee table', c: 'Architectural Salvage & Industrial', s: 'architectural-salvage-industrial', a: 420, flaw: 'wobbly caster wheel' },
    { e: '🪣', n: 'Galvanized farmhouse bucket trio', c: 'Rustic Home Decor', s: 'rustic-home-decor', a: 48, flaw: 'dent in the smallest bucket' },
    { e: '🕰️', keep: true, n: 'Art Deco mantel clock', c: 'Antiques & Collectibles', s: 'antiques-collectibles', a: 120, flaw: 'clock doesn\'t actually keep time' },
    { e: '💿', n: 'Crate of 1970s rock LPs', c: 'Vinyl Records & Retro', s: 'vinyl-records-retro', a: 60, flaw: 'a few sleeves with ring wear' },
    { e: '🥣', keep: true, n: 'Pyrex nesting bowl set', c: 'Vintage Kitchen & Barware', s: 'vintage-kitchen-barware', a: 95, flaw: 'dishwasher fading on one bowl' },
    { e: '🍸', n: 'Brass Hollywood Regency bar cart', c: 'Vintage Kitchen & Barware', s: 'vintage-kitchen-barware', a: 280, flaw: 'tarnish on the handles' },
    { e: '🍳', n: 'Cast-iron skillet, No. 8', c: 'Vintage Kitchen & Barware', s: 'vintage-kitchen-barware', a: 75, flaw: 'spot of surface rust' },
    { e: '🪟', n: 'Salvaged stained-glass window', c: 'Architectural Salvage & Industrial', s: 'architectural-salvage-industrial', a: 340, flaw: 'hairline crack in one pane' },
    { e: '🌞', n: 'Sunburst wall mirror', c: 'Mid-Century Modern', s: 'mid-century-modern', a: 180, flaw: 'one bent ray' },
    { e: '👢', n: 'Hand-tooled cowboy boots', c: 'Vintage Clothing', s: 'vintage-clothing', a: 110, flaw: 'worn-down heels' },
    { e: '📻', n: 'Wood-grain stereo receiver', c: 'Vinyl Records & Retro', s: 'vinyl-records-retro', a: 200, flaw: 'scratchy volume knob' }
  ];

  var VENDORS = [
    { face: '🤠', name: 'Big Earl', vibe: 'Gruff but fair. Hates lowballs.', drain: 1.15, tag: ' Take it or leave it, partner.' },
    { face: '👵', name: 'Miss Dolores', vibe: 'Sweet as pie and patient.', drain: 0.8, tag: ' Bless your heart.' },
    { face: '🧔', name: 'Rico the Picker', vibe: 'Chatty, loves a good story.', drain: 1.0, tag: ' Man, I got this out of a barn in Brenham!' },
    { face: '👩‍🎤', name: 'Jade', vibe: 'Cool, quick, no nonsense.', drain: 1.25, tag: ' I\'ve got three other people eyeing it.' }
  ];

  var ADDONS = ['a box of old postcards', 'a set of brass coasters', 'a vintage tin sign', 'a stack of old LIFE magazines', 'a pair of Bakelite napkin rings', 'a hand-painted souvenir plate'];

  var LINES = {
    greet: ['Howdy! That {item} is a real beauty. I\'m asking {P}.', 'Ah, good eye! The {item} — I\'d let it go for {P}.', 'That one just came in this morning. {P} and it\'s yours.'],
    counter: ['Hmm… I could come down to {P}.', 'Meet me at {P} and we\'ll shake on it.', 'I paid a pretty penny for it. Best I can do right now is {P}.', 'How about {P}? That\'s a fair price for the quality.'],
    floor: ['That\'s rock bottom: {P}. Can\'t go lower.', '{P} is my floor, friend. I\'ve got to eat too.'],
    insult: ['Ha! I paid more than that for it.', 'Now you\'re just pulling my leg.', 'Whoa — let\'s keep it friendly, okay?'],
    lower: ['Wait, you\'re going DOWN? You already offered {L}.', 'Hold on — your last offer was {L}. Going backwards isn\'t how this works.'],
    accept: ['Deal! Pleasure doing business.', 'Sold! Want a bag for that?', 'You drive a hard bargain. It\'s yours!'],
    quit: ['You know what? I think I\'ll just keep it.', 'Let\'s call it a day, friend. It\'s not for sale to you.', 'I\'m done haggling on this one. Have a nice day.'],
    flaw: ['Yeah, I noticed the {flaw} too. Fair point — {P}.', 'Okay, okay, the {flaw}. I\'ll knock it to {P}.'],
    flawAgain: ['Yeah, yeah, you mentioned that already.', 'We covered the {flaw}. Anything else?'],
    bundleYes: ['Tell you what: buy it and I\'ll throw in {addon}.', 'I like moving inventory. I\'ll toss in {addon} if we make a deal.'],
    bundleNo: ['Not today, hon. The price is the price.', 'I\'m not in a giving mood after all that.'],
    letGo: ['Suit yourself! Come back anytime.', 'No worries, happy hunting!', 'Okay — it\'ll probably be gone in an hour, though.'],
    callback: ['Wait! Come back… fine, {P}. Final offer.', 'Hey, hold up! I can do {P} if you take it now.']
  };

  var TIPS = {
    open: 'Etiquette: say hi and show genuine interest before talking price — vendors deal more with friendly shoppers.',
    goodOpen: 'Nice opener. Starting around 70–80% of the tag shows respect and leaves room to meet in the middle.',
    lowball: 'Etiquette: offers under about half the tag can offend. Most vendors build in 10–30% wiggle room, not 60%.',
    lower: 'Never go lower than an offer you already made — it reads as bad faith and burns goodwill fast.',
    flaw: 'Pointing out a genuine flaw — politely, without trashing the piece — is a fair reason to ask for a discount.',
    flawAgain: 'Make your point once. Repeating complaints just annoys the seller.',
    bundle: 'Bundling is one of the best tactics: vendors love moving more inventory in a single sale.',
    bundleNo: 'Bundle requests land best early, while the vendor is still in a good mood.',
    deal: 'Once a vendor accepts your offer, you\'re committed. Pay happily — cash is king at the flea!',
    over: 'Never offer more than the current price — if you\'re happy with it, just say "I\'ll take it!"',
    quit: 'Patience is a two-way street. Too many tiny or rapid-fire offers can end a negotiation.',
    walk: 'Being willing to walk away is your strongest tool — just do it kindly and leave the door open.',
    walkCold: 'Walking away before making any offer is fine, but a polite question like "Is that your best price?" costs nothing.',
    callback: 'Callbacks happen when your last offer was close to what the vendor can accept.'
  };

  /* ---------- state ---------- */
  var root, stage, live, game, cur, ui;

  function fill(s, extra) {
    return s.replace(/\{(\w+)\}/g, function (m, k) {
      if (k === 'P') return money(cur.P);
      if (k === 'item') return cur.item.keep ? cur.item.n : cur.item.n.charAt(0).toLowerCase() + cur.item.n.slice(1);
      if (k === 'flaw') return cur.item.flaw;
      if (extra && extra[k] != null) return extra[k];
      return m;
    });
  }

  function newGame() {
    game = { items: shuffle(ITEMS).slice(0, ITEMS_PER_GAME), idx: 0, results: [] };
    startItem();
  }

  function startItem() {
    var item = game.items[game.idx];
    var vendor = pick(VENDORS);
    var A = item.a;
    var F = Math.round(A * rand(0.55, 0.85));
    cur = { item: item, vendor: vendor, A: A, F: F, P: A, patience: 100, offers: [], flawUsed: false, bundleUsed: false, addon: null, bonus: 0, done: false, callback: null };
    renderItem();
    say(fill(pick(LINES.greet)), 'neutral');
    tip(TIPS.open);
  }

  function lastOffer() { return cur.offers.length ? cur.offers[cur.offers.length - 1] : 0; }

  /* ---------- rendering ---------- */
  function statsBar() {
    var saved = game.results.reduce(function (t, r) { return t + r.saved; }, 0);
    var best = store(BEST_KEY);
    return h('ul', { class: 'g-stats', 'aria-label': 'Progress' }, [
      h('li', { class: 'g-stat' }, [h('b', { text: (game.idx + 1) + '/' + ITEMS_PER_GAME }), h('span', { text: 'Item' })]),
      h('li', { class: 'g-stat g-stat--teal' }, [h('b', { text: money(saved) }), h('span', { text: 'Saved' })]),
      h('li', { class: 'g-stat' }, [h('b', { text: typeof best === 'number' ? money(best) : '—' }), h('span', { text: 'Best' })])
    ]);
  }

  function renderItem() {
    var it = cur.item, v = cur.vendor;
    stage.innerHTML = '';
    ui = {};
    ui.bubble = h('p', { class: 'g-haggle__bubble' });
    ui.meter = h('div', { class: 'g-haggle__meter', role: 'meter', 'aria-label': v.name + '\'s patience', 'aria-valuemin': '0', 'aria-valuemax': '100', 'aria-valuenow': '100' }, [h('i', { style: 'width:100%' })]);
    ui.price = h('span', { class: 'g-haggle__tag', text: money(cur.P) });
    ui.input = h('input', { type: 'number', inputmode: 'numeric', min: '1', step: '1', id: 'g-hag-offer', 'aria-describedby': 'g-hag-pct' });
    ui.range = h('input', { type: 'range', class: 'g-haggle__range', min: '1', step: '1', 'aria-label': 'Offer slider' });
    ui.pct = h('span', { class: 'g-haggle__pct', id: 'g-hag-pct' });
    ui.log = h('ol', { class: 'g-haggle__log', 'aria-label': 'Negotiation history' });
    ui.tip = h('p', { class: 'g-haggle__tip' });
    ui.after = h('div', { class: 'g-row g-mt' });

    ui.input.addEventListener('input', function () { ui.range.value = ui.input.value; updatePct(); });
    ui.range.addEventListener('input', function () { ui.input.value = ui.range.value; updatePct(); });
    ui.input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); doOffer(); } });

    ui.btnOffer = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: doOffer }, ['💵 Make offer']);
    ui.btnFlaw = h('button', { type: 'button', class: 'g-btn', onclick: doFlaw }, ['🔎 Point out a flaw']);
    ui.btnBundle = h('button', { type: 'button', class: 'g-btn', onclick: doBundle }, ['🎁 Bundle it']);
    ui.btnWalk = h('button', { type: 'button', class: 'g-btn', onclick: doWalk }, ['🚶 Walk away']);
    ui.btnTake = h('button', { type: 'button', class: 'g-btn g-btn--sm g-btn--mustard', onclick: function () { deal(cur.P, 'You took the current price.'); } }, ['I\'ll take it']);

    stage.appendChild(h('section', { class: 'g-card g-pop', 'aria-labelledby': 'g-hag-item' }, [
      h('div', { class: 'g-head' }, [
        h('div', null, [h('h2', { class: 'g-title', text: 'Haggle Hero' }), h('p', { class: 'g-sub', text: 'Talk your way to a deal — politely.' })]),
        statsBar()
      ]),
      h('div', { class: 'g-haggle__table' }, [
        h('div', { class: 'g-haggle__item' }, [
          h('div', { class: 'g-haggle__emoji', 'aria-hidden': 'true', text: it.e }),
          h('div', { style: 'min-width:0' }, [
            h('span', { class: 'g-haggle__cat', text: it.c }),
            h('h3', { class: 'g-haggle__itemname', id: 'g-hag-item', text: it.n }),
            h('div', null, [h('span', { class: 'g-sr', text: 'Current price: ' }), ui.price]),
            h('div', { class: 'g-sub', style: 'font-size:.82rem', text: 'Tag said ' + money(cur.A) })
          ])
        ]),
        h('div', { class: 'g-haggle__vendor' }, [
          h('div', { class: 'g-haggle__face', 'aria-hidden': 'true', text: v.face }),
          h('div', { style: 'min-width:0;flex:1' }, [
            h('p', { class: 'g-haggle__vname' }, [v.name, h('span', { class: 'g-sub', style: 'font-weight:400;font-size:.82rem', text: ' — ' + v.vibe })]),
            ui.bubble,
            h('div', { class: 'g-haggle__patience' }, [h('label', { text: 'Patience' }), ui.meter])
          ])
        ])
      ]),
      h('div', { class: 'g-haggle__offer' }, [
        h('label', { for: 'g-hag-offer', style: 'font-weight:700;display:block;margin-bottom:6px', text: 'Your offer' }),
        h('div', { class: 'g-haggle__offerrow' }, [
          h('span', { class: 'g-haggle__money' }, [h('span', { 'aria-hidden': 'true', text: '$' }), ui.input]),
          ui.range, ui.pct
        ]),
        h('div', { class: 'g-haggle__actions' }, [ui.btnOffer, ui.btnFlaw, ui.btnBundle, ui.btnWalk]),
        h('div', { class: 'g-row', style: 'margin-top:8px' }, [ui.btnTake])
      ]),
      ui.tip,
      ui.after,
      ui.log
    ]));
    syncControls(true);
    updateMeter();
  }

  function updatePct() {
    var x = Number(ui.input.value) || 0;
    ui.pct.textContent = x ? Math.round(x / cur.A * 100) + '% of tag' : '';
  }

  function syncControls(resetValue) {
    ui.price.textContent = money(cur.P);
    ui.range.max = String(cur.P);
    ui.range.min = String(Math.max(1, Math.round(cur.A * 0.3)));
    ui.input.max = String(cur.P);
    if (resetValue) {
      var suggestion = Math.max(lastOffer() + 1, Math.round(cur.P * 0.8));
      suggestion = Math.min(suggestion, cur.P);
      ui.input.value = String(suggestion);
      ui.range.value = String(suggestion);
    }
    ui.btnFlaw.textContent = cur.flawUsed ? '🔎 Flaw noted ✓' : '🔎 Point out a flaw';
    ui.btnBundle.textContent = cur.bundleUsed ? '🎁 Bundle asked ✓' : '🎁 Bundle it';
    updatePct();
  }

  function updateMeter() {
    var p = Math.max(0, Math.round(cur.patience));
    ui.meter.firstChild.style.width = p + '%';
    ui.meter.setAttribute('aria-valuenow', String(p));
    ui.meter.setAttribute('aria-valuetext', p + ' percent');
    ui.meter.classList.toggle('is-mid', p <= 60 && p > 30);
    ui.meter.classList.toggle('is-low', p <= 30);
  }

  function say(text, tone) {
    ui.bubble.textContent = text;
    ui.log.insertBefore(h('li', null, [h('b', { text: cur.vendor.name + ': ' }), text]), ui.log.firstChild);
    while (ui.log.children.length > 5) ui.log.removeChild(ui.log.lastChild);
    live.textContent = cur.vendor.name + ' says: ' + text + (tone === 'end' ? '' : ' Price ' + money(cur.P) + '. Patience ' + Math.max(0, Math.round(cur.patience)) + ' percent.');
  }
  function you(text) {
    ui.log.insertBefore(h('li', { style: 'background:transparent;border:1px dashed var(--line,#d8c9b0)' }, [h('b', { text: 'You: ' }), text]), ui.log.firstChild);
  }
  function tip(t) { ui.tip.textContent = '💡 ' + t; }

  function drain(n) { cur.patience -= n * cur.vendor.drain; updateMeter(); }

  /* ---------- actions ---------- */
  function guard() { return cur.done || cur.callback; }

  function doOffer() {
    if (guard()) return;
    var x = Math.round(Number(ui.input.value));
    if (!(x > 0)) { tip('Type a dollar amount or use the slider to make an offer.'); ui.input.focus(); return; }
    you('How about ' + money(x) + '?');
    if (x >= cur.P) {
      var over = x > cur.P;
      deal(cur.P, over ? null : 'You met the price.');
      if (over) tip(TIPS.over);
      return;
    }
    var last = lastOffer();
    if (last && x <= last) {
      drain(14);
      say(fill(pick(LINES.lower), { L: money(last) }));
      tip(TIPS.lower);
      return checkQuit();
    }
    var first = cur.offers.length === 0;
    cur.offers.push(x);
    drain(6);
    var pctTag = x / cur.A;

    if (x >= cur.F) {
      var threshold = cur.F + (cur.P - cur.F) * 0.4;
      if (x >= threshold || cur.patience < 35 || cur.offers.length >= 4) return deal(x);
      cur.P = Math.max(cur.F, Math.round(x + (cur.P - x) * 0.5));
      if (cur.P <= x) cur.P = x + 1;
      say(fill(pick(LINES.counter)) + (Math.random() < 0.35 ? cur.vendor.tag : ''));
      tip(first ? TIPS.goodOpen : 'Meeting in the middle is the classic move — small, steady steps up show good faith.');
    } else if (pctTag < 0.45) {
      drain(30);
      say(pick(LINES.insult));
      tip(TIPS.lowball);
    } else {
      drain(8 + (cur.F - x) / cur.A * 80);
      var newP = Math.max(cur.F, Math.round(cur.P - (cur.P - cur.F) * 0.35));
      if (newP >= cur.P) { cur.P = cur.F; say(fill(pick(LINES.floor))); }
      else { cur.P = newP; say(fill(pick(LINES.counter)) + (Math.random() < 0.35 ? cur.vendor.tag : '')); }
      tip(first && pctTag >= 0.65 ? TIPS.goodOpen : 'Getting closer. Watch the patience meter — each offer costs a little goodwill.');
    }
    syncControls(true);
    checkQuit();
  }

  function doFlaw() {
    if (guard()) return;
    you('I noticed the ' + cur.item.flaw + '…');
    if (cur.flawUsed) {
      drain(15);
      say(fill(pick(LINES.flawAgain)));
      tip(TIPS.flawAgain);
      return checkQuit();
    }
    cur.flawUsed = true;
    cur.F = Math.max(1, Math.round(cur.F - cur.A * 0.05));
    cur.P = Math.max(cur.F, Math.round(cur.P - cur.A * 0.07));
    drain(8);
    say(fill(pick(LINES.flaw)));
    tip(TIPS.flaw);
    syncControls(true);
    checkQuit();
  }

  function doBundle() {
    if (guard()) return;
    you('If I buy this, could you throw in something small?');
    if (cur.bundleUsed) {
      drain(12);
      say(cur.addon ? 'I already said I\'d add ' + cur.addon + '. Don\'t push it!' : 'I told you — not today.');
      tip(TIPS.flawAgain);
      return checkQuit();
    }
    cur.bundleUsed = true;
    if (cur.patience >= 45) {
      cur.addon = pick(ADDONS);
      cur.bonus = Math.max(3, Math.round(cur.A * rand(0.08, 0.12)));
      drain(8);
      say(fill(pick(LINES.bundleYes), { addon: cur.addon }) + ' (about ' + money(cur.bonus) + ' value)');
      tip(TIPS.bundle);
    } else {
      drain(10);
      say(pick(LINES.bundleNo));
      tip(TIPS.bundleNo);
    }
    syncControls(false);
    checkQuit();
  }

  function doWalk() {
    if (guard()) return;
    you('Thanks, I\'ll think about it.');
    var last = lastOffer();
    if (!last) { say(pick(LINES.letGo), 'end'); tip(TIPS.walkCold); return endItem('walked', 0); }
    var ratio = last / cur.F;
    var chance = ratio >= 0.9 ? 0.8 : ratio >= 0.78 ? 0.4 : 0.1;
    if (cur.patience > 0 && Math.random() < chance) {
      var price = Math.max(last, cur.F);
      cur.P = price;
      cur.callback = price;
      say(fill(pick(LINES.callback)));
      tip(TIPS.callback);
      syncControls(false);
      setDisabled(true);
      var yes = h('button', { type: 'button', class: 'g-btn g-btn--teal', onclick: function () { cur.callback = null; deal(price, 'You accepted the callback.'); } }, ['✅ Accept ' + money(price)]);
      var no = h('button', { type: 'button', class: 'g-btn', onclick: function () { cur.callback = null; say(pick(LINES.letGo), 'end'); tip(TIPS.walk); endItem('walked', 0); } }, ['Keep walking']);
      ui.after.innerHTML = '';
      ui.after.appendChild(yes); ui.after.appendChild(no);
      yes.focus();
    } else {
      say(pick(LINES.letGo), 'end');
      tip(TIPS.walk);
      endItem('walked', 0);
    }
  }

  function checkQuit() {
    if (cur.patience <= 0 && !cur.done) {
      say(pick(LINES.quit), 'end');
      tip(TIPS.quit);
      endItem('lost', 0);
    }
  }

  function deal(price, note) {
    if (cur.done) return;
    cur.P = price;
    syncControls(false);
    say(pick(LINES.accept) + (cur.addon ? ' And ' + cur.addon + ' is yours too.' : ''), 'end');
    tip(TIPS.deal);
    endItem('bought', price, note);
  }

  function setDisabled(on) {
    [ui.btnOffer, ui.btnFlaw, ui.btnBundle, ui.btnWalk, ui.btnTake, ui.input, ui.range].forEach(function (b) { b.disabled = on; });
  }

  function endItem(outcome, paid) {
    cur.done = true;
    setDisabled(true);
    var bonus = outcome === 'bought' ? cur.bonus : 0;
    var saved = outcome === 'bought' ? (cur.A - paid) + bonus : 0;
    var pct = outcome === 'bought' ? Math.round(saved / cur.A * 100) : 0;
    game.results.push({ item: cur.item, outcome: outcome, paid: paid, saved: saved, pct: pct, ask: cur.A, floor: cur.F, addon: outcome === 'bought' ? cur.addon : null });

    var msg;
    if (outcome === 'bought') {
      var grade = paid <= cur.F * 1.03 ? 'Masterful — you hit the vendor\'s floor!' : pct >= 25 ? 'Great deal!' : pct >= 10 ? 'Solid haggle.' : 'You paid close to full price.';
      msg = 'Bought for ' + money(paid) + (bonus ? ' + ' + cur.addon + ' (' + money(bonus) + ')' : '') + ' — saved ' + money(saved) + ' (' + pct + '%). ' + grade + ' Their secret floor was ' + money(cur.F) + '.';
    } else if (outcome === 'walked') {
      msg = 'You walked away empty-handed. Their secret floor was ' + money(cur.F) + '.';
    } else {
      msg = cur.vendor.name + ' ran out of patience. Their secret floor was ' + money(cur.F) + '.';
    }
    var fb = h('div', { class: 'g-feedback ' + (outcome === 'bought' ? 'g-feedback--good' : 'g-feedback--bad'), style: 'flex:1 1 100%' }, [h('strong', { text: outcome === 'bought' ? 'Deal! ' : 'No deal. ' }), msg]);
    var lastOne = game.idx >= ITEMS_PER_GAME - 1;
    var next = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: function () {
      if (lastOne) renderResults(); else { game.idx++; startItem(); var f = stage.querySelector('#g-hag-offer'); if (f) f.focus({ preventScroll: true }); }
    } }, [lastOne ? 'See your haul →' : 'Next booth →']);
    ui.after.innerHTML = '';
    ui.after.appendChild(fb);
    ui.after.appendChild(next);
    var oldStats = stage.querySelector('.g-stats');
    if (oldStats) oldStats.parentNode.replaceChild(statsBar(), oldStats);
    live.textContent = msg;
    next.focus({ preventScroll: true });
  }

  function renderResults() {
    var totalSaved = game.results.reduce(function (t, r) { return t + r.saved; }, 0);
    var avgPct = Math.round(game.results.reduce(function (t, r) { return t + r.pct; }, 0) / game.results.length);
    var bought = game.results.filter(function (r) { return r.outcome === 'bought'; });
    var prevBest = store(BEST_KEY);
    var isBest = typeof prevBest !== 'number' || totalSaved > prevBest;
    if (isBest) store(BEST_KEY, totalSaved);

    var rank = avgPct >= 28 ? ['🏆', 'Haggle Hero'] : avgPct >= 18 ? ['🤝', 'Smooth Negotiator'] : avgPct >= 8 ? ['🛍️', 'Friendly Bargainer'] : ['🌱', 'Full-Price Friend'];

    var rows = game.results.map(function (r) {
      return h('tr', null, [
        h('td', null, [r.item.e + ' ' + r.item.n]),
        h('td', { text: r.outcome === 'bought' ? money(r.paid) + ' / ' + money(r.ask) : (r.outcome === 'walked' ? 'Walked' : 'No sale') }),
        h('td', { text: r.outcome === 'bought' ? r.pct + '%' : '—' })
      ]);
    });

    var slugCount = {};
    (bought.length ? bought : game.results).forEach(function (r) { slugCount[r.item.s] = (slugCount[r.item.s] || 0) + 1; });
    var topSlug = Object.keys(slugCount).sort(function (a, b) { return slugCount[b] - slugCount[a]; })[0];
    var topItem = game.results.filter(function (r) { return r.item.s === topSlug; })[0].item;

    stage.innerHTML = '';
    var again = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: function () { newGame(); var f = stage.querySelector('#g-hag-offer'); if (f) f.focus({ preventScroll: true }); } }, ['↻ Play again']);
    stage.appendChild(h('section', { class: 'g-card g-results g-pop', 'aria-labelledby': 'g-hag-res' }, [
      h('div', { class: 'g-results__badge', 'aria-hidden': 'true', text: rank[0] }),
      h('h2', { class: 'g-title', id: 'g-hag-res', text: rank[1] }),
      h('p', { class: 'g-results__big', text: money(totalSaved) + ' saved' }),
      h('p', { text: 'Average savings: ' + avgPct + '% across ' + ITEMS_PER_GAME + ' booths · ' + bought.length + ' item' + (bought.length === 1 ? '' : 's') + ' bought. ' + (isBest ? 'New best haul! 🎉' : 'Best: ' + money(prevBest)) }),
      h('div', { style: 'overflow-x:auto;max-width:100%' }, [
        h('table', { class: 'g-haggle__summary' }, [
          h('caption', { class: 'g-sr', text: 'Your deals' }),
          h('thead', null, [h('tr', null, [h('th', { scope: 'col', text: 'Item' }), h('th', { scope: 'col', text: 'Paid / tag' }), h('th', { scope: 'col', text: 'Saved' })])]),
          h('tbody', null, rows)
        ])
      ]),
      h('p', { class: 'g-haggle__tip', style: 'text-align:left;max-width:520px;margin:14px auto 0', text: '💡 Real-world tip: bring small bills, shop early for selection or late for deals, and always be kind — the best price often goes to the nicest customer.' }),
      h('div', { class: 'g-row g-row--center g-mt' }, [again]),
      h('ul', { class: 'g-links' }, [
        linkItem(shopUrl(topSlug), topItem.e, 'Shop ' + topItem.c, 'Real finds from Vintique Flea dealers'),
        linkItem(shopUrl('flea-market-gear'), '🧺', 'Flea market gear', 'Carts, totes & tools for serious pickers'),
        linkItem(amazon('cash apron with pockets for vendors flea market'), '💵', 'Grab a cash apron', 'On Amazon — haggle with small bills', true)
      ]),
      h('p', { class: 'g-disclose', text: 'Amazon links are affiliate links; we may earn a small commission.' })
    ]));
    live.textContent = rank[1] + '! You saved ' + money(totalSaved) + ', averaging ' + avgPct + ' percent.';
    again.focus({ preventScroll: true });
  }

  function init() {
    root = document.querySelector('.game[data-game="' + SLUG + '"]') || document.getElementById('game-root');
    if (!root) return;
    root.innerHTML = '';
    stage = h('div', { class: 'g-stage' });
    live = h('p', { class: 'g-sr', 'aria-live': 'polite', role: 'status' });
    root.appendChild(stage);
    root.appendChild(live);
    newGame();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
