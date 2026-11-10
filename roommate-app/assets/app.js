/* Rise Roommates — progressive enhancement. Everything works without JS; this makes it faster. */
(function () {
  'use strict';
  var CSRF = (document.querySelector('meta[name=csrf]') || {}).content || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function api(url, opts) {
    opts = opts || {};
    var headers = { 'X-Requested-With': 'fetch', 'Accept': 'application/json', 'X-CSRF-Token': CSRF };
    return fetch(url, { method: opts.method || 'GET', body: opts.body, headers: headers, credentials: 'same-origin' })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) throw j; return j; }); });
  }
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'toast'; t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 2600);
  }
  function esc(s) { var d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
  function linkify(s) { return esc(s).replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener nofollow">$1</a>'); }

  // Flash dismiss + auto-hide
  $$('.flash').forEach(function (f) {
    var x = $('.flash-x', f);
    if (x) x.addEventListener('click', function () { f.remove(); });
    if (f.classList.contains('flash-success')) setTimeout(function () { f.style.transition = 'opacity .4s'; f.style.opacity = 0; setTimeout(function () { f.remove(); }, 400); }, 5000);
  });

  // Confirmations on forms or submit buttons
  document.addEventListener('submit', function (e) {
    var f = e.target;
    var btn = e.submitter;
    var msg = (btn && btn.getAttribute('data-confirm')) || f.getAttribute('data-confirm');
    if (msg && !confirm(msg)) e.preventDefault();
  }, true);

  // Close dropdowns on outside click / Escape
  document.addEventListener('click', function (e) {
    $$('details.menu[open]').forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute('open'); });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') $$('details.menu[open]').forEach(function (d) { d.removeAttribute('open'); });
  });

  // Auto-growing textareas
  function grow(t) { t.style.height = 'auto'; t.style.height = Math.min(t.scrollHeight + 2, 240) + 'px'; }
  $$('textarea.autogrow').forEach(function (t) { t.addEventListener('input', function () { grow(t); }); });

  // Range with labels
  $$('.js-range').forEach(function (r) {
    var labels = JSON.parse(r.getAttribute('data-labels') || '[]');
    var out = r.parentNode.querySelector('.range-out');
    r.addEventListener('input', function () { if (out) out.textContent = labels[r.value - 1] || r.value; });
  });

  // Image previews
  $$('.js-img-input').forEach(function (inp) {
    var form = inp.closest('form');
    var prev = $('.composer-preview', form);
    inp.addEventListener('change', function () {
      if (!inp.files[0] || !prev) return;
      $('img', prev).src = URL.createObjectURL(inp.files[0]);
      prev.hidden = false;
    });
    var clear = prev && $('.composer-clear', prev);
    if (clear) clear.addEventListener('click', function () { inp.value = ''; prev.hidden = true; });
  });
  $$('.js-avatar-input').forEach(function (inp) {
    inp.addEventListener('change', function () {
      if (!inp.files[0]) return;
      var wrap = $('.avatar-preview');
      wrap.innerHTML = '<img class="avatar avatar-xl" alt="">';
      $('img', wrap).src = URL.createObjectURL(inp.files[0]);
    });
  });

  // Filter a list of checkboxes
  $$('.js-filter-list').forEach(function (inp) {
    var list = $(inp.getAttribute('data-target'));
    inp.addEventListener('input', function () {
      var q = inp.value.toLowerCase().trim();
      $$('[data-name]', list).forEach(function (el) { el.hidden = q && el.getAttribute('data-name').indexOf(q) === -1; });
    });
  });

  // Property search (profile editor)
  $$('.js-prop-search').forEach(function (inp) {
    var list = $(inp.getAttribute('data-target'));
    var res = inp.parentNode.querySelector('.prop-search-results');
    var timer;
    var add = function (p) {
      var existing = list.querySelector('input[value="' + p.id + '"]');
      if (existing) { existing.checked = true; } else {
        var none = list.querySelector('.js-none'); if (none) none.remove();
        var l = document.createElement('label');
        l.className = 'pick';
        l.innerHTML = '<input type="checkbox" name="properties[]" value="' + p.id + '" checked><span>' + esc(p.name) + (p.city ? '<small>' + esc(p.city) + '</small>' : '') + '</span>';
        list.insertBefore(l, list.firstChild);
      }
      inp.value = ''; res.hidden = true; inp.focus();
    };
    inp.addEventListener('input', function () {
      clearTimeout(timer);
      var q = inp.value.trim();
      if (q.length < 2) { res.hidden = true; return; }
      timer = setTimeout(function () {
        api('/api/properties?q=' + encodeURIComponent(q)).then(function (j) {
          res.innerHTML = '';
          if (!j.results.length) { res.innerHTML = '<li class="muted small" style="padding:8px">No matches. <a href="/properties/new">Add this property</a></li>'; }
          j.results.forEach(function (p) {
            var li = document.createElement('li');
            var b = document.createElement('button'); b.type = 'button';
            b.innerHTML = '<span>' + esc(p.name) + '</span><small>' + esc(p.city) + '</small>';
            b.addEventListener('click', function () { add(p); });
            li.appendChild(b); res.appendChild(li);
          });
          res.hidden = false;
        }).catch(function () {});
      }, 220);
    });
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); var b = res.querySelector('button'); if (b) b.click(); } });
    document.addEventListener('click', function (e) { if (!inp.parentNode.contains(e.target)) res.hidden = true; });
  });

  // Admin: check all
  $$('.js-check-all').forEach(function (c) {
    c.addEventListener('change', function () { $$('input[name="ids[]"]', c.closest('form')).forEach(function (x) { x.checked = c.checked; }); });
  });

  // Property interest toggles on cards
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('.js-toggle-prop');
    if (!f) return;
    e.preventDefault();
    var b = $('button', f);
    api(f.action, { method: 'POST', body: new FormData(f) }).then(function (j) {
      b.classList.toggle('btn-soft', j.on); b.classList.toggle('is-on', j.on); b.classList.toggle('btn-outline', !j.on);
      b.innerHTML = j.on ? '✓ Interested' : '+ I\'m interested';
      var meta = f.closest('.prop-card').querySelector('.prop-meta span:last-child');
      if (meta) meta.lastChild.textContent = j.count + ' interested';
      toast(j.on ? 'Added to your properties' : 'Removed from your properties');
    }).catch(function (j) { toast((j && j.error) || 'Something went wrong'); });
  });

  // Focus comment box
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.js-focus-comment');
    if (b) { var i = document.getElementById('c-' + b.getAttribute('data-post')); if (i) i.focus(); }
  });

  // Report modal
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.js-report');
    if (!b) return;
    var d = b.closest('details'); if (d) d.removeAttribute('open');
    var type = b.getAttribute('data-type'), id = b.getAttribute('data-id');
    var m = document.createElement('div');
    m.className = 'modal';
    m.innerHTML = '<form class="modal-box form"><h3>Report this ' + esc(type) + '</h3>' +
      '<label>What\'s wrong?<select name="preset"><option>Spam or scam</option><option>Fake profile</option><option>Harassment or hate</option><option>Inappropriate content</option><option>Asking for money</option><option>Other</option></select></label>' +
      '<label>Details (optional)<textarea name="details" rows="3" maxlength="400"></textarea></label>' +
      '<div class="form-actions"><button type="button" class="btn btn-ghost js-close">Cancel</button><button class="btn btn-primary" type="submit">Send report</button></div></form>';
    document.body.appendChild(m);
    var close = function () { m.remove(); };
    m.addEventListener('click', function (ev) { if (ev.target === m || ev.target.closest('.js-close')) close(); });
    $('form', m).addEventListener('submit', function (ev) {
      ev.preventDefault();
      var fd = new FormData();
      fd.append('_csrf', CSRF); fd.append('type', type); fd.append('id', id);
      var f = ev.target;
      fd.append('reason', f.preset.value + (f.details.value.trim() ? ': ' + f.details.value.trim() : ''));
      api('/report', { method: 'POST', body: fd }).then(function (j) { close(); toast(j.message || 'Reported'); })
        .catch(function (j) { toast((j && j.error) || 'Could not send report'); });
    });
  });

  // Unread badges
  function setBadge(key, n) {
    $$('[data-count="' + key + '"] .badge').forEach(function (b) { b.textContent = n > 99 ? '99+' : n; b.hidden = !n; });
  }
  function applyCounts(c) { if (!c) return; setBadge('messages', c.messages); setBadge('notifications', c.notifications); }

  if (!document.getElementById('chat-msgs') && document.body.classList.contains('authed')) {
    // Light polling for badges elsewhere
    var tick = function () { if (!document.hidden) api('/api/counts').then(applyCounts).catch(function () {}); };
    setInterval(tick, 30000);
  }
})();

/* ---------- Interactive features ---------- */
(function () {
  'use strict';
  var CSRF = (document.querySelector('meta[name=csrf]') || {}).content || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function post(url, data) {
    var fd = new FormData(); fd.append('_csrf', CSRF);
    Object.keys(data || {}).forEach(function (k) { fd.append(k, data[k]); });
    return fetch(url, { method: 'POST', body: fd, credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch', 'Accept': 'application/json' } })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw j; return j; }); });
  }
  function getJSON(url) {
    return fetch(url, { credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch', 'Accept': 'application/json' } })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw j; return j; }); });
  }
  function toast(msg) { var t = document.createElement('div'); t.className = 'toast'; t.textContent = msg; document.body.appendChild(t); setTimeout(function () { t.remove(); }, 2600); }
  function avatarHTML(a, size) {
    return a.avatar ? '<img class="avatar avatar-' + size + '" src="' + esc(a.avatar) + '" alt="">'
      : '<span class="avatar avatar-' + size + ' avatar-initials" style="--h:' + (a.hue || 200) + '">' + esc(a.initials || '?') + '</span>';
  }

  // ===== Swipe deck =====
  var deck = $('#deck');
  if (deck) {
    var cards = JSON.parse(deck.getAttribute('data-cards') || '[]');
    var history = [];
    var busy = false;
    var build = function (c) {
      var el = document.createElement('article');
      el.className = 'swipe-card';
      el.innerHTML =
        '<div class="sc-photo" style="' + (c.avatar ? "background-image:url('" + esc(c.avatar) + "')" : '--h:' + c.hue) + '">' +
          (c.avatar ? '' : '<span class="sc-initial">' + esc(c.initials) + '</span>') +
          '<span class="sc-score score ' + (c.score >= 75 ? 'great' : c.score >= 55 ? 'good' : 'fair') + '">' + c.score + '% match</span>' +
          '<span class="stamp stamp-like">LIKE</span><span class="stamp stamp-pass">PASS</span>' +
          '<div class="sc-name"><h2>' + esc(c.name) + (c.age ? '<span>, ' + c.age + '</span>' : '') + '</h2>' +
          '<p>' + esc([c.occupation, c.city].filter(Boolean).join(' · ')) + '</p></div>' +
        '</div>' +
        '<div class="sc-body">' +
          (c.type ? '<span class="type-badge">' + esc(c.type) + '</span>' : '') +
          '<div class="chips">' + (c.budget ? '<span class="chip">💲 ' + esc(c.budget) + '</span>' : '') + (c.move_in ? '<span class="chip">📅 ' + esc(c.move_in) + '</span>' : '') +
          '<span class="chip">' + esc(c.looking_for) + '</span>' + c.chips.map(function (x) { return '<span class="chip">' + esc(x) + '</span>'; }).join('') + '</div>' +
          (c.reasons.length ? '<ul class="reasons">' + c.reasons.map(function (r) { return '<li>✓ ' + esc(r) + '</li>'; }).join('') + '</ul>' : '') +
          (c.bio ? '<p class="sc-bio">' + esc(c.bio) + '</p>' : '') +
          (c.props.length ? '<p class="small muted">🏢 ' + esc(c.props.join(' · ')) + '</p>' : '') +
        '</div>';
      el._data = c;
      return el;
    };
    var render = function () {
      $$('.swipe-card', deck).forEach(function (e) { e.remove(); });
      cards.slice(0, 3).reverse().forEach(function (c, i, arr) {
        var el = build(c);
        var depth = arr.length - 1 - i;
        el.style.setProperty('--depth', depth);
        if (depth === 0) { el.classList.add('top'); bindDrag(el); }
        deck.appendChild(el);
      });
      deck.classList.toggle('is-empty', !cards.length);
    };
    var fly = function (liked) {
      if (busy || !cards.length) return;
      var el = $('.swipe-card.top', deck); if (!el) return;
      busy = true;
      var c = cards.shift();
      history.push(c);
      el.style.transition = 'transform .35s ease, opacity .35s';
      el.style.transform = 'translate(' + (liked ? 600 : -600) + 'px, -40px) rotate(' + (liked ? 28 : -28) + 'deg)';
      el.style.opacity = 0;
      setTimeout(function () { busy = false; render(); }, 300);
      post('/api/swipe', { target: c.id, liked: liked ? 1 : 0 }).then(function (j) { if (j.match) showMatch(j.user); }).catch(function (j) { toast((j && j.error) || 'Something went wrong'); });
    };
    var undo = function () {
      var c = history.pop(); if (!c) return toast('Nothing to undo');
      post('/api/swipe', { target: c.id, undo: 1 }); cards.unshift(c); render();
    };
    function bindDrag(el) {
      var sx = 0, sy = 0, dx = 0, dy = 0, dragging = false;
      el.addEventListener('pointerdown', function (e) {
        if (e.button !== 0) return; dragging = true; sx = e.clientX; sy = e.clientY; el.setPointerCapture(e.pointerId); el.style.transition = 'none';
      });
      el.addEventListener('pointermove', function (e) {
        if (!dragging) return; dx = e.clientX - sx; dy = e.clientY - sy;
        el.style.transform = 'translate(' + dx + 'px,' + dy + 'px) rotate(' + dx / 18 + 'deg)';
        el.style.setProperty('--like', Math.max(0, Math.min(1, dx / 120)));
        el.style.setProperty('--pass', Math.max(0, Math.min(1, -dx / 120)));
      });
      var end = function () {
        if (!dragging) return; dragging = false;
        if (Math.abs(dx) > 110) { fly(dx > 0); }
        else if (Math.abs(dx) < 6 && Math.abs(dy) < 6) { el.classList.toggle('expanded'); el.style.transform = ''; }
        else { el.style.transition = 'transform .25s'; el.style.transform = ''; el.style.setProperty('--like', 0); el.style.setProperty('--pass', 0); }
        dx = dy = 0;
      };
      el.addEventListener('pointerup', end); el.addEventListener('pointercancel', end);
    }
    $$('.deck-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        var a = b.getAttribute('data-act');
        if (a === 'like') fly(true); else if (a === 'pass') fly(false); else if (a === 'undo') undo();
        else if (a === 'info' && cards[0]) location.href = '/u/' + cards[0].username;
      });
    });
    document.addEventListener('keydown', function (e) {
      if (/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName) || !$('#match-modal').hidden) return;
      if (e.key === 'ArrowRight') fly(true); else if (e.key === 'ArrowLeft') fly(false);
      else if (e.key === 'Backspace') { e.preventDefault(); undo(); } else if (e.key === 'ArrowUp' && cards[0]) location.href = '/u/' + cards[0].username;
    });
    var modal = $('#match-modal');
    var showMatch = function (u) {
      $('#match-text').textContent = 'You and ' + u.name + ' liked each other. You\'re now friends!';
      $('#match-them').innerHTML = u.avatar ? '<img class="avatar avatar-xl" src="' + esc(u.avatar) + '" alt="">' : '<span class="avatar avatar-xl avatar-initials" style="--h:200">' + esc(u.name[0]) + '</span>';
      $('#match-msg').href = '/messages/' + u.username;
      modal.hidden = false; confetti(modal);
    };
    modal.addEventListener('click', function (e) { if (e.target === modal || e.target.closest('.js-close-match')) modal.hidden = true; });
    render();
  }
  function confetti(host) {
    var colors = ['#a88e00', '#1d4463', '#e8743b', '#c2367a', '#4b3fd8', '#2e8b3e'];
    for (var i = 0; i < 80; i++) {
      var p = document.createElement('i');
      p.className = 'confetti';
      p.style.left = Math.random() * 100 + 'vw';
      p.style.background = colors[i % colors.length];
      p.style.animationDelay = Math.random() * .5 + 's';
      p.style.animationDuration = 1.8 + Math.random() * 1.4 + 's';
      p.style.transform = 'rotate(' + Math.random() * 360 + 'deg)';
      host.appendChild(p);
      setTimeout(function (n) { n.remove(); }.bind(null, p), 3800);
    }
  }

  // Like back (matches page)
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('.js-likeback'); if (!f) return;
    e.preventDefault();
    post('/api/swipe', { target: f.querySelector('[name=target]').value, liked: 1 }).then(function (j) {
      if (j.match) { toast('💘 It\'s a match with ' + j.user.name + '!'); setTimeout(function () { location.href = '/messages/' + j.user.username; }, 900); }
    });
  });

  // ===== Quiz stepper =====
  var quiz = $('#quiz-form');
  if (quiz) {
    var steps = $$('.quiz-step', quiz);
    var bar = $('.quiz-progress span'), count = $('.quiz-count b');
    var show = function (i) {
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      bar.style.width = (i / steps.length * 100) + '%'; count.textContent = i + 1;
      steps[i].classList.remove('enter'); void steps[i].offsetWidth; steps[i].classList.add('enter');
    };
    steps.forEach(function (s, i) {
      $$('input[type=radio]', s).forEach(function (r) {
        r.addEventListener('change', function () {
          if (i < steps.length - 1) setTimeout(function () { show(i + 1); }, 260);
          else bar.style.width = '100%';
        });
      });
      var back = $('.js-quiz-back', s); if (back) back.addEventListener('click', function () { show(i - 1); });
    });
  }
  var share = $('.js-share-type');
  if (share) share.addEventListener('click', function () {
    var text = share.getAttribute('data-text');
    if (navigator.share) navigator.share({ text: text }).catch(function () {});
    else if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { toast('Copied to clipboard'); });
  });

  // ===== Rent split =====
  var rs = $('#rs-people');
  if (rs) {
    var tpl = $('#rs-person-tpl');
    var people = [{ name: 'You', size: 160, bath: true, park: 0, adj: 0 }, { name: 'Roommate', size: 130, bath: false, park: 0, adj: 0 }];
    var money = function (n) { return '$' + Math.round(n).toLocaleString(); };
    var addRow = function (p) {
      var n = tpl.content.firstElementChild.cloneNode(true);
      $('.rs-name', n).value = p.name; $('.rs-size', n).value = p.size; $('.rs-bath', n).checked = p.bath; $('.rs-park', n).value = p.park; $('.rs-adj', n).value = p.adj;
      $('.rs-del', n).addEventListener('click', function () { if ($$('.rs-person', rs).length > 2) { n.remove(); calc(); } else toast('You need at least 2 people'); });
      n.addEventListener('input', calc);
      rs.appendChild(n);
    };
    var lastSummary = '';
    var calc = function () {
      var rent = +$('#rs-rent').value || 0, util = +$('#rs-util').value || 0, commonPct = +$('#rs-common').value / 100;
      $('#rs-common-out').textContent = Math.round(commonPct * 100) + '% split evenly';
      var rows = $$('.rs-person', rs).map(function (n) {
        return { name: $('.rs-name', n).value || 'Roommate', size: Math.max(1, +$('.rs-size', n).value || 100), bath: $('.rs-bath', n).checked, park: +$('.rs-park', n).value || 0, adj: +$('.rs-adj', n).value || 0 };
      });
      var k = rows.length;
      var weights = rows.map(function (r) { return r.size * (r.bath ? 1.08 : 1); });
      var wsum = weights.reduce(function (a, b) { return a + b; }, 0);
      var adjSum = rows.reduce(function (a, r) { return a + r.adj; }, 0);
      var rentShares = rows.map(function (r, i) { return rent * commonPct / k + rent * (1 - commonPct) * weights[i] / wsum + r.adj - adjSum / k; });
      var utilShares = rows.map(function (r, i) { return $('#rs-utilmode').value === 'even' ? util / k : util * rentShares[i] / (rent || 1); });
      var totals = rows.map(function (r, i) { return rentShares[i] + utilShares[i] + r.park; });
      var max = Math.max.apply(null, totals.concat([1]));
      var colors = ['#1d4463', '#a88e00', '#e8743b', '#4b3fd8', '#2e8b3e', '#c2367a'];
      $('#rs-bars').innerHTML = rows.map(function (r, i) {
        return '<div class="rs-bar"><div class="rs-bar-top"><strong>' + esc(r.name) + '</strong><span class="rs-amt">' + money(totals[i]) + '<small>/mo</small></span></div>' +
          '<div class="rs-track"><span style="width:' + (totals[i] / max * 100) + '%;background:' + colors[i % colors.length] + '"></span></div>' +
          '<div class="small muted">Rent ' + money(rentShares[i]) + ' · Utilities ' + money(utilShares[i]) + (r.park ? ' · Parking ' + money(r.park) : '') + (r.bath ? ' · Private bath' : '') + '</div></div>';
      }).join('');
      var grand = totals.reduce(function (a, b) { return a + b; }, 0);
      $('#rs-total').textContent = 'Total ' + money(grand) + '/mo · ' + money(grand * 12) + '/yr';
      lastSummary = 'Here\'s a fair rent split (' + money(rent) + ' rent + ' + money(util) + ' utilities):\n' +
        rows.map(function (r, i) { return '• ' + r.name + ': ' + money(totals[i]) + '/mo (' + r.size + ' sq ft' + (r.bath ? ', private bath' : '') + (r.park ? ', parking' : '') + ')'; }).join('\n');
    };
    people.forEach(addRow);
    $('#rs-add').addEventListener('click', function () { if ($$('.rs-person', rs).length >= 6) return toast('Up to 6 roommates'); addRow({ name: 'Roommate ' + ($$('.rs-person', rs).length + 1), size: 120, bath: false, park: 0, adj: 0 }); calc(); });
    ['#rs-rent', '#rs-util', '#rs-common', '#rs-utilmode'].forEach(function (s) { $(s).addEventListener('input', calc); $(s).addEventListener('change', calc); });
    $('#rs-copy').addEventListener('click', function () { navigator.clipboard && navigator.clipboard.writeText(lastSummary).then(function () { toast('Summary copied'); }); });
    var fr = $('#rs-friend'); if (fr) fr.addEventListener('change', function () { if (fr.value) location.href = '/messages/' + fr.value + '?draft=' + encodeURIComponent(lastSummary); });
    calc();
  }

  // ===== Property lounge =====
  var lounge = $('#lounge');
  if (lounge) {
    var pid = lounge.getAttribute('data-pid'), box = $('#lounge-msgs'), lastId = 0, first = true;
    var renderMsgs = function (list) {
      if (first) { box.innerHTML = ''; if (!list.length) box.innerHTML = '<p class="muted small center lounge-empty">No messages yet. Start the conversation!</p>'; }
      if (list.length) { var e = $('.lounge-empty', box); if (e) e.remove(); }
      var stick = box.scrollHeight - box.scrollTop - box.clientHeight < 60 || first;
      list.forEach(function (m) {
        if (m.id <= lastId) return; lastId = m.id;
        var d = document.createElement('div');
        d.className = 'lmsg' + (m.mine ? ' mine' : '');
        d.innerHTML = '<a href="/u/' + esc(m.username) + '">' + avatarHTML(m, 'xs') + '</a><div><div class="lmsg-meta"><a href="/u/' + esc(m.username) + '">' + esc(m.mine ? 'You' : m.name) + '</a> · ' + esc(m.time) + '</div><div class="lmsg-body">' + esc(m.body) + '</div></div>';
        box.appendChild(d);
      });
      if (stick) box.scrollTop = box.scrollHeight;
      first = false;
    };
    var pollL = function () {
      if (document.hidden && !first) return;
      getJSON('/api/lounge/' + pid + (lastId ? '?after=' + lastId : '')).then(function (j) {
        renderMsgs(j.messages); $('#lounge-online').textContent = j.online ? '● ' + j.online + ' online' : '';
      }).catch(function () {});
    };
    pollL(); setInterval(pollL, 5000);
    var lf = $('#lounge-form');
    if (lf) lf.addEventListener('submit', function (e) {
      e.preventDefault();
      var inp = lf.body, body = inp.value.trim(); if (!body) return;
      inp.value = '';
      fetch('/api/lounge/' + pid + (lastId ? '?after=' + lastId : ''), { method: 'POST', credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch', 'Accept': 'application/json' },
        body: (function () { var f = new FormData(); f.append('_csrf', CSRF); f.append('body', body); return f; })() })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw j; return j; }); })
        .then(function (j) { renderMsgs(j.messages); })
        .catch(function (j) { inp.value = body; toast((j && j.error) || 'Not sent'); });
    });
  }

})();

/* ---------- Emoji, GIFs, reactions, rich chat, themes ---------- */
(function () {
  'use strict';
  var CSRF = (document.querySelector('meta[name=csrf]') || {}).content || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { var d = document.createElement('div'); d.textContent = s == null ? '' : s; return d.innerHTML; }
  function linkify(s) { return esc(s).replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener nofollow">$1</a>'); }
  function req(url, data, method) {
    var o = { method: method || (data ? 'POST' : 'GET'), credentials: 'same-origin', headers: { 'X-Requested-With': 'fetch', 'Accept': 'application/json' } };
    if (data) { var fd = new FormData(); fd.append('_csrf', CSRF); Object.keys(data).forEach(function (k) { if (data[k] != null) fd.append(k, data[k]); }); o.body = fd; }
    return fetch(url, o).then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) throw j; return j; }); });
  }
  function toast(msg) { var t = document.createElement('div'); t.className = 'toast'; t.textContent = msg; document.body.appendChild(t); setTimeout(function () { t.remove(); }, 2600); }
  var isTouch = window.matchMedia('(hover: none)').matches;

  // ===== Popover helper =====
  var openPop = null;
  function closePop() { if (openPop) { openPop.remove(); openPop = null; } }
  function showPop(el, anchor, opts) {
    closePop(); opts = opts || {};
    el.classList.add('pop'); document.body.appendChild(el); openPop = el;
    var r = anchor.getBoundingClientRect(), w = el.offsetWidth, h = el.offsetHeight, vw = document.documentElement.clientWidth;
    var left = Math.min(Math.max(8, (opts.alignRight ? r.right - w : r.left + r.width / 2 - w / 2)), vw - w - 8);
    var top = r.top - h - 8; if (top < 8 || opts.below) top = r.bottom + 8;
    if (top + h > window.innerHeight - 8) top = Math.max(8, window.innerHeight - h - 8);
    el.style.left = left + 'px'; el.style.top = top + 'px';
    return el;
  }
  document.addEventListener('pointerdown', function (e) { if (openPop && !openPop.contains(e.target) && !e.target.closest('.js-emoji,.js-gif')) closePop(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { closePop(); closeMenu(); } });
  window.addEventListener('resize', closePop);

  // ===== Emoji picker =====
  var EMOJI = {
    'Smileys': '😀 😃 😄 😁 😆 😅 🤣 😂 🙂 😉 😊 😇 🥰 😍 🤩 😘 😋 😛 😜 🤪 🤗 🤭 🤫 🤔 😐 😏 😒 🙄 😬 😌 😔 😴 🥱 😷 🤒 🥳 😎 🤓 😕 😟 😮 😲 🥺 😢 😭 😱 😤 😡 🤯 😳 🥵 🥶 😈 💀 🤡 👻 👽 🤖 💩',
    'Gestures': '👍 👎 👌 🤌 ✌️ 🤞 🤟 🤘 🤙 👋 👏 🙌 👐 🤲 🙏 🤝 💪 👀 🫶 ❤️ 🧡 💛 💚 💙 💜 🖤 🤍 💔 ❣️ 💕 💯 ✨ 🔥 ⭐ 🎉 🎊 💥 💫',
    'Home': '🏠 🏡 🏢 🏘️ 🔑 🗝️ 🛋️ 🛏️ 🚿 🛁 🧹 🧺 🧼 🧽 🪴 🖼️ 📦 🚚 🧾 💸 💵 💳 📅 ⏰ 💡 🔌 📶 🧯 🚗 🅿️ 🚲 🐶 🐱 🐾 🍳 🥡 🍕 🍔 🌮 🍜 🍣 ☕ 🍷 🍺',
    'Activities': '🎮 🎲 🎵 🎧 🎸 🎤 🎬 📺 📚 💻 🏋️ 🧘 🏃 ⚽ 🏀 🏈 ⚾ 🎾 🏊 🚴 🥾 🏕️ ✈️ 🌴 🏖️ 🎨 📷 🎂 🎁 🛍️',
    'Weather': '☀️ 🌤️ ⛅ 🌧️ ⛈️ 🌈 ❄️ 🌙 🌟 🌊 🌵 🌸 🌻 🍂'
  };
  function emojiPicker(onPick) {
    var el = document.createElement('div');
    el.className = 'emoji-pop';
    var tabs = Object.keys(EMOJI);
    el.innerHTML = '<div class="ep-tabs">' + tabs.map(function (t, i) { return '<button type="button" data-t="' + i + '" class="' + (i ? '' : 'on') + '">' + EMOJI[t].split(' ')[0] + '</button>'; }).join('') + '</div><div class="ep-grid"></div>';
    var grid = $('.ep-grid', el);
    var fill = function (i) { grid.innerHTML = EMOJI[tabs[i]].split(' ').map(function (e) { return '<button type="button">' + e + '</button>'; }).join(''); grid.scrollTop = 0; };
    fill(0);
    el.addEventListener('click', function (e) {
      var t = e.target.closest('.ep-tabs button');
      if (t) { $$('.ep-tabs button', el).forEach(function (b) { b.classList.remove('on'); }); t.classList.add('on'); fill(+t.dataset.t); return; }
      var b = e.target.closest('.ep-grid button'); if (b) onPick(b.textContent);
    });
    return el;
  }
  function insertAtCursor(input, text) {
    var s = input.selectionStart != null ? input.selectionStart : input.value.length, en = input.selectionEnd != null ? input.selectionEnd : s;
    input.value = input.value.slice(0, s) + text + input.value.slice(en);
    var pos = s + text.length; try { input.setSelectionRange(pos, pos); } catch (e) {}
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.js-emoji'); if (!b) return;
    e.preventDefault();
    if (openPop && openPop.classList.contains('emoji-pop')) return closePop();
    var target = $(b.dataset.target) || b.closest('form').querySelector('textarea, input[type=text]');
    showPop(emojiPicker(function (em) { insertAtCursor(target, em); if (!isTouch) target.focus(); }), b);
  });

  // ===== GIF picker =====
  var gifModal = null;
  function openGifPicker(onPick) {
    if (gifModal) gifModal.remove();
    var m = document.createElement('div');
    m.className = 'modal gif-modal';
    m.innerHTML = '<div class="modal-box"><div class="gif-head"><input type="search" placeholder="Search GIFs" class="gif-q" autocomplete="off"><button type="button" class="iconbtn gif-x" aria-label="Close">✕</button></div>' +
      '<div class="gif-grid"><p class="muted small center">Loading…</p></div>' +
      '<form class="gif-link"><input type="url" placeholder="…or paste a GIF link (GIPHY, Tenor or .gif)" class="gif-url"><button class="btn btn-outline btn-sm">Add</button></form>' +
      '<p class="gif-credit small muted">Powered by GIPHY</p></div>';
    document.body.appendChild(m); gifModal = m;
    var close = function () { m.remove(); gifModal = null; };
    m.addEventListener('click', function (e) { if (e.target === m || e.target.closest('.gif-x')) close(); });
    var grid = $('.gif-grid', m), q = $('.gif-q', m), timer;
    var load = function () {
      req('/api/gifs?q=' + encodeURIComponent(q.value.trim())).then(function (j) {
        if (!j.enabled) { grid.innerHTML = '<p class="muted small center gif-off">GIF search isn\'t switched on yet. You can still paste a GIF link below.</p>'; q.hidden = true; $('.gif-credit', m).hidden = true; return; }
        grid.innerHTML = j.results.length ? j.results.map(function (g) { return '<button type="button" data-url="' + esc(g.url) + '"><img src="' + esc(g.thumb) + '" alt="' + esc(g.title) + '" loading="lazy"></button>'; }).join('') : '<p class="muted small center">No GIFs found.</p>';
      }).catch(function () { grid.innerHTML = '<p class="muted small center">Couldn\'t load GIFs.</p>'; });
    };
    q.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(load, 300); });
    grid.addEventListener('click', function (e) { var b = e.target.closest('button[data-url]'); if (b) { close(); onPick(b.dataset.url); } });
    $('.gif-link', m).addEventListener('submit', function (e) {
      e.preventDefault(); var u = $('.gif-url', m).value.trim();
      if (!/^https:\/\/\S+$/i.test(u) || !(/(giphy\.com|tenor\.com)/i.test(u) || /\.(gif|webp)(\?|$)/i.test(u))) return toast('Paste an https GIF link from GIPHY, Tenor or ending in .gif');
      close(); onPick(u);
    });
    load(); if (!isTouch) setTimeout(function () { q.focus(); }, 50);
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.js-gif'); if (!b) return;
    e.preventDefault();
    var form = b.closest('form');
    if (b.dataset.mode === 'chat') return openGifPicker(function (url) { chatSend('', url); });
    openGifPicker(function (url) {
      var hidden = form.querySelector('input[name=gif]'); hidden.value = url;
      var prev = form.querySelector('.gif-preview');
      if (prev) { $('img', prev).src = url; prev.hidden = false; var ip = form.querySelector('.js-img-input'); if (ip) { ip.value = ''; var cp = form.querySelector('.composer-preview'); if (cp) cp.hidden = true; } }
      else form.requestSubmit ? form.requestSubmit() : form.submit(); // comments: send right away
    });
  });
  document.addEventListener('click', function (e) {
    var x = e.target.closest('.gif-clear'); if (!x) return;
    var f = x.closest('form'); f.querySelector('input[name=gif]').value = ''; x.closest('.gif-preview').hidden = true;
  });
  // Comments: allow GIF-only submit, block empty
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('.comment-form'); if (!f) return;
    if (!f.body.value.trim() && !f.gif.value) e.preventDefault();
  }, true);

  // ===== Post reactions =====
  var hoverTimer = null, pressTimer = null, suppressClick = false;
  function showPicker(wrap) {
    $$('.react-wrap.open').forEach(function (w) { if (w !== wrap) w.classList.remove('open'); });
    var bar = document.querySelector('.topbar'), limit = bar ? bar.getBoundingClientRect().bottom : 0;
    wrap.classList.toggle('below', wrap.getBoundingClientRect().top - 64 < limit + 4);
    wrap.classList.add('open');
  }
  function hidePicker(wrap) { wrap.classList.remove('open'); }
  document.addEventListener('mouseover', function (e) {
    if (isTouch) return; var w = e.target.closest('.react-wrap'); if (!w) return;
    clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { showPicker(w); }, 450);
  });
  document.addEventListener('mouseout', function (e) {
    if (isTouch) return; var w = e.target.closest('.react-wrap'); if (!w || w.contains(e.relatedTarget)) return;
    clearTimeout(hoverTimer); hoverTimer = setTimeout(function () { hidePicker(w); }, 350);
  });
  document.addEventListener('touchstart', function (e) {
    var b = e.target.closest('.react-btn'); if (!b) return;
    suppressClick = false;
    pressTimer = setTimeout(function () { suppressClick = true; showPicker(b.closest('.react-wrap')); if (navigator.vibrate) navigator.vibrate(15); }, 420);
  }, { passive: true });
  document.addEventListener('touchend', function () { clearTimeout(pressTimer); });
  document.addEventListener('touchmove', function () { clearTimeout(pressTimer); }, { passive: true });
  document.addEventListener('contextmenu', function (e) { if (e.target.closest('.react-btn')) e.preventDefault(); });
  document.addEventListener('pointerdown', function (e) { if (!e.target.closest('.react-wrap')) $$('.react-wrap.open').forEach(hidePicker); });
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('.js-react'); if (!f) return;
    e.preventDefault();
    var sub = e.submitter, reaction = sub && sub.name === 'reaction' ? sub.value : null;
    if (!reaction && suppressClick) { suppressClick = false; return; }
    hidePicker(f);
    var btn = $('.react-btn', f);
    req(f.action, { reaction: reaction }).then(function (j) {
      var opt = j.reaction ? f.querySelector('.react-picker [value="' + j.reaction + '"]') : null;
      btn.className = 'act react-btn' + (j.reaction ? ' reacted r-' + j.reaction : '');
      $('.react-ico', btn).innerHTML = opt ? opt.dataset.emoji : '<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20s-7.5-4.6-9-9.5C2 7 4.5 4.5 7.5 4.5c2 0 3.5 1.2 4.5 2.7 1-1.5 2.5-2.7 4.5-2.7 3 0 5.5 2.5 4.5 6-1.5 4.9-9 9.5-9 9.5z"/></svg>';
      $('.react-label', btn).textContent = opt ? opt.dataset.label : 'Like';
      btn.classList.add('pop-anim'); setTimeout(function () { btn.classList.remove('pop-anim'); }, 300);
      var sum = f.closest('.post').querySelector('.reaction-summary');
      if (sum) { sum.hidden = !j.count; $('.rs-icons', sum).innerHTML = j.top.map(function (x) { return '<span>' + x + '</span>'; }).join(''); $('.rs-count', sum).textContent = j.count; }
    }).catch(function (j) { toast((j && j.error) || 'Something went wrong'); });
  });

  // ===== Rich chat =====
  var box = $('#chat-msgs'), form = $('#chat-form'), typingEl = $('#typing');
  var chatSend = function () {};
  var menu = null;
  function closeMenu() { if (menu) { menu.remove(); menu = null; } $$('.msg.menu-open').forEach(function (m) { m.classList.remove('menu-open'); }); }
  if (box) {
    var other = box.dataset.other, otherName = form ? form.dataset.otherName : '';
    var last = 0, since = '', lastDate = '', byId = {}, replyTo = null, editing = null;
    var QUICK = ['❤️', '😂', '😮', '😢', '😡', '👍'];
    var startReply = function () {}, startEdit = function () {};
    var atBottom = function () { return box.scrollHeight - box.scrollTop - box.clientHeight < 90; };
    var toBottom = function () { box.scrollTop = box.scrollHeight; };
    function inner(m) {
      if (m.deleted) return '<div class="bubble unsent">🚫 ' + (m.mine ? 'You unsent a message' : 'This message was unsent') + '</div>';
      var h = '';
      if (m.reply) h += '<a href="#m-' + m.reply.id + '" class="reply-quote" data-jump="' + m.reply.id + '"><small>' + (m.reply.mine ? (m.mine ? 'You replied to yourself' : 'Replied to you') : (m.mine ? 'You replied to ' + esc(otherName) : 'Replied to themselves')) + '</small><span>' + esc(m.reply.body || '') + '</span></a>';
      if (m.gif) h += '<div class="bubble gif"><img src="' + esc(m.gif) + '" alt="GIF" loading="lazy"></div>';
      if (m.body) {
        var onlyEmoji = /^(\p{Extended_Pictographic}|\p{Emoji_Component}|‍|️|\s){1,12}$/u.test(m.body) && !/[0-9#*]/.test(m.body);
        h += '<div class="bubble' + (onlyEmoji ? ' big-emoji' : '') + '">' + linkify(m.body) + '</div>';
      }
      if (m.reactions && m.reactions.length) h += '<div class="msg-reacts">' + m.reactions.map(function (r) { return '<button type="button" class="' + (r.mine ? 'mine' : '') + '" data-emoji="' + esc(r.emoji) + '">' + esc(r.emoji) + (r.count > 1 ? ' ' + r.count : '') + '</button>'; }).join('') + '</div>';
      return h;
    }
    function render(m) {
      byId[m.id] = m;
      var el = document.getElementById('m-' + m.id);
      var html = inner(m) + '<time>' + esc(m.time) + (m.edited && !m.deleted ? ' · edited' : '') + '</time>';
      if (el) { el.innerHTML = html; el.className = 'msg ' + (m.mine ? 'mine' : 'theirs') + (m.deleted ? ' is-unsent' : ''); return; }
      var hello = $('.chat-hello', box); if (hello) hello.hidden = true;
      if (m.date !== lastDate) { lastDate = m.date; var d = document.createElement('div'); d.className = 'chat-date'; d.textContent = m.date; box.appendChild(d); }
      el = document.createElement('div');
      el.id = 'm-' + m.id; el.className = 'msg ' + (m.mine ? 'mine' : 'theirs') + (m.deleted ? ' is-unsent' : '');
      el.dataset.id = m.id; el.innerHTML = html;
      box.appendChild(el);
      if (m.id > last) last = m.id;
    }
    function seen(lastRead) {
      var s = $('.seen', box); if (s) s.remove();
      var mine = $$('.msg.mine', box).pop();
      if (mine && lastRead && +mine.dataset.id <= lastRead) { var el = document.createElement('div'); el.className = 'seen'; el.textContent = 'Seen'; box.appendChild(el); }
    }
    JSON.parse(box.dataset.initial || '[]').forEach(render);
    toBottom();
    var busy = false;
    var poll = function () {
      if (busy || document.hidden) return; busy = true;
      req('/api/conversation/' + other + '?after=' + last + (since ? '&since=' + encodeURIComponent(since) : '')).then(function (j) {
        var stick = atBottom();
        (j.messages || []).forEach(render); (j.updated || []).forEach(render);
        since = j.now || since; seen(j.last_read);
        if (typingEl) typingEl.hidden = !j.typing;
        if (j.counts) $$('[data-count="messages"] .badge').forEach(function (b) { b.textContent = j.counts.messages; b.hidden = !j.counts.messages; });
        if (stick) toBottom();
      }).catch(function () {}).then(function () { busy = false; });
    };
    setInterval(poll, 3000); document.addEventListener('visibilitychange', poll); poll();

    // Jump to quoted message
    box.addEventListener('click', function (e) {
      var q = e.target.closest('[data-jump]'); if (q) { e.preventDefault(); var t = document.getElementById('m-' + q.dataset.jump); if (t) { t.scrollIntoView({ behavior: 'smooth', block: 'center' }); t.classList.add('flash-msg'); setTimeout(function () { t.classList.remove('flash-msg'); }, 1200); } return; }
      var r = e.target.closest('.msg-reacts button'); if (r) react(+r.closest('.msg').dataset.id, r.dataset.emoji);
    });
    // Double-tap / double-click to ❤️
    box.addEventListener('dblclick', function (e) { var el = e.target.closest('.msg'); if (el && !el.classList.contains('is-unsent')) { window.getSelection && window.getSelection().removeAllRanges(); react(+el.dataset.id, '❤️'); } });

    function react(id, emoji) { req('/api/message/' + id, { action: 'react', emoji: emoji }).then(function (j) { render(j.message); }).catch(function (j) { toast((j && j.error) || 'Couldn\'t react'); }); }

    // Context menu: right-click or long-press
    function openMenu(el, x, y) {
      var m = byId[el.dataset.id]; if (!m || m.deleted) return;
      closeMenu(); el.classList.add('menu-open');
      menu = document.createElement('div');
      menu.className = 'msg-menu';
      menu.innerHTML = '<div class="mm-reacts">' + QUICK.map(function (q) { return '<button type="button" data-react="' + q + '">' + q + '</button>'; }).join('') + '<button type="button" data-more="1" aria-label="More reactions">＋</button></div>' +
        (form ? '<button type="button" data-act="reply">↩️ Reply</button>' : '') +
        (m.body ? '<button type="button" data-act="copy">📋 Copy text</button>' : '') +
        (m.can_edit && m.body ? '<button type="button" data-act="edit">✏️ Edit</button>' : '') +
        (m.mine ? '<button type="button" data-act="unsend" class="danger">🗑️ Unsend</button>' : '');
      document.body.appendChild(menu);
      var w = menu.offsetWidth, h = menu.offsetHeight, vw = document.documentElement.clientWidth;
      menu.style.left = Math.min(Math.max(8, x - w / 2), vw - w - 8) + 'px';
      menu.style.top = (y - h - 12 > 8 ? y - h - 12 : Math.min(y + 12, window.innerHeight - h - 8)) + 'px';
      menu.addEventListener('click', function (e) {
        var b = e.target.closest('button'); if (!b) return;
        if (b.dataset.react) { react(m.id, b.dataset.react); closeMenu(); return; }
        if (b.dataset.more) { var anchor = b; showPop(emojiPicker(function (em) { closePop(); react(m.id, em); }), anchor); closeMenu(); return; }
        var a = b.dataset.act; closeMenu();
        if (a === 'reply') startReply(m);
        else if (a === 'copy') { navigator.clipboard && navigator.clipboard.writeText(m.body).then(function () { toast('Copied'); }); }
        else if (a === 'edit') startEdit(m);
        else if (a === 'unsend') { if (confirm('Unsend this message? It will show as "message unsent" for both of you.')) req('/api/message/' + m.id, { action: 'unsend' }).then(function (j) { render(j.message); }).catch(function (j) { toast((j && j.error) || 'Couldn\'t unsend'); }); }
      });
    }
    box.addEventListener('contextmenu', function (e) {
      var el = e.target.closest('.msg'); if (!el || e.target.closest('a[href^="http"]')) return;
      e.preventDefault(); openMenu(el, e.clientX, e.clientY);
    });
    var lpTimer = null, lpStart = null;
    box.addEventListener('touchstart', function (e) {
      var el = e.target.closest('.msg'); if (!el) return;
      var t = e.touches[0]; lpStart = [t.clientX, t.clientY];
      lpTimer = setTimeout(function () { if (navigator.vibrate) navigator.vibrate(15); openMenu(el, lpStart[0], lpStart[1]); }, 450);
    }, { passive: true });
    box.addEventListener('touchmove', function (e) { var t = e.touches[0]; if (lpStart && Math.hypot(t.clientX - lpStart[0], t.clientY - lpStart[1]) > 10) clearTimeout(lpTimer); }, { passive: true });
    box.addEventListener('touchend', function () { clearTimeout(lpTimer); });
    document.addEventListener('pointerdown', function (e) { if (menu && !menu.contains(e.target)) closeMenu(); });
    box.addEventListener('scroll', closeMenu, { passive: true });

    if (form) {
      var ta = $('textarea', form), replyBar = $('#reply-bar'), editBar = $('#edit-bar');
      var grow = function () { ta.style.height = 'auto'; ta.style.height = Math.min(ta.scrollHeight, 140) + 'px'; };
      startReply = function (m) {
        cancelEdit(); replyTo = m.id;
        $('.rb-who', replyBar).textContent = m.mine ? 'yourself' : otherName;
        $('.rb-text', replyBar).textContent = m.body || 'GIF';
        replyBar.hidden = false; ta.focus();
      }
      function cancelReply() { replyTo = null; replyBar.hidden = true; }
      startEdit = function (m) {
        cancelReply(); editing = m.id;
        $('.rb-text', editBar).textContent = m.body; editBar.hidden = false;
        ta.value = m.body; grow(); ta.focus();
      }
      function cancelEdit() { if (editing) { editing = null; editBar.hidden = true; ta.value = ''; grow(); } }
      $('.rb-x', replyBar).addEventListener('click', cancelReply);
      $('.rb-x', editBar).addEventListener('click', cancelEdit);
      var lastTyping = 0;
      ta.addEventListener('input', function () {
        grow(); var now = Date.now();
        if (now - lastTyping > 3000 && ta.value.trim()) { lastTyping = now; req('/api/typing/' + other, {}).catch(function () {}); }
      });
      ta.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey && !e.isComposing && !isTouch) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit', { cancelable: true })); }
        if (e.key === 'Escape') { cancelReply(); cancelEdit(); }
        if (e.key === 'ArrowUp' && !ta.value) { var mine = Object.keys(byId).map(function (k) { return byId[k]; }).filter(function (m) { return m.mine && m.can_edit && m.body; }).pop(); if (mine) { e.preventDefault(); startEdit(mine); } }
      });
      chatSend = function (body, gif) {
        var tmp = document.createElement('div');
        tmp.className = 'msg mine pending';
        tmp.innerHTML = (gif ? '<div class="bubble gif"><img src="' + esc(gif) + '" alt=""></div>' : '') + (body ? '<div class="bubble">' + linkify(body) + '</div>' : '') + '<time>Sending…</time>';
        var hello = $('.chat-hello', box); if (hello) hello.hidden = true;
        box.appendChild(tmp); toBottom();
        var rt = replyTo; cancelReply();
        return req('/api/conversation/' + other, { body: body, gif: gif || '', reply_to: rt || '' }).then(function (j) { tmp.remove(); render(j.message); toBottom(); })
          .catch(function (j) { tmp.remove(); if (body) ta.value = body; toast((j && j.error) || 'Message not sent'); });
      };
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var body = ta.value.trim(); if (!body) return;
        if (editing) {
          var id = editing; cancelEdit();
          req('/api/message/' + id, { action: 'edit', body: body }).then(function (j) { render(j.message); }).catch(function (j) { toast((j && j.error) || 'Couldn\'t edit'); });
          return;
        }
        ta.value = ''; grow(); chatSend(body, null);
      });
      if (!isTouch) ta.focus();
    }
  }

  // ===== Lounge input emoji (reuses picker) is wired via .js-emoji =====

  // ===== Theme picker =====
  var tf = $('#theme-form');
  if (tf) {
    var apply = function () {
      var t = tf.querySelector('input[name=theme]:checked').value, m = tf.querySelector('input[name=mode]:checked').value;
      var root = document.documentElement;
      if (t === 'navy') delete root.dataset.theme; else root.dataset.theme = t;
      if (m === 'system') delete root.dataset.mode; else root.dataset.mode = m;
      try { localStorage.setItem('rr-theme', t); localStorage.setItem('rr-mode', m); } catch (e) {}
      req('/api/theme', { theme: t, mode: m }).then(function () { toast('Appearance saved'); }).catch(function () { toast('Couldn\'t save'); });
    };
    tf.addEventListener('change', apply);
  }
})();
