/* claimsconsultant.com — the only script on the site.
   Header state, drawer, scroll reveal, and the six claim calculators.
   No dependencies, no build step. */
(function () {
  'use strict';

  var d = document;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* ------------------------------------------------------------ header */
  var mast = $('.masthead');
  if (mast) {
    var onScroll = function () {
      mast.classList.toggle('is-stuck', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ------------------------------------------------------------ drawer */
  var burger = $('.burger');
  var drawer = $('.drawer');
  var scrim = $('.drawer-scrim');
  var lastFocus = null;

  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('is-open', open);
    if (scrim) scrim.classList.toggle('is-open', open);
    if (burger) burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
    d.documentElement.style.overflow = open ? 'hidden' : '';
    if (open) {
      lastFocus = d.activeElement;
      var first = $('.drawer-close', drawer);
      if (first) first.focus();
    } else if (lastFocus) {
      lastFocus.focus();
    }
  }

  if (burger) burger.addEventListener('click', function () {
    setDrawer(!drawer.classList.contains('is-open'));
  });
  if (scrim) scrim.addEventListener('click', function () { setDrawer(false); });
  var dclose = $('.drawer-close');
  if (dclose) dclose.addEventListener('click', function () { setDrawer(false); });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && drawer && drawer.classList.contains('is-open')) setDrawer(false);
  });
  $$('.drawer a').forEach(function (a) {
    a.addEventListener('click', function () { setDrawer(false); });
  });

  /* ------------------------------------------------------- scroll reveal */
  var rv = $$('.rv');
  if (rv.length && 'IntersectionObserver' in window &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  /* ------------------------------------------------ accordion: one open */
  $$('.acc[data-exclusive]').forEach(function (acc) {
    var items = $$('details', acc);
    items.forEach(function (det) {
      det.addEventListener('toggle', function () {
        if (!det.open) return;
        items.forEach(function (o) { if (o !== det) o.open = false; });
      });
    });
  });

  /* ------------------------------------------------------------ formats */
  var usd0 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
  var usd2 = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2, maximumFractionDigits: 2 });
  function money(n) { return isFinite(n) ? usd0.format(Math.round(n)) : '—'; }
  function money2(n) { return isFinite(n) ? usd2.format(n) : '—'; }
  function pct(n, dp) { return isFinite(n) ? n.toFixed(dp == null ? 1 : dp) + '%' : '—'; }
  function num(el) {
    if (!el) return 0;
    var v = parseFloat(String(el.value).replace(/[^0-9.\-]/g, ''));
    return isFinite(v) ? v : 0;
  }
  function val(root, name) { return num($('[name="' + name + '"]', root)); }
  function raw(root, name) { var el = $('[name="' + name + '"]', root); return el ? el.value : ''; }
  function put(root, key, text) {
    /* several outputs share a key — the headline figure repeats one of the
       summary rows — so write to every match, not just the first. */
    $$('[data-out="' + key + '"]', root).forEach(function (el) { el.textContent = text; });
  }
  function flag(root, key, on, html) {
    var el = $('[data-flag="' + key + '"]', root);
    if (!el) return;
    el.hidden = !on;
    if (on && html) el.innerHTML = html;
  }

  /* --------------------------------------------------------- calculators
     Each calculator is a <form data-calc="name">. Inputs are read by name,
     results written into [data-out="key"]. Recalculates on every input. */
  var CALC = {};

  /* 1. Commercial claim value estimator ------------------------------- */
  CALC['claim-value'] = function (f) {
    var sf = val(f, 'sqft');
    var cost = val(f, 'cost');
    var dmg = val(f, 'damage') / 100;
    var contents = val(f, 'contents') / 100;
    var code = val(f, 'code') / 100;
    var debris = val(f, 'debris') / 100;
    var age = val(f, 'age');
    var life = Math.max(val(f, 'life'), 1);
    var dedType = raw(f, 'dedtype');
    var dedVal = val(f, 'ded');

    var rcvBuilding = sf * cost;
    var directLoss = rcvBuilding * dmg;
    var contentsLoss = directLoss * contents;
    var codeLoss = directLoss * code;
    var debrisLoss = directLoss * debris;
    var grossRCV = directLoss + contentsLoss + codeLoss + debrisLoss;

    var depRate = Math.min(age / life, 0.75);            // capped: carriers rarely sustain >75%
    var depreciation = (directLoss + contentsLoss) * depRate;
    var acv = grossRCV - depreciation;

    var tiv = rcvBuilding;
    var deductible = dedType === 'pct' ? tiv * (dedVal / 100) : dedVal;

    var acvNet = Math.max(acv - deductible, 0);
    var rcvNet = Math.max(grossRCV - deductible, 0);
    var recoverableDep = rcvNet - acvNet;

    put(f, 'rcv', money(grossRCV));
    put(f, 'tiv', money(tiv));
    put(f, 'direct', money(directLoss));
    put(f, 'contents', money(contentsLoss));
    put(f, 'code', money(codeLoss));
    put(f, 'debris', money(debrisLoss));
    put(f, 'dep', '(' + money(depreciation) + ')');
    put(f, 'deprate', pct(depRate * 100, 0));
    put(f, 'deductible', '(' + money(deductible) + ')');
    put(f, 'acvnet', money(acvNet));
    put(f, 'holdback', money(recoverableDep));
    put(f, 'rcvnet', money(rcvNet));

    flag(f, 'pctded', dedType === 'pct' && dedVal > 0,
      '<b>Percentage deductible.</b> At ' + pct(dedVal, 0) + ' of a ' + money(tiv) +
      ' insured value, your retention is ' + money(deductible) +
      ' before a dollar is paid. Named-storm deductibles are applied per occurrence, and on multi-building schedules the wording decides whether that is once or once per structure. It is worth reading before the next storm, not after.');
    flag(f, 'codeflag', code > 0 && codeLoss > 0,
      '<b>Ordinance or law.</b> ' + money(codeLoss) + ' of this figure is code-upgrade cost. It is payable only to the extent Coverage B/C limits exist, and those limits are often a small percentage of the building limit rather than a full replacement guarantee.');
  };

  /* 2. Business interruption ------------------------------------------ */
  CALC['bi'] = function (f) {
    var rev = val(f, 'revenue');
    var margin = val(f, 'margin') / 100;
    var continuing = val(f, 'continuing') / 100;
    var months = val(f, 'months');
    var capacity = val(f, 'capacity') / 100;      // share of operations still running
    var extra = val(f, 'extra');
    var saved = val(f, 'saved');
    var waiting = val(f, 'waiting');              // hours or days of waiting period
    var trend = val(f, 'trend') / 100;

    var monthlyRev = rev / 12;
    var projMonthlyRev = monthlyRev * (1 + trend);
    var lostRevenue = projMonthlyRev * months * (1 - capacity);
    var grossEarnings = lostRevenue * margin;
    var continuingExp = lostRevenue * continuing;
    var biLoss = grossEarnings + continuingExp;

    var waitDeduct = (projMonthlyRev / 30) * waiting * (1 - capacity) * (margin + continuing);
    biLoss = Math.max(biLoss - waitDeduct, 0);

    var total = biLoss + extra - saved;

    put(f, 'monthly', money(projMonthlyRev));
    put(f, 'lostrev', money(lostRevenue));
    put(f, 'gross', money(grossEarnings));
    put(f, 'cont', money(continuingExp));
    put(f, 'wait', '(' + money(waitDeduct) + ')');
    put(f, 'bi', money(biLoss));
    put(f, 'extra', money(extra));
    put(f, 'saved', '(' + money(saved) + ')');
    put(f, 'total', money(Math.max(total, 0)));
    put(f, 'perday', money(total / Math.max(months * 30.44, 1)));

    flag(f, 'longtail', months >= 12,
      '<b>Period of restoration.</b> At ' + months + ' months you are past the point where most policies stop paying without an extended period of indemnity endorsement. Check whether yours carries one, and what the sub-limit is — that single endorsement often decides the last third of a claim this size.');
  };

  /* 3. Coinsurance penalty -------------------------------------------- */
  CALC['coinsurance'] = function (f) {
    var carried = val(f, 'carried');
    var value = val(f, 'value');
    var co = val(f, 'co') / 100;
    var loss = val(f, 'loss');
    var ded = val(f, 'ded');

    var required = value * co;
    var ratio = required > 0 ? Math.min(carried / required, 1) : 0;
    var payable = loss * ratio;
    var afterDed = Math.max(payable - ded, 0);
    var penalty = Math.max(loss - payable, 0);
    var shortfall = Math.max(required - carried, 0);

    put(f, 'required', money(required));
    put(f, 'carried', money(carried));
    put(f, 'shortfall', money(shortfall));
    put(f, 'ratio', pct(ratio * 100, 1));
    put(f, 'payable', money(payable));
    put(f, 'penalty', '(' + money(penalty) + ')');
    put(f, 'ded', '(' + money(ded) + ')');
    put(f, 'net', money(afterDed));

    flag(f, 'penalized', shortfall > 0 && loss > 0,
      '<b>You are underinsured by ' + money(shortfall) + '.</b> The coinsurance clause reduces every covered loss by the same ratio, so this penalty applies to a $10,000 claim and a total loss alike — ' + money(penalty) +
      ' of this loss is uninsured before the deductible is even taken. Where the valuation behind the limit is stale, that ratio is commonly negotiable on the value side.');
    flag(f, 'clean', shortfall <= 0 && loss > 0,
      '<b>No coinsurance penalty.</b> The limit carried meets or exceeds the required amount, so the loss is payable in full subject to the deductible and policy limits.');
  };

  /* 4. RCV / ACV depreciation ----------------------------------------- */
  CALC['depreciation'] = function (f) {
    var rcv = val(f, 'rcv');
    var age = val(f, 'age');
    var life = Math.max(val(f, 'life'), 1);
    var condition = val(f, 'condition');         // -2 .. +2 adjustment in years
    var labor = raw(f, 'labor') === 'yes';
    var laborShare = val(f, 'laborshare') / 100;
    var ded = val(f, 'ded');

    var effAge = Math.max(Math.min(age - condition, life), 0);
    var rate = Math.min(effAge / life, 1);

    var depreciableBase = labor ? rcv : rcv * (1 - laborShare);
    var depreciation = depreciableBase * rate;
    var acv = rcv - depreciation;
    var acvPayment = Math.max(acv - ded, 0);
    var holdback = Math.max(rcv - ded, 0) - acvPayment;

    put(f, 'rcv', money(rcv));
    put(f, 'effage', effAge.toFixed(1) + ' yrs');
    put(f, 'rate', pct(rate * 100, 1));
    put(f, 'base', money(depreciableBase));
    put(f, 'dep', '(' + money(depreciation) + ')');
    put(f, 'acv', money(acv));
    put(f, 'ded', '(' + money(ded) + ')');
    put(f, 'first', money(acvPayment));
    put(f, 'holdback', money(holdback));

    flag(f, 'labordep', labor && rcv > 0,
      '<b>Labor is being depreciated.</b> ' + money(rcv * laborShare * rate) +
      ' of the withholding is depreciation taken on labor instead of materials. Texas policies vary on whether that is permitted, and the answer usually sits in the valuation wording instead of the estimate. It is one of the first line items worth challenging.');
    flag(f, 'bigholdback', holdback > 0 && rcv > 0 && (holdback / Math.max(rcv, 1)) > 0.35,
      '<b>Recoverable depreciation is ' + pct((holdback / rcv) * 100, 0) + ' of the claim.</b> That sum is payable only after the work is completed and documented, and most policies put a clock on it — commonly 180 days or two years from the loss. Track the deadline from day one.');
  };

  /* 5. Cabinet repair vs replace ---------------------------------------- */
  CALC['cabinet'] = function (f) {
    var total = val(f, 'total');
    var damaged = Math.min(val(f, 'damaged'), total);
    var repairable = Math.min(val(f, 'repairable'), damaged);
    var refinish = val(f, 'refinish');
    var replace = val(f, 'replace');
    var tops = val(f, 'tops');
    var matching = raw(f, 'matching') === 'yes';

    var notRepairable = Math.max(damaged - repairable, 0);
    /* A discontinued profile means new boxes cannot be blended into the run, so
       replacement extends across the whole run — and nothing is refinished,
       because the boxes that could have been saved are replaced along with it. */
    var fullRun = !matching && notRepairable > 0;
    var partialBoxes = fullRun ? total : notRepairable;
    var refinishedBoxes = fullRun ? 0 : repairable;
    var partialRefinish = refinishedBoxes * refinish;
    var partialReplace = partialBoxes * replace;
    var partialTops = partialBoxes > 0 ? tops : 0;
    var partial = partialRefinish + partialReplace + partialTops;

    var full = total * replace + tops;
    var ratio = full > 0 ? (partial / full) * 100 : 0;
    var saving = full - partial;

    put(f, 'damaged', damaged ? damaged + ' of ' + total : '—');
    put(f, 'repairable', repairable + ' boxes');
    put(f, 'refinished', refinishedBoxes + ' boxes');
    put(f, 'notrepairable', notRepairable + ' boxes');
    put(f, 'partialboxes', partialBoxes + ' boxes');
    put(f, 'partialrefinish', money(partialRefinish));
    put(f, 'partialreplace', money(partialReplace));
    put(f, 'partialtops', money(partialTops));
    put(f, 'partial', money(partial));
    put(f, 'full', money(full));
    put(f, 'ratio', pct(ratio, 0));
    put(f, 'saving', money(saving));

    flag(f, 'nomatch', fullRun,
      '<b>The profile is discontinued.</b> New boxes cannot be blended into a run that has to '
      + 'read as one installation, so the replacement scope extends across all ' + total
      + ' boxes rather than the ' + notRepairable + ' that failed. That is the matching '
      + 'argument, and it needs documentary support &mdash; manufacturer correspondence or a '
      + 'discontinued-product notice, not an assertion.');
    flag(f, 'threshold', matching && full > 0 && ratio >= 70,
      '<b>The partial path costs ' + pct(ratio, 0) + ' of full replacement.</b> Once a repair '
      + 'scope passes roughly 70% of the replacement cost, replacement is usually the better '
      + 'outcome for everyone: one trade mobilization, a uniform finish and a warranty on the '
      + 'whole run. Worth stating explicitly instead of defending a marginal saving.');
    flag(f, 'worthit', matching && full > 0 && ratio > 0 && ratio < 70,
      '<b>Partial repair saves ' + money(saving) + '</b> against full replacement, at '
      + pct(ratio, 0) + ' of the cost. That is a defensible repair scope, provided the '
      + repairable + ' boxes called repairable are, which is a substrate and moisture '
      + 'question instead of a visual one.');
  };

  /* 6. Commercial roof replacement estimator -------------------------- */
  CALC['roof'] = function (f) {
    var sf = val(f, 'area');
    var rate = val(f, 'system');
    var layers = val(f, 'layers');
    var insul = val(f, 'insul');
    var deck = val(f, 'deck') / 100;
    var flashLf = val(f, 'flashing');
    var curbs = val(f, 'curbs');
    var access = val(f, 'access') / 100;
    var market = val(f, 'market') / 100;

    var field = sf * rate;
    var tearoff = sf * 1.35 * layers;
    var insulation = sf * insul;
    var deckRepair = sf * deck * 9.5;
    var flashing = flashLf * 28;
    var curbWork = curbs * 850;

    var subtotal = field + tearoff + insulation + deckRepair + flashing + curbWork;
    var accessCost = subtotal * access;
    var base = subtotal + accessCost;
    var oandp = base * 0.20;
    var withOP = base + oandp;
    var total = withOP * (1 + market);
    var perSf = sf > 0 ? total / sf : 0;
    var squares = sf / 100;

    put(f, 'squares', squares ? squares.toFixed(1) + ' sq' : '—');
    put(f, 'field', money(field));
    put(f, 'tearoff', money(tearoff));
    put(f, 'insul', money(insulation));
    put(f, 'deck', money(deckRepair));
    put(f, 'flashing', money(flashing));
    put(f, 'curbs', money(curbWork));
    put(f, 'access', money(accessCost));
    put(f, 'oandp', money(oandp));
    put(f, 'total', money(total));
    put(f, 'persf', money2(perSf));

    flag(f, 'op', total > 0,
      '<b>Overhead and profit is included at 20%.</b> A re-roof of this size involves three or more trades, which is the standard test for whether a general contractor is reasonably required. Carriers regularly strip O&amp;P from the first estimate on commercial roofs; on a ' + money(base) + ' scope that removal is worth ' + money(oandp) + '.');
  };

  /* 7. Overhead, profit and general conditions ------------------------- */
  CALC['oandp'] = function (f) {
    var direct = val(f, 'direct');
    var trades = val(f, 'trades');
    var gcPct = val(f, 'gc') / 100;
    var oPct = val(f, 'overhead') / 100;
    var pPct = val(f, 'profit') / 100;
    var occupied = raw(f, 'occupied') === 'yes';
    var occPct = val(f, 'occupancy') / 100;
    var months = val(f, 'months');
    var bondPct = val(f, 'bond') / 100;

    var access = occupied ? direct * occPct : 0;
    var base = direct + access;
    var gc = base * gcPct;
    var subtotal = base + gc;
    var overhead = subtotal * oPct;
    var profit = subtotal * pPct;
    var bond = (subtotal + overhead + profit) * bondPct;
    var total = subtotal + overhead + profit + bond;
    var combined = subtotal > 0 ? ((overhead + profit) / subtotal) * 100 : 0;
    var gcPerMonth = months > 0 ? gc / months : 0;

    put(f, 'direct', money(direct));
    put(f, 'access', money(access));
    put(f, 'base', money(base));
    put(f, 'gc', money(gc));
    put(f, 'gcmo', money(gcPerMonth));
    put(f, 'subtotal', money(subtotal));
    put(f, 'overhead', money(overhead));
    put(f, 'profit', money(profit));
    put(f, 'combined', pct(combined, 1));
    put(f, 'bond', money(bond));
    put(f, 'total', money(total));

    flag(f, 'trades', trades >= 3,
      '<b>' + trades + ' trades on this scope.</b> Three or more is the usual threshold for '
      + 'saying a general contractor is reasonably required, which is the common test for whether '
      + 'overhead and profit are owed. On this scope that is ' + money(overhead + profit)
      + ' &mdash; worth establishing on the record rather than leaving to be argued.');
    flag(f, 'fewtrades', trades > 0 && trades < 3,
      '<b>Only ' + trades + ' trade' + (trades === 1 ? '' : 's') + ' on this scope.</b> Below the '
      + 'usual three-trade threshold, a general contractor may not be reasonably required and '
      + 'full O&amp;P is harder to sustain. Coordination cost may still be real; it is better '
      + 'argued as general conditions than as O&amp;P.');
    flag(f, 'gcflag', gcPct > 0 && months > 0,
      '<b>General conditions run ' + money(gcPerMonth) + ' per month</b> over a '
      + months + '-month schedule. Supervision, temporary utilities, dumpsters, protection, '
      + 'permits and logistics are time-dependent, so a disputed period of restoration moves '
      + 'this line as well as the time-element claim.');
  };

  /* wire every calculator on the page */
  $$('form[data-calc]').forEach(function (f) {
    var fn = CALC[f.getAttribute('data-calc')];
    if (!fn) return;
    var run = function () { try { fn(f); } catch (e) { /* never break the page */ } };
    f.addEventListener('input', run);
    f.addEventListener('change', run);
    f.addEventListener('submit', function (e) { e.preventDefault(); run(); });
    var reset = $('[data-action="reset"]', f);
    if (reset) reset.addEventListener('click', function () { f.reset(); setTimeout(run, 0); });
    var printer = $('[data-action="print"]', f);
    if (printer) printer.addEventListener('click', function () { window.print(); });
    var copier = $('[data-action="copy"]', f);
    if (copier) copier.addEventListener('click', function () {
      var lines = [d.title.split('|')[0].trim(), ''];
      $$('.outrow', f).forEach(function (r) {
        var c = r.children;
        if (c.length >= 2) lines.push(c[0].textContent.trim() + ': ' + c[1].textContent.trim());
      });
      var big = $('.bignum', f);
      if (big) lines.push('', 'Headline figure: ' + big.textContent.trim());
      lines.push('', 'Estimated with the ' + (f.getAttribute('data-label') || 'calculator') + ' at ' + location.href);
      var text = lines.join('\n');
      var done = function () {
        var old = copier.textContent;
        copier.textContent = 'Copied';
        setTimeout(function () { copier.textContent = old; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {});
      } else {
        var ta = d.createElement('textarea');
        ta.value = text; d.body.appendChild(ta); ta.select();
        try { d.execCommand('copy'); done(); } catch (e) {}
        d.body.removeChild(ta);
      }
    });
    run();
  });

  /* ------------------------------------------------------- contact form
     Static hosting: the form posts nowhere by default. Until a handler is
     wired in, hand the inquiry to the visitor's mail client instead of
     dropping it silently. */
  var cf = $('form[data-contact]');
  if (cf && !cf.getAttribute('action')) {
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      var get = function (n) { var el = $('[name="' + n + '"]', cf); return el ? el.value.trim(): ''; };
      var body = [
        'Organization: ' + get('org'),
        'Contact: ' + get('name'),
        'Role: ' + get('role'),
        'Phone: ' + get('phone'),
        'Email: ' + get('email'),
        'Property location: ' + get('location'),
        'Date of loss: ' + get('dol'),
        'Cause of loss: ' + get('cause'),
        'Carrier / pool: ' + get('carrier'),
        'Claim status: ' + get('status'),
        '',
        get('message')
      ].join('\n');
      var to = cf.getAttribute('data-contact');
      window.location.href = 'mailto:' + to +
        '?subject=' + encodeURIComponent('Claim review request — ' + (get('org') || get('name'))) +
        '&body=' + encodeURIComponent(body);
    });
  }

  /* --------------------------------------------------- current year fill */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
