/* Live Houston weather from the National Weather Service API (api.weather.gov — free, no key, CORS enabled).
   Drives the homepage mini widget (#wx-mini) and the full tracker (#wx-app). */
(function () {
  'use strict';
  var API = 'https://api.weather.gov';
  var H = { headers: { 'Accept': 'application/geo+json' } };

  function j(url) { return fetch(url, H).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function f(c) { return c == null ? null : Math.round(c * 9 / 5 + 32); }
  function mph(v, unit) { if (v == null) return null; return Math.round(/km_h/.test(unit || '') ? v * 0.621371 : /m_s/.test(unit || '') ? v * 2.23694 : v); }
  function compass(d) { if (d == null) return ''; return ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'][Math.round(d / 22.5) % 16]; }
  function ago(iso) { var m = Math.round((Date.now() - new Date(iso)) / 60000); return m < 60 ? m + ' min ago' : Math.round(m / 60) + ' hr ago'; }
  function sevClass(p) { return /Extreme|Severe/.test(p.severity) ? '' : 'minor'; }

  function point(lat, lng) {
    var key = 'hpa_pt_' + lat + ',' + lng;
    try { var c = sessionStorage.getItem(key); if (c) return Promise.resolve(JSON.parse(c)); } catch (e) {}
    return j(API + '/points/' + lat + ',' + lng).then(function (d) {
      var p = { forecast: d.properties.forecast, stations: d.properties.observationStations, city: d.properties.relativeLocation && d.properties.relativeLocation.properties.city };
      try { sessionStorage.setItem(key, JSON.stringify(p)); } catch (e) {}
      return p;
    });
  }
  function observation(stationsUrl) {
    return j(stationsUrl).then(function (d) {
      var ids = (d.features || []).slice(0, 3).map(function (s) { return s.properties.stationIdentifier; });
      // Try the nearest stations in order until one has a recent temperature.
      return ids.reduce(function (pr, id) {
        return pr.then(function (found) {
          if (found) return found;
          return j(API + '/stations/' + id + '/observations/latest').then(function (o) {
            return o.properties.temperature.value != null ? { id: id, name: (d.features.find(function (s) { return s.properties.stationIdentifier === id; }) || { properties: {} }).properties.name, o: o.properties } : null;
          }).catch(function () { return null; });
        });
      }, Promise.resolve(null));
    });
  }
  function alerts(lat, lng) { return j(API + '/alerts/active?point=' + lat + ',' + lng).then(function (d) { return (d.features || []).map(function (x) { return x.properties; }); }); }

  /* ---------- Homepage mini widget ---------- */
  var mini = document.getElementById('wx-mini');
  if (mini) {
    var lat = mini.dataset.lat, lng = mini.dataset.lng;
    var set = function (k, html) { var el = mini.querySelector('[data-wx=' + k + ']'); if (el) el.innerHTML = html; };
    point(lat, lng).then(function (p) { return observation(p.stations); }).then(function (r) {
      if (!r) throw new Error('no obs');
      set('temp', f(r.o.temperature.value) + '&deg;F');
      set('cond', esc(r.o.textDescription || 'Current conditions'));
      var w = mph(r.o.windSpeed.value, r.o.windSpeed.unitCode);
      set('station', esc(r.name || r.id) + (w != null ? ' &middot; wind ' + compass(r.o.windDirection.value) + ' ' + w + ' mph' : '') + ' &middot; ' + ago(r.o.timestamp));
    }).catch(function () { set('cond', 'Live conditions unavailable right now'); set('station', ''); });
    alerts(lat, lng).then(function (list) {
      if (!list.length) { set('alerts', '<span class="pill green">No active NWS alerts for Houston</span>'); return; }
      set('alerts', list.slice(0, 3).map(function (a) { return '<span class="pill red">' + esc(a.event) + '</span> '; }).join('') +
        '<br><small>' + esc(list[0].headline || '') + '</small>');
    }).catch(function () { set('alerts', '<span class="pill">Alert feed unavailable &mdash; check weather.gov</span>'); });
  }

  /* ---------- Full tracker page ---------- */
  var app = document.getElementById('wx-app');
  if (!app) return;
  var sel = document.getElementById('wx-area');
  var out = {
    now: document.getElementById('wx-now'),
    alerts: document.getElementById('wx-alerts'),
    forecast: document.getElementById('wx-forecast'),
    updated: document.getElementById('wx-updated')
  };

  function load() {
    var opt = sel.options[sel.selectedIndex];
    var lat = opt.dataset.lat, lng = opt.dataset.lng, name = opt.textContent;
    try { localStorage.setItem('hpa_wx_area', sel.value); } catch (e) {}
    out.now.innerHTML = '<p class="skel">Loading current conditions for ' + esc(name) + '&hellip;</p>';
    out.alerts.innerHTML = '<p class="skel">Checking National Weather Service alerts&hellip;</p>';
    out.forecast.innerHTML = '<p class="skel">Loading 7-day forecast&hellip;</p>';

    alerts(lat, lng).then(function (list) {
      if (!list.length) { out.alerts.innerHTML = '<div class="wx-ok">&#10003; No active watches, warnings or advisories for ' + esc(name) + ' right now.</div>'; return; }
      out.alerts.innerHTML = list.map(function (a) {
        return '<div class="wx-alert ' + sevClass(a) + '"><h4>' + esc(a.event) + '</h4><p>' + esc(a.headline || '') + '</p>' +
          '<p><small>Severity: ' + esc(a.severity) + ' &middot; Until ' + (a.ends || a.expires ? new Date(a.ends || a.expires).toLocaleString([], { weekday: 'short', hour: 'numeric', minute: '2-digit' }) : 'further notice') + '</small></p>' +
          '<details><summary>Full alert text</summary>' + esc(a.description || '') + (a.instruction ? '\n\n' + esc(a.instruction) : '') + '</details></div>';
      }).join('');
    }).catch(function () { out.alerts.innerHTML = '<p>The alert feed is unavailable right now. Check <a href="https://www.weather.gov/hgx/" target="_blank" rel="noopener">weather.gov/hgx</a>.</p>'; });

    point(lat, lng).then(function (p) {
      observation(p.stations).then(function (r) {
        if (!r) throw new Error('no obs');
        var o = r.o;
        var w = mph(o.windSpeed.value, o.windSpeed.unitCode), g = mph(o.windGust.value, o.windGust.unitCode);
        var hi = o.heatIndex && o.heatIndex.value != null ? f(o.heatIndex.value) : null;
        var wc = o.windChill && o.windChill.value != null ? f(o.windChill.value) : null;
        out.now.innerHTML = '<h3>' + esc(name) + ' right now</h3><div class="wx-temp">' + f(o.temperature.value) + '&deg;F</div>' +
          '<p class="wx-cond">' + esc(o.textDescription || '') + '</p><div class="wx-meta">' +
          '<span>Feels like <b>' + (hi || wc || f(o.temperature.value)) + '&deg;F</b></span>' +
          '<span>Humidity <b>' + (o.relativeHumidity.value != null ? Math.round(o.relativeHumidity.value) + '%' : '&ndash;') + '</b></span>' +
          '<span>Wind <b>' + (w != null ? compass(o.windDirection.value) + ' ' + w + ' mph' : '&ndash;') + '</b></span>' +
          '<span>Gusts <b>' + (g != null ? g + ' mph' : '&ndash;') + '</b></span>' +
          '<span>Pressure <b>' + (o.barometricPressure.value ? (o.barometricPressure.value / 3386.39).toFixed(2) + ' inHg' : '&ndash;') + '</b></span>' +
          '<span>Dew point <b>' + (o.dewpoint.value != null ? f(o.dewpoint.value) + '&deg;F' : '&ndash;') + '</b></span>' +
          '</div><p style="margin:14px 0 0;font-size:.85rem">Station: ' + esc(r.name || r.id) + ' &middot; observed ' + ago(o.timestamp) + '</p>';
      }).catch(function () { out.now.innerHTML = '<p>Current observations are unavailable right now.</p>'; });

      j(p.forecast).then(function (d) {
        var periods = d.properties.periods.slice(0, 14);
        out.forecast.innerHTML = periods.map(function (x) {
          var rain = x.probabilityOfPrecipitation && x.probabilityOfPrecipitation.value;
          return '<div class="wx-day"><b>' + esc(x.name) + '</b><img src="' + esc(x.icon) + '" alt="" loading="lazy"><div class="t">' + x.temperature + '&deg;' + esc(x.temperatureUnit) + '</div>' +
            '<div>' + esc(x.shortForecast) + '</div>' + (rain ? '<div class="p">' + rain + '% rain</div>' : '') +
            '<div><small>Wind ' + esc(x.windSpeed) + ' ' + esc(x.windDirection) + '</small></div></div>';
        }).join('');
      }).catch(function () { out.forecast.innerHTML = '<p>The forecast is unavailable right now.</p>'; });
    }).catch(function () {
      out.now.innerHTML = '<p>Weather data is unavailable right now. Try again in a minute.</p>';
      out.forecast.innerHTML = '';
    });

    out.updated.textContent = 'Updated ' + new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
    // Refresh the animated radar and outlook images too.
    document.querySelectorAll('[data-refresh]').forEach(function (img) { img.src = img.dataset.refresh + '?t=' + Date.now(); });
  }

  try { var saved = localStorage.getItem('hpa_wx_area'); if (saved && sel.querySelector('option[value="' + saved + '"]')) sel.value = saved; } catch (e) {}
  sel.addEventListener('change', load);
  document.getElementById('wx-refresh').addEventListener('click', load);
  load();
  setInterval(load, 10 * 60 * 1000);
})();
