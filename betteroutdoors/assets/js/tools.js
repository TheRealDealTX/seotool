/* Better Outdoors - interactive tool logic. Each block runs only when its tool is on the page. */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var fill = window.BO_fillRange || function () {};
  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  var BOWS = [
    { name: 'Mathews Prima', url: '/mathews-prima-level-1-package/', dl: [21.5, 27.5] },
    { name: 'Mathews Lift 29.5', url: '/mathews-lift-29-5/', dl: [24.5, 30] },
    { name: 'PSE Evolve 28', url: '/2018-pse-evolve-28/', dl: [24.5, 30] },
    { name: 'Bear Alaskan XT RTH', url: '/bear-archery-alaskan-xt-rth-compound-bow/', dl: [25, 30] },
    { name: 'Bear Persist', url: '/bear-archery-persist-compound-bow/', dl: [25, 30] },
    { name: 'Bear Persist 33', url: '/bear-archery-persist-compound-bow/', dl: [26.5, 30.5] },
    { name: 'Bear Whitetail Maxx RTH', url: '/bear-archery-whitetail-maxx-rth-compound-bow/', dl: [26, 30] }
  ];

  /* ---------- Draw length ---------- */
  var dlTool = $('[data-tool="draw-length"]');
  if (dlTool) {
    var mode = 'wingspan', ws = $('#dl-ws'), ht = $('#dl-h'), unit = $('#dl-unit'), rel = $('#dl-release');
    function fmtLen(v) { return unit.value === 'cm' ? Math.round(v * 2.54) + ' cm' : v + ' in'; }
    function fmtHeight(v) { return unit.value === 'cm' ? Math.round(v * 2.54) + ' cm' : Math.floor(v / 12) + ' ft ' + (v % 12) + ' in'; }
    function calc() {
      var base = mode === 'wingspan' ? +ws.value : +ht.value;
      var dl = Math.round((base / 2.5 + (+rel.value)) * 2) / 2;
      $('#dl-ws-out').textContent = fmtLen(+ws.value);
      $('#dl-h-out').textContent = fmtHeight(+ht.value);
      $('#dl-result').textContent = unit.value === 'cm' ? (dl * 2.54).toFixed(1) : dl.toFixed(1);
      $('#dl-result').nextElementSibling.textContent = unit.value === 'cm' ? 'cm' : 'inches';
      $('#dl-range').innerHTML = 'Try ' + (dl - 0.5).toFixed(1) + '&Prime; to ' + (dl + 0.5).toFixed(1) + '&Prime; at full draw and confirm by shooting.' + (mode === 'height' ? ' (Height-based: measure wingspan for a better estimate.)' : '');
      var pull = Math.max(40, Math.min(150, 40 + (dl - 20) * 8));
      $('#dl-string').setAttribute('d', 'M230 20 L' + (230 - pull) + ' 70 L230 120');
      $('#dl-arrow').setAttribute('x1', 230 - pull);
      $('#dl-label').setAttribute('x', 230 - pull / 2 + 15);
      $('#dl-label').textContent = dl.toFixed(1) + '"';
      var fits = BOWS.filter(function (b) { return dl >= b.dl[0] && dl <= b.dl[1]; });
      $('#dl-bows').innerHTML = fits.length ? fits.map(function (b) {
        return '<a class="match" href="' + b.url + '"><span><b>' + esc(b.name) + '</b><small>Draw range ' + b.dl[0] + '&Prime;–' + b.dl[1] + '&Prime;</small></span><span class="pct"><i class="fa-solid fa-circle-check"></i></span></a>';
      }).join('') : '<p>None of the bows we&rsquo;ve reviewed adjust to ' + dl + '&Prime;. Ask a pro shop about youth or long-draw models.</p>';
      store('bo_dl', dl);
    }
    $$('.seg button', dlTool).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.seg button', dlTool).forEach(function (x) { x.classList.remove('on'); x.setAttribute('aria-selected', 'false'); });
        b.classList.add('on'); b.setAttribute('aria-selected', 'true'); mode = b.dataset.mode;
        $('#dl-ws-field').hidden = mode !== 'wingspan'; $('#dl-h-field').hidden = mode !== 'height'; calc();
      });
    });
    [ws, ht, unit, rel].forEach(function (el) { el.addEventListener('input', calc); });
    calc();
  }

  /* ---------- Arrow speed ---------- */
  var asTool = $('[data-tool="arrow-speed"]');
  if (asTool) {
    var ids = ['ibo', 'dl', 'dw', 'aw', 'sw'], el = {};
    ids.forEach(function (i) { el[i] = $('#as-' + i); });
    var saved = store('bo_dl'); if (saved) { el.dl.value = saved; fill(el.dl); }
    $('#as-preset').addEventListener('change', function () { if (this.value) { el.ibo.value = this.value; fill(el.ibo); calc(); } });
    function calc() {
      var ibo = +el.ibo.value, dl = +el.dl.value, dw = +el.dw.value, aw = +el.aw.value, sw = +el.sw.value;
      var lDl = (30 - dl) * 10, lDw = (70 - dw) * 2, lAw = Math.max(0, aw - 350) / 3, lSw = sw / 3;
      var v = Math.max(120, ibo - lDl - lDw - lAw - lSw);
      $('#as-ibo-out').textContent = ibo + ' fps'; $('#as-dl-out').textContent = dl + ' in';
      $('#as-dw-out').textContent = dw + ' lb'; $('#as-aw-out').textContent = aw + ' gr'; $('#as-sw-out').textContent = sw + ' gr';
      $('#as-result').textContent = Math.round(v);
      $('#as-loss').textContent = Math.round(ibo - v);
      $('#as-ke').textContent = (aw * v * v / 450240).toFixed(1);
      $('#as-mo').textContent = (aw * v / 225218).toFixed(2);
      $('#as-t20').textContent = (60 / v).toFixed(2);
      $('#as-t40').textContent = (120 / v).toFixed(2);
      var rows = [['Draw length', lDl], ['Draw weight', lDw], ['Arrow weight', lAw], ['String accessories', lSw]];
      $('#as-breakdown').innerHTML = rows.map(function (r) {
        var x = Math.round(r[1]);
        return '<li class="' + (x > 0 ? 'no' : 'ok') + '" style="opacity:1"><i class="fa-solid ' + (x > 0 ? 'fa-arrow-trend-down' : 'fa-circle-check') + '"></i> ' + r[0] + ': ' + (x > 0 ? '−' + x : (x < 0 ? '+' + (-x) : '0')) + ' fps</li>';
      }).join('');
    }
    ids.forEach(function (i) { el[i].addEventListener('input', calc); });
    calc();
  }

  /* ---------- Kinetic energy ---------- */
  var keTool = $('[data-tool="ke"]');
  if (keTool) {
    var sp = $('#ke-speed'), wt = $('#ke-weight'), game = $('#ke-game');
    var need = { small: [0, 0], medium: [25, 0.3], large: [42, 0.45], xl: [65, 0.6] };
    var labels = { small: 'small game', medium: 'medium game', large: 'large game', xl: 'the toughest game' };
    function calc() {
      var v = +sp.value, w = +wt.value, ke = w * v * v / 450240, mo = w * v / 225218;
      $('#ke-speed-out').textContent = v + ' fps'; $('#ke-weight-out').textContent = w + ' gr';
      $('#ke-result').textContent = ke.toFixed(1); $('#ke-mo').textContent = mo.toFixed(2);
      $('#ke-needle').style.left = 'calc(' + Math.min(100, ke) + '% - 2px)';
      var n = need[game.value], ok = ke >= n[0] && mo >= n[1];
      $('#ke-verdict').textContent = ok ? 'Ready' : 'Under';
      $('#ke-verdict-l').textContent = (ok ? 'Meets guideline for ' : 'Below guideline for ') + labels[game.value];
      $$('#ke-list li').forEach(function (li) {
        var pass = ke >= +li.dataset.min && mo >= +li.dataset.mo;
        li.className = pass ? 'ok' : 'no';
        li.querySelector('i').className = 'fa-solid ' + (pass ? 'fa-circle-check' : 'fa-circle-xmark');
      });
    }
    [sp, wt, game].forEach(function (x) { x.addEventListener('input', calc); });
    calc();
  }

  /* ---------- Bow finder quiz ---------- */
  var bfTool = $('[data-tool="bow-finder"]');
  if (bfTool) {
    var bows = JSON.parse($('#bf-data').textContent);
    var Q = [
      { q: 'How much archery experience do you have?', o: [['fa-seedling', 'Brand new or returning after years', 'beginner'], ['fa-person-hiking', 'A few seasons under my belt', 'mid'], ['fa-crosshairs', 'Experienced, I tune my own bows', 'experienced']] },
      { q: 'What is your draw length?', o: [['fa-ruler', 'Under 25"', 24], ['fa-ruler', '25" to 27"', 26], ['fa-ruler', '27" to 29"', 28], ['fa-ruler', '29" or longer', 29.5], ['fa-circle-question', 'Not sure yet', 0]] },
      { q: 'Where will you hunt most?', o: [['fa-tree', 'Treestand', 'stand'], ['fa-tent', 'Ground blind', 'blind'], ['fa-mountain', 'Spot-and-stalk / open country', 'spot'], ['fa-bullseye', 'Mostly target practice', 'target']] },
      { q: 'What fits your budget?', o: [['fa-tag', 'Best value, complete package', 'value'], ['fa-scale-balanced', 'Mid-range', 'mid'], ['fa-gem', 'Premium flagship', 'premium'], ['fa-recycle', 'Happy to buy used', 'used']] },
      { q: 'What matters most to you?', o: [['fa-gauge-high', 'Speed and flat trajectory', 'speed'], ['fa-hand-holding-heart', 'Forgiveness and steady aim', 'forgiving'], ['fa-volume-xmark', 'Quiet, dead-in-hand shot', 'quiet'], ['fa-feather', 'Light and easy to carry', 'light']] },
      { q: 'How would you describe your build?', o: [['fa-child-reaching', 'Smaller frame or shorter draw', 'smaller'], ['fa-person', 'Average', 'avg'], ['fa-person-arrow-up-from-line', 'Tall or long arms', 'tall']] }
    ];
    var step = 0, ans = [];
    function render() {
      $('#bf-bar').style.width = (step / Q.length * 100) + '%';
      $('#bf-n').textContent = Math.min(step + 1, Q.length);
      $('#bf-back').hidden = step === 0;
      if (step >= Q.length) { $('#bf-q').innerHTML = '<div class="quiz-q"><h2>All done!</h2><p>Your matches are ranked on the right. Tap a bow to read the full Better Outdoors review.</p></div>'; results(); return; }
      var q = Q[step];
      $('#bf-q').innerHTML = '<div class="quiz-q"><h2>' + q.q + '</h2><div class="opts">' + q.o.map(function (o, i) {
        return '<button type="button" data-i="' + i + '"><i class="fa-solid ' + o[0] + '" aria-hidden="true"></i> ' + o[1] + '</button>';
      }).join('') + '</div></div>';
      $$('#bf-q .opts button').forEach(function (b) { b.addEventListener('click', function () { ans[step] = q.o[+b.dataset.i][2]; step++; render(); }); });
    }
    function results() {
      var dl = ans[1];
      var scored = bows.map(function (b) {
        var s = 50, t = b.tags;
        if (dl && (dl < b.dl[0] || dl > b.dl[1])) return { b: b, s: -1 };
        ans.forEach(function (a, i) { if (i !== 1 && t.indexOf(a) > -1) s += 12; });
        if (ans[0] === 'beginner' && t.indexOf('package') > -1) s += 8;
        if (ans[2] === 'blind' && t.indexOf('compact') > -1) s += 8;
        if (ans[2] === 'spot' && t.indexOf('stable') > -1) s += 6;
        if (ans[5] === 'smaller' && t.indexOf('short') > -1) s += 15;
        if (ans[5] === 'tall' && b.dl[1] >= 30) s += 6;
        if (ans[3] === 'value' && t.indexOf('premium') > -1) s -= 12;
        return { b: b, s: Math.min(98, s) };
      }).filter(function (x) { return x.s >= 0; }).sort(function (a, b) { return b.s - a.s; });
      $('#bf-intro').textContent = scored.length ? 'Based on your answers, these bows fit you best:' : 'None of our reviewed bows reach that draw length. A pro shop can suggest youth or long-draw models.';
      $('#bf-results').innerHTML = scored.slice(0, 3).map(function (x) {
        return '<a class="match" href="/' + x.b.slug + '/"><img src="' + x.b.img + '" alt="" loading="lazy"><span><b>' + esc(x.b.name) + '</b><small>' + esc(x.b.note) + '</small></span><span class="pct">' + x.s + '%</span></a>';
      }).join('');
      $('#bf-restart').hidden = false;
    }
    $('#bf-back').addEventListener('click', function () { if (step > 0) { step--; render(); } });
    $('#bf-restart').addEventListener('click', function () { step = 0; ans = []; $('#bf-results').innerHTML = ''; this.hidden = true; $('#bf-intro').textContent = 'Answer the questions and we will rank the bows for you.'; render(); });
    render();
  }

  /* ---------- Checklist ---------- */
  var clTool = $('[data-tool="checklist"]');
  if (clTool) {
    var boxes = $$('input[type=checkbox]', clTool), state = store('bo_checklist') || {};
    function sync() {
      var done = boxes.filter(function (b) { return b.checked; }).length;
      $('#cl-count').textContent = done + ' / ' + boxes.length + ' packed';
      $('#cl-bar').style.width = (done / boxes.length * 100) + '%';
    }
    boxes.forEach(function (b) {
      b.checked = !!state[b.dataset.id];
      b.addEventListener('change', function () { state[b.dataset.id] = b.checked; store('bo_checklist', state); sync(); });
    });
    $('#cl-print').addEventListener('click', function () { window.print(); });
    $('#cl-reset').addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); state = {}; store('bo_checklist', state); sync(); });
    sync();
  }
})();
