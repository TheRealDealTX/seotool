/* Live Texas weather: NWS forecast + active alerts + last-24h storm reports */
(function () {
  'use strict';
  var root = document.querySelector('[data-weather]');
  if (!root || !window.fetch) return;
  var KEY = 'txpa-wx-city';
  var RELEVANT = /tornado|severe thunderstorm|hail|flash flood|flood warning|flood watch|hurricane|tropical storm|storm surge|high wind|extreme wind|winter storm|ice storm|blizzard|hard freeze|freeze warning|wind advisory|fire weather|red flag/i;
  var STORMY = /thunder|storm|hail|tornado|hurricane|tropical|severe/i;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var get = function (url) { return fetch(url, { headers: { Accept: 'application/geo+json' } }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }); };

  // Forecast
  var sel = root.querySelector('[data-wx-city]');
  var box = root.querySelector('[data-wx-forecast]');
  try { var saved = localStorage.getItem(KEY); if (saved && sel.querySelector('option[value="' + saved + '"]')) sel.value = saved; } catch (e) {}

  function forecast(latlng, label) {
    box.innerHTML = '<p class="wx__muted">Loading forecast…</p>';
    get('https://api.weather.gov/points/' + latlng).then(function (pt) {
      var place = label || (pt.properties.relativeLocation && pt.properties.relativeLocation.properties.city) || '';
      return get(pt.properties.forecast).then(function (fc) { render(fc.properties.periods || [], place); });
    }).catch(function () {
      box.innerHTML = '<p class="wx__muted">The forecast service is not responding right now. See <a href="https://www.weather.gov/" target="_blank" rel="noopener" style="color:#fff">weather.gov</a>.</p>';
    });
  }
  function render(periods, place) {
    if (!periods.length) { box.innerHTML = '<p class="wx__muted">No forecast available.</p>'; return; }
    var now = periods[0];
    var html = '<div class="wx__now"><img src="' + esc(now.icon) + '" alt="" width="76" height="76"><div>' +
      '<div class="wx__temp">' + esc(now.temperature) + '<small>°' + esc(now.temperatureUnit) + '</small></div>' +
      '<p class="wx__desc">' + esc(now.name) + ': ' + esc(now.shortForecast) + '</p>' +
      '<p class="wx__meta">' + esc(place) + ' · Wind ' + esc(now.windSpeed) + ' ' + esc(now.windDirection) +
      (now.probabilityOfPrecipitation && now.probabilityOfPrecipitation.value != null ? ' · Rain ' + now.probabilityOfPrecipitation.value + '%' : '') + '</p></div></div>';
    html += '<div class="wx__periods">' + periods.slice(1, 7).map(function (p) {
      return '<div class="wx__p' + (STORMY.test(p.shortForecast) ? ' is-storm' : '') + '" title="' + esc(p.detailedForecast) + '">' + esc(p.name.replace(' Night', ' night').replace('This ', '')) +
        '<img src="' + esc(p.icon) + '" alt="" width="40" height="40" loading="lazy"><strong>' + esc(p.temperature) + '°</strong>' + esc(p.shortForecast.split(' then ')[0]) + '</div>';
    }).join('') + '</div>';
    box.innerHTML = html;
  }
  sel.addEventListener('change', function () {
    try { localStorage.setItem(KEY, sel.value); } catch (e) {}
    forecast(sel.value, sel.options[sel.selectedIndex].text);
  });
  var geo = root.querySelector('[data-wx-geo]');
  if (geo && navigator.geolocation) {
    geo.addEventListener('click', function () {
      navigator.geolocation.getCurrentPosition(function (pos) {
        forecast(pos.coords.latitude.toFixed(4) + ',' + pos.coords.longitude.toFixed(4));
      }, function () { box.insertAdjacentHTML('afterbegin', '<p class="wx__muted">Location unavailable; showing the selected city.</p>'); });
    });
  } else if (geo) { geo.hidden = true; }

  // Alerts
  var alertsBox = root.querySelector('[data-wx-alerts]');
  var countEl = root.querySelector('[data-wx-count]');
  get('https://api.weather.gov/alerts/active?area=TX').then(function (d) {
    var all = (d.features || []).map(function (f) { return f.properties; });
    var rel = all.filter(function (a) { return RELEVANT.test(a.event); });
    var order = { Extreme: 0, Severe: 1, Moderate: 2, Minor: 3, Unknown: 4 };
    rel.sort(function (a, b) { return (order[a.severity] || 4) - (order[b.severity] || 4); });
    countEl.textContent = rel.length + ' storm-related · ' + all.length + ' total';
    if (!rel.length) {
      alertsBox.innerHTML = '<div class="wx__ok"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg><div><strong>No storm, flood or wind alerts in Texas right now.</strong><br>A good time to photograph your roof and property, so you have a "before" record for the next storm.</div></div>';
      return;
    }
    alertsBox.innerHTML = rel.slice(0, 12).map(function (a) {
      var cls = a.severity === 'Extreme' || a.severity === 'Severe' ? ' is-severe' : a.severity === 'Minor' ? ' is-minor' : '';
      var until = a.expires || a.ends;
      var areas = (a.areaDesc || '').split(';').map(function (x) { return x.trim(); });
      // Alerts can span state lines; keep only the Texas zones when the zone codes line up with the names.
      var ugc = (a.geocode && a.geocode.UGC) || [];
      if (ugc.length === areas.length) areas = areas.filter(function (x, i) { return ugc[i].indexOf('TX') === 0; });
      return '<a class="wx__alert' + cls + '" href="https://alerts.weather.gov/search?area=TX" target="_blank" rel="noopener"><strong>' + esc(a.event) + '</strong>' +
        esc(areas.slice(0, 4).join(', ') + (areas.length > 4 ? ' +' + (areas.length - 4) + ' more' : '')) +
        (until ? '<br><small>Until ' + esc(new Date(until).toLocaleString('en-US', { timeZone: 'America/Chicago', weekday: 'short', hour: 'numeric', minute: '2-digit' })) + ' CT · ' + esc(a.senderName || '') + '</small>' : '') + '</a>';
    }).join('');
  }).catch(function () {
    countEl.textContent = '';
    alertsBox.innerHTML = '<p class="wx__muted">Alerts are unavailable right now. Check <a href="https://alerts.weather.gov/search?area=TX" target="_blank" rel="noopener" style="color:#fff">alerts.weather.gov</a>.</p>';
  });

  // Last 24 hours of Texas storm reports
  var strip = root.querySelector('[data-wx-reports]');
  var end = new Date(), start = new Date(end.getTime() - 86400000);
  fetch('https://mesonet.agron.iastate.edu/geojson/lsr.geojson?states=TX&sts=' + start.toISOString().slice(0, 16) + 'Z&ets=' + end.toISOString().slice(0, 16) + 'Z')
    .then(function (r) { return r.json(); }).then(function (d) {
      var f = (d.features || []).map(function (x) { return x.properties; });
      var hail = f.filter(function (p) { return p.type === 'H'; });
      var wind = f.filter(function (p) { return p.type === 'G' || p.type === 'D' || p.type === 'N' || p.type === 'O'; });
      var torn = f.filter(function (p) { return p.type === 'T'; });
      var maxHail = hail.reduce(function (m, p) { return Math.max(m, parseFloat(p.magnitude) || 0); }, 0);
      strip.innerHTML = '<div><span>' + hail.length + '</span><p>hail reports in Texas, last 24 hours</p></div>' +
        '<div><span>' + (maxHail ? maxHail.toFixed(2) + '"' : '–') + '</span><p>largest hail reported' + (maxHail ? ' (' + esc(hail.filter(function (p) { return parseFloat(p.magnitude) === maxHail; })[0].city) + ')' : '') + '</p></div>' +
        '<div><span>' + wind.length + '</span><p>damaging wind and gust reports</p></div>' +
        '<div><span>' + torn.length + '</span><p>tornado reports</p></div>';
    }).catch(function () { strip.hidden = true; });

  // Start once the section is near the viewport (saves API calls for visitors who never scroll).
  var started = false;
  function startForecast() { if (started) return; started = true; forecast(sel.value, sel.options[sel.selectedIndex].text); }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { startForecast(); io.disconnect(); } }, { rootMargin: '400px' });
    io.observe(root);
  } else { startForecast(); }
})();
