/* Houston Public Adjusters — nav, lead popup, form submission, site-wide weather alert strip. */
(function () {
  'use strict';
  var store = {
    get: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} },
    lget: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    lset: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  };

  // Mobile nav
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') { nav.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); } });
  }
  var header = document.querySelector('.site-header');
  window.addEventListener('scroll', function () { header && header.classList.toggle('scrolled', window.scrollY > 10); }, { passive: true });

  // Lead popup: opens 4 seconds after page load, once per browser session.
  var modal = document.getElementById('lead-modal');
  var lastFocus = null;
  function openModal() {
    if (!modal || !modal.hidden) return;
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    var first = modal.querySelector('input:not([type=hidden]):not([tabindex="-1"])');
    if (first) setTimeout(function () { first.focus(); }, 50);
    store.set('hpa_popup_seen', '1');
  }
  function closeModal() {
    if (!modal) return;
    modal.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  if (modal) {
    modal.querySelector('.lead-close').addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !modal.hidden) closeModal(); });
    if (!store.get('hpa_popup_seen') && !store.lget('hpa_lead_sent')) {
      setTimeout(function () {
        // Don't interrupt someone who is already typing in a form.
        var a = document.activeElement;
        if (a && /INPUT|TEXTAREA|SELECT/.test(a.tagName)) return;
        openModal();
      }, 4000);
    }
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-open-lead]') : null;
    if (!t) return;
    e.preventDefault();
    if (modal) openModal(); else location.href = '/contact/';
  });

  // Lead forms: AJAX submit to /submit-lead.php; falls back to a normal POST without JS.
  document.querySelectorAll('form.lead-form').forEach(function (form) {
    var src = form.querySelector('input[name=source]');
    if (src) src.value = location.pathname + ' [' + form.id + ']';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = form.querySelector('.form-status');
      var btn = form.querySelector('button[type=submit]');
      status.className = 'form-status';
      var name = form.name.value.trim(), phone = form.phone.value.trim(), email = form.email.value.trim();
      if (!name || (!phone && !email)) { status.textContent = 'Please add your name and a phone number or email.'; status.classList.add('err'); return; }
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { status.textContent = 'Please check your email address.'; status.classList.add('err'); return; }
      if (!form.consent.checked) { status.textContent = 'Please tick the box so we can contact you.'; status.classList.add('err'); return; }
      btn.disabled = true; btn.textContent = 'Sending…';
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (r) { return r.json().catch(function () { return { ok: false }; }); })
        .then(function (res) {
          if (res.ok) {
            store.lset('hpa_lead_sent', '1');
            form.classList.add('sent');
            status.textContent = 'Thank you! A licensed Houston public adjuster will contact you shortly. Need us now? Call or text (832) 503-5866.';
            status.classList.add('ok');
            if (window.gtag) window.gtag('event', 'generate_lead', { form_id: form.id });
          } else {
            throw new Error(res.error || 'failed');
          }
        })
        .catch(function (err) {
          btn.disabled = false; btn.textContent = 'Get My Free Claim Review';
          status.textContent = (err && err.message && err.message !== 'failed' ? err.message + ' ' : 'Something went wrong sending the form. ') + 'Please call or text (832) 503-5866.';
          status.classList.add('err');
        });
    });
  });

  // Site-wide alert strip: active NWS warnings for Harris County (cached 10 minutes per session).
  var strip = document.getElementById('alert-strip');
  function showAlerts(list) {
    if (!strip || !list.length) return;
    var a = list[0];
    strip.innerHTML = '<div class="wrap"><strong>&#9888; ' + esc(a.event) + '</strong><span>' + esc(a.headline || '') +
      (list.length > 1 ? ' (+' + (list.length - 1) + ' more)' : '') + '</span><a href="/houston-weather/">Live tracker &rarr;</a>' +
      '<a href="tel:+18325035866">Storm damage? Call (832) 503-5866</a></div>';
    strip.hidden = false;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  if (strip && window.fetch && !document.body.classList.contains('weather-page')) {
    var cached = store.get('hpa_alerts');
    var parsed = cached ? JSON.parse(cached) : null;
    if (parsed && Date.now() - parsed.t < 600000) { showAlerts(parsed.a); }
    else {
      fetch('https://api.weather.gov/alerts/active?zone=TXC201', { headers: { 'Accept': 'application/geo+json' } })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          var a = (d.features || []).map(function (f) { return f.properties; })
            .filter(function (p) { return /Warning|Watch/.test(p.event) && p.severity !== 'Minor'; })
            .map(function (p) { return { event: p.event, headline: p.headline }; });
          store.set('hpa_alerts', JSON.stringify({ t: Date.now(), a: a }));
          showAlerts(a);
        }).catch(function () {});
    }
  }
})();
