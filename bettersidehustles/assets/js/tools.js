/* Better Side Hustles — calculator and quiz logic. Each .tool[data-tool]
   recalculates on every input change. */
(function () {
  'use strict';

  var usd = function (n, d) {
    if (!isFinite(n)) return '—';
    var neg = n < 0; n = Math.abs(n);
    var s = n.toLocaleString('en-US', { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
    return (neg ? '−$' : '$') + s;
  };
  var pct = function (n) { return isFinite(n) ? n.toFixed(1) + '%' : '—'; };
  var num = function (n, d) { return isFinite(n) ? n.toLocaleString('en-US', { maximumFractionDigits: d || 0 }) : '—'; };

  // rows: [label, value, emphasis?]; bars: [{label, value}] drawn as a mini chart
  function paint(out, rows, bars, note) {
    var h = '<div class="out-rows">';
    rows.forEach(function (r) {
      h += '<div class="out-row' + (r[2] ? ' is-key' : '') + '"><span>' + r[0] + '</span><b data-count="' + (r[3] || '') + '">' + r[1] + '</b></div>';
    });
    h += '</div>';
    if (bars && bars.length) {
      var max = Math.max.apply(null, bars.map(function (b) { return Math.abs(b.value); })) || 1;
      h += '<div class="out-bars">';
      bars.forEach(function (b) {
        var w = Math.max(2, Math.abs(b.value) / max * 100);
        h += '<div class="out-bar"><span>' + b.label + '</span><i style="--w:' + w.toFixed(1) + '%"' + (b.value < 0 ? ' class="neg"' : '') + '></i><b>' + usd(b.value) + '</b></div>';
      });
      h += '</div>';
    }
    if (note) h += '<p class="out-note">' + note + '</p>';
    out.innerHTML = h;
  }

  // 2026 federal brackets (taxable income upper bounds) and standard deductions.
  var BRACKETS = {
    single:  [[12400, .10], [50400, .12], [105700, .22], [201775, .24], [256225, .32], [640600, .35], [Infinity, .37]],
    married: [[24800, .10], [100800, .12], [211400, .22], [403550, .24], [512450, .32], [768700, .35], [Infinity, .37]],
    hoh:     [[17700, .10], [67450, .12], [105700, .22], [201750, .24], [256200, .32], [640600, .35], [Infinity, .37]]
  };
  var STD = { single: 16100, married: 32200, hoh: 24150 };
  var SS_WAGE_BASE = 184500;
  function incomeTax(taxable, status) {
    var tax = 0, prev = 0;
    BRACKETS[status].some(function (b) {
      if (taxable > prev) tax += (Math.min(taxable, b[0]) - prev) * b[1];
      prev = b[0];
      return taxable <= b[0];
    });
    return Math.max(0, tax);
  }

  var CALC = {
    'income-calculator': function (v) {
      var weekly = v.rate * v.hours;
      var yearGross = weekly * v.weeks;
      var yearNet = (yearGross - v.costs * 12) * (1 - v.tax / 100);
      var month = yearNet / 12;
      var months = month > 0 ? Math.ceil(v.goal / month) : Infinity;
      return {
        rows: [
          ['Gross per week', usd(weekly)],
          ['Take-home per month', usd(month), true, month],
          ['Take-home per year', usd(yearNet), true, yearNet],
          ['Time to reach ' + usd(v.goal), isFinite(months) ? months + (months === 1 ? ' month' : ' months') : 'Never at this pace']
        ],
        bars: [
          { label: '3 months', value: month * 3 }, { label: '6 months', value: month * 6 },
          { label: '1 year', value: yearNet }, { label: '3 years', value: yearNet * 3 }
        ],
        note: 'After costs and your tax set-aside. Invested at 7%/yr, three years of this income grows to about ' + usd(fv(month, 36, 0.07)) + '.'
      };
    },
    'gig-calculator': function (v) {
      var gasCost = v.mpg > 0 ? v.miles / v.mpg * v.gas : 0;
      var wear = v.miles * v.wear;
      var net = v.gross - gasCost - wear;
      var gh = v.hours ? v.gross / v.hours : 0;
      var nh = v.hours ? net / v.hours : 0;
      var deduction = v.miles * v.irs * 50;
      return {
        rows: [
          ['Advertised hourly (gross)', usd(gh, 2)],
          ['True hourly after car costs', usd(nh, 2), true, nh],
          ['Net per week', usd(net), true, net],
          ['Per mile earned', usd(v.miles ? v.gross / v.miles : 0, 2)],
          ['Yearly mileage deduction (50 wks)', usd(deduction)]
        ],
        bars: [{ label: 'App pay', value: v.gross }, { label: 'Gas', value: -gasCost }, { label: 'Wear', value: -wear }, { label: 'You keep', value: net }],
        note: nh < 15 ? 'Under $15/hr after costs — try driving only peak hours or adding a second app.' : 'Solid. Track every mile: the standard mileage deduction can wipe out most of the tax on this income.'
      };
    },
    'tax-estimator': function (v) {
      var st = v.status || 'single';
      var seBase = v.profit * 0.9235;
      var ssRoom = Math.max(0, SS_WAGE_BASE - v.wages);
      var se = v.profit >= 400 ? Math.min(seBase, ssRoom) * 0.124 + seBase * 0.029 : 0;
      var before = incomeTax(Math.max(0, v.wages - STD[st]), st);
      var after = incomeTax(Math.max(0, v.wages + v.profit - se / 2 - STD[st]), st);
      var fed = after - before;
      var state = v.profit * v.state / 100;
      var total = se + fed + state;
      return {
        rows: [
          ['Self-employment tax (15.3%)', usd(se)],
          ['Extra federal income tax', usd(fed)],
          ['State income tax (est.)', usd(state)],
          ['Total tax on side income', usd(total), true, total],
          ['Set aside from each dollar', pct(v.profit ? total / v.profit * 100 : 0), true],
          ['Quarterly estimated payment', usd(total / 4)]
        ],
        bars: [{ label: 'SE tax', value: se }, { label: 'Federal', value: fed }, { label: 'State', value: state }, { label: 'You keep', value: v.profit - total }],
        note: 'Estimate using 2026 federal brackets and the standard deduction. Not tax advice — QBI deductions, credits and local taxes can change your number.'
      };
    },
    'course-calculator': function (v) {
      var gross = v.price * v.sales;
      var own = v.own / 100;
      var udemy = gross * (1 - own) * 0.37 + gross * own * 0.97;
      var skill = v.minutes * v.perMin;
      var thinkific = gross * (1 - 0.029) - v.sales * 0.30 - v.plan;
      return {
        rows: [
          ['Udemy (37% organic / 97% your coupons)', usd(udemy), false, udemy],
          ['Skillshare (minutes-watched royalties)', usd(skill)],
          ['Thinkific (you keep sales − fees − plan)', usd(thinkific), true, thinkific],
          ['Yearly on the best option', usd(Math.max(udemy, skill, thinkific) * 12), true]
        ],
        bars: [{ label: 'Udemy', value: udemy }, { label: 'Skillshare', value: skill }, { label: 'Thinkific', value: thinkific }],
        note: 'Monthly estimates. Udemy and Skillshare bring the audience; Thinkific makes you find it but you keep the student list. Rates change — check each platform\'s current terms.'
      };
    },
    'freelance-rate': function (v) {
      var monthlyHours = v.hours * 52 / 12;
      var needed = (v.target / (1 - v.tax / 100) + v.costs) / (1 - v.fee / 100);
      var rate = monthlyHours ? needed / monthlyHours : 0;
      return {
        rows: [
          ['Billable hours per month', num(monthlyHours, 1)],
          ['Charge at least', usd(rate, 2) + '/hr', true, rate],
          ['Price a ' + num(v.gigHours, 1) + '-hour gig at', usd(Math.ceil(rate * v.gigHours / 5) * 5), true],
          ['Gross billings needed per month', usd(needed)],
          ['Platform fees per month', usd(needed * v.fee / 100)]
        ],
        bars: [{ label: 'Billings', value: needed }, { label: 'Fees', value: -needed * v.fee / 100 }, { label: 'Tax', value: -(v.target / (1 - v.tax / 100) - v.target) }, { label: 'Take-home', value: v.target }],
        note: 'Tip: offer three packages (basic, standard, premium) priced at 1×, 2× and 3.5× this gig price.'
      };
    },
    'shopify-profit': function (v) {
      var fees = v.price * v.feePct / 100 + 0.30;
      var per = v.price - v.cost - v.ship - fees - v.ads;
      var monthly = per * v.orders - v.fixed;
      var be = per > 0 ? Math.ceil(v.fixed / per) : Infinity;
      return {
        rows: [
          ['Profit per order', usd(per, 2), true, per],
          ['Margin', pct(v.price ? per / v.price * 100 : 0)],
          ['Monthly profit', usd(monthly), true, monthly],
          ['Break-even orders / month', isFinite(be) ? num(be) : 'Never — raise price or cut costs'],
          ['Max ad spend per order to break even', usd(v.price - v.cost - v.ship - fees, 2)]
        ],
        bars: [{ label: 'Price', value: v.price }, { label: 'Product', value: -v.cost }, { label: 'Ship+fees', value: -(v.ship + fees) }, { label: 'Ads', value: -v.ads }, { label: 'Profit', value: per }],
        note: per / v.price < 0.2 ? 'Below a 20% margin, one bad ad week wipes out the month. Aim for 30%+.' : 'Healthy margin — now focus on repeat customers to lower your ad cost per order.'
      };
    },
    'affiliate-calculator': function (v) {
      var sales = v.visitors * v.ctr / 100 * v.conv / 100;
      var month = sales * v.commission;
      var year = 0, vis = v.visitors;
      for (var i = 0; i < 12; i++) { year += vis * v.ctr / 100 * v.conv / 100 * v.commission; vis *= 1 + v.growth / 100; }
      return {
        rows: [
          ['Clicks to the offer / month', num(v.visitors * v.ctr / 100)],
          ['Sales / month', num(sales, 1)],
          ['Commission this month', usd(month), true, month],
          ['Next 12 months with growth', usd(year), true, year],
          ['Earnings per 1,000 visitors', usd(v.visitors ? month / v.visitors * 1000 : 0, 2)]
        ],
        bars: [{ label: 'Month 1', value: month }, { label: 'Month 6', value: month * Math.pow(1 + v.growth / 100, 5) }, { label: 'Month 12', value: month * Math.pow(1 + v.growth / 100, 11) }],
        note: 'The biggest lever is usually click-through: a comparison table or a tool on the page converts better than a sidebar banner.'
      };
    }
  };

  function fv(monthly, months, rate) {
    var r = rate / 12, t = 0;
    for (var i = 0; i < months; i++) t = (t + monthly) * (1 + r);
    return t;
  }

  function bindCalc(tool) {
    var key = tool.getAttribute('data-tool');
    var form = tool.querySelector('.tool-form');
    var out = tool.querySelector('.tool-out');
    var last = null;
    function run(celebrate) {
      var v = {};
      Array.prototype.forEach.call(form.elements, function (el) {
        if (!el.name) return;
        v[el.name] = el.tagName === 'SELECT' ? el.value : (parseFloat(el.value) || 0);
      });
      var r = CALC[key](v);
      paint(out, r.rows, r.bars, r.note);
      var key$ = r.rows.filter(function (x) { return x[2]; })[0];
      if (celebrate && key$ && key$[3] > 0 && key$[3] !== last && window.BSH && window.BSH.coinBurst) {
        window.BSH.coinBurst(out.querySelector('.is-key b'));
      }
      last = key$ ? key$[3] : null;
    }
    var timer;
    form.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(function () { run(true); }, 350); });
    run(false);
  }

  /* ---------------------------------------------------------------- quiz */
  var HUSTLES = [
    { n: 'Food & grocery delivery', u: '/side-hustles-you-can-start-with-just-your-smartphone/', pay: '$15–$25/hr', t: { fast: 3, steady: 1, out: 2, phone: 2, car: 3, '0': 2, lt5: 1, '5to10': 2, '10to20': 2, gt20: 2 } },
    { n: 'Rideshare driving (Uber/Lyft)', u: '/lyft-uber/', pay: '$18–$30/hr gross', t: { fast: 2, steady: 2, out: 2, people: 2, car: 4, '0': 1, '10to20': 2, gt20: 3 } },
    { n: 'Freelancing on Fiverr', u: '/fiverr/', pay: '$20–$75/hr', t: { home: 3, creative: 3, tech: 2, scale: 2, steady: 1, '0': 2, '5to10': 2, '10to20': 2 } },
    { n: 'Digital marketing for small businesses', u: '/digital-marketing-side-hustle/', pay: '$300–$1,500/client/mo', t: { home: 3, tech: 3, creative: 1, people: 1, scale: 3, steady: 2, '0': 2, '10to20': 2, gt20: 1 } },
    { n: 'Teach a course on Udemy', u: '/udemy/', pay: '$50–$2,000+/mo', t: { passive: 4, scale: 2, home: 2, creative: 2, tech: 2, '100': 1, '500': 2, '5to10': 1, '10to20': 1 } },
    { n: 'Skillshare classes', u: '/skillshare/', pay: 'Royalties per minute watched', t: { passive: 3, creative: 3, home: 2, '100': 1, lt5: 1, '5to10': 1 } },
    { n: 'Your own course on Thinkific', u: '/thinkific/', pay: 'You set the price', t: { scale: 3, passive: 2, tech: 1, people: 1, home: 2, '500': 2, more: 2, '10to20': 1 } },
    { n: 'Shopify store (print-on-demand)', u: '/shopify/', pay: '20–40% margins', t: { scale: 3, passive: 1, creative: 2, tech: 1, home: 2, '100': 1, '500': 2, more: 2, '10to20': 1, gt20: 1 } },
    { n: 'Semrush affiliate & SEO services', u: '/semrush/', pay: '$200 per referred sale', t: { passive: 2, scale: 3, tech: 3, home: 2, '0': 1, '100': 1, '5to10': 1, '10to20': 1 } },
    { n: 'Pet sitting & dog walking', u: '/blog/?cat=city-guides', pay: '$15–$30/walk', t: { fast: 2, steady: 2, out: 3, people: 2, hands: 1, no: 1, '0': 2, lt5: 2, '5to10': 2 } },
    { n: 'Cleaning & Airbnb turnovers', u: '/blog/?cat=city-guides', pay: '$25–$45/hr', t: { steady: 3, fast: 1, out: 3, hands: 3, '100': 2, '5to10': 1, '10to20': 2 } },
    { n: 'Handyman & furniture assembly', u: '/blog/?cat=city-guides', pay: '$35–$75/hr', t: { steady: 2, scale: 1, out: 3, hands: 4, car: 1, '100': 1, '500': 2, '5to10': 1, '10to20': 2 } },
    { n: 'Paid surveys, testing & micro-tasks', u: '/side-hustles-you-can-start-with-just-your-smartphone/', pay: '$5–$15/hr', t: { phone: 4, lt5: 3, '0': 3, fast: 1, no: 1 } },
    { n: 'UGC videos for brands', u: '/side-hustles-you-can-start-with-just-your-smartphone/', pay: '$100–$300/video', t: { phone: 3, creative: 4, scale: 1, people: 1, '100': 1, lt5: 1, '5to10': 2 } },
    { n: 'Reselling (thrift flipping)', u: '/side-hustles-you-can-start-with-just-your-smartphone/', pay: '$200–$1,000/mo', t: { fast: 1, steady: 1, out: 2, phone: 2, hands: 1, '100': 2, '500': 1, car: 1, '5to10': 2 } },
    { n: 'Online tutoring', u: '/blog/?cat=city-guides', pay: '$20–$60/hr', t: { home: 3, people: 3, steady: 3, tech: 1, '0': 2, lt5: 1, '5to10': 2 } },
    { n: 'Virtual assistant work', u: '/fiverr/', pay: '$18–$35/hr', t: { home: 3, steady: 3, people: 1, tech: 1, '0': 2, '10to20': 2, gt20: 1 } },
    { n: 'Coursera certificate → freelance skill', u: '/coursera/', pay: 'Unlocks $25–$60/hr work', t: { scale: 2, tech: 2, home: 1, '100': 1, '5to10': 1 } }
  ];
  var LABELS = { lt5: 'a few hours a week', '5to10': '5–10 hours a week', '10to20': '10–20 hours a week', gt20: '20+ hours a week' };

  function bindQuiz(tool) {
    var steps = tool.querySelectorAll('.quiz-step');
    var bar = tool.querySelector('.quiz-progress span');
    var result = tool.querySelector('.quiz-result');
    var ans = {}, i = 0;
    function show(n) {
      Array.prototype.forEach.call(steps, function (s, k) { s.classList.toggle('is-active', k === n); });
      bar.style.width = (n / steps.length * 100) + '%';
    }
    tool.addEventListener('click', function (e) {
      var b = e.target.closest('.quiz-opt');
      if (b) {
        var step = b.closest('.quiz-step');
        ans[step.getAttribute('data-q')] = b.getAttribute('data-v');
        i++;
        if (i < steps.length) show(i); else finish();
      }
      if (e.target.closest('.quiz-restart')) {
        ans = {}; i = 0; result.hidden = true; tool.querySelector('.quiz-steps').hidden = false; show(0);
      }
    });
    function finish() {
      bar.style.width = '100%';
      var picks = Object.keys(ans).map(function (k) { return k === 'car' && ans[k] === 'yes' ? 'car' : ans[k]; });
      var scored = HUSTLES.map(function (h) {
        var s = 0;
        picks.forEach(function (p) { s += h.t[p] || 0; });
        if (ans.where === 'any') s += (h.t.home || 0) / 2 + (h.t.out || 0) / 2;
        if (ans.car === 'no' && (h.t.car || 0) >= 3) s -= 10;
        if (ans.budget === '0' && (h.t.more || h.t['500']) && !h.t['0']) s -= 2;
        return { h: h, s: s };
      }).sort(function (a, b) { return b.s - a.s; }).slice(0, 3);
      var html = '<p class="quiz-kicker">Your top matches for ' + (LABELS[ans.time] || 'your schedule') + '</p><ol class="quiz-picks">';
      scored.forEach(function (x, k) {
        html += '<li style="--d:' + (k * 120) + 'ms"><span class="rank">' + (k + 1) + '</span><div><b>' + x.h.n + '</b><small>Typical pay: ' + x.h.pay + '</small></div><a class="btn btn-sm" href="' + x.h.u + '">Read the guide</a></li>';
      });
      html += '</ol><div class="quiz-after"><a href="/tools/income-calculator/">Estimate your earnings →</a><button type="button" class="quiz-restart">Retake quiz</button></div>';
      tool.querySelector('.quiz-steps').hidden = true;
      result.innerHTML = html;
      result.hidden = false;
      if (window.BSH && window.BSH.coinBurst) window.BSH.coinBurst(result);
    }
  }

  document.querySelectorAll('.tool[data-tool]').forEach(function (t) {
    var key = t.getAttribute('data-tool');
    if (key === 'quiz') bindQuiz(t);
    else if (CALC[key]) bindCalc(t);
  });
})();
