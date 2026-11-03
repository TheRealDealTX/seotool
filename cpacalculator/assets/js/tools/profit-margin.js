(function () {
  var form = document.getElementById('pm-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var m2 = function (n) { return C.money(n, Math.abs(n) < 1000 && Math.round(n * 100) % 100 !== 0 ? 2 : 0); };
  var rows = function (list, total) {
    C.$('[data-rows]', tool).innerHTML = list.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      (total ? '<li class="total"><span>' + total[0] + '</span><b>' + total[1] + '</b></li>' : '');
  };
  var pctOrDash = function (n) { return isFinite(n) ? C.pct(n) : '—'; };

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var mode = C.str(f, 'mode') || 'price';
    C.$$('[data-when]', f).forEach(function (el) {
      var off = el.dataset.when.split(' ').indexOf(mode) < 0;
      el.hidden = off; el.style.display = off ? 'none' : '';
    });
    var bigEl = C.$('[data-out="big"]', tool), segs, note = 'Margin is profit ÷ price; markup is profit ÷ cost.';

    if (mode === 'pl') {
      var rev = v('rev'), cogs = v('cogs'), opex = v('opex'), other = v('other');
      var gross = rev - cogs, op = gross - opex, net = op - other;
      var gm = rev ? gross / rev : 0, om = rev ? op / rev : 0, nm = rev ? net / rev : 0;
      C.set(tool, 'biglabel', 'Net profit margin');
      C.big(tool, 'big', nm, function (x) { return C.pct(x); });
      bigEl.classList.toggle('bad', net < 0);
      C.set(tool, 'sub', rev ? 'Keeps ' + C.money(Math.max(0, net) / rev * 100, 2) + ' of every $100 in sales · net profit ' + C.money(net) : 'Enter revenue to calculate margins');
      C.set(tool, 'k1l', 'Gross margin'); C.set(tool, 'k1', C.pct(gm));
      C.set(tool, 'k2l', 'Operating margin'); C.set(tool, 'k2', C.pct(om));
      C.set(tool, 'k3l', 'Gross profit'); C.set(tool, 'k3', C.money(gross));
      C.set(tool, 'k4l', 'Operating profit'); C.set(tool, 'k4', C.money(op));
      segs = [
        { label: 'Cost of goods sold', value: cogs, color: '#f59e0b' },
        { label: 'Operating expenses', value: opex, color: '#6366f1' },
        { label: 'Interest, taxes & other', value: other, color: '#0e7490' },
        { label: 'Net profit', value: net, color: '#10b981' }
      ];
      rows([
        ['Revenue', C.money(rev)], ['Cost of goods sold', '−' + C.money(cogs)],
        ['Gross profit (' + C.pct(gm) + ')', C.money(gross)], ['Operating expenses', '−' + C.money(opex)],
        ['Operating profit / EBIT (' + C.pct(om) + ')', C.money(op)], ['Interest, taxes & other', '−' + C.money(other)]
      ], ['Net profit (' + C.pct(nm) + ')', C.money(net)]);
      note = net < 0 ? 'The business shows a net loss for this period.' : 'Each margin is that level of profit divided by revenue.';
    } else {
      var cost = Math.max(0, v('cost')), price, warn = '';
      if (mode === 'price') price = v('price');
      else if (mode === 'margin') {
        var tm = v('tmargin') / 100;
        if (tm >= 1) { warn = 'A margin must be below 100%.'; tm = 0.99; }
        price = cost / (1 - tm);
      } else price = cost * (1 + v('tmarkup') / 100);
      var profit = price - cost, margin = price ? profit / price : 0, markup = cost ? profit / cost : NaN;
      if (mode === 'price') {
        C.set(tool, 'biglabel', 'Profit margin');
        C.big(tool, 'big', margin, function (x) { return C.pct(x); });
      } else {
        C.set(tool, 'biglabel', 'Selling price');
        C.big(tool, 'big', price, m2);
      }
      bigEl.classList.toggle('bad', profit < 0);
      C.set(tool, 'sub', price > 0 ? (profit >= 0 ? 'Profit of ' + m2(profit) + ' per unit' : 'Loss of ' + m2(-profit) + ' per unit') + ' · ' + C.pct(margin) + ' margin · ' + pctOrDash(markup) + ' markup' : 'Enter a cost and price to start');
      C.set(tool, 'k1l', 'Profit margin'); C.set(tool, 'k1', C.pct(margin));
      C.set(tool, 'k2l', 'Markup'); C.set(tool, 'k2', pctOrDash(markup));
      C.set(tool, 'k3l', 'Profit per unit'); C.set(tool, 'k3', m2(profit));
      C.set(tool, 'k4l', 'Selling price'); C.set(tool, 'k4', m2(price));
      segs = [{ label: 'Cost', value: Math.min(cost, price), color: '#f59e0b' }, { label: 'Profit', value: profit, color: '#10b981' }];
      var list = [['Cost per unit', m2(cost)], ['Selling price', m2(price)], ['Profit per unit', m2(profit)]];
      var u = v('units');
      if (u > 0) {
        list.push(['Revenue (' + u.toLocaleString() + ' units)', C.money(price * u)]);
        list.push(['Total cost', '−' + C.money(cost * u), 'sub']);
        list.push(['Total profit', C.money(profit * u)]);
      }
      list.push(['Price for common margins', '']);
      [0.2, 0.3, 0.4, 0.5, 0.6].forEach(function (m) { list.push([C.pct(m, 0) + ' margin (' + C.pct(m / (1 - m)) + ' markup)', m2(cost / (1 - m)), 'sub']); });
      rows(list, [u > 0 ? 'Total profit' : 'Profit margin', u > 0 ? C.money(profit * u) : C.pct(margin)]);
      if (warn) note = warn;
      else if (mode === 'markup') note = 'A ' + C.pct(v('tmarkup') / 100) + ' markup gives a ' + C.pct(margin) + ' margin — markup is always the bigger number.';
    }
    segs = segs.filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);
    C.set(tool, 'note', note);
  });
})();
