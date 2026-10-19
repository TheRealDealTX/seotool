/* Adjuster salary estimate model, shared by the homepage estimator and /salary-calculator/.
   Mid-career (about 5 years) annual base by role and line, adjusted for experience and state. */
(function () {
  'use strict';
  var BASE = {
    desk:        { property: 64000, auto: 58000, wc: 66000, casualty: 70000, commercial: 88000 },
    field:       { property: 74000, auto: 64000, wc: 68000, casualty: 76000, commercial: 96000 },
    independent: { property: 84000, auto: 60000, wc: 68000, casualty: 78000, commercial: 110000 },
    cat:         { property: 98000, auto: 68000, wc: 70000, casualty: 82000, commercial: 125000 },
    public:      { property: 82000, auto: 60000, wc: 60000, casualty: 70000, commercial: 120000 }
  };
  // Spread of realistic outcomes around the estimate (low, high multipliers)
  var SPREAD = {
    desk: [0.85, 1.17], field: [0.85, 1.2], independent: [0.55, 1.6], cat: [0.45, 2.0], public: [0.5, 1.9]
  };
  var LABELS = {
    desk: 'Staff desk adjuster', field: 'Staff field adjuster', independent: 'Independent adjuster (1099)',
    cat: 'Catastrophe (CAT) adjuster', public: 'Public adjuster'
  };

  function expFactor(years) {
    // 0 yrs ~0.72x, 5 yrs ~1.0x, 10 yrs ~1.15x, 20 yrs ~1.27x
    return 0.72 + 0.58 * (1 - Math.exp(-years / 6.2)) * 1.0;
  }

  /**
   * opts: { role, line, years, stateIndex, designation (bool), bilingual (bool) }
   * returns { mid, low, high, hourly, monthly, label, benefits }
   */
  function estimate(opts) {
    var role = BASE[opts.role] ? opts.role : 'desk';
    var line = BASE[role][opts.line] ? opts.line : 'property';
    var mid = BASE[role][line] * expFactor(+opts.years || 0) / expFactor(5);
    var idx = +opts.stateIndex || 1;
    // 1099 and CAT pay is set by national fee schedules, so location matters less
    var stateWeight = (role === 'desk' || role === 'field') ? 1 : 0.35;
    mid *= 1 + (idx - 1) * stateWeight;
    if (opts.designation) mid *= 1.06;
    if (opts.bilingual) mid *= 1.04;
    var s = SPREAD[role];
    var round = function (n) { return Math.round(n / 500) * 500; };
    var benefits = role === 'field' ? 11000 : role === 'desk' ? 8000 : 0;
    return {
      mid: round(mid), low: round(mid * s[0]), high: round(mid * s[1]),
      hourly: mid / 2080, monthly: mid / 12, label: LABELS[role], benefits: benefits,
      w2: role === 'desk' || role === 'field'
    };
  }

  window.IAS = window.IAS || {};
  IAS.salary = { estimate: estimate, labels: LABELS };
})();
