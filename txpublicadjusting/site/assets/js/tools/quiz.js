/* "Do I need a public adjuster?" self-assessment */
(function () {
  'use strict';
  var root = document.querySelector('[data-quiz]');
  if (!root) return;
  var Q = [
    ['What kind of property and damage?', [['Minor damage to one area of a home (a fence, one room, a few shingles)', 0], ['A full roof or significant exterior damage', 2], ['Major interior damage: fire, smoke or water through several rooms', 3], ['Commercial, multifamily, church or multiple buildings', 3]]],
    ['Roughly how large is the loss?', [['Under $10,000', 0], ['$10,000 to $30,000', 1], ['$30,000 to $100,000', 2], ['Over $100,000, or I really don\'t know yet', 3]]],
    ['Where is the claim right now?', [['I haven\'t filed yet', 1], ['Filed, waiting on the inspection or estimate', 1], ['I received an estimate or payment', 1], ['Denied, partly denied, or stalled for weeks', 3]]],
    ['How does the insurer\'s number compare with real repair bids?', [['Close: within about 10%', 0], ['No estimate or bids yet', 1], ['Noticeably lower: 10% to 30% short', 2], ['Way off, or major areas left out entirely', 3]]],
    ['Does the claim involve any of these?', [['None of these', 0], ['Personal property (contents) inventory', 2], ['Business income, loss of rents or extra expense', 3], ['Disputed cause (wear and tear, prior damage, cosmetic, flood vs. wind)', 3]]],
    ['How much time can you give the claim?', [['Plenty, and I\'m comfortable negotiating', 0], ['Some, but it\'s stressful', 1], ['Very little: work, family or I\'ve been displaced', 2], ['I\'m out of state, deployed or managing it remotely', 2]]],
    ['Have deadlines or paperwork become a problem?', [['No, everything is on track', 0], ['The insurer keeps asking for more documents', 1], ['I\'m not sure what my policy deadlines are', 1], ['A deadline is close, or the insurer has missed its own', 2]]],
  ];
  var answers = [], i = 0;
  var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  function show() {
    var qs = root.querySelector('[data-out="qs"]'), res = root.querySelector('[data-out="result"]');
    root.querySelector('[data-act="back"]').hidden = i === 0 || i >= Q.length;
    root.querySelector('[data-act="restart"]').hidden = i < Q.length;
    root.querySelector('[data-out="bar"]').style.width = (Math.min(i, Q.length) / Q.length * 100) + '%';
    if (i < Q.length) {
      root.querySelector('[data-out="step"]').textContent = 'Question ' + (i + 1) + ' of ' + Q.length;
      res.classList.remove('is-on');
      qs.innerHTML = '<div class="quiz-q is-on"><h3>' + esc(Q[i][0]) + '</h3><div class="quiz-opts">' + Q[i][1].map(function (o, k) { return '<button type="button" data-k="' + k + '">' + esc(o[0]) + '</button>'; }).join('') + '</div></div>';
      return;
    }
    root.querySelector('[data-out="step"]').textContent = 'Your result';
    qs.innerHTML = '';
    var score = answers.reduce(function (s, a, n) { return s + Q[n][1][a][1]; }, 0);
    var max = Q.reduce(function (s, q) { return s + Math.max.apply(null, q[1].map(function (o) { return o[1]; })); }, 0);
    var v;
    if (score >= 11) v = ['high', 'A public adjuster is likely worth it', 'Your answers point to a larger or more complex claim, where documentation, scope and negotiation usually decide the outcome. A free review costs nothing and will show how much is at stake.'];
    else if (score >= 6) v = ['mid', 'Worth a second opinion', 'You could handle this yourself, but there are signs the claim may be short or stuck. Have a licensed adjuster look over the estimate before you accept a final number.'];
    else v = ['low', 'You can probably handle this one yourself', 'Your claim looks small and on track. Use our documentation checklist and deadline calculator, and keep everything in writing. If the insurer\'s number comes back low, check again.'];
    res.innerHTML = '<div class="verdict verdict--' + v[0] + '"><p class="eyebrow" style="margin-bottom:.4rem">Score ' + score + ' / ' + max + '</p><h3>' + v[1] + '</h3><p style="margin:0">' + v[2] + '</p></div>' +
      '<div class="tbtns">' + (v[0] === 'low'
        ? '<a class="btn btn--primary" href="/tools/claim-documentation-checklist/">Open the documentation checklist</a><a class="btn btn--ghost" href="/tools/texas-claim-deadline-calculator/">Check your deadlines</a>'
        : '<a class="btn btn--primary" href="/contact-us/">Request a free claim review</a><a class="btn btn--ghost" href="tel:+18325035866">Call (832) 503-5866</a>') + '</div>';
    res.classList.add('is-on');
  }
  root.addEventListener('click', function (e) {
    var b = e.target.closest('[data-k]');
    if (b) { answers[i] = +b.getAttribute('data-k'); i++; show(); return; }
    var a = e.target.closest('[data-act]');
    if (!a) return;
    if (a.getAttribute('data-act') === 'back' && i > 0) { i--; show(); }
    if (a.getAttribute('data-act') === 'restart') { answers = []; i = 0; show(); }
  });
  show();
})();
