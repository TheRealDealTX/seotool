/* Monetization Readiness Quiz */
(function () {
  'use strict';
  var box = document.getElementById('quiz');
  if (!box) return;

  // Each option: [label, readiness 0-10, {stream: points}]
  var Q = [
    ['How many followers do you have on your main platform?', [
      ['Under 1,000', 1, { ugc: 3, aff: 2 }], ['1,000 - 10,000', 4, { aff: 3, ugc: 2, brand: 1 }],
      ['10,000 - 100,000', 7, { brand: 3, aff: 2, prod: 1 }], ['100,000 or more', 10, { brand: 3, ads: 2, prod: 2, mem: 1 }]]],
    ['Where is your audience mostly?', [
      ['Instagram', 6, { brand: 2, aff: 1 }], ['TikTok', 6, { ugc: 2, brand: 1, aff: 1 }],
      ['YouTube', 7, { ads: 3, aff: 1, mem: 1 }], ['Pinterest or a blog', 6, { aff: 3, ads: 1 }], ['Facebook', 5, { ads: 1, mem: 2, brand: 1 }]]],
    ['What is your average engagement rate?', [
      ['I do not know yet', 2, { ugc: 1 }], ['Under 1%', 3, { ads: 1 }], ['1% - 3%', 6, { brand: 1, aff: 1 }], ['Over 3%', 9, { brand: 2, mem: 1 }]]],
    ['How often do you post?', [
      ['A few times a month', 2, { prod: 1, ugc: 1 }], ['About once a week', 5, { aff: 1 }], ['Several times a week', 8, { brand: 1, ads: 1 }], ['Daily', 10, { ads: 2, brand: 1 }]]],
    ['What do followers ask you most?', [
      ['"Where did you get that?"', 6, { aff: 3 }], ['"How do you do that?"', 7, { prod: 3, mem: 1 }],
      ['"When is the next video?"', 7, { ads: 2, mem: 2 }], ['They mostly like and scroll', 3, { ugc: 2 }]]],
    ['How do you feel about making content for brands?', [
      ['Love it, I enjoy filming for others', 7, { ugc: 3, brand: 1 }], ['Only on my own channel', 5, { prod: 1, ads: 1 }],
      ['Happy to, if the brand fits', 7, { brand: 2 }], ['I would rather sell my own thing', 6, { prod: 2, aff: 1 }]]],
    ['Have you earned money from your content yet?', [
      ['Not yet', 2, { aff: 1, ugc: 1 }], ['Free products only', 5, { brand: 1 }], ['One or two paid deals', 8, { brand: 2 }], ['Yes, regularly', 10, { brand: 2, prod: 1 }]]],
    ['Do you have a media kit or rate card?', [
      ['No', 2, {}], ['I am working on one', 5, {}], ['Yes, and it is up to date', 9, { brand: 2 }]]],
    ['Do you own a website or email list?', [
      ['Neither', 2, {}], ['Just a link-in-bio page', 4, { aff: 1 }], ['A website', 7, { prod: 2, aff: 1 }], ['An email list (with or without a site)', 10, { prod: 2, mem: 2 }]]],
    ['How much time can you give the business side each week?', [
      ['Under 2 hours', 2, { aff: 2, ads: 1 }], ['2 - 5 hours', 5, { aff: 1, brand: 1 }], ['5 - 10 hours', 8, { brand: 2, prod: 1 }], ['10+ hours', 10, { prod: 2, mem: 2, brand: 1 }]]]
  ];

  var STREAMS = {
    brand: { name: 'Brand deals', steps: ['Calculate your rate per post', 'Build a one-page media kit', 'Pitch 5 brands your audience already buys'],
      link: ['/monetization/#brand-outreach', 'Brand outreach guide'], tool: ['/tools/influencer-email-generator/', 'Write your pitch'] },
    aff: { name: 'Affiliate marketing', steps: ['Join programs for products you already use', 'Add links to your highest-intent content', 'Disclose clearly and track clicks'],
      link: ['/affiliate-marketing-for-influencers/', 'Affiliate marketing playbook'], tool: ['/tools/income-stream-simulator/', 'Model affiliate income'] },
    ads: { name: 'Ad revenue', steps: ['Check your platform\'s creator program requirements', 'Make longer, evergreen videos', 'Add direct ad placements to your content'],
      link: ['/monetization/#ad-placements', 'Ad placements guide'], tool: ['/tools/income-stream-simulator/', 'Estimate ad revenue'] },
    prod: { name: 'Digital products', steps: ['List the questions you answer most', 'Package the answer as a guide, template or course', 'Sell it from a page you own'],
      link: ['/monetization/#white-labeling', 'Product launch guide'], tool: ['/website-design/', 'Get a money site'] },
    mem: { name: 'Memberships', steps: ['Pick one exclusive perk fans would pay for', 'Launch at a low monthly price', 'Deliver consistently for 90 days'],
      link: ['/monetization/', 'Influencer monetization guide'], tool: ['/tools/income-stream-simulator/', 'Model membership income'] },
    ugc: { name: 'UGC creation', steps: ['Film 3 sample product videos', 'Build a simple UGC portfolio', 'Pitch brands that run lots of video ads'],
      link: ['/monetization/#short-content', 'Short content guide'], tool: ['/tools/influencer-email-generator/', 'Write a brand pitch'] }
  };

  var answers = [], cur = 0, busy = false;

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function showQuestion(dir) {
    busy = false;
    var q = Q[cur];
    box.innerHTML = '';
    var prog = el('div', 'quiz-progress', '<span>Question ' + (cur + 1) + ' of ' + Q.length + '</span><span>' + Math.round(cur / Q.length * 100) + '% done</span>');
    var meter = el('div', 'meter', '<i style="width:' + (cur / Q.length * 100) + '%"></i>');
    var wrap = el('div', 'quiz-q');
    var h = el('h2'); h.id = 'qh'; h.textContent = q[0]; h.tabIndex = -1;
    var opts = el('div', 'quiz-opts'); opts.setAttribute('role', 'group'); opts.setAttribute('aria-labelledby', 'qh');
    q[1].forEach(function (o, i) {
      var b = el('button', answers[cur] === i ? 'picked' : '', '<span class="k">' + String.fromCharCode(65 + i) + '</span><span>' + esc(o[0]) + '</span>');
      b.type = 'button';
      b.addEventListener('click', function () { choose(i, b); });
      opts.appendChild(b);
    });
    var nav = el('div', 'quiz-nav');
    var back = el('button', 'btn btn-ghost btn-sm', 'Back'); back.type = 'button'; back.disabled = cur === 0;
    back.addEventListener('click', function () { cur--; transition(); });
    nav.appendChild(back);
    nav.appendChild(el('span', 'small', 'Tip: press A-' + String.fromCharCode(64 + q[1].length) + ' on your keyboard'));
    wrap.appendChild(h); wrap.appendChild(opts); wrap.appendChild(nav);
    box.appendChild(prog); box.appendChild(meter); box.appendChild(wrap);
    requestAnimationFrame(function () { meter.firstChild.style.width = ((cur + (dir ? 0 : 0)) / Q.length * 100) + '%'; });
    if (dir) h.focus({ preventScroll: true });
  }

  function transition() {
    var q = box.querySelector('.quiz-q');
    if (!q || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { cur < Q.length ? showQuestion(true) : showResult(); return; }
    q.classList.add('out');
    setTimeout(function () { cur < Q.length ? showQuestion(true) : showResult(); }, 260);
  }

  function choose(i, btn) {
    if (busy) return;
    busy = true;
    answers[cur] = i;
    box.querySelectorAll('.quiz-opts button').forEach(function (b) { b.classList.remove('picked'); });
    btn.classList.add('picked');
    cur++;
    setTimeout(transition, 180);
  }

  function showResult() {
    busy = false;
    var ready = 0, max = 0, pts = { brand: 0, aff: 0, ads: 0, prod: 0, mem: 0, ugc: 0 };
    Q.forEach(function (q, qi) {
      var o = q[1][answers[qi]];
      max += Math.max.apply(null, q[1].map(function (x) { return x[1]; }));
      ready += o[1];
      Object.keys(o[2]).forEach(function (k) { pts[k] += o[2][k]; });
    });
    var score = Math.round(ready / max * 100);
    var ranked = Object.keys(pts).sort(function (a, b) { return pts[b] - pts[a]; });
    var top = Math.max(1, pts[ranked[0]]);
    var stage = score < 40 ? ['Foundation stage', 'Build consistency and start with streams that need no big audience.'] :
      score < 70 ? ['Ready to earn', 'You have enough to start pitching and selling. Package your numbers and go.'] :
      ['Ready to scale', 'You are ready to stack streams and negotiate bigger, longer partnerships.'];
    var C = 2 * Math.PI * 80;

    box.innerHTML = '';
    var head = el('div', 'result-head quiz-q');
    head.innerHTML =
      '<svg class="ring" viewBox="0 0 200 200" role="img" aria-label="Readiness score ' + score + ' out of 100">' +
      '<defs><linearGradient id="ringGrad" x1="0" x2="1" y1="0" y2="1"><stop offset="0" stop-color="#29b6f6"/><stop offset=".5" stop-color="#8b5cf6"/><stop offset="1" stop-color="#ff3d9a"/></linearGradient></defs>' +
      '<circle class="bg" cx="100" cy="100" r="80"/><circle class="fg" id="ring-fg" cx="100" cy="100" r="80" stroke-dasharray="' + C + '" stroke-dashoffset="' + C + '"/>' +
      '<text x="100" y="108" text-anchor="middle" id="ring-num">0</text><text class="sub" x="100" y="132" text-anchor="middle">out of 100</text></svg>' +
      '<span class="tier-badge pop">' + stage[0] + '</span><h2 style="margin-top:14px">Your monetization readiness score</h2><p class="small">' + stage[1] + '</p>';
    box.appendChild(head);

    var grid = el('div', 'rec-grid');
    ranked.slice(0, 2).forEach(function (k, i) {
      var s = STREAMS[k], r = el('div', 'rec');
      r.innerHTML = '<span class="chip">' + (i === 0 ? 'Best fit' : 'Runner-up') + '</span><h3>' + s.name + '</h3><ol>' +
        s.steps.map(function (x) { return '<li>' + esc(x) + '</li>'; }).join('') + '</ol>' +
        '<a href="' + s.link[0] + '">' + s.link[1] + ' &rarr;</a><br><a href="' + s.tool[0] + '">' + s.tool[1] + ' &rarr;</a>';
      grid.appendChild(r);
    });
    box.appendChild(grid);

    var bars = el('div', 'stream-bars');
    ranked.forEach(function (k) {
      var row = el('div', '', '<span>' + STREAMS[k].name + '</span><div class="meter"><i></i></div><b>' + pts[k] + '</b>');
      bars.appendChild(row);
      setTimeout(function () { row.querySelector('i').style.width = (pts[k] / top * 100) + '%'; }, 200);
    });
    var bh = el('h3', '', 'Fit by income stream'); bh.style.marginTop = '8px';
    box.appendChild(bh); box.appendChild(bars);

    var nav = el('div', 'btn-row');
    nav.style.marginTop = '24px'; nav.style.justifyContent = 'center';
    var again = el('button', 'btn btn-ghost', 'Retake the quiz'); again.type = 'button';
    again.addEventListener('click', function () { answers = []; cur = 0; showQuestion(true); });
    nav.appendChild(again);
    nav.appendChild(el('a', 'btn btn-glow', 'Get a personal plan &rarr;')).href = '/get-started/';
    box.appendChild(nav);

    requestAnimationFrame(function () {
      setTimeout(function () { document.getElementById('ring-fg').style.strokeDashoffset = C * (1 - score / 100); }, 60);
    });
    var numEl = document.getElementById('ring-num'), t0 = null;
    (function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1400, 1);
      numEl.textContent = Math.round(score * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
    if (window.MI) MI.confetti(180);
    box.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  document.addEventListener('keydown', function (e) {
    if (cur >= Q.length || e.altKey || e.ctrlKey || e.metaKey) return;
    var t = e.target.tagName;
    if (t === 'INPUT' || t === 'TEXTAREA' || t === 'SELECT') return;
    var i = e.key.toUpperCase().charCodeAt(0) - 65;
    if (e.key.length === 1 && i >= 0 && i < Q[cur][1].length) {
      var r = box.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var b = box.querySelectorAll('.quiz-opts button')[i];
      if (b) choose(i, b);
    }
  });

  showQuestion(false);
})();
