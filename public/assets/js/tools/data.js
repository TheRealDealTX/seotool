/* 4G data & microSD storage calculator */
(function () {
  'use strict';
  SC.init('data', function (form, box) {
    var o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
    var ev = SC.num(form, 'ev', 25), clip = SC.num(form, 'clip', 20), res = SC.num(form, 'res', 3), codec = SC.num(form, 'codec', 0.6);
    var live = SC.num(form, 'live', 5), lqv = SC.val(form, 'lq', '0.5'), up = SC.num(form, 'up', 1), sd = SC.num(form, 'sd', 128), cont = SC.val(form, 'cont', false);
    var mbps = res * codec, lq = lqv === 'hd' ? mbps : 0.5;
    var clipMB = clip * mbps / 8;                     // MB per clip
    var clipsDay = ev * clipMB * up;                  // MB/day uploaded
    var liveDay = live * 60 * lq / 8;
    var overDay = (clipsDay + liveDay) * 0.1 + 2;     // overhead + keep-alive (~60 MB/mo)
    var dayMB = clipsDay + liveDay + overDay, monthGB = dayMB * 30 / 1024;
    o('gb').innerHTML = SC.fmt(monthGB, monthGB < 10 ? 1 : 0) + ' <small>GB / month</small>';
    o('sum').innerHTML = up ? 'Estimated <strong>cellular data</strong> for one camera uploading every clip and using live view as set.' : 'Clips stay on the card, so 4G only carries <strong>live view, alerts and keep-alive</strong> traffic.';
    o('day').textContent = SC.fmt(dayMB, 0) + ' MB';
    var plan = monthGB <= 1 ? '1 GB IoT plan' : monthGB <= 3 ? '3 GB plan' : monthGB <= 5 ? '5 GB plan' : monthGB <= 10 ? '10 GB plan' : monthGB <= 20 ? '20 GB plan' : 'Unlimited / 50 GB+';
    o('plan').textContent = plan;
    var cardMB = sd * 1000 * 0.93; // formatted capacity
    var sdDayMB = cont ? 86400 * mbps / 8 : ev * clipMB;
    var days = cardMB / sdDayMB;
    o('sdd').textContent = days >= 365 ? '1 year+' : SC.fmt(days, days < 10 ? 1 : 0) + ' days';
    o('clips').textContent = cont ? SC.fmt(cardMB / (86400 * mbps / 8), 1) + ' days 24/7' : SC.fmt(cardMB / clipMB, 0);
    var parts = [['Motion clips', clipsDay * 30 / 1024], ['Live view', liveDay * 30 / 1024], ['Overhead', overDay * 30 / 1024]];
    var mx = Math.max.apply(null, parts.map(function (p) { return p[1]; })) || 1;
    o('bars').innerHTML = parts.map(function (p) { return '<div class="b"><span>' + p[0] + '</span><i style="--w:' + (p[1] / mx * 100).toFixed(0) + '%"></i><span>' + SC.fmt(p[1], 2) + ' GB</span></div>'; }).join('');
  });
})();
