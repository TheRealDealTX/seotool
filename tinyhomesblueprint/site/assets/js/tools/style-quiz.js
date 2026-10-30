// Tiny Homes Blueprint - tiny house style quiz.
(function () {
  var root = document.getElementById('qz');
  if (!root) return;
  var $ = function (id) { return document.getElementById(id); };
  var STYLES = {};
  try { STYLES = JSON.parse($('qz-data').textContent); } catch (e) { return; }
  var keys = Object.keys(STYLES);
  var qs = Array.prototype.slice.call(root.querySelectorAll('.quiz-q'));
  var total = qs.length;
  var answers = []; // option index per question
  var cur = 0;

  function scores() {
    var pts = {}, possible = {}, why = {};
    keys.forEach(function (k) { pts[k] = 0; possible[k] = 0; why[k] = []; });
    answers.forEach(function (oi, qi) {
      if (oi == null) return;
      var btns = qs[qi].querySelectorAll('[data-s]');
      var best = {};
      btns.forEach(function (b) { var s = JSON.parse(b.dataset.s); Object.keys(s).forEach(function (k) { best[k] = Math.max(best[k] || 0, s[k]); }); });
      Object.keys(best).forEach(function (k) { possible[k] += best[k]; });
      var b = btns[oi], s = JSON.parse(b.dataset.s);
      Object.keys(s).forEach(function (k) { pts[k] += s[k]; if (s[k] >= 2) why[k].push(b.dataset.label); });
    });
    return keys.map(function (k) {
      // Match = points earned / points available from the questions answered so far.
      var pct = possible[k] ? pts[k] / possible[k] : 0;
      return { key: k, pts: pts[k], pct: pct, why: why[k] };
    }).sort(function (a, b) { return b.pct - a.pct || b.pts - a.pts; });
  }

  function renderLive() {
    var answered = answers.filter(function (a) { return a != null; }).length;
    var list = scores();
    if (!answered) {
      $('qz-lead').textContent = 'Answer to begin';
      $('qz-lead-sub').textContent = 'All nine styles start even. Your top matches update after every answer.';
      $('qz-live').innerHTML = keys.map(function (k) {
        return '<li><div><span>' + STYLES[k].name + '</span><b>-</b></div><div class="bar"><i style="width:0%"></i></div></li>';
      }).join('');
      return;
    }
    $('qz-lead').textContent = STYLES[list[0].key].name;
    $('qz-lead-sub').textContent = 'Leading after ' + answered + ' of ' + total + ' answers';
    $('qz-live').innerHTML = list.slice(0, 6).map(function (s, i) {
      var p = Math.round(s.pct * 100);
      return '<li' + (i === 0 ? ' class="lead"' : '') + '><div><span>' + STYLES[s.key].name + '</span><b>' + p + '%</b></div><div class="bar"><i style="width:' + p + '%"></i></div></li>';
    }).join('');
  }

  function show(i, focus) {
    cur = i;
    qs.forEach(function (q, n) { q.classList.toggle('active', n === i); });
    var answered = answers.filter(function (a) { return a != null; }).length;
    $('qz-count').textContent = 'Question ' + (i + 1) + ' of ' + total;
    $('qz-pct').textContent = Math.round(answered / total * 100) + '% done';
    $('qz-bar').setAttribute('aria-valuenow', answered);
    $('qz-bar').firstElementChild.style.width = (answered / total * 100) + '%';
    $('qz-back').disabled = i === 0;
    qs[i].querySelectorAll('[data-o]').forEach(function (b) {
      var chosen = answers[i] === +b.dataset.o;
      b.classList.toggle('chosen', chosen);
      b.setAttribute('aria-pressed', chosen ? 'true' : 'false');
    });
    if (focus) qs[i].querySelector('h2').focus({ preventScroll: true });
  }

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function finish() {
    var list = scores(), top = list[0], st = STYLES[top.key];
    var why = top.why.slice(0, 4).map(function (w) { return '<li>You chose &ldquo;' + esc(w) + '&rdquo;</li>'; }).join('');
    var plans = st.plans.length
      ? '<p class="plan-no" style="margin-top:6px">Plans in this style</p><div class="quiz-plans">' + st.plans.map(function (p) { return '<a class="btn btn-sm btn-wood" href="' + p.url + '">' + esc(p.name) + '</a>'; }).join('') + '</div>'
      : '<p class="muted" style="font-size:.92rem">Want this style drawn for your site? <a href="/contact/">Ask Tiny Homes Blueprint about a custom plan</a> or <a href="/tiny-house-plans/">browse all plans</a>.</p>';
    var runners = list.slice(1, 3).map(function (s, i) {
      var r = STYLES[s.key];
      return '<div class="runner"><p class="plan-no">Runner-up ' + (i + 1) + ' &middot; ' + Math.round(s.pct * 100) + '% match</p><strong>' + r.name + '</strong><p>' + esc(r.blurb) + '</p><a href="' + r.url + '">Explore ' + r.name.toLowerCase() + ' &rarr;</a></div>';
    }).join('');
    $('qz-result').innerHTML =
      '<p class="eyebrow" style="margin:0">Your tiny house style</p>' +
      '<div class="match-card"><span class="link-ico">' + st.icon + '</span><div>' +
      '<span class="match-pct">' + Math.round(top.pct * 100) + '% match</span>' +
      '<h3 id="qz-res-h">' + st.name + '</h3><p>' + esc(st.blurb) + '</p>' +
      (why ? '<p style="margin:0;font-weight:600">Why it fits</p><ul class="why-list">' + why + '</ul>' : '') +
      '<a class="btn btn-sm" href="' + st.url + '">See ' + st.name.toLowerCase() + '</a>' + plans + '</div></div>' +
      '<h3 style="font-size:1.15rem">Also worth a look</h3><div class="runner-ups">' + runners + '</div>' +
      '<div class="quiz-nav"><button type="button" class="btn btn-outline btn-sm" id="qz-review">&larr; Change answers</button><button type="button" class="btn btn-sm" id="qz-restart">Retake the quiz</button></div>';
    $('qz-quiz').hidden = true;
    $('qz-result').hidden = false;
    $('qz-lead-sub').textContent = 'Final result after all ' + total + ' answers';
    $('qz-label').textContent = 'Your top matches';
    $('qz-result').focus({ preventScroll: true });
    var top0 = root.getBoundingClientRect().top;
    if (top0 < 0) root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function restart() {
    answers = [];
    $('qz-result').hidden = true; $('qz-quiz').hidden = false;
    $('qz-label').textContent = 'Your matches so far';
    renderLive(); show(0, true);
  }

  root.addEventListener('click', function (e) {
    var b = e.target.closest('[data-o]');
    if (b) {
      var qi = +b.closest('.quiz-q').dataset.q;
      answers[qi] = +b.dataset.o;
      renderLive();
      // Next unanswered question, or finish.
      var next = -1;
      for (var i = qi + 1; i < total; i++) if (answers[i] == null) { next = i; break; }
      if (next < 0) for (var j = 0; j < total; j++) if (answers[j] == null) { next = j; break; }
      if (next < 0) { show(qi); finish(); } else show(next, true);
      return;
    }
    if (e.target.closest('#qz-back')) { if (cur > 0) show(cur - 1, true); return; }
    if (e.target.closest('#qz-restart') || e.target.closest('#qz-restart-top')) { restart(); return; }
    if (e.target.closest('#qz-review')) { $('qz-result').hidden = true; $('qz-quiz').hidden = false; show(total - 1, true); }
  });

  // Letter keys A-E pick an option on the visible question.
  document.addEventListener('keydown', function (e) {
    if ($('qz-quiz').hidden || e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = e.target && e.target.tagName;
    if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
    if (!root.contains(e.target) && e.target !== document.body) return;
    var idx = 'abcde'.indexOf((e.key || '').toLowerCase());
    if (idx < 0) return;
    var b = qs[cur].querySelectorAll('[data-o]')[idx];
    if (b) { e.preventDefault(); b.click(); }
  });

  renderLive();
  show(0);
})();
