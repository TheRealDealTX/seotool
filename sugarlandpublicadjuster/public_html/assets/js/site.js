/* Sugar Land Public Adjuster — navigation, lead popup and form handling. */
(function () {
  'use strict';
  var doc = document, body = doc.body;
  function store(kind) { try { return window[kind]; } catch (e) { return null; } }
  var ss = store('sessionStorage'), ls = store('localStorage');
  function get(s, k) { try { return s && s.getItem(k); } catch (e) { return null; } }
  function set(s, k, v) { try { s && s.setItem(k, v); } catch (e) {} }

  /* Header shadow */
  var header = doc.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* Mobile nav */
  var toggle = doc.querySelector('.nav-toggle');
  if (toggle) toggle.addEventListener('click', function () {
    var open = body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  doc.querySelectorAll('.sub-toggle').forEach(function (b) {
    b.addEventListener('click', function () {
      var sub = b.nextElementSibling, open = sub.classList.toggle('open');
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });

  /* Lead popup: opens once per session after 4 seconds, never after a submission. */
  var popup = doc.getElementById('lead-popup'), lastFocus = null;
  function openPopup() {
    if (!popup || !popup.hidden) return;
    lastFocus = doc.activeElement;
    popup.hidden = false; body.classList.add('popup-open');
    var f = popup.querySelector('input[name="name"]'); if (f) setTimeout(function () { f.focus(); }, 50);
    set(ss, 'slpa_popup_seen', '1');
  }
  function closePopup() {
    if (!popup || popup.hidden) return;
    popup.hidden = true; body.classList.remove('popup-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (popup) {
    popup.querySelectorAll('[data-close-popup]').forEach(function (el) { el.addEventListener('click', closePopup); });
    doc.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePopup(); });
    if (!get(ss, 'slpa_popup_seen') && !get(ls, 'slpa_lead_sent') && !body.classList.contains('no-auto-popup')) {
      setTimeout(function () {
        var a = doc.activeElement;
        // Don't interrupt someone who is typing into a form.
        if (a && (a.tagName === 'INPUT' || a.tagName === 'TEXTAREA' || a.tagName === 'SELECT')) return;
        openPopup();
      }, 4000);
    }
  }
  doc.querySelectorAll('[data-open-popup]').forEach(function (b) {
    b.addEventListener('click', function (e) {
      e.preventDefault();
      if (popup) openPopup(); else location.href = '/contact/';
    });
  });

  /* Lead forms: submit with fetch; without JS they post normally and redirect. */
  doc.querySelectorAll('form[data-lead-form]').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status'), btn = form.querySelector('button[type="submit"]');
      var phone = (form.phone.value || '').replace(/\D/g, '');
      if (phone.length < 10) { status.className = 'form-status err'; status.textContent = 'Please enter a valid phone number.'; form.phone.focus(); return; }
      btn.disabled = true; var label = btn.textContent; btn.textContent = 'Sending…';
      status.className = 'form-status'; status.textContent = '';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res && res.ok) {
            set(ls, 'slpa_lead_sent', '1');
            form.reset();
            status.className = 'form-status ok';
            status.textContent = 'Thank you! A Sugar Land public adjuster will contact you shortly. For urgent help call or text (832) 503-5866.';
            if (window.gtag) window.gtag('event', 'generate_lead', { form: form.source ? form.source.value : '' });
          } else {
            status.className = 'form-status err';
            status.textContent = (res && res.error) || 'Something went wrong. Please call or text (832) 503-5866.';
          }
        })
        .catch(function () {
          status.className = 'form-status err';
          status.textContent = 'Network error. Please call or text (832) 503-5866.';
        })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });

  /* Compact live-weather strip (homepage and storm pages). */
  var strip = doc.getElementById('wx-strip');
  if (strip && window.fetch) {
    var pt = '29.6197,-95.6349';
    var H = { 'Accept': 'application/geo+json' };
    Promise.all([
      fetch('https://api.weather.gov/stations/KSGR/observations/latest', { headers: H }).then(function (r) { return r.json(); }).catch(function () { return null; }),
      fetch('https://api.weather.gov/alerts/active?point=' + pt, { headers: H }).then(function (r) { return r.json(); }).catch(function () { return null; })
    ]).then(function (res) {
      var obs = res[0] && res[0].properties, al = res[1] && res[1].features || [];
      var out = [];
      if (obs && obs.temperature && obs.temperature.value !== null) {
        var f = Math.round(obs.temperature.value * 9 / 5 + 32);
        var w = obs.windSpeed && obs.windSpeed.value !== null ? Math.round(obs.windSpeed.value * 0.621371) + ' mph wind' : '';
        out.push('<span class="wx-pill">Sugar Land now: <strong>' + f + '°F</strong> ' + (obs.textDescription || '') + (w ? ' · ' + w : '') + '</span>');
      }
      if (al.length) {
        out.push('<span class="wx-pill alert">⚠ ' + al.length + ' active alert' + (al.length > 1 ? 's' : '') + ': ' + al.map(function (a) { return a.properties.event; }).slice(0, 2).join(', ') + '</span>');
      } else if (res[1]) {
        out.push('<span class="wx-pill">No active NWS alerts</span>');
      }
      var slot = strip.querySelector('[data-wx]');
      if (out.length && slot) slot.innerHTML = out.join(' ');
    });
  }
})();
