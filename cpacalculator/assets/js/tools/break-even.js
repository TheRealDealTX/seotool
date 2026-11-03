(function () {
  var form = document.getElementById('be-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var n0 = function (x) { return Math.round(x).toLocaleString('en-US'); };
  var m2 = function (x) { return C.money(x, Math.round(x * 100) % 100 !== 0 && Math.abs(x) < 1000 ? 2 : 0); };
  var short = function (x) {
    var a = Math.abs(x);
    return a >= 1e6 ? '$' + (x / 1e6).toFixed(a >= 1e7 ? 0 : 1).replace(/\.0$/, '') + 'M' : a >= 1e3 ? '$' + (x / 1e3).toFixed(a >= 1e4 ? 0 : 1).replace(/\.0$/, '') + 'k' : '$' + Math.round(x);
  };
  var nice = function (x) {
    if (x <= 0) return 1;
    var p = Math.pow(10, Math.floor(Math.log10(x))), r = x / p;
    return (r <= 1 ? 1 : r <= 2 ? 2 : r <= 2.5 ? 2.5 : r <= 5 ? 5 : 10) * p;
  };

  function chart(svg, F, p, vc, be, expected) {
    if (!svg) return;
    var W = 420, H = 270, L = 52, R = 14, T = 16, B = 40, pw = W - L - R, ph = H - T - B;
    var ok = p - vc > 0 && isFinite(be);
    var xmax = nice(Math.max(ok ? be * 2 : 0, expected * 1.15, 10));
    var ymax = nice(Math.max(p * xmax, F + vc * xmax, F * 1.2, 1));
    var X = function (u) { return L + u / xmax * pw; }, Y = function (d) { return T + ph - d / ymax * ph; };
    var h = '';
    for (var i = 0; i <= 4; i++) {
      var yv = ymax * i / 4, xv = xmax * i / 4;
      h += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(yv) + '" y2="' + Y(yv) + '" stroke="#e3e8f0"/>';
      h += '<text x="' + (L - 6) + '" y="' + (Y(yv) + 3.5) + '" text-anchor="end" font-size="10" fill="#5b6b82">' + short(yv) + '</text>';
      h += '<text x="' + X(xv) + '" y="' + (H - B + 15) + '" text-anchor="' + (i === 4 ? 'end' : i === 0 ? 'start' : 'middle') + '" font-size="10" fill="#5b6b82">' + n0(xv) + '</text>';
    }
    h += '<text x="' + (L + pw / 2) + '" y="' + (H - 6) + '" text-anchor="middle" font-size="10.5" fill="#24324f" font-weight="600">Units sold</text>';
    if (ok) {
      // Loss wedge (left of break-even) and profit wedge (right).
      h += '<polygon points="' + X(0) + ',' + Y(0) + ' ' + X(0) + ',' + Y(F) + ' ' + X(be) + ',' + Y(F + vc * be) + '" fill="#f43f5e" fill-opacity=".10"/>';
      h += '<polygon points="' + X(be) + ',' + Y(p * be) + ' ' + X(xmax) + ',' + Y(Math.min(ymax, p * xmax)) + ' ' + X(xmax) + ',' + Y(F + vc * xmax) + '" fill="#10b981" fill-opacity=".14"/>';
    }
    h += '<line x1="' + X(0) + '" x2="' + X(xmax) + '" y1="' + Y(F) + '" y2="' + Y(F) + '" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="5 4"/>';
    h += '<line x1="' + X(0) + '" x2="' + X(xmax) + '" y1="' + Y(F) + '" y2="' + Y(F + vc * xmax) + '" stroke="#f43f5e" stroke-width="2.5"/>';
    h += '<line x1="' + X(0) + '" x2="' + X(xmax) + '" y1="' + Y(0) + '" y2="' + Y(p * xmax) + '" stroke="#10b981" stroke-width="2.5"/>';
    if (expected > 0 && expected <= xmax) {
      h += '<line x1="' + X(expected) + '" x2="' + X(expected) + '" y1="' + T + '" y2="' + Y(0) + '" stroke="#0e7490" stroke-width="1.2" stroke-dasharray="3 3"/>';
      h += '<text x="' + (X(expected) + 4) + '" y="' + (T + 10) + '" font-size="10" fill="#0e7490">Expected</text>';
    }
    if (ok) {
      var bx = X(be), by = Y(p * be);
      h += '<circle cx="' + bx + '" cy="' + by + '" r="5.5" fill="#0b1220" stroke="#fff" stroke-width="2"><title>Break-even: ' + n0(Math.ceil(be)) + ' units, ' + C.money(p * be) + '</title></circle>';
      h += '<text x="' + (bx - 8) + '" y="' + (by - 10) + '" text-anchor="end" font-size="10.5" font-weight="700" fill="#0b1220">Break-even ' + n0(Math.ceil(be)) + '</text>';
    }
    // Legend
    var lg = [['Revenue', '#10b981', ''], ['Total cost', '#f43f5e', ''], ['Fixed cost', '#94a3b8', '5 4']], lx = L + 8;
    lg.forEach(function (g) {
      h += '<line x1="' + lx + '" x2="' + (lx + 16) + '" y1="' + (T + 8) + '" y2="' + (T + 8) + '" stroke="' + g[1] + '" stroke-width="2.5"' + (g[2] ? ' stroke-dasharray="' + g[2] + '"' : '') + '/>';
      h += '<text x="' + (lx + 20) + '" y="' + (T + 11.5) + '" font-size="10" fill="#24324f">' + g[0] + '</text>';
      lx += g[0].length * 5.6 + 34;
    });
    h += '<line x1="' + L + '" x2="' + L + '" y1="' + T + '" y2="' + Y(0) + '" stroke="#cfd8e4"/><line x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(0) + '" y2="' + Y(0) + '" stroke="#cfd8e4"/>';
    svg.innerHTML = h;
  }

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var F = Math.max(0, v('fixed')), p = Math.max(0, v('price')), vc = Math.max(0, v('var'));
    var target = v('target'), expected = Math.max(0, v('expected'));
    var cm = p - vc, cmr = p > 0 ? cm / p : 0, ok = cm > 0;
    var be = ok ? F / cm : Infinity, beRev = ok ? F / cmr : Infinity, beUnits = ok ? Math.ceil(be - 1e-9) : 0;
    var tu = ok ? Math.ceil((F + Math.max(0, target)) / cm - 1e-9) : 0;
    var unitsEl = C.$('[data-out="units"]', tool);
    unitsEl.classList.toggle('bad', !ok);
    if (ok) C.big(tool, 'units', beUnits, function (x) { return n0(x) + ' units'; });
    else { unitsEl.dataset.v = 0; unitsEl.textContent = 'Not reachable'; }
    C.set(tool, 'sub', ok ? '= ' + C.money(beUnits * p) + ' in sales to cover ' + C.money(F) + ' of fixed costs' : 'Price must be higher than variable cost per unit to ever break even.');
    C.set(tool, 'rev', ok ? C.money(beRev) : '—');
    C.set(tool, 'cm', m2(cm));
    C.set(tool, 'cmr', C.pct(cmr));
    C.set(tool, 'tu', ok ? n0(tu) : '—');
    var profit = expected * cm - F, mos = expected - be;
    C.set(tool, 'mos', expected > 0 && ok ? n0(mos) + ' units (' + C.pct(mos / expected) + ')' : '—');
    C.set(tool, 'profit', expected > 0 ? C.money(profit) : '—');
    chart(C.$('[data-chart]', tool), F, p, vc, be, expected);

    var rows = [
      ['Selling price per unit', m2(p)], ['Variable cost per unit', '−' + m2(vc), 'sub'],
      ['Contribution margin per unit', m2(cm)], ['Fixed costs', C.money(F)],
      ['Break-even units (' + C.money(F) + ' ÷ ' + m2(cm) + ')', ok ? n0(beUnits) : '—']
    ];
    if (target > 0 && ok) rows.push(['Revenue for ' + C.money(target) + ' profit', C.money(tu * p)]);
    if (expected > 0) {
      rows.push(['Expected sales', n0(expected) + ' units · ' + C.money(expected * p)]);
      rows.push(['Total contribution margin', C.money(expected * cm), 'sub']);
      if (ok) rows.push(['Margin of safety ($)', C.money(mos * p), 'sub']);
      if (profit > 0) rows.push(['Operating leverage (DOL)', (expected * cm / profit).toFixed(2) + '×', 'sub']);
    }
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>' + (expected > 0 ? (profit >= 0 ? 'Profit at expected sales' : 'Loss at expected sales') : 'Break-even revenue') + '</span><b>' + (expected > 0 ? C.money(profit) : (ok ? C.money(beRev) : '—')) + '</b></li>';
    C.set(tool, 'note', (expected > 0 && ok && expected < be ? 'Expected sales are below break-even — you need ' + n0(beUnits - expected) + ' more units to cover fixed costs. ' : '') +
      'Assumes price and variable cost per unit stay constant; figures are before income tax.');
  });
})();
