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
