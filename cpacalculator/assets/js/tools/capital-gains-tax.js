(function () {
  var form = document.getElementById('cgt-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;

  /* Tax on `amt` stacked above `base` at ordinary rates, each rate capped at `cap` (25% / 28% gain). */
  function capped(base, amt, cap, s, yr) {
    if (amt <= 0) return 0;
    var t = 0;
    C.bracketTax(base + amt, s, yr).layers.forEach(function (l) {
      var lo = Math.max(l.from, base), hi = Math.min(l.to, base + amt);
      if (hi > lo) t += (hi - lo) * Math.min(l.rate, cap);
    });
    return t;
  }
  /* Federal income tax with gains split by character. ord = other gross ordinary income. */
  function fed(o, s, yr) {
    var ordT = Math.max(0, o.ord - o.ded), left = Math.max(0, o.ded - o.ord);
    var st = o.st || 0, g25 = o.g25 || 0, g28 = o.g28 || 0, lt = o.lt || 0, r;
    r = Math.min(left, st); st -= r; left -= r;
    r = Math.min(left, g25); g25 -= r; left -= r;
    r = Math.min(left, g28); g28 -= r; left -= r;
    r = Math.min(left, lt); lt -= r;
    var base = ordT + st;
    var ordTax = C.bracketTax(base, s, yr);
    var t25 = capped(base, g25, 0.25, s, yr), t28 = capped(base + g25, g28, 0.28, s, yr);
    var stack = base + g25 + g28;
    var ltTax = C.incomeTax(stack, lt, s, yr).prefTax;
    // LTCG layers for display
    var layers = [], prev = 0;
    C.year(yr).ltcg[s].forEach(function (b) {
      var top = b[0] == null ? Infinity : b[0], lo = Math.max(stack, prev), hi = Math.min(stack + lt, top);
      layers.push({ rate: b[1], amount: Math.max(0, hi - lo), from: prev, to: top });
      prev = top;
    });
    return { tax: ordTax.tax + t25 + t28 + ltTax, ordTaxable: ordT, marginal: ordTax.marginal, ltLayers: layers, st: st, g25: g25, g28: g28, lt: lt, t25: t25, t28: t28, ltTax: ltTax };
  }

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), s = C.str(f, 'status'), d = C.year(yr);
    var asset = C.str(f, 'asset'), term = C.str(f, 'term') || 'long';
    document.getElementById('cgt-rental').hidden = asset !== 'rental';
    document.getElementById('cgt-home').hidden = asset !== 'home';

    var ord = v('income'), std = C.stdDeduction(s, yr), ded = Math.max(std, v('itemized'));
    var stateRate = C.clamp(v('state'), 0, 20) / 100;
    var proceeds = v('sale'), basis = v('basis'), fees = v('fees');
    var gain = proceeds - basis - fees;
    var homeLoss = asset === 'home' && gain < 0;
    var saleGain = homeLoss ? 0 : gain;
    var exclCap = s === 'mfj' ? 500000 : 250000;
    var excl = asset === 'home' && v('excl') && saleGain > 0 ? Math.min(saleGain, exclCap) : 0;
    var carry = v('carry');
    var net = saleGain - excl - carry;
    var base = fed({ ord: ord, ded: ded }, s, yr);
    var lossLimit = s === 'mfs' ? 1500 : 3000;

    function scenario(t) {
      var g = { ord: ord, ded: ded };
      if (net > 0) {
        if (t === 'short') g.st = net;
        else if (asset === 'collect') g.g28 = net;
        else if (asset === 'rental') { g.g25 = Math.min(net, v('depr')); g.lt = net - g.g25; }
        else g.lt = net;
      }
      var res = fed(g, s, yr);
      var magi = ord + Math.max(0, net);
      res.niit = net > 0 ? Math.max(0, Math.min(net, magi - d.niit[s])) * 0.038 : 0;
      res.fedOnGain = res.tax - base.tax;
      res.state = Math.max(0, net) * stateRate;
      res.total = res.fedOnGain + res.niit + res.state;
      return res;
    }

    var rows = [['Sale price', C.money(proceeds)], ['Cost basis', '−' + C.money(basis)]];
    if (fees) rows.push(['Selling costs', '−' + C.money(fees)]);
    rows.push([gain >= 0 ? 'Capital gain' : 'Capital loss', C.money(gain)]);
    var tool$ = function (k) { return C.$(k, tool); };
    var bigEl = tool$('[data-out="tax"]');

    if (net > 0) {
      var r = scenario(term);
      bigEl.className = 'res-big';
      C.set(tool, 'headline', 'Estimated tax on this sale');
      C.big(tool, 'tax', r.total);
      C.set(tool, 'gainLabel', 'Taxable gain');
      C.set(tool, 'gain', C.money(net));
      C.set(tool, 'eff', C.pct(r.total / net));
      C.set(tool, 'niit', C.money(r.niit));
      var rateTxt;
      if (term === 'short') rateTxt = Math.round(r.marginal * 100) + '% (ordinary)';
      else if (asset === 'collect') rateTxt = 'up to 28%';
      else {
        var on = r.ltLayers.filter(function (l) { return l.amount > 0; }).map(function (l) { return Math.round(l.rate * 100) + '%'; });
        rateTxt = (on.length ? on.join(' / ') : '0%') + (r.g25 ? ' + ≤25%' : '');
      }
      C.set(tool, 'rate', rateTxt);
      var keep = Math.max(0, proceeds - fees - r.total);
      C.set(tool, 'summary', 'You keep ' + C.money(keep) + ' of ' + C.money(proceeds) + ' · after-tax profit ' + C.money(Math.max(0, gain - r.total)));
      if (excl) rows.push(['Home sale exclusion (§121)', '−' + C.money(excl)]);
      if (carry) rows.push(['Loss carryover applied', '−' + C.money(Math.min(carry, saleGain - excl))]);
      rows.push(['Taxable gain (' + (term === 'short' ? 'short-term' : 'long-term') + ')', C.money(net)]);
      if (r.g25) rows.push(['Unrecaptured §1250 gain (≤25%)', C.money(r.t25), 'sub']);
      if (r.g28) rows.push(['Collectibles gain (≤28%)', C.money(r.t28), 'sub']);
      rows.push(['Ordinary taxable income (other income − ' + (ded > std ? 'itemized' : 'standard') + ' deduction)', C.money(base.ordTaxable)]);
      rows.push(['Federal tax on the gain', C.money(r.fedOnGain)]);
      if (r.niit) rows.push(['Net investment income tax (3.8%)', C.money(r.niit)]);
      if (r.state) rows.push(['State tax (' + (stateRate * 100).toFixed(2).replace(/\.?0+$/, '') + '%)', C.money(r.state)]);
      C.$('[data-rows]', tool).innerHTML = rowsHtml(rows) + '<li class="total"><span>Total tax on this sale</span><b>' + C.money(r.total) + '</b></li>';

      var segs = [
        { label: 'Cost basis & fees returned', value: Math.min(proceeds, basis + fees), color: '#94a3b8' },
        { label: 'Federal capital gains tax', value: r.fedOnGain, color: '#0e7490' },
        { label: 'NIIT', value: r.niit, color: '#f43f5e' },
        { label: 'State tax', value: r.state, color: '#f59e0b' },
        { label: 'Profit you keep', value: Math.max(0, gain - r.total), color: '#10b981' }
      ].filter(function (x) { return x.value > 0; });
      C.donut(tool$('[data-donut]'), segs); C.legend(tool$('[data-legend]'), segs);

      // Bracket stack
      if (term === 'long' && asset !== 'collect') {
        C.set(tool, 'stackLabel', 'Your long-term gain across the 0 / 15 / 20% brackets');
        tool$('[data-stack]').innerHTML = r.ltLayers.map(function (l) {
          var range = C.money(l.from) + (l.to === Infinity ? '+' : ' – ' + C.money(l.to));
          return '<li><span>' + Math.round(l.rate * 100) + '% on ' + C.money(l.amount) + ' <small class="hint">(' + range + ')</small></span><b>' + C.money(l.amount * l.rate) + '</b></li>';
        }).join('') + (r.g25 ? '<li><span>§1250 portion ' + C.money(r.g25) + ' at ordinary rates ≤25%</span><b>' + C.money(r.t25) + '</b></li>' : '');
      } else {
        C.set(tool, 'stackLabel', term === 'short' ? 'Short-term gain taxed at ordinary rates' : 'Collectibles gain at ordinary rates (max 28%)');
        tool$('[data-stack]').innerHTML = '<li><span>Ordinary taxable income before the sale</span><b>' + C.money(base.ordTaxable) + '</b></li>' +
          '<li><span>Top bracket reached</span><b>' + Math.round(C.bracketTax(base.ordTaxable + net, s, yr).marginal * 100) + '%</b></li>';
      }
      // Short vs long comparison
      if (asset === 'collect' && term === 'long') C.set(tool, 'compare', 'Collectibles held over a year are taxed at your ordinary rate, but never more than 28%.');
      else {
        var alt = scenario(term === 'long' ? 'short' : 'long'), diff = alt.total - r.total;
        C.set(tool, 'compare', term === 'long'
          ? 'Held one year or less, the same gain would cost ' + C.money(alt.total) + ' — holding long-term saves you ' + C.money(Math.max(0, diff)) + '.'
          : 'If you wait until you’ve held it more than a year, the tax would be about ' + C.money(alt.total) + ' — a saving of ' + C.money(Math.max(0, -diff)) + '.');
      }
    } else {
      // No taxable gain: loss, fully excluded home gain, or carryover exceeds gain
      var loss = Math.max(0, -net);
      var deductible = homeLoss && !carry ? 0 : Math.min(loss, lossLimit);
      var cf = loss - deductible;
      var after = fed({ ord: Math.max(0, ord - deductible), ded: ded }, s, yr);
      var saved = base.tax - after.tax + deductible * stateRate;
      bigEl.className = 'res-big good';
      C.set(tool, 'gainLabel', gain < 0 ? 'Capital loss' : 'Taxable gain');
      C.set(tool, 'gain', C.money(gain < 0 ? gain : 0));
      C.set(tool, 'niit', C.money(0));
      C.set(tool, 'eff', '0%');
      if (excl && net === 0 && !carry) {
        C.set(tool, 'headline', 'Tax on this sale');
        C.big(tool, 'tax', 0);
        C.set(tool, 'rate', '0% (excluded)');
        C.set(tool, 'summary', 'Your entire ' + C.money(saleGain) + ' gain is covered by the ' + C.money(exclCap) + ' home sale exclusion.');
      } else {
        C.set(tool, 'headline', saved > 0 ? 'Tax saved by this loss' : 'Tax on this sale');
        C.big(tool, 'tax', saved);
        C.set(tool, 'rate', 'n/a');
        C.set(tool, 'summary', homeLoss && !carry ? 'A loss on your personal residence is not deductible.' :
          C.money(deductible) + ' deducted against ordinary income this year' + (cf > 0 ? ' · ' + C.money(cf) + ' carries forward' : ''));
      }
      if (excl) rows.push(['Home sale exclusion (§121)', '−' + C.money(excl)]);
      if (carry) rows.push(['Loss carryover from prior years', '−' + C.money(carry)]);
      if (homeLoss) rows.push(['Personal-residence loss (not deductible)', C.money(0)]);
      rows.push(['Net capital loss', C.money(-loss)]);
      rows.push(['Deductible this year (limit ' + C.money(lossLimit) + ')', '−' + C.money(deductible)]);
      rows.push(['Carryforward to next year', C.money(cf)]);
      C.$('[data-rows]', tool).innerHTML = rowsHtml(rows) + '<li class="total"><span>Tax saved this year</span><b>' + C.money(saved) + '</b></li>';
      var segs2 = [
        { label: 'Deducted this year', value: deductible, color: '#10b981' },
        { label: 'Carried forward', value: cf, color: '#6366f1' },
        { label: 'Not deductible', value: homeLoss ? -gain : 0, color: '#94a3b8' }
      ].filter(function (x) { return x.value > 0; });
      if (!segs2.length) segs2 = [{ label: 'Sale proceeds (tax-free)', value: proceeds, color: '#10b981' }];
      C.donut(tool$('[data-donut]'), segs2); C.legend(tool$('[data-legend]'), segs2);
      C.set(tool, 'stackLabel', 'How capital losses are used');
      tool$('[data-stack]').innerHTML = '<li><span>1. Offset capital gains (unlimited)</span><b>—</b></li><li><span>2. Offset ordinary income up to ' + C.money(lossLimit) + '/yr</span><b>' + C.money(deductible) + '</b></li><li><span>3. Carry the rest forward indefinitely</span><b>' + C.money(cf) + '</b></li>';
      C.set(tool, 'compare', 'Your marginal federal bracket is ' + Math.round(base.marginal * 100) + '%, so each $1,000 of deductible loss saves about ' + C.money(base.marginal * 1000) + ' in federal tax. Mind the 30-day wash-sale rule if you buy back the same investment.');
    }
  });

  function rowsHtml(rows) {
    return rows.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('');
  }
})();
