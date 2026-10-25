/* Influencer Earnings Calculator */
(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  if (!$('ec-form')) return;

  var P = {
    instagram: { name: 'Instagram', base: 10, avg: 3, unit: 'Followers', likes: 'Avg likes per post',
      types: [['Feed post', 1], ['Reel', 1.3], ['Carousel', 1.1], ['Story (3 frames)', 0.5]] },
    tiktok: { name: 'TikTok', base: 7, avg: 5, unit: 'Followers', likes: 'Avg likes per video',
      types: [['Video', 1], ['Video + Spark Ads rights', 1.4], ['LIVE mention', 0.6]] },
    youtube: { name: 'YouTube', base: 20, avg: 4, unit: 'Subscribers', likes: 'Avg likes per video',
      types: [['Integration (60-90s)', 1], ['Dedicated video', 2.2], ['Short', 0.45]] },
    facebook: { name: 'Facebook', base: 6, avg: 1.5, unit: 'Followers', likes: 'Avg reactions per post',
      types: [['Post', 1], ['Reel', 1.2], ['Live stream', 1.5]] },
    pinterest: { name: 'Pinterest', base: 5, avg: 1, unit: 'Followers', likes: 'Avg saves per Pin',
      types: [['Standard Pin', 1], ['Video Pin', 1.4], ['Board takeover', 2]] }
  };
  var mode = 'rate';
  var MINF = 100, MAXF = 10000000;

  function toSlider(n) { return Math.log(n / MINF) / Math.log(MAXF / MINF) * 100; }
  function fromSlider(v) { return Math.round(MINF * Math.pow(MAXF / MINF, v / 100) / 100) * 100; }
  function money(n) { return '$' + Math.round(n).toLocaleString(); }
  function tween(el, to, fmt) {
    var from = parseFloat(el.dataset.v || 0), t0 = null, d = 600;
    el.dataset.v = to;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { el.textContent = fmt(to); return; }
    (function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / d, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(from + (to - from) * e);
      if (p < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  function fillTypes() {
    var sel = $('ec-type'), plat = P[$('ec-platform').value];
    sel.innerHTML = '';
    plat.types.forEach(function (t, i) { var o = document.createElement('option'); o.value = i; o.textContent = t[0]; sel.appendChild(o); });
    $('ec-flabel').textContent = plat.unit;
    $('ec-likes-l').textContent = plat.likes;
  }

  function engagement(followers) {
    if (mode === 'rate') return parseFloat($('ec-er').value);
    var l = parseFloat($('ec-likes').value) || 0, c = parseFloat($('ec-comments').value) || 0;
    return followers > 0 ? (l + c) / followers * 100 : 0;
  }

  function rateFor(key, followers, er, niche, typeMult) {
    var p = P[key], ratio = Math.max(0.05, er / p.avg);
    var engMult = Math.min(2.2, Math.max(0.5, Math.pow(ratio, 0.7)));
    return Math.max(50, followers / 1000 * p.base * engMult * niche * typeMult);
  }

  function tier(n) {
    return n < 10000 ? 'Nano-influencer' : n < 100000 ? 'Micro-influencer' : n < 500000 ? 'Mid-tier influencer' : n < 1000000 ? 'Macro-influencer' : 'Mega-influencer';
  }

  var lastTier = '';
  function update() {
    var key = $('ec-platform').value, plat = P[key];
    var f = Math.max(0, parseFloat($('ec-followers').value) || 0);
    var er = engagement(f), niche = parseFloat($('ec-niche').value);
    var type = plat.types[$('ec-type').value || 0] || plat.types[0];
    var mid = rateFor(key, f, er, niche, type[1]);
    var lo = Math.max(50, mid * 0.75), hi = mid * 1.35;
    var posts = parseInt($('ec-posts').value, 10);
    var aff = (parseFloat($('ec-aff').value) || 0) * (parseFloat($('ec-comm').value) || 0);
    var monthly = mid * posts + aff;

    $('ec-er-o').textContent = parseFloat($('ec-er').value).toFixed(1) + '%';
    $('ec-posts-o').textContent = posts;
    $('ec-rate').textContent = money(lo) + ' - ' + money(hi);
    $('ec-mid').textContent = 'Suggested asking price: ' + money(mid) + ' per ' + type[0].toLowerCase();
    tween($('ec-month'), monthly, money);
    tween($('ec-year'), monthly * 12, money);

    var t = tier(f), badge = $('ec-tier');
    badge.querySelector('span').textContent = t;
    if (t !== lastTier) { badge.classList.remove('pop'); void badge.offsetWidth; badge.classList.add('pop'); lastTier = t; }

    // platform comparison bars (same followers, same relative engagement, base content type)
    var bars = $('ec-bars'), rel = er / plat.avg, vals = {}, max = 0;
    Object.keys(P).forEach(function (k) { vals[k] = rateFor(k, f, rel * P[k].avg, niche, 1); max = Math.max(max, vals[k]); });
    if (!bars.children.length) {
      Object.keys(P).forEach(function (k) {
        var d = document.createElement('div'); d.className = 'bc'; d.dataset.k = k;
        d.innerHTML = '<em></em><i></i><span>' + P[k].name + '</span>'; bars.appendChild(d);
      });
    }
    Array.prototype.forEach.call(bars.children, function (d) {
      var v = vals[d.dataset.k];
      d.querySelector('i').style.height = Math.max(4, v / max * 100) + '%';
      d.querySelector('i').style.opacity = d.dataset.k === key ? 1 : .45;
      d.querySelector('em').textContent = '$' + MI_short(v);
    });

    var engNote = er >= plat.avg * 1.5 ? 'well above average' : er >= plat.avg ? 'above average' : er >= plat.avg * 0.6 ? 'slightly below average' : 'below average';
    $('ec-break').innerHTML =
      '<li>Base benchmark <b>$' + plat.base + ' / 1K ' + plat.unit.toLowerCase() + '</b></li>' +
      '<li>Your engagement <b>' + er.toFixed(2) + '% (' + engNote + ')</b></li>' +
      '<li>Niche multiplier <b>' + niche.toFixed(2) + 'x</b></li>' +
      '<li>' + type[0] + ' multiplier <b>' + type[1].toFixed(2) + 'x</b></li>' +
      '<li>Sponsored income / month <b>' + money(mid * posts) + '</b></li>' +
      '<li>Affiliate income / month <b>' + money(aff) + '</b></li>';
  }
  function MI_short(v) { return window.MI && MI.fmtNum ? MI.fmtNum(v) : Math.round(v); }

  $('ec-fslider').value = toSlider(25000);
  $('ec-fslider').addEventListener('input', function () { $('ec-followers').value = fromSlider(this.value); update(); });
  $('ec-followers').addEventListener('input', function () {
    var n = Math.min(MAXF, Math.max(MINF, parseFloat(this.value) || MINF)); $('ec-fslider').value = toSlider(n); update();
  });
  $('ec-platform').addEventListener('change', function () { fillTypes(); update(); });
  document.querySelectorAll('[data-emode]').forEach(function (b) {
    b.addEventListener('click', function () {
      mode = b.dataset.emode;
      document.querySelectorAll('[data-emode]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
      $('ec-rate-box').hidden = mode !== 'rate';
      $('ec-count-box').hidden = mode === 'rate';
      update();
    });
  });
  ['ec-er', 'ec-likes', 'ec-comments', 'ec-niche', 'ec-type', 'ec-posts', 'ec-aff', 'ec-comm'].forEach(function (id) {
    $(id).addEventListener('input', update); $(id).addEventListener('change', update);
  });
  fillTypes();
  update();
})();
