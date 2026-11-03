/* Solar panel angle calculator */
(function () {
  'use strict';
  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var MID = [17, 47, 75, 105, 135, 162, 198, 228, 258, 288, 318, 344]; // mid-month day of year
  function decl(n) { return 23.44 * Math.sin(2 * Math.PI * (284 + n) / 365); }
  function noonElev(lat, n) { return Math.max(0, 90 - Math.abs(lat - decl(n))); }

  function viz(el, tilt, elev, south) {
    // side view: ground, panel tilted, sun ray at winter-noon elevation
    var W = 520, H = 210, gx = 150, gy = 170, L = 150;
    var t = tilt * Math.PI / 180, e = elev * Math.PI / 180;
    var px = gx + Math.cos(t) * L * (south ? 1 : 1), py = gy - Math.sin(t) * L;
    // panel faces the sun side (right). Draw panel from (gx,gy) up-left so its face points right
    var x1 = gx, y1 = gy, x2 = gx - Math.cos(t) * L, y2 = gy - Math.sin(t) * L;
    var cx = (x1 + x2) / 2, cy = (y1 + y2) / 2;
    var sx = cx + Math.cos(e) * 260, sy = cy - Math.sin(e) * 260;
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Panel tilted ' + Math.round(tilt) + ' degrees facing the winter noon sun">';
    s += '<rect x="0" y="' + gy + '" width="' + W + '" height="' + (H - gy) + '" fill="#cfe8c9"/>';
    s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + sx + '" y2="' + sy + '" stroke="#f59e0b" stroke-width="2" stroke-dasharray="6 6"/>';
    s += '<circle cx="' + Math.min(sx, W - 24) + '" cy="' + Math.max(sy, 22) + '" r="18" fill="#fbbf24"/><circle cx="' + Math.min(sx, W - 24) + '" cy="' + Math.max(sy, 22) + '" r="28" fill="#fbbf24" opacity=".25"/>';
    s += '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + gx + '" y2="' + (gy + 0) + '" />';
    s += '<line x1="' + (x2 + 6) + '" y1="' + (y2 + 8) + '" x2="' + (x2 + 6) + '" y2="' + gy + '" stroke="#64748b" stroke-width="4"/>';
    s += '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="#1d3f8f" stroke-width="10" stroke-linecap="round"/>';
    s += '<line x1="' + x1 + '" y1="' + (y1 - 4) + '" x2="' + x2 + '" y2="' + (y2 - 4) + '" stroke="#5b8def" stroke-width="2" stroke-linecap="round"/>';
    // angle arc
    var r = 46, ax = gx - r, ay = gy;
    var bx = gx - Math.cos(t) * r, by = gy - Math.sin(t) * r;
    s += '<path d="M' + ax + ' ' + ay + ' A' + r + ' ' + r + ' 0 0 1 ' + bx + ' ' + by + '" fill="none" stroke="#f97316" stroke-width="2.5"/>';
    s += '<text x="' + (gx - r - 44) + '" y="' + (gy - 10) + '" font-size="15" font-weight="700" fill="#0f172a">' + Math.round(tilt) + '°</text>';
    s += '<text x="' + (W - 12) + '" y="' + (gy + 26) + '" text-anchor="end" font-size="13" fill="#14532d" font-weight="600">' + (south ? 'Face TRUE SOUTH →' : 'Face TRUE NORTH →') + '</text>';
    s += '<text x="' + (Math.min(sx, W - 24) - 30) + '" y="' + (Math.max(sy, 22) + 44) + '" font-size="11" fill="#7c2d12">winter noon sun ' + Math.round(elev) + '°</text>';
    s += '</svg>';
    el.innerHTML = s;
  }

  SC.init('panel-angle', function (form, box) {
    var o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
    var lat = SC.clamp(SC.num(form, 'lat', 40), -70, 70);
    var a = Math.abs(lat), south = lat >= 0;
    var goal = SC.val(form, 'goal', 'winter'), snow = SC.val(form, 'snow', '0') === '1';
    var minT = a < 15 ? 15 : 10;
    var w = SC.clamp(Math.round(a + 15), minT, 80), sp = SC.clamp(Math.round(a), minT, 75), su = SC.clamp(Math.round(a - 15), minT, 70);
    var rec = goal === 'winter' ? SC.clamp(Math.round(a + 10), minT, 75) : goal === 'summer' ? su : sp;
    if (snow && rec < 45) rec = Math.max(rec, Math.min(45, w));
    var winterDay = south ? 355 : 172;
    var lowNoon = noonElev(lat, winterDay);
    o('tilt').textContent = rec + '°';
    o('w').textContent = w + '°'; o('sp').textContent = sp + '°'; o('su').textContent = su + '°';
    o('noon').textContent = Math.round(lowNoon) + '°';
    var dir = south ? 'true south' : 'true north';
    var note = a < 12 ? ' Near the equator the sun crosses overhead, so keep at least 10–15° of tilt for rain to wash the panel clean.' : '';
    o('summary').innerHTML = 'Tilt your panel <strong>' + rec + '° from horizontal</strong> and face it <strong>' + dir + '</strong>' +
      (goal === 'winter' ? ' (latitude + 10°, biased toward the low winter sun).' : goal === 'summer' ? ' (latitude − 15°).' : ' (≈ your latitude).') +
      (snow ? ' Steep enough to shed snow.' : '') + note;
    viz(o('viz'), rec, lowNoon, south);
    var pts = MID.map(function (n, i) { return [i, noonElev(lat, n)]; });
    var opt = MID.map(function (n, i) { return [i, SC.clamp(90 - noonElev(lat, n), 0, 90)]; });
    var fixed = MID.map(function (n, i) { return [i, rec]; });
    SC.lineChart(o('chart'), {
      xmin: 0, xmax: 11, ymin: 0, ymax: 90, yticks: [0, 30, 60, 90], ysuf: '°', h: 200,
      xticks: MONTHS.map(function (m, i) { return [i, m]; }), label: 'Noon sun elevation and ideal tilt by month',
      series: [
        { pts: pts, color: '#f59e0b', fill: 'rgba(245,158,11,.12)' },
        { pts: opt, color: '#1d4ed8', dash: '5 5' },
        { pts: fixed, color: '#15803d', width: 2 }
      ]
    });
    if (!o('chart').nextElementSibling || !o('chart').nextElementSibling.classList.contains('legend')) {
      var lg = document.createElement('p'); lg.className = 'tool-note legend';
      lg.innerHTML = '<span style="color:#f59e0b">━</span> noon sun height &nbsp; <span style="color:#1d4ed8">┅</span> ideal tilt that month &nbsp; <span style="color:#15803d">━</span> your fixed tilt';
      o('chart').after(lg);
    }
  });

  document.addEventListener('change', function (e) {
    if (e.target.name === 'city' && e.target.value) {
      var f = e.target.form; f.elements.lat.value = e.target.value; f.elements.lat.dispatchEvent(new Event('input', { bubbles: true }));
    }
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-geo]');
    if (!b || !navigator.geolocation) return;
    b.disabled = true;
    navigator.geolocation.getCurrentPosition(function (p) {
      var f = b.form; f.elements.lat.value = p.coords.latitude.toFixed(1); f.elements.city.value = '';
      f.elements.lat.dispatchEvent(new Event('input', { bubbles: true })); b.disabled = false;
    }, function () { b.disabled = false; alert('Location unavailable. Enter your latitude or pick a city.'); }, { timeout: 8000 });
  });
})();
