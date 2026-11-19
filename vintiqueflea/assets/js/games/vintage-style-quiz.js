/* What's Your Vintage Style? — Vintique Flea quiz */
(function () {
  'use strict';

  var SLUG = 'vintage-style-quiz';
  var LAST_KEY = 'vf_game_style_last';

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
  function reduced() {
    try { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { return false; }
  }
  function linkItem(href, ico, label, sub, amz) {
    var a = h('a', { class: 'g-link', href: href }, [
      h('span', { class: 'g-link__ico', 'aria-hidden': 'true', text: ico }),
      h('span', null, [label, sub ? h('small', { text: sub }) : null])
    ]);
    if (amz) { a.target = '_blank'; a.rel = 'sponsored nofollow noopener'; }
    return h('li', null, [a]);
  }

  /* ---------- styles ---------- */
  var STYLES = {
    mcm: {
      name: 'Mid-Century Modern', e: '🪑', bg: '#e9be52', slug: 'mid-century-modern', also: 'retro',
      desc: 'Clean lines, warm walnut and a dash of atomic-age optimism. You love furniture that\'s as sculptural as it is functional — tapered legs, sunburst clocks and a well-stocked bar cart. Your home looks like it could star in a 1960s design magazine.',
      picks: [['Sunburst wall clock', 'mid century modern sunburst wall clock', '✴️'], ['Tapered-leg side table', 'mid century modern side table tapered legs', '🪵'], ['Atomic-print throw pillow', 'atomic mid century throw pillow cover', '🛋️']]
    },
    industrial: {
      name: 'Industrial Salvage', e: '🏭', bg: '#9aa3a8', slug: 'architectural-salvage-industrial', also: 'farmhouse',
      desc: 'Raw steel, reclaimed wood and the patina of a hard-working past. You see potential in factory carts, old lockers and salvaged doors, and you\'d rather tell a piece\'s backstory than buy it new. Exposed brick? Yes, please.',
      picks: [['Edison-bulb pendant light', 'industrial edison bulb pendant light', '💡'], ['Pipe & wood shelving', 'industrial pipe wood shelving', '🔩'], ['Factory-cart coffee table', 'industrial cart coffee table casters', '🛒']]
    },
    farmhouse: {
      name: 'Rustic Farmhouse', e: '🌾', bg: '#c9b78f', slug: 'rustic-home-decor', also: 'antique',
      desc: 'Barnwood, galvanized metal and a long table full of friends. Your style is cozy, unfussy and a little bit Texas — ironstone pitchers of wildflowers, worn-in quilts and crates that hold everything. Home should feel like a warm welcome.',
      picks: [['Galvanized metal decor', 'galvanized metal farmhouse decor', '🪣'], ['Ironstone-style pitcher', 'white ironstone style pitcher vase', '🫗'], ['Rustic wooden crate', 'rustic wooden crate decor', '📦']]
    },
    boho: {
      name: 'Boho Vintage Fashion', e: '🌼', bg: '#d77d58', slug: 'vintage-clothing', also: 'retro',
      desc: 'Free-spirited, layered and always one-of-a-kind. You gravitate to embroidered blouses, suede fringe, turquoise jewelry and macramé. Your closet is a time machine to the \'60s and \'70s, and every piece has a story from a booth or a road trip.',
      picks: [['Fringe suede crossbody bag', 'boho fringe suede crossbody bag', '👜'], ['Macramé wall hanging', 'macrame wall hanging boho', '🪢'], ['Embroidered peasant blouse', 'vintage style embroidered peasant blouse', '👚']]
    },
    retro: {
      name: 'Retro Collector', e: '💿', bg: '#4f938e', slug: 'vinyl-records-retro', also: 'mcm',
      desc: 'Vinyl, neon and joyful kitsch. You\'re the one flipping through record crates and spotting the vintage lunchbox across the aisle. Your space is a playlist of decades — jukebox colors, lava lamps and shelves of curated treasures.',
      picks: [['Retro-style turntable', 'vintage style record player turntable', '🎶'], ['Vinyl record storage crate', 'vinyl record storage crate', '📦'], ['Lava lamp', 'lava lamp', '🫧']]
    },
    antique: {
      name: 'Antique Romantic', e: '🕯️', bg: '#e3c3b8', slug: 'antiques-collectibles', also: 'boho',
      desc: 'Gilded frames, fine china and things that whisper of another century. You love heirlooms, velvet, brass candlesticks and the thrill of an estate-sale find. Your home feels storied, elegant and just a little bit enchanted.',
      picks: [['Brass candlestick set', 'vintage brass candlestick holders', '🕯️'], ['Gilded ornate mirror', 'antique style gold ornate mirror', '🪞'], ['Floral teacup set', 'vintage floral teacup and saucer set', '☕']]
    }
  };
  var STYLE_KEYS = ['mcm', 'industrial', 'farmhouse', 'boho', 'retro', 'antique'];

  var QUESTIONS = [
    { q: 'Pick your perfect Saturday morning:', a: [
      ['mcm', '🏠', 'Touring modernist homes'], ['industrial', '🏗️', 'Poking around an old warehouse'], ['farmhouse', '🧺', 'Farmers market & fresh bread'],
      ['boho', '👗', 'Thrifting a festival outfit'], ['retro', '💿', 'Digging through record crates'], ['antique', '🫖', 'An estate sale with a thermos of tea']] },
    { q: 'Your dream sofa is…', a: [
      ['mcm', '🛋️', 'Low, walnut-framed and tufted'], ['industrial', '🧳', 'Cognac leather on a steel frame'], ['farmhouse', '🧵', 'A slipcovered linen sink-in'],
      ['boho', '🧶', 'Floor cushions and kilim pillows'], ['retro', '🍒', 'Cherry-red vinyl with chrome'], ['antique', '👑', 'A velvet Victorian settee']] },
    { q: 'Choose a color palette:', a: [
      ['mcm', '🟡', 'Mustard, teal & walnut'], ['industrial', '⚙️', 'Charcoal, rust & raw steel'], ['farmhouse', '🌿', 'Cream, sage & barnwood'],
      ['boho', '🧡', 'Terracotta, saffron & indigo'], ['retro', '🌈', 'Turquoise, pink & neon'], ['antique', '🌸', 'Blush, ivory & gold']] },
    { q: 'You spot it across the aisle. You can\'t pass up…', a: [
      ['mcm', '🪑', 'A molded shell chair'], ['industrial', '💡', 'A salvaged factory pendant light'], ['farmhouse', '🫗', 'An ironstone pitcher'],
      ['boho', '🧥', 'A suede fringe jacket'], ['retro', '🎮', 'A tin lunchbox & board games'], ['antique', '💍', 'A cameo brooch']] },
    { q: 'Put on a record. Which one?', a: [
      ['mcm', '🎷', 'Cool West Coast jazz'], ['industrial', '🎸', 'Gritty Texas blues'], ['farmhouse', '🪕', 'Bluegrass & folk'],
      ['boho', '🌼', 'Laurel Canyon singer-songwriters'], ['retro', '📻', 'Doo-wop & Motown hits'], ['antique', '🎻', 'A string quartet']] },
    { q: 'Your statement wall features…', a: [
      ['mcm', '✴️', 'A sunburst clock'], ['industrial', '🧱', 'Exposed brick & old signage'], ['farmhouse', '🪵', 'Shiplap and a grapevine wreath'],
      ['boho', '🪢', 'Macramé and a tapestry'], ['retro', '🎨', 'Framed album covers & a neon sign'], ['antique', '🖼️', 'Oil portraits in gilt frames']] },
    { q: 'You\'re hosting. What\'s on the menu?', a: [
      ['mcm', '🍸', 'Martinis from the bar cart'], ['industrial', '🌮', 'Food-truck tacos & craft beer'], ['farmhouse', '🥧', 'Sunday supper & pie'],
      ['boho', '🧺', 'A picnic on a blanket'], ['retro', '🥤', 'Milkshakes & a jukebox'], ['antique', '☕', 'High tea on fine china']] },
    { q: 'Pick a movie set to live in:', a: [
      ['mcm', '🏙️', 'A 1960s Madison Avenue office'], ['industrial', '🍺', 'A converted brewery loft'], ['farmhouse', '🤠', 'A Hill Country ranch house'],
      ['boho', '🚌', 'A \'70s band\'s tour bus'], ['retro', '🍔', 'A neon roadside diner'], ['antique', '🏰', 'A Regency-era country estate']] }
  ];

  /* ---------- state ---------- */
  var root, stage, live, state;

  function newQuiz() {
    state = {
      i: 0,
      answers: [],
      order: QUESTIONS.map(function (q) { return shuffle(q.a); })
    };
    renderQuestion();
  }

  function renderQuestion() {
    var q = QUESTIONS[state.i];
    stage.innerHTML = '';
    var heading = h('h3', { class: 'g-quiz__q', id: 'g-quiz-q', tabindex: '-1', text: q.q });
    var opts = h('div', { class: 'g-quiz__opts', role: 'group', 'aria-labelledby': 'g-quiz-q' });
    state.order[state.i].forEach(function (a) {
      var st = STYLES[a[0]];
      var picked = state.answers[state.i] === a[0];
      var btn = h('button', { type: 'button', class: 'g-quiz__opt' + (picked ? ' is-picked' : ''), 'aria-pressed': picked ? 'true' : 'false', onclick: function () { choose(a[0], btn, opts); } }, [
        h('span', { class: 'g-quiz__pic', style: 'background:' + st.bg + '33', 'aria-hidden': 'true', text: a[1] }),
        h('span', { text: a[2] })
      ]);
      opts.appendChild(btn);
    });
    var back = h('button', { type: 'button', class: 'g-btn g-btn--sm', disabled: state.i === 0, onclick: function () { state.i = Math.max(0, state.i - 1); renderQuestion(); focusHeading(); } }, ['← Back']);
    stage.appendChild(h('section', { class: 'g-card g-pop', 'aria-labelledby': 'g-quiz-title' }, [
      h('div', { class: 'g-head' }, [
        h('div', null, [
          h('h2', { class: 'g-title', id: 'g-quiz-title', text: 'What\'s Your Vintage Style?' }),
          h('p', { class: 'g-sub', text: '8 quick questions. No wrong answers — just your taste.' })
        ]),
        h('ul', { class: 'g-stats' }, [h('li', { class: 'g-stat g-stat--teal' }, [h('b', { text: (state.i + 1) + '/' + QUESTIONS.length }), h('span', { text: 'Question' })])])
      ]),
      h('div', { class: 'g-progress', role: 'progressbar', 'aria-label': 'Quiz progress', 'aria-valuemin': '0', 'aria-valuemax': String(QUESTIONS.length), 'aria-valuenow': String(state.i) },
        [h('i', { style: 'width:' + (state.i / QUESTIONS.length * 100) + '%' })]),
      heading, opts,
      h('div', { class: 'g-row g-mt' }, [back])
    ]));
  }

  function focusHeading() {
    var hd = stage.querySelector('#g-quiz-q');
    if (hd) hd.focus({ preventScroll: true });
  }

  var busy = false;
  function choose(key, btn, opts) {
    if (busy) return;
    busy = true;
    state.answers[state.i] = key;
    Array.prototype.forEach.call(opts.children, function (b) { b.classList.toggle('is-picked', b === btn); b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
    window.setTimeout(function () {
      busy = false;
      if (state.i < QUESTIONS.length - 1) {
        state.i++;
        renderQuestion();
        live.textContent = 'Question ' + (state.i + 1) + ' of ' + QUESTIONS.length + '.';
        focusHeading();
      } else {
        renderResult();
      }
    }, reduced() ? 0 : 260);
  }

  function tally() {
    var sc = {};
    STYLE_KEYS.forEach(function (k) { sc[k] = 0; });
    state.answers.forEach(function (k, idx) {
      sc[k] += 3;
      sc[STYLES[k].also] += 1;
      if (idx === state.answers.length - 1) sc[k] += 0.1; // tie-breaker: final answer
    });
    var total = STYLE_KEYS.reduce(function (t, k) { return t + sc[k]; }, 0) || 1;
    var ranked = STYLE_KEYS.slice().sort(function (a, b) { return sc[b] - sc[a]; });
    return { sc: sc, total: total, ranked: ranked };
  }

  function copyText(text, done) {
    function fallback() {
      var ta = h('textarea', { 'aria-hidden': 'true', readonly: true, style: 'position:fixed;top:0;left:0;width:1px;height:1px;opacity:0' });
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
      ta.remove();
      done(ok);
    }
    try {
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
        return;
      }
    } catch (e) {}
    fallback();
  }

  function renderResult() {
    var t = tally();
    var top = t.ranked[0], st = STYLES[top], runner = STYLES[t.ranked[1]];
    var pct = function (k) { return Math.round(t.sc[k] / t.total * 100); };
    store(LAST_KEY, { style: top, at: Date.now() });

    var shareUrl = '';
    try { shareUrl = window.location.href.split('#')[0]; } catch (e) {}
    var shareText = 'My vintage style is ' + st.name + ' ' + st.e + ' (' + pct(top) + '% match, with a dash of ' + runner.name + ')! Find yours at Vintique Flea' + (shareUrl ? ': ' + shareUrl : '.');

    var copyMsg = h('p', { class: 'g-sub', style: 'min-height:1.4em', 'aria-hidden': 'true' });
    var copyBtn = h('button', { type: 'button', class: 'g-btn g-btn--teal', onclick: function () {
      copyText(shareText, function (ok) {
        if (ok) { copyMsg.textContent = 'Copied! Paste it anywhere to share.'; live.textContent = 'Result copied to clipboard.'; }
        else {
          copyMsg.textContent = '';
          var inp = h('input', { type: 'text', readonly: true, class: 'g-btn', style: 'width:100%;max-width:460px;border-radius:10px;font-weight:400', 'aria-label': 'Your result text — select and copy it' });
          inp.value = shareText;
          copyMsg.appendChild(inp);
          copyMsg.removeAttribute('aria-hidden');
          inp.focus(); inp.select();
          live.textContent = 'Copy is not available; the result text is selected so you can copy it.';
        }
      });
    } }, ['📋 Copy my result']);
    var again = h('button', { type: 'button', class: 'g-btn g-btn--rust', onclick: function () { newQuiz(); focusHeading(); } }, ['↻ Take it again']);

    var bars = h('ul', { class: 'g-quiz__bars', 'aria-label': 'Your style mix' }, t.ranked.map(function (k) {
      return h('li', null, [
        h('span', { text: STYLES[k].e + ' ' + STYLES[k].name }),
        h('span', { class: 'g-quiz__bar', 'aria-hidden': 'true' }, [h('i', { style: 'width:' + pct(k) + '%;' + (k === top ? '' : 'background:var(--teal,#1f6f6b)') })]),
        h('b', { text: pct(k) + '%' })
      ]);
    }));

    stage.innerHTML = '';
    stage.appendChild(h('section', { class: 'g-card g-results g-quiz__result g-pop', 'aria-labelledby': 'g-quiz-res' }, [
      h('p', { class: 'g-sub', style: 'text-transform:uppercase;letter-spacing:.12em;font-weight:700', text: 'Your vintage style is' }),
      h('div', { class: 'g-quiz__resultpic', style: 'background:' + st.bg, 'aria-hidden': 'true', text: st.e }),
      h('h2', { class: 'g-title', id: 'g-quiz-res', text: st.name }),
      h('p', { class: 'g-results__big', style: 'font-size:1.6rem', text: pct(top) + '% match' }),
      h('p', { text: st.desc }),
      h('p', { class: 'g-sub', text: 'Runner-up: ' + runner.e + ' ' + runner.name + ' — mix them for a look that\'s all yours.' }),
      bars,
      h('div', { class: 'g-row g-row--center g-mt' }, [copyBtn, again]),
      copyMsg,
      h('ul', { class: 'g-links' }, [linkItem(shopUrl(st.slug), '🏷️', 'Shop ' + st.name + ' at Vintique Flea', 'One-of-a-kind finds from our Houston dealers')]),
      h('h3', { class: 'g-sub', style: 'font-weight:700;margin-top:18px', text: '3 picks for your style' }),
      h('ul', { class: 'g-links', style: 'margin-top:8px' }, st.picks.map(function (p) { return linkItem(amazon(p[1]), p[2], p[0], 'On Amazon', true); })),
      h('p', { class: 'g-disclose', text: 'Amazon links are affiliate links; we may earn a small commission.' })
    ]));
    live.textContent = 'Your vintage style is ' + st.name + ', ' + pct(top) + ' percent match.';
    var hd = stage.querySelector('#g-quiz-res');
    if (hd) { hd.setAttribute('tabindex', '-1'); hd.focus({ preventScroll: true }); }
  }

  function init() {
    root = document.querySelector('.game[data-game="' + SLUG + '"]') || document.getElementById('game-root');
    if (!root) return;
    root.innerHTML = '';
    stage = h('div', { class: 'g-stage' });
    live = h('p', { class: 'g-sr', 'aria-live': 'polite', role: 'status' });
    root.appendChild(stage);
    root.appendChild(live);
    newQuiz();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
