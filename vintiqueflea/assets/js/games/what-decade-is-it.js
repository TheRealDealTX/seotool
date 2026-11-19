/* What Decade Is It? — Vintique Flea mini game */
(function () {
  'use strict';

  var SLUG = 'what-decade-is-it';
  var ROUNDS = 10;
  var BEST_KEY = 'vf_game_decade_best';
  var DECADES = ['1920s', '1930s', '1940s', '1950s', '1960s', '1970s', '1980s', '1990s'];

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
      else if (k === 'html') el.innerHTML = v;
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
  function linkItem(href, ico, label, sub, amz) {
    var a = h('a', { class: 'g-link', href: href }, [
      h('span', { class: 'g-link__ico', 'aria-hidden': 'true', text: ico }),
      h('span', null, [label, sub ? h('small', { text: sub }) : null])
    ]);
    if (amz) { a.target = '_blank'; a.rel = 'sponsored nofollow noopener'; }
    return h('li', null, [a]);
  }

  /* ---------- item bank: decade each item was popularized ---------- */
  var BANK = [
    { e: '💃', n: 'Beaded flapper dress', d: '1920s', s: 'vintage-clothing', hint: 'Dropped waist, fringe hem, made for dancing the Charleston.', f: 'Flapper hemlines rose to the knee — scandalous at the time — and the fringe was cut to shimmy on the dance floor.' },
    { e: '👒', n: 'Felt cloche hat', d: '1920s', s: 'vintage-clothing', hint: 'Bell-shaped and pulled low over a sleek bobbed haircut.', f: '"Cloche" is French for bell, and the snug shape only worked with the short bob hairstyles of the Jazz Age.' },
    { e: '📯', n: 'Wind-up Victrola phonograph', d: '1920s', s: 'antiques-collectibles', hint: 'Crank it by hand — no electricity needed to spin a 78.', f: 'Victor hid the horn inside a wooden cabinet so the record player looked like fine parlor furniture.' },
    { e: '☎️', n: 'Western Electric 302 rotary phone', d: '1930s', s: 'antiques-collectibles', hint: 'Heavy black desk phone with the dial and handset all in one.', f: 'Styled with industrial designer Henry Dreyfuss and introduced in 1937, the 302 was built to survive almost anything.' },
    { e: '📻', n: 'Cathedral-arch tabletop radio', d: '1930s', s: 'antiques-collectibles', hint: 'A wooden Gothic arch the family gathered around for evening broadcasts.', f: 'Compact "cathedral" sets like the Philco 90 brought Depression-era families serials, music and FDR\'s fireside chats.' },
    { e: '🍽️', n: 'Fiesta dinnerware', d: '1930s', s: 'vintage-kitchen-barware', hint: 'Bold solid-color plates with concentric rings, meant to be mixed and matched.', f: 'Homer Laughlin launched Fiesta in 1936 — and the original orange-red glaze contained uranium oxide.' },
    { e: '🟠', n: 'Carved Bakelite bangles', d: '1930s', s: 'antiques-collectibles', hint: 'Chunky, colorful jewelry made from an early plastic.', f: 'Bakelite was the first fully synthetic plastic, and its cheap, cheerful bangles were a Depression-era hit.' },
    { e: '🎶', n: 'Wurlitzer 1015 jukebox', d: '1940s', s: 'vinyl-records-retro', hint: 'Glowing bubble tubes and a nickel a play at the soda fountain.', f: 'Introduced in 1946, the 1015 sold around 56,000 units and became the defining image of the jukebox.' },
    { e: '🕴️', n: 'Zoot suit', d: '1940s', s: 'vintage-clothing', hint: 'Sky-high trousers, a knee-length coat and a long watch chain.', f: 'The exaggerated suits were tied to swing culture — and to the 1943 Zoot Suit Riots in Los Angeles.' },
    { e: '🧦', n: 'Seamed nylon stockings', d: '1940s', s: 'vintage-clothing', hint: 'A brand-new miracle fiber that caused riots at department stores.', f: 'Nylons debuted nationally in 1940; during wartime shortages, women drew seams on their legs with eyebrow pencil.' },
    { e: '🎟️', n: 'War ration book', d: '1940s', s: 'antiques-collectibles', hint: 'Stamps you needed to buy sugar, coffee and meat on the home front.', f: 'The U.S. issued ration books starting in 1942, and many families tucked theirs away as keepsakes.' },
    { e: '🪑', n: 'Eames-style lounge chair & ottoman', d: '1950s', s: 'mid-century-modern', hint: 'Molded plywood shells and leather cushions, "like a well-used baseball mitt."', f: 'Charles and Ray Eames debuted their lounge chair on live national TV in 1956.' },
    { e: '🐩', n: 'Poodle skirt', d: '1950s', s: 'vintage-clothing', hint: 'A felt circle skirt with an appliqué pet, worn over petticoats to the sock hop.', f: 'Easy to sew at home from a single circle of felt, the skirt became a teen uniform of the rock-and-roll era.' },
    { e: '🥣', n: 'Pyrex Butterprint mixing bowls', d: '1950s', s: 'vintage-kitchen-barware', hint: 'Turquoise-on-white bowls with roosters and farm couples.', f: 'Pyrex introduced the Butterprint pattern in 1957, and complete nesting sets are still hunted by collectors.' },
    { e: '⭕', n: 'Hula hoop', d: '1950s', s: 'vinyl-records-retro', hint: 'A plastic ring you keep spinning with your hips.', f: 'Wham-O launched its hoop in 1958 and sold tens of millions in a matter of months.' },
    { e: '📺', n: 'TV dinner tray', d: '1950s', s: 'vintage-kitchen-barware', hint: 'Turkey, peas and sweet potatoes in a compartmented aluminum tray.', f: 'Swanson\'s 1953 TV dinner was born from a surplus of Thanksgiving turkey and a new love of the living-room set.' },
    { e: '✴️', n: 'Starburst wall clock', d: '1950s', s: 'mid-century-modern', hint: 'Brass rays shooting out from the center, inspired by the Atomic Age.', f: 'Designers like George Nelson turned atomic and space-age imagery into sunburst clocks for the modern home.' },
    { e: '🫧', n: 'Lava lamp', d: '1960s', s: 'vinyl-records-retro', hint: 'Glowing blobs of wax drift up and down a tapered bottle.', f: 'British inventor Edward Craven Walker introduced his "Astro" lamp in 1963, and it became a psychedelic staple.' },
    { e: '👢', n: 'White go-go boots', d: '1960s', s: 'vintage-clothing', hint: 'Low-heeled, mid-calf and made for Mod mini dresses.', f: 'French designer André Courrèges sent white boots down the runway in 1964, and dance-show go-go girls made them famous.' },
    { e: '🧥', n: 'Nehru jacket', d: '1960s', s: 'vintage-clothing', hint: 'A slim tailored jacket with a stand-up mandarin collar.', f: 'Named for India\'s first prime minister, the look swept Western menswear in the mid-to-late \'60s.' },
    { e: '🌈', n: 'Hand-dyed tie-dye shirt', d: '1960s', s: 'vintage-clothing', hint: 'Rubber bands, buckets of dye and a Summer of Love vibe.', f: 'The ancient technique exploded with the counterculture around 1967\'s Summer of Love.' },
    { e: '🧶', n: 'Shag carpet', d: '1970s', s: 'rustic-home-decor', hint: 'Deep, fluffy pile you could lose a contact lens in.', f: 'Wall-to-wall shag in orange, gold and brown defined the conversation pits of the \'70s.' },
    { e: '🥑', n: 'Avocado-green refrigerator', d: '1970s', s: 'vintage-kitchen-barware', hint: 'Matched the harvest gold oven and the brown-and-orange wallpaper.', f: 'Avocado green and harvest gold were the must-have appliance colors of the decade.' },
    { e: '💍', n: 'Mood ring', d: '1970s', s: 'antiques-collectibles', hint: 'Its stone supposedly changes color with your feelings.', f: 'Introduced in 1975, mood rings used heat-sensitive liquid crystals — they read your skin temperature, not your soul.' },
    { e: '📼', n: '8-track tape player', d: '1970s', s: 'vinyl-records-retro', hint: 'Chunky cartridges that clunked between tracks mid-song.', f: 'Born in the mid-\'60s for car stereos, the 8-track hit its peak in the \'70s before cassettes took over.' },
    { e: '🪩', n: 'Mirrored disco ball', d: '1970s', s: 'vinyl-records-retro', hint: 'Hundreds of tiny mirrors spinning above the dance floor.', f: 'Mirror balls date back to the 1920s, but disco and Studio 54 made them icons.' },
    { e: '🪨', n: 'Pet Rock', d: '1970s', s: 'antiques-collectibles', hint: 'A smooth stone in a cardboard carrier with an owner\'s manual.', f: 'Ad man Gary Dahl sold over a million Pet Rocks in 1975 — the ultimate low-maintenance pet.' },
    { e: '📸', n: 'Polaroid SX-70 camera', d: '1970s', s: 'antiques-collectibles', hint: 'A folding instant camera — watch the picture appear in your hand.', f: 'Launched in 1972, the SX-70 was the first folding SLR instant camera with self-developing film.' },
    { e: '🎧', n: 'Sony Walkman', d: '1980s', s: 'vinyl-records-retro', hint: 'Your mixtape, foam headphones and a belt clip.', f: 'The first Walkman arrived in 1979 and made music portable all through the \'80s — it even had two headphone jacks.' },
    { e: '🧩', n: 'Rubik\'s Cube', d: '1980s', s: 'vinyl-records-retro', hint: 'Six colors, nine squares a side, endless frustration.', f: 'Invented in 1974, it went worldwide in 1980; there are over 43 quintillion possible positions.' },
    { e: '🔊', n: 'Boombox', d: '1980s', s: 'vinyl-records-retro', hint: 'Dual tape decks, big speakers, carried on the shoulder.', f: 'Portable "ghetto blasters" powered street dance and early hip-hop culture.' },
    { e: '🩰', n: 'Neon leg warmers', d: '1980s', s: 'vintage-clothing', hint: 'Dancewear turned street style, thanks to aerobics videos.', f: 'Movies like Fame (1980) and Flashdance (1983) took leg warmers out of the ballet studio.' },
    { e: '👾', n: 'Pac-Man arcade cabinet', d: '1980s', s: 'vinyl-records-retro', hint: 'A yellow circle, four ghosts and a maze full of dots.', f: 'Namco released Pac-Man in 1980, and it became one of the highest-grossing arcade games ever.' },
    { e: '🥚', n: 'Tamagotchi', d: '1990s', s: 'vinyl-records-retro', hint: 'An egg-shaped keychain pet that needs feeding — even during class.', f: 'Bandai launched the digital pet in Japan in 1996 and sold tens of millions worldwide.' },
    { e: '🧸', n: 'Beanie Babies', d: '1990s', s: 'antiques-collectibles', hint: 'Under-stuffed plush animals with a heart-shaped tag you never removed.', f: 'Ty introduced them in 1993; collectors kept the tags on, convinced they\'d fund retirement.' },
    { e: '🌀', n: 'Slap bracelet', d: '1990s', s: 'vintage-clothing', hint: 'A flat metal strip that curls around your wrist with one smack.', f: 'Invented in 1990, slap bracelets were so popular some schools banned them.' },
    { e: '👕', n: 'Oversized flannel shirt', d: '1990s', s: 'vintage-clothing', hint: 'Plaid, unbuttoned, worn over a band tee — very Seattle.', f: 'Grunge bands like Nirvana and Pearl Jam made thrift-store flannel a fashion statement.' }
  ];

  var SHOP_NAMES = {
    'mid-century-modern': 'Mid-Century Modern',
    'vintage-clothing': 'Vintage Clothing',
    'antiques-collectibles': 'Antiques & Collectibles',
    'vinyl-records-retro': 'Vinyl Records & Retro',
    'vintage-kitchen-barware': 'Vintage Kitchen & Barware',
    'rustic-home-decor': 'Rustic Home Decor'
  };

  /* ---------- state ---------- */
  var root, stage, live, state;

  function newGame() {
    state = {
      rounds: shuffle(BANK).slice(0, ROUNDS).map(function (item) {
        var wrong = shuffle(DECADES.filter(function (d) { return d !== item.d; })).slice(0, 3);
        var opts = wrong.concat(item.d).sort();
        return { item: item, opts: opts };
      }),
      i: 0, score: 0, streak: 0, bestStreak: 0, answered: false, missed: {}
    };
    renderRound();
  }

  function bestScore() { var b = store(BEST_KEY); return typeof b === 'number' ? b : 0; }

  function statsBar() {
    return h('ul', { class: 'g-stats', 'aria-label': 'Score' }, [
      h('li', { class: 'g-stat' }, [h('b', { text: String(Math.min(state.i + 1, ROUNDS)) + '/' + ROUNDS }), h('span', { text: 'Round' })]),
      h('li', { class: 'g-stat g-stat--teal' }, [h('b', { text: String(state.score) }), h('span', { text: 'Score' })]),
      h('li', { class: 'g-stat' }, [h('b', { text: (state.streak >= 3 ? '🔥' : '') + state.streak }), h('span', { text: 'Streak' })]),
      h('li', { class: 'g-stat' }, [h('b', { text: String(bestScore()) }), h('span', { text: 'Best' })])
    ]);
  }

  function header() {
    return h('div', { class: 'g-head' }, [
      h('div', null, [
        h('h2', { class: 'g-title', text: 'What Decade Is It?' }),
        h('p', { class: 'g-sub', text: 'Guess when each find was all the rage.' })
      ]),
      statsBar()
    ]);
  }

  function renderRound() {
    var r = state.rounds[state.i];
    state.answered = false;
    stage.innerHTML = '';
    var fb = h('div', { class: 'g-feedback', id: 'g-dec-fb' });
    var next = h('button', { type: 'button', class: 'g-btn g-btn--rust', hidden: true, onclick: advance },
      [state.i === ROUNDS - 1 ? 'See results →' : 'Next item →']);
    var opts = h('div', { class: 'g-decade__opts', role: 'group', 'aria-label': 'Choose a decade' },
      r.opts.map(function (d) {
        return h('button', { type: 'button', class: 'g-decade__opt', 'data-d': d, onclick: function () { answer(d, opts, fb, next); } }, [d]);
      }));
    var card = h('section', { class: 'g-card g-pop', 'aria-labelledby': 'g-dec-name' }, [
      header(),
      h('div', { class: 'g-progress', role: 'progressbar', 'aria-label': 'Progress', 'aria-valuemin': '0', 'aria-valuemax': String(ROUNDS), 'aria-valuenow': String(state.i) },
        [h('i', { style: 'width:' + (state.i / ROUNDS * 100) + '%' })]),
      h('div', { class: 'g-decade__stage g-mt' }, [
        h('div', { class: 'g-decade__art', 'aria-hidden': 'true', text: r.item.e }),
        h('div', null, [
          h('h3', { class: 'g-decade__name', id: 'g-dec-name', text: r.item.n }),
          h('p', { class: 'g-decade__hint' }, [h('b', { text: 'Hint: ' }), r.item.hint])
        ])
      ]),
      opts, fb,
      h('div', { class: 'g-row g-mt' }, [next])
    ]);
    stage.appendChild(card);
    var first = opts.querySelector('button');
    if (state.i > 0 && first) first.focus({ preventScroll: true });
  }

  function answer(d, opts, fb, next) {
    if (state.answered) return;
    state.answered = true;
    var r = state.rounds[state.i];
    var right = d === r.item.d;
    Array.prototype.forEach.call(opts.querySelectorAll('button'), function (b) {
      b.disabled = true;
      var bd = b.getAttribute('data-d');
      if (bd === r.item.d) b.classList.add('is-right');
      else if (bd === d) b.classList.add('is-wrong');
      else b.classList.add('is-dim');
    });
    if (right) {
      state.streak++;
      state.score += 1;
      state.bestStreak = Math.max(state.bestStreak, state.streak);
    } else {
      state.streak = 0;
      state.missed[r.item.s] = (state.missed[r.item.s] || 0) + 1;
    }
    var head = right
      ? (state.streak >= 3 ? 'Groovy — ' + state.streak + ' in a row!' : 'Right on!')
      : 'Not quite — it\'s the ' + r.item.d + '.';
    fb.className = 'g-feedback ' + (right ? 'g-feedback--good' : 'g-feedback--bad');
    fb.innerHTML = '';
    fb.appendChild(h('strong', { text: head + ' ' }));
    fb.appendChild(document.createTextNode(r.item.f));
    if (!right) { var art = root.querySelector('.g-decade__art'); if (art) { art.classList.remove('g-shake'); void art.offsetWidth; art.classList.add('g-shake'); } }
    // refresh stats in place
    var old = root.querySelector('.g-stats');
    if (old) old.parentNode.replaceChild(statsBar(), old);
    live.textContent = head + ' ' + r.item.f + ' Score ' + state.score + ' of ' + (state.i + 1) + '.';
    next.hidden = false;
    next.focus({ preventScroll: true });
  }

  function advance() {
    state.i++;
    if (state.i >= ROUNDS) renderResults();
    else renderRound();
  }

  function renderResults() {
    var prevBest = bestScore();
    var isBest = state.score > prevBest;
    if (isBest) store(BEST_KEY, state.score);
    var rank =
      state.score >= 9 ? ['🏆', 'Certified Time Traveler', 'You could date a find from across the flea market floor.'] :
      state.score >= 7 ? ['🕰️', 'Seasoned Picker', 'Dealers are going to start asking YOU for appraisals.'] :
      state.score >= 4 ? ['🔍', 'Weekend Treasure Hunter', 'A few more Saturdays browsing booths and you\'ll be a pro.'] :
      ['🛍️', 'Fresh Rookie', 'Every collector starts somewhere — come wander the aisles and learn.'];

    // Pick the category they tripped over most (or the most common category played)
    var counts = {};
    state.rounds.forEach(function (r) { counts[r.item.s] = (counts[r.item.s] || 0) + 1; });
    var src = Object.keys(state.missed).length ? state.missed : counts;
    var topSlug = Object.keys(src).sort(function (a, b) { return src[b] - src[a]; })[0] || 'antiques-collectibles';
    var second = topSlug === 'antiques-collectibles' ? 'vinyl-records-retro' : 'antiques-collectibles';

    stage.innerHTML = '';
    var again = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: newGame }, ['↻ Play again']);
    stage.appendChild(h('section', { class: 'g-card g-results g-pop', 'aria-labelledby': 'g-dec-res' }, [
      h('div', { class: 'g-results__badge', 'aria-hidden': 'true', text: rank[0] }),
      h('h2', { class: 'g-title', id: 'g-dec-res', text: rank[1] }),
      h('p', { class: 'g-results__big', text: state.score + ' / ' + ROUNDS }),
      h('p', { text: rank[2] }),
      h('p', { class: 'g-sub', text: 'Best streak: ' + state.bestStreak + ' · ' + (isBest ? 'New personal best! 🎉' : 'Personal best: ' + Math.max(prevBest, state.score)) }),
      h('div', { class: 'g-row g-row--center g-mt' }, [again]),
      h('ul', { class: 'g-links' }, [
        linkItem(shopUrl(topSlug), '🏷️', 'Browse ' + (SHOP_NAMES[topSlug] || 'the shop'), 'Brush up on real finds from our Houston dealers'),
        linkItem(shopUrl(second), '🧭', 'Explore ' + SHOP_NAMES[second], 'More eras, more stories'),
        linkItem(amazon('antiques collectibles price guide book'), '📚', 'Get a collector\'s price guide', 'On Amazon', true)
      ]),
      h('p', { class: 'g-disclose', text: 'Amazon links are affiliate links; we may earn a small commission.' })
    ]));
    live.textContent = 'Game over. You scored ' + state.score + ' out of ' + ROUNDS + '. ' + rank[1] + '.';
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
