/* Friendswood Roofers - progressive enhancements. Everything works without
   this file; it only adds convenience. No dependencies, no build step. */
(function () {
  'use strict';

  var doc = document.documentElement;
  doc.classList.remove('no-js');
  doc.classList.add('js');

  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  /* ---------- Sticky header shadow ---------- */
  var header = $('[data-header]');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Mobile navigation ---------- */
  var navToggle = $('[data-nav-toggle]');
  var nav = $('[data-nav]');
  var mobileQuery = window.matchMedia('(max-width: 1279px)');

  function setNav(open, returnFocus) {
    if (!navToggle || !nav) return;
    navToggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
    document.body.classList.toggle('nav-open', open);
    if (open) {
      var first = nav.querySelector('a, button');
      if (first) first.focus();
    } else if (returnFocus) {
      navToggle.focus();
    }
  }
  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      setNav(navToggle.getAttribute('aria-expanded') !== 'true', false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) setNav(false, true);
    });
    // Keep keyboard focus inside the open mobile menu.
    nav.addEventListener('keydown', function (e) {
      if (e.key !== 'Tab' || !nav.classList.contains('is-open') || !mobileQuery.matches) return;
      var items = $$('a, button', nav).filter(function (el) { return el.offsetParent !== null; });
      items.unshift(navToggle);
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === nav.querySelector('a, button')) { e.preventDefault(); navToggle.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    navToggle.addEventListener('keydown', function (e) {
      if (e.key === 'Tab' && e.shiftKey && nav.classList.contains('is-open') && mobileQuery.matches) {
        var items = $$('a, button', nav).filter(function (el) { return el.offsetParent !== null; });
        e.preventDefault();
        items[items.length - 1].focus();
      }
    });
    mobileQuery.addEventListener('change', function () { setNav(false, false); });
    // Close the menu after following an in-page link (e.g. #estimate-form).
    nav.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (a && a.hash && a.pathname === location.pathname) setNav(false, false);
    });
  }

  /* ---------- Services submenu (disclosure) ---------- */
  $$('[data-submenu]').forEach(function (item) {
    var btn = $('[data-submenu-toggle]', item);
    if (!btn) return;
    function set(open) {
      btn.setAttribute('aria-expanded', String(open));
      item.classList.toggle('is-open', open);
    }
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      set(btn.getAttribute('aria-expanded') !== 'true');
    });
    item.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && item.classList.contains('is-open')) { e.stopPropagation(); set(false); btn.focus(); }
    });
    item.addEventListener('focusout', function (e) {
      if (!mobileQuery.matches && !item.contains(e.relatedTarget)) set(false);
    });
    // Desktop: open on hover for mouse users.
    item.addEventListener('mouseenter', function () { if (!mobileQuery.matches) set(true); });
    item.addEventListener('mouseleave', function () { if (!mobileQuery.matches) set(false); });
    document.addEventListener('click', function (e) { if (!item.contains(e.target) && !mobileQuery.matches) set(false); });
  });

  /* ---------- Scroll reveal ---------- */
  var revealEls = $$('[data-reveal]');
  if (!reduceMotion && 'IntersectionObserver' in window && revealEls.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-in');
          entry.target.classList.remove('reveal-pending');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    var vh = window.innerHeight;
    revealEls.forEach(function (el) {
      // Only hide elements that start below the fold, so nothing visible flashes.
      if (el.getBoundingClientRect().top > vh * 0.92) {
        el.classList.add('reveal-pending');
        io.observe(el);
      }
    });
  }

  /* ---------- Estimate form ---------- */
  var labels = { name: 'Name', phone: 'Phone', email: 'Email', location: 'Property address or ZIP code', service: 'Service needed', consent: 'Consent' };

  function validateField(form, name) {
    var el = form.elements[name];
    if (!el) return '';
    var v = el.type === 'checkbox' ? el.checked : String(el.value || '').trim();
    switch (name) {
      case 'name': return v.length < 2 ? 'Please enter your name.' : '';
      case 'phone':
        if (!v) return 'Please enter a phone number so we can reach you.';
        var digits = v.replace(/\D/g, '');
        return (digits.length < 10 || digits.length > 15 || /[^0-9+().\-\sextEXT]/.test(v)) ? 'Please enter a valid phone number, including area code.' : '';
      case 'email':
        return v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? 'That email address doesn\'t look right. Check it, or leave it blank.' : '';
      case 'location': return v.length < 5 ? 'Please enter the property address or ZIP code.' : '';
      case 'service': return v ? '' : 'Please choose the service you need (or "Not sure / other").';
      case 'consent': return v ? '' : 'Please confirm we may contact you about this request.';
    }
    return '';
  }

  function showFieldError(form, name, msg) {
    var el = form.elements[name];
    var box = form.querySelector('#err-' + name);
    if (!el || !box) return;
    if (msg) {
      el.setAttribute('aria-invalid', 'true');
      box.innerHTML = '';
      box.insertAdjacentHTML('afterbegin', '<svg class="icon icon-sm" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/></svg>');
      var span = document.createElement('span');
      span.textContent = msg;
      box.appendChild(span);
      box.hidden = false;
    } else {
      el.removeAttribute('aria-invalid');
      box.hidden = true;
      box.textContent = '';
    }
  }

  function showStatus(statusEl, type, message, errors) {
    statusEl.hidden = false;
    statusEl.classList.toggle('is-success', type === 'success');
    statusEl.innerHTML = '';
    var p = document.createElement('p');
    p.className = 'form-status-title';
    p.innerHTML = type === 'success'
      ? '<svg class="icon icon-sm" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
      : '<svg class="icon icon-sm" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3 2 20h20z"/><path d="M12 10v4M12 17h.01"/></svg>';
    var s = document.createElement('span');
    s.textContent = message;
    p.appendChild(s);
    statusEl.appendChild(p);
    var keys = errors ? Object.keys(errors) : [];
    if (keys.length) {
      var ul = document.createElement('ul');
      keys.forEach(function (k) {
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.href = '#f-' + k;
        a.textContent = (labels[k] || k) + ': ' + errors[k];
        a.addEventListener('click', function (e) { e.preventDefault(); var f = document.getElementById('f-' + k); if (f) f.focus(); });
        li.appendChild(a);
        ul.appendChild(li);
      });
      statusEl.appendChild(ul);
    }
  }

  $$('[data-estimate-form]').forEach(function (form) {
    var card = form.closest('.estimate-card');
    var statusEl = card ? $('[data-form-status]', card) : null;
    var submit = $('[data-submit]', form);
    var submitLabel = $('[data-submit-label]', form);
    var fields = ['name', 'phone', 'email', 'location', 'service', 'consent'];
    var busy = false;

    // Validate on blur, re-validate as the user fixes a field.
    fields.forEach(function (name) {
      var el = form.elements[name];
      if (!el) return;
      el.addEventListener('blur', function () {
        if (el.type !== 'checkbox' && !String(el.value).trim() && name !== 'email' && !el.hasAttribute('aria-invalid')) return;
        showFieldError(form, name, validateField(form, name));
      });
      el.addEventListener(el.tagName === 'SELECT' || el.type === 'checkbox' ? 'change' : 'input', function () {
        if (el.getAttribute('aria-invalid') === 'true') showFieldError(form, name, validateField(form, name));
      });
    });

    form.addEventListener('submit', function (e) {
      var errors = {};
      fields.forEach(function (name) {
        var msg = validateField(form, name);
        showFieldError(form, name, msg);
        if (msg) errors[name] = msg;
      });
      var keys = Object.keys(errors);
      if (keys.length) {
        e.preventDefault();
        if (statusEl) showStatus(statusEl, 'error', 'Please correct the ' + (keys.length === 1 ? 'highlighted field' : keys.length + ' highlighted fields') + ' and try again.', errors);
        var firstBad = form.elements[keys[0]];
        if (firstBad) firstBad.focus();
        return;
      }
      if (!window.fetch || !window.FormData) return; // normal POST fallback
      e.preventDefault();
      if (busy) return;
      busy = true;
      submit.disabled = true;
      submit.setAttribute('aria-disabled', 'true');
      var original = submitLabel.textContent;
      submitLabel.textContent = 'Sending…';
      if (statusEl) { statusEl.hidden = true; }

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' },
        credentials: 'same-origin'
      }).then(function (res) {
        return res.json().catch(function () { return { ok: false, message: 'Sorry, something went wrong and your request was not sent. Please call us.' }; });
      }).then(function (data) {
        if (data && data.ok && data.redirect) {
          window.location.assign(data.redirect);
          return;
        }
        busy = false;
        submit.disabled = false;
        submit.removeAttribute('aria-disabled');
        submitLabel.textContent = original;
        var errs = (data && data.errors) || {};
        Object.keys(errs).forEach(function (k) { showFieldError(form, k, errs[k]); });
        if (statusEl) {
          showStatus(statusEl, 'error', (data && data.message) || 'Your request was not sent. Please try again or call us.', errs);
          statusEl.scrollIntoView({ block: 'center', behavior: reduceMotion ? 'auto' : 'smooth' });
        }
      }).catch(function () {
        busy = false;
        submit.disabled = false;
        submit.removeAttribute('aria-disabled');
        submitLabel.textContent = original;
        if (statusEl) showStatus(statusEl, 'error', 'We could not reach the server, so your request was not sent. Check your connection and try again, or call us.', null);
      });
    });
  });

  /* ---------- Blog category filters ---------- */
  var filterBar = $('[data-filter-bar]');
  var grid = $('[data-filter-grid]');
  if (filterBar && grid) {
    var status = $('[data-filter-status]');
    var buttons = $$('[data-filter]', filterBar);
    var applyFilter = function (cat, push) {
      var shown = 0;
      $$('.article-card', grid).forEach(function (card) {
        var match = cat === 'all' || card.getAttribute('data-category') === cat;
        card.hidden = !match;
        if (match) { shown++; card.classList.remove('reveal-pending'); }
      });
      buttons.forEach(function (b) {
        if (b.getAttribute('data-filter') === cat) b.setAttribute('aria-current', 'true');
        else b.removeAttribute('aria-current');
      });
      if (status) {
        var active = buttons.filter(function (b) { return b.getAttribute('data-filter') === cat; })[0];
        status.textContent = 'Showing ' + shown + ' article' + (shown === 1 ? '' : 's') + (cat === 'all' ? '' : ' in ' + active.textContent.trim()) + '.';
      }
      if (push && window.history && history.replaceState) {
        history.replaceState(null, '', cat === 'all' ? '/blog/' : '/blog/?category=' + encodeURIComponent(cat));
      }
    };
    buttons.forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault();
        applyFilter(b.getAttribute('data-filter'), true);
      });
    });
  }

  /* ---------- Roofing Project Planner ---------- */
  var planner = $('[data-planner]');
  if (planner) {
    var result = $('[data-planner-result]');
    var summaryBox = $('[data-planner-summary]');
    var copyBtn = $('[data-copy-summary]');
    var copyStatus = $('[data-copy-status]');
    var useBtn = $('[data-use-summary]');
    var tipsList = $('[data-planner-tips]');
    var linkP = $('[data-planner-link]');
    var questions = $$('[data-question]', planner);
    if (navigator.clipboard || document.queryCommandSupported) copyBtn.hidden = false;

    questions.forEach(function (fs) {
      fs.addEventListener('change', function () {
        fs.classList.remove('has-error');
        var err = fs.querySelector('.field-error');
        if (err) err.hidden = true;
        fs.removeAttribute('aria-describedby');
      });
    });

    planner.addEventListener('submit', function (e) {
      e.preventDefault();
      var lines = ['Roofing Project Planner summary', ''];
      var missing = [];
      var concern = null, damage = null;
      questions.forEach(function (fs) {
        var checked = fs.querySelector('input:checked');
        var err = fs.querySelector('.field-error');
        if (!checked) {
          missing.push(fs);
          fs.classList.add('has-error');
          if (err) { err.hidden = false; fs.setAttribute('aria-describedby', err.id); }
          return;
        }
        var label = planner.querySelector('label[for="' + checked.id + '"]').textContent.trim();
        lines.push(fs.getAttribute('data-label') + ': ' + label);
        if (fs.getAttribute('data-question') === 'concern') concern = checked;
        if (fs.getAttribute('data-question') === 'damage') damage = checked;
      });
      if (missing.length) {
        var firstInput = missing[0].querySelector('input');
        if (firstInput) firstInput.focus();
        return;
      }
      var notes = String(planner.elements.notes.value || '').trim();
      if (notes) lines.push('Notes: ' + notes);
      summaryBox.value = lines.join('\n');

      // Tips and related reading (general, non-diagnostic).
      tipsList.innerHTML = '';
      var tips = [];
      if (damage && damage.getAttribute('data-tip')) tips.push(damage.getAttribute('data-tip'));
      tips.push('Keep photos and notes together. Dated photos are useful for any later conversation with your insurer.');
      tips.forEach(function (t) { var li = document.createElement('li'); li.textContent = t; tipsList.appendChild(li); });
      linkP.innerHTML = '';
      if (concern && concern.getAttribute('data-link')) {
        linkP.appendChild(document.createTextNode('Related reading: '));
        var a = document.createElement('a');
        a.href = concern.getAttribute('data-link');
        a.textContent = concern.getAttribute('data-link-label');
        linkP.appendChild(a);
      }
      useBtn.setAttribute('data-service', concern ? concern.getAttribute('data-service') : '');
      copyStatus.textContent = '';
      result.hidden = false;
      result.focus();
      result.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    });

    var reset = $('[data-planner-reset]');
    if (reset) reset.addEventListener('click', function (e) {
      e.preventDefault();
      planner.reset();
      questions.forEach(function (fs) { fs.classList.remove('has-error'); var er = fs.querySelector('.field-error'); if (er) er.hidden = true; });
      result.hidden = true;
      summaryBox.value = '';
      history.replaceState && history.replaceState(null, '', '/roofing-project-planner/');
      var first = planner.querySelector('input[type="radio"]');
      if (first) first.focus();
    });

    copyBtn.addEventListener('click', function () {
      var text = summaryBox.value;
      var done = function () { copyStatus.textContent = 'Summary copied to your clipboard.'; };
      var fail = function () { summaryBox.removeAttribute('readonly'); summaryBox.select(); copyStatus.textContent = 'Press Ctrl+C (or Cmd+C) to copy the selected summary.'; };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, fail);
      } else {
        summaryBox.removeAttribute('readonly');
        summaryBox.select();
        try { document.execCommand('copy') ? done() : fail(); } catch (err) { fail(); }
        summaryBox.setAttribute('readonly', '');
      }
    });

    useBtn.addEventListener('click', function (e) {
      var msg = $('[data-message-field]');
      var svc = document.getElementById('f-service');
      if (!msg) return;
      e.preventDefault();
      var current = msg.value.trim();
      msg.value = current && current.indexOf(summaryBox.value) === -1 ? current + '\n\n' + summaryBox.value : summaryBox.value;
      var s = useBtn.getAttribute('data-service');
      if (svc && s && !svc.value) svc.value = s;
      var target = document.getElementById('estimate-form');
      target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
      copyStatus.textContent = 'Summary added to the estimate request form below.';
      var name = document.getElementById('f-name');
      if (name) setTimeout(function () { name.focus({ preventScroll: true }); }, reduceMotion ? 0 : 400);
    });
  }

  /* ---------- Weather map fallback ---------- */
  $$('[data-weather]').forEach(function (fig) {
    var frame = $('[data-weather-frame]', fig);
    var placeholder = $('[data-weather-placeholder]', fig);
    if (!frame || !placeholder) return;
    frame.addEventListener('load', function () { fig.classList.add('is-loaded'); });
    // If the map hasn't loaded 20s after it scrolls into view, emphasise the link.
    if ('IntersectionObserver' in window) {
      var wio = new IntersectionObserver(function (entries) {
        if (!entries[0].isIntersecting) return;
        wio.disconnect();
        setTimeout(function () {
          if (!fig.classList.contains('is-loaded')) {
            fig.classList.add('is-slow');
            frame.hidden = true;
            placeholder.querySelector('span').textContent = 'The live radar map could not be loaded right now. ';
            var a = document.createElement('a');
            a.href = fig.querySelector('.weather-ext').href;
            a.rel = 'noopener';
            a.textContent = 'Open the Friendswood radar on RainViewer';
            placeholder.querySelector('span').appendChild(a);
          }
        }, 20000);
      });
      wio.observe(fig);
    }
  });
})();
