/* Calculator pages: salary calculator, CAT deployment, public adjuster fees, state explorer */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var money = function (n) { return IAS.money(n); };
  var MIN = 30000, MAX = 230000;
  function pos(n) { return Math.max(0, Math.min(100, (n - MIN) / (MAX - MIN) * 100)); }
  function bind(root, fn) { root.addEventListener('input', fn); root.addEventListener('change', fn); fn(); }

  // ---- Salary calculator ----
  var sc = $('salary-calc');
  if (sc && IAS.salary) {
    bind(sc, function () {
      var years = +$('c-years').value;
      var r = IAS.salary.estimate({
        role: sc.querySelector('input[name=role]:checked').value,
        line: $('c-line').value,
        years: years,
        stateIndex: +$('c-state').value,
        designation: $('c-desig').checked,
        bilingual: $('c-bi').checked
      });
      $('c-years-out').textContent = years + (years === 20 ? '+' : '');
      $('c-mid').textContent = money(r.mid);
      $('c-label').textContent = r.label + ' · ' + $('c-state').selectedOptions[0].text;
      $('c-range').textContent = money(r.low) + ' - ' + money(r.high);
      $('c-hour').textContent = money(r.hourly) + '/hr';
      $('c-month').textContent = money(r.monthly);
      $('c-ben').textContent = r.benefits ? '+' + money(r.benefits) : 'None (1099)';
      var diff = (r.mid - 76790) / 76790 * 100;
      $('c-vs').textContent = (diff >= 0 ? '+' : '') + diff.toFixed(0) + '%';
      $('c-note').textContent = r.w2
        ? 'Estimate for a W-2 salary before taxes. Not a job offer.'
        : 'Gross 1099 income before expenses and self-employment tax. Varies heavily with storm activity.';
      $('c-band').style.left = pos(r.low) + '%';
      $('c-band').style.width = (pos(r.high) - pos(r.low)) + '%';
      $('c-pin').style.left = pos(r.mid) + '%';
    });
  }

  // ---- CAT deployment calculator ----
  var cat = $('cat-calc');
  if (cat) {
    cat.querySelectorAll('input[name=fee]').forEach(function (r) {
      r.addEventListener('change', function () {
        $('k-fee').value = r.value;
        if (r.dataset.days) $('k-days').value = r.dataset.days;
        if (r.dataset.cpd) $('k-cpd').value = r.dataset.cpd;
        ['k-fee', 'k-days', 'k-cpd'].forEach(function (id) { IAS.paintRange($(id)); });
      });
    });
    bind(cat, function () {
      var fee = +$('k-fee').value, days = +$('k-days').value, cpd = +$('k-cpd').value;
      var split = +$('k-split').value / 100, exp = +$('k-exp').value, tax = +$('k-tax').value / 100;
      var travel = Math.max(0, +$('k-travel').value || 0);
      // Field days: allow ~1 day in 7 for paperwork, re-inspections and travel inside the deployment
      var workDays = days * 6 / 7;
      var claims = Math.round(workDays * cpd);
      var gross = claims * fee;
      var share = gross * split;
      var costs = days * exp + travel;
      var pretax = share - costs;
      var taxes = Math.max(0, pretax) * tax;
      var net = pretax - taxes;
      $('k-fee-out').textContent = money(fee);
      $('k-days-out').textContent = days + ' days';
      $('k-cpd-out').textContent = cpd.toFixed(1);
      $('k-split-out').textContent = Math.round(split * 100) + '%';
      $('k-exp-out').textContent = money(exp);
      $('k-tax-out').textContent = Math.round(tax * 100) + '%';
      $('k-net').textContent = money(net);
      $('k-net2').textContent = money(net);
      $('k-perday').textContent = money(net / days) + ' per deployment day';
      $('k-claims').textContent = claims.toLocaleString('en-US');
      $('k-gross').textContent = money(gross);
      $('k-share').textContent = money(share);
      $('k-costs').textContent = '-' + money(costs);
      $('k-taxes').textContent = '-' + money(taxes);
      var parts = [[Math.max(0, net), '#be9967'], [taxes, '#8f6c3f'], [Math.min(costs, share), '#5d5d62'], [gross - share, '#2d2d31']];
      $('k-stack').innerHTML = gross > 0 ? parts.map(function (p) {
        return '<span style="display:block;height:100%;width:' + (p[0] / gross * 100) + '%;background:' + p[1] + ';transition:width .5s"></span>';
      }).join('') : '';
    });
  }

  // ---- Public adjuster fee calculator ----
  var pa = $('pa-calc');
  if (pa) {
    var CAPS = { none: null, tx: 10, fl: 20, fle: 10 };
    bind(pa, function () {
      var capKey = pa.querySelector('input[name=cap]:checked').value;
      var cap = CAPS[capKey];
      var want = +$('p-fee').value;
      var rate = cap !== null ? Math.min(want, cap) : want;
      var offer = Math.max(0, +$('p-offer').value || 0);
      var settle = Math.max(0, +$('p-settle').value || 0);
      var fee = settle * rate / 100;
      var net = settle - fee;
      $('p-fee-out').textContent = want + '%';
      $('p-cap-hint').textContent = cap !== null && want > cap
        ? 'Capped at ' + cap + '% under this state rule.'
        : 'Fees above the state cap are reduced automatically.';
      $('p-feeamt').textContent = money(fee);
      $('p-rate').textContent = rate + '% of ' + money(settle) + (cap !== null ? ' · cap ' + cap + '%' : '');
      $('p-net').textContent = money(net);
      var gain = net - offer;
      $('p-gain').textContent = (gain >= 0 ? '+' : '-') + money(Math.abs(gain));
      $('p-break').textContent = offer > 0 ? money(offer / (1 - rate / 100)) : '-';
      var count = +$('p-count').value, split = +$('p-split').value / 100;
      $('p-count-out').textContent = count;
      $('p-split-out').textContent = Math.round(split * 100) + '%';
      $('p-annual').textContent = money(fee * count * split);
    });
  }

  // ---- State explorer ----
  var table = $('state-table');
  if (table) {
    var tbody = table.querySelector('tbody');
    var rows = Array.prototype.slice.call(tbody.rows);
    var search = $('st-search'), catSel = $('st-cat'), count = $('st-count');
    var sortKey = 'name', dir = 1;
    function apply() {
      var q = search.value.trim().toLowerCase(), c = catSel.value, shown = 0;
      rows.forEach(function (r) {
        var ok = (!q || r.dataset.name.toLowerCase().indexOf(q) > -1 || r.dataset.code.toLowerCase() === q) && (!c || r.dataset.cat === c);
        r.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      count.textContent = 'Showing ' + shown + ' of ' + rows.length + ' states.';
    }
    table.querySelectorAll('th button').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-sort');
        dir = (k === sortKey) ? -dir : (k === 'name' ? 1 : -1);
        sortKey = k;
        var order = { H: 3, M: 2, L: 1 };
        rows.sort(function (a, z) {
          var x = a.dataset[k], y = z.dataset[k];
          if (k === 'cat') { x = order[x]; y = order[y]; }
          else if (k !== 'name') { x = +x; y = +y; }
          return (x > y ? 1 : x < y ? -1 : 0) * dir;
        });
        rows.forEach(function (r) { tbody.appendChild(r); });
      });
    });
    search.addEventListener('input', apply);
    catSel.addEventListener('change', apply);
    apply();
    // Highlight a state linked by hash (#TX)
    if (location.hash.length === 3) {
      var row = document.getElementById(location.hash.slice(1).toUpperCase());
      if (row) { row.style.background = 'rgba(190,153,103,.25)'; setTimeout(function () { row.scrollIntoView({ block: 'center' }); }, 300); }
    }
  }
})();
