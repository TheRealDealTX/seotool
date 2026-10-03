/* Temple Roofers — live weather widget (data from /api/weather/, server-cached). */
(function () {
  'use strict';
  var roots = document.querySelectorAll('[data-weather]');
  if (!roots.length) return;
  var TZ = 'America/Chicago';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function icon(name, cls) {
    return '<svg class="icon ' + (cls || '') + '" aria-hidden="true" focusable="false"><use href="#i-' + esc(name) + '"></use></svg>';
  }
  function num(v, suffix) {
    return (v === null || v === undefined || v === '') ? '—' : esc(v) + (suffix || '');
  }
  // "2026-10-03T06:45" (already Central Time) -> "6:45 AM CT"
  function localClock(s) {
    var m = /T(\d{2}):(\d{2})/.exec(s || '');
    if (!m) return '';
    var h = parseInt(m[1], 10), ap = h >= 12 ? 'PM' : 'AM';
    h = h % 12 || 12;
    return h + ':' + m[2] + ' ' + ap + ' CT';
  }
  function fmtStamp(iso) {
    if (!iso) return '';
    try {
      return new Date(iso).toLocaleString('en-US', { timeZone: TZ, weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' }) + ' CT';
    } catch (e) { return iso; }
  }
  function dayParts(dateStr) {
    var p = dateStr.split('-');
    var d = new Date(+p[0], +p[1] - 1, +p[2]);
    return {
      name: d.toLocaleDateString('en-US', { weekday: 'short' }),
      long: d.toLocaleDateString('en-US', { weekday: 'long' }),
      date: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    };
  }
  function riskLabel(l) { return l === 'high' ? 'High' : l === 'elevated' ? 'Elevated' : 'Low'; }

  function alertsHtml(al, compact) {
    if (!al || al.status === 'unavailable') {
      return compact ? '' : '<div class="wx-status wx-status--error">' + icon('alert') + ' National Weather Service alerts could not be retrieved right now. Check <a href="https://www.weather.gov/fwd/" rel="noopener">weather.gov</a> for official alerts.</div>';
    }
    var items = al.items || [];
    if (compact) {
      if (!items.length) return '';
      return '<a class="wx-alert-chip" href="/weather/">' + icon('alert') + ' ' + items.length + ' active NWS alert' + (items.length > 1 ? 's' : '') + ': ' + esc(items[0].event) + '</a>';
    }
    var stamp = al.status === 'cached' ? ' (cached ' + esc(fmtStamp(al.fetched_at)) + ')' : ' as of ' + esc(fmtStamp(al.fetched_at));
    if (!items.length) {
      return '<div class="wx-noalerts">' + icon('shield') + ' No active National Weather Service alerts for Temple' + stamp + '.</div>';
    }
    return items.map(function (a) {
      var sev = (a.severity || '').toLowerCase();
      return '<article class="wx-alert wx-alert--' + esc(sev) + '">' +
        '<div class="wx-alert__head">' + icon('alert') + '<div><h2 class="wx-alert__title">' + esc(a.event) + '</h2><div>' + esc(a.headline) + '</div></div></div>' +
        '<div class="wx-alert__body"><div class="wx-alert__meta">' +
        '<span><strong>Severity:</strong> ' + esc(a.severity) + '</span>' +
        (a.urgency ? '<span><strong>Urgency:</strong> ' + esc(a.urgency) + '</span>' : '') +
        (a.effective ? '<span><strong>Effective:</strong> ' + esc(fmtStamp(a.effective)) + '</span>' : '') +
        (a.ends ? '<span><strong>Until:</strong> ' + esc(fmtStamp(a.ends)) + '</span>' : '') +
        '</div>' +
        (a.area ? '<p><strong>Areas:</strong> ' + esc(a.area) + '</p>' : '') +
        (a.description ? '<div class="wx-alert__desc">' + esc(a.description) + '</div>' : '') +
        (a.instruction ? '<p><strong>What to do:</strong> ' + esc(a.instruction) + '</p>' : '') +
        '<p>Issued by ' + esc(a.sender) + '. ' + (a.url ? '<a href="' + esc(a.url) + '" rel="noopener">View the official alert</a>' : '') + '</p>' +
        '</div></article>';
    }).join('') + '<p class="wx-attrib">Alerts' + stamp + '. Always follow official NWS guidance.</p>';
  }

  function renderCompact(root, data) {
    var fc = data.forecast || {};
    if (fc.status === 'unavailable' || !fc.current) {
      root.innerHTML = '<div class="wx-error">' + icon('cloud') + ' Live Temple weather is temporarily unavailable. <a href="/weather/">Try the weather page</a> or the <a href="' + esc(data.links.nws) + '" rel="noopener">NWS forecast</a>.</div>';
      return;
    }
    var c = fc.current;
    var days = (fc.days || []).slice(0, 4);
    var cachedNote = fc.status === 'cached' ? '<p class="wx-foot"><strong>Showing cached data from ' + esc(fmtStamp(fc.fetched_at)) + '</strong> — live data is temporarily unavailable.</p>' : '';
    root.innerHTML = alertsHtml(data.alerts, true) +
      '<div class="wx-card">' +
      '<div class="wx-card__top">' + icon(c.icon, 'wx-card__icon') +
      '<div><div class="wx-card__temp">' + num(c.temp, '°F') + '</div></div>' +
      '<div><div class="wx-card__label">' + esc(c.label) + '</div><div class="wx-card__feels">Feels like ' + num(c.feels, '°F') + ' · Temple, TX</div></div></div>' +
      '<div class="wx-meta"><span>' + icon('wind') + ' Wind ' + num(c.wind, ' mph') + ' ' + esc(c.wind_dir) + '</span><span>' + icon('gauge') + ' Gusts ' + num(c.gust, ' mph') + '</span><span>' + icon('droplets') + ' Humidity ' + num(c.humidity, '%') + '</span></div>' +
      '<div class="wx-mini-days">' + days.map(function (d) {
        var p = dayParts(d.date);
        return '<div class="wx-mini-day"><strong>' + esc(p.name) + '</strong>' + icon(d.icon) + '<div>' + num(d.hi, '°') + ' / ' + num(d.lo, '°') + '</div><div>' + icon('umbrella') + ' ' + num(d.pop, '%') + '</div></div>';
      }).join('') + '</div>' +
      cachedNote +
      '<p class="wx-foot">Observed ' + esc(localClock(c.time)) + '. Data: <a href="https://open-meteo.com/" rel="noopener">Open-Meteo</a> &amp; NWS.</p>' +
      '</div>';
  }

  function renderFull(root, data) {
    var fc = data.forecast || {};
    var status = root.querySelector('[data-wx-status]');
    var alertsEl = root.querySelector('[data-wx-alerts]');
    var curEl = root.querySelector('[data-wx-current]');
    var riskEl = root.querySelector('[data-wx-risk]');
    var daysEl = root.querySelector('[data-wx-days]');
    var updEl = root.querySelector('[data-wx-updated]');

    alertsEl.innerHTML = alertsHtml(data.alerts, false);

    if (fc.status === 'cached') {
      status.className = 'wx-status wx-status--cached';
      status.innerHTML = icon('clock') + ' Live forecast data is temporarily unavailable. Showing the most recent cached data, retrieved ' + esc(fmtStamp(fc.fetched_at)) + '. This is not live data.';
      status.hidden = false;
    } else if (fc.status === 'unavailable' || !fc.current) {
      status.className = 'wx-status wx-status--error';
      status.innerHTML = icon('alert') + ' Live Temple weather is temporarily unavailable. Please try again shortly or view the <a href="' + esc(data.links.nws) + '" rel="noopener">National Weather Service forecast for Temple</a>.';
      status.hidden = false;
      curEl.innerHTML = '<div class="wx-error">Current conditions are unavailable right now.</div>';
      daysEl.innerHTML = '<div class="wx-error">The 7-day forecast is unavailable right now.</div>';
      riskEl.innerHTML = '';
      return;
    } else {
      status.hidden = true;
    }

    var c = fc.current;
    curEl.innerHTML =
      '<div class="wx-now__head"><div class="wx-now__main">' + icon(c.icon, 'wx-now__icon') +
      '<div><div class="wx-now__temp">' + num(c.temp, '°F') + '</div></div>' +
      '<div><p class="wx-now__label">' + esc(c.label) + '</p><p class="wx-now__feels">Feels like ' + num(c.feels, '°F') + '</p></div></div>' +
      '<div class="wx-now__time">Temple, TX<br>Observed ' + esc(localClock(c.time)) + '<br>Updated ' + esc(fmtStamp(fc.fetched_at)) + '</div></div>' +
      '<div class="wx-stats">' +
      '<div class="wx-stat"><small>' + icon('droplets') + ' Humidity</small><strong>' + num(c.humidity, '%') + '</strong></div>' +
      '<div class="wx-stat"><small>' + icon('wind') + ' Wind speed</small><strong>' + num(c.wind, ' mph') + ' ' + esc(c.wind_dir) + '</strong></div>' +
      '<div class="wx-stat"><small>' + icon('gauge') + ' Wind gusts</small><strong>' + num(c.gust, ' mph') + '</strong></div>' +
      '<div class="wx-stat"><small>' + icon('umbrella') + ' Precip. chance</small><strong>' + num(c.pop, '%') + '</strong></div>' +
      '<div class="wx-stat"><small>' + icon('sun') + ' UV index</small><strong>' + num(c.uv) + '</strong></div>' +
      '<div class="wx-stat"><small>' + icon('cloud-rain') + ' Precip. now</small><strong>' + num(c.precip, ' in') + '</strong></div>' +
      '</div>';

    var days = fc.days || [];
    var today = days[0];
    var upcoming = days.slice(1).filter(function (d) { return d.risk && d.risk.level !== 'low'; });
    if (today) {
      var lv = today.risk ? today.risk.level : 'low';
      riskEl.innerHTML = '<h2 class="wx-risk__title">' + icon('home') + ' Roof-weather indicator</h2>' +
        '<p>Today: <span class="risk-pill risk--' + esc(lv) + '">' + riskLabel(lv) + '</span></p>' +
        (today.risk && today.risk.reasons.length ? '<ul>' + today.risk.reasons.map(function (r) { return '<li>' + esc(r) + '</li>'; }).join('') + '</ul>' : '<p>No wind, storm, heavy-rain or extreme-heat triggers in today\'s forecast.</p>') +
        (upcoming.length ? '<p><strong>Watch later this week:</strong> ' + upcoming.map(function (d) { return esc(dayParts(d.date).long) + ' (' + riskLabel(d.risk.level) + ')'; }).join(', ') + '</p>' : '<p>No elevated roof-weather days in the rest of the 7-day forecast.</p>') +
        '<p class="wx-risk__note">Informational only — not an official alert. Rules: High = gusts ≥ 58 mph or thunderstorms with hail; Elevated = gusts 40–57 mph, thunderstorms, ≥ 1.5 in of rain or highs ≥ 100°F.</p>';
    }

    daysEl.innerHTML = days.map(function (d, i) {
      var p = dayParts(d.date);
      var lv = d.risk ? d.risk.level : 'low';
      return '<article class="wx-day' + (i === 0 ? ' wx-day--today' : '') + '">' +
        (d.storm ? '<span class="wx-day__storm" title="Thunderstorms possible">' + icon('cloud-lightning') + '<span class="sr-only">Thunderstorms possible</span></span>' : '') +
        '<span class="wx-day__name">' + (i === 0 ? 'Today' : esc(p.name)) + '</span>' +
        '<span class="wx-day__date">' + esc(p.date) + '</span>' +
        icon(d.icon, 'wx-day__icon') +
        '<span class="wx-day__label">' + esc(d.label) + '</span>' +
        '<span class="wx-day__temps">' + num(d.hi, '°') + ' <span>/ ' + num(d.lo, '°F') + '</span></span>' +
        '<dl><dt>Rain chance</dt><dd>' + num(d.pop, '%') + '</dd>' +
        '<dt>Rain total</dt><dd>' + num(d.rain, ' in') + '</dd>' +
        '<dt>Wind</dt><dd>' + num(d.wind, ' mph') + '</dd>' +
        '<dt>Max gusts</dt><dd>' + num(d.gust, ' mph') + '</dd>' +
        '<dt>UV max</dt><dd>' + num(d.uv) + '</dd>' +
        '<dt>Storms</dt><dd>' + (d.storm ? 'Possible' : 'Not expected') + '</dd></dl>' +
        '<span class="risk-pill risk--' + esc(lv) + '">Roof risk: ' + riskLabel(lv) + '</span>' +
        '</article>';
    }).join('');
    if (updEl) updEl.textContent = 'Forecast retrieved ' + fmtStamp(fc.fetched_at) + '.';
  }

  function load() {
    fetch('/api/weather/', { headers: { 'Accept': 'application/json' }, cache: 'no-store' })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (data) {
        roots.forEach(function (root) {
          if (root.getAttribute('data-weather') === 'full') renderFull(root, data);
          else renderCompact(root, data);
        });
      })
      .catch(function () {
        roots.forEach(function (root) {
          var msg = '<div class="wx-error">Live Temple weather could not be loaded. Please refresh the page or check the <a href="https://forecast.weather.gov/MapClick.php?lat=31.0982&amp;lon=-97.3428" rel="noopener">National Weather Service forecast</a>.</div>';
          if (root.getAttribute('data-weather') === 'full') {
            root.querySelector('[data-wx-current]').innerHTML = msg;
            root.querySelector('[data-wx-alerts]').innerHTML = '';
            root.querySelector('[data-wx-days]').innerHTML = '';
          } else {
            root.innerHTML = msg;
          }
        });
      });
  }
  load();
  setInterval(function () { if (!document.hidden) load(); }, 10 * 60 * 1000);
})();
