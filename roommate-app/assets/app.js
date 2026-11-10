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

  // Likes
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('.js-like');
    if (!f) return;
    e.preventDefault();
    var b = $('button', f);
    api(f.action, { method: 'POST', body: new FormData(f) }).then(function (j) {
      b.classList.toggle('liked', j.liked);
      b.setAttribute('aria-pressed', j.liked ? 'true' : 'false');
      $('.n', b).textContent = j.likes || '';
    }).catch(function (j) { toast((j && j.error) || 'Something went wrong'); });
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

  // Chat
  var box = $('#chat-msgs');
  var form = $('#chat-form');
  if (box) {
    var other = box.getAttribute('data-other');
    var last = parseInt(box.getAttribute('data-last'), 10) || 0;
    var lastDate = ($$('.chat-date', box).pop() || {}).textContent || '';
    var atBottom = function () { return box.scrollHeight - box.scrollTop - box.clientHeight < 80; };
    var toBottom = function () { box.scrollTop = box.scrollHeight; };
    toBottom();

    var render = function (m) {
      if (box.querySelector('[data-id="' + m.id + '"]')) return;
      var hello = $('.chat-hello', box); if (hello) hello.remove();
      if (m.date !== lastDate) {
        lastDate = m.date;
        var d = document.createElement('div'); d.className = 'chat-date'; d.textContent = m.date; box.appendChild(d);
      }
      var el = document.createElement('div');
      el.className = 'msg ' + (m.mine ? 'mine' : 'theirs');
      el.setAttribute('data-id', m.id);
      el.innerHTML = '<div class="bubble">' + linkify(m.body) + '</div><time>' + esc(m.time) + '</time>';
      box.appendChild(el);
      if (m.id > last) last = m.id;
    };
    var seen = function (lastRead) {
      var s = $('.seen', box); if (s) s.remove();
      var mine = $$('.msg.mine', box).pop();
      if (mine && lastRead && parseInt(mine.getAttribute('data-id'), 10) <= lastRead) {
        var el = document.createElement('div'); el.className = 'seen'; el.textContent = 'Seen'; box.appendChild(el);
      }
    };
    var busy = false;
    var poll = function () {
      if (busy || document.hidden) return;
      busy = true;
      api('/api/conversation/' + other + '?after=' + last).then(function (j) {
        var stick = atBottom();
        (j.messages || []).forEach(render);
        seen(j.last_read);
        applyCounts(j.counts);
        if (stick) toBottom();
      }).catch(function () {}).then(function () { busy = false; });
    };
    setInterval(poll, 3500);
    document.addEventListener('visibilitychange', poll);
    poll();

    if (form) {
      var ta = $('textarea', form);
      ta.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event('submit', { cancelable: true })); }
      });
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var body = ta.value.trim();
        if (!body) return;
        ta.value = ''; grow(ta);
        var fd = new FormData(); fd.append('body', body); fd.append('_csrf', CSRF);
        var tmp = document.createElement('div');
        tmp.className = 'msg mine pending';
        tmp.innerHTML = '<div class="bubble">' + linkify(body) + '</div><time>Sending…</time>';
        box.appendChild(tmp); toBottom();
        api('/api/conversation/' + other, { method: 'POST', body: fd }).then(function (j) {
          tmp.remove(); render(j.message); toBottom();
        }).catch(function (j) {
          tmp.remove(); ta.value = body; toast((j && j.error) || 'Message not sent');
        });
      });
      if (window.matchMedia('(min-width: 721px)').matches) ta.focus();
    }
  } else if (document.body.classList.contains('authed')) {
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

  // ===== Typing indicator =====
  var cform = $('#chat-form'), typingEl = $('#typing');
  if (cform && typingEl) {
    var other = cform.getAttribute('data-other'), lastSent = 0;
    $('textarea', cform).addEventListener('input', function () {
      var now = Date.now();
      if (now - lastSent > 3000) { lastSent = now; post('/api/typing/' + other, {}).catch(function () {}); }
    });
    // Piggy-back on the chat poll responses
    var origFetch = window.fetch;
    window.fetch = function (url, opts) {
      var p = origFetch.apply(this, arguments);
      if (typeof url === 'string' && url.indexOf('/api/conversation/') === 0 && (!opts || !opts.method || opts.method === 'GET')) {
        p.then(function (r) { return r.clone().json(); }).then(function (j) {
          typingEl.hidden = !j.typing;
          if (j.typing) { var b = $('#chat-msgs'); if (b && b.scrollHeight - b.scrollTop - b.clientHeight < 120) b.scrollTop = b.scrollHeight; }
        }).catch(function () {});
      }
      return p;
    };
  }
})();
