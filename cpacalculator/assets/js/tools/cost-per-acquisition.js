(function () {
  var form = document.getElementById('cpa-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var m2 = function (x) { return isFinite(x) ? C.money(x, Math.abs(x) < 1000 ? 2 : 0) : '—'; };
  var n0 = function (x) { return isFinite(x) ? Math.round(x).toLocaleString('en-US') : '—'; };
  var pc = function (x, dp) { return isFinite(x) ? C.pct(x, dp == null ? 2 : dp) : '—'; };

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var mode = C.str(f, 'mode') || 'actual';
    C.$$('[data-when]', f).forEach(function (el) { var off = el.dataset.when !== mode; el.hidden = off; el.style.display = off ? 'none' : ''; });

    var adSpend, other = 0, conv, clicks, impr;
    if (mode === 'plan') {
      adSpend = Math.max(0, v('budget'));
      var cpcIn = v('cpc'), ctrIn = v('ctr') / 100, cvrIn = v('cvr') / 100;
      clicks = cpcIn > 0 ? adSpend / cpcIn : NaN;
      conv = clicks * cvrIn;
      impr = ctrIn > 0 ? clicks / ctrIn : NaN;
    } else {
      adSpend = Math.max(0, v('spend')); other = Math.max(0, v('other'));
      conv = v('conv'); clicks = v('clicks') || NaN; impr = v('impr') || NaN;
    }
    var cost = adSpend + other;
    var cpa = conv > 0 ? cost / conv : NaN;
    var cpc = clicks > 0 ? adSpend / clicks : NaN, ctr = impr > 0 ? clicks / impr : NaN;
    var cvr = clicks > 0 ? conv / clicks : NaN, cpm = impr > 0 ? adSpend / impr * 1000 : NaN;
    var rpc = v('rpc'), rev = conv > 0 ? conv * rpc : 0;
    var roas = adSpend > 0 && rpc > 0 ? rev / adSpend : NaN, roi = cost > 0 && rpc > 0 ? (rev - cost) / cost : NaN;
    var clv = v('clv'), margin = C.clamp(v('margin'), 0, 100) / 100;
    var tcpa = clv > 0 ? clv * (1 - margin) : NaN, maxcpc = isFinite(tcpa) && isFinite(cvr) ? tcpa * cvr : NaN;

    var big = C.$('[data-out="cpa"]', tool);
    if (isFinite(cpa)) C.big(tool, 'cpa', cpa, function (x) { return C.money(x, 2); });
    else { big.dataset.v = 0; big.textContent = '—'; }
    big.classList.toggle('good', isFinite(cpa) && isFinite(tcpa) && cpa <= tcpa);
    big.classList.toggle('bad', isFinite(cpa) && isFinite(tcpa) && cpa > tcpa);
    C.set(tool, 'sub', !isFinite(cpa) ? 'Enter cost and conversions to calculate CPA' :
      C.money(cost) + ' ÷ ' + n0(conv) + ' conversions' + (isFinite(tcpa) ? (cpa <= tcpa ? ' · ' + m2(tcpa - cpa) + ' under your ' + m2(tcpa) + ' target' : ' · ' + m2(cpa - tcpa) + ' over your ' + m2(tcpa) + ' target') : ''));
    C.set(tool, 'cpc', m2(cpc)); C.set(tool, 'ctr', pc(ctr)); C.set(tool, 'cvr', pc(cvr)); C.set(tool, 'cpm', m2(cpm));
    C.set(tool, 'roas', isFinite(roas) ? roas.toFixed(2) + '× (' + C.pct(roas, 0) + ')' : '—');
    C.set(tool, 'roi', pc(roi, 0));

    var steps = [['Impressions', n0(impr)], ['Clicks' + (isFinite(ctr) ? ' · ' + pc(ctr) + ' CTR' : ''), n0(clicks)], ['Conversions' + (isFinite(cvr) ? ' · ' + pc(cvr) + ' CVR' : ''), n0(conv)], ['Revenue', rpc > 0 ? C.money(rev) : '—']];
    C.$('[data-funnel]', tool).innerHTML = steps.map(function (s) { return '<div><small>' + s[0] + '</small><b>' + s[1] + '</b></div>'; }).join('');

    var segs = [
      { label: 'Ad spend', value: adSpend, color: '#f59e0b' },
      { label: 'Other campaign costs', value: other, color: '#6366f1' },
      { label: 'Revenue after acquisition cost', value: Math.max(0, rev - cost), color: '#10b981' }
    ].filter(function (x) { return x.value > 0; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var rows = [];
    if (mode === 'plan') {
      rows.push(['Budget ÷ CPC = clicks', n0(clicks)]);
      rows.push(['Clicks × conversion rate = conversions', n0(conv)]);
      rows.push(['CPA = CPC ÷ conversion rate', m2(cpa), 'sub']);
    } else {
      rows.push(['Total cost' + (other ? ' (ads + other)' : ''), C.money(cost)]);
      if (other) rows.push(['Media-only CPA', m2(conv > 0 ? adSpend / conv : NaN), 'sub']);
    }
    if (rpc > 0) {
      rows.push(['Revenue (' + n0(conv) + ' × ' + m2(rpc) + ')', C.money(rev)]);
      rows.push(['Revenue per conversion − CPA', m2(rpc - cpa), 'sub']);
    }
    if (isFinite(tcpa)) {
      rows.push(['Break-even CPA (lifetime value)', m2(clv)]);
      rows.push(['Target CPA (' + m2(clv) + ' × ' + C.pct(1 - margin, 0) + ')', m2(tcpa)]);
      if (isFinite(maxcpc)) rows.push(['Max CPC at target (' + m2(tcpa) + ' × ' + pc(cvr) + ')', m2(maxcpc), 'sub']);
      if (conv > 0) rows.push(['Max spend for ' + n0(conv) + ' conversions at target', C.money(conv * tcpa), 'sub']);
    }
    C.$('[data-rows]', tool).innerHTML = rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Cost per acquisition</span><b>' + (isFinite(cpa) ? C.money(cpa, 2) : '—') + '</b></li>';
    C.set(tool, 'note', (isFinite(cpa) && isFinite(tcpa) && cpa > tcpa ? 'CPA is above target — improve conversion rate, lower CPC or raise customer value. ' : '') +
      'ROI here is on revenue; subtract product costs for a profit-based ROI.');
  });
})();
