/* CCTV camera planner */
(function () {
  'use strict';
  var TYPES = {
    door: ['Video doorbell (head-to-toe view)', 60, 200],
    tele: ['Dual-lens or 4K camera (plates, detail)', 90, 250],
    wide: ['Wide-angle 2K camera', 50, 150],
    ptz: ['Pan-tilt (360°) camera', 70, 200],
    lte: ['4G LTE solar camera', 130, 300],
    indoor: ['Indoor camera with privacy mode', 25, 80],
    flood: ['Floodlight camera', 90, 250]
  };
  function typeFor(z, net, prop) {
    if (z === 'front') return 'door';
    if (z === 'drive') return 'tele';
    if (z === 'gate') return net === 'none' ? 'lte' : 'tele';
    if (z === 'yard' || z === 'fence') return (prop === 'large' || prop === 'acre') ? 'ptz' : 'wide';
    if (z === 'garage' || z === 'back') return 'flood';
    if (z === 'shed') return net === 'good' ? 'wide' : 'lte';
    if (z === 'hall' || z === 'living' || z === 'stairs') return 'indoor';
    return 'wide';
  }
  SC.init('planner', function (form, box) {
    var o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
    var prop = SC.val(form, 'prop', 'house'), lvl = SC.num(form, 'lvl', 2), pow = SC.val(form, 'pow', 'few'), net = SC.val(form, 'net', 'good');
    var minP = 4 - lvl; // lvl1 -> p3 only, lvl2 -> p>=2, lvl3 -> all
    var big = prop === 'large' || prop === 'acre' || prop === 'biz';
    var rows = [], outN = 0, inN = 0, solarN = 0, lo = 0, hi = 0;
    form.querySelectorAll('input[data-zone]').forEach(function (c) {
      if (!c.checked) return;
      var p = +c.getAttribute('data-p'), z = c.value;
      if (p < minP && lvl < 3) return;
      var qty = 1;
      if (lvl === 3 && big && (z === 'yard' || z === 'fence' || z === 'drive')) qty = prop === 'acre' ? 3 : 2;
      if (prop === 'apt' && c.getAttribute('data-type') === 'out' && z !== 'front' && z !== 'patio') return;
      var t = typeFor(z, net, prop), T = TYPES[t];
      var outdoor = c.getAttribute('data-type') === 'out';
      var solar = outdoor && t !== 'door' && t !== 'flood' && (pow !== 'many' || z === 'gate' || z === 'shed' || z === 'fence');
      if (outdoor && t === 'flood' && pow === 'none') { T = ['Solar floodlight camera', 90, 230]; solar = true; }
      if (outdoor) outN += qty; else inN += qty;
      if (solar) solarN += qty;
      lo += T[1] * qty; hi += T[2] * qty;
      var power = !outdoor ? 'plug-in' : t === 'door' ? (pow === 'none' ? 'battery doorbell' : 'wired doorbell') : solar ? 'solar' : 'wired / plug-in';
      rows.push('<li><span><b>' + qty + '×</b> ' + SC.esc(c.getAttribute('data-label')) + ' — ' + T[0] + '</span><b>' + power + '</b></li>');
    });
    var total = outN + inN;
    o('total').innerHTML = total + ' <small>camera' + (total === 1 ? '' : 's') + '</small>';
    o('sum').innerHTML = total ? 'Recommended for a <strong>' + form.elements.prop.selectedOptions[0].text.toLowerCase() + '</strong> at <strong>' + ['essential', 'balanced', 'complete'][lvl - 1] + '</strong> coverage. Overlap fields of view slightly so nobody can walk between two cameras unseen.' : 'Tick at least one zone to build a plan.';
    o('out').textContent = outN; o('in').textContent = inN; o('solar').textContent = solarN;
    o('cost').textContent = total ? SC.money(lo) + '–' + SC.money(hi) : '—';
    o('plan').innerHTML = rows.join('') || '<li><span>No zones selected for this coverage level.</span></li>';
    var tips = [];
    if (solarN) tips.push('Check each solar spot gets 3+ hours of direct sun with the <a href="/tools/solar-camera-site-check/">Solar Site Check</a>.');
    if (net !== 'good') tips.push('Weak Wi‑Fi at the edges: add a mesh node or outdoor access point, or choose 4G cameras for the far spots (<a href="/tools/4g-data-and-storage-calculator/">estimate data use</a>).');
    if (outN >= 4) tips.push('With ' + outN + ' outdoor cameras, a local hub or NVR keeps footage in one place without per-camera subscriptions.');
    if (big) tips.push('On large lots, size the driveway/gate cameras with the <a href="/tools/camera-coverage-calculator/">coverage calculator</a> so plates are readable at the distance you need.');
    tips.push('Mount outdoor cameras 7–10 ft (2.1–3 m) high, angled down ~15–30°, out of easy reach.');
    o('tips').innerHTML = '<h4>Tips for this plan</h4><ul>' + tips.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>';
  });
})();
