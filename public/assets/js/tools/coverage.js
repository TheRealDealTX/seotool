/* Camera coverage & DORI calculator */
(function () {
  'use strict';
  var LV = [['Identify', 250, 'Faces & license plates beyond doubt', '#15803d'], ['Recognize', 125, 'Recognize a known person', '#65a30d'], ['Observe', 62, 'Clothing, actions', '#f59e0b'], ['Detect', 25, 'A person is there', '#f97316']];
  SC.init('coverage', function (form, box) {
    var o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
    var hp = SC.num(form, 'hp', 2560), fov = SC.num(form, 'fov', 105), ft = SC.val(form, 'u', 'ft') === 'ft', d = SC.num(form, 'd', 30);
    var dm = ft ? d * 0.3048 : d, u = ft ? 'ft' : 'm', k = ft ? 3.28084 : 1;
    var outEl = form.querySelector('output[data-for="d"]'); if (outEl) outEl.textContent = d + ' ' + u;
    var tan = Math.tan(fov / 2 * Math.PI / 180), widthM = 2 * dm * tan, ppm = hp / widthM;
    var lvl = LV.filter(function (l) { return ppm >= l[1]; })[0];
    o('w').innerHTML = SC.fmt(widthM * k, 0) + ' <small>' + u + ' wide</small>';
    o('sum').innerHTML = 'At ' + d + ' ' + u + ' the scene is ' + SC.fmt(widthM * k, 0) + ' ' + u + ' across with <strong>' + SC.fmt(ppm, 0) + ' px/m</strong> (' + SC.fmt(ppm / 3.28084, 0) + ' px/ft): good enough to <strong>' + (lvl ? lvl[0].toLowerCase() : 'barely detect') + '</strong>' + (lvl ? ' (' + lvl[2].toLowerCase() + ').' : '. Use a narrower lens or higher resolution.');
    var rows = LV.map(function (l) { var maxM = hp / (2 * tan * l[1]); return [l, maxM]; });
    o('tbl').innerHTML = rows.map(function (r) { return '<tr><td><b style="color:' + r[0][3] + '">' + r[0][0] + '</b></td><td>' + r[0][1] + ' px/m · ' + r[0][2] + '</td><td><b>' + SC.fmt(r[1] * k, 0) + ' ' + u + '</b></td></tr>'; }).join('');
    // top-down cone with DORI bands
    var W = 520, H = 230, cx = 30, cy = H / 2, maxM = Math.max(dm * 1.15, rows[3][1] * 1.05), sc = (W - 50) / maxM;
    var half = Math.min(fov / 2, 80) * Math.PI / 180;
    var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="Top-down coverage cone">';
    s += '<defs><clipPath id="cvc"><path d="M' + cx + ' ' + cy + ' L' + (cx + 2000 * Math.cos(half)) + ' ' + (cy - 2000 * Math.sin(half)) + ' L' + (cx + 2000 * Math.cos(half)) + ' ' + (cy + 2000 * Math.sin(half)) + 'Z"/></clipPath></defs>';
    s += '<rect width="' + W + '" height="' + H + '" fill="#f3f6fb"/>';
    s += '<g clip-path="url(#cvc)">';
    for (var i = rows.length - 1; i >= 0; i--) s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (rows[i][1] * sc).toFixed(1) + '" fill="' + rows[i][0][3] + '" opacity="' + (0.22 + i * 0.04) + '"/>';
    s += '</g>';
    var tx = cx + dm * sc, th = Math.min(H / 2 - 6, dm * tan * sc);
    s += '<line x1="' + tx + '" y1="' + (cy - th) + '" x2="' + tx + '" y2="' + (cy + th) + '" stroke="#0f172a" stroke-width="2" stroke-dasharray="4 4"/>';
    s += '<text x="' + (tx + 6) + '" y="' + (cy - th + 12) + '" font-weight="700" fill="#0f172a">target ' + d + ' ' + u + '</text>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="7" fill="#0b1324"/>';
    rows.forEach(function (r) { var x = cx + r[1] * sc; if (x < W - 10) s += '<text x="' + (x - 4) + '" y="' + (cy + 4) + '" text-anchor="end" fill="#0f172a" font-size="10">' + r[0][0] + '</text>'; });
    s += '</svg>';
    o('viz').innerHTML = s;
  });
})();
