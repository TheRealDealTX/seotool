/* Houston Public Adjusters — claim calculators. Each tool is a <form data-tool="name"> that recalculates on input. */
(function () {
  'use strict';
  var usd = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  function $(form, name) { return form.querySelector('[name="' + name + '"]'); }
  function num(form, name) { var el = $(form, name); if (!el) return 0; var v = parseFloat(String(el.value).replace(/[$,%\s]/g, '')); return isFinite(v) ? v : 0; }
  function rows(list) {
    return '<div class="result-rows">' + list.map(function (r) {
      return '<div class="result-row' + (r[2] ? ' ' + r[2] : '') + '"><span>' + r[0] + '</span><b>' + r[1] + '</b></div>';
    }).join('') + '</div>';
  }
  function bars(list, max) {
    return '<div class="bar-compare">' + list.map(function (b) {
      var w = max > 0 ? Math.max(2, Math.min(100, b[1] / max * 100)) : 0;
      return '<div class="bar' + (b[2] ? ' ' + b[2] : '') + '"><i style="width:' + w + '%"></i><span>' + b[0] + ': ' + usd.format(b[1]) + '</span></div>';
    }).join('') + '</div>';
  }
  function cta(text) {
    return '<p style="margin:16px 0 0">' + text + ' <a href="tel:+18325035866" style="color:#ffa24a;font-weight:700">Call (832) 503-5866</a> or <a href="#" data-open-lead style="color:#ffa24a;font-weight:700">request a free review</a>.</p>';
  }

  var tools = {
    settlement: function (f) {
      var rcv = num(f, 'rcv'), depPct = num(f, 'dep_pct') / 100, ded = num(f, 'deductible'), prior = num(f, 'prior');
      var policy = $(f, 'policy').value;
      var dep = rcv * depPct;
      var acv = rcv - dep;
      var first = Math.max(0, acv - ded - prior);
      var recoverable = policy === 'rcv' ? dep : 0;
      var total = Math.max(0, rcv - (policy === 'rcv' ? 0 : dep) - ded - prior);
      return '<h3>Your estimated settlement</h3>' + rows([
        ['Replacement cost value (RCV)', usd.format(rcv)],
        ['Depreciation withheld', '&minus;' + usd.format(dep)],
        ['Actual cash value (ACV)', usd.format(acv)],
        ['Deductible', '&minus;' + usd.format(ded)],
        ['Prior payments', '&minus;' + usd.format(prior)],
        ['First check (ACV payment)', usd.format(first)],
        ['Recoverable depreciation after repairs', policy === 'rcv' ? usd.format(recoverable) : '$0 (ACV policy)'],
        ['Total you should receive', usd.format(total), 'total']
      ]) + bars([['First check', first], ['Total after repairs', total, 'alt']], Math.max(total, 1)) +
        cta(dep > rcv * 0.3 ? 'Depreciation over 30% is often worth challenging.' : 'Not sure the carrier’s RCV is complete?');
    },

    fee: function (f) {
      var offer = num(f, 'offer'), withPa = num(f, 'with_pa'), pct = Math.min(num(f, 'fee_pct'), 100) / 100;
      var basis = $(f, 'basis').value;
      var feeBase = basis === 'increase' ? Math.max(0, withPa - offer) : withPa;
      var fee = feeBase * pct;
      var net = withPa - fee;
      var gain = net - offer;
      return '<h3>Net comparison</h3>' + rows([
        ['Carrier offer without representation', usd.format(offer)],
        ['Settlement with a public adjuster', usd.format(withPa)],
        ['Public adjuster fee (' + Math.round(pct * 1000) / 10 + '% of ' + (basis === 'increase' ? 'the increase' : 'the settlement') + ')', '&minus;' + usd.format(fee)],
        ['You keep with a public adjuster', usd.format(net)],
        [gain >= 0 ? 'Net gain from hiring' : 'Net difference', (gain >= 0 ? '+' : '&minus;') + usd.format(Math.abs(gain)), 'total']
      ]) + bars([['Without PA', offer, 'alt'], ['With PA (after fee)', net]], Math.max(offer, net, 1)) +
        '<p style="margin:14px 0 0">Break-even: the settlement only has to rise above <b style="color:#fff">' + usd.format(basis === 'increase' ? offer : (pct < 1 ? offer / (1 - pct) : offer)) + '</b> for hiring to pay for itself.</p>' +
        cta('Want a realistic estimate of what your claim should be worth?');
    },

    deductible: function (f) {
      var a = num(f, 'coverage_a'), pct = num(f, 'pct') / 100, std = num(f, 'standard'), dmg = num(f, 'damage');
      var hd = a * pct;
      var payHurr = Math.max(0, dmg - hd), payStd = Math.max(0, dmg - std);
      return '<h3>Your windstorm deductible</h3>' + rows([
        ['Dwelling coverage (Coverage A)', usd.format(a)],
        ['Hurricane / named-storm deductible (' + (pct * 100).toFixed(1).replace('.0', '') + '%)', usd.format(hd)],
        ['Your standard all-peril deductible', usd.format(std)],
        ['Estimated damage', usd.format(dmg)],
        ['Insurer pays if a named storm caused it', usd.format(payHurr)],
        ['Insurer pays if the standard deductible applies', usd.format(payStd), 'total']
      ]) + bars([['Named-storm deductible', payHurr, 'alt'], ['Standard deductible', payStd]], Math.max(payHurr, payStd, 1)) +
        (dmg <= hd ? '<p style="margin:14px 0 0">&#9888; Your damage estimate is below the hurricane deductible. Carrier estimates are often low &mdash; a full scope can push a claim over the line.</p>' : '') +
        cta('Was a hurricane deductible applied to non-hurricane damage?');
    },

    depreciation: function (f) {
      var cost = num(f, 'cost'), age = num(f, 'age'), life = Math.max(1, num(f, 'life')), cap = num(f, 'cap') / 100 || 1;
      var pct = Math.min(cap, age / life);
      var dep = cost * pct;
      return '<h3>Depreciation estimate</h3>' + rows([
        ['Replacement cost (new)', usd.format(cost)],
        ['Age / useful life', age + ' of ' + life + ' years'],
        ['Depreciation (' + Math.round(pct * 100) + '%)', '&minus;' + usd.format(dep)],
        ['Actual cash value (ACV)', usd.format(cost - dep), 'total']
      ]) + bars([['ACV', cost - dep, 'alt'], ['Replacement cost', cost]], Math.max(cost, 1)) +
        '<p style="margin:14px 0 0">With a replacement-cost policy, the ' + usd.format(dep) + ' withheld is usually recoverable once the work is done and invoiced.</p>' +
        cta('Carrier depreciating more than this?');
    },

    ale: function (f) {
      var months = num(f, 'months');
      var extra = ['housing', 'meals', 'mileage', 'utilities', 'other'].reduce(function (s, k) { return s + num(f, k); }, 0);
      var normal = num(f, 'normal_housing') + num(f, 'normal_food');
      var monthly = Math.max(0, extra - normal);
      var limit = num(f, 'limit');
      var total = monthly * months;
      return '<h3>Additional living expense estimate</h3>' + rows([
        ['Monthly costs while displaced', usd.format(extra)],
        ['Minus your normal monthly costs', '&minus;' + usd.format(normal)],
        ['Additional cost per month', usd.format(monthly)],
        ['Months displaced', String(months)],
        ['Your Coverage D limit', limit ? usd.format(limit) : 'not entered'],
        ['Estimated ALE claim', usd.format(limit ? Math.min(total, limit) : total), 'total']
      ]) + (limit && total > limit ? '<p style="margin:14px 0 0">&#9888; Your estimate exceeds the Coverage D limit by ' + usd.format(total - limit) + '.</p>' : '') +
        cta('Insurer cutting off ALE before your home is livable?');
    },

    deadline: function (f) {
      var lossV = $(f, 'loss').value, noticeV = $(f, 'notice').value, docsV = $(f, 'docs').value, cat = $(f, 'cat').checked;
      if (!lossV && !noticeV) return '<h3>Your claim timeline</h3><p>Enter at least your date of loss or the date you reported the claim.</p>';
      function d(v) { var p = v.split('-'); return new Date(+p[0], +p[1] - 1, +p[2]); }
      function addDays(dt, n) { var x = new Date(dt); x.setDate(x.getDate() + n); return x; }
      function addBiz(dt, n) { var x = new Date(dt); while (n > 0) { x.setDate(x.getDate() + 1); if (x.getDay() % 6) n--; } return x; }
      function addYears(dt, n) { var x = new Date(dt); x.setFullYear(x.getFullYear() + n); return x; }
      var fmt = function (x) { return x.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); };
      var today = new Date(); today.setHours(0, 0, 0, 0);
      var items = [];
      var ext = cat ? 15 : 0;
      if (lossV) {
        var loss = d(lossV);
        items.push([loss, 'Date of loss', 'Photograph everything, mitigate further damage and report the claim promptly.']);
        items.push([addYears(loss, 1), '1 year after loss', 'Common Texas deadline to report wind/hail damage (required for TWIA coastal policies; many homeowners policies have a similar clause). Check your policy.']);
        items.push([addYears(loss, 2), '2 years after loss', 'A frequent contractual deadline for filing suit on a property claim. Many Texas policies measure it from the date of loss or the date of denial; read the “Suit Against Us” clause.']);
      }
      if (noticeV) {
        var notice = d(noticeV);
        items.push([notice, 'Claim reported', 'Write down your claim number and the adjuster’s name.']);
        items.push([addDays(notice, 15 + ext), (15 + ext) + ' days after notice', 'Insurer must acknowledge the claim, begin its investigation and request the documents it needs (Tex. Ins. Code §542.055).']);
      }
      if (docsV) {
        var docs = d(docsV);
        var decision = addBiz(docs, 15 + ext);
        items.push([docs, 'All requested items provided', 'Keep proof of what you sent and when.']);
        items.push([decision, (15 + ext) + ' business days later', 'Insurer must accept or reject the claim in writing (§542.056). It may extend up to 45 days if it explains why in writing.']);
        items.push([addDays(decision, 45), 'Latest date with a 45-day extension', 'If the insurer notified you it needs more time, this is the outside limit.']);
        items.push([addBiz(decision, 5), '5 business days after approval', 'Payment is due within 5 business days of the insurer accepting the claim (§542.057).']);
      }
      items.sort(function (a, b) { return a[0] - b[0]; });
      return '<h3>Your claim timeline</h3><ul class="timeline-out">' + items.map(function (i) {
        return '<li class="' + (i[0] < today ? 'past' : '') + '"><b>' + fmt(i[0]) + '</b><span><strong style="color:#fff">' + i[1] + '.</strong> ' + i[2] + '</span></li>';
      }).join('') + '</ul>' + cta('Insurer missing these deadlines? Texas law can add interest to late payments.');
    }
  };

  document.querySelectorAll('form[data-tool]').forEach(function (form) {
    var fn = tools[form.dataset.tool];
    var out = document.getElementById(form.dataset.out);
    if (!fn || !out) return;
    function run() { out.innerHTML = fn(form); out.hidden = false; }
    form.addEventListener('input', run);
    form.addEventListener('change', run);
    form.addEventListener('submit', function (e) { e.preventDefault(); run(); });
    // Preset selectors fill other fields (e.g. useful-life presets).
    form.querySelectorAll('[data-fill]').forEach(function (sel) {
      sel.addEventListener('change', function () { if (sel.value) { $(form, sel.dataset.fill).value = sel.value; run(); } });
    });
    run();
  });

  /* Contents inventory builder (saved in this browser only). */
  var inv = document.getElementById('inventory');
  if (inv) {
    var body = inv.querySelector('tbody');
    var totalEl = document.getElementById('inv-total');
    var KEY = 'hpa_inventory';
    var fields = ['room', 'item', 'qty', 'age', 'cost'];
    function addRow(data) {
      data = data || {};
      var tr = document.createElement('tr');
      tr.innerHTML = fields.map(function (k) {
        var t = k === 'qty' || k === 'age' || k === 'cost' ? 'number' : 'text';
        return '<td><input aria-label="' + k + '" data-k="' + k + '" type="' + t + '" min="0" step="any" value="' + String(data[k] == null ? (k === 'qty' ? 1 : '') : data[k]).replace(/"/g, '&quot;') + '"></td>';
      }).join('') + '<td class="line"></td><td><button type="button" class="btn btn-outline" style="padding:.4em .8em" aria-label="Remove row">&times;</button></td>';
      tr.querySelector('button').addEventListener('click', function () { tr.remove(); save(); });
      body.appendChild(tr);
    }
    function read() {
      return Array.prototype.map.call(body.rows, function (tr) {
        var o = {}; tr.querySelectorAll('input').forEach(function (i) { o[i.dataset.k] = i.value; }); return o;
      });
    }
    function save() {
      var data = read(), total = 0;
      Array.prototype.forEach.call(body.rows, function (tr, i) {
        var line = (parseFloat(data[i].qty) || 0) * (parseFloat(data[i].cost) || 0);
        total += line; tr.querySelector('.line').textContent = usd.format(line);
      });
      totalEl.textContent = usd.format(total);
      try { localStorage.setItem(KEY, JSON.stringify(data)); } catch (e) {}
    }
    var saved = null;
    try { saved = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) {}
    (saved && saved.length ? saved : [{ room: 'Living room', item: '65" television', qty: 1, age: 3, cost: 900 }, {}, {}]).forEach(addRow);
    body.addEventListener('input', save);
    document.getElementById('inv-add').addEventListener('click', function () { addRow(); save(); });
    document.getElementById('inv-print').addEventListener('click', function () { window.print(); });
    document.getElementById('inv-clear').addEventListener('click', function () { if (confirm('Clear every row?')) { body.innerHTML = ''; addRow(); save(); } });
    document.getElementById('inv-csv').addEventListener('click', function () {
      var csv = [['Room', 'Item', 'Quantity', 'Age (years)', 'Replacement cost each', 'Line total']].concat(read().map(function (r) {
        return [r.room, r.item, r.qty, r.age, r.cost, (parseFloat(r.qty) || 0) * (parseFloat(r.cost) || 0)];
      })).map(function (r) { return r.map(function (c) { return '"' + String(c == null ? '' : c).replace(/"/g, '""') + '"'; }).join(','); }).join('\n');
      var a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
      a.download = 'contents-inventory.csv';
      document.body.appendChild(a); a.click(); a.remove();
    });
    save();
  }

  /* Hurricane preparedness checklist progress (saved in this browser only). */
  var prep = document.getElementById('prep');
  if (prep) {
    var boxes = prep.querySelectorAll('input[type=checkbox]');
    var bar = document.getElementById('prep-bar'), count = document.getElementById('prep-count');
    var state = {};
    try { state = JSON.parse(localStorage.getItem('hpa_prep') || '{}'); } catch (e) {}
    function update() {
      var done = 0;
      boxes.forEach(function (b) { state[b.id] = b.checked; if (b.checked) done++; });
      bar.style.width = (done / boxes.length * 100) + '%';
      count.textContent = done + ' of ' + boxes.length + ' done';
      try { localStorage.setItem('hpa_prep', JSON.stringify(state)); } catch (e) {}
    }
    boxes.forEach(function (b) { b.checked = !!state[b.id]; b.addEventListener('change', update); });
    document.getElementById('prep-reset').addEventListener('click', function () { boxes.forEach(function (b) { b.checked = false; }); update(); });
    update();
  }
})();
