/* Storm report lookup: NWS Local Storm Reports (IEM GeoJSON API) filtered by distance */
(function () {
  'use strict';
  var root = document.querySelector('[data-storm]');
  if (!root) return;
  var $ = function (s) { return root.querySelector(s); };
  var places = [], byName = {}, mode = 'day';
  var HAIL = [[4.5, 'softball'], [4, 'grapefruit'], [3, 'teacup'], [2.75, 'baseball'], [2.5, 'tennis ball'], [2, 'hen egg'], [1.75, 'golf ball'], [1.5, 'ping pong ball'], [1.25, 'half dollar'], [1, 'quarter'], [0.88, 'nickel'], [0.75, 'penny']];
  var TYPES = { H: 'Hail', G: 'Thunderstorm wind gust', D: 'Thunderstorm wind damage', T: 'Tornado', N: 'Non-thunderstorm wind gust', O: 'Non-thunderstorm wind damage' };

  fetch('/assets/data/tx-places.json').then(function (r) { return r.json(); }).then(function (list) {
    places = list;
    var dl = document.getElementById('tx-places');
    dl.innerHTML = list.map(function (p) { byName[p[0].toLowerCase()] = p; return '<option value="' + p[0].replace(/"/g, '') + '">'; }).join('');
  });

  var today = new Date();
  function iso(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  $('[data-in="d1"]').value = iso(new Date(today.getFullYear(), today.getMonth(), today.getDate() - 7));
  $('[data-in="d2"]').value = iso(today);

  $('[data-seg="range"]').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    this.querySelectorAll('button').forEach(function (x) { x.classList.toggle('is-on', x === b); });
    mode = b.getAttribute('data-v');
    root.querySelectorAll('[data-r]').forEach(function (el) { el.hidden = el.getAttribute('data-r').split(' ').indexOf(mode) < 0; });
  });

  function miles(a, b, c, d) {
    var R = 3958.8, toR = Math.PI / 180, dLat = (c - a) * toR, dLon = (d - b) * toR;
    var x = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a * toR) * Math.cos(c * toR) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 2 * R * Math.asin(Math.sqrt(x));
  }
  function hailName(sz) { for (var i = 0; i < HAIL.length; i++) if (sz >= HAIL[i][0] - 0.01) return HAIL[i][1]; return 'small hail'; }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function setStatus(t) { $('[data-out="status"]').textContent = t; }

  function links(start, end) {
    var out = [], d = new Date(start), n = 0;
    while (d <= end && n < 3) {
      var yy = String(d.getFullYear()).slice(2), mm = String(d.getMonth() + 1).padStart(2, '0'), dd = String(d.getDate()).padStart(2, '0');
      out.push('<a href="https://www.spc.noaa.gov/climo/reports/' + yy + mm + dd + '_rpts.html" target="_blank" rel="noopener"><span>NOAA Storm Prediction Center reports for ' + d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) + '<small>Nationwide map and list; each day runs from 12Z to 12Z (6 or 7 a.m. Central)</small></span><span>↗</span></a>');
      d.setDate(d.getDate() + 1); n++;
    }
    var p = function (x) { return String(x).padStart(2, '0'); };
    out.push('<a href="https://www.ncei.noaa.gov/stormevents/listevents.jsp?eventType=ALL&beginDate_mm=' + p(start.getMonth() + 1) + '&beginDate_dd=' + p(start.getDate()) + '&beginDate_yyyy=' + start.getFullYear() + '&endDate_mm=' + p(end.getMonth() + 1) + '&endDate_dd=' + p(end.getDate()) + '&endDate_yyyy=' + end.getFullYear() + '&county=ALL&hailfilter=0.00&tornfilter=0&windfilter=000&sort=DT&submitbutton=Search&statefips=48%2CTEXAS" target="_blank" rel="noopener"><span>NCEI Storm Events Database (Texas)<small>Official verified records, published a few months after the event</small></span><span>↗</span></a>');
    $('[data-out="links"]').innerHTML = out.join('');
  }

  function go() {
    var name = ($('[data-in="city"]').value || '').trim().toLowerCase();
    var place = byName[name];
    if (!place) { setStatus('Pick a Texas city or town from the list.'); return; }
    var start, end;
    if (mode === 'year') { end = new Date(); start = new Date(end.getFullYear() - 1, end.getMonth(), end.getDate()); }
    else {
      start = new Date($('[data-in="d1"]').value + 'T00:00:00');
      end = mode === 'span' ? new Date($('[data-in="d2"]').value + 'T00:00:00') : new Date(start);
      if (isNaN(start) || isNaN(end) || end < start) { setStatus('Check the dates.'); return; }
      if ((end - start) / 86400000 > 400) { setStatus('Please search 13 months or less at a time.'); return; }
    }
    var endPlus = new Date(end); endPlus.setDate(endPlus.getDate() + 1);
    var radius = +$('[data-in="radius"]').value, types = $('[data-in="types"]').value;
    var allowed = types === 'hailonly' ? 'H' : types === 'all' ? 'HGDTNO' : 'HGDNO';
    setStatus('Searching National Weather Service reports…');
    $('[data-out="summary"]').innerHTML = '';
    $('[data-out="tablewrap"]').hidden = true;
    var url = 'https://mesonet.agron.iastate.edu/geojson/lsr.geojson?states=TX&sts=' + start.toISOString().slice(0, 16) + 'Z&ets=' + endPlus.toISOString().slice(0, 16) + 'Z';
    fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (data) {
      var hits = (data.features || []).map(function (f) {
        var p = f.properties; return { p: p, dist: miles(place[1], place[2], p.lat, p.lon) };
      }).filter(function (h) { return allowed.indexOf(h.p.type) >= 0 && h.dist <= radius; })
        .sort(function (a, b) { return new Date(b.p.valid) - new Date(a.p.valid); });
      links(start, end);
      if (!hits.length) {
        setStatus('No ' + (types === 'hailonly' ? 'hail' : 'storm') + ' reports within ' + radius + ' miles of ' + place[0] + ' for those dates. Try a wider radius or nearby dates.');
        return;
      }
      setStatus('');
      var hail = hits.filter(function (h) { return h.p.type === 'H'; });
      var maxHail = hail.reduce(function (m, h) { return Math.max(m, parseFloat(h.p.magnitude) || 0); }, 0);
      var wind = hits.filter(function (h) { return h.p.type === 'G' || h.p.type === 'N'; });
      var maxWind = wind.reduce(function (m, h) { return Math.max(m, parseFloat(h.p.magnitude) || 0); }, 0);
      var days = {}; hits.forEach(function (h) { days[new Date(h.p.valid).toLocaleDateString('en-US', { timeZone: 'America/Chicago' })] = 1; });
      $('[data-out="summary"]').innerHTML = '<div class="inv-totals" style="margin:1rem 0"><div><span>' + hits.length + '</span><p>reports within ' + radius + ' mi of ' + esc(place[0]) + '</p></div>' +
        '<div><span>' + (maxHail ? maxHail.toFixed(2) + '"' : '–') + '</span><p>largest hail' + (maxHail ? ' (' + hailName(maxHail) + ')' : '') + '</p></div>' +
        '<div><span>' + (maxWind ? Math.round(maxWind) + ' mph' : '–') + '</span><p>strongest measured or estimated gust</p></div>' +
        '<div><span>' + Object.keys(days).length + '</span><p>different storm days</p></div></div>';
      $('[data-out="rows"]').innerHTML = hits.slice(0, 300).map(function (h) {
        var p = h.p, mag = parseFloat(p.magnitude);
        var size = p.type === 'H' ? (mag ? mag.toFixed(2) + '" (' + hailName(mag) + ')' : '') : (p.type === 'G' || p.type === 'N') && mag ? Math.round(mag) + ' mph' : '';
        var when = new Date(p.valid).toLocaleString('en-US', { timeZone: 'America/Chicago', month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
        return '<tr><td>' + esc(when) + '</td><td>' + esc(TYPES[p.type] || p.typetext) + (p.remark ? '<br><small class="muted">' + esc(p.remark).slice(0, 160) + '</small>' : '') + '</td><td>' + esc(size) + '</td><td>' + esc(p.city) + ', ' + esc(p.county) + ' Co.</td><td>' + h.dist.toFixed(1) + ' mi</td><td>' + esc(p.source) + '</td></tr>';
      }).join('');
      $('[data-out="tablewrap"]').hidden = false;
    }).catch(function () {
      links(start, end);
      setStatus('The storm report service did not respond. Use the NOAA links below, or try again in a minute.');
    });
  }
  root.addEventListener('click', function (e) { if (e.target.closest('[data-act="go"]')) go(); });
  root.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.matches('input')) { e.preventDefault(); go(); } });
})();
