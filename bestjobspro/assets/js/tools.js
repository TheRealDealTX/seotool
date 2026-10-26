/* Best Jobs Pro career tools. Each widget is a [data-tool] element rendered by inc/tools.php. */
(function () {
  'use strict';

  // 2026 federal figures (estimates are labelled as such on the page).
  var BRACKETS = {
    single:  [[12400, .10], [50400, .12], [105700, .22], [201775, .24], [256225, .32], [640600, .35], [Infinity, .37]],
    married: [[24800, .10], [100800, .12], [211400, .22], [403550, .24], [512450, .32], [768700, .35], [Infinity, .37]],
    head:    [[17700, .10], [67450, .12], [105700, .22], [201750, .24], [256200, .32], [640600, .35], [Infinity, .37]]
  };
  var STD = { single: 16100, married: 32200, head: 24150 };
  var SS_BASE = 184500;
  var ADDL_MED = { single: 200000, married: 250000, head: 200000 };

  function incomeTax(taxable, status) {
    var tax = 0, prev = 0, b = BRACKETS[status] || BRACKETS.single;
    taxable = Math.max(0, taxable);
    for (var i = 0; i < b.length && taxable > prev; i++) {
      tax += (Math.min(taxable, b[i][0]) - prev) * b[i][1];
      prev = b[i][0];
    }
    return tax;
  }

  function money(n, cents) {
    if (!isFinite(n)) return '-';
    return (n < 0 ? '-$' : '$') + Math.abs(n).toLocaleString('en-US', { minimumFractionDigits: cents ? 2 : 0, maximumFractionDigits: cents ? 2 : 0 });
  }
  function pct(n) { return isFinite(n) ? Math.round(n * 100) + '%' : '-'; }
  function val(form, name) { var el = form.elements[name]; var v = parseFloat(el && el.value); return isFinite(v) ? v : 0; }
  function out(root, key, text) { var el = root.querySelector('[data-out="' + key + '"]'); if (el) el.textContent = text; return el; }

  // Count numbers up smoothly when they change.
  function animateTo(el, target, fmt) {
    if (!el) return;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var from = parseFloat(el.getAttribute('data-v')) || 0;
    el.setAttribute('data-v', target);
    if (reduce || !isFinite(target)) { el.textContent = fmt(target); return; }
    var t0 = null, dur = 450;
    function step(t) {
      if (!t0) t0 = t;
      var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(from + (target - from) * e);
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function show(root, key, n, fmt) { animateTo(root.querySelector('[data-out="' + key + '"]'), n, fmt || money); }

  var TOOLS = {};

  TOOLS.paycheck = function (root) {
    var f = root.querySelector('form');
    function sync() {
      var hourly = f.elements.mode.value === 'hourly';
      ['rate', 'hours', 'ot'].forEach(function (n) { f.elements[n].closest('.tfield').hidden = !hourly; });
      f.elements.salary.closest('.tfield').hidden = hourly;
    }
    function calc() {
      sync();
      var status = f.elements.filing.value, weeks = Math.min(52, val(f, 'weeks'));
      var gross, hours;
      if (f.elements.mode.value === 'hourly') {
        var r = val(f, 'rate');
        hours = val(f, 'hours') + val(f, 'ot');
        gross = (r * val(f, 'hours') + r * 1.5 * val(f, 'ot')) * weeks;
      } else {
        gross = val(f, 'salary');
        hours = 40;
      }
      var fed = incomeTax(gross - STD[status], status);
      var fica = Math.min(gross, SS_BASE) * .062 + gross * .0145 + Math.max(0, gross - ADDL_MED[status]) * .009;
      var net = gross - fed - fica;
      show(root, 'gross', gross); show(root, 'net', net);
      show(root, 'month', net / 12); show(root, 'biweek', net / 26); show(root, 'week', net / 52);
      show(root, 'hourly', hours && weeks ? net / (hours * weeks) : 0, function (n) { return money(n, true); });
      out(root, 'fed', money(fed)); out(root, 'fica', money(fica)); out(root, 'netpct', gross ? pct(net / gross) : '');
      var bar = root.querySelector('[data-out="bar"]');
      if (bar && gross > 0) {
        bar.children[0].style.width = (net / gross * 100) + '%';
        bar.children[1].style.width = (fed / gross * 100) + '%';
        bar.children[2].style.width = (fica / gross * 100) + '%';
      }
    }
    f.addEventListener('input', calc); f.addEventListener('change', calc); calc();
  };

  TOOLS['contractor-tax'] = function (root) {
    var f = root.querySelector('form');
    function calc() {
      var status = f.elements.filing.value, income = val(f, 'income'), w2 = val(f, 'w2');
      var profit = Math.max(0, income - val(f, 'expenses'));
      var base = profit * .9235;
      var se = Math.max(0, Math.min(base, SS_BASE - w2)) * .124 + base * .029 + Math.max(0, base + w2 - ADDL_MED[status]) * .009;
      if (profit < 400) se = 0;
      var agi = w2 + profit - se / 2;
      var preQbi = Math.max(0, agi - STD[status]);
      var qbi = Math.min(.2 * Math.max(0, profit - se / 2), .2 * preQbi);
      var incTotal = incomeTax(preQbi - qbi, status);
      var incW2 = incomeTax(w2 - STD[status], status);
      var inc = Math.max(0, incTotal - incW2);
      var total = se + inc;
      show(root, 'profit', profit); show(root, 'se', se); show(root, 'inc', inc);
      show(root, 'total', total); show(root, 'quarter', total / 4);
      show(root, 'per100', income ? total / income * 100 : 0, function (n) { return money(n, true); });
    }
    f.addEventListener('input', calc); f.addEventListener('change', calc); calc();
  };

  TOOLS['freelance-rate'] = function (root) {
    var f = root.querySelector('form');
    function calc() {
      var fee = Math.min(.9, val(f, 'fee') / 100), tax = Math.min(.9, val(f, 'tax') / 100);
      var hrs = val(f, 'hours') * Math.max(0, 52 - val(f, 'weeks'));
      var revenue = (val(f, 'target') + val(f, 'expenses')) / (1 - tax) / (1 - fee);
      var rate = hrs ? revenue / hrs : 0;
      show(root, 'rate', rate, function (n) { return money(n, true); });
      show(root, 'day', rate * 8); show(root, 'rev', revenue); show(root, 'fees', revenue * fee);
      show(root, 'hrs', hrs, function (n) { return Math.round(n).toLocaleString('en-US'); });
      show(root, 'w2', Math.max(0, (revenue * (1 - fee) - val(f, 'expenses')) / 1.25));
    }
    f.addEventListener('input', calc); calc();
  };

  TOOLS['vacancy-cost'] = function (root) {
    var f = root.querySelector('form');
    function calc() {
      var perDay = val(f, 'salary') * Math.max(1, val(f, 'multiplier')) / 260;
      var vacancy = perDay * val(f, 'days') * 5 / 7;
      var hr = val(f, 'hrHours') * val(f, 'hrRate');
      var total = vacancy + hr;
      var agency = perDay * val(f, 'agencyDays') * 5 / 7 + hr * .25;
      var saved = Math.max(0, total - agency);
      show(root, 'perday', perDay); show(root, 'vacancy', vacancy); show(root, 'hr', hr);
      show(root, 'bad', val(f, 'salary') * .3); show(root, 'total', total); show(root, 'saved', saved);
      var c = root.querySelector('[data-out="compare"]');
      if (c && total > 0) {
        c.querySelector('.compare__a').style.width = '100%';
        c.querySelector('.compare__b').style.width = Math.max(4, agency / total * 100) + '%';
      }
    }
    f.addEventListener('input', calc); calc();
  };

  var STOP = ('a an and are as at be by for from has have in is it its of on or that the to was were will with you your we our ' +
    'this they their them who what when where which while can may must should would could able about above after all also any ' +
    'both but each etc every have how if into more most not other out over per such than then there these through under up ' +
    'us very via well within without work working job jobs role position candidate candidates ideal including include includes ' +
    'looking seeking join team company opportunity responsibilities requirements required preferred qualifications plus strong ' +
    'excellent ability skills skill experience years year new day days time make help ensure using use based provide like ' +
    'related other others duties apply applicants equal employer employment status benefits pay offer offers please').split(' ');
  var STOPSET = {}; STOP.forEach(function (w) { STOPSET[w] = 1; });

  function words(text) {
    return (text.toLowerCase().replace(/[^a-z0-9+#./ -]+/g, ' ').match(/[a-z0-9+#][a-z0-9+#.\/-]*[a-z0-9+#]|[a-z0-9]/g) || []);
  }
  function keyTerms(text) {
    var w = words(text), counts = {};
    for (var i = 0; i < w.length; i++) {
      var a = w[i];
      if (!STOPSET[a] && a.length > 2 && !/^\d+$/.test(a)) counts[a] = (counts[a] || 0) + 1;
      if (i + 1 < w.length) {
        var b = w[i + 1];
        if (!STOPSET[a] && !STOPSET[b] && a.length > 2 && b.length > 2) {
          var bg = a + ' ' + b; counts[bg] = (counts[bg] || 0) + 1.6;
        }
      }
    }
    var list = Object.keys(counts).filter(function (k) { return counts[k] >= (k.indexOf(' ') > 0 ? 3.2 : 1); });
    list.sort(function (x, y) { return counts[y] - counts[x]; });
    // Drop single words already covered by a chosen phrase.
    var picked = [];
    list.forEach(function (k) {
      if (picked.length >= 24) return;
      if (k.indexOf(' ') < 0 && picked.some(function (p) { return p.indexOf(' ') > 0 && p.split(' ').indexOf(k) >= 0; })) return;
      picked.push(k);
    });
    return picked;
  }

  TOOLS['resume-keywords'] = function (root) {
    var f = root.querySelector('form'), res = root.querySelector('.tool__out');
    function chip(t) { var s = document.createElement('span'); s.className = 'chip'; s.textContent = t; return s; }
    function scan() {
      var jd = f.elements.jd.value, cv = ' ' + words(f.elements.cv.value).join(' ') + ' ';
      if (jd.trim().length < 40 || cv.trim().length < 40) {
        res.hidden = false;
        out(root, 'verdict', 'Paste both texts first');
        out(root, 'summary', 'Add the full job description and your résumé (at least a few lines each).');
        return;
      }
      var terms = keyTerms(jd), have = [], miss = [];
      terms.forEach(function (t) { (cv.indexOf(' ' + t + ' ') >= 0 || cv.indexOf(' ' + t + 's ') >= 0 ? have : miss).push(t); });
      var score = terms.length ? have.length / terms.length : 0;
      res.hidden = false;
      var h = root.querySelector('[data-out="have"]'), m = root.querySelector('[data-out="miss"]');
      h.innerHTML = ''; m.innerHTML = '';
      have.forEach(function (t) { h.appendChild(chip(t)); });
      miss.forEach(function (t) { m.appendChild(chip(t)); });
      if (!have.length) h.appendChild(chip('none yet'));
      if (!miss.length) m.appendChild(chip('nothing missing'));
      animateTo(root.querySelector('[data-out="score"]'), score * 100, function (n) { return Math.round(n) + '%'; });
      var ring = root.querySelector('.ring__val');
      if (ring) ring.style.strokeDashoffset = String(326.7 * (1 - score));
      out(root, 'verdict', score >= .75 ? 'Strong match' : score >= .5 ? 'Good start' : 'Needs tailoring');
      out(root, 'summary', 'You match ' + have.length + ' of the ' + terms.length + ' most important terms in this posting.' +
        (miss.length ? ' Work the true ones into your summary and bullet points.' : ''));
    }
    root.querySelector('[data-action="scan"]').addEventListener('click', scan);
    root.querySelector('[data-action="sample"]').addEventListener('click', function () {
      f.elements.jd.value = 'Administrative Assistant - Southlake, TX. We are hiring an administrative assistant to support our office team. ' +
        'Responsibilities: answer phones, schedule appointments, data entry, maintain filing systems, process invoices in QuickBooks, ' +
        'prepare reports in Microsoft Excel and Microsoft Word, and provide excellent customer service. Requirements: 2+ years of office ' +
        'administration, strong data entry speed and accuracy, Microsoft Excel, QuickBooks experience, calendar management, ' +
        'customer service skills and attention to detail. Bilingual Spanish a plus.';
      f.elements.cv.value = 'Office assistant with 3 years of experience answering multi-line phones, scheduling appointments and ' +
        'calendar management for a busy medical office. Data entry of 500+ patient records per week with 99% accuracy. ' +
        'Created weekly reports in Microsoft Excel. Customer service award 2025. Skills: Microsoft Word, Microsoft Excel, typing 65 WPM.';
      scan();
    });
  };

  TOOLS['job-quiz'] = function (root) {
    var form = root.querySelector('.quiz'), result = root.querySelector('.quiz__result');
    var data = JSON.parse(root.querySelector('.quiz-data').textContent);
    var steps = form.querySelectorAll('.quiz__q'), bar = form.querySelector('.quiz__progress span');
    var BLURB = {
      office: 'You like structure, accuracy and keeping things running. Office and administrative roles reward exactly that, with steady weekday hours.',
      labor: 'You are energetic and like seeing the work get done. Warehouse, production and general labor roles often start fast and offer overtime.',
      trades: 'You like building, fixing and getting better at a craft. Skilled trades pay more as your skills grow and are in demand across Texas.',
      customer: 'You are good with people and stay calm under pressure. Customer service, food service and hospitality roles put that to work.',
      driving: 'You value independence and like being on the move. Driving roles, especially with a CDL, are some of the most in-demand jobs in Texas.'
    };
    function go(i) {
      steps.forEach(function (s, k) { s.hidden = k !== i; });
      bar.style.width = (i / steps.length * 100) + '%';
      var first = steps[i] && steps[i].querySelector('input');
      if (first && i > 0) first.focus({ preventScroll: true });
    }
    function finish() {
      var tally = {};
      Object.keys(data.cats).forEach(function (c) { tally[c] = 0; });
      steps.forEach(function (s) { var c = s.querySelector('input:checked'); if (c) tally[c.value]++; });
      var ranked = Object.keys(tally).sort(function (a, b) { return tally[b] - tally[a]; });
      var top = ranked[0];
      bar.style.width = '100%';
      form.hidden = true; result.hidden = false;
      out(root, 'cat', data.cats[top]);
      out(root, 'blurb', BLURB[top]);
      var bars = root.querySelector('[data-out="bars"]'); bars.innerHTML = '';
      ranked.forEach(function (c) {
        var row = document.createElement('div'); row.className = 'qbar';
        row.innerHTML = '<span></span><i><b></b></i><em></em>';
        row.children[0].textContent = data.cats[c];
        row.children[2].textContent = Math.round(tally[c] / steps.length * 100) + '%';
        bars.appendChild(row);
        requestAnimationFrame(function () { row.querySelector('b').style.width = (tally[c] / steps.length * 100) + '%'; });
      });
      var ul = root.querySelector('[data-out="jobs"]'); ul.innerHTML = '';
      (data.jobs[top] || []).concat(data.jobs[ranked[1]] || []).slice(0, 6).forEach(function (j) {
        var li = document.createElement('li'); li.textContent = j; ul.appendChild(li);
      });
    }
    form.addEventListener('change', function (e) {
      var s = e.target.closest('.quiz__q'), i = +s.getAttribute('data-step');
      setTimeout(function () { i + 1 < steps.length ? go(i + 1) : finish(); }, 260);
    });
    root.querySelector('[data-action="restart"]').addEventListener('click', function () {
      form.reset(); form.hidden = false; result.hidden = true; go(0);
    });
    go(0);
  };

  document.querySelectorAll('[data-tool]').forEach(function (root) {
    var fn = TOOLS[root.getAttribute('data-tool')];
    if (fn) { try { fn(root); } catch (err) { if (window.console) console.error(err); } }
  });
})();
