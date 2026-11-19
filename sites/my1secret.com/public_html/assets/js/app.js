/* My 1 Secret: progressive enhancement. Every feature also works without JavaScript. */
(function () {
  'use strict';
  var $$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var mnav = document.getElementById('mobile-nav');
  if (toggle && mnav) {
    toggle.addEventListener('click', function () {
      var open = mnav.hasAttribute('hidden');
      if (open) { mnav.removeAttribute('hidden'); } else { mnav.setAttribute('hidden', ''); }
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Close <details> dropdowns when clicking elsewhere
  document.addEventListener('click', function (e) {
    $$('details.dropdown[open]').forEach(function (d) { if (!d.contains(e.target)) { d.removeAttribute('open'); } });
  });

  // Confirm dialogs
  document.addEventListener('submit', function (e) {
    var f = e.target.closest('form[data-confirm]');
    if (f && !window.confirm(f.getAttribute('data-confirm'))) { e.preventDefault(); }
  }, true);

  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-confirm-click]');
    if (b && !window.confirm(b.getAttribute('data-confirm-click'))) { e.preventDefault(); }
  }, true);

  // Auto-submit selects (admin role picker)
  $$('[data-autosubmit]').forEach(function (s) { s.addEventListener('change', function () { s.form.submit(); }); });

  // Votes without page reload
  document.addEventListener('submit', function (e) {
    var form = e.target;
    var box = form.closest('[data-vote]');
    if (!box || e.defaultPrevented) { return; }
    e.preventDefault();
    var btn = form.querySelector('button');
    var val = parseInt(btn.getAttribute('data-val'), 10);
    var mine = parseInt(box.getAttribute('data-my'), 10) || 0;
    var next = mine === val ? 0 : val;
    var fd = new FormData(form);
    fd.set('value', String(next));
    box.classList.add('busy');
    fetch(form.action, { method: 'POST', body: fd, headers: { Accept: 'application/json' }, credentials: 'same-origin' })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); })
      .then(function (res) {
        box.classList.remove('busy');
        if (res.status === 401 && res.j.login) { window.location = res.j.login + '?next=' + encodeURIComponent(location.pathname); return; }
        if (!res.ok) { alert(res.j.error || 'Could not save your vote.'); return; }
        box.setAttribute('data-my', String(res.j.vote));
        box.querySelector('.vote-score').textContent = res.j.score.toLocaleString();
        $$('form', box).forEach(function (f) {
          var b = f.querySelector('button');
          var v = parseInt(b.getAttribute('data-val'), 10);
          var on = res.j.vote === v;
          b.classList.toggle('on', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
          f.querySelector('input[name=value]').value = on ? '0' : String(v);
        });
      })
      .catch(function () { box.classList.remove('busy'); form.submit(); });
  });

  // Inline reply forms
  document.addEventListener('click', function (e) {
    var r = e.target.closest('[data-reply]');
    if (r) {
      var slot = document.querySelector('[data-reply-slot="' + r.getAttribute('data-reply') + '"]');
      if (slot) {
        e.preventDefault();
        slot.hidden = !slot.hidden;
        if (!slot.hidden) { var ta = slot.querySelector('textarea'); if (ta) { ta.focus(); } }
      }
      return;
    }
    var c = e.target.closest('[data-cancel-reply]');
    if (c) { var s = c.closest('.reply-slot'); if (s) { s.hidden = true; } return; }
    var col = e.target.closest('[data-collapse]');
    if (col) {
      var li = col.closest('.comment');
      var collapsed = li.classList.toggle('collapsed');
      col.textContent = collapsed ? '[+]' : '[–]';
      col.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
      return;
    }
    var sh = e.target.closest('[data-share]');
    if (sh) {
      var url = sh.getAttribute('data-share');
      if (navigator.share) { navigator.share({ url: url, title: document.title }).catch(function () {}); }
      else if (navigator.clipboard) { navigator.clipboard.writeText(url).then(function () { sh.textContent = 'Link copied'; setTimeout(function () { sh.textContent = 'Share'; }, 2000); }); }
    }
  });

  // Character counters on SEO fields
  $$('[data-count]').forEach(function (el) {
    var out = document.createElement('span');
    out.className = 'hint';
    el.insertAdjacentElement('afterend', out);
    var upd = function () { out.textContent = el.value.length + ' characters'; };
    el.addEventListener('input', upd);
    upd();
  });

  // Submit with Ctrl/Cmd+Enter in comment boxes
  document.addEventListener('keydown', function (e) {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && e.target.matches('.comment-form textarea')) {
      e.target.form.requestSubmit ? e.target.form.requestSubmit() : e.target.form.submit();
    }
  });
})();
