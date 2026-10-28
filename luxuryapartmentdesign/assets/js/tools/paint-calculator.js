(function () {
  'use strict';
  var L = window.LAD, form = document.getElementById('paint-form'), out = document.getElementById('paint-result');
  if (!form) return;
  function cans(gal) {
    var g = Math.floor(gal), rem = gal - g, q = Math.ceil(rem * 4 - 0.001);
    if (q === 4) { g++; q = 0; }
    if (q === 3) { g++; q = 0; }                       // three quarts cost about as much as a gallon
    return { g: g, q: q, txt: (g ? g + ' gallon' + (g > 1 ? 's' : '') : '') + (g && q ? ' + ' : '') + (q ? q + ' quart' + (q > 1 ? 's' : '') : '') || '1 quart' };
  }
  L.bind(form, function (v) {
    var wall = 2 * (v.len + v.wid) * v.hei - v.doors * 20 - v.wins * 15;
    wall = Math.max(0, wall);
    var ceil = v.ceiling ? v.len * v.wid : 0;
    var cov = v.cov || 350, coats = v.coats || 2;
    var wallGal = wall * coats / cov, ceilGal = ceil * coats / cov, primerGal = v.primer ? (wall + ceil) / cov : 0;
    var w = cans(wallGal), c = cans(ceilGal), p = cans(primerGal);
    var cost = (w.g + w.q * 0.35 + c.g + c.q * 0.35) * v.price + (p.g + p.q * 0.35) * v.price * 0.7;
    out.innerHTML = '<p class="result__label">Wall paint to buy</p><p class="result__big">' + w.txt + '</p>' +
      '<p class="result__sub">' + L.fmt(wall, 0) + ' sq ft of wall × ' + coats + ' coat' + (coats > 1 ? 's' : '') + ' ÷ ' + cov + ' sq ft per gallon = ' + L.fmt(wallGal, 2) + ' gallons</p>' +
      '<div class="result-stats">' +
      '<div class="stat"><b>' + L.fmt(wall, 0) + '</b><span>sq ft of wall</span></div>' +
      (v.ceiling ? '<div class="stat"><b>' + c.txt + '</b><span>ceiling paint (' + L.fmt(ceil, 0) + ' sq ft)</span></div>' : '') +
      (v.primer ? '<div class="stat"><b>' + p.txt + '</b><span>primer, one coat</span></div>' : '') +
      '<div class="stat"><b>$' + L.fmt(cost, 0) + '</b><span>estimated paint cost</span></div></div>' +
      '<ul><li>We subtract 20 sq ft per door and 15 sq ft per window.</li>' +
      '<li>Coverage of 350 sq ft per gallon is conservative; textured or porous walls can take more.</li>' +
      '<li>Buy all wall paint at once (or ask the store to box it) so the color matches from can to can.</li>' +
      (v.primer ? '' : '<li>Going from a dark color to a light one, or painting over patches? Tick primer.</li>') +
      '<li>Renting? Check your lease before painting, and keep the original color name so you can repaint when you move.</li></ul>';
  });
})();
