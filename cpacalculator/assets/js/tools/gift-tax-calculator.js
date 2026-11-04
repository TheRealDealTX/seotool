(function () {
  var form = document.getElementById('gift-form');
  if (!form) return;
  var tool = form.closest('.tool'), C = window.CPA;
  var rows = C.$$('[data-row]', form), addBtn = C.$('[data-addrow]', form);

  /* Unified transfer tax on a cumulative amount (estate.brackets in tax.json). */
  function unified(amt, br) {
    var tax = 0, prev = 0;
    for (var i = 0; i < br.length; i++) {
      var top = br[i][0] == null ? Infinity : br[i][0];
      if (amt > prev) tax += (Math.min(amt, top) - prev) * br[i][1];
      prev = top;
    }
    return tax;
  }
  function syncAdd() { addBtn.hidden = rows.every(function (r) { return !r.hidden; }); }
  addBtn.addEventListener('click', function () {
    var next = rows.filter(function (r) { return r.hidden; })[0];
    if (next) { next.hidden = false; var inp = next.querySelector('input'); if (inp) inp.focus(); }
    syncAdd();
  });
  syncAdd();

  CPA.bind(form, function (f) {
    var v = function (n) { return C.val(f, n); };
    var yr = v('year'), d = C.year(yr);
    var ex = d.giftAnnualExclusion, br = d.estate.brackets, exempt = d.estate.exemption, nc = d.giftSpouseNonCitizen;
    // Reveal any hidden rows that hold a value (e.g. restored from a share link).
    rows.forEach(function (r) { var inp = r.querySelector('input'); if (r.hidden && inp && C.num(inp.value) > 0) r.hidden = false; });
    syncAdd();
    var split = !!v('split');
    C.set(tool, 'exhint', 'Each recipient can receive up to ' + C.money(split ? ex * 2 : ex) + (split ? ' from you and your spouse combined' : ' from you') + ' in ' + yr + ' tax-free and without a Form 709.');

    var exclUsed = 0, taxable = 0, total = 0, need709 = false, future = 0, five29 = 0, lines = [];
    rows.forEach(function (r, i) {
      var n = i + 1, amt = Math.max(0, v('g' + n));
      if (!amt) return;
      var type = C.str(f, 't' + n);
      var mine = split ? amt / 2 : amt, e = 0, note = '';
      total += amt;
      if (type === 'future') { e = 0; future += mine; need709 = true; note = 'future interest'; }
      else if (type === '529') {
        // 5-year election: up to 5× the exclusion is spread ratably; any excess is a current-year gift.
        var eligible = Math.min(mine, ex * 5), excess = mine - eligible;
        mine = eligible / 5 + excess;
        e = Math.min(mine, ex); need709 = true; five29 += eligible * 4 / 5; note = '529, 1/5 this year';
      } else e = Math.min(mine, ex);
      var t = Math.max(0, mine - e);
      if (t > 0) need709 = true;
      exclUsed += e; taxable += t;
      lines.push(['Recipient ' + n + (note ? ' (' + note + ')' : ''), t > 0 ? C.money(t) + ' taxable' : 'excluded']);
    });

    var sg = Math.max(0, v('sg')), spouseType = C.str(f, 'spouse'), spouseTaxable = 0, marital = 0, spouseExcl = 0;
    if (spouseType === 'noncitizen') { spouseExcl = Math.min(sg, nc); spouseTaxable = sg - spouseExcl; if (spouseTaxable > 0) need709 = true; }
    else marital = sg;
    taxable += spouseTaxable;
    if (split && total > 0) need709 = true;
    var edmed = Math.max(0, v('edmed'));
    var prior = Math.max(0, v('prior'));

    var credit = unified(exempt, br);
    var usedPrior = Math.min(unified(prior, br), credit);
    var due = Math.max(0, unified(prior + taxable, br) - unified(prior, br) - (credit - usedPrior));
    var usedThis = Math.min(taxable, Math.max(0, exempt - prior));
    var cum = prior + taxable;
    var left = Math.max(0, exempt - cum);

    var big = C.$('[data-out="due"]', tool);
    big.classList.toggle('good', due < 0.5);
    big.classList.toggle('bad', due >= 0.5);
    C.big(tool, 'due', due);
    var sum;
    if (due >= 0.5) sum = 'Your lifetime exemption is exhausted — gift tax is due at up to 40%. Form 709 required.';
    else if (need709) sum = 'No tax due, but you must file Form 709' + (split ? ' (both spouses, to split gifts)' : '') + ' by April 15, ' + (+yr + 1) + '.';
    else sum = 'No tax and no Form 709 needed — every gift is within the exclusions.';
    C.set(tool, 'summary', sum);
    C.set(tool, 'excl', C.money(exclUsed + spouseExcl));
    C.set(tool, 'taxable', C.money(taxable));
    C.set(tool, 'used', C.money(Math.min(cum, exempt)));
    C.set(tool, 'left', C.money(left));

    var meter = C.$('[data-meter]', tool);
    var pPrior = Math.min(100, prior / exempt * 100), pThis = Math.min(100 - pPrior, taxable / exempt * 100);
    meter.innerHTML = '<span style="width:' + pPrior + '%;background:#94a3b8" title="Used in earlier years"></span><span style="width:' + pThis + '%;background:#f59e0b" title="Used this year"></span>';
    meter.setAttribute('aria-label', C.pct(Math.min(1, cum / exempt)) + ' of the ' + C.money(exempt) + ' lifetime exemption used');

    var segs = [
      { label: 'Annual exclusions', value: exclUsed + spouseExcl, color: '#10b981' },
      { label: 'Marital deduction', value: marital, color: '#0e7490' },
      { label: 'Tuition / medical', value: edmed, color: '#6366f1' },
      { label: 'Uses lifetime exemption', value: usedThis, color: '#f59e0b' },
      { label: 'Taxed (over exemption)', value: Math.max(0, taxable - usedThis), color: '#e11d48' }
    ].filter(function (x) { return x.value > 0.5; });
    C.donut(C.$('[data-donut]', tool), segs);
    C.legend(C.$('[data-legend]', tool), segs);

    var out = [['Gifts to individuals', C.money(total)]];
    if (split) out.push(['Your half after gift splitting', C.money(total / 2), 'sub']);
    lines.forEach(function (l) { out.push([l[0], l[1], 'sub']); });
    if (five29) out.push(['529 gifts treated as made in the next 4 years', C.money(five29), 'sub']);
    if (sg) out.push(['Gift to spouse', spouseType === 'citizen' ? C.money(sg) + ' deducted' : C.money(spouseTaxable) + ' taxable']);
    if (edmed) out.push(['Tuition / medical paid directly', 'excluded']);
    out.push(['Taxable gifts this year', C.money(taxable)]);
    out.push(['Prior taxable gifts', C.money(prior)]);
    out.push(['Cumulative taxable gifts', C.money(cum)]);
    out.push(['Applicable credit (on ' + C.money(exempt) + ')', C.money(credit)]);
    out.push(['Form 709 required', need709 ? 'Yes' : 'No']);
    C.$('[data-rows]', tool).innerHTML = out.map(function (x) { return '<li' + (x[2] ? ' class="sub"' : '') + '><span>' + x[0] + '</span><b>' + x[1] + '</b></li>'; }).join('') +
      '<li class="total"><span>Gift tax due</span><b>' + C.money(due) + '</b></li>';

    var note = 'Federal gift tax only; Connecticut is the one state with its own gift tax. ';
    if (split) note += 'Splitting applies to all gifts either spouse made this year — your spouse’s own gifts also count half to you. ';
    if (future) note += 'Future-interest gifts get no annual exclusion. ';
    note += 'Not legal advice.';
    C.set(tool, 'note', note);
  });
})();
