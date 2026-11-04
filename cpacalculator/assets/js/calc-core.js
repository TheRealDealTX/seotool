/* CPA Calculator — shared tax engine + UI helpers.
 * Tax tables come from window.TAX (inlined by PHP from app/data/tax.json),
 * so the PHP pages and the JavaScript calculators share a single source. */
(function () {
  'use strict';
  var T = window.TAX || { default: 2026, years: {} };

  var CPA = {
    year: function (y) { return T.years[String(y || T.default)] || T.years[String(T.default)]; },
    defaultYear: T.default,

    /* ---------- formatting ---------- */
    money: function (n, dp) {
      if (!isFinite(n)) n = 0;
      var neg = n < 0; n = Math.abs(n);
      var s = n.toLocaleString('en-US', { minimumFractionDigits: dp || 0, maximumFractionDigits: dp || 0 });
      return (neg ? '−$' : '$') + s;
    },
    pct: function (n, dp) { if (!isFinite(n)) n = 0; return (n * 100).toFixed(dp == null ? 1 : dp) + '%'; },
    num: function (v) {
      if (typeof v === 'number') return v;
      var n = parseFloat(String(v || '').replace(/[^0-9.\-]/g, ''));
      return isFinite(n) ? n : 0;
    },
    clamp: function (n, a, b) { return Math.min(b, Math.max(a, n)); },

    /* ---------- core tax math ---------- */
    stdDeduction: function (status, y, seniors) {
      var d = CPA.year(y);
      return d.std[status] + (seniors || 0) * d.addl65[status];
    },
    /* OBBBA senior deduction ($6,000 per person 65+, phases out at 6% of MAGI over threshold). */
    seniorDeduction: function (status, y, seniors, magi) {
      var d = CPA.year(y);
      if (!seniors || !d.senior) return 0;
      var per = Math.max(0, d.senior.amount - Math.max(0, magi - d.senior.phaseStart[status]) * d.senior.rate);
      return per * seniors;
    },
    bracketTax: function (taxable, status, y) {
      var br = CPA.year(y).brackets[status];
      var prev = 0, tax = 0, layers = [], marginal = br[0][1];
      taxable = Math.max(0, taxable);
      for (var i = 0; i < br.length; i++) {
        var top = br[i][0] == null ? Infinity : br[i][0];
        var rate = br[i][1];
        var amt = Math.max(0, Math.min(taxable, top) - prev);
        layers.push({ from: prev, to: top, rate: rate, amount: amt, tax: amt * rate });
        tax += amt * rate;
        if (taxable > prev) marginal = rate;
        prev = top;
      }
      return { tax: tax, marginal: marginal, layers: layers };
    },
    /* Ordinary income taxed in brackets; qualified dividends / LTCG stacked on top at 0/15/20%. */
    incomeTax: function (ordinaryTaxable, prefIncome, status, y) {
      ordinaryTaxable = Math.max(0, ordinaryTaxable);
      prefIncome = Math.max(0, prefIncome || 0);
      var ord = CPA.bracketTax(ordinaryTaxable, status, y);
      var lt = CPA.year(y).ltcg[status], prev = 0, start = ordinaryTaxable, end = ordinaryTaxable + prefIncome, cg = 0;
      for (var i = 0; i < lt.length; i++) {
        var top = lt[i][0] == null ? Infinity : lt[i][0];
        var lo = Math.max(start, prev), hi = Math.min(end, top);
        if (hi > lo) cg += (hi - lo) * lt[i][1];
        prev = top;
      }
      return { tax: ord.tax + cg, ordinaryTax: ord.tax, prefTax: cg, marginal: ord.marginal, layers: ord.layers };
    },
    fica: function (wages, status, y) {
      var d = CPA.year(y);
      var ss = Math.min(Math.max(0, wages), d.ssWageBase) * 0.062;
      var med = Math.max(0, wages) * 0.0145;
      var addl = Math.max(0, wages - d.addlMedicare[status]) * 0.009;
      return { ss: ss, medicare: med, addl: addl, total: ss + med + addl };
    },
    /* Schedule SE. w2Wages reduce the room left under the Social Security wage base. */
    seTax: function (netProfit, status, y, w2Wages) {
      var d = CPA.year(y);
      w2Wages = Math.max(0, w2Wages || 0);
      var base = Math.max(0, netProfit) * 0.9235;
      if (base < 400) return { base: base, ss: 0, medicare: 0, addl: 0, total: 0, half: 0 };
      var ssRoom = Math.max(0, d.ssWageBase - w2Wages);
      var ss = Math.min(base, ssRoom) * 0.124;
      var med = base * 0.029;
      var addl = Math.max(0, base + w2Wages - d.addlMedicare[status]) * 0.009 - Math.max(0, w2Wages - d.addlMedicare[status]) * 0.009;
      addl = Math.max(0, addl);
      var total = ss + med + addl;
      return { base: base, ss: ss, medicare: med, addl: addl, total: total, half: (ss + med) / 2 };
    },
    /* Simplified §199A: 20% of qualified business income, capped at 20% of taxable income
       before QBI less net capital gains. Above the threshold a phase-in can apply (noted in UI). */
    qbi: function (qbiIncome, taxableBeforeQbi, prefIncome, status, y) {
      var cap = Math.max(0, taxableBeforeQbi - (prefIncome || 0)) * 0.2;
      return Math.max(0, Math.min(Math.max(0, qbiIncome) * 0.2, cap));
    },
    ctc: function (kids, agi, status, y) {
      var d = CPA.year(y).ctc;
      var full = kids * d.amount;
      var reduce = Math.ceil(Math.max(0, agi - d.phaseStart[status]) / 1000) * 50;
      return Math.max(0, full - reduce);
    },
    /* One-stop federal estimate used by several tools. */
    estimate: function (o) {
      var y = o.year || T.default, s = o.status || 'single';
      var w2 = o.wages || 0, se = Math.max(0, (o.seIncome || 0) - (o.seExpenses || 0));
      var seT = CPA.seTax(se, s, y, w2);
      var other = o.otherIncome || 0, pref = (o.ltcg || 0) + (o.qualDiv || 0);
      var stcg = o.stcg || 0;
      var adjustments = (o.pretax || 0) + (o.hsa || 0) + seT.half + (o.otherAdjustments || 0);
      var gross = w2 + se + other + pref + stcg;
      var agi = Math.max(0, gross - adjustments);
      var std = CPA.stdDeduction(s, y, o.seniors || 0);
      var ded = o.itemized && o.itemized > std ? o.itemized : std;
      // OBBBA tips, overtime and senior deductions require a joint return if married (not allowed for MFS).
      var below = s === 'mfs' ? 0 : (o.tips ? Math.min(o.tips, CPA.year(y).tipsMax) : 0) +
                  (o.overtime ? Math.min(o.overtime, CPA.year(y).overtimeMax[s]) : 0) +
                  CPA.seniorDeduction(s, y, o.seniors || 0, agi);
      var beforeQbi = Math.max(0, agi - ded - below);
      var qbiDed = o.noQbi ? 0 : CPA.qbi(se, beforeQbi, pref, s, y);
      var taxable = Math.max(0, beforeQbi - qbiDed);
      var ordTaxable = Math.max(0, taxable - pref);
      var it = CPA.incomeTax(ordTaxable, Math.min(pref, taxable), s, y);
      var credits = (o.credits || 0) + (o.kids ? CPA.ctc(o.kids, agi, s, y) : 0);
      var incomeTax = Math.max(0, it.tax - credits);
      var fica = CPA.fica(w2, s, y);
      var niit = Math.max(0, Math.min(pref + stcg + (o.netInvestment || 0), agi - CPA.year(y).niit[s])) * 0.038;
      var total = incomeTax + seT.total + niit;
      return {
        year: y, status: s, gross: gross, agi: agi, deduction: ded, usedItemized: ded !== std, std: std,
        belowLine: below, qbi: qbiDed, taxable: taxable, incomeTaxBeforeCredits: it.tax, credits: Math.min(credits, it.tax),
        incomeTax: incomeTax, marginal: it.marginal, layers: it.layers, prefTax: it.prefTax,
        se: seT, fica: fica, niit: niit, totalFederal: total,
        effective: gross > 0 ? total / gross : 0,
        effectiveIncome: gross > 0 ? incomeTax / gross : 0
      };
    },

    /* ---------- UI helpers ---------- */
    $: function (s, r) { return (r || document).querySelector(s); },
    $$: function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); },
    val: function (form, name) {
      var el = form.elements[name];
      if (!el) return 0;
      if (el.type === 'checkbox') return el.checked;
      if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value; return ''; }
      if (el.dataset && el.dataset.money !== undefined || el.inputMode === 'decimal' || el.type === 'number' || el.type === 'range') return CPA.num(el.value);
      return el.value;
    },
    str: function (form, name) { var el = form.elements[name]; if (!el) return ''; if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value; return ''; } return el.value; },
    set: function (root, key, text) { CPA.$$('[data-out="' + key + '"]', root).forEach(function (el) { el.textContent = text; }); },
    /* Animate a money value from its previous number. */
    tween: function (el, to, fmt) {
      if (!el) return;
      fmt = fmt || CPA.money;
      var from = parseFloat(el.dataset.v || '0');
      el.dataset.v = to;
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = fmt(to); return; }
      var t0 = null, dur = 450;
      cancelAnimationFrame(el._raf);
      function step(t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - p, 3);
        el.textContent = fmt(from + (to - from) * e);
        if (p < 1) el._raf = requestAnimationFrame(step);
      }
      el._raf = requestAnimationFrame(step);
    },
    big: function (root, key, to, fmt) { CPA.$$('[data-out="' + key + '"]', root).forEach(function (el) { CPA.tween(el, to, fmt); }); },
    /* Donut: segments [{label, value, color}] drawn into an <svg data-donut>. */
    donut: function (svg, segs) {
      if (!svg) return;
      var total = segs.reduce(function (a, s) { return a + Math.max(0, s.value); }, 0) || 1;
      var r = 42, c = 2 * Math.PI * r, off = 0, html = '<circle cx="50" cy="50" r="' + r + '" class="donut-track"/>';
      segs.forEach(function (s) {
        var len = Math.max(0, s.value) / total * c;
        html += '<circle cx="50" cy="50" r="' + r + '" stroke="' + s.color + '" stroke-dasharray="' + len + ' ' + (c - len) +
          '" stroke-dashoffset="' + (-off) + '" class="donut-seg"><title>' + s.label + ': ' + CPA.money(s.value) + '</title></circle>';
        off += len;
      });
      svg.innerHTML = html;
    },
    legend: function (el, segs) {
      if (!el) return;
      el.innerHTML = segs.map(function (s) {
        return '<li><i style="background:' + s.color + '"></i><span>' + s.label + '</span><b>' + CPA.money(s.value) + '</b></li>';
      }).join('');
    },
    /* Bracket staircase: shows how much of the income falls in each bracket. */
    brackets: function (el, layers) {
      if (!el) return;
      var max = layers.reduce(function (a, l) { return Math.max(a, l.amount); }, 1);
      el.innerHTML = layers.map(function (l) {
        var w = l.amount / max * 100;
        var range = CPA.money(l.from) + (l.to === Infinity ? '+' : ' – ' + CPA.money(l.to));
        return '<div class="br-row' + (l.amount > 0 ? ' on' : '') + '"><span class="br-rate">' + Math.round(l.rate * 100) + '%</span>' +
          '<span class="br-bar"><span style="width:' + w + '%"></span></span><span class="br-amt">' + (l.amount > 0 ? CPA.money(l.tax) : '—') +
          '</span><span class="br-range">' + range + '</span></div>';
      }).join('');
    },
    /* Wire a calculator form: recalc on input, format money fields, restore from URL hash, share link. */
    bind: function (form, fn) {
      if (!form) return;
      var run = function () { try { fn(form); } catch (e) { if (window.console) console.error(e); } };
      CPA.$$('input[data-money]', form).forEach(function (el) {
        el.addEventListener('blur', function () { if (el.value !== '') el.value = CPA.num(el.value).toLocaleString('en-US'); });
        el.addEventListener('focus', function () { if (el.value !== '') el.value = String(CPA.num(el.value)); });
      });
      // Restore from ?query (shareable results)
      try {
        var q = new URLSearchParams(location.search);
        q.forEach(function (v, k) {
          var el = form.elements[k];
          if (!el) return;
          if (el.length && !el.tagName) { for (var i = 0; i < el.length; i++) el[i].checked = el[i].value === v; }
          else if (el.type === 'checkbox') el.checked = v === '1';
          else el.value = v;
        });
      } catch (e) {}
      form.addEventListener('input', run);
      form.addEventListener('change', run);
      form.addEventListener('submit', function (e) { e.preventDefault(); run(); });
      CPA.$$('[data-range-for]', form).forEach(function (r) {
        var t = form.elements[r.dataset.rangeFor];
        if (!t) return;
        r.addEventListener('input', function () { t.value = Number(r.value).toLocaleString('en-US'); run(); });
        t.addEventListener('input', function () { r.value = CPA.num(t.value); });
        r.value = CPA.num(t.value);
      });
      var tool = form.closest('.tool');
      if (tool) {
        CPA.$$('[data-share]', tool).forEach(function (b) {
          b.addEventListener('click', function () {
            var p = new URLSearchParams();
            CPA.$$('input,select', form).forEach(function (el) {
              if (!el.name || el.type === 'range') return;
              if (el.type === 'radio') { if (el.checked) p.set(el.name, el.value); }
              else if (el.type === 'checkbox') { if (el.checked) p.set(el.name, '1'); }
              else if (el.value !== '') p.set(el.name, CPA.num(el.value) || el.value);
            });
            var url = location.origin + location.pathname + '?' + p.toString();
            var done = function () { b.dataset.label = b.dataset.label || b.textContent; b.textContent = 'Link copied ✓'; setTimeout(function () { b.textContent = b.dataset.label; }, 1800); };
            if (navigator.clipboard) navigator.clipboard.writeText(url).then(done, function () { prompt('Copy this link', url); });
            else prompt('Copy this link', url);
          });
        });
        CPA.$$('[data-print]', tool).forEach(function (b) { b.addEventListener('click', function () { window.print(); }); });
        CPA.$$('[data-reset]', tool).forEach(function (b) {
          b.addEventListener('click', function () { form.reset(); history.replaceState(null, '', location.pathname); setTimeout(run, 0); });
        });
      }
      run();
    }
  };
  window.CPA = CPA;
})();
