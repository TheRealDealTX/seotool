/* Solar camera site suitability quiz */
(function () {
  'use strict';
  function gauge(el, score) {
    var a = Math.PI * (1 - score / 100), r = 80, cx = 90, cy = 90;
    var x = cx + r * Math.cos(a), y = cy - r * Math.sin(a);
    var col = score >= 70 ? '#15803d' : score >= 45 ? '#f59e0b' : '#c2410c';
    el.innerHTML = '<svg viewBox="0 0 180 100" aria-hidden="true"><path d="M10 90 A80 80 0 0 1 170 90" fill="none" stroke="#e3e8f0" stroke-width="14" stroke-linecap="round"/>' +
      '<path d="M10 90 A80 80 0 0 1 ' + x.toFixed(1) + ' ' + y.toFixed(1) + '" fill="none" stroke="' + col + '" stroke-width="14" stroke-linecap="round"/></svg><div class="val">' + score + '</div>';
  }
  SC.init('site-check', function (form, box) {
    var o = function (k) { return box.querySelector('[data-o="' + k + '"]'); };
    var g = function (n) { return SC.num(form, n, 0); };
    var sun = g('sun'), shade = g('shade'), face = g('face'), clim = g('clim'), act = g('act'), panel = g('panel'), net = g('net');
    // Energy score (0-100)
    var energy = sun / 4 * 34 + shade / 3 * 16 + face / 2 * 12 + clim / 3 * 16 + act / 3 * 14 + Math.min(panel, 2) / 2 * 8;
    if (panel === 3) energy = Math.min(100, energy + 8 + (3 - shade) * 4 + (4 - sun) * 3); // panel can be moved into sun
    var score = Math.round(SC.clamp(energy, 0, 100));
    gauge(o('gauge'), score);
    var v = o('verdict'), recs = [];
    if (score >= 70) { v.className = 'verdict ok'; v.innerHTML = '✔ <span><strong>Great solar site.</strong> A standard 3–6 W camera panel should keep the battery topped up most of the year.</span>'; }
    else if (score >= 45) { v.className = 'verdict mid'; v.innerHTML = '◐ <span><strong>Workable with the right setup.</strong> Expect occasional top-ups in winter unless you upsize the panel or cut down triggers.</span>'; }
    else { v.className = 'verdict bad'; v.innerHTML = '✖ <span><strong>Solar will struggle here.</strong> Move the panel, add capacity, or consider a wired/plug-in camera for this spot.</span>'; }
    if (sun <= 1) recs.push('Under 2 hours of sun is the main problem. Use a separate panel on an extension cable (most brands sell 3–5 m / 10–16 ft cables) to reach a sunnier spot.');
    if (shade === 1) recs.push('Low winter sun is blocked: mount the panel higher (roof edge, pole) or steeper. Check the <a href="/tools/solar-panel-angle-calculator/">panel angle calculator</a> for your winter tilt.');
    if (shade === 2) recs.push('Deciduous trees shade less in winter, which is when you need it most. Re-check in summer and clean leaves off the panel in fall.');
    if (face === 1) recs.push('East/west facing panels collect roughly 15–25% less than south-facing ones. Pick a 6 W panel instead of 3 W to compensate.');
    if (face === 0) recs.push('A panel facing away from the sun will not keep up. Mount it on a different wall, fence post or pole and run the cable.');
    if (clim <= 1) recs.push('Grey winters: budget for 1–2 peak sun hours a day from November to February. A larger battery or a second panel (where supported) bridges the gap.');
    if (act <= 1) recs.push('Lots of motion: narrow activity zones, enable person/vehicle detection and lower sensitivity. Every avoided clip saves power.');
    if (panel === 1 && score < 70) recs.push('Built-in panels are small (usually 1–3 W). If your camera supports an external panel, add one.');
    if (net === 2) recs.push('Weak Wi‑Fi makes the camera transmit longer and harder, draining the battery. Add a mesh node or outdoor access point nearer the camera.');
    if (net === 1) recs.push('No Wi‑Fi but good cell signal: a 4G SIM solar camera fits. 4G radios use more power, so pair it with a 5–10 W panel.');
    if (net === 0) recs.push('No Wi‑Fi or cell signal: you can record locally to microSD, but you will get no phone alerts. A point-to-point Wi‑Fi bridge can extend your network up to several hundred metres.');
    if (!recs.length) recs.push('Your site ticks every box. Mount the panel facing ' + 'the equator at roughly your latitude in degrees and you are set.');
    o('recs').innerHTML = recs.map(function (r) { return '<li>' + r + '</li>'; }).join('');
  });
})();
