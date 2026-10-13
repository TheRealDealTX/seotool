/* Live Sugar Land weather from the National Weather Service and NOAA (all public, CORS-enabled APIs). */
(function () {
  'use strict';
  var root = document.getElementById('wx');
  if (!root || !window.fetch) return;
  var LAT = root.getAttribute('data-lat'), LNG = root.getAttribute('data-lng');
  var H = { headers: { 'Accept': 'application/geo+json' } };
  var q = function (k) { return document.querySelector('[data-wx="' + k + '"]'); };
  var set = function (k, v) { var el = q(k); if (el) el.innerHTML = v; };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var cToF = function (c) { return c == null ? null : Math.round(c * 9 / 5 + 32); };
  var kmhToMph = function (k) { return k == null ? null : Math.round(k * 0.621371); };
  var deg = function (d) { return d == null ? '' : ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'][Math.round(d / 22.5) % 16]; };
  var time = function (iso) { return new Date(iso).toLocaleString('en-US', { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZone: 'America/Chicago' }); };
  var get = function (url) { return fetch(url, H).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }); };

  function current() {
    get('https://api.weather.gov/stations/KSGR/observations/latest').then(function (d) {
      var p = d.properties, v = function (o) { return o && o.value; };
      var t = cToF(v(p.temperature));
      var feels = cToF(v(p.heatIndex) != null ? v(p.heatIndex) : v(p.windChill));
      set('temp', t != null ? t + '°F' : '--');
      set('cond', esc(p.textDescription || '—'));
      set('feels', (feels != null ? feels : t != null ? t : '--') + '°F');
      set('hum', v(p.relativeHumidity) != null ? Math.round(v(p.relativeHumidity)) + '%' : '--');
      var w = kmhToMph(v(p.windSpeed));
      set('wind', w != null ? (w === 0 ? 'Calm' : deg(v(p.windDirection)) + ' ' + w + ' mph') : '--');
      var g = kmhToMph(v(p.windGust));
      set('gust', g != null ? g + ' mph' : 'None');
      var pr = v(p.barometricPressure);
      set('pres', pr != null ? (pr / 3386.39).toFixed(2) + ' inHg' : '--');
      var dw = cToF(v(p.dewpoint));
      set('dew', dw != null ? dw + '°F' : '--');
      set('updated', 'Observed ' + time(p.timestamp) + ' CT · National Weather Service');
    }).catch(function () { set('cond', 'Current conditions are temporarily unavailable. <a href="https://forecast.weather.gov/MapClick.php?lat=' + LAT + '&lon=' + LNG + '" target="_blank" rel="noopener" style="color:#fff">View on weather.gov</a>'); });
  }

  function alerts() {
    get('https://api.weather.gov/alerts/active?point=' + LAT + ',' + LNG).then(function (d) {
      var f = d.features || [];
      if (!f.length) { set('alerts', '<div class="wx-ok">✓ No active watches, warnings or advisories for Sugar Land right now.</div>'); return; }
      set('alerts', f.map(function (a) {
        var p = a.properties, minor = /Minor|Unknown/.test(p.severity) || /Advisory|Statement/.test(p.event);
        return '<div class="wx-alert' + (minor ? ' minor' : '') + '"><h3>⚠ ' + esc(p.event) + '</h3>' +
          '<p>' + esc(p.headline || '') + '</p>' +
          '<p class="small">Until ' + (p.ends || p.expires ? time(p.ends || p.expires) : 'further notice') + ' · ' + esc(p.senderName || 'NWS') + '</p>' +
          '<details><summary>Details &amp; instructions</summary><p style="white-space:pre-line">' + esc(p.description || '') + '</p>' +
          (p.instruction ? '<p style="white-space:pre-line"><strong>What to do:</strong> ' + esc(p.instruction) + '</p>' : '') + '</details></div>';
      }).join(''));
    }).catch(function () { set('alerts', '<div class="wx-alert minor"><p>Alerts are temporarily unavailable. Check <a href="https://alerts.weather.gov/" target="_blank" rel="noopener">alerts.weather.gov</a>.</p></div>'); });
  }

  function forecast() {
    get('https://api.weather.gov/points/' + LAT + ',' + LNG).then(function (pt) {
      return get(pt.properties.forecast);
    }).then(function (fc) {
      var per = fc.properties.periods, days = [], i = 0;
      while (i < per.length && days.length < 7) {
        var a = per[i], b = per[i + 1];
        if (a.isDaytime) { days.push({ name: a.name, hi: a.temperature, lo: b && !b.isDaytime ? b.temperature : null, icon: a.icon, short: a.shortForecast, pop: a.probabilityOfPrecipitation && a.probabilityOfPrecipitation.value, wind: a.windSpeed }); i += 2; }
        else { days.push({ name: a.name, hi: null, lo: a.temperature, icon: a.icon, short: a.shortForecast, pop: a.probabilityOfPrecipitation && a.probabilityOfPrecipitation.value, wind: a.windSpeed }); i += 1; }
      }
      set('forecast', days.map(function (d) {
        return '<div class="wx-day"><strong>' + esc(d.name) + '</strong><img src="' + esc(d.icon) + '" alt="" width="56" height="56" loading="lazy">' +
          '<div><span class="hi">' + (d.hi != null ? d.hi + '°' : '') + '</span>' + (d.lo != null ? ' <span class="muted">' + d.lo + '°</span>' : '') + '</div>' +
          '<div class="small">' + esc(d.short) + '</div>' + (d.pop ? '<div class="pop">💧 ' + d.pop + '%</div>' : '') + '<div class="small muted">' + esc(d.wind) + '</div></div>';
      }).join(''));
      set('fcupdated', 'NWS forecast issued ' + time(fc.properties.updateTime || fc.properties.generatedAt) + ' CT');
    }).catch(function () { set('forecast', '<div class="wx-day">Forecast temporarily unavailable. <a href="https://forecast.weather.gov/MapClick.php?lat=' + LAT + '&lon=' + LNG + '" target="_blank" rel="noopener">weather.gov</a></div>'); });
  }

  function river() {
    fetch('https://api.water.noaa.gov/nwps/v1/gauges/RMOT2').then(function (r) { return r.json(); }).then(function (g) {
      var o = g.status && g.status.observed, fc = g.status && g.status.forecast;
      if (!o || o.primary == null || o.primary < -100) throw new Error('no obs');
      var cat = { no_flooding: 'No flooding', action: 'Action stage', minor: 'Minor flooding', moderate: 'Moderate flooding', major: 'Major flooding' }[o.floodCategory] || o.floodCategory || '';
      set('rstage', o.primary.toFixed(2) + ' ft');
      set('rcat', esc(cat) + ' · ' + time(o.validTime) + ' CT');
      var m = q('rmarker'); if (m) m.style.left = Math.max(0, Math.min(100, o.primary / 60 * 100)) + '%';
      var txt = 'Flood stage (minor) is 45 ft; major is 50 ft. Record crest: 55.19 ft during Hurricane Harvey (Sept. 1, 2017).';
      if (fc && fc.primary != null && fc.primary > -100) txt = 'Forecast: ' + fc.primary.toFixed(1) + ' ft by ' + time(fc.validTime) + ' CT. ' + txt;
      set('rmeta', txt);
    }).catch(function () { set('rcat', 'Live reading unavailable—see NOAA.'); });
  }

  function season() {
    var now = new Date(), y = now.getFullYear(), start = new Date(y, 5, 1), end = new Date(y, 10, 30, 23, 59);
    var txt;
    if (now >= start && now <= end) txt = 'Hurricane season is underway — ' + Math.ceil((end - now) / 864e5) + ' days left (ends Nov. 30).';
    else { var next = now < start ? start : new Date(y + 1, 5, 1); txt = 'Next hurricane season starts in ' + Math.ceil((next - now) / 864e5) + ' days (June 1).'; }
    set('season', txt);
  }

  function refreshImages() {
    document.querySelectorAll('img[data-refresh]').forEach(function (img) {
      var base = img.src.split('?')[0]; img.src = base + '?t=' + Date.now();
    });
  }

  function all() { current(); alerts(); forecast(); river(); }
  all(); season();
  setInterval(function () { all(); refreshImages(); }, 10 * 60 * 1000);
})();
