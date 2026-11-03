/* Solar camera battery & power calculator */
(function () {
  'use strict';
  SC.init('battery', function (form, box) {
    var o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
    var mah = SC.num(form, 'mah', 10000), v = SC.num(form, 'v', 3.7);
    var ev = SC.num(form, 'ev', 30), clip = SC.num(form, 'clip', 20), live = SC.num(form, 'live', 3);
    var lte = SC.val(form, 'net', 'wifi') === 'lte', res = SC.num(form, 'res', 1), spot = SC.val(form, 'spot', false);
    var pw = SC.num(form, 'pw', 5), n = Math.max(1, Math.round(SC.num(form, 'n', 1)));
    var psh = SC.num(form, 'psh', 2.5), exp = SC.num(form, 'exp', 1), cloud = SC.num(form, 'cold', 0) ? 0 : 0;
    cloud = SC.num(form, 'cloud', 3);
    var cold = SC.val(form, 'cold', false);

    var activeW = (lte ? 4 : 3) * res;
    var standby = lte ? 2 : 0.6;                          // Wh/day sleep + keep-alive
    var evWh = ev * (clip + 4) * activeW / 3600;          // +4 s wake/upload overhead
    var spotWh = spot ? ev * 0.5 * clip * 3 / 3600 : 0;   // half the events at night, ~3 W LEDs
    var liveWh = live * 60 * activeW / 3600;
    var use = standby + evWh + spotWh + liveWh;
    var capWh = mah / 1000 * v * 0.9 * (cold ? 0.8 : 1);
    var gain = pw * psh * exp * 0.7;
    var net = gain - use;
    var daysNoSun = capWh / use;
    var need = use / (psh * exp * 0.7) * 1.3;

    o('days').innerHTML = (daysNoSun >= 60 ? '60+' : SC.fmt(daysNoSun, daysNoSun < 10 ? 1 : 0)) + ' <small>days</small>';
    o('sum').innerHTML = 'Runtime on a <strong>full battery with zero sun</strong>. Your camera uses about <strong>' + SC.fmt(use, 2) + ' Wh/day</strong> and the panel brings in about <strong>' + SC.fmt(gain, 1) + ' Wh/day</strong>.';
    var vd = o('verdict');
    var ratio = gain / use;
    if (ratio >= 2) { vd.className = 'verdict ok'; vd.innerHTML = '✔ <span><strong>Self-sustaining with margin.</strong> The panel makes ' + SC.fmt(ratio, 1) + '× what the camera uses, so the battery refills quickly after cloudy spells.</span>'; }
    else if (ratio >= 1.2) { vd.className = 'verdict mid'; vd.innerHTML = '◐ <span><strong>Sustainable, thin margin.</strong> Fine on average days, but long cloudy spells will drain it. A bigger panel or fewer triggers adds headroom.</span>'; }
    else { vd.className = 'verdict bad'; vd.innerHTML = '✖ <span><strong>Energy deficit.</strong> The camera uses more than the panel can replace (' + SC.fmt(ratio * 100) + '%). Expect manual recharges unless you add panel watts, move it to full sun or cut triggers/live view.</span>'; }
    o('use').textContent = SC.fmt(use, 2) + ' Wh';
    o('gain').textContent = SC.fmt(gain, 1) + ' Wh';
    o('cap').textContent = SC.fmt(capWh, 1) + ' Wh';
    o('need').textContent = (need < 2.5 ? 'built-in / 2.5' : SC.fmt(Math.ceil(need), 0)) + ' W';

    // 14-day hourly simulation, start 80%, cloudy spell days 4..(3+cloud) at 15% harvest
    var pts = [], b = capWh * 0.8, hrs = 14 * 24, minB = b;
    var dayLen = 10, sunrise = 7;
    for (var h = 0; h <= hrs; h++) {
      var day = Math.floor(h / 24), hod = h % 24;
      var factor = (day >= 3 && day < 3 + cloud) ? 0.15 : 1;
      if (cold && hod < 10 && day % 2 === 0) factor *= 0.3; // frosty mornings block charging
      var sun = (hod >= sunrise && hod < sunrise + dayLen) ? Math.sin((hod - sunrise + 0.5) / dayLen * Math.PI) : 0;
      var inWh = gain * factor * sun * (Math.PI / 2) / dayLen;
      b = Math.min(capWh, Math.max(0, b + inWh - use / 24));
      minB = Math.min(minB, b);
      if (h % 3 === 0) pts.push([h / 24, b / capWh * 100]);
    }
    SC.lineChart(o('chart'), {
      xmin: 0, xmax: 14, ymin: 0, ymax: 100, yticks: [0, 25, 50, 75, 100], ysuf: '%', h: 210,
      xticks: [[0, 'Day 1'], [3, '4'], [7, '8'], [11, '12'], [14, '15']], label: 'Simulated battery percentage over 14 days',
      bands: cloud > 0 ? [[3, Math.min(14, 3 + cloud), 'rgba(100,116,139,.12)']] : [],
      series: [{ pts: pts, color: minB <= 0.01 ? '#c2410c' : '#15803d', fill: minB <= 0.01 ? 'rgba(194,65,12,.1)' : 'rgba(21,128,61,.1)' }]
    });
    var parts = [['Standby & keep-alive', standby], ['Motion clips', evWh], ['Live view', liveWh]];
    if (spot) parts.push(['Night spotlight', spotWh]);
    var mx = Math.max.apply(null, parts.map(function (p) { return p[1]; })) || 1;
    o('bars').innerHTML = parts.map(function (p) { return '<div class="b"><span>' + p[0] + '</span><i style="--w:' + (p[1] / mx * 100).toFixed(0) + '%"></i><span>' + SC.fmt(p[1], 2) + ' Wh</span></div>'; }).join('');
    if (n > 1) {
      var tot = use * n, ah12 = tot * 3 / 12 / 0.8;
      o('multi').innerHTML = '<h4>Powering ' + n + ' cameras from one shared 12 V system</h4><ul class="plan-list">' +
        '<li><span>Total daily energy</span><b>' + SC.fmt(tot, 1) + ' Wh</b></li>' +
        '<li><span>Shared panel for this site (with 30% margin)</span><b>' + SC.fmt(Math.ceil(need * n / 5) * 5) + ' W</b></li>' +
        '<li><span>12 V battery for 3 sunless days (80% DoD)</span><b>' + SC.fmt(Math.ceil(ah12)) + ' Ah</b></li></ul>';
    } else o('multi').innerHTML = '';
  });
})();
