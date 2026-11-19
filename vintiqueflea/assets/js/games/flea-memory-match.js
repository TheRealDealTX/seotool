/* Flea Memory Match — Vintique Flea mini game */
(function () {
  'use strict';

  var SLUG = 'flea-memory-match';
  var BEST_KEY = 'vf_game_memory_best';

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
  function fmt(sec) { var m = Math.floor(sec / 60), s = sec % 60; return m + ':' + (s < 10 ? '0' : '') + s; }
  function linkItem(href, ico, label, sub, amz) {
    var a = h('a', { class: 'g-link', href: href }, [
      h('span', { class: 'g-link__ico', 'aria-hidden': 'true', text: ico }),
      h('span', null, [label, sub ? h('small', { text: sub }) : null])
    ]);
    if (amz) { a.target = '_blank'; a.rel = 'sponsored nofollow noopener'; }
    return h('li', null, [a]);
  }

  /* ---------- content ---------- */
  var FACES = [
    { e: '📻', n: 'Tube radio', s: 'antiques-collectibles' },
    { e: '☎️', n: 'Rotary phone', s: 'antiques-collectibles' },
    { e: '🪑', n: 'Shell chair', s: 'mid-century-modern' },
    { e: '💿', n: 'Vinyl LP', s: 'vinyl-records-retro' },
    { e: '🫖', n: 'Enamel teapot', s: 'vintage-kitchen-barware' },
    { e: '🕰️', n: 'Mantel clock', s: 'antiques-collectibles' },
    { e: '📷', n: 'Film camera', s: 'antiques-collectibles' },
    { e: '🧳', n: 'Steamer trunk', s: 'antiques-collectibles' },
    { e: '👢', n: 'Cowboy boots', s: 'vintage-clothing' },
    { e: '🎸', n: 'Archtop guitar', s: 'vinyl-records-retro' },
    { e: '🍸', n: 'Cocktail glass', s: 'vintage-kitchen-barware' },
    { e: '🫧', n: 'Lava lamp', s: 'vinyl-records-retro' },
    { e: '🪞', n: 'Vanity mirror', s: 'antiques-collectibles' },
    { e: '🏮', n: 'Paper lantern', s: 'rustic-home-decor' },
    { e: '🪣', n: 'Galvanized pail', s: 'rustic-home-decor' },
    { e: '👒', n: 'Sun hat', s: 'vintage-clothing' }
  ];
  var LEVELS = {
    easy: { label: 'Easy', cols: 4, rows: 3 },
    medium: { label: 'Medium', cols: 4, rows: 4 },
    hard: { label: 'Hard', cols: 6, rows: 4 }
  };
  var SHOP_NAMES = {
    'antiques-collectibles': 'Antiques & Collectibles', 'mid-century-modern': 'Mid-Century Modern', 'vinyl-records-retro': 'Vinyl Records & Retro',
    'vintage-kitchen-barware': 'Vintage Kitchen & Barware', 'vintage-clothing': 'Vintage Clothing', 'rustic-home-decor': 'Rustic Home Decor'
  };

  /* ---------- state ---------- */
  var root, stage, live, grid, statEls = {}, g, timerId, level = 'medium', narrowMq;

  function bests() { var b = store(BEST_KEY); return b && typeof b === 'object' ? b : {}; }

  function cols() {
    var L = LEVELS[level];
    var narrow = false;
    try { narrow = narrowMq ? narrowMq.matches : false; } catch (e) {}
    return narrow ? Math.min(4, L.cols) : L.cols;
  }

  function stopTimer() { if (timerId) { window.clearInterval(timerId); timerId = null; } }

  function newGame(focusGrid) {
    stopTimer();
    var L = LEVELS[level];
    var pairs = (L.cols * L.rows) / 2;
    var faces = shuffle(FACES).slice(0, pairs);
    var deck = shuffle(faces.concat(faces)).map(function (f, i) { return { id: i, face: f, up: false, matched: false }; });
    g = { deck: deck, open: [], moves: 0, matched: 0, pairs: pairs, start: 0, elapsed: 0, lock: false, done: false };
    render(focusGrid);
  }

  function tick() {
    if (!g.start || g.done) return;
    g.elapsed = Math.floor((Date.now() - g.start) / 1000);
    if (statEls.time) statEls.time.textContent = fmt(g.elapsed);
  }

  function updateStats() {
    statEls.moves.textContent = String(g.moves);
    statEls.pairs.textContent = g.matched + '/' + g.pairs;
    statEls.time.textContent = fmt(g.elapsed);
  }

  function render(focusGrid) {
    stage.innerHTML = '';
    var b = bests()[level];
    statEls.moves = h('b', { text: '0' });
    statEls.time = h('b', { text: '0:00' });
    statEls.pairs = h('b', { text: '0/' + g.pairs });

    var diff = h('div', { class: 'g-mem__diff', role: 'group', 'aria-label': 'Difficulty' });
    Object.keys(LEVELS).forEach(function (k) {
      var L = LEVELS[k];
      diff.appendChild(h('button', { type: 'button', class: 'g-btn g-btn--sm', 'aria-pressed': k === level ? 'true' : 'false',
        onclick: function () { if (k === level && !g.moves) return; level = k; newGame(false); var btn = stage.querySelector('.g-mem__diff [aria-pressed="true"]'); if (btn) btn.focus({ preventScroll: true }); live.textContent = L.label + ' board: ' + (L.cols * L.rows / 2) + ' pairs.'; } },
        [L.label + ' ' + L.cols + '×' + L.rows]));
    });

    grid = h('div', { class: 'g-mem__grid', role: 'group', 'aria-label': 'Memory cards. Use arrow keys to move between cards.' });
    grid.style.setProperty('--g-cols', String(cols()));
    g.deck.forEach(function (c, i) {
      var btn = h('button', { type: 'button', class: 'g-mem__card', 'data-i': String(i), 'aria-label': label(c, i) }, [
        h('span', { class: 'g-mem__inner', 'aria-hidden': 'true' }, [
          h('span', { class: 'g-mem__face g-mem__back' }),
          h('span', { class: 'g-mem__face g-mem__front' }, [
            h('span', { class: 'g-mem__emoji', text: c.face.e }),
            h('span', { class: 'g-mem__label', text: c.face.n })
          ])
        ])
      ]);
      btn.addEventListener('click', function () { flip(i); });
      btn.addEventListener('keydown', navKey);
      c.el = btn;
      grid.appendChild(btn);
    });

    stage.appendChild(h('section', { class: 'g-card g-pop', 'aria-labelledby': 'g-mem-title' }, [
      h('div', { class: 'g-head' }, [
        h('div', null, [
          h('h2', { class: 'g-title', id: 'g-mem-title', text: 'Flea Memory Match' }),
          h('p', { class: 'g-sub', text: 'Flip two cards at a time and pair up the vintage finds.' })
        ]),
        h('ul', { class: 'g-stats', 'aria-label': 'Game stats' }, [
          h('li', { class: 'g-stat' }, [statEls.moves, h('span', { text: 'Moves' })]),
          h('li', { class: 'g-stat g-stat--teal' }, [statEls.time, h('span', { text: 'Time' })]),
          h('li', { class: 'g-stat' }, [statEls.pairs, h('span', { text: 'Pairs' })])
        ])
      ]),
      h('div', { class: 'g-row' }, [diff, h('button', { type: 'button', class: 'g-btn g-btn--sm g-btn--ghost', onclick: function () { newGame(true); live.textContent = 'Cards reshuffled.'; } }, ['↻ Shuffle'])]),
      h('p', { class: 'g-mem__best', id: 'g-mem-best', text: 'Best ' + LEVELS[level].label + ' time: ' + (b ? fmt(b.t) + ' in ' + b.m + ' moves' : 'none yet — set the record!') }),
      grid
    ]));
    if (focusGrid) grid.firstChild.focus({ preventScroll: true });
  }

  function label(c, i) {
    var pos = 'Card ' + (i + 1);
    if (c.matched) return pos + ', ' + c.face.n + ', matched';
    if (c.up) return pos + ', ' + c.face.n;
    return pos + ', face down';
  }

  function navKey(e) {
    var i = Number(e.currentTarget.getAttribute('data-i'));
    var n = g.deck.length, c = cols(), t = null;
    if (e.key === 'ArrowRight') t = Math.min(n - 1, i + 1);
    else if (e.key === 'ArrowLeft') t = Math.max(0, i - 1);
    else if (e.key === 'ArrowDown') t = i + c < n ? i + c : i;
    else if (e.key === 'ArrowUp') t = i - c >= 0 ? i - c : i;
    else if (e.key === 'Home') t = 0;
    else if (e.key === 'End') t = n - 1;
    if (t != null) { e.preventDefault(); g.deck[t].el.focus(); }
  }

  function setCard(c, i) {
    c.el.classList.toggle('is-up', c.up || c.matched);
    c.el.classList.toggle('is-matched', c.matched);
    c.el.setAttribute('aria-label', label(c, i));
  }

  function flip(i) {
    if (g.done) return;
    var c = g.deck[i];
    if (g.lock || c.up || c.matched) return;
    if (!g.start) { g.start = Date.now(); timerId = window.setInterval(tick, 1000); }
    c.up = true;
    setCard(c, i);
    g.open.push(i);
    if (g.open.length < 2) { live.textContent = c.face.n + '.'; return; }

    g.moves++;
    var a = g.deck[g.open[0]], b = g.deck[g.open[1]];
    var ia = g.open[0], ib = g.open[1];
    g.open = [];
    if (a.face.n === b.face.n) {
      a.matched = b.matched = true;
      setCard(a, ia); setCard(b, ib);
      g.matched++;
      updateStats();
      live.textContent = 'Match! ' + a.face.n + '. ' + g.matched + ' of ' + g.pairs + ' pairs found.';
      if (g.matched === g.pairs) finish();
    } else {
      g.lock = true;
      a.el.classList.add('is-miss'); b.el.classList.add('is-miss');
      updateStats();
      live.textContent = b.face.n + '. No match with ' + a.face.n + '.';
      window.setTimeout(function () {
        a.up = b.up = false;
        a.el.classList.remove('is-miss'); b.el.classList.remove('is-miss');
        setCard(a, ia); setCard(b, ib);
        g.lock = false;
      }, 850);
    }
  }

  function finish() {
    g.done = true;
    stopTimer();
    g.elapsed = Math.max(1, Math.round((Date.now() - g.start) / 1000));
    updateStats();
    var all = bests();
    var prev = all[level];
    var isBest = !prev || g.elapsed < prev.t || (g.elapsed === prev.t && g.moves < prev.m);
    if (isBest) {
      all[level] = { t: g.elapsed, m: g.moves };
      store(BEST_KEY, all);
      var bestEl = stage.querySelector('#g-mem-best');
      if (bestEl) bestEl.textContent = 'Best ' + LEVELS[level].label + ' time: ' + fmt(g.elapsed) + ' in ' + g.moves + ' moves';
    }
    var perfect = g.moves === g.pairs;
    var rating = perfect ? ['🧠', 'Photographic Memory!'] : g.moves <= g.pairs * 1.5 ? ['🏆', 'Eagle-Eyed Picker'] : g.moves <= g.pairs * 2.2 ? ['🔍', 'Sharp Shopper'] : ['🛍️', 'Happy Browser'];

    var counts = {};
    g.deck.forEach(function (c) { counts[c.face.s] = (counts[c.face.s] || 0) + 1; });
    var topSlug = Object.keys(counts).sort(function (x, y) { return counts[y] - counts[x]; })[0];

    window.setTimeout(function () {
      var again = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: function () { panel.remove(); newGame(true); } }, ['↻ Play again']);
      var harder = level !== 'hard' ? h('button', { type: 'button', class: 'g-btn g-btn--ghost', onclick: function () { panel.remove(); level = level === 'easy' ? 'medium' : 'hard'; newGame(true); live.textContent = LEVELS[level].label + ' board.'; } }, ['Try ' + (level === 'easy' ? 'Medium' : 'Hard') + ' →']) : null;
      var panel = h('section', { class: 'g-card g-results g-pop', 'aria-labelledby': 'g-mem-res' }, [
        h('div', { class: 'g-results__badge', 'aria-hidden': 'true', text: rating[0] }),
        h('h2', { class: 'g-title', id: 'g-mem-res', tabindex: '-1', text: rating[1] }),
        h('p', { class: 'g-results__big', text: fmt(g.elapsed) }),
        h('p', { text: 'You matched all ' + g.pairs + ' pairs in ' + g.moves + ' moves on ' + LEVELS[level].label + '. ' + (isBest ? 'New best time! 🎉' : 'Best: ' + fmt(prev.t) + ' in ' + prev.m + ' moves.') }),
        h('div', { class: 'g-row g-row--center g-mt' }, [again, harder]),
        h('ul', { class: 'g-links' }, [
          linkItem(shopUrl(topSlug), '🏷️', 'Shop ' + SHOP_NAMES[topSlug], 'Find the real thing from our Houston dealers'),
          linkItem(shopUrl(topSlug === 'antiques-collectibles' ? 'vinyl-records-retro' : 'antiques-collectibles'), '🧭', 'Browse ' + (topSlug === 'antiques-collectibles' ? 'Vinyl Records & Retro' : 'Antiques & Collectibles'), 'More treasures to spot'),
          linkItem(amazon('vintage memory matching card game'), '🃏', 'Get a vintage-style memory game', 'On Amazon — for family game night', true)
        ]),
        h('p', { class: 'g-disclose', text: 'Amazon links are affiliate links; we may earn a small commission.' })
      ]);
      stage.insertBefore(panel, stage.firstChild);
      live.textContent = rating[1] + ' All pairs found in ' + fmt(g.elapsed) + ' with ' + g.moves + ' moves.' + (isBest ? ' New best time!' : '');
      var hd = panel.querySelector('#g-mem-res');
      if (hd) hd.focus({ preventScroll: false });
    }, 450);
  }

  function init() {
    root = document.querySelector('.game[data-game="' + SLUG + '"]') || document.getElementById('game-root');
    if (!root) return;
    root.innerHTML = '';
    stage = h('div', { class: 'g-stage' });
    live = h('p', { class: 'g-sr', 'aria-live': 'polite', role: 'status' });
    root.appendChild(stage);
    root.appendChild(live);
    try {
      narrowMq = window.matchMedia('(max-width: 599px)');
      var onChange = function () { if (grid) grid.style.setProperty('--g-cols', String(cols())); };
      if (narrowMq.addEventListener) narrowMq.addEventListener('change', onChange);
      else if (narrowMq.addListener) narrowMq.addListener(onChange);
    } catch (e) { narrowMq = null; }
    newGame(false);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
